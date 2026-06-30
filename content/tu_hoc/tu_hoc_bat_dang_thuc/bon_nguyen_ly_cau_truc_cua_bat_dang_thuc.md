# Bốn nguyên lý cấu trúc của bất đẳng thức  
*Chương mở đầu - Tự học Bất đẳng thức*

## 1. Giới thiệu
Dự án Tự học Bất đẳng thức đặt mục tiêu không dừng lại ở việc liệt kê các bất đẳng thức hoặc học thuộc các “dạng bài”, mà đi đến mức độ hiểu *bản chất toán học* của bất đẳng thức, nắm rõ *cấu trúc sinh* ra chúng, và phát triển *tư duy giải thích - dự đoán - sáng tạo* bất đẳng thức mới.

Trọng tâm của chương mở đầu này là trình bày *bốn nguyên lý cấu trúc* (structural principles) xuất hiện xuyên suốt trong lý thuyết bất đẳng thức cổ điển và hiện đại. Những nguyên lý này không phải là thủ thuật giải bài, mà là những đặc điểm hình học, đại số và phân tích đứng phía sau phần lớn các bất đẳng thức được dùng trong Toán học.

Bốn nguyên lý cấu trúc:

1. *Nguyên lý độ cong* (Convexity Principle)  
2. *Nguyên lý độ phân tán và tái sắp xếp* (Majorization and Rearrangement Principle)  
3. *Nguyên lý tuyến tính hóa qua dạng bậc hai* (Quadratic Positivity / Linearization Principle)  
4. *Nguyên lý đồng nhất hóa và chuẩn hóa* (Homogenization and Normalization Principle)

Các nguyên lý này được chọn không phải vì tính phổ biến, mà vì tính *khai sinh*. Mỗi nguyên lý là một động cơ tạo dạng (generative engine) cho nhiều bất đẳng thức lớn: từ AM-GM, Cauchy-Schwarz đến Hölder, Minkowski, Karamata, Schur, Nesbitt và vô số bất đẳng thức tối ưu hóa.

## 2. Nguyên lý độ cong  
### 2.1 Định nghĩa và bản chất
Hàm \(f : I \to \mathbb{R}\) là *lồi* nếu:
\[
f(\lambda x + (1-\lambda)y)
\le \lambda f(x) + (1-\lambda)f(y)
\quad (0 < \lambda < 1).
\]

Định nghĩa này là bản dịch đại số của hình ảnh hình học: *đồ thị của hàm lồi nằm dưới dây cung nối hai điểm bất kỳ.*

Độ cong sinh bất đẳng thức vì *trung bình của hai giá trị thường “nằm thấp hơn” so với giá trị của hàm tại trung điểm* (hoặc ngược lại với hàm lõm).

### 2.2 Các bất đẳng thức sinh từ độ cong
1. Jensen  
2. Young  
3. Hölder  
4. Minkowski  
5. AM-GM (hàm \(\ln t\) là concave)  
6. Power means inequality  
7. Karamata (phiên bản tổng quát liên quan majorization)

### 2.3 Ví dụ: AM-GM từ Jensen
Hàm \(f(t) = \ln t\) là concave.

\[
\ln\left(\frac{x+y}{2}\right)
\ge \frac{\ln x + \ln y}{2}
\]

Lấy mũ:
\[
\frac{x+y}{2} \ge \sqrt{xy}.
\]

Điều này cho thấy AM-GM không phải “mẹo”, mà là hệ quả tất yếu của tính lõm của \(\ln t\).

### 2.4 Tài liệu chuẩn
- Rockafellar - *Convex Analysis*  
- Boyd & Vandenberghe - *Convex Optimization* (Ch. 3-5)  
- Hardy-Littlewood-Pólya - *Inequalities*, chương 2-3  


## 3. Nguyên lý độ phân tán và tái sắp xếp (Majorization)
### 3.1 Định nghĩa chuẩn
Sắp xếp giảm dần:
\[
x_1 \ge x_2 \ge \cdots \ge x_n,\quad
y_1 \ge \cdots \ge y_n.
\]

Vector \(x\) *majorizes* \(y\) (ký hiệu \(x \succ y\)) nếu:
\[
\sum_{i=1}^k x_i \ge \sum_{i=1}^k y_i
\quad (1 \le k \le n),
\]
và:
\[
\sum_{i=1}^n x_i = \sum_{i=1}^n y_i.
\]

Majorization mô tả sự “lệch” và “đều” một cách toán học:
- vector *lệch hơn* có một vài giá trị lớn vượt trội,
- vector *đều hơn* trải đều giá trị.

### 3.2 Định lý cơ bản
Nếu \(f\) là hàm lồi, thì:
\[
x \succ y \quad \Rightarrow \quad 
\sum f(x_i) \ge \sum f(y_i).
\]

Đây là nội dung của *Karamata inequality*, một trong các định lý mạnh nhất của bất đẳng thức đối xứng.

### 3.3 Ví dụ kinh điển
\((4,1) \succ (2.5,2.5)\).

Với \(f(t)=t^2\) lồi:
\[
4^2 + 1^2 \ge 2.5^2 + 2.5^2.
\]

Từ đây sinh ra:
- inequality of means,  
- rearrangement inequality,  
- Schur,  
- nhiều bất đẳng thức đối xứng bậc cao.

