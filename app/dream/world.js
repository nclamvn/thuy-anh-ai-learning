// P02 bounded renderer contract. P01 remains immutable; no provider/storage/renderer code.
const freeze=v=>{Object.freeze(v);for(const x of Object.values(v))if(x&&typeof x==='object')freeze(x);return v;};
export const BASE_SPEC=freeze({schemaVersion:2,id:'sky-whale',version:1,seed:45107,dataKind:'prepared-synthetic-demo',world:{sky:'sunset',cityScale:1,gardens:false,starBridge:false,whaleColor:'indigo'},invariants:['flying-whale','city-on-back'],choices:[{id:'whale-city',description:{vi:'Ví dụ chuẩn bị: cá voi bay mang thành phố.',en:'Prepared example: a flying whale carries a city.'},origin:'offline-suggestion',status:'prepared-example'}]});
export const WORLD_KEYS=Object.freeze(['sky','cityScale','gardens','starBridge','whaleColor']);
const clone=v=>JSON.parse(JSON.stringify(v));
const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
export function validateWorldSpec(v){
 if(!exact(v,['schemaVersion','id','version','seed','dataKind','world','invariants','choices'])||v.schemaVersion!==2||v.id!=='sky-whale'||!['prepared-synthetic-demo','local-session-story'].includes(v.dataKind)||!Number.isInteger(v.version)||v.version<1||v.version>100||!Number.isInteger(v.seed)||v.seed<1||v.seed>999999)throw Error('invalid-spec');
 const w=v.world;if(!exact(w,WORLD_KEYS)||!['sunset','night'].includes(w.sky)||!Number.isFinite(w.cityScale)||w.cityScale<.8||w.cityScale>1.3||typeof w.gardens!=='boolean'||typeof w.starBridge!=='boolean'||!['indigo','teal'].includes(w.whaleColor)||JSON.stringify(v.invariants)!=='["flying-whale","city-on-back"]'||!Array.isArray(v.choices)||v.choices.length>16)throw Error('invalid-spec');
 const ids=new Set();for(const c of v.choices){if(!exact(c,['id','description','origin','status'])||typeof c.id!=='string'||!/^[a-z0-9][a-z0-9-]{0,63}$/.test(c.id)||ids.has(c.id)||!exact(c.description,['vi','en'])||!['vi','en'].every(l=>typeof c.description[l]==='string'&&c.description[l].trim().length>0&&c.description[l].length<=500)||!['child','mentor','ai-proposal','session-input','offline-suggestion','imported-proposal'].includes(c.origin)||!['prepared-example','confirmed-in-session'].includes(c.status))throw Error('invalid-choice');ids.add(c.id);}return clone(v);
}
export function seededRandom(seed){let value=seed>>>0;return()=>{value=(Math.imul(value,1664525)+1013904223)>>>0;return value/4294967296;};}
export function layoutPlan(input){const s=validateWorldSpec(input),random=seededRandom(s.seed);return {houses:Array.from({length:12},(_,i)=>({x:(i%4-1.5)*1.65+(random()-.5)*.4,z:(Math.floor(i/4)-1)*1.5+(random()-.5)*.45,height:1.1+random()*1.1,roof:i%3})),stars:Array.from({length:100},()=>({x:(random()-.5)*90,y:10+random()*25,z:(random()-.5)*90})),lanterns:Array.from({length:5},(_,i)=>({id:`lantern-${i+1}`,x:-5+i*2.6,y:4.3+Math.sin(i*1.4),z:3.5+Math.cos(i)}))};}
export function worldDiff(before,after){const a=validateWorldSpec(before),b=validateWorldSpec(after);return WORLD_KEYS.filter(k=>a.world[k]!==b.world[k]).map(key=>({key,before:a.world[key],after:b.world[key]}));}
export function createWorldSession(compile,dispose=()=>{},{initialSpec=BASE_SPEC,initialArtifact=null}={}){
 if(typeof compile!=='function'||typeof dispose!=='function')throw Error('invalid-compiler');
 let spec=validateWorldSpec(initialSpec),artifact=initialArtifact,history=[],cleanupErrors=[];
 function compileCandidate(next){const candidate=compile(clone(next));if(!candidate||typeof candidate.then==='function')throw Error('compile-failed');return candidate;}
 function cleanup(old){if(old)try{dispose(old);}catch{cleanupErrors.push('dispose-failed');cleanupErrors=cleanupErrors.slice(-10);}}
 return {get spec(){return clone(spec);},get artifact(){return artifact;},get history(){return clone(history);},get cleanupErrors(){return [...cleanupErrors];},
 print(input){const next=validateWorldSpec(input),difference=worldDiff(spec,next),changed=difference.length>0||next.seed!==spec.seed;if(next.version!==(changed?spec.version+1:spec.version))throw Error('invalid-version');const rebuilt=changed||!artifact;const candidate=rebuilt?compileCandidate(next):artifact;const old=artifact;history=[...history,{before:spec.version,after:next.version,difference,changed,rebuilt}].slice(-100);spec=next;artifact=candidate;if(rebuilt&&old!==candidate)cleanup(old);return {artifact,spec:clone(spec),difference,changed,rebuilt};},
 reset(){const next=validateWorldSpec(BASE_SPEC),candidate=compileCandidate(next),old=artifact;spec=next;artifact=candidate;history=[];if(old!==candidate)cleanup(old);return {artifact,spec:clone(spec)};},
 dispose(){const old=artifact;artifact=null;cleanup(old);}
 };
}
