# P1.3c — Deep source read: Semantic roles của R6

**Ngày đọc:** 2026-10-05  
**Trạng thái:** staging research; inventory evidence v0.2, không phải semantic token, Design Principle, Decision hay specification mới.  
**Phạm vi:** đọc source graph v0.2, geometry v0.1 và variation tool hiện hành; chỉ khảo sát semantic roles, representation convention và implementation mapping.

## 1. Mục tiêu và phạm vi

P1.3c đọc trực tiếp tài liệu quy chuẩn, README, style, compiler/integration và dữ liệu mẫu để xác định subsystem thực sự phân biệt những semantic roles nào. Trọng tâm là variation, geometry, và đối chiếu graph. Không thiết kế lại subsystem, chọn visual direction, nghiên cứu external, render hoặc sửa source.

Thứ tự phân tích được giữ là:

> semantic meaning → role → representation → medium adaptation → implementation

Mỗi phát hiện được xếp vào một trong ba trạng thái:

- **Confirmed from direct source:** có tên/trường/điều kiện trực tiếp trong source hoặc quy chuẩn được giao đọc.
- **Consolidated inference:** tổng hợp hợp lý xuyên subsystem nhưng chưa được source nào định nghĩa như role dùng chung.
- **Still open:** chưa có bằng chứng trực tiếp đủ để xác nhận.

“Confirmed” chỉ nghĩa source hiện hành phân biệt hoặc mô tả role đó; không có nghĩa role đã được chọn làm semantic token hay chuẩn Design System.

## 2. Source đã đọc và provenance

### Baseline nội bộ

- [P1.3a — Baseline nội bộ cho R6](../P1_1_R1/P1_3a_baseline_ngon_ngu_bieu_dat_Toan_hoc_R6.md), đặc biệt mục 4.2–4.4, 5–6, 10–12, 16–20. Đây là baseline/hypothesis để đối chiếu, không phải source production.
- Không tìm thấy báo cáo/tệp P1.3b trong `_audit/zo_design_system` theo mẫu `P1_3b*`. Vì vậy P1.3c không gán cho P1.3b bất kỳ claim nào không có trong baseline hoặc yêu cầu hiện tại; các nhãn “P1.3a/b” dưới đây chỉ đối chiếu những giả thuyết/candidate đã có thể xác định.

### Graph — 4 source subsystem

1. [Quy chuẩn sản xuất đồ thị hàm số ZO Math v0.2](../../../../quy_trinh_xay_dung/quy_chuan_san_xuat_do_thi_ham_so_zo_math_v0.2.md), mục 1–5, 7–8, 10–11 và ví dụ đặc tả. Đây là quy chuẩn production cho sản phẩm graph mới; tài liệu tự nêu không tự áp dụng hồi tố.
2. [README bộ công cụ đồ thị](../../../../quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/README.md), mục 1–5.
3. [zo_graph_v02.tex](../../../../quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/tex/zo_graph_v02.tex), các style axis, curve, tangent, asymptote, auxiliary, point, point emphasized, point open, protected label và layer.
4. [zo_graph_build.py](../../../../quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/zo_graph_build.py), phần validate/build. Script kiểm tra nguồn `.tex` trong repository rồi chạy LuaLaTeX/PDF→SVG; không có parser/schema graph có cấu trúc để chuẩn hóa semantic role.

### Geometry — 3 source subsystem

1. [Quy chuẩn sản xuất hình học ZO Math v0.1](../../../../quy_trinh_xay_dung/quy_chuan_san_xuat_hinh_hoc_zo_math_v0.1.md), mục 1–5.
2. [zo-geometry-styles.tex](../../../../assets/tex/zo-geometry-styles.tex), toàn bộ style v0.1.
3. [zo_geometry.py](../../../../scripts/zo_geometry.py), đặc biệt `validate_common`, `validate_2d`, `validate_relations_2d`, `auto_face_visibility`, `validate_3d`, `style_for`, `render_2d`, `render_3d` và các renderer khối cong.

Compiler chứa hợp đồng YAML thực thi; không tìm thấy JSON Schema hoặc YAML schema riêng, cũng không tìm thấy source YAML chính thức trong các đường dẫn được khảo sát. Không dùng receipt `.geometry.json` như schema hay fixture đầu vào.

### Variation — 6 source subsystem

1. [README bộ công cụ bảng biến thiên](../../../../quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/README.md).
2. [zo_variation_build.py](../../../../quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/zo_variation_build.py), đặc biệt `validate_record`, `point_key`, `math_token`, `make_tex`, `build_one`.
3. [zo_variation_v01.tex](../../../../quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/tex/zo_variation_v01.tex).
4. [zo_variation_qmd.lua](../../../../assets/lua/zo_variation_qmd.lua), loader, SVG/PDF embedding và hidden HTML table.
5. [zo_variation.css](../../../../assets/css/zo_variation.css).
6. [bang_bien_thien.json của học liệu R1-G01](../../../../content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/du_lieu/bang_bien_thien.json), một consumer data sample có hàng đạo hàm/biến thiên và `excluded_columns`. Đọc mẫu này chỉ để xác định biểu diễn input/output thực tế; không đồng nhất R1-G01 với Research Program R6.

Thư mục tool không có file schema JSON hoặc fixture JSON độc lập. Hợp đồng chính thức hiện nằm trong README và validator; consumer JSON trên là bằng chứng về một cách dùng thực tế, không thay thế hợp đồng.

