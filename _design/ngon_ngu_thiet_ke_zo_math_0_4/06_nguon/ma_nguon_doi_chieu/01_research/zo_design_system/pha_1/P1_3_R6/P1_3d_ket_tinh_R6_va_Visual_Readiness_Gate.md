# P1.3d — Kết tinh R6 và Visual Readiness Gate

**Dự án:** ZO Math — Hệ thiết kế và ngôn ngữ thương hiệu  
**Phạm vi:** R6 — Ngôn ngữ biểu đạt Toán học  
**Trạng thái:** synthesis / gate preparation  
**Ngày:** 2026-10-05

> P1.3d không mở semantic research mới.
> Mục tiêu là reconcile P1.3b với P1.3c, kiểm inventory trên một số representative cases hiện có, rồi xác định R6 đã đủ để làm constraint cho visual work hay chưa.

---

## 1. Mục tiêu

P1.3d làm bốn việc:

1. phục hồi lineage giữa P1.3b và P1.3c;
2. reconcile các candidate role trong P1.3b bằng direct-source evidence của P1.3c;
3. kiểm semantic inventory trên một bộ representative cases tối thiểu;
4. quyết định:
   - role nào đủ mạnh để dùng như constraint cho visual exploration;
   - role nào phải giữ subsystem-specific;
   - role nào vẫn open;
   - R6 có còn blocker trước visual work hay không.

Không tạo:

- semantic token;
- visual token;
- color system;
- typography system;
- graph style mới;
- geometry style mới;
- component;
- Design Principle chính thức;
- Decision chính thức.

---

## 2. Nguồn

Nguồn chính:

- `P1_3b_Semantic_Role_Inventory_R6.md`
- `P1_3c_deep_source_read_semantic_roles_R6.md`

Nguồn nền:

- `P1_3a_baseline_ngon_ngu_bieu_dat_Toan_hoc_R6.md`
- `P1_2d_Brand_Personality_Candidate_v0_1.md`
- `P1_2e_ket_tinh_R2_va_gate_chuyen_tiep.md`

P1.3c đọc trực tiếp 13 source subsystem:
- graph: 4;
- geometry: 3;
- variation: 6.

---

## 3. Phục hồi lineage P1.3b → P1.3c

P1.3c ghi rằng trong repository lúc đó không tìm thấy file P1.3b.

Điều này là **gap provenance**, không phải bằng chứng rằng P1.3b không tồn tại.

P1.3b đã tạo:

- candidate vocabulary v0.1;
- phân loại mathematical object / state / relation / condition / guide / annotation / decoration;
- các candidate shared roles;
- deliberate gaps cho variation và geometry;
- các ranh giới như:
  - domain ≠ sampling range;
  - sampling range ≠ observation window;
  - asymptote ≠ generic guide;
  - color ≠ semantic role;
  - brand marker ≠ mathematical symbol.

P1.3c sau đó direct-source-read các subsystem và đóng vai trò **verification/refinement** cho P1.3b.

Do đó lineage đúng là:

> P1.3a baseline  
> → P1.3b semantic inventory candidate v0.1  
> → P1.3c direct-source verification / inventory evidence v0.2  
> → P1.3d synthesis + readiness gate

Không xem P1.3c là thay thế hoặc xoá P1.3b.

---

## 4. Những candidate của P1.3b được giữ

### 4.1. Role-first trước visual encoding

Được P1.3c hỗ trợ mạnh ở cấp cách tổ chức nghiên cứu:

> semantic meaning → role → representation → medium adaptation → implementation.

Không promote thành Design Principle ở bước này, nhưng đủ làm **working architecture cho visual exploration**.

---

### 4.2. Domain / sampling range / observation window phải tách

Được direct source graph xác nhận rõ.

Kết luận:

- `domain` = meaning Toán;
- `sampling range` = phạm vi kỹ thuật để dựng;
- `observation window` = vùng được hiển thị.

Ba lớp này không được gộp trong visual or tool design.

**Trạng thái:** đủ mạnh làm visual constraint.

---

### 4.3. Asymptote khác generic guide

P1.3c xác nhận graph có style/API và yêu cầu toán học riêng cho asymptote.

Kết luận:

- asymptote là mathematical reference;
- auxiliary/projection guide là supporting guide;
- representation có thể khác theo medium, nhưng meaning không được nhập nhằng.

