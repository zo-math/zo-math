# Checklist release candidate QMD Operations 0.5.0

Snapshot triển khai dùng để thu thập bằng chứng: `4d8fe92c11d3b6da4267cadfd77463a3dcb24744`. Đây chưa phải commit sạch cuối của gói release.

## Đã đạt

- [x] Self-test của lớp vận hành đạt, gồm `zo_qmd_version.py`, `zo_qmd_config.py`, `zo_qmd_registry.py`, `zo_qmd_core.py`, `zo_real_world_problem.py`, `zo_qmd_package.py`, `zo_qmd_prepublish.py` và `zo_qmd.py`.
- [x] `doctor` đạt cho hai dự án; checker giữ `2.6.0`, schema dự án giữ `1`.
- [x] `inspect` đạt cho dự án hàm số và dự án bài toán thực tế; danh sách `quality_exemplars` được xuất đúng ở cả hai dự án.
- [x] Hồi quy nguồn trên snapshot ứng viên đạt: 2 dự án, 2 bài, `render=no`.
- [x] Hồi quy có render của phiên bản trước `0.4.0` đạt: 2 dự án, 2 bài, `render=yes`.
- [x] Hồi quy có render của ứng viên `0.5.0` đạt: 2 dự án, 2 bài, `render=yes`.
- [x] SHA-256 trước và sau của hai QMD hồi quy không đổi.
- [x] Trạng thái publication của các bài hồi quy vẫn là `pending`.
- [x] Context package thật được tạo ngoài repository và `verify` đạt.
- [x] Manifest chứa hai record `quality_exemplar`, và cả hai tệp tồn tại trong payload theo đúng đường dẫn repository.
- [x] Hai detached worktree dùng cho rollback drill đều sạch.
- [x] Rollback drill từ `0.5.0` về `0.4.0` đạt mà không reset hoặc clean worktree sống.
- [x] Đã tạo commit sạch chứa hồ sơ tiền đóng gói: `ba85e35db84e092fbb2c1786ceb9fff707dfc438`.
- [x] Đã tạo release ZIP `qmd-ops-v0.5.0-rc.zip`.
- [x] Verify release ZIP bằng CLI bên ngoài gói đạt.
- [x] Verify release ZIP bằng CLI tự chứa trong payload đạt.
- [x] Đã ghi SHA-256 của release ZIP: `018bfd0ec562f618efc3e1bf0c236a10cc87ec74b28f4805e33369686190ce24`.
- [x] Đã tạo annotated tag `qmd-ops-v0.5.0` trỏ đến target `ba85e35db84e092fbb2c1786ceb9fff707dfc438`; tag chỉ tồn tại cục bộ.

## Chưa thực hiện

- [ ] Push nhánh `master`.
- [ ] Push tag `qmd-ops-v0.5.0`.
- [ ] Phát hành chính thức.
