export const SCHEMA = 1;
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
export const DEFAULT_ACTIVITY = {
  version: 1, title: 'Kiểm chứng câu trả lời AI', goal: 'Nhận biết khẳng định cần kiểm, đối chiếu công thức và tự giải thích kết luận.',
  provenance: 'Học liệu mẫu · nháp chưa duyệt sư phạm', approvedBy: null,
  sourceCards: [{title:'Diện tích hình chữ nhật',text:'Diện tích = chiều dài × chiều rộng. Đơn vị diện tích: cm².'},{title:'Chu vi hình chữ nhật',text:'Chu vi = 2 × (chiều dài + chiều rộng). Đơn vị độ dài: cm.'}],
  rubric: [
    {key:'verification',title:'Kiểm chứng có căn cứ',description:'Quan sát việc chỉ ra khẳng định cần kiểm và đối chiếu công thức.'},
    {key:'explanation',title:'Tự giải thích',description:'Quan sát cách giải thích việc giữ hoặc sửa kết luận bằng lời của mình.'},
    {key:'independent',title:'Thực hiện bài độc lập',description:'Quan sát bài mới không có AI; ghi cách làm, không chỉ đáp số.'}
  ], createdAt: stamp()
};
export function freshState() {
  return {schemaVersion:SCHEMA, dataKind:'synthetic-demo', savedAt:stamp(), learners:[
    {id:'MAU-001',ageGroup:'13–15',consent:'Đồng ý mẫu · không có giá trị đồng ý thật'},
    {id:'MAU-002',ageGroup:'13–15',consent:'Chưa đồng ý mẫu · chỉ dùng thử giao diện'}
  ], activities:[clone(DEFAULT_ACTIVITY)], sessions:[], activeSessionId:null};
}
export function addLearner(state, rawId, ageGroup) {
  const learnerId = rawId.trim().toUpperCase();
  if (!/^[A-Z0-9][A-Z0-9_-]{2,23}$/.test(learnerId)) throw new Error('Mã cần 3–24 ký tự: A–Z, 0–9, gạch ngang hoặc gạch dưới.');
  if(state.learners.some(l=>l.id===learnerId)) throw new Error('Mã học viên đã tồn tại.');
  if(!['8–12','13–15','16–18'].includes(ageGroup)) throw new Error('Nhóm tuổi không hợp lệ.');
  state.learners.push({id:learnerId,ageGroup,consent:'Đồng ý mẫu · không có giá trị đồng ý thật'});
}
export function reviseActivity(state, values) {
  if(!values.title?.trim() || !values.goal?.trim()) throw new Error('Nhập tên hoạt động và mục tiêu.');
  if(values.title.length>200 || values.goal.length>4000) throw new Error('Nội dung vượt giới hạn.');
  const next=clone(state.activities.at(-1));
  next.version++; next.title=values.title.trim(); next.goal=values.goal.trim(); next.createdAt=stamp(); next.approvedBy=null;
  state.activities.push(next); return next;
}
export function startSession(state, learnerId) {
  if(!state.learners.some(l=>l.id===learnerId)) throw new Error('Không tìm thấy học viên mẫu.');
  const session={id:id('PHIEN'),learnerId,activity:clone(state.activities.at(-1)),step:0,status:'active',answers:{},aiResponse:null,evaluation:{reviewer:'',scores:{},note:''},events:[{at:stamp(),type:'started'}],startedAt:stamp(),completedAt:null};
  state.sessions.push(session);state.activeSessionId=session.id;return session;
}
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
  if(typeof response?.text!=='string'||response.provenance!=='Phản hồi AI mẫu · cố ý có lỗi') throw new Error('Phản hồi mẫu không hợp lệ.');
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
export function validateState(input) {
  const fail=()=>{throw new Error('Backup không hợp lệ hoặc không đúng schema P01. Dữ liệu hiện tại được giữ nguyên.');};
  if(!input||input.schemaVersion!==SCHEMA||input.dataKind!=='synthetic-demo'||!Array.isArray(input.learners)||!Array.isArray(input.activities)||!Array.isArray(input.sessions)||input.learners.length>1000||input.activities.length>200||input.sessions.length>2000)fail();
  const isText=(v,max=10000)=>typeof v==='string'&&v.length<=max;
  const learnerIds=new Set();
  for(const l of input.learners){if(!l||typeof l!=='object'||!isText(l.id,24)||!/^[A-Z0-9][A-Z0-9_-]{2,23}$/.test(l.id)||learnerIds.has(l.id)||!['8–12','13–15','16–18'].includes(l.ageGroup)||!isText(l.consent,200))fail();learnerIds.add(l.id);}
  const versions=new Set();
  const validActivity=a=>!!a&&Number.isInteger(a.version)&&a.version>0&&isText(a.title,200)&&!!a.title.trim()&&isText(a.goal,4000)&&!!a.goal.trim()&&a.approvedBy===null&&a.provenance===DEFAULT_ACTIVITY.provenance&&Array.isArray(a.sourceCards)&&a.sourceCards.length===2&&a.sourceCards.every(c=>c&&isText(c.title,200)&&isText(c.text,2000))&&Array.isArray(a.rubric)&&a.rubric.length===3&&a.rubric.every((r,i)=>r&&r.key===RUBRIC_KEYS[i]&&isText(r.title,200)&&isText(r.description,2000))&&isText(a.createdAt,50);
  for(const a of input.activities){if(!validActivity(a)||versions.has(a.version))fail();versions.add(a.version);}
  if(input.activities.length===0||!input.activities.every((a,i)=>a.version===i+1))fail();
  const sessionIds=new Set();
  for(const s of input.sessions){
    if(!s||typeof s!=='object'||!isText(s.id,100)||sessionIds.has(s.id)||!learnerIds.has(s.learnerId)||!validActivity(s.activity)||!versions.has(s.activity.version)||JSON.stringify(s.activity)!==JSON.stringify(input.activities.find(a=>a.version===s.activity.version))||!Number.isInteger(s.step)||s.step<0||s.step>=STEPS.length||!['active','paused','completed'].includes(s.status)||!s.answers||typeof s.answers!=='object'||Array.isArray(s.answers)||!s.evaluation||!isText(s.evaluation.reviewer,200)||!isText(s.evaluation.note,10000)||!s.evaluation.scores||typeof s.evaluation.scores!=='object'||Array.isArray(s.evaluation.scores)||!Array.isArray(s.events)||s.events.length>10000||!isText(s.startedAt,50))fail();
    sessionIds.add(s.id);
    if(Object.entries(s.answers).some(([k,v])=>!STEPS.some(step=>step.key===k&&!['ai','review'].includes(k))||!isText(v)))fail();
    if(Object.entries(s.evaluation.scores).some(([k,v])=>!RUBRIC_KEYS.includes(k)||!Number.isInteger(v)||v<0||v>3))fail();
    if(s.aiResponse!==null&&(!isText(s.aiResponse?.text,10000)||s.aiResponse.provenance!=='Phản hồi AI mẫu · cố ý có lỗi'))fail();
    if(s.events.some(e=>!e||!isText(e.at,50)||!isText(e.type,50)))fail();
    for(let n=0;n<s.step;n++){const key=STEPS[n].key;if(key==='ai'?!s.aiResponse:!s.answers[key]?.trim())fail();}
    if(s.status==='completed'&&(s.step!==7||!evaluationReady(s)||!isText(s.completedAt,50)||!s.completedAt))fail();
  }
  if(input.activeSessionId!==null&&!sessionIds.has(input.activeSessionId))fail();
  if(!isText(input.savedAt,50))fail();
  return clone(input);
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
  return ['LỚP THỰC HÀNH AI · BÁO CÁO DỮ LIỆU MẪU',`Phiên: ${session.id}`,`Học viên: ${learner.id} · ${learner.ageGroup} · dữ liệu mẫu`,`Hoạt động: ${session.activity.title} · v${session.activity.version}`,session.activity.provenance,`Trạng thái: ${session.status}`,`Bắt đầu: ${session.startedAt}`,`Hoàn thành: ${session.completedAt??'Chưa hoàn thành'}`,'',...fields.flatMap(([title,key])=>[title,session.answers[key]||'Chưa có bài làm','']),`Phản hồi AI mẫu: ${session.aiResponse?.text??'Chưa mở'}`,'',`Đánh giá của người hướng dẫn: ${session.evaluation.reviewer||'Chưa đánh giá'}`,...session.activity.rubric.map(r=>`${r.title}: ${session.evaluation.scores[r.key]??'Chưa đánh giá'}`),`Ghi chú: ${session.evaluation.note||'Chưa có'}`,'','Provider thật: chưa tích hợp. Usage/cost: chưa đo.','Không kết luận hiệu quả giáo dục từ kết quả phần mềm hoặc rubric nháp.'].join('\n');
}
