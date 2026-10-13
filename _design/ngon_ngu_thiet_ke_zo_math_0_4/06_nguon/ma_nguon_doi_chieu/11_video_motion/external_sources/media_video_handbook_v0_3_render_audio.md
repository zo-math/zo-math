# Sổ tay sản xuất video toán học ZO Math

**Phiên bản:** v0.3 — bản biên tập vận hành  
**Trạng thái:** bản dùng để sản xuất video, rút gọn khỏi các ghi chú không phục vụ trực tiếp công việc  
**Mục đích:** thống nhất quy trình sản xuất video toán học ZO Math từ ý tưởng, bài luận hoặc hồ sơ ban đầu đến kịch bản nói, kịch bản video, Manim, voice-over, dựng hậu kì và bản final.

---

## Mục lục

0. Nguyên tắc vận hành
1. Thuật ngữ sản xuất cần dùng thống nhất
2. Quy trình sản xuất chuẩn
3. Chọn phạm vi và chốt vấn đề trung tâm
4. Viết kịch bản nói
5. Thiết kế kịch bản video
6. Sản xuất video bằng Manim
7. Thu voice-over
8. Dựng hậu kì bằng DaVinci Resolve
9. Kiểm duyệt trước khi xuất bản
10. Lưu trữ, đặt tên file và phiên bản hóa
11. Mẫu hồ sơ sản xuất
12. Mẫu file Manim
13. Lỗi thường gặp và cách xử lí
14. Checklist sản xuất
15. Prompt làm việc với ChatGPT
16. Cập nhật sổ tay sau mỗi video

---

## 0. Nguyên tắc vận hành

Video ZO Math được sản xuất để giúp người học nhìn thấy, nghe thấy và hiểu rõ một ý tưởng toán học. Mọi quyết định về lời nói, công thức, hình ảnh, chuyển động, khoảng dừng, âm thanh và dựng hậu kì đều phải phục vụ mạch hiểu đó.

Nguyên tắc gốc:

```text
Kịch bản nói là xương sống nhận thức.
Kịch bản video là bản thiết kế nghe–nhìn.
Manim là bảng toán học động.
Voice-over là dòng dẫn chính.
DaVinci Resolve là bàn dựng hoàn thiện.
```

Không làm hình trước rồi cố viết lời theo hình. Không sửa Manim để cứu một kịch bản nói chưa chốt. Không thêm chuyển động chỉ vì đẹp. Không để chữ trên màn hình cạnh tranh với lời đọc. Không biến video thành phụ đề chạy chữ.

Trình tự ưu tiên khi sản xuất:

```text
Ý tưởng / bài luận / hồ sơ ban đầu
→ phạm vi video
→ vấn đề trung tâm
→ mạch bài giảng
→ kịch bản nói
→ kịch bản video
→ Manim
→ voice-over
→ dựng hậu kì
→ kiểm duyệt
→ final
```

Khi có suy nghĩ mới giữa chừng, không sửa ngay trong Manim. Phải quay lại kiểm tra ở cấp kịch bản nói. Nếu ý mới làm mạch nhận thức rõ hơn thì tích hợp vào kịch bản nói, rồi đồng bộ lại kịch bản video, hồ sơ và Manim.

---

## 1. Thuật ngữ sản xuất cần dùng thống nhất

### 1.1. Bài luận

Bài luận là văn bản nguồn có mạch lập luận đầy đủ. Nó có thể dài, giàu diễn giải và có nhiều nhánh phụ. Video không đọc lại bài luận, mà chuyển hóa bài luận thành trải nghiệm nghe–nhìn.

### 1.2. Phạm vi video

Phạm vi video là phần nội dung được chọn để sản xuất thành một video. Một video có thể bao quát toàn bộ bài luận hoặc chỉ một phần, miễn là phần đó tạo thành một đơn vị nhận thức độc lập.

### 1.3. Vấn đề trung tâm

Vấn đề trung tâm là câu hỏi hoặc căng thẳng nhận thức mà video cần làm sáng rõ. Mọi cảnh trong video phải phục vụ vấn đề trung tâm.

Ví dụ dạng tốt:

```text
Khi một công cụ báo bài viết có dấu hiệu do AI viết, ta có nên tin ngay không?
```

Không nên đặt vấn đề trung tâm quá rộng, chẳng hạn:

```text
Tìm hiểu toàn bộ xác suất có điều kiện.
```

### 1.4. Mạch bài giảng

Mạch bài giảng là đường đi nhận thức của người xem. Nó cho biết người xem bắt đầu từ đâu, gặp điều gì, nhìn thấy dữ kiện nào, thay đổi câu hỏi ra sao, và kết luận điều gì.

Dạng cơ bản:

```text
Mở vấn đề
→ chất liệu làm việc
→ quá trình luận
→ ý tưởng hình thành
→ kết luận nhận thức
```

### 1.5. Kịch bản nói

Kịch bản nói là văn bản dùng để thu voice-over. Nó phải đọc tự nhiên, câu ngắn, rõ, có nhịp. Đây là nơi chốt mạch nhận thức trước khi chuyển sang hình ảnh.

### 1.6. Kịch bản video

Kịch bản video là bản thiết kế từng cảnh. Mỗi cảnh cần có lời đọc, màn hình, chuyển động và ghi chú nhịp.

### 1.7. Hồ sơ sản xuất

Hồ sơ sản xuất là tài liệu trung tâm của một video. Nó chứa thông tin chung, vấn đề trung tâm, phạm vi, mạch bài giảng, kịch bản nói, kịch bản video, đường dẫn file, nhật kí sản xuất và checklist.

### 1.8. Manim

Manim là công cụ tạo hoạt hình toán học. Trong ZO Math, Manim không thay thế kịch bản nói. Manim chỉ hiển thị những điểm tựa thị giác cần thiết để người xem theo được mạch nghe.

### 1.9. Preview

Preview là bản xem thử để kiểm tra mạch, hình, lời, nhịp, bố cục, lỗi chữ, lỗi công thức và lỗi dựng. Preview chưa phải bản xuất bản.

### 1.10. Final

Final là bản đã qua kiểm duyệt và sẵn sàng xuất bản. Nếu sau final còn sửa, phải tạo phiên bản final mới và ghi lí do trong nhật kí sản xuất.

