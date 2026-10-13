# Quy chuẩn sản xuất đồ thị hàm số ZO Math

**Phiên bản:** 0.2

**Ngày biên soạn:** 21/09/2026

**Trạng thái:** Quy chuẩn mới cho sản phẩm đồ thị tương lai; tài sản thực thi dùng chung và kế hoạch chuyển đổi dự án cũ chưa được ban hành.

**Căn cứ:** Toàn văn v0.1; ma trận biên tập đã duyệt; kết quả kiểm chứng thị giác của các mẫu audit v0.2 và v0.3.2.

**Phạm vi áp dụng:** Sản phẩm đồ thị hàm số mới của ZO Math. Không tự động áp dụng hồi tố cho style hay dự án hiện hành.

> Đồ thị phải đúng về toán học, giúp người học nhận ra điều cần hiểu và có diện mạo nhất quán với ZO Math. Việc biên dịch thành công chưa chứng minh rằng hình đã đạt cả ba yêu cầu.

**Gợi ý đọc lần đầu:** Mục 5 xác lập phong cách; Mục 6–7 giải quyết lớp và nhãn; Mục 9 giải quyết kích thước thật; Mục 15 xác định mẫu thử tiếp theo. Những phần còn lại dùng để triển khai, kiểm chứng và tái sử dụng nhất quán.

## 1. Mục đích, phạm vi và cách đọc

### 1.1. Mục đích

Tài liệu xác lập cách sản xuất đồ thị hàm số cho ZO Math: từ quyết định toán học, bố trí các thành phần, dựng hình đến kiểm chứng PDF, SVG và hình trong học liệu.

Đối tượng sử dụng là người biên soạn, người phát triển công cụ, Codex và các tác nhân AI. Người sử dụng không phải tự phát minh phong cách mới cho mỗi hình, nhưng vẫn phải đưa ra quyết định bố trí phù hợp với từng đối tượng toán học.

Đây là quy chuẩn sản xuất, không phải chương trình vẽ đã hoàn thành. Những tên vai trò, trường đặc tả và đoạn mã minh họa trong tài liệu chưa chứng minh rằng công cụ tương ứng đã tồn tại trong repository.

### 1.2. Phạm vi

Áp dụng cho đồ thị hàm số thực một biến, đồ thị từng phần, đường tham số phục vụ trực tiếp việc khảo sát hàm số, và các đối tượng đi kèm: hệ trục, điểm, tiếp tuyến, tiệm cận, đường chiếu, miền tô, nhãn, chú giải.

Không bao gồm thiết kế toàn trang Quarto, hình học thuần túy, biểu đồ thống kê, sơ đồ tư duy, đồ họa chuyển động hoặc toàn bộ quy chuẩn bảng biến thiên. Các lĩnh vực này có thể tham chiếu hệ phong cách chung ở Mục 5, nhưng không mặc nhiên kế thừa mọi quy tắc riêng của đồ thị.

### 1.3. Mức bắt buộc

- **Phải / không được:** điều kiện để nghiệm thu.
- **Mặc định:** áp dụng nếu không có lí do cụ thể để làm khác.
- **Ưu tiên:** thứ tự lựa chọn khi có nhiều cách hợp lệ.
- **Thông số khởi đầu:** giá trị để dựng mẫu, cần xác nhận ở kích thước sử dụng thật.
- **Ngoại lệ:** khác mặc định, phải có lí do và bằng chứng hình vẫn đúng, rõ.

Các màu, phông và vai trò trong Mục 5 là quyết định nhận diện của ZO Math. Các giá trị đã được kiểm chứng bằng mẫu — gồm nét đường cong 1,1 pt, trục 0,8 pt, vạch chia dài 0,75 mm với nét 0,45 pt và khoảng nhãn điểm khoảng 2–3 mm — là mặc định của phiên bản 0.2. Chúng vẫn phải được xác nhận ở kích thước dùng thật; đây không phải các hằng số do TikZ hoặc một tiêu chuẩn quốc tế quy định.

### 1.4. Quan hệ với style và dự án hiện hành

Phiên bản 0.2 điều hành các sản phẩm đồ thị mới. Nó không tự động thay thế `assets/tex/zo-graph-styles.tex`, các style được nhúng trong dự án 100+ Hàm số, đồ thị R1-G01 hay bất kỳ thành phẩm canonical nào.

Việc chuyển một dự án hoặc tài sản cũ sang v0.2 là một nhiệm vụ migration riêng: phải xác định phạm vi, kiểm hồi quy và được chủ dự án chấp thuận. Không sửa, đổi tên, xóa hoặc dựng lại hàng loạt tài sản cũ chỉ vì v0.2 được ban hành.

Các mẫu trong `_audit/` là bằng chứng thiết kế cho tài liệu này, không phải phụ thuộc chạy của sản phẩm tương lai.

## 2. Nguyên tắc nền tảng

### 2.1. Một hình phải có một câu trả lời sư phạm chính

Trước khi dựng, viết được một câu:

> Sau khi xem hình này, người học cần nhận ra điều gì?

Ví dụ: “Tiếp tuyến nằm ngang tại một điểm không đủ để kết luận hàm số có cực trị tại điểm đó.”

Thành phần không giúp trả lời câu hỏi chính hoặc không cần để đọc đúng hình nên được lược bỏ. Không thêm lưới, đường chiếu, tọa độ, đạo hàm hay chú giải chỉ vì công cụ có thể vẽ.