**Số lượng:** 13 source trực tiếp thuộc ba subsystem (graph 4, geometry 3, variation 6), cộng 1 baseline nội bộ P1.3a. Các quy tắc repository/AGENTS được đọc riêng, không tính là evidence subsystem.

## 3. Graph — direct-source findings

### Semantic roles source phân biệt

- Quy chuẩn v0.2 phân cấp theo nhiệm vụ: đường cong chính thường nổi bật; trục định hướng; đường phụ cung cấp căn cứ; nhãn giải thích; khung tổ chức không gian. Khi so sánh hai hàm ngang hàng, hai đường cong phải cùng mức ưu tiên. Do đó “primary” không phải thuộc tính bất biến của mọi đường cong: vai trò có thể thay đổi theo câu hỏi/hình.
- README và TeX style gọi riêng `curve`, `tangent`, `asymptote`, `auxiliary`, `point`, `point emphasized`, `point open`, `axis`, `label`. README gán `auxiliary` cho đường chiếu hoặc tham chiếu phụ; không đồng nhất tên này với `asymptote` hay `tangent`.
- Quy chuẩn định nghĩa rõ **tập xác định**, **miền lấy mẫu** và **miền quan sát** là ba thứ khác nhau. README triển khai tương ứng bằng thông tin `domain`/`samples` và các giới hạn `xmin`, `xmax`, `ymin`, `ymax`.
- Quy chuẩn phân biệt điểm đặc/rỗng và đầu mút theo quan hệ thuộc tập/giá trị hàm; README đưa tọa độ điểm vào nguồn và TeX style có `point`/`point open`. Đây là bằng chứng trực tiếp về ý nghĩa điểm và status trong graph, nhưng kiểu marker rỗng là cách biểu diễn hiện tại, không phải quy tắc bắt buộc của mọi medium.
- Quy chuẩn yêu cầu tách nhánh tại gián đoạn/tiệm cận, không nối qua điểm loại. Tuy vậy đây là yêu cầu cho người viết nguồn; graph build script không phân tích continuity hoặc tự phát hiện điểm loại.
- Quy chuẩn coi miền tô là nội dung cần dựng đúng biên và kiểm tra; style có highlight colors, nhưng màu không định nghĩa semantic của miền.
- Nhãn trực tiếp và legend được hỗ trợ. Source yêu cầu `alt`, caption và nội dung thay thế ở tài liệu; không có field schema phân biệt label nhận diện object với annotation giải thích.

### Representation hiện tại và mức bắt buộc

| Role trong source | Representation hiện tại | Phân loại bằng chứng |
|---|---|---|
| Curve chính / curve ngang hàng | `curve solid/dashed/dashdot`; các curve dùng đỏ `#EF5350`. Nét dựa thứ tự cho các đường ngang hàng. | Meaning “chính”/“ngang hàng” là phân cấp theo mục tiêu; màu/nét là convention v0.2. |
| Axis | PGFPlots axis style, hai chiều mũi tên theo style hiện có. | Axis là role; hình thức và thông số cụ thể là convention. |
| Tangent / asymptote / auxiliary guide | Ba style riêng `zo graph v02 tangent`, `... asymptote`, `... auxiliary`. | Vai trò được gọi tên tách biệt; dash, màu, width là convention. Asymptote phải dựa phân tích giới hạn, tangent phải qua điểm tiếp xúc theo quy chuẩn. |
| Point / emphasized point / open point | Filled marker thường, marker nhấn, marker rỗng. | Role/status điểm được phân biệt; marker, kích thước, màu là realization. |
| Domain / sampling / observation | Công thức/nhánh, `domain`/`samples`, và trục `xmin...ymax`. | Ba khái niệm được quy chuẩn tách; cú pháp cụ thể không phải common semantic schema. |
| Branch break / discontinuity | Tách các lệnh vẽ hoặc dải dữ liệu; không nối qua điểm loại. | Bất biến toán học trong source graph; hiện dựa vào khai báo/kiểm tra của tác giả. |
| Label / legend | Node label hoặc legend; PDF/SVG có thể không chứa văn bản truy cập được, bù bằng học liệu. | Chức năng định danh/giải thích được ghi trong guidance; chưa có loại annotation có cấu trúc. |
| Mathematical filled region | Dựng biên rồi tô, kiểm tra miền tô. | Role miền là nội dung toán; fill color/pattern là representation. |

### Giới hạn runtime

Graph v0.2 có bộ quy chuẩn vai trò phong phú hơn runtime model: bộ dựng nhận `.tex` trực tiếp và sinh PDF/SVG, không nhận một schema semantic typed. Vì vậy “role được quy chuẩn gọi tên” không đồng nghĩa “role được compiler kiểm tra”. Không thấy runtime field riêng cho primary/secondary, domain status, included/excluded hay annotation kind.

## 4. Geometry — direct-source findings

### Object types và vai trò

- Compiler nhận `dimension: 2d|3d`, `points`, `objects`, `labels`; điểm có `id` và tọa độ hoặc phép dựng. Các loại object 2D được renderer gọi trực tiếp gồm circle, polygon, segment, ellipse, parabola, hyperbola và hai marker `right_angle_mark`/`angle_mark`.
- Hình 3D dùng `vertices`, `edges`, `faces`, `segments`; compiler có prototype cho cylinder, cone, frustum, sphere, convex box và convex polyhedron. Đây là các loại object/hình học triển khai, không phải taxonomy đã thống nhất toàn R6.
- `projection` và `circumcenter` là hai kiểu construction point 2D compiler hỗ trợ. Các điểm tạo bởi section có `point_ids`.
- `segment`/`edge` có endpoints. Không có object type tổng quát `line` hoặc `ray` được khai báo ở compiler v0.1; vì thế không gán cho nguồn này một taxonomy line/ray.

