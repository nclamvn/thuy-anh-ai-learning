#!/usr/bin/env python3
"""Deterministic, metadata-only authored review handoff; no user/browser/raw corpus data."""
from __future__ import annotations
import argparse
import io
import json
import os
import posixpath
import re
from urllib.parse import unquote, urlsplit
from pathlib import Path, PurePosixPath
import tempfile
import zipfile
from build_resources import KitError, digest, encode, markdown_links, read_json, require, validate_resource_links

RELEASE='WEB02'
ARCHIVE='app/downloads/project-review-WEB02.zip'
OUTER='app/downloads/project-review-WEB02.json'
INNER='CONTENT-MANIFEST.json'
PREFIX='thuy-anh-ai-learning-WEB02/'
RUNTIME=('index.html','styles.css','main.js','model.js','provider.js','locale.js','resources-client.js','legacy-p01.js','handoff.js','favicon.svg','assets/brandmark.svg','assets/fonts/Lora.ttf','assets/fonts/Lora-OFL.txt','assets/fonts/BeVietnamPro-Regular.ttf','assets/fonts/BeVietnamPro-SemiBold.ttf','assets/fonts/BeVietnamPro-OFL.txt')
ROOT=('LICENSE.md','PROVENANCE.md','start-local.command','docs/SHARING-WEB02.md','docs/SHARING-WEB02.en.md')
REFERENCES=('sources.json','claims.jsonl','domain.yaml','fulltexts/capture-manifest.json')
BENCHMARKS=('task_cases.json','response_template.json','provider-config.template.json','fixtures/synthetic_responses.json')
PACKAGE_READMES={
'README.md':'''# Bộ bàn giao review · WEB02

Bộ offline này gồm ứng dụng hiện tại, 54 tài liệu VI +54 bản EN, ba bài nháp song ngữ, nguồn học liệu, metadata tham khảo và benchmark/template giả định. [English](README.en.md). Dành cho diễn tập người lớn với dữ liệu giả; không là phê duyệt giáo dục, pilot với trẻ hay dịch vụ production.

## Mở trên máy

Giải nén nguyên thư mục. Cần Python 3.10+ có sẵn; không cài dependency, không cần tài khoản/API key.

```sh
python3 -B -m http.server 8875 --bind 127.0.0.1 --directory app
```

Mở http://127.0.0.1:8875/#overview, hoặc chạy ./start-local.command. Toggle VI/EN ở đầu trang. Chỉ dùng dữ liệu giả: dữ liệu buổi học và ghi chú reviewer lưu riêng trong trình duyệt; không gửi server/tự đồng bộ giữa người hay máy. Xuất backup hoặc phiếu góp ý JSON để bàn giao có chủ đích; phiếu góp ý chưa có luồng import. Origin offline khác origin Vercel nên không tự có dữ liệu cũ. Preview không là xác thực hay phân quyền.

Link tải ZIP trong app là chức năng bản online; downloads không được lồng vào ZIP này. Bản offline không có bản ZIP tự tải lại. Website: https://thuy-anh-ai-learning.vercel.app/#overview · hướng dẫn: https://thuy-anh-ai-learning.vercel.app/#guide · nguồn: https://github.com/nclamvn/thuy-anh-ai-learning.

## Nội dung và tính toàn vẹn

CONTENT-MANIFEST.json liệt kê SHA-256/byte count của từng file, release WEB02 và fingerprint của bộ nội dung. Nó không tự băm chính nó, không là chữ ký hay bằng chứng hiệu quả. Outer manifest trên website ghi SHA/bytes của ZIP để đối chiếu trước khi giải nén. [Quy trình bàn giao](docs/SHARING-WEB02.md).

Ứng dụng dùng fixture cố ý có lỗi, không gọi live AI. Metadata nghiên cứu giữ URL/capture hash lịch sử; **không chứa raw toàn văn HTML/PDF**. Không có tools compiler/research verifier trong bộ này: corpus thiếu nên full-capture provenance không thể chạy lại. Manifest resources giữ lịch sử compile ban đầu; không được sửa để giả PASS. Dùng public source repo và bộ kiểm public nếu cần công cụ phát triển; bộ này là handoff có thể mở trực tiếp.

Không chứa dữ liệu browser/người tham gia, consent, QA, env/credentials hay phê duyệt người thật. Quyền sử dụng code/tài liệu dự án chưa được chọn license chung; giữ LICENSE/PROVENANCE và font OFL. Review chuyên gia, diễn tập độc lập, product/data/consent và mọi quyết định pilot/live/production còn cần người chịu trách nhiệm.
''',
'README.en.md':'''# Authored review handoff · WEB02

This offline kit contains the current application, 54 Vietnamese documents +54 authored English counterparts, three bilingual draft lessons, material sources, reference metadata and synthetic benchmark/templates. [Vietnamese](README.md). Scope: adult rehearsal with fictional data; no educational approval, child-pilot approval or production-service claim.

## Open locally

Extract the whole directory. Python 3.10+ must already be available; no dependency installation, account or API key is required.

```sh
python3 -B -m http.server 8875 --bind 127.0.0.1 --directory app
```

Open http://127.0.0.1:8875/#overview, or run ./start-local.command. Use the header VI/EN toggle. Enter fictional data only. Learning records and reviewer notes stay separately in browser-local storage, with no server submission or automatic cross-person/device sync. Export a backup or review JSON for deliberate handoff; review JSON has no import flow. Offline and Vercel origins do not share stored records. Learner preview is not authentication or authorization.

The app's ZIP download links belong to the online distribution; downloads are not nested inside this ZIP. The offline kit has no recursively downloadable ZIP. Website: https://thuy-anh-ai-learning.vercel.app/#overview · guide: https://thuy-anh-ai-learning.vercel.app/#guide · source: https://github.com/nclamvn/thuy-anh-ai-learning.

## Contents and integrity

CONTENT-MANIFEST.json records SHA-256/bytes for every file, release WEB02 and a content fingerprint. It does not hash itself and is not a signature or evidence of effectiveness. The online outer manifest records archive SHA/bytes for comparison before extraction. [Handoff protocol](docs/SHARING-WEB02.en.md).

The application uses deliberately flawed fixtures, not live AI. Research metadata preserves URLs/historical capture hashes; **raw HTML/PDF works are excluded**. No compiler/research-verifier tools are included in this kit: unavailable raw corpus prevents full-capture provenance revalidation. The resource manifest preserves the original compile history and must not be altered to fabricate PASS. Use the public source repository/public checks for development tools; this kit is a directly runnable handoff.

No browser/participant data, consent, QA, env/credentials or authenticated human approvals are included. A general project code/document license remains undecided; retain LICENSE/PROVENANCE and font OFL notices. Educational review, independent rehearsal, product/data/consent decisions and any pilot/live-AI/production decisions remain with responsible people.
'''}


