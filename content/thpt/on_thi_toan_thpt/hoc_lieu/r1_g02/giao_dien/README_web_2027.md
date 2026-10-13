# G02 — HTML từ nguồn canonical

Hiện hành DH_021/QD_028: đối sánh theo báo cáo mới tại `_audit/zo_pair_report_2026-10-11/`. Nguồn sửa có mục tiêu; trạng thái QA và HTML theo 03 của khóa, không dùng các kết quả/đường dẫn lịch sử bên dưới chứng nhận bản mới. Chưa PDF học liệu, promotion root docs, Git hoặc phát hành.

Lượt hiện hành DH_020 kiểm lại cả cụm tại `_audit/zo_2027_dong_bo_cum_2026-10-11/`. Không lấy HTML DH_016 hoặc QA DH_019 làm bằng chứng cho nguồn đã sửa. Lệnh dựng cụm: `python scripts/zo_python.py scripts/zo_web_2027_cluster_check.py render --output <audit_mới> --phase final`; chỉ dùng bản sao cô lập, không ghi root docs. Trạng thái và bước tiếp theo lấy ở 03; các đoạn DH_019 trở về trước là lịch sử.

## Đường dựng hiện hành — DH_019

QMD marker `zo-web-2027-g02` gọi `zo_web_2027_g02_production.py` qua hook chung. Nội dung lấy từ raw Quarto mới; map `web_2027_layout.json` sở hữu nhịp, binding `he_nhan.json` sở hữu nhãn/nhiệm vụ. Không đọc HTML docs/audit cũ làm nguồn. Cách học gom chọn nơi bắt đầu/bản đồ/bảng hỗ trợ cùng nhịp như G01; hỗ trợ và chuyển gói là hai nhịp sau. Khởi động cùng một lượt nhưng giữ ID và đáp án riêng; T11 là tổng quan ba chặng Luyện tập, không phải chặng mới.

Khi được giao dựng HTML, dùng `python scripts/zo_python.py scripts/zo_qmd.py render content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g02/index.qmd`; khi chỉ cần kiểm không đổi đầu ra hiện có, dùng `zo_web_2027_pair.py render --package r1_g02 --output <audit_mới>` qua launcher. Không dùng lại audit đã duyệt. `zo_web_2027_g02_sync_check.py preview` chỉ đổi đường dẫn cho bản xem riêng, `parity` đối chiếu kiểu chữ/giấy/bảng trực tiếp G01–G02; `zo_r1_g02_labels_check.py check --browser` kiểm toàn các view và tuyến hỗ trợ. Phải đọc chỉ dẫn vận hành hiện hành trước chạy.

HTML DH_019: `_audit/r1_g02_dong_bo_lai_g01_2026-10-11/html-current/g02-reading.html`; QA tại `qa-verified/qa.json`, đối sánh tại `pair-verified/pair.json`. Chưa chủ trì duyệt, root docs/PDF/Git/phát hành. Các SVG 0.4 dựng từ TeX; PDF trung gian đồ thị không phải PDF học liệu.

## Hồ sơ lỗi DH_019

### Lỗi đã xử lí ở DH_019, không dùng lại kết luận đồng bộ DH_016

| ID | Triệu chứng và nguyên nhân đã xác minh | Nguồn sửa và hàng rào |
|---|---|---|
| SYNC-G02-01 | Cách học bị tách thành nhiều giấy theo h4, dù chọn nơi/bản đồ/bảng hỗ trợ cùng kết quả đọc | `web_2027_layout.json`/`zo_web_2027_g02.py`; guard ba vùng và fixture tách bản đồ |
| SYNC-G02-02 | Thiếu bảng tổng quan ba chặng như G01, chỉ có lời dẫn | QMD/T11, hợp đồng Lua 13 bảng metadata; guard ba hàng và fixture bỏ T11 |
| SYNC-G02-03 | Ôn nền và nhóm Bài học trong Lời giải có nhãn ngoài thừa | `align_reading_roles` trong adapter G02; guard nhãn thừa/lặp và ảnh Ôn nền/Lời giải |
| SYNC-G02-04 | Render QMD G02 trả shell cũ; kit chỉ chạy qua audit | Marker/hook/adapter canonical G02; dựng tươi cô lập và kiểm output, không lấy HTML audit làm đầu vào |
| SYNC-G02-05 | Khởi động chia giấy theo từng nhiệm vụ; tiêu đề h4 to hơn tiêu đề nhiệm vụ cùng chức năng ở G01 | Gom cùng lượt trong map, chiếu tiêu đề nhiệm vụ sang `.r1-task-label`, giữ ID và unit; guard vùng/chức năng, đối sánh computed typography |
| SYNC-G02-06 | Link lời giải ở cuối câu sát nhãn câu tiếp theo khi gom lượt | CSS cục bộ G02 giữ khoảng nghỉ 30px giữa nhiệm vụ; đã xem ảnh `qa-verified/images/khoi-dong-1440.png` |
| SYNC-G02-07 | Điểm dừng lặp tên chặng trong tiêu đề, mục tiêu/tiên quyết khác cách trình bày G01 | QMD dùng tên ngắn và tên mục tiêu đối ứng; binding giữ ngữ cảnh, guard tiêu đề Điểm dừng |

