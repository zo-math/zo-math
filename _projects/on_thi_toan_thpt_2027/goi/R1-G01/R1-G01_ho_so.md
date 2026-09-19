# ZO Math — Hồ sơ gói R1-G01

## 1. Định danh và trạng thái

- **Tên gói:** Kết nối hàm số, bảng biến thiên và đồ thị.
- **Vai trò:** gói học liệu ngang cấp với D0 trong ấn bản ôn thi 2027.
- **Trạng thái nghiên cứu:** đã kết tinh ở cấp gói.
- **Lịch sử biên tập:** v1.0 đã được đọc và tiếp nhận góp ý; v1.1 là ứng viên đang thẩm định sau vòng đọc thứ nhất.
- **Phát hành:** chưa duyệt phát hành; chưa công bố website.
- **Studio:** chưa sản xuất Studio chính thức.
- **Thử nghiệm:** chưa có dữ liệu học sinh sử dụng v1.1.

Hồ sơ này giữ các quyết định nội dung và trạng thái chính thức của gói. Công cụ nghiên cứu từng được dùng không phải đơn vị quản lí, trạng thái sản xuất hoặc cấu trúc lưu trữ của dự án.

## 2. Câu hỏi trung tâm và phạm vi

Từ công thức, dấu đạo hàm, bảng biến thiên và đồ thị, học sinh có thể suy ra chính xác điều gì về hàm số; cần kiểm tra những điều kiện nào; và những kết luận nào vượt quá dữ kiện?

Gói tập trung vào:

- mối liên hệ giữa công thức, đạo hàm, dấu đạo hàm, chiều biến thiên, bảng biến thiên và đồ thị;
- tính đơn điệu và điều kiện dùng dấu đạo hàm;
- cực trị và điều kiện kết luận từ sự đổi dấu;
- tập xác định, khoảng xét, điểm bị loại và giới hạn của từng biểu diễn;
- đánh giá phát biểu, phân tích lỗi, sửa lập luận và làm bài mới để kiểm tra lỗi đã sửa.

Không thuộc phạm vi gói:

- giá trị lớn nhất và giá trị nhỏ nhất trên miền xét;
- tiệm cận;
- bài toán tối ưu;
- toàn bộ quy trình khảo sát hàm số;
- định lí Fermat, quy tắc đạo hàm cấp hai hoặc các mở rộng không cần cho mục tiêu hiện tại.

## 3. Mục tiêu học tập

| Mục tiêu | Yêu cầu | Bằng chứng ưu tiên trong v1.1 |
|---|---|---|
| M1 | Kết nối các biểu diễn của hàm số. | Bài luyện tập 01, 03, 05; các ý tương ứng trong bài kiểm tra 01–03. |
| M2 | Nêu khoảng xét và điều kiện cần kiểm tra; dùng dấu đạo hàm để kết luận đồng biến hoặc nghịch biến. | Bài luyện tập 01, 02, 06; bài kiểm tra 01, 02, 04. |
| M3 | Kiểm tra điều kiện cực trị; phân biệt điểm cực trị của hàm số, giá trị cực trị và điểm cực trị của đồ thị. | Bài luyện tập 03–05, 08; bài kiểm tra 01, 02, 04. |
| M4 | Đánh giá phát biểu từ giả thiết và giải thích bằng lập luận hoặc phản ví dụ. | Bài luyện tập 05–07; bài kiểm tra 03–05. |
| M5 | Phân tích lỗi, sửa lập luận và làm bài mới kiểm tra đúng lỗi đó. | Bài luyện tập 08; các bài tập khắc phục lỗi và nhật kí học tập. |

Các bằng chứng trên xác nhận cấu trúc học liệu đã được biên soạn, không chứng minh học sinh đã đạt mục tiêu.

## 4. Kết quả nghiên cứu đã kết tinh

Phần này tổng hợp có kiểm chứng từ khung sản phẩm, các kết quả nghiên cứu tiền nhiệm, đề cương sản xuất, bản nội dung nền và hồ sơ biên tập v1.1.

### 4.1. Đơn điệu và dấu đạo hàm

