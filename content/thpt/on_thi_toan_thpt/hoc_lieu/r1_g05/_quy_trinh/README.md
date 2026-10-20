# R1-G05 — Ứng dụng đạo hàm trong thực tiễn

- [Bộ tám PDF và mục tải HTML — hồ sơ kiểm khi bàn giao](ho_so/bo_pdf_va_muc_tai_20261021.md) · [Biên nhận duyệt toàn văn](ho_so/duyet_pdf_toan_van_20261021.json).
- [Lần sửa HTML hiện hành: nguồn và căn giữa công thức](ho_so/sua_chu_thich_va_can_giua_20261021.md).
- [Hồ sơ tích hợp trang khóa học và kiểm HTML](ho_so/tich_hop_khoa_20261021.md).
- [Nghiệm thu bộ HTML tích hợp và quyền commit cục bộ](ho_so/nghiem_thu_html_tich_hop_20261021.json).
- [Phát hành zomath.vn — bảy HTML và tám PDF G05, giữ nguyên 33 PDF cũ](ho_so/phat_hanh_zomath_20261021.json).
- [Nguồn QMD hiện hành](../index.qmd).
- [Bản HTML đã nghiệm thu](http://127.0.0.1:8877/docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g05/index.html).
- [Hồ sơ chuyển QMD, tài nguyên và kiểm HTML](ho_so/chuyen_qmd_html_20261021.md).
- [Bản thảo đã duyệt, giữ nguyên để đối chiếu](ban_thao/noi_dung.md).
- [Hồ sơ phạm vi](../../../tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G05.md).
- [Đối chiếu bản thảo](ho_so/doi_chieu_va_kiem.md) · [Hướng bìa đã duyệt](ho_so/huong_bia.md) · [Biên nhận duyệt đúng bản](ho_so/duyet_ban_thao_va_huong_bia_20261020.json).

Bản thảo, hướng bìa, hình minh họa và phần sửa HTML đã được duyệt. Chủ trì tiếp tục duyệt toàn văn 38 trang và giao sinh các bản theo chức năng, tích hợp tải vào HTML. Đã hoàn thành tám PDF (128 trang), mọi bản có Bảo trợ cuối tài liệu và đã kiểm CURRENT; HTML mới có tám thẻ tải đúng số trang và tệp thật. Cả tám PDF hiện hành đã được chủ trì duyệt theo [biên nhận đúng hash](ho_so/duyet_bo_pdf_20261021.json). Chủ trì đã nghiệm thu bộ HTML tích hợp, sau đó cho phép push và phát hành. Bộ đã triển khai thành công trên zomath.vn ngày 21/10/2026; hash trực tuyến 278/278 tệp khớp biên nhận phát hành. 33 PDF cũ và cả tám PDF G05 được giữ nguyên byte. Nguồn biên tập là `index.qmd`; bản thảo đóng băng làm đối chiếu. Việc hiện hành chỉ do [03](../../../tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md) sở hữu.

Nguồn hình chính thức là `du_lieu/minh_hoa.json` và `_quy_trinh/sinh_hinh.py`; đầu ra chuẩn ở `hinh/`, provenance ở `giao_dien/minh_hoa_manifest.json`. Dùng adapter ZO Math để tìm `E:/zo_math_graphics`, lấy quy chuẩn màu và phông tại đó. Năm hình bối cảnh và bìa được sinh bằng hình học tham số, SVG vector và PNG; không phụ thuộc vùng bản thảo hoặc `_audit/`. Cơ chế đường đo có kiểm chân đường dóng, đầu mút, hướng và vạch giới hạn; quầy kiểm phối cảnh mui–bàn và kết nối cột. Tái sử dụng được các hàm hình chiếu/đường đo và cảnh có cùng cấu trúc; đây chưa là bộ sinh mọi bối cảnh hình học.

Khi cần sửa: sửa QMD, dữ liệu hoặc mã sinh → dựng → kiểm → sửa nguồn rồi ghi đè đầu ra chuẩn. Không sửa tay HTML/SVG/PNG hoặc thay hash để che lỗi. HTML đã duyệt được dựng bằng profile `on-thi-preview` và phát hành nguyên byte qua cổng `prepare --approved-course` theo ủy quyền riêng; không đổi profile hoặc metadata QMD chỉ để phát hành; CLI cấu hình ở `_quy_trinh/cau_hinh_san_xuat_qmd.yml`; PDF toàn văn dùng CLI PDF theo hồ sơ bản in. Hình bối cảnh dùng kích thước chữ thực của bộ sinh; hình và bảng rộng cuộn trong khung riêng trên điện thoại.


Nguồn bố trí in riêng là `_quy_trinh/sinh_hinh_in.py`; vector in và provenance ở `hinh/*.pdf`, `giao_dien/print_assets.json`, `giao_dien/pdf_provenance.json`. Cơ chế in kế thừa đúng hình học, không sửa lại SVG/PNG web.
