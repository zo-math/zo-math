# Video ZO Math

Nơi làm việc theo thông tin đã có: `E:/zo_math_video`. Trạng thái repo hiện tại: **cần AI tại máy xác minh**.

Quy tắc liên quan: ZO001, ZO003, ZO019, ZO020, ZO021, ZO025, ZO026, ZO027.

## Phạm vi

Giữ pipeline sản xuất đang hoạt động. Bản sao demo trong kho nguồn chỉ chứng minh một thời điểm trước; phải đọc cấu trúc hiện tại, hướng dẫn repo và trạng thái các mốc trong repo. Không khởi động lại M0 hay thay compiler chỉ vì bộ mẫu dùng script khác.

## Kiểm kê và nối vào hệ

Tìm nơi định nghĩa màu/font, scene/layout primitives, graph style, subtitle layout, timing, render và ghép FFmpeg. Đọc một sản phẩm gần đây cùng nguồn, không chỉ README. Kết quả kiểm kê phải chỉ rõ nơi gắn cấu hình 0.4 mà không sửa phần dữ liệu/kịch bản/timing ngoài nhiệm vụ.

Giữ ba nhóm riêng: nhận diện (màu/logo/chữ), bố cục (vùng hình/kết luận/phụ đề), thời gian (xuất hiện/di chuyển/dừng/đối chiếu). Tạo profile phiên bản và thành phần dùng lại trong engine hiện tại, thay vì gắn màu/cỡ chữ trực tiếp vào từng scene. Không copy nguyên số pt của TeX sang Manim.

Clip 0.4 được dựng bằng Python/Pillow/FFmpeg để minh họa ý đồ; nó không phải module Manim và không phải chuẩn fps. Giữ fps/codec của pipeline đã chọn trong repo, trừ khi nhiệm vụ riêng yêu cầu đổi và có kiểm.

## Mẫu để nghiệm thu

Dùng một nội dung thử đã có của dự án, mặc định tiếp tục mẫu đang làm trong repo; không tự thay bài toán chỉ để dễ render. So cùng nội dung trước/sau. Dựng video dọc đầy đủ với mở đầu, hình toán, lời/phụ đề, khoảng dừng và kết; kèm ảnh mở/kết cùng nguồn chỉnh sửa.

Kiểm xem-nghe ở kích thước điện thoại, chữ có dấu, biến hoa/thường, cỡ công thức, không che hình và không lộ mã. Vùng an toàn phải được đối chiếu theo nền tảng định phát hành. Không coi mẫu 24 giây là thời lượng chung; không tự chốt hai cue thành âm nhận diện. Nếu chưa có duyệt âm, giữ lựa chọn âm đã được giao trong sản phẩm.

## Điều hành

ChatGPT điều hành nhận bản quy chuẩn và báo cáo repo hiện tại; Copilot thực thi theo công việc có phạm vi. Trước khi soạn prompt giao việc riêng cho Copilot, xác nhận nội dung/phạm vi với chủ dự án nếu phiên điều hành video đang yêu cầu bước đó. Bộ này không tự tạo lệnh sửa repo video; không tự đồng bộ trạng thái giữa chat và repo.

Ghi profile đã nhận, commit nguồn, clip kết quả, kiểm đã chạy và phần còn thử vào hồ sơ tiếp nhận. Tài sản bản nhận ở repo video phải đủ để dựng độc lập, không phụ thuộc đường tuyệt đối sang E:\zo_math.
