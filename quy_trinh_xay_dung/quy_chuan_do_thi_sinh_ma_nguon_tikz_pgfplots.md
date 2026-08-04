# Quy chuẩn sinh đồ thị hàm số TikZ/PGFPlots dành cho AI

**Phiên bản:** 02 — 2026-07-30\
**Trạng thái:** Bản quy chuẩn tự đầy đủ; khối style chuẩn được quản lí trực tiếp trong tài liệu này và đang được kiểm nghiệm bằng đồ thị đại diện\
**Phạm vi:** Sinh một tệp nguồn `.tex` độc lập cho đồ thị hàm số trong ZO Math\
**Đối tượng sử dụng:** AI, Codex hoặc agent có quyền đọc và ghi trong repository

## 1. Mục đích

Quy chuẩn này là chỉ dẫn vận hành để AI nhận một yêu cầu về đồ thị hàm số, tự phân tích đối tượng toán học và sinh ra một tệp `.tex` hoàn chỉnh bằng TikZ/PGFPlots.

Tệp được sinh phải đồng thời:

- đúng về toán học;
- thể hiện rõ đặc điểm mà hình cần truyền đạt;
- nhất quán với ngôn ngữ thị giác ZO Math;
- biên dịch độc lập và tái tạo ổn định;
- phù hợp để chuyển sang PDF hoặc SVG và chèn vào HTML hoặc PDF của Quarto;
- đủ rõ về cấu trúc để một người hoặc một AI khác có thể kiểm tra, sửa đổi và tái sử dụng.

Đây không phải là quy chuẩn viết bài, dàn trang bài học hay thiết kế toàn bộ trang web. Mọi quy tắc trong tài liệu chỉ phục vụ trực tiếp cho việc tạo tệp `.tex` của một hình đồ thị.

Tài liệu này là nguồn chuẩn duy nhất của style đồ thị ZO Math. Mỗi tệp `.tex` được sinh phải tự chứa nguyên khối style chuẩn ở Mục 15; không nạp style từ một tệp bên ngoài. Khi khối chuẩn được nâng phiên bản, các tệp `.tex` đã hoàn thành vẫn giữ nguyên khối style đã nhúng để có thể tái tạo đúng diện mạo tại thời điểm bàn giao.

Ngôn ngữ thị giác cốt lõi của một đồ thị ZO Math gồm bốn dấu hiệu phải được nhận ra nhất quán: trường minh họa có nền vàng ZO Math rất nhạt và khung bo góc nhẹ; hệ trục tối giản có mũi tên ở cả hai đầu khi trục kéo dài theo hai hướng; đường cong chính mang màu đỏ ZO Math; mọi vạch chia, nhãn và đường phụ chỉ xuất hiện khi chúng giúp đọc một thông tin toán học. Hình phải thanh, thoáng và chính xác, không mô phỏng giấy kẻ ô hay giao diện phần mềm vẽ đồ thị.

## 2. Nhiệm vụ của AI

Khi nhận yêu cầu, AI phải thực hiện trọn vẹn chuỗi công việc sau:

1. đọc yêu cầu và các tệp liên quan trong repository nếu chúng được chỉ định;
2. xác định mục đích toán học của hình;
3. phân tích đầy đủ những đặc điểm của hàm có ảnh hưởng đến cách dựng;
4. chọn phương pháp biểu diễn phù hợp;
5. xác định miền quan sát, miền lấy mẫu, cách chia nhánh và mật độ mẫu;
6. chọn những thành phần thị giác thực sự cần thiết;
7. sinh một tệp `.tex` độc lập theo cấu trúc quy định;
8. đưa hình qua chuỗi kiểm định `.tex → PDF → SVG → Quarto HTML` và kiểm tra ở kích thước sử dụng thực tế;
9. tự sửa lỗi toán học, lỗi biên dịch và lỗi thị giác;
10. chỉ bàn giao khi tệp nguồn và bản render đều đạt bảng kiểm nghiệm thu.

AI không được coi nhiệm vụ là thao tác thay một công thức vào tệp mẫu. Mỗi hàm phải được phân tích như một đối tượng toán học riêng.

## 3. Đầu vào và nguyên tắc xử lý thiếu thông tin

Yêu cầu có thể cung cấp một phần hoặc toàn bộ các thông tin sau:

- công thức hoặc định nghĩa của hàm;
- tập xác định hoặc khoảng đang xét;
- mục đích của hình;
- đặc điểm cần nhấn mạnh;
- các điểm, đường, miền hoặc nhãn bắt buộc;
- vị trí tệp đầu ra;
- tệp mẫu hoặc hình tham chiếu;
- yêu cầu riêng về kích thước hay định dạng xuất.

AI phải ưu tiên theo thứ tự:

1. yêu cầu trực tiếp của người dùng;
2. quy ước cục bộ trong thư mục hoặc tệp liên quan;
3. quy chuẩn này;
4. mặc định của TikZ/PGFPlots chỉ khi quy chuẩn không đề cập.

Nếu đầu vào không chỉ định chi tiết thông thường, AI phải tự quyết định bằng các mặc định trong tài liệu này và không hỏi lại. Chỉ hỏi khi có nhiều cách hiểu toán học khác nhau dẫn đến những hình có mục đích khác nhau rõ rệt, hoặc khi hành động cần vượt ra ngoài phạm vi đã được giao.

Nếu yêu cầu trực tiếp khác với mặc định, AI được thay đổi mặc định nhưng phải giữ tính đúng đắn, khả năng đọc và sự nhất quán tổng thể. Không được viện dẫn quy chuẩn để bỏ qua một chỉ dẫn rõ ràng của người dùng.

## 4. Phân tích toán học bắt buộc

Trước khi viết mã, AI phải xác định ít nhất các yếu tố có liên quan sau:

- tập xác định;
- nghiệm và giao điểm với các trục;
- dấu của hàm;
- tính chẵn, lẻ, tuần hoàn hoặc các đối xứng khác;
- giới hạn tại biên tập xác định và khi biến tiến ra vô cực;
- điểm gián đoạn và loại gián đoạn;
- tiệm cận đứng, ngang hoặc xiên;
- khoảng đồng biến, nghịch biến;
- cực trị;
- độ cong và điểm uốn nếu chúng phục vụ mục đích hình;
- giá trị bị chặn hoặc miền giá trị đáng chú ý;
- số nhánh liên thông của đồ thị;
- hành vi dao động, tốc độ tăng hoặc suy giảm;
- các điểm đặc biệt, đầu mút hoặc giá trị được định nghĩa riêng;
- những vùng mà phép lấy mẫu số có thể tạo hình sai.

Không phải mọi kết quả phân tích đều phải xuất hiện trong hình. AI chỉ đưa vào những thành phần giúp hình thực hiện đúng mục đích. Tuy nhiên, mọi quyết định lược bỏ vẫn phải dựa trên phân tích đúng.

AI phải phân biệt rõ:

- **tập xác định:** tập các giá trị đầu vào mà hàm có nghĩa;
- **miền lấy mẫu:** những khoảng mà PGFPlots thực sự tính các điểm để dựng đường;
- **miền quan sát:** hình chữ nhật được hiển thị trong hình cuối cùng.

Ba miền này có thể khác nhau và không được dùng thay thế cho nhau.

## 5. Quy trình chọn phương pháp dựng

### 5.1. Đồ thị tường minh thông thường

Ưu tiên `\addplot` với biểu thức PGFPlots khi hàm được cho dưới dạng $y=f(x)$, biểu thức được PGFPlots tính ổn định và đường cong không đòi hỏi dữ liệu tính trước đặc biệt.

### 5.2. Hàm có điểm không xác định hoặc tiệm cận đứng

Phải chia miền lấy mẫu thành các khoảng liên tục riêng. Mỗi nhánh dùng một lệnh vẽ độc lập. Không lấy mẫu xuyên qua điểm không xác định và không dựa vào `unbounded coords=jump` như biện pháp duy nhất khi vị trí gián đoạn đã biết.

Điểm dừng lấy mẫu gần tiệm cận phải nằm đủ gần để đường cong rời cửa sổ quan sát một cách tự nhiên, nhưng không gần đến mức gây tràn số, làm méo đường dẫn hoặc mở rộng bounding box.

### 5.3. Hàm từng phần

Vẽ từng công thức trên đúng miền của nó. Thể hiện đầu mút bằng điểm đặc hoặc điểm rỗng theo việc giá trị biên có thuộc nhánh hay không. Không để hai nhánh chồng nét tại một điểm chỉ vì dùng cùng một đầu mút lấy mẫu.

### 5.4. Hàm dao động nhanh

