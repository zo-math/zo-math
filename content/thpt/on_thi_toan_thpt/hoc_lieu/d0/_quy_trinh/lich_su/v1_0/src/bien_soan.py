from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
items=[]
def add(r,n,title,objective,prereq,clusters,support,ct,source,level,capacity,fmt,minutes,question,answer,solution,criteria,error,repair,retest,reanswer,resolution,check):
 items.append(dict(id=f'D0-R{r}-{n:02}',version=r'1.0',r=f'R{r}',n=n,title=title,objective=objective,prereq=prereq,clusters=clusters,support=support,ct=ct,source=source,level=level,capacity=capacity,format=fmt,minutes=minutes,question=question,answer=answer,solution=solution,criteria=criteria,error=error,repair=repair,retest_id=f'D0-R{r}-SL{n:02}',retest=retest,reanswer=reanswer,resolution=resolution,check=check,family=f'HO-D0-R{r}-{n:02}',history=r'Câu mới trong gói D0 v1.0; chưa có dữ liệu lịch sử tiếp xúc của từng học sinh. Phải hỏi và ghi trước khi giao.',author=r'ZO Math biên soạn; ChatGPT hỗ trợ soạn và kiểm tra; chưa có xác nhận người chủ trì duyệt.',scope=r'Chương trình chung; N là nền hỗ trợ, không là mạch thứ chín.'))
