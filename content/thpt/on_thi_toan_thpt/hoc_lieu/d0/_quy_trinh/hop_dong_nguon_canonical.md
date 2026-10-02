# D0 — hợp đồng nguồn canonical cho chuyển đổi

## Hợp đồng hiện hành sau duyệt nội dung 2026-10-02

Yêu cầu mới nhất của người dùng thay thế các ranh giới công khai và luồng sử
dụng cũ bên dưới: `index.qmd` là nguồn canonical sau tích hợp bản HTML được
duyệt; `noi_dung_da_duyet.json` khóa toàn chuỗi văn bản và TeX theo năm phần.
Phải giữ nguyên 24 câu, Bài 00 giả lập và 25 phần đối chiếu công khai thu gọn.
D0 tự nguyện, không là điều kiện vào học, không phải một bài học bắt buộc.
Không sửa câu chữ/toán; chỉ đổi cấu trúc kỹ thuật, đích liên kết có thật và
tài sản tương đương đã duyệt. Không chạy script của tài liệu nhập.
Ngân hàng v1.0, 24 câu thử lại và hồ sơ người hướng dẫn vẫn được bảo toàn riêng,
không chiếu vào HTML hiện hành. Kiểm định toàn chuỗi dùng bản nội dung mới được
duyệt, không dùng hướng dẫn 6B cũ; baseline lịch sử vẫn kiểm hash và toán 48/48.
PDF, nghiệm thu HTML và xuất bản là các cổng riêng còn chờ. Phần dưới chỉ ghi
hợp đồng lịch sử và provenance; mọi điểm xung đột nhường quyền cho quyết định này.

## 1. Mục đích

Hợp đồng này xác định cách chuyển D0 v1.0 đã khóa sang hệ sản xuất QMD canonical mà không tự ý biên soạn lại nội dung. Nó điều hành giai đoạn chuyển đổi kỹ thuật; không thay Kế hoạch 0.6, không thay quyết định sư phạm và không tự tạo trạng thái nghiệm thu hoặc xuất bản.

Manifest máy đọc đi kèm là [`manifest_chuyen_doi.yml`](manifest_chuyen_doi.yml).

## 2. Ranh giới thẩm quyền

Trong thời gian chưa có `index.qmd` được đối chiếu và nghiệm thu, toàn bộ cây [`lich_su/v1_0/`](lich_su/v1_0/README.md) là baseline nội dung bất biến.

Thẩm quyền trong baseline được phân lớp như sau:

| Lớp | Nguồn | Cách dùng |
|---|---|---|
| Nội dung 24 nhiệm vụ, lời giải và câu thử lại | `lich_su/v1_0/src/bien_soan.py` | Nguồn biên soạn lịch sử cao nhất cho ngân hàng; không sửa tại chỗ trong lượt chuyển đổi. |
| Dữ liệu có cấu trúc | `lich_su/v1_0/D0_ngan_hang_v1.0.json` | Dữ liệu sinh dùng để trích xuất và kiểm kê; phải đối chiếu với nguồn biên soạn lịch sử. |
| Hướng dẫn phân tích | `lich_su/v1_0/2027_D0_huong_dan_phan_tich_v1.0.md` | Nguồn độc lập cho quy trình chọn câu, phân tích, phản hồi và ghi hồ sơ. |
| Hướng dẫn trải nghiệm | `lich_su/v1_0/HUONG_DAN_SU_DUNG.md` | Nguồn bổ sung đã được xác nhận, dùng để thiết kế điểm vào và luồng sử dụng. |
| Markdown còn lại | Các bản học sinh, thử lại, lời giải và ma trận | Đầu ra sinh để đối chiếu toàn chuỗi; không sửa như nguồn độc lập. |
| PDF v1.0 | Bốn PDF trong baseline | Thành phẩm lịch sử để đối chiếu nội dung và thị giác; không phải nguồn biên soạn. |
| Hồ sơ và kiểm chứng | Hồ sơ, manifest, checker và kết quả trong baseline | Bằng chứng provenance và lớp hồi quy; không phải nội dung công khai. |

