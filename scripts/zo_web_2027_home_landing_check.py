"""Scoped editorial Home QA; does not accept, publish, stage or build PDFs."""
import argparse
import copy
import json
import os
import re
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit, urlunsplit
import requests
from bs4 import BeautifulSoup
from zo_web_2027_preview import REPO, KIT, inventory, sha, footer_data, BRAND_THOUGHT
from zo_web_2027_check import Browser, edge_executable, complete_site_footer
from zo_build_on_thi import outputs, load_yaml, DATA_PATH, package_from_ref


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def preview(page, out, candidates):
    doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
    before = inventory(doc.select_one('.home-landing-content'))
    docs = next(p for p in page.parents if p.name == 'docs')
    runtime = docs / 'assets/zo_web_2027/home'
    shutil.copytree(runtime, out / 'runtime', dirs_exist_ok=True)
    # Preview-only siblings share the NEW Home destination. Do not let a user
    # return from D0/R1 to an earlier Home candidate and mistake it for rollback.
    local_candidates = {key:out/({'d0':'d0','r1_g01':'g01','r1_g02':'g02'}[key]+'-reading.html') for key in candidates}
    old_home = next(iter(candidates.values())).parent / 'home-reading.html'
    projection_map = {source.resolve():local_candidates[key] for key,source in candidates.items()}
    projection_map[old_home.resolve()] = out/'home-reading.html'
    for key, source in candidates.items():
        sibling = BeautifulSoup(source.read_text(encoding='utf-8'),'html.parser')
        snapshot = inventory(sibling.select_one('main'))
        for n in sibling.select('img[src],link[href],script[src],a[href]'):
            attr='src' if n.has_attr('src') else 'href';u=urlsplit(n[attr])
            if u.scheme or u.netloc or not u.path:continue
            target=(source.parent/unquote(u.path)).resolve()
            dest=projection_map.get(target,target)
            n[attr]=urlunsplit(('', '',os.path.relpath(dest,out).replace('\\','/'),u.query,u.fragment))
        if inventory(sibling.select_one('main'))!=snapshot:
            raise ValueError('Sibling preview projection changed learner content')
        local_candidates[key].write_text(str(sibling),encoding='utf-8')
    for n in doc.select('img[src],link[href],script[src],a[href]'):
        key = 'src' if n.has_attr('src') else 'href'
        u = urlsplit(n[key])
        if u.scheme or u.netloc or not u.path:
            continue
        target = (page.parent / unquote(u.path)).resolve()
        if target.is_relative_to(runtime):
            dest = out / 'runtime' / target.relative_to(runtime)
        elif target == page.resolve():
            dest = out / 'home-reading.html'
        else:
            rel = target.relative_to(docs).as_posix()
            dest = REPO / 'docs' / rel
            for package, candidate in candidates.items():
                if '/hoc_lieu/'+package+'/index.html' in '/'+rel:
                    dest = local_candidates[package]
        if not dest.is_file() and dest.name != 'home-reading.html':
            raise ValueError('Missing preview link ' + str(dest))
        n[key] = urlunsplit(('', '', os.path.relpath(dest, out).replace('\\', '/'), u.query, u.fragment))
    if inventory(doc.select_one('.home-landing-content')) != before:
        raise ValueError('Preview must preserve editorial projection')
    target = out / 'home-reading.html'
    target.write_text(str(doc), encoding='utf-8')
    save(out / 'preview.json', {'canonical_html_sha256': sha(page), 'preview_html_sha256': sha(target),
        'candidates': {k: {'path': str(v), 'sha256': sha(v), 'local_projection':str(local_candidates[k]),'projection_sha256':sha(local_candidates[k])} for k, v in candidates.items()}, 'mapping_only': True,'sibling_content_preserved':True})
    return target


def action_only_cards(cards):
    """Only the explicit CTA is a link; never restore a clickable card shell."""
    return bool(cards) and all(
        c.name == 'article' and not any(c.has_attr(k) for k in ['href', 'tabindex', 'role', 'onclick', 'onkeydown'])
        and len(c.select('a')) == 1
        and (a := c.select_one('a.home-card-action[href]')) is not None
        and a.get('aria-labelledby') == a.get('id', '') + ' ' + c.h3.get('id', '')
        and not a.select('img,h3,p,.home-card-copy')
        and c.select_one('div.home-card-content') is not None
        and not c.select('.home-card-link,[role=link],[role=button],[tabindex],[onclick],[onkeydown],button')
        for c in cards)


def reading_layout_checks(doc):
    root=doc.select_one('.home-landing-content')
    purpose=doc.select_one('#chương-trình-giúp-em-làm-gì')
    rows=doc.select('.home-method-grid > div')
    topics=doc.select('.home-strands > div')
    return {
        'intro purpose and audience inside opening hero':bool(purpose and purpose.parent.get('id')=='giới-thiệu' and purpose.find(id='dành-cho-ai')),
        'catalog then method directly after opening hero':bool(root) and [s.get('id') for s in root.find_all('section',recursive=False)][:3]==['giới-thiệu','hoc-lieu-hien-co','học-theo-cách-nào'],
        'four complete method rows without verb labels':len(rows)==4 and not doc.select('.home-method-verb') and all(len(r.find_all('p',recursive=False))==2 and r.select_one('.home-method-heading h3') and r.select_one('.home-method-number[aria-hidden=true]').get_text()==f'{i:02d}' for i,r in enumerate(rows,1)),
        'six large reading panels kept':len(doc.select('.home-reading-panel'))==6,
        'method support copy grouped not removed':bool(doc.select_one('.home-method-tail .home-method-note')) and len(doc.select('.home-method-tail > h3'))==2,
        'eight topic frames numbered accessibly':len(topics)==8 and all(r.select_one('.home-topic-number[aria-hidden=true]').get_text()==f'{i:02d}' for i,r in enumerate(topics,1)),
        'service illustration and copy retained':bool(doc.select_one('.home-service-copy #home-service-title') and doc.select_one('.home-service-illustration img.home-service-art[alt][width="1448"][height="1086"]')) and bool(doc.select_one('.home-service-status h3')),
        'service copy accessible and fee explicit':bool(doc.select_one('.home-service-copy .home-service-fee')) and 'dịch vụ có thu phí' in doc.select_one('.home-service-copy').get_text(' ',strip=True) and not doc.select('.home-service .role'),
        'service accent decorative after fee':bool(doc.select_one('.home-service-copy .home-service-fee + .home-service-accent[aria-hidden=true]')),
        'FAQ four separate native disclosures':len(doc.select('.home-faq > details'))==4,
    }


