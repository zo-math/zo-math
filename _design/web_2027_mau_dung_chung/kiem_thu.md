# Kiểm và bàn giao mẫu web 2027

## GRAY-NAV01 — mục lục phải ở lại khi cuộn trong chế độ xám

Triệu chứng được chủ trì báo ngày 14/10/2026: điều hướng trang biến mất
khi cuộn về cuối trong chế độ xám–trắng. Nguyên nhân là `filter` trên
`body` đổi containing block của phần tử fixed, khiến rail cuộn theo trang.
Sửa canonical tại `web-shell.css`: lọc trên `html.grayscale`, giữ toàn bộ
trang sắc xám và vị trí điều hướng theo viewport. Không lọc body hoặc
tổ tiên bao thanh điều hướng cố định.

`scripts/zo_web_2027_grayscale_check.py` kiểm trình duyệt thật trên D0,
G01/G02 (Bài học), sáu nền, desktop 1440/1000, đầu/giữa/95%/cuối trang:
rail nhìn thấy, bấm được, geometry như bản màu, toolbar còn ở đầu viewport.
Mobile 390 kiểm drawer ở cuối trang và Escape. Fixture âm đưa lại filter
trên body phải làm phép kiểm thất bại, bỏ fixture phải phục hồi.
`zo_web_2027_bundle.py build` bắt buộc chạy guard này trước bàn giao.
Kiểm chỉ bật/tắt xám ở đầu trang trước đây không đủ để bắt lỗi này.

## HOM-S01 — ghép Nhà mới với học liệu cũ và đổi ảnh bìa trên mobile

Triệu chứng: Home dịch vụ mới lấy ba đích từ `_audit/home-preview`, bỏ qua
lượt nguồn/hover đã sửa ở DH_039; đồng thời breakpoint 760px đổi bìa 3x4
sang một bản 1x1 khác. Nguyên nhân nằm ở khâu chọn ứng viên preview và
hợp đồng hai ảnh của QMD/profile/normalizer/CSS, không ở nội dung toán.

Sửa canonical: Home chỉ khai một ảnh 3x4; normalizer/checker từ chối ảnh
thứ hai, CSS không ẩn ảnh này trên mobile, profile chọn đúng ảnh và minh
họa dịch vụ mới. Bộ xem dùng `zo_web_2027_bundle.py` dựng mới cả bốn trang
từ một snapshot; không nhận HTML lịch sử làm nội dung. Manifest khóa nguồn,
HTML và từng tài nguyên; kiểm đích menu/thẻ/quay lại trong cùng bộ. Ca âm
nguồn lệch bị bắt, thiếu/thay ảnh vẫn bị guard Home từ chối. Dọn mirror và
tài nguyên delivery không được dùng sau dựng; không dọn QD_035.

Hai kiểm câu chữ cũ được thay bằng kiểm đúng vùng hỗ trợ hiện hành (trợ
giúp linh hoạt rồi quay lại chỗ dừng) và danh mục thật: tám mạch không giả
link mở học liệu, thẻ khớp mã gói canonical. Không sửa lời văn để đạt kiểm.
Kết quả/giới hạn và chủ trì duyệt/phát hành phân biệt tại bảng 03.

## Home — HOM-L01, chuyển bố cục đọc đã duyệt vào nguồn, 14/10/2026

Nguồn là QMD native/CSS Home/generator, không HTML mẫu. Mẫu thử chỉ dùng
đối chiếu; SVG học trực tiếp được chép vào tài nguyên khóa, kiểm SHA-256
khớp trước khi nạp qua Markdown. Không tạo include hay runtime audit.
Normalizer giữ class layout do QMD khai, chuẩn hóa ảnh/caption thành một
ảnh có alt/kích thước; không chứa câu chữ biên tập. Giữ CTA-only của HOM-C01.

Guard thay đúng phép kiểm bố cục cũ: intro trong hero, catalog rồi Cách học,
sáu panel xen trắng/xám, không nhãn động từ; bốn hàng Cách học đủ heading/
hai đoạn, tám mục kiến thức và bốn FAQ riêng. Runtime đo một cột/full-width/
khoảng cách/viền/bo góc/nền, kiến thức hai cột desktop–một cột mobile, FAQ
mở không cắt chữ, ảnh đúng tỉ lệ. Tiêm CSS bốn cột phải bị bắt trên desktop
và mobile. Không chữa tràn bằng giấu overflow hoặc nới guard.

Đối chiếu tường minh bản trước và bản mẫu: lời văn/toán/headings/disclosures
theo owner, các đích và ID cũ, DOM thẻ giữ nguyên. Riêng catalog giữ lời
QMD hiện tại thay lời mẫu cũ; phục hồi `trạng-thái-triển-khai` trên câu thông
báo đã có để liên kết hoạt động, không đổi câu chữ. Không dùng chỉ số PASS
thay nghiệm thu. Các guard câu chữ nguyên văn cũ không khớp lời chủ trì sửa
vẫn báo riêng; không ép đổi chữ hoặc hạ guard để làm toàn bộ Home PASS.
Bằng chứng/bản cuối và giới hạn ở 03; không sửa ba trang học liệu hoặc PDF.

## Home — HOM-C01, chỉ dòng hành động mở học liệu, 14/10/2026

Chủ trì thay hành vi thẻ phủ link của HOM-R01: bấm ảnh, tiêu đề, mô tả
hoặc nền thẻ không mở trang. Nguyên nhân hiện trạng là generator bọc cả
thẻ bằng `a.home-card-link`, không phải handler JS. Nguồn sửa là generator
`zo_web_2027_home_landing.py`, CSS Home và checker; partial được sinh lại.
Giữ bố cục/hover viền–bóng–màu tiêu đề. Chỉ `a.home-card-action` có href,
tên truy cập gồm hành động và tiêu đề; hover đổi màu/nhích mũi tên, không
nền sáng hoặc gạch chân; focus bàn phím rõ, reduced-motion không chuyển động.

Guard hiện hành thay guard whole-card-link bên dưới, không sửa QA lịch sử:
chặn anchor phủ thẻ, role/tabindex/handler điều hướng trên vỏ thẻ, thiếu
CTA; kiểm pointer thật trên ảnh/tiêu đề/mô tả/nền, CTA đúng đích, Tab/Enter,
hover giữ geometry, no-JS, lọc/tìm và màn hình hẹp. PDF D0 mới còn chờ duyệt
không trở thành bộ tám PDF R1 hay đổi CTA khảo sát; ngoại lệ nhận diện chỉ
cho D0 đúng trạng thái/hợp đồng, không nới kiểm tám PDF của R1. Bản xem,
kết quả và phần chưa kiểm ở 03; không sửa QMD câu chữ hoặc ba trang học liệu.

