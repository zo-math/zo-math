# Hồ sơ phản hồi tích hợp ZO Video với Design 0.4

## Mục đích và ranh giới

Hồ sơ này chuyển bằng chứng M8.1–M8.6 từ repo ZO Video về nhật ký Design 0.4 để truy xét khi chuẩn bị phiên bản kế tiếp. Đây là phản hồi sản phẩm, không phải quy chuẩn mới, quyết định sửa nội dung canonical 0.4 hay Design 0.5.

- Nguồn Design: bộ bàn giao 0.4.2, mẫu thiết kế 0.4 tại `_design/ngon_ngu_thiet_ke_zo_math_0_4`.
- Repo nhận phản hồi: `E:/zo_math_video`.
- Repo video: branch `main`, HEAD tại thời điểm chuyển giao `96b9c30a2fec22058c006047decc77b9b13f3bff`.
- Audit gốc: `E:/zo_math_video/docs/design/design_0_4_video_coverage_audit.md`.
- Feedback log gốc: `E:/zo_math_video/docs/design/zo_math_0_4_video_feedback.md`.
- Profile tích hợp: `E:/zo_math_video/docs/design/zo_math_0_4_video_profile.md`.
- M8.7 đang tạm dừng theo yêu cầu. Ghi chú audio hiện có chỉ được nêu để chỉ ra khoảng trống, không được xem là một trial đã nghiệm thu hay một phản hồi M8.1–M8.6 đã hoàn tất.
- Mọi đường dẫn fixture, source, test và commit bên dưới tính từ gốc repo `E:/zo_math_video`, trừ khi ghi khác.

## Quy ước trạng thái và bằng chứng

Trạng thái dưới đây mô tả mức độ bằng chứng cho phản hồi video, không sửa trạng thái nguồn ZO001–ZO030 và không biến hiện thực video thành quy tắc Design 0.4.

- **Observation** — ghi nhận phạm vi hoặc khoảng trống; chưa đủ bằng chứng đánh giá.
- **Experimental** — đã hiện thực/thử trong video nhưng chưa được xác nhận rộng.
- **Provisionally accepted** — hướng triển khai của fixture đã được người dùng chấp nhận để tiếp tục, không phải chuẩn chung.
- **Candidate for 0.5** — có thể đưa vào backlog xem xét; không phải quyết định hay nội dung 0.5.
- **Rejected** — đã có quyết định loại bỏ; không có mục nào trong hồ sơ này tự được gán trạng thái đó.

## A. Đã xác nhận khi áp dụng

### VIDEO04-FB-001 — Kế thừa palette nhận diện, giữ riêng semantic roles

- **Nguồn Design 0.4:** `03_du_lieu/quy_tac.json` ZO001; `02_quy_chuan/01_mau_logo_chu.md` mục “Màu”.
- **Vấn đề phát hiện:** Cần dùng màu nhận diện 0.4 mà không làm các ánh xạ vai trò màu thử nghiệm trở thành quy tắc canonical.
- **Bằng chứng từ ZO Video:** Palette 23 mã và các màu neo được gom vào `src/zo_video/design/colors.py`; semantic roles là profile `EXPERIMENTAL`, không nằm rải trong scene.
- **Fixture/video/test:** `projects/m4_article_to_narration/`, `projects/m8_motion_test/`; `tests/regression/test_color.py`; commit M8.4 `b18bc001ca13dbd6d98e6a2e008b5a666ad8d5a0`, ghi nhận duyệt `8d96d1fb0c1689a2d80e2386a5cda0f6487a3d54`.
- **Quyết định hiện tại:** Chấp nhận việc giữ palette 0.4 trong video profile; không khẳng định mọi semantic role/màu nền tối đã được chốt toàn hệ.
- **Mức độ tin cậy:** Cao cho palette và việc gom nguồn; trung bình cho độ phù hợp của từng role trên các nội dung khác.
- **Phạm vi áp dụng:** Profile video hiện tại và fixture đã thử; không suy rộng sang web, PDF hay mọi video.
- **Đề xuất cho 0.5:** Giữ rõ ranh giới giữa màu nhận diện đã xác nhận và ánh xạ role theo medium; chỉ mở rộng role sau khi có bằng chứng đa nội dung.
- **Trạng thái:** Provisionally accepted.

### VIDEO04-FB-002 — Typography chữ và toán theo role, không chuyển nguyên đơn vị

