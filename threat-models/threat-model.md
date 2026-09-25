# Threat Model — jolarca-dev Marketplace

**Effective Date:** 2026-09-26  
**Version:** 1.0  
**Owner:** JourneyOfLife (Security Officer)  
**Review Cycle:** Quarterly or after significant change  
**Methodology:** STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)

---

## 1. System Architecture

### Components

1. **jolarca** — Marketplace platform (payments, KYC/AML, VAT OSS)
2. **jolarca-infrastructure** — Terraform IaC, hosting, networking
3. **jolarca-data** — Data pipelines, analytics, synthetic data
4. **jolarca-compliance** — RoPA, vendor assessments, audit evidence
5. **jolarca-legal** — Contracts, DPAs, legal registers
6. **jolarca-control** — Governance control plane (Terraform, policy)
7. **jolarca-security** — Security policies, incident response (this repo)
8. **jolarca-identity** — Identity and access management (planned)
9. **jolarca-observability** — Monitoring, logging, tracing (planned)
10. **jolarca-dr** — Disaster recovery (planned)
11. **jolarca-consent** — GDPR consent management (planned)
12. **jolarca-docs** — Documentation hub (planned)
13. **jolarca-runbooks** — Operational runbooks (planned)
14. **jolarca-vendor** — Vendor management (planned)

### Data Flows

```
User → jolarca (platform) → Payment Processor (Stripe)
                           → Identity Provider (when implemented)
                           → Database (PII, payment data)
                           → Logging (observability, when implemented)
```

### Trust Boundaries

1. **Internet → jolarca** — Public API endpoints
2. **jolarca → Database** — PII/payment data access
3. **jolarca → Third-party APIs** — Payment processor, identity provider
4. **Admin → jolarca-control** — Infrastructure changes

---

## 2. Threat Catalog (STRIDE)

### 2.1 Spoofing

| ID | Threat | Likelihood | Impact | Mitigation | Status |
|----|--------|------------|--------|------------|--------|
| S-01 | Credential stuffing against admin accounts | Medium | High | 2FA required (D-18), strong password policy | ⏳ Pending 2FA |
| S-02 | API key theft from commits | Low | Critical | gitleaks pre-commit hook, secret scanning | ✅ Active |
| S-03 | OAuth token theft | Low | High | Token rotation, minimal scopes | ✅ Active |

### 2.2 Tampering

| ID | Threat | Likelihood | Impact | Mitigation | Status |
|----|--------|------------|--------|------------|--------|
| T-01 | Unauthorized code changes | Low | Critical | Branch protection, required reviews | ✅ Active |
| T-02 | Infrastructure drift | Medium | High | Drift detection (daily), Terraform-only changes | ✅ Active |
| T-03 | Dependency poisoning | Medium | High | Dependabot, lockfile pinning, Trivy scans | ✅ Active |

### 2.3 Repudiation

| ID | Threat | Likelihood | Impact | Mitigation | Status |
|----|--------|------------|--------|------------|--------|
| R-01 | Unauthorized changes without audit trail | Low | High | Git history, signed commits (policy) | ✅ Active |
| R-02 | Denied transactions | Medium | Medium | Database audit logs (when implemented) | ⏳ Pending |

### 2.4 Information Disclosure

| ID | Threat | Likelihood | Impact | Mitigation | Status |
|----|--------|------------|--------|------------|--------|
| I-01 | PII data breach via public repos | High | Critical | Data classification, visibility controls (D-01) | ⚠️ 4 repos public |
| I-02 | Secret leakage in commits | Low | Critical | gitleaks, secret scanning | ✅ Active |
| I-03 | Database exposure | Low | Critical | Network isolation, access controls | ✅ Active |

### 2.5 Denial of Service

| ID | Threat | Likelihood | Impact | Mitigation | Status |
|----|--------|------------|--------|------------|--------|
| D-01 | Application-layer DoS | Medium | High | Rate limiting (when implemented), WAF | ⏳ Pending |
| D-02 | Infrastructure exhaustion | Low | High | Auto-scaling, monitoring (when implemented) | ⏳ Pending |

### 2.6 Elevation of Privilege

