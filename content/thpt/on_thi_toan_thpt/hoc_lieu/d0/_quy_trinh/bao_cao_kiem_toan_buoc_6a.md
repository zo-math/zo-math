# Báo cáo kiểm toán Bước 6A — nội dung và kiến trúc thông tin D0

## 1. Phạm vi và trạng thái

Báo cáo này kiểm toán ứng viên D0 sau vòng nghiệm thu HTML chưa đạt. Phạm vi gồm
nguồn dữ liệu, công cụ sinh QMD, QMD hiện tại, giao diện HTML, checker, tài sản hình
học và các tài liệu điều hành của gói.

Đây là kết quả khảo sát. Chưa biên tập nội dung, chưa sửa QMD, chưa render lại,
chưa tạo PDF canonical và chưa thực hiện xuất bản.

## 2. Kết luận chính

Ngân hàng toán học không phải phần đang bị thiếu. Hiện có đủ 24 nhiệm vụ chính,
24 câu thử lại và 24 hồ sơ nội dung; mỗi mạch R1–R8 có ba nhiệm vụ. Tên và phạm vi
tám mạch đã khớp mục 4.5 của Kế hoạch 0.6. Phép chiếu toàn chuỗi từ baseline và
kiểm tra toán lịch sử đều đạt.

Ứng viên HTML chưa thể nghiệm thu vì lớp biên tập và kiến trúc trình bày chưa trở
thành một sản phẩm công khai hoàn chỉnh. Công cụ sinh hiện ghép nguyên văn tài liệu
hướng dẫn lịch sử vào `Bắt đầu`, đặt R1–R8 ngang cấp với `Khảo sát`, tạo nội dung
tối thiểu cho `Đọc kết quả` và `Thử lại`, đồng thời để `Tải PDF` ở trạng thái thông
báo chưa có tệp. JavaScript chỉ di chuyển các section được liệt kê, nên tám section
R1–R8 vẫn nằm ngoài panel khảo sát. Đây là nguyên nhân cấu trúc khiến `Bắt đầu` và
`Toàn văn` gần như trùng nhau khi quan sát trang.

## 3. Kiểm kê nội dung theo vai trò

| Thành phần | Hiện có | Sai biệt hoặc phần còn thiếu | Mức xử lý |
|---|---|---|---|
| Tiêu đề công khai | `Khảo sát và định vị đầu vào` | Phụ đề, lời dẫn và mã hiển thị vẫn dùng `D0` như tên dành cho người đọc | Bước 6B |
| `Bắt đầu` | Toàn văn hướng dẫn sử dụng lịch sử, ví dụ và quy trình năm bước | Dài, thiên về người tổ chức, còn giọng văn bàn giao/bản nháp; thiếu điểm vào ngắn gọn cho người học | Bước 6B–6C |
| Khai báo phạm vi | Một đoạn chỉ dẫn | Chưa giúp người học/người hướng dẫn thực sự chọn phần đã học và hiểu cách dùng kết quả | Bước 6B–6C |
| `Khảo sát` | Đủ 8 mạch, 24 nhiệm vụ; nội dung toán và ánh xạ mạch đạt kiểm tra | R1–R8 không nằm trong section khảo sát về mặt cấu trúc; cách trình bày đề chưa tạo đủ thứ bậc thị giác | Bước 6C–6D |
| `Đọc kết quả` | Một đoạn cảnh báo không suy điểm thi | Thiếu quy trình đọc bằng chứng, trạng thái kết quả và hành động tiếp theo; chưa đủ để thành một thẻ độc lập | Bước 6B–6C |
| `Thử lại` | Một đoạn nói thời điểm giao câu | Thiếu mục đích, điều kiện, quy trình và cách hiểu kết quả; 24 câu thử lại có trong nguồn riêng nhưng không nên công khai sẵn | Bước 6B–6C |
| `Tải PDF` | Thông báo chưa có PDF | Chưa có tài sản để tải; không nên hiện như một chức năng hoạt động | Bước 6C, mở lại ở Bước 7 |
| `Toàn văn` | Cơ chế JavaScript để hiện các section đã ánh xạ | Chưa đại diện đúng toàn bộ cây nội dung công khai do lỗi quan hệ section | Bước 6C |
| Nội dung người hướng dẫn | Hướng dẫn phân tích, hồ sơ, lời giải và câu thử lại đầy đủ; được Lua loại khỏi HTML | Còn câu chữ theo Kế hoạch 0.5 và trạng thái lịch sử; cần biên tập có kiểm soát theo Kế hoạch 0.6 | Bước 6B |
| PDF canonical | Đã định nghĩa bốn vai trò: học sinh, thử lại, lời giải, hướng dẫn | Chưa tạo | Bước 7, sau nghiệm thu HTML |

