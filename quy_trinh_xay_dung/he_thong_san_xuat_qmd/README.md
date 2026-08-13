# Hệ thống sản xuất và kiểm định QMD cho ZO Math

> **Trạng thái:** Release hiện hành là `0.5.0`; lớp vận hành giữ mốc nghiệm thu `1.0`. Hằng số máy đọc được `OPERATIONS_CONTRACT_VERSION` là `0.5` để khớp `MAJOR.MINOR` của release `0.5.0`. Git tag thật chưa được tạo; chưa push hoặc publish.
>
> Đây là tài liệu vận hành nội bộ. Nó chỉ có thẩm quyền trong phạm vi mà `AGENTS.md`, cấu hình dự án hoặc yêu cầu hiện tại của người dùng dẫn chiếu. Các hồ sơ kiểm kê và thiết kế ban đầu được giữ lại như bằng chứng lịch sử, không tự động ghi đè quy trình đang có hiệu lực ở nơi khác.

## 0. Trạng thái hiện tại

Đã hoàn thành và khóa:

- lõi kĩ thuật QMD phiên bản `1.0`;
- checker phiên bản `2.6.0`;
- schema cấu hình dự án phiên bản `1`;
- chế độ native và đường hồi quy hai dự án.

Release hiện hành `0.5.0` bao gồm:

- `scripts/zo_qmd.py` phiên bản `0.5.0`;
- `scripts/zo_qmd_package.py` phiên bản `0.4.0`;
- mười lệnh `doctor`, `inspect`, `start`, `review-ready`, `prepublish`, `check`, `render`, `regression`, `pack`, `verify`;
- khả năng lập manifest phiên, khóa kế hoạch, tạo và xác minh gói context hoặc release, tổng hợp bằng chứng trước xuất bản;
- khả năng dùng chung `references.quality_exemplars` trong `inspect`, `doctor`, `start`, giao thức agent và gói context;
- bằng chứng hồi quy, trình diễn đầu-cuối, release candidate và rollback drill của O4.

Release `0.3.0` cùng hồ sơ O3 được giữ làm bằng chứng lịch sử của giai đoạn phát hành và khôi phục.

O3 đã triển khai trong mã:

- ma trận phiên bản và changelog;
- `pack --kind context|release`, với `context` là mặc định tương thích;
- hồ sơ release qua `--release-file`;
- kiểm tra worktree sạch, SemVer, tag, commit, bằng chứng và payload release;
- self-test cho release hợp lệ, manifest release sai và worktree bẩn.

Đã có bằng chứng trong O4:

- gói context cuối `qmd-context-20260804-031754`, được tạo từ commit sạch, đã vượt xác minh ngoài gói và tự xác minh;
- một chat-box mới chỉ dùng gói ấy đã tái hiện đúng nhiệm vụ;
- một agent mới trong VS Code đã dùng đúng giao diện vận hành và không sửa bài đường cơ sở;
- phiên trình diễn đầu-cuối đã đi đến `prepublish`, bị chặn đúng khi kiểm định có người quan sát chưa chấp nhận sản phẩm và giữ `publication: pending`.

O4 đã hoàn thành các điều kiện nghiệm thu và quyết định khóa lớp vận hành ở mốc `1.0`.

Ba tài liệu điều khiển giai đoạn vận hành hóa:

- `kien_truc_van_hanh_co_may_qmd.md`;
- `giao_thuc_agent_chat_box_va_goi_ngu_canh.md`;
- `tieu_chi_nghiem_thu_lop_van_hanh.md`.

`scripts/zo_qmd.py` là điểm vào vận hành hiện hành cho mười lệnh. `scripts/zo_check_repo.py` vẫn là checker lõi; CLI vận hành chỉ điều phối và bảo toàn mã thoát, báo cáo cùng các cổng kiểm định hiện có. Logic tạo và xác minh gói nằm trong `scripts/zo_qmd_package.py`; logic tổng hợp bằng chứng trước xuất bản nằm trong `scripts/zo_qmd_prepublish.py`; cả hai không được trộn vào checker.

