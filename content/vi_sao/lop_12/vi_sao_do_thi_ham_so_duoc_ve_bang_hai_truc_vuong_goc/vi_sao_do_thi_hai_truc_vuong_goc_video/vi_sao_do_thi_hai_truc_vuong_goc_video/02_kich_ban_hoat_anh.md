---
title: "Vì sao đồ thị hàm số được vẽ bằng hai trục vuông góc?"
series: "Vì sao?"
project: "ZO Math"
script_type: "Kịch bản hoạt ảnh"
visual_style: "Trời sao kiến tạo học thuật"
visual_variant: "Hoạt ảnh Vì sao?"
voiceover_script: "01_kich_ban_loi_dan.md"
version: "v0.1"
status: "Nháp sản xuất"
updated: "2026-06-26"
---

# VÌ SAO ĐỒ THỊ HÀM SỐ ĐƯỢC VẼ BẰNG HAI TRỤC VUÔNG GÓC?

### KỊCH BẢN HOẠT ẢNH

## 0. Nguyên tắc dựng cho video này

Hoạt ảnh không minh họa lại từng câu lời dẫn.

Hoạt ảnh dựng một con đường nhìn thấy được: từ bảng số, đến mốc $x$, đến đoạn biểu diễn $y$, đến điểm $(x,y)$, đến đường cong, rồi đến hệ hai trục vuông góc.

Trong phần kiến tạo, đối tượng nào chưa có lý do thì chưa xuất hiện.

Vì vậy:

- C01 được phép cho thấy hình ảnh đồ thị quen thuộc như một hình ảnh cần đặt lại câu hỏi.

- Từ C02 trở đi, sau khi quay về tình huống chưa có hình vẽ, đồ thị hoàn chỉnh không được hiện sẵn.

- C02 chưa có trục.
- C03 mới có trục x.
- C04 mới có điểm và đường cong.
- C05 mới có trục y và gốc chung.
- C06 mới gọi lại đồ thị như hình ảnh tổng thể của sự biến thiên.

Mọi chữ văn bản trên màn hình viết in hoa.  
Công thức toán học giữ hình thức toán học riêng, viết bằng LaTeX.

Dữ liệu dùng trong toàn video:

```python
x_values = [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]

y_values = [-8.125, -2.0, 1.125, 2.0, 1.375, 0.0, -1.375, -2.0, -1.125, 2.0, 8.125]
```

Màu gợi ý theo vai trò cục bộ:

```text
COLOR_PRIMARY   = nội dung chính, công thức, điểm đang xét
COLOR_SECONDARY = nội dung phụ còn rõ
COLOR_MUTED     = nhãn phụ, số cảnh, ghi chú
COLOR_GUIDE     = đường phụ, khung, mốc
COLOR_FAINT     = phần đã lùi, dữ liệu nền
```

Màu nhấn chỉ có nghĩa trong video này.  
Không xem các màu trên là quy ước vĩnh viễn cho mọi bài.

## C01. TỰ VẤN

### Mục tiêu hoạt ảnh

Biến hình ảnh đồ thị quen thuộc thành một vấn đề cần được hiểu.

Cảnh này được phép hiện các đồ thị quen thuộc vì lời dẫn bắt đầu từ điều đã quá quen.
Nhưng các đồ thị ấy chỉ giữ vai trò đối tượng bị chất vấn, không phải kết quả được kiến tạo.

Hình ảnh mở đầu là một tấm bảng nhỏ gồm nhiều đồ thị khác nhau.
Chúng khác nhau về đường biểu diễn, nhưng đều chia sẻ một cấu trúc quen thuộc: khung vẽ, trục ngang, trục dọc, và một đường nằm trên hệ trục ấy.

Cuối cảnh, toàn bộ hình ảnh quen thuộc phải được xóa khỏi màn hình để chuẩn bị quay về tình huống ban đầu: chỉ còn hàm số, giá trị $x$, giá trị $y$.

### Khung định danh cảnh

```text
01
TỰ VẤN
```

Số `01` dùng `FONT_SIZE_LABEL`, màu `COLOR_MUTED`.
Tên cảnh dùng `FONT_SIZE_TITLE`, màu `COLOR_PRIMARY`.

Âm thanh: `whoosh` rất nhẹ khi khung định danh hiện ra.

### Đối tượng được phép xuất hiện

```text
một tấm bảng 3 × 3 gồm các đồ thị quen thuộc
các khung vuông nhỏ
các trục ngang và trục dọc trong mỗi khung
các đường biểu diễn hàm số khác nhau
câu hỏi chính
công thức y = x^3 - 3x
một cụm số rời rạc gợi sự khó nhìn
```

### Đối tượng chưa được phép giữ lại sau cảnh

```text
tấm bảng 3 × 3 các đồ thị
hệ trục hoàn chỉnh
đường cong hoàn chỉnh
định nghĩa đồ thị
các điểm (x,y) như đối tượng đã kiến tạo
```

### Diễn tiến hoạt ảnh

#### Pha 1. Tấm bảng các đồ thị quen thuộc xuất hiện

Trên nền tối, một ô đồ thị nhỏ xuất hiện ở giữa màn hình.

Trong ô ấy, một khung vuông mảnh được dựng lên.
Bên trong khung, một trục ngang và một trục dọc xuất hiện, cắt nhau tại trung tâm.
Một đường biểu diễn đơn giản được vẽ vào trong ô.

Ô đầu tiên lùi về vị trí của nó trong một lưới `3 × 3`.

Tám ô còn lại lần lượt xuất hiện.
Mỗi ô có cùng cấu trúc:

```text
KHUNG VUÔNG
HAI TRỤC VUÔNG GÓC
MỘT ĐƯỜNG BIỂU DIỄN
```

Các đường biểu diễn có hình dạng khác nhau: đường hằng ($y=1$), đường thẳng ($y=x$), parabol ($y=x^2$), đường bậc ba ($y=\frac{1}{3}x^3-x$), đường bậc bốn ($y=\frac{1}{4}x^4 - \frac{1}{2}x^2$), hyperbol ($y=\frac{1}{x}$ và $y=x+\frac{1}{x}$), hàm mũ ($y=e^x$), logarit ($y=\ln(x)$).

Không giải thích từng hàm.
Không ghi công thức cho từng ô.
Không yêu cầu người xem đọc từng đồ thị.

Khi đủ 9 ô, toàn bộ lưới được giữ lại trong một nhịp ngắn.
Người xem thấy nhiều đồ thị khác nhau, nhưng tất cả đều chia sẻ cùng một hình thức quen thuộc: hai trục vuông góc và một đường biểu diễn.

Chữ trên màn hình:

```text
MỘT HÌNH ẢNH QUÁ QUEN
```

Chữ đặt thấp, nhỏ, màu `COLOR_MUTED`.

Hoạt ảnh tương ứng với C01-01 và C01-02.

#### Pha 2. Mẫu số chung của các đồ thị được làm nổi

Toàn bộ lưới `3 × 3` hơi mờ xuống.

