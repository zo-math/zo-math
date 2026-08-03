# Tiêu chí nghiệm thu lớp vận hành cỗ máy QMD

> **Trạng thái:** Ma trận nghiệm thu hiện hành `0.3`; O3 đã đạt. O4 đang triển khai với CLI ứng viên `0.4.0`; agent mới và phiên trình diễn đầu-cuối đã có bằng chứng; phép thử context cùng chat-box đã đạt trên một snapshot O4 trước đó; hợp đồng người dùng đã được đồng bộ; còn phép thử lại Mục tiêu 1, gói context cuối cùng, phép thử chat-box tương ứng, hồ sơ tổng hợp đủ bảy mục tiêu và release candidate O4 chưa hoàn tất.
>
> Tài liệu này đánh giá lớp vận hành bao quanh lõi QMD 1.0. Nó không thay thế `tieu_chi_nghiem_thu_he_thong.md`, vốn ghi nhận nghiệm thu của lõi kĩ thuật phiên bản 1.0.

## 1. Phạm vi

Lớp vận hành chỉ được gọi là hoàn thành khi có bằng chứng cho cả bảy mục tiêu:

1. người dùng mô tả được cỗ máy;
2. agent mới trong VS Code sử dụng được;
3. chat-box làm việc được qua gói chuẩn;
4. agent có một giao diện kĩ thuật vận hành thống nhất;
5. có gói phát hành và manifest;
6. có quy trình bảo trì, nâng phiên bản và khôi phục;
7. có phiên trình diễn đầu-cuối đến báo cáo trước xuất bản.

Không mục tiêu nào được suy ra chỉ từ việc checker chạy thành công. O4 nghiệm thu khả năng làm việc trong các dự án đã được tích hợp; khả năng khởi tạo một dự án con hoàn toàn mới được hoãn sang mốc sau O4.

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

Một người dùng đọc phần giới thiệu trong vài phút rồi trả lời bằng ngôn ngữ thông thường:

- người dùng có thể giao nhiệm vụ theo cách nào;
- cỗ máy hiện hỗ trợ phạm vi nào và khi nào cần tích hợp dự án mới;
- người dùng giao gì, agent làm gì và bộ kiểm tra tự động kiểm tra gì;
- sản phẩm và báo cáo chính có thể nhận được;
- phần nào máy kiểm định được, phần nào cần con người chấp nhận;
- ai quyết định xuất bản.

Không hỏi người dùng tên script, cú pháp Terminal hoặc các chi tiết chỉ agent vận hành cần biết.

### Bằng chứng

- bản README hiện hành;
- bảng câu hỏi và câu trả lời;
- ghi nhận các điểm gây hiểu sai, kể cả phép thử không kết luận được vì câu hỏi dùng thuật ngữ kĩ thuật.

### Đạt khi

Không cần lịch sử chat, không cần đọc toàn bộ thư mục tài liệu và không cần biết CLI để mô tả đúng cách giao việc, phạm vi hiện hành, đầu ra cùng ba quyền kiểm định–chấp nhận–xuất bản.

### Không đạt khi

Người dùng tưởng phải tự chạy Terminal, tưởng checker có thể tự chấp nhận hoặc xuất bản, hoặc tưởng dự án chưa được tích hợp đã tự động được hỗ trợ.

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

## 6. Mục tiêu 4 — Một giao diện kĩ thuật thống nhất cho agent

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
- hồ sơ `--release-file`;
- ma trận phiên bản;
- changelog;
- release checklist;
- log `verify`;
- phiên bản và tag dự kiến;
- hồi quy trước và sau;
- rollback log.

### Đạt khi

- release candidate được tạo từ commit sạch;
- `repository.commit` và `release.candidate_commit` là cùng một SHA đầy đủ;
- `release.tag` khớp `qmd-ops-v<release.version>` và `tag_created: false`;
- `regression_status: pass` và `rollback_tested: true`;
- không có tệp thiếu, thừa hoặc checksum sai;
- snapshot, phiên bản và điểm quay lại xác định;
- mọi phụ thuộc cần thiết được khai báo;
- gói đạt mức đủ để tái tạo;
- gói được tạo tại đường dẫn đầu ra đã chỉ định, không để lại ZIP hoặc tệp tạm ở gốc repository.

