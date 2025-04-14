@echo off
REM Bước 1: Xuất PDF với LuaLaTeX
lualatex --shell-escape thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.tex

REM Bước 2: Xuất SVG với make4ht
make4ht -l -f html5+svg thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.tex "svg,-fontswitch"

REM Bước 3: Dọn dẹp file thừa
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.4ct
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.4tc
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.aux
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.css
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.dvi
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.html
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.idv
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.log
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.lg
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.tmp
del /Q thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.xref


REM Bước 4: Chỉ giữ lại file cần thiết
echo Xuất thành công:
dir thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.pdf
dir thap-he-so-nhi-thuc-dang-tam-giac-vuong-den-n-bang-9.svg