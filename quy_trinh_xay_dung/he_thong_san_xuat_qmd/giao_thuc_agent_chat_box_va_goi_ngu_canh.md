# Giao thức cho agent, chat-box và gói ngữ cảnh QMD

> **Trạng thái:** Release hiện hành của lớp vận hành là `0.3.0`; release candidate và rollback drill của O3 đã đạt. O4 đang triển khai với CLI ứng viên `0.4.0`; `start` và `prepublish` đã có mã, còn phép thử chat-box chỉ dùng gói O4 và phiên trình diễn đầu-cuối chưa hoàn tất.
>
> Tài liệu này quy định cách một agent trong VS Code hoặc một chat-box tiếp nhận và bàn giao nhiệm vụ QMD. Nó không thay thế chỉ dẫn cấp repository hoặc quy chuẩn chuyên biệt của dự án.

## 1. Mục đích

Một nhiệm vụ phải có thể được tiếp tục trong phiên mới mà không cần toàn bộ lịch sử hội thoại. Để đạt điều đó, thông tin phải được chuyển thành:

- một prompt bàn giao rõ;
- một manifest có cấu trúc;
- một tập tệp đủ dùng và giữ nguyên đường dẫn tương đối;
- một danh sách checksum;
- bằng chứng phân biệt rõ điều đã chạy với điều chỉ được mô tả.

## 2. Nguyên tắc chung

- Nguồn có thẩm quyền phải được ghi tường minh.
- Tệp thiếu không được âm thầm thay bằng kiến thức chung.
- Tài liệu lịch sử không được dùng để ghi đè tài liệu hiện hành.
- Tài liệu chuyên trách chỉ được kích hoạt khi điều kiện áp dụng xuất hiện.
- Agent và chat-box phải dùng cùng thuật ngữ về phạm vi, trạng thái và cổng nghiệm thu.
- Mọi tuyên bố về Git, lệnh, render hoặc kiểm định phải gắn với bằng chứng có thật.
- Gói ngữ cảnh không trao quyền stage, commit hoặc xuất bản.

## 3. Giao thức của agent trong VS Code

### 3.1. Bước 1 — Xác nhận môi trường

Agent phải xác định:

- repository và thư mục làm việc;
- branch hiện tại;
- commit hiện tại;
- trạng thái worktree;
- thay đổi ngoài phạm vi;
- công cụ repository-local cần dùng.

Nếu không thể xác nhận một mục, phải ghi `unknown`; không dùng dữ liệu từ prompt như bằng chứng thay cho lệnh vừa chạy.

### 3.2. Bước 2 — Nạp thẩm quyền

Agent đọc theo thứ tự:

1. yêu cầu hiện tại của người dùng;
2. `AGENTS.md` ở gốc;
3. các `AGENTS.md` trên đường đến phạm vi;
4. tài liệu được các `AGENTS.md` dẫn chiếu;
5. cấu hình dự án trong `_quy_trinh/`;
6. quy chuẩn chuyên biệt được kích hoạt;
7. hồ sơ bài;
8. QMD và đầu ra.

Hai chuỗi cục bộ hiện hành kết thúc tại:

- `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/AGENTS.md`;
- `content/thpt/zo_math_100/100_bai_toan_thuc_te/AGENTS.md`.

Phải giữ ranh giới:

```text
quy_trinh_xay_dung/he_thong_san_xuat_qmd/
    → tài liệu toàn hệ thống

content/.../<du_an>/_quy_trinh/
    → tài liệu và dữ liệu điều khiển riêng của dự án
```

Agent phải lập danh sách:

- nguồn bắt buộc đã đọc;
- nguồn chuyên trách đã kích hoạt;
- nguồn lịch sử chỉ dùng tham khảo;
- nguồn được dẫn chiếu nhưng còn thiếu.

### 3.3. Bước 3 — Khóa nhiệm vụ

Trước khi sửa, agent phải ghi:

- mục tiêu;
- phạm vi tệp;
- tệp không được tác động;
- trạng thái không được thay đổi;
- kiểm định dự kiến;
- điểm cần quyết định của người dùng.

### 3.4. Bước 4 — Thực hiện

- Chỉ dùng tệp trong phạm vi.
- Không chạy lệnh phá hủy hoặc mở rộng phạm vi mà không có căn cứ.
- Không dùng `git add .`.
- Không tự commit.
- Không sửa bài hồi quy để chữa checker.
- Không tự tạo nguồn có thẩm quyền mới trong một nhiệm vụ sản xuất bài.
- Không mặc định ghi gói ZIP, báo cáo phiên hoặc tệp tạm vào gốc repository hay thư mục dự án; phải dùng vị trí đầu ra đã được khóa trong phạm vi.

