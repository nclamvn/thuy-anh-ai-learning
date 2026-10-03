# Learner surface and storage · fit the delivery model

Status: AI proposal · P03 draft; no accepted roles, educational sign-off or actual field results. 3 October 2026.

P03 learner preview separates navigation for facilitator-held-device rehearsal; it is not a server permission or child account. Anyone with browser/files may inspect sources. Production option unchosen.

| Model | Surface | Storage/access | Checks |
|---|---|---|---|
| One facilitator-held device | Separate preview/facilitator UI | Operator-controlled browser/backups | No key leakage in distributed view, restore/file sharing |
| Learner-held device | Separate learner bundle/key | Context-appropriate identity/session/permissions | Server enforcement where needed, not hidden buttons; access/deletion |
| Multi-device/online class | Console + learner app | Tenant/role server, audit/backup | Authentication/authorisation/isolation/retry/offline/lifecycle |
| Paper/offline kit | Separate sheets | Operator-held records | Key/source collection, help recording, attributable re-entry |

Device holder ____; learner alone ____; group/space ____; network ____; retained data ____; allowed viewers ____; retention ____; offline/recovery ____; chosen model/reason ____.

Test key/history/library access from learner route, facilitator return, closed browser, save failure, unreadable backups, wrong profile, deletion and narrow/keyboard use. A future server requires object-level cross-user/role denial checks, leakage checks and tenant-correct restore. P03 has not implemented/tested that authentication.

Choose with contract/operational evidence, not infrastructure size. A facilitated kit may be suitable. Agree [data responsibility](participant-data-P03.md) before real data.
