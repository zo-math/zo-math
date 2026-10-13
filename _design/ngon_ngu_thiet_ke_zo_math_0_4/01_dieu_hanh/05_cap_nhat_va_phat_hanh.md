# Cập nhật, phát hành và hoàn tác

## Hai phiên bản khác nhau

Mẫu thị giác hiện tại là 0.4. Bộ bàn giao hiện tại là 0.4.2. Không gọi bộ này Design System 1.0. Khi sửa chỉ dẫn/lỗi bàn giao mà không đổi thiết kế, tăng phiên bản bộ bàn giao. Khi đổi mẫu/thiết kế, ghi phiên bản thiết kế mới cùng bản đồ thay đổi.

## Một thay đổi đi qua đâu?

1. Thêm căn cứ vào bản ghi yêu cầu/nguồn, không sửa lời cũ để làm giống quyết định mới.
2. Thêm hoặc cập nhật quy tắc đúng phạm vi; đánh dấu quy tắc bị thay thế, giữ lịch sử.
3. Cập nhật tài sản/cấu hình và mẫu liên quan. Nếu có khác biệt theo phương tiện, ghi điều bất biến và điều thay đổi.
4. Kiểm đầu ra, ghi kết quả và phê duyệt thực sự nhận được.
5. Tạo bản phát hành mới; ghi repo/sản phẩm nào đã nhận, repo nào vẫn ở bản cũ.

03_du_lieu/color_system.json là nguồn giá trị màu của bộ áp dụng. Bản trong 07_mau_thi_giac là snapshot 0.4 để đối chiếu, không phải bản thứ hai được sửa độc lập. Cấu hình CSS/TeX/Python sản xuất nên được sinh/đối chiếu từ dữ liệu gốc; chưa có bộ sinh đa engine sản xuất trong bàn giao này.

## Lưu và hoàn tác

Giữ commit trước khi áp dụng; chỉ stage tệp liên quan khi được phép commit, không dùng git add . Nếu working tree có việc đang làm, thống nhất điểm lưu với chủ dự án thay vì reset. Ghi cách chọn lại style/cấu hình trước; không sửa ngược các đầu ra để giả lập rollback.

Không auto-update mọi repo khi bản gốc đổi. Repo đích nhận một bản xác định có hash/phiên bản và ca kiểm. Như vậy một thay đổi màu/spacing chưa kiểm sẽ không tự lan vào video đang sản xuất.

## Kiểm tính nguyên vẹn

Từ gốc bộ: `python 08_cong_cu/zo_design.py check`. Công cụ chỉ đọc, dùng thư viện chuẩn Python. Nó kiểm tài liệu điều hành, tài nguyên tham chiếu, dữ liệu và manifest; không chứng nhận mỹ thuật hay quyền duyệt.

Các thư mục 09_nhat_ki và _audit dành cho vận hành, có thể thay đổi. Sau khi chủ động sửa quy chuẩn, manifest bản phát hành cũ sẽ báo khác biệt. Tạo bản phát hành và manifest mới sau kiểm/duyệt; không xóa báo lỗi bằng cách đổi hash âm thầm. Giữ bản ZIP phát hành trước.