READING_LAYOUT_GEOMETRY = r'''(()=>{
  const rect=n=>n.getBoundingClientRect(), style=n=>getComputedStyle(n);
  const grid=document.querySelector('.home-method-grid'), g=rect(grid), rows=[...grid.children];
  const frames=nodes=>nodes.every(n=>style(n).borderTopStyle==='solid'&&parseFloat(style(n).borderRadius)>=9);
  const alternating=nodes=>nodes.length>1&&style(nodes[0]).backgroundColor!==style(nodes[1]).backgroundColor;
  const topics=[...document.querySelectorAll('.home-strands>div')], faq=[...document.querySelectorAll('.home-faq>details')];
  const art=document.querySelector('.home-service-art'), a=rect(art);
  const panels=['chương-trình-giúp-em-làm-gì','học-theo-cách-nào','tám-mạch','hoc-truc-tiep','nguon-hoc-lieu','cau-hoi-thuong-gap'].map(id=>style(document.getElementById(id)).backgroundColor);
  return {
    columns:style(grid).gridTemplateColumns.split(' ').length,
    fullWidth:rows.every(n=>Math.abs(rect(n).x-g.x)<1&&Math.abs(rect(n).width-g.width)<1),
    gaps:rows.slice(1).every((n,i)=>rect(n).top-rect(rows[i]).bottom>=9),
    methodFrames:frames(rows),methodAlternates:alternating(rows),
    topicFrames:frames(topics),topicColumns:style(document.querySelector('.home-strands')).gridTemplateColumns.split(' ').length,
    faqFrames:frames(faq),faqAlternates:alternating(faq),
    panelsAlternate:panels.every((c,i)=>c===(i===3?'rgb(255, 255, 255)':i%2?'rgb(247, 247, 245)':'rgb(255, 255, 255)')),
    serviceFits:art.complete&&art.naturalWidth>0&&a.width>0&&a.left>=0&&a.right<=innerWidth&&Math.abs(a.width/a.height-1448/1086)<.01
  };
})()'''


