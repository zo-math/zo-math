---
title: "Vì sao đồ thị hàm số được vẽ bằng hai trục vuông góc?"
series: "Vì sao?"
project: "ZO Math"
script_type: "Kịch bản lời dẫn"
style: "Độc thoại tự vấn học thuật"
version: "v0.1"
status: "Hoàn thành"
source_qmd: "vi_sao_do_thi_duoc_ve_bang_hai_truc_vuong_goc.qmd"
updated: "2026-06-25"
---

# VÌ SAO ĐỒ THỊ HÀM SỐ ĐƯỢC VẼ BẰNG HAI TRỤC VUÔNG GÓC?

## C01. Tự vấn

> **Mô tả.** Biến một hình ảnh quá quen thuộc thành một vấn đề cần được hiểu.
>
> Cảnh này chưa giải thích vì sao đồ thị dùng hai trục vuông góc.
>
> Cảnh này chỉ làm rõ: ta không nên xem điều đó là hiển nhiên.

### C01-01

Khi gặp một hàm số, mình thường nghĩ ngay đến đồ thị của nó.

Một trục ngang.

Một trục dọc.

Hai trục vuông góc với nhau.

Và trên đó, một đường cong được vẽ ra.

### C01-02

Hình ảnh ấy quen thuộc đến mức mình từng không còn thấy có gì cần hỏi về nó.

Thầy cô vẽ như vậy.

Sách giáo khoa vẽ như vậy.

Các bài giải cũng vẽ như vậy.

Lâu dần, mình mặc nhiên nghĩ rằng: đã nói đến đồ thị hàm số thì phải có hai trục vuông góc và một đường cong.

### C01-03

Nhưng một điều quen thuộc không có nghĩa là nó đã được hiểu.

Nếu mình chỉ làm theo, đồ thị sẽ trở thành một thủ tục.

Lập bảng giá trị.

Chấm vài điểm.

Rồi nối chúng lại.

### C01-04

Thủ tục ấy có thể đúng.

Nhưng nó chưa trả lời câu hỏi sâu hơn.

Vì sao ta lại làm như vậy?

Vì sao phải có hai trục?

Và vì sao hai trục ấy lại vuông góc?

## C02. Biến đầu vào $x$ và biến phụ thuộc $y$

> **Mô tả.** Đặt người xem vào tình huống ban đầu: có một hàm số, có các giá trị $x$ được chọn, và có các giá trị $y$ được tính ra từ công thức.
>
> Cảnh này làm rõ sự khác nhau giữa hai vai trò:
>
> $x$ là giá trị mình đưa vào.
>
> $y$ là giá trị công thức trả lại.
>
> Từ bảng số thu được, cảnh này làm xuất hiện nhu cầu quan sát sự phụ thuộc của $y$ vào $x$ một cách rõ hơn.

### C02-01

Trong bài này, mình sẽ đi cùng hàm số

$$
y = x^3 - 3x.
$$

### C02-02

Mình thử chọn một số giá trị của $x$.

Từ $-2.5$ đến $2.5$.

Mỗi lần tăng thêm $0.5$.

Cách chọn này tạo ra một nhịp đều cho $x$.

Nhờ vậy, mình dễ theo dõi hơn điều gì xảy ra với $y$.

### C02-03

Bây giờ, mình thay từng giá trị $x$ vào công thức.

Mỗi lần thay vào, mình nhận được một giá trị $y$.

Các kết quả ấy tạo thành một bảng.

Một cột là những giá trị $x$ mình đã chọn.

Một cột là những giá trị $y$ công thức trả lại.

### C02-04

Nhìn vào bảng, mình thấy hai cột số này không vận động giống nhau.

Cột $x$ đi rất đều.

Mỗi dòng tăng thêm $0.5$.

Nhưng cột $y$ không đi theo nhịp đều ấy.

### C02-05

Khi $x$ đi từ $-2.5$ đến $-1$, $y$ tăng từ $-8.125$ lên $2$.