### 3.5. Bước 5 — Kiểm định và báo cáo

Với bài QMD thuộc hệ thống có cấu hình, agent dùng điểm vào vận hành thống nhất:

```bash
python scripts/zo_python.py scripts/zo_qmd.py check <pham-vi-qmd>...
python scripts/zo_python.py scripts/zo_qmd.py render <pham-vi-qmd>...
```

Không thay lệnh này bằng việc gọi trực tiếp `scripts/zo_check_repo.py`, trừ khi nhiệm vụ hiện tại là bảo trì hoặc chẩn đoán checker và báo cáo đã nêu rõ lí do. Checker lõi vẫn là nơi thực thi validator; CLI vận hành chỉ điều phối, giữ mã thoát và báo cáo.

Agent phải phân biệt:

- lệnh đã chạy;
- kết quả từ công cụ;
- quan sát trực quan;
- suy luận;
- việc chưa thể xác nhận.

Báo cáo kết thúc tối thiểu gồm:

```text
SNAPSHOT
SCOPE
AUTHORITIES
FILES CHANGED
COMMANDS RUN
AUTOMATED RESULT
HUMAN REVIEW
PRODUCTION STATUS
PUBLICATION STATUS
OPEN ISSUES
NEXT GATE
```

## 4. Giao thức của chat-box

### 4.1. Bước 1 — Đọc gói theo thứ tự

Chat-box đọc:

1. `PROMPT.md`;
2. `MANIFEST.yml`;
3. `FILES.sha256`;
4. các tệp bắt buộc trong `payload/`;
5. nguồn chuyên trách theo điều kiện của nhiệm vụ;
6. bằng chứng và đầu ra nếu có.

Không bắt đầu bằng việc đọc ngẫu nhiên toàn bộ ZIP rồi tự suy ra thẩm quyền.

### 4.2. Bước 2 — Kiểm tra tính đủ dùng

Chat-box phải xác định:

- manifest có đúng schema không;
- tệp bắt buộc có đủ không;
- checksum có thể đối chiếu không;
- snapshot là repository sống hay bản xuất;
- trạng thái Git có được xác nhận hay chỉ được khai báo;
- công cụ cần chạy có đủ phụ thuộc không;
- tài liệu dẫn chiếu có bị thiếu không.

Nếu gói không đủ để chạy độc lập, chat-box vẫn có thể khảo sát và đề xuất, nhưng phải gọi đúng tên là **gói đọc hoặc gói khảo sát**, không gọi là gói tái tạo.

### 4.3. Bước 3 — Xác nhận ranh giới

Chat-box phải báo:

- điều được xác nhận trực tiếp từ gói;
- điều chỉ đến từ prompt;
- điều là suy luận;
- điều chưa thể kiểm chứng.

Chat-box không được:

- claim đã kiểm tra worktree sống;
- claim đã render nếu không có log hoặc đầu ra tương ứng;
- điền tệp thiếu bằng một bản giả định;
- thay đổi trạng thái xuất bản trong bản đề xuất;
- dùng lịch sử hội thoại làm nguồn có thẩm quyền cao hơn tài liệu hiện hành.

### 4.4. Bước 4 — Sản phẩm bàn giao

Tùy nhiệm vụ, chat-box bàn giao một trong các dạng:

- bản đồ hiện trạng;
- kiến trúc hoặc kế hoạch;
- bản vá thống nhất;
- các tệp mới có thể tải xuống;
- prompt bàn giao cho agent trong VS Code;
- báo cáo kiểm định dựa trên bằng chứng trong gói.

Mọi tệp tạo ra phải ghi rõ được xây trên snapshot nào.

## 5. Cấu trúc gói chuẩn

```text
<package-root>/
├── PROMPT.md
├── MANIFEST.yml
├── FILES.sha256
└── payload/
    ├── AGENTS.md
    ├── scripts/
    ├── quy_trinh_xay_dung/
    └── content/
```

Nguyên tắc:

- `payload/` giữ nguyên đường dẫn tương đối từ gốc repository;
- không đổi tên tệp để làm gói dễ đọc hơn;
- không chép cùng một tệp vào nhiều vị trí;
- tệp sinh tạm không nằm trong `payload/` trừ khi được khai báo là bằng chứng;
- mọi tệp trong `payload/` phải xuất hiện trong `FILES.sha256`;
- công cụ tạo gói phải yêu cầu đường dẫn đầu ra tường minh;
- vị trí mặc định không được là gốc repository hoặc thư mục dự án;
- nếu đầu ra được đặt trong repository theo yêu cầu riêng, manifest phải khai báo đường dẫn và lí do.

