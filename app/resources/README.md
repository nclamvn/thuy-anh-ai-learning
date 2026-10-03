# Bộ dự án trên máy · bắt đầu ở đây

Trạng thái: Bản nháp AI và hướng dẫn vận hành local. Ngày soạn: 03/10/2026. Học liệu chưa duyệt sư phạm; mọi vai/bài làm/tình huống DEMO là giả. Không có nhóm trao đổi hoặc lời mời được gửi từ bộ này.

## Chọn đường làm việc

- **Làm rõ dự án:** đọc [brief](project-brief.md), ghi điều chưa biết và phân công phần [cần người thật](guides/human-handoff.md).
- **Diễn tập một buổi:** chọn [một bài nháp](curriculum/README.md), dùng [kế hoạch buổi](templates/session-plan.md) và [hướng dẫn 45 phút](guides/facilitator-rehearsal.md). Không phát gói người hướng dẫn chứa đáp án cho người học.
- **Soạn và review:** sử dụng lessons.json, phiếu [rà soát](templates/curriculum-review.md), rồi tạo phiên bản mới; chưa tự công nhận review là phê duyệt sư phạm.
- **Ghi và quyết định:** giữ [quan sát](templates/observer-sheet.md), [evidence](templates/evidence-capture.md), [issue](templates/issue-risk-log.md) và [decision](templates/decision-record.md) tách loại.
- **Vận hành:** đọc [quickstart](guides/operator-quickstart.md), [backup](guides/backup-and-recovery.md), [release local](guides/release-checklist.md).
- **Truy nguồn và benchmark:** đọc [source index](research/source-index.md) và [scoring guide](benchmark/scoring-guide.md). Đo model thật chưa thực hiện; các trường đo để null đến khi có quan sát.

## Danh mục tài liệu

### Dự án

- [Brief dự án · điều đã biết và điều cần quyết định](project-brief.md) · draft.

### Học liệu và phiếu tách riêng

- [Bộ học liệu nháp · ba cách tự kiểm](curriculum/README.md) · draft.
- [Đo lại điều AI nói](curriculum/lesson-01.md) · draft.
- [Đọc đúng lời hẹn](curriculum/lesson-02.md) · draft.
- [Một câu hỏi có thể thử được](curriculum/lesson-03.md) · draft.
- [Phiếu người học · Đo lại điều AI nói](curriculum/handout-01.md) · draft.
- [Bài độc lập riêng · Đo lại điều AI nói](curriculum/transfer-01.md) · draft.
- [Phiếu người học · Đọc đúng lời hẹn](curriculum/handout-02.md) · draft.
- [Bài độc lập riêng · Đọc đúng lời hẹn](curriculum/transfer-02.md) · draft.
- [Phiếu người học · Một câu hỏi có thể thử được](curriculum/handout-03.md) · draft.
- [Bài độc lập riêng · Một câu hỏi có thể thử được](curriculum/transfer-03.md) · draft.

### Hướng dẫn

- [Diễn tập 45 phút · người hướng dẫn](guides/facilitator-rehearsal.md) · operating-guide.
- [Vận hành platform local](guides/operator-quickstart.md) · operating-guide.
- [Lưu thủ công và phục hồi](guides/backup-and-recovery.md) · operating-guide.
- [Bản phát hành local · ghi bằng chứng](guides/release-checklist.md) · operating-guide.
- [Bàn giao con người · quan hệ, quan sát, trách nhiệm](guides/human-handoff.md) · operating-guide.

### Template điền được

- [Phiếu quan sát · điều thực sự xảy ra](templates/observer-sheet.md) · draft.
- [Phiếu bài làm · tám bước](templates/learner-worksheet.md) · draft.
- [Phỏng vấn nhu cầu · tránh dẫn dắt](templates/interview-guide.md) · draft.
- [Ghi bằng chứng · tách nguồn và diễn giải](templates/evidence-capture.md) · draft.
- [Rà soát học liệu · quyết định có phạm vi](templates/curriculum-review.md) · draft.
- [Kế hoạch một buổi · chuẩn bị và dừng](templates/session-plan.md) · draft.
- [Lịch nhóm thử · chưa có người được tuyển](templates/cohort-schedule.md) · draft.
- [Lỗi và rủi ro · sự kiện khác khả năng](templates/issue-risk-log.md) · draft.
- [Bản ghi quyết định · ai chọn và vì sao](templates/decision-record.md) · draft.
- [Tổng hợp tuần · đủ bằng chứng mới kết luận](templates/weekly-synthesis.md) · draft.

### Kiến trúc kênh mẫu

- [Kênh trao đổi · cấu trúc đề xuất](channels/architecture.md) · draft.