---

## 2. Quy trình sản xuất chuẩn

### 2.1. Công đoạn 1 — lập hồ sơ sản xuất

Mỗi video phải có một hồ sơ riêng trước khi viết Manim.

Hồ sơ tối thiểu gồm:

```text
1. Thông tin chung
2. Vấn đề trung tâm
3. Phạm vi chuyển hóa
4. Mạch bài giảng
5. Kịch bản nói
6. Kịch bản video
7. File sản xuất
8. Nhật kí sản xuất
9. Checklist trước khi xuất bản
```

Không làm việc với các file rời rạc nếu chưa có hồ sơ. Hồ sơ là nơi xác định video đang ở công đoạn nào và vì sao nó được sửa.

### 2.2. Công đoạn 2 — chọn phạm vi

Nếu nguồn là một bài luận dài, không mặc định biến toàn bộ bài luận thành một video. Trước hết phải hỏi:

```text
Video này cần làm rõ điều gì?
Phần nào của bài luận đủ để làm rõ điều đó?
Phần được chọn có tạo thành một mạch hiểu độc lập không?
Nếu cắt ở đây, người xem có thiếu nền để hiểu không?
Nếu giữ thêm, video có bị rườm rà không?
```

Một video tốt không nhất thiết chứa nhiều ý. Nó phải chứa đủ ý để người xem đi trọn một bước hiểu.

### 2.3. Công đoạn 3 — chốt mạch bài giảng

Trước khi viết kịch bản nói, phải chốt mạch bài giảng. Mạch bài giảng nên được trình bày bằng các bước ngắn.

Ví dụ:

```text
1. Một công cụ báo bài viết có dấu hiệu do AI viết.
2. Phản ứng tự nhiên là tin ngay.
3. Nhưng cần hiểu kết quả đó được tạo ra trong tình huống nào.
4. Xét nhóm bài thật sự do AI viết và nhóm bài do học sinh tự viết.
5. Tính số bài bị báo là AI từ hai nguồn.
6. Đọc lại kết quả trong chính nhóm bị báo là AI.
7. Kết luận: kết quả kiểm tra là tín hiệu, không phải phán quyết.
```

### 2.4. Công đoạn 4 — viết kịch bản nói

Kịch bản nói phải được chốt trước khi thiết kế video. Nếu kịch bản nói còn thay đổi về lập luận, chưa nên viết Manim.

Khi viết kịch bản nói:

```text
mỗi cảnh chỉ làm một việc chính;
mỗi câu chỉ nên đẩy mạch đi một bước;
từ ngữ dùng ít và nhất quán;
không phô trương thuật ngữ;
không mở nhánh phụ nếu nhánh đó không phục vụ vấn đề trung tâm;
không nói sớm ý của cảnh sau;
không lặp lại một ý đã đủ rõ.
```

### 2.5. Công đoạn 5 — thiết kế kịch bản video

Kịch bản video chuyển kịch bản nói thành cảnh. Mỗi cảnh gồm:

```text
Lời đọc
Màn hình
Chuyển động
Ghi chú nhịp
```

Kịch bản video không được tự thêm ý mới ngoài kịch bản nói. Nếu phát hiện cần thêm ý, quay lại sửa kịch bản nói trước.

### 2.6. Công đoạn 6 — viết và render Manim

Chỉ viết Manim sau khi kịch bản video đã ổn. Khi viết Manim:

```text
dùng nền đen;
dùng chữ và công thức trắng hoặc xám;
chữ trên màn hình dùng IN HOA;
Text dùng cho tiếng Việt;
MathTex dùng cho công thức;
không đưa tiếng Việt có dấu vào MathTex;
không dùng nhiều màu nếu không cần;
không chồng quá nhiều chữ trên màn hình;
chuyển động phải phục vụ mạch hiểu.
```

### 2.7. Công đoạn 7 — thu voice-over

Chỉ thu voice-over sau khi kịch bản nói đã chốt. Có thể thu theo từng cảnh hoặc từng cụm cảnh. Khi thu, ưu tiên rõ, chậm vừa đủ, có khoảng dừng ở chỗ người xem cần nhìn công thức.

### 2.8. Công đoạn 8 — dựng hậu kì

Dựng hậu kì dùng để căn hình với lời đọc, điều chỉnh nhịp, thêm nhạc nền nếu cần, xuất preview và final. Không dùng hậu kì để che lỗi lập luận hoặc lỗi bố cục gốc.

### 2.9. Công đoạn 9 — kiểm duyệt và xuất bản

Trước khi xuất final, phải kiểm duyệt theo bốn lớp:

```text
nội dung toán học;
mạch nhận thức;
nghe–nhìn;
file final.
```

Không xuất bản nếu video đúng công thức nhưng người xem không thấy vì sao đi từ bước này sang bước sau.

---

## 3. Chọn phạm vi và chốt vấn đề trung tâm

### 3.1. Chọn phạm vi

Một phạm vi tốt phải thỏa ba điều kiện:

```text
đủ hẹp để video không lan man;
đủ rộng để người xem không thiếu nền;
đủ trọn để tạo thành một bước hiểu độc lập.
```

Không chọn phạm vi theo độ dài văn bản. Chọn phạm vi theo mạch hiểu.

### 3.2. Chốt vấn đề trung tâm

Vấn đề trung tâm nên viết thành một câu hỏi rõ. Câu hỏi này phải xuất hiện được trong phần mở đầu hoặc được gợi ra rất sớm.

Câu hỏi tốt thường có dạng:

```text
Có nên tin ngay không?
Vì sao cách nghĩ quen thuộc chưa đủ?
Con số này thật sự nói về điều gì?
Cần đổi câu hỏi như thế nào để hiểu đúng tình huống?
```

### 3.3. Kiểm tra ý mới trước khi đưa vào video

Khi xuất hiện một suy nghĩ mới, không đưa ngay vào kịch bản. Trước hết kiểm tra:

```text
Ý mới có giải thích đúng điều video cần giải thích không?
Ý mới làm mạch rõ hơn hay chỉ làm dày thêm?
Ý mới nên nằm ở cảnh nào?
Ý mới có làm cảnh quan trọng bị yếu đi không?
Ý mới có khiến một cảnh nói sớm nhiệm vụ của cảnh sau không?
Ý mới có buộc ta đổi lại kịch bản nói không?
```

