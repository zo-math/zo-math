# Sổ phản hồi tích hợp web 2027 — ZO Math 0.4

## WEB04-FB-039 — DH_028: trang Nhà theo HTML/ảnh chủ trì giao, 12/10/2026

Nhận năm ảnh “Hành trình của người học toán” và HTML mau-3 từ Downloads,
copy/đổi tên bản sao trong nguồn khóa, xác minh SHA-256. Tệp HTML tự ghi
“Mẫu 04”; ghi nhận khác biệt này, không suy phiên bản chuẩn từ tên file.
Mẫu nhập là dữ liệu tham khảo, không thực thi JS và không tự trở thành quy chuẩn.

Áp bố cục/nội dung biên tập vào nguồn Home hiện có; thay thẻ mô phỏng bằng
danh mục thật D0/G01/G02, giữ ảnh đồ thị 0.4 riêng mỗi R1. D0 dùng logo 0.4;
ảnh hành trình là minh họa ý niệm, không dùng làm dữ kiện toán học. Giữ các
token, font/logo khóa, giấy đọc trắng, nhãn không đóng hộp, sáu màu/Sắc xám,
ba icon điều hướng và footer thật; không nhập toàn bộ CSS của mẫu.

Lỗi phát hiện khi kiểm ảnh: nút mục lục mobile còn chữ do nhánh dựng mới
chưa áp modifier icon-only. Sửa ở adapter/CSS, có guard DOM và computed
style. Nội dung chưa xác minh (lịch thi) giữ trạng thái chưa xác minh; dịch
vụ có thu phí chưa mở đăng ký; QR/thông tin ủng hộ dùng nguồn thật trong repo.

Nguồn, mapping, guard, phép kiểm và giới hạn tại README của giao diện Home
và `_audit/zo_home_redesign_2026-10-12/README.md`. HTML chờ chủ trì duyệt,
không chứng nhận D0/R1/PDF hay nâng 0.5. Không đổi 06_nguon, 07_mau_thi_giac,
Video/M8.R, root docs, receipt hoặc Git. Công việc và bước tiếp chỉ ở bảng 03.

Trạng thái: **đang mở**  
Ngày mở: 07/10/2026  
Phạm vi: trang Nhà khóa Ôn thi Toán THPT 2027, R1-G01, R1-G02 và D0.  
Mốc nguồn: mẫu thiết kế 0.4 trong bộ bàn giao 0.4.2; gốc làm việc canonical `_design/ngon_ngu_thiet_ke_zo_math_0_4/`.  
Báo cáo baseline: `_audit/zo_design_0_4_web_2027_baseline_2026-10-07.md` tính từ gốc repository `E:/zo_math`.
Current: FB030, mẫu hình riêng tại `_audit/zo_math_figure_profile_2026-10-08/index.html`, chờ duyệt. DH_004 đã đồng bộ nguồn HTML G01 theo `g01-kit.html`; bản đó giữ nguyên trong lượt này. G01 9/10, Nhà/footer/FB027 đã duyệt; G02 còn khoảng cách kiến trúc. B2/B3/B4 không phải mẫu current. Chưa đồng bộ PDF học liệu hoặc phát hành.

## 1. Mục đích

Sổ này là nguồn canonical duy nhất ghi phản hồi của người chủ trì khi quan sát các trang thử nghiệm dùng ZO Math 0.4. Sổ phục vụ hai việc tách biệt:

1. điều hành sửa và nghiệm thu ứng viên web 2027;
2. kết tinh đầu vào đã có bằng chứng để đề xuất ZO Math 0.5 sau khi các trang trong phạm vi đã được chấp nhận và xuất bản.

Không sửa lại lời phản hồi gốc để khớp cách hiểu về sau. Nếu cách hiểu thay đổi, giữ bản ghi cũ và bổ sung kết luận xác minh.

## 2. Trạng thái không được đánh đồng

- `moi_ghi_nhan`: đã nhận ý kiến, chưa xác minh.
- `da_xac_minh`: đã tái hiện hoặc đối chiếu được biểu hiện và phạm vi.
- `dang_xu_ly`: đã xác định nguồn canonical và đang sửa.
- `da_sua_cho_kiem`: đã có ứng viên mới, chưa đủ bằng chứng kiểm.
- `kiem_dat`: kiểm kỹ thuật đạt; chưa thay nghiệm thu của người chủ trì.
- `cho_nguoi_chu_tri_duyet`: đã sẵn sàng để quan sát lại.
- `da_duyet`: người chủ trì đã chấp nhận kết quả trong đúng phạm vi ghi nhận.
- `khong_tiep_nhan`: không áp dụng, kèm lí do.
- `de_lai`: cần thêm bằng chứng hoặc ngoài phạm vi lượt hiện hành.

`da_duyet` trong sổ này không tự đồng nghĩa `published`. Xuất bản vẫn theo quy trình và thẩm quyền riêng của repository.

## 3. Phân loại phản hồi

- `loi_trien_khai`: hiện thực không đúng thiết kế hoặc làm hỏng chức năng.
- `tinh_chinh_thiet_ke`: cần chỉnh cách biểu đạt của mẫu 0.4 trên sản phẩm thật.
- `ung_vien_quy_tac_chung`: có khả năng áp dụng cho nhiều trang hoặc phương tiện; chưa tự trở thành quy chuẩn.
- `noi_dung_hoac_kien_truc_hoc`: không được lấy thay giao diện làm lí do tự sửa; chuyển đúng hồ sơ có thẩm quyền.
- `ngoai_pham_vi`: ghi nhận để truy lại nhưng không mở rộng lượt đang làm.

## 4. Quy tắc đề cử cho 0.5

Một phản hồi chỉ được ghi `de_xuat_0_5: co` khi:

1. biểu hiện và phạm vi đã được xác minh trên sản phẩm thật;
2. nguyên nhân hoặc nhu cầu thiết kế đã được giải thích;
3. đã có ứng viên triển khai và bằng chứng kiểm phù hợp;
4. người chủ trì đã duyệt kết quả;
5. kết luận phân biệt rõ quy tắc chung với ngoại lệ riêng của một trang.

Các giá trị khác là `khong`, `can_thu_them` và `chi_cuc_bo`. Không nâng hàng loạt mọi sửa đổi của đợt tích hợp thành 0.5.

## 5. Mẫu bản ghi

Sao chép toàn bộ mẫu dưới đây cho mỗi phản hồi. Đánh số liên tiếp `WEB04-FB-001`, `WEB04-FB-002`, ...; không tái sử dụng ID đã bỏ.

### WEB04-FB-xxx — Tên ngắn

- Ngày và người phản hồi:
- Trạng thái: `moi_ghi_nhan`
- Phân loại:
- Trang/view/URL:
- Viewport, trình duyệt và cách truy cập:
- Phiên bản HTML hoặc SHA-256:
- Ý kiến nguyên văn:
- Biểu hiện đã xác minh:
- Kết quả mong đợi:
- Nguyên nhân đã xác minh:
- Nguồn canonical cần sửa:
- Phạm vi ảnh hưởng dùng chung:
- Cách sửa:
- Hàng rào chống tái diễn:
- Kiểm đã chạy và bằng chứng:
- Phần chưa kiểm:
- Quyết định của người chủ trì:
- `de_xuat_0_5`: `khong`
- Lí do đề cử hoặc không đề cử:
- Phản hồi/thay thế bản ghi nào:

## 6. Nhật kí phản hồi

### WEB04-FB-001 — Tích hợp thành công nhưng chất lượng thiết kế mới đạt 4/10

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `da_xac_minh`
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: trang Nhà khóa 2027 và R1-G01; ảnh minh họa tập trung vào đầu trang R1-G01.
- Viewport, trình duyệt và cách truy cập: Microsoft Edge, truy cập tệp HTML cục bộ; ảnh `Screenshot 2026-10-07 154128.png` kích thước 1914 × 855 px.
- Phiên bản HTML hoặc SHA-256: Nhà `876b977ba049cd4cf1b619d71acbb6df874c752198aee51569ca873f9140ca20`; G01 `1f92c7fc97b92ee70df21c51baba8fbf11a9549591fdef06d273d5ce24e292a1`.
- Ý kiến nguyên văn: “Kết quả là thành công. Nhưng mình chưa hài lòng với thiết kế hiện tại… mình cho 4/10.”
- Biểu hiện đã xác minh: người chủ trì xác nhận pilot hoạt động và quan sát được; đánh giá thẩm mỹ/kinh nghiệm tổng thể thấp. Đây là hai kết luận khác nhau, không được ghi “đã duyệt thiết kế 0.4”.
- Kết quả mong đợi: giữ nền chức năng đã đạt nhưng hình thành một art direction rõ, có nhận diện, phân cấp, nhịp đọc và cảm giác học tập đủ thuyết phục.
- Nguyên nhân đã xác minh: chưa kết luận; các phản hồi WEB04-FB-002 đến WEB04-FB-007 là các giả thuyết thành phần cần nghiên cứu.
- Nguồn canonical cần sửa: chưa mở sửa; dự kiến lớp tích hợp 0.4 web 2027 và các component/tài sản canonical được xác định sau khảo sát.
- Phạm vi ảnh hưởng dùng chung: trang Nhà, G01; có khả năng ảnh hưởng G02/D0 nếu được kết tinh thành 0.5.
- Cách sửa: trước khi sửa production, dựng 2–3 hướng bố cục/moodboard có cùng nội dung thật, chọn một hướng rồi mới triển khai candidate.
- Hàng rào chống tái diễn: không dùng PASS kỹ thuật, đúng token hoặc “tối giản” làm bằng chứng thiết kế đã đạt; mỗi vòng cần thesis thị giác và ảnh so sánh.
- Kiểm đã chạy và bằng chứng: phản hồi trực tiếp cùng hai ảnh đính kèm; kiểm kỹ thuật pilot trước đó đạt nhưng không thay đánh giá này.
- Phần chưa kiểm: chưa nghiên cứu tham chiếu, chưa thử phương án mới, chưa thử với người học.
- Quyết định của người chủ trì: xác nhận tích hợp thành công; chưa chấp nhận chất lượng thiết kế hiện tại.
- `de_xuat_0_5`: `can_thu_them`
- Lí do đề cử hoặc không đề cử: đánh giá tổng thể là căn cứ mở nghiên cứu, chưa phải một quy tắc thiết kế đủ cụ thể.
- Phản hồi/thay thế bản ghi nào: bản ghi đầu tiên.

### WEB04-FB-002 — Bộ tùy chỉnh phải nhỏ gọn nhưng luôn cho thấy lựa chọn hiện hành

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `moi_ghi_nhan`
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: đầu trang Nhà và R1-G01.
- Viewport, trình duyệt và cách truy cập: desktop Edge; ảnh `Screenshot 2026-10-07 154128.png`.
- Phiên bản HTML hoặc SHA-256: như WEB04-FB-001.
- Ý kiến nguyên văn: vị trí hiện tại và thiết kế ẩn các tùy chọn “chưa hợp lí”; nên nhỏ gọn, cho thấy tùy chọn nền đang bật và có dấu hiệu còn một danh sách ẩn.
- Biểu hiện đã xác minh: điều khiển hiện là một `details` toàn hàng chỉ hiện nhãn chung khi đóng; trạng thái nền hiện hành không thể quét thấy ở đầu trang.
- Kết quả mong đợi: một control compact luôn hiện swatch/tên nền hiện hành, nút mở danh sách và trạng thái Sắc xám; không chiếm một vùng đọc lớn.
- Nguyên nhân đã xác minh: cấu trúc disclosure hiện ưu tiên ẩn toàn bộ tùy chọn và chưa có summary động theo trạng thái.
- Nguồn canonical cần sửa: `assets/html/zo_design_0_4_web_2027.html`; `assets/css/zo_design_0_4_web_2027.css`.
- Phạm vi ảnh hưởng dùng chung: mọi bề mặt web dùng bộ chọn nền 0.4.
- Cách sửa: nghiên cứu control “current swatch + chevron/menu” cho desktop và bottom sheet/popover an toàn trên mobile; chưa chốt hiện thực.
- Hàng rào chống tái diễn: kiểm trạng thái đóng vẫn nói rõ nền hiện hành và affordance mở; bàn phím, focus, no-JS và lưu lựa chọn phải giữ nguyên.
- Kiểm đã chạy và bằng chứng: đối chiếu ảnh và DOM/thiết kế pilot hiện hành.
- Phần chưa kiểm: vị trí tối ưu theo từng breakpoint; hành vi mobile và độ dễ hiểu với người học.
- Quyết định của người chủ trì: yêu cầu nghiên cứu và cải thiện; chưa chốt mẫu cụ thể.
- `de_xuat_0_5`: `can_thu_them`
- Lí do đề cử hoặc không đề cử: có khả năng là component chung nhưng cần candidate và nghiệm thu.
- Phản hồi/thay thế bản ghi nào: chi tiết hóa WEB04-FB-001.

### WEB04-FB-003 — Đầu gói cần trở thành bìa học liệu có hình ảnh và nhận diện

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `moi_ghi_nhan`
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: title block R1-G01; có thể đối chiếu trang Nhà.
- Viewport, trình duyệt và cách truy cập: desktop Edge; ảnh `Screenshot 2026-10-07 154128.png`.
- Phiên bản HTML hoặc SHA-256: G01 như WEB04-FB-001.
- Ý kiến nguyên văn: phần tên gói “đáng lẽ nên thiết kế thành một ảnh bìa nổi bật”, có tên gói, hình minh họa và nhận diện ZO Math khi hợp lí.
- Biểu hiện đã xác minh: title block hiện là một khối trắng lớn chỉ có tiêu đề và phụ đề; chưa có visual anchor hay nhận diện cấp gói.
- Kết quả mong đợi: cover/hero học liệu có một ý tưởng thị giác chính, tên gói rõ, hình minh họa liên quan đến nội dung và nhận diện ZO Math vừa đủ.
- Nguyên nhân đã xác minh: lượt pilot chỉ áp token/bề mặt, chưa thiết kế hệ cover web hoặc chọn tài sản minh họa.
- Nguồn canonical cần sửa: cần khảo sát metadata gói, nguồn hình/logo 0.4 và cơ chế hero dùng chung trước khi chọn.
- Phạm vi ảnh hưởng dùng chung: R1-G01 trước; sau nghiệm thu có thể thành mẫu cover cho G02 và các gói khác.
- Cách sửa: tạo ba thumbnail/composition cover từ cùng nội dung thật; tránh card trắng rỗng và tránh minh họa trang trí không liên quan toán học.
- Hàng rào chống tái diễn: hero phải qua kiểm desktop/mobile, không che tiêu đề, không làm sai hình toán và không biến logo thử thành logo master đã duyệt.
- Kiểm đã chạy và bằng chứng: ảnh đính kèm; chưa tạo candidate.
- Phần chưa kiểm: art direction, loại hình minh họa, tỉ lệ hero, logo variant và chi phí tải trang.
- Quyết định của người chủ trì: yêu cầu nghiên cứu cover nổi bật; chưa chốt hình hoặc bố cục.
- `de_xuat_0_5`: `can_thu_them`
- Lí do đề cử hoặc không đề cử: có khả năng tạo hệ cover chung nhưng cần thử trên nội dung thật.
- Phản hồi/thay thế bản ghi nào: chi tiết hóa WEB04-FB-001.

### WEB04-FB-004 — Điều hướng cần một hệ bố cục thực sự, không phải bảng chữ tối giản cực đoan

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `moi_ghi_nhan`
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: bảng điều hướng R1-G01.
- Viewport, trình duyệt và cách truy cập: desktop Edge; ảnh `Screenshot 2026-10-07 154128.png`.
- Phiên bản HTML hoặc SHA-256: G01 như WEB04-FB-001.
- Ý kiến nguyên văn: thanh điều khiển “thật quá xấu… tối giản cực đoan”; desktop có thể đưa sang trái, mobile có thể ẩn và kéo ra khi cần.
- Biểu hiện đã xác minh: ba nhóm đúng vai trò nhưng đang trình bày như các nhãn chữ rời trong một card ngang; phân cấp hiện hành yếu và chiếm chiều cao đầu trang.
- Kết quả mong đợi: desktop có navigation rail/sidebar gắn với tiến trình đọc; mobile có trigger rõ và panel/drawer dễ gọi lại, không phụ thuộc cử chỉ ẩn duy nhất.
- Nguyên nhân đã xác minh: vòng trước tối ưu hợp đồng chức năng và chống giật, chưa có art direction cho navigation shell.
- Nguồn canonical cần sửa: component điều hướng dùng chung và lớp tích hợp 0.4; chỉ mở sau khi xác định phương án không phá deep link/sticky/view isolation.
- Phạm vi ảnh hưởng dùng chung: G01 và G02; có thể ảnh hưởng mọi gói dùng component.
- Cách sửa: prototype hai breakpoint từ cùng DOM: rail trái trên desktop; nút rõ + drawer/bottom sheet trên mobile. Cử chỉ kéo chỉ là tiện ích bổ sung, không phải lối vào duy nhất.
- Hàng rào chống tái diễn: giữ ba nhóm, Ôn lại ngay sau Kiểm tra, bàn phím, Back/reload/deep link, no-JS và không giật/tràn ngang.
- Kiểm đã chạy và bằng chứng: ảnh và baseline chức năng hiện hành; chưa prototype.
- Phần chưa kiểm: độ rộng rail, quan hệ với sidebar Quarto, mobile gesture, focus trap và reduced motion.
- Quyết định của người chủ trì: nêu hướng ưu tiên desktop bên trái và gợi ý mobile; chưa chốt pattern cuối.
- `de_xuat_0_5`: `can_thu_them`
- Lí do đề cử hoặc không đề cử: component có tác động hệ thống lớn, cần prototype và hồi quy G01/G02 trước khi đề cử.
- Phản hồi/thay thế bản ghi nào: chi tiết hóa WEB04-FB-001.

