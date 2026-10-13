# Gói bàn giao cho “ZO Math Design System & Brand Language — Draft 0.1”

## 1. Mục tiêu và trạng thái đầu vào

Viết một bản thảo tích hợp có thể review, không phải một hệ thống đã phát hành. Nguồn đang ở các mức khác nhau: owner-confirmed intent, research evidence, research candidate, historical/implementation. Không có permission để gọi các nội dung tổng hợp dưới đây là Decision, Principle, canonical hoặc specification.

Draft 0.1 cần mô tả những gì đã biết, đề xuất có điều kiện ở miền đủ căn cứ, và để mở những miền cần test/owner decision. Không cần giải quyết mọi gap trước khi viết.

**Điểm dừng của gói hiện tại:** đây là brief và source index, không phải bản thảo 0.1. Không bắt đầu viết Draft 0.1 trong nhiệm vụ consolidation này; chỉ bắt đầu khi được giao riêng.

## 2. Brand Foundation — nội dung được phép đưa vào

### Owner-confirmed current intent

- **ZO Math là một không gian giáo dục toán học.**
- ZO Math được khai sinh trong và dành cho việc học Toán trong kỉ nguyên AI; AI vừa thách thức vừa hỗ trợ phát triển. ZO Math không được định vị thành “AI brand”.
- **Suy lí (Reasoning) và Kiến tạo ý nghĩa (Sense Making)** là triết lí nền tảng hiện nay để xây học liệu Toán. Nguồn khởi phát: NCTM, *Focus in High School Mathematics: Reasoning and Sense Making*. Triết lí mở để cập nhật, không phải doctrine đóng.
- Học sinh là đối tượng trung tâm dài hạn; hiện ưu tiên tiếp cận học sinh THPT. Nhóm tiếp theo gồm người tự học, người nghiên cứu và người hợp tác; giáo viên/phụ huynh là nhóm liên quan theo bối cảnh hiện nay.
- Tầng trực tiếp: sản phẩm giáo dục Toán chất lượng cao, trải nghiệm học tập hiệu quả, tạo nguồn thu cho ZO Math. Tầng sâu: phát triển năng lực suy nghĩ và tự hiểu mình thông qua Toán, âm thầm/liên tục; không phải slogan bắt buộc.
- “Học để tìm lại chính mình” và mở rộng phạm vi ngoài THPT là research directions, không phải mission, manifesto, slogan hoặc taxonomy đã chốt.

P1.1f được chủ dự án duyệt làm nền nghiên cứu để chuyển sang R2; đây không phải phê duyệt final Brand Foundation wording hay Decision.

### External research boundary

ER-01 cung cấp nền để nói thận trọng về understanding, procedural fluency, reasoning, sense making, reflection và worked examples. Không tuyên bố mức phổ biến của khó khăn ở học sinh Việt Nam, superiority của một pedagogy hoặc hiệu quả của sản phẩm ZO Math. Xem [P1.1d](../pha_1/P1_1_R1/P1_1d_ER01_boi_canh_hoc_Toan.md) và [P1.1e](../pha_1/P1_1_R1/P1_1e_ket_tinh_ER01_he_qua_thuong_hieu_thiet_ke_R1.md).

## 3. Brand Personality — candidate có owner calibration

Giữ nguyên bốn formulation:

1. Gần gũi trong tôn trọng.
2. Sống động nhưng điềm tĩnh.
3. Giản dị mà sâu sắc.
4. Rõ ràng và trong sáng.

Phân biệt rõ:

- **Personality core:** bốn formulation trên.
- **Điều kiện nền:** chính xác, trung thực với bằng chứng, tôn trọng Toán học/người học.
- **Trait theo ngữ cảnh:** khám phá có định hướng.
- **Strategy:** tối giản/tiết chế/giảm nhiễu/điều chỉnh theo medium.
- **Outcome mong muốn:** đáng tin, có bản sắc, không generic/lạnh/phô diễn.

Các formulation đã được calibration, nhưng profile vẫn là candidate; không chuyển trực tiếp thành quy tắc màu, font, shape, motion hoặc layout. Nguồn: [P1.2c](../pha_1/P1_2_R2/P1_2c_owner_calibration_personality_R2.md), [P1.2d](../pha_1/P1_2_R2/P1_2d_Brand_Personality_Candidate_v0_1.md), [P1.2e](../pha_1/P1_2_R2/P1_2e_ket_tinh_R2_va_gate_chuyen_tiep.md).

