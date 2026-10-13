# P2.2 — Stress Test và Owner Calibration Readiness

**Dự án:** ZO Math — Hệ thiết kế và ngôn ngữ thương hiệu  
**Pha:** P2 — Visual Foundation / Visual Exploration  
**Trạng thái:** stress-test synthesis  
**Ngày:** 2026-10-05

## 1. Mục tiêu

P2.2 kiểm ba Visual Directions v0.1 trên bốn tình huống có tải thiết kế cao hơn:

1. bài học dày;
2. graph khó;
3. mobile;
4. grayscale / print.

P2.2 không chọn winner cuối cùng.

Mục tiêu là xác định:
- direction nào chịu tải tốt;
- direction nào lộ anti-pattern;
- phần nào nên giữ;
- phần nào nên loại hoặc lai ghép;
- khi nào ý kiến chủ dự án trở thành input quyết định.

---

# 2. Stress Test A — Ấm và trong sáng

## 2.1. Bài học dày

### Quan sát
Nền ấm và spacing rộng giúp nội dung dài vẫn dễ vào.

### Điểm mạnh
- đọc êm;
- không tạo cảm giác thể chế;
- callout hòa vào bài mà vẫn thấy rõ;
- công thức nổi bật vừa đủ.

### Điểm yếu
- khi lượng nội dung tăng, softness dễ làm hierarchy bị “êm quá”;
- nếu panel/bo góc xuất hiện nhiều, bài học dễ trở thành generic education UI.

### Đánh giá
**PASS có điều kiện.**

Cần giảm số lượng container mềm và để typography gánh nhiều hierarchy hơn.

---

## 2.2. Graph khó

### Quan sát
Warm neutral làm graph dễ chịu, nhưng secondary vàng đất không tạo phân biệt mạnh khi nhiều curve/reference cùng tồn tại.

### Điểm mạnh
- axis/guide không tranh curve;
- overall calm tốt;
- point đặc/rỗng vẫn rõ.

### Điểm yếu
- hai curve ngang hàng có thể thiếu differentiation;
- yellow/ochre dễ mất lực trong print/grayscale;
- reference system có nguy cơ quá nhẹ.

### Đánh giá
**CONDITIONAL.**

Direction A cần một line grammar mạnh hơn palette grammar.

---

## 2.3. Mobile

### Quan sát
Direction A co xuống mobile khá tự nhiên.

### Điểm mạnh
- warmth vẫn giữ;
- surface/panel đọc dễ;
- không tạo áp lực thị giác.

### Điểm yếu
- nhiều padding/radius dễ chiếm diện tích;
- cần tránh “card hóa” mọi vùng.

### Đánh giá
**PASS.**

---

## 2.4. Grayscale / print

### Quan sát
Khi bỏ màu, identity suy giảm khá mạnh.

### Điểm mạnh
- structure vẫn đọc được;
- marker/line style còn hoạt động.

### Điểm yếu
- warmth gần như biến mất;
- đặc trưng A hiện phụ thuộc khá nhiều vào color temperature và surface treatment.

### Đánh giá
**CONDITIONAL.**

Direction A cần một typographic/line signature mạnh hơn để không phụ thuộc palette.

---

# 3. Stress Test B — Biên tập và chiều sâu

## 3.1. Bài học dày

### Quan sát
Đây là test mạnh nhất của Direction B.

### Điểm mạnh
- hierarchy chữ rất rõ;
- content dày vẫn có cấu trúc;
- serif heading tạo nhịp biên tập tốt;
- ít phụ thuộc container.

### Điểm yếu
- dễ trở nên nghiêm;
- nếu serif/body contrast quá mạnh sẽ kéo về publishing academic.

### Đánh giá
**PASS mạnh.**

---

## 3.2. Graph khó

### Quan sát
Direction B giữ line hierarchy tốt nhưng personality bị giảm khi chuyển sang graphics.

