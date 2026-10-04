# jolarca-security — Security Policies & Incident Response

**Purpose:** Central repository for security policies, threat models, incident response procedures, and compliance evidence for the jolarca-dev marketplace organization.

**Compliance:** SOC 2 CC7.3–CC7.5, ISO 27001 A.5.24–A.5.28, PCI DSS Req 6.3/12.10, GDPR Art. 32–33

---

## Repository Structure

```text
jolarca-security/
├── SECURITY.md                        # Vulnerability disclosure policy
├── README.md                          # This file
├── CONTRIBUTING.md                    # Change pipeline and contribution rules
├── LICENSE                            # Proprietary — all rights reserved
├── REVIEW.md                          # 2026-09-26 review + 2026-09-28 addendum
├── .markdownlint-cli2.jsonc           # Markdown lint policy and justifications
├── .pre-commit-config.yaml            # Local hooks (gitleaks, file hygiene)
├── pyproject.toml                     # Python project and test configuration
├── .github/
│   ├── CODEOWNERS                     # Review ownership
│   ├── dependabot.yml                 # Dependency update configuration
│   ├── ISSUE_TEMPLATE/                # Vulnerability and exception templates
│   └── workflows/                     # gitleaks scan, lint, policy tests
├── audits/
│   └── 2026-09-28-repository-readiness-audit.md
├── incident-response/
│   └── plan.md                        # Incident response plan
├── metrics/
│   └── README.md                      # Security metrics and KPIs
├── pentest-reports/
│   └── README.md                      # Penetration test reports
├── policies/
│   ├── README.md                      # Policy index
│   ├── control-matrix.yml             # Machine-readable control inventory
│   ├── legal-counsel-contact.md
│   └── legal-counsel-engagement.md
├── runbooks/
│   ├── README.md                      # Runbook index
│   └── credential-compromise.md       # Credential compromise response
├── tests/
│   └── test_repository_controls.py    # Policy-as-code control assertions
├── threat-models/
│   └── threat-model.md                # STRIDE threat model
└── vulnerability-management/
    └── register.md                    # Vulnerability register
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

### Security Controls — Verified State

Controls are recorded in
[policies/control-matrix.yml](policies/control-matrix.yml), which is the single
source of truth. The `policy-tests` CI job runs
`tests/test_repository_controls.py`, which fails if any claim below disagrees
with that file — so this table cannot silently drift back into wishful
thinking.

Markers: ✅ verified · ⚠️ compensating control · ❌ known gap.

| Control | Status and evidence |
|---------|---------------------|
| ✅ **gitleaks secret scanning** | pre-commit hook locally, plus a full-history scan over every ref on each push to `main` and on every pull request |
| ✅ **YAML and Markdown linting** | `lint` workflow, triggered on push to `main` and on pull requests |
| ✅ **policy-as-code tests** | `tests/` executed by the `policy-tests` CI job |
| ✅ **Actions pinned to full commit SHAs** | enforced by test, not by convention |
| ✅ **GPG-signed commits** | every commit signed; verify with `git log --show-signature` |
| ✅ **CODEOWNERS review ownership** | `.github/CODEOWNERS` points at a principal that actually exists |
| ✅ **private repository visibility** | confirmed through the GitHub API |
| ✅ **least-privilege repository access** | one owner, zero teams, zero outside collaborators, zero deploy keys |
| ✅ **GitHub Actions allowlist** | `allowed_actions: selected`; GitHub-owned actions plus one pinned third-party action |
| ✅ **Dependabot alerts** | enabled, zero open alerts at audit time |
| ✅ **Dependabot version updates** | `.github/dependabot.yml` covers `github-actions` and `pip` |
| ⚠️ **GitHub private vulnerability reporting** | unavailable for this private repository on the Free plan; enabled on the public `jolarca` repository and published as the disclosure channel |
| ⚠️ **pull request review gate** | with one member, self-approval is impossible; feature branch, pull request, CI, independent automated review and a recorded self-review are used instead |
| ❌ **security disclosure mailbox** | `security@jolarca.com` cannot receive mail — `jolarca.com` has no MX records |
| ❌ **branch protection** | HTTP 403: unavailable for private repositories on the GitHub Free plan |
| ❌ **GitHub secret scanning and push protection** | requires GitHub Advanced Security |
| ❌ **CodeQL code scanning** | requires GitHub Advanced Security for private repositories |
| ❌ **Trivy container scanning** | this repository builds no image, so there is nothing to scan |
| ❌ **required pull request approvals** | depends on branch protection and on a second reviewer |
| ❌ **organisation-wide 2FA enforcement** | the API field is read-only; it must be set in the web UI |
| ❌ **member privilege restrictions** | repository-visibility-change and collaborator-invite flags are web-UI only |

**Scope note.** Controls differ per repository and per plan. Verified on
2026-09-28: `jolarca` (public) has branch protection with required checks
including CodeQL and Trivy; `jolarca-control` (public) has no branch
protection; this private repository cannot have branch protection on the
current plan. Any statement about organisation-wide enforcement must be
verified per repository before it is published.

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

**Security Team:** <security@jolarca.com>
**Security Officer:** JourneyOfLife
**Incident Hotline:** <security@jolarca.com> (P1/P2 incidents)

---

## License

Proprietary. All rights reserved. See [LICENSE](LICENSE).

This repository is **not** open source and is **not** licensed under the AGPL,
GPL, MIT, Apache or any other permissive or copyleft licence. It describes the
organisation's security controls and known weaknesses, so unauthorised
disclosure is prohibited. Access is limited to authorised personnel and to
third parties under written confidentiality obligations.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-26 | JourneyOfLife | Initial version |
| 1.1 | 2026-09-28 | JourneyOfLife | Readiness audit: replaced unscoped control claims with a matrix-verified table, corrected repository structure, added proprietary licence reference |
