# Security Policy — jolarca-dev Marketplace

**Effective Date:** 2026-09-26  
**Version:** 1.0  
**Owner:** JourneyOfLife (Security Officer)  
**Review Cycle:** Annual or after significant incident

---

## Supported Versions

The jolarca-dev marketplace organization consists of 14 repositories, all receiving security updates:

### Core Platform (Active)
| Repository | Purpose | Support Status |
|------------|---------|----------------|
| `jolarca` | Marketplace platform (payments, KYC/AML, VAT OSS) | ✅ Active |
| `jolarca-data` | Data pipelines, analytics, synthetic data | ✅ Active |
| `jolarca-infrastructure` | Terraform IaC, hosting, networking | ✅ Active |

### Governance & Compliance (Active)
| Repository | Purpose | Support Status |
|------------|---------|----------------|
| `jolarca-control` | Governance control plane (Terraform, policy) | ✅ Active |
| `jolarca-compliance` | RoPA, vendor assessments, audit evidence | ✅ Active |
| `jolarca-legal` | Contracts, DPAs, legal registers | ✅ Active |
| `jolarca-security` | Security policies, incident response, threat models | ✅ Active |

### Planned Components (Initialized, Not Yet Active)
| Repository | Purpose | Support Status |
|------------|---------|----------------|
| `jolarca-identity` | Identity and access management | ⏳ Planned |
| `jolarca-observability` | Monitoring, logging, tracing | ⏳ Planned |
| `jolarca-dr` | Disaster recovery, business continuity | ⏳ Planned |
| `jolarca-consent` | GDPR consent management | ⏳ Planned |
| `jolarca-docs` | Central documentation hub | ⏳ Planned |
| `jolarca-runbooks` | Operational runbooks | ⏳ Planned |
| `jolarca-vendor` | Vendor management, third-party risk | ⏳ Planned |

**Policy:** Security patches are applied immediately upon discovery for all active repositories. Planned repositories will receive the same treatment once they become operational.

---

## Reporting a Vulnerability

**⚠️ DO NOT open a public GitHub issue for security vulnerabilities.**

### How to Report

**Primary method:** Email security@jolarca.com (PGP-encrypted preferred)

**Alternative:** GitHub security advisories (when enabled — currently being configured)

**Note:** GitHub private vulnerability reporting is being enabled across all jolarca-dev repositories. Until complete, use email as the primary contact.

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

- **gitleaks:** Secret scanning (pre-commit)
- **Dependabot:** Dependency updates
- **Trivy:** Vulnerability scanning
- **CodeQL:** Semantic analysis
- **Branch protection:** Required checks, no force push

---

## Compliance

- SOC 2 CC7.3–CC7.5 (Incident management)
- ISO 27001 A.5.24–A.5.28 (Incident management)
- PCI DSS Req 6.3/12.10 (Security policies)
- GDPR Art. 32–33 (Security and breach notification)

---

## Contact

**Security Team:** security@jolarca.com  
**Security Officer:** JourneyOfLife

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-26 | JourneyOfLife | Initial version |