Với các hàm như $\sin(1/x)$, phải chia nhánh, chọn ngưỡng dừng gần điểm tích tụ và tăng mật độ mẫu có kiểm soát. Không được nối qua điểm gián đoạn, không dùng một mảng màu đặc để giả làm vô hạn dao động và không tuyên bố rằng phần hữu hạn được vẽ là toàn bộ hành vi của hàm.

Nếu lấy mẫu đều theo $x$ không đủ trung thực, AI phải dùng tham số hóa, phân đoạn thích nghi hoặc dữ liệu tính trước.

### 5.5. Đường tham số

Dùng chế độ tham số khi đối tượng được mô tả tự nhiên bởi $(x(t),y(t))$, khi biểu diễn tường minh gây nhiều nhánh khó kiểm soát hoặc khi cần bảo toàn trật tự của đường cong.

### 5.6. Dữ liệu tính trước

Dùng bảng tọa độ hoặc dữ liệu sinh ngoài PGFPlots khi:

- biểu thức vượt khả năng tính ổn định của PGF;
- cần độ chính xác số cao;
- cần lấy mẫu thích nghi;
- đường cong là nghiệm số;
- dữ liệu đã tồn tại như nguồn chuẩn trong repository.

Dữ liệu tính trước phải có nguồn và quy trình tái tạo rõ ràng. Không chép thủ công một tập điểm thưa rồi nối chúng như thể đó là đồ thị chính xác.

### 5.7. Miền tô và quan hệ giữa các đường

Dùng các đường biên được đặt tên và cơ chế tô của PGFPlots khi cần biểu diễn diện tích, miền nghiệm hoặc khoảng giữa hai đồ thị. Mảng tô phải nằm dưới đường biên, có độ trong suốt vừa phải và không che các nét chính.

### 5.8. Hình học tọa độ

Khi khoảng cách, góc, đường tròn hoặc hình dạng Euclid là thông tin toán học, phải bảo toàn tỉ lệ đơn vị hai trục bằng `axis equal image`. Không dùng thiết lập này cho mọi đồ thị hàm số.

## 6. Thứ tự các lớp của hình

AI phải tổ chức các đối tượng theo thứ tự thị giác từ nền đến tiền cảnh:

1. nền của trường đồ thị;
2. lưới phụ nếu có;
3. lưới chính nếu có;
4. miền tô hoặc dải nhấn;
5. đường tham chiếu;
6. tiệm cận;
7. các đường cong phụ;
8. đường cong chính;
9. điểm đặc, điểm rỗng và điểm đặc biệt;
10. nhãn, ký hiệu và chú thích đặt trong hình.

Một đối tượng nằm trên lớp sau không được che khuất thông tin thiết yếu của lớp trước. Đường cong chính và các điểm đặc biệt luôn phải nhận ra ngay khi nhìn hình ở kích thước xuất bản thực tế.

### 6.1. Trường minh họa và khung bo góc

Mỗi đồ thị chuẩn được đặt trong một trường minh họa có nền vàng ZO Math rất nhạt, viền mảnh và góc bo nhẹ. Khung này chỉ tổ chức không gian thị giác; nó không phải biên của mặt phẳng tọa độ và không mang ý nghĩa toán học.

Khung phải:

- bao quanh cả miền `axis`, mũi tên, nhãn trục và khoảng đệm bên trong;
- dùng nền `zoPlotBackground`, viền `zoPlotBorder`;
- có viền liền `0.45pt`, bán kính bo `2mm`, không đổ bóng, không viền kép;
- có khoảng đệm thị giác khởi đầu `4mm` ở bốn phía;
- để đầu mũi tên cách mép trong của khung tối thiểu `3mm`;
- để nhãn trục và nhãn đường cong cách khung tối thiểu `2mm`;
- không bị dùng như một đường cắt dữ liệu: đường cong được cắt tại miền quan sát của `axis`, rồi toàn bộ `axis` mới được đặt trong trường minh họa.

Khi hình có lý do xuất bản đặc biệt để không dùng khung hoặc nền, AI phải nêu lý do; nền trắng trơn không phải mặc định của đồ thị chuẩn.

## 7. Hệ màu ngữ nghĩa ZO Math

### 7.1. Nguyên tắc

Mọi màu phải được khai báo bằng mã HEX từ hệ màu chính thức. AI không được tự pha màu, dùng màu gần giống hoặc phụ thuộc vào các tên màu mặc định không được ánh xạ rõ.

Màu mang vai trò ngữ nghĩa, không chỉ để trang trí. Một hình thông thường nên dùng ít màu nhất có thể. Không dùng nhiều màu để phân biệt các đối tượng vốn đã phân biệt được bằng vị trí, kiểu nét hoặc nhãn.

### 7.2. Ánh xạ mặc định

| Tên ngữ nghĩa trong tệp `.tex` |   Mã HEX | Vai trò mặc định                                         |
| ------------------------------ | -------: | -------------------------------------------------------- |
| `zoWhite`                      | `FFFFFF` | màu trắng khi một ngoại lệ thực sự cần                   |
| `zoPlotBackground`             | `FFF9E9` | nền vàng rất nhạt bắt buộc của trường đồ thị chuẩn       |
| `zoPlotBorder`                 | `DFD7CA` | viền ấm, mảnh của khung bo góc                           |
| `zoBackground`                 | `FBFAF8` | nền xám ấm rất nhạt cho ngoại lệ có lý do                |
| `zoGridMinor`                  | `F8F5F0` | lưới phụ                                                 |
| `zoGridMajor`                  | `DFD7CA` | lưới chính                                               |
| `zoAxis`                       | `554F48` | trục, vạch chia và chi tiết trục                         |
| `zoText`                       | `3E3A35` | chữ và nhãn chính                                        |
| `zoTextStrong`                 | `25221F` | chữ cần độ tương phản cao                                |
| `zoGraphMain`                  | `EF5350` | đường cong chính                                         |
| `zoGraphStrong`                | `BF4240` | điểm hoặc đoạn chính cần tăng độ đậm                     |
| `zoReference`                  | `997918` | đường hoặc đối tượng tham chiếu                          |
| `zoHighlight`                  | `FFCA28` | nhấn mạnh có kiểm soát                                   |
| `zoHighlightLight`             | `FFF4D4` | miền tô vàng nhạt                                        |
| `zoSuccess`                    | `1DE8B5` | chỉ dùng khi ý nghĩa xác nhận/thành công thực sự tồn tại |

Các màu `42A5F5` và `7986CB` chỉ là màu tương thích cũ. Không dùng chúng cho đồ thị mới nếu yêu cầu không chỉ định một vai trò ngữ nghĩa riêng.

### 7.3. Toàn bộ nguồn màu được phép

- Xám ấm: `FBFAF8`, `F8F5F0`, `DFD7CA`, `C7BEB2`, `9F968B`, `766F66`, `554F48`, `3E3A35`, `25221F`.
- Đỏ: `FDEDED`, `FBDCDC`, `FACBCA`, `F8BAB9`, `F7A9A7`, `F59796`, `F38684`, `F27572`, `F06461`, `EF5350`, `D74A48`, `BF4240`, `A73A38`, `8F3130`, `772928`, `5F2120`, `471818`, `2F1010`, `170808`.
- Vàng: `FFF9E9`, `FFF4D4`, `FFEFBE`, `FFE9A9`, `FFE493`, `FFDF73`, `FFD968`, `FFD452`, `FFCF3D`, `FFCA28`, `E5B524`, `CCA120`, `B28D1C`, `997918`, `7F6514`, `665010`, `4C3C0C`, `332808`, `191404`.
- Bổ trợ: `1DE8B5`, `42A5F5`, `7986CB`, `FFFFFF`, `000000`.

Nếu cần một vai trò chưa có trong bảng ánh xạ mặc định, AI phải chọn một màu trong danh sách trên, khai báo tên ngữ nghĩa rõ ràng và dùng nhất quán trong toàn hình.

## 8. Trục, lưới và vạch chia

### 8.1. Trục

Đồ thị Descartes thông thường ưu tiên hai trục đi qua gốc khi gốc tọa độ nằm trong miền quan sát và việc đó giúp đọc hình. Nếu gốc tọa độ không liên quan hoặc nằm ngoài miền quan sát, có thể đặt một hoặc cả hai trục gần biên của trường hình. Trục phải vẫn được thể hiện như một đối tượng riêng, không trùng hoàn toàn với đường biên và không khiến người đọc hiểu nhầm rằng biên trường hình là một đường có ý nghĩa toán học.

