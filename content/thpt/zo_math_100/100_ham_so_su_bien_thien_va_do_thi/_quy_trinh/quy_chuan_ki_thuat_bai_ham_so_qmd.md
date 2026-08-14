# Quy chuẩn kĩ thuật bài hàm số QMD

**Trạng thái:** Bản tinh gọn để đối chiếu và chốt
**Phạm vi:** Các bài khảo sát một hàm số cụ thể trong dự án **100+ Hàm số: Sự biến thiên và đồ thị**

## 1. Mục đích, phạm vi và thẩm quyền

Tài liệu này quy định **hợp đồng đầu ra kĩ thuật** của một bài `.qmd` về một hàm số cụ thể trong dự án.

Tài liệu điều chỉnh:

- YAML và metadata;
- cấu trúc Markdown/Quarto của thân bài;
- mã thực thi và phụ thuộc;
- việc dùng hệ khối nội dung;
- đường dẫn, hình, bảng và tài nguyên;
- cấu trúc kĩ thuật của hệ bài tập khi được kích hoạt;
- PDF tải xuống;
- cấu trúc cũ và giá trị bị cấm;
- kiểm định tự động, kiểm định có người quan sát và nghiệm thu kĩ thuật.

Tài liệu này **không quyết định**:

- nội dung toán học cần khảo sát;
- hiện tượng trung tâm;
- mạch lập luận và trật tự nhận thức;
- chức năng nhận thức của bảng, hình hoặc bài tập;
- phương pháp dựng đồ thị TikZ/PGFPlots;
- giọng và phong cách văn xuôi.

Những phần ấy thuộc các tài liệu chuyên trách sau:

| Tài liệu                                                             | Thẩm quyền trực tiếp                                                               |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `_quy_trinh/quy_chuan_khao_sat_ham_so.md`                            | Nội dung toán học, hiện tượng, mạch lập luận, kiến trúc bài và nghiệm thu nội dung |
| `_quy_trinh/quy_trinh_tao_bai_ham_so.md`                             | Trình tự sản xuất, điểm kiểm soát và phạm vi bàn giao                              |
| `_quy_trinh/mau_ki_thuat_qmd.qmd`                                    | Khung YAML và các mẫu cú pháp kĩ thuật hiện hành                                   |
| `quy_trinh_xay_dung/huong_dan_su_dung_khoi_noi_dung.md`              | Sự cần thiết, trạng thái, màu, cú pháp và chuyển đổi hệ khối                       |
| `quy_trinh_xay_dung/quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md` | Phân tích, sinh nguồn, render và nghiệm thu đồ thị TikZ/PGFPlots                   |
| Tài liệu phong cách được chỉ định                                    | Giọng, nhịp, ngôn ngữ và thẩm mĩ của văn xuôi                                      |

Khi các chỉ dẫn cùng điều chỉnh một vấn đề, áp dụng theo thứ tự:

1. yêu cầu hiện tại của người dùng;
2. `AGENTS.md` ở gốc repository và `AGENTS.md` trong dự án;
3. quy trình sản xuất bài hàm số;
4. quy chuẩn khảo sát hàm số;
5. quy chuẩn kĩ thuật này;
6. tài liệu chuyên trách được quy chuẩn chuyển giao;
7. mẫu kĩ thuật.

`depth/ham_sin_mot_tren_x.qmd` chỉ là **tham chiếu kĩ thuật đã được chấp thuận** tại thời điểm xây dựng quy chuẩn. Không sao chép mục lục, tên đề mục hoặc kiến trúc nội dung của bài ấy sang bài khác.

## 2. Loại quy tắc và ngôn ngữ kết quả

### 2.1. Ba loại quy tắc

Mỗi quy tắc thuộc một trong ba loại:

1. **Bắt buộc:** mọi bài trong phạm vi áp dụng phải đạt.
2. **Kích hoạt theo điều kiện:** chỉ áp dụng khi hồ sơ sản xuất, trạng thái xuất bản hoặc thành phần của bài kích hoạt.
3. **Cấm đối với nội dung mới:** cấu trúc lịch sử có thể còn được hỗ trợ để tương thích, nhưng không được dùng khi tạo nội dung mới.

Không dùng _không áp dụng_ để tránh một đầu ra bắt buộc.

### 2.2. Ba mức phát hiện

Mỗi phát hiện kĩ thuật phải được phân loại:

- **Lỗi chặn:** phải sửa trước nghiệm thu.
- **Cảnh báo cần xét:** cần người kiểm định đọc ngữ cảnh và ghi quyết định.
- **Thông tin:** không chặn nghiệm thu nhưng cần ghi để bảo trì hoặc giao việc sau.

### 2.3. Trạng thái kiểm định tự động

Tầng tự động dùng các trạng thái:

- `FAIL` — còn lỗi chặn;
- `PASS_WITH_WARNINGS` — hết lỗi chặn nhưng còn cảnh báo chưa xét;
- `PASS` — hết lỗi chặn và các cảnh báo đã được xử lí hoặc chuyển rõ sang tầng quan sát;
- `NOT_RUN` — chưa chạy;
- `NOT_APPLICABLE` — không áp dụng và đã có lí do.

`PASS` của công cụ không phải kết luận nghiệm thu cuối.

### 2.4. Trạng thái nghiệm thu cuối

Báo cáo cuối chỉ dùng:

```text
ĐẠT
KHÔNG ĐẠT
CHƯA ĐỦ BẰNG CHỨNG
```

## 3. Hợp đồng đầu ra kĩ thuật

### 3.1. YAML và metadata

#### 3.1.1. Nguồn cấu trúc

Khi tạo bài mới, dùng `_quy_trinh/mau_ki_thuat_qmd.qmd` làm khung kĩ thuật. Không sao chép YAML từ một bài nội dung khác rồi chỉ thay `title`.

Mọi giá trị phải được suy ra từ chính bài, đường dẫn QMD, mục tương ứng trong `_data/cards.yml` và trạng thái xuất bản.

#### 3.1.2. Các trường bắt buộc

Mọi bài khảo sát một hàm số phải có các trường sau trước khi nghiệm thu:

**Nhận diện và mô tả**

- `title`;
- `title-meta`;
- `subtitle`;
- `pagetitle`;
- `summary`;
- `description`;
- `abstract`;
- `keywords`;
- `author: "ZO Math"`;
- `date: last-modified`;
- `date-format: "DD-MM-YYYY"`.

**Thẻ dự án**

- `image`;
- `listing-order`.

**Bố cục trang**

- `page-layout: article`;
- `toc: true`;
- `toc-title: "Nội dung"`;
- `toc-location: right`;
- `toc-depth: 3`;
- `body-classes` chứa đồng thời `zo-page-article` và `zo-meta-hidden`.

**PDF tải xuống**

- `zo-pdf-download`;
- `zo-pdf-branding`.

