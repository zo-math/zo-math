# Quy chuẩn lưới thẻ trong repository ZO Math

## 1. Mục đích và phạm vi áp dụng

Tài liệu này quy định cách khảo sát, sửa đổi, tái sinh và kiểm tra hệ thống lưới thẻ trong repository ZO Math.

Quy chuẩn áp dụng cho nhiệm vụ liên quan đến dữ liệu thẻ, mã sinh, CSS dùng chung, partial, ảnh sinh tự động và trang sử dụng lưới thẻ. Các nhiệm vụ không liên quan đến lưới thẻ không thuộc phạm vi của tài liệu này.

## 2. Tính chất nội bộ

Đây là tài liệu điều hành nội bộ dành cho quá trình xây dựng repository. Đây không phải là nội dung xuất bản dành cho người đọc ZO Math.

Nội dung hiển thị trên thẻ vẫn là nội dung xuất bản. Agent không được tự thay đổi ý nghĩa, mục tiêu sư phạm hoặc giọng văn của nội dung đó nếu nhiệm vụ không cho phép biên tập.

## 3. Các thành phần của hệ thống

Hệ thống hiện hành của dự án `100_ham_so_su_bien_thien_va_do_thi` gồm:

- dữ liệu nguồn: `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_data/cards.yml`;
- mã sinh: `scripts/zo_build_card_grid.py`;
- CSS dùng chung: `assets/css/zo_card_grid.css`;
- partial sinh tự động: `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_partials/card_grid.qmd`;
- tài nguyên SVG sinh tự động: `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/assets/img/cards/`;
- trang sử dụng partial: `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/index.qmd`.

`cards.yml` chứa nội dung, trạng thái, liên kết, đường dẫn ảnh và cấu hình riêng của thẻ. Script đọc dữ liệu, sinh cấu trúc thẻ, sinh SVG và ghi các báo cáo audit mà nó hỗ trợ. CSS định nghĩa bố cục và hình thức dùng chung. Partial và SVG là đầu ra của quá trình sinh.

## 4. Nguyên tắc nguồn duy nhất

1. `cards.yml` và script là nguồn của partial và SVG được sinh tự động.
2. Không chỉnh trực tiếp partial hoặc SVG đã xác định là đầu ra tự động.
3. Thay đổi nội dung, trạng thái, liên kết hoặc cấu hình thẻ phải thực hiện trong `cards.yml`.
4. Thay đổi cấu trúc thẻ hoặc cách sinh ảnh phải thực hiện trong script.
5. Thay đổi giao diện dùng chung phải thực hiện trong CSS dùng chung sau khi đánh giá phạm vi hồi quy.
6. Đầu ra phải có thể tái sinh từ nguồn; không để logic lâu dài chỉ tồn tại trong partial hoặc SVG.

## 5. Hiện trạng giao diện đã xác minh

`assets/css/zo_card_grid.css` hiện quy định:

- lưới dùng `repeat(auto-fit, minmax(220px, 1fr))`, khoảng cách `1rem` và tự thích ứng theo chiều rộng;
- thẻ có chiều cao cơ sở `18.4rem`;
- ở chiều rộng tối đa `767.98px`, thẻ dùng chiều cao tự động và `min-height: 18.4rem`;
- vùng ảnh có chiều cao cố định `8rem`;
- nền vùng ảnh là gradient dùng `--bs-primary-rgb` và `--bs-secondary-rgb`;
- ảnh dùng `object-fit: cover` và hiệu ứng `drop-shadow`;
- trạng thái chờ chỉ giảm độ rõ của `.zo-card-body`, không làm mờ vùng ảnh;
- thẻ đã xuất bản có trạng thái tương tác khi hover;
- nút hành động của thẻ dùng nhãn do script sinh là `Đọc bài` hoặc `Đang chờ`.

Không suy rộng các giá trị trên thành quy chuẩn thiết kế bất biến. Khi CSS hoặc mã nguồn thay đổi có chủ đích, phải cập nhật tài liệu này trong cùng phạm vi công việc hoặc ghi nhận nhu cầu cập nhật.

## 6. Khảo sát trước khi sửa

Trước khi thay đổi hệ thống lưới thẻ, phải:

1. đọc trạng thái Git và tách các thay đổi ngoài phạm vi;
2. xác định trang sử dụng lưới, tệp dữ liệu, script, CSS, partial và thư mục ảnh liên quan;
3. xác định tệp nào là nguồn và tệp nào được sinh tự động;
4. đọc diff nguồn trước khi đánh giá diff đầu ra;
5. kiểm tra cách trang nạp CSS và chèn partial;
6. kiểm tra lệnh sinh từ entry point hoặc tài liệu hiện hành của repository;
7. đánh giá ảnh hưởng tới mọi trang đang dùng CSS hoặc cấu trúc thẻ bị sửa.

Không xác định hiện trạng chỉ từ tên tệp, thời gian sửa hoặc tài liệu lịch sử.

## 7. Thay đổi dữ liệu hoặc mã sinh

