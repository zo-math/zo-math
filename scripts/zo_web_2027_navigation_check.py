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
import yaml
from zo_web_2027_navigation import ROOT, PAGES, require, destinations
from unittest.mock import patch
from zo_web_2027_check import Browser, edge_executable

def source_checks(text_overrides=None):
    """Check shared destinations without rendering or reading generated HTML."""
    expected=['home','d0','g01','g02','g03','g04','g05','r2_g01']
    output=ROOT/'docs'
    from zo_web_2027_production import runtime_source_checks
    values=runtime_source_checks(ROOT)
    from zo_build_on_thi import outputs,BuildError
    try:
        for source,content in outputs().items():
            values['course generated source current '+source.relative_to(ROOT).as_posix()]=(source.is_file() and source.read_text(encoding='utf-8')==content.rstrip()+'\n')
    except (BuildError,OSError,ValueError,KeyError,TypeError) as exc:
        values['course catalog and generated sources readable: '+str(exc)]=False
    for current in [None,*expected]:
        page=output/PAGES.get(current,PAGES['home'])[0]
        links=destinations(output,page,current)
        values[str(current)+' shared complete menu']=[key for key,_,_ in links]==expected
        g04=[href for key,href,_ in links if key=='g04']
        values[str(current)+' G04 source destination']=len(g04)==1 and (page.parent/unquote(urlsplit(g04[0]).path)).resolve()==(output/BASE_G04).resolve()
        values[str(current)+' G04 starts at beginning']=len(g04)==1 and urlsplit(g04[0]).query=='r1-view=bat-dau' and urlsplit(g04[0]).fragment=='bat-dau'
    for current in [None,*expected]:
        page=output/PAGES.get(current,PAGES['home'])[0]
        g05=[href for key,href,_ in destinations(output,page,current) if key=='g05']
        values[str(current)+' G05 canonical entry']=len(g05)==1 and (page.parent/unquote(urlsplit(g05[0]).path)).resolve()==(output/PAGES['g05'][0]).resolve() and urlsplit(g05[0]).query=='r1-view=bat-dau' and urlsplit(g05[0]).fragment=='bat-dau'
    config=yaml.safe_load((ROOT/'_quarto.yml').read_text(encoding='utf-8'))
    sidebar=next(s for s in config['website']['sidebar'] if s.get('id')=='on-thi')
    values['Quarto sidebar contains G04 once']=sum(n.get('href')==str(BASE_G04.with_suffix('.qmd')).replace('\\','/') for n in sidebar['contents'])==1
    from zo_course_labels import expand
    import re
    from urllib.parse import parse_qs
    source_texts={key:expand(ROOT/relative.with_suffix('.qmd')) for key,(relative,_) in PAGES.items()}
    source_texts.update(text_overrides or {})
    def anchors(text):
        return set(re.findall(r'\{[^}\n]*?#([^\s}]+)',text))|set(re.findall(r"\bid=[\"']([^\"']+)",text))
    source_ids={key:anchors(text) for key,text in source_texts.items()}
    by_source={(ROOT/relative.with_suffix('.qmd')).resolve():key for key,(relative,_) in PAGES.items()}
    for current,(relative,_) in PAGES.items():
        source=ROOT/relative.with_suffix('.qmd')
        text=source_texts[current]
        ids=source_ids[current]
        for target,href,_ in destinations(output,output/relative,current):
            url=urlsplit(href);target_source=ROOT/PAGES[target][0].with_suffix('.qmd')
            target_text=source_texts[target]
            values[current+'/'+target+' file exists']=target_source.is_file()
            values[current+'/'+target+' entry anchor']=not url.fragment or url.fragment in source_ids[target]
        hrefs=[m[2] for m in re.finditer(r'(?<!!)\[([^\]\n]+)\]\(([^\s)]+)\)',text)]
        hrefs+=re.findall(r"\bhref=[\"']([^\"']+)",text)
        for number,href in enumerate(hrefs,1):
            url=urlsplit(href)
            if url.scheme or url.netloc:continue
            destination=(source.parent/unquote(url.path)).resolve() if url.path else source.resolve()
            if destination.suffix=='.html':destination=destination.with_suffix('.qmd')
            target_key=by_source.get(destination)
            if target_key is None:continue
            fragment=unquote(url.fragment)
            generated_local=not url.path and fragment in {'ung-ho','xem-toan-bo'}
            values[current+'/local-link/'+str(number)+' existing anchor']=not fragment or fragment in source_ids[target_key] or generated_local
        for number,m in enumerate(re.finditer(r'(?<!!)\[([^\]\n]+)\]\(([^\s)]+)\)',text),1):
            url=urlsplit(m[2]);params=parse_qs(url.query)
            if not url.path.startswith('../r1_g') or params.get('r1-view',[''])[0] not in ['on-nen','bai-hoc','nhat-ky']:continue
            prefix=current+'/cross-support/'+str(number)
            # Linked shared support may name its return in the source-owned row.
            # Do not force a fixed caller onto an independent support entry.
            binding_path=source.parent/'giao_dien/he_nhan.json'
            binding=json.loads(binding_path.read_text('utf-8')) if binding_path.is_file() else {}
            registered={v['href'].replace('.html','.qmd') for v in binding.get('foundation_links',[])}
            if binding.get('foundation_mode')=='linked-shared' and m[2] in registered:
                row=next((line for line in text.splitlines() if m[0] in line),'')
                values[prefix+' named in-place return']='**Trở lại:**' in row and bool(row.split('**Trở lại:**',1)[1].strip(' |.'))
                continue
            values[prefix+' explicit return page']=params.get('r1-return-page')==[source.parent.name]
            values[prefix+' existing caller']=params.get('r1-return',[''])[0] in ids
            values[prefix+' named return view']=bool(params.get('r1-return-view') and params.get('r1-return-label'))
    d0=source_texts['d0']
    for key,(relative,_) in PAGES.items():
        # D0's diagnostic recommendations remain its own approved content.
        # New catalog entries are available through the shared menu and Home.
        if key in {'g01','g02','g03','g04'}:values['D0 lists '+key]=('../'+relative.parent.name+'/index.qmd') in d0
    return values


BASE_G04=Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/index.html')


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
    values = source_checks()
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
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--browser',action='store_true');p.add_argument('--source-only',action='store_true');p.add_argument('--baseline',type=Path,help='Explicit optional historical HTML comparison');a=p.parse_args()
    out=a.output.resolve()
    if not out.is_relative_to(ROOT/'_audit'):raise ValueError('Evidence must stay in audit')
    if a.source_only:
        out.mkdir(parents=True,exist_ok=True);values=source_checks()
        report={'checks':values,'passed':sum(values.values()),'total':len(values),'failures':[k for k,v in values.items() if not v],'html_built':False}
        (out/'qa-source.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False));return int(bool(report['failures']))
    return run(out,a.browser,a.baseline.resolve() if a.baseline else None)
if __name__=='__main__':raise SystemExit(main())
