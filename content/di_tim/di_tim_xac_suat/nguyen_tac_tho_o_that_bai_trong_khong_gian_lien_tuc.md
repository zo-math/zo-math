# Ghi chú: Vì sao nguyên tắc thờ ơ thất bại trong không gian liên tục?

## 1. Bối cảnh: nguyên tắc thờ ơ muốn làm gì?

*Nguyên tắc thờ ơ (principle of indifference)* phát biểu:

> Nếu không có lý do nào để thiên vị một khả năng hơn các khả năng khác, thì ta phải gán *cùng một xác suất* cho tất cả các khả năng.

Trong không gian rời rạc (ví dụ: tung xúc xắc), nguyên tắc này dẫn đến phép gán “đều” quen thuộc:
\[
P(\text{mỗi mặt}) = \frac{1}{6}.
\]

Trong những ví dụ như vậy, nguyên tắc trông có vẻ hợp lý, nhất quán và “công bằng”.


## 2. Ví dụ hình học: lập phương và ba cách mô tả

Xét một nhà máy sản xuất các khối lập phương sao cho:

- Độ dài cạnh \(L \in [0,1]\) (feet),
- Diện tích một mặt \(A = L^2 \in [0,1]\) (feet vuông),
- Thể tích \(V = L^3 \in [0,1]\) (feet khối).

*Cùng một khối lập phương* có thể được mô tả bằng \(L\), hoặc \(A\), hoặc \(V\).  

Xét biến cố:

> \(E\): “Độ dài cạnh \(L\) của khối lập phương nằm trong khoảng \([0, 1/2]\).”

Vì diện tích một mặt là \(A = L^2\) và thể tích là \(V = L^3\), ta có các tương đương:

- \(E = \{L \le \tfrac{1}{2}\}\),
- \(E = \{A \le \tfrac{1}{4}\}\),
- \(E = \{V \le \tfrac{1}{8}\}\).

Ba cách mô tả này cùng chỉ đến *một và chỉ một* tập khối lập phương trong không gian vật lý.


## 3. Áp dụng nguyên tắc thờ ơ theo ba cách khác nhau

### 3.1. Đều theo cạnh \(L\)

Ta giả sử:

- Không có lý do nào để thiên vị khoảng độ dài này hơn khoảng độ dài kia;
- Do đó, theo nguyên tắc thờ ơ: \(L\) phân bố đều trên \([0,1]\).

Khi đó:
\[
P(L \le \tfrac{1}{2}) = \tfrac{1}{2}.
\]

### 3.2. Đều theo diện tích \(A\)

Ta phát biểu lại bài toán:

> Nhà máy sản xuất các khối lập phương có *diện tích mặt* \(A \in [0,1]\). Không có lý do nào để thiên vị khoảng diện tích này hơn khoảng diện tích kia.

Nguyên tắc thờ ơ (theo đúng tinh thần cũ) lại buộc ta cho:

- \(A\) phân bố đều trên \([0,1]\);
- Mỗi khoảng bằng nhau về chiều dài trên trục \(A\) nhận xác suất như nhau.

Do đó:

- Chia \([0,1]\) thành 4 khoảng \([0,\tfrac{1}{4}], [\tfrac{1}{4},\tfrac{1}{2}], [\tfrac{1}{2},\tfrac{3}{4}], [\tfrac{3}{4},1]\);
- Mỗi khoảng được gán xác suất \(\tfrac{1}{4}\).

Nhưng biến cố \(E\) giờ được mô tả là:
\[
E = \{A \le \tfrac{1}{4}\},
\]
nên:
\[
P(E) = P(A \le \tfrac{1}{4}) = \tfrac{1}{4}.
\]


### 3.3. Đều theo thể tích \(V\)

Tương tự, nếu ta phát biểu lại bài toán theo thể tích:

- \(V\) nằm trong \([0,1]\),
- Nguyên tắc thờ ơ bảo ta cho \(V\) phân bố đều trên \([0,1]\),
- Khi đó biến cố \(E = \{V \le \tfrac{1}{8}\}\) nhận:
\[
P(E) = \tfrac{1}{8}.
\]


