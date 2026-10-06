#!/usr/bin/env python3
"""Explicit R04 public reference derivative. Never reads raw research captures."""
import argparse, hashlib, json, pathlib, re
FROZEN='3cc7fee4c0f745100b110155fdc4bceca434f526cdd143ccc49704c048811b8f'
ROOT=pathlib.Path(__file__).resolve().parents[1]
IDS=['R02-01','R02-02','R02-03','R02-04','R02-06','R02-07','R02-08']+[f'R03-{n:02}' for n in range(1,8)]
def sha(b): return hashlib.sha256(b).hexdigest()
def encode(d): return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
STYLE='''\n<!-- R04:host-style -->\n<style>.host-return{position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:1rem;min-height:52px;padding:12px max(18px,calc((100vw - 1240px)/2));background:#182b39;color:#f5f1e7;flex-wrap:wrap}.host-return a{color:inherit;min-height:44px;display:inline-flex;align-items:center}.host-return small{opacity:.85}.host-return~.topbar{position:relative} section[id],#main,[id^="source-"]{scroll-margin-top:150px}.host-return a:focus-visible{outline:3px solid #cbb580;outline-offset:4px}@media print{.host-return{display:none}}body button:not([data-lang]){box-sizing:border-box;height:auto;min-height:48px;line-height:24px;padding:10px 16px;white-space:normal;border-width:1px;border-radius:2px}.language{box-sizing:border-box;height:48px;min-height:48px;border-width:1px;border-radius:2px}.language button{box-sizing:border-box;height:46px;min-height:46px;line-height:24px;padding-block:11px}.host-return a{min-height:48px}.filters input,.filters select:not([multiple]):is(:not([size]),[size='0'],[size='1']){box-sizing:border-box;height:48px;min-height:48px;line-height:24px;padding:10px 16px;border-width:1px;border-radius:2px}.filters select:not([multiple]):is(:not([size]),[size='0'],[size='1']){appearance:none;padding-right:48px;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 8'%3E%3Cpath d='m2 2 4 4 4-4' fill='none' stroke='%23334d5a' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-size:12px 8px;background-position:right 16px center}@media(forced-colors:active){.filters select:not([multiple]):is(:not([size]),[size='0'],[size='1']){appearance:auto;background-image:none;padding-right:16px;forced-color-adjust:auto}}</style>\n<!-- /R04:host-style -->\n'''
BAR='''\n<!-- R04:host-return -->\n<div class="host-return"><a id="reference-return" href="../#references?lang=vi">Về nguồn tham khảo của dự án</a><small id="reference-host-note">Báo cáo nghiên cứu về học tập cùng AI.</small><span id="reference-link-status" role="status"></span></div>\n<!-- /R04:host-return -->\n'''
BOOT='''\n<!-- R04:host-bootstrap -->\n<script>
(()=>{'use strict';
const requested=new URLSearchParams(location.search).get('lang');
if(['vi','en'].includes(requested))lang=requested;
COPY.vi.colophon='Bản đọc nghiên cứu trên website dự án, được dẫn xuất từ hồ sơ R03 ngày 06/10/2026. Chấp nhận trong phạm vi truy vết nguồn; chưa xác nhận phù hợp giáo dục, nhu cầu, hiệu quả tại địa phương hay duyệt của chủ dự án.';
COPY.en.colophon='Research reading edition on the project website, derived from the R03 dossier dated 6 October 2026. Accepted for source traceability only; educational suitability, demand, local effectiveness and project-owner approval remain unvalidated.';
let alignmentTicket=0;
function syncHost(){const en=lang==='en',back=document.getElementById('reference-return');back.textContent=en?'Return to project references':'Về nguồn tham khảo của dự án';back.href='../#references?lang='+lang;document.getElementById('reference-host-note').textContent=en?'Research dossier on learning with AI.':'Báo cáo nghiên cứu về học tập cùng AI.';const url=new URL(location.href);url.searchParams.set('lang',lang);history.replaceState(null,'',url.pathname+url.search+url.hash);}
function sourceNode(){const status=document.getElementById('reference-link-status');if(!location.hash.startsWith('#source-')){status.textContent='';return null;}const id=location.hash.slice(1);if(!cards.some(c=>'source-'+c.id===id)){status.textContent=lang==='en'?'Unknown source section. Browse the source ledger below.':'Không tìm thấy mục nguồn. Xem danh mục nguồn bên dưới.';return null;}status.textContent='';const node=document.getElementById(id);if(node)node.open=true;return node;}
function settleSource(){const ticket=++alignmentTicket,hash=location.hash,node=sourceNode();if(!node)return;const align=()=>{if(ticket===alignmentTicket&&hash===location.hash)node.scrollIntoView({block:'start',behavior:'instant'});};const afterLayout=()=>requestAnimationFrame(()=>requestAnimationFrame(align));align();afterLayout();if(document.readyState!=='complete')window.addEventListener('load',afterLayout,{once:true});if(document.fonts?.ready)document.fonts.ready.then(afterLayout).catch(()=>{});}
render();syncHost();settleSource();
document.querySelectorAll('[data-lang]').forEach(b=>b.addEventListener('click',()=>{syncHost();settleSource();}));
window.addEventListener('hashchange',settleSource);
window.addEventListener('pageshow',settleSource);
})();
</script>\n<!-- /R04:host-bootstrap -->\n'''
BLOCKS=[(STYLE,'</head>'),(BAR,'<body>'),(BOOT,'</body>')]
def source_data(source):
 if sha(source)!=FROZEN: raise ValueError('Frozen source fingerprint mismatch')
 match=re.search(r'<script type="application/json" id="source-data">(.*?)</script>',source.decode(),re.S)
 if not match: raise ValueError('Missing authored source data')
 data=json.loads(match.group(1));cards=data['cards'];meta=data['meta']
 if [c['id'] for c in cards]!=IDS or meta['sourceReports']!=14 or meta['r03Claims']!=57 or sum(meta['sourceClaims'].values())!=92 or not meta['r03Final']: raise ValueError('Source contract mismatch')
 for c in cards:
  if c['implication']['status']!='AI_PROPOSAL' or len(c['provenance']['claimIDs'])!=meta['sourceClaims'][c['id']]: raise ValueError('Claim/proposal contract mismatch')
 return data