### WEB04-FB-005 — Nội dung dài cần chia thành các vùng đọc có nhịp

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `moi_ghi_nhan`
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: các view nội dung dài của R1-G01.
- Viewport, trình duyệt và cách truy cập: desktop Edge; nhận xét từ trải nghiệm đọc toàn trang.
- Phiên bản HTML hoặc SHA-256: G01 như WEB04-FB-001.
- Ý kiến nguyên văn: “Chưa có sự phân chia vùng đọc theo cấu trúc nội dung”; gần như toàn bộ nội dung chính ở cùng một vùng đọc nên chưa giảm tải thị giác.
- Biểu hiện đã xác minh: lớp pilot mới tạo một bề mặt trắng lớn cho mỗi view/section cấp cao, chưa biểu đạt đầy đủ các chặng, nhiệm vụ và điểm nghỉ bằng nhịp bề mặt/khoảng trắng.
- Kết quả mong đợi: phân đoạn theo ý nghĩa sư phạm, mỗi vùng có một nhiệm vụ đọc rõ; dùng khoảng trắng, nền, heading và visual anchor để tạo điểm nghỉ mà không biến mọi đoạn thành card.
- Nguyên nhân đã xác minh: mapping giữa cấu trúc học tập và primitive bố cục 0.4 chưa được thiết kế; hiện chỉ có rule bề mặt tổng quát.
- Nguồn canonical cần sửa: trước hết là đặc tả mapping cấu trúc–bề mặt; sau đó CSS/component, không sửa nội dung toán để tạo hình thức.
- Phạm vi ảnh hưởng dùng chung: mọi gói học liệu dài.
- Cách sửa: lập bản đồ view → chặng → nhiệm vụ → hỗ trợ; thử một lát cắt Bài học và một lát cắt Luyện tập trước khi áp toàn G01.
- Hàng rào chống tái diễn: không bọc mọi thứ thành card; giữ thứ tự DOM/no-JS, anchor, bảng/hình và mạch học.
- Kiểm đã chạy và bằng chứng: phản hồi trực tiếp; cần audit thêm trên các view dài.
- Phần chưa kiểm: mật độ tối ưu, số cấp bề mặt và ảnh hưởng tới PDF.
- Quyết định của người chủ trì: yêu cầu nghiên cứu giảm tải thị giác theo cấu trúc nội dung.
- `de_xuat_0_5`: `can_thu_them`
- Lí do đề cử hoặc không đề cử: đây có thể là nguyên tắc cốt lõi của 0.5 nhưng chưa có mapping được duyệt.
- Phản hồi/thay thế bản ghi nào: chi tiết hóa WEB04-FB-001.

### WEB04-FB-006 — Thiết kế lại vùng Ủng hộ như một vùng đọc riêng

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `moi_ghi_nhan`
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: khung Ủng hộ ZO Math; ảnh `Screenshot 2026-10-07 154922.png`.
- Viewport, trình duyệt và cách truy cập: ảnh cắt 755 × 529 px từ sản phẩm người chủ trì quan sát.
- Phiên bản HTML hoặc SHA-256: thuộc ứng viên pilot; hash ảnh `d027b28dc30dcd62f82e57977c59b04e5f6cdaf5ddaa5db182019c5438fd9095`.
- Ý kiến nguyên văn: chưa “ưng” giao diện; dấu nhấn ZO Math sai vị trí; nội dung nên ở một vùng đọc riêng, bắt mắt và tạo thiện cảm hơn.
- Biểu hiện đã xác minh: CTA hiện là card Xám ZO đậm, dấu nhấn nằm trong card, QR và dữ liệu ngân hàng cạnh tranh với lời mời; chưa có khoảng chuyển tiếp thành một section độc lập.
- Kết quả mong đợi: một section hỗ trợ có giọng điệu biết ơn, phân cấp lời mời–QR–thông tin chuyển khoản rõ, dấu nhấn đúng vai trò và đủ nổi bật mà không gây áp lực.
- Nguyên nhân đã xác minh: component hiện tập trung chứa đủ dữ liệu trong một card, chưa thiết kế narrative, placement và cảm xúc của section.
- Nguồn canonical cần sửa: cần kiểm component/tài sản hỗ trợ dùng chung trước khi chọn; không sửa riêng ảnh chụp hoặc HTML sinh.
- Phạm vi ảnh hưởng dùng chung: trang Nhà, gói học liệu và các bề mặt có lời mời hỗ trợ.
- Cách sửa: prototype section sáng và section tối có cùng nội dung thật; thử vị trí cuối mạch đọc và một điểm phù hợp khác, không lặp vô cớ.
- Hàng rào chống tái diễn: QR đọc được, dữ liệu chính xác, contrast/focus đạt, dấu nhấn không thay logo, CTA không chen vào mạch làm bài.
- Kiểm đã chạy và bằng chứng: ảnh đính kèm và đối chiếu yêu cầu ZO014; chưa prototype.
- Phần chưa kiểm: vị trí canonical, responsive, cảm nhận người dùng và độ tin cậy thị giác.
- Quyết định của người chủ trì: yêu cầu thiết kế lại; chưa chốt phương án.
- `de_xuat_0_5`: `can_thu_them`
- Lí do đề cử hoặc không đề cử: yêu cầu Ủng hộ nổi bật đã có; cách thể hiện mới cần thử và duyệt.
- Phản hồi/thay thế bản ghi nào: chi tiết hóa WEB04-FB-001.

### WEB04-FB-007 — Chưa thử họ logo 0.4 trên sản phẩm thật

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `moi_ghi_nhan`
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: header, cover/hero và vùng Ủng hộ của trang Nhà/G01.
- Viewport, trình duyệt và cách truy cập: desktop Edge; hai ảnh đính kèm.
- Phiên bản HTML hoặc SHA-256: như WEB04-FB-001.
- Ý kiến nguyên văn: “Hiện tại, cũng chưa thử dùng các mẫu logo với.”
- Biểu hiện đã xác minh: pilot chưa tích hợp có kiểm soát các variant logo 0.4 vào cover/section; header vẫn dùng tài sản hiện hành của site.
- Kết quả mong đợi: xem các variant màu, đơn sắc, đứng/ngang và kích thước nhỏ trong đúng bối cảnh sử dụng trước khi chọn.
- Nguyên nhân đã xác minh: vòng pilot trước cố ý chỉ áp token và bộ điều khiển, chưa mở lựa chọn logo.
- Nguồn canonical cần sửa: chỉ dùng tài sản trong họ logo 0.4 hoặc nguồn logo canonical đã kiểm; chưa thay logo website toàn cục.
- Phạm vi ảnh hưởng dùng chung: nhận diện toàn hệ nếu được duyệt; vòng thử đầu chỉ ở cover và section hỗ trợ.
- Cách sửa: lập một contact sheet theo bối cảnh thật, rồi gắn candidate được chọn vào prototype cover/Ủng hộ; không thay header production ở bước nghiên cứu.
- Hàng rào chống tái diễn: ghi variant, kích thước, nền và trạng thái duyệt; không gọi mẫu thử là logo master.
- Kiểm đã chạy và bằng chứng: đối chiếu ảnh với ZO003/ZO004; chưa thử candidate.
- Phần chưa kiểm: độ rõ ở kích thước nhỏ, nền sáng/tối, favicon/header và quan hệ với dấu nhấn.
- Quyết định của người chủ trì: yêu cầu đưa logo vào vòng thử; chưa chọn variant.
- `de_xuat_0_5`: `can_thu_them`
- Lí do đề cử hoặc không đề cử: logo là tài sản hệ thống nhưng tỉ lệ/variant vẫn ở trạng thái mẫu thử.
- Phản hồi/thay thế bản ghi nào: chi tiết hóa WEB04-FB-001.

## 7. Cách kết sổ để chuẩn bị 0.5

Chỉ kết sổ sau khi bốn bề mặt trong phạm vi có trạng thái rõ và các bản đã được phép xuất bản đã thực sự xuất bản. Khi kết sổ:

1. giữ nguyên toàn bộ bản ghi;
2. lập danh sách các mục `de_xuat_0_5: co` và `can_thu_them`;
3. đối chiếu xung đột giữa các trang/phương tiện;
4. soạn đề xuất 0.5 riêng, không sửa ngược lịch sử 0.4;
5. ghi rõ điều đã được duyệt, điều chỉ là mẫu thử và điều bị loại.

## 8. Theo dõi vòng discovery ngày 07/10/2026

Người chủ trì giao thực hiện nghiên cứu và 2–3 candidate, không sửa production. Đã tạo ba candidate A/B/C và sáu trang thật dưới `_audit/zo_design_web_2027_discovery_2026-10-07/`; điểm mở `index.html`, căn cứ chi tiết `bao_cao_nghien_cuu.md`. Đây là bước thử cho FB-002..007, không thay hoặc viết lại nhận xét ban đầu, không chứng minh đã khắc phục trên production.

| Bản ghi | Bằng chứng thử mới | Còn cần người chủ trì phản hồi |
|---|---|---|
| WEB04-FB-002 | Cả ba mẫu có swatch/tên nền hiện hành + menu sáu nền/Sắc xám | Có dễ thấy, dễ hiểu và gọn không? |
| WEB04-FB-003 | Bìa sáng A, bìa tối B, bìa atlas C; đồ thị từ ví dụ thật | Cảm giác và mức độ nổi bật nào phù hợp? |
| WEB04-FB-004 | Rail trái; drawer A/C, bottom sheet B; trigger luôn thấy trên mobile | Dễ tìm đường hay còn vướng vùng đọc? |
| WEB04-FB-005 | Bề mặt theo mục/nhiệm vụ/điểm dừng, ảnh lát cắt dài | Thoáng hơn hay bị chia vụn? |
| WEB04-FB-006 | Section Ủng hộ riêng, giữ nguyên lời mời/QR/dữ liệu | Có thiện cảm, đáng tin và đúng sức nặng không? |
| WEB04-FB-007 | `logos.html` và logo gắn trong sáu prototype | Variant nào thích hợp ở từng vị trí? |

Trạng thái vòng thử: **chờ chọn hướng**. Agent đề xuất B — Xưởng toán; `de_xuat_0_5` vẫn `can_thu_them`, chưa có quyết định chọn của người chủ trì. Nội dung nguồn production và baseline chức năng không đổi.

Phát hiện nội bộ của lượt thử, không phải lời phản hồi người chủ trì:

- DISC-001: thiếu `.visually-hidden` ở shell cô lập khiến bảng hỗ trợ screen reader hiện lặp; đã sửa prototype, kiểm computed clip và lát cắt BBT. Giữ nguyên fallback table, không xóa để che lỗi.
- DISC-002: checker tải ảnh chạy trước lazy-load nên báo chưa tải; đã buộc tải/đợi decode trong phép kiểm, không bỏ kiểm ảnh.
- DISC-003: bìa tối B dùng logo trên tấm trắng; đã chọn đúng SVG variant nền tối. Thêm đối chiếu logo ở nền/kích thước thực, không tự vẽ lại hoặc recolor logo.
- DISC-004: selector nhiệm vụ ăn cả heading có cùng class, làm heading mang hộp riêng; đã giới hạn ở section và kiểm lại lát cắt mobile.
- DISC-005: rail sticky bị giới hạn bởi đáy grid cha, đẩy lên dưới header ở cuối view ngắn; đã dùng rail fixed trong prototype và thêm ca kiểm top rail ở cuối trang, không chỉ kiểm view dài.

Nguyên tắc làm việc tiếp tục: ghi lỗi ngay khi phát hiện, tách nguyên nhân đã xác minh khỏi giả thuyết, ghi nơi sửa/kiểm chống tái diễn/phần chưa kiểm; không đóng phản hồi bằng PASS tổng hợp hoặc coi prototype đạt là production đã được sửa. Những phản hồi tiếp theo về A/B/C ghi nối tại sổ này với candidate, view, viewport và ảnh cụ thể.

## 9. Phản hồi chọn hướng B và vòng B2 — 07/10/2026

Người chủ trì chọn **hướng B vì tạo cảm giác muốn ngồi học**, không duyệt thiết kế B hiện tại; không thích tên “Xưởng toán”. Từ vòng này chỉ gọi **B2**, không đặt tên thương hiệu mới. Giữ A/B/C làm bằng chứng lịch sử. Hai ảnh gốc: `Screenshot 2026-10-07 170549.png`, `Screenshot 2026-10-07 170707.png` trong `D:/Pictures/Screenshots/`; bản lưu và hash trong audit B2. Các bản ghi dưới đây bổ sung FB-003..006, không xóa lời phản hồi trước.

| Mã | Ý kiến của người chủ trì / yêu cầu | Nguyên nhân hoặc phạm vi đã xác minh | Cách thử và hàng rào hồi quy |
|---|---|---|---|
| WEB04-FB-008 | B muốn ngồi học hơn; không thích tên “Xưởng toán”; bìa xám đậm nặng; Ủng hộ chưa “ăn ảnh” | B dùng hero Xám ZO đậm, vùng ngân hàng xám; cảm nhận chưa đạt do người chủ trì xác nhận | B2 bìa sáng; section Ủng hộ riêng, phân cấp lời mời–QR–dữ liệu; giữ dữ liệu/QR; người chủ trì duyệt cảm nhận, không dùng PASS để thay thế |
| WEB04-FB-009 | Chưa thấy cá tính Đỏ ZO–Vàng ZO; xám/nâu lấn át | B mặc định Xám 3, rail Xám 2, hero Xám 8 | Thử nền Vàng 1 mặc định, đỏ/vàng ở bìa/điều hướng/lời mời; màu chức năng khối học liệu không bị tô lại tùy tiện; kiểm contrast |
| WEB04-FB-010 | Thu nhỏ khung cửa sinh “tai mèo” | `.candidate-b .hero-art` bo vòm nhưng SVG có nền chữ nhật; không có clipping thống nhất | Bỏ vòm, một khung chữ nhật bo góc chứa trọn ảnh; kiểm 390/430/768/1000/1440, cả trước và sau breakpoint |
| WEB04-FB-011 | **Ở zoom 100%, chữ trong BBT và hình minh họa phải ở cỡ bình thường tương ứng văn bản xung quanh; không tự phóng to quá mức** | `.zo-variation-image` bị ép rộng tới 520px, không xét cỡ chữ SVG. Hình vector khác cần đối chiếu riêng, không suy từ BBT | Đây là yêu cầu đã được người chủ trì xác nhận, không chỉ một đề xuất. Định cỡ từ nhãn gốc và cỡ chữ đoạn chứa; không `width:100%` tùy tiện. Hình rộng cuộn cục bộ, không ép nhỏ chữ; kiểm tỉ lệ nhãn/chữ, không sửa toán hoặc dựng PDF |
| WEB04-FB-012 | Vùng đọc quá dài; cần cách chia khoa học, logic, không chẻ nhỏ cơ học | B mới tách theo section cấp 3; một mục chứa nhiều thao tác nhận thức khác nhau | Bản đồ phân đoạn theo đơn vị lập luận: vấn đề–định lí, điều kiện–đối chứng, chuỗi biểu diễn, nhiệm vụ–tự kiểm. Giữ thứ tự, điều kiện cạnh kết luận, đề cạnh hình, không thu gọn mạch bắt buộc; hiệu quả học tập chưa được đo |
| WEB04-FB-013 | Đổi nền có vùng đọc trùng màu nền | Có lớp section trong suốt và khối phụ dùng token trùng nền tùy chọn; cần phân biệt bề mặt đọc với nền khối chức năng bên trong | Bề mặt đọc trắng độc lập sáu nền, khối đỏ/vàng/xám nằm bên trong giấy trắng; kiểm computed style cả JS/no-JS và Sắc xám |
| WEB04-FB-014 | Nội dung chiếm hết lề phải; tiêu đề và hộp quá rộng, thừa khoảng trắng bên trong | Main giãn theo viewport tới grid 1600px; giới hạn đoạn văn không giới hạn hộp/heading | Giới hạn cột đọc và hộp cùng một measure, giữ lề ngoài bên phải; tiêu đề có measure riêng; kiểm 1440/1920 và mobile, không giấu tràn |

Trạng thái khi tiếp nhận: `dang_xu_ly` trong vòng B2; phân loại FB-010/011/013/014 có lỗi bố cục kỹ thuật, FB-008/009/012 là tinh chỉnh thiết kế có yêu cầu rõ. Nguồn sửa hiện tại chỉ trong `_audit/zo_design_web_2027_discovery_2026-10-07/`, không sửa QMD/CSS/JS production hoặc gói thiết kế khóa. `de_xuat_0_5: can_thu_them` đối với cách hiện thực; yêu cầu cỡ hình của FB-011 được giữ riêng là ràng buộc đã xác nhận.

Bằng chứng chung B2 dưới audit nói trên: `b2-report.md`, `b2-qa-results.json` (149/149), `b2-images/`, `b2-baseline.json`. Đường dẫn ghi ngắn trong các bản ghi dưới đây tính từ audit ấy. Kết quả là kiểm prototype mới, không phải production mới. Trạng thái hiện tại của cả bảy bản ghi là **chờ người chủ trì duyệt**, không tự đóng bằng PASS.