- **Nguồn Design 0.4:** ZO019; `02_quy_chuan/01_mau_logo_chu.md` mục “Chữ”; `02_quy_chuan/02_noi_dung_toan_hinh_bang.md` mục công thức.
- **Vấn đề phát hiện:** Cần phân biệt chữ tiếng Việt với công thức, đồng thời không bê px/pt của medium khác sang Manim.
- **Bằng chứng từ ZO Video:** Role chữ dùng Be Vietnam Pro; công thức dùng MathTex/STIX Two Math; cỡ và hệ số fit tập trung trong `src/zo_video/design/typography.py` và vẫn `EXPERIMENTAL`.
- **Fixture/video/test:** M4 và M8 motion test; `tests/regression/test_typography.py`, `tests/test_manim_compiler.py`; M8.4 `b18bc001ca13dbd6d98e6a2e008b5a666ad8d5a0`, duyệt `8d96d1fb0c1689a2d80e2386a5cda0f6487a3d54`.
- **Quyết định hiện tại:** Kế thừa phân cấp theo role và kiểm đầu ra thực; chưa xác lập cỡ chữ, ngưỡng fit hay font strategy thành chuẩn cho mọi video.
- **Mức độ tin cậy:** Cao về cách tổ chức role và kiểm tra compiler; trung bình về readability ngoài fixture hiện có.
- **Phạm vi áp dụng:** Bản xuất Manim trong profile hiện tại; không chuyển con số trực tiếp qua medium.
- **Đề xuất cho 0.5:** Nếu bổ sung hướng dẫn video, ghi rõ phép thử trên đầu ra/cỡ xem và giữ font-size/fit theo medium, không chép token px/pt.
- **Trạng thái:** Provisionally accepted.

### VIDEO04-FB-003 — Logo chính M8.6 được duyệt trong phạm vi fixture

- **Nguồn Design 0.4:** ZO003–ZO004; `02_quy_chuan/01_mau_logo_chu.md` mục “Logo và dấu nhấn”; `07_mau_thi_giac/design/logos.json`.
- **Vấn đề phát hiện:** Dùng asset logo có nguồn gốc rõ, đúng tỉ lệ và không để từng scene tự chọn placement.
- **Bằng chứng từ ZO Video:** Người dùng chỉ định `horizontal_mono_dark.png`; asset được chép vào repo, giữ aspect ratio, đặt tĩnh trong identity contract tập trung. M8.6 chốt scale 1.00, region `(0.08, 0.005, 0.30, 0.04)`, anchor `top_left`, opacity 1.00. Đó là quyết định cho fixture, không phải chốt logo master hoặc toàn bộ nhận diện.
- **Fixture/video/test:** `projects/m8_motion_test/`; `assets/brand/horizontal_mono_dark.png`; `tests/regression/test_identity.py`; commit `4f78842e3b587d8146c4a753b5d82923ee7efdb1`.
- **Quyết định hiện tại:** Logo asset và placement M8.6 được người dùng duyệt cho video thử nghiệm; identity contract vẫn là profile video, không phải quy tắc canonical 0.4.
- **Mức độ tin cậy:** Cao trong phạm vi M8.6 đã duyệt; thấp khi suy rộng ra toàn hệ nhận diện.
- **Phạm vi áp dụng:** Logo tĩnh của fixture M8.6; không bao gồm motif, intro/outro hay âm thanh.
- **Đề xuất cho 0.5:** Nếu quy định logo cho video, tách asset/placement/scale theo medium và giữ việc duyệt asset master ngoài phạm vi kết luận từ một fixture.
- **Trạng thái:** Provisionally accepted.

### VIDEO04-FB-004 — Truy nguyên asset thương hiệu

- **Nguồn Design 0.4:** ZO003–ZO004 và ZO020; `07_mau_thi_giac/design/logos.json` cùng các tệp logo nguồn.
- **Vấn đề phát hiện:** Video phải tái tạo được mà không runtime phụ thuộc đường dẫn Design repo, đồng thời phân biệt logo chính với accent phụ.
- **Bằng chứng từ ZO Video:** Asset được lưu ở `assets/brand/`, provenance tại `assets/brand/README.md`; kiểm thử bảo đảm path repo-relative và ngăn đường dẫn ngoài repo. `motif.png` được đăng ký là accent phụ, không được compiler render vào main scene.
- **Fixture/video/test:** `projects/m8_motion_test/`; `tests/regression/test_identity.py`; commit `4f78842e3b587d8146c4a753b5d82923ee7efdb1`.
- **Quyết định hiện tại:** Quy trình đóng gói và ghi nguồn asset được xác nhận cho hai tệp đã chọn; chưa có quyết định dùng motif trong sản phẩm.
- **Mức độ tin cậy:** Cao cho khả năng tái tạo và provenance của hai asset trong repo.
- **Phạm vi áp dụng:** Tài sản thương hiệu được tích hợp vào ZO Video; không tự áp thành quy trình license/asset toàn bộ hệ.
- **Đề xuất cho 0.5:** Cân nhắc duy trì metadata nguồn, vai trò và quyền sử dụng cùng asset khi chuyển giao giữa sản phẩm.
- **Trạng thái:** Provisionally accepted.

### VIDEO04-FB-005 — Semantic layout tách vai trò nội dung