- Định nghĩa đồng biến, nghịch biến dựa trên so sánh giá trị hàm số trên tập đang xét, không phụ thuộc vào việc đã dùng đạo hàm hay chưa.
- Nếu hàm số có đạo hàm trên một khoảng và đạo hàm dương tại mọi điểm của khoảng thì hàm số đồng biến; nếu đạo hàm âm tại mọi điểm thì hàm số nghịch biến.
- Kết luận vẫn được giữ trong trường hợp đạo hàm bằng không tại một số hữu hạn điểm và có dấu nghiêm ngặt phù hợp tại mọi điểm còn lại trên khoảng.
- Chiều đảo nghiêm ngặt là sai: hàm số đồng biến và có đạo hàm chỉ cho phép suy đạo hàm không âm, không bắt buộc đạo hàm dương tại mọi điểm.
- Nghiệm của phương trình đạo hàm bằng không chỉ tạo ra một điểm cần xét; nó không tự xác nhận sự đổi chiều biến thiên hoặc cực trị.

Đối chứng trung tâm là hàm số

$$
f(x)=(x-1)^3+2,
$$

có

$$
f'(x)=3(x-1)^2.
$$

Đạo hàm bằng không tại $x=1$ nhưng giữ dấu dương ở hai phía; hàm số vẫn đồng biến trên toàn bộ $\mathbb{R}$ và tiếp tuyến tại $(1;2)$ nằm ngang.

### 4.2. Cực trị

- Cực trị được xác định bằng so sánh giá trị hàm số trong một lân cận của điểm đang xét.
- Phải phân biệt điểm cực trị của hàm số $x_0$, giá trị cực trị $f(x_0)$ và điểm cực trị của đồ thị $(x_0;f(x_0))$.
- Với các giả thiết phù hợp về liên tục tại mốc và đạo hàm trên hai khoảng hai phía, dấu đạo hàm đổi từ dương sang âm cho cực đại; đổi từ âm sang dương cho cực tiểu.
- Đạo hàm bằng không tại một điểm không đủ để kết luận có cực trị.
- Đạo hàm không tồn tại tại một điểm không tự loại trừ cực trị.

Hai đối chứng trung tâm:

- $y=x^3$ có $f'(0)=0$ nhưng không có cực trị tại $0$ vì hàm số không đổi chiều biến thiên.
- $y=|x|$ có cực tiểu tại $0$ dù đạo hàm tại đó không tồn tại; kết luận được kiểm tra bằng định nghĩa và hành vi hai phía.

### 4.3. Kết nối các biểu diễn

Chuỗi

$$
\text{công thức}\to\text{đạo hàm}\to\text{dấu đạo hàm}
\to\text{chiều biến thiên}\to\text{bảng biến thiên}\to\text{đồ thị}
$$

là một mạch suy luận cần điều kiện, không phải chuỗi tương đương hai chiều.

- Công thức có thể cung cấp tập xác định, đạo hàm, giá trị tại mốc và giới hạn khi thực hiện đủ phép tính.
- Bảng dấu đạo hàm cho phép suy chiều biến thiên trên các khoảng hợp lệ, nhưng không tự cho mọi giá trị của hàm số hoặc một đồ thị duy nhất.
- Bảng biến thiên cho biết chiều biến thiên và các giá trị hoặc giới hạn được ghi; không tự cho công thức hoặc dấu đạo hàm nghiêm ngặt tại mọi điểm.
- Đồ thị cho phép đọc thông tin hình học trong phạm vi hình và nhãn đã cho; không được tự thêm độ chính xác, giao điểm, giới hạn hoặc công thức.
- Các biểu diễn chỉ được ghép khi mô tả cùng hàm số, cùng miền, cùng mốc và không mâu thuẫn dữ kiện.
- Điểm bị loại khỏi tập xác định không thể là điểm cực trị; không được gộp hai khoảng qua điểm bị loại mà chưa kiểm tra định nghĩa trên tập đang xét.

### 4.4. Sửa lỗi và kiểm tra lại

Quy trình được giữ trong học liệu:

1. xác định phát biểu hoặc bước làm sai;
2. chỉ ra giả thiết, điều kiện hoặc chiều suy luận bị dùng sai;
3. giữ lại phần đúng;
4. viết lại lập luận;
5. làm một bài mới đánh đúng lỗi vừa sửa;
6. ghi kết quả và lịch ôn lại.

Đọc lời giải hoặc làm lại bài đã nhớ đáp án không đủ để kết luận lỗi đã được sửa.

## 5. Cấu trúc học liệu v1.1

Gói ứng viên có:

- 4 câu hỏi khởi động;
- 8 ví dụ;
- 6 câu hỏi tự kiểm tra trong bài học;
- 1 bài tập khắc phục lỗi mẫu;
- 8 bài luyện tập;
- 5 bài kiểm tra, tổng 20 điểm, thời lượng dự kiến 45 phút;
- 8 bài tập khắc phục lỗi;
- phần lời giải, hướng dẫn chấm và nhật kí học tập;
- 10 đồ thị được dựng từ công thức;
- 13 bảng dấu hoặc bảng biến thiên từ dữ liệu tường minh.

Thời lượng và thang điểm phục vụ lượt dùng thử của gói, không được coi là cấu trúc đề thi chính thức hoặc bằng chứng hiệu quả học tập.

## 6. Quyết định biên tập từ vòng đọc v1.0

Các góp ý vòng một đã được đưa vào v1.1:

- dùng “tập xác định” cho tập đầu vào và “khoảng” cho nơi xét đơn điệu;
- đổi tên học liệu thành “Kết nối hàm số, bảng biến thiên và đồ thị”, với dòng phụ về dấu đạo hàm, tính đơn điệu và cực trị;
- làm rõ mục tiêu đơn điệu và điều kiện áp dụng;
- sửa bài kiểm tra về dữ kiện thiếu tính liên tục;
- chuyển giá trị tại trục tung sang đúng bước phác đồ thị;
- gọi rõ “kết nối các biểu diễn của hàm số”;
- tách Học, Luyện tập, Kiểm tra, Sửa lỗi và Ôn lại;
- thống nhất tên hoạt động hiển thị cho học sinh;
- giữ mã nội bộ trong hồ sơ, không dùng thay tên hoạt động;
- dùng “Nhật kí học tập” và ghi đủ bài làm, lỗi, cách sửa, kết quả bài mới và ngày ôn;
- tách học liệu học sinh khỏi hồ sơ biên tập;
- rà điều kiện toán học trên toàn gói;
- dựng lại đồ thị và chuẩn hóa bảng;
- phân biệt phân tích lỗi, sửa bài, bài tập khắc phục lỗi và kiểm tra lại.

## 7. Nguồn và giới hạn đối chiếu

Nguồn hiện hành:

1. Chương trình giáo dục phổ thông môn Toán 2018, đặc biệt các yêu cầu về dấu đạo hàm, tính đơn điệu, bảng biến thiên và cực trị.
2. Toán 12, tập một — Kết nối tri thức với cuộc sống, trọng tâm phần đơn điệu, cực trị và trình tự lập bảng, vẽ đồ thị.
3. Kế hoạch điều hành 0.6 của dự án.
4. Kết quả nghiên cứu tiền nhiệm, đề cương sản xuất và quyết định biên tập đã được đối chiếu trong quá trình tạo v1.0–v1.1.

Các bài tập và lời giải là nội dung ZO Math tự biên soạn. Nguồn chính thức được dùng để đối chiếu thuật ngữ, điều kiện và yêu cầu cần đạt; không gán nội dung tự biên soạn thành yêu cầu nguyên văn của Bộ.

## 8. Nguồn sản xuất và quan hệ sinh tệp

Nguồn nội dung canonical là `src/noi_dung.html`. Dữ liệu bảng nằm ở `src/bang_bien_thien.json`; đồ thị được dựng bởi `src/zo_bieu_dien.py`.

```text
src/noi_dung.html + dữ liệu + CSS + font + hình
    -> R1-G01_NOI_DUNG_v1.1.md
    -> R1-G01_HOC_LIEU_v1.1.html
    -> R1-G01_HOC_LIEU_v1.1.pdf
```

Markdown, HTML và PDF là đầu ra có thể tái sinh. Mọi sửa đổi nội dung phải bắt đầu từ nguồn tương ứng trong `src/`.

## 9. Lịch sử và việc tiếp theo

- v1.0: bộ dùng thử đầu tiên; đã được đọc và tiếp nhận góp ý.
- v1.1: đã thực hiện các quyết định biên tập của vòng một; đang chờ thẩm định tiếp.
- Chưa có bản được duyệt phát hành, chưa công bố website và chưa có Studio chính thức.

Việc tiếp theo duy nhất là hoàn tất thẩm định v1.1 trên HTML và PDF đã tái sinh, ghi nhận lỗi cụ thể nếu có, rồi mới quyết định vòng sửa tiếp theo hoặc duyệt cho bước sử dụng thử.
