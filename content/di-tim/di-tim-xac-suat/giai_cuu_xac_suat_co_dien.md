Kết nối dòng chảy lịch sử–triết học từ **de Moivre → Laplace → Kolmogorov → xác suất hình học**. Bài viết giữ giọng văn “học thuật tĩnh tại” đặc trưng của ZO Math.

---

# Giải cứu xác suất cổ điển: Từ công thức đếm-chia đến tri thức về bất định

Trong chương trình Toán phổ thông, xác suất thường được mở đầu bằng một công thức giản dị:

\[
P(A) = \frac{n(A)}{n(\Omega)}.
\]

Ta học rằng đây là *cách tính xác suất cổ điển* - số trường hợp thuận lợi chia cho tổng số trường hợp có thể.

Từ công thức ấy, học sinh bước vào hàng loạt bài toán “tung xúc xắc”, “rút bài”, “chọn bi”, “bốc thăm”. Tưởng như mọi điều đã rõ ràng. Nhưng đằng sau công thức nhỏ bé đó là một *hành trình triết học hơn hai thế kỷ*, và nếu bỏ qua, ta đánh mất chính linh hồn của lý thuyết xác suất.

## 1. De Moivre: Xác suất như sự công bằng của cơ hội

Năm 1718, Abraham de Moivre viết trong *The Doctrine of Chances* rằng:

> "If we constitute a fraction whereof the numerator be the number of chances whereby an event may happen, and the denominator the number of all the chances whereby it may either happen or fail, that fraction will be a proper designation of the probability of happening."

> "Nếu ta lập một phân số mà tử số là số cơ hội để một biến cố có thể xảy ra, còn mẫu số là tổng số cơ hội khiến nó có thể xảy ra hoặc không xảy ra, thì phân số đó chính là xác suất của việc nó xảy ra."

Đó chính là công thức trong sách giáo khoa hôm nay. Nhưng ở thời de Moivre, từ *chance* chỉ đơn giản là “một kết quả có thể”, và ông *ngầm giả định* rằng các “cơ hội” ấy *bằng nhau* - vì ông đang nghĩ đến trò chơi công bằng: xúc xắc, đồng xu, bài.

Ở đây, xác suất không phải là *nhận thức*, mà là *sự đối xứng của thế giới*.Đếm các khả năng chính là *đếm công bằng vật lý*.


## 2. Laplace: Xác suất như thước đo của tri thức

Gần một thế kỷ sau, Pierre-Simon Laplace viết lại định nghĩa ấy trong *Essai philosophique sur les probabilités* (1814), 

> "The theory of chances consists in reducing all events of the same kind to a certain number of equally possible cases, that is to say, to cases whose existence we are equally uncertain of, and in determining the number of cases favourable to the event whose probability is sought. The ratio of this number to that of all possible cases is the measure of this probability, which is thus only a fraction whose numerator is the number of favourable cases, and whose denominator is the number of all possible cases."

> "Lý thuyết về cơ hội bao gồm việc quy mọi biến cố cùng loại về một số lượng hữu hạn các trường hợp đồng khả năng (equally possible cases), tức là những trường hợp mà ta *bất định như nhau* về sự tồn tại của chúng, rồi xác định số trường hợp thuận lợi cho biến cố mà ta muốn tìm xác suất. Tỷ số giữa số trường hợp thuận lợi này và tổng số trường hợp có thể chính là thước đo của xác suất ấy - một phân số có tử là số thuận lợi và mẫu là tổng số các trường hợp khả dĩ."

và ông thêm vào một mệnh đề nhỏ nhưng làm thay đổi tất cả:

> "... những trường hợp đồng khả năng là những trường hợp mà ta *bất định như nhau về sự tồn tại của chúng*."

Câu này là *sự ra đời của Nguyên lý thờ ơ (Principle of Indifference)*. Đối xứng không còn là thuộc tính của xúc xắc, mà là *trạng thái tri thức của con người*: ta gán cho các khả năng những xác suất bằng nhau *vì ta không có lý do nào để thiên vị*.

