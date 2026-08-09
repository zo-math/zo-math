# Ma trận phiên bản của cỗ máy QMD

> **Trạng thái:** Release/tag hiện hành là `0.5.0`. Candidate đang nghiệm thu là `0.6.0`: CLI `0.6.0`, contract `0.6`, package module `0.5.0`, checker `2.7.0`. Chưa tag, push, tạo release package hoặc publish `0.6.0`.
>
> Tài liệu này ghi quan hệ giữa các phiên bản được quản lí độc lập. Nó không thay thế hằng số phiên bản trong mã đang chạy và không tự tạo release hoặc Git tag.

## 1. Mục đích

Cỗ máy QMD gồm nhiều thành phần có vòng đời khác nhau. Một thay đổi ở lớp vận hành không tự động làm thay đổi lõi QMD, checker hoặc schema cấu hình dự án. Ma trận này dùng để:

- xác định phiên bản hiện hành của từng thành phần;
- xác định phiên bản đích của một release candidate;
- giải thích vì sao một thành phần được nâng phiên bản còn thành phần khác được giữ nguyên;
- khóa điểm quay lại cho diễn tập khôi phục;
- ngăn việc dùng một số phiên bản chung cho những hợp đồng độc lập.

## 2. Nguồn sự thật

- Phiên bản đang chạy của CLI, mô-đun đóng gói và checker được lấy từ hằng số trong mã tương ứng.
- Phiên bản schema được lấy từ hợp đồng schema hiện hành và mã nạp hoặc xác minh schema.
- Tài liệu này là hồ sơ phối hợp phát hành: tại thời điểm tạo release candidate, các giá trị của nó phải khớp mã, manifest, changelog và bằng chứng kiểm nghiệm.
- Khi mã và ma trận khác nhau, không được tự chọn một phía rồi tiếp tục phát hành; phải dừng và xử lí sai lệch.

## 3. Ma trận các release `0.3.0`, `0.4.0`, `0.5.0` và candidate `0.6.0`

Release trước được khóa tại:

```text
version: 0.2.0
commit: c1b26b9a0536b17e0885d8158fddbd20413767c2
```

| Thành phần | Release trước `0.2.0` | Release O3 `0.3.0` | Quyết định |
|---|---:|---:|---|
| Lõi kĩ thuật QMD | `1.0` | `1.0` | Giữ nguyên |
| Checker | `2.6.0` | `2.6.0` | Giữ nguyên |
| Schema cấu hình dự án | `1` | `1` | Giữ nguyên |
| Schema manifest | `1` | `1` | Giữ nguyên |
| Schema hồ sơ phát hành | Chưa có | `1` | Thêm mới |
| Hợp đồng lớp vận hành | `0.2` | `0.3` | Nâng `MINOR` |
| `scripts/zo_qmd.py` | `0.2.0` | `0.3.0` | Nâng `MINOR` |
| `scripts/zo_qmd_package.py` | `0.2.0` | `0.3.0` | Nâng `MINOR` |

Release `0.3.0` bổ sung khả năng tạo và xác minh release candidate nhưng giữ tương thích ngược với gói context và giao diện đã có ở O2. Vì vậy, mức thay đổi đúng là `MINOR`, không phải `MAJOR`.

### 3.1. Ma trận release `0.4.0` tại mốc O4

| Thành phần | Release trước `0.3.0` | Release O4 `0.4.0` | Quyết định |
|---|---:|---:|---|
| Lõi kĩ thuật QMD | `1.0` | `1.0` | Giữ nguyên |
| Checker | `2.6.0` | `2.6.0` | Giữ nguyên |
| Schema cấu hình dự án | `1` | `1` | Giữ nguyên |
| Schema manifest gói | `1` | `1` | Giữ nguyên |
| Schema hồ sơ phát hành | `1` | `1` | Giữ nguyên |
| Hợp đồng lớp vận hành | `0.3` | `0.4` | Nâng `MINOR` |
| Schema manifest phiên `start` | Chưa có | `1` | Thêm mới |
| Schema báo cáo `prepublish` | Chưa có | `1` | Thêm mới |
| `scripts/zo_qmd.py` | `0.3.0` | `0.4.0` | Nâng `MINOR` |
| `scripts/zo_qmd_package.py` | `0.3.0` | `0.3.1` | Nâng `PATCH`; tách phiên bản release khỏi phiên bản mô-đun |
| `scripts/zo_qmd_prepublish.py` | Chưa có | report version `1` | Thêm mới |

