"""Dựng đồ thị ZO Math v0.2 từ nguồn TikZ/PGFPlots thành PDF và SVG."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Sequence


class BuildError(RuntimeError):
    """Lỗi vận hành có thể trình bày trực tiếp cho người dùng."""


def find_repo_root() -> Path:
    """Tìm gốc repository từ vị trí script, không phụ thuộc thư mục gọi."""
    start = Path(__file__).resolve()
    for candidate in (start.parent, *start.parents):
        if (candidate / ".git").exists() and (candidate / "scripts" / "zo_python.py").is_file():
            return candidate
    raise BuildError("Không xác định được gốc repository ZO Math từ vị trí công cụ.")


def path_inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def require_tool(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise BuildError(f"Thiếu chương trình bắt buộc: {name}. Hãy cài hoặc thêm nó vào PATH.")
    return found


def run_command(command: Sequence[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def output_excerpt(result: subprocess.CompletedProcess[str], limit: int = 35) -> str:
    combined = "\n".join(part for part in (result.stdout, result.stderr) if part)
    lines = combined.splitlines()
    return "\n".join(lines[-limit:])


def make_tex_environment(repo_root: Path, source_dir: Path, style_dir: Path) -> dict[str, str]:
    env = os.environ.copy()
    font_dir = repo_root / "assets" / "fonts"
    search_dirs = (source_dir, style_dir, font_dir)
    tex_inputs = os.pathsep.join(str(item) for item in search_dirs) + os.pathsep
    font_inputs = str(font_dir) + os.pathsep
    if env.get("TEXINPUTS"):
        tex_inputs += env["TEXINPUTS"]
    if env.get("OPENTYPEFONTS"):
        font_inputs += env["OPENTYPEFONTS"]
    env["TEXINPUTS"] = tex_inputs
    env["OPENTYPEFONTS"] = font_inputs
    env["MIKTEX_ENABLE_INSTALLER"] = "0"
    return env


def validate_source(source: Path, repo_root: Path) -> None:
    if not source.is_file():
        raise BuildError(f"Không tìm thấy nguồn TeX: {source}")
    if source.suffix.lower() != ".tex":
        raise BuildError("Nguồn phải là tệp .tex.")
    if not path_inside(source, repo_root):
        raise BuildError("Nguồn bị từ chối vì không nằm trong repository ZO Math.")


def validate_pdf(pdf_path: Path, tools: dict[str, str], cwd: Path, env: dict[str, str]) -> None:
    info = run_command([tools["pdfinfo"], str(pdf_path)], cwd, env)
    if info.returncode != 0:
        raise BuildError("pdfinfo không đọc được PDF vừa dựng.\n" + output_excerpt(info))
    pages = None
    for line in info.stdout.splitlines():
        if line.lower().startswith("pages:"):
            pages = line.split(":", 1)[1].strip()
            break
    if pages != "1":
        raise BuildError(f"PDF phải có đúng một trang; giá trị nhận được: {pages or 'không xác định'}.")

    fonts = run_command([tools["pdffonts"], str(pdf_path)], cwd, env)
    if fonts.returncode != 0:
        raise BuildError("pdffonts không đọc được PDF vừa dựng.\n" + output_excerpt(fonts))
    compact_fonts = fonts.stdout.replace(" ", "").lower()
    if "stixtwotext" not in compact_fonts or "stixtwomath" not in compact_fonts:
        raise BuildError("PDF chưa nhúng đủ STIX Two Text và STIX Two Math.")

    images = run_command([tools["pdfimages"], "-list", str(pdf_path)], cwd, env)
    if images.returncode != 0:
        raise BuildError("pdfimages không kiểm tra được cấu trúc PDF.\n" + output_excerpt(images))
    image_rows = [line for line in images.stdout.splitlines() if line.strip() and line.lstrip()[:1].isdigit()]
    if image_rows:
        raise BuildError("PDF chứa ảnh raster; đầu ra đồ thị phải là vector.")


def validate_svg(svg_path: Path) -> None:
    try:
        root = ET.parse(svg_path).getroot()
    except (ET.ParseError, OSError) as exc:
        raise BuildError(f"SVG không hợp lệ: {exc}") from exc
    if root.tag.split("}")[-1] != "svg":
        raise BuildError("Tệp chuyển đổi không có phần tử gốc <svg>.")
    if not root.attrib.get("viewBox"):
        raise BuildError("SVG thiếu thuộc tính viewBox.")
    for element in root.iter():
        for raw_name, raw_value in element.attrib.items():
            name = raw_name.split("}")[-1].lower()
            value = raw_value.strip().lower()
            if (name == "href" and value.startswith(("http://", "https://", "file://"))) or "url(http" in value or "url(file:" in value:
                raise BuildError("SVG còn tham chiếu tài nguyên bên ngoài.")
    text = svg_path.read_text(encoding="utf-8", errors="replace").lower()
    forbidden = (("99" + "7918").lower(), ("52" + "6d82").lower())
    if any(color in text for color in forbidden):
        raise BuildError("SVG chứa màu không thuộc hệ đồ thị ZO Math v0.2.")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dựng một nguồn TikZ/PGFPlots ZO Math thành PDF vector và SVG."
    )
    parser.add_argument("source", type=Path, help="Đường dẫn nguồn .tex nằm trong repository.")
    parser.add_argument("--out-dir", type=Path, help="Thư mục nhận PDF và SVG; mặc định cạnh nguồn.")
    parser.add_argument("--check", action="store_true", help="Kiểm tra một trang, vector, font và SVG.")
    parser.add_argument("--keep-build", action="store_true", help="Giữ thư mục build tạm để chẩn đoán.")
    parser.add_argument("--force", action="store_true", help="Cho phép ghi đè PDF/SVG đã tồn tại.")
    parser.add_argument("--style", choices=("v0.2", "0.4"), default="v0.2",
                        help="0.4 là profile thử nghiệm, chỉ áp dụng khi chọn rõ.")
    parser.add_argument("--surface", choices=("paper", "transparent-light", "transparent-dark"),
                        default="paper", help="Nền hình; transparent chỉ dùng cho bìa đã kiểm bố trí nhãn.")
    parser.add_argument("--label-layout", type=Path, help="Sidecar bố trí nhãn 0.4; chỉ dịch hộp chữ, không sửa toán.")
    return parser.parse_args(argv)


def build(args: argparse.Namespace) -> tuple[Path, Path]:
    repo_root = find_repo_root()
    tool_root = Path(__file__).resolve().parent
    style_dir = tool_root / "tex"
    source = args.source.expanduser()
    if not source.is_absolute():
        source = Path.cwd() / source
    source = source.resolve()
    validate_source(source, repo_root)
    profile = getattr(args, "style", "v0.2")
    surface = getattr(args, "surface", "paper")
    if profile != "0.4" and surface != "paper":
        raise BuildError("Nền trong suốt yêu cầu lựa chọn --style 0.4.")
    layout_path = getattr(args, "label_layout", None)
    if layout_path and profile != "0.4":
        raise BuildError("Bố trí nhãn mới yêu cầu --style 0.4.")

    lualatex = require_tool("lualatex")
    pdf2svg = require_tool("pdf2svg")
    check_tools: dict[str, str] = {}
    if args.check:
        for name in ("pdfinfo", "pdffonts", "pdfimages"):
            check_tools[name] = require_tool(name)

    out_dir = args.out_dir.expanduser() if args.out_dir else source.parent
    if not out_dir.is_absolute():
        out_dir = Path.cwd() / out_dir
    out_dir = out_dir.resolve()
    output_pdf = out_dir / f"{source.stem}.pdf"
    output_svg = out_dir / f"{source.stem}.svg"
    occupied = [path for path in (output_pdf, output_svg) if path.exists()]
    if occupied and not args.force:
        names = ", ".join(str(path) for path in occupied)
        raise BuildError(f"Không ghi đè đầu ra hiện có nếu thiếu --force: {names}")

    build_dir = Path(tempfile.mkdtemp(prefix="zo_graph_build_"))
    env = make_tex_environment(repo_root, source.parent, style_dir)
    try:
        latex_source = source.name
        if profile == "0.4":
            original = source.read_text(encoding="utf-8")
            binding = r"\input{zo_graph_v02.tex}"
            if original.count(binding) != 1:
                raise BuildError("Profile 0.4 yêu cầu đúng một binding zo_graph_v02.tex trong nguồn.")
            if surface != "paper":
                # An open marker needs a local opaque mask. A generic transparent
                # profile cannot safely infer the background under that marker.
                if "point open" in original or r"\pagecolor" in original:
                    raise BuildError("Bìa trong suốt chưa hỗ trợ point open/pagecolor; không tự làm sai điểm khuyết.")
            wrapper = build_dir / source.name
            replacement = (r"\def\zoGraphVFourSurface{" + surface + "}\n"
                           + r"\input{zo_graph_v04.tex}")
            styled = original.replace(binding, replacement)
            if layout_path:
                layout_path = layout_path.resolve()
                if not path_inside(layout_path, repo_root):
                    raise BuildError("Sidecar bố trí phải nằm trong repository.")
                try:
                    layout = json.loads(layout_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as exc:
                    raise BuildError(f"Không đọc được sidecar bố trí: {exc}") from exc
                for item in layout.get("labels", []):
                    # Exact label content is retained by construction; only node
                    # style gains bounded display-unit offsets, never data coordinates.
                    offsets = [item.get(key, 0) for key in ("xshift_pt", "yshift_pt")]
                    if any(isinstance(v, bool) or not isinstance(v, (float, int)) or abs(v) > 60 for v in offsets):
                        raise BuildError("Dịch nhãn phải là số trong [-60,60] pt.")
                    pattern = (r"\\node\[(?P<style>[^\]]+)\](?P<position>\s+at\s+\(axis cs:[^)]+\)\s+)\{"
                               + re.escape(item["math"]) + r"\};")
                    def move(match):
                        return (r"\node[" + match['style'] + f",xshift={offsets[0]:g}pt,yshift={offsets[1]:g}pt]"
                                + match['position'] + "{" + item['math'] + "};")
                    styled, count = re.subn(pattern, move, styled)
                    if count != 1:
                        raise BuildError("Mỗi nhãn sidecar phải khớp đúng một node nguồn.")
                if layout.get("normalize_source_title_font"):
                    styled = styled.replace(r"\fontsize{10}{12}", r"\fontsize{12.8}{15.36}")
            wrapper.write_text(styled, encoding="utf-8", newline="\n")
            latex_source = str(wrapper)
        latex = run_command(
            [
                lualatex,
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                "-synctex=0",
                f"-output-directory={build_dir}",
                latex_source,
            ],
            source.parent,
            env,
        )
        if latex.returncode != 0:
            raise BuildError("LuaLaTeX thất bại. Trích đoạn log cuối:\n" + output_excerpt(latex))

        built_pdf = build_dir / f"{source.stem}.pdf"
        built_svg = build_dir / f"{source.stem}.svg"
        if not built_pdf.is_file() or built_pdf.stat().st_size == 0:
            raise BuildError("LuaLaTeX không tạo được PDF hợp lệ.")

        converted = run_command([pdf2svg, str(built_pdf), str(built_svg)], build_dir, env)
        if converted.returncode != 0 or not built_svg.is_file() or built_svg.stat().st_size == 0:
            raise BuildError("Chuyển PDF sang SVG thất bại.\n" + output_excerpt(converted))

        if args.check:
            validate_pdf(built_pdf, check_tools, build_dir, env)
            validate_svg(built_svg)

        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(built_pdf, output_pdf)
        shutil.copy2(built_svg, output_svg)
        return output_pdf, output_svg
    finally:
        if args.keep_build:
            print(f"Đã giữ thư mục build: {build_dir}", file=sys.stderr)
        else:
            shutil.rmtree(build_dir, ignore_errors=True)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        pdf_path, svg_path = build(args)
    except BuildError as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("LỖI: Đã hủy thao tác.", file=sys.stderr)
        return 130
    print(f"PDF: {pdf_path}")
    print(f"SVG: {svg_path}")
    if args.check:
        print("Kiểm tra kỹ thuật: ĐẠT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
