# Vulnerability Enrichment Provenance Profile (VEPP)

Version: 0.1.0-draft  
Status: Technical companion prototype for NIST RFI `2026-16371`  
Author: Goutam Adwant  
Date: August 16, 2026

## Abstract

AI can help scale vulnerability enrichment, but a consumer should not have to
trust an opaque label simply because it appears in an authoritative feed. VEPP
is an additive sidecar profile that records provenance at the assertion level:
who or what produced a claim, the method and model version used, immutable
evidence references, confidence semantics, review state, validity time, and
revision history. It binds those assertions to the exact source record by
digest and can reference an in-toto/DSSE attestation or SCITT receipt.

VEPP does not define vulnerability identity, product naming, severity,
exploitability, or remediation semantics. Existing standards continue to own
those domains. The profile only supplies a common evidence and accountability
layer that can travel with enrichment produced by NIST, CVE Numbering
Authorities, vendors, data providers, and automated systems.

## Problem

The NVD API identifies sources for several enrichment objects, but AI-era
automation creates more granular questions:

- Was a particular affected-product assertion copied, rule-derived, inferred by
  a model, or approved by a human?
- Which exact source bytes and model version produced it?
- Does a numeric confidence represent a calibrated probability, a rubric-based
  assessment, or merely an ungrounded model score?
- When was a dynamic assertion observed, and when should it be treated as
  stale?
- What replaced an incorrect assertion, and can a consumer reconstruct the
  decision available at a prior point in time?
- Can high-assurance consumers verify integrity without requiring every NVD
  client to adopt a new signing format?

Record-level attribution cannot fully answer these questions when one record
combines assertions from multiple sources and methods.

## Design Principles

1. **Additive deployment.** VEPP is a sidecar bound to an existing record. It
   does not require a breaking NVD API change.
2. **Assertion-level granularity.** Provenance belongs to the specific claim,
   not only to the containing CVE record.
3. **Separate concepts.** Producer identity, derivation method, confidence,
   review status, and lifecycle are distinct fields.
4. **Evidence before explanation.** Every assertion references retrievable
   evidence and a SHA-256 digest. Free-form rationale is supplemental.
5. **No false precision.** Numeric confidence is permitted only with a stated
   calibration method or assessment rubric. Authoritative imported facts may
   use `not_applicable` instead of manufacturing a score.
6. **Time-aware signals.** Exploit activity, exploit probability, and priority
   claims carry observation and optional expiration times.
7. **Reversible automation.** Supersession and retraction remain visible.
8. **Standards reuse.** The profile references CVE, CPE/PURL, CVSS, EPSS, KEV,
   CSAF/VEX, CycloneDX, SPDX, and Vulntology rather than redefining them.
9. **Optional cryptographic transparency.** Implementations can attach in-toto
   DSSE attestations or SCITT receipts without making signing mandatory for all
   producers during an initial pilot.
10. **No sensitive reasoning requirement.** The profile records evidence,
    method metadata, calibration, and a concise rationale. It does not require
    private model prompts, hidden chain-of-thought, proprietary weights, or
    confidential data.

## Information Model

### Root document

| Field | Purpose |
| --- | --- |
| `profileVersion` | Version of the additive profile. |
| `documentId` | Globally unique URI for this sidecar document. |
| `target` | CVE identifier and digest-bound source record. |
| `generatedAt` | Profile generation time. |
| `assertions` | One or more independently attributable claims. |
| `attestation` | Optional integrity/transparency reference. |

### Assertion

| Field | Purpose |
| --- | --- |
| `id` | Stable identifier within the profile document. |
| `claimType` | Affected product, severity, weakness, exploit signal, priority, remediation, reference, or description. |
| `value` | Domain value encoded by the referenced standard. |
| `targetPaths` | Optional JSON Pointers to affected NVD fields. |
| `standardRefs` | Specifications that define the value semantics. |
| `producer` | Person, organization, or software agent responsible for the assertion. |
| `method` | Manual, rules, AI, hybrid, or imported derivation, plus system/model version where relevant. |
| `evidence` | Immutable references to supporting material. |
| `confidence` | Calibrated probability, assessed confidence, or not applicable. |
| `review` | Unreviewed, machine checked, human verified, disputed, or rejected. |
| `validTime` | Observation and optional expiry for dynamic claims. |
| `lifecycle` | Active, superseded, or retracted, with replacement linkage. |
| `createdAt` | Assertion creation time. |

## Confidence Semantics

VEPP deliberately avoids a single universal confidence field.

`calibrated_probability` means the value has an empirical interpretation. The
record includes the calibration method, a digest-bound evaluation dataset, the
evaluation date, and one or more metrics such as Brier score or expected
calibration error.