### Điểm mạnh
- neutral system rõ;
- reference/axis/curve phân lớp tốt;
- grayscale robustness cao.

### Điểm yếu
- graph có nguy cơ trông như textbook/editorial graph chung;
- thiếu một dấu hiệu sống động riêng của ZO Math.

### Đánh giá
**PASS về fidelity, CONDITIONAL về identity.**

---

## 3.3. Mobile

### Quan sát
Editorial hierarchy co xuống mobile vẫn tốt.

### Điểm mạnh
- ít phụ thuộc card;
- title/body/formula rõ;
- density hiệu quả.

### Điểm yếu
- serif heading trên màn nhỏ cần test thật;
- có nguy cơ tạo cảm giác nặng hơn A/C.

### Đánh giá
**PASS có điều kiện.**

---

## 3.4. Grayscale / print

### Quan sát
Đây là direction mạnh nhất trong grayscale.

### Điểm mạnh
- typography và line hierarchy vẫn tồn tại;
- không mất cấu trúc khi color bị loại;
- phù hợp PDF/print.

### Điểm yếu
- chính vì quá mạnh ở editorial/print, nguy cơ institutional coldness tăng.

### Đánh giá
**PASS mạnh.**

---

# 4. Stress Test C — Nhịp toán học

## 4.1. Bài học dày

### Quan sát
Direction C vẫn rõ, nhưng secondary teal bắt đầu có nguy cơ tạo quá nhiều focal points.

### Điểm mạnh
- sinh khí tốt hơn A/B;
- hierarchy có movement;
- công thức và focus dễ nhận biết.

### Điểm yếu
- nếu dùng teal + red đồng thời trong content dài, dễ phá điềm tĩnh;
- cần role discipline rất chặt.

### Đánh giá
**CONDITIONAL-PASS.**

---

## 4.2. Graph khó

### Quan sát
Đây là test mạnh nhất của Direction C.

### Điểm mạnh
- hai curve/reference phân biệt rõ;
- math graphic có identity;
- sống động mà vẫn đọc được.

### Điểm yếu
- teal rất dễ bị hiểu thành semantic role cố định dù chưa được định nghĩa;
- nếu chroma cao hơn nữa sẽ trượt generic edtech/tech.

### Đánh giá
**PASS về clarity, CONDITIONAL về semantic/color discipline.**

---

## 4.3. Mobile

### Quan sát
C co xuống mobile khá tốt.

### Điểm mạnh
- focal hierarchy mạnh;
- ít mềm hơn A, ít nặng hơn B;
- có cảm giác hiện đại mà chưa cần “AI aesthetic”.

### Điểm yếu
- nếu accent density cao ở màn nhỏ, nhanh thành noisy.

### Đánh giá
**PASS có điều kiện.**

---

## 4.4. Grayscale / print

### Quan sát
Khi mất màu, phần lớn “nhịp toán học” vẫn còn nhờ line/spacing, nhưng distinctiveness giảm.

### Điểm mạnh
- graph vẫn đọc;
- marker/line style còn hoạt động.

### Điểm yếu
- identity hiện vẫn dựa đáng kể vào cặp red/teal;
- cần chứng minh spatial rhythm đủ mạnh để sống không cần màu.

### Đánh giá
**CONDITIONAL.**

---

# 5. So sánh sau stress test

| Tiêu chí | A — Ấm và trong sáng | B — Biên tập và chiều sâu | C — Nhịp toán học |
|---|---|---|---|
| Bài học dày | Khá | Mạnh nhất | Khá |
| Graph khó | Khá | Rõ nhưng generic | Mạnh nhất |
| Mobile | Mạnh | Khá–mạnh | Mạnh |
| Grayscale/print | Khá | Mạnh nhất | Khá |
| Warmth | Mạnh nhất | Yếu nhất | Khá |
| Vitality | Khá | Yếu nhất | Mạnh nhất |
| Depth | Khá | Mạnh nhất | Khá |
| Mathematical identity | Khá | Khá | Mạnh nhất |
| Generic risk | warm-edtech | academic-editorial | edtech-tech |

