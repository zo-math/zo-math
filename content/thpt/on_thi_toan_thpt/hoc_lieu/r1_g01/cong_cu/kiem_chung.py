"""Read-only Phase 3 preservation check against immutable R1-G01 HTML v1.1.

Run from repository root through scripts/zo_python.py; HTML argument is explicit.
This is not visual acceptance, a mathematical checker, or a publication gate.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[4]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text):
    return ' '.join(text.split())


def visible_text(root):
    soup = BeautifulSoup(str(root), 'html.parser')
    for node in soup.select('math'):
        annotation = node.find('annotation', encoding='application/x-tex')
        node.replace_with(' ZOMATH '+norm(annotation.get_text())+' END ')
    for node in soup.select('.tools, .zo-variation-caption, a.anchorjs-link'):
        node.decompose()
    return norm(soup.get_text(' ', strip=True))


def table_records(root):
    return [
        {'bbt': table.get('data-bbt'),
         'caption': norm(table.caption.get_text()) if table.caption else None,
         'rows': [[norm(cell.get_text(' ', strip=True)) for cell in row.find_all(['th', 'td'], recursive=False)]
                  for row in table.find_all('tr')]}
        for table in root.select('table')
    ]


def check(html):
    history = json.loads((PACKAGE/'_quy_trinh/lich_su/v1_1.json').read_text(encoding='utf-8'))
    source = ROOT/history['source_root']
    original = BeautifulSoup((ROOT/history['authority']).read_text(encoding='utf-8'), 'html.parser')
    page = BeautifulSoup(html.read_text(encoding='utf-8'), 'html.parser')
    target = page.select_one('.r1-g01')
    if target is None:
        raise ValueError('Missing .r1-g01 scope')
    original = original.main
    checks = {}
    actual_source = {p.relative_to(source).as_posix(): sha(p) for p in source.rglob('*') if p.is_file()}
    checks['source_40_hashes'] = actual_source == history['sha256'] and len(actual_source) == 40
    counts = {}
    for selector, expected in [('h1', 8), ('math', 985), ('annotation', 985), ('[id]', 107),
                               ('a[href^="#"]', 51), ('.answer-link', 42), ('details', 16),
                               ('table', 30), ('table.variation', 13), ('figure', 10)]:
        counts[selector] = [len(original.select(selector)), len(target.select(selector))]
        checks['count:'+selector] = counts[selector] == [expected, expected]
    counts['img'] = [len(original.select('img')), len(target.select('img'))]
    checks['count:img'] = counts['img'] == [10, 23]
    maths = lambda root: [(x.get('display', 'inline'), norm(x.find('annotation', encoding='application/x-tex').get_text())) for x in root.select('math')]
    checks['math_sequence_and_tex'] = maths(original) == maths(target)
    ids = lambda root: [x['id'] for x in root.select('[id]')]
    checks['ordered_ids_unique'] = ids(original) == ids(target) and len(set(ids(target))) == 107
    links = lambda root: [(unquote(x['href']), norm(x.get_text())) for x in root.select('a[href^="#"]')]
    checks['ordered_links'] = links(original) == links(target)
    checks['links_resolve'] = all(href[1:] in ids(target) for href, _ in links(target))
    checks['tables_cells_captions_order'] = table_records(original) == table_records(target)
    figures = lambda root: [(x.img['alt'], norm(x.figcaption.get_text())) for x in root.select('figure')]
    checks['figure_alt_caption_order'] = figures(original) == figures(target)
    checks['details_summary_order'] = [norm(x.summary.get_text()) for x in original.select('details')] == [norm(x.summary.get_text()) for x in target.select('details')]
    checks['text_sequence_whitespace_normalized'] = visible_text(original) == visible_text(target)
    legacy_data = json.loads((source/'src/bang_bien_thien.json').read_text(encoding='utf-8'))
    current_data = json.loads((PACKAGE/'du_lieu/bang_bien_thien.json').read_text(encoding='utf-8'))
    content_projection = [
        {key: value for key, value in item.items() if key != 'column_min_widths_mm'}
        for item in current_data
    ]
    checks['json_content_identity'] = content_projection == legacy_data
    checks['variation_layout_contract'] = all(
        isinstance(item.get('column_min_widths_mm', {}), dict)
        and all(str(col).isdigit() and isinstance(value, (int, float)) and not isinstance(value, bool)
                and 8 <= value <= 60
                for col, value in item.get('column_min_widths_mm', {}).items())
        for item in current_data
    )
    graph_names = [f'do_thi_{i:02d}' for i in range(1, 11)]
    checks['graph_vector_triplets_exist'] = all(
        (PACKAGE/'hinh'/f'{name}.{ext}').is_file()
        for name in graph_names for ext in ('tex', 'pdf', 'svg')
    )
    checks['canonical_graph_png_absent'] = not any(
        (PACKAGE/'hinh'/f'{name}.png').exists() for name in graph_names
    )
    checks['html_graphs_use_svg'] = [
        img.get('src') for img in target.select('figure img')
    ] == [f'hinh/{name}.svg' for name in graph_names]
    variation_names = [f'bbt{i:02d}' for i in range(1, 14)]
    checks['variation_vector_triplets_exist'] = all(
        (PACKAGE/'hinh'/f'{name}.{ext}').is_file()
        for name in variation_names for ext in ('tex', 'pdf', 'svg')
    )
    variation_order = ['bbt01', 'bbt02', 'bbt12', 'bbt13', 'bbt03', 'bbt04',
                       'bbt05', 'bbt06', 'bbt07', 'bbt08', 'bbt09', 'bbt10', 'bbt11']
    checks['html_variations_use_svg'] = [
        img.get('src') for img in target.select('.zo-variation-image')
    ] == [f'hinh/{name}.svg' for name in variation_order]
    # Compare literal JSON rows with display cells, respecting the original excluded-column rule.
    data = {x['id']: x for x in current_data}
    for record in table_records(target):
        if not record['bbt']:
            continue
        table = data[record['bbt']]
        expected = [['∥' if i > 0 and j in table.get('excluded_columns', []) else value
                     for j, value in enumerate(row)] for i, row in enumerate(table['rows'])]
        checks['json_cells:'+record['bbt']] = record['rows'] == expected
    checks['intentional_BBT05'] = data['BBT05'].get('intentional_error') is True
    external = sorted({x.get('src', x.get('href', '')) for x in page.select('[src],link[href]')
                       if urlsplit(x.get('src', x.get('href', ''))).netloc})
    # Existing root theme already includes p5; no new HTTP resource is permitted.
    inherited = {'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.js'}
    checks['no_new_http_resources'] = set(external) <= inherited
    checks['package_profile_private'] = 'publication: pending' in (PACKAGE/'_quy_trinh/ho_so/index.yml').read_text(encoding='utf-8')
    return {'passed': all(checks.values()), 'checks': checks, 'counts': counts,
            'external_resources_inherited': external, 'html': html.as_posix(),
            'final_visual_acceptance': 'NOT_RUN'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    args = parser.parse_args()
    try:
        result = check(args.html.resolve())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(0 if result['passed'] else 1)
    except (ValueError, OSError, KeyError, AttributeError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        raise SystemExit(1)
