"""G02 audit-only figure/download payloads using the frozen approved G01 styles.

Does not update production HTML, G01 assets, or learning PDFs.
"""
from pathlib import Path
import copy
import json
import shutil
import sys
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from pypdf import PdfReader
from zo_web_2027_figures import module, sha, GRAPH, VARIATION, PROFILE, ROOT

PACKAGE = ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02'
CONFIG=PACKAGE/'giao_dien/web_2027_figures.json'

def vector_dependencies():
    config=json.loads(CONFIG.read_text(encoding='utf-8'))
    paths=[CONFIG,Path(__file__),ROOT/'scripts/zo_course_cover_assets.py',GRAPH/'axis_ticks.py',GRAPH/'zo_graph_build.py',GRAPH/'tex/zo_graph_v02.tex',
           GRAPH/'tex/zo_graph_v04.tex',GRAPH/'profiles/lesson-g03.json',PROFILE/'frame-tokens.json',PROFILE/'production-figures.css',
           ROOT/'_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/design/color_system.json']
    paths += [PACKAGE/item['source'] for item in config['figures']]
    paths += list((ROOT/'assets/fonts').glob('STIXTwo*.otf'))
    return {p.relative_to(ROOT).as_posix():sha(p) for p in paths}

def build_vectors(output):
    """Reuse only complete verified pairs; otherwise build from canonical TeX."""
    cache=PACKAGE/'giao_dien/assets/figures_0_4'
    manifest=cache/'manifest.json'
    if manifest.is_file():
        receipt=json.loads(manifest.read_text(encoding='utf-8'))
        if receipt['inputs']==vector_dependencies() and all((cache/n).is_file() and sha(cache/n)==h for n,h in receipt['assets'].items()):
            expected={n+ext for n in ['do_thi_01','do_thi_02','nen_do_thi_01','nen_do_thi_02'] for ext in ['.svg','.pdf']}|{'cover-light.svg'}
            if set(receipt['assets'])==expected:
                dest=output/'assets/figures04';dest.mkdir(parents=True,exist_ok=True)
                for name in receipt['assets']:shutil.copyfile(cache/name,dest/name)
                (dest/'manifest.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                return receipt
    graph = module('g02_graph04', GRAPH/'zo_graph_build.py')
    destination = output/'assets/figures04'
    destination.mkdir(parents=True,exist_ok=True)
    sources = [PACKAGE/'hinh'/f'{name}.tex' for name in ['do_thi_01','do_thi_02','nen_do_thi_01','nen_do_thi_02']]
    inputs = vector_dependencies()
    for source in sources:
        print('G02 vector',source.stem,flush=True)
        pdf,svg = graph.build(graph.parse_args([str(source),'--style','0.4','--layout','lesson-g03','--check','--force','--out-dir',str(output/'figure-build')]))
        shutil.copyfile(svg,destination/svg.name)
        shutil.copyfile(pdf,destination/pdf.name)
    # Representative G02 image: L02, endpoint comparison and a corner minimum.
    # Transparent artwork; background belongs to the independent cover frame.
    old=json.loads(manifest.read_text(encoding='utf-8'))
    keys=[(GRAPH/f).relative_to(ROOT).as_posix() for f in ['tex/zo_graph_v02.tex','tex/zo_graph_v04.tex']]
    keys += [(PACKAGE/'giao_dien/cover_g02.tex').relative_to(ROOT).as_posix()]
    keys += [k for k in inputs if k.startswith('assets/fonts/')]
    if sha(cache/'cover-light.svg')!=old['assets']['cover-light.svg']:raise ValueError('Approved cover bytes changed')
    if any(old['inputs'].get(k)!=inputs[k] for k in keys):
        from zo_course_cover_assets import verify_rebuild
        verify_rebuild(ROOT,PACKAGE/'giao_dien/cover_g02.tex','transparent-light',cache/'cover-light.svg')
    shutil.copyfile(cache/'cover-light.svg',destination/'cover-light.svg')
    if inputs!=vector_dependencies():raise ValueError('G02 vector inputs changed during build')
    expected={p.stem+ext for p in sources for ext in ['.svg','.pdf']}|{'cover-light.svg'}
    assets={p.name:sha(p) for p in destination.iterdir() if p.suffix in ['.svg','.pdf']}
    if set(assets)!=expected:raise ValueError('Incomplete G02 vector build')
    receipt={'profile':'0.4','inputs':inputs,'assets':assets,'cover_surface':'transparent-light',
             'fresh_all_five':False,'learning_pdf_built':False,'canonical_cache_used':False,
             'lesson_layout':'lesson-g03','preserved_cover_origin':old.get('preserved_cover_origin',old)}
    (destination/'manifest.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    cache.mkdir(parents=True,exist_ok=True)
    for name in assets:shutil.copyfile(destination/name,cache/name)
    shutil.copyfile(destination/'manifest.json',manifest)
    return receipt

def verify_print():
    cache=PACKAGE/'giao_dien/assets/figures_0_4'
    receipt=json.loads((cache/'manifest.json').read_text(encoding='utf-8'))
    expected={n+ext for n in ['do_thi_01','do_thi_02','nen_do_thi_01','nen_do_thi_02'] for ext in ['.svg','.pdf']}|{'cover-light.svg'}
    if receipt['inputs']!=vector_dependencies() or set(receipt['assets'])!=expected or not all((cache/n).is_file() and sha(cache/n)==h for n,h in receipt['assets'].items()):
        raise ValueError('G02 current paired figures missing or stale: regenerate before any book PDF render.')
    return cache,receipt

def apply(page,output, *, document=None):
    doc=document if document is not None else BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    doc.body['class']=doc.body.get('class',[])+['zo-web-2027-production']
    # The opt-in class selects frozen styles; the visible trial label remains.
    css=PROFILE/'production-figures.css'
    shutil.copyfile(css,output/css.name)
    doc.head.append(doc.new_tag('link',rel='stylesheet',href=css.name))
    for image in doc.select('.reader-content .figure-viewport img'):
        name=Path(image['src']).name.split('_',1)[-1]
        if name not in ['do_thi_01.svg','do_thi_02.svg','nen_do_thi_01.svg','nen_do_thi_02.svg']:continue
        image['src']='assets/figures04/'+name
        from zo_graphics import set_lesson_graph_size
        set_lesson_graph_size(image,output/'assets/figures04'/name,ROOT)
        image['class']+=['zo-graph-04']
        image.parent['class']+=['zo-figure-scroll']
    sys.path.insert(0,str(VARIATION))
    variation=module('g02_variation04',VARIATION/'zo_variation_html.py')
    records=variation.load_data(PACKAGE/'du_lieu/bang_bien_thien.json')
    by_id={r['id']:r for r in records};fragments=variation.math_fragments(records)
    seen=[]
    for figure in doc.select('.reader-content figure.zo-variation-asset[data-bbt]'):
        rid=figure['data-bbt'];seen.append(rid)
        record=by_id[rid]
        original=figure.select_one('table.variation')
        rows=[[cell.get_text(' ',strip=True) for cell in row.find_all(['td','th'],recursive=False)] for row in original.find_all('tr')]
        if rows!=record['rows']:raise ValueError('BBT data drift: '+rid)
        caption=figure.select_one('figcaption')
        native=BeautifulSoup(variation.render_record(record,fragments),'html.parser').select_one('table')
        native.caption.string=caption.get_text(' ',strip=True)
        viewport=figure.select_one('.figure-viewport')
        if viewport is None:
            viewport=doc.new_tag('div',attrs={'class':'figure-viewport'})
            for child in list(figure.contents):viewport.append(child.extract())
            figure.append(viewport)
        old_image=viewport.select_one('img')
        if old_image:old_image.decompose()
        figure.select_one('.visually-hidden').decompose()
        if caption.parent is viewport:caption.insert_before(native)
        else:viewport.append(native)
        viewport['class']+=['zo-figure-scroll']
    if set(seen)!=set(by_id):raise ValueError('Missing G02 BBT')
    image=doc.select_one('.hero-art img')
    image['src']='assets/figures04/cover-light.svg'
    image['alt']='Minh họa từ nhiệm vụ về giá trị lớn nhất và giá trị nhỏ nhất: g(x)=|x+2| trên [-4;1], nhỏ nhất tại điểm gãy và lớn nhất tại đầu mút'
    frame=doc.new_tag('div',attrs={'class':'zo-cover-frame','style':'--frame-width:420px;--frame-ratio:1/1;--frame-bg:#FFFBE8'})
    image.wrap(frame)
    section=doc.select_one('#tai-tai-lieu')
    cards=section.select('.r1-download-card,.r1-section-download-item')
    if len(cards)!=8:raise ValueError('Expected eight G02 PDF files')
    downloads=[]
    for card in cards:
        link=card.select_one('a[download]')
        title=card.select_one('h3,.r1-section-download-title')
        description=card.select_one('.r1-section-download-description') or card.select_one('p:not(.r1-download-card__meta)')
        if not all([link,title,description]):raise ValueError('Incomplete G02 download card')
        pdf=(output/unquote(urlsplit(link['href']).path)).resolve()
        if pdf.name!=Path(unquote(urlsplit(link.get('data-canonical-href',link['href'])).path)).name:
            raise ValueError('Download target identity changed')
        pages=len(PdfReader(pdf).pages)
        text=doc.new_tag('div',attrs={'class':'zo-pdf-copy'})
        title=copy.deepcopy(title);title['class']=title.get('class',[])+['zo-pdf-title']
        description=copy.deepcopy(description);description['class']=description.get('class',[])+['zo-pdf-description']
        text.extend([title,description])
        status=doc.new_tag('small',attrs={'class':'zo-pdf-version-note'})
        status.string='Bản PDF chưa đồng bộ với HTML này.'
        text.append(status)
        metric=doc.new_tag('div',attrs={'class':'zo-pdf-pages','data-pdf-pages':str(pages)})
        number=doc.new_tag('strong');number.string=str(pages)
        unit=doc.new_tag('span');unit.string='trang';metric.extend([number,unit])
        link=copy.deepcopy(link);link['class']=['zo-pdf-download__link','zo-pdf-download'];link['aria-label']='Tải PDF: '+title.get_text(' ',strip=True)
        link.clear();icon=doc.new_tag('svg',attrs={'viewBox':'0 0 24 24','aria-hidden':'true','focusable':'false'})
        icon.append(doc.new_tag('path',attrs={'d':'M12 3v12m-4-4 4 4 4-4M5 16v5h14v-5','fill':'none','stroke':'currentColor','stroke-width':'1.7','stroke-linecap':'round','stroke-linejoin':'round'}))
        link.extend([icon,'Tải PDF'])
        card.clear();card['class']=card.get('class',[])+['zo-pdf-card'];card.extend([text,metric,link])
        downloads.append({'file':pdf.name,'pages':pages,'sha256':sha(pdf)})
    note=doc.new_tag('p',attrs={'class':'zo-pdf-current-note'})
    note.string='Số trang được đọc từ các tệp PDF đang có. Các PDF này chưa được đồng bộ với nội dung HTML mới; chưa phải bộ PDF để xuất bản.'
    paper=section.select_one('.reading-region');paper.select_one('h2').insert_after(note)
    css=ROOT/'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/giao_dien/downloads.css'
    shutil.copyfile(css,output/'downloads.css');doc.head.append(doc.new_tag('link',rel='stylesheet',href='downloads.css'))
    trigger=doc.select_one('.mobile-trigger');trigger['aria-label']='Mở mục lục học liệu';trigger['title']='Mở mục lục học liệu'
    icon=trigger.select_one('[aria-hidden=true]');icon.clear()
    svg=doc.new_tag('svg',attrs={'viewBox':'0 0 24 24','aria-hidden':'true','focusable':'false'})
    svg.append(doc.new_tag('path',attrs={'d':'M5 6h14M5 12h14M5 18h14','fill':'none','stroke':'currentColor','stroke-width':'1.7','stroke-linecap':'round'}));icon.append(svg)
    shutil.copyfile(PACKAGE/'giao_dien/support-context.js',output/'support-context.js')
    doc.body.append(doc.new_tag('script',src='support-context.js'))
    if document is None:
        page.write_text(str(doc),encoding='utf-8')
    return {'bbt':seen,'downloads':downloads,'styles_reused_without_changes':[css.relative_to(ROOT).as_posix(),(PROFILE/'production-figures.css').relative_to(ROOT).as_posix()]}
