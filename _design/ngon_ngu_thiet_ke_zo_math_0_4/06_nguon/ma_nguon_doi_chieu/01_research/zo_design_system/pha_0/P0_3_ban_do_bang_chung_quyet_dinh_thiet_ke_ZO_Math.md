# P0.3 — Bản đồ bằng chứng và phả hệ quyết định thiết kế ZO Math

**Ngày tổng hợp:** 2026-10-05  
**Phạm vi:** sáu cụm A–F được chọn từ inventory P0.2: nhận dạng/màu; typography; web/layout; ngôn ngữ biểu đạt toán học; video/motion/audio; nền tảng bằng lời/lịch sử nghiên cứu.  
**Mục tiêu:** ghi nhận nguồn, phạm vi, quan hệ giữa ý tưởng, quy tắc và cách triển khai; chỉ ra mâu thuẫn và phần chưa có bằng chứng. Báo cáo này không chọn phương án cho Design System, không tuyên bố canonical, không sửa nguồn và không yêu cầu migration.

## 1. Cách đọc và giới hạn kết luận

Mỗi mục DES là một **ứng viên quyết định** hoặc một ranh giới bằng chứng cần giữ lại, không phải quyết định đã được phê duyệt. Các trường được tách như sau:

- **Giá trị/ý niệm:** điều nguồn muốn truyền đạt hoặc ưu tiên.
- **Quy tắc thiết kế:** chỉ dẫn cụ thể rút ra từ nguồn, nếu nguồn thực sự nêu.
- **Implementation:** cấu hình, mã, tài sản hoặc đầu ra có thể quan sát.
- **Phạm vi và kiểm chứng:** môi trường/kênh mà bằng chứng áp dụng; việc không render/xem/nghe được ghi là khoảng trống, không được xem là kiểm chứng đạt.
- **Trạng thái P0.3:** chỉ dùng **Ý niệm**, **Đang nghiên cứu**, **Tạm chấp nhận**, **Loại bỏ khỏi phạm vi nghiên cứu tiếp**. Trạng thái này mô tả cách giữ ứng viên trong hồ sơ nghiên cứu, không thay cho phê duyệt của chủ dự án.

“Bằng chứng mạnh” chỉ nói về độ trực tiếp của tài liệu hoặc mã đối với một nhận định hẹp. Nó không chứng minh chất lượng thị giác, tính phù hợp xuyên kênh hay quyết định cuối cùng. Tên tệp `master`, `final`, chữ `canonical` trong snapshot, mức độ mới của tài liệu và implementation đang chạy đều không tự tạo quyền ưu tiên.

## 2. Phạm vi đã đọc và phương pháp

Đầu vào nền là 40 mục của [P0.2](./P0_2_khao_co_thiet_ke_ZO_Math.md). P0.3 đọc sâu có chọn lọc các tài liệu và nguồn liên quan đến sáu cụm, bao gồm stylesheet/cấu hình hiện được tham chiếu, quy chuẩn đồ thị/hình học/bảng biến thiên, hướng dẫn khối nội dung, tài liệu video/media, trang định vị và research memory. Các nhánh lịch sử, snapshot, Downloads, audit và worktree chỉ được dùng khi inventory hoặc nguồn được đọc dẫn tới chúng.

Phương pháp là đối chiếu văn bản nguồn với implementation được nêu, lịch sử phiên bản/commit khi đã có bằng chứng, và ghi rõ giới hạn của bằng chứng. P0.3 không render Quarto/PDF/SVG/video, không mở trực quan ảnh, không phát video hoặc nghe audio, không đo tương phản, không thử font trong trình duyệt, không chạy tool sản xuất, không chỉnh sửa tài sản nguồn và không rà lại toàn bộ repository/archive. Vì vậy, các kết luận về đầu ra thực tế được giới hạn nghiêm ngặt.

## 3. Bản đồ điều hành và số lượng ứng viên

Tổng cộng **34 ứng viên** được ghi nhận; các mục có thể giao nhau về chủ đề nhưng được phân biệt theo câu hỏi thiết kế và lớp bằng chứng.

| Cụm | Số ứng viên | Phạm vi chính |
|---|---:|---|
| A — Nhận dạng và màu | 6 | Logo, màu đỏ/vàng, neutrals, dấu nhấn |
| B — Typography | 4 | Web, PDF, media, khác biệt theo medium |
| C — Web và layout | 5 | Cascade, component, CSS cũ, khối nội dung, R1-G01 |
| D — Ngôn ngữ biểu đạt toán học | 10 | Đồ thị, geometry, variation, pipeline và giới hạn đầu ra |
| E — Video, motion, audio | 6 | Guideline, font/khung hình, pipeline, quan hệ phiên bản |
| F — Verbal identity và lịch sử nghiên cứu | 3 | Định vị, tính đang phát triển, provenance nghiên cứu |

### Executive Map