Cách bắt đầu từ thông điệp, giữ nhất quán hình–văn bản và tránh nhãn bị đường che phù hợp với hướng dẫn thiết kế của PGF/TikZ. Những quy tắc cụ thể dưới đây là sự vận dụng cho ZO Math. [S1 — Hướng dẫn đồ họa PGF/TikZ](https://tikz.dev/guidelines)

### 2.2. Tính đúng ưu tiên hơn sự cân đối

Không dịch điểm, đổi miền xác định, kéo lệch đường cong hoặc sửa dữ liệu để né nhãn. Có thể dời nhãn, đổi cửa sổ quan sát hoặc phân bố không gian, nhưng phải giữ ý nghĩa toán học và mục đích hình.

Hình minh họa không thay cho chứng minh. Không suy từ một cửa sổ hữu hạn rằng tính chất đúng trên toàn tập xác định.

### 2.3. Phân biệt giao cắt toán học và xung đột trình bày

Hai đường cong cắt nhau, tiếp tuyến tiếp xúc với đường cong, đồ thị đi qua trục: đó có thể là thông tin cần giữ.

Chữ bị đường gạch qua, nhãn đè marker, chú giải che cực trị: đó là lỗi trình bày.

Không “sửa” giao cắt thật bằng cách tách hai nét hoặc vẽ một đường bắc cầu giả. Cũng không chấp nhận xung đột trình bày chỉ vì mã đã biên dịch.

### 2.4. Phân cấp theo nhiệm vụ, không theo số lượng nét

Thông thường đường cong chính là đối tượng nổi bật nhất; trục giúp định hướng; đường phụ cung cấp căn cứ đọc; nhãn giải thích; khung chỉ tổ chức không gian.

Khi mục tiêu là so sánh hai hàm ngang hàng, hai đường có cùng mức ưu tiên. Không tùy tiện biến một đường thành “phụ” chỉ vì nó được viết sau trong mã.

### 2.5. Một màu nhận diện, nhiều kiểu nét

Mọi đường cong hàm số ngang hàng dùng cùng màu đỏ ZO Math `#EF5350` và cùng độ dày mặc định 1,1 pt. Phân biệt theo thứ tự mặc định: đường thứ nhất nét liền, đường thứ hai nét đứt, đường thứ ba nét gạch–chấm.

Không tạo palette nhiều màu cho các đường cong ngang hàng. Kiểu nét phải đủ rõ khi in đen trắng; nhãn hoặc chú giải chỉ bổ sung nhận diện. Khi có hơn ba đường ngang hàng, phải xem lại mật độ thông tin, khả năng tách hình hoặc cơ chế mã hóa khác đã được duyệt; không tự phát minh màu đường thứ tư.

## 3. Nguồn có thẩm quyền và cấu trúc tài sản

### 3.1. Phân biệt vai trò, không bắt buộc tăng số tệp

| Lớp tài sản | Nội dung có thẩm quyền | Cách thay đổi |
| --- | --- | --- |
| Đặc tả toán học và sư phạm | Hàm, miền, nhánh, điểm, mục đích, dữ kiện cho phép hiển thị | Sửa có chủ ý và kiểm tra lại |
| Phong cách có phiên bản | Màu, phông, nét, kích thước ký hiệu và quy tắc bố trí chung | Nâng phiên bản có kiểm chứng |
| Nguồn dựng | TikZ/PGFPlots, vị trí nhãn, cửa sổ quan sát; script Python nếu cần | Sửa tại nguồn |
| Dữ liệu sinh | Bảng điểm hoặc kết quả số từ script | Tái sinh, không sửa tay |
| Thành phẩm | PDF vector, SVG | Tái sinh, không chỉnh trực tiếp |

Một hình đơn giản không cần năm tệp để tương ứng với năm hàng. Có thể ghi đặc tả trong phần chú thích đầu tệp TeX và dùng macro cho tham số. Hình phức tạp có thể dùng một đặc tả cấu trúc riêng.

Nếu một thông tin xuất hiện ở nhiều nơi, phải xác định nơi chịu trách nhiệm và cách đối chiếu. Không duy trì hai công thức độc lập — một trong JSON, một trong TeX — mà không có kiểm tra chúng khớp nhau.

### 3.2. Nội dung tối thiểu của đặc tả

1. Mã hình ổn định; vị trí bài học sử dụng.
2. Câu hỏi sư phạm và đối tượng chính.
3. Công thức, tham số, tập xác định, miền đang xét.
4. Các nhánh liên tục và những điểm phải tách.
5. Điểm/đường/miền bắt buộc; các giá trị chính xác.
6. Cửa sổ quan sát, tỉ lệ trục và cách lấy mẫu.
7. Nội dung nhãn; chú thích; văn bản thay thế.
8. Những vùng chứa thông tin không được che.
9. Phiên bản quy chuẩn, style và ngoại lệ.
10. Vai trò hình: giải thích, câu hỏi hay hình cố ý sai để phân tích lỗi.

Không tự “sửa đúng” hình cố ý sai. Loại hình này phải có cờ biên tập và mô tả lỗi chủ ý trong hồ sơ riêng; lời giải hoặc nội dung thay thế không được vô tình tiết lộ đáp án nếu người học đang làm bài.

### 3.3. Style dùng chung có phiên bản

Quy chuẩn văn bản mô tả quyết định; tài sản style thực thi quyết định ấy. Không buộc mỗi hình chép hàng trăm dòng style.

Nguồn mới phải tham chiếu một bản style xác định. Khi khóa sản phẩm, phải lưu được chính nội dung style/phông cần thiết trong lịch sử Git hoặc bản đóng gói tương ứng; chỉ ghi số phiên bản hay hash mà không thể lấy lại tệp là chưa đủ để tái tạo.

Không thay nội dung một bản style đã khóa rồi giữ nguyên tên phiên bản. Một thay đổi diện mạo có chủ ý phải nâng phiên bản và ghi phạm vi ảnh hưởng.

Vị trí tài sản mới sẽ được quyết định khi triển khai, dựa trên cấu trúc đang có. Tài liệu này không yêu cầu lập thêm kho, cây dự án hoặc hệ quản lí song song.

### 3.4. Đóng gói tự chứa

Tệp TeX “độc lập” có nghĩa là dựng riêng được khi có các phụ thuộc đã khai báo, không nhất thiết chứa mọi phông và style bên trong nó.

Khi cần giao ra ngoài, tạo gói gồm nguồn, bản style đúng phiên bản, dữ liệu và phông được phép phân phối cùng giấy phép. Bản đóng gói là ảnh chụp để tái tạo, không trở thành nguồn style thứ hai.

## 4. Phân tích toán học và chọn phương pháp dựng

### 4.1. Ba miền khác nhau

- **Tập xác định:** nơi hàm có nghĩa.
- **Miền lấy mẫu:** các khoảng hoặc tham số được dùng để tính điểm vẽ.
- **Miền quan sát:** cửa sổ hiển thị.

Cắt nhánh tại biên cửa sổ không có nghĩa hàm kết thúc ở đó. Khoảng bỏ lấy mẫu gần điểm kỳ dị không phải một phần bị xóa khỏi tập xác định.

### 4.2. Kiểm tra trước khi dựng

Chỉ những mục có liên quan mới cần phân tích sâu, nhưng không được bỏ qua yếu tố có thể làm sai hình:

| Nhóm | Nội dung phải biết |
| --- | --- |
| Định nghĩa | Tập xác định; giá trị gán riêng; đầu mút thuộc/không thuộc |
| Đặc điểm | Nghiệm, dấu, đối xứng, tuần hoàn; điểm và giá trị quan trọng |
| Biến thiên | Đơn điệu, cực trị, tiếp tuyến; tính cong/điểm uốn khi phục vụ mục tiêu |
| Giới hạn | Biên miền, gián đoạn, tiệm cận và hành vi vô cực có liên quan |
| Số học | Nguy cơ tràn số, mất chính xác, bỏ sót dao động, nối nhầm nhánh |
| Diễn giải | Hình cho phép kết luận gì, không cho phép kết luận gì |

Một điểm có đạo hàm bằng không không tự động là cực trị. Một điểm không xác định không tự động là tiệm cận đứng. Đường cong rất gần một đường thẳng trong hình không đủ xác lập tiệm cận.

### 4.3. Phân công công cụ

TikZ/PGFPlots là bộ dựng hình chuẩn. Nguồn được biên dịch bằng LuaLaTeX, dùng STIX Two Text và STIX Two Math. Thành phẩm chuẩn gồm PDF vector và SVG cho web.

| Trường hợp | Cách thực hiện mặc định |
| --- | --- |
| Hàm sơ cấp, tính ổn định | PGFPlots tính biểu thức và dựng đường |
| Gián đoạn hoặc tiệm cận đã biết | Tách nhánh rõ trong nguồn; mỗi nhánh một lệnh vẽ/dải dữ liệu |
| Hàm từng phần | Vẽ từng phần đúng miền; marker đầu mút riêng |
| Tính toán lớn, nghiệm số, lấy mẫu thích nghi | Python tính và xuất dữ liệu; PGFPlots dựng |
| Đường tham số | Lấy mẫu theo tham số và giữ thứ tự điểm |
| Diện tích/miền giữa các đường | Dựng đúng đường biên rồi tô; kiểm tra miền tích hợp/tô |
| Quan hệ góc, khoảng cách, đường tròn | Bảo toàn tỉ lệ đơn vị hai trục |

Python chỉ hỗ trợ tính toán, sinh dữ liệu hoặc kiểm chứng; không phải bộ dựng thị giác canonical thứ hai. Có thể dùng hình tính toán tạm để chẩn đoán, nhưng thành phẩm chuẩn vẫn đi qua TikZ/PGFPlots.

### 4.4. Điều kiện với dữ liệu số

- Lưu công thức, tham số, miền, độ chính xác và phiên bản phụ thuộc cần để tái sinh.
- Phân biệt giá trị chính xác với giá trị gần đúng; không ghi một nghiệm số như một hằng số chính xác.
- Không suy ra nghiệm/cực trị chỉ từ một dãy điểm thưa.
- Giữ ranh giới nhánh. Không xuất thành một đường liên tục xuyên qua điểm loại.
- Không nội suy trơn qua góc gãy, điểm gián đoạn hoặc đoạn hằng.
- Không tự chạy mã Python/TeX nằm trong dữ liệu nhập chưa được kiểm tra.

### 4.5. Lấy mẫu và độ tin cậy

Không đặt một số mẫu lớn duy nhất cho mọi hàm. Khi tăng mật độ kiểm tra, các đặc điểm cần đọc phải ổn định; sự ổn định số không thay cho phân tích toán học.

Với đường trơn hữu hạn, có thể kiểm tra độ lệch điểm giữa đoạn và dây cung trong tọa độ hiển thị, kèm giới hạn bước dựa trên đặc điểm của hàm. Phép thử điểm giữa đơn lẻ vẫn có thể bỏ sót dao động; không dùng nó như chứng nhận phổ quát.

Với $y=\sin(1/x)$, có thể lấy mẫu theo $t=1/x$ rồi chuyển lại tọa độ. Phải ghi miền được vẽ, ngưỡng dừng và giới hạn của minh họa. Không dùng một mảng màu đặc rồi gọi đó là biểu diễn đầy đủ vô hạn dao động.

Các điểm như nghiệm, cực trị, điểm gãy và đầu mút cần có mặt đúng vị trí trong dữ liệu hoặc được dựng riêng. Không bật làm trơn tùy tiện nếu có thể tạo cực trị giả.

### 4.6. Chọn cửa sổ quan sát

Khai báo tường minh bốn giới hạn của cửa sổ. Chọn theo đặc điểm cần đọc, không để một vài giá trị rất lớn gần tiệm cận quyết định toàn bộ chiều cao.

- Chừa khoảng thở quanh điểm quan trọng; 5–10% phạm vi mỗi chiều là mức bắt đầu để thử, không phải điều kiện bắt buộc.
- Với hàm bị chặn, cho thấy rõ các mức biên cần so sánh.
- Với hàm tuần hoàn, vẽ số chu kỳ vừa đủ để đọc quy luật.
- Giữ đối xứng cửa sổ khi nó giúp đọc đối xứng của hàm; không giữ chỉ để cân hình.
- Khi so sánh nhiều hình, dùng cùng thang đo nếu độ lớn là nội dung so sánh; nếu đổi thang phải nêu rõ.
- Không mở rộng cửa sổ chỉ để nhét nhãn dài rồi làm phần dữ liệu chính nhỏ đi.

Gần tiệm cận, điểm dừng lấy mẫu phải đủ để nhánh rời cửa sổ tự nhiên, nhưng không quá gần điểm kỳ dị gây tràn số. Ghi giới hạn quan sát không phải giới hạn miền giá trị.

## 5. Hệ phong cách biểu diễn toán học ZO Math

### 5.1. Phạm vi dùng chung

Phần này là lớp phong cách có thể tái sử dụng cho đồ thị và bảng biến thiên. Các tên token kế thừa tài liệu nền được giữ để giảm thay đổi không cần thiết; nghĩa của token phải rõ, không được suy chỉ từ tên.

Đồ thị dùng màu đỏ cho đối tượng chính không có nghĩa dấu âm, chiều giảm hoặc câu sai phải tô đỏ. Trong bảng biến thiên, màu không được thay thế dấu toán học hoặc trạng thái đúng/sai.

### 5.2. Bảng màu thực thi của v0.2

| Token | HEX | Vai trò |
| --- | --- | --- |
| `zoPlotBackground` | `FFF9E9` | Nền minh họa mặc định |
| `zoPlotBorder` | `DFD7CA` | Viền trang trí mảnh |
| `zoText` | `3E3A35` | Chữ và ký hiệu chính |
| `zoTextStrong` | `25221F` | Nhấn chữ có chọn lọc |
| `zoAxis` | `554F48` | Trục, vạch chia, nét cấu trúc |
| `zoGraphMain` | `EF5350` | Tất cả đường cong hàm số |
| `zoGraphStrong` | `BF4240` | Điểm/đoạn cần nhấn của đối tượng chính |
| `zoGridMajor` | `DFD7CA` | Lưới chính khi thực sự cần |
| `zoGridMinor` | `F8F5F0` | Lưới phụ, mặc định tắt |
| `zoHighlightLight` | `FFF4D4` | Miền tô vàng nhạt |
| `zoHighlight` | `FFCA28` | Nhấn diện tích nhỏ; không dùng làm chữ nhỏ |
| `zoWhite` | `FFFFFF` | Nền giấy/chú giải hoặc ngoại lệ được chỉ rõ |
| `zoBackground` | `FBFAF8` | Nền trung tính khi có lí do |

Không dùng vàng nâu, xanh xám hoặc màu thử nghiệm khác cho đường cong hàm số. Không mở rộng palette chỉ để làm các đường ngang hàng khác màu. Nếu thật sự cần vai trò mới, phải định nghĩa vai trò trước khi chọn màu từ hệ nhận diện đã được duyệt.

### 5.3. Tương phản

Chữ thường dùng `zoText`, kể cả nhãn gọi tên đường đỏ. Không lấy màu đường cong làm màu mọi công thức.

Mục tiêu kiểm tra cho web: chữ thông thường đạt tỉ lệ tương phản ít nhất 4,5:1; nét mang thông tin cần nhận biết đạt ít nhất 3:1 với nền kề, trừ ngoại lệ được đánh giá theo đúng phạm vi tiêu chí. Viền trang trí không phải dữ liệu. Đây là các mốc tham chiếu từ WCAG, không phải tuyên bố toàn bộ học liệu đã đạt WCAG. [S7 — Tương phản đồ họa](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), [S8 — Tương phản chữ](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

Tính theo màu sRGB đặc trên nền `FFF9E9`:

| Màu | Tỉ lệ xấp xỉ | Hệ quả thiết kế |
| --- | ---: | --- |
| Chữ `3E3A35` | 10,73:1 | Dùng cho nhãn |
| Trục `554F48` | 7,69:1 | Phù hợp nét cấu trúc |
| Đỏ chính `EF5350` | 3,32:1 | Giữ cho nét chính; không dùng làm chữ nhỏ mặc định |
| Đỏ đậm `BF4240` | 4,91:1 | Có thể dùng cho nhấn cần tương phản cao |
| Viền `DFD7CA` | 1,36:1 | Chỉ là viền/lưới hỗ trợ, không mang nghĩa duy nhất |

Đây là phép tính trên màu đặc, chưa xét khử răng cưa, độ mảnh hoặc nền miền tô. Phải xem thực tế ở kích thước nhỏ và kiểm tra lại khi đổi nền. Không giảm opacity của đường chính cho “nhẹ mắt” rồi làm mất tương phản.

### 5.4. Phông và ký hiệu

- Văn bản trong hình: STIX Two Text.
- Toán trong hình: STIX Two Math.
- Engine: LuaLaTeX với `fontspec` và `unicode-math`.
- Nạp phông OTF từ tài sản repository; không phụ thuộc phông cài riêng của máy.
- Thiếu phông phải báo, không âm thầm dùng phông thay thế.

Ký hiệu toán học ở math mode; tên hàm, biến, đạo hàm phải thống nhất với học liệu. Dùng $f^\prime$, $f^{\prime\prime}$, $\lvert x\rvert$, $\frac{a}{b}$; viết lời giải thích bằng văn bản, không nhồi vào công thức. Trong tài liệu Markdown/QMD dùng dấu dollar cho toán; không dùng `\qquad`.

Cỡ nền nguồn khởi đầu 10 pt: nhãn trục 10 pt, nhãn điểm/đường 9 pt, nhãn vạch chia 8 pt. Không dùng chữ đậm cho toàn bộ nhãn trục và tọa độ. Cỡ này phải được kiểm tra sau co giãn, không chỉ trong nguồn.

### 5.5. Nét, dấu điểm và khung

| Thành phần | Thông số khởi đầu |
| --- | --- |
| Mọi đường cong hàm số ngang hàng | 1,1 pt; màu `zoGraphMain`; phân biệt bằng kiểu nét |
| Trục | 0,8 pt |
| Tiệm cận | Nét đứt, 0,8 pt |
| Tiếp tuyến/đường chiếu | 0,6 pt; chọn nét theo vai trò |
| Lưới chính/phụ | 0,35 / 0,25 pt |
| Vạch chia | 0,45 pt; tổng chiều dài 0,75 mm |
| Điểm thông thường | `mark size=2.2pt` |
| Điểm trọng tâm | `mark size=2.8pt` |
| Điểm phụ | `mark size=1.7pt` |
| Viền minh họa | 0,45 pt, bo góc 2 mm |
| Khoảng đệm trong khung | Khởi đầu 4 mm |
| Lề ngoài tài sản | Khởi đầu 3 pt |

`mark size` là tham số dựng, không gọi nó là đường kính điểm. Marker phải còn nhận ra ở kích thước mobile thực tế. Kiểm tra kích thước dấu sau render; ngoại lệ phải có tên vai trò và lí do.

Nét chính có đầu/nối nét tròn khi phù hợp. Không phát sáng, đổ bóng hoặc gradient trang trí.

## 6. Phân lớp và thứ tự che phủ

### 6.1. Hai khái niệm khác nhau

**Thứ tự lớp** quyết định nét nào vẽ trên nét nào. **Bố trí** quyết định các đối tượng có nên chiếm cùng một vùng hay không. Đưa nhãn lên lớp cao không giải quyết được việc nhãn đang đặt sai.

Bảng sau là mô hình thị giác của ZO Math, không phải danh sách tên lớp dựng sẵn của PGFPlots.

| Lớp, từ dưới lên | Thành phần | Quy tắc |
| --- | --- | --- |
| 0 | Nền và khung trang trí | Không mang ý nghĩa biên toán học |
| 1 | Lưới nếu có | Chỉ phục vụ đọc, không lấn đường chính |
| 2 | Trục và vạch chia | Rõ hơn lưới, nhẹ hơn đường cong |
| 3 | Miền tô, đường phụ và tham chiếu toán học | Không che trục hoặc đặc điểm cần đọc |
| 4 | Các đường cong hàm số | Ngang hàng về màu và độ dày; kiểu nét phân biệt |
| 5 | Marker điểm | Hiển thị trên đường cong và đường phụ |
| 6 | Nền bảo vệ nhãn | Nhỏ, cùng nền cục bộ; không che vùng bảo vệ |
| 7 | Chữ và công thức | Không có nét xuyên ký tự |
| 8 | Chú giải, đoạn dẫn và chú thích ngoài | Không chiếm vùng dữ liệu quan trọng |

Đối với các đường cong ngang hàng, dùng cùng lớp đường cong và kiểm tra mọi giao điểm; thứ tự vẽ không được tạo ra sự nhấn mạnh sai mục đích.

### 6.2. Những vùng không được che

Đánh dấu theo hình cụ thể, ít nhất gồm các vùng liên quan đến nhiệm vụ:

- nghiệm/giao điểm đang cần đọc;
- điểm cực trị, điểm uốn, điểm gãy hoặc chỗ tiếp xúc;
- điểm rỗng/đặc và khoảng tách giữa các nhánh;
- quan hệ đường cong–tiệm cận;
- đầu mũi tên, ký hiệu trục, vạch chia được dùng làm dữ kiện;
- dải hình cần so sánh để phân biệt hai đường gần nhau.

Bảo vệ cả một lân cận hiển thị, không chỉ một tọa độ có diện tích bằng không. Kích thước lân cận phải đủ để thấy đặc điểm: một chỗ tiếp xúc cần bảo vệ cả đường cong và tiếp tuyến quanh nó.

### 6.3. Giao cắt hoặc trùng nét có chủ ý

- Hai đường cắt nhau: giữ giao điểm, không tẩy một đường để tạo cảm giác hai đường không giao.
- Tiếp tuyến tiếp xúc: không che hoặc khoét khoảng trắng tại tiếp điểm.
- Đường cong trùng trục, ví dụ $y=0$: dùng màu/độ dày/nhãn để chỉ rõ đường đang xét; không dịch nó lên vài pixel.
- Tiệm cận trùng một trục: không dịch tiệm cận. Dùng cùng vị trí và chú thích quan hệ; tránh hai nét đứt/liền chồng làm rối.
- Marker điểm nằm trên đường: đây là che phủ có chủ ý; marker được vẽ sau để rõ.
- Điểm rỗng: phải che đúng nét bên dưới lõi, nhưng không tạo thêm một điểm giá trị giả.

### 6.4. Thực thi phân lớp

PGFPlots có cơ chế `set layers`, `on layer`; khi đã bật lớp, thứ tự câu lệnh trong nguồn không nhất thiết là thứ tự hiển thị. Phân lớp phải được cấu hình cho toàn hình và phối hợp với clipping; `clip mode=individual` là một thiết lập cần xem xét khi các plot ở các lớp khác nhau. [S2 — Phân lớp PGFPlots](https://tikz.dev/pgfplots/reference-layers)

Bộ style triển khai phải ánh xạ các vai trò ở bảng 6.1 sang lớp thực thi rõ ràng, kể cả nhãn số tự sinh. Không chỉ đổi thứ tự các `\addplot` rồi mặc nhiên coi toàn hình đã đúng.

## 7. Logic bố trí nhãn và chống chồng lấp

### 7.1. Đơn vị kiểm tra là hộp nhãn, không phải điểm neo

Một nhãn gồm ký tự, dấu tiếng Việt, chỉ số, phân số và khoảng đệm. Phải xét toàn bộ hình chữ nhật bao nhãn sau sắp chữ, thêm vùng an toàn.

Đường không cắt qua điểm neo vẫn có thể gạch xuyên chữ. Hai điểm neo xa nhau vẫn có thể tạo hai nhãn chồng nhau. `outer sep` không tự tạo vùng tô bảo vệ chữ; khoảng đệm bên trong và vùng tránh va chạm là hai việc khác nhau.

TikZ cung cấp điểm neo, dịch chuyển và khoảng đệm của node; chúng là cơ chế bố trí, không tự động bảo đảm nhãn không va chạm. [S3 — Node và nhãn TikZ](https://tikz.dev/tikz-shapes)

### 7.2. Thứ tự ưu tiên giải quyết

Thực hiện theo thứ tự, dừng ở cách đơn giản nhất đã đọc rõ:

1. Bỏ nhãn trùng lặp hoặc không cần thiết; không bỏ dữ kiện bắt buộc.
2. Đổi góc đặt nhãn quanh đối tượng.
3. Dịch nhãn một khoảng nhỏ trong không gian hiển thị.
4. Chọn vị trí khác dọc cùng đường, vẫn nhận diện đúng đối tượng.
5. Dùng nhãn có nền bảo vệ nhỏ nếu đáp ứng Mục 7.5.
6. Đặt một đoạn dẫn ngắn hoặc đưa phần giải thích dài ra chú thích.
7. Điều chỉnh không gian quan sát hoặc tách hình nếu vẫn không thể đọc.

Không giảm hàng loạt cỡ chữ hoặc kéo nhãn rất xa chỉ để giữ mọi chi tiết.

### 7.3. Chọn vị trí quanh một điểm

Thử các góc chéo trước: trên–phải, trên–trái, dưới–phải, dưới–trái; ưu tiên góc có vùng trống thật, không có thứ tự góc cố định áp dụng cho mọi hình.

- Đỉnh cực đại: vùng trên thường đáng thử, nhưng phải kiểm tra biên và đường khác.
- Đáy cực tiểu: vùng dưới thường đáng thử.
- Điểm nằm trên nhánh dốc: thử phía không bị nhánh tiến vào hộp nhãn.
- Điểm nằm trên trục: tránh vùng nhãn vạch chia; dùng tên điểm và tọa độ có chọn lọc.
- Hai điểm gần nhau: phân bố nhãn về hai vùng khác nhau; không xếp thành một chùm chữ.
- Nhãn tọa độ dài: đưa tên ngắn $A$ vào hình, cặp tọa độ vào chú thích nếu điều đó vẫn phục vụ nhiệm vụ.

Đó là các gợi ý ban đầu; kết quả render quyết định vị trí cuối.

### 7.4. Khoảng cách khởi đầu

Đo bằng đơn vị hiển thị, không dùng một độ lệch theo đơn vị trục cho mọi hình.

| Quan hệ | Mức khởi đầu tại kích thước nguồn |
| --- | --- |
| Mép marker đến mép ngoài hộp nhãn | 2–4 pt |
| Mép chữ/nền nhãn đến nét không liên quan | Ít nhất khoảng 2 pt |
| Giữa hai hộp nhãn | Ít nhất khoảng 3 pt |
| Nhãn đến mép trong khung minh họa | Khoảng 2 mm |
| Đầu mũi tên đến khung minh họa | Khoảng 3 mm |
| Đệm ngang nền nhãn | 1,5–2 pt |
| Đệm dọc nền nhãn | 1–1,5 pt |

Các khoảng này không cấp phép che vùng trọng tâm. Nếu hình bị thu nhỏ khiến khoảng hở không còn nhận ra, phải bố trí lại. Dịch 4 pt ở điểm neo không bảo đảm mép nhãn cách marker 4 pt; cần xét kích thước marker và hộp chữ.

### 7.5. Nền bảo vệ nhãn

**Mục tiêu:** chữ sạch, đồng thời người đọc không hiểu sai hình dạng hoặc tính liên tục của đường cong.

Quy tắc bắt buộc:

1. Chọn vị trí không va chạm trước; nền che là lớp bảo vệ, không phải công cụ bù cho bố trí cẩu thả.
2. Nền đặc, màu khớp vùng chứa nhãn. Chữ đặc, không bị giảm opacity theo nền.
3. Không có viền hộp hoặc bóng đổ cho nhãn thông thường.
4. Hộp chỉ bao chữ và đệm nhỏ; không che một vùng lớn hơn cần thiết.
5. Nền và chữ xuất hiện sau các nét mà chúng cần che.
6. Không che marker, giao điểm, điểm gãy, tiếp điểm, vùng phân biệt hai đường hoặc bất kỳ vùng bảo vệ nào.
7. Không dùng nền che để làm đường cong sai trông “đẹp hơn”.
8. Nếu nền đang tô biến thiên/chồng màu hoặc có ranh giới miền đi qua, ưu tiên dời nhãn ra ngoài; không lấy màu nền vàng chung vá thành một ô khác màu.

Trong vùng trống, nền cùng màu được phép tồn tại nhưng phải gần như không nhận ra. Trong vùng có lưới hoặc đường chiếu thứ yếu, nền nhỏ có thể che chúng.

Nếu một đoạn đường cong không trọng tâm đi qua nhãn và không có vị trí tốt hơn, chỉ cho phép che một đoạn ngắn khi quan hệ đường–nhãn vẫn rõ, không tạo cảm giác điểm khuyết/gián đoạn và không giấu thông tin bài toán. Trường hợp này phải được ghi nhận khi duyệt hình; không dùng làm mặc định.

Không dùng quầng chữ dày hoặc viền trắng quanh từng ký tự làm phong cách mặc định. Ưu tiên node nền đặc, không viền, đệm nhỏ.

### 7.6. Nhãn đường cong

Ưu tiên nhãn trực tiếp khi có một hoặc hai đường, công thức ngắn và vùng vẽ đủ thoáng. Đặt gần đường, thường gần phần cuối nhìn thấy nhưng không nằm trên mép cắt. Đường có thể chạm mép nền bảo vệ nhỏ của nhãn, nhưng không được chạy xuyên glyph; nền không được làm đường cong trông đứt hoặc che đặc điểm toán học.

Nhãn công thức mặc định nằm ngang. Nhãn đường thẳng có thể nghiêng nhẹ theo hướng đường khi dễ đọc; không xoay nhãn gần thẳng đứng hoặc lộn ngược. Góc phải theo hướng hiển thị sau tỉ lệ trục, không lấy máy móc từ hệ số góc toán học.

Không đặt công thức sát một đường khác hơn đường nó gọi tên. Không dùng nhãn “$f$” cho hai đường mà người đọc không thể phân biệt.

Dùng hộp chú giải khi có từ ba đường trở lên, công thức dài, nhiều giao cắt hoặc vùng vẽ chật. Mật độ thông tin và mục đích sư phạm được ưu tiên hơn luật đếm máy móc. Hộp dùng nền sáng, viền nhẹ, không bóng; mẫu nét phải khớp chính xác màu, độ dày và kiểu nét của đường tương ứng. Sắp xếp mục theo logic nội dung và không đặt hộp lên vùng toán học quan trọng.

Nhãn trực tiếp và chú giải chỉ khác cơ chế bố trí tên đường; không được làm thay đổi công thức, cửa sổ, kiểu nét hoặc dữ kiện toán học.

### 7.7. Đoạn dẫn và chú giải

Đoạn dẫn là nét mảnh, ngắn, không mũi tên; nó chỉ liên kết nhãn với đối tượng, không phải véc-tơ hay tiếp tuyến.

- Không chạy xuyên nhãn hoặc marker.
- Không cắt đường khác ở vùng nhạy cảm.
- Điểm cuối đặt sát đối tượng nhưng không làm thay đổi hình dạng của nó.
- Nếu cần nhiều đoạn dẫn đan nhau, phải bố trí lại hoặc tách hình.

Chú giải dùng khi nhiều đường/điểm khó gắn nhãn trực tiếp. Mẫu nét và marker phải đúng màu, kích thước, kiểu nét đang vẽ; không dùng ký tự gần giống để giả marker. Vị trí ưu tiên là vùng trống đã kiểm tra, không luôn cố định ở góc trên–phải.

Nếu không có vùng trống, đặt chú giải ngoài miền dữ liệu nhưng trong khung minh họa, hoặc đưa nội dung sang chú thích. Không thu nhỏ toàn bộ hình để nhét một chú giải dài.

### 7.8. Chấm điểm vị trí — hướng dẫn cho công cụ sau này

Một công cụ hỗ trợ bố trí có thể sinh nhiều vị trí rồi đánh giá theo thứ tự ưu tiên:

1. loại mọi vị trí vi phạm vùng bảo vệ hoặc đè một nhãn khác;
2. giảm giao cắt với nét;
3. giảm khoảng cách giữa nhãn và đối tượng;
4. giữ sự nhất quán với các nhãn cùng loại;
5. giảm nhu cầu dùng đoạn dẫn và nền che.

Không cộng các điểm thành một giá trị mà “nhãn gần đẹp hơn” có thể bù việc che mất giao điểm. Điều kiện toán học là ràng buộc cứng.

Khi kiểm tra tự động, dùng tọa độ hiển thị sau biến đổi trục; nới hộp nhãn theo khoảng an toàn; xét cả đường với độ dày thực, marker và nền nhãn. Không tuyên bố có bộ phát hiện va chạm nếu mới chỉ tìm tọa độ node trong mã.

### 7.9. Ma trận xử lí nhanh

| Hiện tượng | Xử lí đúng | Không làm |
| --- | --- | --- |
| Đường gạch qua chữ | Dời nhãn; sau đó cân nhắc nền nhỏ | Để chữ và nét xuyên tự do |
| Nhãn che điểm cực trị | Chuyển nhãn ra khỏi lân cận đỉnh/đáy | Tăng nền che |
| Nhãn nằm trên miền tô | Dời đến vùng nền đồng nhất; kiểm tra màu nền | Vá ô vàng lên mọi nền |
| Hai nhãn quá sát | Đổi phía; rút gọn tên; lược trùng | Giảm chữ toàn hình |
| Điểm rỗng bị nét xuyên | Vẽ marker sau, lõi đặc khớp nền cục bộ | Lõi trong suốt |
| Đồ thị trùng trục | Giữ đúng tọa độ, phân biệt vai trò bằng nét/nhãn | Dịch đồ thị cho “rõ” |
| Chú giải che dữ liệu | Chuyển vùng, đưa ra ngoài miền dữ liệu | Cố giữ góc mặc định |
| Nhãn bị cắt ở biên | Điều chỉnh vị trí/lề/lớp nhãn | Tắt clipping toàn hình |

## 8. Quy tắc từng thành phần

### 8.1. Trục tọa độ

Trục đi qua gốc khi gốc nằm trong cửa sổ và giúp đọc hình. Nếu dùng trục ở biên hoặc miền không chứa gốc, vạch số phải cho thấy đúng hệ tọa độ; không làm người học nhầm cạnh khung là trục $x=0$ hoặc $y=0$.

Giữ quy ước ZO Math về hai đầu mũi tên cho trục tiếp tục theo hai hướng; chỉ đầu dương mang tên trục. Mũi tên trục không biểu diễn tập xác định của hàm. Hàm xác định trên một đoạn vẫn có thể được vẽ trên hệ trục đầy đủ.

Kiểu đầu mũi tên phải đồng nhất và được khóa trong style. Giữ kiểu `<->` của tài liệu nền làm điểm xuất phát; không chuyển sang một kiểu khác chỉ vì nó mới hơn.

Nhãn $x$, $y$ ở gần đầu dương, ngoài đường trục và có khoảng thở. Không gắn cứng mọi nhãn vào cùng một góc cho tất cả hình.

### 8.2. Gốc, vạch và nhãn số

Gốc tọa độ ghi một nhãn $O$ khi cần, không lặp số 0 trên cả hai trục. Trường hợp nhiều gốc hoặc ký hiệu đặc biệt phải được giải thích.

Vạch chia và nhãn có thể khác mật độ. Ưu tiên mốc chính xác như $\pi$, $\frac{1}{2}$; không thay bằng số gần đúng nếu bài đang dùng giá trị chính xác.

Mặc định giữ cách đặt nhãn riêng bằng node đã có trong quy chuẩn nền để xử lí va chạm theo hình. Tọa độ neo phải đúng tọa độ vạch; chỉ dịch hộp nhãn bằng đơn vị hiển thị. Các trường hợp nhiều vạch đều có thể dùng bộ đặt nhãn tự động nếu qua cùng kiểm tra; ngoại lệ này phải được ghi, không tự bỏ cơ chế bố trí đã duyệt.

Không lạm dụng đường chiếu và nhãn số để “đánh dấu hết” mọi điểm nguyên.

### 8.3. Lưới

Mặc định không lưới. Bật lưới khi nhiệm vụ cần đọc tọa độ, khoảng cách, chu kỳ hoặc so sánh độ lớn.

Lưới nhạt chỉ hỗ trợ; nếu một đường lưới mang dữ kiện bắt buộc, nâng nó thành đường tham chiếu rõ ràng. Không đặt nhiệm vụ dựa duy nhất vào một nét tương phản quá thấp.

### 8.4. Đường cong

Mọi đường cong hàm số dùng đỏ ZO Math `#EF5350` và độ dày mặc định 1,1 pt. Với các đường ngang hàng: đường thứ nhất liền, đường thứ hai đứt, đường thứ ba gạch–chấm. Không dùng khác màu hoặc khác độ dày để tạo thứ bậc giả.

Không marker ở mỗi điểm mẫu, không làm trơn qua góc gãy, không nối qua điểm loại hoặc tiệm cận và không tự gắn mũi tên vào mọi đầu nhánh bị cắt. Khi có hơn ba đường, xem lại việc tách hình hoặc giảm tải trước khi thêm mã hóa mới.

### 8.5. Đường phụ theo vai trò toán học

Dựng từ phương trình hoặc kết quả được kiểm tra. Tiếp tuyến phải đi qua điểm tiếp xúc; không ước lượng bằng mắt. Tiệm cận phải xuất phát từ phân tích giới hạn, không chỉ từ đường cong nhìn gần thẳng.

Tiếp tuyến, tiệm cận, đường chiếu và đường tham chiếu có thể dùng nét đứt theo quy ước toán học. Chúng dùng màu cấu trúc trung tính, độ dày và lớp khác đường cong; nhãn phải nói rõ vai trò khi có nguy cơ nhầm.

Nét đứt của đường phụ không được làm người đọc nhầm với đường cong hàm số thứ hai. Khi xung đột, ưu tiên làm rõ bằng nhãn, vị trí, lớp và mẫu dash khác biệt; không đổi đường cong sang màu mới.

### 8.6. Điểm và đầu mút

Điểm đặc/rỗng biểu thị đúng quan hệ thuộc tập hoặc giá trị hàm. Lõi điểm rỗng khớp nền cục bộ, không mặc nhiên dùng trắng trên nền vàng. Trên miền tô, phải xét màu thực tại vị trí điểm.

Hai marker trùng tọa độ không được vẽ đè làm sai nghĩa. Nếu nhiều phần hàm chung đầu mút, quyết định một cách biểu diễn thống nhất theo giá trị hàm thật.

Với khoảng trên trục số, đoạn hữu hạn có đầu mút phù hợp và không có mũi tên “tiếp tục”. Chỉ tia hoặc hướng tiếp tục mới dùng mũi tên. Marker phải thấy rõ ở mobile. Nhãn điểm đặt cách marker khoảng 2–3 mm theo không gian hiển thị rồi tinh chỉnh theo hộp chữ; không để đường chạy xuyên glyph.

### 8.7. Đường chiếu tọa độ

Chỉ chiếu những tọa độ phục vụ nhiệm vụ. Nếu điểm được dùng để đọc cặp tọa độ, mặc định chiếu tới hai trục; bỏ nhánh chiếu có độ dài bằng không hoặc không được nhiệm vụ yêu cầu.

Đường chiếu không kéo xuyên toàn hình, không có mũi tên; kết thúc tại tâm điểm và được marker vẽ sau che đầu nét. Không tạo hai nhãn khác nhau cho cùng một vạch ở chân chiếu.

### 8.8. Miền tô

Miền tô nằm dưới các đường biên cần đọc. Tránh polygon có cạnh phụ tự sinh khiến người học tưởng là ranh giới toán học.

Không dùng độ trong suốt chồng nhiều lần làm thay đổi nghĩa màu. Nếu có nhiều miền giao nhau, dùng mẫu nét hoặc tách hình khi màu không đủ rõ. Biên bắt buộc phải đọc được ngay cả khi miền tô rất nhạt.

## 9. Kích thước, tỉ lệ và hiển thị nhỏ

### 9.1. Kích thước nguồn

Giữ các khuôn khởi đầu của tài liệu nền:

| Khuôn | Kích thước miền trục dự kiến |
| --- | --- |
| Thông thường | 12 × 7,5 cm |
| Vuông | 9 × 9 cm |
| Ngang rộng | 14 × 7 cm |
| Đứng | 9 × 11 cm |

Với `scale only axis`, kích thước miền trục không phải kích thước toàn tài sản: còn nhãn, khung và đệm. Phải đo bounding box cuối, không tuyên bố ảnh rộng 12 cm chỉ từ `width=12cm`.

Khuôn vuông và tỉ lệ đơn vị bằng nhau là hai yêu cầu khác nhau. Khi miền hai trục không tương ứng, không thể mặc nhiên có cả khung vuông, giới hạn cố định và cùng tỉ lệ đơn vị. Ưu tiên tính đúng, ghi rõ quyết định.

### 9.2. Tỉ lệ trục

Không bắt mọi đồ thị phải có tỉ lệ đơn vị 1:1. Nhưng khi hình dùng để đọc góc, khoảng cách, đường tròn, phép đối xứng qua $y=x$ hoặc hình dạng Euclid, phải dùng tỉ lệ phù hợp.

Độ dốc nhìn thấy phụ thuộc tỉ lệ hai trục. Không suy từ góc trên màn hình ra giá trị đạo hàm khi không có tỉ lệ đơn vị bằng nhau.

### 9.3. Không thu nhỏ đến mức chữ chỉ còn “đúng hình thức”

SVG co giãn không đồng nghĩa dễ đọc. Định mức nội bộ v0.1 để thử:

- bản in: chữ mang thông tin không nhỏ hơn tương đương 8 pt tại kích thước đặt thật;
- web: nhãn chính mục tiêu khoảng 12 CSS px trở lên tại khung nội dung nhỏ; nhãn phụ dưới khoảng 11 CSS px phải được xem là cảnh báo cần xử lí.

Đây là ngưỡng thiết kế nội bộ, không phải chuẩn WCAG về cỡ chữ. Công thức nhiều tầng có thể cần lớn hơn.

Nếu ảnh nguồn rộng $W$ được hiển thị ở chiều rộng $w$, mọi chữ và nét trong ảnh cùng bị nhân gần đúng với $w/W$. Cần tính theo toàn tài sản, không chỉ miền trục.

Nếu khuôn 12 cm không đọc được ở mobile, dựng bố cục nhỏ gọn từ cùng dữ liệu: bớt nhãn phụ, chuyển chú thích ra ngoài, tăng cỡ chữ tương đối hoặc chia hình. Không chỉ ép CSS thu nhỏ. Chỉ tạo biến thể nhỏ khi phép thử chứng minh cần; không nhân đôi mọi tài sản mặc định.

### 9.4. Clipping và bounding box

Cắt đường cong theo cửa sổ quan sát, giữ nhãn trong vùng đã bố trí. Khung trang trí không phải đường cắt dữ liệu.

`clip=true`, `clip mode=individual`, `enlargelimits=false` là cấu hình khởi đầu cần kiểm chứng cùng lớp. Không tắt clipping toàn trục để cứu một nhãn. PGFPlots phân biệt phạm vi cắt và hộp bao ảnh; thay một thứ không mặc nhiên sửa thứ còn lại. [S4 — Hộp bao và clipping](https://tikz.dev/pgfplots/reference-bb-clip)

Không dùng bounding box giả để cắt mất nội dung. Kiểm tra cả đầu mũi tên, dấu tiếng Việt, nhãn nghiêng và khung sau chuyển SVG.

Lưu ý kỹ thuật: trong chế độ `individual`, các lệnh vẽ tùy biến như `\draw` không được mặc nhiên coi là đã cắt như `\addplot`; phần hình cần cắt phải có scope cắt thích hợp. Nhãn được phép ra ngoài miền trục vẫn phải nằm trong khung ảnh. [S4 — Hộp bao và clipping](https://tikz.dev/pgfplots/reference-bb-clip)

## 10. Hồ sơ kỹ thuật và tên tệp

### 10.1. Môi trường

Bộ dựng dùng LuaLaTeX, STIX Two Text/Math và TikZ/PGFPlots. Mức `compat=1.18` là cơ sở từ tài liệu nền, không phải tuyên bố đây là phiên bản thư viện cài đặt. Ghi lại phiên bản engine và gói thực tế khi khóa mẫu.

Lượng giác cần thống nhất đơn vị góc. Không chép một biểu thức Python dùng radian vào PGFPlots mà không kiểm tra cách tính góc của môi trường đang dùng.

Với bộ tính PGF ở chế độ góc mặc định theo độ, biểu thức `sin(deg(x))` diễn đạt sin của biến x tính bằng radian. Không dùng phép chuyển này lần nữa nếu môi trường đã cấu hình radian. Không đổi chế độ lượng giác toàn cục chỉ cho một đường mà không kiểm tra tác động lên các lệnh dựng khác. [S10 — Biểu thức toán học PGF](https://tikz.dev/math-parsing)

Đường dẫn font/style/dữ liệu phải tương đối với cấu trúc thực hoặc do launcher chuẩn giải quyết. Không đóng cứng số cấp `../` của dự án 100+ vào mọi gói mới.

### 10.2. Đặt tên và nơi lưu

Tận dụng nơi lưu hình, script và tài sản đã có trong repository. Không tự tái cấu trúc dự án.

Tên hình ổn định, không dấu, diễn đạt chức năng, ví dụ `tiep_tuyen_ngang_khong_cuc_tri`. Các thành phẩm cùng gốc tên. Nhãn HTML/Quarto dùng ID ổn định, không phụ thuộc số thứ tự trang.

Tên style thể hiện vai trò, ví dụ `zo graph main`, `zo point label`; không dùng `style1` hoặc tên dựa trên một ngoại lệ tạm.

Khi triển khai mới cần xác định riêng namespace/phiên bản để không định nghĩa lại tài sản chung của dự án cũ. Không giả định các tên trong tài liệu đã được khai báo.

### 10.3. Nguồn TeX tối thiểu phải có

1. Metadata hình và mục đích.
2. Lớp standalone, engine và font.
3. Nạp style đã chỉ rõ phiên bản.
4. Tham số, công thức hoặc tham chiếu dữ liệu.
5. Cửa sổ, tỉ lệ, vạch chia.
6. Các đối tượng theo vai trò/lớp.
7. Marker và nhãn với vị trí cục bộ.
8. Chú thích ngoại lệ hoặc giới hạn biểu diễn.

Không nhúng lời giải bài học dài vào hình. Không giấu công thức sau nhiều lớp macro khó kiểm.

## 11. PDF, SVG và tích hợp Quarto

### 11.1. Chuỗi dựng chuẩn

Nguồn TeX, style, phông và dữ liệu được đưa qua LuaLaTeX để tạo PDF vector; SVG được chuyển từ chính PDF ấy; hai tài sản được dùng cho đầu ra tương ứng.

PDF là thành phẩm chuẩn để đưa vào tài liệu in, không chỉ là tệp trung gian có thể bỏ. SVG là thành phẩm web. PNG chỉ dùng cho đối chiếu/raster tạm hoặc tình huống có lí do, không thay đầu ra vector mặc định.

### 11.2. Chuyển SVG

Ưu tiên dùng bộ chuyển đổi đã được xác lập trong repository nếu nó đáp ứng tiêu chí. Nếu chưa có, dvisvgm ở chế độ PDF là ứng viên triển khai cần thử; tài liệu chính thức mô tả khả năng đọc PDF và chuyển glyph thành path. Không coi một lệnh chưa chạy trên môi trường ZO Math là pipeline đã nghiệm thu. [S5 — Hướng dẫn dvisvgm](https://dvisvgm.de/Manpage/)

Để ổn định diện mạo, mặc định thiết kế đầu ra SVG có glyph toán/chữ chuyển thành path. Điều đó giữ hình chữ, nhưng làm mất khả năng chọn/tìm/đọc văn bản nội tại như chữ sống; phải bù bằng mô tả ngữ nghĩa trong học liệu. Không gọi SVG path là “văn bản truy cập được”.

SVG phải có kích thước/viewBox đúng, không tài nguyên font hoặc ảnh từ máy cá nhân, không mã thực thi không cần thiết. Không sửa path thủ công sau chuyển đổi.

### 11.3. Chọn đúng định dạng trong Quarto

HTML dùng SVG; PDF dùng PDF vector. Không dựa vào giả định Quarto tự chọn SVG khi bỏ đuôi tệp. Quarto có cấu hình `default-image-extension` theo định dạng và thuộc tính `fig-alt`; cấu hình phải giới hạn trong phạm vi thích hợp để không đổi cách xử lí hình của dự án khác. [S6 — Hình trong Quarto](https://quarto.org/docs/authoring/figures.html)

Nếu pipeline hiện hành đã ánh xạ tài sản bằng adapter/filter thì tích hợp vào cơ chế ấy, không tạo một cách thứ hai chỉ cho một hình.

### 11.4. Chú thích và nội dung thay thế

Chú thích, ID hình và mô tả dài thuộc QMD hoặc nguồn nội dung có thẩm quyền. Không vẽ số “Hình 01” bên trong SVG rồi lại đánh số ở Quarto.

- `alt`: mô tả ngắn đối tượng và cấu trúc quan trọng.
- Chú thích: gắn hình với nhiệm vụ hoặc lập luận.
- Mô tả dài/văn bản lân cận: cung cấp quan hệ toán học mà hình phức tạp truyền đạt.

Hình phức tạp có thể cần mô tả dài ngoài văn bản thay thế ngắn. [S9 — Mô tả hình phức tạp](https://www.w3.org/WAI/tutorials/images/complex/)

Đối với hình trong đề kiểm tra, mô tả phải giữ dữ kiện và mục tiêu bài, không vô tình cung cấp kết luận mà học sinh phải tìm. Khả năng tiếp cận không được coi là phụ lục chỉ thêm sau khi xuất bản.

### 11.5. Tính tương đương

PDF và SVG phải thống nhất công thức, nhánh, điểm, nhãn, màu, kiểu nét, thứ tự lớp và cửa sổ. Không đòi hai ảnh raster từ hai bộ render phải trùng từng pixel; khác khử răng cưa không đồng nghĩa sai hình.

Sai khác hình học, mất dấu, đổi phông, mất marker hoặc cắt nhãn là lỗi phải sửa. Khi có hai bố cục lớn/nhỏ, so sánh về nghĩa và dữ kiện, không yêu cầu tọa độ nhãn giống nhau.

## 12. Quy trình sản xuất theo hai nhịp

### 12.1. Trước khi sửa

- Xác nhận nguồn, phạm vi và hình mục tiêu.
- Ghi nhận thay đổi đang có; không ghi đè tệp của người dùng.
- Xác định có preview/watch đang chạy hay không trước khi sửa cấu hình ảnh hưởng dựng.
- Với nguồn R1-G01 còn đang thẩm định, dùng mirror hoặc vùng kiểm chứng hiện hành.
- Không chạy render toàn kho chỉ để thử một nhãn.

Việc kiểm tra một launcher hoặc đường dẫn cần cho hình mới không phải yêu cầu kiểm kê/di chuyển toàn bộ tài liệu cũ.

### 12.2. Nhịp 1 — dựng mẫu và sửa nhanh

1. Chốt mục đích sư phạm và điều người học phải nhận ra.
2. Khóa công thức, miền, nhánh, điểm và các quan hệ toán học.
3. Chọn cửa sổ quan sát và tỉ lệ trục.
4. Đánh dấu giao điểm, tiếp điểm, cực trị, đầu mút và các vùng bảo vệ.
5. Chọn nhãn trực tiếp hoặc hộp chú giải theo Mục 7.6.
6. Đặt đường cong, đường phụ, marker và nhãn theo đúng lớp.
7. Dịch vị trí để giải quyết va chạm trước; chỉ thêm nền bảo vệ nhỏ sau khi vị trí hợp lí.
8. Biên dịch PDF vector, chuyển SVG và kiểm tra các bất biến toán học.
9. Xem ở kích thước dùng thật trên desktop/mobile và bản in đen trắng.
10. Ghi rõ điều đã kiểm bằng công cụ, điều đã xem bằng mắt và điều còn chờ duyệt.

Không được bỏ kiểm tra: đúng công thức/nhánh/điểm, không nối sai hoặc tạo đặc điểm giả, không che vùng bảo vệ, không nét xuyên chữ, không cắt marker/nhãn/mũi tên và PDF–SVG tương đương.

### 12.3. Nhịp 2 — khóa mẫu/công cụ

Sau khi bố cục mẫu được chấp thuận:

1. Chạy bộ kiểm thử trong Mục 14 theo phạm vi thay đổi.
2. Kiểm tra PDF/SVG/HTML ở kích thước quy định.
3. Kiểm tra bản in đen trắng và tương phản các nét quan trọng.
4. Chạy hồi quy các hình dùng bản style mới; không dựng lại tài sản cũ không liên quan.
5. Ghi phiên bản, phụ thuộc, lệnh dựng và bằng chứng.
6. Chỉ tạo kế hoạch thay hình R1-G01 sau khi mẫu và công cụ đã đạt.

Thay style chung tác động rộng phải kiểm cả bộ mẫu. Sửa vị trí một nhãn cục bộ chỉ cần kiểm hình ấy và nơi dùng liên quan, trừ khi có thay đổi công cụ chung.

### 12.4. Không gộp kiểm chứng với phê duyệt

Ba trạng thái độc lập:

| Trạng thái | Ý nghĩa |
| --- | --- |
| Kỹ thuật đạt | Dựng đúng, tài sản hợp lệ, không phát hiện lỗi kỹ thuật trong phạm vi kiểm |
| Toán học và biên tập đạt | Dữ kiện đúng và phục vụ mục tiêu |
| Chủ dự án duyệt thị giác | Người dùng chấp nhận diện mạo mẫu |

Người dùng nói “nút hoạt động” hoặc “không tràn” không có nghĩa đã duyệt phong cách. Công cụ không chạy được phải ghi “chưa kiểm chứng”, không suy thành đạt.

## 13. Kiểm chứng và điều kiện nghiệm thu

### 13.1. Bảng kiểm bắt buộc

| Mã | Điều kiện | Bằng chứng tối thiểu |
| --- | --- | --- |
| M01 | Công thức, tham số, tập xác định khớp đặc tả | Đối chiếu nguồn và tính toán |
| M02 | Không nối nhầm nhánh | Kiểm nguồn và xem render |
| M03 | Điểm đặc/rỗng, đầu mút, điểm gãy đúng | Kiểm tọa độ và hình |
| M04 | Tiếp tuyến, tiệm cận, miền tô đúng | Tính độc lập các quan hệ |
| M05 | Lấy mẫu không tạo đặc điểm giả | Phân tích hàm và thử tăng/đổi phân bố mẫu |
| V01 | Đối tượng chính nhận ra ngay | Xem ở kích thước dùng thật |
| V02 | Không nét chạy xuyên chữ | Kiểm hộp nhãn và ảnh render |
| V03 | Nền nhãn không che vùng bảo vệ | Đối chiếu vùng trọng tâm |
| V04 | Marker, vạch, mũi tên không bị cắt | Xem mép và vùng dày |
| V05 | Màu/phông/nét nhất quán | Đối chiếu style và ảnh |
| V06 | Chữ/nét đọc được ở bản nhỏ | Desktop 1440 và mobile 430/390 CSS px |
| V07 | In đen trắng vẫn phân biệt đối tượng | Bản kiểm grayscale |
| V08 | Các đường cong chỉ dùng đỏ ZO Math, cùng 1,1 pt và đúng thứ tự liền/đứt/gạch–chấm | Đối chiếu nguồn, SVG và bản grayscale |
| V09 | Nhãn trực tiếp hoặc mẫu nét chú giải gọi đúng đường; không cắt chữ, không nét xuyên glyph | Kiểm nguồn và ảnh ở kích thước dùng thật |
| V10 | Đường phụ toán học không bị nhầm với đường cong nét đứt | Xem vai trò, nhãn, lớp và mẫu dash |
| T01 | Dựng không có lỗi/thiếu font/style | Log và mã thoát |
| T02 | PDF vector/SVG đúng hộp bao | Kiểm tài sản |
| T03 | PDF và SVG tương đương | Đối chiếu hai bản |
| T04 | Không phụ thuộc máy cá nhân/tài nguyên ngoài không khai báo | Kiểm đường dẫn và phụ thuộc |
| T05 | Có khả năng tái sinh | Nguồn, môi trường, style và dữ liệu xác định |
| A01 | Alt/chú thích/mô tả đủ nghĩa | Kiểm HTML đã dựng |
| A02 | Không lộ lời giải qua mô tả hình kiểm tra | Đối chiếu mục tiêu sư phạm |
| G01 | Không sửa ngoài phạm vi | Diff và danh sách tệp |
| G02 | Phê duyệt thị giác được ghi riêng | Xác nhận của chủ dự án |

Không được dùng một kết quả “PASS” tổng hợp để giấu hạng mục chưa làm. Chưa có ảnh kiểm grayscale không được ghi V07 đạt.

### 13.2. Mức độ lỗi

- **Chặn nghiệm thu:** sai nghĩa toán học, che điểm quan trọng, nối nhầm nhánh, mất chữ/điểm, không đọc được ở kích thước dùng, phụ thuộc thiếu khiến không tái sinh.
- **Cần sửa trước khóa:** nhãn sát, marker thiếu cân đối, bảng chú giải nặng, khoảng trắng bất hợp lí.
- **Cảnh báo môi trường:** chỉ được giữ nếu xác định phạm vi ảnh hưởng, có bằng chứng đầu ra không lỗi và người phụ trách biết. Không bỏ qua cảnh báo phông bằng cách nhìn thấy PDF vẫn mở.

### 13.3. Hồ sơ gọn

Mỗi mẫu khóa cần: mã hình, phiên bản đặc tả/style, phụ thuộc và hash cần thiết, lệnh hoặc launcher thực dùng, các bất biến toán học, ảnh kiểm tiêu biểu, danh sách ngoại lệ và trạng thái phê duyệt.

Tận dụng hồ sơ/receipt của repository nếu đã có; không tạo hệ điều hành dự án mới cho bộ đồ thị. Hash thay đổi cho biết cần xem lại phụ thuộc, không tự chứng minh nội dung toán học đã đổi hoặc vẫn đúng.

## 14. Bộ bảy mẫu nghiệm thu

| Mẫu | Điều kiện toán học và thị giác trọng tâm |
| --- | --- |
| T01 — $y=x^2$ | Đỉnh $O$, đối xứng, đường trơn; nhãn gốc không đè đỉnh; thử điểm tọa độ và đường chiếu |
| T02 — $y=\frac{1}{x}$ | Hai nhánh tách tại 0; hai trục là tiệm cận; không có đoạn đứng nối nhánh; nhãn trục tránh nhánh gần trục |
| T03 — $y=\lvert x\rvert$ | Góc gãy ở $O$; không làm trơn; hai nhánh nối đúng; nền nhãn không che góc |
| T04 — $y=\sin x$ | Nhãn chính xác theo $\pi$; kiểm đơn vị góc; các cực trị và nghiệm; không lặp nhãn 0 |
| T05 — $y=\sin(1/x)$ | Miền loại 0; lấy mẫu theo pha có kiểm soát; ngưỡng dừng được khai báo; không tô đặc để giả đầy đủ dao động |
| T06 — Hàm từng phần ở dưới | Điểm khuyết, giá trị gán riêng, gián đoạn và chồng nhãn |
| T07 — $y=(x-1)^3+2$ trong R1-G01 | Điểm $(1;2)$, tiếp tuyến $y=2$; hàm đồng biến ở hai phía, không cực trị tại 1; thử phân lớp và nhãn trọng tâm |

Mẫu T06 dùng:

$$
f(x)=
\begin{cases}
x+1, & x<0,\\
2, & x=0,\\
x^2, & x>0.
\end{cases}
$$

Phải có điểm rỗng $(0;1)$, điểm rỗng $(0;0)$ và điểm đặc $(0;2)$. Không có đoạn thẳng đứng nối chúng. Nhãn gốc và điểm rỗng tại gốc cần được bố trí riêng, không “giải quyết” bằng cách dời điểm.

Trong bộ bảy mẫu phải phủ thêm các tình huống bố trí sau bằng trường hợp kiểm kèm, không nhất thiết tạo thêm bảy tài sản sản xuất:

- nhãn dài với phân số/chỉ số;
- nhãn nằm cạnh đường dốc;
- nền nhãn trên lưới và bên cạnh miền tô;
- hai đường giao nhau và nhãn gần giao;
- chú giải không còn vùng trống;
- một đường trùng trục;
- kiểm biên mũi tên và cắt nhãn.

Bộ bảy mẫu là mức nền, không chứng minh công cụ xử lí mọi hàm số. Mỗi dạng mới chưa có đại diện phải thêm phép thử tương ứng trước khi dùng trong học liệu.

## 15. Mẫu thử đầu tiên của R1-G01

Chọn T07, vì chính hình này giúp kiểm cả diện mạo hiện được người dùng ưa thích lẫn logic bố trí mới.

Dữ kiện cố định:

$$
f(x)=(x-1)^3+2,\quad f^\prime(x)=3(x-1)^2,\quad f(1)=2,\quad f^\prime(1)=0.
$$

Tiếp tuyến tại $A(1;2)$ là $y=2$. Từ $f^\prime(x)>0$ với mọi $x\ne1$, cùng tính liên tục tại 1 và tính đồng biến ở hai phía, có thể kết luận hàm đồng biến trên $\mathbb{R}$; cũng có thể dùng tính đồng biến của hàm lập phương để đối chiếu. Không đánh dấu A là cực trị.

Yêu cầu thử:

1. Giữ công thức, điểm và mục đích của hình hiện hành.
2. Lần dựng đầu dùng cửa sổ quan sát của nguồn hình hiện tại nếu truy cập được; không suy tọa độ chính xác từ ảnh chụp.
3. Nền vàng nhạt, đường đỏ, trục xám ấm và STIX.
4. Nhãn A hoặc $(1;2)$ nằm gần điểm nhưng không che tiếp điểm và lân cận tiếp xúc.
5. Nền nhãn đúng màu, đệm nhỏ; tiếp tuyến không xuyên chữ.
6. Kiểm nhãn đường cong và tiếp tuyến; thử nhãn trực tiếp trước chú giải.
7. Nếu đọc cặp tọa độ là mục tiêu, bổ sung đường chiếu cần thiết, phân biệt với tiếp tuyến $y=2$.
8. Dựng PDF/SVG và nhúng vào trang thử đúng phạm vi; không thay thành phẩm R1-G01 đã có.
9. Đối chiếu với bản Matplotlib: so nghĩa toán học, khả năng đọc, nhận diện và chi phí sản xuất; không yêu cầu trùng pixel.
10. Ghi riêng điều người dùng đã duyệt và điều còn cần chỉnh.

## 16. Quản trị phiên bản và chuyển tiếp

Phiên bản 0.2 là quy chuẩn mới cho sản phẩm đồ thị tương lai, được chính thức hóa từ toàn văn v0.1 và các mẫu thị giác đã duyệt. Nó không chứng nhận rằng style dùng chung, bộ sinh mã hoặc toàn bộ bảy mẫu đã được chuyển đổi và kiểm thử.

Lộ trình:

1. Duyệt nội dung quy chuẩn, đặc biệt Mục 6–9.
2. Hiện thực style và pipeline tối thiểu cho mẫu T07.
3. Duyệt mẫu, phản hồi các quy tắc chưa hợp thực tế vào quy chuẩn.
4. Hoàn thiện bộ mẫu và khóa bản đủ điều kiện 1.0.
5. Áp dụng có kiểm soát cho các hình R1-G01 được giao.
6. Biên soạn quy chuẩn bảng biến thiên từ lớp phong cách đã được kiểm nghiệm.

Không buộc phải hoàn thành mọi chuyển đổi cũ để bắt đầu hình mới. Không dùng bản mới để xóa tài liệu cũ chưa được rà soát khi đến lượt bảo trì.

## 17. Ranh giới với quy chuẩn bảng biến thiên

Quy chuẩn bảng biến thiên sẽ kế thừa màu, STIX, phân cấp nét, cách xử lí nền và khoảng thở. Nó phải có mô hình dữ liệu riêng cho mốc, dấu đạo hàm, giới hạn một phía, giá trị hàm, điểm không xác định và chiều biến thiên.

Theo kiến trúc đã duyệt, tkz-tab phục vụ PDF; HTML có cách biểu diễn ngữ nghĩa từ cùng dữ liệu. “HTML ngữ nghĩa” không có nghĩa rút một bảng biến thiên thành bảng chữ phẳng mất vị trí cao/thấp và mũi tên.

Không sao chép máy móc tất cả màu đồ thị vào mọi hàng/cột. Các ký hiệu $x$, $f^\prime(x)$, $f(x)$ phải là toán, không dùng phông tiêu đề đậm thô để thay thế. Màu đỏ không mặc nhiên gắn với dấu âm hoặc nghịch biến.

Phần này chỉ xác lập điểm nối, chưa phải toàn văn quy chuẩn bảng biến thiên và chưa giao xây renderer của nó.

## 18. Phụ lục A — Phiếu giao việc cho một đồ thị

~~~yaml
figure_id: tiep_tuyen_ngang_khong_cuc_tri
role: explanation
purpose: "Nhận ra tiếp tuyến ngang không đủ để kết luận có cực trị."
math:
  expression: "(x-1)^3+2"
  domain: "R"
  exact_point: ["1", "2"]
  tangent: "y=2"
  excluded_points: []
rendering:
  primary: "TikZ/PGFPlots"
  computation: "Không cần dữ liệu số ngoài cho mẫu này."
  viewport: "Chốt từ nguồn hình hiện có khi triển khai."
  protected_regions:
    - "Lân cận tiếp xúc tại (1;2)"
  label_policy: "Dời nhãn trước; không che vùng tiếp xúc."
outputs:
  - pdf
  - svg
governance:
  standard_version: "0.2"
  style_version: "Ghi bản thực tế khi triển khai."
  status: "Bố cục nguyên tắc đã được kiểm chứng; sản phẩm cụ thể vẫn cần nghiệm thu."
~~~

Đây là minh họa trường thông tin, chưa phải schema để đưa thẳng vào một bộ sinh mã. Trường diễn giải phải được chuyển thành giá trị hợp lệ trước khi tự động hóa. Không tạo thêm YAML riêng nếu cùng thông tin đã có trong hồ sơ chuẩn của hình.

## 19. Phụ lục B — Minh họa node nhãn có nền

Đoạn dưới minh họa cơ chế, không phải bộ style đã triển khai hoặc tệp TeX hoàn chỉnh. Phông, các màu và môi trường axis phải được khai báo trước. Vị trí cụ thể phải kiểm tra trên hình thật.

~~~tex
% Place after curves and point markers, on the label layer.
% Keep the protected neighborhood of (1,2) unobscured.
\node[
  anchor=north west,
  xshift=5pt,
  yshift=-5pt,
  font=\small,
  text=zoText,
  fill=zoPlotBackground,
  fill opacity=1,
  text opacity=1,
  draw=none,
  inner xsep=1.8pt,
  inner ysep=1.2pt,
  outer sep=0pt
] at (axis cs:1,2) {$A(1;2)$};
~~~

Đoạn mã dùng các khóa node của TikZ. [S3 — Node và nhãn TikZ](https://tikz.dev/tikz-shapes) Nó không tự kiểm tra va chạm; nếu điểm và nhãn đang ở vùng tô khác màu thì không dùng nguyên nền trên. Một điểm neo đúng chưa đảm bảo hộp nhãn đúng.

Không đặt câu lệnh này vào style toàn cục với tọa độ cố định; chỉ hình cụ thể mới sở hữu vị trí nhãn. Bộ style dùng chung giữ màu, đệm và phông; nguồn hình giữ điểm neo và dịch chuyển.

## 20. Phụ lục C — Đối chiếu ma trận đã duyệt

| Hạng mục ma trận | Phần thực hiện trong bản này |
| --- | --- |
| DT-01–02: mục đích, đối tượng | Mục 1–2 |
| DT-03–04, DT-32: nguồn style và khả năng tái tạo | Mục 3, 10, 16 |
| DT-05–10: toán học, phương pháp, dữ liệu | Mục 4 |
| DT-11: phân lớp | Mục 6 |
| DT-12–14: nền, palette, màu | Mục 5 |
| DT-15–17: trục, nhãn trục, lưới | Mục 7–8 |
| DT-18–24: đường, điểm, miền tô, chú giải | Mục 5–8 |
| DT-25–27: kích thước, tỉ lệ, cửa sổ/cắt biên | Mục 4, 9 |
| DT-28: lấy mẫu | Mục 4.5, 13–14 |
| DT-29, DT-33: cấu trúc nguồn và tên | Mục 3, 10 |
| DT-30–31: phông và engine | Mục 5.4, 10 |
| DT-34–37: dựng và kiểm chứng | Mục 11–13 |
| DT-38: bộ mẫu | Mục 14–15 |
| DT-39: phiếu giao việc | Mục 18–19 |
| DT-40: trạng thái và khóa bản | Mục 1.3, 12.4, 16 |
| Bổ sung của chủ dự án: logic bố trí | Mục 6–7, ràng buộc Mục 9, phép thử Mục 13–15 |
| Lớp phong cách cho bảng biến thiên | Mục 5, 17 |

## 21. Nguồn đối chiếu và giới hạn kiểm chứng của tài liệu

### 21.1. Tài liệu nội bộ

- Toàn văn Quy chuẩn sản xuất đồ thị hàm số ZO Math v0.1, được giữ làm nền và không bị ghi đè.
- Quy chuẩn sinh đồ thị hàm số TikZ/PGFPlots dành cho AI, phiên bản 02; khối style phiên bản 05. Nguồn kế thừa palette, STIX, các mức nét, điểm, khuôn và quy tắc toán học.
- Ma trận biên tập Quy chuẩn sản xuất đồ thị hàm số ZO Math v0.1, được chủ dự án phê duyệt trong phiên làm việc.
- Yêu cầu bổ sung của chủ dự án: chủ động thiết kế logic lớp, nền bảo vệ nhãn, chống chồng lấp; không yêu cầu người dùng tự làm chuyên gia bố trí.
- Mẫu audit v0.2 kiểm chứng trục, vạch chia, marker, khoảng nhãn điểm và hai cơ chế nhãn; mẫu audit v0.3.2 kiểm chứng ba đường cùng đỏ ZO Math, cùng 1,1 pt và phân biệt bằng liền/đứt/gạch–chấm.

Các nguồn `_audit/` là bằng chứng thiết kế tại thời điểm ban hành, không phải phụ thuộc chạy. Sản phẩm mới phải tự chứa hoặc tham chiếu style chính thức có phiên bản.

### 21.2. Tài liệu kỹ thuật đối chiếu ngày 21/09/2026

- **[S1]** [PGF/TikZ — Guidelines on Graphics](https://tikz.dev/guidelines): thông điệp hình, nhất quán, nhãn và quan hệ hình–văn bản.
- **[S2]** [PGFPlots — Layers](https://tikz.dev/pgfplots/reference-layers): cơ chế lớp, thứ tự và quan hệ với clipping.
- **[S3]** [PGF/TikZ — Nodes and Edges](https://tikz.dev/tikz-shapes): anchor, padding, màu nền và chữ của node.
- **[S4]** [PGFPlots — Bounding Box and Clipping](https://tikz.dev/pgfplots/reference-bb-clip): phạm vi cắt và hộp bao.
- **[S5]** [dvisvgm — Manual Page](https://dvisvgm.de/Manpage/): PDF đầu vào và lựa chọn glyph/path khi chuyển SVG.
- **[S6]** [Quarto — Figures](https://quarto.org/docs/authoring/figures.html): alt, chú thích, ID và tài sản theo định dạng.
- **[S7]** [W3C — Understanding Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html): mốc tương phản thành phần đồ họa.
- **[S8]** [W3C — Understanding Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html): mốc tương phản chữ.
- **[S9]** [W3C — Complex Images](https://www.w3.org/WAI/tutorials/images/complex/): mô tả ngắn và mô tả dài cho hình phức tạp.
- **[S10]** [PGF/TikZ — Mathematical Expressions](https://tikz.dev/math-parsing): đơn vị góc, chuyển độ/radian và phạm vi cấu hình lượng giác.

Các trang tikz.dev là bản HTML của manual PGF/TikZ và PGFPlots, có liên kết bản PDF và dự án nguồn. Chúng được dùng để đối chiếu cơ chế kỹ thuật, không làm bằng chứng các giá trị khoảng cách do ZO Math đề xuất là tối ưu thực nghiệm.

### 21.3. Điều đã và chưa làm

Đã giữ toàn bộ phạm vi nội dung của v0.1 và hợp nhất các quyết định đã qua thử nghiệm: toolchain TikZ/PGFPlots–LuaLaTeX–STIX, PDF/SVG, hệ một màu đỏ với ba kiểu nét, hai cơ chế nhãn và các thông số hình học đã duyệt.

Chưa xây hoặc sửa style dùng chung; chưa chuyển đổi R1-G01 hay dự án 100+ Hàm số; chưa kiểm toàn bộ bộ bảy mẫu bằng v0.2; chưa xây tự động kiểm va chạm. Đây là các nhiệm vụ triển khai hoặc migration riêng.

Không sửa tệp cũ, không đổi cấu trúc repository, không thay hình/PDF R1-G01, không chuyển nguồn có thẩm quyền và không xuất bản.

## 22. Đối chiếu v0.1 → v0.2

| Phân loại | Quyết định |
| --- | --- |
| Giữ nguyên | Ưu tiên tính đúng; đặc tả toán học; bảo vệ vùng trọng tâm; PDF/SVG tương đương; quy trình hai nhịp; bảng kiểm và bảy mẫu nền |
| Làm rõ | TikZ/PGFPlots là bộ dựng chính; LuaLaTeX và STIX là toolchain chuẩn; Python chỉ hỗ trợ tính; audit là bằng chứng chứ không là phụ thuộc chạy; v0.2 áp dụng cho sản phẩm mới |
| Thay đổi | Mọi đường cong ngang hàng cùng đỏ ZO Math và 1,1 pt; phân biệt liền/đứt/gạch–chấm; không dùng đường cong phụ khác màu; trục 0,8 pt, vạch 0,75 mm và 0,45 pt |
| Bổ sung | Tiêu chí chọn nhãn trực tiếp/chú giải; mẫu nét chú giải phải khớp; khoảng nhãn điểm 2–3 mm; thứ tự lớp mới; quy trình bố trí 10 bước; xử lí xung đột nét đứt |
| Còn mở | Hiện thực style v0.2; migration có kiểm soát; kiểm đủ bảy mẫu; tự động hóa kiểm hộp nhãn và hồi quy thị giác |

**Điểm bàn giao:** v0.2 đủ làm nguồn quy chuẩn cho sản phẩm đồ thị mới; mọi thay đổi style hoặc migration dự án cũ phải được giao và nghiệm thu riêng.
