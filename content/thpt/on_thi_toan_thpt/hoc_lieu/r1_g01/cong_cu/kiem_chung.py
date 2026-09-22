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
    for node in soup.select('.tools, .r1-downloads, .zo-variation-caption, a.anchorjs-link'):
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
    for selector, expected in [('math', 985), ('annotation', 985), ('[id]', 107),
                               ('a[href^="#"]', 51), ('.answer-link', 42), ('details', 16),
                               ('table', 30), ('table.variation', 13), ('figure', 10)]:
        counts[selector] = [len(original.select(selector)), len(target.select(selector))]
        checks['count:'+selector] = counts[selector] == [expected, expected]
    counts['img'] = [len(original.select('img')), len(target.select('img'))]
    checks['count:img'] = counts['img'] == [10, 23]
    headings = original.select('h1,h2,h3')
    mapped = [(2 if h.name == 'h1' or h.get('id') == 'cách-học-với-tài-liệu-này' else int(h.name[1])+1,
               norm(h.get_text())) for h in headings[1:]]
    checks['heading_mapping_D08'] = mapped == [(int(h.name[1]), norm(h.get_text())) for h in target.select('h1,h2,h3,h4')]
    checks['single_page_title'] = len(page.select('main h1')) == 1 and norm(page.select_one('h1.title').get_text()) == norm(headings[0].get_text())
    checks['subtitle_preserved'] = norm(page.select_one('#title-block-header .subtitle').get_text()) == 'Dấu đạo hàm, tính đơn điệu và cực trị'
    counts['logical_regions'] = [len(original.select('h1')), 1 + len([h for h in target.select('h2') if h.get('id', h.parent.get('id')) != 'cách-học-với-tài-liệu-này'])]
    checks['eight_logical_regions'] = counts['logical_regions'] == [8, 8]
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
    original_text = visible_text(original)
    old_intro = norm(headings[0].get_text()) + ' Dấu đạo hàm, tính đơn điệu và cực trị ZO Math · Ôn thi Toán THPT 2027 · R1-G01 · Phiên bản 1.1'
    old_guidance = 'Lời giải nằm ở cuối tài liệu, trong các mục có thể mở khi cần. Nút In toàn bộ in cả lời giải; nút In phần học và bài tập ẩn lời giải. Khi học trên màn hình, nhấn vào tên câu hoặc bài để đi đến lời giải tương ứng.'
    new_guidance = 'Tải bản học và bài tập để tự làm; dùng bản đầy đủ khi cần đối chiếu lời giải. Trên màn hình, các liên kết lời giải mở đúng phần tương ứng.'
    old_positioning = 'Học liệu giúp em đọc đúng công thức, bảng biến thiên và đồ thị; dùng dấu đạo hàm để giải thích kết luận về tính đơn điệu và cực trị. Em cần biết tính đạo hàm đa thức, xét dấu biểu thức và nhận biết tính liên tục tại một điểm. Bốn câu hỏi khởi động sẽ giúp em xác định phần cần ôn.'
    new_positioning = 'R1-G01 là gói củng cố kiến thức nền và chẩn đoán lỗi thuộc chương trình Ôn thi Toán THPT 2027. Học liệu giúp em đọc đúng công thức, bảng biến thiên và đồ thị; dùng dấu đạo hàm để giải thích kết luận về tính đơn điệu và cực trị. Em cần biết tính đạo hàm đa thức, xét dấu biểu thức và nhận biết tính liên tục tại một điểm. Bốn câu hỏi khởi động sẽ giúp em xác định phần cần ôn. Bài kiểm tra cuối gói nhằm xác định mức độ em làm chủ những nội dung này; đây không phải là đề mô phỏng cấu trúc đề thi tốt nghiệp THPT.'
    assert original_text.count(old_intro) == 1 and original_text.count(old_guidance) == 1 and original_text.count(old_positioning) == 1, 'Authority V1/V2 text changed'
    projected_text = original_text.replace(old_intro, 'R1-G01 · Bản xem trước · Chưa xuất bản', 1).replace(old_guidance, new_guidance, 1).replace(old_positioning, new_positioning, 1)
    checks['text_sequence_only_approved_V1_V2'] = projected_text == visible_text(target)
    checks['downloads_exact'] = [(x['href'], x.get('download')) for x in target.select('.r1-downloads a')] == [
        ('index_hoc_sinh.pdf', 'R1-G01_hoc_va_bai_tap_v1.2.pdf'),
        ('index.pdf', 'R1-G01_hoc_lieu_day_du_v1.2.pdf')]
    all_ids = [x['id'] for x in page.select('[id]')]
    checks['whole_dom_unique_ids'] = len(all_ids) == len(set(all_ids))
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
