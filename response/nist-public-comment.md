# Comment on NIST-2026-0100: Assertion-Level Provenance and Verifiable AI Enrichment for a Modernized NVD

**Federal Register document:** 2026-16371  
**Docket:** NIST-2026-0100  
**Submitted by:** Goutam Adwant  
**Capacity:** Individual; independent technical contribution  
**Date prepared:** August 16, 2026

## Executive Summary

I recommend that NIST modernize the National Vulnerability Database (NVD) by
making AI-assisted enrichment **traceable at the assertion level**, not merely
at the record level. Each affected-product mapping, weakness classification,
severity vector, exploit signal, priority recommendation, and remediation
should identify its producer, derivation method, supporting evidence, review
state, validity time where applicable, and revision history.

AI can reduce enrichment latency and increase coverage, but automation without
provenance can amplify source poisoning, product-matching errors, stale threat
signals, false confidence, and unsafe remediation. The goal should not be to
make an AI output appear authoritative. It should be to let producers,
analysts, tool vendors, and users determine what the output means, reproduce how
it was derived to the extent practicable, and apply policy based on evidence.

I propose an additive **Vulnerability Enrichment Provenance Profile (VEPP)** as
a pilot mechanism. The companion prototype includes a JSON Schema, validator,
positive and negative test vectors, standards crosswalk, threat model, and
synthetic examples. VEPP binds a sidecar to the exact source record by digest
and describes each enrichment assertion independently. It does not replace CVE,
the NVD API, NIST Vulntology, CVSS, EPSS, CISA KEV, CPE, Package-URL, CSAF/VEX,
CycloneDX, SPDX, W3C PROV, in-toto, or SCITT.

My recommendations are:

1. Publish provenance, evidence, confidence semantics, review state, and
   lifecycle metadata for each machine-generated or machine-transformed
   assertion.
2. Keep identity, technical severity, observed exploitation, predicted
   exploitation, product applicability, environmental risk, and remediation
   priority as separate typed signals.
3. Use AI first for candidate generation, normalization, deduplication, and
   evidence routing; retain risk-based human gates for authoritative product
   status, disputed analysis, and generated remediation.
4. Require calibrated probabilities or named assessment rubrics instead of
   accepting opaque model confidence scores.
5. Treat all external vulnerability content as untrusted input and prevent it
   from changing model instructions, tool permissions, or publication policy.
6. Preserve corrections through explicit supersession and retraction rather
   than silently overwriting history.
7. Pilot the profile as a backward-compatible sidecar with an open conformance
   suite before changing the core NVD API.
8. Measure user outcomes, calibration, corrections, and provenance coverage,
   not only ingestion volume or processing speed.

This response addresses RFI questions 1(b), 2(b), 3(a), 3(b), 3(d), 4(a), 4(b),
4(c), 5(a)-(e), 7(b), and 7(e).

## 1. Vulnerability Management Process

### Response to Question 1(b): Tasks for AI Automation and Human Review

NIST should use automation where outputs are bounded, independently checkable,
and reversible. Suitable tasks include:

- extracting candidate products, versions, references, and weakness terms from
  public source material;
- normalizing identifiers and validating CPE, PURL, CVE, CWE, and URL syntax;
- detecting duplicates, conflicting claims, stale references, and changed
  source documents;
- routing evidence to analysts and ranking records for review;
- generating candidate mappings or vectors that remain visibly distinct from
  verified NVD enrichment; and
- continuously re-evaluating dynamic signals while retaining observation times
  and source versions.

Human review should be risk-based rather than universal. A human gate is most
important when an assertion can materially change which users believe they are
affected, reduce apparent urgency, or cause code to be deployed. Examples are:

- authoritative affected or unaffected product/version status;
- novel or ambiguous CPE/PURL mappings;
- low-confidence or conflicting CWE and scenario classifications;
- a CVSS vector that differs materially from a vendor or CNA assessment;
- a decision to suppress or downgrade an existing assertion;
- disputed exploitation evidence; and
- all AI-generated remediation before it is presented as authoritative or
  deployed.

A reviewer needs the exact evidence used, source retrieval time and digest,
candidate value, derivation method, system/model version, applicable
calibration or rubric, conflicting assertions, and the consequences of
accepting or rejecting the candidate. Showing only a model summary encourages
automation bias. Review interfaces should expose evidence before or alongside
the recommendation and record whether the reviewer accepted, modified, or
rejected it.