### WEB04-FB-008 — Giữ cảm giác B, thay bìa nặng và thử lại Ủng hộ

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `cho_nguoi_chu_tri_duyet`.
- Phân loại: `tinh_chinh_thiet_ke`.
- Trang/view/URL: `b-g01.html`, bìa và Ủng hộ; thử lại `b2-g01.html`, `b2-home.html`.
- Viewport, trình duyệt và cách truy cập: ảnh 170549, browser nhúng VS Code, file URL; kích thước ảnh không tự coi là CSS viewport.
- Phiên bản HTML hoặc SHA-256: B cũ trong `b2-baseline.json`; B2 theo `b2-qa-results.json` và báo cáo.
- Ý kiến nguyên văn: “Hướng B, Xưởng toán, khiến mình muốn ngồi học hơn. Nhưng mình không thích cách gọi "xưởng toán". Bì có màu xám đậm là quá nặng. Phần Ủng hộ ZO Math vẫn chưa "ăn ảnh".”
- Biểu hiện đã xác minh: hero tối và vùng thông tin ngân hàng xám; cảm nhận do chủ trì xác nhận.
- Kết quả mong đợi: giữ cảm giác muốn học, bìa sáng và section Ủng hộ thiện cảm hơn.
- Nguyên nhân đã xác minh: bố cục B chủ động dùng diện tích xám lớn; không coi sở thích là lỗi toán.
- Nguồn canonical cần sửa: vòng này `build_b2.py`, `b2.css`; production chưa sửa.
- Phạm vi ảnh hưởng dùng chung: hai prototype, chưa nhân rộng G02/D0.
- Cách sửa: nền trắng, đỏ–vàng, logo ngang, QR và dữ liệu phân cấp riêng.
- Hàng rào chống tái diễn: không tự tái dùng tên đã bị từ chối; giữ nguyên QR/lời mời/dữ liệu; xem desktop/mobile.
- Kiểm đã chạy và bằng chứng: bảo toàn text, ảnh tải; ảnh `support-1440.png`, `support-390.png` và hai đầu trang trong `b2-images/`.
- Phần chưa kiểm: cảm nhận chủ trì, điện thoại thật và quét QR bằng thiết bị.
- Quyết định của người chủ trì: chọn hướng B, chưa duyệt thiết kế B/B2.
- `de_xuat_0_5`: `can_thu_them`.
- Lí do đề cử hoặc không đề cử: hình thức mới chưa được chấp nhận.
- Phản hồi/thay thế bản ghi nào: bổ sung FB-003/006, không xóa bản cũ.

### WEB04-FB-009 — Đỏ và vàng phải hiện rõ cá tính

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `cho_nguoi_chu_tri_duyet`.
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: bìa, shell, rail và Ủng hộ hai prototype.
- Viewport, trình duyệt và cách truy cập: ảnh 170549, file URL; kiểm B2 ở sáu viewport.
- Phiên bản HTML hoặc SHA-256: B trong `b2-baseline.json`, bản mới B2.
- Ý kiến nguyên văn: “ZO Math lấy hai màu Đỏ ZO và Vàng ZO làm cá tính, nhưng mình chưa thấy điều đó. Hiện giống như lấy màu xám, mà nâu làm chủ đạo.”
- Biểu hiện đã xác minh: nền mặc định Xám 3, hero Xám 8, rail Xám 2.
- Kết quả mong đợi: đỏ–vàng tạo nhận diện, vùng đọc vẫn điềm tĩnh.
- Nguyên nhân đã xác minh: phân bổ diện tích và vai trò màu của B, không thiếu token.
- Nguồn canonical cần sửa: `b2.css`, adapter `b2.js` sinh bởi `build_b2.py`.
- Phạm vi ảnh hưởng dùng chung: hai prototype; không đổi mặc định toàn site.
- Cách sửa: mặc định thử Vàng 1, tiêu đề Đỏ ZO và CTA Vàng ZO; không recolor khối theo trang trí.
- Hàng rào chống tái diễn: đối chiếu token, contrast và ảnh màu/Sắc xám; không đổi byte logo.
- Kiểm đã chạy và bằng chứng: sáu nền, Sắc xám và ảnh đầu trang trong B2 QA.
- Phần chưa kiểm: mức độ nhận diện theo cảm nhận chủ trì và người học.
- Quyết định của người chủ trì: đỏ–vàng là cá tính; phân bổ B2 chưa duyệt.
- `de_xuat_0_5`: `can_thu_them`.
- Lí do đề cử hoặc không đề cử: xác nhận chủ đích không đồng nghĩa duyệt bố cục.
- Phản hồi/thay thế bản ghi nào: bổ sung FB-003/007.

### WEB04-FB-010 — Khung bo vòm sinh “tai mèo”

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `cho_nguoi_chu_tri_duyet`.
- Phân loại: `loi_trien_khai`.
- Trang/view/URL: hero B tại ảnh 170549; đối chiếu B2.
- Viewport, trình duyệt và cách truy cập: browser nhúng VS Code, file URL; viewport gốc chưa đo trực tiếp.
- Phiên bản HTML hoặc SHA-256: B cũ trong `b2-baseline.json`.
- Ý kiến nguyên văn: “Khi thu nhỏ, khung cửa sinh ra "tai mèo" là sao?”
- Biểu hiện đã xác minh: góc nền chữ nhật SVG lộ ra ở hai vai khung bo vòm.
- Kết quả mong đợi: khung nhất quán ở mọi breakpoint, không cắt nhãn.
- Nguyên nhân đã xác minh: border-radius ở figure không clip nền ảnh con.
- Nguồn canonical cần sửa: `b2.css`, lớp hero của prototype.
- Phạm vi ảnh hưởng dùng chung: hai bìa B2, không đổi SVG.
- Cách sửa: bỏ vòm, hình chữ nhật bo nhẹ, containment rõ.
- Hàng rào chống tái diễn: kiểm kích thước trước/sau breakpoint, không chỉ một ảnh desktop.
- Kiểm đã chạy và bằng chứng: 390/430/768/1000/1440/1920; hình chụp và kiểm overflow/rectangle.
- Phần chưa kiểm: browser khác Edge và thiết bị thật.
- Quyết định của người chủ trì: yêu cầu xử lí biểu hiện, chưa chọn hình khung cuối.
- `de_xuat_0_5`: `can_thu_them`.
- Lí do đề cử hoặc không đề cử: kiểm khung là guard có thể dùng lại; hình thức vẫn thử.
- Phản hồi/thay thế bản ghi nào: bổ sung FB-003.

### WEB04-FB-011 — Cỡ hình theo chữ, không theo chiều rộng hộp

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `cho_nguoi_chu_tri_duyet` đối với B2; yêu cầu cỡ hình đã xác nhận.
- Phân loại: `loi_trien_khai`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: ảnh 170707, BBT trong Kiểm tra; 26 hình toán G01 B2.
- Viewport, trình duyệt và cách truy cập: ảnh cắt của B; B2 kiểm zoom 100%, 1440/390 CSS px.
- Phiên bản HTML hoặc SHA-256: B cũ và SVG trong baseline; từng hình trong `b2-figure-metrics.json`.
- Ý kiến nguyên văn: “Quy tắc là khi 100% khung hình, bảng biến thiên phải ở mức bình thường về cỡ phông như văn bản xung quanh. Đay là quy tắc. Các hình chèn vào khác cũng vậy.”
- Biểu hiện đã xác minh: B ép BBT tới 520px, chữ phóng lớn so với đoạn.
- Kết quả mong đợi: cỡ nhãn thường tương ứng chữ xung quanh; không tự phóng to.
- Nguyên nhân đã xác minh: định cỡ ảnh không có cỡ nhãn gốc làm mốc.
- Nguồn canonical cần sửa: generator/CSS B2; nguồn TeX/SVG chỉ đọc để lấy căn cứ.
- Phạm vi ảnh hưởng dùng chung: yêu cầu dùng lại được cho hình học liệu; mới kiểm 26 hình G01.
- Cách sửa: BBT 10 pt, nhãn đồ thị 9 pt làm mốc 1em; chuyển pt/bp đúng; hình rộng cuộn riêng.
- Hàng rào chống tái diễn: metadata từng hình, assertion 26 tỉ lệ, không `width:100%` tùy tiện, đối chiếu thị giác 100%.
- Kiểm đã chạy và bằng chứng: `b2-figure-metrics.json`, B2 QA, `bbt-1440.png`, `bbt-390.png`.
- Phần chưa kiểm: cảm nhận mọi hình, đo quang học mọi glyph, thiết bị thật; SVG vector cũ chưa thành bảng native.
- Quyết định của người chủ trì: cỡ hình theo chữ là **quy tắc**, không được tự hạ thành sở thích; cách responsive B2 chưa duyệt.
- `de_xuat_0_5`: `can_thu_them` cho cách hiện thực, không phủ nhận yêu cầu đã xác nhận.
- Lí do đề cử hoặc không đề cử: cần kiểm thêm phương tiện/gói trước khi kết tinh schema chung.
- Phản hồi/thay thế bản ghi nào: mới, liên quan FB-005.

### WEB04-FB-012 — Phân vùng theo đơn vị lập luận

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `cho_nguoi_chu_tri_duyet`.
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: các view dài G01 B/B2.
- Viewport, trình duyệt và cách truy cập: trải nghiệm người chủ trì; kiểm B2 1440/390.
- Phiên bản HTML hoặc SHA-256: B baseline; B2 cùng nội dung nguyên vẹn.
- Ý kiến nguyên văn: “Các vùng đọc hiện tại vẫn quá dài. Phải tìm ra một phương thức chia vùng đọc khoa học, logic nhưng không có cảm giác chỉ đơn giản là chẻ nhỏ nội dung.”
- Biểu hiện đã xác minh: một section cấp 3 chứa nhiều thao tác nhận thức.
- Kết quả mong đợi: điểm nghỉ theo ý nghĩa, không chia mỗi đoạn thành thẻ.
- Nguyên nhân đã xác minh: B ánh xạ vùng giấy theo heading cấp cao, chưa có mapping lập luận.
- Nguồn canonical cần sửa: `build_b2.py`, `b2-segmentation.json` sinh ra và `b2.css`.
- Phạm vi ảnh hưởng dùng chung: mới thử G01; không tự gán cùng mapping cho G02.
- Cách sửa: bản đồ Mục 0–7/Kết trong `b2-report.md`; giữ đơn vị điều kiện–kết luận/đề–hình/ví dụ–giải thích.
- Hàng rào chống tái diễn: bảo toàn text/MathML/thứ tự ID, chín heading trực tiếp/TOC, view selection; không thu gọn mạch bắt buộc.
- Kiểm đã chạy và bằng chứng: B2 QA và ảnh lesson/reasoning/chain/checkpoint; hồi quy wrapper được ghi bên dưới.
- Phần chưa kiểm: hiệu quả học tập; một lập luận trọn vẹn vẫn có thể dài hơn màn hình.
- Quyết định của người chủ trì: cần cơ sở logic, chưa duyệt mapping B2.
- `de_xuat_0_5`: `can_thu_them`.
- Lí do đề cử hoặc không đề cử: không tuyên bố “khoa học” là hiệu quả đã chứng minh.
- Phản hồi/thay thế bản ghi nào: chi tiết hóa FB-005.

### WEB04-FB-013 — Giấy đọc không trùng màu nền chọn

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `cho_nguoi_chu_tri_duyet`.
- Phân loại: `loi_trien_khai`.
- Trang/view/URL: G01 B/B2 khi đổi nền.
- Viewport, trình duyệt và cách truy cập: người chủ trì chưa chỉ vùng cụ thể; kiểm B2 sáu lựa chọn, JS/no-JS.
- Phiên bản HTML hoặc SHA-256: B baseline; B2 QA.
- Ý kiến nguyên văn: “Khi đổi màu nên, đôi khi có những vùng đọc có màu hoàn toàn trùng khớp màu nền.”
- Biểu hiện đã xác minh: lớp tổ chức trong suốt và khối chức năng dùng cùng token nền có thể nhập vào canvas; chưa định danh chính xác vùng người chủ trì đã nhìn.
- Kết quả mong đợi: nhận ra vùng đọc ở cả sáu nền.
- Nguyên nhân đã xác minh: nền canvas/giấy/khối chức năng chưa tách rõ trong mapping cũ; không coi khối phụ màu là lỗi tự thân.
- Nguồn canonical cần sửa: `b2.css`, wrapper từ `build_b2.py`.
- Phạm vi ảnh hưởng dùng chung: hai prototype; chưa sửa token chung.
- Cách sửa: giấy trắng độc lập; khối chức năng nằm trong giấy, không tái tô màu từng khối.
- Hàng rào chống tái diễn: kiểm computed background tất cả surface ở sáu nền, có no-JS.
- Kiểm đã chạy và bằng chứng: B2 QA đạt ở 1440/390; Sắc xám vẫn giữ nền trắng.
- Phần chưa kiểm: đúng vùng ban đầu người chủ trì gặp, màn hình thiết bị thật.
- Quyết định của người chủ trì: vùng đọc phải phân biệt nền; chưa nghiệm thu B2.
- `de_xuat_0_5`: `can_thu_them`.
- Lí do đề cử hoặc không đề cử: là nguyên tắc đã có, hiện thực vẫn cần chủ trì xem.
- Phản hồi/thay thế bản ghi nào: bổ sung FB-002/005.

### WEB04-FB-014 — Giới hạn cột đọc, trả lại lề phải

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `cho_nguoi_chu_tri_duyet`.
- Phân loại: `loi_trien_khai`; `tinh_chinh_thiet_ke`.
- Trang/view/URL: G01 B, nội dung dài và hộp; B2 hai trang.
- Viewport, trình duyệt và cách truy cập: desktop theo phản hồi; kiểm 1440/1920 và bốn cỡ hẹp.
- Phiên bản HTML hoặc SHA-256: B baseline; B2 QA.
- Ý kiến nguyên văn: “Vùng nội dung đang giành hết lề phải, gây ra quá tải chiều ngang, một số tiêu đề quá dài theo phương ngang; các hộp chứa nội dung cũng vậy, bỏ trống phần bên phải rất nhiều.”
- Biểu hiện đã xác minh: main giãn theo grid 1600px; max-width đoạn không giới hạn hộp.
- Kết quả mong đợi: vùng đọc vừa mắt, lề ngoài rõ, hộp không quá rộng.
- Nguyên nhân đã xác minh: giới hạn sai cấp bố cục.
- Nguồn canonical cần sửa: `b2.css`, span measure của heading trong generator B2.
- Phạm vi ảnh hưởng dùng chung: hai prototype, không đổi layout site-wide.
- Cách sửa: paper tối đa 760px, main 880px, rail 200px, heading measure riêng; mobile reflow.
- Hàng rào chống tái diễn: kiểm paper width/right margin ở 1440, ảnh 1920, overflow sáu viewport.
- Kiểm đã chạy và bằng chứng: B2 QA và ảnh g01-1440/1920, lesson/bbt mobile.
- Phần chưa kiểm: độ thoải mái khi đọc lâu và kích thước tối ưu theo người học.
- Quyết định của người chủ trì: cần giảm quá tải ngang; tham số B2 chưa duyệt.
- `de_xuat_0_5`: `can_thu_them`.
- Lí do đề cử hoặc không đề cử: chưa biến số pixel của một mẫu thành quy chuẩn.
- Phản hồi/thay thế bản ghi nào: bổ sung FB-005.

### Phát hiện nội bộ B2 và hàng rào bắt buộc khi thử lại

- **B2-DISC-001:** wrapper phân vùng ban đầu làm mất direct child heading/TOC của controller. Biểu hiện: navbar đã xuất hiện nhưng click không chuyển view, Nhật kí/Ôn lại trộn. Nguyên nhân được xác minh từ selector canonical; sửa riêng generator B2 để giữ nguyên cấu trúc cha–con. Thêm kiểm chín heading trực tiếp, TOC trực tiếp và tab thực sự được chọn cho từng view, không chỉ kiểm số nút hay không tràn. Đã kiểm lại B2; production không bị sửa.
- **B2-DISC-002:** phép giả lập Enter thiếu kí tự nên không phát click dù focus đúng. Probe ghi sự kiện xác nhận `text: '\r'` tạo click và mở dialog; sửa phép kiểm B2, không thay UI để né. Giữ kết quả trước sửa bộ kiểm; bàn phím thật/thiết bị thật chưa kiểm.
- Quy tắc làm tiếp: trước sửa ghi phản hồi; sau sửa ghi nguyên nhân đã xác minh, nguồn sửa, ca hồi quy, bằng chứng và phần chưa kiểm. Không đóng lỗi bằng tổng PASS, không coi chọn hướng là nghiệm thu, không áp lên production khi chưa có quyền.

## 10. B2 bị từ chối; cần nghiên cứu lại bố cục tổng thể

