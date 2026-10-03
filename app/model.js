import {validateState as validateLegacyState, DEFAULT_ACTIVITY as LEGACY_ACTIVITY} from './legacy-p01.js';
export const SCHEMA = 3;
export const STORAGE_KEY = 'thuy-anh-ai-learning:p01:v1';
export const STEPS = [
  { key: 'initial', title: 'Suy nghĩ ban đầu', instruction: 'Hình chữ nhật dài 8 cm, rộng 5 cm. Em tự tính diện tích và chu vi, viết cách tính. Chưa dùng AI.' },
  { key: 'ai', title: 'Xem phản hồi AI mẫu', instruction: 'Người hướng dẫn mở phản hồi mẫu. Đọc và xem có điều gì cần kiểm tra.' },
  { key: 'concern', title: 'Chỉ ra điều cần kiểm', instruction: 'Em muốn kiểm tra khẳng định nào trong phản hồi? Vì sao?' },
  { key: 'sourceCheck', title: 'Đối chiếu kiến thức', instruction: 'Dùng hai thẻ công thức bên cạnh. Viết phép tính để đối chiếu với phản hồi AI.' },
  { key: 'revised', title: 'Sửa kết luận', instruction: 'Viết lại diện tích, chu vi và đơn vị. Nêu phần giữ lại hoặc sửa trong phản hồi AI.' },
  { key: 'explanation', title: 'Tự giải thích', instruction: 'Giải thích bằng lời của em vì sao cách kiểm tra này có ích và em đã thay đổi điều gì.' },
  { key: 'transfer', title: 'Bài mới · không có AI', instruction: 'Hình chữ nhật dài 9 cm, rộng 4 cm. Tự tính diện tích và chu vi, viết cách tính. Không dùng thẻ công thức hoặc phản hồi AI.' },
  { key: 'review', title: 'Người hướng dẫn đánh giá', instruction: 'Ghi đánh giá quan sát theo rubric nháp. Điểm do người hướng dẫn nhập; phần mềm không tự kết luận tiến bộ.' }
];
const stamp = () => new Date().toISOString();
const clone = value => JSON.parse(JSON.stringify(value));
const id = prefix => `${prefix}-${globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`}`;
export const RUBRIC_KEYS = ['verification', 'explanation', 'independent'];
const SAMPLE_PROVENANCE='Phản hồi AI mẫu · cố ý có lỗi';
export const DEFAULT_ACTIVITY={...clone(LEGACY_ACTIVITY),id:'LEGACY-MATH01',ageGroup:'13–15',durationMinutes:45,sourceIds:[],instructions:Object.fromEntries(STEPS.map(step=>[step.key,step.instruction])),sampleResponse:{text:'Diện tích = 8 × 5 = 40 cm². Chu vi = 8 × 5 = 40 cm.',provenance:SAMPLE_PROVENANCE,provider:'fixture-v1'},facilitatorNotes:'Hoạt động toán mẫu P01. Chưa duyệt sư phạm.',transferNotes:'Bài độc lập không AI: dài 9 cm, rộng 4 cm. Người hướng dẫn quan sát, không tự chấm.',review:null};
export function freshState(){return{schemaVersion:SCHEMA,dataKind:'synthetic-demo',savedAt:stamp(),learners:[{id:'MAU-001',ageGroup:'13–15',consent:'Đồng ý mẫu · không có giá trị đồng ý thật'},{id:'MAU-002',ageGroup:'13–15',consent:'Chưa đồng ý mẫu · chỉ dùng thử giao diện'}],activities:[clone(DEFAULT_ACTIVITY)],selectedActivityId:DEFAULT_ACTIVITY.id,sessions:[],activeSessionId:null,observations:[],readiness:[]};}
export function latestActivities(state){const byId=new Map();state.activities.forEach(a=>byId.set(a.id,a));return [...byId.values()];}
export function selectedActivity(state){return state.activities.filter(a=>a.id===state.selectedActivityId).at(-1)??state.activities.at(-1);}
export function selectActivity(state,activityId){if(!state.activities.some(a=>a.id===activityId))throw new Error('Không tìm thấy hoạt động.');state.selectedActivityId=activityId;}
const isText=(v,max=10000)=>typeof v==='string'&&v.length<=max;
const validId=v=>isText(v,100)&&/^[A-Z0-9][A-Z0-9_-]{2,99}$/.test(v);
function activityProblem(a){
 if(!a||!validId(a.id)||!Number.isInteger(a.version)||a.version<1)return 'Mã/phiên bản hoạt động không hợp lệ.';
 if(!isText(a.title,200)||!a.title.trim()||!isText(a.goal,4000)||!a.goal.trim())return 'Nhập tên hoạt động và mục tiêu trong giới hạn.';
 if(a.approvedBy!==null||a.provenance!==LEGACY_ACTIVITY.provenance)return 'Không được tự gắn phê duyệt sư phạm.';
 if(!['8–12','13–15','16–18'].includes(a.ageGroup)||!Number.isInteger(a.durationMinutes)||a.durationMinutes<10||a.durationMinutes>240)return 'Chọn nhóm tuổi và thời lượng dự kiến 10–240 phút.';
 if(!Array.isArray(a.sourceIds)||a.sourceIds.length>30||a.sourceIds.some(v=>!validId(v))||new Set(a.sourceIds).size!==a.sourceIds.length)return 'Source ID không hợp lệ hoặc trùng.';
 if(!a.instructions||typeof a.instructions!=='object'||Object.keys(a.instructions).length!==8)return 'Cả 8 bước cần hướng dẫn, tối đa 4.000 ký tự mỗi bước.';
 const invalidStep=STEPS.find(st=>!isText(a.instructions[st.key],4000)||!a.instructions[st.key].trim());if(invalidStep)return `Cả 8 bước cần hướng dẫn. Thiếu hoặc vượt 4.000 ký tự ở bước: ${invalidStep.title}.`;
 if(!Array.isArray(a.sourceCards)||a.sourceCards.length<1||a.sourceCards.length>12||a.sourceCards.some(c=>!c||!isText(c.title,200)||!c.title.trim()||!isText(c.text,4000)||!c.text.trim()))return 'Cần 1–12 thẻ nguồn với tên và nội dung.';
 if(!a.sampleResponse||!isText(a.sampleResponse.text,10000)||!a.sampleResponse.text.trim()||a.sampleResponse.provenance!==SAMPLE_PROVENANCE||!isText(a.sampleResponse.provider,100)||!a.sampleResponse.provider.trim())return 'Nhập phản hồi AI mẫu và giữ nhãn mẫu có lỗi.';
 if(!Array.isArray(a.rubric)||a.rubric.length!==3||a.rubric.some((r,i)=>!r||r.key!==RUBRIC_KEYS[i]||!isText(r.title,200)||!r.title.trim()||!isText(r.description,4000)||!r.description.trim()))return 'Cần đủ 3 tiêu chí rubric có tên và mô tả.';
 if(!isText(a.facilitatorNotes,10000)||!isText(a.transferNotes,10000)||!isText(a.createdAt,50)||!a.createdAt)return 'Ghi chú/thời điểm hoạt động không hợp lệ.';
 if(a.review!==null){const r=a.review;if(!r||!isText(r.reviewer,200)||!r.reviewer.trim()||!isText(r.notes,10000)||!r.notes.trim()||!['ready-for-rehearsal','revise-before-rehearsal'].includes(r.decision)||!isText(r.at,50)||!r.at||r.scope!=='local-rehearsal-unverified-identity')return 'Rà soát cần người, ý kiến, quyết định diễn tập và phạm vi local; không phải phê duyệt trẻ thật.';}
 if(a.translations!==undefined&&(!a.translations||Object.keys(a.translations).some(k=>k!=='en')||!validEnglish(a.translations.en)))return 'Bản dịch tiếng Anh của học liệu không hợp lệ.';
 return null;
}
export function validateActivity(a){const problem=activityProblem(a);if(problem)throw new Error(problem);return clone(a);}
export function createActivity(state,values){const a={...clone(DEFAULT_ACTIVITY),...clone(values),id:id('ACT').toUpperCase(),version:1,createdAt:stamp(),approvedBy:null,provenance:LEGACY_ACTIVITY.provenance,review:null};validateActivity(a);state.activities.push(a);state.selectedActivityId=a.id;return a;}
export function seedLessons(state,payload){
 if(!payload||payload.schemaVersion!==1||payload.dataKind!=='synthetic-curriculum-drafts'||!Array.isArray(payload.lessons)||payload.lessons.length<3||payload.lessons.length>30)throw new Error('Thư viện bài mẫu không đúng schema.');
 const checked=payload.lessons.map(l=>validateActivity({...clone(l),version:1,createdAt:stamp(),approvedBy:null,review:null}));
 if(new Set(checked.map(l=>l.id)).size!==checked.length)throw new Error('Mã bài mẫu trùng.');
 let count=0;for(const l of checked){if(!state.activities.some(a=>a.id===l.id)){state.activities.push(l);count++;}}
 return count;
}
export function reviewActivity(state,values){const base=selectedActivity(state);const next={...clone(base),version:base.version+1,createdAt:stamp(),review:{reviewer:values.reviewer.trim(),notes:values.notes.trim(),decision:values.decision,at:stamp(),scope:'local-rehearsal-unverified-identity'}};validateActivity(next);state.activities.push(next);return next;}
export function activitySteps(activity){return STEPS.map(step=>({...step,instruction:activity.instructions[step.key]}));}
export function migrateP01(input){const legacy=validateLegacyState(input);const enrich=a=>({...clone(DEFAULT_ACTIVITY),...clone(a),id:'LEGACY-MATH01',review:null});return validateState({...legacy,schemaVersion:SCHEMA,observations:[],readiness:[],activities:legacy.activities.map(enrich),selectedActivityId:'LEGACY-MATH01',sessions:legacy.sessions.map(s=>({...s,activity:enrich(s.activity)}))});}
export function addLearner(state, rawId, ageGroup) {
  const learnerId = rawId.trim().toUpperCase();
  if (!/^[A-Z0-9][A-Z0-9_-]{2,23}$/.test(learnerId)) throw new Error('Mã cần 3–24 ký tự: A–Z, 0–9, gạch ngang hoặc gạch dưới.');
  if(state.learners.some(l=>l.id===learnerId)) throw new Error('Mã học viên đã tồn tại.');
  if(!['8–12','13–15','16–18'].includes(ageGroup)) throw new Error('Nhóm tuổi không hợp lệ.');
  state.learners.push({id:learnerId,ageGroup,consent:'Đồng ý mẫu · không có giá trị đồng ý thật'});
}
export function reviseActivity(state,values){const base=selectedActivity(state);const next={...clone(base),translations:undefined,...clone(values),id:base.id,version:base.version+1,createdAt:stamp(),approvedBy:null,provenance:LEGACY_ACTIVITY.provenance,review:null};validateActivity(next);state.activities.push(next);return next;}
export function startSession(state,learnerId){if(!state.learners.some(l=>l.id===learnerId))throw new Error('Không tìm thấy học viên mẫu.');const session={id:id('PHIEN'),learnerId,activity:clone(selectedActivity(state)),step:0,status:'active',answers:{},aiResponse:null,evaluation:{reviewer:'',scores:{},note:''},events:[{at:stamp(),type:'started'}],startedAt:stamp(),completedAt:null};state.sessions.push(session);state.activeSessionId=session.id;return session;}
export function activeSession(state) {return state.sessions.find(s=>s.id===state.activeSessionId) ?? null;}
export function setAnswer(session, key, value) {
  if(session.status!=='active') throw new Error('Phiên đang tạm dừng hoặc đã hoàn thành.');
  if(!STEPS.some(s=>s.key===key && !['ai','review'].includes(key))) throw new Error('Trường bài làm không hợp lệ.');
  if(typeof value!=='string' || value.length>10000) throw new Error('Bài làm cần là văn bản dưới 10.000 ký tự.');
  session.answers[key]=value;
}
export function pauseSession(session) {
  if(session.status==='completed') throw new Error('Phiên đã hoàn thành.');
  session.status=session.status==='paused'?'active':'paused';session.events.push({at:stamp(),type:session.status==='paused'?'paused':'resumed'});
}
export function receiveAI(session, response) {
  if(session.status!=='active'||session.step!==1) throw new Error('Chỉ mở phản hồi tại bước AI của phiên đang hoạt động.');
  if(typeof response?.text!=='string'||response.provenance!==SAMPLE_PROVENANCE||response.text!==session.activity.sampleResponse.text) throw new Error('Phản hồi mẫu không hợp lệ.');
  session.aiResponse=clone(response);session.events.push({at:stamp(),type:'sample-response'});
}
export function evaluationReady(session) {return !!session.evaluation.reviewer.trim() && RUBRIC_KEYS.every(k=>Number.isInteger(session.evaluation.scores[k])&&session.evaluation.scores[k]>=0&&session.evaluation.scores[k]<=3);}
export function canAdvance(session) {
  if(session.status!=='active')return false;
  const key=STEPS[session.step]?.key;
  if(key==='ai')return !!session.aiResponse;
  if(key==='review')return evaluationReady(session)&&STEPS.filter(s=>!['ai','review'].includes(s.key)).every(s=>session.answers[s.key]?.trim())&&!!session.aiResponse;
  return !!session.answers[key]?.trim();
}
export function advance(session) {
  if(!canAdvance(session))throw new Error(session.status==='paused'?'Phiên đang tạm dừng.':'Hoàn thành dữ liệu bắt buộc ở bước này trước khi tiếp tục.');
  session.events.push({at:stamp(),type:'step-finished',step:session.step});
  if(session.step===STEPS.length-1){session.status='completed';session.completedAt=stamp();} else session.step++;
}
export function validateState(input){
 const fail=()=>{throw new Error('Backup không hợp lệ hoặc không thuộc schema được hỗ trợ. Dữ liệu hiện tại được giữ nguyên.');};
 if(input?.schemaVersion===1)return migrateP01(input);
 if(input?.schemaVersion===2)return validateState({...clone(input),schemaVersion:SCHEMA,observations:[],readiness:[]});
 if(!input||input.schemaVersion!==SCHEMA||input.dataKind!=='synthetic-demo'||!Array.isArray(input.learners)||!Array.isArray(input.activities)||!Array.isArray(input.sessions)||input.learners.length>1000||input.activities.length>1000||input.sessions.length>2000||!isText(input.savedAt,50))fail();
 const learnerIds=new Set();for(const l of input.learners){if(!l||!validId(l.id)||l.id.length>24||learnerIds.has(l.id)||!['8–12','13–15','16–18'].includes(l.ageGroup)||!isText(l.consent,200))fail();learnerIds.add(l.id);}
 const versions=new Map(),records=new Map();for(const a of input.activities){if(activityProblem(a))fail();const previous=versions.get(a.id)??0;if(a.version!==previous+1)fail();versions.set(a.id,a.version);records.set(`${a.id}@${a.version}`,a);}
 if(!input.activities.length||!versions.has(input.selectedActivityId))fail();
 const sessionIds=new Set();for(const s of input.sessions){
  if(!s||!isText(s.id,100)||sessionIds.has(s.id)||!learnerIds.has(s.learnerId)||activityProblem(s.activity)||JSON.stringify(s.activity)!==JSON.stringify(records.get(`${s.activity.id}@${s.activity.version}`))||!Number.isInteger(s.step)||s.step<0||s.step>=8||!['active','paused','completed'].includes(s.status)||!s.answers||typeof s.answers!=='object'||Array.isArray(s.answers)||!s.evaluation||!isText(s.evaluation.reviewer,200)||!isText(s.evaluation.note)||!s.evaluation.scores||typeof s.evaluation.scores!=='object'||Array.isArray(s.evaluation.scores)||!Array.isArray(s.events)||s.events.length>10000||!isText(s.startedAt,50))fail();
  sessionIds.add(s.id);
  if(Object.entries(s.answers).some(([k,v])=>!STEPS.some(st=>st.key===k&&!['ai','review'].includes(k))||!isText(v)))fail();
  if(Object.entries(s.evaluation.scores).some(([k,v])=>!RUBRIC_KEYS.includes(k)||!Number.isInteger(v)||v<0||v>3))fail();
  if(s.aiResponse!==null&&(!isText(s.aiResponse?.text)||s.aiResponse.provenance!==SAMPLE_PROVENANCE||(s.activity.id!=='LEGACY-MATH01'&&s.aiResponse.text!==s.activity.sampleResponse.text)))fail();
  if(s.events.some(e=>!e||!isText(e.at,50)||!isText(e.type,50)))fail();
  for(let n=0;n<s.step;n++){const key=STEPS[n].key;if(key==='ai'?!s.aiResponse:!s.answers[key]?.trim())fail();}
  if(s.status==='completed'&&(s.step!==7||!evaluationReady(s)||!isText(s.completedAt,50)||!s.completedAt))fail();
 }
 if(input.activeSessionId!==null&&!sessionIds.has(input.activeSessionId))fail();
 if(!Array.isArray(input.observations)||!Array.isArray(input.readiness)||input.observations.length>5000||input.readiness.length>1000)fail();
 const observations=input.observations.map(o=>{if(o&&['activityId','activityVersion','learnerId'].every(key=>!Object.hasOwn(o,key))){const source=input.sessions.find(s=>s.id===o.sessionId);if(source)return {...o,activityId:source.activity.id,activityVersion:source.activity.version,learnerId:source.learnerId};}return o;});
 const observationIds=new Set();for(const o of observations){if(!validObservation(o)||observationIds.has(o.id)||!sessionIds.has(o.sessionId))fail();const source=input.sessions.find(s=>s.id===o.sessionId);if(o.activityId!==source.activity.id||o.activityVersion!==source.activity.version||o.learnerId!==source.learnerId)fail();observationIds.add(o.id);}
 const readinessIds=new Set();for(const r of input.readiness){if(!validReadiness(r)||readinessIds.has(r.key))fail();readinessIds.add(r.key);}
 return clone({...input,observations});
}
export function backupJSON(state) {return JSON.stringify({...state,savedAt:stamp()},null,2);}
export function restoreJSON(raw) {
  if(typeof raw!=='string'||raw.length>8_000_000)throw new Error('Backup vượt giới hạn 8 MB.');
  let parsed;try{parsed=JSON.parse(raw);}catch{throw new Error('Backup không phải JSON hợp lệ. Dữ liệu hiện tại được giữ nguyên.');}
  return validateState(parsed);
}
export function loadState(storage) {
  try {const raw=storage.getItem(STORAGE_KEY);return {state:raw===null?freshState():restoreJSON(raw),error:null};}
  catch(error){return {state:freshState(),error:`Không đọc được dữ liệu lưu: ${error.message}. Đang dùng bộ mẫu tạm trong bộ nhớ; chưa ghi đè dữ liệu cũ.`};}
}
export function saveState(storage,state) {
  try {storage.setItem(STORAGE_KEY,backupJSON(state));return null;}
  catch(error){return `Không lưu được trên trình duyệt: ${error.message}. Bài làm vẫn ở bộ nhớ; hãy xuất backup trước khi đóng trang.`;}
}
export function reportText(state,session) {
  const learner=state.learners.find(l=>l.id===session.learnerId);
  const fields=[['Bài ban đầu · không AI','initial'],['Điều cần kiểm','concern'],['Đối chiếu học liệu nháp','sourceCheck'],['Bài sửa · có hỗ trợ','revised'],['Tự giải thích','explanation'],['Bài mới · không AI','transfer']];
  return ['LỚP THỰC HÀNH AI · BÁO CÁO DỮ LIỆU MẪU',`Phiên: ${session.id}`,`Học viên: ${learner.id} · ${learner.ageGroup} · dữ liệu mẫu`,`Hoạt động: ${session.activity.title} · ${session.activity.id} · v${session.activity.version}`,session.activity.provenance,`Rà soát local: ${session.activity.review?session.activity.review.reviewer+' / '+session.activity.review.decision:'Chưa rà soát; nháp'}`,`Ý kiến rà soát local: ${session.activity.review?.notes??'Chưa có'}`,`Thời điểm rà soát local: ${session.activity.review?.at??'Chưa có'}`,'Danh tính rà soát local chưa xác thực; chỉ diễn tập người lớn, chưa phê duyệt dùng với trẻ.',`Nhóm tuổi: ${session.activity.ageGroup}; thời lượng dự kiến: ${session.activity.durationMinutes} phút (chưa đo)`,`Nguồn tham chiếu: ${session.activity.sourceIds.join(', ')||'Chưa gắn source ID'}`,`Trạng thái: ${session.status}`,`Bắt đầu: ${session.startedAt}`,`Hoàn thành: ${session.completedAt??'Chưa hoàn thành'}`,'',...fields.flatMap(([title,key])=>[title,session.answers[key]||'Chưa có bài làm','']),`Phản hồi AI mẫu: ${session.aiResponse?.text??'Chưa mở'}`,'',`Đánh giá của người hướng dẫn: ${session.evaluation.reviewer||'Chưa đánh giá'}`,...session.activity.rubric.map(r=>`${r.title}: ${session.evaluation.scores[r.key]??'Chưa đánh giá'}`),`Ghi chú: ${session.evaluation.note||'Chưa có'}`,'','Provider thật: chưa tích hợp. Usage/cost: chưa đo.','Không kết luận hiệu quả giáo dục từ kết quả phần mềm hoặc rubric nháp.'].join('\n');
}

export const READINESS_KEYS=['product-focus','lesson-review','rehearsal','data-responsibility','backup-recovery','incident-response'];
function validObservation(o){return !!o&&isText(o.id,100)&&isText(o.at,50)&&!!o.at&&isText(o.sessionId,100)&&validId(o.activityId)&&Number.isInteger(o.activityVersion)&&o.activityVersion>0&&validId(o.learnerId)&&Number.isInteger(o.step)&&o.step>=0&&o.step<8&&['observed','reported','interpretation'].includes(o.kind)&&['none','prompt','hint','worked-example','technical'].includes(o.support)&&Number.isFinite(o.minutes)&&o.minutes>=0&&o.minutes<=1440&&isText(o.observer,200)&&!!o.observer.trim()&&isText(o.description,4000)&&!!o.description.trim()&&isText(o.issue,4000)&&o.scope==='synthetic-adult-rehearsal';}
function validReadiness(r){return !!r&&READINESS_KEYS.includes(r.key)&&['pending','in-progress','ready-for-adult-rehearsal','needs-revision'].includes(r.status)&&isText(r.owner,200)&&isText(r.note,4000)&&isText(r.version,100)&&!!r.version.trim()&&isText(r.at,50)&&r.scope==='local-only-not-pilot-approval'&&(r.status!=='ready-for-adult-rehearsal'||(r.owner.trim()&&r.note.trim()));}
export function addObservation(state,values){const session=state.sessions.find(s=>s.id===values.sessionId);if(!session)throw new Error('Không tìm thấy phiên quan sát.');const o={...clone(values),id:id('OBS'),at:stamp(),step:session.step,activityId:session.activity.id,activityVersion:session.activity.version,learnerId:session.learnerId,scope:'synthetic-adult-rehearsal'};if(!validObservation(o))throw new Error('Quan sát cần người ghi, mô tả, loại bằng chứng, hỗ trợ và thời gian 0–1440 phút.');state.observations.push(o);return o;}
export function recordReadiness(state,values){const r={...clone(values),at:stamp(),scope:'local-only-not-pilot-approval'};if(!validReadiness(r))throw new Error('Readiness cần phiên bản; sẵn sàng diễn tập cần người chịu trách nhiệm và căn cứ.');const i=state.readiness.findIndex(x=>x.key===r.key);if(i<0)state.readiness.push(r);else state.readiness[i]=r;return r;}
export function activityPresentation(activity,locale='vi'){const en=activity.translations?.en;if(locale==='en'&&en)return {...clone(activity),...clone(en),id:activity.id,version:activity.version,review:activity.review,contentLanguage:'en',translationFallback:false};return {...clone(activity),contentLanguage:'vi',translationFallback:locale==='en'};}
export function workbenchText(state,locale='vi'){const labels=workbenchLabels(locale);return JSON.stringify({presentation:{language:locale,readiness:state.readiness.map(r=>({key:r.key,status:labels.status[r.status]})),observations:state.observations.map(o=>({id:o.id,evidenceType:labels.kind[o.kind],support:labels.support[o.support]}))},format:'P03-local-rehearsal-records',scope:'synthetic-adult-rehearsal',notPilotApproval:true,locale,readiness:state.readiness,observations:state.observations},null,2);}

function validEnglish(en){if(!en||typeof en!=='object'||Array.isArray(en))return false;const allowed=['title','goal','ageGroup','provenance','instructions','sourceCards','sampleResponse','rubric','facilitatorNotes','transferNotes'];if(Object.keys(en).some(k=>!allowed.includes(k)))return false;if(!isText(en.title,200)||!en.title.trim()||!isText(en.goal,4000)||!en.goal.trim()||!en.instructions||Object.keys(en.instructions).length!==8||STEPS.some(s=>!isText(en.instructions[s.key],4000)||!en.instructions[s.key].trim()))return false;if(!Array.isArray(en.sourceCards)||en.sourceCards.length<1||en.sourceCards.length>12||en.sourceCards.some(c=>!c||!isText(c.title,200)||!c.title.trim()||!isText(c.text,4000)||!c.text.trim()))return false;if(!en.sampleResponse||!isText(en.sampleResponse.text)||!en.sampleResponse.text.trim()||!isText(en.sampleResponse.provenance,200)||!isText(en.sampleResponse.provider,100))return false;if(!Array.isArray(en.rubric)||en.rubric.length!==3||en.rubric.some((r,i)=>!r||r.key!==RUBRIC_KEYS[i]||!isText(r.title,200)||!r.title.trim()||!isText(r.description,4000)||!r.description.trim()))return false;return isText(en.facilitatorNotes)&&isText(en.transferNotes)&&(!en.ageGroup||['8–12','13–15','16–18'].includes(en.ageGroup));}
export function seedTranslationCandidates(state,payload){if(!payload?.lessons)return [];return payload.lessons.filter(seed=>seed.translations?.en&&state.activities.some(a=>a.id===seed.id)).filter(seed=>{const latest=state.activities.filter(a=>a.id===seed.id).at(-1);return !latest.translations&&Object.keys(seed).filter(key=>key!=='translations').every(key=>JSON.stringify(seed[key])===JSON.stringify(latest[key]));}).map(seed=>seed.id);}
export function upgradeSeedTranslations(state,payload){seedLessons(clone(state),payload);const candidates=seedTranslationCandidates(state,payload);const editions=candidates.map(identifier=>{const base=state.activities.filter(a=>a.id===identifier).at(-1),source=payload.lessons.find(l=>l.id===identifier);return validateActivity({...clone(base),version:base.version+1,createdAt:stamp(),translations:clone(source.translations),review:null});});state.activities.push(...editions);return editions.length;}

function workbenchLabels(locale){const en=locale==='en';return {status:en?{pending:'Pending','in-progress':'In progress','ready-for-adult-rehearsal':'Evidence recorded for adult rehearsal','needs-revision':'Needs revision'}:{pending:'Chưa làm','in-progress':'Đang làm','ready-for-adult-rehearsal':'Có căn cứ diễn tập người lớn','needs-revision':'Cần sửa'},kind:en?{observed:'Direct observation',reported:'Participant report',interpretation:'Observer interpretation'}:{observed:'Quan sát trực tiếp',reported:'Người tham gia kể lại',interpretation:'Diễn giải người ghi'},support:en?{none:'No support',prompt:'Task prompt',hint:'Hint','worked-example':'Worked example',technical:'Technical support'}:{none:'Không hỗ trợ',prompt:'Nhắc nhiệm vụ',hint:'Gợi ý','worked-example':'Ví dụ đã giải',technical:'Hỗ trợ kỹ thuật'}};}
