# Kế hoạch chuyển đổi sang cỗ máy QMD

> **Trạng thái:** Hồ sơ chuyển đổi đã hoàn tất M0–M9A; M9B khóa tài liệu phiên bản 1.0.
>
> Tài liệu này ghi lại đường chuyển đổi đã thực hiện. Các mô tả legacy chỉ có giá trị lịch sử và không phải hướng dẫn vận hành hiện tại.

## 1. Nguyên tắc đã giữ

- chuyển đổi tăng dần;
- không viết lại checker từ đầu;
- mỗi bước có hồi quy;
- giữ hành vi trước khi tách trách nhiệm;
- không sửa `ham_ln_x.qmd` để chiều theo hệ thống mới;
- không tự xuất bản;
- mỗi commit chỉ chứa một lớp thay đổi rõ;
- không stage các thay đổi ngoài phạm vi;
- chỉ loại bỏ nhánh cũ sau khi hai đường chạy tương đương.

## 2. M0 — Khóa tài liệu thiết kế

**Trạng thái:** Hoàn tất.

Commit:

```text
b8740b0  docs(qmd-system): define architecture and baseline
```

Đầu ra:

- kiểm kê hiện trạng;
- bản đồ kiến trúc;
- phân loại chung–riêng;
- kiến trúc và hợp đồng;
- schema cấu hình;
- vòng đời bài;
- đường cơ sở `ham_ln_x`;
- kế hoạch chuyển đổi;
- tiêu chí nghiệm thu.

## 3. M1–M2 — Nền cấu hình dự án

**Trạng thái:** Hoàn tất.

Commit:

```text
48ae4f3  feat(qmd-system): add project configuration foundation
```

Kết quả:

- tạo `scripts/zo_qmd_config.py`;
- nạp YAML an toàn;
- từ chối khóa trùng;
- kiểm tra schema;
- tìm cấu hình gần nhất;
- xác định loại bài và hồ sơ;
- tạo cấu hình đầu tiên cho 100+ Hàm số;
- giữ đường chạy cũ trong giai đoạn chuyển tiếp.

## 4. M3 — Khám phá dự án thay nhận diện gắn cứng

**Trạng thái:** Hoàn tất.

Commit:

```text
9c92cd2  refactor(checker): discover configured qmd projects
```

Kết quả:

- checker nhận diện bài qua cấu hình dự án;
- báo `project_id`, `article_type` và đường dẫn cấu hình;
- giữ hồi quy bài `ham_ln_x.qmd`.

## 5. M4 — Chuyển dữ liệu dự án ra cấu hình

**Trạng thái:** Hoàn tất.

Commit:

```text
d386588  refactor(qmd-system): move function rules into project config
```

Kết quả:

- metadata bắt buộc lấy từ cấu hình;
- lớp `body` lấy từ cấu hình;
- placeholder dự án lấy từ cấu hình;
- hồ sơ và dữ liệu thẻ được tham chiếu qua cấu hình;
- logic validator vẫn nằm trong Python.

## 6. M5 — Tách validator lõi

**Trạng thái:** Hoàn tất.

Commit:

```text
2ae9661  refactor(qmd-system): extract shared qmd core validator
```

Kết quả:

- tạo `scripts/zo_qmd_core.py`;
- tách front matter, metadata, placeholder, tiêu đề, hình, đường dẫn và mã thực thi dùng chung;
- validator hàm số giữ nghiệp vụ riêng;
- hồi quy nguồn và render được bảo toàn.

## 7. M6 — Registry và dispatch adapter

**Trạng thái:** Hoàn tất.

Commit:

```text
e6371d6  refactor(qmd-system): add validator registry and dispatch
```

Kết quả:

- tạo `scripts/zo_qmd_registry.py`;
- registry mô-đun cố định trong Python;
- tạo kế hoạch validator;
- thêm source adapter và render adapter;
- YAML không được gọi hàm tùy ý.

## 8. M7 — Chuyển 100+ Hàm số sang native

**Trạng thái:** Hoàn tất.

Commit:

```text
b577787  refactor(qmd-system): switch functions project to native mode
```

Kết quả:

- dự án 100+ Hàm số chạy qua registry và adapter;
- không thay đổi nội dung `ham_ln_x.qmd`;
- thẻ 114 tiếp tục `pending`;
- PDF 15 trang và metadata được bảo toàn.

## 9. M8 — Khởi tạo 100+ Bài toán thực tế

**Trạng thái:** Hoàn tất.

Commit:

```text
31a1916  feat(real-world): add initial qmd project configuration
```

Đầu ra:

