# Quy ước biên tập FHSM

## 1. Authority

Nguồn biên tập canonical duy nhất của bản chuyển ngữ là bộ TeX mô-đun trong:

`content/di_tim/di_tim_ly_luan_toan_hoc/fhsm_tex/`

Các đơn vị canonical:

- `tieu_luan_dan_nhap_fhsm_ban_chuyen_ngu.tex`
- `dan_nhap.tex`
- `chuong_01.tex`–`chuong_11.tex`
- `thu_muc_chu_giai.tex`
- `khao_luan_he_thuat_ngu_ban_chuyen_ngu.tex`
- `references.bib`
- driver: `main.tex`

QMD/Web không phải nguồn biên tập của ấn bản này.

## 2. Hệ thuật ngữ hiện hành

Authority thuật ngữ: `fhsm_thuat_ngu.md`.

- `reasoning` → **suy lí**
- `sense making` → **kiến tạo ý nghĩa**

Không quay lại các hệ legacy như `luận / hiểu`, `lập luận / kiến tạo ý nghĩa`, hoặc `thấu hiểu` để thay cho hai thuật ngữ trung tâm.

Phân biệt:

- `reasoning` → **suy lí**
- `inference` → **suy luận**
- `argument` → **lập luận**
- `argumentation` → **hoạt động lập luận**
- `justification` → **biện minh**
- `proof` → **chứng minh**
- `explanation` → **giải thích**
- `interpretation` → **diễn giải**
- `understanding` → **sự hiểu biết** theo ngữ cảnh

## 3. Nguyên tắc hiệu chỉnh

- Bản tiếng Việt là văn bản đích; bản tiếng Anh dùng để kiểm tra nghĩa, thuật ngữ, cấu trúc lập luận và thứ tự nội dung.
- Không dịch lại chỉ để thay cách diễn đạt. Chỉ sửa khi có lí do thực chất.
- Nếu bản dịch đã ổn, giữ nguyên.
- Không tự thêm ý vào bản dịch chính để giải thích điều nguyên tác không nói.
- Sau khi đối chiếu nguyên tác, đọc lại câu Việt như văn bản tiếng Việt độc lập.
- Ưu tiên một phương án tốt nhất.
- Khi chỉ có vài lỗi, nêu đúng vị trí và thay đổi cần thiết; không viết lại toàn khối nếu không cần.

## 4. Bình giải

`\NOTE{...}` dùng để làm rõ chức năng sư phạm, mạch lập luận, thuật ngữ hoặc điểm dễ hiểu nhầm.

- Viết trung tính, học thuật, gọn.
- Không lấn át bản dịch.
- Tránh mở đầu máy móc bằng “Đoạn này…”, “Câu này…”, “Tác giả muốn…”.
- Nếu bản dịch chính đã đủ rõ, không thêm bình giải chỉ để có bình giải.

## 5. Chính tả, đơn vị và số

Xem:

- `quy_uoc_i_y.md`
- `quy_uoc_don_vi_anh_my.md`

Quy ước số:

- Số trong văn bản thông thường, tên mục, tên ví dụ, thông tin mô tả: viết số thường, không bọc LaTeX.
- Số tham gia biểu thức, phép tính, quan hệ toán học, so sánh hoặc được xét như đối tượng toán học: đặt trong math mode.

Quy ước công thức:

- Không dùng `\qquad`; khi cần khoảng cách dùng `\quad`.
- Ưu tiên câu văn thay cho `\Rightarrow`, `\Leftarrow`, `\Leftrightarrow` nếu không thật sự cần.
- Dùng `f^\prime`, `f^{\prime\prime}`, `\frac`, `\lvert\cdot\rvert`.

## 6. Thư mục chú giải

`Annotated Bibliography` → **Thư mục chú giải**.

Giữ chính xác dữ liệu thư mục. Không tự sửa lặng lẽ lỗi nghi ngờ từ OCR/chế bản; phải kiểm chứng nguồn.

## 7. Dàn trang song ngữ `paracol`

- Không dùng `\newpage` để chữa lệch hai cột.
- Tìm **điểm đầu tiên mất đồng bộ**, không chữa từng hậu quả phía sau.
- `\vspace{\baselineskip}` có thể bị bỏ ở đầu trang; khi thật sự cần khoảng cách đầu trang dùng `\vspace*{\baselineskip}`.
- Với hình song ngữ, ưu tiên đồng bộ cả khối hình/caption thay vì rải `\vspace` cục bộ.
- Kiểm tra lại cả trang hiện tại và trang kế tiếp sau mỗi thay đổi dàn trang.

## 8. Legacy

Aggregate `luan_va_hieu.tex` đã được loại khỏi authority.

Các ghi chú dùng hệ thuật ngữ cũ chỉ có giá trị lịch sử; không dùng làm authority biên tập.
