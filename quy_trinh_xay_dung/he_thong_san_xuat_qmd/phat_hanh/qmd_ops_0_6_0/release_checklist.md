# Checklist tiền đóng gói QMD Operations 0.6.0

Product commit dùng làm nền cho hồ sơ release:
`1a2926926c4347a6830557f8b9ca69a46016bdfc`.

Release package đã được tạo từ commit metadata tiền đóng gói `Cmeta`
`0441bbd5c20cdd884b7a318e637274da4987f163`. Annotated tag dự kiến sẽ trỏ
đến chính commit này nhưng chưa được tạo.

## Đã hoàn tất trước package

- [x] Product commit `1a2926926c4347a6830557f8b9ca69a46016bdfc` sạch trong detached worktree.
- [x] Danh tính candidate là release/CLI `0.6.0`, contract `0.6`, package module `0.5.0`, checker `2.7.0`.
- [x] Previous release `0.5.0` được khóa tại peeled target `ba85e35db84e092fbb2c1786ceb9fff707dfc438` của tag `qmd-ops-v0.5.0`.
- [x] Hồi quy có render của previous release đạt: 2 dự án, 2 bài, `render=yes`.
- [x] Hồi quy có render của candidate product đạt: 2 dự án, 2 bài, `render=yes`; filesystem hygiene đạt và không có đường dẫn mới bất ngờ.
- [x] SHA-256 của hai QMD hồi quy giống nhau giữa previous và candidate snapshot.
- [x] Trạng thái xuất bản của bài toán thực tế và trạng thái thẻ 114 của bài `ham_ln_x` vẫn `pending`; thẻ 114 giữ `href` rỗng.
- [x] Rollback drill bằng hai detached worktree ngoài repository sống đạt; hai worktree được tháo sau khi xác nhận sạch.
- [x] Năm tệp hồ sơ/evidence tiền đóng gói đã được chuẩn bị trong `qmd_ops_0_6_0/`.

## Trạng thái các bước hậu metadata

- [x] Review và staging tường minh năm tệp tiền đóng gói.
- [x] Tạo commit metadata tiền đóng gói `Cmeta` `0441bbd5c20cdd884b7a318e637274da4987f163`.
- [x] Tạo release ZIP từ detached worktree sạch tại `Cmeta`.
- [x] Verify release ZIP bằng CLI ngoài gói.
- [x] Verify release ZIP bằng CLI tự chứa trong payload.
- [x] Khóa package ID `qmd-release-0-6-0-20260809-220845` và SHA-256 `9e16f0124bcf44bb5ddc54ac6a771981075ecf00f5b0af7b0b2a0d6f4b78521e` của release ZIP.
- [x] Human acceptance cho release candidate.
- [x] Tạo annotated tag `qmd-ops-v0.6.0` trỏ đến `Cmeta`.
- [ ] Push chuỗi commit release.
- [ ] Push annotated tag.
- [ ] Tạo hoặc công bố release chính thức.
- [ ] Publish website.
