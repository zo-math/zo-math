# Hợp đồng giữa lõi, dự án, hồ sơ và QMD

> **Trạng thái:** Hợp đồng vận hành — phiên bản 1.0.

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

Mỗi tầng trả lời một loại câu hỏi khác nhau:

| Tầng | Câu hỏi chính |
|---|---|
| Lõi | Mọi bài QMD đã đăng kí phải bảo đảm điều gì? |
| Dự án | Dự án này tổ chức bài ở đâu và thêm yêu cầu nào? |
| Quy chuẩn chuyên biệt | Nội dung chuyên môn phải được xây dựng và kiểm định ra sao? |
| Hồ sơ bài | Bài cụ thể chọn gì, đang ở trạng thái nào và có bằng chứng nào? |
| QMD | Sản phẩm nguồn hiện thực hóa các quyết định như thế nào? |
| Checker | Các điều kiện có thể mã hóa có đạt không? |
| Người nghiệm thu | Toán học, nội dung, sư phạm và đầu ra thật có đạt không? |

Không tầng nào được chiếm trách nhiệm của tầng khác.

## 3. Hợp đồng của lõi

Lõi có trách nhiệm:

- định nghĩa vòng đời bài;
- định nghĩa metadata nền;
- định nghĩa kiểm tra nguồn, HTML và PDF dùng chung;
- định nghĩa cách ghi kết quả và mã thoát;
- định nghĩa cổng nghiệm thu và xuất bản;
- cung cấp registry mô-đun an toàn;
- giữ giao diện checker thống nhất;
- giữ khả năng hồi quy nhiều dự án.

Lõi không được:

- áp đặt kiến trúc nội dung của một dự án;
- chứa đường dẫn riêng của dự án;
- yêu cầu trường chuyên môn không áp dụng;
- tự quyết định nghiệm thu hoặc xuất bản;
- cho phép dự án vô hiệu hóa bất biến an toàn;
- thực thi mã do YAML cung cấp.

## 4. Hợp đồng của cấu hình dự án

Cấu hình phải nằm tại:

```text
<project.root>/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Cấu hình phải khai báo các nhóm trường:

- `schema_version`;
- `project`;
- `discovery`;
- `profiles`;
- `modules`;
- `metadata`;
- `publication`;
- `references`;
- `regression`;
- `extensions`.

`catalog` là nhóm tùy chọn khi dự án có danh mục hoặc lưới thẻ.

Cấu hình có thể:

- thêm metadata bắt buộc;
- khai báo mẫu đường dẫn và loại bài;
- khai báo thư mục hồ sơ;
- kích hoạt mô-đun bắt buộc đã đăng kí;
- khai báo mô-đun tùy chọn;
- khai báo dữ liệu danh mục;
- khai báo lớp trang;
- khai báo placeholder dự án;
- dẫn chiếu tài liệu điều khiển;
- chỉ định bài hồi quy;
- cung cấp dữ liệu mở rộng cho adapter dự án.

Cấu hình không được:

- chỉ định hàm Python tùy ý;
- import module;
- tắt kiểm tra an toàn của lõi;
- tự sửa QMD;
- tự chuyển `published`;
- khai báo đường dẫn chứa `..` hoặc thoát repository;
- ghi đè tài liệu cấp cao hơn;
- dùng khóa top-level không thuộc schema phiên bản 1.

## 5. Hợp đồng của quy chuẩn chuyên biệt

Quy chuẩn chuyên biệt chịu trách nhiệm về:

- đơn vị nội dung;
- phương pháp khảo sát hoặc mô hình hóa;
- cấu trúc nhận thức;
- tiêu chuẩn lập luận;
- biểu diễn chuyên môn;
- tiêu chí kiểm định nội dung;
- điều kiện dừng chuyên môn.

Quy chuẩn chỉ có hiệu lực trong dự án khi được `AGENTS.md`, cấu hình dự án hoặc yêu cầu hiện tại dẫn chiếu phù hợp. Một tệp chỉ tồn tại trong repository không tự động trở thành nguồn có thẩm quyền.

## 6. Hợp đồng của hồ sơ bài

Hồ sơ bài phải ghi được:

- nhận diện bài và loại bài;
- phạm vi được sửa;
- tài liệu điều khiển đã dùng;
- quyết định và ngoại lệ;
- tài nguyên;
- bằng chứng kiểm định;
- kết quả kiểm định có người quan sát;
- trạng thái sản xuất;
- trạng thái xuất bản;
- vấn đề còn lại;
- sản phẩm bàn giao.

Phiên bản 1.0 không ép mọi dự án dùng một schema hồ sơ vật lí giống hệt nhau. Adapter dự án chịu trách nhiệm kiểm tra schema hồ sơ của dự án đó.

Hồ sơ không được:

- thay thế quy chuẩn;
- tự cho phép bỏ qua kiểm tra bắt buộc;
- dùng `không áp dụng` mà không có lí do;
- chứa đường dẫn cá nhân hoặc máy cụ thể khi không cần thiết;
- tự chuyển bài sang công khai.

## 7. Hợp đồng của QMD

QMD phải:

- thỏa metadata hiệu lực;
- hiện thực đúng quyết định trong hồ sơ;
- tham chiếu tài nguyên hợp lệ;
- không chứa placeholder bị cấm;
- không chứa thao tác mã bị cấm;
- không dùng cấu trúc bị dự án cấm;
- render được khi giai đoạn yêu cầu;
- tạo đầu ra phù hợp với trạng thái.

QMD không được:

- tự định nghĩa quy tắc kiểm định;
- tự tắt validator;
- dùng metadata để vượt cổng xuất bản;
- thay thế hồ sơ sản xuất;
- mang metadata chuyên biệt của dự án khác nếu không có hợp đồng rõ.

## 8. Hợp đồng của registry và adapter

Registry phải:

- dùng danh sách mô-đun cố định trong Python;
- từ chối mã mô-đun chưa đăng kí;
- giới hạn mô-đun theo `article_type`;
- trả về kế hoạch validator xác định;
- không nhận tên hàm từ YAML.

Adapter nguồn phải:

- chỉ chạy cho loại bài đã đăng kí;
- nhận cấu hình đã được loader xác thực;
- gọi validator lõi khi hợp đồng dự án yêu cầu;
- ghi kết quả qua checker thống nhất;
- không sửa tệp.

Adapter sau render phải:

- chỉ chạy khi render thành công và HTML tồn tại;
- kiểm tra đầu ra của đúng bài;
- không coi kiểm tra cấu trúc là kiểm định trực quan cuối.

## 9. Hợp đồng của checker

Checker phải:

- nhận diện đúng dự án;
- nạp cấu hình một cách xác định;
- từ chối cấu hình không hợp lệ;
- xác định duy nhất một loại bài;
- tạo kế hoạch validator từ registry;
- chạy kiểm tra dùng chung của repository;
- chạy đúng source adapter và render adapter;
- phân biệt `PASS`, `WARN`, `FAIL`, `INFO`;
- giữ mã thoát nhất quán;
- tạo báo cáo JSON khi được yêu cầu;
- không tự sửa tệp;
- không stage, commit hoặc xuất bản.

Checker không được tuyên bố nghiệm thu nội dung cuối cùng.

## 10. Hợp đồng của người nghiệm thu

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

Cảnh báo `human-review-required` và `rendered-visual-review` là cổng bàn giao cho con người, không phải lỗi kĩ thuật tự động.

## 11. Hợp đồng hiệu lực

Checker tạo hợp đồng hiệu lực theo thứ tự:

```text
bất biến lõi
+ yêu cầu dự án
+ mô-đun bắt buộc đã đăng kí
+ dữ liệu mở rộng hợp lệ
= kế hoạch kiểm định của bài
```

Metadata QMD và đầu ra được kiểm tra theo kế hoạch này.

`modules.optional` không tự động tạo adapter hoạt động trong phiên bản 1.0. Muốn một adapter chạy, mô-đun tương ứng phải nằm trong `modules.required` và được cài trong registry cùng bảng dispatch của checker.

## 12. Xung đột

Khi có xung đột:

1. dừng kiểm tra chuyên biệt của bài khi không thể xác định hợp đồng;
2. báo rõ hai nguồn hoặc trường xung đột;
3. không âm thầm chọn một bên;
4. không sửa nguồn điều khiển;
5. dùng thứ tự thẩm quyền;
6. yêu cầu quyết định của người dùng khi thứ tự thẩm quyền chưa đủ.

## 13. Không áp dụng

Một kiểm tra chỉ được đánh dấu `không áp dụng` khi:

- lõi hoặc mô-đun cho phép;
- hồ sơ ghi lí do;
- adapter xác nhận điều kiện;
- việc bỏ qua không làm mất bất biến an toàn.

Không được dùng danh sách `optional_modules` để ngầm bỏ qua kiểm tra bắt buộc.

## 14. Phiên bản và tương thích

Phiên bản 1.0 dùng:

```text
schema_version: 1
checker: 2.6.0
validation mode: native
```

Không còn khóa cấu hình `compatibility`, không còn `legacy_validator` và không còn fallback legacy cho bài hàm số thiếu cấu hình.

Trường `compatibility_mode: "native"` có thể vẫn xuất hiện trong bản tóm tắt hoặc kế hoạch validator để giữ ổn định định dạng báo cáo. Đây không phải khóa của schema cấu hình phiên bản 1.

Khi nâng phiên bản:

- thay đổi schema phải có phiên bản mới hoặc đường di trú rõ;
- thay đổi giao diện checker phải có lí do và hồi quy;
- không khôi phục đường legacy chỉ để né cấu hình dự án;
- hai dự án đường cơ sở phải cùng đạt trước khi khóa phiên bản mới.

## 15. Kết luận

Hợp đồng phân tách rõ:

- lõi quy định cái chung;
- dự án quy định cái riêng;
- hồ sơ ghi quyết định của bài;
- QMD hiện thực hóa;
- registry giới hạn khả năng mở rộng;
- checker xác minh phần mã hóa được;
- con người nghiệm thu và xuất bản.