Nếu ý mới chỉ thú vị nhưng không giúp người xem đi đúng mạch, không đưa vào video.

### 3.4. Kiểm tra mạch của từng cảnh

Mỗi cảnh cần có nhiệm vụ riêng. Có thể dùng bảng sau:

```text
Cảnh 1: mở tình huống.
Cảnh 2: chặn phản ứng vội.
Cảnh 3: dựng bối cảnh.
Cảnh 4: xét nhóm thứ nhất.
Cảnh 5: xét nhóm thứ hai.
Cảnh 6: gom kết quả.
Cảnh 7: đổi câu hỏi hoặc chốt nhận thức chính.
Cảnh 8: giải thích hệ quả.
Cảnh 9: kết luận và nhắc cách dùng kết quả.
```

Bảng này không phải khuôn cố định. Nó chỉ cho thấy mỗi cảnh cần có nhiệm vụ rõ.

---

## 4. Viết kịch bản nói

### 4.1. Vai trò

Kịch bản nói là phần quan trọng nhất của video. Người xem đi theo lời nói trước, rồi dùng hình ảnh để nhìn rõ hơn điều đang nghe.

Một kịch bản nói tốt phải:

```text
nghe tự nhiên;
lập luận liền mạch;
không nhảy cóc;
không thừa thuật ngữ;
không nói dài khi một câu ngắn đã đủ;
cho người xem đủ thời gian nhìn và hiểu.
```

### 4.2. Câu trong kịch bản nói

Mỗi câu nên làm một việc:

```text
nêu tình huống;
đặt câu hỏi;
giới thiệu dữ kiện;
giải thích một con số;
chuyển điểm nhìn;
rút kết luận nhỏ;
chốt kết luận chính.
```

Không nên để một câu vừa đưa dữ kiện, vừa giải thích, vừa kết luận.

### 4.3. Dùng từ ít và nhất quán

Khi một video đã chọn bộ từ, phải giữ bộ từ đó đến cuối. Không thay từ chỉ để câu nghe mới hơn.

Ví dụ với video về công cụ phát hiện văn bản AI, bộ từ nên giữ là:

```text
công cụ báo;
bị báo là AI;
phát hiện đúng;
báo nhầm;
bài thật sự do AI viết;
bài do học sinh tự viết.
```

Không trộn thêm các cách nói khác như:

```text
bắt bài;
nhận diện;
gán nhãn;
bị báo cáo;
nhận nhầm;
dương tính giả;
âm tính giả;
```

trừ khi video thật sự cần thuật ngữ chuyên môn.

### 4.4. Khi dùng số liệu và tỉ lệ

Với mọi tỉ lệ, phải nói rõ tỉ lệ đó được tính trên nhóm nào.

Cách kiểm tra:

```text
95% của nhóm nào?
2% của nhóm nào?
38 trên 57 là 38 trong nhóm nào?
19 trên 57 là 19 trong nhóm nào?
```

Không để một con số đẹp thay thế cho việc đọc đúng bối cảnh tạo ra con số đó.

Cách nói nên dùng:

```text
95% chỉ nói về nhóm bài thật sự do AI viết.
2% chỉ nói về nhóm bài do học sinh tự viết.
38 trên 57 nói về nhóm bài bị báo là AI.
19 trên 57 cũng nói về chính nhóm bài bị báo là AI.
```

### 4.5. Không nói sớm, không lặp

Nếu Cảnh 7 là nơi đổi câu hỏi, Cảnh 2 không nên nói trước đầy đủ câu hỏi của Cảnh 7. Nếu Cảnh 8 là nơi giải thích vì sao tỉ lệ nhỏ vẫn gây nhiều kết quả sai, Cảnh 5 không nên nói trước kết luận đó.

Cách kiểm tra:

```text
Cảnh này đang làm việc của chính nó hay làm hộ cảnh sau?
Ý này đã được nói đủ ở cảnh trước chưa?
Nếu bỏ câu này, mạch có mất không?
Nếu giữ câu này, cảnh sau có yếu đi không?
```

### 4.6. Đọc công thức bằng lời

Công thức trên màn hình không cần được đọc như văn bản kí hiệu. Lời đọc phải giúp người nghe hiểu ý của công thức.

Ví dụ:

```text
38 trên 57, xấp xỉ 2 phần 3.
```

thường tốt hơn:

```text
ba mươi tám chia năm mươi bảy xấp xỉ hai phần ba.
```

### 4.7. Checklist kịch bản nói

```text
[ ] Mở đầu nêu được tình huống hoặc câu hỏi.
[ ] Vấn đề trung tâm xuất hiện sớm.
[ ] Mỗi cảnh có một nhiệm vụ rõ.
[ ] Câu ngắn, đọc tự nhiên.
[ ] Không có thuật ngữ thừa.
[ ] Từ khóa được dùng nhất quán.
[ ] Các con số đều có nhóm nền rõ.
[ ] Không nói sớm ý của cảnh sau.
[ ] Không lặp ý đã đủ rõ.
[ ] Kết luận trả lời đúng câu hỏi mở đầu.
```

---

## 5. Thiết kế kịch bản video

### 5.1. Cấu trúc một cảnh

Mỗi cảnh trong kịch bản video nên có dạng:

````markdown
### Cảnh n. Tên cảnh

**Lời đọc**

```text
...
```

**Màn hình**

```text
...
```

**Chuyển động**

```text
...
```

**Ghi chú nhịp**

```text
...
```
````

### 5.2. Khớp với kịch bản nói

Kịch bản video phải dùng cùng hệ cảnh với kịch bản nói. Nếu kịch bản nói có 9 cảnh, kịch bản video cũng nên có 9 cảnh, trừ khi có lí do rõ để tách một cảnh nói thành nhiều cảnh hình.

Không để xảy ra tình trạng:

```text
kịch bản nói cảnh 7 nói ý A;
kịch bản video cảnh 7 lại hiện ý B;
Manim cảnh 7 lại chạy ý C.
```

### 5.3. Màn hình không phải phụ đề

