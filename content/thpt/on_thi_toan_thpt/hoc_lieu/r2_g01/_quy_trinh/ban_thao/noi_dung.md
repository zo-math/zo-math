# Đọc dữ liệu và đo xu thế trung tâm

**R2-G01 · Bản thảo nội dung 0.2 · 22/10/2026**

_Bản để đọc và góp ý; chưa phải học liệu đã nghiệm thu hoặc phát hành._

<a id="bat-dau"></a>

## Bắt đầu

Một bảng số có thể nói về chiều dài chân chèo của chim cánh cụt, số lượt thuê xe trong ngày hoặc lượng giáng thủy (nước từ mưa, tuyết…) tại một trạm khí tượng. Trước khi tìm một con số đại diện, ta cần biết mỗi số được ghi cho ai, vào lúc nào và bằng đơn vị gì. Sau đó mới có thể hỏi: con số ấy giữ lại điều gì, và làm mờ điều gì?

**Học xong, em cần làm được gì?**

| Mục tiêu | Việc em cần làm được |
|---|---|
| Đọc đúng dữ liệu | Nêu mỗi dòng ghi về đối tượng nào, ghi đại lượng gì, dùng đơn vị nào; đếm số giá trị dùng để tính và nhận ra ô thiếu. |
| Tính trên mẫu gốc | Tính và giải thích số trung bình, trung vị, tứ phân vị, mốt; nhận biết nhiều mốt hoặc không có mốt. |
| Ghép nhóm | Chọn đúng khoảng chứa một giá trị, lập tần số, giá trị đại diện và tần số tích lũy; chỉ ra thông tin bị mất. |
| Tính từ bảng nhóm | Tính số trung bình, trung vị, tứ phân vị và mốt của mẫu ghép nhóm; hiểu chúng được dùng để ước lượng các số đặc trưng của mẫu gốc. |
| Chọn số đại diện | Chọn số phù hợp với câu hỏi; phân biệt mô tả từng nhóm với mô tả mẫu gộp. |
| Giới hạn kết luận | Giữ đúng đơn vị, quy ước làm tròn, ý nghĩa số 0 và phạm vi dữ liệu; sửa kết luận vượt quá bằng chứng. |

