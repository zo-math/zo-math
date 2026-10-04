# Quy chuẩn tổ chức học liệu Ôn thi Toán THPT

Tài liệu nội bộ, chỉ áp dụng cho chuyên mục này. Tài liệu quy định kiến trúc nguồn, ranh giới xuất bản và hợp đồng canonical cho thành phần học liệu; việc một component được mô tả ở đây không tự động có nghĩa component đó đã được triển khai hoặc kiểm định kỹ thuật.

## Một bộ nguồn hiện hành

- Mỗi gói dùng lại nằm tại `hoc_lieu/<ma_goi>/`, độc lập với năm thi.
- `index.qmd` là nguồn biên soạn văn bản duy nhất của gói sau khi chuyển đổi được nghiệm thu. Dữ liệu có cấu trúc và tài sản hình được dẫn chiếu, không chép thành một nguồn bài học thứ hai.
- HTML/PDF là đầu ra sinh, không sửa tay. Mốc lịch sử không được tiếp tục dùng như nguồn phát triển song song.
- Trang khóa `tot_nghiep_thpt/<nam>/index.qmd` dẫn tới học liệu dùng lại; không sao chép bài vào từng khóa.
- Điều hành khóa và hồ sơ nội bộ nằm trong `_quy_trinh`, không đưa nguyên tài liệu điều hành lên trang người học.

## Hợp đồng cho pha tích hợp gói sau này

Mỗi gói sẽ có cấu hình kỹ thuật cục bộ với định danh duy nhất và hồ sơ `_quy_trinh/ho_so/index.yml`, cùng dùng hợp đồng và bộ kiểm định chung của chuyên mục. Cách này tránh va chạm hồ sơ giữa các nguồn cùng tên `index.qmd`.

Mẫu `mau_ho_so_san_xuat.yml` hiện chỉ ghi các quyết định cần có; chưa là schema được CLI hỗ trợ. Không tự đăng ký adapter, sửa receipt PDF hoặc tạo hồ sơ R1-G01 trong Pha 1.

Khi chuyển đổi được giao ở pha sau, phải bảo toàn nội dung, nhiệm vụ, thuật ngữ, ID, bảng và hình; kiểm chứng HTML tương tác và toàn bộ PDF. Phân biệt kiểm định tự động, nghiệm thu của con người và quyết định xuất bản. Không tự đổi trạng thái nghiệm thu/xuất bản.

## Hợp đồng canonical cho thành phần học liệu

Hợp đồng này là quy chuẩn cục bộ dùng chung cho các gói học liệu trong chuyên mục. R1-G01 và R1-G02 là hai trang kiểm chứng hợp đồng, không gói nào tự thân là toàn bộ quy chuẩn. Hiện trạng riêng của một gói chỉ trở thành baseline dùng chung khi thay đổi tương ứng đã được ghi vào tài liệu này, triển khai trên thành phần dùng chung và nghiệm thu trên các gói chịu ảnh hưởng.

### Trình tự quyết định

Khi tổ chức một nội dung, thực hiện theo thứ tự:

1. Xác định nội dung có cần tách thành khối hay hệ tiêu đề và văn bản thông thường đã đủ rõ.
2. Xác định vai trò nhận thức của nội dung theo bảng dưới đây.
3. Xác định nội dung thuộc mạch chính hay phần hỗ trợ để chọn trạng thái mở hoặc thu gọn.
4. Chọn biến thể trình bày và màu theo chức năng; không chọn màu để trang trí.
5. Gắn ID và quan hệ điều hướng nếu nội dung có gợi ý, lời giải hoặc tham chiếu chéo.

Không biến mọi đoạn quan trọng thành khối. Không đặt nhiều khối liên tiếp nếu chúng không tạo thành một đơn vị đọc có quan hệ nội tại rõ ràng.

### Các vai trò canonical