- `AGENTS.md` cục bộ;
- cấu hình dự án;
- quy chuẩn nội dung tối thiểu;
- hồ sơ sản xuất mặc định;
- hồ sơ bài thử;
- bài `chi_phi_di_taxi.qmd`;
- SVG đại diện;
- PDF 4 trang;
- `scripts/zo_real_world_problem.py`;
- source adapter và render adapter `real-world-problem`.

Kết quả kiểm nghiệm:

- dùng cùng loader, registry, checker và validator lõi;
- không mang `listing-order`;
- đủ cấu trúc mô hình hóa riêng;
- HTML/PDF hoạt động;
- trạng thái vẫn `pending`.

## 10. M9A — Đánh giá lần hai và loại bỏ legacy

**Trạng thái:** Hoàn tất.

Commit:

```text
ab7581a  refactor(qmd-system): remove legacy compatibility path
```

Kết quả:

- hai cấu hình đều native;
- loại bỏ `legacy_validation_plan`;
- loại bỏ `legacy_validator`;
- loại bỏ fallback cho bài hàm số thiếu cấu hình;
- loại bỏ khối `compatibility` khỏi schema đang hoạt động;
- checker nâng lên 2.6.0;
- hồi quy nguồn và render của hai dự án đều đạt;
- diff thu gọn 149 dòng.

Tên kiểm tra `function-legacy-classes` vẫn được giữ vì nó phát hiện lớp CSS cũ trong QMD; nó không phải đường chạy tương thích legacy.

## 11. M9B — Khóa tài liệu phiên bản 1.0

**Trạng thái:** Hoàn tất khi commit gói tài liệu M9B.

Phạm vi:

- cập nhật `README.md` thành điểm vào vận hành;
- cập nhật kiến trúc và hợp đồng theo mã đang chạy;
- khóa schema cấu hình không còn `compatibility`;
- khóa vòng đời hai trục;
- ghi đường cơ sở hồi quy hai dự án;
- thêm hướng dẫn tạo dự án và validator;
- ghi kết quả đánh giá phiên bản 1.0;
- giữ tài liệu Giai đoạn 0 như hồ sơ lịch sử.

M9B không sửa checker, cấu hình dự án, QMD, PDF hoặc trạng thái xuất bản.

## 12. Chuỗi commit nền phiên bản 1.0

```text
b8740b0  docs(qmd-system): define architecture and baseline
48ae4f3  feat(qmd-system): add project configuration foundation
9c92cd2  refactor(checker): discover configured qmd projects
d386588  refactor(qmd-system): move function rules into project config
2ae9661  refactor(qmd-system): extract shared qmd core validator
e6371d6  refactor(qmd-system): add validator registry and dispatch
b577787  refactor(qmd-system): switch functions project to native mode
31a1916  feat(real-world): add initial qmd project configuration
ab7581a  refactor(qmd-system): remove legacy compatibility path
```

## 13. Điều kiện dừng đã áp dụng

Quá trình phải dừng khi:

- bài hồi quy không còn được nhận diện;
- validator mới không tương đương đường cơ sở;
- QMD phải sửa chỉ để checker mới vượt qua;
- PDF hoặc metadata đầu ra thay đổi ngoài dự kiến;
- trạng thái `pending` bị đổi;
- diff lan sang tệp ngoài phạm vi;
- YAML được dùng để thực thi mã tùy ý;
- cấu hình tạo nguồn có thẩm quyền cạnh tranh;
- một dự án phải mang metadata chuyên biệt của dự án khác.

Không điều kiện dừng nào bị kích hoạt trong chuỗi M0–M9A.

## 14. Những quyết định chưa tổng quát hóa

Phiên bản 1.0 chưa coi các điểm sau là lõi chung bắt buộc:

- schema hồ sơ vật lí duy nhất cho mọi dự án;
- dispatch độc lập cho mọi mô-đun tùy chọn;
- cấu trúc danh mục dùng chung cho mọi dự án;
- quy chuẩn bảng biến thiên;
- quy chuẩn nội dung đầy đủ của 100+ Bài toán thực tế;
- tự động hóa xuất bản.

Chỉ thăng cấp các điểm này sau khi có thêm bằng chứng vận hành và nhiệm vụ riêng.

## 15. Kết luận

Chuyển đổi đã hoàn thành theo nguyên tắc thay từng điểm nối, hồi quy sau mỗi bước và loại bỏ nhánh cũ chỉ sau khi hai dự án chạy native.

Phiên bản 1.0 được khóa bởi:

```text
một checker
+ một loader cấu hình
+ một validator lõi
+ một registry an toàn
+ hai adapter dự án
+ hai đường cơ sở hồi quy
+ quyền nghiệm thu và xuất bản thuộc người dùng
```
