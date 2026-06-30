# ZO Math: Xuất SVG từ TikZ với Font STIX

## Mục đích ban đầu
- Xuất SVG từ TikZ (vẽ hình toán học) dùng font STIX từ `E:\zo-math\assets\fonts\`.
- Đồng bộ font STIX giữa SVG và HTML (đã có CSS sẵn).

## Công cụ mới

### 1. `make4ht`
- **Công dụng**: Biên dịch TikZ → SVG.
- **Cách dùng**:
  ```bash
  make4ht -l -f html5+svg so-do-nhan-phan-phoi-hai-nhi-thuc.tex
  ```
  - `-l`: Dùng `lualatex` (vì `fontspec`).
  - `-f html5+svg`: Đầu ra SVG.
  - **Kết quả**: Tạo `so-do-nhan-phan-phoi-hai-nhi-thuc0.svg`.

### 2. `dvisvgm`
- **Công dụng**: Chuyển DVI → SVG (tự động trong `make4ht`).
- **Cách dùng thủ công**:
  ```bash
  lualatex --output-format=dvi so-do-nhan-phan-phoi-hai-nhi-thuc.tex
  dvisvgm --font-format=woff2 so-do-nhan-phan-phoi-hai-nhi-thuc.dvi
  ```

## Các bước thực hiện

### 1. Chuẩn bị tệp
- **Tệp TikZ (`so-do-nhan-phan-phoi-hai-nhi-thuc.tex`)**:
  - Dùng `$...$` thay `\(...\)` trong node.
  - Ví dụ: `\draw [->] (d1l)--(d2l) node[midway,right] {$1+x$};`.
- **Tệp preamble (`tikz-preamble.tex`)**:
  - Thêm `\usepackage{tikz}`.
  - Cấu hình font STIX với `.woff2` cho SVG.

### 2. Biên dịch SVG
- Từ `E:\zo-math\figures\toan-tai-hien\khai-trien-luy-thua-nhi-thuc-thanh-da-thuc`:
  ```bash
  make4ht -l -f html5+svg so-do-nhan-phan-phoi-hai-nhi-thuc.tex
  ```
- Kiểm tra: `so-do-nhan-phan-phoi-hai-nhi-thuc0.svg`.

## Vấn đề & Giải pháp

- **Lỗi `fontspec`**: Thêm `-l` vào `make4ht`.
- **Lỗi `\(...\)`**: Thay bằng `$...$`.
- **Cảnh báo `Cannot load extension: svg`**: Bỏ qua (không ảnh hưởng).
- **Font `cmmi10/cmmi5`**: Bỏ qua (dùng STIX).
- **Đường dẫn tương đối**:
  - Chạy từ thư mục chứa TikZ để `../../../assets/...` đúng.
  - Hoặc dùng đường dẫn tuyệt đối: `E:/zo-math/assets/...`.

## Ghi chú
- **Thư mục làm việc**: Chạy từ thư mục chứa TikZ.
- **Font STIX**: Kiểm tra `.woff2` trong `E:\zo-math\assets\fonts\`.
- **Kiểm tra SVG**: Mở trong trình duyệt để xác nhận.
