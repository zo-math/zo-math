# P1.3b — Semantic Role Inventory cho ngôn ngữ biểu đạt Toán học

**Dự án:** ZO Math — Hệ thiết kế và ngôn ngữ thương hiệu  
**Phạm vi:** R6 — Ngôn ngữ biểu đạt Toán học  
**Trạng thái:** staging research / semantic inventory candidate  
**Ngày:** 2026-10-05

> P1.3b trích và hợp nhất các vai trò ngữ nghĩa từ những hệ biểu đạt Toán hiện có.
> Không gán màu, font, token hay implementation cụ thể.
> Không coi các role suy ra là canonical nếu nguồn chưa chứng minh trực tiếp.

## 1. Mục tiêu

P1.3b tiếp tục từ baseline P1.3a bằng cách:

1. trích các semantic role đã có dấu vết rõ trong graph, geometry, notation và variation;
2. hợp nhất các role trùng nghĩa ở cấp khái niệm;
3. giữ riêng role subsystem-specific khi cần;
4. phân biệt:
   - mathematical object;
   - state/status;
   - relation;
   - condition;
   - guide/reference;
   - annotation;
   - decoration;
5. ghi rõ provenance và mức bằng chứng của từng role;
6. chưa ánh xạ role sang:
   - màu;
   - font;
   - độ dày nét;
   - token;
   - component;
   - macro/tool cụ thể.

---

## 2. Nguồn

Nguồn trực tiếp:

- `P0_3_ban_do_bang_chung_quyet_dinh_thiet_ke_ZO_Math.md`, cụm D — DES-D-01 → DES-D-10;
- `P0_2_khao_co_thiet_ke_ZO_Math.md`, các mục graph/geometry/variation;
- `Phong_cach_ZO_Math.md`, phần diện mạo, nhấn mạnh, công thức và phụ đề;
- `P1_3a_baseline_ngon_ngu_bieu_dat_Toan_hoc_R6.md`.

Giới hạn quan trọng:

- P1.3b chưa đọc trực tiếp toàn văn từng source production graph/geometry/variation trong repository ở lượt này;
- các role chi tiết chỉ được đưa vào inventory nếu có bằng chứng trong các nguồn tổng hợp đã đọc;
- nơi nguồn chỉ cho biết “có pipeline” mà không mô tả semantics chi tiết sẽ được giữ là gap, không tự suy diễn.

---

## 3. Mô hình role

P1.3b dùng bảy họ role.

### A. Mathematical object
Đối tượng Toán học cần được nhận diện.

### B. State / status
Trạng thái của một đối tượng hoặc quan hệ.

### C. Relation
Quan hệ Toán học giữa các đối tượng.

### D. Condition / scope
Điều kiện, miền hoặc phạm vi áp dụng.

### E. Guide / reference
Yếu tố hỗ trợ đọc, không phải đối tượng toán chính.

### F. Annotation / explanation
Nhãn, chú thích hoặc diễn giải gắn với đối tượng.

### G. Decoration
Yếu tố không mang semantic content Toán học.

Nguyên tắc làm việc:

> role càng gần semantic meaning thì càng nên ổn định xuyên medium; realization càng gần decoration/implementation thì càng có thể thay đổi.

---

# 4. Inventory — Mathematical object roles

## SR-OBJ-01 — Primary mathematical object

**Định nghĩa candidate:**  
Đối tượng Toán học đang là trọng tâm cần đọc, suy luận hoặc kiểm chứng trong một biểu diễn.

Ví dụ theo nguồn hiện có:
- đường cong chính của graph;
- đối tượng hình học được nhấn để theo dõi;
- công thức chính trong vùng công thức.

**Bằng chứng:**  
- graph v0.2 có phân biệt strong/secondary;
- geometry v0.1 có visible/hidden/emphasis;
- `Phong_cach_ZO_Math.md` yêu cầu đường chính rõ, trục nhẹ.

**Mức bằng chứng:** Mạnh cho nhu cầu có phân cấp; tên role hợp nhất là inference của P1.3b.

**Không đồng nghĩa:** “màu đỏ”.

---

## SR-OBJ-02 — Secondary / comparison mathematical object