---

# 6. Kết luận quan trọng: chưa có winner hoàn chỉnh

Stress test cho thấy:

- **A** giải tốt bài toán gần gũi nhưng chưa đủ mạnh về structural signature.
- **B** giải tốt depth/print/long-form nhưng thiếu vitality và có risk học thuật lạnh.
- **C** giải tốt vitality/math graphics nhưng color architecture dễ biến thành tech/edtech.

Do đó, **không nên chọn một direction nguyên trạng làm winner**.

---

# 7. Hybrid hypothesis xuất hiện

Một hướng có cơ sở hơn sau P2.2 là:

> lấy **warmth + accessibility của A**,  
> **typographic discipline + grayscale resilience của B**,  
> và **mathematical rhythm + line hierarchy của C**.

Nhưng hybrid này chưa được tạo.

Không được hiểu là “trộn ba palette”.

Cần trích **nguyên lý mạnh** từ mỗi direction, rồi dựng một direction v0.2 mới có logic thống nhất.

---

# 8. Những thành phần nên giữ để owner calibration

## Từ A
- nền/surface ấm có kiểm soát;
- cảm giác dễ bước vào;
- spacing breathing room;
- không institutional.

## Từ B
- typography hierarchy mạnh;
- ít phụ thuộc container;
- print/grayscale robustness;
- editorial discipline.

## Từ C
- line hierarchy;
- spatial rhythm;
- math graphics có sinh khí;
- focal logic rõ.

---

# 9. Những thành phần nên loại hoặc cảnh giác

## A
- bo tròn quá nhiều;
- softness như identity chính;
- phụ thuộc warmth/palette.

## B
- serif như shortcut cho chiều sâu;
- quá editorial;
- institutional coldness.

## C
- teal như semantic shortcut;
- nhiều accent;
- generic tech/edtech energy.

---

# 10. Owner calibration readiness

**Đây là thời điểm phù hợp để hỏi ý kiến chủ dự án.**

Lý do:

- ba direction đã qua một vòng stress;
- failure modes đã lộ;
- feedback bây giờ không còn chỉ là “thích màu nào”;
- chủ dự án có thể phản hồi trên các tension thật.

Owner calibration nên tập trung vào ba câu hỏi:

1. **Trong A/B/C, direction nào tạo cảm giác gần nhất với ZO Math hiện bạn hình dung — không cần là direction muốn chọn cuối?**
2. **Có yếu tố nào trong ba direction khiến bạn cảm thấy “đây chắc chắn không phải ZO Math” không?**
3. **Nếu phải chọn một tension quan trọng nhất cần xử lý trong hybrid v0.2, bạn ưu tiên:**
   - A: gần gũi ↔ học thuật;
   - B: sống động ↔ điềm tĩnh;
   - C: giản dị ↔ có bản sắc mạnh;
   - D: khác — mô tả ngắn.

Không hỏi palette/font/logo cụ thể ở bước này.

---

# 11. Bước tiếp theo

Sau owner calibration:

**P2.3 — Hybrid Visual Direction v0.2**

Mục tiêu:
- không ghép cơ học A+B+C;
- xây một direction thống nhất từ các principle được giữ;
- dựng lại 8 specimen;
- test lại dense lesson / hard graph / mobile / grayscale;
- sau đó mới bắt đầu R4/R5/R7 refinement cụ thể.

---

# 12. Kết luận

P2.2 cho thấy việc stress test trước owner feedback là đúng.

Ba direction v0.1 đã làm xong nhiệm vụ của chúng:
- tạo tương phản;
- làm lộ strength;
- làm lộ failure mode;
- chứng minh không direction nào nên được chọn nguyên trạng.

Từ đây, feedback của chủ dự án trở thành input cần thiết cho bước tiếp theo.
