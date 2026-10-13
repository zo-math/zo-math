# Đồng bộ nguồn HTML G01 — 08/10/2026

Phạm vi chủ trì giao: đưa mốc G01 vừa chốt vào đường dựng production, giữ toán,
ID và đường học; chưa PDF, commit hoặc phát hành. Không tái thiết kế.

## Mốc và bảo toàn

Mốc: `_audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08/g01-kit.html`.
SHA-256: `5c97396dd9656971e442cb60a07aa799935d3233bf2ae15a53ebc57f76c77e3c`.
Giữ nguyên tệp và sao lưu cả bundle, kiểm hash, tại
`D:/Downloads/ZO_Math_G01_moc_da_chot_2026-10-08_5c97396dd965`.

## Lỗi, nguyên nhân và guard

| Lỗi/phạm vi | Nguyên nhân đã kiểm | Nguồn sửa / hàng rào |
|---|---|---|
| HTML mới không tái tạo được từ đường production cũ | Bản đồ vùng đọc và shell mới chỉ nằm ở prototype; render QMD vẫn dùng pilot | Marker G01 + hook `zo_web_2027_production.py`, layout metadata canonical; không dùng audit làm build input |
| Có nguy cơ quay về nhật kí sáu mục | Script legacy còn builder sáu mục, trái QMD/chuẩn 14 trường | Shell mới không nạp script legacy; đối chiếu DOM với mốc và kiểm đúng 14 dòng nguồn |
| Khoảng trắng sát công thức bị mất trong adapter đầu tiên | Gộp text binding theo nội dung chuẩn hóa làm lẫn khoảng trắng ở hai vị trí | Lưu leading/trailing whitespace theo vị trí; kiểm chính xác tọa độ và typography của mọi view |
| Link footer còn đường dẫn thư mục thử nghiệm | URL canonical gốc `/content/*.qmd` chưa được chuyển sang đích output | Binding site-path đổi QMD sang HTML, kiểm đích thật trong docs; không giữ đường audit |
| Hình nguồn đổi nhưng SVG trình bày có thể còn cũ | Variant đọc đã duyệt có lớp phóng nhãn/mask riêng | Hash SVG/JSON toán nguồn và hash variant; từ chối drift. So sánh đủ 13 hình giữ nguyên glyph, đường cong, tọa độ và transform toán, chỉ loại lớp label/mask trình bày có cờ rõ ràng |
| Render trang khác có thể kéo G01 vào ngoài phạm vi | Hook đặt ở project dùng chung | Chỉ chọn G01 có trong `QUARTO_PROJECT_OUTPUT_FILES`; không nạp G02 không có marker |

Các lỗi cũ về vùng đọc, thụt lề, Ôn lại/Nhật kí và navbar không được coi là đã
sửa lại bằng việc sao chép. Chúng được kiểm hồi quy qua DOM và hình học bản mới
so với mốc: 12 view, 1440/430/390 px, tất cả disclosure mở, nền/sắc xám,
drawer/Escape, điều hướng còn thấy khi cuộn và no-JS.

## Bằng chứng và giới hạn

`_audit/zo_g01_source_sync_2026-10-08/`: final-render.log, qa-results.json
(267 kiểm), guard-results.json (23 kiểm), promotion.json và ảnh. QMD chỉ thêm
marker, PDF hiện có giữ nguyên hash; G02/D0/Nhà khóa không đổi khi chuyển output.
Readiness G01: PASS, planned=0. PASS kỹ thuật, thiết kế được chủ trì chốt và
quyền phát hành là ba trạng thái riêng.

Không dựng hoặc chứng nhận tám PDF, không stage/commit/push/phát hành. Chưa
kiểm thiết bị cảm ứng thật, Safari hoặc screen reader; không coi thử headless
là thử người học. Còn phải đồng bộ các định dạng khác trong nhiệm vụ sau.
