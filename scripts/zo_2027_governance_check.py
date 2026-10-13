"""Scoped 2027 governance gate. No render, acceptance, or release authority.

The registry selects active rules by topic; hashes record provenance only.
Learning rules remain in 01/02/07. Fixing sources is never locked by this gate.
Run with zo_python.py. Reports must be new files under _audit, never receipts.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.dont_write_bytecode = True
from bs4 import BeautifulSoup
import yaml

ROOT = Path(__file__).resolve().parents[1]
GOV = ROOT / 'content/thpt/on_thi_toan_thpt/tot_nghiep_thpt/2027/_quy_trinh'
REGISTRY = GOV / 'hop_dong_dieu_hanh.json'
MAIN = ['bai-hoc', 'phieu-luyen', 'tu-kiem-tra', 'on-lai']
SUPPORTED_RULES = {'learning_route': 'QD_033', 'supersession_policy': 'QD_022',
                   'label_system': 'QD_025', 'assessment_policy': 'QD_024',
                   'transfer_terminology': 'QD_028', 'math_notation': 'QD_029',
                   'lesson_numbering': 'QD_029', 'table_language': 'QD_030',
                   'full_text_structure': 'QD_031', 'course_navigation': 'QD_032'}


def learning_route_policy_checks(rule: dict) -> dict:
    """Explicit QD_033 contract; never infer learner-source compliance."""
    expected = {
        'scope': 'all_program_learning_packages',
        'standard_recommended_progression': ['lesson', 'practice', 'test', 'review'],
        'mandatory_linear_sequence': False,
        'entry_basis': ['need', 'preparation', 'existing_learning_evidence'],
        'independent_contextual_supports': ['foundation', 'solutions', 'repair', 'journal'],
        'test_attempt_self_reliant': True,
        'end_test_before_help': True,
        'preserve_initial_work_separately': True,
        'checkpoint_evidence_distinct_from_journal': True,
        'journal_required_at_every_checkpoint': False,
        'return_to_question_link': 'only_when_question_solution_locations_separate',
    }
    return {'QD_033 contract: ' + key: (
        rule.get(key) is value if isinstance(value, bool) else rule.get(key) == value)
        for key, value in expected.items()}


def learning_authority_checks(architecture: str, page_rules: str, qmd_contract: str) -> dict:
    """Scoped text invariants; not a complete natural-language contradiction audit."""
    return {
        'QD_033 authority keeps recommended progression without compulsory learning': (
            'Bài học → Luyện tập → Kiểm tra → Ôn lại là tiến trình chuẩn được khuyến nghị' in architecture
            and 'không phải điều kiện bắt buộc phải hoàn thành tuần tự' in architecture
            and 'nhu cầu, mức chuẩn bị và bằng chứng học tập hiện có' in architecture
            and 'Đây là quan hệ tổ chức bắt buộc của gói' not in architecture),
        'QD_033 authority keeps contextual supports independent': (
            'Ôn nền, Lời giải, Sửa lỗi và Nhật kí là các hỗ trợ độc lập' in architecture),
        'QD_033 test authority ends attempt before help and separates initial work': all(
            token in architecture for token in [
                'tự lực hoàn toàn', 'kết thúc lượt kiểm tra trước',
                'giữ riêng bài làm và kết quả ban đầu',
                'phần sau hỗ trợ không được tính ngược thành bằng chứng độc lập']),
        'QD_033 authority separates checkpoint evidence and journal': (
            'Lưu bằng chứng tại Điểm dừng khác với ghi Nhật kí' in architecture
            and 'Không yêu cầu ghi Nhật kí ở mọi Điểm dừng' in architecture
            and 'học sinh hoàn tất sáu việc theo thứ tự' not in architecture),
        'QD_033 page policy uses conditional return-to-question link': (
            'Chỉ yêu cầu liên kết quay lại đề khi đề và lời giải thực sự ở hai vị trí tách biệt' in page_rules
            and 'Mỗi nhiệm vụ độc lập có một đích lời giải xác định và liên kết quay lại đúng đề.' not in page_rules),
        'QD_033 QMD contract replaces unconditional links and nested journal': (
            'Chỉ yêu cầu liên kết quay lại đề khi đề và lời giải thực sự ở hai vị trí tách biệt' in qmd_contract
            and 'Nhật kí không thuộc Ôn lại' in qmd_contract
            and 'Nhiệm vụ độc lập dùng liên kết hai chiều một-một:' not in qmd_contract
            and 'Nhật kí` hiện còn có thể là đích sâu trong Ôn lại' not in qmd_contract),
    }


def profile_learning_rule_checks(audit: dict, product_rule: dict, current: str) -> dict:
    """Account for an untouched historical profile without certifying the product.

    This explicit transition is valid only for QD_021 -> QD_033. An arbitrary
    stale revision, missing state, or claimed application fails the document
    gate. The candidate gate separately requires current source verification.
    """
    pending = (
        current == 'QD_033'
        and audit.get('decision') == product_rule.get('previous_verified_decision') == 'QD_021'
        and product_rule.get('decision') == current
        and product_rule.get('status') == 'pending_source_review'
        and product_rule.get('source_applied') is False
        and product_rule.get('review_scope') == 'qmd_html_alignment_not_yet_cross_checked'
        and product_rule.get('known_mismatch') is False
        and product_rule.get('profile_audit_role') == 'historical_only')
    applied = (
        audit.get('decision') == product_rule.get('decision') == current
        and product_rule.get('source_applied') is True
        and product_rule.get('status') == 'source_applied_checked_pending_owner_review')
    return {'profile learning revision explicitly current or historical pending review': pending or applied}


def candidate_learning_route_ready(product_rule: dict, current: str) -> bool:
    return (product_rule.get('decision') == current
            and product_rule.get('source_applied') is True
            and product_rule.get('status') == 'source_applied_checked_pending_owner_review')


def assessment_policy_checks(rule: dict) -> dict:
    """Registry contract only; this does not certify learner-source wording."""
    return {
        'test policy covers all program packages with Test': rule.get('scope') == 'all_program_packages_with_test',
        'test entry allows preparedness OR confidence': rule.get('entry') == 'prepared_or_confident',
        'test entry has no prior independent work prerequisite': rule.get('prior_independent_work_required_for_entry') is False,
        'single test attempt cannot be split': rule.get('split_attempt_allowed') is False,
        'confidence is not achievement evidence': rule.get('confidence_is_achievement_evidence') is False,
    }


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_repo_path(relative: str) -> Path:
    target = (ROOT / relative).resolve()
    if not target.is_relative_to(ROOT) or '.git' in target.parts:
        raise ValueError('Dependency outside repository scope: ' + relative)
    return target


def governance_context():
    registry_bytes = REGISTRY.read_bytes()
    registry = json.loads(registry_bytes)
    checks = {'registry schema supported': registry.get('schema_version') == 2}
    dependencies = registry.get('dependencies', [])
    checks['required authority and guard dependencies present'] = all(
        p in dependencies for p in [
            (GOV / n).relative_to(ROOT).as_posix() for n in [
                '01_kien_truc_hoc_tap.md', '02_quy_trinh_va_nghiem_thu.md',
                '03_dieu_hanh_chuong_trinh.md', '04_nhat_ki_quyet_dinh.md',
                '07_quy_chuan_cau_truc_trang_nguoi_hoc.md',
                '08_danh_muc_tham_quyen_dieu_hanh.md']]
        + ['scripts/zo_2027_governance_check.py', 'scripts/zo_r1_g01_editorial_check.py',
           'scripts/zo_web_2027_backlog_check.py'])
    actual = {}
    for relative in dependencies:
        path = safe_repo_path(relative)
        actual[relative] = digest(path.read_bytes()) if path.is_file() else None
        checks['authority dependency exists: ' + relative] = actual[relative] is not None
    decision = registry.get('decision')
    journal = (GOV / '04_nhat_ki_quyet_dinh.md').read_text(encoding='utf-8')
    ids = re.findall(r'^## (QD_\d+)\b', journal, re.M)
    revisions = {}
    for topic, supported in SUPPORTED_RULES.items():
        rule = registry.get('active_rules', {}).get(topic, {})
        revisions[topic] = rule.get('decision')
        checks['guard supports active rule: ' + topic] = revisions[topic] == supported
        checks['active rule has decision record: ' + topic] = revisions[topic] in ids
        owner = safe_repo_path(rule.get('owner', 'missing-rule-owner'))
        checks['active rule owner references decision: ' + topic] = (
            owner.is_file() and isinstance(revisions[topic], str)
            and revisions[topic] in owner.read_text(encoding='utf-8'))
    board = (GOV / '03_dieu_hanh_chuong_trinh.md').read_text(encoding='utf-8')
    active = board.split('## A. Công việc đang mở', 1)[-1].split('### DH_', 1)[0]
    checks['active board uses current decision'] = decision in active
    architecture = (GOV / '01_kien_truc_hoc_tap.md').read_text(encoding='utf-8')
    page_rules = (GOV / '07_quy_chuan_cau_truc_trang_nguoi_hoc.md').read_text(encoding='utf-8')
    qmd_contract = (GOV / 'quy_chuan_goi_qmd.md').read_text(encoding='utf-8')
    checks.update(learning_route_policy_checks(registry.get('active_rules', {}).get('learning_route', {})))
    checks.update(learning_authority_checks(architecture, page_rules, qmd_contract))
    for name in ['02_quy_trinh_va_nghiem_thu.md', '03_dieu_hanh_chuong_trinh.md',
                 '07_quy_chuan_cau_truc_trang_nguoi_hoc.md', '08_danh_muc_tham_quyen_dieu_hanh.md',
                 'README.md', 'quy_chuan_goi_qmd.md']:
        checks['QD_033 authority pointer synchronized: ' + name] = 'QD_033' in (
            GOV / name).read_text(encoding='utf-8')
    checks.update(assessment_policy_checks(registry.get('active_rules', {}).get('assessment_policy', {})))
    entry_section = architecture.split('## 2.3.', 1)[-1].split('## 2.4.', 1)[0]
    checks['test authority replaces old entry prerequisite'] = (
        'Không yêu cầu phải có bài làm độc lập trước đó để được vào Kiểm tra.' in entry_section
        and 'Đã có bài làm độc lập phù hợp các mục tiêu của gói: được thử Kiểm tra trực tiếp.' not in entry_section)
    checks['test authority explicitly covers program and single attempt'] = all(
        token in entry_section for token in [
            'toàn bộ các gói của chương trình Ôn thi Toán THPT 2027',
            'không được chia một lượt Kiểm tra thành nhiều đợt/buổi',
            'Tự tin không phải bằng chứng đạt mục tiêu',
            'Không đổi Khảo sát D0 thành Kiểm tra'])
    for name in ['02_quy_trinh_va_nghiem_thu.md', '07_quy_chuan_cau_truc_trang_nguoi_hoc.md',
                 '08_danh_muc_tham_quyen_dieu_hanh.md', 'README.md', '05_huong_dan_su_dung.md',
                 '06_nguon_va_chuyen_tiep.md', 'mau/ho_so_goi.md', 'goi/R1_G01.md', 'goi/R1_G02.md']:
        checks['test policy reference synchronized: ' + name] = 'QD_024' in (
            GOV / name).read_text(encoding='utf-8')
    checks['course agent instruction references program-wide test policy'] = 'QD_024' in (
        ROOT / 'content/thpt/on_thi_toan_thpt/AGENTS.md').read_text(encoding='utf-8')
    checks['14 situation IDs in authority'] = re.findall(r'^\| (DH\d+) \|', architecture, re.M) == [
        f'DH{i:02}' for i in range(1, 15)]
    for package in ['r1_g01', 'r1_g02']:
        profile = yaml.safe_load((ROOT / 'content/thpt/on_thi_toan_thpt/hoc_lieu' /
                                  package / '_quy_trinh/ho_so/index.yml').read_text(encoding='utf-8'))
        checks.update({name + ': ' + package: value for name, value in profile_learning_rule_checks(
            profile.get('governance_audit', {}),
            registry['products'][profile['package']['id']].get('learning_route', {}),
            revisions['learning_route']).items()})
        checks['profile current label rule: ' + package] = profile.get('labeling_audit', {}).get('decision') == revisions['label_system']
        assessment = profile.get('assessment_policy_audit', {})
        product = registry['products'][profile['package']['id']].get('assessment_policy', {})
        checks['profile current test policy and scope: ' + package] = (
            assessment.get('decision') == revisions['assessment_policy']
            and assessment.get('scope') == 'all_program_packages_with_test')
        checks['profile and registry agree test source state: ' + package] = (
            assessment.get('status') == product.get('status')
            and assessment.get('source_applied') is product.get('source_applied')
            and isinstance(assessment.get('source_applied'), bool))
        labeling = profile.get('labeling_audit', {})
        label_product = registry['products'][profile['package']['id']].get('labeling', {})
        checks['profile and registry agree label source state: ' + package] = (
            labeling.get('status') == label_product.get('status')
            and labeling.get('source_applied') is label_product.get('source_applied')
            and isinstance(labeling.get('source_applied'), bool))
    from zo_learning_labels import validate_catalog, validate_application, build_inventory, validate_inventory, DEFAULT_APPLICATION
    from zo_learning_architecture import COMMON_CATALOG, SCHEMA_PATH, load_yaml
    try:
        terms = validate_catalog(load_yaml(COMMON_CATALOG))
        checks['QD_028 transfer and integration are distinct functions'] = (
            terms['function.transfer']['name']=='Chuyển giao'
            and terms['function.integration']['name']=='Phối hợp'
            and terms['function.transfer']['scope']!=terms['function.integration']['scope'])
        application = json.loads(DEFAULT_APPLICATION.read_text(encoding='utf-8'))
        validate_application(application, json.loads(SCHEMA_PATH.read_text(encoding='utf-8')), terms)
        validate_inventory(build_inventory(application, DEFAULT_APPLICATION.parent))
        checks['QD_025 catalog/schema/current G01 map consistent'] = True
    except (ValueError, OSError, KeyError) as exc:
        checks['QD_025 catalog/schema/current G01 map consistent'] = False
        checks['label gate diagnostic: ' + str(exc)] = False
    checks['label implementation dependencies registered'] = all(p in dependencies for p in [
        relative for relative in ['scripts/zo_learning_labels.py', 'scripts/zo_learning_architecture.py',
                                 DEFAULT_APPLICATION.relative_to(ROOT).as_posix(), COMMON_CATALOG.relative_to(ROOT).as_posix(),
                                 SCHEMA_PATH.relative_to(ROOT).as_posix()]])
    if registry['products']['R1-G02'].get('labeling', {}).get('source_applied'):
        from zo_r1_g02_labels_check import BINDING, validate_binding
        try:
            validate_binding(json.loads(BINDING.read_text(encoding='utf-8')))
            checks['current G02 binding matches common vocabulary'] = True
        except (AssertionError, ValueError, OSError, KeyError):
            checks['current G02 binding matches common vocabulary'] = False
        checks['G02 semantic implementation dependencies registered'] = all(p in dependencies for p in [
            BINDING.relative_to(ROOT).as_posix(), 'scripts/zo_r1_g02_labels_check.py',
            'scripts/zo_web_2027_g02.py'])
    context = {'decision': decision,
               'rule_revisions': revisions,
               'fingerprint': digest(json.dumps({'registry_sha256': digest(registry_bytes),
                                                 'actual_dependencies': actual},
                                                sort_keys=True).encode('utf-8')),
               'registry_sha256': digest(registry_bytes),
               'hash_policy': 'provenance_only_not_global_expiry',
               'documents_passed': all(checks.values())}
    return context, checks, registry


def evidence_current(report: dict, context: dict, required_rules=('learning_route',)) -> bool:
    """Only requested rule topics can expire these checks.

    Callers must separately verify the inputs and checker implementation for
    the checks reused. This function does not certify those or owner acceptance.
    """
    old = report.get('governance', {})
    return bool(context['documents_passed'] and all(
        old.get('rule_revisions', {}).get(topic) == context['rule_revisions'].get(topic)
        and context['rule_revisions'].get(topic) is not None for topic in required_rules))


def learning_map_checks(doc: BeautifulSoup) -> dict:
    """Inspect actual main-link relationships, not mere keyword presence.

    Does not certify all prose semantics or browser interaction. Those require
    the 14-case source/target review and fresh browser checks in the next task.
    """
    region = doc.find(id='cách-học-với-tài-liệu-này')
    if region is None:
        return {'learning guide exists': False}
    main = region.select_one('[data-learning-main]')
    if main is None:
        chains = [p for p in region.find_all('p')
                  if '↓' in p.get_text() and len(p.select('a[href^="#"]')) >= 2]
        main = chains[0] if len(chains) == 1 else None
    links = main.select('a[href^="#"]') if main else []
    targets = [unquote(a['href'][1:]) for a in links]
    return {
        'main map lists exactly four activities in catalog order, not mandatory learner sequence': targets == MAIN,
        'main map excludes support/result/journal stages': bool(links) and all(t in MAIN for t in targets),
        'learner lesson label excludes editorial explanation': bool(links) and links[0].get_text(' ', strip=True) == 'Bài học',
    }


def self_tests(context: dict) -> dict:
    def page(chain):
        links = ' ↓ '.join(f'<a href="#{t}">{label}</a>' for t, label in chain)
        return BeautifulSoup('<section id="cách-học-với-tài-liệu-này"><p>' + links + '</p></section>', 'html.parser')
    valid = list(zip(MAIN, ['Bài học', 'Luyện tập', 'Kiểm tra', 'Ôn lại']))
    old = valid[:3] + [('đọc-kết-quả-tự-kiểm-tra', 'Đọc kết quả'),
                      ('cp-kt', 'Sửa lỗi'), ('nhat-ky', 'Nhật kí')] + valid[3:]
    tests = {'positive four-node main map': all(learning_map_checks(page(valid)).values()),
             'negative seven-node old map': not all(learning_map_checks(page(old)).values()),
             'negative lesson editorial label': not all(learning_map_checks(page(
                 [('bai-hoc', 'Bài học, gồm Khởi động')] + valid[1:])).values()),
             'negative reordered main map': not all(learning_map_checks(page(valid[::-1])).values()),
             'negative missing map': not all(learning_map_checks(BeautifulSoup('<p>Chọn nơi bắt đầu Bản đồ học gói Trong hoạt động đang làm không biến</p>', 'html.parser')).values()),
             'negative unbound old PASS report': not evidence_current({'passed': 465, 'total': 465}, context)}
    current = {'governance': dict(context)}
    tests['positive bound evidence'] = evidence_current(current, context)
    stale = copy.deepcopy(current); stale['governance']['fingerprint'] = 'stale'
    tests['positive harmless document hash change'] = evidence_current(stale, context)
    stale = copy.deepcopy(current); stale['governance']['decision'] = 'QD_020'
    tests['positive unrelated global decision change'] = evidence_current(stale, context)
    stale = copy.deepcopy(current); stale['governance']['rule_revisions']['supersession_policy'] = 'unrelated'
    tests['positive unrelated rule revision change'] = evidence_current(stale, context)
    stale = copy.deepcopy(current); stale['governance']['rule_revisions']['learning_route'] = 'QD_020'
    tests['negative superseded learning rule'] = not evidence_current(stale, context)
    tests['positive browser subset needs no learning-rule binding'] = evidence_current({}, context, required_rules=())
    stale_context = dict(context, documents_passed=False)
    tests['negative unresolved authority conflict'] = not evidence_current(current, stale_context)
    stale = copy.deepcopy(current); stale['governance']['rule_revisions']['label_system'] = 'old-labels'
    tests['negative superseded label rule'] = not evidence_current(stale, context, required_rules=('label_system',))
    tests['positive learning checks unaffected by label-only revision'] = evidence_current(stale, context)
    policy = {'scope': 'all_program_packages_with_test', 'entry': 'prepared_or_confident',
              'prior_independent_work_required_for_entry': False, 'split_attempt_allowed': False,
              'confidence_is_achievement_evidence': False}
    tests['positive program-wide test policy'] = all(assessment_policy_checks(policy).values())
    for key, value in [('scope', 'R1_only'), ('entry', 'prepared_and_confident'),
                       ('prior_independent_work_required_for_entry', True),
                       ('split_attempt_allowed', True), ('confidence_is_achievement_evidence', True)]:
        tests['negative superseded test policy: ' + key] = not all(
            assessment_policy_checks(dict(policy, **{key: value})).values())
    tests['negative missing test policy'] = not all(assessment_policy_checks({}).values())
    tests['positive current assessment evidence'] = evidence_current(current, context, required_rules=('assessment_policy',))
    stale = copy.deepcopy(current); stale['governance']['rule_revisions']['assessment_policy'] = 'QD_021'
    tests['negative superseded assessment evidence'] = not evidence_current(stale, context, required_rules=('assessment_policy',))
    tests['positive unrelated learning evidence unaffected by test policy revision'] = evidence_current(stale, context)
    route = json.loads(REGISTRY.read_text(encoding='utf-8'))['active_rules']['learning_route']
    tests['positive QD_033 learning contract'] = all(learning_route_policy_checks(route).values())
    bad_fields = {
        'scope': 'R1_only',
        'standard_recommended_progression': ['lesson', 'test', 'practice', 'review'],
        'mandatory_linear_sequence': True,
        'entry_basis': ['preparation'], 'independent_contextual_supports': ['foundation'],
        'test_attempt_self_reliant': False, 'end_test_before_help': False,
        'preserve_initial_work_separately': False, 'checkpoint_evidence_distinct_from_journal': False,
        'journal_required_at_every_checkpoint': True, 'return_to_question_link': 'always',
    }
    for key, value in bad_fields.items():
        tests['negative QD_033 contract mutation: ' + key] = not all(
            learning_route_policy_checks(dict(route, **{key: value})).values())
    tests['negative missing QD_033 learning contract'] = not all(learning_route_policy_checks({}).values())
    authority = [(GOV / n).read_text(encoding='utf-8') for n in [
        '01_kien_truc_hoc_tap.md', '07_quy_chuan_cau_truc_trang_nguoi_hoc.md', 'quy_chuan_goi_qmd.md']]
    tests['positive QD_033 operative authorities'] = all(learning_authority_checks(*authority).values())
    mutated = authority.copy()
    mutated[0] = mutated[0].replace('giữ riêng bài làm và kết quả ban đầu', 'ghép bài sau hỗ trợ vào bài ban đầu')
    tests['negative test authority merges initial and supported work'] = not all(
        learning_authority_checks(*mutated).values())
    for index, old_clause in [
        (0, 'Đây là quan hệ tổ chức bắt buộc của gói'),
        (0, 'học sinh hoàn tất sáu việc theo thứ tự'),
        (1, 'Mỗi nhiệm vụ độc lập có một đích lời giải xác định và liên kết quay lại đúng đề.'),
        (2, 'Nhiệm vụ độc lập dùng liên kết hai chiều một-một:')]:
        mutated = authority.copy(); mutated[index] += '\n' + old_clause
        tests['negative reintroduced old operative clause: ' + old_clause] = not all(
            learning_authority_checks(*mutated).values())
    pending = {'decision': 'QD_033', 'status': 'pending_source_review', 'source_applied': False,
               'review_scope': 'qmd_html_alignment_not_yet_cross_checked', 'known_mismatch': False,
               'previous_verified_decision': 'QD_021', 'profile_audit_role': 'historical_only'}
    tests['positive explicitly historical profile transition'] = all(profile_learning_rule_checks(
        {'decision': 'QD_021'}, pending, 'QD_033').values())
    tests['negative candidate with untouched historical profile'] = not candidate_learning_route_ready(pending, 'QD_033')
    for key, value in [('decision', 'QD_021'), ('status', 'passed'), ('source_applied', True),
                       ('review_scope', 'known_source_mismatch'), ('known_mismatch', True),
                       ('previous_verified_decision', 'QD_020'), ('profile_audit_role', 'current')]:
        tests['negative forged historical transition: ' + key] = not all(profile_learning_rule_checks(
            {'decision': 'QD_021'}, dict(pending, **{key: value}), 'QD_033').values())
    tests['negative missing product learning revision'] = not all(profile_learning_rule_checks(
        {'decision': 'QD_021'}, {}, 'QD_033').values())
    tests['negative profile relabeled current without source review'] = not all(profile_learning_rule_checks(
        {'decision': 'QD_033'}, pending, 'QD_033').values())
    applied = {'decision': 'QD_033', 'status': 'source_applied_checked_pending_owner_review', 'source_applied': True}
    tests['positive verified current candidate state'] = candidate_learning_route_ready(applied, 'QD_033')
    tests['positive verified current profile state'] = all(profile_learning_rule_checks(
        {'decision': 'QD_033'}, applied, 'QD_033').values())
    stale = copy.deepcopy(current); stale['governance']['rule_revisions']['learning_route'] = 'QD_021'
    tests['negative actual QD_021 evidence reused for QD_033'] = not evidence_current(stale, context)
    return tests


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--candidate', type=Path, help='Read an existing HTML; never renders')
    parser.add_argument('--package', choices=['R1-G01', 'R1-G02'])
    parser.add_argument('--evidence', type=Path, help='Reject reports unbound to current governance')
    parser.add_argument('--required-rule', action='append', choices=list(SUPPORTED_RULES),
                        help='Rule topic for --evidence; repeat as needed (default: learning_route)')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if bool(args.candidate) != bool(args.package):
        parser.error('--candidate and --package must be provided together')
    if args.required_rule and not args.evidence:
        parser.error('--required-rule requires --evidence')
    context, checks, registry = governance_context()
    if args.self_test:
        checks.update({'self-test: ' + k: v for k, v in self_tests(context).items()})
    if args.evidence:
        checks['evidence bound to current governance'] = evidence_current(
            json.loads(args.evidence.read_text(encoding='utf-8')), context,
            required_rules=tuple(args.required_rule or ['learning_route']))
    if args.candidate:
        page = BeautifulSoup(args.candidate.read_text(encoding='utf-8'), 'html.parser')
        if args.package in ('R1-G01', 'R1-G02'):
            checks.update(learning_map_checks(page))
        state = registry['products'][args.package]
        checks['candidate source verified under current learning rule'] = candidate_learning_route_ready(
            state.get('learning_route', {}), context['rule_revisions']['learning_route'])
        checks['package has no open governance blockers'] = not state['open_blockers']
        checks['package requires no unperformed situation audit'] = state['situation_audit'] == 'passed'
    failures = [name for name, value in checks.items() if not value]
    report = {'governance': context, 'checks': checks, 'failures': failures,
              'passed': len(checks) - len(failures), 'total': len(checks),
              'product_states': registry['products'],
              'scope': 'documents' if not args.candidate else 'candidate_preflight',
              'candidate': str(args.candidate) if args.candidate else None,
              'candidate_sha256': digest(args.candidate.read_bytes()) if args.candidate else None,
              'limits': ['No render or source edit', 'No complete semantic/browser/math audit',
                         'Document PASS is not product acceptance or release']}
    if args.report:
        target = args.report.resolve()
        if not target.is_relative_to(ROOT / '_audit') or target.suffix != '.json' or target.exists():
            raise ValueError('Report must be a NEW JSON file under _audit')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': report['passed'], 'total': report['total'],
                      'failures': failures, 'scope': report['scope']}, ensure_ascii=False))
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