**Kiến thức cần có.** Cần biết sắp thứ tự số, tính trung bình cộng và tỉ lệ, đọc khoảng. Không cần dùng đạo hàm. Nếu thiếu thao tác nào, mở đúng phần [Ôn nền](#on-nen), rồi trở về bài đang làm.

**Phạm vi.** Gói này tập trung vào vị trí trung tâm và tứ phân vị. Khoảng biến thiên, khoảng tứ phân vị, phương sai và độ lệch chuẩn sẽ được học riêng. Các dữ liệu thực tế giúp luyện cách đọc và suy nghĩ, không dùng để dự báo hoặc khẳng định một yếu tố là nguyên nhân gây ra yếu tố khác.

### Chọn nơi bắt đầu

- Cần học hoặc học lại: vào [Bài học](#bai-hoc).
- Đã hiểu kiến thức, muốn tự vận dụng: vào [Luyện tập](#luyen-tap).
- Đã chuẩn bị kĩ lưỡng hoặc đủ tự tin: có thể vào thẳng [Kiểm tra](#kiem-tra). Tự tin giúp em chọn điểm vào; bài làm mới cho biết em đã làm được gì.
- Đã hoàn tất lượt chính: thực hiện [Ôn lại](#on-lai) vào ngày đã hẹn.

[Bài học](#bai-hoc) → [Luyện tập](#luyen-tap) → [Kiểm tra](#kiem-tra) → [Ôn lại](#on-lai) là tiến trình khuyến nghị. Em có thể chọn nơi phù hợp; phần bỏ qua không tự được tính là đã đạt.

| Khi cần | Mở phần nào? | Sau đó làm gì? |
|---|---|---|
| Hiểu lại một khái niệm | Đúng mục trong [Bài học](#bai-hoc) | Trở về nhiệm vụ đang vướng |
| Sửa thao tác tính hoặc đọc khoảng | [Ôn nền](#on-nen) | Tự làm bài ngắn ở cuối phần ôn rồi trở về |
| Đối chiếu bài đã làm | [Lời giải](#loi-giai) | Giữ bài ban đầu; dùng [Sửa lỗi](#sua-loi) nếu cần |
| Lưu kết quả và nơi tiếp tục | [Nhật kí](#nhat-ki) | Ghi thông tin đã có, không phải ghi sau mỗi câu |

Trong lúc Kiểm tra, em tự lực trong một lượt, không chia thành nhiều đợt. Nếu cần mở trợ giúp, hãy kết thúc lượt ấy và giữ bài làm ban đầu trước. Phần làm sau khi xem hướng dẫn hoặc được giúp đỡ cần ghi riêng với phần em đã tự làm.

### Thời gian và điều kiện hoàn tất

Lượt chính dự kiến khoảng 4 giờ 05 phút: Khởi động 10 phút, Bài học 100 phút, Luyện tập 75 phút, Kiểm tra 45 phút, đối chiếu và ghi nhận 15 phút. Có thể chia việc học thành nhiều buổi, riêng một lượt Kiểm tra cần làm liền mạch. Ba lượt Ôn lại dự kiến 20 phút mỗi lượt. Ôn nền và Sửa lỗi khi cần có thể thêm khoảng 20–40 phút. Đây là thời gian tham khảo, không phải hạn chót để được công nhận kết quả.

Em hoàn tất lượt học chính khi tự làm được những việc cần đạt ở đầu gói và đã sửa, tự kiểm tra lại những lỗi cản trở việc học tiếp. Không dùng tổng điểm để bù cho một khái niệm còn hiểu sai. Một phép tính nhầm được sửa không làm mất những phần lập luận đúng, nhưng kết quả trước và sau sửa cần phân biệt.

Hẹn ôn sau 2–3 ngày, 7 ngày và 3–4 tuần kể từ khi hoàn tất lượt chính. Có thể học gói tiếp theo phù hợp với kiến thức đang có trong thời gian chờ ôn.

<a id="bai-hoc"></a>

## Bài học

<details>
<summary>Câu hỏi dẫn đường</summary>

**Một con số có thể đại diện cho dữ liệu đến đâu?**

Hãy giữ câu hỏi này khi chuyển từ từng quan sát sang bảng tần số, rồi sang một vài số đặc trưng. Mỗi lần rút gọn dữ liệu, ta có thêm sự dễ đọc nhưng cần biết phần thông tin nào không còn hiện rõ.

</details>

<a id="khoi-dong"></a>

### Khởi động — Đọc số, tính và đọc khoảng

<a id="nv01"></a>

#### Nhiệm vụ 01 — Ba thao tác nền

Ba giá trị đầu trong phần trích Adélie 2007 là $181$, $186$, $195$ mm.

a) Sắp chúng theo thứ tự không giảm và tính trung bình cộng, làm tròn đến một chữ số thập phân.

b) Trong $12$ quan sát, có $3$ quan sát thỏa một điều kiện. Tỉ lệ đó là bao nhiêu phần trăm?

c) Với các khoảng $[180;185)$, $[185;190)$, $[190;195)$, giá trị $190$ thuộc khoảng nào? Viết bất đẳng thức giải thích.

[Xem lời giải](#giai01).

| Bài/điều còn vướng | Phần cần ôn | Trở lại bài |
|---|---|---|
| Tính trung bình hoặc tỉ lệ | [Tính với đủ số quan sát](#nen-tinh) | Nhiệm vụ 01, ý a–b |
| Đầu mút của khoảng | [Đọc khoảng và giữ thứ tự](#nen-khoang) | Nhiệm vụ 01, ý c |

Làm đúng Khởi động cho thấy em đã làm được những thao tác mở đầu này. Các kiến thức còn lại sẽ được học và tự kiểm tra ở những phần sau.

<a id="hoc-doc"></a>

### 1. Mỗi dòng dữ liệu đang nói về điều gì?

#### Gợi mở 01 — Chỗ trống có phải là số 0?

Đoạn đầu của dữ liệu học về chim Adélie năm 2007 có dạng:

| Dòng trong bảng gốc | Loài | Năm | Chiều dài chân chèo, mm |
|---:|---|---:|---:|
| 1 | Adélie | 2007 | $181$ |
| 2 | Adélie | 2007 | $186$ |
| 3 | Adélie | 2007 | $195$ |
| 4 | Adélie | 2007 | Thiếu |
| 5 | Adélie | 2007 | $193$ |

Nếu thay ô thiếu bằng $0$, ta đã thêm một quan sát có nghĩa gì?

Số $0$ sẽ nói rằng chiều dài được ghi là $0$ mm. Trong khi đó, ô thiếu cho biết chưa có số đo chiều dài ở dòng ấy. Hai điều này khác nhau. Khi tính trung bình chiều dài, ta vẫn ghi nhận có một ô thiếu, nhưng chỉ cộng các số đo có sẵn và chia cho số giá trị đã cộng.

Mỗi dòng trong bảng này ghi thông tin của một cá thể chim. Cá thể ấy là **đơn vị quan sát**. Đại lượng được ghi là chiều dài chân chèo; trong thống kê, đại lượng này gọi là **biến**, có đơn vị đo là mm. Số thứ tự dòng giúp tìm lại thông tin trong bảng gốc; nó không phải số đo hoặc mã nhận diện cá thể do nhà nghiên cứu cấp.

Phần Adélie 2007 có $50$ dòng, trong đó có $49$ số đo chiều dài dùng được. Số giá trị được đưa vào phép tính gọi là **cỡ mẫu**; ở đây $n=49$. Nếu một dòng có số đo chiều dài nhưng thiếu thông tin giới tính, số đo chiều dài ấy vẫn được dùng. Trong bài này, **mẫu gốc** là danh sách các giá trị trước khi ghép nhóm.

Dữ liệu được thu thập ở khu vực quần đảo Palmer, Nam Cực. Việc quan sát một số cá thể trong một địa điểm và giai đoạn xác định không tự cho phép kết luận về mọi cá thể của loài.

::: {.zo-source-note}
Nguồn dữ liệu: Allison Horst, Alison Hill và Kristen Gorman, Palmer Penguins, biến flipper_length_mm; dữ liệu gốc do Kristen Gorman và Palmer Station LTER cung cấp. Phần trích trong mục này là Adélie năm 2007; truy cập ngày 22/10/2026.
:::

<a id="nv02"></a>

#### Nhiệm vụ 02 — Đếm đúng mẫu dùng để tính

Trong $17$ dòng đầu của phần Adélie 2007, có đúng một ô thiếu chiều dài. Một bạn cộng các giá trị có sẵn được $3021$ mm rồi chia cho $17$.

a) Nêu đơn vị quan sát, biến và đơn vị đo.

b) Mẫu số cần dùng là bao nhiêu? Vì sao?

c) Sửa câu: “Cá thể ở dòng 4 có chiều dài chân chèo bằng $0$.”

[Xem lời giải](#giai02).

<a id="hoc-goc"></a>

### 2. Những cách khác nhau để nói về vị trí trung tâm

#### Gợi mở 02 — “Ở giữa” và “chia đều” có cùng nghĩa không?

Với các giá trị chiều dài, ta có thể cộng tất cả rồi chia đều cho số quan sát. Ta cũng có thể xếp thứ tự và tìm vị trí chính giữa. Cách thứ nhất sử dụng độ lớn của mọi giá trị; cách thứ hai dựa vào thứ tự. Vì vậy, hai kết quả không nhất thiết bằng nhau.

#### Số trung bình và trung vị

Với mẫu gồm $n$ giá trị $x_1,\ldots,x_n$, số trung bình là

$$
\overline{x}=\frac{x_1+\cdots+x_n}{n}.
$$

Nếu một giá trị thay đổi, tổng và số trung bình thường thay đổi theo. Số trung bình có thể không trùng với bất kì quan sát nào.

Để tìm trung vị $M_e$, trước hết sắp mẫu theo thứ tự không giảm. Nếu $n$ lẻ, chọn giá trị ở vị trí chính giữa. Nếu $n$ chẵn, lấy trung bình cộng của hai giá trị ở giữa. Vị trí trong danh sách đã sắp không phải là chính giá trị cần tìm.

::: {.zo-source-note}
Căn cứ toán học: Toán 10, Tập một, Kết nối tri thức với cuộc sống, Nhà xuất bản Giáo dục Việt Nam, Bài 13, trang 78–79.
:::

#### Ví dụ 01 — Một mẫu có 16 giá trị

Chỉ lấy các số đo có sẵn trong $17$ dòng đầu, ta có mẫu chiều dài chân chèo, đơn vị mm:

$181;\ 186;\ 195;\ 193;\ 190;\ 181;\ 195;\ 193;\ 190;\ 186;\ 180;\ 182;\ 191;\ 198;\ 185;\ 195$.

Sau khi sắp thứ tự:

| Vị trí | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Giá trị, mm | $180$ | $181$ | $181$ | $182$ | $185$ | $186$ | $186$ | $190$ |

| Vị trí | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Giá trị, mm | $190$ | $191$ | $193$ | $193$ | $195$ | $195$ | $195$ | $198$ |

Tổng là $3021$ mm nên

$$
\overline{x}=\frac{3021}{16}=188{,}8125\ \text{mm}.
$$

Hai vị trí ở giữa là $8$ và $9$, cùng mang giá trị $190$ mm. Do đó

$$
M_e=\frac{190+190}{2}=190\ \text{mm}.
$$

Con số $188{,}8125$ mô tả mức trung bình của 16 giá trị đã ghi. Nó không nói rằng ta đã đo được một cá thể chính xác đến bốn chữ số thập phân.

#### Tứ phân vị: chia theo thứ tự

Tứ phân vị thứ hai $Q_2$ chính là trung vị. Để tìm $Q_1$ và $Q_3$:

1. Sắp mẫu theo thứ tự không giảm.
2. Chia thành nửa dưới và nửa trên. Nếu $n$ lẻ, không đưa quan sát ở chính giữa vào hai nửa.
3. $Q_1$ là trung vị của nửa dưới; $Q_3$ là trung vị của nửa trên.

Trong Ví dụ 01, nửa dưới gồm các vị trí từ $1$ đến $8$, nửa trên từ $9$ đến $16$. Vì thế

$$
Q_1=\frac{182+185}{2}=183{,}5,\qquad
Q_2=190,\qquad
Q_3=\frac{193+195}{2}=194.
$$

Các giá trị đều có đơn vị mm. Chúng đánh dấu các vùng vị trí trong mẫu đã sắp. Khi dữ liệu có nhiều giá trị trùng nhau, không nên diễn giải thành “đúng $25\%$ giá trị nhỏ hơn nghiêm ngặt $Q_1$”.

::: {.zo-source-note}
Căn cứ toán học: Toán 10, Tập một, Kết nối tri thức với cuộc sống, Bài 13, trang 80–81. Gói này dùng quy ước trung vị của hai nửa như trên; phần mềm có thể cung cấp những quy ước phân vị khác.
:::

#### Ví dụ 02 — Khi cỡ mẫu lẻ

Năm giá trị hợp lệ đầu của phần dữ liệu đang học là $181;\ 186;\ 195;\ 193;\ 190$ mm. Sau khi sắp, ta được

$$
181;\ 186;\ 190;\ 193;\ 195.
$$

Trung vị là $190$. Nửa dưới gồm $181;186$, nửa trên gồm $193;195$. Do đó $Q_1=183{,}5$ mm và $Q_3=194$ mm. Quan sát $190$ đứng giữa không được tính vào hai nửa.

Ví dụ này dùng lại một phần dữ liệu vừa học để giải thích quy tắc khi số giá trị là số lẻ. Đọc hiểu lời giải giúp em nắm cách làm; để biết có tự làm được hay không, em cần thử một bài khác chưa xem lời giải.

<a id="nv03"></a>

#### Nhiệm vụ 03 — Vị trí và giá trị

Dùng bảng 16 giá trị đã sắp trong Ví dụ 01.

a) Một bạn viết “$Q_1=4{,}5$ vì trung vị của tám vị trí đầu nằm giữa vị trí 4 và 5”. Chỉ ra sự nhầm lẫn và sửa kết quả.

b) Trong Ví dụ 02, nếu đưa quan sát $190$ vào cả hai nửa, em có còn đang dùng quy ước tứ phân vị của bài học không? Giải thích.

[Xem lời giải](#giai03).

#### Mốt: giá trị xuất hiện nhiều nhất

Mốt là giá trị có tần số lớn nhất. Nếu một số giá trị cùng có tần số lớn nhất và nổi trội hơn các giá trị còn lại, mẫu có nhiều mốt. Theo quy ước dùng trong gói này, khi có ít nhất hai giá trị phân biệt và chúng có cùng tần số, mẫu không có mốt. Nếu mọi quan sát đều bằng một giá trị duy nhất, chính giá trị ấy là mốt.

Ở mẫu 16 giá trị, $195$ xuất hiện ba lần, nhiều hơn các giá trị khác, nên mốt là $195$ mm. Khi mở rộng đến toàn bộ 49 giá trị Adélie 2007, các số $180$, $190$, $195$ đều xuất hiện năm lần và cùng đạt tần số lớn nhất. Mẫu lớn này có ba mốt.

Không thể mang mốt của một phần trích sang mẫu lớn hơn mà không đếm lại.

::: {.zo-source-note}
Căn cứ toán học: Toán 10, Tập một, Kết nối tri thức với cuộc sống, Bài 13, trang 81. Các tần số Penguins trong đoạn này được tính từ phần dữ liệu Adélie 2007 đã nêu.
:::

<a id="hoc-ghep"></a>

### 3. Từ từng giá trị đến các khoảng

#### Gợi mở 03 — Biết khoảng có đủ để khôi phục giá trị không?

Nếu chỉ biết một chiều dài thuộc $[190;195)$ mm, ta biết nó không nhỏ hơn $190$ và nhỏ hơn $195$. Ta chưa biết nó là $190$, $191$, $192$ hay một giá trị khác trong khoảng. Ghép nhóm giữ được số quan sát ở từng vùng nhưng làm mất vị trí chính xác bên trong vùng ấy.

Ta chia trục thành các khoảng không chồng lấn và bao phủ mọi giá trị của mẫu. Ta dùng các khoảng lấy đầu mút trái và không lấy đầu mút phải (gọi là đóng trái–mở phải). Vì thế $190$ thuộc $[190;195)$, không thuộc $[185;190)$.

**Tần số** của một nhóm là số quan sát thuộc nhóm. **Tần số tích lũy** đến một nhóm là tổng tần số từ nhóm đầu đến nhóm ấy. **Giá trị đại diện** là trung điểm hai đầu mút.

#### Ví dụ 03 — Ghép nhóm mẫu nhỏ

Với mẫu 16 giá trị ở Ví dụ 01:

| Khoảng, mm | Tần số | Giá trị đại diện, mm | Tần số tích lũy |
|---|---:|---:|---:|
| $[180;185)$ | $4$ | $182{,}5$ | $4$ |
| $[185;190)$ | $3$ | $187{,}5$ | $7$ |
| $[190;195)$ | $5$ | $192{,}5$ | $12$ |
| $[195;200)$ | $4$ | $197{,}5$ | $16$ |

Tổng tần số là $16$, bằng cỡ mẫu. Tần số tích lũy $7$ ở hàng thứ hai cho biết có bảy giá trị nhỏ hơn $190$ mm.

Chiều dài là đại lượng đo liên tục, dù phần dữ liệu này ghi số nguyên mm. Các khoảng trên được chọn trực tiếp trên trục độ dài. Trung điểm $192{,}5$ mm đại diện cho khoảng $[190;195)$; không khẳng định có một cá thể mang đúng giá trị ấy. Không tự đổi biên khoảng khi chuyển giữa bảng và công thức.

::: {.zo-source-note}
Căn cứ toán học: Toán 11, Tập một, Kết nối tri thức với cuộc sống, Bài 8, trang 58–59, và Bài 9, trang 62. Trường hợp nhóm rời rạc được ghi bằng hai giá trị nguyên bao gồm cả hai đầu cần đọc quy tắc hiệu chỉnh riêng ở trang 63; các khoảng độ dài trong gói đã được cho trực tiếp dưới dạng đóng trái–mở phải.
:::

<a id="nv04"></a>

#### Nhiệm vụ 04 — Thông tin còn lại sau ghép nhóm

Dùng bảng ở Ví dụ 03.

a) Có bao nhiêu chiều dài nhỏ hơn $195$ mm?

b) Có thể khẳng định cả năm cá thể ở nhóm $[190;195)$ đều có chiều dài $192{,}5$ mm không?

c) Nếu đếm $195$ vào cả hai nhóm kề nhau, phép kiểm nào giúp em phát hiện sai sót?

[Xem lời giải](#giai04).

<a id="hoc-uoc-luong"></a>

### 4. Ước lượng các số đặc trưng từ bảng nhóm

#### Gợi mở 04 — Làm thế nào khi không còn từng giá trị?

Trong một nhóm có nhiều quan sát, ta có thể dùng trung điểm để tính mức trung bình gần đúng. Với trung vị và tứ phân vị, tần số tích lũy cho biết cần đi đến nhóm nào; sau đó ta ước lượng vị trí bên trong nhóm. Cách tính này gọi là **nội suy**: coi các giá trị trải đều trong nhóm để tìm một giá trị gần đúng.

Bảng sau dùng **toàn bộ 49 giá trị hợp lệ Adélie 2007**, khác với mẫu nhỏ 16 giá trị ở mục trước:

| Khoảng, mm | Tần số $f_i$ | Trung điểm $c_i$, mm | Tần số tích lũy |
|---|---:|---:|---:|
| $[170;175)$ | $2$ | $172{,}5$ | $2$ |
| $[175;180)$ | $3$ | $177{,}5$ | $5$ |
| $[180;185)$ | $15$ | $182{,}5$ | $20$ |
| $[185;190)$ | $10$ | $187{,}5$ | $30$ |
| $[190;195)$ | $10$ | $192{,}5$ | $40$ |
| $[195;200)$ | $9$ | $197{,}5$ | $49$ |
| $[200;205)$ | $0$ | $202{,}5$ | $49$ |
| $[205;210)$ | $0$ | $207{,}5$ | $49$ |
| $[210;215)$ | $0$ | $212{,}5$ | $49$ |

Các khoảng cuối có tần số $0$ vẫn cho thấy trục chia đều. Chúng không thêm quan sát vào mẫu.

#### Số trung bình của mẫu ghép nhóm

$$
\overline{x}_{\text{nhóm}}=\frac{\sum_i f_i c_i}{n},
\qquad n=\sum_i f_i.
$$

Ta nhân trung điểm của mỗi nhóm với số quan sát thuộc nhóm ấy, cộng các tích rồi chia cho tổng số quan sát. Số quan sát của nhóm được gọi là **trọng số** trong phép tính này. Nếu chỉ cộng các trung điểm rồi chia cho số nhóm, ta đã coi các nhóm có số quan sát như nhau, dù thực tế có nhóm nhiều, nhóm ít.

#### Ví dụ 04 — Trung điểm giúp tính, nhưng không khôi phục dữ liệu gốc

Với bảng trên:

$$
\overline{x}_{\text{nhóm}}
=\frac{2\cdot172{,}5+3\cdot177{,}5+15\cdot182{,}5+10\cdot187{,}5+10\cdot192{,}5+9\cdot197{,}5}{49}
=\frac{9192{,}5}{49}
\approx187{,}60\ \text{mm}.
$$

Tính trực tiếp từ 49 giá trị gốc cho

$$
\overline{x}=\frac{9143}{49}\approx186{,}59\ \text{mm}.
$$

Hai kết quả khác nhau vì phép tính từ bảng đã thay từng giá trị bằng trung điểm của nhóm. Chênh lệch không chỉ do làm tròn.

::: {.zo-source-note}
Căn cứ công thức: Toán 11, Tập một, Kết nối tri thức với cuộc sống, Bài 9, trang 62–63. Các tổng và kết quả ở Ví dụ 04 do ZO Math tính từ phần Adélie 2007.
:::

#### Trung vị và tứ phân vị của mẫu ghép nhóm

Với nhóm cần nội suy, gọi:

- $a$ là đầu mút trái;
- $h$ là độ rộng nhóm;
- $f$ là tần số của nhóm, phải dương;
- $F$ là tần số tích lũy **trước** nhóm ấy;
- $r$ là vị trí cần tìm: $\frac{n}{4}$, $\frac{n}{2}$ hoặc $\frac{3n}{4}$.

Công thức chung là

$$
a+\frac{r-F}{f}\,h.
$$

Trước hết dùng tần số tích lũy để chọn nhóm. Phần $\frac{r-F}{f}$ cho biết cần đi thêm một tỉ lệ bao nhiêu của độ rộng nhóm. Đây là phép nội suy theo bảng nhóm, không phải phép tìm lại chính xác từng quan sát đã mất.

Nếu $r$ đúng bằng một tần số tích lũy, kết quả có thể nằm ở biên nhóm. Với hai nhóm kề nhau đều có tần số dương, tính từ cuối nhóm trước hoặc đầu nhóm sau cho cùng biên. Không chia cho tần số $0$.

#### Ví dụ 05 — Xác định nhóm trước khi thay số

Với $n=49$, vị trí trung vị là $r=24{,}5$. Tần số tích lũy đến nhóm $[180;185)$ là $20$, đến nhóm $[185;190)$ là $30$. Vì vậy dùng nhóm $[185;190)$, với $a=185$, $F=20$, $f=10$, $h=5$:

$$
M_{e,\text{nhóm}}=185+\frac{24{,}5-20}{10}\cdot5=187{,}25\ \text{mm}.
$$

Với $Q_1$, vị trí cần tìm là $12{,}25$, thuộc nhóm $[180;185)$:

$$
Q_{1,\text{nhóm}}=180+\frac{12{,}25-5}{15}\cdot5\approx182{,}42\ \text{mm}.
$$

Nếu nhầm $F$ thành tần số tích lũy đến hết nhóm đang xét, phần đi thêm sẽ âm. Việc hiểu $F$ giúp kiểm phép tính trước khi bấm máy.

::: {.zo-source-note}
Căn cứ toán học: Toán 11, Tập một, Kết nối tri thức với cuộc sống, Bài 9, trung vị ở trang 64 và tứ phân vị ở trang 64–65.
:::

#### Mốt của mẫu ghép nhóm

Trong phạm vi đang học, các nhóm có cùng độ rộng $h$. Chọn nhóm có tần số lớn nhất. Nếu nhóm này có đầu mút trái $a$, tần số $f$, hai nhóm kề có tần số $f_-$ và $f_+$, thì

$$
M_{o,\text{nhóm}}
=a+\frac{f-f_-}{(f-f_-)+(f-f_+)}\,h.
$$

Với nhóm ở đầu hoặc cuối bảng, quy ước tần số phía ngoài bằng $0$. Công thức cần mẫu số dương. Nếu có nhiều nhóm cùng cao nhất, cần xem xét tình huống cụ thể; không tùy ý chọn một nhóm rồi tuyên bố mốt duy nhất. Nếu tất cả tần số nhóm bằng nhau, mẫu ghép nhóm không có mốt theo quy ước đang dùng.

#### Ví dụ 06 — Mốt của bảng nhóm và mốt của mẫu gốc

Nhóm $[180;185)$ có tần số lớn nhất là $15$; hai nhóm kề có tần số $3$ và $10$. Do đó

$$
M_{o,\text{nhóm}}
=180+\frac{15-3}{(15-3)+(15-10)}\cdot5
\approx183{,}53\ \text{mm}.
$$

Kết quả gợi một vị trí nổi trội theo bảng nhóm đã chọn. Nó không nói rằng $183{,}53$ đã xuất hiện nhiều nhất trong dữ liệu gốc. Ta đã biết mẫu gốc có ba mốt $180$, $190$, $195$ mm. Chính sự khác nhau này nhắc ta luôn nói rõ đang mô tả dữ liệu gốc hay dữ liệu ghép nhóm.

::: {.zo-source-note}
Căn cứ toán học và điều kiện độ rộng nhóm bằng nhau: Toán 11, Tập một, Kết nối tri thức với cuộc sống, Bài 9, trang 66.
:::

<a id="nv05"></a>

#### Nhiệm vụ 05 — Tự nội suy và giải thích kết quả

Dùng bảng 49 giá trị ở đầu mục 4.

a) Tìm nhóm dùng để tính $Q_3$. Ghi $r,a,F,f,h$, rồi tính $Q_{3,\text{nhóm}}$.

b) Một bạn nói: “Trung vị thật của 49 giá trị phải bằng $187{,}25$ mm vì em đã tính đúng công thức.” Em đồng ý đến đâu? Biết trung vị tính trực tiếp từ dữ liệu gốc là $186$ mm.

[Xem lời giải](#giai05).

<a id="hoc-chon"></a>

### 5. Chọn số đại diện theo câu hỏi

#### Gợi mở 05 — Đại diện cho ai và cho việc gì?

Một con số có thể được tính đúng nhưng trả lời nhầm câu hỏi. Trung bình của một mẫu gộp hai loài không tự mô tả tốt từng loài; trung bình lượt thuê mỗi ngày không phải số người dùng khác nhau; số $0$ trong dữ liệu quan trắc cần được đọc cùng ký hiệu ghi nhận.

#### Ví dụ 07 — Hai loài và một số trung bình chung

Trong dữ liệu học năm 2007:

| Loài | Số giá trị hợp lệ | Tổng chiều dài, mm | Trung bình, mm | Trung vị, mm |
|---|---:|---:|---:|---:|
| Adélie | $49$ | $9143$ | $186{,}59$ | $186$ |
| Gentoo | $34$ | $7314$ | $215{,}12$ | $215$ |

Nếu gộp hai phần trích, trung bình là

$$
\frac{9143+7314}{49+34}=\frac{16457}{83}\approx198{,}28\ \text{mm}.
$$

Con số này được tính từ $49$ cá thể Adélie và $34$ cá thể Gentoo đã ghi trong hai phần dữ liệu. Nó nằm giữa hai trung bình riêng. Nếu câu hỏi quan tâm từng loài, bảng theo loài giữ được sự khác biệt mà một số chung che đi. Không lấy trung bình cộng đơn giản của hai trung bình khi cỡ mẫu hai nhóm khác nhau.

Sự khác nhau trong mẫu là điều quan sát được. Riêng bảng này chưa giải thích nguyên nhân sinh học và không chứng minh mọi cá thể Gentoo đều có chân chèo dài hơn mọi cá thể Adélie.

#### Ví dụ 08 — Một ngày điển hình hay tổng lượt thuê?

Dữ liệu Capital Bikeshare tháng 01/2012 có $31$ ngày, tổng $96744$ lượt thuê, trung vị $3243$ lượt/ngày. Các giá trị theo ngày đều khác nhau.

$$
\overline{x}=\frac{96744}{31}\approx3120{,}77\ \text{lượt/ngày}.
$$

Nếu muốn biết tổng lượt thuê trong tháng chia đều cho mỗi ngày là bao nhiêu, số trung bình phù hợp vì $n\overline{x}$ khôi phục tổng trước khi làm tròn. Nếu muốn mô tả vị trí giữa các ngày khi xếp theo lượng thuê, dùng trung vị. Trung vị không cho biết tổng tháng bằng tích của nó với số ngày.

Mẫu gốc không có mốt vì mọi giá trị đều xuất hiện một lần. Nếu ghép nhóm theo các khoảng $[1000;2000)$, $[2000;3000)$, $[3000;4000)$, $[4000;5000)$, tần số lần lượt là $3;10;10;8$. Hai nhóm đông nhất cũng không biến thành một số lượt thuê gốc xuất hiện nhiều nhất.

Một ngày có nhiều lượt thuê không nhất thiết có từng ấy người: cùng một người có thể thuê nhiều lượt. Các số của tháng này cũng chưa đủ để dự báo chính xác một ngày tương lai.

::: {.zo-source-note}
Nguồn: Hadi Fanaee-T và João Gama, Bike Sharing, UCI Machine Learning Repository, tệp day.csv, cột ngày (dteday) và cột số lượt thuê (cnt), phần trích tháng 01/2012. Dữ liệu CC BY 4.0; ZO Math chọn phần trích và tính bảng tóm tắt, không thay giá trị gốc.
:::

#### Ví dụ 09 — Đọc số 0 cùng ký hiệu quan trắc

Đầu tháng 01/2023, trạm Seattle–Tacoma ghi:

| Ngày | PRCP, mm | Ký hiệu vết giáng thủy |
|---|---:|---|
| 01/01/2023 | $0{,}3$ | Không có ký hiệu T |
| 02/01/2023 | $0{,}0$ | Không có ký hiệu T |
| 03/01/2023 | $0{,}0$ | T |
| 04/01/2023 | $0{,}5$ | Không có ký hiệu T |
| 05/01/2023 | $0{,}0$ | T |
| 06/01/2023 | $3{,}0$ | Không có ký hiệu T |
| 07/01/2023 | $7{,}1$ | Không có ký hiệu T |

PRCP là tên cột ghi lượng giáng thủy: nước từ mưa, tuyết… được quy đổi thành lượng nước tương đương, đo bằng mm. Ký hiệu T ghi bên cạnh cho biết có một lượng giáng thủy rất nhỏ, thường gọi là **vết giáng thủy**, chưa đủ để ghi thành một số đo lớn hơn $0{,}0$ mm. Vì vậy, số $0{,}0$ kèm T không có nghĩa là hoàn toàn không có giáng thủy.

Cả tháng có $31$ giá trị hợp lệ. Tổng các giá trị số được ghi là $78{,}5$ mm; trung bình khoảng $2{,}53$ mm/ngày, trung vị $0{,}8$ mm. Có $13$ ngày được ghi bằng $0$, trong đó $6$ ngày có ký hiệu T. Tổng và trung bình ở đây được tính từ các con số được ghi trong dữ liệu, không tự bổ sung một lượng nước giả định cho các ngày có vết.

Có thể tóm tắt tháng bằng bảng sau:

| Lớp giá trị PRCP, mm | Số ngày |
|---|---:|
| $\{0\}$ | $13$, trong đó $6$ ngày có ký hiệu T |
| $(0;1)$ | $4$ |
| $[1;5)$ | $8$ |
| $[5;10)$ | $3$ |
| $[10;20)$ | $3$ |
| $[20;40)$ | $0$ |

Bảng này để riêng các ngày có giá trị $0$ vào một hàng; những hàng còn lại dùng các khoảng có độ rộng khác nhau. Vì vậy, không áp dụng công thức mốt dành cho các nhóm rộng bằng nhau ở mục 4. Khi cần trung vị hoặc tứ phân vị, hãy tính từ các giá trị gốc; không thay các số $0$ bằng những giá trị trải đều trong một khoảng.

::: {.zo-source-note}
Nguồn: NOAA/NCEI, GHCN-Daily, trạm USW00024233, tháng 01/2023, biến PRCP và ký hiệu đo kèm theo. Phần dữ liệu được lấy từ NCEI theo hệ mét; PRCP trong phần trích này đã có đơn vị mm.
:::

<a id="nv06"></a>

#### Nhiệm vụ 06 — Sửa câu kết luận

a) Sửa câu: “Tháng 01/2012, trung bình có khoảng $3121$ người khác nhau thuê xe mỗi ngày.”

b) Sửa câu: “Tháng 01/2023 có $13$ ngày chắc chắn hoàn toàn không có giáng thủy tại Seattle–Tacoma.”

c) Từ một tháng tại một trạm, có thể kết luận khí hậu của cả thành phố đã thay đổi dài hạn không? Nêu điều dữ liệu còn thiếu.

[Xem lời giải](#giai06).

### Khép lại Bài học

Trước khi tin một con số, hãy thử giải thích được bốn điều: nó được tính từ những quan sát nào; mỗi quan sát có nghĩa gì; cách tính giữ lại điều gì; và câu hỏi nào nó chưa trả lời được. Nếu vẫn nhầm vị trí với giá trị, dữ liệu thiếu với số $0$, hoặc kết quả ghép nhóm với kết quả gốc, hãy trở lại đúng mục ấy trước khi luyện tiếp.



<a id="luyen-tap"></a>

## Luyện tập

Tự làm từng chặng trước khi mở lời giải. Phần này dùng Adélie 2008, Bike Sharing tháng 02/2012 và NOAA tháng 07/2023. Các dòng dữ liệu ở đây chưa được dùng trong Bài học, dù một vài con số có thể trùng nhau. Trong cùng một chặng, em có thể gặp lại một mẫu để tập chuyển từ danh sách số sang bảng nhóm. Làm tiếp trên mẫu đã gặp giúp luyện cách trình bày khác; việc đó chưa cho biết em có tự làm được với một mẫu chưa gặp hay không.

Các kết quả tính gần đúng trong phần Penguins và Bike Sharing làm tròn đến hai chữ số thập phân nếu cần. Với NOAA, giữ số liệu gốc như đã cho và làm tròn trung bình đến hai chữ số thập phân. Không làm tròn kết quả trung gian.

| Chặng | Trọng tâm luyện tập | Nhiệm vụ và Điểm dừng |
|---|---|---|
| Đọc và tính trên mẫu gốc | Cỡ mẫu, thứ tự, các số đặc trưng | Nhiệm vụ 07–08; Điểm dừng 01 |
| Từ danh sách số sang bảng nhóm | Đếm số giá trị, cộng dồn tần số, tính gần đúng và thay độ rộng nhóm | Nhiệm vụ 09–11; Điểm dừng 02 |
| Chọn và giải thích | Chọn số theo câu hỏi, tính trung bình các nhóm và nêu giới hạn kết luận | Nhiệm vụ 12–14; Điểm dừng 03 |

### Chặng 1 — Đọc và tính trên mẫu gốc

<a id="nv07"></a>

#### Nhiệm vụ 07 — Mẫu Adélie năm 2008

Mười hai giá trị chiều dài chân chèo đầu tiên của phần trích Adélie 2008, đơn vị mm, là:

$186;\ 188;\ 190;\ 200;\ 187;\ 191;\ 186;\ 193;\ 181;\ 194;\ 185;\ 195$.

a) Xác định đơn vị quan sát, biến, đơn vị đo và cỡ mẫu.

b) Sắp mẫu, tính số trung bình, trung vị và mốt. Nêu ý nghĩa của trung vị trong mẫu này.

