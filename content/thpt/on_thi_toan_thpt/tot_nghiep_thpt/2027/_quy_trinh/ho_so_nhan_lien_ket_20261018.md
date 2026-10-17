# Thống nhất nhãn liên kết đề–lời giải — 18/10/2026

Trạng thái: đã sửa và kiểm nguồn; chưa dựng lại HTML/PDF, chưa kiểm hiển thị thật sau sửa, chưa chủ trì duyệt, chưa commit/push/xuất bản. Các thay đổi điều hướng NAV-G04-01 của lượt trước được giữ nguyên.

## Kết quả và phạm vi

Quy tắc do chủ trì chốt: lượt đi **Xem lời giải**, lượt về **Xem đề bài**. Đã rà QMD G01–G04 và include được gọi, binding/bản đồ bố cục, bộ sinh, mẫu dùng chung và các cổng kiểm đang vận hành. Nhà và D0 không có các thao tác đề–lời giải tương ứng cần đổi.

| Gói | Nhãn đổi | Liên kết thao tác kiểm trong nguồn |
|---|---:|---:|
| G01 | 2 | 108 |
| G02 | 0 | 95 |
| G03 | 100 | 100 |
| G04 | 29 | 53 |
| Tổng | 131 | 356 |

G01 bỏ ngoại lệ “Xem đáp án câu xác nhận”/“Xem câu xác nhận”. G03 bỏ “Xem lời giải sau khi tự làm”, “Đối chiếu…”, “Trở lại đề”, các nhãn quay về trong lời hướng dẫn; sửa câu dẫn liên quan để đọc tự nhiên. G04 bỏ tên nhiệm vụ khỏi nhãn “Trở về đề — …”, thống nhất liên kết mở nhóm lời giải Kiểm tra. Điều kiện tự làm và hướng dẫn hỗ trợ vẫn còn trong nội dung liên quan; không đổi quyền bắt đầu Kiểm tra hoặc cơ chế đối chiếu.

“Xem công thức để kiểm tra” của G02 mở một phần công thức riêng, khác với lời giải nhiệm vụ; giữ nguyên. Tên mục Lời giải trong mục lục vẫn là tên mục. Các nguồn/bằng chứng lịch sử, bản thảo đã duyệt và chuỗi sai trong ca kiểm âm được giữ đúng vai trò, không dùng để sinh nhãn hiện hành.

## Nguồn đã cập nhật

- QMD chính thức: `hoc_lieu/r1_g01/index.qmd`, `r1_g03/index.qmd`, `r1_g04/index.qmd`. G02 đã đúng nên không sửa QMD.
- G01: `giao_dien/web_2027_layout.json`, đúng hai binding chữ và phần fingerprint văn bản tương ứng. Đối chứng raw trước sửa được xác minh khớp fingerprint của plan trước khi thay; danh sách toán, ID, disclosure giữ nguyên. Đây là di trú metadata nhãn ở mức nguồn, không phải một lần dựng HTML. Chờ kiểm với raw Quarto tươi khi được giao dựng; không dùng ghi chú này để bỏ cổng fingerprint.
- Nguồn câu chữ chung: `answer_actions` tại `_design/web_2027_mau_dung_chung/profiles/r1-consistency.json`. Bộ sinh G01/G02 gọi cùng nguồn; phạm vi profile có đủ bốn gói.
- Cổng nguồn và HTML: `scripts/zo_course_labels.py`, `scripts/zo_check_repo.py`, `scripts/zo_web_2027_consistency.py`; bộ sinh `scripts/zo_r1_g01_labels.py`.
- Kiểm hồi quy nguồn: `scripts/zo_course_answer_actions_selftest.py`.
- Quy tắc và cách gọi kiểm đặt tại 07/6.4 và quy trình 02; trạng thái tiếp tục chỉ ở 03. Hồ sơ này là bằng chứng, không phải bộ chuẩn thứ hai.

## Nguyên nhân và chống tái diễn

Các QMD/bộ dựng giữ cách gọi riêng theo gói; G01 còn một ngoại lệ câu xác nhận. Kiểm cặp/href/số lượng trước đó không buộc nhãn chính xác; nhánh kiểm nguồn tương thích còn bỏ qua G01/G02. Vì vậy PASS trước không phát hiện được các điểm chủ trì chỉ ra.

Đã bổ sung kiểm câu chữ ở CLI QMD cho cả bốn gói, không bỏ qua gói cũ. Cổng nhận diện lượt đi bằng đích trong binding và lượt về bằng quan hệ sở hữu lời giải–đề, nên cả nhãn sai không chứa từ khóa cũ cũng bị chặn. Cổng trình bày HTML dùng cùng quy tắc khi dựng lần sau; không tự sửa nhãn HTML để che lỗi nguồn. Kiểm số lượng/đích và các cổng hiện có vẫn được giữ.

## Kiểm và phần còn chờ

- `python scripts/zo_python.py -B scripts/zo_qmd.py check` với bốn đường dẫn QMD tường minh: PASS; đủ bốn mục `course-answer-actions`.
- `python scripts/zo_python.py -B scripts/zo_course_answer_actions_selftest.py --report _audit/answer_actions_20261018/qa-answer-actions-final.json`: 46/46. Gồm nhãn chuẩn, các biến thể sai trong phản hồi, nhãn quay về tùy ý trong đúng owner, fixture DOM trong bộ nhớ và ca giữ riêng công thức G02. Không ghi trang HTML.
- Đối chiếu trước/sau: toàn bộ đích Markdown theo thứ tự, khai báo ID và chuỗi công thức giữ nguyên; 1.526 tệp/vùng được bảo vệ không đổi, gồm tài nguyên/bản thảo/receipt/PDF, bốn HTML đang xem và ba nguồn điều hướng cần bảo toàn.
- Cú pháp Python, JSON và diff được kiểm. Bằng chứng đầy đủ tại `E:/zo_math/_audit/answer_actions_20261018/`: bản chụp nguồn trước, bảng thay đổi nhãn, migration binding G01, kết quả QMD/hồi quy/bảo toàn và kiểm tài liệu.

Các bản xem tại `http://127.0.0.1:8877/_audit/r1_consistency_20261018/index.html` vẫn là bản trước sửa nhãn và điều hướng. Khi được giao dựng HTML, cần kiểm lại các thao tác thực tế và raw/layout G01, giữ nguyên các cổng bắt buộc. Chưa có bản xem mới để nghiệm thu trong lượt chỉ sửa nguồn này.
