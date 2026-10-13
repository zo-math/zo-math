# P1.1a — Baseline bằng chứng nội bộ cho R1

**Ngày lập:** 2026-10-06  
**Phạm vi:** bằng chứng nội bộ hiện có cho RQ-DS-R1-001 đến RQ-DS-R1-004 và VQ-DS-R1-001  
**Trạng thái:** báo cáo staging; chưa phải kết luận nền tảng thương hiệu, Principle hay Decision

## 1. Phạm vi

P1.1a tổng hợp có giới hạn các nguồn nội bộ được yêu cầu để lập baseline cho R1. Báo cáo không mở rộng khảo cổ P0.2/P0.3, không nghiên cứu bên ngoài, không viết manifesto, không chọn hướng thiết kế và không tạo hồ sơ chính thức trong `_research`.

Phân biệt xuyên suốt:

- **ZO Math evidence:** bằng chứng về điều một tài liệu, source hoặc lịch sử nội bộ thực sự nói/ghi nhận; không mặc nhiên chứng minh điều đó là sự thật giáo dục, ý định đã được phê duyệt hay kết quả đã đạt.
- **External evidence:** không có trong P1.1a. Những sách, tổ chức hoặc nghiên cứu được trích dẫn trong tài liệu nội bộ chưa được mở hay kiểm tra độc lập ở bước này.
- **Inference:** diễn giải do báo cáo rút ra từ bằng chứng; không gán lời diễn giải cho ZO Math.

“Mạnh/vừa/yếu” đánh giá mức hỗ trợ cho **claim hẹp** được ghi, không đánh giá mức trưởng thành của quyết định. Một phát biểu trực tiếp có thể là bằng chứng mạnh cho “About hiện nói X”, nhưng không chứng minh “X đã được chủ dự án duyệt làm nền tảng dài hạn” hoặc “X tạo hiệu quả học tập”.

## 2. Nguồn đã đọc

### 2.1 Mười tài liệu nội bộ

| # | Nguồn | Locator/phạm vi sử dụng |
|---|---|---|
| 1 | [`content/about.qmd`](../../../../content/about.qmd) | Toàn văn; đặc biệt phần mở đầu, “Học toán không chỉ để có một đáp án”, “Các mạch nội dung”, “ZO Math dành cho ai?”, “Một hướng phát triển mở”. |
| 2 | [`content/triet_li_va_dinh_huong.qmd`](../../../../content/triet_li_va_dinh_huong.qmd) | Toàn văn; phần mở đầu, hiểu/thành thạo, chứng minh, chủ thể người học, AI, xây dựng nội dung và định hướng. |
| 3 | [`_research/README.md`](../../../../_research/README.md) | Toàn văn; nguyên tắc, cấu trúc và quy trình sử dụng research memory. |
| 4 | [`_research/90_syntheses/SYN-2026-08-29_khoi-dau-he-thong-tri-nho-nghien-cuu.md`](../../../../_research/90_syntheses/SYN-2026-08-29_khoi-dau-he-thong-tri-nho-nghien-cuu.md) | Toàn văn; ưu tiên, mạch nghiên cứu dài hạn và trạng thái chưa phải framework. |
| 5 | [`_research/10_questions/RQ-003_nguyen-li-thiet-ke-bai-zomath.md`](../../../../_research/10_questions/RQ-003_nguyen-li-thiet-ke-bai-zomath.md) | Toàn văn; câu hỏi, các hướng liên quan và trạng thái `active-through-practice`. |
| 6 | [`P0.2`](../../pha_0/P0_2_khao_co_thiet_ke_ZO_Math.md) | Toàn văn; inventory, đặc biệt P0-0016/P0-0017 và mục provenance About. |
| 7 | [`P0.3`](../../pha_0/P0_3_ban_do_bang_chung_quyet_dinh_thiet_ke_ZO_Math.md) | Toàn văn; DES-F-01..03, phần ranh giới giá trị/implementation, giới hạn bằng chứng và câu hỏi About. |
| 8 | [`P0.4`](../../pha_0/P0_4_ban_do_nghien_cuu_ZO_Math_Design_System.md) | Toàn văn; R1 và trình tự phụ thuộc trong Research Map. |
| 9 | [`P1.0`](../P1_0_governance_provenance_toi_thieu.md) | Toàn văn; evidence model và phần hướng dẫn sử dụng cho P1.1. Đây là tài liệu đề xuất, chưa được coi là governance đã phê duyệt. |
| 10 | About handoff, `D:\Downloads\ZO_MATH_ABOUT_HANDOFF_20260829\01_SITE_IDENTITY_SOURCES\content\about.qmd` | Toàn văn; bản snapshot 37 dòng, dùng đối chiếu VQ. |
| 11 | About integration, `D:\Downloads\ZO_MATH_ABOUT_INTEGRATION_20260829\content\about.qmd` | Toàn văn; bản snapshot 59 dòng, dùng đối chiếu VQ. |

