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

## Giao diện UI04

Dòng phát hành bộ bàn giao vẫn là WEB02 để giữ nguyên link tải; inner/outer manifest ghi `visualEdition: UI04`. Tranh vector nguyên bản, motif đường sao và module điều khiển motion được chọn bằng đúng đường dẫn allowlist và kiểm hash cùng code. Motion có nút dừng, theo system reduced-motion, preference riêng trên browser; nó không đổi bài làm hay rubric. Rebuild/receipt chỉ thực hiện sau khi giao diện thực tế đã được review và freeze. Source receipt mang edition UI04-public-03; resource compiler manifest P03 giữ nguyên.
