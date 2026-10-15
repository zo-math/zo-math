# Danh mục bảo toàn bốn trang — DH_030 và QD_035/DH_032

Ngày: 12/10/2026. Đây là chỉ mục bảo vệ/khôi phục, không là bộ điều hành kiến trúc thứ hai. Trạng thái và bước tiếp theo chỉ ở [03](03_dieu_hanh_chuong_trinh.md); QD_033 hiện hành được ghi ở [04](04_nhat_ki_quyet_dinh.md).

## Bộ bản xem chủ trì chỉ định — không được dọn/xóa

Cập nhật 13/10/2026 theo QD_035: chủ trì chọn chính xác bộ dưới đây làm **nguồn đối chiếu chính thức về bản đang xem để phát triển tiếp**. Không thay bằng một bản Home hoặc bản học liệu khác chỉ vì tên có `approved`/`current`, ngày sửa mới hơn hoặc đã có trong checkpoint DH_030.

- Điểm vào: `_audit/zo_home_refinement_2026-10-12/delivered/home-reading.html`.
- Ba đích học liệu cùng thư mục: `d0-reading.html`, `g01-reading.html`, `g02-reading.html`; giữ nguyên query, fragment, đường dẫn tương đối và runtime của chúng.
- Giữ **toàn cây** `_audit/zo_home_refinement_2026-10-12/delivered/` và tất cả phụ thuộc được liệt kê trong manifest checkpoint DH_032, kể cả phụ thuộc nằm ngoài cây này, CSS/font/hình/JavaScript, tệp tải xuống và bốn trang chân trang Home liên kết trực tiếp: `docs/content/about.html`, `docs/content/contact.html`, `docs/content/support/donate.html`, `docs/content/triet_li_va_dinh_huong.html`.
- Bộ này **không phải cache hay bản thử được phép dọn**. Không xóa, di chuyển hoặc ghi đè để thay bằng bản khác nếu chưa có chỉ thị riêng của chủ trì xác định đúng bộ thay thế và phương án bảo toàn. Tên `_audit/`, tình trạng ignored/untracked hoặc khả năng dựng lại không cho phép loại khỏi danh mục.
- Nguồn đối chiếu được bảo vệ không đồng nghĩa nguồn build: QMD/template/data/script canonical ở bảng dưới vẫn là nơi biên tập và dựng sản phẩm. Giữ cả nguồn canonical và bản đối chiếu; không sửa tay HTML hoặc tái kích hoạt driver đã nghỉ dùng. Việc bảo vệ bản gốc không cấm hiệu chỉnh hợp lệ ở nguồn trong một nhiệm vụ được giao riêng.
- Câu chữ của Home đã chọn khác bản canonical sau DH_028. Chỉ thị bảo toàn này không tự đảo quyết định biên tập, nghiệm thu hay phát hành; không tuyên bố nguồn hiện hành dựng lại chính xác bản Home đã chọn khi chưa đối chiếu. Lịch sử phản hồi và checkpoint cũ giữ nguyên.

Checkpoint bổ sung độc lập: `E:/zo_math_ca_nhan/checkpoints/DH032_20261013_BO_BAN_XEM_CHU_TRI_CHON` và ZIP cùng tên. `manifest.json` là danh sách từng tệp cần giữ với vai trò/kích thước/SHA-256; `payload/` giữ nguyên cấu trúc repo; `README.md` hướng dẫn kiểm/khôi phục. `verification.json` và `scope.json` ghi kết quả kiểm mới; không ghi đè DH_030 hoặc PRE_CLEANUP_QD033. Trước mọi lượt dọn liên quan, phải nạp cả danh mục này và manifest DH_032, kiểm lại checkpoint, loại toàn bộ tệp được bảo vệ khỏi danh sách dọn.

## Nguồn chính thức không được dọn nhầm

Các đường dẫn dưới đây tính từ gốc repo:

| Trang | Nguồn chính thức | Phần phải giữ cùng nguồn |
|---|---|---|
| Nhà | `content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/index.qmd` (nội dung native, DH_038) | `_data/chuong_trinh.yml`, `giao_dien/`, `assets/illustrations/`, ba partial sinh `_partials/home_countdown.qmd`, `home_catalog.qmd`, `home_strands.qmd`, binding `scripts/zo_home_qmd.py` và kit Home; không biên tập trực tiếp partial |
| Khảo sát đầu vào | `content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.qmd` | Dữ liệu, hình, công cụ, cấu hình/hồ sơ và receipt nội dung duyệt trong toàn cây `d0/` |
| Đơn điệu và cực trị | `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.qmd` | Dữ liệu, TeX/hình, binding/layout, công cụ, cấu hình/hồ sơ, receipt lịch sử trong toàn cây `r1_g01/` |
| Giá trị lớn nhất và giá trị nhỏ nhất | `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.qmd` | Dữ liệu, TeX/hình và provenance bộ hình, binding/layout, công cụ, cấu hình/hồ sơ trong toàn cây `r1_g02/` |

