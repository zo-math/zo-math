# Dựng HTML khóa 2027 từ nguồn chính

## Đường vận hành duy nhất của website

### Cập nhật thông thường: ghi đè bản hiện hành

**Phát hành tuyệt đối không dựng lại.** Khi yêu cầu chỉ là phát hành, bỏ
toàn bộ bước dựng: chỉ lấy các tài nguyên liên quan đang có để đưa lên.
Dựng HTML, PDF, hình và các tài nguyên thuộc công việc dựng tài liệu riêng.
Nếu tài nguyên cần phát hành chưa tồn tại thì báo đúng phần thiếu, không
tự gọi bộ dựng để bổ sung trong nhiệm vụ phát hành. `prepare --page <HTML>`
cũng chỉ nhận đầu ra có sẵn, không render và không cần Quarto.

Theo chỉ thị chủ trì ngày 05/11/2026, chỉ vận hành một bản website hiện hành.
Sửa nguồn → dựng đúng trang chịu ảnh hưởng, ghi đè HTML ở `docs/` → khi được
giao cập nhật website, đưa phần thay đổi lên đúng địa chỉ cũ. Không tạo bản
song song, không dựng lại toàn khóa cho một sửa nhỏ, không mở lại nghiệm thu
nội dung hay dựng PDF chỉ để cập nhật HTML.

Đường phát hành HTML mặc định là `zo_publish.py prepare --course-html`, rồi
`zo_publish.py publish`, đều qua `scripts/zo_python.py`. Bước prepare lấy bản
HTML đã dựng; không render, không cần biên nhận duyệt theo ngày. Công cụ tự
ghi thông tin cần dùng trong lần cập nhật, chỉ ghi đè các tệp có byte thay đổi,
giữ PDF public và trang ngoài khóa nguyên trạng. Bản sao khôi phục chỉ là tạm
trong lúc cập nhật và được dọn khi xong; không là một phiên bản website khác.

Agent tự làm chuỗi commit nguồn → push nguồn vào `zo-math/zo-math` → prepare
→ publish khi người dùng yêu cầu đưa thay đổi lên zomath.vn. Không xin lại
quyền cho từng bước kỹ thuật đã nằm trong yêu cầu đó. Sau push website, theo
dõi kết quả triển khai; lỗi GitHub Pages là lỗi triển khai cần xử lý riêng,
không bắt người dùng duyệt hoặc dựng lại học liệu.

Các đường `--current-course`, `--approved-course`, `--existing-course` giữ để
đọc/tái kiểm hồ sơ cũ hoặc tác vụ có phạm vi riêng; không phải đường mặc định
cho cập nhật HTML thông thường. PDF mới/thay đổi chỉ đưa lên khi nhiệm vụ có
yêu cầu PDF; trạng thái hồ sơ PDF cục bộ không chặn cập nhật riêng HTML.

Tài liệu này sở hữu toàn bộ lệnh dựng, kiểm và cập nhật website khóa 2027. Các lệnh Quarto trực tiếp, bộ preview, checkpoint và shell kit cũ trong tài liệu khác đã hết hiệu lực đối với giao diện cuối. Chúng chỉ được gọi nội bộ khi bộ dựng hiện hành cần tạo nội dung native; không chạy chúng để ghi hoặc bàn giao website. Chỉ giữ nguồn nội dung và các hợp đồng toán/học tập còn hiệu lực, không kế thừa bố cục từ bản dựng cũ.

Giao diện nằm trong thư mục này: `build.py` ghép trang; `site.css` là lớp cơ sở; `course-redesign.css` ghi đè giao diện toàn khóa; `learning-redesign.css` và `learning-format.css` áp cho trang học. Khi sửa CSS, phải kiểm thứ tự nạp và giá trị computed trên bản cuối. Không sửa kit `_design/web_2027_mau_dung_chung` để chỉnh header website mới.

Vận hành từ gốc repo qua `scripts/zo_python.py`: `zo_course_site.py plan` để xác định phạm vi; `build --page <QMD>` để dựng trang cụ thể; `check --page <QMD>` để kiểm kết quả. `zo_qmd.py render <QMD> --html-only` là cửa vào tương đương, có gọi lớp website cuối. `build --all` chỉ dùng cho nhiệm vụ toàn khóa. `assets` chỉ dùng với thay đổi được cổng tài nguyên chấp nhận; không gọi riêng `install_assets()` để bỏ qua hồ sơ độ mới và bảo vệ. Mở HTML đã dựng bằng `zo_html_preview.py`, bàn giao theo `zo_html_handoff.py`; không chạy Quarto preview để thay bản website.

Nguồn biên tập và vận hành duy nhất là repository `E:\zo_math`. Không có bản R01 riêng hoặc prototype trong vòng vận hành. Không đọc `inputs/material`, `preview` hay `_audit` làm đầu vào dựng. Các module native mà CLI hiện hành gọi là thành phần nguồn đang hoạt động; chúng không phải phương án khôi phục website cũ.

## Quản lí minh họa thẻ

