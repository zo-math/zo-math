# Bảng Quy chuẩn Ký tự & Cách Gõ

## 1. Typography cơ bản

_Typography:_ nghệ thuật và kỹ thuật trình bày chữ

| Ký tự | Tên chuẩn                | Cách gõ (Windows) | Unicode         | Dùng trực tiếp trong LaTeX? | Ghi chú                                                        |
| ----: | :----------------------- | :---------------- | :-------------- | :-------------------------- | :------------------------------------------------------------- |
|     … | Ellipsis (dấu chấm lửng) | Alt+0133          | U+2026          | Có                          | LaTeX hiển thị được nhưng không “đẹp” bằng `\ldots` / `\dots`  |
|     – | En dash                  | Alt+0150          | U+2013          | Có                          | Tương đương `--` trong văn bản; trong toán thường nên dùng `-` |
|     — | Em dash                  | Alt+0151          | U+2014          | Có                          | LaTeX vẫn render, nhưng không dùng trong toán                  |
|   ‘ ’ | Nháy đơn thông minh      | Alt+0145 / 0146   | U+2018 / U+2019 | Có                          | Dùng trong văn bản; không dùng trong toán                      |
|   “ ” | Nháy kép thông minh      | Alt+0147 / 0148   | U+201C / U+201D | Có                          | Văn bản; toán không dùng                                       |
|     ­ | Soft hyphen              | Alt+0173          | U+00AD          | Có                          | Tự động ẩn; chỉ để gợi ý ngắt dòng                             |

## 2. Ký hiệu toán học cơ bản

| Ký tự | Tên                 | Cách gõ (Windows) | Unicode | Dùng trực tiếp trong LaTeX? | Ghi chú                                                               |
| ----: | :------------------ | :---------------- | :------ | :-------------------------- | :-------------------------------------------------------------------- |
|     π | Pi                  | Alt+227           | U+03C0  | Có                          | Hiển thị tốt; tương đương macro `\pi`                                 |
|     e | Euler’s number      | (phím e)          | U+0065  | Có                          | Đây chỉ là chữ e, không phải ký tự đặc biệt                           |
|     ∞ | Infinity            | Alt+236           | U+221E  | Có                          | Tương đương `\infty`; Unicode hiển thị tốt                            |
|     ± | Plus-minus          | Alt+0177          | U+00B1  | Có                          | Hiển thị đúng; tương đương `\pm`                                      |
|     × | Multiplication sign | Alt+0215          | U+00D7  | Có                          | Hiển thị được; trong toán thường dùng `\times` để thống nhất          |
|     ÷ | Division sign       | Alt+0247          | U+00F7  | Có                          | Hiển thị được; hiếm dùng trong toán học phổ thông nghiêm túc          |
|     · | Dot operator        | Alt+0183          | U+00B7  | Có                          | Tương đương `\cdot` — dùng được                                       |
|     √ | Radical (căn)       | Alt+251           | U+221A  | Có nhưng hạn chế            | Thể hiện được ký hiệu √ nhưng _không thể_ tạo căn dài dạng `\sqrt{x}` |

## 3. Ký hiệu logic & quan hệ

| Ký tự | Tên         | Gõ (Windows) | Unicode | Dùng trực tiếp trong LaTeX? | Ghi chú                                           |
| ----: | :---------- | :----------- | :------ | :-------------------------- | :------------------------------------------------ |
|     → | Right arrow | Alt+26       | U+2192  | Có nhưng không nên          | Render được, nhưng trong toán phải dùng `\to`     |
|     ⇒ | Implies     | copy từ bảng | U+21D2  | Có                          | Trong toán nên dùng `\Rightarrow`                 |
|     ⇔ | Equivalent  | copy         | U+21D4  | Có                          | Tương đương `\Leftrightarrow`                     |
|     ∀ | For all     | Alt+8704     | U+2200  | Có                          | Dùng Unicode được nhưng macro `\forall` chuẩn hơn |
|     ∃ | Exists      | Alt+8707     | U+2203  | Có                          | Dùng Unicode được nhưng macro `\exists` chuẩn hơn |

## 4. Tập hợp số học (không nên dùng Unicode trực tiếp)