**Định nghĩa candidate:**  
Đối tượng Toán học cần xuất hiện để so sánh, đối chiếu hoặc làm đối tượng thứ hai, nhưng không phải trọng tâm chính ở thời điểm đó.

**Bằng chứng:**  
- graph v0.2 có role secondary;
- quy tắc nhiều đường cần phân biệt bằng kiểu nét ngoài màu.

**Mức bằng chứng:** Mạnh trong graph; cần kiểm chứng trước khi dùng xuyên geometry/diagram.

---

## SR-OBJ-03 — Coordinate/reference frame

**Định nghĩa candidate:**  
Hệ tham chiếu giúp định vị hoặc đọc đối tượng Toán nhưng không phải nội dung trọng tâm.

Ví dụ:
- trục tọa độ.

**Bằng chứng:**  
- `Phong_cach_ZO_Math.md`: “Trục nhẹ, đường chính rõ”;
- graph guidelines phân biệt axis và main curve.

**Mức bằng chứng:** Mạnh cho graph.

**Ghi chú:**  
Frame không phải decoration; nó có chức năng semantic/measurement nhưng nên có visual priority thấp hơn object chính khi phù hợp.

---

## SR-OBJ-04 — Mathematical point

**Định nghĩa candidate:**  
Điểm có identity Toán học độc lập và có thể mang trạng thái included/excluded hoặc label.

**Bằng chứng:**  
- graph guidelines có điểm đặc/rỗng;
- geometry v0.1 có điểm/nhãn.

**Mức bằng chứng:** Mạnh.

---

## SR-OBJ-05 — Mathematical region / set

**Định nghĩa candidate:**  
Miền hoặc vùng mang ý nghĩa Toán học như tập xác định, vùng thỏa điều kiện hoặc phần được xét.

**Bằng chứng:**  
- graph sources phân biệt domain;
- `Phong_cach_ZO_Math.md` yêu cầu nhãn tập xác định có vị trí riêng.

**Mức bằng chứng:** Mạnh cho domain; các loại region khác cần nghiên cứu thêm.

---

## SR-OBJ-06 — Mathematical expression / formula

**Định nghĩa candidate:**  
Biểu thức hoặc công thức Toán học có identity nội dung riêng, không chỉ là prose.

**Bằng chứng:**  
- nguồn hiện hành phân biệt công thức chính/dàn riêng với biểu thức trong câu;
- yêu cầu giữ đúng chữ hoa/thường của biến.

**Mức bằng chứng:** Mạnh.

**Ghi chú:**  
Inline/display là representation context, không phải hai semantic object khác nhau.

---

# 5. Inventory — State / status roles

## SR-STATE-01 — Included

**Định nghĩa candidate:**  
Đối tượng/điểm thuộc miền hoặc tập đang biểu diễn.

**Bằng chứng:**  
- graph có điểm đặc/rỗng.

**Mức bằng chứng:** Mạnh trong graph.

**Representation hiện có:** điểm đặc là một convention; role semantic là “included”.

---

## SR-STATE-02 — Excluded

**Định nghĩa candidate:**  
Đối tượng/điểm không thuộc miền hoặc tập tại vị trí được biểu diễn.

**Bằng chứng:**  
- graph có điểm đặc/rỗng.

**Mức bằng chứng:** Mạnh trong graph.

**Representation hiện có:** điểm rỗng là convention; role semantic là “excluded”.

---

## SR-STATE-03 — Visible

**Định nghĩa candidate:**  
Phần hình học nhìn thấy trong phép biểu diễn không gian.

**Bằng chứng:**  
- geometry v0.1 có nét thấy.

**Mức bằng chứng:** Mạnh trong geometry.

---

## SR-STATE-04 — Hidden / occluded

**Định nghĩa candidate:**  
Phần hình học bị che khuất nhưng vẫn tồn tại trong cấu trúc.

**Bằng chứng:**  
- geometry v0.1 có nét khuất.

**Mức bằng chứng:** Mạnh trong geometry.

**Representation hiện có:** dashed/line style có thể là convention; semantic role là hidden.

---

## SR-STATE-05 — Emphasized / current focus

