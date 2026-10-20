# R1-G05 — Bộ PDF và mục tải HTML, 21/10/2026

Chủ trì đã duyệt bản toàn văn 38 trang; biên nhận đúng hash ở `duyet_pdf_toan_van_20261021.json`. Đã sinh bảy bản theo chức năng, dựng lại toàn văn để đồng bộ đầu vào và thêm tám thẻ tải vào HTML canonical. Bộ mới chờ chủ trì xem; chưa commit, push hoặc xuất bản.

| Bản tải | Tệp trong gói | Số trang |
|---|---|---|
| Bản đầy đủ | [index.pdf](../../index.pdf) | 38 |
| Bản học và bài tập | [index_hoc_sinh.pdf](../../index_hoc_sinh.pdf) | 29 |
| Bài học | [index_bai_hoc.pdf](../../index_bai_hoc.pdf) | 14 |
| Luyện tập | [index_luyen_tap.pdf](../../index_luyen_tap.pdf) | 8 |
| Kiểm tra | [index_kiem_tra.pdf](../../index_kiem_tra.pdf) | 7 |
| Sửa lỗi | [index_sua_loi.pdf](../../index_sua_loi.pdf) | 10 |
| Ôn lại | [index_on_lai.pdf](../../index_on_lai.pdf) | 8 |
| Lời giải | [index_loi_giai.pdf](../../index_loi_giai.pdf) | 14 |

Tổng cộng 128 trang. Cả tám bản có Bảo trợ ở cuối, dùng cùng nguồn component HTML, logo/QR và bốn trường thông tin. Quy tắc đã được ghi ở AGENTS gốc, quy chuẩn gói/trang và hướng dẫn PDF dùng chung; bộ dựng không còn lược bỏ theo biến thể. Cổng chặn thiếu trang Bảo trợ, sai lời mời hoặc tài khoản trước thay PDF. Các PDF đã phát hành của gói khác không được dựng lại trong nhiệm vụ này.

Đã kiểm đủ tám bản CURRENT; mỗi bản đạt 23/23 kỹ thuật và hợp đồng bố cục tương ứng. Kiểm bao gồm phông nhúng, hình vector, cỡ nhãn, bảng, đích và số trang in, phạm vi từng biến thể, có/không có lời giải. Tám URL HTTP trả đúng byte PDF trong gói. HTML đạt 1954/1954, giữ 576 biểu thức, chín bảng và bảy câu nguồn đầy đủ. 12 chế độ đọc đã được mở ở 1440 và 390 px, không tràn ngang toàn trang.

Rà màu đủ 90 trang thuộc bảy biến thể mới; ba bố cục full/student/bai_hoc giữ nguyên qua lần dựng cuối được đối chiếu toàn bộ chữ và tọa độ. Toàn văn vẫn 38 trang và giữ bố cục đã duyệt. Đã xem các mẫu thang xám gồm hình bối cảnh, bảng, khối lời giải và Bảo trợ; chưa in giấy hoặc quét QR vật lý. Không coi kết quả kỹ thuật là chủ trì đã duyệt bộ mới.

Khi rà thấy trang gần trống do ngắt cứng trước mạch chính trong bản ngắn, đã thêm cấu hình `flow_functional_opening` ở hồ sơ in G05. Các bản chức năng nối phần nội dung sau Bắt đầu; full/student giữ bố cục cũ. Hồi quy in 32/32, hồi quy PDF/Bảo trợ 7/7. Lần dựng trước được giữ trong audit, không sửa tay PDF hoặc gia hạn hash để vượt cổng.

Nguồn là `index.qmd`, cấu hình sản xuất của gói và các component/bộ dựng được khai báo trong provenance. Tài nguyên hình chính thức, bản thảo và hướng bìa đã duyệt giữ nguyên byte. Hồ sơ máy đọc cạnh báo cáo ghi đủ hash, phạm vi duyệt và kết quả từng bản. Bằng chứng chi tiết ở `_audit/g05_pdf_set_20261021/`; không dùng audit làm đầu vào biên dịch.