Cổng `review-ready` của `functions_100` khóa ba lớp ổn định hóa trước Human Review: (1) lifecycle phải bắt đầu bằng session `start` có scope canonical và authority snapshot bất biến; (2) lõi tự chứa của nguồn TikZ/PGFPlots phải thực sự mang STIX, màu vai trò và trường nền–khung theo quy chuẩn thay vì chỉ có chuỗi `.tex→PDF→SVG`, đồng thời đồ thị phải nằm dưới `_figures/<slug>/`; (3) các cụm ngữ nghĩa mơ hồ kiểu *giữ/bảo toàn độ lớn* bị chặn để buộc tác giả phân biệt bảo toàn một đại lượng với khả năng xác định/khôi phục đại lượng từ đầu ra. Đây là guard cấu trúc; Human Review vẫn quyết định chân trị và chất lượng diễn đạt.

Ranh giới lưu trữ hiện hành:

```text
quy_trinh_xay_dung/he_thong_san_xuat_qmd/
    → hợp đồng và tài liệu toàn hệ thống

content/.../<du_an>/_quy_trinh/
    → cấu hình, hồ sơ, mẫu và quy chuẩn riêng của dự án
```

Gói ZIP, báo cáo phiên và tệp sinh tạm không được mặc định ghi vào gốc repository hoặc thư mục dự án. Công cụ tạo các sản phẩm ấy phải nhận vị trí đầu ra tường minh; báo cáo checker nằm trong repository vẫn tuân theo quy tắc `_audit/` hiện hành.

## Cách người dùng sử dụng cỗ máy

Người dùng giao nhiệm vụ bằng ngôn ngữ tự nhiên. Ví dụ:

> Hãy viết về hàm $y=e^x$.

Với một dự án đã được tích hợp, người dùng không phải biết tên script, cú pháp Terminal, vị trí cấu hình hoặc cách gọi checker. Agent chịu trách nhiệm chuyển yêu cầu thành chuỗi thao tác kĩ thuật: nhận diện dự án, đọc quy chuẩn và hồ sơ, khóa phạm vi, tạo hoặc sửa QMD cùng tài nguyên, kiểm định, render khi cần và trình sản phẩm để người dùng duyệt.

Người dùng giữ ba trách nhiệm không được chuyển cho máy:

- xác nhận mục tiêu nội dung và các quyết định còn mở;
- kiểm tra ý nghĩa toán học, sư phạm, hình thức và đầu ra thực tế;
- quyết định chấp nhận và xuất bản.

Phạm vi triển khai hiện hành gồm đúng hai dự án đã được tích hợp và kiểm nghiệm:

- `functions_100` — 100+ Hàm số: Sự biến thiên và đồ thị;
- `real_world_100` — 100+ Bài toán thực tế.

Lõi được thiết kế để bổ sung dự án khác, nhưng một khóa học Xác suất, Đại số tuyến tính hoặc dự án mới chưa có cấu hình không tự động được hỗ trợ chỉ vì lõi có tính mở rộng. Tích hợp dự án mới là một nhiệm vụ riêng sau O4.

Ba giao diện phải được phân biệt:

1. **Giao diện người dùng:** yêu cầu bằng ngôn ngữ tự nhiên.
2. **Giao diện agent:** `scripts/zo_qmd.py` và các lệnh vận hành repository-local.
3. **Checker lõi:** `scripts/zo_check_repo.py`, được lớp vận hành gọi phía sau.

## 1. Mục đích

Tài liệu này là điểm vào bằng văn bản của cỗ máy QMD. Lõi kĩ thuật cung cấp một hợp đồng thống nhất để sản xuất và kiểm định nhiều loại bài QMD của ZO Math. Lớp vận hành đang được xây để biến hợp đồng này thành một điểm vào có thể dùng lặp lại:

```text
tiếp nhận nhiệm vụ
→ khóa phạm vi
→ xác định dự án và loại bài
→ nạp cấu hình dự án
→ nạp hồ sơ sản xuất
→ tạo hoặc sửa QMD và tài nguyên
→ kiểm định nguồn
→ render khi cần
→ kiểm định đầu ra
→ kiểm định có người quan sát
→ nghiệm thu
→ xuất bản khi người dùng xác nhận
```

Hệ thống không tự viết thay quy chuẩn chuyên môn, không tự nghiệm thu nội dung và không tự xuất bản.

