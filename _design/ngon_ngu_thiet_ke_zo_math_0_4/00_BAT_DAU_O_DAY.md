# ZO Math — bắt đầu ở đây

**Bộ tài nguyên và điều hành 0.4.2 · Mẫu thiết kế 0.4 · 07/10/2026**

Đây là một bộ tài liệu, dữ liệu, tài sản và quy trình; không phải ứng dụng cần cài đặt, cũng chưa phải Design System 1.0.

## Lần đầu: làm ba việc

1. Giải nén để có thư mục `E:\zo_math\_design\zo_math_0_4`. Không chép đè một bản đang dùng; nếu đã có, giữ riêng bản vừa tải cho AI đối chiếu trước khi cập nhật.
2. Mở `E:\zo_math` bằng VS Code. Mở tệp [01_dieu_hanh/00_LENH_KHOI_DONG_AI.txt](01_dieu_hanh/00_LENH_KHOI_DONG_AI.txt), sao chép toàn bộ nội dung gửi cho Codex. Lệnh này bắt đầu bằng kiểm kê tích hợp web, chưa sửa giao diện hoặc xuất bản.
3. Đọc báo cáo Codex trả về: phạm vi nào sẽ áp dụng, tệp nào cần sửa, kiểm bằng cách nào. Từ đó giao nhiệm vụ áp dụng trong phạm vi cụ thể.

Trước khi render/publish repo, AI phải kiểm và loại thư mục bộ bàn giao khỏi đầu vào render, resources và đầu ra công khai. Mẫu có nhiều QMD/tài nguyên nghiên cứu; không tự đưa chúng vào website.

## Khi bạn quay lại vào một ngày khác

Mở bộ này và nói với AI: **“Đọc bộ điều hành thiết kế ZO Math tại `E:\zo_math\_design\zo_math_0_4`, cho biết trạng thái hiện tại rồi tiếp tục nhiệm vụ đang ghi.”** AI đọc sổ công việc, không đoán từ trí nhớ chat.

Bạn chỉ cần mô tả kết quả muốn có và xem sản phẩm được dựng. AI chịu trách nhiệm đọc quy chuẩn đúng phạm vi, kiểm mã nguồn, làm việc, kiểm đầu ra và cập nhật nhật kí. Những điểm thiết kế chưa chốt chỉ cần hỏi khi chúng thực sự cản trở nhiệm vụ; không bắt bạn duyệt lại các yêu cầu đã rõ.

## Đọc gì để hiểu bộ này?

- [Cách bạn vận hành](01_dieu_hanh/01_cach_van_hanh.md): dùng hằng ngày, duyệt và cập nhật.
- [Ngôn ngữ ZO Math hiện có](02_quy_chuan/00_tong_quan.md): bản cô đọng để đọc hiểu.
- [Sổ yêu cầu và mẫu thử](01_dieu_hanh/02_so_quyet_dinh.md): điều đã được xác nhận và điều còn thử.
- [Bản đồ tài nguyên](01_dieu_hanh/03_ban_do_tai_nguyen.md): tìm đúng tệp để dùng.
- [Mở bộ mẫu 0.4](07_mau_thi_giac/index.html): xem, nghe và dùng thử ngoại tuyến.
- [Mở R1-G01 mẫu](07_mau_thi_giac/r1_g01.html): mẫu đối chiếu thiết kế; nội dung sản xuất lấy từ repo hiện tại.

## Điều bạn đã có sau khi tải

Có đủ 30 tệp đầu vào được cung cấp, bản giải nén nguồn, toàn bộ bộ kiểm thử 0.4 đã phát hành, tài sản chỉnh sửa, quy tắc có căn cứ, chỉ dẫn cho AI, sáu hướng dẫn tích hợp và mẫu ghi nhận công việc. Bạn không cần chuyển JSON nhận xét vào một thư mục để bộ này hoạt động.

Bộ này không truy cập ổ E: của bạn từ cuộc trò chuyện. Trạng thái repo video, công cụ ảnh và website cần được AI trên máy kiểm tra khi bắt đầu. Không coi “đã có mẫu” là “đã áp dụng vào repo”.

## Phiên bản

`0.4` chỉ phiên bản mẫu thị giác. `0.4.2` là bản vá hồ sơ bàn giao, không thay đổi thiết kế 0.4. Màu/yêu cầu đã xác nhận được tách khỏi cách thể hiện còn thử. Chi tiết và bằng chứng kiểm gói ở [báo cáo bàn giao](08_cong_cu/BAO_CAO_BAN_GIAO.md).
