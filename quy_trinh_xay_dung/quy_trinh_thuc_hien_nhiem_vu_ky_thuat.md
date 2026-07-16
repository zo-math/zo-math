# Quy trình thực hiện nhiệm vụ kỹ thuật trong repository ZO Math
## 1. Mục đích

Quy trình này quy định cách agent tiếp nhận và thực hiện trọn vẹn một nhiệm vụ kỹ thuật trong repository ZO Math.

Mục tiêu là để người dùng tập trung vào nội dung, tư duy toán học, sư phạm và quyết định thiết kế; agent chịu trách nhiệm thực hiện các thao tác kỹ thuật trong VS Code và repository.

Agent phải tự đọc tệp, chỉnh sửa mã, chạy lệnh, đọc kết quả, xử lý lỗi trong phạm vi được giao và báo cáo kết quả. Không yêu cầu người dùng sao chép lệnh sang Terminal hoặc chuyển kết quả Terminal trở lại cuộc trò chuyện, trừ khi agent thực sự bị chặn bởi quyền hệ thống, thao tác bên ngoài VS Code hoặc một quyết định chỉ người dùng mới có thể đưa ra.

## 2. Tiếp nhận nhiệm vụ

Khi nhận nhiệm vụ, agent phải:

1. Đọc `AGENTS.md` và các tài liệu hiện hành được dẫn chiếu phù hợp với phạm vi công việc.
2. Xác định mục tiêu, phạm vi, tệp liên quan và kết quả cần đạt.
3. Phân biệt rõ:
   - nội dung ZO Math dành cho người đọc;
   - mã nguồn, tài sản và tài liệu nội bộ phục vụ xây dựng ZO Math.
4. Kiểm tra hiện trạng thực tế trước khi đề xuất hoặc thực hiện thay đổi.
5. Xác định nguồn chính thức, tệp đầu ra tự động, quan hệ phụ thuộc và phạm vi ảnh hưởng.
6. Không tự mở rộng nhiệm vụ sang các lỗi hoặc khu vực lân cận.

Nếu yêu cầu đã rõ mục tiêu, phạm vi và cho phép thực hiện, agent phải bắt đầu công việc mà không hỏi lại một cách không cần thiết.

Agent chỉ dừng để hỏi khi:

- thiếu một quyết định về nội dung, toán học, sư phạm hoặc thiết kế;
- có hai nguồn chỉ dẫn cùng cấp mâu thuẫn;
- thao tác có nguy cơ phá hủy dữ liệu hoặc vượt phạm vi đã giao;
- không thể xác định chắc chắn nguồn cần sửa;
- kết quả có nhiều cách hiểu và không thể chọn một phương án tốt nhất từ các quy tắc hiện hành.

## 3. Khảo sát trước khi sửa

Trước khi thay đổi tệp, agent phải khảo sát đủ để trả lời:

- Tệp nào là nguồn cần sửa?
- Tệp nào được sinh tự động?
- Thành phần này đang được cấu hình hoặc nạp từ đâu?
- Có quy tắc, token, class, helper, script hoặc component hiện có để tái sử dụng không?
- Thay đổi có thể ảnh hưởng đến những trang, đầu ra hoặc công cụ nào?
- Repository hiện có những thay đổi chưa commit nào cần tránh đụng vào?

Agent được tự chạy các lệnh chỉ đọc cần thiết để khảo sát.

Không coi ngày sửa tệp, tên tệp hoặc tài liệu cũ là bằng chứng đủ để xác định nguồn có thẩm quyền.

## 4. Trình bày phương án

Trước thay đổi quan trọng, agent phải trình bày ngắn gọn:

- nguyên nhân hoặc hiện trạng đã xác định;
- tệp dự kiến sửa;
- cách thực hiện;
- phạm vi ảnh hưởng;
- cách kiểm tra sau khi sửa.

Chỉ trình bày một phương án tốt nhất.

Không cần trình bày lại phương án đối với thao tác nhỏ, hiển nhiên và đã được yêu cầu trực tiếp, miễn là thao tác đó không làm thay đổi nội dung, kiến trúc hoặc thiết kế đã được chốt.

