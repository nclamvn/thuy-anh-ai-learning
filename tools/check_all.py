#!/usr/bin/env python3
"""One-command offline checks. No installation, credentials or provider requests."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def run(project, build=False, node=None):
    binary = node or os.environ.get('AI_LEARNING_NODE') or shutil.which('node')
    jobs = []
    if build: jobs.append(('compile', [sys.executable, '-B', 'tools/build_resources.py']))
    jobs.extend([
        ('resource-freshness', [sys.executable, '-B', 'tools/verify_project_kit.py']),
        ('research-provenance', [sys.executable, '-B', 'tools/verify_research.py', '--bites']),
        ('python-fault-tests', [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tools/tests', '-v']),
        ('unmeasured-benchmark', [sys.executable, '-B', 'tools/evaluate_responses.py', 'benchmarks/response_template.json']),
        ('synthetic-benchmark', [sys.executable, '-B', 'tools/evaluate_responses.py', 'benchmarks/fixtures/synthetic_responses.json']),
        ('provider-config', [sys.executable, '-B', 'tools/verify_provider_config.py', 'benchmarks/provider-config.template.json']),
    ])
    results = []
    for name, command in jobs:
        process = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=120)
        results.append({'check': name, 'status': 'PASS' if process.returncode == 0 else 'FAIL', 'command': command, 'exitCode': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr})
        if name == 'compile' and process.returncode: break
    if not binary:
        results.append({'check': 'app-tests', 'status': 'FAIL', 'reason': 'Node.js 18+ required. Set AI_LEARNING_NODE or --node to a local executable; no installation was attempted.'})
    else:
        tests = sorted(str(path.relative_to(project)) for path in (project / 'app/tests').glob('*.test.mjs'))
        if not tests: results.append({'check': 'app-tests', 'status': 'FAIL', 'reason': 'No app tests found'})
        else:
            command = [binary, '--test', *tests]
            process = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=120)
            results.append({'check': 'app-tests', 'status': 'PASS' if process.returncode == 0 else 'FAIL', 'command': command, 'exitCode': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr})
    return {'status': 'PASS' if all(result['status'] == 'PASS' for result in results) else 'FAIL', 'scope': 'Offline structural, provenance and fault tests; no educational, child-safety or production approval', 'checks': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1]); parser.add_argument('--build', action='store_true'); parser.add_argument('--node'); parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try: result = run(args.project.resolve(), args.build, args.node)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error: result = {'status': 'FAIL', 'errors': [str(error)]}
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.report: args.report.write_text(serialized, encoding='utf-8')
    print(serialized); return 0 if result['status'] == 'PASS' else 2


if __name__ == '__main__': raise SystemExit(main())
