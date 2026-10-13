# P1.0 — Khung governance và provenance tối thiểu cho nghiên cứu ZO Math Design System

**Ngày lập:** 2026-10-05  
**Trạng thái tài liệu:** đề xuất khung vận hành tối thiểu; chưa phải governance đã được chủ dự án phê duyệt hoặc specification Design System.

## 1. Mục tiêu và phạm vi P1.0

P1.0 đề xuất cách ghi hồ sơ nghiên cứu và quyết định từ P1.1 trở đi sao cho truy được nguồn, phạm vi, bằng chứng, trạng thái, người xác nhận và lịch sử thay đổi. Mục tiêu là nhẹ, có thể dùng ngay và có thể phát triển sau; không xây governance đầy đủ cho Design System 1.0.

Nguồn chính:

- [P0.3 — Bản đồ bằng chứng và phả hệ quyết định thiết kế ZO Math](../pha_0/P0_3_ban_do_bang_chung_quyet_dinh_thiet_ke_ZO_Math.md)
- [P0.4 — Bản đồ nghiên cứu ZO Math Design System](../pha_0/P0_4_ban_do_nghien_cuu_ZO_Math_Design_System.md)
- [_research/README.md](../../../_research/README.md)
- [RQ-003 — Nguyên lí thiết kế bài ZO Math](../../../_research/10_questions/RQ-003_nguyen-li-thiet-ke-bai-zomath.md)
- [SYN-2026-08-29 — Khởi đầu hệ thống trí nhớ nghiên cứu](../../../_research/90_syntheses/SYN-2026-08-29_khoi-dau-he-thong-tri-nho-nghien-cuu.md)

P1.0 chỉ tạo tài liệu này. Không sửa production, không đổi tên/migrate hồ sơ hiện có, không tạo một hệ thống lưu trữ song song, không nghiên cứu câu hỏi cụ thể và không quyết định nội dung thương hiệu.

## 2. Những vấn đề governance được Pha 0 phát hiện

P0.2/P0.3 cho thấy cần truy dấu tốt hơn, nhưng không cho phép kết luận rằng mọi nhánh là lỗi hoặc mọi nguồn đã có cùng thẩm quyền:

- Nhiều logo, palette, stylesheet, font, manual video và snapshot cùng tồn tại; tên `master`, `final`, `canonical` hoặc `official` không chứng minh authority.
- Có implementation đang được cấu hình nhưng chưa có bằng chứng về rationale, output thực tế hoặc acceptance.
- Một số guideline có scope theo medium hoặc project; khác biệt giữa các scope có thể là adaptation có chủ đích.
- Graph, geometry và variation có source/tool/receipt; receipt kỹ thuật không thay visual, semantic, accessibility hoặc chuyên môn review.
- RQ-003 vẫn `active-through-practice`; `40_design_cases/` và `50_principles/` chưa được promote. README quy định chỉ tạo principle khi pattern lặp lại và có cơ sở.
- Audit, output sinh, handoff, snapshot và source không đồng nhất; audit/output có thể là bằng chứng, nhưng không tự thành nguồn thực thi hoặc quyết định.
- Một nhận định có thể có bằng chứng mạnh rằng “đang được dùng” nhưng vẫn yếu đối với câu hỏi “có nên trở thành quy tắc dài hạn không”.

Các điểm trên là nhu cầu provenance/review, không phải quyết định sửa hoặc hợp nhất các nguồn.

## 3. Nguyên tắc governance tối thiểu

1. **Hiện trạng ≠ quy chuẩn; implementation ≠ rationale.**
2. **Proposal ≠ decision; thử nghiệm ≠ acceptance.**
3. Acceptance trong một bài, project hoặc medium không tự trở thành canonical toàn Design System.
4. Khác biệt medium không mặc nhiên là inconsistency; phải ghi scope và lý do trước khi đánh giá.
5. Tên, ngày sửa, vị trí file và tần suất lặp không tự cấp authority.
6. Không xóa lịch sử khi nội dung bị bác bỏ, thay thế hoặc ngừng dùng; ghi liên kết tới hồ sơ kế tiếp.
7. Mỗi claim quan trọng ghi điều bằng chứng hỗ trợ và điều nó không chứng minh.
8. Tách bằng chứng ZO Math, bằng chứng bên ngoài và suy luận.
9. Quyết định Design System cuối cùng cần chủ dự án xác nhận.
10. Dùng hệ `_research` hiện có làm nền; chỉ mở rộng cấu trúc sau khi có nhu cầu và được chấp thuận, không di chuyển hồ sơ trong P1.0.

## 4. Các loại hồ sơ/đối tượng nghiên cứu

Đề xuất năm loại hồ sơ chính. Các khái niệm còn lại là trường/nội dung trong các hồ sơ này, không cần tạo file riêng cho mỗi loại.

