# Hồ sơ sửa thuật ngữ và lời văn — EDITORIAL-20261018

Chủ trì duyệt ma trận vào ngày 18/10/2026 và giao sửa nguồn sáu trang, cập nhật quy tắc/cổng kiểm, giữ điều kiện toán và điều hướng. Phạm vi duyệt là nguồn; chưa có HTML/PDF mới, chưa commit hoặc phát hành. Trạng thái hiện hành ở 03.

## Nội dung đã xử lí

- Áp dụng 61 mục đối chiếu: 59 mục sửa/viết lại/gộp, hai mục giữ làm đối chứng (E07, E19). Xử lí đủ 252 dòng nguồn có chữ “miền”, theo tập xác định, tập đang xét hoặc điều kiện của biến; giữ từ trong ID kỹ thuật cũ. Không áp lệnh thay “miền” cho miền nghiệm/miền phẳng.
- Sáu trang: Khóa 2027, Khảo sát đầu vào, Đơn điệu và cực trị, Giá trị lớn nhất và giá trị nhỏ nhất, Đường tiệm cận, Khảo sát sự biến thiên và vẽ đồ thị của hàm số. Tổng cộng 14 QMD thay đổi trong cây 22 nguồn/include được rà. Dữ liệu danh mục Home và bốn bảng nhãn hiển thị được đối chiếu cùng lượt.
- Viết rõ các yêu cầu và lời giải về tập xác định, giới hạn theo từng phía, điều kiện mô hình, đỉnh/hoành độ đỉnh và các đối tượng cực trị. Bỏ câu mô tả thiết kế đánh giá không giúp học sinh làm bài; gộp hướng dẫn lặp. Giữ nguyên kiến trúc 01, các điều kiện tự lực/tính mới của bài và hỗ trợ theo nhu cầu.
- Đề/lời giải vẫn dùng Xem lời giải và Xem đề bài. Giữ ID, tham số quay về, số nhiệm vụ, số ý/bước và các mục điều hướng. D0 nêu tường minh ID cũ tự sinh `biến-và-miền-hợp-lệ` sau đổi tên, để liên kết sâu cũ tiếp tục dùng. Các liên kết bị bỏ chỉ thuộc chỉ dẫn trùng đã được gộp theo ma trận; đích chức năng vẫn còn. G03 sửa đích hỗ trợ điều kiện mô hình về đúng ví dụ thay vì thẻ biến đổi phân thức.

## Nguyên nhân và phòng tái diễn

Lời điều hành về bằng chứng, tính mới và bài xác nhận đã đi vào chính văn; cách rút ngắn làm mất đối tượng toán; lượt kiểm trước tập trung vào hộp hướng dẫn, chữ đầu và cấu trúc, chưa đủ đối chiếu ngữ nghĩa toàn trang. 07/6.1.6 nay sở hữu quy tắc cho cả Nhà/D0/gói học liệu; 02, mẫu bản thảo 1.4 và bảng kiểm 1.7 (B24) yêu cầu đọc từng ngữ cảnh và ghi trước/sau.

Cổng chung `zo_course_editorial.py` kiểm cả nguồn include, dữ liệu sinh Home, nhãn hiển thị và cách diễn đạt đã xác định là lỗi; hồ sơ rà nguồn hết khớp thì phải đọc phần thay đổi trước khi cập nhật. Có ca âm cho từ sai, nguồn dùng chung, dữ liệu danh mục, hồ sơ cũ và nhầm chứng nhận HTML. Cổng tương lai trên HTML nối Nhà/D0 và bốn gói. Không thêm máy tự viết lại hoặc tự gia hạn hồ sơ. PASS từ vựng/hash không chứng minh mọi câu đều rõ nghĩa; đối chiếu biên tập vẫn bắt buộc.

G01 cập nhật 67 binding đoạn từ nguồn mới. Fingerprint đầy đủ, biên nhận nghiệm thu và hash tài sản lịch sử được giữ. Chỉ đảo các đoạn đã liệt kê trên cây sao để so sánh; nội dung cũ không đi vào đầu ra. Đối sánh cây Markdown JSON xác nhận không đổi cấu trúc mục, điểm neo hoặc số phần tử danh sách; chưa có bản HTML mới để kiểm trực quan.

## Bằng chứng và giới hạn

- Kiểm toàn vẹn: 52/52; 4708 HTML/PDF/SVG/tài nguyên bộ xem giữ nguyên byte. Staged rỗng; Git có thể tự làm mới cache trạng thái tệp trong index khi đọc, không có thao tác stage/commit.
- Cấu trúc sáu nguồn qua Pandoc JSON AST: 18/18; không dựng HTML/PDF. Công thức hiển thị riêng không đổi; 59 dòng có thay đổi cách ghi kí hiệu nội tuyến đã được đối chiếu trong ngữ cảnh, gồm đưa số vào LaTeX và viết rõ đối tượng/điều kiện đã có.
- Hồi quy biên tập: 138/138. Cổng nguồn hiện hành và điều hành được chạy theo phạm vi; xem các báo cáo trong thư mục bằng chứng. Các phép kiểm cũ chỉ giữ giá trị đúng phần không chịu ảnh hưởng.
- Chưa kiểm trực quan HTML mới hoặc PDF mới, chưa có nghiệm thu mới. HTML trong bộ xem sáu trang vẫn là bản trước các lượt sửa mục tiêu, chỉ dẫn và biên tập; không dùng để xem kết quả lần này.

## Mở kết quả để đọc

