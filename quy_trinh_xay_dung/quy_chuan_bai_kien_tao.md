# Quy chuẩn bài viết cho mạch Kiến tạo của ZO Math

**Trạng thái:** Chính thức — tài liệu sống  
**Phạm vi:** Bài viết dài thuộc mạch `Kiến tạo`  
**Đối tượng sử dụng:** Người viết, người biên tập, ChatGPT, Codex và các tác tử AI khác  
**Mẫu khởi tạo:** `quy_trinh_xay_dung/mau_bai_kien_tao.qmd`  
**Bài hiện thực tham chiếu:** `content/kien_tao/diu_dang_va_gai_goc/diu_dang_va_gai_goc.qmd`

Tài liệu này tổng quát hóa những thiết kế đã được chốt qua bài hiện thực tham chiếu. Đây là **house style** của mạch Kiến tạo, không phải yêu cầu để mọi bài có cùng cấu trúc nội dung.

Trong tài liệu này:

- **BẮT BUỘC**: phải tuân thủ;
- **NÊN**: mặc định thực hiện, trừ khi có lí do rõ ràng để làm khác;
- **CÓ THỂ**: lựa chọn theo nội dung và ngữ cảnh;
- **KHÔNG ĐƯỢC**: bị cấm đối với nội dung mới.

## 1. Phạm vi và vai trò của bài Kiến tạo

Bài Kiến tạo là bài viết trình bày một sản phẩm, cách làm, thiết kế, mô hình, công cụ, ý tưởng hoặc kết quả kết tinh từ quá trình xây dựng ZO Math. Sản phẩm có thể thuộc toán học, giáo dục toán học, thiết kế học tập, phần mềm, AI, trực quan hóa, biên tập hoặc một hình thức khác phù hợp với mạch Kiến tạo.

Hình thức không quyết định một nội dung có thuộc Kiến tạo hay không; điều quan trọng là **có một thứ đã được ZO Math tạo ra, phát triển, tổ chức lại hoặc nhìn lại theo cách riêng và có giá trị đủ để trình bày thành một sản phẩm hoàn chỉnh**.

Bài **BẮT BUỘC** làm rõ, theo cách phù hợp với đối tượng của mình:

- sản phẩm hoặc kết quả được trình bày là gì;
- bối cảnh, vấn đề, nhu cầu hoặc câu hỏi làm nó hình thành;
- cách nó được phát triển, tổ chức hoặc kiểm chứng;
- giá trị, giới hạn hoặc ý nghĩa của sản phẩm.

Bài toán học **NÊN** để người đọc nhìn thấy hành trình nhận thức: từ hiện tượng, câu hỏi, trường hợp cụ thể hoặc bằng chứng tới cấu trúc và kết quả. Bài về công cụ, phần mềm hoặc thiết kế **CÓ THỂ** dùng một kiến trúc khác nếu kiến trúc đó diễn đạt sản phẩm tốt hơn.

**KHÔNG ĐƯỢC** biến yêu cầu “có quá trình hình thành” thành một khuôn kể chuyện máy móc cho mọi bài.

## 2. Article shell và YAML

Mỗi bài dài Kiến tạo **BẮT BUỘC** dùng article shell của ZO Math:

```yaml
page-layout: article
toc: true
toc-title: "Nội dung"
toc-location: right
toc-depth: 3
body-classes: "zo-page-article zo-page-kien-tao-article"
```

Các trường tối thiểu **BẮT BUỘC** gồm:

```yaml
title:
summary:
description:
date: last-modified
date-format: "DD-MM-YYYY"
author: "ZO Math"
```

`subtitle` và `abstract` **NÊN** có khi chúng giúp phân biệt nhan đề, lời giới thiệu ngắn và bản tóm tắt đầy đủ; không bắt buộc nếu bài không cần.

`summary` **NÊN** là một câu gọn dùng cho listing/gateway. `description` **BẮT BUỘC** mô tả chính xác nội dung trang. `abstract`, khi có, **NÊN** cho biết đối tượng, hướng phát triển và kết quả chính mà không thay phần dẫn nhập.

Các metadata riêng của mạch hoặc dự án khác, chẳng hạn class ẩn metadata, ảnh thẻ hoặc trường listing đặc thù, **KHÔNG ĐƯỢC** sao chép vào bài Kiến tạo nếu chưa có nhu cầu và hợp đồng tương ứng.