## Home — HOM-R02, áp dụng bản câu chữ đã duyệt ngày 12/10

Triệu chứng: chữ đọc vẫn khó hiểu sau HOM-R01, có “D0”, “R1”, “định vị”,
“mạch ôn” và Điểm dừng chưa giải thích. Nguyên nhân: template mới chỉ sửa
một phần, thẻ vẫn lấy mô tả YAML cũ; generator còn in mã gói/mạch, guard
chỉ chặn vài câu nên QA 255/255 không phát hiện. Chủ trì bác bỏ bản ấy,
sau đó duyệt toàn bản viết lại dành cho học sinh trong hội thoại.

Nguồn sửa: template, YAML mô tả Home, generator, metadata trang và nhãn
mục lục Home. Không sửa shared support/CSS/JS, mã/URL/ID thật, cấu hình
mốc đồng hồ hoặc nguồn D0/R1. Guard Home chặn mã nội bộ trong chữ hiển thị,
giữ kiểm trạng thái/danh mục thật, sự tự nguyện của khảo sát, Kiểm tra tự
làm không chia buổi, tài nguyên/PDF và giải thích Điểm dừng. Ca âm thêm
“Gói khảo sát D0” phải FAIL. Guard câu chữ cũ được thay đúng phạm vi bản
đã duyệt, không giữ điều kiện buộc viết D0 vào FAQ.

Bằng chứng ở `_audit/zo_home_copy_approved_2026-10-12/`: so độc lập từng
đoạn/tiêu đề/câu hỏi với bản duyệt, kiểm browser và hash ngoài phạm vi.
Đối chiếu đúng câu chữ không là thí nghiệm đọc hiểu trên học sinh thật;
duyệt bản viết không tự thành duyệt HTML hoặc phát hành. QA cũ giữ nguyên.

## Home — lỗi HOM-R01 và tinh chỉnh sau phản hồi buổi sáng 12/10

Triệu chứng: “ngày còn lại” rớt dòng/căn chân; các liên kết hiện hộp sáng khi
hover, có gạch chân trong đồng hồ/menu; thẻ không phản hồi toàn vùng; câu
chữ điều hành khó hiểu và danh mục đứng sau đoạn giới thiệu dài.
Nguyên nhân đã xác minh: nhãn `max-width:6ch`/`align-items:baseline`; rule
`a:hover` chung trong reading-regions và hover/underline course-navigation;
thẻ có hai link nhỏ, chưa có trạng thái tương tác của article; câu chữ/thứ tự
có ngay trong template/YAML/generator, không phải do cache trình duyệt.

Nguồn sửa: template/YAML Home, generator `zo_web_2027_home_landing.py`,
CSS Home riêng và checker tương ứng. Các CSS shared, logo/font, mốc đồng hồ,
D0/R1/root docs/PDF/receipt không đổi. Không áp sửa Home thành tuyên bố đã
khép lỗi hover trên cả bốn trang; phạm vi ba trang khác chưa xử lí ở lượt này.

Guard: catalog ngay sau hero/trước purpose; một anchor native bao ảnh/nội dung,
không nested link, tên truy cập từ heading; fixture mất anchor/đảo thứ tự phải
FAIL. Browser kiểm pointer hover không nền/gạch chân/nhảy geometry, focus,
click thật trên ảnh khi không JS, label ngày nowrap/13px/căn tâm trên sáu
viewport. Kiểm lại timer hiện có, links/footer/catalog/theme; lưu QA đầu và
QA cuối riêng. Hồ sơ `_audit/zo_home_refinement_2026-10-12/`.
Đã sửa/đã kiểm/chủ trì duyệt/phát hành là các trạng thái riêng, không sửa QA cũ.

## DH_028 — Home biên tập theo tài liệu nhập

Lỗi chống tái diễn: không thực thi HTML/JS nhập, không để danh mục sáu thẻ
mô phỏng thay metadata thật; không trình mốc tạm như lịch chính thức, không mở đăng ký
dịch vụ đang chuẩn bị; không quay về Home cũ do dùng guard nhóm đọc cũ.
Nguồn mới: template biên tập canonical, generator và adapter Home riêng;
guard `zo_web_2027_home_landing_check.py` khóa projection/nguồn/danh mục/
runtime/anchor/footer, có ca âm mất thẻ, footer, ảnh hoặc ID. Home checker
điều phối theo marker bố cục, không áp điều kiện ảnh bìa toán cho minh họa
ý niệm. Bảng mới chưa phân loại vẫn bị guard bảng chung chặn.

Trong lượt xem ảnh phát hiện nút mục lục có lại dòng chữ từ template cũ:
nguyên nhân nhánh Home mới chưa đặt modifier chỉ-icon, không phải yêu cầu
thiết kế mới. Đã đặt modifier/aria-label ở nguồn adapter, CSS scoped và thêm
guard DOM + computed style. Bản cuối phải dựng lại từ nguồn, không sửa HTML.
Kiểm sáu độ rộng, no-JS, thao tác lọc/tìm/FAQ, link sang ba học liệu, menu/
drawer/Top, sáu nền/Sắc xám, phóng 200%, ảnh nguyên tỉ lệ và footer. Giữ QA
đầu và QA cuối riêng; kiểm ảnh trước bàn giao. Không dùng PASS làm nghiệm thu,
PDF hoặc phát hành. Hồ sơ ở `_audit/zo_home_redesign_2026-10-12/`.

### Đồng hồ Home — guard được thay đúng phạm vi

Yêu cầu 12/10 cho phép đồng hồ chạy tới mốc tham chiếu 2027 từ lịch Toán
2026 đã xác minh. Guard cũ “Chờ xác minh lịch thi chính thức” không còn là
điều kiện bắt buộc; thay bằng kiểm status/target/time/chú thích/link nguồn
đúng cấu hình duy nhất. Không thay receipt hoặc QA lịch sử để báo PASS.
Ca âm: năm 2026, offset thiếu/sai, lệch ngày tham chiếu, ngày không hợp lệ,
gắn nhãn official cho mốc tạm, bỏ cảnh báo; chế độ official có fixture riêng.
Browser kiểm tick thật, phép chia ngày–giờ–phút–giây, mượn phút, lệch tick
do quay lại tab, mốc sát hạn, hết hạn không âm/không khẳng định đang thi,
khôi phục, reduced-motion, timer không live từng giây và no-JS trung thực.
Hồ sơ riêng `_audit/zo_home_countdown_2026-10-12/`; giữ kiểm sáu kích thước,
điều hướng/theme/catalog/footer, nguồn tươi và bảo toàn D0/R1/root docs/PDF.
Giờ theo thiết bị; không nhận là đồng bộ NTP hay nghiệm thu screen reader.