## 5. Thực hiện thay đổi

Trong quá trình thực hiện, agent phải:

1. Chỉ sửa những tệp cần thiết cho mục tiêu.
2. Giữ diff nhỏ, rõ và có thể kiểm tra.
3. Không tiện tay dọn dẹp, đổi định dạng, tái cấu trúc hoặc sửa lỗi ngoài phạm vi.
4. Không chỉnh trực tiếp đầu ra tự động khi đã xác định được nguồn sinh.
5. Tái sử dụng hệ thống hiện có trước khi tạo class, component, màu, helper, script hoặc quy ước mới.
6. Không tự thay đổi ý nghĩa toán học, lập luận, mục tiêu sư phạm, cấu trúc nhận thức hoặc giọng văn.
7. Đặt tệp tạm, bản chụp, script kiểm tra và báo cáo phát sinh trong `_audit/`, trừ khi nhiệm vụ quy định nơi khác.
8. Ưu tiên đường dẫn tương đối và cấu hình có thể dùng trên máy khác.
9. Không tự động commit, push, restore, xóa hoặc di chuyển tệp nếu chưa được người dùng yêu cầu rõ.

### Chạy lệnh Python

Lệnh Python trong quy trình kỹ thuật phải đi qua trình khởi chạy repository-local. Cú pháp chuẩn là:

```text
python scripts/zo_python.py script.py [tham số...]
python scripts/zo_python.py -m module [tham số...]
```

Khi đã dùng trình khởi chạy, không thêm thủ công `PYTHONUTF8=1` vào từng lệnh. Trình khởi chạy chỉ bảo đảm chế độ UTF-8 cho tiến trình Python con; nó không thay đổi logic hoặc dữ liệu của script đích. Báo cáo kết quả phải ghi đúng lệnh thực tế đã dùng.

### Kiểm định kỹ thuật thống nhất

Dùng điểm vào `scripts/zo_check_repo.py` theo nguyên tắc:

- `quick` kiểm tra nhanh các tệp đang thay đổi hoặc phạm vi nhỏ được chỉ định, không render;
- `scope` kiểm tra một hoặc nhiều tệp, thư mục tường minh bằng validator phù hợp;
- `render` chỉ dùng khi nhiệm vụ cần render các trang `.qmd` tường minh;
- `--staged` chỉ dùng khi cần kiểm tra vùng staged;
- `--report` chỉ dùng khi báo cáo JSON máy đọc được trong `_audit/` thực sự hữu ích.

Ví dụ lệnh:

```text
python scripts/zo_python.py scripts/zo_check_repo.py quick
python scripts/zo_python.py scripts/zo_check_repo.py scope scripts/zo_python.py
python scripts/zo_python.py scripts/zo_check_repo.py render content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/index.qmd
```

Công cụ kiểm định không tự sửa lỗi, stage hoặc commit. Trước commit, agent vẫn phải đọc diff, xác nhận phạm vi Git và thực hiện các kiểm tra staged phù hợp.

Agent chịu trách nhiệm tự chạy các lệnh kỹ thuật cần thiết. Không chuyển việc vận hành Terminal cho người dùng chỉ vì thao tác đó có thể được thực hiện bằng lệnh.

## 6. Xử lý lỗi trong quá trình làm việc

Khi lệnh hoặc kiểm tra thất bại, agent phải:

1. Đọc đầy đủ thông báo lỗi.
2. Xác định lỗi có thuộc phạm vi nhiệm vụ hay không.
3. Nếu thuộc phạm vi, tự sửa và chạy lại kiểm tra.
4. Nếu không thuộc phạm vi, không tự sửa; ghi nhận rõ trong báo cáo.
5. Không che giấu cảnh báo hoặc coi lệnh thành công khi chưa kiểm tra mã thoát và đầu ra cần thiết.
6. Không lặp lại cùng một thao tác thất bại mà không thay đổi giả thuyết hoặc cách xử lý.