Khi $x$ tiếp tục đi đến $1$, $y$ lại giảm xuống $-2$.

Rồi khi $x$ đi đến $2.5$, $y$ tăng trở lại đến $8.125$.

### C02-06

Như vậy, mình có thể cho $x$ thay đổi theo một nhịp do mình chọn.

Nhưng mình không thể bắt $y$ thay đổi theo nhịp ấy.

$y$ phụ thuộc vào $x$ thông qua công thức.

Và chính sự phụ thuộc này mới là điều mình muốn quan sát.

### C02-07

Bảng số ghi lại các kết quả một cách chính xác.

Nhưng nó chưa giúp mình thấy sự phụ thuộc ấy thật rõ.

Muốn biết $y$ tăng hay giảm, mình phải đọc từng dòng.

Muốn biết $y$ đổi chiều ở đâu, mình phải so sánh nhiều dòng liên tiếp.

Muốn hình dung toàn bộ sự thay đổi, mình phải tự ráp các con số ấy lại trong đầu.

### C02-08

Đến đây, nhu cầu thật sự xuất hiện.

Mình không chỉ muốn biết từng cặp giá trị $(x,y)$.

Mình muốn thấy dáng điệu biến thiên của $y$ khi $x$ thay đổi.

Vì vậy, mình cần một cách biểu diễn khác.

Cách ấy phải giữ được thứ tự thay đổi của $x$.

Đồng thời, nó phải cho thấy giá trị $y$ tương ứng tại mỗi $x$.

Nói cách khác, mình cần đặt vai trò đầu vào của $x$ và sự phụ thuộc của $y$ vào cùng một điểm nhìn.

## C03. Trục thứ nhất: $x$

> **Mô tả.** Bắt đầu chuyển bảng số thành một cấu trúc hình học.
>
> Cảnh này làm ba việc:
>
> - đặt các giá trị $x$ theo thứ tự trên một đường ngang;
> - từ mỗi mốc $x$, biểu diễn giá trị $y$ bằng một đoạn có hướng lên hoặc xuống;
> - làm lộ ra vì sao phương vuông góc là phương tự nhiên để mang giá trị $y$.
>
> Đến cuối cảnh, mỗi cặp số $(x,y)$ không còn chỉ là hai con số trong bảng.
> Nó đã bắt đầu trở thành một dấu hiệu hình học.

### C03-01

Mình bắt đầu từ những giá trị $x$ đã chọn.

Chúng không lộn xộn.

Chúng có một thứ tự.

$-2.5$ đứng trước $-2.0$.

$-2.0$ đứng trước $-1.5$.

Rồi cứ thế cho đến $2.5$.

### C03-02

Vì có thứ tự như vậy, mình đặt các giá trị ấy lên một đường ngang.

Từ trái sang phải.

Nhỏ ở bên trái.

Lớn ở bên phải.

Bằng cách này, thứ tự của $x$ được giữ lại trong hình.

### C03-03

Đường ngang ấy, mình gọi là trục $x$.

Trục này không chỉ giúp mình sắp xếp các giá trị $x$ từ nhỏ đến lớn.

Nó còn gợi ra rằng giữa các mốc mình đã chọn, vẫn còn những giá trị khác.

Và ở mỗi mốc trên trục ấy, mình đều có thể đặt một câu hỏi.

Nếu $x$ bằng chừng này, thì $y$ bằng bao nhiêu?

### C03-04

Đến đây, phần câu hỏi đã có chỗ đứng của nó.

Nhưng mỗi câu hỏi còn cần một câu trả lời.

Tại từng mốc $x$, mình cần đưa giá trị $y$ vào hình.

### C03-05

Nếu $y$ dương, mình dựng một đoạn đi lên từ mốc $x$.

Nếu $y$ âm, mình dựng một đoạn đi xuống từ mốc $x$.

Nếu $y = 0$, đoạn ấy không vươn lên cũng không hạ xuống.

Nó nằm ngay trên đường ngang.

### C03-06

