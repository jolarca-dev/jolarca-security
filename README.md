# jolarca-security — Security Policies & Incident Response

**Purpose:** Central repository for security policies, threat models, incident response procedures, and compliance evidence for the jolarca-dev marketplace organization.

**Compliance:** SOC 2 CC7.3–CC7.5, ISO 27001 A.5.24–A.5.28, PCI DSS Req 6.3/12.10, GDPR Art. 32–33

---

## Repository Structure

```
jolarca-security/
├── SECURITY.md                          # Vulnerability disclosure policy
├── README.md                            # This file
├── incident-response/
│   └── plan.md                          # Incident response plan
├── threat-models/
│   └── threat-model.md                  # STRIDE threat model
├── vulnerability-management/
│   └── register.md                      # Vulnerability register
├── runbooks/
│   ├── README.md                        # Runbook index
│   └── credential-compromise.md         # Credential compromise response
├── pentest-reports/                     # Penetration test reports (when conducted)
├── policies/                            # Additional security policies
└── metrics/                             # Security metrics and KPIs
```

---

## Quick Start

### Reporting a Vulnerability

**⚠️ DO NOT open a public GitHub issue.**

See [SECURITY.md](SECURITY.md) for secure reporting instructions.

### Incident Response

If you suspect a security incident:

1. **Assess severity** (P1–P4) — see [Incident Response Plan](incident-response/plan.md)
2. **Follow procedures** — see [Runbooks](runbooks/)
3. **Document everything** — create incident record

### Security Controls

All jolarca-dev repositories enforce:

- ✅ **gitleaks** — Secret scanning (pre-commit)
- ✅ **Dependabot** — Dependency vulnerability alerts
- ✅ **Trivy** — Container/filesystem vulnerability scanning
- ✅ **CodeQL** — Semantic code analysis
- ✅ **Branch protection** — Required checks, no force push

---

## Compliance Mapping

| Framework | Controls | Implementation |
|-----------|----------|----------------|
| **SOC 2** | CC7.3–CC7.5 | Incident response plan, threat model, vulnerability register |
| **ISO 27001** | A.5.24–A.5.28 | Incident management planning, response, learning |
| **PCI DSS** | Req 6.3, 12.10 | Security policies, vulnerability management, incident response |
| **GDPR** | Art. 32–33 | Security of processing, breach notification procedures |

---

## Key Documents

| Document | Purpose | Review Cycle |
|----------|---------|--------------|
| [SECURITY.md](SECURITY.md) | Vulnerability disclosure policy | Annual |
| [Incident Response Plan](incident-response/plan.md) | Incident handling procedures | Quarterly |
| [Threat Model](threat-models/threat-model.md) | Known threats and mitigations | Quarterly |
| [Vulnerability Register](vulnerability-management/register.md) | Known vulnerabilities | Weekly |
| [Runbooks](runbooks/) | Step-by-step procedures | Quarterly |

---

## Metrics

**Tracking:**
- Mean Time to Remediate (MTTR) for vulnerabilities
- Open vulnerabilities by severity
- SLA compliance rate
- Incident response drill frequency

**Reporting:**
- Weekly: Open vulnerabilities, new discoveries
- Monthly: MTTR trends, SLA compliance
- Quarterly: Risk acceptance review, drill results

---

## Contact

**Security Team:** security@jolarca.com  
**Security Officer:** JourneyOfLife  
**Incident Hotline:** security@jolarca.com (P1/P2 incidents)

---

## License

This repository contains security policies and procedures. © 2026 jolarca-dev. All rights reserved.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-26 | JourneyOfLife | Initial version |
