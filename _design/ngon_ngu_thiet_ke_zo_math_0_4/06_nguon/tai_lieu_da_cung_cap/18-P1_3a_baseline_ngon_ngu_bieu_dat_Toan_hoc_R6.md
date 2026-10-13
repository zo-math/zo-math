# P1.3a — Baseline nội bộ cho R6: Ngôn ngữ biểu đạt Toán học

**Dự án:** ZO Math — Hệ thiết kế và ngôn ngữ thương hiệu  
**Phạm vi:** R6 — Ngôn ngữ biểu đạt Toán học  
**Trạng thái:** staging research  
**Ngày:** 2026-10-05

> P1.3a là baseline nội bộ.
> Không sửa graph/geometry/variation hiện có, không chọn màu/font mới, không tạo Design Principle hay Decision.

## 1. Mục tiêu

R6 nghiên cứu cách ZO Math biểu đạt Toán học sao cho:

- giữ đúng ý nghĩa Toán;
- giúp đọc, suy luận và kiểm chứng;
- dùng được qua HTML, PDF, SVG, video, social và asset sinh tự động;
- không để decoration hoặc implementation lịch sử quyết định ngược semantics.

P1.3a trả lời ở mức baseline:

1. ZO Math hiện có những hệ biểu đạt nào?
2. Hệ nào đã có nền mạnh?
3. Hệ nào còn xung đột?
4. Quy tắc nào là semantic/representation rule?
5. Quy tắc nào chỉ là visual convention hoặc implementation detail?
6. Brand Foundation và Brand Personality mới tạo ra constraint gì cho R6?
7. Phần nào có khả năng bất biến xuyên medium, phần nào cần modulation?

---

## 2. Nguồn nội bộ

Nguồn trực tiếp:

- `P0_2_khao_co_thiet_ke_ZO_Math.md`
- `P0_3_ban_do_bang_chung_quyet_dinh_thiet_ke_ZO_Math.md`
- `P0_4_ban_do_nghien_cuu_ZO_Math_Design_System.md`
- `Phong_cach_ZO_Math.md`
- `P1_1f_Brand_Foundation_Candidate_v0_1.md`
- `P1_2d_Brand_Personality_Candidate_v0_1.md`
- `P1_2e_ket_tinh_R2_va_gate_chuyen_tiep.md`

Các implementation cụ thể như graph v0.2, geometry v0.1, variation v0.1 được dùng như bằng chứng hiện trạng, không tự trở thành chuẩn Design System.

---

## 3. Phạm vi của “ngôn ngữ biểu đạt Toán học”

Trong R6, “ngôn ngữ biểu đạt Toán học” gồm ít nhất tám lớp:

1. **Notation và biểu thức**
2. **Công thức trong dòng và công thức tách dòng**
3. **Đồ thị hàm số / hệ trục / điểm / miền / tiệm cận**
4. **Hình học**
5. **Bảng biến thiên**
6. **Bảng dữ liệu / bảng Toán**
7. **Sơ đồ / diagram / quan hệ**
8. **Annotation, labels, emphasis và các dấu hiệu phụ trợ**

R6 không đồng nhất với:

- typography;
- color palette;
- layout;
- graph rendering tool;
- TikZ/Manim/CSS implementation.

Các chương trình đó liên quan, nhưng R6 trước hết nghiên cứu **meaning và representation roles**.

---

## 4. Hệ biểu đạt hiện có

### 4.1. Notation và công thức

Nguồn phong cách hiện tại cho thấy đã có phân biệt:

- biểu thức trong lời nói/phụ đề ưu tiên Unicode;
- vùng công thức riêng có thể dùng LaTeX đã dàn hoàn chỉnh;
- không sao chép raw LaTeX vào phụ đề;
- công thức/kí hiệu giữ hoa/thường theo ý nghĩa toán học.

Đây là dấu hiệu của một nguyên tắc quan trọng:

> cùng một nội dung Toán có thể cần **representation khác nhau theo medium**, nhưng semantic meaning phải giữ nguyên.

### Maturity
**Vừa** về quy tắc sử dụng theo medium; chưa có taxonomy xuyên hệ thống.

### Gap
Chưa có model rõ cho:
- prose math;
- display math;
- compact UI math;
- subtitle math;
- annotation math;
- accessibility/alt description.

---

### 4.2. Đồ thị hàm số

