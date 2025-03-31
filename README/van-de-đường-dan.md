## Đường dẫn tài nguyên
- Dùng `/figures/...` trong `.qmd` để tham chiếu ảnh từ thư mục `figures/` ở gốc dự án.
- Khai báo `resources: - "figures/**"` trong `_quarto.yml` để Quarto sao chép tài nguyên vào thư mục đầu ra (`docs/`).
- Lý do: Tránh lỗi 404 và giảm phụ thuộc vào đường dẫn tương đối như `../`.