# Bản phát hành local · ghi bằng chứng

Trạng thái: Hướng dẫn vận hành local. Ngày soạn: 03/10/2026.

Tài liệu này dùng để bàn giao một bản local có thể diễn tập. Hoàn tất checklist không xác nhận sản phẩm production, pháp lý hay hiệu quả giáo dục.

## Trước bàn giao

| Mục cần kiểm | Bằng chứng phải ghi |
|---|---|
| Bài mẫu và phiên bản | IDs, trạng thái nháp, ngày rà soát nếu thực hiện |
| Luồng tám bước | Một report mẫu có initial/revised/transfer và mức hỗ trợ |
| AI lỗi/tạm dừng | Bài nhập còn lại, nút tiếp tục đúng điều kiện |
| Bài độc lập | Không lộ source/history/AI; ghi can thiệp thật nếu có |
| Backup | File trước/sau và đối chiếu một phiên |
| Thư viện | Tài liệu mở được, nguồn/nháp rõ, bản sinh có fingerprint |
| Giao diện | Kiểm thao tác bằng bàn phím và các kích thước yêu cầu |
| Lỗi còn mở | Mã issue, mức độ, owner, thời điểm xem lại |

Từ thư mục dự án chạy `python3 tools/build_resources.py`, `python3 tools/verify_project_kit.py`, `node --test app/tests/model.test.mjs` và `python3 -m unittest discover -s tools/tests`; giữ report của lần chạy. Nếu Node chưa nằm trong PATH, dùng runtime được ghi trong README workspace thay vì đổi môi trường hệ thống. Số PASS chỉ phản ánh case đã chạy. Nhập mã người review local chưa chứng minh danh tính; bài có status nháp chưa tự biến thành được duyệt sư phạm.

## Mẫu biên bản local

Bản/build ____; ngày ____; người kiểm ____; mã case đã thử ____; case chưa thử ____; artifacts ____; lỗi/deferred ____; ai nhận bàn giao ____; phạm vi cho phép ____.

Ví dụ giả: bản DRY-BUILD-A, bốn case đã thử, còn chưa thử phục hồi trên trình duyệt khác. Ghi “sẵn sàng diễn tập local trong profile đã thử”, không ghi “an toàn cho mọi người học”. Chỉ quyết định phát hành ngoài máy sau khi người có trách nhiệm chốt nội dung, vận hành, dữ liệu và hạ tầng.