## 3. Sidebar và mục lục ZO Math

Sidebar và mục lục là hai hệ độc lập:

- sidebar điều hướng giữa các trang;
- mục lục được sinh từ heading của chính bài.

Bài dài Kiến tạo **BẮT BUỘC** bật mục lục bằng `toc: true` và giữ article shell của website. **KHÔNG ĐƯỢC** dùng `sidebar: false` để xử lí mục lục.

`toc-depth: 3` là mặc định. **CÓ THỂ** thay đổi khi cấu trúc bài thực sự cần.

Khi xuất bản một bài mới, bài **BẮT BUỘC** được nối vào hệ điều hướng Kiến tạo theo kiến trúc hiện hành của website. Điểm nối đó **CÓ THỂ** là sidebar, gateway, listing, section hoặc cấu trúc con khác; quy chuẩn bài viết không khóa mạch Kiến tạo vào một kiểu điều hướng duy nhất.

Việc tạo hoặc sửa bài **KHÔNG** mặc nhiên cho phép sửa `_quarto.yml`; chỉ sửa cấu hình khi nhiệm vụ có phạm vi tương ứng.

## 4. Title block và metadata

Title block **BẮT BUỘC** cho người đọc nhận biết được nhan đề và metadata xuất bản. `subtitle` và `abstract`, khi có, phải bổ sung ý nghĩa chứ không lặp máy móc `summary` hoặc `description`.

`title` **NÊN** ngắn và có khả năng nhận diện. `subtitle` **NÊN** làm rõ đối tượng, góc nhìn hoặc chuyển động tư tưởng của bài.

Metadata phục vụ máy đọc như `citation` và `zo-pdf-branding` **BẮT BUỘC** nhất quán với title block và URL canonical. Không dùng tiêu đề, URL hoặc tên ngắn thuộc bài khác.

**KHÔNG ĐƯỢC** làm nghèo, xóa hoặc sửa sai metadata nội dung chỉ để xử lí một vấn đề trình bày của HTML/PDF. Nếu phần BibTeX hoặc appendix sinh tự động gây vấn đề thị giác, ưu tiên sửa ở presentation layer hoặc cơ chế canonical tương ứng.

## 5. Cấu trúc nội dung chính

Nội dung chính **BẮT BUỘC** nằm trong reading flow thông thường, dùng heading, đoạn văn, công thức, hình và liên kết nội tại để tạo mạch.

**KHÔNG ĐƯỢC** box mọi kết luận hoặc dùng màu thay cho cấu trúc lập luận.

Một bài toán học có thể gồm:

1. dẫn nhập hoặc động lực;
2. các chặng phát triển;
3. kiểm chứng, lập luận hoặc chứng minh;
4. kết quả tổng hợp;
5. bài tập nếu bài có chức năng học tập.

Một bài về công cụ hoặc sản phẩm có thể gồm:

1. vấn đề hoặc nhu cầu;
2. sản phẩm;
3. cơ chế hoặc thiết kế;
4. ví dụ sử dụng;
5. giới hạn, kết quả hoặc hướng phát triển.

Các danh sách trên là **khung chức năng**, không phải mục lục bắt buộc.

Heading **NÊN** gọi đúng ý tưởng đang phát triển. ID tường minh như `{#sec-ten-muc}` **NÊN** được dùng khi mục được tham chiếu bằng cross-reference.

## 6. Nội dung phụ và nguyên tắc collapsible

Chỉ nội dung không phải mắt xích bắt buộc của mạch chính mới **CÓ THỂ** đặt trong `<details>`.

Nội dung phụ dài thường phù hợp với collapsible khi việc mở thường trực làm gián đoạn reading flow. Độ dài không tự nó quyết định trạng thái.

Nội dung dài nhưng cần để hiểu phần tiếp theo **BẮT BUỘC** để trong mạch chính hoặc trong khối mở cố định. Nội dung ngắn không có chức năng tách biệt **KHÔNG ĐƯỢC** bọc khối chỉ để trang trí.

Thuộc tính `open` **CÓ THỂ** dùng để khối phụ mở sẵn, nhưng không biến nội dung ấy thành mắt xích bắt buộc.