Khi `index.qmd` mới đạt đủ cổng đối chiếu và được người chủ trì nghiệm thu, nó mới trở thành nguồn biên soạn canonical cho các đầu ra HTML/PDF tiếp theo. Baseline v1.0 vẫn được giữ làm provenance, không duy trì như nguồn biên tập song song.

## 3. Inventory nội dung bị khóa

### Phạm vi bảo trì đã được giao ở Bước 6B

Người dùng đã yêu cầu thực hiện Bước 6B sau kiểm toán Bước 6A. Phạm vi này cho
phép biên tập hướng dẫn công khai, tên hiển thị và hướng dẫn người tổ chức theo
Kế hoạch 0.6. Nó không cho phép thay ngân hàng toán, ID hay quan hệ họ câu.
`du_lieu/huong_dan_cong_khai.md` và `du_lieu/huong_dan_phan_tich.md` là nguồn
hướng dẫn của phép chiếu hiện hành; hai bản hướng dẫn lịch sử chỉ còn dùng để
truy nguyên. `bien_tap_6b.json` khóa từng sai biệt của hướng dẫn phân tích.
Checker tiếp tục so toàn chuỗi QMD, toàn bộ bản hướng dẫn phân tích và toàn bộ
ngân hàng. Hash biên tập khóa bản để duyệt, không tự xác nhận nghiệm thu.

Tên công khai là “Khảo sát và định vị đầu vào”; nhãn nhiệm vụ hiển thị mạch và
số bài. `D0` được giữ trong ID, metadata và hồ sơ quản trị. Hướng dẫn công khai
không chứa câu thử lại hoặc lời giải. HTML đã dựng trước Bước 6B bị đánh dấu
stale, với kết luận thị giác chưa đạt; phải sửa và dựng lại trước nghiệm thu.

### Inventory ngân hàng

- Tám mạch: R1–R8.
- Mỗi mạch có đúng ba nhiệm vụ chính.
- Tổng cộng 24 nhiệm vụ chính, 24 câu thử lại và 24 họ câu.
- Mỗi nhiệm vụ chính có đúng một `retest_id` và một `family`.
- ID phải giữ nguyên; không đánh lại số theo vị trí trên trang hoặc theo giao diện mới.
- Mọi trường dữ liệu bắt buộc được liệt kê trong manifest phải còn khả năng truy nguyên sang `index.qmd`, dữ liệu canonical hoặc hồ sơ nội bộ thích hợp.

Checker chuyển đổi phải so sánh toàn bộ tập ID và quan hệ, không chỉ kiểm số lượng.

## 4. Phân chia nội dung công khai và nội bộ

D0 là công cụ khảo sát có điều phối, không phải một đề thi công khai kèm đáp án ngay bên dưới. Kiến trúc mới phải giữ các ranh giới sau:

- Bản học sinh không chứa đáp án, lời giải, tiêu chí chấm hoặc câu trả lời thử lại.
- Bản thử lại không chứa đáp án và không được mặc định giao toàn bộ.
- Bản lời giải dành cho người hướng dẫn chứa lời giải, tiêu chí, lỗi, nơi ôn và đáp án thử lại.
- Hướng dẫn phân tích dành cho người tổ chức việc chọn câu, đọc bằng chứng và phản hồi.
- HTML công khai không được làm lộ lời giải chỉ bằng việc tắt JavaScript, đổi hash, đọc source HTML hoặc dùng tìm kiếm website.
- Hồ sơ nội bộ, manifest và checker luôn nằm dưới `_quy_trinh` và không được đưa vào allowlist public.

Ranh giới này là yêu cầu chức năng. Không dùng trạng thái thu gọn, tab ẩn hoặc CSS/JavaScript như một cơ chế bảo mật lời giải.

## 5. Kiến trúc HTML dự kiến

