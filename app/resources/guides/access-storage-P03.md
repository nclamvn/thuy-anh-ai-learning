# Surface và lưu trữ · chọn theo cách sử dụng

Trạng thái: đề xuất AI · nháp P03, chưa có người nhận vai, review hay dữ liệu thực tế. 03/10/2026.

P03 learner preview tách navigation để người hướng dẫn cầm thiết bị diễn tập; không là quyền server hoặc tài khoản trẻ. Người dùng có file/browser vẫn có thể xem nguồn. Phương án production chưa chọn.

| Mô hình | Surface | Storage/truy cập | Điều cần kiểm |
|---|---|---|---|
| Một máy, người hướng dẫn giữ | Preview + facilitator riêng | Browser/backup do operator giữ | Không lộ key trong phần phát, restore, file-sharing |
| Người học tự dùng thiết bị | Learner surface tách bundle/key | Identity/session/permission theo bối cảnh | Quyền server khi cần, không dựa giấu nút; xóa/truy cập |
| Lớp nhiều máy/online | Instructor console + learner app | Server phân tenant/role, audit/backup | Auth/authorization, isolation, retry/offline/data lifecycle |
| Kit giấy/offline | Phiếu tách riêng | Hồ sơ người vận hành | Thu/cất key và nguồn, ghi trợ giúp, nhập lại có provenance |

## Decision record

Ai giữ thiết bị ____; người học truy app một mình không ____; nhóm/nơi ____; có network ____; data cần giữ ____; người được xem ____; thời hạn ____; offline/recovery ____; mô hình chọn/lý do ____.

## Phép thử bắt buộc theo lựa chọn

Truy key/history/library từ learner route; quay lại facilitator; lỡ đóng browser; save fail; backup unreadable; nhầm profile; reset/xóa; dùng thiết bị hẹp/keyboard. Với server tương lai: thử truy object của người khác/role khác, không chỉ nav; xác minh denied không lộ data và restore đúng tenant. P03 chưa triển khai hoặc test auth đó.

Không dùng service lớn hơn nhu cầu chỉ để tỏ trưởng thành. Chọn mô hình bằng contract và dữ liệu vận hành; một kit có người hướng dẫn có thể hợp lý nếu đúng mục tiêu. [Data trách nhiệm](participant-data-P03.md) cần được chốt trước dữ liệu thật.
