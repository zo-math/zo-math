# Mốc thiết kế web khóa 2027 đã duyệt — R1-G01

Ngày 08/10/2026 · Bản ghi WEB04-FB-024 · Trạng thái: **chủ trì đã duyệt thiết kế HTML thử nghiệm R1-G01, 9/10**.

## Quyết định và phạm vi

Chủ trì xác nhận: “9/10 điểm. Hãy để 1 điểm còn lại là mục tiêu phấn đấu cải thiện thiết kế trong tương lai.”

Mẫu hiện hành: [g01-reading.html](../../../_audit/zo_design_web_2027_discovery_2026-10-07/g01-reading.html). Không mở lại vòng tìm hướng hoặc yêu cầu chủ trì chọn grid/font. Một điểm còn lại là dư địa cải tiến khi có trải nghiệm mới, không phải lỗi chưa xử lí hoặc điều kiện ngăn dùng mẫu.

Đây là mốc duyệt thiết kế G01, không tự đồng nghĩa với tích hợp nguồn canonical, nghiệm thu các trang khác, hiệu quả sư phạm, PDF, xuất bản hoặc phê duyệt toàn Ngôn ngữ thiết kế 0.5. Những kết luận “chờ xem/chưa nghiệm thu” trong báo cáo FB-023 là trạng thái tại thời điểm bàn giao; bản ghi này bổ sung quyết định sau đó, không sửa lịch sử.

## Những gì cần giữ khi dùng lại

- Nhận diện Đỏ ZO/Vàng ZO, hệ chữ, nhịp khoảng trắng, bìa phủ vùng nội dung bên phải; không quay về các candidate bị bác.
- Vùng đọc chứa trọn nhãn, tiêu đề, lời dẫn và nội dung cùng nhiệm vụ/lập luận; một trục trong, một lớp chịu trách nhiệm khoảng đệm; không lồng giấy, không tạo thanh tiêu đề rỗng.
- Tách vùng theo bước đọc có nghĩa, không theo số heading/đoạn hoặc chiều cao màn hình. Giải thích phụ thuộc và hình thuộc cùng mạch; liên kết chuyển chặng có vùng và ngữ cảnh.
- Điều hướng ba nhóm vai trò; Ôn lại ngay sau Kiểm tra trong mạch chính, Nhật kí là hỗ trợ riêng. Rail desktop, nút mở drawer mobile rõ ràng; giữ trạng thái chọn, deep-link và quay lại điểm dừng.
- Bộ tùy chỉnh cho thấy nền hiện hành; vùng đọc giữ nền giấy trắng. Hình/BBT không giãn theo hộp, cỡ chữ tương ứng văn bản ở zoom 100%; hình/bảng/công thức rộng có cuộn cục bộ khi cần.
- Ủng hộ là section riêng. Bảo toàn nội dung toán, ID, đáp án, luồng học và liên kết tải.

Các quyết định trên là căn cứ thiết kế web khóa 2027 đã có trải nghiệm G01, chưa tự áp cho PDF/video/toàn website. Bản đồ 154 vùng, các cặp mục được ghép và selector mang tên G01 không phải quy tắc để sao chép sang gói khác.

## Nhận diện đúng phiên bản đã duyệt

Tệp dưới đây nằm trong `_audit/zo_design_web_2027_discovery_2026-10-07/`. SHA-256 được đọc trực tiếp khi ghi mốc; năm tệp runtime chính khớp hash của lần QA đã bàn giao.

| Tệp | SHA-256 |
| --- | --- |
| `g01-reading.html` | `34340b7ca1b2db8e06139dcdcaed89930ad05415df9f9e80ad3f41a1710e7a77` |
| `mau_doc_regions.css` | `d19c666daeadf4857f6d9ee194cd4719bc029b89a09163366eef2c3e3088edcd` |
| `g01-reading.css` | `62bfdbf5688fdbb0505e7b99b31b06a93868defd117e0256f33baac03c9e3da8` |
| `g01-reading-controller.js` | `c61f7e0e33e7ebc73bf7cfa1580d6dfc1821aabbc5a41cf6f2b440f302623a61` |
| `g01-reading-ui.js` | `497e8246a14b30509005c5745dd687175a82127288538675ff8e58c59e61b1f7` |
| `build_g01_reading.py` | `2a1a8d47591c02504bad3392cd341b2d2a9ed7af3cc62992c2f5792b392d2600` |
| `g01-reading-content.json` | `d12ac6c4017e22e34eec6a70144e71e73ec3d18434016efdbdf990e21ad44f98` |
| `g01-reading-qa.json` | `54cb9c8b662e87391488d1d64cf64739bc4262bd3ee504d08280c3ded8a68318` |

Đây là dấu vân tay các tệp chính, chưa phải gói runtime độc lập hay manifest mọi phụ thuộc font/logo/hình. Giữ nguyên mẫu và ảnh hiện có làm đối chứng; không đổi chúng âm thầm khi tách bộ khung.

