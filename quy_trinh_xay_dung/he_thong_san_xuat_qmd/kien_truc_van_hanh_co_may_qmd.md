# Kiến trúc vận hành cỗ máy QMD

> **Trạng thái:** Release hiện hành của lớp vận hành là `0.3.0`; O3 đã hoàn tất. O4 đang triển khai với CLI ứng viên `0.4.0`; bảy mục tiêu, gói context cuối, hồi quy có render và rollback drill O4 đều đã có bằng chứng. Release candidate `0.4.0` chưa được tạo hoặc xác minh; việc khóa lớp vận hành `1.0` vẫn cần quyết định riêng của người dùng sau khi RC đạt.
>
> Tài liệu này bao quanh lõi kĩ thuật của Hệ thống sản xuất và kiểm định QMD phiên bản 1.0. Nó không thay thế `kien_truc_he_thong.md`, `hop_dong_loi_va_du_an.md` hoặc các quy chuẩn chuyên biệt của từng dự án.

## 1. Mục đích

Lõi QMD 1.0 đã có loader cấu hình, registry, validator dùng chung, adapter dự án, checker và đường hồi quy hai dự án. Lớp vận hành được bổ sung để một người dùng, một agent trong VS Code hoặc một chat-box có thể sử dụng lõi ấy theo cùng một quy trình, không phụ thuộc vào lịch sử hội thoại.

Lớp vận hành phải trả lời rõ bốn câu hỏi:

1. Bắt đầu từ đâu?
2. Phải nạp những nguồn nào?
3. Phải chạy những cổng kiểm soát nào?
4. Bàn giao bằng chứng theo định dạng nào?

## 2. Quan hệ với lõi kĩ thuật 1.0

Kiến trúc tổng thể gồm chuỗi trách nhiệm:

```text
người dùng
    ↓ yêu cầu bằng ngôn ngữ tự nhiên và quyết định
agent
    ↓ diễn giải yêu cầu, đọc thẩm quyền, sản xuất và điều phối
lớp vận hành
    ↓ CLI, đóng gói, báo cáo và cổng kiểm soát
lõi kĩ thuật QMD 1.0
    ↓ kiểm định phần có thể mã hóa
cấu hình dự án
    ↓
hồ sơ và quy chuẩn chuyên biệt
    ↓
QMD, tài nguyên và đầu ra
```

Lớp vận hành không phải một tầng nghiệp vụ mới chen vào hợp đồng hiệu lực của checker. Nó là lớp bao quanh, có trách nhiệm:

- định hướng người vận hành đến đúng điểm vào;
- khám phá dự án và nguồn có thẩm quyền;
- khóa phạm vi nhiệm vụ;
- điều phối các lệnh hiện có;
- tạo và kiểm tra gói ngữ cảnh;
- tạo báo cáo trước xuất bản;
- tổ chức bảo trì, phát hành và khôi phục.

Lớp vận hành không được:

- thay đổi kết quả toán học hoặc nội dung chuyên môn;
- tự tạo ngoại lệ cho validator;
- tự chuyển trạng thái sang `accepted` hoặc `published`;
- tự stage, commit hoặc xuất bản;
- đưa nghiệp vụ của một dự án vào lõi dùng chung;
- mô tả chức năng chưa triển khai như thể đã có.

### 2.1. Ranh giới lưu trữ

Lớp vận hành phải giữ hai vùng tài liệu tách biệt:

```text
quy_trinh_xay_dung/he_thong_san_xuat_qmd/
    → hợp đồng, giao thức, mẫu và tiêu chí toàn hệ thống

content/.../<du_an>/_quy_trinh/
    → cấu hình, hồ sơ, mẫu và quy chuẩn chuyên biệt của dự án
```

Không đưa giao thức toàn hệ thống vào `_quy_trinh` của một dự án. Không đưa hồ sơ hoặc quy tắc riêng của một dự án vào tài liệu lõi chỉ để thuận tiện cho một phiên làm việc.

### 2.2. Ba cổng kiểm soát

- **V — Validation:** kiểm định tự động phần có thể mã hóa; kết quả không còn `FAIL` không phải nghiệm thu cuối.
- **A — Acceptance:** kiểm định có người quan sát; chỉ tại đây nội dung và đầu ra mới có thể được chấp nhận.
- **P — Publication:** quyết định xuất bản riêng của người dùng.