c) Giá trị tiếp theo trong phần trích là $185$ mm. Nếu đưa thêm quan sát này vào mẫu, mốt của mẫu 13 giá trị thay đổi thế nào? Không cần tính lại các số đặc trưng khác.

[Xem lời giải](#giai07).

<a id="nv08"></a>

#### Nhiệm vụ 08 — Tứ phân vị khi số quan sát thay đổi

a) Tìm $Q_1,Q_2,Q_3$ của mẫu 12 giá trị ở Nhiệm vụ 07. Chỉ rõ các vị trí đã dùng.

b) Xét riêng 11 giá trị đầu trong danh sách ban đầu, tức chưa đưa giá trị cuối $195$ vào mẫu. Tìm lại ba tứ phân vị theo quy ước đã học.

c) Vì sao kết quả ở ý b không thay thế kết quả ở ý a?

[Xem lời giải](#giai08).

<a id="dung01"></a>

#### Điểm dừng 01 — Đã phân biệt được vị trí và giá trị chưa?

| Việc cần xác nhận | Bài làm cần đối chiếu | Nếu chưa đúng |
|---|---|---|
| Dùng đúng cỡ mẫu và giữ đủ số quan sát | Nhiệm vụ 07a–b | Xem [đọc dữ liệu](#hoc-doc); tự kiểm tra thêm bằng Nhiệm vụ 24a hoặc 26a nếu chưa làm và chưa xem lời giải |
| Sắp trước khi tìm trung vị, chọn đúng hai vị trí ở giữa | Nhiệm vụ 07b | Xem [mẫu gốc](#hoc-goc), rồi tự làm Nhiệm vụ 24b nếu chưa làm và chưa xem lời giải |
| Chia hai nửa đúng khi cỡ mẫu chẵn và lẻ | Nhiệm vụ 08a–b | Xem Ví dụ 01–02, rồi tự làm Nhiệm vụ 24b–c nếu chưa làm và chưa xem lời giải |
| Nêu đúng một mốt hoặc nhiều mốt và phạm vi mẫu | Nhiệm vụ 07b–c, 08c | Đếm lại tần số; tự làm Nhiệm vụ 24b về một mốt hoặc 25a về nhiều mốt nếu chưa làm và chưa xem lời giải |

Nếu đã giải thích được các bước, tiếp tục chặng 2. Không cần làm tất cả bài Sửa lỗi.

### Chặng 2 — Từ danh sách số sang bảng nhóm

<a id="nv09"></a>

#### Nhiệm vụ 09 — Tự lập bảng

Ghép 12 giá trị ở Nhiệm vụ 07 theo các khoảng $[180;185)$, $[185;190)$, $[190;195)$, $[195;200)$, $[200;205)$.

a) Lập bảng tần số, trung điểm và tần số tích lũy.

b) Chỉ ra nhóm chứa $190$ và nhóm chứa $200$. Kiểm tổng tần số.

c) Có thể lấy trung điểm làm giá trị thực của từng quan sát trong nhóm không?