Bằng chứng: `_audit/r1_g02_dong_bo_lai_g01_2026-10-11/qa-verified/qa.json` (965/965), `pair-verified/pair.json` (363/363), `governance-verified.json` (134/134), `protected-final.json` (765 tệp trong snapshot, không thay ngoài bốn tài liệu điều hành được cập nhật). QA/ảnh lỗi trước giữ riêng; không sửa receipt hoặc số PASS để che lỗi. G01 dựng lại đúng SHA-256 `3df96a08a03eb3c1a8d01f8f7208d324e3910ca5c366028415ba322211e3556a`.

Khác biệt toán có chủ đích: G02 giữ mục tiêu/nhiệm vụ/nhánh Chuyển giao, hướng dẫn theo từng chặng và hai xác nhận Nền bổ sung riêng; không ép số vùng/nhiệm vụ bằng G01. Các vùng đó có kết quả đọc riêng và giữ cùng component/cấp chức năng. Đã sửa và kiểm không đồng nghĩa chủ trì đã duyệt; PDF học liệu chưa dựng, root docs không promotion, chưa Git hoặc phát hành. Chưa peer-review toán độc lập toàn gói hoặc kiểm Safari/Firefox/cảm ứng thật/trình đọc màn hình.

## DH_016 — đường thử nghiệm lịch sử trước opt-in

**Tại mốc DH_016 ngày 11/10/2026:** `_audit/r1_g02_ap_dung_he_nhan_2026-10-11/delivery-html/g02-reading.html`, dựng từ QMD mới; chưa promotion. Binding `he_nhan.json` dùng danh mục nhãn chung, 59 nhiệm vụ/59 đáp án; G02 không sao chép số G01. `web_2027_layout.json` chỉ sở hữu nhịp đọc. Ôn nền cấp gốc, mọi disclosure mặc định đóng. Chờ chủ trì duyệt; nguồn toán/ID/manifest và Nhật kí chung giữ nguyên.

Dựng raw mới bằng `zo_web_2027_pair.py raw --package r1_g02 --output <audit_mới>` qua launcher, rồi `zo_r1_g02_labels_check.py build --raw <raw_mới> --output <audit_mới>/delivery-html`. Trước build, dựng hai SVG `do_thi_01/02` từ TeX canonical bằng `zo_graph_build.py --style 0.4 --check --out-dir <audit_mới>/figure-build`; ba SVG bìa/Nền lấy từ assets canonical. Kiểm bằng `zo_r1_g02_labels_check.py check --raw <raw_mới> --before <raw_baseline> --page <HTML> --output <qa_mới> --browser`. Các lệnh đều qua `python scripts/zo_python.py`; không gọi default audit cũ. Xem README audit DH_016 để lấy đúng đường dẫn và bằng chứng. Kiểm kỹ thuật không thay nghiệm thu HTML/PDF.

## FB036 — lịch sử 08/10, không là bản hiện tại

**HTML tại mốc FB036:** `_audit/zo_web_pair_refinement_2026-10-08/g02/g02-reading.html`.
Hồ sơ `_audit/zo_web_pair_refinement_2026-10-08/README.md`; ma trận lỗi
`_design/web_2027_mau_dung_chung/doi_sanh_FB036.md`. QMD/cover TeX là nguồn,
SVG bìa mới có receipt nguồn; mẫu Nhật kí include chung. Pair QA 1504/1504,
ownership 122/122, G02 985/985, toán bổ sung 28/28; chưa nghiệm thu chủ trì.
Phần DH007/FB035 bên dưới là lịch sử, không ghi đè audit cũ để cập nhật.

Mốc FB035 lịch sử: `_audit/zo_g02_consistency_2026-10-08/g02-reading.html`.
FB034 trước đây chưa đạt nhất quán theo phản hồi chủ trì. Bản đồ phân vai
canonical `web_2027_layout.json` thay việc dùng grouping theo số heading
trong prototype lịch sử. Nhật kí dùng include chung, đối chiếu nguyên G01.

### Khi được giao dựng lại sau này

Đọc bộ điều hành/08 và kiểm mã script đang có trước. Dùng thư mục audit mới chưa tồn tại, giữ toàn bộ snapshot/QA cũ. `scripts/zo_web_2027_pair.py` có `--output` cho raw/render; checker pair/layout/semantics hiện còn đường dẫn OUT riêng theo mốc, phải đối chiếu hoặc thích ứng có kiểm soát trong nhiệm vụ kỹ thuật được giao, không giả định mọi checker nhận `--output`. Không chạy default để ghi đè báo cáo FB036. Không promotion G02 vào docs, không dựng PDF hoặc dùng `promote-g01` nếu chưa được giao.

### Lệnh FB035 — ghi lại lịch sử, không chạy để tiếp quản hiện tại

Những đường dẫn dưới đây là thư mục đã tồn tại; không dùng làm đích tái dựng mới. Khi được giao tái dựng, thay bằng một đích mới sau kiểm khả năng tham số của từng công cụ:

```text
python scripts/zo_python.py scripts/zo_g02_completion.py render --output _audit/zo_g02_consistency_2026-10-08
python scripts/zo_python.py scripts/zo_g02_completion.py preview --output _audit/zo_g02_consistency_2026-10-08
python scripts/zo_python.py scripts/zo_g02_completion_check.py --output _audit/zo_g02_consistency_2026-10-08
python scripts/zo_python.py scripts/zo_g02_consistency_check.py --output _audit/zo_g02_consistency_2026-10-08
python scripts/zo_python.py scripts/zo_g02_completion_math.py --output _audit/zo_g02_consistency_2026-10-08
python scripts/zo_python.py scripts/zo_g02_completion.py protected --output _audit/zo_g02_consistency_2026-10-08
```

Assets SVG của audit mới được dựng bởi `build_vectors` như lệnh lịch sử
bên dưới nhưng dùng output `zo_g02_consistency_2026-10-08`. Bản mới có 157 vùng;
đó là thống kê, không phải chỉ tiêu bằng G01. 144/144 semantic, 985/985 bố cục,
28/28 toán bổ sung, 398/398 G01 và 990 tệp bảo vệ không đổi; chờ chủ trì.

## Hướng dẫn mốc FB034 — lưu lịch sử, không dùng làm trạng thái mới

`../index.qmd` là nguồn nội dung, `_quy_trinh/kien_truc_hoc_tap.yml` là bản đồ
mục tiêu/chặng/nhiệm vụ. Không lấy HTML cũ trong `docs` hoặc mẫu 0.4 làm nguồn.

## Dựng lại

Chạy từ gốc repo, theo thứ tự:

```text
python scripts/zo_python.py -c "import sys;sys.path.insert(0,'scripts');from pathlib import Path;from zo_web_2027_g02_payloads import build_vectors;build_vectors(Path('_audit/zo_g02_completion_2026-10-08').resolve())"
python scripts/zo_python.py scripts/zo_g02_completion.py render
python scripts/zo_python.py scripts/zo_g02_completion.py preview
python scripts/zo_python.py scripts/zo_g02_completion_check.py
python scripts/zo_python.py scripts/zo_g02_completion_math.py
python scripts/zo_python.py scripts/zo_g02_completion.py protected
```

SVG Nền có TEX nguồn trong `hinh`; hai đồ thị bài tập dùng TEX đã có, không
đổi dữ kiện. JSON BBT vẫn là `du_lieu/bang_bien_thien.json`. Trình bày native
HTML dùng renderer 0.4 chung, giữ chú thích QMD và đối chiếu hàng dữ liệu.
Cover dùng minh họa nhận diện trong suốt đã duyệt, không phải dữ kiện của bài.
Các PDF trong `figure-build` chỉ là trung gian biên dịch SVG, không phải PDF học liệu.

Kit chung và CSS hình/thẻ tải G01 chỉ được đọc và tái dùng, không fork token.
`support-context.js` chỉ bổ sung dữ liệu đích/nhãn G02, không thay controller chung.
G02 có 153 vùng theo nội dung của nó; không lấy số 154 vùng G01 làm chỉ tiêu.
Snapshot bảo vệ ghi trước khi thay kiến trúc; không ghi đè snapshot khi dựng lại.

## Trạng thái và giới hạn

**DH_026/QD_031 hiện hành:** bản xem cách ly `_audit/zo_pair_backlog_2026-10-11/html-current/g02-reading.html`; source/DOM guard trong adapter kiểm ownership và thứ tự thực, không quota vùng. Toàn bộ năm hình dựng mới từ TeX/profile 0.4, manifest đầy đủ trong delivery; cache SVG canonical cũ không còn là runtime input. Kiểm/báo cáo mới cùng thư mục; chờ chủ trì duyệt. Đoạn trạng thái bên dưới là lịch sử DH_007, không phải cổng vận hành hiện tại; số vùng là thống kê từng bản, không chỉ tiêu cố định.

HTML mới ở `_audit/zo_g02_completion_2026-10-08/g02-reading.html`, chờ duyệt.
Không có post-render production G02 được bật trong `_quarto.yml` ở lượt này.
Chỉ sửa nguồn G02, năm thẻ Nền mới và hồ sơ tác nghiệp; nguồn G01/Nhà/D0 giữ nguyên.

Tám PDF đã có vẫn là bản cũ, số trang được đọc trực tiếp, HTML thông báo chưa
đồng bộ. Các ngưỡng kiểm kê PDF trong Lua/checker lịch sử cần được cập nhật và
kiểm bằng PDF thật ở nhiệm vụ PDF sau duyệt; không nới checker để báo PASS
trong lượt HTML. Các ranh giới phần trong QMD đã được sửa theo thứ tự nguồn mới.
Không gọi bộ kiểm thành phần lịch sử là checker nghiệm thu DH_007.

Nguồn mới và giao diện thử nghiệm chưa phải bản xuất bản; chưa commit/push,
không tiếp tục Video/M8.R, chưa khóa Ngôn ngữ thiết kế 0.5.
