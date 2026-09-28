"""Policy-as-code tests for the jolarca-security repository.

This suite is the enforcement layer for the repository readiness audit of
2026-09-28. Each test names the audit finding it guards, so that a change which
reintroduces a defect fails here rather than in production or in front of an
auditor.

Findings register: audits/2026-09-28-repository-readiness-audit.md
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_DIR = ROOT / ".github" / "workflows"
MATRIX_PATH = ROOT / "policies" / "control-matrix.yml"
README = ROOT / "README.md"
SECURITY = ROOT / "SECURITY.md"
REVIEW = ROOT / "REVIEW.md"

VALID_STATUSES = frozenset({"verified", "compensating", "gap"})

# The organisation has zero teams (verified 2026-09-28 via
# `gh api orgs/jolarca-dev/teams`), so any team slug in CODEOWNERS is by
# definition an invalid principal that GitHub silently ignores.
VALID_CODEOWNERS = frozenset({"@JourneyOfLife"})

FULL_COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
SKIP_DIRS = frozenset({".git", ".venv", "node_modules", "__pycache__", ".idea"})

REQUIRED_DOCUMENTS = (
    "README.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "LICENSE",
    ".gitignore",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".pre-commit-config.yaml",
    ".markdownlint-cli2.jsonc",
    "policies/control-matrix.yml",
)

# Root cause of finding F-08: controls verified in one repository were asserted
# as fleet-wide. Any unscoped universal claim must fail.
FORBIDDEN_FLEET_CLAIMS = (
    "All jolarca-dev repositories enforce",
    "all receiving security updates",
)

# Built by concatenation so that this test file never contains a literal that
# gitleaks or the detect-private-key hook would flag.
SECRET_PATTERNS = (
    re.compile(r"AKIA" + r"[0-9A-Z]{16}"),
    re.compile(r"ghp_" + r"[A-Za-z0-9]{36}"),
    re.compile(r"github_pat_" + r"[A-Za-z0-9_]{22,}"),
    re.compile(r"xox[baprs]-" + r"[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN " + r"[A-Z ]*PRIVATE KEY-----"),
)


def _tracked_files() -> list[Path]:
    return sorted(
        p
        for p in ROOT.rglob("*")
        if p.is_file() and not any(part in SKIP_DIRS for part in p.parts)
    )


def _tracked_markdown() -> list[Path]:
    return [p for p in _tracked_files() if p.suffix == ".md"]


def _load_matrix() -> dict:
    return yaml.safe_load(MATRIX_PATH.read_text(encoding="utf-8"))


def _load_workflows() -> dict[str, dict]:
    return {
        p.name: yaml.safe_load(p.read_text(encoding="utf-8"))
        for p in sorted(WORKFLOW_DIR.glob("*.y*ml"))
    }


def _iter_uses(node) -> list[str]:
    """Collect every `uses:` action reference in a workflow document."""
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "uses" and isinstance(value, str):
                found.append(value)
            else:
                found.extend(_iter_uses(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(_iter_uses(item))
    return found


def _strip_code_fences(text: str) -> str:
    """Remove fenced code blocks so prose rules do not match shell comments."""
    return re.sub(r"^```.*?^```", "", text, flags=re.DOTALL | re.MULTILINE)


def _triggers(doc: dict):
    # PyYAML resolves the bare YAML 1.1 key `on` to boolean True.
    return doc.get("on", doc.get(True))


# --- Structure -------------------------------------------------------------


def test_required_governance_documents_exist() -> None:
    """F-06, F-07, F-11: mandatory governance files must exist and be non-empty."""
    missing = [
        rel
        for rel in REQUIRED_DOCUMENTS
        if not (ROOT / rel).is_file() or (ROOT / rel).stat().st_size == 0
    ]
    assert not missing, f"missing or empty required documents: {missing}"


def test_license_is_proprietary_not_copyleft() -> None:
    """F-06: the repository must be proprietary, never AGPL/GPL/MIT/Apache."""
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "All Rights Reserved" in text
    assert "NOT open source" in text
    for grant in (
        "Permission is hereby granted, free of charge",
        "This program is free software",
        "Licensed under the Apache License",
    ):
        assert grant not in text, f"LICENSE contains an open-source grant: {grant!r}"


def test_no_ide_scaffold_files() -> None:
    """F-14: IDE sample scaffolding must not ship in a governance repository."""
    assert not (ROOT / "main.py").exists(), "PyCharm sample main.py is still present"


def test_documented_directories_are_tracked() -> None:
    """F-15: git cannot track empty directories; documented dirs need content."""
    for name in ("metrics", "pentest-reports", "audits", "tests"):
        path = ROOT / name
        assert path.is_dir(), f"{name}/ does not exist"
        assert any(path.iterdir()), f"{name}/ is empty and therefore untracked by git"


def test_markdown_documents_start_with_a_single_h1() -> None:
    """Structural integrity of every governance document."""
    for path in _tracked_markdown():
        prose = _strip_code_fences(path.read_text(encoding="utf-8"))
        lines = [ln for ln in prose.splitlines() if ln.strip()]
        assert lines, f"{path.name} is empty"
        assert lines[0].startswith("# "), f"{path.name} does not start with an H1"
        extra = [ln for ln in lines[1:] if ln.startswith("# ")]
        assert not extra, f"{path.name} has more than one H1: {extra}"


def test_no_secret_material_in_tracked_files() -> None:
    """Defence in depth alongside gitleaks: no credential-shaped strings."""
    hits = []
    for path in _tracked_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        hits.extend(
            f"{path.relative_to(ROOT)}: {pattern.pattern}"
            for pattern in SECRET_PATTERNS
            if pattern.search(text)
        )
    assert not hits, f"possible secret material committed: {hits}"


def test_gitignore_blocks_secret_material() -> None:
    """Defence in depth: ignore rules must cover env files, keys and tool state."""
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in (".env", "*.pem", "*.key", ".venv/", "secrets/", ".idea/"):
        assert pattern in text, f".gitignore does not exclude {pattern}"


# --- Access control --------------------------------------------------------


def test_codeowners_principals_are_valid() -> None:
    """F-04 regression guard: CODEOWNERS must not reference non-existent teams."""
    text = (ROOT / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
    principals: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        principals.update(t for t in stripped.split()[1:] if t.startswith("@"))
    assert principals, "CODEOWNERS declares no owners"
    invalid = principals - VALID_CODEOWNERS
    assert not invalid, (
        f"CODEOWNERS references principals that do not exist in the "
        f"organisation: {sorted(invalid)}"
    )


# --- CI/CD -----------------------------------------------------------------


def test_workflows_are_valid_yaml() -> None:
    workflows = _load_workflows()
    assert workflows, "no workflow files found"
    for name, doc in workflows.items():
        assert isinstance(doc, dict), f"{name} did not parse to a mapping"
        assert doc.get("name"), f"{name} has no workflow name"
        assert doc.get("jobs"), f"{name} has no jobs"


def test_action_references_are_pinned_to_full_commit_sha() -> None:
    """F-01 regression guard: GitHub Actions rejects abbreviated commit SHAs."""
    offenders = []
    for name, doc in _load_workflows().items():
        for ref in _iter_uses(doc):
            if ref.startswith("./") or ref.startswith("docker://"):
                continue
            _, _, revision = ref.partition("@")
            if not FULL_COMMIT_SHA.match(revision):
                offenders.append(f"{name}: '{ref}' is not pinned to a full 40-char SHA")
    assert not offenders, f"unpinned action references: {offenders}"


def test_workflows_declare_least_privilege_permissions() -> None:
    """F-12: workflows must scope GITHUB_TOKEN and request read-only access."""
    for name, doc in _load_workflows().items():
        permissions = doc.get("permissions")
        assert isinstance(permissions, dict) and permissions, (
            f"{name} does not declare least-privilege permissions"
        )
        for scope, level in permissions.items():
            assert level == "read", (
                f"{name} grants {scope}: {level}; write access needs written justification"
            )


def test_workflows_run_on_push_to_default_branch() -> None:
    """F-02 regression guard: a PR-only trigger never ran on this repository."""
    for name, doc in _load_workflows().items():
        triggers = _triggers(doc)
        assert triggers, f"{name} declares no triggers"
        push = triggers.get("push") if isinstance(triggers, dict) else None
        assert isinstance(push, dict), f"{name} has no push trigger"
        assert "main" in push.get("branches", []), f"{name} does not run on push to main"


def test_gitleaks_workflow_is_license_free_and_checksum_verified() -> None:
    """F-01 regression guard: the license-gated action and unpinned binary.

    The check inspects parsed `uses:` references rather than raw text, so the
    design note explaining why the action was removed does not trip the guard.
    """
    doc = yaml.safe_load((WORKFLOW_DIR / "gitleaks.yml").read_text(encoding="utf-8"))
    for ref in _iter_uses(doc):
        assert "gitleaks-action" not in ref, (
            f"'{ref}' requires GITLEAKS_LICENSE for organisation repositories"
        )
    text = (WORKFLOW_DIR / "gitleaks.yml").read_text(encoding="utf-8")
    assert "sha256sum -c" in text, "gitleaks download is not checksum verified"
    assert re.search(r"[0-9a-f]{64}", text), "no sha256 pin present in gitleaks workflow"
    assert "--log-opts" in text, "gitleaks must scan all refs, not just HEAD"
    assert "--redact" in text, "gitleaks must redact findings so secrets never reach CI logs"


def test_dependabot_covers_required_ecosystems() -> None:
    """F-11 regression guard."""
    config = yaml.safe_load((ROOT / ".github" / "dependabot.yml").read_text(encoding="utf-8"))
    assert config["version"] == 2
    ecosystems = {u["package-ecosystem"] for u in config["updates"]}
    assert {"github-actions", "pip"} <= ecosystems, f"missing ecosystems: {ecosystems}"


def test_precommit_runs_secret_scanning() -> None:
    """Compensating control for the absence of GitHub secret scanning (F-17)."""
    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hook_ids = {h["id"] for repo in config["repos"] for h in repo["hooks"]}
    assert {"gitleaks", "detect-private-key"} <= hook_ids, f"hooks present: {sorted(hook_ids)}"


# --- Control matrix and document integrity ---------------------------------


def test_control_matrix_is_well_formed() -> None:
    """F-08: every control must declare a status and support it with evidence."""
    matrix = _load_matrix()
    controls = matrix["controls"]
    assert controls, "control matrix declares no controls"

    ids = [c["id"] for c in controls]
    assert len(ids) == len(set(ids)), "duplicate control ids in the matrix"

    for control in controls:
        cid = control["id"]
        status = control.get("status")
        assert status in VALID_STATUSES, f"{cid}: invalid status {status!r}"

        if status == "verified":
            assert control.get("verify"), f"{cid}: verified controls need a verify command"
            evidence = control.get("evidence")
            if evidence:
                assert (ROOT / evidence).exists(), f"{cid}: evidence file {evidence} missing"

        if status == "compensating":
            assert control.get("rationale"), f"{cid}: compensating controls need a rationale"
            target = control.get("compensates_for")
            assert target in ids, f"{cid}: compensates_for '{target}' is not a known control"

        if status == "gap":
            assert control.get("rationale"), f"{cid}: gaps need a rationale"
            assert control.get("remediation"), f"{cid}: gaps need a remediation path"


def test_document_control_claims_match_the_matrix() -> None:
    """F-08/F-09 regression guard: documents may not overstate controls.

    A status marker next to a bold control name in README.md or SECURITY.md is
    only valid if the control matrix records that exact status, and every
    control carrying a doc_claim must appear in the documentation.
    """
    matrix = _load_matrix()
    markers = matrix["claim_markers"]
    status_of_marker = {marker: status for status, marker in markers.items()}
    marker_re = re.compile(
        r"(" + "|".join(re.escape(m) for m in markers.values()) + r")\s*\*\*(.+?)\*\*"
    )

    claim_status: dict[str, str] = {}
    for control in matrix["controls"]:
        claim = control.get("doc_claim")
        if claim:
            claim_status[claim.lower()] = control["status"]

    problems: list[str] = []
    documented: set[str] = set()

    for doc in (README, SECURITY):
        text = _strip_code_fences(doc.read_text(encoding="utf-8"))
        for marker, claim in marker_re.findall(text):
            key = claim.strip().lower()
            documented.add(key)
            expected = status_of_marker[marker]
            actual = claim_status.get(key)
            if actual != expected:
                problems.append(
                    f"{doc.name}: '{claim}' is marked {marker} ({expected}) but the "
                    f"control matrix records {actual!r}"
                )

    undocumented = sorted(set(claim_status) - documented)
    if undocumented:
        problems.append(
            f"controls present in the matrix but absent from documentation: {undocumented}"
        )

    assert not problems, "document/control-matrix mismatch:\n" + "\n".join(problems)


def test_no_unscoped_fleet_control_claims() -> None:
    """F-08 root cause: controls verified in one repo were asserted fleet-wide."""
    for doc in (README, SECURITY):
        text = doc.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_FLEET_CLAIMS:
            assert phrase not in text, f"{doc.name} still asserts {phrase!r}"


def test_security_policy_scope_matches_the_organisation() -> None:
    """F-09 regression guard: PCI-scoped payments repo was missing from scope."""
    text = SECURITY.read_text(encoding="utf-8")
    assert "jolarca-payments" in text, "SECURITY.md omits the payments repository"
    assert "16 repositories" in text, "SECURITY.md states a stale repository count"


def test_review_document_carries_a_correction_addendum() -> None:
    """F-10: the overclaiming review stays in history, with its correction."""
    text = REVIEW.read_text(encoding="utf-8")
    assert "## Addendum" in text, "REVIEW.md has no dated correction addendum"
    assert "retract" in text.lower(), "REVIEW.md addendum does not retract the prior claim"


def test_audit_report_is_present() -> None:
    """The audit that produced these tests is itself evidence and must be kept."""
    reports = list((ROOT / "audits").glob("*repository-readiness-audit.md"))
    assert reports, "no repository readiness audit report found in audits/"