Đây là miền có nền mạnh nhất.

Các quy chuẩn hiện có đã mô tả:

- hệ trục tối giản;
- đường chính;
- điểm đặc/rỗng;
- tiệm cận;
- đường phụ;
- nhãn;
- miền;
- gián đoạn;
- phân biệt miền xác định, miền lấy mẫu và vùng quan sát;
- dùng line style để phân biệt một số vai trò thay vì chỉ đổi màu.

Graph v0.2 có pipeline sinh asset và role/token riêng.

### Maturity
**Mạnh về source, rule và pipeline.**

### Gap
- xung đột màu/role giữa các thế hệ;
- chưa có acceptance xuyên output;
- chưa rõ semantic mapping nào bất biến giữa print/web/video;
- chưa kiểm tra đầy đủ ca khó, collision, zoom nhỏ, grayscale.

---

### 4.3. Hình học

Geometry v0.1 đã có:

- nét thấy;
- nét khuất;
- nét nhấn;
- điểm;
- nhãn;
- fill;
- mask;
- độ dày nét;
- khoảng đệm;
- compiler YAML → TeX/PDF/SVG/PNG + receipt.

### Maturity
**Mạnh về production baseline và automation.**

### Gap
- chưa chứng minh đây là language chung xuyên medium;
- chưa có taxonomy đầy đủ về semantic roles hình học;
- chưa rõ modulation cho video/interactive;
- chưa tách hoàn toàn “đúng hình học” với “style hiện tại”.

---

### 4.4. Bảng biến thiên

Variation hiện có dùng chung token/logic với graph v0.2 và có pipeline.

### Maturity
**Vừa-mạnh về generation.**

### Gap
- semantic HTML còn yếu;
- accessibility chưa rõ;
- representation của tăng/giảm/cực trị/giới hạn trong các medium khác chưa được thống nhất;
- chưa rõ đâu là data semantics, đâu là visual convention.

---

### 4.5. Bảng dữ liệu và bảng Toán

Có nhiều bảng trong website/PDF/project con, nhưng baseline R6 chưa thấy một semantic model chung.

### Maturity
**Yếu-vừa.**

### Gap
- role header/body/note/derived value;
- alignment theo loại dữ liệu;
- math vs prose;
- responsive behavior;
- accessibility;
- khi nào dùng bảng, khi nào dùng diagram.

---

### 4.6. Sơ đồ / diagram

Chưa có evidence cho một hệ sơ đồ ZO Math thống nhất.

### Maturity
**Yếu.**

### Gap
- node/edge semantics;
- relation types;
- direction;
- emphasis;
- dependency;
- equivalence;
- process;
- proof structure;
- mapping sang video/motion.

---

### 4.7. Annotation và labels

Nhiều hệ hiện có đã dùng:

- nhãn điểm;
- nhãn đường;
- nhãn trục;
- annotation;
- callout;
- emphasis.

Nhưng chưa có taxonomy chung.

### Maturity
**Vừa ở từng subsystem, yếu ở toàn hệ.**

### Gap
- label hierarchy;
- persistent vs temporary annotation;
- semantic vs explanatory label;
- collision;
- language density;
- relation giữa label và color/line style.

---

## 5. Phân loại loại quy tắc

P1.3a đề xuất tách mọi quy tắc R6 vào bốn loại.

### A. Semantic rule

Quy định ý nghĩa cần giữ.

Ví dụ:
- điểm đặc khác điểm rỗng;
- nét khuất khác nét thấy;
- tiệm cận khác graph;
- domain khác sampling range;
- hypothesis khác conclusion.

Đây là lớp có khả năng bất biến cao nhất.

---

### B. Representation rule

Quy định cách một semantic role được biểu hiện.

Ví dụ:
- nét khuất dùng dashed;
- điểm rỗng dùng vòng tròn không tô;
- annotation gắn với object bằng leader/position;
- variation dùng mũi tên tăng/giảm.

Lớp này có thể shared nhưng cần test cross-medium.

---

### C. Visual convention

Quy ước hình thức có thể thay đổi.

Ví dụ:
- màu đỏ cho curve chính;
- nền vàng nhạt;
- độ dày nét cụ thể;
- radius;
- khoảng cách nhãn.

Không được xem là semantic rule nếu chưa có bằng chứng.

---

### D. Implementation detail

Chi tiết tool/runtime.

