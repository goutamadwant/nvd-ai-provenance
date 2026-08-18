# Contribution Status

## Current State

- Opportunity: `opp_5cd8505e839a5194`
- Federal Register document: `2026-16371`
- Regulations.gov docket: `NIST-2026-0100`
- Deadline: October 13, 2026 at 11:59 p.m. EDT (8:59 p.m. PDT)
- Package status: **prepared and verified; not submitted**
- External publication status: **published as a public draft**
- Public repository: https://github.com/goutamadwant/nvd-ai-provenance
- Author review decision: **approved for publication on August 16, 2026**
- Submission portal status: **available and accepting comments**

On August 17, 2026, Regulations.gov published document
`NIST-2026-0100-0001` under docket `NIST-2026-0100`. The official API reports
`openForComment: true`, a start time of `2026-08-17T04:00:00Z`, and an end time
of `2026-10-14T03:59:59Z`. The live submission form is:

https://www.regulations.gov/commenton/NIST-2026-0100-0001

## Verified Locally

- JSON Schema Draft 2020-12 meta-schema check passes.
- Two valid VEPP examples pass schema and semantic validation.
- Negative vectors fail with expected error codes.
- Full Standards Radar and companion suite: 29 tests pass.
- Ruff and mypy pass.
- PDF has seven searchable, nonblank pages and was visually inspected page by page.
- Companion ZIP excludes caches, tokens, databases, and machine-local paths.
- SHA-256 checksums verify for the PDF and ZIP.

## Remaining Submission Actions

1. Review the final PDF and complete the privacy checklist.
2. Open the verified direct comment URL above.
3. Paste the prepared cover text and upload the PDF only. The form does not
   accept ZIP attachments, so use the public repository for the companion files.
4. Complete reCAPTCHA and submit manually through Regulations.gov.
5. Save the tracking number and receipt, then record the outcome as `submitted` only.

Preparation is not submission, acknowledgement, adoption, citation, or evidence
of field-wide impact. Those states require separate public proof.
