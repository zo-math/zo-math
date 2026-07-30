# Hướng dẫn sử dụng khối nội dung trong ZO Math

## 1. Mục đích

Hệ khối nội dung ZO Math dùng để tách những đơn vị nội dung có chức năng rõ ràng trong bài viết toán học.

Khối nội dung không phải là yếu tố trang trí và không thay thế cấu trúc lập luận. Một đoạn văn chỉ được đưa vào khối khi việc tách nó ra giúp người đọc nhận biết đúng vai trò của nó trong bài.

Mỗi khối được xác định bởi hai thuộc tính độc lập:

- **trạng thái hiển thị:** mở cố định hoặc thu gọn;
- **màu sắc:** đỏ, vàng hoặc xám.

Phải xác định trạng thái trước, sau đó mới xác định màu.

## 2. Trình tự quyết định

Khi cân nhắc đưa một nội dung vào khối, thực hiện đúng thứ tự sau:

1. **Nội dung có thực sự cần tách thành khối không?**
   - Nếu văn bản thông thường và hệ tiêu đề đã diễn đạt rõ vai trò của nội dung, không tạo khối.
   - Chỉ tạo khối khi nội dung là một đơn vị tương đối trọn vẹn và việc tách khối có ý nghĩa đối với mạch đọc.
2. **Nội dung có tham gia trực tiếp vào mạch chính của bài không?**
   - Có: dùng **khối mở cố định**.
   - Không: dùng **khối thu gọn**.
3. **Bản chất của nội dung là gì?**
   - Lí thuyết chung, có khả năng tái sử dụng: **đỏ**.
   - Bài viết nhỏ tương đối độc lập, có chức năng khám phá hoặc mở rộng: **vàng**.
   - Nội dung hỗ trợ, phụ thuộc vào ngữ cảnh đang trình bày: **xám**.

Không bắt đầu bằng câu hỏi “nên dùng màu gì?”. Cách làm đó dễ biến màu sắc thành phương tiện trang trí hoặc nhấn mạnh tùy ý.

## 3. Xác định trạng thái hiển thị

### 3.1. Khối mở cố định

Dùng khối mở cố định khi nội dung tham gia trực tiếp vào mạch lập luận tổng thể. Người đọc cần đọc nội dung ấy để hiểu đầy đủ phần đang trình bày hoặc phần tiếp theo.

Nếu bỏ qua khối mở cố định, mạch chính của bài sẽ thiếu một mắt xích cần thiết.

### 3.2. Khối thu gọn

Dùng khối thu gọn khi nội dung không tham gia trực tiếp vào mạch lập luận tổng thể. Người đọc có thể bỏ qua toàn bộ khối mà vẫn hiểu đầy đủ bài chính.

Khối thu gọn thường phù hợp với:

- một hướng khám phá hoặc mở rộng ngoài mạch chính;
- một bài viết nhỏ dành cho người muốn đọc sâu hơn;
- chú giải chuyên môn chỉ cần cho một nhóm người đọc;
- chứng minh, chi tiết kĩ thuật, gợi ý, lời giải hoặc đáp án không bắt buộc;
- nội dung có thể làm gián đoạn mạch đọc nếu luôn hiển thị.

Độ dài không phải là tiêu chí quyết định. Một nội dung dài nhưng bắt buộc đối với mạch chính không được thu gọn chỉ để làm trang ngắn hơn.

### 3.3. Thuộc tính `open`

Có thể thêm thuộc tính `open` để một khối thu gọn được mở sẵn khi tải trang.

Thuộc tính này chỉ thay đổi trạng thái ban đầu trên giao diện. Khối vẫn là khối thu gọn, người đọc vẫn có thể đóng lại, và nội dung của nó vẫn không được xem là mắt xích bắt buộc của mạch chính.

## 4. Xác định màu

Chỉ xác định màu sau khi đã quyết định nội dung cần tạo khối và chọn trạng thái hiển thị.

### 4.1. Khối đỏ — lí thuyết chung

Lớp:

```text
zo-block-red
```

Dùng khối đỏ cho nội dung lí thuyết có tính khái quát và khả năng tái sử dụng ngoài đối tượng đang khảo sát, chẳng hạn:

- định nghĩa một khái niệm;
- định lí, mệnh đề, hệ quả;
- tính chất hoặc kết quả toán học khái quát;
- một điều kiện chung cần thiết để áp dụng lí thuyết.

Một kết luận quan trọng nhưng chỉ đúng cho hàm số, hình hoặc bài toán đang xét không mặc nhiên thuộc khối đỏ.

Ví dụ tiêu đề:

```text
Hàm số
Hàm số lẻ
Định lí giá trị trung gian
Điều kiện để hàm số liên tục
```

### 4.2. Khối vàng — bài viết nhỏ độc lập

Lớp:

```text
zo-block-yellow
```

Dùng khối vàng cho một bài viết nhỏ tương đối độc lập, có thể tách khỏi bài lớn mà vẫn tạo thành một đơn vị đọc có ý nghĩa. Khi xuất hiện trong bài chính, nội dung ấy giữ vai trò:

- giải thích bằng một hướng nhìn giàu trực giác;
- mở rộng vấn đề;
- tạo liên tưởng hoặc kết nối;
- khơi gợi trí tưởng tượng và mong muốn khám phá.

Một ví dụ, hoạt động hoặc bài tập không mặc nhiên thuộc khối vàng. Chúng chỉ dùng màu vàng khi được phát triển thành một đơn vị nội dung tương đối độc lập và đảm nhiệm đúng vai trò trên.

Ví dụ tiêu đề:

```text
Thí nghiệm trên mặt phẳng nghiêng
Khi đồ thị rung nhanh đến vô hạn
Một cách nhìn từ chuyển động
```

### 4.3. Khối xám — nội dung hỗ trợ theo ngữ cảnh

Lớp:

```text
zo-block-gray
```

Dùng khối xám cho nội dung hỗ trợ việc hiểu hoặc xử lí vấn đề đang trình bày và phụ thuộc vào ngữ cảnh của bài, chẳng hạn:

- giải thích hoặc chú giải;
- chứng minh;
- chi tiết kĩ thuật;
- cách hiểu ở bậc học cao hơn;
- gợi ý, lời giải hoặc đáp án.

Khác với khối vàng, nội dung xám không cần có khả năng đứng riêng như một bài viết nhỏ; khi tách khỏi ngữ cảnh, nó có thể mất một phần ý nghĩa.

Ví dụ tiêu đề:

```text
Vì sao cần tính duy nhất?
Cách hiểu trong Toán học bậc cao
Chứng minh
Gợi ý
```

## 5. Những trường hợp dễ phân loại sai

- Không dùng khối đỏ chỉ vì một kết luận quan trọng hoặc cần nổi bật.
- Không dùng khối vàng chỉ vì nội dung là ví dụ, hoạt động hay bài tập.
- Không dùng khối xám như nơi chứa mọi đoạn văn phụ.
- Không chọn màu theo vẻ đẹp, mức độ nổi bật hoặc cảm giác chủ quan.
- Không buộc một bài phải có khối nội dung hoặc phải có đủ ba màu.
- Không đặt nhiều khối liên tiếp nếu văn bản thông thường và hệ tiêu đề đã đủ rõ.
- Không dùng màu để thay thế quan hệ lập luận giữa các phần.
- Không thu gọn nội dung mà người đọc bắt buộc phải biết để hiểu phần tiếp theo.

## 6. Kiến trúc kỹ thuật

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

## 7. Cú pháp khối mở cố định

Ví dụ khối đỏ:

```markdown
:::: {.zo-block .zo-block-red}
::: {.zo-block-title}
Hàm số
:::

Cho $D\subset\mathbb{R}$. Một hàm số trên $D$ gắn cho mỗi
$x\in D$ đúng một giá trị $y=f(x)$.
::::
```

Ví dụ khối vàng:

```markdown
:::: {.zo-block .zo-block-yellow}
::: {.zo-block-title}
Một cách nhìn từ chuyển động
:::

Nội dung bài viết nhỏ tham gia trực tiếp vào mạch chính.
::::
```

Ví dụ khối xám:

```markdown
:::: {.zo-block .zo-block-gray}
::: {.zo-block-title}
Vì sao cần tính duy nhất?
:::

Tính duy nhất bảo đảm rằng mỗi đầu vào xác định rõ một đầu ra.
::::
```

## 8. Cú pháp khối thu gọn

Khối thu gọn dùng thẻ HTML gốc `<details>`. Người đọc nhấp vào tiêu đề để mở hoặc đóng nội dung.

Ví dụ khối đỏ thu gọn:

```html
<details class="zo-block zo-block-red">
  <summary class="zo-block-title">Một mệnh đề mở rộng</summary>
  <div class="zo-block-body">
    Nội dung lí thuyết chung không bắt buộc đối với mạch chính.
  </div>
</details>
```

Ví dụ khối vàng thu gọn:

```html
<details class="zo-block zo-block-yellow">
  <summary class="zo-block-title">Khi đồ thị rung nhanh đến vô hạn</summary>
  <div class="zo-block-body">
    Nội dung một bài viết nhỏ dành cho người muốn khám phá thêm.
  </div>
</details>
```

Ví dụ khối xám thu gọn:

```html
<details class="zo-block zo-block-gray">
  <summary class="zo-block-title">Gợi ý</summary>
  <div class="zo-block-body">
    Hãy bắt đầu từ điều kiện để biểu thức dưới dấu căn không âm.
  </div>
</details>
```

## 9. Cú pháp mở sẵn khối thu gọn

Thêm thuộc tính `open` nếu muốn nội dung xuất hiện ngay khi tải trang nhưng vẫn cho phép người đọc đóng lại:

```html
<details class="zo-block zo-block-gray" open>
  <summary class="zo-block-title">Lời giải</summary>
  <div class="zo-block-body">Nội dung lời giải.</div>
</details>
```

## 10. Quy tắc đặt tiêu đề

Tiêu đề phải gọi đúng nội dung cụ thể hoặc vai trò thực tế của khối.

Ưu tiên tên nội dung khi tên đó rõ nghĩa:

```text
Hàm số
Định lí Pythagoras
Khi đồ thị rung nhanh đến vô hạn
```

Có thể dùng tên chức năng khi phù hợp:

```text
Chứng minh
Gợi ý
Lời giải
```

Không bắt buộc ghi “Định nghĩa”, “Ví dụ” hoặc “Bài tập” nếu tên nội dung cụ thể rõ hơn. Không viết hoa toàn bộ tiêu đề.

## 11. Nguyên tắc thiết kế giao diện

- Tối giản nhưng không lạnh lẽo.
- Không dùng dải nhấn bên trái.
- Không dùng biểu tượng trang trí.
- Không dùng bóng đổ rõ.
- Dùng viền mảnh bao quanh toàn khối.
- Dùng nền rất nhạt.
- Tiêu đề cùng màu chữ với nội dung.
- Chỉ sử dụng bảng màu đã định nghĩa trong `zo-math.scss`.
- Đỏ và vàng là hai màu nhận diện chính của ZO Math.
- Không tạo thêm lớp màu riêng cho từng trang.

Không dùng lại các lớp cũ sau cho nội dung mới:

```text
highlight-box-soft-red
highlight-box-honey-gold
```

## 12. Chuyển đổi nội dung cũ

Các lớp cũ vẫn được giữ trong giai đoạn chuyển tiếp.

Khi chuyển một khối cũ:

1. đọc toàn bộ nội dung và xác định chức năng thật;
2. quyết định nội dung có cần tiếp tục được tách thành khối không;
3. xác định nội dung thuộc mạch chính hay phần đọc thêm để chọn trạng thái;
4. xác định bản chất nội dung để chọn đỏ, vàng hoặc xám;
5. đặt lại tiêu đề nếu cần;
6. render và kiểm tra trực quan;
7. chỉ xóa CSS cũ khi không còn trang nào sử dụng.

## 13. Quy tắc sử dụng màu cho giao diện

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

## 14. Trạng thái triển khai

Hệ khối hiện hỗ trợ đầy đủ:

- đỏ mở cố định và đỏ thu gọn;
- vàng mở cố định và vàng thu gọn;
- xám mở cố định và xám thu gọn;
- khối thu gọn mở sẵn bằng thuộc tính `open`.
