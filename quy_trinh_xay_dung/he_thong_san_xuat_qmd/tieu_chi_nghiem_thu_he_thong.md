# Tiêu chí nghiệm thu hệ thống sản xuất và kiểm định QMD

> **Trạng thái:** Kết quả đánh giá phiên bản 1.0 — đạt về kiến trúc và kiểm định tự động; có hiệu lực từ commit khóa tài liệu M9B.
>
> Nghiệm thu hệ thống không thay thế nghiệm thu nội dung của từng bài và không thay thế xác nhận xuất bản của người dùng.

## 1. Phạm vi nghiệm thu

Phiên bản 1.0 phải chứng minh:

- một lõi phục vụ ít nhất hai dự án;
- 100+ Hàm số không bị suy yếu;
- 100+ Bài toán thực tế không phải mang các trường của hàm số;
- checker vẫn có một điểm vào thống nhất;
- cấu hình không thực thi mã tùy ý;
- xuất bản vẫn do người dùng quyết định.

**Kết quả:** ĐẠT.

## 2. Kiến trúc

| Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|
| Bốn tầng được biểu diễn rõ | ĐẠT | Lõi, cấu hình dự án, hồ sơ/quy chuẩn, QMD/đầu ra |
| Cấu hình cục bộ được khám phá xác định | ĐẠT | `discover_project_config()` tìm cấu hình gần nhất |
| Registry không cho thực thi mã tùy ý | ĐẠT | Danh sách `MODULE_SPECS` cố định trong Python |
| Validator lõi tách khỏi nghiệp vụ dự án | ĐẠT | `scripts/zo_qmd_core.py` |
| Validator dự án chỉ chạy đúng loại bài | ĐẠT | Kế hoạch registry và hai bảng dispatch |
| Lõi không chứa metadata bắt buộc của dự án thứ hai | ĐẠT | Bài thực tế không cần `listing-order` |
| Không còn đường legacy | ĐẠT | Commit `ab7581a`; kiểm tra không còn `legacy_validator` hoặc fallback |

## 3. Cấu hình dự án

| Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|
| Schema có phiên bản | ĐẠT | `schema_version: 1` |
| Khóa trùng bị từ chối | ĐẠT | Loader tùy biến `SafeLoader`; self-test |
| Khóa không biết bị từ chối | ĐẠT | `_known_keys()` |
| Đường dẫn không thể thoát repository | ĐẠT | đường dẫn tương đối, cấm `..`, kiểm tra `_inside()` |
| Vị trí cấu hình phải khớp `project.root` | ĐẠT | loader so với vị trí chuẩn |
| Loại bài không được khớp chồng trên cùng tệp | ĐẠT | `article_type_for()` từ chối nhiều kết quả |
| Mô-đun chưa đăng kí bị từ chối | ĐẠT | loader và registry |
| `qmd-core` bắt buộc | ĐẠT | loader từ chối cấu hình thiếu lõi |
| Cổng xác nhận xuất bản không thể tắt | ĐẠT | `user_confirmation_required` bắt buộc là `true` |
| Hai dự án có cấu hình riêng | ĐẠT | `functions_100`, `real_world_100` |

## 4. Checker

| Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|
| Giữ `quick`, `scope`, `render` | ĐẠT | CLI checker 2.6.0 |
| Giữ `--staged`, `--report` | ĐẠT | parser chung |
| Validator lõi chạy cho cả hai dự án | ĐẠT | `qmd-core-validator` xuất hiện ở cả hai hồi quy |
| Source adapter chạy đúng dự án | ĐẠT | `functions-article`, `real-world-problem` |
| Render adapter chạy đúng dự án | ĐẠT | hai adapter sau render đều qua |
| Báo cáo JSON giữ thông tin cốt lõi | ĐẠT | checker ghi report trong `_audit/` |
| Mã thoát nhất quán | ĐẠT | 0/1/2/3 |
| Checker không sửa tệp | ĐẠT | checker chỉ đọc, render và ghi report khi yêu cầu |
| Checker không stage, commit hoặc xuất bản | ĐẠT | không có chức năng tương ứng |
| Cảnh báo không bị nhầm thành nghiệm thu cuối | ĐẠT | `FINAL ACCEPTANCE: NOT_RUN` |

Phiên bản đường cơ sở:

```text
CHECKER VERSION: 2.6.0
```

## 5. Hồi quy 100+ Hàm số

