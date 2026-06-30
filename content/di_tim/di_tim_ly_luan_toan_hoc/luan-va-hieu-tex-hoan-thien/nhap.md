\NOTE{
\vspace{.5\baselineskip}
Điểm cần chú ý trước hết là bài toán này có một cấu trúc rất đặc biệt: mỗi lần uống, cơ thể được đưa vào một lượng thuốc cố định, $440$ mg; nhưng lượng thuốc bị đào thải sau mỗi chu kì không cố định, vì nó bằng $60\%$ lượng thuốc đang có trong cơ thể. Khi lượng thuốc trong cơ thể còn ít, lượng đào thải cũng ít, nên tổng lượng thuốc sau mỗi liều tăng nhanh. Khi lượng thuốc đã nhiều hơn, lượng đào thải trước liều kế tiếp cũng nhiều hơn, nên phần tăng thêm sau mỗi liều nhỏ dần. Trạng thái ổn định xuất hiện khi lượng đào thải trong một chu kì đúng bằng lượng thuốc được đưa thêm vào:

$$
0.6V=440.
$$

Do đó

$$
V=733\frac{1}{3}\, \text{mg}.
$$

Nói bằng ngôn ngữ chuyển hóa, cơ thể không làm cho thuốc ``biến mất'' hoàn toàn sau mỗi chu kì; nó chỉ giữ lại $40\%$ lượng đang có. Chính sự kết hợp giữa bổ sung cố định và đào thải theo tỉ lệ làm cho lượng thuốc tiến dần tới một mức cân bằng.

Cần lưu ý một lỗi chỉ số trong bản gốc ở Method 2. Bản gốc viết truy hồi dạng $A_{n+1}=0.40A_n+440$ kèm điều kiện đầu $A_1=0$. Nhưng ngay trong bảng số liệu, $A_n$ đã được hiểu là lượng thuốc trong cơ thể ngay sau khi uống $n$ liều. Vì vậy, sau liều thứ nhất phải có

$$
A_1=440,
$$

không thể là $0$. Điều kiện đầu đúng phải là

$$
A_0=0,
$$

nghĩa là trước khi uống liều đầu tiên, trong cơ thể chưa có lượng thuốc này. Khi đó

$$
A_1=0.4A_0+440=440,
$$

khớp với bảng dữ liệu. Nếu giữ $A_1=0$, công thức truy hồi sẽ làm lệch toàn bộ cách đánh số liều và mâu thuẫn với chính định nghĩa của $A_n$ trong bài.

Ví dụ này cho thấy rõ giá trị của một bài toán có thể được quay lại nhiều lần ở những mức độ khác nhau của luận và hiểu. Cùng bối cảnh---thuốc được bổ sung theo chu kì và bị đào thải theo tỉ lệ cố định---có thể trước hết được đọc bằng bảng số liệu và đồ thị rời rạc để làm lộ trực giác về sự ổn định, rồi được mô hình hóa bằng hệ thức truy hồi

$$
A_{n+1}=0.4A_n+440,\, A_0=0.
$$

Sau đó, cùng mô hình ấy có thể được nhìn lại như một bài toán về suy giảm theo hàm mũ, về khái niệm giới hạn, và cuối cùng là về chứng minh hội tụ. Chính cấu trúc nhiều tầng này làm cho ví dụ trở thành trục nối giữa mô hình hóa, hàm số, biểu diễn và suy diễn logic.

Điểm đáng chú ý nhất nằm ở sự khác nhau giữa Phương pháp 3 và Phương pháp 5. Ở Phương pháp 3, trọng tâm được chuyển sang mức tăng

$$
I(n)=A_n-A_{n-1}.
$$

Từ hệ thức truy hồi, ta có

$$
A_{n+1}-A_n=0.4(A_n-A_{n-1}),
$$

nên mỗi mức tăng mới chỉ còn $40\%$ mức tăng trước đó. Vì mức tăng ban đầu là

$$
A_1-A_0=440,
$$

nên

$$
I(n)=440(0.4^{n-1}).
$$

Cách nhìn này hiệu quả vì nó giải thích vì sao lượng thuốc tăng chậm dần: các phần tăng thêm không biến mất ngẫu nhiên, mà giảm theo một quy luật mũ. Từ đó, học sinh có thêm động lực tự nhiên để hiểu cấp số nhân và tổng của cấp số nhân trong một tình huống có nghĩa.

Phương pháp 5 đi xa hơn vì nó xem toàn bộ quá trình dùng thuốc như một phép lặp trạng thái. Ở đây, ta chọn một mốc quan sát cố định: lượng thuốc trong cơ thể ngay sau mỗi liều. Kí hiệu $A_n$ là lượng thuốc trong cơ thể ngay sau liều thứ $n$. Khi đó, từ $A_n$ đến $A_{n+1}$, cơ thể trải qua đúng một chu kì: trong $8$ giờ tiếp theo, cơ thể đào thải $60\%$ lượng thuốc đang có, nên chỉ còn lại $40\%$, tức là $0.4A_n$; sau đó học sinh uống liều kế tiếp, thêm $440$ mg. Vì vậy,

$$
A_{n+1}=0.4A_n+440.
$$

Hàm

$$
C(x)=0.4x+440
$$

được gọi là hàm chuyển tiếp vì nó mô tả đúng một bước chuyển từ trạng thái này sang trạng thái kế tiếp: nếu lượng thuốc ngay sau một liều là $x$, thì lượng thuốc ngay sau liều kế tiếp là $C(x)$. Do đó, toàn bộ dãy lượng thuốc được tạo ra bằng cách lặp đi lặp lại cùng một hàm:

$$
A_{n+1}=C(A_n).
$$

Theo cách nhìn này, giá trị ổn định không còn chỉ là con số được đoán ra từ bảng, mà là một trạng thái không đổi qua phép chuyển tiếp. Nếu ngay sau một liều cơ thể đang có $V$ mg thuốc, và sau một chu kì đào thải rồi uống liều kế tiếp, lượng thuốc lại trở về đúng $V$ mg, thì $V$ phải thỏa

$$
C(V)=V.
$$

Nói cách khác,

$$
0.4V+440=V.
$$

Giải ra được

$$
V=733\frac{1}{3}\, \text{mg}.
$$

Đây là ý nghĩa của điểm bất động: đó là mức thuốc mà phép chuyển tiếp $C$ giữ nguyên. Nếu cơ thể đang ở đúng mức ấy ngay sau một liều, thì sau khi đào thải $60\%$ trong $8$ giờ và uống thêm $440$ mg, lượng thuốc lại trở về đúng mức ấy. Về mặt chuyển hóa, điều này tương đương với việc lượng thuốc bị đào thải trong một chu kì đúng bằng lượng thuốc được đưa thêm vào.

Tuy nhiên, tìm được điểm bất động mới cho biết mức cân bằng là bao nhiêu; điều còn cần chứng minh là dãy $A_n$ có thật sự tiến tới mức cân bằng ấy hay không. Vì vậy, Phương pháp 5 xét độ lệch giữa lượng thuốc thực tế và mức cân bằng:

$$
D_n=A_n-V.
$$

Từ

$$
A_{n+1}=0.4A_n+440
$$

và

$$
V=0.4V+440,
$$

lấy hai đẳng thức trừ nhau, ta được

$$
A_{n+1}-V=0.4(A_n-V).
$$

Tức là

$$
D_{n+1}=0.4D_n.
$$

Do đó, sau mỗi chu kì, độ lệch so với mức cân bằng chỉ còn $40\%$ độ lệch trước đó; nói theo khoảng cách,

$$
\lvert D_{n+1}\rvert=0.4\lvert D_n\rvert.
$$

Vì $0.4<1$, các độ lệch này nhỏ dần về $0$. Đây là phần chứng minh hội tụ: lượng thuốc không chỉ có vẻ ổn định qua bảng số liệu, mà buộc phải tiến dần tới $733\frac{1}{3}$ mg do chính cấu trúc của phép lặp. Ở đây, ``ổn định'' không còn là quan sát số học từ bảng, mà trở thành hệ quả tất yếu của hàm chuyển tiếp $C$.

Giá trị sư phạm của ví dụ vì thế không nằm riêng ở lời giải cho bài toán, mà ở cách nó cho phép cùng một tình huống nâng đỡ nhiều mức học khác nhau. Người mới học có thể bắt đầu từ bảng và đồ thị; học sinh khá hơn có thể nhận ra hệ thức truy hồi và cấu trúc mũ; học sinh đã vững vàng hơn có thể dùng điểm bất động và độ lệch để giải thích vì sao hội tụ xảy ra. Nhờ đó, ví dụ minh họa đúng tinh thần của sách: hiểu không tách rời luận, và cùng một bối cảnh tốt có thể đưa người học từ trực giác định lượng đến biện giải chặt chẽ.
}