### Visibility, emphasis, auxiliary, fill/mask

- `visible` và `hidden` là state được nhận dạng cho cạnh 3D; `auto` được suy từ mặt trước/sau theo camera, có override kèm lý do. Trong geometry, đây là **trạng thái che khuất theo phép chiếu**, không phải thuộc/không thuộc tập điểm hay việc object có tồn tại về mặt toán học.
- `emphasized` là flag để chọn style main/main-hidden. Nó điều khiển độ nổi bật thị giác, không tự nó xác nhận một semantic role toán riêng hoặc “primary object” dùng chung với graph.
- `auxiliary` được map thành style nét phụ cho `segments`; khi thiếu `role`, renderer 3D mặc định segment về auxiliary. Đây là bằng chứng implementation cho segment phụ, nhưng không chứng minh mọi construction line hoặc relation trong hình học đều auxiliary theo một ontology chung.
- `faces` có thể bật `render`; các mặt được `fill` bằng `zo geometry surface`. Đây là mặt hình học được tô; fill style chỉ là cách dựng.
- `labels` có `target`, `text`, `anchor`, `mask` với `mask` là `none|when_required`. “Masked” áp lên nền label để đọc rõ, không phải mathematical region/mask. Schema không phân biệt label định danh với explanatory annotation.

### Relations và relation markers

- `relations` 2D có bốn loại kiểm tra tường minh: `circle_tangent`, `ellipse_tangent`, `parabola_tangent`, `hyperbola_tangent`; compiler kiểm residual hình học trong tolerance. Tangency vì vậy có bằng chứng trực tiếp ở relation/check layer.
- `right_angle_mark` và `angle_mark` tạo ký hiệu góc. Right-angle mark có thể thể hiện góc vuông tại cấu hình chỉ định; source không cung cấp catalog quan hệ line-line tổng quát.
- References từ label, endpoint, face, section và point cung cấp incidence/topology ở dạng liên kết ID. Nhưng không có `incidence` như một relation type độc lập với kiểm tra hình học tổng quát.
- Không thấy relation type hoặc checker tổng quát cho parallel, perpendicular, equal length, equal angle. Right-angle marker không được mở rộng thành taxonomy `perpendicular`; angle marker không tự biểu thị equality.

### Representation hiện tại

| Role/state | Representation hiện tại | Semantic bắt buộc hay convention? |
|---|---|---|
| Point/vertex, segment/edge, face/surface, conic/solid | YAML references → TikZ/tkz-euclide/tikz-3dplot primitives | Object identity/type là dữ liệu; primitive và bố trí là implementation. |
| Visible/hidden edge | Visible nét liền trung tính; hidden nét đứt xám; mặt khuất dựng trước | Trạng thái visibility có ý nghĩa projection; dash/color/order là convention. |
| Emphasized / auxiliary | Main red style hoặc nét auxiliary; `emphasized` boolean và `role` trên segment | Source xác nhận flag/role hiện dùng; đỏ, width, dash không phải semantic. |
| Angle/right-angle marker | Arc/marker, right angle mark, không fill nền | Loại mark được source phân biệt; size/màu/nét là convention. |
| Label và mask | Target + text + anchor; nền mask cục bộ khi cần | Target attachment có cấu trúc; mask chỉ là xử lý readability. |
| Surface | Face `render` được fill bằng style surface | Mặt là object; fill và màu là cách thể hiện. |

## 5. Variation — direct-source findings

**Path thực tế của subsystem:** `quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/`. README ở folder này chỉ rõ tool builder, TeX template và hai adapter dùng chung tại `assets/lua/zo_variation_qmd.lua`, `assets/css/zo_variation.css`. Không suy ra tên/path từ subsystem khác.

### Data contract hiện có

- Một JSON record yêu cầu `id`, `title`, `rows`; có hai hoặc ba hàng. Hàng đầu chứa mốc xen kẽ với ô khoảng trống; số cột chẵn, đồng nhất, tối thiểu bốn. Đây là cấu trúc bảng/cell-position, chưa phải các trường role typed.
- Khi có ba hàng, validator hiểu hàng thứ hai là đạo hàm và hàng thứ ba là biến thiên; README cho phép có hàng dấu đạo hàm và hàng biến thiên, hoặc chỉ một trong hai. Mốc hàng đầu được sắp theo thứ tự số; parser hỗ trợ ±∞ trong mốc.
- `excluded_columns` là field trực tiếp đánh dấu điểm bị loại khỏi miền. Chỉ số cột tính từ 0 trong JSON; compiler đổi các ô dưới tiêu đề tại cột đó thành glyph `∥`. Đây là role/status data rõ nhất trong variation schema hiện tại.
- Các cell còn lại là chuỗi tự do. Compiler map một số token toán học `−∞`, `+∞`, `+`, `−`, `0`, `↗`, `↘`, `→`, `∥` sang TeX; không có enum/field riêng `limit`, `undefined`, `endpoint`, `critical_point`, `local_maximum` hoặc `local_minimum`.
- Validator chỉ kiểm dấu/chiều cho ba-row table ở các cột interval: `+` → `↗`, `−` → `↘`, `0` → `→`; và có hai kiểm tra đặc thù: `+` qua `0` sang `−` yêu cầu ô value tại mốc; `−` qua `0` sang `+` cũng yêu cầu value. Đây là check hẹp cho mẫu cực đại/cực tiểu theo dấu đạo hàm, không phải bộ phân loại critical points tổng quát.
- Sample consumer BBT13 ghi `Không xác định` tại hàng đạo hàm/giá trị ở `x=0`, đồng thời khai `excluded_columns: [3]`. Do generator/Lua thay cell ở cột excluded dưới hàng mốc bằng `∥`, literal “Không xác định” trong những cell này không còn là token output. Data source chứng minh điểm bị loại khỏi miền; không chứng minh `∥` là biểu diễn phổ quát của undefined/discontinuity.
- Không có field tách tập xác định khỏi sample range/observation window trong variation JSON contract; cũng không có khái niệm lấy mẫu đường cong.

