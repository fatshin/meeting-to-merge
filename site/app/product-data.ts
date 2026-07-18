import type { Product } from "./product-types";

export const product: Product = {
  number: "04",
  name: "Meeting to Merge",
  eyebrow: "Spoken decisions to reviewable change",
  tagline: "Turn a meeting decision into tests and a minimal diff.",
  description: "Extract timestamped requirements from a transcript, translate them into executable checks, and prepare the smallest patch for human review.",
  accent: "#4e78ff",
  inputLabel: "Timestamped transcript",
  inputHint: "The same checkout transcript and broken source are evaluated by product.py.",
  inputValue: "[00:18] REQ-1 reject quantity below 1.\n[00:44] REQ-2 orders over $500 require manager approval.\n[01:12] REQ-3 receipt shows order ID.\n[01:48] REQ-4 retry must not create a second charge.\n[02:10] Approval means a non-empty manager token.",
  actionLabel: "Reveal verified result",
  status: "READY_FOR_HUMAN_APPLY",
  statusTone: "good",
  metrics: [{ value: "4", label: "requirements" }, { value: "4", label: "generated tests" }, { value: "0", label: "auto-applied changes" }],
  findings: [
    { title: "Four requirements extracted", detail: "REQ-1 through REQ-4 retain their timestamps and speakers.", badge: "TRACEABLE", tone: "good" },
    { title: "Four expected checks mapped", detail: "The fixture maps each requirement to a named baseline-fail / post-patch-pass expectation.", badge: "EXPECTED", tone: "warn" },
    { title: "Human apply gate preserved", detail: "The unified diff is proposed but never applied automatically.", badge: "REVIEW", tone: "good" },
  ],
  method: [
    { step: "01", title: "Extract", detail: "Identify explicit behaviors, boundaries, and owners with their timestamps." },
    { step: "02", title: "Test", detail: "Generate one focused assertion for each accepted requirement." },
    { step: "03", title: "Diff", detail: "Prepare only the lines needed to satisfy the tests and await review." },
  ],
  proof: ["Timestamp citations", "CRLF regression test", "Human-controlled apply"],
  note: "The transcript and patch are synthetic. The public demo never writes to a repository.",
};
