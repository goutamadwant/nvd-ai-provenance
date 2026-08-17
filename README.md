# NIST NVD AI Modernization Response Package

[![CI](https://github.com/goutamadwant/nvd-ai-provenance/actions/workflows/ci.yml/badge.svg)](https://github.com/goutamadwant/nvd-ai-provenance/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository is a review-ready response package for Federal Register
document `2026-16371`, prepared for submission through Regulations.gov docket
`NIST-2026-0100`.

**Public repository:** https://github.com/goutamadwant/nvd-ai-provenance

The package proposes the Vulnerability Enrichment Provenance Profile (VEPP), an
additive, machine-readable sidecar for recording how individual vulnerability
assertions were produced, what evidence supports them, how confidence was
derived, whether a human reviewed them, and how they changed over time.

VEPP is a prototype for public discussion. It is not a NIST specification, does
not imply NIST endorsement, and does not replace CVE, the NVD API, Vulntology,
CVSS, EPSS, KEV, CSAF, VEX, CycloneDX, SPDX, CPE, or PURL.

## Package Contents

- `response/nist-public-comment.md`: the proposed public comment.
- `response/submission-form.md`: exact Regulations.gov metadata and upload plan.
- `response/review-checklist.md`: final privacy, accuracy, and submission checks.
- `docs/technical-proposal.md`: the VEPP architecture and rollout proposal.
- `docs/crosswalk.md`: relationship to existing vulnerability standards.
- `docs/threat-model.md`: misuse cases and safeguards.
- `schema/vepp.schema.json`: JSON Schema Draft 2020-12 profile.
- `validator/vepp_validator.py`: schema and semantic validator.
- `examples/`: valid synthetic examples.
- `test-vectors/`: expected-validity manifest and negative cases.
- `research/source-register.md`: authoritative sources and retrieval record.
- `research/rfi-question-traceability.md`: RFI-to-recommendation mapping.
- `CITATION.cff`: citation metadata for attribution and reuse.
- `CONTRIBUTING.md`: contribution scope and validation expectations.
- `.github/workflows/ci.yml`: clean-environment validation on supported Python versions.

## Validate

From this directory:

```bash
python3 -m pip install -r requirements.txt
make validate
make test
```

All example CVEs, vendors, people, systems, and digests are synthetic. They are
test fixtures, not vulnerability intelligence.

## Submission Boundary

Nothing in this repository has been submitted to NIST. The final action remains manual
because Regulations.gov publishes comments without change or redaction. The
review checklist must be completed before upload.

As of August 16, 2026, the Federal Register notice directs commenters to docket
`NIST-2026-0100`, but that docket and document are not yet present in the
Regulations.gov search interface or API. Do not submit through a different
docket. See `STATUS.md` and `response/submission-form.md` for the verification
gate.

## License

MIT. See `LICENSE`.
