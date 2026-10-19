"""D0 PDF regressions: source preservation, anchors, vectors, fonts and receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from unittest.mock import patch

from pypdf import PdfReader

from dung_pdf import inputs, OUTPUT, PACKAGE, RECEIPT
from zo_pdf_support import support_model
from kiem_chung_da_duyet import verify_source


def grid_check(pdf):
    """Check long horizontal borders on the raster, including empty headers.

    Scope: the six table-bearing pages of D0, not a general PDF table parser.
    Check full-height vertical borders as well as horizontal counts.
    """
    from PIL import Image
    import numpy as np
    cases = [('Hàm số 𝑓 có đạo hàm', 3, 9), ('Trung bình ghép nhóm', 3, 5),
             ('Có tham gia', 4, 4), ('Loại Vật liệu', 4, 5),
             ('Số bộ B Số bộ A lớn nhất', 7, 4), ('Mạch ôn Nội dung của mạch', 10, 3)]
    binary = shutil.which('pdftoppm')
    assert binary, 'Poppler required for grid regression'
    root = PACKAGE.parents[4] / '.quarto'
    root.mkdir(exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix='d0_grid_', dir=root) as directory:
        for needle, expected, vertical_expected in cases:
            candidates = [i for i,p in enumerate(pdf.pages) if needle in ' '.join(p.extract_text().split())]
            assert candidates, 'Table page missing: ' + needle
            number = candidates[0] + 1
            prefix = Path(directory) / 'page'
            subprocess.run([binary, '-f', str(number), '-l', str(number), '-singlefile',
                            '-scale-to', '1300', '-png', str(OUTPUT), str(prefix)], check=True,
                           capture_output=True)
            im = Image.open(prefix.with_suffix('.png')).convert('RGB')
            rows = []
            rgb = np.asarray(im).astype('int16')
            low, high = rgb.min(axis=2), rgb.max(axis=2)
            mask = (high-low < 35) & (low > 90) & (low < 235)
            for y, row in enumerate(mask):
                if re.search(b'\x01{201,}', row.tobytes()):
                    rows.append(y)
            bands = [y for i,y in enumerate(rows) if i == 0 or y > rows[i-1] + 1]
            assert len(bands) >= expected, f'PDF grid page {number}: {len(bands)} borders, expected at least {expected}'
            groups = []
            for y in bands:
                if not groups or y - groups[-1][-1] > 100:
                    groups.append([])
                groups[-1].append(y)
            vertical_counts = []
            for group in groups:
                match = re.search(b'\x01{201,}', mask[group[0]].tobytes())
                left, right = match.span()
                left, right = max(0, left-2), min(mask.shape[1], right+2)
                columns = np.flatnonzero(mask[group[0]+2:group[-1]-1, left:right].mean(axis=0) > .85)
                count = int(sum(i == 0 or x > columns[i-1]+1 for i,x in enumerate(columns)))
                vertical_counts.append(count)
            assert any(len(group) == expected and count == vertical_expected
                       for group, count in zip(groups, vertical_counts)), (
                f'PDF grid page {number}: table grids '
                f'{[(len(group), count) for group, count in zip(groups, vertical_counts)]}, '
                f'expected ({expected}, {vertical_expected})')
            results.append({'physical_page': number, 'horizontal_borders': len(bands),
                            'vertical_borders_per_table': vertical_counts})
    return results


def negative_grid_tests(pdf):
    """Erase one real rendered border in memory; the raster gate must reject it."""
    from PIL import Image, ImageDraw
    import numpy as np
    original = Image.open
    for axis in ('horizontal', 'vertical'):
        def damaged(path, *args, **kwargs):
            im = original(path, *args, **kwargs).convert('RGB')
            rgb = np.asarray(im).astype('int16')
            lo, hi = rgb.min(axis=2), rgb.max(axis=2)
            mask = (hi-lo < 35) & (lo > 90) & (lo < 235)
            for y, row in enumerate(mask):
                match = re.search(b'\x01{201,}', row.tobytes())
                if match:
                    left, right = match.span()
                    draw = ImageDraw.Draw(im)
                    if axis == 'horizontal':
                        draw.rectangle((0,y-2,im.width,y+2), fill='white')
                    else:
                        draw.rectangle((left-2,0,left+2,im.height), fill='white')
                    break
            return im
        with patch('PIL.Image.open', damaged):
            try:
                grid_check(pdf)
            except AssertionError as error:
                assert 'PDF grid page' in str(error), str(error)
            else:
                raise AssertionError('Missing ' + axis + ' border escaped raster guard')
    return ['missing_horizontal_border', 'missing_vertical_border']


def negative_source_tests():
    source = (PACKAGE / 'index.qmd').resolve()
    text = source.read_text(encoding='utf-8')
    original = Path.read_text
    cases = {
        'math_changed': text.replace('x=-3', 'x=-4', 1),
        'PDF_metadata_changed': text.replace('papersize: a4', 'papersize: a5', 1),
        'comparison_changed': text.replace('Nội dung cần ôn nếu còn vướng:', 'WRONG:', 1),
    }
    for name, mutated in cases.items():
        def reader(path, *args, **kwargs):
            return mutated if path.resolve() == source else original(path, *args, **kwargs)
        with patch.object(Path, 'read_text', reader):
            try:
                verify_source()
            except AssertionError:
                continue
            raise AssertionError(name + ' escaped source regression')
    return list(cases)


def check():
    verify_source()
    negative_cases = negative_source_tests()
    receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
    assert receipt['inputs_sha256'] == inputs(), 'PDF input fingerprint is stale'
    assert receipt['output_sha256'] == hashlib.sha256(OUTPUT.read_bytes()).hexdigest(), 'PDF changed'
    pdf = PdfReader(OUTPUT)
    assert pdf.metadata.title == 'Khảo sát đầu vào' and pdf.metadata.author == 'ZO Math'
    assert receipt['pages'] == len(pdf.pages)
    names = set(pdf.named_destinations)
    expected = {f'd0-r{r}-{n:02d}' for r in range(1, 9) for n in range(1, 4)}
    expected |= {f'doi-chieu-r{r}-{n:02d}' for r in range(1, 9) for n in range(1, 4)}
    expected |= {'cau-minh-hoa', 'doi-chieu-minh-hoa'}
    assert expected <= names, 'Task or comparison anchors missing: ' + str(expected - names)
    from zo_pdf_course_check import strict_structure
    assert strict_structure(OUTPUT), 'PDF dictionaries contain duplicate keys'
    assert len(pdf.outline)>=5, 'D0 section bookmarks missing'
    closing=[page.extract_text() for page in pdf.pages if 'Mở mạch đã chọn' in page.extract_text()]
    assert len(closing)==1 and 'Mạch ôn' in closing[0], 'Choice table and closing navigation split onto a near-empty page'
    text = '\n'.join(page.extract_text() for page in pdf.pages)
    assert not re.search(r'\\(?:frac|sqrt|prime|left|right)\b', text), 'Unrendered LaTeX'
    assert text.count('Kiến thức cần dùng:') == 25, 'Task metadata missing'
    assert text.count('Nội dung cần ôn nếu còn vướng:') == 24, 'Comparison missing'
    assert text.count('Xem lời giải') == 25 and text.count('Xem đề bài') == 25, 'Current answer-action labels missing'
    assert 'Đối chiếu bài này sau khi tự làm' not in text and 'Quay lại đề bài' not in text, 'Old answer-action labels remain'
    assert 'trang ??' not in text, 'Unresolved print page reference'
    for page in (pdf.pages[0], pdf.pages[-1]):
        visible = page.extract_text()
        assert 'Ngày tạo PDF:' in visible and 'Bản quyền nội dung thuộc ZO Math.' in visible
        assert receipt['print_metadata']['date'] in visible
    support=support_model()
    final=''.join(pdf.pages[-1].extract_text().split())
    assert ''.join(support['title'].split()) in final
    assert ''.join(support['copy'].split()) in final
    assert ''.join(support['cta'].split()) in final
    for item in support['fields']:
        assert ''.join(item['value'].split()) in final, 'Support metadata missing: ' + item['label']
    for page in pdf.pages:
        links=[a.get_object() for a in page.get('/Annots',[]) if a.get_object().get('/A',{}).get('/URI')=='https://zomath.vn']
        assert len(links)==1, 'Centered homepage link missing'
        rect=[float(x) for x in links[0]['/Rect']]
        assert abs((rect[0]+rect[2])/2-float(page.mediabox.width)/2)<2, 'Footer not centered'
    urls = set()
    vector_forms = 0
    embedded_fonts = set()
    for page in pdf.pages:
        assert abs(float(page.mediabox.width) - 595.276) < 1
        assert abs(float(page.mediabox.height) - 841.89) < 1
        resources = page['/Resources']
        for obj in resources.get('/XObject', {}).values():
            if obj.get_object().get('/Subtype') == '/Form':
                vector_forms += 1
        for font in resources.get('/Font', {}).values():
            font = font.get_object()
            descendants = font.get('/DescendantFonts', [font])
            for desc in descendants:
                desc = desc.get_object()
                fd = desc.get('/FontDescriptor')
                assert fd, 'Font descriptor missing'
                fd = fd.get_object()
                assert any(key in fd for key in ('/FontFile', '/FontFile2', '/FontFile3')), 'Font not embedded'
                embedded_fonts.add(str(fd['/FontName']))
        for annotation in page.get('/Annots', []):
            annotation = annotation.get_object()
            action = annotation.get('/A', {})
            uri = action.get('/URI')
            if uri:
                assert not any(x in uri for x in ('_audit', '.qmd', '../')), 'Noncanonical PDF URL'
                urls.add(str(uri))
            dest = annotation.get('/Dest') or action.get('/D')
            if isinstance(dest, str):
                assert dest in names, 'Broken internal link: ' + dest
    assert vector_forms >= 1, 'Box geometry missing from PDF'
    # The sign table is now native LaTeX from JSON, not an imported legacy Form.
    sign_page = next(p for p in pdf.pages if 'Hàm số 𝑓 có đạo hàm' in p.extract_text())
    assert len(sign_page.get('/Resources', {}).get('/XObject', {})) == 0, 'Legacy sign table imported'
    assert any('BeVietnam' in name for name in embedded_fonts)
    assert any('STIX' in name for name in embedded_fonts)
    for package in ('r1_g01', 'r1_g02', 'r1_g03', 'r1_g04'):
        assert any('/'+package+'/index.html' in uri for uri in urls), 'Current learning link missing: '+package
    grids = grid_check(pdf)
    negative_grids = negative_grid_tests(pdf)
    return {'status': 'pass', 'pages': len(pdf.pages), 'task_and_comparison_anchors': len(expected),
            'embedded_fonts': sorted(embedded_fonts), 'vector_figures': vector_forms,
            'external_links': sorted(urls), 'source_body': 'historical_full_source_regression_pass',
            'negative_source_cases_rejected': negative_cases,
            'print_metadata_and_support': 'pass',
            'sign_table': 'native_from_current_JSON',
            'raster_grid_regression': grids,
            'negative_raster_cases_rejected': negative_grids,
            'visual_review': 'separate_owner_review_pending', 'publication': 'pending'}


if __name__ == '__main__':
    print(json.dumps(check(), ensure_ascii=False, indent=2))
