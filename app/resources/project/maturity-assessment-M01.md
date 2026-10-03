# Đánh giá mức trưởng thành · M01

Ngày 03/10/2026. Người yêu cầu/owner: Nguyễn Cảnh Lâm. Người đánh giá: AI. Đây là đánh giá dựa trên workspace và bằng chứng local, chưa có hội đồng giáo dục, kiểm thử người dùng độc lập hoặc chứng nhận bên ngoài. [Kế hoạch tiếp theo](completion-roadmap-M01.md).

## Kết luận

Sản phẩm hiện là **prototype vận hành local đã được kiểm kỹ, có bộ chuẩn bị diễn tập người lớn**. Độ nghiêm túc thể hiện ở khả năng truy nguồn, phiên bản học liệu, bảo vệ bài làm khi lỗi và cách giữ điều chưa biết. Mức trưởng thành toàn sản phẩm còn ở trước pilot với trẻ: chưa xác nhận nhu cầu, chưa review sư phạm, chưa có dữ liệu vận hành thực tế được cung cấp, AI đang là phản hồi mẫu.

Hình thức đã có hướng riêng được owner chấp nhận. Giá trị đối với người học và tính tự vận hành của người hướng dẫn khác cần được quan sát. Không suy tỷ lệ hoàn thành toàn sản phẩm từ số màn hình, tài liệu hoặc tests PASS. Phạm vi P02/R01 đã nghiệm thu chỉ là các phạm vi local đã định nghĩa.

## Cách xếp mức

Thang riêng cho đánh giá này, không là TRL hoặc tiêu chuẩn chứng nhận: **0** chưa có bằng chứng trong workspace; **1** đã có bản nháp/thiết kế; **2** đã triển khai và kiểm bằng dữ liệu giả; **3** đã quan sát với đúng người và bối cảnh mục tiêu trong phạm vi xác định; **4** đã vận hành lặp lại và có bằng chứng chất lượng, phục hồi, trách nhiệm. Không lấy trung bình các chiều vì một điều kiện tham gia còn thiếu có thể chặn toàn bộ pilot.

| Chiều | Mức hiện tại | Bằng chứng | Điều còn thiếu để tiến lên |
| --- | --- | --- | --- |
| Nhu cầu, phân khúc và giá trị | 0 · chưa xác nhận | Brief U01/U02, RQ01–03; chưa có responses được cung cấp | Một vấn đề ưu tiên, trải nghiệm gần nhất của gia đình, người quyết định, lựa chọn thay thế |
| Giao diện và luồng công việc | 2 · kiểm local | Năm view; hướng UI03 được owner chấp nhận; bằng chứng responsive và kiểm luồng P02 | Quan sát người hướng dẫn mới; khả năng tìm tài liệu và phục hồi; kiểm tiếp cận đầy đủ |
| Kỹ thuật và tính toàn vẹn dữ liệu | 2 · kiểm local | Migration, snapshot phiên, validation, backup/import, escape nguồn; 36 Node tests chạy lại PASS | Kiểm trình duyệt/thiết bị mục tiêu, kiểm luồng tự động trên browser, reproducible release và restore drill độc lập |
| SOT và quản trị bằng chứng | 2 · có máy kiểm | 19 file canonical khớp; 0 lỗi A3; 11 captures/22 claims; registry dẫn xuất | Chủ thể có quyền review, trách nhiệm cập nhật và cách xử lý bằng chứng mới được vận hành thực tế |
| Nghiên cứu và chọn phương pháp | 1 · intake có provenance | R01 map 18 câu hỏi; bốn nguồn bổ sung, phần lớn mới abstract/metadata | Đọc full methods/appendix, đối chiếu điều kiện, nguồn tiếng Việt và lý do chọn can thiệp |
| Curriculum và đo học tập | 1 · nháp | Ba bài, bài độc lập riêng, rubric và phiếu review | Người có chuyên môn review theo version; độ khó/khả năng hiểu; chấm độc lập, retention/transfer |
| AI và chất lượng phản hồi | 1 · hợp đồng mô phỏng | requestSample chỉ fixture; 16 cases chưa thẩm định; observedResponses=0 | Chốt có cần AI live ở phiên bản đầu không; nếu cần, benchmark thật trên task set được duyệt và giới hạn trợ giúp |
| Quyền, an toàn và dữ liệu người học | 1 · có hướng dẫn | human-handoff, template và nhãn dữ liệu mẫu | Người chịu trách nhiệm; điều kiện tham gia/dừng, data flow, quyền truy cập/lưu/xóa và review yêu cầu áp dụng |
| Khả năng vận hành và bàn giao | 1 · có kit | Launcher, hướng dẫn, backup; ZIP P02 lịch sử | Người khác cài/chạy/đọc bài/xuất/khôi phục mà không cần tác giả; thời gian hỗ trợ và lỗi thật |
| Giá trị kinh tế và mở rộng | 0 · chưa xác nhận | Chi phí, nhu cầu trả tiền và latency đều chưa đo | Công người hướng dẫn, cost thực nếu gọi model, giá trị bổ sung, khả năng hỗ trợ và quyết định hình thức cung cấp |