| Ký tự | Tên          | Cách gõ | Unicode | Dùng trực tiếp trong LaTeX? | Ghi chú                                                                        |
| ----: | :----------- | :------ | :------ | :-------------------------- | :----------------------------------------------------------------------------- |
|     ℝ | Real numbers | copy    | U+211D  | Không nên                   | MathJax/LaTeX _hiển thị được_ nhưng không đảm bảo đồng nhất; dùng `\mathbb{R}` |
|     ℤ | Integers     | copy    | U+2124  | Không nên                   | Dùng `\mathbb{Z}` chuẩn hơn                                                    |
|     ℕ | Naturals     | copy    | U+2115  | Không nên                   | Dùng `\mathbb{N}`                                                              |
|     ℚ | Rationals    | copy    | U+211A  | Không nên                   | Dùng `\mathbb{Q}`                                                              |

## **Kết luận quan trọng (mấu chốt về LaTeX/MathJax)**

1. _Hầu hết ký tự toán Unicode có thể dùng trực tiếp_ trong môi trường toán.
2. _Nhưng ZO Math nên ưu tiên macro LaTeX_ vì:

   - đồng nhất giữa HTML và PDF,
   - dễ chỉnh sửa kiểu toán,
   - tránh lỗi font,
   - tránh bị cắt dòng / render sai.

3. Các ký tự có vấn đề khi dùng trực tiếp:

   - √ (không thể làm căn dài)
   - ℝ, ℤ, ℕ, ℚ (không phải dạng blackboard bold thật sự)

---

# Quy chuẩn ZO Math về cách dùng ký hiệu toán và ký tự văn bản

Tài liệu này hướng đến việc xây dựng một phong cách soạn thảo thống nhất, hiện đại, đẹp mắt và đúng chuẩn học thuật, giúp ZO Math giữ được bản sắc riêng và tính chuyên nghiệp trong mọi sản phẩm: bài giảng, website, PDF, sách điện tử, và tài liệu nội bộ.

Bạn có thể xem đây là một _tài liệu nền tảng_ (baseline typography document) cho toàn bộ hệ thống.

## I. Nguyên tắc chung: Văn bản và Toán học phải được tách bạch rõ ràng

Trong mọi tài liệu học thuật, đặc biệt là tài liệu toán, có hai thế giới song song:

- _Thế giới của văn bản_ — nơi từ ngữ, câu cú, dấu câu và ký tự Unicode vận hành theo những quy luật riêng của typography.
- _Thế giới của toán học_ — nơi các biểu thức được sắp đặt bằng LaTeX, tuân thủ chuẩn spacing, glyph, baseline và logic toán.

Hai thế giới này _không dùng chung một hệ thống dấu và ký hiệu_, và vì vậy việc tách bạch không chỉ làm tài liệu đẹp hơn — nó còn giúp người đọc không bị nhầm lẫn giữa “ký hiệu toán” và “kí tự văn bản”.

## II. Các quy chuẩn và ví dụ minh họa

### 1. Không đặt những thứ không phải toán vào math mode

Math mode (`$...$`) có nhiệm vụ duy nhất: _trình bày ký hiệu toán học_.
Dùng nó cho chữ số hoặc từ ngữ dẫn đến văn bản nghiêng, spacing sai và bố cục thiếu tự nhiên.

**❌ Ví dụ sai**

```
Số $121$ có ba chữ số.
```

**✔ Ví dụ đúng**

```
Số 121 có ba chữ số.
```

**Vì sao đúng?**

- `$121$` làm LaTeX hiểu số 121 như một đối tượng toán học, nó nghiêng và spacing lệch so với dòng văn bản.
- Viết **121** là đủ và đẹp.

### 2. Một ký hiệu có hai dạng tùy ngữ cảnh: dạng văn bản và dạng toán học

Nhiều ký hiệu xuất hiện ở cả hai nơi.
Muốn trình bày đúng, phải chọn đúng phiên bản.

**Ví dụ: π**

Trong văn bản:

> Hằng số **π** đóng vai trò quan trọng trong hình học và giải tích.

Trong toán:

```
$\sin(2\pi)$
```

→ Văn bản dùng **π Unicode**
→ Công thức dùng **\pi** (LaTeX), không dùng chữ π trong math mode.

Lý do:

- π trong văn bản đi theo font chữ văn bản.
- \(\pi\) trong toán đi theo font toán học (math italic), spacing chuẩn và đẹp hơn.

Hai dạng trông khác nhau chút ít — và đó là _chủ ý của chuẩn typography toán học_, không phải lỗi.

### 3. Hằng số e: chữ e thường trong văn bản, dạng upright trong toán

Trong văn bản:

> Số **e** khoảng 2.71828.

Trong toán:

```
$\mathrm{e}^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}.$
```

Dùng `\mathrm{e}` để phân biệt với biến số (e) (nếu có).

### 4. Các hàm số: chữ thường trong văn bản, macro trong toán

Trong văn bản:

> Hàm sin là tuần hoàn với chu kỳ (2\pi).

