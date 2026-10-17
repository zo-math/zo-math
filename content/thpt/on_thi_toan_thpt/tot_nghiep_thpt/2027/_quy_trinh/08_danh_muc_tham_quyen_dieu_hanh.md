# Danh mục và thẩm quyền bộ điều hành 2027

**QD_035:** [Danh mục bảo toàn](bao_toan_bon_trang.md) sở hữu việc bảo vệ đúng bộ `_audit/zo_home_refinement_2026-10-12/delivered/home-reading.html` và các trang/tài nguyên liên kết làm nguồn đối chiếu chính thức để phát triển tiếp, không được dọn/xóa hoặc tự thay bằng bộ DH_030. Manifest DH_032 ngoài repo ghi từng tệp/hash; 03 sở hữu trạng thái. Nguồn build vẫn là QMD/template/data/script canonical; không nâng bản HTML audit thành chuẩn nội dung, runtime production hay nghiệm thu mới, không đảo câu chữ đã duyệt. Giữ nguyên hai checkpoint cũ.

**QD_034:** [Chỉ mục lưu trữ lịch sử](luu_tru_lich_su.json) chỉ ánh xạ bảy cây và 21 driver audit đã được phép nghỉ dùng tới kho ngoài repo/manifest/SHA-256; không là cấu hình chạy, nguồn sản xuất hoặc chuẩn học tập. 03 sở hữu trạng thái DH_031, 04 giữ quyết định mới và lịch sử nguyên trạng. Các checker canonical và đầu vào hiện hành không bị đổi; giữ `html-current`, `delivery` và figure `build`. Không khôi phục thẩm quyền hoặc chạy lại driver cũ từ đường dẫn trong hồ sơ lịch sử. QD_033 tiếp tục sở hữu đường học; PASS lưu trữ không nghiệm thu học liệu.

**QD_032:** 07 sở hữu điều hướng toàn khóa học; `_data/chuong_trinh.yml` sở hữu danh mục, `zo_web_2027_navigation.py` sở hữu binding hiển thị/URL hiện hữu, kit sở hữu CSS/JS và checker sở hữu kiểm kỹ thuật. Bốn adapter gọi cùng module; không lấy mẫu audit làm chuẩn/runtime thứ hai. 03 sở hữu DH_027 và trạng thái HTML. Phân cấp tiêu đề chưa được duyệt, không có quy tắc mới thay cấp hiện hành.

Phiên bản: 0.11 · Ngày: 17/10/2026 · Căn cứ: QD_019, phần còn hiệu lực của QD_021, QD_022–032, QD_033, QD_034, QD_035 và QD_036.

**QD_033:** 01 sở hữu Bài học → Luyện tập → Kiểm tra → Ôn lại là tiến trình chuẩn được khuyến nghị nhưng không cưỡng chế hoàn thành tuần tự, cùng quyền chọn điểm vào, hỗ trợ độc lập, tự lực trong lượt Kiểm tra và phân biệt bằng chứng/Nhật kí; 07 sở hữu cách thể hiện cùng ngoại lệ liên kết tại chỗ; 02 sở hữu cơ chế thay thế. Registry chọn `learning_route`/QD_033, không lấy audit profile QD_021 làm xác nhận QMD/HTML hiện hành. Công việc/trạng thái/bước tiếp chỉ đọc mục A của 03; không phục hồi quy tắc cũ từ hồ sơ hay báo cáo giữ lịch sử.

Làm rõ QD_025/QD_036 ngày 17/10/2026: 01 sở hữu quan hệ Gợi mở thuộc từng mục kiến thức trong Bài học; 07 sở hữu cách giữ cấp mục trong tiêu đề/mục lục/điều hướng; danh mục nhãn cụ thể hóa cùng nghĩa. Bảng kiểm bản thảo 1.1 ghi đường dẫn cha–con; mẫu bản thảo 1.0 đã đúng nên giữ nguyên. Hồ sơ G03 có bảng phân bổ hiện hành và cảnh báo mục 11–13 là lịch sử đã bị thay; không sửa bản thảo đã giữ làm căn cứ, receipt hoặc HTML/PDF. Không lấy hàng kiểm kê chức năng làm cấp mục.

