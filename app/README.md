# Lớp thực hành AI · platform local P03

Bàn làm việc dành cho người hướng dẫn: nhóm học mẫu, nhiều hoạt động có phiên bản, soạn nội dung đầy đủ, rà soát diễn tập local, buổi học tám bước, hồ sơ bài làm, thư viện song ngữ và bàn diễn tập có readiness/quan sát cấu trúc. Hướng UI03 được giữ: masthead ngang, Lora cho học liệu/chương, Be Vietnam Pro cho thao tác, tiếp tục người học đang dở trước.

**Chỉ dùng dữ liệu mẫu.** Không nhập dữ liệu trẻ thật. Curriculum/rubric là nháp; rà soát trên máy chỉ là ghi nhận cho diễn tập người lớn, danh tính chưa xác thực, chưa phê duyệt dùng với trẻ.

## Chạy và kiểm

Tại thư mục `thuy-anh-ai-learning`:

**Bản public references-only:** resources đã biên dịch sẵn. Corpus nghiên cứu không đi kèm; compiler/checks strict yêu cầu khôi phục corpus hợp pháp đúng hash. Đọc README gốc trước khi rebuild. Kiểm public bằng `python3 -B tools/check_public.py`.

```sh
python3 -m http.server 8875 --bind 127.0.0.1 --directory app
```

Mở `http://127.0.0.1:8875`. Cần chạy qua HTTP để ES modules và fetch nguồn local hoạt động. Các tài nguyên đã sinh được kèm trong `app/resources/`; compiler tái lập từ allowlist trong `materials/catalog.json`. Không sửa file resources bằng tay.

```sh
node --test app/tests/*.test.mjs
node --check app/main.js
node --check app/model.js
node --check app/provider.js
node --check app/resources-client.js
```

Không framework, build dependency, API key, live provider, telemetry hoặc dịch vụ bên ngoài. Trình duyệt hiện đại cần ES modules, dialog, localStorage/fetch. Clipboard có giới hạn chờ và đường chọn/sao chép thủ công. Tải file có dialog nội dung dự phòng.

## Chọn và soạn hoạt động

Kho có ba bài nháp LES-01/02/03 từ curriculum, cộng hoạt động toán P01 legacy để giữ các phiên cũ. Seed idempotent; đọc lại resources không tự thay bản local đã sửa. Nhóm học chọn hoạt động dùng cho buổi mới; mở phiên dở giữ snapshot cũ.

Hoạt động → chọn bài hoặc Tạo hoạt động. Form có tên/mục tiêu/nhóm tuổi/thời lượng dự kiến, cả tám hướng dẫn, source ID, 1–12 thẻ nguồn, phản hồi AI mẫu, ba tiêu chí rubric và ghi chú người hướng dẫn/bài độc lập. Các phần dài mở theo disclosure. Validation chặn lưu thiếu nội dung; sửa tạo phiên bản mới và trở lại nháp. Thời lượng là dự kiến, không phải đo đạc.

Rà soát yêu cầu người tự nhập, ý kiến và quyết định “sẵn sàng diễn tập người lớn” hoặc “cần sửa trước diễn tập”. Ghi nhận tạo bản mới có dấu thời gian/phạm vi local; không chữ ký, không xác thực danh tính, không gán phê duyệt giáo dục. Phải lưu nội dung trước khi rà soát. Phiên đã chạy vẫn giữ bản và trạng thái rà soát lúc bắt đầu.

## Một vòng thực hành

1. Chọn hoạt động cho buổi mới; bắt đầu một học viên mẫu hoặc tiếp tục phiên dở.
2. Nhập suy nghĩ ban đầu trước AI.
3. Mở phản hồi mẫu đúng bài. Có chế độ mô phỏng lỗi/timeout và retry không mất bài.
4. Chỉ ra điều cần kiểm, đối chiếu nguồn, sửa kết luận, tự giải thích.
5. Làm bài mới không AI/thẻ nguồn/history; ghi chú riêng của người hướng dẫn không hiển thị ở bước này.
6. Người hướng dẫn nhập mã, từng điểm rubric và ghi chú; phần mềm không tự gán 0 hoặc kết luận tiến bộ.
7. Báo cáo giữ riêng bài ban đầu/có hỗ trợ/độc lập. Xuất text hoặc backup JSON.

