# Threat Model and Safeguards

## Scope

This threat model covers AI-assisted vulnerability ingestion, enrichment,
prioritization, and remediation. It assumes external advisories, repositories,
issue text, exploit reports, and model outputs may be malicious or incorrect.

| Threat | Failure mode | Minimum safeguard | Evidence to retain |
| --- | --- | --- | --- |
| Source poisoning | Forged or compromised advisory causes false affected-product or remediation data | Source authentication, allowlists appropriate to claim type, content digest, multi-source corroboration for high-impact changes | Source bytes/digest, retrieval time, identity validation result |
| Prompt or instruction injection | Text in an advisory tells an AI pipeline to ignore policy or invoke tools | Treat retrieved content as data; isolate instructions from evidence; fixed tool policy; no publication permission in the model context | Sanitized input, policy version, tool decision log |
| Model drift | Accuracy or calibration degrades after ecosystem changes | Versioned model, held-out evaluation, drift thresholds, rollback | Model/config digest, calibration dataset, metrics over time |
| Hallucinated product mapping | Model invents a CPE, PURL, or affected version range | Deterministic syntax/resolution checks; evidence span; human gate before authoritative status | Candidate, resolver result, reviewer decision |
| False confidence | Uncalibrated score is presented as probability | Require calibration metadata for probabilities and a named rubric for assessments | Calibration method, dataset digest, Brier/ECE or rubric version |
| Automation bias | Reviewer accepts output without meaningful inspection | Blind or counterfactual sampling, conflict surfacing, review UI that shows evidence before recommendation | Review duration, evidence viewed, override outcome |
| Cross-source conflation | Severity, exploitation, applicability, and priority are collapsed into one opaque score | Preserve separate typed assertions and source semantics | Individual inputs and policy transformation |
| Stale threat signal | EPSS, KEV, or exploit data is used outside its observation context | Observation/expiration time, freshness policy, historical retention | Source timestamp, ingestion time, expiration decision |
| History rewriting | Incorrect output is silently replaced | Append-only revisions, explicit supersession/retraction, optional transparency receipt | Old/new assertion IDs, reason, actor, timestamp |
| Unsafe generated remediation | Plausible patch introduces regression, backdoor, or data loss | Isolated build/test, deterministic regression and security tests, provenance attestation, human approval, staged rollout and rollback | Patch digest, build provenance, test report, reviewer, deployment outcome |
| Sensitive data leakage | Private vulnerability or environment data reaches a public model/feed | Data classification, least-privilege retrieval, redaction, approved model boundary | Classification result and disclosure decision |
| Exploit enablement | Enrichment publishes operational details that materially increase attacker capability | Tiered disclosure, coordinated disclosure checks, minimize exploit detail not needed for defense | Disclosure policy decision and reviewer |
| Denial of service | Adversarial volume or recursive content exhausts enrichment resources | Size/depth limits, rate limits, quotas, timeouts, bounded decompression and parsing | Rejection reason and resource metrics |

## Remediation Release Gate

An AI-generated remediation should not become authoritative or deployable until
all applicable gates pass:

1. The vulnerable behavior is reproduced or otherwise evidenced.
2. The proposed change is bound to exact source and dependency revisions.
3. Builds run in an isolated, least-privilege environment.
4. Existing tests and targeted regression/security tests pass.
5. Static, dependency, secret, and policy checks pass where applicable.
6. The patch and test results receive provenance attestations.
7. A qualified human approves the change and evidence.
8. Deployment is staged, monitored, and reversible.
9. Post-deployment regressions feed back into the evaluation set.

The profile records the evidence for these controls but does not itself execute
or certify them.