### Năm bài đăng nháp

- [Tin nháp · điều phối nội bộ](channels/posts/internal-coordination.md) · draft.
- [Tin nháp · chào phụ huynh](channels/posts/parent-welcome.md) · draft.
- [Tin nháp · mời người lớn diễn tập](channels/posts/rehearsal-invitation.md) · draft.
- [Tin nháp · ghi chú tiến độ tuần](channels/posts/weekly-note.md) · draft.
- [FAQ nháp · nói rõ giới hạn](channels/posts/faq.md) · draft.

### Nguồn

- [Chỉ mục nguồn · provenance và giới hạn](research/source-index.md) · source-index.

### Benchmark

- [Benchmark offline · chuẩn bị phép so sánh](benchmark/scoring-guide.md) · draft.

## Dữ liệu máy đọc và bản sinh

[lessons.json](curriculum/lessons.json) là ba bài mẫu theo contract của platform, không chứa điểm hoặc reviewer đã được bịa. `catalog.json` là allowlist tài liệu nguồn; compiler trong workspace sinh bản đọc ở `app/resources/`. Không sửa bản sinh thay bản nguồn. Danh mục có fingerprint để kiểm bản đọc đúng nội dung đã tạo.

Các link trong bộ tài liệu trỏ nội bộ materials hoặc nguồn công khai; tên file ngoài materials chỉ là provenance để mở từ workspace. Không đưa QA backup, hội thoại riêng hoặc dữ liệu gia đình vào catalog.

## Cách dùng template thật

Sao chép bản mẫu, giữ trạng thái nháp đến khi người phụ trách xem lại, thay ví dụ giả bằng nội dung thực sự có. Ô chưa có bằng chứng ghi chưa biết. Người soạn phải xin đúng phạm vi dùng dữ liệu; không điền một người thật như đã nhận vai trò hoặc đã đồng ý. AI không tự gửi bài đăng, tuyển người, quyết định giáo dục hay xác nhận quyền xem dữ liệu.

## Nghiên cứu R01 · từ câu hỏi tới bằng chứng

Bổ sung sáu tài liệu nháp; toàn kho R01 có 41 tài liệu trước M01. Bắt đầu ở [18 câu hỏi](research/research-map.md), xem [khoảng trống](research/evidence-gap-register.md), [protocol](research/selection-protocol.md), [đối chiếu](research/evidence-synthesis-R01.md), [hồ sơ nguồn](research/evidence-cards-R01.md) và [kế hoạch dữ liệu](research/data-plan.md). Chưa có responses khảo sát, quan sát trẻ hoặc appraisal đầy đủ nguồn mới.

## Đánh giá và hoàn thiện M01

Tại M01 kho có 43 tài liệu. Đọc [đánh giá mức trưởng thành](project/maturity-assessment-M01.md) và [kế hoạch hoàn thiện](project/completion-roadmap-M01.md). Đây là đề xuất có căn cứ workspace, chưa là phê duyệt dùng với trẻ hoặc lịch/ngân sách đã cam kết.

## Hoàn thiện P03 · song ngữ và rehearsal workbench

Kho hiện có 54 tài liệu với bản tiếng Anh đầy đủ trong `en/`; ba bài seed có nội dung VI/EN được soạn tương ứng. Toggle đổi giao diện/tài liệu, không tự dịch tên hoặc câu trả lời người dùng. P03 chưa có review giáo dục, đồng ý hoặc kết quả trẻ thật.

- [Product contract · chọn một vấn đề đầu tiên](project/product-contract-P03.md) · draft.
- [LES-02 · bản đồ lý do thiết kế](curriculum/anchor-design-P03.md) · draft.
- [LES-02 · bộ đo độc lập và trì hoãn nháp](curriculum/anchor-assessment-P03.md) · draft.
- [Reviewer pack · chấm độc lập và giữ bất đồng](curriculum/review-calibration-P03.md) · draft.
- [P03 · diễn tập độc lập có bằng chứng](guides/adult-rehearsal-P03.md) · draft.
- [Người tham gia và dữ liệu · hồ sơ trách nhiệm nháp](guides/participant-data-P03.md) · draft.
- [Surface và lưu trữ · chọn theo cách sử dụng](guides/access-storage-P03.md) · draft.
- [AI provider · phép đo và gate trước live](benchmark/provider-protocol-P03.md) · draft.
- [Vận hành P03 · incident, release và bàn giao](guides/operations-release-P03.md) · draft.
- [Workbench P03 · quyết định và quan sát](guides/workbench-P03.md) · draft.
- [Appraisal phương pháp P03 · phạm vi đọc và giới hạn](research/full-methods-P03.md) · draft.
