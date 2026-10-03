#!/usr/bin/env python3
"""Build a portable local ZIP from explicit public project directories and files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
from build_resources import KitError, read_json, require
from verify_project_kit import verify
from evaluate_responses import evaluate
from verify_research import verify as verify_research

EXCLUDED = {'qa', 'private', 'backup', 'backups', '_backup', 'archive', 'archives', 'conversations', 'conversation', 'node_modules', '__pycache__', '.git', '.venv', '.env', 'staging', 'runtime', 'exports', 'observed', 'raw-records'}
ALLOWED_EXTENSIONS = {'.md', '.csv', '.json', '.jsonl', '.yaml', '.py', '.html', '.css', '.js', '.mjs', '.svg', '.ttf', '.otf', '.woff', '.woff2', '.txt', '.png', '.webp', '.yml', '.sh', '.pdf'}
ROOT_FILES = ('README.md', 'AGENTS.md', 'start-local.command')


def collect(project, release='P03'):
    project = project.resolve(); collected = {}
    def add(logical, path):
        require(path.resolve().is_relative_to(project), f'package symlink escapes project: {logical}')
        require(not path.is_symlink(), f'package file symlink forbidden: {logical}')
        require(path.is_file(), f'package input missing: {logical}')
        require(path.stat().st_size <= 20 * 1024 * 1024, f'package input exceeds 20MiB: {logical}')
        collected[logical] = path.read_bytes()
    for name in ROOT_FILES: add(name, project / name)
    if (project / 'requirements.txt').is_file(): add('requirements.txt', project / 'requirements.txt')
    for dirname in ('app', 'materials', 'benchmarks', 'tools'):
        root = project / dirname; require(root.is_dir(), f'package input missing: {dirname}')
        for path in sorted(root.rglob('*')):
            if not path.is_file(): continue
            parts = path.relative_to(root).parts
            if any(part.lower() in EXCLUDED or part.startswith('.') for part in parts): continue
            if path.suffix.lower() not in ALLOWED_EXTENSIONS: continue
            name = path.name.lower()
            if name.startswith(('private', 'conversation', 'raw-conversation', 'qa-', 'observed-', 'export-', 'state-')): continue
            if dirname == 'benchmarks' and path.suffix.lower() != '.md' and path.relative_to(root).as_posix() not in {'task_cases.json', 'response_template.json', 'fixtures/synthetic_responses.json', 'provider-config.template.json'}: continue
            if dirname == 'app' and path.suffix.lower() == '.json' and path.relative_to(root).as_posix() != 'package.json' and parts[0] != 'resources': continue
            add(path.relative_to(project).as_posix(), path)
    for path in sorted((project / 'delivery').glob('*.md')):
        if path.name.startswith(('BLUEPRINT-', 'TIP-', 'COMPLETION-')) or path.name in ('HUMAN-WORK-KIT.md', 'RESEARCH-DECISIONS.md', 'RUNTIME-CHECKS.md'):
            add(path.relative_to(project).as_posix(), path)
    for name in ('VERIFY-P02.json', 'VERIFY-R01.json', 'VERIFY-M01.json', 'VERIFY-P03.json', 'P03-tool-receipts.json'):
        path = project / 'delivery' / name
        if path.is_file(): add('delivery/' + name, path)
    workflow = project / '.github/workflows/checks.yml'
    if workflow.is_file(): add('.github/workflows/checks.yml', workflow)
    # Public foundation references only; no baseline tokens/logs, exports or QA
    # state. Canonical data is preserved as reference, research is also emitted
    # as ordinary files so stdlib tools work after extraction without symlinks.
    supplemental_path = project / 'research/fulltexts/capture-manifest.json'
    fulltext_allowlist = {'capture-manifest.json'}
    if supplemental_path.is_file():
        supplemental_data, _ = read_json(supplemental_path)
        fulltext_allowlist.update(row['file'] for row in supplemental_data['captures'] if row.get('status') == 'captured')
    for dirname in ('source_canonical', 'registry', 'adapters'):
        root = project / 'sot' / dirname
        if not root.is_dir(): continue
        for path in sorted(root.rglob('*')):
            if not path.is_file(): continue
            parts = path.relative_to(root).parts
            if dirname == 'source_canonical' and len(parts) >= 3 and parts[:2] == ('research', 'fulltexts') and parts[-1] not in fulltext_allowlist: continue
            if any(part.startswith('.') or part.lower() in EXCLUDED for part in parts): continue
            if path.suffix.lower() not in ALLOWED_EXTENSIONS: continue
            add(path.relative_to(project).as_posix(), path)
    for name in ('README.md', 'PROJECT.yaml', 'sot.yaml', 'sot.hygiene.yaml'):
        path = project / 'sot' / name
        if path.is_file(): add('sot/' + name, path)
    sources, _ = read_json(project / 'research/sources.json')
    for name in ('sources.json', 'domain.yaml', 'claims.jsonl'): add('research/' + name, project / 'research' / name)
    for source in sources:
        if source.get('capture_status') == 'captured':
            relative = source['snapshot']
            require(isinstance(relative, str) and not Path(relative).is_absolute() and '..' not in Path(relative).parts, 'unsafe research snapshot in package')
            add('research/' + relative, project / 'research' / relative)
    supplemental = project / 'research/fulltexts/capture-manifest.json'
    if supplemental.is_file():
        supplement, _ = read_json(supplemental)
        add('research/fulltexts/capture-manifest.json', supplemental)
        for capture in supplement['captures']:
            if capture.get('status') == 'captured':
                add('research/fulltexts/' + capture['file'], project / 'research/fulltexts' / capture['file'])
    return collected


def package(project, destination=None, release='P03'):
    project = project.resolve()
    require(release == 'P03', 'only P03 packaging is supported; historical P02 archive is immutable')
    release_report, _ = read_json(project / 'delivery/VERIFY-P03.json')
    require(isinstance(release_report, dict) and release_report.get('status') == 'PASS', 'Contractor VERIFY-P03 must have status PASS before packaging')
    report = verify(project); require(report['status'] == 'PASS', f'kit verification failed: {report.get("errors")}')
    research = verify_research(project); require(research['status'] == 'PASS', f'research verification failed: {research.get("errors")}')
    for name in ('response_template.json', 'fixtures/synthetic_responses.json'):
        benchmark = evaluate(project / 'benchmarks/task_cases.json', project / 'benchmarks' / name)
        require(benchmark['status'] == 'PASS', f'benchmark structure failed: {name}')
    files = collect(project, release)
    files['PACKAGE-MANIFEST.json'] = (json.dumps({'schemaVersion': 1, 'dataKind': 'portable-local-kit', 'release': release, 'files': {name: {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)} for name, raw in sorted(files.items())}, 'limits': 'Local draft project; excludes QA backups, private notes, environments and historical screenshots.'}, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    destination = destination or project / 'delivery/PROJECT-P03-local.zip'; destination = destination.resolve()
    require(destination.name != 'PROJECT-P02-local.zip', 'historical P02 archive is immutable')
    require(destination.is_relative_to(project), 'package destination must be inside project')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix='.local-package-', suffix='.zip', dir=destination.parent, delete=False) as temporary:
        stage = Path(temporary.name)
    try:
        with zipfile.ZipFile(stage, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for name, raw in sorted(files.items()):
                info = zipfile.ZipInfo('thuy-anh-ai-learning/' + name, date_time=(2026, 10, 3, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED; info.create_system = 3
                mode = 0o100755 if name == 'start-local.command' else 0o100644
                info.external_attr = mode << 16
                archive.writestr(info, raw)
        with zipfile.ZipFile(stage) as archive:
            require(archive.testzip() is None, 'ZIP integrity test failed')
        stage.replace(destination)
    finally:
        if stage.exists(): stage.unlink()
    return {'status': 'PASS', 'fileCount': len(files), 'bytes': destination.stat().st_size, 'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(), 'path': str(destination)}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1]); parser.add_argument('--output', type=Path); args = parser.parse_args()
    try: result = package(args.project, args.output)
    except (KitError, OSError, TypeError, KeyError, ValueError) as exc: result = {'status': 'FAIL', 'errors': [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if result['status'] == 'PASS' else 2


if __name__ == '__main__': raise SystemExit(main())