NIST should sample even apparently successful automated classes. A low overall
error rate can conceal systematic failures affecting one vendor, language
ecosystem, or naming convention. Stratified review by ecosystem, source,
language, confidence range, and claim type is more informative than uniform
random sampling.

## 2. Vulnerability Information Dissemination

### Response to Question 2(b): Helpful Standards and Remaining Gaps

The ecosystem already has strong domain standards. CVE supplies vulnerability
identity and records. NVD enriches those records. CVSS describes technical
severity characteristics. CPE and PURL identify products and packages. CWE and
Vulntology describe weaknesses and exploitation scenarios. EPSS supplies a
time-varying exploitation probability. CISA KEV supplies authoritative observed
exploitation status. CSAF and VEX communicate advisories, product status, and
remediation. CycloneDX and SPDX connect these concepts to software components.
W3C PROV, in-toto, and SCITT provide reusable provenance, attestation, and
transparency concepts.

The gap is not another universal identifier or score. The practical gap is a
consistent way to answer, for each enrichment assertion:

- Who or what produced it?
- Was it copied, rule-derived, model-inferred, hybrid, or manually authored?
- Which exact evidence supported it?
- What does any confidence value mean, and how was it evaluated?
- Has it been machine checked or human verified?
- When was a dynamic claim observed, and when does it become stale?
- Has it been disputed, retracted, or replaced?
- Can a high-assurance consumer verify its integrity and history?

NVD API fields currently provide useful source/type attribution for several
objects. Modernization should preserve that compatibility and add finer
assertion-level provenance. A sidecar profile allows NIST to test this model
without forcing every consumer to migrate immediately.

## 3. Risk Assessment and Prioritization

### Response to Question 3(a): AI-Assisted Contextual Prioritization

AI can improve prioritization by joining heterogeneous evidence and identifying
records needing attention, but NIST should avoid publishing an opaque composite
"AI risk score." A useful prioritization view preserves at least these inputs:

- CVSS vector and score for technical severity;
- CISA KEV and other attributed observations for known exploitation;
- EPSS or another named/versioned model for predicted exploitation;
- affected-product and version confidence;
- CSAF/VEX product status and available remediation;
- exploit and remediation maturity;
- record freshness and unresolved conflicts; and
- consumer-supplied asset exposure, business criticality, compensating
  controls, and deployment context.

The final environment-specific priority belongs to the consuming organization
because NVD cannot know whether a vulnerable component is deployed, exposed,
reachable, safety-critical, or protected by compensating controls. NVD can
provide high-quality interoperable inputs and transparent reference policies.

AI-derived ranking should be evaluated using metrics appropriate to the task.
For rare exploitation outcomes, accuracy is misleading. Coverage/recall,
effort, precision, calibration, and cost-weighted errors are more useful. NIST
should also report performance by ecosystem and time period to reveal uneven
quality and drift.

### Response to Question 3(b): Transparency and Auditability

Transparency should be operational, not merely descriptive. Each assertion
should include:

- a stable assertion identifier;
- a claim type and reference to the standard defining its value;
- the producer and producer role;
- derivation method and system/model version;
- immutable evidence references with retrieval time and digest;
- confidence semantics, including calibration evidence or assessment rubric;
- review status, reviewer identity/role, and review time where applicable;
- observation and expiration time for dynamic claims; and
- active, superseded, or retracted lifecycle status with a reason and
  replacement link.

This metadata permits policy such as "accept vendor-provided remediation only
after human verification," "display machine-inferred CPEs as candidates," or
"ignore exploit probabilities older than a defined threshold." It also enables
historical reconstruction: a consumer can determine which evidence and model
version supported a decision at a prior time.

Numeric confidence deserves special treatment. A model's self-reported
confidence is not automatically a probability. If a score is labeled as a
probability, the producer should publish the calibration method, evaluation
dataset identity and digest, evaluation date, and metrics such as Brier score
or expected calibration error. A rubric-based score should identify the rubric
and must not be presented as calibrated probability. For authoritative imports,
"not applicable" is often more truthful than inventing a number.

The profile should not require chain-of-thought, private prompts, proprietary
weights, or confidential data. Evidence, method metadata, reproducible checks,
calibration, and concise rationale provide accountability without requiring
sensitive model internals.

### Response to Question 3(d): Interoperability

NIST should treat interoperability as both data compatibility and semantic
preservation. A CVSS base score must remain distinguishable from threat or
environmental context. An EPSS probability must retain its model version and
observation date. A KEV entry must remain an authoritative observation rather
than a model prediction. VEX product status must remain bound to a product and
document context.

