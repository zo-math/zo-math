"""Build one coherent four-page preview from current sources, never old HTML.

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
              '.svg','.png','.jpg','.jpeg','.ttf','.woff','.woff2','.scss'}


def sources():
    result = {}
    for folder in INPUTS:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file() and p.suffix in EXTENSIONS and not any(x in p.parts for x in ['__pycache__','.quarto']):
                result[p.relative_to(ROOT).as_posix()] = sha(p)
    for p in ROOT.glob('_quarto*.yml'):
        result[p.name] = sha(p)
    for p in (ROOT/'content').glob('*.qmd'):
        result[p.relative_to(ROOT).as_posix()] = sha(p)
    return result


def require_fresh(manifest, current=None):
    if manifest['sources'] != (sources() if current is None else current):
        raise ValueError('Bundle is stale: rebuild all four pages from current sources')


def checks(out):
    manifest = json.loads((out/'bundle.json').read_text(encoding='utf-8'))
    require_fresh(manifest)
    values = {'all source fingerprints current': True}
    preview = out/'html-current'
    expected = {key:(preview/(key+'-reading.html')).resolve() for key in PAGES}
    for key, page in expected.items():
        doc = BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        if key in {'g01','g02'}:
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
            download_text=doc.select_one('#tai-tai-lieu').get_text(' ',strip=True)
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
    """Retain only the assets reached by the four preview documents."""
    delivery = (out/'delivery/docs').resolve()
    queue = list((out/'html-current').glob('*.html'))
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
    while queue:
        p = queue.pop().resolve()
        if p in seen or not p.is_file():
            continue
        seen.add(p)
        if p.is_relative_to(delivery):
            keep.add(p)
        references = []
        if p.suffix == '.html':
            doc = BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
            references = [n.get('src',n.get('href')) for n in doc.select('img[src],script[src],link[href],a[href]')]
        elif p.suffix == '.css':
            references = re.findall(r'url\([\s\"\']*([^\)\"\']+)',p.read_text(encoding='utf-8'))
        for ref in references:
            url = urlsplit(ref.strip())
            if not url.scheme and not url.netloc and url.path:
                target = (p.parent/unquote(url.path)).resolve()
                if target.is_relative_to(delivery):
                    queue.append(target)
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
    mirror=out/'final/r1_g01-raw'
    # The shared footer reads these canonical source pages, not older HTML.
    for p in (ROOT/'content').glob('*.qmd'):
        shutil.copyfile(p,mirror/'content'/p.name)
    env=dict(os.environ,ZO_WEB_2027_HOME_REPORT=str(mirror/'_audit/home-build.json'))
    for key,path in PAGES.items():
        command=['python','scripts/zo_python.py','-B','scripts/zo_web_2027_production.py',
                 '--html',str(Path('docs')/path),'--output-root','docs']
        with (mirror/(key+'-adapt.log')).open('w',encoding='utf-8') as log:
            if subprocess.run(command,cwd=mirror,env=env,stdout=log,stderr=subprocess.STDOUT).returncode:
                raise RuntimeError(key+' canonical adapter failed: see '+str(log.name))
        print('Adapted',key,flush=True)
    shutil.copyfile(mirror/'_audit/home-build.json',out/'build.json')
    delivery=out/'delivery/docs'
    shutil.copytree(mirror/'docs',delivery)
    preview=out/'html-current';preview.mkdir()
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


def build(out):
    if out.exists():
        raise ValueError('Fresh named output directory required; do not overwrite reviewed HTML')
    out.mkdir(parents=True)
    baseline = sources()
    cluster.PAGES = PAGES
    cluster.render(out,'final',html_only=True)
    adapt_bundle(out)
    if baseline != sources():
        raise ValueError('Sources changed during build; refuse a mixed bundle')
    cluster.save(out/'bundle.json',{'sources':baseline,'pages':{key:{'source':str(path.with_suffix('.qmd')).replace('\\','/'),
        'source_sha256':baseline[path.with_suffix('.qmd').as_posix()],
        'html_sha256':sha(out/'html-current'/(key+'-reading.html'))} for key,path in PAGES.items()},
        'origin':'all four freshly rendered from one source snapshot','published':False})
    checks(out)
    from zo_web_2027_navigation_check import run as navigation_checks
    if navigation_checks(out):
        raise ValueError('Four-page navigation checks failed')
    from zo_web_2027_grayscale_check import run as grayscale_checks
    if grayscale_checks(out):
        raise ValueError('Grayscale scrolling navigation regression failed')
    prune_delivery(out)
    manifest=json.loads((out/'bundle.json').read_text(encoding='utf-8'))
    manifest['asset_sha256']={p.relative_to(out).as_posix():sha(p) for p in (out/'delivery/docs').rglob('*') if p.is_file()}
    cluster.save(out/'bundle.json',manifest)
    mirror = (out/'final/r1_g01-raw').resolve()
    if not mirror.is_relative_to(out.resolve()):
        raise ValueError('Unsafe cleanup target')
    logs = out/'render-logs';logs.mkdir()
    for p in mirror.glob('*.log'):
        shutil.copyfile(p,logs/p.name)
    shutil.rmtree(mirror)
    print('Review:',out/'html-current/home-reading.html')
    return checks(out)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','check'])
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();out=args.output.resolve()
    if not out.is_relative_to(ROOT/'_audit') or out==ROOT/'_audit':
        parser.error('Named _audit output required')
    return build(out) if args.command=='build' else checks(out)


if __name__=='__main__':
    raise SystemExit(main())
