# Chỉ dẫn cho chuyên mục Ôn thi Toán THPT

Đây là tài liệu điều phối nội bộ, không phải nội dung xuất bản.

## Tiếp quản sau phát hành 15/10/2026

Bốn trang Nhà, D0, R1-G01, R1-G02 đã xuất bản. Trước công việc tiếp theo,
đọc mục A của `tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md`,
receipt phát hành và hồ sơ khép việc được dẫn ở đó. Các trạng thái chờ
duyệt trong mốc DH/FB bên dưới chỉ mô tả lịch sử của mốc ấy. Quy tắc
chung vẫn có hiệu lực; một sửa đổi mới phải kiểm theo phạm vi ảnh hưởng.
Bộ ảnh bìa giữ đủ năm tỉ lệ theo `tot_nghiep_thpt/2027/giao_dien/bo_anh_bia.json`; bản
vuông do chủ trì thay đã khép tìm ảnh. Không phục hồi ảnh vuông từ
receipt nhập cũ. Trước dọn tài sản, đọc danh mục bảo toàn và chạy
`python scripts/zo_python.py -B scripts/zo_home_cover_check.py`.

## Phạm vi và thẩm quyền

Tuân thủ `AGENTS.md` ở gốc repository và các tài liệu bắt buộc được dẫn chiếu tại đó. Điểm vào điều hành khóa 2027 là `tot_nghiep_thpt/2027/_quy_trinh/README.md`; quy chuẩn gói hiện hành là `tot_nghiep_thpt/2027/_quy_trinh/quy_chuan_goi_qmd.md`; mẫu hồ sơ là `tot_nghiep_thpt/2027/_quy_trinh/mau/ho_so_goi.md`.

Kiến trúc đã được phê duyệt đặt chuyên mục tại `content/thpt/on_thi_toan_thpt`: học liệu dùng lại thuộc `hoc_lieu/<ma_goi>/`, điều hành khóa theo năm thuộc `tot_nghiep_thpt/<nam>/_quy_trinh/`. Không tạo một lớp điều hành song song bên ngoài chuyên mục sau khi hoàn tất chuyển đổi.

Kiến trúc học tập đang áp dụng cho R1-G01, R1-G02 và các gói R1 tiếp theo của khóa 2027 được điều hành bởi:

- `tot_nghiep_thpt/2027/_quy_trinh/01_kien_truc_hoc_tap.md`;
- `tot_nghiep_thpt/2027/_quy_trinh/02_quy_trinh_va_nghiem_thu.md`;
- `tot_nghiep_thpt/2027/_quy_trinh/07_quy_chuan_cau_truc_trang_nguoi_hoc.md` cho cấu trúc, điều hướng và nghiệm thu giao diện người học;
- `tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G01.md` và `tot_nghiep_thpt/2027/_quy_trinh/goi/R1_G02.md` cho phạm vi từng gói;
- `tot_nghiep_thpt/2027/_quy_trinh/schema_kien_truc_hoc_tap.json` và `tot_nghiep_thpt/2027/_quy_trinh/danh_muc_kien_truc_hoc_tap.yml` cho hợp đồng máy đọc được.

Danh mục thẩm quyền của toàn bộ bộ điều hành là `tot_nghiep_thpt/2027/_quy_trinh/08_danh_muc_tham_quyen_dieu_hanh.md`; phải đọc khi tiếp quản hoặc đổi quyết định dùng chung. Chỉ 03 sở hữu việc hiện hành. Cổng đồng bộ tài liệu trong 02 phải khép trước khi biên tập tiếp; không sửa tài liệu lịch sử/receipt để hợp thức hóa ứng viên.

Manifest từng gói nằm tại `hoc_lieu/<ma_goi>/_quy_trinh/kien_truc_hoc_tap.yml`. Trước khi biên soạn nội dung theo kiến trúc này, chạy checker schema và readiness qua `scripts/zo_learning_architecture.py`; `planned` là khoảng trống nội dung thật, không được đổi thành hoàn tất chỉ để checker readiness đạt. Schema hợp lệ hoặc `planned=0` không chứng nhận nội dung/đường học đã đúng; không đổi manifest trong một lượt chỉ đồng bộ văn bản điều hành.

## Giới hạn tích hợp và đầu mối điều hành

Ngôn ngữ bảng QD_030 áp dụng toàn khóa 2027, theo chức năng tại `07_quy_chuan_cau_truc_trang_nguoi_hoc.md`/6.1.1 và mẫu Design 0.4 được dẫn chiếu. Trước dựng hoặc sửa bảng, kiểm ánh xạ trong `_design/web_2027_mau_dung_chung/profiles/course-tables.json`; bộ dựng dùng `scripts/zo_course_tables.py`. Không dùng quy tắc căn trái đại trà đã bị thay thế cho bảng giá trị/dấu/biến thiên hoặc suy kiểu từ tên; bảng chưa phân loại phải được xử lí trước khi trình HTML. Không sửa dữ liệu toán để khớp hình thức.

Hai quy tắc Kiểm tra QD_024 ở `01_kien_truc_hoc_tap.md`, Mục 2.3–2.3.1, áp dụng cho toàn bộ các gói của chương trình Ôn thi Toán THPT 2027, không chỉ R1: đã chuẩn bị kĩ hoặc đủ tự tin thì có thể bắt đầu; một lượt Kiểm tra không chia nhiều đợt. Quyền bắt đầu không chứng nhận đạt mục tiêu. Nạp 07/4.4 và phép kiểm ở 02 khi sản xuất/rà hoạt động này; không dùng điều kiện vào Kiểm tra cũ. Không ép hợp đồng R1 hoặc Kiểm tra lên Khảo sát D0/tài nguyên Nền. Cổng tài liệu của khóa phải kiểm chủ đề `assessment_policy`; PASS tài liệu không chứng nhận nguồn học liệu/HTML đã áp dụng.

