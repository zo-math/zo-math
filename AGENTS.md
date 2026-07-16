# Chỉ dẫn cho agent trong repository ZO Math

> Đây là tài liệu điều phối nội bộ dành cho agent làm việc với mã nguồn, tài sản và tài liệu xây dựng ZO Math.
>
> Đây không phải là nội dung xuất bản dành cho người đọc ZO Math.

## Chỉ dẫn bắt buộc

Trước khi thực hiện bất kỳ nhiệm vụ nào trong repository này, phải đọc và tuân thủ:

- `quy_trinh_xay_dung/quy_tac_lam_viec_voi_agent.md`
- `quy_trinh_xay_dung/quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md`

Hai tài liệu trên đã được người dùng xác nhận là đang có hiệu lực trên toàn repository:

- `quy_tac_lam_viec_voi_agent.md` quy định nguyên tắc, giới hạn và thứ tự ưu tiên của nguồn chỉ dẫn;
- `quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md` quy định cách agent tiếp nhận, thực hiện, kiểm tra và báo cáo một nhiệm vụ kỹ thuật.

Khi chạy lệnh Python trong repository này, Codex phải dùng trình khởi chạy repository-local:

```text
python scripts/zo_python.py ...
```

Trình khởi chạy bảo đảm tiến trình Python con dùng chế độ UTF-8 mà không yêu cầu thay đổi biến môi trường global.

Mọi lệnh Quarto do Codex chạy trong repository này phải đi qua trình khởi chạy Quarto repository-local, và trình này phải được gọi qua `scripts/zo_python.py`:

```text
python scripts/zo_python.py scripts/zo_quarto.py <quarto-command> [tham số...]
```

Không ghi đường dẫn tuyệt đối tới executable Python vào metadata QMD. Cơ chế trên bảo đảm Jupyter và reticulate dùng nhất quán môi trường Python hiện hành theo cách portable.

Codex dùng `scripts/zo_check_repo.py` làm điểm vào mặc định cho kiểm tra kỹ thuật và luôn gọi qua `scripts/zo_python.py`. Chọn chế độ `quick`, `scope` hoặc `render` theo phạm vi nhiệm vụ. Công cụ này không thay thế kiểm tra trực quan, xuất bản hoặc kiểm tra chuyên biệt chưa được tích hợp.

Khi nhiệm vụ liên quan đến lưới thẻ, phải đọc và tuân thủ thêm:

- `quy_trinh_xay_dung/quy_chuan_luoi_the.md`

Tài liệu này chỉ điều hành các nhiệm vụ liên quan đến dữ liệu, mã sinh, giao diện, đầu ra và kiểm tra lưới thẻ.

Các tài liệu khác trong `README/`, `content/`, `assets/`, `_audit/` hoặc những vị trí khác không tự động được xem là quy chuẩn hiện hành, trừ khi:

- yêu cầu hiện tại của người dùng dẫn chiếu rõ đến tài liệu đó;
- `AGENTS.md` dẫn chiếu đến tài liệu đó;
- một tài liệu quy chuẩn hiện hành xác định rõ phạm vi áp dụng của nó.

Khi nhiệm vụ liên quan đến một lĩnh vực chưa có tài liệu chuyên biệt được dẫn chiếu tại đây, phải:

1. khảo sát hiện trạng kỹ thuật và các nguồn liên quan;
2. phân biệt bằng chứng hiện trạng với quyết định thiết kế;
3. không tự phong tài liệu cũ thành quy chuẩn;
4. hỏi người dùng khi cần một quyết định chưa được xác lập.

Các tài liệu chuyên biệt về Quarto, giao diện, biên tập, TikZ, LaTeX, SVG, Manim, Git, render, audit và xuất bản sẽ được bổ sung vào tệp này sau khi được người dùng phê duyệt.