**Lưu ý cách đếm:** bảng có 11 đường dẫn/tài liệu được đọc: chín tài liệu trong repository (tám nguồn bắt buộc, cộng P0.2 để truy xuất provenance snapshot) và hai snapshot Downloads. Các commit Git nêu ở VQ được tính riêng, không tính là tài liệu độc lập.

### 2.2 Git history đã kiểm tra có mục tiêu

- `b934f0c` — 2026-08-30, `content(site): add philosophy page and unify about pages`; commit thay đổi `content/about.qmd` và thêm `content/triet_li_va_dinh_huong.qmd`.
- `6ad2a49` — 2025-03-15, `Cập nhật ZO Math`; history theo đường dẫn cho thấy About khi đó còn ở root `about.qmd`. Nội dung snapshot này được đối chiếu chọn lọc.
- `git log --follow` cho thấy đường dẫn `about.qmd` được đổi sang `content/about.qmd` ở `e7b2675` ngày 2025-03-20; các commit trước đó gồm `657a4a6` và `487cda4`.

Commit message và lịch sử đường dẫn hỗ trợ provenance kỹ thuật; chúng không tự chứng minh ai phê duyệt nội dung hoặc mức thẩm quyền thương hiệu.

## 3. RQ-DS-R1-001 — ZO Math là gì?

### A. Claim trực tiếp

1. About hiện hành tự mô tả ZO Math là “một không gian giáo dục toán học” — không gọi mình là một khóa học hay chỉ là website. [E01]
2. About nói ZO Math xây dựng nội dung và tài nguyên học tập; nội dung có thể được thể hiện bằng bài viết, video, khóa học, hình ảnh, công cụ hoặc hình thức khác. [E01, E03]
3. About mô tả nhiều mạch nội dung, trong đó Toán phổ thông là một mạch lớn bên cạnh đọc/phân tích tác phẩm, khóa học, chủ đề do ZO Math phát triển và công cụ hỗ trợ học. [E03]
4. About nói hướng phát triển có thể mở từ toán phổ thông sang tiền đại học, đại học và các lĩnh vực toán học sâu hơn. Đây là định hướng được văn bản công bố, không phải bằng chứng rằng việc mở rộng đã xảy ra hoặc được bảo đảm. [E05]
5. Trang triết lí nói rõ ZO Math chưa bắt đầu từ một triết lí giáo dục toán học hoàn chỉnh; các quan niệm hình thành dần và có thể thay đổi. [E06]
6. Research synthesis gọi bản đồ dài hạn là bản đồ đang hình thành, chưa phải framework khoa học đã xác lập; đồng thời nêu sản xuất là dòng chính và nghiên cứu cần trưởng thành cùng thực hành. [E12]

### B. Pattern lặp lại

- About, trang triết lí và research memory cùng thể hiện một dự án giáo dục toán đang phát triển, có nhiều mạch/cách thể hiện và giữ trạng thái mở cho các quan niệm của mình. Đây là pattern trong **tài liệu nội bộ**, chưa phải xác nhận độc lập về bản chất thương hiệu. [E01, E03, E06, E12, E13]

### C. Inference

1. Phát biểu “không gian giáo dục toán học” cùng phạm vi nội dung rộng là ứng viên mô tả cấp thương hiệu tốt hơn các mô tả đơn lẻ về website, khóa học hoặc dự án THPT; báo cáo không nâng nó thành định nghĩa cuối.
2. Các kênh như website/video/công cụ hiện được mô tả như hình thức hoặc phương tiện thể hiện nội dung, không phải bản chất định danh độc lập.

### D. Hypothesis

- Một mô tả dài hạn của ZO Math có thể cần giữ đồng thời hai vế: giáo dục toán học là phạm vi hoạt động; cách tổ chức việc học/hiểu toán là phần định hướng. Cần chủ dự án xác nhận phạm vi và trọng số; đây chưa phải câu chữ đề xuất để công bố.

### E. Open gap

- Chưa có bằng chứng được chủ dự án xác nhận về ranh giới “cốt lõi dài hạn” so với mục tiêu của từng sản phẩm, cũng như về tính ổn định của định hướng khi mở rộng khỏi toán phổ thông.
- Chưa có kiểm tra thực tiễn đủ rộng để xác nhận các sản phẩm hiện tại có nhất quán với những phát biểu cấp thương hiệu này hay không.

## 4. RQ-DS-R1-002 — ZO Math giải quyết vấn đề gì?

### A. Claim trực tiếp

