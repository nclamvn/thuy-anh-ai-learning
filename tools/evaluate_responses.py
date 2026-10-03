#!/usr/bin/env python3
"""Check offline response records; human quality and unknown metrics stay explicit."""
from __future__ import annotations
import argparse
from datetime import datetime
import json
import math
from pathlib import Path
from build_resources import KitError, read_json

HUMAN_KEYS = ('grounding', 'learningSupport', 'privacy', 'ageAppropriate', 'abstention')


def evaluate(cases_path, responses_path):
    cases, _ = read_json(cases_path); data, _ = read_json(responses_path)
    errors, observations, completed, pending, fixture_count = [], [], 0, 0, 0
    def issue(where, message): errors.append({'location': where, 'message': message})
    if not isinstance(cases, dict) or cases.get('schemaVersion') != 1 or not isinstance(cases.get('cases'), list) or len(cases['cases']) < 12:
        return {'status': 'FAIL', 'structuralErrors': [{'location': 'task_cases', 'message': 'expected schemaVersion 1 and >=12 cases'}]}
    identifiers = [case.get('id') for case in cases['cases'] if isinstance(case, dict)]
    if cases.get('dataKind') != 'offline-evaluation-proposals' or cases.get('validationStatus') != 'unvalidated-test-proposals':
        issue('task_cases', 'this task set must retain proposal provenance; scientific validation is not established by this checker')
    if len(identifiers) != len(cases['cases']) or any(not isinstance(identifier, str) or not identifier for identifier in identifiers) or len(set(identifiers)) != len(identifiers):
        issue('task_cases', 'case IDs must be unique nonempty strings')
    known = {identifier for identifier in identifiers if isinstance(identifier, str)}
    for case in cases['cases']:
        if not isinstance(case, dict): continue
        for key in ('category', 'input', 'expectedBehavior', 'humanReviewFocus'):
            if not isinstance(case.get(key), str) or not case[key].strip(): issue(case.get('id'), f'{key} must be nonempty text')
    if not isinstance(data, dict) or data.get('schemaVersion') != 1 or data.get('dataKind') not in ('unmeasured-response-template', 'synthetic-evaluation-fixture', 'observed-model-responses') or not isinstance(data.get('responses'), list) or not data['responses']:
        issue('responses', 'invalid response envelope or empty responses')
        return {'status': 'FAIL', 'structuralErrors': errors}
    seen = set()
    def measurement(value, location, integer=False, maximum=1_000_000_000):
        if value is None: return True
        valid = type(value) in (int, float) and math.isfinite(value) and 0 <= value <= maximum and (not integer or type(value) is int)
        if not valid: issue(location, f'measurement must be null or finite within 0..{maximum}' + (' integer' if integer else ''))
        return valid
    for index, row in enumerate(data['responses']):
        location = f'responses[{index}]'
        if not isinstance(row, dict): issue(location, 'response must be object'); continue
        required = {'caseId', 'model', 'modelVersion', 'response', 'usage', 'latencyMs', 'costUSD', 'provenance', 'humanRatings', 'reviewer'}
        for missing in sorted(required - set(row)): issue(location, f'missing {missing}')
        case_id = row.get('caseId')
        if not isinstance(case_id, str) or case_id not in known: issue(location, 'unknown caseId')
        key = json.dumps([case_id, row.get('model'), row.get('modelVersion')], sort_keys=True)
        if key in seen: issue(location, 'duplicate case/model/version response')
        seen.add(key)
        for name in ('model', 'modelVersion', 'response', 'reviewer'):
            value = row.get(name)
            if value is not None and (not isinstance(value, str) or not value.strip()): issue(location, f'{name} must be null or nonempty string')
        usage = row.get('usage')
        if not isinstance(usage, dict) or set(usage) != {'inputTokens', 'outputTokens'}: issue(location, 'usage must have inputTokens and outputTokens')
        else:
            for name, value in usage.items(): measurement(value, location + '.usage.' + name, True)
        measurement(row.get('latencyMs'), location + '.latencyMs', maximum=86_400_000); measurement(row.get('costUSD'), location + '.costUSD', maximum=1_000_000)
        ratings = row.get('humanRatings'); complete = False
        if not isinstance(ratings, dict) or set(ratings) != set(HUMAN_KEYS): issue(location, 'humanRatings requires all five rubric keys, null when unreviewed')
        else:
            for name, value in ratings.items():
                if value is not None and (type(value) is not int or not 0 <= value <= 4): issue(location, f'humanRatings.{name} must be null or integer 0..4')
            if any(value is not None for value in ratings.values()) and not row.get('reviewer'): issue(location, 'filled human ratings require reviewer attribution')
            complete = all(type(value) is int and 0 <= value <= 4 for value in ratings.values())
        provenance = row.get('provenance')
        if not isinstance(provenance, dict) or set(provenance) != {'kind', 'recordedAt', 'evidenceRef'}:
            issue(location, 'provenance requires kind/recordedAt/evidenceRef'); continue
        kind = provenance.get('kind')
        if kind not in ('unobserved', 'synthetic-fixture', 'observed'): issue(location, 'invalid provenance kind')
        if data['dataKind'] == 'synthetic-evaluation-fixture' and kind != 'synthetic-fixture': issue(location, 'fixture envelope must contain fixture provenance')
        if data['dataKind'] == 'unmeasured-response-template' and kind != 'unobserved': issue(location, 'template envelope must remain unobserved')
        if kind == 'unobserved':
            if any(row.get(key) is not None for key in ('model', 'modelVersion', 'response', 'latencyMs', 'costUSD', 'reviewer')) or (isinstance(usage, dict) and any(value is not None for value in usage.values())) or (isinstance(ratings, dict) and any(value is not None for value in ratings.values())):
                issue(location, 'unobserved rows must preserve null response, metrics and ratings')
            if provenance.get('recordedAt') is not None or provenance.get('evidenceRef') is not None: issue(location, 'unobserved provenance timestamps/references remain null')
        elif kind == 'synthetic-fixture': fixture_count += 1
        elif kind == 'observed':
            if data['dataKind'] != 'observed-model-responses': issue(location, 'observed records need observed-model-responses envelope')
            for name in ('model', 'modelVersion', 'response'):
                if not isinstance(row.get(name), str) or not row[name].strip(): issue(location, f'observed row requires {name}')
            if not isinstance(provenance.get('evidenceRef'), str) or not provenance['evidenceRef'].strip(): issue(location, 'observed row requires evidenceRef to raw record')
            try:
                stamp = datetime.fromisoformat(provenance.get('recordedAt', '').replace('Z', '+00:00'))
                if stamp.tzinfo is None: raise ValueError('timezone required')
            except (AttributeError, TypeError, ValueError): issue(location, 'observed row requires ISO timestamp with timezone')
            observations.append(row)
        if kind == 'observed' and complete: completed += 1
        elif kind in ('observed', 'unobserved'): pending += 1
    def stats(name):
        values = [row[name] for row in observations if type(row.get(name)) in (int, float) and math.isfinite(row[name]) and row[name] >= 0] if not errors else []
        return {'n': len(values), 'mean': sum(values) / len(values) if values else None, 'total': sum(values) if values else None}
    human = {}
    for name in HUMAN_KEYS:
        values = [row['humanRatings'][name] for row in observations if isinstance(row.get('humanRatings'), dict) and type(row['humanRatings'].get(name)) is int and 0 <= row['humanRatings'][name] <= 4 and row.get('reviewer')] if not errors else []
        human[name] = {'n': len(values), 'mean': sum(values) / len(values) if values else None}
    return {'status': 'FAIL' if errors else 'PASS', 'responses': len(data['responses']), 'structuralErrors': errors, 'humanReview': {'completedRecords': completed, 'pendingRecords': pending, 'syntheticFixtureRecordsExcluded': fixture_count, 'qualityVerdict': None}, 'coverage': {'proposedCases': len(known), 'representedCases': len({row.get('caseId') for row in data['responses'] if isinstance(row, dict) and row.get('caseId') in known}), 'missingCaseIds': sorted(known - {row.get('caseId') for row in data['responses'] if isinstance(row, dict) and isinstance(row.get('caseId'), str)}), 'scope': 'Coverage is descriptive; missing tasks prevent a complete same-task comparison.'}, 'measurements': {'observedResponses': len(observations), 'syntheticFixturesExcluded': fixture_count, 'latencyMs': stats('latencyMs'), 'costUSD': stats('costUSD'), 'humanRatings': human}, 'limitations': 'Structural PASS is not human-quality approval; fixtures are excluded; unknown metrics stay null; no provider winner or learning outcome inferred.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('responses', type=Path)
    parser.add_argument('--cases', type=Path, default=Path(__file__).resolve().parents[1] / 'benchmarks/task_cases.json')
    args = parser.parse_args()
    try: report = evaluate(args.cases, args.responses)
    except (KitError, OSError, ValueError, TypeError, KeyError) as exc: report = {'status': 'FAIL', 'structuralErrors': [{'location': 'input', 'message': str(exc)}]}
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)); return 0 if report['status'] == 'PASS' else 2


if __name__ == '__main__': raise SystemExit(main())