def validate(doc, build):
    root = doc.select_one('.home-landing-content')
    refs = load_yaml(DATA_PATH)['packages']
    packages = [package_from_ref(r) for r in refs]
    cards = doc.select('.home-card[data-package-id]')
    text = re.sub(r'\s+([:;,.!?])', r'\1', doc.get_text(' ', strip=True))
    from zo_web_2027_home_landing import countdown_source
    expected = BeautifulSoup(countdown_source(load_yaml(DATA_PATH)['program']), 'html.parser').select_one('.home-countdown')
    clock = doc.select_one('.home-countdown')
    clock_valid = bool(clock) and all(clock.get(k) == expected.get(k) for k in ['data-countdown-target', 'data-countdown-status'])
    clock_copy = bool(clock) and all(clock.select_one(s) and clock.select_one(s).get_text(' ',strip=True) == expected.select_one(s).get_text(' ',strip=True) for s in ['.countdown-date','.countdown-notice','.countdown-fallback'])
    return {
        'editorial layout marker':bool(root) and doc.body.get('data-zo-web-production') == 'course-home',
        'canonical text IDs headings disclosures math unchanged': bool(root) and json.loads(json.dumps(inventory(root))) == build['source_inventory'],
        'catalog prose contains no unrendered TeX':not any(re.search(r'\$|\\(?:infty|frac|sqrt)\b', c.p.get_text(' ', strip=True)) for c in cards),
        'real catalog only and order': [c['data-package-id'] for c in cards] == [p.ref_id for p in packages],
        'catalog title summary status match canonical':len(cards) == len(packages) and all(c.h3.get_text(' ', strip=True) == p.title and c.p.get_text(' ', strip=True) == p.summary and p.display_status in c.select_one('.role').get_text() for c,p in zip(cards,packages)),
        'catalog links actual packages':all(c.select_one('a.home-card-action') and '/hoc_lieu/'+c['data-package-id']+'/index.html' in c.select_one('a.home-card-action').get('data-canonical-href','') for c in cards),
        'cards navigate only through accessible action links':action_only_cards(cards),
        **reading_layout_checks(doc),
        'no management copy or prescribed textbook teacher route':not any(x in text for x in ['Mỗi ngày, một việc học được làm đến nơi.','Phần chưa học được ghi riêng','quyền bắt đầu không chứng nhận','hỏi giáo viên','sách giáo khoa']),
        'no visible internal course codes':not re.search(r'\b(?:D0|R[1-8](?:-G\d+)?)\b', text),
        'flexible help and return to own work':bool(doc.select_one('.home-method-tail')) and 'Em cũng có thể chọn tài liệu, công cụ hoặc trao đổi với người khác' in doc.select_one('.home-method-tail').get_text(' ',strip=True) and 'Sau đó, quay lại bài hoặc phần đang học trước khi mở hỗ trợ.' in doc.select_one('.home-method-tail').get_text(' ',strip=True),
        'unique IDs':len(doc.select('[id]')) == len({n['id'] for n in doc.select('[id]')}),
        'all old Home anchors retained':all(doc.find(id=x) for x in ['giới-thiệu','dành-cho-ai','chương-trình-giúp-em-làm-gì','học-theo-cách-nào','lộ-trình','tám-mạch','hoc-lieu-hien-co','bắt-đầu-từ-đâu','trạng-thái-triển-khai']),
        'real logo retained':doc.select_one('.site-top > a img')['src'].endswith('horizontal_color.svg'),
        'full brand retained':doc.select_one('.home-hero .brand-thought').get_text(' ',strip=True) == BRAND_THOUGHT,
        'six background choices':len(doc.select('.appearance input[type=radio]')) == 6,
        'grayscale retained':bool(doc.select_one('#grayscale[aria-pressed]')),
        'contents trigger icon only':bool(doc.select_one('.mobile-trigger--icon[aria-label]')),
        'all disclosures initially closed':not doc.select('details[open]'),
        'eight strands not fake available packages':len(doc.select('.home-strands > div')) == 8 and not doc.select('.home-strands a[href]') and {n['data-package-id'] for n in doc.select('.home-card[data-package-id]')} == {p.ref_id for p in [package_from_ref(ref) for ref in load_yaml(DATA_PATH)['packages']]},
        'independent test separate from optional survey': 'Không chia bài Kiểm tra thành nhiều buổi.' in text and 'không xem lời giải hay tìm trợ giúp trong lúc làm' in text and 'Đây không phải bài thi để xét điều kiện vào học' in text,
        'survey PDF availability truthful': 'Khảo sát đầu vào hiện dùng trên trang web.' in text,
        'checkpoint explained before use':'Cuối mỗi chặng có Điểm dừng: phần này hướng dẫn em xem lại bài làm' in text,
        'countdown target and status from canonical data':clock_valid,
        'countdown reference notice and fallback truthful':clock_copy,
        'countdown timestamp and verified source':bool(clock and clock.time and clock.select_one('.countdown-notice a')) and clock.time.get('datetime') == expected.time['datetime'] and clock.select_one('.countdown-notice a')['href'] == expected.select_one('.countdown-notice a')['href'],
        'countdown accessible non-live timer':bool(doc.select_one('.countdown-readout[role=timer][aria-live=off][hidden]')),
        'service not open': 'Chưa mở đăng kí' in text and not doc.select('form[action],a[href*="register"]'),
        'complete canonical footer':complete_site_footer(doc, footer_data()),
        'support real QR and voluntary':bool(doc.select_one('img.r1-support-qr[src$="qr_bao_tro_zo_math_vietcombank.jpg"]')) and '0601000137768' in text and 'Việc bảo trợ ZO Math là tự nguyện' in text,
        'no imported mock or internal instructions':not doc.select('.prototype-note,script[src*="reference"],img[src^="data:"],.mock-dialog') and 'BẢN MẪU 04' not in text and not any('_quy_trinh' in a['href'] or 'reference/' in a['href'] for a in doc.select('a[href]')),
        'conceptual image correct roles':len(doc.select('.home-journey img'))==1 and bool(doc.select_one('.journey-portrait[src$="hanh_trinh_nguoi_hoc_toan_3x4.png"]')) and not doc.select('.journey-square'),
        'no artificial task architecture or R1 controller':not doc.select('[data-zo-task],script[src*="r1-controller"]'),
    }