## 4. Ma trận sai biệt với baseline canonical hiện hành

| Hạng mục | Baseline tham chiếu | D0 hiện tại | Kết luận |
|---|---|---|---|
| Tên công khai và mã quản lý | Tên đọc tự nhiên; mã gói nằm ở metadata/quản trị | `D0` xuất hiện trong phụ đề, lời dẫn và 24 mã câu nhìn thấy | Không đạt |
| Cây nội dung | Quan hệ section có nghĩa ngay trong QMD; JavaScript chỉ tăng cường giao diện | `Khảo sát` và R1–R8 là chín section đồng cấp; JS vá theo danh sách ID | Không đạt |
| Bảng thường | Bọc bằng thành phần bảng responsive dùng chung | Có năm bảng thường chưa dùng wrapper canonical | Không đạt |
| Bảng dấu/biến thiên | Dữ liệu có cấu trúc, một nguồn cho HTML/PDF và bản ngữ nghĩa truy cập được | R1-03 là bảng Markdown thuần | Không đạt |
| Trình bày nhiệm vụ | Mã, metadata, lệnh hỏi và dữ liệu có thứ bậc rõ, hỗ trợ quét mắt | Đề bài chủ yếu là một khối văn bản liên tục | Chưa đạt |
| Hình học | Nguồn ZO Geometry; SVG cho HTML, PDF vector cho bản in | Đã có nguồn và đủ SVG/PDF/receipt, nhưng QMD và checker bắt HTML nhúng PDF | Tài sản đạt, tích hợp không đạt |
| Nội dung sáu thẻ | Mỗi thẻ có chức năng thật và không giả chức năng chưa sẵn sàng | Hai thẻ ở mức placeholder; thẻ tải chưa có tệp | Không đạt |
| Riêng tư | Lời giải/câu thử lại không rò sang HTML công khai | Lua loại khối riêng; checker xác nhận không rò | Đạt |
| Ánh xạ R1–R8 | Theo mục 4.5 Kế hoạch 0.6 | Đủ tám tên đúng; fixture âm từ chối `R5 — Số phức` | Đạt |
| Toàn vẹn ngân hàng | 24 chính + 24 thử lại + hồ sơ, giữ quan hệ family | Đủ và phép chiếu toàn chuỗi đạt | Đạt |
| Tình trạng điều hành | Kế hoạch 0.6 thay thế 0.5 | Hướng dẫn người tổ chức còn hai tham chiếu vận hành tới 0.5 và trạng thái lịch sử | Không đạt |
| Checker | Khóa các quy tắc sản phẩm đã duyệt và từ chối hồi quy | Checker hiện còn bắt buộc 24 mã `D0-*` nhìn thấy và đúng một PDF embed; chưa kiểm cây sáu thẻ hay nội dung thực chất | Phải sửa ở Bước 6F |

Năm bảng thường gồm bảng quy trình ở `Bắt đầu`, hai bảng dữ liệu R2, bảng hai
chiều R4 và bảng tài nguyên R8. Bảng R1-03 là bảng dấu đạo hàm, cần đi qua cơ chế
dữ liệu dùng chung của họ bảng biến thiên nhưng không được tự ý thêm hàng giá trị
của hàm nếu đề gốc không cung cấp dữ kiện ấy.

## 5. Mâu thuẫn tài liệu và hợp đồng cần giải quyết

1. Ma trận phép chiếu Bước 4 yêu cầu sao chép hình lịch sử byte-nguyên vẹn, trong
   khi hợp đồng và manifest hiện hành đã chuyển có chủ ý sang tài sản do ZO Geometry
   sinh. Quy tắc cũ phải được đánh dấu là đã được thay thế, không được để hai chuẩn
   cùng có hiệu lực.
2. README và manifest còn mô tả ứng viên HTML là đã khóa chờ nghiệm thu, nhưng người
   dùng đã nghiệm thu và kết luận chưa đạt. Hash ứng viên cũ chỉ còn giá trị lịch sử,
   không được coi là khóa phát hành.