| ID | Cụm | Ứng viên | Bằng chứng | Trạng thái P0.3 |
|---|---|---|---|---|
| DES-AB-01 | A | Navbar/PDF hiện tham chiếu một biến thể logo cụ thể | Mạnh cho cấu hình | Tạm chấp nhận |
| DES-AB-02 | A | Một cặp logo trong `zo_math` và `zo_media` trùng byte | Mạnh cho cặp file | Tạm chấp nhận |
| DES-AB-03 | A | Logo trong Downloads là source khác; chưa xác lập tương đương thị giác | Mạnh về khác biệt source; thiếu so sánh | Đang nghiên cứu |
| DES-AB-04 | A | Đỏ `#EF5350` lặp lại qua nhiều implementation | Mạnh cho sự lặp implementation | Tạm chấp nhận |
| DES-AB-05 | A | Vàng `#FFCA28` và `#FFCF3D` cùng tồn tại; prototype có thêm biến thể | Mạnh cho xung đột source | Đang nghiên cứu |
| DES-AB-06 | A | Neutral và teal khác theo medium/sample | Mạnh cho giá trị mã; yếu cho vai trò thống nhất | Đang nghiên cứu |
| DES-AB-07 | B | Stack UI đặt Be Vietnam Pro trước Manrope nhưng comment nêu ưu tiên Manrope | Mạnh cho source; xung đột ngay trong source | Đang nghiên cứu |
| DES-AB-08 | B | PDF cấu hình STIX Two Text/Math độc lập với web UI | Mạnh cho cấu hình PDF | Tạm chấp nhận |
| DES-AB-09 | B | Guideline media nêu Be Vietnam Pro và STIX Two Math | Mạnh cho ý định; chưa xác minh font đầu ra | Ý niệm |
| DES-AB-10 | A | “Dấu nhấn ZO” là motif phụ trợ theo proposal media | Mạnh cho ý định; chưa xác nhận duyệt | Ý niệm |
| DES-C-01 | C | Cấu hình web nạp SCSS theme và CSS overlay theo chuỗi | Mạnh cho cấu hình; chưa render | Tạm chấp nhận |
| DES-C-02 | C | Điều hướng và layout thay đổi theo loại trang/dự án | Mạnh cho quy tắc/config cục bộ | Tạm chấp nhận |
| DES-C-03 | C | CSS cũ/prototype còn tồn tại nhưng không đồng nghĩa đang hoạt động | Mạnh cho sự hiện diện; phạm vi dùng chưa rõ | Đang nghiên cứu |
| DES-C-04 | C | Khối đỏ/vàng/xám biểu thị chức năng nhận thức; trạng thái mở và màu là hai quyết định độc lập | Mạnh cho guideline và CSS | Tạm chấp nhận |
| DES-C-05 | C | R1-G01 có họ kiến trúc Nhiệm vụ/Ví dụ/Hỗ trợ, không tương đương mapping màu đỏ/vàng/xám | Mạnh trong phạm vi review R1-G01; chưa thấy mapping bắt buộc | Tạm chấp nhận |
| DES-D-01 | D | Graph v0.2 dành cho sản phẩm mới, không tự hồi tố style cũ | Rất mạnh cho phạm vi tài liệu | Tạm chấp nhận |
| DES-D-02 | D | Graph v0.2 gán vai trò màu và token cụ thể | Mạnh cho quy chuẩn; chưa xác minh mọi output | Tạm chấp nhận |
| DES-D-03 | D | Đường biểu đồ có thể phân biệt bằng kiểu nét, không chỉ màu | Mạnh cho rule trong guideline/tool | Tạm chấp nhận |
| DES-D-04 | D | Shared style/layer và compiler là kiến trúc implementation | Mạnh cho pipeline; không phải design intent độc lập | Tạm chấp nhận |
| DES-D-05 | D | Style đồ thị cũ vẫn là bằng chứng production/historical riêng | Mạnh cho file và version comment | Đang nghiên cứu |
| DES-D-06 | D | Geometry v0.1 có pipeline khai báo YAML → compiler → output/receipt | Rất mạnh cho baseline theo tài liệu | Tạm chấp nhận |
| DES-D-07 | D | Variation v0.1 dùng JSON chung và lựa chọn output theo medium | Mạnh cho cấu hình/pipeline | Tạm chấp nhận |
| DES-D-08 | D | Semantic HTML cho variation chưa được triển khai đầy đủ | Mạnh cho gap được ghi nhận | Đang nghiên cứu |
| DES-D-09 | D | Nguồn self-contained cũ và shared-style mới là hai nhánh đóng gói | Mạnh cho khác biệt kiến trúc | Đang nghiên cứu |
| DES-D-10 | D | Receipt/compiler không thay visual acceptance hoặc kiểm tra mọi trường hợp | Mạnh cho ranh giới kiểm định | Tạm chấp nhận |
| DES-E-01 | E | Media/video guideline chọn nền sáng ấm, chữ tối, subtitle nền đặc | Mạnh cho guideline; chưa đo output | Ý niệm |
| DES-E-02 | E | Video guideline đề xuất Be Vietnam Pro và STIX Two Math | Mạnh cho ý định; output chưa xác minh | Ý niệm |
| DES-E-03 | E | Phân phối video cần master 16:9/9:16 và biến thể subtitle | Mạnh cho quy trình được tài liệu nêu | Tạm chấp nhận |
| DES-E-04 | E | Pipeline Manim → voice-over → DaVinci là workflow, không phải sonic identity | Mạnh cho workflow; audio chưa nghe | Tạm chấp nhận |
| DES-E-05 | E | Manual v0.3, handbook, guide v0.6 và v1.0 chưa có quan hệ kế thừa rõ | Mạnh cho sự tồn tại; thiếu provenance đầy đủ | Đang nghiên cứu |
| DES-E-06 | E | Sonic logo/audio chưa được chứng minh là tài sản đã duyệt | Mạnh cho khoảng trống | Đang nghiên cứu |
| DES-F-01 | F | Verbal identity nhấn mạnh hiểu, suy luận, chứng minh và tự kiểm tra | Mạnh, nguồn trực tiếp | Tạm chấp nhận |
| DES-F-02 | F | Triết lý được mô tả là tiếp tục trưởng thành, không đóng băng | Mạnh cho trạng thái epistemic | Tạm chấp nhận |
| DES-F-03 | F | Research memory lưu provenance; design cases/principles chưa được promote | Rất mạnh cho quy trình/trạng thái hiện tại | Tạm chấp nhận |