## NAV-H01 — đồng bộ hover điều hướng, 14/10/2026

Triệu chứng: danh sách toàn khóa trên D0/G01/G02 còn nền sáng khi hover
và gạch chân mục hiện tại. Nguyên nhân: HOM-R01 chỉ ghi đè CSS Home;
`course-navigation.css` dùng chung vẫn giữ hai quy tắc cũ. Không phải
lỗi câu chữ hoặc nguồn QMD, không sửa HTML sinh trực tiếp.

Nguồn sửa: CSS điều hướng chung; mục hiện tại nhận diện bằng chữ đậm và
`aria-current`, hover chỉ đổi màu chữ/icon, focus bàn phím vẫn có outline.
Guard `zo_web_2027_navigation_check.py` đo pointer thật trên cả bốn mục
và ba icon, trạng thái thường/hover/current, hình học không đổi, focus
Tab và no-JS. Ca âm đưa lại nền/gạch chân/bóng phải bị phát hiện, kể cả
CSS cũ được tiêm trong browser. Không thay rail, heading hoặc nội dung.
Bằng chứng/bản xem và trạng thái ở 03; PASS không là chủ trì duyệt/phát hành.

## QD_032 — điều hướng toàn khóa học

Lỗi: hai điều khiển chữ không đúng chức năng, không có đường trực tiếp giữa gói; nguyên nhân là toolbar chỉ có Home và anchor mang tên thương hiệu. Nguồn sửa: module điều hướng chung và bốn adapter, CSS/JS scoped; không sửa generated HTML trực tiếp. Guard `zo_web_2027_navigation_check.py` phải bắt ca âm thiếu/sai thứ tự điều khiển, sai đích, thiếu current-page, mở sẵn hoặc còn link legacy. Build fail nếu catalog đổi mà binding chưa cập nhật hoặc main/rail/footer/logo đổi trong phép nối.

Kiểm browser 1440/1000/768/430/390/320 px: hình học, danh sách đóng mặc định, Enter/Escape/focus/pointer, đích thật và current-page, Top giữ URL/view, no-JS, chọn nền/sắc xám và drawer gói. Đối chiếu text/heading/math/ID/disclosure main với bằng chứng lượt trước, hash QMD/root docs/PDF/receipt/Git index trước–sau. Lưu lỗi QA đầu và kết quả sửa, không ghi đè bằng chứng. Đạt kiểm không đồng nghĩa chủ trì đã nghiệm thu hoặc phát hành; không bao gồm kiểm toán toàn bộ toán/PDF. Hồ sơ mới ở `_audit/zo_course_navigation_2026-10-12/`.

## QD_031 — lỗi tồn đọng hai gói

`zo_web_2027_backlog_check.py` kiểm thứ tự nguồn/DOM Toàn văn, Nhật kí owner độc lập/14 trường, cây nhóm Sửa lỗi/số theo thứ tự, đích routing đúng tiêu đề và hành động đề–đáp án theo vùng sở hữu. Ca âm link cục bộ dư, Journal nhét vào Review, Sau Ôn lại đặt trước và đích sai số phải FAIL. `zo_r1_g01_labels_check.py`/`zo_r1_g02_labels_check.py` dùng cùng predicate local-pair; không còn ép link hai chiều cho mọi đáp án. Guard không đồng nhất “cùng trang” với “cùng vùng”. G02 dựng đủ năm SVG với profile 0.4, manifest hash nguồn/style/font/palette/khung/đầu ra; cache bìa một mình không chứng nhận bộ hình. Chỉ xem bản mới sau QA từ raw tươi và browser; các kết quả lịch sử giữ nguyên. Trạng thái/điểm xem tại 03/DH_026.

## Căn bậc hai và font toán — lỗi RAD-01, 11/10/2026

Phạm vi kỹ thuật: kit HTML 2027 trên Nhà/D0/G01/G02, không nâng chuẩn toàn repo hoặc sửa biểu thức LaTeX. `Math` không còn được dùng làm alias font custom đang hoạt động: CSS hiểu tên không đặt trong chuỗi này là generic `math`, dẫn tới Cambria Math thay STIX trên Edge. Alias `ZOMath` chọn đúng tài sản STIX 0.4 đã có; không đổi tệp font khóa.

Với căn inline trực tiếp có số mũ, glyph native chọn quá cao: sign 0,8em và con trực tiếp 1,25em giữ nguyên cỡ toàn bộ radicand. Không transform, clipping, dịch baseline hoặc sửa cây MathML. Chỉ dùng selector chung trong `web-shell.css`; căn bên trong phân số/mũ, căn lồng, phân số dưới căn và công thức block giữ native. Đây là bù typography có phạm vi, không giảm cỡ mọi công thức.

`zo_math_notation.py` chặn alias sai, thiếu một vế bù cỡ, transform/clipping và CSS inline cũ; cả bốn adapter gọi cổng. `RADICAL_GEOMETRY`/`radical_geometry_errors` là phép đo dùng lại cho browser QA: kiểm cỡ chữ dưới căn, phần dư chân căn theo variant STIX, bao chứa và baseline. Phải đo font thực bằng DevTools, không chỉ đọc tên CSS hoặc `document.fonts.check`. Thử âm dư chân căn/thu chữ phải FAIL. Kiểm căn trong phân số không nhận rule mới, cùng hồi quy bảng và tràn trang. Bằng chứng/trạng thái lượt này theo 03/DH_024; QA cũ chỉ đếm căn hoặc kiểm baseline không chứng nhận tỉ lệ glyph đã cân đối.

Nguồn sửa: `reading-regions.css`, `web-shell.css`, `zo_math_notation.py`, cổng adapter Nhà/D0 và **chỉ checksum/binding hai CSS** trong layout G01; không đổi vùng đọc, QMD, toán/ID, dữ liệu bảng, receipt đã duyệt, root docs hoặc PDF. Bản HTML mới cần chủ trì xem; Safari/Firefox/thiết bị thật chưa kiểm.

