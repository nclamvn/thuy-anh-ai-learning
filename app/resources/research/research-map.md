# Bản đồ câu hỏi nghiên cứu · R01

Ngày 03/10/2026. Owner: Nguyễn Cảnh Lâm. Đề xuất AI để owner/Thuý Anh/người làm giáo dục rà soát; không phải kế hoạch đã được các bên đồng ý. R01 là tìm kiếm có mục tiêu, chưa phải systematic review. Nguồn canonical: `sot/source_canonical/research_questions.csv`.

Mỗi câu hỏi phải phục vụ một quyết định. P0 cần trước thử với trẻ; P1 cần trước chọn sản phẩm/provider; P2 cần trước mở rộng. Mức ưu tiên và phép đo dưới đây đều là đề xuất. [Khoảng trống](evidence-gap-register.md), [tổng hợp](evidence-synthesis-R01.md) và [kế hoạch dữ liệu](data-plan.md) là ba phần đi cùng.

| ID | Ưu tiên | Câu hỏi và quyết định | Bằng chứng đang có | Bằng chứng còn thiếu / cách lấy |
|---|---|---|---|---|
| RQ-01 | P0 | Gia đình đang vướng việc gì khi trẻ dùng AI? Chọn vấn đề đầu tiên | Chỉ có mô tả ý tưởng/khảo sát, chưa có responses | Phỏng vấn một lần sử dụng gần nhất; tổng hợp khảo sát đã được phép dùng |
| RQ-02 | P0 | Ai là người học đầu tiên, nền đọc/toán và thiết bị nào? | 13–15 là giả định bài mẫu | Người làm giáo dục đọc yêu cầu; người phụ trách xác nhận bối cảnh gia đình |
| RQ-03 | P1 | Ai cần sản phẩm và ai trả chi phí? | UNKNOWN | Phỏng vấn người quyết định, cách đang dùng và khoản chi thực tế; lời khen không là bằng chứng trả tiền |
| RQ-04 | P0 | Mục tiêu là hiểu AI, học môn học hay kiểm chứng? | SRC-01; SRC-08 đọc qua web, chưa capture local | Chọn một mục tiêu và nhiệm vụ quan sát; không gộp mọi mục tiêu vào rubric |
| RQ-05 | P0 | Trẻ hiểu và tự giải thích ra sao khi bỏ AI? | SRC-03A, SRC-05, SRC-10 | Bài ban đầu/bài mới tương đương, điều kiện hỗ trợ được ghi, chưa đo trẻ |
| RQ-06 | P0 | Mức gợi ý nào hỗ trợ mà không làm thay? | SRC-03A; SRC-12 có tutor giám sát | Diễn tập các mức gợi ý, log phản hồi và lỗi; người dạy duyệt mức phù hợp |
| RQ-07 | P0 | Có vận dụng sau một thời gian và ở bài khác không? | Transfer gần trong P02 chỉ là thiết kế | Người có chuyên môn chọn bài trì hoãn/chuyển bối cảnh; ngày đo và điều kiện do người phụ trách thống nhất |
| RQ-08 | P0 | Nội dung, độ khó và rubric phù hợp từng nhóm tuổi không? | SRC-01/02; ba bài AI nháp | Review từng version, diễn tập hiểu câu hỏi; không coi tuổi là đại diện duy nhất cho năng lực |
| RQ-09 | P0 | Phụ huynh/người dạy cần biết và làm gì? | SRC-11 định tính; SRC-09 chưa capture nội dung | Quan sát người lớn vận hành và phỏng vấn hiểu AI; ai xử lý tình huống cần được xác nhận |
| RQ-10 | P0 | Điều kiện tham gia, quyền dừng và phạm vi dữ liệu là gì? | SRC-02; human-handoff | Người chịu trách nhiệm chốt vận hành thực tế; review yêu cầu địa phương riêng, chưa xác nhận pháp lý |
| RQ-11 | P0 | Thông tin sai, thiếu nguồn hoặc câu hỏi vượt phạm vi xử lý thế nào? | SRC-06/07; benchmark đề xuất | Bộ tình huống tiếng Việt, người rà soát và tiêu chí không được bỏ qua; thử provider sau khi được chọn |
| RQ-12 | P1 | Hai người chấm có hiểu rubric giống nhau không? | Rubric P02 chưa kiểm định | Chấm độc lập cùng bài, giữ bất đồng và lý do rồi sửa mô tả; chưa có điểm thật |
| RQ-13 | P1 | AI có hơn một cách hỗ trợ đơn giản với cùng thời gian không? | SRC-10; SRC-13, khác đối chứng và bối cảnh | Thiết kế đối chứng công bằng với người có chuyên môn; không suy tác dụng model từ cả gói dạy |
| RQ-14 | P1 | Một buổi tốn bao nhiêu công người hướng dẫn? | 45 phút là ước lượng | Ghi chuẩn bị, hỗ trợ, sửa lỗi và tổng hợp trong diễn tập người lớn |
| RQ-15 | P1 | Provider nào phù hợp cùng task set và giới hạn? | 16 cases, chưa chạy model | Chốt ngân sách/giới hạn; ghi model/version/config, quality, lỗi, latency/cost thực |
| RQ-16 | P1 | Thiết bị yếu/mất mạng/lỗi lưu làm gián đoạn gì? | Prototype backup/error tests | Diễn tập trên thiết bị mục tiêu, phục hồi và đọc lại backup; mẫu local chưa là hạ tầng production |
| RQ-17 | P2 | Ai hưởng lợi/khó tiếp cận, ai bỏ giữa chừng? | SRC-11/13 chỉ gợi ý câu hỏi | Ghi mẫu tuyển, không tham gia, thiếu dữ liệu, nền kiến thức và điều kiện; không chỉ giữ phiên thành công |
| RQ-18 | P0 | Bằng chứng nào dẫn tới tiếp tục, sửa hoặc dừng? | Chưa có ngưỡng đã thống nhất | Owner và người dạy ghi tiêu chí trước thử; chưa đủ điều kiện con người thì giữ diễn tập người lớn |

Không đặt một cỡ mẫu “chuẩn” từ trí nhớ. Phỏng vấn khám phá, kiểm khả dụng và thử hiệu quả trả lời những câu khác nhau, cần thiết kế khác nhau. Ước lượng cỡ mẫu cho đánh giá hiệu quả cần người có chuyên môn và giả định thống kê rõ.
