# Quy tắc làm việc với agent trong repository ZO Math

## 1. Mục đích

Bộ quy tắc này điều hành cách agent khảo sát, sửa đổi và kiểm tra repository ZO Math.

Các quy tắc chuyên biệt về Quarto, giao diện, biên tập, TikZ, LaTeX, SVG, Manim, Git và xuất bản sẽ được đặt trong những tài liệu riêng. Agent chỉ đọc các tài liệu chuyên biệt phù hợp với nhiệm vụ đang thực hiện.

## 2. Thứ tự ưu tiên của nguồn chỉ dẫn

Áp dụng các nguồn theo thứ tự từ cao xuống thấp:

1. Yêu cầu hiện tại của người dùng trong nhiệm vụ đang làm.
2. `AGENTS.md` và các tài liệu được `AGENTS.md` tuyên bố là quy chuẩn hiện hành.
3. Quy tắc cục bộ của dự án con, chỉ trong phạm vi thư mục hoặc dự án đó.
4. Mã nguồn, cấu hình và script đang hoạt động, dùng làm bằng chứng về hiện trạng kỹ thuật nhưng không tự động trở thành quyết định thiết kế lâu dài.
5. Tài liệu không được `AGENTS.md` dẫn chiếu, chỉ dùng để tham khảo và đối chiếu.
6. Nội dung trong `_audit/` và các tệp có dấu hiệu như `before`, `preview`, `stage`, `tam`, `copy`, `_01`, mặc định được xem là lịch sử, thử nghiệm hoặc bản chụp; không dùng làm nguồn thực thi.

Khi hai nguồn cùng cấp mâu thuẫn và yêu cầu hiện tại không giải quyết được mâu thuẫn, agent phải dừng và hỏi người dùng. Không chọn theo ngày sửa tệp hoặc theo phỏng đoán.

## 3. Quy tắc áp dụng cho mọi nhiệm vụ

1. Làm việc bằng tiếng Việt.

2. Thực hiện đúng phạm vi được giao; không tự ý mở rộng nhiệm vụ.

3. Khi yêu cầu chưa đủ rõ hoặc các nguồn cùng cấp mâu thuẫn, phải dừng và hỏi người dùng, không tự suy đoán.

4. Trước thay đổi quan trọng, trình bày ngắn gọn phương án và chỉ thực hiện sau khi người dùng chốt. Khi yêu cầu hiện tại đã nêu rõ mục tiêu và cho phép thực hiện, yêu cầu đó được xem là sự chấp thuận; không hỏi lại một cách không cần thiết.

5. Không tự động commit, push, restore, xóa hoặc di chuyển tệp nếu người dùng chưa yêu cầu rõ.

6. Không chỉnh trực tiếp tệp đầu ra được sinh tự động khi đã xác định rõ nguồn sinh. Phải sửa nguồn dữ liệu hoặc script tương ứng rồi tái tạo đầu ra. Nếu chưa chắc một tệp có phải đầu ra tự động hay không, phải kiểm tra trước, không tự suy đoán.

7. Sau khi thay đổi, chạy các kiểm tra phù hợp với đúng loại nhiệm vụ và báo cáo kết quả cùng danh sách các tệp đã sửa.

8. Tệp tạm, bản chụp, script kiểm tra và báo cáo do agent tạo phải đặt trong `_audit/`, trừ khi nhiệm vụ quy định rõ nơi khác.

9. Khi có nhiều cách thực hiện, đề xuất một phương án tốt nhất; không đưa nhiều lựa chọn ngang hàng gây nhiễu.

10. Tuân thủ thứ tự ưu tiên của nguồn chỉ dẫn được quy định trong tài liệu này.

11. Trước khi chỉnh sửa, phải đọc các tệp liên quan, xác định hiện trạng thực tế, nguồn có thẩm quyền, quan hệ phụ thuộc và phạm vi ảnh hưởng. Không sửa chỉ dựa vào tên tệp, tài liệu cũ hoặc suy đoán.

