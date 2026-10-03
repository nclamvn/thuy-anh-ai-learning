# Bộ học liệu nháp · ba cách tự kiểm

Trạng thái: Bản nháp AI · chờ người phụ trách rà soát. Ngày soạn: 03/10/2026.

Các bài sau dùng cùng một tiến trình nhưng yêu cầu ba cách kiểm khác nhau. Chỉ dùng cho diễn tập người lớn cho đến khi người có chuyên môn rà soát mức khó, ngôn ngữ, rubric và điều kiện vận hành.

| Bài | Hành động người học | Giới hạn phép kiểm |
|---|---|---|
| [Đo lại điều AI nói](lesson-01.md) | Tính lại, phân biệt hai đại lượng | Bài gần cấu trúc cũ, chưa đo ghi nhớ dài hạn |
| [Đọc đúng lời hẹn](lesson-02.md) | Đối chiếu hai văn bản và nói chưa biết | Tài liệu hư cấu, không là kiểm sự thật ngoài đời |
| [Một câu hỏi có thể thử được](lesson-03.md) | Tách biến, thiết kế phép so sánh | Chỉ thiết kế trên giấy, chưa đo thực nghiệm |

Bản máy đọc: [lessons.json](lessons.json). Mỗi bài có tám instruction, thẻ nguồn tự soạn, phản hồi AI mẫu cố ý sai, rubric ba trục và ghi chú chuyển giao. Nguồn nghiên cứu trong sourceIds hỗ trợ cân nhắc phương pháp, không chứng minh độ đúng của mọi chi tiết bài soạn.

## Cách chọn bài

Hỏi người rà soát về nền kiến thức và mục tiêu trước; đừng xếp người học dựa trên tuổi một mình. Diễn tập lần đầu chọn một bài thay vì chạy cả ba trong một buổi. Bài LES-01 có phép tính rõ, dễ phát hiện lỗi vận hành; LES-02 phù hợp để thử cách ghi nguồn; LES-03 để thử mức trợ giúp khi câu trả lời có nhiều phương án hợp lý.

## Chu kỳ học liệu

Soạn nháp → [rà soát](../templates/curriculum-review.md) → diễn tập người lớn → ghi lỗi và sửa thành phiên bản mới → người phụ trách quyết định bước tiếp. Nhận xét local được nhập tay không xác nhận danh tính hay phê duyệt dùng với trẻ. Phiên đã bắt đầu giữ bản học liệu của phiên đó.

Không dùng điểm số mẫu làm kết quả thực tế. Ghi riêng nguồn, số phiên, mức trợ giúp và các điều còn thiếu bằng [phiếu quan sát](../templates/observer-sheet.md).

## Anchor P03 · LES-02

P03 giữ bài seed và bổ sung [bản đồ lý do](anchor-design-P03.md), [bộ đo trước/sau/trì hoãn](anchor-assessment-P03.md), [pack review/calibration](review-calibration-P03.md). Các gói vẫn nháp và không được phát key cho learner. Bản tiếng Anh có nội dung soạn tương ứng trong lessons.json; không tự dịch câu trả lời. Review độ khó/ngôn ngữ VI/EN riêng trước kết luận tương đương.
