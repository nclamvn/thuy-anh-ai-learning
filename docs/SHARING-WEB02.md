# Bàn giao nguyên bộ review · WEB02

Website hiện hành: [Tổng quan](https://thuy-anh-ai-learning.vercel.app/#overview) · [Hướng dẫn reviewer](https://thuy-anh-ai-learning.vercel.app/#guide) · [Bài LES-02 tiếng Anh](https://thuy-anh-ai-learning.vercel.app/#library?doc=MAT-04&lang=en). Link chứa mã tài liệu/ngôn ngữ, không chứa dữ liệu người học. [English](SHARING-WEB02.en.md).

Gửi link website để xem ngay; dùng Download project review kit để lấy ứng dụng và toàn bộ nội dung do dự án biên soạn. Gói không chứa trạng thái browser của người gửi. Người xem tự mở trang, đọc thư viện, thử flow bằng dữ liệu giả và điền phiếu góp ý trên máy của mình. Phiếu góp ý JSON là export riêng để chủ động gửi lại; chưa có import/merge/server nhận phiếu. Không giả định người khác đã nhận hoặc đã review.

## Đúng hai lớp manifest

`app/downloads/project-review-WEB02.json` mô tả release, số tài liệu, SHA-256/bytes ZIP, số file và sourceFingerprint. Nó là receipt dẫn xuất, không chữ ký. Sau giải nén, `CONTENT-MANIFEST.json` liệt kê hashes/bytes của từng file nội dung; manifest không tự băm chính nó. ZIP không lồng downloads hoặc PUBLIC-MANIFEST, tránh vòng checksum/recursion. Chỉ exact ZIP path này được gitignore cho phép lại; archive tự sinh khác tiếp tục bị bỏ qua.

Ứng dụng/VI–EN resource copies, 108 tài liệu authored, ba bài nháp, launcher, metadata tham khảo, benchmark/case/template giả định, LICENSE/PROVENANCE và font OFL đi kèm. Corpus HTML/PDF của bên thứ ba, runtime, env, credentials, tests/QA, localStorage, backup và người tham gia không vào bundle. Citation/capture metadata lịch sử không là xác nhận toàn văn hiện diện. Full-capture verification vẫn unavailable; original compile manifest giữ nguyên lịch sử, không rebuild để tạo PASS giả.

## Mở và đối chiếu

Giải nén nguyên thư mục; chạy `python3 -B -m http.server 8875 --bind 127.0.0.1 --directory app`, mở `http://127.0.0.1:8875/#overview`. Không cần API/model/provider thật. Bản offline dùng dữ liệu origin riêng; link tải ZIP mở website production vì ZIP không tự lồng. Tài liệu local dùng links có thật trong bundle; công cụ phát triển/strict provenance chỉ có ở public repo và vẫn cần corpus hợp pháp khi chạy compiler.

Từ **public source checkout**: `python3 -B tools/build_share_bundle.py` để rebuild sau sửa có chủ đích; `python3 -B tools/build_share_bundle.py --verify` chỉ kiểm, không tự sửa. Builder chọn source bằng allowlist, chặn symlink/traversal/private và kiểm graph module/CSS asset/Markdown trước khi ghi ZIP. ZIP có timestamp/order cố định. Sau app ổn định, rebuild bundle, refresh PUBLIC-MANIFEST có review, chạy `tools/check_public.py`, mới deploy. Source đổi mà quên rebuild phải FAIL.

Người reviewer đọc và tự quan sát; phiếu không xác thực danh tính, không phê duyệt dùng với trẻ. Dữ liệu giữ trên thiết bị theo origin; xoá/đổi browser có thể mất. Tài khoản, shared database, tự gửi email/chat, live AI và pilot chưa được thêm bởi bản WEB02.

## Giao diện UI05

Dòng bộ bàn giao vẫn là WEB02 để giữ link tải; inner/outer manifest ghi `visualEdition: R04`, source receipt là R04-public-01. Tám phòng làm việc có tranh nguyên bản riêng ở `app/assets/rooms/`: group, activity, session, reports, workbench, library, guide và review. Module `room-ui.js` cùng đủ tám SVG được liệt kê chính xác, kiểm graph/hash và đóng gói; không glob toàn thư mục để vô tình thu dữ liệu riêng. Giao diện vẫn giữ motion pause/reduced-motion, mọi trường nghiệp vụ, bài làm/snapshot và local-only scope. Artifact chỉ rebuild sau actual all-room QA và explicit freeze; P03 authored/resource compiler corpus giữ nguyên.

## Tích hợp tham chiếu R04

Link tải WEB02 giữ nguyên và nay có thêm `references-client.js`, danh mục tham chiếu, biên bản build riêng và hồ sơ nghiên cứu tại `app/references/`. Danh mục có 14 tài liệu nguồn và 92 tham chiếu nhận định; 54 mục học liệu vẫn được đếm riêng. Bảy tài liệu R03 gồm cả nghiên cứu cũ được đọc sâu, tổng hợp và bối cảnh chính sách, không phải bảy thử nghiệm độc lập mới. Mở `#references?lang=vi` hoặc `references/report.html?lang=vi`; đường quay lại nằm trong app sau giải nén và giữ ngôn ngữ. Link nhà xuất bản cần kết nối mạng.

Protocol build tham chiếu đối chiếu bản hồ sơ được tích hợp với bản authored đã đóng băng; không thay thế kiểm toàn văn vắng mặt. Module runtime, tệp tham chiếu, link HTML và vân tay metadata được kiểm trước khi đóng gói. Review thay đổi nguồn trước. Khi có các tệp font bị xoá từ trước, tạo stage sạch từ Git HEAD và chỉ chồng những tệp sửa có chủ đích đã được review; stage giữ font đã commit, working tree giữ nguyên các xoá đó. Chỉ tạo bundle và public manifest trong stage đã được review, rồi chủ động chép hai artifact tải và manifest về checkout.