Với cách làm này, mỗi giá trị $y$ vẫn bám vào đúng giá trị $x$ đã sinh ra nó.

Mình không bị lẫn.

$y$ nào thuộc về $x$ nào, mình đều nhìn ra được.

Mốc trên đường ngang cho biết mình đã chọn giá trị $x$ nào.

Đoạn dựng lên hoặc hạ xuống cho biết công thức trả lại giá trị $y$ nào.

### C03-07

Đến đây, mình bắt đầu thấy rõ một điều.

Nếu đường ngang đã được dùng để sắp xếp các giá trị $x$,

thì phương tự nhiên nhất để biểu diễn $y$ là phương dọc.

Mình đi lên và đi xuống để thay đổi độ cao,

nhưng không làm thay đổi vị trí ngang đã chọn.

### C03-08

Chính ở đây, sự vuông góc bắt đầu có lý do của nó.

Mình cần một phương mới để biểu diễn $y$.

Nhưng phương mới ấy phải tách bạch khỏi phương đang dùng cho $x$.

Nó phải cho phép mình thay đổi giá trị biểu diễn của $y$,

mà vẫn giữ nguyên mốc $x$.

### C03-09

Mình còn thấy thêm một điều nữa.

Tại mỗi mốc trên đường ngang, chỉ có một phương vuông góc với nó.

Còn nếu dùng một phương xiên, mình sẽ có vô số cách chọn.

Khi đó, mình lại phải hỏi thêm:

vì sao là góc này, mà không phải góc khác?

### C03-10

Với phương thẳng đứng, sự lựa chọn ấy không còn tùy tiện nữa.

Nó gắn trực tiếp với nhu cầu đang có.

Giữ nguyên nơi mình đã đặt $x$.

Và từ đúng nơi ấy, biểu diễn giá trị $y$.

### C03-11

Đến đây, bảng số đã bắt đầu đổi dạng.

Các giá trị $y$ không còn nằm yên trong một cột số.

Chúng trở thành những đoạn dài ngắn khác nhau.

Có đoạn hướng lên.

Có đoạn hướng xuống.

Và mỗi đoạn đều gắn với một giá trị $x$ cụ thể.

### C03-12

Như vậy, mỗi cặp số trong bảng không còn chỉ là hai con số.

Nó đã trở thành một dấu hiệu hình học.

Tại vị trí $x$ này,

giá trị $y$ được biểu diễn bằng một độ cao có dấu.

## C04. Điểm $(x,y)$ và đường cong

> **Mô tả.** Đi từ các đoạn biểu diễn $y$ đến phần thông tin thật sự cần giữ lại: đầu mút của mỗi đoạn.
>
> Cảnh này làm bốn việc:
>
> - nhận ra đầu mút là nơi cô đọng thông tin của mỗi cặp số;
> - giữ lại các đầu mút để thu được một dãy điểm;
> - từ dãy điểm, bắt đầu thấy xu hướng và một vài đối xứng;
> - đặt câu hỏi về khoảng trống giữa các điểm, rồi để từ đó xuất hiện đường cong.
>
> Đến cuối cảnh, bảng số không còn chỉ được nhìn như các dòng rời rạc.
> Nó đã hiện ra như một hình dạng đang được hình thành.

### C04-01

Nhìn các đoạn thẳng ấy một lúc, mình nhận ra rằng phần thật sự cần nhìn là đầu mút của mỗi đoạn.

Không phải vì các đoạn ấy vô ích.

Chính chúng đã giúp mình đưa giá trị $y$ ra khỏi bảng số.

Nhưng sau khi làm xong việc ấy, phần còn lại mang thông tin mình cần chính là đầu mút.

### C04-02

Ở đầu mút ấy, mình biết được hai điều cùng một lúc.

Mình biết giá trị $x$ đã được chọn ở đâu.

Và mình biết giá trị $y$ đang nằm ở mức nào.

Nói cách khác, một đầu mút giữ lại trọn vẹn thông tin của một cặp số.

