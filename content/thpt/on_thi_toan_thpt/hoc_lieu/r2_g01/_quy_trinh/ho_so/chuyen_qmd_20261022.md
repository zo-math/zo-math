# R2-G01 — Chuyển bản thảo 0.2 sang QMD

Ngày thực hiện: 22/10/2026. Phạm vi: chuyển nguồn sau khi chủ trì duyệt nội dung và diễn đạt; chưa dựng HTML/PDF hoặc commit. Trạng thái và việc tiếp theo do [03 — Điều hành](../../../../tot_nghiep_thpt/2027/_quy_trinh/03_dieu_hanh_chuong_trinh.md) sở hữu.

## Kết quả chuyển nguồn

[Nguồn index.qmd](../../index.qmd) giữ nguyên nội dung người học của [bản thảo 0.2 đã duyệt](../ban_thao/noi_dung.md). Bản thảo và năm tệp dữ liệu bản thảo được giữ nguyên từng byte. QMD hiện là bản chuyển để duyệt; không sửa tiếp bản thảo như một nguồn phát triển song song. [Biên nhận duyệt](duyet_ban_thao_02_20261022.json) chỉ xác nhận phạm vi chủ trì đã cho phép, không suy thành nghiệm thu QMD hay sản phẩm dựng.

Một tệp QMD chứa các phần riêng Bắt đầu, Bài học, Luyện tập, Kiểm tra, Ôn lại, Ôn nền, Sửa lỗi, Nhật kí, Lời giải và Nguồn. Giữ đủ 27 nhiệm vụ, 27 lời giải, 5 Gợi mở, 9 Ví dụ và 7 Điểm dừng; không đổi số thứ tự, thời lượng hoặc khoảng ghép nhóm. Lời giải dùng thành phần QMD chung, mặc định đóng. Bốn nhiệm vụ Sửa lỗi vẫn là phần dự trữ dùng chung theo chỉ dẫn đã duyệt; không nhân bản thành ba bộ bài.

Các thay đổi khi chuyển chỉ gồm:

- Đưa tiêu đề vào YAML; bỏ hai dòng quản lí bản thảo cũ khỏi phần người học. Thông tin phiên bản và duyệt nằm ở hồ sơ.
- Gắn mã ổn định, vai trò và vùng sở hữu vào phần học, nhiệm vụ, ví dụ, lượt ôn và điểm dừng. Giữ mọi mã điều hướng cũ; thêm tên đích tương thích với hệ dùng chung.
- Thêm liên kết cho các tham chiếu trong bảng, giữ nguyên chữ hiển thị; các tham chiếu Ví dụ dẫn đúng Ví dụ.
- Gắn 28 bảng của gói với kiểu bảng dùng chung; Nhật kí gọi một nguồn dùng chung với hai bảng sẵn có, không chép lại nội dung Nhật kí.
- Bổ sung cấu hình sản xuất, hồ sơ nguồn, hệ nhãn và dữ liệu chính thức. Không khai báo PDF chưa có, tài nguyên bìa chưa được chọn hoặc toàn bộ dữ liệu thành gói tải chung cho Học/Luyện.

## Dữ liệu theo từng phần

Các số dưới đây đếm số dòng giữ trong tệp, gồm cả dòng thiếu chiều dài nếu có; không phải tất cả đều là cỡ mẫu của một phép tính.

| Phần | Penguins | Bike Sharing | NOAA | Nhiệm vụ |
|---|---:|---:|---:|---|
| Học | 84 | 31 | 31 | 01–06 |
| Luyện | 50 | 29 | 31 | 07–14 |
| Kiểm tra | 52 | 31 | 30 | 15–18 |
| Ôn lại | 68 | 0 | 0 | 19–21 |
| Sửa lỗi | 90 | 0 | 28 | 24–27 |