Không cổng nào tự động mở cổng tiếp theo.

### 2.3. Ba giao diện và phạm vi hỗ trợ

Cỗ máy có ba giao diện khác nhau:

1. **Người dùng → agent:** người dùng mô tả nhiệm vụ bằng ngôn ngữ tự nhiên, chẳng hạn "Hãy viết về hàm $y=e^x$". Đây là điểm khởi đầu thông thường.
2. **Agent → lớp vận hành:** agent dùng `scripts/zo_qmd.py` để nhận diện, lập kế hoạch, kiểm định, render, đóng gói và báo cáo. Người dùng không phải nhớ giao diện này.
3. **Lớp vận hành → checker lõi:** `scripts/zo_check_repo.py` thực thi validator phía sau; không phải giao diện thông thường của người dùng hoặc agent sản xuất bài.

Phạm vi O4 chỉ gồm các dự án đã được tích hợp, hiện có `functions_100` và `real_world_100`. Kiến trúc cho phép bổ sung dự án khác, nhưng việc khởi tạo cấu hình, loại bài, quy chuẩn và đường hồi quy cho một dự án mới là một mốc riêng, không phải khả năng tự động đã được O4 chứng minh.

## 3. Giao diện kĩ thuật thống nhất của agent

Điểm vào đích của lớp vận hành là:

```bash
python scripts/zo_python.py scripts/zo_qmd.py <command> [tham số...]
```

Trong nhánh ứng viên O4, `scripts/zo_qmd.py` phiên bản `0.4.0` là điểm vào vận hành cho:

```text
doctor
inspect
start
prepublish
check
render
regression
pack
verify
```

Điểm vào kiểm định lõi vẫn là:

```bash
python scripts/zo_python.py scripts/zo_check_repo.py ...
```

`zo_qmd.py` điều phối các thành phần hiện có, không sao chép validator và không thay đổi hợp đồng của `zo_check_repo.py`. `pack --kind context|release` và `verify` được triển khai qua `scripts/zo_qmd_package.py`; `context` là mặc định tương thích ngược và `--release-file` bắt buộc cho gói release. `start` tạo manifest phiên và kế hoạch từ yêu cầu ban đầu; `prepublish` gọi `scripts/zo_qmd_prepublish.py` để tổng hợp bằng chứng đã có, chỉ phản ánh trạng thái `accepted` khi bảng kiểm có người quan sát đã ghi nhận trạng thái ấy, không sửa hồ sơ và không xuất bản. Release hiện hành vẫn là `0.3.0` cho đến khi O4 hoàn tất và một quyết định phát hành riêng được thực hiện.

### 3.1. Bộ lệnh đích

| Lệnh | Trách nhiệm | Được sửa tệp nội dung? |
|---|---|---:|
| `doctor` | Kiểm tra môi trường, tệp bắt buộc và khả năng gọi các công cụ | Không |
| `inspect` | Nhận diện repository, dự án, loại bài, hồ sơ và nguồn có thẩm quyền | Không |
| `start` | Tạo bản tóm tắt phiên và kế hoạch sản xuất từ yêu cầu ban đầu | Chỉ tạo hồ sơ phiên khi được yêu cầu |
| `check` | Điều phối kiểm định nguồn qua checker hiện hành | Không |
| `render` | Điều phối kiểm định nguồn, render và kiểm định đầu ra | Chỉ tạo đầu ra và báo cáo |
| `regression` | Chạy đường cơ sở hai dự án và self-test bắt buộc | Không sửa bài hồi quy |
| `pack` | Tạo gói ngữ cảnh hoặc gói phát hành theo manifest | Chỉ tạo gói |
| `verify` | Kiểm tra manifest, checksum, tệp bắt buộc và tính nhất quán | Không |
| `prepublish` | Tổng hợp bằng chứng và tạo báo cáo trước xuất bản | Không xuất bản |

### 3.2. Nguyên tắc tương thích

