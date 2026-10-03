#!/usr/bin/env python3
"""Deterministic, offline provenance gate for the project's research foundation.

domain.yaml must use JSON syntax (a YAML subset). PASS confirms internal
provenance integrity, not source truth or educational effectiveness.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata


def normalized(text: str) -> str:
    return unicodedata.normalize("NFC", html.unescape(text))


def load_json(text: str):
    def reject_constant(value):
        raise ValueError(f"nonstandard JSON constant {value}")

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON object key {key}")
            result[key] = value
        return result

    return json.loads(text, parse_constant=reject_constant, object_pairs_hook=unique_object)


def verify(project: Path) -> dict:
    errors: list[dict] = []
    project_root = project.resolve()
    research = (project_root / "research").resolve()
    report = {"status": "FAIL", "sources": 0, "claims": 0, "errors": errors}

    def error(code: str, location: str, message: str) -> None:
        errors.append({"code": code, "location": location, "message": message})

    if not research.is_relative_to(project_root):
        error("RESEARCH_PATH", "research", "research directory must remain inside project")
        return report

    def read_json(path: Path):
        try:
            return load_json(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            error("INPUT_INVALID", str(path.relative_to(project.resolve())), str(exc))
            return None

    sources = read_json(research / "sources.json")
    domain = read_json(research / "domain.yaml")
    claims = []
    try:
        for line_number, line in enumerate((research / "claims.jsonl").read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                claim = load_json(line)
                if not isinstance(claim, dict):
                    raise ValueError("claim must be a JSON object")
                claims.append((line_number, claim))
            except ValueError as exc:
                error("INPUT_INVALID", f"research/claims.jsonl:{line_number}", str(exc))
    except (OSError, UnicodeError) as exc:
        error("INPUT_INVALID", "research/claims.jsonl", str(exc))
    report["claims"] = len(claims)
    if not isinstance(sources, list) or not sources:
        error("MANIFEST_SCHEMA", "research/sources.json", "expected a nonempty source array")
        sources = []
    report["sources"] = len(sources)
    if not claims:
        error("CLAIMS_EMPTY", "research/claims.jsonl", "expected at least one claim")

    fields: list = []
    tiers: list = []
    extractions: list = []
    unknown_fields: list = []
    if not isinstance(domain, dict):
        error("DOMAIN_SCHEMA", "research/domain.yaml", "expected JSON-syntax YAML object")
    else:
        schema, verification = domain.get("schema"), domain.get("verification")
        for name, owner, key in (
            ("fields", schema, "fields"),
            ("tiers", verification, "allowed_tiers"),
            ("extractions", verification, "allowed_extractions"),
            ("unknown_fields", verification, "unknown_fields"),
        ):
            value = owner.get(key) if isinstance(owner, dict) else None
            if (not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value)
                    or len(set(value)) != len(value) or (name != "unknown_fields" and not value)):
                error("DOMAIN_SCHEMA", f"research/domain.yaml:{key}", "expected unique nonempty strings in an array")
            else:
                if name == "fields":
                    fields = value
                elif name == "tiers":
                    tiers = value
                elif name == "extractions":
                    extractions = value
                else:
                    unknown_fields = value
        if not set(unknown_fields).issubset(fields):
            error("DOMAIN_SCHEMA", "research/domain.yaml:unknown_fields", "unknown fields must be declared schema fields")
        if "source_statement" not in fields or "verbatim" not in extractions:
            error("DOMAIN_SCHEMA", "research/domain.yaml", "source_statement field and verbatim extraction are required")

    by_id: dict[str, dict] = {}
    snapshots: dict[str, str] = {}
    for index, source in enumerate(sources):
        location = f"research/sources.json:{index + 1}"
        if not isinstance(source, dict):
            error("MANIFEST_SCHEMA", location, "source must be an object")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id:
            error("SOURCE_ID", location, "source id must be a nonempty string")
            continue
        if source_id in by_id:
            error("SOURCE_DUPLICATE", location, f"duplicate source id {source_id}")
            continue
        by_id[source_id] = source
        for key in ("url", "origin"):
            if not isinstance(source.get(key), str) or not source[key]:
                error("MANIFEST_SCHEMA", location, f"{key} must be a nonempty string")
        if source.get("tier") not in tiers:
            error("SOURCE_TIER", location, "tier is not allowed by domain")
        status = source.get("capture_status")
        if status not in ("captured", "unavailable"):
            error("CAPTURE_STATUS", location, "expected captured or unavailable")
            continue
        if status == "unavailable":
            continue
        snapshot = source.get("snapshot")
        if not isinstance(snapshot, str) or not snapshot:
            error("SNAPSHOT_PATH", location, "captured source requires snapshot")
            continue
        path = (research / snapshot).resolve()
        if Path(snapshot).is_absolute() or not path.is_relative_to(research):
            error("SNAPSHOT_PATH", location, "snapshot must remain inside project research directory")
            continue
        try:
            raw = path.read_bytes()
            if source.get("sha256") != hashlib.sha256(raw).hexdigest():
                error("SNAPSHOT_HASH", location, "SHA-256 does not match snapshot bytes")
            if not isinstance(source.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
                error("MANIFEST_HASH", location, "sha256 must contain 64 lowercase hexadecimal characters")
            if "bytes" in source and (type(source["bytes"]) is not int or source["bytes"] != len(raw)):
                error("SNAPSHOT_BYTES", location, "bytes metadata does not match snapshot")
            snapshots[source_id] = normalized(raw.decode("utf-8"))
        except (OSError, UnicodeError) as exc:
            error("SNAPSHOT_INVALID", location, str(exc))

    seen = set()
    for line_number, claim in claims:
        location = f"research/claims.jsonl:{line_number}"
        source_id, field = claim.get("entity"), claim.get("field")
        if not isinstance(source_id, str) or source_id not in by_id:
            error("CLAIM_SOURCE", location, "entity must identify a manifest source")
            source = None
        else:
            source = by_id[source_id]
        if not isinstance(field, str) or field not in fields:
            error("CLAIM_FIELD", location, "field is not allowed by domain")
        if isinstance(field, str) and field in unknown_fields:
            error("UNKNOWN_ASSERTED", location, "unknown research field must remain without a claim")
        if claim.get("tier") not in tiers:
            error("CLAIM_TIER", location, "tier is not allowed by domain")
        if claim.get("extraction") not in extractions:
            error("CLAIM_EXTRACTION", location, "extraction is not allowed by domain")
        span, value, capture = claim.get("evidence_span"), claim.get("value"), claim.get("capture")
        if not isinstance(span, str) or not span.strip():
            error("EVIDENCE_INVALID", location, "evidence_span must be a nonempty string")
        if (value is None or isinstance(value, (dict, list, bool)) or
                (isinstance(value, float) and not math.isfinite(value)) or
                (isinstance(value, str) and not value.strip())):
            error("VALUE_INVALID", location, "claim value must be a nonempty string or number; unknowns remain absent")
        if field == "source_statement" and (claim.get("extraction") != "verbatim" or value != span):
            error("VERBATIM_MISMATCH", location, "source_statement requires verbatim extraction and value exactly equal to evidence_span")
        if not isinstance(capture, dict):
            error("CAPTURE_INVALID", location, "capture must be an object")
            capture = {}
        duplicate_key = json.dumps([source_id, field, value, capture.get("source")], ensure_ascii=False, sort_keys=True)
        if duplicate_key in seen:
            error("CLAIM_DUPLICATE", location, "duplicate entity+field+value+source")
        seen.add(duplicate_key)
        if source is None:
            continue
        if source.get("capture_status") != "captured":
            error("SOURCE_UNAVAILABLE", location, "unavailable sources cannot provide evidence")
            continue
        if capture.get("url") != source.get("url") or capture.get("source") != source.get("origin"):
            error("CAPTURE_MISMATCH", location, "capture url/source must match manifest url/origin")
        manifest_snapshot = source.get("snapshot")
        if not isinstance(manifest_snapshot, str) or capture.get("snapshot") != Path(manifest_snapshot).name:
            error("CAPTURE_SNAPSHOT", location, "capture snapshot must equal manifest snapshot basename")
        if claim.get("tier") != source.get("tier"):
            error("TIER_MISMATCH", location, "claim tier must match source tier")
        if isinstance(span, str) and source_id in snapshots and normalized(span) not in snapshots[source_id]:
            error("EVIDENCE_ABSENT", location, "normalized evidence_span is absent from captured snapshot")
    supplementary_path = research / 'fulltexts/capture-manifest.json'
    report['supplementary'] = {'capturedFiles': 0, 'failedAttempts': 0, 'independentSourceIncrement': 0}
    if supplementary_path.exists():
        supplementary = read_json(supplementary_path)
        if not isinstance(supplementary, dict) or supplementary.get('kind') != 'supplementary-fulltext-captures' or supplementary.get('not_independent_sources') is not True or not isinstance(supplementary.get('captures'), list):
            error('SUPPLEMENT_SCHEMA', 'research/fulltexts/capture-manifest.json', 'expected supplementary captures with no independent-source increment')
        else:
            fulltexts = (research / 'fulltexts').resolve(); captured_files = set()
            if not fulltexts.is_relative_to(research):
                error('SUPPLEMENT_PATH', 'research/fulltexts', 'fulltexts directory must stay inside research')
            else:
                failed_attempts = supplementary.get('failed_attempts', [])
                if not isinstance(failed_attempts, list):
                    error('SUPPLEMENT_SCHEMA', 'research/fulltexts/capture-manifest.json', 'failed_attempts must be an array'); failed_attempts = []
                for index, capture in enumerate(supplementary['captures'] + failed_attempts):
                    location = f'research/fulltexts/capture-manifest.json:{index + 1}'
                    if not isinstance(capture, dict):
                        error('SUPPLEMENT_SCHEMA', location, 'capture must be an object'); continue
                    if not isinstance(capture.get('sourceId'), str) or capture['sourceId'] not in by_id:
                        error('SUPPLEMENT_SOURCE', location, 'sourceId must identify an existing source; fulltext is not a new independent source')
                    relative = capture.get('file')
                    if not isinstance(relative, str) or not re.fullmatch(r'[A-Za-z0-9_-]+\.(pdf|html)', relative):
                        error('SUPPLEMENT_PATH', location, 'capture file must be a plain PDF/HTML basename'); continue
                    path = fulltexts / relative
                    if path.is_symlink() or not path.resolve().is_relative_to(fulltexts):
                        error('SUPPLEMENT_PATH', location, 'supplement file symlink/escape forbidden'); continue
                    status = capture.get('status')
                    if index >= len(supplementary['captures']) and status != 'unavailable':
                        error('SUPPLEMENT_SCHEMA', location, 'failed_attempts must stay unavailable'); continue
                    if status == 'unavailable':
                        report['supplementary']['failedAttempts'] += 1
                        if not isinstance(capture.get('error'), str) or not capture['error'].strip(): error('SUPPLEMENT_SCHEMA', location, 'unavailable attempt requires error')
                        continue
                    if status != 'captured':
                        error('SUPPLEMENT_SCHEMA', location, 'expected captured or unavailable'); continue
                    if relative in captured_files:
                        error('SUPPLEMENT_DUPLICATE', location, 'duplicate valid fulltext file'); continue
                    captured_files.add(relative); report['supplementary']['capturedFiles'] += 1
                    if capture.get('http_status') != 200 or type(capture.get('http_status')) is not int:
                        error('SUPPLEMENT_HTTP', location, 'valid capture must record HTTP 200')
                    if not isinstance(capture.get('url'), str) or not capture['url'].startswith('https://') or not isinstance(capture.get('final_url'), str) or not capture['final_url'].startswith('https://'):
                        error('SUPPLEMENT_SCHEMA', location, 'capture requires original/final HTTPS URLs')
                    try:
                        raw = path.read_bytes()
                        if len(raw) > 20 * 1024 * 1024: error('SUPPLEMENT_BYTES', location, 'fulltext exceeds 20MiB')
                        if type(capture.get('bytes')) is not int or capture['bytes'] != len(raw): error('SUPPLEMENT_BYTES', location, 'bytes metadata mismatch')
                        if not isinstance(capture.get('sha256'), str) or capture['sha256'] != hashlib.sha256(raw).hexdigest(): error('SUPPLEMENT_HASH', location, 'SHA-256 mismatch')
                        if relative.endswith('.pdf'):
                            if not raw.startswith(b'%PDF-') or len(raw) < 20 or b'%%EOF' not in raw[-2048:]: error('SUPPLEMENT_CONTENT', location, 'PDF signature/trailer absent; not a verified PDF capture')
                        else:
                            content = raw.decode('utf-8')
                            if not re.search(r'<(?:html|article|main)\b', content, re.I) or not re.search(r'<(?:p|h[1-6])\b', content, re.I): error('SUPPLEMENT_CONTENT', location, 'HTML document body required')
                            if re.search(r'(verify (?:you are|that you are) human|just a moment|enable javascript and cookies to continue|checking your browser)', content, re.I): error('SUPPLEMENT_CONTENT', location, 'challenge response is not publication content')
                    except (OSError, UnicodeError) as exc:
                        error('SUPPLEMENT_CONTENT', location, str(exc))
    report["status"] = "FAIL" if errors else "PASS"
    return report


def run_bites(project: Path) -> list[dict]:
    """Mutate independent temporary research copies and execute the CLI gate."""
    results = []
    mutations = (
        ("snapshot_bytes", "SNAPSHOT_HASH"),
        ("claim_value", "VERBATIM_MISMATCH"),
        ("duplicate_claim", "CLAIM_DUPLICATE"),
        ("capture_url", "CAPTURE_MISMATCH"),
        ("manifest_hash", "SNAPSHOT_HASH"),
        ("unavailable_source", "SOURCE_UNAVAILABLE"),
    )
    for name, expected_code in mutations:
        with tempfile.TemporaryDirectory(prefix="research-bite-") as directory:
            temporary_project = Path(directory)
            research = temporary_project / "research"
            shutil.copytree(project / "research", research)
            manifest = json.loads((research / "sources.json").read_text(encoding="utf-8"))
            claims = [json.loads(line) for line in (research / "claims.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
            target = next(claim for claim in claims if claim["field"] == "source_statement")
            source = next(item for item in manifest if item["id"] == target["entity"])
            if name == "snapshot_bytes":
                path = research / source["snapshot"]
                path.write_bytes(path.read_bytes() + b"\n<!-- adversarial byte mutation -->")
            elif name == "claim_value":
                target["value"] += " [unsupported mutation]"
            elif name == "duplicate_claim":
                claims.append(json.loads(json.dumps(target)))
            elif name == "capture_url":
                target["capture"]["url"] += "#adversarial-mismatch"
            elif name == "manifest_hash":
                source["sha256"] = ("1" if source["sha256"][0] == "0" else "0") + source["sha256"][1:]
            elif name == "unavailable_source":
                source["capture_status"] = "unavailable"
            (research / "sources.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
            (research / "claims.jsonl").write_text("\n".join(json.dumps(claim, ensure_ascii=False) for claim in claims) + "\n", encoding="utf-8")
            process = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--project", directory], capture_output=True, text=True, timeout=30)
            try:
                output = json.loads(process.stdout)
                codes = sorted({item["code"] for item in output["errors"]})
            except (ValueError, KeyError, TypeError):
                codes = ["INVALID_GATE_OUTPUT"]
            passed = process.returncode == 2 and expected_code in codes
            results.append({"name": name, "status": "PASS" if passed else "FAIL", "exit_code": process.returncode,
                            "expected_error": expected_code, "observed_errors": codes})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--bites", action="store_true", help="run six adversarial checks on temporary copies after baseline passes")
    args = parser.parse_args()
    report = verify(args.project)
    report["bites"] = []
    if args.bites and report["status"] == "PASS":
        try:
            report["bites"] = run_bites(args.project.resolve())
            if any(bite["status"] != "PASS" for bite in report["bites"]):
                report["errors"].append({"code": "BITE_FAILED", "location": "--bites", "message": "a mutation escaped its expected gate"})
                report["status"] = "FAIL"
        except (OSError, ValueError, KeyError, StopIteration, subprocess.TimeoutExpired) as exc:
            report["errors"].append({"code": "BITES_INVALID", "location": "--bites", "message": str(exc)})
            report["status"] = "FAIL"
    elif args.bites:
        report["bites_status"] = "SKIPPED_BASELINE_FAILED"
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