[Xem lời giải](#giai09).

<a id="nv10"></a>

#### Nhiệm vụ 10 — Ước lượng trên mẫu lớn hơn

Toàn bộ phần trích Adélie 2008 có $50$ giá trị hợp lệ và được ghép nhóm như sau:

| Khoảng, mm | Tần số |
|---|---:|
| $[170;175)$ | $0$ |
| $[175;180)$ | $1$ |
| $[180;185)$ | $3$ |
| $[185;190)$ | $15$ |
| $[190;195)$ | $18$ |
| $[195;200)$ | $9$ |
| $[200;205)$ | $2$ |
| $[205;210)$ | $2$ |
| $[210;215)$ | $0$ |

a) Lập tần số tích lũy và tính số trung bình của mẫu ghép nhóm.

b) Tìm trung vị, $Q_1,Q_3$. Với mỗi số, ghi nhóm được dùng và tần số tích lũy trước nhóm.

c) Tính mốt của mẫu ghép nhóm, nêu điều kiện cho phép dùng công thức.

d) Tính trực tiếp trên mẫu gốc cho trung bình $191{,}04$ mm và trung vị $190$ mm. Giải thích vì sao kết quả ở ý a–b có thể khác.

[Xem lời giải](#giai10).

<a id="nv11"></a>

#### Nhiệm vụ 11 — Độ rộng nhóm có quyết định mọi sai khác không?

Vẫn 50 giá trị của Nhiệm vụ 10, nay ghép nhóm rộng $10$ mm:

| Khoảng, mm | Tần số |
|---|---:|
| $[170;180)$ | $1$ |
| $[180;190)$ | $18$ |
| $[190;200)$ | $27$ |
| $[200;210)$ | $4$ |

a) Tính số trung bình của mẫu ghép nhóm mới.

b) So với trung bình gốc $191{,}04$ mm, kết quả của bảng rộng $5$ mm hay $10$ mm gần hơn trong trường hợp này?

c) Đánh giá phát biểu: “Cứ chia nhóm nhỏ hơn thì mọi số đặc trưng tính từ bảng chắc chắn gần số gốc hơn.”

[Xem lời giải](#giai11).

<a id="dung02"></a>

#### Điểm dừng 02 — Kiểm lại cách lập bảng và tính gần đúng

| Việc cần xác nhận | Bài làm cần đối chiếu | Nếu chưa đúng |
|---|---|---|
| Không bỏ sót hoặc đếm hai lần ở biên | Nhiệm vụ 09a–b | Xem [ghép nhóm](#hoc-ghep); tự làm Nhiệm vụ 25a nếu chưa làm và chưa xem lời giải |
| Nhân từng trung điểm với tần số rồi chia tổng các tích cho tổng tần số | Nhiệm vụ 10a | Xem Ví dụ 04; tự làm Nhiệm vụ 25c nếu chưa làm và chưa xem lời giải |
| Chọn đúng nhóm, đúng $F$, đúng $f$ | Nhiệm vụ 10b | Xem Ví dụ 05; tự làm Nhiệm vụ 25c nếu chưa làm và chưa xem lời giải |
| Dùng mốt trong điều kiện nhóm rộng bằng nhau | Nhiệm vụ 10c | Xem Ví dụ 06; tự làm Nhiệm vụ 25d nếu chưa làm và chưa xem lời giải |
| Phân biệt phép ước lượng với dữ liệu gốc | Nhiệm vụ 10d, 11b–c | Xem mục 4; đối chiếu lại lý do, không chỉ đáp số |

Nếu còn một phép tính sai, sửa đúng phép tính đó và kiểm xem nó có làm đổi kết luận không. Nếu đã xem lời giải, bài làm sau đó giúp em luyện lại cách giải, nhưng chưa cho biết em có tự giải được khi không có hướng dẫn hay không.

### Chặng 3 — Chọn và giải thích

<a id="nv12"></a>

#### Nhiệm vụ 12 — Chọn số cho bản tóm tắt lượt thuê

Bike Sharing tháng 02/2012 có $29$ ngày, tổng $103137$ lượt thuê và trung vị $3777$ lượt/ngày. Các giá trị theo ngày đều khác nhau.

a) Tính số trung bình. Nếu báo cáo cần cho biết tổng lượt thuê trong tháng chia đều cho mỗi ngày là bao nhiêu, em chọn số nào?

b) Nếu báo cáo cần vị trí giữa các ngày sau khi xếp theo số lượt thuê, em chọn số nào?

c) Có mốt của mẫu gốc không? Giải thích. Có thể gọi các lượt thuê là số người khác nhau không?

[Xem lời giải](#giai12).

<a id="nv13"></a>

#### Nhiệm vụ 13 — Trung bình của các nhóm không phải lúc nào cũng lấy trung bình cộng

Vẫn tháng 02/2012:

| Nhóm ngày | Số ngày | Tổng lượt thuê |
|---|---:|---:|
| Ngày làm việc, không phải cuối tuần hoặc ngày nghỉ lễ theo dữ liệu nguồn | $20$ | $77403$ |
| Những ngày còn lại | $9$ | $25734$ |

a) Tính trung bình của mỗi nhóm.

b) Từ các nhóm, tính lại trung bình của cả tháng. Vì sao không lấy trung bình cộng đơn giản của hai số trung bình nhóm?

c) Bảng này có chứng minh việc là ngày làm việc gây ra mức thuê cao hơn không? Viết một kết luận vừa đủ với dữ kiện.

[Xem lời giải](#giai13).

<a id="nv14"></a>

#### Nhiệm vụ 14 — Trung vị bằng 0 có nghĩa là không có giáng thủy?

Tại trạm Seattle–Tacoma, tháng 07/2023 có $31$ giá trị PRCP hợp lệ: $30$ ngày ghi $0$ mm, ngày 24/07 ghi $2{,}3$ mm. Không ngày nào trong phần trích có ký hiệu T.

a) Tính trung bình và trung vị của các giá trị đã ghi.

b) Sửa câu: “Trung vị bằng $0$ nên tổng lượng giáng thủy ghi nhận trong tháng bằng $0$.”

c) Em sẽ giữ lại những thông tin nào nếu phải viết một câu mô tả ngắn mà không che mất ngày có giáng thủy?

[Xem lời giải](#giai14).

<a id="dung03"></a>

#### Điểm dừng 03 — Một số đúng đã trả lời đúng câu hỏi chưa?

Đối chiếu Nhiệm vụ 12a–b: lý do chọn số phải gắn với tổng hoặc vị trí giữa, không chỉ nói “số này tốt hơn”. Ở Nhiệm vụ 13, cần tính trung bình theo đúng số ngày của mỗi nhóm. Số liệu cho thấy hai nhóm khác nhau, nhưng chưa giải thích được nguyên nhân của sự khác nhau ấy. Ở Nhiệm vụ 14, cần phân biệt trung vị, tổng và tần số của số $0$.

Nếu còn vướng, xem [chọn số đại diện](#hoc-chon). Nhiệm vụ 26 giúp em tự kiểm tra cách tính trung bình khi gộp hai nhóm và cách kết luận đúng với phần dữ liệu đã xét; Nhiệm vụ 27 giúp kiểm cách đọc số $0$ và ký hiệu T. Chọn ý đúng với điều cần sửa, chưa làm và chưa xem lời giải. Khi đã sẵn sàng, em có thể thực hiện Kiểm tra.

<a id="kiem-tra"></a>

## Kiểm tra

**Thời gian dự kiến: 45 phút, trong một lượt.** Có thể bắt đầu khi đã chuẩn bị kĩ lưỡng hoặc đủ tự tin. Không chia một lượt thành nhiều buổi.

Được dùng máy tính cho phép tính số học; cần ghi các vị trí, nhóm và lập luận được yêu cầu. Không dùng chức năng thống kê tự động thay cho việc xác định tứ phân vị theo quy ước của gói. Trong lượt, không mở Bài học, Ôn nền, Lời giải hoặc Sửa lỗi. Nếu cần trợ giúp, kết thúc lượt trước và giữ bài làm ban đầu.

Làm tròn các số gần đúng đến hai chữ số thập phân; giữ đủ chữ số ở bước trung gian. Bốn nhiệm vụ dưới đây dùng những phần trích chưa xuất hiện trong Bài học và Luyện tập.

<a id="nv15"></a>

#### Nhiệm vụ 15 — Đọc, tính và ghép nhóm một mẫu mới

Mười hai chiều dài chân chèo đầu của phần trích Adélie 2009, đơn vị mm, là:

$192;\ 203;\ 183;\ 190;\ 193;\ 184;\ 199;\ 190;\ 181;\ 197;\ 198;\ 191$.

a) Nêu đơn vị quan sát, biến, đơn vị đo và cỡ mẫu.

b) Sắp mẫu; tính trung bình, trung vị, $Q_1,Q_3$ và mốt. Chỉ rõ các vị trí dùng để tìm tứ phân vị.

c) Lập tần số theo các khoảng rộng $5$ mm từ $[180;185)$ đến $[200;205)$. Giữ cả khoảng có tần số $0$.

[Xem lời giải](#giai15).

<a id="nv16"></a>

#### Nhiệm vụ 16 — Bảng ghép nhóm Adélie 2009

Toàn bộ phần trích năm 2009 có $52$ giá trị chiều dài hợp lệ:

| Khoảng, mm | Tần số |
|---|---:|
| $[170;175)$ | $0$ |
| $[175;180)$ | $1$ |
| $[180;185)$ | $4$ |
| $[185;190)$ | $11$ |
| $[190;195)$ | $19$ |
| $[195;200)$ | $12$ |
| $[200;205)$ | $4$ |
| $[205;210)$ | $0$ |
| $[210;215)$ | $1$ |

a) Lập tần số tích lũy; tính trung bình của mẫu ghép nhóm.

b) Tính trung vị, $Q_1,Q_3$, nêu nhóm và các đại lượng dùng trong mỗi lần nội suy.

c) Tính mốt của mẫu ghép nhóm. Nêu điều kiện về độ rộng các nhóm.

d) Một bạn cho rằng giá trị $210$ phải thuộc $[205;210)$ và trung vị tính ở ý b là trung vị chính xác của mẫu gốc. Sửa hai nhận định đó.

[Xem lời giải](#giai16).

<a id="nv17"></a>

#### Nhiệm vụ 17 — Số nào phù hợp với báo cáo?

Bike Sharing tháng 03/2012 có $31$ ngày, tổng $164875$ lượt thuê, trung vị $5382$ lượt/ngày. Mỗi số lượt thuê ngày chỉ xuất hiện một lần.

a) Tính trung bình và chọn số cho biết tổng lượt thuê trong tháng chia đều cho mỗi ngày là bao nhiêu.

b) Chọn số để mô tả vị trí giữa các ngày đã xếp theo lượng thuê. Nêu khác biệt về ý nghĩa so với ý a.

c) Cho biết mẫu có mốt hay không và nêu một kết luận mà dữ liệu này chưa cho phép về người sử dụng hoặc tương lai.

[Xem lời giải](#giai17).

<a id="nv18"></a>

#### Nhiệm vụ 18 — Đọc một tháng quan trắc

Tháng 11/2023 tại trạm Seattle–Tacoma có $30$ giá trị PRCP hợp lệ, tổng các giá trị số là $147$ mm. Có $15$ giá trị bằng $0$; trong số đó, ngày 07/11 có ký hiệu T. Giá trị dương nhỏ nhất là $1{,}3$ mm.

a) Tính trung bình và trung vị của mẫu. Giải thích hai giá trị ở giữa đã dùng.

b) Sửa câu: “Có đúng $15$ ngày chắc chắn hoàn toàn không có giáng thủy.”

c) Vì sao không thể dùng riêng tháng này để kết luận một xu thế khí hậu dài hạn?

[Xem lời giải](#giai18).

<a id="dung04"></a>

### Điểm dừng 04 — Đọc kết quả theo mục tiêu

Chỉ mở lời giải sau khi đã kết thúc lượt. Giữ riêng bài làm ban đầu; ghi kết quả sau hỗ trợ ở phần khác.

| Mục tiêu cần kiểm | Bài làm cần đối chiếu | Biểu hiện cần có |
|---|---|---|
| Đọc đúng mẫu | Nhiệm vụ 15a, 16a, 18 | Nêu đúng đối tượng, đại lượng và đơn vị đo; đếm đúng số giá trị dùng để tính |
| Tính trên mẫu gốc | Nhiệm vụ 15b, 17c, 18a | Sắp đúng; dùng đúng vị trí; các số đặc trưng và lý do đúng; không ép mẫu phải có mốt |
| Ghép nhóm | Nhiệm vụ 15c, 16a và 16d | Xếp mỗi giá trị vào đúng một nhóm; đếm đủ, giữ nhóm có tần số bằng không và cộng dồn đúng |
| Ước lượng từ bảng | Nhiệm vụ 16a–c | Nhân trung điểm với tần số; chọn đúng nhóm, $F,f,h$; dùng công thức mốt đúng điều kiện |
| Chọn số đại diện | Nhiệm vụ 17a–b | Lý do phân biệt mục đích mô tả tổng với vị trí giữa |
| Giới hạn kết luận | Nhiệm vụ 16d, 17c, 18b–c | Không gọi ước lượng là số gốc; giữ ý nghĩa lượt thuê, ký hiệu T và phạm vi thời gian |

Bài Kiểm tra này hỏi tứ phân vị khi mẫu gốc có số giá trị chẵn, chưa hỏi lại trường hợp lẻ. Em đã gặp trường hợp lẻ ở Nhiệm vụ 08b, nhiều mốt ở Nhiệm vụ 07c và sẽ gặp lại khi Ôn lại; dữ liệu thiếu đã được học ở Nhiệm vụ 02. Khi ghi kết quả của những bài ấy, hãy nói rõ em đã tự làm hay cần xem hướng dẫn. Kết quả của chúng được giữ riêng với bài Kiểm tra này.

Nếu cần sửa, dùng [bảng Sửa lỗi](#sua-loi) để chọn đúng ý. Nhiệm vụ 24–27 giúp em tự kiểm tra từng chỗ còn vướng; làm đúng một ý chưa có nghĩa là đã làm được toàn bộ bài Kiểm tra. Nếu ý phù hợp đã được làm hoặc xem lời giải, ghi lại chỗ còn cần tự kiểm tra bằng bài khác. Giữ các bài Ôn lại cho đúng ngày đã hẹn.

<a id="on-lai"></a>

## Ôn lại

Tính lịch từ ngày hoàn tất lượt chính. Mỗi lượt dự kiến 20 phút. Tự làm trước khi đối chiếu; nếu phải nhận hỗ trợ, giữ phần đã tự làm và ghi riêng phần sau hỗ trợ. Không xem trước dữ liệu của lượt sau.

| Thời điểm ôn | Nhiệm vụ cần tự làm | Điểm dừng |
|---|---|---|
| Sau 2–3 ngày | Nhiệm vụ 19 — mẫu gốc | Điểm dừng 05 |
| Sau 7 ngày | Nhiệm vụ 20 — mẫu ghép nhóm | Điểm dừng 06 |
| Sau 3–4 tuần | Nhiệm vụ 21 — lựa chọn và giới hạn | Điểm dừng 07 |

<a id="nv19"></a>

### Nhiệm vụ 19 — Tìm lại các số đặc trưng

Mười hai chiều dài chân chèo đầu trong phần Chinstrap 2007, đơn vị mm:

$192;\ 196;\ 193;\ 188;\ 197;\ 198;\ 178;\ 197;\ 195;\ 198;\ 193;\ 194$.

a) Nêu cỡ mẫu, sắp dữ liệu và tính trung bình, trung vị, $Q_1,Q_3$.

b) Tìm tất cả các mốt. Có hợp lí không nếu chỉ ghi một mốt vì đề dùng từ “mốt”?

