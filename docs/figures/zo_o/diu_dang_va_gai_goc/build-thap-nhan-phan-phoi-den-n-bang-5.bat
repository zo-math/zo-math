@echo off
REM Bước 1: Xuất PDF với LuaLaTeX
lualatex --shell-escape thap-nhan-phan-phoi-den-n-bang-5.tex

REM Bước 2: Xuất SVG với make4ht
make4ht -l -f html5+svg thap-nhan-phan-phoi-den-n-bang-5.tex "svg,-fontswitch"

REM Bước 3: Dọn dẹp file thừa
del /Q thap-nhan-phan-phoi-den-n-bang-5.4ct
del /Q thap-nhan-phan-phoi-den-n-bang-5.4tc
del /Q thap-nhan-phan-phoi-den-n-bang-5.aux
del /Q thap-nhan-phan-phoi-den-n-bang-5.css
del /Q thap-nhan-phan-phoi-den-n-bang-5.dvi
del /Q thap-nhan-phan-phoi-den-n-bang-5.html
del /Q thap-nhan-phan-phoi-den-n-bang-5.idv
del /Q thap-nhan-phan-phoi-den-n-bang-5.log
del /Q thap-nhan-phan-phoi-den-n-bang-5.lg
del /Q thap-nhan-phan-phoi-den-n-bang-5.tmp
del /Q thap-nhan-phan-phoi-den-n-bang-5.xref


REM Bước 4: Chỉ giữ lại file cần thiết
echo Xuất thành công:
dir thap-nhan-phan-phoi-den-n-bang-5.pdf
dir thap-nhan-phan-phoi-den-n-bang-5.svg