Ba cổng phải được phân biệt:

- **V — Validation:** checker kiểm định phần có thể mã hóa; không còn `FAIL` mới đủ điều kiện xem xét trạng thái `validated`;
- **A — Acceptance:** con người kiểm tra nội dung, hình thức và đầu ra thực tế trước khi chấp nhận;
- **P — Publication:** chỉ người dùng mới quyết định chuyển sang xuất bản.

Vượt cổng trước không tự động vượt cổng sau.

## 2. Kiến trúc đang vận hành

Phiên bản 1.0 gồm bốn tầng:

1. **Lõi dùng chung**
   - vòng đời bài;
   - metadata nền;
   - kiểm tra QMD, tài nguyên, HTML và PDF;
   - định dạng báo cáo;
   - cổng nghiệm thu và xuất bản.

2. **Cấu hình dự án**
   - gốc dự án;
   - loại bài và mẫu đường dẫn;
   - thư mục hồ sơ;
   - mô-đun đã đăng kí;
   - metadata bổ sung;
   - tài liệu điều khiển;
   - đường cơ sở hồi quy.

3. **Hồ sơ sản xuất và quy chuẩn chuyên biệt**
   - quyết định của bài cụ thể;
   - trạng thái sản xuất và xuất bản;
   - phần mở rộng nghiệp vụ của dự án;
   - bằng chứng kiểm định và nghiệm thu.

4. **QMD, tài nguyên và đầu ra**
   - tệp nguồn;
   - hình và dữ liệu;
   - HTML;
   - PDF;
   - dữ liệu danh mục khi áp dụng.

Checker tạo hợp đồng hiệu lực từ lõi, cấu hình dự án và mô-đun được đăng kí, rồi chỉ kiểm tra phần có thể mã hóa.

## 3. Thành phần triển khai

### 3.1. Giao diện kĩ thuật của agent

```text
scripts/zo_qmd.py
scripts/zo_qmd_package.py
```

Trạng thái phiên bản:

```text
CURRENT OPERATIONS RELEASE: 0.5.0
QMD OPERATIONS CLI: 0.5.0
PACKAGE MODULE: 0.4.0
```

Các lệnh đã triển khai:

```text
doctor
inspect
start
review-ready
prepublish
check
render
regression
pack
verify
```

Cách agent gọi chuẩn trong repository:

```bash
python scripts/zo_python.py scripts/zo_qmd.py <command> [tham số...]
```

`start` nhận yêu cầu, tái sử dụng kết quả nhận diện của `inspect`, rồi tạo manifest phiên JSON; nếu không truyền `--output`, tên chuẩn là `_audit/<slug>_session.json`. Với dự án bật lifecycle canonical như `functions_100`, `start` phải chạy trước khi sửa candidate, tự suy ra phạm vi production thay vì bắt agent tự đoán `--allow`, chụp fingerprint của các thay đổi đã tồn tại và khóa authority set bằng SHA-256. Manifest đặt `review-ready` sau `render` và trước `human_review`. `review-ready` đọc policy trong `extensions.human_review_gate`, bắt buộc session hợp lệ, đối chiếu HEAD/target/project, kiểm authority drift và so phần thay đổi kể từ `start` với scope canonical trước khi kiểm tiếp navigation, đồ thị, hồ sơ và artifact. Lệnh này không thay checker lõi, không tự sửa candidate, không nghiệm thu và luôn giữ `final_acceptance: NOT_RUN`, `publication: pending`. `prepublish` đọc manifest phiên, báo cáo `check`, báo cáo `render` và bảng kiểm có người quan sát để tạo báo cáo tổng hợp; lệnh này không chạy lại checker, không tự đặt trạng thái `accepted`, không sửa hồ sơ sản xuất và luôn giữ `publication: pending`. Khi bảng kiểm hợp lệ đã ghi `production_status: accepted`, báo cáo chỉ phản ánh bằng chứng ấy để chờ quyết định xuất bản riêng của người dùng.