## 4. Owner-confirmed constraints về ngôn ngữ Toán

- Công thức thực sự phải được dàn bằng LaTeX đúng trong vùng công thức phù hợp.
- Tránh lạm dụng dấu suy ra/tương đương `⇒`/`⇔` để rút ngắn prose.
- Khi phù hợp, trình bày lập luận bằng câu văn.

Đây là constraints có provenance trong owner calibration P2.3, không phải bằng chứng rằng mọi mockup/asset cũ đã tuân thủ.

## 5. Research constraints và ngôn ngữ ngữ nghĩa Toán

### R6 working architecture

> semantic meaning → role → representation → medium adaptation → implementation

R6 đủ làm visual-exploration constraints, không đủ tạo semantic token cuối:

- bảo toàn mathematical object identity và phân biệt role khác nghĩa;
- tách domain / sampling range / observation window;
- tách mathematical reference (ví dụ asymptote/tangent) khỏi generic auxiliary guide;
- giữ included/excluded khi relevant;
- geometry visible/hidden là projection state, không phải membership;
- label attachment phải rõ;
- representation có thể đổi, meaning không đổi;
- decoration/brand marker không tự có mathematical authority.

Giữ graph, geometry, variation specifics đúng subsystem. Open gaps chính: rich variation semantics, geometry relation taxonomy, label-vs-explanation typing, semantic HTML/accessibility, acceptance theo medium. Nguồn: [P1.3b](../pha_1/P1_3_R6/P1_3b_Semantic_Role_Inventory_R6.md), [P1.3c](../pha_1/P1_3_R6/P1_3c_deep_source_read_semantic_roles_R6.md), [P1.3d](../pha_1/P1_3_R6/P1_3d_ket_tinh_R6_va_Visual_Readiness_Gate.md).

## 6. Domain-by-domain summary

| Miền | Tình trạng dùng trong Draft 0.1 |
|---|---|
| Brand Foundation | Nêu owner intent, research directions và external-evidence boundaries |
| Personality | Nêu bốn owner-calibrated formulations ở cấp candidate |
| Verbal/mathematical language | Ghi constraints LaTeX/prose/notation; các quy tắc verbal còn lại phải gắn trạng thái nguồn |
| Color | Inventory + palette hypotheses; không chọn final values |
| Typography | Role/fallback candidates; không chọn final family |
| Logo/identity | Asset/provenance problem và research direction; không chọn master |
| Mathematical expression | R6 constraints candidate; giữ subsystem-specific roles |
| Layout/spatial | Hypotheses về hierarchy/specimen; chưa có system chung |
| Website/UI | Current config/cascade evidence; không coi CSS hiện tại là spec |
| PDF/learning materials | Config và print questions; không khẳng định output đã nghiệm thu |
| Graph/geometry/variation | Direct-source roles/pipelines; semantic HTML/edge cases còn mở |
| Video/motion | Có prototype/workflow đại diện; chỉ candidate experiments, không có motion grammar |
| Audio/sonic | Narration/cues có dấu vết; không đủ để đề xuất identity |
| Social/distribution | Assets/card generator và format mentions; adaptation/performance chưa kiểm |
| Accessibility | Nêu test requirements; không claim conformance |
| Cross-medium | Invariants/adaptations là hypothesis; cần matrix test |
| Tokens/components/automation | Inventory kỹ thuật; chưa thiết kế tokens/components |
| Governance/provenance | P1.0 là proposal; `_research` là research memory, không phải policy DS đã duyệt |

Mức readiness theo từng miền ở [03](./03_MA_TRAN_TRANG_THAI_VA_SAN_SANG.md); conflict/gap ở [04](./04_MAU_THUAN_VA_KHOANG_TRONG.md).

## 7. Những gì có thể đề xuất

- Brand Foundation và personality formulation có provenance, giới hạn và trạng thái candidate.
- Verbal/math constraints được owner xác nhận.
- R6 minimal semantic constraints và subsystem-specific representation candidates.
- Palette/type/layout hypotheses được nêu như options cần so trên cùng nội dung.
- Candidate test criteria cho print/grayscale, mobile, line hierarchy, contrast, captions, labels và semantics.
- Rà asset/provenance và adaptation requirements cho logo, video, social, PDF.
- Governance/provenance process candidate dựa trên P1.0, ghi rõ chưa phê duyệt.