- [Đối chiếu 61 mục sau sửa](/E:/zo_math/_audit/editorial_implementation_20261018/doi_chieu_61_muc.md).
- [Kiểm kê 252 vị trí trước/sau](/E:/zo_math/_audit/editorial_implementation_20261018/term_resolution.json).
- [Tất cả dòng nguồn thay đổi trong lượt này](/E:/zo_math/_audit/editorial_implementation_20261018/source_changes.json).
- [Đối chiếu kí hiệu nội tuyến](/E:/zo_math/_audit/editorial_implementation_20261018/math_inline_review.json), [liên kết](/E:/zo_math/_audit/editorial_implementation_20261018/navigation_changes.json), [toàn vẹn](/E:/zo_math/_audit/editorial_implementation_20261018/integrity.json).

Các tệp audit là bằng chứng đọc/kiểm, không là đầu vào biên dịch. Nguồn hiện hành tiếp tục ở vị trí gói và điều hành đã thống nhất.

## Tệp sửa/tạo trong lượt này

- [editorial-language.json](/E:/zo_math/_design/web_2027_mau_dung_chung/profiles/editorial-language.json) — `_design/web_2027_mau_dung_chung/profiles/editorial-language.json`.
- [AGENTS.md](/E:/zo_math/content/thpt/on_thi_toan_thpt/AGENTS.md) — `content/thpt/on_thi_toan_thpt/AGENTS.md`.
- [N-GH-01.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-GH-01.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-GH-01.qmd`.
- [N-LT-01.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-LT-01.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-LT-01.qmd`.
- [N-NGUYÊN-01.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-NGUYÊN-01.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-NGUYÊN-01.qmd`.
- [N-TXĐ-01.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-TXĐ-01.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-TXĐ-01.qmd`.
- [N-ĐH-02.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-ĐH-02.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-ĐH-02.qmd`.
- [N-ĐH-03.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-ĐH-03.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nen/N-ĐH-03.qmd`.
- [nhat_ki_hoc_tap.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nhat_ki_hoc_tap.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nhat_ki_hoc_tap.qmd`.
- [index.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.qmd`.
- [web_2027_layout.json](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/giao_dien/web_2027_layout.json) — `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/giao_dien/web_2027_layout.json`.
- [index.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd`.
- [he_nhan.json](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/giao_dien/he_nhan.json) — `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/giao_dien/he_nhan.json`.
- [index.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.qmd`.
- [he_nhan.json](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/giao_dien/he_nhan.json) — `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/giao_dien/he_nhan.json`.
- [index.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g03/index.qmd`.
- [he_nhan.json](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/giao_dien/he_nhan.json) — `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/giao_dien/he_nhan.json`.
- [index.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/index.qmd) — `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g04/index.qmd`.
- [chuong_trinh.yml](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_data/chuong_trinh.yml) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_data/chuong_trinh.yml`.
- [home_catalog.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_partials/home_catalog.qmd) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_partials/home_catalog.qmd`.
- [02_quy_trinh_va_nghiem_thu.md](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/02_quy_trinh_va_nghiem_thu.md) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/02_quy_trinh_va_nghiem_thu.md`.
- [03_dieu_hanh_chuong_trinh.md](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md`.
- [04_nhat_ki_quyet_dinh.md](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/04_nhat_ki_quyet_dinh.md) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/04_nhat_ki_quyet_dinh.md`.
- [07_quy_chuan_cau_truc_trang_nguoi_hoc.md](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/07_quy_chuan_cau_truc_trang_nguoi_hoc.md) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/07_quy_chuan_cau_truc_trang_nguoi_hoc.md`.
- [08_danh_muc_tham_quyen_dieu_hanh.md](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/08_danh_muc_tham_quyen_dieu_hanh.md) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/08_danh_muc_tham_quyen_dieu_hanh.md`.
- [ho_so_bien_tap_ro_nghia_20261018.json](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/ho_so_bien_tap_ro_nghia_20261018.json) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/ho_so_bien_tap_ro_nghia_20261018.json`.
- [ho_so_bien_tap_ro_nghia_20261018.md](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/ho_so_bien_tap_ro_nghia_20261018.md) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/ho_so_bien_tap_ro_nghia_20261018.md`.
- [hop_dong_dieu_hanh.json](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/hop_dong_dieu_hanh.json) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/hop_dong_dieu_hanh.json`.
- [ban_thao_goi.md](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/mau/ban_thao_goi.md) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/mau/ban_thao_goi.md`.
- [bang_kiem_ban_thao_goi.md](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/mau/bang_kiem_ban_thao_goi.md) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/mau/bang_kiem_ban_thao_goi.md`.
- [index.qmd](/E:/zo_math/content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.qmd) — `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.qmd`.
- [zo_check_repo.py](/E:/zo_math/scripts/zo_check_repo.py) — `scripts/zo_check_repo.py`.
- [zo_course_editorial.py](/E:/zo_math/scripts/zo_course_editorial.py) — `scripts/zo_course_editorial.py`.
- [zo_course_editorial_selftest.py](/E:/zo_math/scripts/zo_course_editorial_selftest.py) — `scripts/zo_course_editorial_selftest.py`.
- [zo_web_2027_consistency.py](/E:/zo_math/scripts/zo_web_2027_consistency.py) — `scripts/zo_web_2027_consistency.py`.
- [zo_web_2027_d0.py](/E:/zo_math/scripts/zo_web_2027_d0.py) — `scripts/zo_web_2027_d0.py`.
- [zo_web_2027_home.py](/E:/zo_math/scripts/zo_web_2027_home.py) — `scripts/zo_web_2027_home.py`.
- [zo_web_2027_production.py](/E:/zo_math/scripts/zo_web_2027_production.py) — `scripts/zo_web_2027_production.py`.
