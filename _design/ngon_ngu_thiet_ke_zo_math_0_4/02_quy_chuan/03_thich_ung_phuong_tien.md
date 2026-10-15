# Thích ứng theo phương tiện

| Phương tiện | Giữ chung | Điều phải thích ứng |
|---|---|---|
| Web | Màu, logo, kiểu chữ theo vai trò, ý nghĩa hình/bảng | Responsive, sidebar/ToC, bàn phím, hover/focus, sáu nền, Sắc xám, lưu lựa chọn |
| PDF | Màu, logo, cấu trúc và cách diễn đạt Toán | Trang giấy, lề, ngắt trang, font nhúng, trắng đen, bìa/kết, QR và liên kết |
| Video | Căn tính đối tượng, màu/nét/nhãn, tinh thần diễn đạt | Thời gian, chuyển động, lời đọc, phụ đề, vùng an toàn, cỡ xem trên điện thoại |
| Ảnh bìa | Nhận diện và phân cấp | Crop, khung dọc/ngang, hình thu nhỏ, tiêu đề dài và CTA |

## Web

Chia khối theo chặng đọc có nghĩa; không biến từng đoạn thành thẻ. Màu nền ở ngoài, nội dung trên trắng. Sắc xám hoạt động độc lập. Trạng thái link/thẻ có dấu hiệu ngoài màu; bàn phím vẫn thấy focus. Thành phần Ủng hộ ở đầu trang, cuối chặng và vùng tải là mẫu triển khai, cần kiểm nhịp đọc thực.

## PDF

Bổ sung vận hành được chủ trì giao ngày 14/10/2026 tại
[hướng dẫn PDF](../04_ap_dung/06_pdf.md): thông tin ấn bản/bản quyền,
trang kết/Ủng hộ, bảng, nhịp trang và kiểm hồi quy. D0 là bản kiểm chứng;
không nâng mẫu 0.4 thành nghiệm thu mọi PDF hoặc khóa Design 0.5.

Bìa gọi rõ học liệu và bản tải; trang kết có bước tiếp theo, Ủng hộ và đường quay lại học. Tám PDF 0.4 đã thay đầu/cuối, ruột vẫn v1.3. Đây không phải bằng chứng toàn bộ ruột đã có tag/bảng phẳng 0.4. Khi tích hợp, lấy nội dung mới nhất và dựng bìa/kết từ quy trình sản xuất, kiểm phân trang, bookmark và links.

## Video và âm

Mỗi cảnh có một việc nhận thức: đặt đối tượng, quan sát biến đổi, dừng ở mốc, đối chiếu, kết luận. Khoảng dừng phải đủ đọc và nhìn; không áp đặt thời lượng clip mẫu lên mọi bài. Không dùng đoạn logo dài chiếm phần mở của video ngắn.

Tách vùng hình, diễn giải/kết luận và phụ đề. Khi thiếu chỗ, giảm số ý trên cảnh hoặc chia cảnh, không thu nhỏ mọi chữ. Video dọc cần bố trí lại thay vì crop bản ngang. Kiểm vùng bị giao diện nền tảng che tại thời điểm phát hành; không coi tọa độ vùng an toàn là vĩnh viễn.

Lời đọc ưu tiên rõ, đúng thuật ngữ và có khoảng nghỉ. Chú âm là nguồn riêng trong source_bundle/12_audio; chưa suy thành giọng thương hiệu cuối. Nhạc/cue chỉ hỗ trợ; mẫu focus/close 0.4 là ứng viên. Có thể dùng bản im lặng/phụ đề; không tự phát âm trong giao diện web. Kiểm nghe bản xuất trên thiết bị phổ thông, không chỉ đọc thông số RMS/peak.

## Ảnh bìa và thẻ

Bìa trước mở đúng câu hỏi/chủ đề, bìa sau kết và dẫn hành động thích hợp. Thumbnail phải đọc được ở kích thước nhỏ. Các tỉ lệ cùng hệ nhận diện nhưng cần template riêng. Nguồn nội dung tách khỏi template để công cụ sinh mới được, không chỉnh từng PNG.

## Ủng hộ và thông tin nhận

Dữ liệu QR/tài khoản trong mẫu lấy từ nguồn lúc dựng. Trước xuất bản thực tế, đối chiếu lại nguồn đang được chủ dự án dùng. Không bịa số tiền, số người ủng hộ, nhà tài trợ hoặc mục tiêu tài chính. Nút sao chép chỉ sao chép số, không thực hiện thanh toán.
