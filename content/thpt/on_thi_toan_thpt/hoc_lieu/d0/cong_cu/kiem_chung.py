from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import yaml

from tao_qmd_chuyen_doi import PRIVATE_FIELDS, PUBLIC_FIELDS, build_qmd


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = next(
    parent for parent in (PACKAGE_ROOT, *PACKAGE_ROOT.parents) if (parent / ".git").exists()
)
PROCESS_ROOT = PACKAGE_ROOT / "_quy_trinh"
BASELINE_ROOT = PROCESS_ROOT / "lich_su" / "v1_0"
MANIFEST_PATH = PROCESS_ROOT / "manifest_chuyen_doi.yml"
CONFIG_PATH = PROCESS_ROOT / "cau_hinh_san_xuat_qmd.yml"
PROFILE_PATH = PROCESS_ROOT / "ho_so" / "index.yml"
CONTRACT_PATH = PROCESS_ROOT / "hop_dong_nguon_canonical.md"
PROJECTION_MATRIX_PATH = PROCESS_ROOT / "ma_tran_phep_chieu_noi_dung.md"
CANONICAL_DATA_PATH = PACKAGE_ROOT / "du_lieu" / "ngan_hang.json"
QMD_PATH = PACKAGE_ROOT / "index.qmd"
LUA_PATH = PACKAGE_ROOT / "cong_cu" / "d0.lua"
GENERATOR_PATH = PACKAGE_ROOT / "cong_cu" / "tao_qmd_chuyen_doi.py"
ASSET_ROOT = PACKAGE_ROOT / "hinh"
PLAN_PATH = PACKAGE_ROOT / ".." / ".." / "tot_nghiep_thpt" / "2027" / "_quy_trinh" / "dieu_hanh" / "ke_hoach_dieu_hanh.md"
HISTORICAL_STUDENT_PATH = BASELINE_ROOT / "2027_D0_hoc_sinh_v1.0.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.relative_to(REPO_ROOT)} không phải YAML mapping")
    return value


