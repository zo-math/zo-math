"""QD_025 source inventory and application-map gate; never edits learner sources.

This is not the production renderer or a mathematical/visual acceptance gate.
Explicit annotations identify semantic units; CSS/heading counts cannot do so.
Reports are rebuilt from current canonical QMD, includes and the manifest.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
from zo_learning_architecture import COMMON_CATALOG, SCHEMA_PATH, REPO_ROOT, load_yaml

ANCHOR = re.compile(r"\{[^}\n]*#([^\s}]+)[^}\n]*\}")
HEADING = re.compile(r"^(#{1,6})\s+(.+)")
INCLUDE = re.compile(r"\{\{<\s*include\s+(.+?)\s*>\}\}")


def relative(path):
    return path.relative_to(REPO_ROOT).as_posix()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(value):
    return re.sub(r"\s*\{[^}]*\}\s*$", "", value).strip()


def repository_path(base, value):
    path = (base / value).resolve()
    if not path.is_relative_to(REPO_ROOT) or ".git" in path.parts:
        raise ValueError("Path outside repository: " + value)
    return path


def validate_catalog(catalog):
    contract = catalog.get("label_contract", {})
    if contract.get("version") != 1 or contract.get("decision") != "QD_025" or contract.get('scope') != 'all_program_packages_2027':
        raise ValueError("Unsupported label contract/decision")
    terms = contract.get("terms", {})
    if not terms:
        raise ValueError("Empty label dictionary")
    names = set()
    for key, term in terms.items():
        system = term.get("system")
        if system not in ("architecture", "content_type", "function") or not term.get("scope"):
            raise ValueError("Invalid term: " + key)
        identity = (system, term.get("name"))
        if not identity[1] or identity in names:
            raise ValueError("Duplicate/empty term name: " + key)
        names.add(identity)
        if system == "architecture":
            parent, visited = term.get("parent"), {key}
            while parent:
                if parent not in terms or terms[parent].get("system") != "architecture" or parent in visited:
                    raise ValueError("Invalid structural parent/cycle: " + key)
                visited.add(parent)
                parent = terms[parent].get("parent")
        if system == "function" and not set(term.get("roles", [])) <= set(catalog["valid_task_roles"]):
            raise ValueError("Unknown task role: " + key)
        if term.get("aliases"):
            raise ValueError("Aliases require an explicitly approved migration; none in version 1")
    return terms


def validate_application(data, schema, terms):
    # The migration map has its own closed schema; live manifest stays version 1/0.2.
    import jsonschema
    try:
        jsonschema.Draft202012Validator({"$ref": "#/$defs/label_application", "$defs": schema["$defs"]}).validate(data)
    except jsonschema.ValidationError as exc:
        raise ValueError("label_application schema: " + exc.message) from exc
    if data["package_id"] != "R1-G01":
        raise ValueError("Version 1 implements the G01 migration map only; other packages require their own integration")
    for field, system in (("areas", "architecture"), ("groups", "architecture"),
                          ("class_types", "content_type"), ("task_functions", "function")):
        for key in data[field].values():
            if key not in terms or terms[key]["system"] != system:
                raise ValueError("Unknown/wrong-system term: " + key)
    if data["warmup"]["function"] != "function.warmup":
        raise ValueError("Warmup function drift")
    if data["areas"].get("tu-kiem-tra") != "area.test":
        raise ValueError("Legacy test ID must not become lesson self-check")
    if terms["area.foundation"].get("parent") is not None:
        raise ValueError("Foundation must be an independent area")
    for unit in data["knowledge_units"]:
        if unit["type"] not in terms or terms[unit["type"]]["system"] != "content_type":
            raise ValueError("Invalid knowledge unit type")
    for role, function in data["task_functions"].items():
        if role not in terms[function]["roles"]:
            raise ValueError("Task role/function mismatch: " + role)


def read_sources(source):
    files, placements, lines = {}, [], []
    def visit(path, stack):
        if path in stack:
            raise ValueError("Include cycle: " + relative(path))
        text = path.read_text(encoding="utf-8")
        files[relative(path)] = sha(path)
        for number, line in enumerate(text.splitlines(), 1):
            include = INCLUDE.search(line)
            if include:
                target = repository_path(path.parent, include.group(1))
                placements.append({"source": relative(target), "called_from": relative(path), "line": number})
                visit(target, stack + [path])
            else:
                lines.append({"path": relative(path), "line": number, "text": line})
    visit(source, [])
    return files, placements, lines


def build_inventory(data, base):
    applied = data['status'] == 'source_applied_pending_html_acceptance'
    binding_path = repository_path(base, '../giao_dien/he_nhan.json')
    bindings = json.loads(binding_path.read_text(encoding='utf-8')) if applied else None
    unit_bindings = {u['question']: u for u in bindings['units']} if applied else {}
    source = repository_path(base, data["source"])
    manifest_path = repository_path(base, data["manifest"])
    manifest = load_yaml(manifest_path)
    if manifest["package"]["id"] != data["package_id"]:
        raise ValueError("Package/manifest mismatch")
    files, includes, lines = read_sources(source)
    files[relative(manifest_path)] = sha(manifest_path)
    rows, references, assets, ids, components = [], [], [], {}, []
    variations = []
    if data.get("variation_source"):
        variation_path = repository_path(base, data["variation_source"])
        files[relative(variation_path)] = sha(variation_path)
        variations = json.loads(variation_path.read_text(encoding="utf-8"))
    for value in data.get("presentation_bindings", []):
        binding_path = repository_path(base, value)
        files[relative(binding_path)] = sha(binding_path)
    stack, current_foundation = [], None
    fence_stack = []
    def add(row):
        row.setdefault("source_applied", applied)
        row.setdefault("approval", "source_applied_html_review_pending" if applied else "pending_package_approval")
        rows.append(row)
        return row
    for item in lines:
        text = item["text"]
        heading = HEADING.match(text)
        anchors = ANCHOR.findall(text)
        fence_parent = next((f["anchor"] for f in reversed(fence_stack) if f["anchor"]), None)
        source_parent = fence_parent or (stack[-1][1] if stack else None)
        if heading:
            level = len(heading.group(1))
            stack = [h for h in stack if h[0] < level]
            anchor = anchors[0] if anchors else None
            parent = stack[-1][1] if stack else None
            title = clean(heading.group(2))
            row = add(dict(item, kind="heading", anchor=anchor, parent=parent,
                           area=next((data["areas"][h[1]] for h in reversed(stack) if h[1] in data["areas"]), None),
                           title=title, proposed_title=data["title_proposals"].get(anchor, title),
                           structural_label=data["areas"].get(anchor, data["groups"].get(anchor)),
                           content_type=None, function=None, number=None))
            stack.append((level, anchor))
            if anchor:
                if anchor in ids:
                    raise ValueError("Duplicate ID: " + anchor)
                ids[anchor] = row
            current_foundation = None
        elif anchors:
            for anchor in anchors:
                classes = re.findall(r"(?<!\w)\.([\w-]+)", text)
                types = [data["class_types"][c] for c in classes if c in data["class_types"]]
                if "r1-foundation-unit" in classes:
                    current_foundation = anchor
                    types = []  # compatibility class zo-learning-hint is not a hint unit
                row = add(dict(item, kind="anchor", anchor=anchor,
                               parent=current_foundation if anchor != current_foundation else "on-nen",
                               area="area.foundation" if current_foundation else next((data["areas"][h[1]] for h in reversed(stack) if h[1] in data["areas"]), None),
                               title="", proposed_title=data["title_proposals"].get(anchor, ""),
                               structural_label=None, content_type=types[0] if types else None,
                               function=None, number=None))
                if not current_foundation:
                    row["parent"] = source_parent
                if anchor in ids:
                    raise ValueError("Duplicate ID: " + anchor)
                ids[anchor] = row
        # Anonymous semantic wrappers are placements, never extra semantic counts.
        if "{" in text and not anchors:
            classes = re.findall(r"(?<!\w)\.([\w-]+)", text)
            types = [data["class_types"][c] for c in classes if c in data["class_types"]]
            if types:
                add(dict(item, kind="semantic_placement", anchor=None, parent=current_foundation or source_parent,
                         area="area.foundation" if current_foundation else next((data["areas"][h[1]] for h in reversed(stack) if h[1] in data["areas"]), None),
                         title="", proposed_title="", content_type=types[0], function=None, number=None,
                         classification="placement_not_distinct_unit"))
        if re.match(r"^:{3,}\s+\S", text):
            fence_stack.append({"anchor": anchors[0] if anchors else None})
        elif re.match(r"^:{3,}\s*$", text) and fence_stack:
            closed = fence_stack.pop()
            if closed["anchor"] == current_foundation:
                current_foundation = None
        reference_owner = next((f["anchor"] for f in reversed(fence_stack) if f["anchor"]), None) or (stack[-1][1] if stack else None)
        bbt = re.search(r'\bbbt="([^"]+)"', text)
        if bbt:
            definition = next((v for v in variations if v["id"] == bbt.group(1)), None)
            if definition is None:
                raise ValueError("Native BBT has no canonical data: " + bbt.group(1))
            components.append(dict(item, kind="native_variation_table", id=bbt.group(1), parent=reference_owner,
                                   canonical_definition=definition, classification="component_not_semantic_unit"))
        for label, target in re.findall(r"\[([^\]\n]*)\]\(#([^\s)]+)\)", text):
            references.append(dict(item, label=label, target=target, from_anchor=reference_owner))
        for target in re.findall(r"!?\[[^\]\n]*\]\(([^\s)#]+\.(?:svg|png|jpg|pdf|wav|mp4))\)", text):
            path = repository_path((REPO_ROOT / item["path"]).parent, target)
            assets.append(dict(item, target=target, exists=path.is_file(), sha256=sha(path) if path.is_file() else None))
    def get(anchor):
        if anchor not in ids:
            raise ValueError("Missing source selector: " + str(anchor))
        return ids[anchor]
    def locate(path, prefix, parent, unit_key, content_type, **values):
        candidates = [l for l in lines if l["path"] == path and l["text"].startswith(prefix)]
        if len(candidates) != 1:
            raise ValueError(f"Locator not unique: {path} / {prefix}: {len(candidates)}")
        return add(dict(candidates[0], kind="semantic_unit", anchor=None, parent=parent,
                        unit_key=unit_key, title=prefix.strip("*- ."), proposed_title="", content_type=content_type,
                        function=None, number=None, **values))
    for anchor, label in data["areas"].items():
        get(anchor)["area"] = label
    for anchor in data["groups"]:
        group = data["groups"][anchor]
        get(anchor)["proposed_owner"] = {"group.study_guide": "area.start", "group.warmup": "area.lesson"}.get(group, "area.remediation")
    # Manifest is sole owner of task meaning, objectives, exposure and routing.
    tasks = []
    for task in manifest["tasks"]:
        row = get(task["source_anchor"])
        answer = get(task["answer_anchor"])
        role = task["role"]
        function = data["task_functions"].get(role)
        if not function:
            raise ValueError("Task role has no explicit function binding: " + role)
        row.update(content_type="type.task", function=function, task=copy.deepcopy(task), unit_key=task["id"])
        row["area"] = {"L": "area.practice", "K": "area.test", "O": "area.review"}.get(role, "area.remediation")
        row["proposed_owner"] = row["area"]
        if role == "K":
            points = re.search(r"(\d+) điểm", row["title"])
            if applied:
                section = '\n'.join(l['text'] for l in lines if l['path'] == relative(source) and row['line'] < l['line'] < row['line'] + 5)
                points = re.search(r'(\d+) điểm', section)
            if not points:
                raise ValueError("Test score missing in source heading")
            row["secondary_info"] = {"points": int(points.group(1)), "placement": "metadata_not_title"}
        answer.update(content_type="type.solution", unit_key="answer:" + task["id"], answer_of=task["id"], function=function,
                      proposed_title=data["title_proposals"].get(task["source_anchor"], row["title"]),
                      source_group=row["area"])
        tasks.append(row)
    # Whole-group numbering, not per stage/round; S numbering is a proposal.
    counters = Counter()
    for row in sorted(tasks, key=lambda r: r["line"]):
        counters[row["function"]] += 1
        row["number"] = counters[row["function"]]
        if applied:
            binding = unit_bindings[row['anchor']]
            if binding['number'] != row['number'] or binding['title'] != row['title']:
                raise ValueError('Source title/whole-group number differs from binding: ' + row['anchor'])
            row['proposed_title'] = binding['title']
        elif row["anchor"] not in data["title_proposals"]:
            row["proposed_title"] = "Nhiệm vụ " + f'{row["number"]:02}' + " – " + re.sub(r"^(Bài )?(luyện tập|kiểm tra|Ôn lại|Sửa lỗi|sửa lỗi).*?(?:\. | — | – )", "", row["title"], flags=re.I)
        row["proposed_title"] = re.sub(r"\s*[—–-]\s*\d+ điểm$", "", row["proposed_title"])
        get(row["task"]["answer_anchor"]).update(proposed_title=row["proposed_title"], number=row["number"])
    warmup = data["warmup"]
    get(warmup["container"])
    get(warmup["answer"])
    for n in range(1, warmup["count"] + 1):
        key = "G01-KD" + f"{n:02}"
        row = get(warmup['proposed_anchor_prefix'] + f'{n:02}') if applied else locate(relative(source), warmup["prefix"] + f"{n:02}.", warmup["owner"], key, "type.task")
        row.update(content_type='type.task', unit_key=key)
        row.update(function=warmup["function"], area="area.lesson", number=n, proposed_title=f"Nhiệm vụ {n:02}",
                   answer=warmup["answer"], proposed_anchor=warmup["proposed_anchor_prefix"] + f"{n:02}",
                   condition="guided; self-work before answer; not independent-test evidence")
        answer = get('lg-' + row['proposed_anchor']) if applied else locate(relative(source), warmup["answer_prefix"] + f"{n:02}.", warmup["answer"], key + "-answer", "type.solution")
        answer.update(content_type='type.solution', unit_key=key + '-answer')
        answer.update(answer_of=key, function="function.warmup", source_group="group.warmup", proposed_title=f"Nhiệm vụ {n:02}",
                      proposed_anchor="lg-" + row["proposed_anchor"])
    for n, anchor in enumerate(data["self_checks"], 1):
        row = get(anchor)
        target = "lg-cg01" if n == 7 else f"lg-d{n:02}"
        row.update(content_type="type.task", function="function.self_check", area="area.lesson", unit_key="G01-TC" + f"{n:02}",
                   number=n, answer=target, proposed_title=data["title_proposals"].get(anchor, f"Nhiệm vụ {n:02}"),
                   condition="guided lesson self-check; not S bank even when legacy name mentions repair")
        get(target).update(content_type="type.solution", function="function.self_check", unit_key="answer:" + row["unit_key"], answer_of=row["unit_key"], source_group="area.lesson", proposed_title=row["proposed_title"])
    for n, anchor in enumerate(data["guided_prompts"], 1):
        get(anchor).update(content_type="type.task", function="function.guided_thinking", unit_key="guided:" + anchor,
                           number=n, proposed_title=f'Nhiệm vụ {n:02}',
                           condition="guided prompt; explanation follows in lesson; no duplicated answer or independent evidence")
    confirmation = data["confirmation"]
    get(confirmation["anchor"]).update(content_type="type.task", function="function.confirmation", area="area.practice",
                                      parent=confirmation["parent"], answer=confirmation["answer"], unit_key="G01-L08-XN01",
                                      proposed_title="Xác nhận nhiệm vụ 08", condition="child confirmation; not regular L09")
    get(confirmation["answer"]).update(content_type="type.solution", function="function.confirmation", unit_key="answer:G01-L08-XN01", answer_of="G01-L08-XN01", source_group="area.practice", proposed_title="Xác nhận nhiệm vụ 08")
    for unit in data["knowledge_units"]:
        row = get(unit["anchor"])
        if unit["parts"]:
            row["classification"] = "owner_of_atomic_units_not_extra_unit"
            for n, prefix in enumerate(unit["parts"], 1):
                locate(row["path"], prefix, row["anchor"], row["anchor"] + f":part{n}", unit["type"])
        else:
            row.update(content_type=unit["type"], unit_key=unit["anchor"])
    for example in data["examples"]:
        row = get(example["anchor"])
        if example["prefix"]:
            row = locate(row["path"], example["prefix"], row["anchor"], example["id"], "type.example")
        row.update(content_type="type.example", unit_key=example["id"])
        title = row["title"]
        if row["kind"] == "heading":
            title = re.sub(r"^\d+(?:\.\d+)*\.\s*", "", title)
            if "Ví dụ" not in title:
                title = "Ví dụ " + example["id"][1:] + " – " + title.split(" — ")[-1]
        else:
            title = "Ví dụ " + example["id"][1:] + " – " + get(example["anchor"])["title"].split(". ", 1)[-1]
        row["proposed_title"] = title
        for anchor in example["parts"] + example["reuses"]:
            get(anchor).update(content_type="type.example", relation="part_of" if anchor in example["parts"] else "reuse_of", related_unit=example["id"], classification="placement_not_distinct_unit")
    foundation_number = 0
    for include in includes:
        path = include["source"]
        if "/nen/" not in path:
            continue
        unit_id = Path(path).stem
        source_ids = [r for r in rows if r["path"] == path and 'r1-foundation-unit' in r['text']]
        if len(source_ids) != 1:
            raise ValueError("Foundation owner selector ambiguous: " + path)
        owner = source_ids[0]
        owner.update(area="area.foundation", structural_label="area.foundation", proposed_owner="area.foundation", content_type=None)
        for prefix, kind, suffix in (("**Dùng khi:", "type.guidance", "use"), ("**Nhớ lại.", "type.explanation", "recall"),
                                     (data["foundation"]["example_prefix"], "type.example", "example"), ("**Quay về:", "type.guidance", "return")):
            locate(path, prefix, owner["anchor"], unit_id + ":" + suffix, kind).update(area="area.foundation")
        prefixes = [data["foundation"]["task_prefix"]]
        if unit_id == data["foundation"]["extra_unit"]:
            prefixes.append(data["foundation"]["extra_prefix"])
            locate(path, data["foundation"]["method_prefix"], owner["anchor"], unit_id + ":method", "type.method").update(area="area.foundation")
        for index, prefix in enumerate(prefixes):
            foundation_number += 1
            target = "lg-" + owner["anchor"] + ("-xac-nhan" if index else "")
            row = locate(path, prefix, owner["anchor"], unit_id + ":confirmation" + str(index + 1), "type.task")
            row.update(area="area.foundation", function="function.foundation_confirmation", number=foundation_number,
                       proposed_title=f"Nhiệm vụ {foundation_number:02}", proposed_anchor=owner["anchor"] + f"-xn{index+1:02}",
                       answer=target, condition="new unexposed confirmation only; return to actual caller; package numbering must not be hardcoded in shared include")
            get(target).update(content_type="type.solution", function="function.foundation_confirmation", unit_key="answer:" + row["unit_key"], answer_of=row["unit_key"], source_group="area.foundation", proposed_title=row["proposed_title"])
    for checkpoint in manifest["checkpoints"]:
        anchor = data["checkpoint_bindings"].get(checkpoint["id"])
        if not anchor:
            raise ValueError("Checkpoint lacks explicit source binding: " + checkpoint["id"])
        get(anchor).update(structural_label="point.checkpoint", content_type="type.checkpoint", unit_key=checkpoint["id"], checkpoint=checkpoint, proposed_title="Điểm dừng")
    for row in rows:
        area = row.get("area")
        kind = row.get("content_type")
        function = row.get("function")
        display = None
        if kind == "type.task" or row.get("answer_of"):
            if function in ("function.warmup", "function.self_check"):
                display = "BÀI HỌC • " + ("KHỞI ĐỘNG" if function == "function.warmup" else "TỰ KIỂM TRA")
            elif area == "area.foundation" or row.get("source_group") == "area.foundation":
                display = "ÔN NỀN • " + Path(row["path"]).stem
            elif row.get("task"):
                role = row["task"]["role"]
                if role == "L":
                    stage = next(s for s in manifest["stages"] if row["task"]["id"] in s["practice_task_ids"])
                    row["stage"] = stage["id"]
                    display = "LUYỆN TẬP • CHẶNG " + stage["id"].rsplit("C", 1)[-1]
                else:
                    display = {"K": "KIỂM TRA", "O": "ÔN LẠI • LƯỢT " + str(row["number"]),
                               "S-L": "SỬA LỖI • SAU LUYỆN TẬP", "S-K": "SỬA LỖI • SAU KIỂM TRA", "S-O": "SỬA LỖI • SAU ÔN LẠI"}[role]
            elif function == "function.confirmation":
                display = "LUYỆN TẬP • XÁC NHẬN"
        elif row.get("checkpoint"):
            cp = row["checkpoint"]["id"]
            display = "LUYỆN TẬP • CHẶNG " + cp[-1] if cp.startswith("CP-LT") else "ÔN LẠI • LƯỢT " + cp[-1] if cp.startswith("CP-ON") else "KIỂM TRA • KẾT QUẢ"
        elif kind in ("type.definition", "type.theorem", "type.method", "type.guidance", "type.source"):
            display = {"type.definition": "ĐỊNH NGHĨA", "type.theorem": "ĐỊNH LÍ", "type.method": "PHƯƠNG PHÁP", "type.guidance": "HƯỚNG DẪN", "type.source": "NGUỒN"}[kind]
        row["display_label_proposal"] = display
        row["display_label_note"] = "omit if title/context already states this; keep metadata"
    for row in tasks:
        get(row["task"]["answer_anchor"])["display_label_proposal"] = row["display_label_proposal"]
    for anchor, row in ids.items():
        row["incoming"] = [dict(path=r["path"], line=r["line"], label=r["label"], from_anchor=r["from_anchor"]) for r in references if r["target"] == anchor]
        row["proposed_owner"] = row.get("proposed_owner", row.get("area"))
    missing = sorted({r["target"] for r in references} - ids.keys())
    # Some links target Pandoc auto-generated headings; never certify them as explicit IDs.
    auto_titles = {clean(h["title"]): h for h in rows if h["kind"] == "heading" and not h["anchor"]}
    distinct = [r for r in rows if r.get("unit_key") and r.get("classification") != "placement_not_distinct_unit"]
    counts = Counter(r["content_type"] for r in distinct)
    if applied:
        if get('on-nen')['parent'] is not None:
            raise ValueError('Applied foundation must have an independent source owner')
        for unit in bindings['units']:
            get(unit['question'])
            if unit.get('answer'):
                get(unit['answer'])
        for row in rows:
            if row.get('anchor') in unit_bindings:
                row['display_label_proposal'] = unit_bindings[row['anchor']]['label']
        files[relative(binding_path)] = sha(binding_path)
    return dict(package=data["package_id"], decision=data["decision"], status=data['status'], source_applied=applied,
                sources=files, includes=includes, rows=rows, references=references, assets=assets, components=components,
                unresolved_explicit_targets=missing, unanchored_headings=list(auto_titles),
                counts=dict(rows=len(rows), headings=sum(r["kind"] == "heading" for r in rows), explicit_ids=len(ids),
                            annotated_semantic_units=dict(counts), task_functions=dict(Counter(r.get("function") for r in distinct if r["content_type"] == "type.task")),
                            placement_rows=sum(r["kind"] == "semantic_placement" for r in rows),
                            prose_tables=sum(bool(r.get("anchor", "") and r["anchor"].startswith("r1-table-t")) for r in rows),
                            native_variation_tables=len({c["id"] for c in components}), native_variation_placements=len(components),
                            graph_assets=len({a["target"] for a in assets if a["target"].startswith("hinh/do_thi_")}),
                            canonical_includes=len({i["source"] for i in includes}), include_placements=len(includes), references=len(references)),
                open_decisions=data["open_decisions"])


def self_tests(data, catalog, schema, inventory):
    terms = validate_catalog(catalog)
    def rejected(action):
        try:
            action()
        except (ValueError, KeyError):
            return True
        except Exception as exc:
            import jsonschema
            if isinstance(exc, jsonschema.ValidationError):
                return True
            raise
        return False
    tests = {}
    fixture = copy.deepcopy(catalog); fixture['label_contract']['scope'] = 'R1_2027'
    tests['program-wide label scope cannot shrink to R1'] = rejected(lambda: validate_catalog(fixture))
    tests['Gợi mở distinct from self-check'] = terms['function.guided_thinking']['name'] == 'Gợi mở' and terms['function.self_check']['name'] == 'Tự kiểm tra'
    guided = [r for r in inventory['rows'] if r.get('function') == 'function.guided_thinking']
    tests['seven guided prompts continuous without answer duplicates'] = [r['number'] for r in guided] == list(range(1,8)) and all(not r.get('answer') for r in guided)
    for name, field, value in (("unknown schema version", "schema_version", 2), ("unknown contract version", "label_contract_version", 2),
                               ("false source-applied claim", "status", "source_applied"), ("unknown field", "unexpected", True)):
        fixture = copy.deepcopy(data); fixture[field] = value
        tests[name] = rejected(lambda: validate_application(fixture, schema, terms))
    fixture = copy.deepcopy(data); fixture["areas"]["on-nen"] = "unknown.term"
    tests["unknown term rejected"] = rejected(lambda: validate_application(fixture, schema, terms))
    fixture = copy.deepcopy(data); fixture["areas"]["tu-kiem-tra"] = "area.lesson"
    tests["legacy test anchor cannot change function"] = rejected(lambda: validate_application(fixture, schema, terms))
    fixture = copy.deepcopy(catalog); fixture["label_contract"]["terms"]["area.foundation"]["parent"] = "area.lesson"
    tests["foundation cannot become lesson child"] = rejected(lambda: validate_application(data, schema, validate_catalog(fixture)))
    fixture = copy.deepcopy(catalog); fixture["label_contract"]["terms"]["area.lesson"]["parent"] = "area.lesson"
    tests["ownership cycle rejected"] = rejected(lambda: validate_catalog(fixture))
    fixture = copy.deepcopy(catalog); fixture["label_contract"]["terms"]["area.test"]["name"] = "Bài học"
    tests["duplicate term rejected"] = rejected(lambda: validate_catalog(fixture))
    fixture = copy.deepcopy(data); fixture["self_checks"][0] = "nonexistent-id"
    tests["missing selector rejected"] = rejected(lambda: build_inventory(fixture, DEFAULT_APPLICATION.parent))
    tasks = [r for r in inventory["rows"] if r.get("task")]
    tests["eight L continuous across stages"] = [r["number"] for r in tasks if r["task"]["role"] == "L"] == list(range(1, 9))
    tests["three O continuous across rounds"] = [r["number"] for r in tasks if r["task"]["role"] == "O"] == [1, 2, 3]
    tests["26 S in one functional group"] = sorted(r["number"] for r in tasks if r["function"] == "function.remediation") == list(range(1, 27))
    tests["V03 one unit with multiple placements"] = sum(r.get("unit_key") == "V03" for r in inventory["rows"]) == 1 and sum(r.get("related_unit") == "V03" for r in inventory["rows"]) == 5
    tests["four atomic definitions not two boxes"] = inventory["counts"]["annotated_semantic_units"]["type.definition"] == 4
    tests["eight foundation confirmations not seven cards"] = inventory["counts"]["task_functions"]["function.foundation_confirmation"] == 8
    tests["manifest tasks preserve answer identity"] = all(next(r for r in inventory["rows"] if r.get("anchor") == t["task"]["answer_anchor"]).get("answer_of") == t["task"]["id"] for t in tasks)
    tests["all generated rows match actual source state"] = all(r["source_applied"] == inventory['source_applied'] for r in inventory["rows"])
    tests["seven checkpoints explicitly bound"] = sum(bool(r.get("checkpoint")) for r in inventory["rows"]) == 7
    tests["test total 20 preserved as secondary information"] = sum(r.get("secondary_info", {}).get("points", 0) for r in tasks) == 20
    tests["20 prose tables including the approved review calendar"] = inventory["counts"]["prose_tables"] == 20
    tests["14 native BBT including the approved O03 answer"] = inventory["counts"]["native_variation_tables"] == 14
    tests["13 graph source assets exist"] = inventory["counts"]["graph_assets"] == 13 and all(a["exists"] for a in inventory["assets"])
    fixture = copy.deepcopy(data); fixture["task_functions"]["L"] = "function.test"
    tests["same type task cannot erase learning function"] = rejected(lambda: validate_application(fixture, schema, terms))
    validate_inventory(inventory)
    for name, change in (
        ("stage numbering reset rejected", lambda r: next(x for x in r["rows"] if x.get("unit_key") == "G01-L05").update(number=1)),
        ("wrong answer identity rejected", lambda r: next(x for x in r["rows"] if x.get("anchor") == "loi-giai-2").update(answer_of="G01-L02")),
        ("repeated V03 counted twice rejected", lambda r: next(x for x in r["rows"] if x.get("related_unit") == "V03").update(unit_key="V03", classification="distinct")),
        ("map cannot misstate source state", lambda r: r["rows"][0].update(source_applied=not r['source_applied']))):
        fixture = copy.deepcopy(inventory); change(fixture)
        tests[name] = rejected(lambda: validate_inventory(fixture))
    return tests


def validate_inventory(report):
    rows = report["rows"]
    for function in ("function.practice", "function.test", "function.review", "function.remediation"):
        group = sorted((r for r in rows if r.get("task") and r["function"] == function), key=lambda r: r["line"])
        if [r["number"] for r in group] != list(range(1, len(group) + 1)):
            raise ValueError("Whole-group numbering broken: " + function)
    by_id = {r["anchor"]: r for r in rows if r.get("anchor")}
    for row in rows:
        if row.get("task") and by_id[row["task"]["answer_anchor"]].get("answer_of") != row["task"]["id"]:
            raise ValueError("Answer/task identity mismatch")
    keys = [r["unit_key"] for r in rows if r.get("unit_key")]
    if len(keys) != len(set(keys)):
        raise ValueError("Semantic unit counted twice")
    expected = report['status'] == 'source_applied_pending_html_acceptance'
    if report['status'] not in ('mapping_only', 'source_applied_pending_html_acceptance') or report['source_applied'] != expected or any(r['source_applied'] != expected for r in rows):
        raise ValueError('Migration map/source state mismatch; no HTML acceptance implied')


def markdown(report, terms):
    out = ["# Bảng áp dụng hệ nhãn R1-G01", "", "QD_025 · Bảng áp dụng từ nguồn hiện tại · Chưa sửa QMD, chưa nghiệm thu HTML.", "",
           "Quy tắc chung đã duyệt; tên/số/anchor con cụ thể vẫn là phương án chờ chốt. Không dùng bảng này làm nguồn build.", "",
           "## Kiểm kê", "", "```json", json.dumps(report["counts"], ensure_ascii=False, indent=2), "```", "",
           "Mỗi heading/ID và khối ngữ nghĩa đều có dòng đối chiếu; khối bao hoặc lần dùng lại không làm tăng số đơn vị. Câu thiếu ID có locator theo tệp và dòng. Phân loại không tường minh vẫn chờ rà, không được tính là 0.", "",
           "## Những điểm cần chốt trước sửa nguồn", ""]
    for issue in report["open_decisions"]:
        out += ["- " + issue["id"] + ": " + issue["question"]]
    out += ["", "## Bảng áp dụng toàn nguồn", "", "| Nguồn / ID hoặc locator | Hiện tại → Dự kiến | Nhãn cấu trúc / loại / chức năng | Sở hữu hiện tại → đích | Đáp án / quan hệ / trạng thái |", "|---|---|---|---|---|"]
    name = lambda key: terms.get(key, {}).get("name", key or "—")
    for row in report["rows"]:
        address = row.get("anchor") or row.get("unit_key") or "chưa có ID"
        source = "`" + row["path"] + ":" + str(row["line"]) + "`<br>" + address
        current = row.get("title") or row.get("text", "")[:100]
        proposed = row.get("proposed_title") or "giữ / chốt theo ngữ cảnh"
        labels = " / ".join(name(row.get(k)) for k in ("structural_label", "content_type", "function")) + "<br>Hiển thị: " + (row.get("display_label_proposal") or "không thêm nhãn lặp / chốt theo ngữ cảnh")
        owner = str(row.get("parent") or "gói") + " → " + str(row.get("proposed_owner") or row.get("area") or "giữ owner")
        answer = row.get("answer") or row.get("task", {}).get("answer_anchor") or row.get("answer_of") or row.get("related_unit") or "—"
        notes = row.get("condition") or row.get("classification") or row.get("relation") or row["approval"]
        if row.get("secondary_info"):
            notes += "; " + str(row["secondary_info"]["points"]) + " điểm giữ ở thông tin phụ"
        cells = [source, current + " → " + proposed, labels, owner, str(answer) + "; " + notes]
        out.append("| " + " | ".join(c.replace("\n", " ").replace("|", "\\|") for c in cells) + " |")
    out += ["", "## Đề–đáp án và đường học từ manifest", "", "| Mã | Chức năng / độ lộ | Đề → đáp án | Mục tiêu / điểm dừng | Nhánh đạt / nhánh lỗi |", "|---|---|---|---|---|"]
    for row in report["rows"]:
        if not row.get("task"):
            continue
        t = row["task"]
        cells = [t["id"], t["role"] + " / " + t["exposure_policy"], t["source_anchor"] + " → " + t["answer_anchor"],
                 ", ".join(t["objective_ids"] + t["checkpoint_ids"]), json.dumps([t["next_on_pass"], t["next_on_error"]], ensure_ascii=False)]
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    out += ["", "## Toàn bộ dẫn chiếu phải giữ hoặc đổi lời gọi", "", "| Nơi gọi | Chữ hiện tại | Đích ID giữ nguyên |", "|---|---|---|"]
    for ref in report["references"]:
        out.append(f'| `{ref["path"]}:{ref["line"]}` | {ref["label"].replace("|", "\\|")} | {ref["target"]} |')
    out += ["", "## Bảng, hình và tài nguyên", "", "| Nguồn | Tài nguyên | Có tệp |", "|---|---|---|"]
    for asset in report["assets"]:
        out.append(f'| `{asset["path"]}:{asset["line"]}` | {asset["target"]} | {asset["exists"]} |')
    out += ["", "| Nguồn | Bảng native | Vùng sở hữu / nguồn dữ liệu |", "|---|---|---|"]
    for component in report["components"]:
        out.append(f'| `{component["path"]}:{component["line"]}` | {component["id"]} | {component["parent"]}; `du_lieu/bang_bien_thien.json` |')
    out += ["", "## Nguồn và giới hạn", "", "```json", json.dumps(report["sources"], indent=2, ensure_ascii=False), "```", "",
            "JSON đi kèm giữ đầy đủ task, checkpoint, incoming references, hash, include placements, quan hệ và ID dự kiến. Những link không trỏ ID tường minh: " + ", ".join(report["unresolved_explicit_targets"]), "",
            "Không chứng nhận tính đúng toán, toàn bộ phân loại ngữ nghĩa, DOM/mục lục, đường quay về runtime hoặc trải nghiệm. Chưa áp dụng nguồn, dựng HTML/PDF, stage/commit hay phát hành.", ""]
    result = '\n'.join(out)
    if report['source_applied']:
        result = result.replace('Chưa sửa QMD, chưa nghiệm thu HTML.', 'Đã áp dụng nguồn; chưa nghiệm thu HTML.').replace('tên/số/anchor con cụ thể vẫn là phương án chờ chốt.', 'tên/số/anchor con đã áp dụng theo bản chốt chủ trì sửa và QD_025.').replace('Chưa áp dụng nguồn, dựng HTML/PDF, stage/commit hay phát hành.', 'Bảng này xác minh nguồn/binding; không chứng nhận HTML, PDF, stage/commit hoặc phát hành.')
    return result


DEFAULT_APPLICATION = REPO_ROOT / "content/thpt/on_thi_toan_thpt/hoc_lieu/r1_g01/_quy_trinh/ap_dung_he_nhan.json"


def run(application=None, output=None, with_tests=False):
    path = repository_path(REPO_ROOT, application) if application else DEFAULT_APPLICATION
    data = json.loads(path.read_text(encoding="utf-8"))
    catalog = load_yaml(COMMON_CATALOG)
    terms = validate_catalog(catalog)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validate_application(data, schema, terms)
    report = build_inventory(data, path.parent)
    validate_inventory(report)
    report["sources"][relative(path)] = sha(path)
    report["sources"][relative(COMMON_CATALOG)] = sha(COMMON_CATALOG)
    report["sources"][relative(SCHEMA_PATH)] = sha(SCHEMA_PATH)
    report["sources"][relative(Path(__file__).resolve())] = sha(Path(__file__).resolve())
    report["sources"]["scripts/zo_learning_architecture.py"] = sha(REPO_ROOT / "scripts/zo_learning_architecture.py")
    report["self_tests"] = self_tests(data, catalog, schema, report) if with_tests else {}
    report["passed"] = all(report["self_tests"].values())
    if output:
        destination = repository_path(REPO_ROOT, output)
        if not destination.is_relative_to(REPO_ROOT / "_audit"):
            raise ValueError("Reports must stay in _audit")
        destination.mkdir(parents=True, exist_ok=True)
        for filename in ("ap_dung_he_nhan.json", "ap_dung_he_nhan.md"):
            if (destination / filename).exists():
                raise ValueError("Refusing to overwrite report: " + filename)
        (destination / "ap_dung_he_nhan.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (destination / "ap_dung_he_nhan.md").write_text(markdown(report, terms), encoding="utf-8")
    print(json.dumps({"status": report["status"], "passed": report["passed"], "counts": report["counts"],
                      "self_tests": report["self_tests"], "unresolved_explicit_targets": report["unresolved_explicit_targets"]}, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1
