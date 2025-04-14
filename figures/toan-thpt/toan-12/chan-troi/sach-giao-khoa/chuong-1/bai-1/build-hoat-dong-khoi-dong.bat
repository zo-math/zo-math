@echo off
REM Bước 1: Xuất PDF với LuaLaTeX
lualatex --shell-escape hoat-dong-khoi-dong.tex

REM Bước 2: Xuất SVG với pdftocairo
pdftocairo -svg -expand hoat-dong-khoi-dong.pdf hoat-dong-khoi-dong.svg

@REM REM Bước 2.: Xuất SVG với Inkscape
@REM inkscape --export-type="svg" "hoat-dong-khoi-dong.pdf" --export-filename="hoat-dong-khoi-dong.svg"

REM Bước 4: Chỉ giữ lại file cần thiết
echo Xuất thành công:
dir hoat-dong-khoi-dong.pdf
dir hoat-dong-khoi-dong.svg