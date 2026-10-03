import {DEFAULT_ACTIVITY} from './model.js';
// Adapter independent of the learning state machine. No network/provider requests.
export async function requestSample({mode='success',delayMs=450,timeoutMs=1500,activity=DEFAULT_ACTIVITY}={}) {
  if(!['success','error','timeout'].includes(mode))throw new Error('Chế độ provider mẫu không hợp lệ.');
  return new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>{clearTimeout(work);reject(new Error('Mô phỏng timeout: provider mẫu chưa phản hồi. Có thể thử lại; bài làm được giữ nguyên.'));},timeoutMs);
    const work=setTimeout(()=>{
      if(mode==='timeout')return;
      clearTimeout(timeout);
      if(mode==='error')reject(new Error('Mô phỏng lỗi provider. Có thể thử lại; bài làm được giữ nguyên.'));
      else if(!activity?.sampleResponse?.text)reject(new Error('Hoạt động thiếu phản hồi mẫu.'));
      else resolve(JSON.parse(JSON.stringify(activity.sampleResponse)));
    },delayMs);
  });
}