QD_025 mở rộng hệ nhãn QD_023 bằng Gợi mở, áp dụng toàn chương trình. Chủ sở hữu từ vựng/quan hệ vẫn ở danh mục/01, hiển thị ở 07. G01 đã áp dụng bản chốt vào QMD; `giao_dien/he_nhan.json` là binding hiển thị canonical của G01, không là từ điển hoặc nguồn toán thứ hai. `zo_r1_g01_labels.py` và `zo_r1_g01_labels_check.py` thực thi/kiểm phép chiếu; `zo_r1_g01_rebind.py` chỉ là thao tác di trú layout tường minh, không phụ thuộc build thông thường. G02 đã di trú tại DH_016 bằng binding riêng `giao_dien/he_nhan.json` và `zo_r1_g02_labels_check.py`; helper chung nhận binding G02 tường minh, mặc định G01 không đổi. Kiểm kê từ nguồn tươi nằm trong audit, không là nguồn build thứ hai. Không tuyên bố CLI di trú G01 đã tự hỗ trợ mọi gói. Trạng thái từng gói ở 03/profile, không suy từ cùng CSS.

Đây là sổ phân vai tài liệu, không phải một bộ quy tắc hoặc roadmap thứ hai. [README](README.md) là điểm vào; [03](03_dieu_hanh_chuong_trinh.md) sở hữu công việc và trạng thái tổng hợp. Đường dẫn có tiền tố `content/`, `_design/`, `_projects/`, `scripts/`, `assets/` và `quy_trinh_xay_dung/` dưới đây tính từ gốc repo.

QD_028 bổ sung phân biệt chức năng nhánh tại 01/2.5.1 và danh mục nhãn, quy trình đối sánh tại 02/1.3, hiển thị tại 07 và ánh xạ tại chuẩn QMD. Không tạo quy chuẩn riêng từ báo cáo nghiên cứu. DH_021 là mốc đối sánh lịch sử; việc hiện hành của hai gói và toàn khóa chỉ lấy từ mục A của 03. Hồ sơ và báo cáo mới không thay receipt lịch sử.


**Bổ sung vận hành bản thảo ngày 17/10/2026:** 07/6.3 giữ yêu cầu chính văn phát biểu trực tiếp và không miễn thiết kế cho hình nháp; quy chuẩn gói giữ quy cách .zo-source-note; 02/1.4 bắt buộc nạp trước viết/rà. Mẫu nội dung hiện hành 1.1, bảng kiểm 1.2. Ghi chép 1.0/1.1 ở đoạn Gợi mở phía trên chỉ mô tả mốc hiệu chỉnh trước đó. Giới hạn không sửa G01–G03 chỉ áp dụng lượt G04 ngày 17/10. Yêu cầu ngày 18/10 đã cho phép đối chiếu và sửa QMD/HTML G01–G04 theo 07/6.4; không mở PDF hoặc nâng Design 0.5.

## 1. Một vấn đề, một nguồn có thẩm quyền

