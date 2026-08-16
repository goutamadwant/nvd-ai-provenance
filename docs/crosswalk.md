# Standards Crosswalk

VEPP is an evidence layer, not a replacement for the formats below.

| Ecosystem | Existing responsibility | VEPP relationship |
| --- | --- | --- |
| CVE Record Format | Vulnerability identity and CNA/ADP record structure | Binds a provenance sidecar to a CVE and may reference exact CVE record bytes as evidence. |
| NVD CVE API 2.0 | NVD enrichment, API transport, source/type metadata | Adds assertion-level method, evidence, confidence, review, validity, and lifecycle metadata without changing the base response. |
| NIST Vulntology | Structured vulnerability scenarios and characterization | References Vulntology elements as assertion values; does not redefine vulnerability semantics. |
| CPE 2.3 | Platform naming and matching | Carries CPE values inside affected-product assertions and records how the mapping was derived. |
| Package-URL / ECMA-427 | Package identity across ecosystems | Carries PURLs alongside or instead of CPE when package coordinates are the clearer identifier. |
| CVSS 4.0 | Technical severity characteristics | Records the source and derivation of a CVSS assertion; never treats CVSS as complete organizational risk. |
| EPSS | Calibrated probability of observed exploitation in the next 30 days | Imports score, percentile, model version, and observation date as a time-varying source assertion. |
| CISA KEV | Authoritative catalog of vulnerabilities exploited in the wild | Imports KEV status as an authoritative threat signal, distinct from model confidence or severity. |
| CSAF 2.0 / VEX | Structured advisories, product status, and remediation | References CSAF/VEX fields and documents as evidence for affected status and remediation. |
| CycloneDX VEX | Product-context exploitability in CycloneDX BOMs | Preserves the VEX assertion and product context while adding derivation and review metadata. |
| SPDX | SBOM components and external identifiers | Uses SPDX/PURL/CPE identifiers to connect vulnerability assertions to software components. |
| W3C PROV | General provenance concepts and interchange model | VEPP producer, evidence, derivation, and revision concepts can map to PROV Agent, Entity, Activity, and derivation relations. |
| in-toto Attestation | Digest-bound, typed software-supply-chain claims | A VEPP document can be referenced or carried as an in-toto predicate and protected by DSSE. |
| SCITT / RFC 9943 | Transparent, receipt-backed digital supply-chain statements | A VEPP document can reference a SCITT receipt for append-only transparency and independent verification. |

## Separation of Signals

A modernized NVD should expose inputs without silently collapsing them:

- **Identity:** CVE.
- **Affected product:** CPE, PURL, vendor product identifiers, and version ranges.
- **Weakness/scenario:** CWE and Vulntology.
- **Technical severity:** CVSS vector and score.
- **Observed exploitation:** CISA KEV and other attributed observations.
- **Predicted exploitation:** EPSS or another identified, versioned model.
- **Product-specific status:** CSAF/VEX or CycloneDX VEX.
- **Environment-specific risk and priority:** consumer asset context and policy.
- **Provenance and review:** VEPP.

Keeping these dimensions separate prevents a model-generated priority from
being mistaken for an authoritative fact or a CVSS base score from being
treated as complete operational risk.
