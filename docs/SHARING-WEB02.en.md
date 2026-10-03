# Full review handoff · WEB02

Current website: [Overview](https://thuy-anh-ai-learning.vercel.app/#overview?lang=en) · [Reviewer guide](https://thuy-anh-ai-learning.vercel.app/#guide?lang=en) · [LES-02 in English](https://thuy-anh-ai-learning.vercel.app/#library?doc=MAT-04&lang=en). Links contain document/language identifiers, not learner records. [Vietnamese](SHARING-WEB02.md).

Share the website for immediate viewing; Download project review kit provides the application and all project-authored content. It does not contain the sender's browser state. Reviewers open the site, read the library, try a flow using fictional data and fill in a local review form. Review JSON is a separate export for deliberate return; there is no review import/merge/server endpoint. Do not assume someone received or reviewed a link.

## Two manifest layers

`app/downloads/project-review-WEB02.json` records release, document counts, archive SHA-256/bytes, file count and sourceFingerprint. It is a derived receipt, not a signature. Inside the extracted kit, `CONTENT-MANIFEST.json` lists hashes/bytes for every content file and does not hash itself. Downloads and PUBLIC-MANIFEST are not nested inside the ZIP, preventing checksum cycles/recursion. Gitignore re-admits only this exact generated ZIP; other archives remain ignored.

Application/VI–EN resources, 108 authored documents, three draft lessons, launcher, research reference metadata, synthetic benchmark/case/templates, LICENSE/PROVENANCE and font OFL notices are included. Third-party HTML/PDF corpus, runtime, env/credentials, tests/QA, localStorage/backups and participant records are excluded. Historical citation/capture metadata does not mean full works are present. Full-capture verification remains unavailable; the original resource compile manifest preserves its history, not a fabricated rebuild PASS.

## Open and verify

Extract the entire directory; run `python3 -B -m http.server 8875 --bind 127.0.0.1 --directory app`, then open `http://127.0.0.1:8875/#overview`. No real model/API/provider is needed. Offline data belongs to its own origin; ZIP download links open production because no recursive ZIP is included. Local document links resolve within the bundle. Developer tools/strict provenance are in the public repository; the compiler still requires lawfully held corpus.

From the **public source checkout**: `python3 -B tools/build_share_bundle.py` deliberately rebuilds after source edits; `python3 -B tools/build_share_bundle.py --verify` checks without repairing. An explicit allowlist, confinement and symlink/private-path rejection select input files. Module/CSS asset/Markdown graphs are checked before writing. ZIP timestamps/order are fixed. Freeze app changes, rebuild, refresh the reviewed PUBLIC-MANIFEST, run `tools/check_public.py`, then deploy. Source changes without rebuilding must FAIL.

Reviewers read and observe; review forms do not authenticate identity or approve use with children. Records stay on the device by origin and can disappear after browser data removal. WEB02 adds no accounts, shared database, automatic email/chat submission, live AI or child pilot.

## UI04 visual edition

The handoff retains WEB02 lineage and download URLs; inner/outer manifests record `visualEdition: UI04`. Original vector artwork, star-path motifs and the motion-control module enter through exact allowlisted paths and share content hashes with the code. Motion has a pause control, follows system reduced-motion and stores a separate browser preference; learning records/rubrics stay unchanged. Rebuild/receipt generation follows actual visual review and an explicit freeze. The source receipt edition is UI04-public-03; the original P03 resource compile manifest is retained.