### C04-03

Nếu chỉ giữ các đầu mút, mình thu được một dãy điểm.

Mỗi điểm ứng với một cặp giá trị trong bảng.

Giá trị $x$ cho biết điểm ấy nằm ở đâu theo chiều ngang.

Giá trị $y$ cho biết điểm ấy ở cao hay thấp.

Đó là lý do mình có thể gọi chúng là các điểm $(x,y)$.

### C04-04

Đến đây, hình bắt đầu gọn hơn.

Nếu mình cứ giữ tất cả các đoạn thẳng, hình vẽ sẽ sớm trở nên dày và rối khi số giá trị $x$ tăng lên.

Còn các điểm thì khác.

Chúng vẫn giữ lại hai thông tin quan trọng nhất.

Tại giá trị $x$ này, giá trị $y$ ở mức nào.

### C04-05

Và khi nhìn các điểm ấy, mắt mình bắt đầu thấy điều mà bảng số không cho thấy ngay.

Các điểm bên trái đi lên.

Rồi chúng quay xuống.

Sau đó, chúng lại đi lên.

Một xu hướng bắt đầu lộ ra.

### C04-06

Một vài sự cân xứng cũng bắt đầu hiện ra.

Điểm ứng với $x=-1$ và $y=2$ nằm đối xứng với điểm ứng với $x=1$ và $y=-2$ qua điểm ứng với $x=0$ và $y=0$.

Điểm ứng với $x=-2.5$ và $y=-8.125$ cũng đối xứng với điểm ứng với $x=2.5$ và $y=8.125$ qua điểm ấy.

Nói cách khác, khi đổi $x$ thành $-x$, giá trị $y$ cũng đổi dấu.

Những điểm bên trái và bên phải không xuất hiện ngẫu nhiên.

Chúng đang gợi ra một sự cân xứng quanh vị trí trung tâm.

### C04-07

Như vậy, các điểm không còn buộc mình phải đọc từng dòng của bảng nữa.

Mình bắt đầu nhìn thấy hình dạng chung của sự thay đổi.

Nhưng đến đây lại xuất hiện một câu hỏi tự nhiên.

Mình mới chỉ có một số điểm.

Thế còn khoảng trống giữa hai điểm thì sao?

### C04-08

Ban đầu, mình chỉ chọn một số giá trị $x$ để lập bảng.

Nhưng hàm số không chỉ có bấy nhiêu giá trị ấy.

Giữa $-2.5$ và $-2$ còn rất nhiều giá trị khác của $x$.

Giữa $-2$ và $-1.5$ cũng vậy.

Và với mỗi giá trị ấy, công thức vẫn cho một giá trị $y$ tương ứng.

### C04-09

Điều đó có nghĩa là nếu mình chọn thêm nhiều giá trị $x$ hơn, thì sẽ có thêm nhiều điểm xuất hiện.

Các điểm sẽ ngày một dày hơn.

Khoảng cách giữa chúng sẽ ngày một nhỏ hơn.

Và khi các giá trị $x$ được chọn ngày càng sát nhau, dãy điểm ấy bắt đầu gợi ra một đường cong.

### C04-10

Đường cong ấy không thêm thông tin gì xa lạ.

Nó chỉ làm hiện rõ điều đã có sẵn trong hàm số.

Bảng cho mình các kết quả theo từng dòng.

Còn đường cong cho mình thấy dáng điệu chung của sự thay đổi ấy trong một cái nhìn.

## C05. Trục thứ hai: $y$

> **Mô tả.** Từ đường cong đã hình thành, làm xuất hiện nhu cầu về một trục đo chung cho các giá trị $y$.
>
> Cảnh này làm bốn việc:
>
> - chỉ ra rằng đường cong cho thấy dáng điệu chung, nhưng chưa đủ để đọc giá trị $y$ một cách thống nhất;
> - giải thích vì sao không thể giữ mãi các đoạn dựng đứng hoặc ghi nhãn $y$ cho mọi điểm;
> - dựng trục $y$ như một thước đo chung cho độ cao;
> - làm rõ bản chất của hệ trục vuông góc: không phải $x$ và $y$ độc lập về giá trị, mà là hai phương đo được tách bạch.

