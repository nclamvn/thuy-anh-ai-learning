# Đọc sâu phương pháp · phạm vi P03

Bản thẩm định kỹ thuật do AI soạn ngày 03/10/2026, chưa được chuyên gia giáo dục ký duyệt. Đọc có mục tiêu để ra quyết định thiết kế, không phải systematic review hoặc meta-analysis. Không chuyển kết quả quốc tế thành hiệu quả của platform này.

## Hồ sơ đọc và giới hạn

R01 giữ nguyên lịch sử 14 hồ sơ nguồn, 11 HTML captures hợp lệ và 22 claims. P03 bổ sung bốn bản toàn văn có SHA/byte count trong `research/fulltexts/capture-manifest.json`: OECD PDF, UNESCO PDF từ kho đồng tác giả UCL, hai HTML arXiv. Chúng là bản bổ sung của nguồn cũ, không tăng số nghiên cứu độc lập. Tải World Bank PDF chưa hoàn tất; ghi ba lần thử thất bại, không tuyên bố đã đọc phương pháp toàn văn. Những dấu vân tay chứng minh nội dung lưu, không xác nhận tính đúng của nghiên cứu.

| Nguồn / phần đã đọc | Điều có thể dùng | Giới hạn suy luận |
|---|---|---|
| [SRC-10 · Kestin, Scientific Reports 2025](https://www.nature.com/articles/s41598-025-97652-6): Methods, Results, Discussion từ HTML đã lưu; supplementary information chưa đọc riêng. | Thử nghiệm crossover hai bài vật lý đại học; 194/233 sinh viên đủ điều kiện phân tích. Tutor được thiết kế cho môn học; đánh giá ngay sau bài. | Điều kiện học tại nhà và lớp khác nhau; không phải trẻ Việt Nam hay đo duy trì dài hạn. Không lấy câu “học gấp đôi” làm cam kết sản phẩm. |
| [SRC-11 · nghiên cứu gia đình, arXiv v1](https://arxiv.org/html/2510.24070v1): Methods, Findings, Discussion/Limitations. | Định tính với 13 gia đình, trẻ 7–13 tuổi; tuyển qua quan hệ/snowball, trao đổi online trên khung thảo luận có sẵn. | Chủ yếu góc nhìn cha mẹ; không chứng minh tác động hay thang năng lực đã kiểm định. Dùng để thiết kế phỏng vấn, không áp giai đoạn phát triển cố định. |
| [SRC-12 · LearnLM/Eedi, arXiv v1](https://arxiv.org/html/2512.23633v1): Methods, limitations và phụ lục B/D/E/F/G/H chọn lọc. | 165 học sinh 13–15 tuổi, năm trường UK, bảy tuần; phân nhóm và tutor với người duyệt mọi tin AI. | Chuyển giao trong bài toán nền tảng không là duy trì độc lập dài hạn. Hiệu quả không tách khỏi người duyệt. Prompt phụ lục có chỉ dẫn che danh tính AI: không áp dụng vào dự án. |
| [SRC-13 · World Bank WP11125](https://openknowledge.worldbank.org/entities/publication/15e1ff08-15ae-4f7a-b2a8-d146e6c113ee): landing/abstract đã lưu; PDF chưa lấy được. | Có tín hiệu đáng theo dõi về một chương trình học có giáo viên hỗ trợ. | Comparator, attrition, randomisation và mô hình phân tích vẫn chưa được thẩm định ở P03. Không đưa con số abstract vào mục tiêu hoặc dự báo cho pilot. |
| [SRC-08 · OECD/EC 2026 bản cuối](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/06/empowering-learners-for-the-age-of-ai_2f8315e7/65cd27d4-en.pdf): cấu trúc, vai trò và competence; PDF trang 9–12, 27–43. | Bốn miền Engage/Create/Manage/Shape AI; progression không gắn cứng tuổi/lớp. | Framework định hướng, không phải bằng chứng hiệu quả hoặc rubric đo đã xác nhận. Cần giáo viên điều chỉnh theo người học. |
| [SRC-09 · UNESCO teacher framework 2024](https://discovery.ucl.ac.uk/10196729/1/UNESCO_AI_CFT_Final.pdf): principles và cấu trúc competence; PDF trang 15–18, 22–28. | Trách nhiệm sư phạm thuộc con người; xem AI như hỗ trợ năng lực và quyền chủ động. | Kho UCL là bản công bố của đồng tác giả. Framework không xác nhận ai trong dự án đã đủ chuyên môn hoặc được cấp chứng nhận. |

## Quyết định thiết kế của chúng ta · đề xuất cần thử

Chọn LES-02 để diễn tập trước: một thông báo cũ và một bản cập nhật buộc người học nhận biết thời điểm, nguồn và mức chắc chắn. Tình huống đời thường cho phép quan sát cách tìm căn cứ mà không để tốc độ tính toán lấn át. Đây là lý do thiết kế của nhóm AI, chưa là nhu cầu đã được gia đình xác nhận.

Giữ ba lớp bằng chứng tách biệt: bài ban đầu trước hỗ trợ; bài sửa sau nguồn/phản hồi; bài độc lập mới không AI và không mở đáp án. Thêm bài duy trì ở buổi khác nếu người giáo dục thấy phù hợp. Không dùng điểm tổng hợp tự động để suy ra tiến bộ hoặc xếp trẻ. Đổi ngôn ngữ cũng có thể đổi mức khó đọc, nên không gộp VI/EN vào so sánh hiệu quả trước khi kiểm tương đương.

Mỗi ghi nhận cần mã phiên, phiên bản bài, ngôn ngữ nhiệm vụ, trợ giúp thực tế, thời lượng quan sát và vai người ghi. Tách hành vi, lời kể và diễn giải; dữ liệu rehearsal giả không vào kết quả người thật. Điểm nhập tay phải đi kèm bằng chứng bài làm và người chịu trách nhiệm, không chỉ lựa chọn trong UI.

Khi hai người review khác nhau, giữ cả nhận xét và phần bất đồng, trao đổi cách hiểu rubric rồi sửa bản nháp. Không lấp ô trống bằng suy luận AI. Những đáp án minh họa phục vụ calibration nằm ở phần người hướng dẫn, không là dữ liệu kiểm định.

## Việc còn cần làm trước kết luận

- Chuyên gia rà soát nhiệm vụ, ngôn ngữ VI/EN, mức khó, rubric và bài duy trì; ghi quyết định theo phiên bản.
- Một người lớn khác tự vận hành và ghi lỗi mà không được AI dẫn từng bước. Rehearsal chứng minh vận hành trong điều kiện đó, chưa chứng minh hiệu quả giáo dục.
- Thuý Anh/Lâm xác nhận người dùng, nhu cầu, trách nhiệm dữ liệu và điều kiện tham gia; không dùng nội dung form khảo sát thay kết quả trả lời chưa được cung cấp.
- Đọc World Bank toàn văn và SI Kestin khi lấy được; kiểm phân bổ, attrition, mẫu phân tích, đối chứng, kết quả phụ và xung đột lợi ích trước sử dụng trong quyết định pilot.
- Nếu thử AI thật: khóa task set, model/version/prompt, chi phí và quyền gọi; log phản hồi gốc và quyết định người duyệt. Không đưa dữ liệu trẻ vào benchmark chuẩn bị.

Các việc này được theo dõi trong workbench và hồ sơ P03. Một checklist có ghi tên người hoặc evidence không tự xác thực danh tính, đồng ý tham gia hay phê duyệt sử dụng với trẻ.