Các mức 0 là thiếu bằng chứng trong dự án hiện có, không khẳng định việc ngoài máy chưa từng xảy ra. Mức 2 không tương đương production-ready.

## Phát hiện ảnh hưởng đến kế hoạch

| ID | Phát hiện | Bằng chứng cụ thể | Hệ quả / ưu tiên |
| --- | --- | --- | --- |
| F01 | Chưa chốt khách hàng và vấn đề đầu tiên | brief U01–U03, RQ01–04 | P0 chiến lược: tránh mở rộng platform cho một bài toán chưa được chọn |
| F02 | AI chưa hoạt động như dịch vụ thật | app/provider.js trả sampleResponse, không network | P1 có điều kiện: cần AI live mới benchmark/integrate; AI literacy với ví dụ được biên soạn vẫn là hướng khả thi |
| F03 | Curriculum/rubric chưa có review sư phạm được cung cấp | Seed review=null; tài liệu giữ nháp | P0 trước trẻ: freeze một bài được review, không mặc định toàn bộ ba bài đã phù hợp |
| F04 | Chưa có kết quả vận hành độc lập | Kit và QA là dữ liệu giả, chưa ghi buổi người hướng dẫn mới | P0 trước mở pilot: quan sát rehearsal, lỗi và công sức thay vì đánh giá bằng vẻ hoàn chỉnh |
| F05 | Tách hỗ trợ/bài độc lập hiện phụ thuộc người hướng dẫn | Step transfer ẩn trợ giúp trong view; thư viện có đáp án, không role/auth | P0 nếu người học tự cầm thiết bị: thiết kế surface/điều kiện truy cập; ẩn UI không là phân quyền |
| F06 | Trạng thái review/đồng ý không là enforcement cho trẻ | startSession chỉ kiểm mã có trong mẫu; reviewer là người tự nhập | Đúng phạm vi demo, P0 khi đổi sang trẻ: cần trạng thái/ủy quyền có trách nhiệm; không dùng consent mẫu như consent thật |
| F07 | Lưu trữ phù hợp demo một thiết bị | localStorage + backup JSON, lỗi lưu giữ RAM, không backup server | P0 trước dữ liệu thật: chọn mô hình lưu/truy cập/giữ/xóa theo bối cảnh; không tự ép cloud hoặc giữ nguyên vì tiện |
| F08 | Chất lượng phần mềm đã kiểm nhưng chưa đủ bảo đảm toàn hệ thống | 36 Node + 35 Python PASS; tests chủ yếu model/renderer/tools; browser QA lịch sử | P1: test tích hợp browser/cross-device và accessibility; tests không đo hiệu quả học tập |
| F09 | Nghiên cứu mới chưa là thẩm định phương pháp đầy đủ | R01 cards/gaps, 2 nguồn mới chưa capture; 3 nguồn mới abstract/metadata | P0 chọn cách dạy: intake thêm nguồn không đóng khoảng trống hiệu quả |
| F10 | Bàn giao chưa đồng bộ tất cả revision | app README còn ghi 35 trước M01; ZIP P02 không chứa R01 | P1 release: README được đồng bộ trong M01; tạo gói mới và clean-start sau revision triển khai tiếp |
| F11 | Nợ khả năng bảo trì bắt đầu xuất hiện | main.js ghép render/event cho nhiều view, nhiều dòng dài; chưa thấy CI config trong project | P1 theo đổi tiếp: tách điểm khó khi có chức năng mới, thêm repeatable checks; không đổi framework chỉ vì trưởng thành |
| F12 | Source IDs trong bài là tham chiếu, không chứng minh bài hiệu quả | Ba bài ghi provenance synthetic-curriculum-drafts | P0 nội dung: gắn mục tiêu/bước học/rubric với lý do thiết kế và reviewer, không dùng số lượng citations như thước đo sư phạm |