Trục phải có màu `zoAxis`, dày `0.8pt` theo khối style chuẩn và mảnh hơn đường cong chính. Khi một trục tọa độ tiếp tục theo cả hai hướng trong miền đang biểu diễn, trục phải có mũi tên ở cả hai đầu. Hai mũi tên biểu thị sự tiếp tục của trục số, không thay đổi quy ước chiều dương. Chỉ bỏ mũi tên ở một đầu khi hình chỉ biểu diễn một nửa trục, hoặc khi đầu ấy tương ứng với biên toán học thật của miền đang xét. Không bỏ mũi tên chỉ vì trục chạm biên của cửa sổ quan sát.

Trong phiên bản này, hai đầu trục dùng cú pháp mũi tên mặc định, tương thích ổn định với PGFPlots:

```tex
<->
```

Không dùng lại `Stealth[...]` hoặc `>=stealth` trước khi một bản thử riêng đã biên dịch sạch trên đúng môi trường LuaLaTeX của repository. Hình học đầu mũi tên hiện tại tiếp tục được đánh giá trực tiếp trên các đồ thị đại diện.

Hai trục dùng cùng kiểu và cùng kích thước đầu mũi tên. Chỉ đầu dương mang nhãn trục:

- nhãn $x$ mặc định nằm phía ngoài đầu mũi tên dương của trục $x$, theo hướng kéo dài của trục;
- nhãn $y$ mặc định nằm phía trên đầu mũi tên dương của trục $y$, theo hướng kéo dài của trục;
- hai nhãn phải ở gần đầu mũi tên, có khoảng cách thị giác tương đương và không chạm vào mũi tên;
- nếu vị trí mặc định bị đường cong hoặc thành phần khác cản, có thể dịch chuyển nhãn đến vị trí gần đó, ưu tiên giữ nhãn ở phía ngoài khung trục và không làm mơ hồ trục mà nhãn biểu thị;
- vị trí, điểm neo và độ dịch chuyển cụ thể của mỗi nhãn được khai báo trực tiếp trong tệp nguồn của từng đồ thị;
- nhãn trục dùng `\normalsize` và màu `zoText`.

Hai vị trí trên là điểm xuất phát, không phải tọa độ cứng bắt buộc. Vị trí của $x$, $y$, $O$, các số trên trục và mọi nhãn khác phải được khai báo trực tiếp trong tệp nguồn của từng hình. Sau mỗi lần render, AI phải kiểm tra vùng an toàn quanh nhãn và tự điều chỉnh `at`, `anchor`, `xshift`, `yshift` hoặc cách tạo nhãn số cho đúng hoàn cảnh. Không đưa các quyết định vị trí này vào khối style chuẩn.

Khi đường cong, tiệm cận, điểm đặc biệt hoặc chú thích chiếm vùng neo thông thường, nhãn được dời đến vùng trống gần đầu trục nhất mà vẫn giữ rõ quan hệ với trục. Với $y=1/x$, nhánh ở góc phần tư I tiến sát trục hoành nên nhãn $x$ phải dời xuống dưới đầu dương của trục hoành; nhãn $y$ có thể giữ phía trái đầu dương của trục tung. Đây là quyết định cục bộ của hình, không phải một style mới.

Nếu gốc tọa độ cần được định vị, ghi duy nhất $O$, không ghi số $0$ trên cả hai trục. Nhãn $O$ đặt chếch xuống–trái của giao điểm, không đè lên trục, đường cong hoặc điểm đặc. Có thể lược bỏ $O$ khi gốc không có vai trò hoặc khi gốc nằm ngoài miền quan sát.

Không vẽ khung hộp đậm. Khung bo góc nhẹ ở mục 6.1 là trường minh họa, không phải bốn đường trục hay biên tọa độ. Không để trục cạnh tranh thị giác với đường cong.

### 8.2. Lưới

Không dùng lưới theo mặc định. Chỉ bật lưới khi nó giúp đọc một thông tin toán học cụ thể như tọa độ, chu kỳ, độ lớn hoặc quan hệ hình học; việc một hàm có các giá trị nguyên dễ thấy không tự nó là lý do đủ để bật lưới. Hình mang tính định tính phải bỏ lưới.

Nếu dùng lưới:

- lưới phụ dùng `zoGridMinor` và nét mảnh hơn lưới chính;
- lưới chính dùng `zoGridMajor`, dày `0.35pt` theo khối style chuẩn và vẫn phải nhạt hơn trục;
- mật độ lưới phải phù hợp với vạch chia;
- không tạo một nền ô vuông dày làm chìm đường cong.

### 8.3. Vạch chia và số

Chỉ hiển thị những vạch chia giúp đọc hình. Ưu tiên các mốc nguyên, phân số đơn giản, bội của $\pi$, giá trị cực trị, điểm gián đoạn hoặc biên đáng chú ý.

Vạch chia phải rất ngắn, cắt đều qua trục, mảnh hơn trục nhưng vẫn rõ. Giá trị khởi đầu là chiều dài tổng `0.8mm` và độ dày `0.32pt`. Không dùng hệ vạch tự động dày đặc; mỗi vạch xuất hiện phải có chức năng đọc hình.

Vạch chia và nhãn số không bắt buộc có cùng mật độ: có thể giữ một số vạch cần thiết nhưng chỉ ghi nhãn ở các mốc quan trọng.

Với các vạch chia được khai báo bằng `xtick` và `ytick`. Nhãn tự động của PGFPlots phải được ẩn:

```text
xtick={...},
ytick={...},
xticklabel=\empty,
yticklabel=\empty,
```

Mỗi giá trị cần hiển thị phải được đặt bằng một \node riêng tại tọa độ toán học tương ứng. Không dùng `xticklabels`, `yticklabels`, `xticklabel style` hoặc `yticklabel style` để tạo và bố trí đồng loạt các nhãn.

Ví dụ, nhãn $\pi$ trên trục hoành được đặt như sau:

```tex
\node[
  text=zoText,
  font=\footnotesize,
  anchor=north,
  xshift=0pt,
  yshift=-2pt
] at (axis cs:pi,0) {$\pi$};
```

Tọa độ trong `axis cs` phải giữ đúng vị trí toán học của vạch chia. Việc tinh chỉnh thị giác chỉ được thực hiện bằng `anchor`, `xshift` và `yshift`; không thay đổi tọa độ toán học để né va chạm.

Vị trí của từng nhãn phải được quyết định sau khi quan sát bản render. Nếu nhãn bị đường cong, điểm đặc biệt, tiệm cận hoặc thành phần khác cản, điều chỉnh riêng `anchor`, `xshift` hoặc `yshift` của chính `\node` đó. Không sửa quy tắc dùng chung để xử lý một va chạm cục bộ.

Các nhãn giá trị dùng `\footnotesize` và màu chữ chung `zoText`. Không để số $0$ lặp lại trên cả hai trục; gốc tọa độ chỉ mang một nhãn $O$ nếu nhãn này cần thiết. Không dùng quá nhiều chữ số thập phân và không đặt các nhãn sát nhau đến mức nhập chữ.

Với hàm lượng giác, nhãn phải dùng biểu thức chính xác như $-\pi$, $-\pi/2$, $\pi/2$, $\pi$, không thay bằng số thập phân nếu không có lý do riêng.

Danh sách vạch chia, nội dung hiển thị, tọa độ, điểm neo và độ dịch chuyển của từng nhãn phải được khai báo trực tiếp trong tệp nguồn của hình. Khối style chuẩn không được quyết định vị trí của các nhãn giá trị.

## 9. Đường cong, đường tham chiếu và tiệm cận

### 9.1. Đường cong chính

Đường cong chính dùng `zoGraphMain`, nét liền, dày `1.2pt` theo khối style chuẩn, đầu nét và chỗ nối tròn. Độ dày phải đủ rõ khi hình được thu về chiều rộng một cột nội dung, nhưng không được che mất độ cong nhỏ, giao điểm hoặc khoảng hở.

Không dùng marker tại mọi điểm lấy mẫu. Không dùng hiệu ứng phát sáng, bóng đổ, gradient hoặc trang trí không mang thông tin toán học.

### 9.2. Nhiều đường cong

Nếu một hình chứa nhiều đường, phải xác định rõ một đường chính và các đường phụ, trừ khi mục đích là so sánh bình đẳng. Đường cong phụ dùng độ dày thử nghiệm `0.9pt`. Phân biệt trước hết bằng độ đậm, kiểu nét và nhãn trực tiếp; chỉ thêm màu khi thật cần thiết.

Nhãn trực tiếp gần đường cong được ưu tiên hơn một bảng chú giải tách rời, miễn là nhãn không gây nhập nhằng.

### 9.3. Đường tham chiếu

Đường như $y=x$, tiếp tuyến, đường phụ chiếu tọa độ hoặc đường biên so sánh dùng `zoReference` hoặc một xám ấm thích hợp. Chúng phải mảnh hơn đường chính; đường phụ trợ và đường chiếu dùng độ dày thử nghiệm `0.6pt`, thường kèm nét đứt hoặc nét chấm gạch theo vai trò.

