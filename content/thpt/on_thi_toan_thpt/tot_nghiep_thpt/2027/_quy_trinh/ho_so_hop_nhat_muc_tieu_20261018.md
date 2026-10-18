# Hợp nhất mục tiêu và Câu hỏi dẫn đường — 18/10/2026

Chủ trì duyệt phương án và giao sửa nguồn bốn gói; chưa dựng HTML/PDF. Quy tắc sở hữu tại 07/6.1.4, không thay kiến trúc học tập.

## Nguồn đang lưu

- [Đơn điệu và cực trị](../../../hoc_lieu/r1_g01/index.qmd).
- [Giá trị lớn nhất và giá trị nhỏ nhất](../../../hoc_lieu/r1_g02/index.qmd).
- [Đường tiệm cận](../../../hoc_lieu/r1_g03/index.qmd).
- [Khảo sát sự biến thiên và vẽ đồ thị](../../../hoc_lieu/r1_g04/index.qmd).
- [Đối chiếu từng yêu cầu cũ, dòng hiện tại và bằng chứng](ho_so_hop_nhat_muc_tieu_20261018.json).

## Kết quả đối chiếu

| Gói | Bảng tại Bắt đầu | Yêu cầu cần chú ý khi hợp nhất |
|---|---|---|
| Đơn điệu và cực trị | Năm dòng mục tiêu hiện có | Hợp nhất danh sách Bắt đầu và bảng lặp, giữ điều kiện, nối biểu diễn, ba đối tượng cực trị, giới hạn dữ kiện, đánh giá/sửa/xác nhận. |
| Giá trị lớn nhất và nhỏ nhất | Năm dòng cốt lõi hiện có | Nhánh Chuyển giao giữ riêng ở Bắt đầu, với tiên quyết lượng giác/mũ/lôgarit và ghi rõ không là điều kiện hoàn tất lõi. Hợp nhất đủ tiên quyết từng nằm trong Định hướng. |
| Đường tiệm cận | Bảy dòng tổng hợp yêu cầu đã có | Giữ sáu yêu cầu ở Bắt đầu và nêu riêng đánh giá/sửa lập luận từ bảng cũ; giữ miền, hướng, dấu, hai đầu, không đếm trùng, kiểm hiệu, quan hệ với hình/giao điểm và đơn vị. Xác nhận sau sửa theo nhu cầu, không buộc đi qua Sửa lỗi. |
| Khảo sát sự biến thiên và vẽ đồ thị | Sáu dòng tổng hợp yêu cầu đã có | Tách hai họ phân thức cho dễ đọc, giữ rõ đối xứng từ mục tiêu Bắt đầu vốn không có trong bảng cũ; giữ trường hợp đạo hàm bằng không nhưng không cực trị, hai đầu/hướng nhánh, kiểm biểu diễn và miền/đơn vị mô hình. |

Số dòng phản ánh cách nhóm yêu cầu có sẵn, không thêm chủ đề hoặc định mức chung. Bảng đối chiếu máy đọc giữ toàn văn các mục tiêu Bắt đầu trước sửa, từng dòng bảng cũ, nơi được giữ và đích bằng chứng. Các bảng đọc kết quả/tiêu chí sau Kiểm tra được giữ nguyên, vì chúng có chức năng khác.

Ở đầu Bài học, khối mặc định đóng nay tên **Câu hỏi dẫn đường**, không chứa bảng hoặc nhãn cùng tên lặp trong thân. Chỉ dẫn cần khi thực hiện được giữ/chuyển về Cách học, không bị xóa cùng bảng. Mục lục tiếp tục sở hữu các liên kết tra mục. ID bảng và các điểm neo được giữ, kể cả tên ID cũ không còn là nhãn hiển thị.

## Nguồn đồng cấp và chống tái diễn

Đã đồng bộ bốn binding `he_nhan.json:learning_goals` (ID/tên dòng/đích bằng chứng), kiểu bảng chung và bản đồ nguồn G01. Bộ kiểm `zo_course_learning_goals.py` nối QMD/Quarto và cổng trước ghi HTML; không dùng binding sinh nội dung người học. Phép kiểm G02 từng buộc mục tiêu nằm trong Định hướng đã được thay; profile cũ được đánh dấu lịch sử và đường dựng G02 thiếu raw Quarto tươi bị từ chối.

G01 giữ nguyên fingerprint nguồn render và hash nghiệm thu lịch sử. Ràng buộc hiện hành ghi đúng QMD sau sửa, phép đảo chỉ phần di chuyển kiểm lại fingerprint cũ; văn bản lịch sử chỉ dùng so sánh, không đưa vào DOM/đầu ra. Ca âm tiếp tục bắt thay toán, chữ, ID ngoài phạm vi và mất nội dung mục tiêu. Mẫu bản thảo 1.2 và bảng kiểm 1.5 đã áp dụng quy tắc; không sửa hồi tố các bản thảo/receipt đã duyệt.

## Kiểm và giới hạn

- Cổng nguồn cả bốn QMD đạt; hồi quy mục tiêu 92/92; phép đảo/binding trên G01 thực trong bộ nhớ 3/3; tham chiếu đề–lời giải 58/58; điều hành 244/244.
- Phần nguồn từ Khởi động trở đi của cả bốn gói giữ nguyên; đa tập công thức LaTeX toàn nguồn không đổi. Biểu thức chỉ đổi vị trí cùng phần mục tiêu.
- Tất cả tệp đầu ra và Git index được bảo vệ theo `_audit/learning_goals_20261018/protected.json`, kết quả trong `final.json`: không đổi. Chưa dựng hình, HTML hoặc PDF; chưa commit/push/xuất bản.
- Bằng chứng `_audit/learning_goals_20261018`: bản trước sửa, coverage.json, source-complete.json, regression-complete.json, real-dom-inverse.json, answer-actions.json, governance-complete.json và final.json. Giữ các lần kiểm lỗi ban đầu làm lịch sử chẩn đoán, không dùng thay kết quả cuối.

Trạng thái: phương án đã được duyệt; nguồn đã cập nhật và kiểm kỹ thuật. [Bộ xem hiện có](http://127.0.0.1:8877/_audit/html_six_20261018/index.html) vẫn là bản trước lượt hợp nhất này; chưa có HTML mới để xem/duyệt bố cục.