- **Nguồn Design 0.4:** `04_ap_dung/02_video.md` mục kiểm kê/nghiệm thu; `02_quy_chuan/03_thich_ung_phuong_tien.md` mục Video; nguyên tắc giữ thứ bậc trong `02_quy_chuan/01_mau_logo_chu.md`.
- **Vấn đề phát hiện:** Một vùng chung khiến graph/text/equation va chạm với nhau và với phụ đề.
- **Bằng chứng từ ZO Video:** Semantic slots cho title, primary math, visual, annotation, conclusion và subtitle nằm trong `src/zo_video/design/layout.py`; scene content và subtitle compositor dùng cùng contract. Regression kiểm các slot và fixture được compile theo role.
- **Fixture/video/test:** M4, M8 motion test; `tests/regression/test_layout.py`, `tests/regression/test_subtitle.py`; M8.1R/M8.2 commit `6406b38ab968f4cbad15265f44389c11e93d4231`, phản hồi M8.1 `3d2d0b05e4e653010cb93cd6b5bcf71b1b8b528a`.
- **Quyết định hiện tại:** Semantic separation được chấp nhận để dùng trong profile thử nghiệm; các toạ độ/tỉ lệ slot không phải token 0.4 dùng chung.
- **Mức độ tin cậy:** Cao về tính nhất quán và kiểm cấu trúc; trung bình về chất lượng bố cục trên nội dung/phân giải chưa thử.
- **Phạm vi áp dụng:** Layout video dọc 1080×1920 trong fixture; không phải layout web/PDF.
- **Đề xuất cho 0.5:** Mô tả vai trò/quan hệ nội dung theo medium, tránh biến normalized coordinates của một video profile thành quy tắc toàn hệ.
- **Trạng thái:** Provisionally accepted.

## B. Phải thích nghi khi sang video

### VIDEO04-FB-006 — Layout dọc, vùng an toàn và diện tích nội dung

- **Nguồn Design 0.4:** `04_ap_dung/02_video.md` phần kiểm tra theo nền tảng; `02_quy_chuan/03_thich_ung_phuong_tien.md` mục Video.
- **Vấn đề phát hiện:** Pixel/pt và bố cục của web/PDF không thể chuyển nguyên sang khung 9:16; vùng an toàn phụ thuộc nơi phát hành.
- **Bằng chứng từ ZO Video:** Profile 1080×1920 dùng normalized semantic slots; phần content fit theo role, subtitle tách riêng; identity có safe region riêng. Đây là adaptation, không phải safe-area tọa độ phổ quát.
- **Fixture/video/test:** M4 và `projects/m8_motion_test/`; `tests/regression/test_layout.py`, `test_subtitle.py`, `test_identity.py`; M8.1R/M8.2 `6406b38ab968f4cbad15265f44389c11e93d4231`, M8.6 `4f78842e3b587d8146c4a753b5d82923ee7efdb1`.
- **Quyết định hiện tại:** Chấp nhận nguyên tắc bố trí lại theo medium; contract hiện tại chỉ dành cho frame và fixture đã kiểm.
- **Mức độ tin cậy:** Cao cho contract hiện tại; thấp cho nền tảng, crop, overscan và thiết bị chưa thử.
- **Phạm vi áp dụng:** Video dọc hiện tại; safe area cần xác minh lại theo platform và đầu ra.
- **Đề xuất cho 0.5:** Giữ nguyên tắc kiểm safe-area theo platform; không công bố các tỉ lệ hiện tại là bất biến.
- **Trạng thái:** Provisionally accepted.

### VIDEO04-FB-007 — Geometry phụ đề dùng chung contract và giới hạn slot

- **Nguồn Design 0.4:** ZO027; `02_quy_chuan/02_noi_dung_toan_hinh_bang.md` mục “Công thức và lời văn”; `04_ap_dung/02_video.md` mục nghiệm thu.
- **Vấn đề phát hiện:** Phụ đề không được che hình; geometry phải nhất quán giữa scene và renderer phụ đề, còn cách chia cue không được nguồn 0.4 quy định cụ thể.
- **Bằng chứng từ ZO Video:** ASS được clip theo subtitle slot của layout. M8.2 tạo nhiều cue cho một narration segment; cue ngắn và giới hạn chiều ngang là thử nghiệm, không phải yêu cầu một dòng của Design 0.4.
- **Fixture/video/test:** `projects/m4_article_to_narration/comparison/m8_2/`; `tests/regression/test_subtitle.py`; M8.2 commit `6406b38ab968f4cbad15265f44389c11e93d4231`, review `4bbd18d915c686269e70cf83cbeeb961b34ce8ae`.
- **Quyết định hiện tại:** Chấp nhận geometry tách slot; chưa chuẩn hóa số dòng, độ dài cue hoặc ngưỡng chiều rộng cho mọi nội dung.
- **Mức độ tin cậy:** Cao cho kiểm geometry/timing; trung bình cho khả năng đọc trên các thiết bị khác.
- **Phạm vi áp dụng:** Subtitle compositor ZO Video hiện hành.
- **Đề xuất cho 0.5:** Nếu cần quy định segmentation, xem riêng theo ngữ nghĩa, độ dài lời, thời gian và độ đọc; không đồng nhất với quy tắc text-only của ZO027.
- **Trạng thái:** Provisionally accepted.

### VIDEO04-FB-008 — Kích thước đồ thị và slot hình

