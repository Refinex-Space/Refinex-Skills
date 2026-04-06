#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List

from _garden_common import (
    build_profile,
    bullet_list,
    collect_managed_files,
    detect_doc_language,
    is_managed,
    load_text_template,
    missing_archive_header,
    render_check_script,
    render_manifest,
    required_paths_for_garden,
)

PLAN_FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")


def _has_dated_plan_name(path: Path) -> bool:
    return bool(PLAN_FILENAME_RE.match(path.name))


def _append_finding(
    findings: List[Dict[str, str]],
    severity: str,
    code: str,
    path: str,
    message: str,
    action: str,
) -> None:
    key = (severity, code, path, message)
    if any((item["severity"], item["code"], item["path"], item["message"]) == key for item in findings):
        return
    findings.append(
        {
            "severity": severity,
            "code": code,
            "path": path,
            "message": message,
            "action": action,
        }
    )


def _missing_file_severity(rel_path: str) -> str:
    if rel_path in {"AGENTS.md", "ARCHITECTURE.md", "docs/PLANS.md"}:
        return "P0"
    if rel_path in {
        "docs/SECURITY.md",
        "docs/RELIABILITY.md",
        "docs/OBSERVABILITY.md",
        "docs/QUALITY_SCORE.md",
        "docs/exec-plans/tech-debt-tracker.md",
    }:
        return "P1"
    return "P2"