**Định nghĩa candidate:**  
Đối tượng đang được chú ý tạm thời hoặc được chọn làm focus trong lập luận.

**Bằng chứng:**  
- geometry v0.1 có nét nhấn;
- `Phong_cach_ZO_Math.md` có “chỉ làm nổi một lần”;
- video/subtitle có moving emphasis.

**Mức bằng chứng:** Mạnh cho sự tồn tại của focus/emphasis; cần phân biệt permanent hierarchy với temporary focus ở bước sau.

---

## SR-STATE-06 — Persistent vs temporary emphasis

**Định nghĩa candidate:**  
Phân biệt semantic hierarchy ổn định với emphasis chỉ xuất hiện ở một thời điểm/cảnh.

**Bằng chứng:**  
- video guideline nói một điểm nhấn di chuyển;
- graph/geometry có role cố định hơn.

**Mức bằng chứng:** Vừa; đây là hợp nhất/inference cần kiểm tra khi nối R6 với R8.

---

# 6. Inventory — Condition / scope roles

## SR-COND-01 — Mathematical domain

**Định nghĩa candidate:**  
Tập giá trị mà đối tượng/hàm/quan hệ được xác định hoặc đang xét.

**Bằng chứng:**  
- graph source phân biệt miền xác định;
- `Phong_cach_ZO_Math.md` nêu nhãn tập xác định.

**Mức bằng chứng:** Mạnh.

---

## SR-COND-02 — Sampling range

**Định nghĩa candidate:**  
Phạm vi kỹ thuật được dùng để lấy mẫu khi dựng graph, không đồng nhất với domain.

**Bằng chứng:**  
- P0.2 ghi graph rules phân biệt miền xác định – lấy mẫu – quan sát.

**Mức bằng chứng:** Mạnh trong graph.

**Điểm quan trọng:**  
Đây là role kỹ thuật có tác động semantic nếu bị nhầm với domain.

---

## SR-COND-03 — Observation window / viewport

**Định nghĩa candidate:**  
Vùng được hiển thị/quan sát, không đồng nhất với domain hoặc sampling range.

**Bằng chứng:**  
- graph rules phân biệt miền xác định – lấy mẫu – quan sát.

**Mức bằng chứng:** Mạnh trong graph.

---

## SR-COND-04 — Mathematical condition / hypothesis

**Định nghĩa candidate:**  
Điều kiện làm thay đổi phạm vi đúng của một kết luận hoặc biểu diễn.

**Bằng chứng:**  
- Brand/voice rules yêu cầu nêu đủ điều kiện của kết luận;
- P1.3a xác định preserve conditions là candidate semantic core.

**Mức bằng chứng:** Vừa ở R6; mạnh ở verbal/math reasoning layer.

**Gap:**  
Chưa có representation convention chung cho condition trong graph/diagram/table.

---

# 7. Inventory — Relation roles

Nguồn hiện đọc cho P1.3b chưa đủ để lập taxonomy relation chi tiết như song song, vuông góc, bằng nhau, ánh xạ, implication, dependency.

Vì vậy không tự tạo một danh mục quan hệ đầy đủ.

Chỉ ghi nhận một role khái quát:

## SR-REL-01 — Mathematical relation

**Định nghĩa candidate:**  
Quan hệ có ý nghĩa Toán học giữa hai hoặc nhiều object.

**Bằng chứng:**  
- R6 Research Map yêu cầu geometry, diagram, hierarchy và relation;
- Brand Personality yêu cầu biểu diễn làm rõ cấu trúc/quan hệ;
- các subsystem hiện có chắc chắn chứa relation nhưng nguồn tổng hợp chưa mô tả đủ taxonomy.

**Mức bằng chứng:** Mạnh cho nhu cầu role khái quát; yếu cho subtype taxonomy.

**Trạng thái:** Cần đọc source trực tiếp trước khi chia subtype.

---

# 8. Inventory — Guide / reference roles

## SR-GUIDE-01 — Axis / scale guide

**Định nghĩa candidate:**  
Yếu tố định vị hoặc đo lường cần thiết nhưng không phải object chính.

**Bằng chứng:**  
- “Trục nhẹ, đường chính rõ”.

