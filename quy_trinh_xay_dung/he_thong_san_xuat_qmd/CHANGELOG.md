# Changelog lớp vận hành QMD

Tài liệu này ghi những thay đổi quan sát được của lớp vận hành cỗ máy QMD. Nó không thay thế lịch sử Git và không tự chứng minh một release đã được tạo.

## `0.4.0` — chưa phát hành — O4 đang triển khai

### Thêm và thay đổi

- Nâng `scripts/zo_qmd.py` lên phiên bản ứng viên `0.4.0`; nâng `scripts/zo_qmd_package.py` lên `0.3.1`; giữ checker `2.6.0` và lõi QMD `1.0`.
- Thêm `start` để tạo manifest phiên JSON từ yêu cầu ban đầu, kết quả `inspect`, nguồn có thẩm quyền, phạm vi, kế hoạch và các cổng người dùng.
- `start` yêu cầu đầu ra tường minh, chặn phạm vi được phép–loại trừ chồng lấn và chặn QMD hiện hữu thiếu hồ sơ bắt buộc.
- Thêm `scripts/zo_qmd_prepublish.py` và lệnh `prepublish` để tổng hợp manifest phiên, báo cáo `check`, báo cáo `render` cùng bảng kiểm có người quan sát.
- `prepublish` không chạy lại checker, không tự nghiệm thu, không sửa trạng thái xuất bản và luôn giữ `publication: pending`.
- Thêm self-test cùng phép thử trường hợp sẵn sàng, bị chặn và đầu ra không hợp lệ.
- Sửa kiểm tra freshness của QMD/PDF theo trạng thái Git để worktree mới không bị `FAIL` giả do sai lệch `mtime` khi checkout.
- Thống nhất `scripts/zo_qmd.py` là giao diện kĩ thuật của agent đối với bài QMD đã được cấu hình; giữ `scripts/zo_check_repo.py` là checker lõi phía sau.
- Bảo toàn khối nội dung ZO Math trong PDF và khái quát hóa các bài học từ kiểm định trực quan.
- Làm rõ giao diện người dùng là yêu cầu bằng ngôn ngữ tự nhiên, còn CLI thuộc agent; khóa phạm vi O4 ở các dự án đã được tích hợp.

### Bằng chứng hiện có

- Commit `278b1d9` bổ sung `start`.
- Commit `c966bcb` bổ sung `prepublish`.
- Hồi quy nguồn hai dự án đạt sau từng thay đổi.
- Hai QMD đường cơ sở giữ nguyên SHA-256.
- Worktree O4 sạch sau các commit triển khai và sửa lỗi.
- Gói context cuối `qmd-context-20260804-031754` đã vượt hai đường `verify`; chat-box mới chỉ dùng gói ấy đã tái hiện đúng nhiệm vụ.
- Agent mới trong VS Code dùng đúng giao diện vận hành, kiểm định bài đường cơ sở và không sửa repository.
- Phiên trình diễn đầu-cuối đi đến `prepublish`; lệnh chặn đúng khi kiểm định có người quan sát còn `FAIL` và giữ `publication: pending`.
- Release candidate `0.4.0` đã được tạo từ commit sạch `6425dec241cc27cad76bf55f8385531e56fb1a86` và vượt xác minh ngoài gói lẫn tự thân; package ID `qmd-release-0-4-0-20260804-142216`.
- Hồi quy nguồn cùng render của release `0.3.0` và ứng viên `0.4.0` đều đạt; hai QMD đường cơ sở không đổi, trạng thái xuất bản vẫn `pending`, và rollback drill O4 đã đạt.

### Chưa hoàn tất

- Chưa có quyết định khóa lớp vận hành 1.0.
- Không push và không publish.

### Di trú từ `0.3.0`

Các lệnh hiện có giữ nguyên. `start` và `prepublish` là hai lệnh mới, đều yêu cầu đầu ra JSON tường minh. `prepublish` cần manifest do `start` tạo, báo cáo `check`, báo cáo `render` và bảng kiểm có người quan sát; nó không thay thế các bước tạo bằng chứng ấy.

## `0.3.0` — 2026-08-02

### Thêm và thay đổi

- Dùng `pack --kind context|release`; `context` tiếp tục là mặc định tương thích ngược.
- Gói release nhận một hồ sơ tường minh qua `--release-file`.
- Release candidate phải được tạo từ commit sạch và đầu ra tường minh ngoài repository.
- Manifest release phải ghi phiên bản, tag dự kiến, phiên bản và commit trước, trạng thái hồi quy và kết quả rollback drill.
- Release candidate phải mang changelog, ma trận phiên bản, checklist, hướng dẫn nâng cấp–khôi phục và bằng chứng hồi quy.
- O3 không tạo tag thật, không push và không publish.

### Thành phần `0.3.0`

- Nâng `scripts/zo_qmd.py` và `scripts/zo_qmd_package.py` lên `0.3.0`.
- Thêm `pack --kind release --release-file ...` nhưng giữ `context` là mặc định.
- Từ chối release từ worktree bẩn, đầu ra trong repository, hồ sơ sai SemVer, tag, commit, trạng thái hồi quy hoặc rollback.
- Đưa tài liệu, runtime dependency, hai QMD hồi quy và toàn bộ bằng chứng khai báo vào payload.
- Mở rộng `verify` để kiểm tra quan hệ phiên bản–tag–commit, vai trò nguồn, payload bắt buộc và runtime dependency closure.
- Bổ sung self-test cho release hợp lệ, manifest release sai và worktree bẩn.

### Bằng chứng phát hành

- Hồi quy nguồn và render trước–sau đều đạt trên hai worktree riêng.
- Rollback drill về commit `c1b26b9a0536b17e0885d8158fddbd20413767c2` đạt.
- Hai QMD hồi quy giữ nguyên SHA-256 và trạng thái xuất bản vẫn `pending`.
- Hồ sơ, checklist, rollback log và hai log hồi quy đã được ghi tại `phat_hanh/qmd_ops_0_3_0/`.

### Ranh giới phát hành

- Release candidate `0.3.0` đã được tạo từ commit sạch và đạt hai phép `verify`; danh tính cùng log được lưu tại `phat_hanh/qmd_ops_0_3_0/`.
- Git tag thật chưa được tạo; không push và không publish.

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
