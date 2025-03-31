Mình đang gặp vấn đề với việc sử dụng `custom.tex` trong các tệp `.qmd` nằm ở các thư mục khác nhau trong dự án ZO Math. Cụ thể:

1. **Mình muốn sử dụng cùng một `custom.tex`** cho tất cả các `.qmd` trong dự án, bất kể chúng nằm ở độ sâu thư mục nào.
2. **Vấn đề phát sinh là nội dung bên trong cỉa `custom.tex` cần thiết lập đường dẫn đến thư mục chứa phông chữ cần dùng**, vì:
   - Nếu dùng **đường dẫn tuyệt đối** (ví dụ: `E:/zo-math/assets/fonts/`), thì khi di chuyển dự án hoặc đưa lên GitHub, đường dẫn sẽ không còn hợp lệ.
   - Nếu dùng **đường dẫn tương đối** (ví dụ: `../../../assets/fonts/`), thì nó phụ thuộc vào vị trí của `.qmd`. Khi một `.qmd` ở một thư mục sâu hơn, số lượng `../` có thể không đủ để quay về đúng thư mục `assets/fonts/`, gây lỗi khi biên dịch PDF.
3. **Mình muốn một giải pháp tổng quát**, sao cho:
   - Không cần chỉnh sửa đường dẫn trong `custom.tex` khi thay đổi hoặc thêm `.qmd`.
   - Dự án có thể hoạt động đồng nhất trên các máy khác nhau và khi đưa lên GitHub.
   - Không phải .qmd nào cũng cần render thành pdf nên mình không chấp nhận những cách liên quan đến việc thiết lập render pdf trong \_quarto.yml ch toàn bộ dự án.
