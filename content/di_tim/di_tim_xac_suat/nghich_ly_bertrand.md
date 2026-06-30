# Nghịch lý Bertrand (Bertrand’s Paradox)
### Bản ghi chú học thuật ZO Math / Đi tìm Xác suất

---

## Bản chất của nghịch lý

> Trong một *đường tròn bán kính \(R\)*, chọn *một dây cung ngẫu nhiên*. Hỏi xác suất để dây cung ấy *dài hơn cạnh của tam giác đều nội tiếp* đường tròn là bao nhiêu?

Cạnh tam giác đều nội tiếp có độ dài \(s = R\sqrt{3}\).

Tưởng chừng chỉ có một đáp án, nhưng tuỳ cách hiểu “chọn ngẫu nhiên một dây cung”, ta nhận được *ba kết quả khác nhau*:  

\[
P = \frac{1}{3},\quad \frac{1}{2},\quad \frac{1}{4}.
\]

## Ba cách chọn và ba kết quả

| Cách chọn | Mô tả “ngẫu nhiên” | Đại lượng được chia đều | Kết quả |
|------------|--------------------|--------------------------|----------|
| **Cách 1** | Chọn **hai điểm** độc lập, đều trên đường tròn. | Góc ở tâm \(\theta \in [0, \pi]\) | \(P(\theta > 120^\circ) = 1/3\) |
| **Cách 2** | Chọn **một bán kính**, rồi **một trung điểm** đều theo độ dài trên bán kính đó; dây vuông góc tại điểm đó. | Độ dài \(r\in[0,R]\) | \(P(r<R/2)=1/2\) |
| **Cách 3** | Chọn **trung điểm đều trong toàn bộ hình tròn**, rồi dựng dây vuông góc với bán kính đi qua nó. | Diện tích \(A(r) = \pi r^2\) | \(P(r<R/2) = (1/2)^2 = 1/4\) |

**Công thức độ dài dây**
\[
L = 2\sqrt{R^2 - r^2}.
\]

Điều kiện dây dài hơn cạnh tam giác đều
\[
L > R\sqrt{3} \Rightarrow r < R/2.
\]

## Phân tích hình học & xác suất

### (a) Cách 1: chia đều theo *góc ở tâm*
- Tập khả năng là \(\theta \in [0, \pi]\).  
- Vì \(\theta\) phân bố đều,  
  \[
  P(\theta > 2\pi/3) = (\pi - 2\pi/3)/\pi = 1/3.
  \]

### (b) Cách 2: chia đều theo *độ dài dọc bán kính*
- \(r\) phân bố đều trong \([0,R]\).  
- Điều kiện \(r < R/2 \Rightarrow P = (R/2)/R = 1/2.\)  
- Tuy nhiên, ta đã **ngầm chọn ra một họ dây song song**,  
  nên không đại diện cho toàn bộ không gian dây.

### (c) Cách 3: chia đều theo *diện tích* (phân bố bất biến hình học)
- Xác suất trung điểm nằm trong bán kính \(x\):
  \[
  P(r<x)=(x/R)^2.
  \]
- Do đó \(P(r<R/2)=(1/2)^2=1/4.\)
- Đây là *phân bố duy nhất* tôn trọng đối xứng quay và tịnh tiến.


## Ý nghĩa triết học

### Nguyên lý thờ ơ của Laplace

> “Khi không có lý do để thiên vị khả năng nào, hãy chia đều xác suất cho tất cả các khả năng.”

Nghịch lý Bertrand cho thấy:
- “Chia đều” **phụ thuộc vào bạn đang chia đều cái gì** (góc, độ dài, diện tích…).
- Vì vậy, nguyên lý này **tự mâu thuẫn** nếu không xác định rõ “độ đo” trên không gian khả năng.

### Hệ quả triết học
- “Ngẫu nhiên” không phải là **tính chất khách quan tuyệt đối**,  
  mà là **một cấu trúc phụ thuộc vào cách ta mô tả hệ thống** (the measure space).
- Đây chính là động cơ dẫn đến **lý thuyết độ đo xác suất của Kolmogorov (1933)**:  
  mọi phát biểu xác suất phải được gắn với một **không gian mẫu \((\Omega, \mathbf{F}, P)\)** xác định.