Ví dụ:
- TikZ macro;
- YAML key;
- CSS class;
- Manim object;
- file naming;
- export pipeline.

Không nên quyết định R6 semantics.

---

## 6. Những gì hiện đã có khả năng là semantic core

Các candidate sau có provenance nội bộ khá mạnh:

### SC-01 — Meaning before decoration
Biểu diễn phải ưu tiên ý nghĩa Toán trước decoration.

### SC-02 — Không dùng màu như kênh duy nhất
Thông tin Toán quan trọng không nên chỉ phân biệt bằng màu.

### SC-03 — Object continuity
Một đối tượng Toán phải giữ được identity khi chuyển trạng thái/biểu diễn.

### SC-04 — Distinguish mathematical roles
Các vai trò khác nhau về nghĩa cần có dấu hiệu phân biệt đủ rõ.

Ví dụ:
- graph / guide;
- visible / hidden;
- exact / approximate;
- domain / sampling;
- point included / excluded.

### SC-05 — Preserve conditions
Không được làm mất điều kiện, miền hoặc caveat chỉ để hình “sạch” hơn.

### SC-06 — Labels serve identification
Nhãn phải giúp nhận diện object/role, không trở thành decoration.

### SC-07 — Medium changes representation, not meaning
Medium có thể đổi cách biểu diễn nhưng không được đổi semantic meaning.

### SC-08 — Mathematical fidelity is a hard constraint
Một output đẹp nhưng sai Toán là thất bại.

Các mục này vẫn là **candidate semantic core**, chưa phải Design Principle.

---

## 7. Những gì chưa nên nâng thành semantic core

Chưa có đủ cơ sở để coi các mục sau là bất biến:

- đỏ là màu đường chính;
- vàng là màu secondary;
- nền vàng nhạt;
- STIX là font bắt buộc;
- trục luôn một kiểu cụ thể;
- khung luôn bo;
- mọi graph cùng kích thước;
- mọi medium dùng cùng label style;
- mọi geometry dùng đúng một thickness scale;
- mọi annotation phải cùng form.

Đây chủ yếu là visual convention hoặc implementation hiện tại.

---

## 8. Xung đột nội bộ cần giữ mở

### 8.1. Color-role divergence

Graph v0.2 và shared graph style hiện không hoàn toàn thống nhất vai trò strong/secondary.

=> Không giải quyết ở P1.3a.

---

### 8.2. Embedded style vs shared style module

Nguồn cũ từng coi style nhúng là “nguồn duy nhất”; tool mới dùng shared module.

=> Đây là architecture/implementation conflict, không phải semantic conflict.

---

### 8.3. Typography divergence

Web, PDF, graph, geometry và Manim đang dùng các font stack khác nhau.

=> R6 chỉ ghi yêu cầu fidelity/readability; R5 xử lý font architecture.

---

### 8.4. Color semantics vs structural hierarchy

Một số content block dùng màu để gán vai trò; review khác lại ưu tiên typography/whitespace.

=> R6/R4 cần phân định role nào thật sự semantic và role nào chỉ là content UI convention.

---

## 9. Constraint từ Brand Foundation và Personality

### 9.1. Gần gũi trong tôn trọng

Ngôn ngữ Toán không được:
- infantilize;
- thêm icon/character không cần thiết;
- làm notation “dễ thương”;
- đổi terminology chính xác để tạo cảm giác thân thiện.

Nó nên:
- dễ bước vào;
- nhãn dễ hiểu;
- giải thích object role khi cần.

---

### 9.2. Sống động nhưng điềm tĩnh

Biểu đạt Toán có thể sống động nhờ:
- biến đổi;
- highlight có mục đích;
- interaction;
- motion;
- progressive disclosure.

Nhưng:
- không mọi object cùng chuyển động;
- không mọi role cùng accent;
- không tạo nhiều điểm nhấn đồng thời.

---

### 9.3. Giản dị mà sâu sắc

R6 nên:
- bỏ dấu hiệu thừa;
- giữ cấu trúc sâu;
- không giảm nội dung Toán chỉ để đẹp;
- không thêm sophistication giả bằng visual complexity.

---

### 9.4. Rõ ràng và trong sáng

R6 phải:
- phân biệt role;
- làm rõ hierarchy;
- giữ điều kiện;
- không che logic;
- không dùng decoration để giả lập clarity.

---

