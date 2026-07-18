# Meeting to Merge

Meeting to Merge carries four cited meeting requirements into failing test
names and a minimal proposed diff. A human approval boundary remains between
the proposal and repository mutation.

## Judge path

1. Run `./scripts/run.sh --port 8104`.
2. Open `http://127.0.0.1:8104`.
3. Select **Run analysis**.
4. Confirm four speaker-and-timestamp citations and four baseline failures.
5. Expand the machine-readable artifact and inspect the unified diff.
6. Remove the approval definition and rerun to see the fail-closed ambiguity gate.

## What is implemented

- timestamped `REQ-*` extraction;
- explicit ambiguity gate;
- one test name per requirement;
- a bounded diff for validation, approval, receipt, and idempotency;
- baseline FAIL and proposed-rerun PASS evidence;
- human apply requirement.

## Verification

```sh
./scripts/check.sh
```

## OpenAI and Codex

Codex was used to implement the requirement-to-diff workflow. GPT-5.6 can draft
requirements and patch candidates, while deterministic validation enforces
citations, ambiguity handling, and the human-apply boundary.

## Limits

The MVP operates on a bounded source snippet. It does not edit a live
repository, infer unstated product decisions, or claim a simulated rerun is CI.

