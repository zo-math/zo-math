"""Sinh TEX/PDF/SVG vector cho bảng biến thiên ZO Math từ một JSON canonical."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


class VariationError(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
TOOL = Path(__file__).resolve().parent


def run(command, cwd, env=None):
    return subprocess.run(command, cwd=cwd, env=env, text=True, encoding="utf-8",
                          errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def point_key(value):
    value = value.strip().replace("−", "-")
    if value in {"−∞", "-∞"}:
        return float("-inf")
    if value in {"+∞", "∞"}:
        return float("inf")
    try:
        return float(value.replace(",", "."))
    except ValueError as exc:
        raise VariationError(f"Mốc không có thứ tự số được hỗ trợ: {value!r}") from exc


def validate_record(record):
    required = {"id", "rows", "title"}
    missing = sorted(required - record.keys())
    if missing:
        raise VariationError(f"{record.get('id', '?')}: thiếu trường {', '.join(missing)}")
    rows = record["rows"]
    if len(rows) not in {2, 3} or any(not isinstance(row, list) for row in rows):
        raise VariationError(f"{record['id']}: rows phải có hai hoặc ba hàng")
    width = len(rows[0])
    if width < 4 or width % 2 != 0 or any(len(row) != width for row in rows):
        raise VariationError(f"{record['id']}: số ô phải chẵn, đồng nhất và có ít nhất bốn ô")
    points = rows[0][1::2]
    keys = [point_key(x) for x in points]
    if keys != sorted(keys) or len(set(keys)) != len(keys):
        raise VariationError(f"{record['id']}: thứ tự mốc không tăng nghiêm ngặt")
    excluded = set(record.get("excluded_columns", []))
    if any(not isinstance(x, int) or x < 1 or x >= width for x in excluded):
        raise VariationError(f"{record['id']}: excluded_columns không hợp lệ")
    column_widths = record.get("column_min_widths_mm", {})
    if not isinstance(column_widths, dict):
        raise VariationError(f"{record['id']}: column_min_widths_mm phải là object")
    for raw_col, value in column_widths.items():
        if not isinstance(raw_col, str) or not raw_col.isdigit():
            raise VariationError(f"{record['id']}: khóa column_min_widths_mm phải là chỉ số cột")
        col = int(raw_col)
        if col < 0 or col >= width or isinstance(value, bool) or not isinstance(value, (int, float)):
            raise VariationError(f"{record['id']}: column_min_widths_mm không hợp lệ tại cột {raw_col}")
        if not 8 <= float(value) <= 60:
            raise VariationError(f"{record['id']}: chiều rộng cột phải nằm trong [8, 60] mm")
    if len(rows) == 3:
        derivative, variation = rows[1], rows[2]
        contradictions = []
        for col in range(2, width, 2):
            sign, trend = derivative[col].strip(), variation[col].strip()
            expected = {"+": "↗", "−": "↘", "-": "↘", "0": "→"}.get(sign)
            if expected and trend and expected not in trend:
                contradictions.append((col, sign, trend))
        if contradictions and not record.get("intentional_error", False):
            raise VariationError(f"{record['id']}: dấu đạo hàm mâu thuẫn chiều biến thiên: {contradictions}")
        for col in range(3, width - 1, 2):
            left, right = derivative[col - 1].strip(), derivative[col + 1].strip()
            if derivative[col].strip() == "0" and left == "+" and right in {"−", "-"}:
                if not variation[col].strip():
                    raise VariationError(f"{record['id']}: cực đại thiếu giá trị tại cột {col}")
            if derivative[col].strip() == "0" and left in {"−", "-"} and right == "+":
                if not variation[col].strip():
                    raise VariationError(f"{record['id']}: cực tiểu thiếu giá trị tại cột {col}")


def load_data(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise VariationError(f"Không đọc được JSON: {exc}") from exc
    if not isinstance(data, list) or not data:
        raise VariationError("Nguồn phải là một danh sách bảng không rỗng")
    ids = [item.get("id") for item in data]
    if len(ids) != len(set(ids)):
        raise VariationError("Mã bảng bị trùng")
    for item in data:
        validate_record(item)
    return data


def tex_escape(value):
    return (value.replace("\\", r"\textbackslash{}")
                 .replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
                 .replace("_", r"\_").replace("{", r"\{").replace("}", r"\}"))


def math_token(value):
    value = value.strip()
    direct = {
        "−∞": r"-\infty", "+∞": r"+\infty", "∞": r"\infty",
        "−": "-", "+": "+", "0": "0", "↗": r"\nearrow", "↘": r"\searrow",
        "→": r"\rightarrow", "∥": r"\parallel",
    }
    if value in direct:
        return f"${direct[value]}$"
    if re.fullmatch(r"[−+]?\d+(?:[,.]\d+)?", value):
        return "$" + value.replace("−", "-").replace(",", "{,}") + "$"
    if value in {"x"}:
        return "$x$"
    label = re.fullmatch(r"([A-Za-z])′\(x\)", value)
    if label:
        return f"${label.group(1)}^{{\\prime}}(x)$"
    label = re.fullmatch(r"([A-Za-z])\(x\)", value)
    if label:
        return f"${label.group(1)}(x)$"
    if value.startswith("↘ "):
        return r"$\searrow\;" + tex_escape(value[2:].strip()).replace("−", "-") + "$"
    if value.endswith(" ↗"):
        return "$" + tex_escape(value[:-2].strip()).replace("−", "-") + r"\;\nearrow$"
    return tex_escape(value)


def make_tex(record):
    rows = record["rows"]
    width = len(rows[0])
    body = []
    excluded = set(record.get("excluded_columns", []))
    column_widths = {int(col): float(value) for col, value in record.get("column_min_widths_mm", {}).items()}
    for r, row in enumerate(rows):
        cells = []
        for col, value in enumerate(row):
            shown = r > 0 and col in excluded
            token = r"$\parallel$" if shown else math_token(value)
            wrapper = "zoVarInterval" if col > 0 and col % 2 == 0 else "zoVarCell"
            node_style = f"|[minimum width={column_widths[col]:g}mm]| " if col in column_widths else ""
            cells.append(f"{node_style}\\{wrapper}{{{token}}}")
        body.append(" & ".join(cells) + r" \\")
    last_row = len(rows)
    vertical_rules = []
    for col in range(1, width):
        left_data_col, right_data_col = col - 1, col
        if right_data_col in column_widths:
            position = f"bbt-1-{col + 1}.west"
        elif left_data_col in column_widths:
            position = f"bbt-1-{col}.east"
        else:
            position = f"$(bbt-1-{col}.center)!0.5!(bbt-1-{col + 1}.center)$"
        vertical_rules.append(
            f"\\coordinate (bbt-v-{col}) at ({position});\n"
            f"\\draw[zo variation rule] (bbt-v-{col} |- bbt.north) -- (bbt-v-{col} |- bbt.south);"
        )
    horizontal_rules = [
        f"\\coordinate (bbt-h-{row}) at ($(bbt-{row}-1.center)!0.5!(bbt-{row + 1}-1.center)$);\n"
        f"\\draw[zo variation rule] (bbt.west |- bbt-h-{row}) -- (bbt.east |- bbt-h-{row});"
        for row in range(1, last_row)
    ]
    return "\n".join([
        r"\documentclass[border=2mm]{standalone}",
        r"\input{zo_variation_v01.tex}",
        r"\begin{document}",
        r"\pagecolor{zoVarBackground}",
        r"\begin{tikzpicture}",
        r"\matrix (bbt) [zo variation matrix] {",
        *body,
        r"};",
        r"\begin{scope}[on background layer]",
        r"\clip[rounded corners=2mm] (bbt.north west) rectangle (bbt.south east);",
        r"\fill[zoVarBackground] (bbt.north west) rectangle (bbt.south east);",
        *vertical_rules,
        *horizontal_rules,
        r"\end{scope}",
        r"\draw[zo variation frame] (bbt.north west) rectangle (bbt.south east);",
        r"\node[zo graph v02 font sentinel] at (bbt.center) {ZO};",
        r"\end{tikzpicture}",
        r"\end{document}", ""
    ])


def validate_outputs(pdf, svg):
    for tool in ("pdfinfo", "pdffonts", "pdfimages"):
        if not shutil.which(tool):
            raise VariationError(f"Thiếu công cụ kiểm tra: {tool}")
    info = run(["pdfinfo", str(pdf)], pdf.parent)
    if info.returncode or "Pages:           1" not in info.stdout:
        raise VariationError(f"PDF không phải một trang: {pdf}")
    fonts = run(["pdffonts", str(pdf)], pdf.parent)
    compact = fonts.stdout.replace(" ", "").lower()
    if "stixtwotext" not in compact or "stixtwomath" not in compact:
        raise VariationError(f"PDF thiếu font STIX: {pdf}")
    images = run(["pdfimages", "-list", str(pdf)], pdf.parent)
    if any(line.lstrip()[:1].isdigit() for line in images.stdout.splitlines()):
        raise VariationError(f"PDF chứa raster: {pdf}")
    try:
        root = ET.parse(svg).getroot()
    except ET.ParseError as exc:
        raise VariationError(f"SVG lỗi: {svg}: {exc}") from exc
    if not root.attrib.get("viewBox"):
        raise VariationError(f"SVG thiếu viewBox: {svg}")


def build_record(record, out_dir, force, check):
    stem = record["id"].lower()
    tex = out_dir / f"{stem}.tex"
    pdf = out_dir / f"{stem}.pdf"
    svg = out_dir / f"{stem}.svg"
    if not force and any(path.exists() for path in (tex, pdf, svg)):
        raise VariationError(f"Đầu ra đã tồn tại cho {record['id']}; dùng --force")
    tex.write_text(make_tex(record), encoding="utf-8", newline="\n")
    build_dir = Path(tempfile.mkdtemp(prefix="zo_variation_build_"))
    env = os.environ.copy()
    font_dir = ROOT / "assets" / "fonts"
    graph_style_dir = ROOT / "quy_trinh_xay_dung" / "cong_cu_do_thi_ham_so_zo_math" / "tex"
    env["TEXINPUTS"] = os.pathsep.join((str(out_dir), str(TOOL / "tex"), str(graph_style_dir), str(font_dir))) + os.pathsep
    env["OPENTYPEFONTS"] = str(font_dir) + os.pathsep
    env["MIKTEX_ENABLE_INSTALLER"] = "0"
    env["SOURCE_DATE_EPOCH"] = "0"
    try:
        result = run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", "-synctex=0",
                      f"-output-directory={build_dir}", tex.name], out_dir, env)
        if result.returncode:
            raise VariationError(f"LuaLaTeX lỗi ở {record['id']}:\n" + "\n".join((result.stdout + result.stderr).splitlines()[-25:]))
        built_pdf = build_dir / pdf.name
        built_svg = build_dir / svg.name
        result = run(["pdf2svg", str(built_pdf), str(built_svg)], build_dir, env)
        if result.returncode:
            raise VariationError(f"pdf2svg lỗi ở {record['id']}: {result.stderr}")
        shutil.copy2(built_pdf, pdf)
        shutil.copy2(built_svg, svg)
        if check:
            validate_outputs(pdf, svg)
    finally:
        shutil.rmtree(build_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    check_p = sub.add_parser("check")
    build_p = sub.add_parser("build")
    for p in (check_p, build_p):
        p.add_argument("source", type=Path)
    build_p.add_argument("--out-dir", type=Path, required=True)
    build_p.add_argument("--id", action="append", dest="ids")
    build_p.add_argument("--force", action="store_true")
    build_p.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        data = load_data(args.source.resolve())
        if args.command == "check":
            print(f"ĐẠT: {len(data)} bảng; hợp đồng và quan hệ dấu–chiều biến thiên hợp lệ.")
            return 0
        selected = [x for x in data if not args.ids or x["id"] in args.ids]
        if args.ids and len(selected) != len(set(args.ids)):
            raise VariationError("Có mã --id không tồn tại")
        out = args.out_dir.resolve()
        out.mkdir(parents=True, exist_ok=True)
        for record in selected:
            build_record(record, out, args.force, args.check)
            print(f"Đã dựng {record['id']}: {out / (record['id'].lower() + '.pdf')}")
        return 0
    except VariationError as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
