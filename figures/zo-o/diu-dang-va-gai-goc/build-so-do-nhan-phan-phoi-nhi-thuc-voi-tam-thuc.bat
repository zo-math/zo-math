@echo off
REM Bước 1: Xuất PDF với LuaLaTeX
lualatex --shell-escape so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.tex

REM Bước 2: Xuất SVG với make4ht
make4ht -ulm default -c myconfig.cfg -f html5 so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.tex "svg, -fontswitch"

REM Bước 3: Dọn dẹp file thừa
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.4ct
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.4tc
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.aux
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.css
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.dvi
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.html
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.idv
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.log
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.lg
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.tmp
del /Q so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.xref

REM Bước 4: Chỉ giữ lại file cần thiết
echo Xuất thành công:
dir so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.pdf
dir so-do-nhan-phan-phoi-nhi-thuc-voi-tam-thuc.svg