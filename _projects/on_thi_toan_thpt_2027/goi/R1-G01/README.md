# ZO Math — R1-G01

**Chuyển tiếp 10/10/2026:** toàn bộ trạng thái, nguồn `src/` và lệnh bên dưới thuộc gói v1.1 lịch sử. Nguồn canonical hiện hành là `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd`; tiếp quản tại [README vận hành](../../../../content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/_quy_trinh/README.md) và [bộ điều hành khóa](../../../../content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/README.md). Không biên tập hoặc tái sinh gói cũ để thay FB036; giữ nội dung phía dưới làm provenance, không nguồn sản xuất song song.

Gói học liệu **Kết nối hàm số, bảng biến thiên và đồ thị**, thuộc dự án ZO Math — Ôn thi Toán THPT, Ấn bản ôn thi 2027.

## Trạng thái

- Nghiên cứu đã kết tinh ở cấp gói.
- Bản dùng thử v1.0 đã được đọc và tiếp nhận góp ý.
- Bản v1.1 là ứng viên đang thẩm định sau vòng đọc thứ nhất.
- Chưa duyệt phát hành, chưa công bố website và chưa sản xuất Studio chính thức.
- Chưa có dữ liệu học sinh sử dụng v1.1.

## Điểm vào

- Đọc và thẩm định trên màn hình: `R1-G01_HOC_LIEU_v1.1.html`.
- Đọc hoặc in bản đầy đủ lời giải: `R1-G01_HOC_LIEU_v1.1.pdf`.
- Nội dung Markdown được sinh: `R1-G01_NOI_DUNG_v1.1.md`.
- Hồ sơ nội dung, nguồn, quyết định và trạng thái: `R1-G01_ho_so.md`.
- Nguồn sản xuất canonical: `src/noi_dung.html` cùng dữ liệu, mã dựng và tài sản trong `src/`.
- Kết quả kiểm tra: `kiem_chung/kiem_tra_thanh_pham.md`.

Không chỉnh trực tiếp HTML, Markdown hoặc PDF đầu ra. Khi sửa học liệu, chỉnh đúng nguồn trong `src/`, tái sinh các đầu ra và kiểm tra lại phần bị ảnh hưởng.

## Tái sinh

Từ gốc repository:

```text
python scripts/zo_python.py _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/zo_bieu_dien.py
python scripts/zo_python.py _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/dong_goi.py
python scripts/zo_python.py _projects/on_thi_toan_thpt_2027/goi/R1-G01/src/xuat_pdf.py
```

Việc tái sinh không thay đổi trạng thái phát hành. Chỉ chủ dự án mới quyết định duyệt phát hành hoặc công bố.