- `zo_check_repo.py` tiếp tục là checker thống nhất của lõi 1.0.
- `zo_qmd.py` là mặt tiền vận hành, không phải checker thứ hai.
- Các lệnh cũ chỉ bị thay đổi khi có đường di trú, hồi quy và quyết định phiên bản rõ ràng.
- Mọi lệnh Python vẫn đi qua `scripts/zo_python.py`.
- Mọi lệnh Quarto vẫn đi qua `scripts/zo_quarto.py` theo chỉ dẫn cấp repository.

## 4. Một vòng vận hành chuẩn

Một nhiệm vụ QMD phải đi qua các pha sau:

```text
A. Khởi động
→ B. Khóa phạm vi và nguồn điều khiển
→ C. Lập kế hoạch
→ D. Sản xuất hoặc chỉnh sửa
→ E. Kiểm định tự động
→ F. Kiểm định có người quan sát
→ G. Báo cáo trước xuất bản
→ H. Xuất bản khi người dùng xác nhận riêng
```

### 4.1. Pha A — Khởi động

- xác định đang làm trên repository sống hay gói ngữ cảnh;
- ghi branch, commit và trạng thái worktree nếu có thể;
- chạy hoặc mô phỏng `doctor`;
- phát hiện tệp bắt buộc còn thiếu;
- không bắt đầu sửa khi chưa xác định được nguồn có thẩm quyền.

### 4.2. Pha B — Khóa phạm vi và nguồn điều khiển

- xác định dự án và `article_type`;
- đọc `AGENTS.md` từ ngoài vào trong; với hai dự án đường cơ sở hiện hành, chuỗi kết thúc tại:
  - `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/AGENTS.md`;
  - `content/thpt/zo_math_100/100_bai_toan_thuc_te/AGENTS.md`;
- nạp cấu hình dự án trong `_quy_trinh/`;
- xác định hồ sơ bài;
- kích hoạt tài liệu chuyên trách theo điều kiện;
- phân biệt tài liệu vận hành hiện hành với tài liệu lịch sử;
- ghi danh sách tệp được phép tác động và tệp bị loại trừ.

### 4.3. Pha C — Lập kế hoạch

Kế hoạch phải nêu:

- mục tiêu đầu ra;
- tệp dự kiến tạo hoặc sửa;
- cổng cần người dùng quyết định;
- kiểm định cần chạy;
- điều kiện dừng;
- trạng thái không được thay đổi.

### 4.4. Pha D — Sản xuất hoặc chỉnh sửa

- chỉ tác động tệp trong phạm vi đã khóa;
- không dùng bài hồi quy để chữa lỗi checker;
- không tự sửa tài liệu điều khiển khi nhiệm vụ chỉ là sản xuất bài;
- ghi nhận mọi ngoại lệ vào hồ sơ hoặc báo cáo phù hợp.

### 4.5. Pha E — Kiểm định tự động

Tối thiểu phải chọn đúng một trong các mức:

```text
check       kiểm định nguồn
render      kiểm định nguồn + đầu ra
regression  kiểm định lõi và hai đường cơ sở
```

Kết quả tự động chỉ được diễn giải theo hợp đồng của checker:

```text
PASS / WARN / FAIL / INFO
FINAL ACCEPTANCE: NOT_RUN
```

### 4.6. Pha F — Kiểm định có người quan sát

Người quan sát kiểm tra phần mà checker không thể kết luận đầy đủ, gồm:

- tính đúng toán học;
- chất lượng lập luận;
- giá trị nhận thức và sư phạm;
- hình và bố cục;
- HTML/PDF ở kích thước sử dụng thực tế;
- ngoại lệ thiết kế;
- mức độ sẵn sàng để nghiệm thu.

### 4.7. Pha G — Báo cáo trước xuất bản

Báo cáo phải tổng hợp:

- snapshot và phạm vi;
- nguồn có thẩm quyền đã dùng;
- tệp đã tác động;
- lệnh và mã thoát;
- kết quả kiểm định nguồn, render và trực quan;
- trạng thái sản xuất;
- trạng thái xuất bản;
- vấn đề còn lại;
- quyết định còn chờ người dùng.

`prepublish` không được đổi `pending` thành `published`.

### 4.8. Pha H — Xuất bản

