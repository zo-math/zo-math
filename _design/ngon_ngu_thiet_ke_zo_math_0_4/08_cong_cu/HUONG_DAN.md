# Công cụ kiểm bộ bàn giao

Chạy bằng Python 3, chỉ dùng thư viện chuẩn, không cần pip. AI trong repo có thể chạy giúp bạn.

```bash
python 08_cong_cu/zo_design.py status
python 08_cong_cu/zo_design.py check
python 08_cong_cu/zo_design.py find zo_graph
```

Các lệnh chỉ đọc, không sửa repo, không tải mạng, không áp dụng thiết kế hoặc xuất bản. Công cụ tìm gốc bộ theo vị trí chính nó nên không phụ thuộc thư mục đang đứng. Với Windows repo có launcher Python UTF-8, AI dùng launcher hiện có nếu cần.

`status` đọc phiên bản và công việc hiện tại. `find` tìm tên/đường dẫn tệp trong bộ, bỏ cache và _audit; không tìm ổ đĩa bên ngoài. `check` xác minh manifest, dữ liệu, tuyến đọc và liên kết tài liệu vận hành, đồng thời báo giới hạn tài liệu lịch sử. Lệnh trả mã khác 0 khi có lỗi cần xử lí. Nhật kí và audit là dữ liệu vận hành có thể thay đổi, không bị khóa hash bản phát hành.

Kiểm này không thay kiểm Quarto, trình duyệt, Manim, LaTeX hoặc nghe/nhìn sản phẩm; cũng không tự phê duyệt quy tắc. Mã công cụ và ca kiểm được kèm trong bộ.
