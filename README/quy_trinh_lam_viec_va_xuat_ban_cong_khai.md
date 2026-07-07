# Quy trình làm việc và xuất bản công khai ZO Math

## 1. Nguyên tắc

- /e/zo_math là nơi làm việc chính.
- /e/zo_math_publish là nơi xuất bản website công khai.
- Làm việc, render, preview đầy đủ trong /e/zo_math.
- Những mục chưa muốn công khai được ghi trong _publish_exclude.md.
- Khi xuất bản, script scripts/publish_public.sh sẽ render toàn bộ, copy sang /e/zo_math_publish, rồi xóa các mục trong _publish_exclude.md.

## 2. Khi mở VS Code để làm việc

Mở thư mục E:\zo_math.

Làm việc với .qmd như bình thường.

Render local:

    quarto render

Preview local:

    quarto preview

## 3. Khi muốn tạm ẩn một mục khỏi website công khai

Mở file _publish_exclude.md.

Thêm mỗi mục một dòng, dùng dấu /.

Ví dụ:

    content/di_tim/di_tim_xac_suat/
    content/di_tim/di_tim_ly_luan_toan_hoc/
    content/di_tim/di_tim_toan_hoc/

Không viết docs/ ở đầu dòng.

## 4. Khi muốn công khai lại một mục

Xóa dòng tương ứng trong _publish_exclude.md.

Sau đó xuất bản lại website công khai.

## 5. Khi xuất bản website công khai

Chạy trong Git Bash:

    cd /e/zo_math
    ./scripts/publish_public.sh

Script sẽ dừng ở bước hiển thị git status --short trong /e/zo_math_publish.

Nếu kiểm tra thấy đúng, chạy tiếp:

    cd /e/zo_math_publish
    git add -A
    git commit -m "Cap nhat website cong khai"
    git push origin gh-pages

## 6. Lưu ý quan trọng

Không push master lên repo public nếu trong source còn nội dung chưa muốn công khai.

Website công khai nên đi qua /e/zo_math_publish sau khi đã lọc.