## Điều kiện bất biến hình học (Jaynes, 1973)

### Đề xuất của bạn và Jaynes cùng quan điểm
> “Tất cả các dây có cùng độ dài được xem là một.”  
> ↳ tức là xác suất không phụ thuộc vào vị trí hay hướng, chỉ phụ thuộc vào độ dài.

Đây chính là **nguyên lý bất biến hình học**:
- Phép chọn dây không thay đổi khi ta quay, tịnh tiến, hay phản xạ hệ toạ độ.
- Khi đó, các dây có cùng độ dài tương ứng với *một vòng tròn trung điểm* duy nhất.
- Phân bố trung điểm phải *đều theo diện tích*,  
  nên kết quả \(P = 1/4\) là duy nhất thỏa mãn.

Jaynes gọi đây là *“The Well-Posed Problem”*,  
và xem \(1/4\) là đáp án chính thống, vì chỉ nó giữ được *tính bất biến nhóm (group invariance)*.

## Tổng kết so sánh ba cách

| Cách chọn | Không gian chọn dây | Độ đo sử dụng | Có bất biến hình học? | Xác suất |
|------------|----------------------|----------------|------------------------|-----------|
| C1 | Hai điểm trên đường tròn | Đều theo góc ở tâm | ❌ | 1/3 |
| C2 | Trung điểm trên một bán kính cố định | Đều theo độ dài | ❌ | 1/2 |
| C3 | Trung điểm trong toàn bộ hình tròn | Đều theo diện tích | ✅ | *1/4* |


## Bình luận triết học

- **Laplace**: tin vào tính “đều đặn tuyệt đối” - nhưng Bertrand chứng minh khái niệm này không tự định nghĩa được.  
- **Kolmogorov**: khắc phục bằng cách định nghĩa xác suất như một **độ đo** trên không gian mẫu; tránh mâu thuẫn bằng tính hình thức.  
- **Jaynes**: khôi phục ý nghĩa triết học của Laplace bằng nguyên lý bất biến — một dạng hiện đại của “thờ ơ có lý”.  
- **Van Fraassen**: dùng Bertrand để minh chứng rằng *ngẫu nhiên luôn tương đối với mô hình quan sát* (người chọn không gian quyết định xác suất).  
- **Hájek**: xem Bertrand là một minh họa sống động cho sự khủng hoảng của xác suất cổ điển — lý do Kolmogorov ra đời.


## Tài liệu khuyến nghị đọc

### A. Nguồn gốc lịch sử
- **Joseph Bertrand (1889)**, *Calcul des Probabilités*, §5 — bản gốc của nghịch lý.
- (Có thể xem bản dịch tiếng Anh trong *Sources in the Foundations of Probability*.)

### B. Phân tích toán học và triết học hiện đại
1. **E.T. Jaynes (1973)** - *The Well-Posed Problem*, *Foundations of Physics* 3(4): 477-493.  
   → Bài viết **kinh điển** nhất, trình bày đầy đủ về nguyên lý bất biến hình học.  
   [Tải bản PDF từ arXiv hoặc Springerlink.]

2. **Ian Hacking (1975)** - *The Emergence of Probability*, Ch. 14-15.  
   → Giải thích lịch sử và sụp đổ của Nguyên lý Thờ ơ (Principle of Indifference).

3. **Alan Hájek (2023)** - *Interpretations of Probability*, *Stanford Encyclopedia of Philosophy*, mục 3.1.  
   → Tổng hợp toàn cảnh triết học về xác suất cổ điển và Bertrand’s paradox.

4. **M. van Fraassen (1989)** - *Laws and Symmetry*, Ch. 10.  
   → Diễn giải triết học hiện đại: “ngẫu nhiên là tương đối với cách biểu diễn”.

5. **A.N. Kolmogorov (1933)** - *Foundations of the Theory of Probability*, Ch. 1-2.  
   → Cột mốc đặt nền móng lý thuyết độ đo xác suất.

6. **Patrick Suppes (1957)** - *Introduction to Logic and Probability*, §13.4.  
   → Giải thích bài toán Bertrand kèm minh họa, trình bày vừa phải, dễ đọc.


## Lời dẫn cho lần gặp tới