## 4. Phả hệ bằng chứng theo thời gian

Các mốc sau là trật tự xuất hiện/tài liệu hóa đã thấy, không phải thứ bậc thẩm quyền:

1. **Các prototype và lớp web cũ:** P0.2 ghi nhận nhiều stylesheet/theme thử nghiệm với đỏ, vàng, neutral và typography khác nhau. Một số tệp không được cấu hình HTML hiện được quan sát tham chiếu; không có căn cứ từ tên hay nội dung prototype để coi chúng là lựa chọn cuối.
2. **Website hiện hành theo cấu hình được khảo sát:** `_quarto.yml` nạp `zo-math.scss` và `assets/css/custom.css`. Theme có token và rule hiện đại hơn, nhưng overlay CSS vẫn là một lớp riêng; chưa render để xác định cascade cuối trên trang.
3. **Quy chuẩn đồ thị:** tài liệu v0.2 và tool shared-style tạo một tuyến dành cho sản phẩm mới. Quy chuẩn chủ động không áp ngược lên sản phẩm hiện có. `assets/tex/zo-graph-styles.tex` có `VERSION 04` và màu/kiến trúc khác; đây là nhánh production/historical cần giữ genealogy, không phải bằng chứng thay thế âm thầm.
4. **Quy chuẩn hình học:** geometry v0.1 ghi baseline ngày 2026-10-01 và mô tả YAML/compiler/output/receipt; audit spike được xác định là evidence/fixture, không phải dependency production. Tài liệu có giới hạn auto-visibility/label và vẫn cần visual review.
5. **Variation:** công cụ v0.1 có nguồn JSON và output theo medium, nhưng tài liệu đánh dấu semantic HTML renderer là chưa được giao/hoàn thiện. Không được đồng nhất SVG hoặc bảng nhìn thấy được với biểu diễn HTML có ngữ nghĩa đầy đủ.
6. **Video/media:** có handbook chưa version, manual v0.3, guideline media v0.6 “bản dùng thử” và manual v1.0 trong Downloads ghi ngày kết tinh 2026-09-29. P0.2 không xác lập v1.0 thay thế các tài liệu kia; khác biệt có thể là phạm vi hoặc nhánh vận hành.
7. **Nền tảng giáo dục và research memory:** nội dung giới thiệu/triết lý hiện hành cùng synthesis ngày 2026-08-29 và RQ-003 cho thấy việc hình thành nguyên lý vẫn đang diễn ra. Tài liệu này là nền tảng lời nói và quy trình học hỏi, không phải đặc tả visual.

Không có bằng chứng đủ để sắp xếp mọi snapshot, handoff, archive, nhánh cá nhân hoặc worktree theo một chuỗi tuyến tính duy nhất.

## 5. Cụm A — Nhận dạng và màu

| ID | Ý niệm / quy tắc | Implementation và nguồn | Phạm vi, giới hạn, xung đột | Bằng chứng / trạng thái |
|---|---|---|---|---|
| DES-AB-01 | Logo cần được dùng theo biến thể phù hợp nền/kênh; chưa suy ra một master duy nhất. | `_quarto.yml` và `assets/tex/zo-pdf.tex` tham chiếu `zo_math_logo_black_on_transprentt_1024`; P0-0004 ghi nhận nhiều biến thể nền/transparent/avatar-safe. | Chỉ xác nhận cấu hình navbar/bìa PDF quan sát được; không xác nhận tất cả trang hoặc output. | Mạnh cho config; **Tạm chấp nhận** như sự thật triển khai hẹp. |
| DES-AB-02 | Hai bản logo trong `E:\zo_math` và `E:\zo_media` là cùng nội dung byte theo phép so sánh hash đã thực hiện. | Các asset được inventory dưới `assets/logo` và `zo_brand/logo`; so sánh hash cho cặp file được agent ghi nhận là trùng. | Chỉ áp dụng cho đúng cặp đã so; không chứng minh mọi variant là tương đương hoặc cùng provenance. | Mạnh cho hai file; **Tạm chấp nhận** giới hạn này. |
| DES-AB-03 | Bản `D:\Downloads\zo_math_logo_black_on_transprentt_master.svg` là source khác với cặp trên. | P0-0034 ghi SVG Inkscape, wordmark, fill đen, metadata Arial Bold và canvas vuông; tên `master` không có giá trị phê duyệt tự thân. | Chưa render để xác nhận khác biệt nhìn thấy, chất lượng hoặc mục đích sử dụng; không kết luận khác nhận dạng. | Mạnh cho đặc tính source; **Đang nghiên cứu**. |
| DES-AB-04 | Đỏ `#EF5350` lặp lại ở theme web, PDF, graph, geometry, Manim và media. | P0-0001, P0-0009, P0-0011, P0-0012, P0-0014, P0-0022. | Sự lặp lại là evidence của implementation, chưa chứng minh vai trò, sắc độ và contrast nhất quán ở mọi đầu ra. Các quy chuẩn graph còn dùng `#BF4240` cho vai trò riêng. | Mạnh cho sự lặp; **Tạm chấp nhận** việc màu này đang được dùng, không nâng thành palette chung. |
| DES-AB-05 | Vàng `#FFCA28` trong theme/graph/scene và `#FFCF3D` trong media v0.6 cùng tồn tại; prototypes còn có `#FDD835`, `#FFC107`, `#FFD700`. | P0-0003, P0-0009, P0-0011, P0-0014, P0-0022, P0-0027. | Media v0.6 được ghi là dùng thử; prototype không nhất thiết đang chạy. Chưa có quyết định vai trò/medium hay đánh giá tương phản để giải quyết nhánh màu. | Mạnh cho xung đột; **Đang nghiên cứu**. |
| DES-AB-06 | Nền/ink/grid và teal thay đổi giữa web, Manim, graph và media. | Ví dụ scene Manim dùng `#FBFAF7`, `#222222`, `#DDDDDD`, teal `#1DE8B5`; media guideline ghi `#FBFAF8`; theme có các neutral khác. | Giá trị literal được biết, nhưng chưa có token mapping cross-medium hoặc kiểm tra thị giác để biết đây là sai lệch hay chủ ý theo medium. | Mạnh cho mã; **Đang nghiên cứu**. |

