# P0.4 — Bản đồ nghiên cứu ZO Math Design System

**Ngày lập:** 2026-10-05  
**Vai trò:** kết thúc Pha 0 bằng một bản đồ có thứ tự phụ thuộc cho các chương trình nghiên cứu từ Pha 1 đến khi đủ điều kiện hình thành ZO Math Design System 1.0.  
**Nguồn chính:** [P0.2 — Khảo cổ thiết kế ZO Math](./P0_2_khao_co_thiet_ke_ZO_Math.md) và [P0.3 — Bản đồ bằng chứng và phả hệ quyết định thiết kế ZO Math](./P0_3_ban_do_bang_chung_quyet_dinh_thiet_ke_ZO_Math.md).

## 1. Ranh giới và nguyên tắc

Đây là **Research Map**, không phải specification hay quyết định thiết kế. Không có nghiên cứu bên ngoài hoặc khảo cổ mới được thực hiện trong P0.4. Các nguồn lịch sử, implementation đang chạy và giá trị lặp lại được giữ đúng vai trò bằng chứng của chúng:

- hiện trạng không tự trở thành quy chuẩn; implementation không tự chứng minh rationale;
- sự lặp lại không đồng nghĩa với quyết định cuối;
- khác biệt giữa medium không mặc nhiên là inconsistency;
- `master`, `final`, `canonical` hoặc `official` trong tên tài liệu/tài sản không tạo thẩm quyền;
- không chọn palette, font, logo, motion hoặc hướng thiết kế cuối; không có ứng viên nào được nâng thành **Đã chốt**.

Mức nền dưới đây mô tả độ dày của bằng chứng Pha 0 trong từng chương trình, không phải mức độ quan trọng. Nghiên cứu được đề xuất có thể bao gồm nghiên cứu nguồn bên ngoài ở các pha sau; việc đề xuất đó không có nghĩa P0.4 đã thực hiện.

## 2. Cách đọc thứ tự và phụ thuộc

Đề xuất 12 chương trình chiến lược. Các chương trình không phải 12 task tuyến tính độc lập:

```text
Pha 1 — Khung nghiên cứu và nền tảng:
  R12 (khung governance/provenance ban đầu)
  R1 (nền tảng thương hiệu) ──> R2 (tính cách/cảm giác)
  R6 (ngôn ngữ Toán học) bắt đầu song song, tiếp nối nền hiện có

Pha 2 — Nghiên cứu miền:
  R1 + R2 + R6 ──> R3, R4, R5, R7, R8, R9
  R6 là đầu vào trọng yếu cho R4, R7, R8 và R11

Pha 3 — Tổng hợp liên kênh:
  R3 + R4 + R5 + R6 + R7 + R8 + R9 ──> R10

Pha 4 — Mô hình hệ thống và thử nghiệm:
  R10 + các quy tắc miền đủ chín ──> R11
  R12 duy trì provenance, trạng thái và review trong toàn bộ quá trình

Pha 5 — Thí điểm, nghiệm thu và tiến tới 1.0:
  R11 + R12 + bằng chứng từ các thử nghiệm/medium ──> đánh giá mức sẵn sàng 1.0
```

Các phụ thuộc là thứ tự logic để tránh quyết định token hoặc component trước khi có căn cứ. Chúng không mặc định rằng mọi chương trình phải đóng hoàn toàn mới được bắt đầu nghiên cứu kế tiếp. R12 cần khởi động sớm để lưu provenance và tiêu chí review; các quy tắc phát hành/deprecation chỉ có thể trưởng thành sau thí điểm.

## 3. Các chương trình nghiên cứu

### R1 — Nền tảng thương hiệu và định hướng giáo dục

**Mục tiêu:** làm rõ ZO Math là ai, tồn tại để làm gì, phục vụ ai, vấn đề giáo dục Toán nào cần giải quyết, và quan hệ dài hạn giữa giáo dục, Toán học, công nghệ và thương hiệu. Phân biệt bản chất có thể áp dụng xuyên sản phẩm với mục tiêu riêng của một khóa học/sản phẩm hiện tại.  
**Câu hỏi cốt lõi:** Mệnh đề nền tảng nào mô tả đúng ZO Math qua các sản phẩm và thời gian mà không đồng nhất thương hiệu với một khóa học hoặc một kênh?

**Vì sao phải nghiên cứu:** P0.3 có verbal identity rõ về hiểu quan hệ/cấu trúc, suy luận, biện minh và tự kiểm tra, nhưng cũng ghi nhận triết lý còn phát triển; các bản about handoff/integration chưa được phân xử về provenance. Cần làm rõ nền tảng trước khi suy diễn thành tính cách hoặc quy tắc nhận dạng.  
**Ảnh hưởng tới những medium nào:** Tất cả; đây là đầu vào định hướng, không phải bộ quy tắc thị giác cho mọi medium.

**Bằng chứng ZO Math đã có:**
- DES-F-01, DES-F-02, DES-F-03.
- `content/about.qmd`, `content/triet_li_va_dinh_huong.qmd`, research synthesis và RQ-003 được dẫn trong P0.3.
- P0-0016, P0-0017, P0-0035.

**Mức nền hiện tại:** **Vừa** — có tuyên bố trực tiếp và research memory, nhưng chưa có framework được xác lập và một số provenance nội dung còn mở.  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** các tuyên bố verbal identity hiện có; ranh giới rõ rằng nội dung giáo dục không tự chứng minh visual identity; vai trò của RQ-003 và research memory.  
**Những gì còn thiếu:** phân đoạn người học/đối tượng liên quan; vấn đề cần giải quyết; quan hệ giữa định hướng dài hạn và sản phẩm; bằng chứng thực tiễn cho các tuyên bố; đối chiếu provenance các bản about khi câu hỏi đó ảnh hưởng đến diễn giải.