### Không đạt khi

Chỉ có tên ZIP hoặc comment commit; worktree phát hành bẩn; tag, phiên bản hoặc commit không khớp; gói tuyên bố chạy độc lập nhưng thiếu import, công cụ hoặc bằng chứng bắt buộc.

## 8. Mục tiêu 6 — Bảo trì, nâng phiên bản và khôi phục

### Phép thử

Thực hiện một thay đổi nhỏ có phân loại, tạo release candidate mới, rồi diễn tập trở lại release trước trong worktree hoặc nhánh riêng.

### Bằng chứng

- ma trận phiên bản;
- changelog;
- migration note nếu có;
- release checklist;
- rollback log;
- hồi quy trước và sau;
- `previous_version` và `previous_commit`;
- SHA-256 hai QMD hồi quy trước và sau;
- bằng chứng trạng thái `publication: pending`.

### Đạt khi

Có thể giải thích vì sao phiên bản thay đổi, dựng release trước trực tiếp từ commit đã ghi trong worktree riêng, chạy lại kiểm tra bắt buộc và bảo toàn hai bài hồi quy cùng trạng thái xuất bản.

### Không đạt khi

Khôi phục dựa vào thao tác phá hủy worktree sống, thiếu điểm quay lại, dùng một commit không xác định, cần sửa bài hồi quy hoặc không chứng minh được trạng thái `pending`.

## 9. Mục tiêu 7 — Phiên trình diễn đầu-cuối

### Phép thử

Dùng một yêu cầu mới bằng ngôn ngữ tự nhiên trong dự án đã được tích hợp, thực hiện từ tiếp nhận đến báo cáo trước xuất bản trong môi trường dùng một lần.

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
| O2 — đã triển khai kĩ thuật | `pack`, `verify`, gói ngữ cảnh | Gói thư mục/ZIP, thư mục sạch, checksum, thiếu/thừa/sai băm | Chat-box dùng được không cần lịch sử; không sửa bài hồi quy; không để lại gói thử trong repository |
| O3 — đã đạt | Release, versioning, rollback | Release candidate và rollback drill | Có changelog, commit quay lại, bằng chứng bất biến và hai log xác minh |
| O4 — đang triển khai | `start`, `prepublish`, gói O4 và trình diễn đầu-cuối | Toàn bộ bảy mục tiêu | Không xuất bản; bằng chứng đầy đủ |

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

## 12. Nghiệm thu riêng của O1

O1 đạt khi:

- `scripts/zo_qmd.py --help` và trợ giúp của năm lệnh hoạt động;
- `doctor` xác nhận môi trường, tệp hệ thống, cấu hình và bài hồi quy;
- `inspect` nhận diện đúng hai dự án, loại bài, hồ sơ, adapter và chuỗi `AGENTS.md`;
- `check` và `render` bảo toàn checker `2.6.0`, mã thoát và cảnh báo nghiệm thu có người quan sát;
- `regression` chạy bốn self-test, hồi quy nguồn và hồi quy render hai dự án;
- hai QMD cùng hồ sơ hồi quy không bị sửa;
- CLI không stage, commit, nghiệm thu hoặc xuất bản;
- mọi subprocess Python của CLI đi qua `scripts/zo_python.py`;
- khám phá cấu hình không bị đóng cứng vào một dự án hay một nhánh nội dung cụ thể.

O1 không chứng minh rằng `start`, `pack`, `verify` hoặc `prepublish` đã tồn tại.

## 13. Nghiệm thu riêng của O2

O2 đã có bằng chứng kĩ thuật khi:

- `pack` tạo gói context dạng thư mục và ZIP tại đầu ra tường minh;
- `verify` phát hiện manifest sai, checksum sai, tệp thiếu, tệp thừa, checksum chưa sắp xếp, symlink và đường dẫn nguy hiểm;
- gói tự xác minh được bằng CLI trong `payload/` từ thư mục sạch;
- không sinh `__pycache__` hoặc `.pyc`;
- hai QMD hồi quy không bị sửa và trạng thái xuất bản không đổi.

