# Runbook: Credential Compromise

**Purpose:** Respond to compromised API keys, tokens, or passwords
**Trigger:** Suspicious activity, secret leak detected, or credible report
**Owner:** JourneyOfLife (Incident Commander)
**Estimated time:** 1–4 hours

---

## Prerequisites

- [ ] Access to GitHub org settings
- [ ] Access to affected services (payment processor, identity provider, etc.)
- [ ] Incident response plan reviewed

---

## Steps

### Step 1: Contain (0–15 minutes)

1. **Identify compromised credential:**
   - Which key/token/password?
   - Which service(s) does it access?
   - When was it last used?

2. **Revoke immediately:**
   - GitHub: Settings → Developer settings → Personal access tokens → Revoke
   - Payment processor: Dashboard → API keys → Revoke
   - Other services: Follow provider's revocation process

3. **Block suspicious activity:**
   - If suspicious IP identified → block at WAF/firewall
   - If suspicious user → disable account

### Step 2: Investigate (15–60 minutes)

1. **Check audit logs:**
   - GitHub audit log: `gh api orgs/jolarca-dev/audit-log`
   - Service audit logs (payment processor, etc.)
   - Look for: unusual API calls, data access, configuration changes

2. **Determine scope:**
   - What data was accessed?
   - What actions were taken?
   - Was data exfiltrated?

3. **Preserve evidence:**
   - Screenshot audit logs
   - Export log files
   - Document timeline

### Step 3: Remediate (60–120 minutes)

1. **Generate new credentials:**
   - Create new API key/token with minimal required scopes
   - Update all services that use the credential
   - Test to ensure functionality

2. **Update secrets:**
   - Update GitHub secrets: `gh secret set SECRET_NAME`
   - Update environment variables
   - Update configuration files (if not using secrets manager)

3. **Verify no persistence:**
   - Check for backdoors
   - Check for unauthorized API keys
   - Re-scan for secrets in code

### Step 4: Communicate (120–180 minutes)

1. **Internal notification:**
   - Notify stakeholders (see incident-response/plan.md)
   - Document in incident record

2. **External notification (if needed):**
   - If PII/payment data accessed → notify legal counsel
   - If regulatory notification required → follow GDPR/PCI DSS procedures

### Step 5: Review (180–240 minutes)

1. **Post-incident review:**
   - What happened?
   - How was it detected?
   - How quickly was it contained?
   - What could be improved?

2. **Update documentation:**
   - Update threat model (if new attack vector)
   - Update vulnerability register (if vulnerability exploited)
   - Update runbook (if procedures need refinement)

---

## Verification

- [ ] Compromised credential revoked
- [ ] New credential generated and tested
- [ ] Audit logs reviewed (no suspicious activity)
- [ ] Secrets updated in all locations
- [ ] Incident record created
- [ ] Stakeholders notified

---

## Rollback

If new credential doesn't work:

1. Revert to previous credential (if not yet revoked)
2. Debug configuration
3. Re-attempt rotation

---

## References

- [Incident Response Plan](../incident-response/plan.md)
- [SECURITY.md](../SECURITY.md)
- [Secret Rotation Runbook](secret-rotation.md)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-26 | JourneyOfLife | Initial version |
