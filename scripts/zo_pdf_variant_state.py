"""Evidence for course PDF status based on the inputs selected for one edition."""
import json
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

import yaml

import zo_pdf_contract as contract


def evidence_path(source):
    return source.parent / '_quy_trinh/pdf_print_variants.json'


def evidence(root, source):
    path = evidence_path(source)
    if not path.is_file():
        return None
    data = contract._load_manifest(path)
    if data.get('version') != 1 or data.get('source') != source.relative_to(root).as_posix():
        raise ValueError('Invalid PDF edition evidence')
    if not isinstance(data.get('variants'), dict):
        raise ValueError('Missing PDF edition evidence records')
    return data


def projection(root, source, variant, *, text=None, pipeline=None):
    """Match the PDF section selector and follow its actual includes and figures.

    Unknown dependencies stay in the fingerprint. Keep the original anchor
    inventory too, since links to other sections can survive as web links.
    """
    from zo_course_pdf_layout import selected_source

    package = source.parent
    if text is None:
        text = source.read_text('utf-8')
    if pipeline is None:
        pipeline = contract._pipeline_records(root, source)
    package_profile = yaml.safe_load((package / '_quy_trinh/ho_so/index.yml').read_text('utf-8'))['package']
    print_package = {'id': package_profile['id'], 'version': str(package_profile['candidate_version'])}
    selected = selected_source(text, variant)
    if not selected.startswith('---'):
        selected = '---' + text.split('---', 2)[1] + '---\n' + selected
    includes, references = set(), set()

    def scan(body, parent, stack):
        for target in re.findall(r'\{\{<\s*include\s+([^>]+?)\s*>\}\}', body):
            path = (parent / target.strip().strip('"')).resolve()
            if not path.is_relative_to(root) or path in stack:
                raise ValueError('Invalid include in PDF edition: ' + target)
            includes.add(path)
            scan(path.read_text('utf-8'), path.parent, (*stack, path))
        for target in re.findall(r'!\[[^\n]*?\]\(([^)\s]+)|(?:src|href)=["\']([^"\']+)', body):
            name = next(value for value in target if value)
            if '://' not in name:
                references.add((parent / name).resolve())
        # Preserve handwritten TeX graphics and references in nested captions.
        for name in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', body):
            references.add((parent / name).resolve())

    scan(selected, package, (source,))
    graph_list = package / 'giao_dien/web_2027_figures.json'
    figure_dir = package / 'giao_dien/assets/figures_0_4'
    optional_figures, used_figures = set(), set()
    if graph_list.is_file():
        listing = json.loads(graph_list.read_text('utf-8'))
        for item in listing['figures']:
            if item['role'] == 'cover':
                continue
            tex = package / contract._safe_relative_path(item['source'], 'graph source')
            svg = figure_dir / tex.with_suffix('.svg').name
            pdf = svg.with_suffix('.pdf')
            family = {tex, svg, pdf}
            optional_figures.update(family)
            if family & references:
                used_figures.update(family)

    used_inputs = {}
    for item in pipeline:
        path = root / item['path']
        # The whole-graph receipt and HTML adapter do not enter the rendered
        # document. Selected graph files are checked individually below.
        if path in {figure_dir / 'manifest.json', package / 'giao_dien/html.json'}:
            continue
        if path in optional_figures and path not in used_figures:
            continue
        if path.suffix == '.qmd' and path.is_relative_to(package / 'noi_dung') and path not in includes:
            continue
        used_inputs[item['path']] = item['sha256']
    images = {path for path in references if path.is_file() and path.is_relative_to(root)
              and path.suffix.lower() in {'.svg', '.pdf', '.png', '.jpg', '.jpeg', '.webp'}}
    for path in includes | used_figures | images:
        key = path.relative_to(root).as_posix()
        if key not in used_inputs:
            used_inputs[key] = contract.sha256_file(path)
    anchors = re.findall(r'(?m)^#{1,6}\s+[^\n]*?\{#([^\s}]+)|\{#([^\s}]+)|\bid=["\']([^"\']+)', text)
    return contract._canonical_json_hash({
        'content': contract.course_pdf_source_digest(selected),
        'anchors': anchors,
        'print_package': print_package,
        'definition': contract.pdf_variant(root, source, variant),
        'inputs': used_inputs,
    })


def record_variant(root, source, variant, record, **inputs):
    return {
        'build_fingerprint': record['input_fingerprint'],
        'pdf_sha256': record['output']['sha256'],
        'projection_sha256': projection(root, source, variant, **inputs),
    }


def refresh_current(root, source):
    """Save edition evidence while the original build can still be verified."""
    data = evidence(root, source)
    if data is None:
        return
    manifest = contract._load_manifest(contract.canonical_pdf_provenance_path(root, source))
    records, errors = contract._record_map(manifest)
    if errors:
        return
    previous = dict(data['variants'])
    for variant, record in records.items():
        saved = previous.get(variant, {})
        if (saved.get('build_fingerprint') == record.get('input_fingerprint')
                and saved.get('pdf_sha256') == record.get('output', {}).get('sha256')):
            continue
        if not contract.validate_canonical_pdf_provenance(root, source, variant=variant):
            data['variants'][variant] = record_variant(
                root, source, variant, record, pipeline=manifest['pipeline_inputs'])
    if data['variants'] == previous:
        return
    path = evidence_path(source)
    with NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                            dir=path.parent, delete=False) as stream:
        replacement = Path(stream.name)
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    try:
        replacement.replace(path)
    finally:
        replacement.unlink(missing_ok=True)