### Role và representation trong variation

| Role thật sự có evidence | Meaning trong source | Representation hiện tại | Semantic bắt buộc hay convention? | Mức evidence |
|---|---|---|---|---|
| Abscissa/mốc phân hoạch | Hàng đầu chứa các mốc theo thứ tự; gồm mốc hữu hạn hoặc ±∞ | Hàng đầu, các cột lẻ trong mảng dữ liệu; xen kẽ với cột interval | Mốc là nội dung dữ liệu; cột xen kẽ là cấu trúc representation | Trực tiếp: README, `validate_record`, `point_key`. |
| Interval | Ô xen giữa hai mốc trên trục x | Cột xen kẽ; các cell cùng cột mang sign/trend/value | Ý nghĩa khoảng có trong hướng dẫn cấu trúc; cột không bắt buộc xuyên medium | Trực tiếp nhưng không có cell type riêng. |
| Derivative/sign | Hàng 2 trong record ba hàng; token sign `+`, `−`, `0` được validator dùng | Hàng dấu đạo hàm `f′(x)` (hoặc tên hàm tương tự) | Nội dung dấu mang nghĩa; nhãn hàng tự do và index hàng là convention/schema positional | Trực tiếp, chỉ khi record ba hàng và tuân theo layout hiện tại. |
| Function value | Hàng biến thiên chứa giá trị ở các mốc, bao gồm value cần cho hai mẫu chuyển dấu qua 0 | Cell tại cột mốc trong hàng cuối | Giá trị là dữ liệu; không có typed `value_at_critical_point` riêng | Trực tiếp nhưng phụ thuộc cell position. |
| Increasing | Chiều ứng với dấu dương khi validator kiểm mối quan hệ derivative/trend | `↗` hoặc token có `↗` | Meaning toán được ghi; glyph là convention hiện tại | Trực tiếp, validator chỉ kiểm partial pattern. |
| Decreasing | Chiều ứng với dấu âm | `↘` hoặc token có `↘` | Meaning toán được ghi; glyph là convention hiện tại | Trực tiếp, validator chỉ kiểm partial pattern. |
| Constant trend | Mapping `0` → `→` trong sign/trend validation | Mũi tên ngang | Mapping hiện thực có trong compiler; không đủ để tuyên bố mọi zero derivative là constant trên lân cận | Trực tiếp ở mức mapping/implementation hẹp. |
| Local-extremum consistency check | Dấu `+ 0 −` hoặc `− 0 +` phải có function value ở cột mốc | Mốc chứa `0` và giá trị hàng biến thiên; không có label max/min bắt buộc | Logic kiểm định của compiler, không phải taxonomy đầy đủ hoặc role type | Trực tiếp cho hai pattern này. |
| Excluded point from domain | Điểm bị loại khỏi miền tại cột mốc | `excluded_columns`; cell dưới mốc hiện được thay bằng `∥` | Field loại trừ là semantic data; glyph thay thế là representation convention | Trực tiếp; README, compiler, Lua và sample BBT13. |

### Accessibility/medium note

Lua integration chọn SVG/PDF theo output; với HTML nó thêm hidden HTML `<table>` có `<caption>`, header cell (`scope="col"`) và row header (`scope="row"`). Điều này thu hẹp gap “không có semantic HTML” của baseline P1.3a. Tuy nhiên các row semantics phần lớn vẫn đến từ chuỗi cell/nhãn tự do; image `alt` mặc định chỉ gồm title và ID, và CSS riêng chỉ định bố cục hình/caption/image. Chưa có markup role-level riêng cho derivative sign, interval, extremum, limit hoặc excluded status ngoài HTML table headers và nội dung cell.

## 6. Semantic roles được xác nhận

Source trực tiếp xác nhận một số semantic role ở cấp subsystem:

- **Graph:** function curve và peer/comparison curve; axis; tangent; asymptote; auxiliary/projection/reference guide; point; included/excluded point status; domain; sampling interval; observation window; discontinuity/branch break; object label/legend; filled mathematical region.
- **Geometry:** point/vertex; segment/edge; face/surface; supported 2D and 3D geometric object families; visible/hidden projection state; auxiliary segment; constructed point; angle/right-angle mark; four typed tangent relations; dimension annotation; label attached to target.
- **Variation:** abscissa/breakpoint; interval; derivative-sign row; function-value row; increasing/decreasing/constant trend; excluded-domain point. Ngoài các role families này, compiler còn kiểm tra hai mẫu dấu quanh điểm `0` để yêu cầu function value cho local extremum; đây là consistency check, không phải role type riêng.