## 10. Taxonomy nhiệm vụ biểu đạt sơ bộ

P1.3a đề xuất taxonomy ban đầu:

### M1 — Identify
Nhận diện object/điểm/đường/miền.

### M2 — Compare
So sánh hai hoặc nhiều object/trạng thái.

### M3 — Trace change
Theo dõi biến đổi theo tham số/thời gian/biến.

### M4 — Show relation
Thể hiện quan hệ phụ thuộc, tương ứng, song song, vuông góc, containment, implication.

### M5 — Mark condition
Đánh dấu miền, giả thiết, constraint, excluded region.

### M6 — Distinguish status
Phân biệt exact/approximate, included/excluded, visible/hidden, active/reference.

### M7 — Explain structure
Làm lộ cấu trúc hoặc decomposition.

### M8 — Support verification
Cho phép kiểm tra consistency, sign, scale, endpoint, continuity, relation.

### M9 — Summarize
Cô đọng pattern hoặc kết quả.

### M10 — Navigate reasoning
Hỗ trợ theo dõi chuỗi suy luận/chứng minh.

Taxonomy này là **working hypothesis**, cần test trên case thật.

---

## 11. Mapping sơ bộ subsystem ↔ nhiệm vụ

| Subsystem | Nhiệm vụ mạnh |
|---|---|
| Notation/formula | M4, M5, M7, M10 |
| Graph | M1, M2, M3, M5, M6, M8 |
| Geometry | M1, M2, M4, M6, M7 |
| Variation table | M3, M5, M6, M9 |
| Data table | M2, M6, M9 |
| Diagram | M4, M7, M10 |
| Annotation | M1, M5, M6, M8 |
| Motion | M3, M4, M7 |

Bảng này chưa phải specification.

---

## 12. Shared meaning vs medium-specific realization

### Có khả năng shared

- object identity;
- semantic roles;
- included/excluded;
- exact/approximate;
- visible/hidden;
- primary/reference;
- relation type;
- condition;
- continuity/discontinuity;
- annotation attachment;
- hierarchy.

### Có khả năng medium-specific

- line thickness;
- animation timing;
- label density;
- hover/focus;
- progressive reveal;
- subtitle representation;
- touch target;
- print contrast;
- screen-safe spacing.

R6 nên nghiên cứu semantics chung trước, rồi mới map sang medium.

---

## 13. Accessibility baseline

R6 phải xem accessibility là phần của semantic clarity, không phải kiểm tra sau cùng.

Candidate requirements:

- không dùng màu như kênh duy nhất;
- giữ đủ contrast;
- có text/structural equivalent khi biểu diễn quan trọng;
- line style/shape/label hỗ trợ phân biệt;
- math semantics không biến mất ở responsive/mobile;
- generated asset cần có route cho alt/description khi phù hợp;
- bảng biến thiên/diagram cần semantic representation nếu dùng trên web.

Chưa chọn standard hoặc threshold cụ thể ở P1.3a.

---

## 14. Maturity map

| Subsystem | Semantic maturity | Representation maturity | Pipeline maturity | Cross-medium evidence |
|---|---|---|---|---|
| Notation/formula | vừa | vừa | cao tùy medium | yếu-vừa |
| Graph | mạnh | mạnh | mạnh | vừa |
| Geometry | mạnh | vừa-mạnh | mạnh | yếu-vừa |
| Variation | vừa-mạnh | vừa | mạnh | yếu |
| Data table | yếu-vừa | vừa | vừa | yếu |
| Diagram | yếu | yếu | yếu-vừa | yếu |
| Annotation | vừa | vừa | phân tán | yếu |
| Motion-math mapping | yếu | yếu | có tool/video pipeline | yếu |

Đây là baseline research judgment, không phải acceptance rating chính thức.

---

## 15. Những gap quan trọng nhất

### G1 — Chưa có semantic model chung

Graph/geometry/variation có rule riêng nhưng chưa có vocabulary xuyên subsystem.

### G2 — Chưa có representation-role registry

Chưa có mapping chính thức:
semantic role → visual representation → medium variant.

### G3 — Chưa có acceptance cases xuyên output

Có tool và receipt nhưng visual/semantic acceptance chưa bao phủ đủ.

### G4 — Chưa có edge-case suite chung

Ví dụ:
- nhiều đường gần nhau;
- label collision;
- discontinuity dày;
- dense geometry;
- small-screen;
- grayscale;
- print;
- low-resolution video.

