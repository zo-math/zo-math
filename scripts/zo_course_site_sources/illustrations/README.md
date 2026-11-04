# Minh họa chuyên đề đã duyệt

Nguồn ảnh thuộc từng gói tại `content/thpt/on_thi_toan_thpt/hoc_lieu/<ma_goi>/hinh/minh_hoa_chuyen_de_vN/`, không thuộc thư mục mã giao diện này. Danh mục duy nhất chọn phiên bản hiện hành là `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_data/minh_hoa_chuyen_de.json`.

Mỗi bộ có `originals/` giữ ảnh đã duyệt nguyên byte, `manifest.json` ghi approval/nguồn/hash và năm PNG 1:1, 3:4, 4:3, 9:16, 16:9. `scripts/zo_topic_art.py build/check` xuất/kiểm các cỡ từ nguồn đã khai báo, giữ riêng trạng thái nguồn đã duyệt và bố cục chờ duyệt; bản thân công cụ xuất không vẽ lại. Website kiểm hash và trạng thái duyệt, chép ảnh gốc vào `docs/assets/course_site_2027/illustrations/<ma_goi>.png`; tệp docs là bản sinh, không sửa tay.

Thêm chuyên đề tiếp theo: chốt nội dung và ảnh trong chat trước; tạo thư mục phiên bản thật đang dùng trong `hinh/` của gói; lưu ảnh gốc/provenance/approval; đăng ký đường dẫn manifest trong danh mục; chạy build/check bộ ảnh; cập nhật HTML đúng phạm vi rồi xem trực tiếp. Không tạo ảnh, approval hoặc thư mục gói tương lai trước khi có yêu cầu. Không suy duyệt mới từ ảnh gói khác.

Ngôn ngữ đã chốt: đường cong trơn và điểm tròn đúng hình; đỏ ZO cho đường cong/viền điểm, vàng ZO cho điểm trọng tâm, xám nâu cho điểm phụ/chữ; nền trong suốt. Ý tưởng phải lấy từ vấn đề đặc thù của chuyên đề. Không thay hình thành dải/ribbon, không méo hình học. Mã màu tham chiếu trong danh mục; không coi PNG sinh ảnh là bản khóa RGB tuyệt đối.

Đổi hình, màu hoặc bố cục: tạo phiên bản mới, trình riêng rồi mới chuyển binding. Các tỉ lệ 1:1, 3:4, 4:3, 9:16 được bố trí lại riêng bằng công cụ tạo ảnh, lưu nguồn trong `candidates/` và ghi `pending_owner_review` ở từng nguồn/bản xuất. Bản 16:9 giữ bố cục đã duyệt. Công cụ xuất chỉ chuẩn hóa tỉ lệ chính xác bằng fit đồng dạng, không cắt/méo/phóng lớn. Các bố cục mới không tự kế thừa duyệt của ảnh gốc. Nghiệm thu ảnh không tự cho phép commit, push, thay bìa PDF hoặc xuất bản.


## Bố cục G04 và kiểm đúng tiệm cận

Bốn bố cục mới của G04 lấy nguồn từ `scripts/zo_topic_art_g04.py`, dùng cùng phép đổi tọa độ cho công thức và tiệm cận; PNG/SVG trong `candidates/` được ghi là `formula_based_native_geometry`. Bản AI vẽ sai phía tiệm cận bị loại khỏi bộ nguồn sử dụng. Giữ ảnh gốc đã chốt nguyên byte, tách duyệt bố cục mới khỏi kiểm đúng toán. Không tự vẽ lại đường tiệm cận theo góc khác với phép đổi tọa độ áp lên đường cong.
