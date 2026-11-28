"""Build the canonical 2027 site after successful native QMD validation.

The UI consumes only HTML just produced in this invocation. It never reads the
R01 repository, prototype inputs, audit snapshots, or a previous final HTML.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit,unquote
import argparse,json,hashlib,os,re,shutil,sys
from collections import Counter
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
from zo_course_site_sources import context as c

ROOT=c.ROOT
CURRENT=ROOT/c.HOME/'_quy_trinh/ho_so/current_site_build.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    with NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                            dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(content)
        except BaseException:
            stream.close()
            temporary.unlink(missing_ok=True)
            raise
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
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
    from zo_course_review_disclosures import project_remediation, project_solutions
    root=doc.select_one('.reader-content')
    if root is None:raise ValueError('Native reader missing: '+key)
    if key in {'r1_g01', 'r1_g02'}:
        from zo_course_foundation import validate_local_answers
        from zo_course_labels import answer_action_labels, binding
        source=ROOT/c.PAGES[key].with_suffix('.qmd')
        validate_local_answers(root, binding(source)['units'], answer_action_labels()['forward'])
    # Lifecycle text is replaced explicitly; no learning sentence is rewritten.
    notes=[]
    for n in root.select('.zo-pdf-current-note'):
        notes.append(n.get_text(' ',strip=True))
    if root.select('#tai-tai-lieu .zo-pdf-card'):
        from zo_course_pdf_download_state import apply as apply_pdf_state
        apply_pdf_state(doc,ROOT,c.BASE/'hoc_lieu'/key)
    if key in {'r1_g01', 'r1_g02'}:
        support = root.select_one('#tai-tai-lieu .r1-download-support')
        if support is not None:
            from zo_web_2027_downloads import project_course_support
            support.replace_with(project_course_support(support, c.OUT / c.PAGES[key], c.OUT))
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
    project_remediation(root, doc)
    project_solutions(root)
    after=fingerprint(root)
    # Grouping checkpoints changes ID traversal order only if content moved;
    # all original text, notation, headings, IDs and disclosures must survive.
    for field in ['text','math','ids','headings','images','tables']:
        if before[field]!=after[field]:raise ValueError('Review grouping changed '+field+' in '+key)
    if not all(d in after['disclosures'] for d in before['disclosures']):raise ValueError('Existing answer disclosure lost')
    return doc,notes
def install_assets():
    from zo_topic_art import card_art, load_registry
    (c.ASSETS/'illustrations').mkdir(parents=True,exist_ok=True)
    for key in load_registry(ROOT)['packages']:
        src,_=card_art(ROOT,key);dest=c.ASSETS/'illustrations'/(key+'.png')
        if not dest.exists() or sha(src)!=sha(dest):shutil.copyfile(src,dest)
    c.ASSETS.mkdir(parents=True,exist_ok=True)
    for name in ['site.css','course-redesign.css','learning-redesign.css','guidance.css','learning-format.css','app.js','presence.js','foundation-return.js']:
        src=c.DESIGN/name;dest=c.ASSETS/name
        data=c.presence_script() if name=='presence.js' else src.read_bytes()
        if not dest.exists() or dest.read_bytes()!=data:dest.write_bytes(data)
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
    from zo_course_site_sections import build_lock
    with build_lock(ROOT/'.quarto/course-site-sections.lock'):
        return _project_rendered(raw_paths,report,native_input)

def _project_rendered(raw_paths,report,native_input):
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
    from zo_course_site_sections import declarations, full_projection
    results={}
    section_builds={}
    for page,text in native.items():
        c.PAGE=page;items=c.catalog()
        sections=declarations(ROOT/page.with_suffix('.qmd'), ROOT)
        key=next((k for k,v in c.PAGES.items() if v==page),None)
        if key=='home':result=b.home(items)
        elif key in c.KEYS:
            doc,notes=prepare_reader(BeautifulSoup(text,'html.parser'),key)
            c.FRESH[key]=str(doc)
            item=next(p for p in items if p['id']==key)
            result,record=b.reader(item,items,sections)
            result=c.finish(result,page)
            target=BeautifulSoup(result,'html.parser').select_one('.reader-content')
            from zo_course_labels import governed, omit_reader_context_labels
            if governed(page) and omit_reader_context_labels(target):
                if target.select_one('[data-reading-label]'):
                    raise ValueError(f'{key}: generated reader still contains context labels')
            assert fingerprint(target)==fingerprint(doc.select_one('.reader-content')),key+' native-to-r20 projection drift'
            record.update(source=str(page.with_suffix('.qmd')),source_sha256=sha(ROOT/page.with_suffix('.qmd')),lifecycle_notes_replaced=notes,review_rounds_closed=len(target.select('#on-lai details.r01-review-round:not([open])')))
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
        finished=c.finish(result,page)
        results[page],section_builds[page.as_posix()]=full_projection(finished,sections,c.OUT/page)
    if c.PAGES['home'].with_suffix('.qmd') in selected:
        c.PAGE=c.PAGES['home'];items=c.catalog()
        for name,html in [('chuyen-de.html',b.topics(items)),('da-luu.html',b.saved(items)),('cach-hoc.html',b.guide())]:results[c.HOME/name]=c.finish(html,c.HOME/name)
        for g in b.GUIDES:results[c.HOME/g['file']]=c.finish(b.detailed_guide(g,items),c.HOME/g['file'])
    for page in results.keys()-native.keys():
        sections=declarations(ROOT/c.PAGES['home'].with_suffix('.qmd'), ROOT, output=page.name)
        results[page],section_builds[page.as_posix()]=full_projection(results[page],sections,c.OUT/page)
    for page,text in results.items():
        dest=c.OUT/page;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text,'utf-8')
    # Download products come from the canonical package, independently of
    # whether Quarto's per-article resource list happens to copy each variant.
    import yaml
    for key,page in c.PAGES.items():
        if key=='home' or page.with_suffix('.qmd') not in selected:continue
        config=ROOT/page.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml'
        variants=yaml.safe_load(config.read_text('utf-8')).get('extensions',{}).get('pdf_variants',{}) if config.is_file() else {}
        names=['index.pdf'] if key=='d0' else [v['output'] for v in variants.values()]
        for name in names:
            src=ROOT/page.parent/name;dest=c.OUT/page.parent/name
            if not src.is_file():raise ValueError('Missing canonical PDF download: '+str(src))
            if not dest.is_file() or sha(src)!=sha(dest):shutil.copyfile(src,dest)
    from zo_course_site_output import normalize_lines
    normalized_lines=normalize_lines(ROOT,c.OUT,[c.OUT/p for p in results])
    check=local_check([c.OUT/p for p in results])
    # Prune only after a complete build has valid final pages. A partial
    # render must not retire assets of a page it did not regenerate.
    removed=[]
    if not check['failures'] and len(selected)==len(c.PAGES)+1:
        from zo_course_site_output import prune
        removed=prune(ROOT,c.OUT,[c.OUT/p for p in results])
    data={'built_at':datetime.now(timezone.utc).isoformat(),'root':str(ROOT),'source_mode':'fresh native QMD after existing source and render validators','sources':{p.as_posix():sha(ROOT/p) for p in selected},'outputs':{p.as_posix():sha(c.OUT/p) for p in results},'packages':records,'local_links':check,'retired_generated_assets':removed,'normalized_text_line_endings':normalized_lines,'PDF_built':False,'published':False,'owner_acceptance':False}
    out=Path(report).with_name(Path(report).stem+'-site.json') if report else ROOT/'_audit/course_site_build.json'
    if not out.is_absolute():out=ROOT/out
    save(out,data)
    if check['failures']:raise ValueError('Course site check failed: '+str(check['failures'][:20]))
    from zo_pdf_variant_state import refresh_current
    for source in selected:
        refresh_current(ROOT, ROOT / source)
    prior=json.loads(CURRENT.read_text('utf-8')) if CURRENT.is_file() else {}
    combined=dict(prior.get('outputs',{}),**data['outputs'])
    # All declared sources must have final HTML, never a native/intermediate page.
    complete=all((c.OUT/p).is_file() and 'data-zo-course-site=' in (c.OUT/p).read_text('utf-8') for p in [*c.PAGES.values(),c.FOUNDATION])
    record=dict(data,inputs=live_inputs(),catalog_metadata=catalog_metadata(),outputs=combined,assets={p.relative_to(c.OUT).as_posix():sha(p) for p in c.ASSETS.rglob('*') if p.is_file()},complete=complete)
    record['section_builds']={**prior.get('section_builds',{}),**section_builds}
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
def validate_native_view_inputs(source, key, mirror, native_path):
    from zo_course_editorial import closure

    inputs = [*closure(ROOT / source, ROOT), ROOT / source.parent / 'giao_dien/html.json',
              ROOT / source.parent / 'giao_dien/he_nhan.json']
    if key in {'r1_g01', 'r1_g02'}:
        # Quarto runs these package adapters inside the isolated copy, before
        # the current course site builder receives their rendered HTML.
        inputs.extend(ROOT / name for name in (
            '_quarto.yml', '_quarto-on-thi-preview.yml',
            'scripts/zo_web_2027_production.py',
            f'scripts/zo_web_2027_{key.removeprefix("r1_")}_revision.py',
            'scripts/zo_r1_g01_labels.py',
        ))
    if key == 'r1_g02':
        inputs.append(ROOT / 'scripts/zo_g02_revision_downloads.py')
    generated_at = native_path.stat().st_mtime_ns
    for path in inputs:
        relative = path.relative_to(ROOT)
        staged = mirror / relative
        if not staged.is_file() or sha(staged) != sha(path):
            raise ValueError(f'Isolated build input differs: {relative.as_posix()}. '
                             'Build again from current canonical inputs.')
        if staged.stat().st_mtime_ns > generated_at:
            raise ValueError(f'Isolated native HTML predates its input: {relative.as_posix()}. '
                             'Render this view again from current canonical inputs.')


def native_view_projection(source, view, native_input, related=()):
    """Prepare a course view from an isolated native HTML render of this source."""
    from zo_course_site_sections import Locations, declarations, project, render, replace_view_outline
    from zo_course_site_sources import build as b
    from zo_course_solution_prompts import project_solution_prompts

    page=source.with_suffix('.html')
    key=next((key for key, path in c.PAGES.items() if path==page), None)
    native_path=(ROOT/native_input).resolve()
    ancestors=[p for p in native_path.parents if p.name=='docs']
    if (key not in c.KEYS or view not in {'bai-hoc', 'phieu-luyen', 'tu-kiem-tra', 'on-lai', 'on-nen', 'sua-loi', 'loi-giai', 'nhat-ky', 'tai-tai-lieu'} or not native_path.is_relative_to(ROOT/'.quarto')
            or not ancestors or native_path.relative_to(ancestors[0])!=page):
        raise ValueError('Expected the matching view HTML from an isolated Quarto build')
    validate_native_view_inputs(source, key, ancestors[0].parent, native_path)
    raw=native_path.read_text(encoding='utf-8')
    if 'data-zo-course-site=' in raw:
        raise ValueError('Expected native HTML before course shell projection')
    doc,_=prepare_reader(BeautifulSoup(raw,'html.parser'),key)
    c.FRESH[key]=str(doc)
    c.PAGE=page
    items=c.catalog()
    item=next(p for p in items if p['id']==key)
    sections = declarations(ROOT / source, ROOT)
    result,_=b.reader(item,items,sections)
    result = c.finish(result, page)
    if view == 'sua-loi':
        intro = sections.get('cach-thuc-hien-sua-loi')
        if intro is not None:
            result = project(result, {intro.target: render(intro)}, c.OUT / page)[0]
    result = project_solution_prompts(result)
    fragments = {target: result[start:end]
                 for target, (start, end) in Locations(result, [view, *related]).spans.items()}
    reader = doc.select_one('.reader-content')
    update_outline = view == 'loi-giai' or (view == 'sua-loi' and
                                           reader.select_one('#sua-loi [data-zo-remediation-chooser]'))
    outline = (next(entry for entry in json.loads(reader['data-zo-contents']) if entry['view'] == view)
               if update_outline else None)
    assessment_gate = view == 'tu-kiem-tra' and reader.select_one('#tu-kiem-tra .zo-post-test-review')
    app_script = re.compile(r'<script\b[^>]*\bsrc="([^"]*/app(?:\.[0-9a-f]{16})?\.js)"')
    runtime = app_script.search(result)[1] if assessment_gate else None

    def project_view(selected, before):
        if selected != page:
            return before
        updated = project(before, fragments, c.OUT/page)[0]
        if runtime:
            binding = app_script.search(updated)
            if binding is None:
                raise ValueError('The assessment gate needs the current reader script binding')
            start, end = binding.span(1)
            updated = updated[:start] + runtime + updated[end:]
        return replace_view_outline(updated, outline) if outline else updated

    project_view.runtime = (c.OUT / page.parent / runtime).resolve() if runtime else None
    return project_view

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['build','check','plan','assets']);parser.add_argument('--report');parser.add_argument('--page',action='append',default=[]);parser.add_argument('--all',action='store_true',help='Explicit full-course build')
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--section',action='append',default=[],help='QMD section ID; repeat for multiple regions')
    mode.add_argument('--changed-sections',action='store_true',help='Find changed declared sections and their consumers')
    native = parser.add_mutually_exclusive_group()
    native.add_argument('--native-lesson-input', type=Path, help='Import Bài học from a matching isolated native render')
    native.add_argument('--native-practice-input', type=Path, help='Import Luyện tập from a matching isolated native render')
    native.add_argument('--native-test-input', type=Path, help='Import Kiểm tra from a matching isolated native render')
    native.add_argument('--native-review-input', type=Path, help='Import Ôn lại from a matching isolated native render')
    native.add_argument('--native-foundation-input', type=Path, help='Import Ôn nền from a matching isolated native render')
    native.add_argument('--native-remediation-input', type=Path, help='Import Sửa lỗi from a matching isolated native render')
    native.add_argument('--native-solution-input', type=Path, help='Import Lời giải from a matching isolated native render')
    native.add_argument('--native-journal-input', type=Path, help='Import Nhật kí from a matching isolated native render')
    native.add_argument('--native-download-input', type=Path, help='Import Tải PDF from a matching isolated native render')
    parser.add_argument('--native-related', action='append', default=[], metavar='ID',
                        help='Import an additional disjoint HTML region from the same native render')
    parser.add_argument('--preserve-html-baseline', metavar='SHA256',
                        help='For a hierarchy-only native Sửa lỗi build, keep an inspected current HTML baseline')
    mode.add_argument('--reader-catalog',action='store_true',help='Refresh only the configured course switcher and its data')
    mode.add_argument('--reader-nav-labels', action='store_true', help='Refresh shared navigation and full-text labels on all course reader pages')
    mode.add_argument('--presence-copy',action='store_true',help='Refresh only the shared QR dialog script')
    args=parser.parse_args(argv)
    native_views = {
        'bai-hoc': args.native_lesson_input,
        'phieu-luyen': args.native_practice_input,
        'tu-kiem-tra': args.native_test_input,
        'on-lai': args.native_review_input,
        'on-nen': args.native_foundation_input,
        'sua-loi': args.native_remediation_input,
        'loi-giai': args.native_solution_input,
        'nhat-ky': args.native_journal_input,
        'tai-tai-lieu': args.native_download_input,
    }
    native_view, native_input = next(
        ((view, path) for view, path in native_views.items() if path is not None),
        (None, None),
    )
    if args.native_related and not native_input:
        parser.error('--native-related requires a native view input')
    if args.preserve_html_baseline and (args.command != 'build' or native_view != 'sua-loi'
                                      or len(args.page) != 1 or args.native_related or not args.section):
        parser.error('--preserve-html-baseline requires one native Sửa lỗi section build without related sections')
    if args.reader_nav_labels:
        if args.command != 'build' or args.page or args.all or native_input:
            parser.error('Reader group labels require build without a page or native input')
        from zo_course_site_assets import refresh_reader_nav_labels
        try:
            refresh_reader_nav_labels(sys.modules[__name__], args.report or '_audit/course_reader_nav_labels.json')
        except (OSError, ValueError) as exc:
            parser.exit(1,str(exc)+'\n')
        return 0
    if args.presence_copy:
        if args.command!='assets' or args.page or args.all or native_input:
            parser.error('Shared QR dialog refresh requires assets without a page or native input')
        from zo_course_site_assets import refresh_presence_copy
        refresh_presence_copy(sys.modules[__name__], args.report or '_audit/course_presence_copy.json')
        return 0
    if args.reader_catalog:
        pages=relevant(args.page)
        if args.command!='build' or args.all or len(args.page)!=1 or len(pages)!=1:
            parser.error('Reader catalog refresh requires build and exactly one canonical reader page')
        from zo_course_site_assets import refresh_reader_catalog
        print(json.dumps(refresh_reader_catalog(sys.modules[__name__],pages[0]),ensure_ascii=False))
        return 0
    if native_input and (args.command!='build' or len(args.page)!=1 or not args.section):
        parser.error('A native view input needs build, one --page and explicit section fragments')
    if args.command=='assets' and args.section:
        pages=relevant(args.page)
        if args.all or len(args.section)!=1 or len(pages)!=len(args.page) or len(pages)>1:
            parser.error('A stylesheet refresh needs one --section and at most one canonical --page')
        from zo_course_site_assets import refresh_style_section
        try:
            refresh_style_section(sys.modules[__name__], args.report or '_audit/course_style_section.json',
                                  args.section[0], pages[0] if pages else None)
        except (OSError,ValueError) as exc:
            parser.exit(1,str(exc)+'\n')
        return 0
    if args.section or args.changed_sections:
        if args.all or args.command not in {'build','plan'}:
            parser.error('Section scope requires build or plan without --all')
        pages=relevant(args.page)
        if len(pages)!=len(args.page):
            parser.error('Use canonical course QMD paths')
        report=(ROOT/(args.report or '_audit/course_section_build.json')).resolve()
        if not report.is_relative_to(ROOT/'_audit'):
            parser.error('Section reports belong under _audit')
        from zo_course_site_sections import build_sections
        try:
            prepare=native_view_projection(pages[0],native_view,native_input,args.native_related) if native_input else None
            result=build_sections(pages,args.section,CURRENT,report,plan=args.command=='plan',
                                  prepare=prepare,native_view=native_view if prepare else None,
                                  preserved_baseline=(pages[0].with_suffix('.html'), args.preserve_html_baseline)
                                  if args.preserve_html_baseline else None)
        except (OSError,ValueError) as exc:
            parser.exit(1,str(exc)+'\n')
        print(json.dumps(result,ensure_ascii=False))
        return 0
    args.report=args.report or '_audit/course_site_build.json'
    if args.command=='assets':
        from zo_course_site_assets import apply
        return apply(sys.modules[__name__], args.report)
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
