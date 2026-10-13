# Chỉ dẫn cho AI làm việc với bộ bàn giao ZO Math

Đọc [điểm bắt đầu](00_BAT_DAU_O_DAY.md), [quy trình AI](01_dieu_hanh/04_quy_trinh_cho_ai.md), [trạng thái công việc](09_nhat_ki/cong_viec_hien_tai.json) và hướng dẫn của đúng sản phẩm. Không cần đọc lại toàn bộ kho nguồn mỗi phiên.

- Chỉ dẫn hiện tại của chủ dự án có ưu tiên; ghi lại thay đổi phạm vi/tiêu chí có ảnh hưởng lâu dài. Tuân quy tắc repo đích đang có. Không tự dùng tài liệu lịch sử để phủ nhận yêu cầu mới.
- `03_du_lieu/quy_tac.json` tách yêu cầu đã xác nhận khỏi mẫu thử. Không đồng nhất “được tạo”, “được dùng thử” và “được chủ dự án duyệt cuối”.
- `06_nguon` và `07_mau_thi_giac` là tham chiếu gốc. Không chạy hàng loạt script mẫu, sửa gốc hoặc chép toàn bộ CSS vào sản xuất. Làm lớp tích hợp trong repo đích và giữ cách quay lại cấu hình cũ.
- Yêu cầu tính đúng của Toán và bảo toàn nội dung có hiệu lực. Không sửa kiến thức, đáp án, ID, luồng học hoặc dữ liệu vì thay thiết kế; nếu nhiệm vụ có bao gồm sửa nội dung thì ghi phạm vi đó riêng.
- Làm hết thao tác đọc/kiểm/chỉnh sửa đã được giao. Hỏi chủ dự án khi phải chọn quyết định thiết kế chưa rõ có ảnh hưởng lớn, hoặc làm việc ngoài phạm vi. Không dựng các cổng xin phép cho việc thường lệ đã được ủy quyền.
- Không ghi đè thay đổi của người khác. Không dùng `git add .`. Không tự commit/push/publish nếu chưa nằm trong nhiệm vụ được giao. Audit tạm vào `_audit/` theo repo đích.
- Trước render, kiểm bộ bàn giao không bị đưa vào render/resources/publication. Không sửa toàn cục chỉ để làm đẹp một trang thử.
- Kết thúc phiên phải cập nhật công việc hiện tại, nhật kí và hồ sơ tiếp nhận sản phẩm; ghi kiểm đã chạy và chưa chạy. Không ghi “đạt” cho kiểm chưa thực hiện.

AGENTS.md này chỉ tự có phạm vi trong cây thư mục của nó. Khi làm việc ở repo khác, AI phải được yêu cầu đọc bộ này; không giả định VS Code tự nạp hay các cuộc trò chuyện tự đồng bộ.
