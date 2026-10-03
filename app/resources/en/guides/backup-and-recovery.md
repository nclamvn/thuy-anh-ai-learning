# Manual saving and recovery

Status: local operating guide. Prepared: 3 October 2026.

A backup is a snapshot of browser-local data, distinct from a single-session report. Export both before switching computers or testing an import. Only import a file whose origin the operator knows; invalid schema must be rejected without overwriting current data.

## Save and inspect

- Export a backup; if downloaded, open it in a text reader and check fictional learner codes, session IDs and answers.
- If the in-app browser cannot confirm a download, use the interface's preview/copy option, copy the entire payload and save UTF-8 `.json` in an editor. A screenshot is not a backup.
- Fictional filenames: `DRY-01-before-2026-10-03.json` and `DRY-01-after-2026-10-03.json`. Do not place identifying codes in filenames.
- Save a separate `.txt` report; it is readable evidence, not a restorable state backup.

## Restore with comparison

Export current state first. Select the backup, read validation feedback and confirm replacement only for the intended purpose. Compare learner codes, session counts, lesson title/version, unfinished answers and pause state. Check a completed session's comments/scores. If import fails, retain the message and file; do not invent edits to make counts match.

## Incident response

Do not clear browser data before obtaining a readable backup. If only a report remains, record that the session cannot be restored; retain readable evidence without fabricating the old session. Local data lack production encryption/access management; rights to retain, share and delete real data remain undecided.

Record: operator ____; before file ____; after file ____; checked session ____; original answers match ____; comments match ____; error ____.

Fictional example: DRY-01 rejects a file without a schema and retains existing sessions. The conclusion “failed import did not overwrite data” applies only to the tested conditions.