→ Văn bản: **sin**, **cos**, **log**
→ Không dùng `$sin$` hay `$cos$` trong văn bản.

Trong toán:

```
$\sin x,\ \cos x,\ \log a,\ \ln x$
```

Macro LaTeX giúp chữ không bị nghiêng lạ như biến, giúp đọc nhanh hơn.

### 5. Dấu chấm lửng

Typography của toán và văn bản là khác nhau.

**Trong văn bản: dùng Unicode**

```
Ta thấy dãy số tăng rất nhanh…
```

**Trong toán: dùng macro toán học**

```
$1, 2, 3, \ldots, n$
```

→ `\ldots`, `\dots`, `\cdots` tùy ngữ cảnh theo chuẩn amsmath.

### 6. Dấu nhân, dấu chấm, dấu chia

**Trong văn bản:**

> Tốc độ tăng trưởng gấp **3×** so với dự kiến.

**Trong toán:**

```
$2\cdot 3 = 6$
```

LaTeX spacing cho `\cdot` chuẩn hơn dùng ký tự Unicode “·”.

### 7. Mũi tên, suy luận logic

Khi diễn tả trong lời văn, mũi tên chỉ là ký tự:

> Khi thay đổi góc nhìn → ta sẽ thấy điều khác.

Nhưng trong toán:

```
$a = b \Rightarrow f(a) = f(b)$
```

Không dùng Unicode `⇒` trong công thức nếu muốn spacing đẹp và đúng.

### 8. Tên tập hợp số: dùng Unicode trong văn bản, dùng macro trong toán

Trong văn bản:

> Hàm số này xác định trên **ℝ**.

Trong toán (macro chuẩn):

```
$f : \mathbb{R} \to \mathbb{R}$
```

Lý do:

- Unicode ℝ trông giống nhưng _không phải blackboard bold thực thụ_ trong PDF.
- `\mathbb{R}` luôn đúng.

### 9. Dấu ngoặc và dấu gạch ngang

Trong văn bản:

- “ ” — dùng cho trích dẫn
- – (en dash) — dùng cho khoảng
- — (em dash) — dùng cho ngắt câu

Không dùng các dấu này trong công thức toán.

Trong toán chỉ dùng:

```
- + * / ( ) [ ] { }
```

## III. Bảng tổng hợp quy chuẩn

| Ngữ cảnh | Văn bản | Công thức toán | Ghi chú                                 |
| -------- | ------- | -------------- | --------------------------------------- |
| π        | π       | \(\pi\)        | Văn bản dùng Unicode, toán dùng LaTeX   |
| e        | e       | \(\mathrm{e}\) | Dùng upright trong toán                 |
| ∞        | ∞       | \(\infty\)     |                                         |
| ×        | ×       | \(\times\)     | Tránh dùng × trong toán                 |
| ·        | ·       | \(\cdot\)      | LaTeX đẹp hơn nhiều                     |
| sin      | sin     | \(\sin\)       | Văn bản không cần macro                 |
| →        | →       | \(\to\)        | Unicode trong văn bản, macro trong toán |
| ℝ        | ℝ       | \(\mathbb{R}\) | Không dùng ℝ trong toán                 |
| …        | …       | \(\ldots\)     | Không dùng Unicode … trong công thức    |
| số       | 121     | 121            | Không bao giờ dùng `$121$`              |

## IV. Quy tắc vàng ZO Math

1. _Văn bản là văn bản → dùng Unicode._
2. _Toán là toán → dùng LaTeX._
3. Không dùng `$...$` cho từ ngữ hoặc các số bình thường.
4. Với mỗi ký hiệu, hãy chọn _phiên bản phù hợp với ngữ cảnh_.
5. Giữ nhất quán: _một kiểu cho văn bản, một kiểu cho toán_.

## V. Kết luận

Tài liệu này giúp ZO Math đạt được:

- tính nhất quán về mặt hình thức,
- độ rõ ràng trong phân biệt lời văn và biểu thức,
- chất lượng typography cao,
- trải nghiệm đọc tốt trên web và PDF,
- phong cách học thuật chuyên nghiệp giống các textbook quốc tế.

---

Nếu bạn muốn, tôi có thể:

- tạo file `.qmd` hoàn chỉnh với bảng đẹp và cấu trúc rõ,
- tạo phiên bản PDF cho nhóm biên tập dùng nội bộ,
- hoặc thêm phần “Sai lầm thường gặp” và “Test tuân thủ quy chuẩn”.

Bạn muốn phiên bản nào tiếp theo?

---

$\pi < 3.14159\dots$
