# Chỉ dẫn cho agent trong repository ZO Math

> Đây là tài liệu điều phối nội bộ dành cho agent làm việc với mã nguồn, tài sản và tài liệu xây dựng ZO Math.
>
> Đây không phải là nội dung xuất bản dành cho người đọc ZO Math.

## Chỉ dẫn bắt buộc

Trước khi thực hiện bất kỳ nhiệm vụ nào trong repository này, phải đọc và tuân thủ:

- `quy_trinh_xay_dung/quy_tac_lam_viec_voi_agent.md`
- `quy_trinh_xay_dung/quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md`

Hai tài liệu trên đã được người dùng xác nhận là đang có hiệu lực trên toàn repository:

- `quy_tac_lam_viec_voi_agent.md` quy định nguyên tắc, giới hạn và thứ tự ưu tiên của nguồn chỉ dẫn;
- `quy_trinh_thuc_hien_nhiem_vu_ky_thuat.md` quy định cách agent tiếp nhận, thực hiện, kiểm tra và báo cáo một nhiệm vụ kỹ thuật.

Khi nhiệm vụ tác động đến một dự án con hoặc một thư mục cụ thể, trước khi khảo sát hay thay đổi tệp, phải kiểm tra các `AGENTS.md` trên đường dẫn từ gốc repository đến phạm vi đó và đọc theo thứ tự từ ngoài vào trong. `AGENTS.md` gần tệp đang làm việc hơn có thể bổ sung hoặc quy định cụ thể hơn cho phạm vi của nó; những chỉ dẫn cấp gốc không bị mất hiệu lực nếu không có quy định cục bộ rõ ràng thay thế. Nếu phiên làm việc được mở từ thư mục gốc và chỉ dẫn ở sâu hơn không được tự động nạp, agent phải chủ động đọc tệp ấy.

Khi chạy lệnh Python trong repository này, Codex phải dùng trình khởi chạy repository-local:

```text
python scripts/zo_python.py ...
```

Trình khởi chạy bảo đảm tiến trình Python con dùng chế độ UTF-8 mà không yêu cầu thay đổi biến môi trường global.

Mọi lệnh Quarto do Codex chạy trong repository này phải đi qua trình khởi chạy Quarto repository-local, và trình này phải được gọi qua `scripts/zo_python.py`:

```text
python scripts/zo_python.py scripts/zo_quarto.py <quarto-command> [tham số...]
```

Không ghi đường dẫn tuyệt đối tới executable Python vào metadata QMD. Cơ chế trên bảo đảm Jupyter và reticulate dùng nhất quán môi trường Python hiện hành theo cách portable.

Đối với bài QMD thuộc hệ thống có cấu hình, Codex dùng `scripts/zo_qmd.py` làm điểm vào vận hành và luôn gọi qua `scripts/zo_python.py`: dùng `check` cho kiểm định nguồn và `render` khi cần dựng đầu ra. `scripts/zo_check_repo.py` là checker lõi phía sau, chỉ được gọi trực tiếp khi bảo trì hoặc chẩn đoán checker, hoặc khi kiểm tra kĩ thuật ngoài vòng đời bài QMD có cấu hình. Cả hai công cụ đều không thay thế kiểm tra trực quan, nghiệm thu hoặc xuất bản.

## Quy ước trình bày chung

Không dùng `\boxed{...}` hoặc khung viền trực tiếp quanh công thức để nhấn mạnh. Công thức quan trọng được làm nổi bật bằng vị trí trong mạch văn hoặc bằng khối nội dung ZO Math phù hợp. Khi gặp công thức hiển thị riêng đang dùng `\boxed{...}`, chỉ loại bỏ lớp `\boxed` và giữ công thức ở dạng `$$...$$`, trừ khi nhiệm vụ hiện tại yêu cầu tổ chức lại nội dung.

## Chỉ dẫn theo loại nhiệm vụ

### Hệ thống sản xuất và kiểm định QMD

Khi nhiệm vụ liên quan đến sản xuất, chỉnh sửa, kiểm định, đóng gói hoặc bàn giao một bài QMD thuộc hệ thống có cấu hình, trước hết phải đọc:

- `quy_trinh_xay_dung/he_thong_san_xuat_qmd/README.md`.

Tài liệu trên là điểm vào bằng văn bản của hệ thống. Khi phạm vi nằm trong một dự án con, phải tiếp tục đọc `AGENTS.md` cục bộ của dự án rồi mới nạp cấu hình, hồ sơ và quy chuẩn trong `_quy_trinh/`. Ví dụ hiện hành:

- `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/AGENTS.md`;
- `content/thpt/zo_math_100/100_bai_toan_thuc_te/AGENTS.md`.

Lõi kĩ thuật QMD phiên bản 1.0 đã được khóa. Lớp vận hành hóa đang được xây theo các tài liệu trong `quy_trinh_xay_dung/he_thong_san_xuat_qmd/`; chức năng được mô tả là đích kiến trúc không được coi là đã có nếu chưa tồn tại mã và bằng chứng kiểm nghiệm. Với vòng đời một bài QMD có cấu hình, điểm vào hiện hành là `scripts/zo_qmd.py`; checker lõi `scripts/zo_check_repo.py` được CLI này điều phối và không phải lệnh mặc định mà agent phải tự chọn.