1. About phân biệt kết quả đúng/thành thạo thủ tục với việc thực sự hiểu kiến thức; một đáp án hoặc khả năng tái hiện công thức chưa cho biết người học hiểu vì sao, khi nào dùng hoặc xử lý ra sao khi bài toán đổi khác. [E02]
2. About nêu mục tiêu để người học nhận ra quan hệ/cấu trúc, lựa chọn cách tiếp cận, dùng điều đã biết trong tình huống mới và tự kiểm tra hiểu biết. [E02]
3. Trang triết lí nói đánh giá việc học không thể chỉ dựa vào sản phẩm cuối, vì sự hiểu biết được suy ra từ những gì người học nói/làm/tạo ra; đồng thời khẳng định hiểu biết và thành thạo không phải hai phía loại trừ nhau. [E06, E07]
4. Trang triết lí coi suy lí, kiến tạo ý nghĩa, tìm căn cứ, phản ví dụ và chứng minh là các hoạt động quan trọng; chứng minh gắn với câu hỏi “vì sao ta được quyền khẳng định điều này?”. [E06, E07]
5. Các nguồn nói người học cần có cơ hội đặt câu hỏi, quan sát, phỏng đoán, thử nghiệm, giải thích/biện minh, kết nối biểu diễn, phát hiện và sửa sai, lựa chọn và tự kiểm tra. [E02, E07, E09]
6. Trang triết lí nêu mục tiêu giữ lại phần việc trí tuệ cho người học; không yêu cầu họ tự khám phá mọi thứ, và chấp nhận trình bày trực tiếp, hướng dẫn hoặc luyện tập khi phù hợp. [E07]
7. Nguồn nói cách tổ chức việc học cần thay đổi theo nội dung và mục đích; không đặt “hiểu” đối lập với “luyện tập/kĩ thuật”. [E02, E07]

### B. Pattern lặp lại

1. About, triết lí và RQ-003 lặp lại trục “đáp án/thủ tục không đủ để mô tả hiểu biết”, đi cùng giải thích, quan hệ, suy luận hoặc tự kiểm tra. [E02, E06, E07, E13]
2. Nhiều nguồn nhấn mạnh căn cứ và tự kiểm tra thay vì chỉ tiếp nhận/tái hiện kết quả; đồng thời không phủ nhận tính chính xác, thủ tục, hướng dẫn hay luyện tập. [E02, E07, E11]

### C. Inference

- Vấn đề giáo dục được các văn bản **đặt ra** là nguy cơ nhầm sản phẩm đúng/tái hiện thủ tục với hiểu biết có thể giải thích, kiểm tra và sử dụng. Các tài liệu chưa chứng minh đây là pain point phổ biến của mọi nhóm người học hoặc đã đo được mức độ của vấn đề.

### D. Hypothesis

- Cơ hội suy luận, kết nối biểu diễn, tự kiểm tra và giữ lại phần việc trí tuệ có thể là những hướng thiết kế giúp xử lý vấn đề nội bộ nêu trên; hiệu quả thực tế cần được kiểm tra với người học và sản phẩm cụ thể.

### E. Open gap

- Chưa có dữ liệu nội bộ về tần suất/mức độ người học gặp các khó khăn này, nhóm nào chịu ảnh hưởng, hoặc sản phẩm nào đang giải quyết chúng tốt/chưa tốt.
- “Khả năng tiếp cận tri thức” hoặc một vấn đề hệ thống rộng hơn chưa được nguồn bắt buộc nêu cụ thể như vấn đề trung tâm của thương hiệu. Không tự thêm thành pain point.

## 5. RQ-DS-R1-003 — ZO Math phục vụ ai?

### A. Claim trực tiếp

1. About hiện hành hướng tới “những người muốn học toán ở nhiều mức độ và với nhiều mục đích khác nhau”; nêu các mục đích gồm củng cố kĩ thuật, chuẩn bị kì thi, học lại chủ đề và tìm hiểu sâu hơn. [E04]
2. About hiện hành không giới hạn người học vào một cấp học hay một hình thức học; văn bản nói người học không phải học toán theo cùng một cách. [E04]
3. About handoff lịch sử từng gọi đối tượng là học sinh, sinh viên, người cần học toán và người yêu toán; nội dung lịch sử cũng nêu học theo sách giáo khoa từ tiểu học đến đại học và luyện thi. Đây là lời của snapshot cũ, không tự động là phân khúc hiện hành. [E15]
4. Triết lí nhắc giáo viên, sách, video và công cụ như các nguồn có thể hỗ trợ người học; tài liệu không vì thế gọi giáo viên là nhóm khách hàng/đối tượng thương hiệu. [E07]
5. Research README và synthesis ghi thực hành trước mắt ưu tiên phát triển toán phổ thông, đặc biệt các mạch có giá trị thực tế/khả năng tạo nguồn lực cho dự án; đây là ưu tiên hoạt động, không phải danh sách toàn bộ đối tượng của thương hiệu. [E10, E12]

### B. Pattern lặp lại

- Tài liệu cũ và hiện hành đều nêu người học với mục đích đa dạng, nhưng cách gọi và phạm vi cấp học thay đổi đáng kể. Bằng chứng này ủng hộ việc giữ riêng “đối tượng được bản About lịch sử nêu” và “cách About hiện hành mô tả người học”, không hợp nhất thành một persona đã xác nhận. [E04, E15]

### C. Inference

1. Người tự học có thể nằm trong nhóm “những người muốn học toán”, nhưng thuật ngữ/nhóm “người tự học” không được nguồn hiện hành trực tiếp xác lập.
2. Các nhóm người học của từng project/cấp học cần ghi theo scope riêng; ưu tiên THPT hiện tại không chứng minh toàn thương hiệu chỉ phục vụ học sinh THPT.

### D. Hypothesis

