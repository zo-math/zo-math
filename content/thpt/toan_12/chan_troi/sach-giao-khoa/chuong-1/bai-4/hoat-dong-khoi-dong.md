Để vẽ đồ thị của hàm số $C(v) = \frac{16000}{v} + \frac{5}{2}v$ với $0 < v \leq 120$, có thể bắt đầu bằng một cách làm trực tiếp và quen thuộc: chọn một số giá trị cụ thể của $v$, tính giá trị tương ứng $C(v)$, sau đó chấm các điểm thu được và nối lại để hình dung đồ thị. Để có bối cảnh tư duy vững chắc, cần hiểu rõ ý nghĩa thực tế của hai đại lượng $v$ và $C$:

- $v$ là *tốc độ trung bình* của chuyến đi, tính bằng km/h.
- $C(v)$ là *chi phí tiền xăng* cho toàn bộ chuyến đi, tính bằng đồng. Quan sát dòng đầu tiên trong bảng trên, với tốc độ $20$ km/h, chi phí tương ứng là $850$ đồng - nếu được hiểu là tiền xăng đi mỗi km dành cho một xe gắn máy thông thường thì khá hợp lý.

Hãy quản lý các điểm bằng cách lập bảng giá trị như sau:

| $v$ <br> (km/h) | $\dfrac{16000}{v}$ | $\dfrac{5}{2}v$ | $C(v)$ <br> (đồng) |
| :--------: | :----------------: | :-------------: | :-----------: |
|     20     |        800         |       50        |      850      |
|     40     |        400         |       100       |      500      |
|     60     |       266.67       |       150       |    416.67     |
|     80     |        200         |       200       |      400      |
|    100     |        160         |       250       |      410      |
|    120     |       133.33       |       300       |    433.33     |

Mỗi hàng trong bảng tương ứng với một cặp tọa độ $(v, C(v))$ trên mặt phẳng, thể hiện chi phí tương ứng với một mức tốc độ cụ thể. Khi chấm các điểm này và nối chúng lại, dạng đường cong hiện ra, phản ánh *quy luật thay đổi của chi phí theo tốc độ* - ban đầu giảm rồi tăng.

![Đồ thị hàm số C(v)= \frac{16000}{v} +\frac{5}{2}v.](/figures/toan-thpt/toan-12/chan-troi/sach-giao-khoa/chuong-1/bai-4/hdkd-do-thi-diem.svg){width=350px}

Cách làm này giúp hình thành trực giác ban đầu về hình dạng đồ thị. Mỗi điểm thu được là một vị trí trên mặt phẳng tọa độ, biểu diễn mối quan hệ giữa tốc độ và chi phí. Tuy nhiên, việc chỉ chấm vài điểm không thể đem lại một đồ thị chính xác. Dù có chọn thêm nhiều giá trị của $v$, chấm thêm nhiều điểm và nối lại thật mịn, thì vẫn chưa thể đảm bảo rằng đường cong ấy *không đổi hướng đột ngột ở đâu đó giữa các điểm chưa xét*.

Đây là giới hạn tự nhiên của cách làm thực nghiệm: *nó chỉ cho thấy điều quan sát được*, chứ chưa khẳng định được đặc trưng hình học ổn định của đồ thị. Muốn vẽ một đường cong phản ánh đúng quy luật vận động nội tại của hàm số - *liền mạch, trơn tru và đi theo một xu hướng nhất định* - cần có sự đảm bảo bằng lý luận toán học. Chính vì thế, việc khảo sát tính liên tục và chiều biến thiên là thiết yếu.

Hàm số $C(v)$ gồm hai thành phần có xu hướng đối lập:

- Thành phần $\frac{16000}{v}$ đại diện cho *khoản chi phí tỉ lệ nghịch với tốc độ*, cho thấy nếu đi càng chậm ($v$ nhỏ), thời gian di chuyển sẽ dài hơn và tiêu tốn nhiều nhiên liệu hơn - dẫn đến chi phí cao.
- Thành phần $\frac{5}{2}v$ là *khoản chi phí tỉ lệ thuận với tốc độ*, phản ánh rằng tốc độ cao khiến động cơ hoạt động mạnh hơn và tiêu hao nhiên liệu nhiều hơn theo thời gian - làm chi phí cũng tăng.

Khi kết hợp hai yếu tố này, tổng chi phí $C(v)$ sẽ giảm dần khi tốc độ còn thấp, nhưng sau đó tăng trở lại khi tốc độ cao hơn. Sự thay đổi này không đều một chiều, mà có một mức tốc độ tối ưu tại đó chi phí đạt thấp nhất. Đây là điều cần được thể hiện và xác nhận rõ bằng phân tích toán học.

Hàm số $C(v)$ có đạo hàm là

$$
    C'(v) 
        = -\frac{16000}{v^2} + \frac{5}{2}.
$$

Phương trình $C'(v) = 0$ có nghiệm $v=80$. Dấu của đạo hàm $C^\prime(v)$ và chiều biến thiên của hàm số $C(v)$ được xác định như sau:

- Vì $C'(v) < 0$ với $v\in (0;80)$, nên hàm $C(v)$ giảm trên khoảng này.
- Vì $C'(v) > 0$ với $v\in (80;120)$, nên hàm $C(v)$ tăng trên khoảng này.

Vì đạo hàm đổi dấu từ âm sang dương tại $v=80$, nên đây là điểm cực tiểu của hàm số, giá trị cực tiểu là $C(80)=400$. Hơn nữa, giá trị cực tiểu này cũng là giá trị nhỏ nhất của hàm số:

$$
    \min_{(0;120]}C(v)
        =C(80)
        =400.
$$

Vì đã biết hàm số liên tục, có đạo hàm và có một điểm cực tiểu duy nhất tại $v=80$, nên chỉ cần chấm vài điểm then chốt rồi nối lại bằng một đường cong trơn tru đi xuống đến $v=80$ rồi đi lên, ta sẽ thu được hình dạng đúng của đồ thị.

Điều quan trọng nằm ở chỗ này: chính hiểu biết toán học về tính liên tục, chiều biến thiên và cực trị mới bảo đảm được đường cong ấy phản ánh đúng bản chất của hàm số, chứ không phải độ dày đặc hay sự mượt mà của các điểm được chấm. Có thể thêm nhiều điểm đến mức gần như "liền mạch", nhưng nếu không chứng minh được hàm luôn đi theo một xu hướng, thì vẫn không loại trừ được khả năng nó đổi hướng bất ngờ giữa các điểm chưa xét.

Đó là giới hạn tất yếu của cách làm thực nghiệm. Chỉ khi có một lý luận toán học dẫn đường, mới có thể khẳng định rằng đường nối giữa các điểm không chỉ đẹp mắt mà còn đúng về mặt cấu trúc.

Kết quả toán học này cũng mang lại một ý nghĩa thực tế quan trọng: muốn chi phí xăng thấp nhất, nên đi với vận tốc khoảng $80$ km/h. Nhưng nếu đi quá chậm để tiết kiệm hơn nữa, thời gian di chuyển sẽ kéo dài - điều không phải lúc nào cũng chấp nhận được. Ngược lại, đi quá nhanh tuy rút ngắn thời gian nhưng lại làm chi phí tăng vọt.

Phân tích đồ thị vì vậy không chỉ là thao tác toán học, mà còn là công cụ để *cân nhắc giữa hai yếu tố quan trọng trong thực tế*: *chi phí* và *thời gian di chuyển*.
