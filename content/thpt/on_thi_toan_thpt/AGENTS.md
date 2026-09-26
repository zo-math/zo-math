# Chỉ dẫn cho chuyên mục Ôn thi Toán THPT

Đây là tài liệu điều phối nội bộ, không phải nội dung xuất bản.

## Phạm vi và thẩm quyền

Tuân thủ `AGENTS.md` ở gốc repository và các tài liệu bắt buộc được dẫn chiếu tại đó. Quy chuẩn cục bộ là `_quy_trinh/quy_chuan_goi_qmd.md`; mẫu hồ sơ thiết kế là `_quy_trinh/mau_ho_so_san_xuat.yml`.

Kiến trúc đã được phê duyệt đặt chuyên mục tại `content/thpt/on_thi_toan_thpt`: học liệu dùng lại thuộc `hoc_lieu/<ma_goi>/`, điều hành khóa theo năm thuộc `tot_nghiep_thpt/<nam>/_quy_trinh/`. Không tạo một lớp điều hành song song bên ngoài chuyên mục sau khi hoàn tất chuyển đổi.

## Giới hạn tích hợp và đầu mối điều hành

- Hai cửa ngõ và R1-G01 có ứng viên ra mắt cục bộ để nghiệm thu; R1-G01 đã hoàn tất nội dung/kỹ thuật và có thể học, nhưng `publication: pending` và chưa xuất bản công khai.
- Không xem mẫu hồ sơ thiết kế của chuyên mục là schema CLI. Ứng viên R1-G01 có cấu hình và hồ sơ riêng trong `_quy_trinh/`; phải đọc README tại đó trước khi làm việc.
- Với khóa 2027, phải đọc `tot_nghiep_thpt/2027/_quy_trinh/README.md`: đây là đầu mối điều hành canonical duy nhất, ghi trạng thái chuyển đổi và việc tiếp theo. README cũ trong `_projects/on_thi_toan_thpt_2027` chỉ dùng để chuyển tiếp.
- Tài liệu đã khóa và thành phẩm lịch sử chỉ được chuyển hoặc sửa trong phạm vi chủ dự án giao; không suy từ việc chuyển quản trị thành quyền chuyển đổi học liệu.
- Không tạo trước thư mục gói tương lai hoặc tài nguyên chưa dùng.
- Không tự thay nội dung toán học, nhiệm vụ, thuật ngữ hoặc thiết kế đã chốt.

## Render, preview và xuất bản

Kế thừa dự án Quarto ở gốc; không tạo `_quarto.yml` độc lập. Hai trang cửa ngõ chưa thuộc một dự án QMD có cấu hình, nên dùng trình khởi chạy Quarto chung từ gốc repository:

```text
python scripts/zo_python.py scripts/zo_quarto.py render content/thpt/on_thi_toan_thpt --profile on-thi-preview
python scripts/zo_python.py scripts/zo_quarto.py preview content/thpt/on_thi_toan_thpt/index.qmd --profile on-thi-preview
```

Preview chỉ lắng nghe tại `127.0.0.1`. Navbar/sidebar nguồn dùng chung có đường vào ứng viên để kiểm tra đường đi; hàng rào publish vẫn chặn chuyên mục cho tới quyết định mở public riêng. Khi cần bảo toàn đầu ra hiện có trong một nhiệm vụ kiểm thử, dùng bản sao dự án cô lập dưới `_audit/`, giữ nguyên cấu hình dự án và profile.

Metadata `draft: true` không thay thế hàng rào xuất bản. `publish_public.yml` chặn toàn chuyên mục trong giai đoạn này và chặn `_quy_trinh` lâu dài. Không liên kết tài liệu điều hành từ trang dành cho người đọc, không khai báo resources quét cả cây chuyên mục.

Tuân thủ `quy_trinh_xay_dung/quy_trinh_xuat_ban_website.md`. Chỉ dùng `zo_publish.py check` khi kiểm tra; `prepare`/`publish`, staging, commit và push cần yêu cầu riêng. Không dùng `_publish_exclude.md` hoặc `.gitignore` làm hàng rào public.
