# Operating the local platform

Status: local operating guide. Prepared: 3 October 2026.

From the project directory run `python3 -m http.server 8875 --bind 127.0.0.1 --directory app`, then open `http://127.0.0.1:8875/`. Reuse an existing server on port 8875; do not launch a second one on that port. The operator checks background execution and shutdown in their own environment. This is localhost, without a login backend or multi-device synchronisation. Use a known browser profile so you do not confuse separate profiles' data.

## Before rehearsal

1. Export a backup and save it in an operator-selected directory, with a session code and date.
2. Select or copy a draft lesson; check title, instructions, source cards, sample response, rubric and notes.
3. Record a local review only if a real person performed it. The entered reviewer code is not authenticated and does not authorise use with children.
4. Create a fictional learner code; start the intended lesson/version and record the session ID.

## During and after the session

The session retains its starting lesson snapshot; editing creates a new version rather than changing work in progress. Pause and resume the correct session. AI currently uses fixtures, without measured model latency or cost. If a fixture fails, keep entered work, retry and record the error conditions.

After manual review, export a report and a new backup. Open a saved file and check its session ID. See [manual backup](backup-and-recovery.md) if automatic download fails.

## Data boundary

Clearing browser data may erase localStorage; it is not production storage. Identity verification, access roles and an organisation-approved data policy are absent. Use fictional data for current rehearsals. Agree real-data access, deletion and retention outside the software via the [human handoff](human-handoff.md).

Fictional example: DEMO-07 → LES-01 → record starting version → complete eight steps → DEMO-REVIEW enters comments → save DEMO-07-report.txt and a backup. Do not encode a child's name, school or birth date in their code.