### WEB04-FB-015 — B2 5/10, sai tỉ lệ và sai cách định cỡ hình

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `da_xac_minh`; mở lại nhu cầu của FB-008/010/011/012/014. B2 không được chấp nhận; chưa có bản sửa mới.
- Phân loại: `loi_trien_khai`; `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: B2 G01 ở Bài học và bìa; B2 trang Nhà.
- Viewport, trình duyệt và cách truy cập: ảnh Edge ngoài và browser nhúng VS Code, `file://`; không suy CSS viewport hoặc zoom từ kích thước ảnh vật lí.
- Phiên bản HTML hoặc SHA-256: bản B2 trong `b2-final-integrity.json`; ba ảnh 175034/174742/175845 có hash trong `b2-review-reset.md` ở audit discovery.
- Ý kiến nguyên văn: “Mình thấy không ra cái gì hết.”; “Thanh điều hướng bên trái thì không cân đối, nhìn rẻ tiền, bên bo góc, bên không.”; “Bây giờ, chẳng những bảng biến thiên bị phong to, mà luôn cả đồ thị cũng bị phóng to.”; “Trang bìa nên chiếm chọn lề phải, hiện tại cứ thập thò.”; “Thanh Bài học vô cùng xấu xí và chướng mắt.”; “Mình thấy xu hướng càng tệ, lần này cho 5/10.”
- Biểu hiện đã xác minh: bìa chịu max-width main; đầu Bài học và Mục lục thành hai hộp trắng lớn; rail cao với scrollbar ngay cạnh đường bo; generator phóng cả bản vẽ để đưa nhãn về mốc em.
- Kết quả mong đợi: bố cục tổng thể cân đối, có vùng nhận diện trên cột trái rồi tới điều hướng; bìa rộng ở vùng phải; đọc vừa mắt; hình không phóng quá mức; không tạo hộp lớn chỉ để chứa tiêu đề.
- Nguyên nhân đã xác minh: giới hạn cột đọc áp quá rộng phạm vi; wrapper/heading được xử lí bằng hộp; định cỡ hình lấy nhãn làm điều kiện đủ. Nguyên nhân góc rail cần tái hiện browser riêng, chưa khẳng định mọi nền tảng.
- Nguồn canonical cần sửa: chưa sửa giao diện; nguồn thử liên quan là `build_b2.py`, `b2.css`, CSS/controller kế thừa trong audit. Production không phải đích của lượt này.
- Phạm vi ảnh hưởng dùng chung: hai prototype; yêu cầu cỡ hình là ràng buộc tiếp tục có hiệu lực, không đóng bằng PASS cũ.
- Cách sửa: đề xuất nghiên cứu lại bố cục trước, hai bản phối cảnh có cùng nội dung để căn chỉnh cảm nhận; mẫu chuẩn cỡ hình riêng, chưa triển khai hàng loạt.
- Hàng rào chống tái diễn: tách độ rộng bìa/cột đọc; đo cả canvas và nhãn; không tự ép cỡ phông bằng phóng toàn ảnh; kiểm chuyển tiếp đầu mục/điều hướng, không coi số lượng kiểm là chất lượng thiết kế.
- Kiểm đã chạy và bằng chứng: đối chiếu ảnh và nguồn; ví dụ do_thi_01 bị đặt khoảng 825px ở chữ 20px, so với kích thước nội tại khoảng 493px. Chưa chạy browser QA mới vì chưa có giao diện mới.
- Phần chưa kiểm: vị trí chính xác các hình chủ trì đang xem; tái hiện góc rail; tham chiếu thị giác mới, bố cục mới và cảm nhận chủ trì.
- Quyết định của người chủ trì: B2 5/10, cần xem lại và nghiên cứu toàn diện; câu gợi ý “Học trong kỉ nguyên AI, học để tìm lại chính mình.” được giữ là phương án thử nhận diện, chưa tự thành slogan chính thức.
- `de_xuat_0_5`: `can_thu_them`.
- Lí do đề cử hoặc không đề cử: bản thử không đạt; yêu cầu đã rõ nhưng cách hiện thực cần làm lại. Rút lại kết luận diễn giải rằng cỡ hình đã xử lí thỏa đáng; giữ nguyên dữ liệu kiểm cũ để truy nguyên.
- Phản hồi/thay thế bản ghi nào: bổ sung và cập nhật trạng thái FB-008..014; không xóa phản hồi/bằng chứng cũ.

Ghi chú lịch sử: lượt tiếp nhận B2 từng đề nghị chủ trì căn chỉnh brief/tham chiếu. Chỉ thị tiếp theo đã bác bỏ cách làm này: chủ trì đã đưa nhận xét trải nghiệm, agent phải tự nghiên cứu và ra giải pháp. Không còn dùng câu hỏi về bố cục hoặc tham chiếu như một điều kiện để bắt đầu; xem FB-016. Cách hiện thực bìa phủ vùng phải và cột đọc hẹp là quyết định thử của agent, không được ghi thành thiết kế đã được chủ trì duyệt.

## 11. Agent nhận trách nhiệm thiết kế; B3 là bản thử riêng

### WEB04-FB-016 — Phản hồi trải nghiệm đã đủ để bắt đầu nghiên cứu

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `da_xac_minh`; nguyên tắc phân công áp dụng ngay cho vòng discovery này.
- Phân loại: `quy_trinh_lam_viec`.
- Trang/view/URL: quá trình nghiên cứu B/B2 và vòng tiếp theo.
- Viewport, trình duyệt và cách truy cập: không áp dụng; đây là phản hồi về cách phối hợp.
- Phiên bản HTML hoặc SHA-256: B2 giữ nguyên; không phải yêu cầu nghiệm thu HTML.
- Ý kiến nguyên văn: “Mình không muốn trả lời câu hỏi của bạn, vì mình đã nói mình không có kiến thức thiết kế giao diện web. Việc đó phải xuất phát từ hiểu biết của bạn, mình chỉ là người đưa ra trải nghiệm chứ không phải người ra ý tưởng thiết kế.”; “Thì tôi đã nhận xét rồi. Bây giờ phải làm gì?”
- Biểu hiện đã xác minh: agent đưa thêm câu hỏi/brief sau khi đã có phản hồi đủ cụ thể để nghiên cứu trong phạm vi được giao.
- Kết quả mong đợi: agent tự chuyển cảm nhận thành tiêu chí, tự tuyển tham chiếu, lựa chọn và thử giải pháp; chủ trì chỉ cần trải nghiệm và nhận xét.
- Nguyên nhân đã xác minh: biến sự bất định chuyên môn của agent thành nhiệm vụ thiết kế cho chủ trì; nhầm việc chủ trì có quyền duyệt với việc chủ trì phải sáng tạo phương án.
- Nguồn canonical cần sửa: sổ công việc hiện hành, ghi chú cuối FB-015 và nguyên tắc làm tiếp trong chính sổ này.
- Phạm vi ảnh hưởng dùng chung: vòng discovery web 2027 hiện tại; không tự sửa quy chuẩn toàn repository.
- Cách sửa: tự nghiên cứu hai nguồn thị giác và dựng B3, không hỏi lại thiết kế hoặc xin lại quyền tạo prototype đã có.
- Hàng rào chống tái diễn: trước khi hỏi, phân biệt quyết định mục tiêu/phạm vi/quyền của chủ trì với quyết định thiết kế nằm trong chuyên môn được giao. Không dùng việc chưa có website mẫu, grid hay tên phông từ chủ trì làm blocker. Không đòi chủ trì chứng minh cảm giác bằng kiến thức chuyên môn.
- Kiểm đã chạy và bằng chứng: `b3-report.md`, hai prototype mới, moodboard và bằng chứng QA; giao diện/nguồn production bảo toàn.
- Phần chưa kiểm: cảm nhận mới của chủ trì về B3.
- Quyết định của người chủ trì: không trả lời câu hỏi thiết kế; đã đưa trải nghiệm. Không suy thành sự chấp nhận bất kì phương án cụ thể nào.
- `de_xuat_0_5`: `khong` — nguyên tắc phối hợp, không phải token/component thiết kế.
- Lí do đề cử hoặc không đề cử: tránh giao ngược trách nhiệm chuyên môn; cần thực hiện ngay, không đợi phiên bản thiết kế mới.
- Phản hồi/thay thế bản ghi nào: thay đề nghị chờ căn chỉnh brief ở cuối FB-015; không sửa lời nhận xét B2.

### WEB04-FB-017 — B3 thực hiện lại bố cục và thử cỡ hình

- Ngày và nguồn ghi: 07/10/2026, agent ghi kết quả thực hiện từ FB-015/016; **không phải nhận xét hoặc duyệt mới của chủ trì**.
- Trạng thái: `cho_nguoi_chu_tri_duyet`; các giới hạn trong báo cáo vẫn mở.
- Phân loại: `tinh_chinh_thiet_ke`; `loi_trien_khai`.
- Trang/view/URL: `b3-g01.html`, `b3-home.html`; điểm vào `b3-index.html` trong audit discovery.
- Viewport, trình duyệt và cách truy cập: Chromium headless, file://, 390/430/768/1000/1440/1920, deviceScaleFactor 1.
- Phiên bản HTML hoặc SHA-256: manifest bàn giao `b3-delivery.json`; nguồn bảo vệ `b3-baseline.json`.
- Ý kiến nguyên văn: tiếp tục xử lí các ý kiến đã ghi ở FB-015/016; không có ý kiến nghiệm thu B3.
- Biểu hiện đã xác minh: giới hạn bìa/cột đọc chung, hình bị scale theo nhãn, heading/TOC bị bọc thành thanh và vị trí nhận diện không hợp lí ở B2.
- Kết quả mong đợi: bố cục có nhận diện và thứ bậc, cỡ hình vừa, đọc yên, điều hướng dùng được; agent chịu trách nhiệm giải pháp.
- Nguyên nhân đã xác minh: nêu trong `b3-report.md`, gồm phát hiện selector TOC sau khởi tạo và nhãn đồ thị sau scale.
- Nguồn canonical cần sửa: chỉ nguồn prototype mới `build_b3.py`, `b3.css`, `b3_figures.py`; không sửa nguồn production hoặc tài sản khóa 0.4.
- Phạm vi ảnh hưởng dùng chung: hai prototype; không mặc định chuyển sang G02/D0 hoặc hệ hình toàn repo.
- Cách sửa: tách bìa rộng/cột đọc, rail nhận diện–nav, disclosure gọn, Ủng hộ riêng; canvas đồ thị giữ nguyên, glyph nhãn tăng riêng, BBT định cỡ theo nhãn khoảng 18 px.
- Hàng rào chống tái diễn: đối chiếu cả canvas/nhãn/tình huống nhiều panel; so text/MathML/ID/disclosure; chọn từng view; đo cuộn và kiểm ảnh thực, không coi PASS là chấp nhận thị giác.
- Kiểm đã chạy và bằng chứng: 156/156 ở `b3-qa-results.json`, ảnh mới và contact sheet 26 hình; `b3-report.md` ghi đầy đủ B3-DISC-001..003 cùng cách kiểm.
- Phần chưa kiểm: chủ trì chưa trải nghiệm; thiết bị thật, Safari/Firefox/screen reader, tích hợp navbar production và toàn bộ nhiều tab chưa kiểm. Cách hậu xử lí nhãn SVG chỉ là thử nghiệm, chưa phải pipeline nguồn hình chính thức.
- Quyết định của người chủ trì: chưa duyệt B3; B2 vẫn là bản không được chấp nhận.
- `de_xuat_0_5`: `can_thu_them`.
- Lí do đề cử hoặc không đề cử: có một bản để trải nghiệm và bằng chứng kỹ thuật, chưa có căn cứ nâng thành quy chuẩn.
- Phản hồi/thay thế bản ghi nào: triển khai tiếp FB-008..015; không tự đóng những phản hồi ấy bằng số lượng phép kiểm.

Nguyên tắc ghi lỗi tiếp tục bắt buộc: lưu biểu hiện/phạm vi, nguyên nhân đã kiểm chứng, nguồn sửa, phép kiểm chống tái diễn, bằng chứng và phần chưa kiểm; tách “đã sửa”, “đã kiểm”, “chủ trì duyệt”, “đã phát hành”. Những lỗi phát hiện trong B3 không được xóa lịch sử vì đã sửa xong.

## 12. B3 6.5/10; B4 thử trục đọc và nhãn vai trò

### WEB04-FB-018 — Thoáng hơn nhưng chưa liền mạch; tham chiếu 0.3 chỉ về ý tưởng

- Ngày và người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Trạng thái: `cho_nguoi_chu_tri_duyet` bản thử B4; B3 chưa nghiệm thu.
- Phân loại: `tinh_chinh_thiet_ke`; `ung_vien_quy_tac_chung`.
- Trang/view/URL: B3 G01 bìa, Luyện tập và Ôn lại; ảnh 204812/185451/185438. Mẫu tham chiếu chỉ đọc: `E:/zo_math_design_system/specimens/bo_kiem_thu_0_3/ZO_Math_R1_G01_0_3.html`.
- Viewport/trình duyệt: ảnh người dùng Edge/file://; không suy zoom từ kích thước ảnh. B4 kiểm Chromium headless sáu viewport CSS 390..1920, scale 1.
- Phiên bản/hash: nguồn B3 bảo toàn trong `b4-baseline.json`; nguồn tham chiếu, ảnh phản hồi và B4 ghi tại `b4-reference-register.json`, `b4-delivery.json` ở audit discovery.
- Ý kiến nguyên văn: “Nếu phải cho điểm, thì mình cho bản này 6.5/10.”; “Mọi thứ nó ít gò bó hơn trước, ít xuất hiện những khối vô ích.”; “Mình cảm giác mỗi thứ đang rải rác, dàn trải chưa có một trục thống nhất, một ẩn ngôn thiết kế kết nối các thành phần với nhau.”; “các tài nguyên của trang đó đã xưa rồi, bạn không được dùng lại, chỉ lấy ý tưởng thôi.”; “mình không thích gạch đít.”
- Mong đợi: bố cục có cảm giác kết nối, nhãn giúp nhận ra vai trò, giữ sự thoáng nhưng không ngộp văn bản dài; không sao chép mẫu 0.3.
- Căn cứ đã kiểm: mẫu 0.3 có hệ nhãn và hộp tương đối nhất quán nhưng ít khoảng nghỉ dài; B3 đặt bìa và cột đọc trên hai trục khác nhau. Đây là phân tích thiết kế, không phải kết luận thực nghiệm về học tập.
- Nguồn thực hiện: `build_b4.py`, `b4-layout.css` trong `_audit/zo_design_web_2027_discovery_2026-10-07/`; không sửa production hoặc nguồn 0.3.
- Phạm vi: G01 và trang Nhà thử; không suy rộng sang G02/D0.
- Giải pháp thử: cùng trục chữ từ cover tới giấy đọc/Ủng hộ; nhãn vai trò nhỏ, không badge; thêm ba ranh giới tại đầu mục hoàn chỉnh, phân nhóm Lời giải theo heading sẵn có; bỏ gạch chân kể cả hover, giữ focus bàn phím.
- Hàng rào: mã sinh không đọc tài nguyên 0.3; so chữ/MathML/ID/disclosure, chỉ loại đúng nhãn UI mới khỏi phép so chữ; kiểm trục và ảnh đa cỡ. Không tách theo N đoạn hoặc cắt giữa đề–hình–lập luận.
- Bằng chứng: `b4-report.md`, `b4-content-check.json`, hai bộ kiểm B4 và ảnh mới. Cỡ canvas/BBT không bị tăng để lấp đầy hộp.
- Chưa kiểm: cảm nhận chủ trì, hiệu quả học tập, mọi thiết bị/zoom/trình đọc màn hình; một đơn vị hoàn chỉnh vẫn có thể dài hơn màn hình.
- Quyết định chủ trì: B3 6.5/10; thích ý tưởng nhãn/hộp của 0.3, cấm dùng lại tài nguyên cũ; chưa duyệt giải pháp B4.
- `de_xuat_0_5`: `can_thu_them`; đây là thử nghiệm, không tự sửa quy chuẩn khóa 0.4.
- Liên hệ: tiếp nối FB-012/014/016/017, giữ các yêu cầu trước đây; không dùng tham chiếu mới để xóa phản hồi cũ.

### WEB04-FB-019 — Chữ sát mép: PASS toàn trang đã bỏ sót lỗi bên trong vùng đọc

- Ngày và nguồn: 07/10/2026; chủ trì báo lỗi, agent xác minh nguyên nhân và ghi kết quả B4.
- Trạng thái: `cho_nguoi_chu_tri_duyet`; đã có bản sửa và kiểm trong prototype, chưa sửa production.
- Phân loại: `loi_trien_khai`; `quy_trinh_lam_viec`.
- Ý kiến nguyên văn: “Còn lỗi kĩ thuật tràn nội dung ở nhiều vùng đọc.”
- Biểu hiện/phạm vi xác minh: các nhiệm vụ Luyện tập/Kiểm tra/Ôn lại B3 có computed padding 0px, tiêu đề cùng mép trái vùng trắng. Chưa khẳng định đó là mọi dạng tràn mà chủ trì đã gặp.
- Nguyên nhân: adapter gắn `.task-unit` vào `.standalone-unit`; CSS xuất hiện sau ghi đè `padding:0`. Phép kiểm không có scrollbar ngang toàn trang vẫn PASS. Xem `b4-before-padding.json`.
- Nguồn sửa: generator/CSS B4 bỏ khai báo gây xung đột, quy định khoảng đệm chung cho vùng nhiệm vụ. Không hoàn nguyên cụm giao diện hoặc sửa B3 để xóa bằng chứng.
- Hàng rào bắt buộc trong vòng discovery: kiểm computed padding sau JavaScript, kiểm dòng chữ/phần tử con trong mép giấy, cấm che lỗi bằng overflow hidden, mở hết lời giải rồi kiểm lại; kiểm hình rộng cuộn tới cuối. Không chỉ dùng document.scrollWidth để đóng lỗi.
- Lỗi phát sinh khi thử đã xử lí: `B4-DISC-002` nhãn summary bị flex kéo cùng hàng; chuyển summary khối chức năng sang block và kiểm lại. `B4-DISC-003` ghi chú prototype ngoài workspace bị rail che; sửa offset và thêm phép kiểm. Chi tiết tại `b4-report.md`.
- Bằng chứng: `qa_b4_surfaces.py`, `b4-surface-evidence.json`, `b4-surface-results.json`, `b4-surface-run.json` (hash đầu vào và trạng thái hoàn tất); các ảnh practice/review/roles ở desktop/mobile.
- Ranh giới phép kiểm: chữ thường được đo theo dòng; MathML kiểm tính nguyên vẹn và ảnh đại diện, chưa đo từng glyph trên mọi nền tảng. Có một lần chạy đồng thời CDP timeout khi chờ decode ảnh; chạy lại tuần tự, không nới/bỏ assertion, không lấy kết quả cũ làm kết quả mới.
- Chưa kiểm: chủ trì xem lại những vùng đã báo lỗi, Safari/Firefox/thiết bị thật/zoom khác và toàn bộ nhiều tab; không suy PASS thành đã nghiệm thu.
- Quyết định chủ trì: yêu cầu sửa lỗi và tiếp tục tinh chỉnh; không có chấp thuận B4 hoặc quyền sửa production mới.
- `de_xuat_0_5`: `can_thu_them` cho bộ kiểm vùng đọc dùng chung; nguyên tắc ghi lỗi và không đánh đồng kiểm với nghiệm thu áp dụng ngay trong phạm vi đã giao.

