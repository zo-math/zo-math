Ví dụ 10 (Example 10: Patterns, Plane and Symbol - _Focus in High School Mathematics: Reasoning and Sense Making (2009)_, page 42) là một minh họa rất giàu ý nghĩa cho _Using Multiple Representations of Functions_, nhưng để thấy rõ giá trị của nó, cần nhìn lại cấu trúc logic của ví dụ theo một trật tự chặt chẽ hơn.

Thực chất, bốn “phương pháp” trong ví dụ này không phải là bốn con đường hoàn toàn độc lập, mà là bốn cách khác nhau để đi từ _một nền dữ liệu chung_ đến _một biểu diễn ký hiệu của cùng một hàm số_.

---

## 1. Bảng dữ liệu là điểm xuất phát chung

Bước nền tảng (dù được nêu hay không) của mọi phương pháp là:

- xuất phát từ tình huống hình học: các đường thẳng không song song, không đồng quy,
- đếm số miền tương ứng với một vài giá trị của \(L\),
- lập bảng các cặp \((L,R)\).

Chính bảng này cung cấp:

- dữ liệu thực nghiệm,
- trực giác ban đầu về mối quan hệ giữa \(L\) và \(R\),
- cơ sở cho mọi hình thức lập luận tiếp theo.

Nếu không có bảng (hoặc một cơ chế sinh dữ liệu tương đương), thì không phương pháp nào trong bốn phương pháp có thể triển khai.

## 2. Phương pháp 1: Từ bảng đến truy hồi

Quan sát các hiệu giữa những giá trị liên tiếp của \(R\), học sinh nhận ra rằng:

- khi \(L\) tăng thêm 1,
- số miền tăng thêm đúng \(L\).

Điều này dẫn đến mô tả hàm số dưới dạng _truy hồi_:
\[
R(1)=2,\qquad R(L)=R(L-1)+L.
\]

Ở mức độ này, truy hồi vẫn mang tính _mô tả theo dữ liệu_.  
Để truy hồi trở thành một kết quả toán học đúng với mọi \(L\), cần một lập luận hình học tổng quát (xem Mục 6).

## 3. Phương pháp 2: Từ bảng đến _mô hình đếm hình học_

Phương pháp 2 không đếm miền trực tiếp, mà mô hình hóa _quy luật tăng của số miền_, từ đó rút ra được công thức tính số miền.

Ý tưởng cốt lõi là:

- mỗi bước tăng \(L\) làm \(R\) tăng thêm \(L\),
- do đó \(R\) được xây dựng từ tổng
  \[
  1+1+2+3+\cdots+L.
  \]

Mô hình bằng các vật thể (quân cờ, đồng xu, viên gạch) giúp:

- trực quan hóa tổng \(1+2+\cdots+L\),
- nhận ra cấu trúc tam giác,
- từ đó suy ra công thức
  \[
  R = 1 + \frac{L(L+1)}{2}.
  \]

Phương pháp này đóng vai trò _biện minh cấu trúc_ cho công thức, nhưng chỉ thực sự chặt chẽ khi được nối lại với bài toán hình học ban đầu.

## 4. Phương pháp 3: Từ bảng đến _hồi quy_ (regression)

Ở phương pháp này, học sinh:

- nhập các cặp \((L,R)\) bằng một CAS,
- quan sát đồ thị phân tán,
- phỏng đoán dạng bậc hai,
- dùng _hồi quy bậc hai_ để tìm hàm gần đúng
  \[
  R = 0.5L^2 + 0.5L + 1.
  \]

Điểm quan trọng cần nhấn mạnh:

- hồi quy _không phải là chứng minh_,
- nó chỉ cho thấy một công thức _phù hợp dữ liệu đã cho_.

Phương pháp này có giá trị trong:

- khám phá,
- hình thành phỏng đoán,
- kiểm tra chéo với các cách lập luận khác.

## 5. Phương pháp 4: Giả sử dạng công thức và tìm hệ số

