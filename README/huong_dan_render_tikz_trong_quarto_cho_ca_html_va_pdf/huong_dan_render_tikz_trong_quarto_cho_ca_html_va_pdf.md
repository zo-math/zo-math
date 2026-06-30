# Hướng dẫn render TikZ trong Quarto cho cả HTML và PDF

## 1. Tổng quan
Khi sử dụng TikZ trong Quarto, ta cần đảm bảo hình ảnh hiển thị đúng khi xuất sang cả **HTML** (cần SVG) và **PDF** (cần PDF). Vì vậy, ta sẽ:

1. Tạo hình vẽ bằng TikZ trong `figure.tex`
2. Xuất `figure.tex` thành `figure.pdf`
3. Chuyển `figure.pdf` thành `figure.svg`
4. Dùng chung tham chiếu `![Hình minh họa TikZ](figure)` trong `.qmd`, Quarto sẽ tự chọn định dạng phù hợp.

---

## 2. Nội dung file `.qmd`
```yaml
---
title: "Dùng TikZ trong Quarto"
format:
    html:
        math: mathjax
        default-image-extension: svg
    pdf:
        pdf-engine: lualatex
        default-image-extension: pdf
---

![Hình minh họa TikZ](figure)
```

---

## 3. Nội dung file `figure.tex`
```latex
\documentclass{standalone}
\usepackage{tikz}
\begin{document}
    \begin{tikzpicture}
        \draw[thick] (0,0) circle (1cm);
        \draw[->] (-1.5,0) -- (1.5,0);
        \draw[->] (0,-1.5) -- (0,1.5);
    \end{tikzpicture}
\end{document}
```

---

## 4. Các lệnh cần thiết
### 4.1. Biên dịch TikZ thành PDF
```sh
lualatex -shell-escape figure.tex
```
Kết quả: `figure.pdf`

### 4.2. Chuyển PDF thành SVG
Nếu có `pdf2svg`, chạy:
```sh
pdf2svg figure.pdf figure.svg
```
Nếu dùng **Inkscape**, chạy:
```sh
inkscape figure.pdf --export-type=svg --export-filename=figure.svg
```

---

## 5. Tự động hóa với Makefile (tùy chọn)
Nếu dùng Linux/macOS, có thể tạo `Makefile` để tự động thực hiện:
```makefile
all: figure.pdf figure.svg

figure.pdf: figure.tex
	lualatex -shell-escape figure.tex

figure.svg: figure.pdf
	pdf2svg figure.pdf figure.svg
```
Chạy lệnh:
```sh
make
```

---

## 6. Kết luận
Với cách này, mình chỉ cần viết hình TikZ một lần trong `figure.tex`, rồi sử dụng nó trong `.qmd` mà không cần quan tâm đến định dạng khi xuất bản. 🚀

# Vấn đề đồng bộ phông

Mình muốn đảm bảo rằng phông chữ (cả chữ thường và toán học) trong các hình minh họa TikZ (được biên dịch từ tệp `figure.tex`) trông giống hệt với phông chữ của phần văn bản và công thức toán trong tệp `.qmd` khi xuất ra HTML hoặc PDF.  

Điều này có nghĩa là mình cần đồng bộ:
1. **Phông chữ chữ thường** giữa tài liệu Quarto và hình vẽ TikZ.  
2. **Phông chữ toán học** để công thức trong hình vẽ giống với công thức bên ngoài hình vẽ.  

Mình có thể xác nhận xem đây có đúng là vấn đề mình đang gặp phải không? Nếu đúng, mình sẽ hướng dẫn cách đồng bộ hoá chúng. 🚀

Mình muốn đảm bảo rằng:

1. Toàn bộ dự án Quarto (HTML & PDF) sử dụng STIX Two Text và STIX Two Math.

2. Hình vẽ TikZ cũng sử dụng đúng các phông này.

3. Màu sắc và kiểu chữ của TikZ phù hợp với theme của Quarto.