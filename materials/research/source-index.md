# Chỉ mục nguồn · provenance và giới hạn

Trạng thái: Chỉ mục nguồn. Ngày soạn: 03/10/2026.

Sau R01 có 11 nguồn capture hợp lệ và 22 claims. Manifest 14 dòng giữ ba lần capture unavailable: PNAS trực tiếp (có bản PMC cùng DOI), OECD HTML 403 và UNESCO teacher page trả challenge. Chỉ đếm DOI/nghiên cứu độc lập một lần. Bản nguồn, SHA và claim nằm trong `research/sources.json` và `research/claims.jsonl`. Đây là chỉ mục intake, chưa phải toàn bộ literature hoặc xác nhận hiệu quả địa phương.

## SRC-01 · UNESCO AI competency framework for students

[Đọc nguồn gốc](https://www.unesco.org/en/articles/ai-competency-framework-students) · 2024.

Khung năng lực giúp tổ chức mục tiêu có trọng tâm con người. Khung không cung cấp đáp án bài toán hoặc chứng minh học liệu này có hiệu quả.

## SRC-02 · UNICEF Guidance on AI and children

[Đọc nguồn gốc](https://www.unicef.org/innocenti/reports/policy-guidance-ai-children) · 3.0 / 2025.

Hướng dẫn về AI và trẻ em giúp đặt câu hỏi về quyền, sự tham gia và trách nhiệm. Không thay quy trình đồng ý hoặc tư vấn pháp lý tại địa phương.

## SRC-04 · EEF Metacognition and Self-Regulated Learning

[Đọc nguồn gốc](https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/metacognition) · current page.

Hướng dẫn siêu nhận thức hỗ trợ cân nhắc các bước lên kế hoạch, tự theo dõi và xem lại. Chuỗi tám bước của dự án là lựa chọn soạn mới.

## SRC-05 · IES Organizing Instruction and Study to Improve Student Learning

[Đọc nguồn gốc](https://ies.ed.gov/ncee/wwc/practiceguide/1) · 2007.

Hướng dẫn dạy và học giúp cân nhắc việc tự nhớ và kiểm lại kiến thức. Một bài transfer gần không đo ghi nhớ lâu dài.

## SRC-06 · NIST AI 600-1 Generative AI Profile

[Đọc nguồn gốc](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) · 2024.

Profile rủi ro AI tạo sinh giúp lập danh sách điều phải kiểm và giới hạn vận hành. Không chứng nhận platform an toàn.

## SRC-07 · OWASP LLM Top 10 official repository

[Đọc nguồn gốc](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10) · 2026.

Kho nhận thức bảo mật LLM hỗ trợ soạn các tình huống thử prompt/data handling. Không là báo cáo penetration test cho platform này.

## SRC-03A · Bastani et al. Original PNAS article archived in PMC

[Đọc nguồn gốc](https://pmc.ncbi.nlm.nih.gov/articles/PMC12232635/) · 2025; doi:10.1073/pnas.2422633122.

Nghiên cứu thực nghiệm gợi ý cần cân nhắc loại trợ giúp và kiểm năng lực khi bỏ AI. Không chuyển kết quả của nghiên cứu sang tỷ lệ hiệu quả cho bộ bài Việt Nam.

## Thẻ nguồn giảng dạy khác nguồn nghiên cứu

Các công thức hình chữ nhật, thông báo CLB và thẻ phép so sánh trong [curriculum](../curriculum/README.md) do nhóm soạn. Thông báo CLB hoàn toàn hư cấu; phản hồi AI là fixture cố ý có lỗi. SourceIds ở bài chỉ dẫn đến nguồn phương pháp. Không dùng nhãn SOURCE_CAPTURED cho tình huống tác giả tạo.

## Nếu nguồn đổi hoặc chưa đủ

Ghi nguồn mới/phiên bản mới và để owner chạy quy trình Refinery/SOT trước khi đổi claim canonical. Không cập nhật số hoặc suy đoán nghiên cứu từ trí nhớ. Nội dung lesson mới vẫn cần người làm giáo dục rà soát, dù source link mở được.

## Nguồn mới và chương trình nghiên cứu R01

[Hồ sơ bốn nguồn mới](evidence-cards-R01.md): SRC-10 Scientific Reports RCT với sinh viên; SRC-11 nghiên cứu gia đình preprint; SRC-12 RCT exploratory preprint với tutor giám sát; SRC-13 World Bank working paper. Cards ghi capture level, thiếu appraisal và giới hạn. SRC-08/09 chờ capture, không dùng làm sourceIds đã kiểm.

[Bản đồ câu hỏi](research-map.md) · [khoảng trống](evidence-gap-register.md) · [protocol](selection-protocol.md) · [đối chiếu](evidence-synthesis-R01.md) · [kế hoạch dữ liệu](data-plan.md).
