# Rollback log — QMD Operations 0.3.0

## 1. Điểm quay lại

- Phiên bản trước: `0.2.0`
- Commit trước: `c1b26b9a0536b17e0885d8158fddbd20413767c2`
- Commit mã ứng viên: `902991bb3780aeb20d4d6f31e5c2abb795051428`
- Worktree previous: `E:\zo_math_o3_previous`
- Worktree candidate: `E:\zo_math_o3_candidate`

Hai worktree được tạo bằng `git worktree add --detach`; worktree sống `E:\zo_math` không bị reset, clean hoặc ghi đè.

## 2. Hồi quy trước và sau

Phiên bản trước:

```text
REGRESSION RESULT: PASS | projects=2 | articles=2 | render=yes
EXIT_CODE=0
```

Ứng viên:

```text
REGRESSION RESULT: PASS | projects=2 | articles=2 | render=yes
EXIT_CODE=0
```

Log đầy đủ:

- `regression_before.txt`
- `regression_after.txt`

## 3. Bất biến của hai bài hồi quy

### `chi_phi_di_taxi.qmd`

```text
d20163265f730bb5c0648c15791fc631a1fdd6c803c45c116608ac0c1c26edb3
```

### `ham_ln_x.qmd`

```text
5388b6e76806ae24cbe8dd36607729146cdb55e05fce4e38d9cdf9672dae17ce
```

Các checksum trên giống hệt trong worktree previous và candidate.

Hồi quy xác nhận:

- `chi_phi_di_taxi.qmd`: `publication='pending'`;
- `ham_ln_x.qmd`: thẻ có `status='pending'`.

## 4. Sai lệch thời gian tệp khi dựng worktree

Khi Git tạo worktree mới, `ham_ln_x.qmd` được ghi sau `ham_ln_x.pdf` khoảng dưới 2 mili giây. Checker vì thế ban đầu báo PDF cũ hơn QMD dù Git blob và SHA-256 không đổi.

Để loại sai lệch chỉ thuộc metadata hệ thống tệp, thời gian của PDF được đặt bằng thời gian của QMD:

```bash
touch -r ham_ln_x.qmd ham_ln_x.pdf
```

Thao tác này:

- không thay đổi nội dung;
- không thay đổi Git blob;
- không thay đổi SHA-256;
- không làm worktree bẩn.

Sau khi chuẩn hóa thời gian, hồi quy đầy đủ đạt ở cả hai worktree.

## 5. Kết luận diễn tập

Rollback drill đạt vì:

1. release trước và commit quay lại được xác định;
2. worktree previous được dựng trực tiếp từ commit ấy;
3. self-test, hồi quy nguồn và render chạy thành công;
4. hai QMD hồi quy không đổi;
5. trạng thái `pending` được bảo toàn;
6. không sửa bài hồi quy để thích nghi;
7. worktree sống không bị tác động phá hủy;
8. log có lệnh, kết quả và mã thoát.

Không tạo Git tag, không push và không publish.
