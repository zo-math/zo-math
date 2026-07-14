# Hướng dẫn sử dụng khối nội dung trong ZO Math

## 1. Mục đích

Hệ khối nội dung ZO Math dùng để tạo những vùng nội dung có trọng tâm trong bài viết toán học.

Hệ này không phân loại cứng theo chức năng như “định nghĩa”, “ví dụ” hay “bài tập”. Người viết chỉ chọn một trong ba màu và tự đặt tiêu đề phù hợp với nội dung thực tế.

## 2. Nguyên tắc thiết kế

- Tối giản nhưng không lạnh lẽo.
- Không dùng dải nhấn bên trái.
- Không dùng biểu tượng trang trí.
- Không dùng bóng đổ rõ.
- Dùng viền mảnh bao quanh toàn khối.
- Dùng nền rất nhạt.
- Tiêu đề cùng màu chữ với nội dung.
- Chỉ sử dụng bảng màu đã định nghĩa trong `zo-math.scss`.
- Đỏ và vàng là hai màu nhận diện chính của ZO Math.
- Không dùng khối chỉ để trang trí một đoạn văn không có trọng tâm rõ ràng.

## 3. Kiến trúc kỹ thuật

CSS của hệ khối được đặt tại:

```text
assets/css/_zo_content_blocks.scss
```

Tệp này được nhập từ:

```text
zo-math.scss
```

Mọi khối đều dùng lớp chung:

```text
zo-block
```

Sau đó thêm đúng một lớp màu:

```text
zo-block-red
zo-block-yellow
zo-block-gray
```

Tiêu đề dùng lớp:

```text
zo-block-title
```

Nội dung của khối thu gọn dùng lớp:

```text
zo-block-body
```

## 4. Ba loại khối

### 4.1. Khối đỏ

Lớp:

```text
zo-block-red
```

Dùng khi cần nhấn mạnh nội dung cốt lõi, giới hạn, điều kiện, cảnh báo hoặc một ý cần được nhận diện rõ.

Ví dụ tiêu đề:

```text
Hàm số
Điều kiện xác định
Điều cần tránh
Định lý Pythagoras
```

### 4.2. Khối vàng

Lớp:

```text
zo-block-yellow
```

Dùng cho nội dung dẫn dắt, quan sát, khám phá, ví dụ, hoạt động hoặc bài tập.

Ví dụ tiêu đề:

```text
Quan sát đồ thị
Một ví dụ mở đầu
Khám phá
Bài tập 3
```

### 4.3. Khối xám

Lớp:

```text
zo-block-gray
```

Dùng cho phần giải thích, ghi chú, chứng minh, gợi ý, lời giải hoặc nội dung hỗ trợ.

Ví dụ tiêu đề:

```text
Vì sao cần tính duy nhất?
Ghi chú
Gợi ý
Lời giải
```

Các cách dùng trên là định hướng, không phải luật cứng. Màu được chọn theo mức độ nhấn mạnh và vai trò của khối trong mạch đọc.

## 5. Khối mở cố định

### Khối đỏ

```markdown
:::: {.zo-block .zo-block-red}
::: {.zo-block-title}
Hàm số
:::

Cho $D\subset\mathbb{R}$. Một hàm số trên $D$ gắn cho mỗi
$x\in D$ đúng một giá trị $y=f(x)$.
::::
```

### Khối vàng

```markdown
:::: {.zo-block .zo-block-yellow}
::: {.zo-block-title}
Quan sát đồ thị
:::

Thay đổi tham số $a$ trong hàm số $y=ax^2$ và quan sát đồ thị.
::::
```

### Khối xám

```markdown
:::: {.zo-block .zo-block-gray}
::: {.zo-block-title}
Vì sao cần tính duy nhất?
:::

Tính duy nhất bảo đảm rằng mỗi đầu vào xác định rõ một đầu ra.
::::
```

## 6. Khối thu gọn

Khối thu gọn dùng thẻ HTML gốc `<details>`. Người đọc nhấp vào tiêu đề để mở hoặc đóng nội dung.

### Khối đỏ thu gọn

```html
<details class="zo-block zo-block-red">
<summary class="zo-block-title">Điều cần tránh</summary>
<div class="zo-block-body">

Không gắn cùng một giá trị $x$ với hai giá trị $y$ khác nhau.

</div>
</details>
```

### Khối vàng thu gọn