| Loại hồ sơ | Nội dung bao gồm | Cách ghi nhận tối thiểu |
|---|---|---|
| **Research item** | Research Question (RQ), Validation Question (VQ), Observation, Hypothesis, Design Candidate; có thể giữ nhiều quan sát/giả thuyết trong một nghiên cứu | Một câu hỏi/phạm vi trung tâm, có liên kết tới chương trình R1–R12 và evidence |
| **Experiment** | Thử nghiệm thiết kế, so sánh, usability/readability/accessibility hoặc technical validation có hypothesis/tiêu chí | Hồ sơ độc lập khi cần lặp lại, so sánh hoặc truy acceptance; nếu là kiểm tra nhỏ, ghi kết quả trong Research item |
| **Decision record** | Decision; chấp nhận/tạm chấp nhận/bác bỏ Design Candidate; Principle Candidate; Design Principle hoặc Specification/Rule đã được duyệt | Chỉ một decision khi có quyết định thực sự; không tạo record quyết định cho 34 DES lịch sử |
| **Exception record** | Ngoại lệ có chủ đích theo project/medium/scope so với rule đã chấp nhận | Gắn với decision/rule gốc và điều kiện xem xét lại |
| **Asset/implementation provenance** | Implementation, asset source, generated output, derivative, snapshot, experiment hoặc production use | Record/section provenance gắn với hồ sơ liên quan; không thay thế source file hay registry kỹ thuật nếu sau này được duyệt |

**Ánh xạ các đối tượng được cân nhắc:**

- RQ/VQ, observation, hypothesis và design candidate: Research item.
- Experiment: Experiment record hoặc mục con trong Research item nếu chỉ là kiểm tra nhỏ, không cần theo dõi riêng.
- Decision, Principle Candidate, Design Principle, Specification/Rule: Decision record; phần nội dung được chấp nhận là kết quả của quyết định, không phải một lifecycle độc lập.
- Implementation/asset/generated asset: provenance fields gắn với quyết định hoặc experiment; status triển khai được quản trị trên trục riêng.
- Exception: Exception record.
- Deprecated item: không phải loại hồ sơ độc lập; lưu sự kiện deprecation/supersession trong decision/provenance record và liên kết tới hồ sơ thay thế.

## 5. Status lifecycle

### Trục A — Mức trưởng thành của tri thức/định hướng quyết định

Giữ bộ trạng thái đang dùng, với nghĩa được giới hạn rõ. Trục này áp dụng cho câu hỏi, candidate, kết luận nghiên cứu và decision; **không mô tả implementation/release**.

| Trạng thái | Nghĩa | Ai có thể gán | Điều kiện vào | Điều kiện ra |
|---|---|---|---|---|
| **Ý niệm** | Ý tưởng/quan sát đáng giữ nhưng chưa có câu hỏi và bằng chứng đủ để nghiên cứu | Bất kỳ người tham gia nào có thể đề xuất; người ghi hồ sơ gán khi tạo | Có mô tả ngắn, nguồn/ngữ cảnh nếu biết | Chuyển sang Đang nghiên cứu khi có câu hỏi, phạm vi và người phụ trách; hoặc Loại bỏ nếu không còn liên quan |
| **Đang nghiên cứu** | Câu hỏi/candidate đang được khảo sát; chưa được xem là accepted | Người phụ trách nghiên cứu; agent chỉ được ghi nhận theo giao việc, không tự thăng cấp quyết định | Có câu hỏi, scope, phương pháp dự kiến và liên kết evidence đầu vào | Tạm chấp nhận, Đã chốt hoặc Loại bỏ theo review; có thể tiếp tục mở nếu còn gap |
| **Tạm chấp nhận** | Kết luận/candidate đủ hữu ích để thử hoặc dùng trong phạm vi ghi rõ, có giới hạn và điều kiện mở lại | Người phụ trách đề xuất; chủ dự án xác nhận nếu có ảnh hưởng Design System ngoài thử nghiệm cục bộ | Có rationale, evidence, scope, risk, thời hạn/điều kiện review và người xác nhận tạm thời | Đã chốt sau decision gate; quay lại Đang nghiên cứu nếu xuất hiện gap; Loại bỏ nếu bị bác bỏ |
| **Đã chốt** | Quyết định được chấp nhận trong scope ghi rõ, ở thời điểm/version ghi rõ | Chỉ chủ dự án có quyền xác nhận trạng thái cuối của Design System | Có decision record và gate phù hợp; system-level cần chủ dự án xác nhận rõ | Có thể giữ làm lịch sử; nếu thay đổi, tạo decision mới liên kết `supersedes`/`superseded_by`, không ghi đè lịch sử |
| **Loại bỏ** | Candidate/kết luận không được theo tiếp hoặc bị bác bỏ trong scope đã ghi | Người phụ trách có thể đề xuất; chủ dự án xác nhận nếu đó là quyết định system-level | Ghi rationale, scope và evidence; không xóa hồ sơ | Giữ làm trạng thái lịch sử; bằng chứng mới tạo hồ sơ liên kết mới, không hồi sinh âm thầm record cũ |

