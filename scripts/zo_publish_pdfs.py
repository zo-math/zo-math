"""Select and validate PDFs belonging to explicitly selected source pages.

This module never builds PDFs or expands the page scope. Existing PDF build
contracts remain the authority for source/output freshness.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
from pypdf import PdfReader

import zo_publish as p
from zo_pdf_contract import (
    canonical_pdf_provenance_enabled, pdf_build_receipt_path, pdf_output_path,
    pdf_variant, validate_canonical_pdf_provenance, validate_pdf_build_receipt,
)
from zo_qmd_config import discover_project_config


def selected_pdfs(root, sources, *, evidence=True):
    """Derive outputs from source/config, never from arbitrary PDF links."""
    records = []
    for name in sources:
        name = p.safe_relative(name, 'PDF source')
        source = root / name
        if source.is_symlink() or not source.resolve().is_relative_to(root.resolve()):
            raise p.ConfigError('Unsafe PDF source: '+name)
        if name == 'content/thpt/on_thi_toan_thpt/hoc_lieu/d0/index.qmd':
            records.append({'source': name, 'path': source.with_suffix('.pdf').relative_to(root).as_posix(),
                            'variant': 'full', 'contract': 'd0'})
            continue
        config = discover_project_config(root, Path(name))
        variants = config.raw.get('extensions', {}).get('pdf_variants') if config else None
        canonical = canonical_pdf_provenance_enabled(root, source)
        for variant in (variants if variants is not None else ['full']):
            pdf_variant(root, source, variant)  # Validate output names/collisions.
            record = {'source': name, 'path': pdf_output_path(root, source, variant).relative_to(root).as_posix(),
                      'variant': variant, 'contract': 'canonical' if canonical else 'build-receipt'}
            if evidence and not canonical:
                receipt = pdf_build_receipt_path(root, source, variant)
                try:
                    record['build_receipt'] = json.loads(receipt.read_text(encoding='utf-8'))
                except (OSError, ValueError):
                    record['build_receipt'] = None
            records.append(record)
    if len({record['path'] for record in records}) != len(records):
        raise p.ConfigError('Selected sources declare overlapping PDF outputs.')
    return records


def validate_pdfs(source_root, records, config, candidate=None):
    """Check only selected PDFs; unchanged published PDFs need no rebuild."""
    from zo_publish_pages import d0_pdf_issues
    issues = []
    sources = sorted({record['source'] for record in records})
    expected = selected_pdfs(source_root, sources, evidence=False)
    identity = lambda record: {key: record.get(key) for key in ('source', 'path', 'variant', 'contract')}
    if sorted(map(identity, records), key=lambda r: r['path']) != sorted(expected, key=lambda r: r['path']):
        return [{'type': 'page-pdf-scope', 'message': 'PDF list differs from selected source definitions.'}]
    for record in records:
        name = p.safe_relative(record['path'], 'selected PDF')
        file = source_root / name
        errors = []
        if (not p.path_allowed(name, config['allowlist']['files'], config['allowlist']['globs'])
                or p.path_denied(name, config['denylist']['paths'], config['denylist']['globs'])):
            errors.append('PDF is not public/allowlisted')
        if not file.is_file() or file.is_symlink() or not file.resolve().is_relative_to(source_root.resolve()):
            errors.append('Missing or unsafe canonical PDF')
        if not errors:
            try:
                if not PdfReader(file).pages:
                    errors.append('PDF contains no pages')
            except Exception as exc:
                errors.append('Unreadable PDF: '+str(exc))
        if not errors:
            if record['contract'] == 'd0':
                issues.extend(d0_pdf_issues(candidate or source_root, source_root))
            elif record['contract'] == 'canonical':
                errors.extend(validate_canonical_pdf_provenance(
                    source_root, source_root / record['source'], variant=record['variant']))
            else:
                # Seal existing build evidence into the prepare receipt. Final
                # validation is independent of disposable audit history, and
                # still rechecks every source/pipeline/output hash.
                if not isinstance(record.get('build_receipt'), dict):
                    errors.append('Missing PDF build receipt; build this source PDF first')
                else:
                    with tempfile.TemporaryDirectory(prefix='zo-pdf-evidence-') as temp:
                        receipt = Path(temp) / 'receipt.json'
                        receipt.write_text(json.dumps(record['build_receipt']), encoding='utf-8')
                        errors.extend(validate_pdf_build_receipt(
                            source_root, source_root / record['source'], file, receipt,
                            variant=record['variant']))
            if candidate is not None:
                output = candidate / name
                if not output.is_file() or p.sha256(output) != p.sha256(file):
                    errors.append('Candidate PDF differs from canonical PDF')
        if errors:
            issues.append({'type': 'page-pdf-provenance', 'path': name, 'errors': errors})
    return issues
