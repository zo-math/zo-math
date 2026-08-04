# Release checklist — QMD Operations 0.4.0

## Bằng chứng trước commit phát hành

- [x] Bảy mục tiêu O4 đã có hồ sơ tổng hợp.
- [x] Gói context cuối đã được xác minh ngoài gói và tự thân.
- [x] Hồi quy release `0.3.0` đạt, gồm cả render.
- [x] Hồi quy snapshot ứng viên `0.4.0` đạt, gồm cả render.
- [x] Rollback drill O4 đạt.
- [x] Hai QMD đường cơ sở giữ nguyên SHA-256.
- [x] Trạng thái xuất bản vẫn `pending`.
- [x] Tài liệu hiện hành đã được đồng bộ với trạng thái O4.
- [x] Hồ sơ `ho_so_release_candidate.yml` đã được lập.

## Bước hậu commit — đã hoàn tất, trừ quyết định khóa lớp vận hành `1.0`

- [x] Commit hồ sơ phát hành O4 từ worktree sạch.
- [x] Chạy lại doctor và regression tại commit cuối.
- [x] Tạo release candidate `qmd-ops-v0.4.0-rc.zip` ngoài repository.
- [x] Xác minh bằng CLI ngoài gói.
- [x] Xác minh bằng CLI tự chứa trong payload.
- [x] Ghi candidate commit, package ID và SHA-256 của ZIP.
- [x] Xác nhận không tạo Git tag thật.
- [x] Xác nhận không push hoặc publish.
- [ ] Người dùng quyết định riêng việc khóa lớp vận hành `1.0`.
