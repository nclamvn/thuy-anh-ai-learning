# Local release · record the evidence

Status: local operating guide. Prepared: 3 October 2026.

Use this to hand over a local rehearsal build. Completing it does not certify production readiness, legal compliance or educational effectiveness.

| Check | Evidence to record |
|---|---|
| Lessons/versions | IDs, draft status, review date if actually performed |
| Eight-step flow | Sample report with initial/revised/independent work and assistance |
| AI failure/pause | Entered answers retained; correct resume conditions |
| Independent task | No source/history/AI leakage; actual interventions recorded |
| Backup | Before/after files and one compared session |
| Library | Documents open, source/draft labels clear, generated fingerprint |
| Interface | Keyboard operation and requested viewport sizes |
| Open issues | ID, severity, owner, review point |

Run `python3 tools/build_resources.py`, `python3 tools/verify_project_kit.py`, `node --test app/tests/model.test.mjs` and `python3 -m unittest discover -s tools/tests` from the project directory; retain the run report. If Node is outside PATH, use the runtime documented in the workspace README rather than modifying the system. A PASS count describes the tested cases. A local reviewer code does not prove identity; a draft does not become educationally approved through software.

## Local handover record

Build ____; date ____; checker ____; cases tried ____; cases not tried ____; artifacts ____; open/deferred issues ____; recipient ____; permitted scope ____.

Fictional example: DRY-BUILD-A has four tested cases but no cross-browser restore. State “ready for local rehearsal in the tested profile”, not “safe for every learner”. External release requires responsible people to agree content, operations, data and infrastructure.
