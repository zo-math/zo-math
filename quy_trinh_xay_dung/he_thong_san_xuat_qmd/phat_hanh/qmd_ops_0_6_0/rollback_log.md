# Rollback drill QMD Operations 0.6.0

## Phạm vi

- Previous release: `0.5.0`.
- Previous commit: `ba85e35db84e092fbb2c1786ceb9fff707dfc438`.
- Candidate product version: `0.6.0`.
- Candidate product commit: `1a2926926c4347a6830557f8b9ca69a46016bdfc`.
- Detached previous worktree: `C:\Users\DELL\AppData\Local\Temp\qmd_release_0_6_0_previous_ba85e35`.
- Detached candidate worktree: `C:\Users\DELL\AppData\Local\Temp\qmd_release_0_6_0_candidate_1a29269`.

Hai worktree nằm ngoài repository sống, được dựng trực tiếp từ hai commit trên và
được tháo bằng `git worktree remove` sau khi xác nhận sạch. Không dùng
`git reset`, `git clean` hoặc `git worktree remove --force`.

## Kết quả hồi quy

- Previous `0.5.0`: CLI `0.5.0`, checker `2.6.0`; `REGRESSION RESULT: PASS | projects=2 | articles=2 | render=yes`; exit code `0`.
- Candidate product `0.6.0`: CLI `0.6.0`, checker `2.7.0`; source và render đạt; filesystem hygiene `PASS`, `unexpected_new_paths=[]`; `REGRESSION RESULT: PASS | projects=2 | articles=2 | render=yes`; exit code `0`.
- Cả hai detached worktree sạch sau regression.
- Worktree sống không bị reset, clean, ghi đè hoặc dùng để chạy comparison.

## SHA-256 hai QMD hồi quy

| Tệp | Previous `0.5.0` | Candidate product `0.6.0` | Kết quả |
|---|---|---|---|
| `content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd` | `d20163265f730bb5c0648c15791fc631a1fdd6c803c45c116608ac0c1c26edb3` | `d20163265f730bb5c0648c15791fc631a1fdd6c803c45c116608ac0c1c26edb3` | Khớp |
| `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd` | `5388b6e76806ae24cbe8dd36607729146cdb55e05fce4e38d9cdf9672dae17ce` | `5388b6e76806ae24cbe8dd36607729146cdb55e05fce4e38d9cdf9672dae17ce` | Khớp |

## Trạng thái publication/card/profile

- `chi_phi_di_taxi`: hồ sơ giữ `trang_thai_san_xuat: in_production`, `trang_thai_xuat_ban: pending` và `xac_nhan_xuat_ban_cua_nguoi_dung: false` ở cả hai snapshot.
- `ham_ln_x`: thẻ 114 giữ `status: pending` và `href: ''` ở cả hai snapshot.
- Không sửa QMD hồi quy, hồ sơ dự án hoặc dữ liệu thẻ để làm regression đạt.

## Kết luận

Rollback drill: **PASS**. Previous release vẫn khởi động và vượt hồi quy có
render; candidate product vượt cùng hồi quy với hygiene đạt; hai QMD và trạng
thái xuất bản được bảo toàn. Bằng chứng cho phép ghi `rollback_tested: true`.