def static(page, build, *, public_candidate=False):
    doc = BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    checks = validate(doc, build)
    for key, path in [('canonical_data',REPO/build['canonical_data']), ('editorial',REPO/build['editorial_source']), ('profile',KIT/'profiles/course-home.json')]:
        checks[key+' source current'] = sha(path) == build[key+'_sha256']
    checks['generated component sources current'] = bool(build.get('component_sha256')) and all(sha(REPO/path)==digest for path,digest in build['component_sha256'].items())
    from zo_home_qmd import source_checks, source_fixtures
    checks.update(source_checks((REPO/build['editorial_source']).read_text(encoding='utf-8')))
    checks.update(source_fixtures((REPO/build['editorial_source']).read_text(encoding='utf-8')))
    checks['generated outputs current'] = all(p.is_file() and p.read_text(encoding='utf-8') == value.rstrip()+'\n' for p,value in outputs().items())
    # The full-page D0 PDF is pending review, not an eight-variant R1 catalog.
    import zo_build_on_thi as catalog
    from unittest.mock import patch
    refs=load_yaml(DATA_PATH)['packages']
    survey=package_from_ref(refs[0])
    checks['D0 pending PDF preserves web survey entry']=survey.html_only and not survey.pdfs
    for ref in refs:
        profile=catalog.load_yaml(catalog.PACKAGE_ROOT/ref['id']/catalog.PROFILE_NAME)
        profile['acceptance']['pdf_canonical']='full_page_pending_owner_review_2026_10_14_typo'
        if ref['id']!='d0':profile['acceptance']['pdf_canonical']='full_page_pending_owner_review_2026_10_14'
        try:
            with patch.object(catalog,'load_yaml',return_value=profile), patch.object(catalog,'qmd_metadata',return_value={'title':'Fixture','format':{'pdf':{}}}):
                package_from_ref(ref)
            rejected=False
        except ValueError:rejected=True
        checks['negative PDF contract exception limited '+ref['id']]=rejected
    checks['current implementation built'] = all(sha(REPO/'scripts'/name)==digest for name,digest in build['implementation_sha256'].items())
    checks['table guard still mounted'] = 'course-tables.css' in build['resources']
    runtime = (page.parent / unquote(urlsplit(doc.select_one('link[rel=stylesheet]')['href']).path)).resolve().parent
    used=None
    if public_candidate:
        from zo_publish import asset_dependencies, tree_manifest
        public_root=page.parents[5]
        missing_assets=[]
        used=asset_dependencies(public_root, tree_manifest(public_root, True),
                                [page.relative_to(public_root).as_posix()], missing_assets)
        checks['public referenced asset closure complete']=not missing_assets
    for name, spec in build['resources'].items():
        if used is not None and (runtime/name).relative_to(public_root).as_posix() not in used:
            continue  # Unreferenced template assets are not part of a filtered publication.
        checks['runtime source and copy exact '+name] = sha(REPO/spec['source']) == spec['sha256'] and (runtime/name).is_file() and sha(runtime/name) == spec['sha256']
    missing=[]; parsed={page.resolve():doc}
    for n in doc.select('a[href],img[src],script[src],link[href]'):
        u=urlsplit(n.get('src',n.get('href')))
        if u.scheme or u.netloc:continue
        target=(page.parent/unquote(u.path)).resolve() if u.path else page.resolve()
        if not target.is_file():missing.append(n.get('src',n.get('href')));continue
        if u.fragment and target.suffix=='.html':
            if target not in parsed:parsed[target]=BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
            if not parsed[target].find(id=unquote(u.fragment)):missing.append(n['href'])
    checks['all resources links and fragments exist'] = not missing
    for name, selector in [('missing catalog card','.home-card'),('missing footer','#site-footer'),('wrong illustration','.journey-portrait'),('lost anchor','#lộ-trình')]:
        bad=copy.deepcopy(doc);bad.select_one(selector).decompose()
        checks['negative fixture '+name] = not all(validate(bad,build).values())
    for attribute, value in [('data-countdown-target','2026-06-11T14:30:00+07:00'),('data-countdown-target','2027-06-11T14:30:00Z'),('data-countdown-status','official')]:
        bad=copy.deepcopy(doc);bad.select_one('.home-countdown')[attribute]=value
        checks['negative countdown '+attribute+' '+value] = not validate(bad,build)['countdown target and status from canonical data']
    bad=copy.deepcopy(doc);bad.select_one('.countdown-notice').string='Lịch thi chính thức 2027.'
    checks['negative countdown missing provisional notice'] = not validate(bad,build)['countdown reference notice and fallback truthful']
    bad=copy.deepcopy(doc);bad.select_one('.home-card-action').unwrap()
    checks['negative missing native action link'] = not action_only_cards(bad.select('.home-card'))
    bad=copy.deepcopy(doc);shell=bad.select_one('.home-card-content');shell.name='a';shell['href']='d0-reading.html';shell['class']=['home-card-link']
    checks['negative restored whole card anchor'] = not action_only_cards(bad.select('.home-card'))
    bad=copy.deepcopy(doc);bad.select_one('.home-card')['onclick']='location.href="d0-reading.html"'
    checks['negative restored card click handler'] = not action_only_cards(bad.select('.home-card'))
    bad=copy.deepcopy(doc);bad.select_one('.home-card')['tabindex']='0';bad.select_one('.home-card')['role']='link'
    checks['negative restored keyboard card link'] = not action_only_cards(bad.select('.home-card'))
    bad=copy.deepcopy(doc);bad.select_one('#hoc-lieu-hien-co').insert_before(bad.select_one('.home-introduction').extract())
    checks['negative purpose outside opening hero'] = not reading_layout_checks(bad)['intro purpose and audience inside opening hero']
    bad=copy.deepcopy(doc);bad.select_one('.home-service-illustration').decompose()
    checks['negative service illustration removed'] = not reading_layout_checks(bad)['service illustration and copy retained']
    bad=copy.deepcopy(doc);bad.select_one('.home-method-grid > div').decompose()
    checks['negative method row lost'] = not reading_layout_checks(bad)['four complete method rows without verb labels']
    bad=copy.deepcopy(doc);bad.select_one('.home-lead').append(' Gói khảo sát D0')
    checks['negative internal code in learner copy'] = not validate(bad,build)['no visible internal course codes']
    from zo_web_2027_home_landing import countdown_source
    for key,value in [('target','2026-06-11T14:30:00+07:00'),('target','2027-06-11T14:30:00'),('target','2027-06-12T14:30:00+07:00'),('status','unknown'),('target','not-a-date')]:
        program=copy.deepcopy(load_yaml(DATA_PATH)['program']);program['exam_countdown'][key]=value
        try: countdown_source(program); rejected=False
        except (ValueError,TypeError): rejected=True
        checks['negative canonical countdown '+key+' '+value]=rejected
    program=copy.deepcopy(load_yaml(DATA_PATH)['program']);program['exam_countdown'].update(status='official',target='2027-06-12T14:30:00+07:00')
    checks['official mode changes copy from same configuration']='Lịch thi chính thức' in countdown_source(program) and 'chưa phải lịch' not in countdown_source(program)
    return checks, missing


