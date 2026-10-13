# P2.3 — Hybrid Visual Direction A+ v0.2

**Dự án:** ZO Math — Hệ thiết kế và ngôn ngữ thương hiệu  
**Pha:** P2 — Visual Foundation / Visual Exploration  
**Trạng thái:** hybrid visual direction candidate v0.2  
**Ngày:** 2026-10-05

> P2.3 lấy Direction A làm base direction sau owner calibration, nhưng không giữ A nguyên trạng. Mục tiêu là xây một hệ trực quan giàu bằng chứng hơn, có thể kiểm trên nhiều medium, đồng thời hấp thụ có chọn lọc các điểm mạnh của B và C.

## 1. Owner-confirmed inputs

Chủ dự án xác nhận:

1. Direction A — “Ấm và trong sáng” gần nhất với hình dung hiện tại về ZO Math.
2. Công thức Toán thực sự phải được dàn bằng LaTeX trong vùng công thức phù hợp; mockup dùng chữ thường để giả công thức không được xem là hướng trình bày tương lai.
3. ZO Math không lạm dụng các dấu suy ra hoặc tương đương. Khi không cần kí hiệu hóa quan hệ logic, ưu tiên lập luận bằng câu văn.
4. Bằng chứng thị giác ở P2.1/P2.2 còn quá ít để yêu cầu owner calibration sâu hơn.

P2.3 vì vậy không hỏi thêm gu; nó mở rộng lượng visual evidence trước.

## 2. Design hypothesis v0.2

Tên làm việc:

**Direction A+ — Ấm, trong sáng, có kỉ luật**

Giả thuyết:

> ZO Math có thể gần gũi mà không mềm yếu, có chiều sâu mà không lạnh, sống động mà không cần nhiều màu hoặc hiệu ứng. Hệ trực quan nên dùng nền ấm và khoảng thở để tạo khả năng bước vào; typography và hierarchy để giữ kỉ luật; line grammar và mathematical graphics để tạo sinh khí và bản sắc.

## 3. Những gì giữ từ A

- nền ấm;
- surface sáng;
- accent đỏ tiết chế;
- nhịp thoáng;
- cảm giác dễ bước vào;
- không institutional;
- không “academic authority” bằng hình thức.

## 4. Những gì hấp thụ từ B

Không lấy serif như shortcut cho chiều sâu.

Chỉ giữ:

- hierarchy phải đủ mạnh khi nội dung dày;
- typography gánh cấu trúc nhiều hơn container;
- print/grayscale phải vẫn đọc tốt;
- border và separator dùng có mục đích;
- PDF không được phụ thuộc vào warmth/color để giữ identity.

## 5. Những gì hấp thụ từ C

Không lấy teal hoặc cặp đỏ–teal làm signature.

Chỉ giữ:

- line hierarchy mạnh hơn;
- mathematical graphics có nhịp;
- guide/reference/main object phân tầng rõ;
- focal logic đủ sống động mà không noisy.

## 6. Constraint mới về ngôn ngữ Toán

### 6.1. Công thức

Khi biểu thức là công thức thực sự hoặc là object Toán chính:

- dùng LaTeX để dàn;
- không giả lập bằng text formatting;
- giữ notation, hoa/thường và spacing toán học đúng.

### 6.2. Lập luận

Không dùng `⇒`, `⇔` chỉ để rút ngắn câu.

Ưu tiên:

- “Vì …, nên …”;
- “Do đó …”;
- “Suy ra …” bằng câu văn khi phù hợp;
- chỉ dùng kí hiệu logic khi bản thân cấu trúc kí hiệu là đối tượng cần nhìn thấy.

Đây là constraint xuyên web/PDF/video/caption, không chỉ là lựa chọn văn phong trong specimen hiện tại.

## 7. Prototype set v0.2

P2.3 đã dựng 8 specimen độc lập.

### SP-01 — Web lesson

Kiểm:
- bài học dài;
- prose + LaTeX display;
- note;
- conclusion;
- graph;
- hierarchy không phụ thuộc quá nhiều vào card.

Phát hiện:
- warmth vẫn tạo cảm giác gần gũi;
- typography cần giữ vai trò chính;
- công thức LaTeX làm hệ thống “đúng Toán” hơn rõ rệt so với mockup P2.1;
- việc viết lập luận bằng câu làm trang tự nhiên và đúng personality hơn dùng mũi tên logic.

### SP-02 — PDF page

Kiểm:
- A4-like structure;
- grayscale resilience;
- formula/prose balance;
- note block;
- graph placement.

Phát hiện:
- A+ có thể sống ở print mà không cần bo góc nhiều;
- identity cần đến từ nhịp, type và line chứ không chỉ nền ấm.

### SP-03 — Graph

Kiểm:
- curve;
- asymptote;
- axis;
- guide;
- point status;
- label hierarchy.

Phát hiện:
- line grammar là thành phần bản sắc tiềm năng quan trọng;
- đỏ có thể làm accent chính nhưng không mang semantic cố định;
- reference màu đất cần kiểm grayscale thêm.

### SP-04 — Geometry

Kiểm:
- visible/hidden;
- auxiliary;
- relation marker;
- labels.

Phát hiện:
- warmth không cần được đưa vào mọi nét;
- geometry nên trung tính hơn interface surface;
- relation marker cần nổi vừa đủ để không thành decoration.

### SP-05 — Variation table

Kiểm:
- breakpoint;
- interval;
- derivative sign;
- trend;
- excluded point.

