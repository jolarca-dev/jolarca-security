# Incident Response Plan — jolarca-dev Marketplace

**Effective Date:** 2026-09-26
**Version:** 1.0
**Owner:** JourneyOfLife (Incident Commander)
**Review Cycle:** Quarterly or after significant incident
**Compliance:** SOC 2 CC7.3–CC7.5, ISO 27001 A.5.24–A.5.28, PCI DSS Req 12.10

---

## 1. Purpose

This plan establishes procedures for detecting, responding to, and recovering from security incidents in the jolarca-dev marketplace organization.

**Goals:**
- Minimize impact to confidentiality, integrity, and availability
- Preserve evidence for forensic analysis
- Meet regulatory notification requirements (GDPR Art. 33: 72 hours)
- Restore operations within defined RTOs

---

## 2. Incident Severity Levels

| Level | Definition | Response Time | Escalation |
|-------|-----------|---------------|------------|
| **P1 — Critical** | Active data breach, system compromise, or service outage affecting PCI/PII data | Immediate | Owner + Legal + All stakeholders |
| **P2 — High** | Vulnerability exploit in progress, unauthorized access detected | 2 hours | Owner + Legal |
| **P3 — Medium** | Suspicious activity, potential vulnerability, minor service degradation | 24 hours | Owner |
| **P4 — Low** | Policy violation, minor security event, near-miss | 5 business days | Owner |

---

## 3. Incident Response Team

### Current State: Single-Operator Reality

**As of 2026-09-26, jolarca-dev is operated by a single individual (JourneyOfLife) who fills all incident response roles.**

| Role | Name | Contact | Responsibilities |
|------|------|---------|------------------|
| **Incident Commander** | JourneyOfLife | security@jolarca.com | Overall coordination, decision authority |
| **Technical Lead** | JourneyOfLife | security@jolarca.com | Technical investigation, containment |
| **Communications** | JourneyOfLife | security@jolarca.com | Stakeholder updates, public comms |
| **Legal Counsel** | ⏳ In Progress | [TBD — see policies/legal-counsel-contact.md](../policies/legal-counsel-contact.md) | Regulatory notification, liability |

### Implications of Single-Operator Model

**Risks:**
- **Cognitive overload:** One person must simultaneously coordinate, investigate, contain, and communicate
- **No peer review:** Decisions made under stress without second opinion
- **Availability risk:** If the operator is unavailable, no one can respond
- **Burnout risk:** Incident response is high-stress; no one to share the burden

**Mitigations (current):**
- ✅ Automated detection (Dependabot, Trivy, gitleaks) reduces manual monitoring burden
- ✅ Runbooks provide step-by-step guidance to reduce decision fatigue
- ✅ External legal counsel available for regulatory decisions
- ✅ Post-incident reviews ensure lessons are captured

**Mitigations (planned):**
- ⏳ Enable 2FA to reduce credential compromise risk (D-18)
- ⏳ Hire second operator to enable role separation (D-10 trigger)
- ⏳ Establish on-call rotation when team grows
- ⏳ **Engage legal counsel** — Engagement guide created (policies/legal-counsel-engagement.md), outreach pending

### When to Separate Roles

**Trigger events for hiring additional incident response personnel:**

1. **Second operator onboarded** — Immediately separate Incident Commander and Technical Lead roles
2. **P1 incident occurs** — Post-incident, prioritize hiring to prevent recurrence
3. **Regulatory requirement** — If auditor or regulator requires role separation
4. **Business growth** — When marketplace goes live and handles real transactions

**Target state (post-hire):**
```
Incident Commander: [Person A] — coordinates, makes decisions
Technical Lead:     [Person B] — investigates, contains
Communications:     [Person A or C] — updates stakeholders
Legal Counsel:      [External] — regulatory guidance
```

### Auditor Guidance

**If an auditor questions the single-operator model:**

1. **Acknowledge the limitation:** "Yes, we currently operate with a single incident responder."
2. **Explain mitigations:** "We use automated detection, runbooks, and external legal counsel to reduce risk."
3. **Show awareness:** "We've documented this as a known limitation in our risk register."
4. **Demonstrate plan:** "We have clear triggers for when we'll separate roles (see above)."
5. **Provide evidence:** Show this document, the risk register, and any post-incident reviews.

**Key point:** Auditors accept single-operator models for small organizations **if** the risks are documented, mitigated, and there's a plan to separate roles when the organization grows.

---

## 4. Incident Response Phases

### Phase 1: Preparation

