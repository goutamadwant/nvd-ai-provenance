# Contributing

VEPP is an early technical prototype intended for public evaluation. Focused
issues and pull requests are welcome for schema correctness, interoperability,
threat-model coverage, test vectors, and alignment with existing vulnerability
standards.

## Before Opening a Change

1. Search existing issues and pull requests for related work.
2. Keep the profile additive. Do not redefine CVE, NVD, CVSS, EPSS, KEV, CPE,
   PURL, CSAF/VEX, CycloneDX, SPDX, W3C PROV, in-toto, or SCITT semantics.
3. Use synthetic data only. Do not include unpublished vulnerability details,
   personal data, credentials, or proprietary material.
4. Add or update a test vector when behavior changes.
5. Run `make validate` and `make test`.

## Pull Requests

Describe the problem, the proposed behavior, standards affected, compatibility
considerations, and tests performed. Small, reviewable changes are preferred.

By contributing, you agree that your contribution is licensed under the MIT
License in this repository.
