# Quy trình phát hành và khôi phục lớp vận hành QMD

> **Trạng thái:** Release hiện hành của lớp vận hành là `0.3.0`. Release candidate O4 `0.4.0` tại commit `6425dec241cc27cad76bf55f8385531e56fb1a86` đã được tạo và xác minh bằng hai đường độc lập; package ID `qmd-release-0-4-0-20260804-142216`. Chưa tạo Git tag thật, chưa push hoặc publish; việc khóa lớp vận hành `1.0` còn chờ quyết định riêng của người dùng.
>
> Quy trình này chỉ điều hành lớp vận hành QMD. Nó không tự stage, commit, tag, push, publish hoặc thay đổi trạng thái bài.

## 1. Mục đích

Quy trình này xác định một đường phát hành có thể kiểm tra và một đường khôi phục không phá hủy worktree sống. Mục tiêu của O3 là tạo một **release candidate** có thể xác minh và diễn tập quay lại release trước, không phải xuất bản website hay khóa lớp vận hành `1.0`.

## 2. Thuật ngữ

- **Phiên bản hiện hành:** phiên bản đã có mã và bằng chứng kiểm nghiệm được khóa tại một commit biết trước.
- **Phiên bản đích:** phiên bản đang được chuẩn bị; chưa có hiệu lực chỉ vì đã xuất hiện trong tài liệu.
- **Release candidate:** gói `package.kind: release` được tạo từ commit sạch, đã đủ bằng chứng phát hành và có thể `verify` trong thư mục sạch.
- **Release trước:** phiên bản và commit được dùng làm điểm quay lại.
- **Rollback drill:** diễn tập tái lập release trước trong worktree hoặc nhánh riêng mà không sửa hoặc reset worktree sống.
- **Tag dự kiến:** tên nhận diện được ghi trong hồ sơ; không đồng nghĩa Git tag đã tồn tại.

## 3. Ranh giới an toàn

O3 không được:

- dùng `git reset --hard`, `git clean`, `git checkout -- .` hoặc thao tác phá hủy tương đương trên worktree sống;
- sửa hai bài hồi quy để làm release candidate đạt;
- đổi `publication: pending` thành `published`;
- tạo tag, push hoặc publish khi chưa có yêu cầu riêng;
- tạo release candidate từ worktree bẩn;
- gọi context package là release package;
- lưu ZIP hoặc tệp tạm ở gốc repository theo mặc định.

Nếu worktree sống chứa thay đổi ngoài phạm vi, phần build và rollback phải dùng worktree tách biệt ở vị trí ngoài repository.

## 4. Giao diện CLI đích của O3

Điểm vào vẫn là:

```bash
python scripts/zo_python.py scripts/zo_qmd.py pack ...
```

Giao diện được khóa:

```text
--kind context|release
--release-file <duong_dan_yaml>
```

Quy tắc:

- `--kind` mặc định là `context` để giữ tương thích với O2;
- `--release-file` chỉ hợp lệ và bắt buộc khi `--kind release`;
- không tạo lệnh `release` riêng;
- `verify` tiếp tục dùng chung cho gói context và release;
- mọi đầu ra vẫn phải được khai báo tường minh.

Giao diện trên đã có trong release `0.3.0`. Nó không tự tạo bằng chứng hồi quy, không tự đổi hồ sơ từ `pending` sang `pass` và không tự tuyên bố rollback đã đạt; các bằng chứng O3 đã được tạo riêng và lưu trong hồ sơ phát hành.

## 5. Hồ sơ phát hành

Tệp `mau_ho_so_phat_hanh_qmd.yml` là mẫu cho `--release-file`. Hồ sơ có bốn nhóm:

1. `release_record_version` — phiên bản schema của chính hồ sơ phát hành;
2. `release` — danh tính ứng viên và điểm quay lại;
3. `change` — phân loại thay đổi và quyết định SemVer;
4. `evidence` — đường dẫn đến các bằng chứng bắt buộc.

Mọi đường dẫn bằng chứng phải là đường dẫn tương đối an toàn trong repository và phải trỏ đến tệp có thật tại commit ứng viên. Hồ sơ không chứa `candidate_commit`; công cụ lấy SHA của `HEAD` từ worktree sạch khi tạo manifest.

Tối thiểu phải có:

- ma trận phiên bản;
- changelog;
- release checklist;
- rollback log;
- hồi quy trước;
- hồi quy sau;
- hướng dẫn nâng cấp và khôi phục.

`regression_status` chỉ được là `pass` khi cả hồi quy nguồn và render của hai dự án đạt. `rollback_tested` chỉ được là `true` sau khi rollback drill thực sự hoàn tất.

## 6. Điều kiện tạo release candidate

`pack --kind release` phải từ chối khi có một trong các điều kiện sau:

- không xác định được repository Git hoặc commit hiện tại;
- worktree phát hành không sạch;
- hồ sơ phát hành thiếu trường hoặc sai kiểu dữ liệu;
- phiên bản không theo `MAJOR.MINOR.PATCH`;
- tag không bằng `qmd-ops-v<version>`;
- `previous_commit` không phải SHA đầy đủ 40 kí tự;
- `regression_status` khác `pass`;
- `rollback_tested` khác `true`;
- `tag_created` là `true` trong O3;
- thiếu bất kì tệp bằng chứng bắt buộc nào;
- thiếu mã CLI, checker, phụ thuộc runtime, tài liệu hiện hành hoặc đường cơ sở hồi quy;
- đầu ra đã tồn tại, nằm trong repository hoặc không được khai báo tường minh.