| Vấn đề | Chủ sở hữu | Tài liệu khác được làm gì |
|---|---|---|
| Phạm vi, mạch và lộ trình toàn chương trình | [Kế hoạch 0.6](ke_hoach_dieu_hanh.md), trong phần chưa bị quyết định sau thay thế | Tham chiếu; không khôi phục trạng thái hay lệnh sản xuất cũ |
| Đường học, chức năng học tập, Nhật kí 14 trường | [01 — Kiến trúc](01_kien_truc_hoc_tap.md) | Hồ sơ gói cụ thể hóa mục tiêu/toán/tham số; manifest ghi hiện thực cần đối chiếu |
| Quyền bắt đầu và không chia một lượt Kiểm tra, toàn chương trình (QD_024) | 01/2.3–2.3.1 | 07/4.4 giữ lời dẫn, 02 giữ phép kiểm; hồ sơ/template không giới hạn hai quy tắc này ở R1 hoặc dùng lại điều kiện cũ |
| Cách sản xuất, sửa và nghiệm thu | [02 — Quy trình](02_quy_trinh_va_nghiem_thu.md) | README vận hành chỉ dẫn đúng công cụ và phạm vi của gói |
| Gọi mẫu, đối chiếu trước viết và kiểm trước trình bản thảo R1 (QD_036) | 02/1.4; [mẫu bản thảo](mau/ban_thao_goi.md) và [bảng kiểm](mau/bang_kiem_ban_thao_goi.md) là công cụ áp dụng 01/07 | AGENTS kích hoạt từ yêu cầu tự nhiên; hồ sơ gói ghi phiên bản/bằng chứng trong ho_so, không tạo bộ kiến trúc hoặc thiết kế trang thứ hai |
| Việc đang mở, thứ tự và bước tiếp | [03 — Điều hành](03_dieu_hanh_chuong_trinh.md) | Chỉ trỏ về đây; không duy trì roadmap cạnh tranh |
| Bản đối chiếu chủ trì chọn, nguồn/phụ thuộc không được dọn (QD_035) | [Danh mục bảo toàn](bao_toan_bon_trang.md); manifest DH_032 ghi từng tệp/hash | 03 ghi trạng thái; bản xem là nguồn đối chiếu được bảo vệ, không thay QMD/template/data/script làm nguồn dựng; không lấy tên `_audit/` hay bản khác mới hơn làm quyền xóa |
| Quyết định và phần bị thay thế | [04 — Nhật kí quyết định](04_nhat_ki_quyet_dinh.md) | Ghi nguồn phát sinh/evidence, không tự phê duyệt đề xuất |
| Cách tiếp quản và giao việc | [05 — Hướng dẫn](05_huong_dan_su_dung.md) | Prompt cũ không cấp quyền mới |
| Provenance, chuyển tiếp, tài liệu nhập | [06 — Nguồn](06_nguon_va_chuyen_tiep.md) | Bằng chứng giữ nguyên theo thời điểm |
| Vai trò trang, nhịp đọc và điều hướng | [07 — Cấu trúc trang](07_quy_chuan_cau_truc_trang_nguoi_hoc.md) | Kit cụ thể hóa component; không quyết định lại đường học |
| Ngôn ngữ bảng theo chức năng, toàn khóa (QD_030) | 07/6.1.1, dẫn mẫu bảng Design 0.4 | Kit `profiles/course-tables.json` ánh xạ từng bảng; `zo_course_tables.py` chặn bảng chưa phân loại và sai dữ liệu native. Không áp căn trái đại trà cho bảng toán; không đổi toán/đường học hoặc mặc nhiên chứng nhận PDF |
| Hợp đồng QMD và ánh xạ sang đầu ra | [Quy chuẩn gói QMD](quy_chuan_goi_qmd.md) | Cấu hình/filter là hiện thực, không chứng nhận chất lượng sư phạm |
| Nghĩa/chức năng của hệ nhãn | 01; `label_contract` trong danh mục kiến trúc giữ một bản khóa/tên/phạm vi | 07 giữ quy tắc hiển thị; không tạo từ điển độc lập trong gói/kit/audit |
| Áp dụng/di trú nhãn riêng của gói | Bảng `_quy_trinh/ap_dung_he_nhan.json` của gói, schema/loader dùng chung | Chỉ ánh xạ, không là nguồn văn bản/toán thứ hai hoặc xác nhận đã sửa học liệu |
| Phạm vi toán, tham số và vấn đề riêng của gói | [G01](goi/R1_G01.md), [G02](goi/R1_G02.md), [mẫu hồ sơ](mau/ho_so_goi.md) | Không viết lại quy tắc chung, không sao chép số vùng/bài của gói mẫu |

Khi cùng vấn đề thay đổi nhiều lần, áp dụng quyết định được chủ trì xác nhận sau cùng **trong đúng phạm vi**. Chỉ thị mới không mặc nhiên xóa quyết định khác không liên quan. Chưa có quyết định thì ghi đề xuất/chưa chốt, không lấy hiện trạng mã hoặc lời agent làm quy chuẩn.