**Mức bằng chứng:** Mạnh trong graph.

---

## SR-GUIDE-02 — Construction / auxiliary line

**Định nghĩa candidate:**  
Đường phụ hỗ trợ đọc, dựng, so sánh hoặc kiểm chứng nhưng không phải object toán chính.

**Bằng chứng:**  
- graph sources có đường phụ;
- `Phong_cach_ZO_Math.md` nói nhãn, điểm, trục và đường phụ phải đúng và cần thiết.

**Mức bằng chứng:** Mạnh.

---

## SR-GUIDE-03 — Asymptote / mathematically meaningful reference

**Định nghĩa candidate:**  
Đường tham chiếu có ý nghĩa Toán học riêng, khác với guide thuần thị giác.

**Bằng chứng:**  
- graph guidelines xử lý tiệm cận như một role riêng.

**Mức bằng chứng:** Mạnh.

**Điểm cần giữ:**  
Asymptote không được gộp với generic construction line chỉ vì cùng có thể vẽ bằng nét phụ.

---

## SR-GUIDE-04 — Grid / background guide

**Định nghĩa candidate:**  
Hệ phụ trợ đọc vị trí/tỉ lệ khi cần.

**Bằng chứng:**  
- current implementations có grid/axis neutrals;
- P0.2 ghi grid thay đổi giữa media.

**Mức bằng chứng:** Vừa cho sự tồn tại; yếu cho necessity/semantics.

**Trạng thái:** Chưa đủ để xem grid là role bắt buộc.

---

# 9. Inventory — Annotation roles

## SR-ANN-01 — Identifier label

**Định nghĩa candidate:**  
Tên/kí hiệu trực tiếp của object: điểm, đường, trục, tọa độ, đối tượng.

**Bằng chứng:**  
- geometry có point/label;
- graph có labels;
- `Phong_cach_ZO_Math.md` nêu trong hình chỉ giữ nhãn trực tiếp cần thiết.

**Mức bằng chứng:** Mạnh.

---

## SR-ANN-02 — Mathematical value label

**Định nghĩa candidate:**  
Giá trị số/toạ độ/mốc có chức năng nhận diện hoặc kiểm chứng.

**Bằng chứng:**  
- guideline cảnh báo không dồn số, ngoặc khoảng, dấu đánh dấu và đường phụ vào cùng mốc.

**Mức bằng chứng:** Mạnh cho sự tồn tại; taxonomy chi tiết cần nghiên cứu thêm.

---

## SR-ANN-03 — Explanatory annotation

**Định nghĩa candidate:**  
Chú thích giải thích ý nghĩa, quan hệ hoặc lý do nhưng không phải identity của object.

**Bằng chứng:**  
- guideline tách nhãn trực tiếp trong hình với kết luận/diễn giải dài đặt ngoài hình.

**Mức bằng chứng:** Mạnh.

**Điểm quan trọng:**  
Identifier label và explanatory annotation không nên là cùng một role.

---

## SR-ANN-04 — Conclusion / external explanatory statement

**Định nghĩa candidate:**  
Kết luận hoặc diễn giải dài liên quan tới hình nhưng không nên nằm trong vùng mathematical graphic nếu gây chồng lấn.

**Bằng chứng:**  
- `Phong_cach_ZO_Math.md`: “Kết luận đặt ngoài đồ thị”.

**Mức bằng chứng:** Mạnh trong media guideline; cần kiểm tra áp dụng xuyên web/PDF.

---

# 10. Inventory — Representation-context roles cho notation/formula

Các mục này không phải mathematical semantic roles thuần; chúng là **representation-context roles**.

## RC-MATH-01 — Inline mathematical expression

Dùng trong câu văn, tiêu đề, chú thích, phụ đề khi biểu thức đủ đơn giản để đọc rõ.

**Nguồn hiện hành:** ưu tiên Unicode chính xác.

**Meaning:** giữ semantic identity; đổi representation theo medium.

---

## RC-MATH-02 — Display / standalone formula

Dùng khi công thức là đối tượng chính hoặc quá phức tạp để đặt trong prose.