I recommend a pilot endpoint or bulk sidecar feed keyed by CVE ID and source
record digest. Consumers should be able to filter by modified time, producer,
claim type, review status, and lifecycle state. Domain values should use their
native standard representation or reference it by URI and digest. Optional
in-toto/DSSE attestations or SCITT receipts can provide integrity and
transparency for consumers that require them.

## 4. Remediation Development, Deployment, and Monitoring

### Responses to Questions 4(a), 4(b), and 4(c)

AI can propose remediations, generate targeted tests, summarize changes, and
help locate equivalent fixes across branches. It should not directly publish or
deploy an authoritative remediation based only on plausibility.

An AI-generated remediation should pass a verifiable release gate:

1. Bind the proposal to exact source, dependency, build, and vulnerability
   evidence.
2. Build in an isolated, least-privilege environment without production
   credentials.
3. Run existing tests plus targeted tests that reproduce the vulnerable
   behavior and verify the fix.
4. Run applicable static, dependency, secret, policy, and compatibility checks.
5. Produce provenance for the patch, build, test results, and tools used.
6. Require a qualified human to review both the change and the evidence.
7. Use staged deployment, monitoring, explicit rollback criteria, and a tested
   rollback mechanism.
8. Feed failures and regressions into future evaluation sets.

Roles should be separated where practical: generator, verifier, approver, and
deployer. The same AI system should not both generate a patch and serve as the
sole verifier. NIST should publish minimum evidence expectations for remediation
claims and allow CSAF/VEX or other established advisory formats to carry the
domain content while provenance/attestation mechanisms carry verification
evidence.

External advisories, repositories, issues, and exploit reports must be treated
as untrusted input. A document can contain instructions intended to manipulate
an AI pipeline. Retrieved content must not be able to change system
instructions, tool permissions, publication thresholds, or review policy.
Other required controls include source authentication, input size/depth limits,
model and configuration versioning, drift monitoring, data classification,
coordinated-disclosure checks, and append-only correction history.

## 5. Vulnerability Data and Standards

### Responses to Questions 5(a)-(e)

NIST should improve machine-readable vulnerability data through five related
changes.

**First, publish assertion-level provenance.** Record-level attribution is not
sufficient when fields are assembled from multiple sources and methods. The
metadata should be structured and queryable, not only embedded in analyst prose.

**Second, support multiple product identifiers with explicit mapping
provenance.** CPE remains essential for NVD and SCAP, while PURL is often a more
precise fit for package ecosystems and SBOMs. A record may need both, plus vendor
identifiers and version ranges. Each mapping should identify evidence, method,
confidence semantics, review state, and mapping version.

**Third, make dynamic data explicitly temporal.** Exploit probability, exploit
activity, priority, remediation availability, and product status can change.
Records should carry observation time, source update time, and optional
expiration/freshness policy. Consumers should be able to reconstruct historical
state rather than receiving only the latest overwritten value.

**Fourth, publish an open conformance suite.** JSON Schema validation is
necessary but insufficient. Test vectors should cover conflicting sources,
supersession, retraction, invalid product identifiers, ambiguous version
ranges, stale dynamic signals, model-version changes, calibration failures, and
mixed human/machine review states. The suite should include positive and
negative cases with expected outcomes.

**Fifth, preserve uncertainty without conflating it with severity or risk.** A
confidence score about a product mapping is not CVSS. EPSS is not an
organization's complete risk. KEV is not a prediction. A machine-generated
priority is not an observed fact. Typed assertions and explicit semantics let
tools combine these values without erasing their meaning.

The companion VEPP prototype demonstrates these recommendations as an additive
JSON Schema and validator. It intentionally leaves CVE identity, NVD transport,
Vulntology scenarios, CVSS vectors, EPSS probabilities, KEV status, CPE/PURL
identifiers, and CSAF/VEX remediation in their existing standards.

## 7. Vision for the NVD

### Response to Question 7(b): Five-Year Capabilities

Over five years, a modernized NVD should provide:

- near-real-time candidate enrichment with visible machine/human status;
- assertion-level evidence and provenance APIs;
- historical, versioned records and correction chains;
- interoperable product identifiers and source-preserving crosswalks;
- independently testable conformance profiles;
- calibration and drift reports for automated systems;
- transparent service and data-quality metrics;
- optional signed attestations or transparency receipts; and
- feedback channels for evidence-backed corrections from vendors, CNAs, tool
  providers, researchers, and users.

