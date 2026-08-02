# Tiêu chí nghiệm thu lớp vận hành cỗ máy QMD

> **Trạng thái:** Dự thảo ma trận nghiệm thu 0.1 — mốc O0, chờ duyệt.
>
> Tài liệu này đánh giá lớp vận hành bao quanh lõi QMD 1.0. Nó không thay thế `tieu_chi_nghiem_thu_he_thong.md`, vốn ghi nhận nghiệm thu của lõi kĩ thuật phiên bản 1.0.

## 1. Phạm vi

Lớp vận hành chỉ được gọi là hoàn thành khi có bằng chứng cho cả bảy mục tiêu:

1. người dùng mô tả được cỗ máy;
2. agent mới trong VS Code sử dụng được;
3. chat-box làm việc được qua gói chuẩn;
4. có một điểm vào vận hành thống nhất;
5. có gói phát hành và manifest;
6. có quy trình bảo trì, nâng phiên bản và khôi phục;
7. có phiên trình diễn đầu-cuối đến báo cáo trước xuất bản.

Không mục tiêu nào được suy ra chỉ từ việc checker chạy thành công.

## 2. Nguyên tắc bằng chứng

Mỗi tiêu chí phải có:

- điều kiện trước;
- thao tác hoặc phép thử;
- bằng chứng lưu lại;
- kết quả mong đợi;
- điều kiện không đạt.

Bằng chứng phải phân biệt:

- kiểm định tự động;
- kiểm định có người quan sát;
- quyết định của người dùng;
- thông tin chỉ được khai báo nhưng chưa xác minh.

## 3. Mục tiêu 1 — Người dùng mô tả được cỗ máy

### Phép thử

Một người dùng đọc điểm vào tài liệu trong vài phút và trả lời đúng:

- cỗ máy giải quyết vấn đề gì;
- lõi kĩ thuật và lớp vận hành khác nhau thế nào;
- đầu vào và đầu ra chính;
- ba cổng V, A, P;
- lệnh khởi đầu;
- vì sao checker không tự nghiệm thu hoặc xuất bản.

### Bằng chứng

- bản README hiện hành;
- bảng câu hỏi và câu trả lời;
- ghi nhận các điểm gây hiểu sai.

### Đạt khi

Không cần lịch sử chat và không cần đọc toàn bộ thư mục tài liệu để trả lời chính xác.

### Không đạt khi

Người dùng phải tự ghép nhiều lệnh rời hoặc hiểu nhầm `PASS` là `accepted` hay `published`.

## 4. Mục tiêu 2 — Agent mới trong VS Code sử dụng được

### Phép thử

Mở một phiên agent không có lịch sử chat trong repository sống. Giao một nhiệm vụ nhận diện và kiểm định một bài đường cơ sở.

Agent phải:

- đọc `AGENTS.md` cấp gốc và `AGENTS.md` cục bộ của đúng dự án;
- xác nhận Git;
- xác định đúng dự án, loại bài và hồ sơ;
- dùng đúng điểm vào;
- chạy đúng mức kiểm định;
- không sửa bài hồi quy;
- báo cáo theo giao thức.

### Bằng chứng

- transcript hoặc log lệnh;
- báo cáo phiên;
- diff xác nhận không có thay đổi ngoài ý muốn.

### Đạt khi

Agent hoàn thành mà không cần cung cấp lại lịch sử thiết kế hệ thống.

### Không đạt khi

Agent phải đoán tài liệu, gọi script rời không có chỉ dẫn, hoặc claim trạng thái chưa kiểm chứng.

## 5. Mục tiêu 3 — Chat-box làm việc qua gói chuẩn

### Phép thử

Cung cấp một gói ngữ cảnh được tạo bằng `pack` cho một chat-box không có quyền truy cập repository.

Chat-box phải:

- đọc prompt và manifest trước;
- xác minh checksum;
- phân loại nguồn hiện hành, chuyên trách và lịch sử;
- nhận diện tệp thiếu hoặc hạn chế;
- tạo một sản phẩm bàn giao đúng phạm vi;
- phân biệt bản sao của gói với repository sống và chỉ dẫn đúng cho người vận hành trung gian khi cần;
- không claim đã chạy lệnh ngoài bằng chứng.

### Bằng chứng

- gói ngữ cảnh;
- báo cáo `verify`;
- câu trả lời hoặc tệp do chat-box tạo;
- danh sách giới hạn được nhận diện.

### Đạt khi

Một chat-box mới tái hiện đúng bản đồ nhiệm vụ và không cần lịch sử hội thoại.

### Không đạt khi

Gói thiếu manifest, đường dẫn bị mất, hoặc chat-box trộn thông tin khai báo với bằng chứng đã xác minh.

## 6. Mục tiêu 4 — Một điểm vào vận hành thống nhất

### Phép thử

Thực hiện các thao tác thường dùng qua:

```bash
python scripts/zo_python.py scripts/zo_qmd.py ...
```

Tối thiểu kiểm tra:

```text
doctor
inspect
start
check
render
regression
pack
verify
prepublish
```

### Bằng chứng

- `--help`;
- log lệnh;
- mã thoát;
- báo cáo;
- kiểm tra rằng validator không bị sao chép;
- kiểm tra các lệnh sinh tệp yêu cầu vị trí đầu ra tường minh và không làm bẩn gốc repository.

### Đạt khi

Người vận hành không cần nhớ nhiều điểm vào cho vòng đời thông thường, trong khi `zo_check_repo.py` vẫn là checker lõi; các lệnh tạo gói hoặc báo cáo không sinh tệp vào vị trí ngoài phạm vi đã chỉ định.

### Không đạt khi

CLI mới trở thành checker thứ hai, phá giao diện cũ hoặc che mất mã thoát và báo cáo của lõi.

## 7. Mục tiêu 5 — Gói phát hành và manifest

### Phép thử

Tạo một release candidate từ commit sạch, sau đó mở gói trong thư mục sạch và chạy `verify`.

### Bằng chứng

- `MANIFEST.yml`;
- `FILES.sha256`;
- changelog;
- log `verify`;
- phiên bản và tag;
- bằng chứng hồi quy.

### Đạt khi

- không có tệp thiếu, thừa hoặc checksum sai;
- snapshot và phiên bản xác định;
- mọi phụ thuộc cần thiết được khai báo;
- gói đủ mức mà manifest tuyên bố;
- gói được tạo tại đường dẫn đầu ra đã chỉ định, không để lại ZIP hoặc tệp tạm ở gốc repository.

### Không đạt khi

Chỉ có tên ZIP hoặc comment commit, hoặc gói tuyên bố chạy độc lập nhưng thiếu import và công cụ bắt buộc.

## 8. Mục tiêu 6 — Bảo trì, nâng phiên bản và khôi phục

### Phép thử

Thực hiện một thay đổi nhỏ có phân loại, tạo release candidate mới, rồi diễn tập trở lại release trước trong worktree hoặc nhánh riêng.

### Bằng chứng

- version matrix;
- changelog;
- migration note nếu có;
- release checklist;
- rollback log;
- hồi quy trước và sau.

### Đạt khi

Có thể giải thích vì sao phiên bản thay đổi, tái lập release trước và bảo toàn hai bài hồi quy cùng trạng thái xuất bản.

### Không đạt khi

Khôi phục dựa vào thao tác phá hủy worktree, thiếu điểm quay lại hoặc cần sửa bài hồi quy.

## 9. Mục tiêu 7 — Phiên trình diễn đầu-cuối

### Phép thử

Dùng một yêu cầu mới trong dự án đã có, thực hiện từ tiếp nhận đến báo cáo trước xuất bản trong môi trường dùng một lần.

Chuỗi bắt buộc:

