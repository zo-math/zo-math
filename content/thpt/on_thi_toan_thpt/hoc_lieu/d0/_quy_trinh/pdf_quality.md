# PDF D0 — hồ sơ chất lượng trình bày, 14/10/2026

## Bản dựng chính thức sau duyệt mẫu

Mẫu 9 trang đã được chủ trì duyệt làm hướng dàn. Đường dựng hiện hành dùng
`d0_print.lua`/`d0_print_profile.json` và template D0 để chiếu đủ nội dung
QMD thành PDF. Mỗi bài/đối chiếu được giữ trọn trong một cụm; bản 20 trang
đã xem màu toàn trang. Hướng dẫn ghi nhận chuyển lên phần bắt đầu, đoạn
hướng dẫn lặp nguyên văn trong 24 lời giải được in một lần sau khi kiểm
trùng. Bảng dấu lấy JSON, hình học giữ vector và nhãn không bị phóng lớn.
Trang cuối có vùng học tiếp hai cột và khung Ủng hộ từ component HTML.

Checker `kiem_chung_pdf.py` lưu trạng thái máy ở `pdf_review.json`. Kiểm
ảnh nhận diện cặp số đường ngang/dọc của cùng bảng, kể cả ca âm xóa một
đường. Chưa có bằng chứng in giấy hoặc quét QR vật lý; không tự suy nghiệm
thu toàn bộ PDF hay xuất bản từ việc dựng/kiểm đạt.

## PDF-D0-01 — lưới bảng và bảng dấu cũ

Triệu chứng: viền trên bảng hai chiều (tiêu đề ô góc trống) mất trong PDF
đầu; bảng dấu BBT01 nhập vector cũ nền vàng/bo góc, không nhất quán.
Phạm vi: PDF D0; không suy lỗi này thành mọi bảng của website.

Nguồn đã xác minh: `d0_pdf.lua` dựng longtable với rowcolor/hline cho
header; lớp tô nền đi cùng đường kẻ làm viền trên không hiện trong đầu ra.
Nhánh LaTeX của variation dùng trực tiếp `hinh/bbt01.pdf` lịch sử.
Sửa: bỏ phủ nền header, dùng lưới .5 pt; d0.lua đọc JSON dựng bảng dấu
native trong nhánh LaTeX, giữ nhánh HTML và dữ kiện toán.

Guard: kiểm trên ảnh Poppler, đếm đủ các đường ngang và đường dọc xuyên
suốt bảng; cả bảng góc trống, bảng thống kê, bảng dấu, bảng tối ưu và bảng
mô tả. Checker từ chối XObject bảng dấu cũ, bảo toàn nguồn và kiểm input
fingerprint. Ca bảng tiếp trang được yêu cầu trong hướng dẫn; D0 hiện
không có bảng tiếp trang để chứng nhận ca đó.

## PDF-D0-02 — thông tin ấn bản và trang kết

Bìa thiếu ngày/bản quyền; cuối có bản quyền nhưng thiếu logo và tài khoản.
Nguyên nhân: template không khai các trường này, chỉ có liên kết Bảo trợ.
Builder đọc nguồn Bảo trợ hiện hành và sinh metadata vào cây dựng cô lập;
template thêm logo, ngày/phiên bản/bản quyền, QR có nhãn và dữ liệu chữ.
Guard kiểm trường hiển thị trên bìa/kết và hash nguồn Bảo trợ/QR.

## Phân trang và kiểm

Nguồn ép ngắt mọi section nên trang mục lục khảo sát gần rỗng; adapter
giữ các mạch ở trang mới, ghép mục lục này với cuối phần hướng dẫn.
Tham chiếu trang chỉ bổ sung cho liên kết đề/đối chiếu, tránh làm dài mọi
link trong đoạn văn. R8-03 tách ở ranh giới bài để không đẩy hai dòng cuối
sang trang nhận xét. Không rút gọn câu chữ hay sửa toán để vừa bố cục.

Bằng chứng máy hiện hành ở `pdf_review.json`/`pdf_build.json`; ảnh tạm của
vòng DH_042 đã được dọn sau khi dựng bản đầy đủ. Đã sửa không đồng nghĩa được chủ trì duyệt hoặc
phát hành. Trạng thái cuối và giới hạn kiểm ghi theo kiểm thực tế ở 03.
