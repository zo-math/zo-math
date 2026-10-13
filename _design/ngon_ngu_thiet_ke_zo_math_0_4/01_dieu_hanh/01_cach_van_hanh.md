# Cách chủ dự án vận hành

## Mỗi lần làm việc

Bạn giao một kết quả cụ thể, ví dụ “Áp dụng thiết kế 0.4 cho trang khóa học 2027 theo phạm vi vừa kiểm kê, dựng bản xem thử”. AI phải hiểu sản phẩm, phạm vi và đầu ra; nếu chúng đã rõ thì tiến hành. Nó đọc hướng dẫn chung cùng hướng dẫn của sản phẩm đó, không bắt bạn học tên từng token.

Mỗi nhiệm vụ đi qua bốn bước: **đọc hiện trạng → áp dụng trong phạm vi → dựng và kiểm → ghi nhận để tiếp tục**. Nếu mới kiểm kê, kết quả là bản đồ tích hợp; nếu giao triển khai, kết quả phải có sản phẩm mở/xem/nghe được. Một báo cáo thay đổi không thay cho sản phẩm.

## Bạn cần duyệt điều gì?

- Nội dung và cảm giác của sản phẩm ở kích thước sử dụng thật.
- Chi tiết còn thử mà bạn muốn biến thành quy tắc lâu dài.
- Phạm vi mở rộng hoặc xuất bản khi đến bước đó.

Yêu cầu bạn đã nêu, như mã Xám ZO, không gạch chân, hàng hàm số phẳng, không cần được hỏi lại. Các sửa nhỏ để thực hiện đúng yêu cầu nằm trong nhiệm vụ đã giao.

Khi bạn nói “mẫu này dùng được cho khóa 2027”, AI ghi đúng phạm vi đó. Khi bạn nói “dùng làm chuẩn chung cho video”, AI ghi phạm vi video. Một câu khen sản phẩm không tự phê duyệt mọi thành phần của hệ thiết kế.

## Muốn thay đổi một quy tắc

Mô tả điều muốn sửa và lí do. AI tìm mã quy tắc liên quan, ghi yêu cầu mới có trích dẫn, xác định sản phẩm bị ảnh hưởng, dựng mẫu nếu cần, rồi cập nhật dữ liệu/quy chuẩn/nhật kí cùng nhau. Mẫu cũ được giữ để so sánh. Không thay mọi sản phẩm cũ trong một lượt nếu bạn chỉ yêu cầu đổi sản phẩm mới.

Thay màu gốc phải cập nhật nguồn dữ liệu rồi sinh lại cấu hình cho từng công cụ. Thay cách dùng màu chỉ cần sửa vai trò đúng phạm vi. Không tìm-thay số hex toàn repo một cách mù quáng.

## Làm việc qua nhiều AI và nhiều repo

Bản gốc bộ điều hành nằm ở E:\zo_math\_design\zo_math_0_4 và được quản lí bằng Git sau khi bạn cho phép lưu commit. Với repo video/công cụ ảnh, AI đọc bản gốc; khi triển khai, chép bản phát hành cần thiết vào repo đích, ghi phiên bản và hash. Những bản nhận không tự sửa thành chuẩn mới; yêu cầu đổi được trả về bản gốc để xét phạm vi.

Không dùng đường dẫn tuyệt đối tới ổ E: làm phụ thuộc của sản phẩm đã đóng gói. Các công cụ phải dựng được từ tài nguyên trong repo/gói của chúng. Đường dẫn ổ E: ở đây chỉ giúp tìm nơi làm việc trên máy hiện tại.

Chỉ nên có một phiên đang sửa sổ quyết định chung. Mỗi phiên cập nhật theo trạng thái mới nhất, không ghi đè nhật kí của phiên khác. Báo cáo local có thể được gửi cho AI điều hành; sản phẩm minh họa gửi kèm khi quyết định cần xem/nghe.

## Cuối phiên

AI báo: đã thay gì, sản phẩm xem ở đâu, đã kiểm gì, chưa kiểm gì, trạng thái hiện tại và bước tiếp theo. Hồ sơ nằm trong tệp để phiên sau tiếp tục. Không bắt buộc bạn xuất nhận xét JSON; phản hồi trực tiếp được AI ghi lại với nguồn và phạm vi.
