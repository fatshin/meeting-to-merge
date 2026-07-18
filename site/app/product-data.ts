import type { Product } from "./product-types";

export const product: Product = {
  number: "04",
  name: "Meeting to Merge",
  eyebrow: "Spoken decisions to reviewable change",
  tagline: "Turn a meeting decision into tests and a minimal diff.",
  description: "Extract timestamped requirements from a transcript, translate them into executable checks, and prepare the smallest patch for human review.",
  accent: "#4e78ff",
  inputLabel: "Timestamped transcript",
  inputHint: "Four explicit requirements are included in this deterministic fixture.",
  inputValue: "[08:12] Reject empty project names. [11:04] Preserve existing slugs. [15:31] Normalize Windows line endings. [19:45] Do not apply the patch without human review.",
  actionLabel: "Prepare merge packet",
  status: "READY_FOR_HUMAN_APPLY",
  statusTone: "good",
  metrics: [{ value: "4", label: "requirements" }, { value: "4", label: "generated tests" }, { value: "0", label: "auto-applied changes" }],
  findings: [
    { title: "Requirement chain is traceable", detail: "Every test links to the transcript timestamp that justified it.", badge: "TRACEABLE", tone: "good" },
    { title: "CRLF regression is covered", detail: "Windows line endings are normalized before requirement parsing.", badge: "TEST", tone: "good" },
    { title: "Human apply gate preserved", detail: "The patch is prepared as a diff and is never merged automatically.", badge: "REVIEW", tone: "warn" },
  ],
  method: [
    { step: "01", title: "Extract", detail: "Identify explicit behaviors, boundaries, and owners with their timestamps." },
    { step: "02", title: "Test", detail: "Generate one focused assertion for each accepted requirement." },
    { step: "03", title: "Diff", detail: "Prepare only the lines needed to satisfy the tests and await review." },
  ],
  proof: ["Timestamp citations", "CRLF regression test", "Human-controlled apply"],
  note: "The transcript and patch are synthetic. The public demo never writes to a repository.",
};