`Đã chốt` nghĩa là decision được phê duyệt trong phạm vi và thời điểm nêu; không có nghĩa là vĩnh viễn hoặc tự động áp dụng cho mọi medium. `Loại bỏ` khác với deprecation: một candidate bị bác bỏ, còn một decision đã được chấp nhận nhưng về sau thay thế vẫn giữ lịch sử chấp nhận cũ.

### Trục B — Trạng thái implementation/use

Trục này áp dụng cho asset, component, rule đã được triển khai hoặc tool. Nó độc lập với Trục A.

| Trạng thái implementation | Nghĩa |
|---|---|
| **Chưa triển khai** | Chưa có implementation; có thể chỉ có quyết định hoặc specification |
| **Thử nghiệm** | Prototype/pilot dùng để kiểm tra; không đồng nghĩa với acceptance |
| **Đang dùng** | Đang được dùng trong scope/project ghi rõ; không chứng minh đã được chấp nhận làm chuẩn Design System |
| **Ngừng dùng** | Không còn dùng trong scope đó; giữ provenance và liên kết replacement nếu có |

Ví dụ: Principle được **Đã chốt** nhưng component triển khai **Thử nghiệm**; asset được **Đang dùng** trong một project nhưng decision Design System vẫn **Đang nghiên cứu**; candidate **Tạm chấp nhận** nhưng chưa triển khai. Khi chưa có implementation, trục B là “không áp dụng”, không ép vào trạng thái.

Tình trạng work của experiment (planned/running/reviewed) là trường vận hành của Experiment record, không thêm status vào lifecycle tri thức.

## 6. Authority và quyền quyết định

| Vai trò | Quyền/trách nhiệm |
|---|---|
| **Người đề xuất** | Mở Research item/candidate/exception; mô tả vấn đề và scope; không tự biến proposal thành decision |
| **Người cung cấp evidence** | Có thể là tác giả, người dùng, reviewer, tool hoặc nguồn bên ngoài; provenance phải ghi rõ |
| **Người thực hiện experiment** | Ghi hypothesis, phương pháp, điều kiện và output; có thể báo kết quả theo tiêu chí, không tự tuyên bố acceptance |
| **Reviewer** | Kiểm tra phương pháp, bằng chứng, scope, rủi ro và độ khớp với claim; ghi review/giới hạn |
| **Chủ dự án** | Quyết định cuối về Design System; duyệt system-level decision, trạng thái Đã chốt, phạm vi canonical và release 1.0 |

Agent/Copilot/AI có thể hỗ trợ tìm/so sánh nguồn, lập bảng, tóm tắt, đề xuất giả thuyết, chạy test đã giao và soạn hồ sơ. AI có thể báo “tool pass/fail” theo output kỹ thuật và đề nghị trạng thái, nhưng chỉ ghi acceptance khi có xác nhận của người có thẩm quyền. AI không tự xác nhận acceptance, visual acceptance, canonical, principle chính thức hoặc release 1.0.

Không cần organizational chart ở P1.0. Nếu nhiều vai trò do cùng một người đảm nhiệm, record vẫn ghi vai trò thực hiện và người xác nhận để phân biệt trách nhiệm.

## 7. Evidence model

Mỗi claim quan trọng ghi nguồn theo một trong ba lớp, không trộn chúng:

| Lớp | Ví dụ | Cách ghi |
|---|---|---|
| **Evidence từ ZO Math** | source/config, implementation, audit, rendered output, usability result, user/owner approval, project history | Ghi URI/path, locator, project/medium, ngày/commit/version/hash nếu có, điều evidence chứng minh và giới hạn |
| **Evidence bên ngoài** | nghiên cứu, tiêu chuẩn, guideline, case study | Ghi citation/URL, tác giả/tổ chức, ngày/version, claim cụ thể được dùng và giới hạn áp dụng |
| **Suy luận** | kết luận do kết nối nhiều nguồn hoặc diễn giải của nhóm | Ghi rõ là inference; nêu các evidence đầu vào, bước suy luận và uncertainty; không giả làm lời nguồn |

**Evidence strength** có thể giữ ba mức của P0.3:

- **Mạnh:** trực tiếp và phù hợp với claim hẹp đang đánh giá.
- **Vừa:** hỗ trợ một phần, hoặc có giới hạn về scope/phiên bản/phương pháp.
- **Yếu:** gián tiếp, thiếu provenance, chưa kiểm chứng hoặc chỉ là gợi ý.

