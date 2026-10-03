# Lỗi và rủi ro · sự kiện khác khả năng

Trạng thái: Bản nháp AI · chờ người phụ trách rà soát. Ngày soạn: 03/10/2026.

Issue là điều đã xảy ra và có cách tái hiện; risk là điều có thể xảy ra. Giữ hai loại riêng để không biến giả thuyết thành lỗi thực tế hoặc bỏ qua lỗi bằng câu “chỉ là rủi ro”.

## Mẫu bản ghi

ID ____; loại issue/risk ____; ngày ____; báo bởi ____; điều kiện/bản/version ____; sự kiện quan sát hoặc khả năng ____; ảnh hưởng ____; bằng chứng ____; mức độ P0/P1/P2/P3 ____; owner ____; xử lý đề nghị ____; trạng thái ____; ngày kiểm lại ____.

Đề xuất mức độ: P0 mất dữ liệu/điều kiện phải dừng; P1 chặn một luồng chính; P2 có cách tránh nhưng gây khó; P3 chi tiết ít ảnh hưởng. Đây là quy ước quản lý nháp, không là đánh giá an toàn đầy đủ. Người phụ trách quyết mức độ dựa trên ảnh hưởng thật.

## Ví dụ giả

ISS-DEMO-01: issue trong diễn tập giả định, mobile hẹp làm dòng nguồn khó đọc, có ảnh và kích thước cửa sổ. P2 đề xuất, sửa wrap và kiểm lại. Không ghi lỗi này như thực tế nếu chưa tái hiện.

RISK-DEMO-02: có thể người hướng dẫn đọc đáp án trước bước transfer. Chưa xảy ra; giảm bằng tách phiếu và kiểm màn hình. Owner vai vận hành; cần quan sát trong rehearsal. Không đánh dấu “đã loại bỏ rủi ro” chỉ vì checklist có ô.

## Đóng bản ghi

Ghi hành động thật, case kiểm lại và artifacts. Nếu deferred: ghi lý do, người chịu trách nhiệm, phạm vi được dùng, thời điểm xem lại. Theo dõi lỗi bằng [release guide](../guides/release-checklist.md), không đóng vì demo đã đẹp.