def browser(page, out):
    out.mkdir(parents=True,exist_ok=True); checks={}; measures=[]
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    base=f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix='_tmp_browser_',dir=out,ignore_cleanup_errors=True) as profile:
        proc=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1',f'--remote-debugging-port={port}','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        b=None
        try:
            for _ in range(100):
                try:
                    if requests.get(base+'/json/version',timeout=.3).ok:break
                except requests.RequestException:pass
                time.sleep(.1)
            tab=next(t for t in requests.get(base+'/json',timeout=3).json() if t['type']=='page');b=Browser(tab['webSocketDebuggerUrl']);b.ws.settimeout(45);b.call('Page.enable');b.call('Runtime.enable')
            def pointer_click(selector):
                b.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"center"})')
                point=b.evaluate('(()=>{const r=document.querySelector('+json.dumps(selector)+').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()')
                for event in ['mousePressed','mouseReleased']:b.call('Input.dispatchMouseEvent',dict(type=event,button='left',clickCount=1,**point))
                time.sleep(.15)
            for width in [1440,1000,768,430,390,320]:
                b.viewport(width,900);b.navigate(page.as_uri())
                for _ in range(50):
                    if b.evaluate('!!document.querySelector(".home-landing-content")'):break
                    time.sleep(.1)
                b.ready()
                result=b.evaluate("""(()=>{const v=n=>!!n&&!!n.getClientRects().length&&!n.closest('[hidden]');return {url:location.href,title:document.title,fits:document.documentElement.scrollWidth<=innerWidth,loaded:[...document.images].every(n=>n.complete&&n.naturalWidth>0),paper:[...document.querySelectorAll('.home-paper')].every(n=>['rgb(255, 255, 255)','rgb(247, 247, 245)'].includes(getComputedStyle(n).backgroundColor)),overflow:[...document.querySelectorAll('main h1,main h2,main h3,main p,main li,summary')].filter(v).filter(n=>n.scrollWidth>n.clientWidth+2).map(n=>n.textContent.slice(0,50)),image:[...document.querySelectorAll('.home-journey img')].filter(v).map(n=>({name:n.className,ratio:n.clientWidth/n.clientHeight,native:n.naturalWidth/n.naturalHeight})),logo:v(document.querySelector('.site-top>a:first-child')),tools:v(document.querySelector('.course-tools')),font:document.fonts.check('17px Be'),closed:!document.querySelector('details[open]')};})()""")
                measures.append({'width':width,'geometry':result})
                for name in ['fits','loaded','paper','logo','tools','font','closed']:checks[f'{width} {name}']=result[name]
                layout=b.evaluate(READING_LAYOUT_GEOMETRY)
                measures[-1]['reading_layout']=layout
                checks[f'{width} method one full-width column']=layout['columns']==1 and layout['fullWidth'] and layout['gaps']
                for key in ['methodFrames','methodAlternates','topicFrames','faqFrames','faqAlternates','panelsAlternate','serviceFits']:checks[f'{width} '+key]=layout[key]
                checks[f'{width} topic responsive columns']=layout['topicColumns']==(1 if width<=650 else 2)
                b.evaluate('document.querySelectorAll(".home-faq details").forEach(n=>n.open=true)')
                checks[f'{width} open FAQ text not clipped']=b.evaluate('[...document.querySelectorAll(".home-faq p,.home-faq summary")].every(n=>n.scrollWidth<=n.clientWidth+2)&&document.documentElement.scrollWidth<=innerWidth')
                b.evaluate('document.querySelectorAll(".home-faq details").forEach(n=>n.open=false)')
                if width in [1440,390]:
                    b.evaluate('window.__badColumns=document.createElement("style");window.__badColumns.textContent=".home-editorial .home-method-grid{grid-template-columns:repeat(4,minmax(0,1fr))!important}";document.head.append(window.__badColumns)')
                    broken=b.evaluate(READING_LAYOUT_GEOMETRY)
                    checks[f'{width} negative inherited four columns caught']=broken['columns']!=1 and not broken['fullWidth']
                    b.evaluate('window.__badColumns.remove()')
                    for selector,name in [('.home-introduction','intro'),('.home-method-grid','method-rows'),('.home-strands','topics'),('.home-service','service'),('.home-faq','faq')]:
                        b.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"center"})');b.screenshot(out/f'{name}-{width}.png')
                    b.evaluate('window.scrollTo(0,0)')
                checks[f'{width} no text overflow']=not result['overflow']
                checks[f'{width} one intact illustration']=len(result['image'])==1 and abs(result['image'][0]['ratio']-result['image'][0]['native'])<.01
                checks[f'{width} days label one line centered']=b.evaluate("""(()=>{const n=document.querySelector('.countdown-days>span'),s=n.previousElementSibling,a=n.getBoundingClientRect(),c=s.getBoundingClientRect();return getComputedStyle(n).whiteSpace==='nowrap'&&Math.abs(a.y+a.height/2-c.y-c.height/2)<1&&a.width+n.offsetLeft<=innerWidth&&getComputedStyle(n).fontSize==='13px'})()""")
                save(out/'measurements.json',measures)
                b.screenshot(out/f'home-{width}.png')
                b.click('[data-course-action=list]')
                checks[f'{width} course menu opens']=b.evaluate('document.querySelector(".zo-course-menu").open&&document.querySelectorAll(".course-panel a").length===4')
                b.key('Escape',27);checks[f'{width} Escape closes course menu']=b.evaluate('!document.querySelector(".zo-course-menu").open')
                b.click('[data-filter=functions]');checks[f'{width} functions filter']=b.evaluate('document.querySelectorAll(".home-card:not([hidden])").length===2')
                b.click('[data-filter=all]')
                b.evaluate('document.querySelector("#home-search").value="cuc tri";document.querySelector("#home-search").dispatchEvent(new Event("input"))')
                checks[f'{width} accent insensitive search']=b.evaluate('[...document.querySelectorAll(".home-card:not([hidden])")].map(n=>n.dataset.packageId).join() === "r1_g01,r1_g02"')
                b.evaluate('document.querySelector("#home-search").value="no-such-package";document.querySelector("#home-search").dispatchEvent(new Event("input"))')
                checks[f'{width} empty results status']=b.evaluate('document.querySelectorAll(".home-card:not([hidden])").length===0&&!document.querySelector(".home-filter-status").hidden')
                b.evaluate('document.querySelector("#home-search").value="";document.querySelector("#home-search").dispatchEvent(new Event("input"))')
                b.click('.home-faq summary');checks[f'{width} FAQ opens']=b.evaluate('document.querySelector(".home-faq details").open')
                b.click('.home-faq summary')
                b.click('.home-section-nav a[href="#hoc-lieu-hien-co"]');b.ready()
                checks[f'{width} anchor clears toolbar']=b.evaluate('document.querySelector("#hoc-lieu-hien-co").getBoundingClientRect().top>=document.querySelector(".site-top").getBoundingClientRect().bottom-1')
                b.screenshot(out/f'catalog-{width}.png')
                # Real pointer hover, not element.click() or a CSS class fixture.
                selector='.home-section-nav a'
                b.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"center"})')
                point=b.evaluate('(()=>{const r=document.querySelector('+json.dumps(selector)+').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()')
                b.call('Input.dispatchMouseEvent',dict(type='mouseMoved',**point));time.sleep(.2)
                checks[f'{width} nav hover only text no box underline']=b.evaluate('(()=>{const s=getComputedStyle(document.querySelector(".home-section-nav a"));return s.backgroundColor==="rgba(0, 0, 0, 0)"&&s.textDecorationLine==="none"})()')
                b.evaluate('document.querySelector(".home-card").scrollIntoView({block:"center"})')
                b.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':1,'y':1});time.sleep(.2)
                before_card=b.evaluate('(()=>{const n=document.querySelector(".home-card"),r=n.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,shadow:getComputedStyle(n).boxShadow}})()')
                point=b.evaluate('(()=>{const r=document.querySelector(".home-card img").getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()')
                b.call('Input.dispatchMouseEvent',dict(type='mouseMoved',**point));time.sleep(.25)
                after_card=b.evaluate('(()=>{const n=document.querySelector(".home-card"),r=n.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,shadow:getComputedStyle(n).boxShadow,underline:getComputedStyle(n.querySelector("a")).textDecorationLine,background:getComputedStyle(n.querySelector("a")).backgroundColor}})()')
                checks[f'{width} whole card reacts without geometry shift']=before_card['shadow']!=after_card['shadow'] and all(before_card[k]==after_card[k] for k in ['x','y','w','h'])
                checks[f'{width} card no hover fill underline']=after_card['underline']=='none' and after_card['background']=='rgba(0, 0, 0, 0)'
                if width in [1440,390]:b.screenshot(out/f'card-hover-{width}.png')
                for package in ['d0','r1_g01','r1_g02']:
                    for part in ['img','h3','p']:
                        before_url=b.evaluate('location.href')
                        pointer_click(f'.home-card[data-package-id={package}] {part}')
                        checks[f'{width} {package} {part} click stays on Home']=b.evaluate('location.href')==before_url
                    selector=f'.home-card[data-package-id={package}]'
                    b.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"center"})')
                    point=b.evaluate('(()=>{const r=document.querySelector('+json.dumps(selector)+').getBoundingClientRect();return {x:r.x+4,y:r.y+4}})()')
                    for event in ['mousePressed','mouseReleased']:b.call('Input.dispatchMouseEvent',dict(type=event,button='left',clickCount=1,**point))
                    checks[f'{width} {package} card background click stays on Home']=b.evaluate('location.href')==before_url
                b.evaluate('document.querySelector(".home-card-action").scrollIntoView({block:"center"})')
                b.call('Input.dispatchMouseEvent',{'type':'mouseMoved','x':1,'y':1});time.sleep(.2)
                before_action=b.evaluate('(()=>{const n=document.querySelector(".home-card-action");return {color:getComputedStyle(n).color,arrow:getComputedStyle(n.querySelector("span")).transform}})()')
                point=b.evaluate('(()=>{const r=document.querySelector(".home-card-action").getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()')
                b.call('Input.dispatchMouseEvent',dict(type='mouseMoved',**point));time.sleep(.25)
                after_action=b.evaluate('(()=>{const n=document.querySelector(".home-card-action"),s=getComputedStyle(n);return {color:s.color,arrow:getComputedStyle(n.querySelector("span")).transform,clean:s.backgroundColor==="rgba(0, 0, 0, 0)"&&s.textDecorationLine==="none"}})()')
                checks[f'{width} action hover responds without fill underline']=after_action['clean'] and after_action['color']!=before_action['color'] and after_action['arrow']!=before_action['arrow']
                checks[f'{width} card shell not interactive pointer']=b.evaluate('[...document.querySelectorAll(".home-card,.home-card-content,.home-card img,.home-card h3,.home-card p")].every(n=>getComputedStyle(n).cursor!=="pointer"&&!n.closest("a"))')
                b.evaluate('document.querySelector("#home-search").focus()');b.key('Tab',9)
                checks[f'{width} card keyboard focus visible']=b.evaluate('getComputedStyle(document.activeElement).outlineStyle!=="none" && getComputedStyle(document.querySelector(".home-card")).boxShadow!=="none"')
                b.key('Tab',9)
                checks[f'{width} Tab goes to next CTA not card']=b.evaluate('document.activeElement.matches(".home-card[data-package-id=r1_g01] .home-card-action")')
                b.evaluate('document.activeElement.blur()')
                b.evaluate('document.querySelector("#ung-ho").scrollIntoView()');b.screenshot(out/f'support-{width}.png')
                b.click('[data-course-action=top]');checks[f'{width} top works']=b.evaluate('scrollY<2')
            b.viewport(1440,900);b.navigate(page.as_uri())
            checks['countdown starts and no noisy live announcements']=b.evaluate('document.querySelector(".home-countdown").dataset.countdownState==="running" && !document.querySelector(".countdown-readout").hidden && document.querySelector(".countdown-readout").getAttribute("aria-live")==="off"')
            first=b.evaluate('document.querySelector("[data-time=seconds]").textContent');time.sleep(2.1)
            checks['countdown really ticks without interaction']=first!=b.evaluate('document.querySelector("[data-time=seconds]").textContent')
            b.evaluate('window.__clockRealNow=Date.now;window.__clockTarget=Date.parse(document.querySelector(".home-countdown").dataset.countdownTarget);window.__clockNow=window.__clockTarget-90061000;Date.now=()=>window.__clockNow;document.dispatchEvent(new Event("visibilitychange"))')
            read='[...document.querySelectorAll(".countdown-readout [data-time]")].map(n=>n.textContent).join(":")'
            config=load_yaml(DATA_PATH)['program']['exam_countdown']
            utc_target=datetime.fromisoformat(config['target']).astimezone(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
            checks['countdown Vietnam target UTC exact']=b.evaluate('new Date(window.__clockTarget).toISOString()==='+json.dumps(utc_target))
            checks['countdown day hour minute second arithmetic']=b.evaluate(read)=='1:01:01:01'
            b.evaluate('window.__clockNow+=2000;document.dispatchEvent(new Event("visibilitychange"))')
            checks['countdown minute borrow on delayed resume']=b.evaluate(read)=='1:01:00:59'
            b.evaluate('window.__clockNow=window.__clockTarget-1;document.dispatchEvent(new Event("visibilitychange"))')
            checks['countdown not expired a millisecond early']=b.evaluate(read)=='0:00:00:01'
            b.evaluate('window.__clockNow=window.__clockTarget+86400000;document.dispatchEvent(new Event("visibilitychange"))')
            checks['countdown expiry clamps zero not negative']=b.evaluate(read)=='0:00:00:00' and b.evaluate('document.querySelector(".home-countdown").dataset.countdownState==="ended" && !document.querySelector(".countdown-ended").hidden')
            checks['countdown expiry reference not official exam start']=config['status']!='reference' or b.evaluate('document.querySelector(".countdown-ended").textContent.includes("không xác nhận")')
            b.evaluate('Date.now=window.__clockRealNow;document.dispatchEvent(new Event("visibilitychange"))')
            checks['countdown refresh recovers correct clock']=b.evaluate('document.querySelector(".home-countdown").dataset.countdownState==="running" && document.querySelector(".countdown-ended").hidden')
            b.call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
            checks['countdown reduced motion no sweep animation']=b.evaluate('getComputedStyle(document.querySelector(".countdown-sweep")).transitionDuration==="0s"')
            b.call('Emulation.setEmulatedMedia',{'features':[]})
            b.screenshot(out/'countdown-desktop.png')
            for anchor,name in [('chương-trình-giúp-em-làm-gì','purpose'),('học-theo-cách-nào','method'),('tám-mạch','strands'),('hoc-truc-tiep','service'),('nguon-hoc-lieu','sources'),('cau-hoi-thuong-gap','faq')]:
                b.evaluate('document.getElementById('+json.dumps(anchor)+').scrollIntoView()');b.screenshot(out/(name+'-desktop.png'))
            b.click('[data-course-action=list]')
            b.evaluate('document.querySelector(".course-panel a").focus()')
            checks['course current link no underline']=b.evaluate('getComputedStyle(document.querySelector(".course-panel [aria-current=page]")).textDecorationLine==="none"')
            b.key('Escape',27)
            for selector in ['.countdown-notice a','.zo-site-footer__links a','[data-course-action=home]','[data-course-action=list]']:
                b.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"center"})')
                point=b.evaluate('(()=>{const r=document.querySelector('+json.dumps(selector)+').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()')
                b.call('Input.dispatchMouseEvent',dict(type='mouseMoved',**point));time.sleep(.2)
                checks['text hover transparent and no underline '+selector]=b.evaluate('(()=>{const s=getComputedStyle(document.querySelector('+json.dumps(selector)+'));return s.backgroundColor==="rgba(0, 0, 0, 0)"&&s.textDecorationLine==="none"})()')
            for theme in ['gray-3','gray-2','yellow-1','yellow-2','red-1','red-2']:
                b.click('[name=background][value='+theme+']');b.call('Page.reload');b.ready()
                checks['persist '+theme]=b.evaluate(f'document.querySelector("[name=background][value={theme}]").checked')
            b.click('#grayscale');b.call('Page.reload');b.ready();checks['grayscale persists']=b.evaluate('document.documentElement.classList.contains("grayscale")');b.click('#grayscale');b.click('[name=background][value=yellow-1]')
            b.evaluate('document.querySelector("[data-filter=survey]").focus()');b.key('Enter',13,'\r');checks['keyboard catalog filter']=b.evaluate('document.querySelectorAll(".home-card:not([hidden])").length===1')
            b.viewport(430,900);b.navigate(page.as_uri());b.click('.mobile-trigger');checks['mobile contents drawer opens']=b.evaluate('document.querySelector("#mobile-nav").open');b.key('Escape',27);checks['mobile drawer Escape']=b.evaluate('!document.querySelector("#mobile-nav").open')
            checks['mobile trigger shows icon not words']=b.evaluate('getComputedStyle(document.querySelector(".mobile-view")).display==="none"')
            for package, filename in [('d0','d0-reading.html'),('r1_g01','g01-reading.html'),('r1_g02','g02-reading.html')]:
                b.navigate(page.as_uri());pointer_click(f'.home-card[data-package-id={package}] .home-card-action');b.ready()
                checks['real navigation '+package]=b.evaluate(f'location.pathname.endsWith({json.dumps(filename)}) && !!document.querySelector("main")')
                if package!='d0':checks['start view '+package]=b.evaluate('new URL(location.href).searchParams.get("r1-view")==="bat-dau" && location.hash==="#bat-dau"')
                b.click('[data-course-action=home]');b.ready()
                checks['return to new Home '+package]=b.evaluate('document.body.classList.contains("home-editorial")')
            b.evaluate('document.querySelector(".home-card-action").focus()');b.key('Enter',13,'\r');b.ready()
            checks['keyboard Enter on CTA opens D0']=b.evaluate('location.pathname.endsWith("d0-reading.html")')
            b.navigate(page.as_uri());b.ready()
            # Browser zoom reduces the CSS viewport and scales the rendering.
            # body.style.zoom doubles boxes WITHOUT changing media queries and
            # is not a valid browser-zoom emulation. Keep that first result in QA.
            b.call('Emulation.setDeviceMetricsOverride',{'width':384,'height':450,'deviceScaleFactor':2,'mobile':False})
            b.navigate(page.as_uri());b.ready()
            checks['200 percent effective viewport reflow simulation']=b.evaluate('document.documentElement.scrollWidth<=innerWidth+1 && !!document.querySelector(".course-tools").getClientRects().length')
            b.screenshot(out/'home-200-percent.png')
            for width in [1440,390]:
                b.call('Emulation.setScriptExecutionDisabled',{'value':True});b.viewport(width,900);b.navigate(page.as_uri())
                checks[f'{width} no JS all cards usable']=b.evaluate('document.querySelectorAll(".home-card:not([hidden])").length===3&&document.querySelector(".home-catalog-tools").hidden')
                checks[f'{width} no JS menu native']=b.evaluate('document.querySelector(".zo-course-menu").tagName==="DETAILS"')
                checks[f'{width} no JS clock honest fallback']=b.evaluate('document.querySelector(".countdown-readout").hidden && !document.querySelector(".countdown-fallback").hidden && !!document.querySelector(".countdown-date time[datetime]")')
                b.screenshot(out/f'nojs-{width}.png')
                b.evaluate('document.querySelector(".home-card img").scrollIntoView({block:"center"})')
                point=b.evaluate('(()=>{const r=document.querySelector(".home-card img").getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()')
                for event in ['mousePressed','mouseReleased']:b.call('Input.dispatchMouseEvent',dict(type=event,button='left',clickCount=1,**point))
                time.sleep(.3);b.ready()
                checks[f'{width} no JS image click stays on Home']=b.evaluate('location.href')==page.as_uri()
                b.click('.home-card-action');time.sleep(.3);b.ready()
                checks[f'{width} no JS action opens D0']=b.evaluate('location.pathname.endsWith("d0-reading.html")')
                b.call('Emulation.setScriptExecutionDisabled',{'value':False})
            save(out/'measurements.json',measures)
        finally:
            if b:b.ws.close()
            proc.terminate();proc.wait(timeout=15)
    return checks


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--html',type=Path,required=True);p.add_argument('--build',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--preview',action='store_true');p.add_argument('--browser',action='store_true')
    for key in ['d0', 'g01', 'g02']: p.add_argument('--'+key, type=Path)
    a=p.parse_args()
    out=a.output.resolve()
    if not out.is_relative_to(REPO/'_audit') or out==REPO/'_audit':p.error('Named _audit output required')
    out.mkdir(parents=True,exist_ok=True);page=a.html.resolve();build=json.loads(a.build.read_text(encoding='utf-8'))
    if a.preview:
        if not all([a.d0, a.g01, a.g02]): p.error('--preview requires explicit --d0, --g01 and --g02 inputs')
        page=preview(page,out,{'d0':a.d0.resolve(), 'r1_g01':a.g01.resolve(), 'r1_g02':a.g02.resolve()})
    checks,missing=static(page,build)
    if a.browser:checks.update(browser(page,out/'images'))
    report={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failures':[k for k,v in checks.items() if not v],'missing_links':missing,'html_sha256':sha(page),'owner_acceptance':'pending','published':False,'limits':['Edge only; not Safari, Firefox, real device or screen reader.','200 percent effective viewport is simulated, not native browser shortcut zoom.','Home-only QA, not mathematical or PDF audit.']}
    target=out/'qa.json'
    if target.exists():target=out/('qa-'+str(time.time_ns())+'.json')
    report['checker_sha256']=sha(Path(__file__))
    save(target,report);print(json.dumps({k:report[k] for k in ['passed','total','failures','missing_links']},ensure_ascii=False))
    return int(bool(report['failures']))

if __name__=='__main__':raise SystemExit(main())