1. Giữ thay đổi trong phạm vi nhỏ nhất đáp ứng mục tiêu.
2. Đọc và kiểm tra diff của `cards.yml` hoặc script trước khi tái sinh.
3. Không dùng chỉnh sửa CSS toàn cục để che lỗi bắt nguồn từ dữ liệu, script hoặc một ảnh riêng.
4. Giữ UTF-8 và tránh thay đổi EOL hoặc định dạng toàn tệp ngoài ý muốn.
5. Nếu thêm định danh nội bộ, định danh phải ổn định và không phụ thuộc vào thứ tự hiển thị.
6. Không hiển thị mã kỹ thuật trên thẻ nếu thiết kế đã duyệt không yêu cầu.
7. Không thực hiện tái cấu trúc lớn hoặc tổng quát hóa hệ thống nếu nhiệm vụ chưa cho phép.

## 8. Tái sinh và kiểm tra tính quyết định

Với hệ thống hiện hành, lệnh sinh là:

```text
python scripts/zo_python.py scripts/zo_build_card_grid.py content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi
```

Trước khi chạy, phải ghi nhận các đầu ra dự kiến bị ghi lại. Khi cần kiểm tra tính quyết định, ghi nhận hàm băm của partial và SVG trước khi sinh, chạy trình sinh một lần, rồi so sánh hàm băm và diff sau khi sinh.

Nếu đầu ra thay đổi ngoài dự kiến, chỉ điều tra và sửa tại dữ liệu nguồn hoặc script, sau đó tái sinh. Không sửa đầu ra để làm khớp diff. Không chạy lặp lại nếu không có giả thuyết hoặc mục đích kiểm tra mới.

Script hiện ghi hai báo cáo vào `_audit/`: báo cáo tổng số thẻ theo trạng thái và báo cáo cấu hình renderer SVG. Không coi các báo cáo này là bằng chứng cho những kiểm tra mà chúng không thực hiện.

Kiểm tra chỉ đọc theo phạm vi lưới thẻ bằng lệnh:

```text
python scripts/zo_python.py scripts/zo_check_repo.py scope content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi
```

Lệnh kiểm định không thay thế việc tái sinh bằng `zo_build_card_grid.py` hoặc phép so sánh hàm băm trước và sau khi tái sinh.

## 9. Kiểm tra bắt buộc theo phạm vi

Chọn các kiểm tra phù hợp với thay đổi, tối thiểu gồm:

1. kiểm tra cú pháp Python khi script thay đổi;
2. phân tích YAML và xác nhận cấu trúc dữ liệu khi `cards.yml` thay đổi;
3. đối chiếu số thẻ hiển thị với dữ liệu nguồn;
4. xác nhận partial chỉ chứa thay đổi giải thích được từ nguồn;
5. xác nhận các ảnh và liên kết nội bộ được tham chiếu đều tồn tại;
6. phân tích SVG liên quan và xác nhận có nội dung đồ họa phù hợp;
7. chạy các script audit hiện hữu phù hợp và đọc đầy đủ kết quả;
8. kiểm tra các báo cáo do trình sinh ghi nhưng không tự suy rộng phạm vi của chúng;
9. chạy `git diff --check` cho phạm vi thay đổi;
10. render đúng trang sử dụng lưới thẻ khi thay đổi có thể ảnh hưởng đầu ra;
11. đọc mã thoát, lỗi và cảnh báo của render;
12. xác nhận partial được chèn, số thẻ đúng và tài nguyên được đưa vào đầu ra;
13. kiểm tra trực quan khi thay đổi tác động đến bố cục, responsive, màu sắc, typography hoặc hình ảnh.

Không render toàn bộ website nếu render trang liên quan đã đủ để kiểm tra. Không coi kiểm tra kỹ thuật là thay thế cho đánh giá trực quan khi giao diện thay đổi.

## 10. Stage và commit

1. Kiểm tra `git status --short` trước khi stage.
2. Stage bằng đường dẫn tường minh; không dùng `git add .` hoặc `git add -A`.
3. Liệt kê chính xác tệp staged.
4. Chạy `git diff --cached --check`.
5. Đọc toàn bộ `git diff --cached` và xác nhận chỉ có tệp thuộc phạm vi.
6. Không đưa tệp tạm, báo cáo ngoài phạm vi, đầu ra render hoặc thay đổi dang dở khác vào commit.
7. Chỉ commit khi nguồn, đầu ra và kiểm tra liên quan đều đạt.
8. Sau commit, xác nhận vùng staged trống và các thay đổi ngoài phạm vi còn nguyên.

## 11. Hiện trạng và hướng cải tiến

`scripts/zo_build_card_grid.py` hiện vừa sinh cấu trúc thẻ vừa chứa logic sinh SVG dành cho dự án hàm số. Đây là hiện trạng kỹ thuật, không phải kiến trúc tổng quát cho mọi loại dự án.

Việc tách phần sinh cấu trúc thẻ khỏi các bộ sinh ảnh theo loại nội dung có thể được xem xét trong tương lai. Đây chỉ là hướng cải tiến; không được mô tả như khả năng đã có hoặc tự thực hiện nếu chưa được giao và phê duyệt.