### 5.1. Giao diện O2 hiện hành

Gói ngữ cảnh được tạo qua:

```bash
python scripts/zo_python.py scripts/zo_qmd.py pack \
  --output <thu-muc-hoac-tep.zip> \
  --prompt <tep-markdown> \
  --purpose "<muc-dich>" \
  [--scope-mode <nhan>] \
  [--include <duong-dan>]... \
  [--inside-repository-reason "<li-do>"] \
  [--json] \
  <pham-vi>...
```

Gói được xác minh qua:

```bash
python scripts/zo_python.py scripts/zo_qmd.py verify \
  <thu-muc-hoac-tep.zip> \
  [--json]
```

Hợp đồng O2:

- `--output`, `--prompt`, `--purpose` và ít nhất một phạm vi là bắt buộc;
- `pack` không ghi đè đầu ra đã tồn tại;
- đầu ra trong repository bị từ chối nếu thiếu `--inside-repository-reason`;
- `pack` mặc định tạo `package.kind: context`; mã ứng viên O3 cho phép `release` khi hồ sơ và các cổng bắt buộc đạt;
- `verify` có thể chạy ngoài repository Git bằng CLI nằm trong `payload/`;
- chế độ `--json` chỉ xuất JSON trên stdout;
- trình khởi chạy `zo_python.py` đặt `PYTHONDONTWRITEBYTECODE=1` để việc chạy mã không sinh `__pycache__` hoặc `.pyc` trong gói.

## 6. `PROMPT.md`

Prompt bàn giao phải ngắn hơn tài liệu hệ thống và gồm:

1. repository, branch và commit khai báo;
2. mục tiêu phiên;
3. trạng thái đã chốt;
4. phạm vi được phép tác động;
5. điều cấm;
6. tệp bắt buộc cần đọc;
7. sản phẩm đầu ra;
8. tiêu chí nghiệm thu;
9. nhiệm vụ đầu tiên.

Prompt không được:

- sao chép toàn bộ quy chuẩn;
- mô tả một chức năng chưa có như đã hoạt động;
- thay manifest;
- dùng lịch sử chat làm bằng chứng chính.

## 7. Schema `MANIFEST.yml` phiên bản 1

Mẫu có thể sao chép nằm tại `mau_manifest_goi_qmd.yml`. Khung chuẩn:

```yaml
manifest_version: 1

package:
  id: qmd-context-YYYYMMDD-HHMMSS
  kind: context
  purpose: "Mô tả ngắn mục đích gói"
  created_at: "YYYY-MM-DDTHH:MM:SS+07:00"
  created_by: human-or-tool

system:
  qmd_core_version: "1.0"
  checker_version: "2.6.0"
  project_config_schema: 1
  operations_contract_version: "0.2"
  manifest_schema: 1

repository:
  name: zo_math
  source: exported_snapshot
  branch: master
  commit: full-40-character-sha
  dirty: unknown
  ahead_of_origin: unknown

scope:
  mode: documentation
  roots:
    - quy_trinh_xay_dung/he_thong_san_xuat_qmd
  excluded:
    - docs
    - changes-outside-scope

output:
  path: unknown
  inside_repository: false
  reason: null

entrypoints:
  current:
    checker: scripts/zo_check_repo.py
    operations_cli: scripts/zo_qmd.py
  target: {}

sources:
  required:
    - path: AGENTS.md
      role: repository_instructions
    - path: quy_trinh_xay_dung/he_thong_san_xuat_qmd/README.md
      role: system_entry
  conditional: []
  historical: []

evidence:
  commands: []
  reports: []
  outputs: []

integrity:
  algorithm: sha256
  file: FILES.sha256

limitations:
  - "Không chứa .git; không xác nhận được worktree sống."
```

### 7.1. Trường bắt buộc

- `manifest_version`;
- `package.id`, `package.kind`, `package.purpose`, `package.created_at`;
- toàn bộ nhóm `system`;
- `repository.source`, `repository.branch`, `repository.commit`, `repository.dirty`;
- `scope.roots` và `scope.excluded`;
- `output.path`, `output.inside_repository`;
- `sources.required`;
- `integrity.algorithm` và `integrity.file`;
- `limitations`.