### C05-01

Đường cong vừa hiện ra đã giúp mình nhìn thấy dáng điệu chung của sự thay đổi.

Từ bên trái, nó đi lên.

Rồi quay xuống.

Sau đó lại đi lên.

Nhưng hình ảnh ấy vẫn còn thiếu một điều quan trọng.

Mình cần đọc được giá trị $y$ tại một điểm bất kì theo một cách thống nhất.

### C05-02

Ở các bước trước, mỗi giá trị $y$ được biểu diễn bằng một đoạn đi lên hoặc đi xuống từ mốc $x$.

Cách ấy rất có ích.

Nó giúp mình đưa $y$ ra khỏi bảng số.

Nó cũng giúp mình thấy giá trị $y$ đang cao hay thấp so với đường ngang.

### C05-03

Nhưng khi các điểm ngày càng nhiều, mình không thể giữ mãi tất cả các đoạn dựng đứng.

Hình vẽ sẽ nhanh chóng trở nên dày và rối.

Mình cũng không thể ghi giá trị $y$ bên cạnh mọi điểm.

Càng nhiều điểm, việc ghi nhãn càng làm mờ đi hình dạng chính mà mình muốn nhìn.

### C05-04

Vì vậy, mình cần một thước đo chung cho các giá trị $y$.

Thước đo ấy không thuộc riêng một điểm nào.

Nó phải cho phép mình đọc độ cao của mọi điểm theo cùng một mốc.

Khi ấy, mỗi điểm trên đường cong không cần mang theo nhãn riêng.

Mình vẫn có thể biết nó ứng với giá trị $y$ nào.

### C05-05

Thước đo chung ấy được đặt theo phương thẳng đứng.

Mình gọi nó là trục $y$.

Từ một điểm trên đường cong, mình có thể nhìn ngang sang trục này để đọc giá trị $y$ của điểm đó.

Nhờ vậy, các độ cao khác nhau được so sánh trong cùng một hệ đo.

### C05-06

Nhưng trục đo ấy nên được đặt ở đâu?

Nếu chỉ cần một thước đo độ cao, mình có thể đặt nó ở bên trái.

Hoặc bên phải.

Hoặc gần một mốc $x$ nào đó.

Những cách đặt ấy đều có thể giúp mình đọc độ cao.

Nhưng chúng lại gắn trục dọc với một vị trí ngang có phần tùy tiện.

### C05-07

Khi đường thẳng đứng này trở thành trục của cả hình vẽ, nó không nên đi qua một giá trị $x$ bất kì.

Nó cần đi qua mốc gốc của trục ngang.

Tức là đi qua vị trí $x=0$.

Ở đó, phép đo theo chiều ngang có điểm bắt đầu tự nhiên của nó.

Không lệch sang trái.

Cũng không lệch sang phải.

### C05-08

Còn theo chiều dọc, giá trị $y=0$ là mốc không cao lên và cũng không thấp xuống.

Khi trục dọc đi qua vị trí $x=0$, hai mốc này gặp nhau tại cùng một điểm.

Điểm ấy vừa có $x=0$,

vừa có $y=0$.

Đó là gốc chung của hai phép đo.

### C05-09

Từ lúc này, hình vẽ có hai trục đo rõ ràng.

Đường ngang giúp mình đọc giá trị $x$.

Đường dọc giúp mình đọc giá trị $y$.

Một điểm trên hình được hiểu bằng hai thao tác.

Nhìn xuống đường ngang để biết nó ứng với giá trị $x$ nào.

Nhìn sang đường dọc để biết giá trị $y$ tương ứng là bao nhiêu.

### C05-10

Đây là chỗ cần phân biệt cẩn thận.

Trong hàm số, $y$ vẫn phụ thuộc vào $x$.