c) Viết một câu giải thích trung vị, giữ đúng phạm vi mẫu.

[Xem lời giải](#giai19).

<a id="dung05"></a>

#### Điểm dừng 05

Đối chiếu việc sắp thứ tự, vị trí và tần số. Lượt này giúp em biết còn nhớ cách đọc mẫu, tính các số đặc trưng từ dữ liệu gốc và tìm nhiều mốt hay không; chưa hỏi công thức ghép nhóm. Nếu còn nhầm, xem mục 2, rồi chọn ý phù hợp trong Nhiệm vụ 24 hoặc 25a để tự làm, với điều kiện chưa làm và chưa xem lời giải. Ghi ngày thực hiện rồi tiếp tục lịch ôn đã hẹn.

<a id="nv20"></a>

### Nhiệm vụ 20 — Tự chọn nhóm để nội suy

Phần trích Chinstrap 2008 có bảng chiều dài chân chèo:

| Khoảng, mm | Tần số |
|---|---:|
| $[175;180)$ | $0$ |
| $[180;185)$ | $0$ |
| $[185;190)$ | $3$ |
| $[190;195)$ | $2$ |
| $[195;200)$ | $5$ |
| $[200;205)$ | $4$ |
| $[205;210)$ | $2$ |
| $[210;215)$ | $2$ |

a) Xác định cỡ mẫu, lập tần số tích lũy và tính trung bình của mẫu ghép nhóm.

b) Tính $Q_1$, trung vị, $Q_3$ và mốt; ghi nhóm đã dùng.

c) Trung bình tính trực tiếp từ dữ liệu gốc khoảng $197{,}72$ mm. Việc trung bình từ bảng khác con số này có tự chứng minh bảng bị sai không?

[Xem lời giải](#giai20).

<a id="dung06"></a>

#### Điểm dừng 06

Kiểm lại phép nhân từng trung điểm với tần số, cách chọn nhóm để nội suy, tần số tích lũy trước nhóm và điều kiện dùng công thức mốt. Nếu đúng số nhưng chưa giải thích được $F$, xem mục 4 rồi tự làm ý phù hợp của Nhiệm vụ 25 nếu chưa làm và chưa xem lời giải. Lượt này không hỏi lại toàn bộ cách chọn số đại diện trong dữ liệu lượt thuê xe hoặc khí tượng.

<a id="nv21"></a>

### Nhiệm vụ 21 — Khi một mốt không kể hết câu chuyện

Phần trích Chinstrap 2009 có 24 chiều dài đã sắp, đơn vị mm:

$187;\ 187;\ 189;\ 190;\ 191;\ 193;\ 193;\ 194;\ 195;\ 196;\ 197;\ 198;\ 198;\ 199;\ 201;\ 201;\ 202;\ 202;\ 203;\ 203;\ 206;\ 207;\ 210;\ 212$.

Tổng là $4754$ mm. Ghép nhóm rộng $5$ mm từ $[185;190)$ đến $[210;215)$ cho các tần số $3;5;6;6;2;2$; các nhóm từ $175$ đến dưới $185$ có tần số $0$.

a) Tính trung bình, trung vị và nêu tất cả các mốt của mẫu gốc.

b) Nếu muốn một số mô tả vị trí giữa của 24 quan sát, em chọn số nào? Vì sao việc chọn tùy ý một mốt có thể che mất thông tin?

c) Nêu hai nhóm đông nhất. Có đủ căn cứ để khẳng định một nhóm chứa mốt duy nhất không? Không cần nội suy mốt khi hai nhóm cùng có tần số lớn nhất.

d) Sửa câu: “Mọi chim Chinstrap trên thế giới đều có chân chèo khoảng $198$ mm.”

[Xem lời giải](#giai21).

<a id="dung07"></a>

#### Điểm dừng 07

Đối chiếu phép tính, lý do chọn trung vị, cách nhận ra các giá trị hoặc nhóm cùng có tần số lớn nhất và phạm vi kết luận. Làm đúng lượt này cho thấy em làm được những việc vừa hỏi; các tình huống khác của chủ đề vẫn cần được luyện thêm. Nếu vừa phải sửa một nội dung, hẹn tự kiểm tra lại nội dung ấy sớm hơn; vẫn giữ ngày và bài làm của lần ôn này.



<a id="on-nen"></a>

## Ôn nền

Chỉ mở phần phù hợp với thao tác còn vướng. Các dãy số ngắn trong mục này là ví dụ số học được tạo để giải thích, không phải số liệu thu thập ngoài thực tế.

<a id="nen-tinh"></a>

### Tính với đủ số quan sát

Trung bình cộng bằng tổng chia cho số giá trị thực sự được tính. Với dãy minh họa $2;4;6$, ta có $\overline{x}=4$. Nếu giá trị $6$ chưa được ghi nhận, ta chỉ còn hai giá trị hợp lệ $2;4$, có trung bình $3$. Đưa một số $0$ vào chỗ thiếu sẽ tạo thành mẫu khác.

Nếu $3$ quan sát trong tổng $12$ thỏa điều kiện, tỉ lệ là $\frac{3}{12}=0{,}25=25\%$. Mẫu số là tổng số quan sát của câu hỏi đang xét.

<a id="nv22"></a>

#### Nhiệm vụ 22 — Tự kiểm tra phép tính cơ bản

Với dãy minh họa $4;6;8;10$:

a) Tính tổng và trung bình.

b) Có bao nhiêu phần trăm giá trị lớn hơn $7$?

c) Nếu ô cuối bị thiếu, mẫu dùng để tính còn bao nhiêu giá trị và có trung bình bao nhiêu? Không điền thay bằng $0$.

[Xem lời giải](#giai22).

**Đọc kết quả và học tiếp.** Kiểm lại xem em đã chia cho đúng số giá trị, tính tỉ lệ với đúng mẫu số và phân biệt ô thiếu với $0$ chưa. Nếu đã làm đúng, trở lại ý còn vướng ở Nhiệm vụ 01 hoặc bài đang làm. Bài ngắn này chỉ hỏi những phép tính cơ bản vừa ôn; các số đặc trưng khác còn cần tự kiểm tra ở bài tương ứng.

<a id="nen-khoang"></a>

### Đọc khoảng và giữ thứ tự

Khoảng $[a;b)$ gồm những số $x$ thỏa $a\leq x<b$. Với hai khoảng kề $[10;15)$ và $[15;20)$, số $15$ chỉ thuộc khoảng sau.

Sắp thứ tự không giảm nghĩa là giá trị đứng sau không nhỏ hơn giá trị đứng trước. Các giá trị trùng nhau vẫn phải giữ đủ số lần xuất hiện. Từ dãy minh họa $8;3;8;5$ ta được $3;5;8;8$, không phải $3;5;8$.

<a id="nv23"></a>

#### Nhiệm vụ 23 — Tự kiểm tra cách đọc khoảng

Dãy minh họa $9;15;10;14;15$ được chia vào $[5;10)$, $[10;15)$ và $[15;20)$.

a) Sắp dãy theo thứ tự không giảm.

b) Đếm tần số từng khoảng và kiểm tổng.

[Xem lời giải](#giai23).

**Đọc kết quả và học tiếp.** Kiểm lại xem em đã giữ cả hai giá trị $15$, xếp chúng vào đúng khoảng và có tổng tần số bằng số phần tử ban đầu chưa. Sau đó trở về ý đang vướng ở Nhiệm vụ 01, 09 hoặc bài em đang làm.

<a id="sua-loi"></a>

## Sửa lỗi

Trước hết giữ bài đã làm và tìm bước em còn vướng. Đọc lại giải thích hoặc ví dụ của đúng mục, rồi chọn một ý bên dưới hỏi đúng việc ấy để tự làm. Chọn ý em chưa làm và chưa xem lời giải; như vậy, kết quả mới cho biết em có tự giải được sau khi ôn hay không. Các dữ liệu Gentoo 2008–2009 và NOAA tháng 02/2023 được dành riêng cho phần Sửa lỗi.

Nếu một Điểm dừng khác dẫn đến bài em đã làm hoặc đã xem lời giải, hãy ghi rõ điều đó. Em vẫn có thể làm lại để luyện, nhưng kết quả chưa cho biết em có tự giải được một bài chưa gặp hay không. Nếu không còn bài phù hợp, ghi “cần một bài khác để tự kiểm tra phần này”, tiếp tục ôn chỗ còn vướng. Em có thể học tiếp những phần không cần đến kiến thức ấy và đã có đủ kiến thức để học. Giữ các bài Ôn lại cho đúng ngày đã hẹn.

| Nút thắt nhận thức | Biểu hiện dễ nhầm | Câu hỏi và cách tháo gỡ | Tự kiểm tra |
|---|---|---|---|
| Số dòng và số giá trị dùng được | Chia cho số dòng kể cả ô thiếu; thay thiếu bằng $0$ | Ô đó có thực sự chứa phép đo không? Xem [đọc dữ liệu](#hoc-doc), tách số dòng và số giá trị hợp lệ | Nhiệm vụ 26a |
| Vị trí và giá trị | Lấy vị trí giữa làm trung vị hoặc không sắp mẫu | Vị trí ấy mang giá trị nào? Xem [Ví dụ 01 trong mẫu gốc](#hoc-goc) | Nhiệm vụ 24a–b |
| Hai nửa khi cỡ mẫu lẻ | Đưa quan sát giữa vào cả hai nửa | Sau khi tách quan sát giữa, mỗi nửa còn mấy giá trị? Xem Ví dụ 02 | Nhiệm vụ 24c |
| Một mốt, nhiều mốt, không có mốt | Chọn tùy ý một số hoặc buộc mọi mẫu phải có mốt | Các tần số lớn nhất có bằng nhau không? Có nổi trội so với phần còn lại không? Xem [mốt mẫu gốc](#hoc-goc) | Nhiệm vụ 24b: một mốt; 25a: nhiều mốt; 26d: không có mốt |
| Đầu mút khoảng | Đếm đầu mút chung hai lần hoặc bỏ sót | Giá trị có thỏa dấu nhỏ hơn ở đầu phải không? Xem [ghép nhóm](#hoc-ghep) | Nhiệm vụ 25a |
| Trung điểm và quan sát | Cho rằng mọi giá trị trong nhóm đều bằng trung điểm | Bảng có còn cho từng giá trị không? Xem Ví dụ 03–04 | Nhiệm vụ 25b–c |
| Tần số trước nhóm và đến hết nhóm | Nội suy cho kết quả ra ngoài nhóm | Đã đi qua bao nhiêu quan sát trước khi vào nhóm? Xem Ví dụ 05 | Nhiệm vụ 25c |
| Điều kiện công thức mốt ghép nhóm | Dùng công thức khi các nhóm rộng khác nhau; thấy nhiều nhóm có cùng tần số lớn nhất nhưng vẫn kết luận chỉ có một mốt | Có đúng một nhóm có tần số lớn nhất và các nhóm rộng bằng nhau không? Xem Ví dụ 06 | Nhiệm vụ 25d; bài này chỉ hỏi trường hợp có đúng một nhóm có tần số lớn nhất |
| Số giá trị của từng nhóm khi tính trung bình chung | Lấy trung bình cộng của hai trung bình có cỡ mẫu khác nhau | Hai nhóm có bao nhiêu giá trị hợp lệ? Xem Ví dụ 07 | Nhiệm vụ 26b |
| Số 0 và ký hiệu ghi kèm | Đồng nhất số $0$ với không có hiện tượng; đồng nhất trung vị với tổng | Con số đang ghi là gì, ký hiệu bên cạnh cho biết thêm điều gì? Xem Ví dụ 09 | Nhiệm vụ 27 |
| Mẫu quan sát và kết luận tổng quát | Suy mọi cá thể, mọi ngày hoặc nguyên nhân từ một bảng mô tả | Những đối tượng và thời điểm nào thực sự được quan sát? Xem [chọn số đại diện](#hoc-chon) | Nhiệm vụ 26c, 27c |

Em có thể dùng các bài sau khi gặp khó ở Bài học, Luyện tập, sau khi kết thúc Kiểm tra hoặc khi Ôn lại. Chỉ chọn ý đúng với chỗ cần sửa theo hướng dẫn trên; không cần làm toàn bộ.

<a id="nv24"></a>

### Nhiệm vụ 24 — Tự làm với mẫu Gentoo nhỏ

Mười hai giá trị chiều dài chân chèo trong phần dữ liệu Gentoo 2008 dành cho Sửa lỗi, đơn vị mm:

$220;\ 220;\ 213;\ 219;\ 208;\ 208;\ 208;\ 225;\ 210;\ 216;\ 222;\ 217$.

a) Nêu cỡ mẫu và sắp thứ tự.

b) Tính trung bình, trung vị, $Q_1,Q_3$ và mốt. Chỉ rõ các vị trí đã dùng.

c) Với riêng 11 giá trị đầu trong danh sách ban đầu, tính lại ba tứ phân vị; giải thích cách tách hai nửa.

[Xem lời giải](#giai24).

**Đọc kết quả.** Ghi rõ những ý em đã tự làm đúng và những ý còn cần giúp đỡ. Trở về Điểm dừng 01, 04, 05 hoặc bài em đang làm trước khi mở Sửa lỗi. Nếu đã làm bài này hoặc xem lời giải từ trước, ghi đây là lần luyện lại.

<a id="nv25"></a>

### Nhiệm vụ 25 — Tự kiểm tra ghép nhóm và nội suy

Phần Gentoo 2008 còn lại có 34 chiều dài hợp lệ. Mười hai giá trị đầu của phần này là:

$210;\ 225;\ 213;\ 215;\ 210;\ 220;\ 210;\ 225;\ 217;\ 220;\ 208;\ 220$ mm.

a) Chỉ với 12 giá trị trên, lập tần số theo các khoảng rộng $5$ mm từ $[200;205)$ đến $[230;235)$. Tìm các mốt của mẫu 12 giá trị gốc.

Bảng sau dành cho **toàn bộ 34 giá trị**, không phải riêng 12 giá trị ở ý a:

| Khoảng, mm | Tần số |
|---|---:|
| $[200;205)$ | $0$ |
| $[205;210)$ | $4$ |
| $[210;215)$ | $6$ |
| $[215;220)$ | $7$ |
| $[220;225)$ | $11$ |
| $[225;230)$ | $3$ |
| $[230;235)$ | $3$ |

b) Giá trị đại diện của nhóm $[215;220)$ là bao nhiêu? Có thể nói bảy quan sát trong nhóm đều bằng giá trị đó không?

c) Tính trung bình, $Q_1$, trung vị và $Q_3$ của mẫu ghép nhóm. Giải thích trường hợp trung vị nằm đúng biên $220$ mm.

d) Tính mốt ghép nhóm, nêu điều kiện. Có thể gọi kết quả ấy là một chiều dài chắc chắn đã được ghi trong mẫu gốc không?