def walk_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(walk_strings(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(walk_strings(item))
        return result
    return []


def verify_original_manifest(manifest: dict) -> None:
    baseline = manifest["baseline"]
    original_manifest = BASELINE_ROOT / "MANIFEST_SHA256.txt"
    require(original_manifest.is_file(), "thiếu manifest SHA-256 gốc")
    require(
        sha256(original_manifest) == baseline["manifest_sha256"],
        "hash manifest gốc không khớp hợp đồng chuyển đổi",
    )

    lines = original_manifest.read_text(encoding="utf-8").splitlines()
    entries: list[tuple[str, str]] = []
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, f"dòng manifest gốc không hợp lệ: {line}")
        entries.append((match.group(1), match.group(2)))
    require(len(entries) == baseline["manifest_entries"], "sai số mục manifest gốc")
    for expected, relative in entries:
        path = BASELINE_ROOT / relative
        require(path.is_file(), f"thiếu tệp baseline: {relative}")
        require(sha256(path) == expected, f"hash baseline sai: {relative}")

    supplemental = baseline["supplemental_file"]
    supplemental_path = BASELINE_ROOT / supplemental["path"]
    require(supplemental_path.is_file(), "thiếu tài liệu bổ sung ngoài manifest")
    require(
        sha256(supplemental_path) == supplemental["sha256"],
        "hash tài liệu bổ sung không khớp",
    )
    require(
        len([path for path in BASELINE_ROOT.rglob("*") if path.is_file()])
        == baseline["total_files"],
        "tổng số tệp baseline không khớp",
    )


def verify_classification(manifest: dict) -> None:
    authority = {
        key: value
        for key, value in manifest["authority"].items()
        if key != "governing"
    }
    classified = {(PACKAGE_ROOT / value).resolve() for value in walk_strings(authority)}
    actual = {path.resolve() for path in BASELINE_ROOT.rglob("*") if path.is_file()}
    require(classified == actual, "phân loại 25 tệp baseline không còn chính xác")

    for relative in manifest["authority"]["governing"]:
        require((PACKAGE_ROOT / relative).is_file(), f"thiếu tài liệu điều hành: {relative}")


def verify_inventory(manifest: dict, data: dict) -> None:
    inventory = manifest["inventory"]
    items = data.get("items")
    require(isinstance(items, list), "ngân hàng không có danh sách items")
    require(data.get("version") == "1.0", "phiên bản ngân hàng không phải 1.0")
    require(len(items) == inventory["primary_count"], "sai số nhiệm vụ chính")

    primary_ids = [item.get("id") for item in items]
    retest_ids = [item.get("retest_id") for item in items]
    family_ids = [item.get("family") for item in items]
    require(primary_ids == inventory["primary_ids"], "tập hoặc thứ tự ID chính sai")
    require(retest_ids == inventory["retest_ids"], "tập hoặc thứ tự ID thử lại sai")
    require(family_ids == inventory["family_ids"], "tập hoặc thứ tự họ câu sai")
    require(len(set(primary_ids)) == inventory["primary_count"], "ID chính không duy nhất")
    require(len(set(retest_ids)) == inventory["retest_count"], "ID thử lại không duy nhất")
    require(len(set(family_ids)) == inventory["family_count"], "họ câu không duy nhất")

    strands = Counter(item.get("r") for item in items)
    require(list(strands) == inventory["strands"], "thứ tự tám mạch không khớp")
    require(
        all(strands[strand] == inventory["tasks_per_strand"] for strand in inventory["strands"]),
        "một mạch không có đúng ba nhiệm vụ chính",
    )
    required_fields = set(inventory["required_item_fields"])
    for item in items:
        require(required_fields <= set(item), f"{item.get('id')} thiếu trường bắt buộc")
        require(item["retest_id"].startswith(item["id"][:5]), f"{item['id']} ghép sai mạch thử lại")
        require(item["family"] == f"HO-{item['id']}", f"{item['id']} ghép sai họ câu")


def plan_strand_titles() -> dict[str, str]:
    text = PLAN_PATH.resolve().read_text(encoding="utf-8")
    pairs = re.findall(r"^\| \*\*(R[1-8])\. ([^*]+)\*\* \|", text, flags=re.MULTILINE)
    result = dict(pairs)
    require(list(result) == [f"R{index}" for index in range(1, 9)], "không đọc được đủ tám tên mạch từ Kế hoạch 0.6 mục 4.5")
    require("Không đưa số phức hoặc nội dung chương trình cũ vào lõi" in text, "Kế hoạch 0.6 thiếu hàng rào số phức")
    return result


def validate_strand_titles(candidate: dict[str, str], authority: dict[str, str]) -> None:
    require(candidate == authority, "ánh xạ tên mạch không khớp Kế hoạch 0.6 mục 4.5")


def verify_strand_contract(manifest: dict, data: dict) -> None:
    contract = manifest["strand_contract"]
    require(contract["authority_section"] == "4.5", "hợp đồng mạch không trỏ tới mục 4.5")
    require((PACKAGE_ROOT / contract["authority"]).resolve() == PLAN_PATH.resolve(), "nguồn thẩm quyền mạch sai")
    specs = contract["strands"]
    candidate = {strand: spec["title"] for strand, spec in specs.items()}
    authority = plan_strand_titles()
    validate_strand_titles(candidate, authority)

    negative = dict(candidate)
    negative["R5"] = "Số phức"
    rejected = False
    try:
        validate_strand_titles(negative, authority)
    except AssertionError:
        rejected = True
    require(rejected, "fixture âm R5 — Số phức không bị từ chối")

    historical = HISTORICAL_STUDENT_PATH.read_text(encoding="utf-8")
    historical_titles = dict(re.findall(r"^## (R[1-8])\. (.+)$", historical, flags=re.MULTILINE))
    require(list(historical_titles) == list(authority), "baseline học sinh thiếu tiêu đề R1–R8")
    for strand in ("R1", "R2", "R3", "R4", "R5", "R8"):
        require(historical_titles[strand] == authority[strand], f"baseline và Kế hoạch 0.6 lệch tên {strand}")

    for item in data["items"]:
        strand = item["r"]
        require(item["id"].startswith(f"D0-{strand}-"), f"{item['id']} không khớp trường r={strand}")
        observed = set(re.findall(r"B\d{2}", item["clusters"]))
        allowed = set(specs[strand]["allowed_clusters"])
        require(observed <= allowed, f"{item['id']} có cụm ngoài hợp đồng {strand}: {sorted(observed - allowed)}")

    qmd = QMD_PATH.read_text(encoding="utf-8")
    for strand, title in authority.items():
        prefix = f'{strand} — ' if (PROCESS_ROOT / 'dieu_chinh_sau_duyet.json').is_file() else ''
        heading = (f"### {prefix}{title} {{#mach-{strand.lower()}}}" if
                   (PROCESS_ROOT / 'noi_dung_da_duyet.json').is_file() else
                   f"## {strand} — {title} {{#mach-{strand.lower()}}}")
        require(qmd.count(heading) == 1, f"QMD sai tiêu đề {strand}")
    require("Số phức" not in qmd, "QMD còn nhãn Số phức")


def verify_project_files(manifest: dict) -> None:
    config = load_yaml(CONFIG_PATH)
    profile = load_yaml(PROFILE_PATH)
    scaffold = manifest["scaffold"]
    require(scaffold["status"] == "operational_spec_completed_pending_architecture", "trạng thái scaffold sai")
    for key in (
        "project_config", "production_profile", "canonical_data", "migration_checker", "html_checker",
        "migration_generator", "projection_matrix", "html_privacy_filter", "qmd_source",
    ):
        require((PACKAGE_ROOT / scaffold[key]).is_file(), f"thiếu thành phần scaffold: {key}")
    require(scaffold["content_projection"] == "verified", "trạng thái phép chiếu nội dung sai")
    require(scaffold["html_render"] == "architecture_preview_6c", "HTML phải là preview kiến trúc 6C")
    require(scaffold["canonical_pdfs"] == "not_created", "PDF canonical phải còn ở trạng thái chưa tạo")
    require(config["project"]["id"] == "on_thi_d0", "project.id của D0 sai")
    require(
        config["project"]["root"] == "content/thpt/on_thi_toan_thpt/hoc_lieu/d0",
        "project.root của D0 sai",
    )
    require(config["regression"]["articles"] == ["index.qmd"], "regression article sai")
    require(profile["package"]["id"] == "D0", "profile package.id sai")
    require(profile["workflow"]["production"] == "in_production", "production phải là in_production")
    require(profile["workflow"]["publication"] == "pending", "publication phải là pending")
    require(profile["acceptance"]["content_projection"] == "verified", "profile chưa khóa phép chiếu nội dung")
    require(profile["acceptance"]["html_render"] == "architecture_preview_6c", "profile phải ghi preview kiến trúc 6C")
    require(
        profile["acceptance"]["html_visual"] == "rejected_requires_revision",
        "profile không giữ đúng cổng nghiệm thu trực quan HTML",
    )
    require(profile["acceptance"]["pdf_canonical"] == "pending", "PDF canonical không được nâng trạng thái sớm")
    require(QMD_PATH.is_file(), "thiếu khung index.qmd")

    qmd = QMD_PATH.read_text(encoding="utf-8")
    require('title: "Khảo sát và định vị đầu vào"' in qmd, "title QMD sai")
    require("draft: false" in qmd, "ứng viên HTML phải dùng draft: false để render canonical không rỗng")
    require("zo-page-article zo-meta-hidden zo-on-thi-package-page d0-page" in qmd, "body class D0 thiếu")
    require("## Bắt đầu {#bat-dau}" in qmd, "QMD thiếu điểm bắt đầu")
    require("## Khai báo phạm vi {#khai-bao-pham-vi}" in qmd, "QMD thiếu khai báo phạm vi")
    require("## Khảo sát {#khao-sat}" in qmd, "QMD thiếu vùng khảo sát")
    require(".d0-private .d0-facilitator-material" in qmd, "QMD thiếu ranh giới nội bộ")

    contract = CONTRACT_PATH.read_text(encoding="utf-8")
    for invariant in (
        "không được làm lộ lời giải",
        "24 nhiệm vụ chính, 24 câu thử lại và 24 họ câu",
        "Không nới phép so sánh",
    ):
        require(invariant in contract, f"hợp đồng thiếu bất biến: {invariant}")

    require(
        manifest["target_contract"]["canonical_authoring_source"] == "index.qmd",
        "đích nguồn canonical không phải index.qmd",
    )
    require(len(manifest["target_contract"]["pdf_variants"]) == 4, "D0 phải có đúng bốn vai trò PDF dự kiến")


def verify_approved_release_contract(manifest: dict) -> None:
    profile = load_yaml(PROFILE_PATH)
    scaffold = manifest["scaffold"]
    delivery = manifest["target_contract"]["delivery"]
    require(manifest["active_authority"]["html_acceptance"] == "owner_accepted_desktop_mobile_2026_10_03", "HTML chưa khóa nghiệm thu của chủ dự án")
    require(manifest["active_authority"]["content_pdf_delivery"] == "not_required", "D0 phải giữ quyết định không phát hành PDF nội dung")
    require(manifest["package"]["production"] == "accepted", "ứng viên D0 chưa ở trạng thái accepted")
    require(scaffold["status"] == "release_candidate_html_only", "trạng thái ứng viên HTML-only sai")
    require(scaffold["content_pdfs"] == "not_applicable", "PDF nội dung phải ở trạng thái không áp dụng")
    require("canonical_pdfs" not in scaffold, "không được giữ cổng PDF nội dung cũ trong scaffold")
    require(delivery["html"] == {"required": True, "canonical_output": "index.html"}, "hợp đồng đầu ra HTML sai")
    require(delivery["content_pdfs"]["required"] is False, "D0 không được yêu cầu PDF nội dung")
    require(delivery["content_pdfs"]["technical_pdf_assets_remain_canonical_assets"] is True, "phải bảo toàn tài sản PDF kỹ thuật")
    require("pdf_variants" not in manifest["target_contract"], "không được giữ danh sách biến thể PDF nội dung")
    require(profile["workflow"]["production"] == "accepted", "profile chưa khóa production accepted")
    require(profile["workflow"]["publication"] == "pending", "publication chỉ đổi sau khi xuất bản thành công")
    require(profile["acceptance"]["html_visual"] == "owner_accepted_2026_10_03", "profile chưa khóa nghiệm thu HTML")
    require(profile["acceptance"]["pdf_canonical"] == "not_applicable_html_only", "profile còn yêu cầu PDF nội dung")
    qmd = QMD_PATH.read_text(encoding="utf-8")
    front_matter = qmd.split("---", 2)[1]
    require("  html:" in front_matter and "  pdf:" not in front_matter, "QMD phải chỉ khai báo đầu ra HTML")


def verify_editorial_contract(manifest: dict) -> None:
    contract = manifest["target_contract"]["editorial_contract"]
    require(contract["authorization"] == "user_requested_step_6b1", "thiếu phạm vi biên tập Bước 6B.1")
    require(contract["human_content_review"] == "pending", "không tự nâng nghiệm thu nội dung")
    expected_paths = {contract["public_guide"], contract["analysis_guide"], contract["revision_map"], contract["operational_spec"]}
    require(set(contract["files"]) == expected_paths, "inventory nguồn biên tập sai")
    for relative, expected in contract["files"].items():
        require(sha256(PACKAGE_ROOT / relative) == expected, f"nguồn biên tập ngoài bản đã khóa: {relative}")

    stage2 = json.loads((PACKAGE_ROOT / contract["revision_map"]).read_text(encoding="utf-8"))
    revisions = json.loads((PACKAGE_ROOT / stage2["base_revision_map"]).read_text(encoding="utf-8"))
    original = (PACKAGE_ROOT / revisions["historical_source"]).read_text(encoding="utf-8").rstrip() + "\n"
    canonical = (PACKAGE_ROOT / stage2["canonical_source"]).read_text(encoding="utf-8")
    require(stage2["canonical_source"] == contract["analysis_guide"], "sai đích hướng dẫn đã biên tập")
    replacements = {entry["before"]: entry["after"] for entry in revisions["revisions"]}
    require(len(replacements) == len(revisions["revisions"]), "mốc biên tập trùng")
    for before in replacements:
        require(original.count(before) == 1, "mốc biên tập phải có đúng một lần trong bản lịch sử")
    pattern = re.compile("|".join(re.escape(before) for before in replacements))
    expected = pattern.sub(lambda match: replacements[match.group(0)], original)
    replacements2 = {entry["before"]: entry["after"] for entry in stage2["revisions"]}
    require(len(replacements2) == len(stage2["revisions"]), "mốc biên tập Bước 6B.1 trùng")
    for before in replacements2:
        require(expected.count(before) == 1, "mốc Bước 6B.1 phải có đúng một lần trong bản Bước 6B")
    pattern2 = re.compile("|".join(re.escape(before) for before in replacements2))
    expected = pattern2.sub(lambda match: replacements2[match.group(0)], expected)
    require(canonical == expected, "hướng dẫn có sai biệt ngoài danh sách biên tập Bước 6B và 6B.1")
    require("Kế hoạch 0.5" not in canonical and "lộ trình 0.5" not in canonical, "hướng dẫn còn dùng kế hoạch cũ")
    require("B.8, tuần 16–17 là tọa độ không gian Oxyz" in canonical, "thiếu đính chính B.8 theo Kế hoạch 0.6")

    public = (PACKAGE_ROOT / contract["public_guide"]).read_text(encoding="utf-8")
    require("D0" not in public, "hướng dẫn công khai còn mã quản lý D0")
    spec = load_yaml(PACKAGE_ROOT / contract["operational_spec"])
    require(spec["package"] == "d0" and spec["role"]["not_a_lesson"] is True, "đặc tả chưa khóa vai trò D0")
    require(spec["boundaries"]["route_independent_of_delivery_readiness"] is True, "tuyến còn phụ thuộc tình trạng sản xuất")
    require(len(spec["route_catalog"]) == 9, "đặc tả phải bao phủ B.1-B.9")
    require(len(spec["required_scenarios"]) == 5, "đặc tả thiếu tình huống vận hành")
    actual = QMD_PATH.read_text(encoding="utf-8")
    require('subtitle: "Xác định việc cần ôn trước"' in actual, "phụ đề công khai sai")
    labels = re.findall(r"\[Bài (\d{2})\]\{\.d0-task-number\} \[(R[1-8])\]\{\.d0-task-code\}", actual)
    require(labels == [(f"{item['n']:02d}", item["r"]) for item in json.loads(CANONICAL_DATA_PATH.read_text(encoding="utf-8"))["items"]], "nhãn công khai không khớp nhiệm vụ")
    require(not re.search(r"\[D0-[^\]]+\]\{\.d0-task-code\}", actual), "mã quản lý còn hiển thị ở đề bài")
    candidate = manifest["target_contract"]["html_candidate"]
    require(candidate["status"] == "stale_after_editorial_revision", "HTML cũ chưa bị loại khỏi ứng viên hiện hành")
    require(candidate["visual_review"] == "rejected_requires_revision", "thiếu kết luận HTML chưa đạt")


def verify_content_projection(manifest: dict, data: dict) -> None:
    actual = QMD_PATH.read_text(encoding="utf-8")
    expected = build_qmd()
    require(actual == expected, "index.qmd không khớp toàn chuỗi với phép chiếu D0 v1.0")
    sign_data = json.loads((PACKAGE_ROOT / 'du_lieu/bang_bien_thien.json').read_text(encoding='utf-8'))
    source = next(item['question'] for item in data['items'] if item['id'] == 'D0-R1-03')
    lines = [line for line in source.splitlines() if line.startswith('|')]
    require(len(lines) == 3, 'nguồn bảng dấu đã thay đổi cấu trúc')
    cells = [[cell.strip().strip('$') for cell in line.strip('|').split('|')] for line in (lines[0], lines[2])]
    require(cells[0] == ['x', r'(-\infty;-2)', '-2', '(-2;1)', '1', r'(1;+\infty)'], 'mốc và khoảng bảng dấu nguồn đã thay đổi')
    signs = cells[1][1:]
    expected_rows = [['x', '−∞', '', '−2', '', '1', '', '+∞'],
                     ['f′(x)', '', signs[0].replace('-', '−'), signs[1], signs[2], signs[3], signs[4], '']]
    require(len(sign_data) == 1 and sign_data[0]['rows'] == expected_rows, 'bảng dấu vector không khớp mốc/dấu nguồn độc lập')
    require('bbt="BBT01"' in actual, 'QMD thiếu component bảng dấu canonical')
    for relative, expected_hash in manifest['target_contract']['variation_assets_6d'].items():
        require(sha256(PACKAGE_ROOT / relative) == expected_hash, f'tài sản bảng dấu ngoài bản khóa 6D: {relative}')

    inventory = manifest["inventory"]
    require(
        len(re.findall(r"<!-- D0_PRIMARY_START D0-R[1-8]-\d{2} -->", actual))
        == inventory["primary_count"],
        "sai số khối nhiệm vụ chính trong QMD",
    )
    require(
        len(re.findall(r"<!-- D0_PRIVATE_RECORD_START D0-R[1-8]-\d{2} -->", actual))
        == inventory["primary_count"],
        "sai số hồ sơ nội bộ trong QMD",
    )
    for item in data["items"]:
        primary_anchor = f'#{item["id"].lower()}'
        retest_anchor = f'#{item["retest_id"].lower()}'
        require(actual.count(primary_anchor) == 1, f"anchor nhiệm vụ chính sai: {primary_anchor}")
        require(actual.count(retest_anchor) == 1, f"anchor thử lại sai: {retest_anchor}")
        require(actual.count(f'd0-family="{item["family"]}"') == 3, f"quan hệ họ câu sai: {item['id']}")

    for field in (*PUBLIC_FIELDS, *PRIVATE_FIELDS):
        require(field in manifest["inventory"]["required_item_fields"], f"trường chưa có phép chiếu: {field}")
    require(set(PUBLIC_FIELDS) | set(PRIVATE_FIELDS) == set(manifest["inventory"]["required_item_fields"]),
            "ma trận phép chiếu không bao phủ đúng 30 trường")
    require(r"\boxed{" not in actual, "QMD còn dùng \\boxed")
    require("(src/hinh_hop.pdf)" not in actual, "QMD còn tham chiếu tài nguyên lịch sử")
    require("(hinh/hinh_hop.pdf)" in actual, "QMD thiếu tài nguyên hình hộp canonical")

    lua = LUA_PATH.read_text(encoding="utf-8")
    require("html and div.classes:includes('d0-private')" in lua, "Lua chưa nhận diện vùng riêng tư HTML")
    require("return {}" in lua, "Lua chưa xóa vùng riêng tư khỏi AST HTML")
    require("display: none" not in lua and "visibility" not in lua, "không được che lời giải bằng CSS")

    matrix = PROJECTION_MATRIX_PATH.read_text(encoding="utf-8")
    for phrase in ("30 trường bắt buộc", "xóa `Div` này khỏi cây tài liệu", "hinh/hinh_hop.pdf"):
        require(phrase in matrix, f"ma trận phép chiếu thiếu hợp đồng: {phrase}")

    geometry_toolchain = manifest["target_contract"]["geometry_toolchain"]
    require(set(geometry_toolchain) == {"compiler", "checker", "style"}, "sai inventory công cụ hình học")
    for role, contract in geometry_toolchain.items():
        tool_path = REPO_ROOT / contract["path"]
        require(tool_path.is_file(), f"thiếu thành phần công cụ hình học: {role}")
        require(sha256(tool_path) == contract["sha256"], f"hash công cụ hình học sai: {role}")

    canonical_assets = manifest["target_contract"]["canonical_assets"]
    expected_assets = {
        "hinh_hop.pdf",
        "hinh_hop.png",
        "hinh_hop.svg",
        "hinh_hop.tex",
        "hinh_hop.geometry.json",
    }
    require(set(canonical_assets) == expected_assets, "sai inventory tài nguyên canonical")
    for filename, contract in canonical_assets.items():
        target = ASSET_ROOT / filename
        require(target.is_file(), f"thiếu tài nguyên canonical: {filename}")
        require(sha256(target) == contract["sha256"], f"hash tài nguyên canonical sai: {filename}")
        source = PACKAGE_ROOT / contract["source"]
        require(source.is_file(), f"thiếu nguồn tài nguyên canonical: {contract['source']}")
        require(sha256(source) == contract["source_sha256"], f"hash nguồn tài nguyên canonical sai: {filename}")
        expected_replacement = filename in {"hinh_hop.pdf", "hinh_hop.png"}
        require(
            contract.get("replaces_historical_asset") is expected_replacement,
            f"sai khai báo quan hệ với tài nguyên lịch sử: {filename}",
        )


def verify_legacy_math_checker() -> None:
    historical_checker = BASELINE_ROOT / "kiem_chung" / "kiem_tra_toan.py"
    require(historical_checker.is_file(), "thiếu checker toán lịch sử")
    with tempfile.TemporaryDirectory(prefix="zo-d0-check-") as temp_dir:
        isolated = Path(temp_dir) / "v1_0"
        shutil.copytree(BASELINE_ROOT, isolated)
        result = subprocess.run(
            [sys.executable, str(isolated / "kiem_chung" / "kiem_tra_toan.py")],
            cwd=isolated,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        require(result.returncode == 0, "checker toán lịch sử thất bại trong bản sao cô lập")
        combined = result.stdout + result.stderr
        require("48/48" in combined or "48 nhiệm vụ" in combined, "checker toán không xác nhận inventory 48 nhiệm vụ")


def main() -> int:
    manifest = load_yaml(MANIFEST_PATH)
    require(manifest.get("schema_version") == 1, "schema manifest không được hỗ trợ")
    require(manifest["package"]["id"] == "d0", "manifest không thuộc gói d0")

    verify_original_manifest(manifest)
    verify_classification(manifest)

    baseline_data_path = BASELINE_ROOT / "D0_ngan_hang_v1.0.json"
    require(CANONICAL_DATA_PATH.is_file(), "thiếu dữ liệu canonical")
    require(
        CANONICAL_DATA_PATH.read_bytes() == baseline_data_path.read_bytes(),
        "dữ liệu canonical không còn là bản sao byte của baseline v1.0",
    )
    data = json.loads(CANONICAL_DATA_PATH.read_text(encoding="utf-8"))
    verify_inventory(manifest, data)
    verify_strand_contract(manifest, data)
    if (PROCESS_ROOT / 'noi_dung_da_duyet.json').is_file():
        from kiem_chung_da_duyet import verify_source
        verify_approved_release_contract(manifest)
        verify_source()
        verify_legacy_math_checker()
        print('PASS: approved QMD source fingerprint; 25 immutable historical files; bank byte equality; 24 tasks/24 retests/24 families; Plan 0.6 strand mapping and negative fixture; historical math checker 48/48. Publication pending.')
        return 0
    verify_project_files(manifest)
    verify_editorial_contract(manifest)
    verify_content_projection(manifest, data)
    verify_legacy_math_checker()

    print("D0 full content projection: PASS")
    print("25 baseline files classified and hash-verified")
    print("8 strands | 24 primary tasks | 24 retest tasks | 24 unique families")
    print("strand authority: Plan 0.6 section 4.5 | negative R5 complex-number fixture: PASS")
    print("canonical data equals baseline JSON byte-for-byte")
    print("legacy math checker: PASS in isolated temporary copy")
    print("QMD full-sequence projection: PASS | HTML privacy: AST removal contracted")
    print("Step 6B.1 operational role, route contract, source hashes and revision maps: PASS")
    print("render status: HTML architecture preview 6C; visual review pending | PDF: pending | publication: pending")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"D0 migration foundation: FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
