# Dựng lại sáu trang HTML — 18/10/2026

Bản xem thực tế: [mở Nhà, Khảo sát đầu vào và bốn bài hiện có](http://127.0.0.1:8877/_audit/html_refresh_20261018/index.html). Các trang lưu tại `E:\zo_math\_audit\html_refresh_20261018\html`; mỗi trang giữ đường dẫn chuyên mục nên liên kết hỗ trợ liên học liệu tới đúng trang mới.

Đã dựng HTML từ mốc `ff12e7c4b9373d71d830ce7570290ce9496c85c5` và các sửa nguồn có căn cứ phát hiện khi dựng/kiểm. Bộ nguồn cách ly ở `E:\zo_math\.quarto\html_refresh_20261018`; các lớp sửa được ghi hash riêng trong hồ sơ JSON cùng tên. Không dùng HTML cũ hoặc báo cáo PASS cũ làm đầu vào dựng hay thay việc đọc sản phẩm.

## Các lỗi khép khi dựng và kiểm thật

- Hồ sơ bố cục Đơn điệu và cực trị còn dấu kiểm JS cũ: đồng bộ đúng hai binding runtime, giữ nội dung/layout/ảnh bìa và biên nhận nghiệm thu lịch sử. Thêm cổng kiểm ngay ở nguồn QMD và gate điều hướng; thử âm bằng dấu kiểm cũ.
- Danh mục Nhà có Đường tiệm cận nhưng thiếu khai báo bản xem trong khi nguồn mới đang sửa: khai rõ preview như hai bài đầu và dùng bộ sinh cập nhật đúng một include QMD. Không đổi profile nghiệm thu hoặc nâng trạng thái phát hành. Gate chung kiểm mô hình và các nguồn sinh, chặn thiếu khai báo hoặc include cũ.
- Bộ kiểm D0 còn giả định bảng là ảnh SVG và ràng buộc trạng thái duyệt cũ: kiểm đúng một bảng dấu native với dữ liệu JSON và một hình hình học canonical; so đầy đủ nội dung/TeX với biên nhận bất biến và so phép chiếu với markup Quarto tươi. Thử âm đổi dữ liệu native phải bị chặn. Giữ nguyên checker và receipt lịch sử.
- Đường tiệm cận: đích lời giải là section, còn details là con. Mã cũ chỉ mở ancestor nên hộp vẫn đóng, không bấm được lượt về bằng thao tác thật. Controller nay mở duy nhất hộp lời giải thuộc nhiệm vụ được gọi; giữ nhóm/đáp án khác đóng. Đồng bộ ràng buộc JS và dùng bộ materialize hiện hành cập nhật tám bản tài nguyên trong mirror/bộ xem; không sửa tay nội dung HTML hoặc dựng lại toàn bộ bài vì đổi JS. Bốn fixture ownership mới được giữ trong bộ hồi quy nguồn.

## Phạm vi kiểm và kết quả

- Kiểm HTML: 8321/8321; đủ sáu đích trong mục lục, cặp đề–lời giải theo ownership và nhãn chuẩn, bảng/chú thích, neo và liên kết thật của bộ xem.
- Trình duyệt: 228/228; Edge ở 1440/430/390 px, thao tác chuột vào vùng chữ thật, bàn phím, đi–về của bốn bài, G04 qua G03 và G02 rồi về đúng lượt Ôn lại, Back/tải lại/hai tab, drawer D0 và trang không JavaScript.
- Đã xem ảnh chụp đại diện: bảng G04 desktop, bảng G02 mobile, bìa G03 mobile, D0 không JavaScript và nhánh nền ngoại gói. Bảng toán dùng cùng nền/nét và cỡ/khoảng đệm theo em của chữ xung quanh; không ép mọi ngữ cảnh thành cùng số px. 55 bảng toán và 63 đồ thị R1 được kiểm theo vai trò; logo/QR không tính là đồ thị.
- Cổng nguồn cuối: 1397/1397; hồi quy định tuyến 28/28, ràng buộc runtime 6/6, danh mục 3/3. Bản HTML giữ đủ các thay đổi trước: nhãn thao tác, vị trí tên bảng/hình và bỏ dòng dưới bìa.
- 1727 tệp thành phẩm/tài nguyên/bản thảo/bằng chứng duyệt được bảo toàn theo hash. QMD nội dung không bị biên tập trong lượt dựng này. PDF học liệu, bìa, SVG/TEX canonical và thành phẩm công khai giữ nguyên.

Các log lần dựng/kiểm chưa đạt được giữ trong hồ sơ audit, cùng nguyên nhân và sửa tương ứng. Lỗi ban đầu của bộ bấm ở giữa khung bao liên kết nhiều dòng được sửa bằng client rectangle nhìn thấy; kiểm spacing chuyển từ px tuyệt đối sang em đúng quy chuẩn. Đây là sửa phép đo, không sửa dữ liệu học liệu để đạt PASS. Lỗi lời giải G03 là lỗi sản phẩm thật và đã sửa nguồn, có hồi quy.

## Nơi lưu và trạng thái

Bằng chứng: `E:\zo_math\_audit\html_refresh_20261018`; `qa-static.json`, `qa-browser.json`, `preflight-final/qa-source.json`, `qa-route-regression.json`, `qa-runtime-binding-fix.json`, `qa-catalog-regression.json`, `qa-runtime-asset-refresh.json`, `qa-preservation.json`, các render log và ảnh chụp trong `screenshots/`.

Nguồn sửa phát sinh được liệt kê bằng hash trong [hồ sơ JSON](ho_so_dung_lai_html_20261018.json); quy trình/gate ở 02, hành vi mở đúng hộp ở 07, trạng thái duy nhất ở 03. HTML đã dựng và kiểm kỹ thuật; còn chờ chủ trì duyệt. Chưa commit các sửa phát sinh, chưa push hoặc xuất bản; `_audit/` và `.quarto/` vẫn ngoài Git.

Giới hạn: chưa kiểm Safari/Firefox, thiết bị cảm ứng thật hoặc trình đọc màn hình; không thay việc nghiệm thu nội dung toán. G02 dựng lại bốn cặp SVG/PDF vector trung gian trong mirror do dependency cache của adapter; không dựng PDF học liệu và không thay tài nguyên canonical. Các liên kết chân trang ngoài phạm vi sáu trang trỏ tới HTML công khai đang có, không dựng lại toàn website.