### G5 — Semantic HTML/accessibility còn yếu

Đặc biệt với variation/diagram/generated assets.

### G6 — Motion chưa được nối với semantic role

Có video pipeline nhưng chưa có grammar rõ cho object continuity, transformation, comparison, emphasis.

---

## 16. RQ cho R6

### RQ-DS-R6-001
Những semantic roles nào cần được định nghĩa chung xuyên graph, geometry, variation, diagram và annotation?

### RQ-DS-R6-002
Representation rule nào có thể shared xuyên medium, và rule nào phải modulation?

### RQ-DS-R6-003
Làm sao phân biệt rõ mathematical data, explanatory guide và decoration?

### RQ-DS-R6-004
Làm sao giữ object identity và semantic continuity khi chuyển từ static sang motion/interactive?

### RQ-DS-R6-005
Một bộ acceptance cases tối thiểu cần gồm những ca nào để kiểm tra correctness, readability, accessibility và personality alignment?

### RQ-DS-R6-006
Semantic HTML/text equivalent nào cần có cho table, variation, diagram và generated mathematical graphics?

---

## 17. Hypothesis ban đầu

### HYP-R6-01
R6 nên được tổ chức quanh **semantic roles**, không quanh từng tool.

### HYP-R6-02
Graph/geometry/variation hiện có đủ nền để trích semantic vocabulary chung mà không cần viết lại các subsystem.

### HYP-R6-03
Color nên là secondary encoding cho phần lớn mathematical roles, không phải channel duy nhất.

### HYP-R6-04
Line style, shape, position và label có thể là encoding bền hơn màu cho một số role xuyên print/screen.

### HYP-R6-05
Motion grammar sau này nên xuất phát từ semantic transformation:
appear / transform / compare / trace / reveal relation / emphasize / verify.

### HYP-R6-06
“Giản dị mà sâu sắc” trong R6 có thể chuyển thành nguyên tắc làm ít dấu hiệu hơn nhưng mỗi dấu hiệu mang semantic load rõ hơn.

---

## 18. Điều không làm ở P1.3a

Không:

- sửa graph v0.2;
- sửa geometry v0.1;
- sửa variation;
- chọn palette;
- chọn font;
- migration asset cũ;
- tạo semantic token;
- tạo component;
- render prototype;
- tạo Design Principle;
- tạo Decision;
- sửa `_research`;
- sửa production.

---

## 19. Readiness

P1.3a cho thấy R6 có nền mạnh hơn các chương trình visual khác:

- source/rule/pipeline đã có;
- semantic fragment đã tồn tại;
- conflict chủ yếu nằm ở cross-system mapping và acceptance.

Do đó R6 sẵn sàng cho bước nghiên cứu sâu tiếp theo.

---

## 20. Bước tiếp theo đề xuất

**P1.3b — Semantic Role Inventory cho ngôn ngữ biểu đạt Toán học**

Mục tiêu:

1. trích semantic roles từ graph v0.2, geometry v0.1, variation v0.1 và notation rules;
2. hợp nhất role trùng nghĩa;
3. giữ role subsystem-specific khi cần;
4. phân biệt:
   - mathematical object;
   - mathematical state;
   - relation;
   - condition;
   - guide;
   - annotation;
   - decoration;
5. chưa ánh xạ sang màu/font/token cụ thể;
6. tạo vocabulary candidate để sau đó test bằng representative cases.

P1.3b nên là bước phân tích nội bộ, chưa cần external research.

---

## 21. Kết luận

Baseline R6 cho thấy ZO Math không bắt đầu từ con số 0.

Hệ thống đã có nền đáng kể ở:

- graph;
- geometry;
- variation;
- notation theo medium;
- pipeline sinh asset.

Vấn đề chính không phải “thiết kế lại đồ thị cho đẹp hơn”, mà là:

> trích xuất và thống nhất **ngữ nghĩa biểu đạt** nằm bên dưới các subsystem hiện có, rồi mới quyết định cách realization qua màu, nét, chữ, layout và motion.

Đây là hướng phù hợp với Brand Personality mới:

- gần gũi trong tôn trọng;
- sống động nhưng điềm tĩnh;
- giản dị mà sâu sắc;
- rõ ràng và trong sáng.

P1.3a dừng ở baseline; chưa tạo chuẩn mới.