Có thể bổ sung trường khác khi dự án hoặc nhiệm vụ yêu cầu, nhưng không được bỏ trường bắt buộc.

#### 3.1.3. Quan hệ giữa các trường

Phải bảo đảm:

- `title` gọi đúng hàm và có thể chứa công thức;
- `pagetitle` là tiêu đề văn bản thuần gọn cho tab/trình duyệt, không phụ thuộc khả năng hiển thị LaTeX; biểu thức phải được chuyển sang dạng văn bản đọc đúng về toán học, ưu tiên Unicode chuẩn khi có biểu diễn trực tiếp (ví dụ `x²` thay cho chuỗi nguồn `x^2`); không tự thêm hậu tố `ZO Math` nếu cấu hình site đã thêm hậu tố;
- `subtitle` gọi đúng trục nhận thức hoặc hiện tượng trung tâm, đủ đặc trưng cho chính bài, không dùng khẩu hiệu quảng bá hoặc một ẩn dụ chung chung có thể gắn cho nhiều bài; không chứa một quan hệ chưa được xác lập;
- `summary` nén cách nhìn hoặc kết luận trung tâm của bài, không biến thành danh sách thuật ngữ và không lặp nguyên văn `description`;
- `description` là lời giới thiệu bằng văn xuôi, nói được nội dung đáng đọc hoặc cách nhìn mà bài đem lại; không dùng như mục lục hay danh sách từ khóa; công thức toán trong trường này phải dùng cú pháp LaTeX phù hợp;
- `abstract` phát triển lời giới thiệu ở mức dài hơn khi cần, không lặp máy móc `summary` hoặc `description` và không mô tả nội dung không có trong bài;
- `keywords` là nơi chứa các khái niệm hoặc thuật ngữ tìm kiếm thực sự có vai trò;
- `listing-order` khớp `number` của thẻ tương ứng;
- `image` trong QMD khớp tài nguyên `image` của thẻ sau khi chuẩn hóa tiền tố đường dẫn `/content/.../`;
- `author`, `date` và `abstract` vẫn được giữ làm metadata nhưng không hiện ngoài ý muốn trên HTML;
- `zo-pdf-download.href` gọi đúng PDF của bài;
- `zo-pdf-branding.short-title` gọi đúng bài;
- `zo-pdf-branding.canonical-url` được suy ra từ đường dẫn QMD sau khi đổi `.qmd` thành `.html`;
- `zo-pdf-branding.display-url` dùng giá trị hiện hành của dự án.

#### 3.1.4. Tiêu đề theo từng đầu ra

Các trường tiêu đề có vai trò riêng và không được dùng thay thế lẫn nhau:

- `title`: tiêu đề hiển thị của bài; được phép chứa công thức TeX;
- `subtitle`: phụ đề hiển thị; được phép chứa công thức TeX khi cần;
- `pagetitle`: tiêu đề tab trình duyệt; dùng văn bản thuần, không chứa TeX;
- `title-meta`: tiêu đề metadata của PDF; dùng văn bản thuần, không chứa TeX;
- `zo-pdf-branding.short-title`: tiêu đề chạy ở đầu trang PDF; được phép chứa công thức TeX.

Khi `title` chứa lệnh toán học như `\ln`, không được dùng trực tiếp trường này làm metadata PDF. Phải khai báo `title-meta` riêng để tránh mất lệnh toán học khi Hyperref chuyển tiêu đề sang chuỗi metadata.

#### 3.1.5. Giá trị giữ chỗ

Không được còn giá trị giữ chỗ trong bài bàn giao, gồm các biến thể của:

```text
CHƯA XÁC ĐỊNH
CHUA_XAC_DINH
CHON_MAU
TIÊU ĐỀ KHỐI
TEN_TEP
TÊN_TỆP
URL_HTML_CHÍNH_TẮC
DUONG_DAN_DEN_TEP_QMD
DUONG_DAN_DEN_TEP_PDF
```

Quy tắc này áp dụng cho bài QMD sản xuất, không áp dụng cho chính tài liệu hướng dẫn hoặc mẫu kĩ thuật đang minh họa các giá trị ấy.

### 3.2. Cấu trúc thân bài và tiêu đề

#### 3.2.1. Tiêu đề cấp cao nhất

`title` trong YAML là tiêu đề cấp cao nhất của trang. Sau YAML, thân bài không được có H1.

Không dùng:

```markdown
# Khảo sát hàm số ...

# Bài tập

# Lời giải
```

Phát hiện H1 thật trong thân bài là lỗi chặn. Dấu `#` nằm trong code block hoặc ví dụ minh họa không phải tiêu đề thật.

#### 3.2.2. Hệ tiêu đề

Hệ mặc định gồm:

- H2: một phần hoặc chuyển động nhận thức lớn;
- H3: một mạch cục bộ trong H2;
- H4: một đơn vị phụ thuộc rõ ràng, trường hợp hoặc bài tập cụ thể.

Không nhảy cấp. Không dùng H5 hoặc H6 nếu chưa có nhu cầu đặc biệt và kiểm tra trực quan.

Tên đề mục phải phát sinh từ mạch của chính bài. Không mặc định dùng một checklist như “Tập xác định — Đạo hàm — Bảng biến thiên — Đồ thị”.

#### 3.2.3. Tiêu đề thật và tiêu đề khối

Không dùng lớp hoặc cấu trúc trình bày để giả lập tiêu đề Markdown, đặc biệt:

```text
.tieu-de-chu-thich
```

Nếu nội dung là một phần của kiến trúc bài, dùng tiêu đề Markdown đúng cấp. Nếu nội dung chỉ là tên của một khối, dùng `zo-block-title`; tiêu đề khối không mặc định xuất hiện trong mục lục.

#### 3.2.4. Mục lục

Mục lục phải được sinh từ hệ tiêu đề thật. Với `toc-depth: 3`, H2 và H3 xuất hiện trong mục lục; H4 có thể tồn tại trong thân bài nhưng không mặc định xuất hiện.

Không thay đổi `toc-depth` để che một kiến trúc đề mục quá sâu hoặc thiếu tổ chức.

### 3.3. Mã thực thi và phụ thuộc

#### 3.3.1. Nguyên tắc mặc định

Bài xuất bản ưu tiên nội dung tĩnh và tài nguyên đã được tạo, kiểm tra rồi lưu trong repository.

Chỉ giữ code chunk khi mã có chức năng xác định, chẳng hạn:

- tạo bảng, dữ liệu hoặc kết quả cần tái tạo;
- tạo tài nguyên được bài sử dụng trực tiếp;
- thực hiện phép tính không phù hợp để chép thủ công;
- minh họa mã khi bản thân mã là nội dung học tập.

Không thêm code chunk chỉ để chuẩn bị cho khả năng dùng về sau.

#### 3.3.2. Yêu cầu đối với mỗi chunk

