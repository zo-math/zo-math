# Mẫu hồ sơ một gói mới

Phiên bản: 0.9 · Ngày biên tập: 16/10/2026 · Ma trận đồng bộ theo QD_021–025.

## Hệ nhãn của gói

Nạp từ điển QD_025 của chương trình (kế thừa QD_023, bổ sung Gợi mở), không sao chép thành từ điển cục bộ hoặc giới hạn ở R1. Hồ sơ phải có bảng áp dụng: nguồn/ID hoặc locator, owner, nhãn kiến trúc/loại, chức năng/độ lộ, dãy số toàn nhóm, tiêu đề dự kiến, đề–đáp án, dẫn chiếu/quay về và trạng thái duyệt. Tách đơn vị, lần bố trí và nguồn include chung; ghi thiếu phân loại/ID rõ. Ghi các trạng thái riêng: mapping_only, nguồn đã áp dụng, nguồn đã kiểm, HTML đã kiểm, chủ trì duyệt, phát hành. Không điền sẵn achieved hoặc dùng số hộp chứng nhận đủ nội dung.

Đây là mẫu trống, chưa phải gói đang sản xuất. Sao chép vào `goi/` sau khi xác định mã thật. Không sửa mẫu để ghi trạng thái một gói cụ thể.


[Điểm vào](../README.md) · [Kiến trúc](../01_kien_truc_hoc_tap.md) · [Quy trình](../02_quy_trinh_va_nghiem_thu.md).

## Khởi tạo nơi biên soạn

