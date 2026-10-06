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

## UI05 visual edition

The handoff retains WEB02 lineage/download URLs. Inner/outer manifests record `visualEdition: R04`; the source receipt is R04-public-01. Eight purposeful working rooms have original local artwork under `app/assets/rooms/`: group, activity, session, reports, workbench, library, guide and review. The exact `room-ui.js` module and all eight SVG paths enter graph/hash validation and the bundle; no folder glob can capture private records. Existing pause/reduced-motion, business fields, work/snapshots and local-only scope remain authoritative. Artifact regeneration follows actual all-room QA and an explicit freeze; the original P03 authored/resource compiler corpus stays unchanged.

## R04 references integration

The stable WEB02 download now also includes `references-client.js`, the native reference catalog, its separate build receipt and the hosted research dossier under `app/references/`. The directory contains 14 source documents and 92 claim references; the 54 learning-material entries remain a separate count. Seven R03 documents include a deepened existing study, a synthesis and policy context; they are not seven independent new trials. Browse `#references?lang=en` or open the dossier with `references/report.html?lang=en`. Its return path stays within the extracted app and preserves the language. Primary publication links require an internet connection.

The references build protocol checks the hosted derivative against the frozen authored dossier; it does not rerun missing raw-capture validation. Runtime imports, reference artifacts, hosted HTML links and metadata fingerprints are checked before packaging. Review source changes first. If inherited font deletions are present, create a clean release stage from committed Git HEAD and overlay only reviewed intended files; committed fonts stay in the stage while working-tree deletions remain untouched. Build the bundle and public manifest only in that reviewed stage, then copy the two generated download artifacts and the manifest back deliberately.