### 9.4. Tiệm cận

Tiệm cận phải được vẽ như một đối tượng toán học riêng, không phải phần của đường cong. Dùng nét đứt, độ dày thử nghiệm `0.8pt`, màu tham chiếu hoặc xám đậm vừa phải, và đặt dưới đường cong chính.

Chỉ vẽ tiệm cận phục vụ mục đích của hình. Nếu nhãn cần thiết, dùng công thức của đường thẳng. Không để nét tiệm cận trùng với lưới đến mức không thể phân biệt.

## 10. Điểm đặc biệt, đầu mút và khoảng trên trục

Điểm đặc dùng lõi đặc với màu tương ứng của đối tượng. Điểm rỗng dùng lõi trùng hoàn toàn với `zoPlotBackground`, viền cùng màu với đối tượng và đủ dày để vẫn nhận ra khi thu nhỏ; không để lõi trong suốt vì nét phía dưới sẽ xuyên qua. Khối style chuẩn dùng `mark size=2.2pt` cho điểm đặc biệt thông thường, `2.8pt` cho điểm là trọng tâm trực tiếp của hình và `1.7pt` cho điểm phụ trợ. Điểm đặc và điểm rỗng cùng vai trò phải có cùng kích thước.

Mọi điểm đặc biệt phải được đặt bằng tọa độ toán học chính xác, không ước lượng bằng mắt. Nếu điểm nằm trên một đường cong đã lấy mẫu, vẫn nên vẽ điểm ở lớp riêng để kích thước và thứ tự lớp ổn định.

Nhãn tọa độ chỉ xuất hiện khi cần cho việc đọc. Ưu tiên đặt lệch khỏi đường cong, không dùng đường dẫn dài nếu một vị trí gần đã đủ rõ. Vị trí do AI sinh là vị trí ban đầu; người kiểm định được phép tinh chỉnh `anchor`, `xshift`, `yshift` ở mức vài `pt` sau khi xem ảnh thật. Đây là một phần bình thường của nghiệm thu quang học, không phải lí do để thay đổi tọa độ toán học của điểm hoặc tạo một style vị trí dùng chung.

Đường chiếu tọa độ chỉ chạy từ điểm đến đúng trục cần đọc, không kéo xuyên toàn trường đồ thị và không có mũi tên. Nó nằm dưới trục, đường cong và điểm; đi tới tâm điểm để dấu điểm vẽ sau che đầu đường chiếu. Nếu chỉ một tọa độ có ý nghĩa, chỉ vẽ một đường chiếu. Tại chân đường chiếu, dùng vạch chia chuẩn và không lặp lại một nhãn đã có.

Đường chiếu phải được vẽ trước marker của điểm đặc biệt. Đường chiếu kết thúc tại tâm điểm; marker được vẽ sau sẽ che đầu nét đứt, nhờ đó đường chiếu không xuyên qua hoặc làm biến dạng dấu điểm.

Nếu đường chiếu phục vụ việc đọc hoành độ, nó chỉ chạy từ điểm đến trục hoành; nếu phục vụ tung độ, nó chỉ chạy đến trục tung. Không tự động vẽ cả hai đường chiếu cho mọi điểm.

Với khoảng hoặc tập trên trục số, dùng đầu mút đặc/rỗng đúng với quan hệ thuộc tập; đoạn hoặc tia phải có mũi tên và hướng chính xác. Không dùng màu tô như cách duy nhất để phân biệt đầu mút đóng và mở.

Khi hình chứa hai dãy hoành độ xen kẽ hoặc tập trung dày trên cùng một đoạn trục, có thể đặt nhãn của một dãy phía trên trục và dãy còn lại phía dưới trục để duy trì thứ tự và tránh nhập chữ.

Trong vùng dày, ưu tiên các ký hiệu rút gọn như $a_n$, $b_n$, $c_n$ tại từng vị trí; công thức tổng quát của dãy được đưa vào hộp chú thích. Không lặp công thức phân số đầy đủ tại mọi điểm nếu điều đó làm mất khả năng đọc.

Các nhãn phải giữ đúng tọa độ toán học. Việc né va chạm chỉ được thực hiện bằng `anchor`, `xshift`, `yshift`, lựa chọn phía trên hoặc phía dưới trục và lược bớt nhãn; không dịch tọa độ của điểm đánh dấu.

## 11. Miền tô

Miền tô phải dùng một màu nhạt từ hệ chính thức với độ trong suốt đủ để thấy lưới, trục và đường biên. Màu mặc định cho nhấn mạnh là `zoHighlightLight`; khi miền thuộc đường cong chính có thể dùng một đỏ rất nhạt.

Đường biên quan trọng phải được vẽ lại phía trên mảng tô. Không để đường viền tự sinh của polygon tạo thêm một nét không có ý nghĩa.

Nếu có nhiều miền chồng nhau, AI phải bảo đảm phần giao vẫn phân biệt được mà không tạo màu bẩn hoặc tương phản quá thấp. Khi màu không giải quyết tốt, dùng hatch hoặc tách hình.

## 12. Nhãn và chữ trong hình

Chỉ đặt chữ trực tiếp trong trường đồ thị khi nó giúp người đọc nhận ra đối tượng hoặc hiểu một quan hệ cần thiết. Không đưa lời giải thích dài vào hình.

Mọi ký hiệu toán học phải ở math mode. Ký hiệu trong hình phải thống nhất với bài viết, đặc biệt về tên biến, tham số, khoảng và cách viết hàm.

Nhãn phải:

- dùng `zoText` hoặc màu của đối tượng khi sự liên hệ cần được thấy ngay;
- tránh giao với đường cong, trục, vạch chia và nhãn khác;
- không bị cắt bởi `clip`;
- giữ được khả năng đọc khi hình được thu nhỏ;
- không làm bounding box mất cân đối.

Nhãn đường cong phải được đặt trong vùng trống gần chính đường mà nó gọi tên, cùng màu với các nhãn khác tức màu chữ chung `zoText`. Nhãn của đường cong thông thường ưu tiên nằm ngang. Riêng nhãn của đường thẳng, tiếp tuyến, tiệm cận xiên hoặc đường tham chiếu có hướng rõ ràng nên nghiêng theo chính hướng hiển thị của đường.

Khi một nhánh đường cong rời cửa sổ quan sát ở vùng thoáng, ưu tiên đặt nhãn công thức gần phần cuối nhìn thấy của nhánh ấy, theo cách tương tự nhãn trục gọi tên đối tượng ở nơi nó tiếp tục. Không đặt nhãn đúng tại điểm bị cắt bởi biên, vì đó chỉ là đầu mút của miền quan sát chứ không phải đầu mút toán học. Vị trí khoảng `94%–97%` chiều dài đường vẽ có thể dùng làm điểm bắt đầu để thử, sau đó phải điều chỉnh theo bản render; đây không phải tỉ lệ bắt buộc.

Có thể gắn node trực tiếp vào `\addplot` bằng `node[pos=...]` để nhãn đi cùng đường cong. Chỉ dùng cách này khi node không bị cắt, không làm thay đổi bounding box ngoài ý muốn và vẫn tách khỏi nét cong bằng `anchor`, `xshift`, `yshift`. Với nhiều nhánh hoặc vùng cuối bị chật, chọn một vùng trống khác có quan hệ trực tiếp và không nhập nhằng với đường.

Khi nhãn cần nghiêng theo đường, phải dùng một `\path` trùng hướng với đường và đặt node bằng `sloped`; không ấn định góc bằng `rotate` nếu hai trục có thể có tỉ lệ hiển thị khác nhau. Góc nhìn của đường phụ thuộc đồng thời vào hệ số góc và tỉ lệ vật lý giữa hai trục.

Điểm neo của node không được nằm ngay trên nét cong nếu điều đó làm chữ chạm hoặc nhập vào đường. Mặc định không dùng đường dẫn từ nhãn đến đồ thị; chỉ dùng một đoạn dẫn rất ngắn, không mũi tên, khi nhiều đường gần nhau khiến việc nhận diện vẫn còn nhập nhằng.

Nhãn điểm và nhãn đường cong dùng `\small`; số trên vạch chia và chú thích phụ rất ngắn dùng `\footnotesize`. Không dùng `\scriptsize` làm mặc định.

Không dùng một chú giải lớn nếu có thể gắn nhãn trực tiếp một cách rõ ràng.

### 12.1. Hộp chú thích

Chỉ dùng hộp chú thích khi nhãn trực tiếp làm hình rối, khi nhiều đối tượng tập trung trong cùng một vùng hoặc khi cần giải thích một họ điểm, một dãy đặc biệt hay nhiều đường có quan hệ chặt chẽ.