**Loại công việc cần thiết:**
- phân tích nội bộ các tuyên bố và quyết định đã có;
- user feedback/phỏng vấn phù hợp để kiểm tra mức độ phản ánh thực tiễn;
- nghiên cứu nguồn bên ngoài có chọn lọc nếu thiếu bằng chứng về bối cảnh giáo dục hoặc đối tượng;
- tổng hợp và lưu provenance/giả thuyết, không biến phát biểu chưa kiểm chứng thành nguyên lý.

**Phụ thuộc vào:** không phụ thuộc chương trình nào khác; là tiền đề chính cho R2–R10. R12 cần cung cấp cách ghi lại nguồn, giả thuyết và trạng thái.  
**Đầu ra mong muốn:** hồ sơ nền tảng thương hiệu có ranh giới “cốt lõi dài hạn / mục tiêu theo sản phẩm”, nguồn dẫn và phần còn tranh luận.  
**Pha xử lý đề xuất:** Pha 1; rà soát lại khi có bằng chứng sản phẩm mới ở Pha 5.  
**Điều kiện để coi chương trình đủ chín:** người chịu trách nhiệm có thể xác nhận nội dung phản ánh đúng định hướng; từng mệnh đề quan trọng phân biệt rõ bằng chứng với giả thuyết; không suy ra logo, palette hay font trực tiếp từ triết lý.

### R2 — Tính cách thương hiệu và cảm giác

**Mục tiêu:** nghiên cứu cảm giác mà ZO Math cần tạo ra và các trục như học thuật/thân thiện, hiện đại/nghiêm túc, khám phá/đáng tin; phân biệt tối giản với lạnh lẽo, học thuật với khó gần, cao cấp với generic, trẻ trung với generic edtech.  
**Câu hỏi cốt lõi:** Những thuộc tính cảm nhận nào hỗ trợ nền tảng R1 và giúp ZO Math khác biệt mà không bị quyết định bởi gu tức thời?

**Vì sao phải nghiên cứu:** P0.2/P0.3 có nhiều style samples nhưng chưa có tiêu chí cảm giác tổng quát xuyên kênh. Một visual treatment có thể trông “tối giản” nhưng không nhất thiết đúng tính cách hoặc hỗ trợ học tập.  
**Ảnh hưởng tới những medium nào:** Tất cả, với cách diễn đạt và kiểm tra khác nhau trên web, tài liệu, video, social và audio.

**Bằng chứng ZO Math đã có:**
- DES-F-01, DES-F-02; DES-E-01/02 và DES-AB-10 chỉ là bằng chứng cục bộ/ý niệm, không phải kết luận tính cách.
- P0-0003, P0-0016, P0-0022, P0-0026.

**Mức nền hiện tại:** **Yếu** — có các mô tả và thử nghiệm cục bộ, chưa có khung thuộc tính được kiểm chứng.  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** tuyên bố giáo dục ở R1; các ví dụ lịch sử chỉ dùng làm stimulus/reference, không làm chuẩn ngầm.  
**Những gì còn thiếu:** từ vựng thuộc tính có ý nghĩa với người học; mức ưu tiên/tension giữa các trục; cách nhận biết “generic”; khác biệt mong muốn giữa các nhóm đối tượng/kênh.

**Loại công việc cần thiết:**
- nghiên cứu nội bộ để chuyển các từ cảm tính thành câu hỏi kiểm tra;
- user feedback hoặc nghiên cứu người dùng với đối tượng phù hợp;
- thử nghiệm thiết kế/visual comparison có giả thuyết và tiêu chí định trước;
- phân tích ví dụ đối chiếu, chỉ khi giúp kiểm tra tính khác biệt chứ không sao chép hướng thẩm mỹ.

**Phụ thuộc vào:** R1 trước khi viết tiêu chí; là đầu vào cho R3–R9.  
**Đầu ra mong muốn:** khung thuộc tính và các đối cực/tension cần quản lý, kèm bằng chứng và phản ví dụ; không phải moodboard được xem là kết luận.  
**Pha xử lý đề xuất:** Pha 1–2.  
**Điều kiện để coi chương trình đủ chín:** các thuộc tính có thể được người dùng diễn giải nhất quán; prototype khác nhau được so theo tiêu chí đó; đã ghi nhận cả bằng chứng trái chiều và phạm vi áp dụng.

### R3 — Kiến trúc nhận dạng và logo

**Mục tiêu:** nghiên cứu vai trò và quan hệ giữa logo, wordmark, logo variants, favicon/avatar, motif và “Dấu nhấn ZO”; xác định các trường hợp dùng/không dùng, nền, tỷ lệ, scale, clear space và cách kết hợp.  
**Câu hỏi cốt lõi:** Những tài sản nào thực sự thuộc kiến trúc nhận dạng, dùng trong tình huống nào, và bằng chứng provenance/duyệt nào xác lập quan hệ giữa chúng?

**Vì sao phải nghiên cứu:** P0.2 ghi nhận nhiều asset, P0.3 chỉ xác minh một cặp logo trùng byte và một source Downloads khác; chưa có so sánh trực quan/provenance để chọn master. Dấu nhấn ZO được mô tả là proposal, không thay logo.  
**Ảnh hưởng tới những medium nào:** Web, PDF, video, social, favicon/avatar, tài sản sản xuất và các sản phẩm mới.

**Bằng chứng ZO Math đã có:**
- DES-AB-01, DES-AB-02, DES-AB-03, DES-AB-10.
- P0-0004, P0-0021, P0-0022, P0-0034.

