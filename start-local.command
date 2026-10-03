#!/bin/sh
# Local launcher: serves app/ on loopback only, without installing dependencies.
PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 2
if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'Không tìm thấy python3. Cần Python 3 có sẵn để mở bản local; launcher không cài phần mềm.'
  exit 2
fi
exec python3 -B - "$PROJECT_DIR" <<'PY'
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import sys

project = Path(sys.argv[1]).resolve()
app = project / 'app'
if not (app / 'index.html').is_file():
    print('Không thấy app/index.html. Giữ launcher trong thư mục gốc dự án hoặc giải nén đầy đủ gói local.', flush=True)
    raise SystemExit(2)
try:
    port = int(os.environ.get('AI_LEARNING_PORT', '8875'))
    if not 1024 <= port <= 65535:
        raise ValueError('Port must be 1024..65535')
except ValueError:
    print('AI_LEARNING_PORT phải là số nguyên từ 1024 đến 65535.', flush=True)
    raise SystemExit(2)
try:
    server = ThreadingHTTPServer(('127.0.0.1', port), partial(SimpleHTTPRequestHandler, directory=str(app)))
except OSError as exc:
    print(f'Không mở được cổng {port}: {exc}. Đóng phiên local cũ hoặc chạy AI_LEARNING_PORT=8876 ./start-local.command.', flush=True)
    raise SystemExit(2)
print(f'Mở trình duyệt: http://127.0.0.1:{port}/', flush=True)
print('Chỉ phục vụ app/ trên máy này. Nhấn Ctrl+C để dừng. Không kết nối cloud hoặc cài thêm thư viện.', flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('\nĐã dừng bản local.', flush=True)
finally:
    server.server_close()
PY
