# Ảnh bìa, thẻ và ảnh thu nhỏ

Nơi làm việc theo thông tin đã có: `E:/zo_media/on_thi_toan_thpt_2027/00_dung_chung/ZO_Math_Cong_cu_tao_anh_video`. Trạng thái repo hiện tại: **cần AI tại máy xác minh**.

Quy tắc liên quan: ZO001, ZO003, ZO019, ZO020, ZO029.

## Xác minh đầu vào

Đường dẫn do chủ dự án cung cấp; bộ này không chứa đầy đủ mã hiện tại của công cụ. AI tại máy phải đọc entry point, định dạng dữ liệu, template, font, vị trí asset và quy trình xuất. Không mặc định công cụ này là zo_build_card_grid.py của website: chúng có thể là hai công cụ khác nhau.

## Cách tích hợp

Thêm bộ template 0.4 vào cơ chế hiện có, dùng logo/màu/font cùng phiên bản với video. Giữ dữ liệu nội dung tách khỏi bố cục: mã bài, tiêu đề, câu hỏi, công thức/hình, CTA. Tài nguyên tham khảo trong social và design/distribution.json của mẫu, gồm cả hệ 0.2 được giữ để đối chiếu.

Mỗi tỉ lệ cần dàn lại: dọc, ngang, thumbnail, ảnh chia sẻ. Không kéo giãn/crop tự động một bố cục rồi gọi là thiết kế hoàn tất. Bìa trước đặt chủ đề/câu hỏi; bìa sau kết/dẫn hành động theo nội dung; ảnh thu nhỏ cần đọc ở cỡ nhỏ.

## Kiểm và đầu ra

Dựng cùng một nội dung ở các đầu ra mà công cụ hiện cung cấp và nhiệm vụ yêu cầu; thử tiêu đề ngắn/dài, nhiều dấu tiếng Việt, có/không hình. Kiểm vùng crop/nút nền tảng, logo, font, cỡ chữ và công thức. Xuất nguồn template, dữ liệu mẫu, ảnh đã dựng và phiên bản profile. Giữ template cũ để sản phẩm đang làm không tự đổi.
