# Đối chiếu và kiểm bản thảo R1-G05 · 20/10/2026

## Phạm vi và bằng chứng

Bản thảo 0.1 tại [nguồn duy nhất](../ban_thao/noi_dung.md). Chủ trì đã duyệt phương án và giao viết; chưa duyệt bản thảo hoặc hướng bìa. Mẫu nội dung 1.4, bảng kiểm 1.7 cùng bổ sung B25/B26 hiện hành. Hash nguồn đối chiếu và mẫu nằm trong `tiep_nhan.json`; hash bản đang trình và các kiểm tự động trong `kiem_ban_thao.json`.

Đối chiếu trước viết là báo cáo khảo sát được chủ trì duyệt trong cuộc trò chuyện; hồ sơ tệp này hợp nhất kết quả trước viết và kết quả rà sau viết, không giả rằng tệp đã tồn tại trước khi viết. Nguồn sản phẩm G01–G04, HTML/PDF hiện hành đã được đọc ở lượt khảo sát; lượt này đối chiếu lại những đoạn/mẫu cần biên soạn và bảo toàn hash. Không dùng báo cáo PASS thay đọc sản phẩm.

## A. Trước viết

| ID | Kết quả và vị trí | Trạng thái |
|---|---|---|
| A01 | Hồ sơ `goi/R1_G05.md`, duyệt trực tiếp trong hội thoại; CT tr.95–96,106–107; SGK Bài 2/Bài 5 | Đã xác định |
| A02 | Mẫu 1.4, bảng kiểm 1.7, 01/07, khối nội dung, ngoặc LaTeX, geometry v0.1; hash nguồn G01–G04 trong tiếp nhận | Đã đọc theo phạm vi |
| A03 | Bảng chức năng dưới đây; thay nội dung theo khoảng trống lập mô hình, không sao quota | Đã đối chiếu |
| A04 | Sáu mục tiêu, bảng độ phủ tại hồ sơ gói; mục Kiểm tra ghi phần vận tốc/gia tốc cần bằng chứng bổ sung | Đã xác định |
| A05 | 29 nhiệm vụ, 8 Gợi mở, 8 Ví dụ, 8 Điểm dừng; số theo loại toàn gói; lời giải phản chiếu owner | Đã thiết kế, kiểm lại sau viết |
| A06 | Một Markdown tại ban_thao/noi_dung.md, nguồn và ảnh riêng tại ban_thao/hinh | Đúng phạm vi |
| A07 | Chủ trì cho phép bổ sung cơ chế hình; chưa cho QMD/HTML/PDF. Minh họa bối cảnh dùng bộ dựng nguồn riêng, không thay chuẩn chung | Có căn cứ chỉ thị |

## Đối chiếu theo chức năng

Nguồn đối chứng: `hoc_lieu/r1_g01/index.qmd` (G01), `r1_g02/index.qmd` (G02), `r1_g03/index.qmd` (G03), `r1_g04/index.qmd` (G04), cùng HTML/PDF tại vị trí chuẩn đã kiểm trong lượt khảo sát. Tên rút gọn trong hồ sơ nội bộ không là nhãn người học.

