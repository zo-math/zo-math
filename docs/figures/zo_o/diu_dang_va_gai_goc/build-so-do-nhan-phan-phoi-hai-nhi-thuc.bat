@echo off
REM Bước 1: Xuất PDF với LuaLaTeX
lualatex --shell-escape so-do-nhan-phan-phoi-hai-nhi-thuc.tex

REM Bước 2: Xuất SVG với make4ht
make4ht -l -f html5+svg so-do-nhan-phan-phoi-hai-nhi-thuc.tex "svg,-fontswitch"

REM Bước 3: Dọn dẹp file thừa
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.4ct
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.4tc
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.aux
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.css
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.dvi
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.html
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.idv
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.log
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.lg
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.tmp
del /Q so-do-nhan-phan-phoi-hai-nhi-thuc.xref


REM Bước 4: Chỉ giữ lại file cần thiết
echo Xuất thành công:
dir so-do-nhan-phan-phoi-hai-nhi-thuc.pdf
dir so-do-nhan-phan-phoi-hai-nhi-thuc.svg