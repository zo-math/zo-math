# Ma trận phép chiếu nội dung D0

## Phép chiếu hiện hành 2026-10-02

`index.qmd` giữ nội dung bản HTML chủ dự án đã duyệt, không còn là đầu ra sống
của generator 6B. Năm phần công khai: Bắt đầu, Chuẩn bị, Làm khảo sát,
Đối chiếu bài làm, Chọn mạch ôn. Giao diện không có thẻ Toàn văn.
24 câu và Bài 00 giữ nguyên lời dẫn/toán; 25 đối chiếu công khai theo phạm vi
đã được duyệt. Metadata nội bộ, câu thử lại và hướng dẫn người tổ chức không
được đưa vào QMD công khai. BBT01 và hình hộp dùng tài sản vector canonical.
Kiểm toàn chuỗi từng phần và TeX bằng `noi_dung_da_duyet.json`.
Các ma trận PDF cũ là dự kiến lịch sử và không được triển khai: chủ dự án đã
chốt D0 là trang HTML-only ngày 2026-10-03. Tài sản PDF kỹ thuật và PDF lịch sử
vẫn được giữ nguyên, không phải đầu ra PDF nội dung của D0.
Phần dưới ghi phép chiếu cũ, không còn điều hành HTML hiện hành.

## Trạng thái và phạm vi

Tài liệu này khóa phép chiếu ngân hàng D0 v1.0 và lớp hướng dẫn đã biên tập ở Bước 6B sang `index.qmd`. Người dùng đã yêu cầu thực hiện Bước 6B; nghiệm thu nội dung biên tập và đầu ra vẫn là các cổng riêng.

`du_lieu/ngan_hang.json` vẫn là bản sao byte của dữ liệu lịch sử. `index.qmd` được tạo một lần bằng `cong_cu/tao_qmd_chuyen_doi.py` và phải khớp toàn chuỗi với kết quả của công cụ này trong giai đoạn chuyển đổi. Khi người dùng nghiệm thu QMD làm nguồn canonical, cơ chế sinh chuyển đổi phải được đóng lại hoặc đổi vai trò bằng một quyết định riêng.

## Ma trận trường dữ liệu

| Nhóm | Trường | HTML công khai | Vùng nội bộ trong QMD | Vai trò |
|---|---|---:|---:|---|
| Nhận diện nhiệm vụ | `id`, `title` | Tiêu đề và nhãn mạch/bài; ID chỉ ở thuộc tính máy đọc | Có | Tiêu đề, anchor và đối chiếu nhiệm vụ |
| Điều kiện giao bài | `prereq`, `format`, `minutes` | Có | Có qua bản ghi phép chiếu | Giúp chọn và tổ chức lượt khảo sát |
| Đề bài | `question` | Có | Có qua bản ghi phép chiếu | Nội dung nhiệm vụ chính |
| Phân loại chuyên môn | `version`, `r`, `n`, `objective`, `clusters`, `support`, `ct`, `source`, `level`, `capacity` | Không | Có | Hồ sơ biên soạn và phân tích |
| Chấm và phản hồi | `answer`, `solution`, `criteria`, `error`, `repair`, `check` | Không | Có | Dành cho người hướng dẫn |
| Thử lại | `retest_id`, `retest`, `reanswer`, `resolution` | Không | Có | Chỉ giao sau sửa; không lộ trong HTML |
| Quan hệ và xuất xứ | `family`, `history`, `author`, `scope` | Không | Có | Bảo toàn họ câu và provenance |

Mỗi trường trong 30 trường bắt buộc xuất hiện trong phép chiếu. Checker so sánh toàn bộ `index.qmd` với kết quả sinh xác định từ JSON và hai tài liệu hướng dẫn canonical; không dùng whitelist rút gọn và không chỉ so sánh số lượng. Ngân hàng JSON vẫn khớp byte với baseline; ba nguồn biên tập được khóa SHA-256 trong `editorial_contract` của manifest.

## Nguồn hướng dẫn

| Nguồn canonical từ Bước 6B | Vị trí trong QMD | HTML công khai |
|---|---|---:|
| `du_lieu/huong_dan_cong_khai.md` | `#bat-dau`, `#khai-bao-pham-vi`, `#doc-ket-qua`, `#thu-lai`, `#tai-pdf` | Có |
| `du_lieu/huong_dan_phan_tich.md` | `#danh-cho-nguoi-huong-dan` trong `.d0-private` | Không |

Hướng dẫn công khai được biên tập từ vai trò khảo sát trong Kế hoạch 0.6 và hai hướng dẫn lịch sử; không chứa đáp án hay câu thử lại. Hướng dẫn phân tích giữ toàn bộ nội dung ngoài 15 sai biệt được ghi chính xác trong `bien_tap_6b.json`. Checker đối chiếu toàn văn với bản lịch sử và toàn bộ danh sách sai biệt, từ chối thay đổi ngoài danh sách. Front matter và lệnh `\clearpage` được loại khỏi thân QMD như trước. Bản lịch sử không bị sửa.

## Anchor và quan hệ

- Mạch: `#mach-r1` đến `#mach-r8`.
- Nhiệm vụ chính: ID viết thường, ví dụ `#d0-r1-01`.
- Hồ sơ nội bộ: tiền tố `#ho-so-`, ví dụ `#ho-so-d0-r1-01`.
- Câu thử lại: ID viết thường, ví dụ `#d0-r1-sl01`.
- Lời giải: tiền tố `#loi-giai-` cộng ID viết thường.
- Quan hệ máy đọc được: thuộc tính `d0-id` và `d0-family` giữ nguyên chữ hoa của baseline.

## Ranh giới công khai

Toàn bộ nội dung dành cho người hướng dẫn nằm trong một `Div` có lớp `.d0-private`. `cong_cu/d0.lua` xóa `Div` này khỏi cây tài liệu khi định dạng là HTML. Không dùng CSS hoặc JavaScript để che nội dung. Bước 4 chỉ kiểm định hợp đồng nguồn; bằng chứng HTML thực tế phải chờ Bước 5 render và kiểm tra đầu ra.

## Chuyển đổi tài nguyên

Tham chiếu lịch sử `src/hinh_hop.pdf` được đổi kỹ thuật thành `hinh/hinh_hop.pdf`. Quy tắc sao chép hình byte-nguyên vẹn của Bước 4 đã được thay thế bởi pilot ZO Geometry được duyệt ở Đợt 5, theo mục tài sản hình học trong hợp đồng nguồn. Bản hình lịch sử vẫn bất biến; tài sản pilot và nguồn được khóa checksum trong manifest. Bước 6B chưa đổi định dạng nhúng hình; SVG cho HTML được xử lý ở Bước 6E.