Một ô ở giữa, hoặc một ô đại diện, được giữ sáng hơn.
Trong ô ấy, trục ngang được nhấn nhẹ.
Sau đó trục dọc được nhấn nhẹ.
Cuối cùng đường biểu diễn được nhấn nhẹ.

Các chữ ngắn xuất hiện lần lượt, không hiện cùng lúc:

```text
MỘT TRỤC NGANG
MỘT TRỤC DỌC
HAI TRỤC VUÔNG GÓC
MỘT ĐƯỜNG CONG
```

Sau mỗi dòng, chữ mờ xuống để nhường chỗ cho dòng tiếp theo.

Mục đích của pha này không phải giải thích.
Pha này chỉ gom sự chú ý vào điều quá quen: hễ nói đến đồ thị hàm số, ta thường hình dung ngay một hệ trục vuông góc và một đường nằm trên đó.

Hoạt ảnh tương ứng với C01-01 và C01-02.

#### Pha 3. Điều quen thuộc bị làm chậm lại

Tấm bảng 9 đồ thị lùi xuống độ mờ.

Các cụm chữ lần lượt hiện ở xung quanh, không chen dày:

```text
THẦY CÔ VẼ NHƯ VẬY
SÁCH GIÁO KHOA VẼ NHƯ VẬY
BÀI GIẢI CŨNG VẼ NHƯ VẬY
```

Sau đó ba cụm chữ mờ đi.

Ở giữa màn hình hiện câu:

```text
QUEN KHÔNG CÓ NGHĨA LÀ ĐÃ HIỂU
```

Âm thanh: `typing` nhẹ cho câu chính.
Không dùng `hit`.

Hoạt ảnh tương ứng với C01-02 và C01-03.

#### Pha 4. Thủ tục được tách thành ba bước

Tấm bảng 9 đồ thị biến mất dần.

Hiện ba dòng chữ theo cột dọc:

```text
LẬP BẢNG GIÁ TRỊ
CHẤM VÀI ĐIỂM
NỐI THÀNH ĐƯỜNG CONG
```

Mỗi dòng hiện ra bằng `play_type_text()`.

Sau khi hiện đủ, cả ba dòng bị đặt trong một khung mờ với nhãn:

```text
THỦ TỤC
```

Khung này không nổi mạnh.
Nó chỉ cho thấy: nếu không hỏi vì sao, đồ thị dễ bị hiểu như một chuỗi thao tác quen tay.

Hoạt ảnh tương ứng với C01-03.

#### Pha 5. Câu hỏi chính

Khung `THỦ TỤC` lùi xuống.

Ba câu hỏi hiện lần lượt, mỗi câu một nhịp:

```text
VÌ SAO TA LẠI LÀM NHƯ VẬY?
VÌ SAO PHẢI CÓ HAI TRỤC?
VÌ SAO HAI TRỤC ẤY LẠI VUÔNG GÓC?
```

Câu thứ ba dùng `FONT_SIZE_TITLE` hoặc `FONT_SIZE_EMPHASIS * 0.75`.
Màu ưu tiên `COLOR_PRIMARY`.
Chỉ dùng `COLOR_ZO_RED` nếu muốn đánh dấu đây là câu hỏi trung tâm của toàn video.

Âm thanh: `hit` rất nhẹ ở câu hỏi thứ ba.

Hoạt ảnh tương ứng với C01-04 và C01-05.

#### Pha 6. Xóa hình quen thuộc, quay về dữ liệu ban đầu

Toàn bộ câu hỏi mờ đi.

Màn hình trở về trạng thái sạch.

Ở giữa màn hình hiện công thức:

$$
y = x^3 - 3x
$$

Bên dưới công thức, các giá trị $x$ rời rạc xuất hiện như một hàng số:

```text
-2.5  -2.0  -1.5  ...  2.5
```

Chưa có trục.
Chưa có bảng đầy đủ.
Chưa có điểm.
Chưa có đường cong.

Chỉ là các con số đặt trên màn hình.

Sau đó, một vài giá trị $y$ tương ứng xuất hiện rải rác, chưa tổ chức thành bảng hoàn chỉnh.
Các con số đủ nhiều để tạo cảm giác khó nhìn, nhưng không dày đến mức người xem phải đọc chúng.

Chữ kết cảnh:

```text
CẦN NHÌN THẤY Y THAY ĐỔI KHI X THAY ĐỔI
```

Cuối cảnh, các số rời rạc mờ đi một phần, chỉ giữ lại cảm giác rằng bảng số sắp được hình thành ở cảnh sau.

Hoạt ảnh tương ứng với C01-06 đến C01-08.

### Chữ trên màn hình

```text
MỘT HÌNH ẢNH QUÁ QUEN
MỘT TRỤC NGANG
MỘT TRỤC DỌC
HAI TRỤC VUÔNG GÓC
MỘT ĐƯỜNG CONG
QUEN KHÔNG CÓ NGHĨA LÀ ĐÃ HIỂU
THỦ TỤC
VÌ SAO TA LẠI LÀM NHƯ VẬY?
VÌ SAO PHẢI CÓ HAI TRỤC?
VÌ SAO HAI TRỤC ẤY LẠI VUÔNG GÓC?
CẦN NHÌN THẤY Y THAY ĐỔI KHI X THAY ĐỔI
```

### Âm thanh

```text
whoosh = hiện tấm bảng đồ thị quen thuộc, chuyển sang dữ liệu ban đầu
typing = các câu hỏi và câu kết cảnh
hit    = câu hỏi chính cuối cùng
```

Âm thanh dùng rất nhẹ.
Không tạo cảm giác mở màn kịch tính.

### Ghi chú Manim

Helper dự kiến:

```python
clear_screen()
make_text()
make_text_block()
make_math()
make_frame()
play_type_text()
play_focus()
play_dim()
```

Đối tượng gợi ý:

```python
graph_gallery
graph_cell
cell_frame
cell_axes
cell_curve
representative_graph
procedure_steps
procedure_frame
main_questions
formula_tex
raw_x_values
raw_y_values
```

Cấu trúc tấm bảng gợi ý:

```text
graph_gallery = lưới 3 × 3

mỗi graph_cell gồm:
- cell_frame
- cell_axes
- cell_curve
```

Các đồ thị trong `graph_gallery` không cần chính xác tuyệt đối như một bài khảo sát hàm số.
Chúng chỉ cần gợi đúng các hình quen thuộc: hằng, tuyến tính, parabol, bậc ba, bậc bốn, phân thức, mũ, logarit.

Điều quan trọng là mọi ô đều chia sẻ cùng một hình thức thị giác: khung nhỏ, hai trục vuông góc, một đường biểu diễn.

Sau C01, không dùng lại `graph_gallery`.
Từ C02 trở đi, toàn bộ hình ảnh phải được kiến tạo lại từ dữ liệu ban đầu.

## C02. BIẾN ĐẦU VÀO X VÀ BIẾN PHỤ THUỘC Y

### Mục tiêu hoạt ảnh