Hệ nhãn học liệu QD_025 có hiệu lực cho toàn bộ các gói của chương trình, không chỉ R1: kế thừa QD_023 và bổ sung chức năng Gợi mở. Đọc 01/07, `label_contract` của danh mục kiến trúc và chuẩn QMD. Không tạo nhãn riêng, reset số theo chặng, suy chức năng từ tên hoặc dùng bố cục cũ để chứng nhận đã di trú. Trước sửa nguồn, lập/kiểm bảng `_quy_trinh/ap_dung_he_nhan.json` bằng `zo_learning_architecture.py labels --self-test` qua launcher. Bảng mapping_only không cho phép tự sửa QMD, render hoặc tuyên bố đã nghiệm thu. G01/G02 có binding hiển thị canonical riêng `giao_dien/he_nhan.json`; G02 đã áp dụng nguồn và kiểm HTML cô lập tại DH_016, chưa nghiệm thu chủ trì. Quy tắc mới thay phần cũ nhưng không cấm hiệu chỉnh theo QD_022.

Trước biên tập hoặc kiểm xin duyệt gói R1 của khóa 2027, chạy `python scripts/zo_python.py scripts/zo_2027_governance_check.py` để xác minh bản điều hành và guard theo registry của khóa. Quyết định mới phải thay phần hoạt động cũ và đồng bộ những đích bị ảnh hưởng ngay trong cùng lượt theo mục 1.2 của quy trình 02. Cổng tài liệu đạt không chứng nhận sản phẩm; ứng viên có lỗi chặn không được trình như đã đạt. Theo QD_022/02/1.2, chỉ kiểm lại phần chịu ảnh hưởng của quy tắc, đầu vào hoặc phép kiểm thay đổi; không tái áp dụng quy tắc bị thay, không hủy toàn bộ QA vì hash tài liệu đổi hoặc cấm hiệu chỉnh hợp lệ. Không sửa hash/receipt/kết quả lịch sử để che lệch nguồn.

- Tiếp quản từ mục A của bảng `03_dieu_hanh_chuong_trinh.md`, rồi hồ sơ gói và README vận hành, không từ mốc g01-kit/pilot/receipt lịch sử. QD_016–018 đã hợp nhất quyết định sau FB036: Bài học/Luyện tập không xen kẽ, Nhật kí một nguồn đủ 14 trường, vùng đọc theo nhịp và trạng thái đúng bản. Bản sửa hai gói chưa tự kế thừa nghiệm thu cũ; PDF/phát hành là nhiệm vụ riêng. Không suy trạng thái hiện hành từ số PASS hoặc metadata chưa đồng bộ.
- Không xem mẫu hồ sơ thiết kế của chuyên mục là schema CLI. Ứng viên R1-G01 có cấu hình và hồ sơ riêng trong `_quy_trinh/`; phải đọc README tại đó trước khi làm việc.
- Với khóa 2027, phải đọc `tot_nghiep_thpt/2027/_quy_trinh/README.md`: đây là điểm vào canonical duy nhất. Công việc hiện hành và việc tiếp theo chỉ được ghi tại `03_dieu_hanh_chuong_trinh.md`. README cũ trong `_projects/on_thi_toan_thpt_2027` chỉ dùng để chuyển tiếp.
- Tài liệu đã khóa và thành phẩm lịch sử chỉ được chuyển hoặc sửa trong phạm vi chủ dự án giao; không suy từ việc chuyển quản trị thành quyền chuyển đổi học liệu.
- Không tạo trước thư mục gói tương lai hoặc tài nguyên chưa dùng.
- Không tự thay nội dung toán học, nhiệm vụ, thuật ngữ hoặc thiết kế đã chốt.

## Render, preview và xuất bản

Kế thừa dự án Quarto ở gốc; không tạo `_quarto.yml` độc lập. Hai trang cửa ngõ chưa thuộc một dự án QMD có cấu hình, nên dùng trình khởi chạy Quarto chung từ gốc repository:

```text
python scripts/zo_python.py scripts/zo_quarto.py render content/thpt/on_thi_toan_thpt --profile on-thi-preview
python scripts/zo_python.py scripts/zo_quarto.py preview content/thpt/on_thi_toan_thpt/index.qmd --profile on-thi-preview
```

Preview chỉ lắng nghe tại `127.0.0.1`. Navbar/sidebar nguồn dùng chung có đường vào ứng viên để kiểm tra đường đi; các trang và tài sản đã duyệt của chuyên mục chỉ được chọn qua allowlist publish. Khi cần bảo toàn đầu ra hiện có trong một nhiệm vụ kiểm thử, dùng bản sao dự án cô lập dưới `_audit/`, giữ nguyên cấu hình dự án và profile.

Metadata `draft: true` không thay thế hàng rào xuất bản. `publish_public.yml` chỉ cho phép đầu ra công khai đã duyệt và tiếp tục chặn `_quy_trinh` lâu dài. Không liên kết tài liệu điều hành từ trang dành cho người đọc, không khai báo resources quét cả cây chuyên mục.

Tuân thủ `quy_trinh_xay_dung/quy_trinh_xuat_ban_website.md`. Chỉ dùng `zo_publish.py check` khi kiểm tra; `prepare`/`publish`, staging, commit và push cần yêu cầu riêng. Không dùng `_publish_exclude.md` hoặc `.gitignore` làm hàng rào public.