Chi tiết permission theo domain: [06](./06_CANDIDATE_CO_THE_DE_XUAT.md).

## 8. Những gì phải giữ mở

- Public mission/manifesto/slogan, ý nghĩa cuối cùng của “Học để tìm lại chính mình”.
- User needs/segmentation/customer hierarchy/market claims.
- Exact palette, semantic color assignments, final fonts/fallbacks, logo master, motif approval.
- Grid/spacing/radius/breakpoints, component/token values, migration.
- A+ owner calibration sau P2.3; direction cuối.
- Motion grammar, subtitle/vertical-safe-zone system, voice/TTS/music/SFX/sonic logo.
- Accessibility conformance; semantic HTML coverage; R10 cross-medium acceptance.
- Governance authority, release/deprecation/exception processes.

## 9. Critical conflicts

1. Palette/color-role divergence: repeated red is not a final primary; graph versions and media/prototype values differ.
2. Typography configuration/comment conflict and per-medium stacks not yet tested.
3. Logo variants and `master` labels lack authority/provenance resolution.
4. A+ is not a final direction; visual evidence improved from P2.1/2 but remains exploratory and lacks post-A+ owner calibration.
5. Accessibility/output acceptance and governance proposal are not approved/verified.

The apparent content-block versus R1-G01 difference is not currently demonstrated as a direct conflict: the sources address different architecture/meaning layers. Do not “resolve” by collapsing them.

## 10. Required structure of Draft 0.1

1. Purpose, scope, audience and explicit non-goals.
2. Evidence/status vocabulary and how to read the document.
3. Brand Foundation: owner-confirmed intent, research directions, external claim boundaries.
4. Brand Personality: core, conditions, contextual traits, strategy, outcomes.
5. Verbal and mathematical expression constraints.
6. Semantic constraints for graph/geometry/variation and open subsystem roles.
7. Eighteen-domain status/candidate summary (link this consolidation matrix rather than repeat inventories).
8. Candidate areas, with provenance, confidence, scope, test condition and caveat.
9. Conflicts, open questions and acceptance gaps; distinguish G1/G2/G3.
10. Governance/provenance proposal status; explicit non-canonical status.
11. Source index and review path.
12. “What this draft is not”: not release spec, not system 1.0, no migration authority.

## 11. Source index for the writer

### Read first — source synthesis

- [P0.2 — Design archaeology](../pha_0/P0_2_khao_co_thiet_ke_ZO_Math.md)
- [P0.3 — Evidence and design genealogy](../pha_0/P0_3_ban_do_bang_chung_quyet_dinh_thiet_ke_ZO_Math.md)
- [P0.4 — Research map](../pha_0/P0_4_ban_do_nghien_cuu_ZO_Math_Design_System.md)
- [P1.0 — Governance/provenance proposal](../pha_1/P1_0_governance_provenance_toi_thieu.md)

### Foundation and personality

- [P1.1b — Owner confirmations](../pha_1/P1_1_R1/P1_1b_xac_nhan_noi_bo_chu_du_an_R1.md)
- [P1.1c — Audience scope](../pha_1/P1_1_R1/P1_1c_ket_tinh_pham_vi_doi_tuong_R1.md)
- [P1.1d — ER-01](../pha_1/P1_1_R1/P1_1d_ER01_boi_canh_hoc_Toan.md)
- [P1.1e — ER-01 implications](../pha_1/P1_1_R1/P1_1e_ket_tinh_ER01_he_qua_thuong_hieu_thiet_ke_R1.md)
- [P1.1f — Brand Foundation Candidate](../pha_1/P1_1_R1/P1_1f_Brand_Foundation_Candidate_v0_1.md)
- [P1.1a — Internal evidence baseline](../pha_1/P1_1_R1/P1_1a_baseline_bang_chung_noi_bo_R1.md)
- [P1.2a — Personality baseline](../pha_1/P1_2_R2/P1_2a_baseline_tinh_cach_cam_giac_R2.md)
- [P1.2b — Comparative research](../pha_1/P1_2_R2/P1_2b_nghien_cuu_tham_chieu_R2.md)
- [P1.2c — Personality owner calibration](../pha_1/P1_2_R2/P1_2c_owner_calibration_personality_R2.md)
- [P1.2d — Personality Candidate](../pha_1/P1_2_R2/P1_2d_Brand_Personality_Candidate_v0_1.md)
- [P1.2e — R2 synthesis](../pha_1/P1_2_R2/P1_2e_ket_tinh_R2_va_gate_chuyen_tiep.md)