Mỗi code chunk phải truy được:

- mục đích;
- đầu vào;
- đầu ra;
- phụ thuộc;
- tệp đọc hoặc ghi;
- cách tái tạo và kiểm tra;
- lí do ẩn hoặc hiện mã.

Chunk không tạo ra nội dung hoặc tài nguyên được bài sử dụng phải bị loại bỏ.

#### 3.3.3. Cấu trúc bị cấm

Không đặt trong QMD xuất bản:

- lệnh cài thư viện;
- `setwd()` hoặc thao tác tương đương;
- đường dẫn tuyệt đối phụ thuộc một máy;
- thông tin đăng nhập, khóa truy cập hoặc dữ liệu bí mật;
- lời gọi mạng không cần thiết;
- mã thử nghiệm, mã tạm hoặc mã bị vô hiệu hóa nhưng vẫn để lại;
- thư viện không sử dụng;
- thông báo thư viện, cảnh báo hoặc đầu ra chẩn đoán ngoài ý muốn.

Khối `setup` chỉ tồn tại khi có chunk khác thực sự phụ thuộc vào thiết lập ấy.

#### 3.3.4. Cache và đầu ra

Cache, log và tệp tạm không phải tài nguyên bàn giao. Không dùng `_cache`, `_freeze`, `_audit` hoặc sản phẩm trung gian làm nguồn chính thức của bài.

Nếu mã tạo tài nguyên, nguồn, đầu ra, đường dẫn trong QMD và lệnh tái tạo phải thống nhất.

### 3.4. Khối nội dung

#### 3.4.1. Chuyển giao thẩm quyền

Mọi quyết định về sự cần thiết, trạng thái, màu, cú pháp và chuyển đổi khối phải tuân thủ:

`quy_trinh_xay_dung/huong_dan_su_dung_khoi_noi_dung.md`

Quy chuẩn này chỉ khóa các điều kiện kĩ thuật dành cho bài hàm số.

#### 3.4.2. Điều kiện kĩ thuật

- Một bài không bắt buộc phải có khối.
- Phải quyết định theo thứ tự: **có cần khối không → mở cố định hay thu gọn → đỏ, vàng hay xám → tiêu đề và cú pháp**.
- Nội dung bắt buộc đối với mạch chính không được đặt trong khối thu gọn.
- Khối hiện hành dùng lớp chung `zo-block`, đúng một lớp màu và `zo-block-title`.
- Khối thu gọn dùng `<details>`, `<summary class="zo-block-title">` và `.zo-block-body` theo tài liệu chuyên trách.
- Mỗi khối phải đứng tại nơi gần nhất với câu hỏi, mệnh đề hoặc hiện tượng mà nó soi sáng; không gom các khối đọc thêm vào một cụm chỉ vì chúng cùng màu hoặc cùng trạng thái thu gọn.
- Chỉ đặt nhiều khối liên tiếp khi cụm ấy có một chủ đề và quan hệ nội tại rõ ràng.
- Không dùng khối để thay tiêu đề Markdown hoặc để trang trí.
- Trên PDF, toàn bộ nội dung của khối mở và khối thu gọn phải xuất hiện; nền, viền và tiêu đề phải được bảo toàn ở mức tương đương với HTML.

#### 3.4.3. Lớp cũ

Không dùng cho nội dung mới:

```text
collapsible-box-*
highlight-box-soft-red
highlight-box-honey-gold
```

Khi kiểm định bài cũ, phải phân loại từng trường hợp: giữ tương thích tạm thời, chuyển đổi trong phạm vi hiện tại, giao nhiệm vụ riêng hoặc loại bỏ ngay. Không thay mọi lớp cũ bằng cùng một lớp màu.

### 3.5. Bảng, hình và tài nguyên

#### 3.5.1. Chức năng và đặc tả

Chức năng nhận thức, mệnh đề trọng tâm, miền, giới hạn biểu diễn và phần đọc ngược được xác định theo `quy_chuan_khao_sat_ham_so.md`.

Tài nguyên không được chèn chỉ vì bài khảo sát hàm số “thường có” thành phần ấy. Riêng **đồ thị của chính hàm** là đầu ra production tối thiểu của `function_article` trước Human Review theo cấu hình dự án; đây là hợp đồng đầu ra, không phải một biểu diễn phụ được thêm vì thói quen. Các bảng, hình soi chiếu và biểu diễn bổ sung khác vẫn phải được quyết định theo chức năng nhận thức.

#### 3.5.2. Đường dẫn và vị trí

Trong thân bài, dùng đường dẫn tương đối tính từ QMD. Không dùng:

- đường dẫn tuyệt đối Windows hoặc Unix;
- URL localhost hoặc preview;
- đường dẫn tới `docs/`;
- đường dẫn tới `_audit/`, cache hoặc tệp tạm;
- đường dẫn tới tài nguyên của bài khác ngoài chủ ý.

Đường dẫn `/content/...` chỉ dùng ở trường metadata website đã được quy định, chẳng hạn `image` trong YAML; không dùng thay đường dẫn tương đối của hình trong thân bài.

Cấu trúc mặc định cho hình riêng của một bài là:

```text
_figures/<slug>/
├── src/
├── pdf/
└── svg/
```

Chỉ tạo các thư mục thực sự cần. Với đồ thị bắt buộc của `function_article`, trước Human Review phải có đủ chuỗi `src/*.tex → pdf/*.pdf → svg/*.svg` tương ứng. Candidate không được tự khai ngoại lệ để thay chuỗi này bằng SVG-only hoặc để bỏ hẳn đồ thị; ngoại lệ, nếu thực sự cần, phải được quyết định ở cấp yêu cầu người dùng hoặc cấu hình dự án trước khi chạy cổng review.

#### 3.5.3. Tên và định dạng

Tên tệp mới phải:

- dùng chữ thường không dấu;
- dùng dấu gạch dưới;
- gọi đúng đối tượng và chức năng;
- không mang hậu tố tạm như `final`, `new`, `test`, `copy`;
- dùng cùng tên cơ sở cho các định dạng của cùng một tài nguyên.

Với hình vector:

- HTML ưu tiên SVG;
- PDF ưu tiên PDF;
- nguồn chỉnh sửa được giữ khi nhiệm vụ yêu cầu khả năng tái tạo.

Không dùng ảnh raster thay hình vector khi đối tượng gồm đường, chữ và công thức có thể dựng bằng vector.

#### 3.5.4. Hình TikZ/PGFPlots

Khi tạo hoặc sửa đồ thị TikZ/PGFPlots, phải hoàn thành đặc tả chức năng rồi chuyển giao sang:

`quy_trinh_xay_dung/quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md`

Không tạo một hệ trục, màu, lấy mẫu hoặc cấu trúc `.tex` cạnh tranh trong QMD.