- **Nguồn Design 0.4:** ZO021–ZO022; `02_quy_chuan/02_noi_dung_toan_hinh_bang.md` mục “Đồ thị và hình học”; hướng dẫn video về tách hình/diễn giải/phụ đề.
- **Vấn đề phát hiện:** Graph quá cao có thể lấn subtitle và thành phần nội dung khác; nguồn không đưa giới hạn chiều cao theo video.
- **Bằng chứng từ ZO Video:** M8.3 đưa graph vào visual slot, gom graph styles và fit trong layout. Audit ghi nhận graph M4 không còn lấn subtitle trong video xem; không suy ra một phần trăm diện tích chung.
- **Fixture/video/test:** `projects/m4_article_to_narration/comparison/m8_3/`; `tests/regression/test_graph.py`, `test_layout.py`; M8.3 commit `33f114ccedf4a4e96d8da14bde1dc5454c90af27`, phản hồi duyệt `e40ef4f2c35b77ddf8ec34153b6b8c76c9e11cc7`.
- **Quyết định hiện tại:** Chấp nhận giới hạn đồ thị trong visual slot ở fixture; không chốt kích thước hoặc tỉ lệ diện tích.
- **Mức độ tin cậy:** Cao cho fixture M4; trung bình cho graph nhiều đường, gián đoạn hoặc nhãn dài.
- **Phạm vi áp dụng:** Graph trong video profile hiện tại.
- **Đề xuất cho 0.5:** Ưu tiên nguyên tắc fit/giữ thứ bậc và kiểm nội dung thực; thu thêm graph phức tạp trước khi đặt giới hạn hình học.
- **Trạng thái:** Provisionally accepted.

### VIDEO04-FB-009 — Dịch ngôn ngữ đồ thị sang Manim

- **Nguồn Design 0.4:** ZO021–ZO022; quy chuẩn đồ thị v0.2 chỉ trong phạm vi tài liệu nêu; `04_ap_dung/02_video.md` về không chuyển nguyên đơn vị giữa medium.
- **Vấn đề phát hiện:** Nét, trục, ticks và labels cần được điều chỉnh cho độ phân giải/cỡ xem video mà không đổi nghĩa toán học.
- **Bằng chứng từ ZO Video:** Graph roles và token tập trung tại `src/zo_video/design/graph.py`; curve chính, axis/context, ticks, points, auxiliary và highlight có vai trò riêng; Manim sizes không sao chép đơn vị TeX.
- **Fixture/video/test:** M4 GraphDiagnostic và M8 motion test; `tests/regression/test_graph.py`; M8.3 `33f114ccedf4a4e96d8da14bde1dc5454c90af27`, quy tắc endpoint được bổ sung tại `da26cf750c9fc1cb7a7b7bff37f42111f23f4b08`.
- **Quyết định hiện tại:** Ngôn ngữ đồ thị M8.3 được chấp nhận cho thử nghiệm; các giá trị Manim và quy tắc riêng cho endpoint vẫn là video-specific.
- **Mức độ tin cậy:** Cao về tập trung token và invariant được test; trung bình về khả năng chuyển sang đồ thị ngoài fixture.
- **Phạm vi áp dụng:** Graph renderer của ZO Video; không hồi tố quy chuẩn TeX/TikZ hay quy tắc đồ thị chung.
- **Đề xuất cho 0.5:** Xem xét nguyên tắc đồ thị theo medium và ghi rõ ranh giới với thông số renderer; bổ sung fixture đa dạng trước khi kết luận.
- **Trạng thái:** Provisionally accepted.

### VIDEO04-FB-010 — Nhịp action/observation trong budget scene

- **Nguồn Design 0.4:** ZO025; `04_ap_dung/02_video.md` phần chuyển động, thời gian và khoảng dừng.
- **Vấn đề phát hiện:** Scene có thể cạn thời gian cho quan sát nếu chỉ cộng duration action; ví dụ/clip 0.4 không phải chuẩn thời lượng chung.
- **Bằng chứng từ ZO Video:** M8.5 dùng action-to-motion roles và scene budget dựa trên timing; action duration phải nằm trong scene, observation hold được tính có giới hạn. Token duration/easing vẫn `EXPERIMENTAL`.
- **Fixture/video/test:** `projects/m8_motion_test/`; `tests/test_motion.py`, `tests/regression/test_motion.py`; M8.5 `b0fed3f501b97c92ac3a478bf5fd4ad3c349a6cf`.
- **Quyết định hiện tại:** Chấp nhận kiểm budget kỹ thuật; chưa xác nhận các thời lượng/easing là nhịp chung phù hợp.
- **Mức độ tin cậy:** Cao về tính xác định và giới hạn budget; thấp đến trung bình về cảm nhận cadence.
- **Phạm vi áp dụng:** Scene trong fixture đã căn với audio; không phải thời lượng video hoặc cadence tiêu chuẩn.
- **Đề xuất cho 0.5:** Giữ nguyên tắc dành thời gian quan sát như hướng dẫn định tính; không đưa duration cụ thể lên cấp toàn hệ nếu chưa review nhiều nội dung.
- **Trạng thái:** Experimental.