Chữ trên màn hình chỉ là điểm tựa thị giác. Nó không cần chép đủ lời đọc.

Màn hình nên ưu tiên:

```text
từ khóa;
con số chính;
công thức chính;
quan hệ giữa các nhóm;
câu hỏi trung tâm;
kết luận cần nhớ.
```

Không nên đưa quá nhiều câu dài lên màn hình.

### 5.4. Chuyển động

Chuyển động phải cho người xem thấy ý đang được hình thành. Một chuyển động tốt có thể:

```text
đưa đối tượng vào đúng lúc lời đọc nhắc tới;
gom các nhóm lại;
đổi điểm nhìn;
làm nổi bật mẫu số;
cho thấy phần đúng và phần sai;
đưa kết luận lên sau khi dữ kiện đã đủ.
```

Không dùng chuyển động chỉ để trang trí.

### 5.5. Khoảng dừng

Khoảng dừng là một phần của kịch bản. Sau công thức, sau câu hỏi quan trọng, hoặc sau kết luận chính, cần có khoảng dừng để người xem kịp nhìn.

Trong kịch bản video, ghi rõ:

```text
dừng ngắn sau khi hiện câu hỏi;
dừng vừa sau khi hiện công thức;
dừng lâu hơn sau kết luận chính.
```

### 5.6. Checklist kịch bản video

```text
[ ] Mỗi cảnh có lời đọc, màn hình, chuyển động, ghi chú nhịp.
[ ] Màn hình chỉ chứa điểm tựa cần thiết.
[ ] Chữ trên màn hình không thay thế lời đọc.
[ ] Công thức hiện đúng lúc.
[ ] Chuyển động phục vụ mạch hiểu.
[ ] Không có cảnh nào nói sớm nhiệm vụ của cảnh sau.
[ ] Không có cảnh nào lặp lại mà không thêm chức năng.
[ ] Kịch bản video khớp với kịch bản nói.
```

---

## 6. Sản xuất video bằng Manim

### 6.1. Vai trò của Manim

Manim dùng để dựng bảng toán học động. Trong video ZO Math, Manim cần rõ, sạch, có nhịp và ít nhiễu.

Manim không cần phô diễn kĩ thuật. Một cảnh Manim tốt là cảnh giúp người xem hiểu điều lời đọc đang nói.

### 6.2. Chuẩn hình ảnh

Chuẩn tạm chốt:

```text
nền đen;
chữ trắng hoặc xám;
font không chân;
font chính: Arial;
ít màu;
không trang trí thừa;
không chồng quá nhiều lớp chữ;
không để cảnh trước lẫn vào cảnh sau.
```

### 6.3. Chuẩn chữ trên màn hình

Văn bản xuất hiện trên video thống nhất dùng chữ IN HOA. Phân cấp thị giác bằng:

```text
cỡ chữ;
độ đậm;
sắc độ trắng/xám;
khoảng cách;
vị trí;
thời điểm xuất hiện.
```

Không trộn chữ thường và chữ hoa để phân cấp.

### 6.4. Dấu câu trên màn hình

Chữ trên màn hình Manim không cần đầy đủ dấu câu như văn bản viết. Quy ước:

```text
không dùng dấu chấm cuối dòng;
hạn chế dấu phẩy;
hạn chế dấu hai chấm;
giữ dấu hỏi khi thật sự là câu hỏi;
dùng xuống dòng để tạo nhịp;
dùng khoảng trống để chia ý.
```

Ví dụ nên dùng:

```text
KẾT QUẢ ẤY ĐÁNG TIN ĐẾN ĐÂU?

VÀ NÓ CÓ THỂ KHIẾN TA
KẾT LUẬN SAI ĐẾN MỨC NÀO?
```

Không cần viết:

```text
KẾT QUẢ ẤY ĐÁNG TIN ĐẾN ĐÂU?

VÀ NÓ CÓ THỂ KHIẾN TA
KẾT LUẬN SAI ĐẾN MỨC NÀO?
.
```

### 6.5. Text và MathTex

Quy tắc:

```text
Text(...): dùng cho tiếng Việt.
MathTex(...): dùng cho công thức toán học.
Không đưa tiếng Việt có dấu vào MathTex.
Không ép mọi thứ thành công thức nếu đó là lời nói.
```

Ví dụ:

```python
label = Text("BÀI BỊ BÁO LÀ AI", font="Arial")
ratio = MathTex(r"\frac{38}{57} \approx \frac{2}{3}")
```

### 6.6. Bố cục

Màn hình nên có một điểm nhìn chính. Không rải nhiều chữ ở bốn góc nếu người xem không biết nhìn đâu trước.

Các bố cục thường dùng:

```text
chữ chính ở giữa;
nhóm dữ kiện bên trái và bên phải;
công thức ở giữa, ghi chú phía dưới;
kết luận cuối cảnh ở giữa;
nhóm đúng và nhóm nhầm đặt cạnh nhau để so sánh.
```

### 6.7. Chuyển cảnh

Trước khi vào cảnh mới, nên xóa rõ các đối tượng cũ nếu chúng không còn phục vụ cảnh mới. Tránh để chữ hoặc công thức cũ còn sót lại gây nhiễu.

### 6.8. Nhịp chờ

Không nên để mọi thứ chạy liên tục. Sau mỗi điểm chính, cần `self.wait(...)`.

Gợi ý:

```text
0.4–0.8 giây: chờ rất ngắn sau chuyển động phụ;
1.0–1.5 giây: chờ sau một dòng chữ ngắn;
1.5–2.5 giây: chờ sau công thức hoặc con số quan trọng;
2.5 giây trở lên: chờ sau kết luận chính.
```

### 6.9. Quy trình render Manim

Luôn đứng ở thư mục gốc của xưởng video:

```powershell
PS E:\zo_media\zo_video>
```

Không `cd` vào thư mục `manim`. Gọi file Manim bằng đường dẫn:

```powershell
.\manim\ten_video.py
```

Kiểm tra cú pháp:

```powershell
uv run python -m py_compile .\manim\ten_video.py
```

Khi đang dựng từng cảnh hoặc ghép thử vài cảnh, chỉ mở các cảnh cần kiểm tra trong `construct()` và render nháp bằng lệnh:

```powershell
uv run manim -pql --disable_caching .\manim\ten_video.py TenClass
```

Khi đã chốt hình, nhịp và âm thanh, render bản chất lượng cao:

```powershell
uv run manim -pqh --disable_caching .\manim\ten_video.py TenClass
```

Nếu gặp hiện tượng lạ như render nhầm bản cũ, lúc có âm thanh lúc mất âm thanh, hoặc video mở ra không đúng bản mới, xóa thư mục render cũ của video đó rồi render lại:

```powershell
Remove-Item -Recurse -Force .\media\videos\ten_video
uv run manim -pql --disable_caching .\manim\ten_video.py TenClass
```

Quy tắc chốt:

```text
Đang sản xuất: dùng -pql --disable_caching.
Xuất bản cuối: dùng -pqh --disable_caching.
Luôn chạy lệnh từ E:\zo_media\zo_video.
Không bỏ .\manim\ nếu file nằm trong thư mục manim.
```

### 6.10. Chuẩn hóa tệp âm thanh cho Manim

Hiệu ứng âm thanh dùng trong Manim nên được chuẩn hóa về `.wav` trước khi render.

Đặt các tệp âm thanh dùng chung trong:

```text
assets/sounds/
```

Nếu tệp gốc là `.mp3`, chuyển sang `.wav` bằng FFmpeg:

```powershell
ffmpeg -y -i ten_file.mp3 -ar 48000 -ac 1 -c:a pcm_s16le ten_file.wav
```

Nếu tệp gốc là `.m4a`, chuyển sang `.wav` bằng FFmpeg:

```powershell
ffmpeg -y -i ten_file.m4a -ar 48000 -ac 1 -c:a pcm_s16le ten_file.wav
```

Quy tắc chốt:

```text
SFX ngắn cho Manim: dùng WAV PCM 16-bit, 48 kHz, mono.
Tệp tải về từ Pixabay hoặc nguồn khác: đổi tên ngắn, không dấu, không khoảng trắng.
Sau khi chuyển xong, trỏ đường dẫn trong Manim tới tệp .wav, không dùng lẫn nhiều định dạng.
```

Ví dụ:

```python
SFX = {
    "tick": "assets/sounds/computer_mouse_click.wav",
    "hit": "assets/sounds/menu_beep_accept_soft.wav",
    "whoosh": "assets/sounds/simple_whoosh.wav",
}
```

### 6.11. Checklist Manim

```text
[ ] Code chạy không lỗi cú pháp.
[ ] Cảnh khớp với kịch bản video.
[ ] Chữ trên màn hình dùng IN HOA.
[ ] Dấu câu được tối giản.
[ ] Text dùng cho tiếng Việt.
[ ] MathTex dùng cho công thức.
[ ] Font chính là Arial.
[ ] Không có chữ quá dài tràn màn hình.
[ ] Không có cảnh quá nhiều đối tượng.
[ ] Chuyển động có mục đích.
[ ] Có khoảng dừng sau ý quan trọng.
[ ] Tệp hiệu ứng âm thanh nếu dùng đã được chuẩn hóa về .wav.
[ ] Preview đã được xem lại từ đầu đến cuối.
```

---

## 7. Thu voice-over

### 7.1. Thời điểm thu

Chỉ thu sau khi kịch bản nói đã chốt. Nếu kịch bản nói còn đang sửa mạch lập luận, chưa nên thu.

### 7.2. Giọng đọc

Giọng đọc cần rõ, bình tĩnh, có nhịp, không diễn quá mức. Video toán học cần sự tin cậy và sáng rõ hơn là kịch tính.

### 7.3. Khoảng dừng

Khoảng dừng nên xuất hiện ở:

```text
sau câu hỏi mở đầu;
sau khi nêu dữ kiện lớn;
sau công thức;
sau khi đổi điểm nhìn;
sau kết luận chính.
```

### 7.4. Thu theo đoạn

Nên thu theo cảnh hoặc theo cụm cảnh. Không nhất thiết thu toàn bộ một lần. Nếu một câu đọc hỏng, thu lại đoạn đó, không cần thu lại toàn bộ video.

### 7.5. Chuẩn file âm thanh

Tên file đề nghị:

```text
audio/ten_video_voice_v01.wav
audio/ten_video_voice_v02.wav
audio/ten_video_voice_final.wav
```

### 7.6. Checklist voice-over

```text
[ ] Kịch bản nói đã chốt.
[ ] Giọng đọc rõ.
[ ] Không đọc quá nhanh.
[ ] Có khoảng dừng sau công thức và câu hỏi.
[ ] Không nuốt chữ ở thuật ngữ chính.
[ ] File âm thanh đặt tên đúng.
[ ] Nếu sửa kịch bản nói, đã đánh dấu đoạn cần thu lại.
```

---

## 8. Dựng hậu kì bằng DaVinci Resolve

### 8.1. Vai trò

DaVinci Resolve dùng để ghép video Manim, voice-over, nhạc nền nếu có, logo, intro/outro nếu cần, rồi xuất preview và final.

### 8.2. Căn hình theo lời đọc

Khi dựng, ưu tiên lời đọc. Hình nên xuất hiện đúng lúc lời đọc cần người xem nhìn vào.

Không để:

```text
lời đọc đã sang ý mới nhưng hình còn ở ý cũ;
hình hiện công thức trước khi lời đọc chuẩn bị cho nó;
chuyển cảnh quá nhanh khiến người xem chưa kịp nhìn;
một khoảng trống quá dài không có chức năng.
```

### 8.3. Nhạc nền

Nếu dùng nhạc nền, phải nhỏ và không cạnh tranh với giọng đọc. Nếu nhạc làm giảm độ rõ của toán học, bỏ nhạc.

### 8.4. Phụ đề

Không mặc định cần phụ đề đầy đủ. Nếu có phụ đề, phụ đề không được làm rối màn hình hoặc lặp lại toàn bộ chữ đã có trong Manim.

### 8.5. Xuất file

Preview:

```text
exports/preview/ten_video_preview_v01.mp4
```

Final:

```text
exports/final/ten_video_final.mp4
```

Nếu sửa final:

```text
exports/final/ten_video_final_v02.mp4
```