def audit_repository(repo: Path, strictness: str) -> Dict[str, object]:
    skill_root = Path(__file__).resolve().parent.parent
    profile = build_profile(repo)
    findings: List[Dict[str, str]] = []

    for rel_path in required_paths_for_garden(repo):
        path = repo / rel_path
        if not path.exists():
            _append_finding(
                findings,
                _missing_file_severity(rel_path),
                "missing-file",
                rel_path,
                f"Missing Harness file: {rel_path}",
                "safe-fix",
            )

    root_agents = repo / "AGENTS.md"
    root_budget = 140 if strictness == "standard" else 120
    if root_agents.exists():
        content = root_agents.read_text(encoding="utf-8")
        if len(content.splitlines()) > root_budget:
            action = "safe-fix" if is_managed(root_agents) else "manual-plan"
            _append_finding(
                findings,
                "P1",
                "root-agent-too-large",
                "AGENTS.md",
                f"Root AGENTS.md exceeds {root_budget} lines and is no longer a clean routing map",
                action,
            )
        if "docs/PLANS.md" not in content:
            action = "safe-fix" if is_managed(root_agents) else "manual-plan"
            _append_finding(
                findings,
                "P1",
                "missing-plans-route",
                "AGENTS.md",
                "Root AGENTS.md does not route to docs/PLANS.md",
                action,
            )
        for rel_path in profile["route_docs"]:
            if rel_path not in content:
                action = "safe-fix" if is_managed(root_agents) else "manual-plan"
                _append_finding(
                    findings,
                    "P2",
                    "missing-route",
                    "AGENTS.md",
                    f"Root AGENTS.md does not route to {rel_path}",
                    action,
                )

    plans_path = repo / "docs" / "PLANS.md"
    active_dir = repo / "docs" / "exec-plans" / "active"
    plans_budget = 180 if strictness == "standard" else 150
    if plans_path.exists():
        plans_text = plans_path.read_text(encoding="utf-8")
        if len(plans_text.splitlines()) > plans_budget:
            action = "safe-fix" if is_managed(plans_path) else "manual-plan"
            _append_finding(
                findings,
                "P2",
                "plans-too-large",
                "docs/PLANS.md",
                f"PLANS.md exceeds {plans_budget} lines and should remain a short routing index",
                action,
            )
        if active_dir.exists():
            active_plan_paths = [
                path for path in active_dir.glob("*.md") if path.is_file() and path.name != "README.md"
            ]
            active_plans = [path.name for path in active_plan_paths]
            if active_plans and "docs/exec-plans/active" not in plans_text:
                action = "safe-fix" if is_managed(plans_path) else "manual-plan"
                _append_finding(
                    findings,
                    "P1",
                    "plans-missing-active-pointer",
                    "docs/PLANS.md",
                    "PLANS.md does not mention docs/exec-plans/active",
                    action,
                )
            for plan_path in active_plan_paths:
                if not _has_dated_plan_name(plan_path):
                    _append_finding(
                        findings,
                        "P2",
                        "plan-missing-date-prefix",
                        str(plan_path.relative_to(repo)),
                        "Execution plan filename must start with YYYY-MM-DD-",
                        "manual-plan",
                    )
                if plan_path.name not in plans_text:
                    action = "safe-fix" if is_managed(plans_path) else "manual-plan"
                    _append_finding(
                        findings,
                        "P2",
                        "plans-missing-active-entry",
                        "docs/PLANS.md",
                        f"PLANS.md does not mention active plan {plan_path.name}",
                        action,
                    )

    for target_dir in profile["local_agent_dirs"]:
        path = repo / target_dir / "AGENTS.md"
        if not path.exists():
            _append_finding(
                findings,
                "P1",
                "missing-local-agent",
                f"{target_dir}/AGENTS.md",
                f"Missing local AGENTS.md for workspace boundary {target_dir}",
                "safe-fix",
            )
            continue
        if len(path.read_text(encoding="utf-8").splitlines()) > 120:
            action = "safe-fix" if is_managed(path) else "manual-plan"
            _append_finding(
                findings,
                "P2",
                "local-agent-too-large",
                f"{target_dir}/AGENTS.md",
                "Local AGENTS.md is too large and should stay boundary-specific",
                action,
            )

    manifest = repo / "docs" / "generated" / "harness-manifest.md"
    expected_manifest = render_manifest(skill_root, repo, detect_doc_language(repo), collect_managed_files(repo))
    if not manifest.exists():
        _append_finding(
            findings,
            "P2",
            "missing-manifest",
            "docs/generated/harness-manifest.md",
            "Harness manifest is missing",
            "safe-fix",
        )
    else:
        current_manifest = manifest.read_text(encoding="utf-8")
        if current_manifest != expected_manifest:
            _append_finding(
                findings,
                "P2",
                "stale-manifest",
                "docs/generated/harness-manifest.md",
                "Harness manifest is stale relative to the current repository profile",
                "safe-fix",
            )

    check_script = repo / "scripts" / "check_harness.py"
    expected_check = render_check_script(skill_root, profile)
    if not check_script.exists():
        _append_finding(
            findings,
            "P2",
            "missing-check-script",
            "scripts/check_harness.py",
            "Repo-local Harness check script is missing",
            "safe-fix",
        )
    else:
        current_check = check_script.read_text(encoding="utf-8")
        if current_check != expected_check:
            _append_finding(
                findings,
                "P2",
                "stale-check-script",
                "scripts/check_harness.py",
                "Repo-local Harness check script is stale relative to the current repository profile",
                "safe-fix",
            )
        try:
            result = subprocess.run(
                ["python3", str(check_script), "--repo", str(repo), "--format", "json"],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            payload = json.loads(result.stdout or "{}")
            for item in payload.get("findings", []):
                path = item.get("path", ".")
                manual = path in {"AGENTS.md", "docs/PLANS.md"} and not is_managed(repo / path)
                _append_finding(
                    findings,
                    item.get("severity", "P2"),
                    item.get("code", "repo-check"),
                    path,
                    item.get("message", "Harness check reported a problem"),
                    "manual-plan" if manual else "safe-fix",
                )
        except Exception:
            _append_finding(
                findings,
                "P2",
                "check-script-failed",
                "scripts/check_harness.py",
                "Repo-local Harness check script could not be executed cleanly",
                "safe-fix",
            )

    completed_dir = repo / "docs" / "exec-plans" / "completed"
    if completed_dir.exists():
        for path in sorted(completed_dir.glob("*.md")):
            if path.name == "README.md":
                continue
            if not _has_dated_plan_name(path):
                _append_finding(
                    findings,
                    "P2",
                    "plan-missing-date-prefix",
                    str(path.relative_to(repo)),
                    "Execution plan filename must start with YYYY-MM-DD-",
                    "manual-plan",
                )
            if missing_archive_header(path):
                _append_finding(
                    findings,
                    "P2",
                    "missing-archive-header",
                    str(path.relative_to(repo)),
                    "Completed plan is missing the standard archive header",
                    "safe-fix",
                )

    findings.sort(key=lambda item: (item["severity"], item["path"], item["code"], item["message"]))
    return {
        "repo": str(repo),
        "language": detect_doc_language(repo),
        "profile": profile,
        "findings": findings,
    }


def render_markdown(skill_root: Path, result: Dict[str, object]) -> str:
    template = load_text_template(skill_root, f"audit-report.{result['language']}.md.tpl")
    findings: List[Dict[str, str]] = result["findings"]
    by_severity = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    for item in findings:
        by_severity[item["severity"]] = by_severity.get(item["severity"], 0) + 1
    summary_lines = bullet_list(
        [
            f"P0: {by_severity.get('P0', 0)}",
            f"P1: {by_severity.get('P1', 0)}",
            f"P2: {by_severity.get('P2', 0)}",
            f"P3: {by_severity.get('P3', 0)}",
        ],
        "No findings",
    )
    finding_lines = bullet_list(
        [
            f"[{item['severity']}] `{item['code']}` {item['path']} -> {item['message']} ({item['action']})"
            for item in findings
        ],
        "No findings",
    )
    return template.substitute(
        REPO_PATH=result["repo"],
        LANGUAGE=result["language"],
        SUMMARY_LINES=summary_lines,
        FINDING_LINES=finding_lines,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit repository Harness health")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--format", choices=("json", "md"), default="md")
    parser.add_argument("--strictness", choices=("standard", "high"), default="standard")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    result = audit_repository(repo, args.strictness)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(Path(__file__).resolve().parent.parent, result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