## C. Quy tắc mới phát sinh từ video

### VIDEO04-FB-011 — Phân đoạn subtitle theo cue và đồng bộ thời gian

- **Nguồn Design 0.4:** ZO027; `02_quy_chuan/02_noi_dung_toan_hinh_bang.md`; `04_ap_dung/02_video.md`. Nguồn yêu cầu thời gian đọc/nhìn và không che hình, không quy định một dòng hay segmentation algorithm.
- **Vấn đề phát hiện:** Một narration paragraph/block dài khó theo dõi trên màn hình điện thoại và chiếm vùng hình.
- **Bằng chứng từ ZO Video:** M8.2 tách scene, narration segment và subtitle cue; một segment có thể sinh nhiều cue. Feedback VF-001/VF-007 ghi nhận M4 có 16 cue cho 3 segments, video được người dùng duyệt.
- **Fixture/video/test:** `projects/m4_article_to_narration/comparison/m8_2/`; `tests/regression/test_subtitle.py`; commit `6406b38ab968f4cbad15265f44389c11e93d4231`, review `4bbd18d915c686269e70cf83cbeeb961b34ce8ae`.
- **Quyết định hiện tại:** Hướng cue segmentation tạm chấp nhận trong profile video; one-line, giới hạn ký tự/chiều rộng vẫn không phải quy tắc phổ quát.
- **Mức độ tin cậy:** Cao cho cấu trúc dữ liệu/timing fixture; trung bình cho segmentation semantic tổng quát.
- **Phạm vi áp dụng:** Video có narration/subtitle; không thay đổi định nghĩa subtitle chung ở Design 0.4.
- **Đề xuất cho 0.5:** Xem xét hướng dẫn segmentation theo cụm nghĩa, timing và độ đọc ở video; phải thử cả cue một dòng và nhiều dòng.
- **Trạng thái:** Candidate for 0.5.

### VIDEO04-FB-012 — Narration và visual action cần semantic alignment

- **Nguồn Design 0.4:** `04_ap_dung/02_video.md` yêu cầu hình, lời đọc và khoảng quan sát phối hợp; ZO025 yêu cầu giữ căn tính đối tượng và cho thời gian quan sát. Nguồn chưa mô tả schema alignment.
- **Vấn đề phát hiện:** Đồng bộ file/timing không tự chứng minh visual diễn đạt đúng mệnh đề đang được đọc hoặc giữ đúng đối tượng qua transform.
- **Bằng chứng từ ZO Video:** Scene plan có `narration`, `visual_intent`, objects/actions; M8.5 kiểm motion/action, object identity, order và scene timing. Bằng chứng sâu chủ yếu là fixture M8 motion test.
- **Fixture/video/test:** `projects/m8_motion_test/plan/scenes.json`; `tests/test_motion.py`, `tests/test_scenes.py`; M8.5 `b0fed3f501b97c92ac3a478bf5fd4ad3c349a6cf`.
- **Quyết định hiện tại:** Có contract kỹ thuật cho cấu trúc và timing, nhưng semantic correctness vẫn cần xem-nghe người; chưa là quy tắc 0.4.
- **Mức độ tin cậy:** Trung bình cho mức cần thiết của contract; thấp cho khả năng khái quát qua nhiều bài.
- **Phạm vi áp dụng:** Video giáo dục có lời dẫn và diễn biến hình theo scene.
- **Đề xuất cho 0.5:** Cân nhắc mô tả cách rà soát narration ↔ visual intent/action và giữ identity đối tượng; giữ bước duyệt con người tách khỏi validation cấu trúc.
- **Trạng thái:** Candidate for 0.5.

### VIDEO04-FB-013 — Quy tắc graph axis endpoint và ticks

- **Nguồn Design 0.4:** ZO021–ZO022 và quy chuẩn đồ thị v0.2 trong phạm vi của nó; không thấy quy tắc chung bắt buộc hai arrowheads hoặc cấm endpoint ticks.
- **Vấn đề phát hiện:** Scene-level override có thể làm mất nhất quán trục và đặt ticks vào vùng đầu mũi tên.
- **Bằng chứng từ ZO Video:** Graph contract dùng arrowheads ở hai đầu, interior ticks và clearance; validator chặn scene override. M8 endpoint regression có kiểm riêng.
- **Fixture/video/test:** M4/M8 graph fixtures; `tests/regression/test_graph.py`; commit `da26cf750c9fc1cb7a7b7bff37f42111f23f4b08`.
- **Quyết định hiện tại:** Đây là quy tắc đã chốt cho ZO Video, không phải nội dung canonical của Design 0.4; review hình học vẫn gắn với renderer video.
- **Mức độ tin cậy:** Cao về implementation invariant; trung bình về việc quy tắc nên dùng cho mọi loại hệ trục.
- **Phạm vi áp dụng:** Graph axis của ZO Video theo contract hiện tại.
- **Đề xuất cho 0.5:** Đánh giá như một ứng viên medium-specific; so sánh các trường hợp biểu diễn trục trước khi quyết định phạm vi.
- **Trạng thái:** Candidate for 0.5.