def derivative(source):
 text=source.decode()
 for block,anchor in BLOCKS:
  if text.count(anchor)!=1: raise ValueError('Unexpected source anchors')
  text=text.replace(anchor,anchor+block if anchor=='<body>' else block+anchor)
 return text.encode()
def recover(report):
 text=report.decode()
 for block,_ in BLOCKS:
  if text.count(block)!=1: raise ValueError('Hosted integration block changed')
  text=text.replace(block,'')
 source=text.encode();source_data(source);return source
def outputs(source):
 data=source_data(source);report=derivative(source)
 catalog=encode({'schemaVersion':1,'kind':'public-authored-reference-metadata','sourceHTMLSha256':FROZEN,'reportHref':'references/report.html','reportSha256':sha(report),'documents':14,'claimReferences':92,**data})
 receipt=encode({'schemaVersion':1,'protocol':'R04-frozen-authored-dossier-v1','sourceHTMLSha256':FROZEN,'dataSha256':sha(encode(data)),'files':{'catalog.json':{'sha256':sha(catalog),'bytes':len(catalog)},'report.html':{'sha256':sha(report),'bytes':len(report)}}})
 return {'catalog.json':catalog,'report.html':report,'build.json':receipt}
def check(out):
 source=recover((out/'report.html').read_bytes())
 for name,expected in outputs(source).items():
  if (out/name).read_bytes()!=expected: raise ValueError(f'Stale or modified generated reference: {name}')
 return True
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source',type=pathlib.Path);parser.add_argument('--check',action='store_true');parser.add_argument('--out',type=pathlib.Path,default=ROOT/'app/references');args=parser.parse_args()
 if args.check:
  if args.source: parser.error('--check reconstructs the fingerprinted source; no --source')
  check(args.out);print('PASS references: 14 documents / 92 claim references; exact frozen source recovered');return
 if not args.source: parser.error('Explicit --source frozen authored HTML required to build')
 generated=outputs(args.source.read_bytes());args.out.mkdir(parents=True,exist_ok=True)
 for name,content in generated.items(): (args.out/name).write_bytes(content)
 print('Built references deterministically; existing materials and research untouched')
if __name__=='__main__': main()
