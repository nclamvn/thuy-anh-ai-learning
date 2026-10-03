# AI provider · phép đo và gate trước live

Trạng thái: đề xuất AI · nháp P03, chưa có người nhận vai, review hay dữ liệu thực tế. 03/10/2026.

P03 giữ fixture mặc định; chưa chọn provider, gọi API, dùng key hoặc đo model. Tài liệu này chuẩn bị phép so sánh và quyết định có cần live. Học cách kiểm AI với ví dụ biên soạn không bắt buộc model thật.

## Contract trước run

Mục tiêu/bài/version/ngôn ngữ ____; AI chỉ gợi hay trả lời ____; dữ liệu được gửi ____; người giám sát ____; budget/max tokens/retries ____; model/version/config ____; task set/version ____; người đánh giá ____; hành vi không được chấp nhận ____.

Không nhập key vào browser/library/ZIP. Nếu có adapter sau này, server giữ secret, hạn mức, timeout/retry/cancel, log có giảm định danh và fallback biên soạn. AI identity phải rõ: không sao prompt che việc đang dùng AI hoặc giả người hướng dẫn. Người thật chịu trách nhiệm khi vượt phạm vi.

## Cùng điều kiện và metric có mẫu số

Cùng cases/input/context/config cho ứng viên; lưu output nguyên gốc, lỗi, model version, retry/usage/time/cost quan sát. Đừng xếp hạng fixture cạnh model. Chấm tay grounding/learningSupport/privacy/ageAppropriate/abstention0–4 với quote. Missing output/rating/latency/cost là null. Điểm kỹ thuật không là hiệu quả học.

Thử VI/EN riêng; thẻ nguồn đúng locale; kiểm hallucination, answer leakage ở independent step, source injection, yêu cầu thông tin riêng, giới hạn an toàn, failure, contradictory/missing source và tôn trọng người học. Xem [16 cases](scoring-guide.md); reviewer phải rà soát task set trước dùng trẻ.

## Quyết định sau đo

Báo fail quan trọng từng case, số thực chạy/missing/errors, distributions và tradeoff chất lượng/cost/human labour. Không average che lỗi lộ đáp án hoặc bịa nguồn. Owner chọn tiếp/sửa/giữ fixture với lý do/evidence. Ngưỡng chưa chốt không tự sinh pass. Offline checker chỉ kiểm schema/coherence, không tự nhận xét output. Theo [data responsibility](../guides/participant-data-P03.md).
