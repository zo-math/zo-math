# Hợp đồng giữa lõi, dự án, hồ sơ và QMD

> **Trạng thái:** Bản thiết kế v1.0 — Giai đoạn 1.

## 1. Mục đích

Tài liệu này xác định trách nhiệm và ranh giới giữa:

- lõi sản xuất QMD;
- cấu hình dự án;
- quy chuẩn chuyên biệt;
- hồ sơ sản xuất của bài;
- QMD và đầu ra;
- checker;
- người nghiệm thu.

## 2. Nguyên tắc hợp đồng

Mỗi tầng phải trả lời một loại câu hỏi khác nhau:

| Tầng | Câu hỏi chính |
|---|---|
| Lõi | Mọi bài QMD của ZO Math phải bảo đảm điều gì? |
| Dự án | Dự án này thêm những yêu cầu nào và tổ chức bài ở đâu? |
| Quy chuẩn chuyên biệt | Nội dung chuyên môn phải được xây dựng và kiểm định ra sao? |
| Hồ sơ bài | Bài cụ thể này chọn gì, không áp dụng gì và đã có bằng chứng nào? |
| QMD | Sản phẩm nguồn hiện thực hóa các quyết định như thế nào? |
| Checker | Các điều kiện mã hóa được có đạt không? |
| Người nghiệm thu | Nội dung, nhận thức và đầu ra thật có đạt không? |

## 3. Hợp đồng của lõi

Lõi có trách nhiệm:

- định nghĩa vòng đời bài;
- định nghĩa metadata nền;
- định nghĩa cấu trúc hồ sơ nền;
- định nghĩa trạng thái sản xuất và xuất bản;
- định nghĩa kiểm định nguồn, HTML và PDF;
- định nghĩa cách ghi bằng chứng;
- định nghĩa cổng nghiệm thu và xuất bản;
- cung cấp registry mô-đun;
- giữ giao diện checker.

Lõi không được:

- áp đặt kiến trúc nội dung của một dự án;
- chứa đường dẫn riêng của dự án;
- yêu cầu trường chuyên môn không áp dụng;
- tự quyết định xuất bản;
- cho phép dự án vô hiệu hóa bất biến an toàn.

## 4. Hợp đồng của cấu hình dự án

Cấu hình dự án phải khai báo tối thiểu:

- `schema_version`;
- `project_id`;
- `project_name`;
- `project_root`;
- `article_types`;
- `profile`;
- `modules`;
- `metadata`;
- `publication`;
- `references`;
- `regression`.

Cấu hình có thể:

- thêm metadata bắt buộc;
- khai báo mẫu đường dẫn;
- kích hoạt mô-đun;
- khai báo dữ liệu danh mục;
- khai báo lớp trang;
- khai báo cách ánh xạ trạng thái;
- chỉ định đường cơ sở hồi quy.

Cấu hình không được:

- chỉ định hàm Python tùy ý;
- tắt kiểm tra an toàn của lõi;
- tự sửa QMD;
- tự chuyển `published`;
- khai báo đường dẫn ra ngoài repository;
- ghi đè tài liệu cấp cao hơn.

## 5. Hợp đồng của quy chuẩn chuyên biệt

Quy chuẩn chuyên biệt chịu trách nhiệm về:

- đơn vị nội dung;
- phương pháp khảo sát hoặc mô hình hóa;
- cấu trúc nhận thức;
- tiêu chuẩn lập luận;
- biểu diễn chuyên môn;
- tiêu chí kiểm định nội dung;
- điều kiện dừng chuyên môn.

Quy chuẩn chuyên biệt phải được cấu hình dự án dẫn chiếu rõ. Một tệp tồn tại trong repository không tự động có hiệu lực.

## 6. Hợp đồng của hồ sơ bài

Hồ sơ bài phải:

- nhận diện bài và loại bài;
- ghi phạm vi được sửa;
- ghi tài liệu điều khiển đã dùng;
- ghi quyết định và ngoại lệ;
- ghi tài nguyên;
- ghi bằng chứng kiểm định;
- ghi kết quả nghiệm thu;
- ghi trạng thái sản xuất;
- ghi trạng thái xuất bản;
- ghi các vấn đề còn lại;
- ghi sản phẩm bàn giao.

Hồ sơ không được:

- thay thế quy chuẩn;
- tự cho phép bỏ qua kiểm tra bắt buộc;
- dùng `không áp dụng` mà không có lí do;
- chứa đường dẫn cá nhân hoặc máy cụ thể;
- tự chuyển bài sang công khai.

## 7. Hợp đồng của QMD

QMD phải:

- thỏa metadata hiệu lực;
- hiện thực đúng quyết định trong hồ sơ;
- tham chiếu tài nguyên hợp lệ;
- không chứa placeholder;
- không chứa thao tác mã bị cấm;
- không dùng cấu trúc bị dự án cấm;
- render được khi giai đoạn yêu cầu;
- tạo đầu ra phù hợp với trạng thái.

QMD không được:

- tự định nghĩa quy tắc kiểm định;
- tự tắt validator;
- dùng metadata để vượt cổng xuất bản;
- thay thế hồ sơ sản xuất.

## 8. Hợp đồng của checker

Checker phải:

- nhận diện đúng dự án;
- nạp cấu hình một cách xác định;
- từ chối cấu hình không hợp lệ;
- tạo hợp đồng hiệu lực;
- chạy validator lõi;
- chạy đúng mô-đun đã đăng kí;
- chạy validator dự án;
- phân biệt `PASS`, `WARN`, `FAIL`, `INFO`;
- giữ mã thoát nhất quán;
- tạo báo cáo có thể đọc bằng máy;
- không tự sửa tệp;
- không stage, commit hoặc xuất bản.

Checker không được tuyên bố nghiệm thu nội dung cuối cùng.

## 9. Hợp đồng của người nghiệm thu

Người nghiệm thu quyết định:

- tính đúng toán học;
- chất lượng lập luận;
- giá trị nhận thức;
- chất lượng sư phạm;
- tính phù hợp của hình;
- trải nghiệm HTML/PDF;
- ngoại lệ thiết kế;
- nghiệm thu cuối;
- xuất bản.

## 10. Hợp đồng hiệu lực

Checker tạo hợp đồng hiệu lực theo thứ tự:

```text
bất biến lõi
+ yêu cầu dự án
+ mô-đun được kích hoạt
+ lựa chọn hợp lệ trong hồ sơ
= hợp đồng hiệu lực của bài
```

Metadata QMD và đầu ra được kiểm tra theo hợp đồng này.

## 11. Xung đột

Khi có xung đột:

1. dừng kiểm tra chuyên biệt của bài;
2. báo rõ hai nguồn và trường xung đột;
3. không âm thầm chọn một bên;
4. không sửa nguồn điều khiển;
5. yêu cầu quyết định của người dùng khi không thể giải bằng thứ tự thẩm quyền.

## 12. Không áp dụng

Một kiểm tra chỉ được đánh dấu `không áp dụng` khi:

- lõi hoặc mô-đun cho phép;
- hồ sơ ghi lí do;
- checker xác nhận điều kiện;
- việc bỏ qua không làm mất bất biến an toàn.

## 13. Tương thích ngược

Trong giai đoạn chuyển đổi:

- hệ thống cũ vẫn là nguồn hành vi;
- cấu hình mới có thể chạy ở `legacy_compatibility`;
- validator cũ tiếp tục hoạt động;
- kết quả mới phải tương đương đường cơ sở;
- chỉ loại bỏ nhánh cũ sau khi hồi quy đạt.

## 14. Kết luận

Hợp đồng phân tách rõ:

- lõi quy định cái chung;
- dự án quy định cái riêng;
- hồ sơ ghi quyết định của bài;
- QMD hiện thực hóa;
- checker xác minh phần mã hóa được;
- con người nghiệm thu và xuất bản.
