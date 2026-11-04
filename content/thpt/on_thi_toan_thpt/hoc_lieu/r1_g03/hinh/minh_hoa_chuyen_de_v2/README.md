# Đường tiệm cận — bộ minh họa v2

Chủ trì duyệt ảnh gốc ngày 04/11/2026. Bản v2 bỏ nhãn, tăng độ cao đường cong, giữ hai đuôi dài ép sát tiệm cận. Ảnh gốc đã chốt giữ nguyên byte trong `originals/r1_g03-approved.png`.

| Tỉ lệ | Kích thước PNG | Trạng thái |
|---|---|---|
| 1:1 | 1200 × 1200 | Bố trí lại — chờ duyệt riêng |
| 3:4 | 960 × 1280 | Bố trí lại — chờ duyệt riêng |
| 4:3 | 1280 × 960 | Bố trí lại — chờ duyệt riêng |
| 9:16 | 864 × 1536 | Bố trí lại — chờ duyệt riêng |
| 16:9 | 1600 × 900 | Giữ bố cục đã chốt |

Tất cả ảnh nền trong suốt. `candidates/` giữ nguyên các bản bố trí lại từ công cụ tạo ảnh, không dùng bản landscape nhỏ đặt vào khung dọc. `manifest.json` ghi hash, nguồn, bằng chứng duyệt và trạng thái riêng từng tỉ lệ. Bộ xuất chỉ khóa tỉ lệ chính xác bằng thu nhỏ đồng dạng trên canvas trong suốt, không cắt hình, kéo méo hoặc phóng lớn.

Danh mục khóa 2027 `_data/minh_hoa_chuyen_de.json` chọn v2 làm nguồn ảnh thẻ. Website tiếp tục dùng ảnh gốc đã chốt, không tự lấy các bố cục mới. V1 giữ riêng làm lịch sử, không là nguồn hiện hành.

Từ gốc repository:

```text
python -B scripts/zo_python.py -B scripts/zo_topic_art.py build --package r1_g03
python -B scripts/zo_python.py -B scripts/zo_topic_art.py check --package r1_g03
```

Không thay ảnh gốc đã duyệt; sửa thiết kế cần phiên bản mới và duyệt riêng. Không commit, push hoặc phát hành trong lượt tạo bộ ảnh này.