## 6. Cụm B — Typography

| ID | Ý niệm / quy tắc | Implementation và nguồn | Phạm vi, giới hạn, xung đột | Bằng chứng / trạng thái |
|---|---|---|---|---|
| DES-AB-07 | Web UI có stack bắt đầu bằng Be Vietnam Pro, tiếp theo Manrope, Nunito Sans, Inter và system fallbacks. | `zo-math.scss:95–100, 188–207` theo kiểm tra source/blame được báo cáo. Import Google Fonts; selectors UI áp dụng stack. | Comment lân cận nói “ưu tiên Manrope” trong khi declaration ưu tiên Be Vietnam Pro. Chưa test network failure, font fallback hoặc browser output. | Mạnh cho source, xung đột nội bộ; **Đang nghiên cứu**. |
| DES-AB-08 | PDF cấu hình STIX Two Text cho text/sans/mono và STIX Two Math cho math; tách với web UI. | `_quarto-pdf.yml:1–18`, `assets/tex/zo-pdf.tex`, local font assets; LuaLaTeX, A4, 11pt theo cấu hình. Git blame ghi thay đổi PDF ngày 2026-07-28. | Không nên gộp với stack web. Chưa render/kiểm tra font embedding hoặc fallback phát hành. | Mạnh cho config; **Tạm chấp nhận** như quy tắc PDF đang khai báo. |
| DES-AB-09 | Guideline media đề xuất Be Vietnam Pro cho chữ và STIX Two Math khi công cụ hỗ trợ. | `E:\zo_media\...\Phong_cach_ZO_Math.md:17` theo P0-0022. | Đây là intended guideline, không chứng minh font đã dùng trong video; không có fallback matrix. Không tự mở rộng sang website/PDF. | Mạnh cho ý định; **Ý niệm**. |
| DES-AB-10 | Logo có thể có metadata Arial Bold; dấu nhấn đỏ/vàng là motif phụ trợ, không phải logo hay ký hiệu toán. | P0-0034 nêu metadata SVG; P0-0022 ghi dấu nhấn hai thanh bo tròn đỏ/vàng, mỗi trang/cảnh một dấu và đề xuất/chờ duyệt. | Metadata SVG không chứng minh font rendering; motif chưa có bằng chứng phê duyệt và màu vàng phụ thuộc DES-AB-05. | Mạnh cho proposal; **Ý niệm**. |

## 7. Cụm C — Web và layout

| ID | Ý niệm / quy tắc | Implementation và nguồn | Phạm vi, giới hạn, xung đột | Bằng chứng / trạng thái |
|---|---|---|---|---|
| DES-C-01 | Cascade web phải được hiểu theo chuỗi nạp, không xem một file theme tách rời là toàn bộ output. | `_quarto.yml` nạp `zo-math.scss` và `assets/css/custom.css`; P0-0001. | Chưa render ở desktop/mobile để xác định cascade sau cùng, specificity và các component theo dự án con. | Mạnh cho cấu hình; **Tạm chấp nhận** như sơ đồ nạp hiện tại. |
| DES-C-02 | Điều hướng/layout thay đổi theo loại trang và dự án; sidebar không đồng nhất với TOC. | `_quarto.yml`, `quy_tac_sidebar_va_muc_luc.md`; P0-0008. P0-0001 cũng ghi các biến navbar/sidebar. | Đây là rule/config ở web; chưa đánh giá thị giác, hành vi hay viewport thực tế. Không suy rộng layout của một dự án con thành chuẩn mọi trang. | Mạnh cho quy tắc/config; **Tạm chấp nhận** trong phạm vi được tài liệu nêu. |
| DES-C-03 | CSS overlay, component CSS, stylesheet gói và prototype tồn tại song song; tên hoặc sự hiện diện không chứng minh chúng đều đang dùng. | `custom.css`, `zo-math.css`, `custom-temp.css`, các SCSS cũ/prototype và CSS theo gói; P0-0001, P0-0003, P0-0007. | Có dấu hiệu hard-code giá trị khác hệ token; cần truy import/use theo từng project. Không xóa hoặc chuẩn hóa trong P0.3. | Mạnh cho sự tồn tại; **Đang nghiên cứu**. |
| DES-C-04 | Hệ khối dùng đỏ cho lý thuyết chung có tính khái quát/tái sử dụng; vàng cho bài viết nhỏ tương đối độc lập, mở rộng/khám phá/kết nối; xám cho hỗ trợ phụ thuộc ngữ cảnh. Việc tách block, trạng thái mở/thu gọn và màu là các bước riêng. | `quy_trinh_xay_dung/huong_dan_su_dung_khoi_noi_dung.md` không ghi version/date ở phần đầu (`:7–31, 75–146, 157–165`); `_zo_content_blocks.scss` không có version/date trong header (`:1–21, 42–59, 61–109, 112–136`). CSS dùng token đỏ/vàng/xám của `zo-math.scss`; legacy `highlight-box-*` và Quarto callouts được phân biệt. | Scope là content blocks/học liệu, không phải palette thương hiệu. Hướng dẫn cấm chọn màu chỉ vì nổi bật/đẹp/cảm giác, không bắt buộc mỗi bài có đủ ba màu. Mở/thu gọn độc lập với màu; khối mới và lớp legacy không được đồng nhất. | Mạnh cho semantics và implementation source; hướng dẫn yêu cầu kiểm tra PDF trực quan nhưng lượt này không render. **Tạm chấp nhận** trong phạm vi khối. |
| DES-C-05 | R1-G01 đề xuất mạch tuyến tính, phân cấp bằng typography/whitespace và ba họ kiến trúc cục bộ: Nhiệm vụ, Ví dụ, Hỗ trợ; không thêm màu theo từng loại nội dung. | `E:\zo_math_ca_nhan\zo_math_on_thi_toan_thpt\Kiến trúc trình bày R1-G01.md`, “Báo cáo Lượt 3A” (`:1–4, 56–80, 102–130, 390–465`); P0-0028 ghi nhận review và viewport. Review giới hạn dự kiến sửa trong gói R1-G01, không sửa theme toàn cục. | Bằng chứng hiện có cho thấy **khác layer/scope, chưa chứng minh mâu thuẫn trực tiếp**: ba họ R1-G01 là information architecture/interaction roles; đỏ/vàng/xám là semantics của block theo chức năng nội dung. “Không thêm hệ màu theo từng loại nội dung” không nhất thiết phủ định hệ block hiện có. Mâu thuẫn chỉ phát sinh nếu implementation bắt buộc map mọi Nhiệm vụ/Ví dụ/Hỗ trợ sang một màu; các file đã đọc chưa chứng minh mapping đó. | Mạnh trong scope review; status checker `PASS`, PDF `CURRENT` theo `worktree-mtime` (không phải receipt hash), visual review là mẫu chứ chưa nghiệm thu toàn bộ. Hai audit liên quan cũng không chứng minh semantics màu: `_audit/R1-G01_pdf_trinh_bay_sua_20260923/README.md` ghi check/layout evidence; `_audit/on_thi_phase3_checks.json` ghi integrity/DOM contract. **Tạm chấp nhận** khác biệt layer; kiểm tra implementation nếu cần xác nhận. |