Bài:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
```

| Tiêu chí | Kết quả |
|---|---|
| Được nhận diện là `functions_100` | ĐẠT |
| Được nhận diện là `function_article` | ĐẠT |
| Kế hoạch chạy `functions-article` | ĐẠT |
| Không cần sửa QMD để chuyển kiến trúc | ĐẠT |
| Không có `FAIL` mới | ĐẠT |
| HTML có lớp trang bắt buộc | ĐẠT |
| HTML có đúng một H1 | ĐẠT |
| HTML có liên kết PDF | ĐẠT |
| PDF Title khớp `title-meta` | ĐẠT |
| PDF đọc được, đường cơ sở 15 trang | ĐẠT |
| Hồ sơ hình được kiểm tra | ĐẠT |
| Số hình mở rộng bằng 0 | ĐẠT |
| Thẻ 114 giữ `pending` | ĐẠT |
| `href` của thẻ giữ rỗng | ĐẠT |
| Không xuất bản | ĐẠT |

## 6. Kiểm nghiệm 100+ Bài toán thực tế

Bài:

```text
content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd
```

| Tiêu chí | Kết quả |
|---|---|
| Có cấu hình dự án riêng | ĐẠT |
| Có hồ sơ sản xuất riêng | ĐẠT |
| Được nhận diện là `real_world_100` | ĐẠT |
| Được nhận diện là `real_world_problem` | ĐẠT |
| Kế hoạch chạy `real-world-problem` | ĐẠT |
| Dùng cùng validator lõi | ĐẠT |
| Không chứa `listing-order` | ĐẠT |
| Đủ bốn phần mô hình hóa bắt buộc | ĐẠT |
| HTML có lớp trang bắt buộc | ĐẠT |
| HTML có đúng một H1 | ĐẠT |
| HTML có liên kết PDF | ĐẠT |
| PDF được tạo và chuyển vào `docs` | ĐẠT |
| PDF Title đúng, A4, đường cơ sở 4 trang | ĐẠT |
| Trạng thái sản xuất là `in_production` | ĐẠT |
| Trạng thái xuất bản là `pending` | ĐẠT |
| Không xuất bản | ĐẠT |

Bài thử chỉ chứng minh đường ống kĩ thuật và ranh giới dự án; nó không tự động trở thành nội dung đã nghiệm thu để xuất bản.

## 7. Hồi quy đồng thời hai dự án

Đã chạy cùng một lệnh checker trên hai bài và nhận:

```text
AUTOMATED RESULT: PASS_WITH_WARNINGS | EXIT=0
```

Đã chạy cùng một lệnh render trên hai bài và nhận:

- Quarto thoát 0;
- lỗi render 0;
- cảnh báo Quarto 0 trong kiểm tra checker;
- source adapter đúng cho từng bài;
- render adapter đúng cho từng bài;
- PDF của cả hai bài được nhận diện;
- trạng thái xuất bản vẫn `pending`.

Các `WARN` còn lại là cổng kiểm định có người quan sát, đúng theo hợp đồng hệ thống.

## 8. Tài liệu

| Tiêu chí | Kết quả |
|---|---|
| Có điểm vào vận hành | ĐẠT — `README.md` |
| Có tài liệu kiến trúc | ĐẠT |
| Có hợp đồng lõi và dự án | ĐẠT |
| Có schema cấu hình | ĐẠT |
| Có vòng đời bài | ĐẠT |
| Có đường cơ sở hai dự án | ĐẠT |
| Có hướng dẫn thêm dự án | ĐẠT |
| Có hướng dẫn thêm validator | ĐẠT |
| Có hồ sơ chuyển đổi | ĐẠT |
| Có phân loại tài liệu lịch sử và vận hành | ĐẠT |

## 9. Vận hành phiên mới

Một phiên mới có thể:

1. đọc `AGENTS.md`;
2. đọc `README.md` của hệ thống;
3. tìm cấu hình dự án;
4. dùng loader để xác định loại bài;
5. tìm hồ sơ theo `by_article_stem`;
6. chạy `scope` hoặc `render`;
7. đọc trạng thái và cảnh báo;
8. chạy hồi quy hai dự án khi sửa lõi;
9. tiếp tục công việc mà không cần toàn bộ lịch sử hội thoại.

**Kết quả:** ĐẠT.

## 10. Hiệu quả

Đã chứng minh:

- không cần sao chép checker cho dự án mới;
- không cần sao chép toàn bộ quy chuẩn hàm số;
- dự án mới chủ yếu cần cấu hình, quy chuẩn, hồ sơ và adapter chuyên biệt;
- thay đổi lõi có đường hồi quy rõ;
- registry ngăn YAML biến thành ngôn ngữ thực thi;
- loại bỏ được 149 dòng đường tương thích sau khi native ổn định;
- tài liệu bền vững thay thế phần lớn ngữ cảnh hội thoại tạm thời.

## 11. Những gì phiên bản 1.0 chưa tuyên bố

Phiên bản 1.0 chưa tuyên bố:

- có một schema hồ sơ vật lí duy nhất cho mọi dự án;
- mọi mô-đun tùy chọn đều có dispatch độc lập;
- quy chuẩn nội dung bài toán thực tế đã hoàn chỉnh;
- bài taxi đã được nghiệm thu nội dung để xuất bản;
- hệ thống tự động hóa xuất bản;
- kiểm định tự động có thể thay thế người quan sát.

Các giới hạn này không làm sai mục tiêu phiên bản 1.0.

## 12. Điều kiện không đạt

Hệ thống sẽ mất trạng thái đạt nếu:

- một dự án hồi quy không còn được nhận diện;
- validator lõi không còn chạy cho cả hai dự án;
- adapter dự án chạy sai phạm vi;
- cấu hình có thể thực thi mã tùy ý;
- dự án mới phải mang trường chuyên biệt của dự án khác;
- giao diện checker bị phá vỡ không có đường di trú;
- bài hồi quy phải sửa để checker vượt qua;
- trạng thái nghiệm thu và xuất bản bị trộn;
- xuất bản có thể xảy ra không cần xác nhận;
- nhánh legacy được khôi phục mà không có nhiệm vụ riêng.

## 13. Quyết định phiên bản 1.0

Dựa trên bằng chứng M0–M9A, hệ thống đạt các điều kiện kiến trúc và kiểm định tự động của phiên bản 1.0.

Commit tài liệu M9B có ý nghĩa:

- khóa mô tả vận hành hiện tại;
- xác nhận schema cấu hình phiên bản 1;
- xác nhận checker 2.6.0 là đường cơ sở;
- xác nhận hai bài hồi quy;
- kết thúc giai đoạn chuyển đổi;
- không thay đổi trạng thái sản xuất hoặc xuất bản của từng bài.

## 14. Kết luận

Nghiệm thu hệ thống không dựa vào số lượng tệp hoặc độ dài checker.

Tiêu chí quyết định đã đạt là:

```text
một lõi rõ
+ hai dự án thực dùng được
+ hồi quy an toàn
+ cấu hình không thực thi mã
+ validator đúng phạm vi
+ quyền nghiệm thu và xuất bản thuộc người dùng
```