## 2. Toàn bộ các lớp phải tiếp quản

| Lớp/tài liệu | Vai trò và giới hạn |
|---|---|
| `AGENTS.md` gốc; hai quy trình bắt buộc trong `quy_trinh_xay_dung/`; `content/thpt/on_thi_toan_thpt/AGENTS.md` | Chỉ dẫn agent có hiệu lực theo phạm vi. Chỉ dẫn thư mục sâu hơn bổ sung, không tự vô hiệu hóa gốc |
| `quy_trinh_xay_dung/he_thong_san_xuat_qmd/README.md` và tài liệu nó dẫn; chuẩn khối nội dung, lưới thẻ, đồ thị, hình học, xuất bản | Quy trình hạ tầng toàn repo. Nạp nhánh liên quan khi làm loại nhiệm vụ đó; không nâng chuẩn cục bộ 2027 thành chuẩn toàn ZO Math |
| Các tệp 01–08, README, quy chuẩn QMD, mẫu và hai hồ sơ trong thư mục này | Bộ điều hành khóa, theo bảng chủ sở hữu ở trên |
| `schema_kien_truc_hoc_tap.json`, `danh_muc_kien_truc_hoc_tap.yml` | Hợp đồng/danh mục máy đọc; schema hợp lệ hoặc `planned=0` không chứng minh đường học khép kín |
| `truyen_thong_qua_trinh.md` | Sổ nội dung truyền thông; không chứng nhận học liệu hoàn thiện hoặc đã phát hành |
| `content/thpt/on_thi_toan_thpt/hoc_lieu/{d0,r1_g01,r1_g02}/_quy_trinh/README.md` | Điểm vào vận hành riêng; trạng thái hiện hành phải khớp 03 và hồ sơ đúng bản |
| Cùng các thư mục trên: `cau_hinh_san_xuat_qmd.yml`, `ho_so/index.yml`; manifest kiến trúc/chuyển đổi, ma trận và hợp đồng nếu có | Cấu hình đang chạy, trạng thái máy đọc, quan hệ nguồn. Danh sách `controlling_documents` trong cấu hình là danh sách nạp/kiểm; không khiến báo cáo lịch sử trở thành quy chuẩn hiện hành. Phải phân vai theo README và sổ này |
| D0: `hop_dong_nguon_canonical.md`, `ma_tran_phep_chieu_noi_dung.md` | Phần đầu hiện hành sở hữu phép chiếu D0 đã duyệt; phần 6B bên dưới chỉ lịch sử. Tự nguyện, không áp nguyên kiến trúc R1; bổ sung PDF toàn trang ngày 14/10 theo yêu cầu trực tiếp, không khôi phục bốn biến thể |
| D0: `bao_cao_sua_loi_5a.md`, `bao_cao_kiem_toan_buoc_6a.md`, `pilot_hinh_hoc/README.md`, `lich_su/v1_0/**` | Bằng chứng chuyển đổi/fixture/baseline bất biến, không lệnh tái sinh QMD mới |
| G01/G02: `giao_dien/README_web_2027.md` nếu có; `_quy_trinh/README.md`; `giao_dien/web_2027_layout.json`, `web_2027_figures.json` | Hợp đồng vận hành/profile thực. Layout quy định ownership kỹ thuật, không tự quyết cấp sư phạm. Tổng số vùng là thống kê của bản kiểm, không mục tiêu liên gói |
| `_design/web_2027_mau_dung_chung/AGENTS.md`, `README.md`, `hop_dong_vung_doc.md`, `kiem_thu.md`, `doi_sanh_lien_goi.md`, `doi_sanh_FB036.md`, `figure-profile-candidate/README.md` | Kit/hợp đồng component/QA và hồ sơ lỗi. Chức năng học do 01/07 xác lập. Các mốc FB cũ là evidence, không xác nhận ứng viên mới |
| `_design/ngon_ngu_thiet_ke_zo_math_0_4/AGENTS.md`, `00_BAT_DAU_O_DAY.md`, `01_dieu_hanh/**`, `02_quy_chuan/**`, `03_token/**` và tài sản nguồn/mẫu khóa | Nền thiết kế 0.4 có phạm vi riêng. Không sửa package khóa hoặc tự nâng 0.5. Đường dẫn cài đặt cũ trong bộ khóa không là gốc vận hành mới |
| Cùng package Design: `04_ap_dung/01_web_2027.md`, `09_nhat_ki/cong_viec_hien_tai.json`, `tiep_nhan_san_pham.json`, `lich_su.md`, `phan_hoi_tich_hop_web_2027_0_4.md`, mốc duyệt và backlog 0.5 | Binding Web, con trỏ về 03, nhật kí feedback và đề xuất. Không mở lại M8.R/Video, không có quyền phát hành từ backlog |
| `quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/README.md`, `quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/README.md`; `scripts/zo_web_2027_*.py`, các hook/filter và CSS/JS | Hướng dẫn và hiện thực kỹ thuật: style 0.4 opt-in, bảng native HTML đã tích hợp nguồn canonical G01/G02 qua adapter và dựng cô lập. Preview G02 cũ chỉ là bằng chứng lịch sử; không gọi mặc định toàn repo là đã đổi, không suy PDF từ HTML |
| `content/thpt/on_thi_toan_thpt/hoc_lieu/_dung_chung/nhat_ki_hoc_tap.qmd`, `nen/**`, `index.qmd` từng gói, trang Nhà/cửa ngõ, dữ liệu danh mục | Nguồn sản phẩm cần bảo toàn và đối chiếu với quy tắc; không phải một nguồn điều hành mới. Nhật kí dùng chung một nguồn, không viết riêng cho mỗi gói |
| G02 `_quy_trinh/ho_so/lich_su_ban_thao_v0_1.md`; G01 `_quy_trinh/lich_su/**`; kho chuyển tiếp tại 06 | Bản thảo và mốc đồng bộ cũ giữ nguyên. Ma trận chuyển đổi G02 tháng 9 đã được lưu ngoài repo, gỡ khỏi cây làm việc; không là chỉ dẫn biên soạn. Kiến trúc theo 01/QD_033, hiển thị theo 07 |
| `_projects/on_thi_toan_thpt_2027/README.md`, `AGENTS.md`; tài liệu/bộ bàn giao còn lại ở vị trí cũ | Chuyển tiếp hoặc provenance; không điều hành song song, không thực thi prompt lịch sử. Bộ G01 v1.1 còn là đầu vào kiểm bảo toàn theo manifest SHA-256; giữ nguyên bytes, không xóa/sửa để làm mất sơ đồ lịch sử |
| `_audit/**`, receipt nghiệm thu, checkpoint ngoài repo, PDF/HTML đã dựng và báo cáo QA | Bằng chứng theo bản/phạm vi. Giữ nguyên lịch sử; không dùng làm nguồn biên tập hoặc sửa hash để báo PASS |

