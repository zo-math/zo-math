"""Kiểm thử tích hợp cho bộ công cụ đồ thị hàm số ZO Math v0.1."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


class TestFailure(AssertionError):
    pass


def repo_root_from_script() -> Path:
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / ".git").exists() and (candidate / "scripts" / "zo_python.py").is_file():
            return candidate
    raise TestFailure("Không tìm được gốc repository.")


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TestFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_fingerprint(path: Path) -> tuple[bool, tuple[tuple[str, int, str], ...]]:
    if not path.exists():
        return False, ()
    if path.is_file():
        return True, ((path.name, path.stat().st_size, sha256(path)),)
    rows = []
    for item in sorted((p for p in path.rglob("*") if p.is_file()), key=lambda p: str(p).lower()):
        rows.append((item.relative_to(path).as_posix(), item.stat().st_size, sha256(item)))
    return True, tuple(rows)


def validate_pdf(pdf: Path, cwd: Path) -> None:
    info = run(["pdfinfo", str(pdf)], cwd)
    require(info.returncode == 0, f"pdfinfo thất bại với {pdf.name}")
    require(any(line.lower().startswith("pages:") and line.split(":", 1)[1].strip() == "1" for line in info.stdout.splitlines()), f"{pdf.name} không phải PDF một trang")

    fonts = run(["pdffonts", str(pdf)], cwd)
    require(fonts.returncode == 0, f"pdffonts thất bại với {pdf.name}")
    compact = fonts.stdout.replace(" ", "").lower()
    require("stixtwotext" in compact, f"{pdf.name} thiếu STIX Two Text")
    require("stixtwomath" in compact, f"{pdf.name} thiếu STIX Two Math")

    images = run(["pdfimages", "-list", str(pdf)], cwd)
    require(images.returncode == 0, f"pdfimages thất bại với {pdf.name}")
    image_rows = [line for line in images.stdout.splitlines() if line.strip() and line.lstrip()[:1].isdigit()]
    require(not image_rows, f"{pdf.name} chứa ảnh raster")


def validate_svg(svg: Path) -> None:
    root = ET.parse(svg).getroot()
    require(root.tag.split("}")[-1] == "svg", f"{svg.name} không có gốc SVG")
    require(bool(root.attrib.get("viewBox")), f"{svg.name} thiếu viewBox")
    for element in root.iter():
        for raw_name, raw_value in element.attrib.items():
            name = raw_name.split("}")[-1].lower()
            value = raw_value.strip().lower()
            external = (name == "href" and value.startswith(("http://", "https://", "file://"))) or "url(http" in value or "url(file:" in value
            require(not external, f"{svg.name} phụ thuộc tài nguyên ngoài")


def main() -> int:
    repo_root = repo_root_from_script()
    tool_root = Path(__file__).resolve().parents[1]
    build_script = tool_root / "zo_graph_build.py"
    fixtures = tool_root / "kiem_thu" / "fixtures"
    samples = tool_root / "mau"
    style = tool_root / "tex" / "zo_graph_v02.tex"
    literal_system_drive = repo_root / "%SystemDrive%"
    system_drive_before = tree_fingerprint(literal_system_drive)
    temp_before = {path.resolve() for path in Path(tempfile.gettempdir()).glob("zo_graph_build_*")}

    for tool in ("lualatex", "pdf2svg", "pdfinfo", "pdffonts", "pdfimages"):
        require(shutil.which(tool) is not None, f"Thiếu công cụ kiểm thử: {tool}")

    style_text = style.read_text(encoding="utf-8")
    require("{HTML}{EF5350}" in style_text, "Style không định nghĩa đúng đỏ ZO Math")
    for style_name in ("solid", "dashed", "dashdot"):
        marker = f"zo graph v02 curve {style_name}/.style"
        require(marker in style_text, f"Thiếu style đường {style_name}")
    curve_blocks = [block for block in style_text.split("zo graph v02 curve ")[1:4]]
    require(all("draw=zoGraphVTwoMain" in block and "line width=1.1pt" in block for block in curve_blocks), "Ba style đường không cùng màu hoặc cùng 1,1 pt")

    direct_text = (samples / "do_thi_nhan_truc_tiep.tex").read_text(encoding="utf-8")
    legend_text = (samples / "do_thi_hop_chu_thich.tex").read_text(encoding="utf-8")
    expected_styles = ("solid", "dashed", "dashdot")
    for name in expected_styles:
        require(f"\\addplot[zo graph v02 curve {name}" in direct_text, f"Mẫu nhãn trực tiếp thiếu đường {name}")
        require(f"\\addplot[zo graph v02 curve {name}" in legend_text, f"Mẫu chú thích thiếu đường {name}")
        require(f"\\addlegendimage{{zo graph v02 curve {name}}}" in legend_text, f"Mẫu nét chú thích không khớp đường {name}")

    forbidden = (("99" + "7918").lower(), ("52" + "6d82").lower())
    for path in tool_root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".py", ".tex", ".md"}:
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            require(not any(token in text for token in forbidden), f"Màu bị cấm xuất hiện trong {path.relative_to(tool_root)}")

    with tempfile.TemporaryDirectory(prefix=".zo_graph_tests_", dir=tool_root / "kiem_thu") as raw_temp:
        test_dir = Path(raw_temp)
        outputs = test_dir / "outputs"
        outputs.mkdir()

        built: dict[str, tuple[Path, Path]] = {}
        for fixture_name in ("mot_duong", "nhan_truc_tiep", "hop_chu_thich"):
            source = fixtures / f"{fixture_name}.tex"
            destination = outputs / fixture_name
            command = [sys.executable, str(build_script), str(source), "--out-dir", str(destination), "--check"]
            result = run(command, repo_root)
            require(result.returncode == 0, f"Dựng {fixture_name} thất bại:\n{result.stderr}\n{result.stdout}")
            pdf = destination / f"{fixture_name}.pdf"
            svg = destination / f"{fixture_name}.svg"
            require(pdf.is_file() and svg.is_file(), f"Thiếu đầu ra của {fixture_name}")
            validate_pdf(pdf, repo_root)
            validate_svg(svg)
            built[fixture_name] = (pdf, svg)
            print(f"PASS build/vector/SVG/font: {fixture_name}")

        multi_svg = built["nhan_truc_tiep"][1].read_text(encoding="utf-8", errors="replace").lower()
        require("stroke-dasharray" in multi_svg, "SVG nhiều đường không chứa mẫu nét đứt")
        dash_values = {part.split(";", 1)[0] for part in multi_svg.split("stroke-dasharray:")[1:]}
        require(len(dash_values) >= 2, "SVG nhiều đường không thể hiện đủ nét đứt và gạch-chấm")
        print("PASS màu/độ dày/ba kiểu nét và mẫu nét chú thích")

        protected_pdf, protected_svg = built["mot_duong"]
        before_hashes = (sha256(protected_pdf), sha256(protected_svg))
        no_force = run([sys.executable, str(build_script), str(fixtures / "mot_duong.tex"), "--out-dir", str(protected_pdf.parent)], repo_root)
        require(no_force.returncode != 0 and "--force" in no_force.stderr, "Công cụ đã ghi đè khi thiếu --force")
        require(before_hashes == (sha256(protected_pdf), sha256(protected_svg)), "Đầu ra đổi dù thiếu --force")
        with_force = run([sys.executable, str(build_script), str(fixtures / "mot_duong.tex"), "--out-dir", str(protected_pdf.parent), "--force", "--check"], repo_root)
        require(with_force.returncode == 0, "--force không hoạt động")
        print("PASS bảo vệ ghi đè và --force")

        spaced_dir = test_dir / "thu muc co khoang trang"
        spaced_dir.mkdir()
        spaced_source = spaced_dir / "nguon co khoang trang.tex"
        shutil.copy2(samples / "do_thi_mot_duong.tex", spaced_source)
        spaced_output = test_dir / "dau ra co khoang trang"
        spaced = run([sys.executable, str(build_script), str(spaced_source), "--out-dir", str(spaced_output), "--check"], repo_root)
        require(spaced.returncode == 0, f"Đường dẫn có khoảng trắng thất bại:\n{spaced.stderr}")
        require((spaced_output / "nguon co khoang trang.pdf").is_file(), "Thiếu PDF cho đường dẫn có khoảng trắng")
        print("PASS đường dẫn có khoảng trắng")

        bad_source = test_dir / "loi_bien_dich.tex"
        bad_source.write_text("\\documentclass{standalone}\n\\begin{document}\n\\lenhKhongTonTai\n\\end{document}\n", encoding="utf-8")
        bad = run([sys.executable, str(build_script), str(bad_source), "--out-dir", str(test_dir / "bad-output")], repo_root)
        require(bad.returncode != 0, "Lỗi biên dịch không trả mã khác 0")
        require("LuaLaTeX thất bại" in bad.stderr, "Thông báo lỗi biên dịch không rõ")
        print("PASS lỗi biên dịch và thông báo")

        with tempfile.TemporaryDirectory(prefix="zo_graph_outside_") as outside_raw:
            outside = Path(outside_raw) / "outside.tex"
            outside.write_text("\\documentclass{standalone}\n\\begin{document}x\\end{document}\n", encoding="utf-8")
            rejected = run([sys.executable, str(build_script), str(outside)], repo_root)
            require(rejected.returncode != 0 and "không nằm trong repository" in rejected.stderr, "Nguồn ngoài repository không bị từ chối")
        print("PASS từ chối nguồn ngoài repository")

        keep_output = test_dir / "keep-build-output"
        kept = run([sys.executable, str(build_script), str(fixtures / "mot_duong.tex"), "--out-dir", str(keep_output), "--keep-build"], repo_root)
        require(kept.returncode == 0, "--keep-build không dựng thành công")
        marker = "Đã giữ thư mục build:"
        kept_lines = [line for line in kept.stderr.splitlines() if marker in line]
        require(len(kept_lines) == 1, "--keep-build không báo đúng một thư mục build")
        kept_dir = Path(kept_lines[0].split(marker, 1)[1].strip()).resolve()
        require(kept_dir.is_dir() and kept_dir.name.startswith("zo_graph_build_"), "--keep-build không giữ đúng thư mục tạm")
        shutil.rmtree(kept_dir)
        print("PASS --keep-build và dọn thư mục được giữ sau kiểm tra")

    temp_after = {path.resolve() for path in Path(tempfile.gettempdir()).glob("zo_graph_build_*")}
    require(temp_after == temp_before, "Còn thư mục build tạm sau kiểm thử")
    require(tree_fingerprint(literal_system_drive) == system_drive_before, "%SystemDrive%/ bị tạo mới hoặc thay đổi")
    print("PASS dọn thư mục tạm và bảo toàn %SystemDrive%/")
    print("TẤT CẢ KIỂM THỬ ĐẠT")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except TestFailure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
