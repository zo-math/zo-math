# Rà điều hướng tới–về — nguồn sáu trang, 18/10/2026

Phạm vi: Nhà khóa học, Khảo sát đầu vào, Đơn điệu và cực trị, Giá trị lớn nhất và giá trị nhỏ nhất, Đường tiệm cận, Khảo sát sự biến thiên và vẽ đồ thị của hàm số. Chỉ sửa nguồn theo yêu cầu; không dựng HTML/PDF, không commit/push/xuất bản.

| Thành phần | Kết quả rà và xử lí |
|---|---|
| Mục lục toàn khóa và Quarto sidebar | Đã đủ sáu trang từ NAV-G04-01; giữ nguyên. Cổng nay kiểm tệp/neo đích trên cả sáu trang. |
| Khảo sát đầu vào | Danh sách học liệu còn thiếu hai bài mới: đã thêm. Drawer mobile chưa nhận cùng thao tác đóng hộp/focus đích như Nhà: đã nối vào handler dùng chung. |
| Các vùng học, hỗ trợ và tiện ích của bốn bài | Đối chiếu nguồn và bộ điều khiển; giữ ba nhóm và các điểm vào tự chọn. Không thêm nút tuần tự bắt buộc. G04 chưa có PDF nên không tạo mục tải rỗng. |
| Cặp đề–lời giải | Kiểm theo binding và nhãn “Xem lời giải”/“Xem đề bài”. Các câu xác nhận có lời giải ngay trong thẻ giữ đối chiếu tại chỗ; Kiểm tra dùng đích nhóm sau khi kết thúc lượt. Không thêm liên kết nhảy thừa vì chỉ đếm thiếu một href riêng. |
| Ôn nền/Nhật kí liên học liệu | Mười một liên kết G03/G04 có mốc về dự phòng trong nguồn. Controller lấy đúng caller/Điểm dừng nếu đã có và mang trong URL; giữ caller qua các tài nguyên hỗ trợ kế tiếp và đối chiếu lời giải. G02 không ghi đè thanh quay về ngoại gói. Liên kết Nhật kí G04 dùng đúng view nhat-ky. |
| Nhà khóa học | Danh mục thẻ theo dữ liệu phát hành giữ nguyên; menu toàn khóa đã có G04. Không dùng lượt sửa điều hướng để đổi G04 thành đã xuất bản. |

Nguyên nhân thiếu: kiểm trước chủ yếu bao phủ menu toàn khóa và đường đi trong cùng bài; danh sách D0 là nguồn riêng, handler drawer chỉ chọn .home-nav, controller bỏ qua liên kết khác pathname, nhánh hỗ trợ riêng G02 dựng lại thanh quay về theo đích nội trang. Đã sửa cả các điểm sinh và phạm vi kiểm.

Nguồn sửa: D0/index.qmd, G03/index.qmd, G04/index.qmd; _design/web_2027_mau_dung_chung/r1-controller.js và site-ui.js; G02/giao_dien/support-context.js; scripts/zo_web_2027_navigation.py và zo_web_2027_navigation_check.py. Bộ fixture tái sử dụng tại scripts/zo_course_navigation_routes_selftest.js. Quy tắc/quy trình/trạng thái cập nhật ở 07, 02 và 03 cùng thư mục này. Các sửa nguồn chưa commit từ các lượt trước được giữ.

Kiểm đã thực hiện:

- Cổng nguồn điều hướng: 1362/1362, gồm mục lục, neo liên kết Markdown/HTML trong sáu nguồn mở rộng include và điểm về liên học liệu.
- Fixture JavaScript trong bộ nhớ: 24/24; caller từ Ôn lại, điểm về trực tiếp, qua hai tài nguyên hỗ trợ, URL để tải lại/tab độc lập, các kiểu mở liên kết và handler drawer Nhà/D0. Đây không phải phép kiểm trình duyệt thật.
- Thử âm nguồn: 5/5; chặn thiếu/sai trang về, sai mốc caller, sai neo cục bộ và thiếu G04 trong D0.
- Hồi quy nhãn đề–lời giải: 46/46; 356 thao tác nguồn của bốn bài.
- Cổng QMD: D0, G03, G04 đạt. Biểu thức toán và ID của ba nguồn đối chiếu trước/sau: 6/6 không đổi. Kiểm cú pháp Python/JavaScript và diff đạt.
- Tệp HTML/PDF/SVG/TEX, bản thảo, khai báo ảnh bìa và bằng chứng duyệt trong danh mục bảo toàn trước đó được đối chiếu hash, không đổi; xem qa-preservation.json trong hồ sơ audit.

Bằng chứng nguồn lưu tại E:/zo_math/_audit/navigation_sources_20261018/: inventory-before.json, before/, qa-source.json, qa-routes.json, qa-negative.json, qa-qmd.json, qa-answer-actions.json và qa-preservation.json.

Chưa hoàn tất: dựng HTML theo nguồn mới và kiểm click/Back/tải lại/mở tab/bàn phím trên các trang thật ở desktop/mobile; chưa có duyệt hiển thị mới. Bản xem cũ http://127.0.0.1:8877/_audit/r1_consistency_20261018/index.html vẫn là trước các lượt sửa nguồn; không dùng nó để xác nhận các sửa lần này. Không dựng lại PDF hoặc xuất bản.
