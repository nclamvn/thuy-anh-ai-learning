// Authored interface copy only. Never machine-translate learner answers or authored documents.
export const LOCALE_KEY='thuy-anh-ai-learning:locale';
export function readLocale(storage){try{return storage.getItem(LOCALE_KEY)==='en'?'en':'vi';}catch{return 'vi';}}
export function writeLocale(storage,locale){if(!['vi','en'].includes(locale))throw new Error('Invalid locale');try{storage.setItem(LOCALE_KEY,locale);return null;}catch{return 'Language preference could not be saved.';}}
const entries=`
Lớp thực hành AI|AI Learning Studio
Người hướng dẫn|Facilitator
Khu làm việc|Workspace
Nhóm học|Learning group
Hoạt động học|Learning activity
Hoạt động|Activities
Buổi thực hành|Practice session
Thư viện dự án|Project library
Báo cáo|Reports
Hồ sơ thực hành|Practice record
Dữ liệu mẫu, lưu trên thiết bị|Synthetic data · stored on this device
Giới hạn thử nghiệm|Rehearsal limitations
Chỉ dùng dữ liệu mẫu|Use synthetic data only
Không nhập thông tin trẻ thật. Học liệu và rubric chưa duyệt sư phạm. Chưa có tài khoản, phân quyền hoặc provider AI thật; usage và cost chưa đo. Lưu trên thiết bị, chưa có backup server.|Do not enter real children's information. Lesson materials and rubrics have not received educational review. Accounts, access controls and live AI providers are not implemented; usage and costs are unmeasured. Data stays on this device without server backup.
Xuất backup|Export backup
Khôi phục|Restore
Xóa dữ liệu mẫu trên thiết bị?|Delete synthetic data from this device?
Xóa dữ liệu mẫu|Delete synthetic data
Tải backup trước khi xóa. Không thể khôi phục nếu không giữ file backup.|Export a backup before deleting. Recovery requires your saved backup file.
Khôi phục backup hợp lệ?|Restore this validated backup?
Backup thay thế dữ liệu mẫu hiện tại. Có thể tải backup hiện tại trước khi xác nhận.|The backup replaces the current synthetic data. Export the current data before confirming.
1. Mở backup trước|1. Open backup first
2. Xóa dữ liệu mẫu|2. Delete synthetic data
Mở backup hiện tại|Open current backup
Nội dung xuất|Export contents
Có thể sao chép nội dung hoặc yêu cầu trình duyệt tải file.|Copy the contents or request a file download.
Nội dung dữ liệu mẫu · chỉ đọc|Synthetic data contents · read only
Chọn toàn bộ|Select all
Sao chép nội dung|Copy contents
Yêu cầu tải file|Request download
Đóng|Close
Hủy|Cancel
Theo dõi từng bài làm và tiếp tục đồng hành ở bước người học đang thực hiện.|Follow each learner's work and resume support at their current step.
Hoạt động cho buổi mới|Activity for new sessions
Thêm học viên mẫu|Add synthetic learner
Học viên và buổi đang dở|Learners and unfinished sessions
Chọn một người học để tiếp tục|Choose a learner to resume
Mọi mã và trạng thái đồng ý đều là dữ liệu mẫu. Không nhập thông tin trẻ thật.|All learner identifiers and consent labels are synthetic. Do not enter real children's information.
Học liệu cho buổi thực hành|Session materials
Nháp, chưa duyệt sư phạm|Draft · educational review pending
Xem học liệu|View materials
Đang thực hành|In progress
Tạm dừng|Paused
Hoàn thành|Completed
Chưa đồng ý mẫu|Synthetic consent pending
Đã đồng ý mẫu|Synthetic consent recorded
Chưa có buổi đang dở|No unfinished session
Có thể bắt đầu hoạt động mẫu.|A sample activity can be started.
Tiếp tục buổi học|Resume session
Bắt đầu buổi mới|Start a new session
Bắt đầu buổi học|Start session
Dùng mã giả để thử luồng học. Không nhập tên hoặc liên hệ của trẻ thật.|Use a fictional identifier to rehearse the learning flow. Do not enter real children's names or contact details.
Đóng form thêm học viên|Close learner form
Mã học viên mẫu|Synthetic learner ID
Ví dụ: MAU-003|Example: DEMO-003
3–24 ký tự: chữ, số, gạch ngang hoặc gạch dưới. Mỗi mã dùng một lần.|3–24 characters: letters, digits, hyphens or underscores. Each identifier must be unique.
Nhóm tuổi giả định|Assumed age group
Thêm vào nhóm mẫu|Add to synthetic group
Tên thẻ nguồn|Reference card title
Nội dung nguồn / tình huống|Reference content / scenario
Bỏ thẻ này|Remove card
Tên hoạt động|Activity title
Mục tiêu quan sát|Observable learning objective
Thời lượng dự kiến, chưa đo (phút)|Estimated duration, unmeasured (minutes)
Hướng dẫn cho 8 bước học|Instructions for eight learning steps
Bài mới là nhiệm vụ độc lập. Không chèn đáp án hoặc yêu cầu AI/người hướng dẫn làm thay.|The transfer task is independent. Do not insert answers or ask AI or the facilitator to complete it for the learner.
Thẻ kiến thức và nguồn tham chiếu|Knowledge cards and references
Source ID tham chiếu (phân cách bằng dấu phẩy)|Reference source IDs (comma separated)
ID lưu để truy nguồn; không tự xác nhận nguồn đã duyệt cho bài.|IDs support traceability; they do not establish that a source is approved for this lesson.
Thêm thẻ nguồn|Add reference card
Phản hồi AI mẫu cho bài này|AI fixture response for this activity
Dữ liệu mẫu có lỗi có chủ đích để diễn tập. Chưa gọi provider AI thật.|The rehearsal fixture contains a deliberate error. No live AI provider is called.
Nội dung phản hồi mẫu|Fixture response contents
Rubric người hướng dẫn nhập|Facilitator-entered rubric
Tên tiêu chí:|Criterion title:
Mô tả điều quan sát|Description of observable evidence
Ghi chú người hướng dẫn và bài độc lập|Facilitator and independent-task notes
Ghi chú vận hành buổi học|Session operation notes
Ghi chú dành riêng cho người hướng dẫn về bài độc lập|Facilitator-only independent-task notes
Ghi chú này không hiển thị trong bước làm bài độc lập.|These notes are hidden during the independent task.
Tạo hoạt động mới|Create new activity
Hủy tạo mới|Cancel creation
Bản đã sửa trở lại nháp. Các phiên đang chạy giữ nguyên học liệu, phản hồi và rubric cũ.|Edits create a new draft. Existing sessions retain their pinned materials, response and rubric.
Đã ghi nhận sẵn sàng diễn tập|Readiness for adult rehearsal recorded
Cần sửa trước diễn tập|Revise before rehearsal
chưa duyệt dùng với trẻ|not approved for use with children
Nháp, chưa rà soát local|Draft · local review pending
Soạn một buổi học đầy đủ, lưu phiên bản và ghi nhận rà soát cho diễn tập người lớn.|Prepare a complete session, save a version and record a review for adult rehearsal.
Tạo hoạt động|Create activity
Chọn hoạt động trong kho local|Choose a local activity
Thư viện tài liệu dự án|Project document library
Đọc lại thư viện|Reload library
Hoạt động mới|New activity
Nội dung buổi học|Session contents
Biên soạn từ bản đang chọn; sửa đủ nội dung theo nhiệm vụ mới.|Draft from the selected version; adapt every field to the new task.
Nhiệm vụ đang chọn|Selected task
Bài ban đầu|Initial work
Ghi nhận rà soát local|Record local review
Chỉ cho diễn tập người lớn. Danh tính nhập ở máy này chưa xác thực; không phải phê duyệt dùng với trẻ.|Adult rehearsal only. Identities entered on this device are unverified; this is not approval for use with children.
Người rà soát (tự nhập)|Reviewer (self-reported)
Ý kiến có căn cứ|Review rationale and evidence
Quyết định diễn tập|Rehearsal decision
Chọn quyết định|Choose a decision
Sẵn sàng diễn tập người lớn|Ready for adult rehearsal
Ghi nhận rà soát|Record review
Các phiên bản của hoạt động|Activity version history
Rà soát local|Local review
Tạo lúc|Created
Tên|Title
Bản|Version
Thư viện dành cho người hướng dẫn. Có đáp án và ghi chú diễn tập; không đưa trọn bộ cho người học. Xem nguồn, sao chép hoặc lưu nội dung trên máy.|A facilitator library containing answer keys and rehearsal notes. Do not share the entire library with learners. Inspect references, copy or save documents locally.
Tìm tài liệu|Search documents
Tên, nội dung mô tả hoặc source ID|Title, description or source ID
Nhóm tài liệu|Document category
Tất cả|All
Đang đọc danh mục local…|Loading the local catalog…
Tài liệu dự án|Project documents
Không có tài liệu phù hợp. Thử từ khóa khác hoặc đọc lại danh mục.|No documents match. Try another search or reload the catalog.
Không gắn nguồn ngoài; tài liệu vận hành/nháp local|No external source attached; local draft / operating document
Sao chép / lưu tài liệu|Copy / save document
Mở file nguồn|Open source file
Đang đọc tài liệu…|Loading document…
Chọn tài liệu để đọc|Choose a document to read
Tài liệu nguồn và template giữ rõ nháp, hướng dẫn vận hành hoặc chỉ mục nghiên cứu. Không tự xác nhận curriculum đã được duyệt.|Documents retain their draft, operating-guide or research-index status. They do not establish educational approval.
Đánh giá model offline|Offline model evaluation
Bài đăng mẫu|Draft channel posts
Kênh trao đổi|Communication channels
Chương trình học|Curriculum
Hướng dẫn|Guides
Bộ dự án|Project kit
Nghiên cứu|Research
Biểu mẫu|Templates
Bản nháp|Draft
Hướng dẫn vận hành|Operating guide
Chỉ mục nguồn|Source index
Chọn phiên thực hành|Choose practice session
Để đối chiếu|References for checking
Học liệu nháp|Draft material
Học liệu mẫu · nháp chưa duyệt sư phạm · v|Sample material · educational review pending · v
AI mẫu · cố ý có lỗi|AI fixture · deliberate error
Phản hồi AI mẫu · cố ý có lỗi|AI fixture response · deliberate error
Mã / tên người đánh giá mẫu|Synthetic reviewer ID / name
VD: HUONG-DAN-MAU|Example: DEMO-FACILITATOR
Chưa đánh giá|Not rated
Chưa thể hiện|Not demonstrated
Cần hỗ trợ nhiều|Substantial support needed
Thể hiện một phần|Partially demonstrated
Thể hiện rõ|Clearly demonstrated
Ghi chú quan sát của người hướng dẫn|Facilitator observation note
Suy nghĩ ban đầu|Initial thinking
Xem phản hồi AI mẫu|Inspect the AI fixture
Chỉ ra điều cần kiểm|Identify a claim to check
Đối chiếu kiến thức|Check against references
Sửa kết luận|Revise the conclusion
Tự giải thích|Explain in your own words
Bài mới · không có AI|Transfer task · without AI
Người hướng dẫn đánh giá|Facilitator review
Chọn học viên để bắt đầu một vòng học có hướng dẫn.|Choose a learner to begin a guided learning cycle.
Chưa có phiên được chọn|No session selected
Chọn một học viên mẫu để bắt đầu vòng học. Không có provider thật hoặc dữ liệu người học thật.|Choose a synthetic learner to start. No live AI provider or real learner data is present.
Chọn học viên mẫu|Choose synthetic learner
Phiên mẫu đã hoàn thành. Đây là trạng thái vận hành, chưa phải bằng chứng hiệu quả giáo dục.|The synthetic session is complete. This is an operational status, not evidence of educational effectiveness.
Xem báo cáo|View report
Chế độ provider mẫu|Fixture provider mode
Phản hồi mẫu|Fixture response
Mô phỏng lỗi|Simulated error
Mô phỏng timeout|Simulated timeout
Đang mở mẫu…|Opening fixture…
Mở lại / thử lại|Reopen / retry
Mở phản hồi mẫu|Open fixture response
Phản hồi mẫu có lỗi có chủ đích theo hoạt động đang chọn. Phần mềm không gọi AI thật.|The selected activity's fixture contains a deliberate error. This application does not call live AI.
Bài làm của người học mẫu|Synthetic learner's work
Nhập bài làm mẫu tại đây…|Enter synthetic work here…
Lưu trên thiết bị sau mỗi thay đổi.|Saved on this device after every edit.
Bài độc lập, không có AI hoặc thẻ gợi ý.|Independent task, without AI or hint cards.
Câu trả lời do người học thực hiện.|The learner completes the response.
Khu vực bài độc lập: không hiển thị phản hồi AI, thẻ kiến thức hoặc đáp án.|Independent-task area: AI responses, reference cards and answer keys are hidden.
Buổi thực hành đã hoàn thành|Practice session completed
Tiếp tục phiên|Resume session
Đã hoàn thành 8 bước|All eight steps completed
Đã ghi nhận|Recorded
Bước hiện tại|Current step
Chưa thực hiện|Not yet completed
Bài làm đã ghi nhận|Recorded work
Ghi nhận của người hướng dẫn|Facilitator record
Nhiệm vụ ở bước này|Task at this step
Phiên đang tạm dừng. Bài làm được giữ; tiếp tục phiên để nhập hoặc chuyển bước.|This session is paused. Work is preserved; resume to edit or advance.
Đủ dữ liệu bắt buộc ở bước này.|Required information is present for this step.
Nhập dữ liệu bắt buộc để tiếp tục.|Enter the required information to continue.
Hoàn thành phiên|Complete session
Lưu và tiếp tục|Save and continue
Giữ lại cách người học đã suy nghĩ, kiểm chứng và tự làm. Nhận xét do người hướng dẫn ghi lại.|Preserve the learner's thinking, verification and independent work. Feedback is recorded by the facilitator.
Chưa có buổi thực hành để xem|No practice session to display
Chọn học viên mẫu và bắt đầu một phiên. Báo cáo sẽ giữ lại bài làm qua từng bước.|Choose a synthetic learner and start a session. Reports preserve work across steps.
Bài làm mẫu. Học liệu và rubric nháp, chưa duyệt sư phạm.|Synthetic work. Lesson materials and rubrics are drafts awaiting educational review.
Xuất báo cáo|Export report
Thông tin phiên và nguồn dữ liệu|Session details and data provenance
Mã phiên:|Session ID:
Bắt đầu:|Started:
Hoàn thành:|Completed:
Chưa hoàn thành|Not completed
Phản hồi AI:|AI response:
có lỗi mẫu theo bài.|includes the activity's deliberate fixture error.
Người đánh giá:|Reviewer:
Rà soát học liệu:|Material review:
chưa có người rà soát|No reviewer recorded
Chưa gắn|Not attached
Ý kiến rà soát:|Review notes:
Chưa có|Not recorded
Danh tính rà soát local chưa xác thực; không phải phê duyệt dùng với trẻ.|Local reviewer identities are unverified; this is not approval for use with children.
So sánh bài làm qua ba giai đoạn|Compare work across three stages
Tự làm trước khi xem AI|Independent work before seeing AI
Bài đã sửa|Revised work
Sau AI mẫu và thẻ kiến thức|After the AI fixture and reference cards
Bài độc lập|Independent work
Nhiệm vụ mới, không có AI|New task, without AI
Chưa có bài làm ở giai đoạn này.|No work recorded at this stage.
Nhận xét của người hướng dẫn|Facilitator feedback
Ghi chú quan sát|Observation notes
Chưa có ghi chú quan sát.|No observation notes recorded.
Cách đọc báo cáo|How to read this report
Bài ban đầu và bài độc lập giữ riêng với bài có hỗ trợ. Điểm rubric do người hướng dẫn nhập, chưa tự động đánh giá.|Initial and independent work are kept separate from supported work. Rubric scores are entered by the facilitator, not generated automatically.
Phiên hoàn thành hoặc phần mềm chạy đúng chưa chứng minh hiệu quả giáo dục.|A completed session or working software does not establish educational effectiveness.
Giới hạn của dữ liệu mẫu|Synthetic-data limitations
Không có dữ liệu người học thật hoặc pilot. Provider chưa tích hợp; usage, cost và chất lượng chưa đo. Chưa có phân quyền hoặc lưu trữ server.|No real learner or pilot data exists. A live provider is not integrated; usage, cost and quality are unmeasured. Access controls and server storage are not implemented.
Xem từng bước thực hành|Inspect each practice step
Lưu trữ cần xử lý|Storage needs attention
Thử đọc lại dữ liệu lưu|Retry reading saved data
Dùng và lưu bộ mẫu tạm hiện tại|Use and save the temporary synthetic dataset
Xuất dữ liệu đang có|Export current data
Backup JSON · dữ liệu mẫu|JSON backup · synthetic data
Nội dung đã sẵn sàng. Chưa xác nhận file được lưu trên máy.|Contents are ready. Saving the file on your device has not been confirmed.
Nội dung đã chọn. Dùng Ctrl+C hoặc Command+C rồi lưu thành file. Hãy giữ backup trước khi xóa.|Contents selected. Press Ctrl+C or Command+C and save a file. Keep the backup before deleting data.
Đang yêu cầu quyền sao chép…|Requesting clipboard access…
Đã sao chép nội dung. Hãy lưu thành file và giữ backup trước khi xóa.|Contents copied. Save a file and keep the backup before deleting data.
Trình duyệt chưa cho phép sao chép; nội dung đã chọn, dùng Ctrl+C hoặc Command+C và lưu file.|Clipboard access is unavailable. Contents are selected; press Ctrl+C or Command+C and save a file.
Đã yêu cầu tải file. Kiểm tra file đã lưu; nếu không có, sao chép nội dung ở trên.|Download requested. Check that the file was saved; otherwise copy the contents above.
Báo cáo text · dữ liệu mẫu|Text report · synthetic data
Tài liệu local|Local document
Đã thêm học viên mẫu.|Synthetic learner added.
Đã bắt đầu phiên với học liệu được giữ theo phiên bản.|Session started with a pinned material version.
Bỏ phần soạn chưa lưu để chọn hoạt động khác?|Discard unsaved edits and select another activity?
Lưu nội dung thành phiên bản nháp trước khi ghi nhận rà soát.|Save the draft version before recording a review.
Đã mở phản hồi AI mẫu. Hãy kiểm chứng nội dung.|AI fixture opened. Check its claims.
Backup đã mở để xem, sao chép hoặc yêu cầu tải file.|Backup opened for inspection, copying or download.
Đã khôi phục backup hợp lệ.|Validated backup restored.
Đã xóa dữ liệu lưu. Bộ mẫu khởi tạo mới đang ở bộ nhớ.|Saved data deleted. A fresh synthetic dataset is now in memory.
Không tìm thấy hoạt động.|Activity not found.
Mã học viên đã tồn tại.|Learner identifier already exists.
Nhóm tuổi không hợp lệ.|Invalid age group.
Mã cần 3–24 ký tự: A–Z, 0–9, gạch ngang hoặc gạch dưới.|Identifier must contain 3–24 characters: A–Z, digits, hyphens or underscores.
Backup vượt giới hạn 8 MB.|Backup exceeds the 8 MB limit.
Backup không phải JSON hợp lệ. Dữ liệu hiện tại được giữ nguyên.|Backup is not valid JSON. Current data is preserved.
Backup không hợp lệ hoặc không thuộc schema được hỗ trợ. Dữ liệu hiện tại được giữ nguyên.|Backup is invalid or uses an unsupported schema. Current data is preserved.
Tối đa 12 thẻ nguồn.|Maximum 12 reference cards.
Quan sát cần người ghi, mô tả, loại bằng chứng, hỗ trợ và thời gian 0–1440 phút.|Observation requires an observer, description, evidence type, support level and duration from 0 to 1440 minutes.
Readiness cần phiên bản; sẵn sàng diễn tập cần người chịu trách nhiệm và căn cứ.|A version is required. Adult-rehearsal readiness also requires an owner and supporting rationale.
Không tìm thấy phiên quan sát.|Observation session not found.
`;
export const COPY=Object.fromEntries(entries.trim().split('\n').map(line=>line.split('|')));
const ordered=Object.keys(COPY).sort((a,b)=>b.length-a.length);
export function translate(text,locale='vi'){if(locale!=='en')return String(text);let value=String(text);const slots=[];for(const key of ordered){value=value.split(key).join(`\uE000${slots.push(COPY[key])-1}\uE001`);}return value.replace(/\uE000(\d+)\uE001/g,(_,n)=>slots[Number(n)]);}
export function localizedCatalogItem(item,locale){if(locale==='en'&&item.translations?.en)return {...item,...item.translations.en,id:item.id,sourceIds:item.sourceIds,category:item.category,translationFallback:false};return {...item,translationFallback:locale==='en'};}
export const EN_STEPS=['Initial thinking','Inspect the AI fixture','Identify a claim to check','Check against references','Revise the conclusion','Explain in your own words','Transfer task · without AI','Facilitator review'];
Object.assign(COPY,{
 'Hình chữ nhật dài 8 cm, rộng 5 cm':'Rectangle: 8 cm long and 5 cm wide', 'Tạm dừng phiên':'Pause session', 'Bản làm việc để đọc và diễn tập':'Project review and rehearsal', 'Dự án':'Project', 'Lộ trình xem':'Guided review', 'Góp ý':'Feedback', 'Bỏ qua điều hướng, đến nội dung':'Skip navigation and go to content', 'Diễn tập':'Rehearsal', 'Platform local P03':'Local rehearsal · P03', 'Bản dịch tiếng Anh của học liệu không hợp lệ.':'Invalid authored English lesson translation.',
 'Bước ':'Step ', ' tuổi':' years', ' học viên mẫu':' synthetic learners', ' buổi đang dở':' unfinished sessions',' buổi hoàn thành':' completed sessions',
 ' tài liệu trong kết quả. Các bản đọc là bản sao của kho tài liệu nguồn; trạng thái nháp giữ rõ.':' matching documents. Previews are copies of the source library; draft status is retained.',
 'Lưu phiên bản ':'Save version ', 'phiên bản ':'version ', 'Thời lượng ':'Duration ', ' phút là đề xuất, chưa đo. Nội dung vẫn là nháp sư phạm.':' minutes is proposed and unmeasured. Content remains an educational draft.',
 'Học liệu v':'Material v','Rubric nháp cùng phiên bản ':'Draft rubric, version ',' bài làm mẫu':' synthetic work',
 'File:':'File:',
 'Mã/phiên bản hoạt động không hợp lệ.':'Invalid activity identifier or version.',
 'Nhập tên hoạt động và mục tiêu trong giới hạn.':'Enter an activity title and objective within the length limits.',
 'Không được tự gắn phê duyệt sư phạm.':'Educational approval cannot be assigned automatically.',
 'Chọn nhóm tuổi và thời lượng dự kiến 10–240 phút.':'Choose an age group and an estimated duration from 10 to 240 minutes.',
 'Source ID không hợp lệ hoặc trùng.':'Invalid or duplicate source ID.',
 'Cả 8 bước cần hướng dẫn, tối đa 4.000 ký tự mỗi bước.':'All eight steps require instructions of up to 4,000 characters per step.',
 'Cả 8 bước cần hướng dẫn. Thiếu hoặc vượt 4.000 ký tự ở bước: ':'All eight steps require instructions. Missing content or a 4,000-character limit exceeded at step: ',
 'Cần 1–12 thẻ nguồn với tên và nội dung.':'Provide 1–12 reference cards with titles and content.',
 'Nhập phản hồi AI mẫu và giữ nhãn mẫu có lỗi.':'Enter a fixture response and retain the deliberate-error label.',
 'Cần đủ 3 tiêu chí rubric có tên và mô tả.':'Provide all three rubric criteria with titles and descriptions.',
 'Ghi chú/thời điểm hoạt động không hợp lệ.':'Invalid activity notes or timestamp.',
 'Rà soát cần người, ý kiến, quyết định diễn tập và phạm vi local; không phải phê duyệt trẻ thật.':'A review requires a reviewer, notes, a rehearsal decision and local scope; it is not approval for use with children.',
 'Thư viện bài mẫu không đúng schema.':'Lesson library schema is invalid.',
 'Mã bài mẫu trùng.':'Duplicate sample lesson identifier.',
 'Không tìm thấy học viên mẫu.':'Synthetic learner not found.',
 'Phiên đang tạm dừng hoặc đã hoàn thành.':'Session is paused or completed.',
 'Trường bài làm không hợp lệ.':'Invalid learner-work field.',
 'Bài làm cần là văn bản dưới 10.000 ký tự.':'Learner work must be text of up to 10,000 characters.',
 'Phiên đã hoàn thành.':'Session is completed.',
 'Chỉ mở phản hồi tại bước AI của phiên đang hoạt động.':'Open a response only at the AI step of an active session.',
 'Phản hồi mẫu không hợp lệ.':'Invalid fixture response.',
 'Phiên đang tạm dừng.':'Session is paused.',
 'Hoàn thành dữ liệu bắt buộc ở bước này trước khi tiếp tục.':'Complete the required information at this step before continuing.',
 'Không đọc được dữ liệu lưu: ':'Unable to read saved data: ',
 '. Đang dùng bộ mẫu tạm trong bộ nhớ; chưa ghi đè dữ liệu cũ.':'. A temporary synthetic dataset is in memory; existing saved data has not been overwritten.',
 'Không lưu được trên trình duyệt: ':'Unable to save in the browser: ',
 '. Bài làm vẫn ở bộ nhớ; hãy xuất backup trước khi đóng trang.':'. Work remains in memory; export a backup before closing the page.',
 'Danh mục thư viện không hợp lệ.':'Invalid library catalog.',
 'Chưa đọc được danh mục tài liệu. Chạy compiler thư viện rồi tải lại.':'Unable to load the document catalog. Build the library resources and reload.',
 'Không đọc được tài liệu; giữ nguyên dữ liệu hiện tại.':'Unable to read the document; current data is preserved.',
 'Tài liệu vượt giới hạn preview 500 KB.':'Document exceeds the 500 KB preview limit.',
 'Chế độ provider mẫu không hợp lệ.':'Invalid fixture provider mode.',
 'Mô phỏng timeout: provider mẫu chưa phản hồi. Có thể thử lại; bài làm được giữ nguyên.':'Simulated timeout: the fixture provider has not responded. Retry is available; learner work is preserved.',
 'Mô phỏng lỗi provider. Có thể thử lại; bài làm được giữ nguyên.':'Simulated provider error. Retry is available; learner work is preserved.',
 'Hoạt động thiếu phản hồi mẫu.':'Activity has no fixture response.',
 'Quyền lưu trữ bị chặn.':'Storage permission is blocked.',
 'Đã đọc lại dữ liệu lưu.':'Saved data reloaded.',
 'Đã lưu bộ mẫu tạm.':'Temporary synthetic dataset saved.',
 'Đọc lại bản đã lưu có thể thay bài làm chưa lưu trong bộ nhớ. Hãy xuất backup trước. Tiếp tục?':'Reloading saved data may replace unsaved work in memory. Export a backup first. Continue?',
 'Ghi bộ mẫu tạm hiện tại thay dữ liệu lưu không đọc được? Hãy giữ backup trước khi tiếp tục.':'Replace unreadable saved data with the current temporary synthetic dataset? Keep a backup before continuing.',
 'Đã lưu rà soát diễn tập local trong phiên bản mới; danh tính chưa xác thực, chưa duyệt dùng với trẻ.':'Local rehearsal review saved in a new version; identity is unverified and use with children is not approved.',
 'Phiên mẫu đã hoàn thành. Xem báo cáo để kiểm tra bằng chứng.':'Synthetic session completed. Inspect the report to review the evidence.',
 'Đã chuyển sang bước ':'Advanced to step ', 'Đã lưu ':'Saved ', '; bản này là nháp.':'; this version is a draft.',
 'Chưa đọc được bài mẫu. Chạy compiler thư viện rồi đọc lại.':'Unable to load sample lessons. Build library resources and reload.'
});
// Include supplemental interface copy in the same deterministic lookup.
ordered.splice(0,ordered.length,...Object.keys(COPY).sort((a,b)=>b.length-a.length));