Trước Human Review, cổng `review-ready` kiểm tra một **lõi tự chứa không được phép trôi** của nguồn đồ thị: `fontspec`/`unicode-math` và STIX Two từ repository; các màu vai trò cốt lõi `zoPlotBackground=FFF9E9`, `zoPlotBorder=DFD7CA`, `zoAxis=554F48`, `zoText=3E3A35`, `zoGraphMain=EF5350`; trường nền–khung chuẩn; trục giữa có phân cấp nét chuẩn; và đường cong chính dùng đúng vai trò `zoGraphMain`. Các quyết định cục bộ như miền quan sát, vị trí nhãn và số vạch chia vẫn thuộc từng hình.

#### 3.5.5. Văn bản thay thế, nhãn và chú thích

Mọi hình mang thông tin phải có `fig-alt` hoặc cơ chế tương đương.

`fig-alt` phải mô tả đối tượng và quan hệ thị giác chính; không dùng các mô tả chung như “Hình đồ thị” hoặc “Ảnh minh họa”. Văn bản thay thế phải khớp artifact đã render: không mô tả một marker, điểm, đường chiếu, nhãn hoặc đối tượng như thể nó được thể hiện trên hình nếu artifact thực tế không biểu diễn nó.

Khi hình hoặc bảng cần được gọi lại, dùng nhãn duy nhất và dẫn chiếu Quarto. Không ghi cứng số thứ tự nếu Quarto có thể sinh tự động.

Chú thích không thay thế phần giải thích toán học hoặc phần đọc ngược.

#### 3.5.6. Kích thước và bố cục

Bố cục mặc định của hình trên cả HTML và PDF là nằm trong bề ngang nội dung. Với hình thường, không dùng `.column-screen-inset-shaded`.

Chỉ phân loại một hình là `mo_rong_html` khi bề ngang nội dung thông thường không đủ để đọc chi tiết toán học thiết yếu. Quyết định này phải được ghi trong hồ sơ sản xuất bằng nhãn `fig-*` của hình và một lí do cụ thể.

`.column-screen-inset-shaded` chỉ được dùng cho hình `mo_rong_html` và chỉ được đặt trong nhánh `.content-visible` có `when-format="html"`. Không dùng lớp này trong nhánh PDF hoặc trong phần dùng chung cho nhiều đầu ra.

Nhánh PDF luôn giữ hình trong bề ngang nội dung. Kích thước PDF được điều chỉnh bằng thuộc tính của ảnh, thường không vượt quá `width="100%"`.

Không suy ra nhu cầu mở rộng chỉ từ kích thước tệp nguồn, từ cách chèn hình trong bài tham chiếu hoặc từ việc hình là đồ thị. Mỗi hình phải được phân loại lại theo nhu cầu đọc của chính bài.

Không dùng chiều rộng pixel cố định làm mặc định. Không nén hình đến mức mất chi tiết toán học. Khi một hình không thể đồng thời cho thấy các hành vi thiết yếu, dùng nhiều cửa sổ có chức năng phân biệt.

Cả hình thường và hình mở rộng phải được kiểm tra trên HTML desktop, HTML mobile và PDF thật.

#### 3.5.7. Bảng

Bảng chỉ dùng khi nén hoặc đối chiếu thông tin tốt hơn văn xuôi. Bảng phải có tiêu đề cột rõ, đơn vị khi cần, kí hiệu đã giới thiệu và mức làm tròn được công bố.

Không dùng bảng hữu hạn để chứng minh kết luận vô hạn hoặc toàn cục. Không dùng nhiều thư viện chỉ để tạo một bảng mà Markdown/Quarto có thể biểu diễn trực tiếp, trừ khi mã cần cho việc tái tạo dữ liệu.

### 3.6. Hệ thống bài tập

#### 3.6.1. Điều kiện kích hoạt

Đối với bài production chuẩn về một hàm số cụ thể trong dự án này, `quy_chuan_khao_sat_ham_so.md` xem hệ thống bài tập là thành phần tiếp tục của bài học. Yêu cầu trực tiếp của người dùng có thể loại bỏ bài tập hoặc một loại nhiệm vụ có thể không cần hệ bài tập; ngoại lệ phải được ghi rõ trong hồ sơ.

Quy chuẩn kĩ thuật này điều khiển cách hiện thực hệ bài tập khi áp dụng; nó không tạo một cơ chế tự khai để agent tùy ý tắt thành phần mặc định.

#### 3.6.2. Cấu trúc tiêu đề

Cấu trúc hiện hành:

```markdown
## Bài tập

### Tên nhóm toán học tự nhiên

#### Bài 1. Tên bài tập cụ thể

Nội dung bài tập
```

- H2 dành cho toàn hệ bài tập;
- H3 dành cho một nhóm toán học tự nhiên có nhiều bài cần được đọc cùng nhau;
- H4 dành cho từng bài tập trong contract kĩ thuật hiện hành;
- không dùng H1;
- không công khai các nhãn thiết kế nội bộ như “Mục tiêu A/B”.

Tên nhóm phải gọi đúng nội dung toán học. Tên bài và số thứ tự phải giúp định vị bài tập mà không biến metadata thiết kế nội bộ thành cấu trúc công khai. Việc thay đổi container H4 chỉ được thực hiện đồng bộ với checker và các bài production đang tuân contract hiện hành.

#### 3.6.3. Đề bài và thành phần thu gọn

Đề bài, giả thiết, dữ kiện và yêu cầu phải hiển thị trong mạch chính. Không đặt toàn bộ đề bài trong khối thu gọn.

Gợi ý, đáp án và lời giải có thể dùng khối xám thu gọn khi chúng không phải mắt xích bắt buộc của chuỗi bài tập.

Nếu nhiệm vụ không yêu cầu gợi ý, đáp án hoặc lời giải, không để tiêu đề hoặc khối giữ chỗ.

#### 3.6.4. Kí hiệu và tài nguyên

Kí hiệu phải nhất quán với thân bài. Tài nguyên trong bài tập phải tuân thủ Mục 3.5. Cú pháp LaTeX phải tuân thủ `AGENTS.md` và quy ước hiện hành của dự án. Trong nội dung mới của dự án, dùng `\quad` cho khoảng cách công thức theo quy ước hiện hành, `\lvert...\rvert` cho trị tuyệt đối và `f^\prime`, `f^{\prime\prime}` cho đạo hàm; không dùng `\qquad`, dạng `|...|` để biểu diễn trị tuyệt đối hoặc `f'`, `f''` như biến thể trình bày.

Các yêu cầu về mục tiêu, quan hệ phụ thuộc, độ khó, tính tự chứa, trùng lặp và giá trị nhận thức thuộc `quy_chuan_khao_sat_ham_so.md`, không lặp lại trong tài liệu này.

### 3.7. PDF tải xuống

#### 3.7.1. Phạm vi bắt buộc

