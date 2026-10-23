# Bảng kiểm áp dụng mẫu bản thảo gói

Phiên bản mẫu: **1.8** · Ngày: 23/10/2026 · Phạm vi: bản thảo gói R1 của khóa 2027. Đây là công cụ áp dụng, không tạo kiến trúc hoặc chuẩn hiển thị mới.

Nguồn: [01 — chức năng học tập](../01_kien_truc_hoc_tap.md), [07 — trình bày](../07_quy_chuan_cau_truc_trang_nguoi_hoc.md), [02/1.4 — cách dùng](../02_quy_trinh_va_nghiem_thu.md#ap-dung-mau-ban-thao), [khung bản thảo](ban_thao_goi.md), [tổ chức nguồn](../quy_chuan_goi_qmd.md). G01/G02 là học liệu đối chiếu theo chức năng; nội dung toán và số lượng nhiệm vụ thuộc gói đang viết.

## Cách lập kết quả

Lập kết quả trong `hoc_lieu/<ma_goi>/_quy_trinh/ho_so/` hiện có, không sửa bảng mẫu thành trạng thái một gói. Có thể dùng một tệp cho hai thời điểm, phân rõ kết quả trước viết và trước trình. Đối với gói đã có bản thảo, ghi áp dụng hồi cứu trước bước kế tiếp; không tuyên bố đã dùng mẫu trước khi viết.

Ghi mã/tên gói, phiên bản và SHA-256 bản thảo; phiên bản/hash hai mẫu; phiên bản/hash nguồn G01/G02 thực sự đối chiếu; tài liệu kiểm, ngày, người thực hiện và phạm vi. Mỗi dòng phải có đích cụ thể (tệp + mục/anchor, hình + trang nếu có), không điền “đã có” hoặc PASS chỉ vì đếm đủ.

Trạng thái: **Đạt / Cần sửa / Chưa kiểm / Không áp dụng có lí do / Hoãn theo chốt của chủ trì**. Khi hoãn, ghi đúng chỉ thị, việc và giai đoạn phải xử lí, phép kiểm và giới hạn công nhận; không đổi thành Đạt. Kết luận tách nội dung, đường học, hình, bản xuất, chủ trì duyệt và phát hành. Chỉ 03 sở hữu việc hiện hành và bước tiếp theo.

## A. Trước viết nội dung

| ID | Điều cần xác định | Nguồn sở hữu | Kết quả/vị trí bằng chứng | Trạng thái |
|---|---|---|---|---|
| A01 | Nhiệm vụ được giao, người học, mục tiêu, phạm vi lõi/loại trừ và nguồn chính thức cần đọc | Hồ sơ gói; Kế hoạch trong phần còn hiệu lực | Chưa điền | Chưa kiểm |
| A02 | Phiên bản mẫu, quy tắc trình bày/chú thích nguồn/ngoặc/khối/hình hiện hành và nguồn G01/G02 thực sự dùng làm đối chiếu | 02/1.4; 08 | Chưa điền | Chưa kiểm |
| A03 | Bản đồ từng thành phần: tương ứng ở gói mẫu, vị trí dự kiến, phần không áp dụng và khác biệt có lí do | 01; 07 | Chưa điền | Chưa kiểm |
| A04 | Mục tiêu ↔ phần học/ví dụ ↔ luyện/Điểm dừng ↔ kiểm tra ↔ ôn ↔ lỗi/nền | Hồ sơ gói; 01/2.1–2.8 | Chưa điền | Chưa kiểm |
| A05 | Nhóm nhiệm vụ, chức năng, cách đánh số, cặp đề–đáp án và lịch sử lộ; không sao số bài G01/G02 | 01/QD_025; 07/6.2 | Chưa điền | Chưa kiểm |
| A06 | Vị trí nguồn đang sửa, tài nguyên nháp và kết quả kiểm; không phát sinh kho mới | Quy chuẩn gói, mục Khởi tạo | Chưa điền | Chưa kiểm |
| A07 | Khác biệt cần chốt được báo trước, ghi lí do và phạm vi đã được chấp thuận | 02/1.4; chỉ thị chủ trì | Chưa điền | Chưa kiểm |

Bảng đối chiếu cấu trúc dùng trước viết: mỗi dòng phải ghi đủ đường dẫn cha–con, không suy cấp mục từ việc các dòng nằm ngang hàng trong bảng. Tách các dòng “từng mục kiến thức” theo từng mục thực tế của gói; kiểm cả nhãn/số, câu hỏi và phản hồi tại chỗ. Đối chiếu G03 hiện hành khi dùng cách phân bổ Gợi mở đã chốt ở gói này; không dùng bản thảo cũ đã bị thay. Không sao số lượng hoặc tạo nhiệm vụ rỗng cho gói đối chứng không có Gợi mở.

| Thành phần/chức năng và nơi sở hữu | Vị trí trong gói đối chứng đã đọc (ghi rõ G01/G02/G03) | Vị trí dự kiến ở gói mới | Giữ/đổi/không áp dụng | Lí do và căn cứ chốt nếu đổi |
|---|---|---|---|---|
| Bắt đầu | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Bài học → Định hướng | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Bài học → Khởi động → nhiệm vụ và phản hồi/đường chọn nền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Chỉ dẫn thao tác nếu cần → bỏ lặp, điều kiện nhìn thấy, đầu câu viết hoa | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Bài học → từng mục kiến thức → Gợi mở và phản hồi/cầu nối tại chỗ | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Bài học → từng mục kiến thức → lời giảng, định nghĩa/định lí và ví dụ | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Bài học → từng mục kiến thức → Tự kiểm tra và hỗ trợ | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Bài học → Khép lại | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Luyện tập → từng chặng → nhiệm vụ và Điểm dừng | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Kiểm tra → nhiệm vụ, kết thúc lượt và xử lí kết quả | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Ôn lại → từng lượt và Điểm dừng | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Ôn nền → tài nguyên được gọi theo nhu cầu | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Sửa lỗi → nhóm theo nơi phát hiện và đường quay về | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Nhật kí | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Lời giải → nhóm phản chiếu nơi chứa đề | Chưa điền | Chưa điền | Chưa điền | Chưa điền |
| Nguồn | Chưa điền | Chưa điền | Chưa điền | Chưa điền |

## B. Trước trình duyệt bản thảo

| ID | Điều phải đọc/kiểm thực chất | Nguồn sở hữu | Kết quả/vị trí bằng chứng | Trạng thái |
|---|---|---|---|---|
| B01 | Bắt đầu có một bảng Học xong, em cần làm được gì? nhìn thấy, đối chiếu không mất mục tiêu từ bảng cũ/bằng chứng; đủ tiên quyết, điểm vào và điều kiện hoàn tất | 01/2.2–2.3,2.7; 07/4 | Chưa điền | Chưa kiểm |
| B02 | Bài học và Luyện tập riêng; Câu hỏi dẫn đường mặc định đóng, không lặp bảng mục tiêu/Mục lục; giữ bốn khu vực và hỗ trợ ngang, không tạo chuỗi bắt buộc | 01/2.2.1; 07/3–4 | Chưa điền | Chưa kiểm |
| B03 | Khởi động thuộc Bài học, là nhiệm vụ kiểm nền thật, có phản hồi và đường chọn nền; không thay Gợi mở | 01/2.3; G01/G02 | Chưa điền | Chưa kiểm |
| B04 | Từng Gợi mở thuộc đúng mục kiến thức trong Bài học, sau chỉ dẫn thao tác nếu thật sự cần, trước lời giải thích, có phản hồi/cầu nối tại chỗ; giữ nhãn và số liên tục toàn nhóm, không reset theo mục; không có mục Gợi mở chung ngang cấp Khởi động/Bài học | 01/QD_025; 07 bổ sung QD_025 | Chưa điền | Chưa kiểm |
| B05 | Chính văn phát biểu trực tiếp; lời giảng/định nghĩa/định lí đủ điều kiện và có căn cứ đã đọc; chú thích .zo-source-note đúng vị trí/câu/tên/trang, không dẫn “theo SGK…” hoặc kể quá trình biên soạn trong lời giảng | Nguồn toán gói; 07/4.2,6.3; quy chuẩn gói/Công thức và nguồn đối chiếu | Chưa điền | Chưa kiểm |
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
| B18 | Gọi guard kí pháp hiện có, ghi rõ phạm vi hỗ trợ; toán đúng tập xác định/tập đang xét, dấu, hướng, đơn vị, mức đạt/chưa đạt và giới hạn suy luận; LaTeX cho số/biểu thức, phân số và ngoặc đúng quy chuẩn | Nguồn toán; quy chuẩn kí hiệu/dấu ngoặc | Chưa điền | Chưa kiểm |
| B19 | Lập ma trận tài nguyên theo vai trò trước viết/chuyển QMD; dùng công cụ ZO Math/component hiện hành, tách hình trong bài và bìa. BBT từ một JSON/native MathML, giữ mốc/dấu/giới hạn hai phía/điểm loại/số hàng. Kiểm khung và cỡ hiển thị đồ thị theo GRAPH-G03-01/G03, scope CSS thật sự hoạt động, phông/nét/vạch/nhãn/điểm/trục; đối chứng đồ thị với G03 và BBT với gói có bảng trên desktop/mobile và thử âm. Không lấy profile 0.4, hash, kind=variation hoặc ảnh montage làm đủ bằng chứng | 07/6.1.2,6.3; 02/2.5; công cụ ZO Math và binding kit | Chưa điền | Chưa kiểm |
| B20 | Chính văn và nhãn liên kết dùng tên có nghĩa, không dùng mã quản lí; liên kết tồn tại và thực sự dẫn đúng nội dung | 07/6.2; đối chiếu ngữ nghĩa thủ công | Chưa điền | Chưa kiểm |
| B21 | Bản trình duyệt đúng phiên bản, hết chỗ trống/ghi chú nội bộ; phân biệt nội dung và HTML/PDF; ghi rõ những phần được hoãn | 02/4; quy chuẩn gói | Chưa điền | Chưa kiểm |
| B22 | Trạng thái đã sửa/đã kiểm/chủ trì duyệt/phát hành tách biệt; không sửa receipt cũ và không kế thừa PASS sai phạm vi | 02/4; 03 | Chưa điền | Chưa kiểm |
| B23 | Rà từng Cách thực hiện trong ngữ cảnh: bỏ đoạn chỉ lặp thứ tự đọc/phương pháp; giữ yêu cầu cần thiết nhìn thấy; trợ giúp tùy chọn mới dùng hộp xám đóng; câu đầu viết hoa; có kiểm kê giữ/sửa/bỏ và không mất điều kiện | 07/6.1.5; INSTRUCTIONS-20261018 | Chưa điền | Chưa kiểm |
| B24 | Rà thuật ngữ theo nghĩa: tập xác định/tập đang xét/điều kiện biến; câu đủ đối tượng và quan hệ toán, không có lời điều hành hoặc viết tắt tối nghĩa. Đối chiếu nguyên văn/câu mới/lí do bỏ, đích hỗ trợ đúng lỗi; đọc lại tiêu đề, đề–lời giải, bảng, alt, include và dữ liệu sinh. Giữ điều kiện, ID và điều hướng; hồ sơ rà nguồn khớp bản hiện tại; cổng máy không thay đọc ngữ nghĩa | 07/6.1.6; EDITORIAL-20261018 | Chưa điền | Chưa kiểm |

## Bảng ngoại lệ và việc hoãn

| ID kiểm | Khác mẫu hoặc lỗi quan sát | Lí do/phạm vi | Chỉ thị chốt của chủ trì | Giai đoạn phải khép | Phép kiểm và giới hạn công nhận |
|---|---|---|---|---|---|
| Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền | Chưa điền |

## Kết luận trước trình

Nêu phần đã đạt, phần cần sửa/chưa kiểm và ngoại lệ có căn cứ. Lỗi toán/đường học thiết yếu chưa khép không được trình như đã đạt; việc hoãn chỉ có hiệu lực đúng phạm vi chủ trì chốt. Mẫu và kiểm kỹ thuật không thay đọc toàn nội dung, xem hình hoặc chủ trì duyệt. Chuyển QMD sau duyệt bản thảo theo quy chuẩn gói; tài nguyên chính thức phải dựng lại bằng công cụ ZO Math. Mẫu bản thảo không chứa CSS/JS, thiết kế lại trang hoặc chỉ tiêu số bài.


Nhãn khi chuyển QMD/HTML: áp 07/6.2, quy tắc Nhãn ngữ cảnh theo cấp chứa ngày 17/10/2026. Bài học → MẠCH HỌC CHÍNH; Khởi động → MẠCH HỌC CHÍNH · BÀI HỌC; nhiệm vụ Khởi động thêm KHỞI ĐỘNG ở cuối. Không dùng bảng nhãn mỹ thuật cũ làm mẫu. Kiểm kê owner/tiêu đề/nhãn trước–sau, dấu chấm nhỏ, cùng kiểu .role và quan hệ đề–lời giải; giữ loại/chức năng/số trong metadata.

Bổ sung B19 theo 07/6.1.2, 02/2.5: phải có ma trận tài nguyên theo vai trò; hình trong bài/bìa đối chiếu riêng, cấu hình surface/cỡ tường minh; BBT đi qua JSON/bộ dựng native, có đối sánh mốc/dấu/giới hạn/điểm loại/hàng thật; bằng chứng thử âm và xem desktop/mobile: đồ thị theo G03, BBT theo gói có bảng cùng vai trò. Không đánh Đạt chỉ vì cùng profile 0.4, cùng CSS, đủ hash hoặc kind=variation. Áp dụng cả bản thảo, không đẩy thiếu sót này tới bước QMD.


### B25 — Bảng nút thắt nhận thức (bổ sung 19/10/2026)

- Đối chiếu toàn bộ mục tiêu/kiến thức/Gợi mở/ví dụ/nhiệm vụ/lời giải với từng dòng hoặc lí do không có dòng riêng.
- Đủ bốn cột theo 07/6.1.7; mỗi dòng có biểu hiện cụ thể, câu hỏi, cách tháo gỡ, đích học lại và nhiệm vụ/ý đúng phạm vi hoặc ghi thiếu.
- Đọc thực tế đề và tiêu chí, giữ nhóm theo ngữ cảnh, lịch sử đã gặp và đường về; không gán một bài cho tất cả biểu hiện cùng họ lỗi.
- Cổng nguồn và bảng rộng/hẹp được kiểm ở đúng giai đoạn; không dùng PASS cấu trúc thay kết luận sư phạm hoặc nghiệm thu.
- Khi dùng danh mục làm trục bài giảng, giữ tiên quyết, Gợi mở trong Bài học và hỗ trợ tùy nhu cầu; ghi nhận bài đã dùng trước lớp.


### B26 — Tiêu chí, so sánh và quy trình theo chức năng (19/10/2026)

- Đối chiếu ngang theo 07/6.1.8; giữ hoặc không có bảng theo nhu cầu thật, không theo quota.
- Tiêu đề cột đúng nội dung; mục tiêu có bài/ý và tiêu chí tương ứng, giới hạn chưa đo được ghi rõ. Không dùng nơi hỗ trợ thay tiêu chí.
- Số điểm chỉ ở nơi có thang điểm; điều kiện toán, tên nhiệm vụ và đích tới/lui còn nguyên. Nhật kí đủ 14 trường; không giữ danh mục lỗi trùng làm nguồn cạnh tranh.
- Chọn profile chức năng dùng chung, không tự chia đều cột hoặc thu nhỏ chữ. Phân biệt bảng cần so ngang với bảng tra từng tình huống; kiểm nguồn trước dựng và quan sát rộng/hẹp sau khi được phép dựng.

### B27 — Giọng văn rõ nghĩa, có ngữ cảnh (23/10/2026)

Áp dụng tiêu chí biên tập này cho toàn khóa theo 07/6.1.6; không ép cấu trúc mẫu R1 lên trang/gói có chức năng khác.

- Người học hiểu đối tượng, đại lượng, đơn vị, thời gian/địa điểm cần thiết; không còn thuật ngữ hoặc mã chưa giải thích cản trở việc hiểu đề.
- Mỗi nhiệm vụ có mục đích; câu hỏi dùng ngữ cảnh và yêu cầu giải thích cụ thể; lời giải trả lời đủ, giữ giới hạn kết luận.
- Câu văn đủ đối tượng, hành động và điều kiện; không rút gọn gây hiểu sai, không diễn giải dài ngoài nhu cầu.
- Ôn lại không nhắc trước kiến thức/công thức/cách giải hoặc mục “Nhớ lại trước khi làm”; quy ước dữ liệu vẫn đủ tại đề.
- Ghi phạm vi/đoạn đối chiếu và kết luận bằng đọc thực tế. Chưa rà thì ghi Chưa kiểm; không suy đạt từ PASS công cụ hoặc từ việc quy chuẩn đã được duyệt.
