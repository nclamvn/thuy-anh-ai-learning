#!/usr/bin/env python3
"""Refresh a reviewed public source receipt; not a signature or release approval."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

EXCLUDED={'dist','.git','.vercel','__pycache__','.venv','node_modules','exports','observed','runtime'}
PRIVATE={'private','backup','backups','qa','snapshots','raw','conversations'}
ARCHIVE='app/downloads/project-review-WEB02.zip'

def prepared(root):
    root=root.resolve()
    sources=json.loads((root/'research/sources.json').read_text())
    supplements=json.loads((root/'research/fulltexts/capture-manifest.json').read_text())
    omitted=sorted({'research/'+s['snapshot'] for s in sources if s.get('capture_status')=='captured'}|{'research/fulltexts/'+s['file'] for s in supplements['captures'] if s.get('status')=='captured'})
    files={}
    for path in sorted(root.rglob('*')):
        relative=path.relative_to(root)
        if any(part in EXCLUDED for part in relative.parts) or path.name=='PUBLIC-MANIFEST.json' or path.name.endswith('.pyc'):continue
        if path.is_symlink():raise ValueError(f'public source symlink forbidden: {relative}')
        if not path.is_file():continue
        name=relative.as_posix()
        private_name=path.name.lower()
        if name in omitted or path.suffix.lower()=='.pdf' or (path.suffix.lower()=='.zip' and name!=ARCHIVE) or any(part.lower() in PRIVATE for part in relative.parts) or private_name=='.env' or private_name.startswith('.env.') or private_name in {'project-feedback.json','project-feedback.md','browser-state.json'} or private_name.endswith('.backup.json') or (name.startswith('research/') and path.suffix.lower()=='.html'):
            raise ValueError(f'raw/private distribution path forbidden: {name}')
        raw=path.read_bytes();files[name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    return {'schemaVersion':1,'dataKind':'public-references-only','release':'DEPLOY-CLEANUP-public-20261007','files':files,'omittedRawCaptures':omitted,'limits':'Integrity receipt for available public sources only; frozen-dossier-derived references have a separate build receipt. Missing raw corpus cannot be reverified; no cryptographic signature or educational approval.'}

def build(root):
    root=root.resolve();receipt=prepared(root)
    destination=root/'PUBLIC-MANIFEST.json'
    if destination.is_symlink():raise ValueError('public manifest output symlink forbidden')
    destination.write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    return {'status':'PASS','release':receipt['release'],'files':len(receipt['files']),'omittedRawCaptures':len(receipt['omittedRawCaptures'])}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    try:result=build(args.project)
    except (ValueError,OSError,KeyError,TypeError) as exc:result={'status':'FAIL','errors':[str(exc)]}
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['status']=='PASS' else 2

if __name__=='__main__':raise SystemExit(main())