[Xem lời giải](#giai25).

**Đọc kết quả.** Ý a hỏi cách lập bảng và tìm nhiều mốt của mẫu gốc; ý b hỏi trung điểm; ý c hỏi cách tính trung bình theo tần số và nội suy; ý d hỏi mốt ghép nhóm. Làm đúng một ý chưa cho biết em đã làm được các ý còn lại. Trở về Điểm dừng 02, 04, 05, 06 hoặc bài em đang làm trước khi mở Sửa lỗi.

<a id="nv26"></a>

### Nhiệm vụ 26 — Đếm giá trị, tính trung bình và giới hạn kết luận

Phần dữ liệu Gentoo 2009 được chia theo thứ tự dòng trong bảng gốc thành hai phần:

| Phần | Số dòng | Số chiều dài hợp lệ | Tổng chiều dài hợp lệ, mm |
|---|---:|---:|---:|
| 20 dòng đầu | $20$ | $20$ | $4375$ |
| 24 dòng còn lại | $24$ | $23$ | $5017$ |

a) Toàn bộ phần trích có bao nhiêu dòng và bao nhiêu số đo chiều dài dùng được? Một ô thiếu có được coi là chiều dài $0$ mm không?

b) Tính trung bình mỗi phần và trung bình chung. Nêu số giá trị dùng để tính ở mỗi phần; giữ đủ chữ số trung gian.

c) Sửa câu: “Trung bình chung này cho biết chiều dài chân chèo của mọi chim Gentoo là như nhau.”

d) Bốn giá trị có trong phần trích là $212;\ 221;\ 224;\ 228$ mm. Xét riêng mẫu bốn giá trị này: có mốt không? Giải thích.

[Xem lời giải](#giai26).

**Đọc kết quả.** Ý a hỏi cách đếm khi có ô thiếu; ý b hỏi cách tính trung bình chung; ý c hỏi có thể kết luận về những cá thể nào; ý d hỏi trường hợp không có mốt. Trở về Điểm dừng 01, 03, 04, 07 hoặc bài em đang làm trước khi mở Sửa lỗi. Bốn giá trị ở ý d được chọn để luyện quy tắc tìm mốt, không được chọn ngẫu nhiên để đại diện cho cả loài.

<a id="nv27"></a>

### Nhiệm vụ 27 — Đọc ký hiệu T

Đoạn dữ liệu NOAA tại Seattle–Tacoma:

| Ngày | PRCP, mm | Ký hiệu T |
|---|---:|---|
| 09/02/2023 | $2{,}3$ | Không |
| 10/02/2023 | $0{,}0$ | Có |
| 11/02/2023 | $0{,}0$ | Không |

a) Tính tổng, trung bình và trung vị của ba giá trị số được ghi.

b) Có thể viết “cả hai ngày ghi $0$ đều được xác nhận hoàn toàn không có giáng thủy” không? Sửa câu cho đúng.

c) Kết quả trung vị bằng $0$ có cho phép bỏ qua ngày 09/02 khi mô tả ba ngày này hoặc kết luận cho cả năm không?

[Xem lời giải](#giai27).

**Đọc kết quả.** Cần đọc cả con số và ký hiệu ghi kèm, phân biệt trung vị với tổng, giới hạn kết luận trong ba ngày đã xét. Trở về Điểm dừng 03, 04 hoặc bài em đang làm trước khi mở Sửa lỗi. Bài này không hỏi lại toàn bộ nội dung về thống kê ghép nhóm.

<a id="nhat-ki"></a>

## Nhật kí

[Mở mẫu Nhật kí học tập dùng chung, gồm 14 mục cần ghi](../../../_dung_chung/nhat_ki_hoc_tap.qmd).

Ghi khi cần lưu một quyết định, nơi tiếp tục hoặc khi kết thúc buổi học. Chỉ điền thông tin đã có. Ghi riêng bài làm ban đầu, hướng dẫn hoặc giúp đỡ đã nhận, chỗ đã sửa và kết quả tự làm khi ôn lại sau một thời gian. Không bắt buộc ghi sau mọi câu.

Ở mục “Bài khắc phục mới”, ghi đúng tên nhiệm vụ và ý đã dùng; nếu đã xem trước lời giải, ghi rõ điều đó. Mẫu chung có ví dụ về một tình huống học được đặt ra ở gói khác để minh họa cách ghi; em không phải làm thêm bài trong ví dụ ấy.


<a id="loi-giai"></a>

## Lời giải

Giữ bài làm ban đầu trước khi mở phần tương ứng. Các ví dụ trong Bài học đã được giải tại chỗ; ở đây là lời giải của những nhiệm vụ tự làm. Lời giải Kiểm tra chỉ dùng sau khi kết thúc lượt.

### Bài học — Khởi động

<a id="giai01"></a>
<details>
<summary>Lời giải Nhiệm vụ 01 — Ba thao tác nền</summary>

a) Ba số đã theo thứ tự không giảm. Trung bình là $\frac{181+186+195}{3}=\frac{562}{3}\approx187{,}3$ mm.

b) $\frac{3}{12}\cdot100\%=25\%$.

c) $190\in[190;195)$ vì $190\leq190<195$. Khoảng $[185;190)$ không nhận đầu mút phải $190$.

[Xem đề bài](#nv01).

</details>

### Bài học — Các nhiệm vụ trong mạch học

<a id="giai02"></a>
<details>
<summary>Lời giải Nhiệm vụ 02 — Đếm đúng mẫu dùng để tính</summary>

a) Đơn vị quan sát là một cá thể chim; biến là chiều dài chân chèo; đơn vị đo mm.

b) Có $16$ giá trị hợp lệ nên phải chia cho $16$: $\overline{x}=\frac{3021}{16}=188{,}8125$ mm. Số $17$ là số dòng trong bảng, gồm cả dòng thiếu số đo chiều dài.

c) Sửa thành: “Dòng 4 chưa có số đo chiều dài chân chèo.” Không có căn cứ gán chiều dài bằng $0$.

[Xem đề bài](#nv02).

</details>

<a id="giai03"></a>
<details>
<summary>Lời giải Nhiệm vụ 03 — Vị trí và giá trị</summary>

a) $4{,}5$ diễn tả vị trí nằm giữa vị trí 4 và 5, không phải chiều dài. Hai giá trị ở đó là $182$ và $185$ mm, nên $Q_1=\frac{182+185}{2}=183{,}5$ mm.

b) Không. Với mẫu lẻ, quy ước của bài loại quan sát đứng giữa khỏi cả hai nửa. Đưa nó vào cả hai nửa là dùng quy ước khác, có thể làm thay đổi kết quả. Cần nêu và dùng nhất quán quy ước, không đổi theo đáp số mong muốn.

[Xem đề bài](#nv03).

</details>

<a id="giai04"></a>
<details>
<summary>Lời giải Nhiệm vụ 04 — Thông tin còn lại sau ghép nhóm</summary>

a) Có $4+3+5=12$ giá trị nhỏ hơn $195$ mm.

b) Không. Bảng chỉ cho biết năm giá trị thuộc $[190;195)$; trung điểm $192{,}5$ là giá trị đại diện dùng trong phép ước lượng.

c) Nếu chỉ mắc lỗi đếm $195$ hai lần, tổng tần số sẽ vượt $16$. Kiểm thêm quy tắc đầu mút để biết phải sửa ở nhóm nào, thay vì chỉ ép tổng về đúng số.

[Xem đề bài](#nv04).

</details>

<a id="giai05"></a>
<details>
<summary>Lời giải Nhiệm vụ 05 — Tự nội suy và giải thích kết quả</summary>

a) $r=\frac{3\cdot49}{4}=36{,}75$. Tần số tích lũy trước nhóm $[190;195)$ là $30$, đến hết nhóm là $40$, nên dùng $a=190$, $F=30$, $f=10$, $h=5$:

$$
Q_{3,\text{nhóm}}=190+\frac{36{,}75-30}{10}\cdot5=193{,}375\approx193{,}38\ \text{mm}.
$$

b) Phép tính $187{,}25$ đúng cho trung vị của mẫu ghép nhóm và được dùng làm ước lượng. Nó không khôi phục trung vị gốc $186$ mm. Sửa câu thành: “Từ bảng nhóm này, trung vị được ước lượng là $187{,}25$ mm; tính trực tiếp trên mẫu gốc cho $186$ mm.”

[Xem đề bài](#nv05).

</details>

<a id="giai06"></a>
<details>
<summary>Lời giải Nhiệm vụ 06 — Sửa câu kết luận</summary>

a) “Tháng 01/2012, dữ liệu ghi trung bình khoảng $3121$ lượt thuê mỗi ngày.” Không đổi lượt thuê thành người khác nhau.

b) “Tháng 01/2023 có $13$ ngày được ghi PRCP bằng $0$; trong đó $6$ ngày có ký hiệu vết giáng thủy.” Ký hiệu T bác bỏ cách hiểu rằng mọi số $0$ đều xác nhận hoàn toàn không có giáng thủy.

c) Chưa đủ căn cứ. Một tháng tại một trạm chỉ mô tả đúng phạm vi đó. Muốn kết luận về khí hậu lâu dài, cần dữ liệu của nhiều năm, kiểm tra xem cách đo qua các năm có so sánh được với nhau hay không và các trạm đo có đủ để nói về khu vực muốn xét hay không. Riêng bảng này chưa đủ.

[Xem đề bài](#nv06).

</details>

### Luyện tập — Chặng 1

<a id="giai07"></a>
<details>
<summary>Lời giải Nhiệm vụ 07 — Mẫu Adélie năm 2008</summary>

a) Một quan sát ứng với một cá thể Adélie; biến chiều dài chân chèo, đơn vị mm; $n=12$.

b) Dãy đã sắp:

$181;\ 185;\ 186;\ 186;\ 187;\ 188;\ 190;\ 191;\ 193;\ 194;\ 195;\ 200$.

Tổng $2276$ mm nên $\overline{x}=\frac{2276}{12}\approx189{,}67$ mm. Hai vị trí giữa là $6$ và $7$, mang giá trị $188$ và $190$, nên $M_e=189$ mm.

Mốt là $186$ mm, xuất hiện hai lần; các giá trị còn lại xuất hiện một lần. Trung vị $189$ mm nằm giữa hai giá trị chính giữa của mẫu đã sắp, không phải một chiều dài bắt buộc xuất hiện trong dữ liệu.

c) Trong mẫu 13 giá trị, $185$ và $186$ đều xuất hiện hai lần; các giá trị khác xuất hiện một lần. Mẫu có hai mốt $185$ và $186$ mm. Đây là mẫu đã thêm một quan sát, không phải đổi đáp án của mẫu 12 giá trị ở ý b.

[Xem đề bài](#nv07).

</details>

<a id="giai08"></a>
<details>
<summary>Lời giải Nhiệm vụ 08 — Tứ phân vị khi số quan sát thay đổi</summary>

a) Với 12 giá trị, nửa dưới có sáu giá trị, nửa trên có sáu giá trị:

$$
Q_1=\frac{x_3+x_4}{2}=\frac{186+186}{2}=186,\quad
Q_2=\frac{x_6+x_7}{2}=189,\quad
Q_3=\frac{x_9+x_{10}}{2}=\frac{193+194}{2}=193{,}5.
$$