## 8. Cụm D — Ngôn ngữ biểu đạt toán học

| ID | Ý niệm / quy tắc | Implementation và nguồn | Phạm vi, giới hạn, xung đột | Bằng chứng / trạng thái |
|---|---|---|---|---|
| DES-D-01 | Quy chuẩn graph v0.2 áp dụng cho sản phẩm mới; không tự thay style đang dùng hoặc hồi tố sản phẩm cũ. | `quy_chuan_san_xuat_do_thi_ham_so_zo_math_v0.2.md`, P0-0009 và README tool v0.2. | Phạm vi migration được tài liệu giới hạn rõ; đây không phải chỉ dẫn chuyển đổi mọi hình. | Rất mạnh cho scope; **Tạm chấp nhận**. |
| DES-D-02 | Graph v0.2 gán vai trò màu cụ thể, gồm strong `#BF4240`, secondary `#997918`, nền vàng nhạt và trục xám. | Quy chuẩn v0.2 và `cong_cu_do_thi_ham_so_zo_math/tex/zo_graph_v02.tex`; P0-0009, P0-0011. | `#997918` cũng có trong style cũ nhưng có thể mang vai trò khác. Không nhập hai vai trò thành một token chung nếu chưa so source. | Mạnh cho rule; **Tạm chấp nhận** trong phạm vi graph v0.2. |
| DES-D-03 | Nhiều đường nên được phân biệt bằng kiểu nét, ngoài màu. | Quy chuẩn v0.2/tool ghi đường ngang có thể dùng các kiểu nét khác nhau. | Đây là quy tắc biểu đạt trong graph, không khẳng định mọi trường hợp đã được kiểm tra về khả năng tiếp cận hoặc in đơn sắc. | Mạnh cho rule; **Tạm chấp nhận**. |
| DES-D-04 | Shared style/layer declarations, compiler và validation là cơ chế implementation để quản lý tái sử dụng/che phủ. | `zo_graph_v02.tex`, `zo_graph_build.py`, README tool; P0-0011. | Layer/compiler là kỹ thuật hỗ trợ. Chúng không tự chứng minh layout có chất lượng, nhãn không va chạm hoặc mọi đầu ra đạt. | Mạnh cho pipeline; **Tạm chấp nhận** như implementation, không coi là design intent độc lập. |
| DES-D-05 | `assets/tex/zo-graph-styles.tex` là một nhánh style có provenance, không phải canonical v0.2. | Version comment 04, ngày 2026-07-27; palette có strong/reference vàng `#997918`, khung 12×7.5 cm và khai báo layer; P0-0010. | Xung đột mã/vai trò với v0.2; còn là bằng chứng production hiện trạng. Chưa truy đủ mọi source đang input file này. | Mạnh cho tệp/version; **Đang nghiên cứu** về phạm vi dùng hiện tại. |
| DES-D-06 | Geometry v0.1 xác lập pipeline có receipt cho nguồn khai báo mới. | `quy_chuan_san_xuat_hinh_hoc_zo_math_v0.1.md`, `scripts/zo_geometry.py`, `assets/tex/zo-geometry-styles.tex`, `_audit/zo_geometry_spike/`; YAML → compiler → TeX/PDF/SVG/PNG/receipt. | Quy chuẩn nói không hồi tố tài sản cũ. Auto-visibility/label là hữu hạn; hình dày đặc cần visual review. SVG có thể không giữ semantic TikZ IDs. | Rất mạnh cho baseline đã được tài liệu hóa; **Tạm chấp nhận** trong phạm vi nguồn mới. |
| DES-D-07 | Variation v0.1 dùng một nguồn JSON và tạo các dạng output theo medium. | `zo_variation_v01.tex`, `zo_variation_build.py`, `zo_variation.css`, `zo_variation_qmd.lua`; P0-0013. HTML chọn SVG, PDF học liệu chọn PDF; có phần tử bảng ngữ nghĩa. | Chưa đối chiếu mọi bảng cũ hoặc mọi gói sản phẩm. Cấu hình không chứng minh hết mọi output hiện hành đã đi qua tool. | Mạnh cho pipeline được nêu; **Tạm chấp nhận** như kiến trúc hiện có. |
| DES-D-08 | Semantic HTML của variation là implementation gap, không phải tính năng hoàn tất. | Tài liệu v0.2/variation nêu điểm nối nhưng chưa giao renderer đầy đủ; agent ghi nhận tool graph/geometry chỉ chứng minh PDF/SVG. | Không suy semantic structure từ ảnh/SVG nhìn thấy được; cần kiểm tra renderer và output trực tiếp. | Mạnh cho trạng thái thiếu; **Đang nghiên cứu**. |
| DES-D-09 | Đóng gói style self-contained trong nguồn cũ khác với kiến trúc dùng shared style mới. | Tài liệu graph cũ yêu cầu style nhúng đầy đủ; tool v0.2 có `zo_graph_v02.tex` chung. Quy chuẩn mới không thay style cũ; P0-0009–0011. | Đây là lineage/implementation divergence. Không migration hoặc canonicalize một nhánh dựa riêng vào tuổi/tiện lợi. | Mạnh cho sự khác biệt; **Đang nghiên cứu**. |
| DES-D-10 | Compiler/checker/receipt là bằng chứng cấu trúc và nguồn gốc, không thay nghiệm thu trực quan. | Quy chuẩn geometry và graph; audit spike/receipt. Các giới hạn label/collision và đầu ra cần visual review được ghi nhận. | Không có lượt render/duyệt lại trong P0.3; không kết luận tất cả fixture hoặc mọi hình đã đạt. | Mạnh cho ranh giới; **Tạm chấp nhận**. |

