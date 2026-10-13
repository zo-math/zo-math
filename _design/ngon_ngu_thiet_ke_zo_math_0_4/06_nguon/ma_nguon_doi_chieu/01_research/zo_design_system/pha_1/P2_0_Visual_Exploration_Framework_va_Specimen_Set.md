# P2.0 — Visual Exploration Framework và Specimen Set

**Dự án:** ZO Math — Hệ thiết kế và ngôn ngữ thương hiệu  
**Pha:** P2 — Visual Foundation / Visual Exploration  
**Trạng thái:** framework candidate / exploration setup  
**Ngày:** 2026-10-05

> P2.0 bắt đầu pha trực quan.
> Đây chưa phải visual direction, chưa chọn palette/font/logo/layout cuối, chưa sửa production.
> Mục tiêu là tạo một mặt bằng thử nghiệm chung để các hướng thiết kế sau này có thể được nhìn thấy, so sánh và kiểm chứng bằng cùng một nội dung.

---

## 1. Mục tiêu

P2.0 trả lời năm câu hỏi:

1. **Ta sẽ dùng những specimen nào để nhìn thấy ZO Math tương lai?**
2. **Những biến số trực quan nào được phép thử?**
3. **Những ý nghĩa nào tuyệt đối không được làm sai khi thử?**
4. **Mỗi phương án sẽ được đánh giá bằng tiêu chí nào?**
5. **Khi nào một visual direction đủ tốt để đi tiếp, và khi nào phải loại?**

P2.0 không cố tìm “một giao diện đẹp”.

Nó dựng một **visual test bench** cho toàn hệ.

---

# 2. Inputs đã đủ chín

## 2.1. Brand Foundation

Visual work phải phục vụ:

- một không gian giáo dục Toán học;
- người học ở trung tâm;
- hoạt động trí tuệ có ý nghĩa;
- Suy lí và Kiến tạo ý nghĩa;
- không xây identity từ AI aesthetic;
- vừa hữu ích trực tiếp vừa có chiều sâu lâu dài.

---

## 2.2. Brand Personality

Bốn formulation hiện dùng làm tiêu chí:

- **Gần gũi trong tôn trọng**
- **Sống động nhưng điềm tĩnh**
- **Giản dị mà sâu sắc**
- **Rõ ràng và trong sáng**

Điều kiện nền:

- chính xác;
- trung thực với bằng chứng;
- tôn trọng Toán học;
- tôn trọng người học.

---

## 2.3. R6 Visual Readiness constraints

Visual experimentation phải giữ:

1. mathematical object identity;
2. role distinction;
3. membership distinction;
4. domain / sampling range / observation window separation;
5. mathematical reference ≠ auxiliary guide;
6. projection visibility của geometry phải giữ đúng context;
7. label attachment phải rõ;
8. representation có thể đổi nhưng meaning không đổi;
9. decoration/brand marker không được mang mathematical authority.

---

# 3. Nguyên tắc vận hành visual exploration

## VF-01 — Cùng nội dung, nhiều hướng

Các direction phải dùng **cùng một specimen content**.

Không được:
- Direction A dùng bài dễ;
- Direction B dùng bài đẹp;
- Direction C dùng nội dung giàu hình hơn.

Nếu khác nội dung, không thể biết hiệu quả đến từ design hay content.

---

## VF-02 — Không chọn từng phần độc lập

Không chọn riêng:

- “màu đẹp nhất”;
- “font đẹp nhất”;
- “card đẹp nhất”;
- “logo đẹp nhất”.

Mỗi direction phải là một **hệ phối hợp** gồm:

- color;
- type;
- line;
- spacing;
- density;
- hierarchy;
- shape;
- mathematical graphics treatment.

Sau đó mới tách component để chuẩn hóa.

---

## VF-03 — Math-first, brand-visible

Toán học giữ quyền ưu tiên về meaning.

Nhưng visual exploration cũng phải đủ mạnh để ZO Math có personality và nhận diện.

Không chấp nhận hai cực:

- brand decoration lấn Toán;
- functional correctness nhưng hoàn toàn generic.

---

## VF-04 — Không đồng nhất consistency với sameness

