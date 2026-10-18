# Sáu HTML từ nguồn hiện hành — 18/10/2026

[Mở bộ xem mới](http://127.0.0.1:8877/_audit/html_current_six_20261018/index.html).

- HTML tại `E:\zo_math\_audit\html_current_six_20261018\html`; trang đầu `index.html` ở thư mục cha. Mở lại sau reboot bằng `Mo_ban_xem_HTML.cmd` cùng thư mục trang đầu, dùng công cụ canonical kiểm HTTP đúng tệp trên cổng 8877.
- Dựng mới sáu trang Khóa 2027, Khảo sát đầu vào, Đơn điệu và cực trị, Giá trị lớn nhất và giá trị nhỏ nhất, Đường tiệm cận, Khảo sát sự biến thiên và vẽ đồ thị của hàm số từ nguồn hiện hành tại checkpoint `2562f4bc`. Dùng launcher và QMD `render --html-only`; trang khóa dùng Quarto `--to html`. Profile `on-thi-preview`, giữ G04 là bản thảo. Bìa D0 dùng cơ chế xem trước đã có; không thay trạng thái duyệt ảnh.
- Nguồn cách ly tại `.quarto/html_current_six_20261018`, lấy từ nguồn chính thức, không lấy HTML lịch sử để sinh sáu trang. Các trang thông tin phụ và tài nguyên liên kết được chép nguyên trạng từ thành phẩm hiện có để giữ đường dẫn; không chứng nhận đã dựng lại các trang phụ.
- Khi kiểm Home, phát hiện tóm tắt tiệm cận chứa mã LaTeX trong component HTML thô. Đổi hai ký hiệu thành lời “âm vô cực”, “dương vô cực”, giữ nghĩa; sửa YAML rồi sinh lại đúng `home_catalog.qmd`. Cổng Home bổ sung chặn TeX lộ trong câu giới thiệu. Cập nhật đúng hai binding nguồn đã đối chiếu; không nâng trạng thái duyệt. Phép kiểm quay lại bài cũng đồng bộ câu văn hiện hành đã được duyệt, không dùng câu cũ để báo sai.

## Kết quả và giới hạn

- Toàn bộ sáu HTML: 3767/3767; Home: 113/113, gồm ca âm lộ TeX; D0: 186/186. Không thiếu tài nguyên hoặc đích fragment trong sáu trang.
- Trình duyệt 1440/390 px: 256/256 sau đối chiếu phạm vi. Báo ban đầu 253/256 giữ nguyên; ba báo lệch trục đều là tiêu đề vùng Bảo trợ G02 hai cột có logo. Kiểm lại đúng ba view với phép đo trục giới hạn vào nội dung bài đạt 22/22; không sửa sản phẩm để ép vùng Bảo trợ về giấy bài học. Menu sáu trang, ảnh, bảng, drawer mobile và các vòng Xem lời giải/Xem đề bài Khởi động hoạt động.
- Đã tự xem ảnh chụp Bắt đầu G01, Bài học G03, Bài học G04 trên mobile và Khảo sát D0. Đây là kiểm kỹ thuật và quan sát của agent, chưa phải chủ trì nghiệm thu.
- 2434 tệp được bảo vệ (PDF, hình, website đã xuất bản, các bộ xem trước) giữ nguyên. HEAD và staging không đổi. Chưa dựng lại PDF học liệu hoặc hình, chưa commit/push/xuất bản; tài nguyên sẵn có được tái sử dụng.
- Bằng chứng: `_audit/html_current_six_20261018/final.json`, `source-manifest.json`, `render-results.json`, log dựng Home cuối `home-render-eol.log`, `qa-static.json`, `qa-home-final.json`, `qa-d0-final.json`, `qa-browser.json`, `qa-browser-axis.json`, `home-render-copy-fix.json`, `screenshots/`. Manifest ghi đầu vào dựng; hồ sơ này và trạng thái 03 được ghi sau QA.

Trạng thái: HTML đã dựng và kiểm kỹ thuật, chờ chủ trì xem/duyệt. Bìa thành phẩm D0 vẫn chờ duyệt; PDF giữ nguyên và có thể chưa đồng bộ với nguồn mới.

## Lưu mốc theo yêu cầu chủ trì

Nguồn sửa nhỏ Home và cổng kiểm đã commit tại a9d8a119. Hồ sơ này và trạng thái điều hành được commit riêng sau đó. Các ghi nhận chưa commit ở trên mô tả thời điểm dựng; không thay bằng chứng lịch sử hoặc trạng thái chờ duyệt. Không dựng thêm HTML/PDF, không push hoặc xuất bản trong lượt lưu mốc.
