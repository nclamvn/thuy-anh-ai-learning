"""Independent fault fixtures for P02 compiler, verifier and response checker."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from build_resources import KitError, build, STAGES
from verify_project_kit import verify
from evaluate_responses import evaluate, HUMAN_KEYS


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')


class KitFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name) / 'project'; self.project.mkdir()
        (self.project / 'app').mkdir(); self.materials = self.project / 'materials'; self.materials.mkdir()
        raw = b'Fixture evidence.'
        snapshot = self.project / 'research/snapshots/SRC-T.html'; snapshot.parent.mkdir(parents=True); snapshot.write_bytes(raw)
        write_json(self.project / 'research/sources.json', [{'id': 'SRC-T', 'capture_status': 'captured', 'url': 'https://example.org/fixture', 'origin': 'example.org', 'tier': 'A', 'snapshot': 'snapshots/SRC-T.html', 'sha256': hashlib.sha256(raw).hexdigest()}])
        write_json(self.project / 'research/domain.yaml', {'schema': {'fields': ['source_statement']}, 'verification': {'allowed_tiers': ['A'], 'allowed_extractions': ['verbatim'], 'unknown_fields': []}})
        (self.project / 'research/claims.jsonl').write_text(json.dumps({'entity': 'SRC-T', 'field': 'source_statement', 'value': 'Fixture evidence.', 'evidence_span': 'Fixture evidence.', 'tier': 'A', 'extraction': 'verbatim', 'capture': {'url': 'https://example.org/fixture', 'source': 'example.org', 'snapshot': 'SRC-T.html'}}) + '\n')
        self.catalog = {'schemaVersion': 1, 'generatedKind': 'ai-draft-local-kit', 'items': []}
        for index in range(18):
            relative = f'templates/template-{index:02}.md'; path = self.materials / relative; path.parent.mkdir(exist_ok=True)
            path.write_text('# Bản nháp\n\nDữ liệu ví dụ giả định.\n\n[Danh mục](../catalog.json)\n', encoding='utf-8')
            self.catalog['items'].append({'id': f'DOC-{index}', 'title': f'Tài liệu {index}', 'category': 'template', 'path': relative, 'status': 'draft', 'description': 'Mẫu có dữ liệu giả.', 'sourceIds': ['SRC-T']})
        self.lessons = {'schemaVersion': 1, 'dataKind': 'synthetic-curriculum-drafts', 'lessons': []}
        for index in range(3):
            self.lessons['lessons'].append({'id': f'LESSON-{index}', 'title': 'Kiểm chứng', 'goal': 'Tự giải thích', 'ageGroup': '13–15', 'durationMinutes': 45, 'provenance': 'Học liệu mẫu · nháp chưa duyệt sư phạm', 'sourceIds': ['SRC-T'], 'instructions': {key: 'Hướng dẫn giả định.' for key in STAGES}, 'sourceCards': [{'title': 'Nguồn giả', 'text': 'Chỉ dùng cho fixture.'}], 'sampleResponse': {'text': 'Phản hồi sai cố ý.', 'provenance': 'Phản hồi AI mẫu · cố ý có lỗi', 'provider': 'fixture-v2'}, 'rubric': [{'key': key, 'title': key, 'description': 'Cần người đánh giá.'} for key in ('verification', 'explanation', 'independent')], 'facilitatorNotes': 'Cần người duyệt.', 'transferNotes': 'Tự thực hiện.'})
        self.save()

    def save(self):
        write_json(self.materials / 'catalog.json', self.catalog)
        write_json(self.materials / 'curriculum/lessons.json', self.lessons)

    def test_compiler_deterministic_allowlist(self):
        (self.materials / 'unlisted-private.md').write_text('Not public')
        first = build(self.project)
        outputs = self.project / 'app/resources'
        before = {str(path.relative_to(outputs)): path.read_bytes() for path in outputs.rglob('*') if path.is_file()}
        second = build(self.project)
        self.assertEqual(first, second); self.assertEqual(len(before), 22)
        self.assertFalse((outputs / 'unlisted-private.md').exists())
        self.assertEqual(before, {str(path.relative_to(outputs)): path.read_bytes() for path in outputs.rglob('*') if path.is_file()})
        self.assertEqual(verify(self.project)['status'], 'PASS')

    def test_bad_import_preserves_old_resources(self):
        build(self.project); marker = self.project / 'app/resources/manifest.json'; before = marker.read_bytes()
        (self.materials / 'catalog.json').write_text('{bad')
        with self.assertRaises(KitError): build(self.project)
        self.assertEqual(marker.read_bytes(), before)

    def test_duplicate_catalog_id(self):
        self.catalog['items'][1]['id'] = self.catalog['items'][0]['id']; self.save()
        with self.assertRaisesRegex(KitError, 'duplicate catalog id'): build(self.project)

    def test_traversal_rejected(self):
        for relative in ('../outside.md', '/absolute.md', 'templates/space name.md'):
            with self.subTest(path=relative):
                self.catalog['items'][0]['path'] = relative; self.save()
                with self.assertRaisesRegex(KitError, 'unsafe material path'): build(self.project)

    def test_private_path_rejected(self):
        self.catalog['items'][0]['path'] = 'QA/report.md'; self.save()
        with self.assertRaisesRegex(KitError, 'private/QA'): build(self.project)

    def test_symlink_escape_rejected(self):
        outside = self.project.parent / 'outside.md'; outside.write_text('private fixture')
        victim = self.materials / self.catalog['items'][0]['path']; victim.unlink(); victim.symlink_to(outside)
        with self.assertRaisesRegex(KitError, 'symlink escapes'): build(self.project)

    def test_material_alias_to_private_inside_root_rejected(self):
        private = self.materials / 'private'; private.mkdir(); (private / 'record.md').write_text('Private fixture')
        victim = self.materials / self.catalog['items'][0]['path']; victim.unlink(); victim.symlink_to(private / 'record.md')
        with self.assertRaisesRegex(KitError, 'symlink forbidden'): build(self.project)

    def test_lessons_input_symlink_escape(self):
        outside = self.project.parent / 'outside.json'; write_json(outside, self.lessons)
        path = self.materials / 'curriculum/lessons.json'; path.unlink(); path.symlink_to(outside)
        with self.assertRaisesRegex(KitError, 'symlink escapes'): build(self.project)

    def test_oversize_rejected(self):
        path = self.materials / self.catalog['items'][0]['path']; path.write_bytes(b'x' * (1024 * 1024 + 1))
        with self.assertRaisesRegex(KitError, 'too large'): build(self.project)

    def test_unknown_source_rejected(self):
        self.catalog['items'][0]['sourceIds'] = ['UNAVAILABLE']; self.save()
        with self.assertRaisesRegex(KitError, 'unknown or unavailable'): build(self.project)

    def test_missing_stage_rejected(self):
        del self.lessons['lessons'][0]['instructions']['transfer']; self.save()
        with self.assertRaisesRegex(KitError, 'eight instruction'): build(self.project)

    def test_seeded_approval_rejected(self):
        self.lessons['lessons'][0]['approvedBy'] = 'invented reviewer'; self.save()
        with self.assertRaisesRegex(KitError, 'seeded review'): build(self.project)

    def test_rubric_keys_rejected(self):
        self.lessons['lessons'][0]['rubric'][0]['key'] = 'automatic-score'; self.save()
        with self.assertRaisesRegex(KitError, 'rubric keys'): build(self.project)

    def test_stale_generated_digest_detected(self):
        build(self.project); path = self.project / 'app/resources/catalog.json'; path.write_bytes(path.read_bytes() + b' ')
        report = verify(self.project); self.assertEqual(report['status'], 'FAIL'); self.assertTrue(any('fingerprint' in error for error in report['errors']))

    def test_generated_parent_symlink_rejected(self):
        build(self.project)
        old = self.project / 'app'; saved = self.project / 'app-saved'; old.rename(saved); old.symlink_to(saved)
        self.assertEqual(verify(self.project)['status'], 'FAIL')

    def test_changed_input_requires_recompile(self):
        build(self.project); path = self.materials / self.catalog['items'][0]['path']; path.write_text('# Updated draft')
        self.assertEqual(verify(self.project)['status'], 'FAIL'); build(self.project); self.assertEqual(verify(self.project)['status'], 'PASS')

    def test_stale_unlisted_output_removed_by_build(self):
        build(self.project); stale = self.project / 'app/resources/stale.md'; stale.write_text('Old')
        self.assertEqual(verify(self.project)['status'], 'FAIL'); build(self.project); self.assertFalse(stale.exists())

    def test_dead_relative_link_detected(self):
        (self.materials / self.catalog['items'][0]['path']).write_text('[Missing](missing.md)')
        with self.assertRaisesRegex(KitError, 'not allowlisted'): build(self.project)
        self.assertEqual(verify(self.project)['status'], 'FAIL')

    def test_root_link_not_portable_is_rejected_before_replace(self):
        build(self.project); previous = (self.project / 'app/resources/manifest.json').read_bytes()
        (self.project / 'README.md').write_text('Existing root document')
        (self.materials / self.catalog['items'][0]['path']).write_text('[Root](../../README.md)')
        with self.assertRaisesRegex(KitError, 'escapes resources'): build(self.project)
        self.assertEqual((self.project / 'app/resources/manifest.json').read_bytes(), previous)

    def test_external_links_not_fetched(self):
        (self.materials / self.catalog['items'][0]['path']).write_text('[Source](https://example.invalid/no-fetch)')
        build(self.project); self.assertEqual(verify(self.project)['status'], 'PASS')

    def test_atomic_replace_failure_restores_existing(self):
        build(self.project); old = (self.project / 'app/resources/manifest.json').read_bytes()
        real_replace = os.replace
        def fail_staging(src, dst):
            if Path(src).name == 'staged': raise OSError('injected atomic replacement failure')
            return real_replace(src, dst)
        with patch('build_resources.os.replace', side_effect=fail_staging):
            with self.assertRaises(OSError): build(self.project)
        self.assertEqual((self.project / 'app/resources/manifest.json').read_bytes(), old)

    def test_portable_package_extract_and_tools(self):
        import shutil
        import zipfile
        from package_project import package
        for name in ('README.md', 'AGENTS.md'): (self.project / name).write_text('Fixture document')
        shutil.copyfile(TOOLS.parent / 'start-local.command', self.project / 'start-local.command')
        (self.project / 'app/index.html').write_text('<h1>Local fixture</h1>')
        shutil.copytree(TOOLS.parent / 'benchmarks', self.project / 'benchmarks')
        (self.project / 'benchmarks/provider-run.csv').write_text('Private observed fixture')
        (self.project / 'tools').mkdir()
        for name in ('build_resources.py', 'verify_project_kit.py', 'evaluate_responses.py', 'verify_research.py', 'package_project.py', 'verify_package.py', 'check_all.py', 'verify_provider_config.py'):
            shutil.copyfile(TOOLS / name, self.project / 'tools' / name)
        (self.project / 'app/QA').mkdir(); (self.project / 'app/QA/private.json').write_text('Private fixture')
        (self.project / 'app/QA-backup.json').write_text('Private fixture')
        (self.project / 'materials/guides').mkdir(); (self.project / 'materials/guides/backup-and-recovery.md').write_text('Public operating guide')
        (self.project / 'tools/__pycache__').mkdir(); (self.project / 'tools/__pycache__/dummy.pyc').write_bytes(b'no')
        write_json(self.project / 'sot/registry/_backup/old.json', {'private': 'fixture'})
        write_json(self.project / 'delivery/VERIFY-P02.json', {'dataKind': 'synthetic-test-fixture'})
        write_json(self.project / 'delivery/VERIFY-P03.json', {'status': 'PASS', 'dataKind': 'synthetic-test-fixture'})
        write_json(self.project / 'delivery/P02-state-private.json', {'private': 'fixture'})
        build(self.project)
        result = package(self.project); archive_path = Path(result['path'])
        from verify_package import verify as verify_zip
        self.assertEqual(verify_zip(archive_path)['status'], 'PASS')
        with self.assertRaisesRegex(KitError, 'P02 archive'): package(self.project, self.project / 'delivery/PROJECT-P02-local.zip')
        with zipfile.ZipFile(archive_path) as archive:
            self.assertFalse(any('QA' in name or '__pycache__' in name or '_backup' in name for name in archive.namelist()))
            self.assertIn('thuy-anh-ai-learning/materials/guides/backup-and-recovery.md', archive.namelist())
            self.assertIn('thuy-anh-ai-learning/delivery/VERIFY-P02.json', archive.namelist())
            self.assertFalse(any('P02-state' in name or 'provider-run.csv' in name for name in archive.namelist()))
            extracted = self.project.parent / 'extracted'; archive.extractall(extracted)
            self.assertEqual((archive.getinfo('thuy-anh-ai-learning/start-local.command').external_attr >> 16) & 0o777, 0o755)
        extracted_project = extracted / 'thuy-anh-ai-learning'
        commands = [('tools/build_resources.py',), ('tools/verify_project_kit.py',), ('tools/verify_research.py',), ('tools/evaluate_responses.py', 'benchmarks/response_template.json')]
        for command in commands:
            process = subprocess.run([sys.executable, '-B', *command], cwd=extracted_project, capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            self.assertEqual(json.loads(process.stdout)['status'], 'PASS')

    def supplement(self, extension='pdf', raw=b'%PDF-1.4\nSynthetic signature fixture only.\n%%EOF\n'):
        root = self.project / 'research/fulltexts'; root.mkdir(exist_ok=True)
        path = root / ('SRC-T.' + extension); path.write_bytes(raw)
        row = {'sourceId':'SRC-T','file':path.name,'url':'https://example.org/fulltext','final_url':'https://example.org/fulltext','http_status':200,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'status':'captured'}
        manifest = {'kind':'supplementary-fulltext-captures','not_independent_sources':True,'captures':[row]}
        write_json(root / 'capture-manifest.json', manifest)
        return manifest

    def research_result(self):
        from verify_research import verify as research_verify
        return research_verify(self.project)

    def test_supplement_preserves_source_counts_and_failed_attempts(self):
        manifest = self.supplement(); manifest['captures'].append({'sourceId':'SRC-T','file':'SRC-T.pdf','url':'https://example.org/failure','status':'unavailable','error':'Synthetic download failure'})
        write_json(self.project / 'research/fulltexts/capture-manifest.json', manifest)
        result = self.research_result(); self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['sources'], 1); self.assertEqual(result['claims'], 1)
        self.assertEqual(result['supplementary'], {'capturedFiles':1,'failedAttempts':1,'independentSourceIncrement':0})

    def test_supplement_bad_hash_duplicate_and_unknown_id_rejected(self):
        for mutate, expected in ((lambda m:m['captures'][0].update(sha256='0'*64), 'SUPPLEMENT_HASH'), (lambda m:m['captures'].append(copy.deepcopy(m['captures'][0])), 'SUPPLEMENT_DUPLICATE'), (lambda m:m['captures'][0].update(sourceId='UNKNOWN'), 'SUPPLEMENT_SOURCE'), (lambda m:m['captures'][0].update(file='../outside.pdf'), 'SUPPLEMENT_PATH')):
            manifest = self.supplement(); mutate(manifest); write_json(self.project / 'research/fulltexts/capture-manifest.json', manifest)
            result = self.research_result(); self.assertEqual(result['status'], 'FAIL'); self.assertIn(expected, {error['code'] for error in result['errors']})

    def test_compiler_supplement_union_requires_full_provenance_gate(self):
        manifest = self.supplement()
        sources_path = self.project / 'research/sources.json'; sources = json.loads(sources_path.read_text())
        sources.append({'id':'SRC-U','capture_status':'unavailable','url':'https://example.org/primary','origin':'example.org','tier':'A'})
        write_json(sources_path,sources)
        manifest['captures'][0]['sourceId'] = 'SRC-U'; write_json(self.project / 'research/fulltexts/capture-manifest.json',manifest)
        self.catalog['items'][0]['sourceIds'] = ['SRC-U']; self.save()
        result=build(self.project); self.assertEqual(result['status'],'PASS')
        marker=self.project / 'app/resources/manifest.json'; before=marker.read_bytes()
        self.assertIn('research/fulltexts/SRC-T.pdf',json.loads(before)['inputs'])
        (self.project / 'research/fulltexts/SRC-T.pdf').write_bytes(b'Changed invalid synthetic capture')
        with self.assertRaisesRegex(KitError,'provenance gate'): build(self.project)
        self.assertEqual(marker.read_bytes(),before)

    def test_supplement_pdf_or_challenge_content_rejected(self):
        for extension, raw in (('pdf', b'<html><p>Not a PDF</p></html>'), ('html', b'<html><title>Just a moment</title><p>Verify you are human</p></html>')):
            self.supplement(extension, raw); result = self.research_result()
            self.assertEqual(result['status'], 'FAIL'); self.assertIn('SUPPLEMENT_CONTENT', {error['code'] for error in result['errors']})

    def test_supplement_html_body_utf8_and_http_verified(self):
        manifest = self.supplement('html', b'<html><main><h1>Paper</h1><p>Public fulltext fixture.</p></main></html>')
        self.assertEqual(self.research_result()['status'], 'PASS')
        manifest['captures'][0]['http_status'] = 403; write_json(self.project / 'research/fulltexts/capture-manifest.json', manifest)
        self.assertIn('SUPPLEMENT_HTTP', {error['code'] for error in self.research_result()['errors']})

    def add_english(self):
        for item in self.catalog['items']:
            relative = 'en/' + item['path']; path = self.materials / relative; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# Draft\n\n[Catalog](../../catalog.json)\n', encoding='utf-8')
            item['translations'] = {'en': {'path': relative, 'title': 'Draft material', 'description': 'Synthetic example pending review.', 'status': item['status']}}
        for lesson in self.lessons['lessons']:
            translated = {key: copy.deepcopy(lesson[key]) for key in ('title','goal','provenance','instructions','sourceCards','sampleResponse','rubric','facilitatorNotes','transferNotes')}
            translated['provenance'] = 'Sample learning material · draft pending educational review'
            translated['sampleResponse']['provenance'] = 'Sample AI response · deliberately contains errors'
            lesson['translations'] = {'en': translated}
        self.save()

    def test_authored_english_and_explicit_fallback(self):
        self.add_english(); del self.catalog['items'][0]['translations']; self.save()
        build(self.project)
        catalog = json.loads((self.project / 'app/resources/catalog.json').read_text())
        self.assertEqual(catalog['items'][0]['localeAvailability']['en'], 'fallback-vi')
        self.assertEqual(catalog['items'][1]['translations']['en']['href'], 'resources/en/templates/template-01.md')
        self.assertEqual(verify(self.project)['translatedDocuments'], 17)
        self.assertEqual(verify(self.project)['translatedLessons'], 3)

    def test_english_path_cannot_escape_or_change_counterpart(self):
        self.add_english(); self.catalog['items'][0]['translations']['en']['path'] = '../private.md'; self.save()
        with self.assertRaisesRegex(KitError, 'counterpart'): build(self.project)

    def test_english_cannot_upgrade_status_or_curriculum_identity(self):
        self.add_english(); self.catalog['items'][0]['translations']['en']['status'] = 'approved'; self.save()
        with self.assertRaisesRegex(KitError, 'review status'): build(self.project)
        self.catalog['items'][0]['translations']['en']['status'] = 'draft'
        self.lessons['lessons'][0]['translations']['en']['id'] = 'override'; self.save()
        with self.assertRaisesRegex(KitError, 'presentation fields'): build(self.project)

    def test_english_source_reference_cannot_disappear(self):
        self.add_english()
        (self.materials / self.catalog['items'][0]['path']).write_text('[Evidence](https://example.org/evidence)')
        with self.assertRaisesRegex(KitError, 'drops source/reference'): build(self.project)

    def test_english_broken_link_and_missing_field_preserve_outputs(self):
        self.add_english(); build(self.project); marker = self.project / 'app/resources/manifest.json'; before = marker.read_bytes()
        path = self.materials / self.catalog['items'][0]['translations']['en']['path']; path.write_text('[Missing](missing.md)')
        with self.assertRaisesRegex(KitError, 'not allowlisted'): build(self.project)
        self.assertEqual(marker.read_bytes(), before)
        path.write_text('# Draft')
        del self.lessons['lessons'][0]['translations']['en']['instructions']['review']; self.save()
        with self.assertRaisesRegex(KitError, 'English instruction'): build(self.project)
        self.assertEqual(marker.read_bytes(), before)

    def test_source_edit_during_staging_preserves_previous_build(self):
        build(self.project); marker = self.project / 'app/resources/manifest.json'; before = marker.read_bytes()
        actual_write = Path.write_bytes; changed = [False]
        def mutate(path, data):
            result = actual_write(path, data)
            if '.resources-build-' in str(path) and not changed[0]:
                changed[0] = True
                actual_write(self.materials / self.catalog['items'][0]['path'], b'# Concurrent edit')
            return result
        with patch('pathlib.Path.write_bytes', new=mutate):
            with self.assertRaisesRegex(KitError, 'source changed during build'): build(self.project)
        self.assertEqual(marker.read_bytes(), before)

    def test_launcher_occupied_port_message(self):
        from contextlib import redirect_stdout
        import io
        (self.project / 'app/index.html').write_text('Fixture')
        launcher = (TOOLS.parent / 'start-local.command').read_text()
        payload = launcher.split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
        output = io.StringIO()
        # Inject a real server-construction failure without requiring bind access
        # in CI/sandbox. Exercise the exact Python payload used by the launcher.
        with patch('http.server.ThreadingHTTPServer', side_effect=OSError('Address already in use')), patch.object(sys, 'argv', ['-', str(self.project)]), patch.dict(os.environ, {'AI_LEARNING_PORT': '8875'}), redirect_stdout(output):
            with self.assertRaises(SystemExit) as caught: exec(compile(payload, 'launcher-payload', 'exec'), {})
        self.assertEqual(caught.exception.code, 2); self.assertIn('cổng 8875', output.getvalue()); self.assertIn('AI_LEARNING_PORT=', output.getvalue())


class ProviderConfigFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / 'config.json'
        self.config = json.loads((TOOLS.parent / 'benchmarks/provider-config.template.json').read_text())

    def result(self):
        from verify_provider_config import verify
        write_json(self.path, self.config); return verify(self.path)

    def test_inactive_config_is_offline(self):
        self.assertFalse(self.result()['active']); self.assertEqual(self.result()['requests'], 0)

    def test_activation_secret_or_child_data_rejected(self):
        for field, value in (('enabled', True), ('apiKey', 'synthetic-not-secret'), ('allowChildData', True), ('maxRequests', 1), ('credentialsEnvName', 'secret-value')):
            with self.subTest(field=field):
                original = copy.deepcopy(self.config); self.config[field] = value
                with self.assertRaises(KitError): self.result()
                self.config = original

    def test_package_missing_contractor_report_is_rejected(self):
        from package_project import package
        with self.assertRaises(KitError): package(Path(self.temporary.name))
        write_json(Path(self.temporary.name) / 'delivery/VERIFY-P03.json', {'status':'FAIL'})
        with self.assertRaisesRegex(KitError, 'Contractor'): package(Path(self.temporary.name))

    def test_zip_hash_and_exact_coverage_faults(self):
        import zipfile
        from verify_package import verify
        files = {name:b'Synthetic package fixture only.' for name in ('app/index.html','materials/catalog.json','delivery/VERIFY-P03.json','tools/check_all.py','start-local.command')}
        manifest = {'release':'P03','dataKind':'portable-local-kit','files':{name:{'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)} for name,raw in files.items()}}
        archive = Path(self.temporary.name) / 'package.zip'
        def write(extra=False, changed=False):
            with zipfile.ZipFile(archive,'w') as output:
                for name,raw in files.items(): output.writestr('thuy-anh-ai-learning/'+name, raw+b' Changed' if changed and name=='app/index.html' else raw)
                output.writestr('thuy-anh-ai-learning/PACKAGE-MANIFEST.json',json.dumps(manifest))
                if extra: output.writestr('thuy-anh-ai-learning/unlisted.json','{}')
        write(); self.assertEqual(verify(archive)['status'],'PASS')
        write(changed=True)
        with self.assertRaisesRegex(KitError,'fingerprint mismatch'): verify(archive)
        write(extra=True)
        with self.assertRaisesRegex(KitError,'exactly cover'): verify(archive)

    def test_zip_traversal_or_private_data_rejected(self):
        import zipfile
        from verify_package import verify
        archive = Path(self.temporary.name) / 'unsafe.zip'
        for name in ('thuy-anh-ai-learning/../outside.json', 'thuy-anh-ai-learning/app/qa-backup.json'):
            with zipfile.ZipFile(archive, 'w') as target: target.writestr(name, '{}')
            with self.assertRaises(KitError): verify(archive)


class BenchmarkFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        base = TOOLS.parent / 'benchmarks'
        self.cases = json.loads((base / 'task_cases.json').read_text())
        self.data = json.loads((base / 'response_template.json').read_text())
        self.case_path, self.response_path = self.root / 'cases.json', self.root / 'responses.json'
        self.save()

    def save(self):
        write_json(self.case_path, self.cases); write_json(self.response_path, self.data)

    def result(self): self.save(); return evaluate(self.case_path, self.response_path)

    def observed(self):
        self.data['dataKind'] = 'observed-model-responses'; self.data['responses'] = [self.data['responses'][0]]
        row = self.data['responses'][0]
        row.update(model='test-model', modelVersion='test-v1', response='Observed fixture for unit test.', provenance={'kind': 'observed', 'recordedAt': '2026-10-03T12:00:00+07:00', 'evidenceRef': 'unit-test-only/raw.json'})
        return row

    def test_unobserved_nulls_preserved(self):
        before = self.response_path.read_bytes(); report = evaluate(self.case_path, self.response_path)
        self.assertEqual(report['status'], 'PASS'); self.assertEqual(self.response_path.read_bytes(), before)
        self.assertEqual(report['measurements']['observedResponses'], 0)
        self.assertIsNone(report['measurements']['latencyMs']['mean']); self.assertIsNone(report['measurements']['costUSD']['total'])
        self.assertEqual(report['humanReview']['pendingRecords'], len(self.cases['cases']))

    def test_bad_import_cli_returns_json_failure(self):
        self.response_path.write_text('{bad')
        result = subprocess.run([sys.executable, str(TOOLS / 'evaluate_responses.py'), str(self.response_path), '--cases', str(self.case_path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2); self.assertEqual(json.loads(result.stdout)['status'], 'FAIL')

    def test_unknown_case(self):
        self.data['responses'][0]['caseId'] = 'UNKNOWN'; self.assertEqual(self.result()['status'], 'FAIL')

    def test_scientific_validation_label_not_invented(self):
        self.cases['validationStatus'] = 'scientifically-validated'; self.assertEqual(self.result()['status'], 'FAIL')

    def test_negative_cost(self):
        row = self.observed(); row['costUSD'] = -1; self.assertEqual(self.result()['status'], 'FAIL')

    def test_out_of_bounds_latency(self):
        row = self.observed(); row['latencyMs'] = 1e300; report = self.result(); self.assertEqual(report['status'], 'FAIL'); self.assertIsNone(report['measurements']['latencyMs']['mean'])

    def test_incomplete_observed_coverage_is_explicit(self):
        self.observed(); report = self.result()
        self.assertEqual(report['status'], 'PASS')
        self.assertEqual(report['coverage']['representedCases'], 1)
        self.assertEqual(len(report['coverage']['missingCaseIds']), len(self.cases['cases']) - 1)
        self.assertIsNone(report['humanReview']['qualityVerdict'])

    def test_missing_human_ratings(self):
        del self.data['responses'][0]['humanRatings']; self.assertEqual(self.result()['status'], 'FAIL')

    def test_human_score_without_reviewer(self):
        row = self.observed(); row['humanRatings']['grounding'] = 4; self.assertEqual(self.result()['status'], 'FAIL')

    def test_human_quality_not_automatically_approved(self):
        row = self.observed(); row['humanRatings'] = {key: 4 for key in HUMAN_KEYS}; row['reviewer'] = 'unit-test-reviewer'; row['latencyMs'] = 100; row['costUSD'] = 0.01
        report = self.result(); self.assertEqual(report['status'], 'PASS'); self.assertIsNone(report['humanReview']['qualityVerdict'])
        self.assertEqual(report['measurements']['latencyMs']['n'], 1); self.assertEqual(report['measurements']['costUSD']['total'], 0.01)

    def test_fixture_excluded_from_metrics(self):
        self.data = json.loads((TOOLS.parent / 'benchmarks/fixtures/synthetic_responses.json').read_text()); self.data['responses'][0]['latencyMs'] = 100
        report = self.result(); self.assertEqual(report['status'], 'PASS'); self.assertEqual(report['measurements']['observedResponses'], 0); self.assertIsNone(report['measurements']['latencyMs']['mean']); self.assertEqual(report['humanReview']['completedRecords'], 0)

    def test_observed_requires_evidence_and_timestamp(self):
        row = self.observed(); row['provenance']['evidenceRef'] = None; row['provenance']['recordedAt'] = None
        self.assertEqual(self.result()['status'], 'FAIL')

    def test_unobserved_cannot_smuggle_measurements(self):
        self.data['responses'][0]['costUSD'] = 0.02; self.assertEqual(self.result()['status'], 'FAIL')

    def test_token_boolean_rejected(self):
        row = self.observed(); row['usage']['inputTokens'] = True; self.assertEqual(self.result()['status'], 'FAIL')


if __name__ == '__main__': unittest.main()