Phát hiện:
- hệ bảng cần line hierarchy chặt hơn các card UI;
- màu chỉ nên hỗ trợ, không định nghĩa tăng/giảm/điểm loại;
- đây là specimen quan trọng cho R4/R5/R7 vì density cao.

### SP-06 — Mobile

Kiểm:
- content compression;
- math display;
- graph placement;
- note;
- no over-cardification.

Phát hiện:
- A+ co xuống mobile tốt nếu giảm padding;
- formula display phải được dành vùng riêng thay vì thu nhỏ;
- không nên biến mọi đoạn thành container bo tròn.

### SP-07 — Learning card

Kiểm:
- brand compression;
- recognizability;
- formula/graph thumbnail;
- CTA.

Phát hiện:
- một surface nhỏ vẫn có thể nhận ra A+ mà không cần logo lớn;
- graph thumbnail + type hierarchy có giá trị nhận diện hơn decoration.

### SP-08 — Video frame

Kiểm:
- headline;
- graph;
- subtitle safe zone;
- accent;
- brand marker.

Phát hiện:
- A+ có thể sống động bằng composition và focal rhythm;
- không cần dark cinematic look;
- subtitle và math content phải có vùng riêng;
- brand motif nên nhỏ và ngoài semantic math area.

## 8. Hệ visual candidate hiện ra sau P2.3

### Base surface

Candidate mạnh:
- warm off-white canvas;
- near-white reading surface;
- warm neutral support surface.

Chưa chốt mã màu.

### Accent

Candidate mạnh:
- một đỏ trầm/ấm làm accent chính.

Vàng/ochre:
- chỉ là secondary candidate;
- chưa đủ bằng chứng để giữ làm brand accent bắt buộc.

### Typography

Candidate architecture:
- sans mạnh cho reading/UI;
- hierarchy từ size/weight/spacing trước khi thêm decorative type;
- math type phải tương thích LaTeX và notation.

Chưa chốt font family.

### Shape

Candidate:
- softness vừa phải ở surface lớn;
- radius không dùng mặc định cho mọi block;
- mathematical graphics ít softness hơn UI.

### Line grammar

Candidate mạnh:
- line hierarchy là một phần quan trọng của identity;
- main object > reference > guide > frame;
- line style phải còn hoạt động khi mất màu.

### Spatial rhythm

Candidate mạnh:
- generous nhưng không “luxury whitespace”;
- breathing room tập trung quanh semantic groups;
- density thay đổi theo task.

## 9. Những thứ P2.3 loại khỏi hướng phát triển hiện tại

Không coi là hướng ưu tiên:

- bo tròn như signature;
- nền kem như toàn bộ identity;
- serif như shortcut cho chiều sâu;
- teal như shortcut cho vitality;
- two-accent system mặc định;
- card hóa mọi block;
- công thức giả bằng plain text;
- chuỗi lập luận dày đặc kí hiệu `⇒`, `⇔`;
- brand motif nằm trong vùng semantic của graph/geometry.

## 10. Những gì vẫn chưa đủ bằng chứng

Chưa chốt:

- exact palette;
- primary/secondary brand colors;
- canonical font family;
- exact type scale;
- exact spacing scale;
- exact corner radius scale;
- logo architecture;
- illustration language;
- icon language;
- graph token values;
- geometry token values;
- motion;
- dark mode;
- sonic identity.

## 11. Self-reflection gate

P2.3 có làm dự án tiến gần tới Design System có thể nhìn, test và dùng không?

**Có.**

Lí do:

- visual evidence đã tăng từ board tổng quát thành 8 specimen độc lập;
- direction A đã được biến đổi thành hệ A+ thay vì chỉ được “ưa thích”;
- owner feedback đã làm thay đổi thật sự cách trình bày công thức và lập luận;
- các nguyên tắc mạnh của B/C đã được hấp thụ ở mức structure, không copy style;
- các quyết định lớn vẫn chưa bị chốt quá sớm.

## 12. Owner calibration sau P2.3

Sau P2.3, owner feedback có thể đi sâu hơn P2.2, nhưng **không bắt buộc phải chốt direction ngay**.

Feedback hữu ích nhất sẽ là:

- phần nào của A+ đã bắt đầu “đúng ZO Math”;
- phần nào còn generic hoặc không đúng;
- mức ấm hiện tại có quá nhiều/ít;
- hierarchy có đủ kỉ luật;
- mathematical graphics có đủ sinh khí;
- card/video có còn cùng một hệ với web/PDF hay không.

## 13. Bước tiếp theo đề xuất

**P2.4 — Owner Calibration + Visual Principle Extraction**

Mục tiêu:

1. lấy phản hồi từ bộ 8 specimen A+;
2. không hỏi “thích màu nào” một cách rời rạc;
3. trích các visual principles có thể promotion candidate;
4. xác định R4 — color, R5 — typography và R7 — layout cần nghiên cứu sâu theo thứ tự nào;
5. chỉ sau đó mới bắt đầu refinement thông số cụ thể.

## 14. Kết luận

P2.3 không phải “Direction A đẹp hơn”.

Nó là lần đầu Direction A được phát triển thành một **visual system hypothesis đủ rộng**:

> ấm để dễ bước vào;  
> typography để giữ kỉ luật;  
> line và spatial rhythm để tạo sinh khí;  
> mathematical semantics để giữ sự trong sáng;  
> branding hiện diện nhưng không giành quyền của Toán học.

Tên làm việc hiện tại:

**A+ — Ấm, trong sáng, có kỉ luật.**
