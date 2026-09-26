# Legal Counsel Engagement Guide — jolarca-dev Marketplace

**Purpose:** Guide for engaging legal counsel for incident response and regulatory compliance
**Date:** 2026-09-26
**Owner:** JourneyOfLife

---

## What Type of Lawyer to Look For

### Required Expertise

1. **Data Privacy & Security Law**
   - GDPR compliance and breach notification
   - PCI DSS requirements
   - Data protection regulations (Lithuanian/EU)

2. **Incident Response**
   - Experience with data breach response
   - Regulatory notification procedures
   - Law enforcement liaison

3. **Technology Law**
   - Software licensing (AGPL-3.0, etc.)
   - SaaS agreements
   - Terms of service

### Preferred Qualifications

- **Location:** Lithuania or EU (familiar with local regulations)
- **Experience:** 5+ years in data privacy/security law
- **Clients:** Experience with marketplace/e-commerce platforms
- **Availability:** Can respond within 2 hours for P1 incidents

### Where to Find

1. **Local law firms** (Vilnius, Lithuania)
   - Search: "duomenų apsauga teisininkas Vilniuje" (data protection lawyer Vilnius)
   - Search: "GDPR konsultantas" (GDPR consultant)

2. **EU-wide firms**
   - Firms with EU-wide data privacy practice
   - Must understand Lithuanian supervisory authority (VDAI)

3. **Industry associations**
   - Lithuanian Bar Association (Lietuvos advokatūra)
   - International Association of Privacy Professionals (IAPP)

---

## Initial Consultation Preparation

### Questions to Ask

**Experience:**
1. How many data breach incidents have you handled in the past 3 years?
2. Have you worked with marketplace/e-commerce platforms before?
3. Are you familiar with GDPR breach notification to VDAI (Lithuanian DPA)?
4. Have you handled PCI DSS incident response?

**Availability:**
5. What is your typical response time for P1 incidents?
6. Do you offer 24/7 emergency contact?
7. Who would be my primary contact? (partner vs. associate)

**Fees:**
8. What is your hourly rate for incident response work?
9. Do you offer retainer agreements? What are the terms?
10. What is your estimated cost for initial consultation?

**Approach:**
11. How do you approach breach notification decisions? (conservative vs. aggressive)
12. Do you coordinate with law enforcement? When?
13. How do you handle privilege and confidentiality during incidents?

### Documents to Provide

1. **This incident response plan** (incident-response/plan.md)
2. **Threat model** (threat-models/threat-model.md)
3. **SECURITY.md** (vulnerability disclosure policy)
4. **Organization structure** (single-operator, 14 repos)
5. **Data classification** (what data you handle: PII, payment data, etc.)

---

## Initial Consultation Email Template

```
Subject: Incident Response Legal Counsel — Initial Consultation Request

Dear [Lawyer/Firm Name],

I am the operator of jolarca-dev, a marketplace platform organization hosted on GitHub. I am seeking legal counsel for incident response and regulatory compliance.

**About jolarca-dev:**
- Single-operator organization (myself, JourneyOfLife)
- 14 GitHub repositories (marketplace platform, governance, compliance)
- Handles: customer PII, payment data (PCI DSS scope), KYC/AML data
- Compliance frameworks: SOC 2, GDPR, ISO 27001, PCI DSS
- Location: Lithuania (EU)

**What I need:**
1. Initial consultation (1-2 hours) to review our incident response plan
2. Availability for P1 incident response (2-hour response time)
3. Guidance on GDPR breach notification procedures (VDAI)
4. Guidance on PCI DSS incident response
5. Potential retainer agreement for ongoing support

**Questions:**
- Do you have experience with data breach incident response?
- Are you familiar with GDPR and PCI DSS requirements?
- What is your hourly rate for incident response work?
- Do you offer retainer agreements?

I have attached our incident response plan for your review. I am available for a consultation [provide 2-3 time slots].

Thank you for your time. I look forward to your response.

Best regards,
JourneyOfLife
Security Officer, jolarca-dev
security@jolarca.com
```

---

## Evaluation Criteria

### Must-Have

- ✅ Experience with GDPR breach notification
- ✅ Availability for P1 incidents (2-hour response)
- ✅ Clear fee structure
- ✅ Good communication (responds within 24 hours)

### Nice-to-Have

- ✅ Experience with marketplace/e-commerce
- ✅ Familiarity with PCI DSS
- ✅ Lithuanian language capability
- ✅ Fixed-fee retainer option

### Red Flags

- ❌ No experience with data breaches
- ❌ Cannot guarantee response time
- ❌ Vague fee structure
- ❌ Slow to respond to initial inquiry

---

## Decision Matrix

| Criterion | Weight | Lawyer A | Lawyer B | Lawyer C |
|-----------|--------|----------|----------|----------|
| GDPR experience | 30% | /10 | /10 | /10 |
| Availability | 25% | /10 | /10 | /10 |
| Cost | 20% | /10 | /10 | /10 |
| Communication | 15% | /10 | /10 | /10 |
| Marketplace experience | 10% | /10 | /10 | /10 |
| **Total** | **100%** | /10 | /10 | /10 |

**Decision:** Select lawyer with highest total score (minimum 7/10 required)

---

## Next Steps

1. **This week:**
   - [ ] Research 3-5 potential lawyers/firms
   - [ ] Send initial consultation emails
   - [ ] Schedule consultations

2. **Next week:**
   - [ ] Conduct consultations
   - [ ] Evaluate using decision matrix
   - [ ] Select lawyer

3. **Following week:**
   - [ ] Sign retainer agreement (if applicable)
   - [ ] Update incident response plan with lawyer details
   - [ ] Conduct initial review of incident response plan

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-26 | JourneyOfLife | Initial version |