- Có thể tồn tại nhiều phân đoạn theo trình độ, mục đích và mức độ chủ động học; cần xác minh bằng đối thoại với chủ dự án và phản hồi của người dùng thay vì hợp nhất danh sách ở các tài liệu khác thời điểm.

### E. Open gap

- Chưa có phân khúc người dùng cấp thương hiệu được chủ dự án duyệt hoặc được kiểm chứng bằng dữ liệu; chưa rõ tỷ trọng/mức ưu tiên giữa học sinh, sinh viên, người tự học, người yêu Toán, giáo viên và các nhóm khác.
- Không có bằng chứng trong tập bắt buộc để xác nhận giáo viên là đối tượng trực tiếp của sản phẩm/thương hiệu, thay vì người dạy, cộng tác viên hoặc bên trung gian.

## 6. RQ-DS-R1-004 — Vai trò của công nghệ

### A. Claim trực tiếp

1. About mô tả website không phải theo cách “ZO Math là website”; nó liệt kê website-like formats như bài viết, video, khóa học, hình ảnh và công cụ như những hình thức nội dung có thể dùng. [E01, E03]
2. Trang triết lí nói AI có thể trở thành công cụ của việc học toán; câu hỏi đang mở là AI làm phần nào và người học còn phải làm phần nào. Nguồn nói rõ chưa có câu trả lời chung cho mọi tình huống. [E08]
3. Trang triết lí không coi chống AI là mục tiêu giáo dục và không mặc nhiên coi AI là chủ thể học thay người học. Đây là định hướng được văn bản nêu, không phải chính sách AI đã được ban hành cho mọi sản phẩm. [E08]
4. Research README đề cập AI như khả năng hỗ trợ truy xuất research memory; đây là mô tả vận hành tiềm năng, không phải định vị thương hiệu AI. [E10]
5. P0.3 phân biệt workflow/công cụ sản xuất với ý nghĩa thương hiệu; P1.0 cũng nói tool/AI không tự xác nhận acceptance hay authority. Đây là ranh giới phương pháp luận, không phải tuyên bố rằng ZO Math đã có một chính sách công nghệ hoàn chỉnh. [E13, E14]

### B. Pattern lặp lại

- Trong các nguồn, công nghệ xuất hiện như hình thức truyền đạt, công cụ hỗ trợ học hoặc công cụ truy xuất/sản xuất; không có mệnh đề nào trong tập nguồn định nghĩa ZO Math là một “AI brand”. [E03, E08, E10, E13]

### C. Inference

1. Bằng chứng hiện tại phù hợp hơn với cách đọc “công nghệ là phương tiện/công cụ” so với “công nghệ là bản chất thương hiệu”; đây là inference từ mô tả, không phải định vị đã được chủ dự án xác nhận.
2. Vai trò của automation, phần mềm sản xuất và hạ tầng kỹ thuật vẫn chưa được xác định đầy đủ trong tập nguồn R1; không suy từ việc có công cụ/pipeline sang mục đích thương hiệu.

### D. Hypothesis

1. Có thể phân biệt vai trò công nghệ theo ngữ cảnh: công cụ học cho người học, phương tiện truyền đạt, công cụ sản xuất và hạ tầng. Cần kiểm tra xem phân biệt này có khớp thực tiễn và chủ đích của dự án hay không.
2. Định hướng AI có thể xoay quanh việc bảo toàn vai trò suy nghĩ/kiểm chứng của người học; đây là hypothesis từ trang triết lí, chưa phải chính sách dùng AI hoặc yêu cầu sản phẩm.

### E. Open gap

- Chưa có tuyên bố cấp thương hiệu về mức độ công nghệ là bản chất hay phương tiện, cũng chưa có ranh giới được duyệt cho AI, automation, phần mềm và sản phẩm công nghệ tương lai.
- Chưa có bằng chứng user/owner feedback cho biết người dùng hiện nhận diện ZO Math qua công nghệ nào, hoặc công nghệ có phải lý do chọn sản phẩm hay không.

## 7. VQ-DS-R1-001 — Provenance About

**Câu hỏi:** Các phiên bản `about.qmd` lịch sử và hiện hành có thay đổi nền tảng thương hiệu hay chủ yếu là thay đổi biên tập/provenance?

### A. Claim trực tiếp / quan sát trực tiếp

1. Snapshot handoff ngày 2026-08-29 mô tả ZO Math là “trang toán học” cho học sinh, sinh viên, người cần học toán và người yêu toán; dùng giọng văn thân mật, nêu phương pháp “Tầm nguyên và Tái hiện”, luyện thi, sách giáo khoa, công cụ và ZO Shelf. [E15]
2. Snapshot integration ngày 2026-08-29 và About hiện hành dùng mô tả “không gian giáo dục toán học”; mô tả nhiều mạch nội dung, chuyển trọng tâm câu chữ sang quan hệ/cấu trúc, hiểu, tự kiểm tra và các mục đích học đa dạng. Nội dung chính của integration gần với bản hiện hành; khác biệt đáng thấy gồm front matter/navigation và chi tiết biên tập. [E01, E16]
3. Git ghi nhận commit `b934f0c` ngày 2026-08-30 với thông điệp “add philosophy page and unify about pages”; commit sửa About hiện hành và thêm trang triết lí. Lịch sử trước đó cho thấy About tồn tại từ 2025 và được chuyển từ root vào `content/`. [E17]