add(1,1,r'Điều kiện xác định',
r'Kết hợp điều kiện căn thức và mẫu số; giữ điểm biên được phép.',
r'Lớp 10: tập xác định; nền THCS về căn bậc hai và phân thức.',
r'B04; N: B01–B02',r'N',r'80',r'S10.2 Bài 15, tr.in 6 / PDF 7.',
r'Nhận diện/điều kiện: phối hợp hai điều kiện trực tiếp.',r'Tư duy và lập luận; giao tiếp toán học',r'Một lựa chọn + giải thích',3,
r'''Cho $f(x)=\frac{\sqrt{x+2}}{x-1}$. Chọn **một** tập xác định đúng và viết hai điều kiện mà em đã dùng.

A. $[-2;+\infty)$.

B. $(-2;1)\cup(1;+\infty)$.

C. $[-2;1)\cup(1;+\infty)$.

D. $\mathbb{R}\setminus\{1\}$.''',
r'C; $D=[-2;1)\cup(1;+\infty)$.',
r'''Căn thức có nghĩa khi $x+2\geq0$; mẫu số khác không khi $x\ne1$. Kết hợp hai điều kiện được $x\geq-2$, $x\ne1$, tức phương án C. Tại $x=-2$, tử số bằng 0 và mẫu số bằng $-3$, nên phải giữ điểm này.

A còn chứa 1; B loại nhầm $-2$; D còn chứa các số nhỏ hơn $-2$. Do đó chỉ C đúng.''',
[r'Chọn C.',r'Nêu cả điều kiện $x\geq-2$ và $x\ne1$; giữ được $-2$.'],
r'ĐK: bỏ mẫu khác 0; KN: hiểu nhầm căn phải dương; ĐỌC: nhầm dấu ngoặc.',
r'Viết riêng điều kiện của từng bộ phận, lấy giao rồi thử điểm biên. Ôn S10.2 tr.6 và nền B02; sau đó vào R1-G01 khi gói được tạo, hàng B.1 tuần 2–4.',
r'Cho $g(x)=\frac{\sqrt{5-x}}{x+1}$. Tìm tập xác định; giải thích có nhận $x=5$ và $x=-1$ hay không.',
r'$(-\infty;-1)\cup(-1;5]$.',
r'Cần $5-x\geq0$ và $x+1\ne0$, nên $x\leq5$, $x\ne-1$. Nhận 5 vì tử bằng 0, mẫu bằng 6; loại $-1$ vì mẫu bằng 0.',
r'Kiểm riêng hai điều kiện, thế các điểm biên; đối chiếu miền bằng bất đẳng thức chính xác.')
add(1,2,r'Đạo hàm và tiếp tuyến',
r'Tính đạo hàm và dùng đồng thời điểm tiếp xúc, hệ số góc.',
r'Lớp 11: quy tắc đạo hàm và phương trình tiếp tuyến.',
r'B16–B17; N: B02',r'N',r'95–96',r'S11.2 Bài 31, tr.in 84 / PDF 85; Bài 32, tr.in 89 / PDF 90.',
r'Thực hiện: áp dụng quy tắc và ghép điểm với hệ số góc.',r'Giải quyết vấn đề; giao tiếp toán học',r'Trả lời ngắn + bước tính',4,
r'Cho $f(x)=x^3-3x$. Tính $f^\prime(1)$ và viết phương trình tiếp tuyến của đồ thị tại điểm có hoành độ 1. Ghi rõ tọa độ tiếp điểm.',
r'$f^\prime(1)=0$; tiếp điểm $(1;-2)$; tiếp tuyến $y=-2$.',
r'$f^\prime(x)=3x^2-3$, nên $f^\prime(1)=0$. Vì $f(1)=-2$, tiếp điểm là $(1;-2)$. Phương trình tiếp tuyến là $y=f^\prime(1)(x-1)+f(1)=-2$. Hệ số góc 0 cho tiếp tuyến ngang, không có nghĩa tiếp tuyến là trục hoành.',
[r'Tính đúng đạo hàm và giá trị $f^\prime(1)=0$.',r'Ghi đúng tiếp điểm và tiếp tuyến $y=-2$.'],
r'TÍNH: sai đạo hàm; KN: đồng nhất tung độ với hệ số góc.',
r'Ôn ý nghĩa hình học tại S11.2 tr.84, quy tắc tr.89; xác định điểm trước, hệ số góc sau. Hàng B.1 tuần 2–4.',
r'Cho $g(x)=x^2+2x$. Tính $g^\prime(1)$ rồi lập tiếp tuyến tại hoành độ 1; ghi tiếp điểm.',
r'$g^\prime(1)=4$; $(1;3)$; $y=4x-1$.',
r'$g^\prime(x)=2x+2$, $g^\prime(1)=4$, $g(1)=3$. Tiếp tuyến $y=4(x-1)+3=4x-1$; thế $x=1$ được đúng tung độ 3.',
r'Lấy đạo hàm biểu thức; kiểm đường thẳng đi qua tiếp điểm và có đúng hệ số góc.')
add(1,3,r'Đọc dấu đạo hàm',
r'Phân biệt nghiệm của đạo hàm và cực trị; nối bảng dấu với chiều biến thiên.',
r'Lớp 12: đơn điệu và cực trị bằng dấu đạo hàm.',
r'B18; N: B01, B06',r'N',r'105–106',r'S12.1 Bài 1, tr.in 7, 10 / PDF 9, 12.',
r'Giải thích/phối hợp: suy luận từ bảng dấu và phản bác kết luận thiếu điều kiện.',r'Tư duy và lập luận; giao tiếp toán học',r'Đúng/sai 4 ý + giải thích',5,
r'''Hàm số $f$ có đạo hàm trên $\mathbb{R}$ với bảng dấu sau:

| $x$ | $(-\infty;-2)$ | $-2$ | $(-2;1)$ | $1$ | $(1;+\infty)$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| $f^\prime(x)$ | $-$ | $0$ | $+$ | $0$ | $+$ |

Xét đúng/sai từng khẳng định và giải thích ngắn từ bảng dấu:

a) $f$ đạt cực tiểu tại $x=-2$.

b) $f$ đạt cực đại tại $x=1$.

c) $f$ đồng biến trên $(-2;+\infty)$.

d) $f(-3)<f(-2)$.''',
r'a) Đúng; b) Sai; c) Đúng; d) Sai.',
r'''a) Đúng: đạo hàm đổi dấu từ âm sang dương khi qua $-2$, nên hàm đổi chiều từ giảm sang tăng.

b) Sai: tại 1 đạo hàm bằng 0 nhưng không đổi dấu; hàm vẫn tăng khi đi qua 1, nên không có cực đại.

c) Đúng: đạo hàm dương trên $(-2;1)$ và $(1;+\infty)$, chỉ bằng 0 tại 1. Hàm có đạo hàm nên liên tục tại 1; việc đạo hàm bằng 0 tại một điểm không phá vỡ tính đồng biến trên toàn khoảng.

d) Sai: hàm giảm từ $-3$ đến $-2$, nên $f(-3)>f(-2)$. Không cần biết giá trị cụ thể của $f$.''',
[r'Lưu riêng Đ/S của a, b, c, d.',r'Giải thích bằng đổi dấu ở a, không đổi dấu ở b, tính tăng qua điểm 1 ở c, thứ tự giá trị ở d.'],
r'KN/ĐK: xem mọi nghiệm đạo hàm là cực trị; ĐỌC: đọc nhầm dấu hoặc đảo thứ tự giá trị.',
r'Ôn S12.1 tr.7 và tr.10, vẽ mũi tên tăng/giảm dưới từng khoảng. Hàng B.1 tuần 2–4; không kết luận đã vững R1 từ câu này.',
r'''Hàm $g$ có đạo hàm trên $\mathbb{R}$; $g^\prime>0$ khi $x<0$, $g^\prime<0$ khi $0<x<2$ và khi $x>2$; $g^\prime(0)=g^\prime(2)=0$. Xét đúng/sai và giải thích:

a) $g$ có cực đại tại 0. b) $g$ có cực tiểu tại 2.

c) $g$ nghịch biến trên $(0;+\infty)$. d) $g(1)<g(2)$.''',
r'Đúng; Sai; Đúng; Sai.',
r'Tại 0 dấu đổi từ dương sang âm nên có cực đại. Tại 2 dấu âm ở hai phía nên không có cực tiểu. Hàm giảm trên $(0;+\infty)$ dù đạo hàm bằng 0 tại một điểm. Vì $1<2$, ta có $g(1)>g(2)$.',
r'Kiểm tính khả thi của bảng bằng đạo hàm mẫu $(x+2)(x-1)^2$; câu thử lại dùng $-x(x-2)^2$. Kiểm dấu từng khoảng và lập luận đơn điệu, không dùng vài điểm thay chứng minh.')
add(2,1,r'Thước đo phù hợp',
r'Nhận ra ảnh hưởng của giá trị lớn bất thường đến số trung bình.',
r'Lớp 10: số trung bình, trung vị của mẫu không ghép nhóm.',
r'B36; N: B02',r'N',r'85',r'S10.1 Bài 13, tr.in 78–79 / PDF 79–80.',
r'Nhận diện: nhận biết thước đo ít bị kéo lệch trong mẫu cụ thể.',r'Tư duy và lập luận; giao tiếp toán học',r'Trả lời ngắn + giải thích',4,
r'Năm lần chờ xe có thời gian (phút): $4;5;5;6;30$. Tính số trung bình và trung vị. Nếu muốn mô tả thời gian chờ điển hình của phần lớn năm lần này, em chọn số nào trong hai số ấy? Giải thích dựa vào dữ liệu.',
r'Trung bình 10 phút; trung vị 5 phút; chọn trung vị cho mục đích nêu trong đề.',
r'Tổng bằng 50 nên số trung bình là $50/5=10$ phút. Dữ liệu đã sắp tăng, giá trị thứ ba là 5 nên trung vị bằng 5 phút. Bốn trong năm lần chờ nằm trong khoảng 4–6 phút; lần 30 phút kéo trung bình lên. Trung vị 5 phút phù hợp hơn với mục đích mô tả phần lớn các lần này. Điều đó không có nghĩa số trung bình sai hoặc phải xóa lần chờ 30 phút.',
[r'Tính đúng cả hai số và đơn vị.',r'Chọn trung vị với lý do gắn với bốn lần chờ 4–6 phút; không tự loại số liệu 30.'],
r'KN: xem số trung bình luôn đại diện tốt; TÍNH: không sắp xếp khi tìm trung vị.',
r'Ôn S10.1 tr.78–79; nói rõ câu hỏi thực tiễn trước khi chọn thước đo. Hàng B.2 tuần 5.',
r'Năm lần chờ có thời gian (phút): $3;4;4;5;24$. Tính trung bình, trung vị và chọn số mô tả thời gian chờ điển hình của phần lớn các lần này, kèm lý do.',
r'Trung bình 8 phút; trung vị 4 phút; chọn trung vị.',
r'Tổng là 40, trung bình $40/5=8$ phút; giá trị giữa là 4. Bốn giá trị nằm từ 3 đến 5 phút, còn 24 kéo trung bình lên nên trung vị phù hợp mục đích đã nêu.',
r'Cộng chính xác; xác định phần tử giữa sau sắp xếp; đối chiếu diễn giải với từng giá trị.')
add(2,2,r'Trung bình ghép nhóm',
r'Dùng trung điểm nhóm và trọng số tần số; hiểu tính ước lượng.',
r'Lớp 11: mẫu ghép nhóm và số trung bình.',
r'B37; N: B02',r'N',r'101–102',r'S11.1 Bài 8, tr.in 59 / PDF 60; Bài 9, tr.in 62 / PDF 63.',
r'Thực hiện: tính trung bình có trọng số từ ba nhóm.',r'Giải quyết vấn đề; sử dụng công cụ toán học',r'Trả lời ngắn + giải thích',4,
r'''Thời gian hoàn thành một công việc được ghi như sau:

| Thời gian (phút) | $[0;10)$ | $[10;20)$ | $[20;30)$ |
|:---|:---:|:---:|:---:|
| Số người | 2 | 5 | 3 |

Tính số trung bình của mẫu ghép nhóm bằng giá trị đại diện là trung điểm nhóm. Có thể khẳng định đây là số trung bình chính xác của dữ liệu gốc không? Vì sao?''',
r'16 phút; chỉ là giá trị ước lượng cho trung bình của dữ liệu gốc.',
r'Giá trị đại diện lần lượt là 5, 15, 25; cỡ mẫu $n=2+5+3=10$. Số trung bình ghép nhóm là $(2\cdot5+5\cdot15+3\cdot25)/10=16$ phút. Ta chỉ biết mỗi quan sát nằm trong nhóm nào, không biết giá trị cụ thể, nên không được khẳng định 16 là trung bình chính xác của dữ liệu gốc.',
[r'Dùng đủ tần số; tính 16 phút.',r'Nêu rõ dữ liệu gốc chưa biết nên kết quả theo trung điểm là ước lượng.'],
r'PP: lấy trung bình ba trung điểm không có trọng số; KN: đồng nhất số đại diện với mọi quan sát.',
r'Ôn S11.1 tr.59, 62; ghi riêng hàng trung điểm và tổng tần số. Hàng B.2 tuần 5.',
r'''Thời gian (phút) chia thành $[0;10)$, $[10;20)$, $[20;30)$ với tần số lần lượt $3;4;3$. Tính trung bình ghép nhóm và giải thích có biết chính xác trung bình gốc không.''',
r'15 phút; chưa biết chính xác trung bình gốc.',
r'Trung bình ghép nhóm $(3\cdot5+4\cdot15+3\cdot25)/10=15$ phút. Mỗi giá trị gốc có thể khác trung điểm nên không suy ra trung bình gốc chính xác.',
r'Kiểm tổng tần số; tính có trọng số. Dựng hai mẫu gốc cùng nhóm nhưng khác trung bình để kiểm kết luận về tính ước lượng.')
add(2,3,r'Cùng trung bình, khác phân tán',
r'So sánh hai mẫu ghép nhóm bằng phương sai và giới hạn kết luận.',
r'Lớp 12: phương sai mẫu ghép nhóm; lớp 11: trung bình ghép nhóm.',
r'B37–B38; N: B02',r'R8; N',r'110',r'S12.1 Bài 10, tr.in 80–81 / PDF 82–83.',
r'Giải thích/phối hợp: nối trung bình, phương sai với nhận xét về dữ liệu.',r'Tư duy và lập luận; giải quyết vấn đề',r'Tự luận ngắn',6,
r'''Hai nhóm có thời gian hoàn thành công việc được ghép như sau:

| Thời gian (phút) | $[0;10)$ | $[10;20)$ | $[20;30)$ |
|:---|:---:|:---:|:---:|
| Nhóm A | 2 | 6 | 2 |
| Nhóm B | 4 | 2 | 4 |

Tính trung bình và phương sai của mỗi mẫu ghép nhóm (dùng mẫu số $n$). Một bạn nói: “Hai nhóm có cùng trung bình nên mức độ phân tán cũng như nhau.” Em có đồng ý không? Chỉ kết luận trong phạm vi các mẫu này.''',
r'$\bar x_A=\bar x_B=15$ phút; $s_A^2=40$, $s_B^2=80$ phút$^2$; không đồng ý.',
r'''Cả hai mẫu có cỡ 10 và trung bình 15 phút theo các giá trị đại diện 5, 15, 25. Phương sai:

$$s_A^2=\frac{2(5-15)^2+6(15-15)^2+2(25-15)^2}{10}=40,$$
$$s_B^2=\frac{4(5-15)^2+2(15-15)^2+4(25-15)^2}{10}=80.$$

Đơn vị phương sai là phút$^2$. Theo số liệu ghép nhóm, mẫu B phân tán hơn mẫu A. Cùng trung bình không buộc cùng độ phân tán. Đây là nhận xét về hai mẫu theo cách ghép nhóm; không đủ căn cứ kết luận mọi lần làm của nhóm A luôn ổn định hơn nhóm B.''',
[r'Tính hai trung bình và hai phương sai đúng, dùng mẫu số 10.',r'Phản bác nhận định bằng phương sai; giới hạn nhận xét ở mẫu ghép nhóm.'],
r'KN: trung tâm quyết định phân tán; TÍNH: quên bình phương hoặc chia $n-1$; ĐV: sai đơn vị phương sai.',
r'Ôn S12.1 tr.80–81; so sánh từng khoảng cách đến trung bình. Hàng B.2 tuần 5.',
r'''Các nhóm $[0;10)$, $[10;20)$, $[20;30)$ có tần số mẫu C là $1;8;1$, mẫu D là $3;4;3$. Tính trung bình, phương sai (mẫu số $n$); xét nhận định “cùng trung bình thì phân tán như nhau”.''',
r'Trung bình đều 15 phút; phương sai C bằng 20, D bằng 60 phút$^2$; nhận định sai.',
r'Giá trị đại diện 5, 15, 25 và cỡ mẫu đều 10. Trung bình đều 15. Phương sai C là $(100+100)/10=20$; D là $(300+300)/10=60$. Theo mẫu ghép nhóm, D phân tán hơn C; không suy rộng vượt mẫu.',
r'Tính bằng cả tổng bình phương độ lệch và trung bình bình phương trừ bình phương trung bình.')
add(3,1,r'Cùng phương khi có tọa độ bằng 0',
r'Xét cùng phương bằng một bội vô hướng, không chia cho 0.',
r'Lớp 10: nhân vectơ với số và tọa độ vectơ.',
r'B26; N: B02',r'N',r'82–83',r'S10.1 Bài 9, tr.in 56 / PDF 57; Bài 10, tr.in 63 / PDF 64.',
r'Nhận diện/điều kiện: dùng định nghĩa và nhận ra phép chia không hợp lệ.',r'Tư duy và lập luận',r'Tự luận ngắn',3,
r'Cho $\vec u=(0;2)$ và $\vec v=(0;-3)$. Hai vectơ có cùng phương không? Nếu có, tìm $k$ để $\vec u=k\vec v$ và cho biết chúng cùng hướng hay ngược hướng. Có được viết $\frac{0}{0}=\frac{2}{-3}$ để kiểm tra không?',
r'Cùng phương; $k=-\frac23$; ngược hướng; không được chia $0/0$.',
r'Từ tọa độ thứ hai, $2=-3k$ nên $k=-2/3$. Khi đó $k\vec v=(0;2)=\vec u$, xác nhận cả hai tọa độ. Hai vectơ đều khác vectơ-không và $k<0$ nên ngược hướng. Biểu thức $0/0$ không xác định; không được dùng tỉ số ấy làm tiêu chuẩn kiểm tra.',
[r'Xác định cùng phương qua $\vec u=(-2/3)\vec v$.',r'Kết luận ngược hướng và bác phép chia cho 0.'],
r'ĐK: chia tọa độ bằng 0; KN: nhầm cùng phương với cùng hướng.',
r'Ôn S10.1 tr.56; viết hai đẳng thức tọa độ với cùng một $k$. Hàng B.3 tuần 6–8.',
r'Cho $\vec a=(3;0)$ và $\vec b=(-6;0)$. Xét cùng phương, hướng và tìm $k$ trong $\vec a=k\vec b$. Giải thích vì sao không dùng tỉ số $0/0$.',
r'Cùng phương; $k=-1/2$; ngược hướng; $0/0$ không xác định.',
r'$3=-6k$ cho $k=-1/2$; tọa độ còn lại thỏa $0=k\cdot0$. Vì cả hai khác vectơ-không, $k<0$ cho ngược hướng. Không cần và không được chia $0/0$.',
r'Thế hệ số vào cả hai tọa độ; kiểm hai vectơ khác không trước khi kết luận về hướng.')
add(3,2,r'Khoảng cách điểm đến mặt phẳng',
r'Nhận pháp tuyến và tính khoảng cách bằng chuẩn hóa đúng.',
r'Lớp 12: tọa độ không gian, phương trình mặt phẳng và khoảng cách.',
r'B33–B34; N: B02',r'N',r'108',r'S12.2 Bài 14, tr.in 38 / PDF 40.',
r'Thực hiện: chọn đúng công thức và thay tọa độ.',r'Giải quyết vấn đề; sử dụng công cụ toán học',r'Trả lời ngắn + bước tính',4,
r'Trong không gian $Oxyz$, cho $A(1;2;3)$ và mặt phẳng $(P):x+2y+2z-5=0$. Nêu một vectơ pháp tuyến của $(P)$ và tính khoảng cách từ $A$ đến $(P)$. Đơn vị tọa độ là mét.',
r'$\vec n=(1;2;2)$; $d(A,(P))=2$ m.',
r'Pháp tuyến là $(1;2;2)$, có độ dài $\sqrt{1+4+4}=3\ne0$. Khoảng cách bằng $\frac{\lvert1+2\cdot2+2\cdot3-5\rvert}{3}=\frac63=2$ m. Phải lấy trị tuyệt đối ở tử; giá trị thế vào phương trình chưa phải khoảng cách nếu chưa chia độ dài pháp tuyến.',
[r'Chọn đúng một pháp tuyến khác không.',r'Thay đúng cả tử, mẫu và đơn vị; kết quả 2 m.'],
r'PP/ĐK: bỏ trị tuyệt đối, quên căn ở mẫu; TÍNH: thế nhầm tọa độ.',
r'Ôn S12.2 tr.38; kiểm đơn vị và độ dài pháp tuyến. Hàng B.8 tuần 16–17, sau nền vectơ ở B.3.',
r'Trong $Oxyz$, cho $M(2;0;1)$ và $(Q):2x-y+2z-3=0$. Nêu pháp tuyến và tính $d(M,(Q))$, đơn vị mét.',
r'$\vec n=(2;-1;2)$; khoảng cách 1 m.',
r'Pháp tuyến có độ dài 3. Tử số $\lvert4+0+2-3\rvert=3$; khoảng cách $3/3=1$ m.',
r'Kiểm bằng hình chiếu $H=A-\frac{\vec n\cdot A-5}{\|\vec n\|^2}\vec n$: H thuộc mặt phẳng và AH bằng 2. Câu thử lại kiểm tương tự.')
add(3,3,r'Góc của đường chéo',
r'Xác định đúng hình chiếu rồi tính góc đường thẳng với mặt phẳng.',
r'Lớp 11: hình hộp chữ nhật, hình chiếu, góc đường–mặt; lượng giác tam giác vuông.',
r'B25, B31–B32; N: B02',r'R6; B33 nếu dùng tọa độ',r'99–100',r'S11.2 Bài 24, tr.in 40 / PDF 41.',
r'Giải thích/phối hợp: chuyển hình không gian thành tam giác vuông.',r'Tư duy và lập luận; giải quyết vấn đề',r'Tự luận ngắn có hình',5,
r'''Cho hình hộp chữ nhật $ABCD.A_1B_1C_1D_1$ có $AB=3$ m, $AD=4$ m, $AA_1=2$ m; các đỉnh có chỉ số 1 nằm thẳng đứng trên các đỉnh tương ứng. Xác định góc giữa $AC_1$ và mặt phẳng $(ABCD)$, rồi tính số đo góc đó đến $0{,}1^\circ$. Giải thích vì sao em chọn được góc ấy.

![Hình biểu diễn hình hộp, không theo tỉ lệ.](src/hinh_hop.pdf){width=70%}''',
r'Góc $\widehat{CAC_1}$; $\arctan(2/5)\approx21{,}8^\circ$.',
r'Vì $CC_1\perp(ABCD)$, hình chiếu của $AC_1$ lên đáy là $AC$. Do đó góc cần tìm là $\widehat{CAC_1}$. Đường chéo đáy $AC=\sqrt{3^2+4^2}=5$ m. Trong tam giác vuông $ACC_1$, $\tan\widehat{CAC_1}=CC_1/AC=2/5$. Suy ra góc khoảng $21{,}8^\circ$. Nếu dùng tọa độ, vectơ đường chéo là $(3;4;2)$; $\sin\alpha=2/\sqrt{29}$ cho cùng kết quả. Cách tọa độ chỉ là cách kiểm thêm, không là điều kiện để học sinh lớp 11 làm câu này.',
[r'Xác định hình chiếu AC và góc tại A, kèm lý do vuông góc.',r'Tính AC = 5; dùng đúng tỉ số lượng giác, góc và làm tròn.'],
r'KN: lấy góc với cạnh đáy tùy ý; PP: dùng đường chéo không gian thay đường chéo đáy trong tỉ số tang; ĐV: máy ở radian.',
r'Ôn S11.2 tr.40; dựng tam giác chứa đường xiên và hình chiếu. Hàng B.3 tuần 6–8.',
r'Cho hình hộp chữ nhật $ABCD.A_1B_1C_1D_1$ có $AB=6$ m, $AD=8$ m, $AA_1=5$ m. Xác định và tính góc giữa $AC_1$ và đáy đến $0{,}1^\circ$, giải thích hình chiếu.',
r'$\widehat{CAC_1}=\arctan(1/2)\approx26{,}6^\circ$.',
r'Hình chiếu là AC, có độ dài $\sqrt{6^2+8^2}=10$ m; $CC_1=5$ m. Góc tại A trong tam giác vuông $ACC_1$ có tang $5/10=1/2$, nên bằng $26{,}6^\circ$ sau làm tròn.',
r'Kiểm hai cách tang qua hình chiếu và sin qua vectơ; kiểm nhãn hình từ tọa độ không gian trước khi chiếu lên giấy.')
add(4,1,r'Độc lập và xung khắc',
r'Phân biệt hai khái niệm bằng không gian mẫu nhỏ.',
r'Lớp 11: giao, hợp, độc lập, xung khắc; xác suất cổ điển lớp 10.',
r'B39–B40; N: B01',r'N',r'86, 102',r'S11.2 Bài 28, tr.in 68, 70 / PDF 69, 71; S10.2 Bài 27, tr.in 84 / PDF 85.',
r'Nhận diện/điều kiện: đối chiếu định nghĩa trên bốn kết quả.',r'Tư duy và lập luận',r'Đúng/sai 4 ý + giải thích',5,
r'''Tung một đồng xu cân đối hai lần độc lập. Gọi $A$ là biến cố “lần đầu ngửa”, $B$ là biến cố “lần thứ hai ngửa”. Xét đúng/sai từng ý, kèm giải thích hoặc liệt kê kết quả:

a) $P(A\cap B)=1/4$.

b) $A$ và $B$ xung khắc.

c) $A$ và $B$ độc lập.

d) $P(A\cup B)=1$.''',
r'a) Đúng; b) Sai; c) Đúng; d) Sai.',
r'Viết N là ngửa, S là sấp. Bốn kết quả NN, NS, SN, SS đồng khả năng. Giao chỉ có NN nên xác suất $1/4$; do giao không rỗng, hai biến cố không xung khắc. Mỗi biến cố có xác suất $1/2$, và $P(A\cap B)=P(A)P(B)=1/4$ nên độc lập. Hợp gồm NN, NS, SN, xác suất $3/4$, không phải 1. Các ý đều được xét từ giả thiết chung, không lấy một ý trước làm giả thiết cho ý sau.',
[r'Lưu riêng đáp án bốn ý.',r'Có không gian mẫu đúng hoặc lập luận xác suất tương đương; phân biệt xung khắc với độc lập.'],
r'KN: xem độc lập là không thể cùng xảy ra; PP: cộng xác suất không trừ giao.',
r'Ôn S11.2 tr.68, 70; vẽ bốn kết quả và tô A, B. Hàng B.4 tuần 9–10.',
r'''Gieo một xúc xắc cân đối. $E$ là biến cố “số chấm chẵn”, $F$ là biến cố “số chấm chia hết cho 3”. Xét đúng/sai và giải thích:

a) $P(E\cap F)=1/6$. b) $E,F$ xung khắc.

c) $E,F$ độc lập. d) $P(E\cup F)=5/6$.''',
r'Đúng; Sai; Đúng; Sai.',
r'$E=\{2,4,6\}$, $F=\{3,6\}$, giao là $\{6\}$. Xác suất giao $1/6=(1/2)(1/3)$ nên độc lập, nhưng không xung khắc. Hợp $\{2,3,4,6\}$ có xác suất $4/6=2/3$, không phải $5/6$.',
r'Liệt kê toàn bộ bốn kết quả đồng xu và sáu kết quả xúc xắc; kiểm giao, hợp và tích xác suất.')
add(4,2,r'Chọn hai viên khác màu',
r'Đếm đủ, không trùng trong mô hình chọn không hoàn lại.',
r'Lớp 10: tổ hợp, xác suất cổ điển.',
r'B39; N: B02',r'N',r'86',r'S10.2 Bài 24, tr.in 68 / PDF 69; Bài 27, tr.in 84 / PDF 85.',
r'Thực hiện: chọn mô hình các cặp đồng khả năng và đếm thuận lợi.',r'Giải quyết vấn đề; tư duy và lập luận',r'Trả lời ngắn + lập luận',4,
r'Hộp có 4 viên đỏ và 3 viên xanh, các viên cùng kích thước và khối lượng. Chọn ngẫu nhiên đồng thời 2 viên, mọi cặp viên đều có khả năng được chọn như nhau. Tính xác suất chọn được hai viên khác màu. Nêu số trường hợp có thể và thuận lợi.',
r'$\frac{4}{7}$; 21 cặp có thể, 12 cặp thuận lợi.',
r'Có $\binom72=21$ cặp không thứ tự. Mỗi cặp khác màu được xác định duy nhất bởi một trong 4 viên đỏ và một trong 3 viên xanh, nên có $4\cdot3=12$ cặp. Xác suất $12/21=4/7$. Nếu chọn theo thứ tự, phải đếm đủ hai thứ tự màu: $(4/7)(3/6)+(3/7)(4/6)=4/7$. Hai cách dùng không gian mẫu khác nhau nhưng đều nhất quán.',
[r'Đếm 21 cặp tổng và 12 cặp khác màu, hoặc cách có thứ tự nhất quán.',r'Kết quả $4/7$, không coi ba kiểu màu là đồng khả năng.'],
r'PP: đếm thuận lợi có thứ tự nhưng mẫu không thứ tự; KN: chọn không hoàn lại mà giữ mẫu số 7 ở lần sau.',
r'Ôn tổ hợp S10.2 tr.68 và mô hình xác suất B39; ghi rõ có hay không xét thứ tự. Hàng B.4 tuần 9–10.',
r'Hộp có 5 viên đỏ, 3 viên xanh cùng kích thước, khối lượng. Chọn ngẫu nhiên đồng thời 2 viên với mọi cặp đồng khả năng. Tính xác suất hai viên khác màu, nêu cách đếm.',
r'$15/28$.',
r'Tổng số cặp $\binom82=28$. Cặp khác màu có $5\cdot3=15$. Xác suất $15/28$; theo thứ tự cũng được $2(5/8)(3/7)=15/28$.',
r'Vét cạn tất cả cặp viên có nhãn: 21 và 28 cặp; đối chiếu với tính theo thứ tự.')
add(4,3,r'Đổi chiều điều kiện',
r'Đọc bảng hai chiều; phân biệt hai xác suất điều kiện.',
r'Lớp 12: xác suất có điều kiện và bảng hai chiều.',
r'B41; N: B02',r'R2; N',r'110',r'S12.2 Bài 18, tr.in 65–66 / PDF 67–68.',
r'Giải thích/phối hợp: đổi mẫu số theo thông tin đã biết.',r'Mô hình hóa; tư duy và lập luận',r'Tự luận ngắn với bảng',5,
r'''Một lớp có bảng tham gia câu lạc bộ như sau:

| | Có tham gia | Không tham gia |
|:---|:---:|:---:|
| Nữ | 18 | 12 |
| Nam | 6 | 14 |

Chọn ngẫu nhiên một học sinh, mọi học sinh có khả năng được chọn như nhau.

a) Biết học sinh được chọn có tham gia câu lạc bộ, tính xác suất đó là nữ.

b) Biết học sinh được chọn là nữ, tính xác suất bạn ấy có tham gia. Giải thích vì sao hai mẫu số khác nhau.''',
r'a) $3/4$; b) $3/5$.',
r'Có 24 học sinh tham gia, trong đó 18 nữ, nên câu a có xác suất $18/24=3/4$. Có 30 học sinh nữ, trong đó 18 tham gia, nên câu b có xác suất $18/30=3/5$. Điều kiện “tham gia” giới hạn tập xét vào 24 người; điều kiện “nữ” giới hạn vào 30 người. Cả hai mẫu số dương. Không dùng 50 cho xác suất đã có điều kiện và không đồng nhất hai chiều điều kiện.',
[r'Tính riêng đúng a và b.',r'Nêu được nhóm bị giới hạn bởi điều kiện, mẫu số 24 và 30.'],
r'ĐK/KN: đảo điều kiện; dùng toàn lớp làm mẫu số; ĐỌC: đọc nhầm hàng/cột.',
r'Ôn S12.2 tr.65–66; khoanh nhóm đã biết trước rồi đếm trong nhóm ấy. Hàng B.9 tuần 18; nền B.4 nếu đếm/tỉ lệ chưa ổn.',
r'''Bảng mượn sách: nữ có mượn 12, không mượn 8; nam có mượn 8, không mượn 12. Chọn đều một người. Tính xác suất là nữ biết có mượn; tính xác suất có mượn biết là nữ. Hai kết quả bằng nhau có chứng minh hai chiều điều kiện luôn bằng nhau không?''',
r'Cả hai bằng $3/5$; không chứng minh luôn bằng nhau.',
r'Số người có mượn là 20, số nữ cũng là 20, giao gồm 12 nữ có mượn. Hai xác suất cùng bằng $12/20=3/5$ do hai mẫu số ở bảng này tình cờ bằng nhau. Nói chung các nhóm điều kiện có thể có cỡ khác nhau; bảng câu gốc đã cho hai kết quả khác nhau.',
r'Kiểm tổng hàng/cột và mẫu số dương; tính phân số chính xác; thử lại đổi cấu trúc mẫu số bằng nhau để tránh học mẹo “hai chiều luôn khác”.')
add(5,1,r'Tăng theo lượng hay theo tỉ lệ',
r'Nhận dạng cấp số cộng và cấp số nhân qua quy luật thay đổi.',
r'Lớp 11: cấp số cộng, cấp số nhân.',
r'B10; N: B02',r'N',r'91–92',r'S11.1 Bài 6, tr.in 49 / PDF 50; Bài 7, tr.in 52 / PDF 53.',
r'Nhận diện: phân biệt hiệu không đổi và tỉ số không đổi.',r'Tư duy và lập luận',r'Trả lời ngắn + giải thích',3,
r'Với $n=0,1,2,\ldots$, hai dãy được cho bởi $a_n=100+20n$, $b_n=100(1{,}2)^n$. Dãy nào là cấp số cộng, dãy nào là cấp số nhân? Nêu công sai hoặc công bội và giải thích dãy nào tăng 20% sau mỗi bước.',
r'$a_n$ là cấp số cộng, công sai 20; $b_n$ là cấp số nhân, công bội 1,2; $b_n$ tăng 20% mỗi bước.',
r'$a_{n+1}-a_n=20$ nên a là cấp số cộng. Vì $b_n>0$, tỉ số $b_{n+1}/b_n=1{,}2$ cho cấp số nhân. Nhân với $1{,}2=1+20\%$ có nghĩa tăng thêm 20% giá trị ngay trước đó. Dãy a tăng một lượng cố định 20, không tăng một tỉ lệ cố định 20%. Hai dãy trùng ở bước đầu chưa đủ để đồng nhất quy luật.',
[r'Nhận đúng hai loại dãy và công sai/công bội.',r'Gắn tăng 20% với nhân 1,2, phân biệt tăng thêm 20 đơn vị.'],
r'KN: nhầm tăng 20 đơn vị với tăng 20%; ĐỌC: nhầm chỉ số bắt đầu ở 0.',
r'Ôn S11.1 tr.49, 52; tính ba số đầu rồi kiểm hiệu và tỉ số. Hàng B.5 tuần 11–12.',
r'Với $n\geq0$ nguyên, cho $c_n=80+8n$ và $d_n=80(1{,}1)^n$. Nhận dạng hai dãy, nêu công sai/công bội, và chỉ ra dãy tăng 10% mỗi bước.',
r'Cấp số cộng c có công sai 8; cấp số nhân d có công bội 1,1; d tăng 10%.',
r'Hiệu $c_{n+1}-c_n=8$; tỉ số $d_{n+1}/d_n=1{,}1=1+10\%$. Tăng thêm 8 chỉ bằng 10% của 80 ở bước đầu, không phải 10% mọi số hạng trước.',
r'Kiểm đại số tổng quát hiệu/tỉ số; tính thêm bước n=2 để phát hiện nhầm quy luật.')
add(5,2,r'Lôgarit và nghiệm ngoại lai',
r'Giải phương trình lôgarit có giữ điều kiện từng đối số.',
r'Lớp 11: tính chất lôgarit, phương trình lôgarit; phương trình bậc hai.',
r'B13, B15; N: B02, B06',r'N',r'94–95',r'S11.2 Bài 19, tr.in 11 / PDF 12; Bài 21, tr.in 21 / PDF 22.',
r'Thực hiện: ghép lôgarit và kiểm nghiệm sau biến đổi.',r'Giải quyết vấn đề; tư duy và lập luận',r'Tự luận ngắn',4,
r'Giải phương trình $\log_2(x-1)+\log_2(x-3)=3$. Ghi điều kiện trước khi biến đổi và kiểm tra từng nghiệm của phương trình đại số thu được.',
r'$x=5$.',
r'Điều kiện $x-1>0$, $x-3>0$ cho $x>3$. Trong miền này, ghép lôgarit được $\log_2[(x-1)(x-3)]=3$, nên $(x-1)(x-3)=8$. Phương trình $x^2-4x-5=0$ có hai nghiệm 5 và $-1$. Chỉ 5 thỏa $x>3$. Thế vào đề: $\log_2 4+\log_2 2=2+1=3$. Nghiệm $-1$ làm cả hai đối số âm nên bị loại, dù tích của chúng dương.',
[r'Ghi đúng $x>3$ trước hoặc trong lập luận tương đương có điều kiện.',r'Giải được 5 và $-1$, loại $-1$, thế ngược nghiệm 5.'],
r'ĐK: chỉ yêu cầu tích dương mà quên từng đối số; TÍNH: sai phân tích bậc hai.',
r'Ôn S11.2 tr.11, 21 và B02/B06 nếu biến đổi sai. Hàng B.5 tuần 11–12.',
r'Giải $\log_3(x-1)+\log_3(x-3)=1$, giữ điều kiện và kiểm từng nghiệm đại số.',
r'$x=4$.',
r'Điều kiện $x>3$. Phương trình tích $(x-1)(x-3)=3$ cho $x^2-4x=0$, nghiệm 0 hoặc 4. Loại 0; tại 4, $\log_3 3+\log_3 1=1$.',
r'Phân tích đa thức chính xác; lọc nghiệm theo từng đối số; thế ngược vào lôgarit gốc.')
add(5,3,r'Thời điểm đạt ngưỡng',
r'Lập mô hình nhân theo chu kì và tìm số kì nguyên nhỏ nhất.',
r'Lớp 11: cấp số nhân, tăng trưởng; có thể dùng bảng lũy thừa hoặc lôgarit.',
r'B10, B14–B15; N: B02',r'R8; N',r'92, 95',r'S11.1 Bài 7, tr.in 52 / PDF 53; S11.2 Bài 21, tr.in 21 / PDF 22.',
r'Giải thích/phối hợp: mô hình, bất đẳng thức ngưỡng và tính nguyên.',r'Mô hình hóa; giải quyết vấn đề',r'Tự luận ngắn',5,
r'Trong một mô hình giả định, diện tích bèo ban đầu là $100$ cm$^2$ và sau mỗi ngày bằng $120\%$ diện tích ngày trước. Chỉ quan sát ở cuối từng ngày, với ngày ban đầu là $n=0$. Viết diện tích sau $n$ ngày và tìm số ngày nguyên nhỏ nhất để diện tích đạt ít nhất $200$ cm$^2$. Kiểm tra cả ngày đó và ngày liền trước.',
r'$S_n=100(1{,}2)^n$ cm$^2$; $n_{\min}=4$.',
r'Vì tăng theo tỉ lệ cố định, $S_n=100(1{,}2)^n$ với n nguyên không âm. Tại $n=3$, $S_3=172{,}8<200$; tại $n=4$, $S_4=207{,}36\geq200$. Dãy tăng vì công bội $1{,}2>1$, nên mọi ngày trước ngày 3 cũng chưa đạt ngưỡng; ngày 4 là nhỏ nhất. Dùng lôgarit cũng cho $n\geq\log(2)/\log(1{,}2)\approx3{,}802$; cần lấy số nguyên nhỏ nhất không dưới ngưỡng là 4, không bỏ phần thập phân để lấy 3.',
[r'Lập đúng mô hình và miền n nguyên không âm.',r'Kết luận 4, kiểm ngày 3, ngày 4 và lý do dãy tăng.'],
r'KN: tăng tuyến tính; ĐK: làm tròn số kì không đúng ngưỡng; ĐỌC: lệch mốc n=0.',
r'Ôn S11.1 tr.52; lập bảng hai mốc kề ngưỡng. Hàng B.5 tuần 11–12, phối hợp R8.',
r'Diện tích ban đầu 80 cm$^2$, mỗi ngày bằng 125% ngày trước. Quan sát cuối ngày, $n=0$ là ban đầu. Viết mô hình và tìm ngày nguyên nhỏ nhất đạt ít nhất 150 cm$^2$, kiểm hai mốc kề nhau.',
r'$S_n=80(1{,}25)^n$; ngày 3.',
r'Dãy tăng; $S_2=125<150$, $S_3=156{,}25\geq150$. Vậy ngày 3 là nhỏ nhất. Công thức dùng n=0 nên trả đúng giá trị ban đầu 80.',
r'Tính các mốc bằng phân số chính xác 6/5 và 5/4; dùng tính tăng để chứng minh nhỏ nhất.')
add(6,1,r'Độ, radian và dấu',
r'Chuyển đơn vị góc và xác định dấu của côsin.',
r'Lớp 11: radian, đường tròn lượng giác; góc phần tư.',
r'B07; N: B02',r'N',r'89–90',r'S11.1 Bài 1, tr.in 8 / PDF 9; Bài 3, tr.in 23 / PDF 24.',
r'Nhận diện: chuyển đơn vị và đọc dấu theo góc.',r'Tư duy và lập luận',r'Một lựa chọn + giải thích',3,
r'''Với $\alpha=150^\circ$, chọn **một** phương án đúng về số đo radian và dấu của $\cos\alpha$. Giải thích ngắn.

A. $\alpha=5\pi/6$; $\cos\alpha<0$.

B. $\alpha=5\pi/6$; $\cos\alpha>0$.

C. $\alpha=5\pi/3$; $\cos\alpha<0$.

D. $\alpha=\pi/6$; $\cos\alpha>0$.''',
r'A.',
r'$150^\circ=150\cdot\pi/180=5\pi/6$ radian. Góc này thuộc góc phần tư II, nên côsin âm; cụ thể $\cos150^\circ=-\sqrt3/2$. B sai dấu; C và D sai số đo radian của góc đã cho. Chỉ A đúng.',
[r'Chọn A.',r'Dùng đúng hệ số đổi $\pi/180$ và giải thích dấu âm.'],
r'ĐV: đổi đơn vị sai; KN: nhầm dấu ở góc phần tư II.',
r'Ôn S11.1 tr.8; biểu diễn góc trên đường tròn lượng giác. Hàng B.6 tuần 13.',
r'Đổi $240^\circ$ sang radian và nêu dấu của $\sin240^\circ$; giải thích bằng vị trí góc.',
r'$4\pi/3$; sin âm.',
r'$240\pi/180=4\pi/3$. Góc thuộc góc phần tư III nên sin âm; giá trị chính xác là $-\sqrt3/2$.',
r'Đổi đơn vị bằng phân số; tính sin/cos của góc chuẩn để kiểm dấu và tính duy nhất của phương án.')
add(6,2,r'Họ nghiệm và khoảng xét',
r'Viết đủ hai họ nghiệm, chia đối số đúng và lọc theo khoảng.',
r'Lớp 11: phương trình lượng giác cơ bản; góc tính bằng radian.',
r'B09; N: B02',r'N',r'91',r'S11.1 Bài 4, tr.in 33 / PDF 34.',
r'Thực hiện: giải phương trình và chọn nghiệm trong một khoảng.',r'Giải quyết vấn đề; tư duy và lập luận',r'Trả lời ngắn + họ nghiệm',5,
r'Giải $\sin(2x)=\frac{\sqrt3}{2}$ với $x\in[0;2\pi)$. Viết họ nghiệm tổng quát trước khi liệt kê nghiệm trong khoảng. Góc tính bằng radian.',
r'$x=\pi/6+k\pi$ hoặc $x=\pi/3+k\pi$; nghiệm $\pi/6,\pi/3,7\pi/6,4\pi/3$.',
r'Đặt góc $2x$. Hai họ là $2x=\pi/3+2k\pi$ hoặc $2x=2\pi/3+2k\pi$, $k\in\mathbb Z$. Chia cả hai vế cho 2 được $x=\pi/6+k\pi$ hoặc $x=\pi/3+k\pi$. Điều kiện $0\leq x<2\pi$ cho $k=0,1$ ở mỗi họ. Bốn nghiệm phân biệt là $\pi/6,\pi/3,7\pi/6,4\pi/3$. Các k khác cho nghiệm ngoài khoảng.',
[r'Viết đủ hai họ với bước $k\pi$, không giữ nhầm $2k\pi$.',r'Liệt kê đúng đủ bốn nghiệm và loại các k ngoài khoảng.'],
r'KN: chỉ lấy nghiệm máy tính trả về; TÍNH: quên chia chu kì; ĐK: sai đầu mút khoảng.',
r'Ôn S11.1 tr.33; viết hai bất đẳng thức lọc k cho từng họ. Hàng B.6 tuần 13.',
r'Giải $\sin(2x)=1/2$ trên $[0;2\pi)$, góc radian. Viết hai họ rồi chọn đủ nghiệm.',
r'$x=\pi/12+k\pi$ hoặc $5\pi/12+k\pi$; nghiệm $\pi/12$, $5\pi/12$, $13\pi/12$, $17\pi/12$.',
r'Hai họ của 2x là $\pi/6+2k\pi$ và $5\pi/6+2k\pi$. Chia 2, rồi lấy k=0,1 ở cả hai họ. Các k còn lại nằm ngoài khoảng; thế từng nghiệm vào sin(2x) đều bằng 1/2.',
r'Thế ngược cả bốn nghiệm và kiểm đầy đủ k bằng bất đẳng thức khoảng, không chỉ quét số.')
add(6,3,r'Một mô hình tuần hoàn',
r'Giải thích biên độ, chu kì và thời điểm đầu tiên đạt cực đại.',
r'Lớp 11: hàm sin, chu kì, phương trình sin cơ bản.',
r'B08–B09; N: B02',r'R8; N',r'90–91',r'S11.1 Bài 3, tr.in 25 / PDF 26; Bài 4, tr.in 33 / PDF 34.',
r'Giải thích/phối hợp: nối công thức lượng giác với đại lượng có đơn vị.',r'Mô hình hóa; giải quyết vấn đề',r'Tự luận ngắn',5,
r'Một mô hình mực nước cho $h(t)=3+2\sin(\pi t/6)$ mét, với $t\geq0$ tính bằng giờ; đối số của sin tính bằng radian. Tìm chu kì dương nhỏ nhất, khoảng giá trị của h và thời điểm đầu tiên mực nước đạt 5 m. Giải thích ngắn.',
r'Chu kì 12 giờ; $h\in[1;5]$ m; lần đầu tại $t=3$ giờ.',
r'Đối số tăng $2\pi$ khi thời gian tăng $2\pi/(\pi/6)=12$ giờ. Vì hệ số sin khác 0, đây là chu kì dương nhỏ nhất. Từ $-1\leq\sin\leq1$ được $1\leq h\leq5$; các biên đều đạt được. Điều kiện $h=5$ cho $\sin(\pi t/6)=1$, nên $t=3+12k$, k nguyên. Trên miền $t\geq0$, thời điểm đầu là 3 giờ.',
[r'Xác định 12 giờ và khoảng [1;5] m.',r'Giải được họ thời điểm, lấy đúng lần đầu t=3 theo miền t không âm.'],
r'KN: nhầm hệ số 2 là chu kì; ĐV: bỏ đơn vị; ĐK: không chọn thời điểm không âm nhỏ nhất.',
r'Ôn S11.1 tr.25, 33; tách mức nền 3, độ dao động 2 và tốc độ góc $\pi/6$. Hàng B.6 tuần 13.',
r'Mô hình $h(t)=4+\sin(\pi t/4)$ mét, $t\geq0$ giờ, đối số radian. Tìm chu kì dương nhỏ nhất, khoảng giá trị và lần đầu đạt 5 m.',
r'8 giờ; [3;5] m; t=2 giờ.',
r'Chu kì $2\pi/(\pi/4)=8$ giờ. Vì sin trong [-1;1], h trong [3;5]. Khi sin=1, $t=2+8k$; thời điểm không âm đầu tiên là 2 giờ.',
r'Kiểm chu kì bằng thay t+T; dùng miền sin và giải họ thời điểm để chứng minh lần đầu.')
add(7,1,r'Nhận diện nguyên hàm',
r'Dùng đạo hàm để nhận nguyên hàm và hiểu hằng số cộng.',
r'Lớp 12: định nghĩa và họ nguyên hàm; đạo hàm lớp 11.',
r'B22; N: B02',r'R1; N',r'107',r'S12.2 Bài 11, tr.in 5 / PDF 7.',
r'Nhận diện: kiểm định nghĩa bằng đạo hàm từng biểu thức.',r'Tư duy và lập luận',r'Chọn tất cả biểu thức đúng + giải thích',3,
r'''Trong bốn hàm trên $\mathbb R$ dưới đây, hãy chọn **tất cả** hàm là nguyên hàm của $f(x)=2x$, rồi giải thích bằng đạo hàm:

$F_1(x)=x^2+3$; $F_2(x)=x^2-5$; $F_3(x)=2x^2$; $F_4(x)=x^2+x$.

Đây là câu chọn nhiều biểu thức, không phải trắc nghiệm một đáp án.''',
r'$F_1$ và $F_2$.',
r'Đạo hàm lần lượt là $2x,2x,4x,2x+1$. Chỉ $F_1,F_2$ có đạo hàm bằng 2x với mọi x thực. Hai nguyên hàm này khác nhau hằng số 8. Việc đạo hàm trùng tại một điểm, chẳng hạn $4x=2x$ ở x=0, không đủ để là nguyên hàm trên cả $\mathbb R$.',
[r'Chọn đúng và đủ $F_1,F_2$.',r'Kiểm cả bốn đạo hàm; hiểu đẳng thức phải đúng trên miền xét.'],
r'KN: bỏ hằng số cộng hoặc lẫn đạo hàm với nguyên hàm; ĐK: chỉ thử một điểm.',
r'Ôn S12.2 tr.5; kiểm bằng đạo hàm trên toàn miền. Hàng B.7 tuần 14–15.',
r'Chọn tất cả nguyên hàm của $3x^2$ trên $\mathbb R$ trong $G_1=x^3+7$, $G_2=x^3-2$, $G_3=3x^3$, $G_4=x^3+x$; giải thích.',
r'$G_1,G_2$.',
r'Các đạo hàm là $3x^2,3x^2,9x^2,3x^2+1$. Chỉ hai hàm đầu thỏa định nghĩa với mọi x.',
r'Lấy đạo hàm tượng trưng của cả bốn biểu thức; kiểm đẳng thức đồng nhất, không dựa một điểm.')
add(7,2,r'Điều kiện đầu',
r'Tìm nguyên hàm riêng từ điều kiện tại một điểm.',
r'Lớp 12: nguyên hàm đa thức và điều kiện đầu.',
r'B22; N: B02',r'R1; N',r'107',r'S12.2 Bài 11, tr.in 5 / PDF 7.',
r'Thực hiện: tính nguyên hàm, giải hằng số, thay giá trị.',r'Giải quyết vấn đề',r'Trả lời ngắn + bước tính',4,
r'Cho $F^\prime(x)=3x^2-2$ trên $\mathbb R$ và $F(1)=4$. Tìm $F(x)$ rồi tính $F(2)$.',
r'$F(x)=x^3-2x+5$; $F(2)=9$.',
r'Họ nguyên hàm có dạng $F(x)=x^3-2x+C$. Từ $F(1)=1-2+C=4$ suy ra C=5. Vì vậy $F(2)=8-4+5=9$. Kiểm lại: đạo hàm bằng $3x^2-2$ và giá trị tại 1 bằng 4. Có thể kiểm độc lập bằng $F(2)=F(1)+\int_1^2(3x^2-2)\,dx=4+5=9$.',
[r'Tìm họ nguyên hàm và C=5.',r'Ghi đúng F và F(2)=9; thỏa điều kiện đầu.'],
r'KN: quên C hoặc thay F(1) vào đạo hàm; TÍNH: sai dấu hằng số.',
r'Ôn S12.2 tr.5; luôn kiểm hai điều kiện: đạo hàm và giá trị ban đầu. Hàng B.7 tuần 14–15.',
r'Cho $G^\prime(x)=2x+3$ và $G(0)=1$. Tìm $G(x)$ và $G(2)$.',
r'$G(x)=x^2+3x+1$; $G(2)=11$.',
r'Nguyên hàm $x^2+3x+C$; tại 0 bằng 1 nên C=1. Tại 2 được $4+6+1=11$. Lấy đạo hàm và thế x=0 kiểm cả hai điều kiện.',
r'Kiểm bằng đạo hàm, điều kiện đầu và hiệu tích phân xác định; đối chiếu chính xác.')
add(7,3,r'Độ dời và quãng đường',
r'Lập tích phân có dấu và tích phân tốc độ; tách tại thời điểm đổi chiều.',
r'Lớp 12: tích phân, dấu hàm, vận tốc và quãng đường.',
r'B23–B24; N: B02, B06',r'R1; R8; N',r'107',r'S12.2 Bài 12, tr.in 14, 17 / PDF 16, 19; Bài 13, tr.in 19 / PDF 21.',
r'Giải thích/phối hợp: phân biệt đại lượng tích lũy theo dấu trong mô hình.',r'Mô hình hóa; tư duy và lập luận',r'Tự luận ngắn',6,
r'Một vật chuyển động trên trục thẳng, vận tốc $v(t)=t-2$ m/s trong $0\leq t\leq5$ giây. Viết biểu thức tích phân **trước khi tính** để tìm: a) độ dời từ t=0 đến t=5; b) tổng quãng đường đi được. Giải thích vì sao hai kết quả khác nhau.',
r'Độ dời 2,5 m; quãng đường 6,5 m.',
r'''Độ dời là

$$\Delta x=\int_0^5(t-2)\,dt=\left[\frac{t^2}{2}-2t\right]_0^5=\frac52\text{ m}.$$

Vận tốc âm trên [0;2), bằng 0 tại 2 và dương trên (2;5]. Vì vật đổi chiều, tổng quãng đường là

$$L=\int_0^5\lvert t-2\rvert\,dt=\int_0^2(2-t)\,dt+\int_2^5(t-2)\,dt=2+\frac92=\frac{13}{2}\text{ m}.$$

Vật đi 2 m theo chiều âm rồi 4,5 m theo chiều dương; độ dời là $-2+4{,}5=2{,}5$ m, còn quãng đường cộng hai độ dài. Không cần biết vị trí ban đầu để tính hai đại lượng này.''',
[r'Lập và tính đúng độ dời.',r'Lập tích phân trị tuyệt đối, tách ở 2, tính 6,5 m; giải thích đổi chiều.'],
r'KN: dùng tích phân vận tốc làm quãng đường khi vận tốc đổi dấu; PP: tách sai cận; ĐV: sai đơn vị.',
r'Ôn dấu B06 và S12.2 tr.14, 17, 19; vẽ hai phần tam giác dưới đồ thị vận tốc. Hàng B.7 tuần 14–15.',
r'Vận tốc $v(t)=t-1$ m/s trên $0\leq t\leq3$ giây. Lập tích phân rồi tính độ dời và quãng đường; giải thích dấu.',
r'Độ dời 1,5 m; quãng đường 2,5 m.',
r'Độ dời $\int_0^3(t-1)\,dt=3/2$ m. Vận tốc đổi dấu ở 1, nên quãng đường $\int_0^1(1-t)\,dt+\int_1^3(t-1)\,dt=1/2+2=5/2$ m. Hai đoạn chuyển động ngược chiều nhau.',
r'Kiểm nguyên hàm và diện tích hai tam giác trên đồ thị vận tốc; kiểm L không nhỏ hơn trị tuyệt đối độ dời.')
add(8,1,r'Biến và miền hợp lệ',
r'Từ lời văn lập ràng buộc và hàm mục tiêu với miền không suy biến.',
r'Lớp 10: hàm số bậc hai; nền chu vi và diện tích hình chữ nhật.',
r'B03–B05; N: B02',r'R1; N',r'79–80',r'S10.1 Bài 4, tr.in 27 / PDF 28; S10.2 Bài 15, tr.in 6 / PDF 7.',
r'Nhận diện/điều kiện: xác định biến, ba cạnh rào và miền.',r'Mô hình hóa; giao tiếp toán học',r'Tự luận ngắn',4,
r'Một mảnh vườn hình chữ nhật có một cạnh tựa vào bức tường thẳng đủ dài. Dùng đúng 20 m hàng rào cho **ba cạnh còn lại**, không chừa lối mở. Gọi x là chiều dài mỗi cạnh vuông góc với tường, y là cạnh song song với tường. Viết ràng buộc giữa x,y; miền hợp lệ của x; và diện tích A theo x để chuẩn bị tìm diện tích lớn nhất. **Chưa cần giải bài toán tối ưu.**',
r'$2x+y=20$; $0<x<10$; $A(x)=x(20-2x)$ m$^2$.',
r'Hai cạnh vuông góc đều dài x và một cạnh song song dài y, nên $2x+y=20$. Vườn phải có hai kích thước dương: x>0 và $y=20-2x>0$, suy ra $0<x<10$. Diện tích $A=xy=x(20-2x)$. Không dùng chu vi bốn cạnh vì cạnh tựa tường không cần rào. Miền mở loại các hình suy biến x=0 hoặc y=0.',
[r'Lập đúng ràng buộc ba cạnh và miền $0<x<10$.',r'Lập hàm diện tích, đơn vị; chưa cần tìm điểm tối ưu.'],
r'ĐỌC: tính cả bốn cạnh; ĐK: nhận hình suy biến; PP: lấy chiều dài rào làm diện tích.',
r'Vẽ sơ đồ ba cạnh, gắn tên biến và đơn vị; ôn S10.1 tr.27, S10.2 tr.6. Sửa ở chặng A; phối hợp R1 tại B.1 tuần 2–4.',
r'Mảnh vườn tựa tường tương tự, dùng đúng 30 m rào ba cạnh. Đặt x là hai cạnh vuông góc với tường, y là cạnh còn lại. Viết ràng buộc, miền x và diện tích theo x, chưa tối ưu.',
r'$2x+y=30$; $0<x<15$; $A=x(30-2x)$ m$^2$.',
r'Hai cạnh x và một cạnh y dùng hết 30 m nên y=30-2x. Điều kiện hai cạnh dương cho $0<x<15$. Nhân hai kích thước được diện tích.',
r'Đếm đúng số cạnh; thế một cấu hình hợp lệ; kiểm các biên suy biến và đơn vị của hàm mục tiêu.')
add(8,2,r'Từ giá cước đến khoảng cách',
r'Lập chi phí từ hai đoạn tính tiền và kiểm tra ngưỡng ngân sách.',
r'Lớp 10: mô hình hàm số và bất phương trình bậc nhất; nền đơn vị.',
r'B04; N: B02',r'R1; N',r'80',r'S10.2 Bài 15, tr.in 6 / PDF 7; CT tr.80 nêu mô hình chi phí theo khoảng.',
r'Thực hiện: chuyển quy tắc bằng lời thành biểu thức rồi giải.',r'Mô hình hóa; giải quyết vấn đề',r'Tự luận ngắn',4,
r'Một mô hình cước xe giả định tính 18 nghìn đồng cho kilômét đầu tiên; phần vượt 1 km tính 11 nghìn đồng/km, theo đúng độ dài thực, không làm tròn số kilômét và không có phụ phí. Một chuyến đi dài $d\geq1$ km có ngân sách 73 nghìn đồng. Lập công thức chi phí rồi tìm quãng đường lớn nhất có thể đi; kiểm tra kết quả theo quy tắc tính cước.',
r'$C(d)=18+11(d-1)$ nghìn đồng; $d_{\max}=6$ km.',
r'Kilômét đầu đã được tính trong 18, nên phần tính thêm là d-1. Ràng buộc $18+11(d-1)\leq73$ cho $d\leq6$. Kết hợp d≥1, miền đi được là [1;6]. Vì giá tăng theo d và cho phép độ dài thực, lớn nhất là 6 km. Kiểm: 1 km đầu 18, 5 km sau 55, tổng 73 nghìn đồng. Không dùng $18+11d$ vì sẽ tính thêm một kilômét.',
[r'Lập đúng công thức trên miền d≥1.',r'Giải ngưỡng và kiểm 6 km tốn đúng 73 nghìn đồng.'],
r'ĐỌC/PP: tính thêm phí trên cả d thay vì d-1; ĐV: trộn đồng và nghìn đồng.',
r'Ôn mô hình hàm số B04 và bất phương trình nền B02; thay d=1 để kiểm công thức. Sửa ở chặng A, phối hợp B.1 tuần 2–4.',
r'Mô hình cước giả định: 20 nghìn đồng cho 1 km đầu; phần vượt 1 km là 12 nghìn đồng/km, theo độ dài thực, không phụ phí. Với d≥1 và ngân sách 80 nghìn đồng, lập công thức và tìm d lớn nhất; kiểm kết quả.',
r'$C(d)=20+12(d-1)$; lớn nhất 6 km.',
r'Bất phương trình $20+12(d-1)\leq80$ cho d≤6. Kết hợp d≥1 được [1;6]. Thế d=6 cho $20+12\cdot5=80$ nghìn đồng; giá tăng nên không thể đi xa hơn.',
r'Kiểm tại d=1 và ngưỡng ngân sách; giải bất phương trình chính xác, giữ đơn vị nghìn đồng.')
add(8,3,r'Chọn phương án khả thi',
r'Tự chọn công cụ để tối ưu trên một tập nghiệm nguyên hữu hạn.',
r'Lớp 10: hệ bất phương trình hai ẩn; lập bảng hữu hạn, số nguyên không âm.',
r'B03, B42; N: B02',r'R1; N',r'79',r'S10.1 Bài 4, tr.in 27 / PDF 28. Ràng buộc nguyên và vét cạn nhỏ là thiết kế ZO Math cho bối cảnh, không yêu cầu lí thuyết tối ưu nguyên.',
r'Giải thích/phối hợp: xây mô hình và chứng minh đã xét đủ ứng viên khả thi.',r'Mô hình hóa; giải quyết vấn đề; lập luận',r'Tự luận ngắn',7,
r'''Một nhóm làm hai loại bộ quà A và B. Dữ liệu cho một bộ:

| Loại | Vật liệu (đơn vị) | Thời gian (giờ) | Lãi (nghìn đồng) |
|:---|:---:|:---:|:---:|
| A | 2 | 1 | 30 |
| B | 1 | 2 | 40 |

Có tối đa 8 đơn vị vật liệu và 8 giờ. Chỉ làm số nguyên không âm các bộ; tất cả bộ làm ra đều bán được, lãi cộng theo bảng. Hãy tìm số bộ mỗi loại để tổng lãi lớn nhất. Em tự chọn cách giải, viết các ràng buộc và giải thích vì sao không bỏ sót phương án tốt hơn.''',
r'2 bộ A, 3 bộ B; lãi lớn nhất 180 nghìn đồng.',
r'''Đặt x,y là số bộ A,B. Cần $x,y\in\mathbb Z_{\geq0}$, $2x+y\leq8$, $x+2y\leq8$; tối đa hóa $L=30x+40y$ (nghìn đồng).

Vì x≤4, chỉ xét x=0,1,2,3,4. Với x cố định, lãi tăng theo y nên chỉ cần y nguyên lớn nhất thỏa cả hai ràng buộc:

| x | y lớn nhất | L (nghìn đồng) |
|:---:|:---:|:---:|
| 0 | 4 | 160 |
| 1 | 3 | 150 |
| 2 | 3 | 180 |
| 3 | 2 | 170 |
| 4 | 0 | 120 |

Lớn nhất là 180 tại (2;3); dùng 7 đơn vị vật liệu và 8 giờ, thỏa giới hạn. Bảng xét đủ mọi x khả thi và y tốt nhất tương ứng, nên chứng minh được tối ưu. Giao hai đường biên cho x=y=8/3 nhưng đây không phải số bộ nguyên, không được dùng làm đáp án hay làm tròn tùy ý.''',
[r'Lập đủ hai ràng buộc, miền nguyên không âm, hàm lãi.',r'Tìm (2;3), kiểm khả thi và chứng minh xét đủ; chấp nhận cách đúng khác.'],
r'ĐK: bỏ miền nguyên; PP: chỉ tìm giao hai đường hoặc chỉ thử vài phương án không chứng minh đủ; ĐỌC: nhầm loại nguồn lực.',
r'Ôn S10.1 tr.27; lập bảng từ giới hạn x và tối đa y. Sửa nền ở A; phối hợp R8 trong B và luyện tổng hợp ở C1 tuần 19–22 khi đã đủ nền.',
r'''Giữ nguyên dữ liệu một bộ A (2 vật liệu, 1 giờ, lãi 30 nghìn) và B (1 vật liệu, 2 giờ, lãi 40 nghìn), nhưng có tối đa 7 vật liệu và 7 giờ. Số bộ nguyên không âm, đều bán được. Tìm phương án lãi lớn nhất và chứng minh xét đủ.''',
r'1 bộ A, 3 bộ B; lãi lớn nhất 150 nghìn đồng.',
r'Ràng buộc $2x+y\leq7$, $x+2y\leq7$, x,y nguyên không âm. Chỉ có x=0,1,2,3. Với mỗi x, y lớn nhất lần lượt là 3,3,2,1; lãi lần lượt 120,150,140,130. Vậy (1;3) cho lớn nhất 150, dùng 5 vật liệu và 7 giờ. Đã xét đủ x và chọn y tốt nhất vì hệ số lãi của y dương.',
r'Vét cạn toàn bộ cặp nguyên không âm trong hộp 0≤x,y≤8 (gốc), 0≤x,y≤7 (thử lại); lọc hai ràng buộc, đối chiếu bảng rút gọn và nghiệm tối ưu duy nhất.')

assert len(items)==24
(ROOT/r'D0_ngan_hang_v1.0.json').write_text(json.dumps({r'version':r'1.0',r'date':r'2026-09-09',r'plan':r'0.5',r'items':items},ensure_ascii=False,indent=2))