**Mức nền hiện tại:** **Yếu** — có tài sản và vị trí tham chiếu, nhưng không có kiến trúc/acceptance xuyên ngữ cảnh.  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** các biến thể hiện có và cặp asset hash-identical; điều đã biết rằng nhãn `master` không chứng minh thẩm quyền; phân biệt motif với logo.  
**Những gì còn thiếu:** lineage và quyền sử dụng; tương đương hình ảnh; mục đích từng variant; hành vi ở kích thước/nền khác nhau; quy tắc clear space/scale; tình huống không cần logo; trạng thái phê duyệt motif.

**Loại công việc cần thiết:**
- phân tích nội bộ provenance và cấu hình sử dụng;
- visual comparison có kích thước/nền/kịch bản xác định;
- thử nghiệm thiết kế các ứng dụng nhận dạng;
- usability/recognition test ở avatar, favicon và kích thước nhỏ;
- accessibility/contrast test khi logo có nền hoặc chữ kèm theo;
- user/stakeholder feedback về nhận diện, không dùng bỏ phiếu thay cho kiểm tra kỹ thuật.

**Phụ thuộc vào:** R1 và R2; R4 cung cấp bối cảnh màu nhưng không được dùng để chốt logo trước; R10 kiểm tra adaptation.  
**Đầu ra mong muốn:** bản đồ asset/provenance và quy tắc ứng dụng có điều kiện, kèm ma trận nền/kích thước/kênh và unresolved list.  
**Pha xử lý đề xuất:** Pha 2; xác nhận lại trên prototypes liên kênh ở Pha 3–5.  
**Điều kiện để coi chương trình đủ chín:** mọi asset được đề xuất dùng có nguồn gốc/trạng thái rõ; các use cases đại diện qua visual/recognition review; ngoại lệ và trường hợp không dùng được ghi nhận; chưa có asset nào được chọn chỉ vì tên file.

### R4 — Hệ màu và semantic color

**Mục tiêu:** nghiên cứu quan hệ giữa brand colors, semantic colors, mathematical colors, UI states, surfaces/neutrals, accents và các điều kiện web, PDF, grayscale/print, dark context nếu cần. Xác định cách đánh giá contrast và ý nghĩa, chưa xác lập giá trị màu cụ thể.  
**Câu hỏi cốt lõi:** Màu nào cần giữ ý nghĩa nào trong ngữ cảnh nào; phần nào có thể chia sẻ và phần nào cần mapping theo medium?

**Vì sao phải nghiên cứu:** P0.3 thấy đỏ lặp lại, nhiều vàng và neutral, graph-specific color roles và media guideline riêng. Các literal hiện có là bằng chứng implementation/guideline theo scope — **chưa phải câu trả lời cho chương trình nghiên cứu này**. Khác biệt có thể là role hoặc medium, không nhất thiết là inconsistency.  
**Ảnh hưởng tới những medium nào:** Website, PDF/in ấn, đồ thị/hình học/bảng, video/subtitle, social và UI components.

**Bằng chứng ZO Math đã có:**
- DES-AB-04, DES-AB-05, DES-AB-06, DES-D-02, DES-D-03, DES-E-01.
- P0-0001, P0-0003, P0-0009–0014, P0-0022, P0-0027.

**Mức nền hiện tại:** **Vừa** — nhiều mã và một số semantic roles theo graph/content blocks đã được ghi; còn thiếu semantic cross-system, đo kiểm và adaptation.  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** inventory các giá trị màu đã thấy; semantics giới hạn của graph v0.2 và content blocks; sự phân biệt role màu với kiểu nét trong graph. Không nâng đỏ `#EF5350` lặp nhiều thành palette cuối.  
**Những gì còn thiếu:** phân loại vai trò xuyên sản phẩm; contrast/accessibility; grayscale/print; dark context có cần hay không; neutral/accent semantics; cách duy trì khác biệt có chủ đích giữa media; đánh giá màu theo người dùng và chức năng toán.

**Loại công việc cần thiết:**
- phân tích nội bộ token/source lineage;
- thử nghiệm thiết kế và visual comparison có nội dung đại diện;
- accessibility/contrast test theo cỡ chữ, nền, trạng thái và đối tượng;
- technical validation trên browser, PDF và output vector/raster;
- user feedback/readability test với tasks cụ thể.

**Phụ thuộc vào:** R1, R2; R6 cho mathematical color/semantic emphasis; R7 cho surface/layout; R5 cho màu cạnh chữ; đầu vào từ R3/R10.  
**Đầu ra mong muốn:** mô hình vai trò màu, tiêu chí đánh giá, ánh xạ theo medium và tập ca kiểm thử — không chốt palette trong P0.4.  
**Pha xử lý đề xuất:** Pha 2; cross-medium validation ở Pha 3–5.  
**Điều kiện để coi chương trình đủ chín:** vai trò không mơ hồ; contrast/accessibility được kiểm theo tiêu chí đã chọn; khác biệt giữa các medium có rationale; đã thử print/grayscale và các trạng thái cần thiết; không dựa riêng vào màu khi phân biệt thông tin quan trọng.

### R5 — Kiến trúc typography

**Mục tiêu:** phân biệt brand/display, UI/navigation, reading/body, mathematical typography, labels, captions và subtitle; nghiên cứu fallback, tiếng Việt, accessibility và ràng buộc theo web/PDF/video.  
**Câu hỏi cốt lõi:** Những vai trò chữ nào cần được bảo đảm xuyên hệ thống, và implementation/fallback nào phù hợp theo từng môi trường mà vẫn giữ khả năng đọc Toán và tiếng Việt?