QD_030: kiểm đủ bảng của bốn trang theo `profiles/course-tables.json`, đối chiếu từng ô/chức năng với nguồn và bảng toán JSON. `zo_course_tables.py --self-test` kiểm độ phủ/binding và từ chối bảng chưa phân loại. Runtime đo theo loại (không dùng guard “mọi header trái” cũ cho bảng giá trị/dấu/ma trận), lưới/cỡ chữ/màu/MathML, cục bộ cuộn và không tràn trang; kiểm tất cả view và disclosure đã mở. Ca âm mất binding, role sai, lưới mất hoặc căn sai phải FAIL. Không sửa receipt lịch sử; HTML mới chờ xem, PDF chưa đồng bộ. Evidence lượt hiện hành ở 03.

**QD_025:** trước di trú chạy `zo_learning_architecture.py labels --self-test` qua launcher: kiểm dictionary/schema/bảng source hiện tại, số toàn nhóm, đơn vị dùng lại và đề–đáp án. Sau áp dụng G01, dùng `zo_r1_g01_labels_check.py --audit <thư_mục_dựng_cô_lập> --browser` qua launcher để kiểm nguồn tươi/HTML/binding, owner Ôn nền, 69 nhiệm vụ/62 đáp án, số liên tục, ID cũ, không nhãn/giấy lồng, disclosure đóng và đường quay về. Gợi mở không có đáp án sao chép lời giảng. Đây không là duyệt của chủ trì, kiểm toán độc lập hoặc nghiệm thu PDF. Không dùng PASS FB036/receipt lịch sử chứng nhận bản mới; số lượng G01 không là quota gói khác.

QD_033: trước kiểm xin duyệt, chạy `scripts/zo_2027_governance_check.py` qua `scripts/zo_python.py`. Kiểm quan hệ link sơ đồ, nhánh và 14 ca trong 01/2.2.2, không chỉ từ khóa/độ rộng/số vùng. Kiểm quyền chọn điểm vào, hỗ trợ độc lập, kết thúc lượt Kiểm tra và giữ riêng bài làm trước nhận trợ giúp, lưu bằng chứng khác ghi Nhật kí, cùng link quay lại chỉ khi đề–đáp án tách vị trí. QA QD_021/465/465 không chứng nhận nguồn/HTML đã đạt QD_033. QD_022: kiểm lại các phép kiểm đường học bị ảnh hưởng; phần trình duyệt không liên quan có thể dùng lại khi đầu vào và phép kiểm tương ứng không đổi. Không hủy toàn bộ QA vì hash điều hành đổi; tài liệu và sản phẩm ghi kết quả riêng. Các bằng chứng FB bên dưới thuộc mốc lịch sử, không thay trạng thái ở 03.

Phạm vi hiện hành: Nhà/G01/G02/D0 đã tích hợp adapter canonical opt-in, mọi đầu ra lượt này dựng cô lập từ nguồn; Edge headless `file://`. Không phải kiểm website đã xuất bản. Các kết quả/giới hạn từng mốc giữ riêng, không dùng PASS preview chứng nhận production khác.

D0 DH_018 dùng `zo_web_2027_d0_check.py`: kiểm receipt toàn văn/TeX năm khu vực,
24 câu/Bài 00/25 đối chiếu, map nhịp riêng, nguồn/tài sản tươi và fixture mất
công thức/ID/câu chữ. Browser bảy độ rộng, năm view/all-open/no-JS, header
bảng trái, vòng đề–đối chiếu–quay lại–reload–Back, hình/bảng cuộn cục bộ,
đích học liệu, drawer/keyboard/resize/nền/persistence/scroll. Kiểm ngân hàng,
25 tệp baseline và toán 48/48 bằng checker D0 riêng. Nghiệm thu nội dung/HTML
cũ giữ nguyên; HTML mới chờ chủ trì xem. Không PDF nội dung hoặc phát hành.

## Nhà sau DH_017

Dùng `zo_web_2027_home_check.py rebuild/preview/check --browser` qua launcher; chỉ dựng từ QMD/data/partial hiện hành, chưa promotion root docs. Kiểm đủ projection/ID/thứ tự, map vai trò, không nhãn trùng, giấy lồng hoặc orphan; canonical links/bat-dau và preview tới HTML G01/G02 tường minh; bìa SVG trong suốt/khung token riêng, footer đầy đủ, không controller R1. Edge 1920/1440/1000/768/430/390/320px: cột/inset/tràn/ảnh, cuộn ổn định, controls và persistence, drawer Enter/Escape/focus/resize, no-JS navigation còn hiện. Fixture kéo heading ra giấy, lặp nhãn và xóa footer phải bị bắt. Builder danh mục phân biệt bản xem trước với nghiệm thu; không đổi profile gói để vượt kiểm. Lỗi no-JS mobile do `.rail nav` từ CSS tương thích được chữa bằng selector Home-only, không nới checker hoặc sửa shell G01/G02. Báo cáo mới theo 03, không ghi đè các mốc FB.

## G02 sau áp dụng DH_016 — kiểm riêng theo vai trò

`zo_r1_g02_labels_check.py build/check` qua launcher dựng từ raw QMD mới và binding canonical G02; kiểm 59 nhiệm vụ/59 đáp án, dãy liên tục, 14 trường Nhật kí, owner Ôn nền cấp gốc, DH01–DH14 ở mức nguồn/đích/câu chữ, công thức/ID cũ và fixture lỗi cố ý. Trình duyệt kiểm 12 view ở 1440/430/390/320px, tuyến hỗ trợ/quay về và no-JS; không ép G02 có 69 nhiệm vụ, Gợi mở hoặc số vùng G01. Thẻ tải có trục riêng của ô tiêu đề/mô tả: giữ kiểm orphan/overflow và kiểm riêng ba cột, nút 44px/mobile; không ép heading trong thẻ lên trục prose ngoài thẻ. Không nới ngoại lệ cho các vùng nội dung toán.

Mốc hiện tại và báo cáo ở 03/profile G02. Không dùng báo cáo này nghiệm thu PDF, production, Safari/Firefox, thiết bị thật hoặc kiểm toán độc lập toàn gói. Kiểm tương thích helper mặc định G01 ghi riêng, không sửa receipt G01 để khớp hash mới.