Mình chọn $x$.

Công thức trả lại $y$.

Vì vậy, không nên hiểu rằng $x$ và $y$ độc lập với nhau về giá trị.

### C05-11

Điều được tách bạch ở đây là hai phương đo.

Phương ngang dùng để đi qua các giá trị đầu vào $x$.

Phương dọc dùng để đo các giá trị $y$ mà công thức trả lại.

Khi đi ngang, mình thay đổi vị trí $x$ mà không thay đổi độ cao.

Khi đi dọc, mình thay đổi độ cao mà không làm lệch vị trí $x$ đang xét.

### C05-12

Chính sự tách bạch ấy làm cho hai trục vuông góc trở nên tự nhiên.

Một hướng dùng để sắp xếp các giá trị đầu vào.

Một hướng dùng để đo các giá trị phụ thuộc.

Hai công việc không bị trộn vào nhau.

### C05-13

Vì vậy, hai trục vuông góc không xuất hiện như một thói quen vẽ hình vô cớ.

Chúng xuất hiện từ nhu cầu quan sát hàm số.

Mình cần một trục để sắp xếp các giá trị $x$.

Mình cần một trục để đo các giá trị $y$.

Và mình cần một điểm gốc chung để cả hai phép đo cùng bắt đầu từ một nơi.

Từ gốc ấy, lệch sang trái hay sang phải cho biết giá trị $x$.

Cao lên hay thấp xuống cho biết giá trị $y$.

Nhờ vậy, mỗi điểm trên hình có thể được đọc một cách thống nhất như một cặp giá trị $(x,y)$.

## C06. Hình ảnh của sự biến thiên

> **Mô tả.** Nhìn lại toàn bộ quá trình vừa đi qua.
>
> Cảnh này làm rõ rằng bảng giá trị và đồ thị không thay thế nhau.
> Chúng làm hai công việc khác nhau:
>
> - bảng giữ các kết quả cụ thể;
> - đồ thị cho thấy hình ảnh tổng thể của sự biến thiên.
>
> Đến cuối cảnh, định nghĩa đồ thị mới được gọi tên như kết quả tự nhiên của quá trình đã kiến tạo.

### C06-01

Đến đây, mình nhìn lại bảng giá trị.

Bảng vẫn có vai trò của bảng.

Nó cho mình các giá trị cụ thể.

Nếu muốn biết tại $x=2.5$ thì $y$ bằng bao nhiêu, bảng trả lời ngay.

Khi đó, $y=8.125$.

Mỗi dòng của bảng là một câu trả lời chính xác của hàm số.

### C06-02

Nhưng điều mình đi tìm từ đầu không chỉ là từng câu trả lời riêng lẻ.

Mình muốn biết $y$ thay đổi như thế nào khi $x$ thay đổi.

Muốn thấy điều đó trong bảng, mình phải đọc nhiều dòng liên tiếp.

Phải so sánh các giá trị $y$.

Rồi phải tự ráp chúng lại trong đầu để hình dung hướng đi chung.

### C06-03

Hình vừa được tạo ra làm việc ấy theo một cách trực quan hơn.

Khi mỗi cặp giá trị $(x,y)$ được đặt thành một điểm trong hệ hai trục,

mắt mình không chỉ thấy từng giá trị riêng lẻ.

Mình còn thấy cách các giá trị ấy nối nhau thành một hình dạng.

### C06-04

Với hàm số

$$
y = x^3 - 3x,
$$

bảng cho mình biết từng cặp số.

Còn hình trên hai trục cho mình thấy một chuyển động chung.

Từ bên trái, các điểm đi lên.

Sau đó quay xuống.

Rồi lại đi lên.

### C06-05

Những điều ấy không phải tự nhiên xuất hiện thêm từ bên ngoài.

Chúng vốn đã có trong bảng.

Nhưng trong bảng, chúng bị giấu trong các dòng số.

Khi được đặt thành điểm và nhìn cùng nhau, chúng hiện ra trước mắt.