| Vai trò | Chức năng | Trạng thái mặc định | Yêu cầu |
|---|---|---|---|
| `guidance` | Chỉ dẫn cách học hoặc một tiến trình thực hiện | Thu gọn | Dùng danh sách số khi thứ tự bắt buộc, dấu chấm khi các ý song song, hoặc một đoạn văn cho chỉ dẫn ngắn. |
| `task-pause` | Câu hỏi dừng trong mạch bài học | Mở cố định | Ngắn, có hành động rõ và có ID nếu dẫn tới gợi ý hoặc lời giải. |
| `task-item` | Bài luyện tập, kiểm tra, sửa lỗi hoặc nhiệm vụ độc lập | Mở cố định | Có ID riêng; dùng trình bày trung tính để một dãy bài không tạo quá nhiều khối nặng. |
| `example` | Ví dụ đã được giải hoặc phân tích ngay trong mạch chính | Mở cố định | Không tạo thêm lời giải trùng lặp ở phần cuối. |
| `theory` | Định nghĩa, định lí, tính chất hoặc kết quả tổng quát | Mở cố định nếu thuộc mạch chính | Dùng khối đỏ theo quy chuẩn khối nội dung chung. |
| `context-note` | Giải thích, phân biệt, chứng minh hoặc lưu ý phụ thuộc ngữ cảnh | Mở hoặc thu gọn theo vai trò trong mạch | Dùng khối xám theo quy chuẩn khối nội dung chung. |
| `extension` | Bài viết nhỏ tương đối độc lập hoặc nội dung mở rộng | Thu gọn | Dùng khối vàng; không dùng màu vàng chỉ vì nội dung là ví dụ hoặc hoạt động. |
| `hint` | Gợi ý cho một nhiệm vụ cụ thể | Thu gọn | Tách khỏi `guidance`, đặt gần nhiệm vụ và có quan hệ đích rõ ràng. |
| `solution` | Lời giải, đáp án hoặc hướng dẫn chấm | Thu gọn | Một nhiệm vụ độc lập có một đích lời giải xác định và liên kết quay lại. |
| `answer-link` | Điều hướng giữa nhiệm vụ, gợi ý và lời giải | Không phải khối nội dung | Đặt sát đối tượng nguồn hoặc đích; nhãn phải mô tả đúng hành động và đích đến. |
| `figure-table` | Bảng, bảng biến thiên, hình hoặc đồ thị | Mở cố định | Dùng component và caption chuyên biệt; không dùng khối màu để thay thế cấu trúc hình hoặc bảng. |

Không bắt buộc một gói phải dùng đủ mọi vai trò hoặc đủ ba màu. Số lượng khối phải do nội dung quyết định, không dùng chỉ tiêu số lượng để làm trang giống một gói khác.

### Quy tắc cho khối `guidance`

`guidance` chỉ chứa hướng dẫn điều phối việc học hoặc một quy trình có phạm vi rõ. Không xếp câu hỏi, bài tập, ví dụ, kết luận, tiêu chí toán học, gợi ý cục bộ hoặc lời giải vào `guidance` chỉ vì nội dung có động từ mệnh lệnh.

- Dùng danh sách đánh số khi bước sau phụ thuộc bước trước hoặc thứ tự thao tác ảnh hưởng kết quả.
- Dùng danh sách dấu chấm khi các thao tác độc lập, có thể đổi thứ tự hoặc chỉ là các điểm cần lưu ý.
- Dùng một đoạn văn khi chỉ có một chỉ dẫn ngắn và không cần tách thành nhiều ý.
- Không trộn thời lượng, mục đích và chuỗi thao tác thành các bước ngang hàng nếu chúng không cùng cấp logic.

### Quy tắc cho nhiệm vụ và ví dụ

`task-pause` và `task-item` là hai biến thể của cùng vai trò nhiệm vụ, nhưng khác cường độ trình bày:

- `task-pause` dùng để ngắt mạch đúng lúc và buộc người học tự dự đoán, kiểm tra hoặc trả lời trước khi đọc tiếp;
- `task-item` dùng cho các bài trong một dãy luyện tập, kiểm tra hoặc sửa lỗi; phải đủ rõ để được dẫn chiếu độc lập nhưng không cần hình thức thị giác nặng như một khối nhấn mạnh.

Một nội dung đã trình bày cả đề, lập luận và kết quả trong mạch bài là `example`, không phải `task`. Nếu người học phải tự làm trước rồi mới xem phần xử lí tách riêng, nội dung đó là `task` và phần xử lí là `solution`.

