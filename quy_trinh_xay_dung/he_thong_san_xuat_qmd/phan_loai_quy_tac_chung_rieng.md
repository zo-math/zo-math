# Phân loại quy tắc chung–riêng của hệ thống QMD

> **Trạng thái:** Bản phân loại cấp nhóm — Giai đoạn 0.
>
> Tài liệu này là đầu vào thiết kế, chưa phải quy chuẩn có hiệu lực.

## 1. Ba trạng thái phân loại

- **A — Dùng chung chắc chắn:** không phụ thuộc nghiệp vụ khảo sát hàm số và có ý nghĩa trực tiếp với nhiều dự án QMD.
- **B — Riêng cho 100+ Hàm số:** phụ thuộc loại bài, dữ liệu, thư mục hoặc quy chuẩn chuyên môn của dự án.
- **C — Chưa đủ căn cứ:** có khả năng dùng chung nhưng chưa được kiểm nghiệm ở dự án thứ hai hoặc chưa khóa cách biểu diễn.

## 2. A — Dùng chung chắc chắn

### 2.1. Điều phối công việc

- đọc chỉ dẫn theo thứ tự thẩm quyền;
- khóa mục tiêu, phạm vi, tệp được sửa và tệp chỉ đọc;
- kiểm tra hiện trạng Git trước khi thay đổi;
- phân biệt nguồn chính thức với đầu ra tự động;
- không tự mở rộng nhiệm vụ;
- không tự commit, push, xuất bản, xóa hoặc di chuyển;
- báo cáo tệp đã thay đổi và kiểm tra đã chạy.

### 2.2. Vòng đời kĩ thuật của bài QMD

```text
tiếp nhận nhiệm vụ
→ khóa phạm vi
→ khởi tạo hồ sơ
→ tạo QMD và tài nguyên
→ kiểm định tự động
→ kiểm định có người quan sát
→ nghiệm thu
→ bàn giao
→ xuất bản khi người dùng xác nhận
```

Tên và số giai đoạn có thể còn điều chỉnh, nhưng các chức năng trên là dùng chung.

### 2.3. Hợp đồng QMD cơ bản

- YAML front matter hợp lệ;
- không còn giá trị giữ chỗ;
- đường dẫn và tài nguyên cục bộ hợp lệ;
- cú pháp Markdown/QMD hợp lệ;
- cấu trúc tiêu đề được kiểm soát;
- mã thực thi và phụ thuộc được khai báo rõ;
- không có thao tác mã bị cấm;
- nội dung và đầu ra truy được về nguồn.

### 2.4. Metadata và đầu ra

Các khái niệm có tính dùng chung:

- tiêu đề hiển thị;
- tiêu đề metadata thuần văn bản;
- `pagetitle`;
- mô tả;
- ngày cập nhật;
- canonical URL;
- ảnh đại diện khi áp dụng;
- lớp trang;
- cấu hình PDF tải xuống;
- branding PDF;
- trạng thái bài.

Tên trường chính xác và trường bắt buộc sẽ được khóa ở Giai đoạn 1.

### 2.5. HTML, PDF và tài nguyên

- render QMD khi nhiệm vụ yêu cầu;
- xác nhận HTML đầu ra;
- kiểm tra lớp `body`;
- kiểm soát số lượng `H1`;
- kiểm tra liên kết và tài nguyên PDF;
- đối chiếu metadata PDF với QMD;
- quản lí nguồn hình, PDF trung gian và SVG;
- có văn bản thay thế khi hình mang thông tin;
- kiểm tra tự động không thay thế quan sát HTML/PDF thật.

### 2.6. Kiểm định và báo cáo

- phân biệt `PASS`, `WARN`, `FAIL`, `INFO`;
- tách kiểm định tự động khỏi nghiệm thu của con người;
- ghi phiên bản checker, phạm vi, kết quả và mã thoát;
- không tự sửa lỗi ngoài phạm vi;
- giữ bằng chứng kiểm định và tiêu chí dừng rõ ràng.

### 2.7. Giao diện checker

Giữ làm lõi:

```text
quick
scope
render
--staged
--report
```

Cùng các chức năng dùng chung:

- tìm gốc repository;
- mở rộng phạm vi;
- kiểm tra Git, EOL và khoảng trắng;
- đọc UTF-8;
- kiểm tra YAML, Markdown, SVG và Python;
- chuẩn bị môi trường Quarto;
- gọi render và đọc log;
- in kết quả và ghi báo cáo JSON.

## 3. B — Riêng cho 100+ Hàm số

### 3.1. Nghiệp vụ toán học

- đơn vị khảo sát là hàm số hoặc họ hàm;
- tham số và miền tham số;
- bản đồ miền;
- vòng rà nền tảng và vòng rà kích hoạt;
- hồ sơ mệnh đề–chứng cứ;
- hiện tượng trung tâm;
- bản đồ hiện tượng;
- mạch lập luận và mạng phụ thuộc;
- trật tự nhận thức của bài khảo sát hàm số.

### 3.2. Cấu trúc dự án

```text
core/
depth/
_data/cards.yml
assets/img/cards/
_quy_trinh/ho_so/
```

Cùng các trường và quan hệ:

- `listing-order`;
- số thẻ;
- `status`;
- `href`;
- ảnh thẻ;
- collection của dự án;
- đối chiếu QMD với thẻ.