Áp dụng mục [Khởi tạo gói mới và quản lí bản thảo](../quy_chuan_goi_qmd.md#khởi-tạo-gói-mới-và-quản-lí-bản-thảo) của quy chuẩn gói. Ghi đường dẫn gói, bản thảo đang sửa, tài nguyên bản thảo và căn cứ chủ trì giao tạo. Đây là mẫu áp dụng cho G04 và các gói tiếp theo; khi thực tế cần cải tiến, cập nhật nguồn quy định và mẫu liên quan trong cùng lượt. Không tạo QMD trước khi bản thảo được duyệt hoặc sao tài nguyên nháp thành tài nguyên chính thức.

## Mẫu biên soạn và kết quả áp dụng

Nạp [khung bản thảo](ban_thao_goi.md) và [bảng kiểm](bang_kiem_ban_thao_goi.md) theo [02/1.4](../02_quy_trinh_va_nghiem_thu.md#ap-dung-mau-ban-thao). Hồ sơ chỉ giữ tham chiếu/phiên bản và bằng chứng áp dụng, không sao ngân hàng nội dung hoặc quy tắc mẫu thành nguồn thứ hai.

| Thông tin | Giá trị của gói |
|---|---|
| Phiên bản/SHA-256 mẫu bản thảo và bảng kiểm | Chưa xác định |
| Bản G01/G02 thực sự đối chiếu, phiên bản/SHA-256 | Chưa xác định |
| Bảng đối chiếu trước viết (phần A), nơi lưu kết quả | Chưa lập |
| Kết quả kiểm trước trình (phần B), bản/hash được kiểm | Chưa kiểm |
| Khác mẫu, lí do và căn cứ chủ trì chốt | Chưa xác định |
| Phần chưa kiểm/được hoãn, giai đoạn và điều kiện phải khép | Chưa xác định |

Nếu tiếp quản bản thảo đã có, ghi rõ hồi cứu trước bước kế tiếp thay vì điền đã kiểm trước viết. Trạng thái công việc không thuộc mẫu này; dẫn về 03.

## 1. Nhận diện và phạm vi

- Mã và tên gói: chưa xác định.
- Mạch, vị trí trong Kế hoạch: chưa xác định.
- Người học và nhu cầu: chưa xác định.
- Tiên quyết: chưa xác định.
- Phạm vi bắt buộc, nhánh mở rộng và phần loại trừ: chưa xác định.
- Nguồn toán chính thống, vị trí đã đọc: chưa xác định.
- Nguồn QMD, thành phần chung, bản xuất và phiên bản kiểm: chưa xác định.
- Căn cứ người chủ trì chốt phạm vi: chưa có.

## 1.1. Bản điều hành và ca đường học cần khép

- Quy tắc hiện hành theo chủ đề; đầu vào/phép kiểm của phần bằng chứng được dùng lại: chưa kiểm.
- Phần quyết định cũ bị thay và ứng viên cần thu hồi trạng thái xin duyệt: chưa xác định.
- Đối chiếu DH01–DH14 trong 01/2.2.2: chưa kiểm; mỗi ca ghi vị trí nguồn, đích hỗ trợ, nơi quay về, bằng chứng/điều kiện và phần thiếu.
- Sơ đồ chỉ có bốn hoạt động mạch chính; ôn nguồn, đối chiếu–sửa lỗi, Nhật kí là hỗ trợ ngang. Tách Kiểm tra đang diễn ra khỏi Kiểm tra đã kết thúc.
- Không chép mô hình/ghi chú nội bộ thành câu chữ người học; không tự đổi menu Ôn nền/Nguồn.
- Kết quả tài liệu và kết quả sản phẩm ghi riêng; phần chưa sửa giữ lỗi mở.
- Với hoạt động Kiểm tra của mọi gói trong chương trình, áp dụng QD_024 tại 01/2.3.1; không giới hạn ở R1. Kiểm điểm vào và hướng dẫn một lượt không chia đợt ở Cách học/đầu Kiểm tra, tách quyền bắt đầu khỏi bằng chứng đạt mục tiêu. Nếu gói không có Kiểm tra, ghi không áp dụng cho hoạt động này, không tự thêm một bài kiểm tra hoặc đổi Khảo sát thành Kiểm tra.

## 2. Ma trận học tập

| Mục tiêu quan sát được | Phần học/ví dụ | Luyện và Điểm dừng | Kiểm tra độc lập | Ôn lại | Lỗi/tiên quyết cần hỗ trợ |
|---|---|---|---|---|---|
| Chưa điền | | | | | |

Mỗi mục tiêu thiết yếu có bằng chứng thực. Ghi nhánh chuyển giao riêng nếu có tiên quyết chưa thuộc lõi. Chặng thuộc Luyện tập; Bài học/Luyện tập không xen kẽ. Liên kết xem lại không là thứ tự luân phiên bắt buộc. Số chặng suy từ mục tiêu, không mặc định ba; lịch ôn và số bài là tham số gói.

## 3. Hành trình và tuyến hỗ trợ

| Chặng/điểm vào | Việc làm | Tiêu chí đạt | Nếu lỗi/thiếu nền | Câu xác nhận chưa lộ | Đích quay về/đi tiếp |
|---|---|---|---|---|---|
| Chưa điền | | | | | |

Tài nguyên Nền chỉ ghi “có” khi có nội dung, ví dụ, câu mới, đáp án/tiêu chí và đường quay về. Ghi cách xử lý khi câu đã lộ hoặc hết câu mới.

### Bản đồ vùng đọc và đối sánh vai trò

| Owner/ID nguồn | Vai trò/cấp nội dung | Kết quả đọc | Nội dung và action cùng vùng | Lí do ghép/ngắt | Cặp tương đương ở gói mẫu/khác biệt có căn cứ |
|---|---|---|---|---|---|
| Chưa điền | | | | | |

Không copy số vùng/view hoặc đề toán G01. Nhãn/heading/nội dung/chú thích/action trong vùng, một inset; cùng chức năng dùng cùng component. Nhật kí include một nguồn đủ 14 trường theo 01, không viết mẫu mới. Ngoại lệ về toán phải ghi lí do, không bỏ một mắt xích bắt buộc vì nguồn cũ chưa có.

## 4. Ma trận nhiệm vụ và nguồn bằng chứng

| Mã nhiệm vụ | Vai trò | Mục tiêu | Họ lỗi | Đề/lời giải ở đâu | Điều kiện coi là độc lập |
|---|---|---|---|---|---|
| Chưa điền | | | | | |

Chỉ liên kết tới nội dung nguồn chính; không chép cả ngân hàng bài vào hồ sơ. Nếu có nội dung dự thảo chờ tích hợp, ghi trạng thái và dừng sửa bản nháp song song khi đã nhập nguồn.

## 5. Phạm vi công việc được giao

### Ma trận đồng bộ điều hành trước sản xuất

| Quyết định/nguồn có thẩm quyền | Tài liệu/hồ sơ/template bị ảnh hưởng | Hiện thực nguồn có khớp không | Phần lịch sử bị thay | Phép kiểm và khoảng cách còn mở |
|---|---|---|---|---|
| Chưa điền | | | | |

Đọc danh mục 08 và cổng 02; không tự đặt chuẩn chung từ gói mẫu. Bảng này ghi tác động của quyết định, không chép lại nội dung 01/07/kit. Thiếu nội dung hoặc tuyến sai phải ghi backlog, không đổi trạng thái để readiness đạt. D0/HTML-only có hợp đồng riêng, không bắt dùng mọi mắt xích R1.

| ID | Vấn đề/yêu cầu | Bằng chứng | Thay đổi cụ thể | Phép kiểm | Trạng thái và căn cứ chốt |
|---|---|---|---|---|---|
| Chưa điền | | | | | |

## 6. Nghiệm thu

| Tình huống đặc trưng của gói | Kết quả mong đợi | Kết quả thực và vị trí bằng chứng |
|---|---|---|
| Đường học mặc định | | |
| Kiểm tra: đủ tự tin được bắt đầu dù chưa có bài làm trước; một lượt không chia đợt; chưa tự coi là đạt | | |
| Thiếu tiên quyết quan trọng | | |
| Lỗi tái diễn sau K/O | | |
| Câu đã lộ hoặc hết câu mới | | |
| Nhánh chuyển giao nếu có | | |
| Điện thoại/bàn phím/đích quay về | | |

## 7. Trạng thái sản phẩm

| Mặt kiểm | Trạng thái | Bản/commit, ngày, căn cứ |
|---|---|---|
| Nội dung | Chưa kiểm | |
| Đường học | Chưa kiểm | |
| HTML/PDF | Chưa kiểm | |
| Phát hành | Chưa phát hành | |

Ghi rõ người chủ trì chấp nhận bản nào/hash/phạm vi, khác bản đang sửa; receipt lịch sử không tự chứng nhận ứng viên mới. Metadata máy đọc phải phân lớp `acceptance` hiện hành và `historical_acceptance`; không để cờ accepted cũ cạnh ứng viên pending mà không xác định phạm vi. Góp ý chưa có phương án chốt ghi riêng, không giả nghiệm thu. Công việc tiếp theo thuộc bảng điều hành, không tạo roadmap cạnh tranh.

## 8. Công sức và phản hồi

Ghi giờ người làm thực tế, giờ chờ máy riêng, chi phí xây chung và chi phí riêng của gói, phần làm lại do lỗi. Ghi phản hồi người học và giới hạn quan sát; không suy hiệu quả học từ việc đã xuất đủ tệp.

## ?nh ??i di?n tr??c khi d?ng ngu?n

- N?i dung ch?nh c?n ???c ?nh ??i di?n th? hi?n:
- H?nh ???c ?? xu?t v? l? do ch?n; ngu?n/c?ng c? t?o:
- B?ng ch?ng ch? tr? duy?t ph??ng ?n:
- Khai b?o `giao_dien/anh_bia.json` sau duy?t; kh?ng d?ng ?nh m?c ??nh.
- Ki?m ngu?n/hash/?nh HTML v? ki?m tr?c quan theo m?c ?Ch?n ?nh ??i di?n
  khi d?ng g?i m?i? c?a quy tr?nh 02.