O2 không chứng minh rằng gói release có thể được tạo hoặc khôi phục.

## 14. Hợp đồng nghiệm thu riêng của O3

O3 chỉ được chuyển sang trạng thái đã triển khai khi:

- ma trận phiên bản, changelog, quy trình phát hành–khôi phục và mẫu hồ sơ release nhất quán;
- `pack --kind release --release-file ...` hoạt động mà không phá giao diện context;
- `verify` kiểm tra kiểu dữ liệu, quan hệ phiên bản–tag–commit và các bằng chứng release;
- self-test bao phủ cả release hợp lệ và release bị từ chối;
- release candidate `0.3.0` được tạo từ commit sạch và tự xác minh trong thư mục sạch;
- rollback drill từ commit ứng viên về `c1b26b9a0536b17e0885d8158fddbd20413767c2` đạt;
- SHA-256 hai QMD hồi quy không đổi;
- `publication: pending` được bảo toàn;
- không tạo tag thật, không push và không publish.

Các điều kiện O3 đã được chứng minh: mã tạo gói release và self-test đạt; hồi quy trước–sau cùng rollback drill đạt; release candidate được tạo từ commit sạch và xác minh thành công bằng CLI ngoài repository lẫn CLI tự chứa trong payload. Bằng chứng được lưu tại `phat_hanh/qmd_ops_0_3_0/`.

## 15. Trạng thái nghiệm thu riêng của O4

O4 đã có bằng chứng triển khai ban đầu khi:

- `start --help` hoạt động và tạo manifest phiên JSON tại đầu ra tường minh;
- `start` nhận diện được QMD dự kiến tạo mới, ghi đúng nguồn điều khiển, phạm vi, kế hoạch và `publication: pending`;
- phạm vi được phép tác động chồng lấn phạm vi loại trừ bị từ chối;
- QMD hiện hữu thiếu hồ sơ bắt buộc bị chặn;
- `scripts/zo_qmd_prepublish.py self-test` đạt;
- `prepublish` tạo được báo cáo sẵn sàng khi bằng chứng tổng hợp hợp lệ;
- `prepublish` chặn trường hợp chưa có kiểm định có người quan sát hoặc khai báo xuất bản sai;
- cả hai lệnh từ chối đầu ra tùy tiện ở gốc repository;
- hồi quy nguồn hai dự án đạt và SHA-256 hai QMD đường cơ sở không đổi.

Các bằng chứng trên chỉ chứng minh hai giao diện O4 đã được triển khai đúng ranh giới ban đầu. O4 vẫn chưa đạt cho đến khi:

- tài liệu hiện hành phản ánh đúng CLI ứng viên;
- gói context được tạo từ commit sạch chứa trạng thái O4 và vượt hai đường `verify`;
- một chat-box mới chỉ dùng gói ấy mà tái hiện đúng nhiệm vụ;
- một yêu cầu mới đi hết chuỗi `inspect → start → sản xuất → check → render → human review → prepublish`;
- bảy mục tiêu đều có bằng chứng lưu lại;
- trạng thái xuất bản vẫn `pending` và người dùng quyết định riêng việc khóa lớp vận hành 1.0.

## 16. Điều kiện khóa lớp vận hành 1.0

Chỉ khóa lớp vận hành 1.0 khi:

- O0–O4 đều đạt;
- bảy mục tiêu đều có bằng chứng;
- tài liệu hiện hành phản ánh đúng mã;
- một agent mới và một chat-box mới đều vượt phép thử;
- release candidate có thể xác minh và khôi phục;
- phiên trình diễn kết thúc ở báo cáo trước xuất bản;
- người dùng chấp thuận khóa phiên bản.

## 17. Kết luận

Lõi QMD 1.0 chứng minh hệ thống kiểm định có thể phục vụ hai dự án. Lớp vận hành chỉ đạt khi khả năng ấy được biến thành một quy trình có thể học nhanh, bàn giao, chạy, kiểm tra, phát hành và khôi phục bằng bằng chứng lặp lại được.