Các role trên chưa ngang độ mạnh: có role được semantic meaning nêu rõ trong quy chuẩn, có role chỉ được xác nhận bởi field/compiler mapping hoặc cell position. Bảng có mã hóa từng role ở mục 12 để tránh biến implementation detail thành semantic claim.

## 7. Consolidated roles / inference

Các mục dưới đây là suy luận tổng hợp, không phải taxonomy được source hiện hành tuyên bố:

1. **Object / reference / guide** có thể là nhóm vocabulary hữu ích xuyên graph và geometry; nhưng graph phân biệt curve, tangent, asymptote, auxiliary, còn geometry dùng object type, segment role và visibility. Không thể gộp tất cả thành một vai trò “secondary”.
2. **Included/excluded** có thể là một khái niệm quan hệ tập dùng chung giữa graph và variation: graph có endpoint/point status; variation có `excluded_columns`. Geometry point `draw: false` chỉ ẩn marker khi render, không tương đương point excluded khỏi tập hình học.
3. **Visible/hidden** chỉ có thể được hợp nhất sau khi nêu domain: geometry dùng front/back occlusion theo camera; graph open point là membership/endpoint convention; một đối tượng toán học có thể bị che trong hình mà vẫn tồn tại. Đây không phải một cặp state duy nhất xuyên subsystem.
4. **Domain / sampling / observation** là bộ phân biệt có thể dùng làm vocabulary R6 vì graph v0.2 định nghĩa rõ ba khái niệm. Chưa có source variation/geometry biểu diễn bộ ba này.
5. **Variation row/cell semantics** có thể mô hình hóa theo interval cells và breakpoint cells, nhưng source hiện thực dùng index trong mảng và text value; bất kỳ schema role chuẩn hóa nào cũng sẽ là thiết kế mới.
6. **Label/annotation** có thể cần lớp attachment và lớp explanatory content riêng; source hiện tại chỉ có generic label/target/text/anchor, row labels và legend. Không có evidence rằng các subsystem đã phân loại identifier label và explanation annotation đồng nhất.
7. **Emphasis/primary** là hai khái niệm khác nhau: graph ưu tiên curve theo mục tiêu và có thể coi hai curve là đồng hạng; geometry có boolean `emphasized` để chọn style. Không được map boolean đó trực tiếp thành “primary mathematical object”.
8. **Semantic roles trước visual encoding** phù hợp với cách đọc source: role thường được nêu bằng field/tên style/ý nghĩa rồi mới map sang glyph, color hoặc nét. Đây là tổng hợp để tiếp tục nghiên cứu R6, chưa phải Principle.

## 8. Representation conventions, không phải semantics

- Graph curve đỏ `#EF5350`, solid/dashed/dashdot theo thứ tự, độ dày và marker size.
- Graph point open được biểu diễn bằng marker vòng rỗng; marker emphasized lớn/đậm hơn.
- Graph tangent/asymptote/auxiliary dùng nét và màu trung tính/dash khác nhau; các nét này mã hóa vai trò nhưng bản thân dash pattern không phải định nghĩa toán học của role.
- Graph area dùng fill/highlight; frame/background/rounded corners không phải mathematical region.
- Geometry visible/hidden styles là nét liền/nét đứt và xám; main là đỏ; `zoGeometrySurface` là fill; label mask là nền trắng cục bộ.
- Geometry right-angle/angle marker có stroke và size cụ thể; style `fill=none` là quy ước thị giác.
- Variation `↗`, `↘`, `→`, `∥`, cách xen kẽ cột và ma trận các hàng là realization hiện có. Glyph có thể được chuyển sang TeX/math mode hoặc HTML cell; không được nhầm glyph hiện tại với requirement bất biến của mọi medium.
- Variation border, nền, accent, minimum cell width, CSS max height/width, margin, font và spacing là representation/visual convention.
- Không có căn cứ để lấy các màu hiện hành hay `main`/`accent` style đặt tên rồi gán ngược thành semantic definition. Đặc biệt màu đỏ curve/main và màu accent của bảng không có nghĩa “tăng”, “giảm”, “đúng”, “sai” hoặc một quan hệ hình học.

## 9. Implementation details, không phải semantics

- **Graph:** `zo_graph_build.py` xác nhận đường dẫn, gọi LuaLaTeX và chuyển PDF→SVG; source là raw TikZ/PGFPlots. Tên `zo graph v02 ...` là style macro; không phải schema semantic. `domain`, `samples`, `xmin/xmax` là các tham số trong TeX, chưa được một parser R6 kiểm tra xuyên output.
- **Geometry:** YAML keys, role strings, `ROLE_STYLE`, `tkz-euclide`/`tikz-3dplot` commands, auto-visibility, coordinate projection, `draw` flag, layer/order, `visibility_overrides`, receipt và output formats là implementation contract của compiler. Các giá trị này chỉ được nhận là semantic evidence ở đúng phần chúng thực sự biểu diễn, không tự thành ontology.
- **Variation:** positional rows, token replacement, index offset `excluded_columns`, conversion sang TeX, Lua module options, CSS selectors, hidden table generation, file ID/title và asset path là implementation. `column_min_widths_mm` là layout parameter, không phải semantic property.
- **Schema gaps:** variation không có JSON Schema độc lập; geometry không có external YAML schema trong phạm vi source đã tìm. Không tạo schema hoặc sửa implementation tại P1.3c.

