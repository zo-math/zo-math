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

## Chưa thực hiện

- [ ] Tạo commit sạch chứa hồ sơ tiền đóng gói.
- [ ] Tạo release ZIP.
- [ ] Verify release ZIP bằng CLI bên ngoài gói.
- [ ] Verify release ZIP bằng CLI tự chứa trong gói.
- [ ] Ghi SHA-256 của release ZIP.
- [ ] Tạo tag `qmd-ops-v0.5.0`.
- [ ] Push hoặc phát hành chính thức.
