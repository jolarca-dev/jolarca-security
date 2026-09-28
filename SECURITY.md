# Security Policy — jolarca-dev Marketplace

**Effective Date:** 2026-09-26
**Version:** 1.0
**Owner:** JourneyOfLife (Security Officer)
**Review Cycle:** Annual or after significant incident

---

## Supported Versions

The jolarca-dev marketplace organization consists of 16 repositories. Visibility
and content status were verified through the GitHub API on 2026-09-28.

### Core Platform (Active)

| Repository | Purpose | Visibility | Support Status |
|------------|---------|------------|----------------|
| `jolarca` | Marketplace platform (payments, KYC/AML, VAT OSS) | Public | ✅ Active |
| `jolarca-payments` | Payment processing components | Public | ✅ Active |
| `jolarca-data` | Data pipelines, analytics, synthetic data | Private | ✅ Active |
| `jolarca-infrastructure` | Terraform IaC, hosting, networking | Private | ✅ Active |

`jolarca-payments` is in PCI DSS scope and must never be treated as optional in
a security review. It was missing from this table until the 2026-09-28 audit.

### Governance & Compliance (Active)

| Repository | Purpose | Visibility | Support Status |
|------------|---------|------------|----------------|
| `jolarca-control` | Governance control plane (Terraform, policy) | Public | ✅ Active |
| `jolarca-compliance` | RoPA, vendor assessments, audit evidence | Private | ✅ Active |
| `jolarca-legal` | Contracts, DPAs, legal registers | Private | ✅ Active |
| `jolarca-security` | Security policies, incident response, threat models | Private | ✅ Active |
| `.github` | Organization profile and community health files | Public | ✅ Active |

`jolarca-control` is a governance control plane and is currently public. That is
threat model entry D-01 (confidential material published by visibility error)
and is flagged for owner review.

### Planned Components (Initialized, Not Yet Active)

| Repository | Purpose | Visibility | Support Status |
|------------|---------|------------|----------------|
| `jolarca-identity` | Identity and access management | Public | ⏳ Planned |
| `jolarca-observability` | Monitoring, logging, tracing | Private | ⏳ Planned |
| `jolarca-dr` | Disaster recovery, business continuity | Public | ⏳ Planned |
| `jolarca-consent` | GDPR consent management | Public | ⏳ Planned |
| `jolarca-docs` | Central documentation hub | Public | ⏳ Planned |
| `jolarca-runbooks` | Operational runbooks | Public | ⏳ Planned |
| `jolarca-vendor` | Vendor management, third-party risk | Public | ⏳ Planned |

`jolarca-identity` and `jolarca-consent` are public and already contain content,
so their "Planned" classification needs re-verification by the owner. A GDPR
consent repository that is publicly readable should be reviewed deliberately
rather than by default.

**Policy:** Security patches are applied immediately upon discovery for all active repositories. Planned repositories will receive the same treatment once they become operational.

---

## Reporting a Vulnerability

**⚠️ DO NOT open a public GitHub issue for security vulnerabilities.**

### How to Report

**Primary method:** GitHub private vulnerability reporting on the public
repository [jolarca-dev/jolarca](https://github.com/jolarca-dev/jolarca/security/advisories/new).
This channel was verified enabled on 2026-09-28 and reaches the Security Officer
directly without exposing the report publicly.

**Email — currently NOT deliverable:** `security@jolarca.com` is published as a
contact address across this repository, but the domain `jolarca.com` resolves to
parking nameservers (`orbit.dns-parking.com`, `dns.hostinger.com`) and has **no
MX records**. Mail sent to that address is discarded, so it must not be relied
upon until MX records and the mailbox are provisioned. Until then, use the
GitHub channel above.

**Why private vulnerability reporting is not available on this repository:** the
feature is free for public repositories only. For a private repository it
requires GitHub Advanced Security, and the API returns HTTP 404 here. It was
therefore enabled on the public `jolarca` repository instead, which is recorded
as a compensating control in
[policies/control-matrix.yml](policies/control-matrix.yml).

### What to Include

- **Description:** Clear explanation of the vulnerability
- **Impact:** What an attacker could achieve
- **Steps to reproduce:** Minimal steps to demonstrate
- **Affected component:** Repository, service, or infrastructure
- **Suggested fix:** (if known)

### Severity Classification (CVSS v3.1)

| Severity | CVSS Score | Response Time |
|----------|------------|---------------|
| Critical | 9.0–10.0 | 24 hours |
| High | 7.0–8.9 | 48 hours |
| Medium | 4.0–6.9 | 5 business days |
| Low | 0.1–3.9 | Next release |

### Response Timeline

| Severity | Initial Response | Resolution Target |
|----------|------------------|-------------------|
| Critical | 24 hours | 7 days |
| High | 48 hours | 14 days |
| Medium | 5 business days | 30 days |
| Low | 10 business days | Next release |

---

## Disclosure Policy

### Coordinated Disclosure

1. Reporter submits vulnerability privately
2. Security team validates and classifies
3. Engineering develops fix
4. Fix deployed to production
5. Public disclosure after 30 days

### Safe Harbor

We will not take legal action against researchers who report in good faith, do not access/modify/delete data without authorization, and do not perform DoS attacks.

---

## Security Controls

The authoritative, machine-checked inventory of controls for this repository is
[policies/control-matrix.yml](policies/control-matrix.yml). The rendered summary
lives in [README.md — Security Controls, Verified State](README.md).

Controls are **not** uniform across the organisation. They depend on repository
visibility and on the GitHub plan, so this policy deliberately does not assert
fleet-wide enforcement. Verified differences as of 2026-09-28:

- `jolarca` (public) has branch protection with required status checks that
  include `codeql`, `trivy`, `gitleaks` and `secrets`.
- `jolarca-control` (public) has **no** branch protection.
- `jolarca-security` (this repository, private) **cannot** have branch
  protection, secret scanning, push protection or CodeQL on the GitHub Free
  plan. Compensating controls are documented in the control matrix.

Do not copy a control list between repositories without verifying it against the
target repository first.

---

## Compliance

- SOC 2 CC7.3–CC7.5 (Incident management)
- ISO 27001 A.5.24–A.5.28 (Incident management)
- PCI DSS Req 6.3/12.10 (Security policies)
- GDPR Art. 32–33 (Security and breach notification)

---

## Contact

**Security Officer:** JourneyOfLife (owner of the jolarca-dev organisation)

**Report vulnerabilities:** GitHub private vulnerability reporting on
[jolarca-dev/jolarca](https://github.com/jolarca-dev/jolarca/security/advisories/new)
— see [Reporting a Vulnerability](#reporting-a-vulnerability). The published
address `security@jolarca.com` is not currently deliverable.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-26 | JourneyOfLife | Initial version |
| 1.1 | 2026-09-28 | JourneyOfLife | Readiness audit: corrected repository count to 16, added `jolarca-payments` and `.github`, added verified visibility column, replaced non-deliverable email disclosure channel with GitHub private vulnerability reporting, replaced unscoped control list with the control matrix |