Quy tắc làm tiếp sau B4: luôn giữ bằng chứng trước sửa; gắn mỗi kết quả kiểm với đúng HTML/CSS/JS đã dựng; không coi một thuộc tính “không tràn trang” là đủ chứng minh mọi phần tử nằm đúng vùng đọc. Không biến thông số pixel hoặc tên ẩn dụ của B4 thành chuẩn 0.5 khi chưa được chủ trì chấp thuận.

## 13. B4 không đạt — phải thay phương pháp thử

### WEB04-FB-020 — Thụt lề, cỡ chữ và vai trò thiếu nhất quán; chi phí không tương xứng

- Ngày/người phản hồi: 07/10/2026, người chủ trì ZO Math.
- Quyết định: **B4 không đạt**, không nghiệm thu; không nâng thành 0.5. Trạng thái lỗi: đã ghi nhận, chưa có bản sửa mới.
- Nguyên văn: “Không đạt, thụt ra thụt vào, lúc nhỏ lúc lúc lớn, không có phân vai trò rõ ràng. Bạn đang làm tốn kém nhưng không hiệu quả.”
- Bằng chứng: năm ảnh tại `D:/Pictures/Screenshots/`: `Screenshot 2026-10-07 215457.png`, `215440.png`, `215430.png`, `215422.png`, `215357.png` (cùng tiền tố/ngày). Đã xem ảnh người dùng trong hội thoại; không suy CSS viewport/zoom từ ảnh cắt.
- Quan sát cụ thể: đầu khối Hướng dẫn nằm lệch trục so với tiêu đề/nhiệm vụ; cùng khối hướng dẫn khi đứng ngoài, khi lồng trong giấy trắng có độ thụt khác nhau; đoạn dẫn nhập có hộp riêng khiến nhiều bề mặt cạnh tranh; điều hướng mạch chính/hỗ trợ có trục tên khác nhau. Đây là bằng chứng thị giác, chưa phải lần đo lại computed CSS.
- Sai sót của agent: thêm nhãn và khoảng đệm nhưng chưa giải quyết quan hệ cấp bậc giữa vùng đọc và khối chức năng. Kết luận “một trục thống nhất” đã vượt bằng chứng: kiểm trục cover/breadcrumb/Bắt đầu không bao phủ mọi cấu trúc lồng ở Bài học/Luyện tập/Kiểm tra. Không viện số lượng PASS để phản bác trải nghiệm.
- Việc làm ngay: cập nhật trạng thái từ chờ trải nghiệm sang không đạt; giữ nguyên B4 và kết quả kiểm cũ để truy nguyên. Không sửa giao diện, không dựng/render bản toàn trang mới trong lượt tiếp nhận này.
- Đề xuất thay cách làm: chỉ một mẫu nhỏ dùng nội dung thật, đặt cạnh nhau các cấp điều hướng–tiêu đề–hướng dẫn–nhiệm vụ–lời giải; agent xác lập trước cùng vai trò phải giống nhau ở đâu, khác vai trò được khác gì, khi nào được lồng hộp. Tự kiểm quan hệ giữa các khối trong cùng một cảnh trước khi đưa chủ trì xem; chưa nhân rộng sang toàn tài liệu/trang Nhà. Đây là đề xuất, chưa phải phê duyệt mới.
- Phòng tái diễn: không kiểm từng component riêng rồi suy cả hệ thống thống nhất; kiểm cả các vị trí độc lập/lồng nhau và chuyển tiếp giữa các vai trò. Không dựng nhiều bản đầy đủ khi mẫu đại diện chưa giải quyết phản hồi cốt lõi. Chủ trì chỉ cần phản hồi trải nghiệm, không bị giao việc chọn grid, font hoặc thiết kế giải pháp.
- Phần chưa kiểm/chưa sửa: chưa chẩn đoán lại toàn bộ CSS, chưa có mẫu thay thế hoặc kiểm trình duyệt mới. Các lỗi thị giác vẫn mở; production không thay đổi.
- Nguồn điều hành cập nhật: chính sổ này, `cong_viec_hien_tai.json`, `tiep_nhan_san_pham.json`, `lich_su.md` trong cùng thư mục. Báo cáo/manifest B4 giữ nguyên như hồ sơ lần bàn giao trước, không còn là kết luận nghiệm thu hiện hành.
- `de_xuat_0_5`: `can_thu_them`; không đề cử hiện thực B4 là mẫu đã đạt. Bản ghi này thay trạng thái chờ phản hồi ở FB-018/019, không xóa bằng chứng sửa lỗi padding trước đó.

### Tiếp tục FB-020 — Mẫu đọc 01 theo chỉ thị “Làm nhanh đi, còn rất nhiều việc.”

Đã dựng riêng `mau_doc_01.html` trong audit discovery: chỉ hướng dẫn, bốn câu hỏi khởi động và lời giải tương ứng từ nguồn hiện hành. Ba fragment/37 MathML giữ nguyên, không nhập tài nguyên 0.3, không thay kiến thức hoặc đáp án. Không phải B5 toàn trang.

Thử một cấp vùng đọc, cùng inset cho nhãn/summary/thân bài, typography theo cấp thay vì theo vị trí lồng. Bỏ phụ thuộc stylesheet B4; nhãn Nhiệm vụ/Hướng dẫn/Lời giải nằm cùng trục. Kiểm đo các vị trí tương ứng trong mẫu ở 1440/390, đóng/mở, link lời giải, bàn phím/no-JS, sáu nền; xem ảnh đại diện. Kết quả có hash đầu vào ở `mau_doc_01-qa.json`; ghi chú tại `mau_doc_01-notes.md`.

Giới hạn: mẫu không kiểm hết các loại khối/bảng/hình hoặc luồng G01; chưa có nghiệm thu thị giác. B4 vẫn không đạt, FB-020 chưa đóng. Chỉ cập nhật nguồn mẫu và bốn sổ điều hành; không production, PDF hoặc phát hành. Agent tiếp tục chịu trách nhiệm giải pháp, không yêu cầu chủ trì ra ý tưởng.

### WEB04-FB-021 — Tái diễn do nhầm mép khối với trục chữ bên trong

- Phản hồi 07/10/2026: “Bạn có thấy cái nhãn và cái tiêu đề đang bị thụt vô trong không? Cái lỗi này đã nói rồi, có lưu lại chưa mà làm sai nữa? Mình ngán ngẫm quá.” Hai ảnh `D:/Pictures/Screenshots/Screenshot 2026-10-07 222357.png` và `Screenshot 2026-10-07 222632.png`.
- Lỗi trước đã ghi ở FB-020 nhưng cách hiện thực và kiểm sai: `.chapter{padding:0 var(--inset)}` đẩy nhãn Bài học/Khởi động và tiêu đề nằm NGOÀI khối vào trục chữ BÊN TRONG. Phép kiểm còn yêu cầu mọi tiêu đề cùng trục nội bộ nên chứng nhận chính bố cục sai. Đây là lỗi hiểu và áp dụng của agent, không phải chủ trì thiếu brief.
- Quy tắc cụ thể trong mẫu: **nhãn/tiêu đề ngoài khối căn với mép ngoài của khối; nhãn/tiêu đề/chữ trong khối dùng khoảng đệm trong**. Không xóa padding nội dung để chữa tiêu đề ngoài; không ép hai vai trò lên một trục.
- Sửa hẹp: `mau_doc_01.css` bỏ padding ngang của `.chapter`; không sửa nội dung hoặc tái thiết kế trang. `qa_mau_doc_01.py` tách kiểm trục ngoài/trong và thử khôi phục lỗi cũ tạm trong browser để chứng minh phát hiện được sai lệch.
- Bằng chứng: CSS/QA/ảnh trước sửa ở `mau_doc_01-before-heading-fix/`; ảnh và phép đo mới ở `mau_doc_01-images/`, `mau_doc_01-qa.json`. Đã xem desktop1440/mobile390; 39 phép kiểm đạt trên mẫu sửa. Không dùng con số này để tuyên bố thiết kế đã được chấp nhận.
- Trạng thái: **`da_duyet` — đóng FB-021**. Ngày 07/10/2026, chủ trì xác nhận nguyên văn: “Sửa thành công. Mình chốt.” Phạm vi duyệt là sửa căn nhãn/tiêu đề ngoài khối của mẫu đọc01; cách căn ngoài/trong nêu trên được giữ làm quyết định cho công việc tiếp theo, không hỏi lại. Bằng chứng phiên bản là các hash HTML/CSS trong `mau_doc_01-qa.json` sau sửa.
- Giới hạn duyệt: FB-020 về thiết kế tổng thể vẫn mở. Chưa sửa production, chưa nhân rộng, chưa kiểm mọi loại khối. Không suy thành nghiệm thu toàn G01, quyền commit/push/phát hành hoặc nâng chuẩn 0.5. `de_xuat_0_5: can_thu_them` cho hiện thực dùng chung; không hạ lại trạng thái chấp thuận lỗi cụ thể thành chờ duyệt.

### Tiếp tục FB-020 — Mẫu đọc 02; chỉ làm HTML trước

Chỉ thị 07/10/2026: “Làm tiếp đi. Mình chỉ muốn xem HTML trước, khi nào xong HTML mới sang bước khác.” Không mở pha production, PDF, G02/D0 hoặc xuất bản trong khi hoàn thiện HTML.

Đã tạo `mau_doc_02.html` riêng: nguyên mục 3 về chuỗi công thức–đạo hàm–dấu–BBT–đồ thị và lời giải tự kiểm tra 03, 51 MathML giữ nguyên. Nhãn/tiêu đề ngoài theo mép vùng đọc như FB-021; bốn mục con chia vùng theo vai trò có sẵn, phần đồ thị ngắt giữa ràng buộc và đối chiếu; không lồng giấy hoặc đổi luồng toán. Mẫu 01 đã duyệt giữ nguyên.

Phòng tái diễn trong mẫu: kiểm cả mép ngoài và khoảng đệm trong, thử tái chèn padding sai để chứng minh guard phát hiện; kiểm tràn từng đoạn/hộp ngoài vùng cuộn được chỉ định; hình dùng cỡ theo chữ, không giãn đầy hộp; giữ nền giấy trắng trên sáu nền. Không suy các thông số thử thành chuẩn 0.5. Kết quả ở `mau_doc_02-qa.json` gắn hash HTML/CSS/JS, ảnh ở `mau_doc_02-images/`; 83 kiểm đạt, đã xem ảnh 1440/390. Đây là bằng chứng mẫu mới, không phải kiểm toàn G01 hoặc nghiệm thu thị giác.

Trạng thái: **mẫu đọc 02 chờ chủ trì xem HTML**; FB-020 chưa đóng, FB-021 vẫn đã duyệt. Chưa kiểm trình duyệt khác/thiết bị thật/toàn luồng. Chi tiết và tệp tác động ở `mau_doc_02-notes.md`. Không hỏi lại quyết định căn lề, không giao chủ trì việc thiết kế giải pháp.

### WEB04-FB-022 — Vùng đọc phải chứa trọn nhãn, tiêu đề và mạch nội dung

- Phản hồi 07/10/2026: “Tất cả nhãn và tiêu đề phải nằm trong vùng đọc. Phân chia theo nhịp đọc.” Chủ trì bác cách đóng khung lai tạp, link rơi ngoài vùng và yêu cầu sửa cả Câu hỏi khởi động; yêu cầu agent tự tham khảo trang học toán uy tín, không tiếp tục bắt chủ trì giải thích ngôn ngữ thiết kế.
- Bằng chứng: bảy ảnh 225812/225826/225841/225854/225906/225922/225931 cùng tiền tố `Screenshot 2026-10-07` trong `D:/Pictures/Screenshots/`, kèm hai ảnh cũ 222357/222632. Đã xem ảnh trong hội thoại.
- Nguyên nhân đã xác minh: builder đặt `.section-heading` ngoài `.paper`, chapter/lời dẫn/footer trực tiếp trên nền; phân mảnh câu giải thích đồ thị sau danh sách ràng buộc. CSS và kiểm trước chỉ yêu cầu đúng tọa độ, chưa xác lập vùng sở hữu nội dung. Agent đã suy sai từ sửa lỗi căn lề thành nguyên tắc tiêu đề ngoài vùng.
- Quyết định hiện hành: tất cả nhãn/tiêu đề/lời dẫn trong nội dung chính thuộc một vùng đọc; link chuyển đoạn thuộc vùng điều hướng có nhãn. Một vùng là một bước đọc có nghĩa, không đồng nhất một vùng với một heading hoặc một hộp chức năng. Không cộng khoảng đệm theo lớp lồng.
- Quan hệ lịch sử: FB-021 vẫn ghi nhận sửa căn lề đã được chốt tại thời điểm đó; **chỉ thị FB-022 thay cách đặt tiêu đề ngoài vùng cho công việc tiếp theo**. Không viện lần chốt cũ để giữ cách tổ chức người dùng vừa bác; không sửa lịch sử thành chưa từng duyệt.
- Tham khảo: đã đọc/xem OpenStax về đạo hàm và đồ thị, Math Insight về trực giác đạo hàm; tham khảo văn bản APEX/LibreTexts. Chỉ học cách nối giải thích–hình và dùng nhãn chức năng/điều hướng có ngữ cảnh; không lấy tài sản hoặc nội dung. URL, ảnh và giới hạn quan sát tại `reading-regions-report.md` trong audit discovery.
- Nguồn sửa: `reading_regions.py`, hai builder mẫu, một CSS/JS vùng đọc dùng chung; tái sinh cả `mau_doc_01.html` và `mau_doc_02.html`. Ba vùng ở Khởi động; năm vùng ở chuỗi biểu diễn. Giữ nguyên nội dung/thứ tự/toán/ID; link cuối ở vùng cuối có nhãn Chuyển đoạn đọc. Lưu nguyên trước sửa ở `before-reading-regions/`, có manifest hash.
- Phòng tái diễn: `qa_reading_regions.py` kiểm cả hai mẫu, mọi nhãn/heading/đoạn/link phải có vùng chứa; không vùng lồng, không inset cộng dồn, không tràn ngoài vùng cuộn; kiểm câu dẫn phụ thuộc ở cùng vùng, khoảng nghỉ giữa vùng, cỡ hình, sáu nền, bàn phím/no-JS. Ca âm chủ động tách heading ra khỏi vùng và chèn inset sai phải bị phát hiện. Hai điểm vào QA cũ chuyển sang bộ kiểm mới; yêu cầu tọa độ ngoài khối cũ được thay vì chỉ thị mới, không phải nới kiểm để PASS.
- Lỗi phát hiện khi tự xem: `.reading-section{margin:0}` làm hai vùng độc lập chạm nhau; đã sửa selector và thêm phép đo khoảng nghỉ tối thiểu giữa tất cả vùng. Không dùng kết quả “không tràn trang” để bỏ qua lỗi này.
- Bằng chứng: `reading-regions-qa.json` với hash HTML/CSS/JS mới; ảnh `reading-regions-images/`. 177 kiểm đạt trên hai mẫu ở 1440/390/430/768; đã xem ảnh desktop/mobile. Chưa kiểm thiết bị thật/Safari/Firefox/trình đọc màn hình/toàn luồng G01. Kết quả cũ không áp dụng cho HTML mới.
- Trạng thái: **đã sửa trong prototype, chờ chủ trì xem HTML**. FB-020 tổng thể còn mở. Không production/PDF/commit/push/phát hành; không nâng thành quy chuẩn 0.5. `de_xuat_0_5: can_thu_them` cho hiện thực; yêu cầu nội dung thuộc vùng đọc áp dụng ngay trong hai mẫu.

### WEB04-FB-023 — Tiếp tục từ hai mẫu sang toàn HTML G01

- Phản hồi: “Chưa phát hiện lỗi, làm gì tiếp?” và phân vân hai mục cùng vùng. Agent xác định là 3.1–3.2, giải thích căn cứ cùng mục tiêu từ công thức đến chiều biến thiên; không coi mỗi heading là một vùng, cũng không coi cùng ví dụ là đủ để ghép. Ngày 08/10/2026, chủ trì giao “OK. Hãy thực hiện ngay đề xuất của bạn.”
- Phạm vi: toàn bộ HTML prototype R1-G01; giữ nội dung toán/ID/luồng, chưa production/PDF hoặc chuẩn 0.5. Phản hồi chưa phát hiện lỗi ở mẫu không được ghi thành nghiệm thu toàn G01.
- Hiện thực: `g01-reading.html`, nguồn `build_g01_reading.py` + CSS vùng đọc dùng chung của hai mẫu + `g01-reading.css`. Bản đồ vùng và chứng cứ bảo toàn ở `g01-reading-content.json`; controller/UI được sinh riêng trong audit. Mẫu 01/02 và lịch sử cũ không ghi đè.
- Lỗi tự phát hiện: builder ban đầu thay một stylesheet nhưng B3 có hai link, làm CSS cũ tiếp tục gây lề lồng/hình giãn; đã thay toàn danh sách style bằng đúng hai nguồn mới, QA khóa danh sách và đo trục/tỉ lệ. Không dùng !important chồng tiếp để che lỗi.
- Lỗi tự phát hiện: ghép heading nhóm vào details khiến heading chỉ hiện khi mở. Sửa vùng đọc bọc ngoài details; bảo toàn quan hệ heading/disclosure với nguồn. Một mục nguồn chỉ có tiêu đề được ghép với nhiệm vụ đầu thay vì làm hộp rỗng. Inline MathML dài trên mobile được cuộn cục bộ, giữ nguyên biểu thức và cỡ chữ.
- Hồi quy: `qa_g01_reading.py`, kết quả/hash `g01-reading-qa.json`, ảnh `g01-reading-images/`. Kiểm các nhãn/heading/link có vùng chứa; không giấy lồng; cùng trục trong, bề rộng và khoảng nghỉ; tràn khi mở mọi lời giải; cỡ hình; phân tách Ôn lại/Nhật kí; mục lục/chuyển nhánh/quay về; cuộn/drawer/bàn phím/no-JS/sáu nền. Hash đầu vào production và mẫu trước không thay đổi.
- Trạng thái: đã dựng/kiểm, **chờ chủ trì xem HTML đầy đủ**. Chưa kiểm trình duyệt khác, thiết bị thật hoặc trình đọc màn hình. FB-020 tổng thể chưa đóng, không lấy số kiểm làm kết luận thẩm mỹ. Báo cáo chi tiết `g01-reading-report.md` trong audit discovery. `de_xuat_0_5: can_thu_them`.