Xuất bản nằm ngoài phạm vi tự động của cỗ máy QMD. Chỉ thực hiện theo quy trình xuất bản website và khi người dùng yêu cầu rõ.

## 5. Ba môi trường vận hành

### 5.1. Người dùng

Người dùng phải có thể:

- giao một nhiệm vụ bằng ngôn ngữ tự nhiên trong dự án đã được tích hợp;
- hiểu agent chịu trách nhiệm vận hành repository, còn checker chỉ kiểm tra phần có thể mã hóa;
- nhận biết đầu ra gồm QMD, tài nguyên, HTML/PDF và báo cáo khi áp dụng;
- phân biệt kiểm định tự động, chấp nhận của con người và quyết định xuất bản;
- biết rằng dự án chưa được tích hợp cần một nhiệm vụ khởi tạo riêng.

Người dùng không phải nhớ tên script hoặc cú pháp Terminal để sử dụng cỗ máy trong vòng đời thông thường.

### 5.2. Agent trong VS Code

Agent có quyền đọc repository và chạy lệnh. Agent phải:

- xác nhận trạng thái Git trước khi tác động;
- đọc đầy đủ chuỗi `AGENTS.md`;
- dùng điểm vào vận hành thống nhất khi đã được triển khai;
- không dựa vào lịch sử chat để bù cho tài liệu thiếu;
- báo rõ lệnh đã chạy và bằng chứng thực tế;
- không claim kiểm định trực quan nếu chưa quan sát đầu ra.

### 5.3. Chat-box

Chat-box có thể không truy cập repository sống. Chat-box phải làm việc qua gói ngữ cảnh chuẩn và:

- kiểm tra manifest trước khi suy luận;
- phân biệt bằng chứng trong gói với điều chưa thể xác nhận;
- không tự điền tệp hoặc trạng thái bị thiếu;
- không claim đã chạy lệnh nếu gói không chứa bằng chứng;
- trả lại bản đồ, bản vá, tệp mới hoặc chỉ dẫn có thể chuyển giao cho agent trong VS Code.

Giao thức chi tiết được quy định tại `giao_thuc_agent_chat_box_va_goi_ngu_canh.md`.

## 6. Gói ngữ cảnh và gói phát hành

Hệ thống dùng hai loại gói:

1. **Gói ngữ cảnh** — phục vụ bàn giao nhiệm vụ cho chat-box hoặc agent mới.
2. **Gói phát hành** — đóng băng một phiên bản lớp vận hành cùng mã, tài liệu và bằng chứng hồi quy.

Cả hai phải có:

```text
PROMPT.md
MANIFEST.yml
FILES.sha256
payload/
```

`payload/` giữ nguyên đường dẫn tương đối của repository để nguồn dẫn chiếu không bị mất ngữ cảnh.

Tệp mẫu và quy chuẩn đóng gói được theo dõi trong Git. Gói được sinh, báo cáo phiên và tệp tạm là sản phẩm vận hành: lệnh tạo chúng phải yêu cầu vị trí đầu ra tường minh. Không mặc định ghi vào gốc repository hoặc thư mục dự án. Nếu người dùng yêu cầu giữ báo cáo trong repository, vị trí phải thuộc vùng đã được quy định, chẳng hạn `_audit/` đối với báo cáo checker.

Không được coi một ZIP chỉ có danh sách tệp và commit trong comment là gói chuẩn.

## 7. Phiên bản

Các phiên bản được quản lí độc lập:

| Thành phần | Release trước `0.2.0` | Hiện hành `0.3.0` | Ứng viên O4 |
|---|---:|---:|---:|
| Lõi kĩ thuật QMD | `1.0` | `1.0` | `1.0` |
| Checker | `2.6.0` | `2.6.0` | `2.6.0` |
| Schema cấu hình dự án | `1` | `1` | `1` |
| Hợp đồng lớp vận hành | `0.2` | `0.3` | `0.4` |
| Schema manifest gói | `1` | `1` | `1` |
| Schema hồ sơ phát hành | Chưa có | `1` | `1` |
| Schema manifest phiên `start` | Chưa có | Chưa có | `1` |
| Schema báo cáo `prepublish` | Chưa có | Chưa có | `1` |
| CLI vận hành | `0.2.0` | `0.3.0` | `0.4.0` |
| Mô-đun đóng gói | `0.2.0` | `0.3.0` | `0.3.0` |