b) Bỏ giá trị cuối $195$ của danh sách ban đầu, dãy 11 giá trị đã sắp là

$181;\ 185;\ 186;\ 186;\ 187;\ 188;\ 190;\ 191;\ 193;\ 194;\ 200$.

$Q_2=x_6=188$. Bỏ $x_6$ khi chia hai nửa; mỗi nửa có năm giá trị. $Q_1=186$, $Q_3=193$ mm.

c) Hai ý xét hai mẫu khác nhau. Giảm số quan sát làm thay đổi các vị trí và có thể làm thay đổi các số đặc trưng; không thể dùng đáp án của mẫu 11 giá trị thay cho mẫu 12 giá trị.

[Xem đề bài](#nv08).

</details>

### Luyện tập — Chặng 2

<a id="giai09"></a>
<details>
<summary>Lời giải Nhiệm vụ 09 — Tự lập bảng</summary>

| Khoảng, mm | Tần số | Trung điểm, mm | Tần số tích lũy |
|---|---:|---:|---:|
| $[180;185)$ | $1$ | $182{,}5$ | $1$ |
| $[185;190)$ | $5$ | $187{,}5$ | $6$ |
| $[190;195)$ | $4$ | $192{,}5$ | $10$ |
| $[195;200)$ | $1$ | $197{,}5$ | $11$ |
| $[200;205)$ | $1$ | $202{,}5$ | $12$ |

$190$ thuộc $[190;195)$, $200$ thuộc $[200;205)$. Tổng tần số $12$ khớp cỡ mẫu.

Trung điểm chỉ là đại diện của khoảng. Chỉ biết khoảng chứa một số đo thì chưa biết số đo ấy chính xác là bao nhiêu.

[Xem đề bài](#nv09).

</details>

<a id="giai10"></a>
<details>
<summary>Lời giải Nhiệm vụ 10 — Ước lượng trên mẫu lớn hơn</summary>

a) Tần số tích lũy lần lượt là $0;1;4;19;37;46;48;50;50$. Tổng các tích tần số với trung điểm là $9600$, nên $\overline{x}_{\text{nhóm}}=\frac{9600}{50}=192$ mm.

b) Các phép nội suy:

| Số cần tìm | Vị trí $r$ | Nhóm, mm | $F$ | $f$ | Kết quả, mm |
|---|---:|---|---:|---:|---:|
| $Q_1$ | $12{,}5$ | $[185;190)$ | $4$ | $15$ | $187{,}83$ |
| $M_e=Q_2$ | $25$ | $[190;195)$ | $19$ | $18$ | $191{,}67$ |
| $Q_3$ | $37{,}5$ | $[195;200)$ | $37$ | $9$ | $195{,}28$ |

Chẳng hạn $Q_{1,\text{nhóm}}=185+\frac{12{,}5-4}{15}\cdot5$. Với trung vị, dùng $190+\frac{25-19}{18}\cdot5$. Với $Q_3$, dùng $195+\frac{37{,}5-37}{9}\cdot5$.

c) Các nhóm đều rộng $5$ mm. Nhóm có tần số lớn nhất duy nhất là $[190;195)$, tần số $18$, hai bên là $15$ và $9$:

$$
M_{o,\text{nhóm}}=190+\frac{18-15}{(18-15)+(18-9)}\cdot5=191{,}25\ \text{mm}.
$$

d) Dữ liệu nhóm không giữ từng chiều dài. Dùng trung điểm và nội suy tạo các số đặc trưng dùng để ước lượng. Khác biệt với số gốc không tự chứng minh có lỗi tính toán.

[Xem đề bài](#nv10).

</details>

<a id="giai11"></a>
<details>
<summary>Lời giải Nhiệm vụ 11 — Độ rộng nhóm có quyết định mọi sai khác không?</summary>

a) Các trung điểm là $175;185;195;205$:

$$
\overline{x}_{\text{nhóm}}
=\frac{1\cdot175+18\cdot185+27\cdot195+4\cdot205}{50}
=\frac{9590}{50}=191{,}8\ \text{mm}.
$$

b) Bảng rộng $10$ mm cho $191{,}8$, cách trung bình gốc $191{,}04$ một lượng $0{,}76$ mm. Bảng rộng $5$ mm cho $192$, cách trung bình gốc $0{,}96$ mm. Trong mẫu này, kết quả từ nhóm rộng $10$ mm gần hơn.

c) Phát biểu “chắc chắn” là sai; chính mẫu đang xét là một phản ví dụ đối với số trung bình. Nhóm nhỏ hơn giữ vị trí trong khoảng hẹp hơn, nhưng độ gần của một số đặc trưng cụ thể còn phụ thuộc vị trí quan sát và biên nhóm. Không đảo thành quy tắc “nhóm rộng hơn luôn tốt hơn”.

[Xem đề bài](#nv11).

</details>

### Luyện tập — Chặng 3

<a id="giai12"></a>
<details>
<summary>Lời giải Nhiệm vụ 12 — Chọn số cho bản tóm tắt lượt thuê</summary>

a) $\overline{x}=\frac{103137}{29}\approx3556{,}45$ lượt/ngày. Số trung bình phù hợp với câu hỏi tổng lượt thuê chia đều cho mỗi ngày là bao nhiêu, vì tổng bằng số ngày nhân với trung bình chưa làm tròn.

b) Chọn trung vị $3777$ lượt/ngày để mô tả vị trí giữa khi xếp 29 ngày theo số lượt thuê. Điều này không nói tổng tháng bằng $29\cdot3777$.

c) Mọi giá trị đều xuất hiện một lần nên mẫu gốc không có mốt theo quy ước đã học. Lượt thuê không phải người dùng khác nhau; một người có thể thực hiện nhiều lượt.

[Xem đề bài](#nv12).

</details>

<a id="giai13"></a>
<details>
<summary>Lời giải Nhiệm vụ 13 — Trung bình của các nhóm</summary>

a) Trung bình nhóm ngày làm việc là $\frac{77403}{20}=3870{,}15$ lượt/ngày. Trung bình những ngày còn lại là $\frac{25734}{9}\approx2859{,}33$ lượt/ngày.

b) Mỗi ngày là một quan sát. Trung bình chung:

$$
\overline{x}
=\frac{77403+25734}{20+9}
=\frac{103137}{29}
\approx3556{,}45\ \text{lượt/ngày}.
$$

Nếu tính từ hai số trung bình nhóm, ta phải nhân chúng lần lượt với số ngày tương ứng là $20$ và $9$, cộng lại rồi chia cho tổng số ngày. Trung bình cộng đơn giản của hai trung bình nhóm chỉ khoảng $3364{,}74$ lượt/ngày, vì cách tính ấy coi hai nhóm có số ngày như nhau.

c) Có thể kết luận: “Trong phần dữ liệu tháng 02/2012, trung bình lượt thuê của nhóm ngày làm việc cao hơn nhóm còn lại.” Số lượt thuê còn có thể chịu ảnh hưởng của thời tiết, sự kiện và các yếu tố khác. Riêng bảng này chưa cho biết có phải vì là ngày làm việc mà số lượt thuê cao hơn hay không.

[Xem đề bài](#nv13).

</details>

<a id="giai14"></a>
<details>
<summary>Lời giải Nhiệm vụ 14 — Trung vị bằng 0</summary>

a) Tổng là $2{,}3$ mm nên trung bình $\frac{2{,}3}{31}\approx0{,}07$ mm/ngày. Khi sắp 31 giá trị, vị trí thứ 16 bằng $0$, nên trung vị bằng $0$ mm.

b) Sửa thành: “Trung vị bằng $0$ mm, nhưng tổng giá trị PRCP ghi nhận trong tháng là $2{,}3$ mm.” Trung vị không tính bằng tổng chia cho cỡ mẫu, cũng không quyết định tổng.

c) Có thể viết: “Tháng 07/2023 tại trạm Seattle–Tacoma có 30 ngày PRCP ghi bằng $0$ và ngày 24/07 ghi $2{,}3$ mm; trung vị bằng $0$ mm.” Câu này giữ cả hiện tượng phổ biến và ngày có giá trị dương. Không cần nhồi mọi số đặc trưng vào một câu.

[Xem đề bài](#nv14).

</details>

### Kiểm tra — Chỉ đối chiếu sau khi kết thúc lượt

<a id="giai15"></a>
<details>
<summary>Lời giải Nhiệm vụ 15 — Đọc, tính và ghép nhóm một mẫu mới</summary>

a) Mỗi quan sát là một cá thể Adélie trong phần trích 2009; biến chiều dài chân chèo, đơn vị mm, cỡ mẫu $12$.

b) Dãy đã sắp:

$181;\ 183;\ 184;\ 190;\ 190;\ 191;\ 192;\ 193;\ 197;\ 198;\ 199;\ 203$.

Tổng $2301$ mm nên $\overline{x}=\frac{2301}{12}=191{,}75$ mm.

$$
Q_1=\frac{x_3+x_4}{2}=\frac{184+190}{2}=187,\quad
M_e=Q_2=\frac{x_6+x_7}{2}=\frac{191+192}{2}=191{,}5,
$$
$$
Q_3=\frac{x_9+x_{10}}{2}=\frac{197+198}{2}=197{,}5.
$$

Đơn vị của các kết quả là mm. Mốt $190$ mm xuất hiện hai lần.

c) Tần số của các khoảng từ $[180;185)$ đến $[200;205)$ lần lượt là $3;0;5;3;1$, tổng $12$. Khoảng $[185;190)$ không chứa giá trị $190$.

[Xem đề bài](#nv15).

</details>

<a id="giai16"></a>
<details>
<summary>Lời giải Nhiệm vụ 16 — Bảng ghép nhóm Adélie 2009</summary>

a) Tần số tích lũy là $0;1;5;16;35;47;51;51;52$. Tổng các tích tần số với trung điểm là $10020$, nên

$$
\overline{x}_{\text{nhóm}}=\frac{10020}{52}\approx192{,}69\ \text{mm}.
$$

b) Với độ rộng $h=5$ mm:

| Số cần tìm | $r$ | Nhóm, mm | $a$ | $F$ | $f$ | Kết quả, mm |
|---|---:|---|---:|---:|---:|---:|
| $Q_1$ | $13$ | $[185;190)$ | $185$ | $5$ | $11$ | $188{,}64$ |
| $M_e=Q_2$ | $26$ | $[190;195)$ | $190$ | $16$ | $19$ | $192{,}63$ |
| $Q_3$ | $39$ | $[195;200)$ | $195$ | $35$ | $12$ | $196{,}67$ |

Các biểu thức lần lượt là $185+\frac{13-5}{11}\cdot5$, $190+\frac{26-16}{19}\cdot5$, $195+\frac{39-35}{12}\cdot5$.

c) Các nhóm rộng bằng nhau. Nhóm $[190;195)$ có tần số cao nhất duy nhất $19$, hai bên là $11$ và $12$:

$$
M_{o,\text{nhóm}}=190+\frac{19-11}{(19-11)+(19-12)}\cdot5\approx192{,}67\ \text{mm}.
$$

d) $210$ thuộc $[210;215)$, không thuộc $[205;210)$. Trung vị ở ý b được tính từ mẫu ghép nhóm và là ước lượng cho trung vị gốc; chỉ bảng nhóm không cho phép khẳng định bằng nhau chính xác.

[Xem đề bài](#nv16).

</details>

<a id="giai17"></a>
<details>
<summary>Lời giải Nhiệm vụ 17 — Số nào phù hợp với báo cáo?</summary>

a) $\overline{x}=\frac{164875}{31}\approx5318{,}55$ lượt/ngày. Chọn số trung bình để cho biết tổng lượt thuê chia đều cho mỗi ngày là bao nhiêu.

b) Chọn trung vị $5382$ lượt/ngày cho vị trí giữa khi sắp 31 ngày. Nó dựa vào vị trí thứ 16, trong khi trung bình dùng tổng của tất cả các ngày.

c) Mẫu không có mốt vì mọi giá trị có tần số bằng một. Chưa thể suy ra số người dùng khác nhau, hoặc khẳng định một ngày tương lai sẽ có đúng số lượt thuê bằng trung bình này. Em chỉ cần nêu một điều chưa thể kết luận và giải thích vì sao dữ liệu này chưa đủ.

[Xem đề bài](#nv17).

</details>

<a id="giai18"></a>
<details>
<summary>Lời giải Nhiệm vụ 18 — Đọc một tháng quan trắc</summary>

a) Trung bình $\frac{147}{30}=4{,}9$ mm/ngày. Khi sắp mẫu, vị trí thứ 15 là $0$, vị trí thứ 16 là $1{,}3$. Vì vậy

$$
M_e=\frac{0+1{,}3}{2}=0{,}65\ \text{mm}.
$$

Có 15 số $0$ trong 30 giá trị không làm trung vị tự động bằng $0$.

b) “Có 15 ngày được ghi PRCP bằng $0$; trong đó ngày 07/11 có ký hiệu vết giáng thủy.” Một số $0$ được ghi trong bảng chưa đủ để khẳng định hoàn toàn không có giáng thủy; cần đọc cả ký hiệu đi kèm.

c) Một tháng ở một trạm chưa đủ để suy ra xu thế dài hạn. Cần dữ liệu của nhiều năm, kiểm tra xem cách đo có so sánh được giữa các thời điểm hay không và các trạm đo có đủ để nói về khu vực muốn xét hay không.

[Xem đề bài](#nv18).

</details>

### Ôn lại

<a id="giai19"></a>
<details>
<summary>Lời giải Nhiệm vụ 19 — Tìm lại các số đặc trưng</summary>

a) $n=12$. Dãy đã sắp:

$178;\ 188;\ 192;\ 193;\ 193;\ 194;\ 195;\ 196;\ 197;\ 197;\ 198;\ 198$.

Tổng $2319$ mm nên $\overline{x}=193{,}25$ mm. $M_e=\frac{194+195}{2}=194{,}5$ mm; $Q_1=\frac{192+193}{2}=192{,}5$ mm; $Q_3=\frac{197+197}{2}=197$ mm.

