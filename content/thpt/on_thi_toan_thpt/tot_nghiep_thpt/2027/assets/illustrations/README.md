# Bộ ảnh trang Nhà 2027

**Đã khép việc tìm ảnh — 15/10/2026:** chủ trì đã tải lại ảnh vuông và
thay vào đúng thư mục, đồng thời yêu cầu khép nhiệm vụ. Bản 1:1 hiện tại
có SHA-256 `f5123bd916d610434b5029f307f3687f21a120d538c7c279bd8fe3a66a460573`.
Manifest hiện hành là `../../giao_dien/bo_anh_bia.json`; biên bản nhập cũ
chỉ giữ lịch sử, không được dùng để ghi đè lại ảnh chủ trì vừa thay.

Bộ bìa **Hành trình của người học toán** gồm đủ năm tệp đang được giữ để
sử dụng, không phải năm bản thử. Trang Nhà hiện hiển thị bản 3:4 trên mọi
chiều rộng; các bản còn lại phục vụ lựa chọn định dạng khi truyền thông.
Không xóa ảnh chỉ vì QMD hiện không tham chiếu đến ảnh ấy.

| Tỉ lệ | Tệp | Kích thước (px) |
|---|---|---|
| 1:1 | [hanh_trinh_nguoi_hoc_toan_1x1.png](hanh_trinh_nguoi_hoc_toan_1x1.png) | 1254 × 1254 |
| 3:4 | [hanh_trinh_nguoi_hoc_toan_3x4.png](hanh_trinh_nguoi_hoc_toan_3x4.png) | 1086 × 1448 |
| 4:3 | [hanh_trinh_nguoi_hoc_toan_4x3.png](hanh_trinh_nguoi_hoc_toan_4x3.png) | 1448 × 1086 |
| 9:16 | [hanh_trinh_nguoi_hoc_toan_9x16.png](hanh_trinh_nguoi_hoc_toan_9x16.png) | 941 × 1672 |
| 16:9 | [hanh_trinh_nguoi_hoc_toan_16x9.png](hanh_trinh_nguoi_hoc_toan_16x9.png) | 1672 × 941 |

SHA-256 và kích thước bộ đang dùng nằm tại `../../giao_dien/bo_anh_bia.json`.
Đường dẫn nguồn nhập và dấu kiểm tại mốc nhập được giữ nguyên trong
`../../giao_dien/reference/tai_nguyen_trang_nha_mau_3.json`.
Bốn bản 1:1, 4:3, 9:16, 16:9 từng bị dọn nhầm; ngày 15/10/2026 đã khôi
phục từ Git `fb425ca1`. Sau đó chủ trì thay bản vuông; bốn tỉ lệ còn lại
giữ nguyên byte tại mốc nhập. Không tạo lại, cắt hoặc nén ảnh.

Minh họa học trực tiếp hiện dùng `hoc_truc_tiep_buoi_hoc.svg`; PNG cùng tên
là nguồn của SVG, phải giữ cả hai. Bản cũ `hoc_truc_tiep_trao_doi.svg` đã
nghỉ dùng, được chuyển ra kho ngoài repository, có manifest SHA-256 tại
`E:/zo_nhap/zo_math_archive/home-cover-assets-20261015/manifest.json`.

Kiểm trước bàn giao hoặc dọn tài sản:

```text
python scripts/zo_python.py -B scripts/zo_home_cover_check.py
```

Phép kiểm bảo vệ đủ năm định dạng và nguyên byte, đồng thời xác nhận QMD
vẫn chỉ chọn bản 3:4 và không còn gọi minh họa học trực tiếp cũ. Đây là
kiểm tài sản nguồn, không phải nghiệm thu hình ảnh mới hoặc xuất bản.