### WEB04-FB-024 — Chốt thiết kế HTML G01 9/10; chuẩn bị mẫu dùng chung

- Ngày/người phản hồi: 08/10/2026, người chủ trì ZO Math.
- Quyết định nguyên văn: “9/10 điểm. Hãy để 1 điểm còn lại là mục tiêu phấn đấu cải thiện thiết kế trong tương lai.” Chủ trì rất ưng thiết kế lần này; muốn chốt để nhân bản gói khóa học và đưa vào Ngôn ngữ thiết kế 0.5, hỏi bước tiếp theo hợp lí nhất.
- Trạng thái: **`da_duyet` trong phạm vi thiết kế HTML thử nghiệm đầy đủ R1-G01**, mẫu `g01-reading.html`. Không còn chờ chọn hướng hoặc nghiệm thu thị giác G01. Không suy thành duyệt các trang khác, nội dung G02, production/PDF, xuất bản hoặc toàn phiên bản 0.5.
- Liên hệ: đóng FB-020 về thiết kế tổng thể trên mẫu G01 hiện hành; lịch sử B4 không đạt vẫn nguyên. FB-022 về nhãn/tiêu đề nằm trọn trong vùng đọc tiếp tục có hiệu lực. Bản đồ vùng G01 là ví dụ có căn cứ nội dung, không là sơ đồ cố định cho mọi gói.
- Mốc đối chứng: `moc_thiet_ke_web_2027_da_duyet_2026-10-08.md` ghi hash HTML/CSS/JS, builder, bản đồ vùng và kết quả QA. Năm hash runtime chính khớp `g01-reading-qa.json`; 457 kiểm đều đạt ở lần bàn giao. Không chạy lại browser hoặc thay prototype trong lượt ghi nhận.
- Bước kế tiếp đề nghị: tách mẫu/đặc tả/thành phần/checker dùng chung; chứng minh dùng lại bằng HTML Nhà khóa, rồi G02/D0; tổng kết hồ sơ 0.5 có quyết định, ví dụ, hồi quy và backlog. Không sao chép HTML G01 cho từng gói hoặc dùng `_audit` làm nguồn chạy production lâu dài; không chỉ đổi tên thư mục/số phiên bản để gọi là 0.5.
- Dư địa 1 điểm: ghi nhận mục tiêu cải tiến tương lai, chưa có một lỗi cụ thể mới hay điều kiện chặn. Ghi phản hồi mới khi có trải nghiệm thực, không tự tạo yêu cầu thiết kế rồi mở lại vòng tìm hướng.
- Giới hạn còn giữ: chưa kiểm Safari/Firefox, cảm ứng thật hoặc trình đọc màn hình; đầu ra canonical chưa tích hợp. Khi chuyển nguồn phải chuyển cả guard cho căn lề/vùng sở hữu/tràn/cỡ hình/điều hướng và tái kiểm đúng đầu ra mới. Duyệt của chủ trì không thay các kiểm này.
- Phạm vi tệp đổi: bốn sổ điều hành hiện có và mốc duyệt mới trong `09_nhat_ki`; không sửa nội dung prototype/production, tài sản khóa 0.4, QMD/CSS/JS production, PDF hoặc bản báo cáo lịch sử. Chưa commit/push/phát hành.
- `de_xuat_0_5`: `da_duyet_lam_moc_tham_chieu_web_G01`; chưa chốt toàn bộ bộ quy chuẩn 0.5 hoặc triển khai nhiệm vụ đóng gói/nhân bản trong lượt này.

### WEB04-FB-025 — Đóng gói bộ khung đã duyệt; chứng minh dùng lại bằng Nhà khóa HTML

- Ngày/phạm vi: 08/10/2026. Chủ trì giao “OK. Hãy thực hiện ngay nhiệm vụ mới mà bạn vừa đề xuất.” Đây là giao việc đóng gói mẫu dùng chung và dựng Nhà khóa, **không phải phản hồi duyệt thị giác Nhà khóa**.
- Nguồn thực hiện: `_design/web_2027_mau_dung_chung/` và hai script `scripts/zo_web_2027_preview.py`, `scripts/zo_web_2027_check.py`. Tách shell/giấy/chữ/hình/UI khỏi bản đồ nhịp đọc riêng; controller R1 không nạp vào Nhà. Hợp đồng và guard dùng lại cùng hình thức, không chỉ sao chép stylesheet.
- Đầu ra: `_audit/zo_web_2027_mau_dung_chung_2026-10-08/home-reading.html` và `g01-kit.html`. Nhà khóa chín vùng nội dung theo mục tiêu đọc, ủng hộ riêng; giữ dữ liệu canonical/thứ tự/ID/link/ba gói. G01 dùng kit giữ nguyên nội dung/MathML/ID/disclosure/12 view/luồng và thông số bố cục đã duyệt. G01 gốc giữ hash FB-024, không ghi đè.
- Lỗi tự phát hiện và guard: mô tả thẻ bị ép vào cột cạnh thumbnail; sửa adapter chỉ đặt cover ở phần nhận diện, thân mô tả đủ bề rộng và thêm phép đo. Adapter lần đầu giả định h3 trực tiếp trong copy nhưng Quarto bọc section; dừng build, sửa giữ section/ID/heading descendant. Template nguồn bị ignore `*.html`; chuyển `.html.tpl`, không thay ignore repo. Những việc này không thay nội dung toán hoặc thiết kế G01 đã duyệt.
- Lỗi tự xem ảnh: mục lục còn đánh dấu đoạn trước khi vùng Trạng thái đã ở đầu cảnh, vì scrollspy đo section nằm sau nhãn thay vì mép vùng sở hữu. Sửa Home scrollspy theo `.reading-region` và thêm kiểm mục cuối trên năm độ rộng; không thay vị trí/chiều cao navbar hoặc luồng G01.
- Lỗi kiểm/hạ tầng: static checker ban đầu parse lại HTML lớn theo từng fragment; cache theo đích, không bỏ kiểm. No-JS guard ban đầu coi bất kì `[hidden]` là nội dung mất, trong khi nguồn có bảng máy và hint chủ động ẩn; thay bằng đối chiếu hidden inventory chính xác và kiểm phần học/review/journal vẫn đọc được. Không unhide nguồn hoặc bỏ no-JS để làm PASS. Sandbox browser bị ngắt kết nối; chạy lại chính checker có quyền, không tắt browser sandbox. Một profile tạm cũ chưa dọn được do từ chối truy cập; báo cáo ghi phần dư, profile của lần kiểm cuối được dọn.
- Bằng chứng: `build-manifest.json` ghi source/hash/link và projection; `qa-results.json` gắn hash runtime/checker; ảnh trong `images/`, báo cáo `bao_cao.md`. Kiểm mới năm độ rộng, 12 view, sáu nền, drawer/bàn phím/deep-link/quay về/no-JS, hai ca âm vùng sở hữu/inset; đối chiếu computed metrics G01 kit với bản duyệt. Số phép kiểm và giới hạn lấy từ báo cáo mới, không suy PASS thành nghiệm thu.
- Kết quả bàn giao cuối: 712/712 phép kiểm; 23 ảnh, đã xem các cảnh đại diện; dựng lặp lại không đổi bảy hash runtime/manifest. Kiểm trực tiếp link thuộc vùng đọc đã chuyển vào checker. Bộ tài sản 0.4 vẫn đạt 1812/1812 và 1572 tệp baseline bảo vệ không thay đổi. Một thư mục browser tạm cũ vẫn được ghi là chưa dọn, không gộp thành PASS cleanup toàn bộ.
- Trạng thái: **kit đã đóng gói/HTML Nhà đã dựng và kiểm; Nhà chờ chủ trì xem**. G01 vẫn đã duyệt 9/10. G02/D0 chưa áp dụng; tài sản 0.4/QMD/CSS/JS/HTML/PDF production giữ nguyên. Không render production, commit/push/phát hành hoặc khóa 0.5. Phạm vi chưa kiểm: trình duyệt khác, thiết bị thật, screen reader.
- Bước tiếp: chủ trì trải nghiệm HTML Nhà; agent ghi/xử lí cảm nhận. Chỉ sau đó và khi được giao mới mở G02/D0, rồi hồ sơ đề xuất 0.5. Chủ trì không phải cung cấp ý tưởng thiết kế hay tự vận hành CLI.
- `de_xuat_0_5`: `mau_web_dung_chung_da_tach_dau_vao_0_5_Nha_cho_duyet`; không đổi phiên bản/adoption thành 0.5.

### WEB04-FB-026 — Nhà được phản hồi tốt; khôi phục footer mà đóng băng thiết kế phía trên

- Ngày 08/10/2026, chủ trì: “Rất tốt. Mình đã xem trang Nhà khóa học”, chỉ còn footer biến mất; yêu cầu thiết kế lại footer nhưng trước tiên không làm thay đổi thiết kế hiện tại. Sau kế hoạch bổ sung riêng trong prototype, chủ trì giao “OK. Thực hiện theo kế hoạch của bạn.” Chỉ phần footer mới chờ xem; không hạ lại phản hồi tốt của Nhà hay G01 9/10.
- Nguyên nhân xác minh: builder lấy content root rồi thay shell, không mang theo `website.page-footer`. Footer vẫn có trong cấu hình/HTML production; không phải bị CSS ẩn. Checker trước chưa phân biệt footer website với `prototype-note` trong Ủng hộ. Fragment footer cũ không được cấu hình sử dụng, không phải nguồn hợp lệ.
- Nguồn sửa: `templates/page.html.tpl`, template/CSS footer mới và hai script preview/check trong kit. Nội dung footer từ `_quarto.yml`, không viết một bản dữ liệu liên hệ mới. Mọi CSS dưới `.zo-site-footer`; không thay CSS/JS hoặc markup phần phía trên. Chỉ bật cho Nhà qua `--footer-baseline`, không thêm footer vào G01 đối chứng.
- Guard: đúng landmark contentinfo, ngoài main/Ủng hộ, đủ sáu link và bản quyền/đích canonical; ca âm xóa footer vẫn phải bị phát hiện khi còn prototype-note. Khóa DOM/hashes cũ, so toàn bộ hình học/chữ/màu phía trên trên năm viewport và ảnh bìa/đọc/Ủng hộ desktop/mobile; không tràn/che bởi nút mục lục, đích 44px, bàn phím/no-JS/sáu nền/sắc xám. Ghi cách dùng lại ở `kiem_thu.md`, không tự nâng thành quy chuẩn toàn repo/0.5.
- Bằng chứng: audit riêng `_audit/zo_web_2027_footer_2026-10-08/`: `bao_cao.md`, baseline, manifest, QA/layout/pixel JSON và 42 ảnh. 814/814 kiểm đạt; 49 tài sản có hash, 1572 tệp bảo vệ không đổi. DOM cũ và computed layout/type/color giữ nguyên, CSS/JS/profile/template cũ cùng hai HTML trước không đổi, G01 kit byte-identical. Dựng lặp lại không đổi tám hash runtime/manifest.
- Sai lệch checker ở lần đầu: parse hai lần trên một phía gây khác serialize void element; chín pixel khử răng cưa chênh 1/255. Sửa phép so đối xứng, ghi giới hạn lượng tử (không nới tọa độ/màu CSS), chạy lại toàn bộ. Không sửa UI để làm PASS hoặc dùng kết quả cũ chứng nhận bản mới.
- Trạng thái: **đã sửa/đã kiểm trong prototype, footer mới chờ chủ trì xem**. Không sửa/render production hoặc PDF; không commit/push/phát hành, mở G02/D0 hoặc khóa 0.5. Chưa Safari/Firefox, thiết bị thật/screen reader, chưa kiểm trực tiếp URL mạng. Profile tạm run cuối đã dọn; phần dư cũ FB-025 vẫn ngoài phạm vi và được báo riêng.
- Bước tiếp: xem riêng footer ở HTML Nhà mới; không mở lại vòng thiết kế. `de_xuat_0_5: footer_component_va_guard_dau_vao_chua_duyet_thi_giac`.

### WEB04-FB-027 — Footer được duyệt; viết đầy đủ câu nhận diện và đưa chấm nền lên toolbar

- Ngày/phạm vi: 08/10/2026. Chủ trì phản hồi “Tốt, rất tốt” về footer FB-026: **footer đã được duyệt**, không còn chờ xem. Giao hai tinh chỉnh nhỏ trong HTML thử nghiệm Nhà/G01, không mở lại thiết kế đã chốt.
- Câu dùng mới: “Học trong kỉ nguyên trí tuệ nhân tạo, học để tìm lại chính mình.” Thay ở rail Nhà/G01 và footer Nhà. Một hằng trong builder cấp cho template, không đổi tài sản/logo khóa 0.4. Câu dài hơn tự xuống dòng; đây là thay đổi được yêu cầu, không phải sửa bố cục vùng đọc.
- Vướng mắc UI: dropdown che lựa chọn, mỗi dòng lặp radio + chấm màu + tên; các nhãn làm bộ tùy chỉnh cồng kềnh. Thay bằng sáu vòng tròn màu trên một hàng ngay toolbar, mỗi vòng tròn là radio native với viền báo đang chọn; không còn chữ “Nền” hoặc tên màu hiển thị. Tên giữ trong nhãn truy cập/chú giải khi trỏ chuột. Nút tròn nửa sáng–nửa tối bật/tắt Sắc xám, có `aria-pressed` và focus rõ; không bỏ chức năng hoặc dữ liệu lựa chọn đã lưu.
- Nguồn sửa: kit `templates/page.html.tpl`, `templates/site-footer.html.tpl`, `templates/appearance-inline.html.tpl`, `appearance-inline.css`, `site-ui.js`; hai script preview/check. CSS mới giới hạn ở bộ tùy chỉnh/header chứa nó. Bản kiểu cũ còn được hỗ trợ để đối chiếu lịch sử, không sửa HTML đã duyệt. Hợp đồng/README/kiểm thử kit ghi quy tắc mới; không tự phong thành quy chuẩn 0.5/toàn repo.
- Đầu ra/bằng chứng: `_audit/zo_web_2027_tuy_chinh_2026-10-08/`, hai HTML Nhà/G01, `bao_cao.md`, manifest, QA/layout/pixel JSON và 58 ảnh. Dựng qua `--ui-baseline` trỏ tới Nhà có footer đã duyệt. Dựng lặp lại không đổi chín hash runtime/manifest.
- Guard: 1057/1057 kiểm đạt. Kiểm đầy đủ trên 390/768/1000/1440/1920px; thêm UI Nhà/G01 ở 320/360/375px. Sáu radio + nút Sắc xám cùng hàng, không tràn/đè logo, vùng bấm ít nhất 24×44px; chọn thực bằng chuột, phím mũi tên, Enter, lưu/tải lại và tắt sắc xám. Giữ sáu token nền, giấy đọc trắng, controller R1/ID/nội dung/luồng/nhịp đọc. DOM còn lại sau khi loại đúng hai thay đổi được yêu cầu phải trùng; toàn bộ computed layout/type/color của main không đổi; ảnh main đối chiếu bìa/đọc/Ủng hộ có chênh kênh tối đa 0.
- Ngăn tái diễn: không thay radio bằng chấm trang trí không tương tác; trạng thái chọn/focus phải nhìn thấy; không mất Sắc xám khi bỏ nhãn; không cho dãy chấm đẩy toolbar thành hai hàng trên màn hình nhỏ. Không áp dụng guard đóng băng toolbar/rail cũ cho chính hai vùng được yêu cầu sửa, nhưng không nới bảo vệ nội dung chính.
- Trạng thái: **hai tinh chỉnh đã làm/đã kiểm, chờ chủ trì xem riêng**; footer đã duyệt, G01 9/10 và phản hồi tốt về Nhà giữ nguyên. 10 tệp đóng băng và 1572 tệp bảo vệ không đổi. Chưa kiểm browser khác/cảm ứng thật/screen reader; tên truy cập và bàn phím đã kiểm không thay kiểm screen reader. Profile tạm lượt này đã dọn; không tác động phần dư FB-025.
- Không sửa/render QMD/CSS/JS/HTML/PDF production, commit/push/phát hành, mở G02/D0 hoặc chốt 0.5. `de_xuat_0_5: tuy_chinh_truc_tiep_va_cau_nhan_dien_day_du_dau_vao_cho_xem`.

### WEB04-FB-028 — Chốt FB027; HTML thử nghiệm R1-G02 dùng kit đã duyệt

