# Xác minh release candidate — QMD Operations 0.6.0

## Danh tính sản phẩm

- Release candidate: `0.6.0`.
- Product base: `1a2926926c4347a6830557f8b9ca69a46016bdfc`.
- Candidate commit / Cmeta: `0441bbd5c20cdd884b7a318e637274da4987f163`.
- Tệp ZIP: `qmd-ops-v0.6.0-rc.zip`.
- Package ID: `qmd-release-0-6-0-20260809-220845`.
- Loại gói: `release`.
- Phiên bản mô-đun đóng gói: `0.5.0`.
- Số tệp payload: `48`.
- SHA-256: `9e16f0124bcf44bb5ddc54ac6a771981075ecf00f5b0af7b0b2a0d6f4b78521e`.
- Tag dự kiến: `qmd-ops-v0.6.0`, trỏ đến Cmeta `0441bbd5c20cdd884b7a318e637274da4987f163`.

ZIP được tạo từ detached worktree sạch tại candidate commit/Cmeta
`0441bbd5c20cdd884b7a318e637274da4987f163`. Product base của candidate là
`1a2926926c4347a6830557f8b9ca69a46016bdfc`.

## Kết quả đóng gói

- Kết quả tự động: `PASS`.
- Mã thoát: `0`.
- Log: [`bang_chung/release_pack.txt`](bang_chung/release_pack.txt).

## Kết quả xác minh

### CLI ngoài gói

- Kết quả tự động: `PASS`.
- Mã thoát: `0`.
- Log: [`release_verify_external.txt`](release_verify_external.txt).

### CLI tự chứa trong payload

- Kết quả tự động: `PASS`.
- Mã thoát: `0`.
- Log: [`release_verify_self.txt`](release_verify_self.txt).

Cả hai phép xác minh đạt các kiểm tra cấu trúc cấp cao nhất, manifest schema,
an toàn payload, checksum, nguồn khai báo, release payload và runtime dependency
closure.

SHA-256 của ZIP giữ ổn định trước và sau hai phép xác minh:
`9e16f0124bcf44bb5ddc54ac6a771981075ecf00f5b0af7b0b2a0d6f4b78521e`.

## Trạng thái sau xác minh

- Human acceptance: `PENDING`.
- Annotated tag: `NOT_CREATED`.
- Push commit: `NOT_DONE`.
- Push tag: `NOT_DONE`.
- Release chính thức: `NOT_DONE`.
- Publish website: `NOT_DONE`.

Release candidate `0.6.0` đã được đóng gói và vượt hai phép xác minh tự động.
Kết quả này không phải human acceptance và không có nghĩa `0.6.0` đã được phát
hành, tag, push hoặc publish.