Trạng thái/nhiệm vụ theo [bảng điều hành khóa](../../content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md). Phần FB033/FB027/FB028 dưới đây giữ phép kiểm đúng mốc lịch sử; bản sửa FB036 dùng mục cuối, không tự cập nhật receipt cũ. Hợp nhất tài liệu ngày 10/10 không chạy lại browser QA hoặc mở render.

## Kiểm mốc duyệt lịch sử G01 từ nguồn — FB033

```text
python scripts/zo_python.py scripts/zo_web_2027_g01_checkpoint.py check --output _audit/zo_g01_checkpoint_check
python scripts/zo_python.py scripts/zo_web_2027_g01_checkpoint.py rebuild --output _audit/zo_g01_checkpoint_rebuild
```

`check` đối chiếu receipt chủ trì đã duyệt; khóa bytes HTML, runtime, nội dung/MathML/ID, nguồn trình bày, 154 vùng và nhật kí 14 trường. Có guard orphan/nested paper, tám PDF thật, cảnh báo freshness, fixture heading/link/inset. Edge kiểm 12 view, mở disclosure, tràn/giấy trắng/hình tải, bốn viewport, thẻ tải, drawer Enter/Escape/focus, sáu nền/Sắc xám, trace toolbar và no-JS. Hash khóa hình/bảng/nguồn; checker này không thay phép xác minh toán hoặc chứng minh mọi nhãn vector không chồng lấn.

`rebuild` dùng **chỉ nguồn repository**, không seed từ audit mirror/HTML cũ/docs. Render đúng QMD G01 bằng CLI cấu hình trong thư mục tạm, dùng index riêng; kiểm đầu ra với cùng receipt rồi dọn mirror. Không promotion khi kiểm xong, không ghi đè HTML đã duyệt. Các gói khác/PDF/index và đầu ra G01 phải nguyên trạng. Mốc không được tự đổi để cho PASS; muốn cập nhật receipt cần nhiệm vụ và duyệt mới. `seal` là thao tác ghi nhận duyệt có SHA và lời chủ trì, không thuộc build thường.

Bằng chứng lượt này: `_audit/zo_g01_html_checkpoint_2026-10-08/`. Các audit FB031/032 giữ làm lịch sử kiểm chi tiết, không là phụ thuộc chạy của checker mới. Mã chính thức trong `scripts/` và receipt trong nguồn; việc có tệp trong repo không đồng nghĩa đã commit.

## Các nhóm hàng rào

| Rủi ro đã gặp | Phép kiểm hiện hành |
|---|---|
| Nội dung/ID/luồng biến đổi khi tổ chức vùng | Projection nguyên văn/thứ tự/MathML/ID/heading/disclosure; dữ liệu canonical Nhà; ba gói đúng thứ tự D0–G01–G02; G01 12 view và nhánh quay về |
| Heading/nhãn/link rơi ngoài vùng | Kiểm DOM sở hữu trong `.reader-content`; ca âm chủ động kéo heading ra ngoài phải bị phát hiện |
| Thụt ra/vào hoặc giấy lồng | Đo trục nhãn/heading/summary, độ rộng, vùng lồng và khoảng nghỉ; ca âm thêm inset phải bị phát hiện |
| CSS cũ còn nạp hoặc selector mất sau tách | Khóa danh sách stylesheet, đối chiếu hash nguồn/đầu ra; so computed geometry và typography G01 kit với bản đã duyệt |
| Tràn khi mở lời giải hoặc hình bị giãn | Mở mọi disclosure khi đo rồi trả trạng thái; kiểm tràn cục bộ, toàn trang và tỉ lệ `--figure-em` |
| Mô tả thẻ bị ép cạnh thumbnail | Đo mô tả dùng hết bề rộng đọc ở mọi viewport; cover chỉ thuộc phần nhận diện |
| Giấy hòa với nền | Sáu lựa chọn nền, giấy luôn trắng, lựa chọn hiện hành, chế độ sắc xám |
| Navbar mất/giật; review trộn journal | Trace cuộn toolbar/rail/nút mobile; Ôn lại/Nhật kí riêng; reload/deep-link/quay lại |
| Drawer khó dùng hoặc mất điều hướng sau resize | Enter, Escape, trả focus, link đúng đích không bị toolbar che, resize trả nav về rail; R1 bàn phím lên/xuống |
| Nội dung thiếu khi không JS | Nhà đọc trọn/mục lục sẵn có; G01 không giấu các phần nguồn khi thiếu controller |
| Phụ thuộc hoặc sửa production ngoài phạm vi | Manifest tài sản/font/license/link/hash; kiểm protected-before gồm nguồn, docs, bản G01 duyệt và tài sản khóa 0.4 |
| Footer website mất khi thay shell | Kiểm đúng `footer#site-footer[role=contentinfo]` ngoài `main`/Ủng hộ; đủ ba link thông tin, ba kênh và bản quyền từ cấu hình đang dùng; ca âm xóa footer vẫn phải FAIL dù còn prototype-note |
| Bổ sung footer làm đổi thiết kế đã duyệt | Khóa DOM phía trên, hash CSS/JS/template/profile cũ, so toàn bộ hình học/chữ/màu và ảnh trước–sau; CSS footer chỉ có selector cục bộ; G01 đối chứng byte-identical |
| Footer mobile bị nút mục lục che | Tại cuối trang: link không tràn/che, đích 44px, focus bàn phím rõ, no-JS còn đủ link; kiểm năm độ rộng và sáu nền/sắc xám |
| Tùy chỉnh tiếp tục dư chữ/ẩn lựa chọn hoặc bỏ Sắc xám | Sáu radio màu + nút biểu tượng Sắc xám trực tiếp một hàng, không summary/chữ hiện; kiểm vòng chọn, tên truy cập, aria-pressed, vùng bấm ít nhất 24×44px, không đè logo, pointer/ArrowRight/Enter/reload |
| Câu nhận diện lệch giữa rail/footer/trang khác | So đúng `BRAND_THOUGHT` đầy đủ; không còn câu viết tắt tại các điểm nhận diện đang dùng, giữ mốc cũ để đối chiếu |

Kiểm trình duyệt ở 390, 768, 1000, 1440 và 1920px. Chụp và xem các cảnh desktop/mobile: bìa, định hướng, cách học, tám mạch, danh mục, điểm bắt đầu, ủng hộ, drawer và G01/BBT. Việc PASS tự động không thay nghiệm thu trải nghiệm của chủ trì.

## Vận hành