Website, PDF, video, graph không cần trông giống hệt nhau.

Cần giữ:
- shared logic;
- shared personality;
- shared hierarchy principles;
- shared semantic roles.

Surface treatment có thể modulation theo medium.

---

## VF-05 — Một direction phải chịu được cả nội dung dễ và khó

Không đánh giá design chỉ bằng hero page hoặc một graph đẹp.

Direction phải chịu được:

- nội dung dày;
- formula dài;
- labels;
- nhiều trạng thái;
- mobile;
- grayscale/print;
- visual focus mạnh và yếu.

---

# 4. Specimen Set v0.1

P2.0 chọn **8 specimen**.

Không nhiều hơn ở vòng đầu để tránh exploration bị loãng.

---

## SP-01 — Trang bài học web

### Chức năng
Specimen chính để kiểm:

- reading hierarchy;
- body typography;
- heading structure;
- inline/display math;
- note/callout;
- spacing;
- rhythm;
- width;
- density;
- brand presence.

### Nội dung đại diện
Một bài Toán THPT thật có:

- title;
- 2–3 cấp heading;
- đoạn giải thích;
- công thức inline;
- công thức display;
- một ví dụ;
- một nhận xét;
- một hình/graph;
- một kết luận.

### Không dùng
- landing page marketing;
- hero banner;
- card gallery.

Lý do:
Design System giáo dục phải chứng minh nó đọc được **nội dung thật** trước.

---

## SP-02 — Trang PDF/học liệu A4

### Chức năng
Kiểm:

- print hierarchy;
- text/math balance;
- margins;
- line length;
- block spacing;
- figure placement;
- caption;
- grayscale;
- brand restraint.

### Nội dung
Cùng nội dung lõi với SP-01.

### Mục đích
So xem visual language có còn là ZO Math khi mất interaction và viewport động hay không.

---

## SP-03 — Graph specimen

### Thành phần bắt buộc
- axis;
- một curve chính hoặc hai curve ngang hàng;
- asymptote;
- auxiliary/projection guide;
- included/excluded point;
- label;
- observation window;
- nếu phù hợp: discontinuity/branch break.

### Kiểm
- hierarchy;
- semantic distinction;
- line grammar;
- marker grammar;
- label system;
- color dependency;
- print/grayscale viability.

---

## SP-04 — Geometry specimen

### Thành phần
- point/vertex;
- visible edge;
- hidden edge;
- auxiliary segment;
- label;
- angle/right-angle marker;
- nếu phù hợp: surface fill hoặc tangency.

### Kiểm
- line hierarchy;
- depth;
- label treatment;
- relation marker clarity;
- auxiliary/main distinction;
- geometric calmness.

---

## SP-05 — Variation specimen

### Thành phần
- breakpoint;
- interval;
- derivative sign;
- increasing/decreasing trend;
- value at breakpoint;
- excluded point.

### Kiểm
- table semantics;
- row hierarchy;
- sign/trend distinction;
- density;
- print clarity;
- non-color encoding.

---

## SP-06 — Compact learning card

### Chức năng
Kiểm personality trong surface nhỏ.

### Nội dung
Một thẻ có:

- tên chủ đề;
- một biểu thức hoặc graph thumbnail;
- một metadata line;
- một CTA nhỏ.

### Kiểm
- visual identity;
- hierarchy;
- recognizability;
- “generic edtech” risk;
- logo/motif pressure.

SP-06 không được trở thành nơi quyết định toàn bộ brand style.

---

## SP-07 — Video frame tĩnh

### Khung
Một frame 16:9 hoặc 9:16 có:

- narration subtitle;
- một formula/graph;
- một highlighted object;
- brand marker nhỏ;
- safe zone.

### Kiểm
- sống động nhưng điềm tĩnh;
- object hierarchy;
- subtitle/math coexistence;
- color contrast;
- focus mechanics.

Chưa test motion timing ở P2.0.

---

## SP-08 — Navigation / interface shell

### Thành phần
- top navigation;
- page title;
- breadcrumb hoặc contextual navigation;
- sidebar/TOC nếu cần;
- content entry;
- active state;
- mobile equivalent.