**Nguồn hiện hành:** dàn công thức hoàn chỉnh bằng LaTeX trong vùng riêng.

---

## RC-MATH-03 — Spoken/subtitle math

Biểu thức trong lời nói/phụ đề cần giữ dễ đọc, không để lộ raw LaTeX.

**Nguồn hiện hành:** Unicode/plain text, giữ hoa/thường của biến.

---

## RC-MATH-04 — Mathematical case fidelity

Chữ hoa/thường của biến là semantic information và không được thay đổi theo typography của lời nói.

**Bằng chứng:** guideline phụ đề ghi rõ giữ nguyên hoa/thường theo ý nghĩa.

**Mức bằng chứng:** Mạnh.

---

# 11. Decoration boundary

## SR-DEC-01 — Decorative element

**Định nghĩa candidate:**  
Yếu tố không mang thông tin Toán học cần thiết cho việc nhận diện, suy luận, kiểm chứng hoặc điều hướng biểu diễn.

Ví dụ có thể gồm:
- motif thương hiệu;
- khung trang trí;
- texture;
- motion không làm rõ meaning.

**Bằng chứng:**  
- dấu nhấn ZO được nguồn hiện hành nói rõ “không dùng như kí hiệu toán học”;
- R1/R2/R6 đều yêu cầu meaning before decoration.

**Mức bằng chứng:** Mạnh cho boundary khái niệm.

---

## SR-DEC-02 — Brand marker

**Định nghĩa candidate:**  
Yếu tố nhận diện thương hiệu có thể hiện diện cùng mathematical content nhưng không được nhập vai semantic.

Ví dụ:
- Dấu nhấn ZO;
- logo.

**Bằng chứng:**  
- guideline nói dấu nhấn không thay logo và không dùng như kí hiệu toán học.

**Mức bằng chứng:** Mạnh.

---

# 12. Vocabulary candidate v0.1

## Mathematical objects
- `object.primary`
- `object.secondary`
- `frame.coordinate`
- `point`
- `region.set`
- `expression`

## States
- `state.included`
- `state.excluded`
- `state.visible`
- `state.hidden`
- `state.focus`
- `state.focus-temporary` *(candidate/inference)*

## Conditions / scope
- `condition.domain`
- `condition.sampling-range`
- `condition.observation-window`
- `condition.hypothesis` *(candidate, needs representation research)*

## Relations
- `relation.mathematical` *(umbrella only; subtype taxonomy not yet supported)*

## Guides / references
- `guide.axis`
- `guide.auxiliary`
- `reference.asymptote`
- `guide.grid` *(weak/conditional)*

## Annotation
- `annotation.identifier`
- `annotation.value`
- `annotation.explanatory`
- `annotation.conclusion-external`

## Representation context
- `math.inline`
- `math.display`
- `math.subtitle`
- `math.case-sensitive`

## Decoration boundary
- `decoration.generic`
- `brand.marker`

Các tên trên là **candidate vocabulary**, không phải token API.

---

# 13. Role nào đã có bằng chứng mạnh nhất?

### Nhóm mạnh
- primary vs secondary/focus hierarchy;
- axis/frame;
- point;
- included vs excluded;
- visible vs hidden;
- domain;
- sampling range;
- observation window;
- asymptote;
- auxiliary line;
- identifier label;
- explanatory annotation;
- inline vs display math;
- case fidelity;
- decoration ≠ mathematical symbol.

### Nhóm vừa
- temporary vs persistent focus;
- general mathematical condition/hypothesis;
- value-label subtype;
- grid role.

### Nhóm chưa đủ
- relation subtype taxonomy;
- detailed variation semantics;
- data-table roles;
- diagram node/edge roles;
- proof/reasoning flow roles;
- motion-semantic roles;
- exact/approximate status as a source-backed shared role;
- variation critical-point/increase/decrease/extremum roles.

Không tự bổ sung các mục “chưa đủ” chỉ vì chúng quen thuộc trong Toán.

---

# 14. Variation — deliberate gap

Nguồn tổng hợp hiện xác nhận:

- variation v0.1 có một nguồn JSON;
- có output theo medium;
- có phần tử bảng ngữ nghĩa;
- semantic HTML vẫn chưa hoàn tất.