### 7.2. Giá trị `package.kind`

Phiên bản 1 cho phép:

```text
context
release
```

- `context`: bàn giao một nhiệm vụ hoặc snapshot để khảo sát.
- `release`: đóng băng một release candidate của lớp vận hành đã qua điều kiện phát hành và rollback drill. Gói context không được đổi `kind` bằng cách sửa tay manifest rồi gọi là release.

### 7.3. Giá trị `repository.source`

```text
live_repository
exported_snapshot
```

Nếu là `exported_snapshot`, manifest không được ngầm coi `dirty`, `ahead_of_origin` hoặc trạng thái index là đã kiểm chứng, trừ khi gói chứa bằng chứng Git được tạo tại thời điểm đóng gói.

### 7.4. Kiểu dữ liệu trạng thái repository

- `repository.commit`: SHA đầy đủ 40 kí tự hoặc `unknown`;
- `repository.dirty`: `true`, `false` hoặc `unknown`;
- `repository.ahead_of_origin`: số nguyên không âm hoặc `unknown`;
- các giá trị lấy từ prompt nhưng chưa có bằng chứng Git phải được ghi là `unknown` trong manifest, rồi mô tả riêng trong `limitations`.

### 7.5. Nguồn có thẩm quyền

Mỗi mục trong `sources` có:

```yaml
- path: path/inside/payload
  role: stable_identifier
  condition: optional-human-readable-condition
```

Ba nhóm:

- `required`: luôn phải đọc;
- `conditional`: chỉ đọc khi điều kiện áp dụng xuất hiện;
- `historical`: bằng chứng lịch sử, không ghi đè nguồn hiện hành.


### 7.6. Giao diện tạo gói của O3

O3 giữ một lệnh `pack` và khóa hai tham số:

```text
--kind context|release
--release-file <duong_dan_yaml>
```

`context` là mặc định tương thích ngược. `--release-file` chỉ hợp lệ và bắt buộc khi `--kind release`. Hồ sơ phát hành tuân theo `mau_ho_so_phat_hanh_qmd.yml`.

Giao diện này đã được triển khai, kiểm nghiệm và dùng để tạo release candidate `0.3.0`. Hồi quy, hai phép xác minh và rollback drill đều đã đạt; vì vậy `0.3.0` là release hiện hành, dù Git tag thật chưa được tạo.

### 7.7. Giao diện lập hồ sơ phiên và báo cáo trước xuất bản của O4

CLI ứng viên `0.4.0` bổ sung hai lệnh tương thích ngược:

```text
start --output <session.json> (--request <text> | --request-file <file>) [--allow <path>] [--exclude <path>] <target>
prepublish --output <report.json> --session <session.json> --check-report <check.json> --render-report <render.json> --human-review <review.json> <target>
```

`start` phải ghi đầu ra tường minh ngoài repository hoặc dưới `_audit/`, giữ nguyên yêu cầu ban đầu, kết quả `inspect`, nguồn có thẩm quyền, phạm vi được phép tác động, phạm vi loại trừ, kế hoạch và các cổng người dùng. Phạm vi được phép và phạm vi loại trừ không được chồng lấn. Với một QMD dự kiến tạo mới, hồ sơ bài có thể chưa tồn tại nhưng phải được ghi là sản phẩm cần tạo; với QMD đã tồn tại, hồ sơ bắt buộc bị thiếu phải chặn kế hoạch.

`prepublish` chỉ tổng hợp manifest phiên, báo cáo `check`, báo cáo `render` và bảng kiểm có người quan sát. Lệnh không chạy lại checker, không sửa hồ sơ sản xuất và không tự đặt `accepted`; báo cáo chỉ phản ánh `production_status: accepted` khi bảng kiểm hợp lệ đã ghi nhận trạng thái ấy. Lệnh không chuyển sang `published` và luôn ghi `publication: pending`. Báo cáo chỉ ở trạng thái `ready_for_user_decision` khi bằng chứng tự động cùng kiểm định có người quan sát đều đạt; mọi trường hợp thiếu hoặc mâu thuẫn phải bị chặn.

Hai lệnh này chưa tự chứng minh O4 hoàn tất. Gói context từ trạng thái O4, phép thử chat-box mới và phiên trình diễn đầu-cuối vẫn là bằng chứng bắt buộc.

## 8. `FILES.sha256`

Định dạng:

```text
<sha256><hai khoảng trắng>payload/<duong_dan_tuong_doi>
```

Ví dụ:

```text
0123456789abcdef...  payload/AGENTS.md
```

Quy tắc:

- dùng SHA-256;
- sắp xếp theo đường dẫn;
- chứa `PROMPT.md`, `MANIFEST.yml` và toàn bộ tệp trong `payload/`;
- không chứa chính `FILES.sha256` vì tệp không thể tự băm ổn định;
- `verify` phải báo tệp thiếu, tệp thừa và checksum sai;
- gói release không được phát hành khi có sai lệch.

## 9. Chọn tệp cho gói ngữ cảnh

### 9.1. Lõi bắt buộc

Tùy nhiệm vụ, tối thiểu gồm:

- `AGENTS.md` cấp gốc;
- hai tài liệu bắt buộc mà `AGENTS.md` dẫn chiếu;
- README hệ thống QMD;
- tài liệu kiến trúc và hợp đồng liên quan;
- script điểm vào và mọi phụ thuộc import cần thiết nếu gói tuyên bố có thể chạy;
- cấu hình dự án;
- `AGENTS.md` cục bộ;
- hồ sơ và QMD trong phạm vi.

### 9.2. Nguồn chuyên trách theo điều kiện

Chỉ thêm khi nhiệm vụ kích hoạt, ví dụ:

- quy chuẩn khảo sát hàm số;
- quy chuẩn kĩ thuật bài hàm số;
- quy chuẩn đồ thị TikZ/PGFPlots;
- hướng dẫn khối nội dung;
- phong cách viết đã được chỉ định;
- dữ liệu danh mục;
- tài nguyên hình liên quan.

### 9.3. Bằng chứng

Khi gói dùng để kiểm định hoặc bàn giao kết quả, thêm:

- báo cáo JSON;
- log lệnh;
- HTML/PDF/SVG cần quan sát;
- ảnh chụp khi có giá trị;
- diff hoặc patch;
- kết quả Git cần xác nhận.

Bằng chứng phải được ghi trong manifest; không trộn với nguồn điều khiển.

### 9.4. Loại trừ

Mặc định loại trừ:

- `.git/`;
- cache;
- tệp tạm;
- build ngoài phạm vi;
- bí mật và thông tin máy cá nhân;
- thay đổi ngoài phạm vi;
- tệp lịch sử không cần thiết cho nhiệm vụ;
- các ZIP, báo cáo và tệp thử đã nằm ở gốc repository nhưng không thuộc phạm vi.

Việc một tệp đang tồn tại trong worktree không làm nó trở thành thành phần của gói.

## 10. Gói phát hành

### 10.1. Điều kiện nguồn

Release candidate phải được tạo từ repository Git và commit xác định, với worktree phát hành sạch và đầu ra ngoài repository. Nếu worktree bẩn, công cụ phải dừng; việc ghi sai lệch trong prompt hoặc limitation không biến một snapshot bẩn thành release candidate.

Gói release phải ghi:

```yaml
repository:
  source: exported_snapshot
  commit: full-40-character-sha
  dirty: false
```

### 10.2. Thành phần bắt buộc trong payload

Ngoài cấu trúc chung, gói release phải có trong `payload/`:

- mã CLI vận hành và mô-đun đóng gói;
- checker cùng toàn bộ phụ thuộc runtime cần thiết;
- tài liệu hiện hành của lõi và lớp vận hành;
- schema manifest và mẫu hồ sơ phát hành;
- đường cơ sở hồi quy hai dự án;
- ma trận phiên bản;
- changelog;
- release checklist;
- hướng dẫn nâng cấp và khôi phục;
- rollback log;
- hồi quy trước và sau;
- bằng chứng kiểm tra release candidate.

Các đường dẫn bằng chứng được khai báo trong hồ sơ `--release-file`; công cụ không được suy đoán bằng tên gần giống.

### 10.3. Nhóm `release` trong manifest

Manifest release phải thêm:

```yaml
release:
  stage: candidate
  version: "X.Y.Z"
  tag: qmd-ops-vX.Y.Z
  tag_created: false
  previous_version: "X.Y.Z"
  previous_commit: full-40-character-sha
  candidate_commit: full-40-character-sha
  regression_status: pass
  rollback_tested: true
change:
  semver: minor
  classifications:
    - operations_contract
    - cli
    - package_module
  migration_required: false
  migration_summary: "Mô tả đường di trú hoặc lí do không cần di trú."
```

Quy tắc:

- `version` và `previous_version` theo `MAJOR.MINOR.PATCH`;
- `tag` phải khớp chính xác `qmd-ops-v<version>`;
- `tag_created` phải là `false` trong O3;
- `previous_commit` và `candidate_commit` là SHA đầy đủ 40 kí tự;
- `candidate_commit` phải khớp `repository.commit`;
- `regression_status` chỉ chấp nhận `pass`;
- `rollback_tested` chỉ chấp nhận `true`;
- mọi trường phải có đúng kiểu dữ liệu, không chỉ tồn tại theo tên;
- nhóm `change` phải khớp mức tăng phiên bản và có phân loại thay đổi hợp lệ.

### 10.4. Hồ sơ phát hành đầu vào

`mau_ho_so_phat_hanh_qmd.yml` định nghĩa hồ sơ máy đọc được cho `--release-file`. Hồ sơ phải ghi danh tính release trước, phân loại thay đổi, quyết định SemVer và đường dẫn từng bằng chứng. Hồ sơ không ghi `candidate_commit`; công cụ phải lấy SHA của `HEAD` từ worktree sạch rồi ghi vào manifest để tránh tự tham chiếu tới commit chứa chính hồ sơ.

Tệp mẫu có thể dùng `pending`, `false` hoặc `unknown` để ngăn việc claim sớm. `pack --kind release` phải từ chối các giá trị ấy; chỉ hồ sơ đã được cập nhật bằng bằng chứng thật mới đủ điều kiện tạo release candidate.

### 10.5. Mức đầy đủ

Gói release phải đạt mức **đủ để tái tạo**. Gói chỉ đủ để đọc hoặc đủ để chạy không được gọi là release candidate.

## 11. Quy tắc xác minh

Một gói được gọi là **đủ để đọc** khi:

- có prompt, manifest và checksum;
- mọi nguồn bắt buộc cho việc hiểu nhiệm vụ có mặt;
- hạn chế được ghi rõ.

Một gói được gọi là **đủ để chạy** khi:

- mọi import và script phụ thuộc có mặt;
- công cụ ngoài repository được khai báo;
- đường dẫn tương đối còn hợp lệ;
- lệnh kiểm tra khởi động được trong thư mục sạch.

Một gói được gọi là **đủ để tái tạo** khi:

- đủ để chạy;
- snapshot, phiên bản và đầu ra mong đợi được khóa;
- cùng một gói cho kết quả kiểm tra tương đương trong môi trường được hỗ trợ.

Không được dùng ba mức này thay thế cho nhau.

## 12. Báo cáo thiếu gói

Khi gói thiếu, báo theo mẫu:

```text
MISSING REQUIRED FILES
MISSING RUNTIME DEPENDENCIES
UNVERIFIED REPOSITORY STATE
BROKEN REFERENCES
SAFE WORK STILL POSSIBLE
WORK THAT MUST STOP
```

Chat-box có thể tiếp tục phân tích tài liệu khi an toàn, nhưng phải dừng mọi kết luận phụ thuộc vào tệp hoặc bằng chứng bị thiếu.

## 13. Bàn giao ngược về repository

Chat-box không sửa repository sống. Khi không có kết nối trực tiếp, người dùng có thể đóng vai trò **người vận hành trung gian**: nhận đúng một lệnh hoặc một nhóm lệnh có kiểm soát, chạy trong repository, rồi chuyển nguyên kết quả trở lại. Chat-box phải luôn phân biệt repository thật với bản sao trong môi trường của mình và không tuyên bố đã sửa repository trước khi có bằng chứng từ người vận hành.

Sản phẩm trả lại phải gồm:

- snapshot nguồn;
- danh sách tệp mới hoặc sửa;
- patch hoặc gói tệp;
- kiểm tra đã thực hiện trên bản sao;
- kiểm tra cần agent chạy lại trong repository sống;
- tệp ngoài phạm vi phải được giữ nguyên;
- không kèm lệnh `git add .`.

Khi cần người vận hành trung gian thực thi, chỉ dẫn phải nêu rõ: thư mục chạy, lệnh duy nhất hoặc nhóm lệnh cùng mục đích, điều lệnh được phép làm, và kết quả cần gửi lại. Không gộp thao tác đọc, sửa, staging và commit trong cùng một bước.

## 14. Kết luận

Giao thức này biến việc “gửi một ZIP và một prompt” thành một hợp đồng có thể kiểm tra. Manifest nói gói là gì; checksum nói gói có toàn vẹn không; payload giữ ngữ cảnh đường dẫn; prompt nói nhiệm vụ hiện tại; agent và chat-box cùng dùng một cách báo cáo.
