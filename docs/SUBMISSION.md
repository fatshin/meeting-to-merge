# Meeting to Merge — Submission

**Tagline:** Turn a meeting decision into tests and a minimal diff.

**Category:** Developer Tools  
**Codex Session ID:** `019f7306-7262-7371-a03f-6b99df7129bf`

## What it does

Meeting to Merge extracts timestamped behavioral requirements from a transcript,
turns each into a focused test, and prepares the smallest patch for human
review. It never applies the patch automatically.

## How it was built

Codex implemented transcript normalization, requirement extraction, test and
diff generation, a CRLF regression fix, and the public UI. GPT-5.6 is intended
to draft structured requirements; tests and the human gate remain authoritative.

## Proof

- 4 timestamped requirements produce 4 focused tests
- Windows line endings are regression-tested
- no change is applied without human review

## Links

- Live product: https://meeting-to-merge.fatshin.chatgpt.site
- Source: https://github.com/fatshin/meeting-to-merge
- Devpost draft: https://devpost.com/software/meeting-to-merge
- Video: `UPLOAD_TO_YOUTUBE_AND_REPLACE`

## Limits

The transcript and patch are synthetic. Repository owners retain merge control.