Mọi bài khảo sát một hàm số ở trạng thái `published` phải có PDF tải xuống của chính bài và nút tải hoạt động trên HTML.

Ngoài cổng xuất bản, còn có yêu cầu toàn vẹn của output dùng cho Human Review: nếu bản HTML được đưa cho người kiểm định có hiển thị nút tải PDF, tệp PDF mà nút ấy trỏ tới phải tồn tại và mở được. Nếu PDF chưa được build, không được coi HTML có nút tải chưa hoạt động là output review hoàn chỉnh.

Output review cũng không được tự tuyên bố trạng thái xuất bản chưa đạt. PDF tạo ở trạng thái `draft`, `in_production`, `validated` hoặc khi publication còn `pending` không được chứa câu khẳng định rằng đó là “ấn bản chính thức đã phát hành”. Nếu hạ tầng PDF dùng một câu chung cho mọi trạng thái, câu ấy phải trung tính về xuất bản; nhãn “chính thức/đã phát hành” chỉ được sinh ở bước xuất bản có thẩm quyền.


YAML phải có:

```yaml
zo-pdf-download:
  href: "<ten_qmd>.pdf"
  label: "Tải PDF"

zo-pdf-branding:
  collection: "100+ Hàm số: Sự biến thiên và đồ thị"
  short-title: "..."
  canonical-url: "https://zo-math.github.io/zo-math/content/.../<ten_qmd>.html"
  display-url: "zo-math.github.io/zo-math"
```

Tên PDF mặc định cùng tên cơ sở với QMD và nằm cạnh QMD.

#### 3.7.2. Hệ thống hiện hành

PDF được điều khiển bởi:

```text
_quarto-pdf.yml
assets/lua/zo_pdf_branding.lua
assets/lua/zo_pdf_content.lua
assets/tex/zo-pdf.tex
assets/tex/zo-pdf-rights.tex
assets/tex/zo-pdf-support.tex
scripts/zo_pdf.py
scripts/zo_python.py
scripts/zo_quarto.py
```

Nút tải PDF trên HTML được điều khiển bởi:

```text
assets/lua/zo_pdf_download.lua
```

Không sao chép hệ đầu trang, chân trang, metadata hoặc nhận diện PDF vào từng QMD.

#### 3.7.3. Lệnh build và trạng thái

Từ gốc repository:

```bash
python scripts/zo_python.py scripts/zo_pdf.py build \
DUONG_DAN_DEN_TEP_QMD
```

Kiểm tra sơ bộ:

```bash
python scripts/zo_python.py scripts/zo_pdf.py status \
DUONG_DAN_DEN_TEP_QMD
```

`status` trả một trong ba trạng thái:

```text
MISSING
STALE
CURRENT
```

`CURRENT` chỉ so sánh thời gian sửa của QMD với PDF. Nó không chứng minh PDF hiện hành sau khi cấu hình, Lua filter, tệp TeX, font, logo hoặc tài nguyên dùng chung thay đổi.

#### 3.7.4. Quan hệ QMD — PDF — HTML

Phải bảo đảm:

1. QMD khai báo đúng tên PDF;
2. PDF được build từ chính QMD;
3. PDF được chép về cạnh QMD;
4. lần render HTML cuối có thể đưa PDF vào tài nguyên xuất bản;
5. nút trên HTML tải đúng tệp, không trả `404` và không tải PDF của bài khác.

Sau khi build hoặc thay PDF, phải render lại HTML trước nghiệm thu cuối.

#### 3.7.5. Metadata và nhận diện

Hệ hiện hành đọc các dữ liệu chính từ:

- `title` cho tiêu đề hiển thị trên bìa PDF;
- `title-meta` cho trường `Title` trong metadata PDF;
- `subtitle`;
- `date`;
- `summary` hoặc `description`;
- `keywords`;
- `zo-pdf-branding.short-title` cho tiêu đề chạy ở đầu trang PDF;
- `zo-pdf-branding.collection`;
- `zo-pdf-branding.canonical-url`;
- `zo-pdf-branding.display-url`.

Tác giả, nhà phát hành và dữ liệu bản quyền được hệ TeX hiện hành đặt theo ZO Math.

Phải kiểm tra metadata của PDF thật, không chỉ đọc YAML. `canonical-url` phải là URL HTML chính thức của chính bài; mã QR và liên kết trong PDF phải dùng đúng URL ấy.

#### 3.7.6. Kiểm tra PDF thật

Phải kiểm tra ít nhất:

- PDF mở được, không rỗng và có số trang hợp lệ;
- trang đầu;
- trang nội dung đầu tiên;
- một trang giữa khi có;
- trang cuối;
- tiêu đề, phụ đề, bộ sưu tập và ngày;
- đầu trang, chân trang, số trang;
- font tiếng Việt và công thức;
- bảng, hình và khối nội dung;
- mục lục và liên kết;
- URL và mã QR;
- trang quyền và trang hỗ trợ theo hệ hiện hành;
- không có chữ, hình, bảng hoặc công thức vượt lề;
- không có trang trắng hoặc ngắt trang ngoài ý muốn.

Khối thu gọn trên HTML không được làm nội dung biến mất khỏi PDF.

### 3.8. Cấu trúc cũ và giá trị bị cấm

#### 3.8.1. Danh mục tối thiểu

Trong bài QMD mới hoặc phần nội dung mới, không được có:

| Nhóm            | Mẫu cần phát hiện                                                  | Mức mặc định                             |
| --------------- | ------------------------------------------------------------------ | ---------------------------------------- |
| Tiêu đề         | H1 thật trong thân bài                                             | Lỗi chặn                                 |
| Tiêu đề giả     | `.tieu-de-chu-thich`                                               | Lỗi chặn                                 |
| Khối cũ         | `collapsible-box-*`, `highlight-box-*`                             | Lỗi chặn đối với nội dung mới            |
| Giá trị giữ chỗ | Các giá trị tại Mục 3.1.5                                          | Lỗi chặn                                 |
| LaTeX           | `\(`, `\)`, `\[`, `\]`, `\boxed`; trong nội dung mới còn phải tuân `\quad`, `\lvert...\rvert`, `f^\prime`, `f^{\prime\prime}` theo quy ước dự án | Lỗi chặn đối với mẫu xác định chắc chắn |
| Mã              | lệnh cài thư viện, `setwd()`, mã tạm, thư viện không dùng          | Lỗi chặn hoặc cảnh báo theo độ chắc chắn |
| Đường dẫn       | tuyệt đối, localhost, `docs/`, `_audit/`, cache                    | Lỗi chặn                                 |
| Tài nguyên      | tên tạm, tệp thiếu, thiếu `fig-alt`, sai bài                       | Lỗi chặn hoặc cảnh báo theo trường hợp   |
| PDF             | thiếu khai báo, sai tên, sai URL, sai bài                          | Lỗi chặn                                 |
| Bài mẫu         | metadata, công thức, hình, bài tập hoặc kí hiệu còn thuộc bài khác | Lỗi chặn khi xác định chắc chắn          |

