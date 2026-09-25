# Security Policies — jolarca-dev Marketplace

**Purpose:** Central repository for security policies, procedures, and governance documents  
**Owner:** JourneyOfLife (Security Officer)  
**Review Cycle:** Annual or after significant change

---

## Policies Index

### Active Policies

1. ✅ **[Legal Counsel Engagement Guide](legal-counsel-engagement.md)** — Guide for selecting and engaging legal counsel for incident response
2. ✅ **[Legal Counsel Contact](legal-counsel-contact.md)** — Contact details and engagement terms (⏳ In Progress)

### Planned Policies

3. ⏳ **Data Classification Policy** — How to classify data (public, internal, confidential, restricted)
4. ⏳ **Access Control Policy** — Who gets access to what, and how
5. ⏳ **Encryption Policy** — When and how to encrypt data
6. ⏳ **Acceptable Use Policy** — What is and isn't allowed on jolarca-dev systems
7. ⏳ **Vendor Security Policy** — Security requirements for third-party vendors
8. ⏳ **Remote Work Policy** — Security requirements for remote work

---

## Policy Development Process

### Creating a New Policy

1. **Identify need** — What gap does this policy fill?
2. **Research** — What are industry best practices? What do similar organizations do?
3. **Draft** — Write the policy (use existing policies as templates)
4. **Review** — Self-review, then legal counsel review (when engaged)
5. **Approve** — Security Officer approval
6. **Publish** — Commit to this repository
7. **Communicate** — Announce to stakeholders

### Reviewing Existing Policies

**Annual review:**
- Is the policy still relevant?
- Are there any gaps or ambiguities?
- Has the environment changed (new systems, new regulations)?
- Are there any lessons learned from incidents?

**Post-incident review:**
- Did the policy work as intended?
- Were there any gaps that contributed to the incident?
- Should the policy be updated?

---

## Compliance Mapping

| Policy | SOC 2 | ISO 27001 | PCI DSS | GDPR |
|--------|-------|-----------|---------|------|
| Legal Counsel Engagement | CC7.3 | A.5.26 | 12.10 | Art. 33 |
| Data Classification | CC6.1 | A.8.9 | 1.2 | Art. 5 |
| Access Control | CC6.1 | A.9.1 | 7.1 | Art. 32 |
| Encryption | CC6.7 | A.10.1 | 3.4 | Art. 32 |
| Acceptable Use | CC1.4 | A.7.2 | 12.1 | — |
| Vendor Security | CC9.2 | A.15.1 | 12.4 | Art. 28 |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-26 | JourneyOfLife | Initial version |
