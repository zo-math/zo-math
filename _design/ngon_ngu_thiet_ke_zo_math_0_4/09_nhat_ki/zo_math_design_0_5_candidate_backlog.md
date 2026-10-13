# ZO Math Design 0.5 Candidate Backlog

> Backlog evidence để chuẩn bị thảo luận phiên bản kế tiếp. Đây không phải Design 0.5, không phải quyết định đã duyệt, và không sửa hay diễn giải lại quy tắc canonical 0.4. Mỗi candidate cần được xem xét riêng theo medium, phạm vi, nguồn và bằng chứng; không mục nào tự động được nhập vào phiên bản kế tiếp.

## Candidates

### CAND-VIDEO-001 — Segmentation phụ đề theo nội dung và thời gian

- **Evidence:** `VIDEO04-FB-007`, `VIDEO04-FB-011`; VF-001/VF-007; M8.2, 16 cue cho 3 narration segments trong fixture M4, video được người dùng duyệt.
- **Nguồn 0.4 liên quan:** ZO027; `04_ap_dung/02_video.md`; `02_quy_chuan/02_noi_dung_toan_hinh_bang.md`.
- **Đề nghị xem xét:** Có cần hướng dẫn video-specific về phân đoạn theo cụm nghĩa, đồng bộ cue và giới hạn đọc hay không.
- **Giới hạn:** Không suy ra mọi phụ đề phải một dòng; 0.4 hiện quy định hình thức văn bản và đủ thời gian đọc, không quy định segmentation.
- **Trạng thái:** Candidate for 0.5.
- **Kiểm tiếp theo cần thiết:** Nhiều đoạn narration với cue ngắn/dài, một dòng/nhiều dòng, nhiều cỡ màn hình; review người dùng vẫn cần thiết.

### CAND-VIDEO-002 — Semantic alignment giữa narration và visual

- **Evidence:** `VIDEO04-FB-012`; M8.5 `projects/m8_motion_test/plan/scenes.json`; `tests/test_motion.py`, `tests/test_scenes.py`; commit `b0fed3f501b97c92ac3a478bf5fd4ad3c349a6cf`.
- **Nguồn 0.4 liên quan:** Hướng dẫn video về phối hợp hình/lời đọc/khoảng dừng; ZO025.
- **Đề nghị xem xét:** Hướng dẫn một lượt rà narration ↔ visual intent/action và bảo toàn identity đối tượng xuyên biến đổi.
- **Giới hạn:** Schema/action validation không chứng minh hình diễn đạt đúng nghĩa; cần xem-nghe người và nhiều dạng bài.
- **Trạng thái:** Candidate for 0.5.
- **Kiểm tiếp theo cần thiết:** Thử nhiều video với biểu đồ, biến đổi công thức và cảnh đối chiếu; đánh giá cả đúng nghĩa và nhịp quan sát.

### CAND-VIDEO-003 — Quy tắc trục và ticks tại endpoint

- **Evidence:** `VIDEO04-FB-009`, `VIDEO04-FB-013`; `tests/regression/test_graph.py`; video graph fixture; commit `da26cf750c9fc1cb7a7b7bff37f42111f23f4b08`.
- **Nguồn 0.4 liên quan:** ZO021–ZO022; quy chuẩn đồ thị v0.2 trong phạm vi áp dụng được nêu.
- **Đề nghị xem xét:** Có nên quy định arrowhead/tick clearance như một hướng dẫn theo loại trục/medium hay không.
- **Giới hạn:** Đây là contract đã chốt trong ZO Video, không phải quy tắc 0.4 hiện hành; không khái quát sang mọi hệ trục hoặc graph.
- **Trạng thái:** Candidate for 0.5.
- **Kiểm tiếp theo cần thiết:** Thử nhiều miền, tick spacing, nhãn và loại trục trước khi chốt phạm vi.

### CAND-VIDEO-004 — Formula presentation theo medium

