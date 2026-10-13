# P1.1e — Kết tinh ER-01 thành hệ quả cho nền tảng thương hiệu và hệ thiết kế ZO Math

**Ngày lập:** 2026-10-05  
**Phạm vi:** kết tinh các phát hiện của P1.1d — ER-01 thành hệ quả có liên quan trực tiếp tới R1 và nghiên cứu Hệ thiết kế/ngôn ngữ thương hiệu ZO Math.  
**Trạng thái:** staging research; không phải Decision, Principle, canonical hay specification.

## 1. Mục tiêu

P1.1e không mở thêm nghiên cứu bên ngoài. Mục tiêu là trả lời ba câu hỏi:

1. ER-01 củng cố những claim nền tảng nào của ZO Math?
2. Claim nào cần thu hẹp hoặc giữ ở trạng thái câu hỏi?
3. Những phát hiện đó tạo ra những ràng buộc thiết kế cấp cao nào đáng mang sang các chương trình nghiên cứu tiếp theo?

P1.1e không biến kết quả nghiên cứu giáo dục Toán thành Design Principle. Các hệ quả thiết kế dưới đây chỉ là **candidate constraints** để nghiên cứu tiếp.

## 2. Nguồn

Nguồn trực tiếp:

- `P1_1d_ER01_boi_canh_hoc_Toan.md`
- `P1_1a_baseline_bang_chung_noi_bo_R1.md`
- `P1_1b_xac_nhan_noi_bo_chu_du_an_R1.md`
- `P1_1c_ket_tinh_pham_vi_doi_tuong_R1.md`

Không dùng thêm external source ngoài những nguồn đã được ER-01 tổng hợp.

## 3. Những claim nền tảng được ER-01 củng cố

### 3.1. Không đồng nhất đáp án/thủ tục với toàn bộ sự hiểu

ER-01 hỗ trợ cách diễn đạt thận trọng rằng một đáp án đúng hoặc việc thực hiện đúng một thủ tục chỉ cung cấp bằng chứng về phần năng lực mà task đó đo; riêng nó không đại diện đầy đủ cho hiểu khái niệm, giải thích, lựa chọn chiến lược hay transfer.

**Ý nghĩa đối với ZO Math:** ZO Math có cơ sở để tiếp tục coi “hiểu” là nhiều hơn việc tái hiện kết quả, nhưng không được phủ nhận giá trị của thủ tục, luyện tập hay độ chính xác.

### 3.2. Hiểu và thành thạo thủ tục có thể hỗ trợ lẫn nhau

ER-01 không hỗ trợ cách đối lập “hiểu” với “làm được”. Conceptual understanding và procedural fluency có thể phát triển tương hỗ.

**Ý nghĩa đối với ZO Math:** triết lí học liệu không nên biến thành một lựa chọn nhị nguyên giữa suy nghĩ và luyện tập; giữa kiến tạo ý nghĩa và thành thạo.

### 3.3. Suy lí và Kiến tạo ý nghĩa có nền chuyên môn phù hợp với Toán THPT

NCTM cung cấp nền chuyên môn trực tiếp cho việc xem reasoning và sense making là trọng tâm quan trọng trong Toán THPT.

**Ý nghĩa đối với ZO Math:** lựa chọn “Suy lí và Kiến tạo ý nghĩa” làm triết lí học liệu hiện tại có provenance chuyên môn rõ và không phải một thuật ngữ do ZO Math tự tạo. Tuy nhiên, ER-01 không chứng minh mọi sản phẩm gắn nhãn này đều hiệu quả.

### 3.4. Giải thích, biện minh, phản tư và tự kiểm tra có giá trị, nhưng không phải chỉ báo tuyệt đối

ER-01 hỗ trợ việc coi các hoạt động này là những cách quan sát thêm quá trình hiểu và suy nghĩ của người học.

**Ý nghĩa đối với ZO Math:** học liệu có thể tạo điều kiện cho người học giải thích, kiểm tra và phản tư, nhưng không được mặc định rằng chỉ cần xuất hiện các hoạt động ấy là đã tạo ra “hiểu sâu”.

## 4. Những claim phải thu hẹp

ZO Math chưa nên phát biểu như claim chung rằng:

- học sinh THPT thường học theo mẫu mà không hiểu;
- học sinh Việt Nam phổ biến thiếu suy lí, transfer hoặc tự kiểm tra;
- reasoning/sense making luôn hiệu quả hơn direct instruction, worked examples hay luyện tập;
- worked examples gây lệ thuộc hoặc ngược lại luôn hữu ích;
- metacognition tạo hiệu quả lớn và ổn định trong mọi bối cảnh;
- triết lí hoặc sản phẩm ZO Math đã được chứng minh là hiệu quả.

