# QUY TRÌNH CẬP NHẬT VÀ XUẤT BẢN ZO MATH

## A. Cập nhật nhánh `master` (Phát triển & Render)

### Mỗi lần cập nhật nội dung hoặc code mới:

1️⃣ **Chuyển sang nhánh `master`**

```sh
git checkout master
```

2️⃣ **Cập nhật repository (nếu làm việc trên nhiều máy):**

```sh
git pull origin master
```

3️⃣ **Chỉnh sửa, thêm nội dung, cập nhật trang web**  
 (Chỉnh sửa `.qmd`, code, tài nguyên,...)

4️⃣ **Render lại toàn bộ trang web bằng Quarto**

```sh
quarto render
```

📌 **Lưu ý:**

- Quarto sẽ tạo ra nội dung mới trong thư mục `docs/`
- Nếu muốn làm sạch các kết quả cũ trước khi render, chạy:
  ```sh
  quarto clean
  ```

5️⃣ **Commit & đẩy lên GitHub (`master`)**

```sh
git add .
git commit -m "Cập nhật nội dung mới cho ZO Math"
git push origin master
```

## B. Cập nhật nhánh `gh-pages` (Xuất bản trang web)

### Sau khi đã cập nhật xong `master`, xuất bản trang web mới:\*\*

1️⃣ Chuyển sang nhánh `gh-pages`

```sh

git checkout gh-pages
```

2️⃣ Xóa nội dung cũ trong `gh-pages` để làm sạch

```sh
git rm -rf docs
```

3️⃣ Lấy thư mục `docs/` từ `master`

```sh

git checkout master -- docs
```

4️⃣ Commit & đẩy lên GitHub (`gh-pages`)

```sh
git add .
git commit -m "Cập nhật nội dung xuất bản"
git push --force origin gh-pages
```

**Lưu ý:**

- `--force` đảm bảo nội dung cũ bị ghi đè hoàn toàn.
- Nếu bạn đã đặt `docs/` làm thư mục gốc trong **GitHub Pages Settings**, không cần di chuyển file nào.

# 🔥 LƯU Ý QUAN TRỌNG

## 1. Xử lý lỗi khi chuyển nhánh `gh-pages` bị mất

Nếu chạy `git checkout gh-pages` mà gặp lỗi:

```sh
error: pathspec 'gh-pages' did not match any file(s) known to git
```

👉 Chạy lệnh tạo lại nhánh `gh-pages`:

```sh
git checkout --orphan gh-pages
```

Sau đó làm lại các bước cập nhật `gh-pages`.

## 2. Làm sạch file cũ trước khi render

Nếu muốn dọn dẹp các file cũ trước khi `quarto render`:

```sh
quarto clean
quarto render
```

## 3. Kiểm tra lại trước khi `push`

Trước khi `push`, luôn kiểm tra nội dung đã cập nhật đúng bằng cách chạy:

```sh
git status
git diff
```

Đảm bảo chỉ có các thay đổi mong muốn được đẩy lên GitHub.

# Tóm gọn

**Mỗi lần cập nhật nội dung:**

```sh
git checkout master
git pull origin master
quarto render
git add .
git commit -m "Cập nhật nội dung mới"
git push origin master
```

**Mỗi lần xuất bản trang web:**

```sh
git checkout gh-pages
git rm -rf docs
git checkout master -- docs
git add .
git commit -m "Cập nhật nội dung xuất bản"
git push --force origin gh-pages
```

---

# QUY TRÌNH ĐƯỢC CHATGPT HIỆU CHỈNH

Đây là **quy trình chuẩn mới** từ nay về sau.

Lý do: nó giữ đúng mô hình đang dùng:

```text
master    = nơi viết và render nội dung
gh-pages  = nơi xuất bản bản web trong docs/
```

Quy trình nên dùng cố định:

```sh
git checkout master
# Chuyển sang nhánh master, nơi bạn sửa nội dung gốc của website.

git pull origin master
# Lấy phiên bản mới nhất của nhánh master từ GitHub về máy.

quarto render
# Render toàn bộ website Quarto, tạo/cập nhật thư mục docs/.

touch docs/.nojekyll
# Báo cho GitHub Pages không xử lý site như Jekyll, để các file CSS/JS của Quarto được phục vụ đúng.

git add -A
# Đưa toàn bộ thay đổi trên master vào vùng chuẩn bị commit.

git commit -m "Cập nhật nội dung mới"
# Lưu các thay đổi nội dung và bản render docs/ thành một commit.

git push origin master
# Đẩy nhánh master mới nhất lên GitHub.
```

Rồi xuất bản:

```sh
git checkout gh-pages
# Chuyển sang nhánh gh-pages, nơi GitHub Pages lấy website để xuất bản.

git pull origin gh-pages
# Lấy phiên bản mới nhất của nhánh gh-pages từ GitHub về máy.

git rm -rf docs
# Xóa thư mục docs cũ trên nhánh gh-pages.

git checkout master -- docs
# Sao chép thư mục docs mới đã render từ nhánh master sang nhánh gh-pages.

git add -A docs
# Đưa toàn bộ thư mục docs mới vào vùng chuẩn bị commit.

git commit -m "Cập nhật nội dung xuất bản"
# Lưu bản website mới trên nhánh gh-pages.

git push origin gh-pages
# Đẩy bản xuất bản mới lên GitHub Pages.
```

Chỉ dùng `--force` khi Git báo không push được và bạn hiểu rằng mình muốn ghi đè nhánh `gh-pages`.

Với lần này, bạn cũng dùng đúng quy trình trên để sửa lỗi giao diện thô hiện tại. Sau đó vào GitHub Pages giữ:

```text
Branch: gh-pages
Folder: /docs
```
