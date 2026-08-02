# Release checklist — QMD Operations 0.3.0

## Danh tính ứng viên

- Phiên bản ứng viên: `0.3.0`
- Tag dự kiến: `qmd-ops-v0.3.0`
- Tag thật đã tạo: không
- Phiên bản trước: `0.2.0`
- Commit quay lại: `c1b26b9a0536b17e0885d8158fddbd20413767c2`
- Commit mã ứng viên trước hồ sơ: `902991bb3780aeb20d4d6f31e5c2abb795051428`

## Điều kiện trước khi đóng gói

- [x] Hai worktree previous và candidate được tạo ngoài worktree sống.
- [x] Hai worktree ở trạng thái detached và sạch.
- [x] Hồi quy nguồn và render tại phiên bản trước đạt, mã thoát `0`.
- [x] Hồi quy nguồn và render tại ứng viên đạt, mã thoát `0`.
- [x] Checker vẫn ở phiên bản `2.6.0`.
- [x] Hai QMD hồi quy có SHA-256 giống hệt trước và sau.
- [x] Trạng thái xuất bản của hai bài vẫn `pending`.
- [x] Rollback drill không sửa hai bài hồi quy để thích nghi.
- [x] Không dùng thao tác phá hủy worktree sống.
- [x] Hồ sơ phát hành và mọi bằng chứng bắt buộc có trong commit ứng viên.
- [x] `tag_created` vẫn là `false`.
- [x] Không push và không publish.

## Bước hậu commit — đã hoàn tất

- [x] Release candidate được tạo từ worktree sạch.
- [x] Candidate commit: `99a7c04c69eb0a54d381f5afd0d3e79fe26e9cab`.
- [x] Package ID: `qmd-release-0-3-0-20260802-223550`.
- [x] SHA-256 của ZIP: `cc6b28627ff365ee4a1a83e3a1529fe8a43047507c4b8bf9768bfae4a4a7547c`.
- [x] `verify` bằng CLI ngoài repository đạt, mã thoát `0`.
- [x] `verify` bằng CLI tự chứa trong payload đạt, mã thoát `0`.
- [x] Không tạo Git tag thật.
- [x] Không push và không publish.

Bằng chứng hậu đóng gói:

- `release_verification.md`;
- `release_verify_external.txt`;
- `release_verify_self.txt`.
