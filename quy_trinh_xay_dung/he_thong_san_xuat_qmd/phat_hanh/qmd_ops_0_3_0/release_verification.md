# Xác minh release candidate — QMD Operations 0.3.0

## Danh tính sản phẩm

- Tệp: `qmd-ops-v0.3.0-rc.zip`
- Package ID: `qmd-release-0-3-0-20260802-223550`
- Candidate commit: `99a7c04c69eb0a54d381f5afd0d3e79fe26e9cab`
- SHA-256: `cc6b28627ff365ee4a1a83e3a1529fe8a43047507c4b8bf9768bfae4a4a7547c`
- Loại gói: `release`
- Phiên bản: `0.3.0`
- Tag dự kiến: `qmd-ops-v0.3.0`
- Git tag thật đã tạo: không

## Kết quả xác minh

### CLI ngoài repository

- Kết quả tự động: `PASS`
- Mã thoát của công cụ: `0`
- Mã thoát của lần chạy: `0`
- Log đầy đủ: `release_verify_external.txt`

### CLI tự chứa trong payload

- Kết quả tự động: `PASS`
- Mã thoát của công cụ: `0`
- Mã thoát của lần chạy: `0`
- Log đầy đủ: `release_verify_self.txt`

## Quan hệ với commit ứng viên

Release candidate được tạo từ worktree sạch tại commit
`99a7c04c69eb0a54d381f5afd0d3e79fe26e9cab`.

Hai log được ghi sau khi ZIP đã được tạo. Chúng không thuộc payload của gói; chúng xác minh đúng sản phẩm được nhận diện bằng package ID, candidate commit và SHA-256 nêu trên.

## Kết luận

Release candidate `0.3.0` đã được tạo ngoài repository, đạt hai phép `verify`, giữ `tag_created: false`, không tạo tag thật, không push và không publish.
