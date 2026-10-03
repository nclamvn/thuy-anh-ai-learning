# Lớp thực hành AI · AI Learning Practice

Bộ công cụ local dành cho người hướng dẫn thiết kế và diễn tập việc học có AI: giao diện VI/EN, ba bài học nháp, thư viện 54 tài liệu song ngữ, phiên học tám bước, hồ sơ bài làm và bàn ghi quan sát/readiness. Bản P03 public-01 giữ hướng thiết kế UI03 và ứng dụng đã nghiệm thu trên máy. [English README](README.en.md).

**Phạm vi: diễn tập người lớn với dữ liệu giả.** Chưa được phê duyệt sử dụng với trẻ, chưa có kết quả hiệu quả giáo dục tại Việt Nam và chưa là dịch vụ production. Preview người học chỉ ẩn công cụ người hướng dẫn; không có xác thực hay phân quyền bảo mật. AI hiện dùng fixture cố ý có lỗi, không gọi model/API trả phí.

## Chạy trên máy

Cần Python 3.10+; Node.js 18+ chỉ cần cho tests. Không cài thư viện để chạy ứng dụng hoặc bộ kiểm public.

```sh
python3 -B -m http.server 8875 --bind 127.0.0.1 --directory app
```

Mở [ứng dụng local](http://127.0.0.1:8875/). Hoặc chạy `./start-local.command` (macOS/Linux); `AI_LEARNING_PORT=8876` để đổi cổng. Toggle VI/EN ở đầu trang ghi nhớ lựa chọn. Dữ liệu người dùng lưu trong localStorage của trình duyệt; xuất backup trước khi đổi máy/origin hoặc thử import. Không đưa bản backup thật, dữ liệu trẻ, khóa API hoặc quan sát cá nhân lên GitHub.

## Kiểm bản public

```sh
python3 -B tools/check_public.py
```

Bộ kiểm này xác nhận dấu vân tay của **file đang được phân phối**, nguồn/copy học liệu, link local, metadata dịch, Python fault tests, Node app tests, hai benchmark offline và provider config chưa kích hoạt. `PUBLIC-MANIFEST.json` là receipt kiểm tính toàn vẹn, không chữ ký, không chứng minh chất lượng sư phạm. Sau thay đổi có chủ đích và review, cập nhật receipt bằng `python3 -B tools/create_public_manifest.py`, rồi chạy lại bộ kiểm.

**Toàn văn nghiên cứu không được tái phân phối.** `research/` chỉ có URL, metadata, claim trích ngắn và hashes của capture lịch sử. Các đường dẫn snapshot/fulltext trong metadata trỏ đến corpus lưu riêng, không phải file có sẵn trong repo public. Trạng thái capture lịch sử không đồng nghĩa corpus có trong bản này. Bộ kiểm public luôn ghi `fullCaptureProvenance: UNAVAILABLE` và thực thi verifier strict nguyên bản để cho thấy nó thất bại khi thiếu corpus.

`tools/check_all.py`, `verify_research.py`, `verify_project_kit.py`, compiler và packager strict vẫn giữ nguyên. Chúng yêu cầu corpus hợp pháp đúng hash được khôi phục thủ công tại các đường dẫn đã ghi; không có tải lại tự động, không tạo dữ liệu giả để vượt gate. App có `app/resources/` đã biên dịch nên chạy được mà không có corpus. Không gọi `build_resources.py` trong quickstart public khi thiếu corpus. [Phạm vi nguồn và quyền](PROVENANCE.md).

## Đường hoàn thiện

Chốt product contract giữa người chịu trách nhiệm; chuyên gia giáo dục review LES-02; người hướng dẫn độc lập diễn tập; quyết định dữ liệu/consent và xử lý sự cố; chỉ sau đó quyết định pilot, live AI và vận hành production. Các template, đề xuất độ tuổi/thời lượng/rubric và nội dung kênh vẫn là nháp. Review/readiness do người tự nhập trên máy không xác thực danh tính, không tự cấp phê duyệt.

[Kho tài liệu](materials/README.md) · [Bài học](materials/curriculum/README.md) · [Tài liệu ứng dụng](app/README.md) · [Benchmark](benchmarks/EVALUATION_GUIDE.md)

Public visibility không tự chọn license phần mềm. Chưa cấp MIT/Apache hoặc quyền tái sử dụng riêng cho code/tài liệu dự án; xem [LICENSE.md](LICENSE.md). Các font đi kèm giữ nguyên SIL OFL và thông báo copyright riêng.

![P03 English library · local adult rehearsal workspace](docs/images/library-en.png)
