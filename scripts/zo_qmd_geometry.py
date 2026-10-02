"""Opt-in geometry asset lifecycle for configured QMD projects."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence

from zo_qmd_config import ProjectConfigError, discover_project_config


class GeometryLifecycleError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _assets_for_paths(root: Path, paths: Sequence[str]) -> list[tuple[Path, Path, int]]:
    assets: list[tuple[Path, Path, int]] = []
    seen_projects: set[Path] = set()
    for raw in paths:
        article = Path(raw)
        if article.suffix.casefold() != ".qmd":
            continue
        config = discover_project_config(root, article)
        if config is None or config.config_path in seen_projects:
            continue
        seen_projects.add(config.config_path)
        geometry = config.raw.get("extensions", {}).get("geometry")
        if geometry is None:
            continue
        if not isinstance(geometry, dict) or set(geometry) != {"assets"}:
            raise GeometryLifecycleError("extensions.geometry phải chỉ chứa khóa assets.")
        raw_assets = geometry["assets"]
        if not isinstance(raw_assets, list) or not raw_assets:
            raise GeometryLifecycleError("extensions.geometry.assets phải là danh sách không rỗng.")
        project_root = (root / config.project_root).resolve()
        for index, item in enumerate(raw_assets):
            label = f"extensions.geometry.assets[{index}]"
            if not isinstance(item, dict) or not {"source", "output"} <= set(item) <= {"source", "output", "dpi"}:
                raise GeometryLifecycleError(f"{label} phải có source, output và tùy chọn dpi.")
            source = (project_root / str(item["source"])).resolve()
            output = (project_root / str(item["output"])).resolve()
            if not _inside(source, project_root) or not _inside(output, project_root):
                raise GeometryLifecycleError(f"{label} chứa đường dẫn ngoài dự án.")
            dpi = item.get("dpi", 180)
            if not isinstance(dpi, int) or dpi <= 0:
                raise GeometryLifecycleError(f"{label}.dpi phải là số nguyên dương.")
            assets.append((source, output, dpi))
    return assets


def _receipt_errors(root: Path, source: Path, output: Path, dpi: int) -> list[str]:
    compiler = root / "scripts/zo_geometry.py"
    style = root / "assets/tex/zo-geometry-styles.tex"
    receipt_path = output.with_suffix(".geometry.json")
    required = [source, compiler, style, *(output.with_suffix(s) for s in (".tex", ".pdf", ".svg", ".png"))]
    missing = [str(path.relative_to(root)) for path in required if not path.is_file()]
    if missing:
        return ["thiếu tệp: " + ", ".join(missing)]
    if not receipt_path.is_file():
        return [f"thiếu receipt: {receipt_path.relative_to(root)}"]
    try:
        receipt: Any = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"receipt không đọc được: {exc}"]
    expected = {
        "schema_version": 1,
        "source_sha256": _sha256(source),
        "compiler_sha256": _sha256(compiler),
        "style_sha256": _sha256(style),
        "dpi": dpi,
        "outputs": {suffix: _sha256(output.with_suffix(suffix)) for suffix in (".tex", ".pdf", ".svg", ".png")},
    }
    return [] if receipt == expected else [f"receipt hoặc tài sản đã lỗi thời: {receipt_path.relative_to(root)}"]


def run_geometry_lifecycle(root: Path, paths: Sequence[str], *, build_stale: bool) -> int:
    try:
        assets = _assets_for_paths(root, paths)
    except (ProjectConfigError, GeometryLifecycleError, OSError) as exc:
        print(f"ERROR: geometry lifecycle: {exc}", file=sys.stderr)
        return 1
    if not assets:
        return 0
    launcher = root / "scripts/zo_python.py"
    compiler = root / "scripts/zo_geometry.py"
    checker = root / "scripts/zo_geometry_check.py"
    for source, output, dpi in assets:
        errors = _receipt_errors(root, source, output, dpi)
        if errors and build_stale:
            command = [sys.executable, str(launcher), str(compiler), "build", str(source), str(output), "--dpi", str(dpi)]
            if subprocess.run(command, cwd=root, check=False).returncode != 0:
                return 1
            errors = _receipt_errors(root, source, output, dpi)
        if errors:
            print("ERROR: geometry asset stale: " + "; ".join(errors), file=sys.stderr)
            return 1
        command = [sys.executable, str(launcher), str(checker), "--strict-labels", str(source), str(output.with_suffix(".svg"))]
        if subprocess.run(command, cwd=root, check=False).returncode != 0:
            return 1
        print(f"GEOMETRY PASS: {source.relative_to(root)} -> {output.relative_to(root)}")
    return 0


def _self_test() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "project/source.yml"
        output = root / "project/figure"
        compiler = root / "scripts/zo_geometry.py"
        style = root / "assets/tex/zo-geometry-styles.tex"
        for path, content in ((source, "id: test\n"), (compiler, "compiler\n"), (style, "style\n")):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        for suffix in (".tex", ".pdf", ".svg", ".png"):
            output.with_suffix(suffix).write_bytes(suffix.encode("ascii"))
        receipt = {
            "schema_version": 1,
            "source_sha256": _sha256(source),
            "compiler_sha256": _sha256(compiler),
            "style_sha256": _sha256(style),
            "dpi": 180,
            "outputs": {suffix: _sha256(output.with_suffix(suffix)) for suffix in (".tex", ".pdf", ".svg", ".png")},
        }
        output.with_suffix(".geometry.json").write_text(json.dumps(receipt), encoding="utf-8")
        assert _receipt_errors(root, source, output, 180) == []
        style.write_text("changed\n", encoding="utf-8")
        assert _receipt_errors(root, source, output, 180)


if __name__ == "__main__":
    if sys.argv[1:] != ["self-test"]:
        print("Usage: zo_qmd_geometry.py self-test", file=sys.stderr)
        raise SystemExit(2)
    _self_test()
    print("PASS: zo_qmd_geometry self-test")