**Vì sao phải nghiên cứu:** web stack có xung đột giữa comment “ưu tiên Manrope” và declaration đặt Be Vietnam Pro trước; PDF khai báo STIX; media nêu Be Vietnam Pro/STIX Math; font availability/rendering chưa được kiểm.  
**Ảnh hưởng tới những medium nào:** Web, PDF, graph/geometry/variation, video, subtitle, social và công cụ tạo asset.

**Bằng chứng ZO Math đã có:**
- DES-AB-07, DES-AB-08, DES-AB-09, DES-E-02.
- P0-0005–0007, P0-0011–0014, P0-0014, P0-0022.

**Mức nền hiện tại:** **Vừa** — role/config theo một số medium đã hiện rõ; ý định UI đang xung đột và output/fallback chưa được kiểm.  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** stack khai báo trên web, STIX trong PDF/math, guideline media và font local đã inventoried. Không giả định một font phải dùng mọi nơi.  
**Những gì còn thiếu:** role matrix; comment/declaration provenance; tải font khi offline; fallback cho glyph/diacritics tiếng Việt và toán; embedding PDF; font trong subtitle; độ đọc ở kích thước nhỏ và màn hình khác nhau.

**Loại công việc cần thiết:**
- phân tích nội bộ source/font licensing and availability facts đã có;
- technical validation font load/fallback/embed ở môi trường xác định;
- readability/accessibility test với tiếng Việt, ký hiệu Toán và cỡ chữ thực;
- visual comparison giữa vai trò/type hierarchy;
- thử nghiệm thiết kế theo medium, có kiểm tra người dùng khi cần.

**Phụ thuộc vào:** R1/R2 để định nghĩa cảm giác và hierarchy; R6 cho yêu cầu ký hiệu/nhãn; R7 cho measure/layout; R10 cho mapping theo medium.  
**Đầu ra mong muốn:** role/fallback matrix và tiêu chí typography theo medium, kèm bộ mẫu kiểm tra glyph, tiếng Việt và công thức.  
**Pha xử lý đề xuất:** Pha 2; test tổng hợp tại Pha 3–5.  
**Điều kiện để coi chương trình đủ chín:** font/fallback đã xác minh ở browser/PDF/video tool được chọn; không mất glyph/diacritics; hierarchy/readability đạt test định trước; vai trò được ghi rõ mà không yêu cầu đồng nhất font giữa các medium.

### R6 — Ngôn ngữ biểu đạt Toán học

**Mục tiêu:** nghiên cứu riêng ngôn ngữ biểu đạt Toán học: đồ thị/hệ trục/labels/điểm/miền/đường phụ/asymptote/line styles; geometry; bảng biến thiên và bảng dữ liệu; sơ đồ; hierarchy/emphasis; accessibility; ranh giới giữa dữ liệu Toán và decoration.  
**Câu hỏi cốt lõi:** Cách biểu diễn nào giữ đúng ý nghĩa Toán, giúp đọc/suy luận/kiểm chứng, và chuyển được qua dạng HTML, PDF, SVG, video hoặc phương tiện khác?

**Vì sao phải nghiên cứu:** Đây là miền chuyên môn và ngôn ngữ biểu đạt, không chỉ là trang trí visual identity. Có nền kỹ thuật đáng kể nhưng thiếu acceptance xuyên output, semantic HTML cho variation và bằng chứng về mọi trường hợp khó.  
**Ảnh hưởng tới những medium nào:** Đồ thị, hình học, bảng biến thiên, bảng dữ liệu/sơ đồ trong web/PDF/video/social và asset sinh tự động.

**Bằng chứng ZO Math đã có:**
- DES-D-01 → DES-D-10.
- P0-0009–0014; graph v0.2, geometry v0.1, variation v0.1 và các pipeline được P0.3 dẫn.

**Mức nền hiện tại:** **Mạnh về nền tảng nguồn/quy tắc và pipeline; vừa về chất lượng đầu ra; yếu ở semantic variation HTML và acceptance tổng quát.**  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** graph v0.2 cho sản phẩm mới và giới hạn không hồi tố; role/line-style rules được tài liệu hóa; geometry YAML/compiler/receipt baseline; variation JSON và export hiện có. Không viết lại các quy chuẩn chuyên biệt nếu câu hỏi không yêu cầu.  
**Những gì còn thiếu:** ma trận biểu đạt theo loại nhiệm vụ Toán; kiểm chứng ý nghĩa; edge cases/collision; semantic HTML/accessibility của variation; mapping giữa source và các output; acceptance trực quan; ranh giới trang trí/toán học; khả năng đọc khi in/xem nhỏ.

**Loại công việc cần thiết:**
- phân tích nội bộ các quy chuẩn, fixtures, sources, receipts và output đã chọn;
- technical validation cho pipeline/semantic structure;
- visual comparison và review chuyên môn Toán;
- readability/accessibility test (bao gồm không chỉ dựa vào màu);
- thử nghiệm thiết kế có bài toán đại diện và ca khó;
- user feedback khi cần kiểm tra khả năng đọc/suy luận, không thay thế kiểm tra tính đúng Toán.

**Phụ thuộc vào:** R1 để gắn với mục tiêu học tập; bắt đầu song song Pha 1 vì đã có nền mạnh. Là tiền đề cho R4, R5, R7, R8, R10, R11.  
**Đầu ra mong muốn:** taxonomy nhiệm vụ biểu đạt, nguyên tắc và tiêu chí nghiệm thu theo loại biểu diễn, cùng gap list giữa source/compiler/HTML/PDF/video.  
**Pha xử lý đề xuất:** bắt đầu Pha 1; nghiên cứu/kiểm chứng trọng tâm Pha 2–4.  
**Điều kiện để coi chương trình đủ chín:** ví dụ đại diện và edge cases giữ đúng nội dung Toán; labels/points/regions/line styles đọc được ở các đầu ra mục tiêu; semantic/accessibility path được xác định; receipt kỹ thuật được bổ sung visual/subject review chứ không thay thế nó.

