from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
import yaml


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = next(parent for parent in PACKAGE_ROOT.parents if (parent / ".git").exists())
HTML_PATH = REPO_ROOT / "docs" / PACKAGE_ROOT.relative_to(REPO_ROOT) / "index.html"
DATA_PATH = PACKAGE_ROOT / "du_lieu" / "ngan_hang.json"
SOURCE_CSS = PACKAGE_ROOT / "giao_dien" / "d0.css"
OUTPUT_CSS = HTML_PATH.parent / "giao_dien" / "d0.css"
MANIFEST_PATH = PACKAGE_ROOT / "_quy_trinh" / "manifest_chuyen_doi.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if (PACKAGE_ROOT / '_quy_trinh/noi_dung_da_duyet.json').is_file():
        from kiem_chung_da_duyet import verify_html
        verify_html()
        return 0
    require(HTML_PATH.is_file(), "thiếu HTML D0 đã render")
    raw = HTML_PATH.read_text(encoding="utf-8")
    require(len(raw) > 50_000, "HTML quá nhỏ; có thể đã render trang draft rỗng")
    soup = BeautifulSoup(raw, "html.parser")
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))

    html_candidate = manifest["target_contract"]["html_candidate"]
    architecture_only = sys.argv[1:] == ["--architecture-only"]
    require(not sys.argv[1:] or architecture_only, "tham số checker không hợp lệ")
    if not architecture_only:
        require(html_candidate["status"] == "locked_pending_user_review", "HTML candidate chưa được khóa để nghiệm thu")
    for relative, expected_hash in (html_candidate["files"].items() if not architecture_only else []):
        candidate_file = REPO_ROOT / relative
        require(candidate_file.is_file(), f"thiếu tệp HTML candidate: {relative}")
        require(sha256(candidate_file) == expected_hash, f"hash HTML candidate sai: {relative}")

    body = soup.body
    require(body is not None and "d0-page" in body.get("class", []), "body thiếu lớp d0-page")
    require(len(soup.select(".zo-on-thi-package.d0-package")) == 1, "sai số root package D0")
    require(len(soup.select(".d0-primary-task")) == 24, "HTML không có đúng 24 nhiệm vụ chính")
    require(len(soup.select(".d0-task-number")) == 24, "HTML không có đúng 24 số thứ tự nhiệm vụ")
    require(len(soup.select(".d0-task-code")) == 24, "HTML không có đúng 24 mã nhiệm vụ")
    require(len(soup.select(".d0-task-meta")) == 24, "HTML không có đúng 24 vùng metadata nhẹ")
    require(len(soup.select(".d0-task-prompt")) == 24, "HTML không có đúng 24 vùng đề bài")
    require(len(soup.select('section[id^="mach-r"]')) == 8, "HTML không có đúng tám mạch")
    for strand, spec in manifest["strand_contract"]["strands"].items():
        heading = soup.select_one(f"#khao-sat #mach-{strand.lower()} > h3")
        require(heading is not None, f"HTML thiếu tiêu đề {strand}")
        require(heading.get_text(" ", strip=True) == f"{strand} — {spec['title']}", f"HTML sai tiêu đề {strand}")
    require("Số phức" not in soup.get_text(" ", strip=True), "HTML còn nhãn Số phức")
    require(len(soup.select('#khao-sat .d0-primary-task')) == 24, "nhiệm vụ bị tách khỏi thẻ Khảo sát")
    require(soup.select_one('#khai-bao-pham-vi table') is not None, "thiếu phiếu khai báo")
    require(len(soup.select('#doc-ket-qua table')) == 2, "thiếu mẫu hồ sơ hoặc bản đồ tuyến")
    require(len(soup.select('#khao-sat .d0-data-table table.r1-data-table')) == 4, 'sai inventory bốn bảng dữ liệu trong đề')
    require(len(soup.select('.d0-data-table table.r1-data-table')) == 7, 'bảng thường chưa áp dụng đầy đủ component canonical')
    require(len(soup.select('#d0-r1-03 .zo-variation-asset img[src="hinh/bbt01.svg"]')) == 1, 'bảng dấu chưa dùng SVG canonical')
    require(sha256(HTML_PATH.parent / 'hinh/bbt01.svg') == sha256(PACKAGE_ROOT / 'hinh/bbt01.svg'), 'bảng dấu SVG đầu ra lỗi thời')
    sign_rows = soup.select('#d0-r1-03 table.variation tr')
    require([[cell.get_text(strip=True) for cell in row.select('th,td')] for row in sign_rows] ==
            [['x', '−∞', '', '−2', '', '1', '', '+∞'], ['f′(x)', '', '−', '0', '+', '0', '+', '']], 'bảng dấu trợ năng sai mốc hoặc dấu')

    identifiers = [tag["id"] for tag in soup.select("[id]")]
    require(len(identifiers) == len(set(identifiers)), "HTML có ID trùng")
    for tag in soup.find_all(src=True) + soup.find_all(href=True):
        raw_reference = tag.get("src") or tag.get("href")
        parsed = urlsplit(raw_reference)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        decoded = unquote(parsed.path)
        local_target = (REPO_ROOT / "docs" / decoded.lstrip("/")) if decoded.startswith("/") else (HTML_PATH.parent / decoded)
        require(local_target.resolve().is_file(), f"HTML liên kết tệp cục bộ không tồn tại: {raw_reference}")
    for item in data["items"]:
        require(soup.find(id=item["id"].lower()) is not None, f"thiếu nhiệm vụ chính {item['id']}")

    require(not soup.select(".d0-private"), "HTML còn khối d0-private")
    require("D0_PRIVATE_RECORD_START" not in raw, "HTML còn marker hồ sơ nội bộ")
    require("Dành cho người hướng dẫn" not in raw, "HTML còn tiêu đề dành cho người hướng dẫn")
    for item in data["items"]:
        require(item["retest_id"] not in raw, f"HTML làm lộ ID thử lại {item['retest_id']}")
        for field in ("solution", "retest", "resolution", "error", "repair"):
            value = item[field]
            if len(value) >= 40:
                require(value not in raw, f"HTML làm lộ trường {field} của {item['id']}")

    require(not soup.select('embed[src="hinh/hinh_hop.pdf"], iframe[src="hinh/hinh_hop.pdf"], object[data="hinh/hinh_hop.pdf"]'), "HTML còn nhúng trình đọc PDF cho hình hộp")
    figures = soup.select('#khao-sat img[src="hinh/hinh_hop.svg"]')
    require(len(figures) == 1, "HTML phải có đúng một hình hộp SVG canonical")
    require('width' not in figures[0].get('style', ''), "hình SVG còn kích thước inline ghi đè tỉ lệ chữ")
    require(sha256(HTML_PATH.parent / 'hinh' / 'hinh_hop.svg') == sha256(PACKAGE_ROOT / 'hinh' / 'hinh_hop.svg'), "SVG đầu ra khác tài sản canonical")

    css_hrefs = [tag.get("href") for tag in soup.find_all("link", rel="stylesheet")]
    require("giao_dien/d0.css" in css_hrefs, "HTML chưa nạp CSS riêng D0")
    require(OUTPUT_CSS.is_file(), "đầu ra thiếu CSS riêng D0")
    require(sha256(OUTPUT_CSS) == sha256(SOURCE_CSS), "CSS đầu ra không đồng bộ nguồn")
    css = SOURCE_CSS.read_text(encoding="utf-8")
    for contract in (".d0-primary-task", "@media (max-width: 640px)", "overflow-x: auto"):
        require(contract in css, f"CSS thiếu hợp đồng responsive: {contract}")
    nav_rule = re.search(r"\.d0-nav-slot\s*\{([^}]*)\}", css, flags=re.DOTALL)
    require(nav_rule is not None, "CSS thiếu quy tắc d0-nav-slot")
    require("position: sticky" in nav_rule.group(1), "thanh điều khiển D0 phải còn truy cập được khi cuộn")
    require(re.search(r"\btop\s*:\s*0\s*;", nav_rule.group(1)) is not None,
            "thanh điều khiển D0 phải bám sát đầu viewport, không chừa khoảng Navbar giả")
    require("d0-nav-slot" in raw and "d0-view-panel" in raw, "HTML thiếu script điều hướng riêng D0")
    require("r1-section-nav" not in raw, "HTML còn dùng script điều hướng R1 không tương thích")

    require(not re.search(r"(?:src|href)=['\"](?:\.\./)*_quy_trinh/", raw), "HTML liên kết tài liệu nội bộ")
    print("D0 HTML architecture: PASS (not final acceptance)" if architecture_only else "D0 HTML candidate: PASS")
    print("24 public tasks | 8 strands | 0 private blocks | 0 retest IDs")
    print("package CSS and canonical image assets: PASS")
    print(f"HTML: {HTML_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"D0 HTML candidate: FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