### VIDEO04-FB-014 — Formula presentation cho video

- **Nguồn Design 0.4:** ZO027 và `02_quy_chuan/02_noi_dung_toan_hinh_bang.md` mục công thức; nguồn yêu cầu công thức được render, không quy định slash-fraction hay `\left...\right`.
- **Vấn đề phát hiện:** Slash-fraction và ngoặc không co giãn có thể kém rõ trong formula presentation; validator cần bắt kiểu viết đã thống nhất cho fixture.
- **Bằng chứng từ ZO Video:** `src/zo_video/formulas.py` từ chối slash fraction, yêu cầu `\frac{...}{...}`; function argument có phân số/lũy thừa dùng `\left(...\right)`. Unit tests bao gồm trường hợp chấp nhận/từ chối.
- **Fixture/video/test:** `projects/m8_motion_test/plan/scenes.json`; `tests/test_formulas.py`; kiểm regression được ghi trong M8.A audit; pipeline/validator hiện hành ở HEAD `96b9c30a2fec22058c006047decc77b9b13f3bff`.
- **Quyết định hiện tại:** Giữ validator trong phạm vi video; không tuyên bố cú pháp trình bày này là quy tắc Design 0.4 hay bắt buộc cho mọi biểu thức/medium.
- **Mức độ tin cậy:** Cao về hành vi validator; thấp đến trung bình về cơ sở thị giác/khả năng tổng quát của ngưỡng cú pháp.
- **Phạm vi áp dụng:** Chuỗi formula gửi vào renderer ZO Video.
- **Đề xuất cho 0.5:** Đánh giá guideline presentation-math theo medium, kèm ví dụ/counterexample và kiểm tra biểu thức hợp lệ để tránh over-validation.
- **Trạng thái:** Candidate for 0.5.

## D. Chưa đủ bằng chứng

### VIDEO04-FB-015 — Motif như brand accent trong main scene

- **Nguồn Design 0.4:** ZO020; `02_quy_chuan/01_mau_logo_chu.md` mục “Logo và dấu nhấn”; `07_mau_thi_giac/design/logos.json`.
- **Vấn đề phát hiện:** Chưa có bằng chứng motif tăng nhận diện mà không cạnh tranh với nội dung Toán.
- **Bằng chứng từ ZO Video:** `motif.png` có trong asset registry và provenance; test xác nhận compiler không render motif vào scene chính.
- **Fixture/video/test:** M8.6 `projects/m8_motion_test/`; `tests/regression/test_identity.py`; commit `4f78842e3b587d8146c4a753b5d82923ee7efdb1`.
- **Quyết định hiện tại:** Lưu như accent phụ, không sử dụng trong main scene; chưa có preview được người dùng duyệt.
- **Mức độ tin cậy:** Cao về việc chưa dùng; chưa có bằng chứng hiệu quả thị giác.
- **Phạm vi áp dụng:** Video fixture M8.6.
- **Đề xuất cho 0.5:** Không đưa motif thành thành phần mặc định; chỉ xem xét qua thử nghiệm riêng có mục tiêu và duyệt.
- **Trạng thái:** Observation.

### VIDEO04-FB-016 — Audio/spoken presentation

- **Nguồn Design 0.4:** `04_ap_dung/02_video.md` phần “Video và âm”/“Mẫu để nghiệm thu”; ZO024–ZO026 và quy chuẩn chú âm chỉ trong đúng phạm vi nguồn.
- **Vấn đề phát hiện:** Kỹ thuật mux/alignment không đo độ rõ, nhịp, pronunciation hay khoảng nghỉ đủ để quan sát.
- **Bằng chứng từ ZO Video:** Chỉ có evidence sơ bộ M8.7: voice do dự án cung cấp được căn timing và mux; baseline/trial pass-through hiện có giống hệt từng byte. Chưa có kết quả nghe của người dùng. M8.7 đang tạm dừng.
- **Fixture/video/test:** `projects/m8_motion_test/comparison/m8_7_audio_trial/`; `listening_notes.md`; tài liệu trial và VF-008 trong repo video. Không có kết luận M8.1–M8.6 về audio.
- **Quyết định hiện tại:** Chưa nghiệm thu audio; không thêm TTS, sonic logo, nhạc, filter hay ngưỡng loudness. Không tiếp tục M8.7 trong nhiệm vụ này.
- **Mức độ tin cậy:** Cao về pipeline kỹ thuật và trạng thái chưa nghe; chưa có bằng chứng trải nghiệm nghe.
- **Phạm vi áp dụng:** Voice track fixture và đường build ZO Video.
- **Đề xuất cho 0.5:** Sau khi M8.7 được tiếp tục và nghe thực tế, cân nhắc checklist tiếp nhận thiết bị/độ rõ/nhịp; không đề xuất target loudness từ số đo hiện tại.
- **Trạng thái:** Observation.

### VIDEO04-FB-017 — Intro/outro video