I recommend a staged rollout:

1. **Inventory:** document current sources, transformations, review states, and
   fields where provenance is lost.
2. **Sidecar pilot:** publish profiles for affected-product mappings and CWE
   classifications over a stratified sample while leaving existing API
   responses unchanged.
3. **Evaluation:** use blinded adjudication to measure automated candidates,
   human review, disagreements, latency, and calibration.
4. **Conformance:** publish schemas, test vectors, validator behavior, and
   producer/consumer implementation guidance.
5. **Integration:** promote proven fields into versioned APIs while retaining
   sidecar compatibility and historical evidence.

### Response to Question 7(e): Success Metrics

NIST should publish metrics in four groups.

**Service metrics:** P50/P95 time from CVE publication to candidate and verified
enrichment; API/feed availability and schema compatibility; backlog by age,
ecosystem, and enrichment class.

**Data-quality metrics:** provenance/evidence coverage by claim type;
adjudicated precision/recall for product and weakness mappings; inter-provider
agreement and unresolved conflicts; correction latency and supersession
completeness; stale dynamic-assertion rate.

**Automation metrics:** human acceptance, modification, and rejection by
confidence range; calibration and drift by model version and ecosystem;
coverage/recall, effort, precision, and cost-weighted error; automation
incidents, policy violations, and rollback outcomes.

**User-outcome metrics:** time to determine applicability; time from actionable
information to verified remediation; reduction in false-positive remediation
work without loss of exploited-vulnerability coverage; adoption of
machine-readable provenance by tools and data providers.

Counts of records processed, model calls, or fields populated are operational
inputs, not sufficient measures of cybersecurity impact.

## Companion Prototype

The attached companion package contains:

- VEPP JSON Schema Draft 2020-12;
- a standalone schema and semantic validator;
- valid synthetic AI-assisted and human-verified examples;
- negative vectors for missing calibration, missing dynamic validity time, and
  cyclic supersession;
- a standards crosswalk;
- a threat model and remediation release gate; and
- a question-to-artifact traceability matrix.

The prototype is intentionally small enough to evaluate and revise. A useful
next step would be a public pilot with NVD analysts, CNAs, vendors, FIRST/CVSS
and EPSS participants, CISA, SBOM/VEX communities, tool providers, and academic
or independent researchers.

## Conclusion

NVD modernization should increase speed without making provenance and human
accountability disappear. AI-assisted enrichment will be most useful when each
claim remains attributable, evidence-backed, semantically distinct,
time-aware, reviewable, and reversible. An additive assertion-level provenance
profile and open conformance pilot provide a practical way to test that model
without disrupting existing NVD consumers.

Thank you for the opportunity to comment.

Goutam Adwant  
https://www.goutamadwant.com  
https://github.com/goutamadwant

## References

1. NIST, Federal Register document 2026-16371:
   https://www.federalregister.gov/d/2026-16371
2. NIST, NVD general information: https://nvd.nist.gov/General
3. NIST, NVD CVE API 2.0: https://nvd.nist.gov/developers/vulnerabilities
4. NIST, NVD Source API: https://nvd.nist.gov/developers/data-sources
5. NIST, Vulntology: https://pages.nist.gov/vulntology/
6. CVE Program, CVE Record Format: https://cveproject.github.io/cve-schema/
7. FIRST, CVSS v4.0: https://www.first.org/cvss/v4.0/
8. FIRST, Exploit Prediction Scoring System: https://www.first.org/epss/
9. CISA, Known Exploited Vulnerabilities Catalog:
   https://www.cisa.gov/known-exploited-vulnerabilities-catalog
10. NISTIR 7695, CPE Naming Specification 2.3:
    https://doi.org/10.6028/NIST.IR.7695
11. Package-URL Specification / ECMA-427:
    https://github.com/package-url/purl-spec
12. OASIS, CSAF 2.0:
    https://docs.oasis-open.org/csaf/csaf/v2.0/cs03/csaf-v2.0-cs03.html
13. CycloneDX, Vulnerability Exploitability eXchange:
    https://www.cyclonedx.org/capabilities/vex/
14. W3C, PROV-O: https://www.w3.org/TR/prov-o/
15. in-toto, Statement v1:
    https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md
16. IETF, RFC 9943, SCITT Architecture:
    https://www.rfc-editor.org/rfc/rfc9943.html
17. NIST AI 600-1, Generative AI Profile:
    https://doi.org/10.6028/NIST.AI.600-1