```html
<details class="zo-block zo-block-yellow">
<summary class="zo-block-title">Một ví dụ mở đầu</summary>
<div class="zo-block-body">

Với $f(x)=x^2$, hai giá trị $x=2$ và $x=-2$ cùng cho $f(x)=4$.

</div>
</details>
```

### Khối xám thu gọn

```html
<details class="zo-block zo-block-gray">
<summary class="zo-block-title">Gợi ý</summary>
<div class="zo-block-body">

Hãy bắt đầu từ điều kiện để biểu thức dưới dấu căn không âm.

</div>
</details>
```

## 7. Mở sẵn khối thu gọn

Thêm thuộc tính `open` nếu muốn nội dung xuất hiện ngay khi tải trang nhưng vẫn cho phép người đọc đóng lại:

```html
<details class="zo-block zo-block-gray" open>
<summary class="zo-block-title">Lời giải</summary>
<div class="zo-block-body">

Nội dung lời giải.

</div>
</details>
```

## 8. Quy tắc đặt tiêu đề

Tiêu đề được đặt tự do theo nội dung.

Có thể dùng tên chức năng:

```text
Định nghĩa
Ví dụ
Gợi ý
Lời giải
```

Có thể dùng trực tiếp tên nội dung:

```text
Hàm số
Định lý Pythagoras
Điều kiện xác định
Quan sát đồ thị
```

Không bắt buộc phải ghi “Định nghĩa”, “Ví dụ” hoặc “Bài tập” nếu tên nội dung cụ thể rõ hơn.

Không viết hoa toàn bộ tiêu đề.

## 9. Khi nào dùng dạng thu gọn

Dùng dạng thu gọn khi nội dung:

- không cần đọc ngay để hiểu mạch chính;
- là gợi ý, lời giải hoặc đáp án;
- khá dài;
- chỉ phục vụ một nhóm người đọc;
- có thể làm gián đoạn mạch đọc nếu luôn mở.

Không thu gọn nội dung bắt buộc phải đọc để hiểu phần tiếp theo.

## 10. Những điều không nên làm

Không tạo thêm lớp màu mới theo từng trang.

Không dùng lại các lớp cũ như:

```text
highlight-box-soft-red
highlight-box-honey-gold
```

cho nội dung mới.

Không dùng nhiều khối liên tiếp khi văn bản thông thường và tiêu đề mục đã đủ rõ.

Không dùng màu để thay thế cho cấu trúc lập luận.

## 11. Chuyển đổi nội dung cũ

Các lớp cũ vẫn được giữ trong giai đoạn chuyển tiếp.

Khi chuyển một khối cũ:

1. đọc chức năng thật của nội dung;
2. chọn đỏ, vàng hoặc xám;
3. đặt lại tiêu đề phù hợp;
4. quyết định dạng mở cố định hay thu gọn;
5. render và kiểm tra trực quan;
6. chỉ xóa CSS cũ khi không còn trang nào sử dụng.

## 12. Trạng thái triển khai

Hệ ba khối đã được kiểm tra đầy đủ:

- đỏ dạng thường;
- đỏ dạng thu gọn;
- vàng dạng thường;
- vàng dạng thu gọn;
- xám dạng thường;
- xám dạng thu gọn.
]633;E;{ printf '\\n'\x3b printf '%s' 'IyMgMTMuIFF1eSB04bqvYyBz4butIGThu6VuZyBtw6B1IGNobyBu4buZaSBkdW5nIG3hu5tpCgpOZ3Xhu5NuIMSR4buLbmggbmdoxKlhIG3DoHUgdHJ1bmcgdMOibSBj4bunYSBaTyBNYXRoIGzDoDoKCmBgYHRleHQKem8tbWF0aC5zY3NzCmBgYAoKQ8OhYyB0aMOgbmggcGjhuqduIGdpYW8gZGnhu4duIG3hu5tpIGNo4buJIHPhu60gZOG7pW5nIG5o4buvbmcgbmjDs20gbcOgdSBjaMOtbmggdGjhu6ljIHNhdToKCmBgYHRleHQKJHJlZC0wMSDEkeG6v24gJHJlZC0xOQokeWVsbG93LTAxIMSR4bq/biAkeWVsbG93LTE5CiRncmF5LTEwMCDEkeG6v24gJGdyYXktOTAwCiR0ZWFsCiR3aGl0ZQokYmxhY2sKYGBgCgpLaMO0bmcgZ2hpIHRy4buxYyB0aeG6v3AgbcOjIG3DoHUgbeG7m2kgdHJvbmcgdOG7q25nIHRow6BuaCBwaOG6p24gbuG6v3UgbcOgdSDEkcOzIMSRw6MgY8OzIHRyb25nIGB6by1tYXRoLnNjc3NgLgoKS2jDtG5nIHThuqFvIHRow6ptIG3hu5l0IHThuqduZyBiaeG6v24gbcOgdSB0b8OgbiBj4bulYyBjaOG7iSDEkeG7gyDEkeG7lWkgdMOqbiBjw6FjIG3DoHUgxJHDoyBjw7MuCgpDw6FjIGJp4bq/biBj4bulYyBi4buZIGLDqm4gdHJvbmcgbeG7mXQgdGjDoG5oIHBo4bqnbiwgY2jhurNuZyBo4bqhbjoKCmBgYHRleHQKLS16by1ibG9jay1iYWNrZ3JvdW5kCi0tem8tYmxvY2stYm9yZGVyCi0tem8tYmxvY2staG92ZXIKYGBgCgrEkcaw4bujYyBwaMOpcCBz4butIGThu6VuZyBraGkgY2jDum5nIGdpw7pwIG5oaeG7gXUgYmnhur9uIHRo4buDIGPhu6dhIGPDuW5nIG3hu5l0IHRow6BuaCBwaOG6p24gZMO5bmcgY2h1bmcgY+G6pXUgdHLDumMgQ1NTLgoKQ8OhYyBiaeG6v24gYCRibHVlYCB2w6AgYCRpbmRpZ29gIGNo4buJIMSRxrDhu6NjIGdp4buvIMSR4buDIHTGsMahbmcgdGjDrWNoIHbhu5tpIEJvb3RzdHJhcCwgUXVhcnRvIHbDoCBjw6FjIHRyYW5nIGPFqS4gS2jDtG5nIGTDuW5nIGNow7puZyDEkeG7gyB0aGnhur90IGvhur8gdGjDoG5oIHBo4bqnbiBaTyBNYXRoIG3hu5tpLgoKVmnhu4djIGNodeG6qW4gaMOzYSBtw6B1IGtow7RuZyB04buxIMSR4buZbmcgw6FwIGThu6VuZyBuZ8aw4bujYyBjaG8gdG/DoG4gYuG7mSBu4buZaSBkdW5nIGPFqS4gQ2jhu4kgY2h1eeG7g24gxJHhu5VpIHThu6tuZyB0cmFuZyBob+G6t2MgdOG7q25nIHRow6BuaCBwaOG6p24gY8WpIGtoaSBjw7MgecOqdSBj4bqndSB2w6Agc2F1IGtoaSDEkcOjIGtp4buDbSB0cmEgdHLhu7FjIHF1YW4uCg==' | base64 -d\x3b } >> README/huong_dan_su_dung_khoi_noi_dung.md;77ee8c29-fa45-4be2-9801-3eeee6643bbf]633;C
## 13. Quy tắc sử dụng màu cho nội dung mới

Nguồn định nghĩa màu trung tâm của ZO Math là:

```text
zo-math.scss
```

Các thành phần giao diện mới chỉ sử dụng những nhóm màu chính thức sau:

```text
$red-01 đến $red-19
$yellow-01 đến $yellow-19
$gray-100 đến $gray-900
$teal
$white
$black
```

Không ghi trực tiếp mã màu mới trong từng thành phần nếu màu đó đã có trong `zo-math.scss`.

Không tạo thêm một tầng biến màu toàn cục chỉ để đổi tên các màu đã có.

Các biến cục bộ bên trong một thành phần, chẳng hạn:

```text
--zo-block-background
--zo-block-border
--zo-block-hover
```

được phép sử dụng khi chúng giúp nhiều biến thể của cùng một thành phần dùng chung cấu trúc CSS.

Các biến `$blue` và `$indigo` chỉ được giữ để tương thích với Bootstrap, Quarto và các trang cũ. Không dùng chúng để thiết kế thành phần ZO Math mới.

Việc chuẩn hóa màu không tự động áp dụng ngược cho toàn bộ nội dung cũ. Chỉ chuyển đổi từng trang hoặc từng thành phần cũ khi có yêu cầu và sau khi đã kiểm tra trực quan.
