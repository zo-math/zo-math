# Changelog lớp vận hành QMD

Tài liệu này ghi những thay đổi quan sát được của lớp vận hành cỗ máy QMD. Nó không thay thế lịch sử Git và không tự chứng minh một release đã được tạo.

## Chưa phát hành — đích `0.3.0`

### Đã triển khai trong mã ứng viên

- Dùng `pack --kind context|release`; `context` tiếp tục là mặc định tương thích ngược.
- Gói release nhận một hồ sơ tường minh qua `--release-file`.
- Release candidate phải được tạo từ commit sạch và đầu ra tường minh ngoài repository.
- Manifest release phải ghi phiên bản, tag dự kiến, phiên bản và commit trước, trạng thái hồi quy và kết quả rollback drill.
- Release candidate phải mang changelog, ma trận phiên bản, checklist, hướng dẫn nâng cấp–khôi phục và bằng chứng hồi quy.
- O3 không tạo tag thật, không push và không publish.

### Mã ứng viên `0.3.0`

- Nâng `scripts/zo_qmd.py` và `scripts/zo_qmd_package.py` lên `0.3.0`.
- Thêm `pack --kind release --release-file ...` nhưng giữ `context` là mặc định.
- Từ chối release từ worktree bẩn, đầu ra trong repository, hồ sơ sai SemVer, tag, commit, trạng thái hồi quy hoặc rollback.
- Đưa tài liệu, runtime dependency, hai QMD hồi quy và toàn bộ bằng chứng khai báo vào payload.
- Mở rộng `verify` để kiểm tra quan hệ phiên bản–tag–commit, vai trò nguồn, payload bắt buộc và runtime dependency closure.
- Bổ sung self-test cho release hợp lệ, manifest release sai và worktree bẩn.

### Bằng chứng O3 đã hoàn tất trước đóng gói

- Hồi quy nguồn và render trước–sau đều đạt trên hai worktree riêng.
- Rollback drill về commit `c1b26b9a0536b17e0885d8158fddbd20413767c2` đạt.
- Hai QMD hồi quy giữ nguyên SHA-256 và trạng thái xuất bản vẫn `pending`.
- Hồ sơ, checklist, rollback log và hai log hồi quy đã được ghi tại `phat_hanh/qmd_ops_0_3_0/`.

### Chưa hoàn tất O3

- Chưa tạo và tự xác minh release candidate `0.3.0` từ commit sạch.
- O3 không tạo Git tag thật, không push và không publish.

### Di trú từ `0.2.0`

Không cần đổi lệnh tạo gói context hiện hành. Lệnh không khai báo `--kind` tiếp tục được hiểu là `context`. Chỉ quy trình tạo release candidate mới phải cung cấp `--kind release` và `--release-file`.

## `0.2.0` — 2026-08-02

Commit khóa:

```text
c1b26b9 feat(qmd-ops): add context package verification
```

### Thêm

- `scripts/zo_qmd_package.py`;
- `pack` tạo gói context dạng thư mục hoặc ZIP;
- `verify` kiểm tra manifest, checksum, tệp thiếu, tệp thừa, symlink và đường dẫn nguy hiểm;
- `PROMPT.md`, `MANIFEST.yml`, `FILES.sha256` và `payload/` giữ đường dẫn tương đối từ repository;
- khả năng tự xác minh gói ngoài repository Git;
- chặn sinh `__pycache__` và `.pyc` qua trình khởi chạy Python.

### Giữ nguyên

- checker `2.6.0`;
- lõi QMD `1.0`;
- hai bài hồi quy và trạng thái xuất bản `pending`.

## `0.1.0` — 2026-08-02

Commit khóa:

```text
53dba71 feat(qmd-ops): add unified operations cli
```

### Thêm

- điểm vào `scripts/zo_qmd.py`;
- các lệnh `doctor`, `inspect`, `check`, `render`, `regression`;
- điều phối checker và các self-test hiện hành mà không sao chép validator.

## Hợp đồng kiến trúc ban đầu

Commit:

```text
53e0cdd docs(qmd-ops): lock operations architecture
```

Mốc này chỉ khóa kiến trúc O0; chưa phải một release runtime độc lập.