Các lệnh `check` và `render` chuyển trách nhiệm kiểm định cho checker hiện hành. `review-ready` là lớp enforcement riêng ở cổng lifecycle, dùng khi dự án đã khai báo policy; tách lớp này giúp giữ checker `2.6.0` ổn định trong khi vẫn khóa các invariant production đã được chứng minh qua kiểm thử. `regression` đọc bài hồi quy từ cấu hình dự án, chạy các self-test bắt buộc rồi điều phối hồi quy nguồn và, khi được yêu cầu, hồi quy render.

`pack` tạo gói context hoặc release dạng thư mục hay ZIP tại đường dẫn đầu ra bắt buộc, sinh `PROMPT.md`, `MANIFEST.yml`, `FILES.sha256` và `payload/`. Gói release chỉ được tạo từ worktree sạch, dùng hồ sơ `--release-file` và đầu ra ngoài repository. `verify` xác minh cả hai loại gói, kể cả khi chạy bằng CLI nằm trong chính gói và không có repository Git bao quanh.

### 3.2. Checker lõi

```text
scripts/zo_check_repo.py
```

Checker lõi giữ giao diện ổn định để lớp vận hành điều phối và để bảo trì, chẩn đoán chuyên sâu. Với vòng đời thông thường của một bài QMD có cấu hình, agent không gọi trực tiếp checker mà dùng `scripts/zo_qmd.py check` hoặc `scripts/zo_qmd.py render`.

Phiên bản đường cơ sở của hệ thống 1.0:

```text
CHECKER VERSION: 2.6.0
```

Các lệnh được giữ ổn định:

```text
quick
scope
render
--staged
--report
```

### 3.3. Bộ đọc cấu hình

```text
scripts/zo_qmd_config.py
```

Trách nhiệm:

- tìm cấu hình gần nhất;
- nạp YAML an toàn và từ chối khóa trùng;
- kiểm tra schema phiên bản 1;
- xác định loại bài;
- xác định đường dẫn hồ sơ;
- từ chối mô-đun chưa đăng kí và đường dẫn không an toàn.

### 3.4. Validator lõi

```text
scripts/zo_qmd_core.py
```

Chứa các kiểm tra dùng chung như front matter, metadata, placeholder, tiêu đề, hình, tài nguyên, đường dẫn bị cấm và mã thực thi.

### 3.5. Registry mô-đun

```text
scripts/zo_qmd_registry.py
```

Registry cố định trong Python; YAML không được gọi hàm hoặc import mã tùy ý.

Các mã mô-đun của phiên bản 1.0:

```text
qmd-core
zo-html-pdf
content-blocks
figure-layout
card-grid
functions-article
real-world-problem
```

### 3.6. Validator dự án

- `functions-article`: được cài trong checker hiện hành;
- `real-world-problem`: được cài tại `scripts/zo_real_world_problem.py`.

Mỗi adapter chỉ chạy cho loại bài mà registry cho phép.

## 4. Hai dự án đường cơ sở

### 4.1. 100+ Hàm số: Sự biến thiên và đồ thị

Cấu hình:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Bài hồi quy:

```text
content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
```

Loại bài và adapter:

```text
function_article
functions-article
```

Bất biến quan trọng:

- thẻ 114 giữ `pending`;
- `href` của thẻ vẫn rỗng;
- PDF Title khớp `title-meta`;
- PDF đường cơ sở có 15 trang;
- số hình mở rộng của bài là 0;
- không sửa nội dung bài để làm checker vượt qua.

### 4.2. 100+ Bài toán thực tế

Cấu hình:

```text
content/thpt/zo_math_100/100_bai_toan_thuc_te/_quy_trinh/cau_hinh_san_xuat_qmd.yml
```

Bài hồi quy:

```text
content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd
```

Loại bài và adapter:

```text
real_world_problem
real-world-problem
```

Bất biến quan trọng:

- không mang `listing-order` hoặc metadata riêng của dự án hàm số;
- đủ bốn phần mô hình hóa bắt buộc;
- hồ sơ giữ `production: in_production` và `publication: pending`;
- HTML có liên kết PDF;
- PDF đường cơ sở có 4 trang;
- không xuất bản trong quá trình kiểm nghiệm hệ thống.

Đường cơ sở hợp nhất được ghi tại `duong_co_so_hoi_quy_hai_du_an.md`.

## 5. Quy trình kiểm định ngắn hiện hành

### 5.1. Kiểm tra môi trường