### 3.3. Biểu diễn chuyên môn

- đồ thị hàm số;
- miền lấy mẫu và cửa sổ quan sát;
- bảng giá trị;
- bảng dấu;
- bảng biến thiên;
- đọc ngược từ biểu diễn về tính chất hàm số.

Quy chuẩn sinh bảng biến thiên trong tương lai cũng thuộc mô-đun chuyên môn, không thuộc lõi QMD.

### 3.4. Nguồn điều khiển chuyên biệt

```text
_quy_trinh/quy_chuan_khao_sat_ham_so.md
_quy_trinh/nguon_li_thuyet/khung_khao_sat_ham_so_hoan_chinh_04.qmd
quy_trinh_xay_dung/quy_chuan_do_thi_sinh_ma_nguon_tikz_pgfplots.md
```

### 3.5. Validator chuyên biệt

- `is_function_article()`;
- `function_card()`;
- kiểm tra metadata gắn với thẻ;
- kiểm tra `listing-order`;
- kiểm tra `core/` và `depth/`;
- kiểm tra profile trong `_quy_trinh/ho_so/`;
- kiểm tra hình mở rộng theo hồ sơ;
- kiểm tra trạng thái PDF theo thẻ;
- kiểm tra lưới thẻ.

## 4. C — Chưa đủ căn cứ để khóa

### 4.1. Hồ sơ lõi và phần mở rộng

Chưa quyết định:

- hồ sơ lõi là một tệp, schema hay mẫu;
- phần mở rộng dự án được ghép như thế nào;
- trường nào bắt buộc với mọi bài;
- trường nào chỉ kích hoạt theo mô-đun.

### 4.2. Cấu hình dự án

Chưa khóa:

- tên và vị trí tệp cấu hình;
- registry dự án ở cấp repository hay cục bộ;
- cách khai báo thư mục bài, hồ sơ, dữ liệu và validator.

### 4.3. Cách đăng kí validator

Chưa quyết định checker sẽ dùng:

- registry Python;
- YAML kết hợp registry;
- hay một lớp cấu hình trung gian.

Thiết kế phải đơn giản, kiểm tra được và không cho YAML thực thi mã tùy ý.

### 4.4. Metadata PDF và trạng thái bài

Chưa khóa:

- trường PDF nào thuộc lõi;
- quy tắc đối với bài `pending`;
- quan hệ giữa trạng thái hồ sơ, trạng thái bài và trạng thái thẻ;
- vòng đời chính thức từ đang sản xuất đến `published`.

### 4.5. Lưới thẻ

Hiện chỉ đủ căn cứ để khẳng định lưới thẻ không phải lõi bắt buộc của mọi bài QMD. Chưa khóa nó là mô-đun dùng chung hay thành phần riêng của từng dự án.

### 4.6. Dự án 100+ Bài toán thực tế

Chưa xác định:

- cấu trúc thư mục;
- dữ liệu danh mục;
- mẫu QMD;
- hồ sơ chuyên môn;
- quy chuẩn nội dung;
- bài thử đại diện.

## 5. Bảng tóm tắt

| Thành phần | Nhóm | Hướng xử lí |
|---|---:|---|
| Quy tắc làm việc với agent | A | Giữ ở cấp repository và dẫn chiếu |
| Quy trình kĩ thuật chung | A | Dùng làm nền của quy trình lõi |
| YAML và metadata cơ bản | A | Tách thành hợp đồng lõi |
| HTML/PDF và tài nguyên | A | Tách validator lõi, cho phép cấu hình |
| Kiểm định, nghiệm thu, bàn giao | A | Tách thành quy trình lõi |
| `quick`, `scope`, `render` | A | Giữ nguyên giao diện |
| Quy chuẩn khảo sát hàm số | B | Giữ trong dự án |
| `core/`, `depth/` | B | Khai báo bằng cấu hình dự án |
| `cards.yml`, `listing-order` | B | Giữ trong mô-đun dự án/lưới thẻ |
| Đồ thị, bảng dấu, bảng biến thiên | B | Giữ trong mô-đun chuyên môn |
| Hồ sơ lõi và phần mở rộng | C | Thiết kế ở Giai đoạn 1 |
| Registry dự án và validator | C | Thiết kế ở Giai đoạn 1 |
| Mô hình trạng thái | C | Thiết kế ở Giai đoạn 1 |
| Cấu trúc dự án thứ hai | C | Xác định sau khi khóa lõi tối thiểu |

## 6. Điều kiện đưa một quy tắc vào lõi

Một quy tắc chỉ được đưa vào lõi khi:

1. không phụ thuộc ý nghĩa chuyên môn của một dự án;
2. được chứng minh cần thiết trong ít nhất hai ngữ cảnh thực;
3. không chứa đường dẫn hoặc cấu trúc riêng của một dự án;
4. có tiêu chí kiểm tra hoặc nghiệm thu rõ;
5. làm giảm trùng lặp mà không khiến lõi khó hiểu hơn.

## 7. Kết luận

Bản phân loại cấp nhóm đủ để chuyển sang Giai đoạn 1.

Ba vấn đề thiết kế đầu tiên là:

1. hợp đồng giữa lõi và cấu hình dự án;
2. cấu trúc hồ sơ lõi cùng phần mở rộng;
3. cơ chế checker chọn validator theo dự án mà không thay giao diện lệnh.