## 9. Cụm E — Video, motion và audio

| ID | Ý niệm / quy tắc | Implementation và nguồn | Phạm vi, giới hạn, xung đột | Bằng chứng / trạng thái |
|---|---|---|---|---|
| DES-E-01 | Media guideline nêu nền sáng ấm, chữ xám đậm và subtitle nền đặc nhằm giữ tương phản ổn định. | `E:\zo_media\...\Phong_cach_ZO_Math.md`; P0-0022. | Chỉ scope media/video. Chưa có contrast ratio, WCAG, render hay small-screen test; neutral không đồng nhất với token web. | Mạnh cho guideline, vừa cho deployed media; **Ý niệm**. |
| DES-E-02 | Typography media đề xuất Be Vietnam Pro và STIX Two Math. | P0-0022, guideline phong cách media. | Chưa xác minh font thực tế của video hoặc khả năng hỗ trợ/fallback của công cụ. Không gộp với web stack. | Mạnh cho ý định; **Ý niệm**. |
| DES-E-03 | Một nguồn production có thể cần master ngang/dọc và subtitle/no-subtitle riêng. | Video guide v1.0 trong Downloads ghi 16:9, 9:16, 30fps và các biến thể subtitle; P0-0036. | Tài liệu hỗ trợ yêu cầu đóng gói, không chứng minh các export hiện có đã qua duyệt. Tên `final` trong export không phải acceptance. | Mạnh cho yêu cầu được ghi; **Tạm chấp nhận** trong scope phân phối video. |
| DES-E-04 | Manim → voice-over → DaVinci là workflow sản xuất, không phải sonic identity hay motion grammar đã chốt. | P0-0024 ghi source Manim/Resolve/audio và manuals; tool/tài liệu mô tả quy trình. | Chưa phát/nghe/xem sản phẩm; không có bằng chứng chuẩn hóa voice, âm lượng, timing/easing hay audio mix. Quy chuẩn chú âm trong repo không đồng nghĩa sonic branding. | Mạnh cho workflow; **Tạm chấp nhận** việc phân biệt hai khái niệm. |
| DES-E-05 | Handbook chưa version, manual v0.3, media guide v0.6 và manual v1.0 không có quan hệ kế thừa được chứng minh. | P0-0022–0025 và P0-0036. Guide v0.6 ghi dùng thử; v1.0 ghi ngày kết tinh 2026-09-29. | Có thể là successor, phạm vi con hoặc nhánh song song. Chưa xác định commit/ngày tạo của mọi tài liệu, so sánh đầy đủ nội dung hay trạng thái duyệt. | Mạnh cho sự tồn tại; **Đang nghiên cứu**. |
| DES-E-06 | Chưa có bằng chứng đủ để coi sonic logo là asset đã được duyệt và có mix specification. | v1.0 có đề cập sonic logo; P0-0015 là quy chuẩn chú âm/phát âm, không phải nhạc hiệu; P0-0024 ghi có thư mục audio. | Chưa nghe bất kỳ file audio nào; không biết asset nào optional, approved, trial hoặc chỉ là bước quy trình. | Mạnh cho khoảng trống; **Đang nghiên cứu**. |

## 10. Cụm F — Verbal identity và nền tảng nghiên cứu