- **Evidence:** `VIDEO04-FB-014`; `src/zo_video/formulas.py`; `tests/test_formulas.py`; fixture `projects/m8_motion_test/plan/scenes.json`.
- **Nguồn 0.4 liên quan:** ZO027; `02_quy_chuan/02_noi_dung_toan_hinh_bang.md` mục “Công thức và lời văn”.
- **Đề nghị xem xét:** Có cần ví dụ/hướng dẫn trình bày video cho phân số dùng `\frac` và ngoặc co giãn `\left...\right` trong các biểu thức cần thiết.
- **Giới hạn:** Đây là validator video-specific; nguồn 0.4 yêu cầu công thức render, chưa quy định cú pháp này. Cần tránh từ chối biểu thức hợp lệ.
- **Trạng thái:** Candidate for 0.5.
- **Kiểm tiếp theo cần thiết:** Mở rộng test cases hợp lệ/không hợp lệ và review render ở cỡ dùng thực.

### CAND-VIDEO-005 — Hướng dẫn layout dọc và safe-area theo platform

- **Evidence:** `VIDEO04-FB-005`, `VIDEO04-FB-006`, `VIDEO04-FB-008`; `src/zo_video/design/layout.py`; regression layout/subtitle/identity; M8.1R/M8.3/M8.6.
- **Nguồn 0.4 liên quan:** `04_ap_dung/02_video.md`; `02_quy_chuan/03_thich_ung_phuong_tien.md`.
- **Đề nghị xem xét:** Làm rõ rằng video cần bố trí lại theo medium, tách vùng nội dung/phụ đề/identity và xác minh safe area theo platform.
- **Giới hạn:** Tọa độ normalized và slots của video profile không được đưa thành thông số chung cho 0.5.
- **Trạng thái:** Candidate for 0.5.
- **Kiểm tiếp theo cần thiết:** Kiểm tra các tỷ lệ/crop/platform mục tiêu và nội dung có graph/formula khác nhau.

### CAND-VIDEO-006 — Tiêu chí nghiệm thu audio/spoken presentation

- **Evidence:** `VIDEO04-FB-016`; VF-008; `E:/zo_math_video/docs/design/m8_7_audio_spoken_presentation_trial.md`; cặp baseline/trial M8.7 byte-identical, chưa có kết quả người dùng nghe.
- **Nguồn 0.4 liên quan:** `04_ap_dung/02_video.md` yêu cầu rõ lời, đúng thuật ngữ, có khoảng nghỉ và nghe trên thiết bị phổ thông; ZO026 là cue thử nghiệm.
- **Đề nghị xem xét:** Sau khi M8.7 được tiếp tục và người dùng nghe, cân nhắc checklist nghiệm thu theo thiết bị và quan hệ khoảng nghỉ–hình.
- **Giới hạn:** Chưa có bằng chứng nghe chủ quan; không đề nghị loudness target, fade, EQ, TTS, voice identity hay sonic logo từ trial hiện tại.
- **Trạng thái:** Candidate for 0.5.
- **Kiểm tiếp theo cần thiết:** Hoàn tất lượt nghe thực tế và cập nhật evidence trước khi đánh giá candidate; backlog này không tự tiếp tục M8.7.

### CAND-VIDEO-007 — Đánh giá motion cadence trên nhiều nội dung

- **Evidence:** `VIDEO04-FB-010`, `VIDEO04-FB-019`; `src/zo_video/design/motion.py`; `tests/test_motion.py`, `tests/regression/test_motion.py`; M8.5 commit `b0fed3f501b97c92ac3a478bf5fd4ad3c349a6cf`.
- **Nguồn 0.4 liên quan:** ZO025; hướng dẫn video về thời gian, chuyển động và quan sát.
- **Đề nghị xem xét:** Phân biệt vai trò chuyển động và nguyên tắc dành thời gian quan sát khỏi duration/easing cụ thể.
- **Giới hạn:** Một fixture và test budget không chứng minh cadence tổng quát hoặc trải nghiệm học.
- **Trạng thái:** Candidate for 0.5.
- **Kiểm tiếp theo cần thiết:** Thử nhiều nhịp lời đọc, dạng graph/transform và thời lượng cảnh; có người xem đánh giá.

## Không đưa thành candidate đã xác nhận

