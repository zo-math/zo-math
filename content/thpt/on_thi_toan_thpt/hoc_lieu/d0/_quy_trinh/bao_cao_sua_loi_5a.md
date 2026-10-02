# Báo cáo sửa lỗi Bước 5A — ánh xạ mạch D0

## Lỗi được phát hiện

Ứng viên HTML từng hiển thị `R5 — Số phức` trong khi ba nhiệm vụ R5 thuộc dãy số, mũ và lôgarit. Nguyên nhân là bảng tên mạch viết thủ công trong công cụ chuyển đổi, không được đối chiếu độc lập với Kế hoạch 0.6. Checker cũ so QMD với chính đầu ra của công cụ này nên hai phía nhất quán với cùng một lỗi.

## Phạm vi tác động

Lỗi nằm ở tám nhãn mạch do lớp chuyển đổi tạo. Dữ liệu baseline, 24 nhiệm vụ chính, 24 câu thử lại, ID, mã cụm, nguồn, lời giải và quan hệ họ câu không bị thay đổi. Kiểm tra 24 nhiệm vụ không phát hiện nhiệm vụ nào nằm sai mạch.

## Bản sửa

- Khóa tám tên mạch và miền mã cụm tại `strand_contract` trong `manifest_chuyen_doi.yml`.
- Công cụ sinh QMD đọc hợp đồng này, không giữ bảng tên riêng.
- Checker đọc độc lập mục 4.5 của Kế hoạch 0.6 rồi so khớp toàn bộ manifest và QMD.
- Checker kiểm tra ID của từng nhiệm vụ khớp trường `r` và mọi mã B trong `clusters` thuộc miền cho phép của mạch.
- Fixture âm cố ý đặt `R5` thành `Số phức` phải bị từ chối.
- Checker HTML kiểm tra đủ tám tiêu đề và cấm chuỗi `Số phức` trong đầu ra công khai.

## Bằng chứng sau sửa

- Checker chuyển đổi: PASS.
- Fixture âm `R5 — Số phức`: PASS theo nghĩa bị từ chối đúng.
- Checker toán lịch sử: PASS, 48/48 nhiệm vụ.
- Render canonical: PASS, không lỗi hoặc cảnh báo.
- Checker HTML: PASS; 24 nhiệm vụ chính, tám mạch, không có khối nội bộ hoặc ID thử lại.
- `git diff --check`: PASS.

Sửa lỗi này không thay đổi giới hạn sư phạm của D0: ba nhiệm vụ trong mỗi mạch chỉ là mẫu định vị ban đầu, không bao quát toàn bộ mạch và không đủ để kết luận mức thành thạo toàn mạch.
