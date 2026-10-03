# Kế hoạch hoàn thiện theo điều kiện nghiệm thu · M01

Ngày 03/10/2026. Owner: Nguyễn Cảnh Lâm. Đề xuất AI từ [đánh giá mức trưởng thành](maturity-assessment-M01.md); chưa là lịch cam kết, ngân sách, phân công Thuý Anh/chuyên gia hoặc quyết định kiến trúc đã được các bên đồng ý. Đã làm M01: đánh giá, kiểm lại và lập kế hoạch. Các hạng mục P03/P04 dưới đây chưa triển khai.

## Đích đợt tiếp theo

P03 đề xuất: **một bài, một mục tiêu, một phiên bản; người hướng dẫn khác tự diễn tập bằng dữ liệu giả và đem về bằng chứng có thể hành động**. Chuẩn bị điều kiện pilot với trẻ là đường song song có người chịu trách nhiệm. Giữ hướng UI03, tám bước, snapshot và SOT đã có; thay đổi vì vấn đề quan sát được.

Giả định để soạn kế hoạch: công cụ hỗ trợ người hướng dẫn tổ chức học cách kiểm chứng AI. Nếu Thuý Anh xác định sản phẩm là khóa học phụ huynh, lớp học AI hay tutor trực tiếp, phải sửa product contract trước xây chức năng phụ thuộc. Không mở mọi hướng cùng lúc.

## NOW · chuẩn bị và xác nhận rehearsal

| ID | Đầu ra | Việc trên máy / phần người thật | Phụ thuộc | Điều kiện hoàn tất |
| --- | --- | --- | --- | --- |
| P03-01 | Product contract một trang | AI soạn các lựa chọn từ brief/RQ; Lâm và Thuý Anh thống nhất vấn đề, nhóm đầu tiên, ai dùng/ai hưởng lợi, một mục tiêu, hình thức và phạm vi | RQ01–04; dữ liệu nhu cầu được phép dùng | Decision record có người quyết, lý do, bằng chứng và giả định; không biến lời khen thành nhu cầu |
| P03-02 | Thẩm định nguồn và bảng lý do thiết kế | AI đọc full methods/appendix, lấy official captures còn thiếu, tách effect/context/limits; người có chuyên môn chọn mức áp dụng | Không cần chờ P03-01 để đọc; chọn can thiệp phụ thuộc 01 | Mỗi nguồn có capture level và appraisal; mỗi khuyến nghị có evidence/limits; không suy hiệu quả Việt Nam |
| P03-03 | Một gói bài/version đủ để review | AI tạo bản đồ mục tiêu → bước → đáp án mẫu → rubric → bài độc lập; người làm giáo dục review ngôn ngữ/độ khó/trợ giúp | 01 và phần phù hợp của 02 | Nhận xét có phạm vi/version/người review; vấn đề nghiêm trọng được sửa; chưa có reviewer thì giữ nháp |
| P03-04 | Phép ghi quan sát tối thiểu | AI chuẩn bị schema/template: loại dữ liệu, bài/version, mốc thời gian, mức trợ giúp, sự kiện/error, thiếu dữ liệu, nhận xét tách diễn giải; mới triển khai tích hợp sau TIP | Mục tiêu 01; không cần provider thật | Có thể ghi dữ liệu giả và xuất đọc lại không mất trường; không tự tính learning gain hoặc điểm thay con người |
| P03-05 | Rehearsal bởi người hướng dẫn khác | AI chuẩn bị kit/tình huống lỗi; người phụ trách mời người lớn, quan sát, ghi thao tác/trợ giúp/thời gian và debrief | 03/04, vận hành local có sẵn | Người hướng dẫn vận hành từ mở bài đến report/backup/restore; có bằng chứng mọi lỗi chặn được xử lý; không coi tác giả thao tác hộ là hoàn tất |
| P03-06 | Hoàn thiện usability và tiếp cận | AI sửa theo quan sát sau TIP, kiểm keyboard/focus/dialog/errors, zoom/reflow, thiết bị mục tiêu; người dùng thử lại | Có thể chuẩn bị phép kiểm ngay; ưu tiên sửa từ 05 | Luồng chính không có lỗi chặn đã biết; checklist có bằng chứng/pass/fail và phần chưa kiểm; không tự tuyên bố WCAG chỉ từ contrast sampler |
| P03-07 | Release rehearsal tái lập | AI đồng bộ README/resource fingerprints, automated checks, gói bàn giao mới và clean-start/restore drill | Sau revision 03/04/06 | Gói gắn revision rõ, checksum/manifest đúng, không dữ liệu riêng/QA; người khác chạy được từ hướng dẫn; ZIP P02 vẫn là lịch sử |

P03-02 và chuẩn bị P03-04/06 có thể tiến hành khi trao đổi con người ở P03-01 đang diễn ra. Kết quả rehearsal có thể buộc quay lại 01/03; không lấy lịch dự kiến làm kết quả. Phần mềm thay đổi sẽ đi blueprint/TIP → Builder → Completion → Contractor verify theo Vibecode; kế hoạch này chưa là giấy phép mở dịch vụ công khai hoặc mua API.

## NEXT · mở phạm vi sau khi có bằng chứng

