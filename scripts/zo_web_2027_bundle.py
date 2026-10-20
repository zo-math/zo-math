"""Build one coherent registered-page preview from current sources, never old HTML.

Run through zo_python.py. Official renders remain independent of _audit;
the isolated mirror is merely an output destination. No publish or Git writes.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit
import argparse
import json
import os
import re
import shutil
import sys
import subprocess

sys.dont_write_bytecode = True
import zo_web_2027_cluster_check as cluster
from bs4 import BeautifulSoup
from zo_web_2027_preview import sha

ROOT = Path(__file__).resolve().parents[1]
PAGES = {k:v for k,v in cluster.PAGES.items() if k != 'gateway'}
INPUTS = ['scripts', 'assets', 'content/thpt/on_thi_toan_thpt',
          '_design/web_2027_mau_dung_chung',
          '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac']
EXTENSIONS = {'.py','.qmd','.yml','.yaml','.json','.css','.js','.lua','.tex',
              '.pdf','.svg','.png','.jpg','.jpeg','.ttf','.woff','.woff2','.scss'}


def sources():
    result = {}
    for folder in INPUTS:
        for p in (ROOT/folder).rglob('*'):
            if p.name in {'ban_dang_duyet.json','ho_so_dong_bo_sau_bang_20261019.json'}:continue
            if p.is_file() and p.suffix in EXTENSIONS and not any(x in p.parts for x in ['__pycache__','.quarto']):
                result[p.relative_to(ROOT).as_posix()] = sha(p)
    for p in ROOT.glob('_quarto*.yml'):
        result[p.name] = sha(p)
    for p in (ROOT/'content').glob('*.qmd'):
        result[p.relative_to(ROOT).as_posix()] = sha(p)
    return result


def require_fresh(manifest, current=None):
    if manifest['sources'] != (sources() if current is None else current):
        raise ValueError('Bundle is stale: rebuild all registered pages from current sources')


def checks(out):
    manifest = json.loads((out/'bundle.json').read_text(encoding='utf-8'))
    require_fresh(manifest)
    values = {'all source fingerprints current': True}
    preview = out/'html-current'
    expected = {key:(preview/(key+'-reading.html')).resolve() for key in PAGES}
    for key, page in expected.items():
        doc = BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        if key.startswith('g'):
            import yaml
            from pypdf import PdfReader
            from zo_pdf_contract import validate_canonical_pdf_provenance
            source=ROOT/PAGES[key].with_suffix('.qmd')
            metadata=yaml.safe_load(source.read_text(encoding='utf-8').split('---',2)[1])
            specs=metadata['r1-download-files']+metadata['r1-section-download-files']
            by_name={spec['href']:spec for spec in specs}
            config=yaml.safe_load((source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text(encoding='utf-8'))
            variants={item['output']:name for name,item in config['extensions']['pdf_variants'].items()}
            cards=doc.select('#tai-tai-lieu .zo-pdf-card')
            card_names=[Path(unquote(urlsplit(card.select_one('a[download]')['href']).path)).name for card in cards]
            values[key+' exactly eight registered PDF cards']=len(card_names)==8 and set(card_names)==set(variants)==set(by_name)
            download_section=doc.select_one('#tai-tai-lieu')
            values[key+' PDF utility section exists']=download_section is not None
            from zo_web_2027_downloads import download_region_coverage
            values[key+' PDF cards retain reading regions']=download_region_coverage(download_section)
            download_text=download_section.get_text(' ',strip=True) if download_section is not None else ''
            values[key+' no obsolete PDF-state notice']=all(s not in download_text for s in ['chưa được đồng bộ','đang chờ cập nhật'])
            for card,name in zip(cards,card_names):
                link=card.select_one('a[download]');spec=by_name[name]
                target=(page.parent/unquote(urlsplit(link['href']).path)).resolve()
                original=source.parent/name
                count=len(PdfReader(original).pages)
                text=' '.join(card.get_text(' ',strip=True).split())
                values[key+' current PDF '+name]=card.get('data-pdf-current')=='true' and not validate_canonical_pdf_provenance(ROOT,source,variant=variants[name])
                values[key+' exact PDF bytes '+name]=target.is_file() and sha(target)==sha(original)
                values[key+' download metadata '+name]=link['download']==spec['download'] and spec['title'] in text and spec['description'] in text and f'{count} trang' in text and ('pages' not in spec or spec['pages']==count)
        if key=='d0':
            package=ROOT/PAGES[key].parent
            receipt=json.loads((package/'_quy_trinh/pdf_build.json').read_text('utf-8'))
            values['d0 current custom PDF receipt']=receipt['output_sha256']==sha(package/'index.pdf') and all((ROOT/rel).is_file() and sha(ROOT/rel)==digest for rel,digest in receipt['inputs_sha256'].items())
            links=[n for n in doc.select('a[href]') if Path(unquote(urlsplit(n['href']).path)).name=='index.pdf']
            values['d0 current PDF download exists']=bool(links)
            for n in links:
                target=(page.parent/unquote(urlsplit(n['href']).path)).resolve()
                values['d0 exact PDF download '+n['href']]=target.is_file() and sha(target)==sha(package/'index.pdf')
        values[key+' generated HTML uses LF without trailing whitespace'] = b'\r' not in page.read_bytes() and not any(line.endswith((b' ',b'\t')) for line in page.read_bytes().splitlines())
        values[key+' footer provenance uses public HTML destinations'] = not any('.qmd' in n.get('data-canonical-href','') for n in doc.select('footer a'))
        values[key+' HTML matches manifest'] = sha(page)==manifest['pages'][key]['html_sha256']
        for link in doc.select('.course-panel [data-course-page]'):
            target = (page.parent/unquote(urlsplit(link['href']).path)).resolve()
            values[key+' current menu '+link['data-course-page']] = target == expected[link['data-course-page']]
        for link in doc.select('a[href]'):
            url = urlsplit(link['href'])
            if not url.scheme and not url.netloc and url.path:
                target = (page.parent/unquote(url.path)).resolve()
                if any('/'+str(p).replace('\\','/') in target.as_posix() for p in PAGES.values()):
                    values[key+' no old course HTML '+link['href']] = target in expected.values()
                if target.name in {p.name for p in expected.values()}:
                    values[key+' no old preview HTML '+link['href']] = target in expected.values()
        values[key+' assets exist'] = all((page.parent/unquote(urlsplit(n.get('src',n.get('href'))).path)).resolve().is_file()
            for n in doc.select('img[src],script[src],link[rel=stylesheet][href]')
            if not urlsplit(n.get('src',n.get('href'))).scheme)
    home = BeautifulSoup(expected['home'].read_text(encoding='utf-8'),'html.parser')
    from zo_course_cover import load_cover
    for card in home.select('.home-card[data-package-id]'):
        package=card['data-package-id'];cover=load_cover(ROOT,package,allow_direction_approved=package in {'d0','r1_g05'})
        actual=(expected['home'].parent/unquote(urlsplit(card.img['src']).path)).resolve()
        values['Home declared cover '+package]=actual.is_file() and sha(actual)==sha(cover)
    for key,page in expected.items():
        doc=BeautifulSoup(page.read_text('utf-8'),'html.parser')
        links=doc.select('.rail-support')
        values[key+' sidebar support opens canonical information page']=len(links)==1 and urlsplit(links[0].get('href','')).path.endswith('/content/support/donate.html') and not urlsplit(links[0].get('href','')).fragment

    from copy import deepcopy
    from zo_web_2027_check import complete_site_footer
    from zo_web_2027_preview import footer_data
    broken_footer = deepcopy(home)
    broken_footer.select_one('footer#site-footer nav a')['data-canonical-href'] = '/wrong-destination.html'
    values['negative wrong footer destination rejected'] = not complete_site_footer(broken_footer, footer_data())
    images = home.select('.home-journey img')
    values['one approved cover without mobile replacement'] = len(images)==1 and images[0]['src'].endswith('hanh_trinh_nguoi_hoc_toan_3x4.png') and not home.select('.journey-square')
    css = (ROOT/'_design/web_2027_mau_dung_chung/course-home-landing.css').read_text(encoding='utf-8')
    values['cover never hidden on mobile'] = '.journey-portrait{display:none}' not in css
    for relative,digest in manifest.get('asset_sha256',{}).items():
        asset=out/relative
        values['bundled asset '+relative] = asset.is_file() and sha(asset)==digest
    from zo_web_2027_home_landing_check import static
    home_values, missing = static(expected['home'], json.loads((out/'build.json').read_text(encoding='utf-8')))
    values.update({'Home/'+k:v for k,v in home_values.items()})
    values['no missing Home links'] = not missing
    try:
        require_fresh(manifest, dict(manifest['sources'], **{'injected-stale-source':'bad'}))
    except ValueError:
        values['negative stale source rejected'] = True
    else:
        values['negative stale source rejected'] = False
    report = {'checks':values,'passed':sum(values.values()),'total':len(values),
              'failures':[k for k,v in values.items() if not v], 'missing_links':missing,
              'browser_checked':False,'published':False}
    cluster.save(out/'bundle-qa.json',report)
    print(json.dumps({k:report[k] for k in ['passed','total','failures','missing_links']},ensure_ascii=False))
    return int(bool(report['failures']))


def prune_delivery(out):
    """Retain only the assets reached by the six preview documents."""
    delivery = (out/'delivery/docs').resolve()
    queue = list((out/'html-current').glob('*.html')) + ([out/'index.html'] if (out/'index.html').is_file() else [])
    keep = set()
    seen = set()
    # Declared runtime assets include font licences and provenance resources;
    # they remain part of the build contract even without a DOM/CSS URL.
    report=json.loads((out/'build.json').read_text(encoding='utf-8'))
    for relative in report['resources']:
        asset=(delivery/'assets/zo_web_2027/home'/relative).resolve()
        if not asset.is_relative_to(delivery) or not asset.is_file():
            raise ValueError('Missing declared runtime asset: '+relative)
        keep.add(asset)
        queue.append(asset)
    from zo_html_dependencies import preview_files
    keep.update(p for p in preview_files(ROOT,queue) if p.is_relative_to(delivery))
    removed = 0
    for p in delivery.rglob('*'):
        if p.is_file() and p.resolve() not in keep:
            p.unlink();removed += 1
    for p in sorted(delivery.rglob('*'),key=lambda p:len(p.parts),reverse=True):
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    cluster.save(out/'cleanup.json',{'unused_delivery_files_removed':removed,'kept_files':len(keep)})


def adapt_bundle(out):
    # Adapt inside the isolated source project, so official input guards stay
    # active. Reading a historical outer _audit HTML into a production adapter
    # is intentionally forbidden; this adapter sees only its fresh docs output.
    mirror=cluster.render_mirror(out,'final')
    # The shared footer reads these canonical source pages, not older HTML.
    for p in (ROOT/'content').glob('*.qmd'):
        shutil.copyfile(p,mirror/'content'/p.name)
    # This command only builds named local review bundles. D0 has approval
    # for the cover direction, not acceptance of the finished image. The
    # adapter additionally requires its isolated .quarto source context.
    env=dict(os.environ,ZO_WEB_2027_HOME_REPORT=str(mirror/'_audit/home-build.json'),
             ZO_D0_COVER_PREVIEW='1')
    for key,path in PAGES.items():
        command=['python','scripts/zo_python.py','-B','scripts/zo_web_2027_production.py',
                 '--html',str(Path('docs')/path),'--output-root','docs']
        with (mirror/(key+'-adapt.log')).open('w',encoding='utf-8') as log:
            if subprocess.run(command,cwd=mirror,env=env,stdout=log,stderr=subprocess.STDOUT).returncode:
                raise RuntimeError(key+' canonical adapter failed: see '+str(log.name))
        print('Adapted',key,flush=True)
    shutil.copyfile(mirror/'_audit/home-build.json',out/'build.json')
    delivery=out/'delivery/docs'
    # Copy exactly the new six-page dependency closure, without accumulating
    # every unrelated Quarto resource and without deleting existing files.
    from zo_html_dependencies import preview_files
    required=preview_files(mirror,[mirror/'docs'/path for path in PAGES.values()])
    for relative in json.loads((out/'build.json').read_text('utf-8'))['resources']:
        required.add(mirror/'docs/assets/zo_web_2027/home'/relative)
    for source in required:
        relative=source.resolve().relative_to((mirror/'docs').resolve())
        target=delivery/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    preview=out/'html-current';preview.mkdir(exist_ok=True)
    mapping={(delivery/path).resolve():preview/(key+'-reading.html') for key,path in PAGES.items()}
    for key,path in PAGES.items():
        page=delivery/path
        doc=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        for n in doc.select('img[src],script[src],link[href],a[href]'):
            attr='src' if n.has_attr('src') else 'href';url=urlsplit(n[attr])
            if url.scheme or url.netloc or not url.path:
                continue
            target=(delivery/unquote(url.path).lstrip('/')).resolve() if url.path.startswith('/') else (page.parent/unquote(url.path)).resolve()
            destination=mapping.get(target,target)
            if not destination.is_file() and destination not in mapping.values() and target.is_relative_to(delivery):
                fallback=ROOT/'docs'/target.relative_to(delivery)
                if fallback.is_file():
                    destination=fallback
            n[attr]=urlunsplit(('', '',os.path.relpath(destination,preview).replace('\\','/'),url.query,url.fragment))
        from zo_course_html import write
        write(preview/(key+'-reading.html'), doc)


def review_hub(out):
    """Generate the review entrypoint together with the six-page bundle."""
    from html import escape
    import yaml
    names={'home':'Khóa 2027','d0':'Khảo sát đầu vào','g01':'Đơn điệu và cực trị','g02':'Giá trị lớn nhất và giá trị nhỏ nhất','g03':'Đường tiệm cận','g04':'Khảo sát sự biến thiên và vẽ đồ thị của hàm số'}
    sections=[]
    for key,path in PAGES.items():
        links=[];source=ROOT/path.with_suffix('.qmd')
        if key=='d0':files=[{'href':'index.pdf','title':'Bản PDF đầy đủ'}]
        elif key.startswith('g'):
            meta=yaml.safe_load(source.read_text('utf-8').split('---',2)[1])
            files=meta['r1-download-files']+meta['r1-section-download-files']
        else:files=[]
        for spec in files:
            target=out/'delivery/docs'/path.parent/spec['href']
            if not target.is_file():raise ValueError('Missing hub PDF: '+str(target))
            links.append('<li><a href="'+escape(target.relative_to(out).as_posix())+'">'+escape(spec['title'])+'</a></li>')
        sections.append('<section><h2><a href="html-current/'+key+'-reading.html">'+escape(names[key])+'</a></h2><ul>'+''.join(links)+'</ul></section>')
    text='<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Bản xem đồng bộ — ZO Math</title><style>body{font:18px/1.6 system-ui;max-width:1000px;margin:32px auto;padding:0 20px;background:#fffdf4;color:#333}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}section{background:white;border:1px solid #ddd;padding:20px;border-radius:12px}a{color:#a92828}h2{font-size:1.2em}</style><h1>Bản xem đồng bộ — ZO Math</h1><p>Sáu trang HTML và các bản PDF hiện hành. Đang chờ chủ biên duyệt; chưa xuất bản.</p><main>'+''.join(sections)+'</main></html>\n'
    (out/'index.html').write_text(text,'utf-8')


RECEIPT = Path('content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/ho_so_dong_bo_sau_bang_20261019.json')


def canonical_output(root=ROOT):
    import yaml
    root=Path(root).resolve()
    name=yaml.safe_load((root/'_quarto.yml').read_text('utf-8'))['project']['output-dir']
    out=(root/name).resolve()
    if out != root/'docs':
        raise ValueError('Course output must use the configured docs directory')
    return out


def install_current(produced, destination, paths, *, root=ROOT):
    """Replace generated files only after validation; restore on copy failure."""
    import tempfile
    root=Path(root).resolve();produced=Path(produced).resolve();destination=Path(destination).resolve()
    if destination != canonical_output(root) or not produced.is_relative_to(root/'.quarto'):
        raise ValueError('Install only freshly generated .quarto files into canonical docs')
    files={}
    for relative in paths:
        rel=Path(relative);source=(produced/rel).resolve();target=(destination/rel).resolve()
        if rel.is_absolute() or '..' in rel.parts or not source.is_relative_to(produced) or not target.is_relative_to(destination) or not source.is_file():
            raise ValueError('Unsafe or missing generated output: '+str(relative))
        if source.is_symlink() or any(x.is_symlink() for x in target.parents if x!=root):
            raise ValueError('Symlink in canonical output')
        files[rel]=sha(source)
    with tempfile.TemporaryDirectory(prefix='course-output-rollback-',dir=root/'.quarto') as backup:
        backup=Path(backup);previous={};written=[]
        try:
            for rel,digest in files.items():
                target=destination/rel;target.parent.mkdir(parents=True,exist_ok=True)
                previous[rel]=target.is_file()
                if previous[rel]:
                    saved=backup/rel;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(target,saved)
                written.append(rel);shutil.copyfile(produced/rel,target)
                if sha(target)!=digest:raise ValueError('Generated output copy differs: '+str(rel))
        except Exception:
            for rel in reversed(written):
                target=destination/rel
                if previous[rel]:shutil.copyfile(backup/rel,target)
                elif target.is_file():target.unlink()
            raise
    return {rel.as_posix():digest for rel,digest in files.items()}


def check_current(out, record=None):
    out=Path(out).resolve()
    if out!=canonical_output():raise ValueError('Check the canonical docs output')
    if record is None:
        record=json.loads((ROOT/RECEIPT).read_text('utf-8'))['canonical_html_build']
    require_fresh(record)
    if record.get('output_dir')!='docs':raise ValueError('Noncanonical course receipt')
    values={}
    for rel,digest in record['files'].items():
        target=(out/rel).resolve()
        values['current file '+rel]=target.is_relative_to(out) and target.is_file() and sha(target)==digest
    expected={key:(out/path).resolve() for key,path in PAGES.items()}
    for key,page in expected.items():
        doc=BeautifulSoup(page.read_text('utf-8'),'html.parser')
        values[key+' source-owned reader']=doc.select_one('.home-landing-content' if key=='home' else '.reader-content') is not None
        values[key+' exact page']=sha(page)==record['pages'][key]['html_sha256']
        for node in doc.select('img[src],script[src],link[href],a[href]'):
            href=node.get('src',node.get('href',''));u=urlsplit(href)
            if u.scheme or u.netloc or not u.path:continue
            target=(out/unquote(u.path).lstrip('/')).resolve() if u.path.startswith('/') else (page.parent/unquote(u.path)).resolve()
            if node.name!='a' or target.suffix=='.pdf' or node.has_attr('data-course-page') or 'rail-support' in node.get('class',[]):
                values[key+' resolved '+href]=target.is_file() and target.is_relative_to(out)
            values[key+' no audit '+href]='_audit' not in target.parts and not target.name.endswith('-reading.html')
        for node in doc.select('.course-panel [data-course-page]'):
            values[key+' canonical menu '+node['data-course-page']]=(page.parent/unquote(urlsplit(node['href']).path)).resolve()==expected[node['data-course-page']]
    from zo_html_dependencies import preview_files
    closure=preview_files(ROOT,expected.values())
    values['complete resource closure in docs']=all(p.is_relative_to(out) for p in closure)
    values['all registered pages declared']=set(record['pages'])==set(PAGES)
    failures=[k for k,v in values.items() if not v]
    if failures:raise ValueError('Canonical HTML verification failed: '+str(failures))
    return {'passed':len(values),'total':len(values),'failures':[],'output_dir':'docs','published':False}


def build(out, reports=None):
    import tempfile
    out=Path(out).resolve()
    if out!=canonical_output():
        raise ValueError('Build writes canonical docs; _audit is for reports, not course HTML')
    reports=Path(reports or ROOT/'_audit/current/verification/html-canonical-build').resolve()
    if not reports.is_relative_to(ROOT/'_audit'):raise ValueError('Reports belong in _audit')
    reports.mkdir(parents=True,exist_ok=True)
    from zo_web_2027_d0 import pdf_download
    from zo_pdf_contract import validate_canonical_pdf_provenance
    import yaml
    pdf_download(ROOT,Path('content/thpt/on_thi_toan_thpt/hoc_lieu/d0'),'index.pdf')
    for key,path in PAGES.items():
        if not key.startswith('g'):continue
        source=ROOT/path.with_suffix('.qmd')
        config=yaml.safe_load((source.parent/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text('utf-8'))
        for variant in config['extensions']['pdf_variants']:
            errors=validate_canonical_pdf_provenance(ROOT,source,variant=variant)
            if errors:raise ValueError(f'{key}/{variant} PDF is stale: '+str(errors))
    baseline=sources();cluster.PAGES=PAGES
    (ROOT/'.quarto').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='course-canonical-',dir=ROOT/'.quarto') as temp:
        stage=Path(temp)/'stage';stage.mkdir();mirror=cluster.render_mirror(stage,'final')
        try:
            cluster.render(stage,'final',html_only=True);adapt_bundle(stage)
            require_fresh({'sources':baseline})
            snapshot={'sources':baseline,'pages':{key:{'source':path.with_suffix('.qmd').as_posix(),'source_sha256':baseline[path.with_suffix('.qmd').as_posix()],'html_sha256':sha(stage/'html-current'/(key+'-reading.html'))} for key,path in PAGES.items()}}
            cluster.save(stage/'bundle.json',snapshot)
            if checks(stage):raise ValueError('Fresh HTML bundle failed before install')
            from zo_web_2027_navigation_check import run as navigation_checks
            from zo_web_2027_grayscale_check import run as grayscale_checks
            if navigation_checks(stage) or grayscale_checks(stage):raise ValueError('Navigation/grayscale failed before install')
            require_fresh(snapshot)
            produced=stage/'delivery/docs'
            paths=[p.relative_to(produced) for p in produced.rglob('*') if p.is_file()]
            installed=install_current(produced,out,paths)
            record={'sources':baseline,'output_dir':'docs','files':installed,'pages':{key:{'source':path.with_suffix('.qmd').as_posix(),'html':(Path('docs')/path).as_posix(),'html_sha256':sha(out/path)} for key,path in PAGES.items()},'origin':'fresh canonical-source render; validated before automatic docs replacement','published':False}
            result=check_current(out,record)
            operating=json.loads((ROOT/RECEIPT).read_text('utf-8'));operating['canonical_html_build']=record
            cluster.save(ROOT/RECEIPT,operating);cluster.save(reports/'canonical-output-check.json',result)
            print(json.dumps(result,ensure_ascii=False));print('Current HTML:',out/PAGES['home'],flush=True)
            return 0
        finally:
            for p in stage.glob('*.json'):shutil.copyfile(p,reports/p.name)
            if mirror.is_dir():
                logs=reports/'render-logs';logs.mkdir(exist_ok=True)
                for p in mirror.glob('*.log'):shutil.copyfile(p,logs/p.name)
                if not mirror.is_relative_to((ROOT/'.quarto/course_html_build').resolve()):raise ValueError('Unsafe build scratch cleanup')
                shutil.rmtree(mirror)


def main():
    parser=argparse.ArgumentParser(description='Build and overwrite current course HTML in configured docs; audit holds reports only.')
    parser.add_argument('command',choices=['build','check'])
    parser.add_argument('--output',type=Path,default=ROOT/'docs')
    parser.add_argument('--reports',type=Path)
    args=parser.parse_args();out=args.output.resolve()
    if out!=canonical_output():parser.error('Use canonical docs output; _audit is reserved for verification evidence')
    if args.command=='build':return build(out,args.reports)
    print(json.dumps(check_current(out),ensure_ascii=False));return 0


if __name__=='__main__':raise SystemExit(main())