`assessed_confidence` is a bounded score produced under a named rubric. It is
not presented as a probability. The rubric must make the score reproducible
enough for independent review.

`not_applicable` is appropriate when a producer is relaying an authoritative
statement or when assigning a numeric score would mislead consumers.

These values describe confidence in the assertion, not vulnerability severity,
likelihood of exploitation, business impact, or remediation priority. CVSS,
EPSS, KEV, environmental context, and organization policy remain separate.

## AI and Hybrid Enrichment Controls

An AI or hybrid assertion identifies the system name and version. A model ID,
model digest, and parameters digest are available when disclosure and technical
architecture permit. Every assertion references the evidence actually used,
not only a search page or mutable landing page.

Recommended publication gates:

| Assertion class | Default automation | Human gate |
| --- | --- | --- |
| Reference tagging and deduplication | Publish after deterministic checks | Sampled audit |
| Candidate CPE/PURL mapping | Publish as machine-inferred candidate | Required before authoritative affected-product status |
| CWE or scenario classification | Publish with calibrated confidence | Required for low-confidence or conflicting sources |
| CVSS vector candidate | Keep distinct from official score | Required before primary-source publication |
| Exploit probability import | Publish with source, model version, and observation time | Not required for faithful import |
| KEV status import | Publish only from authoritative CISA data | Not required for faithful import |
| Remediation generation | Never publish directly as authoritative | Required after isolated verification |

All external text should be treated as untrusted data. Advisory content must not
be allowed to alter system instructions, tool permissions, publication rules,
or review thresholds.

## Conformance Levels

### Level 1: Traceable

- Valid JSON Schema document.
- Digest-bound source record and evidence for every assertion.
- Producer, method, review, confidence, and lifecycle fields present.
- Dynamic claims include observation time.

### Level 2: Reproducible

- AI/rules system version and relevant configuration digest are present.
- Numeric confidence includes calibration evidence or a versioned rubric.
- Replacement chains are complete and acyclic.
- Domain values validate against their referenced standards.

### Level 3: Verifiable

- The profile or referenced evidence is signed or transparency-logged.
- Verification policy identifies trusted producers and acceptable review states.
- Historical versions and receipts support independent reconstruction.

The included validator implements core Level 1 checks and selected Level 2
semantic checks. It does not resolve remote evidence or validate domain-specific
CVSS, CPE, PURL, CSAF, or VEX values.

## Pilot Architecture

1. Select two high-value enrichment classes: affected-product mappings and CWE
   classifications.
2. Publish VEPP sidecars for a stratified sample while leaving the NVD CVE API
   response unchanged.
3. Invite NVD analysts, CNAs, vendors, tool providers, and researchers to
   generate and consume the profile.
4. Compare human and automated decisions using a blinded adjudication set.
5. Publish calibration, disagreement, correction, latency, and provenance
   coverage metrics.
6. Revise the profile before considering first-class API integration.

The sidecar approach enables opt-in experimentation, independent caches, and
rollback. A profile endpoint could later support requests by CVE ID, modified
time, producer, claim type, and review status.

## Metrics

- Assertion provenance coverage by claim type.
- Evidence digest and retrievability coverage.
- P50/P95 time from CVE publication to candidate and verified enrichment.
- Human acceptance, modification, and rejection rates for machine candidates.
- Correction latency and supersession completeness.
- Inter-provider agreement and adjudicated precision/recall for product and CWE
  mappings.
- Brier score, expected calibration error, coverage, effort, and drift for
  probabilistic outputs where those metrics are appropriate.
- Stale dynamic-assertion rate.
- Backward-compatibility and schema-validation failure rates.
- Remediation test-pass, rollback, and post-deployment regression rates.
- Consumer outcomes measured separately from feed activity, including time to
  identify applicable vulnerabilities and time to a verified remediation.

## Open Questions for a Pilot

1. Which enrichment assertions justify public evidence snapshots when source
   material is mutable, licensed, or safety-sensitive?
2. Should producer identity use organizational URIs, CVE source identifiers, or
   a dedicated registry?
3. Which claim types should require human verification before appearing in the
   primary NVD record?
4. What retention period is needed to reconstruct historical prioritization
   decisions?
5. Which transparency mechanism best fits NVD scale and public-sector
   operational requirements?

## Non-Goals

VEPP does not create a new vulnerability identifier, universal risk score,
product naming scheme, vulnerability ontology, advisory format, SBOM format, or
signature protocol. It does not assert that AI should replace NVD analysts. It
does not make a model's output trustworthy merely because metadata is present;
trust remains a policy decision supported by evidence, review, calibration, and
independent evaluation.