Tạm dừng khóa nhập và chuyển bước. Tiến trình mặc định gọn ở tablet/mobile. Nút tiếp tục đứng sau phần cần làm và trước history tùy chọn. Phiên giữ instruction, fixture, source, rubric và review của đúng hoạt động/version, không lấy nội dung mới nhất lúc xem lại.

## Thư viện dự án

Link “Thư viện dự án” ở footer mở catalog, tìm theo tên/mô tả/source ID và lọc nhóm. Preview hỗ trợ tiêu đề, chữ đậm/nghiêng, code, danh sách, trích dẫn và bảng Markdown đơn giản. Link tài liệu trong catalog mở ngay trong thư viện; link HTTPS ngoài mở tab riêng. Link tương đối chỉ được ở bên trong resources; HTML được escape, không chạy nội dung nguồn. Tiêu đề đầu trùng tên tài liệu được lược trong preview, bản nguồn/export giữ nguyên. Có nguồn file cùng origin và dialog xem/sao chép/lưu nội dung thật. Không trộn tài liệu chưa đọc được vào file export.

Thư viện dành cho người hướng dẫn, có đáp án và ghi chú. Không đưa nguyên pack cho người học; chọn đúng handout theo giai đoạn. Catalog/resources/manifest là dẫn xuất của material allowlist, không copy backup QA hay thông tin riêng vào thư viện. Danh mục song ngữ gồm tài liệu nền, R01/M01 và bộ diễn tập P03; bản P03 hiện có 54 tài liệu VI cùng 54 bản EN, 3 bài nháp dịch đầy đủ và 112 file resources dẫn xuất. Manifest ghi số và fingerprint cụ thể. Source ID truy nguồn tham khảo, không tự xác nhận curriculum hiệu quả hoặc nguồn đã duyệt cho trẻ.

## Lưu trữ / migration / khôi phục

Giữ storage key `thuy-anh-ai-learning:p01:v1`; schema hiện tại 3. P01 schema 1 được kiểm bằng validator legacy trước migration. Bài làm, sự kiện, thời gian, người đánh giá, AI phản hồi và trạng thái phiên giữ nguyên. Bài P01 được gắn ID LEGACY-MATH01 cùng hướng dẫn/nguồn cũ, không đổi sang lesson mới. Backup P01 hợp lệ được import/migrate qua dialog xác nhận.

Schema 2 (định dạng lịch sử P02) có activity ID + chuỗi phiên bản riêng; selectedActivityId và snapshot của mỗi phiên. Version/review/snapshot sai bị từ chối; import hỏng không thay dữ liệu hiện tại. Migration lỗi hiển thị cảnh báo và giữ raw storage, dùng mẫu tạm ở RAM mà không tự ghi đè.

Bài làm lưu sau mỗi thay đổi trong localStorage theo origin/device/profile. Đổi port/host/profile tạo kho khác; JSON export/import là đường chuyển. Save thất bại giữ RAM và hướng dẫn xuất trước khi đóng. Backup tối đa 8 MB. Xóa yêu cầu thao tác giữ backup trước, rồi xác nhận riêng. Browser không cho ứng dụng biết người vận hành thực sự giữ file; kiểm tra file hoặc lưu nội dung thủ công.

## Chưa triển khai

Provider thật, benchmark live/cost/latency; authentication/authorization/backend/backup server; consent/chính sách vận hành với trẻ thật; duyệt giáo dục; tự chấm, chống gian lận/khóa màn hình; lịch học, nghiên cứu hiệu quả dài hạn; phát hành public. Bộ benchmark offline là chuẩn bị đo, không kết quả xếp hạng.

Khu mặc định dành cho người hướng dẫn; learner preview ẩn khu soạn, thư viện và rubric trong cùng ứng dụng local. Chế độ hiển thị không bảo vệ file/source hoặc xác thực người dùng; bài độc lập vẫn cần người hướng dẫn tổ chức đúng quy trình. Phần mềm/test PASS không chứng minh trẻ học tốt hơn.

## P03 · VI / EN và bàn diễn tập

