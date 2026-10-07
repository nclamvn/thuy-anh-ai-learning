#!/usr/bin/env python3
"""Verify the reviewed static Dream projection, exact canonical recovery and authored kit reproduction."""
from pathlib import Path
import argparse,json,hashlib,tempfile,subprocess,sys,shutil,re
P=Path(__file__).resolve().parents[1];D=P/'app/dream';S=P/'docs/dream/SOURCE.json';BUILD=P/'docs/dream/BUILD.json'
def require(value,message):
 if not value:raise ValueError(message)
def fp(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def recover(name,raw,meta):
 text=raw.decode()if name in ['main.js','index.html','style.css']else None;a=meta['adaptations']
 if name=='main.js':
  require(text.startswith(a['importPrefix']),'public OFF import missing');text=text[len(a['importPrefix']):]
  item=a['syncPrefix'];require(text.count(item['published'])==1,'public return adapter drift');text=text.replace(item['published'],item['canonical'],1)
  item=a['explanationHook'];require(text.count(item['published'])==1,'public explanation adapter drift');text=text.replace(item['published'],item['canonical'],1)
  for item in a['main'].values():require(text.count(item['published'])==1,'static OFF function drift');text=text.replace(item['published'],item['canonical'],1)
 elif name=='index.html':require(text.count(a['indexFooter'])==1,'public return footer drift');text=text.replace(a['indexFooter'],'',1)
 elif name=='style.css':require(text.endswith(a['styleSuffix']),'public return style drift');text=text[:-len(a['styleSuffix'])]
 return text.encode()if text is not None else raw

def inventory():
 out={}
 for f in sorted(D.rglob('*')):
  if not f.is_file()or '__pycache__'in f.parts:continue
  require(not f.is_symlink(),'Dream source symlink forbidden');rel=f.relative_to(P).as_posix();require(not any(x in {'server.mjs','provider.mjs','.env'}or x.startswith('.env')for x in f.parts),'private/backend in static Dream');out[rel]=fp(f.read_bytes())
 return out

def kit_projection(meta,write=False):
 with tempfile.TemporaryDirectory(prefix='dream-public-kit-')as tmp:
  root=Path(tmp)
  for name in ['render.py','CONTENT.json']:shutil.copyfile(D/'kit'/name,root/name)
  r=subprocess.run([sys.executable,'-B',str(root/'render.py')],capture_output=True,text=True);require(r.returncode==0,'kit renderer failed: '+r.stderr)
  projection=meta['kitPublicProjection'];require(projection['protocol']=='public-colophon-permanent-OFF-v1','public kit projection protocol drift')
  outputs={n:(root/n).read_bytes()for n in projection['canonicalOutputs']}
  for n,row in projection['canonicalOutputs'].items():require(fp(outputs[n])==row,'canonical kit reproduction mismatch: '+n)
  original=outputs['index.html'];text=original.decode()
  for item in projection['replacements']:
   require(text.count(item['canonical'])==1,'canonical kit colophon not unique');text=text.replace(item['canonical'],item['published'],1)
  public=text.encode();recovered=text
  for item in reversed(projection['replacements']):
   require(recovered.count(item['published'])==1,'public kit colophon not unique');recovered=recovered.replace(item['published'],item['canonical'],1)
  require(recovered.encode()==original,'public kit exact recovery failed')
  build=json.loads(outputs['BUILD.json']);build['outputSha256']=fp(public)['sha256'];build['files']['index.html']=fp(public);build['publicProjection']={'protocol':projection['protocol'],'canonicalIndexSha256':fp(original)['sha256'],'canonicalBuildSha256':fp(outputs['BUILD.json'])['sha256']}
  outputs['index.html']=public;outputs['BUILD.json']=(json.dumps(build,indent=2)+'\n').encode()
  for n,raw in outputs.items():
   if write:(D/'kit'/n).write_bytes(raw)
   else:require(raw==(D/'kit'/n).read_bytes(),'canonical public kit generated drift: '+n)
 return {'canonicalOutputsReproduced':len(outputs),'publicFooterLocales':2,'protocol':projection['protocol']}

def check_sources():
 meta=json.loads(S.read_text());require(meta['mode']=='public-static-OFF','Dream publication mode mismatch')
 for n,row in meta['canonicalRuntime'].items():require(fp(recover(n,(D/n).read_bytes(),meta))==row,'canonical Dream recovery mismatch: '+n)
 for n,row in meta['canonicalBackend'].items():require(fp((P/'source/dream-backend'/n).read_bytes())==row,'canonical source-only backend mismatch: '+n)
 main=(D/'main.js').read_text();require(not re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\s*\(',main) and '/api/'not in main,'public Dream must have no API request');require("import {applyPublicOff, syncPublicReturn, syncPublicExplanation} from './public-mode.js';"in main,'OFF adapter unavailable')
 mode=(D/'public-mode.js').read_text();require('lab.setLive(false)'in mode and not re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\s*\(',mode),'public adapter not permanently OFF')
 require(fp((D/'kit/CONTENT.json').read_bytes())['sha256']==meta['kitCanonicalSourceSha256'],'authored kit source drift')
 kit_projection(meta)
 data=json.loads((D/'kit/CONTENT.json').read_text());require(len(data['sections'])==11 and len(data['rehearsal']['scenarios'])==8,'prepared kit topology mismatch');require(all(s['actualResult']is None and s['observationStatus']=='not-observed'for s in data['rehearsal']['scenarios']),'fabricated observation')
 template=json.loads((D/'kit/observation-template.json').read_text());require(template['printId']is None and template['geometryVersion']is None and template['observerConfirmation']is None,'observation template not blank')
 # Bare three imports resolve through this exact same-origin map only.
 index=(D/'index.html').read_text();mapmatch=re.search(r'<script type="importmap">(.*?)</script>',index);require(mapmatch is not None and json.loads(mapmatch[1])=={'imports':{'three':'./vendor/three.module.js'}},'local Three importmap drift')
 require('../#overview'in index and 'target="_blank" rel="noopener"'in index,'safe project return link missing')
 return {'canonicalRuntimeRecovered':len(meta['canonicalRuntime']),'kitSections':11,'syntheticScenarios':8,'generatedKitFiles':7,'publicKitFooterLocales':2,'liveAI':'PERMANENTLY_OFF_STATIC','providerCalls':0,'rawCorpus':'UNAVAILABLE_REFERENCES_ONLY','limits':'Reconstructs accepted canonical source bytes; no original Completion/human studies included or asserted.'}

def run(write=False):
 if write:kit_projection(json.loads(S.read_text()),True)
 result=check_sources();payload={'schemaVersion':1,'edition':'DREAM-JOURNEY-public-20261007','dataKind':'public-static-synthetic-rehearsal','source':fp(S.read_bytes()),'files':inventory(),'verification':result}
 if write:BUILD.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
 else:require(json.loads(BUILD.read_text())==payload,'public Dream build receipt drift')
 return {'status':'PASS','files':len(payload['files']),**result}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
 try:print(json.dumps(run(args.write),indent=2))
 except(ValueError,OSError,KeyError)as e:print(json.dumps({'status':'FAIL','error':str(e)}));sys.exit(2)