### B. Pattern lặp lại

- Từ snapshot integration sang About hiện tại, phần định hướng giáo dục cốt lõi nhìn chung được duy trì; khác biệt chủ yếu quan sát được là lớp trình bày, cấu hình trang và liên kết điều hướng. Cần thận trọng vì không có hồ sơ phê duyệt nội dung đi kèm để xác nhận toàn bộ quan hệ kế thừa.

### C. Inference

1. Từ handoff sang integration/current, thay đổi không chỉ là biên tập câu chữ: đối tượng được gọi tên, cách mô tả phạm vi ZO Math, cấu trúc các mạch nội dung và cách diễn đạt trọng tâm giáo dục đều được tổ chức lại. Vì vậy, kết luận “chỉ thay đổi provenance/biên tập” không được hỗ trợ.
2. Các bản integration/current có vẻ là một articulation mới có tính nền tảng hơn bản handoff cũ, nhưng không thể khẳng định đây là thay đổi nền tảng đã được chủ dự án chấp thuận. Cần phân biệt thay đổi **trong văn bản** với thay đổi **được phê duyệt về định vị**.
3. Commit 2026-08-30 là dấu provenance kỹ thuật hỗ trợ rằng hai trang About/triết lí được hợp nhất/tổ chức lại ở repository; commit message không chỉ rõ snapshot Downloads nào là nguồn được duyệt.

### D. Hypothesis

- Handoff có thể là bản verbal identity cũ/nguồn đầu vào, còn integration/current là bản tái biên tập với định hướng giáo dục rõ và rộng hơn. Cần người tạo/duyệt xác nhận lineage và ý nghĩa thay đổi trước khi xem đây là kết luận lịch sử.

### E. Open gap

- Chưa có metadata/biên bản trong các snapshot xác nhận tác giả, người duyệt, quan hệ nguồn–đích hoặc trạng thái “handoff/integration”; tên thư mục và ngày không tự tạo authority.
- Chưa xác nhận được thay đổi ở bản hiện hành là quyết định đổi nền tảng thương hiệu hay là bản biên tập diễn đạt lại cùng một định hướng.
- Git history giúp xác nhận thay đổi tệp/ngày/commit nhưng không giải quyết được ý định, mức phê duyệt, audience validation hay acceptance của chủ dự án.

**Kết luận VQ:** giải quyết được phần so sánh văn bản và provenance kỹ thuật trong phạm vi nguồn đã cho; **chưa giải quyết được** câu hỏi liệu nền tảng thương hiệu có thực sự được đổi và được chủ dự án duyệt hay không.

## 8. Các claim có bằng chứng mạnh

“Mạnh” dưới đây chỉ có nghĩa văn bản được dẫn nói trực tiếp và locator rõ:

1. About hiện hành tự gọi ZO Math là một không gian giáo dục toán học. [E01]
2. About mô tả nhiều mạch nội dung và nhiều định dạng, không chỉ một khóa học hoặc một kênh. [E03]
3. About công bố định hướng phục vụ người học với nhiều mức độ/mục đích; handoff lịch sử nêu một danh sách khác, có phạm vi/thời điểm riêng. [E04, E15]
4. About và trang triết lí trực tiếp phân biệt đáp án/thủ tục với bằng chứng về hiểu biết, đồng thời không phủ nhận vai trò của thành thạo/luyện tập. [E02, E06, E07]
5. Trang triết lí trực tiếp nói quan niệm giáo dục chưa hoàn chỉnh và câu hỏi về AI chưa có câu trả lời chung. [E06, E08]
6. Snapshot và Git history xác nhận có thay đổi văn bản About giữa handoff và integration/current; commit `b934f0c` là dấu vết tổ chức lại About và thêm trang triết lí. [E15–E17]

Các claim này mạnh về **nội dung/tình trạng nguồn**, không đủ để kết luận hiệu quả sư phạm, tính đại diện của audience, định vị được duyệt hay quyết định thiết kế cuối.

## 9. Các inference cần giữ riêng

1. ZO Math có thể được mô tả ở cấp rộng hơn website/khóa học; chủ đích cấp thương hiệu này vẫn cần chủ dự án xác nhận.
2. “Đáp án đúng nhưng chưa hiểu” là vấn đề được verbal identity đặt ra, không phải pain point đã được đo lường.
3. Có thể tồn tại các audience theo cấp học, mục đích và mức độ tự học; chưa có cơ sở để gộp các nhóm qua những phiên bản/scope khác nhau.
4. Giáo viên hiện được nêu như nguồn hỗ trợ người học, không phải bằng chứng xác lập giáo viên là customer/audience.
5. Định hướng học tập trong triết lí được mở rộng sang AI, nhưng chưa tương đương policy hoặc product requirements.
6. Công nghệ hiện được trình bày như phương tiện/công cụ nhiều hơn bản chất thương hiệu; đây chưa phải tuyên bố positioning.
7. Handoff so với integration/current có thay đổi đáng kể cách định vị bằng lời, nhưng chủ đích và acceptance của thay đổi còn chưa rõ.
8. Research README/synthesis phản ánh ưu tiên vận hành và memory practice; không tự thay thế một tuyên bố thương hiệu đã duyệt.
9. Việc tài liệu dẫn NCTM hoặc sách về đánh giá là bằng chứng ZO Math sử dụng/dẫn các nguồn ấy trong văn bản; nội dung ngoài chưa được xác minh ở P1.1a.