Hộp chú thích chuẩn dùng `\matrix` hai cột: cột trái chứa mẫu ký hiệu, cột phải chứa công thức hoặc nội dung. Mặc định hộp được neo bằng `anchor=north east` tại `rel axis cs:1,1`, có nền `zoWhite`, viền `zoPlotBorder` dày `0.45pt`, góc bo `1mm`, `inner sep=5pt`, `row sep=3pt` và `column sep=5pt`.

Khi dùng `\matrix` bên trong `axis`, phải khai báo `ampersand replacement=\&` và dùng `\&` để phân cột.

Mẫu ký hiệu trong hộp chú thích phải tái tạo đúng kiểu nét, màu, độ dày, marker và kích thước đang dùng trên đồ thị. Không thay marker bằng một ký tự LaTeX có hình dạng gần giống, chẳng hạn không dùng `\times` thay cho `mark=x` hoặc `\bullet` thay cho `mark=*`.

Đối với đường cong, mẫu chú thích phải là một đoạn nét ngắn đúng màu, kiểu nét và độ dày của đường; không dùng ô màu đặc nếu đối tượng được biểu diễn bằng đường. Đối với điểm, phải dùng chính plot mark tương ứng.

Nếu marker được dựng bằng một `tikzpicture` con, phải khóa bounding box của ký hiệu ở kích thước xác định để hình con không làm tăng bất thường chiều cao hàng hoặc kích thước hộp chú thích.

## 13. Kích thước, tỉ lệ và miền quan sát

### 13.1. Kích thước mặc định

Đồ thị thông thường dùng:

```tex
width=12cm,
height=7.5cm,
scale only axis,
axis equal image=false,
```

Hình chỉ được co giãn đồng dạng khi đưa vào tài liệu. Không dùng `\resizebox` trong tệp nguồn, không kéo giãn độc lập theo một chiều và không đặt kích thước bằng `\textwidth` hoặc `\linewidth`.

### 13.2. Các ngoại lệ kích thước

Chỉ dùng các ngoại lệ xác định trước khi bản chất đối tượng đòi hỏi:

- hình vuông: `width=9cm`, `height=9cm`, `axis equal image`;
- hình ngang rộng: `width=14cm`, `height=7cm`;
- hình đứng: `width=9cm`, `height=11cm`.

Không tạo một kích thước tùy ý mới chỉ để chứa quá nhiều nội dung. Trước hết phải bỏ chi tiết không cần thiết, rút gọn nhãn, điều chỉnh miền quan sát hoặc tách hình.

### 13.3. Chọn miền quan sát

Mỗi tệp phải khai báo tường minh `xmin`, `xmax`, `ymin`, `ymax`. Không để PGFPlots tự quyết định toàn bộ miền từ dữ liệu.

Miền theo $x$ phải đủ để thấy những đặc điểm phục vụ hình: nghiệm, cực trị, điểm uốn, gián đoạn, tiệm cận, chu kỳ, xu hướng hoặc đối xứng. Ưu tiên miền đối xứng khi đối xứng là đặc điểm cần đọc, nhưng không tạo khoảng trống vô ích chỉ để đạt đối xứng hình thức.

Miền theo $y$ phải cho thấy hình dạng cần đọc mà không bị một vài giá trị lớn gần tiệm cận chi phối. Với hàm bị chặn, chừa một khoảng nhỏ ngoài các giá trị biên. Với hàm không bị chặn, giới hạn trên và dưới chỉ là cửa sổ quan sát, không phải tập giá trị.

Các đặc điểm quan trọng nên cách mép hình khoảng 5–10% phạm vi tương ứng. Đây là điểm khởi đầu để đánh giá trên bản render, không phải công thức máy móc.

Miền quan sát còn phải chừa khoảng thở để đường cong, điểm đặc và nhãn không chạm khung. Đường cong chỉ được chạm hoặc rời miền `axis` khi việc cắt ấy có chủ ý nhằm biểu thị rằng nhánh còn tiếp tục. Không mở rộng miền chỉ để lấp đầy khung, và không để khung ép miền quan sát vào một tỉ lệ làm yếu đặc điểm chính.

### 13.4. Cắt biên và lề

Mặc định dùng:

```tex
enlargelimits=false,
clip=true,
clip mode=individual,
```

Không đặt `clip=false` cho toàn bộ `axis` chỉ để cứu một nhãn đặt sai. Điều chỉnh vị trí nhãn, miền quan sát hoặc lớp vẽ thích hợp.

Có thể dùng `restrict y to domain` như giới hạn kỹ thuật của đường dẫn, nhưng không dùng nó để thay tập xác định, thay việc chia nhánh hoặc che một lỗi lấy mẫu.

Tệp `standalone` dùng `border=3pt`. Khoảng này là lề ngoài của tệp xuất, không thay thế khoảng đệm bên trong miền quan sát.

## 14. Mật độ mẫu và độ chính xác số

AI phải chọn số mẫu dựa trên độ phức tạp thực tế, không dùng một con số lớn cố định cho mọi hàm.

Mật độ đạt yêu cầu khi đường cong render mượt, không có góc giả, không bỏ qua cực trị hoặc nghiệm đáng chú ý và không làm thay đổi hình khi tăng số mẫu ở mức kiểm tra hợp lý.

Phải tăng hoặc phân bố lại mẫu khi:

- độ cong thay đổi nhanh;
- hàm dao động nhanh;
- hai đặc điểm nằm gần nhau;
- đường cong tiến gần tiệm cận;
- phép biến đổi tham số làm điểm mẫu phân bố không đều.

Không tăng mẫu vô hạn để sửa một phương pháp dựng sai. Khi lấy mẫu đều không phù hợp, phải chia miền, đổi biến, tham số hóa hoặc dùng dữ liệu tính trước.

## 15. Cấu trúc bắt buộc của tệp `.tex`

Tệp phải là tài liệu độc lập và có cấu trúc dễ kiểm tra theo thứ tự:

1. khai báo lớp `standalone` với cỡ chữ nền `10pt`;
2. nạp `fontspec`, `unicode-math`, `pgfplots` và các gói cần thiết khác;
3. khai báo STIX Two Text và STIX Two Math từ `assets/fonts/`;
4. đặt phiên bản tương thích PGFPlots;
5. nạp đúng các thư viện TikZ/PGFPlots thực sự dùng;
6. chép nguyên khối style chuẩn ở Mục 15.1 vào tệp;
7. khai báo vị trí nhãn, macro hoặc dữ liệu riêng của hình;
8. bắt đầu tài liệu;
9. tạo `tikzpicture` và `axis`;
10. vẽ các lớp theo đúng thứ tự;
11. kết thúc đầy đủ các môi trường và tài liệu.

Không nạp gói hoặc thư viện không dùng. Tệp được biên dịch ngay tại thư mục chứa tệp nguồn theo cấu hình LuaLaTeX của VS Code, để `.aux`, `.log`, `.pdf` và các sản phẩm liên quan nằm cùng hệ thư mục của hình, không rơi vào gốc repository. Mọi tệp phông và dữ liệu ngoài phải được dẫn chiếu bằng đường dẫn tương đối tính từ thư mục chứa tệp `.tex`; không dùng đường dẫn tuyệt đối hoặc cấu hình riêng của một máy tính.

Khối style chuẩn phải được chép nguyên vẹn, kể cả khi một hình không dùng hết mọi style đã khai báo. Không rút gọn khối chuẩn theo từng hình, vì việc đó tạo ra nhiều biến thể khó kiểm soát. Các style hoặc màu thật sự riêng của một hình được khai báo sau khối chuẩn và không được đổi nghĩa những tên đã có.

### 15.1. Khối style chuẩn

Khối dưới đây là nguồn chuẩn duy nhất của bảng màu và style đồ thị ZO Math trong phiên bản này. Khi sinh tệp mới, chép nguyên văn từ dòng `BEGIN` đến dòng `END`, không nạp từ tệp bên ngoài và không chỉnh các giá trị ngay trong khối.

