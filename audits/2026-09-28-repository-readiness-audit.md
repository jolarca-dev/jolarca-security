# Repository Readiness Audit — jolarca-security

**Audit date:** 2026-09-28

**Auditor:** Release Architect (independent pre-deployment readiness review)

**Repository:** `jolarca-dev/jolarca-security` (private, default branch `main`)

**Commit at audit start:** `4e10a90` (14 commits, all GPG-signed, all previously
pushed directly to `main`)

**Compliance targets:** SOC 2 Type II (CC6, CC7, CC8), ISO/IEC 27001 (A.5, A.8),
GDPR (Art. 32–33), PCI DSS (Req. 6, 12)

**Evidence discipline:** every statement below is marked VERIFIED (command run,
output observed) or ASSUMED (not checked). No finding is based on a prior report
or on documentation alone.

---

## Verdict

| Stage | Verdict | Basis |
|-------|---------|-------|
| At audit start | **BLOCKED** | 4 critical findings; CI failing on the default branch; no licence; no functioning disclosure channel |
| After remediation in this change set | **READY-WITH-FIXES** | All repository-level findings closed and verified; 3 owner actions remain that cannot be performed through the API |

**Not READY.** Three findings (F-05 MX provisioning, F-18 organisation 2FA
enforcement, F-19 member privilege restrictions) require action in the GitHub
web UI or at the DNS provider. They are listed in
[Owner actions required](#owner-actions-required) with exact steps. The
repository should not be described as launch-ready until they are closed and
re-verified.

---

## Executive Summary

This repository was presented as a new repository awaiting its first commit. It
was not new: 14 signed commits had already been pushed directly to `main`, and a
prior self-review (`REVIEW.md`) declared the documentation "100% accurate",
"fully audit-ready" with "no remaining issues".

That declaration was wrong, and it was wrong in the specific way that is most
damaging in an audit. The documentation asserted security controls that do not
exist in this repository — Trivy, CodeQL and branch protection — because they
had been verified in a different repository (`jolarca`, public) and then
generalised to the whole organisation without restating the scope. Meanwhile the
only CI security control that did exist, gitleaks, had been failing on every
single run since it was added, and the lint workflow had never executed once.

The most serious finding was not technical. `SECURITY.md` published
`security@jolarca.com` as the primary vulnerability disclosure channel. The
domain `jolarca.com` resolves to parking nameservers and has **no MX records**,
so every vulnerability report sent there was silently discarded. A prior review
had raised exactly this as an open critical action, and then concluded "no
remaining issues" in the same document.

Remediation therefore had two halves: fix the defects, and install an
enforcement layer so the same class of defect cannot recur silently. Control
claims are now bound to a machine-readable inventory
([policies/control-matrix.yml](../policies/control-matrix.yml)) and validated in
CI by [tests/test_repository_controls.py](../tests/test_repository_controls.py).

**Findings: 21 total — 4 critical, 6 high, 6 medium, 4 low, 1 informational.**

---

## Phase 1 — Repository Readiness Audit

### 1.1 Structural checks

| Item | Result | Evidence |
|------|--------|----------|
| Repository visibility | VERIFIED private | `gh api repos/jolarca-dev/jolarca-security --jq '.visibility'` → `private` |
| README.md | VERIFIED present | `git ls-files` |
| LICENSE | **ABSENT** (F-06) | `gh api ... --jq '.license'` → `null`; not in `git ls-files` |
| Licence type | N/A at audit start | No licence file existed; proprietary status was asserted only in README prose |
| .gitignore | VERIFIED present and adequate | 63 lines; covers `.env`, `*.pem`, `*.key`, `.venv/`, `secrets/`, `.idea/`, scan outputs |
| CODEOWNERS | VERIFIED present but **ineffective** (F-04) | Referenced `@jolarca-dev/security-team` and `@jolarca-dev/compliance` |
| CONTRIBUTING.md | **ABSENT** (F-07) | not in `git ls-files` |
| SECURITY.md | VERIFIED present, **inaccurate** (F-08, F-09) | 14 repositories claimed, 16 exist |
| Documented directories tracked | **FAILED** (F-15) | `metrics/` and `pentest-reports/` exist locally, contain no files, therefore absent from git |
| Scaffold artefacts | **FAILED** (F-14) | `main.py` was PyCharm's generated sample script |
| Commit signing | VERIFIED | `git log --format='%h %G? %GS'` → `G` on all 14 commits |
| Secret material in history | VERIFIED clean | `gitleaks git . --exit-code 0` → 14 commits scanned, 0 findings |

### 1.2 Access control checks

| Item | Result | Evidence |
|------|--------|----------|
| Collaborators | VERIFIED single owner, admin | `gh api .../collaborators` → `JourneyOfLife` only |
| Teams | VERIFIED none | `gh api repos/.../teams` → `[]`; `gh api orgs/jolarca-dev/teams` → `[]` |
| Outside collaborators | VERIFIED none | `gh api orgs/jolarca-dev/outside_collaborators` → `[]` |
| Deploy keys | VERIFIED none | `gh api repos/.../keys` → `[]` |
| Deploy keys org-wide | VERIFIED disabled | `deploy_keys_enabled_for_repositories: false` |
| Default member permission | VERIFIED `none` (least privilege) | `default_repository_permission: "none"` |
| Private forking | VERIFIED disabled | `members_can_fork_private_repositories: false` |
| Forking of this repo | VERIFIED disabled | `allow_forking: false` |
| Member 2FA | VERIFIED enabled for the sole member | `gh api user --jq '.two_factor_authentication'` → `true` |
| **Org-wide 2FA enforcement** | **FAILED** (F-18) | `two_factor_requirement_enabled: false` |
| Members can change repo visibility | **FAILED** (F-19) | `members_can_change_repo_visibility: true` — directly matches threat model entry D-01 |
| Members can invite outside collaborators | **FAILED** (F-19) | `members_can_invite_outside_collaborators: true` |
| Web commit sign-off | VERIFIED required | `web_commit_signoff_required: true` |
| Wiki / Projects / Downloads | VERIFIED disabled | all `false` |

### 1.3 Branch protection checks

| Item | Result | Evidence |
|------|--------|----------|
| Default branch protected | **NOT POSSIBLE** (F-17) | `gh api repos/.../branches/main/protection` → HTTP 403 "Upgrade to GitHub Pro or make this repository public to enable this feature." |
| Repository rulesets | **NOT POSSIBLE** | `gh api repos/.../rulesets` → HTTP 403, same reason |
| PR required / ≥1 approval | **NOT ENFORCEABLE** | Requires branch protection; additionally the sole member cannot approve their own pull request |
| Force-push blocked | **NOT ENFORCEABLE** | Requires branch protection |
| Branch deletion blocked | **NOT ENFORCEABLE** | Requires branch protection |
| Signed commits required | **NOT ENFORCEABLE** | Requires branch protection; observed in practice instead (all 14 commits signed) |
| Plan confirmed | VERIFIED `free` | `gh api orgs/jolarca-dev --jq '.plan.name'` → `free` |

Making the repository public would unlock branch protection at no cost, but this
repository holds threat models, incident response procedures and a vulnerability
register. Publishing it to gain a control would destroy more value than the
control provides. Recorded as an accepted risk with an upgrade trigger.

### 1.4 Secrets and scanning checks

| Item | Result | Evidence |
|------|--------|----------|
| gitleaks pre-commit hook | VERIFIED installed and passing | `.git/hooks/pre-commit` present; pre-commit 4.6.2; `gitleaks` and `detect-private-key` configured |
| gitleaks in CI | **FAILING ON EVERY RUN** (F-01) | Run `36256982130` on `main`: `completed failure` |
| Secrets in working tree or history | VERIFIED none | gitleaks 8.30.1 over 14 commits, `--log-opts=--all`: 0 findings |
| GitHub secret scanning | **UNAVAILABLE** (F-17) | `gh api .../secret-scanning/alerts` → HTTP 404 "Secret scanning is disabled on this repository." |
| Push protection | **UNAVAILABLE** (F-17) | Requires GitHub Advanced Security |
| CodeQL code scanning | **UNAVAILABLE** (F-17) | HTTP 403 "Advanced Security must be enabled for this repository to use code scanning." |
| Dependabot alerts | VERIFIED enabled, 0 open | `gh api .../dependabot/alerts` → `0` |
| Dependabot version updates | **ABSENT** (F-11) | No `.github/dependabot.yml`; automated security fixes `{"enabled":false}` |
| Dependency graph | VERIFIED working | Run `36253435776` "Graph Update: pip in /" → `success` |

### 1.5 CI/CD readiness

| Item | Result | Evidence |
|------|--------|----------|
| gitleaks workflow | VERIFIED present, **failing** (F-01) | `.github/workflows/gitleaks.yml` |
| lint workflow | VERIFIED present, **never executed** (F-02) | `pull_request` trigger only; all 14 commits went straight to `main` |
| Test suite | **ABSENT** (F-13) | No `tests/` directory, so no "tests" status check could ever exist |
| markdownlint policy | **ABSENT** (F-03) | 514 default-rule violations across 11 documents |
| yamllint | VERIFIED clean | `yamllint -d relaxed --no-warnings .` → exit 0 |
| Actions permissions | **FAILED** (F-12) | `allowed_actions: "all"`, `sha_pinning_required: false` |
| Total workflow runs on `main` | VERIFIED 2 | one gitleaks failure, one dependency-graph success |

---

## Findings Register

Status key: **FIXED** closed and verified in this change set · **OWNER ACTION**
cannot be performed through the API or from this repository · **ACCEPTED**
documented risk with a remediation trigger.

| ID | Sev | Finding | Status |
|----|-----|---------|--------|
| F-01 | Critical | gitleaks CI workflow failed on every run: abbreviated SHA ref `e0c47f4` is rejected by Actions, and `gitleaks-action` v2 requires a `GITLEAKS_LICENSE` secret that was never configured | FIXED |
| F-02 | High | lint workflow had no `push` trigger so it never ran once; it also used a bare `pip install` that fails under PEP 668 on ubuntu-24.04 runners | FIXED |
| F-03 | High | No markdownlint policy existed; default rules produced 514 violations, so the first pull request would have been blocked by CI | FIXED |
| F-04 | Critical | CODEOWNERS referenced `@jolarca-dev/security-team` and `@jolarca-dev/compliance`; the organisation has zero teams, so GitHub silently ignored both and the file enforced nothing | FIXED |
| F-05 | Critical | No functioning vulnerability disclosure channel: `jolarca.com` has no MX records so `security@jolarca.com` silently discards mail, and private vulnerability reporting was disabled | PARTIALLY FIXED — MX provisioning is an OWNER ACTION |
| F-06 | High | No LICENSE file; proprietary status existed only as README prose and the GitHub API reported `license: null` | FIXED |
| F-07 | Medium | No CONTRIBUTING.md and no documented change pipeline | FIXED |
| F-08 | Critical | README.md and SECURITY.md asserted Trivy, CodeQL and branch protection as active controls for all repositories; none exist here. Claims verified in `jolarca` were generalised fleet-wide | FIXED |
| F-09 | High | SECURITY.md declared 14 repositories when 16 exist, and omitted `jolarca-payments` — the PCI DSS-scoped repository — from the security policy scope entirely | FIXED |
| F-10 | High | REVIEW.md asserted "100% accurate", "No remaining issues" and "fully audit-ready" while its own Priority Actions list still carried open critical items | FIXED by dated addendum; original retained |
| F-11 | Medium | No `.github/dependabot.yml` despite Dependabot being claimed as an active control | FIXED |
| F-12 | Medium | Actions permitted `allowed_actions: all`; workflows pinned actions by mutable tag rather than commit SHA | FIXED |
| F-13 | Medium | No test suite, so no meaningful status check could gate a merge | FIXED |
| F-14 | Low | `main.py` was PyCharm's generated sample script, committed into a governance repository | FIXED (deleted) |
| F-15 | Low | `metrics/` and `pentest-reports/` were empty, therefore untracked by git, contradicting the documented repository structure | FIXED |
| F-16 | Low | Commits are authored from a personal Gmail address; no repository-local git identity is configured | ACCEPTED |
| F-17 | Medium | Branch protection, secret scanning, push protection and CodeQL are all unavailable for a private repository on the GitHub Free plan | ACCEPTED with compensating controls |
| F-18 | High | Organisation-wide 2FA enforcement is disabled and cannot be changed through the REST API | OWNER ACTION |
| F-19 | Medium | `members_can_change_repo_visibility` and `members_can_invite_outside_collaborators` are both `true` and are not writable through the API | OWNER ACTION |
| F-20 | Low | Organisation billing email was the placeholder `your-billing-email@example.com` | FIXED |
| F-21 | Informational | The first 14 commits were pushed directly to `main`, bypassing the branch-and-pull-request pipeline this audit enforces | ACCEPTED, documented |

### Further inaccuracies found while remediating

Correcting F-08 required reading every document that repeats a control claim,
which surfaced four more factual errors of the same class. All are now fixed:

| Location | Claimed | Verified | Correction |
|----------|---------|----------|------------|
| `threat-models/threat-model.md` T-01 | "Branch protection, required reviews" — Active | `jolarca` has branch protection but `required_approving_review_count: 0`; `jolarca-control` has none; private repos cannot have any | Status changed to Partial, scope stated |
| `threat-models/threat-model.md` I-01 | "4 repos public" | 10 public, 6 private | Count corrected |
| `threat-models/threat-model.md` components | 14 components | 16 repositories | `jolarca-payments` and `.github` added |
| `policies/legal-counsel-engagement.md` | "14 repos" in counsel briefing and email template | 16 repositories | Count corrected |

Scope notes were added to `threat-models/threat-model.md`,
`vulnerability-management/register.md` and `incident-response/plan.md` so that a
reader can no longer mistake an organisation-level claim for a repository-level
one. The underlying lesson is that a control claim without a named scope is not
a control claim — it is an assumption.

---

## Bugs Found and Fixed

These are the defects that were broken code or configuration rather than missing
artefacts. Each entry records the observed failure, the root cause and the
verification that proves the fix.

### BUG-1 — gitleaks CI failed on every run (F-01)

**Observed failure.** Run `36256982130` on `main`, log line:

```text
##[error]Unable to resolve action `gitleaks/gitleaks-action@e0c47f4`, the provided
ref `e0c47f4` is the shortened version of a commit SHA, which is not supported.
Please use the full commit SHA `e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e` instead.
```

**Root cause — two independent defects.**

1. GitHub Actions requires a full 40-character commit SHA when pinning by
   commit. An abbreviated SHA can never resolve, so the workflow failed at the
   action-resolution step before executing anything.
2. Fixing the SHA alone would not have worked. `gitleaks-action` v2 requires a
   `GITLEAKS_LICENSE` environment value for organisation-owned repositories.
   `gh api repos/jolarca-dev/jolarca-security/actions/secrets` returned an empty
   list, so the secret did not exist and the action would have failed next.

**Fix.** Removed the third-party action entirely. The gitleaks CLI is open
source and needs no licence, so the workflow now downloads the pinned release
asset, verifies its sha256 against the digest published by the release, installs
it and runs `gitleaks git . --redact --exit-code 1 --log-opts="--all"`.

**Verification.** The identical command was run locally against the full history
before being committed: exit code 0, 14 commits scanned, no leaks found. The
sha256 pin was taken from the GitHub release API rather than transcribed by
hand. Confirmed again by the CI run on the remediation branch.

### BUG-2 — lint workflow never executed (F-02)

**Observed failure.** `gh run list` showed exactly two runs in the repository's
history: the failing gitleaks run and a dependency-graph update. No lint run had
ever been created.

**Root cause.** The workflow declared only `on: pull_request`. Every one of the
14 commits was pushed directly to `main`, so the trigger condition was never
met. The repository therefore had no status check at all, which also means
branch protection — had it been available — would have had nothing to require.

A second latent defect sat behind it: the job ran `pip install yamllint`
directly. ubuntu-24.04 runners ship a PEP 668 externally-managed Python, so a
bare `pip install` fails. The bug had never surfaced only because the workflow
had never run.

**Fix.** Added a `push` trigger on `main`, and installed yamllint, pytest and
pyyaml inside an isolated virtualenv.

**Verification.** The workflow now appears in the run list for the remediation
branch and for `main` after merge.

### BUG-3 — markdownlint would have blocked the first pull request (F-03)

**Observed failure.** Running markdownlint-cli2 v0.22.1 with default rules
against the 11 tracked Markdown documents produced **514 errors** and exit
code 1.

Distribution: MD060 table-column-style 274, MD013 line-length 99, MD032
blanks-around-lists 63, MD029 ol-prefix 20, MD024 duplicate-heading 13, MD022
blanks-around-headings 13, MD036 emphasis-as-heading 12, MD034 bare-urls 11,
MD040 fenced-code-language 4, MD058 blanks-around-tables 3, MD033 inline-html 1,
MD031 blanks-around-fences 1.

**Root cause.** No `.markdownlint-cli2.jsonc` existed, so the CI action would
apply default rules to governance prose written without them.

**Fix — deliberate and split.** An automatic fix was evaluated on a scratch copy
first, and it was **partially rejected**:

- **Accepted (111 fixes):** MD032, MD034, MD022, MD058, MD031 — blank lines
  around lists, tables and fences, and bare URLs and email addresses converted
  to autolinks. These are genuine rendering and accessibility improvements.
- **Rejected (20 fixes):** MD029 renumbering. The automatic fix renumbered
  `policies/README.md` from 3–8 to 1–6 and `runbooks/README.md` from 2–3 and
  4–6 to 1–2 and 1–3. Those documents number items **continuously across
  sections on purpose**, and the numbers are cross-referenced. The "fix" would
  have falsified item identifiers in a governance index. MD029 is disabled with
  that justification recorded in the config file.
- **Disabled with justification:** MD013 (line length — 99 findings, no defect
  signal, harms diff review of evidence tables), MD060 (introduced in
  markdownlint v0.40 after these documents were written; 274 purely cosmetic
  findings), MD036 (bold field labels such as `**Purpose:**` are data labels,
  not headings).
- **Relaxed:** MD024 to `siblings_only: true`, since review documents repeat
  headings such as "Verified Accurate" under different parents.
- **Fixed properly, not disabled:** MD040 (4 code fences missing a language) and
  MD033 (1 inline `<name>` placeholder).

**Verification.** markdownlint-cli2 exits 0 against all tracked Markdown files
after the change, and the rejected renumbering was confirmed absent from the
final diff.

### BUG-4 — CODEOWNERS enforced nothing (F-04)

**Observed failure.** `gh api orgs/jolarca-dev/teams` returned `[]`. The
CODEOWNERS file assigned ownership to two teams that have never existed.

**Root cause.** The file shipped with a comment reading "Replace team slugs with
actual GitHub team slugs before enabling" and was then committed and pushed
without that step. GitHub does not error on unknown owners; it silently ignores
them, so the file gave the appearance of a review control while enforcing
nothing.

**Fix.** Ownership now points at `@JourneyOfLife`, the sole organisation member.
`tests/test_repository_controls.py::test_codeowners_principals_are_valid` fails
if a team slug reappears while the organisation still has no teams.

### BUG-5 — the published disclosure channel discarded all reports (F-05)

**Observed failure.** A DNS MX query for `jolarca.com` returned no answer
records — only an SOA pointing at `orbit.dns-parking.com` /
`dns.hostinger.com`. The domain is parked.

**Root cause.** `SECURITY.md` named `security@jolarca.com` as the **primary**
disclosure method. With no MX records, mail to that address is discarded.
GitHub private vulnerability reporting, the only alternative mentioned, was
disabled, and is unavailable for this repository because it is private on the
Free plan (the endpoint returns HTTP 404 here, versus HTTP 200 with
`{"enabled":false}` on the organisation's public repositories).

**Impact.** Between 2026-09-26 and 2026-09-28 the organisation had no working
way to receive a vulnerability report. For GDPR Art. 33 the 72-hour notification
clock cannot start on a report nobody receives.

**Fix applied.** Private vulnerability reporting was enabled on the public
`jolarca` repository and verified (`{"enabled":true}`); `SECURITY.md` now names
it the primary channel and states explicitly that the email address is not
deliverable. **Owner action still required:** provision MX records and the
mailbox, then re-verify.

---

## Owner Actions Required

These cannot be completed from the repository or through the CLI. The API fields
involved are documented as response-only: they appear in the `GET /orgs/{org}`
response schema but are not accepted `PATCH` body parameters, so the API returns
HTTP 200 and silently ignores them. That silent no-op was observed directly
during this audit and is the reason these items are listed rather than fixed.

### A1 — Provision the disclosure mailbox (F-05, Critical)

At the DNS provider for `jolarca.com` (currently Hostinger parking):

1. Add MX records for `jolarca.com` pointing at a real mail provider.
2. Create the `security@` mailbox and confirm it is monitored.
3. Verify:

```bash
nslookup -type=MX jolarca.com
```

4. Send a test message and confirm receipt, then update
   `policies/control-matrix.yml` to move `disclosure-email` from `gap` to
   `verified`. The CI test suite will fail until the documentation and the
   matrix agree, which is intentional.

### A2 — Enforce organisation-wide 2FA (F-18, High)

Web UI: **Organisation settings → Authentication security → Require
two-factor authentication for everyone in your organization**.

No lockout risk: the sole member already has 2FA enabled, there are zero outside
collaborators and zero pending invitations (all verified).

Verify afterwards:

```bash
gh api orgs/jolarca-dev --jq '.two_factor_requirement_enabled'
```

Expected: `true`. Note that the API **cannot** set this — a PATCH returns 200
and leaves the value at `false`.

### A3 — Restrict member privileges (F-19, Medium)

Web UI: **Organisation settings → Member privileges**. Disable:

- **Repository visibility change** — threat model entry D-01 is precisely an
  accidental flip of a confidential repository to public.
- **Outside collaborator invites** — least privilege until the team grows.

Verify afterwards:

```bash
gh api orgs/jolarca-dev --jq '{members_can_change_repo_visibility,members_can_invite_outside_collaborators}'
```

Expected: both `false`.

### A4 — Plan upgrade decision (F-17, Medium)

Branch protection, secret scanning, push protection and CodeQL all require
GitHub Team for a private organisation repository (USD 8 per user per month).
Until the upgrade, the compensating controls are: gitleaks in pre-commit and in
CI over full history, mandatory pull requests, GPG-signed commits, an Actions
allowlist, SHA-pinned actions, and the policy-as-code test suite.

Trigger for revisiting: first revenue, first external collaborator, or any
finding that the compensating controls failed to prevent.

When upgrading, apply immediately:

```bash
gh api -X PUT repos/jolarca-dev/jolarca-security/branches/main/protection \
  --input branch-protection.json
```

with required status checks `gitleaks`, `YAML syntax validation`,
`Markdown lint` and `Policy-as-code tests`, `enforce_admins: true`,
`allow_force_pushes: false`, `allow_deletions: false`.

### A5 — Verify controls for the remaining repositories (F-08 follow-up)

This audit verified `jolarca-security`, and spot-checked `jolarca` and
`jolarca-control` only where a claim in this repository depended on them. The
other 13 repositories were **not** audited and their control state is ASSUMED,
not VERIFIED.

Before any document in this repository states a control for another repository,
run per repository:

```bash
for r in $(gh api 'orgs/jolarca-dev/repos?per_page=100' --jq '.[].name'); do
  printf '%s\n' "$r"
  gh api "repos/jolarca-dev/$r/branches/main/protection" \
    --jq '.required_status_checks.contexts' 2>&1 | head -2
  gh api "repos/jolarca-dev/$r" --jq '{visibility,private}'
  gh api "repos/jolarca-dev/$r/actions/permissions" --jq '.allowed_actions'
done
```

Record the result as a per-repository control matrix, or scope every claim in
this repository explicitly to `jolarca-security`. An unscoped claim is the
defect that produced F-08, F-09 and F-10.

---

## Remediation Applied in This Change Set

Settings changes, already applied and verified:

| Change | Command | Verified result |
|--------|---------|-----------------|
| Restrict Actions to an allowlist | `gh api -X PUT .../actions/permissions` with `{"enabled":true,"allowed_actions":"selected"}` | `allowed_actions: "selected"` |
| Define the allowlist | `gh api -X PUT .../actions/permissions/selected-actions` | `{"github_owned_allowed":true,"patterns_allowed":["DavidAnson/*"],"verified_allowed":false}` |
| Enable private vulnerability reporting on `jolarca` | `gh api -X PUT repos/jolarca-dev/jolarca/private-vulnerability-reporting` | `{"enabled":true}` |
| Auto-delete merged branches | `gh api -X PATCH repos/.../jolarca-security` with `{"delete_branch_on_merge":true}` | `true` |
| Replace placeholder billing email | `gh api -X PATCH orgs/jolarca-dev` with `{"billing_email":"..."}` | org contact address |
| Enable Dependabot alerts and dependency graph for new repositories | `gh api -X PATCH orgs/jolarca-dev` | both `true` |

Repository changes, delivered through the pipeline below:

| Commit group | Contents |
|--------------|----------|
| `ci:` | Rewrote gitleaks and lint workflows; added `.markdownlint-cli2.jsonc`; added `.github/dependabot.yml` |
| `fix:` | CODEOWNERS pointed at a real principal; removed `main.py` scaffold |
| `feat:` | Added `LICENSE`, `CONTRIBUTING.md`, `policies/control-matrix.yml`, `tests/`, directory README stubs |
| `docs:` | Corrected README, SECURITY and REVIEW; added this audit report |
| `style:` | Applied the accepted markdownlint autofixes (MD032, MD034, MD022, MD058, MD031) and the manual MD040 and MD033 fixes |

---

## First-Commit Pipeline — Walkthrough and Checkpoints

The repository already had commits, so this pipeline was executed for the
remediation change set. It is the mandatory sequence for every future change and
is reproduced in [CONTRIBUTING.md](../CONTRIBUTING.md).

### Step A — VERIFY FIRST

```bash
git remote -v                     # expect git@github.com:jolarca-dev/jolarca-security.git
git rev-parse --abbrev-ref HEAD   # expect a feature branch, never main
git status --porcelain            # expect no unintended files
ls .git/hooks/pre-commit          # expect the hook to exist
gh api orgs/jolarca-dev --jq '.plan.name'
```

**Checkpoint A:** correct remote, feature branch, clean tree, hook installed.
If any of these fails, stop.

Observed during this audit: branch `chore/readiness-audit-remediation` created
from `4e10a90`; hook present; pre-commit 4.6.2; gitleaks 8.30.1.

### Step B — COMMIT

```bash
git add <explicit paths>          # never git add -A in a compliance repository
git commit -m "ci: pin actions to full SHAs and drop the license-gated scanner"
```

**Checkpoint B:** Conventional Commits format, one logical change per commit,
pre-commit hooks pass, commit is GPG-signed, no secret and no personal data in
the diff — confirmed by reading the diff, not by trusting the hook.

### Step C — PUSH

```bash
git push -u origin chore/readiness-audit-remediation
```

**Checkpoint C:** feature branch only. Never `git push origin main`.

### Step D — REVIEW

```bash
gh pr create --base main --head chore/readiness-audit-remediation --title "..." --body "..."
gh pr checks --watch
```

**Checkpoint D:** description present and explains *why*; findings referenced;
all CI checks green; no unrelated files in the diff; independent review run
against the diff.

### Step E — MERGE

```bash
gh pr merge <number> --merge --delete-branch
```

**Checkpoint E:** all status checks green, no conflicts, no unresolved threads.
Use `--merge` rather than `--squash` so individual conventional commits stay
separately attributable in the audit trail.

**Solo-operator caveat:** GitHub will not let an author approve their own pull
request, so the "one approval" gate is unachievable today. The compensating
controls are the pull request record itself, an independent automated review of
the diff, and a written self-review. This is recorded as control `review-gate`
in the matrix and must not be described as a satisfied approval requirement.

### Step F — VERIFY AGAIN

```bash
git switch main && git pull
git log --oneline -1
gh run list --limit 5
git status --porcelain
gh api repos/jolarca-dev/jolarca-security --jq '{visibility,default_branch,has_wiki,allow_forking}'
```

**Checkpoint F:** the merge landed on `main`; CI on `main` is green; the working
tree is clean; repository settings are unchanged from the audited baseline.

---

## Final Sign-Off Checklist

| # | Check | State |
|---|-------|-------|
| 1 | Repository is private, forkable false, wiki/projects/downloads disabled | VERIFIED |
| 2 | No secrets in working tree or in any commit on any ref | VERIFIED (gitleaks, `--log-opts=--all`, 0 findings) |
| 3 | No deploy keys, no outside collaborators, no teams, default member permission `none` | VERIFIED |
| 4 | All commits GPG-signed | VERIFIED |
| 5 | Proprietary LICENSE present; not AGPL/GPL/MIT/Apache | VERIFIED |
| 6 | CODEOWNERS references only principals that exist | VERIFIED |
| 7 | CI runs on push to `main` **and** on pull requests | VERIFIED |
| 8 | CI is green on the default branch | to be confirmed at Step F |
| 9 | Actions restricted to an allowlist and pinned to full commit SHAs | VERIFIED |
| 10 | Control claims in documentation match the control matrix | VERIFIED by test in CI |
| 11 | A functioning vulnerability disclosure channel exists | PARTIAL — GitHub channel live, mailbox still an owner action |
| 12 | Organisation-wide 2FA enforced | **OPEN — owner action A2** |
| 13 | Member privilege restrictions applied | **OPEN — owner action A3** |
| 14 | Branch protection with required status checks | **NOT POSSIBLE on current plan — accepted risk F-17, owner action A4** |
| 15 | Secret scanning and push protection | **NOT POSSIBLE on current plan — compensating controls in force** |
| 16 | Residual risk documented with remediation triggers | VERIFIED (control matrix) |
| 17 | Control state of the other 15 repositories in the organisation | **NOT VERIFIED — owner action A5** |

**Sign-off.** Items 12, 13 and 14 are open. The repository is
**READY-WITH-FIXES** for continued development and is **not** to be represented
to an auditor, assessor or customer as fully hardened until those items are
closed and re-verified with the commands recorded above.

Signed: ____________________ (Security Officer)  Date: ____________

---

## Residual Risk

| Risk | Likelihood | Impact | Compensating control | Trigger to revisit |
|------|-----------|--------|----------------------|--------------------|
| Force-push or deletion rewrites audit history on `main` | Low | Critical | Signed commits make tampering detectable; policy prohibition in CONTRIBUTING.md | Plan upgrade (A4) |
| A secret is pushed to `main` and not caught | Low | High | gitleaks in pre-commit and over full history in CI on every push | Secret scanning available (A4) |
| A vulnerability report is lost | Medium | Critical | GitHub private vulnerability reporting on the public `jolarca` repository | Mailbox provisioned (A1) |
| A confidential repository is flipped to public | Low | Critical | Visibility is private; `allow_forking` false | Member privileges restricted (A3) |
| Documentation drifts from reality again | Medium | High | Control matrix plus CI tests that bind claims to it | Any control status change |
| Single-operator unavailability | Medium | High | Runbooks, documented compensating controls, external legal counsel | First hire or contractor |

---

## Re-Audit Triggers

Re-run this audit, in full, on any of:

1. Completion of owner actions A1, A2, A3 or A4.
2. Any change of repository visibility, in either direction.
3. Addition of a second operator, collaborator or team.
4. Addition of application code, containers or infrastructure to this repository.
5. Any security incident touching this repository.
6. Quarterly, regardless of the above.

---

## Appendix — Evidence Commands

```bash
# Repository and organisation state
gh api repos/jolarca-dev/jolarca-security --jq '{visibility,private,default_branch,allow_forking,has_wiki,has_projects,delete_branch_on_merge,license}'
gh api orgs/jolarca-dev --jq '{plan:.plan.name,two_factor_requirement_enabled,default_repository_permission,deploy_keys_enabled_for_repositories}'

# Access control
gh api repos/jolarca-dev/jolarca-security/collaborators
gh api repos/jolarca-dev/jolarca-security/teams
gh api repos/jolarca-dev/jolarca-security/keys
gh api orgs/jolarca-dev/outside_collaborators
gh api orgs/jolarca-dev/invitations

# Platform limitations (expect 403 / 404 on the Free plan)
gh api repos/jolarca-dev/jolarca-security/branches/main/protection
gh api repos/jolarca-dev/jolarca-security/rulesets
gh api repos/jolarca-dev/jolarca-security/secret-scanning/alerts
gh api repos/jolarca-dev/jolarca-security/code-scanning/analyses
gh api repos/jolarca-dev/jolarca-security/private-vulnerability-reporting

# Scanning and CI
gh api repos/jolarca-dev/jolarca-security/dependabot/alerts --jq 'length'
gh api repos/jolarca-dev/jolarca-security/actions/permissions
gh api repos/jolarca-dev/jolarca-security/actions/secrets
gh run list --repo jolarca-dev/jolarca-security --limit 25
gh run view <run-id> --repo jolarca-dev/jolarca-security --log-failed

# Local secret scanning over every ref
gitleaks git . --redact --exit-code 1 --log-opts="--all"

# Commit integrity
git log --format='%h %G? %GS %ae' -n 20

# Disclosure channel reachability
nslookup -type=MX jolarca.com
```

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-28 | JourneyOfLife | Initial readiness audit: 21 findings, 5 bugs fixed, 3 owner actions raised |