Khối phụ **BẮT BUỘC** nằm gần nhất với nội dung mà nó soi sáng; không gom các khối theo màu hoặc theo trạng thái thu gọn.

## 7. Hệ khối canonical

Mọi khối mới **BẮT BUỘC** dùng lớp chung `zo-block` và đúng một lớp màu:

- `zo-block-red`;
- `zo-block-yellow`;
- `zo-block-gray`.

Tiêu đề dùng `zo-block-title`; phần thân của `<details>` dùng `zo-block-body`.

### 7.1. Khối đỏ

Đỏ biểu thị **lí thuyết hoặc kết quả chung có khả năng tái sử dụng**: định nghĩa, định lí, mệnh đề, hệ quả, tính chất hoặc điều kiện chung.

Một kết luận chỉ đúng cho đối tượng đang xét **KHÔNG ĐƯỢC** chuyển thành đỏ chỉ vì nó quan trọng.

Khối đỏ **NÊN** mở cố định trong reading flow. Không thu gọn một kết quả mà người đọc phải dùng để hiểu phần tiếp theo.

### 7.2. Khối vàng

Vàng biểu thị một bài viết nhỏ tương đối độc lập có chức năng khám phá, mở rộng, liên tưởng hoặc kết nối.

Ví dụ hay bài tập không mặc nhiên là khối vàng.

### 7.3. Khối xám

Xám biểu thị nội dung hỗ trợ phụ thuộc ngữ cảnh: giải thích bổ trợ, chứng minh phụ, chi tiết kĩ thuật, cách hiểu nâng cao, gợi ý, lời giải hoặc đáp án.

Một chứng minh là mắt xích bắt buộc của lập luận **BẮT BUỘC** ở reading flow; **KHÔNG ĐƯỢC** đưa vào khối xám chỉ vì nó là “chứng minh”.

### 7.4. Trạng thái, màu và hover

Trạng thái mở/thu gọn và màu là hai quyết định độc lập.

**BẮT BUỘC** quyết định trạng thái theo vai trò trong mạch đọc trước, rồi mới quyết định màu theo chức năng nhận thức.

Màu **KHÔNG ĐƯỢC** biểu thị “chính/phụ”, độ quan trọng hoặc sở thích thẩm mĩ.

Hover của summary **BẮT BUỘC** chỉ tăng cường độ trong cùng họ màu canonical. Nội dung QMD **KHÔNG ĐƯỢC** ghi style inline hoặc đổi hover sang một họ màu khác.

### 7.5. Khi không dùng block

Không dùng block nếu:

- heading và văn xuôi đã diễn đạt rõ vai trò;
- nội dung chưa tạo thành một đơn vị tương đối trọn vẹn;
- mục đích duy nhất là “làm nổi bật”.

Công thức quan trọng được nhấn bằng vị trí và mạch văn; **KHÔNG ĐƯỢC** dùng `\boxed{...}` chỉ để trang trí.

## 8. Bài tập

Bài tập **KHÔNG BẮT BUỘC** đối với mọi bài Kiến tạo.

Nếu bài có bài tập, các bài tập **BẮT BUỘC** được gom dưới một mục cấp hai duy nhất:

```markdown
## Bài tập
```

Mục này **BẮT BUỘC** nằm ở cuối phần nội dung chính, trước tài liệu tham khảo và appendix do Quarto sinh.

Bài tập **NÊN** tiếp tục, kiểm tra hoặc mở rộng điều bài vừa xây dựng; không nên là một danh sách ngẫu nhiên.

Mỗi bài **NÊN** dùng cross-reference canonical như:

```markdown
::: {#exr-1}
...
:::
```

**CÓ THỂ** chia bài tập thành các nhóm cấp ba hoặc cấp bốn nếu cần.

## 9. Hình ảnh và đồ thị

Mỗi hình **BẮT BUỘC** có vai trò rõ, caption và ID ổn định nếu được tham chiếu.

`fig-alt` **BẮT BUỘC** mô tả đủ để người không nhìn thấy hình hiểu nội dung thiết yếu.

Văn bản **NÊN** dẫn tới hình bằng cross-reference thay vì các cụm mơ hồ như “hình dưới đây” khi thứ tự hiển thị có thể thay đổi.

Đường dẫn tài nguyên **BẮT BUỘC** portable trong repository. Không hard-code đường dẫn máy cá nhân.