> 🧭 *Khi quay lại chủ đề này, hãy mở rộng từ “ngẫu nhiên hình học” sang “ngẫu nhiên trong thế giới vật lý thực” — để xem cách quan điểm tần suất (frequentist) và khuynh hướng (propensity) đối thoại với nguyên lý bất biến.*  
>  
> Đoạn mở đầu kế tiếp nên là mục *3.2 Logical / Evidential Probability* trong Hájek (SEP), hoặc phần “Jaynes and the Principle of Maximum Entropy”.

*Bản ghi chú biên soạn bởi ChatGPT (GPT-5) cùng ZO Math,  
cho chuyên đề “Đi tìm Xác suất”.*  
*Lần cập nhật: {{ngày hiện tại}}.*


---

# Nghịch lý Bertrand  
### *(Bertrand’s Paradox)*  

Bản ghi chú học thuật - Dự án *Đi tìm Xác suất*, thuộc ZO Math  


## 1. Bản chất của nghịch lý


### 1.1. Đề bài

> Xét một đường tròn bán kính \(R\). Chọn ngẫu nhiên một dây cung trong đường tròn đó. Hỏi: xác suất để dây cung dài hơn cạnh của tam giác đều nội tiếp là bao nhiêu?

Cạnh của tam giác đều nội tiếp có độ dài \(s = R\sqrt{3}\). 

Ta mong chờ một đáp án duy nhất, nhưng thực tế có ba kết quả khác nhau tùy theo cách hiểu “chọn ngẫu nhiên”:

\[
P_1 = \frac{1}{3}, \quad P_2 = \frac{1}{2}, \quad P_3 = \frac{1}{4}.
\]

Điều này tạo thành nghịch lý do Joseph Bertrand nêu ra năm 1889 trong *Calcul des Probabilités* (§5).


## 2. Mô tả ba cách chọn và ba kết quả

| Cách chọn | Mô tả phép chọn | Đại lượng được xem là "chia đều" | Kết quả |
|------------|-----------------|----------------------------------|----------|
| (1) | Chọn hai điểm độc lập, đều ngẫu nhiên trên đường tròn. | Góc ở tâm giữa hai điểm | \(P_1 = 1/3\) |
| (2) | Chọn một bán kính bất kỳ, rồi chọn trung điểm của dây trên bán kính ấy đều theo độ dài. | Độ dài dọc bán kính | \(P_2 = 1/2\) |
| (3) | Chọn trung điểm của dây đều trong toàn bộ diện tích hình tròn, rồi dựng dây vuông góc với bán kính qua đó. | Diện tích (độ đo hai chiều) | \(P_3 = 1/4\) |

### 2.1. Biểu thức độ dài dây
Mỗi dây được xác định bởi khoảng cách \(r\) từ tâm đến trung điểm:
\[
L = 2\sqrt{R^2 - r^2}.
\]
Khi \(r = 0\), dây là đường kính, có \(L = 2R\).  
Khi \(r = R\), dây suy biến thành điểm.

### 2.2. Điều kiện dây dài hơn cạnh tam giác đều
\[
L > R\sqrt{3} \quad \Longleftrightarrow \quad r < \frac{R}{2}.
\]

Vấn đề là: “trung điểm \(r\)” được chọn theo quy tắc nào?


## 3. Phân tích từng cách chọn


### 3.1. Cách 1 - Chia đều theo góc ở tâm

Cố định một đầu dây tại một điểm của đường tròn, rồi chọn đầu kia sao cho góc ở tâm \(\theta\) phân bố đều trong \([0, \pi]\). Dây dài hơn cạnh tam giác đều khi \(\theta > 120^\circ = 2\pi/3\). Vì \(\theta\) phân bố đều, ta có:
\[
P_1 = \frac{\pi - 2\pi/3}{\pi} = \frac{1}{3}.
\]

Cách này phản ánh trực giác “mỗi cặp điểm trên đường tròn đều có khả năng bằng nhau”.


### 3.2. Cách 2 - Chia đều theo độ dài dọc bán kính

Chọn một bán kính bất kỳ, rồi chọn trung điểm của dây trên bán kính đó đều trong đoạn \([0,R]\). Vì dây dài hơn cạnh khi \(r < R/2\), ta có:
\[
P_2 = \frac{R/2}{R} = \frac{1}{2}.
\]