Lớp vận hành dùng phiên bản `MAJOR.MINOR.PATCH`:

- `MAJOR`: thay đổi không tương thích về CLI, manifest hoặc giao thức;
- `MINOR`: thêm khả năng tương thích ngược;
- `PATCH`: sửa lỗi hoặc làm rõ tài liệu không phá hợp đồng.

Release `0.3.0` thêm khả năng tạo và xác minh release candidate nhưng giữ nguyên giao diện context của O2, nên mức tăng là `MINOR`. Schema manifest gói vẫn là `1` vì `package.kind: release` và nhóm `release` đã thuộc hợp đồng schema hiện hành.

Ứng viên `0.4.0` bổ sung hai lệnh tương thích ngược `start` và `prepublish`, đồng thời thêm schema manifest phiên cùng schema báo cáo trước xuất bản ở phiên bản `1`. Checker, lõi, schema cấu hình, schema manifest gói và mô-đun đóng gói không đổi. Đây mới là mã ứng viên O4, chưa phải release hiện hành.

Ma trận đầy đủ, điểm quay lại và điều kiện có hiệu lực được khóa tại `ma_tran_phien_ban_qmd.md`. Toàn bộ điều kiện O3 đã đạt nên `0.3.0` vẫn là phiên bản hiện hành; lớp vận hành chưa được gọi là phiên bản 1.0 trước khi hoàn thành O4.

## 8. Bảo trì, phát hành và khôi phục

### 8.1. Phân loại thay đổi

Mọi thay đổi phải được gắn ít nhất một loại:

- tài liệu vận hành;
- CLI;
- checker;
- loader hoặc registry;
- schema cấu hình;
- schema manifest;
- adapter dự án;
- đầu ra render;
- đường hồi quy.

Loại thay đổi quyết định phạm vi self-test, hồi quy và mức phiên bản cần nâng.

### 8.2. Điều kiện phát hành

Một release candidate chỉ được tạo khi:

- worktree phát hành sạch; worktree bẩn chỉ có thể dùng để khảo sát, không được gọi là release candidate;
- self-test bắt buộc đạt;
- hồi quy nguồn và render của hai dự án đạt;
- manifest và checksum được xác minh;
- tài liệu hiện hành nhất quán;
- changelog nêu rõ thay đổi và đường di trú;
- ma trận phiên bản, release checklist và rollback log có mặt;
- không có thay đổi trạng thái xuất bản ngoài phạm vi.

Giao thức chi tiết, hồ sơ đầu vào và đường dẫn bằng chứng được quy định tại `quy_trinh_phat_hanh_va_khoi_phuc_qmd.md` và `mau_ho_so_phat_hanh_qmd.yml`.

### 8.3. Khôi phục

Khôi phục phải dựa trên phiên bản và commit đã biết, ưu tiên worktree hoặc nhánh riêng bên ngoài repository sống. Không dùng thao tác phá hủy worktree đang chứa thay đổi ngoài phạm vi.

Một diễn tập khôi phục đạt khi:

- xác định được `previous_version` và `previous_commit`;
- dựng lại được worktree previous trực tiếp từ commit ấy;
- chạy lại được kiểm tra bắt buộc;
- hai bài hồi quy giữ nguyên SHA-256 và không bị sửa để thích nghi;
- trạng thái `pending` được bảo toàn;
- log ghi đủ lệnh, mã thoát và kết quả.

Điểm quay lại của O3 là lớp vận hành `0.2.0` tại commit `c1b26b9a0536b17e0885d8158fddbd20413767c2`.

## 9. Phiên trình diễn đầu-cuối

Phiên trình diễn bắt đầu từ một yêu cầu bằng ngôn ngữ tự nhiên trong dự án đã được tích hợp, nhưng không sửa hai bài hồi quy và không tạo dự án mới chỉ để biểu diễn.

Chuỗi bằng chứng bắt buộc:

```text
yêu cầu ban đầu
→ inspect
→ khóa nguồn điều khiển
→ hồ sơ và kế hoạch
→ sản phẩm QMD/tài nguyên
→ check
→ render
→ kiểm định trực quan
→ prepublish
```

