# Kế hoạch chuyển đổi sang cỗ máy QMD

> **Trạng thái:** Bản thiết kế v1.0 — Giai đoạn 1.

## 1. Nguyên tắc

- chuyển đổi tăng dần;
- không viết lại checker;
- mỗi bước có hồi quy;
- giữ hành vi trước khi đổi tên hoặc tách mã;
- không sửa bài `ham_ln_x.qmd` để chiều theo hệ thống mới;
- không xuất bản;
- mỗi commit chỉ chứa một lớp thay đổi rõ.

## 2. Bước M0 — Khóa tài liệu thiết kế

Đầu ra:

- kiến trúc;
- hợp đồng;
- schema cấu hình;
- vòng đời bài;
- kế hoạch chuyển đổi;
- tiêu chí nghiệm thu.

Chưa sửa mã.

## 3. Bước M1 — Thêm bộ đọc cấu hình

Tạo khả năng:

- tìm `_quy_trinh/cau_hinh_san_xuat_qmd.yml`;
- nạp YAML an toàn;
- kiểm tra schema tối thiểu;
- trả về đối tượng cấu hình.

Chưa thay nhánh `is_function_article()`.

Kiểm tra:

- unit test hoặc script kiểm tra cấu hình;
- checker cũ vẫn cho kết quả như trước.

## 4. Bước M2 — Tạo cấu hình 100+ Hàm số ở chế độ tương thích

Tạo:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Khai báo dữ liệu hiện hành:

- project root;
- `core/`, `depth/`;
- thư mục hồ sơ;
- `cards.yml`;
- `listing-order`;
- lớp trang;
- bài hồi quy;
- `compatibility.mode: legacy`.

Checker đọc được cấu hình nhưng vẫn gọi validator cũ.

## 5. Bước M3 — Thay nhận diện gắn cứng bằng khám phá dự án

Thay:

```text
is_function_article()
```

bằng:

```text
discover_project()
identify_article_type()
```

Trong chế độ `legacy`, kết quả cuối vẫn gọi:

```text
validate_function_article()
```

Hồi quy:

- `scope ham_ln_x.qmd`;
- kết quả không có `FAIL` mới;
- bài vẫn được nhận diện đúng.

## 6. Bước M4 — Chuyển hằng dữ liệu sang cấu hình

Chuyển dần:

- `FUNCTION_ARTICLE_DIRS`;
- `FUNCTION_PROFILE_DIR`;
- `FUNCTION_CANONICAL_BASE`;
- lớp `body`;
- placeholder dự án;
- đường dẫn dữ liệu thẻ.

Không chuyển logic validator sang YAML.

Sau mỗi nhóm:

- chạy scope;
- so sánh tên và số kiểm tra quan trọng;
- kiểm tra trạng thái thẻ vẫn `pending`.

## 7. Bước M5 — Tách validator lõi

Trích từ validator hàm số:

- front matter;
- placeholder chung;
- metadata lõi;
- tài nguyên;
- HTML/PDF chung;
- cảnh báo quan sát.

Giữ validator hàm số cho:

- thẻ;
- `listing-order`;
- profile hàm số;
- hình mở rộng theo quy tắc dự án;
- nghiệp vụ riêng.

Hồi quy `scope` và `render` khi nhánh sau render thay đổi.

## 8. Bước M6 — Tách hồ sơ lõi và phần mở rộng

Thiết kế:

```yaml
loi: ...
mo_rong:
  ham_so: ...
```

Tạo mẫu mới nhưng chưa buộc hồ sơ cũ chuyển ngay.

Thêm adapter đọc hồ sơ phiên bản cũ.

Chỉ chuyển `ham_ln_x.yml` trong một nhiệm vụ di trú riêng sau khi adapter đã được kiểm nghiệm.

## 9. Bước M7 — Chuyển sang chế độ native

Khi:

- cấu hình dự án đủ;
- validator lõi đã tách;
- validator hàm số vẫn đạt;
- hồ sơ tương thích;
- `ham_ln_x` hồi quy đạt;

thì đổi:

```yaml
compatibility:
  mode: native
```

Giữ nhánh legacy thêm một chu kì ngắn để đối chiếu, sau đó loại bỏ trong commit riêng.

## 10. Bước M8 — Khởi tạo 100+ Bài toán thực tế

Tạo tối thiểu:

- `AGENTS.md` cục bộ;
- `_quy_trinh/cau_hinh_san_xuat_qmd.yml`;
- quy chuẩn nội dung tối thiểu;
- mẫu hồ sơ mở rộng;
- một bài thử;
- validator dự án tối thiểu.

Dùng cùng:

- lõi QMD;
- HTML/PDF;
- báo cáo;
- vòng đời;
- cổng xuất bản.

## 11. Bước M9 — Đánh giá lần hai

Sau hai dự án:

- xem lại quy tắc nhóm C;
- chỉ thăng cấp quy tắc đã có bằng chứng ở hai dự án;
- thu gọn trường hoặc mô-đun không cần;
- khóa phiên bản 1.0 của hệ thống.

## 12. Chiến lược commit

Dự kiến:

```text
docs(qmd-system): define architecture and contracts
feat(checker): add project configuration loader
feat(functions): add qmd production configuration
refactor(checker): discover project article types
refactor(checker): load function project constants from config
refactor(checker): split qmd core validators
refactor(profiles): support core and project extensions
test(qmd-system): preserve ln x regression baseline
feat(real-world): add initial qmd project configuration
test(qmd-system): validate two-project workflow
```

## 13. Điều kiện dừng khẩn cấp

Dừng khi:

- bài hồi quy không còn được nhận diện;
- validator cũ bị mất trước khi validator mới tương đương;
- QMD phải sửa chỉ để checker mới vượt qua;
- PDF hoặc metadata đầu ra thay đổi ngoài dự kiến;
- trạng thái `pending` bị đổi;
- diff lan sang tệp ngoài phạm vi;
- YAML được dùng để thực thi mã tùy ý;
- cấu hình tạo nhiều nguồn có thẩm quyền cạnh tranh.

## 14. Kết luận

Chuyển đổi được thực hiện bằng lớp tương thích, không bằng thay thế toàn bộ.

Mỗi bước chỉ thay một điểm nối và luôn giữ một đường quay lại an toàn.