Nhưng P1.3b chưa có đủ text nguồn để xác nhận taxonomy chi tiết của variation.

Vì vậy chưa tạo các role như:

- increasing;
- decreasing;
- local maximum;
- local minimum;
- limit;
- discontinuity;
- derivative sign.

Đây là **gap có chủ đích**, không phải thiếu sót vô tình.

Bước tiếp theo cần đọc trực tiếp specification/data model của variation trước khi thêm role.

---

# 15. Geometry — deliberate gap

Geometry v0.1 hiện đủ để xác nhận:

- point;
- label;
- visible;
- hidden;
- emphasized;
- fill/mask như implementation/representation support.

Nhưng chưa đủ để tạo taxonomy quan hệ như:

- parallel;
- perpendicular;
- equal length;
- equal angle;
- incidence;
- tangent;
- congruent;
- similar.

Cần đọc trực tiếp geometry schema/spec trước khi tạo subtype.

---

# 16. Graph — role consolidation

Graph hiện là subsystem giàu semantic evidence nhất.

Có thể tách:

### Object
- main curve/object;
- secondary comparison curve;
- point.

### Frame/reference
- axes;
- asymptote;
- auxiliary line.

### State
- included/excluded.

### Scope
- domain;
- sampling range;
- observation window.

### Annotation
- identifier/value/explanatory label.

### Representation
- line style;
- point fill;
- relative emphasis.

Điểm quan trọng:

> màu hiện tại là realization, không phải identity của role.

---

# 17. Cross-subsystem shared candidates

Các role có khả năng shared cao:

1. `object.primary`
2. `object.secondary`
3. `state.focus`
4. `annotation.identifier`
5. `annotation.explanatory`
6. `condition.domain/scope` ở mức khái quát
7. `guide.auxiliary`
8. `decoration.generic`
9. `brand.marker`

Các role có khả năng subsystem-specific cao:

- asymptote;
- sampling range;
- observation window;
- visible/hidden geometry;
- included/excluded endpoint;
- variation-specific states.

Không ép role subsystem-specific vào một vocabulary quá trừu tượng nếu việc hợp nhất làm mất meaning.

---

# 18. Semantic vs representation mapping — ví dụ

| Semantic role | Representation hiện có | Trạng thái mapping |
|---|---|---|
| state.included | điểm đặc | mạnh trong graph |
| state.excluded | điểm rỗng | mạnh trong graph |
| state.hidden | nét khuất | mạnh trong geometry |
| reference.asymptote | line style phụ | mạnh về role, realization cần đọc sâu |
| object.primary | strong visual treatment | mạnh về hierarchy, màu cụ thể không canonical |
| object.secondary | secondary treatment / alternate line style | mạnh trong graph |
| guide.axis | trục nhẹ | mạnh |
| annotation.identifier | label gần object | mạnh |
| annotation.explanatory | đặt tách khỏi graphic khi dài | mạnh |
| math.inline | Unicode trong prose/subtitle | mạnh trong media guideline |
| math.display | vùng công thức dàn riêng | mạnh |
| brand.marker | motif/logo, không dùng như kí hiệu toán | mạnh |

Bảng này chưa phải token map.

---

# 19. Constraint từ Brand Personality lên role system

## Gần gũi trong tôn trọng
- role naming phải dễ hiểu với người sản xuất;
- output không “nói xuống” người học bằng icon hóa quá mức;
- annotation giải thích phải tôn trọng khả năng suy luận.

## Sống động nhưng điềm tĩnh
- temporary focus có thể thay đổi theo thời gian;
- không nhiều role cùng ở trạng thái strong/focus.

## Giản dị mà sâu sắc
- mỗi mark nên gánh một role rõ;
- tránh nhiều encoding trùng nghĩa;
- không bỏ role toán chỉ để hình sạch.

## Rõ ràng và trong sáng
- role khác meaning phải phân biệt được;
- semantics không phụ thuộc riêng màu;
- annotation phải tách identity khỏi explanation khi cần.

---

# 20. Những gì không được hợp nhất

P1.3b xác định một số “mâu thuẫn giả” cần tránh:

### Không gộp domain với viewport
Một graph có thể chỉ hiển thị một phần domain.

### Không gộp sampling range với domain
Sampling là yêu cầu dựng; domain là meaning Toán.

### Không gộp asymptote với generic guide
Asymptote mang ý nghĩa Toán riêng.

### Không gộp identifier label với explanation
Một cái gọi tên; một cái giải thích.

### Không gộp brand marker với annotation
Motif/logo không được mang semantic Toán.

### Không gộp focus với primary identity
Một object có thể là primary lâu dài hoặc chỉ được focus tạm thời.

### Không gộp color token với semantic role
Màu là một kênh realization có thể thay đổi.

---

# 21. Gap list sau inventory

## GAP-R6-01 — Variation semantic schema
Cần đọc trực tiếp variation v0.1.

## GAP-R6-02 — Geometry relation schema
Cần đọc trực tiếp geometry v0.1/schema.

## GAP-R6-03 — Diagram vocabulary
Chưa có system source đủ mạnh.

## GAP-R6-04 — Data-table semantics
Chưa có role model chung.

## GAP-R6-05 — Proof/reasoning-flow semantics
Chưa có vocabulary cho giả thiết, bước suy luận, kết luận, counterexample, dependency.

## GAP-R6-06 — Exact vs approximate
P1.3a đặt như hypothesis nhưng P1.3b chưa có source trực tiếp đủ mạnh để promote.

## GAP-R6-07 — Motion semantic mapping
Cần nối R6 với R8 sau này.

## GAP-R6-08 — Accessibility representation route
Cần role → non-color cue → text/semantic equivalent.

---

# 22. RQ được cập nhật

### RQ-DS-R6-001
Các shared semantic role nào đủ mạnh để trở thành vocabulary chung?

**Hiện tại:** có candidate list, nhưng variation/geometry relation/diagram còn thiếu.

### RQ-DS-R6-002
Representation rule nào shared, rule nào subsystem-specific?

**Hiện tại:** point fill, line style, light axis là bằng chứng cục bộ mạnh; chưa đủ để universalize.

### RQ-DS-R6-003
Phân biệt mathematical data, guide và decoration thế nào?

**Hiện tại:** boundary đã rõ hơn:
- object/relation/condition = mathematical semantics;
- guide/reference = hỗ trợ đọc nhưng có thể mang meaning;
- decoration/brand marker = không mang mathematical semantics.

---

# 23. Readiness

P1.3b đã tạo được vocabulary candidate đủ để làm bước tiếp theo, nhưng chưa đủ để tạo Design Principle hoặc semantic token.

Điểm mạnh:

- role graph khá rõ;
- geometry có state roles rõ;
- notation có context roles rõ;
- boundary decoration rõ.

Điểm yếu:

- variation chưa đọc trực tiếp;
- relation taxonomy chưa đủ;
- diagram/data table/proof flow còn thiếu.

---

# 24. Bước tiếp theo đề xuất

**P1.3c — Deep source read cho các gap semantic còn thiếu**

Scope hẹp:

1. đọc trực tiếp specification/schema của:
   - variation v0.1;
   - geometry v0.1;
   - graph v0.2 nếu cần đối chiếu role naming;
2. trích role chi tiết mà không suy từ kiến thức Toán chung;
3. bổ sung:
   - variation roles;
   - geometry relation roles;
   - graph role mapping;
4. chưa nghiên cứu diagram/data table rộng nếu repository chưa có source tương ứng;
5. cập nhật Semantic Role Inventory v0.2.

Không cần external research ở P1.3c.

---

# 25. Kết luận

P1.3b cho thấy một semantic vocabulary chung bắt đầu hình thành, nhưng không nên được thiết kế bằng cách “đặt tên token trước”.

Hướng đúng là:

> semantic meaning → role → representation candidate → medium adaptation → implementation/token.

Inventory hiện tại đủ để giữ ranh giới quan trọng nhất:

- mathematical object khác guide;
- guide khác decoration;
- label identity khác explanation;
- domain khác sampling/view;
- role khác color;
- brand marker khác kí hiệu Toán.

P1.3b dừng tại vocabulary candidate v0.1.