F05–F07 là khoảng cách khi mở phạm vi, không là cáo buộc lỗi an ninh trong demo localhost. Chưa thực hiện pentest, audit pháp lý hoặc kiểm WCAG toàn diện.

## Bằng chứng kiểm lại ngày 03/10/2026

- Node: 36/36 tests PASS. Python tools: 35/35 PASS. Tests này kiểm phần mềm bằng dữ liệu giả.
- Kit: 41 tài liệu trước khi thêm hai tài liệu M01, 3 bài, 45 file sinh; 142 liên kết nguồn và 142 liên kết sinh đạt. Số sau cập nhật M01 nằm trong VERIFY-M01.json, không ghi đè nghiệm thu R01.
- Research verifier: 14 manifest rows, 22 claims, 0 lỗi. Có 11 captures hợp lệ, 3 unavailable toàn kho; 2 unavailable mới ở R01.
- Benchmark template: 16 records pending, 0 observed responses, latency/cost/quality verdict null. Đây là kiểm cấu trúc, không kết quả chất lượng.
- SOT check: 19 canonical fingerprints khớp, 0 A3. Không đổi canonical hoặc nâng proposal thành quyết định trong đánh giá này.
- UI03/P02/R01 có ảnh và báo cáo lịch sử. M01 không chạy lại toàn bộ luồng học browser hoặc kiểm tất cả breakpoint; không viện dẫn lịch sử như phép đo mới.

## Điều kiện để gọi là trưởng thành hơn

**Rehearsal được xác nhận:** người hướng dẫn khác vận hành một bài tới báo cáo và khôi phục; quan sát khó khăn, mọi trợ giúp và thời gian thật; xử lý lỗi chặn luồng. Đây chưa là hiệu quả ở trẻ.

**Pilot có trách nhiệm:** bài/version và mục tiêu được người có chuyên môn review; người phụ trách chốt điều kiện tham gia/dừng/dữ liệu; surface và lưu trữ đúng mô hình dùng; có protocol quan sát và tiêu chí tiếp/sửa/dừng trước khi thu dữ liệu. Không dùng kết quả mô phỏng để vượt điều kiện này.

**Beta lặp lại:** người vận hành mục tiêu dùng được qua nhiều phiên, dữ liệu có thể phục hồi, trách nhiệm hỗ trợ rõ, có kết quả usability/cost và giới hạn kết luận học tập. Cỡ mẫu/đối chứng đánh giá hiệu quả cần thiết kế riêng, không được suy ra từ số người rehearsal.

**Production:** chỉ sau khi hình thức cung cấp đã chọn; kiểm vận hành, an toàn, truy cập, phục hồi, release và hỗ trợ phù hợp hình thức đó. Nhiều người dùng trên mạng cần kiến trúc khác demo một thiết bị. M01 chưa đưa ra quyết định cloud/provider/stack.

## Căn cứ ngoài dự án cho kế hoạch kiểm

[UNICEF Guidance on AI and Children 3.0](https://www.unicef.org/innocenti/reports/policy-guidance-ai-children) là nguồn định hướng về quyền trẻ em và AI; dùng để dựng câu hỏi review và trách nhiệm, không là xác nhận dự án đã đáp ứng. [WCAG 2.2 của W3C](https://www.w3.org/TR/WCAG22/) cung cấp các tiêu chí khả năng tiếp cận có thể kiểm. Đề xuất kiểm theo mục tiêu AA gồm keyboard/focus, nhãn và lỗi, reflow/zoom, target size, status và luồng đầy đủ; chưa tuyên bố đạt WCAG.

Ưu tiên của tổng công trình sư lúc này: nối vấn đề gia đình → mục tiêu học → bài và mức trợ giúp → bằng chứng quan sát → quyết định sản phẩm. UI03 và nền local có thể được giữ để phục vụ vòng học hỏi đó.