```bash
python scripts/zo_python.py scripts/zo_qmd.py doctor
```

### 5.2. Xác định dự án và loại bài

```bash
python scripts/zo_python.py scripts/zo_qmd.py inspect \
  <duong_dan_den_bai_qmd>
```

### 5.3. Kiểm tra nguồn

```bash
python scripts/zo_python.py scripts/zo_qmd.py check \
  <duong_dan_den_bai_qmd>
```

### 5.4. Kiểm tra và render

```bash
python scripts/zo_python.py scripts/zo_qmd.py render \
  <duong_dan_den_bai_qmd>
```

### 5.5. Kiểm tra readiness trước Human Review

Với dự án đã bật `extensions.human_review_gate`, sau `check` và `render` cuối chạy:

```bash
python scripts/zo_python.py scripts/zo_qmd.py review-ready \
  --report _audit/<slug>_review_ready.json \
  <duong_dan_den_bai_qmd>
```

`PASS` của cổng này chỉ cho phép chuyển candidate sang Human Review; không thay thế đánh giá của con người.

### 5.6. Kiểm tra index trước commit

```bash
python scripts/zo_python.py scripts/zo_qmd.py check --staged \
  <cac_duong_dan_da_stage>

git diff --cached --check
```

Báo cáo JSON chỉ được ghi bên trong `_audit/`:

```bash
python scripts/zo_python.py scripts/zo_qmd.py check \
  --report _audit/bao_cao.json \
  <duong_dan>
```

## 6. Trạng thái và quyền xuất bản

Hai trục độc lập:

```text
production: draft → in_production → validated → accepted
publication: pending → published
```

Các bất biến:

- `validated` chỉ có nghĩa là kiểm định có thể mã hóa không còn `FAIL`;
- `accepted` cần kiểm định có người quan sát;
- `accepted` không tự động thành `published`;
- `published` luôn cần xác nhận rõ của người dùng;
- checker không tự đổi trạng thái, không stage, không commit và không xuất bản.

## 7. Phân loại tài liệu trong thư mục

### 7.1. Tài liệu lõi kĩ thuật phiên bản 1.0

- `README.md`;
- `kien_truc_he_thong.md`;
- `hop_dong_loi_va_du_an.md`;
- `cau_truc_cau_hinh_du_an.md`;
- `vong_doi_bai_qmd.md`;
- `duong_co_so_hoi_quy_hai_du_an.md`;
- `huong_dan_them_du_an_va_validator.md`;
- `tieu_chi_nghiem_thu_he_thong.md`.

### 7.2. Tài liệu lớp vận hành

Hợp đồng nền và nghiệm thu:

- `kien_truc_van_hanh_co_may_qmd.md`;
- `giao_thuc_agent_chat_box_va_goi_ngu_canh.md`;
- `tieu_chi_nghiem_thu_lop_van_hanh.md`;
- `mau_manifest_goi_qmd.yml`.

Hợp đồng phát hành O3:

- `ma_tran_phien_ban_qmd.md`;
- `CHANGELOG.md`;
- `quy_trinh_phat_hanh_va_khoi_phuc_qmd.md`;
- `mau_ho_so_phat_hanh_qmd.yml`.

CLI cơ bản và gói context đã có bằng chứng O2. O3 đã có release candidate `0.3.0` được tạo từ commit sạch, đạt xác minh bằng CLI ngoài repository và CLI tự chứa trong payload; hồi quy trước–sau, rollback drill và bằng chứng hậu đóng gói được lưu tại `phat_hanh/qmd_ops_0_3_0/`. Phiên trình diễn đầu-cuối thuộc O4.

### 7.3. Hồ sơ chuyển đổi

- `ke_hoach_chuyen_doi.md`;
- `duong_co_so_hoi_quy_ham_ln_x.md`.

Hai tài liệu này ghi lại đường chuyển đổi và đường cơ sở ban đầu; không dùng chúng để khôi phục nhánh legacy đã loại bỏ.

### 7.4. Hồ sơ lịch sử Giai đoạn 0

- `kiem_ke_he_thong_hien_tai.md`;
- `ban_do_kien_truc_hien_trang.md`;
- `phan_loai_quy_tac_chung_rieng.md`.

