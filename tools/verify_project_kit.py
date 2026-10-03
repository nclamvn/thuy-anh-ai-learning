#!/usr/bin/env python3
"""Offline validation of materials, local links and generated-resource freshness."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from build_resources import KitError, prepare, markdown_links


def verify(project):
    project = project.resolve(); errors, checked_links = [], 0
    try:
        payloads, manifest, catalog, lessons = prepare(project)
    except (KitError, OSError, TypeError, KeyError) as exc:
        return {'status': 'FAIL', 'errors': [str(exc)], 'checkedLinks': 0}
    resource_root = project / 'app/resources'
    if (resource_root.is_symlink() or (project / 'app').is_symlink() or
            not resource_root.resolve().is_relative_to(project) or not resource_root.is_dir()):
        errors.append('generated app/resources must be a regular project directory')
    else:
        actual = {str(path.relative_to(resource_root)) for path in resource_root.rglob('*') if path.is_file()}
        expected = set(payloads)
        for extra in sorted(actual - expected): errors.append(f'stale/unlisted generated resource: {extra}')
        for relative, raw in payloads.items():
            path = resource_root / relative
            if not path.is_file(): errors.append(f'generated resource missing: {relative}')
            elif path.is_symlink() or not path.resolve().is_relative_to(resource_root.resolve()): errors.append(f'generated resource symlink forbidden: {relative}')
            elif path.read_bytes() != raw: errors.append(f'generated resource stale/fingerprint mismatch: {relative}')
    for path in sorted((project / 'materials').rglob('*.md')):
        if not path.resolve().is_relative_to((project / 'materials').resolve()):
            errors.append(f'material symlink escapes: {path.relative_to(project)}'); continue
        try: content = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append(str(exc)); continue
        for href in markdown_links(content):
            checked_links += 1
            parsed = urlsplit(href)
            if parsed.scheme in ('http', 'https', 'mailto'): continue
            if parsed.scheme or parsed.netloc or href.startswith('/') or '\\' in href:
                errors.append(f'unsafe local link {path.relative_to(project)}: {href}'); continue
            if not parsed.path: continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(project): errors.append(f'local link escapes project {path.relative_to(project)}: {href}')
            elif not resolved.exists(): errors.append(f'dead local link {path.relative_to(project)}: {href}')
    generated_links = sum(len(markdown_links(raw.decode('utf-8'))) for relative, raw in payloads.items() if relative.endswith('.md'))
    return {'status': 'FAIL' if errors else 'PASS', 'catalogItems': len(catalog['items']), 'translatedDocuments': sum('en' in item.get('translations', {}) for item in catalog['items']), 'translatedLessons': sum('en' in lesson.get('translations', {}) for lesson in lessons['lessons']), 'lessons': len(lessons['lessons']), 'generatedFiles': len(payloads), 'checkedLinks': checked_links, 'checkedGeneratedLinks': generated_links, 'fingerprint': manifest['fingerprint'], 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1]); args = parser.parse_args()
    try: report = verify(args.project)
    except (OSError, ValueError, TypeError) as exc: report = {'status': 'FAIL', 'errors': [str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2)); return 0 if report['status'] == 'PASS' else 2


if __name__ == '__main__': raise SystemExit(main())