Các thư mục nguồn/media/specimen khác của Design là tài sản tham chiếu hoặc phụ thuộc, không vì nằm trong package mà có thẩm quyền điều hành khóa. Không cần sửa hàng trăm tài sản để đồng bộ văn bản điều hành.

Trang Nhà DH_038: `index.qmd` trực tiếp sở hữu nội dung biên tập native Markdown; không còn include toàn trang HTML sinh hoặc dùng template làm nguồn câu chữ. `zo_build_on_thi.py` sinh riêng ba component `_partials/home_countdown.qmd`, `home_catalog.qmd`, `home_strands.qmd` từ YAML/metadata thật. `giao_dien/README_web_2027.md` sở hữu hướng vận hành; `profiles/course-home.json` vẫn chọn bố cục `editorial-home-2027`. Adapter `zo_web_2027_home.py` điều phối `zo_web_2027_home_landing.py`; `zo_home_qmd.py` nối DOM native với UI đã có; checker Home kiểm nguồn native, hash component và Quarto tươi. HTML/PNG nhập tại reference/assets chỉ là tài nguyên được giao, không là quy chuẩn. Thay đúng cơ chế nguồn Nhà DH_028, không thay câu chữ đã chốt, đường học 01, QD_035, nghiệm thu lịch sử, D0, nguồn riêng G01/G02 hoặc PDF; catalog preview không chứng nhận đã nghiệm thu gói.