Laplace đã nâng xác suất từ “đếm cơ học” lên “lý trí khi đối diện với bất định”. Từ đây, xác suất cổ điển trở thành *một hình thức của tri thức* -
một phép đo của “biết ít” chứ không phải của “ngẫu nhiên vật lý”.


## 3. Kolmogorov: Từ tri thức sang cấu trúc

Đến thế kỷ XX, Andrei Kolmogorov (1933) đưa xác suất vào hình thức tiên đề hóa. Ông không định nghĩa xác suất là gì; ông chỉ định nghĩa *cách nó phải hoạt động*: phi âm, chuẩn hóa, cộng hữu hạn, và (nếu mở rộng) cộng đếm được.

Điều đáng chú ý: Kolmogorov *giữ im lặng* về việc xác suất được gán *như thế nào* cho các phần tử ban đầu. Chính vì thế, *de Moivre và Laplace* vẫn là hai “nguồn” để ta rót giá trị vào hàm \(P\):

* Khi có *đối xứng vật lý*, ta gán đồng đều (tinh thần de Moivre).
* Khi có *đối xứng tri thức*, ta gán đồng đều (tinh thần Laplace).

Cả hai đều sống bên trong khung Kolmogorov - một bên là *vật lý của trò chơi công bằng*, một bên là *lô-gic của tri thức công bằng*.


## 4. Xác suất hình học: Độ đo của sự chia đều

Sách giáo khoa hiện nay thường tách riêng phần “xác suất hình học” với công thức:

\[
P(A) = \frac{\text{độ dài (diện tích, thể tích) phần thuận lợi}}{\text{độ dài (diện tích, thể tích) toàn bộ}}.
\]

Nhưng thật ra, đó vẫn là *xác suất cổ điển* - chỉ khác là “đếm” được thay bằng “đo”. Khi ta không còn đếm được từng phần tử, ta *chia đều theo độ đo liên tục*.

Laplace đã lường trước điều này: nếu ta bất định như nhau về vị trí của một điểm trong đoạn thẳng, ta nên chia đều độ dài của đoạn - đó chính là xác suất hình học.

Xác suất hình học, vì thế, *không tách rời khỏi cổ điển*, mà là *mở rộng của nguyên lý thờ ơ sang không gian liên tục*. Nó không phải chương phụ, mà là *mạch tiếp nối tự nhiên*.


## 5. Vì sao điều này quan trọng

Khi ta hiểu rằng: de Moivre dạy ta *cách đếm*, Laplace dạy ta *vì sao được đếm đều*, Kolmogorov dạy ta *hình thức hóa cách đếm ấy*, thì xác suất không còn là mẹo chia tỉ lệ, mà trở thành *một ngôn ngữ thống nhất giữa tri thức và thế giới*.

Khi ấy, học sinh không chỉ biết tính \(P(A)\), mà còn biết *vì sao phép tính ấy hợp lý*. Và giáo viên không chỉ dạy công thức, mà đang dạy một cách *suy nghĩ về sự công bằng và bất định* - tinh thần thật sự của xác suất.


## 6. Tóm lại

| Giai đoạn        | Nhân vật          | Bản chất “chia đều” | Ý nghĩa triết học                   |
| ---------------- | ----------------- | ------------------- | ----------------------------------- |
| Thế kỷ XVIII | de Moivre         | Đối xứng vật lý     | Trò chơi công bằng                  |
| Thế kỷ XIX   | Laplace           | Đối xứng tri thức   | Nguyên lý thờ ơ – bất định như nhau |
| Thế kỷ XX   | Kolmogorov        | Cấu trúc tiên đề    | Khung hình thức cho mọi diễn giải   |
| Mở rộng      | Xác suất hình học | Độ đo liên tục      | Sự nối dài tự nhiên của cổ điển     |


> *“Probability is common sense reduced to calculation.”* - Laplace
>
> Xác suất, hiểu theo tinh thần cổ điển, không chỉ là trò chơi của con số, mà là phép đo của sự công bằng trong nhận thức - nơi lý trí, giữa bóng tối của bất định, chia đều ánh sáng hiểu biết cho mọi khả năng có thể.

