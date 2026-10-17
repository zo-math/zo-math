# R1-G02 — Đồng bộ nhãn cấp chứa, chưa phát hành

Đã áp dụng cùng quy tắc 07/6.2 và bộ ghép zo_course_labels.py như R1-G04; mode parent-context-v1. Giữ nguyên cấu trúc nguồn, câu hỏi, lời giải, ID và số; bổ sung context tường minh cho chặng/lượt/nơi phát hiện, Phối hợp/Chuyển giao và lời giải tại chỗ. Không đưa mọi lời giải vào ngữ cảnh Lời giải khi nó thực sự thuộc Bài học/Ôn nền.

[Mở HTML thực tế](../../../../../../../_audit/r1_previous_labels_20261017/g02-reading.html). [Kiểm kê từng nhãn và fingerprint](dong_bo_nhan_20261017.json).

- 192 nhãn đã kiểm; HTML 953/953.
- Dựng đúng HTML của gói qua CLI QMD, không lỗi/cảnh báo; dùng lại hình vector đã kiểm. Không dựng PDF học liệu.
- Chính văn sau bỏ nhãn/trạng thái PDF, toàn bộ toán theo thứ tự và toàn bộ ID khớp bản phát hành. Metadata chức năng/số/cặp đề–lời giải không đổi.
- Kiểm trình duyệt toàn bộ ba gói đạt 315/315 ở 1440/430/390 px; đã xem lát cắt thật. Kiểm cũ G01 209/209, G02 332/332, G03 1263/1263 sau thay đúng các giả định nhãn hết hiệu lực.
- Tệp PDF vẫn là bản đã phát hành. Thẻ tải đọc provenance thật và ghi đang chờ cập nhật khi cần; không ghi lại hash/receipt cũ để nhận CURRENT.

HTML mới chờ chủ trì xem. Chủ trì giao commit mốc nguồn, chưa xuất bản lại, chưa tạo PDF hoặc push. Báo cáo/ảnh/bản xem cần duyệt giữ trong _audit/r1_previous_labels_20261017/; vùng dựng và cache do lượt này tạo được dọn sau kiểm. Công cụ kiểm dùng lại: scripts/zo_course_context_labels_check.py.
