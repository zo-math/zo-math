#!/usr/bin/env bash
set -euo pipefail

PAGE="${1:-}"

if [[ -z "$PAGE" ]]; then
  echo "Usage: bash scripts/zo_check_page.sh path/to/page.qmd"
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if [[ ! -f "$PAGE" ]]; then
  echo "ERROR: Không tìm thấy tệp: $PAGE"
  exit 1
fi

echo
echo "===== PAGE ====="
echo "$PAGE"

echo
echo "===== GIT STATUS ====="
git status --short

echo
echo "===== DIFF ====="
git --no-pager diff --stat
git --no-pager diff --name-status

echo
echo "===== EOL ====="
mapfile -t changed_files < <(git diff --name-only | sort -u)

if [[ ${#changed_files[@]} -eq 0 ]]; then
  echo "OK: không có tệp tracked đang thay đổi"
else
  git ls-files --eol -- "${changed_files[@]}" || true
fi

echo
echo "===== COMMAND REMNANT CHECK ====="
if grep -nE "^(cat >|python - <<|EOF$)|path\.write_text" "$PAGE"; then
  echo "ERROR: Có vẻ còn sót mã lệnh trong trang."
  exit 1
else
  echo "OK: không thấy mã lệnh thừa trong trang"
fi

echo
echo "===== TRAILING WHITESPACE CHECK ====="
python - <<'PY'
from pathlib import Path
import subprocess
import sys

result = subprocess.run(
    ["git", "diff", "--name-only"],
    capture_output=True,
    text=True,
    check=True,
)

bad = []

for name in result.stdout.splitlines():
    path = Path(name)
    if not path.is_file():
        continue

    data = path.read_bytes()

    for lineno, line in enumerate(data.splitlines(keepends=True), start=1):
        body = line.rstrip(b"\r\n")
        if body.endswith((b" ", b"\t")):
            bad.append(f"{name}:{lineno}: trailing whitespace")

if bad:
    print("\n".join(bad))
    sys.exit(1)

print("OK: không có khoảng trắng cuối dòng trong các tệp tracked đang sửa")
PY

echo
echo "===== RENDER ====="
quarto render "$PAGE"

OUT="docs/${PAGE%.qmd}.html"

echo
echo "===== OPEN ====="
if [[ -f "$OUT" ]]; then
  echo "$OUT"
  cmd //c start "" "$(cygpath -w "$OUT")" >/dev/null 2>&1 || true
else
  echo "WARN: Không tìm thấy HTML dự kiến: $OUT"
fi

echo
echo "===== DONE ====="