### 8.6. Checklist dựng

```text
[ ] Voice-over và hình khớp nhau.
[ ] Không có đoạn hình chạy quá nhanh.
[ ] Không có đoạn im lặng thừa.
[ ] Nhạc nền nếu có không che giọng đọc.
[ ] Chữ trên màn hình đọc được.
[ ] Công thức không bị cắt.
[ ] Preview đã xem lại sau khi xuất.
[ ] Final đã xem lại sau khi xuất.
```

---

## 9. Kiểm duyệt trước khi xuất bản

### 9.1. Kiểm duyệt nội dung

```text
[ ] Không sai toán học.
[ ] Không sai số liệu.
[ ] Không dùng thuật ngữ lệch nghĩa.
[ ] Công thức khớp với lời đọc.
[ ] Kết luận không vượt quá dữ kiện.
```

### 9.2. Kiểm duyệt mạch nhận thức

```text
[ ] Người xem biết video đang trả lời câu hỏi nào.
[ ] Các cảnh đi theo thứ tự hợp lí.
[ ] Không có bước nhảy cóc.
[ ] Không có nhánh phụ làm loãng mạch.
[ ] Cảnh quan trọng nhất đủ rõ.
[ ] Kết luận trả lời đúng mở đầu.
```

### 9.3. Kiểm duyệt nghe–nhìn

```text
[ ] Chữ đủ lớn.
[ ] Công thức đủ rõ.
[ ] Không có màn hình quá dày.
[ ] Chuyển động không gây rối.
[ ] Giọng đọc rõ.
[ ] Nhịp không quá nhanh.
[ ] Khoảng dừng hợp lí.
```

### 9.4. Kiểm duyệt final

```text
[ ] File final mở được.
[ ] Âm thanh không lỗi.
[ ] Hình ảnh không giật bất thường.
[ ] Không có cảnh đen ngoài ý muốn.
[ ] Không có chữ sai chính tả.
[ ] Tên file đúng chuẩn.
[ ] Hồ sơ sản xuất đã cập nhật trạng thái final.
```

---

## 10. Lưu trữ, đặt tên file và phiên bản hóa

### 10.1. Thư mục gốc

Xưởng video ZO Math:

```text
E:\zo_media\zo_video
```

Cấu trúc:

```text
E:\zo_media\zo_video
│
├─ scripts
├─ manim
├─ audio
├─ resolve
├─ exports
│  ├─ preview
│  └─ final
└─ assets
   ├─ logo
   ├─ music
   ├─ sounds
   └─ fonts
```

Vai trò:

```text
scripts: hồ sơ sản xuất, kịch bản nói, kịch bản video;
manim: code Manim;
audio: voice-over;
resolve: project hoặc ghi chú dựng;
exports/preview: bản xem thử;
exports/final: bản hoàn chỉnh;
assets: tài nguyên dùng chung, gồm logo, nhạc, hiệu ứng âm thanh và font.
```

### 10.2. Mã video

Quy tắc:

```text
viết thường;
không dấu;
dùng gạch dưới;
ngắn nhưng nhận ra nội dung;
không khoảng trắng;
không kí tự đặc biệt.
```

Ví dụ:

```text
cong_cu_phat_hien_van_ban_ai_co_dang_tin
xac_suat_co_dieu_kien
bai_toan_hai_con
y_nghia_cua_gioi_han
```

### 10.3. Tên file chuẩn

Với mã video `ten_video`:

```text
scripts/ten_video_ho_so_v01.md
manim/ten_video_v01.py
audio/ten_video_voice_v01.wav
resolve/ten_video.drp
exports/preview/ten_video_preview_v01.mp4
exports/final/ten_video_final.mp4
```

Không dùng:

```text
final.mp4
final2.mp4
final_final.mp4
ban_moi.mp4
ok.py
video.py
```

### 10.4. Phiên bản hóa

```text
v01: bản đầu tiên;
v02: bản chỉnh tiếp;
v03: bản chỉnh tiếp;
final: bản đã chốt để xuất bản.
```

Nếu đã có final nhưng cần sửa:

```text
ten_video_final_v02.mp4
```

và phải ghi lí do sửa trong nhật kí sản xuất.

---

## 11. Mẫu hồ sơ sản xuất

````markdown
# Hồ sơ sản xuất video: ten_video

**Phiên bản hồ sơ:** v01  
**Trạng thái:** đang phát triển / đã chốt kịch bản nói / đã chốt kịch bản video / đang làm Manim / preview / final  
**Ngày bắt đầu:**  
**Ngày cập nhật gần nhất:**

---

## 1. Thông tin chung

- Mã video:
- Tên video:
- Nguồn nội dung:
- Phạm vi chuyển hóa:
- Độ dài dự kiến:
- Công cụ chính:

---

## 2. Vấn đề trung tâm

Video này giúp người xem hiểu rõ điều gì?

```text

```

---

## 3. Phạm vi chuyển hóa

Video này chuyển hóa toàn bộ nguồn nội dung hay chỉ một phần?

```text

```

Vì sao phạm vi này tạo thành một mạch hiểu độc lập?

```text

```

---

## 4. Mạch bài giảng

```text
Cảnh 1:
Cảnh 2:
Cảnh 3:
Cảnh 4:
Cảnh 5:
...
```

---

## 5. Kịch bản nói

```text
[Cảnh 1]

...

[Cảnh 2]

...
```

---

## 6. Kịch bản video

### Cảnh 1. Tên cảnh

**Lời đọc**

```text

```

**Màn hình**

```text

```

**Chuyển động**

```text

```

**Ghi chú nhịp**

```text

```

---

## 7. File sản xuất

```text
Hồ sơ:
scripts/ten_video_ho_so_v01.md

Manim:
manim/ten_video_v01.py

Voice-over:
audio/ten_video_voice_v01.wav

Preview:
exports/preview/ten_video_preview_v01.mp4

Final:
exports/final/ten_video_final.mp4
```

---

## 8. Nhật kí sản xuất

```text
v01:
v02:
v03:
final:
```

---

## 9. Checklist trước khi xuất bản