def safe_file(project,relative):
    path=PurePosixPath(relative)
    require(relative==path.as_posix() and not path.is_absolute() and all(p not in ('.','..') and not p.startswith('.') for p in path.parts),f'unsafe share path: {relative}')
    require(not any(p.lower() in {'private','qa','backup','backups','snapshots','exports','observed','runtime','downloads','tests','conversations'} for p in path.parts),f'private/raw/recursive share path: {relative}')
    target=project/relative
    require(target.resolve().is_relative_to(project),f'share path escapes project: {relative}')
    require(not any((project/Path(*path.parts[:i])).is_symlink() for i in range(1,len(path.parts)+1)),f'share symlink forbidden: {relative}')
    require(target.is_file(),f'share source missing: {relative}')
    require(target.stat().st_size<=20*1024*1024,f'share source too large: {relative}')
    return target


def validate_links(files):
    def target(source,href):
        parsed=urlsplit(href)
        if parsed.scheme in ('https','http','mailto','data') or not parsed.path:return
        require(not parsed.scheme and not parsed.netloc and '\\' not in href,f'unsafe bundle link: {href}')
        name=posixpath.normpath(posixpath.join(posixpath.dirname(source),unquote(parsed.path)))
        require(not name.startswith('../') and not name.startswith('/') and name in files,f'bundle link missing/escaping: {source} -> {href}')
    for name,raw in files.items():
        if name.endswith('.md'):
            for href in markdown_links(raw.decode('utf-8')):target(name,href)
        if name.startswith('app/') and name.endswith('.js'):
            body=raw.decode('utf-8')
            imports=re.findall(r"(?:import|export)\s+(?:(?:[^;\n]*?)\s+from\s+)?['\"]([^'\"]+)['\"]",body)
            imports+=re.findall(r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",body)
            for href in imports:
                require(href.startswith(('./','../')),f'nonlocal runtime module: {href}')
                target(name,href)
        if name.startswith('app/') and name.endswith('.css'):
            for href in re.findall(r"url\(\s*['\"]?([^'\")\s]+)",raw.decode('utf-8')):
                require(not urlsplit(href).scheme or href.startswith('data:'),f'external stylesheet asset: {href}')
                target(name,href)
        if name=='app/index.html':
            for href in re.findall(r'(?:src|href)=[\"\']([^\"\']+)',raw.decode('utf-8')):target(name,href)


def collect(project):
    project=project.resolve();files={}
    def add(name):
        require(name not in files,f'duplicate share path: {name}')
        files[name]=safe_file(project,name).read_bytes()
    for relative in RUNTIME:add('app/'+relative)
    resources,_=read_json(project/'app/resources/manifest.json')
    require(resources['fingerprint']==digest(encode({'inputs':resources['inputs'],'outputs':resources['outputs']})),'frozen resource manifest corrupt')
    for name,sha in resources['outputs'].items():
        add('app/resources/'+name);require(digest(files['app/resources/'+name])==sha,f'frozen resource stale: {name}')
    add('app/resources/manifest.json')
    payloads={name.removeprefix('app/resources/'):raw for name,raw in files.items() if name.startswith('app/resources/')}
    validate_resource_links(payloads)
    catalog,_=read_json(project/'materials/catalog.json');add('materials/catalog.json');add('materials/curriculum/lessons.json')
    require(len(catalog['items'])==54,'review bundle requires 54 reviewed catalog documents')
    for item in catalog['items']:
        require('en' in item.get('translations',{}),f'authored English document missing: {item["id"]}')
        for presentation in (item,item['translations']['en']):
            name=presentation['path'];add('materials/'+name)
            require(files['materials/'+name]==payloads[name],f'authored/compiled copy differs: {name}')
    require(files['materials/curriculum/lessons.json']==payloads['curriculum/lessons.json'],'authored/compiled lessons differ')
    for name in ROOT:add(name)
    for name in REFERENCES:add('research/'+name)
    for name in BENCHMARKS:add('benchmarks/'+name)
    for name,content in PACKAGE_READMES.items():files[name]=content.encode('utf-8')
    validate_links(files)
    require(sum(map(len,files.values()))<20*1024*1024,'review bundle too large')
    return files


def prepared(project):
    files=collect(project)
    entries={name:{'sha256':digest(raw),'bytes':len(raw)} for name,raw in sorted(files.items())}
    fingerprint=digest(encode({'release':RELEASE,'files':entries}))
    manifest={'schemaVersion':1,'dataKind':'authored-review-handoff','release':RELEASE,'sourceFingerprint':fingerprint,'catalogDocuments':54,'authoredLanguageDocuments':108,'documentCountScope':'catalog entries only; package support documents excluded','files':entries,'limits':'Synthetic adult rehearsal; references metadata only; excludes raw third-party works/user records; not a signature or educational approval.'}
    files[INNER]=encode(manifest)
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for name,raw in sorted(files.items()):
            info=zipfile.ZipInfo(PREFIX+name,date_time=(2026,10,3,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3
            info.external_attr=(0o100755 if name=='start-local.command' else 0o100644)<<16
            archive.writestr(info,raw)
    raw=output.getvalue()
    outer={'schemaVersion':1,'dataKind':'authored-review-download','release':RELEASE,'archive':'project-review-WEB02.zip','sha256':digest(raw),'bytes':len(raw),'fileCount':len(files),'files':{name:{'sha256':digest(payload),'bytes':len(payload)} for name,payload in sorted(files.items())},'sourceFingerprint':fingerprint,'catalogDocuments':54,'authoredLanguageDocuments':108,'documentCountScope':'catalog entries only; package support documents excluded','languageDocuments':{'vi':54,'en':54},'lessons':3,'resourceFiles':len([p for p in files if p.startswith('app/resources/')]),'limits':'Full authored handoff; third-party raw corpus and all browser/user records excluded. No cryptographic signature or human approval.'}
    return raw,encode(outer),outer


def build(project):
    project=project.resolve();raw,metadata,outer=prepared(project)
    destination=project/'app/downloads';require(not destination.is_symlink() and destination.resolve().is_relative_to(project),'download destination symlink/escape forbidden')
    destination.mkdir(exist_ok=True)
    require(prepared(project)[2]['sourceFingerprint']==outer['sourceFingerprint'],'share sources changed during packaging')
    staged=[]
    try:
        for name,data in [('project-review-WEB02.zip',raw),('project-review-WEB02.json',metadata)]:
            require(not (destination/name).is_symlink(),f'download output symlink forbidden: {name}')
            with tempfile.NamedTemporaryFile(prefix='.share-',dir=destination,delete=False) as handle:handle.write(data);stage=Path(handle.name)
            staged.append((stage,destination/name))
        for source,target in staged:os.replace(source,target)
    finally:
        for stage,_ in staged:
            if stage.exists():stage.unlink()
    return {'status':'PASS',**{key:value for key,value in outer.items() if key!='files'}}


def verify(project):
    try:
        project=project.resolve();raw,metadata,outer=prepared(project)
        archive=project/ARCHIVE;manifest=project/OUTER
        require(not archive.is_symlink() and not manifest.is_symlink() and not archive.parent.is_symlink(),'download output symlink forbidden')
        require(archive.is_file() and archive.read_bytes()==raw,'share archive stale/missing: rebuild after deliberate source changes')
        require(manifest.is_file() and manifest.read_bytes()==metadata,'outer share manifest stale/missing')
        with zipfile.ZipFile(io.BytesIO(raw)) as contents:
            require(contents.testzip() is None,'share ZIP corrupt')
            inner=json.loads(contents.read(PREFIX+INNER));require(len(contents.namelist())==len(inner['files'])+1,'inner file count mismatch')
            for name,row in inner['files'].items():
                payload=contents.read(PREFIX+name);require(row=={'sha256':digest(payload),'bytes':len(payload)},f'inner share fingerprint mismatch: {name}')
        return {'status':'PASS',**{key:value for key,value in outer.items() if key!='files'}}
    except (KitError,OSError,KeyError,TypeError,ValueError,zipfile.BadZipFile) as exc:return {'status':'FAIL','errors':[str(exc)]}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    try:result=verify(args.project) if args.verify else build(args.project)
    except (KitError,OSError,KeyError,TypeError,ValueError) as exc:result={'status':'FAIL','errors':[str(exc)]}
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['status']=='PASS' else 2

if __name__=='__main__':raise SystemExit(main())
