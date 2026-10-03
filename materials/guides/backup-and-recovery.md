# Lưu thủ công và phục hồi

Trạng thái: Hướng dẫn vận hành local. Ngày soạn: 03/10/2026.

Backup là ảnh trạng thái dữ liệu local của trình duyệt, khác với báo cáo một phiên. Xuất cả hai trước khi đổi máy hoặc thử import. Chỉ nhập file có nguồn do người vận hành biết; schema không hợp lệ phải bị từ chối mà không ghi đè dữ liệu.

## Lưu và kiểm

- Bấm xuất backup; nếu trình duyệt tạo file, mở bằng trình đọc văn bản và kiểm mã học viên mẫu, mã phiên và dữ liệu bài làm.
- Nếu IAB không xác nhận tải: dùng phần xem/sao chép của giao diện, sao chép toàn bộ nội dung, lưu dạng UTF-8 `.json` bằng editor. Không chỉ lưu ảnh màn hình.
- Đặt tên ví dụ giả: `DRY-01-before-2026-10-03.json` và `DRY-01-after-2026-10-03.json`. Không cần đưa mã có định danh thật vào tên.
- Lưu báo cáo riêng `.txt`; báo cáo giúp đọc kết quả, không thay backup phục hồi.

## Phục hồi có đối chiếu

Xuất trạng thái hiện tại trước. Chọn file backup trong import, đọc thông báo hợp lệ và xác nhận thay dữ liệu nếu đúng mục đích. Sau nhập: so mã học viên, số phiên, tên/version bài, nội dung bài đang dở và trạng thái tạm dừng. Chọn một phiên đã hoàn thành, kiểm nhận xét/điểm vẫn còn. Nếu import báo lỗi, ghi thông báo và giữ file; không sửa số phiên cho khớp bằng phỏng đoán.

## Khi gặp sự cố

Không xóa dữ liệu trình duyệt khi chưa có backup đọc được. Nếu chỉ còn báo cáo, ghi rõ mất khả năng phục hồi phiên; có thể lưu bằng chứng đọc được, không giả tạo phiên cũ. Dữ liệu local chưa được mã hóa/quản lý truy cập ở mức production; quyền lưu, chia sẻ và xóa dữ liệu thật là điều chưa chốt.

Mẫu ghi kiểm: Người vận hành ____; file trước ____; file sau ____; kiểm phiên ____; bài ban đầu khớp ____; nhận xét khớp ____; lỗi ____. Ví dụ giả: DRY-01 import file thiếu schema bị từ chối, phiên cũ còn đủ; kết luận “import lỗi không ghi đè” trong điều kiện đã thử.
