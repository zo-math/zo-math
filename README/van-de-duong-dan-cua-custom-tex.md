Mình đang gặp vấn đề với việc sử dụng `custom.tex` trong các tệp `.qmd` nằm ở các thư mục khác nhau trong dự án ZO Math. Cụ thể:

1. **Mình muốn sử dụng cùng một `custom.tex`** cho tất cả các `.qmd` trong dự án, bất kể chúng nằm ở độ sâu thư mục nào.
2. **Vấn đề phát sinh là nội dung bên trong của `custom.tex` cần thiết lập đường dẫn đến thư mục chứa phông chữ cần dùng**, vì:
   - Nếu dùng **đường dẫn tuyệt đối** (ví dụ: `E:/zo-math/assets/fonts/`), thì khi di chuyển dự án hoặc đưa lên GitHub, đường dẫn sẽ không còn hợp lệ.
   - Nếu dùng **đường dẫn tương đối** (ví dụ: `../../../assets/fonts/`), thì nó phụ thuộc vào vị trí của `.qmd`. Khi một `.qmd` ở một thư mục sâu hơn, số lượng `../` có thể không đủ để quay về đúng thư mục `assets/fonts/`, gây lỗi khi biên dịch PDF.
3. **Mình muốn một giải pháp tổng quát**, sao cho:
   - Không cần chỉnh sửa đường dẫn trong `custom.tex` khi thay đổi hoặc thêm `.qmd`.
   - Dự án có thể hoạt động đồng nhất trên các máy khác nhau và khi đưa lên GitHub.
   - Không phải .qmd nào cũng cần render thành pdf nên mình không chấp nhận những cách liên quan đến việc thiết lập render pdf trong \_quarto.yml ch toàn bộ dự án.

   ---

**Vấn đề mình đang gặp phải:**

Mình đang cố gắng biên dịch một số tệp `.qmd` trong dự án Quarto của mình sang định dạng PDF bằng LuaLaTeX. Các tệp `.qmd` này cần sử dụng các tài nguyên bên ngoài, cụ thể là:

* **Font chữ STIX** nằm trong thư mục `assets/fonts/`.
* **Các thiết lập LaTeX tùy chỉnh** được định nghĩa trong tệp `assets/tex/custom.tex`.

Mình đang sử dụng tùy chọn `include-in-header` trong phần `pdf` của frontmatter mỗi tệp `.qmd` để nhúng các lệnh LaTeX cần thiết để thiết lập font và nhập tệp `custom.tex`.

**Cấu trúc thư mục dự án chính:**

```
e/zo-math/
├── assets/
│   ├── fonts/
│   │   ├── STIXTwoMath.otf
│   │   └── ... (các tệp font khác)
│   └── tex/
│       └── custom.tex
└── content/
    ├── zo-o/
    │   └── diu-dang-va-gai-goc/
    │       └── diu-dang-va-gai-goc.qmd
    └── zo-thau/
        └── xac-suat-va-thong-ke/
            └── bien-ngau-nhien/
                └── bien-ngau-nhien.qmd
```

**Các thử nghiệm và kết quả đã trao đổi:**

1.  **Thử nghiệm 1 (Lỗi ban đầu với `bien-ngau-nhien.qmd`):**
    * Tệp `bien-ngau-nhien.qmd` nằm ở `content/zo-thau/xac-suat-va-thong-ke/bien-ngau-nhien/`.
    * mình sử dụng `include-in-header` với đường dẫn `../../../../assets/fonts/` và `../../../../assets/tex/custom.tex`.
    * **Kết quả:** Lỗi "cannot find file ''".

2.  **Thử nghiệm 2 (`diu-dang-va-gai-goc.qmd` thành công):**
    * Tệp `diu-dang-va-gai-goc.qmd` nằm ở `content/zo-o/diu-dang-va-gai-goc/`.
    * mình sử dụng `include-in-header` với đường dẫn `../../../assets/fonts/` và `../../../assets/tex/custom.tex`.
    * **Kết quả:** Render PDF thành công.

3.  **Thử nghiệm 3 (Di chuyển `bien-ngau-nhien.qmd` lên một cấp):**
    * mình di chuyển `bien-ngau-nhien.qmd` đến `content/zo-thau/xac-suat-va-thong-ke/`.
    * mình sử dụng `include-in-header` với đường dẫn `../../../assets/fonts/` và `../../../assets/tex/custom.tex`.
    * **Kết quả:** Render PDF thành công.

4.  **Thử nghiệm 4 (Di chuyển `bien-ngau-nhien.qmd` lên hai cấp):**
    * mình di chuyển `bien-ngau-nhien.qmd` đến `content/zo-thau/`.
    * mình (ngầm hiểu) sử dụng `include-in-header` với đường dẫn `../../assets/fonts/` và `../../assets/tex/custom.tex`.
    * **Kết quả:** Lỗi tương tự (thiếu gói hoặc không tìm thấy tệp).

5.  **Thử nghiệm 5 (Nhúng trực tiếp cấu hình font vào `bien-ngau-nhien.qmd`):**
    * Tệp `bien-ngau-nhien.qmd` ở vị trí ban đầu.
    * mình nhúng trực tiếp các lệnh `\setmainfont` và `\setmathfont` với đường dẫn `../../../../assets/fonts/` vào `include-in-header`.
    * **Kết quả:** Lỗi "compilation failed- missing packages". (Sau khi cài đặt gói, lỗi có thể trở lại vấn đề đường dẫn).

**Vấn đề mình cần giải quyết một cách rõ ràng:**

Mình cần tìm ra một phương pháp **nhất quán và đáng tin cậy** để các tệp `.qmd` nằm ở các vị trí khác nhau trong cấu trúc thư mục của mình có thể **tham chiếu chính xác** đến các tài nguyên trong thư mục `assets/` khi biên dịch sang PDF.

Cụ thể, mình muốn:

* Sử dụng font chữ STIX và các thiết lập tùy chỉnh từ `custom.tex` trong các tệp PDF được tạo ra từ các `.qmd` khác nhau.
* Tránh việc phải điều chỉnh đường dẫn tương đối một cách thủ công cho mỗi tệp `.qmd` dựa trên vị trí của nó.
* Tìm hiểu nguyên nhân tại sao Quarto/LuaLaTeX dường như có hành vi khác nhau trong việc giải quyết đường dẫn tương đối tùy thuộc vào vị trí của tệp `.qmd`.
* Nếu có thể, tìm ra một cấu hình (có thể trong `_quarto.yml` hoặc cách khác) để quản lý các đường dẫn tài nguyên chung một cách hiệu quả cho toàn bộ dự án, đặc biệt là cho quá trình biên dịch PDF.

Mục tiêu cuối cùng là mình có thể đặt các tệp `.qmd` ở các vị trí logic trong cấu trúc dự án của mình mà không phải lo lắng về việc đường dẫn đến các tài nguyên chung bị sai khi tạo PDF.
