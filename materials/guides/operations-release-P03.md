# Vận hành P03 · incident, release và bàn giao

Trạng thái: đề xuất AI · nháp P03, chưa có người nhận vai, review hay dữ liệu thực tế. 03/10/2026.

Mẫu cho bản local song ngữ; từng kết quả phải có artifact thật. Không lấy template điền được làm bằng chứng đã có người vận hành độc lập.

## Trước buổi

Build/hash ____; nguồn/lessons/catalog fingerprint ____; VI/EN ____; browser/profile/device ____; dữ liệu giả ____; backup trước và nơi giữ ____; người hướng dẫn/quan sát ____; lỗi/deferred/giới hạn ____.

Kiểm mở đúng bản, keyboard/focus, chữ chưa lưu khi toggle, nguồn/bài đúng locale, fixture, pause/retry/restore, learner preview. Giữ source-language/provenance và trạng thái draft rõ. Tên người học/tự nhập không tự dịch.

## Incident loop

Stop/pause nếu mất bài, nguồn sai, lộ key trong bài độc lập hoặc không biết data được ghi đâu. Giữ câu trả lời/original backup và thông báo; ghi thời điểm/step/version/viewport/data kind. Tách OBSERVED khỏi interpretation. Tránh retry hàng loạt hoặc xóa state khi chưa lưu. Owner triage impact → workaround/sửa → test case bị ảnh hưởng → ghi closure/deferred với phạm vi dùng. Không giả đo độ an toàn toàn hệ thống.

## Release và clean start

Run check command trong README hiện hành, giữ report/count/version. Compiler phải atomic: lỗi source/translation không ghi nửa kho. Gói chỉ source/app/docs/public research/SOT/delivery cho phép; bỏ env/key/private backups/QA/browser state. Check manifest/hash, giải nén thư mục thử riêng, chạy localhost, đọc cả VI/EN và thử export/restore synthetic. ZIP cũ giữ lịch sử; không gọi kiểm cũ là kiểm mới.

## Handover record

Người nhận thực ____; hướng dẫn đã đọc ____; việc tự làm ____; tác giả đã giúp ____; lỗi còn mở ____; chưa kiểm ____; fallback ____; quyền/giới hạn ____; evidence ____; trách nhiệm/lần xem lại ____.

Chỉ ghi “độc lập” sau quan sát. Chỉ ghi READY_LOCAL trong scope được kiểm, không production/pilot approval. Thời gian chuẩn bị/hỗ trợ/tổng hợp đều đo riêng; chi phí API không là tổng chi phí.