- Ngày/phạm vi: 08/10/2026. Chủ trì **chốt hai tinh chỉnh FB027** và giao HTML G02, giữ nội dung toán/ID/luồng; tự kiểm, ghi lỗi chống tái diễn. Không production/PDF/phát hành, D0 hoặc khóa toàn bộ 0.5.
- Bổ sung current FB029: kiểm local của lượt này không chứng minh kiến trúc G02 đã đồng bộ với G01. Lượt đối sánh mới tách rõ lỗi trình bày đã sửa và các thiếu hụt Nền/Nhật kí/CP/Ôn lại còn mở; không viết lại bằng chứng lịch sử bên dưới.
- Nguồn dùng lại: kit `_design/web_2027_mau_dung_chung/`; CSS/JS/template shell/giấy/nhận diện/tùy chỉnh đã duyệt giữ nguyên. Profile `profiles/r1-g02.json` khóa nhịp G02; `r1-g02-adapter.css` chỉ kết cấu download/Ủng hộ và khoảng cuộn. `scripts/zo_web_2027_g02.py` được preview/check CLI hiện hành điều phối. Không sao chép 154 vùng hoặc 12 view G01.
- Đầu ra: `_audit/zo_web_2027_g02_2026-10-08/g02-reading.html`, báo cáo, manifest/hash, QA và ảnh. 112 vùng đọc gồm Ủng hộ; 10 view nguồn, Cách học mặc định; 11 bài luyện theo thứ tự hiện có và 5 bài kiểm tra. Bảo toàn nguyên văn/thứ tự, 1074 công thức, ID, heading, disclosure, mọi link/download và alt/caption.
- Giới hạn hiện trạng: G02 không có Ôn nền, Nhật kí hoặc CP độc lập như G01. Không tạo thẻ rỗng hoặc thêm nội dung để đủ khuôn; không xác nhận G02 đã đạt toàn bộ kiến trúc đích hay nghiệm thu mới nội dung toán. PDF cũ chỉ giữ link; không dựng/đồng bộ/kiểm PDF trong lượt này.
- G02-WEB-001, **lỗi thật đã sửa trong prototype**: nguồn ID task/solution nằm dưới nhãn của paper; offset 88px khiến nhãn deep-link sát/che một phần dưới toolbar 64px. Nguyên nhân xác minh từ ảnh + tọa độ DOM. Sửa `r1-g02-adapter.css`: khoảng cuộn ID G02 128px, không đổi inset/chữ/bố cục. Guard role của L06/KT03/lời giải L06 phải ở dưới toolbar ở 390/1440; chụp lại và chạy lại bản cuối.
- G02-CHECK-001, **lỗi scope checker, không phải lỗi thiết kế**: grid Ủng hộ có cột logo 60px + gap 24px nên heading cách trục prose 84px. Checker đầu ép trục prose cho cả grid, báo 40 FAIL. Sửa scope đúng component như G01, kiểm riêng text axis `.support-content`, giấy trắng và full reader width. Không sửa UI để che FAIL, không nới guard prose. `qa-first-run.json` giữ kiểm đầu.
- G02-CHECK-002, **phân biệt quyền viết hồ sơ với production**: snapshot rộng gồm cả README điều hành; khi cập nhật hồ sơ được giao, guard cũ gọi đó là thay production. Checker ghi hash trước/sau của đúng ba hồ sơ được cấp quyền riêng; mọi QMD/CSS/JS/HTML/PDF/tài sản và mốc cũ vẫn phải bất biến. Không loại cả thư mục khỏi bảo vệ.
- Các lỗi build đầu (API BeautifulSoup `before` không có; parser XML phụ thuộc không cài) sửa bằng `insert_before` và ElementTree chuẩn; không cài phụ thuộc, không bỏ kiểm. Đối chiếu công thức xử lí riêng hai dòng alt hình (8 TeX trong alt không là MathML hiển thị); sau đó chuỗi 1074 công thức phải khớp chính xác, alt/caption vẫn kiểm riêng.
- Guard: tám viewport 320–1920px, mọi view và mọi disclosure mở; nhãn/heading trong giấy, một inset/không giấy lồng, khoảng cách, chiều rộng, không tràn toàn trang; tỷ lệ nhãn hình bằng chữ, local scroll; chọn nền/sắc xám/bàn phím/lưu lại; drawer/Escape/focus/chọn view; rail/toolbar không giật; deep-link, đề–lời giải–trở lại–Back, no-JS. Negative fixture bỏ math/đổi ID/lệch nhãn 8px phải bị phát hiện. Số đạt cuối và hash hiện hành lấy ở `qa-results.json`/báo cáo, không lấy PASS bản trước.
- Trạng thái: **FB027 đã được chủ trì duyệt; G02 đã dựng/tự kiểm, chờ chủ trì xem HTML**. Các mốc G01/Nhà/footer giữ nguyên. Chưa Safari/Firefox, thiết bị cảm ứng thật, screen reader hay kiểm URL ngoài mạng. `de_xuat_0_5: nhan_ban_kit_va_profile_nhip_doc_G02_dau_vao_chua_duyet_G02`.

### WEB04-FB-029 — Đối sánh triệt để G01/G02; không đánh đồng cùng CSS với cùng kiến trúc

- Ngày/phạm vi: 08/10/2026. Chủ trì yêu cầu ma trận thiết kế, logic học, nội dung, trình bày cùng nội dung; liệt kê và sửa lỗi cũ vì hai gói thiếu nhất quán. Giữ giới hạn prototype, không production/PDF/phát hành, đổi toán/ID/luồng hoặc khóa 0.5.
- Nguyên nhân xác minh: G01 đã chuyển kiến trúc; G02 mới thích nghi shell quanh nguồn cũ. Builder G02 dùng nhãn chương/view thay chức năng, chưa kế thừa guard header rỗng, giới thiệu ngoài section lặp mọi view, class tải không khớp selector; footer G01 chưa được mở trong lượt footer Nhà. Kiểm FB028 chỉ local/preservation, không kiểm tương đương chức năng liên gói. Agent nhận thiếu sót này; không yêu cầu chủ trì cung cấp ý tưởng thiết kế.
- Đầu ra: `_audit/zo_web_2027_g01_g02_doi_sanh_2026-10-08/`: 46 tiêu chí (`ma_tran_doi_sanh.md`, `matrix.json`, `index.html`), inventory đầy đủ heading/task/table/hình/disclosure/route trước/sau, canonical line pointers, nguyên văn đủ 28 bản ghi trước trong `old-defects.json`, hai HTML mới, QA và ảnh. Không xóa/sửa ngược phản hồi lịch sử.
- Sửa prototype: taxonomy nhiệm vụ/lý thuyết, nhãn bảy câu dừng, ghép một header rỗng đúng thứ tự, giới thiệu chỉ ở điểm vào/Toàn văn (no-JS đọc đủ), alias danh sách tải, cùng footer trên G01 đối sánh mới. G02 112 → 111 vùng; G01 154 vùng giữ nguyên. Chuỗi văn bản/MathML/ID/heading/disclosure phải bất biến, không chỉ giữ số lượng. Snapshot FB027/FB028 và toàn bộ production giữ hash.
- Nguồn/guard: `scripts/zo_web_2027_g02.py`, adapter CSS; mô-đun `scripts/zo_web_2027_compare.py` do CLI preview/check hiện hành điều phối qua `--compare`. Hợp đồng/lỗi riêng ở `_design/web_2027_mau_dung_chung/doi_sanh_lien_goi.md`. Kiểm đúng self-or-ancestor của nhiệm vụ section/div, không PASS tập rỗng; không so summary mục lục với guidance; hai phía tuple/list dùng cùng schema. Ca âm typography/inset và các guard cũ giữ nguyên.
- Khoảng cách còn mở: Bắt đầu riêng, chặng/CP có quyết định và đường quay về, Nền theo nhu cầu, Nhật kí 14 trường, ba bài Ôn lại định danh/lời giải/CP riêng, tách chuyển giao khỏi lõi, wording mã quản lí. Đây là thiếu hụt kiến trúc được ma trận đánh CÒN THIẾU, không phải khác biệt hợp lệ do nguồn cũ thiếu. Không tự tạo thẻ rỗng hoặc bịa bài mới để làm PASS.
- Trạng thái: đã sửa/kiểm lớp trình bày, **chưa đồng bộ toàn bộ và chưa được chủ trì duyệt G02 mới**. QA cuối trong hai báo cáo cùng audit, không dùng số kiểm lịch sử chứng nhận bản mới. Không thẩm định lại chân trị mọi đáp án, PDF, trình duyệt khác Edge, thiết bị thật, screen reader hoặc URL mạng.
- Việc tiếp theo đề nghị: giao nhiệm vụ chuyển kiến trúc G02 ở nguồn theo ma trận và chốt hợp đồng ID/luồng trước khi viết; không mở vòng thiết kế khác. `de_xuat_0_5: guard_doi_sanh_lien_goi_dau_vao_chua_duyet_G02`.
- Bằng chứng cuối: 876/876 kiểm liên gói ở 1440/430/390px và 1089/1089 hồi quy G02 ở tám độ rộng; 42 + 37 ảnh. Các snapshot đã duyệt/production giữ hash; ba hồ sơ điều hành được phép đổi ghi hash trước/sau riêng. Hai browser profile cuối đã dọn. Không dùng các số này đóng 13 dòng khoảng cách kiến trúc trong ma trận.

### WEB04-FB-030 — 08/10/2026: khung bìa trong suốt, đồ thị/bảng và vùng hình 0.4

- **Yêu cầu gốc:** chủ trì muốn ảnh toán làm bìa không có nền; khung vuông/dọc/ngang, mỗi dạng hai kích thước; sáu nền sáng/tối Đỏ/Vàng/Xám ZO. Đồ thị và bảng theo 0.4; định nghĩa vùng chèn hình. Chủ trì duyệt kế hoạch và giao bắt đầu. Mốc đầu là HTML mẫu riêng, không đổi G01 hiện hành trước khi xem mẫu.
- **Nguồn:** profile riêng `_design/web_2027_mau_dung_chung/figure-profile-candidate/`; `zo_graph_build.py` thêm lựa chọn 0.4, `tex/zo_graph_v04.tex` mới; `mau/cover_cubic_04.tex` giữ hàm/cửa sổ/A–B–C của hình 02. Renderer `zo_variation_html.py` dùng JSON và validator/converter token hiện hành, tạo MathML bằng Pandoc; không sửa QMD, JSON, SVG canonical, Lua/CSS hiện hành hoặc bản style v0.2.
- **Đã thực hiện:** mẫu bìa có ba dạng × hai kích thước và sáu token nền từ palette 0.4; ảnh sáng/tối trong suốt. Ba đồ thị G01 dựng lại trong audit, đủ 13 bảng native cùng dữ liệu/ID/cờ cố ý sai/cột loại/giới hạn một phía. Bộ chọn khung chỉ dành cho biên soạn, không thêm tùy chọn người học. Hình bài giữ kích thước tự nhiên và cuộn riêng khi hẹp; nhãn/tiêu đề/hình/chú thích thuộc vùng đọc, không lồng vùng đọc.
- **FIG-030-01 — đã xác minh và sửa:** ở 320 px, ảnh có thể vượt khung ngang do kích thước nội tại và max-height phần trăm trong bố cục grid chưa ràng buộc đủ. Sửa tại `figure.css`: hộp ảnh định vị trong inset khung, object-fit contain giữ toàn hình/tỉ lệ. Guard kiểm đủ 144 tổ hợp viewport/dạng/cỡ/nền và sự chứa ảnh; không chữa bằng overflow:hidden để giấu phần bị cắt.
- **FIG-030-02 — đã xác minh và sửa:** tăng cỡ chữ hình làm nhãn hàm v của hình giá trị tuyệt đối chạm nhãn trục. `absolute-value-labels.json` dịch riêng hộp chữ sang phải và chuẩn hóa cỡ tiêu đề; CLI giữ nguyên nội dung toán/tọa độ, yêu cầu nhãn khớp đúng một node, giới hạn dịch theo pt. Nguồn G01 không đổi. Đã xem lại ảnh desktop/mobile; không tuyên bố có máy phát hiện mọi va chạm.
- **QA-030-01 — đã xác minh và sửa phép kiểm:** ảnh chụp ngay sau scroll có thể chưa có SVG được vẽ, mặc dù decode/loaded đã đạt. Checker chờ paint sau scroll và kiểm pixel đường đỏ trên ảnh thật; không dùng loaded thay kiểm trực quan. Không sửa tài sản để làm PASS.
- **Hồi quy lỗi cũ:** guard cỡ bảng bằng văn bản, ảnh bài bằng naturalWidth, không tràn trang, cùng inset/giấy trắng, không nhãn ngoài vùng đọc hoặc vùng lồng; đối chiếu từng ô nguồn, cột loại và cờ cố ý sai. Mặc định công cụ vẫn v0.2; dựng hình 01 trùng SHA SVG canonical `ae76e97b17ad3ce970d1e11c01113b21d9dcaede57a6a0b9d61a16c41f0f1245`.
- **Bằng chứng:** `_audit/zo_math_figure_profile_2026-10-08/` có HTML, SVG/PDF vector hình, manifest, QA và 18 ảnh. Lượt cuối 1108/1108 kiểm đạt ở 1440/430/390/320; 669 tệp bảo vệ không đổi, gồm G01 production, nguồn toán và 06/07 immutable. PDF trong audit chỉ là vector hình do toolchain yêu cầu, không dựng PDF học liệu. Profile browser riêng đã dọn.
- **Còn mở:** chờ chủ trì duyệt HTML; chưa nối renderer bảng vào QMD hay migration G01; chưa kiểm đủ bộ bảy dạng đồ thị, trình duyệt khác, cảm ứng thật, screen reader hoặc bản in grayscale. Bìa trong suốt hiện chặn điểm rỗng/pagecolor để không làm sai dữ kiện; trường hợp đó cần giải pháp mask riêng. G02 còn thiếu kiến trúc, không đóng việc bằng PASS mẫu hình.
- **Trạng thái:** `cho_nguoi_chu_tri_duyet`; đã sửa/kiểm không đồng nghĩa đã duyệt/phát hành. Đầu vào ứng viên 0.5, chưa sửa quy chuẩn khóa 0.4, version, commit/push hoặc phát hành.

### WEB04-FB-031 — Duyệt FB030; tích hợp hình/bảng vào nguồn HTML G01

- **Chỉ thị và phạm vi:** chủ trì duyệt bảng thiết kế FB030, xác nhận mẫu riêng
  không thay giao diện G01 đã chốt, rồi giao bắt đầu bước tích hợp. Giữ shell,
  vùng đọc, toán/ID/luồng; chỉ thay payload bìa/đồ thị/BBT. Không PDF học liệu,
  G02, Video/M8.R, commit/push/phát hành hoặc khóa 0.5.
- **Nguồn:** `giao_dien/web_2027_figures.json`, bốn sidecar title/05/09/10,
  15 SVG web/manifest riêng; `scripts/zo_web_2027_figures.py`, hook production,
  CSS figure opt-in. QMD/JSON toán/TeX/PDF lịch sử và layout đã duyệt không sửa.
  Native MathML dùng renderer chung từ cùng JSON, giữ caption QMD, cột loại
  và lỗi cố ý. Không hiển thị tên JSON nội bộ thay caption bài học.
- **WEB-FIG-031-01 — đã xác minh/sửa bộ nối:** fallback/caption có hai vị trí
  DOM; selector chỉ trong viewport gây bỏ sót 11 bảng. Chuyển selector tới
  figure sở hữu và giữ vị trí caption. BBT13 fallback ∥ cần đối chiếu theo
  excluded_columns; native vẫn giữ “Không xác định” trong data/aria. Guard
  đủ mọi ô của 13 bảng, không nới so sánh ngoài cột loại.
- **WEB-FIG-031-02 — lỗi thị giác thật:** sau font 17px, hai nhãn công thức
  hình 05 chồng nhau, nhãn hình 09 đè tick y, nhãn (-1;-9) hình 10 sát trục.
  Không lấy PASS máy làm lý do bỏ qua. Chỉ dịch hộp nhãn qua sidecar có ràng
  buộc số pt và khớp đúng một node; không thay điểm/đường/biểu thức. Dựng lại
  qua tool, giữ ảnh trước/sau, xem toàn hình ở cỡ tự nhiên. Hàng rào tiếp tục:
  mọi graph mới phải rà ảnh, không chỉ loaded hoặc đếm số SVG.
- **WEB-CHECK-031-01 — lỗi checker, không đổi UI để che FAIL:** kiểm cỡ bảng
  phải theo figure/ngữ cảnh lời giải, không so mọi bảng với 17px gốc; kiểm
  tách Nhật kí dùng ID thật g01-o01 và bắt cả hai đích tồn tại, không PASS
  tập rỗng. WinError cache đường dài ngoài gói và token “lỗi” trong nhãn Sửa
  lỗi là vấn đề hạ tầng/rút gọn log, không kết luận thành lỗi toán hay giao diện.
- **Bằng chứng hiện hành:** `_audit/zo_g01_figure_integration_2026-10-08/`,
  README, before.json, qa-results.json, first-run-issues.md, ảnh 13 hình và
  toàn trang. QA trước rà nhãn giữ riêng qa-before-label-review.json; không
  dùng để chứng nhận HTML cuối. Giới hạn browser và kết quả promote ghi tại đó.
  Kiểm cuối đạt **782/782** tại 1440/430/390/320px; HTML cục bộ đã được đưa
  vào docs qua guard hash HTML và toàn bộ tài sản. `handoff.json` kiểm lại
  sau bàn giao; không dùng số PASS để thay nghiệm thu của chủ trì.
