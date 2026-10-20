# Tích hợp R1-G05 vào khóa 2027 — ngày 21/10/2026

Tám PDF hiện hành đã được chủ trì duyệt, khóa đúng hash tại [biên nhận](duyet_bo_pdf_20261021.json). Lượt này không dựng PDF, không commit, push, prepare xuất bản hoặc phát hành. HTML tích hợp đang chờ chủ trì xem.

## Kết quả

- Danh mục canonical thêm G05 sau G04, dùng bìa riêng đã khai báo của G05 và mô tả đúng phạm vi đã duyệt; trạng thái hiển thị Bản xem trước không thay nghiệm thu.
- Menu dùng cùng bảy đích trên Nhà, D0 và G01–G05. Bộ dựng toàn khóa lấy danh sách từ cùng binding, không giữ danh sách sáu trang thứ hai.
- Chính văn QMD của cả bảy trang giữ nguyên byte. D0 giữ toàn bộ nội dung khảo sát/định vị; mở G05 qua menu và Nhà. 41 PDF học liệu và mọi PDF provenance/receipt giữ nguyên.
- Nhà đạt 116/116; G05 đạt 1954/1954; D0 đạt 240/240; nguồn điều hướng 1728/1728; đối chiếu tích hợp 95/95, không hỏng liên kết/tệp/anchor. D0 giữ đủ nội dung đã duyệt và có ca âm chống sai hash PDF, sai đường dẫn hoặc gán CURRENT cho đầu vào cũ.
- Mở menu trên bảy trang ở khung rộng (1440 px, riêng một lượt G05 1309 px) và 390 px: đủ bảy đích, không tràn ngang toàn trang. Thử tìm G05, mở nút từ thẻ tới Bắt đầu, thẻ tải trên điện thoại và Escape trả focus. Bàn giao mới quan sát thật Nhà/D0/G05 và đối chiếu HTTP đúng hash 278 tệp.

## PDF cũ và giới hạn

[Khảo sát 33 PDF cũ](../../../../tot_nghiep_thpt/2027/_quy_trinh/tinh_trang_bao_tro_33_pdf_20261021.md): 9 có Bảo trợ ở trang cuối, 24 bản chức năng chưa có. Không sửa tệp hoặc biên nhận PDF lịch sử.

Cổng CURRENT phản ánh đầu vào hiện hành, khác với tệp cũ đã được duyệt. D0 có hai đầu vào giao diện chung đã đổi trước lượt này; R1 cũ cũng chưa được dựng bằng pipeline mới. HTML giữ đúng tệp cũ và ghi rõ chưa đồng bộ, không thay hash để cấp CURRENT. Bộ PDF G05 vẫn CURRENT đủ tám bản. Chưa chạy lại bộ dựng toàn khóa có hợp đồng PDF CURRENT; lượt này dựng HTML từng trang qua cửa canonical và kiểm bộ kết quả, không nới cổng PDF.

Việc kiểm Bảo trợ gồm đọc văn bản mọi trang và quan sát đủ 33 trang cuối, không là rà lại toàn văn hoặc xác nhận in giấy/quét QR. Kiểm trình duyệt lấy mẫu phần tích hợp; không thay nghiệm thu chủ trì.

## Nguồn, cơ chế và bằng chứng

Nguồn danh mục ở `_data/chuong_trinh.yml`; component Home lấy bìa từ khai báo của từng gói. Binding menu ở `scripts/zo_web_2027_navigation.py`; cluster/bundle dùng lại danh sách ấy. D0 kiểm đúng byte PDF so biên nhận gốc, phân biệt tệp giữ lại với đầu vào CURRENT và vẫn chặn PDF bị đổi hoặc đường dẫn không an toàn. Không sửa tay HTML/PDF/SVG.

Danh mục tệp sửa, hash trước/sau và kết quả ở [báo cáo máy đọc](tich_hop_khoa_20261021.json). Audit `_audit/g05_integration_20261021/` chỉ giữ bằng chứng: kiểm nguồn/render/DOM, ảnh trình duyệt, trang cuối PDF và bảo toàn. Bản thảo, hình chính thức G05, nguồn chính văn, PDF và vùng staged được bảo toàn; HEAD không đổi. Byte thô index Git có thể đổi do stat-cache khi đọc trạng thái; vùng staged vẫn rỗng, không chạy lệnh stage/commit.

Nguồn chính thức và HTML hiện hành ở vị trí chuẩn, không phụ thuộc audit để dựng. Trạng thái/bước tiếp theo chỉ do bản điều hành 03 sở hữu.