### Kiểm
- clarity;
- warmth;
- density;
- institutional-coldness risk;
- generic SaaS risk;
- relationship giữa chrome và mathematical content.

---

# 5. Specimen relationships

Không xem 8 specimen là 8 sản phẩm độc lập.

### Core content pair
SP-01 ↔ SP-02

Cùng nội dung, hai medium.

### Mathematical graphics trio
SP-03 ↔ SP-04 ↔ SP-05

Kiểm semantic expression language.

### Brand compression pair
SP-06 ↔ SP-07

Kiểm personality trong surface nhỏ / high-attention.

### System shell
SP-08

Kiểm interface architecture.

---

# 6. Dimensions được phép thử

## D1 — Color architecture

Được thử:

- warm vs neutral base;
- red/yellow legacy roles;
- one-accent vs two-accent;
- chroma intensity;
- background warmth;
- semantic neutrals;
- highlight strategy;
- grayscale fallback.

Không được:

- dùng màu làm kênh semantic duy nhất;
- gán meaning toán trực tiếp cho đỏ/vàng chỉ vì lịch sử;
- chọn palette chỉ từ logo hiện tại.

---

## D2 — Typography architecture

Được thử:

- serif/sans balance;
- humanist vs geometric sans;
- body vs UI distinction;
- math typography relationship;
- heading rhythm;
- contrast of weight/size;
- caption/label system.

Không được:

- suy “học thuật = serif”;
- suy “hiện đại = geometric sans”;
- dùng type display làm giảm readability;
- hi sinh tiếng Việt hoặc glyph Toán.

---

## D3 — Line grammar

Được thử:

- stroke hierarchy;
- visible/hidden;
- guide/reference distinction;
- curve/axis contrast;
- border intensity;
- separator logic.

Không được:

- biến line style thành decoration vô nghĩa;
- để auxiliary mạnh ngang main object;
- dùng dashed/solid tùy ý nếu làm đổi role.

---

## D4 — Shape language

Được thử:

- sharp vs soft geometry;
- corner radius;
- panel/container shape;
- point marker form;
- tag/chip geometry;
- relation marker form.

Không được:

- suy “gần gũi = bo tròn mọi thứ”;
- biến shape brand motif thành kí hiệu toán.

---

## D5 — Spacing / density

Được thử:

- compact ↔ spacious;
- paragraph rhythm;
- equation spacing;
- figure spacing;
- card density;
- sidebar density;
- white space distribution.

Không được:

- dùng nhiều khoảng trắng đến mức mất continuity;
- nén đến mức label/math collision;
- coi “minimal” = nhiều khoảng trắng.

---

## D6 — Layout / hierarchy

Được thử:

- centered vs left-weighted;
- single-column vs constrained multi-column;
- reading width;
- figure anchoring;
- callout placement;
- sidebar/TOC behavior;
- conclusion placement.

Không được:

- phá reading order;
- để chrome cạnh tranh content;
- dùng layout symmetry nếu làm mờ hierarchy.

---

## D7 — Mathematical graphics treatment

Được thử:

- axis visual weight;
- curve/reference contrast;
- marker grammar;
- label distance;
- area fill strategy;
- graph frame/background;
- geometry depth cues;
- variation row/cell styling.

Không được:

- đổi meaning;
- universalize một graph convention sang geometry/variation nếu không có rationale.

---

## D8 — Brand marking intensity

Được thử:

- logo frequency;
- wordmark scale;
- motif frequency;
- accent placement;
- branded frame vs unbranded content area.

Không được:

- dùng logo/motif để bù cho visual language yếu;
- đặt brand marker vào semantic area của math graphic;
- ép mọi page/cảnh phải có motif.

---

# 7. Dimensions chưa thử ở P2.0

Giữ ngoài vòng đầu:

- motion easing;
- motion durations;
- sonic identity;
- music;
- voice;
- animation choreography;
- responsive microinteraction;
- icon library chi tiết;
- full logo redesign.

Các phần này sẽ đến sau khi static visual grammar đủ rõ.

---

# 8. Acceptance rubric

Mỗi visual direction sau này được chấm theo 8 trục.