Ở phương pháp này, học sinh:

- giả sử trước dạng \(R=aL^2+bL+c\),
- dùng ba cặp dữ liệu từ bảng để lập hệ,
- giải hệ tìm \(a,b,c\).

Cách này:

- đòi hỏi kỹ năng đại số cao hơn,
- cho một đa thức bậc hai khớp dữ liệu,
- nhưng _chưa tự nó đảm bảo_ công thức đúng với mọi \(L\).

Giá trị của phương pháp này nằm ở việc:

- kết nối bảng dữ liệu với cấu trúc đại số,
- rèn luyện thao tác suy luận ký hiệu.

## 6. Mảnh ghép logic then chốt: lập luận hình học tổng quát

Để toàn bộ ví dụ trở nên chặt chẽ về mặt toán học, cần bổ sung một lập luận sau:

Trong điều kiện không có hai đường song song và không có ba đường đồng quy, khi thêm đường thẳng thứ \(L\):

- đường này cắt \(L-1\) đường trước tại \(L-1\) điểm phân biệt,
- do đó bị chia thành \(L\) đoạn,
- mỗi đoạn đi qua một miền cũ và chia miền đó thành hai.

Vì vậy, số miền tăng thêm đúng \(L\), và
\[
R(L)=R(L-1)+L,\qquad R(0)=1.
\]

Từ truy hồi này suy ra:
\[
R(L)=1+\sum\_{k=1}^L k=1+\frac{L(L+1)}{2}.
\]

Lập luận này là _cơ sở chứng minh_ làm cho mọi biểu diễn khác trở nên nhất quán.

## 7. Phân biệt: truy hồi và hồi quy

Hai thuật ngữ này dễ gây nhầm lẫn nhưng bản chất hoàn toàn khác nhau:

- _Truy hồi (recursion)_:

  - mô tả giá trị sau dựa trên giá trị trước,
  - là một cách _định nghĩa hàm số chính xác_,
  - khi có lập luận nền, truy hồi mang tính suy diễn.

- _Hồi quy (regression)_:
  - là kỹ thuật thống kê-số học,
  - tìm hàm _xấp xỉ tốt nhất_ cho dữ liệu,
  - không phải là chứng minh toán học.

> **Hồi quy** là một phương pháp dùng dữ liệu để tìm _một công thức xấp xỉ_ mô tả mối quan hệ giữa các đại lượng.
> Ta _chọn trước dạng công thức_ (chẳng hạn \(y=ax+b\) hoặc \(y=ax^2+bx+c\)).
> Dựa trên các cặp dữ liệu \((x,y)\), máy tính tìm các hệ số sao cho công thức đó _phù hợp dữ liệu nhất_.
> Hồi quy _không cho công thức đúng tuyệt đối_, mà cho công thức _khớp tốt với dữ liệu đã có_.
> Vì vậy, hồi quy dùng để _khám phá và kiểm tra phỏng đoán_, không dùng để chứng minh.

Trong Ví dụ 10:

- truy hồi là một phần của lập luận toán học,
- hồi quy là công cụ khám phá và kiểm tra.

Việc phân biệt rõ hai khái niệm này giúp học sinh không nhầm lẫn giữa _“đúng vì cấu trúc toán học”_ và _“đúng vì khớp dữ liệu”_.

## 8. Thông điệp trung tâm của Ví dụ 10

Ví dụ 10 không nhằm trình bày bốn lời giải độc lập, mà nhằm cho thấy:

- cùng một mối quan hệ hàm số,
- có thể được tiếp cận qua nhiều biểu diễn khác nhau,
- mỗi biểu diễn làm lộ một khía cạnh của cấu trúc,
- và khi các biểu diễn cùng hội tụ, hiểu biết của học sinh trở nên sâu và vững hơn.

Đây chính là tinh thần cốt lõi của _Reasoning with Functions_: không tách rời dữ liệu, hình học, đại số và công nghệ, mà dùng chúng để soi sáng lẫn nhau.
