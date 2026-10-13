"""Scoped cross-package audit of trial HTML; does not render QMD or publish."""
from __future__ import annotations
import argparse
import copy
import html
import json
from pathlib import Path
import re
import shutil
import socket
import subprocess
import tempfile
import time
import sys
sys.dont_write_bytecode = True
from bs4 import BeautifulSoup
import requests
from zo_web_2027_preview import REPO, KIT, PreviewBuilder, audit_path, dump, inventory, projection, sha
from zo_web_2027_g02 import AUTHORIZED_RECORDS, build as build_g02, inv
from zo_web_2027_check import Browser, Checks, GEOMETRY, edge_executable

OLD = REPO / '_audit/zo_web_2027_tuy_chinh_2026-10-08'
OLD_G02 = REPO / '_audit/zo_web_2027_g02_2026-10-08/g02-reading.html'
LOG = REPO / '_design/ngon_ngu_thiet_ke_zo_math_0_4/09_nhat_ki/phan_hoi_tich_hop_web_2027_0_4.md'


def read(path):
    return BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')


def details(doc):
    root = doc.select_one('.reader-content')
    return {
        'inventory': inv(root),
        'regions': [{'ids':[x['id'] for x in n.select('[id]')],
                     'role': n.select_one('.role').get_text(' ',strip=True) if n.select_one('.role') else '',
                     'words':len(projection(n).split()), 'text':projection(n)} for n in root.select('.reading-region')],
        'headings': [{'tag':n.name,'id':n.get('id',n.get('data-anchor-id')),'text':n.get_text(' ',strip=True)} for n in root.select('h2,h3,h4,h5')],
        'tasks': [{'id':n.get('id'), 'kind':n.get('class'), 'text':projection(n),
                   'routes':[(a.get('href'),a.get_text(' ',strip=True)) for a in n.select('a[href]')]}
                  for n in root.select('.zo-learning-task--item,.zo-learning-task--pause') if n.name in ['section','div']],
        'tables': [{'id':n.find_parent(id=True).get('id'), 'rows':len(n.select('tr')),
                    'headings':[x.get_text(' ',strip=True) for x in n.select('thead th')],
                    'text':projection(n)} for n in root.select('table')],
        'disclosures': [{'id':n.get('id'),'role':n.get('class'),'open':n.has_attr('open'),
                        'summary':n.select_one('summary').get_text(' ',strip=True)} for n in root.select('details')],
        'routes': [{'owner':a.find_parent(id=True).get('id') if a.find_parent(id=True) else None,
                    'href':a.get('data-canonical-href',a['href']), 'text':a.get_text(' ',strip=True),
                    'download':a.get('download')} for a in root.select('a[href]')],
        'figures': [{'alt':n.get('alt'),'scale':n.get('style'),'src':n.get('src'),
                    'caption':n.find_parent('figure').get_text(' ',strip=True)} for n in root.select('figure img')],
        'roles':sorted({n.get_text(' ',strip=True) for n in root.select('[data-reading-label]')}),
        'support_owner': 'inside-reader' if root.select_one('.support-region') else 'outside-reader',
        'footer': bool(doc.select_one('#site-footer')),
    }