Release `0.4.0` bổ sung hai khả năng tương thích ngược: `start` lập manifest phiên và khóa kế hoạch; `prepublish` tổng hợp bằng chứng trước xuất bản. Hai commit triển khai ban đầu là `278b1d9` và `c966bcb`. Checker, lõi QMD, mô-đun đóng gói và các schema đã có không thay đổi.

`0.4.0` là release hiện hành sau khi người dùng chấp thuận release candidate tại commit `6425dec241cc27cad76bf55f8385531e56fb1a86`. Package ID là `qmd-release-0-4-0-20260804-142216`; chưa tạo Git tag thật, chưa push hoặc publish.

Mốc nghiệm thu **lớp vận hành `1.0`** ghi mức trưởng thành của toàn hệ thống vận hành. Nó không thay thế phiên bản hợp đồng máy đọc được `0.4`, vốn phải khớp `MAJOR.MINOR` của release `0.4.0`.

### 3.2. Ma trận release hiện hành `0.5.0`

| Thành phần | Release trước `0.4.0` | Release hiện hành `0.5.0` | Quyết định |
|---|---:|---:|---|
| Lõi kĩ thuật QMD | `1.0` | `1.0` | Giữ nguyên |
| Checker | `2.6.0` | `2.6.0` | Giữ nguyên |
| Schema cấu hình dự án | `1` | `1` | Giữ nguyên; khóa mới tương thích ngược |
| Schema manifest gói | `1` | `1` | Giữ nguyên |
| Schema manifest phiên `start` | `1` | `1` | Giữ nguyên |
| Hợp đồng lớp vận hành | `0.4` | `0.5` | Nâng `MINOR` |
| `scripts/zo_qmd.py` | `0.4.0` | `0.5.0` | Nâng `MINOR` |
| `scripts/zo_qmd_package.py` | `0.3.1` | `0.4.0` | Nâng `MINOR` |

Release `0.5.0` bổ sung khả năng tương thích ngược
`references.quality_exemplars`: loader chuẩn hóa khóa vắng mặt thành danh sách
rỗng; `inspect`, `doctor`, `start` và context package cùng nhận diện bài chuẩn;
giao thức agent quy định cách đọc hoặc quan sát chúng. Checker, lõi QMD và các
schema giữ nguyên vì thay đổi không tác động validator và cấu trúc phiên bản 1
vẫn biểu diễn đầy đủ hợp đồng mới.

Tại thời điểm push tag, nhánh `master` và `origin/master` đã được xác minh
đồng bộ tại commit `5c1dddaae51c4e76f72628c8206d54d9ff7e1aff`. Annotated tag
`qmd-ops-v0.5.0` đã được push lên origin; tag object là
`7d45d37ae0ccf6e4933d3342dfc5de6f9c3abd4a` và trỏ đến product commit
`ba85e35db84e092fbb2c1786ceb9fff707dfc438`, không trỏ đến `master` hiện
tại. Release chính thức chưa được tạo hoặc công bố; website chưa được publish.

### 3.3. Ma trận candidate `0.6.0`

| Thành phần | Release/tag hiện hành `0.5.0` | Candidate `0.6.0` | Quyết định |
|---|---:|---:|---|
| Lõi kĩ thuật QMD | `1.0` | `1.0` | Giữ nguyên |
| Checker | `2.6.0` | `2.7.0` | Nâng vì giao diện evidence quan sát được thay đổi |
| Schema cấu hình dự án | `1` | `1` | Giữ nguyên |
| Schema manifest gói | `1` | `1` | Giữ nguyên |
| Schema manifest phiên `start` | `1` | `2` | Giữ identity/session contract đã triển khai |
| Schema evidence checker | Chưa có | `1` | Ghi evidence có identity máy đọc được |
| Schema human review | `1` | `2` | Khóa observation và final human acceptance |
| Schema báo cáo `prepublish` | `1` | `2` | Khóa chuỗi nghiệm thu ba lớp |
| Hợp đồng lớp vận hành | `0.5` | `0.6` | Nâng `MINOR` |
| `scripts/zo_qmd.py` | `0.5.0` | `0.6.0` | Nâng `MINOR` |
| `scripts/zo_qmd_package.py` | `0.4.0` | `0.5.0` | Nâng `MINOR` tương thích ngược |