3. Checker HTML đang mã hóa chính hai hành vi cần loại bỏ: mã quản lý `D0-*` hiển
   thị công khai và hình PDF nhúng trong HTML. Checker đạt hiện tại chỉ chứng minh
   ứng viên khớp hợp đồng cũ, không chứng minh trải nghiệm đã đúng.
4. Hướng dẫn nội bộ còn tham chiếu Kế hoạch 0.5, dù Kế hoạch 0.6 tuyên bố thay thế
   đầy đủ 0.5 trong điều hành. Nội dung toán lịch sử vẫn phải giữ để truy nguyên,
   nhưng lớp vận hành canonical cần dùng 0.6.

## 6. Quyết định biên tập đề nghị khóa trước Bước 6B

1. Dùng `Khảo sát và định vị đầu vào` làm tên công khai; giữ `D0` trong metadata,
   ID máy đọc, tên tệp nội bộ và hồ sơ quản trị.
2. Trên giao diện, nhãn nhiệm vụ dùng dạng `R1 · Bài 01` hoặc chỉ `Bài 01` trong
   từng mạch; không hiện `D0-R1-01` cho người học.
3. `Bắt đầu` trở thành phần ngắn, hướng tới người học: mục đích, cách chọn phạm vi,
   cách làm và điều sẽ nhận sau khảo sát. Quy trình chi tiết của người hướng dẫn ở
   tài liệu riêng, không đổ toàn văn vào thẻ này.
4. `Đọc kết quả` giải thích cách đọc bằng chứng và chọn tối đa hai việc cần ôn;
   không chấm điểm tổng, không dự báo điểm thi, không tự động chẩn đoán.
5. `Thử lại` mô tả quy trình và điều kiện sử dụng nhưng không công khai 24 câu thử
   lại trong HTML.
6. Ẩn hoặc vô hiệu hóa `Tải PDF` cho đến khi Bước 7 tạo và kiểm định xong các tệp.
7. R1-03 giữ nguyên nội dung toán là bảng dấu đạo hàm; chỉ chuẩn hóa cơ chế render,
   không tự thêm một bảng biến thiên đầy đủ.

## 7. Thứ tự triển khai sau kiểm toán

1. **Bước 6B — biên tập có kiểm soát:** tạo lớp nội dung canonical cho `Bắt đầu`,
   `Đọc kết quả`, `Thử lại`; loại ngôn ngữ quản lý khỏi bề mặt công khai; cập nhật
   phần người hướng dẫn từ 0.5 sang 0.6 mà không đổi ngân hàng toán.
2. **Bước 6C — kiến trúc:** dựng cây sáu view ngay trong QMD; đặt R1–R8 thật sự
   bên trong khảo sát; bảo đảm trang vẫn đọc tuyến tính khi không có JavaScript.
3. **Bước 6D — thành phần:** áp dụng bảng responsive canonical, cơ chế dữ liệu cho
   bảng dấu và thiết kế đề bài tập trung, không lạm dụng khối màu.
4. **Bước 6E — hình học:** dùng SVG trong HTML, PDF vector trong bản in; cập nhật
   provenance và loại hợp đồng sao chép hình lịch sử đã lỗi thời.
5. **Bước 6F — kiểm định:** sửa checker để khóa tên công khai, cây view, bảng,
   định dạng hình theo output, riêng tư và trạng thái PDF; thêm fixture âm.
6. **Bước 6G — render và nghiệm thu:** render HTML, kiểm desktop/mobile và xin
   nghiệm thu trực quan rõ ràng.
7. Chỉ sau nghiệm thu HTML mới bắt đầu **Bước 7 — bốn PDF canonical**.

## 8. Bằng chứng kiểm tra tại thời điểm lập báo cáo

- `zo_qmd.py check` trên toàn thư mục D0: đạt checker repository phiên bản 2.6.0.
- Checker D0: đạt phép chiếu toàn chuỗi, 25 tệp baseline, 8 mạch, 24 nhiệm vụ
  chính, 24 câu thử lại, 24 family và fixture âm R5.
- Kết quả đạt nói trên là bằng chứng toàn vẹn nguồn hiện tại; không đảo ngược kết
  luận nghiệm thu thị giác chưa đạt và không thay thế các Bước 6B–6G.