```tex
% BEGIN ZO MATH GRAPH STYLE — VERSION 05 — 2026-07-30
% Copy this block verbatim into every graph source.

\definecolor{zoWhite}{HTML}{FFFFFF}
\definecolor{zoPlotBackground}{HTML}{FFF9E9}
\definecolor{zoPlotBorder}{HTML}{DFD7CA}
\definecolor{zoBackground}{HTML}{FBFAF8}
\definecolor{zoGridMinor}{HTML}{F8F5F0}
\definecolor{zoGridMajor}{HTML}{DFD7CA}
\definecolor{zoAxis}{HTML}{554F48}
\definecolor{zoText}{HTML}{3E3A35}
\definecolor{zoTextStrong}{HTML}{25221F}
\definecolor{zoGraphMain}{HTML}{EF5350}
\definecolor{zoGraphStrong}{HTML}{BF4240}
\definecolor{zoGraphSecondary}{HTML}{997918}
\definecolor{zoReference}{HTML}{997918}
\definecolor{zoHighlight}{HTML}{FFCA28}
\definecolor{zoHighlightLight}{HTML}{FFF4D4}
\definecolor{zoSuccess}{HTML}{1DE8B5}

\pgfplotsset{
  zo axis/.style={
    width=12cm,
    height=7.5cm,
    scale only axis,
    axis equal image=false,
    enlargelimits=false,
    clip=true,
    clip mode=individual,
    axis lines=middle,
    grid=none,
    axis line style={draw=zoAxis,line width=0.8pt,<->},
    tick align=center,
    tickwidth=0.4mm,
    tick style={draw=zoAxis,line width=0.32pt},
    every axis x label/.append style={
      text=zoText,
      font=\normalsize
    },
    every axis y label/.append style={
      text=zoText,
      font=\normalsize
    },
    every tick label/.append style={
      text=zoText,
      font=\footnotesize
    },
    every axis plot/.append style={line cap=round,line join=round}
  },
  zo grid/.style={
    major grid style={draw=zoGridMajor,line width=0.35pt},
    minor grid style={draw=zoGridMinor,line width=0.25pt}
  },
  zo graph main/.style={
    draw=zoGraphMain,
    line width=1.2pt,
    solid,
    no marks
  },
  zo graph secondary/.style={
    draw=zoGraphSecondary,
    line width=0.9pt,
    solid,
    no marks
  },
  zo graph strong/.style={
    draw=zoGraphStrong,
    line width=1.2pt,
    solid,
    no marks
  },
  zo reference/.style={
    draw=zoReference,
    line width=0.6pt,
    dashed,
    no marks
  },
  zo asymptote/.style={
    draw=zoReference,
    line width=0.8pt,
    dashed,
    no marks
  },
  zo auxiliary line/.style={
    draw=zoAxis,
    line width=0.6pt,
    densely dashed,
    no marks
  },
  zo point closed/.style={
    only marks,
    mark=*,
    mark size=2.2pt,
    draw=zoGraphMain,
    fill=zoGraphMain
  },
  zo point open/.style={
    only marks,
    mark=*,
    mark size=2.2pt,
    draw=zoGraphMain,
    fill=zoPlotBackground,
    line width=0.8pt
  },
  zo point emphasized/.style={
    only marks,
    mark=*,
    mark size=2.8pt,
    draw=zoGraphStrong,
    fill=zoGraphStrong
  },
  zo point auxiliary/.style={
    only marks,
    mark=*,
    mark size=1.7pt,
    draw=zoReference,
    fill=zoReference
  }
}

\tikzset{
  zo graph field/.style={
    show background rectangle,
    inner frame sep=4mm,
    background rectangle/.style={
      fill=zoPlotBackground,
      draw=zoPlotBorder,
      line width=0.45pt,
      rounded corners=2mm
    }
  },
  zo axis label/.style={
    text=zoText,
    font=\normalsize
  },
  zo origin label/.style={
    text=zoText,
    font=\normalsize
  },
  zo graph label/.style={
    text=zoText,
    font=\small
  },
  zo point label/.style={
    text=zoText,
    font=\small
  },
  zo tick label/.style={
    text=zoText,
    font=\footnotesize
  },
  zo reference label/.style={
    text=zoText,
    font=\small
  },
  zo legend label/.style={
    text=zoText,
    font=\small
  },
  zo auxiliary label/.style={
    text=zoText,
    font=\small
  }
}

% END ZO MATH GRAPH STYLE
```

`zoGraphStrong` là đỏ đậm dành cho điểm hoặc đoạn của đối tượng chính cần nhấn mạnh. `zoGraphSecondary` là vàng nâu dành cho đường cong phụ. `zoReference` dùng cùng mã màu với đường phụ nhưng mang kiểu nét và độ dày riêng cho đường tham chiếu; không dùng ba tên này thay thế lẫn nhau.

### 15.2. Khung tệp hoàn chỉnh

Khung dưới đây cho thấy đúng vị trí của khối style chuẩn trong một tệp tự đầy đủ. Phải tính lại đường dẫn `assets/fonts/` từ thư mục chứa tệp nguồn trước khi biên dịch.

```tex
\documentclass[tikz,border=3pt,10pt]{standalone}

\usepackage{fontspec}
\usepackage{unicode-math}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}

\setmainfont{STIXTwoText-Regular.otf}[
  Path=../../../../../../assets/fonts/,
  BoldFont=STIXTwoText-Bold.otf,
  ItalicFont=STIXTwoText-Italic.otf,
  BoldItalicFont=STIXTwoText-BoldItalic.otf
]
\setmathfont{STIXTwoMath.otf}[Path=../../../../../../assets/fonts/]

% Chỉ nạp các thư viện thực sự cần.
% \usepgfplotslibrary{fillbetween}
\usetikzlibrary{backgrounds}

% Chép nguyên khối style chuẩn ở Mục 15.1 vào đây.

% Khai báo macro, dữ liệu và style riêng của hình ở đây.

\begin{document}
\begin{tikzpicture}[zo graph field]
  \begin{axis}[
    zo axis,
    xmin=-4,
    xmax=4,
    ymin=-3,
    ymax=5
  ]
    % Nền và miền tô
    % Đường tham chiếu và tiệm cận
    % Đường cong phụ
    % Đường cong chính
    % Điểm đặc biệt
    % Nhãn: khai báo trực tiếp at, anchor và độ dịch chuyển theo hình này
  \end{axis}
\end{tikzpicture}
\end{document}
```

Khung trên không phải tệp để thay công thức một cách máy móc. AI phải xác định trục, vạch chia, vị trí nhãn, thư viện, phương pháp dựng và các khai báo riêng phù hợp với từng hình. Nếu thiếu một trong năm tệp phông đã khai báo, AI phải dừng và báo lỗi; không được âm thầm thay bằng phông khác.

## 16. Style trong tệp nguồn, macro và cách đặt tên

Mỗi tệp đồ thị phải chứa nguyên khối style chuẩn của Mục 15.1. Không được đặt vị trí của $x$, $y$, $O$, nhãn số, nhãn điểm hoặc nhãn đường cong vào khối chuẩn: các vị trí ấy phụ thuộc miền quan sát và phải chỉnh trong chính tệp nguồn sau khi xem bản render.

Tên style riêng của hình phải mô tả vai trò, không mô tả hình thức tức thời; dùng `zo tangent segment`, không dùng `gray dashed line`. Style riêng được khai báo sau khối chuẩn, không được định nghĩa lại tên đã có và không được làm thay đổi ý nghĩa ngữ nghĩa của màu chuẩn.

Các giá trị chuẩn của phiên bản này đã được mã hóa trực tiếp trong khối style:

| Vai trò                    |     Giá trị chuẩn |
| -------------------------- | ----------------: |
| Đường cong chính           |           `1.2pt` |
| Đường cong phụ             |           `0.9pt` |
| Trục                       |           `0.8pt` |
| Tiệm cận                   |           `0.8pt` |
| Đường phụ trợ, đường chiếu |           `0.6pt` |
| Lưới chính                 |          `0.35pt` |
| Điểm đặc biệt thông thường | `mark size=2.2pt` |
| Điểm cần nhấn mạnh         | `mark size=2.8pt` |
| Điểm phụ trợ               | `mark size=1.7pt` |

Trong từng hình, không sửa trực tiếp các giá trị bên trong khối chuẩn. Nếu cấu trúc toán học hoặc điều kiện hiển thị thật sự đòi hỏi một ngoại lệ, khai báo một style riêng có tên ngữ nghĩa sau khối chuẩn và ghi ngắn gọn lý do ngay trong mã. Nếu cùng một ngoại lệ xuất hiện có hệ thống ở nhiều hình, ghi nhận để xem xét trong lần nâng phiên bản quy chuẩn; không âm thầm tạo một bản khối chuẩn khác.

Một giá trị toán học được dùng nhiều lần hoặc cần thay đổi đồng bộ có thể đặt thành macro, chẳng hạn tham số, tọa độ đặc biệt hoặc ngưỡng chia miền.

Không tạo macro cho một giá trị chỉ xuất hiện một lần và không giúp mã rõ hơn. Không giấu công thức cốt lõi sau nhiều lớp macro khiến việc kiểm tra toán học khó khăn.

Tên phải viết bằng tiếng Anh không dấu trong mã, ngắn nhưng biểu đạt đúng vai trò. Không dùng các tên như `style1`, `line2`, `colorA` hoặc `temp` trong tệp bàn giao.

