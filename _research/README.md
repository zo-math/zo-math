# ZO Math Research Memory

Đây là hệ thống trí nhớ nghiên cứu và trí nhớ thiết kế của ZO Math. Nó lưu có cấu trúc những tri thức có khả năng sống lâu, phát sinh tự nhiên trong quá trình xây dựng ZO Math, để ý tưởng, câu hỏi, nguồn đọc và lịch sử quyết định thiết kế không bị thất thoát.

Đây không phải nội dung xuất bản và không phải dự án luận án. Hệ thống này phục vụ sự trưởng thành của ZO Math, không thay thế dòng công việc sản xuất chính.

## Nguyên tắc

- Sản xuất ZO Math là dòng chính; nghiên cứu phát triển song song và bám theo thực hành.
- Không ghi mọi thứ. Chỉ lưu những điều có khả năng sống lâu và còn hữu ích sau nhiều tháng hoặc nhiều năm.
- Không dừng sáng tác, hoàn thiện hay xuất bản chỉ để theo đuổi ngay một câu hỏi mới nảy ra.
- Không biến linh cảm, diễn giải hoặc giả thuyết thành kết luận nghiên cứu.
- Trong source note (ghi chú nguồn), phải phân biệt rõ điều nguồn nói trực tiếp, diễn giải của ZO Math và giả thuyết của ZO Math.
- Ưu tiên thực hành trước mắt vẫn là phát triển khối kiến thức toán phổ thông, nhất là những mạch có giá trị thực tế và khả năng tạo nguồn thu nuôi dự án.

## Sơ đồ thư mục

- `00_inbox`: nơi ghi nhanh ý tưởng chưa phân loại.
- `10_questions`: các câu hỏi dài hạn đang được giữ và phát triển.
- `20_sources`: các source note (ghi chú nguồn), lưu điều ZO Math học được từ từng nguồn.
- `30_concepts`: các concept note (ghi chú khái niệm), lưu hiểu biết hiện hành về các khái niệm.
- `40_design_cases`: các design case (trường hợp thiết kế) thực tế có ý nghĩa giáo dục.
- `50_principles`: các principle (nguyên lí) đang hình thành từ thực hành và bằng chứng.
- `90_syntheses`: các synthesis (bản tổng hợp) tư tưởng theo thời điểm hoặc phạm vi.
- `_templates`: mẫu ngắn dùng khi tạo note mới.

## Quy trình sử dụng hằng ngày

1. Đang sản xuất mà nảy ra ý đáng giữ → ghi nhanh vào inbox.
2. Không dừng công việc chính để nghiên cứu ngay.
3. Khi có thời gian, phân loại note.
4. Nếu là câu hỏi sống lâu → đưa sang `10_questions`.
5. Nếu xuất phát từ nguồn → tạo source note (ghi chú nguồn).
6. Nếu là thay đổi thiết kế giáo dục quan trọng → tạo design case (trường hợp thiết kế).
7. Chỉ khi một mẫu lặp lại nhiều lần và có cơ sở mới tạo principle (nguyên lí).
8. Định kỳ viết synthesis (bản tổng hợp).

## Nếu quay lại sau một thời gian dài

1. Đọc `_research/README.md`.
2. Mở synthesis (bản tổng hợp) mới nhất trong `90_syntheses`.
3. Xem các câu hỏi đang hoạt động trong `10_questions`.
4. Xem inbox còn gì chưa xử lí.
5. Sau đó quay lại công việc sản xuất chính của ZO Math.

> Không cần nhớ toàn bộ hệ thống. README là nơi để nhớ thay cho con người.

## Luồng phát triển và liên kết

Một ý tưởng từ inbox có thể phát triển thành question, source note (ghi chú nguồn), concept note (ghi chú khái niệm) hoặc design case (trường hợp thiết kế). Qua thời gian, nhiều nguồn, khái niệm và design case có thể cùng góp phần hình thành một principle (nguyên lí).

Synthesis (bản tổng hợp) không phải cấp cao hơn principle, mà là hoạt động định kỳ để nhìn lại mạng lưới tri thức, nhận ra thay đổi, mối liên hệ và những điều đang nổi lên. Không phải note nào cũng phải phát triển sang loại khác.

inbox
↓
question / source / concept / design case
↓
principle
↓
synthesis

## Truy xuất bằng AI

Sau này có thể yêu cầu ChatGPT, Codex hoặc Copilot:

- tìm mọi design case (trường hợp thiết kế) liên quan đến một khái niệm;
- truy lịch sử thay đổi của một quan niệm;
- tìm nguồn hỗ trợ hoặc phản bác một nguyên lí;
- tổng hợp các pattern đang nổi lên.
- Quy trình giao việc cho Codex: [`CODEX_WORKFLOW.md`](CODEX_WORKFLOW.md).

Vì vậy, mỗi file cần có tiêu đề rõ và liên kết tới các ID liên quan khi có thể. Khi bổ sung hoặc sửa note, giữ nguyên ranh giới giữa lời của nguồn, diễn giải của ZO Math và giả thuyết của ZO Math để kết quả truy xuất không làm sai cấp độ bằng chứng.

## Đạo đức nghiên cứu

Không mặc nhiên coi dữ liệu cá nhân của học sinh hoặc người dùng thu được trong vận hành thông thường là “dữ liệu luận án”. Nếu sau này tiến hành nghiên cứu trên người tham gia, phải có thiết kế nghiên cứu và quy trình đạo đức phù hợp.