- **Nguồn Design 0.4:** `04_ap_dung/02_video.md` yêu cầu nghiệm thu đầu/kết video; không xác lập một intro/outro dùng chung hay thời lượng logo.
- **Vấn đề phát hiện:** Chưa có thử nghiệm nhận diện đầu/kết độc lập; không thể suy ra yêu cầu từ logo tĩnh M8.6.
- **Bằng chứng từ ZO Video:** M8.6 chỉ đặt logo tĩnh trong scene; không có intro/outro contract được thử nghiệm/duyệt.
- **Fixture/video/test:** `projects/m8_motion_test/`; identity test M8.6; commit `4f78842e3b587d8146c4a753b5d82923ee7efdb1`.
- **Quyết định hiện tại:** Chưa xác định; không thêm đoạn mở/kết hoặc duration.
- **Mức độ tin cậy:** Cao rằng phạm vi M8.6 không kiểm intro/outro; không có bằng chứng về hướng thiết kế.
- **Phạm vi áp dụng:** Video ZO Math nói chung.
- **Đề xuất cho 0.5:** Chỉ mở mục này nếu có yêu cầu sản phẩm cụ thể; tách nhận diện tĩnh khỏi mở/kết chuyển động.
- **Trạng thái:** Observation.

### VIDEO04-FB-018 — Readability/accessibility trên nhiều thiết bị

- **Nguồn Design 0.4:** `04_ap_dung/02_video.md` yêu cầu xem ở kích thước điện thoại và theo platform; quy chuẩn 0.4 liên quan typography/medium.
- **Vấn đề phát hiện:** Regression cấu trúc và một lượt xem video không chứng minh readability hoặc accessibility trên thiết bị/nền tảng khác nhau.
- **Bằng chứng từ ZO Video:** Có frame 1080×1920/30 fps và kiểm slot/font; audit không ghi nhận kiểm nhiều thiết bị/nền tảng hoặc tuyên bố accessibility compliance.
- **Fixture/video/test:** M4 và M8 motion test; `tests/regression/test_video_format.py`, `test_typography.py`, `test_layout.py`; M8.A `96b9c30a2fec22058c006047decc77b9b13f3bff`.
- **Quyết định hiện tại:** Chưa có kết luận accessibility đa thiết bị; các test hiện hữu chỉ xác nhận contract kỹ thuật đã lập.
- **Mức độ tin cậy:** Cao về phạm vi test ghi nhận; chưa có bằng chứng người dùng đa thiết bị.
- **Phạm vi áp dụng:** Chưa giới hạn được ngoài fixture và thiết bị đang dùng.
- **Đề xuất cho 0.5:** Xác định thiết bị/cỡ kiểm tối thiểu và tiêu chí đọc/contrast/caption trước khi đưa ra tuyên bố accessibility.
- **Trạng thái:** Observation.

### VIDEO04-FB-019 — Motion cadence tổng quát

- **Nguồn Design 0.4:** ZO025; `04_ap_dung/02_video.md` phần chuyển động/khoảng dừng; thời lượng mẫu không phải chuẩn.
- **Vấn đề phát hiện:** Một fixture chứng minh được budget và vài action, không xác lập cadence tối ưu cho nhiều dạng nội dung.
- **Bằng chứng từ ZO Video:** M8.5 có mapping, duration, easing và observation hold; test tập trung deterministic budget/order. Audit giữ các thông số này là `EXPERIMENTAL`.
- **Fixture/video/test:** `projects/m8_motion_test/`; `tests/test_motion.py`, `tests/regression/test_motion.py`; M8.5 `b0fed3f501b97c92ac3a478bf5fd4ad3c349a6cf`.
- **Quyết định hiện tại:** Giữ token motion ở trạng thái thử nghiệm; không nâng thành cadence/giây chung.
- **Mức độ tin cậy:** Cao về hành vi kỹ thuật của fixture; thấp về đánh giá cadence đa nội dung.
- **Phạm vi áp dụng:** Motion M8.5 trong fixture hiện có.
- **Đề xuất cho 0.5:** Cân nhắc bộ tiêu chí xem-nghe trên nhiều nội dung, tách vai trò chuyển động khỏi duration cụ thể.
- **Trạng thái:** Experimental.

## Lệch trạng thái cần chủ dự án quyết định

Không thay đổi trạng thái của VF-002, VF-003 hoặc VF-004 trong lần chuyển giao này.

