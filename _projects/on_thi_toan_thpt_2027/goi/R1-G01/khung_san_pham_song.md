# ZO Math — Ôn thi Toán THPT 2027
## R1-G01 — Khung sản phẩm sống

- **Phiên bản:** 0.1
- **Trạng thái:** tài liệu điều phối chính thức đang sống; chưa phải học liệu công bố
- **Gói:** R1-G01 — Kết nối đạo hàm, bảng biến thiên và đồ thị
- **Cập nhật sau:** NB01 — Đạo hàm và Đơn điệu; NB02 — Đạo hàm và Cực trị

---

## 1. Vai trò của tài liệu này

Tài liệu này là cầu nối giữa **nghiên cứu trong Notebook** và **bộ học liệu R1-G01 dành cho học sinh**.

Sau mỗi notebook:
1. ghi nhận phần kiến thức đã đủ chắc;
2. ánh xạ phần đó vào mục tiêu R1-G01-M1 đến M5;
3. chỉ ra khoảng trống còn lại;
4. xác định đúng câu hỏi nghiên cứu tiếp theo;
5. chỉ chuyển sang sản xuất học liệu hoàn chỉnh khi lõi nghiên cứu đã đủ.

Tài liệu này **không thay** bản kết tinh của từng notebook và **không phải** bài học để công bố.

---

## 2. Đích của gói R1-G01

### Câu hỏi trung tâm

Từ công thức, dấu đạo hàm, bảng biến thiên và đồ thị, học sinh suy ra được điều gì, cần điều kiện nào và dễ kết luận sai ở đâu?

### Phạm vi

R1-G01 tập trung vào:
- mối liên hệ đạo hàm – biến thiên – bảng biến thiên – đồ thị;
- tính đơn điệu;
- cực trị;
- các điều kiện và lỗi suy luận thường gặp trong các nội dung trên.

Chưa thuộc R1-G01:
- giá trị lớn nhất, giá trị nhỏ nhất;
- tiệm cận;
- tối ưu;
- toàn bộ quy trình khảo sát hàm số.

---

## 3. Trạng thái năm mục tiêu của R1-G01

| Mục tiêu | Trạng thái sau NB01 + NB02 | Bằng chứng hiện có | Phần còn thiếu |
|---|---|---|---|
| **M1 — Nối các biểu diễn** | **Đang hình thành** | NB01 đã nối chuỗi công thức → đạo hàm → dấu đạo hàm → chiều biến thiên → bảng biến thiên → dáng điệu đồ thị; đã lưu ý đây không phải chuỗi tương đương hai chiều | Chưa nghiên cứu có hệ thống việc đọc ngược/đổi qua lại giữa bảng dấu, bảng biến thiên và đồ thị; chưa kiểm tra đầy đủ điều kiện miền, khoảng xét, nhãn trục và giới hạn suy luận từ từng biểu diễn |
| **M2 — Giải thích đơn điệu** | **Đã đạt lõi nghiên cứu** | NB01 phân biệt định nghĩa đơn điệu với định lí dấu đạo hàm; giữ đúng điều kiện đủ; xử lí trường hợp đạo hàm bằng 0 tại hữu hạn điểm; thực hành và kiểm chứng | Sau này cần chuyển thành nhiệm vụ luyện và kiểm tra độc lập cho học sinh |
| **M3 — Xác định cực trị** | **Đã đạt lõi nghiên cứu** | NB02 xác lập định nghĩa, thuật ngữ, điều kiện đủ qua đổi dấu của đạo hàm; xử lí \(x^3\), \(|x|\); hoàn thành 5 bài thực hành | Sau này cần chuyển thành nhiệm vụ luyện và kiểm tra độc lập cho học sinh |
| **M4 — Đúng/sai có lí do** | **Chưa hoàn thành** | NB01–NB02 đã phát hiện nhiều mệnh đề dễ sai và đã sửa lập luận | Chưa có một cụm đúng/sai được thiết kế và tự giải theo đúng quy tắc của gói |
| **M5 — Tự sửa lỗi và dùng câu mới** | **Chưa hoàn thành** | Quá trình nghiên cứu đã có sửa lỗi sau phản biện | Chưa có quy trình học sinh ghi lỗi → sửa → làm câu mới cùng mục tiêu và chưa có câu sau chữa được kiểm chứng |