[Dữ liệu và chỉ mục phân chia](../../du_lieu/phan_chia.json) trỏ đến năm tệp riêng. Mỗi bản ghi được đối chiếu bằng dòng nguồn Penguins, mã ngày Bike Sharing, hoặc cặp trạm–ngày NOAA: không trùng giữa các phần. Giá trị đo, thứ tự dòng, ô thiếu, ký hiệu T và các ký hiệu quan trắc khác giữ nguyên. Nhiệm vụ 22–23 thuộc Ôn nền dùng ví dụ số học giả định đã ghi rõ trong nội dung.

Các đoạn trích và bảng đã biên soạn vẫn thuộc đúng phần trong QMD. Việc dùng một tệp QMD không phải cơ chế khóa quyền xem; phân chia hiển thị và việc không lộ trước đề/dữ liệu khi học phải kiểm tiếp trên đầu ra khi được giao dựng.

## Kiểm chứng

- CLI `zo_qmd.py check` phiên bản 2.6.0: PASS, phạm vi chỉ nguồn R2-G01; nhận đúng dự án `on_thi_r2_g01`.
- Đối chiếu và kiểm cấu trúc nguồn: **959/959**, không lỗi; [kết quả chi tiết](chuyen_qmd_20261022.json). Đây là các kiểm tra tự động về nguồn, liên kết, metadata và bảo toàn, không phải 959 bài toán được giải lại.
- So sánh độc lập phần chữ người học: giống bản 0.2 sau khi bỏ cú pháp trình bày. Toàn bộ **778 biểu thức toán** và thứ tự của chúng giữ nguyên; đồng thời có đối chiếu đảo ngược từng thao tác chuyển.
- Mọi ID cũ được giữ; không trùng ID; các liên kết trong trang có đích; đề và lời giải ghép đúng số. Các khối QMD đóng/mở cân bằng.
- Dữ liệu chính thức giống dữ liệu đã duyệt, chỉ đổi trường trạng thái quản lí trong tệp mới. Giữ đủ 344 dòng Penguins, mỗi dòng ở đúng một phần.
- Kiểm điều hành hiện hành: **192/192**. Bộ tự kiểm quy tắc đã chạy trước khi chuyển: **250/250**.
- **3.147 tệp hiện có được bảo toàn** theo danh sách trước lượt chuyển; Git index không đổi. Bốn tệp có sẵn được sửa đúng phạm vi: README của gói; một đoạn R2-G01 tại 03; thêm riêng R2-G01 vào bảng kiểu bảng chung và sổ đối chiếu diễn đạt. Mọi mục cũ của hai sổ chung giữ nguyên giá trị.

Dấu SHA-256 bản thảo đã duyệt: `9de582583024dff638010e261c0af4dece7c5c212ba447f37ee78c84cf737d56`.

Dấu SHA-256 QMD sau chuyển: `83f169f8661d9b46478d2421ac349896fefa8a1fe831b1c8105928cc9f6181dd`.

## Giới hạn và điểm chờ duyệt

Chưa dựng, mở xem hoặc nghiệm thu HTML/PDF; chưa kiểm bố cục, tương tác, phân trang hay việc chọn riêng từng phần trên sản phẩm dựng. Các dòng PASS chung về cover/math assets chỉ là kiểm nguồn có áp dụng, không xác nhận đã chọn bìa hoặc đã kiểm hiển thị. Chưa chọn bìa cho R2-G01.

Không đổi schema kiến trúc R1 để ép Ôn nền cục bộ và Sửa lỗi dùng chung của R2 thành cấu trúc khác. Hệ nhãn, mục tiêu, điều hướng và phân chia dữ liệu của nguồn R2 được khai báo tường minh và qua kiểm nguồn dùng chung; không coi đó là chứng nhận toàn bộ manifest kiến trúc R1.

Không khảo sát lại giấy phép hoặc tính lại toàn bộ số học trong lượt này: giữ nguồn, giấy phép, giới hạn và nội dung toán đã duyệt, kiểm chính xác việc chuyển và bảo toàn. Không thay đổi các kết quả kiểm 0.1 hoặc hồ sơ rà diễn đạt 0.2 trong lịch sử. Không có đầu vào dựng nào phụ thuộc bản thảo hay audit.

Bản chuyển QMD chờ chủ trì duyệt. Chưa stage, commit, push hoặc phát hành.