Các tài liệu lịch sử mô tả bằng chứng và giả định tại thời điểm khảo sát. Khi khác với tài liệu vận hành phiên bản 1.0, tài liệu vận hành hiện hành được ưu tiên trong phạm vi cỗ máy QMD.

## 8. Bất biến của phiên bản 1.0

- cấu hình dự án là YAML khai báo, không thực thi mã;
- mọi dự án phải dùng cấu hình cục bộ tại vị trí chuẩn;
- `qmd-core` là mô-đun bắt buộc;
- checker giữ một điểm vào thống nhất;
- validator dự án chỉ chạy đúng loại bài;
- không còn đường chạy legacy hoặc fallback cho bài hàm số thiếu cấu hình;
- hai dự án hồi quy phải cùng đạt trước khi đổi lõi, loader, registry hoặc dispatch;
- kiểm định tự động không thay thế nghiệm thu của con người;
- xuất bản vẫn thuộc quyền quyết định của người dùng.

## 9. Đường chuyển đổi đã hoàn tất

Các commit nền của phiên bản 1.0:

```text
b8740b0  docs(qmd-system): define architecture and baseline
48ae4f3  feat(qmd-system): add project configuration foundation
9c92cd2  refactor(checker): discover configured qmd projects
d386588  refactor(qmd-system): move function rules into project config
2ae9661  refactor(qmd-system): extract shared qmd core validator
e6371d6  refactor(qmd-system): add validator registry and dispatch
b577787  refactor(qmd-system): switch functions project to native mode
31a1916  feat(real-world): add initial qmd project configuration
ab7581a  refactor(qmd-system): remove legacy compatibility path
```

Commit khóa tài liệu M9B hoàn tất phiên bản 1.0 mà không thay đổi QMD hồi quy hoặc trạng thái xuất bản.

## 10. Trạng thái hoàn tất O2–O4

O2 đã triển khai và kiểm nghiệm `pack` cùng `verify` trên gói context dạng thư mục và ZIP, bao gồm các trường hợp tệp thiếu, tệp thừa, checksum sai, danh sách checksum chưa sắp xếp và việc chạy CLI trong thư mục sạch.

Release `0.3.0` đã hoàn tất O3: `pack --kind release` và `verify` đã được kiểm nghiệm; release candidate được tạo từ commit sạch; hai lớp xác minh đều đạt; rollback drill đạt; hai QMD hồi quy giữ nguyên SHA-256 và trạng thái xuất bản vẫn `pending`. Git tag thật chưa được tạo, không push và không publish.

O4 đã hoàn tất các phép thử, hồ sơ nghiệm thu, gói context cuối, hồi quy có render, rollback drill và release candidate `0.4.0` được xác minh. Người dùng đã chấp thuận `0.4.0` làm release hiện hành và khóa lớp vận hành ở mốc nghiệm thu `1.0`; chưa tag, push hoặc publish.

## Q1-R5 — authority closure và ownership của trạng thái

Đối với dự án đã bật `human_review_gate`, `start` không chỉ chụp một danh sách `references` phẳng. Cấu hình dự án khai `authority_registry` theo vai trò `governing_required`, `conditional_required`, `provenance_required` và `reference_only`; Cỗ máy hợp nhất registry với chuỗi `AGENTS.md` thực tế và project config để tạo **effective authority closure**. Session manifest ghi path, role, activation reason, SHA-256 và trạng thái lock. Nguồn `reference_only` được inventory nhưng chỉ trở thành provenance bắt buộc khi hồ sơ khai đã dùng.

Hồ sơ production từ schema version 5 là **agent-owned profile**. Check/render/freshness/Git/authority và trạng thái đầu ra HTML/PDF thuộc machine-owned audit; profile không có nhóm `dau_ra_ki_thuat`. `tu_xem` là agent self-view riêng; Human Review và nghiệm thu nằm ngoài profile. `review-ready` kiểm schema/ownership, yêu cầu hồ sơ giữ cấu trúc template cùng các ID checklist tự kiểm, và đọc trực tiếp các bằng chứng machine-owned thay vì yêu cầu agent chép trạng thái kiểm định vào YAML. Mục tiêu của phân tách này là giảm trạng thái lặp, stale SHA và khác biệt giữa các fresh run.