---

## 4. Lõi kiến thức đã đủ chắc để tái sử dụng

### Từ NB01 — Đạo hàm và Đơn điệu

Đã có thể dùng làm nền cho học liệu:
- định nghĩa đồng biến, nghịch biến;
- định lí dấu đạo hàm và phạm vi áp dụng;
- phân biệt điều kiện đủ với chiều suy luận đảo;
- trường hợp \(f'(x)=0\) tại một số hữu hạn điểm nhưng hàm vẫn giữ chiều biến thiên;
- chuỗi biểu diễn:
  công thức → đạo hàm → dấu đạo hàm → chiều biến thiên → bảng biến thiên → dáng điệu đồ thị;
- các ngộ nhận đã loại bỏ, đặc biệt:
  - \(f'(x_0)=0\) không tự động có nghĩa đổi chiều biến thiên;
  - đồng biến không buộc \(f'(x)>0\) tại mọi điểm;
  - không biến điều kiện đủ thành điều kiện cần và đủ.

### Từ NB02 — Đạo hàm và Cực trị

Đã có thể dùng làm nền cho học liệu:
- định nghĩa cực đại, cực tiểu;
- phân biệt:
  - điểm cực trị của hàm số;
  - giá trị cực trị;
  - điểm cực trị của đồ thị;
- điều kiện đủ qua dấu của \(f'\) ở hai phía;
- \(f'(x_0)=0\) không đủ để kết luận có cực trị;
- đạo hàm không tồn tại tại \(x_0\) không loại trừ cực trị;
- hai đối chứng trung tâm:
  - \(y=x^3\): \(f'(0)=0\) nhưng không có cực trị;
  - \(y=|x|\): có cực tiểu tại \(0\) dù \(f'(0)\) không tồn tại;
- 5 bài thực hành đã được tự giải và kiểm chứng.

---

## 5. Cấu trúc bộ học liệu R1-G01 sẽ được sản xuất

Đây là cấu trúc chính thức dự kiến của gói, nhưng **chưa viết thành phẩm** ở giai đoạn hiện tại.

### A. Chỉ dẫn vào gói + câu thử nền
Mục đích:
- kiểm tra nhanh học sinh có đủ nền về hàm số, đạo hàm và đọc biểu diễn hay không;
- nếu thiếu nền, chỉ rõ phần quay lại thay vì buộc học lại cả chương.

### B. Bài học lõi
Mạch nhận thức dự kiến:

1. Từ dấu đạo hàm đến chiều biến thiên.
2. Từ chiều biến thiên đến bảng biến thiên.
3. Từ bảng biến thiên đến dáng điệu đồ thị và ngược lại trong phạm vi dữ kiện cho phép.
4. Cực trị là gì và cách nhận biết đúng.
5. Những suy luận dễ sai:
   - đạo hàm bằng 0;
   - điểm không có đạo hàm;
   - suy quá dữ kiện từ bảng/đồ thị;
   - nhầm điểm cực trị với giá trị cực trị.

### C. Phiếu luyện
Mỗi M1–M5 phải có ít nhất:
- một nhiệm vụ luyện;
- một nhiệm vụ kiểm tra độc lập;
- thêm câu đại diện nếu mục tiêu có nhiều trường hợp.

### D. Lời giải và phản biện
Không chỉ cho đáp án:
- chỉ rõ điều kiện đã dùng;
- chỉ ra lỗi suy luận nếu có;
- đối chiếu giữa các biểu diễn khi thích hợp.

### E. Cụm kiểm tra mới
Dùng để kiểm tra sau khi học xong lõi R1-G01, không sao chép nguyên bài luyện.

### F. Câu sau chữa
Sau một lỗi:
- ghi lỗi;
- sửa lí do;
- làm một câu mới kiểm tra đúng lỗi vừa sửa.

### G. Lịch ôn lại
Ghi thời điểm quay lại câu/cụm mục tiêu sau khi chữa.

### H. Studio thử
Chỉ tạo sau khi lõi nội dung đủ chắc:
- một sơ đồ liên hệ các biểu diễn;
- một bài tự kiểm tra ngắn;
- mọi câu và cách chấm phải được kiểm định lại.

---

## 6. Phần còn thiếu trước khi chuyển sang sản xuất học liệu hoàn chỉnh

Khoảng trống nghiên cứu lớn nhất hiện nay là **M1 — nối các biểu diễn theo cả chiều đọc và chiều suy luận, với ranh giới kết luận từ từng biểu diễn**.

Cần làm rõ có hệ thống:
- từ bảng dấu \(f'\) suy ra bảng biến thiên và đồ thị được đến đâu;
- từ bảng biến thiên suy ra được gì về dấu đạo hàm, và điều gì không được suy quá;
- từ đồ thị suy ra được gì về đơn điệu, cực trị, dấu đạo hàm;
- vai trò của tập xác định, điểm gián đoạn, khoảng xét, nhãn trục;
- khi hai biểu diễn trông “khớp” nhưng thực ra mô tả khác miền hoặc thiếu dữ kiện;
- cách ghép công thức, bảng dấu, bảng biến thiên và đồ thị trong một nhiệm vụ.

M4 và M5 chủ yếu là **năng lực vận dụng/đánh giá**, nên chưa cần mở notebook lí thuyết riêng ngay. Chúng sẽ được tích hợp vào vòng thực hành sau khi M1 được làm chắc.

---

## 7. Phiên nghiên cứu tiếp theo được đề xuất

### NB03 — Đọc và nối các biểu diễn

**Câu hỏi nghiên cứu trung tâm dự kiến:**

> Từ bảng dấu đạo hàm, bảng biến thiên và đồ thị, ta có thể suy ra chính xác những thông tin nào về hàm số; những chiều suy luận nào hợp lệ, những chiều nào cần thêm điều kiện, và những lỗi nào xuất hiện khi bỏ qua tập xác định hoặc khoảng xét?

NB03 sẽ hoàn thiện phần còn thiếu của M1 và chuẩn bị chất liệu để sau đó kiểm tra M4–M5 bằng cụm bài đúng/sai, sửa lỗi và câu sau chữa.

---

## 8. Điều kiện để kết thúc pha nghiên cứu R1-G01

Chưa chuyển sang “Lõi học liệu và Studio” cho đến khi:

- M1 có bản kết tinh đủ chắc;
- M2 và M3 giữ trạng thái đã đạt;
- có một vòng thực hành phối hợp kiểm tra M1–M4;
- có ít nhất một chu trình sửa lỗi + câu mới cho M5;
- các phát biểu cốt lõi đã được kiểm tra điều kiện và nguồn.

Khi đó mới biên soạn **một lần có hệ thống**:
bài ôn → phiếu luyện → lời giải → cụm kiểm tra → câu sau chữa → lịch ôn lại → Studio thử.

---

## 9. Trạng thái hiện tại

**Pha hiện tại:** Nghiên cứu R1-G01.

**Đã khóa:**
- NB01 — Đạo hàm và Đơn điệu.
- NB02 — Đạo hàm và Cực trị.

**Chưa công bố học liệu R1-G01.**

**Việc kế tiếp duy nhất:** chuẩn bị NB03 để hoàn thiện M1 — đọc và nối các biểu diễn.
