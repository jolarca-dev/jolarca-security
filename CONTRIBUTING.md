# Contributing to jolarca-security

This repository holds compliance evidence for the jolarca-dev organisation:
security policies, threat models, incident response procedures, vulnerability
records and audit reports. Treat every change as if it will be read by an
auditor, a regulator and an attacker — because all three eventually will.

Changes here are held to a higher standard than ordinary application code.
Follow the process below exactly; do not improvise.

## Ground Rules

- **Never commit secrets, credentials, tokens, private keys or customer data.**
  Not even as an example, not even "temporarily", not even in a branch you plan
  to delete. Once pushed, assume it is compromised and rotate it.
- **Never commit personal data (GDPR).** Incident records must reference
  individuals by role or pseudonymised identifier, never by name plus contact
  details.
- **Never force-push or rewrite history on `main`.** This repository is an
  audit trail; rewriting it destroys the evidence value of the record.
- **Claims must be evidenced.** If a document states that a control exists, the
  control must exist and be verifiable. Record it in
  [policies/control-matrix.yml](policies/control-matrix.yml).
- **Do not delete findings or audit records.** Correct them by appending a
  dated addendum. Superseded evidence stays in history for a reason.

## Environment Setup

Requires Python 3.12+, [git](https://git-scm.com), and
[gitleaks](https://github.com/gitleaks/gitleaks) v8.30.1 or newer.

```bash
git clone git@github.com:jolarca-dev/jolarca-security.git
cd jolarca-security
python3 -m venv .venv --upgrade-deps
.venv/bin/pip install pre-commit pytest pyyaml
.venv/bin/pre-commit install
```

Verify the hooks are installed and passing before your first commit:

```bash
.venv/bin/pre-commit run --all-files
```

Note for Debian/Ubuntu: system `pip3 install --user` is blocked by PEP 668 and
`ensurepip` may be disabled. Always use the project virtualenv created above.

## Change Pipeline

Every change follows this sequence. Skipping a step is a process deviation and
must be recorded in the audit trail if it happens.

### Step A — Verify First

Before writing anything, confirm:

```bash
git remote -v                       # correct repository
git rev-parse --abbrev-ref HEAD     # correct branch, never main
git status --porcelain              # clean of unintended files
gh api orgs/jolarca-dev --jq '.plan.name'
```

If any check fails, stop and resolve it before continuing.

### Step B — Commit

Use [Conventional Commits](https://www.conventionalcommits.org), one logical
change per commit. Commits are GPG-signed; signing is configured globally and
must not be disabled.

```text
feat:     a new policy, runbook or control
fix:      correction of an inaccurate or broken statement
docs:     documentation only, no control change
ci:       workflow or automation change
chore:    tooling, configuration, repository hygiene
test:     policy-as-code tests
style:    formatting only, no semantic change
```

### Step C — Push

Push to a feature branch only. Never push directly to `main`.

```bash
git switch -c chore/short-description
git push -u origin chore/short-description
```

### Step D — Review

Open a pull request and complete the checklist below before requesting merge.
Run the same checks CI will run:

```bash
.venv/bin/pre-commit run --all-files
.venv/bin/pytest -q
gitleaks git . --redact --exit-code 1 --log-opts="--all"
```

### Step E — Merge

Merge only when CI is green and the review checklist is complete. Use a merge
commit rather than a squash so that individual conventional commits remain
separately attributable in the audit trail.

### Step F — Verify Again

After merging, confirm the change actually landed and did not alter anything
else:

```bash
git switch main && git pull
git log --oneline -1
gh run list --limit 5
git status --porcelain
```

## Pull Request Checklist

- Description explains **what** changed and **why**, referencing the finding or
  incident that prompted it.
- Every new or changed control claim is reflected in
  [policies/control-matrix.yml](policies/control-matrix.yml).
- `.venv/bin/pytest -q` passes locally.
- No unrelated files, no build artefacts, no editor state.
- No secrets, no personal data — confirmed by re-reading your own diff.
- Document history table updated where the document has one.

## Review Capacity — Single Operator

This organisation currently has one member and zero teams. GitHub does not
permit a pull request author to approve their own pull request, so a
"one approval" gate cannot be satisfied today. Until a second operator exists,
the compensating controls are:

1. Feature branches and pull requests are still mandatory, so every change has
   a recorded review surface and a CI result.
2. An independent automated review is run against the diff before merge.
3. The author records an explicit self-review against the checklist above in
   the pull request description.
4. The deviation is documented as an accepted risk with a remediation trigger
   in [policies/control-matrix.yml](policies/control-matrix.yml).

## Markdown and YAML Standards

Linting is enforced in CI. The rule policy and the justification for each
deviation live in `.markdownlint-cli2.jsonc`. Do not disable a lint rule
without adding a written justification there.

Do not renumber ordered lists to satisfy a linter. Several index documents
number items continuously across sections, and those numbers are referenced
elsewhere.

## Reporting a Vulnerability

Do not open a public issue. Follow [SECURITY.md](SECURITY.md).