Width trong QMD chỉ điều khiển cách một hình **đã đúng geometry** được đặt trong layout; không phải công cụ sửa bản thân hình.

Một hình không cần nhánh riêng **CÓ THỂ** dùng cú pháp figure Quarto thông thường. Chỉ tạo nhánh HTML/PDF khi hai đầu ra cần asset hoặc layout khác nhau.

## 10. TikZ/source geometry

Đối với hình sinh từ TikZ, PGFPlots hoặc nguồn geometry khác, geometry **BẮT BUỘC** được sửa ở source rồi tái sinh asset.

**KHÔNG ĐƯỢC** dùng `width`, global scale trong QMD, crop ngẫu nhiên hoặc CSS để che lỗi khoảng trắng, tỉ lệ, bounding box, vị trí nhãn hay bố cục bên trong hình.

Source **NÊN** là nguồn duy nhất cho các asset SVG/PDF tương ứng và phải được giữ để có thể tái sinh.

Khi sửa hình, **BẮT BUỘC** kiểm tra:

1. source;
2. asset sinh;
3. HTML;
4. PDF.

Không sửa trực tiếp SVG/PDF nếu đã xác định được nguồn sinh.

Khi một nhóm hình cùng loại được trình bày trong một bài, **NÊN** tinh chỉnh các thông số như cỡ chữ, khoảng cách, bounding box và trọng lượng thị giác theo cùng một hệ để tránh cảm giác mỗi hình thuộc một thiết kế khác nhau.

## 11. HTML/PDF figure branches

HTML **NÊN** ưu tiên SVG. PDF **BẮT BUỘC** dùng asset PDF khi hình có canonical PDF branch.

Mẫu thông thường:

```markdown
:::: {.content-visible when-format="html"}
::: {#fig-ten-hinh}
![](duong-dan/hinh.svg){fig-alt="Mô tả hình." fig-align="center" width="100%"}

Chú thích hình.
:::
::::

:::: {.content-visible when-format="pdf"}
::: {#fig-ten-hinh}
![](duong-dan/hinh.pdf){fig-alt="Mô tả hình." fig-align="center" width="85%"}

Chú thích hình.
:::
::::
```

Hai nhánh **BẮT BUỘC** có cùng figure ID, cùng ý nghĩa và caption tương ứng.

Khác biệt width **CÓ THỂ** dùng để thích ứng layout sau khi geometry nguồn đã đúng. `100%` và `85%` chỉ là ví dụ từ reference implementation, không phải hằng số toàn mạch.

### 11.1. Ngoại lệ figure trong block/collapsible

Không bắt buộc hai nhánh HTML/PDF phải đối xứng tuyệt đối về vị trí source.

Nếu HTML figure nằm trong `<details>` hoặc `zo-block` nhưng PDF figure gây lỗi float/tcolorbox, chẳng hạn `Not in outer par mode`, **BẮT BUỘC** ưu tiên đầu ra PDF đúng hơn sự đối xứng source.

Trong trường hợp đó:

- nhánh HTML **CÓ THỂ** ở lại trong block;
- nhánh PDF **CÓ THỂ** đặt ngay sau block;
- hai nhánh vẫn **BẮT BUỘC** giữ cùng figure ID, caption, ý nghĩa và quan hệ logic với nội dung;
- không đưa figure PDF ra một vị trí xa khiến quan hệ đọc bị thay đổi.

Nguyên tắc: **tương đương logic giữa các đầu ra quan trọng hơn đối xứng hình thức trong source**.

Layout như `column-screen-inset-shaded` hoặc `layout-ncol` **CÓ THỂ** dùng khi hình thực sự cần; không phải mặc định của mọi bài.

## 12. Chú âm tên và thuật ngữ nước ngoài

Trước khi thêm chú âm, **BẮT BUỘC** tra:

- `quy_trinh_xay_dung/tu_dien_chu_am_zo_math.yml`;
- `quy_trinh_xay_dung/quy_chuan_chu_am_zo_math.md`.

Mục `approved` được dùng nguyên văn. Mục `trial` chỉ dùng trong `trial_scope`. Mục `needs_review`, `research` hoặc trường hợp chưa có authority **KHÔNG ĐƯỢC** tự xuất bản như chú âm canonical.

