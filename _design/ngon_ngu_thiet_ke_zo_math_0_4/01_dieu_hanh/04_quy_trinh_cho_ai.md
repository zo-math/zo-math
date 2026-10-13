# Quy trình tác nghiệp cho AI

## Đường đọc tối thiểu

1. AGENTS.md của repo hiện tại, rồi AGENTS.md bộ này.
2. 03_du_lieu/bo_ban_giao.json; 09_nhat_ki/cong_viec_hien_tai.json.
3. 02_quy_chuan/00_tong_quan.md; các quy tắc liên quan trong 03_du_lieu/quy_tac.json.
4. Hướng dẫn đúng sản phẩm ở 04_ap_dung và mẫu tương ứng ở 07_mau_thi_giac.
5. Chỉ mở nguồn nghiên cứu khi cần giải thích, xác minh mâu thuẫn hoặc quyết định mới.

Các đường dẫn trong tài liệu này tính từ gốc bộ trừ khi ghi khác.

## 1. Tiếp nhận và xác minh

Ghi nhiệm vụ, đầu ra, phạm vi được giao và điều kiện hoàn thành. Đọc git status, nhánh/commit, AGENTS và các tệp nguồn thực sự liên quan. Phân biệt dữ liệu hiện tại ở repo với snapshot trong bộ này. Kiểm tra công việc đang có của người dùng; không checkout, reset, xóa hoặc ghi đè chúng để làm sạch repo.

Kiểm kê theo dependency: nơi khai báo token, style, template, nơi gọi chúng và sản phẩm được sinh. Không dựa vào tên file để gọi một thứ là master/canonical. Ghi các tệp ngoài phạm vi có thể bị ảnh hưởng nếu đổi tài nguyên chung.

## 2. Áp dụng

Dùng nguồn nội dung hiện tại của sản phẩm, không thay bằng nội dung R1-G01 mẫu cũ. Tách dữ liệu, vai trò và cách dựng. Lập phiên bản style mới khi thay style dùng chung có thể ảnh hưởng sản phẩm khác. Chỉ dùng cấu hình/tài sản thật đã có hoặc tạo và ghi rõ mới tạo; các hồ sơ JSON trong 03_du_lieu là đặc tả tích hợp, không phải plugin cài sẵn.

Bảo toàn toán: tập xác định, điều kiện, dấu, điểm loại, nhãn, ID và đáp án. Phân biệt ví dụ sai có chủ ý với lỗi sản xuất. Thay đổi kiến trúc học tập theo nhiệm vụ riêng, không lấy thay giao diện làm lí do tự đổi nội dung.

Nếu nhiệm vụ cho phép thử chi tiết candidate, dùng mẫu làm cơ sở và ghi trạng thái thử; không dừng chỉ vì mọi token chưa được duyệt cuối. Nếu cần chọn một quyết định mới ảnh hưởng phạm vi rộng, làm phần có thể xem được rồi nêu một khuyến nghị cụ thể để chủ dự án quyết định.

## 3. Kiểm

Chạy kiểm cần thiết theo sản phẩm, không dùng số lượng ca máy để chứng minh chất lượng. Kiểm trên sản phẩm đã render, ở kích thước thực. Với web, thử trình duyệt/màn hình nhỏ và hành vi; với video, xem-nghe bản xuất; với PDF, xem đầu/ruột/cuối và in hoặc xem theo cỡ thực. Không claim đã kiểm khi môi trường không hỗ trợ.

So sánh nguồn đầu-cuối. Chọn ít nhất một sản phẩm ngoài phạm vi dùng chung để kiểm ảnh hưởng nếu đã sửa thành phần shared. Chỉ mở rộng kiểm khi có rủi ro cụ thể, tránh thử lại toàn repo vô cớ.

## 4. Bàn giao và tiếp tục

Cập nhật 09_nhat_ki/cong_viec_hien_tai.json, lich_su.md và tiep_nhan_san_pham.json. Mỗi sản phẩm ghi phiên bản thiết kế đã nhận, commit, tệp bị đổi, mẫu/báo cáo, trạng thái kiểm và bằng chứng duyệt nếu có. Dùng mẫu 05_mau_bieu cho nhiệm vụ lớn; nhiệm vụ nhỏ dùng ghi chú ngắn đủ truy lại.

Một nhiệm vụ hoàn thành khi có đầu ra đúng phạm vi, kiểm phù hợp và hồ sơ tiếp tục; không phải chỉ khi đã viết kế hoạch. Không tự thêm bước xin phép cho hành động đã được giao. Không tự xuất bản, gửi thông điệp hay đổi toàn hệ ngoài phạm vi.

## Thứ tự giải quyết xung đột

Yêu cầu trực tiếp mới nhất của chủ dự án trong đúng phạm vi → yêu cầu/quyết định có căn cứ trong sổ → hướng dẫn áp dụng của sản phẩm → mẫu thử → nguồn lịch sử. Quy tắc repo về an toàn/quy trình vẫn phải được đọc và đối chiếu. Nếu có xung đột chưa giải được, trích đúng hai điều xung đột, nêu tác động và một cách xử lí đề nghị; không suy diễn thành đã được duyệt.

Nguồn lịch sử có câu “chưa được chọn màu”, “không thiết kế token” là giới hạn nhiệm vụ lúc đó. Phản hồi trực tiếp mới cho phép tạo mẫu màu/logo không nâng mọi phần của nghiên cứu cũ thành final, cũng không bị các giới hạn lịch sử vô hiệu hóa.