### R7 — Layout và spatial system

**Mục tiêu:** nghiên cứu spacing, measure, hierarchy, grid, responsive, article/gateway/cards/content blocks, PDF/mobile, 16:9/9:16/social; phân biệt shared principles với medium-specific adaptation.  
**Câu hỏi cốt lõi:** Quan hệ không gian nào cần được duy trì vì phục vụ học/đọc, và phần nào cần đổi theo viewport, loại trang hoặc medium?

**Vì sao phải nghiên cứu:** P0.2/P0.3 có layout web/PDF/media và review theo gói nhưng chưa có bản đồ liên medium. R1-G01 và hướng dẫn khối hiện có khác scope; không được coi là mâu thuẫn toàn hệ thống nếu chưa chỉ ra mapping và output.  
**Ảnh hưởng tới những medium nào:** Website, PDF, card grid, content blocks, hình/bảng, mobile, video ngang/dọc, thumbnail/social.

**Bằng chứng ZO Math đã có:**
- DES-C-01 → DES-C-05, DES-E-03.
- P0-0001, P0-0002, P0-0006–0008, P0-0020, P0-0025, P0-0028.

**Mức nền hiện tại:** **Vừa** — có page rules, một số cấu hình và R1-G01 review/output evidence; chưa có spatial system tổng hợp xuyên medium.  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** distinction giữa sidebar và TOC; layout theo loại trang; card-grid values như hiện trạng; khuyến nghị R1-G01 trong đúng scope; kích thước/output requirements hiện thấy.  
**Những gì còn thiếu:** shared spatial principles; measure và grid theo tác vụ; responsive behavior được kiểm chứng; cách phân biệt block pedagogy với architecture roles; PDF/mobile/video adaptation; vùng an toàn social/subtitle; đối chiếu source-version với output review.

**Loại công việc cần thiết:**
- phân tích nội bộ config, CSS, audit/report và output đại diện;
- thử nghiệm thiết kế/layout ở viewport và page types xác định;
- usability/readability test trên desktop, mobile, PDF/print và video frames;
- visual comparison, technical validation responsive/render;
- user feedback cho navigation, scanability và cognitive load.

**Phụ thuộc vào:** R1/R2; R6 cho bố cục biểu đạt Toán; R4/R5 cho density và hierarchy; R10 tổng hợp adaptation.  
**Đầu ra mong muốn:** ma trận spatial patterns theo chức năng/medium và bằng chứng thử nghiệm ở kịch bản đại diện; không gom mọi layout thành một template.  
**Pha xử lý đề xuất:** Pha 2–3.  
**Điều kiện để coi chương trình đủ chín:** các page types và viewport đại diện qua review; nội dung không mất chức năng khi responsive/print; exceptions có rationale; source và output được gắn phiên bản/provenance.

### R8 — Motion language

**Mục tiêu:** nghiên cứu animation purpose, pacing, entrance, transformation, continuity, transitions, camera, pause và temporal hierarchy; đánh giá việc chuyển động có làm lộ cấu trúc/lập luận Toán hay chỉ trang trí.  
**Câu hỏi cốt lõi:** Chuyển động nào giúp người học theo dõi biến đổi và quan hệ Toán, và khi nào tĩnh/pausing mới là lựa chọn đúng?

**Vì sao phải nghiên cứu:** P0.3 xác nhận workflow Manim/DaVinci nhưng không có motion grammar, easing/timing hoặc output review đủ để suy ra quy tắc. Đây là miền bằng chứng yếu.  
**Ảnh hưởng tới những medium nào:** Video, motion graphics, intro/outro, lesson clips, social vertical/horizontal và công cụ sinh animation.

**Bằng chứng ZO Math đã có:**
- DES-E-04, DES-E-05; P0-0014, P0-0023–0025.

**Mức nền hiện tại:** **Yếu** — có pipeline và một số format/workflow; thiếu rule được chứng minh và phân tích trực quan.  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** tồn tại của Manim → voice-over → DaVinci và gói 16:9/9:16; các nguồn hiện có là case material chứ không phải grammar đã chốt.  
**Những gì còn thiếu:** motion purpose taxonomy; pacing/pause; liên tục biến đổi; camera/framing; temporal hierarchy; điều kiện xem trên màn hình nhỏ; khi nào animation làm sai hoặc che khuất toán học; phiên bản tool/scene tương ứng.

**Loại công việc cần thiết:**
- phân tích nội bộ video/scene đã được phép xem;
- thử nghiệm thiết kế motion trên cùng một nội dung Toán với giả thuyết khác nhau;
- visual comparison và review chuyên môn Toán;
- usability/readability test, bao gồm tốc độ, pause và khả năng theo dõi;
- user feedback; technical validation trên player/aspect ratio mục tiêu.

**Phụ thuộc vào:** R1/R2 và R6; R7 cung cấp framing/spatial constraints; R10 định nghĩa adaptation.  
**Đầu ra mong muốn:** motion research cases và tiêu chí theo chức năng (explain/compare/transform/emphasize/pause), bao gồm trường hợp không dùng motion.  
**Pha xử lý đề xuất:** Pha 2–3; kiểm nghiệm cùng R6/R7 ở Pha 4.  
**Điều kiện để coi chương trình đủ chín:** các chuyển động thử nghiệm cải thiện hoặc không làm suy giảm khả năng theo dõi Toán theo test đã định; timing/pause và framing được ghi bằng lý do; có giới hạn accessibility/thiết bị; không suy luận grammar từ pipeline tool.

### R9 — Audio và sonic language