## 10. Các hypothesis cần kiểm tra

1. Định nghĩa dài hạn của ZO Math có thể kết hợp phạm vi giáo dục toán học với một định hướng về hiểu/suy nghĩ; cần owner confirmation.
2. Tạo cơ hội suy luận và tự kiểm tra có thể xử lý một phần vấn đề giáo dục mà văn bản nêu; cần kiểm tra trên sản phẩm và người học thực.
3. Phân đoạn audience theo trình độ, mục đích và mức chủ động có thể hữu ích hơn danh sách đối tượng gộp; chưa có dữ liệu xác nhận.
4. Công nghệ có thể có các vai trò khác nhau tùy ngữ cảnh (học, truyền đạt, sản xuất, hạ tầng) mà không trở thành brand essence; cần xác nhận thực hành và chủ đích.
5. Trang integration/current có thể là tái định vị diễn đạt so với handoff, nhưng chưa có provenance phê duyệt để xác nhận.
6. Cách đặt AI có thể ưu tiên duy trì quyền suy nghĩ/kiểm chứng của người học; chưa thể coi là chính sách áp dụng chung.

## 11. Các khoảng trống cần nghiên cứu bên ngoài

Không có External evidence trong báo cáo này. Nghiên cứu bên ngoài chỉ thực sự cần khi câu hỏi chuyển từ “ZO Math hiện nói gì/định hướng gì?” sang kiểm tra bối cảnh hoặc tác động:

1. **Bối cảnh vấn đề học Toán:** nếu muốn khẳng định các khó khăn về hiểu, suy luận, transfer hoặc tự kiểm tra là phổ biến/quan trọng với một nhóm cụ thể, cần nguồn nghiên cứu đáng tin và phù hợp đối tượng; About/triết lí không đủ để chứng minh độ phổ biến.
2. **Nhu cầu và phân đoạn người dùng:** cần user research/feedback với các nhóm thực tế (người học theo cấp độ/mục đích, và giáo viên nếu chủ dự án coi họ là audience). Đây là nghiên cứu người dùng, không thể thay bằng suy luận từ cách viết About.
3. **AI và học tập:** nếu R1 muốn viện dẫn tác động/điều kiện sử dụng AI, cần xem nguồn nghiên cứu bên ngoài phù hợp; nguồn nội bộ hiện chỉ nêu một câu hỏi định hướng.

Không cần nghiên cứu bên ngoài để quyết định chủ dự án muốn ZO Math là gì, bản About nào được duyệt, hay giáo viên/nhóm nào thuộc audience chủ đích. Những câu hỏi đó trước hết cần xác nhận nội bộ/owner. Không cần external research để biến các lời tuyên bố trong About thành “bằng chứng hiệu quả”.

## 12. Các câu hỏi cần chủ dự án xác nhận trực tiếp

1. “Không gian giáo dục toán học” có phải mô tả cấp thương hiệu dài hạn mà chủ dự án muốn giữ, hay chỉ là cách viết của About hiện hành?
2. Mối quan tâm về hiểu, suy luận, biện minh, chứng minh và tự kiểm tra: đâu là định hướng cốt lõi, đâu là hướng đang thử nghiệm, và đâu vẫn là câu hỏi mở?
3. Các mạch sản phẩm và nhóm người học nào thuộc phạm vi thương hiệu dài hạn; nhóm nào chỉ là ưu tiên hiện tại của một project (đặc biệt toán phổ thông/THPT)?
4. Giáo viên là đối tượng trực tiếp, người ảnh hưởng, người dùng trung gian hay chỉ được nhắc như một nguồn hỗ trợ?
5. Người tự học và người yêu Toán có còn là audience chủ đích hiện nay? Nếu có, ở mức nào so với học sinh/sinh viên và người học theo kỳ thi?
6. Công nghệ/AI nên được hiểu là phương tiện, năng lực sản phẩm, hạ tầng hay một phần định vị; có giới hạn nào đã được chủ dự án quyết định?
7. Handoff và integration About được tạo/duyệt bởi ai, quan hệ lineage ra sao, và thay đổi nào phản ánh đổi nền tảng thay vì biên tập?
8. Các tuyên bố về định hướng mở rộng lên toán tiền đại học/đại học là ý định dài hạn, ưu tiên chiến lược hay chỉ là khả năng đang cân nhắc?

## 13. Đề xuất bước P1.1b

