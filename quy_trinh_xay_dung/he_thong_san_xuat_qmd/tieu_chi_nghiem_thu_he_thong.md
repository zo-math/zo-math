# Tiêu chí nghiệm thu hệ thống sản xuất và kiểm định QMD

> **Trạng thái:** Bản thiết kế v1.0 — Giai đoạn 1.

## 1. Phạm vi nghiệm thu

Hệ thống phiên bản đầu chỉ được xem là đạt khi chứng minh được:

- một lõi phục vụ ít nhất hai dự án;
- 100+ Hàm số không bị suy yếu;
- 100+ Bài toán thực tế không phải mang các trường của hàm số;
- checker vẫn có một điểm vào thống nhất;
- xuất bản vẫn do người dùng quyết định.

## 2. Kiến trúc

Đạt khi:

- bốn tầng được biểu diễn rõ;
- cấu hình dự án cục bộ được khám phá xác định;
- hồ sơ tách vùng lõi và vùng mở rộng;
- registry mô-đun không cho thực thi mã tùy ý;
- thứ tự thẩm quyền rõ;
- lõi không chứa đường dẫn riêng của dự án.

## 3. Cấu hình dự án

Đạt khi:

- schema có phiên bản;
- cấu hình sai bị từ chối với thông báo rõ;
- đường dẫn không thể thoát repository;
- loại bài không chồng lấn;
- mô-đun không đăng kí bị từ chối;
- cổng xác nhận xuất bản không thể bị tắt;
- checker nhận diện đúng bài của hai dự án.

## 4. Checker

Đạt khi:

- giữ `quick`, `scope`, `render`;
- giữ `--staged`, `--report`;
- validator lõi chạy cho cả hai dự án;
- validator dự án chỉ chạy đúng phạm vi;
- validator sau render vẫn hoạt động;
- báo cáo JSON giữ thông tin cốt lõi;
- mã thoát nhất quán;
- checker không sửa tệp;
- checker không xuất bản.

## 5. Hồi quy 100+ Hàm số

Đạt khi `ham_ln_x.qmd`:

- được nhận diện đúng;
- không cần sửa nội dung;
- không có `FAIL` mới;
- HTML vẫn có lớp trang và liên kết PDF;
- PDF Title vẫn khớp;
- hồ sơ hình vẫn được kiểm tra;
- số hình mở rộng vẫn bằng 0;
- thẻ 114 vẫn `pending`;
- `href` vẫn rỗng;
- không có thay đổi ngoài phạm vi.

## 6. Kiểm nghiệm dự án thứ hai

Đạt khi một bài 100+ Bài toán thực tế:

- có cấu hình dự án riêng;
- có hồ sơ mở rộng riêng;
- không chứa trường bắt buộc của hàm số;
- dùng cùng metadata lõi;
- dùng cùng HTML/PDF;
- chạy cùng checker;
- có validator nội dung dự án;
- tạo báo cáo cùng định dạng;
- giữ `pending` cho tới khi người dùng xác nhận.

## 7. Tài liệu

Đạt khi:

- có tài liệu lõi;
- có schema cấu hình;
- có mẫu hồ sơ lõi;
- có hướng dẫn thêm dự án;
- có hướng dẫn thêm validator;
- có đường cơ sở hồi quy;
- tài liệu có thẩm quyền được dẫn chiếu đúng cấp;
- không có hai tài liệu cùng cấp mâu thuẫn.

## 8. Vận hành

Đạt khi một phiên mới có thể:

1. đọc `AGENTS.md`;
2. đọc tài liệu cỗ máy QMD;
3. tìm cấu hình dự án;
4. tìm hồ sơ bài;
5. chạy checker;
6. hiểu trạng thái;
7. tiếp tục công việc mà không cần toàn bộ lịch sử hội thoại.

## 9. Hiệu quả

Đạt khi:

- không cần sao chép checker cho dự án mới;
- không cần sao chép toàn bộ quy chuẩn kĩ thuật;
- thêm dự án chủ yếu bằng cấu hình, hồ sơ mở rộng và validator chuyên biệt;
- thay đổi lõi có hồi quy rõ;
- token hội thoại được giảm nhờ tài liệu bền vững trong repository.

## 10. Không đạt

Hệ thống không đạt nếu:

- chỉ đổi tên hằng mà chưa tách trách nhiệm;
- YAML trở thành nơi chứa logic khó kiểm soát;
- dự án mới phải điền trường hàm số;
- checker bị chia thành nhiều script độc lập;
- bài hồi quy phải sửa để phù hợp hệ thống;
- trạng thái nghiệm thu và xuất bản vẫn bị trộn;
- xuất bản có thể xảy ra không cần xác nhận;
- kiểm định tự động được coi là nghiệm thu cuối.

## 11. Điều kiện nghiệm thu phiên bản 1.0

Phiên bản 1.0 được nghiệm thu khi đồng thời:

- toàn bộ tiêu chí kiến trúc đạt;
- cấu hình hai dự án hợp lệ;
- `ham_ln_x` hồi quy đạt;
- bài thử dự án thứ hai đạt;
- kiểm tra tự động không có `FAIL`;
- quan sát HTML/PDF hoàn tất;
- tài liệu chuyển giao đủ;
- người dùng xác nhận hệ thống đạt.

## 12. Kết luận

Nghiệm thu hệ thống không dựa vào số lượng tệp hoặc độ phức tạp của checker.

Tiêu chí quyết định là: một lõi rõ, hai dự án thực dùng được, hồi quy an toàn và quyền xuất bản vẫn thuộc người dùng.