**Tools:**
- GitHub Security Advisories (vulnerability reporting)
- Dependabot alerts (dependency vulnerabilities)
- Trivy scans (container/filesystem vulnerabilities)
- gitleaks (secret detection in commits)
- Cloud provider monitoring (when implemented)

**Documentation:**
- This incident response plan
- Threat models (threat-models/)
- Vulnerability register (vulnerability-management/register.md)
- Security runbooks (runbooks/)

**Training:**
- Annual incident response drill
- Post-incident reviews

### Phase 2: Detection & Analysis

**Detection Sources:**
1. Automated alerts (Dependabot, Trivy, gitleaks)
2. User reports (via SECURITY.md disclosure)
3. Anomalous behavior (logs, metrics)
4. Third-party notifications

**Triage Process:**
1. **Validate:** Confirm the incident is real
2. **Classify:** Assign severity (P1–P4)
3. **Scope:** Determine affected systems/data
4. **Document:** Create incident record (incident-response/incidents/YYYY-MM-DD-<name>.md)

**Evidence Preservation:**
- Do NOT delete logs or modify affected systems
- Capture screenshots, log excerpts, network traces
- Store evidence in secure location (incident-response/evidence/)

### Phase 3: Containment

**Short-term containment:**
- Isolate affected systems (if possible without data loss)
- Block malicious IPs/users
- Revoke compromised credentials
- Disable vulnerable services

**Long-term containment:**
- Apply security patches
- Implement additional monitoring
- Restrict access to affected areas

**Decision authority:** Incident Commander can authorize containment actions without prior approval if P1/P2.

### Phase 4: Eradication

- Remove malware/backdoors
- Patch vulnerabilities
- Reset compromised credentials
- Verify no persistence mechanisms remain

**Verification:**
- Re-scan affected systems
- Review logs for suspicious activity
- Confirm eradication before recovery

### Phase 5: Recovery

- Restore systems from clean backups (if needed)
- Re-enable services
- Monitor closely for recurrence (72 hours minimum)
- Verify data integrity

**Communication:**
- Update stakeholders on recovery progress
- Confirm service restoration

### Phase 6: Lessons Learned

**Timeline:** Within 5 business days of incident closure

**Post-Incident Review:**
1. What happened? (timeline)
2. What went well? (response effectiveness)
3. What could be improved? (gaps, delays)
4. What actions will prevent recurrence?

**Deliverables:**
- Updated incident record with lessons learned
- Updated threat models (if new attack vector)
- Updated runbooks (if procedures need refinement)
- Updated vulnerability register (if new vulnerability class)

---

## 5. Notification Requirements

### Internal Notification

| Severity | Notify | Timeline |
|----------|--------|----------|
| P1 | Owner + Legal + All stakeholders | Immediate |
| P2 | Owner + Legal | 2 hours |
| P3 | Owner | 24 hours |
| P4 | Owner | 5 business days |

### External Notification

**GDPR (Art. 33):** If personal data breach → notify supervisory authority within **72 hours**
**PCI DSS:** If cardholder data compromised → notify payment brands immediately
**Users:** If user data at risk → notify affected users without undue delay

**Legal counsel** must approve all external communications.

---

## 6. Incident Record Template

```markdown
# Incident: [Title]

**Date:** YYYY-MM-DD HH:MM UTC
**Severity:** P1/P2/P3/P4
**Status:** Open / Contained / Resolved / Closed
**Incident Commander:** [Name]

## Summary
[1-2 sentence description]

## Timeline
- HH:MM — [Event]
- HH:MM — [Event]

## Impact
- **Systems affected:** [List]
- **Data affected:** [PII, payment data, etc.]
- **Duration:** [Start to resolution]

## Root Cause
[Technical explanation]

## Containment Actions
[What was done to contain]

## Eradication Actions
[What was done to remove threat]

## Recovery Actions
[What was done to restore]

## Lessons Learned
[What went well, what didn't, improvements]

## Follow-up Actions
- [ ] Action 1 (Owner, Due date)
- [ ] Action 2 (Owner, Due date)
```

---

## 7. Testing & Maintenance

### Quarterly Drills

- Tabletop exercise for P1 scenario
- Test communication channels
- Verify tool access

### Annual Review

- Review and update this plan
- Update contact information
- Review lessons learned from past year

---

## 8. Related Documents

- [SECURITY.md](../SECURITY.md) — Vulnerability disclosure policy
- [Threat Models](../threat-models/) — Known threats and mitigations
- [Vulnerability Register](../vulnerability-management/register.md) — Known vulnerabilities
- [Security Runbooks](../runbooks/) — Step-by-step procedures

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-26 | JourneyOfLife | Initial version |
