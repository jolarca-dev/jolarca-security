# Security Metrics

This directory holds the security metrics and KPIs referenced by
[README.md](../README.md) and by
[vulnerability-management/register.md](../vulnerability-management/register.md).

## Status

**No metrics have been collected yet.** This file exists so the directory is
tracked by git and so the definitions below are agreed before measurement
starts. An empty directory is invisible to git, which previously left this path
documented in README.md but absent from the repository.

## Definitions

| Metric | Definition | Target | Cadence |
|--------|------------|--------|---------|
| MTTR (Critical) | Mean elapsed time from vulnerability confirmation to remediation for Critical severity | 7 days | Monthly |
| MTTR (High) | Same measure for High severity | 14 days | Monthly |
| Open vulnerabilities | Count of unresolved entries in the register, grouped by severity | 0 Critical, 0 High beyond SLA | Weekly |
| SLA compliance rate | Percentage of vulnerabilities remediated within the SLA in SECURITY.md | 100% | Monthly |
| Secret scanning coverage | Percentage of repositories with a passing gitleaks CI workflow | 100% | Monthly |
| Incident drill frequency | Number of completed incident response drills | 1 per quarter | Quarterly |
| Disclosure channel availability | Whether the published reporting channel is verified working | Always available | Monthly |

## Recording Convention

- One file per reporting period: `YYYY-MM.md` for monthly, `YYYY-Qn.md` for
  quarterly.
- Record the source command or system for every number. A metric without a
  reproducible source is not evidence.
- Never include personal data. Reference individuals by role.
- Metrics that were not collected must be recorded as `not collected` with a
  reason, not left blank. Silence in a compliance record is indistinguishable
  from concealment.

## Review

Reviewed quarterly alongside the vulnerability register, or after any incident.