**Mục tiêu:** tách narration, pronunciation, TTS/voice, music, sound effects, silence, sonic logo, loudness/mix và accessibility thành các câu hỏi nghiên cứu riêng nhưng liên kết.  
**Câu hỏi cốt lõi:** Audio phục vụ mục đích học tập và nhận diện ở những điểm nào, và đâu là nội dung giọng nói, workflow, âm nhạc/hiệu ứng hay tài sản sonic brand?

**Vì sao phải nghiên cứu:** Có hướng dẫn voice-over và thư mục audio, nhưng chưa nghe media; chưa có bằng chứng sonic logo được duyệt hoặc mix specification. `quy_chuan_chu_am_zo_math` điều hành cách chú âm/phát âm, không đồng nghĩa với sonic identity.  
**Ảnh hưởng tới những medium nào:** Video, audio lesson, TTS, voice-over, social clips, công cụ dựng và nội dung có captions/transcripts.

**Bằng chứng ZO Math đã có:**
- DES-E-04, DES-E-06; P0-0015, P0-0024, P0-0025, P0-0036.

**Mức nền hiện tại:** **Gần như chưa có** cho sonic identity/mix; **vừa** cho quy trình narration/pronunciation.  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** quy chuẩn chú âm và phân biệt nó với sonic brand; workflow media; yêu cầu voice/subtitle ghi trong tài liệu. Không suy ra sonic identity từ việc có thư mục audio hoặc bước tùy chọn.  
**Những gì còn thiếu:** asset/status/provenance; voice/TTS decision context; music/effects/silence roles; loudness/mix targets; accessibility; subtitle/transcript synchronization; evidence of human approval.

**Loại công việc cần thiết:**
- phân tích nội bộ tài liệu và provenance audio;
- nghe mẫu khi có thẩm quyền/phê duyệt và người đánh giá phù hợp;
- thử nghiệm thiết kế audio/mix nếu có câu hỏi rõ;
- accessibility/usability test cho nghe trong điều kiện khác nhau, captions/transcripts;
- user feedback; technical validation loudness, codec, sync theo môi trường phân phối.

**Phụ thuộc vào:** R1/R2; R8 để đồng bộ thời gian với motion; R10 cho adaptation theo platform; R12 để lưu quyền duyệt/provenance.  
**Đầu ra mong muốn:** taxonomy sonic/media audio và acceptance questions; nếu không có sonic brand đã duyệt thì ghi nhận khoảng trống thay vì tạo tài sản mặc định.  
**Pha xử lý đề xuất:** Pha 2–3, sau đó kiểm tra tích hợp với R8/R10.  
**Điều kiện để coi chương trình đủ chín:** từng asset/role có trạng thái và mục đích; narration/music/effects/silence phân biệt được; mức nghe, sync và accessibility được test; mọi sonic mark chỉ được coi là chính thức sau phê duyệt có provenance.

### R10 — Cross-medium adaptation

**Mục tiêu:** xác định phần nào là brand core, phần nào medium-specific; nghiên cứu token có thể chia sẻ hay phải map; giữ ý nghĩa nhưng thay implementation; tránh ép web/PDF/video/social giống hệt nhau.  
**Câu hỏi cốt lõi:** Điều gì cần bất biến về ý nghĩa, điều gì được phép đổi cách thể hiện, và tiêu chí nào phân biệt adaptation có chủ ý với drift?

**Vì sao phải nghiên cứu:** P0.2/P0.3 cho thấy khác biệt về màu, font, khổ trang, graph, responsive, video và audio nhưng không đủ để kết luận inconsistency. Đây là chương trình tích hợp để giải quyết “mâu thuẫn giả” và xác định giới hạn chia sẻ.  
**Ảnh hưởng tới những medium nào:** Toàn bộ website, PDF, mathematical graphics, video/motion, social/audio và công cụ sinh.

**Bằng chứng ZO Math đã có:**
- DES-AB-04 → DES-AB-09, DES-C-01 → DES-C-05, DES-D-01 → DES-D-10, DES-E-01 → DES-E-06.
- P0-0001, P0-0005–0014, P0-0022–0025, P0-0028–0029.

**Mức nền hiện tại:** **Yếu** — có ranh giới theo medium và nhiều case, chưa có core-to-adaptation map.  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** toàn bộ mâu thuẫn/ràng buộc được lập ở P0.2/P0.3; các trường hợp đã ghi rõ medium-specific; không coi khác biệt code là bằng chứng lỗi.  
**Những gì còn thiếu:** khái niệm bất biến/biến đổi; map role/token sang medium; acceptance criteria theo chức năng; cách kiểm tra coherence mà không ép giao diện giống nhau; trường hợp thích nghi accessibility/format.

**Loại công việc cần thiết:**
- tổng hợp nội bộ kết quả R3–R9;
- visual comparison giữa các adaptation của cùng một nội dung/role;
- readability/usability/accessibility test theo từng medium;
- technical validation output và mapping;
- thử nghiệm thiết kế cross-medium; user feedback có bối cảnh.

**Phụ thuộc vào:** kết quả đủ chín của R3–R9; R1/R2 làm tiêu chí nền; R6 giữ đúng ý nghĩa Toán.  
**Đầu ra mong muốn:** cross-medium matrix: shared meaning, medium-specific realization, evidence, exceptions, test/acceptance route.  
**Pha xử lý đề xuất:** Pha 3, sau khi có kết quả miền; lặp lại trong Pha 4–5.  
**Điều kiện để coi chương trình đủ chín:** các cặp medium đại diện đã được so theo cùng chức năng/nội dung; khác biệt có rationale và không mất ý nghĩa/khả năng sử dụng; shared tokens chỉ được đề xuất khi bằng chứng cho thấy chúng thực sự dùng chung.

