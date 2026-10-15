"""Approval-specific, full-sequence regression; never edits content or receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
import yaml

from tich_hop_html_da_duyet import ROOT, REPO, RECEIPT, SECTIONS, signature

REVISION_PATH = ROOT / '_quy_trinh/dieu_chinh_sau_duyet.json'

# DH_025, direct user rule on 2026-10-11: exactly two delimiter-only changes.
# Reverse these deltas for historical comparison, never update approval hashes
# or globally strip sizing commands (which would hide unrelated source edits).
DELIMITER_DELTAS = {
    r'\sin(\frac{\pi t}{6})=1':r'\sin\left(\frac{\pi t}{6}\right)=1',
    r'\int_0^5(t-2)\,dt=[\frac{t^2}{2}-2t]_0^5=\frac52':r'\int_0^5(t-2)\,dt=\left[\frac{t^2}{2}-2t\right]_0^5=\frac52',
}


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def verify_source():
    approval = json.loads(RECEIPT.read_text(encoding='utf-8'))
    qmd = ROOT / 'index.qmd'
    original_qmd = qmd.read_text(encoding='utf-8')
    # Owner-approved print layout moves the existing HTML filter under HTML
    # and replaces only PDF options. Reverse these exact presentation changes
    # before checking the immutable content approval receipt.
    print_layout = [
        ('format:\n  html:\n    filters:\n      - cong_cu/d0.lua\n',
         'filters:\n  - cong_cu/d0.lua\nformat:\n  html:\n'),
        ('geometry: [top=22mm, bottom=22mm, left=21mm, right=21mm]',
         'geometry: [top=24mm, bottom=24mm, left=23mm, right=23mm]'),
        ('toc: false\n    toc-depth: 2', 'toc: true\n    toc-depth: 2'),
        ('      - cong_cu/d0_print.lua', '      - cong_cu/d0_pdf.lua'),
    ]
    for current, previous in print_layout:
        require(original_qmd.count(current)==1, 'PDF layout delta missing or repeated: '+current)
        original_qmd=original_qmd.replace(current,previous,1)
    pdf_delta = ROOT / '_quy_trinh/pdf_source_delta.json'
    if pdf_delta.is_file():
        # New PDF-only metadata is reversed in memory, not in the historical receipt.
        delta = json.loads(pdf_delta.read_text(encoding='utf-8'))
        require(delta['authority'] == 'owner_requested_D0_page_PDF_2026_10_14', 'Sai thẩm quyền PDF D0')
        insertion = delta['metadata_insertion']
        require(insertion.startswith('  pdf:\n') and '\n---' not in insertion, 'Delta phải chỉ chứa cấu hình PDF')
        require(hashlib.sha256(insertion.encode()).hexdigest() == delta['sha256'], 'Delta PDF bị đổi')
        block = '\n' + insertion.rstrip('\n')
        front, body = original_qmd.split('\n---\n', 1)
        require(front.count(block) == 1 and block not in body, 'Delta PDF sai vị trí/số lượng')
        original_qmd = front.replace(block, '', 1) + '\n---\n' + body
    for before, after in DELIMITER_DELTAS.items():
        require(original_qmd.count(after) == 1, 'Sai delta dấu ngoặc DH_025')
        original_qmd = original_qmd.replace(after, before, 1)
    # DH_018 permits only this presentation opt-in, not a new content receipt.
    opted = 'body-classes: zo-page-article zo-meta-hidden zo-on-thi-package-page d0-page zo-web-2027-d0'
    if opted in original_qmd:
        require(original_qmd.count(opted) == 1, 'Marker D0 opt-in bị lặp')
        original_qmd = original_qmd.replace(opted, opted.removesuffix(' zo-web-2027-d0'), 1)
    # a46a8051472b70c526f4554c862bb75e506110fc changed only the two
    # live catalog labels, outside the approved survey text. Reverse this
    # exact committed delta; never replace the historical approval hash.
    catalog = '- [Đơn điệu và cực trị](../r1_g01/index.qmd)\n- [Giá trị lớn nhất và giá trị nhỏ nhất](../r1_g02/index.qmd)'
    historical = '- [Kết nối hàm số, bảng biến thiên và đồ thị](../r1_g01/index.qmd)\n- [Giá trị lớn nhất và giá trị nhỏ nhất của hàm số](../r1_g02/index.qmd)'
    if catalog in original_qmd:
        require(original_qmd.count(catalog) == 1, 'Delta danh mục D0 bị lặp')
        original_qmd = original_qmd.replace(catalog, historical, 1)
    if REVISION_PATH.is_file():
        revision = json.loads(REVISION_PATH.read_text(encoding='utf-8'))
        for change in revision['replacements']:
            require(original_qmd.count(change['after']) == 1, 'Sai vị trí/số lượng chỉnh sửa đã duyệt')
            original_qmd = original_qmd.replace(change['after'], change['before'], 1)
    require(hashlib.sha256(original_qmd.encode()).hexdigest() == approval['qmd_sha256'],
            'QMD khác ứng viên chuyển đổi đã khóa: cần đối chiếu đầy đủ, không cập nhật hash để bỏ qua sai biệt')
    profile = yaml.safe_load((ROOT / '_quy_trinh/ho_so/index.yml').read_text(encoding='utf-8'))
    require(profile['workflow']['publication'] == 'pending', 'Không được nâng trạng thái xuất bản')
    require(profile['workflow']['production'] == 'accepted', 'Ứng viên HTML chưa được nghiệm thu')
    return approval


def original_signature(element, identifier):
    if not REVISION_PATH.is_file():
        return signature(element)
    copy = BeautifulSoup(str(element), 'html.parser')
    for annotation in copy.select('annotation[encoding="application/x-tex"]'):
        formula = annotation.get_text()
        for before, after in DELIMITER_DELTAS.items():
            if formula == after:
                annotation.string = before
    if identifier == 'khai-bao-pham-vi':
        require(not any(h.get_text(' ', strip=True) == 'Hàm số, đạo hàm, đồ thị' for h in copy.select('h3')), 'Tiêu đề trước ví dụ vẫn còn')
        heading = copy.new_tag('h3')
        heading.string = 'Hàm số, đạo hàm, đồ thị'
        copy.select_one('#cau-minh-hoa').insert_before(heading)
        label = copy.select_one('#cau-minh-hoa .d0-task-code')
        require(label.get_text(strip=True) == 'Hàm số, đạo hàm, đồ thị', 'Bài 00 sai tên mạch')
        label.string = 'R1'
        require('Trước khi xem hướng dẫn:' not in copy.get_text(), 'Đoạn đã yêu cầu bỏ vẫn còn')
        anchor = next(p for p in copy.select('p') if p.get_text(strip=True).startswith('Giả sử Minh'))
        paragraph = copy.new_tag('p')
        paragraph.string = json.loads(REVISION_PATH.read_text(encoding='utf-8'))['removed_paragraph']
        anchor.insert_before(paragraph)
    if identifier == 'khao-sat':
        toc = copy.select_one('.d0-survey-toc')
        require(toc is not None, 'Thiếu mục lục nguồn đọc được khi không JS')
        links = toc.select('a')
        require([a.get('href') for a in links] == [f'#mach-r{i}' for i in range(1,9)], 'Sai đích/thứ tự mục lục')
        for index in range(1,9):
            heading = copy.select_one(f'#mach-r{index} > h3')
            title = heading.get_text(' ',strip=True)
            require(title.startswith(f'R{index} — '), 'Thiếu mã mạch trên tiêu đề')
            require(links[index-1].get_text(' ',strip=True) == title, 'Mục lục lệch tiêu đề')
            heading.string = title.removeprefix(f'R{index} — ')
        toc.decompose()
    return signature(copy)


def verify_projection(root):
    """Full approved learner text/TeX, after removing presentation wrappers only."""
    approval = verify_source()
    require(root is not None, 'Thiếu root canonical')
    require([s.get('id') for s in root.find_all('section', recursive=False)] == SECTIONS, 'Sai cấu trúc thẻ')
    for identifier, expected in approval['sections'].items():
        actual = original_signature(root.find(id=identifier), identifier)
        require(actual['math'] == expected['math'], f'Chuỗi công thức khác bản duyệt: {identifier}')
        require(actual['text_sha256'] == expected['text_sha256'], f'Toàn chuỗi văn bản khác bản duyệt: {identifier}')
    return approval


def verify_html():
    path = REPO / 'docs' / ROOT.relative_to(REPO) / 'index.html'
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    root = soup.select_one('.zo-on-thi-package.d0-package')
    if soup.body.get('data-zo-web-production') == 'd0':
        import sys
        sys.path.insert(0, str(REPO / 'scripts'))
        from zo_web_2027_d0 import strip_papers
        from zo_web_2027_d0_check import validate
        verify_projection(strip_papers(root))
        checks, missing = validate(path)
        require(all(checks.values()), 'D0 web 2027: ' + ', '.join(k for k,v in checks.items() if not v))
        require(not missing, 'D0 web 2027 thiếu đích: ' + str(missing))
        print('PASS: D0 web 2027; full approved text/TeX, IDs, closed disclosures and links.')
        return
    approval = verify_projection(root)
    ids = [s['id'] for s in root.select('[id]')]
    require(len(ids) == len(set(ids)), 'ID trùng')
    require([t['id'] for t in root.select('.d0-primary-task')] == approval['task_ids'], 'Sai 24 ID/thứ tự câu')
    require(len(root.select('#khao-sat section[id^="mach-r"]')) == 8, 'Sai tám mạch')
    require(len(root.select('#doc-ket-qua details')) == 24, 'Sai 24 đối chiếu')
    require(root.select_one('#cau-minh-hoa .d0-task-number').get_text() == 'Bài 00', 'Thiếu Bài 00')
    require(root.select_one('details#doi-chieu-minh-hoa') is not None, 'Thiếu đối chiếu Bài 00')
    require(not root.select('details[open]'), 'Đối chiếu phải đóng mặc định')
    for r in range(1, 9):
        for n in range(1, 4):
            task = f'd0-r{r}-{n:02}'
            answer = f'doi-chieu-r{r}-{n:02}'
            require(root.select_one(f'#{answer} a[href="#{task}"]') is not None, 'Sai liên kết quay lại ' + task)
            require(root.select_one(f'a[href="#{answer}"]') is not None, 'Thiếu liên kết đối chiếu ' + task)
    # All approved link labels/targets, permitting only the documented course target rewrite.
    approved_links = approval['links']
    actual_links = [[a.get_text(' ', strip=True), a['href']] for a in root.select('a[href]')
                    if not a.find_parent(class_='d0-live-materials') and not a.find_parent(class_='d0-survey-toc')]
    require(len(actual_links) == len(approved_links), 'Sai số liên kết đã duyệt')
    course = REPO / 'docs/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.html'
    for (label, href), (wanted_label, wanted_href) in zip(actual_links, approved_links):
        require(label == wanted_label, 'Nhãn liên kết khác bản duyệt')
        if wanted_href.startswith('https://zomath.vn/'):
            parsed = urlsplit(href)
            require((path.parent / parsed.path).resolve() == course.resolve() and parsed.fragment == 'hoc-lieu-hien-co', 'Sai đích khóa 2027')
        else:
            require(href == wanted_href, 'Sai liên kết đã duyệt ' + wanted_href)
    for a in root.select('a[href]'):
        parsed = urlsplit(a['href'])
        if not parsed.path:
            require(root.find(id=unquote(parsed.fragment)) is not None, 'Anchor không có đích: ' + a['href'])
        elif not parsed.scheme and not parsed.netloc:
            target = (path.parent / unquote(parsed.path)).resolve()
            require(target.is_file(), 'Đích học liệu chưa tồn tại: ' + a['href'])
            if parsed.fragment:
                destination = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
                require(destination.find(id=unquote(parsed.fragment)) is not None, 'Anchor học liệu không có thật')
    live_links = root.select('.d0-live-materials a')
    availability = root.select_one('.d0-live-materials')
    require(availability is not None and availability.find_all('p')[-1].get_text(strip=True) == 'R2–R8: chưa có học liệu để mở.', 'Thiếu trạng thái mạch chưa có học liệu')
    require(len(live_links) == 2, 'Chỉ có hai học liệu đã tích hợp, không thêm đích giả')
    for link, slug in zip(live_links, ('r1_g01', 'r1_g02')):
        target = (path.parent / urlsplit(link['href']).path).resolve()
        wanted = path.parent.parent / slug / 'index.html'
        require(target == wanted.resolve(), 'Sai đích học liệu hiện có ' + slug)
        metadata = yaml.safe_load((ROOT.parent / slug / 'index.qmd').read_text(encoding='utf-8').split('---', 2)[1])
        require(link.get_text(' ', strip=True) == metadata['title'], 'Tên học liệu không khớp nguồn canonical')
    require(not root.select('.d0-private, .d0-retest-task'), 'Rò hồ sơ/câu bổ sung nội bộ')
    require(not root.select('embed, iframe, object, img[src^="data:"]'), 'Còn hình nhúng cũ')
    for asset in ('bbt01.svg', 'hinh_hop.svg'):
        require(root.select_one(f'img[src="hinh/{asset}"]') is not None, 'Thiếu tài sản canonical ' + asset)
        require((path.parent / 'hinh' / asset).read_bytes() == (ROOT / 'hinh' / asset).read_bytes(), 'Tài sản đầu ra stale')
    require(len(root.select('.d0-data-table .r1-data-table')) == 6, 'Sai inventory 6 bảng thường')
    require(len(root.select('.zo-variation-asset table.variation')) == 1, 'Thiếu bảng dấu trợ năng')
    require((path.parent / 'giao_dien/d0.css').read_bytes() == (ROOT / 'giao_dien/d0.css').read_bytes(), 'CSS đầu ra stale')
    script = (ROOT / 'giao_dien/d0_script.html').read_text(encoding='utf-8').strip()
    require(script in path.read_text(encoding='utf-8'), 'Script đầu ra stale')
    rows = root.select('#d0-r1-03 table.variation tr')
    require([[c.get_text(strip=True) for c in r.select('th,td')] for r in rows] ==
            [['x','−∞','','−2','','1','','+∞'], ['f′(x)','','−','0','+','0','+','']], 'Sai bảng dấu')
    print('PASS: approved full text and TeX sequences, 24 questions, Bài 00, 25 closed disclosures, anchors, existing learning links, canonical assets, 6 bordered tables.')


if __name__ == '__main__':
    verify_html()