Tuy nhiên, cách này không thật sự bao quát toàn bộ không gian các dây. Ta đã ngầm giả định mọi dây đều *vuông góc với cùng một hướng bán kính*, tức là ta chỉ xét một họ dây song song, không phải toàn bộ các dây có thể có. Do đó, \(P_2\) phản ánh một loại “đều đặn một chiều”, không phải “đều trong không gian hai chiều”.


### 3.3. Cách 3 - Chia đều theo diện tích (độ đo hai chiều)

Chọn trung điểm của dây đều trong toàn bộ hình tròn, tức là mọi điểm trong đĩa có khả năng như nhau. Khi đó, xác suất để trung điểm nằm trong bán kính \(x\) là:
\[
P(r < x) = \frac{\pi x^2}{\pi R^2} = \left(\frac{x}{R}\right)^2.
\]
Với điều kiện \(r < R/2\), ta được:
\[
P_3 = \left(\frac{1}{2}\right)^2 = \frac{1}{4}.
\]

Đây là kết quả duy nhất tương thích với *đối xứng hình học của đường tròn*: nó không thay đổi khi ta quay, tịnh tiến hay phản xạ hệ tọa độ.


## 4. Bình luận hình học và triết học


### 4.1. Nguồn gốc của nghịch lý

Nguyên lý thờ ơ của Laplace phát biểu rằng:

> Khi không có lý do để ưu tiên khả năng nào, ta nên gán cho chúng xác suất bằng nhau.

Trong bài toán Bertrand, câu “chọn ngẫu nhiên một dây cung” không chỉ ra rõ  
“xác suất bằng nhau” được hiểu theo đại lượng nào: theo góc, theo độ dài, hay theo diện tích.  
Vì vậy, nguyên lý của Laplace trở nên mâu thuẫn với chính nó:  
kết quả thay đổi tùy cách định nghĩa “ngẫu nhiên”.


### 4.2. Hệ quả triết học

Nghịch lý này cho thấy:
1. “Ngẫu nhiên” không phải là một tính chất tuyệt đối của thế giới vật lý,  
   mà phụ thuộc vào cấu trúc mô tả mà ta áp đặt lên nó.  
2. Muốn phát biểu một xác suất có nghĩa, ta phải chỉ rõ **không gian mẫu** và **độ đo xác suất** đi kèm.  
   Đây chính là tư tưởng được Kolmogorov (1933) hoàn thiện trong *Foundations of the Theory of Probability*.


## 5. Điều kiện bất biến hình học

Một cách khắc phục tự nhiên - cũng chính là đề xuất mà bạn nêu ra - là yêu cầu:

> Mọi dây có cùng độ dài phải được xem là tương đương.

Nói cách khác, xác suất chỉ phụ thuộc vào độ dài của dây,  
và phép chọn phải bất biến đối với mọi phép quay, tịnh tiến và phản xạ.

Với yêu cầu này, các dây có cùng độ dài tương ứng với một vòng tròn trung điểm duy nhất có bán kính \(r\), và mật độ xác suất phải tỉ lệ với diện tích, tức là phân bố đều trong toàn bộ đĩa. Khi đó kết quả \(P = 1/4\) là duy nhất thỏa mãn điều kiện bất biến hình học.

E.T. Jaynes (1973) gọi đây là *The Well-Posed Problem*: một bài toán xác suất chỉ được xem là “có nghĩa” khi quy tắc chọn thoả mãn tính bất biến nhóm (group invariance). Theo Jaynes, đó cũng là tinh thần hiện đại hóa của nguyên lý thờ ơ: không chia đều một cách mù quáng, mà chia đều trên những biến giữ nguyên dưới các phép đối xứng cơ bản của hệ.


## 6. Tóm tắt so sánh

| Cách chọn | Không gian chọn dây | Quy tắc “đều” | Tôn trọng đối xứng hình học | Xác suất |
|------------|---------------------|----------------|-----------------------------|----------|
| 1 | Hai điểm trên đường tròn | Đều theo góc ở tâm | Không | 1/3 |
| 2 | Trung điểm trên một bán kính cố định | Đều theo độ dài | Không | 1/2 |
| 3 | Trung điểm trong toàn bộ đĩa | Đều theo diện tích | Có | 1/4 |


