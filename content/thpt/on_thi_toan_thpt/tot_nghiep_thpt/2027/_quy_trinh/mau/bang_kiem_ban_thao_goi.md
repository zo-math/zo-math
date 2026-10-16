# Bảng kiểm áp dụng mẫu bản thảo gói

Phiên bản mẫu: **1.0** · Ngày: 16/10/2026 · Phạm vi: bản thảo gói R1 của khóa 2027. Đây là công cụ áp dụng, không tạo kiến trúc hoặc chuẩn hiển thị mới.

Nguồn: [01 — chức năng học tập](../01_kien_truc_hoc_tap.md), [07 — trình bày](../07_quy_chuan_cau_truc_trang_nguoi_hoc.md), [02/1.4 — cách dùng](../02_quy_trinh_va_nghiem_thu.md#ap-dung-mau-ban-thao), [khung bản thảo](ban_thao_goi.md), [tổ chức nguồn](../quy_chuan_goi_qmd.md). G01/G02 là học liệu đối chiếu theo chức năng; nội dung toán và số lượng nhiệm vụ thuộc gói đang viết.

## Cách lập kết quả

Lập kết quả trong `hoc_lieu/<ma_goi>/_quy_trinh/ho_so/` hiện có, không sửa bảng mẫu thành trạng thái một gói. Có thể dùng một tệp cho hai thời điểm, phân rõ kết quả trước viết và trước trình. Đối với gói đã có bản thảo, ghi áp dụng hồi cứu trước bước kế tiếp; không tuyên bố đã dùng mẫu trước khi viết.

Ghi mã/tên gói, phiên bản và SHA-256 bản thảo; phiên bản/hash hai mẫu; phiên bản/hash nguồn G01/G02 thực sự đối chiếu; tài liệu kiểm, ngày, người thực hiện và phạm vi. Mỗi dòng phải có đích cụ thể (tệp + mục/anchor, hình + trang nếu có), không điền “đã có” hoặc PASS chỉ vì đếm đủ.

Trạng thái: **Đạt / Cần sửa / Chưa kiểm / Không áp dụng có lí do / Hoãn theo chốt của chủ trì**. Khi hoãn, ghi đúng chỉ thị, việc và giai đoạn phải xử lí, phép kiểm và giới hạn công nhận; không đổi thành Đạt. Kết luận tách nội dung, đường học, hình, bản xuất, chủ trì duyệt và phát hành. Chỉ 03 sở hữu việc hiện hành và bước tiếp theo.

## A. Trước viết nội dung

| ID | Điều cần xác định | Nguồn sở hữu | Kết quả/vị trí bằng chứng | Trạng thái |
|---|---|---|---|---|
| A01 | Nhiệm vụ được giao, người học, mục tiêu, phạm vi lõi/loại trừ và nguồn chính thức cần đọc | Hồ sơ gói; Kế hoạch trong phần còn hiệu lực | Chưa điền | Chưa kiểm |
| A02 | Phiên bản mẫu, quy tắc hiện hành và nguồn G01/G02 thực sự dùng làm đối chiếu | 02/1.4; 08 | Chưa điền | Chưa kiểm |
| A03 | Bản đồ từng thành phần: tương ứng ở gói mẫu, vị trí dự kiến, phần không áp dụng và khác biệt có lí do | 01; 07 | Chưa điền | Chưa kiểm |
| A04 | Mục tiêu ↔ phần học/ví dụ ↔ luyện/Điểm dừng ↔ kiểm tra ↔ ôn ↔ lỗi/nền | Hồ sơ gói; 01/2.1–2.8 | Chưa điền | Chưa kiểm |
| A05 | Nhóm nhiệm vụ, chức năng, cách đánh số, cặp đề–đáp án và lịch sử lộ; không sao số bài G01/G02 | 01/QD_025; 07/6.2 | Chưa điền | Chưa kiểm |
| A06 | Vị trí nguồn đang sửa, tài nguyên nháp và kết quả kiểm; không phát sinh kho mới | Quy chuẩn gói, mục Khởi tạo | Chưa điền | Chưa kiểm |
| A07 | Khác biệt cần chốt được báo trước, ghi lí do và phạm vi đã được chấp thuận | 02/1.4; chỉ thị chủ trì | Chưa điền | Chưa kiểm |

Bảng đối chiếu cấu trúc dùng trước viết:

| Thành phần/chức năng | Vị trí trong G01/G02 đã đọc | Vị trí dự kiến ở gói mới | Giữ/đổi/không áp dụng | Lí do và căn cứ chốt nếu đổi |
|---|---|---|---|---|
| Bắt đầu, Khởi động, từng mục học/Gợi mở/Tự kiểm tra, Luyện tập/Điểm dừng, Kiểm tra, Ôn lại, Ôn nền, Sửa lỗi, Nhật kí, Lời giải, Nguồn — tách thành các dòng thực | Chưa điền | Chưa điền | Chưa điền | Chưa điền |

## B. Trước trình duyệt bản thảo

| ID | Điều phải đọc/kiểm thực chất | Nguồn sở hữu | Kết quả/vị trí bằng chứng | Trạng thái |
|---|---|---|---|---|
| B01 | Bắt đầu đủ mục tiêu, tiên quyết, cách học/điểm vào, sơ đồ đúng nghĩa và điều kiện hoàn tất | 01/2.2–2.3,2.7; 07/4 | Chưa điền | Chưa kiểm |
| B02 | Bài học và Luyện tập riêng; bốn khu vực chính và hỗ trợ ngang, không biến mục lục thành chuỗi bắt buộc | 01/2.2.1; 07/3–4 | Chưa điền | Chưa kiểm |
| B03 | Khởi động là nhiệm vụ kiểm nền thật, có phản hồi và đường chọn nền; không thay Gợi mở | 01/2.3; G01/G02 | Chưa điền | Chưa kiểm |
| B04 | Gợi mở nằm trước lời giải thích của đúng mục, nhãn và số liên tục toàn nhóm, lời dẫn đúng chức năng | 01/QD_025; 07 bổ sung QD_025 | Chưa điền | Chưa kiểm |
| B05 | Lời giảng, định nghĩa/định lí đủ điều kiện; đã đọc đúng tài liệu/trang chính thức, không tự tạo phát biểu | Nguồn toán gói; 07/4.2 | Chưa điền | Chưa kiểm |
| B06 | Ví dụ đủ lời giải; Tự kiểm tra để tự làm, không dùng lại ví dụ đã giải làm bằng chứng mới; khép lại có điều cần tự giải thích | 01/2.1,2.5; G01/G02 | Chưa điền | Chưa kiểm |
| B07 | Mục/tiểu mục và từng nhóm nhiệm vụ đánh liên tục; tên, số, chức năng, đề–đáp án và dẫn chiếu cùng ánh xạ | 07/6.2; danh mục nhãn | Chưa điền | Chưa kiểm |
| B08 | Luyện tập có mục tiêu từng chặng, Điểm dừng đủ tiêu chí và quyết định; số bài không reset | 01/2.4; 07/4.3 | Chưa điền | Chưa kiểm |
| B09 | Mỗi tuyến hỗ trợ đúng lỗi và từng ý; câu xác nhận kiểm đúng tình huống/biểu diễn, còn mới; trở về đúng nơi gọi; hết bài mới không tự nhận đạt | 01/2.5–2.6; 02/1.3 | Chưa điền | Chưa kiểm |
| B10 | Kiểm tra cho vào khi chuẩn bị hoặc tự tin, tự lực toàn lượt, không chia đợt, kết thúc trước hỗ trợ và giữ bài ban đầu | 01/2.3.1; 07/4.4 | Chưa điền | Chưa kiểm |
| B11 | Thời lượng/thang điểm có phạm vi đề xuất rõ; đề–lời giải đủ ý; điểm thành phần cộng rõ; bảng mục tiêu đúng bằng chứng, không bù thiếu bằng tổng điểm | 01/2.3,2.7; 07/4.4 | Chưa điền | Chưa kiểm |
| B12 | Ôn lại có ngày hẹn, khoảng trễ, mục tiêu lấy mẫu, Điểm dừng, giới hạn kết luận và đường hỗ trợ riêng | 01/2.7; 07/4.5 | Chưa điền | Chưa kiểm |
| B13 | Ôn nền dùng nguồn chung phù hợp; thẻ mới đủ giải thích/ví dụ/câu khác/đáp án/tiêu chí/nơi về, không có bản sửa song song | 01/2.6; 07/5 | Chưa điền | Chưa kiểm |
| B14 | Sửa lỗi đủ đề–tiêu chí–đích xem lại theo ý–đáp án–đường quay về; câu đã lộ không đổi thành mới; bảng ghi đủ tên nhiệm vụ | 01/2.5; 07/3,5,6 | Chưa điền | Chưa kiểm |
| B15 | Phối hợp và Chuyển giao phân biệt, có tiên quyết, đề/lời giải riêng nếu thật sự cần; không ép thành lõi | 01/2.5.1; 07 | Chưa điền | Chưa kiểm |
| B16 | Nhật kí đúng nguồn 14 trường; không bắt ghi mỗi câu; ví dụ ghi giả lập và không lộ đáp án câu xác nhận chưa dùng | 01/2.8; nguồn Nhật kí chung | Chưa điền | Chưa kiểm |
| B17 | Mọi đề có lời giải đúng nhóm/tên/ý; tách vị trí thì có đường đi/về, xử lí tại chỗ thì không nhân lời giải hoặc tạo nhóm trống | 07/5.3,6.2; quy chuẩn gói | Chưa điền | Chưa kiểm |
| B18 | Toán đúng miền, dấu, hướng, đơn vị, mức đạt/chưa đạt và giới hạn suy luận; LaTeX cho số/biểu thức, phân số và ngoặc đúng quy chuẩn | Nguồn toán; quy chuẩn kí hiệu/dấu ngoặc | Chưa điền | Chưa kiểm |
| B19 | Từng hình khớp dữ kiện/đáp án; nhãn đọc được, điểm kín/hở đúng; nếu có hệ trục tọa độ thì hai trục cắt nhau đúng tại gốc, không đứt/lệch; xem thực thay vì chỉ tin kiểm vector | 07/6.1; yêu cầu chủ trì ngày 16/10/2026 về hình G03 | Chưa điền | Chưa kiểm |
| B20 | Chính văn và nhãn liên kết dùng tên có nghĩa, không dùng mã quản lí; liên kết tồn tại và thực sự dẫn đúng nội dung | 07/6.2; đối chiếu ngữ nghĩa thủ công | Chưa điền | Chưa kiểm |
| B21 | Bản trình duyệt đúng phiên bản, hết chỗ trống/ghi chú nội bộ; phân biệt nội dung và HTML/PDF; ghi rõ những phần được hoãn | 02/4; quy chuẩn gói | Chưa điền | Chưa kiểm |
| B22 | Trạng thái đã sửa/đã kiểm/chủ trì duyệt/phát hành tách biệt; không sửa receipt cũ và không kế thừa PASS sai phạm vi | 02/4; 03 | Chưa điền | Chưa kiểm |

## Bảng ngoại lệ và việc hoãn

| ID kiểm | Khác mẫu hoặc lỗi quan sát | Lí do/phạm vi | Chỉ thị chốt của chủ trì | Giai đoạn phải khép | Phép kiểm và giới hạn công nhận |
|---|---|---|---|---|---|
| Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |

## Kết luận trước trình

Nêu phần đã đạt, phần cần sửa/chưa kiểm và ngoại lệ có căn cứ. Lỗi toán/đường học thiết yếu chưa khép không được trình như đã đạt; việc hoãn chỉ có hiệu lực đúng phạm vi chủ trì chốt. Mẫu và kiểm kỹ thuật không thay đọc toàn nội dung, xem hình hoặc chủ trì duyệt. Chuyển QMD sau duyệt bản thảo theo quy chuẩn gói; tài nguyên chính thức phải dựng lại bằng công cụ ZO Math. Mẫu bản thảo không chứa CSS/JS, thiết kế lại trang hoặc chỉ tiêu số bài.
