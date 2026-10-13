# Mâu thuẫn và khoảng trống thực sự

## Kết luận lọc

Không có gap G1 ngăn việc viết Draft 0.1 nếu bản thảo dùng nhãn owner-confirmed / research / candidate / historical và giữ các quyết định cụ thể ở trạng thái mở. Các gap dưới đây có ý nghĩa với mức đề xuất hoặc bước nghiệm thu tiếp theo; không phải danh sách mọi câu hỏi nhỏ.

| ID | Loại / mức | Mâu thuẫn hoặc gap | Evidence và giới hạn | Tác động / cách xử lý trong Draft 0.1 |
|---|---|---|---|---|
| CG-01 | Conflict / G2 | **Màu:** đỏ `#EF5350` lặp rộng, nhưng graph v0.2 dùng strong `#BF4240`; role yellow/neutral/teal cũng khác giữa graph, web, media và prototypes. | P0.3 DES-AB-04..06, DES-D-02/05; khác biệt có thể do scope, phiên bản hoặc vai trò, chưa có mapping toàn hệ. | Ghi inventory và candidate direction; không chọn giá trị primary cuối hoặc hòa giải role bằng suy luận. |
| CG-02 | Conflict / G2 | **Typography:** web code đặt Be Vietnam Pro trước Manrope dù comment nói ưu tiên Manrope; PDF dùng STIX; media guideline nêu Be Vietnam Pro/STIX Math. | P0.3 DES-AB-07..09; config chứng minh khai báo, không chứng minh render, fallback hay cùng vai trò. | Draft có thể đề xuất role matrix; để family/fallback cụ thể ở trạng thái candidate. |
| CG-03 | Provenance gap / G2 | **Logo/identity:** nhiều biến thể; config tham chiếu một logo; asset `master`/`final` không xác lập authority; motif dấu nhấn chỉ là proposal. | P0.2 P0-0004/P0-0034; P0.3 DES-AB-01..03/10; chưa có visual comparison/approval đủ. | Không chọn master, redesign hoặc ghi motif thành nhận diện chính thức. |
| CG-04 | Visual evidence gap / G2 | **P2.1–P2.3:** A gần hình dung hiện tại của owner nhất trong bộ A/B/C; A+ mở rộng bằng 8 specimens nhưng vẫn là hypothesis, không có owner calibration sau A+. | P2.1–2.3 ghi nội bộ visual checks; owner nói evidence P2.1/2 quá ít; công thức mock ban đầu không đủ chính xác; A+ chưa chốt. | Cho phép nêu A+ như early visual probe và kế thừa insight có điều kiện; không dùng như baseline chuẩn. |
| CG-05 | Accessibility/acceptance gap / G2 | Contrast, grayscale, semantic HTML, captions/alt và screen-reader/keyboard chưa có audit đầy đủ xuyên medium. | P0.3 ghi không render/đo contrast; P1.3c/d xác nhận semantic HTML variation và một số accessibility mappings còn mở; P2 chỉ có visual specimens. | Ghi acceptance cần có trước phát hành; không tuyên bố WCAG/conformance hoặc accessible by design. |
| CG-06 | User evidence gap / G2 | OCONF xác định đối tượng chủ đích và ưu tiên, không xác lập nhu cầu, hành vi, segmentation, usability hay willingness to pay. | P1.1c và RQ-003 giới hạn rõ; ER-02 chưa thực hiện. | Mô tả audience intent; không viết persona, customer hierarchy hoặc claim thị trường. |
| CG-07 | Mathematical expression gap / G2 | Variation chưa typed rich roles như limit/undefined/discontinuity/critical point; geometry chưa có ontology chung cho nhiều relation; identifier label và explanation chưa tách ở source. | P1.3c direct-source read; P1.3d giữ gap open nhưng kết luận không chặn visual work. | Đưa role confirmed/candidate đúng scope; không phát minh semantic standard cho case chưa có evidence. |
| CG-08 | Delivery gap / G2 | Video vertical/subtitles/safe zones và social adaptations có ý định/tài sản nhưng workflow đại diện chưa xác minh. | P0.2/P0.3 manuals có phiên bản/scope khác; khảo sát video đại diện thấy horizontal Manim, chưa tìm thấy vertical/subtitle implementation trong package đó. | Draft nêu need for adaptation; không khẳng định output coverage/cross-platform consistency. |
| CG-09 | System governance gap / G2 | P1.0 có lifecycle/provenance proposal nhưng chưa được phê duyệt làm governance chính thức; không có authority/release/exception process đã chốt. | P1.0 tự ghi proposal; `_research` README là research memory practice, không phải governance Design System. | Dùng nguyên tắc provenance như recommendation/candidate; không gọi P1.0 là policy bắt buộc. |
| CG-10 | Implementation / G3 | Source/current output linkages, version/hash/receipt không hoàn chỉnh cho mọi logo, style, generated asset, video/social package. | P0.2/P0.3 inventory có snapshots/outputs và giới hạn truy lineage; chưa cần resolve hết để viết Draft 0.1. | Xử lý theo từng asset/pilot khi triển khai; Draft 0.1 chỉ nêu source index và provenance limits. |
| CG-11 | Implementation / G3 | Exact type scale, spacing, radius, token names, responsive breakpoints, audio loudness, motion timing. | Có một số cấu hình/prototype nhưng chưa có cross-domain decision/test. | Không kê thành quy tắc cuối trong Draft 0.1; chỉ đề xuất sau nghiên cứu miền hoặc implementation task cụ thể. |

## Những điểm trông như mâu thuẫn nhưng chưa được chứng minh là conflict

1. **Content-block colors và R1-G01:** block đỏ/vàng/xám mã hóa chức năng của khối nội dung trong hướng dẫn; “Nhiệm vụ/Ví dụ/Hỗ trợ” trong R1-G01 là họ kiến trúc nội dung. P0.3 DES-C-04/05 nói hai lớp chưa được chứng minh mapping trực tiếp, nên không tuyên bố một bên phủ định bên kia.
2. **Khác biệt giữa medium:** web/PDF/video có font, density, palette và output khác nhau. P0.4/P2.0 yêu cầu kiểm tra shared logic, không sameness; chỉ gọi conflict khi cùng role/scope nhưng khác rule mà không có rationale.
3. **P2 A và A+:** owner preference cho Direction A gần nhất là phản hồi trong exploration, không phải chốt A; A+ là phát triển giả thuyết sau đó, không phải owner-approved direction.
4. **R6 open gaps:** taxonomy chưa đầy đủ không phải blocker của visual exploration theo P1.3d; chỉ mở lại khi representative case thực sự bị semantic blocker.

## Ưu tiên xử lý sau Draft 0.1

1. Owner calibration có tiêu chí trên bộ specimen A+ hoặc phiên bản tiếp theo.
2. Test palette/type/layout theo nội dung giữ nguyên, gồm contrast, grayscale/print, mobile và glyph Toán/tiếng Việt.
3. Xác minh identity assets/provenance và ứng dụng nhỏ/nền khác nhau.
4. Chọn pilot accessibility/cross-medium trước khi promotion candidate thành specification.
5. Chỉ phát triển tokens/automation khi domain roles và quyết định dùng chung đã rõ.