12. Agent kỹ thuật không được tự thay đổi ý nghĩa toán học, lập luận, mục tiêu sư phạm, cấu trúc nhận thức hoặc giọng văn của nội dung, trừ khi nhiệm vụ yêu cầu rõ việc biên tập những phần đó.

13. Mỗi dữ liệu, quy tắc hoặc giá trị dùng chung nên có một nguồn chính thức. Không duy trì nhiều định nghĩa độc lập nếu chúng có thể dùng chung hoặc được sinh từ một nguồn duy nhất.

14. Ưu tiên đường dẫn tương đối và cấu hình có thể dùng trên máy khác. Không hard-code đường dẫn cá nhân hoặc phụ thuộc ngầm vào một máy tính, trừ khi đó là cấu hình cục bộ được tách riêng và ghi rõ.

15. Mỗi nhiệm vụ chỉ tạo những thay đổi cần thiết và có quan hệ trực tiếp với mục tiêu đã giao. Không tiện tay dọn dẹp, tái cấu trúc hoặc sửa lỗi lân cận. Diff phải đủ gọn để con người kiểm tra và có thể hoàn nguyên an toàn.

16. Trước khi tạo class, màu, component, cấu trúc trang hoặc quy ước mới, phải kiểm tra hệ thống hiện có và tái sử dụng thành phần phù hợp. Chỉ tạo ngoại lệ khi có lý do chức năng hoặc thiết kế rõ ràng.

## 4. Nguyên tắc nền tảng về giao diện

Các nguyên tắc trong mục này chỉ áp dụng khi nhiệm vụ tác động đến giao diện, bố cục, component, màu sắc, typography hoặc hành vi của trang.

### 4.1. Tổ chức khoa học và nhất quán hệ thống

Trang ZO Math phải được tổ chức khoa học và nhất quán ở mọi cấp độ, từ cấu trúc trang đến từng thành phần giao diện.

Một thành phần có cùng chức năng hoặc cùng vị trí trong hệ thống phải tuân theo cùng quy tắc về màu sắc, typography, khoảng cách, trạng thái và hành vi, trừ khi có lý do thiết kế rõ ràng để tạo ngoại lệ.

Một giá trị giao diện không được lựa chọn riêng cho từng trang theo cảm giác. Nếu màu, kiểu chữ, khoảng cách hoặc hành vi đã mang một ý nghĩa xác định trong hệ thống, ý nghĩa đó phải được giữ nhất quán ở những vị trí tương ứng trên các trang khác.

### 4.2. Tối giản có mục đích

Thiết kế ZO Math theo hướng tối giản có mục đích: loại bỏ sự dư thừa và nhiễu thị giác, nhưng giữ đầy đủ các chức năng, tín hiệu điều hướng và tiện ích cần thiết cho việc học, đọc và thao tác.

Không cắt bỏ tiện ích chỉ để tạo vẻ ngoài tối giản. Không theo đuổi sự trống rỗng hoặc giảm thiểu cực đoan làm suy yếu khả năng sử dụng, khả năng nhận biết cấu trúc hoặc trải nghiệm học tập.

## 5. Các quy trình và quy chuẩn chuyên biệt

Các lĩnh vực sau được điều hành bằng những tài liệu chuyên biệt thuộc hệ thống tài liệu xây dựng ZO Math:

- kiến trúc Quarto và các loại trang;
- hệ thống SCSS, CSS, màu sắc và typography;
- khối nội dung và lưới thẻ;
- phong cách biên tập và dấu câu;
- TikZ, LaTeX, pgfplots, SVG và font;
- Manim, Python và sản xuất video;
- Git, render, audit và xuất bản;
- Definition of Done theo từng loại nhiệm vụ.

Các nội dung trên sẽ được chuẩn hóa trong những tài liệu riêng trước khi tạo `AGENTS.md` chính thức.
