# Xác minh release candidate — QMD Operations 0.5.0

## Danh tính sản phẩm

- Tệp: `qmd-ops-v0.5.0-rc.zip`
- Package ID: `qmd-release-0-5-0-20260805-234913`
- Loại gói: `release`
- Phiên bản lớp vận hành: `0.5.0`
- Phiên bản mô-đun đóng gói: `0.4.0`
- Candidate commit: `ba85e35db84e092fbb2c1786ceb9fff707dfc438`
- Phiên bản trước: `0.4.0`
- Commit trước: `6425dec241cc27cad76bf55f8385531e56fb1a86`
- Số tệp payload: `52`
- SHA-256: `018bfd0ec562f618efc3e1bf0c236a10cc87ec74b28f4805e33369686190ce24`
- Tag dự kiến: `qmd-ops-v0.5.0`
- Tại thời điểm tạo ZIP, Git tag thật đã tạo: không

ZIP được tạo từ detached worktree sạch tại candidate commit `ba85e35db84e092fbb2c1786ceb9fff707dfc438`.

## Kết quả đóng gói

- Kết quả tự động: `PASS`.
- Mã thoát: `PACK_EXIT=0`.
- Log: [`bang_chung/release_pack.txt`](bang_chung/release_pack.txt).

## Kết quả xác minh

### CLI ngoài gói

- Kết quả tự động: `PASS`.
- Mã thoát: `VERIFY_EXTERNAL_EXIT=0`.
- Log: [`release_verify_external.txt`](release_verify_external.txt).

### CLI tự chứa trong payload

- Kết quả tự động: `PASS`.
- Mã thoát: `VERIFY_SELF_EXIT=0`.
- Log: [`release_verify_self.txt`](release_verify_self.txt).

Cả hai phép xác minh đều đạt các kiểm tra sau:

- cấu trúc cấp cao nhất;
- manifest schema phiên bản 1;
- an toàn payload;
- định dạng, tính đầy đủ và giá trị checksum;
- các nguồn khai báo trong manifest;
- release payload;
- runtime dependency closure của release.

SHA-256 của ZIP giữ nguyên trước và sau cả hai phép xác minh: `018bfd0ec562f618efc3e1bf0c236a10cc87ec74b28f4805e33369686190ce24`.

Hai log verify được tạo sau ZIP nên không thuộc payload của gói.

## Trạng thái hậu xác minh

- Annotated tag `qmd-ops-v0.5.0` được tạo cục bộ sau hai phép verify.
- Tag trỏ đến candidate/product commit `ba85e35db84e092fbb2c1786ceb9fff707dfc438`.
- Post-package evidence commit là `9dd5d082f78cced6ae136f6e836c65196af55300`; tag không trỏ đến commit này.
- Tag message khóa package ID `qmd-release-0-5-0-20260805-234913` và SHA-256 `018bfd0ec562f618efc3e1bf0c236a10cc87ec74b28f4805e33369686190ce24`.
- Việc tạo tag không sửa ZIP và không thay đổi SHA-256 của ZIP.
- Tại thời điểm push tag, nhánh `master` và `origin/master` đã được xác minh đồng bộ tại commit `5c1dddaae51c4e76f72628c8206d54d9ff7e1aff`.
- Tag được push lên origin sau khi ZIP và hai phép verify đã hoàn tất.
- Remote tag object `7d45d37ae0ccf6e4933d3342dfc5de6f9c3abd4a` khớp local tag object.
- Remote peeled target khớp product commit `ba85e35db84e092fbb2c1786ceb9fff707dfc438`; tag không trỏ đến `master` hiện tại.
- Việc push tag không sửa ZIP và không thay đổi SHA-256 `018bfd0ec562f618efc3e1bf0c236a10cc87ec74b28f4805e33369686190ce24`.
- Release chính thức chưa được tạo hoặc công bố; website chưa được publish.

## Kết luận

Release candidate `0.5.0` đã được đóng gói và vượt cả xác minh bằng CLI ngoài gói lẫn CLI tự chứa. Annotated tag đã được push lên origin; release chính thức chưa được tạo hoặc công bố và website chưa được publish.