Khi cần chạy lệnh ngoài sandbox hoặc cần người dùng phê duyệt, agent phải nêu rõ:

- lệnh sẽ chạy;
- mục đích;
- thao tác chỉ đọc hay có ghi dữ liệu;
- phạm vi ảnh hưởng;
- lý do cần vượt giới hạn hiện tại.

## 7. Kiểm tra sau thay đổi

Agent phải chọn kiểm tra phù hợp với loại nhiệm vụ, không chạy máy móc mọi kiểm tra của toàn repository.

Tối thiểu phải xác nhận:

1. Tệp yêu cầu đã được sửa đúng.
2. Không có tệp ngoài phạm vi bị thay đổi.
3. Cú pháp hoặc cấu trúc liên quan hợp lệ.
4. Lệnh build, render, compile hoặc script mục tiêu hoàn thành, nếu nhiệm vụ cần.
5. Các cảnh báo và lỗi đã được đọc.
6. Đầu ra được sinh từ nguồn đã đồng bộ, nếu có.
7. Diff không chứa thay đổi ngoài ý muốn, tàn dư lệnh, lỗi EOL hoặc khoảng trắng đáng chú ý.
8. Kết quả đáp ứng mục tiêu đã giao.

Khi nhiệm vụ tác động đến giao diện, kiểm tra kỹ thuật không thay thế cho đánh giá trực quan. Agent phải xác định trang hoặc đầu ra cần người dùng xem và mô tả rõ nội dung cần duyệt.

## 8. Điều kiện hoàn thành nhiệm vụ

Một nhiệm vụ kỹ thuật chỉ được xem là hoàn thành khi:

- mục tiêu đã được thực hiện trong đúng phạm vi;
- các kiểm tra phù hợp đã chạy;
- lỗi thuộc phạm vi đã được xử lý;
- các giới hạn hoặc vấn đề còn lại đã được nêu rõ;
- không có thay đổi ngoài ý muốn;
- người dùng nhận được báo cáo đủ để đánh giá mà không phải tự khảo sát lại repository.

Agent không được tuyên bố hoàn thành chỉ vì đã sửa mã. Việc kiểm tra là một phần của nhiệm vụ.

## 9. Báo cáo kết quả

Báo cáo cuối nhiệm vụ phải ngắn gọn và gồm:

### Kết quả

Mô tả điều đã thực hiện và trạng thái đạt được.

### Tệp đã thay đổi

Liệt kê chính xác các tệp được tạo, sửa, xóa hoặc tái sinh.

### Kiểm tra đã chạy

Liệt kê các lệnh hoặc kiểm tra quan trọng và kết quả của chúng.

### Nội dung cần người dùng duyệt

Chỉ nêu những quyết định, đánh giá trực quan hoặc vấn đề mà agent không thể tự kết luận.

### Giới hạn còn lại

Nêu rõ lỗi, cảnh báo hoặc vấn đề chưa xử lý, nếu có. Không tạo mục này khi không còn giới hạn đáng kể.

Không kể lại toàn bộ quá trình suy luận nội bộ và không đưa một danh sách dài các khả năng không cần thiết.

## 10. Những việc agent không chuyển lại cho người dùng

Trong điều kiện VS Code, repository và công cụ đang hoạt động bình thường, agent không được yêu cầu người dùng:

- tự tìm tệp liên quan;
- tự chép và chạy lệnh Terminal;
- tự gửi lại log mà agent có thể đọc;
- tự kiểm tra Git status hoặc diff;
- tự tạo tệp audit;
- tự sửa những lỗi kỹ thuật thuộc phạm vi đã giao;
- tự lặp lại các bước mà agent có thể thực hiện trực tiếp.

Người dùng giữ quyền quyết định về:

- nội dung và ý nghĩa toán học;
- mục tiêu sư phạm;
- cấu trúc nhận thức;
- nguyên tắc và ngoại lệ thiết kế;
- đánh giá thẩm mỹ;
- commit, push, xuất bản hoặc thao tác phá hủy khi chưa được ủy quyền.