- **Motif:** Chưa render trong main scene; chỉ đăng ký như accent phụ (`VIDEO04-FB-015`). Cần nhiệm vụ thử và duyệt riêng.
- **Intro/outro:** Chưa có contract hoặc thử nghiệm (VIDEO04-FB-017); logo tĩnh M8.6 không phải bằng chứng cho một opening/closing sequence.
- **Accessibility nhiều thiết bị:** Chưa có kiểm đa thiết bị/platform hoặc kết luận compliance (VIDEO04-FB-018). Cần xác định phạm vi/tiêu chí trước.
- **Typography, palette, identity asset và semantic layout:** Có bằng chứng tích hợp/fixture M8.1–M8.6 (`VIDEO04-FB-001`–`005`), nhưng đây là ghi nhận tiếp nhận trong profile hiện tại, không tự phát sinh đề xuất thay đổi canonical 0.4.

## Ranh giới quyết định

1. Candidate chỉ là đầu vào để thảo luận và cần truy về hồ sơ `09_nhat_ki/phan_hoi_tich_hop_zo_video_0_4.md`.
2. Không tự sửa `02_quy_chuan/`, `03_du_lieu/quy_tac.json`, mẫu 0.4, package version hoặc specimen version dựa trên backlog.
3. Bất kỳ nội dung nào được chọn cho phiên bản kế tiếp phải qua quyết định có thẩm quyền, xác lập phạm vi áp dụng, nguồn và phép kiểm riêng. Tài liệu này không tuyên bố hoặc tạo Design 0.5.

## CAND-WEB-FIGURE-001 — Tách ảnh bìa khỏi nền khung và khỏi hình đọc trong bài

- Evidence: WEB04-FB-030, `_audit/zo_math_figure_profile_2026-10-08/`; profile
  nguồn `_design/web_2027_mau_dung_chung/figure-profile-candidate/`.
- Đề nghị: bìa dùng SVG trong suốt và khung tác giả chọn từ ba dạng × hai cỡ,
  sáu token sáng/tối; không tạo bảng tùy chọn người học mới. Hình trong bài
  giữ cỡ chữ tự nhiên, cuộn cục bộ, cùng vùng đọc với alt/chú thích/nhãn.
- Đồ thị: opt-in 0.4; giữ công thức/miền/điểm/lớp. Bố trí nhãn được kiểm tại
  cỡ thật, không chỉ đổi font rồi coi là đạt. Điểm rỗng trên bìa trong suốt
  còn cần mask đúng toán, chưa khái quát mẫu đóng điểm sang mọi dạng.
- Bảng: native HTML + MathML từ cùng JSON, không ảnh phóng to; giữ hai/ba
  hàng, cột loại, giới hạn một phía và lỗi chủ ý. Renderer cũ giữ tương thích.
- Trạng thái: kiểm kỹ thuật mẫu đạt, **chủ trì đã duyệt FB030 ngày 08/10/2026**;
  HTML G01 đã tích hợp theo FB031, kiểm 782/782 và chờ chủ trì xem tại
  `_audit/zo_g01_figure_integration_2026-10-08/`. Chưa quyết định đưa
  số đo khung hoặc profile này vào quy chuẩn 0.5.
- Kiểm tiếp: nghiệm thu HTML, hồi quy đủ dạng toán và bộ nối QMD, áp dụng thử
  G01 rồi đối sánh toàn trang. Không dùng bằng chứng này chứng nhận Video,
  PDF học liệu, G02 hoặc toàn bộ hệ thiết kế.

## WEB-FB033 — Hợp đồng nhân bản có receipt và guard canonical

- G01 HTML hình/bảng/tải PDF/drawer đã được chủ trì duyệt tới FB032. Nguồn dùng lại trong `_design/web_2027_mau_dung_chung/hop_dong_vung_doc.md`; không lấy 154 vùng/12 view/tám PDF làm con số chung.
- Ứng viên quy trình: receipt rõ hash/phạm vi/chủ trì; dựng nguồn độc lập audit, fail-closed khi lệch; không tự cập nhật mốc để cho PASS. Hiện thực G01 trong `scripts/zo_web_2027_g01_checkpoint.py`.
- Cần chứng minh tiếp ở G02 với toán và kiến trúc riêng, rồi hồ sơ phạm vi/di trú/quy chuẩn trước khi xin chốt 0.5. Không tự áp dụng hoặc nâng version trong lượt này.