| ID | Threat | Likelihood | Impact | Mitigation | Status |
|----|--------|------------|--------|------------|--------|
| E-01 | Privilege escalation via vulnerability | Medium | Critical | Regular patching, dependency scans | ✅ Active |
| E-02 | Unauthorized admin access | Low | Critical | Least privilege, 2FA (pending) | ⏳ Pending 2FA |

---

## 3. Critical Assets

| Asset | Classification | Owner | Protection |
|-------|---------------|-------|------------|
| Customer PII | Restricted | JourneyOfLife | Encryption, access controls, GDPR compliance |
| Payment data | Restricted | JourneyOfLife | PCI DSS compliance, tokenization |
| Terraform state | Confidential | JourneyOfLife | Remote backend (pending), access controls |
| API keys/secrets | Confidential | JourneyOfLife | Secret scanning, rotation |
| Audit evidence | Confidential | JourneyOfLife | Immutable storage, access logs |

---

## 4. Attack Scenarios

### Scenario 1: Credential Stuffing → Admin Access → Data Breach

**Likelihood:** Medium  
**Impact:** Critical  
**Kill chain:**
1. Attacker obtains credentials from breach elsewhere
2. Attempts login to jolarca admin panel
3. Gains access (if no 2FA)
4. Exports customer PII
5. Sells on dark web or leaks publicly

**Mitigation:**
- ✅ Strong password policy
- ⏳ 2FA (D-18 — pending)
- ✅ Anomaly detection (when implemented)

**Residual risk:** High until 2FA is enforced

### Scenario 2: Dependency Poisoning → Supply Chain Attack

**Likelihood:** Medium  
**Impact:** High  
**Kill chain:**
1. Attacker publishes malicious package
2. Developer adds dependency (or transitive dependency)
3. Malicious code executes in CI/CD or production
4. Data exfiltration or backdoor installation

**Mitigation:**
- ✅ Dependabot alerts
- ✅ Trivy scans
- ✅ Lockfile pinning
- ✅ Code review for dependency changes

**Residual risk:** Medium (transitive dependencies harder to control)

### Scenario 3: Public Repo → PII Exposure → GDPR Breach

**Likelihood:** High (currently)  
**Impact:** Critical  
**Kill chain:**
1. Repo classified confidential but set to public (D-01)
2. Attacker discovers repo via GitHub search
3. Downloads RoPA, vendor assessments, contracts
4. Reports to supervisory authority or leaks publicly
5. GDPR investigation, fines, reputational damage

**Mitigation:**
- ⚠️ Flip repos to private (D-01 — pending)
- ✅ Data classification in YAML
- ✅ Drift detection for visibility changes

**Residual risk:** Critical until repos are private

---

## 5. Risk Register

| ID | Threat | Likelihood | Impact | Risk Level | Mitigation | Owner | Status |
|----|--------|------------|--------|------------|------------|-------|--------|
| R-01 | Credential stuffing | Medium | High | High | 2FA | JourneyOfLife | ⏳ Pending |
| R-02 | Dependency poisoning | Medium | High | High | Scans, reviews | JourneyOfLife | ✅ Active |
| R-03 | PII exposure (public repos) | High | Critical | Critical | Flip private | JourneyOfLife | ⚠️ Pending |
| R-04 | Infrastructure drift | Medium | High | High | Drift detection | JourneyOfLife | ✅ Active |
| R-05 | DoS attack | Medium | High | High | Rate limiting, WAF | JourneyOfLife | ⏳ Pending |

---

## 6. Compliance Mapping

| Control | Framework | Implementation |
|---------|-----------|----------------|
| Threat identification | ISO 27001 A.5.25 | This document |
| Risk assessment | ISO 27001 A.5.26 | Risk Register section |
| Mitigation planning | ISO 27001 A.5.27 | Mitigation column |
| Incident response | SOC 2 CC7.3 | incident-response/plan.md |
| Vulnerability management | PCI DSS Req 6.3 | vulnerability-management/register.md |

---

## 7. Review & Updates

**Quarterly review:**
- Update threat catalog with new threats
- Re-assess likelihood/impact based on changes
- Update mitigation status

**After significant change:**
- New component added
- Architecture change
- Security incident

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-26 | JourneyOfLife | Initial version |
