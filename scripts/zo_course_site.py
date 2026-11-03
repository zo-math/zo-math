"""Build the canonical 2027 site after successful native QMD validation.

The UI consumes only HTML just produced in this invocation. It never reads the
R01 repository, prototype inputs, audit snapshots, or a previous final HTML.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit,unquote
import argparse,json,hashlib,os,shutil,sys
from collections import Counter
from bs4 import BeautifulSoup
from zo_course_site_sources import context as c

ROOT=c.ROOT
CURRENT=ROOT/c.HOME/'_quy_trinh/ho_so/current_site_build.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8')
def relevant(raw):
    known={v.with_suffix('.qmd') for v in [*c.PAGES.values(),c.FOUNDATION]}
    result=[]
    for item in raw:
        p=Path(item);p=p.resolve().relative_to(ROOT) if p.is_absolute() else p
        if p in known:result.append(p)
    return result
def fingerprint(node):
    from copy import deepcopy
    text_node=deepcopy(node)
    for label in text_node.select('[data-r20-review-label]'):label.decompose()
    return {'text':' '.join(text_node.get_text(' ',strip=True).split()),'math':[str(m) for m in node.select('math')],'ids':[n['id'] for n in node.select('[id]')],'headings':[(n.name,n.get_text()) for n in node.select('h1,h2,h3,h4,h5,h6')],'images':len(node.select('img')),'tables':len(node.select('table')),'disclosures':[(n.get('id'),n.has_attr('open'),n.select_one('summary').get_text(' ',strip=True) if n.select_one('summary') else '') for n in node.select('details')]}
def prepare_reader(doc,key):
    root=doc.select_one('.reader-content')
    if root is None:raise ValueError('Native reader missing: '+key)
    # Lifecycle text is replaced explicitly; no learning sentence is rewritten.
    notes=[]
    for n in root.select('.zo-pdf-current-note'):
        notes.append(n.get_text(' ',strip=True))  # Preserve the live provenance label emitted by the native adapter.
    before=fingerprint(root)
    on_lai=root.select_one('#on-lai')
    if on_lai:
        bindings=json.loads(root.get('data-r1-review-rounds','[]'))
        markers=[n for n in on_lai.select('[data-zo-context]') if str(n.get('data-zo-context','')).startswith('round:') and not n.find_parent(attrs={'data-zo-context':True})]
        if not markers and bindings:
            targets=[root.find(id=b['target']) for b in bindings]
            if any(n is None or n.parent is not on_lai for n in targets):raise ValueError('Unexpected declared review boundaries in '+key)
            for index,(first,binding) in enumerate(zip(targets,bindings)):
                stop=targets[index+1] if index+1<len(targets) else None
                group=[];node=first
                while node is not None and node is not stop:
                    group.append(node);node=node.next_sibling
                panel=doc.new_tag('details',attrs={'class':'zo-learning-guidance r01-review-round','name':'r01-review-rounds'})
                summary=doc.new_tag('summary');label=doc.new_tag('span',attrs={'data-r20-review-label':binding['view']});label.string=binding['label'];summary.append(label);panel.append(summary)
                first.insert_before(panel)
                for node in group:panel.append(node.extract())
        for outer in markers:
            if outer.select_one('details.r01-review-round'):continue
            heading=outer.find(['h3','h4'])
            if heading is None:raise ValueError('Review round lacks heading: '+key)
            prefix=[]
            for child in list(heading.parent.contents):
                prefix.append(child)
                if child is heading:break
                if getattr(child,'name',None) and 'role' not in child.get('class',[]):raise ValueError('Unexpected pre-heading content: '+key)
            panel=doc.new_tag('details',attrs={'class':'zo-learning-guidance r01-review-round','name':'r01-review-rounds'})
            summary=doc.new_tag('summary')
            for child in prefix:summary.append(child.extract())
            panel.append(summary)
            for child in list(outer.contents):panel.append(child.extract())
            outer.append(panel);outer['data-zo-review-disclosure']='closed'
        panels=on_lai.select('details.r01-review-round')
        if len(panels)!=3:raise ValueError('Expected three declared independent review rounds in '+key)
        for panel in panels:panel['name']='r01-review-rounds'
    after=fingerprint(root)
    # Grouping checkpoints changes ID traversal order only if content moved;
    # all original text, notation, headings, IDs and disclosures must survive.
    for field in ['text','math','ids','headings','images','tables']:
        if before[field]!=after[field]:raise ValueError('Review grouping changed '+field+' in '+key)
    if not all(d in after['disclosures'] for d in before['disclosures']):raise ValueError('Existing answer disclosure lost')
    return doc,notes
def install_assets():
    c.ASSETS.mkdir(parents=True,exist_ok=True)
    for name in ['site.css','course-redesign.css','learning-redesign.css','guidance.css','learning-format.css','app.js','presence.js','foundation-return.js']:
        src=c.DESIGN/name;dest=c.ASSETS/name
        if not dest.exists() or sha(src)!=sha(dest):shutil.copyfile(src,dest)
    for name in ['revision-review-rounds.css','revision-review-rounds.js']:
        shutil.copyfile(ROOT/'scripts/assets'/name,c.ASSETS/name.replace('revision-',''))
    palette=json.loads((ROOT/'_design/ngon_ngu_thiet_ke_zo_math_0_4/03_du_lieu/color_system.json').read_text('utf-8'))['palette']
    (c.ASSETS/'zo-colors.css').write_text(':root{'+''.join('--zo-'+k+':'+v+';' for k,v in palette.items())+'}\n','utf-8')
    font=ROOT/'_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/assets'
    (c.ASSETS/'fonts').mkdir(exist_ok=True)
    for name in ['BeVietnamPro_Regular.ttf','BeVietnamPro_SemiBold.ttf','STIXTwoMath.ttf','OFL_BeVietnamPro.txt','OFL_STIX.txt']:
        shutil.copyfile(font/name,c.ASSETS/'fonts'/name)
    shutil.copyfile(ROOT/'_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/logos/horizontal_color.svg',c.ASSETS/'logo.svg')
    shutil.copyfile(ROOT/'assets/images/qr_bao_tro_zo_math_vietcombank.jpg',c.ASSETS/'qr.jpg')
def local_check(pages):
    cache={}
    failures=[];references=0
    for page in pages:
        doc=BeautifulSoup(page.read_text('utf-8'),'html.parser')
        ids=[n['id'] for n in doc.select('[id]')]
        if len(ids)!=len(set(ids)):failures.append(str(page)+': duplicate IDs '+str([x for x,n in Counter(ids).items() if n>1]))
        for n in doc.select('[href],[src],[poster],[data]'):
            for attr in ['href','src','poster','data']:
                if not n.get(attr):continue
                u=urlsplit(n[attr])
                if u.scheme or u.netloc:continue
                target=(c.OUT/unquote(u.path).lstrip('/')).resolve() if u.path.startswith('/') else (page.parent/unquote(u.path)).resolve() if u.path else page
                references+=1
                if not target.is_file():failures.append(f'{page.name}: missing {n[attr]}');continue
                if u.fragment and target.suffix=='.html':
                    if target not in cache:cache[target]={x['id'] for x in BeautifulSoup(target.read_text('utf-8'),'html.parser').select('[id]')}
                    if unquote(u.fragment) not in cache[target]:failures.append(f'{page.name}: missing anchor {n[attr]}')
        text=doc.get_text(' ',strip=True)
        for token in ['BẢN THẢO ĐỘC LẬP','Chờ chủ trì duyệt','Bản sửa độc lập R01','Về bản thiết kế này']:
            if token in text:failures.append(page.name+': stale prototype text '+token)
    return {'pages':len(pages),'references':references,'failures':failures}
def live_inputs():
    from zo_course_site_dependencies import build_sources
    files=build_sources(ROOT,c)
    return {p.relative_to(ROOT).as_posix():sha(p) for p in sorted(files)}

def freshness(record):
    failures=[]
    current=live_inputs()
    if 'page_inputs' in record:
        for page,changes in scope_state(record)[2].items():
            failures.append('Pending page: '+page+' ('+', '.join(changes)+')')
    else:
        for path in sorted(set(current)|set(record['inputs'])):
            if current.get(path)!=record['inputs'].get(path):failures.append('Changed input: '+path)
    for path,digest in record['outputs'].items():
        p=c.OUT/path
        if not p.is_file() or sha(p)!=digest:failures.append('Changed output: '+path)
    for path,digest in record.get('assets',{}).items():
        p=c.OUT/path
        if not p.is_file() or sha(p)!=digest:failures.append('Changed asset: '+path)
    return failures

def catalog_metadata():
    import yaml
    result={}
    for key,page in c.PAGES.items():
        text=(ROOT/page.with_suffix('.qmd')).read_text('utf-8')
        result[key]=yaml.safe_load(text.split('---',2)[1])
    return result

def validate_render_scope(selected):
    """Validate the requested pages; never expand a local render to the course."""
    known={v.with_suffix('.qmd') for v in [*c.PAGES.values(),c.FOUNDATION]}
    unknown=set(selected)-known
    if unknown:raise ValueError('Unknown course sources: '+str(sorted(unknown)))
    if not selected:raise ValueError('Select at least one source')

def scope_state(record):
    from zo_course_site_scope import TABLES, page_inputs, baseline, stale_pages
    inputs=live_inputs();tables=json.loads((ROOT/TABLES).read_text('utf-8'))
    current=page_inputs(ROOT,c,inputs,catalog_metadata(),tables)
    previous=baseline(ROOT,c,record,inputs,tables)
    return previous,current,stale_pages(previous,current),tables


def project_rendered(raw_paths,report=None,native_input=None):
    selected=relevant(raw_paths)
    if not selected:return 0
    validate_render_scope(selected)
    from zo_course_site_sources import build as b
    c.FRESH.clear();native={};records=[]
    for source in selected:
        page=source.with_suffix('.html');text=native_input[page] if native_input is not None else (c.OUT/page).read_text('utf-8')
        if 'data-zo-course-site=' in text:raise ValueError('Expected a fresh native render, received previous final HTML')
        native[page]=text
        for key,value in c.PAGES.items():
            if value==page:c.FRESH[key]=text
    install_assets()
    results={}
    for page,text in native.items():
        c.PAGE=page;items=c.catalog()
        key=next((k for k,v in c.PAGES.items() if v==page),None)
        if key=='home':result=b.home(items)
        elif key in c.KEYS:
            doc,notes=prepare_reader(BeautifulSoup(text,'html.parser'),key)
            c.FRESH[key]=str(doc)
            item=next(p for p in items if p['id']==key)
            result,record=b.reader(item,items)
            result=c.finish(result,page)
            target=BeautifulSoup(result,'html.parser').select_one('.reader-content')
            assert fingerprint(target)==fingerprint(doc.select_one('.reader-content')),key+' native-to-r20 projection drift'
            record.update(source=str(page.with_suffix('.qmd')),source_sha256=sha(ROOT/page.with_suffix('.qmd')),lifecycle_notes_replaced=notes,review_rounds_closed=len(target.select('details.r01-review-round:not([open])')))
            records.append(record)
        elif page==c.FOUNDATION:
            doc=BeautifulSoup(text,'html.parser');content=doc.select_one('main.content')
            if content is None:raise ValueError('Foundation native content missing')
            content.attrs.pop('id',None);content.name='article';content['class']=['reader-content']
            import yaml
            title=yaml.safe_load((ROOT/page.with_suffix('.qmd')).read_text('utf-8').split('---',2)[1])['title']
            # This independent resource keeps its own outline and native answer
            # disclosure script; it is not a segmented specialist package.
            links=[]
            for heading in content.select('h2,h3'):
                target=heading if heading.get('id') else heading.find_parent(id=True)
                if target is not None:
                    label=BeautifulSoup(str(heading),'html.parser')
                    for annotation in label.select('annotation'):annotation.decompose()
                    links.append('<a class="foundation-toc-'+heading.name+'" href="#'+b.esc(target['id'],quote=True)+'">'+b.esc(label.get_text(' ',strip=True))+'</a>')
            contents='<details class="foundation-contents"><summary>Trong tài nguyên này</summary><nav aria-label="Mục lục Ôn nền">'+''.join(links)+'</nav></details>'
            body=b.header('guide')+'<main id="main-content" class="utility-main"><div id="foundation-return" hidden></div><header><h1>'+b.esc(title)+'</h1></header>'+contents+str(content)+'</main>'+b.footer()
            result=b.document(doc.title.get_text().removesuffix(' – ZO Math'),body,'foundation',{'catalog':items})
            native_scripts=[n['src'] for n in doc.select('script[src]') if n['src'].endswith('giao_dien/so_gan_dung_sai_so.js')]
            if len(native_scripts)!=1:raise ValueError('Foundation canonical answer-reveal script missing or repeated')
            result=result.replace('</body>','<script src="'+b.esc(native_scripts[0],quote=True)+'" defer></script><script src="foundation-return.js" defer></script></body>')
        else:continue
        results[page]=c.finish(result,page)
    if c.PAGES['home'].with_suffix('.qmd') in selected:
        c.PAGE=c.PAGES['home'];items=c.catalog()
        for name,html in [('chuyen-de.html',b.topics(items)),('da-luu.html',b.saved(items)),('cach-hoc.html',b.guide())]:results[c.HOME/name]=c.finish(html,c.HOME/name)
        for g in b.GUIDES:results[c.HOME/g['file']]=c.finish(b.detailed_guide(g,items),c.HOME/g['file'])
    for page,text in results.items():
        dest=c.OUT/page;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text,'utf-8')
    check=local_check([c.OUT/p for p in results])
    # Prune only after a complete build has valid final pages. A partial
    # render must not retire assets of a page it did not regenerate.
    removed=[]
    if not check['failures'] and len(selected)==len(c.PAGES)+1:
        from zo_course_site_output import prune
        removed=prune(ROOT,c.OUT,[c.OUT/p for p in results])
    data={'built_at':datetime.now(timezone.utc).isoformat(),'root':str(ROOT),'source_mode':'fresh native QMD after existing source and render validators','sources':{p.as_posix():sha(ROOT/p) for p in selected},'outputs':{p.as_posix():sha(c.OUT/p) for p in results},'packages':records,'local_links':check,'retired_generated_assets':removed,'PDF_built':False,'published':False,'owner_acceptance':False}
    out=Path(report).with_name(Path(report).stem+'-site.json') if report else ROOT/'_audit/course_site_build.json'
    if not out.is_absolute():out=ROOT/out
    save(out,data)
    if check['failures']:raise ValueError('Course site check failed: '+str(check['failures'][:20]))
    prior=json.loads(CURRENT.read_text('utf-8')) if CURRENT.is_file() else {}
    combined=dict(prior.get('outputs',{}),**data['outputs'])
    # All declared sources must have final HTML, never a native/intermediate page.
    complete=all((c.OUT/p).is_file() and 'data-zo-course-site=' in (c.OUT/p).read_text('utf-8') for p in [*c.PAGES.values(),c.FOUNDATION])
    record=dict(data,inputs=live_inputs(),catalog_metadata=catalog_metadata(),outputs=combined,assets={p.relative_to(c.OUT).as_posix():sha(p) for p in c.ASSETS.rglob('*') if p.is_file()},complete=complete)
    from zo_course_site_scope import merge_evidence, stale_pages
    previous,current,pending,tables=scope_state(prior)
    record['page_inputs']=merge_evidence(previous,current,[p.as_posix() for p in results])
    record['table_profiles']=tables
    record['pending_pages']=stale_pages(record['page_inputs'],current)
    save(CURRENT,record)
    from zo_course_site_protection import refresh
    refresh(ROOT,c,record)
    print('COURSE SITE: PASS; pages='+str(len(results))+'; references='+str(check['references']))
    return 0
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['build','check','plan']);parser.add_argument('--report',default='_audit/course_site_build.json');parser.add_argument('--page',action='append',default=[]);parser.add_argument('--all',action='store_true',help='Explicit full-course build');args=parser.parse_args(argv)
    if args.command=='plan':
        record=json.loads(CURRENT.read_text('utf-8')) if CURRENT.is_file() else {}
        pending=scope_state(record)[2]
        result={'pending_pages':pending,'automatic_full_build':False}
        save(ROOT/args.report,result);print(json.dumps(result,ensure_ascii=False));return 0
    if args.command=='check' and args.page:
        requested=relevant(args.page)
        if len(requested)!=len(args.page):raise ValueError('Use canonical QMD paths with --page')
        pages=[c.OUT/p.with_suffix('.html') for p in requested]
        record=json.loads(CURRENT.read_text('utf-8'));pending=scope_state(record)[2]
        result=local_check(pages)
        for source in requested:
            key=source.with_suffix('.html').as_posix()
            if key in pending:result['failures'].append('Pending page: '+key)
            if key not in record.get('outputs',{}) or not (c.OUT/key).is_file() or sha(c.OUT/key)!=record['outputs'][key]:
                result['failures'].append('Changed or missing output: '+key)
        result['other_pending_pages']=[p for p in pending if p not in {s.with_suffix('.html').as_posix() for s in requested}]
        save(ROOT/args.report,result);print(json.dumps(result,ensure_ascii=False));return int(bool(result['failures']))
    if args.command=='check':
        pages=[c.OUT/p for p in [*c.PAGES.values(),c.FOUNDATION]]
        from zo_course_site_sources.guidance_content import GUIDES
        pages += [c.OUT/c.HOME/n for n in ['chuyen-de.html','cach-hoc.html','da-luu.html',*[g['file'] for g in GUIDES]]]
        result=local_check(pages);record=json.loads(CURRENT.read_text('utf-8'));result['failures']+=freshness(record);result['failures']+=[] if record.get('complete') else ['Incomplete current course build'];save(ROOT/args.report,result);print(json.dumps(result,ensure_ascii=False));return int(bool(result['failures']))
    import zo_qmd
    if args.all and args.page:parser.error('Choose --page or --all, not both')
    if not args.all and not args.page:parser.error('Select --page <QMD>; use --all only for an explicitly requested full-course build')
    paths=[str(p.with_suffix('.qmd')) for p in [*c.PAGES.values(),c.FOUNDATION]] if args.all else args.page
    if len(relevant(paths))!=len(paths):parser.error('Use canonical course QMD paths')
    return zo_qmd.main(['render',*paths,'--html-only','--report',args.report])
if __name__=='__main__':raise SystemExit(main())