### Mathematical expression and visual exploration

- [P1.3a — R6 baseline](../pha_1/P1_3_R6/P1_3a_baseline_ngon_ngu_bieu_dat_Toan_hoc_R6.md)
- [P1.3b — Semantic Role Inventory](../pha_1/P1_3_R6/P1_3b_Semantic_Role_Inventory_R6.md)
- [P1.3c — Deep source read](../pha_1/P1_3_R6/P1_3c_deep_source_read_semantic_roles_R6.md)
- [P1.3d — R6 synthesis/readiness gate](../pha_1/P1_3_R6/P1_3d_ket_tinh_R6_va_Visual_Readiness_Gate.md)
- [P2.0 — Visual exploration framework](../pha_1/P2_0_Visual_Exploration_Framework_va_Specimen_Set.md)
- [P2.1 — Directions A/B/C](../pha_1/P2_1/P2_1_Visual_Directions_v0_1.md)
- [P2.2 — Stress tests](../pha_1/P2_2/P2_2_Stress_Test_va_Owner_Calibration_Readiness.md)
- [P2.3 — A+ hypothesis](../pha_1/P2_3/P2_3_Hybrid_Visual_Direction_Aplus_v0_2.md)

### Technical source pointers (read only when drafting a domain section)

- Web: `../../../_quarto.yml`, `../../../zo-math.scss`, `../../../assets/css/custom.css`, `../../../assets/css/`.
- PDF: `../../../_quarto-pdf.yml`, `../../../assets/tex/zo-pdf.tex`, `../../../assets/lua/zo_pdf_branding.lua`.
- Graph: `../../../quy_trinh_xay_dung/quy_chuan_san_xuat_do_thi_ham_so_zo_math_v0.2.md`, `../../../quy_trinh_xay_dung/cong_cu_do_thi_ham_so_zo_math/`.
- Geometry: `../../../quy_trinh_xay_dung/quy_chuan_san_xuat_hinh_hoc_zo_math_v0.1.md`, `../../../scripts/zo_geometry.py`, `../../../assets/tex/zo-geometry-styles.tex`.
- Variation: `../../../quy_trinh_xay_dung/cong_cu_bang_bien_thien_zo_math/`, `../../../assets/lua/zo_variation_qmd.lua`, `../../../assets/css/zo_variation.css`.
- Logo/font: `../../../assets/logo/`, `../../../assets/fonts/`.
- Research memory: `../../../_research/README.md`, `../../../_research/90_syntheses/SYN-2026-08-29_khoi-dau-he-thong-tri-nho-nghien-cuu.md`.
- Video representative: `../../../content/vi_sao/lop_12/vi_sao_do_thi_ham_so_duoc_ve_bang_hai_truc_vuong_goc/vi_sao_do_thi_hai_truc_vuong_goc_video/vi_sao_do_thi_hai_truc_vuong_goc_video/00_README.md`, `02_kich_ban_hoat_anh.md`, `04_manim_scene.py`.
- Card distribution representative: `../../../content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_data/cards.yml`, `../../../scripts/zo_build_card_grid.py`.
- Media manuals/assets outside the main repository remain versioned historical evidence until lineage and approval are confirmed; see P0.2/P0.3 inventory.

P0.2/P0.3 and P1.3c list representative paths and limits. Do not expand this into a repository-wide inventory unless a claim in Draft 0.1 needs a specific locator.

## 12. Status vocabulary

Use these evidence labels consistently:

- **Owner-confirmed current intent** — owner statement; not external fact or final decision.
- **Research evidence** — external research or direct-source observation, with scope and limit.
- **Inference** — synthesis drawn from sources; never attribute it to the owner.
- **Hypothesis/candidate** — proposed direction awaiting test/review.
- **Historical/implementation** — existing code, asset, config, output or archive.
- **Open** — unresolved; no claim beyond the evidence.

Where governance maturity is discussed, distinguish P1.0's proposal-level lifecycle from approved policy. Never create a fake decision by labeling content “accepted”, “canonical” or “standard”.

## 13. Explicit drafting instruction

**Đề xuất cụ thể khi đủ cơ sở; dùng candidate khi chưa đủ; không biến historical implementation thành canonical.** Cite source and scope near each claim. Keep owner-confirmed intent separate from research and inference. Preserve contradictions instead of inventing a compromise. Do not write or authorize implementation/migration in Draft 0.1.
