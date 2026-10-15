"""Regression checks for the isolated 2027 web kit, not publication or acceptance.

Owns one headless Edge process with a temporary profile; closes only that process.
Checks actual rendered geometry as well as semantic ownership/content projection.
"""
from __future__ import annotations

import argparse
import base64
import copy
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from urllib.parse import quote, unquote, urlsplit, urlunsplit

sys.dont_write_bytecode = True
from bs4 import BeautifulSoup
import requests
import websocket
from zo_web_2027_preview import BRAND_THOUGHT, REPO, audit_path, dump, footer_data, inventory, projection, sha, without_requested_ui, without_site_footer


class Browser:
    def __init__(self, ws_url: str):
        self.ws = websocket.create_connection(ws_url, timeout=15, origin='http://localhost')
        self.counter = 0

    def call(self, method, params=None):
        self.counter += 1
        ident = self.counter
        self.ws.send(json.dumps({'id': ident, 'method': method, 'params': params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get('id') != ident:
                continue
            if 'error' in message:
                raise RuntimeError(f'{method}: {message["error"]}')
            return message.get('result', {})

    def evaluate(self, code):
        response = self.call('Runtime.evaluate', {'expression': code, 'returnByValue': True, 'awaitPromise': True})
        if response.get('exceptionDetails'):
            raise RuntimeError(str(response['exceptionDetails']))
        return response.get('result', {}).get('value')

    def ready(self):
        for _ in range(80):
            if self.evaluate('document.readyState') == 'complete':
                self.evaluate("document.fonts.ready.then(()=>Promise.all([...document.images].map(i=>{i.loading='eager';return i.decode().catch(()=>null)})))")
                time.sleep(.1)
                return
            time.sleep(.1)
        raise TimeoutError('Page not ready')

    def navigate(self, url):
        self.call('Page.navigate', {'url': url}); time.sleep(.15); self.ready()

    def viewport(self, width, height):
        self.call('Emulation.setDeviceMetricsOverride', {'width': width, 'height': height, 'deviceScaleFactor': 1, 'mobile': width <= 500})

    def click(self, selector):
        self.evaluate('document.querySelector(' + json.dumps(selector) + ').click()'); time.sleep(.15)

    def key(self, key, number, text=None):
        args = {'type': 'keyDown', 'key': key, 'windowsVirtualKeyCode': number}
        if text is not None:
            args['text'] = text
        self.call('Input.dispatchKeyEvent', args)
        self.call('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': key, 'windowsVirtualKeyCode': number})
        time.sleep(.15)

    def screenshot(self, output: Path):
        output.write_bytes(base64.b64decode(self.call('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': False})['data']))


GEOMETRY = r"""(() => {
  const reader=document.querySelector('.reader-content'), visible=n=>!!n.getClientRects().length&&!n.closest('[hidden]');
  const regions=[...reader.querySelectorAll('.reading-region')].filter(visible);
  const text=[...reader.querySelectorAll('h2,h3,h4,h5,p,li,summary,.role')].filter(visible);
  const orphans=text.filter(n=>!n.closest('.reading-region'));
  const overflow=text.filter(n=>!n.closest('.table-scroll,.figure-viewport,.r1-table-scroll-x')&&n.scrollWidth>n.clientWidth+2);
  const axes=text.filter(n=>n.matches('h2,h3,h4,h5,.role,summary')).map(n=>{
    const r=n.closest('.reading-region'); if(!r)return {text:n.textContent.slice(0,40),delta:999};
    return {text:n.textContent.slice(0,40),delta:n.getBoundingClientRect().left-r.getBoundingClientRect().left-parseFloat(getComputedStyle(r).paddingLeft)};
  }).filter(n=>Math.abs(n.delta)>1.3);
  return {
    orphan:orphans.map(n=>n.textContent.slice(0,50)), overflow:overflow.map(n=>n.textContent.slice(0,50)), axes,
    fits:document.documentElement.scrollWidth<=innerWidth+1,
    nested:reader.querySelectorAll('.reading-region .reading-region').length,
    white:regions.every(n=>getComputedStyle(n).backgroundColor==='rgb(255, 255, 255)'),
    widths:regions.every(n=>Math.abs(n.getBoundingClientRect().width-reader.getBoundingClientRect().width)<2),
    gaps:regions.slice(1).every((n,i)=>n.getBoundingClientRect().top-regions[i].getBoundingClientRect().bottom>=20),
    regionCount:regions.length, readerWidth:reader.getBoundingClientRect().width,
    rightMargin:innerWidth-reader.getBoundingClientRect().right,
    loaded:[...document.images].every(n=>n.complete&&n.naturalWidth>0)
  };
})()"""


def style_metrics(browser, root_selector):
    return browser.evaluate("""(() => {
      const root=document.querySelector(%s);
      return ['.hero','.hero h1','.hero-art','.rail','.site-top',%s,%s+' .reading-region'].map(selector=>{
        const n=document.querySelector(selector),c=getComputedStyle(n),r=n.getBoundingClientRect();
        return [r.x,r.y,r.width,r.height,c.fontFamily,c.fontSize,c.lineHeight,c.paddingLeft,c.paddingRight,c.backgroundColor];
      });
    })()""" % (json.dumps(root_selector), json.dumps(root_selector), json.dumps(root_selector)))


ABOVE_FOOTER_METRICS = r"""(() => {
  const nodes=[...document.querySelectorAll('.site-top,.site-top *, .rail,.rail *, main,main *, .mobile-trigger,.mobile-trigger *')];
  const props=['fontFamily','fontSize','fontWeight','lineHeight','color','backgroundColor','paddingLeft','paddingRight','paddingTop','paddingBottom','marginLeft','marginRight','marginTop','marginBottom','borderRadius','display'];
  return nodes.filter(n=>!!n.getClientRects().length).map(n=>{
    const r=n.getBoundingClientRect(),c=getComputedStyle(n),round=x=>Math.round(x*1000)/1000;
    return [n.tagName,n.id,n.className,round(r.left),round(r.top+scrollY),round(r.width),round(r.height),...props.map(p=>c[p])];
  });
})()"""
READING_METRICS = ABOVE_FOOTER_METRICS.replace('.site-top,.site-top *, .rail,.rail *, main,main *, .mobile-trigger,.mobile-trigger *', 'main,main *')


def complete_site_footer(doc, data):
    nodes = doc.select('footer#site-footer[role=contentinfo]')
    if len(nodes) != 1 or nodes[0].find_parent('main') or nodes[0].find_parent(class_='support-region'):
        return False
    def rendered(value):
        url = urlsplit(value or '')
        path = url.path[:-4] + '.html' if url.path.endswith('.qmd') else url.path
        return urlunsplit((url.scheme, url.netloc, path, url.query, url.fragment))
    actual = [(rendered(n.get('data-canonical-href')), n.get_text(' ', strip=True).replace(' ↗', ''))
              for n in nodes[0].select('nav a[href]')]
    expected = [(rendered(n['canonical_href']), n['label']) for n in data['information'] + data['social']]
    return actual == expected and data['copyright'] in nodes[0].get_text(' ', strip=True)


class Checks:
    def __init__(self, output):
        self.output = output
        self.checks = []
        self.errors = []

    def check(self, name, actual, expected=True):
        passed = actual == expected
        self.checks.append({'name': name, 'pass': passed, 'actual': actual, 'expected': expected})
        if not passed:
            print('FAIL', name, str(actual)[:600], flush=True)

    def static(self):
        manifest = json.loads((self.output / 'build-manifest.json').read_text(encoding='utf-8'))
        home = BeautifulSoup((self.output / 'home-reading.html').read_text(encoding='utf-8'), 'html.parser')
        root = home.select_one('.reader-content')
        hero = home.select_one('.hero')
        source = manifest['home']['source_inventory']
        self.check('Home exact text order', projection(hero) + ' ' + projection(root), source['text'])
        self.check('Home exact ID order', [n['id'] for n in hero.select('[id]')] + [n['id'] for n in root.select('[id]')], source['ids'])
        self.check('Home exact heading roles', inventory(root)['headings'], [tuple(n) for n in source['headings']])
        self.check('Home canonical data checked by builder', manifest['home']['preserved_projection'])
        self.check('Kit source files still match the build', [name for name, digest in manifest['kit_source_hashes'].items() if not (REPO / name).is_file() or sha(REPO / name) != digest], [])
        self.check('Builder still matches the build', sha(REPO / 'scripts/zo_web_2027_preview.py'), manifest['builder_sha256'])
        self.check('D0 precedes G01 and G02', [n['data-package-id'] for n in root.select('[data-package-id]')], ['d0', 'r1_g01', 'r1_g02'])
        self.check('Home does not load the R1 tab controller', [n['src'] for n in home.select('script[src]')], ['site-ui.js'])
        self.footer_info = manifest['home'].get('site_footer')
        self.inline_ui = bool(self.footer_info and self.footer_info.get('ui_revision') == 'FB027')
        styles = ['reading-regions.css', 'web-shell.css', 'course-home.css']
        if self.footer_info:
            styles.append('site-footer.css')
            current_footer = footer_data()
            self.check('Home global footer complete and separate from support', complete_site_footer(home, current_footer))
            self.check('Footer link destinations equal the canonical mapping', [n['href'] for n in home.select('#site-footer nav a')], [n['preview_href'] for n in self.footer_info['information'] + self.footer_info['social']])
            self.check('Footer canonical config hash is current', self.footer_info['source_sha256'], current_footer['source_sha256'])
            self.footer_baseline = REPO / self.footer_info['baseline']
            self.check('Footer original Home baseline hash unchanged', sha(self.footer_baseline), self.footer_info['baseline_sha256'])
            compare = without_requested_ui if self.inline_ui else without_site_footer
            self.check('Home DOM outside explicitly requested changes preserved', compare((self.output / 'home-reading.html').read_text(encoding='utf-8')), compare(self.footer_baseline.read_text(encoding='utf-8')))
            before = json.loads((self.output / ('ui-before.json' if self.inline_ui else 'footer-before.json')).read_text(encoding='utf-8'))
            self.check('Footer preserves all frozen original CSS/JS/templates/profile/previews', [name for name, digest in before.items() if sha(REPO / name) != digest], [])
            frozen_runtime = ['reading-regions.css','web-shell.css','course-home.css','r1-controller.js','site-footer.css'] if self.inline_ui else ['reading-regions.css','web-shell.css','course-home.css','site-ui.js','r1-controller.js','g01-kit.html']
            for name in frozen_runtime:
                self.check('Footer leaves baseline runtime unchanged: ' + name, sha(self.output / name), sha(self.footer_baseline.parent / name))
            # Do not mistake the prototype-note <footer> inside Support for the site footer.
            negative = copy.deepcopy(home)
            negative.select_one('#site-footer').decompose()
            self.check('Negative footer guard rejects omission despite prototype-note footer', not complete_site_footer(negative, current_footer) and bool(negative.select_one('footer.prototype-note')))
            css = (self.output / 'site-footer.css').read_text(encoding='utf-8')
            self.check('Footer stylesheet selectors are local only', all(selector.strip().startswith('.zo-site-footer') for rule in re.findall(r'(?:^|[{}])\s*([^{}]+)\{', re.sub(r'/\*.*?\*/', '', css, flags=re.S)) if not rule.lstrip().startswith('@') for selector in rule.split(',')))
        if self.inline_ui:
            styles.append('appearance-inline.css')
        self.check('Home only loads current styles', [n['href'] for n in home.select('link[rel=stylesheet]')], styles)
        self.check('Every registered resource matches source hash', [name for name, item in manifest['resources'].items() if sha(self.output / name) != item['sha256']], [])
        for name in ['home-reading.html', 'g01-kit.html']:
            page = BeautifulSoup((self.output / name).read_text(encoding='utf-8'), 'html.parser')
            self.check(name + ' every content link belongs to a reading beat', [a.get('href') for a in page.select('.reader-content a') if not a.find_parent(class_='reading-region')], [])
            missing = []
            parsed_targets = {(self.output / name).resolve(): page}
            for n in page.select('[src],a[href],link[href]'):
                value = n.get('src', n.get('href', ''))
                split = urlsplit(value)
                if split.scheme or split.netloc:
                    continue
                path = (self.output / unquote(split.path)).resolve() if split.path else self.output / name
                if not path.is_file():
                    missing.append(value); continue
                if split.fragment and path.suffix == '.html':
                    if path not in parsed_targets:
                        parsed_targets[path] = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
                    target = parsed_targets[path]
                    if not target.find(id=unquote(split.fragment)):
                        missing.append(value)
            self.check(name + ' all local resources/links/fragments exist', missing, [])
        reference = REPO / manifest['g01_reference']['source']
        old = BeautifulSoup(reference.read_text(encoding='utf-8'), 'html.parser')
        new = BeautifulSoup((self.output / 'g01-kit.html').read_text(encoding='utf-8'), 'html.parser')
        self.g01_source_hidden = [n.get('id') for n in old.select('.zo-on-thi-package [hidden]')]
        self.check('G01 all math/content/IDs/disclosures preserved', inventory(new.select_one('.reader-content')), inventory(old.select_one('.zo-on-thi-package')))
        self.check('G01 full document ID order preserved', [n['id'] for n in new.select('[id]')], [n['id'] for n in old.select('[id]')])
        self.check('G01 does not load Home extension styles', [n['href'] for n in new.select('link[rel=stylesheet]')], ['reading-regions.css', 'web-shell.css'] + (['appearance-inline.css'] if self.inline_ui else []))
        if self.inline_ui:
            self.check('G01 DOM outside requested changes preserved', without_requested_ui((self.output / 'g01-kit.html').read_text(encoding='utf-8')), without_requested_ui((self.footer_baseline.parent / 'g01-kit.html').read_text(encoding='utf-8')))
            for name, page in [('Home', home), ('G01', new)]:
                self.check(name + ' full brand phrase exact', page.select_one('.brand-thought').get_text(' ', strip=True), BRAND_THOUGHT)
                self.check(name + ' six accessible radios and one grayscale button', len(page.select('.appearance--inline input[type=radio][aria-label]')) == 6 and len(page.select('.appearance--inline button#grayscale[aria-pressed][aria-label]')) == 1)
                self.check(name + ' controls have no visible labels or dropdown', page.select_one('.appearance').get_text(' ', strip=True) == '' and not page.select_one('.appearance summary'))
            self.check('Footer brand phrase exact', home.select_one('.zo-site-footer__brand p').get_text(' ', strip=True), BRAND_THOUGHT)
        return manifest

    def footer(self, browser, width):
        if not self.footer_info:
            return
        from PIL import Image, ImageChops
        url = (self.output / 'home-reading.html').as_uri()
        measures = []
        snapshots = {}
        for label, address in [('before', self.footer_baseline.as_uri()), ('after', url)]:
            browser.navigate(address)
            browser.click('[name=background][value=yellow-1]')
            browser.evaluate('document.querySelector(".appearance").open=false;scrollTo(0,0)'); time.sleep(.15)
            measures.append(browser.evaluate(READING_METRICS if self.inline_ui else ABOVE_FOOTER_METRICS))
            if width in [1440,390]:
                for scene, y in [('cover', 0), ('reading', 1250), ('support', None)]:
                    if label == 'after':
                        y = snapshots[scene][0][1]
                    if y is None:
                        y = browser.evaluate('document.getElementById("ung-ho").getBoundingClientRect().top+scrollY-88')
                    browser.evaluate(f'scrollTo(0,{y})'); time.sleep(.2)
                    actual_y = browser.evaluate('scrollY')
                    path = self.output / 'images' / f'footer-{label}-{scene}-{width}.png'
                    browser.screenshot(path)
                    snapshots.setdefault(scene, []).append((path, actual_y))
        scope = 'main content' if self.inline_ui else 'all visible elements above footer'
        self.check(f'Footer/{width} {scope} keeps exact geometry/typography/colors', measures[1], measures[0])
        dump(self.output / f'footer-layout-{width}.json', {'before': measures[0], 'after': measures[1]})
        for scene, pair in snapshots.items():
            (old, old_y), (new, new_y) = pair
            self.check(f'Footer/{width}/{scene} unchanged scroll position', new_y, old_y)
            # A longer document changes the native scrollbar thumb, not the page design.
            content_width = browser.evaluate('document.documentElement.clientWidth')
            footer_top = browser.evaluate('document.getElementById("site-footer").getBoundingClientRect().top+scrollY') - new_y
            height = min(Image.open(new).height, max(0, int(footer_top)))
            left = browser.evaluate('document.querySelector(".workspace").getBoundingClientRect().left') if self.inline_ui else 0
            top = 64 if self.inline_ui else 0
            box = (int(left), top, content_width, height)
            difference = ImageChops.difference(Image.open(old).convert('RGB').crop(box), Image.open(new).convert('RGB').crop(box))
            # Chromium can round anti-aliased border pixels by one RGB level.
            # Geometry/styles are compared exactly separately, not fuzzily.
            max_delta = max(high for low, high in difference.getextrema())
            self.check(f'Footer/{width}/{scene} above-footer pixels within one RGB rounding level', max_delta <= 1)
            dump(self.output / f'footer-pixels-{scene}-{width}.json', {'max_channel_delta': max_delta,
                 'difference_bbox': difference.getbbox(), 'compared_box': box, 'allowed_channel_rounding': 1})
        browser.navigate(url)
        browser.evaluate('scrollTo(0,document.documentElement.scrollHeight)'); time.sleep(.15)
        metrics = browser.evaluate(r"""(() => {
          const f=document.getElementById('site-footer'),r=f.getBoundingClientRect(),s=document.getElementById('ung-ho').getBoundingClientRect();
          const inner=f.querySelector('.zo-site-footer__inner').getBoundingClientRect(),reader=document.querySelector('.reader-content').getBoundingClientRect();
          const links=[...f.querySelectorAll('nav a')],trigger=document.querySelector('.mobile-trigger'),t=trigger.getBoundingClientRect();
          return {afterSupport:r.top>=s.bottom,static:getComputedStyle(f).position==='static',aligned:Math.abs(inner.left-reader.left)<1&&Math.abs(inner.width-reader.width)<1,
            links:links.length,visible:links.every(n=>{const q=n.getBoundingClientRect();return q.top>=64&&q.bottom<=innerHeight&&q.left>=0&&q.right<=innerWidth}),
            targetSize:links.every(n=>n.getBoundingClientRect().height>=44),notCovered:links.every(n=>{const q=n.getBoundingClientRect();return !t.width||q.bottom<=t.top||q.right<=t.left||q.left>=t.right}),
            white:getComputedStyle(f).backgroundColor==='rgb(255, 255, 255)',fits:document.documentElement.scrollWidth<=innerWidth+1};
        })()""")
        for key in ['afterSupport','static','aligned','visible','targetSize','notCovered','white','fits']:
            self.check(f'Footer/{width} {key}', metrics[key])
        self.check(f'Footer/{width} six canonical links', metrics['links'], 6)
        browser.evaluate('document.querySelector("#site-footer nav a").focus()')
        browser.key('Tab', 9)
        self.check(f'Footer/{width} keyboard reaches next information link', browser.evaluate('document.activeElement.textContent.trim()'), 'Triết lí và định hướng')
        self.check(f'Footer/{width} keyboard focus visible', browser.evaluate('getComputedStyle(document.activeElement).outlineStyle'), 'solid')
        browser.evaluate('document.activeElement.blur();scrollTo(0,document.documentElement.scrollHeight)')
        browser.screenshot(self.output / 'images' / f'home-footer-{width}.png')
        if width in [1440,390]:
            for theme in ['yellow-1','yellow-2','red-1','red-2','gray-2','gray-3']:
                browser.click(f'[name=background][value={theme}]')
                self.check(f'Footer/{width}/{theme} footer remains white', browser.evaluate('getComputedStyle(document.getElementById("site-footer")).backgroundColor'), 'rgb(255, 255, 255)')
            browser.click('#grayscale')
            self.check(f'Footer/{width} grayscale includes footer without moving fixed navigation', browser.evaluate('document.documentElement.classList.contains("grayscale")&&getComputedStyle(document.documentElement).filter==="grayscale(1)"&&getComputedStyle(document.body).filter==="none"'))
            browser.click('#grayscale'); browser.click('[name=background][value=yellow-1]')
            browser.call('Emulation.setScriptExecutionDisabled', {'value': True}); browser.navigate(url)
            self.check(f'Footer/{width} no JS footer and all six links remain available', browser.evaluate('document.getElementById("site-footer").getClientRects().length>0&&document.querySelectorAll("#site-footer nav a[href]").length===6'))
            browser.evaluate('scrollTo(0,document.documentElement.scrollHeight)')
            browser.screenshot(self.output / 'images' / f'home-footer-nojs-{width}.png')
            browser.call('Emulation.setScriptExecutionDisabled', {'value': False})

    def appearance(self, browser, width):
        if not self.inline_ui:
            return
        for page in ['home-reading.html','g01-kit.html']:
            browser.navigate((self.output / page).as_uri())
            prefix = f'Inline/{page}/{width}'
            state = browser.evaluate(r"""(() => {
              const controls=[...document.querySelectorAll('.appearance--inline .swatches label,.appearance--inline .gray-toggle')];
              const r=controls.map(n=>n.getBoundingClientRect());
              return {count:r.length,oneRow:new Set(r.map(q=>q.top)).size===1,
                visible:r.every(q=>q.left>=0&&q.right<=innerWidth&&q.top>=0&&q.bottom<=64),
                targets:r.every(q=>q.width>=24&&q.height>=44),fits:document.documentElement.scrollWidth<=innerWidth+1,
                clearBrand:innerWidth>=1000||document.querySelector('.site-top>a:first-child img').getBoundingClientRect().right+4<=r[0].left,
                selected:document.querySelectorAll('[name=background]:checked').length===1,
                circles:[...document.querySelectorAll('[name=background]')].every(n=>getComputedStyle(n).appearance==='none'&&getComputedStyle(n).borderRadius==='50%'),
                selectedRing:getComputedStyle(document.querySelector('[name=background]:checked')).boxShadow!=='none'};
            })()""")
            self.check(prefix + ' seven visible controls', state['count'], 7)
            for key in ['oneRow','visible','targets','fits','clearBrand','selected','circles','selectedRing']:
                self.check(prefix + ' ' + key, state[key])
            if width in [1440,390]:
                for theme in ['gray-3','gray-2','yellow-1','yellow-2','red-1','red-2']:
                    point = browser.evaluate(f'(()=>{{const r=document.querySelector("[name=background][value={theme}]").closest("label").getBoundingClientRect();return {{x:r.x+r.width/2,y:r.y+r.height/2}}}})()')
                    browser.call('Input.dispatchMouseEvent', {'type':'mousePressed','button':'left','clickCount':1,**point})
                    browser.call('Input.dispatchMouseEvent', {'type':'mouseReleased','button':'left','clickCount':1,**point}); time.sleep(.1)
                    self.check(prefix + '/' + theme + ' actual pointer selects colored circle', browser.evaluate(f'document.querySelector("[name=background][value={theme}]").checked'))
                    self.check(prefix + '/' + theme + ' canvas matches existing token', browser.evaluate(f'getComputedStyle(document.documentElement).getPropertyValue("--canvas").trim()===getComputedStyle(document.documentElement).getPropertyValue("--theme-{theme}").trim()'))
                    self.check(prefix + '/' + theme + ' paper remains white', browser.evaluate(GEOMETRY)['white'])
                browser.evaluate('document.querySelector("[name=background][value=gray-3]").focus()')
                browser.key('ArrowRight',39)
                self.check(prefix + ' native radio keyboard changes selection', browser.evaluate('document.querySelector("[name=background][value=gray-2]").checked'))
                self.check(prefix + ' keyboard focus visible', browser.evaluate('getComputedStyle(document.activeElement).outlineStyle'), 'solid')
                browser.evaluate('document.getElementById("grayscale").focus()'); browser.key('Enter',13,'\r')
                self.check(prefix + ' grayscale keyboard toggle/state', browser.evaluate('document.documentElement.classList.contains("grayscale")&&document.getElementById("grayscale").getAttribute("aria-pressed")==="true"'))
                browser.call('Page.reload'); browser.ready()
                self.check(prefix + ' reload retains background and grayscale', browser.evaluate('document.querySelector("[name=background][value=gray-2]").checked&&document.getElementById("grayscale").getAttribute("aria-pressed")==="true"'))
                browser.click('#grayscale'); browser.click('[name=background][value=yellow-1]')
                self.check(prefix + ' grayscale can be disabled', browser.evaluate('!document.documentElement.classList.contains("grayscale")&&document.getElementById("grayscale").getAttribute("aria-pressed")==="false"'))
            browser.evaluate('document.activeElement.blur();scrollTo(0,0)')
            browser.screenshot(self.output / 'images' / f'inline-{page.removesuffix(".html")}-{width}.png')
        self.errors += browser.evaluate('window.zoQaErrors||[]')

    def home(self, browser, width):
        url = (self.output / 'home-reading.html').as_uri()
        browser.navigate(url)
        state = browser.evaluate(GEOMETRY)
        for field in ['orphan', 'overflow', 'axes']:
            self.check(f'Home/{width} {field}', state[field], [])
        for field in ['fits', 'white', 'widths', 'gaps', 'loaded']:
            self.check(f'Home/{width} {field}', state[field])
        self.check(f'Home/{width} no nested regions', state['nested'], 0)
        self.check(f'Home/{width} nine content beats', state['regionCount'], 9)
        self.check(f'Home/{width} bounded reading width', state['readerWidth'] <= 816)
        self.check(f'Home/{width} package summaries use the full reading axis', browser.evaluate("(()=>{const paragraphs=[...document.querySelectorAll('.zo-on-thi-package__copy section.level3>p')];return paragraphs.length===6&&paragraphs.every(n=>Math.abs(n.getBoundingClientRect().width-n.closest('.zo-on-thi-package').getBoundingClientRect().width)<2)})()"))
        if width >= 1000:
            self.check(f'Home/{width} breathing space right', state['rightMargin'] >= 24)
        browser.evaluate('document.querySelector(".home-nav a:last-child").hash');
        browser.evaluate('document.getElementById(decodeURIComponent(document.querySelector(".home-nav a:last-child").hash.slice(1))).scrollIntoView({block:"start"})'); time.sleep(.12)
        self.check(f'Home/{width} last reading beat marks its own nav item', browser.evaluate('document.querySelector(".home-nav a[aria-current]")===document.querySelector(".home-nav a:last-child")'))
        browser.evaluate('scrollTo(0,0)'); time.sleep(.12)
        if width in [1440, 390]:
            browser.screenshot(self.output / 'images' / f'home-cover-{width}.png')
            for ident, label in [('giới-thiệu', 'orientation'), ('học-theo-cách-nào', 'method'), ('tám-mạch', 'strands'), ('hoc-lieu-hien-co', 'packages'), ('bắt-đầu-từ-đâu', 'start'), ('ung-ho', 'support')]:
                browser.evaluate('document.getElementById(' + json.dumps(ident) + ').scrollIntoView({block:"start"})'); time.sleep(.12)
                browser.screenshot(self.output / 'images' / f'home-{label}-{width}.png')
            for theme in ['yellow-1','yellow-2','red-1','red-2','gray-2','gray-3']:
                browser.click(f'[name=background][value={theme}]')
                self.check(f'Home/{width}/{theme} paper always white', browser.evaluate(GEOMETRY)['white'])
                self.check(f'Home/{width}/{theme} visible current choice', browser.evaluate(f'document.querySelector("[name=background][value={theme}]").checked'))
            browser.click('#grayscale')
            self.check(f'Home/{width} grayscale', browser.evaluate('document.documentElement.classList.contains("grayscale")'))
            browser.click('#grayscale'); browser.click('[name=background][value=yellow-1]')
            positions = []
            for y in [250, 450, 850, 1250, 850, 450]:
                browser.evaluate(f'scrollTo(0,{y})'); time.sleep(.08)
                positions.append(browser.evaluate('({y:scrollY,top:document.querySelector(".site-top").getBoundingClientRect().top,nav:document.querySelector(innerWidth>=1000?".rail":".mobile-trigger").getBoundingClientRect().top})'))
            self.check(f'Home/{width} no scroll jump', [n['y'] for n in positions], [250, 450, 850, 1250, 850, 450])
            self.check(f'Home/{width} stable toolbar', len({n['top'] for n in positions}), 1)
            self.check(f'Home/{width} stable navigation', len({n['nav'] for n in positions}), 1)
            if width == 390:
                browser.evaluate('document.querySelector(".mobile-trigger").focus()'); browser.key('Enter', 13, '\r')
                self.check('Home mobile keyboard opens drawer', browser.evaluate('document.querySelector("#mobile-nav").open'))
                browser.screenshot(self.output / 'images' / 'home-drawer-390.png')
                browser.key('Escape', 27)
                self.check('Home mobile Escape closes/focus returns', browser.evaluate('!document.querySelector("#mobile-nav").open&&document.activeElement.matches(".mobile-trigger")'))
                browser.click('.mobile-trigger'); browser.click('.home-nav a[href="#hoc-lieu-hien-co"]')
                self.check('Home drawer link closes and targets actual section', browser.evaluate('!document.querySelector("#mobile-nav").open&&decodeURIComponent(location.hash)==="#hoc-lieu-hien-co"&&document.getElementById("hoc-lieu-hien-co").getBoundingClientRect().top>=63'))
                self.check('Home drawer link marks current navigation', browser.evaluate('document.querySelector(".home-nav a[aria-current]").hash'), '#hoc-lieu-hien-co')
                browser.click('.mobile-trigger'); browser.viewport(1000,960); time.sleep(.15)
                self.check('Resize closes drawer and returns actual nav', browser.evaluate('!document.querySelector("#mobile-nav").open&&!!document.querySelector(".rail .home-nav")'))
                browser.viewport(390,844)
            for ident in ['hoc-lieu-hien-co', 'bắt-đầu-từ-đâu']:
                browser.navigate(url + '#' + quote(ident))
                self.check(f'Home/{width} deep-link {ident} not covered', browser.evaluate(f'document.getElementById({json.dumps(ident)}).getBoundingClientRect().top>=63'))
                browser.call('Page.reload'); browser.ready()
                self.check(f'Home/{width} reload keeps target', browser.evaluate('decodeURIComponent(location.hash)'), '#' + ident)
            browser.navigate(url + '#hoc-lieu-hien-co')
            browser.click('[data-package-id=r1_g01] a'); browser.ready()
            self.check(f'Home/{width} G01 entry opens approved reference', browser.evaluate('location.pathname.endsWith("g01-kit.html")&&document.querySelector(".r1-tab[aria-selected=true]").id==="r1-tab-bat-dau"'))
            browser.evaluate('history.back()'); time.sleep(.2); browser.ready()
            self.check(f'Home/{width} Back restores Home', browser.evaluate('location.pathname.endsWith("home-reading.html")'))
            # Guards must reject reintroducing the exact classes of old errors.
            browser.evaluate("window.savedHeading=document.getElementById('giới-thiệu').querySelector('h2');window.savedParent=savedHeading.parentNode;window.savedNext=savedHeading.nextSibling;document.querySelector('.reader-content').prepend(savedHeading)")
            self.check(f'Home/{width} negative guard rejects heading outside paper', bool(browser.evaluate(GEOMETRY)['orphan']))
            browser.evaluate('savedParent.insertBefore(savedHeading,savedNext)')
            browser.evaluate("document.getElementById('giới-thiệu').style.paddingLeft='20px'")
            self.check(f'Home/{width} negative guard rejects double inset', bool(browser.evaluate(GEOMETRY)['axes']))
            browser.evaluate("document.getElementById('giới-thiệu').style.removeProperty('padding-left')")
            browser.call('Emulation.setScriptExecutionDisabled', {'value': True}); browser.navigate(url)
            self.check(f'Home/{width} no JS complete/contained content', browser.evaluate(GEOMETRY)['regionCount'] == 9 and browser.evaluate(GEOMETRY)['fits'])
            self.check(f'Home/{width} no JS navigation available', browser.evaluate('!!document.querySelector(".rail .home-nav")'))
            browser.screenshot(self.output / 'images' / f'home-nojs-{width}.png')
            browser.call('Emulation.setScriptExecutionDisabled', {'value': False})
        self.errors += browser.evaluate('window.zoQaErrors||[]')

    def g01(self, browser, width, reference):
        url = (self.output / 'g01-kit.html').as_uri()
        browser.navigate(reference.as_uri())
        old = style_metrics(browser, '.zo-on-thi-package')
        browser.navigate(url)
        self.check(f'G01/{width} shared extraction retains accepted shell metrics', style_metrics(browser, '.reader-content'), old)
        views = ['bat-dau','bai-hoc','luyen-tap','kiem-tra','on-lai','on-nen','sua-loi','nhat-ky','loi-giai','tai-pdf','nguon','toan-van']
        self.check(f'G01/{width} all twelve views', browser.evaluate('document.querySelectorAll(".r1-tab").length'), 12)
        for view in views:
            browser.click('#r1-tab-' + view)
            self.check(f'G01/{width}/{view} selected', browser.evaluate('document.querySelector(".r1-tab[aria-selected=true]").id'), 'r1-tab-' + view)
            browser.evaluate('window.qaClosed=[...document.querySelectorAll(".reader-content details:not([open])")];qaClosed.forEach(n=>n.open=true)')
            state = browser.evaluate(GEOMETRY)
            for field in ['orphan','overflow','axes']:
                self.check(f'G01/{width}/{view} {field}', state[field], [])
            for field in ['fits','white','widths','gaps']:
                self.check(f'G01/{width}/{view} {field}', state[field])
            self.check(f'G01/{width}/{view} figure scale retained', browser.evaluate("[...document.querySelectorAll('.math-illustration')].filter(n=>n.getClientRects().length&&!n.closest('[hidden]')).every(n=>Math.abs(n.getBoundingClientRect().width/parseFloat(getComputedStyle(n).fontSize)-parseFloat(n.style.getPropertyValue('--figure-em')))<.03)"))
            browser.evaluate('qaClosed.forEach(n=>n.open=false)')
        if width in [1440,390]:
            browser.click('#r1-tab-bat-dau'); browser.screenshot(self.output / 'images' / f'g01-kit-cover-{width}.png')
            browser.click('#r1-tab-bai-hoc')
            self.check(f'G01/{width} lesson TOC keeps nine targets', browser.evaluate('document.querySelectorAll(".lesson-toc a").length'), 9)
            browser.evaluate('document.getElementById("từ-chiều-biến-thiên-đến-bảng-biến-thiên").scrollIntoView()'); browser.screenshot(self.output / 'images' / f'g01-kit-bbt-{width}.png')
            browser.click('#r1-tab-on-lai')
            self.check(f'G01/{width} review not journal', browser.evaluate('!document.getElementById("nhat-ky").getClientRects().length&&!!document.getElementById("g01-o01").getClientRects().length'))
            browser.click('#r1-tab-nhat-ky')
            self.check(f'G01/{width} journal not review', browser.evaluate('!!document.getElementById("nhat-ky").getClientRects().length&&!document.getElementById("g01-o01").getClientRects().length'))
            browser.navigate(url + '#cp-lt1'); browser.click('#cp-lt1 a[href="#sua-loi-sau-luyen-tap"]')
            self.check(f'G01/{width} return checkpoint stored', browser.evaluate('new URLSearchParams(location.search).get("r1-return")'), 'cp-lt1')
            browser.click('.r1-return-link')
            self.check(f'G01/{width} returns to checkpoint', browser.evaluate('decodeURIComponent(location.hash)'), '#cp-lt1')
            if width == 390:
                browser.click('.mobile-trigger'); browser.click('#r1-tab-bai-hoc')
                self.check('G01 shared drawer switches view and closes', browser.evaluate('!document.getElementById("mobile-nav").open&&document.querySelector(".r1-tab[aria-selected=true]").id==="r1-tab-bai-hoc"'))
            else:
                browser.evaluate('document.getElementById("r1-tab-bai-hoc").focus()'); browser.key('ArrowDown', 40)
                self.check('G01 shared rail keyboard next', browser.evaluate('document.activeElement.id'), 'r1-tab-luyen-tap')
            browser.call('Emulation.setScriptExecutionDisabled', {'value': True}); browser.navigate(url)
            self.check(f'G01/{width} no JS retains only source-declared hidden items', browser.evaluate('[...document.querySelectorAll(".reader-content [hidden]")].map(n=>n.id)'), self.g01_source_hidden)
            self.check(f'G01/{width} no JS main sections/review/journal remain readable', browser.evaluate('[...document.querySelectorAll(".reader-content>section"),document.getElementById("g01-o01"),document.getElementById("nhat-ky")].every(n=>!!n.getClientRects().length)'))
            self.check(f'G01/{width} no JS content fits', browser.evaluate(GEOMETRY)['fits'])
            browser.screenshot(self.output / 'images' / f'g01-kit-nojs-{width}.png')
            browser.call('Emulation.setScriptExecutionDisabled', {'value': False})
        self.errors += browser.evaluate('window.zoQaErrors||[]')


def edge_executable():
    executable = shutil.which('msedge') or shutil.which('msedge.exe')
    if executable:
        return executable
    for directory in [os.environ.get('ProgramFiles(x86)', ''), os.environ.get('ProgramFiles', '')]:
        candidate = Path(directory) / 'Microsoft/Edge/Application/msedge.exe'
        if candidate.is_file():
            return str(candidate)
    raise RuntimeError('Existing Edge executable not found; no browser will be installed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', type=Path, required=True)
    parser.add_argument('--compare', action='store_true', help='Check functional role consistency across G01/G02 trials')
    args = parser.parse_args()
    output = audit_path(args.preview)
    if args.compare:
        from zo_web_2027_compare import check
        return check(output)
    if (output / 'g02-manifest.json').is_file():
        from zo_web_2027_g02 import check_preview
        return check_preview(output)
    (output / 'images').mkdir(exist_ok=True)
    checks = Checks(output)
    manifest = checks.static()
    reference = REPO / manifest['g01_reference']['source']
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0)); port = probe.getsockname()[1]
    base = f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix='_tmp_browser_', dir=output) as profile:
        process = subprocess.Popen([edge_executable(), '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--remote-debugging-address=127.0.0.1', f'--remote-debugging-port={port}', '--remote-allow-origins=http://localhost', '--user-data-dir=' + profile, 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        browser = None
        try:
            for _ in range(100):
                try:
                    if requests.get(base + '/json/version', timeout=.3).ok:
                        break
                except requests.RequestException:
                    time.sleep(.1)
            else:
                raise TimeoutError('Own headless Edge did not start')
            target = requests.put(base + '/json/new?about:blank', timeout=10).json()
            browser = Browser(target['webSocketDebuggerUrl'])
            browser.call('Page.enable'); browser.call('Runtime.enable')
            browser.call('Page.addScriptToEvaluateOnNewDocument', {'source': "window.zoQaErrors=[];addEventListener('error',e=>zoQaErrors.push(e.message));const original=console.error;console.error=(...a)=>{zoQaErrors.push(a.map(String).join(' '));original(...a)};"})
            for width in [1440,390,768,1000,1920]:
                print('Checking viewport', width, flush=True)
                browser.viewport(width, 960 if width > 500 else 844)
                checks.home(browser, width)
                checks.footer(browser, width)
                checks.g01(browser, width, reference)
                checks.appearance(browser, width)
            if checks.inline_ui:
                for width in [320,360,375]:
                    browser.viewport(width,844)
                    checks.appearance(browser,width)
        finally:
            if browser:
                try:
                    browser.call('Browser.close')
                except Exception:
                    pass
                browser.ws.close()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill(); process.wait(timeout=10)
    before = json.loads((output / 'protected-before.json').read_text(encoding='utf-8'))
    changed = [name for name, digest in before.items() if not (REPO / name).is_file() or sha(REPO / name) != digest]
    checks.check('Production, accepted reference and immutable 0.4 sources unchanged', changed, [])
    checks.check('No JavaScript errors observed in tested pages', checks.errors, [])
    leftovers = [p.name for p in output.glob('_tmp_browser_*')]
    review_limit = 'Owner approved Home/footer; only the new FB027 UI refinement awaits review.' if checks.inline_ui else 'Owner reviewed Home positively; only the new footer awaits review.' if checks.footer_info else 'Visual owner acceptance of Home is still required.'
    report = {'checks': checks.checks, 'checker_sha256': sha(Path(__file__)), 'input_hashes': {name: sha(output / name) for name in manifest['output_hashes']}, 'scope': 'Edge headless file://; Home plus G01 shared-kit reference, not production', 'limits': ['No Safari/Firefox, real touch device or screen reader.', 'No production render, PDFs, commit, push or release.', review_limit], 'temporary_browser_profile_removed': not Path(profile).exists(), 'leftover_profiles_from_earlier_runs': leftovers}
    dump(output / 'qa-results.json', report)
    failures = [n for n in checks.checks if not n['pass']]
    print(json.dumps({'checks': len(checks.checks), 'passed': len(checks.checks) - len(failures), 'failures': [{'name': n['name'], 'actual': str(n['actual'])[:700]} for n in failures], 'temporary_browser_profile_removed': report['temporary_browser_profile_removed'], 'leftover_profiles_from_earlier_runs': leftovers}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