**Trạng thái:** đủ mạnh làm visual constraint.

---

### 4.4. Included / excluded

Direct source xác nhận:

- graph có endpoint/point status;
- variation có `excluded_columns`.

Kết luận:

- membership status là semantic;
- marker rỗng/đặc hoặc glyph `∥` chỉ là realization hiện tại;
- không ép geometry visibility vào cùng family.

**Trạng thái:** đủ mạnh ở graph + variation; không universalize sang geometry.

---

### 4.5. Visible / hidden

Direct source xác nhận geometry dùng visible/hidden theo camera/projection.

Kết luận:

- đây là projection state;
- không đồng nghĩa membership;
- không đồng nghĩa object exists/does not exist.

**Trạng thái:** subsystem-specific semantic.

---

### 4.6. Emphasis / primary

P1.3c sửa giả thuyết P1.3b:

- graph hierarchy phụ thuộc task;
- hai curve có thể ngang hàng;
- geometry `emphasized` là visual/render flag.

Kết luận:

- không tạo một role universal `object.primary`;
- cần tách:
  - semantic identity;
  - task priority;
  - temporary prominence.

**Trạng thái:** giữ mở ở shared-vocabulary level.

---

### 4.7. Label identity vs explanatory annotation

P1.3b từng đề xuất tách hai loại.

P1.3c cho thấy source hiện tại **chưa thực sự encode separation này**.

Kết luận:

- sự phân biệt vẫn có giá trị thiết kế;
- nhưng chưa được promote thành shared semantic role từ source evidence;
- visual exploration có thể test distinction này như hypothesis.

**Trạng thái:** hypothesis / test candidate.

---

## 5. Representative Case A — Graph

### Case definition

Không chọn một style mới.

Dùng một graph representative chứa tối thiểu:

- một curve hoặc hai curve ngang hàng;
- axis;
- auxiliary/projection guide;
- asymptote;
- included/excluded point;
- domain;
- sampling range;
- observation window;
- label;
- discontinuity hoặc branch break nếu có.

### Role test

#### A1 — Object vs guide

Pass nếu:
- curve được đọc như mathematical object;
- axis/auxiliary không cạnh tranh hierarchy;
- asymptote vẫn nhận biết là mathematical reference riêng.

Fail nếu:
- mọi đường đều có cùng visual priority;
- guide trông như data curve;
- asymptote chỉ được phân biệt bằng màu mà mất nghĩa khi grayscale.

#### A2 — Scope

Pass nếu:
- domain không bị suy từ viewport;
- sampling parameter không bị người dùng hiểu thành domain;
- observation window chỉ là framing.

#### A3 — Membership

Pass nếu:
- included/excluded vẫn phân biệt được không phụ thuộc riêng màu.

#### A4 — Label

Pass nếu:
- label xác định được object;
- explanation dài không che graph;
- collision không làm biến semantic role.

### Kết luận case A

R6 đã đủ constraint để visual exploration graph bắt đầu.

Không cần một semantic schema hoàn chỉnh trước khi thử visual alternatives.

---

## 6. Representative Case B — Geometry

### Case definition

Dùng một hình geometry có:

- point/vertex;
- segment/edge;
- visible/hidden edge;
- auxiliary segment;
- label;
- angle/right-angle mark;
- nếu phù hợp: tangency relation;
- surface/fill nếu là 3D.

### Role test

#### B1 — Visibility

Pass nếu:
- hidden edge phân biệt được với visible edge;
- hidden không bị hiểu là “không tồn tại”.

#### B2 — Auxiliary

Pass nếu:
- auxiliary segment hỗ trợ đọc/dựng;
- không cạnh tranh object chính.

#### B3 — Relation marker

Pass nếu:
- right-angle/angle/tangent marker được đọc như relation evidence;
- marker không biến thành decoration.

#### B4 — Label

Pass nếu:
- target attachment rõ;
- mask chỉ giúp readability, không tạo semantic region giả.

### Kết luận case B

Geometry đủ constraint để bước vào visual experiments.

Các relation như parallel/equal-length chưa có ontology chung **không phải blocker** cho visual phase; chúng được giữ open cho case khi thật sự cần.

---

## 7. Representative Case C — Variation

### Case definition

Dùng sample kiểu BBT13 hoặc equivalent có:

- breakpoints;
- intervals;
- derivative sign row;
- increasing/decreasing trend;
- function value at breakpoint;
- excluded point from domain;
- nếu có: zero derivative/local-extremum consistency.

### Role test

#### C1 — Breakpoint vs interval

Pass nếu:
- mốc và khoảng không bị nhập vai.

#### C2 — Sign vs trend

Pass nếu:
- sign row và trend row phân biệt meaning;
- glyph arrow không bị coi là meaning duy nhất.

#### C3 — Excluded point

Pass nếu:
- exclusion được nhận biết như membership/domain status;
- glyph hiện tại có thể thay mà meaning vẫn giữ.

#### C4 — Undefined / limit / discontinuity

Hiện **không yêu cầu pass**, vì source chưa typed các role này đầy đủ.

Kết luận:

- đây là deliberate open gap;
- visual exploration không được tự phát minh một semantic convention mới rồi coi là R6 standard.

### Kết luận case C

Variation đủ constraint cho visual exploration ở các role đã confirmed.

Không đủ để chuẩn hóa limit/undefined/discontinuity ở cấp system; các role đó phải được nghiên cứu khi representative case thật sự yêu cầu.

---

## 8. Representative Case D — Notation / formula context

### Case definition

Một nội dung Toán xuất hiện ở ít nhất hai context:

- inline/prose;
- display/standalone;
- subtitle hoặc compact UI khi phù hợp.

### Role test

Pass nếu:
- semantic identity không đổi khi representation đổi;
- hoa/thường của biến không bị mất;
- raw LaTeX không xuất hiện ở medium không phù hợp;
- công thức phức tạp được chuyển sang display thay vì ép vào prose.

### Kết luận case D

Notation đủ constraint để phối hợp R5 typography và cross-medium visual tests.

---

## 9. Shared semantic candidates sau reconciliation

P1.3d không tạo token, nhưng có thể giữ một **minimal shared set** cho visual work.

### S1 — Mathematical object identity

Một object phải giữ identity khi representation đổi.

### S2 — Mathematical role distinction

Các role khác meaning phải phân biệt được.

### S3 — Membership status

Included/excluded phải được biểu diễn đủ rõ khi relevant.

### S4 — Scope distinction

Domain, sampling range và observation window không được nhập làm một.

### S5 — Mathematical reference vs auxiliary guide

Asymptote/tangent/relation reference không được gộp với generic guide.

### S6 — Projection visibility is contextual

Visible/hidden của geometry là projection state, không phải membership.

### S7 — Label attachment

Nhãn phải liên hệ rõ với object/target.

### S8 — Representation may vary, meaning may not

Medium có thể đổi glyph, color, line style, font, layout hoặc motion mà không đổi semantic meaning.

### S9 — Decoration has no mathematical authority

Frame, background, border, radius, motif, logo và brand marker không được mang mathematical meaning nếu không được định nghĩa rõ.

Đây là **visual constraints candidate**, chưa phải Design Principles.

---

## 10. Những role phải giữ subsystem-specific

Không cố hợp nhất:

### Graph
- asymptote;
- tangent;
- sampling range;
- observation window;
- branch break/discontinuity authoring;
- graph point membership.

### Geometry
- visible/hidden projection;
- constructed points;
- angle/right-angle marks;
- typed tangency relations;
- face/surface.

### Variation
- breakpoint;
- interval;
- derivative sign row;
- variation trend;
- function-value row;
- `excluded_columns`.

Subsystem-specific không phải thất bại của Design System.

Đây là dấu hiệu rằng shared language nên giữ ở **meaning-level**, không ép mọi subsystem dùng cùng một ontology chi tiết.

---

## 11. Những gì vẫn open nhưng không chặn visual work

### O1 — Full geometry relation taxonomy
Parallel, generic perpendicular, equal length, equal angle, incidence.

### O2 — Rich variation semantics
Limit, undefined, discontinuity, critical point, endpoint extremum.

### O3 — Identifier vs explanatory annotation schema
Có giá trị thiết kế nhưng source chưa typed.

### O4 — Exact / approximate
Chưa có direct-source evidence trong scope đã đọc.

### O5 — Diagram / proof-flow vocabulary
Chưa có subsystem đủ mạnh.

### O6 — Motion-semantic mapping
Để R8 xử lý với input từ R6.

