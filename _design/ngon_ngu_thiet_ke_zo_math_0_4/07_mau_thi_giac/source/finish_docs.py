from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1]
(R/'BAT_DAU.txt').write_text('''ZO MATH — NGÔN NGỮ HÌNH ẢNH VÀ ÂM THANH 0.4

BẮT ĐẦU
Giải nén toàn bộ gói vào thư mục riêng, mở index.html bằng trình duyệt.
Tại đầu trang, mở “Nền trang” để chọn một trong sáu nền. Khối đọc giữ nền trắng.
Sắc xám, cỡ chữ và giảm chuyển động ở cùng vùng thiết lập. Lựa chọn được nhớ trên trình duyệt khi cho phép lưu.
Mở r1_g01.html để dùng R1-G01 đầy đủ. Không cần cài đặt hoặc đăng nhập.
Nếu trình xem tệp chặn JavaScript/video/tải tệp, tải về và mở bằng trình duyệt.

TRONG LƯỢT XEM NÀY
1. Dùng R1-G01 với nền đã chọn: đi từ Bắt đầu → Bài học → đề/lời giải, thử nhật kí.
2. Xem các nhóm Logo, Biến thiên và Tương tác trong bộ mẫu.
3. Đến PDF để xem bìa/trang kết mới và tải các bản đầy đủ.
4. Đến Chuyển động và âm để xem clip thực sự chuyển động, thử từng bước và nghe cue mới.
5. Xem Phạm vi hệ và quy chuẩn PDF để thấy điều đã xác lập, điều đang thử, điều cần nghiên cứu tiếp.

THAY ĐỔI CỐT LÕI
- Đỏ ZO #EF5350, Vàng ZO #FFCA28, Xám ZO #3E3A35.
- Token liên tiếp từ nhạt đến đậm: red-1..7, yellow-1..7, gray-1..9. Mã màu giữ nguyên.
- Sáu nền: red-1/2, yellow-1/2, gray-2/3. Mặc định gray-3. Khối trắng #FFFFFF.
- Z đỏ, O vàng không viền; mỗi chữ trong một ô Xám ZO độc lập.
- Link không gạch chân. Hover đổi màu/nền; focus có viền; thẻ đang chọn có khung màu.
- BBT giữ các hàng dữ kiện nguồn. Hàm số chỉ dùng một hàng phẳng, không giả lập cao-thấp.
- Ủng hộ ZO Math hiện diện ở đầu trang, cuối chặng phù hợp, vùng tải và trang cuối PDF.
- Bìa/kết mới cho cả tám PDF. Ruột giữ nguyên bản v1.3; không nhận là đã tái dàn toàn văn.
- Thêm clip chuyển động toán 24 giây và hai cue âm ứng viên. Không tự phát âm.

DỮ LIỆU HỌC TẬP
Nhật kí lưu trên trình duyệt đang dùng. Nút tải nhật kí giúp giữ hoặc chuyển ghi chép.
Bạn có thể gửi nhận xét thiết kế trực tiếp trong cuộc trò chuyện. Không cần đặt tệp JSON vào thư mục.
Nút sao chép tài khoản chỉ sao chép số, không thực hiện chuyển khoản.
QR và thông tin nhận ủng hộ giữ nguyên từ nguồn ZO Math.

CÁC THƯ MỤC
pdf/ZO_Math_Quy_chuan_0_4.pdf: quy chuẩn 14 trang, mẫu và lí do.
pdf/r1_editions/: tám PDF R1 có bìa/kết mới.
logos/: SVG/PNG logo, dấu nhấn và biểu tượng nhỏ.
graphics/: đồ thị, hình 2D/3D, biểu đồ, bản vector và raster.
tables/: 13 BBT HTML/Quarto/LaTeX thường, PDF/PNG tương ứng.
social/: bìa, ảnh thu nhỏ, thẻ; retained_0_2/ giữ hệ cũ để đối chiếu.
media/: video, clip chuyển động, audio, cue, phụ đề và nguồn thời gian.
design/: màu/tokens/vai trò, 12 nhóm phạm vi, nghiên cứu và bằng chứng.
source/: CSS/JS và các bộ dựng, xem BUILD.txt.
reference/: nội dung gốc đối chiếu, không phải quy chuẩn 0.4.
qa/: báo cáo kiểm và hình xem trước.

GIỚI HẠN
Đã kiểm dữ kiện, bảo toàn nội dung/công thức, luồng DOM, tệp media, bìa/kết PDF; ảnh và PDF được xem sau render.
Chưa xác nhận bố cục bằng trình duyệt thực hoặc tương thích mọi trình duyệt, do môi trường thiếu khả năng kiểm trình duyệt theo quy trình Sites.
Quarto chưa chạy render; HTML và bảng LaTeX đã dựng sẵn.
Giọng đọc/cue/nhạc/chuyển động là mẫu thử, chưa phải chuẩn âm thanh đã chốt.
Phần ruột PDF vẫn giữ bảng/hình của bản nguồn; BBT phẳng mới nằm trên web và các tệp tables/.
Bản 0.4 là một bước phát triển có nguồn chỉnh sửa, chưa tự nâng thành Design System 1.0.
Bản 0.3 và website/repo chính không bị thay đổi.
''')
(R/'source/BUILD.txt').write_text('''DỰNG VÀ CHỈNH 0.4

Không cần chạy mã để xem. index.html và r1_g01.html tự chứa font/hình/tài nguyên cần dùng.

Môi trường: Python3.12; Node.js; XeLaTeX; pdftocairo; ffmpeg.
Python: fontTools, lxml, PyMuPDF, Pillow, numpy, reportlab, qrcode.
Node: npm install katex@0.19.0 jsdom@26 sharp tại thư mục specimen_0_4.

Bộ phận chỉnh trực tiếp:
- design/color_system.json, tokens.css, roles_0_4.json: màu và vai trò. token_migration.json ghi ánh xạ cũ→mới.
- source/system.css: toàn bộ hệ giao diện; lớp0.4 đặt cuối để thấy thay đổi rõ.
- source/common.js, experience04.js: nhật kí, nền, sắc xám, cỡ chữ, giảm chuyển động và hành vi mẫu.
- source/r1_controller.js: luồng học kế thừa; selector mục lục đã thích ứng với khối trắng.
- source/table_engine.py, export_tables.py: BBT phẳng, công thức LaTeX→MathML, nguồn Quarto/tabular.
- logos/*.svg: vector chỉnh sửa trực tiếp; build_identity.py dựng lại logo.
- source/tex/*.tex: hình toán từ nguồn kế thừa; biên dịch trong source/tex bằng XeLaTeX.
- source/build_pdf_editions.py: tám PDF bìa/kết mới, đối chiếu ruột với nguồn.
- source/build_guide04.py: quy chuẩn14trang.

Thứ tự tái dựng sau khi có đầu vào:
python source/build_identity.py
node source/raster.cjs
python source/export_tables.py
python source/build_table_pdfs.py
python source/build_pdf_editions.py
python source/build_media.py
python source/build_motion.py
python source/build_r1.py
python source/build_guide04.py
python source/build_gallery.py
node source/dom_qa.cjs
node source/gallery_qa.cjs
node source/experience_qa.cjs
python source/verify_sources.py
python source/finish_docs.py
python source/build_gallery.py
python source/package_release.py

Một số bộ dựng đối chiếu dùng thư mục evidence/r1_g01 và specimen_0_2/0_3 cùng cấp trong môi trường nghiên cứu gốc. Đường dẫn được khai báo ở đầu script; khi chuyển sang repo, ánh xạ chúng sang nguồn dự án. Các tài sản đã xuất, CSS/JS, native table sources và PDF nguồn đều có sẵn trong gói. Không tự chạy script lên repo đang xuất bản.
Kiểm DOM không phải kiểm bố cục trình duyệt. Mẫu0.4 không tự thay nguồn sản xuất.
''')
reports=[json.loads((R/'qa'/f).read_text()) for f in ['source_report.json','dom_report.json','gallery_dom_report.json','experience_report.json']]
pdf=json.loads((R/'design/pdf_editions.json').read_text());media=json.loads((R/'qa/motion_media_report.json').read_text())
report={'version':'0.4','total':sum(x['total'] for x in reports),'passed':sum(x['passed'] for x in reports),'groups':[{k:x[k] for k in ['scope','total','passed']} for x in reports],'pdf_editions':len(pdf['editions']),'pdf_body_preservation':all(x['body_unchanged_text'] and x['body_unchanged_render'] for x in pdf['editions']),'motion_decode':all(x['decode_ok'] for x in media),'verified':['23 palette hex values preserved; sequential names and six backgrounds','Original R1 text/math/data preserved except documented source punctuation','13 BBT flat HTML and native LaTeX tables, all grid lines','Navigation and 100 answer/back links, journal, preferences, support links and clipboard in jsdom','New PDF boundaries and unchanged source body text/raster/bookmarks','New motion video24s both orientations, user-controlled audio, discrete motion mode','Images, full PDF boundary contact and14page guide inspected'],'not_verified':['Real-browser layout and accessibility/compatibility certification','Quarto render','Human approval of voice, sonic identity, motion and final logo'],'pdf_scope':'Covers and end pages redesigned. Inner pages retain source v1.3 and source numbering, including original tables/figures.','reports':['source_report.json','dom_report.json','gallery_dom_report.json','experience_report.json','motion_media_report.json','../design/pdf_editions.json']}
(R/'qa/report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));shutil.copy(R/'pdf/ZO_Math_Quy_chuan_0_4.pdf',R.parent/'ZO_Math_Quy_chuan_0_4.pdf');print('Checks',report['passed'],'/',report['total'])
