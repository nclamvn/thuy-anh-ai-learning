# Vận hành platform local

Trạng thái: Hướng dẫn vận hành local. Ngày soạn: 03/10/2026.

Khởi chạy từ thư mục dự án: `python3 -m http.server 8875 --bind 127.0.0.1 --directory app`, rồi mở `http://127.0.0.1:8875/`. Nếu máy chủ 8875 đang chạy, dùng bản đang mở; không tạo một máy chủ trùng cổng. Lệnh nền và cách dừng được người vận hành kiểm trong môi trường của mình. Giao diện mở qua localhost; chưa có backend đăng nhập hoặc đồng bộ nhiều máy. Dùng trình duyệt và profile đã biết, tránh nhầm dữ liệu ở profile khác.

## Trước buổi diễn tập

1. Xuất backup từ giao diện; lưu vào thư mục do người vận hành chọn, tên có mã buổi và ngày.
2. Chọn hoặc sao chép bài nháp từ thư viện, kiểm title, instruction, thẻ nguồn, phản hồi mẫu, rubric và ghi chú.
3. Ghi nhận rà soát local nếu có người thật thực hiện. Mã người nhập không được xác thực; không coi đây là giấy phép sử dụng với trẻ.
4. Tạo học viên mẫu với mã giả; mở đúng bài và phiên bản. Người quan sát ghi mã phiên.

## Trong và sau buổi

Phiên giữ bản học liệu đã bắt đầu; sửa bài tạo bản mới để tránh thay yêu cầu giữa chừng. Tạm dừng khi cần, thử tiếp tục đúng phiên. Phản hồi AI hiện là fixture, không có latency/cost model thật. Nếu fixture lỗi, giữ bài đã nhập và thử lại; ghi điều kiện lỗi.

Sau đánh giá tay, xuất báo cáo và backup mới. Kiểm một file đã lưu mở được và có mã phiên đúng. Xem [backup/manual save](backup-and-recovery.md) khi tải tự động không hoạt động.

## Ranh giới dữ liệu

localStorage có thể mất khi xóa dữ liệu trình duyệt; không phải lưu trữ production. Chưa có phân quyền, xác thực danh tính hay chính sách dữ liệu đã được tổ chức duyệt. Dùng dữ liệu giả cho diễn tập hiện tại. Quyền xem/xóa/lưu dữ liệu thật cần thống nhất ngoài phần mềm theo [bàn giao con người](human-handoff.md).

Ví dụ giả: mã DEMO-07 → LES-01 → ghi phiên bản bắt đầu → hoàn thành tám bước → người đánh giá DEMO-REVIEW nhập nhận xét → lưu DEMO-07-report.txt và backup. Không ghi tên, trường hoặc ngày sinh trẻ vào mã.