```text
request
→ doctor
→ inspect
→ start
→ production
→ check
→ render
→ human review
→ prepublish
```

### Bằng chứng

- yêu cầu ban đầu;
- manifest phiên;
- hồ sơ và kế hoạch;
- QMD/tài nguyên;
- báo cáo checker;
- đầu ra render;
- bảng kiểm trực quan;
- báo cáo trước xuất bản;
- diff và trạng thái Git.

### Đạt khi

- không có `FAIL` tự động;
- kiểm định trực quan được ghi nhận;
- trạng thái sản xuất được nêu chính xác;
- trạng thái xuất bản vẫn `pending`;
- không sửa hai bài hồi quy;
- không xuất bản.

### Không đạt khi

Bỏ qua cổng có người quan sát, checker tự tuyên bố nghiệm thu, hoặc trình diễn kết thúc bằng việc xuất bản ngoài yêu cầu.

## 10. Ma trận mốc triển khai

| Mốc | Sản phẩm | Kiểm tra bắt buộc | Điều kiện commit độc lập |
|---|---|---|---|
| O0 | Kiến trúc, giao thức, manifest, ma trận nghiệm thu | Markdown, liên kết, nhất quán thuật ngữ | Không sửa mã; không mô tả chức năng đích như đã có |
| O1 | CLI vận hành cơ bản | Self-test, hồi quy hai dự án, `--help` | Không phá checker 2.6.0 |
| O2 | `pack`, `verify`, gói ngữ cảnh | Gói trong thư mục sạch, checksum, thiếu/thừa | Chat-box dùng được không cần lịch sử |
| O3 | Release, versioning, rollback | Release candidate và rollback drill | Có changelog và điểm quay lại |
| O4 | Trình diễn đầu-cuối | Toàn bộ bảy mục tiêu | Không xuất bản; bằng chứng đầy đủ |

## 11. Nghiệm thu riêng của O0

O0 đạt khi:

- quan hệ giữa lõi 1.0 và lớp vận hành được ghi rõ;
- điểm vào CLI đích được khóa nhưng không bị mô tả là đã triển khai;
- giao thức agent và chat-box nhất quán, có mô hình người vận hành trung gian;
- chuỗi `AGENTS.md` cấp gốc → dự án và ranh giới toàn hệ thống → `_quy_trinh` dự án được ghi rõ;
- schema manifest phiên bản 1 và mẫu YAML hợp lệ được định nghĩa;
- gói ngữ cảnh và gói phát hành được phân biệt;
- bảy mục tiêu có phép thử và điều kiện không đạt;
- README và tài liệu lõi không còn tuyên bố mơ hồ rằng toàn bộ cỗ máy đã hoàn thành;
- quy tắc vị trí đầu ra ngăn việc mặc định sinh gói và tệp tạm vào repository;
- không có script, QMD hồi quy hoặc trạng thái xuất bản bị sửa.

O0 chưa chứng minh:

- `zo_qmd.py` hoạt động;
- `pack` hoặc `verify` tồn tại;
- có release candidate;
- đã chạy phiên trình diễn.

## 12. Điều kiện khóa lớp vận hành 1.0

Chỉ khóa lớp vận hành 1.0 khi:

- O0–O4 đều đạt;
- bảy mục tiêu đều có bằng chứng;
- tài liệu hiện hành phản ánh đúng mã;
- một agent mới và một chat-box mới đều vượt phép thử;
- release candidate có thể xác minh và khôi phục;
- phiên trình diễn kết thúc ở báo cáo trước xuất bản;
- người dùng chấp thuận khóa phiên bản.

## 13. Kết luận

Lõi QMD 1.0 chứng minh hệ thống kiểm định có thể phục vụ hai dự án. Lớp vận hành chỉ đạt khi khả năng ấy được biến thành một quy trình có thể học nhanh, bàn giao, chạy, kiểm tra, phát hành và khôi phục bằng bằng chứng lặp lại được.
