#!/usr/bin/env bash
set -euo pipefail

WORK_DIR="/e/zo_math"
PUBLISH_DIR="/e/zo_math_publish"
EXCLUDE_FILE="$WORK_DIR/_publish_exclude.md"

cd "$WORK_DIR"

echo "== Render website =="
quarto render

echo "== Update publish worktree =="
cd "$PUBLISH_DIR"
git pull origin gh-pages

echo "== Clear old public files =="
find . -mindepth 1 -maxdepth 1 ! -name ".git" -exec rm -rf -- {} +

echo "== Copy rendered website =="
cp -a "$WORK_DIR/docs/." .

echo "== Remove private paths =="
if [ -f "$EXCLUDE_FILE" ]; then
  while IFS= read -r path; do
    path="${path%$'\r'}"

    [ -z "$path" ] && continue
    case "$path" in
      \#*) continue ;;
    esac

    rm -rf -- "$path"
    echo "Excluded: $path"
  done < "$EXCLUDE_FILE"
fi

touch .nojekyll

echo "== Public status =="
git status --short