Đặt người xem vào tình huống ban đầu: có một công thức, có các giá trị $x$ được chọn, và có các giá trị $y$ được trả lại.

Cảnh này làm rõ hai vai trò:

```text
X = GIÁ TRỊ ĐƯA VÀO
Y = GIÁ TRỊ TRẢ LẠI
```

Từ bảng số, cảnh làm xuất hiện nhu cầu nhìn thấy sự phụ thuộc của $y$ vào $x$ rõ hơn.

### Khung định danh cảnh

```text
02
BIẾN ĐẦU VÀO X VÀ BIẾN PHỤ THUỘC Y
```

### Đối tượng được phép xuất hiện

```text
công thức y = x^3 - 3x
một khung quy tắc / máy hàm số
một hàng giá trị x
một bảng hai cột x và y
mũi tên biểu thị đưa vào và trả lại
dấu nhấn cho các đoạn tăng, giảm, tăng của y
```

### Đối tượng chưa được phép hiện

```text
trục x
trục y
mặt phẳng tọa độ
điểm (x,y)
đường cong
```

### Diễn tiến hoạt ảnh

#### Pha 1. Công thức như một quy tắc

Hiện công thức ở trung tâm:

$$
y = x^3 - 3x
$$

Sau đó công thức được đặt trong một khung mờ như một “quy tắc”.

Bên trái khung hiện:

```text
X ĐƯA VÀO
```

Bên phải khung hiện:

```text
Y TRẢ LẠI
```

Một giá trị $x$ mẫu đi từ trái vào khung.  
Một giá trị $y$ tương ứng đi ra bên phải.

Không cần dùng hình máy móc vui nhộn.  
Chỉ dùng khung, mũi tên, công thức.

Hoạt ảnh tương ứng với C02-01 đến C02-04.

#### Pha 2. So sánh với thời điểm và nhiệt độ

Công thức lùi xuống.

Hiện một hàng thời điểm:

```text
6 GIỜ   7 GIỜ   8 GIỜ   9 GIỜ
```

Bên dưới, hiện các chấm nhiệt độ không đều nhau về độ cao, nhưng chưa dựng trục.

Chữ:

```text
THỜI ĐIỂM ĐƯỢC CHỌN
NHIỆT ĐỘ ĐƯỢC ĐO
```

Hai dòng này giúp người xem cảm vai trò chọn và nhận.

Sau đó toàn bộ ví dụ nhiệt độ mờ đi để quay về hàm số.

Hoạt ảnh tương ứng với C02-03.

#### Pha 3. Chọn các giá trị x

Hiện một hàng số nằm giữa màn hình, chưa phải trục:

```text
-2.5  -2.0  -1.5  -1.0  -0.5  0  0.5  1.0  1.5  2.0  2.5
```

Một nhịp đều được gợi bằng khoảng cách đều giữa các số.

Chữ nhỏ phía trên:

```text
MỖI LẦN TĂNG 0.5
```

Các số $x$ dùng màu `COLOR_ZO_TEAL` hoặc `COLOR_PRIMARY`.

Hoạt ảnh tương ứng với C02-05 và C02-06.

#### Pha 4. Tạo bảng giá trị

Hàng số $x$ chuyển thành cột trái của bảng.

Cột phải được điền dần từng giá trị $y$:

```text
x       y
-2.5   -8.125
-2.0   -2
-1.5    1.125
-1.0    2
-0.5    1.375
 0      0
 0.5   -1.375
 1.0   -2
 1.5   -1.125
 2.0    2
 2.5    8.125
```

Không cần hiện tất cả dòng quá lớn.  
Có thể dùng bảng gọn, chia hai nửa, hoặc hiển thị 11 dòng với cỡ `FONT_SIZE_DETAIL`/`FONT_SIZE_LABEL`.

Âm thanh: `typing` rất nhẹ khi bảng được điền.

Hoạt ảnh tương ứng với C02-07.

#### Pha 5. Cột x đều, cột y không đều

Cột $x$ được quét nhẹ từ trên xuống, nhấn nhịp đều.

Chữ:

```text
X ĐI ĐỀU
```

Sau đó cột $y$ được nhấn theo ba đoạn:

```text
TĂNG
GIẢM
TĂNG
```

Các nhóm dòng được đóng khung nhẹ:

```text
x: -2.5 → -1      y: -8.125 → 2
x: -1 → 1         y: 2 → -2
x: 1 → 2.5        y: -2 → 8.125
```

Không vẽ đường cong.  
Chỉ cho thấy bảng bắt đầu khó đọc nếu muốn thấy xu hướng.

Hoạt ảnh tương ứng với C02-08 đến C02-10.

#### Pha 6. Nhu cầu biểu diễn khác

Bảng hơi dày lên: các dòng số lặp bóng mờ hoặc tăng độ rối nhẹ.

Ở giữa hiện câu kết cảnh:

```text
BẢNG CHÍNH XÁC
NHƯNG CHƯA CHO THẤY DÁNG ĐIỆU BIẾN THIÊN
```

Sau đó hiện câu:

```text
CẦN MỘT CÁCH BIỂU DIỄN KHÁC
```

Câu cuối là cầu nối sang C03.

Hoạt ảnh tương ứng với C02-11 và C02-12.

### Chữ trên màn hình

```text
X ĐƯA VÀO
Y TRẢ LẠI
THỜI ĐIỂM ĐƯỢC CHỌN
NHIỆT ĐỘ ĐƯỢC ĐO
MỖI LẦN TĂNG 0.5
X ĐI ĐỀU
Y KHÔNG ĐI ĐỀU
BẢNG CHÍNH XÁC
NHƯNG CHƯA CHO THẤY DÁNG ĐIỆU BIẾN THIÊN
CẦN MỘT CÁCH BIỂU DIỄN KHÁC
```

### Âm thanh

```text
typing = điền bảng
tick   = mỗi lần nhấn một dòng hoặc một nhóm giá trị
whoosh = chuyển từ công thức sang bảng, từ bảng sang nhu cầu
```

### Ghi chú Manim

Helper dự kiến:

```python
make_math()
make_text()
make_text_block()
make_frame()
play_type_text()
play_scan_once()
play_focus()
play_dim()
fit_to_width()
```

Đối tượng gợi ý:

```python
function_rule_frame
input_label
output_label
x_value_row
value_table
x_column
y_column
increase_group_left
decrease_group_middle
increase_group_right
need_for_representation
```

## C03. TRỤC THỨ NHẤT: X

### Mục tiêu hoạt ảnh

Bắt đầu chuyển bảng số thành cấu trúc hình học.

Cảnh này chỉ được dựng **trục thứ nhất** và các đoạn biểu diễn $y$ tại từng mốc $x$.

Trục $y$ chưa xuất hiện.  
Đường cong chưa xuất hiện.  
Điểm $(x,y)$ chưa được gọi tên như điểm trên hệ trục hoàn chỉnh.

### Khung định danh cảnh

```text
03
TRỤC THỨ NHẤT: X
```

