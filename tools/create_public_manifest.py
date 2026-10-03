#!/usr/bin/env python3
"""Refresh the public source receipt after reviewed edits; not a signature or approval."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
excluded={'.git','__pycache__','.venv','node_modules','exports','observed','runtime'}
sources=json.loads((root/'research/sources.json').read_text())
supplements=json.loads((root/'research/fulltexts/capture-manifest.json').read_text())
omitted=sorted({'research/'+s['snapshot'] for s in sources if s.get('capture_status')=='captured'}|{'research/fulltexts/'+s['file'] for s in supplements['captures'] if s.get('status')=='captured'})
files={}
for path in sorted(root.rglob('*')):
    relative=path.relative_to(root)
    if any(part in excluded for part in relative.parts) or path.name=='PUBLIC-MANIFEST.json' or path.name.endswith('.pyc'):continue
    if path.is_symlink():raise ValueError(f'public source symlink forbidden: {relative}')
    if not path.is_file():continue
    name=relative.as_posix()
    if name in omitted or path.suffix in {'.pdf','.zip'} or any(part.lower() in {'private','backup','backups','qa','snapshots'} for part in relative.parts):raise ValueError(f'raw/private distribution path forbidden: {name}')
    raw=path.read_bytes();files[name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
receipt={'schemaVersion':1,'dataKind':'public-references-only','release':'P03-public-01','files':files,'omittedRawCaptures':omitted,'limits':'Integrity receipt for available public sources only; missing research corpus cannot be reverified; no cryptographic signature or educational approval.'}
(root/'PUBLIC-MANIFEST.json').write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','files':len(files),'omittedRawCaptures':len(omitted)}))