Lệnh dựng/kiểm ở [README](README.md). Cần các thư viện Python hiện có `beautifulsoup4`, `PyYAML`, `requests`, `websocket-client`, `Pillow` (so ảnh footer) và Edge đã cài; không tự cài trình duyệt/thư viện. Mọi lệnh Python qua `scripts/zo_python.py`. Checker tạo và đóng **một process headless riêng**; không tương tác với profile/tab của người dùng. Đầu ra QA và ảnh nằm cùng preview, không ghi vào production.

Nếu browser bị sandbox chặn, không xem đó là lỗi HTML đã xác minh và không báo “đã kiểm trực quan” trước khi có ảnh. Chỉ xin quyền chạy chính checker cần thiết; không tắt sandbox của browser hoặc sửa security hệ thống. Hồ sơ tạm phải phân biệt run hiện hành với phần dư từ run lỗi; phần chưa dọn được ghi rõ, không che bằng một cờ cleanup chung.

Một lần kiểm mới ghi hash đầu vào runtime, hash checker và giới hạn. Nếu thay HTML/CSS/JS thì kết quả cũ không chứng nhận bản mới. Kiểm dựng lặp lại phải cho cùng hash runtime với cùng nguồn. Tệp template `.html.tpl` là nguồn có thể quản lí trong Git; HTML audit là đầu ra, không canonical.

## Ghi lỗi và trạng thái

DH_019 bổ sung kiểm G02: cùng ba vùng Cách học như G01, Khởi động cùng một lượt đọc giữ đơn vị nguyên tử, T11 tổng quan ba chặng Luyện tập, không nhãn ngoài Ôn nền dư/nhãn lặp tiêu đề. Fixture bỏ T11 hoặc tách bản đồ Cách học phải FAIL. Đường dựng QMD có marker và adapter G02 canonical, không phụ thuộc HTML audit. `zo_web_2027_g02_sync_check.py parity` đo trực tiếp giấy và typography h2/h3/h4/nhãn/prose/header bảng trên hai HTML hiện hành; khác số câu hoặc đối tượng toán không là lỗi đồng bộ. Kiểm 12 view × 4 độ rộng và các tuyến hỗ trợ bằng `zo_r1_g02_labels_check.py`; xem ảnh trước bàn giao. Bằng chứng tại `_audit/r1_g02_dong_bo_lai_g01_2026-10-11/`, không thay QA/receipt lịch sử.

Với lỗi đã xác minh/xử lí, ghi triệu chứng/phạm vi, nguyên nhân, nguồn sửa, guard, bằng chứng và phần chưa kiểm vào sổ phản hồi hoặc báo cáo liên kết từ sổ. Lỗi hạ tầng kiểm không được gán nhầm thành lỗi trang. Phân biệt **đã sửa → đã kiểm → chủ trì duyệt → tích hợp → phát hành**; không đóng mọi trạng thái chỉ từ con số PASS.

Giới hạn đã ghi: chưa Safari/Firefox, cảm ứng thật hoặc screen reader. Nhà/footer và FB027 đã được chốt qua FB028; không hạ lại trạng thái ấy. G01 đã nối nguồn HTML, G02 đã có adapter canonical từ DH_019, các bản sửa hiện hành chờ xem theo 03; D0 đã tích hợp opt-in ở DH_018. Các tuyên bố “production/G02 giữ nguyên” trong phép kiểm lịch sử chỉ áp dụng lượt đó. PDF chưa đồng bộ; chưa phát hành/khóa 0.5.

Đối chiếu ảnh footer chụp hai trang cùng browser/viewport/nền/scroll. Bỏ riêng gutter scrollbar hệ điều hành (thumb thay khi trang dài thêm), chỉ so pixel phía trên mép footer mới; không che hoặc loại vùng nội dung đã duyệt. Cho phép sai số lượng tử tối đa 1/255 mỗi kênh màu ở pixel khử răng cưa của Chromium, ghi mức chênh thực vào JSON; không dùng sai số này cho tọa độ/chữ/màu CSS. Mọi phần tử thấy được phía trên còn được so toàn bộ tọa độ và computed typography/màu chính xác. DOM so từ hai nguồn thô cùng một lần parse, tránh chứng nhận sai lệch giả do một phía bị parse hai lần. Kết quả mới nằm trong audit footer, mốc trước giữ nguyên.

FB-027 có quyền đổi câu nhận diện/thanh tùy chỉnh: so DOM sau loại đúng hai nhóm node, không loại toàn shell/footer. So toàn bộ main và ảnh vùng workspace dưới toolbar (rail/câu nhận diện và toolbar mới được xem riêng); không gọi ảnh toàn trang bất biến khi UI đang được yêu cầu đổi. Dãy màu kiểm thêm 320/360/375px bên cạnh năm viewport chính trên cả Nhà/G01. `ui-before.json` khóa các tệp ngoài hai thay đổi; không bỏ guard footer, vùng đọc hoặc luồng học.

## Lịch sử FB028 — G02, không ép profile G01

- Kiểm 10 view nguồn trên 320/360/375/390/768/1000/1440/1920px; mở toàn bộ disclosure ở 390/1440 để không chỉ đo trang đang thu gọn. Guard nguyên văn, thứ tự, MathML và 1074 TeX từ QMD; giữ alt/caption, ID, link/download. Fixture bỏ công thức, đổi ID và lệch nhãn 8px phải bị phát hiện.
- Vùng prose: nhãn/tiêu đề bên trong giấy, đúng trục/inset, không lồng giấy, không tràn toàn trang; bảng và hình cuộn trong vùng có focus. Hình tính em theo viewBox/cỡ nhãn vector, không kéo đầy chiều rộng giấy. Nguyên liệu SVG không bị sửa.
- Ủng hộ dùng component grid riêng đã duyệt, kiểm trục text theo `.support-content`, không ép h3 của grid lên trục prose phía ngoài logo. G02 giữ component trong phép chiếu nguồn để bảo toàn thứ tự ID/text; scope hình học prose loại đúng `.support-region`, không loại khối toán. Kiểm riêng bề mặt trắng, chiều rộng, heading và link của Ủng hộ.
- Deep-link đến task/solution phải thấy cả nhãn vai trò dưới toolbar, không chỉ thấy ID đích. `r1-g02-adapter.css` đặt khoảng cuộn 128px cho ID nguồn G02; không đổi typography, inset hay CSS G01.
- Kiểm chọn nền/sắc xám, bàn phím và lưu/tải lại; drawer có nút mở, Escape trả focus, chọn view đóng drawer; vị trí rail/toolbar ổn định khi cuộn, đề–lời giải–trở lại–Back và no-JS.
- Hash bảo vệ production, toàn bộ tài sản, nguồn 0.4 và các HTML đã duyệt. Chỉ ba hồ sơ điều hành G02/README/bảng công việc được phép cập nhật theo nhiệm vụ này; ghi riêng hash trước/sau của các hồ sơ ấy, không lẫn với quyền sửa QMD/CSS/JS production.
- Báo cáo `qa-results.json` là kết quả hiện hành; `qa-first-run.json` lưu phép kiểm đầu thất bại. Không suy PASS thành nghiệm thu thị giác, nội dung toán, PDF hoặc phát hành; chưa kiểm Safari/Firefox, cảm ứng thật hoặc screen reader.

