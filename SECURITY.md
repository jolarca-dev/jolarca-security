# Security Policy — jolarca-dev Marketplace

**Effective Date:** 2026-09-26  
**Version:** 1.0  
**Owner:** JourneyOfLife (Security Officer)  
**Review Cycle:** Annual or after significant incident

---

## Supported Versions

| Component | Version | Support Status |
|-----------|---------|----------------|
| jolarca (platform) | Latest main branch | ✅ Active |
| jolarca-infrastructure | Latest main branch | ✅ Active |
| All other repos | Latest main branch | ✅ Active |

**Policy:** Security patches are applied immediately upon discovery.

---

## Reporting a Vulnerability

**⚠️ DO NOT open a public GitHub issue for security vulnerabilities.**

### Private Vulnerability Disclosure

GitHub's private vulnerability disclosure is enabled for all jolarca-dev repositories.

**To report:** Go to affected repository → **Security** → **Report a vulnerability**

**Alternative:** security@jolarca.com (PGP-encrypted preferred)

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