### O7 — Accessibility equivalence xuyên medium
Cần test trong visual/cross-medium phase.

Các open items chỉ được mở lại khi:
- một representative case thực tế cần;
- hoặc một downstream program bị blocker.

---

## 12. Visual Readiness Gate

### Câu hỏi 1
R6 đã đủ để ngăn visual work chọn màu/nét/layout làm sai nghĩa Toán chưa?

**Có, ở mức đủ cho experimentation.**

### Câu hỏi 2
R6 đã đủ để tạo semantic token cuối cùng chưa?

**Chưa.**

### Câu hỏi 3
R6 đã đủ để visual designers/tools phân biệt:
- object;
- guide;
- reference;
- membership;
- projection visibility;
- scope;
- annotation;
- decoration?

**Đủ ở mức candidate constraint.**

### Câu hỏi 4
Các open gaps có bắt buộc phải giải quyết trước khi nghiên cứu màu/type/layout không?

**Không.**

### Câu hỏi 5
Có còn lợi ích đủ lớn để tiếp tục semantic deep-read ngay bây giờ không?

**Không thấy.**

---

## 13. Kết luận gate

**R6 đạt Visual Readiness ở mức research candidate.**

Điều này không có nghĩa R6 “hoàn thành tuyệt đối”.

Nó có nghĩa:

- semantic foundation đã đủ để constrain visual exploration;
- các gap còn lại đã được xác định rõ;
- tiếp tục đào sâu semantics lúc này có lợi ích biên thấp;
- nên chuyển sang visual programs và chỉ quay lại R6 khi case thật tạo blocker.

---

## 14. Trạng thái đề xuất

### Tạm chấp nhận ở cấp research constraint
- meaning before implementation;
- role distinction;
- domain/sample/view separation;
- object/reference/guide separation;
- membership distinction;
- projection visibility distinction;
- representation varies, meaning stays;
- decoration has no mathematical authority.

### Giữ subsystem-specific
- graph role details;
- geometry visibility/relations;
- variation row/cell semantics.

### Giữ open
- rich variation semantics;
- geometry relation taxonomy;
- annotation taxonomy;
- exact/approximate;
- diagram/proof-flow vocabulary;
- motion mapping;
- cross-medium accessibility equivalence.

Không có mục nào là `Đã chốt`.

---

## 15. R6 status

Đề xuất ghi:

- P1.3a — complete
- P1.3b — complete
- P1.3c — complete
- P1.3d — complete

R6 — **đủ chín để phục vụ visual work**.

Không tiếp tục P1.3e theo mặc định.

Chỉ mở lại R6 nếu downstream visual/system work xuất hiện blocker semantic thật.

---

## 16. Bước tiếp theo

Sau P1.3d, bước tiếp theo không nên là một semantic report khác.

Cần chuyển sang **Visual Foundation / Visual Exploration**, trong đó R3/R4/R5/R7 được phối hợp bằng cùng một bộ representative specimens.

Mục tiêu của bước tiếp theo phải là:

- bắt đầu nhìn thấy các visual directions của ZO Math;
- nhưng mỗi direction phải truy được về:
  - Brand Foundation;
  - Brand Personality;
  - R6 semantic constraints;
- không chọn logo, màu, font hoặc layout tách rời nhau bằng gu.

Đề xuất bước kế tiếp:

> **P2.0 — Visual Exploration Framework và Specimen Set**

P2.0 chưa chọn phương án cuối.

Nó chỉ:
1. chọn representative specimens;
2. xác định dimensions sẽ thử:
   - color;
   - typography;
   - line/shape;
   - spacing/density;
   - layout/hierarchy;
   - mathematical graphics treatment;
3. xác định acceptance criteria từ R1/R2/R6;
4. chuẩn bị 2–4 visual directions để so sánh ở bước sau.

---

## 17. Điểm kiểm soát mục tiêu dự án

P1.3d được coi là thành công chỉ nếu nó giúp trả lời:

> Chúng ta đã biết đủ về meaning để bắt đầu nhìn thấy ZO Math tương lai mà không làm sai bản chất của ZO Math hay chưa?

Kết luận:

**Có.**

Từ đây, tiếp tục nghiên cứu chỉ có giá trị nếu nó phục vụ visual decision cụ thể.

Đó là điểm dừng của R6 trong pha hiện tại.