| ID | Ý niệm / quy tắc | Implementation và nguồn | Phạm vi, giới hạn, xung đột | Bằng chứng / trạng thái |
|---|---|---|---|---|
| DES-F-01 | ZO Math tự định vị là không gian giáo dục toán, hướng tới hiểu quan hệ/cấu trúc, suy luận, biện minh và tự kiểm tra—not chỉ đáp số hay thủ tục. | `content/about.qmd` và `content/triet_li_va_dinh_huong.qmd`; P0-0016. | Bằng chứng verbal identity và định hướng giáo dục; không suy ra palette, logo, motion, âm thanh hay layout. | Mạnh, nguồn trực tiếp; **Tạm chấp nhận** như verbal baseline hiện được công bố. |
| DES-F-02 | Triết lý được giữ liên tục nhưng vẫn có thể trưởng thành; các khẳng định chưa đủ bằng chứng cần để mở. | `triet_li_va_dinh_huong.qmd` và synthesis ngày 2026-08-29. Synthesis gọi research map là bản đồ đang hình thành, không phải framework đã xác lập. | Handoff và integration copy `about.qmd` ngày 2026-08-29/30 chưa được chứng minh quan hệ thay thế; không đóng băng nội dung. | Mạnh cho trạng thái đang hình thành; **Tạm chấp nhận**. |
| DES-F-03 | Research memory giữ provenance, lý do, quan sát, giả thuyết và bài học; design case/principle chỉ được promote khi có thực hành/lặp lại/bằng chứng. | `_research/README.md`, `RQ-003_nguyen-li-thiet-ke-bai-zomath.md`, synthesis; P0-0017. RQ-003 ở trạng thái `active-through-practice`; hai thư mục cases/principles trống ngoài `.gitkeep`. | Thư mục trống cho thấy chưa có nội dung được promote vào cấu trúc này; không chứng minh không có lịch sử thiết kế ở audit, media, snapshots hoặc sản phẩm. | Rất mạnh cho quy trình/trạng thái; **Tạm chấp nhận**. |

## 11. Mâu thuẫn và nhánh chưa giải quyết

1. **Màu vàng:** `#FFCA28` hiện diện trong SCSS/graph/Manim; `#FFCF3D` xuất hiện trong guideline media v0.6 dùng thử; prototypes còn `#FDD835`, `#FFC107`, `#FFD700`. Không lựa chọn màu nào ở P0.3.
2. **Thứ tự web font:** khai báo stack đặt Be Vietnam Pro trước Manrope, nhưng comment mô tả ưu tiên Manrope. Chưa biết comment hay khai báo nào phản ánh ý định gần nhất.
3. **Khối màu so với cấu trúc trung tính:** bằng chứng hiện có chủ yếu cho thấy khác layer/scope: đỏ/vàng/xám là semantics khối theo chức năng nội dung; Nhiệm vụ/Ví dụ/Hỗ trợ là họ kiến trúc cục bộ R1-G01. Chưa thấy mapping bắt buộc giữa hai trục, nên chưa có contradiction trực tiếp. Nếu implementation bắt buộc mỗi họ R1-G01 mang một màu, điều đó sẽ xung đột với hướng dẫn khối; chưa có bằng chứng như vậy trong các file đã đọc.
4. **Đồ thị cũ so với v0.2:** màu, tên style, đóng gói source và layer model khác nhau. v0.2 giới hạn ở sản phẩm mới; không có căn cứ migration tự động.
5. **Neutrals/teal và khác biệt medium:** các sample/code có literal khác nhau; chưa phân biệt sai lệch, theme riêng hay lựa chọn tối ưu theo đầu ra.
6. **Logo:** cặp asset trong hai root trùng byte, Downloads có source khác, nhưng chưa render/đối chiếu trực quan và chưa có provenance đủ để chọn master.
7. **Video manual/version:** v0.3, handbook, v0.6 dùng thử và v1.0 cùng tồn tại. Ngày/nhãn version chưa đủ để xác định kế thừa.
8. **Sonic logo và audio:** tài liệu có nhắc, thư mục audio tồn tại, nhưng chưa nghe file hoặc xác minh acceptance.
9. **Typography theo kênh:** web font phụ thuộc Google Fonts; PDF dùng STIX; graph/geometry có local STIX; sample Manim dùng DejaVu Sans. Chưa có ma trận tải font/fallback hoặc kiểm tra glyph thực tế.
10. **Bằng chứng kiểm tra đầu ra:** tài liệu có thể ghi test viewport/receipt, nhưng P0.3 không kiểm tra lại các artifact để xác nhận còn khớp source hiện tại.

## 12. Bằng chứng mạnh và điều nó không chứng minh

| Bằng chứng mạnh | Có thể kết luận | Không thể kết luận |
|---|---|---|
| `_quarto.yml`, SCSS/CSS và PDF YAML | Tệp nào được cấu hình/tham chiếu; literal values và stack được khai báo | Kết quả cascade/typography trên browser hoặc PDF cuối |
| Quy chuẩn graph v0.2 và geometry v0.1 | Phạm vi, rule và pipeline được tài liệu hóa | Mọi hình cũ đã migrate, mọi nhãn/đường không va chạm, mọi output đạt thẩm mỹ |
| Hash giống nhau của cặp logo | Hai file cụ thể giống byte | Logo đó canonical, được duyệt hoặc tương đương với các file khác |
| Media guideline/manual | Ý định, yêu cầu đóng gói và workflow được viết ra | Font/màu đã thực sự xuất hiện trong mọi media, media đã được duyệt, sonic identity đã hoàn chỉnh |
| About/triết lý/research docs | Verbal identity và trạng thái nghiên cứu được công bố | Visual system hoặc nguyên tắc thiết kế đã được xác lập |
| R1-G01 review | Có một đề xuất trong phạm vi gói R1-G01 và báo cáo ghi nhận kiểm tra cụ thể | Đề xuất đó là chuẩn toàn repository hoặc output hiện tại vẫn đạt |