Mức mạnh gắn với từng claim/evidence link, không gắn chung vào toàn bộ record. Luôn ghi “điều này chứng minh” và “điều này không chứng minh”. Ví dụ: source/config có thể là evidence **mạnh** cho “CSS này được cấu hình/nạp”, nhưng **yếu** cho “lựa chọn này tốt cho người học”. Evidence strength **không phải** status và không tự nâng candidate lên Tạm chấp nhận/Đã chốt.

## 8. Research record schema

Dùng một record cho RQ hoặc VQ; loại câu hỏi là field, không cần hai template khác nhau.

```yaml
id: RQ-DS-R1-001
title: "<tên ngắn>"
type: RQ # RQ | VQ
program: R1
question: "<một câu hỏi có thể nghiên cứu/kiểm chứng>"
why: "<vì sao câu hỏi quan trọng>"
scope:
  products: ["<project hoặc all-design-system>"]
  media: ["<web, PDF, graph, video...>"]
status: "Đang nghiên cứu"
owner: "<người phụ trách>"
evidence:
  - id: EVID-DS-001
    class: "ZO Math" # ZO Math | External | Inference
    source: "<path/URI + locator>"
    version_or_date: "<nếu có>"
    claim_supported: "<điều nguồn thực sự hỗ trợ>"
    limitation: "<điều không chứng minh>"
    strength: "vừa" # mạnh | vừa | yếu
method: ["<phân tích, test, phỏng vấn...>"]
findings: []
limitations: []
provisional_conclusion: "<để trống khi chưa có>"
related_candidates: []
related_experiments: []
related_decisions: []
review:
  reviewer: null
  reviewed_on: null
  next_review_condition: "<trigger hoặc mốc>"
```

Research item có thể chứa nhiều evidence entries; chỉ tạo source note riêng khi nguồn có khả năng được tái sử dụng/diễn giải lâu dài theo quy trình `_research`. Kết luận tạm luôn phân biệt với trích dẫn nguồn.

## 9. Experiment record schema

```yaml
id: EXP-DS-R1-001
title: "<tên thử nghiệm>"
research_item: "RQ-DS-R1-001"
hypothesis: "<dự đoán có thể bị bác bỏ>"
status: "planned" # planned | running | reviewed | cancelled
scope:
  project: "<project>"
  media: "<medium>"
  audience: "<đối tượng>"
variants:
  - id: "A"
    description: "<mô tả>"
  - id: "B"
    description: "<mô tả>"
reference_or_control: "<nếu có; nêu rõ không có nếu không dùng>"
test_content: "<nội dung/kịch bản giữ ổn định để so>"
criteria:
  - "<tiêu chí và cách đo/quan sát>"
participants_or_reviewers: "<đối tượng, vai trò, cỡ mẫu nếu phù hợp>"
method: "<quy trình, thiết bị, môi trường, phiên bản>"
outputs:
  - "<path/URI + version/hash>"
results: []
issues_and_limits: []
conclusion: "<kết luận theo tiêu chí; không phải sở thích chung>"
supported_or_refuted: ["<HYP/CAND/DEC IDs>"]
review:
  reviewer: "<người>"
  acceptance: "not-assessed" # not-assessed | accepted-for-test | rejected | inconclusive
  notes: "<giới hạn; acceptance sản phẩm nếu có phải được ghi riêng>"
```

Không kết luận “nhìn thích hơn nên chốt”. Nếu có đánh giá chủ quan, ghi người đánh giá, câu hỏi, điều kiện, tiêu chí và xem đó là một evidence stream; so sánh phải giữ nội dung/kịch bản/medium phù hợp và nêu giới hạn.

## 10. Decision record schema

```yaml
id: DEC-DS-001
title: "<quyết định ngắn>"
status: "Đang nghiên cứu"
decision_statement: "<câu quyết định, hoặc 'chưa quyết định'>"
scope:
  products: ["<project hoặc toàn hệ thống>"]
  media: ["<medium>"]
  effective_version: "<nếu áp dụng>"
rationale: "<lý do>"
evidence:
  - "<EVID ID; phân biệt ZO Math / External / Inference>"
alternatives:
  - "<phương án và lý do giữ/bác bỏ/chưa đủ căn cứ>"
tests: ["<EXP/VQ IDs hoặc lý do không cần>"]
accessibility_and_cross_medium: "<tác động/đánh giá hoặc chưa biết>"
unresolved_risks: []
implementation_refs: ["<path/asset/component/version>"]
confirmed_by: null
confirmed_on: null
review_condition: "<điều kiện xem xét lại>"
supersedes: null
superseded_by: null
```

Record này chỉ được tạo khi có decision cần truy vết. Không cần chuyển toàn bộ 34 DES P0.3 thành decision records; các ID `DES-*` giữ nguyên là lịch sử ứng viên Pha 0.

## 11. Exception record schema