## 10. Các giả thuyết P1.3a/b được xác nhận hoặc sửa

| Giả thuyết/candidate trước đây | Đánh giá sau direct-source read |
|---|---|
| **HYP-R6-01:** tổ chức R6 quanh semantic roles thay vì từng tool | Được hỗ trợ như một cách tổ chức nghiên cứu, vì từng subsystem đã có các role fragments; chưa được kiểm chứng như kiến trúc cuối hoặc Principle. |
| **HYP-R6-02:** graph/geometry/variation đủ nền để trích vocabulary chung mà không viết lại subsystem | **Chỉ đúng một phần.** Có thể trích các role cục bộ và một vài khái niệm tương cận. Variation vẫn dựa positional/free-text schema; geometry relations chỉ có vài kind; graph runtime raw TeX. Bằng chứng chưa đủ để khẳng định đã có shared vocabulary hoặc bao phủ đầy đủ. |
| **HYP-R6-03:** color là secondary encoding cho phần lớn mathematical roles | Source ngăn màu thay thế sign/status ở graph/variation, nhưng thực thi còn màu curve-main/geometry-main. Giữ như candidate, không xác nhận thành quy tắc xuyên hệ thống. |
| **HYP-R6-04:** line style/shape/position/label bền hơn color xuyên print/screen | Source hiện có các encoding không chỉ màu, nhưng chưa có kiểm thử tương đương cross-medium. Chưa xác nhận tính “bền hơn” nói chung. |
| **SC-04 / “distinguish mathematical roles”** | Xác nhận ở cấp subsystem đối với axis/curve/guide, included/excluded graph & variation, visible/hidden geometry; không suy ra rằng mọi ví dụ ở baseline là shared roles. |
| **P1.3a: domain khác sampling range** | Được xác nhận rõ bởi graph v0.2; README nối `domain`/`samples` với TeX. Cần thêm observation window thành khái niệm thứ ba; không gộp ba khái niệm thành một “domain”. |
| **P1.3a: point included/excluded** | Được xác nhận trong graph convention và variation field `excluded_columns`; chưa xác nhận là field/state dùng chung với geometry. |
| **P1.3a: visible/hidden** | Xác nhận là role/state 3D geometry theo camera; không tương đương included/excluded hoặc có/không có object. |
| **P1.3a: primary/reference** | Graph guidance phân cấp theo task nhưng so sánh ngang hàng có hai curve đồng mức; geometry `emphasized` là style flag. Sửa thành role có context, không phải thuộc tính phổ quát của object. |
| **P1.3a: exact/approximate, active/reference** | Chưa thấy role type/field tương ứng trong nguồn đã đọc; loại khỏi phần **confirmed**. Có thể giữ open nếu các case R6 sau này cần. |
| **P1.3a: asymptote khác graph/guide** | Xác nhận: graph gọi asymptote riêng, yêu cầu dựa phân tích giới hạn; style/API khác generic auxiliary. Không khái quát thành một cách vẽ bắt buộc xuyên medium. |
| **P1.3a: label và annotation** | Chưa đủ cơ sở để khẳng định hai role hiện được tách. Graph có label/legend, geometry có label target/text, variation có row-header text; không subsystem nào có loại `identifier` so với `explanation` rõ ràng. |
| **P1.3a: relation markers** | Thu hẹp mạnh ở geometry: right-angle/angle marker và tangent constraints có bằng chứng; không có taxonomy tổng quát cho parallel, perpendicular, equal length, equal angle. |

## 11. Gap còn lại

### Variation

- Không có role type/schema riêng cho endpoint, finite/infinite limit, function value vs limit, undefined, discontinuity, critical point, local maximum/minimum hoặc included/excluded endpoint tổng quát.
- `+∞`/`−∞` được nhận diện để sắp mốc và dựng glyph, nhưng source không nhận biết đó là domain endpoint, limit của function hay nội dung cell khác.
- “Không xác định” hiện là chuỗi tự do; field loại khỏi miền mới là dữ liệu có semantics trực tiếp. Cần phân biệt undefined value, excluded domain point, jump/discontinuity và hole nếu mục tiêu inventory sau này cần chúng.
- Local-extrema validation chỉ bao phủ hai mẫu sign change quanh `0`; không xử lý mọi critical point, plateau, endpoint extremum hoặc derivative undefined.
- Cấu trúc accessible HTML có table/caption/header nhưng chưa gán semantic role riêng cho derivative/trend/limit/undefined; `alt` mặc định chưa mô tả nội dung toán học.

### Geometry

- Không có relation catalog chung: chỉ bốn loại tangency được kiểm tra và hai loại angle marks được vẽ. Parallel, generic perpendicular, equal-length/equal-angle markers còn mở.
- Không có line/ray object type tổng quát ở compiler đã đọc; chỉ có segment/edge và các hình/curve hỗ trợ.
- Không phân biệt identifier label với explanatory annotation; `mask`, `draw` và `emphasized` là cờ render, không nên đọc thành semantic status.
- Cần giữ rõ surface fill (mặt hình học) với mask nền label và brand/background decoration.

### Graph và cross-system