```text
[ ] Vấn đề trung tâm rõ.
[ ] Mạch bài giảng liền.
[ ] Kịch bản nói đã chốt.
[ ] Kịch bản video khớp kịch bản nói.
[ ] Manim khớp kịch bản video.
[ ] Voice-over rõ.
[ ] Hình và lời khớp nhau.
[ ] Final đã xem lại từ đầu đến cuối.
```
````

---

## 12. Mẫu file Manim

```python
from manim import *

# =========================
# ZO Math visual constants
# =========================

BACKGROUND = "#050507"

WHITE_MAIN = "#F5F5F5"
WHITE_SOFT = "#D8D8D8"

GRAY_MAIN = "#9A9A9A"
GRAY_SOFT = "#5F5F5F"
GRAY_FAINT = "#303030"

FONT = "Arial"


class TenVideo(Scene):
    def setup(self):
        self.camera.background_color = BACKGROUND

    def clear_screen(self, *objects, run_time=0.8):
        self.play(
            *[FadeOut(obj) for obj in objects],
            run_time=run_time,
        )

    def make_text(self, text, font_size=32, color=WHITE_MAIN, line_spacing=0.9):
        return Text(
            text.upper(),
            font=FONT,
            font_size=font_size,
            color=color,
            line_spacing=line_spacing,
        )

    def make_title(self, text):
        return self.make_text(
            text,
            font_size=36,
            color=WHITE_MAIN,
        )

    def make_note(self, text):
        return self.make_text(
            text,
            font_size=28,
            color=WHITE_SOFT,
            line_spacing=0.9,
        )

    def construct(self):
        # Cảnh 1: Mở vấn đề
        title = self.make_title("TIÊU ĐỀ VIDEO")
        self.play(Write(title), run_time=1.4)
        self.wait(1.2)
        self.clear_screen(title)

        # Cảnh 2: Công thức hoặc dữ kiện chính
        equation = MathTex(
            r"x + 3 = 7",
            font_size=84,
            color=WHITE_MAIN,
        )
        self.play(Write(equation), run_time=1.4)
        self.wait(1.4)
        self.clear_screen(equation)

        # Cảnh 3: Chốt nhận thức
        conclusion = self.make_note(
            "CÂU CHỐT NHẬN THỨC\nCỦA VIDEO"
        )
        self.play(FadeIn(conclusion, shift=UP * 0.2), run_time=1.2)
        self.wait(2.4)
        self.clear_screen(conclusion)
```

---

## 13. Lỗi thường gặp và cách xử lí

### 13.1. Sửa Manim khi kịch bản nói chưa chốt

Dấu hiệu:

```text
càng sửa code càng thấy mạch không liền;
phải thêm nhiều chữ để giải thích;
Cảnh này nói lặp cảnh kia;
Manim có hình nhưng không rõ người xem cần hiểu gì.
```

Cách xử lí:

```text
Dừng sửa Manim.
Quay lại kịch bản nói.
Chốt lại mạch nhận thức.
Sau đó mới đồng bộ kịch bản video và code.
```

### 13.2. Một cảnh nói quá nhiều việc

Dấu hiệu:

```text
cảnh có quá nhiều chữ;
lời đọc chuyển qua nhiều ý;
người xem không biết trọng tâm là gì.
```

Cách xử lí:

```text
Xác định nhiệm vụ chính của cảnh.
Bỏ hoặc chuyển ý không thuộc nhiệm vụ đó sang cảnh khác.
```

### 13.3. Nói sớm ý của cảnh sau

Dấu hiệu:

```text
cảnh sau mất lực;
người xem đã nghe kết luận trước khi thấy dữ kiện;
video bị lặp.
```

Cách xử lí:

```text
Giữ cảnh trước ở mức mở đường.
Để cảnh sau thực hiện đúng nhiệm vụ của nó.
```

### 13.4. Từ ngữ không thống nhất

Dấu hiệu:

```text
cùng một đối tượng nhưng lúc gọi thế này, lúc gọi thế khác;
người xem phải học thêm từ mới không cần thiết;
kịch bản nghe như đang phô từ.
```

Cách xử lí:

```text
Chọn một bộ từ nhỏ.
Thay toàn bộ kịch bản theo bộ từ đó.
Không dùng từ đồng nghĩa nếu không thêm chức năng.
```

### 13.5. Màn hình quá nhiều chữ

Dấu hiệu:

```text
người xem đọc không kịp;
chữ giống phụ đề;
công thức bị chìm;
không biết nhìn đâu.
```

Cách xử lí:

```text
Giữ từ khóa, số liệu và công thức chính.
Đưa phần giải thích về lời đọc.
Chia cảnh nếu thật sự cần.
```

### 13.6. Con số không rõ nhóm nền

Dấu hiệu:

```text
người xem thấy 95% nhưng không biết 95% của nhóm nào;
người xem nhầm tỉ lệ phát hiện đúng với độ tin của kết quả bị báo;
con số đẹp làm che mất bối cảnh.
```

Cách xử lí:

```text
Nói rõ nhóm mà tỉ lệ được tính trên.
Nói rõ khi nào cần đổi mẫu số.
Dùng hình ảnh để gom nhóm và tách nhóm.
```

---

## 14. Checklist sản xuất

### 14.1. Trước khi viết kịch bản

```text
[ ] Đã có nguồn nội dung.
[ ] Đã chọn phạm vi video.
[ ] Đã chốt vấn đề trung tâm.
[ ] Đã rút mạch bài giảng.
[ ] Đã biết video cần bao nhiêu cảnh chính.
```

### 14.2. Trước khi làm kịch bản video

```text
[ ] Kịch bản nói đã đọc tự nhiên.
[ ] Mạch lập luận không nhảy cóc.
[ ] Từ khóa đã thống nhất.
[ ] Không còn ý mới đang chờ xét.
[ ] Kết luận đã trả lời câu hỏi mở đầu.
```

### 14.3. Trước khi viết Manim

```text
[ ] Kịch bản video đã có màn hình từng cảnh.
[ ] Mỗi cảnh có nhiệm vụ rõ.
[ ] Chữ trên màn hình đã tối giản.
[ ] Công thức cần hiện đã xác định.
[ ] Chuyển động chính đã mô tả.
```

### 14.4. Trước khi thu voice-over