# Each row specifies the SAME functional question, not equal topic/counts.
ROWS = [
('Thiết kế','Bộ khung/font/token','Kit chung','Kit chung','GIỮ','CSS chung chưa đủ chứng minh DOM/logic chung.'),
('Thiết kế','Nhãn nhiệm vụ','Nhiệm vụ','Nhiệm vụ · Luyện tập/Kiểm tra/Sửa lỗi/Ôn lại','SỬA','Một vai trò nhiệm vụ dùng một nhãn; khu vực học đã xác định ngữ cảnh.'),
('Thiết kế','Nhãn lý thuyết','Khái niệm/Định nghĩa/Định lí/Đối chứng','Lặp tên chương cho nhiều công việc','SỬA','Phân vai theo hoạt động; không lặp tên chương thay vai trò.'),
('Thiết kế','Câu dừng trong bài','Có nhãn Tự kiểm tra','7 pause thiếu nhãn cùng hệ','SỬA','Thêm metadata nhãn, giữ đề/lời giải/ID và trạng thái nguồn.'),
('Thiết kế','Giấy chỉ chứa tiêu đề','Đã có guard ghép vào nhiệm vụ đầu','Builder G02 chưa có guard cùng loại','SỬA','Không coi một header rỗng là một nhịp đọc.'),
('Thiết kế','Hộp tải từng phần','Danh sách không bullet, CTA riêng','Class r1-section-download-list khác selector kit','SỬA','Alias class trong adapter; không sửa link/download.'),
('Thiết kế','Footer website','Không có (mốc footer trước chỉ mở Nhà)','Có footer','SỬA','Bổ sung cùng component ở bản đối sánh G01 mới; không ghi đè bản đã duyệt.'),
('Thiết kế','Ôn lại trình bày nhiệm vụ','Ba bài riêng có tiêu đề/đích','Ba bài dài nằm trong bảng T05','CÒN THIẾU','Chuyển thành ba bài/anchor/solution/CP riêng cần cập nhật kiến trúc nguồn; không chỉ đổi CSS bảng.'),
('Thiết kế','Vai trò D/K','Giải thích trong mạch khái niệm','Giải thích đối tượng + r1-unboxed-label','SỬA','Giữ nội dung khác nhau; thống nhất trọng lượng nhãn hỗ trợ bằng r1-task-label.'),
('Thiết kế','Ủng hộ','Ngoài reader; có grid logo + nội dung','Trong reader do bảo toàn thứ tự nguồn','GIỮ CÓ LÝ DO','Cùng hình thức và trục riêng; vị trí DOM không chứng minh sai toán. Kiểm riêng component.'),
('Thiết kế','Cover','Đơn điệu/cực trị + đồ thị minh họa','GTLN/GTNN + cùng đồ thị nhận diện','GIỮ CÓ LÝ DO','Hình bìa chỉ minh họa, không dùng làm dữ kiện G02; backlog cover theo chủ đề không chặn.'),
('Thiết kế','Nhãn/tiêu đề nằm trong giấy','Có','Có','KIỂM LẠI','Guard orphan, nested, inset trên mọi view; không căn mép ngoài thay trục chữ.'),
('Thiết kế','Lề phải/cột đọc','Giới hạn 816px','Giới hạn 816px','KIỂM LẠI','Cùng measure, không width:100vw; hình rộng cuộn cục bộ.'),
('Thiết kế','Nền hiện hành/Sắc xám','6 radio màu + nút biểu tượng','Cùng template','KIỂM LẠI','Không mất gray; không lặp tên màu; giấy trắng qua sáu nền/no-JS.'),
('Thiết kế','Cỡ hình/BBT','Theo em và nhãn gốc từng asset','Theo em, nhãn gốc 10pt','KIỂM LẠI','Không ép bằng bề rộng giấy; assets khác không được ép cùng số px.'),
('Điều hướng','Ba nhóm vai trò','5 chính / 4 hỗ trợ / 3 tiện ích','5 chính / 2 hỗ trợ / 3 tiện ích','CÒN THIẾU','Không bịa tab Nền/Nhật kí rỗng; thiếu nội dung là thiếu kiến trúc, không đóng là đã đồng bộ.'),
('Điều hướng','Điểm vào','Bắt đầu view riêng','Cách học default + giới thiệu luôn hiện','CÒN THIẾU','Tên/thẩm quyền nguồn khác; cần chốt nguồn Bắt đầu và tránh giới thiệu lặp ở mọi view.'),
('Điều hướng','Giới thiệu lặp ở các view','Giới thiệu thuộc điểm vào','Giới thiệu hiển thị cả khi làm bài/kiểm tra','SỬA','Cô lập bằng visibility theo view đã có; không di chuyển DOM hoặc đổi ID. No-JS/Toàn văn vẫn đọc đầy đủ.'),
('Điều hướng','Kiểm tra → Ôn lại','Liền nhau','Liền nhau','KIỂM LẠI','Sửa lỗi thuộc hỗ trợ; không chen vào mạch chính.'),
('Điều hướng','Cuộn/rail/drawer','Rail fixed, mobile trigger','Cùng controller','KIỂM LẠI','Đo cuối view ngắn/dài, không biến mất/giật; keyboard/focus/no-JS.'),
('Điều hướng','Ôn lại/Nhật kí','Hai view cô lập','Không có Nhật kí','CÒN THIẾU','G02 không thể PASS ca cô lập hai view khi một view chưa có.'),
('Điều hướng','Anchor/ID/luồng nguồn','Giữ nguyên','Giữ nguyên','KIỂM LẠI','Đối chiếu chính xác danh sách có thứ tự, không chỉ đếm.'),
('Logic học','Quan hệ mục tiêu–bằng chứng–quyết định','Chặng + CP + tuyến hỗ trợ','Ma trận đích có nhưng HTML chưa CP độc lập','CÒN THIẾU','Điểm yếu chính không thể khắc phục bằng cùng stylesheet.'),
('Logic học','Ba chặng luyện','Hiện hữu và có checkpoint','Hồ sơ đích C1/C2/C3; nguồn thứ tự L01–05,L11,L06–10','CÒN THIẾU','Không di chuyển DOM lớn bằng JS; cập nhật nguồn theo nhiệm vụ kiến trúc.'),
('Logic học','Chuyển giao có điều kiện','Có tuyến riêng theo mục tiêu','L07/L08 vẫn nằm Luyện tập','CÒN THIẾU','Hồ sơ yêu cầu P01/P02; không đổi ID trong lượt giữ ID này.'),
('Logic học','Luyện mô hình trước Kiểm tra','Có các ví dụ/luyện trước K','Có L05/L11 trước K04','CÓ BẰNG CHỨNG','Nội dung mới đã hiện hữu; không tái sinh 14 nhiệm vụ từ bàn giao cũ.'),
('Logic học','Nền theo dấu hiệu cần dùng','7 đơn vị include canonical + đường quay về','Không có on-nen độc lập','CÒN THIẾU','Chọn đúng N-TXĐ/đạo hàm/cận/mô hình/biến nguyên; không copy nền G01 tùy tiện.'),
('Logic học','Nhật kí','Schema 14 trường','Không có nhật kí riêng','CÒN THIẾU','Cần triển khai đúng schema chung, không dùng lời khuyên ghi lại thay component.'),
('Logic học','Sửa sau L/K/O','Các nhóm có nhiệm vụ/đích xác nhận','S00–05, S-K-E01..06, S-O-E01..06 đã có','CÓ BẰNG CHỨNG','Có bài không chứng minh tuyến quay về CP đã hoàn chỉnh; kiểm hai lớp riêng.'),
('Logic học','Giữ điểm gốc và bằng chứng sau sửa','Quyết định tại CP','Chỉ dẫn/đề đã có, chưa CP tương đương','CÒN THIẾU','Không công bố hoàn tất từ điểm tổng hoặc bài đã xem lời giải.'),
('Logic học','Lịch ôn','2–3 ngày / 7 ngày / 3–4 tuần','Cùng ba khoảng trễ','GIỮ','Khoảng trễ tương đương; cách định danh và điều khiển lượt chưa tương đương.'),
('Logic học','Ngữ cảnh hỗ trợ O/CP','Đích và ngữ cảnh từng lượt','CP-ON là mã văn bản; một answer link cho bảng','CÒN THIẾU','Back hoạt động ở L01 chưa chứng minh hồi phục từng lượt O.'),
('Nội dung','Đối tượng toán chính','Đơn điệu, cực trị cục bộ','GTLN/GTNN trên tập, điểm đạt','KHÁC BIỆT ĐÚNG','Không dùng ma trận mục tiêu G01 thay M1–M6 G02.'),
('Nội dung','Tập xác định/tập đang xét','D/điều kiện trên khoảng','D khác K và điểm bị loại','KHÁC BIỆT ĐÚNG','Cùng thao tác đọc đối tượng, khác yêu cầu so sánh toàn tập.'),
('Nội dung','Đạo hàm bằng 0','Xét đổi dấu, không suy cực trị chỉ từ nghiệm','Lập ứng viên, kể cả điểm không có đạo hàm/đầu mút','KHÁC BIỆT ĐÚNG','Không đồng nhất điều kiện cực trị và đủ ứng viên tối ưu.'),
('Nội dung','Giới hạn và sự đạt','Giới hạn suy luận từ hình/giả thiết','Cận/giới hạn không thay giá trị đạt','KHÁC BIỆT ĐÚNG','Cùng vai trò giới hạn suy luận; phát biểu toán riêng phải giữ.'),
('Nội dung','BBT/đồ thị','Chiều biến thiên, ba đối tượng cực trị','So sánh giá trị, điểm hở/kín, đủ thành phần','KHÁC BIỆT ĐÚNG','Một asset/cùng bảng có câu hỏi khác; không dùng hình bìa thay dữ kiện.'),
('Nội dung','Mô hình/biến nguyên','Phạm vi mục tiêu riêng G01','G02 có lợi nhuận, chi phí bình quân, nguyên, đơn vị','KHÁC BIỆT ĐÚNG','Phải so sánh chức năng H/L/K chứ không yêu cầu đề bài trùng nhau.'),
('Nội dung','Số nhiệm vụ/công thức/hình','Theo nguồn G01','Theo nguồn G02','KHÁC BIỆT ĐÚNG','Không dùng số lượng equal làm tiêu chí đồng bộ; xem inventory đầy đủ kèm theo.'),
('Trình bày','Đề–gợi ý–lời giải','Đề mở, hint/solution đóng','Tương tự; summary cùng component','KIỂM LẠI','Không đổi open/heading của nguồn; kiểm ca mở tất cả, liên kết quay về.'),
('Trình bày','Định nghĩa/định lí','Khối ngữ nghĩa + nhãn trong giấy','Nguồn có khối, nhãn chương đè vai trò','SỬA','Nhãn mở đầu theo Khái niệm/Định nghĩa/Định lí; không chọn màu trang trí.'),
('Trình bày','Bảng quan hệ và bài dài','Bảng giữ quan hệ, nhiệm vụ riêng','T05 dùng bảng chứa ba bài dài','CÒN THIẾU','T05 cần thay mô hình bài Ôn lại, không biến mọi bảng thành card.'),
('Trình bày','Mã quản lí trong văn bản','Tên lỗi/checkpoint thân thiện','CP-ON, N-ĐH-03, E01... vẫn lộ','CÒN THIẾU','Đổi wording canonical cần nhiệm vụ nội dung; ghi từng vị trí trong inventory, không che bằng CSS.'),
('Vận hành','Nghiệm thu/phát hành','G01 thử nghiệm 9/10; chưa production','G02 trial chưa duyệt','GIỮ','Checker PASS không có nghĩa kiến trúc/nội dung đã nghiệm thu.'),
('Vận hành','Hồ sơ current so với lịch sử','Có đoạn còn báo 4/10/chờ nghiên cứu','Có mục bàn giao chưa kiểm + mục G hiện hành','SỬA HỒ SƠ','Thêm trạng thái current đối sánh; không sửa phản hồi lịch sử hoặc tự chứng nhận kiến trúc.'),
('Vận hành','Guard liên gói','Trước đây chủ yếu từng trang','1089 ca local/preservation','SỬA','Thêm đối sánh vai trò/computed metrics và ca âm; báo cáo thiếu kiến trúc riêng không gộp PASS.'),
]