### Quy tắc tham chiếu nhiệm vụ, gợi ý và lời giải

- Nhiệm vụ độc lập dùng liên kết hai chiều một-một: nhiệm vụ dẫn tới đúng lời giải và lời giải quay lại đúng nhiệm vụ.
- Nếu có gợi ý, nhiệm vụ dẫn tới đúng gợi ý; gợi ý phải cho phép quay lại nhiệm vụ mà không thay thế đích lời giải.
- Một nhóm câu hỏi rất ngắn có thể dùng lời giải tổng hợp khi việc nhóm có chủ ý sư phạm; mỗi câu vẫn phải có anchor đủ chính xác để người đọc quay lại vị trí tương ứng.
- Nhãn liên kết phải nêu đúng loại đích. Cặp đề–lời giải dùng hai nhãn ngắn `Xem lời giải` và `Xem đề bài`; chỉ thêm định danh vào nhãn khi một đích khác không thể được nhận biết từ ngữ cảnh.
- Không tạo liên kết tới một lời giải lặp lại đối với `example` đã được giải ngay trong mạch bài.

### Tiêu đề và ID

- Ưu tiên tiêu đề mô tả nội dung cụ thể; chỉ dùng tên chức năng như `Gợi ý` hoặc `Lời giải` khi không có tên cụ thể rõ hơn.
- Khối thuộc hệ `zo-block` phải dùng cấu trúc tiêu đề canonical của hệ khối; không giả lập tiêu đề bằng một dòng chữ đậm trong thân khối.
- Mọi nhiệm vụ, gợi ý và lời giải tham gia tham chiếu chéo phải có ID duy nhất, ổn định và không phụ thuộc vào số dòng hoặc văn bản tiêu đề tự sinh.
- Sau khi một gói được phát hành, không đổi ID nếu chưa có cơ chế tương thích cho liên kết cũ.

## Baseline canonical 1.0 sau nghiệm thu R1-G01 và R1-G02

Định danh baseline: `on-thi-learning-components/1.0`.

Baseline này được chốt từ hai gói kiểm chứng R1-G01 và R1-G02 sau nghiệm thu HTML ở desktop và mobile 430 px, 390 px. Hệ PDF của từng gói được nghiệm thu và khóa bằng ma trận hồi quy riêng ở phần ánh xạ canonical sang PDF.

### Nguồn kỹ thuật dùng chung

- `assets/css/_zo_learning_components.scss` là nguồn trình bày chung cho các vai trò học liệu.
- `assets/lua/zo_learning_components.lua` là nguồn chuyển đổi chung từ vai trò QMD sang cấu trúc HTML.
- `assets/css/zo_on_thi_learning_package.css` cung cấp khung trang, thanh thẻ, bảng và hình dùng chung; scope canonical là `.zo-on-thi-package` và `body.zo-on-thi-package-page`.
- `assets/html/zo_on_thi_learning_package_script.html` cung cấp hành vi điều hướng, trạng thái thẻ, mục lục trong bài học và hỗ trợ cuộn bảng dùng chung.
- Hai tệp lịch sử `hoc_lieu/r1_g01/giao_dien/r1_g01.css` và `r1_g01_script.html` chỉ được giữ tạm để bảo toàn hồ sơ provenance của các PDF R1-G01 hiện có; QMD không được tham chiếu chúng. Chúng được loại bỏ cùng lúc tái lập provenance PDF ở pha PDF kế tiếp.
- CSS riêng của mỗi gói chỉ chứa ngoại lệ thật sự của gói; không sao chép component dùng chung để tạo baseline song song.

### Khung trang và điều hướng