Những điều trên nếu cần phát biểu phải có nghiên cứu trực tiếp hơn về đối tượng, task và sản phẩm.

## 5. Những câu hỏi nên giữ mở

ER-01 không giải quyết:

- mức độ phổ biến của từng khó khăn ở học sinh THPT Việt Nam;
- cách kết hợp tối ưu worked examples, explicit instruction, practice và reflective prompts theo từng chủ đề;
- cách đo hợp lệ understanding, reasoning, transfer và self-monitoring;
- tác động thật sự của học liệu ZO Math;
- câu hỏi “học để tìm lại chính mình” trong kỉ nguyên AI.

Các câu hỏi này không phải blocker cho nghiên cứu Design System hiện tại.

## 6. Hệ quả cho nền tảng thương hiệu

### 6.1. ZO Math không nên định vị mình bằng sự đối lập với “cách học truyền thống”

External evidence không hỗ trợ một narrative đơn giản kiểu “hiểu tốt — luyện tập xấu” hay “suy lí tốt — hướng dẫn trực tiếp xấu”.

Vì vậy, brand language nên tránh giọng điệu phủ định hoặc đối đầu với luyện tập, thủ tục, worked examples hay hướng dẫn trực tiếp.

### 6.2. Nền tảng phù hợp hơn là “giữ ý nghĩa và hoạt động trí tuệ của người học”

Các bằng chứng phù hợp hơn với định hướng:

- không chỉ quan tâm sản phẩm cuối;
- quan tâm cách người học tạo nghĩa, lập luận, kiểm tra và sử dụng tri thức;
- đồng thời vẫn coi tính chính xác, thành thạo và luyện tập là thành phần có giá trị.

Điều này tương thích với tầng sâu mà chủ dự án đã xác nhận: giúp người học hình thành năng lực suy nghĩ và tự hiểu mình qua Toán học.

### 6.3. ZO Math phải giữ giọng điệu epistemically modest

Vì evidence phụ thuộc bối cảnh và không đồng đều, ZO Math không nên xây bản sắc bằng những lời hứa như “phương pháp này giúp hiểu sâu hơn”, “học như vậy chắc chắn hiệu quả hơn” hoặc “cách học cũ là sai”.

Ngôn ngữ thương hiệu nên phân biệt:

- điều ZO Math tin và theo đuổi;
- điều nghiên cứu bên ngoài hỗ trợ;
- điều sản phẩm ZO Math đã thực sự kiểm chứng.

## 7. Candidate constraints cho hệ thiết kế

Các mục sau là **candidate constraints**, chưa phải Principle hay Specification.

### DC-01 — Không tối ưu giao diện chỉ cho đáp án/kết quả cuối

Một sản phẩm ZO Math không nên mặc định rằng mục tiêu hiển thị duy nhất là đưa người học tới kết quả nhanh nhất.

**Hệ quả cần nghiên cứu ở R7/R10:** bố cục có thể cần dành không gian cho quá trình, liên hệ, giải thích, kiểm tra và thay đổi biểu diễn.

### DC-02 — Biểu diễn phải ưu tiên cấu trúc toán học hơn trang trí

Nếu hình, đồ thị, màu, motion hoặc layout che khuất quan hệ toán học, chúng đi ngược mục tiêu học tập.

**Hệ quả cần nghiên cứu ở R6:** distinction rõ giữa dữ liệu/toán học chính, phần hỗ trợ và decoration.

### DC-03 — Thiết kế không được dựa vào một kênh nhấn mạnh duy nhất

Thông tin quan trọng cần có nhiều cue khi cần: vị trí, nhãn, kiểu nét, cấu trúc, ngôn ngữ.

**Hệ quả cần nghiên cứu ở R4/R6:** semantic color không thay thế semantics của cấu trúc.

### DC-04 — Phải có chỗ cho kiểm tra và phản tư khi chức năng học tập yêu cầu

Không phải mọi trang/cảnh đều cần câu hỏi phản tư, nhưng khi mục tiêu là reasoning hoặc self-monitoring, UI/layout phải không cản trở hoạt động đó.

**Hệ quả cần nghiên cứu ở R7/R8:** khoảng dừng, sequencing, vùng ghi chú/so sánh, nhịp motion.

### DC-05 — Motion phải phục vụ reasoning, không chỉ tạo cảm giác hiện đại

Animation chỉ có giá trị khi giúp lộ quan hệ, biến đổi, thứ tự hoặc điểm cần chú ý.

**Hệ quả cần nghiên cứu ở R8:** motion grammar cần phân biệt explain/transform/compare/emphasize/pause với motion trang trí.