b) Có ba mốt: $193$, $197$, $198$ mm, mỗi số xuất hiện hai lần. Chỉ ghi một số sẽ bỏ sót các giá trị cùng đạt tần số lớn nhất.

c) Có thể viết: “Trong 12 quan sát Chinstrap thuộc phần trích này, trung vị chiều dài chân chèo là $194{,}5$ mm.” Không thay “12 quan sát” bằng “mọi chim Chinstrap”.

[Xem đề bài](#nv19).

</details>

<a id="giai20"></a>
<details>
<summary>Lời giải Nhiệm vụ 20 — Tự chọn nhóm để nội suy</summary>

a) $n=18$. Tần số tích lũy là $0;0;3;5;10;14;16;18$. Tổng các tích của tần số với trung điểm là $3585$, nên $\overline{x}_{\text{nhóm}}=\frac{3585}{18}\approx199{,}17$ mm.

b) Các kết quả:

$$
Q_{1,\text{nhóm}}=190+\frac{4{,}5-3}{2}\cdot5=193{,}75\ \text{mm},
$$
$$
M_{e,\text{nhóm}}=195+\frac{9-5}{5}\cdot5=199\ \text{mm},
$$
$$
Q_{3,\text{nhóm}}=200+\frac{13{,}5-10}{4}\cdot5=204{,}375\approx204{,}38\ \text{mm}.
$$

Nhóm chứa mốt là $[195;200)$, tần số $5$, hai bên $2$ và $4$:

$$
M_{o,\text{nhóm}}=195+\frac{5-2}{(5-2)+(5-4)}\cdot5=198{,}75\ \text{mm}.
$$

c) Không. Trung bình từ bảng dùng trung điểm; khác trung bình gốc chưa chứng minh sai bảng. Cần kiểm lại cách đếm và tính nếu nghi ngờ, đồng thời giữ đúng ý nghĩa ước lượng.

[Xem đề bài](#nv20).

</details>

<a id="giai21"></a>
<details>
<summary>Lời giải Nhiệm vụ 21 — Khi một mốt không kể hết câu chuyện</summary>

a) $\overline{x}=\frac{4754}{24}\approx198{,}08$ mm. Hai vị trí giữa đều bằng $198$, nên $M_e=198$ mm. Sáu mốt là $187$, $193$, $198$, $201$, $202$, $203$ mm; mỗi số xuất hiện hai lần.

b) Chọn trung vị $198$ mm cho câu hỏi về vị trí giữa. Một mốt được chọn tùy ý bỏ qua năm mốt còn lại, và không nhất thiết trả lời câu hỏi về vị trí giữa.

c) Hai nhóm đông nhất là $[195;200)$ và $[200;205)$, cùng có sáu quan sát. Cả hai nhóm cùng có tần số lớn nhất, nên không tùy ý bỏ qua một nhóm. Ý này không yêu cầu tính mốt ghép nhóm khi hai nhóm cùng có tần số lớn nhất.

d) “Trong phần trích 24 quan sát Chinstrap năm 2009, trung vị chiều dài chân chèo là $198$ mm.” Trung vị không nói các chiều dài bằng nhau; mẫu tại địa điểm và giai đoạn xác định cũng không đại diện mặc nhiên cho toàn thế giới.

[Xem đề bài](#nv21).

</details>

### Ôn nền

<a id="giai22"></a>
<details>
<summary>Lời giải Nhiệm vụ 22 — Tự kiểm tra phép tính cơ bản</summary>

a) Tổng $4+6+8+10=28$, trung bình $\frac{28}{4}=7$.

b) Hai giá trị lớn hơn $7$ là $8$ và $10$, chiếm $\frac{2}{4}=50\%$.

c) Còn ba giá trị $4;6;8$, trung bình $\frac{18}{3}=6$. Ô thiếu không thêm một số $0$ vào mẫu.

[Xem đề bài](#nv22).

</details>

<a id="giai23"></a>
<details>
<summary>Lời giải Nhiệm vụ 23 — Tự kiểm tra cách đọc khoảng</summary>

a) Dãy đã sắp: $9;10;14;15;15$.

b) Tần số lần lượt là $1;2;2$, tổng $5$. Số $10$ thuộc $[10;15)$; cả hai số $15$ thuộc $[15;20)$.

[Xem đề bài](#nv23).

</details>

### Sửa lỗi — Đối chiếu đúng ý đã tự làm

<a id="giai24"></a>
<details>
<summary>Lời giải Nhiệm vụ 24 — Tự làm với mẫu Gentoo nhỏ</summary>

a) $n=12$. Dãy đã sắp:

$208;\ 208;\ 208;\ 210;\ 213;\ 216;\ 217;\ 219;\ 220;\ 220;\ 222;\ 225$.

b) Tổng $2586$ mm nên $\overline{x}=215{,}5$ mm.

$$
Q_1=\frac{x_3+x_4}{2}=\frac{208+210}{2}=209,\quad
M_e=Q_2=\frac{x_6+x_7}{2}=216{,}5,\quad
Q_3=\frac{x_9+x_{10}}{2}=220.
$$

Các kết quả có đơn vị mm. Mốt là $208$ mm, xuất hiện ba lần.

c) Bỏ giá trị cuối $217$ của danh sách ban đầu. Dãy còn 11 giá trị, trung vị ở vị trí thứ 6 bằng $216$. Hai nửa đều có năm giá trị và không gồm quan sát giữa; trung vị của nửa dưới là $208$, của nửa trên là $220$. Vậy $Q_1=208$, $Q_2=216$, $Q_3=220$ mm.

[Xem đề bài](#nv24).

</details>

<a id="giai25"></a>
<details>
<summary>Lời giải Nhiệm vụ 25 — Tự kiểm tra ghép nhóm và nội suy</summary>

a) Với riêng 12 giá trị, tần số theo bảy khoảng từ $[200;205)$ đến $[230;235)$ là $0;1;4;2;3;2;0$. Tổng bằng $12$. Hai mốt gốc là $210$ và $220$ mm, mỗi số xuất hiện ba lần.

b) Trung điểm của $[215;220)$ là $217{,}5$ mm. Bảng không cho biết cả bảy quan sát của nhóm đều bằng trung điểm.

c) Với toàn bộ 34 giá trị, tần số tích lũy là $0;4;10;17;28;31;34$. Tổng các tích tần số với trung điểm là $7455$:

$$
\overline{x}_{\text{nhóm}}=\frac{7455}{34}\approx219{,}26\ \text{mm}.
$$

$$
Q_{1,\text{nhóm}}=210+\frac{8{,}5-4}{6}\cdot5=213{,}75\ \text{mm},
$$
$$
M_{e,\text{nhóm}}=215+\frac{17-10}{7}\cdot5=220\ \text{mm},
$$
$$
Q_{3,\text{nhóm}}=220+\frac{25{,}5-17}{11}\cdot5\approx223{,}86\ \text{mm}.
$$

Vị trí trung vị $17$ bằng tần số tích lũy đến hết nhóm $[215;220)$. Nội suy từ nhóm kế tiếp cũng cho $220+\frac{17-17}{11}\cdot5=220$. Đây là biên chung, không phải lý do để đếm một quan sát vào hai nhóm.

d) Các nhóm rộng đều $5$ mm; nhóm $[220;225)$ có tần số lớn nhất duy nhất $11$:

$$
M_{o,\text{nhóm}}=220+\frac{11-7}{(11-7)+(11-3)}\cdot5\approx221{,}67\ \text{mm}.
$$

Đây là kết quả nội suy từ bảng; không chứng minh có một quan sát mang đúng giá trị ấy.

[Xem đề bài](#nv25).

</details>

<a id="giai26"></a>
<details>
<summary>Lời giải Nhiệm vụ 26 — Đếm giá trị, tính trung bình và giới hạn kết luận</summary>

a) Có $44$ dòng, với $43$ số đo chiều dài dùng được và một ô thiếu. Ô thiếu không phải một phép đo bằng $0$.

b) Trung bình hai phần lần lượt là $\frac{4375}{20}=218{,}75$ mm và $\frac{5017}{23}\approx218{,}13$ mm. Trung bình chung:

$$
\overline{x}=\frac{4375+5017}{20+23}=\frac{9392}{43}\approx218{,}42\ \text{mm}.
$$

Nếu tính từ hai số trung bình riêng, cần nhân chúng với số giá trị dùng được của từng phần là $20$ và $23$, cộng lại rồi chia cho tổng số giá trị. Không dùng $20$ và $24$, vì phần sau có một ô thiếu; cũng không chỉ cộng hai số trung bình rồi chia đôi.

c) “Trong 43 giá trị hợp lệ của phần trích Gentoo 2009, chiều dài chân chèo trung bình khoảng $218{,}42$ mm.” Trung bình không làm mọi quan sát bằng nhau và không tự mở rộng phạm vi ra mọi cá thể Gentoo.

d) Bốn giá trị phân biệt đều xuất hiện một lần nên mẫu bốn giá trị không có mốt theo quy ước đang dùng.

[Xem đề bài](#nv26).

</details>

<a id="giai27"></a>
<details>
<summary>Lời giải Nhiệm vụ 27 — Đọc ký hiệu T</summary>

a) Tổng các giá trị đã ghi là $2{,}3$ mm. Trung bình $\frac{2{,}3}{3}\approx0{,}77$ mm/ngày. Dãy sắp là $0;0;2{,}3$, nên trung vị bằng $0$ mm.

b) Không. Ngày 10/02 có ký hiệu T, cho biết vết giáng thủy. Có thể viết: “Hai ngày có giá trị PRCP ghi bằng $0$; riêng ngày 10/02 được gắn ký hiệu vết giáng thủy.” Không xóa ký hiệu khi diễn giải.

c) Trung vị bằng $0$ không xóa giá trị dương ngày 09/02 và không làm tổng bằng $0$. Ba ngày cũng chưa đủ để mô tả cả năm.

[Xem đề bài](#nv27).

</details>

<a id="nguon"></a>

## Nguồn và cách dùng dữ liệu

### Tài liệu toán học

- **Toán 10, Tập một — Kết nối tri thức với cuộc sống**, Nhà xuất bản Giáo dục Việt Nam, Bài 13, trang 78–81: trung bình, trung vị, tứ phân vị và mốt của mẫu chưa ghép nhóm.
- **Toán 11, Tập một — Kết nối tri thức với cuộc sống**, Nhà xuất bản Giáo dục Việt Nam, Bài 8, trang 58–60; Bài 9, trang 62–66: mẫu ghép nhóm, các số đặc trưng và điều kiện áp dụng.

Lời giảng, nhiệm vụ và lời giải trong gói do ZO Math biên soạn; không sao chép bài tập hoặc hình sách.

### Palmer Penguins

[Trang dữ liệu và mô tả biến](https://allisonhorst.github.io/palmerpenguins/reference/penguins.html) · [CSV](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv) · [CC0 1.0](https://allisonhorst.github.io/palmerpenguins/LICENSE.html).

Ghi công Allison Horst, Alison Hill, Kristen Gorman; dữ liệu gốc Kristen Gorman và Palmer Station LTER, các bộ dữ liệu EDI được dẫn ở trang nguồn. Nghiên cứu liên quan: Gorman, Williams và Fraser (2014), [Ecological Sexual Dimorphism and Environmental Variability within a Community of Antarctic Penguins](https://doi.org/10.1371/journal.pone.0090081).

ZO Math chọn biến chiều dài chân chèo và các phần theo loài, năm; giữ ô thiếu trong hồ sơ dữ liệu, loại đúng ô thiếu khỏi phép tính tương ứng; lập bảng và làm tròn kết quả cuối. Các phần trích nhỏ phục vụ học thao tác, không được coi là mẫu ngẫu nhiên của toàn bộ loài.

### Bike Sharing

Fanaee-T, H. và Gama, J., [Bike Sharing — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset), [DOI dữ liệu](https://doi.org/10.24432/C5W894), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

ZO Math dùng day.csv, chọn các cột ngày, số lượt thuê và thông tin cho biết ngày đó có phải ngày làm việc hay không; trích theo tháng, tính tổng và các số đặc trưng, dịch nhãn sang tiếng Việt. Không thay các giá trị quan sát. Việc ghi công không hàm ý tác giả hoặc UCI bảo trợ học liệu.

Dữ liệu mô tả một hệ thống thuê xe và giai đoạn cụ thể. Không dùng lượt thuê để suy trực tiếp số người khác nhau, năng lực phục vụ cần có ở mọi thời điểm hoặc nguyên nhân của sự khác biệt.

### NOAA/NCEI

Menne và cộng sự, [GHCN-Daily, Version 3](https://doi.org/10.7289/V5D21VHZ), [giải thích các cột và ký hiệu trong dữ liệu](https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt), [thông tin trạm USW00024233](https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00024233/detail).

Phần dùng trong gói là PRCP năm 2023 của trạm Hoa Kỳ này. Dữ liệu được lấy từ NCEI theo hệ mét, giữ nguyên các ký hiệu ghi kèm số đo. Các số trung bình và tổng tính trên giá trị đã ghi; không tự gán lượng nước cho ký hiệu T.

[Chính sách dữ liệu mở của NCEI](https://www.ncei.noaa.gov/sites/default/files/2023-12/NCEI%20PD-10-2-02%20-%20Open%20Data%20Policy%20Signed.pdf) phân biệt dữ liệu chính phủ Hoa Kỳ thuộc phạm vi công cộng với dữ liệu bên thứ ba có thể có điều kiện riêng. Không suy rằng mọi dữ liệu trên NCEI đều mang CC0. Học liệu chỉ sử dụng phần dữ liệu trạm Hoa Kỳ đã nêu, không sử dụng logo hoặc ảnh của cơ quan.

Các nguồn dữ liệu được truy cập ngày 22/10/2026. Mọi kết luận trong gói cần giữ đúng đơn vị, phần mẫu và thời điểm đang xét.