## Bằng chứng và giới hạn còn giữ

[Báo cáo kỹ thuật](../../../_audit/zo_design_web_2027_discovery_2026-10-07/g01-reading-report.md), kết quả `g01-reading-qa.json` và ảnh `g01-reading-images/`: 457 kiểm đạt ở lần bàn giao, 12 view Edge 1440/390/768/1000. Trong lượt ghi nhận này chỉ đối chiếu hash/kết quả đã có, không chạy lại trình duyệt hoặc render.

Chưa kiểm Safari/Firefox, trình đọc màn hình và cảm ứng trên thiết bị thật. Duyệt thị giác không xóa giới hạn này; khi chuyển sang nguồn canonical phải kiểm lại đúng đầu ra và CSS/JS của nguồn mới. Các guard chống lề lồng, nhãn ngoài vùng, tràn bên trong, phóng hình, selector mục lục sai, mất navbar/giật cuộn và trộn Ôn lại/Nhật kí cần được chuyển cùng bộ khung, không chỉ sao chép CSS.

## Nhiệm vụ kế tiếp được đề nghị

1. **Đóng gói mẫu web dùng chung:** đặc tả vai trò/vùng đọc, token, thành phần vỏ trang và điều hướng, cơ chế tổ chức vùng từ nguồn canonical, bộ kiểm hồi quy và mẫu G01 đối chứng. Tách lớp trình bày khỏi nội dung và bản đồ nhịp đọc riêng; khi tích hợp thật, nguồn chạy lâu dài không phụ thuộc `_audit` hoặc vá chuỗi HTML riêng G01.
2. **Chứng minh nhân bản bằng HTML trang Nhà khóa**, rồi R1-G02 và D0. Dùng cùng nền thiết kế nhưng tổ chức theo chức năng thật: Nhà là tổng quan/đường vào; D0 là khảo sát, không bị ép vào hệ thẻ R1. Khảo sát hiện trạng nội dung/ID/luồng từng trang trước áp dụng; không suy duyệt G01 thành duyệt nội dung G02.
3. **Tổng kết thành bản 0.5:** giữ 0.4 làm lịch sử; hồ sơ 0.5 tách quyết định đã duyệt, thành phần dùng lại, ví dụ kiểm chứng, thay đổi so với 0.4, giới hạn và backlog. Phần web đã xác nhận không tự nâng các phần PDF/video/hình chưa thử thành chuẩn mới. Tích hợp production và xuất bản là các bước có phạm vi/kiểm/duyệt riêng.

Lượt hiện tại chỉ ghi mốc và khuyến nghị, chưa thực hiện ba nhiệm vụ này. Yêu cầu làm HTML trước tiếp tục có hiệu lực; chưa sửa QMD/CSS/JS production, render production/PDF, commit, push hoặc phát hành.

## Bổ sung mốc FB028 — 08/10/2026

Chủ trì đã **chốt hai tinh chỉnh FB027**: câu “Học trong kỉ nguyên trí tuệ nhân tạo, học để tìm lại chính mình.” và sáu vòng tròn nền trực tiếp trên toolbar, giữ Sắc xám bằng biểu tượng. HTML mốc: `_audit/zo_web_2027_tuy_chinh_2026-10-08/home-reading.html` và `g01-kit.html`; không ghi đè hai tệp này.

Chủ trì giao áp dụng kit cho HTML thử nghiệm G02, tự kiểm và ghi lỗi, giữ nội dung toán/ID/luồng; không production, PDF hoặc phát hành. Bản G02 mới ở `_audit/zo_web_2027_g02_2026-10-08/g02-reading.html` **chưa được chủ trì duyệt**. Mốc G01 9/10 và một điểm tương lai giữ nguyên; không tự nâng toàn bộ Ngôn ngữ thiết kế lên 0.5.

## Mốc hiện hành G01 FB033 — thay trạng thái chờ xem FB032

Chủ trì đã xem HTML FB032 và nói “Mình đã xem kết quả, tốt.” Mốc nguồn/HTML:
`docs/content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/index.html`, SHA-256
`8b3a9a1ad532e72951edb415d9ab32a37990a80e13c2d754a2f57028fedc764a`.
Receipt canonical: `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/giao_dien/web_2027_accepted.json`.
Mốc này gồm hình/bảng FB031 và tải PDF/nút drawer FB032; các HTML audit cũ giữ
làm lịch sử, không được lấy lại làm hiện hành. Kiểm/dựng theo hướng dẫn G01 và
`scripts/zo_web_2027_g01_checkpoint.py`; bằng chứng FB033 trong audit checkpoint.
Giữ 9/10 và một điểm tương lai. Chưa PDF đồng bộ, G02 hoàn thiện, phát hành hoặc 0.5 đã khóa.