### DC-06 — Không ép mọi sản phẩm vào một “pedagogical look”

ER-01 cho thấy nhiều hình thức học tập có thể hữu ích tùy bối cảnh. Vì vậy, Design System không nên đồng nhất “đúng triết lí” với một hình thức thị giác duy nhất.

**Hệ quả cần nghiên cứu ở R10:** giữ shared meaning nhưng cho phép medium- và task-specific adaptation.

### DC-07 — Visual acceptance không thể thay learning validation

Một giao diện đẹp, đồ thị đúng style hay motion mượt không chứng minh học liệu giúp hiểu hơn.

**Hệ quả governance:** visual/design acceptance và learning-effect evidence phải là hai loại bằng chứng khác nhau.

## 8. Những candidate constraints chưa đủ để promote

Không promote DC-01 → DC-07 thành `PRIN-*` hoặc `DEC-*` ở bước này.

Chúng cần được kiểm tra tiếp trong R2, R4, R5, R6, R7, R8 và R10.

## 9. ER-02 có cần cho Design System ngay không?

**Kết luận P1.1e:** chưa cần mở ER-02 như một nhánh bắt buộc của Design System ngay bây giờ.

User research về nhu cầu, hành vi, segmentation, willingness to pay hoặc customer journey chủ yếu phục vụ product/market research.

Đối với Design System, ER-02 chỉ nên mở khi có một câu hỏi thiết kế cụ thể cần bằng chứng người dùng, ví dụ:

- học sinh đọc/hiểu layout nào tốt hơn;
- hệ nhãn/callout có gây nhầm không;
- subtitle/video có theo dõi được không;
- graph có đọc được trên mobile không;
- brand language có bị hiểu sai không.

Khi đó nghiên cứu người dùng nên được thiết kế như một experiment/validation có scope hẹp, thay vì một chương trình segmentation rộng.

## 10. ER-03 có cần cho Design System ngay không?

ER-03 về AI và học tập có giá trị đối với R1 và tầm nhìn dài hạn, nhưng chưa phải blocker cho việc nghiên cứu visual identity/design foundation.

Nó nên được mở khi:

- cần phát biểu claim cụ thể về tác động AI tới học tập;
- cần xây chính sách sản phẩm hoặc design pattern liên quan trực tiếp tới AI;
- hoặc cần nghiên cứu sâu hơn “Học để tìm lại chính mình”.

Không cần ER-03 trước khi bắt đầu R2/R6 và các chương trình thiết kế nền.

## 11. Cập nhật trạng thái R1 sau P1.1e

R1 hiện có:

- owner-confirmed positioning;
- owner-confirmed audience priority;
- owner-confirmed philosophy hiện tại;
- owner-confirmed AI context;
- external evidence đủ để kiểm tra tính hợp lý của các khái niệm trọng tâm;
- ranh giới rõ về những claim không nên nói quá.

Phần còn thiếu chủ yếu là:

- diễn đạt nền tảng thương hiệu ở dạng có thể dùng làm đầu vào cho R2;
- phân biệt rõ core statement, research direction và product-level goals;
- xác định điều nào nên được Tạm chấp nhận ở cấp nghiên cứu, chưa phải `Đã chốt`.

## 12. Đề xuất bước tiếp theo

Không mở ER-02 ngay.

Đề xuất:

**P1.1f — Tổng hợp R1 thành “Brand Foundation Candidate v0.1” có provenance**

Mục tiêu:

- kết tinh những owner-confirmed claims và external evidence thành một hồ sơ nền tảng;
- phân loại mỗi mệnh đề là core candidate, research direction, product priority hoặc open question;
- không viết marketing manifesto;
- không tạo Design Principle;
- trình chủ dự án duyệt từng mệnh đề trước khi bất kỳ nội dung nào được chuyển thành Decision.

Sau khi P1.1f được duyệt, R2 — Tính cách thương hiệu và cảm giác — có thể bắt đầu với một nền đủ chắc.

## 13. Kết luận giới hạn

P1.1e không chứng minh hiệu quả của ZO Math và không xây theory of mathematics education.

Giá trị chính của ER-01 đối với dự án Design System là:

1. củng cố tính hợp lý của một số quan tâm nền tảng;
2. giới hạn những claim ZO Math không nên nói quá;
3. chuyển một số phát hiện thành candidate constraints cho thiết kế;
4. xác định rằng user research rộng và AI research sâu chưa phải blocker của Design System;
5. cho phép R1 tiến tới bước tổng hợp nền tảng thương hiệu mà không cần tiếp tục mở rộng nghiên cứu giáo dục Toán.