Không dùng “đẹp/xấu” làm tiêu chí chính.

---

## A1 — Gần gũi trong tôn trọng

Đạt khi:
- dễ bước vào;
- không lạnh;
- không trẻ con;
- không cute edtech;
- không institutional authority.

---

## A2 — Sống động nhưng điềm tĩnh

Đạt khi:
- có rhythm;
- có focal hierarchy;
- không dead/static;
- không noisy;
- không quá nhiều accent.

---

## A3 — Giản dị mà sâu sắc

Đạt khi:
- ít cạnh tranh không cần thiết;
- vẫn giữ structure;
- không “empty minimalism”;
- không complexity phô diễn.

---

## A4 — Rõ ràng và trong sáng

Đạt khi:
- hierarchy đọc được ngay;
- mathematical role không nhập nhằng;
- visual logic không cần đoán;
- content khó vẫn rõ.

---

## A5 — Mathematical fidelity

Hard gate.

Fail nếu:
- graph role sai;
- hidden/visible bị nhầm;
- included/excluded chỉ dựa màu;
- notation mất meaning;
- variation role bị nhập;
- decoration trông như math semantics.

---

## A6 — Cross-medium resilience

Đạt khi direction vẫn sống được ở:

- web;
- PDF;
- graph;
- small card;
- video frame.

Không yêu cầu giống nhau từng pixel.

---

## A7 — Distinctiveness without spectacle

Đạt khi:
- có thể nhận ra “đây là ZO Math”;
- không cần logo lớn;
- không cần visual trick;
- không giống generic edtech / AI startup / academic institution.

---

## A8 — Systemizability

Đạt khi có khả năng về sau chuyển thành:

- semantic roles;
- tokens;
- components;
- automation;
- cross-medium rules.

Một direction đẹp nhưng quá phụ thuộc art direction thủ công sẽ bị trừ điểm.

---

# 9. Hard gates

Một direction bị loại ngay nếu vi phạm một trong các điều sau.

## HG-01 — Mathematical meaning bị sai hoặc nhập nhằng

## HG-02 — Color là kênh duy nhất cho semantic distinction

## HG-03 — Typography làm mất glyph/notation/tiếng Việt

## HG-04 — Branding lấn mathematical content

## HG-05 — Cute/gamified/institutional/futuristic shortcut trở thành identity chính

## HG-06 — Direction chỉ hoạt động trên hero/mockup, thất bại ở bài học thật

## HG-07 — Không thể chuyển sang PDF/print cơ bản

## HG-08 — Không có đường để systemize

---

# 10. Evaluation protocol

Mỗi direction phải được render trên **cùng 8 specimen**.

Mỗi specimen được đánh:

- Pass
- Conditional
- Fail

theo A1–A8.

Không cộng điểm số thành một “tổng điểm tuyệt đối”.

Lý do:
Một hard semantic failure không thể được bù bởi 7 mục thẩm mỹ tốt.

---

# 11. Visual direction count

Vòng đầu chỉ tạo:

**3 directions.**

Không 2:
- dễ thành “A hoặc B”.

Không 4–6:
- quá nhiều để phân tích sâu.

Ba direction phải:
- cùng Brand Foundation;
- cùng Brand Personality;
- cùng R6 constraints;
- khác nhau đủ rõ ở visual realization.

---

# 12. Cách tạo 3 direction

Không đặt tên kiểu:

- Modern
- Classic
- Premium

vì quá mơ hồ.

Mỗi direction phải được mô tả bằng **design hypothesis**.

Ví dụ cấu trúc tên:

### Direction A
“Warm clarity through restrained contrast”

### Direction B
“Editorial depth through typographic structure”

### Direction C
“Mathematical vitality through active spatial rhythm”

Các tên trên chỉ minh họa cách đặt hypothesis, **không phải direction đã chọn**.

---

# 13. Những axis bắt buộc phải tạo khác biệt giữa directions

Ít nhất 5 trong 8 dimensions phải thực sự khác.

Nếu cả ba direction chỉ đổi palette, đó không phải exploration.

Các axis nên tạo contrast:

1. type architecture;
2. color architecture;
3. spatial density;
4. shape softness;
5. line hierarchy;
6. brand marking intensity;
7. graph surface treatment;
8. UI chrome restraint.

---

# 14. Những invariant phải giữ giữa directions

Không được thay đổi:

- nội dung specimen;
- semantic role;
- mathematical correctness;
- hierarchy task;
- information architecture;
- page function;
- accessibility baseline tối thiểu;
- Brand Personality targets.

Nếu thay invariant, ta đang so sản phẩm khác nhau chứ không còn so design direction.

---

# 15. R3/R4/R5/R7 trong P2.0

P2.0 không xử lý từng Research Program như silo.

## R3 — Identity architecture
Ở vòng đầu chỉ test:
- brand presence;
- logo/motif intensity;
- relationship brand ↔ content.

Chưa redesign logo.

## R4 — Color
Test:
- architecture;
- role;
- intensity;
- contrast;
- cross-medium resilience.

Chưa chốt hex cuối.

## R5 — Typography
Test:
- role architecture;
- prose/math relationship;
- hierarchy;
- readability.

Chưa chọn canonical font stack cuối.

## R7 — Layout
Test:
- spacing;
- density;
- hierarchy;
- reading width;
- structural rhythm.

Chưa chốt spacing token.

---

# 16. Source material cho specimen

Ưu tiên lấy từ sản phẩm ZO Math thật hiện có.

Không tạo demo lorem ipsum.

### Web/PDF
Một đoạn học liệu THPT có:
- prose;
- formula;
- example;
- note;
- conclusion.

### Graph
Một graph có asymptote/guide/point status.

### Geometry
Một geometry có visible/hidden + relation marker.

### Variation
BBT13 hoặc sample tương đương đã được source P1.3c đọc.

### Card
Một thẻ project/lesson có thật.

### Video
Một frame từ nội dung Toán có thật.

---

# 17. Deliverables sau P2.0

P2.0 bản thân chỉ tạo framework.

Bước sau phải tạo:

## P2.1 — Visual Directions v0.1

Mỗi direction gồm ít nhất:

1. design hypothesis;
2. palette candidate;
3. typography candidate;
4. spacing/density behavior;
5. line/shape grammar;
6. 8 specimen renders;
7. rationale nối về R1/R2/R6;
8. hard-gate audit;
9. strengths;
10. failure modes.

---

# 18. Không làm ở P2.0

Không:

- chốt palette;
- chốt font;
- redesign logo;
- sửa website;
- sửa PDF production;
- sửa graph tool;
- sửa geometry tool;
- sửa variation tool;
- tạo design tokens;
- tạo component library;
- commit;
- push;
- chọn visual direction cuối.

---

# 19. Visual exploration success criteria

P2.0 được xem là đủ nếu:

1. specimen set bao phủ đủ web/PDF/math/video/UI;
2. mỗi specimen có chức năng kiểm rõ;
3. dimensions thử nghiệm được tách khỏi semantic invariants;
4. acceptance rubric có thể loại phương án sai;
5. 3 directions sau này có thể so bằng cùng content;
6. không cần thêm semantic research trước khi bắt đầu render visual alternatives.

---

# 20. Gate kết luận

P2.0 xác lập:

> Từ đây, ZO Math Design System chuyển từ nghiên cứu “meaning phải giữ gì” sang nghiên cứu “meaning đó có thể được biểu hiện bằng những visual systems nào”.

Điều quan trọng:

- visual work bắt đầu;
- nhưng không phải free-form styling;
- mỗi quyết định phải chịu kiểm bởi Brand Foundation, Brand Personality và R6;
- không chọn một phần riêng lẻ bằng gu;
- không để current implementation trở thành default chỉ vì đã tồn tại.

---

# 21. Bước tiếp theo duy nhất

**P2.1 — Visual Directions v0.1**

Mục tiêu:

- dựng **3 visual directions có khác biệt thật sự**;
- dùng cùng 8 specimen;
- chưa chọn winner ngay;
- so sánh bằng acceptance rubric P2.0.

P2.1 là bước đầu tiên người dùng phải có thể **nhìn thấy ZO Math tương lai** dưới nhiều khả năng khác nhau.
