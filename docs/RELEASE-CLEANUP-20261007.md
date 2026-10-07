# Release boundary and remaining debt · 7 October 2026

The static website is built with `node tools/build_site.mjs` (Node18+; no packages, secrets or network). It copies an exact allowlist from `app` into ignored `dist`, preserving source bytes. It checks declared catalog/report reference hashes, compiled resource hashes, kit source/output hashes, blank observations and the download archive's outer receipt before replacing a managed output. `.vercel/static-site-receipt.json` binds input/output SHA-256 and an aggregate fingerprint. `node tools/build_site.mjs --check` rejects source/output drift. A foreign or unlisted `dist` is never silently deleted.

Both Git and CLI deployments use `vercel.json` buildCommand/outputDirectory; `.vercelignore` limits CLI inputs but is not the output acceptance gate. Required compiler/kit metadata may enter build input; it does not enter `dist`. The output excludes tests, kit render.py/BUILD/CONTENT source, compiler/reference build manifests, source-only backend, docs, raw research and keys/env files. Runtime licenses and authored downloadable blank records remain. The downloadable review ZIP intentionally contains its declared authored browser handoff/provenance metadata, independently validated; it is not a route to arbitrary repository files.

| Priority / debt | Status / scoped evidence |
|---|---|
| P1 · direct app output depends on input exclusions | Fixed by one exact runtime-only output for local/CI/Git/CLI, negative input/output and tamper tests. This was a release-boundary weakness, not proof of a current production leak. |
| P2 · OFF guard missed direct calls with whitespace | Hardened for fetch/XMLHttpRequest/WebSocket/EventSource direct-call syntax, plus exact canonical source recovery. This is a bounded check, not an exhaustive network/security certificate. |
| P2 · active adult help said OFF until configured | Fixed by a recorded reversible public-copy adapter: static public has permanent OFF and no provider configuration. Local canonical source remains exact. |
| P2 · hosting docs described no build/app output | Updated to the dependency-free build, dist integrity check and separate source-only developer adapter. |
| Canonical one-line adapter sensitivity | Retained deliberate exact/fail-loud mapping; future canonical changes require a reviewed new projection, rather than silently normalizing historical source. No broad module refactor was needed. |
| Product/language/learning uncertainty | Open: bounded keyword matcher, unsupported wishes, adult/family research and education review, comprehensive accessibility/device validation. No unperformed study or full-corpus validation is promoted to PASS. |

```sh
python3 -B tools/check_public.py
node tools/build_site.mjs --check
python3 -m http.server 8875 --bind 127.0.0.1 --directory dist
```

For publication, the owner reviews the source manifest/bundle and CI, builds the same output, previews a Vercel deployment, verifies served bytes/routes/negative paths and promotes the intended deployment. CLI authentication/project selection is separate from source; no credential or active environment is required by the static build. Deployment identity and actual UI evidence live in the dated release receipt, not in a self-updating source claim. [Vercel build/output configuration](https://vercel.com/docs/project-configuration/vercel-json) and [deployment exclusions](https://vercel.com/docs/deployments/vercel-ignore) explain the respective controls.

Tiếng Việt: build chỉ tạo website static từ danh sách runtime đã chọn; mã nguồn developer và tài liệu kiểm không thành route. AI public luôn OFF, không gửi lời kể/ghi chú. Những kiểm tra trên xác nhận nguồn/output và luồng phần mềm đã quan sát, không chứng minh hiệu quả giáo dục, quyền chạy pilot, file tải đã lưu hoặc PDF native. Nợ nghiên cứu, giới hạn ngôn ngữ/mẫu dựng và đánh giá đầy đủ với người thật vẫn còn.

Production follow-up: the public kit footer now has two reversible locale-specific permanent-OFF replacements, leaving canonical content/generator/seven historical outputs exact. `trailingSlash:true` normalizes extensionless directory entries so relative modules and downloads resolve correctly; file extensions remain direct per [Vercel trailingSlash documentation](https://vercel.com/docs/project-configuration/vercel-json#trailingslash). Earlier production observations of unslashed failures are retained; corrected redirect/UI proof is recorded separately after redeployment.
