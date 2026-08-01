# Hệ thống sản xuất và kiểm định QMD cho ZO Math

> **Trạng thái:** Đang thiết kế — Giai đoạn 0.
>
> Thư mục này hiện là hồ sơ thiết kế nội bộ. Các tài liệu trong đây chưa tự động trở thành quy chuẩn có hiệu lực trên toàn ZO Math.

## 1. Tên gọi

Tên đầy đủ:

**Thiết kế hệ thống sản xuất và kiểm định QMD cho ZO Math**

Tên gọi ngắn trong quá trình làm việc:

**Thiết kế cỗ máy QMD**

## 2. Mục tiêu

Xây dựng một hệ thống dùng chung để hỗ trợ quá trình:

```text
tiếp nhận nhiệm vụ
→ khóa phạm vi
→ khởi tạo hồ sơ
→ xây dựng nội dung
→ tạo QMD và tài nguyên
→ kiểm định tự động
→ kiểm định có người quan sát
→ nghiệm thu
→ chuẩn bị xuất bản
```

Hệ thống phải hỗ trợ nhiều dự án nội dung của ZO Math mà không sao chép nguyên bộ quy trình, mẫu và checker cho từng dự án.

Việc xuất bản không thuộc quyền tự động của hệ thống. Mỗi bài chỉ được chuyển sang trạng thái công khai khi người dùng xác nhận rõ.

## 3. Kiến trúc đích sơ bộ

Hệ thống dự kiến gồm bốn tầng:

1. **Lõi dùng chung của ZO Math**
   - hợp đồng QMD;
   - metadata;
   - HTML và PDF;
   - tài nguyên;
   - hồ sơ sản xuất;
   - kiểm định;
   - nghiệm thu;
   - trạng thái và bàn giao.

2. **Cấu hình dự án**
   - phạm vi thư mục;
   - kiểu bài;
   - metadata bổ sung;
   - tài nguyên và dữ liệu dự án;
   - bộ kiểm tra cần kích hoạt;
   - cơ chế quản lí trạng thái.

3. **Quy chuẩn nội dung chuyên biệt**
   - khảo sát hàm số;
   - mô hình hóa bài toán thực tế;
   - các mô-đun chuyên môn khác.

4. **Hồ sơ của từng bài**
   - phạm vi;
   - tài liệu điều khiển;
   - quyết định nội dung;
   - tài nguyên;
   - kiểm định;
   - nghiệm thu;
   - bàn giao.

Đây mới là kiến trúc định hướng. Cấu trúc chính thức chỉ được khóa sau khi hoàn thành kiểm kê và phân loại chung–riêng.

## 4. Hai dự án kiểm nghiệm ban đầu

### 4.1. 100+ Hàm số: Sự biến thiên và đồ thị

Dự án hiện có hệ thống sản xuất bài hoạt động thực tế và được dùng làm đường cơ sở hồi quy.

Bài kiểm nghiệm chính:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
```

### 4.2. 100+ Bài toán thực tế

Dự án này sẽ được dùng làm trường hợp thứ hai để kiểm tra rằng lõi mới không bị gắn cứng với nghiệp vụ khảo sát hàm số.

Ở giai đoạn hiện tại chưa tạo bài hoặc cấu trúc dự án mới.

## 5. Nguyên tắc thiết kế

- Khảo sát hiện trạng trước khi thiết kế.
- Phân biệt bằng chứng hiện trạng với quyết định mới.
- Chỉ đưa một quy tắc vào lõi khi nó thực sự dùng chung.
- Không sao chép toàn bộ quy trình của một dự án sang dự án khác.
- Không viết lại checker từ đầu.
- Chuyển đổi từng phần và giữ khả năng hồi quy.
- Giữ nguyên giao diện lệnh `quick`, `scope` và `render` nếu không có lí do bắt buộc phải thay đổi.
- Một điểm vào kiểm định có thể kích hoạt các bộ quy tắc khác nhau theo cấu hình dự án.
- Hồ sơ bài phải ghi được cả phần dùng chung và phần mở rộng chuyên biệt.
- Xuất bản luôn là một cổng riêng cần người dùng xác nhận.
- Không suy diễn quy chuẩn từ một bài mẫu.

## 6. Các giai đoạn thực hiện

### Giai đoạn 0 — Khóa đường cơ sở

- kiểm kê nguồn có thẩm quyền;
- lập bản đồ kiến trúc hiện trạng;
- phân loại quy tắc chung–riêng;
- xác định đường cơ sở hồi quy;
- xác định các ràng buộc không được phá vỡ.

### Giai đoạn 1 — Thiết kế kiến trúc và hợp đồng

- khóa các tầng của hệ thống;
- định nghĩa giao diện giữa lõi và dự án;
- định nghĩa vòng đời bài;
- định nghĩa cấu trúc cấu hình;
- lập kế hoạch chuyển đổi.

### Giai đoạn 2 — Tách lõi dùng chung

- tách quy chuẩn kĩ thuật lõi;
- tách quy trình lõi;
- tạo mẫu QMD lõi;
- tạo mẫu hồ sơ lõi;
- giữ lớp tương thích với hệ thống hiện tại.

### Giai đoạn 3 — Cấu hình hóa 100+ Hàm số

- tạo cấu hình dự án;
- giữ quy chuẩn khảo sát hàm số ở tầng chuyên biệt;
- chuyển các điểm gắn cứng sang cấu hình;
- chạy hồi quy trên bài đã nghiệm thu.

### Giai đoạn 4 — Cấu hình hóa checker

- thêm bộ đọc cấu hình;
- tách kiểm tra dùng chung;
- kích hoạt kiểm tra chuyên biệt theo dự án;
- giữ nguyên các lệnh vận hành hiện hành;
- kiểm tra hồi quy sau từng nhóm thay đổi.

### Giai đoạn 5 — Kiểm nghiệm bằng dự án thứ hai

- tạo cấu hình tối thiểu cho 100+ Bài toán thực tế;
- tạo một bài thử đại diện;
- chạy cùng hệ thống QMD, HTML, PDF, hồ sơ và kiểm định;
- chỉ tổng quát hóa những gì đã được chứng minh cần thiết trong cả hai dự án.

## 7. Tài liệu hiện có trong thư mục

- `README.md`: mục tiêu, phạm vi và kế hoạch tổng thể.
- `kiem_ke_he_thong_hien_tai.md`: bằng chứng kiểm kê của Giai đoạn 0.
- `ban_do_kien_truc_hien_trang.md`: quan hệ giữa các thành phần hiện hành.

Các tài liệu thiết kế chính thức sẽ chỉ được bổ sung sau khi ba tài liệu đường cơ sở được duyệt.