## 3. Các thay thế đã có căn cứ

**QD_031 / DH_026:** Nhật kí là khu vực ngang hàng, không thuộc Ôn lại; Toàn văn dùng đúng thứ tự ở 07/3. Nội dung con trở về đúng owner, không ghép peer. Sửa lỗi đánh số liên tục theo thứ tự Sau Luyện tập → Sau Kiểm tra → Sau Ôn lại, nhánh Chuyển giao đặt theo owner riêng G02; đồng bộ số qua binding/tiêu đề/đích/nhãn tham chiếu. Đề và đáp án cùng vùng/tài nguyên không có liên kết nhảy thừa, đáp án vẫn thu gọn. Bảng chọn bài dùng một kiểu bốn cột, chỉ dẫn dài tách khỏi ô nhưng không mất nội dung. G02 dựng mới đủ năm SVG theo profile 0.4 và kiểm provenance. Các hợp đồng/QA cũ trái các quy tắc này chỉ có giá trị lịch sử; không phục hồi Nhật kí gộp Ôn lại, lời giải sai nhóm hoặc cache hình cũ. 01/02/07 sở hữu quy tắc, registry và guard chỉ hiện thực kiểm; scope không bao gồm PDF học liệu/Git/phát hành.

**QD_033 hiện hành cho đường học, kế thừa phần không bị thay của QD_021:** nghĩa và 14 tình huống lấy từ 01/2.2.1–2.2.2; cổng thay thế/bằng chứng ở 02/1.2. DH_015/016 đã triển khai hai gói theo quyết định tại thời điểm đó; không chứng nhận nguồn đã đạt QD_033 và không kế thừa nghiệm thu giữa gói. QA DH_011/FB036 và audit QD_021 trong profile giữ lịch sử; trạng thái đường học mới lấy từ 03/registry, không từ đoạn lịch sử.

| Phần bị thay | Đích tiếp quản và tác động |
|---|---|
| Bốn khu vực phải hoàn thành tuần tự; sáu việc ở Điểm dừng thành nghi thức Nhật kí; mọi cặp đề–lời giải cần link quay lại | QD_033/01/2.2–2.4 và 07/2, 3, 5.3–5.4: chọn điểm vào theo ngữ cảnh, lưu bằng chứng khác ghi Nhật kí, chỉ link quay lại khi thực sự tách vị trí; hợp đồng QMD thay cùng lượt |
| Phải có bài làm độc lập trước đó mới được vào Kiểm tra; suy chia việc học thành quyền chia một lượt Kiểm tra | QD_024/01/2.3.1: chuẩn bị kĩ hoặc đủ tự tin thì có thể bắt đầu; một lượt không chia đợt, toàn bộ các gói có Kiểm tra; quyền vào không là bằng chứng đạt |
| Đổi một hash tài liệu/guard thì mọi QA hết hiệu lực | QD_022/02: chống quy tắc bị thay; chỉ kiểm lại phần ảnh hưởng, cho phép hiệu chỉnh hợp lệ |
| Bản đồ bảy nút ở DH_011; sửa/ghi/hẹn ôn là chặng tuyến tính | 01/2.2.1: bốn hoạt động mạch chính và nhánh hỗ trợ; G01 RD01/RD06 đã sửa nguồn ở DH_015, chờ duyệt HTML |
| Nhãn công bố “Bài học, gồm Khởi động” và câu giải thích quyết định nội bộ | 07: tên ngắn phù hợp người học; không chép lí do biên tập vào học liệu |
| Ôn nguồn chỉ được hiểu là Ôn nền; sửa chỉ sau Kiểm tra | 01/2.2.2: xem lại Bài học/Ôn nền và đối chiếu–sửa ở đúng thời điểm, trừ Kiểm tra đang diễn ra |
| 465/465 hoặc FB036 làm cổng xin duyệt đường học hiện tại | 02/1.2: kiểm đường học theo quy tắc hiện hành; không lấy số PASS cũ chứng nhận quan hệ chưa kiểm |