### Phong cách viết

ZO Math sử dụng nhiều phong cách viết khác nhau. Chỉ áp dụng một phong cách khi người dùng chỉ định rõ cho bài viết hoặc nhiệm vụ hiện tại, hoặc khi chỉ dẫn có thẩm quyền của dự án con đã được người dùng phê duyệt chọn phong cách ấy cho một phạm vi xác định.

Khi một phong cách được chỉ định, phải đọc:

- `quy_trinh_xay_dung/phong_cach_viet/index.md`;
- tài liệu chuyên biệt của phong cách được liệt kê trong tệp chỉ mục.

Chỉ áp dụng phong cách trong phạm vi đã được người dùng hoặc chỉ dẫn có thẩm quyền của dự án con xác lập. Không tự suy rộng phong cách sang bài, nhiệm vụ hay dự án khác; một phong cách được chọn làm mặc định cục bộ không trở thành mặc định của toàn bộ ZO Math. Không suy diễn quy chuẩn chỉ từ bài mẫu. Khi thực tiễn biên tập cho thấy cần thay đổi quy chuẩn, phải đề xuất cập nhật tài liệu chuyên biệt và chỉ thực hiện sau khi người dùng chấp thuận. Không ghi toàn bộ nội dung chi tiết của từng phong cách vào `AGENTS.md`.

### Khối nội dung

Khi nhiệm vụ tạo, sửa, chuyển đổi hoặc kiểm định khối nội dung trong tệp Markdown hoặc QMD, phải đọc và tuân thủ:

- `quy_trinh_xay_dung/huong_dan_su_dung_khoi_noi_dung.md`.

Phải xác định trước nội dung có thực sự cần tách thành khối hay không; sau đó xác định khối thuộc mạch chính hay phần đọc thêm để chọn trạng thái mở cố định hoặc thu gọn; cuối cùng mới chọn màu theo chức năng nội dung. Không chọn màu để trang trí, không thu gọn mắt xích bắt buộc và không suy diễn quy tắc khối từ một bài mẫu.

Khi kiểm định hoặc chuyển đổi nội dung cũ, phải phân biệt lớp còn được giữ để tương thích với hệ khối chuẩn dùng cho nội dung mới. Không tự động chuyển đổi toàn bộ trang nếu nhiệm vụ hiện tại không bao gồm việc đó.

### Lưới thẻ

Khi nhiệm vụ liên quan đến lưới thẻ, phải đọc và tuân thủ thêm:

- `quy_trinh_xay_dung/quy_chuan_luoi_the.md`

Tài liệu này chỉ điều hành các nhiệm vụ liên quan đến dữ liệu, mã sinh, giao diện, đầu ra và kiểm tra lưới thẻ.

### Xuất bản website

Khi nhiệm vụ liên quan đến xuất bản website, phải đọc và tuân thủ thêm:

- `quy_trinh_xay_dung/quy_trinh_xuat_ban_website.md`

Dùng `scripts/zo_publish.py` cho quy trình xuất bản mới. Các chế độ `check`, `prepare` và `publish` được chính thức hỗ trợ. Chỉ chạy `prepare` hoặc `publish` khi người dùng yêu cầu rõ; trước nhiệm vụ xuất bản phải đọc quy trình chính thức được dẫn chiếu trên. Không chạy `scripts/publish_public.sh` nếu yêu cầu hiện tại không chỉ định rõ việc khảo sát script cũ.

## Thẩm quyền của tài liệu chuyên biệt

Các tài liệu khác trong `README/`, `content/`, `assets/`, `_audit/` hoặc những vị trí khác không tự động được xem là quy chuẩn hiện hành, trừ khi:

- yêu cầu hiện tại của người dùng dẫn chiếu rõ đến tài liệu đó;
- một `AGENTS.md` có hiệu lực trong phạm vi đang làm việc dẫn chiếu đến tài liệu đó;
- một tài liệu quy chuẩn hiện hành xác định rõ phạm vi áp dụng của nó.

Khi nhiệm vụ liên quan đến một lĩnh vực chưa có tài liệu chuyên biệt được dẫn chiếu tại đây, phải:

1. khảo sát hiện trạng kỹ thuật và các nguồn liên quan;
2. phân biệt bằng chứng hiện trạng với quyết định thiết kế;
3. không tự phong tài liệu cũ thành quy chuẩn;
4. hỏi người dùng khi cần một quyết định chưa được xác lập.

Chỉ những tài liệu chuyên biệt có hiệu lực trên toàn ZO Math mới được dẫn trực tiếp từ `AGENTS.md` ở gốc repository sau khi người dùng phê duyệt. Tài liệu chỉ áp dụng cho một dự án con phải được dẫn từ `AGENTS.md` gần dự án ấy nhất.
