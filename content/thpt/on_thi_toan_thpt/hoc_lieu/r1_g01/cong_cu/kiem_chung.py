"""Read-only Phase 3 preservation check against immutable R1-G01 HTML v1.1.

Run from repository root through scripts/zo_python.py; HTML argument is explicit.
This is not visual acceptance, a mathematical checker, or a publication gate.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from pypdf import PdfReader
import yaml
from kiem_chung_header_pdf import inspect_pdf

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[4]
CANONICAL_CONTRACT = ROOT / 'content/thpt/on_thi_toan_thpt/_quy_trinh/quy_chuan_goi_qmd.md'

TABLE_CONTRACT = [
    {'id': 'r1-table-t01', 'label': 'Cách học với tài liệu này', 'family': 'R', 'mode': 'fit', 'widths': [16, 50, 34], 'row_header': True},
    {'id': 'r1-table-t02', 'label': 'Học xong, em cần làm được gì?', 'family': 'R', 'mode': 'fit', 'widths': [30, 70], 'row_header': True},
    {'id': 'r1-table-t03', 'label': 'Chọn đúng phần cần ôn', 'family': 'R', 'mode': 'fit', 'widths': [27, 49, 24], 'row_header': True},
    {'id': 'r1-table-t04', 'label': '3.2. Từ đạo hàm đến dấu và chiều biến thiên', 'family': 'R', 'mode': 'scroll', 'widths': [25, 16, 16, 18, 25], 'min_width': '30em', 'row_header': True},
    {'id': 'r1-table-t05', 'label': '4.1. Định lí cực trị dùng điều kiện nào?', 'family': 'R', 'mode': 'scroll', 'widths': [25, 25, 28, 22], 'min_width': '40em', 'row_header': False},
    {'id': 'r1-table-t06', 'label': '5.2. Ba đối tượng cần tách biệt', 'family': 'R', 'mode': 'scroll', 'widths': [30, 24, 23, 23], 'min_width': '36em', 'row_header': True},
    {'id': 'r1-table-t07', 'label': '6.2. Đồ thị của f khác đồ thị của f′', 'family': 'R', 'mode': 'scroll', 'widths': [30, 25, 45], 'min_width': '40em', 'row_header': True},
    {'id': 'r1-table-t08', 'label': '6.5. Bản đồ giới hạn suy luận', 'family': 'R', 'mode': 'scroll', 'widths': [24, 38, 38], 'min_width': '40em', 'row_header': True},
    {'id': 'r1-table-t09', 'label': '7.1. Tách phát biểu thành từng vế', 'family': 'R', 'mode': 'fit', 'widths': [24, 36, 40], 'row_header': True},
    {'id': 'r1-table-t10', 'label': '7.4. Một dòng ghi lỗi có ích', 'family': 'R', 'mode': 'fit', 'widths': [25, 75], 'row_header': True},
    {'id': 'r1-table-t11', 'label': '7.5. Tám lỗi để tự nhận diện', 'family': 'R', 'mode': 'fit', 'widths': [7, 43, 50], 'row_header': True},
    {'id': 'r1-table-t12', 'label': 'Chọn bài tập khắc phục lỗi', 'family': 'R', 'mode': 'scroll', 'widths': [22, 26, 26, 26], 'min_width': '52em', 'row_header': True},
    {'id': 'r1-table-t13', 'label': 'Nhật kí học tập', 'family': 'J', 'mode': 'scroll', 'widths': [31, 69], 'min_width': '38em', 'row_header': True},
    {'id': 'r1-table-t18', 'label': 'Ví dụ giả lập Nhật kí học tập', 'family': 'J', 'mode': 'scroll', 'widths': [31, 69], 'min_width': '42em', 'row_header': True},
    {'id': 'r1-table-t14', 'label': 'Bài luyện tập 07 — Lời giải và phản biện', 'family': 'R', 'mode': 'scroll', 'widths': [6, 12, 37, 45], 'min_width': '44em', 'row_header': True},
    {'id': 'r1-table-t15', 'label': 'Bài kiểm tra 01 — Đáp án và cách chấm 5 điểm', 'family': 'R', 'mode': 'scroll', 'widths': [6, 64, 30], 'min_width': '42em', 'row_header': True},
    {'id': 'r1-table-t16', 'label': 'Bài kiểm tra 03 — Đáp án và cách chấm 4 điểm', 'family': 'R', 'mode': 'fit', 'widths': [6, 14, 80], 'row_header': True},
    {'id': 'r1-table-t17', 'label': 'Đọc kết quả tự kiểm tra', 'family': 'R', 'mode': 'scroll', 'widths': [25, 33, 42], 'min_width': '42em', 'row_header': True},
]
SCROLL_HINT = 'Bảng có thể cuộn ngang. Kéo sang bên hoặc dùng phím mũi tên khi bảng đang được chọn.'
PRACTICE_RULES = ('Dùng các số liệu trong hình có nhãn như dữ kiện chính xác; '
                  'chỉ xét phần tập xác định được đề bài chỉ rõ. Không dùng kết luận '
                  'của một câu như giả thiết của câu khác.')
GUIDANCE_CONTRACT = [
    {'id': 'cach-thuc-hien-su-dung-tai-lieu', 'blocks': [('ul', ['Tải bản học và bài tập để tự làm.', 'Dùng bản đầy đủ khi cần đối chiếu lời giải.', 'Trên màn hình, dùng các liên kết lời giải để mở đúng phần tương ứng.'])]},
    {'id': 'cach-thuc-hien-bat-dau', 'blocks': [('ol', ['Làm bốn câu hỏi khởi động trên giấy.', 'Đối chiếu lời giải rồi dùng bảng chỉ dẫn để ôn đúng phần còn vướng.']), ('p', 'Đọc các mục tiêu để biết mình cần làm được gì.')]},
    {'id': 'cach-thuc-hien-don-dieu', 'blocks': [('ol', ['Trả lời câu hỏi mở đầu bằng lời của em.', 'Đọc định nghĩa và Ví dụ 01, rồi tự làm Câu hỏi tự kiểm tra 01.', 'Khi đối chiếu, kiểm tra xem lập luận đã bao quát mọi cặp điểm trên khoảng xét chưa.'])]},
    {'id': 'cach-thuc-hien-dau-dao-ham', 'blocks': [('ul', ['Đọc giả thiết của định lí trước kết luận.', 'Với Ví dụ 02, đối chiếu dấu đạo hàm, mũi tên trong bảng và đồ thị.', 'Tự làm Câu hỏi tự kiểm tra 02.']), ('p', 'Phần giải thích bằng giới hạn được đặt trong mục đọc thêm.')]},
    {'id': 'cach-thuc-hien-chuoi-bieu-dien', 'blocks': [('ol', ['Với Ví dụ 03, tự tính đạo hàm và xét dấu trước khi xem bảng. Tính giá trị tại các mốc.', 'Lập bảng biến thiên rồi phác đồ thị.', 'Làm Câu hỏi tự kiểm tra 03 để kiểm tra sự phù hợp giữa bảng và hình.'])]},
    {'id': 'cach-thuc-hien-diem-can-xet', 'blocks': [('ul', ['So sánh lần lượt bốn tình huống: đổi dấu, không đổi dấu, không có đạo hàm tại mốc, và mốc không thuộc tập xác định.', 'Mỗi lần kết luận, chỉ rõ tính liên tục và dấu ở hai phía.', 'Cuối mục, tự làm Câu hỏi tự kiểm tra 04.'])]},
    {'id': 'cach-thuc-hien-goi-ten-cuc-tri', 'blocks': [('ol', ['Đọc định nghĩa rồi trở lại Ví dụ 03.', 'Viết riêng ba đối tượng: điểm cực trị của hàm số, giá trị cực trị và điểm cực trị của đồ thị.', 'Hoàn thành Câu hỏi tự kiểm tra 05 để kiểm tra cách dùng thuật ngữ.'])]},
    {'id': 'cach-thuc-hien-doc-nguoc', 'blocks': [('ul', ['Trước mỗi bảng hoặc hình, đọc nhãn và xác định dữ kiện nói về hàm số hay đạo hàm.', 'Với mỗi kết luận, nêu dữ kiện làm căn cứ.', 'Tự làm Câu hỏi tự kiểm tra 06; không dùng tung độ trên đồ thị đạo hàm thay cho giá trị của hàm số.'])]},
    {'id': 'cach-thuc-hien-sua-duoc-loi', 'blocks': [('ol', ['Phân tích phát biểu sai trong Ví dụ 08 và giữ lại phần đúng.', 'Tự làm bài tập khắc phục lỗi mẫu trước khi mở lời giải.', 'Ghi rõ điều đã sửa và câu mới em đã tự làm vào nhật kí học tập.'])]},
    {'id': 'cach-thuc-hien-luyen-tap', 'blocks': [('ul', ['Ở lượt đầu, làm các bài theo ba chặng: Bài 01–04 củng cố chuỗi công thức–dấu–biến thiên–cực trị; Bài 05–06 luyện đọc ngược mà không thêm dữ kiện; Bài 07–08 luyện đánh giá và sửa lỗi.', 'Sau mỗi chặng, ghi lại lỗi còn lặp rồi mới chuyển tiếp.', 'Ghi tập xác định, khoảng và lí do trước khi kết luận.', 'Chỉ mở lời giải ở phần Lời giải và hướng dẫn chấm của bản đầy đủ.'])]},
    {'id': 'cach-thuc-hien-kiem-tra', 'blocks': [('p', 'Thời gian đề xuất: 45 phút · Tổng điểm: 20.'), ('p', 'Làm năm bài trên giấy, ghi cả lập luận và điều kiện áp dụng. Chỉ mở hướng dẫn chấm sau khi hoàn thành.'), ('p', 'Thang điểm này phục vụ tự đánh giá trong học liệu ZO Math.')]},
    {'id': 'cach-thuc-hien-sau-kiem-tra', 'blocks': [('ol', ['Mở hướng dẫn chấm và ghi điểm từng ý.', 'Giữ nguyên bài làm ban đầu để nhận diện chỗ sai, sau đó dùng bảng ở phần Sửa lỗi để chọn bài tập khắc phục.', 'Thể hiện việc sửa lỗi bằng bài làm mới; không chỉ đọc quy trình để xác nhận đã sửa được lỗi.'])]},
    {'id': 'cach-thuc-hien-sua-loi', 'blocks': [('p', 'Mỗi lượt:'), ('ol', ['Giữ bài làm sai ban đầu.', 'Chỉ ra điều kiện hoặc bước suy luận bị bỏ.', 'Viết lại cho đúng.', 'Làm bài tập khắc phục lỗi tương ứng khi chưa mở đáp án.']), ('p', 'Nếu một bài mắc nhiều lỗi, làm các bài tập khắc phục lỗi tương ứng, không chỉ chọn lỗi dễ nhất.')]},
    {'id': 'cach-thuc-hien-on-lai', 'blocks': [('ol', ['Sau khi sửa bài, chọn ngày quay lại và ghi vào nhật kí.', 'Ở buổi ôn, đóng tài liệu trước khi tự nhớ và làm nhiệm vụ mới dành riêng cho lượt Ôn lại.', 'Bài từng sai chỉ dùng để nhớ lại nguyên nhân; không dùng việc làm lại bài đã biết lời giải làm bằng chứng chính cho độ bền.', 'Sau mỗi lượt, đối chiếu tại CP-ON tương ứng, ghi mức hỗ trợ và quyết định giữ lịch, rút ngắn hoặc đi tiếp.'])]},
    {'id': 'cach-thuc-hien-dung-loi-giai', 'blocks': [('p', 'Chỉ mở lời giải của câu đã tự làm. Khi đối chiếu, kiểm tra điều kiện và lí do trước khi đối chiếu đáp số.'), ('p', 'Lời giải và thang chấm sau đây do ZO Math biên soạn.')]},
]

THEORY_CONTRACT = [
    ('Đơn điệu: Định nghĩa hàm số đồng biến và nghịch biến',
     'Hàm số đồng biến trên ZOMATH K END nếu với mọi ZOMATH x_1,x_2 END thuộc ZOMATH K END , khi ZOMATH x_1<x_2 END thì ZOMATH f(x_1)<f(x_2) END . Hàm số nghịch biến trên ZOMATH K END nếu với mọi ZOMATH x_1,x_2 END thuộc ZOMATH K END , khi ZOMATH x_1<x_2 END thì ZOMATH f(x_1)>f(x_2) END .'),
    ('Đơn điệu: Dấu đạo hàm và chiều biến thiên',
     'Nếu ZOMATH f^\\prime(x)>0 END với mọi ZOMATH x END thuộc ZOMATH K END thì ZOMATH f END đồng biến trên ZOMATH K END . Nếu ZOMATH f^\\prime(x)<0 END với mọi ZOMATH x END thuộc ZOMATH K END thì ZOMATH f END nghịch biến trên ZOMATH K END .'),
    ('Đơn điệu: Đạo hàm bằng ZOMATH 0 END tại một số hữu hạn điểm',
     'ZOMATH f^\\prime(x)\\geq 0 END trên ZOMATH K END , và chỉ bằng ZOMATH 0 END tại một số hữu hạn điểm, thì ZOMATH f END đồng biến trên ZOMATH K END . ZOMATH f^\\prime(x)\\leq 0 END trên ZOMATH K END , và chỉ bằng ZOMATH 0 END tại một số hữu hạn điểm, thì ZOMATH f END nghịch biến trên ZOMATH K END .'),
    ('Cực trị: Điều kiện đủ qua dấu đạo hàm',
     'Nếu ZOMATH f^\\prime(x)>0 END trên ZOMATH (a;x_0) END và ZOMATH f^\\prime(x)<0 END trên ZOMATH (x_0;b) END , hàm số đạt cực đại tại ZOMATH x_0 END . Nếu ZOMATH f^\\prime(x)<0 END trên ZOMATH (a;x_0) END và ZOMATH f^\\prime(x)>0 END trên ZOMATH (x_0;b) END , hàm số đạt cực tiểu tại ZOMATH x_0 END .'),
    ('Cực trị: Định nghĩa trong một lân cận',
     'Hàm số đạt cực đại tại ZOMATH x_0 END nếu có số ZOMATH h>0 END sao cho ZOMATH (x_0-h;x_0+h) END nằm trong ZOMATH (a;b) END , và với mọi ZOMATH x END trong khoảng nhỏ này, khác ZOMATH x_0 END , ta có ZOMATH f(x)<f(x_0). END Hàm số đạt cực tiểu tại ZOMATH x_0 END nếu tồn tại một khoảng nhỏ như trên mà với mọi ZOMATH x\\ne x_0 END trong khoảng ấy, ta có ZOMATH f(x)>f(x_0). END'),
]

THEORY_SECTION_IDS = {
    'từ-đi-lên-đến-định-nghĩa',
    'định-lí-và-phạm-vi-áp-dụng',
    'một-số-hữu-hạn-điểm-đạo-hàm-bằng-0',
    'điều-kiện-đủ-qua-dấu-đạo-hàm',
    'định-nghĩa-theo-so-sánh-trong-một-lân-cận',
}

ANSWER_LINK_PAIRS = [
    ('bốn-câu-thử-nền-tn01-đến-tn04', 'lg-khoi-dong'),
    ('dừng-lại-1-d01', 'lg-d01'),
    ('dừng-lại-2-d02', 'lg-d02'),
    ('dừng-lại-3-d03', 'lg-d03'),
    ('dừng-lại-4-d04', 'lg-d04'),
    ('dừng-lại-5-d05', 'lg-d05'),
    ('dừng-lại-6-d06', 'lg-d06'),
    ('câu-sau-chữa-cg01', 'lg-cg01'),
    *[(f'lt{index:02}', f'loi-giai-{index + 1}') for index in range(1, 9)],
    *[(f'kt{index:02}', f'loi-giai-{index + 9}') for index in range(1, 6)],
    *[(f'sc{index:02}', f'lg-sc{index:02}') for index in range(1, 9)],
    *[(f'g01-s-k-e{index:02}', f'lg-g01-s-k-e{index:02}') for index in range(1, 10)],
    *[(f'g01-o{index:02}', f'lg-g01-o{index:02}') for index in range(1, 4)],
    *[(f'g01-s-o-e{index:02}', f'lg-g01-s-o-e{index:02}') for index in range(1, 10)],
]

PHASE3_TASK_IDS = {
    *(f'g01-o{index:02}' for index in range(1, 4)),
    *(f'g01-s-k-e{index:02}' for index in range(1, 10)),
    *(f'g01-s-o-e{index:02}' for index in range(1, 10)),
}


def is_ordered_subsequence(expected, actual):
    iterator = iter(actual)
    return all(any(candidate == item for candidate in iterator) for item in expected)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_historical_source():
    """Verify the immutable v1.1 record while treating its one log as local evidence."""
    verification_path = PACKAGE / '_quy_trinh/lich_su/v1_1_verification_v2.json'
    verification = json.loads(verification_path.read_text(encoding='utf-8'))
    source_manifest = verification.get('source_manifest', {})
    expected_manifest_path = (
        'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/'
        '_quy_trinh/lich_su/v1_1.json'
    )
    manifest_path = ROOT / source_manifest.get('path', '')
    manifest_immutable = (
        verification.get('verification_schema_version') == 2
        and source_manifest.get('path') == expected_manifest_path
        and source_manifest.get('sha256') == 'd521e90aa72797b36712dbdd19239f2ab9f6868b09e937e98426a0a371bee2d3'
        and manifest_path.is_file()
        and sha(manifest_path) == source_manifest.get('sha256')
    )
    history = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_immutable else {}
    optional = verification.get('local_evidence_optional')
    expected_optional_repository_path = (
        '_projects/on_thi_toan_thpt_2027/goi/R1-G01/'
        'kiem_chung/pdf_build.log'
    )
    optional_contract_valid = (
        isinstance(optional, list)
        and len(optional) == 1
        and optional[0] == {
            'repository_path': expected_optional_repository_path,
            'source_manifest_path': 'kiem_chung/pdf_build.log',
            'sha256': 'f8b6343da78ba11b65e7f950a4966ea47e567efcf8d721a382c683ae88c1fd8b',
            'role': 'local_build_diagnostic_log',
        }
        and history.get('sha256', {}).get('kiem_chung/pdf_build.log') == optional[0]['sha256']
    )
    release = verification.get('release_required', {})
    declared = history.get('sha256', {})
    required = {
        path: digest for path, digest in declared.items()
        if optional_contract_valid and path != optional[0]['source_manifest_path']
    }
    contract_valid = (
        manifest_immutable
        and history.get('file_count') == 40
        and source_manifest.get('declared_file_count') == 40
        and optional_contract_valid
        and release.get('derivation') == 'source_manifest.sha256 minus local_evidence_optional'
        and release.get('file_count') == 39
        and len(required) == 39
    )
    source = ROOT / history.get('source_root', '_invalid_history_source_')
    actual = {
        path.relative_to(source).as_posix(): sha(path)
        for path in source.rglob('*') if path.is_file()
    } if source.is_dir() else {}
    if optional_contract_valid:
        actual.pop(optional[0]['source_manifest_path'], None)
    return history, source, {
        'history_v1_1_manifest_immutable': manifest_immutable,
        'history_v1_1_verification_contract': contract_valid,
        'source_39_required_hashes': contract_valid and actual == required,
    }


def norm(text):
    return ' '.join(text.split())


def visible_text(root):
    soup = BeautifulSoup(str(root), 'html.parser')
    for node in soup.select('math'):
        annotation = node.find('annotation', encoding='application/x-tex')
        node.replace_with(' ZOMATH '+norm(annotation.get_text())+' END ')
    for node in soup.select(
        '.tools, .r1-downloads, .r1-section-download-heading, '
        '.r1-section-download-list, .r1-download-support, '
        '#tai-tai-lieu > h2, #tai-tai-lieu > p, '
        '.zo-variation-caption, .r1-table-scroll-hint, a.anchorjs-link, '
        'div.zo-block-title, .r1-unboxed-label, .answer-link, table > caption'
    ):
        node.decompose()
    return norm(soup.get_text(' ', strip=True))


def title_text(root):
    soup = BeautifulSoup(str(root), 'html.parser')
    for node in soup.select('math'):
        annotation = node.find('annotation', encoding='application/x-tex')
        node.replace_with(' ZOMATH '+norm(annotation.get_text())+' END ')
    return norm(soup.get_text(' ', strip=True))


def table_records(root):
    return [
        {'bbt': table.get('data-bbt'),
         'caption': norm(table.caption.get_text()) if table.caption else None,
         'rows': [[norm(cell.get_text(' ', strip=True)) for cell in row.find_all(['th', 'td'], recursive=False)]
                  for row in table.find_all('tr')]}
        for table in root.select('table')
    ]


def derive_projection_boundaries(items):
    """Derive the ordered section boundary chain from a manifest."""
    boundaries = []
    expected_start = None
    for item in items:
        start, end_before = item['start'], item['end-before']
        if expected_start is not None and start != expected_start:
            raise ValueError(f'Non-contiguous section PDF boundary: {start} != {expected_start}')
        boundaries.append(start)
        expected_start = end_before
    return boundaries + ([expected_start] if expected_start is not None else [])


def package_scope(page):
    """Return the single, complete package root emitted inside Quarto's main."""
    main = page.select_one('main#quarto-document-content')
    root = page.select_one('.zo-on-thi-package')
    if main is None or root is None:
        return None
    children = [node for node in main.find_all(recursive=False) if node.name]
    try:
        root_index = children.index(root)
    except ValueError as exc:
        raise ValueError('R1-G01 package root is outside main') from exc
    if children[root_index + 1:]:
        raise ValueError('R1-G01 content escaped the package root')
    required = {'đọc-kết-quả-tự-kiểm-tra', 'nguon', 'tai-tai-lieu'}
    if not required <= {node.get('id') for node in root.select('section[id]')}:
        raise ValueError('R1-G01 package root is incomplete')
    return deepcopy(root)