- Graph spec đã định nghĩa nhiều role, nhưng raw TeX pipeline không kiểm tra semantic-role mapping; domain/sample/observation distinction hiện mới được cấu trúc hóa bằng các tham số/authoring conventions.
- Không có evidence đủ cho role taxonomy chung xuyên subsystem, accessibility equivalence của variation/geometry, hoặc semantic continuity khi chuyển sang video/interactive.
- “Brand decoration ≠ mathematical semantics” là ranh giới cần giữ trong inventory: frame, background, border và rounded corners không phải mathematical object/state.

## 12. Semantic Role Inventory v0.2

**Quy ước đếm:** các dòng dưới đây là role families để ghi nhận bằng chứng trực tiếp. Những trạng thái ghép trong cùng một dòng (ví dụ visible/hidden) được tính là một role family; style values và implementation details không được đếm. Số lượng là chỉ mục làm việc của inventory, không phải số lượng token.

### A. Confirmed from direct source — 34 role families

| ID | Subsystem | Role family được source hỗ trợ | Source/locator | Strength and boundary |
|---|---|---|---|---|
| D01 | Graph | Curve toán học chính | Quy chuẩn graph §2.4; README §2 | Trực tiếp; thứ bậc phụ thuộc mục tiêu hình. |
| D02 | Graph | Curve so sánh ngang hàng | Quy chuẩn graph §2.4–2.5; README §2 | Trực tiếp; không tạo primary/secondary giả chỉ theo thứ tự. |
| D03 | Graph | Axis | `zo_graph_v02.tex`, `zo graph v02 axis` | Trực tiếp; arrow/style là convention. |
| D04 | Graph | Tangent | README §2; TeX style `zo graph v02 tangent` | Trực tiếp; role riêng; hình thức dash là convention. |
| D05 | Graph | Asymptote | README §2; TeX style `zo graph v02 asymptote`; quy chuẩn §4.2, §8.5 | Trực tiếp; phải có căn cứ giới hạn; không suy chỉ từ hình gần thẳng. |
| D06 | Graph | Auxiliary/reference guide | README §2; TeX style `zo graph v02 auxiliary` | Trực tiếp; không thay thế tangent/asymptote. |
| D07 | Graph | Projection line/coordinate guide | README §2; quy chuẩn §8.7 | Trực tiếp; guide theo nhiệm vụ. |
| D08 | Graph | Point/marker | README §2; TeX styles point | Trực tiếp. |
| D09 | Graph | Point included/excluded / endpoint status | Quy chuẩn §8.6; README §2; `point open` style | Trực tiếp ở semantic convention; ring marker không universal. |
| D10 | Graph | Function domain | Quy chuẩn §4.1; authoring `domain` trong README | Trực tiếp; không đồng nhất sample interval. |
| D11 | Graph | Sampling interval/range | Quy chuẩn §4.1, §4.4–4.5; README `domain`, `samples` | Trực tiếp; hiện là TeX authoring parameters. |
| D12 | Graph | Observation window | Quy chuẩn §4.1, §4.6; README `xmin...ymax` | Trực tiếp; không phải miền xác định/giá trị. |
| D13 | Graph | Branch break/discontinuity boundary | Quy chuẩn §4.2–4.4; tách lệnh vẽ trong authoring | Trực tiếp như requirement; compiler không kiểm tra. |
| D14 | Graph | Object label/legend identity | README §2; quy chuẩn §7.7, §11.4 | Trực tiếp ở mức label/legend; identifier vs explanation chưa tách. |
| D15 | Graph | Mathematical filled region/area | Quy chuẩn §4.3, §8.5; style highlight | Trực tiếp về ý nghĩa miền; fill token là convention. |
| D16 | Geometry | Point/vertex | Compiler `validate_2d`, `validate_3d`; renderer 2D/3D | Trực tiếp; id và tọa độ/tham chiếu. |
| D17 | Geometry | Segment/edge | Compiler `validate_3d`, `render_2d`, `render_3d` | Trực tiếp; không có generic line/ray type. |
| D18 | Geometry | Face/surface | Compiler `validate_3d`, surface fill renderer | Trực tiếp; fill style không phải semantics. |
| D19 | Geometry | Supported shape/conic object family | Compiler `render_2d`, `validate_3d` | Trực tiếp về supported types; không phải taxonomy R6 đầy đủ. |
| D20 | Geometry | Visible/hidden projection state | Compiler `auto_face_visibility`, `visibility_overrides`; styles | Trực tiếp; visible/hidden là occlusion state theo camera. |
| D21 | Geometry | Auxiliary segment | Compiler `render_3d`/`style_for`, `ROLE_STYLE` | Trực tiếp cho role implementation hiện tại. |
| D22 | Geometry | Constructed point: projection/circumcenter/section point | Compiler `render_2d`, `compute_section` | Trực tiếp; chỉ các construction được hỗ trợ. |
| D23 | Geometry | Angle mark/right-angle mark | Compiler `render_2d`, `render_3d`; geometry style | Trực tiếp; right-angle mark không phải relation catalog tổng quát. |
| D24 | Geometry | Tangency relation to circle/ellipse/parabola/hyperbola | Compiler `validate_relations_2d` | Trực tiếp; bốn kind cụ thể, chưa có tangency generalization khác. |
| D25 | Geometry | Dimension annotation | Compiler `validate_3d`, `render_3d` dimensions/angles | Trực tiếp; display text/position là implementation. |
| D26 | Geometry | Label attached to target point/vertex/section | Compiler `validate_common`, `validate_2d`, `validate_3d` | Trực tiếp; không tách identifier/explanation. |
| D27 | Variation | Abscissa/breakpoint | README sample; `validate_record`, `point_key` | Trực tiếp; nằm trong hàng đầu theo position. |
| D28 | Variation | Interval between breakpoints | README §2; alternating columns in validator/template | Trực tiếp về layout semantics; không có typed cell enum. |
| D29 | Variation | Derivative sign row | README sample; `validate_record` ba hàng | Trực tiếp khi record có ba hàng; nhãn hàng là text. |
| D30 | Variation | Function-value row/value at a breakpoint | README sample; `validate_record` extrema check | Trực tiếp theo vị trí trong row; chưa tách value khỏi limit. |
| D31 | Variation | Increasing trend | Validator sign/trend mapping; README sample | Trực tiếp; mũi tên là convention. |
| D32 | Variation | Decreasing trend | Validator sign/trend mapping; README sample | Trực tiếp; mũi tên là convention. |
| D33 | Variation | Constant trend pattern (`0` ↔ `→`) | `validate_record` | Trực tiếp như mapping kiểm tra hẹp, không là theorem inference tổng quát. |
| D34 | Variation | Excluded point from domain | README `excluded_columns`; compiler/Lua; consumer BBT13 | Trực tiếp; `∥` là current realization, không phải universal glyph. |

