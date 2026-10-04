"""Independent fault and coverage tests for the full authored review handoff."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from build_share_bundle import build, collect, verify, ARCHIVE, OUTER, PREFIX, INNER, RUNTIME, VISUAL_EDITION, ROOM_ASSETS
from build_resources import KitError, markdown_links

class ShareBundle(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.project=Path(self.temp.name)/'project'
        shutil.copytree(ROOT,self.project,ignore=shutil.ignore_patterns('.git','.vercel','.env','.env.*','__pycache__','.venv','node_modules','exports','observed','runtime'))
    def test_coverage_inner_hashes_and_repeat_determinism(self):
        first=build(self.project);raw=(self.project/ARCHIVE).read_bytes();second=build(self.project)
        self.assertEqual(first,second);self.assertEqual(raw,(self.project/ARCHIVE).read_bytes())
        self.assertEqual(verify(self.project)['status'],'PASS')
        with zipfile.ZipFile(self.project/ARCHIVE) as archive:
            names=set(archive.namelist());inner=json.loads(archive.read(PREFIX+INNER))
            catalog=json.loads(archive.read(PREFIX+'materials/catalog.json'))
            self.assertEqual(len(catalog['items']),54)
            for item in catalog['items']:
                for shown in (item,item['translations']['en']):
                    self.assertIn(PREFIX+'materials/'+shown['path'],names)
                    self.assertIn(PREFIX+'app/resources/'+shown['path'],names)
            self.assertEqual(len([n for n in names if n.startswith(PREFIX+'app/resources/')]),112)
            self.assertEqual(len(inner['files'])+1,len(names))
            outer=json.loads((self.project/OUTER).read_text())
            self.assertEqual(len(outer['files']),len(names))
            self.assertEqual(outer['fileCount'],len(names))
            self.assertEqual(outer['sha256'],hashlib.sha256((self.project/ARCHIVE).read_bytes()).hexdigest())
            self.assertEqual(outer['files'][INNER]['sha256'],hashlib.sha256(archive.read(PREFIX+INNER)).hexdigest())
            for name,row in inner['files'].items():
                raw=archive.read(PREFIX+name);self.assertEqual(row,{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
            self.assertEqual((archive.getinfo(PREFIX+'start-local.command').external_attr>>16)&0o777,0o755)
    def test_exact_visual_assets_and_motion_module_are_included_with_hashes(self):
        build(self.project)
        with zipfile.ZipFile(self.project/ARCHIVE) as archive:
            inner=json.loads(archive.read(PREFIX+INNER))
            outer=json.loads((self.project/OUTER).read_text())
            self.assertEqual(inner['visualEdition'],VISUAL_EDITION)
            self.assertEqual(outer['visualEdition'],VISUAL_EDITION)
            for name in RUNTIME:
                with self.subTest(name=name):
                    self.assertIn('app/'+name,inner['files'])
                    self.assertEqual(archive.read(PREFIX+'app/'+name),(self.project/'app'/name).read_bytes())
    def test_all_eight_room_artworks_and_room_renderer_are_portable(self):
        self.assertEqual(len(ROOM_ASSETS),8)
        build(self.project)
        with zipfile.ZipFile(self.project/ARCHIVE) as archive:
            manifest=json.loads(archive.read(PREFIX+INNER))
            for name in ('room-ui.js',*ROOM_ASSETS):
                with self.subTest(name=name):
                    self.assertIn('app/'+name,manifest['files'])
                    self.assertEqual(archive.read(PREFIX+'app/'+name),(self.project/'app'/name).read_bytes())
        missing=self.project/'app'/ROOM_ASSETS[-1];missing.unlink()
        with self.assertRaisesRegex(KitError,'source missing'):collect(self.project)
    def test_room_svg_viewport_and_static_safety_contract_enforced(self):
        path=self.project/'app'/ROOM_ASSETS[0];original=path.read_text()
        for changed in (original.replace('0 0 640 360','0 0 1 1'),original.replace('</svg>','<script>/* synthetic rejected fixture */</script></svg>'),original.replace('</svg>','<animate attributeName="opacity" dur="1s"/></svg>')):
            with self.subTest(changed=changed[-100:]):
                path.write_text(changed)
                with self.assertRaisesRegex(KitError,'contract|forbidden'):collect(self.project)
        path.write_text(original)
    def test_static_art_reference_inside_runtime_markup_must_resolve(self):
        path=self.project/'app/main.js';original=path.read_text()
        path.write_text(original+'''
const dynamicMarkup=`<img src="assets/rooms/${route}.svg">`;
''')
        self.assertIn('app/assets/rooms/group.svg',collect(self.project))
        path.write_text(original+'''
const brokenMarkup=`<img src="assets/missing-world.svg">`;
''')
        with self.assertRaisesRegex(KitError,'link missing'):collect(self.project)
    def test_vector_external_reference_or_missing_local_art_fails(self):
        path=self.project/'app/assets/explorer-world.svg';original=path.read_text()
        for suffix in ('<image href="missing-art.svg"/>','<image href="https://example.invalid/art.svg"/>','<style>path { fill: url(https://example.invalid/paint.svg); }</style>'):
            with self.subTest(suffix=suffix):
                path.write_text(original+suffix)
                with self.assertRaisesRegex(KitError,'missing|external'):collect(self.project)
                path.write_text(original)
        path.unlink()
        with self.assertRaisesRegex(KitError,'missing'):collect(self.project)
    def test_unlisted_secrets_raw_user_exports_and_recursion_excluded(self):
        for name in ('.env.local','private/child.csv','app/browser-state.json','app/private.json','research/snapshots/SRC-01.html','research/fulltexts/SRC-08.pdf','app/downloads/unlisted.zip'):
            path=self.project/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('Synthetic forbidden sentinel, not a secret')
        build(self.project)
        with zipfile.ZipFile(self.project/ARCHIVE) as archive:
            self.assertFalse(any('downloads/' in n or 'private' in n or '.env' in n or '/snapshots/' in n or n.endswith(('.pdf','.csv')) for n in archive.namelist()))
            self.assertNotIn(PREFIX+'PUBLIC-MANIFEST.json',archive.namelist())
            self.assertNotIn(PREFIX+'app/browser-state.json',archive.namelist())
    def test_catalog_traversal_and_private_paths_rejected(self):
        path=self.project/'materials/catalog.json';original=path.read_text();data=json.loads(original)
        for name in ('../../outside.md','private/notes.md'):
            with self.subTest(name=name):
                data['items'][0]['path']=name;path.write_text(json.dumps(data))
                with self.assertRaises(KitError):collect(self.project)
        path.write_text(original)
    def test_same_bytes_symlink_still_rejected(self):
        path=self.project/'app/assets/fonts/Lora.ttf';outside=Path(self.temp.name)/'font.ttf';outside.write_bytes(path.read_bytes());path.unlink();path.symlink_to(outside)
        with self.assertRaisesRegex(KitError,'escapes|symlink'):collect(self.project)
    def test_stale_runtime_requires_explicit_rebuild(self):
        build(self.project);path=self.project/'app/main.js';path.write_text(path.read_text()+'\n// harmless reviewed source revision\n')
        self.assertEqual(verify(self.project)['status'],'FAIL')
        build(self.project);self.assertEqual(verify(self.project)['status'],'PASS')
    def test_archive_and_outer_tampering_detected(self):
        build(self.project);archive=self.project/ARCHIVE;archive.write_bytes(archive.read_bytes()+b'corrupt footer')
        self.assertEqual(verify(self.project)['status'],'FAIL')
        build(self.project);outer=self.project/OUTER;outer.write_bytes(outer.read_bytes()+b' ')
        self.assertEqual(verify(self.project)['status'],'FAIL')
    def test_missing_module_or_font_asset_fails_graph(self):
        for name,suffix in [('app/main.js',"\nimport './missing-runtime.js';\n"),('app/styles.css',"\nbody { background: url('assets/missing.png'); }\n")]:
            with self.subTest(name=name):
                path=self.project/name;original=path.read_text();path.write_text(original+suffix)
                with self.assertRaisesRegex(KitError,'link missing'):collect(self.project)
                path.write_text(original)
    def test_resources_and_authored_copies_cannot_diverge(self):
        path=self.project/'materials/en/curriculum/lesson-02.md';path.write_text(path.read_text()+'\nChanged draft\n')
        with self.assertRaisesRegex(KitError,'copy differs'):collect(self.project)
    def test_package_readme_and_protocol_links_resolve_without_tools(self):
        files=collect(self.project)
        self.assertNotIn('tools/check_public.py',files)
        self.assertNotIn('tools/verify_research.py',files)
        for name in ['README.md','README.en.md','docs/SHARING-WEB02.md','docs/SHARING-WEB02.en.md']:
            self.assertIn(name,files)
            self.assertNotIn('python3 -B tools/check_public.py',files[name].decode())

if __name__=='__main__':unittest.main()