def check(html):
    history, source, history_checks = verify_historical_source()
    original = BeautifulSoup((ROOT/history['authority']).read_text(encoding='utf-8'), 'html.parser')
    html_text = html.read_text(encoding='utf-8')
    page = BeautifulSoup(html_text, 'html.parser')
    target = package_scope(page)
    if target is None:
        raise ValueError('Missing .zo-on-thi-package scope')
    runtime_target = deepcopy(target)
    runtime_toc = runtime_target.select_one('.lesson-toc')
    runtime_headings = runtime_target.select('#bai-hoc > section.level3 > h3')
    if runtime_toc is not None and not runtime_toc.select('a'):
        line_block = page.new_tag('div', attrs={'class': 'line-block'})
        for heading in runtime_headings:
            line = page.new_tag('div', attrs={'class': 'line'})
            section_id = heading.get('id') or heading.parent.get('id')
            link = page.new_tag('a', href='#'+section_id)
            link.string = heading.get_text()
            line.append(link)
            line_block.append(line)
        runtime_toc.append(line_block)
    original = original.main
    checks = dict(history_checks)
    qmd = (PACKAGE/'index.qmd').read_text(encoding='utf-8')
    front_matter = yaml.safe_load(qmd.split('---', 2)[1])
    registry = yaml.safe_load(
        (PACKAGE/'_quy_trinh/cau_hinh_san_xuat_qmd.yml').read_text(encoding='utf-8')
    )['extensions']['pdf_variants']
    manifest = front_matter.get('r1-section-download-files')
    section_variants = ('bai_hoc', 'luyen_tap', 'kiem_tra', 'sua_loi', 'on_lai', 'loi_giai')
    manifest_fields = {'variant', 'href', 'download', 'title', 'description', 'start', 'end-before', 'view'}
    level2_sections = target.select(':scope > section.level2')
    level2_ids = [section.get('id') for section in level2_sections]
    source_index = level2_ids.index('nguon') if 'nguon' in level2_ids else -1
    projected_sections = level2_sections[1:source_index] if source_index > 0 else []
    projected_ids = [section.get('id') for section in projected_sections]
    projected_titles = {
        section.get('id'): norm(section.find('h2', recursive=False).get_text())
        for section in projected_sections
        if section.get('id') and section.find('h2', recursive=False)
    }
    manifest_shape_valid = (
        isinstance(manifest, list)
        and len(manifest) == len(section_variants)
        and all(isinstance(item, dict) and manifest_fields <= set(item) for item in manifest)
    )
    manifest_boundaries = derive_projection_boundaries(manifest) if manifest_shape_valid else []
    fixture_manifest = [
        {'start': 'fixture-first', 'end-before': 'fixture-second'},
        {'start': 'fixture-second', 'end-before': 'nguon'},
    ]
    fixture_before = derive_projection_boundaries(fixture_manifest)
    fixture_manifest[0]['start'] = 'fixture-renamed'
    fixture_after = derive_projection_boundaries(fixture_manifest)
    checks['section_pdf_manifest_boundary_fixture_derived'] = (
        fixture_before == ['fixture-first', 'fixture-second', 'nguon']
        and fixture_after == ['fixture-renamed', 'fixture-second', 'nguon']
    )
    counts = {}
    for selector, expected in [('math', (985, 1469)), ('annotation', (985, 1469)), ('[id]', (107, 224)),
                               ('a[href^="#"]', (51, 149)), ('.answer-link', (42, 100)), ('details', (16, 52)),
                               ('table', (30, 31)), ('table.variation', 13), ('figure', (10, 26))]:
        target_root = runtime_target if selector == 'a[href^="#"]' else target
        counts[selector] = [len(original.select(selector)), len(target_root.select(selector))]
        expected_counts = list(expected) if isinstance(expected, tuple) else [expected, expected]
        checks['count:'+selector] = counts[selector] == expected_counts
    counts['img'] = [len(original.select('img')), len(target.select('img'))]
    checks['count:img'] = counts['img'] == [10, 28]
    headings = original.select('h1,h2,h3')
    mapped = [(2 if h.name == 'h1' or h.get('id') == 'cách-học-với-tài-liệu-này' else int(h.name[1])+1,
               norm(h.get_text())) for h in headings[1:]]
    projected_headings = []
    section = None
    removed_functional_headings = []
    for level, text in mapped:
        if level == 3:
            section = text
        if level == 4 and (text == 'Thử nghĩ trước' or text.startswith('Câu hỏi tự kiểm tra ')):
            removed_functional_headings.append((section, text))
        else:
            projected_headings.append((level, text))
    checks['prototype_functional_headings_exact'] = removed_functional_headings == [
        ('1. Đơn điệu nói điều gì?', 'Thử nghĩ trước'),
        ('1. Đơn điệu nói điều gì?', 'Câu hỏi tự kiểm tra 01'),
        ('2. Dấu đạo hàm cho phép kết luận gì?', 'Thử nghĩ trước'),
        ('2. Dấu đạo hàm cho phép kết luận gì?', 'Câu hỏi tự kiểm tra 02'),
        ('3. Một chuỗi biểu diễn được dựng thế nào?', 'Thử nghĩ trước'),
        ('3. Một chuỗi biểu diễn được dựng thế nào?', 'Câu hỏi tự kiểm tra 03'),
        ('4. Điều gì xảy ra tại một điểm cần xét?', 'Thử nghĩ trước'),
        ('4. Điều gì xảy ra tại một điểm cần xét?', 'Câu hỏi tự kiểm tra 04'),
        ('5. Cực trị được gọi tên thế nào?', 'Thử nghĩ trước'),
        ('5. Cực trị được gọi tên thế nào?', 'Câu hỏi tự kiểm tra 05'),
        ('6. Có thể đọc ngược đến đâu?', 'Thử nghĩ trước'),
        ('6. Có thể đọc ngược đến đâu?', 'Câu hỏi tự kiểm tra 06'),
        ('7. Làm sao biết mình đã sửa được lỗi?', 'Thử nghĩ trước'),
    ]
    checks['heading_mapping_D08'] = is_ordered_subsequence(projected_headings, [
        (int(h.name[1]), norm(h.get_text())) for h in target.select('h1,h2,h3,h4')
        if h.find_parent(id='tai-tai-lieu') is None
    ])
    checks['single_page_title'] = len(page.select('main h1')) == 1 and norm(page.select_one('h1.title').get_text()) == 'Đơn điệu và cực trị'
    checks['subtitle_preserved'] = norm(page.select_one('#title-block-header .subtitle').get_text()) == 'Dấu đạo hàm, tính đơn điệu và cực trị'
    checks['official_display_identity_exact'] = (
        norm(target.select_one('.r1-status').get_text()) == 'Có thể học'
        and norm(target.select_one(':scope > p').get_text()).startswith(
            'Học liệu “Đơn điệu và cực trị” là gói củng cố kiến thức nền'
        )
        and target.select_one(':scope > p a').get('href').endswith(
            '/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html'
        )
        and norm(target.select_one('.r1-footer').get_text())
        == 'ZO Math · Đơn điệu và cực trị · Phiên bản 1.3'
        and norm(target.select_one('#tai-tai-lieu > h2').get_text()) == 'Tải PDF'
        and 'R1-G01' not in norm(target.select_one('.r1-footer').get_text())
    )
    navigation_suffix = 'content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html'
    sidebar_links = [
        link for link in page.select('#quarto-sidebar a[href]')
        if urlsplit(link['href']).path.replace('\\', '/').endswith(navigation_suffix)
    ]
    breadcrumb_links = [
        link for link in page.select('.quarto-page-breadcrumbs a[href]')
        if urlsplit(link['href']).path.replace('\\', '/').endswith(navigation_suffix)
    ]
    official_title = 'Đơn điệu và cực trị'
    checks['raw_html_no_js_navigation_identity_exact'] = (
        len(sidebar_links) == 1 and len(breadcrumb_links) == 1
        and norm(sidebar_links[0].get_text()) == official_title
        and norm(breadcrumb_links[0].get_text()) == official_title
        and all('R1-G01' not in norm(link.get_text()) for link in sidebar_links + breadcrumb_links)
    )
    counts['logical_regions'] = [len(original.select('h1')), 1 + len([h for h in target.select('h2') if h.get('id', h.parent.get('id')) != 'cách-học-với-tài-liệu-này'])]
    checks['static_regions_plus_download_exact'] = counts['logical_regions'] == [8, 9]
    maths = lambda root: [(x.get('display', 'inline'), norm(x.find('annotation', encoding='application/x-tex').get_text())) for x in root.select('math')]
    def maths_outside_theory(root):
        result = []
        for node in root.select('math'):
            heading = node.find_previous(['h3', 'h4'])
            heading_id = heading.get('id', heading.parent.get('id')) if heading is not None else None
            if heading_id in THEORY_SECTION_IDS:
                continue
            result.append((node.get('display', 'inline'),
                           norm(node.find('annotation', encoding='application/x-tex').get_text())))
        return result
    projected_maths = maths_outside_theory(original)
    assert projected_maths[223] == ('inline', 'f^\\prime(x)>0'), 'Approved Mục 6 math anchor changed'
    assert projected_maths[322] == ('inline', '2'), 'Approved Mục 7 math anchor changed'
    projected_maths[322:322] = [('inline', 'g'), ('inline', 'g^\\prime')]
    projected_maths[223:223] = [('inline', 'f'), ('inline', 'f^\\prime')]
    checks['math_sequence_and_tex'] = is_ordered_subsequence(projected_maths, maths_outside_theory(target))
    ids = lambda root: [x['id'] for x in root.select('[id]')]
    target_ids = ids(target)
    guidance_ids = [item['id'] for item in GUIDANCE_CONTRACT]
    navigation_ids = {'tai-tai-lieu', 'r1-support-title'}
    legacy_target_ids = [value for value in target_ids
                         if not value.startswith('r1-table-t')
                         and not value.startswith('lg-')
                         and value not in guidance_ids and value not in navigation_ids]
    expected_table_ids = []
    for spec in TABLE_CONTRACT:
        if spec['mode'] == 'scroll':
            expected_table_ids.append(spec['id']+'-hint')
        expected_table_ids.append(spec['id'])
    checks['ordered_ids_unique'] = (
        is_ordered_subsequence(ids(original), legacy_target_ids)
        and [value for value in target_ids if value.startswith('r1-table-t')] == expected_table_ids
        and [value for value in target_ids if value in guidance_ids] == guidance_ids
        and PHASE3_TASK_IDS <= set(target_ids)
        and len(set(target_ids)) == 224
    )
    links = lambda root: [(unquote(x['href']), norm(x.get_text())) for x in root.select('a[href^="#"]')]
    checks['links_resolve'] = all(href[1:] in ids(target) for href, _ in links(runtime_target))

    answer_pair_records = []
    answer_pair_contract_ok = len(ANSWER_LINK_PAIRS) == 50
    for source_id, solution_id in ANSWER_LINK_PAIRS:
        source_node = target.find(id=source_id)
        solution_node = target.find(id=solution_id)
        forward = source_node.select('.answer-link') if source_node else []
        reverse = solution_node.select('.answer-link') if solution_node else []
        record = (
            source_id,
            solution_id,
            [(norm(item.get_text()), item.select_one('a').get('href')) for item in forward],
            [(norm(item.get_text()), item.select_one('a').get('href')) for item in reverse],
        )
        answer_pair_records.append(record)
        answer_pair_contract_ok &= (
            len(forward) == 1
            and len(reverse) == 1
            and record[2] == [('Xem lời giải', '#'+solution_id)]
            and record[3] == [('Xem đề bài', '#'+source_id)]
        )
    checks['ordered_links'] = answer_pair_contract_ok
    checks['answer_link_pairs_exact'] = answer_pair_contract_ok

    answer_links = target.select('.answer-link')
    answer_links_at_end = len(answer_links) == 100
    for link in answer_links:
        label = norm(link.get_text())
        if label == 'Xem lời giải':
            container = link.find_parent(class_='zo-learning-task')
        else:
            container = link.find_parent(class_='r1-solution-item') or link.find_parent(class_='zo-block-body')
        if container is None:
            container = link.find_parent('section')
        element_children = [child for child in container.children if getattr(child, 'name', None)]
        answer_links_at_end &= bool(element_children and element_children[-1] is link)
    checks['answer_links_at_block_end'] = answer_links_at_end
    projected_table_records = table_records(original)
    for record in projected_table_records:
        if record['bbt'] and record['caption'] and not record['caption'].endswith('.'):
            record['caption'] += '.'
    target_table_records = table_records(target)
    checks['tables_cells_captions_order'] = (
        [record for record in projected_table_records if record['bbt']]
        == [record for record in target_table_records if record['bbt']]
        and len(target_table_records) == 31
    )
    wrappers = target.select('div.r1-table')
    ordinary_tables = [wrapper.find('table', recursive=False) for wrapper in wrappers]
    checks['ordinary_table_inventory_exact'] = (
        len(ordinary_tables) == 18 and len(wrappers) == 18 and all(wrappers)
        and len(target.select('table.variation')) == 13
    )
    table_contract_ok = len(ordinary_tables) == len(TABLE_CONTRACT)
    row_scope_ok = table_contract_ok
    header_scope_ok = table_contract_ok
    accessible_names_ok = table_contract_ok
    scroll_wrappers_ok = table_contract_ok
    for spec, table, wrapper in zip(TABLE_CONTRACT, ordinary_tables, wrappers):
        linked_navigation_table = bool(table.select('a[href^="#"]'))
        classes = set(wrapper.get('class', []))
        cols = table.select(':scope > colgroup > col')
        rendered_widths = []
        for col in cols:
            match = re.search(r'width:\s*([0-9.]+)%', col.get('style', ''))
            rendered_widths.append(float(match.group(1)) if match else None)
        table_contract_ok &= (
            wrapper.get('id') == spec['id']
            and wrapper.get('data-r1-table') == spec['id'][-3:].upper()
            and wrapper.get('data-family') == spec['family']
            and wrapper.get('data-responsive') == spec['mode']
            and wrapper.get('data-col-widths') == ','.join(map(str, spec['widths']))
            and wrapper.get('data-row-header') == str(spec['row_header']).lower()
            and 'r1-table-family-'+spec['family'].lower() in classes
            and 'r1-table-'+('fit' if spec['mode'] == 'fit' else 'scroll-x') in classes
            and (
                linked_navigation_table
                or (
                    len(rendered_widths) == len(spec['widths'])
                    and all(actual is not None and abs(actual-expected) <= 0.1
                            for actual, expected in zip(rendered_widths, spec['widths']))
                )
            )
            and wrapper.get('data-min-width') == spec.get('min_width')
        )
        header_scope_ok &= all(
            cell.get('scope') == 'col' or linked_navigation_table
            for cell in table.select('thead th')
        )
        body_rows = table.select('tbody tr')
        if spec['row_header']:
            row_scope_ok &= all(
                (
                    row.find(['th', 'td'], recursive=False).name == 'th'
                    and row.find(['th', 'td'], recursive=False).get('scope') == 'row'
                )
                or linked_navigation_table
                for row in body_rows
            )
        else:
            row_scope_ok &= all(row.find(['th', 'td'], recursive=False).name == 'td'
                                for row in body_rows)
        accessible_names_ok &= (
            table.get('aria-label') == spec['label']
            or (linked_navigation_table and wrapper.get('aria-label') == spec['label'])
        )
        hint = target.select_one('#'+spec['id']+'-hint')
        if spec['mode'] == 'scroll':
            scroll_wrappers_ok &= (
                wrapper.get('role') == 'region'
                and wrapper.get('aria-label') == spec['label']
                and wrapper.get('tabindex') == '0'
                and wrapper.get('aria-describedby') == spec['id']+'-hint'
                and hint is not None and hint.has_attr('hidden') and norm(hint.get_text()) == SCROLL_HINT
            )
        else:
            scroll_wrappers_ok &= (
                not wrapper.has_attr('role') and not wrapper.has_attr('tabindex')
                and not wrapper.has_attr('aria-describedby') and hint is None
            )
    checks['ordinary_table_contract_exact'] = table_contract_ok
    checks['ordinary_table_header_scope_exact'] = header_scope_ok
    checks['ordinary_table_row_headers_exact'] = row_scope_ok
    checks['ordinary_table_accessible_names_exact'] = accessible_names_ok
    checks['ordinary_table_scroll_wrappers_exact'] = scroll_wrappers_ok
    checks['ordinary_table_families_exact'] = (
        len(target.select('.r1-table-family-r')) == 16
        and len(target.select('.r1-table-family-j')) == 2
        and [x.get('id') for x in target.select('.r1-table-fit')]
        == [x['id'] for x in TABLE_CONTRACT if x['mode'] == 'fit']
        and [x.get('id') for x in target.select('.r1-table-scroll-x')]
        == [x['id'] for x in TABLE_CONTRACT if x['mode'] == 'scroll']
    )
    figures = lambda root: [
        (x.img['alt'], norm(x.figcaption.get_text()))
        for x in root.select('figure:not(.zo-variation-asset)')
    ]
    checks['figure_alt_caption_order'] = (
        is_ordered_subsequence(figures(original), figures(target))
        and len(figures(target)) == 13
    )
    checks['details_summary_order'] = (
        is_ordered_subsequence(
            [norm(x.summary.get_text()) for x in original.select('details')],
            [norm(x.summary.get_text()) for x in target.select('details:not(.r1-guidance)')],
        )
    )
    guidance = target.select('details.r1-details.r1-guidance')
    checks['details_gray_mapping_exact'] = (
        len(target.select('details.r1-details.zo-block.zo-block-gray')) == 52
        and not target.select('details.r1-details.zo-block-yellow, details.r1-details.zo-block-red')
        and len(guidance) == 15
        and len(target.select('details.r1-details.r1-guidance.zo-learning-guidance')) == 15
        and len(target.select('details.r1-details.r1-solution.zo-learning-solution')) == 36
        and len(target.select(
            'details.r1-details.zo-learning-guidance > summary.zo-block-title, '
            'details.r1-details.zo-learning-solution > summary.zo-block-title'
        )) == 51
        and all(norm(x.summary.get_text()) == 'Cách thực hiện' and not x.has_attr('open') for x in guidance)
        and [norm(x.summary.get_text()) for x in target.select('details.zo-learning-context-note')]
        == ['Đọc thêm — Giải thích bằng định nghĩa đạo hàm']
    )
    guidance_records = []
    for details in guidance:
        body = details.select_one(':scope > .zo-block-body')
        blocks = []
        for block in body.find_all(recursive=False):
            if block.name in ('ul', 'ol'):
                blocks.append((block.name, [norm(item.get_text())
                                           for item in block.find_all('li', recursive=False)]))
            elif block.name == 'p':
                blocks.append(('p', norm(block.get_text(' ', strip=True))))
            else:
                blocks.append((block.name, norm(block.get_text(' ', strip=True))))
        guidance_records.append({'id': details.get('id'), 'blocks': blocks})
    direct_bodies = [details.select_one(':scope > .zo-block-body') for details in guidance]
    counts['guidance_structure'] = {
        'blocks': len(guidance),
        'unordered_list_elements': sum(len(body.find_all('ul', recursive=False)) for body in direct_bodies),
        'ordered_list_elements': sum(len(body.find_all('ol', recursive=False)) for body in direct_bodies),
        'paragraph_elements': sum(len(body.find_all('p', recursive=False)) for body in direct_bodies),
        'blocks_with_unordered_lists': sum(bool(body.find('ul', recursive=False)) for body in direct_bodies),
        'blocks_with_ordered_lists': sum(bool(body.find('ol', recursive=False)) for body in direct_bodies),
        'blocks_without_lists': sum(not body.find(['ul', 'ol'], recursive=False) for body in direct_bodies),
    }
    checks['guidance_contract_by_id_exact'] = (
        guidance_records == GUIDANCE_CONTRACT
        and len(guidance_records) == len(GUIDANCE_CONTRACT)
    )
    checks['guidance_structure_counts_exact'] = counts['guidance_structure'] == {
        'blocks': 15,
        'unordered_list_elements': 5,
        'ordered_list_elements': 8,
        'paragraph_elements': 9,
        'blocks_with_unordered_lists': 5,
        'blocks_with_ordered_lists': 8,
        'blocks_without_lists': 2,
    }
    practice = target.select_one('section#phieu-luyen')
    practice_children = practice.find_all(recursive=False) if practice else []
    practice_guidance = target.select_one('#cach-thuc-hien-luyen-tap')
    checks['practice_rules_location_exact'] = (
        len(practice_children) >= 3
        and practice_children[0].name == 'h2'
        and practice_children[1].name == 'p'
        and norm(practice_children[1].get_text(' ', strip=True)) == PRACTICE_RULES
        and practice_children[2] is practice_guidance
        and PRACTICE_RULES not in norm(practice_guidance.get_text(' ', strip=True))
    )
    pdf_texts = {}
    pdf_pages = {}
    pdf_links = {}
    pdf_top_outlines = {}
    pdf_names = (
        'index.pdf', 'index_hoc_sinh.pdf',
        *([item['href'] for item in manifest] if manifest_shape_valid else []),
    )
    for name in pdf_names:
        pdf = PdfReader(PACKAGE/name)
        pdf_pages[name] = len(pdf.pages)
        pdf_texts[name] = norm(' '.join(page.extract_text() or '' for page in pdf.pages))
        pdf_top_outlines[name] = [
            str(item.get('/Title')) for item in pdf.outline if isinstance(item, dict)
        ]
        actions = []
        for pdf_page in pdf.pages:
            for annotation in pdf_page.get('/Annots', []) or []:
                action = annotation.get_object().get('/A')
                if action:
                    actions.append((str(action.get('/S')), unquote(str(action.get('/URI', '')))))
        pdf_links[name] = actions
    canonical_pdf_pages = {
        'index.pdf': 57,
        'index_hoc_sinh.pdf': 42,
        'index_bai_hoc.pdf': 22,
        'index_luyen_tap.pdf': 8,
        'index_kiem_tra.pdf': 5,
        'index_sua_loi.pdf': 9,
        'index_on_lai.pdf': 10,
        'index_loi_giai.pdf': 17,
    }
    checks['pdf_page_counts_canonical_exact'] = pdf_pages == canonical_pdf_pages
    checks['download_page_metadata_canonical_exact'] = {
        item['href']: item.get('pages')
        for item in front_matter.get('r1-download-files', [])
    } == {
        'index_hoc_sinh.pdf': canonical_pdf_pages['index_hoc_sinh.pdf'],
        'index.pdf': canonical_pdf_pages['index.pdf'],
    }
    def guidance_content_present(text, contracts):
        return all(
            all(
                (content in text if kind == 'p' else all(item in text for item in content))
                for kind, content in contract['blocks']
            )
            for contract in contracts
        )
    checks['pdf_guidance_flattened_exact'] = (
        pdf_texts['index.pdf'].count('Cách thực hiện') == 15
        and pdf_texts['index_hoc_sinh.pdf'].count('Cách thực hiện') == 14
        and guidance_content_present(pdf_texts['index.pdf'], GUIDANCE_CONTRACT)
        and guidance_content_present(pdf_texts['index_hoc_sinh.pdf'], GUIDANCE_CONTRACT[:-1])
    )
    checks['student_solution_filter_exact'] = not any(
        marker in pdf_texts['index_hoc_sinh.pdf']
        for marker in ('Xem lời giải', 'Lời giải và phản biện', 'Đáp án và cách chấm')
    )
    allowed_package_code_counts = {
        'index.pdf': 3,
        'index_hoc_sinh.pdf': 3,
        'index_bai_hoc.pdf': 0,
        'index_luyen_tap.pdf': 0,
        'index_kiem_tra.pdf': 0,
        'index_sua_loi.pdf': 0,
        'index_on_lai.pdf': 3,
        'index_loi_giai.pdf': 0,
    }
    checks['pdf_package_identity_exact'] = all(
        all(marker in pdf_texts[name] for marker in (
            'Phiên bản ứng viên v1.3', 'Kết thúc học liệu',
            'Đơn điệu và cực trị',
            'Trở lại gói học liệu trực tuyến', 'Bảo trợ ZO Math',
            'Vietcombank', '0601000137768', 'Nguyễn Tấn Nhựt',
        ))
        for name in ('index.pdf', 'index_hoc_sinh.pdf')
    ) and all(
        pdf_texts[name].count('R1-G01') == expected
        for name, expected in allowed_package_code_counts.items()
    )
    resources = front_matter.get('resources', [])
    checks['section_pdf_manifest_exact'] = (
        manifest_shape_valid
        and tuple(item['variant'] for item in manifest) == section_variants
        and manifest_boundaries == projected_ids + ['nguon']
        and len({item['href'] for item in manifest}) == len(manifest)
        and len({item['download'] for item in manifest}) == len(manifest)
        and len({item['view'] for item in manifest}) == len(manifest)
        and all(
            re.fullmatch(r'index_[a-z0-9_]+\.pdf', item['href'])
            and Path(item['href']).name == item['href']
            and Path(item['download']).name == item['download']
            and all(isinstance(item[field], str) and item[field].strip() for field in manifest_fields)
            for item in manifest
        )
    )
    checks['section_pdf_registry_matches_manifest'] = (
        manifest_shape_valid
        and all(
            item['variant'] in registry
            and registry[item['variant']].get('output') == item['href']
            and registry[item['variant']].get('include_support') is False
            for item in manifest
        )
        and len({item['href'] for item in manifest}) == 6
        and all(item['href'] in resources for item in manifest)
        and {'index.pdf', 'index_hoc_sinh.pdf'} <= set(resources)
    )
    common_markers = (
        'Phiên bản ứng viên v1.3', 'Đơn điệu và cực trị',
        'Cách học với tài liệu này', 'Nguồn đối chiếu',
        'Kết thúc học liệu', 'Trở lại gói học liệu trực tuyến',
    )
    canonical_url = registry['full']['metadata']['zo-pdf-branding']['canonical-url']
    expected_external_labels = {
        'bai_hoc': 8,
        'luyen_tap': 14,
        'kiem_tra': 7,
        'sua_loi': 27,
        'on_lai': 12,
        'loi_giai': 50,
    }
    section_pdf_ok = True
    for item in manifest if manifest_shape_valid else []:
        name = item['href']
        text = pdf_texts[name]
        externalized = [uri for action, uri in pdf_links[name]
                        if action == '/URI' and '?r1-view=' in uri]
        section_pdf_ok &= (
            pdf_pages[name] > 0
            and all(marker in text for marker in common_markers)
            and pdf_top_outlines[name] == [
                'Cách học với tài liệu này', projected_titles[item['start']], 'Nguồn đối chiếu'
            ]
            and (
                item['variant'] not in {'luyen_tap', 'kiem_tra'}
                or not any(marker in text for marker in ('Lời giải và phản biện', 'Đáp án và cách chấm'))
            )
            and all(marker not in text for marker in ('Tải PDF', 'Bảo trợ ZO Math', 'Số tài khoản'))
            and all(uri.startswith(canonical_url + '?r1-view=') and '#' in uri for uri in externalized)
            # One logical PDF link may produce several annotation rectangles when it wraps;
            # table links stay visibly labelled by their cells and do not receive the suffix.
            and text.count('(mở trên trang học liệu)') == expected_external_labels[item['variant']]
        )
    checks['section_pdf_envelope_and_scope_exact'] = bool(section_pdf_ok)
    pause_tasks = target.select('#bai-hoc .zo-learning-task.zo-learning-task--pause')
    think_first_tasks = target.select('#bai-hoc .zo-learning-task.zo-learning-task--pause[id^="thử-nghĩ-trước"]')
    checks['canonical_lesson_roles_exact'] = (
        len(pause_tasks) == 15
        and all(task.find_parent(id='bai-hoc') is not None for task in pause_tasks)
        and len(think_first_tasks) == 7
        and all(
            task.select_one(':scope > p:first-child > .r1-task-label')
            and norm(task.select_one(':scope > p:first-child > .r1-task-label').get_text()) == 'Thử nghĩ trước'
            for task in think_first_tasks
        )
        and len(target.select('#bai-hoc .zo-learning-example')) == 10
        and len(target.select('#bai-hoc .zo-block-red')) == 5
        and not target.select('#bai-hoc div.zo-block-gray')
        and [norm(x.get_text()) for x in target.select('#bai-hoc .r1-unboxed-label')]
        == [
            'Không đảo định lí thành dấu nghiêm ngặt.',
            'Điểm không thuộc tập xác định.',
            'Trình tự xét một mốc.',
            'Ý nghĩa của “cục bộ”.',
            'Phân biệt dữ kiện về đạo hàm và chiều biến thiên.',
            'Đánh giá từng kết luận từ giả thiết đã cho.',
            'Một dòng ghi lỗi có ích.',
        ]
        and len(target.select('#bai-hoc details.zo-learning-context-note')) == 1
        and len(target.select('#bai-hoc details.zo-learning-guidance')) == 8
        and len(target.select('#cách-học-với-tài-liệu-này details.zo-learning-guidance')) == 1
        and [norm(x.get_text()) for x in target.select('.r1-example-label')]
        == [
            'Ví dụ 05 — Đạo hàm đang tăng nhưng hàm số đang giảm.',
            'Ví dụ 06:',
            'Ví dụ 07',
        ]
        and [norm(x.get_text()) for x in target.select('h4.r1-example-heading')]
        == ['1.2. Ví dụ 01 — Chứng minh mà chưa dùng đạo hàm']
    )
    item_tasks = target.select('section.zo-learning-task.zo-learning-task--item')
    item_task_ids = [task.get('id') for task in item_tasks]
    expected_item_task_ids = (
        [f'lt{index:02d}' for index in range(1, 9)]
        + [f'kt{index:02d}' for index in range(1, 6)]
        + [f'g01-s-k-e{index:02d}' for index in range(1, 10)]
        + [f'sc{index:02d}' for index in range(1, 9)]
        + [f'g01-o{index:02d}' for index in range(1, 4)]
        + [f'g01-s-o-e{index:02d}' for index in range(1, 10)]
    )
    checks['canonical_assessment_task_roles_exact'] = (
        len(item_tasks) == 42
        and item_task_ids == expected_item_task_ids
        and all(task.name == 'section' for task in item_tasks)
    )
    checks['guidance_title_color_matches_lesson_toc_exact'] = all(
        fragment in (ROOT/'assets/css/zo_on_thi_learning_package.css').read_text(encoding='utf-8')
        for fragment in (
            '.zo-on-thi-package .r1-section-toc > summary,',
            '.zo-on-thi-package details.zo-learning-guidance > summary { color: var(--r1-muted); }',
        )
    )
    kickoff = target.select_one('#bốn-câu-thử-nền-tn01-đến-tn04')
    kickoff_task = kickoff.select_one(':scope > .zo-learning-task.zo-learning-task--pause') if kickoff else None
    kickoff_children = [child for child in kickoff.children if getattr(child, 'name', None)] if kickoff else []
    kickoff_task_children = [child for child in kickoff_task.children if getattr(child, 'name', None)] if kickoff_task else []
    checks['kickoff_questions_structure_exact'] = (
        kickoff is not None
        and [child.name for child in kickoff_children] == ['h4', 'p', 'div']
        and norm(kickoff_children[0].get_text()) == 'Câu hỏi khởi động'
        and norm(kickoff_children[1].get_text())
        == 'Hãy thử trước khi đọc đáp án trong mục “Lời giải các câu hỏi và bài tập trong bài học” ở phần Lời giải cuối tài liệu. Không cần tính điểm; câu nào chưa làm được sẽ chỉ ra phần cần ôn nhanh.'
        and [child.name for child in kickoff_task_children] == ['ul', 'div']
        and len(kickoff_task.select(':scope > ul > li')) == 4
        and [norm(item.select_one('strong').get_text()) for item in kickoff_task.select(':scope > ul > li')]
        == [f'Câu hỏi khởi động {index:02}.' for index in range(1, 5)]
        and kickoff_task_children[-1].get('class') == ['answer-link']
        and kickoff_task_children[-1].select_one('a').get('href') == '#lg-khoi-dong'
    )
    self_check_tasks = [target.select_one(f'#dừng-lại-{index}-d{index:02d}') for index in range(1, 7)]
    checks['self_check_questions_structure_exact'] = (
        all(task is not None for task in self_check_tasks)
        and all(
            set(('r1-task', 'zo-learning-task', 'zo-learning-task--pause')).issubset(task.get('class', []))
            and task.select_one(':scope > p:first-child > .r1-task-label') is not None
            and norm(task.select_one(':scope > p:first-child > .r1-task-label').get_text())
            == f'Câu hỏi tự kiểm tra {index:02d}'
            and task.select_one(':scope > .answer-link:last-child a') is not None
            and task.select_one(':scope > .answer-link:last-child a').get('href') == f'#lg-d{index:02d}'
            for index, task in enumerate(self_check_tasks, 1)
        )
        and not target.select('h4[id^="dừng-lại-"]')
    )
    theory_blocks = target.select('#bai-hoc div.zo-block.zo-block-red')
    checks['theory_contract_exact'] = [
        (title_text(block.select_one(':scope > .zo-block-title')), visible_text(block))
        for block in theory_blocks
    ] == THEORY_CONTRACT
    source_notes = target.select('span.zo-source-note')
    checks['source_notes_canonical_exact'] = (
        len(source_notes) == 10
        and all(
            norm(note.get_text()).startswith('Nguồn đối chiếu:')
            and norm(note.get_text()).endswith('.')
            and 'Sách giáo khoa Toán 12' in norm(note.get_text())
            and 'SGK' not in norm(note.get_text())
            and ' tr.' not in norm(note.get_text())
            and ' Bài ' not in norm(note.get_text())
            and note.parent is not None and note.parent.name == 'p'
            and [child for child in note.parent.children if getattr(child, 'name', None)][-1] is note
            for note in source_notes
        )
    )
    checks['lesson_toc_generated_exact'] = [
        (unquote(x['href']), norm(x.get_text())) for x in runtime_target.select('.lesson-toc .line-block a')
    ] == [
        ('#'+h.get('id', h.parent.get('id')), norm(h.get_text()))
        for h in runtime_target.select('#bai-hoc > section.level3 > h3')
    ] and len(runtime_target.select('.lesson-toc .line-block a')) == 9
    original_text = visible_text(original)
    old_intro = norm(headings[0].get_text()) + ' Dấu đạo hàm, tính đơn điệu và cực trị ZO Math · Ôn thi Toán THPT 2027 · R1-G01 · Phiên bản 1.1'
    old_guidance = 'Lời giải nằm ở cuối tài liệu, trong các mục có thể mở khi cần. Nút In toàn bộ in cả lời giải; nút In phần học và bài tập ẩn lời giải. Khi học trên màn hình, nhấn vào tên câu hoặc bài để đi đến lời giải tương ứng.'
    new_guidance = 'Tải bản học và bài tập để tự làm. Dùng bản đầy đủ khi cần đối chiếu lời giải. Trên màn hình, dùng các liên kết lời giải để mở đúng phần tương ứng.'
    old_positioning = 'Học liệu giúp em đọc đúng công thức, bảng biến thiên và đồ thị; dùng dấu đạo hàm để giải thích kết luận về tính đơn điệu và cực trị. Em cần biết tính đạo hàm đa thức, xét dấu biểu thức và nhận biết tính liên tục tại một điểm. Bốn câu hỏi khởi động sẽ giúp em xác định phần cần ôn.'
    new_positioning = 'Học liệu “Đơn điệu và cực trị” là gói củng cố kiến thức nền và chẩn đoán lỗi thuộc chương trình Ôn thi Toán THPT 2027 . Học liệu giúp em đọc đúng công thức, bảng biến thiên và đồ thị; dùng dấu đạo hàm để giải thích kết luận về tính đơn điệu và cực trị. Em cần biết tính đạo hàm đa thức, xét dấu biểu thức và nhận biết tính liên tục tại một điểm. Bốn câu hỏi khởi động sẽ giúp em xác định phần cần ôn. Bài kiểm tra cuối gói nhằm xác định mức độ em làm chủ những nội dung này; đây không phải là đề mô phỏng cấu trúc đề thi tốt nghiệp THPT.'
    assert original_text.count(old_intro) == 1 and original_text.count(old_guidance) == 1 and original_text.count(old_positioning) == 1, 'Authority V1/V2 text changed'
    projected_text = original_text.replace(old_intro, 'Có thể học', 1).replace(old_guidance, new_guidance, 1).replace(old_positioning, new_positioning, 1)
    approved_editorial_edits = [
        (
            '6. Có thể đọc ngược đến đâu? Cách thực hiện.',
            '6. Có thể đọc ngược đến đâu? Ở Mục 5, em đã tập gọi đúng đối tượng cực trị. Bây giờ cần kiểm tra thêm một việc: từ bảng, hình hoặc đạo hàm đã cho, ta thực sự biết được bao nhiêu về những đối tượng ấy? Cách thực hiện.',
        ),
        (
            'Hai câu hỏi này buộc ta tách chiều biến thiên khỏi dấu của giá trị, đồng thời đọc đúng đối tượng được biểu diễn. 6.1.',
            'Hai câu hỏi này buộc ta tách chiều biến thiên khỏi dấu của giá trị, đồng thời đọc đúng đối tượng được biểu diễn. Trong cả Mục 6, mỗi lần đọc ngược, hãy dừng ở ba câu hỏi: Dữ kiện đang nói về ZOMATH f END , ZOMATH f^\\prime END hay chỉ về chiều biến thiên? Kết luận nào theo trực tiếp từ dữ kiện ấy? Muốn kết luận thêm thì còn thiếu giả thiết hoặc giá trị nào? 6.1.',
        ),
        (
            '6.3. Cùng bảng tóm tắt không có nghĩa cùng công thức Xét hai hàm số trong Ví dụ 06:',
            '6.3. Cùng bảng tóm tắt không có nghĩa cùng công thức Cùng bảng tóm tắt. Xét hai hàm số trong Ví dụ 06:',
        ),
        (
            'Cũng cần phân biệt “biết dấu của đạo hàm” với “biết chính xác hàm đạo hàm”.',
            'Biết chính xác đạo hàm vẫn chưa đủ biết mọi giá trị của hàm số. Cũng cần phân biệt “biết dấu của đạo hàm” với “biết chính xác hàm đạo hàm”.',
        ),
        (
            'Kí hiệu hợp không tự làm mọi phát biểu sai. Ví dụ,',
            'Đừng thay lỗi “luôn gộp được” bằng một quy tắc sai khác là “hợp các khoảng luôn sai”. Kí hiệu hợp không tự làm mọi phát biểu sai. Ví dụ,',
        ),
        (
            'Mục này hướng dẫn cách sửa lỗi đầy đủ, không chỉ đổi nhãn “sai” thành “đúng”. 7.1.',
            'Mục này hướng dẫn cách sửa lỗi đầy đủ, không chỉ đổi nhãn “sai” thành “đúng”. Mục 6 giúp em kiểm tra một kết luận có vượt quá dữ kiện hay không. Mục 7 dùng chính cách kiểm tra ấy để tách từng vế của một phát biểu, giữ phần đúng và sửa đúng chỗ sai. 7.1.',
        ),
        (
            'Chưa cho giá trị nào của ZOMATH g END . Hãy tự làm bốn việc: Lập bảng dấu',
            'Chưa cho giá trị nào của ZOMATH g END . Hãy tự làm bốn việc: Lượt 1 — Xét dấu và cực trị Lập bảng dấu',
        ),
        (
            'Xác định mốc nào là điểm cực trị, mốc nào không; nêu lí do. Cho biết có tính được giá trị cực trị chỉ từ những dữ kiện trên không.',
            'Xác định mốc nào là điểm cực trị, mốc nào không; nêu lí do. Lượt 2 — Kiểm tra giới hạn của dữ kiện Chưa cho giá trị nào của ZOMATH g END . Có tính được giá trị cực trị chỉ từ công thức ZOMATH g^\\prime END hay không?',
        ),
        (
            'Luyện tập Làm Bài luyện tập 01–08 theo thứ tự trong lượt đầu. Ghi tập xác định, khoảng và lí do trước khi kết luận.',
            'Luyện tập Ở lượt đầu, làm các bài theo ba chặng: Bài 01–04 củng cố chuỗi công thức–dấu–biến thiên–cực trị; Bài 05–06 luyện đọc ngược mà không thêm dữ kiện; Bài 07–08 luyện đánh giá và sửa lỗi. Sau mỗi chặng, ghi lại lỗi còn lặp rồi mới chuyển tiếp. Ghi tập xác định, khoảng và lí do trước khi kết luận.',
        ),
    ]
    for before, after in approved_editorial_edits:
        assert projected_text.count(before) == 1, f'Approved editorial baseline changed: {before}'
        projected_text = projected_text.replace(before, after, 1)
    assert projected_text.count('Cách thực hiện.') == 8, 'R1-G01 guidance label baseline changed'
    projected_text = projected_text.replace('Cách thực hiện.', 'Cách thực hiện')
    guidance_structure_edits = [
        (new_guidance, 'Cách thực hiện '+new_guidance),
        ('Luyện tập Ở lượt đầu,', 'Luyện tập Cách thực hiện Ở lượt đầu,'),
        ('Kiểm tra Thời gian đề xuất:', 'Kiểm tra Cách thực hiện Thời gian đề xuất:'),
        ('Sau khi hoàn thành bài kiểm tra Mở hướng dẫn chấm', 'Sau khi hoàn thành bài kiểm tra Cách thực hiện Mở hướng dẫn chấm'),
        ('Sửa lỗi Mỗi lượt: giữ bài làm sai ban đầu; chỉ ra điều kiện hoặc bước suy luận bị bỏ; viết lại cho đúng; làm bài tập khắc phục lỗi tương ứng khi chưa mở đáp án.',
         'Sửa lỗi Cách thực hiện Mỗi lượt: Giữ bài làm sai ban đầu. Chỉ ra điều kiện hoặc bước suy luận bị bỏ. Viết lại cho đúng. Làm bài tập khắc phục lỗi tương ứng khi chưa mở đáp án.'),
        ('Ôn lại Sau khi sửa bài,', 'Ôn lại Cách thực hiện Sau khi sửa bài,'),
        ('Lời giải và hướng dẫn chấm Chỉ mở lời giải', 'Lời giải và hướng dẫn chấm Cách thực hiện Chỉ mở lời giải'),
    ]
    for before, after in guidance_structure_edits:
        assert projected_text.count(before) == 1, f'Guidance structure baseline changed: {before}'
        projected_text = projected_text.replace(before, after, 1)
    guidance_wording_edits = [
        ('Trước tiên, trả lời câu hỏi mở đầu', 'Trả lời câu hỏi mở đầu'),
        ('Sau đó đọc định nghĩa và Ví dụ 01', 'Đọc định nghĩa và Ví dụ 01'),
        ('Sau đó tính giá trị tại các mốc', 'Tính giá trị tại các mốc'),
        ('Câu hỏi tự kiểm tra 03 giúp em kiểm tra', 'Làm Câu hỏi tự kiểm tra 03 để kiểm tra'),
        ('Sau đó ghi rõ điều đã sửa', 'Ghi rõ điều đã sửa'),
        ('Các số liệu trong hình có nhãn là dữ kiện chính xác;', 'Dùng các số liệu trong hình có nhãn như dữ kiện chính xác;'),
        ('Lời giải nằm ở phần Lời giải và hướng dẫn chấm, không dùng', 'Chỉ mở lời giải ở phần Lời giải và hướng dẫn chấm; không dùng'),
        ('Việc sửa lỗi cần được thể hiện bằng bài làm mới; đọc quy trình chưa đủ để xác nhận', 'Thể hiện việc sửa lỗi bằng bài làm mới; không chỉ đọc quy trình để xác nhận'),
        ('Sau đó tự giải lại một bài từng sai', 'Tự giải lại một bài từng sai'),
        ('Để kiểm tra khả năng vận dụng, hãy làm', 'Để kiểm tra khả năng vận dụng, làm'),
    ]
    for before, after in guidance_wording_edits:
        assert projected_text.count(before) == 1, f'Guidance wording baseline changed: {before}'
        projected_text = projected_text.replace(before, after, 1)
    phase_3e_edits = [
        (
            'Với Ví dụ 03, tự tính đạo hàm và xét dấu trước khi xem bảng. Tính giá trị tại các mốc, lập bảng biến thiên rồi phác đồ thị.',
            'Với Ví dụ 03, tự tính đạo hàm và xét dấu trước khi xem bảng. Tính giá trị tại các mốc. Lập bảng biến thiên rồi phác đồ thị.',
        ),
        (
            'Luyện tập Cách thực hiện Ở lượt đầu, làm các bài theo ba chặng: Bài 01–04 củng cố chuỗi công thức–dấu–biến thiên–cực trị; Bài 05–06 luyện đọc ngược mà không thêm dữ kiện; Bài 07–08 luyện đánh giá và sửa lỗi. Sau mỗi chặng, ghi lại lỗi còn lặp rồi mới chuyển tiếp. Ghi tập xác định, khoảng và lí do trước khi kết luận. Dùng các số liệu trong hình có nhãn như dữ kiện chính xác; chỉ xét phần tập xác định được đề bài chỉ rõ. Chỉ mở lời giải ở phần Lời giải và hướng dẫn chấm; không dùng kết luận của một câu như giả thiết của câu khác.',
            'Luyện tập Dùng các số liệu trong hình có nhãn như dữ kiện chính xác; chỉ xét phần tập xác định được đề bài chỉ rõ. Không dùng kết luận của một câu như giả thiết của câu khác. Cách thực hiện Ở lượt đầu, làm các bài theo ba chặng: Bài 01–04 củng cố chuỗi công thức–dấu–biến thiên–cực trị; Bài 05–06 luyện đọc ngược mà không thêm dữ kiện; Bài 07–08 luyện đánh giá và sửa lỗi. Sau mỗi chặng, ghi lại lỗi còn lặp rồi mới chuyển tiếp. Ghi tập xác định, khoảng và lí do trước khi kết luận. Chỉ mở lời giải ở phần Lời giải và hướng dẫn chấm của bản đầy đủ.',
        ),
    ]
    for before, after in phase_3e_edits:
        assert projected_text.count(before) == 1, f'Phase 3E approved baseline changed: {before}'
        projected_text = projected_text.replace(before, after, 1)
    source_note_edits = [
        ('[SGK Toán 12, tập một, Bài 1, tr. 6]', 'Nguồn đối chiếu: Sách giáo khoa Toán 12, tập một, bài 1, trang 6.'),
        ('[SGK Toán 12, tập một, Bài 1, tr. 7]', 'Nguồn đối chiếu: Sách giáo khoa Toán 12, tập một, bài 1, trang 7.'),
        ('[SGK Toán 12, tập một, Bài 1, tr. 7–8; SGK Toán 12, tập một, Bài 4, tr. 26–27]', 'Nguồn đối chiếu: Sách giáo khoa Toán 12, tập một, bài 1, trang 7–8; Sách giáo khoa Toán 12, tập một, bài 4, trang 26–27.'),
        ('[SGK Toán 12, tập một, Bài 1, tr. 10]', 'Nguồn đối chiếu: Sách giáo khoa Toán 12, tập một, bài 1, trang 10.'),
        ('[Đối chiếu chú ý về ZOMATH x^3 END trong SGK Toán 12, tập một, Bài 1, tr. 11]', 'Nguồn đối chiếu: chú ý về ZOMATH x^3 END trong Sách giáo khoa Toán 12, tập một, bài 1, trang 11.'),
        ('[SGK Toán 12, tập một, Bài 1, tr. 6, 14]', 'Nguồn đối chiếu: Sách giáo khoa Toán 12, tập một, bài 1, trang 6 và 14.'),
        ('[SGK Toán 12, tập một, Bài 1, tr. 9]', 'Nguồn đối chiếu: Sách giáo khoa Toán 12, tập một, bài 1, trang 9.'),
        ('[Đối chiếu dạng đọc đồ thị đạo hàm: SGK Toán 12, tập một, Bài 1, tr. 14, bài 1.6]', 'Nguồn đối chiếu: dạng bài đọc đồ thị đạo hàm trong Sách giáo khoa Toán 12, tập một, bài 1, trang 14, bài tập 1.6.'),
    ]
    for before, after in source_note_edits:
        expected = 2 if before in (
            '[SGK Toán 12, tập một, Bài 1, tr. 7]',
            '[SGK Toán 12, tập một, Bài 1, tr. 9]',
        ) else 1
        assert projected_text.count(before) == expected, f'Source-note baseline changed: {before}'
        projected_text = projected_text.replace(before, after)
    projected_text = projected_text.replace(
        'ZO Math · R1-G01 · Phiên bản 1.1 · Kết nối hàm số, bảng biến thiên và đồ thị',
        'ZO Math · Đơn điệu và cực trị · Phiên bản 1.3',
        1,
    )
    theory_spans = [
        ('1.1. Từ “đi lên” đến định nghĩa', 'Hai điều phải giữ nguyên'),
        ('2.1. Định lí và phạm vi áp dụng', 'Khi áp dụng, viết đủ ba ý'),
        ('2.2. Một số hữu hạn điểm đạo hàm bằng 0', 'Không được rút gọn'),
        ('4.1. Điều kiện đủ qua dấu đạo hàm', 'Đó là định lí điều kiện đủ đang dùng'),
        ('5.1. Định nghĩa theo so sánh trong một lân cận', 'Từ “gần” được làm chính xác'),
    ]
    def mask_theory_spans(text):
        for index, (start, end) in enumerate(theory_spans, 1):
            first = text.index(start) + len(start)
            last = text.index(end, first)
            text = text[:first] + f' THEORY-{index} ' + text[last:]
        return norm(text)
    phase3_solution_ids = {'lg-' + task_id for task_id in PHASE3_TASK_IDS}
    checks['phase3_content_scope_exact'] = (
        PHASE3_TASK_IDS == {node.get('id') for node in target.select(
            '#sua-loi section.zo-learning-task--item[id^="g01-s-k-"], '
            '#on-lai section.zo-learning-task--item[id^="g01-"]'
        )}
        and phase3_solution_ids == {node.get('id') for node in target.select(
            '#loi-giai details.zo-learning-solution[id^="lg-g01-"]'
        )}
        and [node.get('id') for node in target.select('[id^="cp-"]')]
        == ['cp-lt1', 'cp-lt2', 'cp-lt3', 'cp-kt', 'cp-on1', 'cp-on2', 'cp-on3']
        and 'G01-E02' in norm(target.select_one('#r1-table-t18').get_text(' ', strip=True))
    )
    checks['downloads_exact'] = [(x['href'], x.get('download')) for x in target.select('.r1-downloads a')] == [
        ('index_hoc_sinh.pdf', 'R1-G01_hoc_va_bai_tap_v1.3.pdf'),
        ('index.pdf', 'R1-G01_hoc_lieu_day_du_v1.3.pdf')]
    checks['download_cards_exact'] = [
        (norm(card.select_one('h3').get_text()),
         norm(card.select_one('.r1-download-card__meta').get_text()))
        for card in target.select('.r1-download-card')
    ] == [
        ('Bản học và bài tập', f"{pdf_pages['index_hoc_sinh.pdf']} trang · PDF"),
        ('Bản đầy đủ', f"{pdf_pages['index.pdf']} trang · PDF"),
    ]
    section_items = target.select('.r1-section-download-list > li')
    checks['section_download_list_exact'] = (
        len(section_items) == 6
        and [
            {
                'title': norm(item.select_one('.r1-section-download-title').get_text()),
                'description': norm(item.select_one('.r1-section-download-description').get_text()),
                'href': item.select_one('a')['href'],
                'download': item.select_one('a').get('download'),
            }
            for item in section_items
        ] == [
            {key: spec[key] for key in ('title', 'description', 'href', 'download')}
            for spec in (manifest if manifest_shape_valid else [])
        ]
        and not target.select('.r1-section-download-list .r1-download-card')
    )
    support = target.select_one('.r1-download-support')
    checks['download_support_verified_exact'] = (
        support is not None
        and support.name == 'div'
        and norm(support.select_one('p').get_text())
        == 'Nếu học liệu hữu ích với bạn, bạn có thể ủng hộ ZO Math tiếp tục biên soạn và chia sẻ.'
        and support.select_one('.r1-brand-mark').get('src') == 'hinh/dau_nhan_zo.svg'
        and support.select_one('.r1-support-qr').get('src').endswith('/assets/images/qr_bao_tro_zo_math_vietcombank.jpg')
        and [norm(x.get_text()) for x in support.select('dd')]
        == ['Vietcombank', '0601000137768', 'Nguyễn Tấn Nhựt', 'BAO TRO ZO MATH']
        and support.select_one('.r1-support-link a').get('href').endswith('/content/support/donate.html')
    )
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
    graph_names = [f'do_thi_{i:02d}' for i in range(1, 14)]
    checks['graph_vector_triplets_exist'] = all(
        (PACKAGE/'hinh'/f'{name}.{ext}').is_file()
        for name in graph_names for ext in ('tex', 'pdf', 'svg')
    )
    checks['canonical_graph_png_absent'] = not any(
        (PACKAGE/'hinh'/f'{name}.png').exists() for name in graph_names
    )
    checks['html_graphs_use_svg'] = [
        img.get('src') for img in target.select('figure:not(.zo-variation-asset) img')
    ] == [f'hinh/do_thi_{index:02d}.svg' for index in range(1, 9)] + [
        'hinh/do_thi_12.svg', 'hinh/do_thi_11.svg', 'hinh/do_thi_13.svg',
        'hinh/do_thi_09.svg', 'hinh/do_thi_10.svg',
    ]
    variation_names = [f'bbt{i:02d}' for i in range(1, 14)]
    checks['variation_vector_triplets_exist'] = all(
        (PACKAGE/'hinh'/f'{name}.{ext}').is_file()
        for name in variation_names for ext in ('tex', 'pdf', 'svg')
    )
    checks['zo_mark_assets_exact'] = (
        sha(PACKAGE/'hinh/dau_nhan_zo.svg') == 'd6b3c1664ab5d4185d7acbb228100aa0cfcc1b3ea666ae4565592a2c2b6731eb'
        and sha(PACKAGE/'hinh/dau_nhan_zo.png') == 'f71985b029ead81cb04eef78e174cada60ad7753b800300450f789ccbadfcf8e'
    )
    variation_order = ['bbt01', 'bbt02', 'bbt12', 'bbt13', 'bbt03', 'bbt04',
                       'bbt05', 'bbt06', 'bbt07', 'bbt08', 'bbt09', 'bbt10', 'bbt11']
    checks['html_variations_use_svg'] = [
        img.get('src') for img in target.select('.zo-variation-image')
    ] == [f'hinh/{name}.svg' for name in variation_order]
    variation_figures = target.select('figure.zo-variation-asset')
    variation_caption_contract = len(variation_figures) == 13
    for figure in variation_figures:
        children = [child for child in figure.children if getattr(child, 'name', None)]
        image = figure.select_one(':scope > img.zo-variation-image')
        caption = figure.select_one(':scope > figcaption.zo-variation-caption')
        table_caption = figure.select_one(':scope > .visually-hidden table.variation > caption')
        variation_caption_contract &= (
            [child.name for child in children] == ['img', 'figcaption', 'div']
            and image is not None and caption is not None and table_caption is not None
            and norm(caption.get_text()) == norm(table_caption.get_text())
            and norm(caption.get_text()).endswith('.')
            and image.get('alt', '').startswith(norm(caption.get_text()) + ' — ')
        )
    checks['variation_caption_below_asset_exact'] = variation_caption_contract
    variation_css = (ROOT/'assets/css/zo_variation.css').read_text(encoding='utf-8')
    checks['variation_caption_style_exact'] = all(fragment in variation_css for fragment in (
        '.zo-variation-caption {',
        'margin: 0.4rem 0 0;',
        'color: #766f66;',
        'font-size: 0.9em;',
        'font-weight: 400;',
    ))
    css = (ROOT/'assets/css/zo_on_thi_learning_package.css').read_text(encoding='utf-8')
    script = (ROOT/'assets/html/zo_on_thi_learning_package_script.html').read_text(encoding='utf-8')
    lua = (PACKAGE/'cong_cu/r1_g01.lua').read_text(encoding='utf-8')
    checks['lua_manifest_boundary_chain_derived_exact'] = (
        all(fragment in lua for fragment in (
            'local function projection_boundary_chain(specs)',
            'for _, spec in ipairs(specs) do',
            'boundaries:insert(spec.start)',
            'expected_start = spec.end_before',
            'local required = projection_boundary_chain(section_download_specs)',
            'verify_projection_boundary_fixture()',
            "fixture[1].start = 'fixture-renamed'",
        ))
        and not any(f"'{identifier}'" in lua for identifier in projected_ids)
    )
    checks['details_affordance_css_exact'] = all(fragment in css for fragment in (
        'details > summary::-webkit-details-marker { display: none; }',
        'details.zo-block > summary::marker { content: ""; }',
        'content: "";',
        '--r1-disclosure-icon: url("data:image/svg+xml',
        "d='M3 8h10M8 3v10'",
        "d='M3 8h10'",
        'mask: var(--r1-disclosure-icon) center / contain no-repeat;',
        'min-height: 44px;',
        '--focus-ring-color: #554f48;',
        '--focus-ring-width: 2px;',
        '--focus-ring-offset: 2px;',
        'outline: 2px solid #554f48 !important;',
        'outline-offset: 2px !important;',
        'body.zo-on-thi-package-page .zo-on-thi-package details.zo-block {',
        'overflow: visible;',
        'border-radius: inherit;',
        'border-end-start-radius: 0;',
        'border-end-end-radius: 0;',
        'padding-block: 5px;',
        'margin: -5px -4px;',
        'scroll-padding-inline: 4px;',
        'scroll-snap-type: x proximity;',
        'body.zo-on-thi-package-page .r1-tablist::before,',
        'body.zo-on-thi-package-page .r1-tablist::after {',
        'flex: 0 0 4px;',
        'body.zo-on-thi-package-page .r1-tablist > .r1-tab + .r1-tab {',
        'margin-inline-start: .2rem;',
        'body.zo-on-thi-package-page .r1-tablist > .r1-tab:last-of-type {',
        'scroll-snap-align: end;',
        '@media print',
    ))
    checks['all_disclosure_headers_compact_exact'] = all(fragment in css for fragment in (
        '.zo-on-thi-package details > summary {',
        'display: flex;',
        'align-items: center;',
        'min-height: 44px;',
        'box-sizing: border-box;',
        'padding: .4rem 3rem .4rem .85rem;',
        '.zo-on-thi-package .r1-section-toc > summary { font-weight: 600; }',
    )) and 'padding-right: 3rem;' not in css
    checks['table_css_exact'] = (
        'min-width: var(--r1-table-min-width);' in css
        and 'padding: .45em .5em;' in css
        and '.zo-on-thi-package .r1-data-table {\n  table-layout: fixed;\n  border: 1px solid var(--r1-border);\n}' in css
        and '.zo-on-thi-package .r1-data-table th,\n.zo-on-thi-package .r1-data-table td {\n  border: 1px solid var(--r1-border);' in css
        and 'overflow-wrap: anywhere' not in css
        and 'font-size: .875em' not in css
        and 'font-size: .8em' not in css
        and 'padding-inline: .05rem' not in css
        and '.r1-data-table math { font-size: 1em; white-space: nowrap; }' in css
    )
    checks['native_mobile_table_pan_exact'] = all(fragment in css for fragment in (
        '.zo-on-thi-package .r1-table-scroll-x {',
        'max-width: 100%;',
        'overscroll-behavior-x: contain;',
        'overscroll-behavior-y: auto;',
        'touch-action: pan-x pan-y pinch-zoom;',
        '-webkit-overflow-scrolling: touch;',
    )) and all(fragment not in script.lower() for fragment in (
        'touchstart', 'touchmove', 'touchend', 'pointerdown', 'pointermove',
        'pointerup', "addeventlistener('wheel'", 'addeventlistener("wheel"',
    ))
    checks['ordinary_table_weight_exact'] = all(fragment in css for fragment in (
        '.zo-on-thi-package .r1-data-table tbody th { background: #ffffff; }',
        '.zo-on-thi-package .r1-data-table thead th {',
        'background: #ffffff;',
        'font-weight: 400;',
        '.zo-on-thi-package .r1-data-table tbody th { font-weight: 400; }',
    )) and not target.select('#r1-table-t01 tbody strong')
    selected_tab_css = re.search(
        r'body\.zo-on-thi-package-page \.r1-tab\[aria-selected="true"\] \{([^}]*)\}',
        css,
        re.S,
    )
    download_support_css = re.search(
        r'\.zo-on-thi-package \.r1-download-support \{([^}]*)\}',
        css,
        re.S,
    )
    checks['zo_color_and_surface_mapping_exact'] = all(fragment in css for fragment in (
        'body.zo-on-thi-package-page #title-block-header .title {',
        'color: var(--r1-red);',
        '.zo-on-thi-package section.level2 > h2 {',
        'background: #ffffff;',
        '.zo-on-thi-package .r1-download-support {',
        'body.zo-on-thi-package-page .r1-tab[aria-selected="true"] {',
    )) and all((
        selected_tab_css is not None,
        download_support_css is not None,
        'background: var(--bs-secondary-bg);' in selected_tab_css.group(1),
        'box-shadow: none;' in selected_tab_css.group(1),
        'border-color:' not in selected_tab_css.group(1),
        'font-weight:' not in selected_tab_css.group(1),
        'color:' not in selected_tab_css.group(1),
        'inset' not in selected_tab_css.group(1),
        'background: var(--bs-secondary-bg);' in download_support_css.group(1),
        'border: 1px solid var(--r1-border);' in download_support_css.group(1),
        'padding: 1.35rem;' in download_support_css.group(1),
        '#f8f5f0' not in css,
    ))
    shared_learning_css = (ROOT/'assets/css/_zo_learning_components.scss').read_text(encoding='utf-8')
    canonical_contract = CANONICAL_CONTRACT.read_text(encoding='utf-8')
    checks['canonical_baseline_1_0_documented_exact'] = all(
        fragment in canonical_contract
        for fragment in (
            'Định danh baseline: `on-thi-learning-components/1.0`.',
            '### Khung trang và điều hướng',
            '### Khối thu gọn và bề mặt',
            '### Nhiệm vụ, ví dụ và liên kết',
            '### Bảng, bảng biến thiên và hình',
            '### Công thức và nguồn đối chiếu',
            '### Hàng rào kiểm định',
            'desktop, 430 px và 390 px',
        )
    )
    checks['canonical_mobile_tab_edge_contract_exact'] = (
        'const tabEdgePadding = 12;' in script
        and 'selectedTab.offsetLeft - tabEdgePadding' in script
        and 'selectedTab.offsetLeft + selectedTab.offsetWidth + tabEdgePadding' in script
    )
    checks['canonical_package_assets_exact'] = (
        'css: ../../../../../assets/css/zo_on_thi_learning_package.css' in qmd
        and 'include-after-body: ../../../../../assets/html/zo_on_thi_learning_package_script.html' in qmd
        and 'giao_dien/r1_g01.css' not in qmd
        and 'giao_dien/r1_g01_script.html' not in qmd
        and '.zo-on-thi-package' in css
        and 'body.zo-on-thi-package-page' in css
        and '.r1-g01' not in css
        and "document.querySelector('.zo-on-thi-package')" in script
        and "root.dataset.r1Code" in script
        and "document.querySelector('.r1-g01')" not in script
    )
    checks['guidance_white_surface_exact'] = all(fragment in shared_learning_css for fragment in (
        '.zo-learning-guidance {',
        '--zo-block-background: #{$white};',
        '--zo-block-border: #{$gray-300};',
        '--zo-block-hover: #{$gray-100};',
        '.zo-learning-solution {',
        '--zo-block-background: #{$gray-100};',
        '--zo-block-hover: #{$gray-200};',
        'border-radius: 0.5rem;',
        'details.zo-block.zo-learning-guidance > summary,\ndetails.zo-block.zo-learning-solution > summary {',
        'min-height: 44px;',
        'padding: 0.4rem 3rem 0.4rem 0.85rem;',
    ))
    checks['source_note_style_exact'] = all(fragment in shared_learning_css for fragment in (
        '.zo-source-note {',
        'display: block;',
        'margin-top: 0.65rem;',
        'color: #{$gray-600};',
        'font-size: 0.8em;',
        'font-weight: 400;',
        'line-height: 1.45;',
    ))
    checks['decorative_dividers_removed_exact'] = (
        not target.select('hr')
        and re.search(r'(?m)^-{5,}\s*$', qmd) is None
        and '.r1-footer { border-top:' not in css
    )
    bbt_clip_rules = (
        '[data-bbt="BBT01"] { --r1-bbt-clip: 6.7125% 3.2038% 6.7125% 4.5260%; --r1-bbt-radius: 3.3281% / 6.9730%; }',
        '[data-bbt="BBT02"] { --r1-bbt-clip: 6.7125% 2.4272% 6.7125% 3.4288%; --r1-bbt-radius: 2.5213% / 6.9730%; }',
        '[data-bbt="BBT03"] { --r1-bbt-clip: 6.7125% 3.1946% 6.7125% 4.5130%; --r1-bbt-radius: 3.3186% / 6.9730%; }',
        '[data-bbt="BBT04"],\n.zo-on-thi-package .zo-variation-asset[data-bbt="BBT05"] { --r1-bbt-clip: 6.7125% 2.5042% 6.7125% 3.5376%; --r1-bbt-radius: 2.6013% / 6.9730%; }',
        '[data-bbt="BBT06"],\n.zo-on-thi-package .zo-variation-asset[data-bbt="BBT08"] { --r1-bbt-clip: 9.3915% 2.7605% 9.3915% 3.8997%; --r1-bbt-radius: 2.8676% / 9.7559%; }',
        '[data-bbt="BBT07"] { --r1-bbt-clip: 9.3915% 2.6037% 9.3915% 3.6783%; --r1-bbt-radius: 2.7047% / 9.7559%; }',
        '[data-bbt="BBT09"] { --r1-bbt-clip: 9.3915% 2.6470% 9.3915% 3.7394%; --r1-bbt-radius: 2.7497% / 9.7559%; }',
        '[data-bbt="BBT10"] { --r1-bbt-clip: 9.3915% 2.5929% 9.3915% 3.6630%; --r1-bbt-radius: 2.6935% / 9.7559%; }',
        '[data-bbt="BBT11"] { --r1-bbt-clip: 6.7125% 2.4508% 6.7125% 3.4622%; --r1-bbt-radius: 2.5459% / 6.9730%; }',
        '[data-bbt="BBT12"] { --r1-bbt-clip: 6.7125% 2.4198% 6.7125% 3.4184%; --r1-bbt-radius: 2.5137% / 6.9730%; }',
        '[data-bbt="BBT13"] { --r1-bbt-clip: 6.7125% 2.8704% 6.7125% 4.0550%; --r1-bbt-radius: 2.9818% / 6.9730%; }',
    )
    checks['html_bbt_outer_fill_clip_exact'] = (
        '.zo-on-thi-package figure.zo-variation-asset {' in css
        and 'margin: .75rem 0 1rem;' in css
        and 'padding: 0;' in css
        and 'background: transparent;' in css
        and 'clip-path: inset(var(--r1-bbt-clip) round var(--r1-bbt-radius));' in css
        and all(rule in css for rule in bbt_clip_rules)
        and all(f'data-bbt="BBT{i:02d}"' in css for i in range(1, 14))
    )
    checks['html_visual_assets_centered_exact'] = all(fragment in css for fragment in (
        '.zo-on-thi-package .zo-variation-image {\n  margin-inline: auto;',
        '.zo-on-thi-package figure img {',
        'display: block;',
        'margin-inline: auto;',
    ))
    checks['pdf_bbt_outer_fill_trim_exact'] = all(fragment in lua for fragment in (
        'local function render_variation(div)',
        "local id = assert(div.attributes.bbt, 'R1-G01 BBT is missing its identifier')",
        "\\includegraphics[trim=8.01pt 5.67pt 5.67pt 5.67pt,clip]",
        "return render_variation(div)",
    ))
    checks['permanent_link_cue_exact'] = (
        '.zo-on-thi-package a:not(.zo-pdf-download__link)' in css
        and 'text-decoration-line: underline;' in css
    )
    checks['table_overflow_script_exact'] = all(fragment in script for fragment in (
        "root.querySelectorAll('.r1-table-scroll-x')",
        'wrapper.scrollWidth > wrapper.clientWidth + 1',
        "wrapper.tabIndex = 0",
        "wrapper.setAttribute('aria-describedby', hint.id)",
        "wrapper.removeAttribute('tabindex')",
        "wrapper.addEventListener('keydown'",
        "event.key !== 'ArrowLeft' && event.key !== 'ArrowRight'",
        'wrapper.scrollLeft += direction * Math.max(32, wrapper.clientWidth * .2)',
        'event.preventDefault()',
        'new ResizeObserver',
    ))
    checks['native_details_and_hash_exact'] = (
        "if (node.tagName === 'DETAILS') node.open = true;" in script
        and "window.addEventListener('hashchange'" in script
        and "window.addEventListener('popstate'" in script
        and "history[method]({r1View: view, r1Target: targetId}, '', urlFor(view, targetId));" in script
        and "const VIEW_PARAM = 'r1-view';" in script
        and "if (target && view !== 'toan-van') view = ownerView(target);" in script
        and "const view = currentView === 'toan-van' ? 'toan-van' : ownerView(target);" in script
        and "setAttribute('aria-expanded'" not in script and 'role="button"' not in script
    )
    checks['progressive_tabs_apg_exact'] = all(fragment in script for fragment in (
        "{view: 'cach-hoc', label: 'Cách học'",
        "{view: 'tai-pdf', label: 'Tải PDF'",
        "{view: 'toan-van', label: 'Toàn văn'",
        "tablist.setAttribute('role', 'tablist')",
        "tab.setAttribute('role', 'tab')",
        "viewPanel.setAttribute('role', 'tabpanel')",
        "tab.setAttribute('aria-controls', viewPanel.id)",
        "tab.setAttribute('aria-selected'",
        "if (event.key === 'ArrowLeft')",
        "if (event.key === 'ArrowRight')",
        "if (event.key === 'Home')",
        "if (event.key === 'End')",
        "if (event.key === 'Enter' || event.key === ' ')",
        "root.classList.add('r1-tabs-ready')",
        "contentOrder.forEach(id => viewPanel.append(sectionById.get(id)))",
        "viewPanel.setAttribute('aria-labelledby', selectedTab.id)",
        "sectionById.get(id).hidden = !showAll && !definition.ids.includes(id);",
    )) and all(fragment not in script for fragment in (
        "event.key === 'ArrowUp'", "event.key === 'ArrowDown'",
        'cloneNode(', 'r1-view-all-toggle',
        "root.querySelectorAll('details').forEach(details => { details.open = true; })",
    )) and '.zo-on-thi-package.r1-tabs-ready .r1-view-panel > [hidden]' in css
    checks['local_navigation_exact'] = all(fragment in script for fragment in (
        "const expectedLessonCount = Number.parseInt(root.dataset.r1LessonCount || '9', 10);",
        'lessonHeadings.length !== expectedLessonCount',
        "lessonDetails.className = 'r1-section-toc'",
        "lessonSummary.textContent = 'Mục lục'",
        "lessonNav.setAttribute('aria-label', 'Mục lục bên trong Bài học')",
        "lessonNav.append(lessonToc)",
    )) and all(fragment not in script for fragment in (
        'lessonMobile', "summary.textContent = 'Trong phần này'", 'r1-next-link',
    ))
    checks['single_canonical_dom_and_no_js_fallback_exact'] = (
        script.count("setAttribute('role', 'tabpanel')") == 1
        and 'cloneNode(' not in script and '.innerHTML' not in script
        and not target.select('section[hidden]')
        and len(target.select('.lesson-toc')) == 1
    )
    checks['official_title_pdf_style_exact'] = all(fragment in lua for fragment in (
        "header.content:insert(1, pandoc.RawInline('latex', '\\\\color{zomathred}'))",
        '{\\LARGE\\bfseries\\color{zomathred}\\zoPdfTitle\\par}',
        'Kết thúc học liệu “\\zoPdfTitle”.',
    ))
    checks['pdf_running_headers_output'] = all(
        inspect_pdf(PACKAGE / name, label)['ok'] for name, label in (
            ('index.pdf', 'Bản đầy đủ'), ('index_hoc_sinh.pdf', 'Bản học và bài tập'))
    )
    pdf_content_lua = (ROOT/'assets/lua/zo_pdf_content.lua').read_text(encoding='utf-8')
    pdf_tex = (ROOT/'assets/tex/zo-pdf.tex').read_text(encoding='utf-8')
    variation_lua = (ROOT/'assets/lua/zo_variation_qmd.lua').read_text(encoding='utf-8')
    checks['pdf_canonical_component_mapping_exact'] = all(fragment in lua for fragment in (
        "and 'zo-block-white' or 'zo-block-gray'",
        'function Table(tbl)',
        'return render_grid_table(tbl)',
        "replace_plain(output, '\\\\toprule\\\\noalign{}', '\\\\hline')",
        "not pandoc.utils.stringify(following):match('^Xem đề bài')",
        "div.classes:includes('r1-figcaption') and latex",
        "div.classes:includes('r1-figure') and latex",
        'urlcolor=zomathgray',
    )) and all(fragment in pdf_content_lua for fragment in (
        'has_class(classes, "zo-block-white")',
        'has_class(classes, "zo-learning-guidance")',
        'return "zoBlockWhite"',
        'has_class(div.classes, "zo-source-note")',
        'local function style_source_note(span)',
        'doc = doc:walk({Span = style_source_note})',
    )) and all(fragment in pdf_tex for fragment in (
        '\\newtcolorbox{zoBlockWhite}[1]{',
        'colback=zomathblockwhitebg,',
        'coltitle=zomathgray,',
    )) and all(fragment in variation_lua for fragment in (
        "\\\\begin{minipage}{\\\\linewidth}\\\\centering",
        "\\\\includegraphics{'..path..'}}\\\\par\\\\smallskip",
        "{\\\\small\\\\color[HTML]{766F66}'..tex(title)..'}\\\\par",
    ))
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
