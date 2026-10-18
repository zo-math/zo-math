"""Required package-owned, approved cover binding; no default image."""
from pathlib import Path
import hashlib
import json
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup

BASE = Path("content/thpt/on_thi_toan_thpt/hoc_lieu")

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_cover(root, package, *, allow_direction_approved=False):
    root = Path(root).resolve()
    if Path(package).name != package or package in {".", ".."}:
        raise ValueError("Invalid package identity")
    folder = root / BASE / package
    record = json.loads((folder / "giao_dien/anh_bia.json").read_text(encoding="utf-8"))
    if record.get("schema_version") != 1 or record.get("package") != package:
        raise ValueError("Cover declaration belongs to another package")
    allowed = record.get("approval") == "approved" or (allow_direction_approved and record.get("approval") == "direction_approved" and record.get("image_acceptance") == "pending_owner_review")
    if not allowed or not all(str(record.get(k, "")).strip() for k in ["selection_reason", "approval_evidence"]):
        raise ValueError("Cover needs selection rationale and explicit approval evidence")
    image = (folder / record["image"]).resolve()
    if not image.is_relative_to(folder.resolve()) or not image.is_file():
        raise ValueError("Cover must be an existing source asset owned by this package")
    if digest(image) != record.get("sha256"):
        raise ValueError("Cover differs from the approved image; review before rendering")
    # Renaming or copying another package's picture must not evade ownership.
    for other in (root / BASE).glob("*/giao_dien/anh_bia.json"):
        if other.parent.parent.name == package:
            continue
        data = json.loads(other.read_text(encoding="utf-8"))
        if data.get("sha256") == record["sha256"]:
            raise ValueError("Cover duplicates another package's declared image")
    return image

def check_html(root, package, html_path, *, allow_direction_approved=False):
    expected = load_cover(root, package, allow_direction_approved=allow_direction_approved)
    html_path = Path(html_path)
    doc = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    images = doc.select(".hero-art img")
    if len(images) != 1:
        raise ValueError("Package HTML must display exactly one declared cover")
    url = urlsplit(images[0].get("src", ""))
    if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
        raise ValueError("Package cover must use a local generated asset")
    actual = (html_path.parent / unquote(url.path)).resolve()
    if not actual.is_file() or digest(actual) != digest(expected):
        raise ValueError("Rendered HTML does not display this package's approved cover")
    return True
