# Rollback drill QMD Operations 0.5.0

## Phạm vi

- Phiên bản trước: `0.4.0`.
- Commit trước: `6425dec241cc27cad76bf55f8385531e56fb1a86`.
- Snapshot ứng viên: `4d8fe92c11d3b6da4267cadfd77463a3dcb24744`.
- Phiên bản ứng viên: `0.5.0`.
- Detached worktree phiên bản trước: `E:\zo_math_ca_nhan\qmd_release_0_5_0\previous`.
- Detached worktree ứng viên: `E:\zo_math_ca_nhan\qmd_release_0_5_0\candidate`.

## Kết quả đối chứng

- `regression --render` tại phiên bản `0.4.0`: PASS, 2 dự án, 2 bài, `render=yes`, exit code 0.
- `regression --render` tại phiên bản `0.5.0`: PASS, 2 dự án, 2 bài, `render=yes`, exit code 0.
- SHA-256 của `content/thpt/zo_math_100/100_ham_so_su_bien_thien_va_do_thi/core/ham_ln_x.qmd` ở cả hai snapshot: `5388b6e76806ae24cbe8dd36607729146cdb55e05fce4e38d9cdf9672dae17ce`.
- SHA-256 của `content/thpt/zo_math_100/100_bai_toan_thuc_te/core/chi_phi_di_taxi.qmd` ở cả hai snapshot: `d20163265f730bb5c0648c15791fc631a1fdd6c803c45c116608ac0c1c26edb3`.
- Trạng thái publication của các bài hồi quy giữ `pending` ở cả hai snapshot.
- Cả hai detached worktree đều được `doctor`/hồi quy xác nhận không có thay đổi Git.
- Worktree sống `E:\zo_math_bai_chuan` không bị reset hoặc clean trong drill.

## Kết luận

Rollback drill: **PASS**. Phiên bản trước và snapshot ứng viên đều vượt hồi quy có render, hai nguồn QMD không đổi và trạng thái xuất bản không bị tác động.
