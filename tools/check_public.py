#!/usr/bin/env python3
"""Offline validation for the references-only public distribution; no network calls."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from build_resources import KitError, digest, encode, markdown_links, read_json, require, validate_resource_links, validate_lessons


def confined(root, relative):
    path = PurePosixPath(relative)
    require(not path.is_absolute() and relative == path.as_posix() and all(p not in ('..', '.') for p in path.parts), f'unsafe manifest path: {relative}')
    target = root / relative
    require(target.resolve().is_relative_to(root) and not any((root / Path(*path.parts[:i])).is_symlink() for i in range(1,len(path.parts)+1)), f'symlink/escape forbidden: {relative}')
    return target


def verify_distribution(project):
    project = project.resolve()
    errors=[]
    try:
        receipt,_=read_json(project/'PUBLIC-MANIFEST.json')
        require(receipt.get('dataKind')=='public-references-only' and isinstance(receipt.get('files'),dict), 'invalid public manifest schema')
        expected=set(receipt['files'])
        require('PUBLIC-MANIFEST.json' not in expected, 'manifest must not self-reference')
        for name,row in receipt['files'].items():
            path=confined(project,name)
            require(path.is_file(), f'public file missing: {name}')
            raw=path.read_bytes()
            require(row=={'bytes':len(raw),'sha256':digest(raw)}, f'public file fingerprint mismatch: {name}')
        # Git metadata, local caches/reports/exports are intentionally outside this source receipt.
        actual={p.relative_to(project).as_posix() for p in project.rglob('*') if p.is_file() and not any(part in {'dist','.git','.vercel','__pycache__','.venv','node_modules','exports','observed','runtime'} for part in p.relative_to(project).parts) and p.name!='PUBLIC-MANIFEST.json' and not p.name.endswith('.pyc')}
        require(actual==expected, f'unlisted source files: {sorted(actual-expected)}; missing: {sorted(expected-actual)}')
        sources,_=read_json(project/'research/sources.json')
        supplements,_=read_json(project/'research/fulltexts/capture-manifest.json')
        omitted={'research/'+row['snapshot'] for row in sources if row.get('capture_status')=='captured'}
        omitted.update('research/fulltexts/'+row['file'] for row in supplements['captures'] if row.get('status')=='captured')
        require(set(receipt.get('omittedRawCaptures',[]))==omitted,'raw exclusion declaration mismatch')
        for name in omitted: require(not confined(project,name).exists(), f'raw third-party capture must not be published: {name}')
        manifest,_=read_json(project/'app/resources/manifest.json')
        require(manifest['fingerprint']==digest(encode({'inputs':manifest['inputs'],'outputs':manifest['outputs']})), 'compiled manifest fingerprint mismatch')
        checked_inputs=0
        for name,sha in manifest['inputs'].items():
            path=confined(project,name)
            if name in omitted:
                require(not path.exists(),f'raw input unexpectedly present: {name}')
                continue
            require(path.is_file() and digest(path.read_bytes())==sha, f'available compiler input missing/stale: {name}')
            checked_inputs+=1
        payloads={}
        root=project/'app/resources'
        for name,sha in manifest['outputs'].items():
            path=confined(root,name); require(path.is_file(),f'compiled output missing: {name}')
            raw=path.read_bytes();require(digest(raw)==sha,f'compiled output stale: {name}');payloads[name]=raw
        actual_outputs={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        require(actual_outputs==set(payloads)|{'manifest.json'},'unlisted/missing compiled output')
        validate_resource_links(payloads)
        catalog,_=read_json(project/'materials/catalog.json')
        generated,_=read_json(root/'catalog.json')
        lessons,lesson_raw=read_json(project/'materials/curriculum/lessons.json')
        known={s['id'] for s in sources}|{s['sourceId'] for s in supplements['captures']}
        validate_lessons(lessons,known)
        require(payloads['curriculum/lessons.json']==lesson_raw and payloads['lessons.json']==encode(lessons),'lesson copies differ')
        require(len(catalog['items'])==len(generated['items']),'catalog item count differs')
        for source,output in zip(catalog['items'],generated['items']):
            require(set(source['sourceIds']).issubset(known),'catalog reference unknown')
            require(source['id']==output['id'],'catalog ordering differs')
            for key in ('id','title','description','category','path','status','sourceIds'): require(source[key]==output[key],f'catalog source-copy mismatch: {key}')
            for locale,presentation in [('vi',source),*source.get('translations',{}).items()]:
                name=presentation['path'];raw=confined(project/'materials',name).read_bytes()
                require(payloads.get(name)==raw,f'material source-copy mismatch: {name}')
                shown=output if locale=='vi' else output['translations'][locale]
                require(shown['href']=='resources/'+name,f'catalog href mismatch: {name}')
                if locale=='en':
                    urls={u for u in markdown_links((project/'materials'/source['path']).read_text()) if urlsplit(u).scheme in ('http','https')}
                    require(urls.issubset(set(markdown_links(raw.decode()))),f'English translation drops reference URLs: {name}')
        links=0
        for path in (project/'materials').rglob('*.md'):
            for href in markdown_links(path.read_text(encoding='utf-8')):
                links+=1;parsed=urlsplit(href)
                if parsed.scheme in ('http','https','mailto'):continue
                require(not parsed.scheme and not parsed.netloc and not href.startswith('/') and '\\' not in href,'unsafe authored material link')
                if parsed.path:
                    resolved=(path.parent/unquote(parsed.path)).resolve()
                    require(resolved.is_relative_to(project) and resolved.exists(),f'dead/escaped authored link: {href}')
        return {'status':'PASS','publicFiles':len(expected),'availableCompilerInputsChecked':checked_inputs,'compiledOutputsChecked':len(payloads),'catalogDocuments':len(catalog['items']),'englishDocuments':sum('en' in i.get('translations',{}) for i in catalog['items']),'lessons':len(lessons['lessons']),'authoredLinksChecked':links,'fullCaptureProvenance':{'status':'UNAVAILABLE','omittedRawCaptures':len(omitted),'reason':'References-only public distribution intentionally excludes raw third-party corpus. Metadata hashes are historical provenance pointers, not a new verification of missing works.'},'errors':[]}
    except (KitError,OSError,KeyError,TypeError,ValueError) as exc:
        errors.append(str(exc));return {'status':'FAIL','errors':errors}


def run(project,node=None):
    integrity=verify_distribution(project)
    results=[{'check':'public-source-integrity','status':integrity['status'],'result':integrity}]
    binary=node or os.environ.get('AI_LEARNING_NODE') or shutil.which('node')
    jobs=[('python-fault-tests',[sys.executable,'-B','-m','unittest','discover','-s','tools/tests','-v']),('unmeasured-benchmark',[sys.executable,'-B','tools/evaluate_responses.py','benchmarks/response_template.json']),('synthetic-benchmark',[sys.executable,'-B','tools/evaluate_responses.py','benchmarks/fixtures/synthetic_responses.json']),('inactive-provider-config',[sys.executable,'-B','tools/verify_provider_config.py','benchmarks/provider-config.template.json']),('authored-review-bundle',[sys.executable,'-B','tools/build_share_bundle.py','--verify']),('public-dream-source',[sys.executable,'-B','tools/build_dream.py','--check'])]
    if binary:jobs.extend([('static-build-tests',[binary,'--test','tools/tests/build_site.test.mjs']),('static-site-build',[binary,'tools/build_site.mjs']),('static-site-integrity',[binary,'tools/build_site.mjs','--check'])])
    if binary:jobs.append(('app-tests',[binary,'--test',*sorted(str(p.relative_to(project)) for p in (project/'app/tests').glob('*.test.mjs'))]))
    if binary:jobs.append(('source-only-backend-tests',[binary,'--test',*sorted(str(p.relative_to(project)) for p in (project/'source/dream-backend/tests').glob('*.test.mjs'))]))
    if binary:jobs.append(('dream-tests',[binary,'--test',*sorted(str(p.relative_to(project)) for p in (project/'app/dream/tests').glob('*.test.mjs'))]))
    else:results.append({'check':'app-tests','status':'FAIL','reason':'Node.js 18+ required; set --node or AI_LEARNING_NODE'})
    for name,command in jobs:
        result=subprocess.run(command,cwd=project,capture_output=True,text=True,timeout=120)
        results.append({'check':name,'status':'PASS' if result.returncode==0 else 'FAIL','exitCode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    # Exercise the unchanged strict verifier and expose its failure separately.
    strict=subprocess.run([sys.executable,'-B','tools/verify_research.py'],cwd=project,capture_output=True,text=True,timeout=120)
    strict_result=json.loads(strict.stdout)
    strict_state={'status':'UNAVAILABLE' if strict.returncode!=0 and integrity['status']=='PASS' else 'FAIL','strictVerifierStatus':strict_result['status'],'reason':'Missing raw corpus intentionally prevents strict provenance validation. Not included in PASS checks.','errorCodes':sorted({e['code'] for e in strict_result.get('errors',[])})}
    return {'status':'PASS' if all(r['status']=='PASS' for r in results) and strict_state['status']=='UNAVAILABLE' else 'FAIL','scope':'Available public source fingerprints/copies/links and synthetic offline fault tests only; full-capture provenance unavailable, no human/education/pilot/production approval','checks':results,'fullCaptureProvenance':strict_state}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--node');parser.add_argument('--report',type=Path);args=parser.parse_args()
    try:result=run(args.project.resolve(),args.node)
    except (OSError,ValueError,subprocess.TimeoutExpired) as exc:result={'status':'FAIL','errors':[str(exc)]}
    raw=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.report:args.report.write_text(raw,encoding='utf-8')
    print(raw);return 0 if result['status']=='PASS' else 2

if __name__=='__main__':raise SystemExit(main())