| Chức năng/nguồn sở hữu | Vị trí đối chứng | Vị trí G05 | Giữ/đổi và lí do |
|---|---|---|---|
| Bắt đầu, mục tiêu — 01/07 | Cả bốn gói: Bắt đầu; mục tiêu lần lượt 5/5/7/6 dòng | #bat-dau | Giữ một bảng đủ mục tiêu; sáu dòng do phạm vi |
| Bài học → Câu hỏi dẫn đường — 07 | Cả bốn gói: đầu #bai-hoc | #bai-hoc, details đóng | Giữ câu hỏi, không lặp mục tiêu/Mục lục |
| Bài học → Khởi động — 01 | G01/G02 #bắt-đầu-từ-đâu; G03 #khởi-động; G04 #khoi-dong | NV01–03, CP01 | Ba nhiệm vụ theo nền cần kiểm, không chép số lượng |
| Bài học → mục 1 → Gợi mở → giải thích | G02 từng mục; G03 GM01–06; G04 GM01–05 | #bh-11/12/13, GM01–03, VD01–02 | Tách đại lượng, tốc độ và chi phí biên do cách tháo gỡ khác nhau |
| Bài học → mục 2 → Gợi mở → giải thích | G02 mục 5 chủ yếu công thức cho sẵn; G04 #bh-05 | #bh-21/22, GM04–05, VD03–04 | Bước mới tự lập mô hình hình học và giá–lượng |
| Bài học → mục 3 → Gợi mở → giải thích | G02 các mục miền/đạt được; G03/G04 mục mô hình | #bh-03, GM06, VD05–06 | Gọi lại phương pháp, tập trung chứng minh trên miền thật |
| Bài học → mục 4 → Gợi mở → giải thích | G02 mục 5.1, N-NGUYÊN-01 | #bh-04, GM07, VD07 | Giữ điều kiện chọn hai ứng viên, thêm phản ví dụ làm tròn |
| Bài học → mục 5 → Gợi mở → giải thích | G03/G04 mô hình có phạm vi áp dụng | #bh-05, GM08, VD08 | Trả kích thước, kiểm giả thiết; không tạo định lí mới |
| Ví dụ và nhiệm vụ trong Bài học | G01–G04: ví dụ đã giải, nhiệm vụ lời giải tách | VD01–08; NV04–10 | Giữ phân biệt học từ mẫu và bằng chứng độc lập |
| Bài học → Khép lại | G01/G02 Khép lại; G03/G04 kết luận phạm vi | Cuối #bai-hoc | Tự giải thích, không tuyên bố hiểu chỉ vì đọc xong |
| Luyện tập | G01/G02 ba chặng, G03/G04 hai chặng | #luyen-tap; NV11–16, CP02–04 | Ba chặng theo mục tiêu, không định mức dùng chung |
| Kiểm tra | G04 bốn nhiệm vụ, giới hạn lấy mẫu được ghi rõ | #kiem-tra; NV17–20, CP05 | Bốn nhiệm vụ, 75 phút đề xuất; không tổng điểm, không chặn quyền vào |
| Ôn lại | Cả bốn có ba lượt theo kiến trúc | NV21–23, CP06–08 | Chuyển bối cảnh, giữ ngày thực và giới hạn lấy mẫu |
| Ôn nền | G01/G02 include chung; G03 có nền tại gói; G04 dẫn liên gói | #on-nen | Liên kết nguồn chung trong Markdown; chưa tạo include QMD hoặc thẻ mới |
| Sửa lỗi | G01–G04 bảng bốn cột, nhóm theo nơi phát hiện | #sua-loi; 12 dòng, NV24–29 | Giữ đúng vai trò; ghi rõ câu không đo đủ, câu đã lộ/hết mới |
| Nhật kí | G01/G02/G04 include chung; G03 hiện viết tại nguồn gói | #nhat-ki | Dẫn một nguồn chung 14 trường; không sao thành mẫu thứ hai |
| Lời giải | Cả bốn nhóm theo owner, đi–về đúng nhãn | #loi-giai; lg-01–29 | Cặp tên/số/đích giữ nhất quán |
| Điều hướng | Nhãn/số/module dùng chung, riêng nội dung gói | Anchor Markdown và liên kết hỗ trợ | Chưa tạo shell, CSS, JS, binding production |
| Nguồn | Chú thích sau nội dung, danh mục cuối | .zo-source-note và #nguon | Nguồn toán chính thức; số liệu bài do tác giả tạo, không giả dữ liệu thực |

Không có hộp Cách thực hiện riêng vì thao tác đã rõ trong chính văn. Không có bảng biến thiên hoặc đồ thị hàm mới: các lập luận dấu được viết đủ bằng LaTeX; gói tập trung lập mô hình, không yêu cầu thêm hình chỉ để đủ loại. Năm minh họa bối cảnh có chức năng cụ thể và đã tạo, không dùng thiếu công cụ làm lí do bỏ hình. Nếu thêm BBT/đồ thị sau này phải đi bộ dựng đúng vai trò, không dùng bộ minh họa này thay thế.

## B. Trước trình bản thảo

