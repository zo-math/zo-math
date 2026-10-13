# Ma trận trạng thái và mức sẵn sàng

## Thang maturity

| Mức | Định nghĩa dùng trong gói |
|---:|---|
| **0 — Chưa có** | Chưa tìm thấy evidence có thể dùng trong scope |
| **1 — Có dấu vết** | Có ý tưởng, asset, source hoặc implementation; chưa tổng hợp/kiểm chứng đủ |
| **2 — Có nghiên cứu** | Có đối chiếu, phân tích provenance/giới hạn hoặc source research |
| **3 — Có candidate** | Đủ cơ sở để đưa một phương án có giới hạn vào Draft 0.1 |
| **4 — Có thể gần chốt** | Evidence + thử nghiệm + owner calibration đáng kể; vẫn chưa đồng nghĩa đã chốt |

Đây là độ trưởng thành của bằng chứng theo miền, không phải mức tốt/xấu. Không dùng mức 5 hoặc “hoàn tất”.

## Ma trận 18 miền

| # | Miền | Mức | Căn cứ maturity | Trạng thái để viết Draft 0.1 | Còn thiếu quan trọng |
|---:|---|---:|---|---|---|
| 1 | Nền tảng thương hiệu | **3** | OCONF-01..11; R1 synthesis và ER-01 giới hạn claim | Nêu foundation như ý định/candidate có provenance | Final public wording; user evidence cho nhu cầu/thị trường |
| 2 | Tính cách thương hiệu | **3** | Bốn formulation được owner-calibrated; R2 synthesis phân tách core/context/strategy/outcome | Nêu bốn formulation; giữ hồ sơ ở cấp candidate | Owner acceptance của toàn bộ personality system; biểu hiện/test |
| 3 | Ngôn ngữ diễn đạt | **2** | Có guidance lịch sử và owner-confirmed ràng buộc Toán trong P2.3 | Có thể ghi các constraint cụ thể; tone/voice còn candidate | Verbal specification đầy đủ theo medium, caption/subtitle và kết luận |
| 4 | Màu sắc | **2** | Inventory, role cục bộ, xung đột có locator; P2 probes | Chỉ đưa palette direction/candidate có caveat | Palette validation, semantic mapping, contrast/grayscale |
| 5 | Typography | **2** | Config theo web/PDF/media và conflict đã được tổng hợp | Đề xuất role architecture/candidate font pairings để test | Render/fallback/diacritics/math glyphs/accessibility |
| 6 | Logo/nhận dạng | **1** | Nhiều variants, một số config use, provenance gap rõ | Chỉ đề xuất hướng khảo sát/variant review | Lineage, approval, visual/recognition test, usage rules |
| 7 | Ngôn ngữ biểu đạt Toán | **3** | P1.3a–d; 13 source trực tiếp; R6 đạt readiness candidate cho visual work | Đưa semantic constraints candidate, phân rõ shared/subsystem-specific | Acceptance cross-medium; rich roles/gaps theo case |
| 8 | Bố cục/không gian | **2** | Config, project review, P2 specimens; chưa có shared spatial system | Đề xuất hierarchy/layout candidate trên representative tasks | Responsive/readability test, shared-vs-medium rationale |
| 9 | Website/UI | **2** | Config/source map và project-specific patterns; chưa output audit toàn diện | Mô tả hiện trạng và đề xuất testable patterns | Render/cascade/viewport audit và accessibility |
| 10 | PDF/học liệu | **2** | TeX/YAML/Lua setup và content guidance | Nêu constraints đang khai báo và print candidate requirements | Render/print/embedding/readability acceptance |
| 11 | Graph/geometry/variation | **3** | Tool contracts, direct-source semantic inventory, production pipelines | Đưa roles/candidate visual constraints theo đúng subsystem | Variation semantic HTML, geometry relation taxonomy, edge-case QA |
| 12 | Video/motion | **1** | Một production workflow/scene; manuals và visual frame candidates | Đề xuất research questions/prototype candidates hạn chế | Motion grammar, vertical adaptation, safe zones/subtitle, viewer test |
| 13 | Audio/sonic | **1** | Narration source/cues và tài liệu quy trình | Chỉ nêu hiện trạng và gap; không đề xuất identity cụ thể | Voice/TTS/music/SFX/mix/sonic-logo evidence và approval |
| 14 | Social/phân phối | **1** | Social assets, card generator, một số channel/format mentions | Đề xuất adaptation tests, không hứa hiệu quả | Platform templates, crop/safe-area, asset approval, audience data |
| 15 | Accessibility | **1** | Có một số yêu cầu định hướng (non-color, captions/alt) nhưng chưa audit | Có thể nêu acceptance questions/checklist dạng candidate | Đo contrast, semantics, captions, keyboard/screen reader, print |
| 16 | Cross-medium | **2** | P0.4 R10, P2.0 framework và P2.3 specimens | Nêu invariants/adaptations như hypothesis để kiểm | Ma trận test/acceptance toàn medium |
| 17 | Tokens/components/automation | **2** | Kỹ thuật tồn tại theo subsystem; R11 architecture chưa làm | Chỉ mô tả foundation kỹ thuật; không thiết kế token | Semantic source of truth, exception/version mapping, visual acceptance |
| 18 | Governance/provenance | **2** | `_research` practices, P0 evidence map, P1.0 proposal | Ghi nguyên tắc provenance và open status; nêu P1.0 là proposal | Owner approval, authority map, lifecycle/release/deprecation |

## Readiness tổng thể

**Đủ sẵn sàng cho Draft 0.1 dạng bản thảo nghiên cứu có phân tầng trạng thái.** Mức maturity tổng hợp giữ ở **2/4**, vì phần lớn miền thị giác/triển khai chưa qua test và phê duyệt đủ để thành candidate system. Nền tảng thương hiệu, personality và R6 có các phần đạt mức 3.

Không có mức 4: các thử nghiệm P2 chưa được owner-calibrate sau A+; không có bằng chứng user validation xuyên miền; P1.0 chưa là governance được phê duyệt. Draft 0.1 có thể nêu candidate và câu hỏi mà không chờ các việc này, miễn không gọi chúng là chuẩn.

## Cách dùng ma trận

- Mức 1–2: mô tả evidence/hiện trạng, ranh giới và câu hỏi; chỉ đề xuất test.
- Mức 3: có thể đưa candidate cụ thể với provenance, điều kiện áp dụng và caveat.
- Mức 4: chỉ khi có thêm bằng chứng và calibration; vẫn cần chủ dự án chốt nếu nội dung tạo quyết định.
- Một miền có mức cao không làm tăng maturity của miền khác; ví dụ R6 không tự chốt màu, font hoặc layout.