### Đối tượng được phép xuất hiện

```text
hàng giá trị x
đường ngang
các mốc x trên đường ngang
các đoạn thẳng đứng biểu diễn y
nhãn x
nhãn y cục bộ trên vài đoạn
```

### Đối tượng chưa được phép hiện

```text
trục y
đường cong
hệ trục tọa độ hoàn chỉnh
định nghĩa đồ thị
```

### Diễn tiến hoạt ảnh

#### Pha 1. Từ cột x sang thứ tự ngang

Cột $x$ trong bảng được tách ra khỏi bảng.

Các giá trị $x$ di chuyển từ dạng cột sang một hàng ngang.

Chưa có đường.  
Chỉ có các số được sắp từ trái sang phải.

Sau đó một đường ngang mảnh được vẽ qua các số.  
Các số trở thành mốc trên đường ấy.

Chữ:

```text
GIỮ LẠI THỨ TỰ CỦA X
```

Hoạt ảnh tương ứng với C03-01 và C03-02.

#### Pha 2. Đường ngang được gọi là trục x

Đường ngang sáng hơn một chút.

Nhãn nhỏ hiện bên phải:

```text
X
```

Chữ trên màn hình:

```text
TRỤC X
```

Từ các mốc đã chọn, hiện thêm vài mốc mờ ở giữa để gợi rằng giữa các giá trị đã chọn còn nhiều giá trị khác.

Không làm dày quá.  
Chỉ gợi bằng các vạch nhỏ mờ.

Hoạt ảnh tương ứng với C03-03.

#### Pha 3. Câu hỏi tại từng mốc x

Ở vài mốc $x$, hiện dấu hỏi nhỏ phía trên hoặc ngay gần mốc:

```text
Y = ?
```

Các dấu hỏi hiện lần lượt từ trái sang phải.

Ý nghĩa: tại mỗi mốc $x$, công thức cần trả lại một giá trị $y$.

Hoạt ảnh tương ứng với C03-04.

#### Pha 4. Dựng các đoạn biểu diễn y

Từ từng mốc $x$, dựng một đoạn thẳng đứng.

Nếu $y>0$, đoạn đi lên.  
Nếu $y<0$, đoạn đi xuống.  
Nếu $y=0$, chỉ hiện một chấm hoặc vạch ngắn ngay trên đường ngang.

Các đoạn có độ dài theo tỉ lệ $y$ nhưng được scale để vừa màn hình.

Nên dựng theo `LaggedStart`, từ trái sang phải, nhịp chậm.

Màu gợi ý:

```text
đường ngang / mốc x = COLOR_ZO_TEAL hoặc COLOR_PRIMARY
đoạn y = COLOR_ZO_YELLOW hoặc COLOR_SECONDARY
```

Hoạt ảnh tương ứng với C03-05 và C03-06.

#### Pha 5. Phương dọc giữ nguyên vị trí x

Chọn một mốc $x$ cụ thể, ví dụ $x=1$.

Làm sáng mốc ấy và đoạn $y$ của nó.

Một đường phụ mờ kéo dọc qua mốc đó, nhấn rằng đoạn đi lên/xuống không làm lệch vị trí ngang.

Chữ:

```text
THAY ĐỔI ĐỘ CAO
NHƯNG GIỮ NGUYÊN MỐC X
```

Hoạt ảnh tương ứng với C03-07 và C03-08.

#### Pha 6. Vì sao không dùng phương xiên

Trong một khoảnh khắc ngắn, tại một mốc $x$, hiện vài phương xiên mờ khác nhau.

Các phương xiên này hiện rất nhẹ rồi mờ đi.

Chữ:

```text
PHƯƠNG XIÊN TẠO THÊM LỰA CHỌN TÙY TIỆN
```

Sau đó chỉ giữ lại phương thẳng đứng.

Không biến đoạn này thành tranh luận hình học phức tạp.  
Chỉ cần làm rõ: phương vuông góc là lựa chọn ổn định vì nó giữ mốc $x$.

Hoạt ảnh tương ứng với C03-09 và C03-10.

#### Pha 7. Bảng số đổi thành dấu hiệu hình học

Bảng giá trị mờ hiện bên trái như bóng nền.

Các đoạn thẳng đứng trên trục $x$ hiện ở trung tâm.

Một vài dòng bảng nối mờ tới các đoạn tương ứng.

Chữ kết cảnh:

```text
MỖI CẶP SỐ BẮT ĐẦU TRỞ THÀNH MỘT DẤU HIỆU HÌNH HỌC
```

Hoạt ảnh tương ứng với C03-11 và C03-12.

### Chữ trên màn hình

```text
GIỮ LẠI THỨ TỰ CỦA X
TRỤC X
Y = ?
THAY ĐỔI ĐỘ CAO
NHƯNG GIỮ NGUYÊN MỐC X
PHƯƠNG XIÊN TẠO THÊM LỰA CHỌN TÙY TIỆN
MỖI CẶP SỐ BẮT ĐẦU TRỞ THÀNH MỘT DẤU HIỆU HÌNH HỌC
```

### Âm thanh

```text
whoosh = chuyển cột x thành hàng ngang
tick   = các mốc x xuất hiện
hit    = khi phương thẳng đứng được giữ lại
```

### Ghi chú Manim

Helper dự kiến:

```python
make_text()
make_math()
make_frame()
play_focus()
play_dim()
play_scan_once()
```

Đối tượng gợi ý:

```python
x_value_column
x_value_row
x_axis_line
x_ticks
x_tick_labels
y_question_marks
vertical_y_segments
sample_oblique_guides
table_shadow
geometry_sign_note
```

## C04. ĐIỂM (X,Y) VÀ ĐƯỜNG CONG

### Mục tiêu hoạt ảnh

Từ các đoạn biểu diễn $y$, giữ lại phần thông tin cô đọng nhất: đầu mút.

Các đầu mút trở thành các điểm.  
Các điểm dày dần.  
Đường cong xuất hiện như hình dạng được gợi ra bởi nhiều điểm, không phải như một nét vẽ áp đặt từ đầu.

Trục $y$ vẫn chưa xuất hiện.

### Khung định danh cảnh

```text
04
ĐIỂM (X,Y) VÀ ĐƯỜNG CONG
```

### Đối tượng được phép xuất hiện

```text
trục x đã có
các đoạn y
các đầu mút
các điểm (x,y)
các điểm bổ sung dày hơn
đường cong được tạo từ các điểm
```

### Đối tượng chưa được phép hiện

```text
trục y
gốc chung của hai trục như đối tượng chính thức
định nghĩa đồ thị đầy đủ
```

### Diễn tiến hoạt ảnh

#### Pha 1. Đầu mút được nhận ra

Các đoạn thẳng đứng từ C03 hiện lại.

Đầu mút của mỗi đoạn sáng lên.  
Thân đoạn lùi xuống.

Chữ:

```text
PHẦN CẦN GIỮ LẠI LÀ ĐẦU MÚT
```

