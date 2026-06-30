# Ghi chú: Hiểu đúng bản chất nghịch lý Bertrand và vai trò của tham số hóa

## 1. Sự kiện là một, nhưng mô hình thì nhiều

Sự kiện “khối lập phương có cạnh ≤ 1/2” có thể được mô tả bằng nhiều tham số khác nhau:

- chiều dài cạnh \(L\)
- diện tích mặt \(A = L^2\)
- thể tích \(V = L^3\)
- hoặc \(L^\alpha\) với bất kỳ \(\alpha > 0\)

Tất cả cùng mô tả _một thực thể_, nhưng chúng không tạo ra cùng một cấu trúc đo lường (measure) trên không gian khả năng.

Đây là điểm mấu chốt: thay tham số → thay độ đo → thay xác suất.

## 2. Vấn đề không nằm ở toán học, mà ở “sự đều” mà ta đang ngầm giả định

Khi bạn chọn một khối “đều theo _diện tích_ mặt”, bạn đang lấy mẫu theo một độ đo \(d\mu_A\) mà trong đó:

\[
d\mu_A \propto dA
\]

Còn khi bạn chọn một khối “đều theo _chiều dài_ cạnh”, bạn đang dùng độ đo:

\[
d\mu_L \propto dL
\]

Hai độ đo này _không tương đương_, vì phép biến đổi \(A = L^2\) không tuyến tính:

\[
dA = 2LdL
\]

Điều này làm cho:

- các khoảng đều nhau trong \(A\) _không_ tương ứng với các khoảng đều nhau trong \(L\)
- và ngược lại

Vì vậy “đều theo \(A\)” và “đều theo $L$” là hai cách chọn xác suất _khác nhau_, cho kết quả khác nhau.

Không có mâu thuẫn toán học. Có mâu thuẫn trong _niềm tin sai lầm_ rằng hai cái đó tương đương.

## 3. Nghịch lý xuất hiện vì ta lầm tưởng “đều” là khái niệm bất biến

Trong không gian hữu hạn, Laplace có thể nói: “không phân biệt được trường hợp nào → chia đều”.

Nhưng trong không gian vô hạn (đặc biệt uncountable): _không có khái niệm “đều” duy nhất._

- đều theo $L$
- đều theo $A$
- đều theo $V$
- đều theo \(L^\alpha\)

→ tất cả hợp lý như nhau, không ai thắng ai.

_Bertrand muốn chứng minh rằng nguyên tắc “đồng khả năng” (principle of indifference) là bất khả thi trong không gian vô hạn._

## 4. Không có tham số nào “đúng” tuyệt đối

Trong các hệ vật lý _có_ đối xứng duy nhất (như đồng xu, xúc xắc), thế giới “chọn” cho ta một độ đo.

Nhưng trong ví dụ nhà máy sản xuất khối lập phương:

- thế giới không chỉ ra biến nào là biến gốc
- không có symmetry nào duy nhất để bám vào

→ Không thể nói độ đo nào “thật”, độ đo nào “giả”.

Chỉ có thể nói:

> Độ đo nào phù hợp với cơ chế tạo ra dữ liệu thì độ đo đó đúng trong mô hình của ta.

Nếu không biết cơ chế → không có lời giải duy nhất.

## 5. Công thức \(P(A \le 1/4) = P(L \le 1/2)\) không sai

Công thức này _hoàn toàn đúng_ trong một điều kiện quan trọng:

> Bạn đang dùng cùng một độ đo trên không gian, chỉ thay đổi biến.

Nếu độ đo gốc là theo $L$:

- bạn chuyển sang theo A bằng công thức biến đổi (Jacobian)
- và kết quả nhất quán

Nếu bạn đổi luôn độ đo thành “đều theo A”, thì độ đo mới _không còn tương thích_ với độ đo cũ. Khi đó:

\[
P(L \le 1/2) \neq P(A \le 1/4)
\]

Nghĩa là công thức không sai, mà bạn đã thay đổi bài toán.

## 6. Ý nghĩa triết học rút ra

Nghịch lý Bertrand không chứng minh rằng xác suất mâu thuẫn.
Nó chứng minh rằng:

> Xác suất không phải là thuộc tính tuyệt đối của sự kiện, mà là thuộc tính của mô hình mà ta áp dụng lên sự kiện đó.

Nếu mô hình không được xác định đầy đủ (ví dụ “đều theo cái gì?”),
→ xác suất không xác định.

## 7. Điều mà phần lớn sách giáo khoa không nói ra

Để giải quyết những trường hợp như Bertrand, bạn cần:

### 1. Thông tin về cơ chế vật lý → chọn độ đo vật lý

### 2. Hoặc nguyên tắc entropy tối đa (Jaynes)

### 3. Hoặc đối xứng nhóm (symmetry groups)

### 4. Hoặc quan điểm Bayesian chủ quan

Không có nguyên tắc phổ quát.

## Kết luận then chốt

> Nghịch lý Bertrand không phải là nghịch lý của toán học. Nó là nghịch lý của cách suy nghĩ cổ điển về xác suất - khi ta muốn “đồng khả năng” mà lại không chỉ rõ “đồng theo cái gì”.

---
