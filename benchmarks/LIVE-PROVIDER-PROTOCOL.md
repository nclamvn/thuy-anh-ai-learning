# Live-provider preparation · inactive proposal

This kit makes no provider calls. Its active response path remains a deliberately imperfect synthetic fixture. `provider-config.template.json` is an inactive plan, not an executable adapter. Keep credentials outside files; the field `credentialsEnvName` names a future environment variable and never contains a secret.

## Before any observed benchmark

The project owner must choose the service, exact model version, public synthetic adult task set, limits and who may authorize costs. A human operator must record that decision outside the unmeasured template. Review the current provider terms, retention/data region and available controls before selecting a provider. This document records no provider compliance finding. Child or private family data is excluded from this preparation.

Use the same frozen `task_cases.json` for every candidate, one recorded attempt per case/model/version, and preserve failures and abstentions. Record the system instructions, task hash, model version, settings, timestamp, response, raw-record reference, actual tokens, latency and actual invoiced or documented estimated cost method. Do not mix observed and synthetic records. Keep raw observed records outside the portable kit in an access-controlled local location. Strip credentials and personal data before sharing any result.

## Offline intake and review

Copy the structure from `response_template.json`. Set envelope `dataKind` to `observed-model-responses`, fill each row with a real observation and provenance `kind: observed`, timezone-bearing timestamp and evidence reference. Never convert synthetic fixture records into measurements. Keep unavailable tokens/cost/latency as null. Run:

```sh
python3 -B tools/evaluate_responses.py /path/to/observed-responses.json
```

The checker validates structure and produces descriptive metrics; it does not read the evidence reference or verify the authenticity of an observation. A named reviewer must compare the raw record, task and response, then record five quality ratings. A structural PASS never chooses a provider or proves learning/safety. Account for omitted tasks, timing differences, developer involvement and disagreement between reviewers in a separate decision memo.

## Incidents and stop rules

Pause testing if a key/private record leaks, costs exceed the human-approved cap, transport retries repeat a request, the model responds outside the allowed task, or data retention differs from the reviewed terms. Preserve a redacted incident record, owner, containment and reopening decision. No automated retries are enabled. A future adapter needs idempotency, timeout/cancellation, budget accounting, evidence storage, explicit failure states and a documented fixture fallback before integration.

The current template has a zero request/zero cost budget. Validate with `python3 -B tools/verify_provider_config.py benchmarks/provider-config.template.json`. An enabled/live configuration is intentionally rejected because activation is a different implementation and authorization step.