Gói release phải ghi `repository.dirty: false` dựa trên bằng chứng Git tại thời điểm đóng gói. Không dùng `unknown` cho trạng thái sạch của release candidate.

## 7. Chuỗi phát hành chuẩn

### 7.1. Khóa điểm bắt đầu

Ghi:

- branch và commit hiện tại;
- trạng thái worktree;
- phiên bản hiện hành;
- SHA-256 của hai QMD hồi quy;
- trạng thái `publication` của hai dự án.

### 7.2. Phân loại thay đổi

Gắn ít nhất một loại:

- tài liệu vận hành;
- CLI;
- checker;
- loader hoặc registry;
- schema cấu hình;
- schema manifest;
- adapter dự án;
- đầu ra render;
- đường hồi quy.

Từ phân loại đó, ghi mức SemVer và lí do vào ma trận phiên bản cùng changelog.

### 7.3. Kiểm tra trước thay đổi

Chạy hồi quy tại release trước hoặc commit nền bằng worktree sạch:

```bash
python scripts/zo_python.py scripts/zo_qmd.py regression --render
```

Lưu log làm `regression_before`.

### 7.4. Triển khai và commit ứng viên

Mã và tài liệu O3 được kiểm tra, xem diff và commit thành các nhóm độc lập. Không tạo release candidate từ thay đổi chưa commit.

### 7.5. Kiểm tra ứng viên

Tại commit ứng viên sạch:

```bash
python scripts/zo_python.py scripts/zo_qmd.py regression --render
```

Lưu log làm `regression_after`. Xác nhận lại SHA-256 của hai QMD và trạng thái `pending`.

### 7.6. Diễn tập khôi phục

Tạo hai worktree tạm bên ngoài repository sống:

```bash
git worktree add --detach <thu_muc_previous> <previous_commit>
git worktree add --detach <thu_muc_candidate> <candidate_commit>
```

Trong từng worktree, chạy hồi quy bắt buộc và kiểm tra bất biến. Không chép thay đổi từ worktree ứng viên vào worktree previous để “sửa cho đạt”.

Sau khi đã lưu bằng chứng:

```bash
git worktree remove <thu_muc_previous>
git worktree remove <thu_muc_candidate>
```

Chỉ xóa worktree tạm do chính diễn tập tạo. Không dùng `--force` nếu chưa xác nhận worktree sạch.

### 7.7. Tạo và xác minh release candidate

Sau khi hồ sơ ghi `regression_status: pass` và `rollback_tested: true`, tạo gói release tại đầu ra ngoài repository. Sau đó mở gói trong thư mục sạch và chạy:

```bash
python scripts/zo_python.py scripts/zo_qmd.py verify <release_candidate>
```

Release candidate chỉ đạt khi manifest, checksum, payload và bằng chứng đều đạt.

### 7.8. Kết thúc O3 — đã hoàn tất

- Release candidate được tạo ngoài repository với tên `qmd-ops-v0.3.0-rc.zip`; package ID, candidate commit và SHA-256 được khóa trong hồ sơ `phat_hanh/qmd_ops_0_3_0/release_verification.md`.
- Phiên bản là `0.3.0`; tag dự kiến là `qmd-ops-v0.3.0`.
- Candidate commit là `99a7c04c69eb0a54d381f5afd0d3e79fe26e9cab`.
- Package ID là `qmd-release-0-3-0-20260802-223550`.
- Hai phép `verify` đều đạt với mã thoát `0`.
- Tag thật chưa được tạo; không push và không publish.
- Hai bài hồi quy không đổi; trạng thái xuất bản vẫn `pending`.

## 8. Cấu trúc hồ sơ theo phiên bản

Bằng chứng chính thức được theo dõi trong Git tại:

```text
quy_trinh_xay_dung/he_thong_san_xuat_qmd/phat_hanh/
  qmd_ops_<MAJOR>_<MINOR>_<PATCH>/
    ho_so_release_candidate.yml
    release_checklist.md
    rollback_log.md
    regression_before.txt
    regression_after.txt
    release_verification.md
    release_verify_external.txt
    release_verify_self.txt
```

Đây là hồ sơ phát hành có chủ đích, không phải tệp tạm. ZIP release candidate vẫn được tạo ngoài repository.

## 9. Tiêu chí rollback drill đạt

Rollback drill đạt khi:

1. xác định được `previous_version` và `previous_commit`;
2. worktree previous được dựng trực tiếp từ commit ấy;
3. công cụ bắt buộc khởi động và hồi quy chạy được;
4. SHA-256 hai QMD hồi quy khớp đường cơ sở;
5. trạng thái `publication: pending` được bảo toàn;
6. không sửa bài hồi quy hoặc hồ sơ dự án để thích nghi;
7. worktree sống không bị reset, clean hoặc ghi đè;
8. log ghi đủ lệnh, mã thoát và kết quả.

## 10. Quyền quyết định còn lại

O3 có thể tạo release candidate và tag dự kiến trong manifest. Chỉ người dùng mới quyết định:

- commit từng nhóm thay đổi;
- tạo Git tag thật;
- push commit hoặc tag;
- phát hành release chính thức;
- xuất bản website.