Chú âm mặc định xuất hiện ở lần có ý nghĩa đầu tiên trong thân bài:

```text
Dạng viết (chú âm Việt)
```

Tiêu đề, phụ đề, metadata và bibliography không tính là lần xuất hiện có ý nghĩa đầu tiên.

Không lặp chú âm cơ học. Không mặc định mọi tên nước ngoài được đọc theo tiếng Anh.

## 13. Tài liệu tham khảo và trích dẫn

`bibliography` **CHỈ BẮT BUỘC KHI BÀI SỬ DỤNG NGUỒN NGOÀI**.

Khi có nguồn:

```yaml
bibliography: references.bib
```

và trích dẫn bằng cú pháp Quarto, chẳng hạn:

```markdown
[@citation_key]
```

`nocite` **CÓ THỂ** dùng khi một nguồn cần hiện trong danh mục dù không có citation trực tiếp.

References/danh mục tài liệu tham khảo **BẮT BUỘC** để Quarto sinh từ metadata và tệp BibTeX. **KHÔNG ĐƯỢC** dựng thủ công một mục “Tài liệu tham khảo” nếu không có lí do đặc biệt đã được ghi rõ.

Metadata `citation` của **chính trang** là một vấn đề khác với `bibliography`: bài có thể khai báo `citation` cho trang dù không dùng nguồn ngoài.

`citation` **BẮT BUỘC** khớp nhan đề, publisher và URL canonical của bài.

Class `zo-page-kien-tao-article` cho phép presentation layer của Kiến tạo ẩn phần BibTeX sinh tự động mà không làm mất metadata citation. **KHÔNG ĐƯỢC** xóa abstract, citation metadata hoặc dữ liệu BibTeX hợp lệ chỉ để làm appendix ngắn hơn hay đẹp hơn.

## 14. PDF canonical và nút Tải PDF

Đối với bài Kiến tạo dài được xuất bản như một bài hoàn chỉnh, **NÊN** có PDF canonical. Khi bài có PDF, **BẮT BUỘC** dùng cơ chế ZO Math:

```yaml
zo-pdf-download:
  href: "<slug>.pdf"
  label: "Tải PDF"

zo-pdf-branding:
  collection: "Kiến tạo"
  short-title: "<tên ngắn>"
  canonical-url: "https://zomath.vn/content/kien_tao/<slug>/<slug>.html"
  display-url: "zomath.vn"
```

`href` **BẮT BUỘC** trỏ tới PDF canonical của bài, mặc định đặt cạnh QMD theo pipeline hiện hành.

PDF **KHÔNG ĐƯỢC** dựng bằng lệnh Quarto tùy ý nếu pipeline canonical hỗ trợ bài đó. Dùng:

```text
python scripts/zo_python.py scripts/zo_pdf.py build <duong-dan-bai.qmd>
python scripts/zo_python.py scripts/zo_pdf.py status <duong-dan-bai.qmd>
```

Trước bàn giao **BẮT BUỘC**:

- status current;
- mở PDF thật;
- kiểm tra mọi trang;
- kiểm tra figure, block, caption, bibliography và overflow/crop.

Kiểm tra text hoặc build PASS không thay thế kiểm tra thị giác.

Nếu một bài có lí do chính đáng không cung cấp PDF, **KHÔNG ĐƯỢC** giữ `zo-pdf-download` trỏ tới file không tồn tại.

## 15. Responsive/mobile

Bài **BẮT BUỘC** đọc được trên desktop và mobile, không có tràn ngang ngoài chủ ý.

Các khối canonical tự giảm padding ở viewport nhỏ; nội dung **KHÔNG ĐƯỢC** ghi width cố định hoặc style inline phá vỡ cơ chế ấy.

Hình, bảng, công thức dài và layout nhiều cột **BẮT BUỘC** được kiểm tra riêng ở mobile. SVG dùng trên HTML phải co giãn theo container.

Sidebar và TOC **BẮT BUỘC** giữ đúng hành vi dùng chung; không được chồng lên nhau hoặc tạo một hệ TOC riêng chỉ cho một bài.

Render thành công không đủ để kết luận responsive đạt; **BẮT BUỘC** kiểm tra trực quan ở các viewport mục tiêu của quy trình áp dụng.

## 16. Các pattern legacy bị cấm

Đối với nội dung mới, **KHÔNG ĐƯỢC** dùng:

- `highlight-box-*`, gồm `highlight-box-soft-red` và `highlight-box-honey-gold`;
- `collapsible-box-*` hoặc `.details` cũ khi `zo-block` đáp ứng chức năng;
- Quarto callout cũ để thay một khối canonical tương đương;
- màu inline, icon trang trí, dải nhấn bên trái hoặc bóng đổ rõ cho khối;
- màu để biểu thị “chính/phụ” hoặc mức quan trọng;
- `\boxed{...}` chỉ để nhấn công thức;
- references, citation hoặc nút PDF dựng thủ công khi cơ chế canonical đã có;
- `sidebar: false` để tắt mục lục;
- width/global scale trong QMD để che lỗi geometry của hình.

Các lớp legacy còn trong CSS chỉ nhằm tương thích. **KHÔNG ĐƯỢC** suy ra rằng sự tồn tại của chúng cho phép dùng trong bài mới.

## 17. Checklist kiểm định

### 17.1. Nguồn và metadata

- [ ] Bài đúng phạm vi Kiến tạo.
- [ ] `title`, `summary`, `description`, `author`, `date`, `date-format` đầy đủ.
- [ ] `page-layout`, TOC và `body-classes` đúng article shell.
- [ ] `citation` nhất quán với title và URL canonical.
- [ ] Nếu có PDF: `zo-pdf-download` và `zo-pdf-branding` nhất quán với slug, title và URL.
- [ ] Nếu dùng nguồn ngoài: `bibliography` tồn tại và mọi citation key được định nghĩa.
- [ ] Không có metadata bị xóa hoặc làm sai chỉ để xử lí presentation.

### 17.2. Nội dung

- [ ] Reading flow giữ nội dung bắt buộc ngoài collapsible.
- [ ] Mỗi block có lí do, trạng thái và màu đúng chức năng.
- [ ] Chứng minh bắt buộc không bị đưa vào khối xám chỉ vì là chứng minh.
- [ ] Nếu có bài tập: chỉ có một `## Bài tập` ở cuối phần nội dung chính.
- [ ] Chú âm đã tra authority và chỉ dùng trạng thái được phép.

### 17.3. Hình và đầu ra

- [ ] Mọi figure có caption, `fig-alt` và ID khi cần tham chiếu.
- [ ] Geometry đúng từ source; asset SVG/PDF đồng bộ.
- [ ] Các hình cùng nhóm có trọng lượng thị giác nhất quán.
- [ ] Nhánh HTML ưu tiên SVG; nhánh PDF dùng PDF canonical khi có.
- [ ] Figure trong block/collapsible đã được kiểm tra riêng trên PDF.
- [ ] Không có `Not in outer par mode`, crop hoặc overflow.
- [ ] HTML không tràn ngang ở các viewport mục tiêu.
- [ ] Sidebar và TOC hoạt động đúng.
- [ ] Nếu có PDF: pipeline canonical PASS, status current và PDF đã được xem trực quan.
- [ ] Không có pattern legacy bị cấm.
- [ ] Git diff chỉ chứa tệp thuộc phạm vi nhiệm vụ.

## 18. Quy trình tạo hoặc chuẩn hóa một bài Kiến tạo

1. **Xác lập sản phẩm.** Ghi rõ thứ bài muốn trình bày, bối cảnh hình thành, người đọc và giá trị chính.
2. **Nạp authority.** Đọc tài liệu này, template, chuẩn block, sidebar/TOC, chú âm và các chuẩn chuyên biệt liên quan.
3. **Khảo sát hiện trạng.** Xác định thư mục, slug, điều hướng, asset, nguồn sinh, bibliography, PDF và dirty worktree cần bảo vệ.
4. **Khởi tạo hoặc chuẩn hóa shell.** Dùng `mau_bai_kien_tao.qmd` như nguồn tham khảo; không sao chép máy móc các component không cần.
5. **Thiết kế mạch.** Xác định reading flow, nội dung phụ, vị trí hình, block, bài tập nếu có.
6. **Viết và tạo asset.** Tạo hình từ source; tra authority trước khi chú âm; thêm bibliography chỉ khi có nguồn.
7. **Kiểm định source.** Kiểm tra YAML, cross-reference, citation, đường dẫn, class canonical và pattern bị cấm.
8. **Dựng đầu ra.** Render HTML và, nếu bài có PDF, dựng bằng pipeline canonical.
9. **Kiểm tra trực quan.** Xem desktop, mobile và toàn bộ PDF; đặc biệt kiểm tra figure nằm trong block/collapsible.
10. **Bàn giao.** Đọc diff, xác nhận phạm vi, báo kết quả. Không commit hoặc publish nếu chưa được yêu cầu.