**Không cộng vào 34 semantic role families:** geometry `emphasized`, `draw`, `mask`; chúng là field/state điều khiển rendering hoặc readability. Compiler có kiểm tra hai mẫu local maximum/minimum qua dấu đạo hàm; chúng được giữ là evidence của validation rule (mục 5) nhưng không tính là role family vì không có role/type/name riêng trong data contract.

### B. Consolidated inference — 8

1. Object–guide–relation có thể là một lớp phân loại candidate, nhưng từng subsystem giữ các phân biệt riêng.
2. Membership (`included/excluded`) có thể là semantic family dùng chung giữa graph/variation, chưa có bằng chứng ở geometry.
3. Visibility cần gắn context chiếu; không thể dùng như synonym của membership.
4. Domain, sampling range và observation window là ba khái niệm cần tách, hiện có source rõ ở graph chứ không phải schema xuyên subsystem.
5. Variation có thể cần cell/row role typing nếu muốn giảm phụ thuộc positional array; đây là hướng có thể rút từ source gap, không phải thiết kế đã chốt.
6. Label identity, explanation annotation và caption có thể cần tách nhưng chưa có role model chung.
7. Emphasis là prominence/visual state, không đồng nghĩa primary mathematical object.
8. Role-first inventory là cách tổ chức R6 khả thi để nghiên cứu tiếp; chưa xác nhận thành architecture hoặc Principle.

### C. Still open

- Typed variation roles cho endpoint, limit, infinity-as-limit, undefined, discontinuity, critical point, extrema và endpoint inclusion.
- Phân biệt point excluded khỏi domain với value không xác định, lỗ/nhảy/tiệm cận.
- Hệ relation geometry cho parallel, perpendicular tổng quát, equal length, equal angle, incidence semantic và các quan hệ khác.
- Line/ray object types trong geometry.
- Label định danh, explanatory annotation, caption và alt text có cấu trúc.
- Semantic equivalence của các role khi chuyển giữa graph/geometry/variation, print/web/video/interactive.
- Exact/approximate và active/reference: chưa được source trong scope này xác nhận.
- Vai trò nào là shared semantic, subsystem-specific semantic, representation rule hay content/brand decoration sau khi test trên representative cases.

## 13. Readiness cho bước tiếp theo

- **Graph:** đủ evidence để ghi role candidate có provenance và tách role với style; chưa có schema compiler để chứng minh implementation mapping đã được chuẩn hóa.
- **Geometry:** có field/compiler evidence khá cụ thể cho object types, visibility/emphasis, labels, angle marks và một số tangency relations; chưa đủ cho taxonomy relations.
- **Variation:** gap đã thu hẹp đáng kể ở mức cấu trúc dữ liệu hiện có: mốc/interval, derivative sign, direction, function values, excluded point và hai local-extremum checks được nhận diện. Nhưng source không có typed status cho limit/undefined/critical point và representation cross-medium chưa được thống nhất.
- **R6 tổng thể:** đủ sẵn sàng cho bước **kết tinh inventory evidence**; chưa đủ sẵn sàng để promote thành semantic token, Principle, Decision hoặc specification. Chưa thấy blocker kỹ thuật để tiếp tục phân tích; các semantic gaps còn lại cần được giữ explicit, không lấp bằng quy ước của công cụ.

## 14. Đề xuất một bước kế tiếp

**Đề xuất duy nhất: P1.3d — Reconcile và kiểm nghiệm Semantic Role Inventory R6 trên representative cases.**

Bước đó nên dùng một số case hiện có ở graph, geometry và variation để kiểm từng role family, nhất là:

- domain / sampling range / observation window;
- mathematical object / guide / asymptote;
- included/excluded / visible/hidden;
- identifier label / explanatory annotation;
- variation value / limit / undefined / discontinuity.

Mục tiêu là xác định role nào thật sự shared, role nào subsystem-specific, và role nào chưa thể phân loại; chưa ánh xạ sang màu, font, token hoặc implementation. Đây chỉ là đề xuất, không thực hiện P1.3d trong P1.3c.