| ID | Đầu ra | Trách nhiệm đề xuất | Điều kiện bắt đầu / hoàn tất |
| --- | --- | --- | --- |
| P04-01 | Protocol pilot và mô hình dữ liệu/trách nhiệm | Lâm/Thuý Anh + người làm giáo dục/người phụ trách; AI soạn data flow và phương án | Bài/version được review; chốt điều kiện tham gia/dừng, phạm vi dữ liệu, truy cập/giữ/xóa, xử lý tình huống và yêu cầu áp dụng; có người nhận trách nhiệm |
| P04-02 | Surface người học và lưu trữ đúng bối cảnh | AI thiết kế lựa chọn; owner chọn; Builder triển khai theo TIP | Phụ thuộc 04-01 và hình thức dùng: instructor điều phối khác learner tự dùng; không lộ đáp án, không coi giấu nút là phân quyền; restore và truy cập/xóa được kiểm trong đúng phạm vi |
| P04-03 | AI thật có giới hạn, nếu product contract yêu cầu | Owner chốt ngân sách/provider access; AI chuẩn bị task set/runner/spec; người có chuyên môn review | Chỉ chạy khi được phép và có task set/context/config; log phản hồi/lỗi/retry/cost/latency/model version; không đạt hành vi cần thiết thì giữ fixture/nguồn biên soạn hoặc sửa thiết kế |
| P04-04 | Pilot, tổng hợp và quyết định tiếp/sửa/dừng | Người phụ trách tổ chức/quan sát; AI tổng hợp dữ liệu được phép | Đủ 04-01/02, và 03 nếu dùng live; lưu hỗ trợ/không tham gia/dữ liệu thiếu; báo cáo tách usability, học tập và chi phí; tiêu chí quyết định có trước thử |

P04-03 không bắt buộc cho một sản phẩm giáo dục AI dùng ví dụ có kiểm soát. Chưa lựa chọn model/stack production. Pilot có thể đánh giá tính khả thi; muốn kết luận hiệu quả cần thiết kế đối chứng, bài đo phù hợp và cỡ mẫu do người có chuyên môn xây dựng.

## LATER · beta và sản phẩm có thể vận hành lặp lại

Sau khi dữ liệu pilot trả lời vấn đề ưu tiên: hoàn thiện công cụ người hướng dẫn, onboarding/hỗ trợ, vận hành qua nhiều phiên, cost/capacity và release/incident/restore. Nếu chọn dịch vụ đa người dùng: auth/roles, server-side authorization, lưu trữ và audit có kiểm, quản lý phiên bản/model, giám sát và vận hành dữ liệu theo phạm vi được chọn. Nếu chọn kit/lớp có người hướng dẫn: ưu tiên chất lượng giáo viên, học liệu, lịch vận hành và bàn giao; không xây SaaS theo quán tính.

Thanh toán, gamification, social/community, kho bài rất rộng, chatbot mở và automation tự chấm được xếp sau khi có nhu cầu và thiết kế phù hợp. Chưa có bằng chứng để ưu tiên chúng trước P03.

## Điều kiện dừng và chuyển pha

| Mốc | Tiếp tục khi | Sửa hoặc giữ phạm vi khi |
| --- | --- | --- |
| Sau product contract | Vấn đề/nhóm/mục tiêu và trách nhiệm rõ | Các bên chọn những sản phẩm khác nhau hoặc dữ liệu nhu cầu còn thiếu |
| Sau rehearsal | Người hướng dẫn khác vận hành được, dữ liệu/bài làm phục hồi được, vấn đề chặn có cách xử lý | Tác giả phải làm hộ, mất dữ liệu hoặc bài khó hiểu; cần sửa và thử lại phần bị ảnh hưởng |
| Trước pilot trẻ | Bài được review và điều kiện trách nhiệm/dữ liệu/surface được chốt, phép ghi được chuẩn bị | Bất kỳ điều kiện bắt buộc nào chưa rõ thì tiếp tục rehearsal dữ liệu giả |
| Sau pilot | Có bằng chứng đủ cho quyết định trong đúng phạm vi, giữ thất bại/thiếu dữ liệu và chi phí | Không suy rộng, không tăng số tính năng để che vấn đề; có thể sửa mục tiêu hoặc dừng hướng |

## Chỉ số đề xuất, chưa có số đo

- **Usability:** nhiệm vụ hoàn tất không cần tác giả làm hộ, số/mức trợ giúp, thời gian thực, lỗi chặn và khả năng phục hồi; ghi mẫu và thiết bị.
- **Học tập:** bài ban đầu/có hỗ trợ/độc lập, giải thích và bài trì hoãn/chuyển bối cảnh nếu mục tiêu yêu cầu; tách baseline và mức trợ giúp. Không xem một phiên hoàn thành là học được.
- **AI nếu live:** hành vi theo task set, sai/rò đáp án/từ chối phù hợp, lỗi/retry, latency/cost và các mẫu số; human ratings chưa có thì null.
- **Vận hành:** phút chuẩn bị/hỗ trợ/tổng hợp, restore thành công, số vấn đề mở và phiên bị gián đoạn; cost API chỉ là một phần tổng chi phí.

Ngưỡng, cỡ mẫu và lịch chưa được các bên thống nhất nên chưa điền số. Kế hoạch dùng dependency và bằng chứng để chuyển pha; không hứa thời hạn production khi chưa biết năng lực người tham gia.

## Việc bắt đầu trước

Trên máy: P03-02 đọc sâu phương pháp, P03-03 bản đồ thiết kế một bài hiện có và P03-04 schema ghi quan sát để review; chưa thay dữ liệu/luồng hoạt động. Con người: P03-01 thống nhất product contract và xác nhận ai review/diễn tập. Đây là những việc chuẩn bị có thể song song. Khi contract rõ và đã review, chốt TIP P03 để triển khai các thay đổi cần thiết.

Quyền truy cập/đồng ý tham gia không do AI đại diện người khác xác nhận. Tài liệu này không gửi lời mời, không bổ nhiệm Thuý Anh/chuyên gia và không ghi nhận ai đã đồng ý.