Các khoảng lấy mẫu và lý do chia nhánh đặc biệt phải có chú thích ngắn ngay tại mã khi ý nghĩa không hiển nhiên.

Không được gọi một tên style chỉ vì tên đó xuất hiện trong văn xuôi của quy chuẩn hoặc được dự kiến sẽ có. Trước khi dùng, AI phải kiểm tra style đã thực sự được định nghĩa trong khối chuẩn đã nhúng hoặc trong phần khai báo riêng của chính tệp nguồn.

Nếu một vai trò chưa có trong khối chuẩn, phải khai báo rõ style riêng trong tệp nguồn trước khi dùng. Không tự sửa tài liệu quy chuẩn trong phạm vi nhiệm vụ tạo một hình, và không để PGF/TikZ âm thầm bỏ qua một style không tồn tại rồi vẫn coi PDF được tạo là kết quả đạt.

## 17. Phông chữ và khả năng tương thích

Mọi tệp đồ thị độc lập phải dùng LuaLaTeX, `fontspec` và `unicode-math`. Phông được nạp trực tiếp từ các tệp OTF trong repository:

- chữ thường: `assets/fonts/STIXTwoText-Regular.otf`;
- chữ đậm: `assets/fonts/STIXTwoText-Bold.otf`;
- chữ nghiêng: `assets/fonts/STIXTwoText-Italic.otf`;
- chữ đậm nghiêng: `assets/fonts/STIXTwoText-BoldItalic.otf`;
- công thức toán: `assets/fonts/STIXTwoMath.otf`.

Không dùng các tệp `.woff2` cho LuaLaTeX, không phụ thuộc vào phông đã cài trên hệ điều hành và không thay STIX bằng Computer Modern, Latin Modern hoặc một phông gần giống. Đường dẫn tới `assets/fonts/` phải được tính từ thư mục chứa tệp nguồn. Với vị trí chuẩn hiện tại `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_figures/tikz/`, tiền tố là `../../../../../../`. Nếu vị trí nguồn thay đổi, AI phải tính lại tiền tố trước khi bàn giao; không đổi quy trình biên dịch quen thuộc của repository chỉ để làm cho một đường dẫn sai trở nên chạy được.

Cỡ chữ nền là `10pt`; nhãn trục dùng `\normalsize`, nhãn điểm và nhãn đường cong dùng `\small`, số trên vạch chia và chú thích phụ rất ngắn dùng `\footnotesize`. Chữ phải còn đọc được sau khi hình được co về chiều rộng xuất bản. Không dùng `\scriptsize` làm mặc định.

## 18. Ngoại lệ toán học và kỹ thuật

### 18.1. Đầu mút thuộc tập xác định

Nếu hàm chỉ xác định trên một đoạn hoặc nửa khoảng, phải biểu diễn đúng đầu mút và không dùng mũi tên làm người đọc tưởng đồ thị còn tiếp tục.

### 18.2. Điểm khuyết và giá trị được gán lại

Nếu giới hạn tồn tại nhưng hàm không xác định tại điểm đó, vẽ điểm rỗng. Nếu hàm được gán một giá trị khác tại cùng hoành độ, vẽ thêm điểm đặc tại giá trị thật. Không nối hai điểm bằng một đoạn đứng.

### 18.3. Nhánh vượt cửa sổ quan sát

Đường cong phải bị cắt tự nhiên tại biên. Không thêm mũi tên vào mọi chỗ đường cong chạm mép; chỉ dùng mũi tên khi cần diễn đạt hướng tiếp tục và khi nó không gây nhầm với vector hoặc tiếp tuyến.

### 18.4. Hàm có giá trị rất lớn hoặc rất nhỏ

Không mở rộng miền $y$ đến mức phần hữu ích của hình bị nén. Dùng cửa sổ quan sát thích hợp, chia nhánh và giới hạn kỹ thuật có kiểm soát.

### 18.5. Hàm tuần hoàn

Chọn số chu kỳ vừa đủ để thấy quy luật, thường tập trung quanh một chu kỳ chuẩn hoặc một vài chu kỳ khi cần nhấn mạnh tính lặp. Biên và vạch chia phải biểu diễn chính xác theo chu kỳ.

### 18.6. Hàm gần trùng với trục hoặc đường tham chiếu

Điều chỉnh thứ tự lớp, độ đậm hoặc kiểu nét để cả hai còn đọc được. Không dịch chuyển đường cong khỏi tọa độ thật chỉ để nhìn rõ.

### 18.7. Chồng nhãn

Ưu tiên đổi vị trí nhãn hoặc giảm số nhãn. Không giảm toàn bộ cỡ chữ xuống dưới ngưỡng đọc được để giữ mọi chú thích.

## 19. Biên dịch và render

Mọi đồ thị phải đi hết chuỗi kiểm định bắt buộc:

```text
.tex → PDF → SVG → Quarto HTML
```

Tệp `.tex` được biên dịch bằng LuaLaTeX tại thư mục chứa nguồn, theo quy trình VS Code đang dùng trong repository. PDF là sản phẩm trung gian để kiểm tra việc biên dịch; SVG được nhúng trong trang Quarto và hiển thị trong HTML mới là sản phẩm cuối cần duyệt. Không chạy từ gốc repository theo cách làm phát sinh `.aux`, `.log` hoặc `.pdf` ở gốc. Nếu repository có script dựng hình hoặc chuyển đổi đã được quy định, phải dùng script đó thay vì tạo một quy trình riêng. Tên công cụ và câu lệnh chuyển PDF sang SVG chỉ được bổ sung sau khi xác định đúng công cụ đang vận hành trong ZO Math.

Ít nhất phải xác nhận:

- tệp `.tex` biên dịch với mã thoát thành công;
- log không có lỗi;
- không có cảnh báo quan trọng về nhãn, phông, bounding box hoặc đường dẫn dữ liệu;
- PDF được tạo đúng;
- SVG được chuyển đổi thành công, không mất chữ, không thay phông, không cắt nét và giữ nguyên màu, độ dày cùng hình học;
- trang Quarto đại diện render HTML thành công và hình đọc được ở kích thước sử dụng thực tế trên desktop lẫn mobile;
- tệp xuất không chứa khoảng trắng bất thường hoặc đối tượng ngoài ý muốn.

Không được coi việc biên dịch thành công là đủ. AI phải xem bản render.

PGFPlots có thể trì hoãn việc xử lý một số tọa độ cho đến `\end{axis}`. Không để tọa độ trong đường vẽ phụ thuộc trực tiếp vào biến cục bộ của `\foreach` nếu biến ấy có thể hết phạm vi trước khi PGFPlots xử lý đường dẫn.

Với một số lượng nhỏ tọa độ đặc biệt, ưu tiên viết tường minh. Nếu dùng vòng lặp, phải mở rộng và đóng băng đầy đủ giá trị tọa độ ngay trong từng lượt trước khi giao đường dẫn cho PGFPlots.

## 20. Tự kiểm tra bản render

AI phải kiểm tra cả PDF độc lập, SVG sau chuyển đổi và SVG trong trang Quarto ở kích thước thực tế của bài viết, không chỉ ở mức phóng to. Việc kiểm tra gồm:

### 20.1. Đúng toán học

- công thức và miền đúng;
- các nhánh không bị nối qua điểm không xác định;
- nghiệm, cực trị, điểm uốn, điểm gián đoạn và tiệm cận nằm đúng vị trí;
- điểm đặc và điểm rỗng đúng trạng thái;
- miền tô và quan hệ bất đẳng thức đúng;
- vạch chia và nhãn giá trị chính xác;
- đường cong không có góc, đoạn thẳng hoặc dao động giả do lấy mẫu.

### 20.2. Đúng thị giác

- đường cong chính nổi bật vừa đủ;
- trục và lưới không lấn át dữ liệu;
- các kiểu nét còn phân biệt khi thu nhỏ;
- điểm rỗng còn nhìn thấy lõi;
- nhãn không đè nhau, không đè đường và không bị cắt;
- nhãn công thức có quan hệ thị giác rõ với đúng đường cong, không lơ lửng ở vùng không xác định và không nằm đúng điểm cắt giả tạo của cửa sổ quan sát;
- đặc điểm quan trọng không quá sát mép;
- không có khoảng trống vô nghĩa quá lớn;
- tỉ lệ khung không làm sai cảm nhận về hình dạng cần truyền đạt;
- màu đúng mã và đủ tương phản;
- lề ngoài và bounding box cân đối.

### 20.3. Đúng kỹ thuật

