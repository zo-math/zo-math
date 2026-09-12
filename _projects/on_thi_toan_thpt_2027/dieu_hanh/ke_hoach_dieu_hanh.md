# ZO Math — Ôn thi Toán THPT

## Kế hoạch thực hiện · Ấn bản ôn thi 2027

- **Phiên bản:** 0.6 — kế hoạch điều hành đầy đủ; kiến trúc bốn lớp, lộ trình thích ứng và hồ sơ căn cứ A/B/C; kế thừa bản nền canonical 0.5.
- **Ngày cập nhật:** 11/09/2026.
- **Chủ trì:** người sáng lập ZO Math.
- **Mục tiêu điều phối:** giúp học sinh ôn thi theo các mạch kiến thức liên kết, nhận diện thiếu hụt, ôn lại, luyện tổng hợp, luyện đề và sửa lỗi.
- **Quy mô thiết kế:** CT → CD01–CD15 → B01–B42; tám mạch R1–R8 và nền N; 36 tuần × khoảng 6 giờ/tuần là lộ trình tham chiếu đầy đủ. Lịch cá nhân tính từ mốc thi, ngày gia nhập, D0, tiến độ trường và quỹ giờ thực.
- **Căn cứ:** chương trình môn Toán, sáu SGK Kết nối tri thức đã cung cấp, quy chế hợp nhất 2026 và các nguồn đề thi đã đối chiếu. Chấp nhận các bản sách ghi “Bản mẫu”.
- **Cách tạo học liệu:** người chủ trì nghiên cứu từ nguồn với Notebook, thực hành và trao đổi; kết tinh nội dung; sản xuất, kiểm định, đóng gói và công bố theo phạm vi được giao.
- **Trạng thái:** D0 — khảo sát đầu vào — đã hoàn tất v1.0 và có trong Nguồn.
- **Việc triển khai kế tiếp duy nhất sau khi khóa 0.6:** chuẩn bị bộ nguồn và ma trận mục tiêu cho phiên nghiên cứu đầu tiên của R1-G01 — kết nối đạo hàm, bảng biến thiên và đồ thị (15.5).

**Bản 0.6 thay thế đầy đủ bản 0.5 trong điều hành dự án; 0.5 là bản nền canonical đã dùng để audit và kế thừa.** Mọi quyết định đang áp dụng, bảng lộ trình, chỉ mục kiến thức, quy trình, biểu mẫu và kết quả đánh giá nguồn cần dùng đã nằm trong tệp này. Không cần đọc kèm bản cũ hay báo cáo đánh giá tám tài liệu. Các bản nguồn và thành phẩm đã kiểm định vẫn được giữ để tra cứu và truy nguyên.

Kế hoạch đã hoàn thành ở mức thiết kế và điều phối; các gói học liệu, notebook và trang công bố sẽ được tạo theo thứ tự trong kế hoạch. Thời lượng ôn của học sinh không phải định mức lao động của người chủ trì. Các giả thiết thiết kế và các thông tin kỳ thi cần cập nhật được tập trung tại mục 12 và 15, thay vì biến thành điều kiện chờ ở mọi chặng.

## 0. Cách dùng kế hoạch

**Để thấy kiến trúc, đọc 2.5 → 4.2/4.5–4.6; để lập lịch, dùng 12.10 trước rồi đối chiếu mẫu 12.2. Để tiếp tục nội dung, dùng 15.5 và D.14 cho R1-G01.** Audit 0.5 ở F.1; căn cứ nghiên cứu ở 3.13; sổ rà CT ở H. Các phần còn lại phục vụ tra cứu và thực hiện đúng công việc đang làm.

| Cần quyết định | Nơi tra trong chính tài liệu này | Kết quả phải đưa ra |
| --- | --- | --- |
| Tổ chức kiến thức và lịch học thế nào? | 2.5; 4.2/4.5–4.6; 12.10–12.13 | Phân biệt bản đồ/mạch/lịch/định dạng; lập lịch theo người học |
| Học sinh cần sửa gì và khi nào tiến tiếp? | 5.2–5.4; 12.5; 12.9 | Tối đa hai ưu tiên sửa, câu kiểm tra lại và lượt tiếp theo |
| Làm học liệu gì tiếp? | 11; 12.7; 15.5 | D0 đã hoàn tất; chuẩn bị nguồn/ma trận R1-G01 |
| Nguồn và phạm vi toán nằm ở đâu? | 3–4; phụ lục A–C | Đúng yêu cầu, cụm kiến thức và trang nguồn cần đọc |
| Nghiên cứu với Notebook thế nào? | 6–7; D.1–D.4 | Phiên học có câu hỏi, nguồn, bài làm và bản kết tinh |
| Tạo, sửa và lưu sản phẩm thế nào? | 8–10; D.5–D.15 | Thành phẩm đã kiểm tra và hồ sơ đúng phiên bản |
| Tích hợp website, xuất bản và tự động hóa thế nào? | 13–14; D.16 | Gói cụ thể, phạm vi công bố và đầu ra đã kiểm tra |
| Tiếp tục sau gián đoạn hoặc sang mùa sau? | 15–16; D.7; D.9 | Tiếp tục từ tệp mới nhất và một việc kế tiếp |

Mỗi tuần vận hành: mở lịch cá nhân hiện hành (12.10–12.13), đối chiếu hàng tham chiếu 12.2 khi cần; đọc kết quả trước đó; chọn trọng tâm và hai điểm yếu; giao bài ôn; cuối tuần quyết định tiến tiếp hoặc bổ sung. Người chủ trì không phải đọc lại toàn bộ tài liệu hay tự tạo một hệ biểu mẫu trống để bắt đầu.

### 0.1. Nguyên tắc thay thế đầy đủ

Mỗi lần hiệu chỉnh giữ mọi nội dung còn đúng và có ích; sửa chỗ sai hoặc lỗi thời; tích hợp quyết định mới ngay tại nơi áp dụng; rà các tham chiếu, mã và trạng thái. Chỉ rút gọn khi vẫn giữ đầy đủ ý nghĩa và khả năng làm theo. Nhật ký tại mục 15 và phụ lục F giúp tra việc sửa, không thay cho nội dung hiện hành.

Kế hoạch này tổ chức chương trình ôn thi. Quá trình học sâu của người chủ trì là cách tạo học liệu tốt cho chương trình ấy. Một phiên Notebook có thể nghiên cứu một ý rất nhỏ; đơn vị giao cho học sinh vẫn phải gắn với nhiệm vụ ôn và vị trí trong lộ trình.

### 0.2. Mục lục toàn tài liệu

| Mục | Nội dung |
| --- | --- |
| 1 | Mục tiêu ôn thi, đối tượng, nguyên tắc và quá trình sáng tạo |
| 2 | Đơn vị công việc, hệ mã, trách nhiệm và điều phối |
| 3 | Nguồn, phạm vi kiểm chứng và căn cứ đề thi |
| 4 | Tám mạch ôn, bản đồ R–B và các nhóm kiến thức |
| 5 | Ma trận yêu cầu, câu hỏi, đầu vào và quyết định tiến tiếp |
| 6 | Notebook theo gói ôn, thử đọc nguồn và quản lý thay đổi |
| 7 | Nghiên cứu, kết tinh, ghi hình và tiếp tục sau gián đoạn |
| 8 | Hệ học liệu, Studio và trải nghiệm học sinh |
| 9 | Kiểm định, phản hồi, sửa lỗi và điều kiện đóng gói |
| 10 | Hồ sơ, phiên bản, nơi lưu và đóng gói |
| 11 | D0 đã hoàn tất, R1-G01 và mốc sản xuất tiếp nối |
| 12 | Mẫu 36 tuần, lịch thích ứng theo ngày gia nhập, cập nhật thi và lịch sản xuất |
| 13 | Tái sử dụng, tích hợp website và phân phối nhiều kênh |
| 14 | Tự động hóa đóng gói từ bộ đã duyệt |
| 15 | Quyết định hiện hành, kết quả và điểm bàn giao |
| 16 | Kho lâu dài, ấn bản hằng năm và giá trị sản phẩm |
| Phụ lục A | Chỉ mục 24 chương/79 bài, hoạt động trải nghiệm và vị trí ôn |
| Phụ lục B | B01–B42: mục tiêu, nguồn và kiến thức cần trước |
| Phụ lục C | Chín chuyên đề học tập và ranh giới với phần chung |
| Phụ lục D | Chỉ dẫn, prompt và biểu mẫu triển khai |
| Phụ lục E | Tệp nguồn, tham chiếu và đối chiếu đề thực tế |
| Phụ lục F | Audit toàn 0.5, sổ quyết định, tác động và changelog 0.5 → 0.6 |
| Phụ lục G | Đề cương B04–B06 được giữ để bổ sung nền theo nhu cầu |
| Phụ lục H | Sổ rà CT theo nhóm yêu cầu, thực hành, mục tiêu cần làm rõ và giới hạn |

## 1. Mục tiêu và nguyên tắc của chương trình

### 1.1. Kết quả của chương trình

1. **Học sinh ôn thi có định hướng:** biết mình đang ở đâu, cần củng cố gì, tự chọn công cụ trong bài phối hợp, làm đề trong thời gian quy định và sửa lỗi bằng bài mới.
2. **ZO Math có hệ học liệu phục vụ lộ trình:** bài ôn, bài luyện, lời giải, đánh giá, chỉ dẫn quay lại nền và các sản phẩm hỗ trợ có mục đích.
3. **Người sáng lập hiểu toán và thiết kế học liệu sâu hơn:** tự giải thích khái niệm, điều kiện, mối liên hệ và các điểm người học có thể vướng. Kết quả nghiên cứu này được đưa vào học liệu và nội dung quá trình sáng tạo.

Đo tiến bộ bằng bài làm, khả năng giải thích, lỗi đã sửa, việc vận dụng và công sức thực tế. Số notebook, số video hoặc số trang chỉ là dữ liệu sản xuất. Một học sinh đã vững phần nền được vào thẳng nhiệm vụ ôn tương ứng; không buộc học lại lần lượt mọi bài SGK.

### 1.2. Tên, đối tượng và phạm vi

Tên lâu dài là **ZO Math — Ôn thi Toán THPT**; ấn bản đầu là **Lộ trình ôn thi 2027**. Hướng đến học sinh có nhiều nền tảng và mục tiêu, không đóng khung vào một nhóm điểm số. Lịch khởi điểm được thiết kế cho học sinh đang học lớp 12, đã tiếp cận lớp 10–11; nội dung chưa học được ghi riêng và điều chỉnh theo 12.10–12.13; 12.2 là lịch tham chiếu.

Phần kiến thức chung của lớp 10–12 là nền bao quát. Trong đó, lộ trình ôn thi lựa chọn thứ tự và mức luyện theo yêu cầu đánh giá đã kiểm chứng. Chuyên đề học tập, củng cố THCS và mở rộng được nhận diện riêng để không nhầm với yêu cầu chung. Không đồng nhất chương trình này với mọi kỳ thi tuyển sinh riêng của các trường đại học.

### 1.3. Nguồn làm nền; người sáng lập quyết định cách dạy

Chương trình môn Toán xác định nội dung và yêu cầu cần đạt. SGK giúp nghiên cứu cách giới thiệu, trình tự, ví dụ và hoạt động. Nguồn thi chính thức giúp xác định yêu cầu đánh giá của kỳ thi tương ứng. ZO Math quyết định cách kết nối, giải thích, xây bài tập và tổ chức việc tự học.

Giữ định hướng **suy lí và kiến tạo ý nghĩa** bằng những nhiệm vụ thực: giải thích vì sao, kiểm tra điều kiện, nối công thức với bảng và hình, thử phản ví dụ, đánh giá lời giải. Không gắn tên NCTM vào một quy trình do chúng ta tự thiết kế nếu chưa có đoạn nguồn xác nhận.

### 1.4. Quá trình sáng tạo là một lớp nội dung riêng

Video quá trình cho thấy cách đọc nguồn, nảy sinh câu hỏi, tự giải bài, phát hiện lỗi và sửa cách giải thích. Học sinh vẫn phải tự học được bằng bộ học liệu hoàn chỉnh khi chưa xem video ấy.

Ghi lại những phần có ích trong lúc học; không biến toàn bộ phiên làm việc thành một buổi biểu diễn. Khi trình bày lại điều đã nghiên cứu, nói rõ đó là phần trình bày lại. Bản ghi thô được chọn lọc, bỏ thời gian chờ và thao tác tệp không phục vụ nội dung. Video quá trình và video giải thích do Studio tạo là hai loại sản phẩm khác nhau.

### 1.5. Kho lâu dài và ấn bản năm

Kho lâu dài giữ khái niệm, lập luận, hình, bài tập, lời giải, nguồn và lịch sử sửa. Ấn bản 2027 giữ thứ tự học, lựa chọn bài, đề luyện, căn cứ thi và các liên kết đã công bố. Mùa sau kế thừa nội dung tốt và sửa những điểm cần sửa, đồng thời bảo toàn lịch sử mùa trước.

## 2. Đơn vị công việc và trách nhiệm

### 2.1. Không đồng nhất các đơn vị

| Đơn vị | Ý nghĩa |
| --- | --- |
| Chương, bài SGK | Đơn vị tổ chức trong đúng bản sách dùng để tra cứu |
| Nhóm chuyên đề ZO Math | Cách nhóm kiến thức để điều phối; có thể nối các lớp |
| Cụm nội dung Bxx | Mã kiến thức ổn định để tra nguồn và tái sử dụng; một cụm không mặc định là một gói ôn |
| Mạch ôn R1–R8 | Đơn vị điều phối mục tiêu ôn thi, phối hợp nhiều cụm Bxx; nền bổ sung ký hiệu N |
| Gói R1-G01, R3-G01… | Một đơn vị học liệu có mục tiêu và vị trí sử dụng; G01 là số gói trong mạch |
| Bộ D0 | Khảo sát đầu vào và hồ sơ định vị theo các mạch; không phải một chuyên đề kiến thức |
| Phiên học của người chủ trì | Một lần trích xuất, đọc, thực hành, trao đổi hoặc tổng hợp; một cụm có thể cần nhiều phiên |
| Bộ học liệu đã đóng gói | Tập sản phẩm đã kiểm tra, cùng phục vụ mục tiêu xác định và cùng phiên bản nội dung |
| Sản phẩm | Bài đọc, phiếu, lời giải, sơ đồ, slide, âm thanh, video, thẻ nhớ hoặc bài kiểm tra |
| Phiên tự học của học sinh | Một phần của lộ trình phù hợp kiến thức hiện có của em |

Một chương không nhất thiết bằng một bộ; một bộ không bằng một notebook hay một video. Nếu một cụm quá rộng, chia thành bài nhỏ có mục tiêu và kiểm tra độc lập trước khi quyết định cách đóng gói.

### 2.2. Phân công

| Bên thực hiện | Trách nhiệm chính |
| --- | --- |
| Người chủ trì | Học, tự giải bài, đặt câu hỏi, quyết định cách diễn giải và duyệt bản sẽ xuất bản |
| Gemini Notebook | Trích xuất và tổ chức bài học từ nguồn; hỗ trợ trao đổi; tổng hợp; tạo sản phẩm Studio theo đầu vào đã xác định |
| ChatGPT | Chuẩn bị kế hoạch, đối chiếu nguồn, thiết kế câu hỏi nghiên cứu; đọc sản phẩm người dùng gửi, kiểm tra và sửa trực tiếp khi có thể; viết yêu cầu sửa đưa về Notebook khi cần |
| Công cụ toán và công cụ dàn trang | Hỗ trợ tính toán, dựng hình và tạo thành phẩm; kết quả vẫn cần đối chiếu với lập luận và mục tiêu |
| Tác tử có quyền truy cập repo | Thực hiện phần tích hợp website khi cần môi trường repo; bám quy chuẩn hiện có |

ChatGPT làm những việc đọc, tổng hợp và biên tập có thể tự làm. Chỉ yêu cầu người chủ trì thao tác ở nơi ChatGPT chưa truy cập được. Mỗi lần hướng dẫn thực hiện một bước rõ ràng. Không tạo thêm đội tác tử để xử lý công việc văn bản thông thường.

### 2.3. Điều phối và đầu ra của từng bên

Kế hoạch và hồ sơ Markdown bên ngoài Notebook giữ quyết định chính thức của dự án. Sổ ghi chú hỗ trợ học và tạo sản phẩm; trạng thái trong sổ phải được chuyển vào hồ sơ khi kết thúc việc. ChatGPT chuẩn bị và cập nhật hồ sơ, người chủ trì xem các quyết định ảnh hưởng nội dung và cách công bố.

| Công việc | Người hoặc công cụ thực hiện | Đầu ra để xem lại |
| --- | --- | --- |
| Định vị và đối chiếu nguồn | ChatGPT đọc phần truy cập được; người chủ trì cung cấp đúng phần còn thiếu khi cần | Hồ sơ đến trang/mục, mức kiểm tra và điểm thiếu |
| Chuẩn bị phiên học | ChatGPT soạn phạm vi và yêu cầu trích xuất; người chủ trì đưa vào Notebook | Phiếu giao việc có mục tiêu và nguồn |
| Trích xuất và nghiên cứu | Notebook trích xuất; người chủ trì đọc, tự làm và trao đổi | Bài học để đọc, bài làm, câu hỏi và phát hiện |
| Kết tinh | Notebook hỗ trợ tổng hợp; người chủ trì và ChatGPT kiểm tra, sửa | Bản nội dung có điều kiện, nguồn và phiên bản |
| Thiết kế cho học sinh | ChatGPT chuẩn bị mạch tự học và câu hỏi từ nội dung đã làm rõ; người chủ trì chỉnh cách dạy | Bài tự học, nhiệm vụ, lời giải và đường học tiếp |
| Tạo sản phẩm Studio | Người chủ trì thao tác trong sổ; ChatGPT chuẩn bị đầu vào và yêu cầu sửa | Đúng sản phẩm đã chọn, ghi bản nguồn đã dùng |
| Kiểm định và đóng gói | ChatGPT kiểm tra phần đọc được và sửa; người chủ trì xem thành phẩm thực tế | Báo cáo lỗi, bản sửa và gói chờ duyệt |
| Tích hợp và công bố | Tác tử có quyền làm trong repo thực hiện theo quy trình; người chủ trì duyệt phạm vi | Bản xem trước, kết quả kiểm tra, URL sau khi công bố |
| Theo dõi và hiệu chỉnh | ChatGPT tổng hợp dữ liệu thực tế; người chủ trì quyết định nhịp tiếp theo | Tiến độ, số giờ, phản hồi và một việc kế tiếp |

Mối liên hệ cần giữ là: yêu cầu chương trình → mục tiêu ôn của mạch R → cụm kiến thức B cần dùng → nhiệm vụ kiểm tra → gói học liệu → phiên bản công bố. Một yêu cầu có thể đi qua nhiều bài, và một bài có thể đáp ứng nhiều yêu cầu. Khi thay một thành phần, dùng các mã này để tìm phần liên quan, tránh sửa rời rạc.

### 2.4. Quy ước mã để không lẫn lộ trình với kho kiến thức

CD01–CD15 phân nhóm để tra kho; B01–B41 chỉ phạm vi toán và B42 lưu nhiệm vụ tổng hợp. R1–R8 điều phối các mạch ôn; N là nền gọi vào. D0 là bộ khảo sát; R1-G01 là gói đầu tiên của R1. Chặng A–E và các hàng B.1–B.9 ở mục 12.2 chỉ vị trí trong lịch, không phải mã B01–B09 của kiến thức.

Ví dụ R1-G01 dùng B04, B06, B16–B18 và phần B21 phù hợp; một câu trong gói có thể được dùng lại ở B42 khi luyện tổng hợp. Hồ sơ câu giữ mã gốc, mạch chính, mạch hỗ trợ và danh sách gói sử dụng. Một câu nhiều mạch chỉ được tính một lần khi cộng số câu.

Không đánh số lại kho B để khớp thứ tự ôn. Khi tách hoặc ghép gói, ghi ánh xạ thay đổi, giữ nguồn và lịch sử của câu. Phụ lục B là nơi tra chi tiết kiến thức; bảng 4.6 nối trực tiếp kho đó với lộ trình.

### 2.5. Kiến trúc bốn lớp và đường truy nguyên

**Quyết định C-01 của ZO Math:** quản lý bốn lớp riêng nhưng liên kết bằng mã. CT ở đây là **Chương trình GDPT môn Toán**, không phải một hệ mã chủ đề mới. CD01–CD15 là nhóm do ZO Math đặt; không đồng nhất CD với chín chuyên đề học tập chính thức. Quan hệ CT → CD → B là đường tổ chức và truy nguyên phạm vi, không phải quan hệ một–một hay thứ tự học.

| Lớp | Câu hỏi điều hành | Thành phần | Điều làm lớp này thay đổi |
| --- | --- | --- | --- |
| 1. Bản đồ kiến thức/phạm vi | Cần học những gì, từ yêu cầu nào? | CT → CD01–CD15 → B01–B42; yêu cầu cụ thể, phạm vi, nguồn, tiên quyết | Sửa chương trình; phát hiện thiếu/sai ánh xạ; chia nhỏ mục tiêu |
| 2. Mạch ôn | Kết nối kiến thức để thực hiện nhiệm vụ nào? | R1–R8, nền N, gói G; một B có thể phục vụ nhiều R | Thay cách kết nối hoặc đóng gói vì mục tiêu học; không đổi theo số câu đề |
| 3. Lộ trình học thích ứng | Ai học gì, khi nào, quay lại ra sao? | D0, phần đã học ở trường, bằng chứng từng mục tiêu, quỹ giờ, mốc thi, lịch cá nhân | Học sinh gia nhập; tiến độ học, kết quả, nguồn lực hoặc lịch thi đổi |
| 4. Định dạng kỳ thi | Thể hiện và đánh giá năng lực trong quy cách nào? | Cấu hình đề, dạng trả lời, chấm điểm, thời gian, phương tiện, thao tác và đề mô phỏng | Văn bản/định dạng/hướng dẫn áp dụng thay đổi |

Luồng truy nguyên của một nhiệm vụ: **yêu cầu CT → mục tiêu B → R chính/hỗ trợ → gói → câu hỏi và lời giải → lượt học/đánh giá → kết quả và quyết định**. Khi dùng làm đề mô phỏng, gắn thêm mã cấu hình kỳ thi. Phiếu học toán có thể dùng tự luận, giải thích, dựng hình hoặc phản biện dù đề thi chỉ chấm đáp số.

Không gọi R là toàn bộ “trục nội dung”. B42 là hồ sơ nhiệm vụ tổng hợp; B02 là nền củng cố, không phải hai vùng kiến thức chung mới do Bộ quy định. R8 tổ chức mô hình hóa và phối hợp từ đầu; không hút toàn bộ thực hành, công cụ, giao tiếp và lập luận ra khỏi R1–R7.

Ví dụ: mục tiêu nhận biết cực trị từ bảng biến thiên thuộc CT tr.105–106, CD07/B18, được ôn trong R1-G01. Học sinh có thể giải thích bằng lời rồi kiểm tra lại bằng hình mới. Chỉ khi đưa câu vào đề mô phỏng mới chọn quy cách đúng/sai, điểm và thời gian theo cấu hình ở 3.14. Đổi cách chấm không làm định nghĩa cực trị thay đổi.

## 3. Căn cứ và mức kiểm chứng

### 3.1. Bộ nguồn đang dùng

Mã trong bảng là mã nội bộ của kế hoạch này. “Trang PDF” được đếm từ 1; “trang in” là số hiện trên sách. Các trang mục lục đã được xem trực tiếp bằng hình.

| Mã | Tài liệu | Số trang PDF | Phiên bản nhìn thấy | Vị trí đã dùng để kiểm kê |
| --- | --- | ---: | --- | --- |
| CT | Chương trình GDPT môn Toán 2018 | 123 | Kèm Thông tư 32/2018/TT-BGDĐT, 26/12/2018 | Phần THPT tr.79–114; phương pháp, đánh giá tr.115–117 |
| S10.1 | Toán 10, tập một — KNTT | 106 | Tái bản lần thứ tư | Mục lục tr.in 4 = PDF 5 |
| S10.2 | Toán 10, tập hai — KNTT | 102 | Tái bản lần thứ tư | Mục lục tr.in 3 = PDF 4; đã xem nội dung Bài 15 và trang cuối thuật ngữ |
| S11.1 | Toán 11, tập một — KNTT | 134 | Bản mẫu | Mục lục tr.in 4 = PDF 5 |
| S11.2 | Toán 11, tập hai — KNTT | 114 | Bản mẫu | Mục lục tr.in 3 = PDF 4 |
| S12.1 | Toán 12, tập một — KNTT | 104 | Bản mẫu | Mục lục tr.in 4 = PDF 6 |
| S12.2 | Toán 12, tập hai — KNTT | 99 | Bản mẫu | Mục lục tr.in 3 = PDF 5 |

**Quyết định đã thống nhất:** dùng các bản mẫu hiện có để tiếp tục. Khi gặp một chỗ mâu thuẫn có ảnh hưởng, đối chiếu đúng chỗ ấy với chương trình và nguồn bổ sung; không trì hoãn toàn kế hoạch chỉ vì nhãn bản mẫu.

Tệp S10.2 hiện tại là SGK, khác tệp sách bài tập 143 trang đã bị đặt tên tương tự ở lần gửi trước. Không dùng nhầm tệp sách bài tập làm chỉ mục SGK.

### 3.2. Những con số đã xác nhận và những con số thiết kế

| Con số | Kết luận đang sử dụng |
| --- | --- |
| 6 tập SGK | Đã có đúng hai tập mỗi lớp 10, 11, 12 |
| 24 chương | Đã đếm trực tiếp: lớp 10 có 9, lớp 11 có 9, lớp 12 có 6 |
| 79 bài được đánh số | Đã đếm theo mục lục: 27 + 33 + 19; không tính bài tập cuối chương, ôn cuối năm, hoạt động thực hành và trải nghiệm |
| 9 chuyên đề học tập lớp 10–12 trong bản chương trình 2018 | Ba chuyên đề mỗi lớp; kiểm kê riêng ở phụ lục C, không nằm trong 24 chương trên |
| 15 nhóm chuyên đề ZO Math | Cách nhóm nội bộ: 14 nhóm nội dung và 1 nhóm kết nối xuyên suốt; không phải số chuyên đề chính thức |
| 42 mã B01–B42 | Danh mục quản lý gồm: 41 cụm nội dung dự kiến và hồ sơ tổng hợp B42; chưa chốt là 42 bộ thành phẩm |

24 chương và 79 bài là số đếm của **các bản sách đang dùng**, không phải số lượng đơn vị kiến thức tối thiểu do Bộ quy định. Một bài có thể chứa nhiều yêu cầu cần đạt. Số lượng bộ học liệu chỉ được chốt sau khi chia mục tiêu, thử biên soạn và rà khả năng tự học.

### 3.3. Phần chương trình đã đọc và giới hạn kết luận

0.5 đã đọc phần chương trình lớp 10–12 để xác định nhóm nội dung và đối chiếu cấp chương/bài với sáu mục lục. Đợt 0.6 rà lại có hệ thống phần chung theo trang/đề mục và ghi kết quả tại H. Phụ lục B ghép các cụm với trang chương trình và bài SGK. Đây là **ma trận ở cấp cụm**; H bổ sung cấp nhóm yêu cầu. Chưa đủ căn cứ tuyên bố đã kiểm chứng 100% từng yêu cầu cần đạt hoặc tất cả câu chữ, công thức và bài tập trong sáu cuốn sách.

Trước khi sản xuất một cụm, ChatGPT lập hàng đối chiếu cho từng yêu cầu liên quan: nguồn, trang, nội dung diễn giải, nhiệm vụ kiểm tra, bài học đáp ứng và trạng thái. Các công thức bị lỗi khi trích chữ phải được đọc lại ở hình trang gốc. Không gọi bản trích chữ tự động là bản chuẩn toán học.

### 3.4. Văn bản bổ sung và căn cứ thi

| Nguồn và ngày kiểm tra | Kết quả sử dụng |
| --- | --- |
| Thông tư 17/2025/TT-BGDĐT | Đã mở trang Chính phủ và phần quy định phạm vi sửa đổi trong PDF: Lịch sử và Địa lí, Lịch sử, Địa lí, Giáo dục công dân; không có mục sửa chương trình môn Toán trong danh sách ấy. Không gọi đây là một “chương trình Toán 2025” mới. [Nguồn](https://vanban.chinhphu.vn/?docid=215347&pageid=27160) |
| Thông tư 13/2022/TT-BGDĐT | Lần trước đã đọc bản chữ đăng lại và định vị bản PDF tại trường Tân Túc. Bản chữ thứ sinh chỉ còn là dấu vết tra cứu, không thuộc nguồn căn cứ hiện hành. Chưa đối chiếu toàn bộ bản scan; không dùng thông tin ấy để sửa các yêu cầu toán trong CT. [Toàn văn đã đọc](https://thuvienphapluat.vn/van-ban/Giao-duc/Thong-tu-13-2022-TT-BGDDT-sua-doi-Thong-tu-32-2018-TT-BGDDT-Chuong-trinh-giao-duc-524666.aspx) |
| Thông tư 20/2021/TT-BGDĐT | Đã định vị trang công bố và PDF gốc; bản PDF không có chữ trích xuất trong công cụ web. Giữ trong hồ sơ cần đối chiếu khi hoàn thiện lịch sử văn bản. [Nguồn](https://vanban.chinhphu.vn/default.aspx?docid=203766&pageid=27160) |
| Công bố định dạng thi từ 2025, ngày 29/12/2023 | Đã đọc trang Cục QLCL. Dùng làm căn cứ lịch sử cho ba dạng câu hỏi và thời gian Toán 90 phút; trang công bố có lưu ý khả năng điều chỉnh. Không suy thành định dạng đã chốt của 2027. [Nguồn](https://vqa.moet.gov.vn/vi/news/thong-bao/cau-truc-dinh-dang-de-thi-tot-nghiep-thpt-tu-nam-2025-74.html) |
| Thông tin đề án thi trên máy tính, ngày 29/07/2026 | Đã đọc: bài viết mô tả lộ trình đề xuất, dự kiến từ 2027 tại một số điểm đủ điều kiện. Không diễn giải thành áp dụng đại trà đã có hiệu lực. [Nguồn](https://vqa.moet.gov.vn/vi/news/tin-tuc-su-kien/bo-gddt-noi-gi-ve-de-an-to-chuc-thi-tot-nghiep-thpt-tren-may-tinh-286.html) |
| Quy chế hợp nhất 2026 — kiểm tra 09/09/2026 | Đã đọc Điều 4–5: phạm vi THPT, chủ yếu lớp 12; bám yêu cầu cần đạt. [Bản hợp nhất, tr.2](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/4/02-vbhn-bgddt-kem.pdf) |
| Đề năm 2025 và 2026 — kiểm tra 09/09/2026 | Đã đọc trực tiếp toàn bộ bốn trang của mã 0101 mỗi năm, qua bản đề được lưu lại. Có đối chiếu nhiệm vụ ở phụ lục E.4; không suy ra tỉ trọng cố định cho năm 2027. |
| Đáp án Toán 2026 — kiểm tra 09/09/2026 | Đã xem tệp đáp án Bộ công bố do Cổng TTĐT Chính phủ đăng lại. Phần giải thích trên trang lưu đề không được dùng như đáp án Bộ. Hồ sơ 0.5 ghi bản lưu 2025 khi đó có bảng đáp án tại trang PDF 17; tệp 2025 được cung cấp trong đợt này chỉ có 16 trang đề, nên không dùng tham chiếu ấy cho tệp hiện tại. Theo quy tắc hiện hành, các bảng đáp án ngoài không được nạp vào nguồn nghiên cứu mặc định và không phải điều kiện để bắt đầu; ZO Math tự giải và kiểm chứng theo 9.9. [Nguồn công bố](https://xaydungchinhsach.chinhphu.vn/thi-tot-nghiep-thpt-2026-de-thi-mon-toan-vua-suc-co-tinh-phan-hoa-ro-ret-119260611164121523.htm) |
| Hướng dẫn quản lý chất lượng 2026–2027 — kiểm tra 09/09/2026 | Có yêu cầu chuẩn bị thí điểm thi trên máy tính từ 2027; không phải áp dụng đại trà. [Nguồn Cục QLCL](https://vqa.moet.gov.vn/vi/news/tin-tuc-su-kien/bo-gddt-huong-dan-thuc-hien-nhiem-vu-quan-ly-chat-luong-nam-hoc-2026-2027-294.html) |

Kết quả trên là phạm vi kiểm tra cụ thể, chưa phải chứng nhận đã rà hết mọi văn bản đang áp dụng. Phần kế hoạch học kiến thức có thể triển khai trên nguồn đã có; phần quy cách đề thi và lịch thi được cập nhật từ văn bản của kỳ thi tương ứng. Không ấn định tỷ trọng câu theo lớp hoặc lịch thi 2027. Cấu trúc và cách chấm đang dùng đã được đối chiếu tại mục 3.10; cập nhật phần có thay đổi khi có hướng dẫn áp dụng cho 2027.

KNTT được dùng vì người chủ trì đã cung cấp đủ bộ và chọn làm trục tra cứu. Không cần dựa vào một tuyên bố về thống nhất SGK toàn quốc để biện minh cho lựa chọn này.

### 3.5. Có cần bổ sung sách ngay không?

**Không cần thêm sách để triển khai bản kế hoạch này.** Khi nghiên cứu một bài cụ thể, bổ sung SBT nếu cần mở rộng hệ bài luyện; SGV nếu cần tìm dụng ý và lưu ý sư phạm; sách Chuyên đề học tập nếu mở cụm thuộc phụ lục C. ChatGPT phải nêu rõ tên sách, phần cần đọc và mục đích trước khi nhờ cung cấp. Chưa cần sách chuyên hay sưu tập hàng loạt tài liệu nâng cao.

Năm tài liệu quy trình từ sổ khác chỉ được giữ trong lịch sử hình thành thiết kế, không nạp làm nguồn chuẩn của dự án hoặc Notebook. Giữ các ý về nguồn chung, sản phẩm liên kết, kiểm định và trình bày nhất quán. Không kế thừa các lời bảo đảm về tiết kiệm 90%, chất lượng 100%, tự thừa hưởng toàn bộ ngữ cảnh, hay màu thương hiệu chưa được chốt. Công việc này không tiếp tục phát triển sổ ghi chú của dự án khác.

### 3.6. Vai trò và thứ tự xử lý nguồn

**Nguồn căn cứ của dự án là chương trình, SGK và văn bản/đề do cơ quan có thẩm quyền phát hành.** Đọc chương trình để xác định yêu cầu; dùng SGK để tra kiến thức và cách trình bày; dùng văn bản kỳ thi đúng năm để xác định quy cách; dùng đề chính thức và đề tham khảo do Bộ công bố làm dữ liệu nghiên cứu nhiệm vụ ôn. Hướng dẫn sử dụng công cụ lấy từ nhà cung cấp.

Phân biệt nguồn gốc nội dung với nơi lưu bản sao. Một bản scan văn bản Bộ được trường lưu vẫn có thể là bản sao của nguồn sơ cấp; phải kiểm tra cơ quan, số/ngày, trang và phần thực dùng. Một bản đánh máy lại, bài báo tóm tắt, bảng đáp án hoặc lời giải ghép vào cuối PDF không tự có cùng thẩm quyền với phần đề. Bản chép chưa đối chiếu không được gọi là bản chuẩn.

Theo lựa chọn của người chủ trì, không thu thập lời giải của các trang luyện thi hoặc AI bên ngoài để làm nền. Chúng ta tự giải từ đề và kiểm chứng lập luận. **Đáp án do Bộ công bố cũng là nguồn sơ cấp**, nhưng không cần đưa vào nguồn nghiên cứu và không phải điều kiện để tự biên soạn lời giải. Quy tắc chấm điểm và hướng dẫn ghi phiếu vẫn là căn cứ chính thức cần đọc; chúng khác với bảng kết quả của từng câu.

Nội dung ZO Math tự biên soạn được quản lý như sản phẩm có tác giả, phiên bản và bằng chứng kiểm tra. Bản kết tinh đã kiểm định có thể đưa vào Notebook để sản xuất; luôn ghi rõ là nội dung ZO Math, không gắn nhãn văn bản Bộ. Nếu có mâu thuẫn, trở về phát biểu, điều kiện và trang nguồn; kiểm chứng toán học trước khi sửa.

### 3.7. Mức kiểm tra nguồn

| Nhãn nội bộ | Ý nghĩa | Bằng chứng cần ghi |
| --- | --- | --- |
| T0 — Cần tìm | Chưa có đúng phần tài liệu cần dùng | Tên hoặc loại tài liệu, mục đích và phần cần tìm |
| T1 — Đã định vị | Có nơi công bố hoặc tệp ứng viên | Địa chỉ, tên và lý do xác định đúng nguồn |
| T2 — Đã mở | Đọc được toàn văn hoặc phần đang cần | Phần đã mở, ngày đọc, cách đọc chữ/hình |
| T3 — Đã đối chiếu | Đã kiểm tra đoạn phục vụ một mục tiêu cụ thể | Trang, mục tiêu, kết quả và chỗ còn vướng |
| T4 — Đã nạp và thử | Đúng phần nguồn đã qua phép thử trong Notebook đang dùng | Tên sổ, phiên bản nguồn, câu thử và kết quả thực tế |

Ghi mức theo **phần nguồn và công việc**, không gán một nhãn duy nhất cho cả cuốn rồi coi mọi trang đã đạt. T4 không thay T3: Notebook có thể đọc được một đoạn nhưng nội dung dùng trong bài học vẫn cần đối chiếu trực tiếp. Chưa có nguồn nào được ghi T4 cho notebook của chương trình này vì chưa thực hiện nạp và thử.

### 3.8. Sổ nguồn cần theo dõi khi triển khai

Các dòng sau là danh mục điều phối trong kế hoạch, chưa phải các tệp riêng đã tạo. Mã CT và S10.1–S12.2 được dùng xuyên suốt; các mã nhóm bổ sung được giải thích ngay trong bảng. Chỉ cấp mã chi tiết cho một nguồn mới khi thực sự dùng. Các mã này không thay mã SRC trong hệ nghiên cứu `_research/` của ZO Math.

| Mã/nhóm | Nguồn và vai trò | Mức đã có | Việc tiếp theo |
| --- | --- | --- | --- |
| CT | Chương trình môn Toán 2018 | Đã đọc phần THPT, đã đối chiếu cấp cụm | Gắn mục tiêu D0 và R1-G01 với yêu cầu, rồi mở rộng theo các gói ôn |
| S10.1–S12.2 | Sáu SGK làm trục tra cứu | Đọc được; mục lục đã đối chiếu; nội dung trong từng bài chưa kiểm hết | Ghi trang thực dùng và kiểm tra công thức/hình cho cụm đang học |
| VB | Văn bản điều chỉnh và chương trình tổng thể | Có kết quả từng văn bản tại mục 3.4; hồ sơ chưa đầy đủ | ChatGPT hoàn thiện lịch sử thay đổi có liên quan; đọc bản gốc còn thiếu |
| SGV/SBT | Sách giáo viên, bài tập, tài liệu tập huấn | Chưa có bộ hồ sơ đã đọc đầy đủ trong công việc này | Chỉ bổ sung phần cần cho bài đang thiết kế |
| CDHT | Sách Chuyên đề học tập | Đã có danh mục từ CT ở phụ lục C, chưa đọc ba sách | Mở khi đã xác định mục tiêu riêng của chuyên đề |
| THI | Quy định, đề và hướng dẫn kỳ thi | Có kiểm kê từng phần của tám tệp tại E.6; đã tách gói nguồn ở E.7 | Chọn câu theo mục tiêu; tự giải và kiểm chứng trước khi chấm; cập nhật hướng dẫn 2027 |
| ZM | Nội dung ZO Math dùng lại | Có danh sách ứng viên, chưa kiểm kê repo trong phiên này | Đọc đúng bản QMD, hình, PDF và hồ sơ liên quan trước khi dùng |
| NB | Hướng dẫn Notebook và Studio | Đã đọc các trang trợ giúp ghi ở phụ lục E | Thử nguồn, tính năng và cách xuất trên tài khoản thực tế khi triển khai |
| QT | Lịch sử năm ghi chú quy trình | Các quyết định đã chọn nằm trong mục 7–10 | Không nạp ghi chú thứ sinh vào nguồn chuẩn; dùng quy trình hiện hành trong kế hoạch |
| NC | Nghiên cứu giáo dục và toán mở rộng | Chưa mở đợt nghiên cứu mới theo kế hoạch này | Khi thật sự cần, đọc công trình gốc và ghi đúng phạm vi kết luận |

### 3.9. Hồ sơ tối thiểu và cách trích nguồn

Mỗi nguồn cần tên đầy đủ, tác giả/cơ quan, loại, năm/phiên bản, nơi công bố, tên tệp thực dùng, ngày đọc, trang in và trang PDF, mục tiêu/cụm liên quan, mức kiểm tra, phần còn thiếu và lưu ý sử dụng. Mẫu điền nằm ở phụ lục D.10.

Phân biệt trích nguyên văn với diễn giải và ví dụ tự biên soạn. Công thức trích chữ bị sai phải đối chiếu hình trang gốc; bản sửa để làm việc ghi rõ người sửa và chỗ nguồn. Ghi nguồn không đồng nghĩa có quyền phát lại nguyên sách: gói công khai dùng bài tự biên soạn, phần trích phù hợp và chỉ dẫn nguồn cần thiết.

### 3.10. Phạm vi và định dạng thi làm căn cứ

Quy chế thi hợp nhất năm 2026, Điều 4 khoản 2, xác định nội dung thi thuộc chương trình GDPT hiện hành cấp THPT, chủ yếu lớp 12. Điều này không đặt một tỉ lệ cố định cho từng lớp hoặc từng chuyên đề. [Quy chế hợp nhất, trang 2](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/4/02-vbhn-bgddt-kem.pdf).

Bản đề mã 0101 năm 2025 và năm 2026 đã được đọc trực tiếp, mỗi đề bốn trang. Cả hai dùng thời gian 90 phút và ba phần sau:

| Phần | Quy mô dùng cho đề mô phỏng hiện tại | Điểm tối đa |
| --- | --- | ---: |
| I — Nhiều lựa chọn | 12 câu, mỗi câu chọn một đáp án; đúng được 0,25 điểm | 3 |
| II — Đúng/sai | 4 câu, mỗi câu 4 ý. Đúng 0/1/2/3/4 ý được 0/0,1/0,25/0,5/1 điểm cho cả câu | 4 |
| III — Trả lời ngắn | 6 câu, đúng được 0,5 điểm mỗi câu | 3 |
| **Tổng** | **22 câu đánh số theo ba phần, tương ứng 34 lệnh trả lời** | **10** |

Nguồn định dạng: [Cục Quản lý chất lượng](https://vqa.moet.gov.vn/vi/news/thong-bao/cau-truc-dinh-dang-de-thi-tot-nghiep-thpt-tu-nam-2025-74.html). Số câu được đối chiếu trên hai bản đề ở phụ lục E.4. Cách tính điểm được kiểm tra theo [thông tin kỳ thi 2026 trên Cổng Thông tin điện tử Chính phủ](https://xaydungchinhsach.chinhphu.vn/thi-tot-nghiep-thpt-2026-de-thi-mon-ngu-van-11926061110312488.htm), đoạn hướng dẫn ba dạng trắc nghiệm.

**Định dạng trên là căn cứ triển khai ôn luyện hiện tại, không được ghi thành cấu trúc đã chốt riêng cho kỳ thi 2027.** Hướng dẫn năm học 2026–2027 nêu việc chuẩn bị tham gia thí điểm thi trên máy tính từ 2027. Lộ trình giữ năng lực giải toán và chỉ thay phần thao tác thi khi có hướng dẫn áp dụng cụ thể. [Hướng dẫn của Cục Quản lý chất lượng](https://vqa.moet.gov.vn/vi/news/tin-tuc-su-kien/bo-gddt-huong-dan-thuc-hien-nhiem-vu-quan-ly-chat-luong-nam-hoc-2026-2027-294.html).

### 3.11. Phần nguồn đã sẵn sàng và cách dùng ngay

Gói `ZO_Math_Nguon_khoi_dong_v0_5.zip` chứa bảy PDF làm việc, bảng xuất xứ và hướng dẫn chọn nguồn. Các trang được tách nguyên hình từ bản đã đọc; không ghép đáp án hay lời giải ngoài. Danh mục ở E.7 cho biết nguồn cha và trang gốc. “Đã tách” không có nghĩa đã OCR, giải hết đề hoặc đã thử trong Notebook.

Dự án ChatGPT giữ kế hoạch toàn cảnh, CT/SGK và hồ sơ nguồn. Notebook của D0 hoặc R1-G01 chỉ nhận phiếu giao việc, phần CT/SGK liên quan và câu/đề cần nghiên cứu; không cần nạp toàn bộ kế hoạch dài hoặc mọi văn bản hành chính. PDF có thể dùng trực tiếp; chỉ chép có kiểm tra các câu đang cần vào bản làm việc để tìm và phân tích dễ hơn. Luôn giữ hình, bảng, giả thiết chung và chỉ dẫn trang.

Tệp 2026 lần 2 là bản đánh máy lại, chưa đối chiếu đầy đủ với bản phát hành nên chưa nằm trong gói nguồn chuẩn khởi động. Điều này không chặn D0 hoặc R1-G01. Phiếu cũ và bài báo tổng hợp được giữ trong hồ sơ gốc, không dùng điều khiển luyện thi hiện tại.

### 3.12. Ba loại căn cứ A/B/C

| Nhãn | Ý nghĩa và giới hạn | Cách dùng trong 0.6 |
| --- | --- | --- |
| **A — Quy định/căn cứ chính thức** | Chương trình, văn bản và đề của Bộ/Cục; SGK là nguồn triển khai nội dung, không tự thay thế quy định chương trình | Ghi cơ quan, văn bản/bản sách, trang/mục, ngày, phạm vi áp dụng. Tách quy định khỏi nhiệm vụ chỉ quan sát trong một đề |
| **B — Căn cứ nghiên cứu** | Nghiên cứu gốc, tổng quan hệ thống, phân tích tổng hợp hoặc báo cáo học thuật được đọc đúng phần | Ghi đối tượng, nhiệm vụ, đối chứng, kết quả, giới hạn và mức tiếp cận; không đổi kết quả trung bình thành bảo đảm cá nhân |
| **C — Quyết định thiết kế ZO Math** | Cách tổ chức cụ thể để đáp ứng mục tiêu, bằng chứng và điều kiện dự án | Ghi lý do, tham số, dấu hiệu điều chỉnh và sản phẩm bị ảnh hưởng; có thể thử nghiệm, không gọi là định luật học tập |

Nhãn A/B/C không phải mức chất lượng cao–thấp. Một nghiên cứu quốc tế do cơ quan nhà nước công bố vẫn thuộc **B**, không phải quy định thi Việt Nam. Các mã C-01…C-10 ở F.2 là sổ quyết định; A, B và C không lẫn với chặng A–E, cụm Bxx hoặc phụ lục cùng chữ cái.

Quy tắc nguồn của 0.5 tiếp tục áp dụng cho toán và kỳ thi. Bổ sung nguồn học thuật cho thiết kế việc học là mở một loại căn cứ đúng chức năng, không đưa blog hay lời giải luyện thi thương mại trở lại làm nguồn thẩm quyền. SGV được ưu tiên khi cần giải thích ý đồ của tác giả sách; lượt tìm nguồn này chưa truy xuất được đúng tệp SGV, vì vậy chưa đưa kết luận nào dưới nhãn “SGV cho biết”. Điều đó không khẳng định SGV không có trong dự án.

### 3.13. Hồ sơ nghiên cứu thiết kế việc học

**Phạm vi đợt rà ngày 11/09/2026:** rà tài liệu có cấu trúc theo bảy câu hỏi kiến trúc, không tự gọi đây là một tổng quan hệ thống mới đã bao quát toàn bộ văn liệu. Đã ưu tiên nguồn dự án trước; tiếp đó tra theo tên công trình, tác giả và DOI (mã định danh tài liệu), đọc trang nhà xuất bản, tóm tắt tác giả trong cơ sở dữ liệu học thuật, báo cáo EEF và IES. Chỉ kết luận trong phần thực đọc. Từ khóa/nội dung tra cứu gồm retrieval practice trong lớp học; distributed practice/retention interval; interleaving mathematics; formative assessment trong trường trung học; mastery learning; educational feedback; tổ chức học dài hạn và thời điểm gia nhập. Tìm theo nhóm vấn đề rồi kiểm công trình/DOI gốc; không dùng số kết quả tìm kiếm làm thước đo bằng chứng. Danh mục chính dưới đây gồm cả kết quả thuận lợi lẫn giới hạn; không chọn riêng nghiên cứu có hiệu ứng lớn.

Điều kiện nhận nguồn: xác định được công trình/tổ chức và kết quả liên quan trực tiếp đến quyết định; phân biệt thử nghiệm, phân tích tổng hợp và hướng dẫn dựa trên nghiên cứu. Loại khỏi căn cứ: blog, diễn giải thương mại, lời giải ngoài, trang chỉ dẫn sai công trình, đường dẫn không đọc được. Không cộng số nghiên cứu giữa các tổng quan vì có thể trùng nhau. Tìm kiếm chưa bao quát có hệ thống các công trình mới 2022–2026; không tuyên bố danh mục này là toàn bộ bằng chứng mới nhất.

| Mã B / công trình | Phần thực đọc; bằng chứng được phép dùng | Giới hạn và hệ quả thiết kế C |
| --- | --- | --- |
| **NC01 — Roediger & Karpicke (2006), Test-enhanced learning: taking memory tests improves long-term retention**. Psychological Science, 17, 249–255. [Tóm tắt tác giả](https://pubmed.ncbi.nlm.nih.gov/16507066/), DOI 10.1111/j.1467-9280.2006.01693.x | Đã đọc tóm tắt: hai thí nghiệm học đoạn văn, so sánh tự nhớ lại với đọc lại; lợi thế khác nhau giữa kiểm tra ngay và kiểm tra trễ | Không phải thử nghiệm chương trình ôn Toán THPT Việt Nam. C-04 dùng nhiệm vụ tự tái hiện trước lời giải; không lấy cảm giác đọc trôi chảy làm bằng chứng bền vững |
| **NC02 — Agarwal, Nunes & Blunt (2021), Retrieval Practice Consistently Benefits Student Learning: a Systematic Review of Applied Research in Schools and Classrooms**. Educational Psychology Review, 33, 1409–1453. [Nhà xuất bản](https://link.springer.com/article/10.1007/s10648-021-09595-9), DOI 10.1007/s10648-021-09595-9 | Đọc tóm tắt và thông tin phương pháp công bố: 50 thí nghiệm, 5.374 người học; 57% kích thước hiệu ứng ở mức vừa/lớn; lợi ích được ghi nhận ở nhiều bối cảnh lớp học | Chỉ 6% thí nghiệm ngoài nhóm quốc gia phương Tây, có giáo dục, công nghiệp hóa, giàu và dân chủ. Chưa đọc toàn văn thuê bao. Không suy tác động riêng lên điểm thi Việt Nam; cần theo dõi việc sử dụng thực |
| **NC03 — Cepeda và cộng sự (2006), Distributed practice in verbal recall tasks: A review and quantitative synthesis**. Psychological Bulletin, 132, 354–380. [Tóm tắt tác giả](https://pubmed.ncbi.nlm.nih.gov/16719566/), DOI 10.1037/0033-2909.132.3.354 | Đọc tóm tắt: 317 thí nghiệm; khoảng cách học và thời gian cần duy trì cùng ảnh hưởng kết quả; khoảng cách tốt nhất tăng khi thời gian duy trì tăng | Chủ yếu nhiệm vụ nhớ ngôn từ; chưa đọc toàn văn. C-05 giữ các lượt giãn cách và điều chỉnh theo mục tiêu/thời gian đến thi; không suy lịch tối ưu cố định |
| **NC04 — Cepeda và cộng sự (2008), Spacing effects in learning: a temporal ridgeline of optimal retention**. Psychological Science, 19, 1095–1102. [Hồ sơ tác giả qua Europe PMC](https://europepmc.org/article/MED/19076480), DOI 10.1111/j.1467-9280.2008.02209.x | Đọc tóm tắt qua cơ sở dữ liệu Europe PMC: hơn 1.350 người học thông tin sự kiện; khoảng cách ôn đến 3,5 tháng, kiểm tra đến một năm; tăng khoảng cách không tạo lợi ích vô hạn | Nội dung và thiết kế khác giải toán dài hạn. Không lấy tỉ lệ khoảng cách trong thí nghiệm làm thuật toán lịch học sinh; đây là căn cứ giới hạn của C-05 |
| **NC05 — Brunmair & Richter (2019), Similarity matters: A meta-analysis of interleaved learning and its moderators**. Psychological Bulletin, 145, 1029–1052. [Tóm tắt tác giả](https://pubmed.ncbi.nlm.nih.gov/31556629/), DOI 10.1037/bul0000209 | Đọc tóm tắt qua PubMed/Europe PMC: 59 nghiên cứu, hiệu ứng chung g = 0,42; nhóm nhiệm vụ toán g = 0,34; kết quả đổi theo loại tài liệu | Không phải mọi hình thức trộn bài đều tốt. C-06 chọn các loại nhiệm vụ cần phân biệt công cụ; không trộn ngẫu nhiên tám mạch hoặc gọi đổi bối cảnh là đủ xen kẽ |
| **NC06 — Perry và cộng sự (2021), Cognitive Science in the Classroom: Evidence and Practice Review**, EEF | Đọc phần phương pháp, bảng nghiên cứu và đánh giá bằng chứng mục B2 về xen kẽ (tr.in 53–67; PDF 56–70), cùng vị trí các mục B1/B3. [Trang báo cáo và toàn văn](https://educationendowmentfoundation.org.uk/education-evidence/evidence-reviews/cognitive-science-approaches-in-the-classroom) | Nhiều nghiên cứu xen kẽ tập trung toán ở tuổi 8–14, bài kiểm tra do nhóm nghiên cứu thiết kế và quy trình được kiểm soát. C-06 là chuyển dụng có giới hạn sang THPT; phải đo cả chọn phương pháp, duy trì và thời gian |
| **NC07 — Wisniewski, Zierer & Hattie (2020), The Power of Feedback Revisited: A Meta-Analysis of Educational Feedback Research**. Frontiers in Psychology, 10, 3087. [Toàn văn](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full), DOI 10.3389/fpsyg.2019.03087 | Đọc tóm tắt, phương pháp, kết quả và phần dị biệt: 435 nghiên cứu; tác động phụ thuộc nội dung phản hồi và khác nhau đáng kể giữa các nghiên cứu | Không trình bày “phản hồi” như một biện pháp đồng nhất. C-07 yêu cầu chỉ đúng bước sai, việc sửa và bài thử lại; lời khen hoặc chỉ ghi điểm không thay thông tin hành động |
| **NC08 — EEF, Embedding Formative Assessment**, thử nghiệm tại trường trung học, báo cáo đánh giá 2018 | Đọc trang kết quả của đơn vị tài trợ/đánh giá: 140 trường; tác động tích cực ở chỉ số Attainment 8 tổng hợp, nhưng không tìm thấy bằng chứng cải thiện riêng GCSE Toán hoặc tiếng Anh. [Kết quả và báo cáo](https://educationendowmentfoundation.org.uk/projects-and-evaluation/projects/embedding-formative-assessment) | Chưa đọc toàn bộ báo cáo đánh giá; can thiệp gồm phát triển chuyên môn giáo viên, không chỉ thêm bài kiểm tra. C-07 dùng vòng thu bằng chứng–đổi dạy/học–thử lại, không hứa mức tăng điểm Toán |
| **NC09 — Kulik, Kulik & Bangert-Drowns (1990), Effectiveness of Mastery Learning Programs: A Meta-Analysis**. Review of Educational Research, 60, 265–299. [Tóm tắt nhà xuất bản](https://journals.sagepub.com/doi/abs/10.3102/00346543060002265), DOI 10.3102/00346543060002265 | Đọc tóm tắt: 108 đánh giá có đối chứng; nhìn chung có lợi cho kết quả, nhưng có thể tăng thời gian học; mô hình tự tiến theo tốc độ cá nhân ở đại học có nguy cơ giảm hoàn thành | Nguồn cũ, nhiều bối cảnh khác nhau; chưa đọc toàn văn. C-08 giữ sửa tiên quyết và đánh giá lại, đồng thời giới hạn thời gian sửa và cho tiếp tục nhánh độc lập |
| **NC10 — Pashler và cộng sự (2007), Organizing Instruction and Study to Improve Student Learning**, IES/NCER 2007-2004 | Đọc bảng khuyến nghị và các đoạn liên quan của khuyến nghị 1, 2, 5b, 6b trong [báo cáo](https://ies.ed.gov/ncee/WWC/Docs/PracticeGuide/20072004.pdf): giãn cách; xen ví dụ đã giải với tự giải; câu hỏi giải thích; kiểm tra giúp học | Đây là hướng dẫn tổng hợp nghiên cứu tại thời điểm 2007. Xen ví dụ–tự giải khác xen các loại bài toán. C-04/C-06 thêm hỗ trợ cho phần chưa học; không biến D0 thành bài kiểm tra kiến thức chưa được dạy |

**Nguồn bổ trợ về tiến tiếp:** [EEF — Mastery learning](https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/mastery-learning), đã đọc phần định nghĩa, triển khai và giới hạn ngày 11/09/2026. Nguồn mô tả các ngưỡng thường dùng 80–90%, đồng thời nhấn mạnh hỗ trợ và khó khăn triển khai. Đây không phải kiểm chứng cho **đúng 80% + hai cụm + một tuần** của ZO Math. Ngưỡng đó vẫn thuộc C-08, không được đổi nhãn thành kết luận B.

**Gia nhập tháng 9, tháng 11, tháng 1 và thời hạn thi cố định:** chưa có bằng chứng trực tiếp trong tập nguồn đã đọc xác nhận một lịch nén cụ thể tối ưu cho bối cảnh ZO Math. Không khẳng định nghiên cứu như vậy không tồn tại. Thuật toán ở 12.10–12.13 là **C-09**, dựa vào chẩn đoán, tiên quyết, thời gian thực và nguyên tắc giữ độ phủ do dự án chọn. Nó phải được thử và sửa từ dữ liệu.

**Điều không được gán cho nghiên cứu:** 36 tuần; 6 giờ/tuần; số giờ từng khâu; 24 nhiệm vụ D0; 80%; hai cụm cách một tuần; tối đa hai ưu tiên; 2–3 ngày/7 ngày/3–4 tuần; sáu đề; cửa sổ ba đề; lịch nén 29 hoặc 20 tuần. Các con số này là tham số C, trừ quy cách thi đã có căn cứ A và chỉ trong phạm vi áp dụng của căn cứ ấy.

### 3.14. Cấu hình kỳ thi độc lập với nội dung

**C-03:** dùng hồ sơ `THI-THPT-2027-TAM-v1` cho quy cách mô phỏng hiện tại tại 3.10. Chữ TAM nghĩa là cấu hình làm việc tạm thời của ZO Math, **không phải mã hoặc xác nhận định dạng 2027 của Bộ**. Bảng 3.10 giữ 12–4–6, 90 phút và cách chấm để vận hành theo căn cứ đang có; mọi chỗ khác nói “90 phút”, “ba dạng” hoặc “sáu đề” trong lịch phải đọc trong phạm vi cấu hình/lịch tham chiếu này.

| Trường cấu hình | Giá trị hoặc trạng thái hiện tại |
| --- | --- |
| Phạm vi toán | CT hiện hành cấp THPT, chủ yếu lớp 12 theo Điều 4–5 bản quy chế hợp nhất đã đối chiếu; không suy tỉ lệ cố định |
| Quy cách làm việc | Bảng 3.10; phiếu tại Phụ lục VI CV1239/2025 dùng làm mẫu luyện hiện có |
| Năm/bối cảnh căn cứ | Định dạng công bố từ 2025; đề 2025–2026; không phải xác nhận riêng mùa 2027 |
| Ngày thi 2027 | Chưa xác nhận từ nguồn đã kiểm trong đợt này; lịch cá nhân bắt buộc ghi mốc giả định nếu chưa có ngày chính thức |
| Thi giấy/máy tính | Không suy hướng dẫn chuẩn bị thí điểm thành áp dụng đại trà; xác nhận hình thức và đối tượng áp dụng khi có văn bản cụ thể |
| Người kiểm, ngày, văn bản | Hồ sơ dự án; cập nhật nguồn ngày 11/09/2026 như E.8 |
| Phụ thuộc | Mã đề, phiếu, quy tắc chấm, bài tập thao tác, lịch mô phỏng; mỗi thành phẩm ghi cấu hình thực dùng |

Một câu có hai phần hồ sơ: **nhiệm vụ toán và tiêu chí lập luận**; **cách đưa vào đánh giá**. Có thể giữ nhiệm vụ nhưng đổi lựa chọn, số ý, cách nhập đáp số, điểm và thời lượng. Sau đổi phải giải/kiểm lại tính duy nhất và điều kiện; không mặc định đổi hình thức luôn vô hại.

Khi Bộ chỉ đổi số câu, cách chấm, phương tiện hoặc ngày thi, chủ yếu sửa lớp 4 và lớp 3. Khi Bộ đổi **phạm vi/yêu cầu cần đạt**, rà từ CT đến CD/B rồi R/gói; không hứa kiến trúc nội dung bất biến trước một thay đổi chương trình thực sự. Quy trình cập nhật cụ thể ở 12.14.

## 4. Tổ chức phạm vi kiến thức

### 4.1. Bốn nhãn phạm vi

| Nhãn | Cách dùng |
| --- | --- |
| Chung | Yêu cầu trong phần chung của chương trình Toán THPT; là nền của kho ôn thi |
| Chuyên đề học tập | Có trong phần chuyên đề của chương trình; theo dõi riêng, không mặc định toàn bộ là phần bắt buộc của đề thi |
| Củng cố | Kiến thức THCS hoặc công cụ nền cần để học phần chính |
| Mở rộng | Diễn giải sâu, cách giải hoặc nội dung ngoài mục tiêu chung đang đối chiếu; ghi rõ vai trò |

Đào sâu không đồng nghĩa vượt chương trình: một câu hỏi giải thích điều kiện hoặc phản biện lời giải có thể sâu nhưng vẫn ở phạm vi chung. Một nội dung xuất hiện trong hoạt động thực hành cũng không tự trở thành một chuyên đề lý thuyết bắt buộc độc lập.

### 4.2. Nhóm kiến thức để tra kho

| Mã | Nhóm nội dung | Các cụm dự kiến | Câu hỏi dẫn đường |
| --- | --- | --- | --- |
| CD01 | Ngôn ngữ toán và công cụ đại số | B01–B03 | Viết, biến đổi và kết luận thế nào để không đổi nghĩa bài toán? |
| CD02 | Hàm số, đồ thị, dấu và nghiệm | B04–B06 | Công thức, bảng và đồ thị đang nói về cùng một đối tượng ra sao? |
| CD03 | Lượng giác | B07–B09 | Từ chuyển động trên đường tròn đến quy luật tuần hoàn và nghiệm |
| CD04 | Dãy số, giới hạn và liên tục | B10–B12 | Một quá trình tiến gần hoặc tích lũy có thể được mô tả thế nào? |
| CD05 | Lũy thừa, mũ và lôgarit | B13–B15 | Tăng trưởng theo tỉ lệ khác tăng trưởng theo lượng như thế nào? |
| CD06 | Ý nghĩa và phép tính đạo hàm | B16–B17 | Đo tốc độ thay đổi tại một thời điểm bằng cách nào? |
| CD07 | Ứng dụng đạo hàm | B18–B21 | Từ dấu đạo hàm, ta biết và chưa biết gì về hàm số? |
| CD08 | Nguyên hàm và tích phân | B22–B24 | Liên hệ tốc độ thay đổi với tổng lượng tích lũy |
| CD09 | Hệ thức lượng và vectơ phẳng | B25–B27 | Chuyển từ hình vẽ sang các đại lượng có thể tính toán |
| CD10 | Tọa độ trong mặt phẳng | B28–B29 | Một phương trình mô tả hình và vị trí như thế nào? |
| CD11 | Hình học không gian | B30–B32 | Suy luận trong không gian mà không phụ thuộc hình vẽ phối cảnh |
| CD12 | Vectơ và tọa độ trong không gian | B33–B35 | Chọn vectơ và hệ tọa độ để giải quyết quan hệ không gian |
| CD13 | Thống kê và đọc dữ liệu | B36–B38 | Các số đặc trưng nói được và không nói được gì về dữ liệu? |
| CD14 | Đếm và xác suất | B39–B41 | Chọn không gian mẫu và dùng thông tin điều kiện đúng cách |
| CD15 | Kết nối, mô hình hóa và đánh giá tổng hợp | Hồ sơ B42, tích lũy xuyên suốt | Tự chọn công cụ khi đề bài không cho biết đang kiểm tra chuyên đề nào |

Đây là bản đồ quản lý kho kiến thức, không phải thứ tự ôn hoặc thứ tự sản xuất. Danh mục chi tiết, mục tiêu và kiến thức cần trước nằm ở phụ lục B. Khi chia lại cụm, giữ mã gốc và dùng mã con để truy ngược, chẳng hạn B35.a, B35.b; ghi thay đổi cách đóng gói thay vì âm thầm đổi tổng số.

### 4.3. Những điểm phạm vi phải giữ khi triển khai

- B01 phải có mệnh đề đảo, điều kiện cần/đủ, lượng từ và phép toán tập hợp; không chỉ luyện khoảng nghiệm.
- B03 phải có cả bất phương trình và hệ, miền nghiệm và bài toán tối ưu trên miền đa giác đơn giản theo CT tr.79.
- B10 có cách cho dãy, tăng/giảm và bị chặn; không thu hẹp thành hai công thức cấp số.
- B17 có đạo hàm bằng quy tắc và cấp hai; ý nghĩa gia tốc cần được xử lý. Điểm uốn và tính cong được gắn nhãn đúng phạm vi, không tự thêm thành yêu cầu chung chỉ vì đã có trong bài ZO Math khác.
- B21 cần các dạng khảo sát nêu ở CT tr.106, gồm đa thức bậc ba, phân thức bậc nhất trên bậc nhất và bậc hai trên bậc nhất, với điều kiện tương ứng; không bỏ phân thức bậc hai trên bậc nhất.
- B32 phải có hình chóp cụt đều và thể tích theo CT tr.101, bên cạnh chóp, lăng trụ, hộp và khoảng cách.
- B36 phải có phát hiện dữ liệu không hợp lý, số gần đúng và sai số; không chỉ bấm máy tính số đặc trưng.
- B39 tách rõ đếm, nhị thức Newton ở phạm vi chung và xác suất cổ điển; không dùng nhị thức tổng quát của chuyên đề để thay phạm vi chung.
- B41 cần đọc bảng 2×2, sơ đồ cây và diễn giải điều kiện, bên cạnh công thức toàn phần và Bayes.
- Các hoạt động thực hành, trải nghiệm và công cụ được gắn vào đúng mạch từ đầu; B42 không phải nơi dồn tất cả phần còn thiếu.

### 4.4. Năng lực và hoạt động xuyên suốt

Mỗi nhãn năng lực phải có một việc học sinh thực sự làm. Bảng này là gợi ý thiết kế của ZO Math để triển khai suy lí và kiến tạo ý nghĩa; không phải danh mục yêu cầu được trích nguyên văn.

| Mạch | Nhiệm vụ minh họa | Bằng chứng để xem |
| --- | --- | --- |
| Đọc và diễn đạt toán | Viết lại giả thiết, điều cần tìm và điều kiện bằng lời | Học sinh giữ đúng ý nghĩa, không bỏ dữ kiện |
| Suy lí và kiểm chứng | Giải thích một bước, tìm phản ví dụ hoặc sửa lời giải | Lập luận và điều kiện sử dụng được nêu rõ |
| Liên hệ biểu diễn | Ghép công thức–bảng–hình; giải thích chỗ không khớp | Có lý do, không chỉ chọn hình |
| Mô hình hóa | Từ một khoản phí, phép đo hoặc dữ liệu, lập mô hình và kiểm tra miền hợp lệ | Biến, đơn vị, giả thiết và kết luận theo bối cảnh |
| Công cụ | Dựng hình, lập bảng tính hoặc kiểm tra trường hợp nhỏ | Sản phẩm có giải thích; phân biệt quan sát với chứng minh |
| Tự điều chỉnh | Phân loại lỗi, sửa và làm một câu mới | Có bài làm sau sửa, không chỉ đánh dấu đã xem lời giải |

Khi hoàn thiện một nhóm CD, rà có nhiệm vụ thực hành phù hợp trong các bài của nhóm hay chưa. Ghi sản phẩm cụ thể: hình dựng, bảng dữ liệu, mô hình bằng công thức hoặc lời giải thích. Tình huống tự đặt và số liệu giả định phải được ghi rõ. Những hoạt động có điều kiện tổ chức trong CT giữ nguyên điều kiện ấy; điều chỉnh cách thực hiện cho tự học ở nhà khi phù hợp.

### 4.5. Bản đồ tám mạch ôn thi

Mã R dùng trong tài liệu này chỉ mạch ôn thi. Một mạch có thể cần nhiều gói học liệu. Mã N chỉ phần nền được bổ sung khi cần; không phải chặng buộc học lại toàn bộ lớp 10.

| Mạch | Nhiệm vụ ôn thi cần làm được | Kiến thức kết nối lớp 10–12 | Sản phẩm đánh giá đặc trưng |
| --- | --- | --- | --- |
| **R1. Hàm số, đạo hàm, đồ thị** | Đọc và nối công thức, bảng dấu, bảng biến thiên, đồ thị; xét đơn điệu, cực trị, giá trị lớn nhất/nhỏ nhất, tiệm cận; xử lý điều kiện và miền xét | Hàm số, bậc hai, dấu tam thức → giới hạn, liên tục, đạo hàm → khảo sát và ứng dụng đạo hàm | Cụm câu đổi biểu diễn; đúng/sai có giải thích; bài tìm giá trị trên miền có biên |
| **R2. Thống kê và đọc dữ liệu** | Đọc bảng/biểu đồ; tính và giải thích số đặc trưng; so sánh dữ liệu, phát hiện kết luận thiếu căn cứ; giữ đúng đơn vị và cách làm tròn | Dữ liệu không ghép nhóm, số gần đúng → trung tâm mẫu ghép nhóm → độ phân tán mẫu ghép nhóm | Cụm câu từ một bộ dữ liệu, có lựa chọn thước đo và giải thích kết luận |
| **R3. Hình học, vectơ và tọa độ** | Nhận diện quan hệ hình học; chọn cách tổng hợp hoặc tọa độ; tính góc, khoảng cách, thể tích; lập phương trình đường, mặt phẳng, mặt cầu | Hệ thức lượng tam giác, vectơ, Oxy và conic → hình không gian, song song, vuông góc → vectơ Oxyz, phương trình không gian | Một tình huống hình học được biểu diễn theo hai cách, kèm kiểm tra độ dài/góc và miền chuyển động |
| **R4. Đếm và xác suất** | Lập không gian mẫu; đếm không trùng; phân biệt độc lập và xung khắc; dùng xác suất có điều kiện, toàn phần, Bayes; kiểm tra mẫu số | Quy tắc đếm, hoán vị/chỉnh hợp/tổ hợp, nhị thức Newton trong phạm vi chung, xác suất cổ điển → phép toán biến cố → xác suất có điều kiện | Cụm đếm; bảng hai chiều hoặc cây xác suất; câu đổi chiều điều kiện |
| **R5. Dãy số, mũ và lôgarit** | Phân biệt tăng theo lượng và theo tỉ lệ; xử lý cấp số, giới hạn dãy, phương trình/bất phương trình mũ–lôgarit; xây và kiểm tra mô hình tăng trưởng | Dãy số, cấp số, tổng và giới hạn → lũy thừa, mũ, lôgarit → kết nối đạo hàm, nguyên hàm trong mô hình | Bài tìm thời điểm/số kì hoặc tham số; kiểm tra miền, tính nguyên và tính hợp lí |
| **R6. Hàm số lượng giác và phương trình lượng giác** | Đọc góc và giá trị lượng giác; dùng công thức, đồ thị; giải phương trình, chọn nghiệm trong khoảng; giải thích chu kì | Lượng giác tam giác → góc lượng giác, bốn hàm lượng giác và phương trình → đạo hàm/nguyên hàm có lượng giác | Câu họ nghiệm và chọn nghiệm; tình huống tuần hoàn với đơn vị góc được chỉ rõ |
| **R7. Nguyên hàm, tích phân và ứng dụng** | Nối tốc độ biến thiên với lượng tích lũy; tính nguyên hàm/tích phân; lập diện tích, thể tích, quãng đường đúng miền và dấu | Đạo hàm, đồ thị, dấu, giao điểm → nguyên hàm và tích phân → mô hình tích lũy, mặt cắt và khối tròn xoay | Câu chọn biểu thức tích phân trước khi tính; bài có điều kiện đầu và bài hình học–tích phân |
| **R8. Mô hình hóa, tối ưu và tổng hợp** | Chuyển lời văn thành biến, ràng buộc, hàm mục tiêu; chọn công cụ; giải thích đáp số và kiểm tra bối cảnh | Bất phương trình hai ẩn, hàm bậc hai, hình học, dãy số → đạo hàm, tích phân, xác suất và dữ liệu | Bài không ghi sẵn tên phương pháp; yêu cầu tự xác định công cụ và kiểm tra kết quả |
| **N. Nền tảng dùng xuyên suốt** | Đọc mệnh đề, tập hợp, điều kiện; biến đổi đại số; phương trình, bất phương trình; phân số, tỉ lệ, đơn vị; đọc hình và thao tác máy tính | Kiến thức THCS và nội dung nền lớp 10–11 phục vụ trực tiếp R1–R8 | Một lỗi được sửa bằng giải thích ngắn và một câu mới tương đương |

R8 xuất hiện trong các mạch ngay từ lượt đầu, rồi trở thành trọng tâm ở lượt phối hợp. Một câu có thể mang nhiều mã; ví dụ thể tích qua tích phân là R7 chính, R3 hỗ trợ. Khi cộng số câu, chỉ đếm một lần theo mã chính.

**Nguyên tắc bao quát:** nội dung ít xuất hiện trong hai đề đã đọc vẫn có vị trí theo chương trình. Không loại bỏ thống kê phân tán, mặt cầu, lượng giác hay conic chỉ vì một mã đề không hỏi trực tiếp.

### 4.6. Ánh xạ mạch ôn sang danh mục kiến thức đã xây dựng

| Mạch ôn | Cụm chính trong kho | Cụm nền hoặc hỗ trợ | Cách sử dụng |
| --- | --- | --- | --- |
| R1 | B12, B16–B21 | B02, B04–B06; B08, B13–B15 theo loại hàm | Gói ôn nối thông tin; gọi nền đúng lỗi, không đòi hoàn thành tất cả cụm trước |
| R2 | B36–B38 | B02; đọc điều kiện B01 | Đi từ dữ liệu đến tính toán và giải thích |
| R3 | B25–B35 | B02, B05; B16–B21 khi tối ưu khoảng cách | Phối hợp hình tổng hợp, vectơ và tọa độ |
| R4 | B39–B41 | B01–B02; B10 khi đếm có ràng buộc dãy | Đếm, biến cố, điều kiện và kiểm tra mô hình |
| R5 | B10–B11, B13–B15 | B02, B04, B06, B12, B16–B17 | Dãy số, tăng trưởng, ngưỡng và điều kiện |
| R6 | B07–B09 | B25; B16–B17 và B22 khi nối giải tích | Góc, tuần hoàn, nghiệm và ứng dụng |
| R7 | B22–B24 | B04–B06, B12, B17, B29, B32; B08, B13–B15 theo biểu thức | Tích lũy, diện tích, thể tích và lập cận |
| R8 | B03, B19, hồ sơ B42 | Chọn từ R1–R7 và N theo tình huống | Xây mô hình, tự chọn phương pháp, giải và kiểm tra bối cảnh |
| N | B01–B02 và phần nền của các cụm | Kiến thức THCS thực sự cần | Phiếu bổ sung ngắn hoặc dẫn tới nội dung nền đã kiểm định |

Mọi B01–B42 đều có vị trí trong bảng. Tám mạch ôn không thay thế hoặc xóa 15 nhóm và danh mục B; chúng tổ chức cách sử dụng kho theo nhu cầu thi. R8 là mạch phối hợp, vì thế không cộng thời gian của nó một lần nữa khi đã nằm trong gói R1–R7. D0 khảo sát các mạch và nền, không tạo thêm một mạch kiến thức thứ chín.

### 4.7. Chuẩn hóa thuật ngữ và tên gọi

**C-02:** tên chính lấy thuật ngữ CT/SGK; tên nhóm ghép của ZO Math được ghi là tên nội bộ. Ý tưởng giúp hiểu toán nằm ở câu hỏi dẫn đường, mục tiêu hoặc phụ đề. Không biến một cách diễn giải thành một yêu cầu chính thức.

| Phạm vi audit | Quyết định hiện hành | Căn cứ/giới hạn |
| --- | --- | --- |
| R1–R5 | Giữ tên ghép và vai trò tại 4.5; đó là tên mạch của ZO Math | Thuật ngữ thành phần có trong CT; không nói CT quy định tám R |
| R6 | **Hàm số lượng giác và phương trình lượng giác**; góc, công thức và tính tuần hoàn vẫn ở nội dung kết nối | Tên mạch kiến thức CT tr.89–91; không bỏ B07 vì tiêu đề rút gọn |
| R7 | **Nguyên hàm, tích phân và ứng dụng** | CT tr.107; S12.2 Chương IV, Bài 11–13. “Tích lũy” giữ ở lớp ý tưởng/mô hình, không là tên nội dung chính thức |
| R8 và CD01–CD15 | Giữ các tên quản lý tại 4.2/4.5; ghi rõ là tổ chức nội bộ | “Tối ưu”, “đọc dữ liệu”, “kết nối” mô tả nhiệm vụ; không tự mở rộng phạm vi bắt buộc |
| B01–B41 | Tên chính đã chuẩn ở Phụ lục B; toàn bộ diễn giải còn đúng được giữ sau tên | B02 là củng cố; tiêu đề như “từ đồ thị đến dấu và nghiệm” trở thành cách diễn giải, không thay tên “Dấu của tam thức bậc hai…” |
| B42 | Hồ sơ kết nối và đánh giá tổng hợp | Không phải một nội dung chương trình mới |
| Chuyên đề học tập | Chín tên chính và ranh giới tại C | CD của dự án không đồng nghĩa chuyên đề lựa chọn trong CT |
| Tính đơn điệu; cực trị; giá trị lớn nhất/nhỏ nhất | Không dùng ba thuật ngữ thay nhau; phân biệt điểm cực trị, giá trị cực trị và giá trị trên miền xét | CT tr.105–106; kiểm định điều kiện trong từng lời giải |
| Mẫu số liệu; số đặc trưng đo xu thế trung tâm/mức độ phân tán | Tên chính theo CT; “trung tâm”, “độ phân tán” chỉ viết gọn khi ngữ cảnh rõ | CT tr.85–86, 101–102, 110 |
| Góc nhị diện và góc phẳng nhị diện | Ghi đủ khi đó là mục tiêu; không chỉ viết chung “góc không gian” | CT tr.100–101 |
| Tọa độ trong mặt phẳng/không gian | Ghi Oxy/Oxyz đúng chỗ; B.8 trong bảng lịch là không gian | Không nhầm chặng B.8 với cụm B08 |
| Luyện nhớ lại; luyện tập giãn cách; luyện xen kẽ | Dùng kèm thuật ngữ tiếng Anh ở lần định nghĩa; “gọi lại” là cách viết ngắn trong lịch | Định nghĩa hoạt động và giới hạn ở 3.13, 5.5; không đồng nhất đọc lại với tự nhớ lại |
| Đánh giá vì sự tiến bộ; học đến mức làm chủ; phản hồi | Gắn với bằng chứng và hành động; không dùng “mastery” như nhãn chứng nhận chuẩn hóa | CT tr.116–117 và nghiên cứu B; cơ chế cụ thể là C |
| Thực hành/mô phỏng và phương tiện thi | Phân biệt công cụ học toán với công cụ được phép khi thi | CT có hoạt động phần mềm có điều kiện; cấu hình thi kiểm riêng |

Khi phát hành gói mới, rà tên, mục tiêu, sơ đồ, câu hỏi, lời giải, phiếu đánh giá và metadata theo cùng bảng; bản nguồn/lịch sử giữ nguyên tên gốc để truy tìm. Những từ diễn giải hợp lệ như “tích lũy”, “đổi biểu diễn”, “nền”, “vá lỗi” không bị cấm, nhưng không được đưa dưới dạng trích dẫn CT. Không tuyên bố đã audit thuật ngữ của mọi trang SGK hoặc mọi sản phẩm chưa truy xuất.

## 5. Từ phạm vi đến mục tiêu có thể kiểm tra

Với mỗi cụm, chuẩn bị bảng gồm: mã yêu cầu nội bộ; trang CT; bài/trang SGK; mục tiêu diễn giải của ZO Math; nhiệm vụ học sinh làm; sản phẩm chứa nhiệm vụ; trạng thái. Mã yêu cầu do ZO Math đặt, không phải mã của Bộ.

Rà theo hai chiều: từ CT sang bài học để tìm thiếu; từ bài học về CT để nhận ra mở rộng hoặc phát biểu không có căn cứ. Chỉ đánh dấu “đã đáp ứng” sau khi học liệu và nhiệm vụ kiểm tra thực sự tồn tại và đã được xem lại. Có tên chương trong danh mục mới là “đã có vị trí”.

Ba mức học trong một bộ là **Nền tảng — Vận dụng — Đào sâu**. Đây là lối vào linh hoạt, không phải nhãn cố định của học sinh và không phải bản thay thế các mức đánh giá chính thức. Kiểm tra đầu vào giúp em biết cần ôn đúng phần nào; kiểm tra cuối dùng câu mới và có hướng dẫn sửa lỗi.

Không ấn định cùng 12 câu luyện cho mọi cụm. Số câu theo các mục tiêu cần có bằng chứng; mỗi mục tiêu cốt lõi phải có nhiệm vụ thích hợp. Với D0 và R1-G01, dùng đặc tả ở mục 11 để bắt đầu. Các khung luyện B04–B06 được giữ tại phụ lục G để dùng khi cần bổ sung nền. Bài tự luyện tách khỏi lời giải, nhưng lời giải phải đủ để học sinh tự kiểm tra lập luận, điều kiện và đáp số.

### 5.1. Cấu trúc ma trận để kiểm từng yêu cầu cần đạt

| Trường | Cách ghi và kiểm tra |
| --- | --- |
| Mã yêu cầu | Mã nội bộ ổn định, chẳng hạn YC-B04-01; không gọi là mã Bộ |
| Nguồn và phiên bản | CT, SGK hoặc nguồn bổ sung thực dùng; nhóm H-YC và mã yêu cầu con liên quan |
| Căn cứ quyết định | Nhãn A/B/C, mã NC/C khi liên quan; phân biệt yêu cầu nguồn với cách ZO Math tổ chức học |
| Vị trí | Trang in, trang PDF, đề mục/bài; chỗ chưa kiểm tra ghi rõ |
| Yêu cầu nguồn | Diễn giải sát nguồn hoặc đoạn trích được đánh dấu rõ |
| Mục tiêu ZO Math | Động tác học sinh làm được: giải thích, xác định, lập, tính, kiểm tra… |
| Điều kiện học trước | Kiến thức cụ thể và nơi ôn lại có thể dùng |
| Phạm vi | Chung, chuyên đề học tập, củng cố hoặc mở rộng |
| Cụm, mạch và gói | Mã Bxx của kiến thức, mạch R chính/hỗ trợ, mã gói và chặng sử dụng |
| Bằng chứng đánh giá | Mã câu hỏi/nhiệm vụ cùng tiêu chí xem bài làm |
| Thành phẩm | Tệp, trang, sản phẩm chứa nội dung và nhiệm vụ |
| Trạng thái và chỗ thiếu | Có vị trí, đã viết, đã kiểm tra hoặc đã công bố; ghi điều còn thiếu |

Mẫu hàng ở phụ lục D.8 là hàng thiết kế đã định vị nguồn, chưa là chứng nhận học liệu đã đáp ứng. Cần tách từng yêu cầu theo độ cụ thể thực tế; không chia máy móc mỗi câu chữ thành một bài hoặc gộp cả chương thành một hàng.

Nếu báo độ bao phủ, ghi rõ mẫu số là bao nhiêu yêu cầu đã đối chiếu thuộc phạm vi nào; tử số là bao nhiêu yêu cầu có học liệu và nhiệm vụ đã kiểm tra. Công bố cả phần chưa ghép, chưa viết và chưa kiểm tra. Số 24 chương hoặc 79 bài không thay thế phép kiểm này.

Mỗi câu/ý trong ma trận còn có **năng lực cần quan sát**, **cấp độ tư duy dự kiến và lý do**, **định dạng trả lời**, **mã họ câu** và **lịch sử đã gặp**. Ba trục năng lực, mức tư duy và định dạng được ghi riêng; không mặc định câu trả lời ngắn luôn khó hoặc bảng minh họa lớp 10 là tỉ lệ bắt buộc của đề THPT.

Với đúng/sai, lưu kết quả từng ý để chẩn đoán; khi mô phỏng thi, chấm tổng điểm câu theo cấu hình tại 3.10/3.14. Khi học toán, tiêu chí lập luận có thể khác điểm mô phỏng. Điểm mô phỏng và dữ liệu chẩn đoán phục vụ hai mục đích khác nhau. Những mã đề chỉ đổi số hoặc hoán vị có thể cùng họ câu; không tính bốn mã 0101–0104 năm 2025 thành bốn phép đo tiến bộ độc lập nếu học sinh đã luyện các câu tương ứng.

### 5.2. Chọn điểm vào và học tiếp

Học sinh làm phần đầu vào trước khi mở lời giải. Câu nào cho thấy thiếu kiến thức cần trước thì quay về đúng đoạn ôn nhanh hoặc bài nền đã có, sau đó thử lại bằng một câu tương đương. Đầu vào dùng để hướng dẫn, không gắn một nhãn yếu/giỏi cố định.

| Lối vào | Phù hợp khi | Học sinh cần thực hiện |
| --- | --- | --- |
| Nền tảng | Chưa giải thích được khái niệm hoặc còn sai điều kiện | Đọc giải thích, làm ví dụ có hướng dẫn rồi thử câu mới |
| Vận dụng | Đã hiểu phần nền và tự xử lý được nhiệm vụ cơ bản | Đổi dữ kiện, nối biểu diễn, chọn công cụ cho tình huống |
| Đào sâu | Muốn làm rõ giới hạn của cách hiểu hoặc nối nhiều ý | So sánh cách giải, phản biện, thử phản ví dụ và kết nối đúng phạm vi |

Sau bài học, học sinh làm câu mới, ghi lỗi thuộc khái niệm, điều kiện, biến đổi, đọc đề, tính toán hoặc diễn đạt. Mỗi lỗi có chỉ dẫn trở lại đúng mục và một câu kiểm tra sau sửa. Chỉ gợi ý học tiếp khi những mục tiêu cốt lõi đã có bằng chứng phù hợp; không dùng một tỷ lệ đúng chung để bỏ qua lỗi ở điều kiện thiết yếu. Một em có thể vào vận dụng ở hàm số nhưng cần nền tảng ở xác suất.

### 5.3. Mã câu hỏi, lời giải và thời lượng học

Mã đề xuất: D0-R1-01 cho câu khảo sát R1; R1-G01-LT-01 cho luyện; R1-G01-KT-01 cho kiểm tra cuối; R1-G01-SL-01 cho câu sau sửa lỗi. Mã câu Bxx đã có vẫn giữ để truy nguyên khi được sử dụng lại; hồ sơ ghi thêm gói và mạch sử dụng. Mỗi câu giữ mục tiêu, mức dự kiến, nguồn/tác giả, điều kiện, đáp án, lời giải, tiêu chí xem bài làm, lỗi thường gặp và phiên bản. Khi đổi dữ kiện làm thay đáp án, tăng phiên bản câu và cập nhật các sản phẩm dùng câu đó.

Không đồng nhất bài dài với bài khó. Một câu ngắn về điều kiện có thể kiểm tra sự hiểu biết sâu; một câu tính dài có thể chỉ lặp phép tính. Phân bố câu theo mục tiêu và công dụng trước, rồi kiểm tra sự cân đối giữa đọc hiểu, thao tác, vận dụng và giải thích.

Thời gian tự học ghi theo bài nhỏ và dựa trên phạm vi đã soạn. Khi chưa thử, ghi “ước lượng thiết kế, chưa đo”; khi có học sinh thử, giữ thời gian thực học cùng mức hoàn thành. Bài rộng chia thành các điểm dừng có ý nghĩa. Không cộng các khoảng thời gian chưa kiểm chứng thành tổng thời lượng bảo đảm cho toàn khóa.

### 5.4. Đánh giá và quyết định tiến tiếp

#### 5.4.1. Đầu vào không đồng nhất với một đề thi thử

Khi dùng D0, có thể tổ chức hai lượt: khảo sát nền trên nội dung đã học, rồi khảo sát phần lớp 12 đã tiếp cận trong các mạch. Đây là cách giao nhiệm vụ từ ngân hàng v1.0, không khẳng định bộ PDF có cấu trúc hai phần thi cố định. Có thể chia thành hai lượt ngắn. Một đề 90 phút đầy đủ chỉ dùng làm số đo đầu vào khi học sinh đã học đủ phạm vi đề; nếu chưa, dùng để giới thiệu cấu trúc và ghi phần chưa học, không lấy tổng điểm đó làm năng lực chung.

Với từng mục tiêu/phần đã được khảo sát trong mạch, ghi một trong bốn trạng thái: **chưa học; đã học nhưng cần bổ sung; làm được độc lập; dùng được trong bài phối hợp**. Kèm mã câu và ngày làm. Mục tiêu điểm được ghi theo nhu cầu học sinh; tài liệu không tự gán mục tiêu 8, 9 hay 10 điểm cho tất cả.

#### 5.4.2. Quy tắc chuyển chặng

**Các ngưỡng và số lượt trong bảng là tham số C-08; áp dụng cùng giới hạn 5.6, không là cửa bắt buộc cho toàn mạch hoặc toàn lộ trình.**

| Dấu hiệu quan sát | Quyết định vận hành |
| --- | --- |
| Một mục tiêu cơ bản được làm đúng trên ít nhất 80% lệnh hỏi trong hai cụm bài mới, cách nhau khoảng một tuần; không còn sai điều kiện cốt lõi | Giảm luyện riêng; thử phối hợp phù hợp và duy trì, chưa tự chứng nhận đã chuyển giao |
| Biết phương pháp, còn tính sai hoặc quá chậm | Tiếp tục mạch kế tiếp, dành phần chữa lỗi cho thao tác cụ thể |
| Sai khái niệm, sai miền, đảo điều kiện hoặc không chọn được phương pháp ở nhiều câu tương tự | Bổ sung đúng kiến thức cần trước, rồi thử lại bằng câu mới; tạm giảm bài khó liên quan |
| Một phần chưa học | Xếp lại lịch ôn phần đó theo tiến độ học; giữ trạng thái riêng |
| Điểm đề tăng nhưng câu cũ đã được xem lời giải | Không dùng mức tăng này làm bằng chứng sẵn sàng; kiểm tra bằng đề/câu mới |
| Ba đề mới gần nhất đạt mức điểm hướng tới, thời gian phù hợp và lỗi trọng yếu đã được kiểm tra lại | Chuyển trọng tâm sang duy trì và ổn định trước thi |

Ngưỡng 80% áp dụng cho cụm mục tiêu có đủ câu đại diện, không phải “đúng 8/10 bất kì là đạt cả chuyên đề”. Khi một mục tiêu chỉ có một câu khảo sát, phải thêm bằng chứng trước khi kết luận. Kết quả ba đề không bảo đảm điểm thi thật; nó phục vụ quyết định phân bổ thời gian.

#### 5.4.3. Mỗi bài đánh giá phải trả lại thông tin gì?

| Trường theo dõi | Cách ghi để có thể hành động |
| --- | --- |
| Phạm vi đã học | Ghi rõ phần chưa học; không trộn vào tỉ lệ sai của phần đã học |
| Điểm | Điểm toàn đề và từng phần theo thang đang áp dụng |
| Mục tiêu toán | R1–R8, kèm mục tiêu cụ thể; câu nhiều mạch có mã chính và mã hỗ trợ |
| Loại lỗi | Đọc đề; khái niệm; điều kiện; chọn phương pháp; biến đổi/tính; đơn vị/làm tròn; thao tác trả lời; thời gian |
| Câu đúng nhưng đoán | Ghi riêng và yêu cầu giải thích hoặc thử câu tương đương |
| Thời gian | Câu làm quá lâu, câu bỏ và câu biết làm nhưng chưa kịp |
| Việc sửa | Tối đa hai ưu tiên cho lượt tiếp theo; mỗi ưu tiên có câu thử lại và ngày kiểm tra |

Khi phân tích phần đúng/sai, vừa ghi điểm của cả câu theo quy định, vừa ghi từng ý đúng/sai để chẩn đoán. Không chấm mỗi ý cố định 0,25 điểm. Các dạng trả lời không được gán cứng thành “phần dễ”, “phần trung bình”, “phần khó”; độ khó nằm ở nhiệm vụ cụ thể.

### 5.5. Từ nghiên cứu đến hoạt động trong gói học liệu

Các cách làm dưới đây là **thiết kế C-04…C-08**, được gợi bởi các nguồn B tại 3.13 và yêu cầu đánh giá tại CT tr.116–117. Bảng không phải trích nguyên văn một công trình.

| Cơ chế | Hoạt động ZO Math thiết kế | Bằng chứng quan sát và cách điều chỉnh |
| --- | --- | --- |
| Luyện nhớ lại — retrieval practice | Trước khi mở bài/lời giải, tự viết điều kiện, dựng bảng dấu hoặc giải thích lựa chọn công cụ; sau đó đối chiếu | Giữ bài trước hỗ trợ; nếu không bắt đầu được do chưa học, chuyển sang giải thích và ví dụ có hướng dẫn |
| Luyện tập giãn cách — spacing/distributed practice | Đưa mục tiêu trở lại ở ngày hẹn; tự làm trước khi xem lại nguồn | Ghi ngày thật và mức hỗ trợ; khi sai lại, đưa lượt sửa gần hơn; khi vững, giảm câu lặp nhưng vẫn giữ hẹn duy trì |
| Luyện xen kẽ — interleaving | Sau khi đã có nền tối thiểu, trộn các loại nhiệm vụ cần lựa chọn khác nhau, bỏ nhãn báo sẵn cách giải | Xem có tự chọn đúng công cụ không; nếu chỉ đoán hàng loạt, thu hẹp loại bài, thêm cặp ví dụ so sánh rồi thử lại |
| Đánh giá vì sự tiến bộ — formative assessment | Thu một bằng chứng ngắn, quyết định đổi nhiệm vụ/giải thích, cho học sinh thực hiện rồi xem lại | Một bài kiểm tra chỉ có điểm mà không làm thay đổi hành động chưa hoàn tất vòng đánh giá vì sự tiến bộ |
| Phản hồi và sửa lỗi — feedback | Nói rõ bước đã đúng, bước sai, điều kiện cần kiểm, việc cần làm tiếp; giữ câu mới sau sửa | Không suy nguyên nhân từ đáp số; yêu cầu thêm lập luận khi chưa phân biệt lỗi. Phản hồi xong mà học sinh chưa thử lại thì vẫn ghi “chưa xác nhận sửa” |
| Học đến mức làm chủ — mastery learning | Mục tiêu nhỏ, tiên quyết rõ, hỗ trợ khác cách cũ, kiểm tra lại; phân biệt đủ vào việc kế tiếp với duy trì và phối hợp | Chỉ tạm chặn nhiệm vụ phụ thuộc vào tiên quyết chưa đủ; tiếp tục nhánh độc lập. Không đợi “vững toàn mạch” mới được học mạch khác |

Ví dụ gói R1-G01: tự nhớ dấu đạo hàm có ý nghĩa gì; xem một ví dụ có hướng dẫn nếu cần; luyện riêng đủ để tự làm; rồi so sánh trường hợp đạo hàm bằng 0 có đổi dấu và không đổi dấu. Lượt sau trộn cực trị với giá trị lớn nhất/nhỏ nhất **chỉ khi đã học mục tiêu tương ứng**. Yêu cầu giải thích trước khi xem lời giải và trả lại bằng một bảng/đồ thị mới. Đây là thiết kế bài, không phải thí nghiệm chứng minh hiệu quả.

### 5.6. Tiến tiếp có điều kiện và giới hạn thời gian sửa

**C-08:** bốn trạng thái học vẫn giữ, nhưng gắn với **mục tiêu/phần đã khảo sát**, không gắn nhãn toàn học sinh. Thêm cột “chưa có/không đủ bằng chứng”; cột này là tình trạng dữ liệu, không phải trạng thái năng lực thứ năm. “Đã học nhưng chưa được giao” không đồng nghĩa “cần bổ sung”.

Phân biệt ba quyết định: **đủ điều kiện vào nhiệm vụ kế tiếp**, **giảm luyện riêng và chuyển duy trì**, **dùng được trong phối hợp mới**. Quy tắc 80% ở 5.4.2 chỉ hỗ trợ quyết định thứ hai trên một cụm mục tiêu đủ đại diện; không tự quyết định cả ba. Không đòi đạt 80% mọi bài trước khi học tiếp một nhánh độc lập.

Khi dùng ngưỡng, ghi tử số/mẫu số, tiêu chí nào thiết yếu, ngày và tính mới/độc lập của bài. Hai cụm phải cùng đại diện mục tiêu, không cần có cấu trúc kỳ thi. Một đúng/sai bốn ý phụ thuộc cùng ngữ cảnh không tạo bốn quan sát độc lập. D0 và câu SL cùng họ là bằng chứng sửa lỗi hẹp, không tự đủ để xác nhận chuyển giao.

Nếu chưa đạt: xác định tiên quyết bị thiếu; thay cách hỗ trợ bằng ví dụ, biểu diễn hoặc câu hỏi gợi ý phù hợp; dành phần chữa đã dự trù; thử lại. Nếu dùng hết quỹ giờ sửa của tuần mà lỗi vẫn còn, **không lặp vô hạn cùng một phiếu**: ghi mục tiêu chưa đạt, giảm nhiệm vụ khó phụ thuộc, chuyển phần độc lập, hẹn hỗ trợ riêng và tính lại lịch. Không xóa mục tiêu khỏi sổ độ phủ để làm đẹp tiến độ.

Một tuần sau là mốc mặc định thử duy trì, không phải điều kiện nghiên cứu bắt buộc. Nếu ngày thi hoặc lịch học không cho phép, ghi mốc rút ngắn và chỉ kết luận ở độ trễ thực đã đo; không đổi nhãn một kết quả trong ngày thành ghi nhớ bền vững.

### 5.7. Sổ độ phủ và cách đánh giá tham số vận hành

Mỗi mục tiêu theo dõi riêng: **có vị trí trong CT/B; có học liệu đã kiểm tra; đã được học sinh học; có bằng chứng độc lập; có bằng chứng sau khoảng trễ; có bằng chứng phối hợp**. Không gộp các trạng thái này thành một ô “đã xong”. D0 là phép lấy mẫu để chọn điểm vào, không phải giấy chứng nhận bao phủ B01–B42.

Hằng tuần ghi bài mới làm độc lập, thời gian thực, lỗi tái diễn và mục tiêu đến hạn ôn. Sau mỗi gói, xem tham số nào gây quá tải, chặn tiến độ hoặc thiếu bằng chứng; thay **một tham số có lý do** rồi theo dõi. Đây là cải tiến vận hành, không phải thử nghiệm nhân quả: điểm tăng có thể do học ở trường, khác độ khó, quen câu hoặc nhiều yếu tố khác.

Không ấn định cỡ mẫu “đủ chứng minh” khi chưa có thiết kế nghiên cứu. Với dữ liệu ban đầu, báo số học sinh, phần đã học, số nhiệm vụ, ngày, mức hỗ trợ và giới hạn; không suy một lớp nhỏ thành bằng chứng hiệu quả toàn chương trình.

## 6. Tổ chức Notebook

### 6.1. Bắt đầu theo công việc thực tế

D0 v1.0 đã được chuẩn bị và kiểm tra; bộ khảo sát này không đòi tạo một notebook riêng. Giữ thành phẩm hiện hành theo 11.6; phần sửa sau này được đọc và tự giải kiểm tra trước khi dùng. Khi cần nghiên cứu một điểm toán trong D0, chọn đúng phần nguồn và áp dụng quy trình nghiên cứu ở mục 7.

Notebook nội dung đầu tiên phục vụ **R1-G01 — Kết nối đạo hàm, bảng biến thiên và đồ thị**. Tên dự kiến: `ZO Math · Ôn thi 2027 · R1-G01 · Đạo hàm và đồ thị`. Sổ có thể chứa nhiều phiên nghiên cứu và các phần nguồn ở nhiều lớp. Kế hoạch này giữ quyết định điều phối; không cần tạo hàng loạt sổ trống.

### 6.2. Đầu vào của notebook R1-G01

1. Phiếu mục tiêu gói, vị trí tuần 2–4 trong lộ trình và những thiếu hụt quan sát từ D0 nếu đã có học sinh làm.
2. CT tr.95–96, 105–107; phần nền tr.80–81, 92–93 khi câu hỏi nghiên cứu cần.
3. S12.1 Bài 1 và phần liên quan của Bài 4; S11.2 Bài 31–32; S10.2 Bài 15, 17 và S11.1 Bài 16–17 được gọi vào đúng nhu cầu. Hồ sơ phiên phải xác nhận trang in/PDF thực dùng trước khi nạp.
4. Một nhiệm vụ nối đạo hàm–bảng biến thiên–đồ thị để nghiên cứu, kèm các mục tiêu gói ở 11.2 và chỉ dẫn D.1–D.2.

Phạm vi phiên đầu do câu hỏi ôn quyết định, không phải nạp toàn bộ danh sách rồi yêu cầu tạo thành phẩm. ChatGPT đọc và chuẩn bị phần nguồn truy cập được. Nội dung ZO Math dùng lại chỉ đưa vào sau khi đọc đúng bản hiện hành. Không cần chờ đủ SGV, SBT hay tài liệu NCTM để bắt đầu.

Nguồn câu hỏi nạp vào sổ được lấy từ phần đề đã tách, có năm/lần/mã và trang gốc. Không nạp kèm bảng đáp án hay lời giải AI bên ngoài. Phép thử nguồn gồm đọc đúng một công thức có điều kiện, một hình/bảng và một giả thiết chung của cụm câu; phần tự giải được kiểm riêng theo 9.9. Sau nghiên cứu, bản kết tinh ZO Math đã kiểm tra mới là nguồn sản xuất bổ sung.

### 6.3. Kiểm tra khả năng đọc nguồn

Sau khi nạp, người chủ trì thực hiện phép thử ngắn do ChatGPT chuẩn bị:

1. Mở nguồn, xác nhận đúng sách, phần nội dung và phiên bản.
2. Yêu cầu Notebook chỉ một đề mục ở đầu, một chi tiết ở giữa và một chi tiết ở cuối phần đã nạp.
3. Yêu cầu đọc một định nghĩa có điều kiện, một công thức và một hình/bảng quan trọng nếu phần học có chúng.
4. Mở các chỉ dẫn nguồn, đối chiếu trực tiếp với trang sách; ghi vị trí và lỗi nếu có.
5. Nếu đọc sai, cung cấp lại phần nguồn rõ hơn hoặc bản diễn giải đã kiểm tra có dẫn trang gốc; thử lại đúng vùng lỗi trước khi dùng để sản xuất.

Phép thử xác nhận khả năng sử dụng phần nguồn đã thử, không bảo đảm mọi trang đều đọc đúng. ChatGPT đọc được PDF trong cuộc trò chuyện không có nghĩa Notebook đã nhận và đọc đúng nó. Công thức và hình thực sự đưa vào sản phẩm vẫn phải được kiểm tra riêng.

Google giải thích rằng nhập một trang web không tự nhập các trang con hoặc nội dung nhúng; nguồn nhập có giới hạn và cách cập nhật riêng. Vì vậy, cần kiểm tra nội dung thật sau khi nạp thay vì chỉ nhìn thấy tên nguồn. [Trợ giúp Google về nguồn](https://support.google.com/gemininotebook/answer/16215270?hl=en).

### 6.4. Giữ những điều đã làm rõ

Cuối phiên, tạo một bản tổng hợp phân biệt: nội dung nguồn; diễn giải đã kiểm tra; ví dụ mới; quyết định dùng cho bài học; câu hỏi chưa giải quyết. Ghi mã và phiên bản, ví dụ `R1-G01-noi-dung-v0.1`.

Google có chức năng lưu phản hồi thành ghi chú và chuyển ghi chú thành nguồn. Kế hoạch dùng khả năng đó để đưa bản tổng hợp đã sửa vào đầu vào sản xuất; kiểm tra tên bản và nội dung trước khi chọn. Tệp xuất ra ngoài không được mặc định đồng bộ ngược với ghi chú. [Trợ giúp Google về ghi chú](https://support.google.com/gemininotebook/answer/16262519?hl=en).

Đây là cách mang kết quả trao đổi sang Studio có thể kiểm tra được. Không chỉ viết “hãy dùng toàn bộ ngữ cảnh” rồi mặc định công cụ đã dùng đủ và đúng.

### 6.5. Gói đầu vào và quản lý thay đổi giữa các sổ

Ngoài phần chương trình và SGK, mỗi notebook có hồ sơ mục tiêu, kiến thức cần trước, chỉ dẫn viết, câu hỏi đang nghiên cứu và sản phẩm được chọn. Nội dung ZO Math dùng lại chỉ thêm sau khi kiểm tra. Bản kết tinh mới nhất trở thành nguồn cho sản xuất sau bước học, không được mặc định đã có ngay khi mở sổ.

Khi sửa một nguồn làm việc, ghi mã, bản cũ–mới và đoạn thay đổi; xác định các sổ và sản phẩm đã dùng đoạn đó. Nạp hoặc cập nhật theo khả năng thực tế của công cụ rồi thử đọc lại đúng phần thay đổi. Với sản phẩm đã tạo, ghi cần sửa, đã sửa và đã kiểm tra lại riêng biệt. Không coi sửa tệp ngoài sổ là mọi đầu ra đã tự cập nhật.

Chỉ mở thêm sổ khi có phạm vi và nguồn rõ. Có thể đưa bản tóm tắt kiến thức cần trước đã kiểm tra từ R1-G01 sang gói kế tiếp, nhưng giữ mã nguồn và phiên bản. Nếu sau này cần sổ điều phối để hỏi đáp toàn cảnh, sổ đó chỉ là bản hỗ trợ tra cứu; kế hoạch và hồ sơ bên ngoài vẫn giữ quyết định chính. Chưa cần tạo sổ điều phối trong bước đầu.

## 7. Quy trình nghiên cứu và sản xuất cho nhiệm vụ ôn thi

Trước bước 1, chọn một mục tiêu từ mạch R và gói đang làm; xác định câu hỏi cần nghiên cứu để giải thích và luyện mục tiêu ấy. Quy trình dưới đây giữ cách học sâu của người chủ trì và gắn kết quả với vị trí ôn của học sinh.

| Bước | Việc thực hiện | Đầu ra cụ thể |
| --- | --- | --- |
| 1. Trích xuất bài học | Giao Notebook tổ chức nội dung của phiên từ nguồn đã chọn: khái niệm, điều kiện, lập luận, ví dụ, câu hỏi và chỉ dẫn nguồn | Bản bài học để người chủ trì bắt đầu đọc; ghi điểm đọc chưa chắc |
| 2. Học và nghiên cứu | Người chủ trì đọc, tự giải, đặt câu hỏi, thử trường hợp và trao đổi; có thể yêu cầu gợi ý trước lời giải | Bài làm, câu hỏi, phát hiện, chỗ cần sửa; bản ghi nếu đang ghi hình |
| 3. Kết tinh nội dung | Tổng hợp kết quả trao đổi, kiểm tra lại với nguồn và tự giải; chia phần đã rõ và phần còn mở | Bản nội dung có phiên bản, đủ làm nguồn cho những sản phẩm sắp tạo |
| 4. Sản xuất và tinh chỉnh | Tạo học liệu lõi và sản phẩm Studio phù hợp; kiểm tra, sửa bản gốc và đầu ra liên quan | Thành phẩm có hồ sơ kiểm định; còn lỗi nào ghi rõ lỗi đó |
| 5. Đóng gói chờ xuất bản | Tập hợp đúng các bản đã kiểm định, ghi mục tiêu, phiên bản, nguồn và cách sử dụng | Gói sẵn để người chủ trì xem và duyệt công bố |

Đây là chu trình có thể quay lại. Nếu bước 4 phát hiện một định nghĩa chưa rõ, trở lại bước 2–3 rồi tạo lại phần bị ảnh hưởng. Một phiên có thể dừng ở bước 2, không buộc làm đủ năm bước trong cùng một lần ngồi học. Sau bước 5 là công việc xuất bản theo mục 13.

### 7.1. Câu hỏi giúp học thấu đáo

Với mỗi ý quan trọng, cố gắng trả lời: đối tượng đang nói đến là gì; điều kiện nào cần; vì sao phát biểu đúng; có thể nhìn qua biểu diễn khác không; trường hợp nào làm cách hiểu thông thường sai; học sinh cần tự làm gì để cho thấy đã hiểu.

Khi bế tắc, yêu cầu một gợi ý vừa đủ rồi tự làm tiếp. Sau khi đã xem lời giải, thử một câu mới hoặc tự trình bày lại mà không nhìn bản giải. Sự trôi chảy của câu trả lời AI không thay cho việc tự lập luận.

### 7.2. Bản đồ tư duy dùng xuyên suốt

Mind Map (bản đồ tư duy) có thể dùng đầu phiên để nhìn toàn cảnh, giữa phiên để chọn nhánh có liên hệ, cuối phiên để ôn lại. Google hỗ trợ mở nhánh và chọn nút để hỏi tiếp trong trò chuyện. [Trợ giúp Google về Mind Map](https://support.google.com/gemininotebook/answer/16212283?hl=en).

Học nhảy cóc được phép: chọn câu hỏi đang cần, rồi quay lại phần nền thực sự thiếu. Ghi câu hỏi đang tạm gác để không mất mạch. Sơ đồ không tự chứng minh quan hệ tiên quyết và không thay thế bài tập kiểm tra; các mũi nối quan trọng vẫn phải được giải thích bằng toán.


### 7.3. Ghi lại quá trình học và biên tập video

Trước phiên có ghi hình, chọn một câu hỏi trung tâm, mở đúng phần nguồn, thử một đoạn ngắn để kiểm tra âm thanh và cỡ chữ. Người chủ trì học và tự giải theo mạch thật; ghi hình phục vụ lưu lại những quyết định đáng chia sẻ, không tạo áp lực phải hiểu ngay hoặc trình diễn liên tục.

| Thời điểm | Việc cần giữ | Cách dùng sau phiên |
| --- | --- | --- |
| Mở đầu | Câu hỏi, kiến thức đang có và phần chưa rõ | Giúp người xem hiểu lý do nghiên cứu |
| Trong lúc học | Một lập luận, ví dụ, phản ví dụ hoặc cách biểu diễn có giá trị | Làm phần giải thích chính |
| Khi phát hiện lỗi | Điều đã nghĩ, bằng chứng cho thấy chưa đúng, cách sửa | Cho thấy kiểm chứng và thay đổi cách hiểu |
| Khi quyết định biên tập | Vì sao đổi ví dụ, thêm điều kiện hoặc đổi thứ tự bài | Kết nối nghiên cứu với học liệu thành phẩm |
| Kết thúc | Điều đã làm rõ, điều còn mở, mã nội dung và điểm dừng | Tạo nhật ký và chỉ dẫn phiên tiếp theo |

Đánh dấu mốc thời gian trong lúc làm hoặc ngay sau phiên. Khi biên tập, giữ một mạch suy nghĩ có thể theo dõi, bỏ thời gian chờ và thao tác tệp không giúp hiểu toán. Đoạn trình bày lại sau nghiên cứu được nói rõ là trình bày lại. Video có mô tả, các mốc chính, nguồn và liên kết về đúng trang học khi URL đã có.

Theo dõi riêng giờ làm việc, thời lượng ghi hình thô, thời lượng video biên tập và thời gian học sinh tự học. Ghi hình diễn ra trong lúc nghiên cứu không được cộng thêm lần nữa vào giờ lao động. Độ dài video theo câu hỏi đã chọn và khả năng theo dõi, chưa đặt định mức phút cho mọi bài.

### 7.4. Khi có lỗi hoặc phiên bị gián đoạn

| Tình huống | Xử lý ngay | Điều kiện tiếp tục |
| --- | --- | --- |
| Chưa hiểu một ý cốt lõi | Quay lại nguồn, ví dụ và lập luận; ghi đúng câu hỏi đang vướng | Nội dung được làm rõ đủ cho phạm vi sắp dùng |
| Sai toán | Đánh dấu phần bị ảnh hưởng, sửa bản nội dung rồi rà các sản phẩm liên quan | Có bản sửa và kết quả kiểm tra lại |
| Lỗi trình bày | Sửa đúng vùng lỗi, xem lại thành phẩm | Hình/công thức đọc được và không đổi nghĩa |
| Thiếu nguồn | Ghi chính xác đoạn cần tìm; tiếp tục phần độc lập có đủ căn cứ | Phần còn thiếu được cung cấp và đối chiếu trước khi dùng |
| Hết hạn mức hoặc mất phiên | Lưu tệp mới nhất, điểm dừng, điều đã kiểm tra và việc kế tiếp | Phiên sau đọc hồ sơ và kiểm tra đầu ra đã có, tiếp tục từ đó |
| Câu hỏi vượt phạm vi | Ghi câu hỏi và liên hệ; tạm gác nếu không ảnh hưởng tính đúng đắn của bài đang làm | Quay lại khi có mục tiêu riêng hoặc khi bài hiện tại cần |

Cuối phiên phải có một bản lưu được và một việc kế tiếp. Nếu chưa tạo được thành phẩm, ghi đúng đó là bản nháp, ghi chú hay câu hỏi; không chuyển trạng thái chỉ bằng một lời thông báo. Mẫu nhật ký tại D.7 có nơi dừng và việc không cần làm lại.

## 8. Hệ học liệu và vai trò của Studio

### 8.1. Lõi của mỗi gói ôn

Lõi thể hiện các hoạt động và giới hạn tại 5.5–5.7: tự làm trước lời giải, gọi lại, lựa chọn công cụ, phản hồi và thử lại. Số câu/lượt là thiết kế C theo ma trận, không chỉ thêm tên nghiên cứu vào mô tả gói.

| Thành phần | Nội dung cần có |
| --- | --- |
| Chỉ dẫn bắt đầu | Mục tiêu, kiến thức cần trước, chỗ ôn lại, phần chính và phần đào sâu |
| Bài học tự đọc | Khái niệm, điều kiện, lập luận, ví dụ, phản ví dụ, hình/bảng có giải thích |
| Bài tự luyện | Câu hỏi theo mục tiêu, có chỗ để tự làm, chưa hiện đáp án |
| Lời giải | Cách chọn hướng giải, từng bước cần thiết, điều kiện, đáp số và lỗi dễ mắc |
| Tự kiểm tra | Nhiệm vụ đầu vào, câu hỏi trong bài, bài mới cuối bài và hướng sửa lỗi |
| Hồ sơ nguồn và phiên bản | Mã nguồn, trang, bản nội dung đã dùng, thay đổi và tình trạng kiểm định |

Các thành phần có thể nằm trong cùng một bài học hoặc vài tệp liên kết, không phải sáu tệp bắt buộc. Phần lời giải được đặt để người học có thể chủ động mở sau khi tự làm.

### 8.2. Sản phẩm bổ trợ được chọn theo mục tiêu

| Sản phẩm | Dùng khi | Điều cần kiểm tra |
| --- | --- | --- |
| Cẩm nang/báo cáo | Cần tổ chức nội dung thành bài tự đọc có mạch | Không chỉ tóm tắt; đủ điều kiện, ví dụ, luyện và chỉ dẫn |
| Bản đồ tư duy | Cần thấy cấu trúc, liên hệ, chọn điểm vào hoặc ôn lại | Đúng quan hệ khái niệm; không bỏ điều kiện làm đổi nghĩa |
| Bản trình bày | Cần lần lượt quan sát các biểu diễn hoặc lập luận | Công thức, hình và thứ tự giải thích; chữ đủ đọc |
| Đồ họa thông tin | Cần đối chiếu một số ý hoặc nhắc lại kiến thức | Không rút gọn đến mức sai; có đường dẫn tới giải thích đầy đủ |
| Âm thanh | Cần ôn ý nghĩa, câu hỏi hoặc bối cảnh bằng lời | Phát âm thuật ngữ, đọc biểu thức, khả năng hiểu khi không nhìn hình |
| Video giải thích | Cần dẫn mắt qua hình, bảng, đồ thị hay ví dụ | Đúng từng khung quan trọng, lời nói khớp hình, nhịp đủ theo dõi |
| Thẻ ghi nhớ | Cần tự nhớ khái niệm, điều kiện hoặc mối liên hệ ngắn | Không biến thành học thuộc công thức thiếu giả thiết |
| Bài trắc nghiệm tương tác | Cần tự kiểm tra và nhận phản hồi | Mỗi đáp án, cách chấm và lời giải; không mặc định bằng định dạng đề thi |

Các nhóm sản phẩm này được Google liệt kê trong hệ trợ giúp Notebook; lựa chọn và cách phối hợp ở đây là thiết kế của ZO Math. Khả năng xuất tệp hoặc sửa trực tiếp được kiểm tra trên công cụ thực tế lúc làm, không hứa trước một định dạng chưa thử. [Trợ giúp Gemini Notebook](https://support.google.com/gemininotebook/?hl=en).

Đánh giá được thiết kế ngay từ lúc chốt mục tiêu và sử dụng trong suốt quá trình học. Không cần chờ làm xong slide, âm thanh và video mới tạo câu hỏi kiểm tra. Một bộ không bắt buộc có đủ mọi định dạng.

**Cho gói đầu tiên R1-G01:** thử một sơ đồ liên hệ đạo hàm–biến thiên–đồ thị và một bài tự kiểm tra ngắn từ Studio, bên cạnh lõi bài ôn. Kiểm tra cả nội dung lẫn cách chấm; D0 v1.0 là thành phẩm riêng đã hoàn tất theo trạng thái 11.6. Video giải thích hoặc âm thanh dài không là điều kiện hoàn thành gói. Bản ghi quá trình nghiên cứu được quản lý riêng.

### 8.3. Đầu vào sản xuất

Mỗi lần tạo một sản phẩm cần chỉ rõ: mã bộ; phiên bản nội dung đã kiểm tra; người học; mục tiêu sản phẩm; nguồn đang chọn; phần bắt buộc giữ; hình/công thức cần dùng; cách kiểm tra sau khi tạo. Nếu cần lấy ý từ phiên trao đổi, đưa ý đó vào bản tổng hợp ở bước 3 trước.

Một quy chuẩn viết chung giữ thuật ngữ, giọng văn và cách trình bày. Không gọi việc nạp quy chuẩn là huấn luyện lại mô hình và không hứa sẽ đồng bộ tuyệt đối. Quy chuẩn thương hiệu lấy từ ZO Math hiện hành khi đã đọc; không mặc định xanh dương–cam là màu đã được người chủ trì chọn.

### 8.4. Cấu trúc học sinh nhìn thấy

D0 dùng cấu trúc khảo sát–phân tích–chỉ dẫn ôn ở 11.1. Bảng dưới áp dụng cho gói ôn nội dung. Đề toàn phạm vi dùng cấu trúc đề–lời giải–phân tích–câu sau chữa tại 12.5.

| Phần trên trang học | Nội dung và hành động của học sinh |
| --- | --- |
| Bắt đầu ở đây | Đọc mục tiêu, kiến thức cần trước, cách chia phiên và các sản phẩm sẽ dùng |
| Kiểm tra đầu vào | Tự làm rồi đối chiếu; mở đúng phần ôn nhanh nếu thiếu nền |
| Nhiệm vụ ôn và phần nền liên quan | Thử nhiệm vụ, gọi đúng giải thích/khái niệm/điều kiện khi cần; người đã vững có thể đi tiếp |
| Luyện vận dụng | Làm phiếu chưa hiện đáp án; ghi lập luận và điều kiện |
| Mở lời giải | Đối chiếu cách chọn hướng, biến đổi và đáp số; xác định kiểu lỗi |
| Tự kiểm tra cuối | Làm câu mới, đọc chỉ dẫn quay lại đúng mục nếu chưa đạt |
| Đào sâu và học tiếp | Chọn câu hỏi hoặc bài liên hệ theo mục tiêu; phần vượt phạm vi được ghi rõ |
| Sản phẩm hỗ trợ và quá trình sáng tạo | Biết sơ đồ, video hoặc thẻ dùng ở lúc nào; có đường về bài học chính |

Trang học và phiếu phải dùng được khi chưa xem video quá trình. Mỗi sản phẩm phụ cần một lời chỉ dẫn ngắn về mục đích và cách dùng. Khi video biên tập ra sau, ghi “đang chuẩn bị” và bổ sung liên kết khi có; không đặt một nút tải chưa hoạt động.

### 8.5. Kiểm tra thành phẩm theo định dạng

Phiếu tự luyện tải được không để lộ sẵn đáp án; bản lời giải đủ để tự kiểm tra. Trang web cần đọc được trên máy tính và điện thoại. Tệp PDF phải được mở và xem công thức, hình, ngắt trang và vùng viết bài; bản dự kiến để in cần thử ở khổ in đã chọn. Với âm thanh hoặc video, nghe/xem phần thực tế cần kiểm tra và ghi đúng phạm vi đã xem, không suy từ kịch bản sang kết luận thành phẩm đúng.

Nếu một định dạng không thể biểu đạt rõ một ý toán, sửa cách diễn đạt hoặc dùng sản phẩm khác trong cùng bộ có tác dụng phù hợp. Không cố nhét hình học cần quan sát vào âm thanh thuần lời chỉ để đủ danh sách sản phẩm. Nội dung mới xuất hiện khi tạo sản phẩm phải quay lại kiểm định và được ghi vào bản nội dung nếu quyết định sử dụng.

## 9. Kiểm định và vòng chỉnh sửa

### 9.1. Kiểm tra nội dung toán

Giải lại bài từ đề; kiểm tra định nghĩa, giả thiết, miền xác định, điều kiện dùng công thức, trường hợp biên và nghiệm ngoại lai. Xem tính duy nhất của đáp án, quy tắc làm tròn và đơn vị. Đối chiếu hình/bảng với công thức và lời giải. Với đúng/sai, kiểm tra riêng từng ý từ giả thiết chung.

Dùng tính toán hoặc phần mềm để tìm lỗi và đối chiếu khi thích hợp. Kết quả thử vài trường hợp không thay cho chứng minh tổng quát; hai mô hình đồng ý không tự thành bằng chứng. Trường hợp chưa chắc phải được giải quyết hoặc đưa ra khỏi phần công bố với ghi chú rõ.

### 9.2. Kiểm tra khả năng tự học

Đi qua bài như một học sinh: đọc mục tiêu, làm đầu vào, tìm chỗ bù kiến thức, học, tự luyện, mở lời giải, làm câu mới và biết nên học tiếp ở đâu. Chỗ nào phải xem video quá trình mới hiểu thì bài tự học còn thiếu.

Gắn mỗi câu với mục tiêu. Nếu một câu sai bộc lộ nhầm điều kiện cốt lõi, yêu cầu sửa và làm lại câu tương đương, dù tổng điểm đã cao. Chưa có dữ liệu thử với học sinh thì ghi rõ; việc tự kiểm tra của người biên soạn chưa chứng minh hiệu quả học tập.

### 9.3. Vòng sửa với ChatGPT

1. Người chủ trì gửi đúng sản phẩm cần xem: tệp, văn bản, ảnh trang, âm thanh hoặc video có thể đọc được; nêu phiên bản nếu đã có.
2. ChatGPT đọc và chỉ lỗi ở vị trí cụ thể, phân biệt lỗi toán, lỗi thiếu nội dung, lỗi diễn đạt và lỗi hình thức.
3. Nếu có tệp chỉnh được, ChatGPT sửa trực tiếp và kiểm tra phần đã sửa. Nếu cần làm lại trong Notebook, ChatGPT viết yêu cầu sửa cụ thể để người chủ trì đưa về sổ.
4. Nếu lỗi có từ nguồn làm việc, sửa bản nội dung gốc trước, tăng phiên bản rồi rà các sản phẩm liên quan.
5. Xem lại bản mới và ghi kết quả; không đánh dấu đã sửa chỉ vì đã viết prompt yêu cầu sửa.

Không yêu cầu người chủ trì gửi toàn bộ sổ hoặc tất cả sản phẩm cùng lúc. Nếu ChatGPT không đọc được một liên kết thì cần đúng nội dung của sản phẩm đó, không suy đoán từ tên hoặc ảnh danh sách.

### 9.4. Điều kiện đóng gói

| Nhóm | Bằng chứng cần có |
| --- | --- |
| Phạm vi và nguồn | Mục tiêu đã đối chiếu; nguồn và trang của nội dung dùng được ghi |
| Toán | Những bài nằm trong bản giao cho học sinh đã được giải kiểm tra; lỗi ảnh hưởng kết quả đã sửa |
| Tự học | Bài, phiếu, lời giải và kiểm tra khớp nhau; có đường quay lại kiến thức thiếu |
| Sản phẩm | Tệp mở được; công thức, hình, âm thanh hoặc video đã xem/nghe ở phần cần kiểm tra |
| Nhất quán | Các thành phẩm ghi đúng bản nội dung nguồn; không trộn đáp án cũ với đề mới |
| Tình trạng duyệt | Phân biệt kiểm tra của trợ lý với quyết định duyệt của người chủ trì |

Lỗi sai toán, đề thiếu dữ kiện, đáp án mâu thuẫn hoặc hình gây hiểu nhầm phải sửa trước. Tinh chỉnh thẩm mỹ nhỏ có thể để ở danh sách cải thiện nếu không ảnh hưởng học tập.

### 9.5. Kiểm tra theo loại bài tập

| Loại | Điểm phải kiểm tra |
| --- | --- |
| Nhiều lựa chọn | Giải độc lập; kiểm tra đáp án đúng và liệu phương án khác cũng đúng; phương án nhiễu có lý do |
| Đúng/sai | Xét riêng từng ý theo giả thiết chung; tránh ý sau tự dùng một ý sai làm giả thiết |
| Trả lời ngắn | Điều kiện nhận đáp số, đơn vị, độ chính xác, làm tròn và biểu thức tương đương |
| Tự luận, giải thích | Tiêu chí cho lập luận; chấp nhận cách giải khác đúng; không chỉ chấm theo từ khóa |
| Hàm số và phương trình | Miền xác định, biên, biến đổi có giữ nghiệm không, nghiệm ngoại lai và sự khớp với đồ thị |
| Hình học và tọa độ | Điều kiện tồn tại, suy biến, vectơ không, nhãn hình và phép dựng đo góc/khoảng cách |
| Thống kê và xác suất | Dữ liệu hợp lý, quy ước ghép nhóm, đơn vị, mẫu số, đồng khả năng, điều kiện độc lập hoặc xác suất điều kiện |

Giải từ đề trước khi đối chiếu đáp án soạn sẵn khi có thể. Dùng công cụ để hỗ trợ phát hiện lỗi, nhưng kết luận cuối cần lập luận phù hợp. Một kết quả do hai mô hình cùng đưa ra vẫn cần kiểm chứng.

### 9.6. Phản hồi và chỉ số theo dõi

| Nhóm | Ghi nhận thực tế | Dùng để quyết định |
| --- | --- | --- |
| Người chủ trì học được gì | Ý tự giải thích được, bài tự làm được, câu hỏi còn mở | Học thêm đúng điểm cần, sửa bản kết tinh |
| Học sinh học được gì | Bài làm, kiểu lỗi, câu mới sau sửa | Bổ sung giải thích, đổi ví dụ hoặc phần nền |
| Học liệu được dùng ra sao | Điểm dừng, khả năng tìm bài luyện, lượt mở/tải nếu có | Sửa chỉ dẫn, liên kết hoặc độ dài |
| Công sức | Giờ từng khâu, phần đang mở, thời gian chờ kiểm tra | Chỉnh lịch và giảm việc tồn |
| Chất lượng | Lỗi trước/sau công bố, mức ảnh hưởng, thời gian sửa | Cải thiện khâu kiểm định đúng loại lỗi |

Nếu chưa có học sinh thử thì ghi “chưa có dữ liệu sử dụng”. Vẫn có thể công bố bản đã đạt kiểm định nội dung và khả năng sử dụng; không lấy việc chưa có nhóm thử làm điều kiện trì hoãn vô hạn. Khi có vài phản hồi tự chọn, ghi đúng số người và bối cảnh; lượt xem hoặc lời khen không chứng minh học sinh đã tự giải được.

### 9.7. Sửa lỗi sau xuất bản

1. Ghi mã bộ/câu, phiên bản, vị trí lỗi, ngày phát hiện và nguồn phản hồi thích hợp.
2. Xác định ảnh hưởng tới đáp án, lập luận, mục tiêu học, hình hay trình bày. Lỗi làm học sinh học sai cần ưu tiên xử lý và thông tin đính chính rõ ngay tại sản phẩm bị ảnh hưởng.
3. Sửa bản nội dung chính và giải kiểm tra lại phần liên quan.
4. Cập nhật trang, phiếu, lời giải, câu hỏi tương tác và các sản phẩm phụ dùng nội dung ấy. Với video, bổ sung đính chính rõ và thay bản khi lỗi làm hỏng mạch học.
5. Tăng phiên bản thích hợp; ghi thay đổi dễ hiểu trên trang học và trong hồ sơ. Giữ dấu vết bản đã công bố.
6. Mở lại đầu ra đã sửa, kiểm tra liên kết và ghi biện pháp tránh lặp lỗi vào mẫu kiểm định.

ChatGPT không tự ghi người chủ trì đã duyệt bản sửa. Khi đã có quyền sửa/công bố trong phạm vi cụ thể thì làm theo quyền đó; nếu cần quyết định mới, chuẩn bị bản sửa cụ thể để người chủ trì xem.

### 9.8. Kiểm tra riêng đối với bộ khảo sát và đề mô phỏng

D0 phải phân biệt chưa học với đã học nhưng làm sai, không gán trình độ từ một câu duy nhất. Đề mô phỏng phải có ma trận mạch chính/hỗ trợ, quy mô và cách chấm theo 3.10; đúng/sai được kiểm tra từng ý và chấm theo cả câu. Đề đã dùng để học lời giải không dùng lại làm bằng chứng đo tiến bộ độc lập.

Với đề thật và đề tự biên soạn, tự giải từ đúng đề, năm/lần/mã và kiểm chứng theo 9.9; kiểm tra phương án nhiễu, câu trả lời ngắn, hình và quy tắc làm tròn; giữ câu mới sau chữa cho các lỗi quan trọng. Độ bao quát được kiểm theo ma trận chứ không chỉ nhìn số câu đủ 12–4–6.

Kiểm tra phiếu trả lời đúng phiên bản trước khi mô phỏng: số ô số báo danh, mã đề, phần sử dụng và quy tắc ghi kết quả. Phiếu người chủ trì gửi có sáu ô số báo danh/ba ô mã đề; thay bằng mẫu tại Phụ lục VI Công văn 1239 năm 2025, có tám ô số báo danh/bốn ô mã đề, làm căn cứ luyện hiện tại. Gói nguồn có trang hướng dẫn và hai mặt phiếu; trước mùa thi dùng đúng hướng dẫn áp dụng cho năm đó. Thời gian 90 phút bao gồm giải, ghi/tô và rà phiếu. Ghi riêng lỗi toán, lỗi đọc yêu cầu và lỗi chuyển kết quả; lỗi thao tác được thử lại bằng lượt ngắn.

### 9.9. Tự giải và kiểm chứng để tạo đáp án ZO Math

1. Đọc đề và ảnh nguồn; ghi đủ giả thiết, đơn vị, miền giá trị, quy tắc làm tròn, năm/lần/mã/câu. Nếu bản chép khác ảnh, sửa bản chép trước.
2. Tự giải từ đề, trình bày vì sao phương pháp áp dụng được; xử lý trường hợp biên, nghiệm ngoại lai, điều kiện nguyên và tính đủ của các trường hợp xét.
3. Kiểm tra bằng cách phù hợp: thế ngược, phương pháp khác, tính chính xác độc lập, đối chiếu hình hoặc vét cạn hữu hạn có mô tả phạm vi. Hai lần AI trả cùng kết quả không tự chứng minh kết quả đúng; kiểm số không thay chứng minh nếu bài cần lập luận tổng quát.
4. Kiểm từng phương án/ý, tính duy nhất và cách ghi vào phiếu. Tách kết quả chính xác với kết quả làm tròn; với tối ưu nguyên, kiểm các ứng viên khả thi và lý do đã xét đủ.
5. Ghi bằng chứng, người/công cụ kiểm và điểm còn vướng; chỉ đưa vào bản dùng chấm khi đã giải quyết mâu thuẫn. Lời giải ghi “ZO Math biên soạn”, không gọi là đáp án Bộ. Người chủ trì xem và quyết định duyệt thành phẩm theo vòng hiện hành.

Không đặt yêu cầu phải tìm bảng đáp án bên ngoài trước khi làm các bước này. Nếu sau này cần đối chiếu một mâu thuẫn cụ thể với đáp án Bộ, ghi đó là lần kiểm tra riêng; vẫn phải xác minh lập luận và đúng mã đề. Không nhập lời giải thứ sinh để thay công việc tự giải.

## 10. Lưu giữ và đóng gói

### 10.1. Một hồ sơ chung theo gói học liệu

Bổ sung liên kết nhóm H-YC/mục tiêu con, mã quyết định C và nguồn NC liên quan; đề/phiếu mô phỏng ghi mã cấu hình thi thực dùng. Lịch dự kiến và lượt học thật lưu riêng; không ghi ngày giả định thành ngày thi chính thức.

Mỗi bộ giữ năm nhóm thông tin: nội dung gốc; sản phẩm; nguồn và chỉ dẫn tạo; kết quả kiểm định; phiên bản và nơi công bố. Không để từng video, slide, phiếu nằm rời nhau mà không biết cùng thuộc gói và mục tiêu ôn nào.

Trong giai đoạn thử, dùng một hồ sơ Markdown theo bộ và một thư mục sản phẩm; không bắt người chủ trì tự tạo cả hệ nhiều tầng. Những bảng và mẫu trong kế hoạch này sẽ được ChatGPT điền dần khi triển khai, chưa phải hàng loạt tệp đã tạo.

| Nhóm | Ví dụ tên tương lai | Nội dung |
| --- | --- | --- |
| Hồ sơ | `R1-G01_ho_so.md` | Mục tiêu, nguồn, phiên bản, kiểm định, việc kế tiếp |
| Nội dung gốc | `R1-G01_noi_dung.md` | Bài học, ví dụ, mã câu hỏi và lời giải chuẩn đang dùng |
| Thành phẩm | `R1-G01_tu_luyen_v1.0.pdf` | Bản cho người học; định dạng cụ thể chọn lúc sản xuất |
| Bản ghi | `R1-G01_phien_01` | Video/âm thanh thô và mốc nội dung đáng giữ |
| Gói xuất bản | `2027_R1-G01_goi_xuat_ban_v1.0` | Đúng các bản đã kiểm định, mô tả và chỉ dẫn công bố |

Tên bảng là quy ước đề xuất, chưa phải tệp đang tồn tại. Trước khi đặt vào repo, kiểm tra cấu trúc thực tế của ZO Math. Không đưa SGK và bản ghi thô dung lượng lớn vào repo website.

### 10.2. Trạng thái công việc

| Trạng thái | Chứng cứ chuyển vào trạng thái |
| --- | --- |
| Đã định vị nguồn | Có đúng nguồn và phần cần dùng |
| Đang học/nghiên cứu | Có phiên học và câu hỏi đang xử lý |
| Đã kết tinh nội dung | Có bản tổng hợp được kiểm tra cho phạm vi đang làm |
| Đang sản xuất | Có thành phẩm nháp từ bản nội dung xác định |
| Đã kiểm định | Có kết quả kiểm tra và lỗi đã giải quyết |
| Đã đóng gói, chờ duyệt xuất bản | Có gói cụ thể, đủ thành phần đã chọn |
| Đã duyệt xuất bản | Người chủ trì đã duyệt đúng phiên bản và phạm vi công bố |
| Đã xuất bản | Có URL thật, đã mở và kiểm tra tệp/liên kết |

Khi sửa lỗi, quay lại trạng thái cần thiết cho phần bị ảnh hưởng. Giữ lịch sử bản đã công bố và bản đính chính. Không tự ghi người chủ trì đã duyệt hoặc “Human Review PASS”.

### 10.3. Danh sách thành phần trong gói

Gói ghi mã bộ, tên, mục tiêu, phiên bản nội dung; danh sách tệp kèm phiên bản; bản dành cho học sinh và bản có lời giải; nguồn; báo cáo kiểm định ngắn; mô tả trang học; mô tả sản phẩm truyền thông; chỗ cần người chủ trì quyết định; trạng thái liên kết.

URL chưa có ghi “chưa xuất bản”, không điền đường dẫn giả. Video quá trình biên tập xong sau bài học thì cập nhật bổ sung; không để cả lõi học liệu phải chờ một video chưa cần thiết cho việc tự học.

### 10.4. Bố trí hồ sơ khi đưa vào môi trường ZO Math

Các vị trí dưới đây là đề xuất trên máy người chủ trì theo cấu trúc dự án đã biết; chưa được tạo hoặc kiểm tra trong lần biên tập kế hoạch này. Khi tích hợp thực tế, đọc AGENTS.md, quy trình QMD và cấu trúc hiện hành trước khi chọn đường dẫn.

| Loại | Vị trí đề xuất | Cách sử dụng |
| --- | --- | --- |
| Hồ sơ điều phối và nguồn | `E:\zo_math_ca_nhan\on_thi_toan_thpt\` | Kế hoạch, danh mục nguồn, ma trận, tiến độ và bản làm việc |
| Nội dung công khai | `E:\zo_math\content\thpt\on_thi_toan_thpt\` | Trang chương trình, bài và tài liệu tải sau khi xác nhận cấu trúc |
| Nghiên cứu dài hạn | Hệ `_research/` hiện có trong ZO Math | Câu hỏi, nguồn và tổng hợp cần phát triển riêng |
| Bản ghi thô và tài sản lớn | Vùng dữ liệu cá nhân có dung lượng phù hợp | Giữ bản gốc, mốc biên tập và tên liên kết trong hồ sơ bộ |

Trong giai đoạn đọc kế hoạch, một tệp này chứa quyết định và các mẫu. Khi triển khai, ChatGPT chuẩn bị hồ sơ D0, rồi hồ sơ R1-G01 và thư mục sản phẩm tương ứng. Khi bảng chung đã có dữ liệu cần quản lý riêng, tách dần thành `danh_muc_nguon.md`, `ma_tran_yeu_cau.md`, `danh_muc_hoc_lieu.md`, `nhat_ky_tien_do.md`; kế hoạch giữ tên tệp hiện tại. Đây là lộ trình tổ chức, không phải yêu cầu người chủ trì tự tạo năm tệp trống ngay.

### 10.5. Phiên bản nội dung, thành phẩm và gói

Mã R1-G01 chỉ gói ôn đầu tiên thuộc mạch R1; các mã Bxx đi kèm chỉ nội dung được dùng; 2027 là ấn bản lộ trình. Phiên bản của bài toán và phiên bản của một video có thể khác nhau. Mỗi thành phẩm phải ghi nó dựa vào bản nội dung nào; một phiếu chỉ đổi trình bày không có nghĩa toàn bộ kiến thức đã chuyển phiên bản.

| Thành phần | Ví dụ tên/mã đề xuất | Điều cần truy nguyên |
| --- | --- | --- |
| Nội dung | `R1-G01_noi_dung_v1.0.md` | Mục tiêu, công thức, ví dụ, câu hỏi, lời giải |
| Phiếu | `2027_R1-G01_tu_luyen_v1.1.pdf` | Bản nội dung v1.0, những câu thực sự có trong phiếu |
| Lời giải | `2027_R1-G01_loi_giai_v1.1.pdf` | Đúng phiên bản câu hỏi tương ứng |
| Video | `2027_R1-G01_video_01_v1.0` | Bản nội dung đã dùng, ngày tạo, phạm vi đã xem |
| Gói | `2027_R1-G01_goi_xuat_ban_v1.0` | Danh sách đúng các tệp đã kiểm định, trạng thái duyệt |

Đây là ví dụ quy ước, không phải sản phẩm đã tồn tại. Khi đổi mã hoặc tách Bxx thành mã con, ghi ánh xạ cũ–mới trong hồ sơ và cập nhật ma trận, câu hỏi, sổ, trang học. Một quyết định chia lại cụm không được làm mất lịch sử lỗi hoặc nguồn.

### 10.6. Bảng thành phần gói có thể duyệt

Mỗi gói có danh sách gồm tên tệp, vai trò với học sinh, phiên bản thành phẩm, bản nội dung nguồn, kết quả kiểm tra, trạng thái duyệt và vị trí dự kiến công bố. Mẫu cụ thể ở D.13. Tệp không được chọn công bố vẫn có thể giữ trong hồ sơ nghiên cứu, nhưng không tự trộn vào gói phát hành.

Gói thủ công đầu tiên được lập để người chủ trì xem và duyệt. Tự động hóa ở mục 14 chỉ dùng các thành phần đã có thông tin duyệt để tái lập gói xuất bản; hai thời điểm này không được đảo thành yêu cầu phải tự động hóa xong mới có gói đầu tiên.

## 11. D0 hiện hành và gói ôn tiếp nối R1-G01

**D0 — Bộ khảo sát và định vị đầu vào — đã hoàn tất v1.0. Gói ôn nội dung đầu tiên cần tiếp tục là R1-G01 — Kết nối đạo hàm, bảng biến thiên và đồ thị.** Hai đầu ra này giúp thử trọn chu trình khảo sát–ôn–kiểm tra lại, đồng thời thử quy trình nghiên cứu–sản xuất–kiểm định–đóng gói của ZO Math.

### 11.1. Đặc tả D0 được giữ để vận hành và bảo trì

D0 dùng để quyết định việc ôn kế tiếp. Đầu vào gồm bảng mạch R ở 4.5, chỉ mục B ở phụ lục B, cấu trúc thi tại 3.10 và phạm vi học sinh đã học. Bộ đã có được dùng theo 11.6; khi bảo trì có căn cứ, ChatGPT chuẩn bị phần sửa và người chủ trì xem đúng phần thay đổi.

| Thành phần D0 | Quy mô và nội dung thiết kế | Đầu ra có thể dùng |
| --- | --- | --- |
| Khai báo phạm vi | Với từng R1–R8, đánh dấu phần đã học/chưa học; ghi mục tiêu điểm do học sinh lựa chọn và thời gian có thể ôn | Phạm vi câu được giao; phần chưa học giữ riêng |
| Ngân hàng khảo sát lượt đầu | Khởi điểm 24 nhiệm vụ ngắn, 3 nhiệm vụ cho mỗi R; R8 kiểm tra mô hình và lựa chọn công cụ. N được gắn trong các câu theo lỗi cần nhận diện | Bản dành cho học sinh; chỉ giao phần có kiến thức đã học, có thể chia hai lượt |
| Các mức trong một mạch | Một nhiệm vụ nhận diện/điều kiện, một nhiệm vụ thực hiện, một nhiệm vụ giải thích hoặc phối hợp vừa sức | Bằng chứng ban đầu theo mục tiêu; không suy từ ba câu ra đã vững cả mạch |
| Lời giải và tiêu chí phân tích | Giải từ đề, chỉ cách đọc sai, sai điều kiện/phương pháp/thao tác; câu đúng do đoán được thử lại | Bản người chủ trì và bản phản hồi cho học sinh |
| Câu thử lại và bổ sung | Đã có 24 nhiệm vụ thử lại v1.0; soạn thêm có mục tiêu khi bằng chứng chưa đủ phân biệt lỗi | Không gắn nhãn trình độ bằng một câu duy nhất |
| Hồ sơ đầu vào | Bốn trạng thái ở 5.4; tối đa hai ưu tiên sửa; chỉ rõ hàng lộ trình/gói ôn tiếp theo | Một kế hoạch hành động ngắn của từng học sinh |

24 nhiệm vụ là quy mô biên soạn khởi điểm, không phải đề 90 phút hay số câu mọi học sinh đều phải làm. Không chuyển số câu D0 thành điểm dự báo thi thật. Nếu chưa có học sinh thử, bộ D0 vẫn có thể hoàn thiện về nội dung và cách dùng; kết quả chẩn đoán thực tế chỉ được ghi khi có bài làm.

**Điều kiện hoàn tất D0:** câu hỏi, đáp án, lời giải và hồ sơ phản hồi khớp nhau; phân biệt đúng phần chưa học; từng kết quả dẫn đến việc ôn cụ thể; có phương án thử lại khi bằng chứng ít. D0 không cần sản phẩm Studio bổ trợ để được đưa vào sử dụng.

Khi chọn chất liệu cho D0, đề minh họa lớp 10 chỉ cung cấp một phần nền (mệnh đề/tập hợp, vectơ, lượng giác trong tam giác, bất phương trình và mô hình). Phải phối hợp CT/SGK của các lớp theo tám mạch; không dùng nguyên đề này để khảo sát toàn THPT. Giữ nhãn chưa học và lịch sử đã gặp câu. Bản ma trận đi kèm là ví dụ thiết kế cần đọc đúng bối cảnh, không phải bằng chứng ngân hàng 24 nhiệm vụ là định mức của Bộ.

### 11.2. Đặc tả R1-G01

**Câu hỏi trung tâm:** từ công thức, dấu đạo hàm, bảng biến thiên và đồ thị, học sinh suy ra được điều gì, cần điều kiện nào và dễ kết luận sai ở đâu?

**Phạm vi gói đầu:** mối liên hệ đạo hàm–biến thiên–đồ thị, đơn điệu và cực trị trong các trường hợp thuộc chương trình. Dùng B04, B06, B16–B18 và phần B21 phù hợp; giới hạn/liên tục từ B12 được gọi vào khi cần. Giá trị lớn nhất/nhỏ nhất, tiệm cận và tối ưu thuộc các gói kế tiếp của R1; không gọi R1-G01 là đã hoàn thành toàn R1.

| Mục tiêu gói | Nhiệm vụ cần biên soạn | Điểm kiểm định riêng |
| --- | --- | --- |
| R1-G01-M1: nối các biểu diễn | Ghép công thức, bảng dấu, bảng biến thiên, đồ thị; giải thích chỗ không khớp | Tập xác định, khoảng xét, nhãn trục; bảng hữu hạn không xác định toàn hàm |
| R1-G01-M2: giải thích đơn điệu | Từ dấu đạo hàm kết luận trên từng khoảng; phát hiện kết luận vượt dữ kiện | Không suy từ một vài điểm; giữ điều kiện định lí và khoảng xét |
| R1-G01-M3: xác định cực trị | Xử lý điểm đạo hàm bằng 0, đổi dấu hoặc không đổi dấu; phân biệt hoành độ, điểm và giá trị cực trị | Không đồng nhất đạo hàm bằng 0 với có cực trị; kiểm tra điểm thuộc miền |
| R1-G01-M4: xử lý đúng/sai có lý do | Từ giả thiết chung, đánh giá từng ý về đạo hàm và đồ thị; sửa ý sai | Ý sau không tự dùng một ý sai làm giả thiết; chấm cả câu đúng quy tắc |
| R1-G01-M5: tự sửa lỗi và dùng câu mới | Ghi điều kiện bị bỏ, sửa bằng nguồn hoặc phản ví dụ, rồi làm câu khác cùng mục tiêu | Câu mới thực sự kiểm tra lỗi đã sửa, không chỉ thay số máy móc |

**Nguồn:** CT tr.95–96, 105–107; S12.1 Bài 1 và phần liên quan của Bài 4; S11.2 Bài 31–32. Nền bổ sung: CT tr.80–81, 92–93; S10.2 Bài 15, 17; S11.1 Bài 16–17. Trang cụ thể của từng đoạn được xác nhận trong hồ sơ nguồn khi chuẩn bị phiên, không đoán từ số bài.

**Lõi sản phẩm:** chỉ dẫn vào gói và câu thử nền; giải thích ngắn theo nhiệm vụ ôn; phiếu luyện; lời giải; cụm kiểm tra mới; câu sau chữa; lịch ôn lại. Mỗi M1–M5 có ít nhất một nhiệm vụ luyện và một nhiệm vụ kiểm tra độc lập; những mục tiêu có nhiều trường hợp phải có thêm câu đại diện. Số câu cuối cùng theo ma trận sau khi soạn.

**Sản phẩm Studio thử:** sơ đồ liên hệ các biểu diễn và một bài tự kiểm tra ngắn, kiểm định lại từng câu và cách chấm. Bản ghi nghiên cứu của người chủ trì được chọn lọc, biên tập và liên kết về gói khi công bố.

### 11.3. Chuỗi nghiên cứu cho R1-G01

| Phiên làm việc | Trọng tâm nghiên cứu | Kết quả giữ lại |
| --- | --- | --- |
| 1 | Trích xuất đúng phần nguồn về dấu đạo hàm và biến thiên; tự giải một nhiệm vụ nối biểu diễn | Điều kiện, lập luận và chỗ dễ nhầm |
| 2 | Cực trị, các trường hợp đạo hàm bằng 0 và việc đổi dấu | Ví dụ/phản ví dụ, bài làm và lời giải đã kiểm tra |
| 3 | Đúng/sai, sửa lỗi và chuyển giao sang câu mới | Ma trận mục tiêu–nhiệm vụ, tiêu chí đánh giá |
| 4 | Kết tinh toàn gói, kiểm tra lại nguồn và giới hạn nội dung | Bản nguồn dùng cho lõi học liệu và Studio |

Một phiên có thể cần tách thêm. “Đủ sâu” nghĩa là người chủ trì tự giải thích điều kiện, tự giải nhiệm vụ đại diện, nhận ra lỗi và xác định phần còn mở; không phải giải quyết mọi câu hỏi nghiên cứu trước khi có gói đầu tiên. Đề cương chi tiết B04–B06 ở phụ lục G phục vụ những phần nền thực sự cần.

### 11.4. Mốc sản xuất khởi động và phần còn lại

Đây là bốn tuần làm việc **của người chủ trì và ChatGPT**, tách khỏi tuần ôn của học sinh ở 12.2. Không tuyển một nhóm vào toàn lộ trình rồi mặc định học liệu các tuần kế tiếp đã sẵn sàng. Có thể thử D0 và R1-G01 với phạm vi công bố rõ khi từng gói đã đủ dùng.

| Tuần sản xuất | Trọng tâm | ChatGPT chuẩn bị | Người chủ trì thực hiện | Mốc theo đầu ra |
| --- | --- | --- | --- | --- |
| 1 — đã hoàn tất | D0 v1.0 | Giữ bộ hiện hành và đính chính chỉ dẫn ở 11.6 | Dùng khi định vị học sinh | Thành phẩm đã có; không xếp lại việc soạn D0 |
| 2 | Nghiên cứu R1-G01 | Hồ sơ nguồn, phiếu giao việc, phép thử Notebook, hỗ trợ kiểm tra lập luận | Nạp phần nguồn, đọc, tự làm và trao đổi | Có nội dung cốt lõi đủ chắc để kết tinh |
| 3 | Lõi học liệu và Studio | Ma trận câu hỏi, bài ôn, phiếu, lời giải, yêu cầu tạo/sửa sản phẩm | Tạo sản phẩm đã chọn; gửi đúng bản để kiểm tra | Bản nháp đầy đủ và danh sách lỗi cụ thể |
| 4 | Kiểm định, đóng gói và tổng kết | Sửa, kiểm tra cả gói, chuẩn bị hồ sơ xuất bản và bảng giờ thực | Xem gói; duyệt đúng phiên bản nếu đạt | R1-G01 đã đóng gói; lịch sản xuất kế tiếp dựa trên công sức |

Mốc khởi động ban đầu gồm D0 và một gói R1-G01; D0 nay đã hoàn tất. Phần còn lại là nghiên cứu–lõi học liệu–kiểm định R1-G01; ba hàng 2–4 là mốc sản xuất tham chiếu, không phải ba tuần lịch bắt buộc từ ngày khóa 0.6. Nếu phải dành thêm thời gian cho một điểm toán cốt lõi, điều chỉnh ngày công bố; giảm định dạng phụ trước. Không mặc định phải có ba bộ hay phải xuất bản khi chưa kiểm định.

### 11.5. Từ gói đầu sang các gói tiếp theo

Sau R1-G01, chuẩn bị phần R1 còn cần cho chặng B.1: giá trị trên miền, tiệm cận và tối ưu phù hợp; sau đó ưu tiên R2 và R3 theo bảng 12.7. D0 giúp điều chỉnh trọng tâm từng học sinh; nhu cầu nền B04–B06 được đáp ứng bằng phiếu hoặc bộ riêng khi thực tế cần.

Tổng hợp giờ từng khâu, lỗi, sản phẩm còn chờ, phần người chủ trì cần nghiên cứu và phản hồi học sinh nếu có. Chỉ một gói đang nghiên cứu/sản xuất và một gói đang chuẩn bị nguồn. Phần nội dung tốt trong ZO Math được xem để tái sử dụng theo mục 13, không mở nhiệm vụ sửa một dự án khác.

### 11.6. D0 v1.0: thành phẩm hiện hành và tương thích 0.6

**Trạng thái căn cứ vào xác nhận hiện tại của người chủ trì:** D0 đã biên soạn, kiểm tra và đưa vào Nguồn ở v1.0. Đợt nâng kế hoạch này đã truy xuất bốn PDF: `2027_D0_hoc_sinh_v1.0.pdf`, `2027_D0_loi_giai_v1.0.pdf`, `2027_D0_huong_dan_phan_tich_v1.0.pdf`, `2027_D0_thu_lai_v1.0.pdf`. Có 24 nhiệm vụ khảo sát và 24 nhiệm vụ thử lại. Mục 11.1 giữ đặc tả và tiêu chí bảo trì; không phải lệnh biên soạn lại.

Đã rà hướng dẫn chọn câu, trạng thái, phân tích và lịch ôn; kiểm cấu trúc các bản học sinh/lời giải/thử lại. Đây không phải một vòng giải độc lập mới đủ 48 nhiệm vụ và không phải xác nhận có dữ liệu học sinh hay có phê duyệt mới của con người. Tình trạng hoàn tất hiện tại không bị đảo ngược vì một dòng trạng thái lịch sử in trong PDF.

| Điểm tiếp giáp | Quy tắc sử dụng trong 0.6 | Có cần sửa D0 ngay? |
| --- | --- | --- |
| Ba nhiệm vụ mỗi R | Là mẫu định vị; không đại diện đủ mọi B/mọi yêu cầu trong R | Không; khảo sát bổ sung khi một quyết định cần bằng chứng khác |
| CH, KCG, Đ/M/S/B; cờ đoán, trợ giúp, đã gặp, thời gian | Giữ nghĩa theo hướng dẫn D0; CH là chưa học, KCG là đã học nhưng chưa được giao; mã kết quả không tự là nhãn năng lực toàn mạch | Không |
| Hẹn thử lại, khoảng 25–40 phút một lượt | Tham số C theo người học; không bắt làm đủ ngân hàng trong 90 phút | Không |
| Ngưỡng khoảng 80%, hai cụm bài mới cách một tuần | Dùng cùng giới hạn ở 5.6; D0 và câu thử lại cùng họ chưa tự đủ chứng minh làm chủ/chuyển giao | Không |
| Tên R7 cũ có “tích lũy” | Khi tra ở kế hoạch mới, dùng tên “Nguyên hàm, tích phân và ứng dụng”; ý tưởng tích lũy còn giá trị diễn giải | Không đổi mã hoặc đáp án |
| Tên R6 cũ “Lượng giác và tính tuần hoàn” | Ánh xạ sang R6 “Hàm số lượng giác và phương trình lượng giác”; góc/công thức vẫn thuộc mạch | Không đổi mã hoặc phạm vi nhiệm vụ |
| Hướng dẫn phân tích, tr.5, R3: “tọa độ mặt phẳng ở B.8, tuần 16–17” | **Đính chính chỉ dẫn:** B.8 là tọa độ trong không gian Oxyz. Tọa độ mặt phẳng Oxy thuộc phần R3 lượt đầu B.3 | Lỗi hướng dẫn có thể dẫn sai nơi ôn: dùng đính chính này khi vận hành; ghi vào hồ sơ sửa lần bảo trì kế tiếp, giữ nguyên bộ v1.0 hiện tại |
| Tham chiếu kế hoạch 0.5 và tuần cố định | Dùng 0.6 cho điều hành; các số tuần cũ chỉ trỏ lộ trình tham chiếu 12.2; lịch cá nhân theo 12.10 | Không |

Đợt audit kiến trúc chưa phát hiện căn cứ để thay bộ D0 hoặc tạo D0 v1.1. Nếu sau này phát hiện lỗi toán/đáp án hoặc chỉ dẫn tác động thực sự, áp dụng 9.7, ghi đúng câu/trang, tác động, bản sửa và phiên bản; không sửa âm thầm. Không thêm các yêu cầu vừa được làm rõ ở H vào D0 chỉ để biến khảo sát ngắn thành bài kiểm kê toàn chương trình.

## 12. Lộ trình ôn thi toàn cảnh và điều phối sản xuất

### 12.1. Quy mô thiết kế và hai lịch làm việc

| Quyết định | Cách áp dụng |
| --- | --- |
| Quy mô lịch tham chiếu đầy đủ | 36 tuần ôn thực chất; ngày nghỉ/gián đoạn không tính là tuần đã hoàn thành; lịch cá nhân theo 12.10 |
| Mức thời gian làm việc ban đầu của học sinh | 6 giờ/tuần, gồm luyện, chữa, ôn lại và đánh giá; tương đương 216 giờ thiết kế cho cả lộ trình |
| Đối tượng vận hành ban đầu | Học sinh đang học lớp 12, đã tiếp cận chương trình lớp 10–11, có thể còn thiếu hoặc quên từng phần |
| Thứ tự | Hàm số–đạo hàm mở đầu; thống kê và hình học vào sớm; các phần học kì II được bố trí sau; mọi mạch quay lại trong lượt tổng hợp |
| Mức độ | Củng cố nhiệm vụ cơ bản trước, tăng nhiệm vụ phối hợp khi có bằng chứng làm được; không chia học sinh thành nhãn cố định |
| Đo tiến bộ | Theo từng mạch, lỗi, thời gian và bài mới; số video đã xem không dùng làm chỉ báo đạt |
| Sản lượng học liệu | Chuẩn bị theo nhu cầu các chặng; không ấn định 42 bộ hoặc một bộ cho mỗi bài SGK |

Các con số về tuần, giờ và ngưỡng đánh giá trong tài liệu là **quy tắc vận hành do ZO Math đề xuất**, không phải quy định của Bộ hoặc mức hiệu quả đã được thực nghiệm với học sinh của dự án. Chúng đủ cụ thể để triển khai và được điều chỉnh bằng bài làm thực tế.

Lịch ôn ở 12.2 dùng cho học sinh; lịch sản xuất ở 11.4 và 12.7 dùng cho người chủ trì. 216 giờ là ngân sách thời gian ôn khởi điểm, không phải cam kết hiệu quả hoặc công sức làm học liệu. Đối với lịch mùa 2027, chỉ mở chặng cho người học khi học liệu cần dùng đã sẵn sàng hoặc có nguồn thay thế đã kiểm định và hướng dẫn rõ.

### 12.2. Bảng lộ trình tham chiếu đầy đủ 36 tuần

**Toàn bộ tuần, số vòng và số đề của bảng là thiết kế C.** Đọc bảng như mẫu phủ mạch và liên kết; đặt vào lịch người học bằng 12.10. Các dạng trả lời và thời gian mô phỏng dùng cấu hình 3.14, có thể đổi mà không đổi bản đồ toán.

Tuần 1 bắt đầu khi đưa chương trình vào sử dụng. Với mùa 2027, khởi động từ tháng 9/2026; bố trí các tuần nghỉ vào lịch thực tế và giữ hai tuần cuối ngay trước kỳ thi. Khi có lịch thi chính thức, đặt mốc cuối rồi kiểm tra lại số tuần còn lại. Đây là lịch ôn bổ sung cho việc học trên lớp.

**Xử lý nội dung chưa học trên lớp:** ghi riêng “chưa học”, không chấm thành thiếu năng lực. Hoán đổi hàng ôn tương ứng với một hàng ôn lại đã học, đồng thời giữ thứ tự kiến thức cần trước. Nếu học sinh chưa được học phần nền rộng, bố trí học bổ sung ngoài phần ôn; không giả định vài câu chữa nhanh thay được cả nội dung mới.

| Chặng / tuần | Trọng tâm | Phần nền gọi vào | Ôn lại và phối hợp | Bằng chứng cuối chặng | Học liệu ZO Math cần có |
| --- | --- | --- | --- | --- | --- |
| **A · Tuần 1: Định vị đầu vào** | Khảo sát nội dung đã học; nhận diện điểm chắc, điểm quên, điểm sai và nội dung chưa học | Thử đọc điều kiện, biến đổi, dữ liệu, hình, tỉ lệ | Cho nhìn cấu trúc đề toàn cảnh; không ép làm kiến thức chưa học | Hồ sơ tám mạch; hai ưu tiên sửa đầu tiên; ghi mức điểm hướng tới theo nhu cầu thật của học sinh | **D0:** bộ khảo sát phân nhánh theo nội dung đã học, đáp án, hướng dẫn phân tích và hồ sơ đầu vào |
| **B.1 · Tuần 2–4** | **R1:** dùng đạo hàm và đồ thị; đơn điệu, cực trị, giá trị trên miền, tiệm cận | Hàm số, dấu, phương trình, giới hạn, quy tắc đạo hàm đúng chỗ vướng | R8: từ miền và hàm mục tiêu đến quyết định tối ưu; ôn nền từ D0 | Tự xử lý cụm đổi biểu diễn và bài có biên; giải thích được lỗi cực trị/GTLN | Gói R1 cơ bản, gói sửa N, cụm kiểm tra R1 và bài ôn lại |
| **B.2 · Tuần 5** | **R2:** dữ liệu không ghép/ghép nhóm; trung tâm và phân tán | Tần số, tần số tích lũy, đơn vị, quy tròn | Gọi lại R1 bằng câu ngắn; R8: chọn thước đo và đọc kết luận | Tính đúng, đọc đúng ý nghĩa; nêu được hạn chế của kết luận từ dữ liệu | Gói R2, bảng dữ liệu có kiểm tra, câu so sánh và diễn giải |
| **B.3 · Tuần 6–8** | **R3 lượt đầu:** vectơ, Oxy, quan hệ hình không gian, góc–khoảng cách–thể tích; vectơ Oxyz | Tam giác, tích vô hướng, hình chiếu, quan hệ song song/vuông góc | R1 và R2 luân phiên; R8: chọn hệ trục, chuyển hình thực tế thành mô hình | Chọn được cách giải; dựng đúng hình/biểu diễn và tính một đại lượng có đơn vị | Gói R3 hình–vectơ, phiếu cầu nối Oxy/Oxyz; câu kiểm tra có hình rõ |
| **B.4 · Tuần 9–10** | **R4 lượt đầu:** đếm, xác suất cổ điển, hợp/giao/độc lập | Tập hợp, mệnh đề, tỉ lệ; nhị thức Newton đúng phạm vi chương trình chung | R2: phân biệt xác suất với tần suất quan sát; ôn R1/R3; R8: phân chia trường hợp | Nêu rõ đối tượng đếm, trường hợp thuận lợi, kiểm tra trùng và đủ | Gói R4 đếm–biến cố, cây trường hợp, cụm sai lầm độc lập/xung khắc |
| **B.5 · Tuần 11–12** | **R5:** cấp số, giới hạn dãy, mũ–lôgarit và ứng dụng | Biến đổi, điều kiện, hàm số; tổng cấp số | R1: đồ thị và tốc độ biến thiên; ôn R2/R4; R8: tăng trưởng và thời điểm đạt ngưỡng | Chọn được mô hình tăng, giải được điều kiện/ngưỡng và kiểm tra số kì nguyên | Gói R5, phiếu phân biệt mô hình, cụm bài nối dãy số với hàm mũ |
| **B.6 · Tuần 13** | **R6:** công thức, đồ thị, phương trình lượng giác và chu kì | Góc, radian, dấu, nghiệm theo khoảng | R3: hệ thức lượng; R1: đọc đồ thị; R8: diễn giải thời điểm trong chu kì | Viết đủ họ nghiệm, lọc đúng khoảng, giữ đúng đơn vị | Gói R6 và phiếu nối lượng giác với đạo hàm/nguyên hàm |
| **B.7 · Tuần 14–15** | **R7:** nguyên hàm, tích phân và ứng dụng (diện tích, thể tích, mô hình tích lũy) | R1: đạo hàm, dấu, giao điểm; R3: mặt cắt/conic; R5–R6 khi biểu thức cần | R8: lập biểu thức trước khi bấm máy; gọi lại R2/R4 | Lập đúng tích phân, điều kiện đầu, cận và đơn vị; kiểm tra kết quả | Gói R7, phiếu đọc tốc độ–tích lũy và hình–tích phân |
| **B.8 · Tuần 16–17** | **R3 lượt tiếp:** mặt phẳng, đường thẳng, mặt cầu, góc và khoảng cách Oxyz | Vectơ, tích vô hướng, phương trình; hình không gian đã ôn | R1/R8: cực trị khoảng cách; R7: đối chiếu hình; ôn R5/R6 | Chọn được cách tổng hợp hoặc tọa độ; giữ đúng miền của đường/đoạn và đơn vị | Gói R3 tọa độ, bài nối hình tổng hợp–Oxyz, cụm kiểm tra không ghi sẵn phương pháp |
| **B.9 · Tuần 18** | **R4 lượt tiếp:** xác suất có điều kiện, toàn phần, Bayes | Biến cố, bảng hai chiều, tỉ lệ, đếm | R2: đọc dữ liệu; R8: hiểu điều kiện và đảo chiều câu hỏi; ôn R1/R7 | Lập và giải thích đúng mẫu số; không đảo lẫn hai xác suất có điều kiện | Gói R4 điều kiện; bài kiểm tra phủ các mạch đã học |
| **C1 · Tuần 19–22** | **Lượt ôn thứ hai:** nhiệm vụ trộn từ R1–R8, trọng tâm đồ thị–mô hình–dữ liệu | Sửa theo lỗi được phát hiện, không giảng lại toàn bộ mạch | Tuần 19: R1/R5/R8; 20: R2/R4/R8; 21: R3/R7/R8; 22: R6 và các điểm còn thiếu | Mỗi mạch có bằng chứng lần hai; một bài tổng hợp có giới hạn thời gian | Bộ câu trộn theo mục tiêu; bốn cụm phối hợp; một đề đánh giá giữa lộ trình |
| **C2 · Tuần 23–26** | **Lượt ôn thứ ba:** chuyển giao sang tình huống mới, ba dạng trả lời | Vá hai lỗi gây mất điểm nhiều nhất của mỗi học sinh | Tuần 23: R3/R1; 24: R7/R5/R6; 25: R4/R2; 26: R8 phối hợp toàn cảnh | Xử lý được câu mới khi bỏ tên chuyên đề; phân biệt sai phương pháp với sai thao tác | Bộ câu đổi bối cảnh, đổi biểu diễn; câu đúng/sai và trả lời ngắn có giải thích |
| **C3 · Tuần 27–28** | Hoàn tất khoảng trống; tập quyết định thứ tự làm bài | Các mục chưa học đã được học nay phải được khảo sát; các lỗi lặp được kiểm tra lại | Đề tổng hợp và các cụm chữa theo mạch | Hồ sơ sẵn sàng luyện đề; biết câu nên làm trước, quay lại sau và dừng đúng lúc | Một đề chuyển chặng, phiếu phân tích thời gian, bộ chữa theo lỗi |
| **D · Tuần 29–34** | **Luyện đề hoàn chỉnh và sửa lỗi có mục tiêu** | Chỉ ôn phần gây lỗi cụ thể sau mỗi đề | Một đề mới 90 phút mỗi tuần; chữa; làm câu mới cùng mục tiêu; kiểm tra lại sau một tuần | Sáu hồ sơ đề; điểm từng phần, thời gian, lỗi tái diễn; kết quả ba đề cuối | Sáu đề mô phỏng đã kiểm định; đáp án, lời giải, ma trận và câu kiểm tra sau chữa |
| **E · Tuần 35–36** | Củng cố trước thi, ổn định thao tác và chiến lược | Danh sách lỗi cá nhân ngắn; công thức có điều kiện đi kèm | Tuần 35 một lần mô phỏng cuối nếu còn đủ thời gian chữa; tuần 36 ôn ngắn, không dồn đề | Nhớ các điểm dễ sai, giữ nhịp làm bài và chuẩn bị đúng yêu cầu kỳ thi | Phiếu ôn cuối, checklist thao tác, đề cuối có chữa; bản cập nhật hướng dẫn thi áp dụng |

**Mốc của lịch tham chiếu:** tuần 1 có bản đồ đầu vào; hết tuần 18 có lượt ôn cơ bản của các phần đã học và danh sách phần còn thiếu; hết tuần 28 có bằng chứng phối hợp toàn cảnh; tuần 29–34 có chu trình đề–chữa–kiểm tra lại; hai tuần cuối dùng để củng cố.

Nếu một nội dung lớp 12 chưa học xong vào mốc tuần 18, đưa lượt ôn cơ bản của nó vào thời gian bổ sung đầu chặng C và giảm câu đào sâu ở mạch đã vững. Việc này là điều chỉnh lịch theo người học; không đánh dấu nội dung đó “đã phủ” trước khi có bài làm.

### 12.3. Đo công sức trước khi chốt sản lượng

Ghi riêng giờ người chủ trì dành cho: đọc nguồn/học; tự giải và trao đổi; tổng hợp; tạo và biên tập sản phẩm; kiểm định; đóng gói/xuất bản. Thời gian AI chạy hoặc video ghi trùng lúc học không cộng thêm lần nữa vào giờ lao động.

Sau D0 và R1-G01, tính công sức còn lại theo **loại cụm**: học và viết mới; tái sử dụng nhiều; hình học; dữ liệu/xác suất; đề tổng hợp. Không lấy thời gian một bộ hàm số nhân cho tất cả bộ khác.

Để lập lịch, dùng ba thông tin thực: số giờ người chủ trì có thể dành mỗi tuần; giờ hoàn thành một đơn vị tương tự đã đo; các việc kiểm định và tích hợp còn lại. Hiện chưa có số giờ hằng tuần được cam kết và chưa đo công sức bộ mẫu, vì vậy chưa khóa tổng ngân sách giờ hoặc định mức giờ/bộ. Cách lập dự toán cụ thể ở mục 12.6.

### 12.4. Quy tắc giữ việc có thể hoàn thành

- Chỉ một gói đang học/sản xuất và một gói đang chuẩn bị nguồn; các cụm B được chọn theo mục tiêu gói.
- Mỗi phiên kết thúc với một đầu ra lưu được và một việc kế tiếp.
- Câu hỏi nghiên cứu vượt mục tiêu được ghi lại; câu hỏi ảnh hưởng tính đúng đắn phải giải quyết trước.
- Khi chậm, giảm số định dạng bổ trợ và độ cầu kỳ biên tập trước; giữ lõi bài học, lời giải và kiểm định.
- Rà tiến độ sau mỗi bộ và sau mỗi chặng; cập nhật kế hoạch nếu xuất hiện khoảng trống phạm vi hoặc quá nhiều sản phẩm chờ sửa.

### 12.5. Luyện tổng hợp, đề hoàn chỉnh và chữa lỗi

Từ chặng B, mỗi gói có nhiệm vụ đọc hiểu, lập luận, tính toán và mô hình hóa. B42 giữ câu trộn theo phần đã học; gắn mạch R và gói gốc để truy nguyên. Chặng C dùng bài phối hợp, đề giữa lộ trình và đề chuyển chặng; chặng D bố trí **sáu đề mới 90 phút trong sáu tuần 29–34**, mỗi tuần một đề kèm chữa và câu mới sau chữa. Tuần 35 có thể dùng một mô phỏng cuối khi còn đủ thời gian chữa; tuần 36 ôn ngắn và ổn định thao tác.

Sáu đề là số lượng thiết kế của chặng D, thay cho khung thử ba đề trước đây. Đây chưa phải bộ đề đã soạn. Ba đề gần nhất được dùng làm cửa sổ xem độ ổn định ở 5.4, không phải toàn bộ số đề của chương trình.

Mỗi đề tự biên soạn ghi rõ là đề ZO Math, ma trận mạch chính/hỗ trợ, định dạng và cách chấm theo 3.10, phiên bản câu, lời giải, phân loại lỗi và câu mới để thử lại. Đề thật dùng lời giải ZO Math tự xây dựng và đã kiểm chứng theo đúng năm/lần/mã; không phụ thuộc việc có bảng đáp án ngoài. Không dành tất cả thời gian cho việc làm đề rồi bỏ phần chữa.

| Lượt trong một tuần luyện đề | Học sinh thực hiện | Hồ sơ cần giữ |
| --- | --- | --- |
| Làm đề | Tự làm 90 phút, ghi câu bỏ và thời gian bất thường | Bài làm, điểm từng phần, câu đúng nhưng đoán |
| Phân tích và chữa | Tự giải lại, so với lời giải; chọn tối đa hai lỗi ưu tiên | Mạch và loại lỗi, phần nguồn cần quay lại |
| Câu mới sau chữa | Làm nhiệm vụ cùng mục tiêu nhưng chưa biết lời giải | Lỗi đã hết hay còn lặp; việc ôn kế tiếp |
| Kiểm tra duy trì | Gọi lại mục tiêu sau khoảng một tuần | Bằng chứng duy trì trên câu mới |

Nếu học sinh còn thiếu nền đáng kể, giảm bài đào sâu và dành thời gian bổ sung trước hoặc trong chặng C. Không đưa vào đề đo tiến bộ toàn phạm vi những nội dung chưa học mà không ghi rõ giới hạn kết quả. Khi thiếu thời gian gần kỳ thi, điều chỉnh số đề theo quỹ giờ thực nhưng giữ chu trình làm–chữa–thử lại; ghi lý do và phạm vi thay đổi.

Trong các lượt mô phỏng thực được bố trí (sáu lượt ở lịch tham chiếu đầy đủ), kiểm tra họ câu và việc đã tiếp xúc trước khi chọn đề. Bốn mã đề cùng năm không mặc nhiên tạo bốn đề mới đối với học sinh. Ghi thời gian giải và thao tác phiếu, lỗi đọc và lỗi chuyển kết quả; phần chữa phải dẫn đến câu mới hoặc thao tác thử lại. Dùng 36 tuần và nhịp 6 giờ/tuần làm tham số tham chiếu, tính lịch thực theo 12.10; thêm tài liệu không tự làm tăng sản lượng hay chứng minh hiệu quả.

### 12.6. Lập ngân sách công sức có căn cứ

Khi kết thúc R1-G01, ChatGPT điền bảng sau bằng nhật ký thực tế, rồi cùng người chủ trì xác định quỹ thời gian cho chặng kế tiếp. Không điền một số giờ suy đoán như thể đó là cam kết.

| Khâu | Số giờ thực tế cần ghi | Dùng để ước lượng |
| --- | --- | --- |
| Chuẩn bị nguồn và ma trận | Giờ đọc, đối chiếu, sửa phần trích | Tách việc thiết lập chung khỏi phần lặp ở mỗi bài |
| Học và tự giải | Giờ nghiên cứu, làm bài, trao đổi | Phụ thuộc mức quen thuộc và độ rộng nội dung |
| Kết tinh và thiết kế | Giờ tổng hợp, viết bài, soạn câu/lời giải | Phụ thuộc số mục tiêu và phần được dùng lại |
| Tạo và biên tập sản phẩm | Giờ thao tác thực, xem/sửa đầu ra | Theo định dạng đã chọn; thời gian máy chờ ghi riêng |
| Kiểm định | Giờ giải lại, kiểm hình, thử tự học | Theo số câu, rủi ro nội dung và lỗi phát hiện |
| Đóng gói và tích hợp | Giờ tổ chức tệp, dựng trang, kiểm tra đầu ra | Phân biệt thiết lập lần đầu với thao tác lặp |
| Sửa sau phản hồi và dự phòng | Giờ thực tế hoặc khoảng dự phòng được chủ trì thống nhất | Giữ chỗ cho lỗi, gián đoạn và công việc chưa biết rõ |

Cách tính chặng: xác định số giờ có thể dành trong từng tuần; cộng quỹ giờ của chặng; trừ công việc chung và phần dự phòng đã thống nhất; so sánh phần còn lại với tổng giờ ước lượng của các bài nhỏ được chọn. Nếu chưa đủ dữ liệu, dùng khoảng ước lượng và ghi lý do, cập nhật sau mỗi bài tương tự. Không chia quỹ giờ cho một “giờ/bộ trung bình” rồi xem số bộ đó là cam kết.

Ví dụ tính toán thuần minh họa: nếu một chặng được người chủ trì xác nhận có 20 giờ, việc chung cần 3 giờ và dự phòng là 4 giờ thì còn 13 giờ cho các bài đã chọn. Đây không phải quỹ giờ được giao cho dự án. Nếu công việc dự kiến vượt phần còn lại, giảm phạm vi chặng hoặc số định dạng, giữ việc học và kiểm định.

### 12.7. Thứ tự chuẩn bị và nhịp sản xuất

Mỗi tuần sản xuất chọn khối việc theo thứ tự: nguồn/nghiên cứu; tự giải và trao đổi; kết tinh; sản xuất; kiểm định/đóng gói. Một khối có thể kéo qua nhiều phiên. Cuối phiên lưu trạng thái; cuối tuần xem điểm nghẽn. Nhu cầu dùng học liệu trong bảng 12.2 quyết định thứ tự chuẩn bị dưới đây.

| Thứ tự chuẩn bị | Gói cần hoàn thành | Dùng ở đâu? | Điều kiện để coi là sẵn sàng sử dụng |
| --- | --- | --- | --- |
| **1 — đã hoàn tất** | **D0 v1.0: khảo sát đầu vào và hướng dẫn đọc kết quả** | Khi nhập học; tuần A của lịch cá nhân | Giữ thành phẩm; áp dụng 11.6 và ghi bằng chứng thật khi sử dụng |
| **2** | **R1-G01 trước, rồi các gói còn lại của R1** về giá trị trên miền, tiệm cận và tối ưu; kèm N cần thiết | Tuần 2–4 và các lượt ôn lại | Có bài luyện, lời giải, kiểm tra cuối và câu mới sau chữa; cùng một mục tiêu được kiểm tra qua nhiều biểu diễn |
| **3** | R2 và R3 lượt đầu | Tuần 5–8 | Dữ liệu và hình rõ; có câu diễn giải, lựa chọn cách giải và kiểm tra đơn vị |
| **4** | R4 lượt đầu, R5, R6 | Tuần 9–13 | Đếm đúng đối tượng; điều kiện mũ–lôgarit và họ nghiệm lượng giác được kiểm tra |
| **5** | R7, R3 tọa độ, R4 có điều kiện | Tuần 14–18 | Có câu liên kết kiến thức; cận tích phân, điều kiện hình và mẫu số xác suất được kiểm định |
| **6** | Các cụm R8 phối hợp, đề giữa lộ trình và đề chuyển chặng | Tuần 19–28 | Ma trận phủ tám mạch; có câu mới bỏ nhãn chuyên đề; có hướng dẫn chữa |
| **7** | Bộ đề hoàn chỉnh, câu sau chữa và phiếu ôn cuối | Tuần 29–36 | Đề đủ ba phần theo căn cứ đang áp dụng; đáp án/lời giải thống nhất; không dùng lại câu đã lộ cho mục đích đo tiến bộ |

R8 được tích hợp ngay từ gói R1; thứ tự 6 chỉ là lúc hoàn thiện các bộ phối hợp toàn cảnh. N được xây dần từ lỗi và yêu cầu tiên quyết. Không cần tạo trước tám notebook hoặc đủ mọi video, podcast, slide cho từng mạch.


| Công việc đang ưu tiên | Căn cứ | Bằng chứng kết thúc | Việc tiếp theo |
| --- | --- | --- | --- |
| D0 — đã hoàn tất | Đặc tả 11.1, bộ v1.0 tại 11.6 | Thành phẩm có trong Nguồn | Vận hành khi có học sinh; không mở lại sản xuất |
| R1-G01 | Đặc tả 11.2, nguồn 6.2 | Gói ôn có luyện, kiểm tra, câu sau chữa và hồ sơ | Hoàn thiện phần R1 còn cần cho chặng B.1, rồi R2/R3 |

Đặt ngày dự kiến theo quỹ giờ và phép tính ở 12.6. Không tự lấy thời lượng ôn của học sinh để suy công suất sản xuất. Khi đã có dữ liệu cần quản lý riêng, cập nhật bảng tiến độ theo D.11; không yêu cầu người chủ trì theo dõi hai lịch mâu thuẫn.

### 12.8. Điều kiện phải điều chỉnh lịch

| Dấu hiệu | Quyết định cần thực hiện |
| --- | --- |
| Hai bài liên tiếp vượt dự toán rõ rệt | Dừng tăng sản phẩm phụ, xác định khâu gây chậm và tính lại công sức của các bài tương tự |
| Nguồn hoặc toán còn điểm chưa chắc | Giữ kiểm định, dùng phần dự phòng hoặc dịch mốc; tiếp tục phần độc lập có đủ căn cứ |
| Cụm quá rộng để học và kiểm tra rõ ràng | Chia bài nhỏ có đầu ra độc lập; cập nhật mã con, ma trận và tổng số thành phẩm dự kiến |
| Quỹ giờ thực tế giảm | Tính lại lịch từ giờ đã đo; công bố rõ phần chưa kịp, không âm thầm bỏ một mạch kiến thức |
| Sản xuất lấn thời gian luyện tổng hợp | Ưu tiên lõi còn thiếu và chữa lỗi; giữ câu hỏi đào sâu có ích, giảm định dạng phụ tốn công |

Ghi mỗi quyết định đổi lịch cùng lý do, phần bị ảnh hưởng và một việc kế tiếp. Mốc ngày không được dùng để hợp thức hóa một học liệu còn lỗi chặn.

### 12.9. Ngân sách thời gian ôn và các lượt quay lại

Trong chặng B, 6 giờ/tuần được chia thành **3 giờ trọng tâm, 1 giờ 30 phút ôn lại, 1 giờ chữa lỗi và 30 phút kiểm tra**. Chặng C chuyển thành **2 giờ bài phối hợp, 2 giờ ôn các mạch, 1 giờ 30 phút chữa và 30 phút kiểm tra**. Chặng D dùng **90 phút làm đề, 120 phút phân tích–chữa, 90 phút câu mới sau chữa, 60 phút ôn lại**. Đây là tổng thời gian học sinh làm việc, kể cả tự học.

| Lượt quay lại | Thời điểm áp dụng | Học sinh thực hiện | Bằng chứng giữ lại |
| --- | --- | --- | --- |
| Nhớ lại gần | Khoảng 2–3 ngày sau lần luyện đầu | Tự nhắc cách nhận diện, điều kiện; làm câu ngắn chưa xem lời giải | Ý nhớ sai hoặc điều kiện bị bỏ |
| Kiểm tra duy trì | Khoảng 7 ngày | Làm câu mới cùng mục tiêu, thay dữ kiện hoặc biểu diễn | Có còn lặp lỗi không? |
| Nối lại | Khoảng 3–4 tuần | Làm bài trộn với mạch khác, không gắn nhãn phương pháp | Có tự chọn được công cụ không? |
| Dùng trong đề | Chặng C–D | Nhận ra và xử lý nhiệm vụ dưới giới hạn thời gian | Điểm, thời gian, cách kiểm tra đáp số |

Lịch 2–3 ngày, 7 ngày và 3–4 tuần là cách tổ chức được chọn cho dự án, không phải khoảng cách tối ưu đã chứng minh cho mọi người học. Nếu sai lại, đưa mục tiêu đó vào lượt gần nhất. Nếu làm vững qua hai lượt, giảm số câu lặp và chuyển thời gian sang điểm yếu.

R8 được luyện trong mọi chặng bằng năm câu hỏi: **đang tìm đại lượng nào; điều kiện nào ràng buộc; biểu diễn nào phù hợp; công cụ nào giải quyết được; đáp số có hợp lí không?** Bài toán thực tế không chỉ xuất hiện ở cuối khóa.

### 12.10. Lập lịch từ ngày thi và ngày gia nhập

**C-09 — một cơ chế chung cho mọi thời điểm nhập học.** Bảng 36 tuần là lộ trình tham chiếu đầy đủ, không phải điều kiện đăng ký hay con đường duy nhất. Không bắt người nhập tháng 11/tháng 1 học lại nguyên lịch từ tuần 1, cũng không đưa thẳng vào tuần của nhóm tháng 9 khi chưa đủ tiên quyết.

Đầu vào tối thiểu: ngày gia nhập; ngày thi và mức xác nhận của mốc đó; giờ học Toán thực có theo từng tuần; các tuần nghỉ/thi ở trường; nội dung đã học, đang học, ngày dự kiến học phần còn lại; D0 và bài làm mới liên quan; mục tiêu học của học sinh. Nếu chỉ có thông tin “đã học”, chưa tự suy là “đã vững”.

Thực hiện theo thứ tự:

1. **Tính quỹ giờ còn lại.** Lấy mốc thi làm điểm cuối, trừ các khoảng thực sự không học được. Dùng tổng giờ khả dụng từng tuần; không lấy số tháng nhân một hệ số cố định. Nếu ngày thi chưa chính thức, ghi rõ ngày giả định và ngày rà lại. Ngày lẻ chỉ thêm khi đã có giờ học cụ thể.
2. **Định vị bằng D0 v1.0.** Chọn nhiệm vụ thuộc phần đã học; giữ cờ CH/KCG và mức hỗ trợ. Khảo sát bổ sung hẹp bằng bài mới khi D0 chưa lấy mẫu một tiên quyết quan trọng; không tự tạo D0 phiên bản mới chỉ vì người học nhập muộn.
3. **Lập sổ mục tiêu cần phủ.** Với từng B thuộc phần chung, ghi phần đã có bằng chứng, phần chưa rõ và phần chưa học. B02 chỉ được gọi theo nhu cầu; B42 không cộng thành một vùng kiến thức thứ 42 cần học riêng. Giữ đủ R1–R8 trong các mốc kiểm tra độ phủ; R8 có thể nằm trong gói khác.
4. **Đặt các nhiệm vụ theo tiên quyết và tiến độ trường.** Phần chưa học được hẹn sau khi học ở trường hoặc được bố trí học mới có hướng dẫn trong chính quỹ giờ đã tính. Không tính phần học mới là ôn nhanh miễn phí. Giữa các nhánh đủ điều kiện, ưu tiên tiên quyết gây nghẽn, mục tiêu chưa có bằng chứng và mục tiêu đến hạn gọi lại.
5. **Đặt lùi các mốc đánh giá, chữa và củng cố từ ngày thi.** Dành giờ chữa trước khi chốt số đề. Rải luyện nhớ lại và phối hợp từ sớm; không chờ kết thúc toàn bộ B mới bắt đầu. Mỗi mục tiêu cần một vị trí học/kiểm tra và một quyết định theo kết quả, không chỉ có tên trong lịch.
6. **Kiểm ngân sách và phát hành lịch cá nhân.** Chi tiết hai tuần gần nhất, các tuần sau ghi mốc và trọng tâm có thể điều chỉnh. Ghi rõ những mục tiêu chưa đủ chỗ hoặc còn phụ thuộc lịch trường; không công bố lịch là khả thi khi tổng giờ cần vượt giờ có.

Ngân sách C gồm: giờ học mới/ôn trọng tâm + gọi lại + phối hợp + chữa/thử lại + đánh giá và thao tác thi. Mỗi phút chỉ vào một khoản chính; một bài R1/R8 không được tính hai lần. Chỉ tiêu độ phủ được kiểm theo mục tiêu, còn số giờ được cộng theo hoạt động thực.

### 12.11. Khi thời gian không đủ

Giữ **cơ hội học và đánh giá mục tiêu thiết yếu trên toàn phạm vi cần thiết** là ưu tiên thiết kế C, không phải bảo đảm mọi học sinh sẽ làm chủ toàn bộ CT trước thi. “Đã có vị trí”, “đã tiếp xúc” và “đã đạt” là ba kết luận khác nhau.

Giảm theo thứ tự: bài mở rộng và độ đào sâu ở phần đã vững; số câu cùng loại/lượt luyện lặp; số vòng phối hợp có nội dung trùng; số đề hoàn chỉnh. Giữ phần giải thích thiết yếu, sửa lỗi và thử lại. Có thể giảm số câu gọi lại và chọn mục tiêu có nguy cơ quên, nhưng không xóa toàn bộ hoạt động gọi lại để tăng số đề.

Không bỏ cả một mạch vì ít xuất hiện trong một đề 2025/2026. Trước khi giảm phạm vi phải đối chiếu sổ CT/B, tiên quyết và quỹ giờ thực. Nếu đã giảm độ sâu, vòng luyện và đề mà vẫn thiếu giờ, đánh dấu **“lịch chưa đáp ứng phạm vi trong quỹ giờ hiện có”**, nêu rõ mục tiêu nào chưa được bố trí và lý do. Người chủ trì cùng học sinh điều chỉnh cam kết thời gian/phạm vi thực tế; không âm thầm xóa vùng kiến thức, không hứa độ phủ hoặc điểm số không thể bảo đảm.

### 12.12. Ba trường hợp gia nhập — minh họa tính lịch

**Toàn bộ số dưới đây là ví dụ C, không phải lịch thi công bố.** Giả định ngày thi 10/06/2027, học 6 giờ/tuần có học, có đúng hai tuần không học được ở mỗi trường hợp; chỉ tính tuần đầy đủ. Hai tuần củng cố E nằm trong tổng tuần học, không bị trừ lần nữa. Phải thay giả định bằng lịch thật khi vận hành.

| Gia nhập giả định | Tuần đầy đủ đến mốc thi | Tuần học sau hai tuần nghỉ | Tổng giờ | A định vị | B ôn trọng tâm/học phần thiếu | C phối hợp | D đề–chữa | E củng cố |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 14/09/2026 | 38 | 36 | 216 | 1 | 17 | 10 | 6 | 2 |
| 02/11/2026 | 31 | 29 | 174 | 1 | 14 | 8 | 4 | 2 |
| 04/01/2027 | 22 | 20 | 120 | 1 | 10 | 4 | 3 | 2 |

Các cột A–E là phân bổ giờ quy đổi theo tuần để kiểm ngân sách; gọi lại, phản hồi và R8 chạy xuyên chặng. D ba tuần không mặc nhiên đủ ba đề nếu chữa cần nhiều giờ. D0 không nhất thiết chiếm trọn sáu giờ tuần A; phần còn lại dùng định vị và sửa đầu vào. Phân bổ này chỉ được chấp nhận sau bước 6 ở 12.10, không phải ba chương trình cố định hoặc kết quả nghiên cứu.

**Cách áp dụng cụ thể cho người gia nhập tháng 1:** dùng một phần tuần đầu làm D0 những phần đã học và đối chiếu lịch lớp 12. Nếu B18 đã có bằng chứng độc lập, giảm luyện riêng R1-G01 nhưng vẫn hẹn gọi lại; nếu B22–B24 chưa học, giữ trạng thái CH và đặt R7 sau mốc học của trường hoặc bố trí giờ học mới. R2 và R4 phần đếm/biến cố có thể tiến song song trong lúc chờ R7. R3 vẫn phải có cả hình học/vectơ/Oxy và Oxyz; R4 vẫn có phần điều kiện; R5 và R6 vẫn có vị trí dù ít giờ đào sâu hơn. Phiếu phối hợp đưa R8 vào các mạch ấy. Mười tuần B được phân chia theo số mục tiêu còn thiếu, không chia đều cho tám R. Nếu kiểm quỹ giờ cho thấy mười tuần không đủ, giảm C/D theo 12.11 và tính lại, không đánh dấu hoàn thành cho kịp bảng.

**Đầu ra của lịch cá nhân:** một bảng có tuần/ngày thật, mục tiêu B, R chính, trạng thái trước học, hoạt động và số phút, nhiệm vụ mới để kiểm tra, lượt gọi lại, điều kiện đổi lịch. Học sinh cùng nhóm có thể làm chung một bài đã đủ tiên quyết; hồ sơ phần còn thiếu và lịch gọi lại vẫn riêng.

### 12.13. Rà lịch trong quá trình học

Cuối mỗi tuần, kiểm lần lượt: giờ thực so với dự kiến; phần đã học ở trường; mục tiêu chưa có bằng chứng; lỗi cần sửa; lượt đến hạn; tiến độ phủ các R. Dành chỗ cho mục tiêu chưa được đụng tới, tránh chỉ luyện mãi hai điểm yếu quen thuộc. “Tối đa hai ưu tiên sửa” giới hạn tải sửa trong tuần, không giới hạn toàn bộ phạm vi được học.

Đổi lịch khi có bằng chứng mới, học sinh nghỉ/gia nhập lại, quỹ giờ đổi, trường đổi tiến độ hoặc mốc thi đổi. Giữ lịch cũ trong lịch sử, ghi vì sao chuyển mục tiêu. Khi gần thi, chỉ kết luận khả năng duy trì đến khoảng trễ thực đã quan sát. Không so điểm giữa hai đề khác cấu hình như cùng một thước đo nếu chưa có cơ sở.

### 12.14. Cập nhật khi Bộ thay đổi kỳ thi

**C-03/C-10:** người chủ trì rà thông tin chính thức khi có công bố mới; lịch rà định kỳ mỗi tháng là tham số vận hành, không phải quy định của Bộ. Quy trình này không tự thiết lập thông báo hoặc tác vụ nền.

| Bước | Việc làm và sản phẩm |
| --- | --- |
| Xác minh | Lưu văn bản/trang cơ quan phát hành, ngày, điều khoản, đối tượng và thời điểm áp dụng; phân biệt dự thảo, thí điểm và chính thức |
| Phân loại thay đổi | Ngày thi; số câu/dạng trả lời/chấm; phương tiện; phạm vi kiến thức; hoặc nhiều loại cùng lúc |
| Lập tác động | Lịch → tính lại giờ; định dạng → cấu hình/đề/phiếu/thao tác; phạm vi → CT/CD/B rồi R/gói. Ghi danh sách mã chịu ảnh hưởng và mã đã rà |
| Sửa và kiểm | Tạo phiên bản cấu hình mới; giải lại câu đổi biểu diễn, kiểm đáp án/điểm/tổng thời gian; cập nhật ma trận đề và mẫu thao tác; không chuyển dữ liệu điểm cũ sang quy cách mới bằng phỏng đoán |
| Phát hành | Ghi cấu hình nào hết dùng, từ khi nào; cập nhật lịch cá nhân, hướng dẫn, danh sách thành phần gói. Thông báo thay đổi cùng sản phẩm khi công bố theo mục 13 |
| Bảo toàn | Giữ bản cũ để truy nguyên. D0 tiếp tục dùng để định vị toán; chỉ mở sửa nếu phát hiện lỗi toán, mục tiêu không còn phù hợp hoặc hướng dẫn thật sự gây quyết định sai |

Nếu thay đổi chỉ nằm ở lớp định dạng, B01–B42 và R1–R8 giữ mã. Nếu CT thật sự đổi, đánh dấu yêu cầu thêm/bỏ/sửa trong sổ H, quản lý phiên bản nội dung; không chỉ thay nhãn đề rồi coi là đã xử lý.

## 13. Xuất bản trên ZO Math và phân phối nhiều kênh

### 13.1. ZO Math là nơi tập hợp chính

Trang chương trình cho thấy mục tiêu, D0 để định vị đầu vào, tám mạch R, chặng đang mở, các gói đã có và đường ôn lại. Mã B phục vụ tra cứu nguồn trong hồ sơ; học sinh thấy tên mục tiêu và hướng dẫn dễ hiểu. Mỗi trang học giữ phiên bản, nguồn, bài tự luyện, lời giải, tự kiểm tra và sản phẩm hỗ trợ. Video hoặc bài giới thiệu ở kênh khác dẫn về đúng trang học.

Chọn nền website QMD hiện có. Chưa cần xây ứng dụng, tài khoản học sinh hay hệ thống mới để đăng bộ mẫu. Khi tích hợp, đọc quy chuẩn repo và kiểm tra cấu trúc thực tế trước khi sửa.

### 13.2. Quy trình công bố

1. Chuẩn bị gói cụ thể từ các bản đã kiểm định.
2. Người chủ trì xem và duyệt đúng phạm vi, phiên bản và nơi công bố.
3. Tích hợp bằng quy trình xuất bản ZO Math hiện hành.
4. Mở trang thật, thử tải tệp và kiểm tra các liên kết quan trọng trên máy tính và điện thoại.
5. Ghi URL, ngày công bố, phiên bản và phần còn chờ bổ sung vào hồ sơ.

Việc duyệt dựa trên gói có thể xem được, không phải duyệt một ý định chung chưa có sản phẩm. Kế hoạch này chưa thực hiện đăng bài, gửi thông báo hay công bố video.

### 13.3. Tái sử dụng có đối chiếu

Các bài hàm hằng, bậc nhất, giá trị tuyệt đối, bậc hai, bậc ba, lôgarit và khung khảo sát của ZO Math là ứng viên dùng lại theo lịch sử dự án. Trước khi sử dụng, đọc đúng bản nguồn hiện hành và chọn phần phù hợp mục tiêu ôn thi. Không sao chép toàn bài chuyên sâu vào bài nhập môn.

Giữ một bản nội dung dùng chung có thể truy nguyên. Thay đổi ở bài ôn thi không tự kéo theo đổi tên dự án, đường dẫn hay CSS toàn website. Nghiên cứu dài hạn cần lưu thì dùng hệ `_research/` hiện có khi làm việc trong repo, không dựng hệ trùng.

### 13.4. Phân phối từ cùng một gói

Một bộ có thể có trang học, tài liệu tải, video, âm thanh và nội dung giới thiệu trên nhiều kênh. Chỉ chuẩn bị các kênh phù hợp và đã được chọn; cùng mã bộ, phiên bản và đường dẫn về trang học. Chưa tự đặt tên tài khoản hoặc URL kênh chưa xác nhận.

Khi sửa nội dung gốc, rà những sản phẩm bị ảnh hưởng. Nếu video đã đăng có lỗi ảnh hưởng toán, bổ sung đính chính rõ và thay bản khi cần; không chỉ sửa phiếu rồi giữ video sai mà không ghi nhận.

### 13.5. Bảng ứng viên tái sử dụng

Danh sách này định vị phần nên kiểm tra, không xác nhận tệp hiện hành đã được đọc trong lần biên tập kế hoạch. Chỉ dùng nội dung sau khi mở đúng bản và xác định mức phù hợp.

| Nội dung ZO Math đã biết | Cụm có thể dùng | Cần kiểm tra trước khi dùng |
| --- | --- | --- |
| Hàm hằng, hàm bậc nhất, giá trị tuyệt đối | B04; B26 khi có liên hệ phù hợp | Cách giới thiệu, miền xác định, hình và bài tập phù hợp nhập môn |
| Hàm bậc hai | B05–B06 | Dạng biểu thức, đồ thị, dấu và phạm vi bài luyện |
| Bài $y=x^3$ | B16, B18, B21 | Tiếp tuyến, cực trị; điểm uốn/tính cong phải ghi đúng nhãn phạm vi |
| Bài $y=\ln x$ | B13–B15, B17 | Điều kiện, đồ thị, cách giải thích và bài tập |
| Khung khảo sát và các bài 100+ Hàm số | B21 | Chọn phần phục vụ mục tiêu; dẫn đọc thêm khi cần sâu hơn |
| Quy chuẩn QMD và quy trình hình | Toàn hệ trang và các bài có hình | Đọc hướng dẫn hiện hành, xác định tệp nguồn và đầu ra đúng |

Nguồn thuộc bộ SGK khác vẫn có thể tham khảo nếu giải thích hoặc bài tập có ích; trục KNTT phục vụ chỉ mục, không buộc viết lại mọi bài tốt. Nội dung toán dùng chung có một bản nguồn chính; bản ôn thi chỉ chọn, biên tập hoặc dẫn lại phần cần thiết và ghi phiên bản để tránh nhiều bản sao sửa lệch nhau.

### 13.6. Trình bày và giao việc trong repo

Giữ cách viết hiện hành của ZO Math: giải thích bằng câu văn; dùng “suy lí” và “kiến tạo ý nghĩa” đúng ngữ cảnh; phân biệt “đổi chiều biến thiên” với “đổi tính cong”. Trong Markdown/QMD dùng `$...$`, `$$...$$`, `\frac{}{}`, `\lvert...\rvert`, `f^\prime`, `f^{\prime\prime}`; chỉ dùng `\quad` khi thực sự cần khoảng cách.

Tác tử làm trong repo phải đọc AGENTS.md, quy trình QMD, hình, PDF và xuất bản đang áp dụng; xác định đường dẫn thực tế và thay đổi đúng phần được giao. Giữ bố cục, màu và thành phần giao diện hiện có sau khi kiểm tra, không tự thiết kế lại nhận diện để tích hợp một bộ ôn thi. Mẫu giao việc ở D.16 yêu cầu trả về tệp đã sửa, đầu ra đã xem, lỗi còn lại và bản cần người chủ trì duyệt.

Sau công bố, mở URL thật, thử tải phiếu/lời giải, kiểm tra trên máy tính và điện thoại ở mức có thể thực hiện; ghi rõ thiết bị hoặc cách xem đã dùng. Nội dung chưa công bố hiển thị trạng thái chuẩn bị, không tạo liên kết giả. Việc gửi thông báo qua email hoặc ứng dụng nhắn tin chỉ thực hiện khi người chủ trì có yêu cầu gửi cụ thể.

## 14. Tự động hóa từ một việc nhỏ cụ thể

**Tự động hóa đầu tiên sẽ là tạo gói xuất bản cho một bộ học liệu đã duyệt.** Chưa bắt đầu bằng tự động nghiên cứu, tự phê duyệt hoặc đăng đồng loạt nhiều kênh.

| Phần | Thiết kế đề xuất |
| --- | --- |
| Đầu vào | Hồ sơ bộ, phiên bản nội dung, danh sách tệp đã kiểm định, dấu duyệt thực tế của người chủ trì |
| Xử lý | Kiểm tra đủ tệp; phát hiện phiên bản không khớp; tạo danh sách thành phần và mô tả trang; tập hợp gói |
| Đầu ra | Một gói công bố có thể xem lại, báo cáo thiếu tệp hoặc sai phiên bản và chỉ dẫn bước tiếp theo |
| Tình huống phải xử lý | Thiếu tệp; lẫn bản cũ; không có thông tin duyệt; liên kết chưa tồn tại; chạy lại không tạo trùng gói |
| Phép thử đầu tiên | Chạy trên R1-G01 đã duyệt; so sánh với gói đóng thủ công; thử thêm một trường hợp thiếu tệp để kiểm tra báo lỗi |

Sau khi cách đóng gói ổn định, mới mở rộng sang chuẩn bị bản cho từng kênh và công bố theo quyền đã được giao. Công cụ cần ghi lại việc đã làm và kết quả. Không coi một thông báo “thành công” là đủ nếu không có sản phẩm hoặc URL kiểm tra được.

Đây là hạng mục trong lộ trình, chưa phải automation đã cài hay tác vụ đã lên lịch. Chỉ triển khai khi bộ mẫu tạo ra một gói thật làm đầu vào và đã hiểu các thao tác lặp lại cần tự động hóa.

## 15. Quyết định hiện hành và trạng thái bàn giao

### 15.1. Nguyên tắc đang áp dụng

| Nội dung | Quy tắc của 0.6 |
| --- | --- |
| Tài liệu điều hành | 0.6 thay thế đầy đủ 0.5; không cần mở bản cũ để thực hiện |
| Mục tiêu | Ôn thi Toán THPT 2027, suy lí và kiến tạo ý nghĩa; điều phối bằng bài làm, sửa lỗi và thời gian thực |
| Kiến trúc | Bốn lớp ở 2.5; CT/CD/B là bản đồ phạm vi, R là mạch kết nối, lịch là thích ứng, định dạng thi có cấu hình riêng |
| Kế thừa | Giữ 15 nhóm, B01–B42, tám R, nền N, 24 chương/79 bài, chín chuyên đề, quy trình và đề cương nền |
| Nguồn | A/B/C tách rõ; tự giải và kiểm chứng toán; không dùng lời giải thương mại làm thẩm quyền |
| Học liệu | Nghiên cứu với nguồn/Notebook, người chủ trì tự học và trao đổi, kết tinh trước sản xuất; Studio chọn theo tác dụng |
| Người học | Phân biệt chưa học/chưa được khảo sát với đã học nhưng sai; tiến tiếp theo mục tiêu, cho đi tiếp nhánh độc lập |
| Kho và công bố | Một hồ sơ/gói; kiểm nguồn, nội dung, định dạng, phiên bản và phạm vi phát hành; ZO Math là đầu mối |
| Quá trình sáng tạo | Giữ thành lớp nội dung riêng được biên tập; không bắt học sinh xem toàn bộ để dùng gói |
| Tự động hóa | Chỉ triển khai từ một gói đã duyệt và đã thử thủ công như mục 14 |
| Việc tiếp nối | D0 v1.0 đã hoàn tất; bước kế tiếp duy nhất ở 15.5 |

### 15.2. Tham số thiết kế và cách điều chỉnh

| Tham số C | Giá trị tham chiếu | Khi cần thay và bằng chứng cần xem |
| --- | --- | --- |
| Lịch đầy đủ | 36 tuần × 6 giờ = 216 giờ | Ngày gia nhập/thi, giờ thực, phần đã học; tính lại theo 12.10 |
| Gọi lại | 2–3 ngày, 7 ngày, 3–4 tuần | Lỗi, khoảng trễ thực, thời gian đến thi; không gọi đây là khoảng cách tối ưu |
| Giảm luyện riêng | Khoảng 80% hai cụm mới cách một tuần, không sai điều kiện cốt lõi | Độ đại diện/tính mới, mục tiêu thiết yếu, dữ liệu mâu thuẫn; xem 5.6 |
| Ưu tiên sửa | Tối đa hai điểm trong một chu kỳ tuần | Quá tải và tiên quyết gây nghẽn; vẫn giữ kiểm độ phủ các mạch |
| Đề hoàn chỉnh | Sáu đề chặng D trong lịch 36 tuần | Giờ chữa, mức sẵn sàng, cấu hình thi; giảm số đề trước khi bỏ vùng kiến thức |
| Xem độ ổn định | Ba đề mới gần nhất nếu có đủ ba đề phù hợp | Nếu ít hơn thì báo đúng số quan sát; không coi thiếu ba đề là lý do chặn toàn bộ lộ trình |
| D0 | 24 nhiệm vụ + 24 thử lại, thành phẩm v1.0 | Chỉ mở sửa có căn cứ; lấy thêm bằng chứng hẹp khi cần |
| R1-G01 | M1–M5; đạo hàm–biến thiên–đồ thị | Chia nhỏ nếu tải quá lớn; không biến thành toàn R1 |
| Sản xuất | Một gói đang làm, một gói chuẩn bị nguồn | Công sức và điểm nghẽn; giảm định dạng phụ trước |
| Rà nguồn kỳ thi | Khi có công bố; kiểm định kỳ mỗi tháng | Văn bản áp dụng thay đổi; thực hiện 12.14 |

Các quy cách 90 phút/12–4–6/cách chấm tại 3.10 thuộc **A trong phạm vi căn cứ đã công bố**; việc tạm dùng cho thiết kế mùa 2027 thuộc **C**, chờ xác nhận áp dụng. Không gom quy cách Bộ với tham số học tập thành một mức bằng chứng.

### 15.3. Kết quả đã có và phạm vi lần nâng cấp

0.5 đã hoàn thành và là bản nền để audit. D0 v1.0 đã hoàn tất, có trong Nguồn. Lần nâng 0.6 đã rà toàn văn 0–16/A–G, giữ chỉ mục và quy trình, rà CT theo nhóm yêu cầu tại H, kiểm các mục lục, đọc phần liên quan của D0, bổ sung hồ sơ nghiên cứu NC01–NC10, phân loại quyết định, lịch thích ứng và quy trình đổi cấu hình thi. Phụ lục F cho phép truy nguyên từng thay đổi lớn.

Các kiểm tra kế thừa ở 3/E giữ ngày và giới hạn ban đầu. Không suy rằng lần biên tập này đã đọc mọi trang SGK/SGV, tự giải lại mọi đề hoặc có thử nghiệm học sinh. Chưa có bằng chứng được cung cấp để ghi R1-G01 đã biên soạn, Notebook đã nạp nguồn thành công hoặc học liệu đã công bố trên website. Không thay trạng thái đó bằng dự đoán.

### 15.4. Cách vận hành sau khi khóa kế hoạch

Tiếp tục chu trình nguồn → nghiên cứu → kết tinh → học liệu → kiểm định → đóng gói của mục 6–10. Ma trận yêu cầu được làm cụ thể tại gói liên quan, đối chiếu sổ H để không bỏ mục tiêu ẩn. Sổ lịch cá nhân dùng bài làm thật; khi chưa có học sinh, chỉ ghi thiết kế và tình trạng học liệu. Khóa kế hoạch không đồng nghĩa khóa mọi tham số thử nghiệm, phê duyệt mọi thành phẩm hoặc cho phép công bố mọi kênh.

### 15.5. Một việc triển khai kế tiếp duy nhất

**Chuẩn bị bộ nguồn và ma trận mục tiêu cho phiên nghiên cứu đầu tiên của R1-G01**, theo 6.2, 11.2, D.14 và D.2.

Đầu ra của đúng việc này: hồ sơ chỉ rõ tệp/bản/trang in/trang PDF của đoạn CT/SGK cần đọc; đối chiếu M1–M5 với B16–B18 và nền B04/B06/B12 thực sự cần; một yêu cầu trích xuất cho phiên đầu về dấu đạo hàm–biến thiên; phép thử Notebook đọc nguồn. Kết thúc khi bộ này đủ để người chủ trì mở phiên nghiên cứu và biết đọc/làm gì. Chưa mở thêm nhiệm vụ sản xuất R2/R3 hoặc làm lại D0 trong bước đó.

Lần nâng 0.6 chỉ hoàn thiện kế hoạch, không ghi việc chuẩn bị R1-G01 là đã làm. Khi tiếp tục sau gián đoạn, dùng kế hoạch này cùng hồ sơ mới nhất; giữ trạng thái D0 và các bằng chứng đã có.

## 16. Kho lâu dài và các ấn bản hằng năm

### 16.1. Mã kiến thức và mã ấn bản

Phiên bản nội dung toán, cấu hình kỳ thi và lịch cá nhân là ba hồ sơ có thể đổi độc lập. Cấu hình thi theo 3.14/12.14; khi chỉ đổi ngày/định dạng, không đổi mã B hoặc xóa học liệu toán còn đúng.

Kho lâu dài lưu khái niệm, lập luận, hình, câu hỏi, lời giải và nguồn đã kiểm tra. Lộ trình năm chọn nội dung, thứ tự, bài luyện, căn cứ thi và sản phẩm công bố cho năm ấy. Một bản toán tốt có thể dùng ở nhiều mùa; mỗi mùa vẫn giữ được nguồn và phiên bản đã thực sự sử dụng.

| Thành phần | Ví dụ quy ước | Phần được quản lý |
| --- | --- | --- |
| Cụm kiến thức | B04 | Phạm vi toán ổn định; mã con khi chia bài |
| Nội dung | B04, phiên bản 1.0 | Khái niệm, ví dụ, bài tập, lời giải và lịch sử sửa toán |
| Hồ sơ mùa | 2027-R1-G01, dùng các mã B liên quan | Vị trí trong lộ trình, nguồn thi áp dụng, các sản phẩm được chọn |
| Thành phẩm | 2027_R1-G01_tu_luyen_v1.1.pdf | Bản nội dung nguồn, phiên bản câu hỏi, ngày tạo |
| Notebook | ZO Math · Ôn thi 2027 · R1-G01 · Đạo hàm và đồ thị | Nguồn thực dùng, trạng thái thử đọc và liên kết thật |

Các tên là ví dụ quản lý, không phải tệp đã tạo. Khi thay đổi chỉ cách trình bày, ghi đúng thay đổi ở sản phẩm; khi sửa ý nghĩa toán, cập nhật bản nội dung và rà mọi sản phẩm liên quan. Quy tắc này giúp sửa lỗi một lần ở nguồn rồi kiểm tra các bản sử dụng, đồng thời bảo toàn dấu vết của từng mùa.

### 16.2. Tổng kết sau kỳ thi 2027

ChatGPT thu thập đề chính thức, tự giải và kiểm chứng phần dùng để phân tích, đối chiếu những nhiệm vụ học sinh đã học và những chỗ còn vướng. Người chủ trì xem kết quả, chọn phần cần sửa hoặc nghiên cứu thêm. Tổng kết giờ theo khâu, sản phẩm được dùng, lỗi quan trọng, phản hồi thực tế và những phần phạm vi còn thiếu.

Khóa một hồ sơ mùa 2027 gồm danh mục học liệu, nguồn, phiên bản, URL và nhật ký đính chính. “Khóa hồ sơ” là giữ dấu vết ấn bản; lỗi phát hiện sau vẫn phải được đính chính rõ. Không sửa lịch sử để làm như một cải tiến sau kỳ thi đã có từ đầu mùa.

### 16.3. Chuẩn bị ấn bản tiếp theo

Kiểm tra chương trình và văn bản kỳ thi của năm mới; đối chiếu tác động lên lộ trình trước khi đổi bài. Giữ bài tốt, sửa điểm yếu, bổ sung yêu cầu còn thiếu; tạo sản phẩm mới khi giúp học rõ hơn. Không cần viết lại mọi nội dung để có một ấn bản mới.

Với mỗi bài được dùng lại, ghi một trong các tình trạng: giữ nguyên nội dung; đổi cách trình bày; sửa toán; bổ sung nhiệm vụ; tạm ngừng sử dụng. Cập nhật nguồn, câu hỏi và đường dẫn liên quan. Việc đổi lộ trình năm không làm mất mã kiến thức và lịch sử nguồn.

### 16.4. Giá trị lâu dài và sản phẩm trả phí

Sau khi một cụm học liệu đã được sử dụng thực tế, xem xét giá trị của bộ có trình tự, bài luyện, lời giải đã kiểm tra và chỉ dẫn tự học như nền tảng sản phẩm trả phí. Thu thập nhu cầu cụ thể và công sức hỗ trợ trước khi lập giá hoặc dự báo doanh thu.

Trong giai đoạn đầu, tiêu chí tiến bộ là nội dung dùng được, người học có cơ hội thực hành và nhịp sáng tác có thể duy trì. Việc nghiên cứu triết lí giáo dục đi song song với phát triển học liệu; câu hỏi dài hạn được lưu vào hệ nghiên cứu thích hợp, không làm mất điểm kết thúc của bài đang sản xuất. Bản kế hoạch này chưa chốt giá bán, mô hình doanh thu hay cam kết thu nhập.

## Phụ lục A. Chỉ mục 24 chương và 79 bài SGK

Các vị trí tuần/chặng tại A.1 trỏ mẫu 36 tuần ở 12.2, không ấn định lịch cho mọi người học. Lịch cá nhân giữ đường tra chương/B/R khi xếp lại thời gian.

Bảng được lập trực tiếp từ các trang mục lục ghi ở mục 3.1. “Trang đầu” là trang in của bài đầu tiên trong chương, không phải số trang PDF. Tên chương được chuẩn hóa dấu câu để tra cứu. Các dải bài là liên tiếp trong từng lớp.

| Sách | Chương | Tên chương | Bài | Trang đầu | Cụm ZO Math |
| --- | --- | --- | --- | ---: | --- |
| S10.1 | I | Mệnh đề và tập hợp | 1–2 | 5 | B01 |
| S10.1 | II | Bất phương trình và hệ bất phương trình bậc nhất hai ẩn | 3–4 | 22 | B03 |
| S10.1 | III | Hệ thức lượng trong tam giác | 5–6 | 33 | B25 |
| S10.1 | IV | Vectơ | 7–11 | 46 | B26–B27 |
| S10.1 | V | Các số đặc trưng của mẫu số liệu không ghép nhóm | 12–14 | 73 | B36 |
| S10.2 | VI | Hàm số, đồ thị và ứng dụng | 15–18 | 4 | B04–B06 |
| S10.2 | VII | Phương pháp tọa độ trong mặt phẳng | 19–22 | 30 | B28–B29 |
| S10.2 | VIII | Đại số tổ hợp | 23–25 | 60 | B39.a–B39.b |
| S10.2 | IX | Tính xác suất theo định nghĩa cổ điển | 26–27 | 77 | B39.c |
| S11.1 | I | Hàm số lượng giác và phương trình lượng giác | 1–4 | 5 | B07–B09 |
| S11.1 | II | Dãy số. Cấp số cộng và cấp số nhân | 5–7 | 42 | B10 |
| S11.1 | III | Các số đặc trưng đo xu thế trung tâm của mẫu số liệu ghép nhóm | 8–9 | 58 | B37 |
| S11.1 | IV | Quan hệ song song trong không gian | 10–14 | 70 | B30 |
| S11.1 | V | Giới hạn. Hàm số liên tục | 15–17 | 104 | B11–B12 |
| S11.2 | VI | Hàm số mũ và hàm số lôgarit | 18–21 | 4 | B13–B15 |
| S11.2 | VII | Quan hệ vuông góc trong không gian | 22–27 | 27 | B31–B32 |
| S11.2 | VIII | Các quy tắc tính xác suất | 28–30 | 66 | B40 |
| S11.2 | IX | Đạo hàm | 31–33 | 81 | B16–B17 |
| S12.1 | I | Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số | 1–5 | 5 | B18–B21 |
| S12.1 | II | Vectơ và hệ trục tọa độ trong không gian | 6–8 | 45 | B33 |
| S12.1 | III | Các số đặc trưng đo mức độ phân tán của mẫu số liệu ghép nhóm | 9–10 | 75 | B38 |
| S12.2 | IV | Nguyên hàm và tích phân | 11–13 | 4 | B22–B24 |
| S12.2 | V | Phương pháp tọa độ trong không gian | 14–17 | 29 | B34–B35 |
| S12.2 | VI | Xác suất có điều kiện | 18–19 | 64 | B41 |

| Lớp | Số chương | Số bài được đánh số | Phân bố theo hai tập |
| --- | ---: | ---: | --- |
| 10 | 9 | 27 | Tập một: 14; tập hai: 13 |
| 11 | 9 | 33 | Tập một: 17; tập hai: 16 |
| 12 | 6 | 19 | Tập một: 10; tập hai: 9 |
| **Tổng** | **24** | **79** | **6 tập** |

### Hoạt động thực hành và trải nghiệm ngoài số đếm trên

Tên được rút gọn; trang theo mục lục, chưa phải kiểm định nội dung từng hoạt động.

| Sách | Hoạt động và trang in | Nơi dự kiến tích hợp |
| --- | --- | --- |
| S10.1 | Kiến thức tài chính, tr.91; mạng xã hội: lợi và hại, tr.96 | B03, B36 và nhiệm vụ B42 phù hợp |
| S10.2 | Trải nghiệm hình học, tr.90; ước tính số cá thể trong quần thể, tr.93 | B28–B29, B39 và B42 |
| S11.1 | Toán trong tài chính, tr.124; lực căng ngoài của nước, tr.128 | B10, B13–B14; xác định phần toán của hoạt động sau khi đọc |
| S11.2 | Mô hình dùng hàm mũ và lôgarit, tr.99; trải nghiệm hình học, tr.102 | B14–B15, B31–B32 |
| S12.1 | Khảo sát đồ thị với GeoGebra, tr.87; tổng vectơ không gian, tr.92; độ dài gang tay, tr.94 | B21, B33, B38 |
| S12.2 | Nguyên hàm, tích phân và phương pháp hình thang, tr.81; đồ họa 3D, tr.85 | B22–B24, B33–B35 |

Ngoài SGK, CT còn mô tả thực hành công cụ và trải nghiệm ở tr.81, 84, 86–87, 96, 101–103, 107, 109, 111. Các yêu cầu có điều kiện tổ chức trong CT phải giữ đúng điều kiện đó. ZO Math chọn nhiệm vụ tự học phù hợp, không chuyển toàn bộ hoạt động nhà trường thành điều kiện bắt buộc của mỗi bộ.

### A.1. Vị trí ôn của 24 chương

Bảng dưới dùng tên rút gọn để tra cứu. Dải bài theo số đánh trong từng lớp. Đây là chỉ mục nguồn, không phải lịch dạy lại 79 bài.

| Sách / chương | Nội dung nguồn, dải bài | Vị trí ôn chính | Lượt đầu / quay lại trọng điểm |
| --- | --- | --- | --- |
| S10.1 / I | Mệnh đề và tập hợp, bài 1–2 | N, R4; ngôn ngữ điều kiện trong mọi mạch | D0, B.1, B.4; tiếp tục trong C–D |
| S10.1 / II | Bất phương trình hai ẩn, bài 3–4 | R8 | B.1, B.5; C1–C2 |
| S10.1 / III | Hệ thức lượng tam giác, bài 5–6 | R3, R6 | B.3, B.6; C1–C2 |
| S10.1 / IV | Vectơ, bài 7–11 | R3 | B.3, B.8; C1–D |
| S10.1 / V | Dữ liệu không ghép nhóm, bài 12–14 | R2, N | B.2; C1–D |
| S10.2 / VI | Hàm số, đồ thị, dấu và phương trình, bài 15–18 | R1, N, R8 | B.1; B.5, B.7; C–D |
| S10.2 / VII | Tọa độ mặt phẳng và conic, bài 19–22 | R3, R7 | B.3, B.7, B.8; C1–C2 |
| S10.2 / VIII | Đại số tổ hợp, bài 23–25 | R4 | B.4; C1–D |
| S10.2 / IX | Xác suất cổ điển, bài 26–27 | R4 | B.4, B.9; C1–D |
| S11.1 / I | Hàm số và phương trình lượng giác, bài 1–4 | R6, R1, R7 | B.6; B.7, C1–D |
| S11.1 / II | Dãy số, cấp số, bài 5–7 | R5, R4 khi đếm có ràng buộc | B.5; C1–D |
| S11.1 / III | Trung tâm mẫu ghép nhóm, bài 8–9 | R2 | B.2; C1–D |
| S11.1 / IV | Quan hệ song song không gian, bài 10–14 | R3 | B.3, B.8; C1–D |
| S11.1 / V | Giới hạn, liên tục, bài 15–17 | R1, R5 | B.1, B.5; C1–C2 |
| S11.2 / VI | Mũ và lôgarit, bài 18–21 | R5, R1, R7 | B.5; B.7, C1–D |
| S11.2 / VII | Quan hệ vuông góc không gian, bài 22–27 | R3, R7 | B.3, B.8; C1–D |
| S11.2 / VIII | Quy tắc tính xác suất, bài 28–30 | R4 | B.4, B.9; C1–D |
| S11.2 / IX | Đạo hàm, bài 31–33 | R1, R5–R7 | B.1; B.5–B.7; C–D |
| S12.1 / I | Ứng dụng đạo hàm, bài 1–5 | R1, R8 | B.1; C1–D |
| S12.1 / II | Vectơ, hệ trục không gian, bài 6–8 | R3 | B.3, B.8; C1–D |
| S12.1 / III | Phân tán mẫu ghép nhóm, bài 9–10 | R2 | B.2; C1–D |
| S12.2 / IV | Nguyên hàm và tích phân, bài 11–13 | R7, R8 | B.7; C1–D |
| S12.2 / V | Tọa độ không gian, bài 14–17 | R3, R8 | B.8; C1–D |
| S12.2 / VI | Xác suất có điều kiện, bài 18–19 | R4, R2 | B.9; C1–D |

Hoạt động thực hành, trải nghiệm được tích hợp theo mục tiêu: tài chính vào R5/R8; khảo sát dữ liệu vào R2; đo đạc và biểu diễn hình vào R3; mô hình tích lũy vào R7. Thực hành công cụ dùng để tìm hiểu và kiểm tra toán; phần mô phỏng thi chỉ dùng phương tiện được kỳ thi cho phép.

## Phụ lục B. Danh mục cụm nội dung và đối chiếu nguồn

Các mục tiêu dưới đây là diễn giải của ZO Math từ nguồn và thiết kế kế thừa, không phải bản chép từng dòng yêu cầu cần đạt. Bảng định vị tất cả 79 bài vào cụm; chưa chứng minh mỗi yêu cầu đã có học liệu đáp ứng. Các mục tiêu tự kiểm tra, phản biện và liên hệ bổ sung là thiết kế ZO Math, không phải mọi từ trong ô đều được trích từ trang CT được dẫn. “Cần trước” là kiến thức cần có, có thể đáp ứng bằng ôn nhanh hoặc học liệu đã kiểm tra, không bắt xem toàn bộ sản phẩm mang mã ấy.

### B.1. Nền đại số, hàm số, lượng giác, dãy số và mũ–lôgarit

| Mã | Nội dung và mục tiêu | Kiến thức cần trước | CT, trang | SGK đối chiếu |
| --- | --- | --- | --- | --- |
| B01 | **Mệnh đề và tập hợp.** Lập, phủ định và xét đúng/sai mệnh đề; mệnh đề đảo, tương đương, lượng từ, điều kiện cần/đủ; nhận tập con, tập bằng nhau, tập rỗng; thực hiện hợp, giao, hiệu, phần bù và giải thích bằng biểu đồ Ven; ứng dụng đếm phần tử hợp trong bối cảnh | Đọc hiểu, số học THCS | 79 | S10.1 Bài 1–2 |
| B02 | **Biến đổi biểu thức đại số — củng cố THCS.** Rút gọn biểu thức, xử lý phân thức/căn/giá trị tuyệt đối; giữ điều kiện và kiểm tra nghiệm ngoại lai | Đại số THCS; phần điều kiện B01 | Củng cố THCS; liên hệ CT 79–81 | Không có một bài SGK THPT riêng; thêm ôn nhanh nơi cần |
| B03 | **Bất phương trình và hệ bất phương trình bậc nhất hai ẩn.** Nhận diện bất phương trình và hệ; vẽ miền nghiệm; mô hình hóa ràng buộc; tìm cực trị biểu thức bậc nhất trên miền đa giác đơn giản | B01–B02, tọa độ điểm | 79 | S10.1 Bài 3–4 |
| B04 | **Hàm số và đồ thị.** Giải thích điều kiện hàm số; phân biệt tập xác định/tập giá trị; đọc giá trị và khoảng tăng/giảm; nối công thức, bảng, đồ thị và mô hình thực tế | Đại số THCS, đọc tọa độ | 80 | S10.2 Bài 15 |
| B05 | **Hàm số bậc hai.** Tìm đỉnh/trục, xác định giao điểm; dùng dạng biểu thức để giải thích đồ thị và một bài toán thực tế | B02, B04 hoặc phần ôn nhanh tương ứng | 80 | S10.2 Bài 16 |
| B06 | **Dấu của tam thức bậc hai; phương trình quy về phương trình bậc hai.** Lập bảng dấu tam thức; giải bất phương trình; xử lý phương trình quy về bậc hai, kiểm tra điều kiện | B02, B05 | 80–81 | S10.2 Bài 17–18 |
| B07 | **Góc lượng giác và giá trị lượng giác.** Chuyển độ–radian; xác định điểm, dấu và các giá trị liên quan trên đường tròn; nhận biết hệ thức Chasles, bảng giá trị thường gặp và dùng máy tính | Hệ trục, lượng giác tam giác vuông THCS | 89–90 | S11.1 Bài 1 |
| B08 | **Công thức lượng giác và hàm số lượng giác.** Mô tả và dùng công thức cộng, nhân đôi, tích thành tổng, tổng thành tích; kiểm tra một kết quả bằng trường hợp đặc biệt khi phù hợp; nhận diện chẵn/lẻ, tuần hoàn; đọc tập xác định, tập giá trị, biến thiên và đồ thị của bốn hàm lượng giác | B04, B07 | 90 | S11.1 Bài 2–3 |
| B09 | **Phương trình lượng giác cơ bản.** Viết họ nghiệm; chọn nghiệm trong khoảng; giải thích chu kỳ trong tình huống mô hình hóa | B02, B07–B08 | 91 | S11.1 Bài 4 |
| B10 | **Dãy số, cấp số cộng và cấp số nhân.** Nhận diện dãy hữu hạn/vô hạn, các cách cho, tăng/giảm và bị chặn; giải thích số hạng tổng quát, tổng cấp số cộng/nhân, phân biệt tăng theo lượng với tăng theo tỉ lệ và ứng dụng | B02 | 91–92 | S11.1 Bài 5–7 |
| B11 | **Giới hạn của dãy số.** Nhận biết hành vi khi chỉ số tăng; tính các giới hạn trong phạm vi học; xử lý tổng cấp số nhân lùi vô hạn phù hợp | B10 | 92 | S11.1 Bài 15 |
| B12 | **Giới hạn hàm số và hàm số liên tục.** Phân biệt giới hạn với giá trị hàm; kiểm tra giới hạn một bên; xét liên tục tại điểm/khoảng/đoạn, các phép toán và hàm sơ cấp trên miền xác định; có giới hạn tại vô cực và giới hạn vô cực một phía | B04, B06, B11 | 92–93 | S11.1 Bài 16–17 |
| B13 | **Lũy thừa và lôgarit.** Giải thích lôgarit; biến đổi đúng điều kiện; tính và đổi cơ số có mục đích | B02 | 93–94 | S11.2 Bài 18–19 |
| B14 | **Hàm số mũ và hàm số lôgarit.** Đọc tính chất đồ thị; chọn mô hình tăng trưởng/suy giảm; giải thích tham số và đơn vị | B04, B10, B13 | 95 | S11.2 Bài 20 |
| B15 | **Phương trình và bất phương trình mũ, lôgarit.** Chọn phép biến đổi; kiểm tra miền xác định, cơ số và chiều bất đẳng thức; đối chiếu nghiệm với bối cảnh | B06, B13–B14 | 95 | S11.2 Bài 21 |

### B.2. Đạo hàm và tích phân

| Mã | Nội dung và mục tiêu | Kiến thức cần trước | CT, trang | SGK đối chiếu |
| --- | --- | --- | --- | --- |
| B16 | **Khái niệm đạo hàm và ý nghĩa hình học của đạo hàm.** Hiểu bài toán dẫn đến đạo hàm và sự chuyển từ tỉ số thay đổi trung bình đến tức thời; tính một số đạo hàm bằng định nghĩa; giải thích tốc độ, đơn vị, ý nghĩa hình học và lập tiếp tuyến; nhận biết số e qua mô hình lãi suất | B04, B12 | 95–96 | S11.2 Bài 31 |
| B17 | **Các quy tắc tính đạo hàm và đạo hàm cấp hai.** Tính đạo hàm các hàm cơ bản, tổng/hiệu/tích/thương/hàm hợp; chọn quy tắc và kiểm tra kết quả bằng cách khác khi phù hợp; tính đạo hàm cấp hai và giải thích ứng dụng vận tốc–gia tốc; gọi lại ý nghĩa số e ở B16 khi dùng hàm mũ | B02, B08, B13–B16 | 96 | S11.2 Bài 32–33 |
| B18 | **Tính đơn điệu và cực trị của hàm số.** Lập và đọc bảng dấu đạo hàm; kết luận đúng trên từng khoảng; phân biệt điểm có đạo hàm bằng 0 với điểm cực trị | B06, B16–B17 | 105–106 | S12.1 Bài 1 |
| B19 | **Giá trị lớn nhất và giá trị nhỏ nhất của hàm số.** Xét miền hợp lệ, điểm bên trong và biên; giải thích việc có/không có giá trị đạt được; kiểm tra đáp số theo bối cảnh | B18 | 106–107 | S12.1 Bài 2 và 5 |
| B20 | **Đường tiệm cận của đồ thị hàm số.** Tìm và giải thích tiệm cận; phân biệt điểm bị loại với tiệm cận đứng; đối chiếu đồ thị | B04, B12; B17 hỗ trợ khi kết hợp khảo sát | 106 | S12.1 Bài 3 |
| B21 | **Khảo sát sự biến thiên và vẽ đồ thị của hàm số.** Khảo sát ba dạng hàm nêu ở CT tr.106; đọc đối xứng, bảng biến thiên, tiệm cận và đồ thị; vận dụng trong bối cảnh; gắn nhãn các bài tham số mở rộng | B18–B20 | 106–107 | S12.1 Bài 4 và 5 |
| B22 | **Nguyên hàm.** Nhận khái niệm, giải thích tính chất và tìm họ nguyên hàm của các hàm ở CT tr.107/H.3; dùng điều kiện để tìm hằng số; kiểm tra bằng đạo hàm | B17 | 107 | S12.2 Bài 11 |
| B23 | **Tích phân.** Nhận định nghĩa/tính chất và tính tích phân trong phạm vi đã đối chiếu; đọc dấu và đơn vị; liên hệ biến thiên của đại lượng với tích lũy | B12, B22 | 107 | S12.2 Bài 12 |
| B24 | **Ứng dụng hình học của tích phân.** Chọn cận và biểu thức; tách miền khi cần; phân biệt tích phân có dấu với diện tích; lập tích phân tính thể tích phù hợp | B04–B06, B23 | 107 | S12.2 Bài 13 |

### B.3. Hình học, vectơ và tọa độ

| Mã | Nội dung và mục tiêu | Kiến thức cần trước | CT, trang | SGK đối chiếu |
| --- | --- | --- | --- | --- |
| B25 | **Hệ thức lượng trong tam giác.** Đọc giá trị lượng giác góc từ 0 đến 180 độ; giải thích liên hệ phụ/bù, định lí sin/côsin và diện tích; giải tam giác và bài đo đạc, kiểm tra hình có thể tồn tại | Hình học, lượng giác tam giác vuông THCS | 82 | S10.1 Bài 5–6 |
| B26 | **Vectơ và tọa độ trong mặt phẳng.** Hiểu vectơ, vectơ bằng nhau, vectơ-không; cộng/trừ/nhân với số và tọa độ; xét cùng phương, giữ điều kiện khi dùng biểu thức tỉ lệ và xét riêng vectơ-không; dùng cho thẳng hàng, trung điểm, trọng tâm và mô hình lực/chuyển động | B02, đọc tọa độ | 82–83 | S10.1 Bài 7–10 |
| B27 | **Tích vô hướng của hai vectơ.** Tính tích vô hướng theo hai biểu diễn; suy ra độ dài/góc/vuông góc; kiểm tra điều kiện vectơ khác không khi tính góc | B25–B26 | 82–83 | S10.1 Bài 11 |
| B28 | **Phương trình đường thẳng và đường tròn trong mặt phẳng.** Lập phương trình đường thẳng; xét vị trí, góc và khoảng cách; liên hệ hàm bậc nhất; lập đường tròn theo tâm/bán kính hoặc ba điểm, tìm tâm/bán kính và tiếp tuyến tại tiếp điểm | B02, B26–B27 | 83–84 | S10.2 Bài 19–21 |
| B29 | **Ba đường conic.** Nhận biết hình và phương trình chính tắc của elip, hypebol, parabol; giải thích tình huống ứng dụng; các yếu tố sâu hơn thuộc chuyên đề được ghi riêng | B05, B28 | 84 | S10.2 Bài 22 |
| B30 | **Đường thẳng và mặt phẳng; quan hệ song song trong không gian.** Quan hệ điểm–đường–mặt; ba cách xác định mặt phẳng ở CT tr.97, giao tuyến/giao điểm; song song, Thalès, lăng trụ/hộp; phép chiếu song song, ảnh điểm/đoạn/tam giác/đường tròn và hình biểu diễn | Hình học THCS; B26 hữu ích | 97–98 | S11.1 Bài 10–14 |
| B31 | **Quan hệ vuông góc và góc trong không gian.** Nhận diện và chứng minh vuông góc; dùng định lí ba đường vuông góc, hình chiếu; xác định góc đường–đường, đường–mặt và góc nhị diện, góc phẳng nhị diện; tính chất các loại lăng trụ/hộp/chóp ở CT tr.100 | B25, B30 | 99–101 | S11.2 Bài 22–25 |
| B32 | **Khoảng cách và thể tích trong không gian.** Xác định và tính các loại khoảng cách trong trường hợp phù hợp; thể tích chóp, lăng trụ, hộp, chóp cụt đều; kiểm tra đường cao, đơn vị và điều kiện hình | B25, B30–B31 | 99–101 | S11.2 Bài 26–27 |
| B33 | **Vectơ và tọa độ trong không gian.** Biểu diễn điểm/vectơ; tính độ dài, tích vô hướng, góc; chọn tọa độ cho bài hình | B26–B27, B30 | 108 | S12.1 Bài 6–8 |
| B34 | **Phương trình mặt phẳng.** Chọn pháp tuyến; lập phương trình qua điểm/pháp tuyến, điểm/cặp chỉ phương hoặc ba điểm không thẳng hàng; xét vị trí và khoảng cách điểm–mặt phẳng | B31, B33 | 108 | S12.2 Bài 14 |
| B35 | **Phương trình đường thẳng và mặt cầu trong không gian.** Lập đường thẳng, xét vị trí chéo/cắt/song song/vuông góc, tính góc đường–đường/đường–mặt/mặt–mặt; nhận biết và lập mặt cầu, tìm tâm/bán kính; vận dụng đúng phạm vi | B02, B32–B34 | 108–109 | S12.2 Bài 15–17 |

### B.4. Thống kê và xác suất

| Mã | Nội dung và mục tiêu | Kiến thức cần trước | CT, trang | SGK đối chiếu |
| --- | --- | --- | --- | --- |
| B36 | **Số gần đúng, sai số và các số đặc trưng của mẫu số liệu không ghép nhóm.** Số gần đúng, sai số tuyệt đối/tương đối, quy tròn; phát hiện dữ liệu không hợp lý; tính và giải thích trung tâm, độ phân tán của mẫu không ghép nhóm | Số học THCS, B02 | 85–86 | S10.1 Bài 12–14; tích hợp đọc và kiểm tra dữ liệu |
| B37 | **Các số đặc trưng đo xu thế trung tâm của mẫu số liệu ghép nhóm.** Đọc lớp ghép và tần số; ước lượng trung bình, trung vị, tứ phân vị, mốt theo yêu cầu; hiểu kết quả là ước lượng | B36 | 101–102 | S11.1 Bài 8–9 |
| B38 | **Các số đặc trưng đo mức độ phân tán của mẫu số liệu ghép nhóm.** Tính khoảng biến thiên, khoảng tứ phân vị, phương sai, độ lệch chuẩn; so sánh dữ liệu trong cùng bối cảnh và đơn vị | B37 | 110 | S12.1 Bài 9–10 |
| B39 | **Đại số tổ hợp và xác suất cổ điển.** Quy tắc cộng/nhân, cây đếm, hoán vị/chỉnh hợp/tổ hợp; nhị thức Newton với số mũ thấp trong phần chung; không gian mẫu, biến cố đối, tính chất xác suất và nguyên lí xác suất bé; tính xác suất bằng đếm/cây trong mô hình đồng khả năng phù hợp | B01–B02 | 81, 86 | S10.2 Bài 23–27 |
| B40 | **Biến cố và các quy tắc tính xác suất.** Phân biệt hợp/giao/đối; kiểm tra xung khắc và độc lập; chọn công thức cộng/nhân đúng | B39 | 102 | S11.2 Bài 28–30 |
| B41 | **Xác suất có điều kiện, công thức xác suất toàn phần và công thức Bayes.** Giải thích xác suất có điều kiện; đọc bảng 2×2 và sơ đồ cây; mô tả, sử dụng công thức toàn phần/Bayes; phân biệt hai chiều điều kiện và kiểm tra xác suất điều kiện có nghĩa | B40 | 110 | S12.2 Bài 18–19 |

### B.5. B42 — Hồ sơ kết nối và đánh giá tổng hợp

B42 tập hợp các phiếu hỗn hợp, nhiệm vụ mô hình hóa, bài sửa lỗi và đề luyện theo từng đợt. Mỗi phiếu có mã, mục tiêu, các cụm cần trước, nguồn/tác giả, lời giải và phiên bản riêng. B42 là hồ sơ nhiều nhiệm vụ/đề, không tương đương một gói nội dung. R8 sử dụng B42 để phối hợp; câu ở R1–R7 có thể được dùng trong các đề và phiếu này với mã gốc được giữ.

Nhiệm vụ mẫu: nhận ra kiến thức cần dùng khi đề không cho tên chuyên đề; nối đồ thị với dữ liệu; chuyển bài hình sang tọa độ khi phù hợp; kiểm tra mô hình xác suất; làm đề rồi quay lại đúng mục còn yếu. Bắt đầu từ các phần đã hoàn thiện, không chờ cuối mùa.

### B.6. Những cụm cần chia thành bài nhỏ trước khi sản xuất

| Cụm | Cách chia làm việc |
| --- | --- |
| B08 | Công thức lượng giác; hàm số và đồ thị lượng giác |
| B10 | Dãy số; cấp số cộng; cấp số nhân |
| B12 | Giới hạn hàm số; liên tục |
| B13 | Lũy thừa; lôgarit |
| B18 | Đơn điệu; cực trị |
| B28 | Đường thẳng/vị trí/góc/khoảng cách; đường tròn/tiếp tuyến |
| B32 | Khoảng cách; thể tích các khối, gồm chóp cụt đều |
| B35 | Đường thẳng; góc và quan hệ; mặt cầu |
| B36 | Số gần đúng và kiểm tra dữ liệu; xu thế trung tâm; độ phân tán |
| B39 | B39.a đếm; B39.b nhị thức; B39.c xác suất cổ điển |

Mỗi bài nhỏ có một kết quả tự học rõ. Quyết định ghép thành một gói hay nhiều gói sau khi soạn và đo; chưa cộng các bài nhỏ thành một tổng sản phẩm mới.

### B.7. Các ranh giới nội dung cần giữ khi biên soạn

| Điểm cần phân biệt | Cách xử lý |
| --- | --- |
| Nhị thức Newton phần chung và chuyên đề | CT tr.81 nêu khai triển với số mũ thấp, ví dụ 4 hoặc 5; nhị thức tổng quát, tam giác Pascal, tìm hệ số được đọc thêm trong chuyên đề tr.88 |
| Conic phần chung và chuyên đề | CT tr.84 có nhận biết hình, phương trình chính tắc và ứng dụng; các yếu tố đặc trưng sâu hơn trong CT tr.89 được ghi riêng |
| Đạo hàm cấp hai và khảo sát tính cong | CT tr.96 có đạo hàm cấp hai và ứng dụng; không tự suy rằng mọi tiêu chuẩn điểm uốn đều là yêu cầu chung |
| Tối ưu trong phần chung và chuyên đề | B03/B19 có tối ưu phù hợp CT tr.79, 106–107; chuyên đề 12.2 mở rộng bối cảnh và cách vận dụng, không xóa phần tối ưu khỏi lõi |
| Thực hành tính phân bố nhị thức và chuyên đề biến ngẫu nhiên | CT tr.111 có dòng thực hành bằng phần mềm; lý thuyết biến ngẫu nhiên/phân bố thuộc chuyên đề tr.112–113. Giữ cả vị trí và mức yêu cầu, không gộp máy móc |
| Toán cũ và phạm vi hiện tại | Không đưa số phức hoặc nội dung chương trình cũ vào lõi chỉ do quen cấu trúc đề trước đây |

## Phụ lục C. Chuyên đề học tập và phần mở rộng

Danh sách này lấy từ CT, không phải kết quả đã đọc ba cuốn sách Chuyên đề học tập. Chỉ mở một chuyên đề để sản xuất khi đã xác định vai trò trong lộ trình; không gọi toàn bộ là “toán chuyên”.

| Mã trong CT | Tên chuyên đề | Trang CT | Liên hệ với cụm hiện có |
| --- | --- | --- | --- |
| 10.1 | Phương pháp quy nạp toán học. Nhị thức Newton | 87–88 | B01, B10, B39.b |
| 10.2 | Hệ phương trình bậc nhất ba ẩn | 87–89 | B02–B03, bài mô hình hóa |
| 10.3 | Ba đường conic và ứng dụng | 87, 89 | B29 |
| 11.1 | Phép biến hình phẳng | 104 | B28–B29, hoạt động đồ họa |
| 11.2 | Một số yếu tố vẽ kĩ thuật | 104–105 | B30–B32 |
| 11.3 | Làm quen với một số yếu tố của Lí thuyết đồ thị | 104–105 | B42; phân biệt đồ thị trong lý thuyết đồ thị với đồ thị hàm số |
| 12.1 | Biến ngẫu nhiên rời rạc. Các số đặc trưng của biến ngẫu nhiên rời rạc | 112–113 | B39–B41 |
| 12.2 | Ứng dụng toán học để giải quyết một số bài toán tối ưu | 112–113 | B03, B19 |
| 12.3 | Ứng dụng toán học trong một số vấn đề liên quan đến tài chính | 112–114 | B10, B13–B15, B19 |

Liên hệ không có nghĩa cụm hiện tại đã bao phủ đầy đủ chuyên đề. Sách chuyên và tài liệu nâng cao chỉ bổ sung khi có một câu hỏi hoặc mục tiêu cụ thể; không là điều kiện để bắt đầu D0 và R1-G01.

Khi đề thực tế chứa một tình huống có thể giải bằng nội dung chuyên đề, không tự biến toàn bộ chuyên đề thành khóa bắt buộc. Ví dụ dữ liệu dẫn đến hệ ba ẩn có thể được xử lý bằng biến đổi và khử phù hợp; hồ sơ cần chỉ rõ kiến thức dùng và phần cách giải bổ sung. Phạm vi phần chung vẫn được kiểm theo CT, không suy từ tên một bài toán.

## Phụ lục D. Mẫu dùng khi triển khai

Các mẫu dưới đây để ChatGPT chuẩn bị và điền theo công việc thực tế. Người chủ trì không cần tự hoàn thành tất cả biểu mẫu trước phiên đầu. Trường chưa có chứng cứ ghi “chưa xác định”.

### D.1. Chỉ dẫn chung cho Notebook

```text
Bạn đang hỗ trợ tôi học và nghiên cứu toán cho dự án
ZO Math — Ôn thi Toán THPT, ấn bản 2027.
Mục tiêu phiên thuộc gói ôn và mạch R được giao; mã B chỉ phần kiến thức cần đọc.
Bám nhiệm vụ ôn, gọi nền đúng lúc; không tự chuyển thành khóa học tuần tự SGK.

Trước hết, giúp tôi trích xuất và tổ chức nội dung bài học từ các nguồn đã nạp.
Sau đó, cùng tôi đọc, thực hành, đặt câu hỏi và nghiên cứu để hiểu thấu đáo.
Chỉ chuyển sang tạo học liệu thành phẩm khi phạm vi nội dung đã được làm rõ.

Chỉ dùng nguồn căn cứ chính thức đã chọn và bản nội dung ZO Math được ghi nhãn rõ.
Không nạp hay dựa vào đáp án, lời giải AI bên ngoài để thay việc tự giải.
Tự giải từ đề; kiểm điều kiện, trường hợp biên và kiểm tra bằng cách khác khi phù hợp.
Phân biệt nội dung nguồn, diễn giải, đề xuất mới và điểm chưa chắc.
Dẫn đúng nguồn và vị trí; không đoán trang hay bịa trích dẫn.
Giữ đầy đủ điều kiện của công thức và phát biểu toán học.
Khi nguồn đọc không rõ, nêu chính xác chỗ cần kiểm tra.

Viết tiếng Việt rõ ràng, giải thích bằng câu văn và ví dụ có mục đích.
Dùng “suy lí”, “kiến tạo ý nghĩa” đúng ngữ cảnh.
Ưu tiên câu văn thay ký hiệu suy ra/tương đương khi không cần thiết.
Trong bản Markdown dùng $...$, $$...$$; đạo hàm viết f^\prime;
trị tuyệt đối viết \lvert ... \rvert; chỉ dùng \quad nếu cần khoảng cách.

Học sinh tự học bằng học liệu hoàn chỉnh.
Bản ghi quá trình nghiên cứu của tôi là sản phẩm riêng.
Không tự xác nhận tôi đã duyệt nội dung hoặc đã xuất bản.
```

### D.2. Giao Notebook trích xuất cho phiên R1-G01 đầu tiên

```text
Phiên này phục vụ R1-G01 — Kết nối đạo hàm, bảng biến thiên và đồ thị,
thuộc chặng ôn R1 trong kế hoạch ZO Math 2027.
Nguồn là các phần đã nạp từ CT, S12.1 Bài 1 và phần liên quan của Bài 4,
S11.2 Bài 31–32; nền bổ sung chỉ dùng đúng đoạn cần từ hồ sơ nguồn.

Trước hết kiểm tra có đọc được đúng nguồn không. Trích xuất và tổ chức
nội dung để tôi nghiên cứu quan hệ dấu đạo hàm với chiều biến thiên.
Nêu điều kiện, giới hạn của kết luận và dẫn đúng vị trí nguồn.
Cho một nhiệm vụ nối bảng dấu, bảng biến thiên và đồ thị để tôi tự làm;
chưa hiện lời giải. Phân biệt ví dụ nguồn với ví dụ bạn tự tạo.
Nếu phát hiện tôi thiếu kiến thức nền, gọi đúng phần đó rồi trở lại nhiệm vụ.

Chỉ làm phần đầu đủ để tôi đọc và trao đổi. Chưa tạo sản phẩm Studio.
Cuối lượt, giữ các điều đã làm rõ và câu hỏi còn mở cho bản kết tinh.
Không tự coi nội dung trích xuất là đã kiểm định hoặc tôi đã duyệt.
```

### D.3. Học sâu một ý đang vướng

```text
Tôi đang vướng ở: [NÊU Ý HOẶC DÁN LẬP LUẬN].
Hãy dựa vào nguồn của phiên để làm rõ đối tượng và điều kiện đang xét.
Giải thích bằng một mạch lập luận ngắn, có một ví dụ cụ thể.
Nếu cần, đưa một phản ví dụ chỉ đúng chỗ cách hiểu của tôi không còn đúng.

Nếu đây là bài tập tôi đang tự làm, gợi ý bước kế tiếp trước khi đưa lời giải.
Sau khi làm rõ, cho tôi một câu mới để tự kiểm tra.
Ghi nhận điều cần giữ vào bản tổng hợp cuối phiên, chưa chuyển sang sản xuất.
```

### D.4. Kết tinh sau phiên học

```text
Hãy tổng hợp kết quả phiên [MÃ PHIÊN], thuộc [MÃ BỘ].
Giữ các điều đã làm rõ từ trao đổi, đồng thời đối chiếu lại với nguồn.

Chia thành:
- Khái niệm và lập luận đã làm rõ, kèm điều kiện.
- Ví dụ, bài làm và phản ví dụ đã kiểm tra.
- Những cách diễn đạt tôi đã chọn.
- Những câu hỏi còn mở; câu nào ảnh hưởng bản sẽ xuất bản.
- Các mục tiêu học sinh và nhiệm vụ kiểm tra tương ứng.
- Nguồn, trang và phiên bản nội dung đề nghị lưu.
- Một việc tiếp theo duy nhất.

Phân biệt tôi đã hiểu/làm được gì với điều bạn mới đề xuất.
Không ghi “đã duyệt” nếu tôi chưa xác nhận bản cụ thể.
Bản này sẽ được đọc và sửa trước khi dùng làm nguồn cho Studio.
```

### D.5. Giao tạo một sản phẩm từ bản nội dung đã kiểm tra

```text
Tạo [TÊN SẢN PHẨM] cho bộ [MÃ BỘ], phục vụ mục tiêu [MÃ/NỘI DUNG MỤC TIÊU].
Dùng bản nội dung [TÊN, PHIÊN BẢN] và các nguồn [DANH SÁCH] đang được chọn.
Đối tượng là học sinh tự học; kiến thức cần trước là [NỘI DUNG].

Giữ đúng các điều kiện, công thức, mã bài tập và thuật ngữ đã thống nhất.
Những điểm cần có từ quá trình trao đổi đã nằm trong bản nội dung nguồn.
Không tự thêm kết luận chưa có căn cứ để làm sản phẩm đầy đặn hơn.

Sản phẩm cần giúp người học thực hiện hoạt động [MÔ TẢ CỤ THỂ].
Chỉ dẫn về trình bày: [QUY CHUẨN ĐÃ CÓ].
Đánh dấu những chỗ cần kiểm tra lại ở đầu ra; đây vẫn là bản nháp.
```

### D.6. Nhờ ChatGPT kiểm tra và sửa

```text
Đây là sản phẩm [TÊN] của bộ [MÃ], bản [PHIÊN BẢN], kèm nội dung nguồn.
Hãy đọc sản phẩm thực tế, kiểm tra toán, tính nhất quán và khả năng tự học.
Giải lại câu hỏi; đối chiếu điều kiện, hình, dữ liệu, đáp án và lời giải.

Với mỗi lỗi, nêu vị trí, vì sao sai/thiếu, ảnh hưởng và bản sửa cụ thể.
Sửa trực tiếp trong tệp khi bạn có thể làm và kiểm tra được.
Nếu phải sửa trong Notebook, viết một yêu cầu sửa cụ thể để tôi đưa vào đó.
Nếu lỗi có từ bản nội dung nguồn, sửa nguồn trước và chỉ ra sản phẩm bị ảnh hưởng.

Kết thúc bằng bản đã sửa hoặc yêu cầu sửa có thể dùng ngay,
cùng phần đã kiểm tra và phần chưa kiểm tra được.
Không tự xác nhận tôi đã duyệt hoặc báo đã xuất bản.
```

### D.7. Mẫu hồ sơ một bộ và nhật ký phiên

```markdown
# [MÃ BỘ] — [TÊN]

- Ấn bản: 2027
- Phiên bản nội dung:
- Trạng thái thực tế:
- Mục tiêu học sinh và mã mục tiêu:
- Mã yêu cầu đã đối chiếu:
- Mạch R chính/hỗ trợ; mã B của kiến thức dùng:
- Chặng/tuần sử dụng và lượt ôn lại:
- Các bài nhỏ trong bộ:
- Kiến thức cần trước và nơi ôn:
- Phạm vi chung / chuyên đề / củng cố / mở rộng:
- Nguồn, phiên bản, trang in, trang PDF:
- Nội dung ZO Math dùng lại và bản nguồn:
- Câu hỏi nghiên cứu:
- Điểm đã làm rõ:
- Điểm còn mở và ảnh hưởng:
- Mã câu đầu vào / luyện / cuối bài / sau sửa lỗi:
- Lõi bắt buộc và sản phẩm hỗ trợ đã chọn:
- Các sản phẩm, phiên bản, trạng thái kiểm định:
- Giờ dự kiến / thực tế theo từng khâu:
- Thời gian tự học dự kiến / thực tế nếu có:
- Notebook, nguồn đã nạp và kết quả thử đọc:
- Người chủ trì đã xem/duyệt bản nào: chưa xác định
- URL thật hoặc “chưa xuất bản”:
- Việc tiếp theo:

## Phiên [MÃ], ngày [NGÀY]

- Phạm vi đã học:
- Bài đã tự làm / đã xem lời giải:
- Điều đã kiểm tra, bằng cách nào:
- Điều chưa kiểm tra:
- Quyết định diễn giải và thay đổi nguồn:
- Giờ học / tổng hợp / sản xuất / kiểm định / đóng gói:
- Tệp mới nhất, phiên bản và nơi đang dừng:
- Phần đã sửa và quyết định ảnh hưởng sản phẩm khác:
- Điều không cần làm lại:
- Một việc kế tiếp:
```

### D.8. Mẫu hàng đối chiếu yêu cầu

| Mã nội bộ | Nguồn, trang | Yêu cầu diễn giải | Mục tiêu gói / kiến thức | Nhiệm vụ | Thành phẩm | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| YC-B18-01 | CT tr.105–106; S12.1 Bài 1 | Dùng dấu đạo hàm để xét đơn điệu trên khoảng phù hợp | R1-G01-M2; B18 | Bảng dấu và kết luận có/không đủ điều kiện | Theo gói thực tế khi sản xuất | Đã có vị trí thiết kế |
| YC-B04-01 | CT tr.80; S10.2 Bài 15 | Giải thích điều kiện đầu ra duy nhất trong mô hình hàm số | N hỗ trợ R1-G01-M1; B04 | Quan hệ có/không xác định hàm, kèm lý do | Phiếu nền khi cần | Đã có vị trí thiết kế |

Các hàng là ví dụ thiết kế. Khi sản xuất, xác nhận trang SGK thực dùng, tách từng yêu cầu liên quan và gắn câu đã soạn; không lấy ví dụ làm bằng chứng hoàn thành ma trận hoặc học liệu.

### D.9. Giao đóng gói và tiếp tục sau gián đoạn

```text
Hãy đóng gói bộ [MÃ] từ các tệp [DANH SÁCH] ở phiên bản [PHIÊN BẢN].
Kiểm tra có đủ bài học, phiếu, lời giải, tự kiểm tra và sản phẩm đã chọn không.
Đối chiếu phiên bản nội dung, trạng thái kiểm định và thông tin duyệt thực tế.
Tạo danh sách thành phần, mô tả trang học, chỉ dẫn sử dụng và việc còn thiếu.
Chưa công bố nếu phạm vi công bố và bản cụ thể chưa được duyệt.
```

```text
Tiếp tục dự án ZO Math — Ôn thi Toán THPT theo kế hoạch và hồ sơ tôi gửi.
Đọc trạng thái mới nhất, giữ các quyết định đã ghi và xác định nơi đang dừng.
Tự làm phần bạn truy cập và xử lý được; không bắt tôi tạo lại hồ sơ đã có.
Không coi ghi chú kế hoạch là hành động đã hoàn thành.
Kiểm tra đầu ra thực tế và không làm lại phần đã có đủ bằng chứng.
Mỗi bản kế hoạch/nội dung chỉnh sửa phải đủ để đọc độc lập, giữ mọi chi tiết
còn giá trị và tích hợp các quyết định mới vào đúng phần áp dụng.
Tiếp tục đúng việc kế tiếp, cập nhật tệp và cho tôi một bước cần làm nếu có.
```

### D.10. Mẫu hồ sơ nguồn

```markdown
# [MÃ NGUỒN] — [TÊN ĐẦY ĐỦ]

- Tác giả/cơ quan:
- Loại tài liệu và vai trò:
- Từng phần: bản phát hành / bản scan lưu lại / bản chép / ghi chú ZO Math:
- Trang nguồn cha và trang tệp đã tách; thay đổi nếu có:
- Căn cứ xác minh xuất xứ; phần chưa đối chiếu:
- Năm, lần in hoặc phiên bản:
- Trang công bố và xuất xứ:
- Tên tệp/bản thực tế đang dùng:
- Ngày truy cập/đọc:
- Phần cần dùng, trang in và trang PDF:
- Cụm B, mạch R, gói và mục tiêu liên quan:
- Trạng thái theo phần: T0/T1/T2/T3; thử Notebook T4 ghi riêng
- Đã đọc/đối chiếu cụ thể, bằng cách nào:
- Điểm chưa đọc rõ hoặc còn mâu thuẫn:
- Notebook đã nạp bản nào, ngày nào:
- Câu thử nguồn và kết quả:
- Nội dung là trích nguyên văn / diễn giải / ví dụ mới:
- Lưu ý sử dụng và trích dẫn:
- Khi thay nguồn: đoạn thay đổi và sản phẩm cần rà:
- Việc tiếp theo:
```

### D.11. Bảng tiến độ và phản hồi

Các dòng dưới ghi trạng thái thiết kế hiện tại. Khi triển khai, cập nhật bằng tệp và kết quả thực, tách tiến độ sản xuất khỏi kết quả học sinh.

| Gói | Phạm vi / chặng dùng | Nguồn | Trạng thái thành phẩm | Duyệt / công bố | Giờ thực | Việc kế tiếp |
| --- | --- | --- | --- | --- | --- | --- |
| D0 | Tám mạch, khi gia nhập | CT/SGK; bốn PDF ở 11.6 | Đã hoàn tất v1.0 | Đã đưa vào Nguồn theo người chủ trì; không suy đã công bố web | Chưa có số giờ được cung cấp | Dùng bộ hiện hành và đính chính chỉ dẫn |
| R1-G01 | Đạo hàm–biến thiên–đồ thị, chặng B.1 | Định vị nguồn ở 6.2 và 11.2 | Chưa sản xuất | Chưa có bản để duyệt/công bố | Chưa đo | Chuẩn bị nguồn/ma trận cho phiên nghiên cứu đầu tiên |

| Ngày | Mạch / mục tiêu | Phạm vi đã học | Mã câu và phiên bản | Lỗi / bằng chứng | Câu thử lại và ngày | Quyết định ôn |
| --- | --- | --- | --- | --- | --- | --- |
| Điền khi có bài làm | Ghi cụ thể | Tách phần chưa học | Dùng mã thật | Giữ bài làm; ghi câu đúng do đoán | Câu mới cùng mục tiêu | Tối đa hai ưu tiên |

Lần nâng kế hoạch này chưa được cung cấp dữ liệu học sinh để ghi kết quả thực nghiệm. Thêm dòng khi có công việc thật, không tạo hàng chục trạng thái trống để thay cho triển khai.

### D.12. Mẫu hồ sơ câu hỏi và lỗi

```markdown
# [MÃ CÂU] — phiên bản [SỐ]

- Bộ/bài nhỏ:
- Mục tiêu và yêu cầu nguồn liên quan:
- Mạch R chính/hỗ trợ, cụm B, gói và chặng sử dụng:
- Vai trò: đầu vào / luyện / kiểm tra cuối / sau sửa lỗi
- Định dạng trả lời và quy tắc chấm:
- Đã xuất hiện trong tài liệu luyện nào; có còn dùng đo tiến bộ độc lập được không:
- Năng lực cần quan sát:
- Cấp độ tư duy dự kiến và lý do (tách khỏi định dạng trả lời):
- Mã họ câu; biến thể/hoán vị và lịch sử đã gặp:
- Điểm từng ý để chẩn đoán; điểm mô phỏng theo quy tắc cả câu:
- Nguồn hoặc tác giả; phần tự biên soạn:
- Đề bài, hình/bảng và điều kiện:
- Đáp án:
- Lời giải, cách chọn hướng và cách giải khác phù hợp:
- Tiêu chí xem bài làm; đơn vị/làm tròn nếu có:
- Lỗi thường gặp và nơi quay lại học:
- Câu mới để thử sau sửa lỗi:
- Đã giải kiểm tra bằng cách nào, ngày nào:
- Kết quả và điểm chưa chắc:
- Những sản phẩm đang dùng câu này:
- Thay đổi phiên bản và lý do:
```

```markdown
# Lỗi [MÃ LỖI]

- Phát hiện ngày:
- Bộ, câu/sản phẩm, phiên bản và vị trí:
- Mô tả lỗi và bằng chứng:
- Ảnh hưởng: toán / thiếu nội dung / diễn đạt / hình thức
- Có chặn đóng gói hoặc cần đính chính công khai không, vì sao:
- Bản sửa nội dung gốc:
- Các sản phẩm cần cập nhật:
- Đã sửa những bản nào:
- Đã kiểm tra lại những bản nào, bằng cách nào:
- Trạng thái người chủ trì xem/duyệt thực tế:
- Cách tránh lặp lại:
```

### D.13. Mẫu danh sách thành phần và duyệt gói

```markdown
# Gói [ẤN BẢN]_[MÃ BỘ]_[PHIÊN BẢN GÓI]

- Mục tiêu và người học:
- Mạch R, mã B liên quan, chặng dùng và lịch ôn lại:
- Bản nội dung nguồn:
- Phạm vi công bố đề nghị:
- Trang học: URL thật hoặc chưa xuất bản
- Ngày lập gói:
- Người chủ trì đã xem bản nào: chưa xác định
- Quyết định duyệt, ngày và phạm vi: chưa có xác nhận
- Việc còn thiếu hoặc sản phẩm ra sau:

| Tệp | Vai trò | Bản thành phẩm | Bản nội dung nguồn | Kiểm định | Duyệt thực tế | Nơi công bố |
| --- | --- | --- | --- | --- | --- | --- |
| Điền tên thật | Bài/phiếu/lời giải/sản phẩm hỗ trợ | Điền bản thật | Điền bản thật | Ghi chứng cứ | Chưa xác định | Chưa xuất bản |

- Chỉ dẫn học sinh bắt đầu và dùng từng sản phẩm:
- Mô tả trang học:
- Mô tả/mốc video nếu có:
- Nguồn cần ghi ở phần công khai:
- Kết quả kiểm tra mở tệp, công thức, hình và liên kết:
- Một việc tiếp theo:
```

### D.14. Giao ChatGPT chuẩn bị nguồn và ma trận

```text
Thực hiện bước chuẩn bị nguồn cho [MÃ GÓI] của ZO Math — Ôn thi Toán THPT
theo kế hoạch 0.6 hoặc bản hiện hành mới hơn. Với R1-G01, dùng mục 6.2 và 11.2;
định vị CT tr.95–96, 105–107; S12.1 Bài 1 và phần liên quan của Bài 4,
S11.2 Bài 31–32. Gọi nền B04/B06/B12 đúng nhu cầu, không dạy lại tuần tự SGK.

Đọc phần liên quan, ghi tên tệp/phiên bản, trang in và trang PDF.
Tách từng yêu cầu, phân biệt diễn giải với trích nguyên văn; ghép mục tiêu,
kiến thức cần trước, nhiệm vụ dự kiến và phần còn thiếu; nối nhóm H-YC liên quan.
Phân biệt yêu cầu CT (A), nguồn học tập đã đọc (B) và cách tổ chức của ZO Math (C).
Đừng coi mục lục là bằng chứng đã kiểm tra nội dung cả bài.

Chuẩn bị hồ sơ nguồn, phiếu ôn nhanh cần thiết và một yêu cầu trích xuất
vừa đủ cho phiên học đầu. Chuẩn bị phép thử Notebook đọc nguồn.
Tự làm phần bạn truy cập và kiểm tra được; nếu cần tôi cung cấp thêm,
nêu đúng tài liệu/phần còn thiếu và mục đích, chỉ hỏi việc thực sự cần.
Kết thúc bằng tệp cụ thể và một bước kế tiếp.
```

### D.15. Giao thiết kế bộ học liệu từ nội dung đã kết tinh

```text
Thiết kế bộ [MÃ] từ bản kết tinh [TỆP/PHIÊN BẢN], hồ sơ nguồn và ma trận
đã cung cấp. Giữ các cách diễn giải tôi đã chọn; phần mới đề xuất ghi rõ.

Soạn bài tự học, kiến thức cần trước, ví dụ, phản ví dụ, phiếu luyện,
lời giải, kiểm tra đầu vào/cuối và chỉ dẫn học sau sửa lỗi.
Chia Nền tảng – Vận dụng – Đào sâu theo mục tiêu, không gắn nhãn học sinh.
Gắn mã từng câu với mục tiêu, mạch R, cụm B và chặng sử dụng.
Giữ lịch ôn lại và câu mới sau chữa; số câu theo ma trận, không áp định mức chung.
Giữ các chi tiết cần thiết để học sinh sử dụng khi chưa xem video quá trình.

Đọc lại nguồn nếu phát hiện mâu thuẫn, đánh dấu chỗ cần quay lại nghiên cứu.
Chọn sản phẩm Studio theo tác dụng và chuẩn bị đầu vào từ bản đã kiểm tra.
Chưa coi bản mới sinh là bản đã duyệt hoặc đã xuất bản.
```

### D.16. Giao tích hợp trong repo ZO Math

```text
Làm trong repo ZO Math hiện tại với nhiệm vụ: tích hợp bộ [MÃ] từ gói
[TÊN/PHIÊN BẢN] tôi cung cấp. Đọc AGENTS.md và quy trình QMD, hình, PDF,
xuất bản đang áp dụng trước khi sửa; xác định đường dẫn từ repo thực tế.

Giữ quy chuẩn trình bày và thuật ngữ; chọn cách dùng chung nội dung để
không tạo nhiều bản sao sửa lệch nhau. Chỉ thay phần phục vụ bộ ôn thi này.
Không mở nhiệm vụ đổi tên hoặc tinh chỉnh toàn dự án 100+ Hàm số.

Chuẩn bị trang và tài liệu tải từ các bản đã kiểm định; kiểm tra đầu ra
bị ảnh hưởng. Ghi tệp đã sửa, bản đã xem, cách kiểm tra và lỗi còn lại.
Việc công bố theo phạm vi đã được người chủ trì giao và quy trình hiện hành.
Nếu cần quyết định mới, hoàn thành bản cụ thể để xem trước khi hỏi.
Không ghi đã công bố khi chưa có URL thực tế và kết quả kiểm tra.
```

### D.17. Giao hiệu chỉnh kế hoạch theo nguyên tắc thay thế đầy đủ

```text
Hiệu chỉnh bản kế hoạch mới nhất theo các góp ý tôi cung cấp.
Bản mới phải đủ để đọc và sử dụng độc lập, thay thế hoàn toàn bản trước.
Giữ trọng tâm ôn thi; kiểm tra ánh xạ R–B, lịch ôn và lịch sản xuất, điểm bắt đầu
D0/R1-G01 hoặc quyết định mới thay thế; cập nhật mọi prompt bị ảnh hưởng.

Đối chiếu từng phần: giữ nội dung còn giá trị, tích hợp quyết định mới
ngay tại nơi áp dụng, sửa nội dung sai/lỗi thời, bỏ phần trùng khi vẫn
giữ đủ ý nghĩa và chi tiết cần thiết. Không tự chuyển bản chi tiết thành tóm tắt.
Nếu bỏ một giả thiết, viết rõ quy tắc hiện hành thay thế để vẫn làm theo được.

Kiểm tra phần có thể bị mất, mâu thuẫn giữa các bảng, tham chiếu nội bộ,
trạng thái đã làm/chưa làm và điểm bắt đầu tiếp theo.
Chỉ ghi mức kiểm chứng nguồn đúng với bằng chứng đang có.
Xuất một tệp Markdown thống nhất và cập nhật phiên bản, nhật ký trong tệp.
Không yêu cầu đọc lại bản trước hoặc lịch sử trò chuyện để hiểu quyết định.
```

### D.18. Giao sử dụng D0 v1.0 để định vị một học sinh

```text
Dùng bộ D0 v1.0 đã hoàn tất và Kế hoạch 0.6, mục 11.1/11.6.
Đọc phần học sinh đã học, bài làm và quỹ giờ được cung cấp. Chọn câu phù hợp,
giữ CH/KCG, lịch sử gặp câu, trợ giúp/đoán và thời gian. Không soạn lại D0.
Phân tích theo tiêu chí của bộ hiện hành; chưa đủ bằng chứng thì ghi rõ.
Trả tối đa hai ưu tiên sửa, câu thử lại và ngày hẹn; nối lịch cá nhân 12.10.
B.8 của lịch tham chiếu là tọa độ trong không gian Oxyz theo đính chính 11.6.
Không quy kết ba câu thành mức toàn mạch, không dự báo điểm thi từ D0.
Chỉ đề xuất sửa thành phẩm khi có lỗi cụ thể, ghi trang/câu/tác động;
không bịa bài làm, không thay trạng thái D0 v1.0 đã hoàn tất.
```

### D.19. Rà tuần ôn và điều chỉnh theo bài làm

```text
Đọc lịch cá nhân đang dùng theo 12.10–12.13, đối chiếu mẫu 12.2
và hồ sơ bài làm tôi cung cấp.
Tách phần chưa học, phần làm đúng độc lập, câu đoán và lỗi thực tế.
Theo quy tắc ở 5.4, chọn tối đa hai ưu tiên sửa trong tuần tiếp theo.
Giữ phần ôn lại ở 12.9, không thay toàn bộ tuần bằng một bài yếu duy nhất.
Ghi rõ nhiệm vụ trọng tâm, câu mới sau chữa, ngày thử lại và tiêu chí tiến tiếp.
Nếu đổi lịch, nêu nguyên nhân và các hàng phụ thuộc cần dịch.
Không bịa điểm, thời gian học hoặc kết quả tiến bộ khi không có bài làm.
```

### D.20. Lập hoặc cập nhật lịch cá nhân

```text
Dùng Kế hoạch 0.6, mục 12.10–12.13. Với ngày gia nhập, mốc thi (ghi rõ
chính thức hay giả định), giờ học từng tuần, lịch trường và bài làm được cung cấp,
tính quỹ giờ thực; dùng D0 v1.0 để định vị, giữ cờ chưa học/chưa giao.
Lập sổ mục tiêu B còn thiếu, tiên quyết và các mạch cần có vị trí.
Lập chi tiết hai tuần gần nhất, các mốc sau đến thi; dành giờ chữa/gọi lại.
Kiểm tổng giờ, không đếm hai lần R8. Giảm sâu, vòng luyện và số đề trước
khi giảm vùng kiến thức. Nếu vẫn thiếu thời gian, ghi đúng mục tiêu chưa có chỗ.
Không bịa lịch trường, ngày thi, bài làm hoặc chứng nhận làm chủ.
```

### D.21. Xử lý một công bố mới về kỳ thi

```text
Đọc nguồn chính thức được cung cấp và hồ sơ cấu hình tại 3.14.
Xác nhận ngày, đối tượng, hiệu lực; phân biệt dự thảo/thí điểm/áp dụng chính thức.
Nêu trường nào thay đổi và văn bản nào xác nhận. Theo 12.14, liệt kê mã
nội dung, đánh giá, đề/phiếu và lịch chịu ảnh hưởng; chỉ sửa phần có căn cứ.
Giữ bản cũ, lập cấu hình mới và tiêu chí kiểm lại. Không tự suy đổi hình thức
thành đổi kiến thức hoặc dùng một thông tin thí điểm cho mọi học sinh.
```

### D.22. Hồ sơ quyết định và nghiên cứu

| Trường | Nội dung phải ghi khi có quyết định thật |
| --- | --- |
| Quyết định / ngày / người quyết định | Mã C, vấn đề cụ thể, phiên bản đang dùng |
| A | Cơ quan, văn bản, trang/điều khoản, phạm vi áp dụng; nếu không liên quan ghi rõ |
| B | Công trình/DOI/URL, phần đã đọc, đối tượng/nhiệm vụ, kết quả và giới hạn |
| C | Lựa chọn ZO Math, lý do, tham số, điều kiện điều chỉnh |
| Tác động | D0, R, B, lịch, cấu hình thi, gói/câu, công bố |
| Kiểm tra | Nhiệm vụ/bằng chứng để xem quyết định có phù hợp; dữ liệu chưa có không điền giả |
| Trạng thái | Đang thử / đã điều chỉnh / thay thế; liên kết lịch sử |

## Phụ lục E. Tệp nguồn và tham chiếu

### E.1. Bảy tệp nền do người chủ trì cung cấp

Tên dưới đây là tên tệp đã cung cấp cho dự án, để tìm đúng bản. Không cần tải lại chỉ vì tên có hậu tố “(1)”.

| Mã | Tên tệp |
| --- | --- |
| CT | `Chuong trinh giao duc pho thong mon Toan 2018(1).pdf` |
| S10.1 | `Toan 10 - Tap 1 - Ket noi tri thuc voi cuoc song.pdf` |
| S10.2 | `Toan 10 - Tap 2 - Ket noi tri thuc voi cuoc song(1).pdf` |
| S11.1 | `Toan 11 - Tap 1 - Ket noi tri thuc voi cuoc song.pdf` |
| S11.2 | `Toan 11 - Tap 2 - Ket noi tri thuc voi cuoc song.pdf` |
| S12.1 | `Toan 12 - Tap 1 - Ket noi tri thuc voi cuoc song(1).pdf` |
| S12.2 | `Toan 12 - Tap 2 - Ket noi tri thuc voi cuoc song(1).pdf` |

### E.2. Tài liệu được dùng để viết lại quy trình

- Bản 0.3 kế thừa các thiết kế 0.1–0.2 và bản Lộ trình toàn cảnh 1.0 được tích hợp vào 0.4. Các tệp trước chỉ thuộc lịch sử biên tập, không phải tài liệu người đọc cần mở kèm.
- Các quyết định bổ sung trong cuộc trao đổi hiện tại, đặc biệt trình tự học trước–sản xuất sau, dùng Mind Map linh hoạt và đóng gói chờ xuất bản.
- Năm ghi chú tham khảo: *Gemini Notebook — Cấu trúc hỗ trợ học tập kỹ thuật số*; *Kiến trúc Hệ thống và Tư duy Sư phạm ZO Math*; *ZO Math — Cẩm nang Thương hiệu*; *Tiến trình Vàng Chế tác Học liệu Toán học ZO Math*; *Quy trình 5 Bước Chế tác Học liệu ZO Math*.

Những ý có ích của các ghi chú đã được tích hợp vào mục 6–10; người đọc không cần truy cập sổ của dự án khác để làm theo kế hoạch. Những ghi chú này được chọn lọc theo quyết định của người chủ trì, không được dùng như chứng nhận khoa học hoặc tài liệu kỹ thuật chính thức. Chưa dùng các số trích dẫn NCTM trong ghi chú làm dẫn chứng độc lập vì chưa đối chiếu được các đoạn nguồn tương ứng trong lần này.

### E.3. Nguồn web đã dùng

Danh sách này giữ cả dấu vết tra cứu từ các lần trước. Bản chữ trên trang thứ sinh chỉ là lịch sử, không thuộc nguồn căn cứ hoạt động theo 3.6; không nạp vào Notebook. Mức đã đọc và giới hạn được ghi ngay tại mục 3.4 và mục 6–8. Các nguồn về công cụ là thông tin tại thời điểm kiểm tra, không phải cam kết tính năng hoặc hạn mức sẽ giữ nguyên suốt mùa 2027.

- [Thông tư 17/2025/TT-BGDĐT — trang công bố Chính phủ](https://vanban.chinhphu.vn/?docid=215347&pageid=27160); [PDF đính kèm](https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/9/17-bgddt.pdf).
- [Thông tư 13/2022/TT-BGDĐT — bản toàn văn dạng chữ đã đọc](https://thuvienphapluat.vn/van-ban/Giao-duc/Thong-tu-13-2022-TT-BGDDT-sua-doi-Thong-tu-32-2018-TT-BGDDT-Chuong-trinh-giao-duc-524666.aspx); [trang trường Tân Túc có PDF bản gốc](https://thpttantuc.hcm.edu.vn/van-ban-cong-van/thong-tu-so-132022tt-bgddt-ngay-03-thang-8-nam-2022-sua-doi-bo-sung-mot-so-noi/vbctmb/42711/461254).
- [Thông tư 20/2021/TT-BGDĐT — trang công bố Chính phủ](https://vanban.chinhphu.vn/default.aspx?docid=203766&pageid=27160).
- [Cục QLCL — công bố định dạng thi từ 2025](https://vqa.moet.gov.vn/vi/news/thong-bao/cau-truc-dinh-dang-de-thi-tot-nghiep-thpt-tu-nam-2025-74.html).
- [Cục QLCL — thông tin đề án thi trên máy tính, 29/07/2026](https://vqa.moet.gov.vn/vi/news/tin-tuc-su-kien/bo-gddt-noi-gi-ve-de-an-to-chuc-thi-tot-nghiep-thpt-tren-may-tinh-286.html).
- [Google — thêm và quản lý nguồn](https://support.google.com/gemininotebook/answer/16215270?hl=en).
- [Google — tạo ghi chú và chuyển thành nguồn](https://support.google.com/gemininotebook/answer/16262519?hl=en).
- [Google — sử dụng Mind Map](https://support.google.com/gemininotebook/answer/16212283?hl=en).
- [Google — danh mục trợ giúp Gemini Notebook và Studio](https://support.google.com/gemininotebook/?hl=en).

### E.4. Đối chiếu đề thực tế và tác động đến lộ trình

Đã đọc toàn bộ bốn trang của **mã 0101 năm 2025** và **mã 0101 năm 2026**, dùng bản đề được lưu tại TOANMATH. Các trang lời giải đính kèm không được coi là đáp án của Bộ. Riêng tệp 2026 ghi phần hướng dẫn giải do AI tạo; lộ trình sử dụng trang đề để nhận diện nhiệm vụ, không lấy phần đó làm chuẩn chấm.

| Đề / vị trí | Nội dung quan sát được | Quyết định thiết kế từ việc đối chiếu |
| --- | --- | --- |
| 2025, I.7; I.10 | Phương trình lượng giác; phương trình lôgarit | Giữ R5–R6 trong các lượt ôn lại |
| 2025, III.3 | Bài toán bán hàng có ràng buộc | Đưa bất phương trình hai ẩn vào R8 |
| 2025, III.6 | Thể tích kết nối hình khối và phần bị khoét | Luyện phối hợp R3–R7 |
| 2026, I.12 | Trung vị từ dữ liệu ghép nhóm | Duy trì R2 từ đầu đến đề tổng hợp |
| 2026, II.1 | Xác suất có điều kiện từ bảng dữ liệu | Luyện R4 gắn đọc dữ liệu và đổi điều kiện |
| 2026, III.3 | Elip và thể tích khối tròn xoay có lỗ khoan | Giữ conic làm cầu nối R3–R7 |
| 2026, III.6 | Tối ưu lợi nhuận | Đưa R1–R8 vào bài không nêu phương pháp |

Nguồn: [bản đề 2025, bốn trang đầu](https://toanmath.com/toanmath-pdf/de-chinh-thuc-ky-thi-tot-nghiep-thpt-nam-2025-mon-toan.pdf); [bản đề 2026, bốn trang đầu](https://toanmath.com/toanmath-pdf/de-chinh-thuc-ky-thi-tot-nghiep-thpt-nam-2026-mon-toan.pdf).

Hai mã đề là bằng chứng về dạng nhiệm vụ và sự kết nối kiến thức; chúng không đủ để suy ra tần suất ra đề 2027, phân bố điểm cố định hoặc bảo đảm rằng nội dung nào sẽ không thi. Lộ trình được xây từ chương trình và quan hệ kiến thức; đề thực tế dùng để kiểm tra thiết kế có sát việc làm bài hay không.

Đã tìm nguồn [đáp án Toán 2026 do Bộ công bố, được Cổng Thông tin điện tử Chính phủ đăng lại](https://xaydungchinhsach.chinhphu.vn/thi-tot-nghiep-thpt-2026-de-thi-mon-toan-vua-suc-co-tinh-phan-hoa-ro-ret-119260611164121523.htm). Đây là ghi nhận nguồn đã tìm trong lịch sử. Quy tắc hiện hành tại 3.6 và 9.9 dùng đề để tự giải, kiểm chứng và biên soạn lời giải; không yêu cầu nạp bảng đáp án này vào nguồn nghiên cứu.

### E.5. Nguồn bổ sung trong lần nghiên cứu lộ trình ngày 09/09/2026

- [Quy chế thi hợp nhất 2026, Điều 4–5](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/4/02-vbhn-bgddt-kem.pdf).
- [Cách chấm ba dạng trắc nghiệm được Cổng TTĐT Chính phủ nêu trong thông tin kỳ thi 2026](https://xaydungchinhsach.chinhphu.vn/thi-tot-nghiep-thpt-2026-de-thi-mon-ngu-van-11926061110312488.htm).
- [Đáp án Toán 2026 do Bộ công bố, bản PDF được đăng lại](https://xdcs.cdnchinhphu.vn/446259493575335936/2026/6/20/2-dap-an-toan-thitotnghiep2026-17819158422951697488013.pdf).
- [Hướng dẫn quản lý chất lượng năm học 2026–2027, có nội dung chuẩn bị thí điểm thi trên máy tính](https://vqa.moet.gov.vn/vi/news/tin-tuc-su-kien/bo-gddt-huong-dan-thuc-hien-nhiem-vu-quan-ly-chat-luong-nam-hoc-2026-2027-294.html).

Không có dự báo tỉ trọng câu, điểm hoặc nội dung cụ thể sẽ xuất hiện năm 2027 trong kế hoạch này. Khi công bố đề mô phỏng, kiểm tra lại nguồn áp dụng và ngày cập nhật; các kết luận của 2025–2026 không tự trở thành quy định mới.

### E.6. Đánh giá tám tài liệu bổ sung và quyết định sử dụng

Mã N01–N08 dưới đây chỉ tám tệp bổ sung, không thay nhãn N của phần nền kiến thức. Số trang là trang PDF tính từ 1. Đã đọc các phần nêu trong bảng; đây là kiểm kê nguồn và nhiệm vụ, chưa là bộ lời giải đã kiểm định.

| Mã và tên tệp người chủ trì gửi | Nội dung thực tế | Quyết định cho dự án và Notebook |
| --- | --- | --- |
| N01 — Đề chính thức kỳ thi tốt nghiệp THPT năm 2025 môn Toán.pdf | 17 trang: tr.1–4 mã 0101, 5–8 mã 0102, 9–12 mã 0103, 13–16 mã 0104; tr.17 bảng đáp án | Giữ 16 trang đề trong nguồn làm việc. Bảng đáp án đã có trong bản gốc nhưng không nạp. Quản lý họ câu giữa các mã |
| N02 — Đề chính thức kỳ thi tốt nghiệp THPT năm 2026 môn Toán.pdf | 12 trang: tr.1–4 bản scan đề mã 0101; tr.5–12 phần giải ghi do AI Gemini thực hiện | Chỉ dùng bốn trang đề; lời giải ngoài bị loại khỏi nguồn làm việc |
| N03 — Đề chính thức kỳ thi tốt nghiệp THPT năm 2026 lần 2 môn Toán.pdf | 14 trang: tr.1–4 bản đánh máy mã 0110, tr.5 bảng đáp án, tr.6–14 lời giải AI | Giữ bản gốc như ứng viên tra cứu; chưa đưa vào gói khởi động vì chưa đối chiếu bản chép với bản phát hành. Không dùng bảng đáp án/lời giải làm chuẩn |
| N04 — Đề thi tham khảo tốt nghiệp THPT từ năm 2025.pdf | 5 trang: tr.1–4 đề, tr.5 đáp án/cách chấm | Dùng bốn trang đề để nghiên cứu nhiệm vụ; quy tắc chấm nằm tại 3.10, không cần nạp bảng kết quả |
| N05 — PHƯƠNG ÁN TỔ CHỨC THI, XÉT CÔNG NHẬN TỐT NGHIỆP THPT từ năm 2025.pdf | 10 trang bản in bài báo tổng hợp, có nội dung lịch sử và diễn giải | Không đưa vào nguồn căn cứ; dùng văn bản gốc và hướng dẫn năm tương ứng |
| N06 — Phiếu trả lời trắc nghiệm.pdf | 2 trang, sáu ô số báo danh và ba ô mã đề | Không dùng cho các mã đề bốn chữ số đang luyện. Thay bằng mẫu Công văn 1239 như 9.8 |
| N07 — Quyết định số 4068 của Bộ Giáo dục và Đào tạo về việc phê duyệt Phương án tổ chức kỳ thi và xét công nhận tốt nghiệp trung học phổ thông từ năm 2025..pdf | 4 trang bản scan; ngày 28/11/2023; quyết định và phương án kèm theo | Giữ làm văn bản nền lịch sử; không dùng riêng lộ trình máy tính trong văn bản này để quyết định hình thức thi 2027 |
| N08 — Đề minh họa Đề kiểm tra lớp 10.pdf | 6 trang: tr.1–4 đề; tr.5 đáp án; tr.6 ma trận minh họa năng lực, mức tư duy và dạng câu | Tách đề và ma trận thành hai nguồn. Chọn câu nền cho D0, không coi là khảo sát đủ THPT |

**Mức xác minh xuất xứ:** các phần đề scan N01–N02 được đọc trực tiếp; hồ sơ công bố chính thức được đối chiếu như E.4–E.5. N04 đã đọc trực tiếp và có trang Cục QLCL công bố bộ đề tham khảo; chưa so sánh toàn bộ byte với tệp tải từ trang công bố. N08 được đọc trong bối cảnh bộ minh họa định dạng, không gán tỉ trọng của ma trận này cho kỳ thi 2027. Gói làm việc bảo toàn các trang bản sao đã có, không phải chứng nhận mọi bản sao đã được xác thực điện tử. Nếu dùng nguyên một câu, đối chiếu ảnh và vị trí cụ thể trước khi đưa vào bộ chấm.

Các kết quả có ích đã được tích hợp vào công việc ôn:

| Bằng chứng và vấn đề | Cách áp dụng trong kế hoạch |
| --- | --- |
| N04 I.3: đồng loạt nhân đôi tần số | R2 có nhiệm vụ giải thích ý nghĩa thước đo và tính bất biến, bên cạnh tính bằng công thức |
| N04 II.2: tốc độ và quãng đường | R7 kết nối R1/R8; kiểm đơn vị, mốc thời gian, cận và ý nghĩa tích lũy |
| N04 III.2: đường đi và chi phí | R8 tập xét đủ phương án theo dữ kiện; đối chiếu ranh giới phần chung/chuyên đề, không tự yêu cầu toàn bộ lý thuyết đồ thị |
| N08: bảng năng lực và mức tư duy | 5.1 và D.12 tách ba trục; phân tích từng ý đúng/sai, không sao chép tỉ lệ bảng minh họa |
| N01 có bốn mã | 5.1, 9.8 và 12.5 thêm họ câu/lịch sử đã gặp để bảo vệ tính độc lập của đánh giá |
| N06 khác quy cách mã đề | 9.8 và 12.5 thêm kiểm phiếu, thời gian thao tác và lỗi chuyển kết quả |
| N02/N03 ghép lời giải AI | 3.6, 6.2 và 9.9 dùng phần đề, tự giải và kiểm chứng; không dựa vào nhãn của cả tệp |

N03 còn gợi ý các nhiệm vụ phối hợp: vùng phủ và mặt/khối cầu (R3/R8), vận tải có điều kiện nguyên (R8), thể tích từ miền elip/đường tròn (R7/R3), đếm có ràng buộc (R4/R8), tối ưu lợi nhuận sau thuế (R1/R8). Đây chỉ là chỉ mục ứng viên để tìm đúng nguồn phát hành; chưa chọn chúng làm câu chuẩn hay đặt thêm yêu cầu bắt buộc trong D0. Phần giải quân cờ trong bản AI cần thêm lập luận loại phân bố hàng khác, minh họa vì sao phải kiểm từng bước thay vì tin nhãn lời giải. Không kết luận đáp số sai khi chưa giải độc lập toàn bài.

Nguồn chính thức phục vụ các kết luận:

- [Cục QLCL công bố bộ đề tham khảo từ năm 2025, ngày 18/10/2024](https://vqa.moet.gov.vn/vi/news/tin-tuc-su-kien/de-thi-tham-khao-ky-thi-tot-nghiep-thpt-tu-nam-2025-159.html): căn cứ bối cảnh bộ đề tham khảo.
- [Cục QLCL công bố định dạng, ngày 29/12/2023](https://vqa.moet.gov.vn/vi/news/thong-bao/cau-truc-dinh-dang-de-thi-tot-nghiep-thpt-tu-nam-2025-74.html): ba định dạng và bối cảnh minh họa lớp 10–11 lúc công bố.
- [Cục QLCL công bố Công văn 1239 hướng dẫn thi năm 2025](https://vqa.moet.gov.vn/vi/news/tin-tuc-su-kien/huong-dan-to-chuc-ky-thi-tot-nghiep-trung-hoc-pho-thong-nam-2025-178.html); [PDF văn bản được trường lưu](https://bentre.hgs.edu.vn/uploads/Vanban/20242025/20250319_HDTHi_Final.signed.pdf): đã xem Phụ lục VI, trang PDF 14–16; mặt phiếu trang 15 có tám ô số báo danh/bốn ô mã đề.
- [Quyết định 4068 được Chính phủ đăng lại](https://xaydungchinhsach.chinhphu.vn/toan-van-quyet-dinh-4068-qd-ttg-phuong-an-thi-tot-nghiep-thpt-tu-2025-11923112916510334.htm): phương án ban đầu; dùng cùng hướng dẫn mới hơn tại 3.4. Không tuyên bố văn bản hết hiệu lực chỉ vì thông tin tổ chức đã cập nhật.

### E.7. Gói nguồn khởi động v0.5

Tệp `ZO_Math_Nguon_khoi_dong_v0_5.zip` có bảy PDF, tổng cộng 36 trang, kèm `README.md` và `manifest.json`. Giải nén trước khi chọn PDF đưa vào Notebook. Các PDF giữ nguyên trang nguồn, không thêm lời giải, không OCR lại. Bản gốc vẫn dùng để truy nguyên. Bản trích Công văn 1239 phục vụ đọc phụ lục, không thay bản toàn văn có chữ ký điện tử.

| Tệp trong gói | Trang nguồn gốc | Nơi dùng |
| --- | --- | --- |
| 01_De_2025_ma_0101-0104.pdf | N01 tr.1–16; bốn mã, mỗi mã bốn trang | Dữ liệu đề và họ câu; chọn phần liên quan trong sổ nghiên cứu |
| 02_De_2026_ma_0101.pdf | N02 tr.1–4 | Đối chiếu nhiệm vụ thực tế và tự giải |
| 03_De_tham_khao_tu_2025.pdf | N04 tr.1–4 | Nghiên cứu cấu trúc và bài phối hợp |
| 04_De_minh_hoa_lop_10.pdf | N08 tr.1–4 | Chọn chất liệu nền cho D0 |
| 05_Ma_tran_minh_hoa_lop_10.pdf | N08 tr.6 | Thiết kế ma trận; không phải tỉ lệ bắt buộc toàn THPT |
| 06_Quyet_dinh_4068_2023.pdf | N07 tr.1–4, toàn tệp | Hồ sơ chính sách lịch sử ở dự án điều phối |
| 07_Phu_luc_VI_CV1239_2025.pdf | Công văn 1239 tr.14–16 | Quy cách và mẫu phiếu để luyện thao tác hiện tại |

**Cách dùng hiện tại:** giữ D0 v1.0 đã hoàn tất; khi bảo trì có căn cứ, CT/SGK và tệp 04 có thể cung cấp chất liệu nền; dùng 01–03 khi cần nhiệm vụ của các mạch khác, tự giải theo 9.9. Tệp 05 giúp rà thiết kế ma trận; 06–07 thuộc hồ sơ cấu trúc/tổ chức, không cần chọn khi Notebook đang nghiên cứu đạo hàm. Người chủ trì không cần tìm thêm sách để bắt đầu.

**Phép thử nạp:** xác định tên/mã đề; trích đúng công thức có điều kiện; đọc một hình/bảng; chép đầy đủ giả thiết chung của một câu đúng/sai và dẫn đúng trang. Chỉ ghi T4 sau phép thử thực tế. Kết quả giải và bản kết tinh ZO Math được kiểm định riêng trước khi dùng tạo học liệu. Gói nguồn v0.5 tự nó không chứa D0/học liệu thành phẩm. Bộ D0 v1.0 đã hoàn tất được lưu riêng như 11.6; không suy thiếu D0 trong zip là dự án chưa soạn D0.

### E.8. Nguồn và mức kiểm tra bổ sung cho 0.6 — 11/09/2026

| Nguồn | Đã kiểm và cách sử dụng |
| --- | --- |
| Tệp Kế hoạch 0.5 do người chủ trì cung cấp | Đọc toàn văn 2.123 dòng, audit 0–16/A–G trước nghiên cứu bổ sung; làm nền kế thừa, không ghi đè |
| CT và sáu SGK tại E.1 | Rà CT theo H; xem sáu mục lục, hình CT tr.81/106/107. Các lần đọc chi tiết SGK ghi ở 0.5 là bằng chứng kế thừa, không nhận là đọc lại toàn bộ lần này |
| Bốn PDF D0 v1.0 tại 11.6 | Đọc hướng dẫn và kiểm cấu trúc liên quan kiến trúc; xác nhận trạng thái hoàn tất theo người chủ trì; không tuyên bố giải lại đủ 48 nhiệm vụ |
| Các tệp chính thức đã có trong Nguồn | Giữ mã, nguồn gốc và mức kiểm ở E.6–E.7; kiểm kê lại tệp. Bản `01_De_2025_ma_0101-0104.pdf` hiện có 16 trang; tham chiếu trang 17 của bản lưu cũ không áp dụng cho tệp này |
| [Cục QLCL, công bố cấu trúc từ 2025](https://vqa.moet.gov.vn/vi/news/thong-bao/cau-truc-dinh-dang-de-thi-tot-nghiep-thpt-tu-nam-2025-74.html) | Kiểm lại ngày và phạm vi công bố, ba dạng và 90 phút; không chốt riêng 2027 |
| [Bản quy chế hợp nhất 2026](https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/4/02-vbhn-bgddt-kem.pdf) | Kiểm Điều 4–5 tại tr.2: phạm vi/yêu cầu; ngày thi theo hướng dẫn hằng năm |
| [Cục QLCL, nhiệm vụ quản lý chất lượng 2026–2027](https://vqa.moet.gov.vn/vi/news/tin-tuc-su-kien/bo-gddt-huong-dan-thuc-hien-nhiem-vu-quan-ly-chat-luong-nam-hoc-2026-2027-294.html) | Đọc thông tin công bố 20/08/2026 về Công văn 5548/BGDĐT-QLCL: chuẩn bị thí điểm từ 2027 không đồng nghĩa áp dụng đại trà |
| NC01–NC10 và nguồn EEF bổ trợ | Danh mục, DOI/URL, phần đã đọc, kết quả và giới hạn tại 3.13; chỉ dùng làm căn cứ B |
| SGV | Chưa truy xuất được đúng tệp trong lượt tìm; không suy ý đồ tác giả từ tên sách |

Nguồn web ghi ngày truy cập để có thể rà lại. Với tệp dự án, trích bằng tên tệp/mã nguồn và trang; không biến đường dẫn tạm thành định danh lâu dài. Mã H-YC/C/NC là mã nội bộ mới trong 0.6, không trùng với mã đề hay mã yêu cầu của Bộ.

## Phụ lục F. Audit và nhật ký 0.5 → 0.6

### F.1. Bản đồ audit toàn Kế hoạch 0.5

Đã đọc toàn văn bản nền trước khi bổ sung nghiên cứu và soạn 0.6. Nhãn GIỮ NGUYÊN nói về nội dung/quy trình còn đúng, không cấm cập nhật tên, tham chiếu hay trạng thái lỗi thời. Một khu vực có thể vừa giữ nền vừa bổ sung; bảng ghi xử lý chính, sổ F.2–F.3 nêu tác động cụ thể.

| Phần của 0.5 | Phân loại chính | Kết quả và cách xử lý trong 0.6 |
| --- | --- | --- |
| 0 | **CẦN SỬA** | Điểm vào R1-G01; 0.6 thay 0.5; mục lục mới |
| 1 | **GIỮ NGUYÊN** | Mục tiêu, suy lí/kiến tạo ý nghĩa, kho lâu dài, lớp nội dung quá trình |
| 2 | **CẦN BỔ SUNG** | Bốn lớp và quy tắc ánh xạ nhiều-nhiều |
| 3 | **CẦN BỔ SUNG** | A/B/C; nghiên cứu NC; cấu hình kỳ thi có phiên bản |
| 4 | **CẦN SỬA** | Tên chính thức, R7, sổ rà CT và phạm vi ngoài mẫu D0 |
| 5 | **CẦN SỬA** | Ngưỡng tiến tiếp có điều kiện, trạng thái theo mục tiêu, không chặn toàn lộ trình |
| 6–7 | **GIỮ NGUYÊN** | Quy trình nghiên cứu, kiểm nguồn, kết tinh; cập nhật trạng thái và căn cứ |
| 8 | **CẦN BỔ SUNG** | Hành động nhớ lại, xen kẽ, phản hồi cụ thể trong lõi học liệu |
| 9–10 | **GIỮ NGUYÊN** | Kiểm định, sửa lỗi, xuất bản, phiên bản; thêm liên kết quyết định |
| 11 | **CẦN SỬA** | D0 hoàn tất v1.0; đặc tả bảo trì, kế thừa 24+24 câu; R1-G01 kế tiếp |
| 12 | **CẦN BỔ SUNG** | Lập lịch lùi, nhập học nhiều thời điểm, giữ phủ, ngân sách khả thi |
| 13–14 | **GIỮ NGUYÊN** | QMD, repo, nhiều kênh, tự động hóa sau bộ mẫu |
| 15 | **CẦN SỬA** | Trạng thái thật, một việc kế tiếp, tham số thử nghiệm |
| 16 | **CẦN BỔ SUNG** | Phiên bản cấu hình kỳ thi và tác động cập nhật |
| A | **GIỮ NGUYÊN** | 24 chương/79 bài; lịch chỉ tham chiếu |
| B | **CẦN SỬA** | Giữ 42 mã và tiên quyết; đổi tên chính/ghi đủ mục tiêu bị ẩn |
| C | **GIỮ NGUYÊN** | 9 chuyên đề riêng; không đánh đồng phần chung |
| D | **CẦN SỬA** | Prompt cũ 0.4, lệnh biên soạn D0; thêm mẫu lịch/cấu hình/quyết định |
| E | **GIỮ NGUYÊN** | Nguồn đã có và lịch sử; phân biệt kiểm lại 2026-09-11 |
| F | **CẦN SỬA** | Nhật ký 0.5→0.6, bảo toàn công sức, audit toàn tài liệu |
| G | **GIỮ NGUYÊN** | Đề cương B04–B06 đầy đủ, chỉ chuẩn tên |
| CT từng yêu cầu | **CẦN KIỂM CHỨNG** | Rà theo trang/đề mục; không đồng nhất có vị trí với đủ học liệu |
| D0 hiệu quả | **CẦN KIỂM CHỨNG** | Không có dữ liệu học sinh; không tái chứng nhận toàn bộ toán |
| SGV | **CẦN KIỂM CHỨNG** | Chưa truy xuất được đúng tệp trong lượt tìm; không gán ý đồ SGV |
| 2027 | **CẦN KIỂM CHỨNG** | Ngày thi/định dạng riêng chưa chốt từ nguồn đã kiểm |
| Nghiên cứu | **CẦN BỔ SUNG** | Luyện nhớ lại, giãn cách, xen kẽ, đánh giá, phản hồi, tiến tiếp, gia nhập muộn |

### F.2. Sổ thay đổi cấu trúc lớn

Các quyết định dưới đây là **C của ZO Math**. Cột căn cứ phân biệt A, B và lý do vận hành; không lấy việc kế hoạch lựa chọn một cách làm làm bằng chứng nghiên cứu cho chính nó.

| Mã | Vấn đề của 0.5 | Bằng chứng hoặc lý do | Thay đổi trong 0.6 |
| --- | --- | --- | --- |
| C-01 | R dễ bị hiểu là toàn bộ nội dung, lịch dễ bị hiểu là thứ tự bắt buộc | A: CT có phạm vi/yêu cầu riêng; C: một B dùng nhiều R, một nhiệm vụ có nhiều vai trò | Tách bốn lớp 2.5, giữ đường truy nguyên CT/CD/B/R/gói/câu/lượt học/cấu hình |
| C-02 | Độ phủ theo cụm chưa là đối chiếu từng yêu cầu; tên chính lẫn ý tưởng diễn giải | A: CT tr.79–114 và mục lục SGK; các mục tiêu còn ẩn ở H | Chuẩn tên R6/R7 và B; thêm sổ H; giữ mã và nội dung diễn giải còn đúng |
| C-03 | Lịch và đánh giá chứa quy cách 2025–2026 ở nhiều nơi | A: công bố có phạm vi/thời điểm, chưa đủ xác nhận riêng 2027; C: cần giới hạn tác động cập nhật | Hồ sơ cấu hình kỳ thi riêng 3.14, quy trình đổi tại 12.14 |
| C-04 | Có tự kiểm tra nhưng chưa có căn cứ và thao tác luyện nhớ lại rõ | B: NC01/NC02/NC10; C: cần quan sát trước trợ giúp | Tự tái hiện trước lời giải, kiểm bằng bài mới; không dùng đọc trôi chảy làm chứng cứ |
| C-05 | Lịch gọi lại có số cụ thể nhưng nguồn khoa học chưa được truy nguyên | B: NC03/NC04; C: lịch phải vừa thời gian thực | Giữ giãn cách, ghi lịch 2–3 ngày/7 ngày/3–4 tuần là tham số C và điều chỉnh theo kết quả |
| C-06 | “Trộn/tổng hợp” chưa tách việc chọn công cụ với đổi dạng trả lời | B: NC05/NC06, NC10 phân biệt xen ví dụ–tự giải; C: cần nền tối thiểu | Xen các nhiệm vụ cần phân biệt phương pháp; có giải thích lựa chọn, hỗ trợ khi chưa học; không trộn ngẫu nhiên mọi mạch |
| C-07 | Phản hồi/đánh giá có vòng sửa tốt nhưng chưa rõ đâu là nghiên cứu, đâu là thiết kế | A: CT tr.116–117; B: NC07/NC08, kết quả không bảo đảm tăng điểm Toán | Thu bằng chứng → đổi hoạt động → học sinh thực hiện → bài mới; chỉ điểm/lời khen không thay phản hồi hành động |
| C-08 | 80% có nguy cơ thành cửa bắt buộc cho cả mạch, gây mắc kẹt | B: NC09 và giới hạn thời gian/mastery; C: ngưỡng hiện tại chưa thử ở ZO Math | Tách vào nhiệm vụ, giảm luyện riêng, phối hợp; tạm chặn phần phụ thuộc, đi tiếp nhánh độc lập; giới hạn giờ sửa |
| C-09 | 36 tuần chưa có thuật toán xử lý gia nhập muộn | A: ngày thi theo hướng dẫn năm; B: không đủ bằng chứng trực tiếp cho lịch nén cụ thể; C: quỹ giờ và tiên quyết là ràng buộc thật | Lập lịch lùi, D0 + trường + giờ; giảm sâu/vòng/đề trước vùng kiến thức; ghi bất khả thi khi còn thiếu |
| C-10 | Trạng thái còn yêu cầu soạn D0; thiếu sổ căn cứ và tác động đổi phiên bản | C: người chủ trì xác nhận D0 hoàn tất; kiểm bốn PDF, phát hiện lỗi chỉ dẫn R3; quy trình 0.5 vẫn hữu ích | D0 v1.0 giữ nguyên và đính chính chỉ dẫn; cập nhật toàn bộ điểm vào R1-G01, biểu mẫu A/B/C và metadata |

### F.3. Hệ quả đối với các thành phần dự án

| Mã | D0 v1.0 | R1–R8 | B01–B42 | Bảng 36 tuần/lịch cá nhân | Quy trình sản xuất |
| --- | --- | --- | --- | --- | --- |
| C-01 | Công cụ định vị lớp 3 | Mạch kết nối, không là bản đồ CT | Giữ mã, nối yêu cầu/tiên quyết | Trở thành một cấu hình lịch | Mỗi nhiệm vụ có đường truy nguyên |
| C-02 | Ánh xạ tên cũ; không thêm câu để kiểm kê toàn CT | R6/R7 chuẩn tên; R8 giữ xuyên suốt | Làm rõ mục tiêu ẩn, tên chính và ranh giới | Giữ vị trí, không bỏ mạch vì tên đổi | Ma trận gói phải tách yêu cầu H liên quan |
| C-03 | Không bị ép thành đề 90 phút | Giữ cấu trúc khi chỉ đổi quy cách | Giữ nội dung toán; rà lại nếu phạm vi thực đổi | Đổi mốc thi, thời lượng, số đề | Câu toán và phần định dạng tách hồ sơ, kiểm lại khi chuyển |
| C-04 | Kết quả trước hỗ trợ có giá trị định vị | Hoạt động nhớ lại nằm trong từng R | Chọn mục tiêu cụ thể, không chỉ công thức | Giữ các lượt ngắn từ đầu | Có bài làm trước lời giải, câu mới và lịch sử tiếp xúc |
| C-05 | Không coi D0 + thử ngay là duy trì dài hạn | R cũ quay lại khi đang học R mới | Hẹn theo mục tiêu B | Giữ ngân sách gọi lại, điều chỉnh khoảng trễ | Gói có ngày dự kiến và ngày thật, không chỉ nhãn “ôn rồi” |
| C-06 | Mẫu đầu vào không chứng minh đủ chọn công cụ ở mọi tình huống | Cầu nối giữa R, không trộn theo số mạch | Gắn các mục tiêu cần phân biệt | Xen từ sớm khi đủ nền; C1–C3 tăng phối hợp | Phiếu không báo sẵn phương pháp, kiểm lập luận chọn cách |
| C-07 | Dùng phân tích để ra hành động | Hai ưu tiên sửa không thay toàn độ phủ R | Ghi lỗi ở mục tiêu | Dành giờ chữa và thử lại | Lời giải, phản hồi và câu sau chữa phải khớp |
| C-08 | 24 mẫu không là chứng nhận mastery | Không chặn mọi R vì một nhánh yếu | Tiên quyết kiểm tại mục tiêu nhỏ | Giới hạn giờ sửa, chuyển nhánh độc lập | Ghi tử/mẫu, điều kiện thiết yếu, bằng chứng mới và khoảng trễ |
| C-09 | Dùng cho mỗi người nhập, không soạn lại ngân hàng | Đủ chỗ cho các mạch cần thiết theo người học | Theo dõi học/chưa rõ/chưa học, không xóa hàng | 36 tuần giữ; ví dụ 29/20 tuần phải qua kiểm giờ | Ưu tiên học liệu cho mục tiêu sắp dùng, tránh hứa sẵn toàn khóa |
| C-10 | Giữ thành phẩm; đính chính B.8 là Oxyz | R1-G01 là gói nội dung tiếp theo | Giữ chỉ mục/đề cương và lịch sử | Cập nhật lịch bằng bài thật/công bố mới | Mẫu D.11/D.14/D.18–D.22 và bàn giao thống nhất |

### F.4. Changelog 0.5 → 0.6 và kiểm tra bảo toàn

- Tách kiến trúc thành bốn lớp; giữ các mã CT/CD/B/R/G và toàn bộ chức năng đúng của kho, gói và nền N.
- Rà phạm vi theo CT, ghi rõ mục tiêu còn ẩn; chuẩn tên R7 thành “Nguyên hàm, tích phân và ứng dụng”, R6 theo tên mạch CT; giữ “tích lũy” trong diễn giải.
- Bổ sung hồ sơ nghiên cứu có nguồn, mức đọc và giới hạn; tách A/B/C, không gán các tham số vận hành cho nghiên cứu.
- Giữ bảng 36 tuần × 6 giờ như lịch tham chiếu đầy đủ; thêm lập lịch theo mốc thi, D0, trường, giờ thực và cơ chế gia nhập muộn.
- Tách cấu hình kỳ thi; thêm quy trình cập nhật ngày, định dạng, phương tiện hoặc phạm vi.
- Giữ D0 v1.0 hoàn tất, ghi đính chính chỉ dẫn R3; chuyển điểm tiếp tục sang chuẩn bị nguồn/ma trận R1-G01.

Kiểm bảo toàn: các mục 0–16, A–G vẫn có nơi sử dụng; bổ sung H. Giữ đầy đủ chỉ mục 24 chương/79 bài và hoạt động, chín chuyên đề, danh mục B01–B42 cùng tiên quyết, bảng R–B, bảng 36 tuần, đề cương G, quy trình Notebook/Studio/QA/đóng gói/công bố/tự động hóa. Những câu bị thay là tên gọi, trạng thái lỗi thời hoặc quy tắc cần làm rõ; không tái dựng dự án từ đầu.

Kiểm lần này là audit nguồn/kiến trúc/văn bản và tính nhất quán, không phải kiểm định thực nghiệm chương trình, chứng nhận 100% từng yêu cầu hay duyệt của con người. Nguồn thiếu được ghi ở H.4. Tệp 0.5 và các PDF D0 không bị ghi đè.

### F.5. Dấu vết các lần tích hợp trước — chỉ để truy nguyên

0.3 phục hồi chi tiết từ 0.1–0.2; bản Lộ trình toàn cảnh 1.0 bổ sung tổ chức ôn; 0.4 tích hợp chúng, giữ đề cương nền B04–B06 và cập nhật R/D0/lịch. 0.5 giữ các phần ấy, thêm quy tắc nguồn chính thức/tự giải, họ câu và lịch sử gặp câu, kiểm phiếu, đánh giá tám tài liệu và gói nguồn khởi động ở E.6–E.7. Các chỉ dẫn lịch sử “bắt đầu B04”, rồi “biên soạn D0 trước” đã được thay bằng trạng thái hiện hành 15.5; không dùng lịch sử làm lệnh khởi động lại.

## Phụ lục G. Đề cương nền B04–B06 để dùng theo nhu cầu

Các đề cương đã được xây dựng được giữ đầy đủ để tra cứu, nghiên cứu và tạo phần bổ sung N. Chúng không ấn định thứ tự khởi động hoặc buộc người học làm hết ba bộ. D0 và nhiệm vụ R1-G01 xác định phần nào cần dùng. Các phiên và số câu dưới đây là khung riêng của từng cụm, không phải lịch ôn hoặc định mức sản xuất toàn chương trình.

### G.1. B04 — Hàm số và đồ thị: hiểu qua công thức, bảng và hình

**Tên:** Hiểu hàm số qua công thức, bảng và đồ thị.

**Nguồn chính:** CT tr.80; S10.2, Bài 15, tr.in 4–10. Các trang này cần được đối chiếu chi tiết trước phiên học; mục lục và một trang định nghĩa đã được xem trong lần kiểm tra sách.

**Câu hỏi trung tâm:** khi nào một quy tắc hoặc một biểu diễn mô tả hàm số, và làm sao biết công thức, bảng, đồ thị đang nói về cùng một đối tượng?

| Mã mục tiêu nội bộ | Người học cần làm được | Nhiệm vụ kiểm tra đề xuất |
| --- | --- | --- |
| B04-M1 | Nhận ra điều kiện mỗi đầu vào có đúng một đầu ra | Xét bảng và quan hệ có đầu vào lặp với hai đầu ra khác nhau; giải thích |
| B04-M2 | Phân biệt tập xác định và tập giá trị | Tìm hai tập từ một bảng và một biểu thức có điều kiện; không tráo vai trò |
| B04-M3 | Đọc giá trị, điểm trên đồ thị và liên hệ biểu diễn | Ghép công thức–bảng–đồ thị; nhận ra một hình không khớp |
| B04-M4 | Mô tả đồng biến, nghịch biến và đặc trưng đồ thị | Đọc khoảng tăng/giảm và giải thích quan hệ giữa thứ tự đầu vào–đầu ra |
| B04-M5 | Dùng hàm số mô tả bối cảnh và giữ miền hợp lệ | Lập một quy tắc tính phí theo khoảng từ dữ liệu giả định, kiểm tra đầu mút và đơn vị |

Đây là diễn giải thiết kế từ CT tr.80, không phải trích nguyên văn và không mang mã chính thức của Bộ.

**Kiến thức cần trước:** số thực, khoảng, thay số vào biểu thức và tọa độ điểm. Chuẩn bị một phiếu ôn nhanh đủ dùng; B01–B02 chưa thành phẩm không được làm người học mất chỗ bắt đầu.

**Những điểm nên đào sâu trong nghiên cứu:** biểu thức và hàm số khác nhau ở đâu; vì sao hai đầu vào có thể cùng đầu ra; rút gọn biểu thức có thể làm quên miền xác định thế nào; bảng hữu hạn có xác định được toàn bộ hàm không; cần những điều kiện nào khi so sánh hai hàm.

**Giới hạn B04:** chưa dùng đạo hàm để giải thích đơn điệu; chưa khảo sát mọi hàm đã có trong dự án 100+ Hàm số. Phần liên hệ sâu được lưu để quay lại ở B16–B21.

**Ví dụ để lựa chọn khi soạn:** hàm hằng, hàm bậc nhất, giá trị tuyệt đối và hàm bậc hai ở mức vừa đủ để hiểu khái niệm, bảng và đồ thị. Dùng lại bài ZO Math chỉ sau khi kiểm tra phần phù hợp, không đưa toàn bộ khảo sát chuyên sâu vào B04.

**Điểm kiểm định riêng:** tập xác định khác tập giá trị; điểm trống và điểm đặc trên hình có ý nghĩa khác nhau; trục và đơn vị phải rõ; một đầu vào không được có hai đầu ra; rút gọn biểu thức không tự thay miền xác định gốc. Khi hỏi hai biểu diễn có mô tả cùng hàm hay không, phải có đủ thông tin về miền xét, không chỉ so khớp vài giá trị trong bảng.

### G.2. Chuỗi phiên nghiên cứu B04 khi cần bổ sung nền

| Phiên | Trọng tâm | Sản phẩm học của người chủ trì |
| --- | --- | --- |
| 1 | Trích xuất Bài 15; nghiên cứu khái niệm và điều kiện duy nhất của đầu ra | Diễn giải định nghĩa bằng lời, ví dụ và phản ví dụ đã kiểm tra |
| 2 | Tập xác định, tập giá trị và chuyển giữa biểu diễn | Bài làm, hình/bảng đối chiếu và ghi nhận lỗi thường gặp |
| 3 | Đồng biến/nghịch biến; mô hình thực tế | Lập luận và lời giải cho nhiệm vụ đại diện |
| 4 | Tổng hợp B04, thử tự giải lại và chỉ ra chỗ còn mở | Bản nội dung B04 có phiên bản, sẵn sàng cho sản xuất |

Đây là cách chia khởi điểm; một phiên có thể tách làm hai nếu cần. Mỗi phiên bắt đầu bằng yêu cầu trích xuất phạm vi cụ thể từ nguồn, không phải yêu cầu Studio làm ngay bộ thành phẩm.

### G.3. Quy mô bài luyện khởi điểm của B04

Đề xuất 4 câu đầu vào, 12 nhiệm vụ tự luyện, 5 nhiệm vụ cuối bài tương ứng M1–M5; được chỉnh sau khi soạn nếu có mục tiêu chưa được kiểm tra hoặc câu hỏi trùng chức năng. Đây chỉ là thiết kế B04, không áp cho mọi cụm.

| Nhóm luyện | Số nhiệm vụ dự kiến | Trọng tâm |
| --- | ---: | --- |
| Khái niệm, miền xác định, tập giá trị | 4 | Giải thích và nhận diện trường hợp dễ nhầm |
| Công thức, bảng, đồ thị | 3 | Chuyển biểu diễn và kiểm tra sự khớp |
| Đồng biến, nghịch biến | 2 | Đọc và diễn đạt đúng trên từng khoảng |
| Mô hình có bối cảnh | 2 | Miền đầu vào, đầu mút, đơn vị |
| Phản biện lời giải | 1 | Phát hiện lỗi làm đổi nghĩa hàm số |

Bài tự kiểm tra Studio dùng các mục tiêu này, nhưng phải kiểm tra lại câu và cách chấm. Không mặc định câu do Studio tạo tương đương ngay với câu thi chính thức.

### G.4. Đề cương B05 — Hàm số bậc hai

**Câu hỏi trung tâm:** vì sao những cách viết khác nhau của một tam thức lại giúp nhìn thấy các đặc điểm khác nhau của cùng parabol?

**Nguồn:** CT tr.80; S10.2 Bài 16. Khi mở phiên học phải xác nhận dải trang đầy đủ và nội dung thực dùng. **Cần trước:** thay số, tọa độ, biến đổi đại số, khái niệm hàm số và đọc đồ thị từ B04. Chuẩn bị ôn nhanh nếu B02 chưa có thành phẩm.

| Mục tiêu thiết kế | Mạch nghiên cứu và bằng chứng học sinh |
| --- | --- |
| Nhận diện hàm bậc hai | Nêu điều kiện hệ số bậc hai khác không; phân biệt với hàm bậc nhất |
| Liên hệ các dạng biểu thức | Từ dạng tổng quát đến dạng đỉnh; dùng dạng nhân tử khi có nghiệm thực; tự kiểm tra phép biến đổi |
| Đọc và giải thích parabol | Xác định đỉnh, trục, chiều mở, khoảng biến thiên; liên hệ với dấu và giá trị hệ số |
| Kết nối dữ kiện và đồ thị | Tìm giao điểm, lập bảng có mục đích, dựng đồ thị hoặc tìm biểu thức từ dữ kiện phù hợp |
| Vận dụng có điều kiện | Mô hình một tình huống đơn giản, xác định miền hợp lệ và diễn giải kết quả |

Đi từ đồ thị $y=x^2$ và các biến đổi đơn giản đến dạng tổng quát, rồi so sánh các cách viết để giải thích cùng một đồ thị. Chứng minh biến đổi đại số được giữ đủ để người học tự kiểm tra. Chưa dùng đạo hàm; bài tham số vượt mục tiêu chung được ghi nhãn riêng.

**Chuỗi phiên học dự kiến:** trích xuất và nghiên cứu các dạng biểu thức; đọc/dựng đồ thị; giải tình huống và phản biện lỗi; kết tinh. Mỗi phiên dùng quy trình ở mục 7 và có thể tách thêm theo thực tế.

**Khung 12 bài luyện để thử cho riêng B05:** 4 bài nhận diện/đọc đặc điểm; 3 bài chuyển dạng và vẽ; 2 bài tìm biểu thức từ dữ kiện; 2 bài vận dụng; 1 bài phản biện lời giải. Phần đầu vào kiểm tra các kiến thức cần trước; phần cuối dùng nhiệm vụ mới cho các mục tiêu, trong đó có một parabol khác các ví dụ đã làm. Số câu được điều chỉnh nếu còn mục tiêu thiếu bằng chứng.

**Điểm kiểm định riêng:** điều kiện $a\ne0$; dấu trong hoành độ đỉnh; trục đối xứng khác điểm đỉnh; trường hợp không có giao điểm thực với trục hoành; tập giá trị trên miền xét; miền thời gian/độ dài trong bài thực tế. Sản phẩm bổ trợ ưu tiên một bản trình bày liên hệ các dạng biểu thức với parabol nếu nó giúp quan sát; chưa đặt sản phẩm này thành điều kiện bắt buộc.

### G.5. Đề cương B06 — Dấu của tam thức bậc hai và phương trình quy về bậc hai

**Câu hỏi trung tâm:** từ vị trí đồ thị so với trục hoành, làm sao kết luận khoảng nghiệm và giữ đủ điều kiện của bài toán?

**Nguồn:** CT tr.80–81; S10.2 Bài 17–18. Phải mở đúng trang nguồn trước phiên; không suy phạm vi từ tên “phương trình quy về bậc hai” rồi đưa mọi dạng phương trình vào phần chính. **Cần trước:** B05, phép biến đổi có điều kiện, khoảng và tập nghiệm.

| Mục tiêu thiết kế | Mạch nghiên cứu và bằng chứng học sinh |
| --- | --- |
| Hiểu dấu tam thức | Liên hệ vị trí parabol với trục hoành, dấu hệ số và các trường hợp số nghiệm |
| Lập/đọc bảng dấu | Xét có hai nghiệm, nghiệm kép hoặc không có nghiệm thực; xử lý điểm bằng không |
| Giải bất phương trình | Chọn các khoảng đúng với dấu yêu cầu; giữ hoặc loại đầu mút phù hợp |
| Giải phương trình quy về bậc hai trong phạm vi nguồn | Viết điều kiện, chọn phép biến đổi, tìm và kiểm tra nghiệm |
| Phát hiện lời giải sai | Giải thích lỗi về dấu, khoảng nghiệm hoặc nghiệm ngoại lai; sửa và thử lại |

Đi từ một parabol đã hiểu ở B05 sang dấu của tam thức, rồi bất phương trình và phương trình chứa căn thuộc phạm vi đã đối chiếu. Mỗi phép biến đổi cần nói rõ điều kiện; thế lại nghiệm khi cần. Nội dung phân thức hoặc giá trị tuyệt đối dùng để bù nền hay đào sâu được ghi đúng nhãn, không tự trở thành phần chung của B06.

**Chuỗi phiên dự kiến:** trích xuất và giải thích dấu; giải bất phương trình; nghiên cứu phương trình và nghiệm ngoại lai; tổng hợp cùng bài sửa lỗi. Giữ một lỗi thật có ích về nghiệm ngoại lai làm chất liệu cho video quá trình nếu xuất hiện trong lúc học.

**Khung 12 bài luyện để thử cho riêng B06:** 4 bài dấu và khoảng nghiệm; 3 bài bất phương trình; 2 bài phương trình cần kiểm tra điều kiện; 2 bài đọc đồ thị để kết luận; 1 bài sửa lỗi. Mỗi câu có mục tiêu riêng để tránh nhóm dấu và nhóm đồ thị chỉ lặp chức năng. Phần cuối có câu mới kiểm tra lập luận về dấu, đầu mút và điều kiện nghiệm; chỉnh số câu theo ma trận mục tiêu.

**Điểm kiểm định riêng:** dấu khi không có nghiệm thực; nghiệm kép không làm tam thức đổi dấu; dấu lớn hơn khác lớn hơn hoặc bằng; giao điều kiện với tập nghiệm; bình phương có thể sinh nghiệm ngoại lai. Sản phẩm hỗ trợ chỉ chọn sau khi thấy học sinh cần quan sát bảng dấu, đồ thị hay tự sửa lỗi ở điểm nào.

### G.6. Cách đưa nền vào gói ôn

Khi lỗi của học sinh hoặc câu hỏi nghiên cứu cho thấy thiếu khái niệm hàm, chọn mục tiêu tương ứng ở G.1–G.3. Khi cần parabol hoặc dấu, dùng G.4–G.5. Tạo phiếu bổ sung ngắn trước; chỉ phát triển thành bộ nền riêng khi phạm vi thực tế cần. Giữ mã B và gắn nơi sử dụng R/N trong hồ sơ.

Nếu B04–B06 đã có thành phẩm, rà các mối nối khái niệm–đồ thị–dấu, tránh lặp giải thích hoặc thiếu chuyển tiếp. Bài của 100+ Hàm số là ứng viên tái sử dụng sau khi kiểm tra bản hiện hành; công việc này không mở nhiệm vụ sửa dự án đó.

---

**Điểm triển khai hiện hành: chuẩn bị bộ nguồn và ma trận mục tiêu cho phiên nghiên cứu đầu tiên của R1-G01 theo 15.5 và D.14. D0 v1.0 đã hoàn tất.**

## Phụ lục H. Sổ rà phạm vi từ Chương trình 2018

### H.1. Phương pháp, kết quả và giới hạn

Đây là **kết quả rà nguồn trước khi viết 0.6**, không chỉ là danh sách hẹn làm sau. Đã đọc tuần tự phần chung lớp 10 tr.79–87, lớp 11 tr.89–103, lớp 12 tr.105–111; phân biệt phần chuyên đề chen giữa ở tr.87–89, 104–105 và 112–114; đối chiếu phương pháp/đánh giá tr.114–117. Sáu mục lục SGK được dùng kiểm đường tra chương/bài; không coi mục lục là chứng cứ từng yêu cầu đã được triển khai đủ.

Các hàng H-YC dưới đây là **nhóm yêu cầu để kiểm soát phạm vi do ZO Math phân đoạn**, diễn giải từ nguồn A; không phải mã hoặc số lượng yêu cầu chính thức. Một hàng có thể chứa nhiều động từ/đối tượng cần tách tiếp khi làm học liệu. Cột cuối nêu kết quả audit so với 0.5. Các cụm B đã có chỗ cho phần kiến thức chung ở cấp nhóm, nhưng một số mục tiêu còn ẩn sau tên khái quát; 0.6 ghi rõ lại. Không cần tự ý thêm B43 hoặc đổi mã toàn kho.

**Trạng thái chung của bảng:** đã định vị và đối chiếu ở cấp nhóm yêu cầu; chưa hoàn tất kiểm định từng yêu cầu nguyên tử, từng học liệu và từng câu đánh giá. Không công bố “100% yêu cầu cần đạt đã được đáp ứng”. B02 là nền THCS, B42 là hồ sơ tổng hợp; không đưa hai mã này vào mẫu số yêu cầu chung mới của THPT. Phần chuyên đề và thực hành có điều kiện có sổ riêng ở C/H.2.

Khi sản xuất gói, tách hàng H-YC liên quan thành các mục có thể kiểm tra, giữ động từ và điều kiện của CT, gắn trang/đoạn, mục tiêu gói, nhiệm vụ, lời giải và bằng chứng QA theo 5.1. Một yêu cầu được dùng ở nhiều R chỉ đếm một lần trong sổ phạm vi; mọi nơi sử dụng giữ cùng mã truy nguyên. Chỉ tính tỉ lệ hoàn tất sau khi đã thống nhất cách phân đoạn và rà mẫu số; không lấy 41 B, 79 bài hoặc số câu D0 làm mẫu số thay thế.

| Mã nhóm | Lớp / trang CT | Phạm vi yêu cầu được rà — diễn giải | Vị trí CD / B / R | Kết quả audit và việc tích hợp |
| --- | --- | --- | --- | --- |
| H-YC-001 | 10 / 79 | Mệnh đề: thiết lập/phát biểu phủ định, đảo, tương đương, lượng từ, cần/đủ/cần và đủ; xét đúng/sai trường hợp đơn giản | CD01 / B01 / N, R1–R8 | Làm rõ mệnh đề tương đương trong B01 |
| H-YC-002 | 10 / 79 | Tập hợp: tập con, bằng nhau, rỗng và kí hiệu; phép toán, biểu đồ Ven; bài thực tiễn đếm phần tử hợp | CD01 / B01 / N, R4, R8 | Làm rõ khái niệm cơ bản và ứng dụng, không chỉ khoảng nghiệm |
| H-YC-003 | 10 / 79 | Bất phương trình và hệ bậc nhất hai ẩn: nhận biết, biểu diễn miền nghiệm, vận dụng thực tiễn/cực trị tuyến tính trên miền đa giác | CD01 / B03 / R8 | Giữ; không suy phải học trọn quy hoạch tuyến tính chuyên đề |
| H-YC-004 | 10 / 80 | Hàm số: mô hình bảng/biểu đồ/công thức; định nghĩa, tập xác định/tập giá trị, đồng biến/nghịch biến, đồ thị và ứng dụng | CD02 / B04 / R1, N, R8 | Giữ; bao gồm mô hình cho bởi từng khoảng |
| H-YC-005 | 10 / 80 | Bậc hai: lập bảng giá trị, vẽ đồ thị, đỉnh/trục, giải thích tính chất và vận dụng | CD02 / B05 / R1, N, R8 | Giữ; kiểm cả dựng/vẽ, không chỉ nhận hình |
| H-YC-006 | 10 / 80–81 | Giải thích định lí dấu tam thức từ đồ thị; giải và vận dụng bất phương trình bậc hai | CD02 / B06 / R1, N, R8 | Giữ; không chỉ học thuộc bảng dấu |
| H-YC-007 | 10 / 81 | Giải hai dạng phương trình căn thức quy về bậc hai nêu ở CT | CD02 / B06 / N, R1 | Bổ sung định vị hai dạng; đọc hình công thức gốc trước biên soạn |
| H-YC-008 | 10 / 81 | Quy tắc cộng/nhân và sơ đồ cây trong đếm; tính hoán vị/chỉnh hợp/tổ hợp bằng tay và máy tính | CD14 / B39 / R4, R8 | Giữ; làm rõ thao tác máy tính trong mục tiêu con |
| H-YC-009 | 10 / 81 | Khai triển nhị thức Newton bằng tổ hợp với số mũ thấp n = 4 hoặc 5 | CD14 / B39 / R4 | Giữ đúng phạm vi; nhị thức tổng quát kiểm riêng chuyên đề |
| H-YC-010 | 10 / 82 | Giá trị lượng giác góc 0–180 độ; tính bằng máy; giải thích quan hệ phụ/bù | CD09 / B25 / R3, R6 | Giữ; không nhầm góc lượng giác tổng quát lớp 11 |
| H-YC-011 | 10 / 82 | Giải thích định lí sin/côsin, công thức diện tích; mô tả giải tam giác và vận dụng đo đạc | CD09 / B25 / R3, R8 | Giữ cả giải thích và ứng dụng |
| H-YC-012 | 10 / 82–83 | Vectơ, bằng nhau, vectơ-không; biểu diễn đại lượng, phép toán, tính chất hình, ứng dụng liên môn/thực tiễn | CD09 / B26–B27 / R3, R8 | Giữ; tích vô hướng và điều kiện góc kiểm riêng |
| H-YC-013 | 10 / 83 | Tọa độ vectơ/độ dài từ hai đầu mút; biểu thức tọa độ phép toán; giải tam giác và ứng dụng vị trí | CD09 / B26–B27 / R3 | Giữ; có nhiệm vụ dùng tọa độ giải tam giác |
| H-YC-014 | 10 / 83–84 | Đường thẳng Oxy: tổng quát/tham số; lập theo ba cách; vị trí; thiết lập công thức góc; khoảng cách; liên hệ hàm bậc nhất; ứng dụng | CD10 / B28 / R3, R1, R8 | Giữ; tách mục tiêu nhận biết, thiết lập và tính |
| H-YC-015 | 10 / 84 | Đường tròn: tâm/bán kính, lập qua ba điểm, nhận tâm/bán kính từ phương trình, tiếp tuyến tại tiếp điểm, ứng dụng | CD10 / B28 / R3, R8 | Bổ sung rõ cách lập qua ba điểm |
| H-YC-016 | 10 / 84 | Conic: nhận biết hình học và phương trình chính tắc của elip/hypebol/parabol; vấn đề thực tiễn | CD10 / B29 / R3, R7, R8 | Giữ; không đưa tất cả yếu tố chuyên sâu vào phần chung |
| H-YC-017 | 10 / 85 | Số gần đúng/sai số tuyệt đối/tương đối; độ chính xác, quy tròn và dùng máy tính | CD13 / B36 / R2, N | Giữ; phân biệt số gần đúng với số quy tròn |
| H-YC-018 | 10 / 85 | Phát hiện và lí giải số liệu không chính xác bằng quan hệ toán học giữa dữ liệu bảng/biểu đồ | CD13 / B36 / R2, R8 | Giữ nhiệm vụ đọc dữ liệu; không thay bằng tính trung bình |
| H-YC-019 | 10 / 85 | Tính, giải thích vai trò/ý nghĩa và rút kết luận từ trung bình, trung vị, tứ phân vị, mốt mẫu không ghép nhóm | CD13 / B36 / R2 | Giữ; tách từng thước đo trong ma trận gói |
| H-YC-020 | 10 / 85–86 | Tính, giải thích và rút kết luận từ khoảng biến thiên, khoảng tứ phân vị, phương sai, độ lệch chuẩn; liên hệ môn học/thực tiễn | CD13 / B36 / R2, R8 | Giữ; kiểm đơn vị và bối cảnh so sánh |
| H-YC-021 | 10 / 86 | Phép thử, không gian mẫu, biến cố/đối, xác suất cổ điển, nguyên lí xác suất bé; mô tả phép thử đơn giản | CD14 / B39 / R4 | Giữ; không suy “xác suất bé” là không thể |
| H-YC-022 | 10 / 86 | Tính xác suất đồng khả năng bằng tổ hợp/cây; tính chất xác suất và biến cố đối | CD14 / B39 / R4, R8 | Giữ; mẫu số phải phù hợp mô hình |
| H-YC-023 | 11 / 89–90 | Góc lượng giác, số đo, hệ thức Chasles, đường tròn; giá trị góc thường gặp, hệ thức cơ bản, góc liên quan và dùng máy tính | CD03 / B07 / R6 | Bổ sung rõ Chasles, bảng giá trị và máy tính |
| H-YC-024 | 11 / 90 | Mô tả công thức cộng, nhân đôi, tích thành tổng, tổng thành tích; vận dụng giá trị và biến đổi lượng giác | CD03 / B08 / R6, R8 | Ghi đủ bốn nhóm công thức; không thu hẹp theo đề đã gặp |
| H-YC-025 | 11 / 90 | Chẵn/lẻ/tuần hoàn và đặc trưng đồ thị; định nghĩa bốn hàm sin/cos/tan/cot qua đường tròn | CD03 / B08 / R6, R1 | Giữ đủ cot, miền xác định |
| H-YC-026 | 11 / 90 | Bảng giá trị một chu kì, vẽ đồ thị bốn hàm; giải thích tập xác định/tập giá trị/biến thiên/chu kì từ đồ thị; ứng dụng | CD03 / B08 / R6, R8 | Giữ cả vẽ và giải thích, không chỉ nhớ hình |
| H-YC-027 | 11 / 91 | Công thức nghiệm bốn phương trình cơ bản từ đồ thị; nghiệm gần đúng bằng máy; dạng vận dụng trực tiếp và thực tiễn | CD03 / B09 / R6, R8 | Giữ; không nâng phương trình biến đổi phức tạp thành yêu cầu chung |
| H-YC-028 | 11 / 91 | Dãy hữu hạn/vô hạn; bốn cách cho (liệt kê, tổng quát, truy hồi, mô tả); tăng/giảm/bị chặn đơn giản | CD04 / B10 / R5 | Giữ đủ cách cho và bị chặn |
| H-YC-029 | 11 / 91–92 | Cấp số cộng và cấp số nhân: nhận biết, giải thích số hạng tổng quát, tính tổng n số hạng và vận dụng | CD04 / B10 / R5, R8 | Tách hai nhóm mục tiêu trong gói |
| H-YC-030 | 11 / 92 | Khái niệm giới hạn dãy; giải thích giới hạn cơ bản, phép toán; tổng cấp số nhân lùi vô hạn và ứng dụng | CD04 / B11 / R5, R1 | Giữ điều kiện tổng vô hạn |
| H-YC-031 | 11 / 92–93 | Giới hạn hàm tại điểm/một phía/vô cực, giới hạn vô cực một phía; cơ bản, phép toán và ứng dụng | CD04 / B12 / R1, R5 | Làm rõ đủ loại giới hạn, không chỉ tính thay số |
| H-YC-032 | 11 / 93 | Liên tục tại điểm/khoảng/đoạn; tổng/hiệu/tích/thương; các hàm sơ cấp trên tập xác định | CD04 / B12 / R1 | Giữ điều kiện của thương và miền xét |
| H-YC-033 | 11 / 93–94 | Lũy thừa mũ nguyên/hữu tỉ/thực: nhận biết, giải thích tính chất, tính/rút gọn, máy tính, ứng dụng | CD05 / B13 / R5 | Giữ điều kiện cơ số ở từng loại số mũ |
| H-YC-034 | 11 / 94 | Lôgarit: khái niệm, giải thích tính chất, tính/rút gọn, máy tính, ứng dụng liên môn/thực tiễn | CD05 / B13 / R5 | Giữ điều kiện đối số và cơ số |
| H-YC-035 | 11 / 95 | Hàm mũ/lôgarit: nhận biết/ví dụ thực tế, nhận đồ thị, giải thích tính chất từ đồ thị và vận dụng | CD05 / B14 / R5, R1, R8 | Giữ; mô hình tăng trưởng là ứng dụng |
| H-YC-036 | 11 / 95 | Giải phương trình/bất phương trình mũ/lôgarit đơn giản và ứng dụng | CD05 / B15 / R5, R8 | Giữ; kiểm miền và chiều bất đẳng thức |
| H-YC-037 | 11 / 95–96 | Bài toán dẫn đến đạo hàm, định nghĩa/tính bằng định nghĩa, ý nghĩa hình học/tiếp tuyến; nhận biết e qua mô hình lãi suất | CD06 / B16 / R1, R5 | Bổ sung rõ e và trang 96 ở B16; không chỉ “liên hệ khi đọc nguồn” |
| H-YC-038 | 11 / 96 | Đạo hàm hàm sơ cấp, tổng/hiệu/tích/thương/hợp và ứng dụng | CD06 / B17 / R1, R5–R7, R8 | Giữ; nêu điều kiện hàm/điểm khi biên soạn |
| H-YC-039 | 11 / 96 | Đạo hàm cấp hai: khái niệm, tính trường hợp đơn giản, ứng dụng gia tốc | CD06 / B17 / R1, R8 | Giữ; không suy ra bắt buộc điểm uốn/tính cong |
| H-YC-040 | 11 / 97 | Liên thuộc điểm/đường/mặt; ba cách xác định mặt phẳng; giao điểm/giao tuyến và vận dụng; nhận chóp/tứ diện; hình thực tiễn | CD11 / B30 / R3, R8 | Làm rõ ba cách xác định mặt phẳng |
| H-YC-041 | 11 / 97 | Hai đường không gian: trùng/song song/cắt/chéo; tính chất song song và ứng dụng | CD11 / B30 / R3 | Giữ; không đọc vị trí chỉ từ hình phối cảnh |
| H-YC-042 | 11 / 98 | Đường song song mặt: nhận biết, điều kiện, tính chất và ứng dụng | CD11 / B30 / R3 | Giữ điều kiện đường không thuộc mặt khi cần |
| H-YC-043 | 11 / 98 | Hai mặt song song: điều kiện/tính chất, định lí Thalès, tính chất lăng trụ/hộp và ứng dụng | CD11 / B30 / R3 | Giữ cả giải thích, không chỉ nhận dạng |
| H-YC-044 | 11 / 98 | Phép chiếu song song: khái niệm/tính chất; ảnh điểm/đoạn/tam giác/đường tròn; vẽ hình biểu diễn và ứng dụng | CD11 / B30 / R3, R8 | Ghi đủ các đối tượng ảnh; giữ trường hợp suy biến khi có liên quan |
| H-YC-045 | 11 / 99 | Góc hai đường; nhận biết/chứng minh hai đường vuông góc trong trường hợp đơn giản và ứng dụng | CD11 / B31 / R3 | Giữ; hai đường vuông góc không buộc cắt nhau trong không gian |
| H-YC-046 | 11 / 99 | Đường vuông góc mặt: khái niệm/điều kiện; ba đường vuông góc, quan hệ song song–vuông góc; phép chiếu vuông góc và ảnh điểm/đường/tam giác | CD11 / B31 / R3 | Giữ đủ hình chiếu và giải thích định lí |
| H-YC-047 | 11 / 99 | Nhận công thức và tính thể tích chóp/lăng trụ/hộp đơn giản; dùng đường cao/đáy đúng | CD11 / B32 / R3, R8 | Giữ; không chuyển hết thể tích sang tích phân |
| H-YC-048 | 11 / 100 | Hai mặt vuông góc: nhận biết/điều kiện/tính chất; lăng trụ đứng/đều, hộp đứng/chữ nhật, lập phương, chóp đều; ứng dụng | CD11 / B31 / R3 | Làm rõ các loại hình để chia mục tiêu |
| H-YC-049 | 11 / 100 | Khoảng cách điểm–đường, điểm–mặt, các đối tượng song song; đường vuông góc chung và khoảng cách hai đường chéo đơn giản; ứng dụng | CD11 / B32 / R3 | Giữ giới hạn trường hợp và phân biệt định nghĩa/cách tính |
| H-YC-050 | 11 / 100–101 | Góc đường–mặt, góc nhị diện và góc phẳng nhị diện: nhận biết, xác định/tính trường hợp đơn giản, ứng dụng | CD11 / B31 / R3 | Bổ sung rõ góc phẳng nhị diện |
| H-YC-051 | 11 / 101 | Nhận hình chóp cụt đều, tính thể tích và ứng dụng | CD11 / B32 / R3, R8 | Giữ; đã có ở 0.5 |
| H-YC-052 | 11 / 101–102 | Trung bình/trung vị/tứ phân vị/mốt mẫu ghép nhóm: tính, ý nghĩa/vai trò, kết luận và liên hệ liên môn | CD13 / B37 / R2, R8 | Giữ; diễn giải mức ước lượng của kết quả ghép nhóm |
| H-YC-053 | 11 / 102 | Biến cố hợp/giao/độc lập; xác suất hợp, giao độc lập, tổ hợp và cây trong bài đơn giản | CD14 / B40 / R4 | Giữ; không nhầm độc lập với xung khắc |
| H-YC-054 | 12 / 105–106 | Nhận đồng biến/nghịch biến từ dấu đạo hàm cấp một; thể hiện bảng biến thiên; nhận đơn điệu/điểm cực trị/giá trị cực trị từ bảng hoặc hình đồ thị | CD07 / B18 / R1 | Giữ; đây là phần CT chính của R1-G01 |
| H-YC-055 | 12 / 106 | Nhận giá trị lớn nhất/nhỏ nhất trên tập cho trước; xác định bằng đạo hàm trường hợp đơn giản | CD07 / B19 / R1, R8 | Giữ; không gộp với cực trị địa phương |
| H-YC-056 | 12 / 106 | Nhận hình ảnh tiệm cận ngang/đứng/xiên | CD07 / B20 / R1 | Giữ cả ba loại; B12 là tiên quyết giới hạn |
| H-YC-057 | 12 / 106 | Mô tả sơ đồ khảo sát; khảo sát và vẽ ba dạng hàm được CT nêu với điều kiện; nhận tính đối xứng | CD07 / B21 / R1 | Ghi rõ dạng và điều kiện ở H.3; không bỏ phân thức bậc hai/bậc nhất |
| H-YC-058 | 12 / 106–107 | Vận dụng đạo hàm và khảo sát vào vấn đề thực tiễn | CD07 / B19, B21 / R1, R8 | Giữ; không suy mọi tối ưu thuộc chuyên đề |
| H-YC-059 | 12 / 107 | Nguyên hàm: khái niệm, giải thích tính chất, bảng hàm sơ cấp được liệt kê, tính trường hợp đơn giản | CD08 / B22 / R7 | Làm rõ bảng nguyên hàm và tính chất, không chỉ thuật tính |
| H-YC-060 | 12 / 107 | Tích phân: định nghĩa/tính chất và tính trường hợp đơn giản | CD08 / B23 / R7 | Đổi tên chính thành Tích phân; giữ tích lũy trong diễn giải |
| H-YC-061 | 12 / 107 | Tính diện tích hình phẳng/thể tích hình khối; vận dụng tích phân vào thực tiễn | CD08 / B24 / R7, R3, R8 | Giữ; CT không gọi “tích lũy” là tiêu đề nội dung |
| H-YC-062 | 12 / 108 | Vectơ không gian và phép toán; tọa độ/độ dài, biểu thức tọa độ và ứng dụng | CD12 / B33 / R3, R8 | Giữ; gắn rõ nối Oxy–Oxyz |
| H-YC-063 | 12 / 108 | Mặt phẳng: tổng quát; lập qua điểm/pháp tuyến, điểm/cặp chỉ phương, ba điểm không thẳng hàng; điều kiện song song/vuông góc; khoảng cách và ứng dụng | CD12 / B34 / R3 | Làm rõ đủ ba cách, không chỉ công thức pháp tuyến |
| H-YC-064 | 12 / 108–109 | Đường thẳng Oxyz: chính tắc/tham số/chỉ phương; lập qua điểm/chỉ phương hoặc hai điểm; vị trí chéo/cắt/song song/vuông góc | CD12 / B35 / R3 | Giữ đủ vị trí; chia B35 thành mục tiêu con |
| H-YC-065 | 12 / 109 | Thiết lập công thức góc đường–đường/đường–mặt/mặt–mặt và ứng dụng đường thẳng không gian | CD12 / B35 / R3, R8 | Giữ; phân biệt góc giữa mặt phẳng với góc nhị diện có chọn miền |
| H-YC-066 | 12 / 109 | Mặt cầu: nhận phương trình, xác định tâm/bán kính, lập khi biết tâm/bán kính, ứng dụng | CD12 / B35 / R3, R8 | Giữ; không coi B35 là một bài học duy nhất |
| H-YC-067 | 12 / 110 | Khoảng biến thiên/khoảng tứ phân vị/phương sai/độ lệch chuẩn mẫu ghép nhóm: tính, giải thích, kết luận, liên hệ liên môn | CD13 / B38 / R2, R8 | Giữ; không dùng cùng số đo để kết luận quá phạm vi dữ liệu |
| H-YC-068 | 12 / 110 | Xác suất có điều kiện: khái niệm và ý nghĩa tình huống quen thuộc | CD14 / B41 / R4 | Giữ; điều kiện xác suất mẫu số dương |
| H-YC-069 | 12 / 110 | Mô tả toàn phần/Bayes từ bảng 2×2 và cây; dùng Bayes/cây tính xác suất có điều kiện, vận dụng | CD14 / B41 / R4, R2, R8 | Giữ bảng và cây, không chỉ thay số công thức |

### H.2. Công cụ, thực hành, trải nghiệm và chuyên đề

| Nguồn CT | Phạm vi phải có vị trí | Vị trí ZO Math và cách giữ điều kiện |
| --- | --- | --- |
| 10 / tr.81 | Phần mềm hỗ trợ đại số, đồ thị bậc hai, hoa văn/hình khối | B04–B06, R1/R8; hoạt động phòng máy có điều kiện tổ chức |
| 10 / tr.84 | Phần mềm điểm/vectơ Oxy; đường thẳng, đường tròn, conic; thay tham số và thiết kế đồ họa | B26–B29, R3/R8; giữ nhãn có điều kiện |
| 10 / tr.86 | Phần mềm tính số đặc trưng mẫu không ghép nhóm và xác suất cổ điển | B36/B39, R2/R4; không đồng nhất công cụ học với công cụ thi |
| 10 / tr.87 | Tính toán/đo/ước lượng/tạo hình, biểu diễn dữ liệu; tiết kiệm–đầu tư; hoạt động câu lạc bộ/dự án; giao lưu có điều kiện | B04–B06, B25–B29, B36; R1/R2/R3/R5/R8. CT cho tổ chức một số hoạt động và bổ sung theo điều kiện; không biến mọi ví dụ thành gói bắt buộc |
| 11 / tr.96 | Phần mềm lượng giác, giới hạn/liên tục, lũy thừa/mũ/lôgarit, mô hình đạo hàm/tiếp tuyến | B07–B17, R1/R5/R6; có điều kiện. Không suy cụm “đồ thị hàm lũy thừa” ở thực hành thành toàn bộ lý thuyết mở rộng bắt buộc |
| 11 / tr.101 | Phần mềm đường/mặt/giao tuyến/hình không gian và đồ họa/vẽ kĩ thuật | B30–B32, R3/R8; có điều kiện |
| 11 / tr.102 | Phần mềm xu thế trung tâm mẫu ghép nhóm và tính xác suất | B37/B40, R2/R4; có điều kiện |
| 11 / tr.103 | Hình học trong đồ họa/kĩ thuật, lượng giác/xác suất liên môn; dân số, quản lí thu nhập/tích lũy/rủi ro; dự án/giao lưu | R2–R6/R8; chọn nhiệm vụ đại diện có sản phẩm, không dồn toàn bộ vào B42 |
| 12 / tr.107 | Phần mềm đồ thị, tương giao/biến đổi, hình khối và mô hình khối tròn xoay | B18–B24, R1/R7/R8; có điều kiện |
| 12 / tr.109 | Phần mềm điểm/vectơ Oxyz, đường/mặt/cầu và thay tham số | B33–B35, R3/R8; có điều kiện |
| 12 / tr.111 | Phần mềm tính phân bố nhị thức và thống kê | B38/B41 liên kết hồ sơ thực hành R2/R4; giữ nguyên điều kiện phòng máy. Phần chuyên đề 12.1 vẫn riêng; không vì dòng này mà yêu cầu toàn bộ lý thuyết biến ngẫu nhiên ở phần chung |
| 12 / tr.111 | Tính toán/đo/ước lượng/tạo hình; tọa độ/GPS/đồ họa; đạo hàm và tối ưu thực tiễn; tài chính; dự án/giao lưu | R1/R3/R5/R7/R8; chọn theo mục tiêu và điều kiện như CT |
| tr.87–89; 104–105; 112–114 | Chín chuyên đề học tập | Giữ kiểm kê C và ranh giới B.7. Chưa có sổ học liệu đáp ứng từng yêu cầu chuyên đề; không tính là đã hoàn tất chỉ vì có tên |
| tr.114–117 | Tự học, vốn kinh nghiệm, hoạt động chủ động; kết hợp phương pháp; đánh giá bằng bằng chứng và điều chỉnh dạy/học | Mục 1, 5–9; các hoạt động cụ thể là C. Đánh giá trong chương trình rộng hơn định dạng thi |

### H.3. Các chỗ phải đọc đúng công thức và thuật ngữ

Đã xem hình các trang CT 81, 106, 107 trong đợt rà. Các biểu thức dưới đây làm rõ phạm vi, không thay việc tự giải và kiểm điều kiện của từng bài sản xuất:

- B06: $\sqrt{ax^2+bx+c}=\sqrt{dx^2+ex+f}$ và $\sqrt{ax^2+bx+c}=dx+e$ là hai dạng ở tr.81. Phải kiểm điều kiện và nghiệm sau biến đổi.
- B21: $y=ax^3+bx^2+cx+d$ với $a\ne0$; $y=\frac{ax+b}{cx+d}$ với $c\ne0$, $ad-bc\ne0$; $y=\frac{ax^2+bx+c}{mx+n}$ với $a\ne0$, $m\ne0$, đa thức tử không chia hết cho đa thức mẫu. Tập xác định và điều kiện mẫu khác 0 vẫn phải xét.
- B22: CT tr.107 liệt kê các hàm $x^\alpha$ với $\alpha\ne-1$, $\frac{1}{x}$, $\sin x$, $\cos x$, $\frac{1}{\cos^2x}$, $\frac{1}{\sin^2x}$, $a^x$, $e^x$. Điều kiện xác định của từng hàm phải đi kèm; đây là danh sách hàm cần tìm nguyên hàm, không phải bảng đáp án.
- B31: góc nhị diện và góc phẳng nhị diện có mục tiêu riêng; B34 có ba cách cơ bản lập mặt phẳng; B35 cần kiểm riêng đường có thành phần chỉ phương bằng 0 trước khi viết dạng chính tắc.

### H.4. Các việc chưa đủ bằng chứng và cách đóng khi sản xuất

| Khoảng trống còn mở | Bằng chứng cần để đóng | Cách xử lý hiện tại |
| --- | --- | --- |
| Từng yêu cầu nguyên tử đã có đủ nhiệm vụ đánh giá hay chưa | Sổ phân đoạn, ma trận nhiệm vụ, lời giải và kiểm định từng mục tiêu | Làm tại gói liên quan; không treo toàn bộ dự án chờ chứng nhận 100% |
| D0 phân loại/sửa lỗi hiệu quả thế nào với học sinh thực | Bài làm, mức hỗ trợ, thử lại độc lập, lỗi và thời gian | Giữ D0 v1.0 hoàn tất về thành phẩm; chưa khẳng định hiệu quả thực nghiệm |
| Ý đồ sư phạm trong SGV | Đúng sách/ấn bản/trang đã đọc | Chưa truy xuất được đúng tệp trong đợt này; không gán lời cho SGV |
| Ngày, phương tiện, quy cách riêng kỳ thi 2027 | Công bố chính thức đúng đối tượng và thời điểm áp dụng | Cấu hình tạm 3.14; cập nhật theo 12.14 |
| Lịch gia nhập muộn và ngưỡng C có phù hợp không | Giờ thực, mục tiêu được phủ, bằng chứng duy trì/phối hợp, tắc nghẽn | Theo dõi 5.7/12.13; chưa có kiểm chứng nhân quả |