## 7. Ý nghĩa trong lịch sử và triết học xác suất

1. **Laplace** tin rằng mọi khả năng có thể được gán xác suất bằng nhau nếu ta không có thông tin gì thêm. Bertrand chỉ ra rằng khái niệm “chia đều” không có nghĩa trừ khi ta chỉ rõ đại lượng được chia.

2. **Kolmogorov** giải quyết triệt để bằng cách đưa ra khái niệm *không gian xác suất* \((\Omega, \mathbf{F}, P)\), trong đó \(P\) là một độ đo xác suất xác định trên tập các biến cố. Nhờ vậy, mọi bài toán xác suất đều gắn với một cấu trúc độ đo rõ ràng, tránh được mâu thuẫn kiểu Bertrand.

3. **Jaynes** phục hồi tinh thần của Laplace bằng cách đưa vào điều kiện bất biến hình học, làm cho nguyên lý thờ ơ trở thành một nguyên lý vật lý - logic chặt chẽ.

4. **Van Fraassen** xem Bertrand’s paradox là minh chứng rằng mọi phát biểu về xác suất đều mang tính tương đối với cách mô hình hóa; không thể nói tới “xác suất khách quan” nếu chưa nói tới hệ quy chiếu mô tả.

5. **Hájek** trong bài *Interpretations of Probability* (Stanford Encyclopedia of Philosophy), xem đây là ví dụ kinh điển cho sự giới hạn của xác suất cổ điển và là động lực trực tiếp dẫn đến xác suất hình thức của Kolmogorov.


## 8. Tài liệu khuyến nghị đọc

### 8.1. Nguồn gốc lịch sử
- **Joseph Bertrand (1889)**, *Calcul des Probabilités*, §5. Nguồn gốc trực tiếp của nghịch lý; bản tiếng Anh trích trong *Sources in the Foundations of Probability*.

### 8.2. Phân tích toán học và triết học hiện đại
1. **E.T. Jaynes (1973)**, *The Well-Posed Problem*, *Foundations of Physics* 3(4): 477-493. Giải thích chi tiết ba cách chọn, đề xuất điều kiện bất biến hình học, và xem kết quả \(1/4\) là duy nhất hợp lý. Bài viết quan trọng nhất về Bertrand’s paradox sau thế kỷ XIX.

2. **Ian Hacking (1975)**, *The Emergence of Probability*, chương 14-15. Trình bày lịch sử hình thành và sụp đổ của Nguyên lý Thờ ơ.

3. **Alan Hájek (2023)**, *Interpretations of Probability*, *Stanford Encyclopedia of Philosophy*, mục 3.1. Tổng hợp toàn cảnh triết học xác suất cổ điển, trong đó Bertrand’s paradox là ví dụ trung tâm.

4. **M. van Fraassen (1989)**, *Laws and Symmetry*, chương 10. Triết học hiện đại: ngẫu nhiên là tương đối với mô hình quan sát.

5. **A.N. Kolmogorov (1933)**, *Foundations of the Theory of Probability*, chương 1-2. Đặt nền tảng cho xác suất hiện đại trên cơ sở lý thuyết độ đo.

6. **Patrick Suppes (1957)**, *Introduction to Logic and Probability*, §13.4. Giải thích ba phép chọn và ba kết quả bằng ngôn ngữ trực quan, dễ tiếp cận.

## 9. Gợi ý nghiên cứu tiếp

Lần sau, khi quay lại chủ đề này, nên mở rộng sang hai hướng:

1. **Liên hệ với xác suất tần suất (frequentist)**: Khi các sự kiện lặp lại vô hạn, khái niệm “ngẫu nhiên hình học” được thay thế bởi “ngẫu nhiên thống kê” như thế nào?

2. **Liên hệ với xác suất khuynh hướng (propensity)**: Liệu “ngẫu nhiên vật lý” có thể có tính khách quan hơn so với ngẫu nhiên hình học?

Những chủ đề này sẽ xuất hiện trong các mục 3.3 và 3.4 của bài *Interpretations of Probability* (Hájek, SEP).


*Bản ghi chú biên soạn bởi ChatGPT (GPT-5) cùng ZO Math  
cho dự án “Đi tìm Xác suất”.*  
*Cập nhật: 11/11/2025.*

