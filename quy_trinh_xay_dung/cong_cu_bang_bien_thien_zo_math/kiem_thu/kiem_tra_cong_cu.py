"""Kiểm thử hợp đồng dữ liệu của công cụ bảng biến thiên."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


TOOL = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("zo_variation_build", TOOL / "zo_variation_build.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def expect_error(data, message):
    with tempfile.TemporaryDirectory(prefix="zo_variation_test_") as raw:
        path = Path(raw) / "data.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        try:
            module.load_data(path)
        except module.VariationError:
            return
        raise AssertionError(message)


valid = [{
    "id": "T01", "title": "Bảng biến thiên",
    "rows": [["x", "−∞", "", "0", "", "+∞"],
             ["f′(x)", "", "−", "0", "+", ""],
             ["f(x)", "+∞", "↘", "0", "↗", "+∞"]]
}]
with tempfile.TemporaryDirectory(prefix="zo_variation_test_") as raw:
    path = Path(raw) / "valid.json"
    path.write_text(json.dumps(valid, ensure_ascii=False), encoding="utf-8")
    assert len(module.load_data(path)) == 1

bad_order = json.loads(json.dumps(valid, ensure_ascii=False))
bad_order[0]["rows"][0] = ["x", "−∞", "", "2", "", "1"]
expect_error(bad_order, "Không phát hiện thứ tự mốc sai")

bad_sign = json.loads(json.dumps(valid, ensure_ascii=False))
bad_sign[0]["rows"][2][2] = "↗"
expect_error(bad_sign, "Không phát hiện mâu thuẫn dấu–chiều")

intentional = json.loads(json.dumps(bad_sign, ensure_ascii=False))
intentional[0]["intentional_error"] = True
with tempfile.TemporaryDirectory(prefix="zo_variation_test_") as raw:
    path = Path(raw) / "intentional.json"
    path.write_text(json.dumps(intentional, ensure_ascii=False), encoding="utf-8")
    module.load_data(path)

with_width = json.loads(json.dumps(valid, ensure_ascii=False))
with_width[0]["column_min_widths_mm"] = {"3": 30}
with tempfile.TemporaryDirectory(prefix="zo_variation_test_") as raw:
    path = Path(raw) / "with_width.json"
    path.write_text(json.dumps(with_width, ensure_ascii=False), encoding="utf-8")
    record = module.load_data(path)[0]
    tex = module.make_tex(record)
    assert "|[minimum width=30mm]|" in tex
    assert "bbt-1-4.west" in tex and "bbt-1-4.east" in tex

bad_width = json.loads(json.dumps(valid, ensure_ascii=False))
bad_width[0]["column_min_widths_mm"] = {"3": 4}
expect_error(bad_width, "Không phát hiện chiều rộng cột ngoài giới hạn")

print("ĐẠT: schema, thứ tự mốc, chiều rộng cột, mâu thuẫn dấu–chiều và ngoại lệ có chủ ý.")
