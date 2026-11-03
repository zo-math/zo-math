# Dựng HTML khóa 2027 từ nguồn chính

Nguồn biên tập và vận hành duy nhất là repository `E:\zo_math`. Không có bản R01 riêng hoặc prototype trong vòng vận hành. Không đọc `inputs/material`, `preview` hay `_audit` làm đầu vào dựng. Các module native mà CLI hiện hành gọi là thành phần nguồn đang hoạt động; chúng không phải phương án khôi phục website cũ.

## Nguồn nào sở hữu phần nào

| Phần | Nguồn hiện hành |
|---|---|
| Nội dung toán, điều kiện, câu hỏi, lời giải, Nhật kí, ID của từng gói và D0 | `content/thpt/on_thi_toan_thpt/hoc_lieu/**/index.qmd` và các include được khai báo |
| Trang Nhà: lời giới thiệu, hình, phạm vi, lộ trình, dịch vụ, FAQ, bảo trợ | `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.qmd` |
| Danh mục đầy đủ, tóm tắt gói, tám mạch và mô tả, mốc thi tham khảo | `2027/_data/chuong_trinh.yml`; metadata QMD và bìa có binding riêng |
| Ba thành phần dữ liệu trang Nhà | `zo_build_on_thi.py` sinh từ những nguồn trên; không sửa `_partials` bằng tay |
| Giới thiệu Tổng quan và hướng dẫn học r20 | `scripts/zo_course_site_sources/overview_content.py`, `guidance_content.py`, `learning_pages.py`; mục tiêu/toán trong Tổng quan lấy từ HTML vừa dựng của QMD |
| Giao diện, điều hướng và tài nguyên r20 chính | `scripts/zo_course_site_sources/`; `build.py` chỉ ghép bố cục, không thay nội dung toán |
| Nối nguồn → HTML chính, kiểm bảo toàn và liên kết | `scripts/zo_course_site.py`; được `zo_qmd.py` gọi sau kiểm định nguồn và HTML native thành công |
| Trạng thái công việc và bước tiếp theo | `03_dieu_hanh_chuong_trinh.md`; biên nhận xây dựng không tự cấp nghiệm thu |

## Dựng và kiểm

Luôn chạy từ gốc repository, qua launcher:

```text
python scripts/zo_python.py scripts/zo_course_site.py build --report _audit/current/verification/course-render.json
python scripts/zo_python.py scripts/zo_course_site.py check --report _audit/current/verification/course-check.json
```

Lệnh toàn khóa dựng D0, bảy gói, Nhà và Ôn nền dùng chung; sinh bảy trang tiện ích/hướng dẫn. Tất cả ghi vào vị trí canonical trong `docs/`; chỉ dựng HTML. Lệnh `zo_web_2027_bundle.py build/check` chuyển vào cùng đường này, không dùng bộ sáu trang/PDF cũ.

Để sửa riêng một gói, dùng `zo_qmd.py render <đường_dẫn_index.qmd> --html-only --report <báo_cáo_mới>`: kiểm nguồn và HTML native vẫn chạy trước lớp r20. Nếu đổi nguồn giao diện dùng chung hoặc danh mục, dựng lại toàn khóa. Lệnh Quarto thô là tầng trung gian, không phải điểm bàn giao website cuối.

`current_site_build.json` trong hồ sơ khóa ghi nguồn/đầu ra hiện hành và kiểm độ mới; đây là tệp sinh, không là biên nhận nghiệm thu. Không chỉnh hash trong hồ sơ lịch sử. Báo cáo `_audit` chỉ lưu kiểm chứng. Khi thêm gói mới, khai báo trong danh mục và bindings điều hướng/Tổng quan rồi kiểm lại đường dựng; không sao HTML cũ.

`zo_course_site_dependencies.py` theo dõi cả module dựng/kiểm được import, cấu hình Quarto, CSS/JS, mẫu Bảo trợ, màu, phông, logo, analytics và tài sản thuộc nguồn học liệu. Kiểm độ mới so cả tập tệp và hash, nhận biết tệp thêm/xóa. Chạy `zo_course_site_dependencies_selftest.py` qua launcher khi sửa cơ chế này. Manifest `2027/_quy_trinh/ban_dang_duyet.json` bảo vệ toàn bộ đầu ra và nguồn hiện hành, không kế thừa trạng thái duyệt của bản cũ.

Bảng biến thiên được kiểm bằng `du_lieu/bang_bien_thien.json` và hợp đồng ngữ nghĩa `_quy_trinh/hop_dong_bang_bien_thien.json`, không đọc bản thảo đã nghỉ dùng. Hợp đồng giữ giới hạn, chiều biến thiên, điểm loại trừ và dữ kiện đạo hàm đã xác nhận. Khi chủ trì duyệt thay đổi toán học, cập nhật hợp đồng theo quyết định ấy; không sửa hash để che một phép kiểm thất bại. Bộ hồi quy `zo_course_math_assets.py --self-test` phải tiếp tục bắt được các trường hợp sửa sai dữ kiện.

## Giới hạn và kiểm giao diện

D0 là khảo sát độc lập, không áp chu trình Kiểm tra của gói. PDF được giữ nguyên và có thông báo chưa đồng bộ; muốn dựng PDF cần nhiệm vụ riêng. Dựng HTML không commit, push hoặc xuất bản. Trước bàn giao localhost vẫn dùng prepare → quan sát trong trình duyệt ứng dụng → confirm → check theo quy trình chung.

Kiểm ít nhất: danh mục đủ D0 và bảy gói (R2-G02 có thẻ/lọc/điều hướng), Tổng quan, từng lượt Ôn lại, đáp án đóng, chặn mở hỗ trợ trong lượt Kiểm tra, quay lại vị trí gốc, Đã lưu và bố cục rộng/hẹp. Kiểm máy không thay quan sát hay nghiệm thu chủ trì.
