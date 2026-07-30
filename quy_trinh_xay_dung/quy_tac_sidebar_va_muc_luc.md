# Quy tắc dùng Sidebar và Mục lục trong ZO Math

Tệp này ghi lại quy ước phân biệt giữa **Sidebar điều hướng** và **Mục lục bài viết** trong website ZO Math.

Quy tắc này được chốt sau khi thiết kế lại dự án:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/
├── index.qmd
├── dan_nhap.qmd
├── khung_khao_sat_ham_so.qmd
└── core/index.qmd
```

## 1. Phân biệt Sidebar và Mục lục

**Sidebar** là phần điều hướng trong một dự án hoặc một mạch nội dung. Sidebar cho người đọc biết họ đang ở đâu trong cấu trúc lớn hơn, và giúp đi sang các trang liên quan.

Sidebar được khai báo trong `_quarto.yml`, tại phần:

```yaml
website:
  sidebar:
```

**Mục lục** là phần đề mục của riêng trang đang đọc. Mục lục được sinh từ các heading trong chính tệp `.qmd`.

Ví dụ:

```markdown
## 1. Hàm số

### Bài tập

## 2. Sự biến thiên của hàm số
```

Mục lục được điều khiển trong YAML của từng trang:

```yaml
toc: true
toc-location: right
toc-depth: 3
```

## 2. Quy tắc cho từng loại trang

### Trang cửa vào dự án

Trang cửa vào dự án có nhiệm vụ giới thiệu dự án và dẫn người đọc đi tiếp.

Ví dụ:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/index.qmd
```

Trang này cần:

```text
có sidebar điều hướng
không có mục lục bài viết
```

YAML nên dùng:

```yaml
page-layout: article
toc: false
body-classes: zo-page-gateway
```

Không dùng:

```yaml
sidebar: false
```

vì `sidebar: false` sẽ tắt luôn sidebar điều hướng của dự án.

### Trang bài viết dài

Trang bài viết dài có nhiều đề mục, nên cần mục lục bên phải.

Ví dụ:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/dan_nhap.qmd
```

Trang này cần:

```text
có sidebar điều hướng
có mục lục bài viết
```

YAML nên dùng:

```yaml
page-layout: article
toc: true
toc-location: right
toc-depth: 3
body-classes: zo-page-article
```

Nếu bài viết cần mục lục sâu hơn, tăng riêng trang đó:

```yaml
toc-depth: 4
```

Không nên đặt `toc-depth` quá sâu nếu mục lục trở nên rối.

### Trang danh sách

Trang danh sách dùng để liệt kê các bài con.

Ví dụ:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/index.qmd
```

Trang này thường cần:

```text
có sidebar điều hướng
không có mục lục bài viết
```

YAML nên dùng:

```yaml
page-layout: article
toc: false
body-classes: zo-page-listing
```

## 3. Khi thêm một trang vào dự án

Khi tạo một trang mới thuộc dự án có sidebar, cần làm hai việc.

Thứ nhất, đặt YAML đúng vai trò trang.

Ví dụ với bài viết dài:

```yaml
page-layout: article
toc: true
toc-location: right
toc-depth: 3
body-classes: zo-page-article
```

Thứ hai, thêm trang đó vào sidebar trong `_quarto.yml`.

Ví dụ:

```yaml
- text: "Dẫn nhập"
  href: content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/dan_nhap.qmd
```

Nếu không thêm vào `_quarto.yml`, trang có thể vẫn render được, nhưng không nằm đúng trong hệ điều hướng của dự án.

## 4. Quy tắc cho `assets/html/sidebar-layer.html`

Tệp:

```text
assets/html/sidebar-layer.html
```

là tệp nguồn giao diện dùng để xử lí sidebar và nút mục lục.

Tệp này phải được Git theo dõi, dù có đuôi `.html`.

Trong `.gitignore` cần có ngoại lệ:

```gitignore
*.html
!assets/html/sidebar-layer.html
```

Lí do: phần lớn file `.html` là kết quả render, không nên theo dõi; nhưng `assets/html/sidebar-layer.html` là tệp nguồn, cần được commit.

Logic đã chốt trong `sidebar-layer.html`:

```text
Nếu trang không có TOC thật thì không tạo nút TOC.
Nếu trang có TOC thật thì tạo nút TOC.
Các cấp mục lục đã được Quarto sinh ra theo toc-depth phải được hiện ra, không bị ẩn bởi class collapse.
```

Kết quả mong muốn:

```text
Trang cửa vào: có sidebar trái, không có icon mục lục bên phải.
Trang bài viết: có sidebar trái, có icon/mục lục bên phải.
```

## 5. Kiểm tra sau khi sửa

Sau khi sửa YAML, `_quarto.yml`, hoặc `sidebar-layer.html`, render nhánh liên quan:

```bash
quarto render content/thpt/zo_math_100
```

Mở trang để kiểm tra bằng mắt:

```bash
start docs/content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/index.html
start docs/content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/dan_nhap.html
```

Nếu trình duyệt đã mở sẵn, dùng `Ctrl + F5` để tải lại thật sự.

## 6. Lệnh kiểm tra HTML

Kiểm tra class của trang:

```bash
grep -n "<body" docs/content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/index.html
grep -n "<body" docs/content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/dan_nhap.html
```

Kết quả mong muốn cho trang cửa vào:

```text
nav-sidebar
zo-page-gateway
```

Kết quả mong muốn cho trang bài viết:

```text
nav-sidebar
zo-page-article
```

Kiểm tra mục lục của bài viết:

```bash
grep -n "id=\"TOC\"\|quarto-margin-sidebar" docs/content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/dan_nhap.html
```

Trang bài viết dài cần có:

```text
id="TOC"
quarto-margin-sidebar
```

Trang cửa vào không cần có `id="TOC"`.

## 7. Nguyên tắc làm việc

Không dùng `sidebar: false` để tắt mục lục.

Không sửa CSS hoặc JavaScript theo cảm giác khi chưa xác định rõ thành phần đang thấy là sidebar hay TOC.

Không dùng `git add .` khi chưa kiểm tra.

Quy trình an toàn:

```bash
git status --short
git diff --stat
git --no-pager diff --name-status
```

Sau đó chỉ stage đúng các tệp cần commit.
