# Candidate có thể đề xuất trong Draft 0.1

## Nguyên tắc

“Được phép đề xuất” không có nghĩa “được chọn” hoặc “được triển khai”. Mỗi candidate trong Draft 0.1 cần kèm: mục đích, provenance, scope, điều evidence hỗ trợ/không hỗ trợ, điều kiện test, và trạng thái chưa chốt. Không được biến các ứng viên này thành token, specification hoặc Decision.

| Miền | Có thể đề xuất cụ thể? | Mức tin cậy | Được đề xuất | Phải để mở / kiểm tra |
|---|---|---|---|---|
| **Nền tảng thương hiệu** | Có, ở cấp research candidate | Cao đối với owner intent | Foundation wording gần với OCONF; tách core dài hạn, ưu tiên hiện tại và research directions | Public mission/manifesto/slogan; scope/taxonomy dài hạn |
| **Personality** | Có, ở cấp formulation candidate | Cao đối với bốn formulation được calibration | Bốn câu cân bằng đã xác nhận; phân tách core, contextual trait, condition, strategy, outcome | Personality approval cuối; cách đo cảm nhận; chuyển thành visual/verbal rules |
| **Ngôn ngữ diễn đạt** | Có, với constraints đã xác nhận | Cao cho các constraint cụ thể; thấp-vừa cho full voice system | LaTeX đúng cho công thức; tiết chế `⇒`/`⇔`; prose reasoning khi phù hợp; giọng tôn trọng người học như candidate | Full tone/terminology/Unicode/subtitle/caption spec |
| **Màu sắc** | Có thể đề xuất palette scenarios/candidates, không chọn winner | Thấp-vừa | Nêu options rooted in historical values/P2 probes, role hypothesis, contrast/gray-scale test plan | Exact palette, primary/secondary assignment, semantic color tokens, accessibility conformance |
| **Typography** | Có thể đề xuất role architecture/font pairing candidates | Vừa | Role matrix (reading/UI/math/label/caption); candidates từ evidence hiện có, có fallback test | Final family/weights/type scale/licensing/fallback across browser/PDF/video |
| **Logo/identity** | Chỉ hướng nghiên cứu/provenance candidate | Thấp | Asset lineage/variant matrix; test checklist cho nền, size, avatar/favicon; phân biệt mark và motif | Chọn master, redesign, motif use approval, clear-space/spec |
| **Ngôn ngữ Toán (R6)** | Có, ở mức semantic constraints candidate | Vừa-cao | Meaning→role→representation→adaptation; membership, scope, guide/reference, label attachment, decoration boundary | Shared semantic tokens/ontology và những role chưa có direct evidence |
| **Layout/spatial** | Có thể đưa layout hypotheses | Vừa-thấp | Common-content specimen testing; hierarchy/spacing candidates; chống card hóa theo mặc định | Grid/spacing/radius/breakpoints và universal layout rules |
| **Website/UI** | Có thể đưa implementation-aware candidates | Vừa-thấp | Mô tả cascade/dependency và các patterns cần kiểm theo loại trang/viewport | Thay theme hiện tại, source-of-truth, final components |
| **PDF/học liệu** | Có thể đưa role/acceptance candidates | Vừa-thấp | Print/grayscale/readability criteria; xem xét riêng PDF typography/page structure | Final page geometry, font config, headers/footers, acceptance |
| **Graph/geometry/variation** | Có, theo từng subsystem | Vừa-cao về meaning roles; thấp hơn về visual realization | Bảo toàn confirmed roles và phạm vi tool; tách semantics khỏi màu/nét/compiler | Shared tokens; relation taxonomy chưa có; exact styles; semantic HTML variation |
| **Video/motion** | Chỉ weak hypothesis/experiments | Thấp | Motion phục vụ cấu trúc Toán, timing/pause/safe-zone research; cùng nội dung để so | Motion grammar, timing values, intro/outro, vertical/subtitle template |
| **Audio/sonic** | Không đề xuất identity cụ thể | Rất thấp | Chỉ đề xuất câu hỏi, evidence plan, asset/provenance inventory | Voice/TTS profile, music/SFX language, mix, sonic logo |
| **Social/distribution** | Có thể đề xuất adaptation experiments | Thấp | Asset/platform inventory, crop/thumbnail/caption tests trên một số kênh | Platform master templates, performance claims, final sizes/ratios |
| **Accessibility** | Có thể đề xuất test criteria, không claim compliance | Thấp | Contrast/non-color/semantic HTML/captions/alt/keyboard/readability acceptance plan | WCAG conformance hoặc tuyên bố accessibility đã đạt |
| **Cross-medium** | Có thể đề xuất mapping hypotheses | Vừa-thấp | Candidate invariants: meaning, personality, role distinction; adaptation matrix | Quy tắc bất biến chính thức và exception map đã test |
| **Tokens/components/automation** | Chỉ architecture options sau semantic design | Vừa về feasibility kỹ thuật, thấp về system model | Inventory existing SCSS/JSON/YAML/compiler/receipt; source-of-truth questions | Token names/values, component library, migration |
| **Governance/provenance** | Có thể đề xuất process candidate | Vừa-thấp | Giữ evidence classes, owner, scope, status, links, review trigger; tham chiếu P1.0 là proposal | Authority map, accepted lifecycle/release/exception/deprecation policy |

## Cách xử lý P2.1–P2.3

- Có thể mô tả **A+ — “Ấm, trong sáng, có kỉ luật”** như một visual hypothesis đã mở rộng qua 8 specimens, không phải standard candidate.
- Có thể giữ các insight từ A/B/C: controlled warmth; typography/print discipline; line hierarchy/spatial rhythm; tránh phụ thuộc màu hoặc card/radius.
- Ghi rõ owner calibration ban đầu chỉ nói Direction A gần hình dung hiện tại nhất; phản hồi đó không chọn A cuối. P2.1/P2.2 evidence khi đó còn quá ít; P2.3 mở rộng evidence nhưng chưa có owner calibration tiếp.
- Hai owner constraints về LaTeX và kí hiệu logic có thể được nêu trực tiếp như constraints, tách khỏi hình thức A+.

## Không đề xuất cụ thể nếu không mở nghiên cứu bổ sung

- Sonic identity hoặc một profile voice/TTS.
- Một logo master hoặc bộ quy tắc logo.
- Palette/font final hoặc semantic tokens.
- Motion grammar/cụ thể hóa easing/timing.
- User personas, market segments hoặc customer hierarchy.
- Compliance accessibility hoặc claim hiệu quả học tập.

Tham chiếu readiness từng miền tại [03](./03_MA_TRAN_TRANG_THAI_VA_SAN_SANG.md) và gap tại [04](./04_MAU_THUAN_VA_KHOANG_TRONG.md).