Không xóa đoạn ngay.  
Để người xem thấy đầu mút sinh ra từ đoạn.

Hoạt ảnh tương ứng với C04-01 và C04-02.

#### Pha 2. Giữ đầu mút, làm mờ đoạn

Các đoạn dần mờ đi, chỉ còn các đầu mút.

Mỗi đầu mút trở thành một điểm nhỏ.

Một điểm mẫu được nhấn.  
Bên cạnh điểm mẫu hiện nhãn:

$$
(x,y)
$$

Chữ:

```text
MỘT ĐIỂM GIỮ LẠI HAI THÔNG TIN
```

Hoạt ảnh tương ứng với C04-03 và C04-04.

#### Pha 3. Xu hướng hiện ra

Các điểm được nhìn cùng nhau.

Dùng một vệt quét rất nhẹ từ trái sang phải qua dãy điểm.  
Khi quét, các nhóm điểm lần lượt sáng hơn:

```text
ĐI LÊN
QUAY XUỐNG
LẠI ĐI LÊN
```

Không nối điểm bằng đường gấp khúc.  
Chỉ nhấn bằng ánh sáng và vị trí.

Hoạt ảnh tương ứng với C04-05.

#### Pha 4. Cân xứng quanh vị trí trung tâm

Nhấn hai cặp điểm đối xứng:

```text
(-1, 2) và (1, -2)
(-2.5, -8.125) và (2.5, 8.125)
```

Có thể dùng hai đường phụ mờ đi qua vị trí trung tâm để gợi đối xứng tâm, nhưng không cần gọi tên chính thức.

Chữ:

```text
ĐỔI X THÀNH -X
Y CŨNG ĐỔI DẤU
```

Hoạt ảnh tương ứng với C04-06.

#### Pha 5. Khoảng trống giữa các điểm

Các điểm hiện có giữ nguyên.

Khoảng trống giữa hai điểm được làm nổi bằng một vùng mờ hoặc dấu hỏi nhỏ.

Chữ:

```text
GIỮA HAI ĐIỂM THÌ SAO?
```

Sau đó hiện thêm các điểm mới ở giữa các điểm cũ.  
Lần đầu thêm ít điểm.  
Lần sau thêm nhiều hơn.

Các điểm dày dần.

Hoạt ảnh tương ứng với C04-07 đến C04-09.

#### Pha 6. Đường cong xuất hiện

Khi điểm đã đủ dày, một đường cong mảnh đi qua vùng điểm xuất hiện bằng `Create`.

Đường cong không quá sáng ngay.  
Nó sáng dần như hình dạng đã có trong các điểm.

Các điểm cũ mờ đi một phần nhưng không biến mất hoàn toàn ngay.

Chữ kết cảnh:

```text
ĐƯỜNG CONG LÀ DÁNG ĐIỆU CHUNG CỦA SỰ THAY ĐỔI
```

Hoạt ảnh tương ứng với C04-09 và C04-10.

### Chữ trên màn hình

```text
PHẦN CẦN GIỮ LẠI LÀ ĐẦU MÚT
MỘT ĐIỂM GIỮ LẠI HAI THÔNG TIN
ĐI LÊN
QUAY XUỐNG
LẠI ĐI LÊN
ĐỔI X THÀNH -X
Y CŨNG ĐỔI DẤU
GIỮA HAI ĐIỂM THÌ SAO?
ĐƯỜNG CONG LÀ DÁNG ĐIỆU CHUNG CỦA SỰ THAY ĐỔI
```

### Âm thanh

```text
tick   = đầu mút sáng lên
whoosh = các điểm dày dần
hit    = đường cong hiện ra, rất nhẹ
```

### Ghi chú Manim

Helper dự kiến:

```python
play_focus()
play_dim()
play_scan_once()
make_math()
make_text()
```

Đối tượng gợi ý:

```python
vertical_y_segments
endpoint_dots
sample_point_label
trend_groups
symmetric_point_pairs
gap_questions
dense_sample_dots
curve_from_dense_points
```

## C05. TRỤC THỨ HAI: Y

### Mục tiêu hoạt ảnh

Từ đường cong đã hình thành, làm xuất hiện nhu cầu về một thước đo chung cho giá trị $y$.

Trục $y$ không được hiện như một thói quen.  
Nó xuất hiện vì các điểm và đường cong cần một cách đọc độ cao thống nhất.

### Khung định danh cảnh

```text
05
TRỤC THỨ HAI: Y
```

### Đối tượng được phép xuất hiện

```text
trục x đã có
các điểm và đường cong đã hình thành
các đoạn y cục bộ được gọi lại trong chốc lát
thước đo dọc chung
trục y
gốc chung
đường đọc ngang sang trục y
```

### Đối tượng chưa được phép hiện

```text
định nghĩa đồ thị chính thức
khung tọa độ quá đầy đủ ngay từ đầu
```

### Diễn tiến hoạt ảnh

#### Pha 1. Đường cong đã thấy dáng điệu, nhưng chưa đủ để đọc y

Hiện trục $x$, các điểm mờ và đường cong.

Chữ:

```text
ĐÃ THẤY DÁNG ĐIỆU CHUNG
NHƯNG CHƯA CÓ THƯỚC ĐO CHUNG CHO Y
```

Một điểm trên đường cong được chọn.  
Một dấu hỏi nhỏ hiện ngang với độ cao của điểm:

```text
Y = ?
```

Hoạt ảnh tương ứng với C05-01.

#### Pha 2. Không thể giữ mãi các đoạn đứng

Gọi lại các đoạn đứng từ C03 nhưng hiện rất nhiều đoạn mờ, khiến hình trở nên dày.

Sau đó làm mờ chúng nhanh.

Chữ:

```text
QUÁ NHIỀU ĐOẠN SẼ LÀM HÌNH RỐI
```

Tiếp theo, thử hiện nhiều nhãn $y$ nhỏ cạnh các điểm, rồi làm chúng mờ.

Chữ:

```text
QUÁ NHIỀU NHÃN SẼ CHE MẤT HÌNH DẠNG CHÍNH
```

Hoạt ảnh tương ứng với C05-02 và C05-03.

#### Pha 3. Nhu cầu thước đo chung

Ở bên cạnh đường cong, hiện một thước dọc mờ tạm thời.

Các đường ngang mờ từ vài điểm trên đường cong chiếu sang thước dọc ấy.

Chữ:

```text
CẦN MỘT THƯỚC ĐO CHUNG CHO ĐỘ CAO
```

Thước này ban đầu có thể đặt lệch bên trái hoặc bên phải để đặt câu hỏi về vị trí.

Hoạt ảnh tương ứng với C05-04 và C05-05.

#### Pha 4. Thước dọc cần đi qua x = 0

Thước dọc tạm thời được thử ở vài vị trí ngang khác nhau.  
Mỗi vị trí hiện rất nhẹ, rồi mờ.

Sau đó thước dọc di chuyển về mốc $x=0$.

Mốc $x=0$ trên trục ngang sáng lên.

Chữ:

```text
TRỤC DỌC KHÔNG NÊN GẮN VỚI MỘT VỊ TRÍ NGANG TÙY TIỆN
```

Sau đó:

```text
NÓ ĐI QUA MỐC X = 0
```

Hoạt ảnh tương ứng với C05-06 và C05-07.

#### Pha 5. Trục y và gốc chung

Đường dọc qua $x=0$ sáng lên thành trục $y$.

Nhãn nhỏ hiện:

```text
Y
```

Điểm giao với trục $x$ sáng lên.  
Nhãn:

$$
(0,0)
$$

Chữ:

```text
HAI MỐC GẶP NHAU TẠI MỘT GỐC CHUNG
```

Hoạt ảnh tương ứng với C05-08.

#### Pha 6. Đọc một điểm bằng hai thao tác

Chọn một điểm trên đường cong.

Từ điểm ấy, hiện đường phụ dọc xuống trục $x$.  
Sau đó hiện đường phụ ngang sang trục $y$.

Chữ:

```text
NHÌN XUỐNG ĐỂ ĐỌC X
NHÌN SANG ĐỂ ĐỌC Y
```

Không làm thành hệ lưới dày.  
Chỉ dùng một điểm mẫu.

Hoạt ảnh tương ứng với C05-09.

#### Pha 7. Tách bạch hai phương đo

Trên hệ trục, hiện hai mũi tên rất nhẹ:

```text
ĐI NGANG: THAY ĐỔI X
ĐI DỌC: THAY ĐỔI ĐỘ CAO
```

Sau đó hai mũi tên lùi xuống, chỉ giữ lại hệ trục và đường cong.

Chữ kết cảnh:

```text
HAI PHƯƠNG ĐO ĐƯỢC TÁCH BẠCH
```

Hoạt ảnh tương ứng với C05-10 đến C05-13.

### Chữ trên màn hình

```text
ĐÃ THẤY DÁNG ĐIỆU CHUNG
NHƯNG CHƯA CÓ THƯỚC ĐO CHUNG CHO Y
QUÁ NHIỀU ĐOẠN SẼ LÀM HÌNH RỐI
QUÁ NHIỀU NHÃN SẼ CHE MẤT HÌNH DẠNG CHÍNH
CẦN MỘT THƯỚC ĐO CHUNG CHO ĐỘ CAO
TRỤC DỌC KHÔNG NÊN GẮN VỚI MỘT VỊ TRÍ NGANG TÙY TIỆN
NÓ ĐI QUA MỐC X = 0
HAI MỐC GẶP NHAU TẠI MỘT GỐC CHUNG
NHÌN XUỐNG ĐỂ ĐỌC X
NHÌN SANG ĐỂ ĐỌC Y
HAI PHƯƠNG ĐO ĐƯỢC TÁCH BẠCH
```

### Âm thanh

```text
whoosh = thước dọc di chuyển về x=0
hit    = gốc chung sáng lên
tick   = đọc x, đọc y
```

### Ghi chú Manim

Helper dự kiến:

```python
make_text()
make_math()
play_focus()
play_dim()
make_scan_band()
play_scan_once()
```

Đối tượng gợi ý:

```python
x_axis_line
curve
endpoint_dots
temporary_vertical_rulers
y_axis_line
origin_dot
origin_label
sample_point
x_reading_guide
y_reading_guide
direction_arrows
```

## C06. HÌNH ẢNH CỦA SỰ BIẾN THIÊN

### Mục tiêu hoạt ảnh

Nhìn lại bảng giá trị và hình vừa được dựng.

Cảnh này làm rõ:

```text
bảng giữ giá trị cụ thể
đồ thị cho hình ảnh tổng thể của sự biến thiên
```

Định nghĩa đồ thị chỉ được gọi tên ở cuối cảnh, như kết quả tự nhiên của quá trình kiến tạo.

### Khung định danh cảnh

```text
06
HÌNH ẢNH CỦA SỰ BIẾN THIÊN
```

### Đối tượng được phép xuất hiện

```text
bảng giá trị
hệ hai trục đã hình thành
đường cong
các điểm (x,y)
công thức y = x^3 - 3x
định nghĩa đồ thị
```

### Đối tượng chưa được phép hiện quá sớm

```text
định nghĩa đồ thị ngay đầu cảnh
```

### Diễn tiến hoạt ảnh

#### Pha 1. Bảng trở lại với vai trò của nó

Hiện bảng giá trị ở bên trái.

Một dòng trong bảng được nhấn:

```text
x = 2.5
y = 8.125
```

Chữ:

```text
BẢNG GIỮ CÁC GIÁ TRỊ CỤ THỂ
```

Hoạt ảnh tương ứng với C06-01.

#### Pha 2. Bảng khó cho thấy chuyển động chung

Các dòng bảng được quét liên tiếp từ trên xuống.

Người xem thấy phải đọc nhiều dòng.

Chữ:

```text
MUỐN THẤY XU HƯỚNG
PHẢI SO SÁNH NHIỀU DÒNG
```

Bảng lùi xuống.

Hoạt ảnh tương ứng với C06-02.

#### Pha 3. Hình cho cái nhìn cùng lúc

Ở bên phải hiện hệ hai trục và đường cong đã kiến tạo.

Các điểm sáng lên lần lượt theo chiều từ trái sang phải.

Chữ:

```text
HÌNH CHO THẤY CÁCH CÁC GIÁ TRỊ NỐI NHAU
```

Hoạt ảnh tương ứng với C06-03 đến C06-05.

#### Pha 4. Bảng và hình không thay thế nhau

Bảng ở bên trái, hình ở bên phải.

Ở giữa hiện dấu phân biệt, không phải dấu hơn kém:

```text
HAI CÁCH NHÌN
HAI CÔNG VIỆC
```

Dưới bảng:

```text
CHÍNH XÁC TỪNG DÒNG
```

Dưới hình:

```text
TỔNG THỂ BIẾN THIÊN
```

Hoạt ảnh tương ứng với C06-06 và C06-07.

#### Pha 5. Định nghĩa xuất hiện

Bảng và hình lùi xuống.

Ở giữa hiện:

$$
y=f(x)
$$

Sau đó hiện từng phần của định nghĩa:

```text
ĐỒ THỊ LÀ TẬP HỢP CÁC ĐIỂM
```

$$
(x, f(x))
$$

```text
TRONG MẶT PHẲNG TỌA ĐỘ
```

Chữ cuối:

```text
ĐỊNH NGHĨA LÀ CÁCH NÓI GỌN CỦA NHU CẦU ĐÃ ĐƯỢC KIẾN TẠO
```

Hoạt ảnh tương ứng với C06-08.

### Chữ trên màn hình