## FB036 — kiểm hai gói sau phản hồi mới

`scripts/zo_web_2027_pair_check.py` kiểm nguồn tươi/ID/toán, disclosure đóng,
nhãn/link không trùng, header trái, routing chung, đủ nhóm lời giải, ba
chặng G01, xác nhận Nền G02, review metadata và provenance bìa G02. Kiểm
browser sáu viewport, 12 view, all-open/no-JS, nguồn typography, sâu/return/
reload, drawer, nền/sắc xám và đề→lời giải. `pair_semantics.py` tên đầy đủ là
`scripts/zo_web_2027_pair_semantics.py`: kiểm từng đích nằm đúng nhóm và
inventory không bỏ sót disclosure, fixture di chuyển đáp án sang nhóm sai.
Các kết quả ở `_audit/zo_web_pair_refinement_2026-10-08/`. Lệnh checkpoint
FB033 không phải cổng PASS của bản sửa mới: receipt lịch sử giữ nguyên,
nguồn G01 chờ duyệt lại. Không biến khác biệt dự kiến với receipt cũ thành
lỗi nội dung mới, không sửa receipt để che khác biệt.

Khi được giao đối sánh, kiểm **vai trò**, cấp tiêu đề, vùng sở hữu, bảng, disclosure và action/đích; không thay bằng so số vùng/số PASS. Kiểm cả thiếu nhóm đề–lời giải, xác nhận Nền bị tách, nhãn/action lặp, heading ngoài giấy và header trái; fixture phải phát hiện kiểu sai tương ứng. Quy tắc Bài học/Luyện tập và ngân hàng mới thuộc 01/hồ sơ, không kết luận chỉ từ CSS. Audit nguồn/DOM G01 ngày 10/10 ghi 21 RD tại thời điểm rà; DH_011/DH_015 đã triển khai các lượt sửa và kiểm riêng, trạng thái hiện hành ở 03/profile. DH_015 kiểm ngữ cảnh/ownership/runtime đại diện và QD_025 trên HTML cô lập; chưa kiểm toán độc lập toàn gói, chưa nghiệm thu HTML mới. Không dùng QA FB036 thay bằng chứng hiện hành.

## Đối sánh DH_021

Kiểm mới theo 02/1.3 và ma trận M01–M48; không dùng checker quota lịch sử để che đơn vị toán được sửa có thẩm quyền. Rà nguồn–lời giải, ca âm cho duplicate label/header-only/missing-link/misroute, BBT bổ sung, độ lộ và phạm vi xác nhận. Runtime hiện hành phải đo trực tiếp Nhật kí/Ôn lại, reload/Back, hỗ trợ/quay về, drawer/bàn phím và màn hình hẹp. Giới hạn được ghi riêng, không suy từ mã là đã kiểm tương tác.

## DH_037 — Hồi quy áp dụng QD_033

Lỗi đã xác minh: chỉ dẫn ở 12 Điểm dừng biến Nhật kí thành thao tác mặc
định; cp-kt/cp-on3 G02 yêu cầu Sửa lỗi dù đã đạt; Nhà thiếu ngoại lệ kết
thúc Kiểm tra trước trợ giúp; controller làm mất nơi gọi khi xem lại Bài
học từ chặng/Điểm dừng. Đây là lỗi áp dụng nguồn/routing, không phải lý do
đổi kiến trúc hoặc thiết kế.

Nguồn sửa: QMD hai gói, template Nhà (partial sinh lại), controller dùng
chung và binding G01 tương ứng. Giữ bài làm/bằng chứng không đồng nghĩa
ghi Nhật kí mỗi Điểm dừng. Chọn trực tiếp Bài học là điểm vào bình thường;
nhánh hỗ trợ giữ đúng hoạt động gọi qua reload/Back/tab độc lập và khi
chuyển tiếp sang Ôn nền. Không mời trợ giúp giữa lượt Kiểm tra tự lực.

Chạy qua launcher, trên bộ HTML mới dựng cô lập:

```text
python scripts/zo_python.py scripts/zo_qd033_route_check.py --preview <thu_muc_bon_trang_reading> --output <thu_muc_QA_moi_trong_audit> --browser
```

Guard kiểm lời hướng dẫn tại chính Điểm dừng, ca âm bắt buộc Nhật kí/
Sửa lỗi/thiếu ngoại lệ Kiểm tra, nhãn/sở hữu và DH01–DH14 nguồn/DOM;
kiểm browser những đường gọi Bài học thật ở 1440/430/390 px, quay về,
reload/Back/tab khác, nhánh hỗ trợ tiếp, vào trực tiếp và no-JS. Không
dùng PASS này thay nghiệm thu chủ trì, kiểm toán toán, PDF hoặc thiết bị
thật. Nếu công cụ không hoàn tất thì ghi lỗi, không suy PASS từ ca đã chạy.

## DH_038 / HOM-QMD01 — nguồn biên tập Nhà không phải QMD native

Triệu chứng: mở `index.qmd` chỉ thấy include; muốn sửa lời dành cho học sinh
phải mở template HTML. Nguyên nhân: generator sinh toàn trang raw HTML vào
`chuong_trinh.qmd`; Quarto chỉ bọc đầu ra ấy. Không gọi đây là native QMD.

Nguồn sửa: `2027/index.qmd` chứa heading/paragraph/list/link/FAQ và lời
Ủng hộ bằng Markdown. Generator chỉ sinh ba component dữ liệu/UI; YAML
không giữ bản sao bốn đoạn Nhà đã di trú. `zo_home_qmd.py` ràng DOM native
vào UI cũ, không chứa lời biên tập. CSS/JS/tài sản và nguồn D0/R1 giữ nguyên.
Template/partial toàn trang cũ gỡ sau lưu ngoài repo, xác minh SHA-256 và
đối chiếu nội dung/DOM; không phục hồi chúng vào build mới từ checkpoint.