### R11 — Tokens, components và automation

**Mục tiêu:** nghiên cứu cách biểu diễn machine-readable cho semantic tokens, typography/spacing/graph/motion roles, component contracts, source of truth, provenance và generated assets; khảo sát cách tool ZO Math tiêu thụ hệ thống. Không thiết kế token cụ thể trong P0.4.  
**Câu hỏi cốt lõi:** Làm thế nào để hệ thống có thể được biểu diễn, kiểm tra và áp dụng qua tool mà vẫn giữ nguồn gốc, scope, ngoại lệ và chất lượng đầu ra?

**Vì sao phải nghiên cứu:** P0.2/P0.3 đã thấy SCSS/theme, JSON/YAML, shared graph style, compiler, receipt và generated assets, đồng thời phát hiện nhiều lớp source/overlay và token-role divergence. Cần đặt architecture sau khi có semantic/design findings, không để implementation hiện tại quyết định ngược thiết kế.  
**Ảnh hưởng tới những medium nào:** Web, PDF, mathematical graphics, geometry, variation, video/motion, social và các công cụ tương lai.

**Bằng chứng ZO Math đã có:**
- DES-C-01, DES-C-03, DES-D-04, DES-D-06, DES-D-07, DES-D-10; DES-F-03.
- P0-0001–0002, P0-0011–0013, P0-0020, P0-0023, P0-0027.

**Mức nền hiện tại:** **Vừa về pipeline kỹ thuật; yếu về mô hình hệ thống chung.**  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** khả năng hiện có của CSS/SCSS, JSON/YAML, graph/geometry/variation pipelines, compiler/receipt và data→generated asset; giới hạn của chúng theo P0.3.  
**Những gì còn thiếu:** semantic model cross-medium; ownership/source-of-truth policy; token/component contract; biểu diễn ngoại lệ; provenance/version của generated assets; machine-readable validation; quan hệ giữa guideline, runtime và visual acceptance.

**Loại công việc cần thiết:**
- phân tích nội bộ kiến trúc hiện có và dependency graph;
- technical validation/prototype nhỏ theo kết quả R10;
- thử nghiệm thiết kế implementation mapping, không tự tạo token trước khi semantics rõ;
- kiểm tra provenance/hash/version/receipt và generation reproducibility;
- visual/accessibility test cho component/assets sinh.

**Phụ thuộc vào:** R10 và kết quả R3–R9; R6 đặc biệt quan trọng với graph/geometry/variation; R12 cung cấp lifecycle/provenance.  
**Đầu ra mong muốn:** architecture proposal cho nguồn machine-readable, mapping adapters, component contracts và validation pipeline, cùng một pilot có receipt và visual acceptance.  
**Pha xử lý đề xuất:** Pha 4; pilot và điều chỉnh ở Pha 5.  
**Điều kiện để coi chương trình đủ chín:** một số use case đại diện có thể được sinh/kiểm tra tái lập; nguồn và output truy được provenance/version; không có token/component ambiguity vượt qua review; visual/semantic/accessibility acceptance được giữ ngoài checker tự động khi cần.

### R12 — Governance, provenance và tiến hóa hệ thống

**Mục tiêu:** nghiên cứu versioning, lifecycle trạng thái proposal/research/trial/accepted/deprecated, migration/exception, audit, visual acceptance, provenance, release/review và cơ chế ngăn nhiều `master/final/canonical` giả.  
**Câu hỏi cốt lõi:** Ai/điều gì có thẩm quyền thay đổi hệ thống, bằng chứng nào cần thiết cho từng trạng thái, và lịch sử/ngoại lệ được quản lý ra sao mà không xóa provenance?

**Vì sao phải nghiên cứu:** P0.2/P0.3 phát hiện snapshot, handbook nhiều phiên bản, stage/archive, outputs và tài sản có nhãn mạnh nhưng authority không rõ. Research memory đang hình thành; design_cases/principles chưa được promote. Governance phải bắt đầu sớm để bảo toàn bằng chứng, rồi hoàn thiện qua pilot trước 1.0.  
**Ảnh hưởng tới những medium nào:** Tất cả; áp dụng cho token, components, guidelines, tools, assets, exceptions và release.

**Bằng chứng ZO Math đã có:**
- DES-F-03; liên quan DES-AB-03, DES-D-01, DES-D-05, DES-E-05/06 và các khoảng trống provenance ở P0.3.
- P0-0017, P0-0021–0029, P0-0031–0040; research memory và audits được nêu trong P0.2/P0.3.

**Mức nền hiện tại:** **Vừa cho quy trình nghiên cứu/provenance đang hình thành; yếu cho governance của Design System.**  
**Những gì KHÔNG cần nghiên cứu lại từ đầu:** phân biệt source vs audit/snapshot/output; quy trình research memory; nguyên tắc không promote từ một quan sát đơn lẻ; các dấu hiệu provenance đã biết.  
**Những gì còn thiếu:** authority map; status transitions; acceptance roles/evidence; versioning/deprecation; migration/exception policy; audit retention; release gates; cách tránh canonical trùng lặp; liên kết giữa design case/principle và implementation.

**Loại công việc cần thiết:**
- phân tích nội bộ lineage/research/audit và quy trình release hiện có;
- nghiên cứu nguồn bên ngoài chỉ khi cần đối chiếu governance practice;
- technical validation cho provenance/version/release records;
- stakeholder feedback về quyền quyết định và trách nhiệm;
- thử nghiệm workflow proposal→trial→review→release/deprecation.