Danh mục phiên bản và quy cách xuất ảnh tại `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_data/minh_hoa_chuyen_de.json`. Nguồn ảnh thuộc `hinh/minh_hoa_chuyen_de_vN/` của từng gói; ảnh gốc đã chốt được bảo vệ bằng hash. Xem `illustrations/README.md` và dùng `scripts/zo_topic_art.py build/check` qua launcher cho năm tỉ lệ. Bộ dựng thẻ đọc danh mục này, không hard-code danh sách ảnh theo gói và không thay binding bìa học liệu/PDF. HTML hiện tại tiếp tục dùng nguyên byte ảnh gốc được duyệt; các bản xuất kích thước được quản lí riêng.

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
python scripts/zo_python.py scripts/zo_course_site.py build --page <QMD>
python scripts/zo_python.py scripts/zo_publish.py prepare --course-html
python scripts/zo_python.py scripts/zo_publish.py publish
```

Lệnh toàn khóa dựng D0, bảy gói, Nhà và Ôn nền dùng chung; sinh bảy trang tiện ích/hướng dẫn. Tất cả ghi vào vị trí canonical trong `docs/`; chỉ dựng HTML. Lệnh `zo_web_2027_bundle.py build/check` chuyển vào cùng đường này, không dùng bộ sáu trang/PDF cũ.

Để sửa riêng một gói, dùng `zo_qmd.py render <đường_dẫn_index.qmd> --html-only --report <báo_cáo_mới>`: kiểm nguồn và HTML native vẫn chạy trước lớp r20. Không tự mở rộng phạm vi khi tệp dùng chung đổi. `plan` báo từng trang còn cần cập nhật; đổi cấu hình bảng riêng hoặc metadata nội bộ chỉ tính cho trang sở hữu. Thay đổi thật sự dùng chung có thể làm nhiều trang chưa cập nhật, nhưng không chặn dựng trang được yêu cầu và không chứng nhận các trang còn lại. Lệnh `build` phải có `--page <QMD>` hoặc `--all`; chỉ dùng `--all` khi được giao rõ phạm vi toàn khóa. Lệnh Quarto thô là tầng trung gian, không phải điểm bàn giao website cuối.

`current_site_build.json` trong hồ sơ khóa ghi nguồn/đầu ra hiện hành và kiểm độ mới; đây là tệp sinh, không là biên nhận nghiệm thu. Không chỉnh hash trong hồ sơ lịch sử. Báo cáo `_audit` chỉ lưu kiểm chứng. Khi thêm gói mới, khai báo trong danh mục và bindings điều hướng/Tổng quan rồi kiểm lại đường dựng; không sao HTML cũ.

`zo_course_site_dependencies.py` theo dõi cả module dựng/kiểm được import, cấu hình Quarto, CSS/JS, mẫu Bảo trợ, màu, phông, logo, analytics và tài sản thuộc nguồn học liệu. Kiểm độ mới theo `page_inputs` riêng cho từng đầu ra, nhận biết tệp thêm/sửa/xóa; bảng tách phần dùng chung và cấu hình từng gói. Hồ sơ cũ được đọc bảo thủ, không gán dấu kiểm mới cho trang chưa dựng. `check --page <QMD>` chỉ kiểm trang được chọn; `plan` liệt kê trang còn cần cập nhật mà không dựng HTML. Một lượt dựng gói không ghi lại bảy trang tiện ích. Chạy thêm `zo_course_site_scope_selftest.py` khi sửa cơ chế phạm vi. Chạy `zo_course_site_dependencies_selftest.py` qua launcher khi sửa cơ chế này. Manifest `2027/_quy_trinh/ban_dang_duyet.json` bảo vệ toàn bộ đầu ra và nguồn hiện hành, không kế thừa trạng thái duyệt của bản cũ.

Bảng biến thiên được kiểm bằng `du_lieu/bang_bien_thien.json` và hợp đồng ngữ nghĩa `_quy_trinh/hop_dong_bang_bien_thien.json`, không đọc bản thảo đã nghỉ dùng. Hợp đồng giữ giới hạn, chiều biến thiên, điểm loại trừ và dữ kiện đạo hàm đã xác nhận. Khi chủ trì duyệt thay đổi toán học, cập nhật hợp đồng theo quyết định ấy; không sửa hash để che một phép kiểm thất bại. Bộ hồi quy `zo_course_math_assets.py --self-test` phải tiếp tục bắt được các trường hợp sửa sai dữ kiện.

## Giới hạn và kiểm giao diện

D0 là khảo sát độc lập, không áp chu trình Kiểm tra của gói. PDF được dựng riêng theo từng biến thể và có provenance hiện hành; lớp HTML kế thừa trạng thái thật của từng bản tải. Không dựng PDF lại khi chỉ sửa HTML. Đợt phát hành hiện hành đã được giao dựng lại 49 PDF; quyền này không tự áp dụng cho các nhiệm vụ sau. Dựng HTML không commit, push hoặc xuất bản. Trước bàn giao localhost vẫn dùng prepare → quan sát trong trình duyệt ứng dụng → confirm → check theo quy trình chung.

Kiểm ít nhất: danh mục đủ D0 và bảy gói (R2-G02 có thẻ/lọc/điều hướng), Tổng quan, từng lượt Ôn lại, đáp án đóng, chặn mở hỗ trợ trong lượt Kiểm tra, quay lại vị trí gốc, Đã lưu và bố cục rộng/hẹp. Kiểm máy không thay quan sát hay nghiệm thu chủ trì.