`hop_dong_dieu_hanh.json` là registry phụ thuộc của cổng, không là nguồn quy tắc mới. 01/02/07 tiếp tục sở hữu nội dung; registry chọn quy tắc hiện hành theo chủ đề và liệt kê phần ứng viên chưa đủ điều kiện xin duyệt. QD_022 thay việc hủy toàn bộ bằng chứng theo hash bằng kiểm lại đúng phần chịu ảnh hưởng; sửa chữa hợp lệ không bị khóa. Các con trỏ chuyển tiếp không nhắc quyết định/QA cụ thể tiếp tục dùng nguyên trạng. Kế hoạch, D0, nguồn tham chiếu, receipt và tài sản thiết kế khóa không bị tác động.

| Phát biểu dễ dùng nhầm | Căn cứ/đích hiện hành |
|---|---|
| D0 bắt buộc trước khi vào học; tái sinh từ generator 6B; cần bốn biến thể PDF | D0 tự nguyện, QMD canonical; PDF toàn trang ngày 14/10 là sản phẩm được giao riêng, không là điều kiện vào học |
| Bài học và Luyện tập xen kẽ theo ba chặng | QD_017/01: hai khu vực không xen kẽ; chặng thuộc Luyện tập; xem lại là hỗ trợ |
| Nhật kí mẫu riêng của mỗi gói hoặc schema sáu trường | 01: một nguồn đủ 14 trường; ví dụ trong nguồn có thể cần sửa, không vì thế đổi schema |
| G01 154 vùng, G02 phải bằng G01; mọi khối đều thu gọn | 07/kit: theo nhịp và owner; mạch chính mở cố định, chỉ hộp có trạng thái đóng/mở mặc định đóng |
| Nghiệm thu tháng 9/FB033 hoặc PASS FB035 chứng nhận ứng viên FB036 | 03/hồ sơ: lịch sử nghiệm thu giữ nguyên; bản sửa hiện hành chờ xem |
| N07 chưa rà; nội dung G01 đã hoàn thiện tuyệt đối | Rà đã có 21 RD; DH_011 biên tập nhưng QD_021 mở lại RD01/RD06 và thu hồi xin duyệt sơ đồ. Hiện trạng theo 03/hồ sơ, không theo số PASS |
| Bảng native 0.4 chưa nối nguồn; mọi đồ thị mặc định đổi 0.4 | Bảng/hình đã nối HTML G01/G02; style 0.4 opt-in; G02 canonical theo DH_019, đầu ra chỉ dựng cô lập; PDF chưa đồng bộ |
| Số trang PDF cũ/ma trận lịch sử là chuẩn bất biến | Số trang là kết quả của đúng bản PDF; khi được giao PDF, dựng/kiểm lại nội dung và metadata từ tệp thật |

Giữ Kế hoạch 0.6 nguyên byte. Kế hoạch còn điều hành phạm vi/lộ trình; các trạng thái, checklist gói, chế độ D0 và mô tả sản xuất đã thay phải đọc theo chủ sở hữu hiện hành trên. Không chạy lại phụ lục prompt hoặc khôi phục nguồn cũ.

## 4. Điều kiện kết thúc một lượt đồng bộ

DH_018/QD_027 đưa kit vào đường dựng QMD D0 với map riêng; chỉ thay lớp trình bày. D0 vẫn tự nguyện, giữ nguyên nội dung và receipt. Trạng thái HTML mới pending owner review tại 03/hồ sơ D0, không kế thừa nghiệm thu 2026-10-03. Chỉ dẫn HTML ở `hoc_lieu/d0/giao_dien/README_web_2027.md`; PDF toàn trang theo yêu cầu 14/10 ở `_quy_trinh/README.md` của D0. Không chạy generator cũ hoặc khôi phục bốn biến thể PDF.