Candidate `0.6.0` bổ sung authority acknowledgement, provenance gate, evidence
identity/freshness, chuỗi nghiệm thu ba lớp và repository hygiene. Candidate
chưa được tag, push, tạo release package hoặc publish.

## 4. Danh tính release candidate O3

Danh tính đích được khóa như sau:

```yaml
release:
  stage: candidate
  version: "0.3.0"
  tag: qmd-ops-v0.3.0
  tag_created: false
  previous_version: "0.2.0"
  previous_commit: c1b26b9a0536b17e0885d8158fddbd20413767c2
```

`tag` là tên dự kiến để nhận diện release. `tag_created: false` là bắt buộc trong O3 vì phiên này không được tạo tag thật nếu chưa có xác nhận riêng của người dùng.

Commit ứng viên không được ghi cứng trong hồ sơ theo dõi bằng Git vì sẽ tạo quan hệ tự tham chiếu. Khi đóng gói, công cụ phải lấy SHA của `HEAD` từ worktree sạch và ghi SHA ấy vào `repository.commit` cùng `release.candidate_commit` trong manifest. Không dùng commit chứa thay đổi ngoài phạm vi hoặc worktree bẩn làm danh tính release candidate.

## 5. Bất biến tại điểm quay lại

Hai QMD hồi quy tại commit `c1b26b9a0536b17e0885d8158fddbd20413767c2` có SHA-256:

```text
5388b6e76806ae24cbe8dd36607729146cdb55e05fce4e38d9cdf9672dae17ce  content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd
d20163265f730bb5c0648c15791fc631a1fdd6c803c45c116608ac0c1c26edb3  content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd
```

Hồ sơ của cả hai dự án phải tiếp tục phản ánh trạng thái xuất bản `pending`. Rollback drill O3 phải đối chiếu lại các giá trị này ở worktree previous và candidate.

## 6. Quy tắc tăng phiên bản

### 6.1. Lớp vận hành

Dùng `MAJOR.MINOR.PATCH`:

- `MAJOR`: thay đổi không tương thích về CLI, manifest hoặc giao thức vận hành;
- `MINOR`: thêm khả năng tương thích ngược;
- `PATCH`: sửa lỗi hoặc làm rõ không phá hợp đồng quan sát được.

### 6.2. Checker

Chỉ nâng `CHECKER_VERSION` khi hành vi kiểm định quan sát được thay đổi. Không nâng checker chỉ vì thêm tài liệu phát hành, lớp điều phối hoặc khả năng đóng gói release.

### 6.3. Schema

Chỉ nâng schema khi cấu trúc cũ không còn đủ để biểu diễn hợp đồng mới hoặc khi có thay đổi không tương thích. `package.kind: release` và nhóm `release` đã thuộc schema manifest phiên bản `1`, nên O3 không nâng schema manifest.

### 6.4. Lõi QMD

Không nâng lõi QMD khi thay đổi chỉ thuộc lớp vận hành. Hai bài hồi quy phải tiếp tục chạy trên lõi `1.0` mà không bị sửa để thích nghi.

## 7. Điều kiện có hiệu lực của release O3

Trong O3, đích `0.3.0` chỉ trở thành phiên bản hiện hành khi đồng thời:

1. mã CLI và mô-đun đóng gói đã ghi `0.3.0`;
2. self-test bắt buộc đạt;
3. hồi quy nguồn và render hai dự án đạt;
4. release candidate được tạo từ commit sạch;
5. gói release được `verify` trong thư mục sạch;
6. rollback drill đạt;
7. changelog, checklist và rollback log phản ánh đúng bằng chứng;
8. tài liệu hiện hành không còn mô tả O3 như chức năng chưa triển khai.

Tám điều kiện trên đã đạt. Vì vậy, `0.3.0` đã trở thành release hiện hành tại thời điểm hoàn tất O3. Release candidate được tạo từ commit `99a7c04c69eb0a54d381f5afd0d3e79fe26e9cab`, có package ID `qmd-release-0-3-0-20260802-223550` và được xác minh bằng hai đường độc lập. Release này sau đó được thay thế bởi `0.4.0`; Git tag thật cho `0.3.0` không được tạo.