Công cụ phải có khả năng nhận biết code fence và tài liệu hướng dẫn để tránh báo nhầm các mẫu đang được trích dẫn nhằm mô tả quy tắc.

#### 3.8.2. Dấu vết bài mẫu

Không chỉ tìm tên hàm. Phải đối chiếu:

- tiêu đề, phụ đề và mô tả;
- ảnh thẻ và số thẻ;
- PDF và canonical URL;
- tên thư mục hình;
- nhãn hình/bảng;
- kí hiệu đặc thù;
- nội dung bài tập và lời giải;
- hiện tượng được mô tả trong văn xuôi.

Phát hiện chắc chắn là lỗi chặn; phát hiện chưa đủ chắc chắn là cảnh báo cần người đọc lại.

#### 3.8.3. Bài cũ và phạm vi chuyển đổi

Khi kiểm định bài cũ, phân loại cấu trúc lịch sử thành:

1. còn hợp lệ;
2. tương thích tạm thời;
3. phải chuyển đổi trong nhiệm vụ hiện tại;
4. giao nhiệm vụ riêng;
5. phải loại bỏ ngay vì làm sai nội dung hoặc đầu ra.

Không mở rộng nhiệm vụ thành chuyển đổi toàn repository nếu chưa được giao. Báo cáo phải ghi cấu trúc, vị trí, phân loại, lí do và quyết định.

## 4. Mô hình kiểm định

### 4.1. Hai tầng bắt buộc

Nghiệm thu kĩ thuật phải có đồng thời:

1. **kiểm định tự động** — cho những quan hệ có thể xác định từ mã nguồn, tệp và đầu ra;
2. **kiểm định có người quan sát** — cho ý nghĩa, bố cục, khả năng đọc, tương tác và tính đúng của đầu ra thật.

Hai tầng không thay thế nhau.

### 4.2. Giới hạn của công cụ hiện hành

`scripts/zo_check_repo.py` hiện kiểm tra những thành phần cơ bản như mã hóa, khoảng trắng, YAML, tham chiếu tài nguyên, một số cấu trúc repository và khả năng render HTML.

Kết quả `PASS` của công cụ này **không mặc nhiên xác nhận**:

- đủ YAML theo hợp đồng bài hàm số;
- metadata đúng bài;
- hệ tiêu đề đúng ngữ nghĩa;
- hệ khối đúng chức năng;
- `fig-alt` đạt;
- hệ bài tập đạt;
- PDF đúng bài;
- nút PDF hoạt động;
- bố cục desktop, mobile và PDF đạt.

`scripts/zo_qmd.py review-ready` là cổng chuyên biệt trước Human Review của dự án này. Nó không thay checker lõi và không nghiệm thu nội dung; nó chặn những sai lệch production đã có thể mã hóa nhưng nằm ngoài phạm vi `check`/`render`, gồm lifecycle `start`, phạm vi thay đổi, authority snapshot, navigation, đồ thị bắt buộc, chuỗi nguồn–render, tính nhất quán hồ sơ–artifact–bằng chứng và một số guard ngữ nghĩa có thể kiểm tra cấu trúc. Với `function_article`, thiếu `_audit/<slug>_session.json`, start muộn sau khi candidate scope đã bẩn, thay đổi ngoài scope hoặc authority drift đều chặn Human Review.

Báo cáo phải ghi rõ phần nào do `check`/`render`, phần nào do `review-ready` xác nhận và phần nào vẫn cần người quan sát.

### 4.3. Danh mục kiểm định tự động tối thiểu

#### YAML và thẻ

- YAML đọc được;
- đủ trường bắt buộc;
- không còn giá trị giữ chỗ;
- `body-classes` chứa hai lớp bắt buộc;
- `image` tồn tại và khớp thẻ sau chuẩn hóa đường dẫn;
- `listing-order` khớp số thẻ;
- `canonical-url` khớp đường dẫn bài;
- khai báo PDF đầy đủ.

#### Cấu trúc QMD

- không có H1 thật trong thân bài;
- không nhảy cấp tiêu đề;
- không có tiêu đề rỗng;
- không có `.tieu-de-chu-thich`;
- không có lớp khối cũ trong nội dung mới;
- cấu trúc khối hiện hành đóng mở hợp lệ;
- không có cú pháp LaTeX bị cấm ngoài code fence hoặc ví dụ hướng dẫn.

#### Mã và phụ thuộc

- nhận diện các code chunk;
- phát hiện lệnh cài thư viện, `setwd()` và đường dẫn tuyệt đối;
- cảnh báo thư viện hoặc chunk có khả năng không dùng;
- phát hiện lỗi, cảnh báo và thông báo ngoài ý muốn khi render;
- đầu ra được khai báo tồn tại.

#### Tài nguyên

- đường dẫn tồn tại;
- không trỏ tới `docs/`, `_audit`, cache hoặc tệp tạm;
- hình mang thông tin có `fig-alt`;
- nhãn không trùng và dẫn chiếu có đích;
- `.column-screen-inset-shaded` chỉ xuất hiện trong nhánh HTML;
- mọi hình mở rộng HTML có nhãn `fig-*` và được khai báo cùng lí do trong hồ sơ phiên bản hiện hành;
- nhánh PDF và phần dùng chung không chứa `.column-screen-inset-shaded`;
- tài nguyên HTML/PDF cần thiết tồn tại;
- tên tệp không mang dấu vết tạm;
- tài nguyên không còn thuộc bài mẫu.

#### Bài tập

- có `## Bài tập` đối với bài production chuẩn, trừ ngoại lệ đã được thẩm quyền cho phép;
- có H3 cho nhóm toán học tự nhiên và H4 cho từng bài theo contract kĩ thuật hiện hành;
- không có nhãn công khai “Mục tiêu A/B”;
- bài có nội dung;
- đề bài không bị giấu hoàn toàn trong khối thu gọn;
- khối gợi ý, đáp án hoặc lời giải dùng cấu trúc hiện hành;
- tài nguyên và dẫn chiếu hợp lệ.

#### Điều hướng và mục lục

- khi dự án dùng sidebar tường minh, trang phải được đăng kí vào đúng nhóm trước lần render dùng để nghiệm thu;
- HTML phải chứa phần tử sidebar thật, không chỉ chứa mã JavaScript hoặc CSS có nhắc đến sidebar;
- khi `toc: true`, HTML phải chứa mục lục thật và các mục phải khớp hệ tiêu đề;
- ở desktop và mobile, việc đóng–mở sidebar hoặc mục lục không được làm lệch lề trái giữa khối tựa đề và thân bài.

#### PDF