## 4. Nghịch lý: cùng một biến cố, ba xác suất khác nhau

Tóm lại, ta có:

- Nếu “đều theo cạnh” \(L\):  
  \[
  P(E) = \tfrac{1}{2}.
  \]
- Nếu “đều theo diện tích” \(A\):  
  \[
  P(E) = \tfrac{1}{4}.
  \]
- Nếu “đều theo thể tích” \(V\):  
  \[
  P(E) = \tfrac{1}{8}.
  \]

Nhưng \(E\) là *cùng một biến cố vật lý*: “khối lập phương có cạnh không vượt quá \(\tfrac{1}{2}\)”. Không thể chấp nhận được việc *cùng một biến cố* lại có *nhiều giá trị xác suất khác nhau* chỉ vì:

- ta diễn đạt nó bằng \(L\) hay \(A\) hay \(V\),
- mà không hề thay đổi nội dung vật lý của nó.

Đây chính là dạng thức của *nghịch lý kiểu Bertrand* trong ví dụ lập phương.


## 5. Điểm yếu cốt lõi của nguyên tắc thờ ơ

Lý do nghịch lý xuất hiện:

1. *Nguyên tắc thờ ơ chỉ nói “chia đều”, nhưng không nói “đều theo cái gì”.*  
   - Đều theo độ dài, đều theo diện tích, đều theo thể tích, đều theo \(L^k\) với mọi \(k \neq 0\),  
   - Tất cả đều là những cách áp dụng “đều” hợp lệ về mặt hình thức.

2. *Trong không gian liên tục, “đều” là khái niệm tương đối với cách tham số hoá và độ đo nền.*  
   - Một phân phối đều trong một tham số (ví dụ: \(L\)) sẽ trở thành *không đều* khi đổi sang tham số khác (ví dụ: \(A=L^2\)).
   - Ngược lại, nếu ta ép đều trong tham số mới, phân phối quay về tham số cũ sẽ không còn đều nữa.

3. *Nguyên tắc thờ ơ không cung cấp tiêu chuẩn khách quan để chọn tham số hoá “đúng”.*  
   - Khi nhìn theo \(L\), nguyên tắc bảo ta “đều theo \(L\)”.  
   - Khi nhìn theo \(A\), nó lại bảo ta “đều theo \(A\)”.  
   - Hai yêu cầu này mâu thuẫn về mặt xác suất gán cho cùng một biến cố.

Kết luận chính xác:

> Trong không gian liên tục, nguyên tắc thờ ơ *không xác định duy nhất* phân phối xác suất, mà cho những chỉ dẫn *không tương thích* nhau tuỳ theo cách mô tả không gian khả năng. Do đó, nó không thể đóng vai trò nền tảng khách quan cho xác suất.


## 6. Ý nghĩa triết học

- Nguyên tắc thờ ơ được đề xuất để thể hiện *tính công bằng của lý trí*: không thiên vị khi không có lý do.
- Nhưng trong không gian liên tục, mỗi lần ta chọn một cách đo (cạnh, diện tích, thể tích), ta đã *ngầm chọn một dạng thiên vị nền* - một độ đo ưu tiên.
- Vì không có nguyên lý nội tại nào bảo ta phải đo theo \(L\) thay vì \(A\), hay \(A\) thay vì \(V\), “công bằng” của thờ ơ không còn là công bằng của thế giới, mà là công bằng của *cách ta mô tả* thế giới.

Có thể tóm tắt trực giác này như sau:

> *Thờ ơ được sinh ra để tránh thiên vị, nhưng trong không gian liên tục, muốn áp dụng thờ ơ ta buộc phải chọn một cách đo - và chính lựa chọn đó lại là một hình thức thiên vị.*

Đây là lý do sâu xa khiến các nhà toán học và triết học phải rời khỏi cách hiểu cổ điển đơn thuần của Laplace, và chuyển sang các tiếp cận dựa trên *độ đo* (Kolmogorov), *tần suất*, hoặc *xác suất chủ quan/bayesian*, nơi “thước đo nền” (cơ chế vật lý, thông tin sẵn có, entropy cực đại, v.v.) được chỉ rõ ngay từ đầu.
