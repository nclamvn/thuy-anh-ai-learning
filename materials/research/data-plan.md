# Kế hoạch dữ liệu và kiểm giả thuyết · R01

03/10/2026. Đề xuất vận hành, chưa tuyển người/nhận responses hoặc xin quyền dữ liệu. Dùng cùng [bàn giao con người](../guides/human-handoff.md), [interview guide](../templates/interview-guide.md) và [evidence capture](../templates/evidence-capture.md).

## Luồng dữ liệu cần mang về

1. Khảo sát: bản câu hỏi đúng version, cách tuyển/mời, khoảng thời gian thu, số mời nếu biết, số responses hợp lệ/thiếu và quy tắc loại. Đã gửi khảo sát cá nhân không có nghĩa AI có quyền truy cập tập responses. Chưa có dataset trong kho.
2. Phỏng vấn: ghi một trải nghiệm cụ thể, việc đã làm, hỗ trợ đã dùng, điều khó, cách thay thế và điều trái với giả thuyết. Chỉ lấy ghi chú được phép dùng; tách lời kể khỏi trực tiếp quan sát.
3. Diễn tập người lớn: mã giả, bài/version, thiết bị, thứ tự bước, câu khó, mức hỗ trợ, lỗi, thời gian chuẩn bị/buổi/tổng hợp; không tính như mẫu trẻ.
4. Review giáo dục: người/và phạm vi, version, nhận xét có căn cứ, điều kiện cần sửa và kết luận trong phạm vi review. Platform ghi local không xác thực danh tính.
5. Thử thực tế: chỉ sau điều kiện người phụ trách xác nhận; thiết kế đánh giá, bài không AI, theo dõi và phạm vi dữ liệu cần chốt trước. R01 chưa thực hiện.

## Schema ghi tổng hợp đề xuất

record_id, data_kind (REPORTED/OBSERVED/AI_DRAFT), rq_ids, source_ref, collected_at, recorder_role, task_version, context, observation, interpretation, counter_evidence, assistance, missing_reason, next_decision. Dùng mã thay định danh không cần thiết. Mục không có dữ liệu để null/UNKNOWN; không điền zero cho chưa đo. Raw private records, nếu sau này có, phải có nơi lưu/quyền riêng do người phụ trách chọn, không mặc định đưa vào thư viện public local.

## Giả thuyết có thể bị bác bỏ

H1: gia đình ưu tiên kiểm chứng hơn lấy đáp án nhanh. Sẽ cần sửa nếu tình huống thực tế/chọn lựa của người được phỏng vấn cho thấy ưu tiên khác. Không xác nhận bằng câu hỏi dẫn dắt.

H2: chuỗi tám bước đủ dễ vận hành. Cần sửa nếu nhiều người lớn diễn tập phải được giải thích lại hoặc bỏ bước; chưa đặt tỷ lệ ngưỡng trước khi biết design/nguồn lực.

H3: người học tự thực hiện được nhiệm vụ mới sau trợ giúp. Chưa thử; cần bài đo phù hợp và điều kiện hỗ trợ ghi rõ. Bài đã sửa đẹp không tự xác nhận H3.

H4: AI thêm giá trị so với tài liệu/gợi ý đơn giản. Chưa thử; cần đối chứng cùng mục tiêu/thời gian và đo công người vận hành. Không lấy fixture trả nhanh làm bằng chứng.

## Đầu ra sau mỗi vòng

Một bản tổng hợp có RQ được hỗ trợ/chưa trả lời, ngoại lệ, dữ liệu thiếu, độ phù hợp và quyết định owner. Trước vòng mới, thống nhất tiếp/sửa/dừng và trách nhiệm. Không cố định cỡ mẫu, hiệu quả tối thiểu hoặc giá bán khi chưa có design và dữ liệu. Bộ R01 chuẩn bị cách tìm câu trả lời, không tự tạo câu trả lời người thật.