## 19. Ngoại lệ và những điều không tổng quát hóa từ bài tham chiếu

Các thiết kế sau có thể hợp lệ trong một bài cụ thể nhưng **KHÔNG** trở thành chuẩn chung:

- R setup với `knitr`, `kableExtra`, `dplyr`, `MASS` hoặc các gói khác;
- tooltip Bootstrap và footnote song song;
- lối xưng hô, nhan đề ẩn dụ, tên các chặng và số lượng mục cụ thể;
- `nocite` cho một nguồn cụ thể;
- `column-screen-inset-shaded`, lưới hai cột và các layout đặc thù;
- width `85%`/`100%` cụ thể của một hình;
- bounding box hoặc thông số TikZ cụ thể của Hình 3–6;
- việc một figure HTML nằm trong block trong khi figure PDF đặt ngay sau block: đây là workaround có nguyên tắc cho trường hợp cần thiết, không phải layout mặc định;
- đường dẫn asset cụ thể của bài tham chiếu;
- mọi lỗi nội dung, chính tả, công thức hoặc khác biệt lịch sử có thể còn tồn tại trong reference implementation.

Reference implementation là bằng chứng về những quyết định đã được chốt; **không phải nguồn cho phép sao chép mọi chi tiết**.

## 20. Ma trận đối chiếu với reference implementation

| RULE                 | REFERENCE_EVIDENCE                                            | DOCUMENTED_IN_STANDARD | REPRESENTED_IN_TEMPLATE               |
| -------------------- | ------------------------------------------------------------- | ---------------------- | ------------------------------------- |
| Metadata             | title, subtitle, summary, description, abstract, author, date | Mục 2 và 4             | Có, với trường tùy chọn được đánh dấu |
| TOC/sidebar          | `page-layout: article`, TOC phải, depth 3                     | Mục 3                  | Có                                    |
| Reading flow         | Nội dung chính không bị box hàng loạt                         | Mục 5–6                | Có hướng dẫn                          |
| Content blocks       | đỏ mở cố định; vàng/xám cho nội dung phụ                      | Mục 7                  | Có component tùy chọn                 |
| Exercises            | Bài tham chiếu gom bài tập ở cuối                             | Mục 8                  | Component tùy chọn                    |
| Figures              | SVG HTML, PDF asset cho PDF, geometry sửa ở source            | Mục 9–11               | Có mẫu hai nhánh                      |
| Figure/PDF exception | Hình 6 cần nhánh PDF ngoài block để tránh lỗi float/tcolorbox | Mục 11.1               | Có cảnh báo và mẫu                    |
| Pronunciation        | Pascal, Stirling, sigma dùng authority                        | Mục 12                 | Có chỉ dẫn                            |
| Bibliography         | Có bibliography/nocite vì bài dùng nguồn                      | Mục 13                 | Tùy chọn                              |
| Citation appendix    | Quarto sinh, presentation xử lí BibTeX                        | Mục 13                 | Có metadata citation                  |
| PDF/download         | `zo-pdf-download`, branding, PDF cạnh bài                     | Mục 14                 | Có mặc định                           |
| Responsive           | article shell, block responsive, figure co giãn               | Mục 15                 | Có cấu trúc tương thích               |

## 21. Bảo trì quy chuẩn

Quy chuẩn này là tài liệu sống.

Khi một bài Kiến tạo mới làm phát sinh trường hợp mà tài liệu chưa bao quát:

1. xác định đó là ngoại lệ riêng hay một quy tắc có khả năng tái sử dụng;
2. nếu là quy tắc tái sử dụng, cập nhật tài liệu này và template;
3. nếu là workaround riêng, ghi rõ trong bài hoặc quy trình liên quan nhưng không biến thành mặc định toàn mạch;
4. không duy trì các bản `v1`, `v2`, `final`, `final2`; Git là lịch sử thay đổi.
