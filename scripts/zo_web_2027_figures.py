"""G01 shared figure profile: paired SVG/PDF from identical TeX/style/labels."""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import sys
from bs4 import BeautifulSoup
from zo_build_boundary import official_inputs
from zo_graphics import graph_path, load_graph, load_variation, load_variation_html

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01'
CONFIG = PACKAGE / 'giao_dien/web_2027_figures.json'
PROFILE = ROOT / '_design/web_2027_mau_dung_chung/figure-profile-candidate'
# Stable dependency-key namespace; actual IO is resolved by graph_path/module.
GRAPH = ROOT / 'quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math'
VARIATION = ROOT / 'quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math'

def sha(path):
    return hashlib.sha256(graph_path(path, ROOT).read_bytes()).hexdigest()

def module(name, path):
    if Path(path).resolve() == (GRAPH / 'zo_graph_build.py').resolve():
        return load_graph(name, ROOT)
    if Path(path).name == 'zo_variation_build.py':
        return load_variation(path, name, ROOT)
    if Path(path).resolve() == (VARIATION / 'zo_variation_html.py').resolve():
        return load_variation_html(name, ROOT)
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

def dependencies(config):
    paths = [CONFIG, ROOT/'scripts/zo_course_cover_assets.py', GRAPH/'axis_ticks.py', GRAPH/'zo_graph_build.py', GRAPH/'tex/zo_graph_v02.tex',
             GRAPH/'tex/zo_graph_v04.tex', GRAPH/'profiles/lesson-g03.json', GRAPH/'mau/cover_cubic_04.tex',
             PROFILE/'frame-tokens.json', PROFILE/'production-figures.css',
             VARIATION/'zo_variation_html.py', VARIATION/'zo_variation_build.py',
             PACKAGE/config['variation_source'],
             ROOT/'_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/design/color_system.json']
    paths += [PACKAGE/'hinh'/f'{name}.tex' for name in config['graphs']]
    paths += [ROOT/name for name in set(config['label_layouts'].values())]
    paths += list((ROOT/'assets/fonts').glob('STIXTwo*.otf'))
    return {p.relative_to(ROOT).as_posix():sha(p) for p in paths}