## 13. Tách giá trị, quy tắc và implementation

Những điểm sau được giữ tách để tránh nâng code thành ý định thiết kế:

- **Token/mã màu trong SCSS** là implementation; chỉ các nguồn guideline/quy chuẩn mới nói được về ý nghĩa vai trò màu, và scope của chúng cần được giữ nguyên.
- **Stack font/import URL** là cấu hình; nó không tự chứng minh font đã tải thành công hoặc chữ toán hiển thị đúng.
- **Quarto cascade, shared Sass, graph layer, compiler, JSON schema và receipt** là architecture/implementation. Chúng hỗ trợ vận hành và provenance nhưng không thay quyết định thị giác hoặc nghiệm thu.
- **PDF A4, 16:9/9:16, kích thước thumbnail, graph physical size** là constraints theo medium; không nên đồng nhất chúng thành một layout chung.
- **Voice-over/DaVinci/Manim** là workflow; **chú âm** phục vụ phát âm nội dung; **sonic logo/nhạc hiệu** thuộc sonic identity. P0.3 không có bằng chứng để nhập ba phạm vi này thành một.
- **Ý nghĩa giáo dục trong about/triết lý** là verbal/educational foundation; không diễn dịch thành màu sắc hay motif nếu nguồn không nói như vậy.

## 14. Khoảng trống và câu hỏi đưa vào Research Map

Không mở nghiên cứu ngoài phạm vi P0.3. Những câu hỏi sau là các hướng kiểm chứng được phát hiện trong nguồn đã đọc, không phải quyết định:

1. Logo: provenance nào nối các SVG trong `zo_math`, `zo_media` và Downloads; các biến thể có tương đương hình ảnh và mục đích không?
2. Màu: yellow nào thuộc từng medium/role; neutral và teal có vai trò token hay chỉ thuộc sample/prototype?
3. Typography: ý định web là Be Vietnam Pro hay Manrope; browser/build có fallback đúng khi Google Fonts lỗi không; PDF có embed STIX như cấu hình?
4. Content blocks/R1-G01: nếu cần xác nhận triển khai, kiểm tra đúng QMD/CSS của R1-G01 để biết có mapping màu bắt buộc Nhiệm vụ/Ví dụ/Hỗ trợ hay không; đối chiếu HTML/PDF đúng phiên bản với review. Tài liệu hiện đọc chưa chứng minh mapping đó.
5. Graph: nguồn nào thực sự import `zo-graph-styles.tex`; output mới/old có thể so sánh theo source, role, khổ hình và acceptance record nào?
6. Geometry/variation: receipt hiện có bao phủ tình huống nào; renderer semantic HTML của variation hiện ở trạng thái nào; có visual acceptance cho các trường hợp dày đặc/collision không?
7. Video: manual nào kế thừa manual nào; package/Manim version và asset nào được dùng; video, subtitle và export nào được con người duyệt?
8. Audio: có sonic-logo asset đã phê duyệt, mix target và acceptance record không; tài liệu nào chỉ mô tả bước tùy chọn?
9. Verbal identity: handoff và integration copies `about.qmd` có khác nhau về nội dung/provenance không?
10. Research memory: observations nào đủ lặp lại để promote thành design case/principle theo quy trình hiện hành?

### Gói kiểm chứng kế tiếp được gợi ý (chưa thực hiện)

- So sánh content-block guideline, SCSS và R1-G01 review cùng đúng output/mirror phiên bản được nêu trong review; giữ rõ project scope.
- Dựng ma trận lineage/source/output/acceptance cho graph, geometry và variation; chỉ render mẫu chọn lọc nếu có yêu cầu và nguồn có thể tái tạo.
- Duyệt trực quan cặp logo và một số output đại diện; đo contrast và font fallback theo môi trường xác định.
- Lập bảng phiên bản/provenance video; nghe/xem mẫu chỉ khi có phê duyệt và người đánh giá phù hợp.

## 15. Nhật ký, ranh giới hành động và kết luận

- Đầu vào inventory: P0.2, 40 mục; không coi inventory là bao phủ toàn bộ lịch sử.
- Phân tầng A–F được tổng hợp từ nguồn repository, media, hồ sơ R1-G01 và Downloads đã được inventory xác định; không đọc lại toàn bộ các root.
- Đối với R1-G01, đã đọc targeted review, audit layout/PDF ngày 2026-09-23 và `on_thi_phase3_checks.json`; không đọc các PDF/PNG/contact sheet, mọi audit khác, inventory/baseline/boundary, hoặc toàn bộ gói R1-G01. Các kết quả `PASS`/`CURRENT` được giữ đúng nghĩa hẹp được báo cáo, không xem là nghiệm thu thiết kế.
- Không render, phát, nghe, build hoặc chạy script sản xuất; không đánh giá trực quan tài sản.
- Không sửa nguồn sản phẩm, không chọn palette/font/logo, không ban hành canonical, không migration, không commit/push.
- Chỉ tạo báo cáo audit P0.3 này theo yêu cầu; `_audit/` có thể bị `.gitignore` loại khỏi `git status`, như đã ghi ở P0.2.

**Kết luận:** bằng chứng đủ để lập phả hệ và ghi nhận 34 ứng viên theo scope, đồng thời xác định các nhánh xung đột và giới hạn rõ giữa giá trị, quy tắc và implementation. Bằng chứng chưa đủ để khóa lựa chọn liên kênh, thay thế tài liệu lịch sử, tuyên bố output đã đạt hoặc ra lệnh migration. Các quyết định đó tiếp tục mở cho Research Map và chủ dự án.