```text
BẢNG GIỮ CÁC GIÁ TRỊ CỤ THỂ
MUỐN THẤY XU HƯỚNG
PHẢI SO SÁNH NHIỀU DÒNG
HÌNH CHO THẤY CÁCH CÁC GIÁ TRỊ NỐI NHAU
HAI CÁCH NHÌN
HAI CÔNG VIỆC
CHÍNH XÁC TỪNG DÒNG
TỔNG THỂ BIẾN THIÊN
ĐỒ THỊ LÀ TẬP HỢP CÁC ĐIỂM
TRONG MẶT PHẲNG TỌA ĐỘ
ĐỊNH NGHĨA LÀ CÁCH NÓI GỌN CỦA NHU CẦU ĐÃ ĐƯỢC KIẾN TẠO
```

### Âm thanh

```text
tick   = nhấn dòng bảng
whoosh = chuyển từ bảng sang hình
typing = định nghĩa xuất hiện từng phần
```

### Ghi chú Manim

Helper dự kiến:

```python
make_text()
make_text_block()
make_math()
make_frame()
play_scan_once()
play_focus()
play_dim()
```

Đối tượng gợi ý:

```python
value_table
highlighted_table_row
full_coordinate_plane
curve
graph_points
definition_parts
```

## C07. KẾT TINH

### Mục tiêu hoạt ảnh

Gom lại toàn bộ quá trình kiến tạo.

Cảnh này không thêm ví dụ mới.  
Nó tái hiện con đường đã đi qua dưới dạng một bản đồ chuyển hóa ngắn gọn:

```text
X ĐƯỢC CHỌN
Y ĐƯỢC TRẢ LẠI
TRỤC X GIỮ THỨ TỰ
PHƯƠNG DỌC GIỮ MỐC X
ĐIỂM GIỮ CẶP (X,Y)
TRỤC Y LÀ THƯỚC ĐO CHUNG
GỐC CHUNG QUY CHIẾU HAI PHÉP ĐO
ĐỒ THỊ LÀ HÌNH ẢNH CỦA SỰ BIẾN THIÊN
```

### Khung định danh cảnh

```text
07
KẾT TINH
```

### Đối tượng được phép xuất hiện

```text
toàn bộ cấu trúc đã kiến tạo
bản đồ tóm tắt các bước
câu hỏi ban đầu
câu kết tinh
```

### Diễn tiến hoạt ảnh

#### Pha 1. Trở lại câu hỏi ban đầu

Màn hình tối, chỉ hiện câu hỏi:

```text
VÌ SAO ĐỒ THỊ HÀM SỐ THƯỜNG ĐƯỢC VẼ BẰNG HAI TRỤC VUÔNG GÓC?
```

Câu hỏi giữ đủ lâu.

Sau đó mờ xuống nhưng không biến mất hoàn toàn.

Hoạt ảnh tương ứng với C07-01.

#### Pha 2. Dựng bản đồ quá trình

Lần lượt hiện các khối nhỏ theo chiều từ trái sang phải hoặc từ trên xuống dưới:

```text
X ĐƯỢC CHỌN
Y ĐƯỢC TRẢ LẠI
THỨ TỰ CỦA X
ĐỘ CAO CỦA Y
ĐIỂM (X,Y)
TRỤC Y
GỐC CHUNG
HÌNH ẢNH BIẾN THIÊN
```

Mỗi khối có một biểu tượng hình học rất đơn giản:

```text
x row
vertical segment
endpoint dot
y axis
origin
curve
```

Không làm thành sơ đồ quá nhiều mũi tên.  
Ưu tiên chuyển hóa bằng vị trí và xuất hiện tuần tự.

Hoạt ảnh tương ứng với C07-02 đến C07-07.

#### Pha 3. Hai công việc được tách ra

Hệ trục và đường cong hiện lại ở trung tâm.

Trục ngang sáng nhẹ:

```text
ĐI NGANG: THAY ĐỔI X
```

Trục dọc sáng nhẹ:

```text
ĐI DỌC: ĐO Y
```

Sau đó cả hai cùng sáng vừa phải.

Chữ:

```text
HAI CÔNG VIỆC ĐƯỢC TÁCH RA
NHƯNG GẶP NHAU TRONG CÙNG MỘT ĐIỂM
```

Hoạt ảnh tương ứng với C07-08.

#### Pha 4. Không tuyệt đối hóa hệ trục vuông góc

Hệ trục vuông góc lùi xuống.

Hiện một dòng chữ nhỏ, màu `COLOR_MUTED`:

```text
KHÔNG PHẢI CÁCH BIỂU DIỄN DUY NHẤT
```

Sau đó dòng chính hiện:

```text
NHƯNG VỚI NHU CẦU NHÌN Y THAY ĐỔI THEO X
NÓ LÀ MỘT CÁCH RÕ RÀNG, ỔN ĐỊNH, DỄ ĐỌC
```

Hoạt ảnh tương ứng với C07-09.

#### Pha 5. Kết tinh cuối

Toàn bộ hình gọn lại: hệ trục, đường cong, một vài điểm.

Câu cuối hiện ở giữa hoặc phía dưới:

```text
ĐỒ THỊ LÀ HÌNH ẢNH CỦA SỰ BIẾN THIÊN
```

Dòng này dùng `FONT_SIZE_EMPHASIS`, màu `COLOR_PRIMARY` hoặc một nhấn rất nhẹ.

Giữ hình lâu hơn các cảnh trước.

Hoạt ảnh tương ứng với C07-10.

### Chữ trên màn hình

```text
VÌ SAO ĐỒ THỊ HÀM SỐ THƯỜNG ĐƯỢC VẼ BẰNG HAI TRỤC VUÔNG GÓC?
X ĐƯỢC CHỌN
Y ĐƯỢC TRẢ LẠI
THỨ TỰ CỦA X
ĐỘ CAO CỦA Y
ĐIỂM (X,Y)
TRỤC Y
GỐC CHUNG
HÌNH ẢNH BIẾN THIÊN
ĐI NGANG: THAY ĐỔI X
ĐI DỌC: ĐO Y
HAI CÔNG VIỆC ĐƯỢC TÁCH RA
NHƯNG GẶP NHAU TRONG CÙNG MỘT ĐIỂM
KHÔNG PHẢI CÁCH BIỂU DIỄN DUY NHẤT
RÕ RÀNG
ỔN ĐỊNH
DỄ ĐỌC
ĐỒ THỊ LÀ HÌNH ẢNH CỦA SỰ BIẾN THIÊN
```

### Âm thanh

```text
typing = câu hỏi ban đầu
tick   = từng khối trong bản đồ quá trình
hit    = câu kết tinh cuối, rất nhẹ
```

### Ghi chú Manim

Helper dự kiến:

```python
make_text()
make_text_block()
make_math()
make_frame()
play_focus()
play_dim()
```

Đối tượng gợi ý:

```python
initial_question
construction_map_blocks
x_role_block
y_role_block
axis_role_blocks
origin_block
final_axes
final_curve
final_crystallization_text
```

## C08. MÌNH ĐÃ HIỂU CHƯA?

### Mục tiêu hoạt ảnh

Dẫn người xem từ việc nghe lời giải thích sang việc tự đi lại con đường tư duy.