### 3.4 Tài liệu chuẩn
- Marshall-Olkin-Arnold - *Inequalities: Theory of Majorization*  
- Hardy-Littlewood-Pólya - *Inequalities*, chương 2  

---

## 4. Nguyên lý tuyến tính hóa qua dạng bậc hai  
### 4.1 Bản chất
Tuyến tính hóa không phải mẹo, mà là hệ quả của:
\[
\sum (a_i - \lambda b_i)^2 \ge 0.
\]

Đây là tính dương của một dạng bậc hai trong tham số \(\lambda\).  
Điều kiện để đa thức \(A\lambda^2 - 2B\lambda + C\) không âm với mọi \(\lambda\) là:
\[
B^2 \le AC.
\]

### 4.2 Sinh ra Cauchy-Schwarz
Từ:
\[
\sum (a_i - \lambda b_i)^2 \ge 0
\]
suy ra:
\[
(\sum a_i b_i)^2 
\le (\sum a_i^2)(\sum b_i^2).
\]

Quadratic positivity là nền cho:
- Cauchy-Schwarz  
- Hölder (qua Minkowski duality)  
- Bất đẳng thức trong không gian Hilbert

### 4.3 Tài liệu chuẩn
- Steele - *The Cauchy-Schwarz Master Class*  
- Tao - *Analysis I*  
- Lax - *Linear Algebra and Its Applications*

## 5. Nguyên lý đồng nhất hóa và chuẩn hóa
### 5.1 Khái niệm
Hàm \(F\) đồng bậc bậc \(k\) nếu:
\[
F(tx,ty,tz) = t^k F(x,y,z).
\]

Biểu thức \(I\) bất biến theo tỉ lệ nếu:
\[
I(tx,ty,tz) = I(x,y,z).
\]

### 5.2 Nguyên lý chuẩn hóa
Nếu bất đẳng thức có tính đồng bậc hoặc bất biến theo tỉ lệ, ta có thể thêm giả thiết:
- \(x+y+z = 1\),  
- hoặc \(xyz = 1\),  
- hoặc \(xy + yz + zx = 1\),  
mà *không làm mất tính tổng quát*.

Đây là kết quả của phép biến đổi:
\[
a = \frac{x}{x+y+z},\quad b = \frac{y}{x+y+z},\quad c = \frac{z}{x+y+z}.
\]

### 5.3 Ví dụ: Nesbitt
\[
\frac{x}{y+z}+\frac{y}{z+x}+\frac{z}{x+y} \ge \frac{3}{2}.
\]

Biểu thức degree zero → đặt \(x+y+z=1\).

Sau biến đổi:
\[
\frac{a}{1-a}+\frac{b}{1-b}+\frac{c}{1-c} \ge \frac{3}{2}.
\]

Chứng minh bằng Cauchy-Schwarz:
\[
\left(\sum \frac{1}{1-a}\right)\left(\sum (1-a)\right)\ge 9.
\]

### 5.4 Ví dụ homogenization không đồng bậc
\[
\frac{x^2}{y+z} + \frac{y^2}{z+x} + \frac{z^2}{x+y}
\ge \frac{x+y+z}{2}.
\]

Không đồng bậc → nhân với \(x+y+z\) để đồng bậc bậc 2 → chuẩn hóa.

### 5.5 Tối ưu hóa degree zero
\[
F(x,y,z) = \frac{x}{y} + \frac{y}{z} + \frac{z}{x}.
\]

Bất biến theo tỉ lệ → đặt \(xyz = 1\).

### 5.6 Tài liệu chuẩn
- Engel - *Problem Solving Strategies*  
- Mitrinović - *Analytic Inequalities*  
- Bullen - *Handbook of Means*


## 6. Mối liên hệ giữa bốn nguyên lý
1. Convexity sinh ra majorization (Karamata).  
2. Majorization cho ra Schur, rearrangement.  
3. Linearization cho ra Cauchy-Schwarz → dẫn đến Hölder qua dual norms.  
4. Homogenization gắn kết các nguyên lý bằng việc đưa bài toán về simplex hoặc không gian bất biến theo tỉ lệ.

Tổng hợp lại, bốn nguyên lý tạo thành bản đồ chung cho hầu hết bất đẳng thức phổ biến.


## 7. Tài liệu chuẩn mực để tự học
1. Hardy-Littlewood-Pólya - *Inequalities*  
2. Marshall-Olkin-Arnold - *Majorization and Inequalities*  
3. Steele - *The Cauchy-Schwarz Master Class*  
4. Mitrinović - *Analytic Inequalities*  
5. Engel - *Problem-Solving Strategies*  
6. Rockafellar - *Convex Analysis*  
7. Tao - *Analysis I, II*


## 8. Định hướng học tập
1. Hiểu sâu từng nguyên lý cấu trúc.  
2. Viết lại mỗi bất đẳng thức bằng nguyên lý sinh ra nó.  
3. Thực hành bài tập có mục đích: nền tảng, mở rộng, bẫy, cực trị.  
4. Đọc theo thứ tự:  
   Steele → HLP → MOA → các tài liệu bổ sung.  


*Chương này tổng hợp toàn bộ nội dung đã trao đổi trong giai đoạn khởi đầu của dự án Tự học Bất đẳng thức, với định nghĩa chuẩn, lập luận chặt chẽ, ví dụ kinh điển và định hướng học tập.*