Guard Home kiểm nguồn native, đúng ba include dữ liệu, hash QMD/component/
mã dựng và runtime. Ca âm wrapper-only, HTML đổi đuôi QMD, include template
cũ phải bị bắt. So độc lập bản DH_037 được chỉ định tường minh: toàn văn,
ID/heading/disclosure/math, DOM/thuộc tính (trừ URL rebase đã kiểm), support;
kiểm tương tác sáu độ rộng, đồng hồ thật, hover/focus, FAQ, no-JS và tuyến
Home → D0/G01/G02 → Home mới. Không dùng bản lịch sử làm đầu vào render.

Bằng chứng và kết quả hiện hành ở 03/DH_038. Kiểm kỹ thuật không thay chủ
trì duyệt HTML, kiểm toán toán, PDF, Safari/Firefox/thiết bị thật hoặc release.

## COVER-OWN01 ? ?nh g?i kh?ng ph?i t?i nguy?n m?c ??nh c?a m?u

L?i: g?i m?i k? th?a ?nh G01; nguy?n nh?n `PreviewBuilder.common_assets()`
ch?p ?nh c? th? c?ng CSS/logo/font, trong khi thi?u c?ng binding theo g?i.
S?a 17/10/2026 theo ph? duy?t ch? tr?: b? ?nh kh?i common_assets; ?nh Home
legacy ???c n?p r? t?i ???ng Home l?ch s?; t?ng g?i khai b?o ?nh ri?ng t?i
`giao_dien/anh_bia.json`. C?ng `zo_course_cover.py` ???c g?i trong adapter
canonical tr??c/sau d?ng, ki?m ownership, duy?t, hash, tr?ng g?i v? HTML.
H?i quy: `python scripts/zo_python.py -B scripts/zo_course_cover_selftest.py`.
Ca ?m g?m thi?u khai b?o, ch?a duy?t, sai g?i, m??n ???ng d?n, ??i ?nh,
sao ch?p ??i t?n ?nh kh?c v? HTML d?ng nh?m ?nh. Kh?ng suy PASS k? thu?t
th?nh ??nh gi? t? ??ng t?nh ??i di?n, nghi?m thu m?i ho?c ph?t h?nh.

## Nhãn cấp chứa — 17/10/2026

Với mode parent-context-v1, kiểm đủ nhãn tiêu đề theo cây owner và ngữ cảnh khai báo; Bài học = MẠCH HỌC CHÍNH, Khởi động = MẠCH HỌC CHÍNH · BÀI HỌC. Chặn nhãn Khởi động cũ, nhãn cấp cha bị mất khi hai tiêu đề cùng giấy, mode/binding cũ và dấu bullet “•”. Không dùng nhãn type thay ngữ cảnh. Kiểm cùng CSS .role, nhãn trong giấy, không tràn ở 1440/430/390 px và đường đi/về còn đúng. Giữ bộ trích cấu trúc nguồn G01/G02; nhãn cuối cùng gọi bộ ghép chung. Không sửa HTML/PDF phát hành hoặc receipt lịch sử để đạt kiểm.

## MATH-ASSET01 — đường dựng phải khớp vai trò

Theo 07/6.1.2 và 02/2.5 của khóa: source/HTML guard dùng scripts/zo_course_math_assets.py, binding profiles/course-math-assets.json. Không nối BBT bằng bảng thường được gán kind=variation; bộ nối bảng phải từ chối. Hình trong bài gọi cùng production-figures.css và cỡ tự nhiên, bìa dùng manifest riêng. Ma trận đối chứng phải chỉ ra cả component và đầu ra nhìn được; có thử âm JSON rỗng, thiếu giới hạn/điểm loại, surface bìa trong bài, provenance mã sinh/style/phông và sizing. Tương thích G01–G03 không chứng nhận G04/gói mới; không đổi shell/PDF/receipt hoặc xuất bản.

## DRAWER-ICON01 — nút capsule trở lại ở gói chưa có PDF

Nguyên nhân: template/JS shell còn nút chữ theo view; hình thức icon G01/G02 lại nằm trong mô-đun/CSS tải PDF. G04 chưa có PDF nên bỏ qua nhánh ấy. Kiểm cũ chỉ xác nhận mở drawer nên vẫn PASS. Sửa chủ sở hữu trong template/web-shell.css/site-ui.js, không gọi mô-đun PDF để lấy giao diện nút. Cổng zo_web_2027_shell.py nằm trước ghép trang và sau adapter, không phụ thuộc agent nhớ chạy ngoài.

Thử âm: bỏ mode/icon/tên truy cập/đích dialog; lộ tên view; bỏ hidden; CSS trở lại chiều rộng capsule. Browser: 390/430/768/999px phải đúng 52×52, icon 20px, không chữ; 1000/1440px nút ẩn, rail đúng; Enter/Escape/focus, chọn view, tải lại, resize và chế độ xám giữ chức năng. Trang không có PDF là ca bắt buộc. Không sửa PDF/source toán/HTML phát hành hoặc dùng PASS kiểm hình trước đó chứng nhận component này.


## GRAPH-G03-01 — khung và tỉ lệ đồ thị theo G03

Chủ trì chọn G03 làm mẫu ngày 17/10/2026. Áp dụng 07/6.1.2: preset `lesson-g03` của công cụ đồ thị, `set_lesson_graph_size` của adapter và CSS dùng `--figure-em`; không dùng width:auto của bản sửa trước. Giữ bố trí hình ghép, nội dung toán, bìa và BBT. Kiểm giá trị kích thước thật ở desktop/mobile cùng đối chứng G03, thử âm sai preset/hệ số/CSS. Trạng thái và bản xem tại 03; HTML sửa chưa tự là PDF đồng bộ, nghiệm thu hoặc xuất bản.


GRAPH-G03-02 (18/10/2026): bảo toàn đối chứng bằng bản chụp/số đo, không giữ lỗi hiển thị trong nguồn hiện hành. Cổng lesson_display_checks áp dụng đủ G01–G04, bao gồm ảnh không có figure. G03 gọi apply_graph_display như các gói khác; kiểm đủ 11 ảnh trên desktop/mobile, sáu ảnh cũ giữ geometry và năm ảnh sửa nhận cùng tỉ lệ. Không dựng lại TEX/SVG/PDF khi chỉ sửa lớp đặt ảnh.