- PDF được khai báo;
- build trả mã thoát `0`;
- tệp đích tồn tại, không rỗng và mở được;
- số trang hợp lệ;
- metadata có thể trích xuất;
- URL không chứa localhost hoặc giá trị giữ chỗ;
- HTML sau render có nút tải khi workflow yêu cầu hiển thị chức năng ấy;
- nếu HTML dùng cho Human Review có nút tải PDF, liên kết tải trỏ tới tệp tồn tại và mở được;
- liên kết tải trong đầu ra xuất bản trỏ tới đúng tệp tồn tại.

#### Cổng bắt buộc trước Human Review

Sau lần `check` và `render` cuối, tạo bằng chứng visual runtime rồi mới chạy `review-ready`:

```text
python scripts/zo_python.py scripts/zo_qmd.py visual-check <duong_dan_qmd>
python scripts/zo_python.py scripts/zo_qmd.py review-ready --report _audit/<slug>_review_ready.json <duong_dan_qmd>
```

Cổng chỉ đạt khi đồng thời:

- QMD đã được đăng kí trong sidebar tường minh và HTML render chứa sidebar thật;
- PDF tải xuống tồn tại, là PDF hợp lệ ở mức chữ kí tệp và không cũ hơn QMD;
- hồ sơ không tự bỏ đồ thị hoặc tự miễn chuỗi hình bắt buộc;
- tồn tại session manifest version hiện hành do `start` tạo trước khi candidate thay đổi; HEAD, project/article type và candidate target vẫn khớp session;
- session dùng đúng phạm vi canonical do Cỗ máy suy ra; effective authority closure có đủ role/reason và các authority/provenance bắt buộc giữ nguyên SHA-256; mọi thay đổi phát sinh kể từ `start` nằm trong scope đã khóa; `_audit/` chỉ là vùng bằng chứng, không mở rộng phạm vi production;
- QMD tham chiếu SVG đồ thị dưới đúng `_figures/<slug>/svg/` và tồn tại `.tex` trong `src/` cùng PDF tương ứng trong `pdf/`;
- nguồn TikZ/PGFPlots không vi phạm các invariant máy kiểm được đã khóa của quy chuẩn đồ thị; khi quy chuẩn đồ thị được kích hoạt, nguồn còn phải mang đủ lõi tự chứa bắt buộc về LuaLaTeX/STIX, màu ngữ nghĩa, trường nền–khung, trục và phân cấp nét;
- hồ sơ dùng đúng schema version hiện hành và chỉ chứa trạng thái agent-owned; không có nhóm Human Review/nghiệm thu do agent tự điền;
- `_audit/<slug>_check.json` và `_audit/<slug>_render.json` là bằng chứng machine-owned thật, đạt `PASS` hoặc `PASS_WITH_WARNINGS` và bao phủ đúng candidate;
- `_audit/<slug>_visual/html_mobile_measurements.json` là bằng chứng machine-owned do `visual-check` tạo, khóa đúng viewport 390 px và 430 px, khớp SHA-256 của rendered HTML/screenshot và xác nhận `document.scrollWidth <= document.clientWidth` ở cả hai viewport;
- `tu_xem` có bằng chứng thật dưới `_audit/<slug>_visual/`, tối thiểu cho HTML desktop, hai screenshot mobile machine-owned `html_mobile_390.png`, `html_mobile_430.png` và PDF; self-view có thể ghi `canh_bao` nhưng không được giả làm Human Review;
- các phát biểu trung tâm dùng quan hệ như *bảo toàn*, *giữ nguyên*, *phụ thuộc vào*, *làm mất*, *xác định được từ*, *khôi phục được từ* có bản ghi phép thử `dat` trong hồ sơ;
- QMD và hồ sơ không dùng các cụm quan hệ mơ hồ đã cấu hình cấm như *giữ độ lớn*, *giữ nguyên độ lớn*, *bảo toàn độ lớn*, *không xóa độ lớn*; thay bằng phát biểu định lượng chính xác như một đẳng thức bảo toàn cụ thể, *phụ thuộc vào*, hoặc *xác định/khôi phục được từ*;
- không có token nguồn bị cấu hình cấm, hiện gồm `\longmapsto`;
- nội dung mới không dùng cú pháp đạo hàm apostrophe như `f'(x)` hoặc `f''(x)`; dùng `f^\prime(x)` và `f^{\prime\prime}(x)`.

`review-ready: PASS` chỉ có nghĩa candidate đủ điều kiện **được đưa cho người quan sát**; `final_acceptance` vẫn `NOT_RUN` và publication vẫn `pending`. Hồ sơ sản xuất không phải nơi lưu Human Review hay nghiệm thu; các record đó thuộc lớp kiểm định bên ngoài candidate profile.

### 4.4. Kiểm định có người quan sát tối thiểu

Phải quan sát, khi áp dụng:

- QMD nguồn;
- HTML ở chiều rộng desktop;
- HTML ở chiều rộng mobile;
- mục lục;
- khối mở cố định;
- khối thu gọn ở trạng thái đóng và mở;
- bảng và hình;
- phần bài tập;
- nút tải PDF;
- PDF trang đầu, trang nội dung, trang giữa và trang cuối;
- metadata PDF;
- liên kết và mã QR.

Trên HTML phải xác nhận tối thiểu:

- tiêu đề không lặp;
- metadata bị ẩn đúng;
- không tràn ngang ngoài ý muốn;
- công thức, hình và bảng đọc được;
- khối đúng kiểu, tương tác được và được phân bố tại nơi phục vụ mạch đọc;
- sidebar và mục lục xuất hiện đúng; tựa đề và thân bài giữ cùng lề trái khi thay đổi chiều rộng;
- phần bài tập có cấu trúc rõ;
- nút PDF tải đúng tệp;
- liên kết và tài nguyên không trả `404`.

Trên PDF phải xác nhận tối thiểu:

- đúng bài và đủ nội dung;
- metadata và nhận diện đúng;
- font, công thức, hình và bảng đúng;
- mọi khối còn đủ nền, viền, tiêu đề và nội dung; nội dung từ khối thu gọn trên HTML không bị mất trên PDF;
- mục lục, liên kết, đầu trang, chân trang và số trang đúng;
- URL và mã QR đúng;
- không có lỗi cắt, chồng, tràn hoặc ngắt trang ngoài ý muốn.

### 4.5. Thứ tự kiểm định

Thứ tự mặc định:

1. chạy `start` trước mọi sửa đổi candidate để Cỗ máy khóa session, authority snapshot và phạm vi canonical;
2. kiểm tra QMD, YAML và tài nguyên;
3. chạy kiểm định tĩnh;
4. sửa lỗi chặn;
5. render HTML sơ bộ;
6. build PDF khi bắt buộc;
7. render lại HTML sau khi PDF đã tồn tại;
8. kiểm tra đầu ra bằng công cụ;
9. cập nhật hồ sơ bằng bằng chứng cuối và chạy `review-ready`; nếu cổng này `FAIL`, sửa tại nguồn rồi chạy lại các bước bị ảnh hưởng;
10. xét cảnh báo còn lại;
11. quan sát HTML desktop và mobile;
12. quan sát PDF;
13. kiểm tra liên kết và nút tải;
14. sửa lỗi;
15. chạy lại các kiểm tra bị ảnh hưởng;
16. lập báo cáo nghiệm thu.

Không dùng kết quả kiểm tra cũ sau khi nguồn hoặc phụ thuộc liên quan đã thay đổi.

### 4.6. Bằng chứng kiểm định

Báo cáo phải lưu đủ bằng chứng để truy lại phạm vi kiểm tra, gồm tối thiểu:

- tệp nguồn và đầu ra;
- lệnh đã chạy;
- mã thoát;
- báo cáo công cụ;
- metadata và số trang PDF;
- kết quả liên kết/HTTP khi áp dụng;
- kích thước cửa sổ quan sát;
- cảnh báo và quyết định;
- tiêu chí không áp dụng và lí do;
- trạng thái Git trong phạm vi.

Không đưa cache hoặc tệp tạm vào repository chỉ để làm bằng chứng.

## 5. Điều kiện nghiệm thu

### 5.1. Điều kiện tiên quyết

Trước nghiệm thu cuối phải có:

- phạm vi nhiệm vụ đã chốt;
- tài liệu điều khiển đã được đọc;
- hồ sơ sản xuất đã được điền trong phạm vi áp dụng;
- QMD đã hoàn thiện;
- tài nguyên bắt buộc đã tồn tại;
- tiêu chí không áp dụng đã có lí do;
- không còn quyết định quan trọng chưa xác định;
- không còn giá trị giữ chỗ trong sản phẩm.

### 5.2. Điều kiện dừng

Không được kết luận `ĐẠT` khi còn một trong các trường hợp:

- lỗi toán học hoặc lỗi chặn kĩ thuật;
- metadata sai bài;
- dấu vết chắc chắn của bài mẫu;
- H1 trong thân bài;
- cấu trúc LaTeX bị cấm;
- đường dẫn hỏng;
- tài nguyên bắt buộc thiếu;
- nội dung bắt buộc bị thu gọn hoặc mất;
- PDF bắt buộc thiếu, sai bài hoặc không mở được;
- canonical URL sai;
- nút PDF tải sai tệp;
- HTML desktop hoặc mobile chưa được quan sát;
- PDF bắt buộc chưa được quan sát;
- kiểm định tự động chưa chạy lại sau lần sửa cuối;
- cổng `review-ready` chưa `PASS` đối với bài production đi vào Human Review.

### 5.3. Tiêu chí không áp dụng

Một tiêu chí chỉ được đánh dấu `NOT_APPLICABLE` khi:

- bản chất bài hoặc phạm vi nhiệm vụ không kích hoạt tiêu chí;
- tài liệu có thẩm quyền cho phép;
- lí do đã được ghi;
- việc không áp dụng không làm mất đầu ra bắt buộc.

Không dùng _không áp dụng_ để tránh PDF của bài `published`, sửa metadata sai bài, xử lí đường dẫn hỏng, loại bỏ giá trị giữ chỗ hoặc kiểm tra đầu ra thật.

### 5.4. Điều kiện đưa bài sang `published`

Một bài chỉ được đặt hoặc giữ trạng thái `published` khi:

- nội dung đã qua nghiệm thu theo quy chuẩn khảo sát;
- YAML, thẻ và tài nguyên thẻ đúng;
- HTML đã render thành công và được quan sát trên desktop/mobile;
- các thành phần có điều kiện đã đạt khi được kích hoạt;
- PDF đã được build và quan sát;
- nút tải PDF hoạt động;
- không còn lỗi chặn;
- báo cáo cuối kết luận `ĐẠT`.

Không giữ trạng thái `published` chỉ vì thẻ đã xuất hiện trên trang dự án.

### 5.5. Báo cáo nghiệm thu

Báo cáo cuối phải ghi:

1. phạm vi;
2. tệp nguồn;
3. tài liệu điều khiển;
4. đầu ra HTML và PDF;
5. tài nguyên liên quan;
6. lệnh và kết quả kiểm định tự động;
7. kết quả kiểm định có người quan sát;
8. lỗi đã sửa;
9. cảnh báo và quyết định;
10. tiêu chí không áp dụng và lí do;
11. kiểm tra desktop, mobile, PDF và nút tải;
12. trạng thái Git trong phạm vi;
13. kết luận `ĐẠT`, `KHÔNG ĐẠT` hoặc `CHƯA ĐỦ BẰNG CHỨNG`.

### 5.6. Những dấu hiệu chưa đủ để nghiệm thu

Những kết quả sau, riêng lẻ hoặc kết hợp, vẫn chưa đủ:

- `git diff --check` không báo lỗi;
- YAML đọc được;
- `rg` tìm đủ tiêu đề;
- `scripts/zo_check_repo.py` báo `PASS`;
- Quarto render mã thoát `0`;
- HTML trả `200`;
- không có liên kết `404` trong phạm vi kiểm tra hẹp;
- PDF tồn tại hoặc báo `CURRENT`;
- `pdfinfo` đọc được;
- trang đầu trông đúng;
- desktop trông đúng;
- không tìm thấy chuỗi bị cấm.

Nghiệm thu đòi hỏi toàn bộ chuỗi bằng chứng theo đúng phạm vi.

### 5.7. Điều kiện nghiệm thu cuối

Một bài chỉ được kết luận `ĐẠT` khi:

- mọi tiêu chí bắt buộc đã đạt;
- mọi lỗi chặn đã được sửa;
- mọi cảnh báo đã được xét;
- mọi tiêu chí không áp dụng có lí do được chấp thuận;
- không còn cấu trúc bị cấm trong nội dung mới;
- cấu trúc lịch sử đã được phân loại;
- không còn dấu vết bài mẫu;
- HTML và PDF bắt buộc tồn tại;
- đầu ra thật đã được quan sát;
- desktop và mobile đã được kiểm tra;
- sidebar và mục lục đã được xác nhận bằng đầu ra thật khi trang thuộc hệ điều hướng của dự án;
- nút tải PDF đã được kích hoạt thử;
- PDF đúng bài và đúng phiên bản;
- kiểm định tự động đã chạy lại sau lần sửa cuối;
- báo cáo phân biệt rõ bằng chứng tự động với bằng chứng quan sát;
- phạm vi nghiệm thu được ghi rõ.

Nếu thiếu một bằng chứng bắt buộc nhưng chưa xác định là lỗi, kết luận là `CHƯA ĐỦ BẰNG CHỨNG`, không phải `ĐẠT`.
