# Đơn điệu và cực trị — bộ minh họa v1

Ảnh gốc đã được chủ trì chốt ngày 04/11/2026; viền các điểm cùng màu đỏ đường cong. `originals/` giữ nguyên byte bản đã duyệt. `manifest.json` ghi xuất xứ, SHA-256, bằng chứng duyệt, nguồn và trạng thái của từng tỉ lệ.

| Tỉ lệ | Kích thước PNG | Trạng thái |
|---|---|---|
| 1:1 | 1200 × 1200 | Bố trí lại — chờ chủ trì duyệt |
| 3:4 | 960 × 1280 | Bố trí lại — chờ chủ trì duyệt |
| 4:3 | 1280 × 960 | Bố trí lại — chờ chủ trì duyệt |
| 9:16 | 864 × 1536 | Bố trí lại — chờ chủ trì duyệt |
| 16:9 | 1600 × 900 | Giữ bố cục đã chốt |

`candidates/` giữ nguyên tệp công cụ tạo ảnh khi bố trí lại từng tỉ lệ. Các bản đó chỉ kế thừa ý tưởng/phong cách đã chốt, không kế thừa nghiệm thu bố cục. Bộ xuất chỉ chuẩn hóa canvas/thu nhỏ đồng dạng để khóa tỉ lệ chính xác, không cắt chữ/hình, kéo méo hoặc phóng lớn. Không dùng ảnh landscape nhỏ đặt giữa canvas dọc thay cho bố trí lại.

Danh mục nguồn duy nhất: `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_data/minh_hoa_chuyen_de.json`, tính từ gốc repo. Website vẫn dùng ảnh gốc đã duyệt, không tự dùng các bản chờ duyệt và không thay bìa học liệu/PDF.

```text
python -B scripts/zo_python.py -B scripts/zo_topic_art.py build --package r1_g01
python -B scripts/zo_python.py -B scripts/zo_topic_art.py check --package r1_g01
```

Không sửa đè ảnh gốc hoặc tự đổi trạng thái chờ duyệt. Thay ý tưởng/hình thức đã chốt cần phiên bản mới và bằng chứng duyệt riêng. Không suy quyền commit, push hoặc phát hành từ duyệt hình.