```yaml
id: EXC-DS-001
title: "<ngoại lệ ngắn>"
status: "Đang nghiên cứu"
base_decision_or_rule: "DEC-DS-001"
scope:
  project: "<project>"
  media: "<PDF/video/graph/...>"
  assets_or_pages: ["<locator>"]
reason: "<nhu cầu chức năng/medium>"
evidence: ["<EVID IDs>"]
impact_and_risks: "<tác động tới hiểu nghĩa, accessibility, coherence>"
approved_by: null
approved_on: null
implementation_refs: ["<path/version>"]
review_condition: "<ngày, release hoặc trigger>"
replacement_or_expiry: null
```

Ngoại lệ không sửa ngầm rule gốc. Nếu nó cho thấy rule không còn phù hợp, mở decision/research item mới; ngoại lệ hiện tại vẫn giữ scope và lịch sử.

## 12. Provenance model cho asset/implementation

Mỗi asset hoặc implementation được tham chiếu bằng record/section có các trường chung:

| Trường | Nội dung |
|---|---|
| `asset_id` / `implementation_id` | ID ổn định khi cần tham chiếu nhiều nơi |
| `kind` | logo, font, palette, SVG, TikZ style, CSS, Manim, PDF template, generated asset, audio/video asset… |
| `role` và `classification` | source, generated output, derivative, snapshot, experiment, production implementation |
| `source_of` / `derived_from` | URI/path/ID nguồn; ghi nhiều nguồn nếu có |
| `scope` | project, medium, page/use case |
| `version_or_date` | version/commit/ngày; ghi “không biết” nếu thiếu |
| `integrity` | hash/checksum khi phù hợp; không thay thế provenance |
| `generator` | tool/version/command/config nếu là output sinh |
| `status` | status Trục A của quyết định liên quan và status Trục B của implementation/use, lưu riêng |
| `evidence_and_limits` | điều asset/code chứng minh và không chứng minh |
| `approval` | người, phạm vi, ngày và bằng chứng acceptance nếu có |
| `links` | RQ/VQ, EXP, DEC, EXC, replacement/supersession |

**Phân loại quan trọng:**

- **Source:** nguồn có thẩm quyền cho output cụ thể; provenance phải chỉ ra lý do gọi là source.
- **Generated output:** kết quả từ source/tool/config; ghi generator/version và receipt/hash nếu có.
- **Derivative:** được biến đổi từ asset khác; liên kết upstream.
- **Snapshot:** bản chụp theo thời điểm; không tự trở thành source mới.
- **Experiment:** prototype/asset phục vụ kiểm tra; implementation status là Thử nghiệm.
- **Production implementation:** đang được dùng trong scope xác định; không đồng nghĩa Design System đã duyệt.

Quy tắc này áp dụng cho logo, font, palette, SVG/TikZ, CSS, Manim, PDF template và audio/video. Không đổi tên hoặc hợp nhất asset hiện có trong P1.0.

## 13. Deprecation và supersession

- Không xóa decision, evidence hay provenance cũ.
- Khi decision cũ bị thay: tạo DEC mới; ghi `supersedes`/`superseded_by`, lý do, scope và ngày có hiệu lực. Decision cũ giữ lại status lịch sử **Đã chốt** kèm trạng thái superseded; không viết lại thành chưa từng được chấp nhận.
- Khi implementation ngừng dùng: đổi riêng trục B sang **Ngừng dùng**, ghi asset thay thế/migration nếu có; decision gốc có thể vẫn còn hiệu lực.
- Khi candidate bị bác bỏ: status tri thức là **Loại bỏ**, kèm rationale; đây không phải deprecation.
- Nếu chưa có replacement, ghi rõ “không có thay thế” và giữ nguyên links/history.
- Migration chỉ được đề xuất trong decision mới, theo scope được duyệt; P1.0 không migration bất kỳ file nào.

## 14. ID/naming conventions

Đề xuất prefix ngắn, duy nhất trong phạm vi Design System:

| Loại | Mẫu ID | Ví dụ |
|---|---|---|
| Chương trình | `R<n>` | `R1` |
| Câu hỏi | `RQ-DS-R<n>-<NNN>` | `RQ-DS-R1-001` |
| Validation question | `VQ-DS-R<n>-<NNN>` | `VQ-DS-R4-001` |
| Observation | `OBS-DS-R<n>-<NNN>` | `OBS-DS-R3-001` |
| Hypothesis | `HYP-DS-R<n>-<NNN>` | `HYP-DS-R8-001` |
| Candidate | `CAND-DS-R<n>-<NNN>` | `CAND-DS-R4-001` |
| Experiment | `EXP-DS-R<n>-<NNN>` | `EXP-DS-R6-001` |
| Decision | `DEC-DS-<NNN>` | `DEC-DS-001` |
| Exception | `EXC-DS-<NNN>` | `EXC-DS-001` |
| Principle | `PRIN-DS-<NNN>` | `PRIN-DS-001` |
| Evidence entry | `EVID-DS-<NNN>` | `EVID-DS-001` |
| Asset/implementation (khi cần) | `AST-DS-<NNN>` / `IMP-DS-<NNN>` | `AST-DS-001` |