### C06-06

Vì vậy, đồ thị không thay thế bảng giá trị.

Nó làm một việc khác.

Bảng giữ sự chính xác của từng kết quả.

Đồ thị cho mình hình ảnh tổng thể của sự biến thiên.

### C06-07

Có thể nói, đồ thị là cách nhìn cùng một lúc rất nhiều câu trả lời của hàm số.

Mỗi điểm trên đường cong vẫn ứng với một cặp giá trị $(x,y)$.

Nhưng toàn bộ đường cong cho mình thấy cách $y$ đi theo $x$.

### C06-08

Bây giờ, định nghĩa quen thuộc mới trở nên tự nhiên.

Với một hàm số $y=f(x)$,

đồ thị của nó là tập hợp các điểm có dạng $(x,f(x))$ trong mặt phẳng tọa độ.

Nhưng ở đây, mình không đi từ định nghĩa ấy.

Mình đi từ nhu cầu nhìn thấy sự biến thiên.

Rồi từ nhu cầu ấy, định nghĩa tự hiện ra như một cách nói gọn.

## C07. Kết tinh

> **Mô tả.** Trở lại câu hỏi ban đầu và kết tinh toàn bộ quá trình kiến tạo.
>
> Cảnh này không giải thích thêm bằng ví dụ mới.
> Cảnh này gom lại những gì đã xuất hiện:
>
> - $x$ là giá trị được chọn;
> - $y$ là giá trị được trả lại;
> - trục ngang giữ thứ tự của $x$;
> - phương thẳng đứng biểu diễn $y$ mà không làm lệch mốc $x$;
> - trục $y$ cho một thước đo chung;
> - điểm gốc chung giúp hai phép đo cùng quy chiếu về một nơi.
>
> Kết cảnh cần làm rõ: hai trục vuông góc không phải là một thói quen hình vẽ, mà là câu trả lời tự nhiên cho nhu cầu nhìn thấy sự biến thiên.

### C07-01

Bây giờ, mình có thể trở lại câu hỏi ban đầu.

Vì sao đồ thị hàm số thường được vẽ bằng hai trục vuông góc?

Câu trả lời không bắt đầu từ một quy ước vẽ hình.

Nó bắt đầu từ nhu cầu nhìn thấy sự thay đổi của $y$ khi $x$ thay đổi.

### C07-02

Trong một hàm số, $x$ là giá trị mình chủ động chọn.

Vì vậy, các giá trị $x$ cần được sắp xếp theo một thứ tự rõ ràng.

Mình đặt chúng trên một đường ngang.

Từ trái sang phải.

Nhỏ đến lớn.

Đường ngang ấy giữ vai trò của trục $x$.

### C07-03

Nhưng mỗi giá trị $x$ không đứng một mình.

Khi đưa $x$ vào công thức, mình nhận được một giá trị $y$.

Vì vậy, tại mỗi vị trí $x$, mình cần biểu diễn câu trả lời ấy.

Nếu $y$ dương, nó đi lên.

Nếu $y$ âm, nó đi xuống.

Nếu $y=0$, nó nằm ngay tại mốc ngang.

### C07-04

Độ cao ấy cần được biểu diễn theo một phương không làm lệch vị trí $x$ đang xét.

Khi mình muốn thay đổi giá trị $y$, mình không muốn đồng thời làm thay đổi giá trị $x$.

Vì vậy, từ mỗi mốc $x$, giá trị $y$ được dựng lên hoặc hạ xuống theo phương vuông góc với đường ngang.

### C07-05

Sau đó, khi chỉ giữ lại các đầu mút, mình có các điểm.

Mỗi điểm giữ lại đầy đủ hai thông tin.

Nó nằm ở đâu theo chiều ngang để cho biết $x$.

Và nó cao hay thấp để cho biết $y$.

Một cặp số trong bảng đã trở thành một điểm trong hình.

### C07-06

Khi các điểm ngày càng nhiều, mình không thể ghi riêng giá trị $y$ cho từng điểm.

