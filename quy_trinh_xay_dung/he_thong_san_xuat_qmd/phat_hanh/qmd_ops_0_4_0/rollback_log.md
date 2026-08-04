# Rollback log — QMD Operations 0.4.0

## 1. Điểm quay lại

- Phiên bản trước: `0.3.0`
- Commit trước: `99a7c04c69eb0a54d381f5afd0d3e79fe26e9cab`
- Snapshot ứng viên: `9d10683b6b4b1a1db6d2bbd776b67ab468396f0d`
- Worktree previous: `E:\zo_math_o4_rc_previous`
- Worktree candidate: `E:\zo_math_o4_rc_candidate`
- Worktree sống: `E:\zo_math_o4`, không bị sửa bởi diễn tập.

## 2. Hồi quy trước và sau

Release `0.3.0` và snapshot ứng viên `0.4.0` đều được chạy hồi quy nguồn và render.

- `regression_before.txt`: PASS, 2 dự án, 2 bài, có render.
- `regression_after.txt`: PASS, 2 dự án, 2 bài, có render.

## 3. Bất biến của hai bài hồi quy

### `chi_phi_di_taxi.qmd`

- SHA-256 trước và sau: `d20163265f730bb5c0648c15791fc631a1fdd6c803c45c116608ac0c1c26edb3`
- `production='in_production'`.
- `publication='pending'`.

### `ham_ln_x.qmd`

- SHA-256 trước và sau: `5388b6e76806ae24cbe8dd36607729146cdb55e05fce4e38d9cdf9672dae17ce`
- Thẻ vẫn có `status='pending'`.

Hai QMD không thay đổi nội dung giữa release `0.3.0` và snapshot ứng viên `0.4.0`.

## 4. Sai lệch thời gian tệp

Trong worktree previous, PDF của `ham_ln_x.qmd` ban đầu bị báo cũ hơn QMD khoảng 1,4 mili giây do checkout.

QMD và PDF đều được tạo tại commit `32bc1c72f475b7d2f1955ac3e03482d33efd427d`.

Thời gian PDF được chuẩn hóa mà không đổi nội dung, Git blob, SHA-256 hoặc trạng thái Git. Sau đó hồi quy nguồn và render đều đạt.

## 5. Kết luận

Rollback drill O4 đạt:

- release trước và ứng viên đều chạy được;
- hồi quy nguồn và render đều đạt;
- hai bài đường cơ sở không đổi;
- trạng thái xuất bản `pending` được bảo toàn;
- các worktree tạm và worktree sống không bị thay đổi nội dung.

Release candidate `0.4.0` chưa được tạo hoặc xác minh.