Cảnh này không mở kiến thức mới.  
Nó gợi thực hành: tự tính, tự dựng, tự trả lời.

### Khung định danh cảnh

```text
08
MÌNH ĐÃ HIỂU CHƯA?
```

### Đối tượng được phép xuất hiện

```text
bản đồ rút gọn các bước
câu hỏi tự kiểm tra
gợi ý bài luận ZO Math
hình cuối cùng mờ ở nền
```

### Diễn tiến hoạt ảnh

#### Pha 1. Con đường được rút gọn

Hiện một chuỗi bước ngắn, theo chiều ngang hoặc vòng cung nhẹ:

```text
BẢNG SỐ
MỐC X
ĐOẠN Y
ĐIỂM (X,Y)
ĐƯỜNG CONG
HAI TRỤC
```

Mỗi bước có một hình tượng rất nhỏ:

```text
mini table
x ticks
vertical segment
dot
curve
axes
```

Các bước hiện lần lượt, không vội.

Hoạt ảnh tương ứng với C08-01.

#### Pha 2. Câu hỏi tự kiểm tra

Ba câu hỏi hiện lần lượt, mỗi câu có thời gian đọc riêng:

```text
BẢNG CÓ CHO THẤY RÕ Y ĐANG THAY ĐỔI KHÔNG?
ĐOẠN THẲNG ĐỨNG GIỮ NGUYÊN THÔNG TIN NÀO?
VÌ SAO SỰ VUÔNG GÓC GIÚP ĐỌC X VÀ Y KHÔNG LẪN VÀO NHAU?
```

Không cần minh họa thêm nhiều.  
Mỗi câu hỏi có thể đi kèm một phần hình nhỏ tương ứng sáng lên trong chuỗi bước.

Hoạt ảnh tương ứng với C08-02 và C08-03.

#### Pha 3. Dẫn về ZO Math

Hình cuối cùng mờ xuống.

Hiện cụm chữ:

```text
ĐỌC LẠI CHẬM HƠN
TÍNH LẠI TỪNG GIÁ TRỊ
VẼ LẠI TỪNG BƯỚC
```

Sau đó hiện:

```text
ZO MATH
```

và dòng nhỏ:

```text
BÀI LUẬN ĐẦY ĐỦ, BẢNG GIÁ TRỊ, HÌNH MINH HỌA, CÂU HỎI KHAI THÁC
```

Không dùng hiệu ứng quảng cáo.  
Giữ tĩnh, nhẹ, như lời mời học tiếp.

Hoạt ảnh tương ứng với C08-04.

#### Pha 4. Câu hỏi kết

Ở giữa màn hình hiện lại câu hỏi ban đầu:

```text
VÌ SAO ĐỒ THỊ HÀM SỐ THƯỜNG ĐƯỢC VẼ BẰNG HAI TRỤC VUÔNG GÓC?
```

Bên dưới, rất nhỏ:

```text
TỰ ĐI LẠI CON ĐƯỜNG MỘT LẦN NỮA
```

Fade out chậm.

### Chữ trên màn hình

```text
BẢNG SỐ
MỐC X
ĐOẠN Y
ĐIỂM (X,Y)
ĐƯỜNG CONG
HAI TRỤC
BẢNG CÓ CHO THẤY RÕ Y ĐANG THAY ĐỔI KHÔNG?
ĐOẠN THẲNG ĐỨNG GIỮ NGUYÊN THÔNG TIN NÀO?
VÌ SAO SỰ VUÔNG GÓC GIÚP ĐỌC X VÀ Y KHÔNG LẪN VÀO NHAU?
ĐỌC LẠI CHẬM HƠN
TÍNH LẠI TỪNG GIÁ TRỊ
VẼ LẠI TỪNG BƯỚC
ZO MATH
BÀI LUẬN ĐẦY ĐỦ, BẢNG GIÁ TRỊ, HÌNH MINH HỌA, CÂU HỎI KHAI THÁC
TỰ ĐI LẠI CON ĐƯỜNG MỘT LẦN NỮA
```

### Âm thanh

```text
tick   = từng bước trong chuỗi rút gọn
typing = câu hỏi tự kiểm tra
whoosh = chuyển sang phần ZO Math
```

### Ghi chú Manim

Helper dự kiến:

```python
make_text()
make_text_block()
make_frame()
play_type_text()
play_focus()
play_dim()
```

Đối tượng gợi ý:

```python
summary_path
mini_table_icon
mini_x_ticks
mini_y_segment
mini_point
mini_curve
mini_axes
self_check_questions
zo_math_card
final_question
```

---

## 1. Ghi chú chuyển sang mã Manim

Khi chuyển sang `03_manim_scene.py`, không nên viết toàn bộ một mạch ngay.

Thứ tự sản xuất nên là:

```text
1. Dựng helper phong cách.
2. Dựng dữ liệu hàm số và bảng giá trị.
3. Render riêng C02 để kiểm bảng.
4. Render riêng C03 để kiểm trục x và đoạn y.
5. Render riêng C04 để kiểm điểm và đường cong.
6. Render riêng C05 để kiểm trục y và gốc chung.
7. Sau khi C02--C05 ổn, mới hoàn thiện C01, C06, C07, C08.
```

Lý do: lõi toán-hình của video nằm ở C02--C05.  
Nếu phần này đúng, các cảnh mở đầu, kết tinh và dẫn thực hành sẽ dễ hoàn thiện hơn.

## 2. Ghi chú kiểm soát đối tượng đích

Không để các đối tượng sau xuất hiện quá sớm:

```text
trục y
gốc tọa độ
mặt phẳng tọa độ hoàn chỉnh
đường cong hoàn chỉnh
định nghĩa đồ thị
```

Thứ tự xuất hiện bắt buộc:

```text
bảng số
→ hàng x
→ đường ngang
→ trục x
→ đoạn y
→ đầu mút
→ điểm (x,y)
→ nhiều điểm
→ đường cong
→ thước đo y
→ trục y
→ gốc chung
→ hệ hai trục
→ định nghĩa đồ thị
```

Nếu thứ tự này bị đảo, hoạt ảnh sẽ đi ngược tinh thần kiến tạo.

## 3. Tiêu chuẩn kiểm bản nháp

Một bản render nháp đạt yêu cầu khi người xem có thể trả lời bằng mắt:

```text
TẠI SAO X ĐƯỢC ĐẶT TRÊN ĐƯỜNG NGANG?

TẠI SAO Y ĐƯỢC DỰNG LÊN HOẶC HẠ XUỐNG TỪ MỖI MỐC X?

TẠI SAO ĐẦU MÚT CỦA ĐOẠN GIỮ LẠI CẢ X VÀ Y?

TẠI SAO NHIỀU ĐIỂM GỢI RA ĐƯỜNG CONG?

TẠI SAO CẦN TRỤC Y?

TẠI SAO HAI TRỤC CÙNG GẶP Ở MỘT GỐC?

TẠI SAO ĐỒ THỊ LÀ HÌNH ẢNH CỦA SỰ BIẾN THIÊN?
```