Phiên trình diễn phải kết thúc trước cổng xuất bản. Báo cáo cuối phải ghi rõ `publication: pending` trừ khi có một nhiệm vụ xuất bản riêng của người dùng.

## 10. Các mốc triển khai

### O0 — Khóa kiến trúc vận hành

- tài liệu kiến trúc;
- giao thức agent/chat-box;
- schema gói và manifest;
- tiêu chí nghiệm thu;
- không sửa mã.

### O1 — Điểm vào CLI thống nhất — đã triển khai

- `zo_qmd.py` phiên bản `0.1.0`;
- đã có `doctor`, `inspect`, `check`, `render`, `regression`;
- checker `2.6.0` vẫn là lõi kiểm định;
- self-test, hồi quy nguồn và hồi quy render hai dự án đã đạt.

### O2 — Gói ngữ cảnh chuẩn — đã triển khai

- `zo_qmd.py` và `zo_qmd_package.py` phiên bản `0.2.0`;
- `pack` tạo gói ngữ cảnh dạng thư mục hoặc ZIP tại đầu ra tường minh;
- `verify` kiểm tra schema manifest, tệp bắt buộc, symlink, tệp thiếu, tệp thừa, checksum sai và thứ tự `FILES.sha256`;
- gói đã tự xác minh bằng CLI trong `payload/` từ thư mục sạch;
- trình khởi chạy Python khóa việc sinh bytecode để không làm thay đổi gói sau khi chạy.

### O3 — Phát hành, bảo trì và khôi phục — đã hoàn tất

- đã khóa ma trận phiên bản, changelog, giao diện `pack --kind`, hồ sơ release và quy trình rollback;
- đã triển khai tạo và xác minh gói release cùng self-test;
- hồi quy trước–sau và rollback drill đã đạt, với hồ sơ lưu tại `phat_hanh/qmd_ops_0_3_0/`;
- release candidate `0.3.0` đã được tạo từ commit sạch và đạt xác minh ngoài repository lẫn bằng CLI tự chứa trong payload;
- Git tag thật chưa được tạo, không push và không publish.

### O4 — Trình diễn và nghiệm thu — đang triển khai

Đã hoàn thành trong mã ứng viên:

- `start` tạo manifest phiên, khóa phạm vi và kế hoạch tại đầu ra tường minh;
- `prepublish` tổng hợp bằng chứng, chặn trường hợp thiếu kiểm định có người quan sát và giữ `publication: pending`;
- self-test, phép thử cấu trúc và hồi quy nguồn đã đạt; hai QMD đường cơ sở giữ nguyên SHA-256.

Còn phải hoàn thành:

- tạo và xác minh gói context từ trạng thái O4;
- phép thử chat-box mới chỉ dùng gói;
- chạy phiên đầu-cuối với yêu cầu mới;
- thu bằng chứng cho bảy mục tiêu;
- chỉ khi đạt mới cân nhắc khóa lớp vận hành 1.0.

## 11. Bất biến của lớp vận hành

- một điểm vào vận hành, một checker lõi;
- không sao chép validator;
- không dùng gói thiếu manifest như nguồn tái tạo;
- không trộn tài liệu lịch sử với tài liệu hiện hành;
- không claim hành động chưa thực hiện;
- không tự nghiệm thu;
- không tự xuất bản;
- không sửa bài hồi quy để vượt kiểm tra;
- không dùng `git add .`;
- không mặc định sinh gói, báo cáo phiên hoặc tệp tạm vào repository;
- luôn kiểm tra diff trước commit;
- mọi chức năng chưa triển khai phải được ghi rõ là đích kiến trúc.

## 12. Kết luận

Lớp vận hành hoàn chỉnh phải biến lõi QMD 1.0 từ một hệ thống kĩ thuật có thể dùng thành một cỗ máy có thể được hiểu, khởi động, bàn giao, kiểm tra, phát hành và khôi phục theo một giao thức lặp lại được.

Mốc O0 chỉ khóa hợp đồng này. Nó không tuyên bố CLI, gói phát hành hoặc phiên trình diễn đã tồn tại.
