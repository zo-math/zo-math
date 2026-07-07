# Tạo tệp kiểm kê cấu trúc ZO Math

Trong Git Bash, ở `/e/zo_math`, chạy nguyên khối này:

```bash
{
  echo "===== THU MUC CONTENT DEN CAP 4 ====="
  find content -maxdepth 4 -type d | sort

  echo
  echo "===== CAC FILE INDEX.QMD ====="
  find content -type f -name "index.qmd" | sort

  echo
  echo "===== CAC FILE QMD DEN CAP 4 ====="
  find content -maxdepth 4 -type f -name "*.qmd" | sort

  echo
  echo "===== TITLE CUA CAC INDEX.QMD ====="
  grep -Hn "^title:" $(find content -type f -name "index.qmd" | sort)
} > zo_math_home_audit.txt
```

Sau đó gửi cho mình nội dung file:

```text
zo_math_home_audit.txt
```
