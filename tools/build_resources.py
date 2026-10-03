#!/usr/bin/env python3
"""Compile the explicit materials allowlist into deterministic app resources."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit

MAX_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 20 * MAX_FILE_BYTES
TRANSLATED_LESSON_FIELDS = {'title', 'goal', 'provenance', 'instructions', 'sourceCards', 'sampleResponse', 'rubric', 'facilitatorNotes', 'transferNotes'}
STAGES = {'initial', 'ai', 'concern', 'sourceCheck', 'revised', 'explanation', 'transfer', 'review'}
RUBRIC = {'verification', 'explanation', 'independent'}


class KitError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise KitError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def markdown_links(content):
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    return [match.group(1).strip('<>') for match in re.finditer(r'!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)', content)]


def validate_resource_links(payloads):
    directories = {'.'}
    for relative in payloads:
        directories.update(parent.as_posix() for parent in PurePosixPath(relative).parents)
    for relative, raw in payloads.items():
        if not relative.endswith('.md'): continue
        for href in markdown_links(raw.decode('utf-8')):
            parsed = urlsplit(href)
            if parsed.scheme in ('https', 'http', 'mailto'): continue
            require(not parsed.scheme and not parsed.netloc and not href.startswith('/') and '\\' not in href,
                    f'{relative}: unsafe generated link {href}')
            if not parsed.path: continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(relative), unquote(parsed.path)))
            require(target != '..' and not target.startswith('../') and not target.startswith('/'), f'{relative}: generated link escapes resources {href}')
            require(target in payloads or target in directories, f'{relative}: generated link is not allowlisted {href}')


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f'{path}: duplicate JSON key {key}')
            result[key] = value
        return result
    def reject(value):
        raise KitError(f'{path}: invalid JSON constant {value}')
    try:
        raw = path.read_bytes()
        require(len(raw) <= MAX_FILE_BYTES, f'{path}: exceeds file size limit')
        return json.loads(raw.decode('utf-8'), object_pairs_hook=unique, parse_constant=reject), raw
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise KitError(f'{path}: {exc}') from exc


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f'{label}: expected nonempty text')


def material_path(root, relative):
    text(relative, 'catalog path')
    path = PurePosixPath(relative)
    require(re.fullmatch(r'[A-Za-z0-9_./-]+', relative) is not None, f'unsafe material path: {relative}')
    require(not path.is_absolute() and '\\' not in relative and relative == path.as_posix(), f'unsafe material path: {relative}')
    require(all(part not in ('.', '..') and not part.startswith('.') for part in path.parts), f'unsafe material path: {relative}')
    require(path.suffix in ('.md', '.json'), f'unsupported material extension: {relative}')
    require(not any(part.lower() in {'qa', 'private', 'backups', 'backup', 'conversations', 'conversation'} for part in path.parts), f'private/QA path forbidden: {relative}')
    require(not any(char in relative for char in ('?', '#', '%', ':')), f'unsafe URL characters: {relative}')
    destination = root / relative
    require(destination.resolve().is_relative_to(root.resolve()), f'material symlink escapes materials: {relative}')
    require(not destination.is_symlink(), f'material file symlink forbidden: {relative}')
    require(destination.is_file(), f'material missing: {relative}')
    require(destination.stat().st_size <= MAX_FILE_BYTES, f'material too large: {relative}')
    try:
        destination.read_text(encoding='utf-8')
    except UnicodeError as exc:
        raise KitError(f'material must be UTF-8 text: {relative}') from exc
    return destination


def source_ids(value, known, label):
    require(isinstance(value, list) and all(isinstance(item, str) for item in value), f'{label}: expected sourceIds array')
    require(len(value) == len(set(value)), f'{label}: duplicate sourceIds')
    require(set(value).issubset(known), f'{label}: unknown or unavailable sourceIds {sorted(set(value) - known)}')


def validate_lessons(document, known):
    require(isinstance(document, dict) and document.get('schemaVersion') == 1, 'lessons schemaVersion must be 1')
    require(document.get('dataKind') == 'synthetic-curriculum-drafts', 'lessons must be marked synthetic-curriculum-drafts')
    lessons = document.get('lessons')
    require(isinstance(lessons, list) and len(lessons) >= 3, 'at least three draft lessons required')
    seen = set()
    for lesson in lessons:
        require(isinstance(lesson, dict), 'lesson must be an object')
        identifier = lesson.get('id'); text(identifier, 'lesson id')
        require(identifier not in seen, f'duplicate lesson id {identifier}'); seen.add(identifier)
        for key in ('title', 'goal', 'facilitatorNotes', 'transferNotes'):
            text(lesson.get(key), f'{identifier}.{key}')
        require(lesson.get('ageGroup') == '13–15', f'{identifier}: ageGroup must be 13–15')
        require(type(lesson.get('durationMinutes')) is int and 1 <= lesson['durationMinutes'] <= 180, f'{identifier}: durationMinutes invalid')
        require(lesson.get('provenance') == 'Học liệu mẫu · nháp chưa duyệt sư phạm', f'{identifier}: draft review provenance required')
        require(lesson.get('status', 'draft') == 'draft', f'{identifier}: seeded lesson must remain draft')
        require(not any(key in lesson for key in ('approvedBy', 'reviewer', 'reviewedAt', 'review', 'consent')), f'{identifier}: seeded review/consent forbidden')
        source_ids(lesson.get('sourceIds'), known, identifier)
        instructions = lesson.get('instructions')
        require(isinstance(instructions, dict) and set(instructions) == STAGES, f'{identifier}: exactly eight instruction keys required')
        for key, value in instructions.items(): text(value, f'{identifier}.instructions.{key}')
        cards = lesson.get('sourceCards')
        require(isinstance(cards, list) and cards, f'{identifier}: sourceCards required')
        for card in cards:
            require(isinstance(card, dict), f'{identifier}: sourceCard must be object')
            text(card.get('title'), f'{identifier}.sourceCard.title'); text(card.get('text'), f'{identifier}.sourceCard.text')
        sample = lesson.get('sampleResponse')
        require(isinstance(sample, dict), f'{identifier}: sampleResponse required')
        text(sample.get('text'), f'{identifier}.sampleResponse.text')
        require(sample.get('provider') == 'fixture-v2' and sample.get('provenance') == 'Phản hồi AI mẫu · cố ý có lỗi', f'{identifier}: fixture-v2 provenance required')
        rubric = lesson.get('rubric')
        require(isinstance(rubric, list) and len(rubric) == 3 and all(isinstance(item, dict) for item in rubric), f'{identifier}: three rubric entries required')
        require({item.get('key') for item in rubric} == RUBRIC, f'{identifier}: invalid rubric keys')
        for entry in rubric:
            text(entry.get('title'), f'{identifier}.rubric.title'); text(entry.get('description'), f'{identifier}.rubric.description')
        translations = lesson.get('translations', {})
        require(isinstance(translations, dict) and set(translations).issubset({'en'}), f'{identifier}: unsupported lesson locale')
        if 'en' in translations:
            translated = translations['en']
            require(isinstance(translated, dict), f'{identifier}: English lesson must be object')
            require(set(translated) in (TRANSLATED_LESSON_FIELDS, TRANSLATED_LESSON_FIELDS | {'ageGroup'}), f'{identifier}: English lesson must contain authored presentation fields only')
            require(translated.get('ageGroup', lesson['ageGroup']) == lesson['ageGroup'], f'{identifier}: translation cannot change ageGroup')
            for name in ('title', 'goal', 'provenance', 'facilitatorNotes', 'transferNotes'):
                text(translated.get(name), f'{identifier}.en.{name}')
            require(translated['provenance'] == 'Sample learning material · draft pending educational review', f'{identifier}: English draft provenance required')
            require(isinstance(translated['instructions'], dict) and set(translated['instructions']) == STAGES, f'{identifier}: English instruction keys must match')
            for name, value in translated['instructions'].items(): text(value, f'{identifier}.en.instructions.{name}')
            require(isinstance(translated['sourceCards'], list) and len(translated['sourceCards']) == len(cards), f'{identifier}: English source cards must correspond')
            for card in translated['sourceCards']:
                require(isinstance(card, dict) and set(card) == {'title', 'text'}, f'{identifier}: English source card fields invalid')
                text(card['title'], f'{identifier}.en.sourceCard.title'); text(card['text'], f'{identifier}.en.sourceCard.text')
            response = translated['sampleResponse']
            require(isinstance(response, dict) and set(response) == set(sample), f'{identifier}: English response fields must correspond')
            text(response.get('text'), f'{identifier}.en.sampleResponse.text')
            require(response.get('provider') == sample['provider'] and response.get('provenance') == 'Sample AI response · deliberately contains errors', f'{identifier}: English fixture provenance required')
            require(isinstance(translated['rubric'], list) and len(translated['rubric']) == 3 and {entry.get('key') for entry in translated['rubric'] if isinstance(entry, dict)} == RUBRIC, f'{identifier}: English rubric must preserve keys')
            for entry in translated['rubric']:
                require(set(entry) == {'key', 'title', 'description'}, f'{identifier}: English rubric presentation fields only')
                text(entry.get('title'), f'{identifier}.en.rubric.title'); text(entry.get('description'), f'{identifier}.en.rubric.description')
    return lessons


def prepare(project):
    project = project.resolve(); root = project / 'materials'
    require(root.is_dir() and root.resolve().is_relative_to(project), 'materials must exist inside project')
    catalog, catalog_raw = read_json(material_path(root, 'catalog.json'))
    lesson_document, lesson_raw = read_json(material_path(root, 'curriculum/lessons.json'))
    require((project / 'research/sources.json').resolve().is_relative_to(project), 'research sources must remain inside project')
    sources, source_raw = read_json(project / 'research/sources.json')
    require(isinstance(sources, list) and all(isinstance(source, dict) for source in sources), 'research source manifest must be an array')
    known = {source['id'] for source in sources if source.get('capture_status') == 'captured' and isinstance(source.get('id'), str)}
    supplemental_inputs = {}
    supplemental_path = project / 'research/fulltexts/capture-manifest.json'
    if supplemental_path.exists():
        from verify_research import verify as verify_research_provenance
        research_report = verify_research_provenance(project)
        require(research_report['status'] == 'PASS', f'supplementary provenance gate failed: {research_report["errors"]}')
        supplemental, supplemental_raw = read_json(supplemental_path)
        supplemental_inputs['research/fulltexts/capture-manifest.json'] = digest(supplemental_raw)
        for capture in supplemental['captures']:
            if capture.get('status') != 'captured': continue
            known.add(capture['sourceId'])
            relative = 'research/fulltexts/' + capture['file']
            supplemental_inputs[relative] = digest((project / relative).read_bytes())
    validate_lessons(lesson_document, known)
    require(isinstance(catalog, dict) and catalog.get('schemaVersion') == 1, 'catalog schemaVersion must be 1')
    require(catalog.get('generatedKind') == 'ai-draft-local-kit', 'catalog must be marked ai-draft-local-kit')
    items = catalog.get('items'); require(isinstance(items, list) and len(items) >= 18, 'catalog requires at least 18 resources')
    seen_ids, seen_paths, normalized_items, payloads = set(), set(), [], {'curriculum/lessons.json': lesson_raw}
    inputs = {'materials/catalog.json': digest(catalog_raw), 'materials/curriculum/lessons.json': digest(lesson_raw), 'research/sources.json': digest(source_raw)}
    inputs.update(supplemental_inputs)
    for item in items:
        require(isinstance(item, dict), 'catalog item must be object')
        for key in ('id', 'title', 'category', 'path', 'description'): text(item.get(key), f'catalog.{key}')
        identifier, relative = item['id'], item['path']
        require(identifier not in seen_ids, f'duplicate catalog id {identifier}'); seen_ids.add(identifier)
        require(relative not in seen_paths, f'duplicate catalog path {relative}'); seen_paths.add(relative)
        require(relative not in ('catalog.json', 'lessons.json', 'manifest.json'), f'reserved resource path {relative}')
        require(item.get('status') in ('draft', 'operating-guide', 'source-index'), f'{identifier}: invalid status')
        source_ids(item.get('sourceIds'), known, identifier)
        raw = material_path(root, relative).read_bytes()
        require(raw.strip(), f'{relative}: empty resource')
        payloads[relative] = raw; inputs[f'materials/{relative}'] = digest(raw)
        normalized_item = {key: item[key] for key in ('id', 'title', 'category', 'path', 'status', 'description', 'sourceIds')}
        normalized_item['href'] = 'resources/' + relative
        normalized_item['sourceLocale'] = 'vi'
        translations = item.get('translations', {})
        require(isinstance(translations, dict) and set(translations).issubset({'en'}), f'{identifier}: unsupported catalog locale')
        normalized_item['localeAvailability'] = {'vi': 'authored', 'en': 'fallback-vi'}
        if 'en' in translations:
            translated = translations['en']
            require(isinstance(translated, dict) and set(translated) == {'path', 'title', 'description', 'status'}, f'{identifier}: English metadata fields invalid')
            for name in ('path', 'title', 'description'): text(translated.get(name), f'{identifier}.en.{name}')
            require(translated['path'] == 'en/' + relative, f'{identifier}: English counterpart must preserve path')
            require(translated['status'] == item['status'], f'{identifier}: translation cannot change review status')
            require(translated['path'] not in seen_paths, f'duplicate catalog path {translated["path"]}')
            seen_paths.add(translated['path'])
            translated_raw = material_path(root, translated['path']).read_bytes()
            require(translated_raw.strip(), f'{identifier}: empty English resource')
            if relative.endswith('.md'):
                source_urls = {link for link in markdown_links(raw.decode('utf-8')) if urlsplit(link).scheme in ('https', 'http')}
                translated_urls = {link for link in markdown_links(translated_raw.decode('utf-8')) if urlsplit(link).scheme in ('https', 'http')}
                require(source_urls.issubset(translated_urls), f'{identifier}: English translation drops source/reference URLs')
            payloads[translated['path']] = translated_raw; inputs['materials/' + translated['path']] = digest(translated_raw)
            normalized_item['translations'] = {'en': {**translated, 'href': 'resources/' + translated['path'], 'contentUrl': 'resources/' + translated['path'], 'sourceLocale': 'en'}}
            normalized_item['localeAvailability']['en'] = 'authored'
        normalized_items.append(normalized_item)
    payloads['catalog.json'] = encode({'schemaVersion': 1, 'generatedKind': 'ai-draft-local-kit', 'items': normalized_items})
    payloads['lessons.json'] = encode(lesson_document)
    validate_resource_links(payloads)
    require(sum(len(raw) for raw in payloads.values()) <= MAX_TOTAL_BYTES, 'resource bundle exceeds total size limit')
    outputs = {relative: digest(raw) for relative, raw in sorted(payloads.items())}
    manifest = {'schemaVersion': 1, 'generatedKind': 'compiled-local-kit', 'inputs': dict(sorted(inputs.items())), 'outputs': outputs}
    manifest['fingerprint'] = digest(encode({'inputs': manifest['inputs'], 'outputs': outputs}))
    payloads['manifest.json'] = encode(manifest)
    return payloads, manifest, catalog, lesson_document


def build(project):
    payloads, manifest, catalog, lessons = prepare(project)
    project = project.resolve(); app = project / 'app'
    require(app.is_dir() and not app.is_symlink() and app.resolve().is_relative_to(project), 'app must be a regular directory inside project')
    target = app / 'resources'
    require(not target.is_symlink(), 'generated resources directory cannot be a symlink')
    require(not target.exists() or target.is_dir(), 'generated resources must be a directory')
    with tempfile.TemporaryDirectory(prefix='.resources-build-', dir=app) as temporary:
        staged, backup = Path(temporary) / 'staged', Path(temporary) / 'backup'
        staged.mkdir()
        for relative, raw in payloads.items():
            destination = staged / relative; destination.parent.mkdir(parents=True, exist_ok=True); destination.write_bytes(raw)
        # Reject edits during compilation instead of publishing an inconsistent snapshot.
        for relative, expected in manifest['inputs'].items():
            require(digest((project / relative).read_bytes()) == expected, f'source changed during build: {relative}')
        if target.exists(): os.replace(target, backup)
        try:
            os.replace(staged, target)
        except OSError:
            if backup.exists(): os.replace(backup, target)
            raise
    return {'status': 'PASS', 'catalogItems': len(catalog['items']), 'translatedDocuments': sum('en' in item.get('translations', {}) for item in catalog['items']), 'translatedLessons': sum('en' in lesson.get('translations', {}) for lesson in lessons['lessons']), 'lessons': len(lessons['lessons']), 'generatedFiles': len(payloads), 'fingerprint': manifest['fingerprint']}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1]); args = parser.parse_args()
    try:
        print(json.dumps(build(args.project), ensure_ascii=False, indent=2)); return 0
    except (KitError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({'status': 'FAIL', 'errors': [str(exc)]}, ensure_ascii=False, indent=2)); return 2


if __name__ == '__main__': raise SystemExit(main())