Toggle VI / EN ở masthead chỉ đổi cách hiển thị. Preference nằm ở key riêng `thuy-anh-ai-learning:locale`; đổi ngôn ngữ không tạo activity revision, không thay bài làm/điểm/sự kiện và giữ form đang soạn. Tài liệu dùng bản English authored từ catalog; nguồn và nhãn draft giữ nguyên. Nếu thiếu bản dịch, hiển thị rõ bản Vietnamese. Input do người dùng nhập không được dịch tự động.

Bài seed mới lưu cả bản VI và EN trong snapshot; phiên cũ schema 1/2 giữ nguyên nội dung và được đánh dấu fallback VI, không lấy bản dịch mới nhất để thay lịch sử. Editor ghi rõ ngôn ngữ nguồn VI; lưu sửa xóa patch EN tránh bản dịch lỗi thời. Review không thay nội dung nên giữ patch EN.

Schema 3 thêm `observations` và `readiness`. Import schema 2 chỉ thêm hai mảng trống; schema 1 giữ migration legacy rồi thêm các trường mới. Observation ghi phiên/bước, người ghi, observed/reported/interpretation, mức hỗ trợ, số phút, mô tả/sự cố và scope synthetic-adult-rehearsal. Readiness có sáu điều kiện, owner/version/căn cứ/trạng thái; không có giá trị ready mặc định, không phải pilot approval. Màn Diễn tập xuất hồ sơ JSON; full backup chứa cả hai mảng.

“Xem vai người học” trong Buổi thực hành ẩn navigation người hướng dẫn, library, editor, report và bước rubric. Bài độc lập không hiển thị AI/thẻ nguồn/history. Nút quay lại người hướng dẫn luôn rõ. Đây chỉ là display mode trên cùng máy, không phải authentication/authorization hoặc chống truy cập file trực tiếp.

## English operator notes

Use the VI / EN toggle to select authored interface copy and document previews. Enter fictional identifiers and synthetic rehearsal records only. Local review identities are unverified. English translations are pinned with newly seeded lesson snapshots; older snapshots retain their original Vietnamese content with an explicit translation-fallback notice. Editing a local source draft removes its English patch rather than silently retaining a stale translation. Learner answers, reviewer notes and operational observations remain in their original language.

Open **Rehearsal** to record readiness evidence and structured observations. Readiness applies only to adult rehearsal, never to a child pilot. Observation type distinguishes direct observation, participant report and interpretation. Export a rehearsal record or a complete backup before transferring devices. The learner preview hides facilitator surfaces for local rehearsal; it does not provide access control. Live providers, server storage and verified human review remain pending.

Nếu máy đã lưu LES-01/02/03 từ P02, nút “Thêm phiên bản bài song ngữ” xuất hiện khi bản mới nhất khớp chính xác mọi trường nguồn VI và chưa có patch EN. Thao tác rõ của người vận hành tạo version kế tiếp có EN, một lần; không sửa bản cũ, snapshot phiên cũ hoặc bài người dùng đã chỉnh riêng. Các phiên mới có thể dùng edition mới. Ghi nhận review cũ giữ ở version cũ; edition mới trở lại draft. Không tự nâng nội dung trong lúc tải resources hoặc đổi UI language.

## Kiểm chứng APP P03

Bộ kiểm app có **51 kiểm thử tất định**: 36 trường hợp nền và 15 trường hợp P03 về migration, pin nội dung EN, nâng seed có kiểm soát, locale độc lập dữ liệu, source paths, observation/readiness, import lỗi, export có nhãn và reload kết hợp. PASS của các kiểm thử này xác nhận hành vi local trong phạm vi được kiểm, không phải hiệu quả giáo dục, audit accessibility toàn diện hoặc production approval. Browser QA được Contractor ghi riêng trong VERIFY-P03.

Trong P03 diễn tập nội bộ, các observation cũ chưa có ba field context dẫn xuất (activityId/activityVersion/learnerId) được bổ sung từ session đã validate nếu cả ba hoàn toàn chưa có. Context một phần hoặc bị sửa sai không được suy diễn thay thế. Mục đích là giữ được bản ghi đã lưu từ tab cache phiên bản trước; không đổi bài làm, điểm, lịch sử hoặc ý nghĩa của quan sát. Thư viện tìm đồng thời metadata VI/EN, nên đổi ngôn ngữ giữ query và khả năng tìm nguồn.
