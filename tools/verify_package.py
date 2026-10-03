#!/usr/bin/env python3
"""Audit a P03 ZIP and optionally run offline checks after a safe clean extraction."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
from urllib.request import urlopen
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile
from build_resources import KitError, require
from package_project import EXCLUDED

PREFIX = 'thuy-anh-ai-learning/'


def static_smoke(project):
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(project / 'app')))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    responses = []
    try:
        for route in ('/', '/main.js', '/resources/catalog.json', '/resources/lessons.json', '/resources/manifest.json'):
            with urlopen(f'http://127.0.0.1:{server.server_port}{route}', timeout=5) as response:
                raw = response.read(); require(response.status == 200 and raw, f'clean static serve failed: {route}')
                if route.endswith('.json'): json.loads(raw)
                responses.append({'path':route,'status':response.status,'bytes':len(raw)})
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=2)
    return {'status':'PASS','scope':'Loopback static HTTP delivery only; no browser render or learner-data access','responses':responses}


def verify(archive_path, clean=False, node=None, serve_smoke=False):
    with zipfile.ZipFile(archive_path) as archive:
        require(archive.testzip() is None, 'ZIP CRC failure')
        names = archive.namelist(); require(len(names) == len(set(names)), 'duplicate ZIP entries')
        require(len(names) <= 5000 and sum(item.file_size for item in archive.infolist()) <= 100 * 1024 * 1024, 'ZIP size/count budget exceeded')
        for info in archive.infolist():
            name = info.filename; path = PurePosixPath(name)
            require(name == path.as_posix(), f'noncanonical ZIP path {name}')
            require(name.startswith(PREFIX) and not path.is_absolute() and '..' not in path.parts and '\\' not in name, f'unsafe ZIP path {name}')
            require((info.external_attr >> 16) & 0o170000 != 0o120000, f'ZIP symlink forbidden {name}')
            parts = path.parts[1:]
            require(not any(part.startswith('.') for part in parts) or name == PREFIX + '.github/workflows/checks.yml', f'hidden ZIP entry {name}')
            require(not any(part.lower() in EXCLUDED or part.lower().startswith(('qa-', 'private', 'conversation', 'raw-conversation')) for part in parts), f'private/runtime ZIP entry {name}')
        manifest = json.loads(archive.read(PREFIX + 'PACKAGE-MANIFEST.json'))
        require(isinstance(manifest, dict), 'manifest must be an object')
        require(manifest.get('release') == 'P03' and manifest.get('dataKind') == 'portable-local-kit', 'wrong release manifest')
        files = manifest.get('files'); require(isinstance(files, dict), 'missing package files map')
        require(set(names) == {PREFIX + name for name in files} | {PREFIX + 'PACKAGE-MANIFEST.json'}, 'manifest does not exactly cover ZIP')
        for name, record in files.items():
            require(isinstance(name, str) and isinstance(record, dict) and set(record) == {'sha256', 'bytes'}, 'invalid manifest file entry')
            require(isinstance(record['sha256'], str) and len(record['sha256']) == 64 and type(record['bytes']) is int and record['bytes'] >= 0, f'invalid manifest fingerprint {name}')
            raw = archive.read(PREFIX + name)
            require(record.get('sha256') == hashlib.sha256(raw).hexdigest() and record.get('bytes') == len(raw), f'package fingerprint mismatch {name}')
        for name in ('app/index.html','materials/catalog.json','delivery/VERIFY-P03.json','tools/check_all.py','start-local.command'):
            require(name in files, f'required portable artifact missing {name}')
        report = {'status':'PASS','release':'P03','files':len(names),'sha256':hashlib.sha256(Path(archive_path).read_bytes()).hexdigest(),'cleanExtraction':None,'externalNetworkCalls':0,'providerCalls':0}
        if clean or serve_smoke:
            with tempfile.TemporaryDirectory(prefix='thuy-anh-p03-clean-') as temporary:
                archive.extractall(temporary)
                project = Path(temporary) / PREFIX.rstrip('/')
                command = [sys.executable, '-B', 'tools/check_all.py']
                if node: command += ['--node', node]
                result = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=240)
                require(result.returncode == 0, f'clean extracted checks failed: {result.stdout} {result.stderr}')
                parsed = json.loads(result.stdout)
                report['cleanExtraction'] = {'status':'PASS','checks':[{'check':item['check'],'status':item['status']} for item in parsed['checks']]}
                if serve_smoke:
                    report['staticServe'] = static_smoke(project)
                    report['loopbackRequests'] = 5
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archive',type=Path);parser.add_argument('--clean',action='store_true');parser.add_argument('--node');parser.add_argument('--serve-smoke',action='store_true');args=parser.parse_args()
    try: result=verify(args.archive,args.clean,args.node,args.serve_smoke)
    except (KitError,OSError,ValueError,KeyError,zipfile.BadZipFile,subprocess.TimeoutExpired) as error: result={'status':'FAIL','errors':[str(error)]}
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['status']=='PASS' else 2

if __name__=='__main__': raise SystemExit(main())
