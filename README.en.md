# AI Learning Practice · Lớp thực hành AI

A local facilitator workspace for designing and rehearsing learning with AI: a persistent Vietnamese/English toggle, three draft lessons, 54 bilingual documents, eight-step learning sessions, work records and a structured observation/readiness workbench. P03 public-01 retains the accepted UI03 design and local application. [Vietnamese README](README.md).

**Scope: adult rehearsal with fictional data.** This is not approved for use with children, has no measured educational effectiveness in Vietnam and is not a production service. Learner preview hides facilitator controls; it is not authentication or security authorization. The AI provider uses deliberately flawed fixtures and makes no model/API calls.

## Run locally

Python 3.10+ is required; Node.js 18+ is needed for tests. No additional libraries are required to run the application or public check profile.

```sh
python3 -B -m http.server 8875 --bind 127.0.0.1 --directory app
```

Open [the local application](http://127.0.0.1:8875/), or run `./start-local.command` on macOS/Linux. Set `AI_LEARNING_PORT=8876` to change the launcher port. The header language toggle remembers your choice. User records remain in browser localStorage; export a backup before changing devices/origins or testing imports. Never commit real backups, child records, API keys or personal observations.

## Validate the public distribution

```sh
python3 -B tools/check_public.py
```

This checks fingerprints of **files actually distributed**, authored-to-generated learning material copies, local links, translated metadata, Python fault tests, Node app tests, both offline benchmarks and the inactive provider configuration. `PUBLIC-MANIFEST.json` is an integrity receipt, not a signature or educational quality approval. After intentional reviewed edits, refresh it with `python3 -B tools/create_public_manifest.py` and rerun checks.

**Raw third-party research works are not redistributed.** `research/` contains URLs, reference metadata, short extracted claims and historical capture hashes only. Snapshot/full-text paths refer to a separately held corpus, not files present in this public repository. Historical capture status does not mean the corpus is distributed here. Public checks explicitly report `fullCaptureProvenance: UNAVAILABLE` and exercise the unchanged strict verifier to expose its failure on missing works.

The original strict `check_all.py`, `verify_research.py`, `verify_project_kit.py`, compiler and packager remain intact. They require lawfully held corpus files restored manually at declared paths with matching hashes. There is no automatic download or fake corpus to bypass gates. The application runs using precompiled `app/resources/`; do not invoke `build_resources.py` in a public quickstart without restoring the corpus. [Source scope and rights](PROVENANCE.md).

## Further work

Agree the product contract and responsible decision makers; obtain educational review of LES-02; ask an independent facilitator to rehearse; decide consent/data/incident processes; then decide whether a child pilot, live AI and production operation are appropriate. Templates, age/time/rubric proposals and channel copy remain drafts. Locally entered review/readiness records do not authenticate identity or grant approval.

[Document library](materials/en/README.md) · [Curriculum](materials/en/curriculum/README.md) · [Application documentation](app/README.md) · [Benchmark](benchmarks/EVALUATION_GUIDE.md)

Public visibility does not select a software license. No MIT/Apache or other general reuse grant has been chosen for project code or documents; see [LICENSE.md](LICENSE.md). Included fonts retain their own SIL OFL and copyright notices.

![P03 English library · local adult rehearsal workspace](docs/images/library-en.png)