- **Trạng thái:** FB030 **đã được chủ trì duyệt**; HTML tích hợp mới chỉ đã
  dựng/tự kiểm và còn chờ chủ trì xem riêng. Mốc G01 9/10/Nhà/footer/FB027
  giữ nguyên. Không tuyên bố PDF đồng bộ, G02 hoàn thiện hoặc Design 0.5.

## WEB04-FB-032 — Tải PDF ba cột và drawer chỉ biểu tượng (08/10/2026)

- **Phản hồi/chấp thuận:** chủ trì đã xem HTML FB031 và nói “tất cả đều ổn”,
  chỉ yêu cầu mục tải PDF đơn giản, rõ chức năng hơn và bỏ chữ khỏi nút mở
  điều hướng. Ghi nhận phần hình/bảng và các phần còn lại được xem ổn;
  hai tinh chỉnh mới chưa được chủ trì xem, không mở lại thiết kế đã duyệt.
- **Hiện trạng/nguyên nhân:** hai bản toàn bộ dùng article không có lớp
  trình bày phù hợp trong shell mới, sáu bản phần dùng kiểu hàng khác và
  không hiện số trang. Nút drawer ghép nhãn view vào chữ mục lục, dư độ rộng.
- **Sửa canonical:** `scripts/zo_web_2027_downloads.py`, nối từ hook
  `scripts/zo_web_2027_production.py`; scoped CSS G01 ở
  `hoc_lieu/r1_g01/giao_dien/downloads.css`. Tám thẻ cùng ba cột desktop,
  mobile copy trên/page count + nút dưới; giữ mọi tiêu đề/mô tả/URL/download.
  Số trang đọc từ PDF thật, không dựng PDF. Nút SVG ba gạch 52px giữ
  aria-label/title/controls/expanded và JS chung. QMD/layout/toán/ID không đổi.
- **WEB-DOWNLOAD-032-01:** khi thay câu trạng thái PDF, bản đầu đã bỏ cụm
  “khi cần đối chiếu lời giải” vì thay cả text node. Rà ảnh phát hiện;
  sửa replace đúng câu và thêm guard giữ hướng dẫn. Không bàn giao bản lỗi.
- **WEB-CHECK-032-01:** CDP Enter đầu thiếu text carriage-return, không
  kích hoạt native button. Sửa checker gửi đủ sự kiện, kiểm focus rồi mở
  thật/đóng bằng Escape; không sửa UI để che FAIL. Báo cáo đầu giữ riêng.
- **Guard/bằng chứng:** `_audit/zo_g01_downloads_2026-10-08/README.md`,
  qa-results.json **164/164**, ảnh 1440/390/320, DOM ngoài hai vùng chính xác,
  toàn bộ MathML/ID, 154 vùng/14 trường, tám PDF byte-identical/count/link,
  bảy viewport, sáu nền/Sắc xám, bàn phím/no-JS. Negative fixtures sửa
  heading/URL bị phát hiện; Git index và 740 tệp bảo vệ ngoài HTML không đổi.
- **Trạng thái:** nguồn và HTML cục bộ đã sửa/kiểm; hai tinh chỉnh chờ chủ
  trì xem. Các PDF đang có **chưa đồng bộ** với HTML mới, có thông báo đúng
  trên mục tải. Chưa PDF mới, G02/D0/Nhà, Design 0.5, commit/push/phát hành.
  Chưa kiểm Safari/Firefox, screen reader hoặc cảm ứng thật; cảnh báo navbar
  ngoài chuyên mục thuộc mirror kiểm cô lập, không âm thầm sửa trang khác.

## WEB04-FB-033 — Chốt HTML G01 FB032 và bảo vệ nguồn dùng lại

- **Phản hồi chủ trì:** “Mình đã xem kết quả, tốt.”; giao thực hiện bốn điểm ghi nhận duyệt, hợp đồng dùng lại, guard chính thức và dựng nguồn đối chiếu.
- **Đã duyệt:** HTML G01 sau FB031/032, SHA `8b3a9a1ad532e72951edb415d9ab32a37990a80e13c2d754a2f57028fedc764a`. Đóng chờ xem FB032, không hạ phần đã duyệt hoặc lấy g01-kit cũ thay mốc mới.
- **Nguồn:** receipt `content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/giao_dien/web_2027_accepted.json`; QMD vẫn canonical. Hợp đồng vùng đọc/figure/BBT/download/drawer cập nhật trong kit, tách quy tắc chung khỏi số vùng/view/nhiệm vụ riêng. Chưa khóa 0.5.
- **Guard chống tái diễn:** `scripts/zo_web_2027_g01_checkpoint.py`; check/rebuild không tự thay receipt. Khóa bytes nguồn/HTML/runtime/ID/toán/PDF, ownership vùng, nhật kí 14 trường; đo bốn viewport, view thật, drawer/bàn phím/no-JS/nền và cuộn. Không phụ thuộc HTML/audit mirror lịch sử.
- **Lỗi hạ tầng kiểm phát hiện:** mirror đầu thiếu Markdown include cấp gốc khiến Quarto dừng; bổ sung nguồn cấp gốc vào mirror, không sửa QMD. Checker đầu chọn `[data-view]` không tồn tại trên tab thật; sửa sang `button.r1-tab[id]` và kiểm `#r1-view-panel.dataset.r1View` sau mỗi deep link. Không gọi hai lỗi kiểm này là lỗi HTML. Guard: render phải thành công và đủ 12 view thật; không chạy vòng lặp rỗng rồi báo PASS.
- **Bằng chứng:** `_audit/zo_g01_html_checkpoint_2026-10-08/README.md`, qa-results/handoff và báo cáo đầu giữ riêng. Dựng từ nguồn repo đã cho HTML/runtime byte-identical; 325 tệp và index không đổi, không promotion.
- **Kết quả cuối:** 398/398. Fixture đo inset ban đầu dùng padding trên span không đổi mép hộp đo nên FAIL 397/398; đổi fixture sang margin tạo lệch hộp thật và khôi phục style. Báo cáo FAIL được giữ; không sửa CSS trang để cho PASS. JSON thô lượt selector 71/75 không còn; `qa-root-check.json` là lượt root sau sửa, 367/367, không được gọi là báo cáo đầu đó.
- **Giới hạn:** Edge headless, chưa Safari/Firefox/cảm ứng thật/screen reader; không phải chứng minh toán. PDF vẫn chưa đồng bộ. G02/D0/Nhà, nguồn toán, 06/07, M8.R/Video không được thay; chưa Git/phát hành/0.5.

## WEB04-FB-034 — Hoàn thiện G02 từ nội dung sẵn có, DH_007

- **Yêu cầu:** “OK, Hãy bắt đầu hoàn thiện gói G02.” Theo chuẩn khóa 2027 và ma trận đối sánh, không lấy kiến trúc G01 lịch sử thay mốc đã duyệt. HTML trước, PDF/phát hành sau.
- **Nguồn sửa:** G02 `index.qmd`, kiến trúc/profiles/config và Lua; năm thẻ Nền canonical mới; TEX/SVG Nền mới; adapter, payload và checker trong scripts; `giao_dien/support-context.js` G02. Kit/CSS/controller chung và G01 đã duyệt chỉ được tái dùng, không mở lại thiết kế.
- **Kết quả:** Bắt đầu riêng; ba chặng luyện, tám checkpoint, chuyển giao có điều kiện; chín Nền thực; ba bài Ôn lại có lời giải/đích riêng, Nhật kí riêng đúng 14 trường. Toán và ID ngân hàng cũ giữ nguyên. 153 vùng do nội dung G02, không áp số 154 G01 làm chuẩn.
- **Lỗi đã xử lí:** thêm Nền nhưng lesson count còn 7 làm controller dừng; task heading cùng class bị tách khỏi đề; context Nền giữ đích G01; fragment suy đoán sai; mẫu Nền trùng bài thử lại; link L07 sai tuyến. Ghi triệu chứng/nguyên nhân/nguồn sửa/guard trong `_audit/zo_g02_completion_2026-10-08/first-run-issues.md`. Checker sửa giả định tên download và mapping mirror, không sửa UI để che FAIL.
- **Chống tái diễn:** kiểm `r1-tabs-ready` và 12 view thực; cô lập Ôn/Nhật, context từng CP/Ôn, reload/Back; ownership nhãn/tiêu đề cùng trục; không paper lồng; giữ ID/toán, link/download; sáu viewport/nền, icon drawer, scroll/no-JS, fixture âm. Đối chiếu computed style vai trò với G01 hiện hành.
- **Bằng chứng:** `_audit/zo_g02_completion_2026-10-08/README.md`; QA 985/985, toán mới 28/28, G01 398/398, 990 tệp bảo vệ và Git index không đổi; ảnh desktop/mobile đã rà. HTML SHA `f0d243bc60e54ecfbae1f0cfc0d55346d1e09ab1cccefea98084203bfc2907b4`.
- **Trạng thái:** nguồn G02 đã thay; HTML thử nghiệm chờ chủ trì xem, HTML production chưa thay. Cả tám PDF STALE, đã thông báo ở mục tải; phải cập nhật kiểm kê PDF bằng PDF thật khi được giao sau duyệt. Chưa stage/commit/push/phát hành hoặc khóa 0.5; M8.R/Video giữ nguyên. Chưa kiểm Safari/Firefox/cảm ứng thật/screen reader; kiểm toán mới không chứng nhận độc lập toàn bộ ngân hàng cũ.
## WEB04-FB-035 — Lệch semantic G02; tinh chỉnh nguồn, reuse Nhật kí

- **Phản hồi:** cùng vai trò bị đặt khác cấp/vùng, bảng trình bày khác nhau;
  lệch nhiều ngay trang đầu. Nhật kí dùng chung, không cần viết lại mẫu riêng.
  Chủ trì giao “Vậy tinh chỉnh lại nguồn của R1-G02 ngay đi.”
- **Nguyên nhân:** grouping prototype theo heading, không có đối sánh vai trò
  toàn trang; 985 ca layout không kiểm đúng cấp/nhóm semantic. FB034 chưa đạt
  theo phản hồi, không thể dùng báo cáo PASS của nó làm bằng chứng đã đồng bộ.
- **Nguồn sửa:** G02 QMD/config/Lua và `giao_dien/web_2027_layout.json`, adapter
  và checker; include chung `_dung_chung/nhat_ki_hoc_tap.qmd` nguyên G01.
  Cách học/định hướng/khởi động/Ôn nền, khái niệm/ví dụ/phương pháp/tự kiểm
  và 12 bảng được phân vai. Giữ toán/ID cũ, không sửa G01 đã chốt.
- **Chống tái diễn:** `scripts/zo_g02_consistency_check.py` khóa cấp/vai trò,
  ownership, reuse Nhật kí và kiểu bảng theo chức năng; fixture âm sai vai trò,
  cấp, thiếu trường và mode. Không lấy số vùng bằng nhau làm chuẩn. G01 vẫn
  inline đã khóa, G02 dùng include; kiểm nguyên nội dung giữa hai nơi.
- **Bằng chứng:** `_audit/zo_g02_consistency_2026-10-08/README.md`, ma trận,
  `first-run-issues.md`, semantic 144/144, layout 985/985, toán bổ sung 28/28,
  G01 398/398, 990 tệp bảo vệ không đổi. Ba công thức bị mất khi đổi tên tiêu
  đề được guard bắt và khôi phục trước bàn giao; không nới guard bảo toàn.
- **Trạng thái:** đã sửa/kiểm nguồn và HTML audit; **chờ chủ trì duyệt**, không
  chứng nhận độc lập toàn bộ toán/kiến trúc từ các số PASS. Chưa production
  HTML G02, tám PDF vẫn STALE, chưa Git/phát hành/0.5; M8.R/Video không đổi.

### WEB04-FB-036 — lỗi mới cần sửa cả G01 và G02

- **Ngày/người/phạm vi:** 08/10/2026, chủ trì ZO Math; hai nguồn QMD và HTML.
  Ảnh 205643 (hai action trùng), 210442/210647 (nhãn Tự kiểm tra trùng/rơi
  vào Ôn nền, lời giải mở). Chủ trì mở lại G01 để sửa rồi đồng bộ, sau đó
  đối sánh G02; chưa giao PDF, Git hoặc phát hành.
- **Yêu cầu cốt lõi:** bìa riêng G02; bảng/nhật kí header trái, chặng G01,
  tên ngắn, nhãn và lời giải đúng owner, Nền/disclosure đóng mặc định,
  routing Sửa lỗi cùng mẫu, Ôn lại và trang Nguồn nhất quán.
- **Nguyên nhân/nguồn sửa/guard từng lỗi:** 17 dòng có mã P36 tại
  `_design/web_2027_mau_dung_chung/doi_sanh_FB036.md`. Không biến lỗi selector
  QA thành lỗi trang; ghi cả lần tự kiểm phát hiện thứ tự chặng sai.
- **Hiện thực:** QMD G01/G02, shared journal include, layout binding G01,
  scoped consistency policy/CSS/controller và adapter. Cover G02 từ L02
  `g(x)=|x+2|` trên [-4;1], không nền, source/asset receipt kiểm hash.
  Hai action L06 khác chức năng, đổi nhãn chứ không xóa một đích hợp lệ.
- **Kiểm:** pair 1504/1504 ở sáu viewport Edge, ownership 122/122, G02
  985/985, toán bổ sung 28/28; QMD check PASS cả hai; 758 tệp bảo vệ không
  đổi ngoài G01 HTML được giao. Ảnh/QA/hash/provenance ở audit FB036.
- **Trạng thái:** đã sửa và kiểm; G01 đồng bộ HTML cục bộ, G02 HTML audit;
  **chờ chủ trì xem/duyệt bản sửa**. Receipt FB033 giữ nguyên lịch sử, trạng
  thái canonical G01 mở lại chờ duyệt. Chưa PDF học liệu/Git/phát hành/0.5.
- **Chưa kiểm:** trình duyệt khác Edge, cảm ứng thật, screen reader, audit
  độc lập toàn bộ toán và PDF. Không nhận PASS là bảo đảm tuyệt đối hết lỗi.
  M8.R/Video và Design 06/07 giữ nguyên; không nâng chuẩn toàn repo.

### WEB04-FB-038 — DH023/QD030: bảng 0.4 theo chức năng trên bốn trang

- **Ngày/phạm vi:** 11/10/2026, chủ trì giao rà mọi bảng Nhà/D0/G01/G02 và đưa tám loại bảng 0.4 thành quy tắc chung toàn khóa. Giữ bản chất toán, nội dung/ID/đường học.
- **Nguyên nhân xác minh:** consistency adapter/CSS và CSS D0 ép mọi header trái; table có liên kết thiếu lớp chuẩn; G02 bảng giá trị bị căn như dữ liệu số; D0 còn ảnh SVG bảng dấu kèm bảng ẩn.
- **Nguồn/guard:** owner 07/6.1.1, QD_030 tại 04, registry/chỉ dẫn agent/QMD/profile; kit `profiles/course-tables.json`, `course-tables.css`, `zo_course_tables.py` và bốn adapter canonical. Unknown/missing/duplicate table và dữ liệu native khác JSON chặn dựng; checker căn lề theo vai trò thay checker cũ. Hai hàng bảng giá trị giữ cặp đầu vào–giá trị cùng cột, không sửa dữ kiện để làm đẹp.
- **Bằng chứng/trạng thái:** `_audit/zo_course_tables_2026-10-11/` có trước/sau, QA, kiểm kê từng bảng, ảnh desktop/mobile và bốn HTML nguồn tươi. Chờ chủ trì duyệt; số QA không là đảm bảo tuyệt đối hết lỗi. Công việc/trạng thái chỉ ở 03. Không sửa root docs/PDF/receipt/Git index, nguồn khóa 06/07, Video/M8.R hoặc Design 0.5; chưa Safari/Firefox/cảm ứng thật/screen reader hay rà toán độc lập.

### WEB04-FB-037 — DH020 kiểm cụm và mẫu PDF D0 (lịch sử)

- **Ngày/phạm vi:** 11/10/2026; chủ trì giao xử lí danh sách đối sánh rồi nghiên cứu mẫu PDF D0 nếu không còn mục đáng sửa trong danh sách. Không phải duyệt kết quả mới.
- **Nguồn/nguyên nhân/guard:** 13 lỗi và 4 điểm làm rõ được xử lí trong QMD G01/G02, bộ dựng/kiểm dùng chung, gateway và con trỏ điều hành. Bảng từng lỗi, nguyên nhân, nguồn sửa, chống tái diễn và giới hạn ở `_audit/zo_2027_dong_bo_cum_2026-10-11/README.md`; không lặp định nghĩa kiến trúc tại nhật kí.
- **Kiểm:** cụm HTML 1093/1093; tình huống/hồi quy 150/150; G02 965/965; điều hành 137/137; 1268 tệp bảo vệ không đổi. Các kết quả không thay nghiệm thu chủ trì hoặc rà độc lập toàn bộ toán.
- **PDF:** mẫu bảy trang A4, bốn câu chọn từ 24 câu D0 hiện tại; logo/font/màu 0.4, ruột là ứng viên mới. Kiểm 14/14, xem cả bảy trang màu và trắng đen. Hồ sơ/receipt/QA tại `pdf-specimen/` trong audit. Không lấy ruột v1.3 làm nguồn nội dung hiện tại.
- **Trạng thái:** sửa/kiểm xong, chờ duyệt thiết kế. Không đổi root docs/PDF production/receipt, hợp đồng D0 HTML-only, Design khóa 06/07, M8.R/Video hoặc Git/phát hành/0.5. Chưa in thật/PDF-UA hoặc kiểm đủ toàn bộ câu/hình D0. Bước tiếp do bảng điều hành 03 sở hữu.

