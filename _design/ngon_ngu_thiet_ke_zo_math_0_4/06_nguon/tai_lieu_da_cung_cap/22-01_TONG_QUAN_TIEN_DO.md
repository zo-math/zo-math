# ZO Math Design System — Consolidation 01

## Mục tiêu

Đây là gói tổng hợp staging để làm đầu vào cho **ZO Math Design System & Brand Language — Draft 0.1**. Gói nén bằng chứng P0–P2 theo domain, trạng thái, provenance và mức độ sẵn sàng; không phải bản thảo Design System và không thay thế các báo cáo nguồn.

## Tiến độ nghiên cứu được tổng hợp

| Giai đoạn | Đã có | Trạng thái cần giữ |
|---|---|---|
| P0 — Khảo cổ, evidence map, research map | P0.2 inventory 40 mục; P0.3 ghi 34 ứng viên DES trong sáu cụm; P0.4 đề xuất 12 Research Programs và phụ thuộc | Evidence về lịch sử/hiện trạng không tự tạo thẩm quyền; các DES không phải Decision |
| P1 — Brand Foundation (R1) | P1.1a–f; OCONF-01..11; ER-01; tổng hợp ứng viên và giới hạn claim | P1.1f được chủ dự án duyệt làm nền nghiên cứu để chuyển sang R2; đây không phải phê duyệt final wording/Decision |
| P1 — Brand Personality (R2) | P1.2a–e, gồm hiệu chỉnh trực tiếp của chủ dự án | Bốn formulation đã owner-calibrated; hồ sơ personality vẫn là candidate, không phải specification |
| P1 — Mathematical Expression (R6) | P1.3a–d; P1.3c đọc 13 source subsystem trực tiếp: graph 4, geometry 3, variation 6 | Đủ constraint candidate cho visual exploration; chưa có semantic token, Decision hay Design Principle |
| P2 — Visual exploration | P2.0 framework; P2.1 ba direction; P2.2 stress test; P2.3 A+ và 8 specimen | Early visual probes / exploratory experiments; chưa là candidate chuẩn, chưa có winner hay calibration sau A+ |

## Vì sao cần gói consolidation

P0–P2 đã tạo nhiều báo cáo theo từng câu hỏi và miền. P0.2/P0.3 cũng xác nhận repository chứa nhiều nhánh lịch sử, implementation, prototype và asset trùng lặp hoặc khác scope. Đọc từng báo cáo rời không đủ để người viết thấy ranh giới xuyên hệ thống. Gói này chuyển chúng thành một bản đồ điều hành duy nhất: nội dung nào có thể dùng trong Draft 0.1, nội dung nào chỉ được nêu như candidate, và nội dung nào phải để mở.

## Phạm vi và phương pháp

- Đối chiếu P0.2–P0.4; P1.0; các hồ sơ R1, R2, R6; P2.0–P2.3; `_research`; và nguồn triển khai đại diện theo miền.
- Dùng các báo cáo P0 làm inventory/provenance và các báo cáo P1/P2 làm tổng hợp có giới hạn; không coi chúng là chuẩn production.
- Các asset/output nhị phân được tính là bằng chứng tồn tại/provenance khi báo cáo nguồn xác nhận; gói này không tái render hoặc nghiệm thu thị giác.
- Ba nhánh khảo sát độc lập bổ sung đối chiếu Brand Foundation/personality/verbal, P2 probes, và video/audio/social. Khảo sát đại diện, không phải inventory toàn bộ file hoặc archive.
- Không thực hiện web research mới; ER-01 chỉ được dùng qua báo cáo đã có.

## Phân loại bằng chứng

1. **Owner-confirmed** — điều chủ dự án trực tiếp xác nhận là ý định/cách hiểu hiện tại; không đồng nghĩa hiệu quả, nhu cầu, final wording hay Decision.
2. **Research evidence** — phát hiện được hỗ trợ bởi nguồn chuyên môn hoặc source trực tiếp; chỉ áp dụng trong phạm vi và giới hạn nguồn.
3. **Hypothesis / candidate** — phương án/diễn giải đang được nghiên cứu, gồm P2.1–P2.3.
4. **Historical / implementation** — source, configuration, asset, output, snapshot hoặc pipeline đã/đang tồn tại; không tự thành chuẩn mới.

## Kết quả điều hành

- Có đủ đầu vào để viết một **Draft 0.1 ở cấp research synthesis**: đề xuất phần đủ cơ sở, gắn nhãn candidate cho phần chưa được kiểm chứng, và giữ các thông số cuối ở trạng thái mở.
- Không đủ cơ sở để phát hành Design System 1.0, chọn palette/font/logo cuối, tạo token hoặc áp migration.
- Maturity tổng thể cho Draft 0.1: **2/4**; một số miền nền tảng và ngôn ngữ Toán đạt **3/4**. Mức 4 không được gán cho miền nào trong gói này.
- Không có gap G1 ngăn cản việc viết Draft 0.1 nếu bản thảo tuân thủ các giới hạn trong [04](./04_MAU_THUAN_VA_KHOANG_TRONG.md), [06](./06_CANDIDATE_CO_THE_DE_XUAT.md) và [07](./07_KHONG_DUOC_MAC_DINH.md).

## Các tệp trong gói

| File | Vai trò |
|---|---|
| [02 — Bản đồ bằng chứng toàn hệ](./02_BAN_DO_BANG_CHUNG_TOAN_HE.md) | Tóm lược evidence theo đủ 18 miền và chỉ dẫn nguồn |
| [03 — Ma trận trạng thái và sẵn sàng](./03_MA_TRAN_TRANG_THAI_VA_SAN_SANG.md) | Maturity 0–4, ranh giới sử dụng trong Draft 0.1 |
| [04 — Mâu thuẫn và khoảng trống](./04_MAU_THUAN_VA_KHOANG_TRONG.md) | Chỉ giữ conflict/gap ảnh hưởng đề xuất hoặc phát hành |
| [05 — Hạt nhân đủ cơ sở](./05_HAT_NHAN_DA_DU_CO_SO.md) | Nền tảng và constraint có thể mang vào Draft 0.1 |
| [06 — Candidate có thể đề xuất](./06_CANDIDATE_CO_THE_DE_XUAT.md) | Phạm vi đề xuất cụ thể được phép theo từng miền |
| [07 — Không được mặc định](./07_KHONG_DUOC_MAC_DINH.md) | Ranh giới bắt buộc cho người viết |
| [08 — Gói bàn giao Draft 0.1](./08_GOI_BAN_GIAO_CHO_BAN_THAO_0_1.md) | Brief tự chứa để bàn giao cho mô hình viết bản thảo |

## Giới hạn

Tài liệu này không viết manifesto, mission statement, slogan, Principle, Decision hay specification. Đây là điểm dừng trước Draft 0.1; chỉ bắt đầu viết bản thảo khi được giao riêng. Không sửa source, `_research`, production hoặc asset; không render, migration, commit hay push. Các khác biệt được giữ với provenance thay vì hòa giải bằng suy luận.