Mình cần một thước đo chung.

Vì vậy, trục $y$ xuất hiện.

Trục này cho phép mình đọc độ cao của mọi điểm theo cùng một mốc.

### C07-07

Trục $y$ được đặt qua vị trí $x=0$.

Ở đó, mốc gốc của chiều ngang gặp mốc gốc của chiều dọc.

Điểm chung ấy vừa mang $x=0$,

vừa mang $y=0$.

Từ đó, mọi điểm trên hình đều được đọc bằng hai độ lệch so với cùng một gốc.

Lệch ngang bao nhiêu cho biết $x$.

Cao lên hay thấp xuống bao nhiêu cho biết $y$.

### C07-08

Đây là lý do hai trục vuông góc trở nên tự nhiên.

Trục ngang giúp mình đi qua các giá trị đầu vào.

Trục dọc giúp mình đo các giá trị mà hàm số trả lại.

Đi ngang là thay đổi $x$ mà giữ nguyên độ cao.

Đi dọc là thay đổi độ cao mà giữ nguyên vị trí $x$.

Hai công việc được tách ra.

Nhưng chúng vẫn gặp nhau trong cùng một điểm của hình.

### C07-09

Dĩ nhiên, hệ trục vuông góc không phải là cách biểu diễn duy nhất trong toán học.

Nhưng với nhu cầu đang xét ở đây,

nhìn sự biến thiên của một đại lượng $y$ theo một đại lượng $x$,

nó là một cách biểu diễn rất tự nhiên.

Rõ ràng.

Ổn định.

Và dễ đọc.

### C07-10

Khi hiểu như vậy, hai trục vuông góc không còn là một thủ tục phải nhớ.

Chúng trở thành câu trả lời cho một nhu cầu căn bản.

Làm sao để nhìn thấy một đại lượng thay đổi theo một đại lượng khác.

Đó cũng là lúc đồ thị không còn chỉ là một hình vẽ quen thuộc.

Nó trở thành hình ảnh của sự biến thiên.

## C08. Mình đã hiểu chưa?

> **Mô tả.** Dẫn người xem từ việc nghe lời giải thích sang việc tự tái tạo lại con đường tư duy.
>
> Cảnh này không mở thêm kiến thức mới.
> Cảnh này chỉ gợi nhu cầu thực hành và dẫn người xem đến bài viết đầy đủ trên ZO Math.

### C08-01

Nghe đến đây, có thể mình đã hiểu vấn đề.

Nhưng để làm quen với lối tư duy kiến tạo này, mình cần tự đi lại con đường một lần nữa.

Từ bảng số.

Đến các mốc $x$.

Từ các đoạn biểu diễn $y$.

Đến các điểm $(x,y)$.

Rồi đến đường cong của sự biến thiên.

### C08-02

Có vài câu hỏi đáng để tự làm lại.

Nếu chỉ nhìn vào bảng giá trị, mình có thật sự thấy rõ $y$ đang thay đổi như thế nào không?

Khi dựng một đoạn thẳng đứng tại một mốc $x$, thông tin nào được giữ nguyên?

Vì sao sự vuông góc giúp việc đọc $x$ và đọc $y$ không lẫn vào nhau?

### C08-03

Những câu hỏi ấy không chỉ để kiểm tra đáp án.

Chúng giúp mình tự dựng lại lý do của hình vẽ.

Khi tự trả lời được chúng, hai trục vuông góc không còn là một quy tắc phải nhớ.

Chúng trở thành một cấu trúc mình có thể hiểu từ bên trong.

### C08-04

Bài luận đầy đủ, bảng giá trị, hình minh họa và toàn bộ câu hỏi khai thác được đặt trên ZO Math.

Bạn có thể đọc lại chậm hơn.

Tính lại từng giá trị.

Vẽ lại từng bước.

Và tự trả lời câu hỏi ban đầu:

vì sao đồ thị hàm số thường được vẽ bằng hai trục vuông góc?