| Feedback | Current summary status | Current detailed status | Bằng chứng implementation | Đề xuất reconciliation (chưa áp dụng) |
|---|---|---|---|---|
| VF-002 — Đồ thị | Ý niệm | Tạm chấp nhận | M8.3 giới hạn graph trong visual slot; fixture M4 được duyệt; graph regression có style/geometry checks. | Chủ dự án quyết định có tách nhận xét “graph quá lớn” khỏi kết quả M8.3 đã tạm chấp nhận hay không; không đồng nhất bằng chứng fixture với một giới hạn kích thước chung. |
| VF-003 — Hệ trục | Ý niệm | Tạm chấp nhận | M8.3 graph language được duyệt; endpoint/tick contract về sau có test và commit riêng. | Chủ dự án quyết định tách “cảm giác axis/tick/stroke M8.0A” khỏi endpoint rule đã chốt cho video hay giữ chung; chưa tự sửa status. |
| VF-004 — Nhận diện ZO Math trong video | Đang thử nghiệm | Ý niệm | Graph M8.3, typography/colors M8.4 và logo identity M8.6 có các mức duyệt riêng; M8.6 logo được chốt, nhưng audio/motion/identity tổng thể còn mở. | Chủ dự án quyết định có chia feedback theo lớp (logo/graph/typography/audio/motion) hay không; evidence hiện tại không hỗ trợ một trạng thái đơn cho toàn bộ “identity”. |

## Metadata và boundary cần lưu ý khi chuẩn bị 0.5

| Mục | Giá trị hiện tại | Bất nhất quan sát được | Khuyến nghị cho future 0.5 preparation |
|---|---|---|---|
| Phiên bản Design specimen | `0.4` trong `03_du_lieu/bo_ban_giao.json` | Video feedback/profile traceability còn ghi bộ tài nguyên/điều hành `0.4.1`, trong khi metadata bundle hiện tại là `0.4.2`. | Khi chuẩn bị 0.5, đối chiếu lại metadata mọi profile/log với bundle; không đổi phiên bản hiện tại trong lần chuyển giao này. |
| Profile integration boundary | `zo_math_0_4`; mục cuối profile ghi “Next integration boundary: M8.1” | Repo video đã có M8.1–M8.6, M8.A; M8.7 hiện tạm dừng. | Thay boundary chỉ trong một lần cập nhật profile được duyệt; không dùng việc ghi feedback này để sửa profile hoặc mở M8.7. |

## Traceability map

### Design source → ZO Video

| Feedback source ID | Hồ sơ Design | Audit / evidence map | Milestone và commit liên quan |
|---|---|---|---|
| VF-001, VF-007 | `VIDEO04-FB-007`, `VIDEO04-FB-011` | `docs/design/design_0_4_video_coverage_audit.md`; `docs/design/zo_math_0_4_video_feedback.md` | M8.1R/M8.2 `6406b38ab968f4cbad15265f44389c11e93d4231`; review M8.2 `4bbd18d915c686269e70cf83cbeeb961b34ce8ae` |
| VF-002 | `VIDEO04-FB-008` | Coverage audit mục Graph language; feedback detail VF-002 | M8.3 `33f114ccedf4a4e96d8da14bde1dc5454c90af27` |
| VF-003 | `VIDEO04-FB-009`, `VIDEO04-FB-013` | Coverage audit mục Graph language/Axis endpoint; feedback detail VF-003 | M8.3 `33f114ccedf4a4e96d8da14bde1dc5454c90af27`; endpoint `da26cf750c9fc1cb7a7b7bff37f42111f23f4b08` |
| VF-004 | `VIDEO04-FB-001`–`005`, `015`–`019` | Coverage audit toàn ma trận; feedback detail VF-004 | M8.3 `33f114ccedf4a4e96d8da14bde1dc5454c90af27`; M8.4 `b18bc001ca13dbd6d98e6a2e008b5a666ad8d5a0`; M8.5 `b0fed3f501b97c92ac3a478bf5fd4ad3c349a6cf`; M8.6 `4f78842e3b587d8146c4a753b5d82923ee7efdb1` |
| VF-005, VF-006 | `VIDEO04-FB-005`–`007` | Coverage audit mục Layout/Subtitle; feedback detail VF-005/006 | M8.1R/M8.2 `6406b38ab968f4cbad15265f44389c11e93d4231` |
| M8.A coverage audit | Các hồ sơ trên; bảng status conflicts/metadata | `docs/design/design_0_4_video_coverage_audit.md` | Audit `96b9c30a2fec22058c006047decc77b9b13f3bff` |
| M8.7 audio (chưa đóng) | `VIDEO04-FB-016` chỉ ghi nhận khoảng trống | `docs/design/m8_7_audio_spoken_presentation_trial.md`, `comparison/m8_7_audio_trial/listening_notes.md` | Không phải phạm vi kết quả M8.1–M8.6; đang tạm dừng, chưa có duyệt nghe |

### ZO Video → Design source

- Hồ sơ nhận feedback: `E:/zo_math/_design/ngon_ngu_thiet_ke_zo_math_0_4/09_nhat_ki/phan_hoi_tich_hop_zo_video_0_4.md`.
- Backlog chuẩn bị: `E:/zo_math/_design/ngon_ngu_thiet_ke_zo_math_0_4/09_nhat_ki/zo_math_design_0_5_candidate_backlog.md`.
- Trạng thái chuyển giao M8.1–M8.6: đã ghi hồ sơ phía Design; video log có đường dẫn ngược tới hồ sơ này.
- Trạng thái M8.7: chưa chuyển thành kết luận; giữ rõ là chưa hoàn tất và đang tạm dừng.
- Design 0.4 canonical files và metadata version không bị sửa.
