"""Scoped G01 HTML adapter. Content always comes from the fresh Quarto render.

The accepted layout is metadata (nodes, attributes, and content bindings), not
a second copy of the mathematics. Normal builds never read _audit or docs as
an input. Only the explicit, one-time import command reads a visual reference.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote, urlsplit
from zo_build_boundary import official_inputs

sys.dont_write_bytecode = True
from bs4 import BeautifulSoup, Comment, Doctype, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path('content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01')
PLAN = ROOT / PACKAGE / 'giao_dien/web_2027_layout.json'
KIT = ROOT / '_design/web_2027_mau_dung_chung'
ACCEPTED_SHA = '5c97396dd9656971e442cb60a07aa799935d3233bf2ae15a53ebc57f76c77e3c'
MARKER = 'zo-web-2027-production'


def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode('utf-8')).hexdigest()


def runtime_source_checks(root=ROOT, plan=None):
    """Check current source bindings before render; never renew acceptance."""
    root=Path(root).resolve()
    if plan is None:
        plan=json.loads((root/PACKAGE/'giao_dien/web_2027_layout.json').read_text(encoding='utf-8'))
    values={'G01 runtime asset map exists':bool(plan.get('assets'))}
    for spec in plan.get('assets',{}).values():
        source=(root/spec['source']).resolve()
        values['G01 runtime source current '+spec['source']]=(source.is_relative_to(root) and source.is_file() and sha(source.read_bytes())==spec['sha256'])
    return values


def norm(text):
    return re.sub(r'\s+', ' ', text).strip()


def pools(root):
    texts = {sha(norm(str(n))): str(n) for n in root.find_all(string=True)
             if norm(str(n)) and not n.find_parent('math') and not isinstance(n, Comment)}
    maths = {}
    for node in root.select('math'):
        annotation = node.select_one('annotation[encoding="application/x-tex"]')
        key = sha(norm(annotation.get_text()) if annotation else str(node))
        maths[key] = node
    return texts, maths


def content_fingerprint(root):
    return {
        'text_sha256': sha(norm(root.get_text(' ', strip=True))),
        'ids': [n['id'] for n in root.select('[id]')],
        'math': [sha(norm(n.select_one('annotation').get_text())) for n in root.select('math')],
        'disclosures': [[n.get('id'), n.has_attr('open')] for n in root.select('details')],
    }


def import_layout(reference, source, destination):
    raw = reference.read_bytes()
    if sha(raw) != ACCEPTED_SHA:
        raise ValueError('Accepted G01 reference hash mismatch; refuse to import an older page.')
    ref = BeautifulSoup(raw.decode('utf-8'), 'html.parser')
    src = BeautifulSoup(source.read_text(encoding='utf-8'), 'html.parser')
    source_root = src.select_one('.zo-on-thi-package')
    texts, maths = pools(source_root)
    assets = {}
    presentation = []

    def asset(href):
        resolved = (reference.parent / unquote(urlsplit(href).path)).resolve()
        if not resolved.is_relative_to(ROOT) or not resolved.is_file():
            raise ValueError('Missing reference asset: ' + href)
        digest = sha(resolved.read_bytes())
        # Prefer the mathematical source SVG when byte-identical. Approved
        # display variants are promoted below and guarded against source drift.
        candidates = list((ROOT / PACKAGE / 'hinh').glob('*.svg')) if resolved.suffix == '.svg' else []
        for candidate in candidates:
            if sha(candidate.read_bytes()) == digest:
                return {'package_asset': 'hinh/' + candidate.name}
        if digest not in assets:
            name = resolved.name
            for candidate in [*KIT.glob('*.css'), *KIT.glob('*.js'), *KIT.glob('assets/*'),
                              *(ROOT / '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac').rglob('*')]:
                if candidate.is_file() and candidate.suffix == resolved.suffix and sha(candidate.read_bytes()) == digest:
                    resolved = candidate
                    name = candidate.name
                    break
            if resolved.is_relative_to(ROOT / '_audit'):
                # Reference images must have a canonical asset outside audit.
                qr = ROOT / 'assets/images/qr_bao_tro_zo_math_vietcombank.jpg'
                if sha(qr.read_bytes()) == digest:
                    resolved, name = qr, qr.name
                else:
                    name = re.sub(r'^(?:[0-9a-f]{12}_)+', '', resolved.name)
                    dest = ROOT / PACKAGE / 'giao_dien/assets' / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if dest.exists() and sha(dest.read_bytes()) != digest:
                        raise ValueError('Refuse to overwrite a different canonical asset: ' + str(dest))
                    shutil.copyfile(resolved, dest)
                    resolved = dest
            assets[digest] = {'source': resolved.relative_to(ROOT).as_posix(), 'name': name, 'sha256': digest}
        return {'asset': digest}

    def encode(node):
        if isinstance(node, Comment): return None
        if isinstance(node, NavigableString):
            text = str(node)
            if not text.strip(): return {'literal': text}
            key = sha(norm(text))
            if node.find_parent(class_='zo-on-thi-package') and key in texts:
                return {'text': key, 'leading': re.match(r'^\s*', text).group(), 'trailing': re.search(r'\s*$', text).group()}
            presentation.append(norm(text))
            return {'literal': text}
        if not isinstance(node, Tag): return None
        if node.name == 'math':
            a = node.select_one('annotation[encoding="application/x-tex"]')
            key = sha(norm(a.get_text()) if a else str(node))
            if key not in maths: raise ValueError('Reference math absent from canonical render: ' + str(a))
            return {'math': key}
        attrs = copy.deepcopy(node.attrs)
        attrs.pop('data-canonical-href', None)
        if node.name in ['link','img','script']:
            key = 'src' if node.name in ['img','script'] else 'href'
            if attrs.get(key): attrs[key] = asset(attrs[key])
        if node.name == 'a' and attrs.get('href') and not attrs['href'].startswith(('#','http','mailto:')):
            href = attrs['href']
            source_href = node.get('data-canonical-href', href)
            if 'home' in href or 'home' in source_href or '2027/index' in source_href:
                attrs['href'] = {'course_home': True}
            elif '.pdf' in href:
                match = re.search(r'(index(?:_[a-z_]+)?\.pdf)', unquote(href))
                if not match: raise ValueError('Unrecognized PDF link: ' + href)
                attrs['href'] = {'package_asset': match.group(1)}
            elif source_href.startswith('/'):
                site_path = source_href.lstrip('/')
                if site_path.endswith('.qmd'): site_path = site_path[:-4] + '.html'
                attrs['href'] = {'site_path': site_path}
            else:
                p = (reference.parent / unquote(urlsplit(source_href).path)).resolve()
                if p.is_relative_to(ROOT / 'docs'):
                    attrs['href'] = {'site_path': p.relative_to(ROOT / 'docs').as_posix()}
                elif p.is_relative_to(ROOT / '_audit'):
                    raise ValueError('Unresolved audit link: ' + href)
                else:
                    raise ValueError('Unresolved local link: ' + href)
        return {'tag': node.name, 'attrs': attrs, 'children': [v for c in node.children if (v := encode(c)) is not None]}

    layout = encode(ref.html)
    destination.parent.mkdir(parents=True, exist_ok=True)
    data = {'schema_version': 1, 'package': 'R1-G01', 'accepted_sha256': ACCEPTED_SHA,
            'content_source': (PACKAGE / 'index.qmd').as_posix(),
            'source_fingerprint': content_fingerprint(source_root),
            'source_asset_hashes': {p.relative_to(ROOT).as_posix(): sha(p.read_bytes())
                                   for folder, pattern in [('hinh','*.svg'),('du_lieu','*.json')]
                                   for p in sorted((ROOT / PACKAGE / folder).glob(pattern))},
            'assets': assets, 'layout': layout,
            'presentation_literals': sorted(set(presentation))}
    destination.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Imported layout; canonical text bindings:', len(texts), 'math keys:', len(maths), 'assets:', len(assets))


@official_inputs()
def adapt(path, output_root):
    from zo_course_cover import load_cover, check_html
    relative = path.resolve().relative_to(output_root.resolve())
    is_package = relative.parent.parent == Path('content/thpt/on_thi_toan_thpt/hoc_lieu') and relative.parent.name != 'd0'
    if is_package:
        load_cover(ROOT, relative.parent.name, allow_direction_approved=relative.parent.name in {"r1_g05","r2_g01"})
    result = _adapt(path, output_root)
    from zo_web_2027_shell import require as require_shell
    rendered=BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser")
    if rendered.body is not None and rendered.body.has_attr("data-zo-web-shell"):
        require_shell(rendered,path)
    if is_package:
        check_html(ROOT, relative.parent.name, path, allow_direction_approved=relative.parent.name in {"r1_g05","r2_g01"})
    return result


def _adapt(path, output_root):
    relative=path.resolve().relative_to(output_root.resolve())
    if (ROOT/relative.parent/'giao_dien/html.json').is_file():
        from zo_web_2027_package import adapt as adapt_package
        return adapt_package(path,output_root,relative.parent)
    if path.resolve() == (output_root / "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g05/index.html").resolve():
        from zo_web_2027_g05 import adapt as adapt_g05
        return adapt_g05(path,output_root)
    if path.resolve() == (output_root / "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/index.html").resolve():
        from zo_web_2027_g04 import adapt as adapt_g04
        return adapt_g04(path, output_root)
    if path.resolve() == (output_root / "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.html").resolve():
        from zo_web_2027_g03 import adapt as adapt_g03
        return adapt_g03(path, output_root)
    if path.resolve() == (output_root / 'content/thpt/on_thi_toan_thpt/index.html').resolve():
        from zo_web_2027_gateway import adapt as adapt_gateway
        return adapt_gateway(path,output_root)
    if path.resolve() == (output_root / 'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.html').resolve():
        from zo_web_2027_g02_production import adapt as adapt_g02
        return adapt_g02(path, output_root)
    if path.resolve() == (output_root / 'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.html').resolve():
        from zo_web_2027_d0 import adapt as adapt_d0
        return adapt_d0(path, output_root)
    if path.resolve() == (output_root / 'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html').resolve():
        from zo_web_2027_home import adapt as adapt_home
        return adapt_home(path, output_root)
    source = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    if MARKER not in source.body.get('class', []):
        if path.parent.name == 'r1_g01':
            raise ValueError('G01 production marker missing; refuse silent rollback to the legacy layout')
        return False
    if source.body.has_attr('data-zo-web-production'): return False
    from zo_math_notation import require_source, require_runtime_css
    require_source(ROOT / PACKAGE / 'index.qmd')
    require_runtime_css(KIT / 'web-shell.css')
    source_root = source.select_one('.zo-on-thi-package')
    if not source_root: raise ValueError('Production marker without canonical G01 content')
    texts, maths = pools(source_root)
    plan = json.loads(PLAN.read_text(encoding='utf-8'))
    from zo_web_2027_backlog_check import require_source as require_structure_source
    require_structure_source(ROOT/PACKAGE/'index.qmd',json.loads((ROOT/PACKAGE/'giao_dien/he_nhan.json').read_text(encoding='utf-8')))
    for name, digest in plan['source_asset_hashes'].items():
        if sha((ROOT / name).read_bytes()) != digest:
            raise ValueError('Canonical diagram/data changed; revalidate the approved display asset: ' + name)
    from zo_course_learning_goals import inverse_g01_fingerprint
    from zo_course_instructions import restore_g01_for_comparison
    from zo_course_editorial import restore_g01_for_comparison as restore_editorial_for_comparison
    from zo_course_numbering import restore_g01_for_comparison as restore_numbering
    from zo_course_remediation import restore_g01_for_comparison as restore_remediation
    from zo_course_table_roles import restore_g01_for_comparison as restore_table_functions
    table_comparison=restore_table_functions(source_root,plan,ROOT/PACKAGE/'index.qmd')
    remediation_comparison=restore_remediation(table_comparison,plan,ROOT/PACKAGE/'index.qmd')
    numbering_comparison=restore_numbering(remediation_comparison,plan,ROOT/PACKAGE/'index.qmd')
    editorial_comparison=restore_editorial_for_comparison(numbering_comparison,plan,ROOT/PACKAGE/'index.qmd')
    comparison = restore_g01_for_comparison(editorial_comparison,plan,ROOT/PACKAGE/'index.qmd')
    if inverse_g01_fingerprint(comparison,plan,content_fingerprint,ROOT/PACKAGE/'index.qmd') != plan['source_fingerprint']:
        raise ValueError('Fresh QMD content/IDs/disclosures differ from the imported baseline; do not silently drop new content.')
    target = BeautifulSoup('', 'html.parser')
    runtime = output_root / 'assets/zo_web_2027'
    runtime.mkdir(parents=True, exist_ok=True)
    assets = {}
    for digest, spec in plan['assets'].items():
        src = ROOT / spec['source']
        if sha(src.read_bytes()) != spec['sha256']:
            raise ValueError('Accepted runtime asset changed: ' + spec['source'])
        dest = runtime / spec['name']
        shutil.copyfile(src, dest)
        assets[digest] = os.path.relpath(dest, path.parent).replace('\\','/')
    # CSS uses assets/fonts relative to its own location.
    font_root = ROOT / '_design/ngon_ngu_thiet_ke_zo_math_0_4/07_mau_thi_giac/assets'
    for src in font_root.iterdir():
        if src.name in ['BeVietnamPro_Regular.ttf','BeVietnamPro_SemiBold.ttf','STIXTwoMath.ttf'] or src.name.startswith('OFL_'):
            dest = runtime / 'assets/fonts' / src.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)

    def value(v):
        if not isinstance(v, dict): return v
        if 'asset' in v: return assets[v['asset']]
        if 'package_asset' in v: return v['package_asset']
        if 'course_home' in v: return os.path.relpath(output_root / 'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html',path.parent).replace('\\','/')
        if 'site_path' in v: return os.path.relpath(output_root / v['site_path'],path.parent).replace('\\','/')
        raise ValueError('Unknown URL binding')

    def decode(n):
        # Download metadata is current source content, not an imported
        # historical text key. The full inverse comparison above remains strict.
        if n.get('attrs',{}).get('id')=='tai-tai-lieu':
            section=source_root.find(id='tai-tai-lieu')
            from zo_web_2027_downloads import project_source_section
            return project_source_section(section,n['attrs'])
        if 'table_function_node' in n:
            from zo_course_table_roles import source_node
            return source_node(source_root,n['table_function_node'],plan)
        if 'source_node' in n:
            from zo_course_remediation import source_node
            return source_node(source_root,n['source_node'],plan)
        if 'literal' in n: return NavigableString(n['literal'])
        if 'text' in n:
            if n['text'] not in texts: raise ValueError('Canonical wording changed; update its approved layout binding: ' + n['text'])
            return NavigableString(n.get('leading','') + norm(texts[n['text']]) + n.get('trailing',''))
        if 'math' in n:
            if n['math'] not in maths: raise ValueError('Canonical mathematics changed; layout requires revalidation')
            return copy.deepcopy(maths[n['math']])
        tag = target.new_tag(n['tag'], attrs={k:value(v) for k,v in n['attrs'].items()})
        for child in n['children']: tag.append(decode(child))
        return tag

    target.append(Doctype('html'))
    target.append(decode(plan['layout']))
    target.body['class'].append(MARKER)
    target.body['data-zo-web-production'] = 'R1-G01'
    # Remove preview-only claims, while retaining their geometry.
    target.title.string = 'Đơn điệu và cực trị — ZO Math'
    target.select_one('.lab-link').string = 'ZO Math'
    target.select_one('.prototype-note').string = 'Bản HTML dựng từ nguồn · Nội dung và giao diện G01 đã đồng bộ; các tệp PDF chưa được dựng lại.'
    generated_root = target.select_one('.zo-on-thi-package')
    if len(generated_root.select('math')) != len(source_root.select('math')):
        raise ValueError('Mathematics count changed during production adaptation')
    # Figure payloads are an explicit, separately guarded HTML-only opt-in.
    # Validate the complete accepted QMD/layout projection BEFORE adding native
    # MathML BBT cells; never weaken its content fingerprint for a figure change.
    from zo_web_2027_figures import apply as apply_figures
    apply_figures(target, path, output_root)
    from zo_web_2027_downloads import apply as apply_downloads
    apply_downloads(target, path, output_root)
    from zo_web_2027_consistency import apply as apply_consistency
    apply_consistency(target, path, runtime)
    from zo_r1_g01_labels import apply as apply_labels, remove_redundant_labels
    if (ROOT / PACKAGE / 'giao_dien/he_nhan.json').is_file():
        apply_labels(target)
        remove_redundant_labels(target)
    from zo_web_2027_fallback_nav import apply as apply_fallback
    apply_fallback(target)
    from zo_course_tables import apply as apply_tables
    apply_tables(target, 'r1_g01', path, runtime)
    from zo_web_2027_backlog_check import require as require_structure
    require_structure(target,json.loads((ROOT/PACKAGE/'giao_dien/he_nhan.json').read_text(encoding='utf-8')))
    ids = [n['id'] for n in generated_root.select('[id]')]
    if len(ids) != len(set(ids)):
        from collections import Counter
        raise ValueError('Duplicate IDs in adapted content: '+str([i for i,n in Counter(ids).items() if n>1]))
    if '_audit/' in str(target) or 'home-reading.html' in str(target):
        raise ValueError('Production output retains a preview dependency')
    from zo_web_2027_navigation import apply as apply_course_navigation
    apply_course_navigation(target, path, output_root, runtime, 'g01')
    from zo_course_pdf_download_state import apply as apply_pdf_state
    apply_pdf_state(target,ROOT,PACKAGE)
    from zo_web_2027_consistency import apply_editorial_policy
    apply_editorial_policy(target)
    from zo_course_html import write
    write(path, target)
    print('G01 production adapter:', path, 'regions:', len(generated_root.select('.reading-region')))
    return True


def main():
    if os.environ.get('ZO_COURSE_RAW_HTML_ONLY')=='1' and (ROOT/'isolated.index').is_file():
        return 0
    parser = argparse.ArgumentParser()
    parser.add_argument('--import-layout', type=Path)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--output-root', type=Path)
    parser.add_argument('--html', type=Path)
    args = parser.parse_args()
    if args.import_layout:
        if not args.source: parser.error('--source required for import')
        import_layout(args.import_layout.resolve(), args.source.resolve(), PLAN)
        return 0
    output = (args.output_root or Path(os.environ.get('QUARTO_PROJECT_OUTPUT_DIR','docs'))).resolve()
    if args.html:
        paths = [args.html.resolve()]
    else:
        listed = os.environ.get('QUARTO_PROJECT_OUTPUT_FILES')
        listing_file = os.environ.get('QUARTO_USE_FILE_FOR_PROJECT_OUTPUT_FILES')
        if listing_file:
            listed = Path(listing_file).read_text(encoding='utf-8')
        if listed is None:
            parser.error('Use --html explicitly outside a Quarto post-render hook')
        rendered = {(ROOT / item).resolve() for item in listed.splitlines() if item.strip()}
        candidate = (output / PACKAGE / 'index.html').resolve()
        home = (output / 'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html').resolve()
        d0 = (output / 'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.html').resolve()
        g02 = (output / 'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.html').resolve()
        gateway=(output/'content/thpt/on_thi_toan_thpt/index.html').resolve()
        g03 = (output / "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.html").resolve()
        paths = [p for p in [candidate, home, d0, g02, g03, gateway] if p in rendered]
        from zo_course_labels import governed, LEGACY
        paths=list(dict.fromkeys(paths+[p for p in rendered if governed(p) and p.parent.name not in LEGACY]))
    for path in paths:
        if path.is_file():
            adapt(path, output)
            from zo_course_labels import governed, LEGACY, binding as course_label_binding, html_checks as course_label_html_checks, require as require_labels
            if governed(path) and path.parent.name not in LEGACY:
                source=ROOT/path.relative_to(output).with_suffix(".qmd")
                if BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser").body is not None:
                    require_labels(course_label_html_checks(BeautifulSoup(path.read_text(encoding="utf-8"),"html.parser"),course_label_binding(source)),"post-render HTML")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