- Một trang có phần đầu gồm tiêu đề, phụ đề nếu có, trạng thái, đoạn giới thiệu và thanh thẻ.
- Thứ tự thẻ canonical là `Cách học`, `Bài học`, `Luyện tập`, `Kiểm tra`, `Sửa lỗi`, `Ôn lại`, `Lời giải`, `Tải PDF`, `Toàn văn`. Gói không có nội dung cho một thẻ phải khai báo quyết định riêng thay vì đổi nghĩa thẻ.
- Thanh thẻ là vùng cuộn ngang cục bộ trên màn hình hẹp, giữ thẻ đang chọn cách mép nhìn thấy ít nhất 12 px; thanh thẻ không được gây tràn ngang cấp trang.
- Thanh thẻ giữ nguyên trong slot `sticky` ở `top: 0`. Headroom chỉ quản lí Navbar: khi kéo xuống chỉ thanh thẻ còn ở đầu khung nhìn; khi kéo lên Navbar xuất hiện lại. Không chuyển node thanh thẻ vào header hoặc ghép nó vào transform của Navbar.
- `Toàn văn` dùng cùng một cây DOM canonical, không sao chép nội dung sang cây thứ hai. Khi JavaScript không chạy, nội dung vẫn phải đọc được.

### Khối thu gọn và bề mặt

- Tiêu đề của mọi khối thu gọn có chiều cao tối thiểu 44 px và dùng cùng cơ chế dấu mở–đóng.
- `guidance` có tiêu đề `Cách thực hiện`, bề mặt trắng, chữ tiêu đề xám cùng màu với `Mục lục`; nội dung dùng đoạn văn, danh sách dấu chấm hoặc danh sách đánh số theo quan hệ logic.
- `solution` dùng bề mặt xám nhạt và tiêu đề mô tả đúng lời giải hoặc bài tương ứng.
- `hint` là vai trò riêng, không được đếm hoặc trình bày như `guidance`; tiêu đề ngắn gọn như `Cần một gợi ý?`.
- Nội dung thông thường không được đóng khối chỉ để tạo nền, viền hoặc cảm giác nhấn mạnh. Công thức hiển thị không dùng khối trang trí `equation` và không dùng `\boxed{...}`.

### Nhiệm vụ, ví dụ và liên kết

- `task-pause` dùng `.zo-learning-task.zo-learning-task--pause`; `task-item` dùng `.zo-learning-task.zo-learning-task--item`.
- Nhãn nhiệm vụ nằm trong chính khối nhiệm vụ. Liên kết tới gợi ý hoặc lời giải nằm cuối khối nguồn; liên kết quay lại nằm cuối khối đích.
- Hai nhãn ngắn canonical cho cặp đề–lời giải là `Xem lời giải` và `Xem đề bài`. Nhãn khác chỉ dùng khi đích không phải lời giải hoặc đề bài.
- `example` dùng `.zo-learning-example` hoặc `.zo-learning-example-heading` và không tạo lời giải lặp lại ở cuối trang.
- Anchor phải chi tiết, duy nhất và liên kết hai chiều phải trỏ đúng cặp nhiệm vụ–lời giải.

### Bảng, bảng biến thiên và hình

- Bảng thường có khung ngoài và đường kẻ ngang–dọc đầy đủ. Header và row header phải được khai báo theo ngữ nghĩa bảng.
- Chọn `fit` khi bảng vẫn đọc thoải mái trên mobile; chọn `scroll` và `min_width` khi co bảng làm cột quá hẹp. Bảng `scroll` cuộn ngang trong vùng riêng, có chỉ dẫn khi thật sự tràn và không làm trang tràn ngang.
- Bảng biến thiên và đồ thị được căn giữa, dùng tài sản vector canonical. Caption đặt dưới tài sản, cỡ chữ phụ, là câu hoàn chỉnh và kết thúc bằng dấu chấm.
- Không gán công thức hàm số vào nhãn đồ thị nếu đề bài không cung cấp công thức ấy.

### Ánh xạ canonical sang PDF