| ID | Bằng chứng/giới hạn cụ thể | Kết quả |
|---|---|---|
| B01 | #bat-dau có một bảng mục tiêu, tiên quyết, hỗ trợ và điều kiện hoàn tất | Đã rà nguồn |
| B02 | Bài học/Luyện riêng; details câu hỏi đóng; quyền chọn điểm vào | Đã rà nguồn |
| B03 | NV01–03 có LG01–03, CP01 và đích nền | Đã rà nguồn |
| B04 | GM01–08 nằm trong đúng mục, trước giải thích và có cầu nối | Đã rà nguồn |
| B05 | Tốc độ, biên, miền, quy trình có nguồn/trang; phương pháp trên đoạn có điều kiện hữu hạn ứng viên | Đã rà nội dung, chờ chủ trì |
| B06 | VD01–08 giải tại chỗ; NV04–10 tách lời giải; khép lại nêu giới hạn | Đã rà |
| B07 | Dãy NV/GM/VD/CP, 29 cặp đề–lời giải; kiểm tự động | Đạt kiểm nguồn |
| B08 | Ba chặng, CP02–04 có tiêu chí, đường hỗ trợ và giới hạn | Đã rà |
| B09 | Không dùng câu chi phí xác nhận chuyển động, câu hàng rào xác nhận riêng cắt hộp; thiếu câu mới ghi rõ | Đã rà, ngân hàng hữu hạn |
| B10 | #kiem-tra: đủ tự tin được vào, một lượt, giữ bài trước trợ giúp | Đã rà |
| B11 | 75 phút là đề xuất, không thang điểm; bảng từng mục tiêu; NV14 bổ sung chuyển động nếu còn độc lập | Đã rà phạm vi đo |
| B12 | Ba lịch, CP06–08 có ngày thực, phần lấy mẫu và câu mới phù hợp | Đã rà |
| B13 | Các link nguồn nền tồn tại; không tạo thẻ mới rỗng | Đạt nguồn; giao diện chưa dựng |
| B14 | NV24–29 có đủ đề/lời giải; tuyến chia theo nơi phát hiện, giới hạn từng ý | Đã rà |
| B15 | Không tạo nhánh Phối hợp/Chuyển giao riêng vì các chuyển bối cảnh đã thuộc lõi được duyệt | Không áp dụng có lí do |
| B16 | #nhat-ki dẫn nguồn chung đủ 14 trường, không buộc ghi mỗi câu | Đã rà nguồn; include khi chuyển QMD |
| B17 | 29 đề, 29 lời giải cùng tên/số và đích đi/về; kiểm tự động | Đạt nguồn |
| B18 | Guard ngoặc; kiểm biểu thức độc lập, duyệt dấu/miền/đơn vị và diễn giải | Đã kiểm tác giả; không là nghiệm thu độc lập |
| B19 | Năm minh họa + một hướng bìa, SVG/PNG, nguồn/token/font/hash; xem sáu PNG cuối, sửa glyph từ nguồn; không có BBT/đồ thị mới | Đã kiểm ảnh rời; chưa kiểm trang rộng/hẹp/PDF |
| B20 | Link tồn tại, anchor đúng; thay mã gói trong nhãn chính bằng tên có nghĩa | Đạt nguồn |
| B21 | Không chỗ trống biên soạn; duy nhất bản 0.1; file hash gắn kiểm | Sẵn sàng trình bản thảo |
| B22 | Phạm vi duyệt khác nội dung/ảnh duyệt; không sửa receipt của sản phẩm cũ | Đã tách trạng thái |
| B23 | Không có hộp chỉ dẫn lặp; điều kiện của bài đặt nhìn thấy | Đã rà |
| B24 | Rà đề/giải/bảng/alt: miền thực khác tập xác định; trung bình/tức thời; tổng/trung bình/biên; điểm đạt và đơn vị | Đã rà tác giả |
| B25 | Ma trận 12 nút thắt, 8 cột ở hồ sơ; Sửa lỗi bốn cột; cảnh báo câu đã lộ trên lớp | Đã đối chiếu mục tiêu, chưa có dữ liệu học sinh |
| B26 | Bảng mục tiêu, hỗ trợ, chặng, bằng chứng, sửa lỗi có chức năng riêng; không đặt điểm hoặc profile tự tạo | Đã rà nguồn; giao diện chờ giai đoạn sau |

## Ngoại lệ và phần chưa thực hiện

- Chủ trì yêu cầu chưa QMD/HTML/PDF: chưa kiểm bản đọc web rộng/hẹp, bàn phím, điều hướng shell, số trang hoặc PDF. Không dùng kiểm ảnh rời hay đếm liên kết để thay phần này.
- Bìa hiện là phác hướng có nguồn riêng, chưa có binding bìa chính thức hoặc bộ tỉ lệ. Chờ duyệt hướng trước khi phát triển.
- Minh họa tham số là bộ bổ sung cục bộ được phép bởi nhiệm vụ hiện tại, chưa nâng thành công cụ ZO Math dùng chung. Khả năng và giới hạn ở README hình.
- Checker schema/readiness mặc định kiểm G01/G02 báo ba đường hình G01 không tìm thấy (`do_thi_11.tex`, `do_thi_12.tex`, `do_thi_13.tex`). Giữ nguyên báo lỗi trong tiếp nhận, không sửa G01 hoặc đổi thành PASS. G05 chưa có manifest production theo quy chuẩn khởi tạo; không sao manifest để chạy readiness giả.
- Cổng điều hành tài liệu đạt 192/192 trước viết; đây chỉ là đồng bộ tài liệu. Bản thảo và ảnh vẫn chờ chủ trì duyệt; không có phản hồi thử nghiệm học sinh.

## Kiểm đã chạy

Qua launcher repository-local, với cờ `-B`:

- `scripts/zo_2027_governance_check.py`.
- `scripts/zo_learning_architecture.py schema` và `readiness`: lỗi ngoài phạm vi như trên.
- `ban_thao/hinh/sinh_minh_hoa.py`: tạo SVG/PNG; từ chối ba ca dữ liệu không hợp lệ; kiểm nhãn và vector.
- `ho_so/kiem_ban_thao.py`: liên kết/anchor, nhãn, ngoặc LaTeX, điều kiện cấu trúc, kiểm số học–đại số độc lập bằng SymPy và duyệt hết lựa chọn nguyên hữu hạn, kiểm hash bảo toàn.

Tất cả đường rút gọn trong hai dòng cuối tính từ `_quy_trinh` của G05. Lệnh tái chạy đầy đủ nằm trong README hình và mã kiểm. Không chạy render, commit hoặc publish. Kiểm máy không chứng minh hiệu quả sư phạm; chủ trì duyệt riêng nội dung và hướng bìa.

Bản đang trình: SHA-256 `1917e6128609c9038a2a369317a71b717edef9cbe9b8285256823804d17c8a13`. Kiểm tự động: **915/915**; bảo toàn **850** tệp.