```text
[ ] Kịch bản nói đã chốt.
[ ] Không còn sửa câu lớn.
[ ] Đã đánh dấu khoảng dừng.
[ ] Đã đọc thử toàn bộ một lượt.
```

### 14.5. Trước khi xuất final

```text
[ ] Preview đã xem lại từ đầu đến cuối.
[ ] Nội dung đúng.
[ ] Hình và lời khớp.
[ ] Âm thanh rõ.
[ ] Không có lỗi chữ.
[ ] Không có cảnh thừa.
[ ] File final đặt tên đúng.
[ ] Hồ sơ đã cập nhật trạng thái.
```

---

## 15. Prompt làm việc với ChatGPT

### 15.1. Xác định phạm vi video

```text
Tôi có bài luận dưới đây và muốn chuyển thành video ZO Math.

Bạn hãy giúp tôi xác định phạm vi video.

Yêu cầu:
- Chọn một phạm vi tốt nhất.
- Cho biết video nên bao quát toàn bài hay chỉ một phần.
- Chốt vấn đề trung tâm của video.
- Giải thích vì sao phạm vi này tạo thành một mạch hiểu độc lập.
- Không viết kịch bản nói.
- Không thiết kế Manim.
```

### 15.2. Rút mạch bài giảng

```text
Tôi đã chọn phạm vi dưới đây cho một video ZO Math.

Bạn hãy rút thành mạch bài giảng.

Yêu cầu:
- Chỉ tập trung vào đường đi nhận thức của người xem.
- Không viết kịch bản nói hoàn chỉnh.
- Không thiết kế cảnh video.
- Mỗi bước phải cho thấy vì sao ta đi tiếp.
- Ưu tiên một mạch tốt nhất, không đưa nhiều phương án.
```

### 15.3. Viết kịch bản nói

```text
Dưới đây là mạch bài giảng đã chốt.

Bạn hãy viết kịch bản nói cho voice-over.

Yêu cầu:
- Viết cho tai nghe.
- Câu ngắn, rõ, tự nhiên.
- Mỗi cảnh có nhiệm vụ riêng.
- Dùng ít từ khóa và dùng nhất quán.
- Không thêm ý mới ngoài mạch đã chốt.
- Không phô trương thuật ngữ.
- Chỉ trả về kịch bản nói.
```

### 15.4. Kiểm tra kịch bản nói

```text
Dưới đây là kịch bản nói hiện tại.

Bạn hãy kiểm tra:
- Mở đề có rõ không?
- Lập luận có liền mạch không?
- Cảnh nào nói sớm hoặc lặp ý?
- Từ ngữ có thống nhất không?
- Kết luận có trả lời đúng câu hỏi mở đầu không?

Yêu cầu:
- Chỉ nêu những điểm thật sự cần sửa.
- Nếu đã ổn, nói rõ là giữ.
- Không thay từ gần nghĩa chỉ để tạo cảm giác có chỉnh sửa.
```

### 15.5. Thiết kế kịch bản video

```text
Dưới đây là kịch bản nói đã chốt.

Bạn hãy chuyển thành kịch bản video.

Mỗi cảnh gồm:
1. Lời đọc
2. Màn hình
3. Chuyển động
4. Ghi chú nhịp

Yêu cầu:
- Màn hình không phải phụ đề đầy đủ.
- Chữ trên màn hình dùng IN HOA.
- Dấu câu trên màn hình tối giản, giữ dấu hỏi khi cần.
- Chuyển động phục vụ mạch hiểu.
- Không thêm ý mới ngoài kịch bản nói.
```

### 15.6. Chỉnh Manim theo hồ sơ

```text
Dưới đây là hồ sơ sản xuất đã chốt và file Manim hiện tại.

Bạn hãy chỉnh file Manim để khớp với hồ sơ.

Yêu cầu:
- Giữ đúng hệ cảnh trong kịch bản video.
- Đồng bộ chữ trên màn hình với màn hình đã chốt.
- Dùng chữ IN HOA.
- Tối giản dấu câu.
- Không thêm ý mới.
- Kiểm tra cú pháp Python sau khi chỉnh.
```

### 15.7. Cập nhật sổ tay sau một video thật

```text
Tôi vừa hoàn thành một video ZO Math.

Dưới đây là hồ sơ, kịch bản nói, kịch bản video, file Manim và các ghi chú trong quá trình làm.

Bạn hãy cập nhật sổ tay sản xuất video.

Yêu cầu:
- Chỉ giữ kinh nghiệm có thể dùng lại cho nhiều video.
- Không biến sổ tay thành nhật kí của riêng video này.
- Biến kinh nghiệm thành quy tắc thao tác cụ thể.
- Đặt nội dung vào đúng mục sản xuất.
- Bỏ phần suy tư không trực tiếp phục vụ sản xuất.
```

---

## 16. Cập nhật sổ tay sau mỗi video

Sổ tay chỉ nên cập nhật bằng kinh nghiệm sản xuất thật. Không cập nhật theo cảm hứng.

Sau mỗi video, ghi lại:

```text
1. Điều gì trong quy trình hoạt động tốt?
2. Lỗi nào gây mất thời gian?
3. Lỗi đó thuộc công đoạn nào?
4. Sửa ở cấp nào là đúng: kịch bản nói, kịch bản video, Manim, voice-over hay dựng?
5. Kinh nghiệm này có dùng lại được cho nhiều video không?
6. Nếu có, nên cập nhật vào mục nào của sổ tay?
```

Chỉ đưa vào sổ tay những kinh nghiệm có tính lặp lại. Không đưa chi tiết riêng của một video nếu nó không giúp sản xuất video sau tốt hơn.

---

## Kết luận vận hành

Một video ZO Math tốt được tạo ra bằng quy trình rõ ràng, không bằng việc sửa ngẫu hứng từng file. Khi có vấn đề, phải xác định đúng cấp cần sửa:

```text
mạch chưa rõ → sửa kịch bản nói;
hình chưa đúng ý → sửa kịch bản video;
chữ hoặc chuyển động chưa ổn → sửa Manim;
hình và lời lệch → sửa dựng;
giọng chưa rõ → thu lại voice-over.
```

Không để công đoạn sau che lỗi của công đoạn trước. Chốt mạch trước, làm hình sau, dựng cuối cùng.