QD_023 thay cách xem nhãn chỉ là chữ trang trí, suy chức năng từ heading/class, đếm nội dung theo số vùng và đánh lại số theo chặng. Tên khu vực lấy từ danh mục; tiêu đề/câu chữ/số riêng cần trạng thái duyệt trong bảng áp dụng. Những hợp đồng cho phép Ôn nền nằm dưới Khởi động chỉ là tương thích nguồn chưa di trú, không quy tắc sản xuất mới. Quy tắc học lấy QD_033 cùng phần kế thừa của QD_021; cơ chế thay thế QD_022 giữ nguyên. Không sửa Kế hoạch 0.6, Design 0.4 khóa hoặc nguồn D0/Nhà để triển khai hệ nhãn cục bộ này.

Theo [02](02_quy_trinh_va_nghiem_thu.md): ghi quyết định → xác định tài liệu bị ảnh hưởng → cập nhật chủ sở hữu và các bản tham chiếu/trạng thái máy đọc → kiểm liên kết, mâu thuẫn, trạng thái đúng bản và bảo toàn ngoài phạm vi → ghi bằng chứng ở 03. Không chỉ thêm lời tổng kết trên một README.

Các lỗi nội dung/đường học chưa sửa phải có ID, vị trí, chủ sở hữu và trạng thái riêng trong hồ sơ gói. Đồng bộ tài liệu không là nghiệm thu học liệu, không là xác nhận HTML/PDF/live đã đồng bộ.

### Hiệu chỉnh nhãn ngày 17/10/2026

07/6.2 sở hữu quy tắc nhãn cấp chứa; label_contract.display_contract.context_labels sở hữu từ vựng ghép ngữ cảnh; zo_course_labels.py áp dụng/kiểm. Binding gói sở hữu mode, owner và checkpoint_context. r1-consistency.json/page_roles và nhãn riêng của adapter cũ chỉ tương thích gói chưa di trú, không là chuẩn mới. G04 là phạm vi sản phẩm đang sửa; không suy kiểm kê G01–G03 thành quyền tái xuất bản. 03 tiếp tục sở hữu trạng thái và việc tiếp theo.

### Khép lỗi tài nguyên toán G04 ngày 17/10/2026

07/6.1.2 sở hữu vai trò và component; 02/2.5 sở hữu bước nạp trước viết/chuyển QMD và nghiệm thu. course-math-assets.json là binding máy, zo_course_math_assets.py thực thi; công cụ dựng vẫn ở ZO Math Graphics qua adapter. Gói chỉ sở hữu dữ liệu, nguồn sinh và receipt đúng phiên bản. Không lấy lựa chọn surface của bản G04 cũ, bảng kiểm PASS hoặc JSON rỗng G03 làm thẩm quyền thiết kế. Bản thảo/bìa đã duyệt giữ nguyên; 03 ghi bản sửa đang xem và các giới hạn.

### DRAWER-ICON01

07/6 sở hữu nút mục lục chỉ icon; kit/hop_dong_vung_doc.md ghi hợp đồng đã chốt. Template/CSS/site-ui.js sở hữu hiện thực độc lập với downloads; zo_web_2027_shell.py là cổng dùng chung ở template và post-render. 02 sở hữu kiểm bàn giao; 03 sở hữu trạng thái. Đoạn tương thích trong mô-đun PDF G01/G02 không là nguồn chuẩn cho gói mới.


GRAPH-G03-01: 07/6.1.2 sở hữu khung/tỉ lệ đồ thị do chủ trì chọn; `../zo_math_graphics/graph/profiles/lesson-g03.json` là thông số công cụ duy nhất, `zo_graphics.py` nối công cụ và đặt cỡ, `production-figures.css` hiển thị. G01/G02/G03/G04 và gói mới áp dụng; bản chụp G03 trước sửa là đối chứng. GRAPH-G03-02 giữ nguồn vẽ nhưng sửa lớp hiển thị năm ảnh, không coi đối chứng là lệnh giữ lỗi. Chỉ thay phần cỡ tự nhiên trước đó; không thay BBT hoặc bìa, không suy PDF/phát hành.