@official_inputs()
def build(output, force=False, reuse_graphs=False):
    output = output.resolve()
    if not output.is_relative_to(ROOT/'.quarto'):
        raise ValueError('Official graph build intermediates must stay inside .quarto.')
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    before = dependencies(config)
    destination=PACKAGE/config['asset_directory']
    if reuse_graphs:
        receipt=json.loads((destination/'manifest.json').read_text(encoding='utf-8'))
        recorded={k:v for k,v in receipt['source_hashes'].items() if k!=Path(__file__).relative_to(ROOT).as_posix()}
        # Native HTML BBT data are not inputs to graph SVGs. Refresh that
        # dependency only after independently validating it; all graph/style/
        # font inputs and every vector remain strictly hash-checked below.
        native_key=(PACKAGE/config['variation_source']).relative_to(ROOT).as_posix()
        if {k:v for k,v in recorded.items() if k!=native_key}!={k:v for k,v in before.items() if k!=native_key}:
            raise ValueError('Graph inputs changed; cannot reuse vectors.')
        if recorded.get(native_key)!=before.get(native_key):
            sys.path.insert(0,str(VARIATION))
            variation=module('variation_refresh',VARIATION/'zo_variation_html.py')
            variation.load_data(PACKAGE/config['variation_source'])
            receipt['native_variation_dependency_refreshed']=True
        expected={name+ext for name in config['graphs'] for ext in ['.svg','.pdf']}|{'cover-light.svg','cover-dark.svg'}
        if set(receipt['assets'])!=expected:raise ValueError('Incomplete vector cache.')
        for name,digest in receipt['assets'].items():
            if sha(destination/name)!=digest:raise ValueError('Vector cache changed: '+name)
        receipt['source_hashes']=before
        receipt['builder_sha256']=sha(Path(__file__))
        receipt['reused_vectors_with_verified_inputs']=True
        (destination/'manifest.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('Reused all verified vectors; updated adapter provenance, no TeX rebuild needed.')
        return
    graph = module('graph04_web', GRAPH/'zo_graph_build.py')
    generated = {}
    for name in config['graphs']:
        print('Building', name, flush=True)
        command = [str(PACKAGE/'hinh'/f'{name}.tex'), '--style','0.4','--layout',config['lesson_layout'],'--check','--out-dir',str(output/'graphs')]
        if name in config['label_layouts']:
            command += ['--label-layout',str(ROOT/config['label_layouts'][name])]
        if force: command += ['--force']
        pdf, svg = graph.build(graph.parse_args(command))
        generated[svg.name] = svg
        generated[pdf.name] = pdf
    old=json.loads((destination/'manifest.json').read_text(encoding='utf-8'))
    # Lesson layout never changes cover geometry. Verify its original source,
    # styles and fonts, and retain the exact cover assets and origin receipt.
    cover_keys=[(GRAPH/f).relative_to(ROOT).as_posix() for f in
                ['mau/cover_cubic_04.tex','tex/zo_graph_v02.tex','tex/zo_graph_v04.tex']]
    cover_keys += [k for k in before if k.startswith('assets/fonts/')]
    if any(old['source_hashes'].get(k)!=before[k] for k in cover_keys):
        from zo_course_cover_assets import verify_rebuild
        for surface in ['light','dark']:
            verify_rebuild(ROOT,graph_path(GRAPH/'mau/cover_cubic_04.tex'), 'transparent-'+surface,destination/('cover-'+surface+'.svg'))
    for name in ['cover-light.svg','cover-dark.svg']:
        if sha(destination/name)!=old['assets'][name]:raise ValueError('Cover asset changed: '+name)
        generated[name]=destination/name
    if dependencies(config) != before:
        raise ValueError('Source changed while graphs were building; refuse mixed outputs.')
    destination.mkdir(parents=True,exist_ok=True)
    for name,source in generated.items():
        target=destination/name
        if target.exists() and sha(target)!=sha(source) and not force:
            raise ValueError('Different existing web asset; requires explicit --force: '+name)
        if source.resolve()!=target.resolve():shutil.copyfile(source,target)
    receipt={'profile':config['profile'],'source_hashes':before,'builder_sha256':sha(Path(__file__)),
             'assets':{name:sha(destination/name) for name in generated},
             'course_pdf_changed':False,'graph_pdf_evidence':output.relative_to(ROOT).as_posix(),
             'lesson_layout':config['lesson_layout'],'preserved_cover_origin':old.get('preserved_cover_origin',old)}
    (destination/'manifest.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Web SVG assets and guarded provenance:',destination,flush=True)

def graph_only_dependencies(values,config):
    # BBT data/renderer are consumed afresh by apply(), not by the cached
    # graph SVG/PDF compiler. Do not rebuild all vectors for a native-only fix.
    native={(VARIATION/name).relative_to(ROOT).as_posix() for name in
            ["zo_variation_build.py","zo_variation_html.py"]}
    native.add((PACKAGE/config["variation_source"]).relative_to(ROOT).as_posix())
    return {key:value for key,value in values.items() if key not in native}

def verify(config):
    directory=PACKAGE/config['asset_directory']
    receipt=json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    if graph_only_dependencies(receipt['source_hashes'],config) != graph_only_dependencies(dependencies(config),config):
        raise ValueError('Web figure inputs changed; rebuild with zo_web_2027_figures.py before rendering.')
    for name,digest in receipt['assets'].items():
        if sha(directory/name)!=digest: raise ValueError('Web SVG changed: '+name)
    # Fresh native data are validated independently, never certified by a
    # historical graph-cache receipt.
    native=module("verify_native_bbt",VARIATION/"zo_variation_html.py")
    native.load_data(PACKAGE/config["variation_source"])
    return directory,receipt

def verify_print():
    config=json.loads(CONFIG.read_text(encoding='utf-8'))
    directory,receipt=verify(config)
    expected={name+ext for name in config['graphs'] for ext in ['.svg','.pdf']}|{'cover-light.svg','cover-dark.svg'}
    if set(receipt['assets'])!=expected:
        raise ValueError('Incomplete shared graph pairs: rebuild figures before any PDF render.')
    verify_print_source((PACKAGE/'index.qmd').read_text(encoding='utf-8'),config)
    return directory,receipt

def verify_print_source(text,config):
    references=re.findall(r'\]\(([^)]+do_thi_\d{2}\.svg)\)',text)
    expected={config['asset_directory']+'/'+name+'.svg' for name in config['graphs']}
    if set(references)!=expected or len(references)!=len(expected):
        raise ValueError('QMD graph references must select exactly the current shared SVG/PDF pairs; legacy paths are forbidden.')

def apply(target, page, output_root):
    """Replace only figure payloads after the strict accepted-layout guard."""
    config=json.loads(CONFIG.read_text(encoding='utf-8'))
    directory,receipt=verify(config)
    runtime=output_root/'assets/zo_web_2027/figures_0_4'
    runtime.mkdir(parents=True,exist_ok=True)
    for name in receipt['assets']: shutil.copyfile(directory/name,runtime/name)
    shutil.copyfile(PROFILE/'production-figures.css',runtime/'production-figures.css')
    url=lambda name:os.path.relpath(runtime/name,page.parent).replace('\\','/')
    target.head.append(target.new_tag('link',rel='stylesheet',href=url('production-figures.css')))
    # Match original graph identity, not arbitrary img position or basename hashes.
    seen=set()
    for image in target.select('.reader-content .figure-viewport img'):
        match=re.search(r'(do_thi_\d{2})\.svg$',image['src'])
        if not match: continue
        name=match.group(1)
        if name not in config['graphs']: raise ValueError('Unconfigured graph: '+name)
        seen.add(name)
        image['src']=url(name+'.svg')
        from zo_graphics import set_lesson_graph_size
        set_lesson_graph_size(image,directory/(name+'.svg'),ROOT)
        image['class'] += ['zo-graph-04']
        image.parent['class'] += ['zo-figure-scroll']
    if seen!=set(config['graphs']): raise ValueError('Not all canonical G01 graphs were matched: '+str(seen))
    sys.path.insert(0,str(VARIATION))
    variation=module('variation04_web',VARIATION/'zo_variation_html.py')
    records=variation.load_data(PACKAGE/config['variation_source'])
    by_id={r['id']:r for r in records};fragments=variation.math_fragments(records)
    seen=set()
    for figure in target.select('.reader-content figure.zo-variation-asset[data-bbt]'):
        rid=figure['data-bbt'];seen.add(rid)
        record=by_id[rid]
        viewport=figure.select_one('.figure-viewport')
        original=figure.select_one('table.variation')
        if original is None: raise ValueError('Missing accepted BBT data: '+rid)
        rows=[[c.get_text(' ',strip=True) for c in row.find_all(['th','td'],recursive=False)] for row in original.find_all('tr')]
        legacy_rows=copy.deepcopy(record['rows'])
        for r in range(1,len(legacy_rows)):
            for c in record.get('excluded_columns',[]):legacy_rows[r][c]='∥'
        if rows!=legacy_rows: raise ValueError('BBT source/accepted data differ: '+rid)
        caption=figure.select_one('figcaption')
        if not caption: raise ValueError('Missing original BBT caption: '+rid)
        caption_text=caption.get_text(' ',strip=True)
        native=BeautifulSoup(variation.render_record(record,fragments),'html.parser').select_one('table')
        # Preserve the learner-facing QMD caption, not the internal JSON title.
        native.caption.string=caption_text
        old_image=viewport.select_one('img')
        if old_image:old_image.decompose()
        figure.select_one('.visually-hidden').decompose()
        if caption.parent is viewport:
            caption.insert_before(copy.deepcopy(native))
        else:
            viewport.append(copy.deepcopy(native))
        viewport['class'] += ['zo-figure-scroll']
    if seen!=set(by_id): raise ValueError('Incomplete native BBT integration: '+str(seen))
    frames=json.loads((PROFILE/'frame-tokens.json').read_text(encoding='utf-8'))
    palette=json.loads((ROOT/frames['palette_source']).read_text(encoding='utf-8'))['palette']
    cover=config['cover'];width,height=frames['sizes_px'][cover['shape']][cover['size']]
    color=palette[frames['backgrounds'][cover['background']]]
    hero=target.select_one('.hero-art');image=hero.select_one('img')
    image['src']=url('cover-dark.svg' if cover['surface']=='transparent-dark' else 'cover-light.svg')
    frame=target.new_tag('div',attrs={'class':'zo-cover-frame',
        'style':f'--frame-width:{width}px;--frame-ratio:{width}/{height};--frame-bg:{color}'})
    image.wrap(frame)
    # No authoring controls or second lesson DOM are introduced.
    target.body['data-zo-figure-profile']=config['profile']

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'.quarto/zo_g01_figures')
    parser.add_argument('--force',action='store_true')
    parser.add_argument('--reuse-graphs',action='store_true',help='Reuse SVGs only after all mathematical/style/font inputs and every SVG hash match.')
    args=parser.parse_args();build(args.output,args.force,args.reuse_graphs)
