# Quy trình cập nhật ZO Math

1. Quay lại nhánh chính: `git checkout master`

2. Render lại trang để sinh ra thư mục \_site: `quarto render`
3. Chuyển sang nhánh gh-pages: `git checkout gh-pages`
4. Sao chép nội dung \_site từ nhánh master: `git checkout master _site`
5. Sao chép nội dung trong \_site ra ngoài: `cp -r _site/* .`
6. Xóa thư mục \_site để tránh lỗi: `rm -rf _site`
7. Commit và đẩy lên GitHub:
   - `git add .`
   - `git commit -m "Cập nhật ZO Math"`
   - `git push origin gh-pages`

**Lưu ý:** GitHub Pages viết tắt thành gh-pages. Nhánh gh-pages là một nhánh đặc biệt trên GitHub, được GitHub dùng để lấy nội dung và render trang web tĩnh trực tiếp từ kho lưu trữ.