Quy ước:

- ID là định danh ổn định, không đổi khi đổi tiêu đề hoặc vị trí file; file name có thể có slug dễ đọc.
- Số thứ tự tăng dần, không tái sử dụng ID đã bỏ.
- Giữ nguyên RQ-003 và mọi ID `DES-*` hiện có; không rename hoặc giả định chúng thuộc scheme mới.
- Có thể dùng một RQ/VQ hiện tại thay vì tạo câu hỏi trùng; liên kết nhiều chương trình nếu scope giao nhau.
- Chưa cần cấp ID riêng cho mọi nguồn nếu citation/path + locator ổn định đã đủ; cấp EVID ID khi cần tham chiếu lại qua nhiều hồ sơ.

## 15. Quan hệ với `_research`

P1.0 đề xuất **mở rộng nhẹ từ `_research`**, không tạo kho nghiên cứu song song:

1. Dùng nguyên `00_inbox`, `10_questions`, `20_sources`, `30_concepts`, `40_design_cases`, `50_principles`, `90_syntheses` và `_templates` theo vai trò mô tả trong README.
2. Research item RQ/VQ thuộc `10_questions`; source có thể tái sử dụng thuộc `20_sources`; concept bền hơn thuộc `30_concepts`; synthesis theo thời điểm/phạm vi thuộc `90_syntheses`.
3. `40_design_cases` chỉ nhận các trường hợp thiết kế thực tế có ý nghĩa giáo dục và provenance đủ để học từ quyết định/kết quả; không biến mọi CSS change hoặc thử nghiệm nhỏ thành design case.
4. `50_principles` chỉ nhận pattern lặp lại qua thực hành và bằng chứng, phù hợp quy trình README; một ý tưởng hoặc một sản phẩm đơn lẻ chưa đủ.
5. Research Question/hypothesis không đồng nghĩa với Decision. Decision records cần nơi riêng có thể truy vết và cập nhật lịch sử; **đề xuất sau P1.0** là bổ sung một vùng `60_decisions/` trong `_research` nếu chủ dự án duyệt, thay vì lập root Design System độc lập. Cập nhật README/templates trước khi dùng; không tạo thư mục hay di chuyển hồ sơ trong P1.0.
6. Các mẫu Research/Experiment/Decision/Exception trong P1.0 là schema đề xuất để được xem xét; khi ratified, có thể đưa mẫu tối thiểu vào `_research/_templates/` thay vì giữ bản sao dài hạn ở nhiều nơi.
7. Chỉ ghi nội dung có khả năng sống lâu, theo nguyên tắc README; production là dòng chính, nghiên cứu không làm gián đoạn sản xuất. Nếu có dữ liệu người tham gia, tuân thủ lưu ý đạo đức hiện hành và quy trình phù hợp.

Như vậy decision log có thể có một vùng riêng **bên trong** research memory, không phải một hệ authority song song. Các liên kết RQ/EXP/DEC/PRIN là nguồn nối; tránh copy cùng nội dung giữa synthesis, question, audit và decision record.

## 16. Quan hệ với `_audit`

- `_audit` là nơi chứa báo cáo, receipt, preview, log và evidence tạm thời theo quy trình repository; không phải source thực thi hoặc nơi lưu kho vĩnh viễn mặc định.
- Hồ sơ nghiên cứu/decision lâu dài nên ở `_research` theo cấu trúc được duyệt; chỉ tham chiếu audit/output bằng relative path, locator, phiên bản/commit/hash khi có.
- Không copy toàn bộ output/binary vào research record nếu một tham chiếu ổn định và integrity metadata là đủ.
- Nếu một audit/output cần giữ lâu nhưng vòng đời `_audit` hiện hành không cho phép giữ tại đó, trước hết xác định nơi lưu trữ phù hợp và được duyệt; không tự di chuyển trong P1.0.
- Khi dùng receipt/test result, ghi rõ tool/version, scope, lệnh hoặc cấu hình, ngày và claim hẹp mà nó hỗ trợ. Test pass không tự chứng minh visual/design acceptance.
- `_audit` bị `.gitignore` loại khỏi Git trong hiện trạng; không stage/commit nội dung audit, không coi path cục bộ là bằng chứng được phát hành lâu dài.

## 17. Human vs automation