**Chỉ đề xuất, chưa thực hiện:** tổ chức một lượt xác nhận nội bộ có provenance với chủ dự án cho các câu hỏi ở mục 12; đối chiếu câu trả lời với About hiện hành, triết lí, RQ-003 và ưu tiên sản phẩm; ghi riêng claim được xác nhận, claim cần sửa, inference và câu hỏi còn mở. Sau đó mới xác định câu hỏi nào thực sự cần user research hoặc external evidence.

P1.1b không nên viết manifesto hay chuyển nguyên văn câu trả lời thành Principle/Decision trước khi có scope, bằng chứng và phê duyệt phù hợp. Báo cáo P1.1a hiện chỉ là staging evidence; chưa tạo/cập nhật hồ sơ trong `_research`.

## Phụ lục A — Evidence register

| ID | Lớp | Nguồn và locator | Ngày/version | Claim được hỗ trợ | Không chứng minh | Strength |
|---|---|---|---|---|---|---|
| E01 | ZO Math evidence | [`content/about.qmd`](../../../../content/about.qmd), dòng 12–18 | Bản hiện hành; commit `b934f0c`, 2026-08-30 | Tự mô tả “không gian giáo dục toán học”; nêu nội dung/tài nguyên, nhiều hình thức và cách tiếp cận | Không chứng minh positioning đã duyệt hoặc mức độ hiện thực hóa | Mạnh cho “văn bản nói gì”; yếu cho authority |
| E02 | ZO Math evidence | [`content/about.qmd`](../../../../content/about.qmd), “Học toán không chỉ để có một đáp án”, dòng 20–37 | Bản hiện hành | Phân biệt đáp án/thủ tục với hiểu, quan hệ, sử dụng trong tình huống mới, tự kiểm tra | Không chứng minh hiệu quả hoặc mức phổ biến của vấn đề | Mạnh cho lời tuyên bố |
| E03 | ZO Math evidence | [`content/about.qmd`](../../../../content/about.qmd), mở đầu và “Các mạch nội dung”, dòng 12–18, 39–46 | Bản hiện hành | Nhiều mạch và hình thức; THPT là một mạch lớn trong phạm vi rộng hơn | Không chứng minh các mạch đều đang hoạt động ở cùng mức | Mạnh cho nội dung, vừa cho trạng thái thực tế |
| E04 | ZO Math evidence | [`content/about.qmd`](../../../../content/about.qmd), “ZO Math dành cho ai?”, dòng 48–53 | Bản hiện hành | Người học đa dạng về mức độ/mục đích; có ví dụ mục đích cụ thể | Không chứng minh phân khúc, quy mô hoặc người dùng thực tế | Mạnh cho cách văn bản định nghĩa audience |
| E05 | ZO Math evidence | [`content/about.qmd`](../../../../content/about.qmd), “Một hướng phát triển mở”, dòng 56–61 | Bản hiện hành | Nêu ý định mở rộng vượt toán phổ thông và tiếp tục xem xét cách làm | Không chứng minh roadmap được duyệt, nguồn lực hoặc triển khai | Mạnh cho phát biểu; yếu cho cam kết |
| E06 | ZO Math evidence | [`content/triet_li_va_dinh_huong.qmd`](../../../../content/triet_li_va_dinh_huong.qmd), mở đầu, phần hiểu/suy lí/thành thạo, khoảng dòng 12–42 | Bản hiện hành; được thêm ở commit `b934f0c` | Triết lí chưa hoàn chỉnh; mô tả quan niệm về hiểu, suy lí, kiến tạo ý nghĩa và thành thạo | Không xác minh độc lập các nguồn nghiên cứu được dẫn hoặc acceptance của chủ dự án | Mạnh cho lời tài liệu |
| E07 | ZO Math evidence | [`content/triet_li_va_dinh_huong.qmd`](../../../../content/triet_li_va_dinh_huong.qmd), “Từ phỏng đoán đến chứng minh”, “Người học là chủ thể của việc học”, khoảng dòng 43–77 | Bản hiện hành | Vai trò căn cứ/chứng minh, phần việc trí tuệ, cơ hội tự kiểm tra; thừa nhận hướng dẫn/luyện tập | Không chứng minh người học hiện có các cơ hội đó trong mọi sản phẩm | Mạnh cho định hướng được viết |
| E08 | ZO Math evidence | [`content/triet_li_va_dinh_huong.qmd`](../../../../content/triet_li_va_dinh_huong.qmd), “Khi AI có thể tạo ra lời giải”, khoảng dòng 79–103 | Bản hiện hành | AI có thể là công cụ; vai trò người học là vấn đề mở; chưa có câu trả lời chung | Không phải policy AI, đánh giá sản phẩm AI hay nghiên cứu tác động | Mạnh cho trạng thái văn bản |
| E09 | ZO Math evidence | [`content/triet_li_va_dinh_huong.qmd`](../../../../content/triet_li_va_dinh_huong.qmd), “Từ quan niệm đến cách xây dựng nội dung” và “Định hướng”, khoảng dòng 105–154 | Bản hiện hành | Nêu một số hướng thực hành và việc tiếp tục sửa quan niệm; phổ thông là mạch có thực hành rõ nhất | Không phải bộ tiêu chuẩn hoàn chỉnh hoặc đánh giá độc lập | Mạnh cho điều tài liệu tuyên bố |
| E10 | ZO Math evidence | [`_research/README.md`](../../../../_research/README.md), “Nguyên tắc”, “Quy trình sử dụng hằng ngày”, “Truy xuất bằng AI” | Bản hiện hành | Research memory phân biệt lời nguồn/diễn giải/giả thuyết; ưu tiên thực hành; AI được nhắc như khả năng truy xuất | Không chứng minh positioning thương hiệu hay một AI capability đã triển khai | Mạnh cho quy trình được ghi |
| E11 | ZO Math evidence | [`RQ-003`](../../../../_research/10_questions/RQ-003_nguyen-li-thiet-ke-bai-zomath.md), câu hỏi, hướng liên quan, trạng thái | `active-through-practice` | Các chủ đề understanding, representation, reasoning, proof, AI và learner agency còn được giữ làm câu hỏi thực hành | Không phải kết quả nghiên cứu hoặc nguyên lý đã xác nhận | Mạnh cho status/nội dung hồ sơ |
| E12 | ZO Math evidence | [`SYN-2026-08-29`](../../../../_research/90_syntheses/SYN-2026-08-29_khoi-dau-he-thong-tri-nho-nghien-cuu.md), “Bản đồ nghiên cứu dài hạn”, “Phát hiện vận hành” | 2026-08-29 | Nghiên cứu dài hạn đang hình thành; sản xuất là dòng chính; lưu lịch sử thiết kế | Không phải framework khoa học đã xác lập hay brand strategy được duyệt | Mạnh cho tuyên bố synthesis |
| E13 | ZO Math evidence | [`P0.3`](../../pha_0/P0_3_ban_do_bang_chung_quyet_dinh_thiet_ke_ZO_Math.md), DES-F-01..03; mục 12–15 | Pha 0.3 | Xếp About/triết lí/research thành verbal identity và nêu giới hạn evidence/provenance | Không xác nhận bản About nào là canonical hoặc nội dung giáo dục dẫn tới visual rule | Mạnh trong phạm vi báo cáo P0.3 |
| E14 | ZO Math evidence | [`P0.4`](../../pha_0/P0_4_ban_do_nghien_cuu_ZO_Math_Design_System.md), R1; [`P1.0`](../P1_0_governance_provenance_toi_thieu.md), evidence model và phần P1.1 | P0.4/P1.0 | Xác định câu hỏi R1, gaps và cách tách evidence class/claim/limit | P1.0 là proposal; không chứng minh đã được chủ dự án phê duyệt | Mạnh cho phạm vi/đề xuất ghi trong audit |
| E15 | ZO Math evidence | `D:\Downloads\ZO_MATH_ABOUT_HANDOFF_20260829\01_SITE_IDENTITY_SOURCES\content\about.qmd`, toàn văn | Snapshot handoff, 2026-08-29 theo tên thư mục | Wording lịch sử về audience, “trang toán học”, phương pháp và phạm vi nội dung | Không chứng minh tác giả, acceptance, trạng thái phát hành hay authority | Mạnh cho nội dung snapshot; yếu cho provenance |
| E16 | ZO Math evidence | `D:\Downloads\ZO_MATH_ABOUT_INTEGRATION_20260829\content\about.qmd`, toàn văn | Snapshot integration, 2026-08-29 theo tên thư mục | Bản wording gần với About hiện hành về phạm vi, cách tiếp cận, người học và các mạch nội dung | Không chứng minh đây là nguồn trực tiếp của commit hiện hành hoặc đã được duyệt | Mạnh cho nội dung snapshot; yếu cho lineage |
| E17 | ZO Math evidence | Git history `b934f0c`, `e7b2675`, `6ad2a49`, `487cda4`, `657a4a6`; `git log --follow` và diff About | 2025-03 đến 2026-08-30 | Lịch sử đường dẫn/commit và thay đổi file About; commit 2026 thêm triết lí và “unify about pages” | Không chứng minh ý định thương hiệu, người phê duyệt hoặc quan hệ với snapshot Downloads | Mạnh cho provenance Git; yếu cho approval |

## Phụ lục B — Tally các phát hiện

Đếm các mục được đánh số trong phần A–E của bốn RQ và VQ; không đếm từng câu con trong evidence register. Một mục chỉ nằm ở một loại để tránh đếm lặp.

| Loại | Số mục |
|---|---:|
| Claim trực tiếp / quan sát trực tiếp | 26 |
| Pattern lặp lại | 6 |
| Inference | 10 |
| Hypothesis | 6 |
| Open gap | 11 |

**Kiểm tra tally:** RQ-001: 6 direct / 1 pattern / 2 inference / 1 hypothesis / 2 gap; RQ-002: 7 / 2 / 1 / 1 / 2; RQ-003: 5 / 1 / 2 / 1 / 2; RQ-004: 5 / 1 / 2 / 2 / 2; VQ: 3 / 1 / 3 / 1 / 3. Tổng lần lượt là **26 direct / 6 pattern / 10 inference / 6 hypothesis / 11 gap**.