- PDF giữ nguyên vai trò nội dung của QMD/HTML nhưng dùng quy tắc dàn trang phù hợp khổ A4; không sao chép máy móc kích thước hoặc hành vi thu gọn của trình duyệt.
- `guidance` dùng khung nền trắng, viền xám nhạt và tiêu đề xám; `solution` dùng nền xám nhạt; `theory` tiếp tục dùng khung đỏ. Nội dung thường không được tự động đóng khung khi chuyển sang PDF.
- Bảng thường có khung ngoài và đường kẻ ngang–dọc đầy đủ trong PDF. Tỉ lệ cột lấy từ hợp đồng bảng của gói; bảng dài được phép ngắt trang nhưng phải lặp hàng tiêu đề.
- Bảng biến thiên và đồ thị dùng PDF vector, căn giữa; caption nằm dưới tài sản, dùng cỡ chữ phụ và màu xám.
- Dòng `.zo-source-note` được đặt sau nội dung được dẫn, dùng cỡ chữ phụ và màu xám; văn bản và dấu câu phải giữ nguyên từ nguồn QMD.
- Liên kết nội bộ còn đích trong phép chiếu được giữ nội bộ. Liên kết vượt phạm vi biến thể được đổi sang URL canonical có chế độ xem tương ứng; nhãn liên kết không được tự ý đổi nghĩa.
- Tránh tách tiêu đề khỏi phần mở đầu của khối, bảng hoặc hình; không buộc toàn bộ khối dài nằm trên một trang nếu điều đó tạo khoảng trắng lớn hoặc tràn trang.

Baseline PDF canonical đầu tiên của hệ thành phần dùng chung là
`on-thi-learning-pdf/1.0`, được chốt từ tám biến thể R1-G01 sau nghiệm thu thị
giác ngày 2026-09-30. Ma trận hồi quy của gói là: `full` 41 trang, `student` 31
trang, `bai_hoc` 22 trang, `luyen_tap` 7 trang, `kiem_tra` 5 trang, `sua_loi` 5
trang, `on_lai` 3 trang và `loi_giai` 12 trang. Đây là baseline hồi quy riêng
của R1-G01, không phải chỉ tiêu số trang cho gói khác. Metadata thẻ tải phải lấy
đúng số trang của đầu ra hiện hành; checker của gói phải khóa toàn bộ ma trận,
provenance và quan hệ phép chiếu thay vì chỉ kiểm tra PDF tồn tại.

Baseline này xác nhận cách ánh xạ component, bảng, bảng biến thiên, hình, liên
kết và dàn trang A4. R1-G02 đã được nghiệm thu thị giác và chốt ở Pha 6C ngày
2026-09-30 với ma trận hồi quy riêng: `full` 26 trang, `student` 17 trang,
`bai_hoc` 10 trang, `luyen_tap` 6 trang, `kiem_tra` 4 trang, `sua_loi` 5 trang,
`on_lai` 3 trang và `loi_giai` 10 trang. Mọi thay đổi đầu vào đã được khai trong
provenance phải làm biến thể chịu ảnh hưởng thành `STALE` cho tới khi được dựng
lại bằng pipeline canonical và kiểm nghiệm hồi quy.

### Công thức và nguồn đối chiếu

- Công thức dài được đặt trên dòng riêng khi việc đặt trong câu làm giảm khả năng đọc; việc tách dòng không tạo thêm khối nền hoặc viền.
- Với công thức phân nhánh, mỗi nhánh viết theo mẫu `biểu thức & \text{khi } điều kiện`. Không đặt dấu phẩy giữa biểu thức và điều kiện. Dấu phẩy đặt sau điều kiện của các nhánh chưa cuối; dấu chấm đặt sau điều kiện của nhánh cuối khi công thức kết thúc câu.
- Dòng nguồn đối chiếu dùng `.zo-source-note`, đặt sau nội dung được dẫn, viết thành câu hoàn chỉnh, không dùng ngoặc vuông, không viết tắt tên sách hoặc từ `trang`.

### Hàng rào kiểm định

- Checker của từng gói khóa số lượng và quan hệ component theo nội dung riêng, đồng thời khóa các bất biến dùng chung nêu trên.
- Checker HTML/mobile phải phân biệt tràn ngang cấp trang với cuộn ngang cục bộ có chủ ý của thanh thẻ và bảng.
- Nghiệm thu thị giác tối thiểu dùng desktop, 430 px và 390 px; phải xem cả trạng thái mặc định và các khối thu gọn đã mở.
- Thay đổi nguồn CSS, Lua hoặc JavaScript dùng chung phải chạy checker của cả R1-G01 và R1-G02. Render và nghiệm thu lại chỉ được thực hiện khi nhiệm vụ cho phép.

