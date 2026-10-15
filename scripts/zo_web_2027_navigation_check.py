"""QD_032 regression guard: structure, negative fixtures and real browser behavior.

Run against an isolated cluster built from current canonical sources. Does not
render, publish, accept content, or alter earlier receipts.
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse, copy, hashlib, json, socket, subprocess, sys, tempfile, time
sys.dont_write_bytecode = True
from bs4 import BeautifulSoup
import requests
from zo_web_2027_navigation import ROOT, PAGES, require, destinations
from unittest.mock import patch
from zo_web_2027_check import Browser, edge_executable

def hover_style_ok(style):
    return (style['background'] == 'rgba(0, 0, 0, 0)'
            and style['decoration'] == 'none' and style['shadow'] == 'none')

def navigation_style_checks(b, check, prefix):
    """Real pointer states, including current-page links; focus is separate."""
    selectors = ['.course-panel [data-course-page='+key+']' for key in PAGES]
    selectors += ['[data-course-action='+key+']' for key in ['home','list','top']]
    def style(selector):
        return b.evaluate("""(() => {
            const n=document.querySelector(%s),s=getComputedStyle(n),r=n.getBoundingClientRect();
            return {background:s.backgroundColor,decoration:s.textDecorationLine,
              shadow:s.boxShadow,color:s.color,box:[r.x,r.y,r.width,r.height]};
        })()""" % json.dumps(selector))
    for selector in selectors:
        b.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':1,'y':1})
        initial = style(selector)
        x,y,w,h = initial['box']
        b.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':x+w/2,'y':y+h/2})
        time.sleep(.05)
        hovered = style(selector)
        check(prefix+' text-only hover '+selector,
              hover_style_ok(initial) and hover_style_ok(hovered)
              and initial['color'] != hovered['color'] and initial['box'] == hovered['box'])
    check(prefix+' current page remains bold without underline', b.evaluate("""(() => {
        const s=getComputedStyle(document.querySelector('.course-panel [aria-current=page]'));
        return Number(s.fontWeight)>=600 && s.textDecorationLine==='none';
    })()"""))

def run(out, browser=False, baseline=None):
    values = {}
    def check(name, value):
        values[name] = bool(value)
        if not value: print('FAIL', name, flush=True)
    delivery = out / 'delivery/docs'
    good = dict(background='rgba(0, 0, 0, 0)', decoration='none', shadow='none')
    check('style guard accepts text-only hover', hover_style_ok(good))
    for name, field, value in [('bright box','background','rgb(249, 246, 239)'),
                                ('underline','decoration','underline'),
                                ('hover shadow','shadow','rgb(0, 0, 0) 0px 2px 4px')]:
        check('style guard rejects '+name, not hover_style_ok(dict(good, **{field:value})))
    with patch('zo_web_2027_navigation.yaml.safe_load',return_value={'packages':[{'id':'d0'}]}):
        try:destinations(delivery,delivery/PAGES['home'][0])
        except ValueError:check('rejects unbound or changed catalog',True)
        else:check('rejects unbound or changed catalog',False)
    docs = {}
    for key,(relative,_) in PAGES.items():
        page = delivery / relative
        doc = BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        docs[key] = doc
        require(doc,page,delivery,key)
        check(key+' static contract',True)
        for link in doc.select('.course-panel a'):
            check(key+' local destination exists '+link['data-course-page'],(page.parent/unquote(urlsplit(link['href']).path)).resolve().is_file())
        for resource in doc.select('link[href*="course-navigation"],script[src*="course-navigation"]'):
            href=resource.get('href',resource.get('src'))
            asset=(page.parent/unquote(urlsplit(href).path)).resolve()
            canonical=ROOT/'_design/web_2027_mau_dung_chung'/asset.name
            check(key+' current resource '+asset.name,asset.read_bytes()==canonical.read_bytes())
        check(key+' six colors and grayscale retained',len(doc.select('.appearance input[type=radio]'))==6 and len(doc.select('.appearance .gray-toggle'))==1)
        for name, mutate in [
            ('missing control',lambda d:d.select_one('[data-course-action=top]').decompose()),
            ('wrong destination',lambda d:d.select_one('.course-panel a').__setitem__('href','#wrong')),
            ('open by default',lambda d:d.select_one('.zo-course-menu').__setitem__('open','')),
            ('wrong current page',lambda d:d.select_one('.course-panel [aria-current]').__delitem__('aria-current')),
            ('legacy link',lambda d:d.select_one('[data-course-action=home]').__setitem__('class','course-link')),
            ('control order',lambda d:d.select_one('[data-course-action=top]').insert_before(d.select_one('[data-course-action=home]').extract())),
        ]:
            fixture = copy.deepcopy(doc); mutate(fixture)
            try:require(fixture,page,delivery,key)
            except (ValueError,AttributeError):check(key+' rejects '+name,True)
            else:check(key+' rejects '+name,False)
        # Evidence baseline only: never used as a production input.
        old = baseline / (key+'-reading.html') if baseline is not None else None
        if old is not None:
            prior = BeautifulSoup(old.read_text(encoding='utf-8'),'html.parser')
            def inventory(d):
                main=d.select_one('main')
                return {'text':main.get_text(' ',strip=True),
                        'ids':[n['id'] for n in main.select('[id]')],
                        'headings':[(n.name,n.get_text(' ',strip=True)) for n in main.select('h1,h2,h3,h4,h5,h6')],
                        'math':[n.get_text() for n in main.select('annotation[encoding="application/x-tex"],.math')],
                        'details':[(n.get('id'),n.has_attr('open')) for n in main.select('details')],
                        'logo':str(d.select_one('.site-top > a:first-child img'))}
            a,c=inventory(prior),inventory(doc)
            # Resource rebasing changes src only; original logo filename and dimensions must match.
            a.pop('logo');c.pop('logo')
            check(key+' learner content/headings/IDs/math/disclosures unchanged',a==c)
    if browser:
        browser_checks(out,check)
    failures=[k for k,v in values.items() if not v]
    report={'decision':'QD_032','checks':values,'failures':failures,'passed':len(values)-len(failures),'total':len(values),'browser':browser,'owner_acceptance':'pending','published':False,'limits':['Navigation and preservation checks only; not a complete mathematics audit','Heading redesign is not applied','No PDF learning-package validation']}
    report['input_sha256'] = {str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [Path(__file__).resolve(),ROOT/'_design/web_2027_mau_dung_chung/course-navigation.css']}
    target=out/('qa-browser.json' if browser else 'qa-static.json')
    report['historical_baseline_checked'] = baseline is not None
    if target.exists():target=out/(target.stem+'-'+str(time.time_ns())+'.json')
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'total':report['total'],'failures':failures},ensure_ascii=False),flush=True)
    return int(bool(failures))

def browser_checks(out,check):
    images=out/'images';images.mkdir(exist_ok=True)
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    base=f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix='_tmp_browser_',dir=out) as profile:
        proc=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1',f'--remote-debugging-port={port}','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        b=None
        try:
            for _ in range(100):
                try:
                    if requests.get(base+'/json/version',timeout=.3).ok:break
                except requests.RequestException:pass
                time.sleep(.1)
            else:raise TimeoutError('Own browser did not start')
            target=requests.put(base+'/json/new?about:blank',timeout=10).json()
            b=Browser(target['webSocketDebuggerUrl'])
            for width in [1440,1000,768,430,390,320]:
                b.viewport(width,850)
                for key in PAGES:
                    url=(out/'html-current'/f'{key}-reading.html').as_uri()
                    b.navigate(url)
                    prefix=f'{width}/{key}/'
                    geometry=b.evaluate("""(() => {
                        const h=document.querySelector('.site-top'), tools=h.querySelector('.course-tools').getBoundingClientRect(), app=h.querySelector('.appearance').getBoundingClientRect(), r=h.getBoundingClientRect();
                        const boxes=[...h.querySelectorAll('.course-action')].map(n=>n.getBoundingClientRect());
                        return {fits:document.documentElement.scrollWidth<=innerWidth+1,
                          controls:boxes.every(n=>n.width>=39&&n.height>=43&&n.left>=r.left&&n.right<=innerWidth),
                          separated:tools.right<=app.left+1||tools.bottom<=app.top+1,
                          height:r.height,closed:!h.querySelector('details').open,
                          images:[...h.querySelectorAll('img')].every(n=>n.complete&&n.naturalWidth>0)};
                    })()""")
                    for name in ['fits','controls','separated','closed','images']:check(prefix+name,geometry[name])
                    check(prefix+'toolbar height',abs(geometry['height']-(112 if width<=500 else 64))<1)
                    b.evaluate("document.querySelector('.zo-course-menu summary').focus()")
                    b.key('Enter',13,'\r')
                    check(prefix+'keyboard opens menu',b.evaluate("document.querySelector('.zo-course-menu').open"))
                    panel=b.evaluate("""(() => {const n=document.querySelector('.course-panel'),r=n.getBoundingClientRect();return r.width>0&&r.left>=0&&r.right<=innerWidth&&r.bottom<=innerHeight&&getComputedStyle(n).backgroundColor==='rgb(255, 255, 255)'})()""")
                    check(prefix+'menu legible in viewport',panel)
                    navigation_style_checks(b,check,prefix)
                    b.evaluate("document.querySelector('.zo-course-menu summary').focus()")
                    b.key('Tab',9)
                    check(prefix+'keyboard link focus visible',b.evaluate("""(() => {
                        const n=document.activeElement,s=getComputedStyle(n);
                        return n.matches('.course-panel a') && n.matches(':focus-visible')
                          && s.outlineStyle!=='none' && parseFloat(s.outlineWidth)>=2;
                    })()"""))
                    if width == 1440 and key == 'd0':
                        # Inject the old defect: the same computed-style predicate must fail.
                        b.evaluate("window.navOldStyle=document.createElement('style');navOldStyle.textContent='.course-panel a{background:#f9f6ef!important;text-decoration:underline!important}';document.head.append(navOldStyle)")
                        old_style=b.evaluate("(() => {const s=getComputedStyle(document.querySelector('.course-panel a'));return {background:s.backgroundColor,decoration:s.textDecorationLine,shadow:s.boxShadow}})()")
                        check('browser rejects old hover box and underline',not hover_style_ok(old_style))
                        b.evaluate('navOldStyle.remove()')
                    if width in [1440,390,320]:
                        b.evaluate('document.activeElement.blur()')
                        point=b.evaluate("(() => {const r=document.querySelector('.course-panel [aria-current=page]').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()")
                        b.call('Input.dispatchMouseEvent',dict(type='mouseMoved',**point))
                        b.screenshot(images/f'{key}-{width}-menu.png')
                    b.key('Escape',27)
                    check(prefix+'Escape closes and restores focus',b.evaluate("!document.querySelector('.zo-course-menu').open&&document.activeElement===document.querySelector('.zo-course-menu summary')"))
                    b.key(' ',32,' ')
                    check(prefix+'Space opens menu',b.evaluate("document.querySelector('.zo-course-menu').open"))
                    b.key('Escape',27)
                    b.click('.zo-course-menu summary');b.evaluate("document.querySelector('[data-course-action=top]').focus()")
                    check(prefix+'focus outside closes',b.evaluate("!document.querySelector('.zo-course-menu').open"))
                    b.evaluate('window.scrollTo(0,900)')
                    check(prefix+'sticky toolbar',b.evaluate("Math.abs(document.querySelector('.site-top').getBoundingClientRect().top)<1"))
                    before=b.evaluate('location.href');b.click('[data-course-action=top]')
                    check(prefix+'Top preserves URL and scrolls to zero',b.evaluate('location.href')==before and b.evaluate('scrollY')<1)
                    if width in [1440,390]:b.screenshot(images/f'{key}-{width}-header.png')
                    b.click('.zo-course-menu summary');b.evaluate("document.body.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))")
                    check(prefix+'outside pointer closes',b.evaluate("!document.querySelector('.zo-course-menu').open"))
                    if width in [1440,390]:
                        b.call('Emulation.setScriptExecutionDisabled',{'value':True});b.navigate(url)
                        b.click('.zo-course-menu summary')
                        check(prefix+'noJS native menu and real links',b.evaluate("document.querySelector('.zo-course-menu').open&&document.querySelectorAll('.course-panel a[href]').length===4"))
                        navigation_style_checks(b,check,prefix+'noJS/')
                        b.call('Emulation.setScriptExecutionDisabled',{'value':False});b.navigate(url)
                print('Browser width checked:',width,flush=True)
            # Actual link transitions, not just href assertions.
            b.viewport(1440,850)
            b.navigate((out/'html-current/g01-reading.html').as_uri())
            for key in ['g02','d0','home','g01']:
                b.click('.zo-course-menu summary');b.click(f'.course-panel [data-course-page={key}]');b.ready()
                check('transition to '+key,b.evaluate('document.body.dataset.zoCourseNavigation')==key)
                check('transition active '+key,b.evaluate("document.querySelector('.course-panel [aria-current]').dataset.coursePage")==key)
            b.click('[data-course-action=home]');b.ready()
            check('Home action returns to course home',b.evaluate('document.body.dataset.zoCourseNavigation')=='home')
            for key in ['g01','g02']:
                for width in [1440,390,320]:
                    b.viewport(width,850)
                    b.navigate((out/'html-current'/f'{key}-reading.html').as_uri()+'?r1-view=bai-hoc#bai-hoc')
                    check(f'{key}/{width}/lesson anchor clears toolbar',b.evaluate("document.getElementById('bai-hoc').getBoundingClientRect().top>=document.querySelector('.site-top').getBoundingClientRect().bottom-1"))
                    before=b.evaluate('location.href');b.evaluate('window.scrollTo(0,600)');b.click('[data-course-action=top]')
                    check(f'{key}/{width}/Top retains lesson view',b.evaluate('location.href')==before and b.evaluate("document.querySelector('[data-r1-view=\"bai-hoc\"]').getClientRects().length>0"))
            b.viewport(390,850);b.navigate((out/'html-current/g01-reading.html').as_uri())
            b.click('.appearance input[type=radio]:last-of-type')
            check('six color controls remain',b.evaluate("document.querySelectorAll('.appearance input[type=radio]').length===6"))
            b.click('.gray-toggle');check('grayscale toggles',b.evaluate("document.querySelector('.gray-toggle').getAttribute('aria-pressed')==='true'"))
            b.click('.gray-toggle')
            b.click('.mobile-trigger')
            check('package drawer still works',b.evaluate("document.querySelector('#mobile-nav').open"))
            b.key('Escape',27)
            check('package drawer Escape',b.evaluate("!document.querySelector('#mobile-nav').open"))
            for key in ['g01','g02']:
                b.navigate((out/'html-current'/f'{key}-reading.html').as_uri())
                views=b.evaluate("[...document.querySelectorAll('.r1-tab[id]')].map(n=>n.id)")
                check(key+' package view inventory present',len(views)>=9)
                for href in views:
                    b.click('#'+href)
                    time.sleep(.15)
                    check(key+'/'+href+' toolbar keeps three controls',b.evaluate("document.querySelectorAll('.site-top .course-action').length===3&&!document.querySelector('.zo-course-menu').open"))
                    check(key+'/'+href+' no page overflow',b.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
        finally:
            if b:b.ws.close()
            proc.terminate()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--browser',action='store_true');p.add_argument('--baseline',type=Path,help='Explicit optional historical HTML comparison');a=p.parse_args()
    out=a.output.resolve()
    if not out.is_relative_to(ROOT/'_audit'):raise ValueError('Evidence must stay in audit')
    return run(out,a.browser,a.baseline.resolve() if a.baseline else None)
if __name__=='__main__':raise SystemExit(main())