- không có đối tượng vô hình làm mở rộng bounding box;
- không có dữ liệu hoặc tệp thử nghiệm còn sót;
- không có đường dẫn tuyệt đối;
- không có thư viện hoặc gói thừa;
- mã có cấu trúc, tên ngữ nghĩa và chú thích vừa đủ;
- PDF và SVG có cùng miền quan sát, vị trí nhãn và hình học.

Nếu bất kỳ mục nào không đạt, AI phải sửa tệp và lặp lại quá trình biên dịch–render–kiểm tra.

Log không có `Package pgfkeys Error`, `Undefined control sequence` hoặc cảnh báo cho biết một style, màu hay khóa không tồn tại. Việc PDF vẫn được tạo không chứng minh rằng mọi đối tượng đã được vẽ.

## 21. Tiêu chí nghiệm thu

Một tệp chỉ được bàn giao khi đáp ứng đồng thời:

1. người đọc nhận ra ngay đối tượng và đặc điểm chính mà hình muốn truyền đạt;
2. không có sai lệch toán học do miền, chia nhánh, lấy mẫu hoặc cách đánh dấu;
3. hình nhất quán với hệ màu và phân cấp thị giác ZO Math;
4. hình chuẩn có nền vàng rất nhạt, khung bo góc nhẹ, trục hai đầu mũi tên và không có lưới nếu lưới không phục vụ một thông tin toán học cụ thể;
5. tệp độc lập, rõ cấu trúc, không phụ thuộc ngầm vào tài liệu khác;
6. biên dịch bằng LuaLaTeX theo quy trình thực tế của repository;
7. bản PDF và SVG tương đương về nội dung, phông, màu, độ dày, nhãn và hình học;
8. SVG nhúng trong Quarto HTML đọc được ở kích thước xuất bản thực tế trên desktop và mobile;
9. mọi ngoại lệ so với mặc định đều có lý do từ bản chất toán học hoặc mục đích của hình.

## 22. Cách bàn giao

Khi hoàn tất, AI phải báo ngắn gọn:

- đường dẫn tệp `.tex` đã tạo hoặc sửa;
- đối tượng và mục đích chính của hình;
- lệnh hoặc quy trình đã dùng để kiểm tra;
- kết quả biên dịch và kiểm tra render;
- ngoại lệ đáng kể so với mặc định, nếu có.

Không cần thuật lại toàn bộ quá trình suy luận. Nếu còn một giới hạn biểu diễn không thể loại bỏ, phải nêu rõ giới hạn đó thay vì âm thầm bàn giao một hình có thể gây hiểu sai.

## 23. Chỉ dẫn rút gọn có thể giao trực tiếp cho AI

> Hãy tạo tệp `.tex` tự đầy đủ bằng TikZ/PGFPlots cho đồ thị được yêu cầu. Trước khi viết mã, hãy phân tích tập xác định, các nhánh liên tục, giới hạn, gián đoạn, tiệm cận, nghiệm, cực trị, đối xứng, tuần hoàn và hành vi lấy mẫu có liên quan. Chỉ đưa vào hình những thành phần phục vụ mục đích toán học. Dùng LuaLaTeX, `fontspec`, `unicode-math` và nạp trực tiếp STIX Two Text, STIX Two Math từ `assets/fonts/`; không dùng phông dự phòng. Chép nguyên khối style chuẩn ở Mục 15.1 vào tệp, không nạp style từ tệp bên ngoài và không sửa giá trị bên trong khối. Đồ thị chuẩn phải nằm trong trường nền vàng rất nhạt `FFF9E9`, có viền ấm `DFD7CA` mảnh và bo góc nhẹ; đường cong chính dùng `EF5350`; trục dùng `554F48`, có mũi tên ở cả hai đầu khi tiếp tục theo hai hướng; chỉ đầu dương mang nhãn $x$, $y$. Mọi vị trí nhãn trục, nhãn số và nhãn đồ thị phải được thiết lập trong chính tệp nguồn rồi điều chỉnh sau khi xem bản render để tránh va chạm; không bật lưới nếu lưới không giúp đọc một thông tin toán học cụ thể. Dùng kích thước mặc định `12cm × 7.5cm`, khai báo tường minh miền quan sát, phân biệt tập xác định–miền lấy mẫu–miền quan sát, chia nhánh tại mọi điểm không xác định và không lấy mẫu xuyên qua tiệm cận. Tệp dùng `standalone` với `border=3pt`, cỡ chữ nền `10pt`, `scale only axis`, `enlargelimits=false`, `clip=true` và `clip mode=individual`, trừ khi bản chất hình đòi hỏi một ngoại lệ đã được giải thích. Sau khi tạo, đưa hình qua đầy đủ chuỗi `.tex → PDF → SVG → Quarto HTML`, kiểm tra ở kích thước sử dụng thực tế trên desktop và mobile, rồi tự sửa cho đến khi đạt mới bàn giao.

## 24. Kế hoạch kiểm nghiệm và điều kiện khóa phiên bản

Phiên bản 02 xác lập tài liệu này là nguồn chuẩn duy nhất của style đồ thị: mỗi tệp `.tex` phải nhúng nguyên khối style ở Mục 15.1; mọi vị trí nhãn được quyết định trong chính tệp nguồn. Bản này vẫn đang kiểm nghiệm chuỗi render và nhóm hàm đại diện; chưa khóa thành bản chính thức trước khi hoàn thành vòng kiểm nghiệm dưới đây.

### 24.1. Nhóm hàm đại diện bắt buộc

| Hàm số             | Năng lực cần kiểm tra                                                              |
| ------------------ | ---------------------------------------------------------------------------------- |
| $y=x^2$            | Trục, tỉ lệ, nhãn, điểm đặc biệt và đường cong trơn cơ bản                         |
| $y=1/x$            | Hai nhánh, điểm gián đoạn, tiệm cận và miền lấy mẫu tách rời                       |
| $y=\lvert x\rvert$ | Điểm gãy, sự nối nét và tính đối xứng                                              |
| $y=\sin x$         | Vạch chia theo $\pi$, nhãn toán học và tính tuần hoàn                              |
| $y=\sin(1/x)$      | Loại $0$ khỏi tập xác định, dao động dày, chiến lược lấy mẫu và giới hạn biểu diễn |

### 24.2. Trình tự kiểm nghiệm

1. Tạo năm tệp `.tex` tự đầy đủ, mỗi tệp nhúng nguyên khối style chuẩn ở Mục 15.1 và không nạp style từ tệp bên ngoài.
2. Trong từng tệp, đặt trực tiếp nhãn trục, nhãn số và các nhãn khác theo miền quan sát của chính hình đó.
3. Đưa từng tệp qua đầy đủ chuỗi `.tex → PDF → SVG → Quarto HTML`.
4. Duyệt PDF và SVG độc lập; sau đó duyệt trang Quarto ở kích thước xuất bản thực tế trên desktop và mobile.
5. Ghi lại mọi lỗi và ngoại lệ; phân biệt lỗi có tính hệ thống của quy chuẩn với va chạm cục bộ cần sửa trong riêng tệp nguồn.
6. Phản hồi những phát hiện có tính hệ thống vào bản quy chuẩn; không biến một hiệu chỉnh vị trí riêng thành quy tắc chung.
7. Tạo lại các hình bị ảnh hưởng và kiểm tra lại toàn bộ nhóm đại diện.

### 24.3. Nội dung phải được đánh giá sau khi có ảnh thật

- độ dày `1.2pt`, `0.9pt`, `0.8pt`, `0.6pt`, `0.35pt` có tạo đúng phân cấp hay không;
- các kích thước điểm `2.2pt`, `2.8pt`, `1.7pt` có còn rõ khi thu nhỏ hay không;
- đầu mũi tên mặc định do `<->` tạo ra có cân với trục hay không;
- hệ cỡ chữ `10pt`, `\normalsize`, `\small`, `\footnotesize` có đọc tốt trên desktop và mobile hay không;
- mã tự chứa có đủ rõ để một AI khác tạo hình chỉ từ quy chuẩn này hay không;
- SVG có bảo toàn STIX, màu, nét, nhãn, bounding box và hình học của PDF hay không;
- quy chuẩn có hướng dẫn đủ rõ cho trường hợp nhiều nhánh, điểm gãy, tuần hoàn và dao động dày hay không.

### 24.4. Điều kiện khóa phiên bản

Chỉ khóa bản chính thức khi cả năm đồ thị vượt qua chuỗi kiểm định, các lỗi và ngoại lệ đã được phản hồi vào quy chuẩn, và các hình bị ảnh hưởng đã được tạo lại để xác nhận. Tên công cụ cùng câu lệnh PDF → SVG và render Quarto phải được bổ sung theo đúng công cụ thực tế đã dùng trong vòng kiểm nghiệm; không ghi một lệnh giả định.