## Ánh xạ kỹ thuật và chuyển tiếp

Các tên dưới đây ghi trạng thái đã chốt của hai gói. Lớp `r1-*` còn xuất hiện để giữ tương thích, nhưng checker phải khóa vai trò canonical `zo-learning-*` tương ứng.

| Vai trò canonical | Ánh xạ kỹ thuật đã chốt | Trạng thái trên hai gói |
|---|---|---|
| `guidance` | `.zo-learning-guidance`; lớp `r1-details.r1-guidance` được giữ tương thích | Đã áp dụng và kiểm định trên cả hai gói. |
| `task-pause` | `.zo-learning-task.zo-learning-task--pause` | Đã áp dụng và kiểm định trên cả hai gói. |
| `task-item` | `.zo-learning-task.zo-learning-task--item` | Đã áp dụng và kiểm định trên cả hai gói. |
| `example` | `.zo-learning-example`, `.zo-learning-example-heading` | Đã áp dụng và kiểm định trên cả hai gói. |
| `theory` | `.zo-block.zo-block-red` với `.zo-block-title` | Đã áp dụng; số lượng do nội dung từng gói quyết định. |
| `context-note` | `.zo-learning-context-note` hoặc khối xám sau khi phân loại | R1-G01 có một khối đọc thêm; R1-G02 không đóng khối cho giải thích thông thường. |
| `extension` | `.zo-block.zo-block-yellow` khi đúng vai trò mở rộng | Không bắt buộc xuất hiện; không chuyển máy móc từ class cũ. |
| `hint` | `.zo-learning-hint` | Đã áp dụng cho các gợi ý của R1-G02; tách khỏi `guidance`. |
| `solution` | `.zo-learning-solution`; lớp `r1-details.r1-solution` được giữ tương thích | Đã áp dụng và kiểm định trên cả hai gói. |
| `answer-link` | `.answer-link` với anchor hai chiều | Đã áp dụng và kiểm định trên cả hai gói. |
| `source-note` | `.zo-source-note` | Đã áp dụng và kiểm định trên cả hai gói. |
| `figure-table` | `.r1-table-*`, `.r1-bbt`, `.r1-figure`, `.r1-figcaption` | Đã kiểm định trên hai gói; tiếp tục dùng component chuyên biệt và tài sản vector. |

### Ranh giới chuyển đổi hai gói hiện có

- R1-G01 và R1-G02 đã hoàn tất lượt kiểm chứng HTML cho baseline 1.0. Việc thay đổi tiếp theo vẫn phải giữ nguyên nội dung toán học, thứ tự nhận thức, ID, bảng và hình nếu người dùng không giao biên tập nội dung.
- R1-G01 và R1-G02 đều đã có hệ PDF canonical được nghiệm thu riêng; ma trận số trang của mỗi gói là bất biến hồi quy cục bộ, không phải chỉ tiêu dùng chung cho gói khác.
- Không sao chép CSS hoặc JavaScript riêng từ gói này sang gói khác để tạo thêm một baseline ngầm. Thành phần dùng chung phải có một nguồn kỹ thuật chính thức trước khi được dùng cho các gói tiếp theo.
- Một sửa lỗi cục bộ trong R1-G01 không tự động thay đổi baseline. Baseline chỉ đổi khi hợp đồng này được cập nhật, thành phần dùng chung được triển khai và các gói chịu ảnh hưởng được nghiệm thu lại.

## Hàng rào bắt buộc

Các trang và tài sản đã duyệt của chuyên mục chỉ được chọn qua allowlist trong `publish_public.yml`. `_quy_trinh` luôn bị chặn kể cả khi mở các trang học. Không đưa liên kết, dữ liệu chỉ mục hay resources chứa đường dẫn nội bộ vào cây public.

Preview dùng profile `on-thi-preview`, chỉ ở `127.0.0.1`; không phải pipeline xuất bản. `zo_publish.py` phải từ chối profile này và kiểm tra đường dẫn bị cấm sau chuẩn hóa trong manifest, HTML, `search.json` và sitemap.