Phụ thuộc cần giữ: `hoc_lieu/_dung_chung/` (Ôn nền và Nhật kí), bộ điều hành khóa `_quy_trinh/`, các `AGENTS.md`/metadata trên đường dẫn; `_design/web_2027_mau_dung_chung/`, `_design/ngon_ngu_thiet_ke_zo_math_0_4/`; `scripts/`, `assets/`, `figures/`, `quy_trinh_xay_dung/` và cấu hình gốc. Các thư mục dùng chung được sao lưu bảo thủ; danh mục này không tuyên bố mọi tệp đều là phụ thuộc chạy trực tiếp. Không loại tệp khỏi danh sách chỉ vì chưa được Git theo dõi hoặc bị ignore.

## Checkpoint và bản xem

DH_038 di trú nguồn Nhà theo yêu cầu chủ trì, không thay bộ bản xem QD_035
hoặc sửa checkpoint cũ. Hai nguồn cũ `giao_dien/trang_nha.html.tpl` và
`_partials/chuong_trinh.qmd` nghỉ dùng được sao lưu ngoài repo tại
`E:/zo_math_ca_nhan/legacy_backup_archive/ZO_MATH_HOME_QMD_MIGRATION_20261013`;
chỉ gỡ sau kiểm SHA-256 bản lưu và tương đương nội dung/DOM bản QMD mới.
Manifest checkpoint cũ tiếp tục chứng nhận snapshot tại mốc đó, không yêu
cầu phục hồi nguồn cũ vào đường build mới. Không xóa các bản xem/runtimes cũ.

- Thư mục ngoài repo: `E:/zo_math_ca_nhan/checkpoints/DH030_20261012_BON_TRANG`; ZIP nằm cạnh, cùng tên gốc.
- `manifest.json`: danh sách chính xác từng tệp/vai trò/kích thước/SHA-256/tình trạng Git; `payload/` giữ đường dẫn tương đối.
- `verification.json`: kết quả kiểm độc lập payload và từng thành viên ZIP; `README.md`: cách kiểm và khôi phục vào thư mục mới, không tự ghi đè repo.
- Bộ bản xem DH_030 đã sao lưu trước QD_035: Nhà tại `_audit/zo_home_copy_approved_2026-10-12/delivered/home-reading.html`; không thay bộ chủ trì vừa chỉ định ở mục đầu.
- Bản xem D0/G01/G02 trong DH_030: `_audit/zo_course_navigation_2026-10-12/html-current/`; giữ runtime `delivery/` tương ứng. Giữ cả các bản rebased trong delivered Nhà để liên kết xem không mất tài nguyên. Bảo toàn bổ sung không thu hồi bảo vệ bộ này.
- HTML/PDF đã sinh và hồ sơ `_projects/` được giữ để đối chiếu lịch sử, **không thay QMD/template/data làm nguồn dựng**. Những report được chọn giữ nguyên bytes; không chỉnh QA cũ để chứng nhận QD_033.

## Ranh giới và điều kiện dọn sau này

Lượt này chỉ bảo toàn, không dựng lại hoặc nâng nghiệm thu. QD_033 đã duyệt ở bộ điều hành, nhưng G01/G02 chưa được đối chiếu lại ở cấp QMD/HTML với quyết định này và chưa xác định có nội dung nào cần sửa; PDF hiện có chưa được cập nhật. Manifest không sao lưu lịch sử `.git` hoặc chương trình cài trên máy.

Không xóa/di chuyển bất kỳ nguồn hay phụ thuộc được manifest bảo vệ nếu chưa có phương án mục tiêu cụ thể, xác minh vai trò và kiểm lại checkpoint. Trước dọn toàn repo, phải kiểm kê cả phần ngoài bốn trang; checkpoint này **không bảo vệ toàn bộ repo**. Các đường dẫn đã xóa trước lượt được ghi trong `git-state.json`, không tự phục hồi quy tắc cũ từ HEAD.

Checkpoint ngoài repo vẫn cùng ổ E:. Để chống sự cố ổ đĩa, nên chép cả thư mục, ZIP và kết quả kiểm sang nơi lưu độc lập; chưa thực hiện việc đó trong DH_030.