| Tool/AI có thể hỗ trợ | Tool/AI không được tự tuyên bố |
|---|---|
| Tìm nguồn theo scope, so sánh phiên bản/hash, tạo inventory và bảng đối chiếu | Thương hiệu là “đúng” hoặc phương án thiết kế là tốt nhất |
| Đo, lint, test, render theo yêu cầu/phạm vi đã duyệt | Prototype được chấp nhận hoặc đã qua visual acceptance |
| Phát hiện divergence, kiểm tra token/format, sinh receipt và báo lỗi | Tính canonical/toàn hệ thống từ code, tên file hoặc sự lặp lại |
| Tóm tắt evidence, tách quote/source/inference và liệt kê giới hạn | Status Đã chốt nếu chưa có chủ dự án xác nhận |
| Soạn record/template và đề xuất câu hỏi/experiment | Release Design System 1.0 hoặc phê duyệt thay cho người có thẩm quyền |

Con người chịu trách nhiệm xác nhận chất lượng, ý nghĩa Toán/sư phạm, usability/accessibility, acceptance và quyền quyết định. Automation hỗ trợ kiểm tra có thể mã hóa; không thay người duyệt những thuộc tính cần phán đoán.

## 18. Decision gates

Gate tương ứng với mức ảnh hưởng; không buộc mọi record chạy cùng một checklist.

### Low-impact / implementation detail cục bộ

Tối thiểu xem xét:

- scope/project và lý do;
- rule/source hiện có có liên quan;
- evidence hoặc test kỹ thuật phù hợp;
- ảnh hưởng phụ thuộc và khả năng rollback;
- người review/owner cục bộ nếu thay đổi tác động sản phẩm.

Nếu chỉ là sửa kỹ thuật không làm đổi semantics/design intent, không cần tạo system-level DEC; vẫn tuân workflow kỹ thuật của repository.

### System-level decision

Trước khi **Đã chốt**, decision record phải nêu:

- decision statement và rationale;
- scope, medium, sản phẩm và version có hiệu lực;
- evidence ZO Math, evidence bên ngoài nếu dùng, và inference được tách riêng;
- alternatives đã cân nhắc và lý do;
- tests/review phù hợp; accessibility/readability khi liên quan;
- cross-medium impact, exceptions và unresolved risks;
- implementation/provenance và điều kiện xem xét lại;
- xác nhận tường minh của chủ dự án.

Không yêu cầu mọi quyết định system-level phải có user study hoặc external research; người review phải ghi vì sao phương pháp cần thiết/không cần thiết. **Tạm chấp nhận** có thể dùng cho pilot có scope và điều kiện review, nhưng không được quảng bá thành canonical.

## 19. Workflow tối thiểu từ câu hỏi đến quyết định

```text
Research item (RQ/VQ)
  ↓ (khi cần)
Evidence collection: ZO Math / External / Inference
  ↓
Hypothesis hoặc Design Candidate
  ↓ (khi cần)
Experiment / Validation
  ↓
Review: claim, limits, scope, risk, accessibility/cross-medium
  ↓
Tạm chấp nhận để thử / tiếp tục nghiên cứu / Loại bỏ
  ↓ (chỉ khi cần có quyết định bền)
Decision gate phù hợp
  ↓
Đã chốt trong scope / Loại bỏ / tiếp tục nghiên cứu
  ↓
Implementation status theo trục riêng + provenance
  ↓
Review lại khi trigger, thay đổi scope hoặc bằng chứng mới
```

Không phải mọi RQ đều cần experiment hoặc DEC. Một validation question có thể kết thúc sau test. Một implementation detail nhỏ có thể dùng workflow engineering hiện hành mà không tạo principle. Một decision có thể được phê duyệt trước khi triển khai; một implementation đang chạy không bắt buộc có system-level approval nếu nó chỉ thuộc project scope.

## 20. Những phần governance chưa nên chốt ở P1.0

- Cấu trúc thư mục cuối cùng, ngoài đề xuất giữ `_research` làm nơi gốc và cân nhắc `60_decisions/`.
- Bộ status cho mọi loại record/asset; P1.0 chỉ đề xuất maturity axis và implementation axis tối thiểu.
- Ranh giới giữa Principle, Specification/Rule và component contract; cần thử qua một vài nghiên cứu trước khi chuẩn hóa schema.
- Authority ngoài vai trò mặc định của chủ dự án; chưa lập org chart hay hội đồng.
- Evidence-strength rubric chi tiết theo từng phương pháp/ngành.
- Retention, privacy, consent và lưu trữ dài hạn cho user research; tuân thủ chính sách/đạo đức hiện hành trước khi thu thập dữ liệu.
- Kỹ thuật số hóa registry, máy parse, CI checks, schema validation hoặc tự động publish.
- Mức bằng chứng tối thiểu bắt buộc cho mọi loại decision; gate cần tương xứng với impact.
- Nội dung/rationale cụ thể của bất kỳ quyết định thiết kế nào, bao gồm 34 DES P0.3.

## 21. Cách sử dụng ngay cho P1.1 — R1

P1.1 nên bắt đầu bằng R1 theo P0.4 nhưng giữ đúng nguyên tắc `_research`: nghiên cứu phát triển cùng thực hành, không làm gián đoạn sản xuất và không biến giả thuyết thành kết luận.