Trang D0 dùng phong cách và hệ thành phần chung của Ôn thi Toán THPT nhưng có luồng riêng:

1. `Bắt đầu`: vai trò tự nguyện của D0 và cách dùng.
2. `Chuẩn bị`: phần khai báo phạm vi và Bài 00 giả lập.
3. `Làm khảo sát`: tám mạch và 24 nhiệm vụ chính.
4. `Đối chiếu bài làm`: 25 phần đối chiếu đóng/mở đã được duyệt.
5. `Chọn mạch ôn`: cách đọc kết quả và đường dẫn tới học liệu thực sự có.

Các tên trên là vai trò điều hướng, chưa khóa câu chữ giao diện cuối cùng. D0 tái sử dụng typography, màu, khung trang, component, hành vi mobile và quy tắc trợ năng canonical; CSS riêng chỉ chứa ngoại lệ chức năng thực sự.

## 6. Phạm vi đầu ra HTML-only

Theo quyết định của chủ dự án ngày 2026-10-03, D0 chỉ phát hành trang HTML; không
tạo các PDF nội dung kiểu bản học sinh, thử lại, lời giải hoặc hướng dẫn. Quyết
định cục bộ này không thay đổi hợp đồng PDF của R1-G01/R1-G02.

Các PDF dùng làm tài sản kỹ thuật cho hình học và các PDF nằm trong baseline lịch
sử vẫn được bảo toàn. Chúng không phải biến thể PDF của trang D0 và không tạo thẻ
`Tải PDF` trong giao diện.

## 7. Hàng rào đối chiếu khi tạo QMD

Trước khi `index.qmd` được coi là ứng viên hợp lệ, phải chứng minh:

- đủ và đúng thứ tự logic của 24 nhiệm vụ chính;
- đủ 24 câu thử lại và quan hệ đúng với câu chính;
- toàn bộ đề, dữ kiện, công thức, đáp án, lời giải, tiêu chí và mã lỗi giữ nguyên ý nghĩa;
- các trạng thái CH/KCG/Đ/M/S/B, cờ đoán, trợ giúp, đã gặp và thời gian không bị đổi nghĩa;
- giữ nguyên nguyên tắc chỉ giao phần đã học, không bắt làm toàn bộ và không dự báo điểm thi;
- đính chính B.8 của Kế hoạch 0.6 được xử lý như chú thích tương thích, không âm thầm sửa baseline v1.0;
- checker toán lịch sử tiếp tục chạy như một lớp hồi quy, bên cạnh checker QMD/HTML/PDF mới;
- không có lời giải trong đầu ra học sinh hoặc HTML public ngoài phạm vi được duyệt.

Không nới phép so sánh hoặc giảm inventory để làm cho bản chuyển đổi đạt kiểm tra.

### Tài sản hình học pilot D0-R3-03

Từ Đợt 5, `hinh/hinh_hop.pdf` và `hinh/hinh_hop.png` là đầu ra pilot có chủ ý,
không còn phải trùng byte với tài sản lịch sử. Bản lịch sử tiếp tục bất biến trong
`lich_su/v1_0/src/`; manifest khóa checksum của tài sản pilot và nguồn YAML tương
ứng. Thay đổi này chỉ thay backend và ngôn ngữ thị giác của hình, không thay câu
hỏi, dữ kiện, ID, caption hoặc lời giải của `D0-R3-03`.

## 8. Kết quả của Bước 2 và việc tiếp theo

Bước 2 chỉ hoàn tất khi manifest máy đọc khớp baseline và tất cả đường dẫn phân loại tồn tại. Bước này không tạo QMD, HTML hoặc PDF.

Việc tiếp theo là Bước 3: tạo cấu hình dự án QMD và checker chuyển đổi tối thiểu trước, sau đó mới dựng khung `index.qmd`. Checker đầu tiên phải đọc manifest này, kiểm baseline và khóa inventory; chưa kiểm giao diện hoặc số trang khi các đầu ra canonical chưa tồn tại.