**Phụ thuộc vào:** khởi động song song R1 ở Pha 1 để điều hành nghiên cứu; nội dung lifecycle hoàn thiện cùng kết quả R3–R11 và pilot.  
**Đầu ra mong muốn:** governance model và hồ sơ quyết định có trạng thái/owner/evidence/versions, policy cho exception/deprecation/migration, quy trình review/acceptance/release.  
**Pha xử lý đề xuất:** Pha 1 tạo khung provenance; duy trì xuyên suốt; chốt readiness cùng Pha 5.  
**Điều kiện để coi chương trình đủ chín:** một đề xuất, thử nghiệm, quyết định được chấp nhận, ngoại lệ và thay đổi/deprecation đều có status/owner/rationale/evidence; quá trình review có thể truy lại; không dùng tên file hoặc sự hiện diện trong code làm thay thế quyết định; người có thẩm quyền xác nhận release gate.

## 4. Trình tự chương trình và cổng tổng hợp

| Pha | Trọng tâm | Chương trình và quan hệ | Cổng ra đề xuất |
|---|---|---|---|
| **Pha 1 — Nền và cách nghiên cứu** | Đặt nền thương hiệu, khung thuộc tính, bảo toàn provenance; mở miền Toán học không làm lại từ số 0 | Khởi động R12, R1, R2; R6 bắt đầu song song | R1 có hồ sơ nền tảng/ranh giới; R12 có cách ghi nguồn/trạng thái; R2 có câu hỏi kiểm chứng, chưa yêu cầu chốt tính cách |
| **Pha 2 — Nghiên cứu miền** | Nghiên cứu nhận dạng, màu, typography, toán, spatial layout, motion, audio | R3–R9; R1/R2/R6 làm tiền đề; R4/R5/R7/R8/R9 có thể chạy song song theo câu hỏi rõ | Mỗi chương trình có case đại diện, scope, phương pháp, evidence và gap; không nâng proposal thành chuẩn |
| **Pha 3 — Kiểm tra adaptation** | Kiểm tra shared meaning vs medium-specific output, gỡ mâu thuẫn giả | R10 tổng hợp đầu vào R3–R9; lặp các test readability/accessibility/visual theo medium | Có matrix core/adaptation/exception và các unresolved conflicts được giữ minh bạch |
| **Pha 4 — Architecture và automation** | Thiết kế proposal cho machine-readable model, component/tool contracts, provenance và validation | R11 dựa trên R10 và các quy tắc miền đủ chín; R12 tiếp tục quản lý lifecycle | Pilot có reproducible source→output, provenance, technical checks và human visual/semantic acceptance thích hợp |
| **Pha 5 — Thí điểm, nghiệm thu và 1.0** | Dùng sản phẩm đại diện, kiểm tra governance, xử lý exception và đánh giá mức sẵn sàng | Hoàn tất vòng lặp R3–R12; R1/R2 được xem xét khi có feedback thực tế | Chủ dự án xem bằng chứng liên medium, xác nhận quyết định còn mở, acceptance và release gate; chỉ sau đó mới lập kế hoạch ban hành 1.0 |

Pha 5 là **điều kiện dự kiến**, không phải cam kết rằng Design System 1.0 sẽ được phát hành khi hết một mốc lịch. Thiếu bằng chứng hoặc thiếu người có thẩm quyền nghiệm thu thì chương trình tiếp tục mở.

## 5. Tiêu chí sẵn sàng tiến tới Design System 1.0

P0.4 không kết luận bất kỳ tiêu chí nào đã đạt. Trước khi xem xét release 1.0, Research Map đề xuất cần có:

1. Nền tảng thương hiệu và ranh giới sản phẩm được xác nhận, có provenance và phần chưa chắc chắn được ghi riêng.
2. Các chương trình R3–R9 có kết quả nghiên cứu và điều kiện áp dụng; khác biệt medium được giải thích thay vì ép đồng nhất.
3. Ngôn ngữ Toán học đã được kiểm tra về nội dung chuyên môn, khả năng đọc và semantic/accessibility; compiler/receipt không thay visual acceptance.
4. Cross-medium matrix phân biệt shared meaning, medium realization, exceptions và validation.
5. Tokens/components/automation chỉ được đề xuất sau khi semantic roles rõ; pilot chứng minh source-to-output và provenance có thể truy vết.
6. Governance có status lifecycle, authority, review, version, exception, deprecation/migration và release records.
7. Các đánh giá trực quan, kỹ thuật, accessibility/readability và feedback được lưu với đúng sản phẩm/phiên bản/kịch bản.
8. Chủ dự án/người có thẩm quyền chấp nhận phạm vi 1.0, unresolved items và release gate; không suy ra acceptance từ tài liệu tồn tại hoặc implementation.

## 6. Những điều P0.4 không làm

- Không mở lại inventory hoặc đọc rộng repository; hai báo cáo P0.2/P0.3 là nguồn chính.
- Không tra cứu bên ngoài, không chọn phương án logo/palette/font/motion/audio.
- Không định nghĩa token, component hay specification cụ thể.
- Không xếp hạng medium theo ưu tiên và không coi 12 chương trình là dự án con đã được phê duyệt ngân sách/nguồn lực.
- Không tuyên bố chương trình nào, ứng viên DES nào hoặc quyết định thiết kế nào đã chốt.

**Kết luận:** P0.4 chuyển bằng chứng Pha 0 thành 12 chương trình nghiên cứu liên kết theo phụ thuộc. Thứ tự ưu tiên là xây nền và governance/provenance trước; nghiên cứu miền song song nhưng không tách khỏi mục tiêu Toán và người học; tổng hợp adaptation liên medium trước khi định hình tokens/automation; cuối cùng thử nghiệm, review và xem xét điều kiện phát hành 1.0. Pha 0 kết thúc bằng bản đồ này, không kết thúc bằng một hệ thiết kế đã được quyết định.