### Hồ sơ cần tạo khi P1.1 thực sự bắt đầu

1. Dùng một **Research item** cho R1 (hoặc cập nhật RQ hiện có nếu câu hỏi thực chất trùng; không tạo bản sao). Ghi mục tiêu, câu hỏi, scope sản phẩm/medium, owner, status và điều kiện xem xét lại.
2. Nếu cần nhiều câu hỏi phân biệt, tạo các RQ/VQ liên kết dưới chương trình R1; không nhét mọi chủ đề vào một câu hỏi rộng.
3. Tạo **source note** trong `20_sources` chỉ cho nguồn được đọc có khả năng tái sử dụng lâu dài; không chép toàn bộ tài liệu đầu vào vào R1 record.
4. Ghi observation/hypothesis như các mục có ID hoặc liên kết rõ; đánh dấu inference/uncertainty để không biến chúng thành tiếng nói của nguồn.
5. Tạo Experiment record chỉ khi có một test/phỏng vấn/so sánh thực sự cần phương pháp, tiêu chí và output để truy xuất.
6. Tạo Decision record khi có một quyết định cụ thể cần phê duyệt, nhất là khi ảnh hưởng toàn hệ thống hoặc sẽ dẫn tới quy tắc/implementation bền. Không cần DEC chỉ để tổng hợp hiện trạng.

### ID và evidence trong R1

- Chương trình có ID `R1`; câu hỏi mới dùng `RQ-DS-R1-001`, validation dùng `VQ-DS-R1-001`, observations/hypotheses dùng prefix tương ứng.
- Giữ nguyên `RQ-003`; liên kết nó tới R1 nếu câu hỏi cụ thể trong P1.1 thực sự phát triển từ nó, không đổi ID hoặc ép nó sang status mới.
- Với mỗi evidence: ghi path/URL + locator, ngày/version/commit/hash nếu có, project/medium, loại ZO Math/External/Inference, claim được hỗ trợ, giới hạn và strength cho claim đó.
- Lưu audit/output dưới `_audit` chỉ theo vòng đời repository; trong research record lưu đường dẫn/locator và provenance cần thiết, không copy mặc định.

### Nơi conclusion tạm lưu

Kết quả làm việc tạm nằm trong Research item/synthesis theo thời điểm; nếu có một design change có ý nghĩa giáo dục, tạo design case khi đủ điều kiện README. Không tạo principle chỉ từ một cuộc phỏng vấn, một tài liệu hoặc một prototype. Principle chỉ được promote khi pattern lặp lại qua thực hành và có bằng chứng.

### Ngăn R1 thành “brand manifesto” thiếu provenance

- Mỗi mệnh đề viết tách thành **claim**, **evidence**, **inference**, **hypothesis** hoặc **open question**.
- Câu trích/ý nguồn có citation; interpretation ghi rõ người diễn giải và giới hạn.
- Mọi phát biểu về “ai”, “vì sao”, “phục vụ ai” ghi nguồn hoặc nêu là giả thuyết cần feedback.
- Bản tổng hợp phải giữ evidence trái chiều, scope và ngày/version; không chỉ giữ câu chữ thuận ý.
- Chỉ đưa claim đã qua quyết định vào decision record; không dùng bản tuyên ngôn như nguồn quyết định nếu chưa có hồ sơ/phê duyệt.

## 22. Tiêu chí kết thúc

P1.0 được xem là đủ để khởi động nghiên cứu tiếp khi:

1. Có tập loại hồ sơ nhỏ, ánh xạ được RQ/VQ, observations, hypothesis, candidate, experiment, decision, principle/rule, implementation, exception và deprecation.
2. Maturity status được tách khỏi implementation/use; “Tạm chấp nhận”, “Đã chốt” và “Loại bỏ” có nghĩa không nhập nhằng.
3. Quyền đề xuất/evidence/review/acceptance/decision được phân biệt; chủ dự án là người xác nhận cuối của Design System.
4. Evidence model tách ZO Math, external và inference, đồng thời ghi claim/limits/strength riêng.
5. Có schema đủ dùng cho Research, Experiment, Decision, Exception và provenance.
6. Có đường dẫn kế thừa `_research`, quy tắc tham chiếu `_audit`, không di chuyển hoặc nhân đôi hồ sơ trong P1.0.
7. Có workflow/gates tương xứng impact và hướng dẫn áp dụng R1 mà không tự nghiên cứu nội dung R1.
8. Chủ dự án review và chấp nhận hoặc yêu cầu điều chỉnh khung trước khi dùng nó làm quy chuẩn cho P1.1.

P1.0 chỉ là đề xuất để chuẩn bị P1.1; **không tự phê duyệt chính khung này**. Không có thay đổi nào đối với Design System, production hoặc hồ sơ research hiện hữu được thực hiện trong bước này.
