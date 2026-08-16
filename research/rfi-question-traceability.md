# RFI Question Traceability

| RFI question | Response position | Companion evidence |
| --- | --- | --- |
| 1(b): automation versus human review | Use automation for candidate generation, normalization, deduplication, and deterministic validation; retain human gates for authoritative product status, disputed classifications, and remediation | Technical proposal: AI and Hybrid Enrichment Controls; threat model |
| 2(b): standards and gaps | Reuse CVE, CVSS, CPE/PURL, CSAF/VEX, CycloneDX/SPDX, W3C PROV, in-toto, and SCITT; fill the assertion-level provenance and review gap | Crosswalk; VEPP schema |
| 3(a): contextual prioritization inputs | Keep severity, exploit probability, observed exploitation, applicability, asset context, and policy separate | Crosswalk: Separation of Signals |
| 3(b): transparency and auditability | Bind each assertion to evidence, method/model version, calibration, review, time, and lifecycle | Schema; validator; examples |
| 3(d): interoperability | Publish additive sidecars and standard references; do not force a breaking NVD API migration | Technical proposal: Pilot Architecture |
| 4(a): mechanisms for automated remediation | Require machine-readable remediation plus isolated, deterministic verification and provenance | Threat model: Remediation Release Gate |
| 4(b): organizational processes | Separate generator, verifier, approver, and deployer roles; retain evidence and rollback | Threat model |
| 4(c): safeguards | Sandbox, least privilege, targeted tests, attestations, human approval, staged rollout | Threat model |
| 5(a)-(e): data and standards | Add assertion provenance, product-identifier crosswalks, validity time, revision history, and conformance tests | VEPP schema; crosswalk; test vectors |
| 7(b): five-year capabilities | Versioned provenance endpoint, historical reconstruction, conformance suite, transparent metrics | Technical proposal: Pilot Architecture |
| 7(e): metrics | Measure latency, coverage, calibration, corrections, agreement, freshness, compatibility, and consumer outcomes | Technical proposal: Metrics |

## Artifact-to-Claim Traceability

- Claim that the proposal is machine-readable: JSON Schema and valid examples.
- Claim that it is testable: validator, manifest, positive vectors, and negative
  vectors with expected error codes.
- Claim that it is backward-compatible: source-record sidecar binding and no
  modifications to the NVD API schema.
- Claim that it avoids redefining domain standards: standards crosswalk and
  `standardRefs` fields.
- Claim that it supports accountable AI: method/model metadata, evidence
  digests, confidence semantics, review state, lifecycle, and threat model.