def build(output):
    output = audit_path(Path(output))
    output.mkdir(parents=True, exist_ok=True)
    sources = [OLD/'g01-kit.html',OLD_G02,OLD/'home-reading.html']
    protected = {p.relative_to(REPO).as_posix():sha(p) for directory in ['content/thpt/on_thi_toan_thpt','assets','docs/content/thpt/on_thi_toan_thpt',str(OLD.relative_to(REPO)),str(OLD_G02.parent.relative_to(REPO))]
                 for p in (REPO/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    if not (output/'comparison-protected.json').exists():
        dump(output/'comparison-protected.json',protected)
    before = {'g01':details(read(sources[0])), 'g02':details(read(sources[1]))}
    dump(output/'before-inventory.json',before)
    build_g02(output)
    b=PreviewBuilder(output); b.ui_baseline=OLD/'home-reading.html'
    g01=read(OLD/'g01-kit.html')
    b.normalize_links(g01.body, OLD/'g01-kit.html')
    for name in ['reading-regions.css','web-shell.css','appearance-inline.css','r1-controller.js','site-ui.js','site-footer.css']:
        b.materialize(KIT/name,name)
    # Shared footer is appended below the existing accepted main; never reflow
    # or redesign its reading regions. Original snapshot remains immutable.
    footer,_=b.site_footer()
    g01.select_one('.workspace').append(BeautifulSoup(footer,'html.parser'))
    g01.head.append(g01.new_tag('link',rel='stylesheet',href='site-footer.css'))
    for a in g01.select('.site-top>a:first-child,.course-link,.rail-heading>a,.breadcrumb>a'):
        a['href']='home-reading.html'
    (output/'g01-kit.html').write_text(str(g01),encoding='utf-8')
    home=read(OLD/'home-reading.html'); b.normalize_links(home.body,OLD/'home-reading.html')
    for a in home.select('a[href]'):
        if 'g01-kit.html' in a['href']: a['href']='g01-kit.html'+('#'+a['href'].split('#',1)[1] if '#' in a['href'] else '')
        if 'r1_g02/index.html' in a.get('data-canonical-href',''): a['href']='g02-reading.html'
    b.materialize(KIT/'course-home.css','course-home.css')
    (output/'home-reading.html').write_text(str(home),encoding='utf-8')
    after={'g01':details(read(output/'g01-kit.html')),'g02':details(read(output/'g02-reading.html'))}
    dump(output/'after-inventory.json',after)
    for name in before:
        if before[name]['inventory'] != after[name]['inventory']:
            raise ValueError(name+' changed protected content/MathML/ID/heading/disclosure sequence')
    # Actual source line pointers, including every old feedback entry and every
    # emitted task/table/route (not only selected screenshots).
    source_lines={}
    for name in ['r1_g01','r1_g02']:
        path=REPO/f'content/thpt/on_thi_toan_thpt/hoc_lieu/{name}/index.qmd'
        source_lines[name]=[{'line':i,'text':s} for i,s in enumerate(path.read_text(encoding='utf-8').splitlines(),1) if re.match(r'^#{1,6} ',s) or re.search(r'CP-|N-ĐH|nhat|nhật|on-nen|\.zo-learning',s)]
    dump(output/'canonical-pointers.json',source_lines)
    old_feedback=[]
    for part in re.split(r'(?=^### WEB04-FB-\d{3} —)',LOG.read_text(encoding='utf-8'),flags=re.M)[1:]:
        ident,title=re.match(r'### (WEB04-FB-\d{3}) — ([^\n]+)',part).groups()
        if int(ident[-3:])>28: continue
        old_feedback.append({'id':ident,'title':title.strip(),'historical_record':part.strip(),
             'current_scope':'Các mốc G01 đã duyệt giữ nguyên. G02 chỉ được kiểm các yêu cầu hiện có; không suy PASS cho Nền/Nhật kí/CP chưa tồn tại.'})
    dump(output/'old-defects.json',old_feedback)
    rows=[{'id':f'C{i:02}', 'group':g,'question':q,'g01':a,'g02_before':z,'status':s,'action':act} for i,(g,q,a,z,s,act) in enumerate(ROWS,1)]
    dump(output/'matrix.json',rows)
    lines=['# Ma trận đối sánh R1-G01 / R1-G02 — 08/10/2026','',
      '## Kết luận','',
      'Hai gói chưa nhất quán vì đã nhân bản lớp thị giác nhưng chưa hoàn tất chuyển kiến trúc học G02. Kiểm local trước không phải kiểm tương đương theo vai trò. Đây là thiếu sót triển khai/kiểm của agent, không phải do chủ trì thiếu ý tưởng thiết kế.', '',
      'Phạm vi: nguồn canonical + HTML production hiện có (chỉ đọc) + hai prototype hiện hành; sửa prototype và hồ sơ. Không sửa/render production/PDF, commit/push/phát hành, đổi ID hoặc bịa bài Nền/Nhật kí/CP.', '',
      '## Ma trận chức năng','', '| ID / lớp | Tiêu chí | G01 | G02 trước | Xử lí | Căn cứ / hướng sửa |','|---|---|---|---|---|---|']
    for r in rows:
        lines.append('| '+ ' | '.join(str(r[k]).replace('|','/').replace('\n',' ') for k in ['id','question','g01','g02_before','status','action'])+' |')
    lines += ['', '## Bảo toàn và kiểm kê đầy đủ', '',
      'Các tệp JSON kèm theo giữ toàn bộ heading, nhiệm vụ, bảng, hình, disclosure, nhãn và tuyến link của từng gói; không chỉ đếm. `canonical-pointers.json` chỉ tới heading/mã trong QMD. `before-inventory.json` / `after-inventory.json` giữ chuỗi văn bản, MathML, ID, heading và open có thứ tự. Không so bằng byte hai chủ đề toán khác nhau.', '',
      '| Chỉ số (trước → sau) | G01 | G02 |','|---|---|---|']
    for label,key in [('Công thức','math'),('ID','ids'),('Heading','headings'),('Disclosure','disclosures')]:
        lines.append(f'| {label} | {len(before["g01"]["inventory"][key])} → {len(after["g01"]["inventory"][key])} | {len(before["g02"]["inventory"][key])} → {len(after["g02"]["inventory"][key])} |')
    lines += ['', '## Toàn bộ phản hồi cũ (không xóa lịch sử)', '',
       'Đọc từng bản ghi đầy đủ trong `old-defects.json`. Bảng dưới chỉ lập chỉ mục; không nâng trạng thái thẩm mỹ lịch sử thành PASS kỹ thuật.', '', '| Mã | Vấn đề / quyết định | Trạng thái current |','|---|---|---|']
    for r in old_feedback:
        state='G01 đã duyệt theo FB024–028; G02 kiểm lại yêu cầu tương ứng, chưa được chủ trì duyệt.'
        if r['id'] in ['WEB04-FB-005','WEB04-FB-012','WEB04-FB-020','WEB04-FB-022','WEB04-FB-025','WEB04-FB-028']:
            state='G02 còn khoảng cách kiến trúc trong ma trận; không đóng bằng PASS hình học.'
        lines.append(f'| {r["id"]} | {r["title"]} | {state} |')
    lines += ['', '## Lỗi kỹ thuật lịch sử trước sổ phản hồi', '',
      '- Navbar biến mất/giật: cùng rail fixed; kiểm mọi view và nhiều vị trí cuộn. Không đổi accepted shell.',
      '- Ôn lại lẫn Nhật kí: guard G01 cô lập hai view; G02 thiếu Nhật kí nên ghi không áp dụng, không ghi đã sửa.',
      '- Link cuối rơi khỏi vùng đọc, nhãn/tiêu đề lúc trong/lúc ngoài, double inset, giấy lồng, heading rỗng: kiểm ownership/trục và ghép header rỗng trong adapter G02.',
      '- Phóng hình, tai mèo, nền giấy trùng canvas, mất footer, thiếu Sắc xám: giữ guard riêng từng component, không lấy chụp cover thay kiểm nội dung dài.',
      '- DISC-001..005 và G02-WEB-001 / G02-CHECK-001..002: fallback ẩn, lazy image, logo variant, heading/task selector, rail view ngắn, deep-link nhãn, scope grid Ủng hộ, snapshot hồ sơ. Hồ sơ đầy đủ giữ trong old-defects.json; checker trước không phải bằng chứng current.', '',
      '## Những gì chưa thể đóng trong phạm vi HTML', '',
      'Cần một nhiệm vụ chuyển kiến trúc G02 ở nguồn: Bắt đầu riêng; ba chặng/CP có tiêu chí–đích–xác nhận; Nền được chọn theo nhu cầu; Nhật kí 14 trường; ba bài Ôn lại có đích/lời giải/CP riêng; phân biệt L07/L08 chuyển giao với lõi; wording mã quản lí và ngữ cảnh hỗ trợ. Không được âm thầm sửa QMD, đổi ID hoặc tự tạo ngân hàng bài trong lượt này.', '',
      'Lượt này không phải thẩm định lại chân trị mọi công thức/đáp án, không kiểm PDF/link tải qua mạng, Safari/Firefox, thiết bị thật hoặc screen reader. Kiểm bảo toàn toán và phân bố nội dung không thay nghiệm thu toán. Không có kết luận “hai gói đã đồng bộ toàn bộ”.', '',
      '## Xem thử', '', '[G01 đối sánh](g01-kit.html) · [G02 đã sửa lớp trình bày](g02-reading.html) · [Nhà khóa (bản nối link thử nghiệm)](home-reading.html)', '',
      'Kết quả runtime liên gói: `comparison-qa.json`; hồi quy G02: `qa-results.json`; ảnh: `comparison-images/` và `images/`. Các snapshot đã duyệt trước lượt này vẫn giữ nguyên.']
    (output/'ma_tran_doi_sanh.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    tr=''.join('<tr>'+''.join('<td>'+html.escape(str(r[k]))+'</td>' for k in ['id','group','question','g01','g02_before','status','action'])+'</tr>' for r in rows)
    overview=f'''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Đối sánh G01–G02</title><style>body{{font:16px/1.6 sans-serif;color:#3e3a35;margin:28px}}a{{color:#943b35}}table{{border-collapse:collapse}}td,th{{border:1px solid #dfd7ca;padding:12px;vertical-align:top}}th{{background:#fff9e9}}.scroll{{overflow:auto}}.warn{{padding:20px;background:#fff9e9}}</style><h1>Đối sánh R1-G01 / R1-G02</h1><p class="warn">Chưa đồng bộ toàn bộ: đã sửa lớp trình bày; các khoảng cách kiến trúc học G02 còn mở. Không production/PDF/phát hành.</p><p><a href="g01-kit.html">Xem G01</a> · <a href="g02-reading.html">Xem G02</a> · <a href="ma_tran_doi_sanh.md">Báo cáo và sổ lỗi</a></p><div class="scroll"><table><thead><tr>{''.join('<th>'+s+'</th>' for s in ['ID','Lớp','Tiêu chí','G01','G02 trước','Xử lí','Căn cứ'])}</tr></thead><tbody>{tr}</tbody></table></div></html>'''
    (output/'index.html').write_text(overview,encoding='utf-8')
    dump(output/'comparison-manifest.json',{'inputs':{str(p.relative_to(REPO)):sha(p) for p in sources},'outputs':{n:sha(output/n) for n in ['g01-kit.html','g02-reading.html','home-reading.html']},'rows':len(rows),'old_feedback':len(old_feedback),'source_preserved':True,'script_sha256':sha(Path(__file__))})
    print(json.dumps({'matrix_rows':len(rows),'old_feedback':len(old_feedback),'output':str(output)},ensure_ascii=False),flush=True)


def check(output):
    output=audit_path(Path(output)); c=Checks(output); (output/'comparison-images').mkdir(exist_ok=True)
    before=json.loads((output/'before-inventory.json').read_text(encoding='utf-8'))
    styles={}; prose=GEOMETRY.replace('visible=n=>',"visible=n=>!n.closest('.support-region')&&")
    for name,filename in [('g01','g01-kit.html'),('g02','g02-reading.html')]:
        doc=read(output/filename)
        c.check(name+' exact source projection/order',json.loads(json.dumps(inv(doc.select_one('.reader-content')))),before[name]['inventory'])
        c.check(name+' complete footer',bool(doc.select_one('footer#site-footer[role=contentinfo]')))
        c.check(name+' no duplicate IDs',len(doc.select('[id]')),len({n['id'] for n in doc.select('[id]')}))
        c.check(name+' no heading-only paper (TOC checked at runtime)',[n.get('data-reading-beat',n.get('id','')) for n in doc.select('.reader-content .reading-region') if not n.select('p,li,table,figure,details,.zo-learning-task,.r1-section-toc,.lesson-toc')],[])
        taskpapers=[n if 'reading-region' in n.get('class',[]) else n.find_parent(class_='reading-region')
                    for n in doc.select('.reader-content .zo-learning-task--item') if n.name in ['div','section']]
        c.check(name+' common task role (nonempty inventory)',bool(taskpapers) and all(n and n.select_one('.role').get_text(' ',strip=True) in ['Nhiệm vụ','Xác nhận sau sửa'] for n in taskpapers))
    with socket.socket() as s: s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
    base=f'http://127.0.0.1:{port}'
    with tempfile.TemporaryDirectory(prefix='_tmp_pair_',dir=output) as profile:
        proc=subprocess.Popen([edge_executable(),'--headless=new','--disable-gpu','--no-first-run',f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1','--remote-allow-origins=http://localhost','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        browser=None
        try:
            for _ in range(100):
                try:
                    if requests.get(base+'/json/version',timeout=.3).ok: break
                except requests.RequestException: time.sleep(.1)
            target=requests.put(base+'/json/new?about:blank',timeout=10).json()
            browser=Browser(target['webSocketDebuggerUrl']); browser.call('Page.enable');browser.call('Runtime.enable')
            for width in [1440,430,390]:
                for name,filename in [('g01','g01-kit.html'),('g02','g02-reading.html')]:
                    print('PAIR',name,width,flush=True);browser.viewport(width,960 if width>500 else 844)
                    url=(output/filename).as_uri();browser.navigate(url)
                    browser.click('[name=background][value=yellow-1]'); browser.evaluate('scrollTo(0,0)')
                    browser.screenshot(output/'comparison-images'/f'{name}-cover-{width}.png')
                    tabs=browser.evaluate('[...document.querySelectorAll(".r1-tab")].map(n=>n.id)')
                    for tab in tabs:
                        browser.click('#'+tab); state=browser.evaluate(prose)
                        for k in ['orphan','overflow','axes']:c.check(f'{name}/{width}/{tab}/{k}',state[k],[])
                        for k in ['fits','white','widths','gaps','loaded']:c.check(f'{name}/{width}/{tab}/{k}',state[k])
                        c.check(f'{name}/{width}/{tab}/nested',state['nested'],0)
                        c.check(f'{name}/{width}/{tab}/bounded',state['readerWidth']<=816)
                        if name=='g02':
                            c.check(f'{name}/{width}/{tab}/introduction owned by entry view',browser.evaluate('document.querySelector(".g02-start-region").getClientRects().length>0'),tab in ['r1-tab-cach-hoc','r1-tab-toan-van'])
                            if tab=='r1-tab-bai-hoc':
                                c.check(f'{name}/{width}/TOC is real navigation',browser.evaluate('document.querySelectorAll(".lesson-toc a[href]").length>0'))
                        browser.evaluate('scrollTo(0,500)')
                        c.check(f'{name}/{width}/{tab}/toolbar',browser.evaluate('document.querySelector(".site-top").getBoundingClientRect().top'),0)
                        c.check(f'{name}/{width}/{tab}/navigation visible',browser.evaluate('(()=>{const r=document.querySelector(innerWidth>=1000?".rail":".mobile-trigger").getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight})()'))
                        if tab in ['r1-tab-bai-hoc','r1-tab-on-lai','r1-tab-loi-giai','r1-tab-kiem-tra']:
                            browser.screenshot(output/'comparison-images'/f'{name}-{tab}-{width}.png')
                    browser.navigate(url+'?r1-view=toan-van#bai-hoc')
                    browser.evaluate('document.querySelectorAll(".reader-content details").forEach(n=>n.open=true)')
                    state=browser.evaluate(prose)
                    for k in ['orphan','overflow','axes']: c.check(f'{name}/{width}/all-open/{k}',state[k],[])
                    c.check(f'{name}/{width}/all-open/fits',state['fits'])
                    # Compare role components on the same viewport; heading tag
                    # content lengths are not a false equal-height invariant.
                    styles[name,width]=browser.evaluate('(()=>{const sels=[".reader-content",".reader-content .reading-region:has(:is(section,div).zo-learning-task--item)",".reader-content .role",".reader-content details.zo-learning-guidance>summary",".reader-content details.r1-solution>summary",".r1-tab",".site-top",".support-content h3",".zo-site-footer"];return sels.map(s=>{const n=document.querySelector(s),c=getComputedStyle(n);return [s,c.fontFamily,c.fontSize,c.lineHeight,c.paddingLeft,c.paddingRight,c.borderRadius]})})()')
                    browser.evaluate('document.querySelector(".reader-content .role").style.transform="translateX(8px)"')
                    c.check(f'{name}/{width}/negative inset',bool(browser.evaluate(prose)['axes']))
                    browser.evaluate('document.querySelector(".reader-content .role").style.transform=""')
                    if name=='g01':
                        browser.click('#r1-tab-on-lai');c.check(f'G01/{width}/review excludes journal',browser.evaluate('document.getElementById("nhat-ky").getClientRects().length===0'))
                        browser.click('#r1-tab-nhat-ky');c.check(f'G01/{width}/journal isolated',browser.evaluate('document.getElementById("nhat-ky").getClientRects().length>0'))
                    browser.navigate(url+'#ung-ho');browser.screenshot(output/'comparison-images'/f'{name}-support-{width}.png')
                    browser.evaluate('scrollTo(0,document.documentElement.scrollHeight)');browser.screenshot(output/'comparison-images'/f'{name}-footer-{width}.png')
                c.check(f'{width} pair common computed role styles',styles['g01',width],styles['g02',width])
            # A cross-package mismatch must be detected, even when each page fits.
            bad=copy.deepcopy(styles['g02',390]); bad[2][2]='19px'
            c.check('Negative pair guard detects changed role type',bad!=styles['g01',390])
        finally:
            if browser:
                try: browser.call('Browser.close')
                except Exception: pass
                browser.ws.close()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=10)
    protected=json.loads((output/'comparison-protected.json').read_text(encoding='utf-8'))
    changed=[p for p,h in protected.items() if not (REPO/p).is_file() or sha(REPO/p)!=h]
    c.check('Every protected production and previous snapshot unchanged',[p for p in changed if p not in AUTHORIZED_RECORDS],[])
    dump(output/'comparison-qa.json',{'checks':c.checks,'temporary_profile_removed':not Path(profile).exists(),
        'authorized_record_updates':[{'path':p,'before':protected[p],'after':sha(REPO/p)} for p in changed if p in AUTHORIZED_RECORDS],
        'limits':['Architecture gaps stay OPEN; not mathematical truth acceptance','Edge only; no PDF, actual touch or screen reader'],
        'script_sha256':sha(Path(__file__))})
    failed=[n['name'] for n in c.checks if not n['pass']]
    print(json.dumps({'checks':len(c.checks),'failed':failed},ensure_ascii=False));return int(bool(failed))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['build','check']);p.add_argument('--output',required=True);a=p.parse_args()
    sys.exit(check(a.output) if a.command=='check' else build(a.output))
