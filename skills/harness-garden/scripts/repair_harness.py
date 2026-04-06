#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from string import Template
from typing import Dict, List

from _garden_common import (
    build_profile,
    collect_managed_files,
    detect_doc_language,
    is_managed,
    load_text_template,
    missing_archive_header,
    parse_library,
    render_check_script,
    render_manifest,
    required_paths_for_garden,
    write_file,
)
from audit_harness import audit_repository

PLAN_DATE_PREFIX_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<body>.+)$")
REMEDIATION_PLAN_SLUG = "harness-garden-remediation"


def _date_prefixed_plan_name(plan_date: str, slug: str) -> str:
    return f"{plan_date}-{slug}.md"


def _strip_plan_date_prefix(name: str) -> str:
    stem = Path(name).stem
    matched = PLAN_DATE_PREFIX_RE.match(stem)
    return matched.group("body") if matched else stem


def _plan_display_label(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except UnicodeDecodeError:
        pass
    return _strip_plan_date_prefix(path.name).replace("-", " ").title()


def _resolve_remediation_plan_relpath(repo: Path, plan_date: str, dry_run: bool) -> str:
    active_dir = repo / "docs" / "exec-plans" / "active"
    active_dir.mkdir(parents=True, exist_ok=True)
    dated_candidates = sorted(
        path for path in active_dir.glob(f"*-{REMEDIATION_PLAN_SLUG}.md") if path.is_file()
    )
    if dated_candidates:
        return dated_candidates[-1].relative_to(repo).as_posix()

    target = active_dir / _date_prefixed_plan_name(plan_date, REMEDIATION_PLAN_SLUG)
    legacy = active_dir / f"{REMEDIATION_PLAN_SLUG}.md"
    if legacy.exists() and not target.exists() and not dry_run:
        legacy.replace(target)
    return target.relative_to(repo).as_posix()


def _resolve_active_plan(repo: Path, language: str, prefer_remediation: bool, plan_date: str, dry_run: bool) -> Dict[str, str]:
    if prefer_remediation:
        remediation_relpath = _resolve_remediation_plan_relpath(repo, plan_date, dry_run)
        return {
            "path": remediation_relpath,
            "label": "Harness Garden Remediation" if language == "en" else "Harness Garden Remediation",
        }
    active_dir = repo / "docs" / "exec-plans" / "active"
    if active_dir.exists():
        candidates = sorted(
            str(path.relative_to(repo))
            for path in active_dir.glob("*.md")
            if path.is_file() and path.name != "README.md"
        )
        if candidates:
            first = candidates[-1]
            label = _plan_display_label(repo / first)
            return {"path": first, "label": label}
    return {
        "path": "docs/exec-plans/active/",
        "label": "Active Plans Directory" if language == "en" else "活跃计划目录",
    }


def _repair_doc_context(profile: Dict[str, object], language: str, active_plan: Dict[str, str]) -> Dict[str, str]:
    library = parse_library(Path(__file__).resolve().parent.parent, f"repair-docs.{language}.tpl")
    docs_extra = []
    routes_extra = []
    if profile["has_frontend"]:
        docs_extra.append(library["docs/README.md.extra.frontend"].strip())
        routes_extra.append(library["AGENTS.md.extra.frontend"].strip())
    if profile["complex_architecture"]:
        docs_extra.append(library["docs/README.md.extra.design"].strip())
        routes_extra.append(library["AGENTS.md.extra.design"].strip())
    summary = (
        "该仓库使用 Harness Engineering 控制面管理智能体工作流，要求路由短小、计划可继续、运行态可观察。"
        if language == "zh"
        else "This repository uses a Harness Engineering control plane with concise routing, resumable plans, and observable runtime surfaces."
    )
    local_hints = [f"- `{item}/AGENTS.md`" for item in profile["local_agent_dirs"]]
    if not local_hints:
        local_hints = ["- 暂无额外局部 AGENTS" if language == "zh" else "- No additional local AGENTS yet"]
    structure_summary = (
        f"- 顶层结构：{profile['structure_summary']}"
        if language == "zh"
        else f"- Top-level structure: {profile['structure_summary']}"
    )
    return {
        "PROJECT_NAME": profile["repo_name"],
        "PROJECT_SUMMARY": summary,
        "ACTIVE_PLAN_PATH": active_plan["path"],
        "ACTIVE_PLAN_LABEL": active_plan["label"],
        "EXTRA_ROUTES": "\n".join(routes_extra) if routes_extra else "",
        "LOCAL_AGENT_HINTS": "\n".join(local_hints),
        "STRUCTURE_SUMMARY": structure_summary,
        "DOCS_EXTRA_INDEX": "\n".join(docs_extra) if docs_extra else "",
    }


def _render_repair_doc(
    skill_root: Path,
    language: str,
    rel_path: str,
    profile: Dict[str, object],
    active_plan: Dict[str, str],
) -> str:
    library = parse_library(skill_root, f"repair-docs.{language}.tpl")
    template = Template(library[rel_path])
    return template.substitute(_repair_doc_context(profile, language, active_plan))


def _render_local_agent(skill_root: Path, language: str, target_path: str) -> str:
    template = load_text_template(skill_root, f"local-agent.{language}.md.tpl")
    if language == "zh":
        summary = f"`{target_path}` 是需要局部约束、验证与接手说明的真实工作边界。"
    else:
        summary = f"`{target_path}` is a real workspace boundary that needs local rules, validation, and handoff guidance."
    return template.substitute(
        TARGET_NAME=Path(target_path).name,
        TARGET_PATH=target_path,
        AREA_SUMMARY=summary,
    )


def _prepend_archive_header(path: Path, dry_run: bool) -> None:
    header = (
        "> ✅ Completed: TODO\n"
        "> Summary: TODO\n"
        "> Duration: TODO\n"
        "> Key learnings: TODO\n\n"
    )
    content = path.read_text(encoding="utf-8")
    write_file(path, header + content, dry_run)


def _write_remediation_plan(
    skill_root: Path,
    repo: Path,
    language: str,
    high_risk_findings: List[Dict[str, str]],
    auto_fixed: List[str],
    plan_date: str,
    dry_run: bool,
) -> str:
    template = load_text_template(skill_root, f"remediation-plan.{language}.md.tpl")
    plan_path = repo / _resolve_remediation_plan_relpath(repo, plan_date, dry_run)
    content = template.substitute(
        DATE=plan_date,
        HIGH_RISK_FINDINGS=(
            "\n".join(
                f"- [{item['severity']}] `{item['code']}` {item['path']} -> {item['message']}"
                for item in high_risk_findings
            )
            or ("- 无" if language == "zh" else "- none")
        ),
        AUTO_FIXED=(
            "\n".join(f"- {item}" for item in auto_fixed)
            or ("- 无" if language == "zh" else "- none")
        ),
    )
    write_file(plan_path, content, dry_run)
    return str(plan_path.relative_to(repo))


def repair_repository(repo: Path, mode: str, dry_run: bool, plan_date: str) -> Dict[str, object]:
    skill_root = Path(__file__).resolve().parent.parent
    audit = audit_repository(repo, "standard")
    language = detect_doc_language(repo)
    profile = build_profile(repo)
    created: List[str] = []
    updated: List[str] = []
    high_risk: List[Dict[str, str]] = []

    if mode == "report-only":
        return {
            "repo": str(repo),
            "language": language,
            "audit": audit,
            "created": created,
            "updated": updated,
            "high_risk_plan": None,
        }

    prefer_remediation = any(finding["action"] != "safe-fix" for finding in audit["findings"])
    active_plan = _resolve_active_plan(repo, language, prefer_remediation, plan_date, dry_run)

    for finding in audit["findings"]:
        if finding["action"] != "safe-fix":
            high_risk.append(finding)
            continue

        rel_path = finding["path"]
        path = repo / rel_path
        code = finding["code"]

        if code == "missing-file" and rel_path in required_paths_for_garden(repo):
            content = _render_repair_doc(skill_root, language, rel_path, profile, active_plan)
            write_file(path, content, dry_run)
            created.append(rel_path)
            continue

        if code == "missing-local-agent":
            target_dir = rel_path.rsplit("/", 1)[0]
            write_file(path, _render_local_agent(skill_root, language, target_dir), dry_run)
            created.append(rel_path)
            continue

        if code == "missing-archive-header" and path.exists():
            _prepend_archive_header(path, dry_run)
            updated.append(rel_path)
            continue

        if rel_path == "AGENTS.md" and code in {"root-agent-too-large", "missing-plans-route", "missing-route"} and is_managed(path):
            write_file(path, _render_repair_doc(skill_root, language, "AGENTS.md", profile, active_plan), dry_run)
            updated.append(rel_path)
            continue

        if rel_path == "docs/PLANS.md" and code in {"plans-too-large", "plans-missing-active-pointer", "plans-missing-active-entry"} and is_managed(path):
            write_file(path, _render_repair_doc(skill_root, language, "docs/PLANS.md", profile, active_plan), dry_run)
            updated.append(rel_path)
            continue

        if code == "local-agent-too-large" and is_managed(path):
            target_dir = rel_path.rsplit("/", 1)[0]
            write_file(path, _render_local_agent(skill_root, language, target_dir), dry_run)
            updated.append(rel_path)

    remediation_plan = None
    if high_risk:
        remediation_plan = _write_remediation_plan(
            skill_root,
            repo,
            language,
            high_risk,
            created + updated,
            plan_date,
            dry_run,
        )
        active_plan = _resolve_active_plan(repo, language, True, plan_date, dry_run)
        plans_path = repo / "docs" / "PLANS.md"
        if plans_path.exists() and is_managed(plans_path):
            write_file(
                plans_path,
                _render_repair_doc(skill_root, language, "docs/PLANS.md", profile, active_plan),
                dry_run,
            )
            updated.append("docs/PLANS.md")

    manifest_path = repo / "docs" / "generated" / "harness-manifest.md"
    check_path = repo / "scripts" / "check_harness.py"
    if not dry_run:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        check_path.parent.mkdir(parents=True, exist_ok=True)
    post_profile = build_profile(repo)
    managed_touched = [
        rel_path
        for rel_path in created + updated
        if rel_path in {"docs/generated/harness-manifest.md", "scripts/check_harness.py"}
        or (repo / rel_path).exists() and is_managed(repo / rel_path)
    ]
    post_managed_files = sorted(
        set(
            collect_managed_files(repo)
            + managed_touched
            + ["docs/generated/harness-manifest.md", "scripts/check_harness.py"]
        )
    )
    write_file(manifest_path, render_manifest(skill_root, repo, language, post_managed_files), dry_run)
    write_file(check_path, render_check_script(skill_root, post_profile), dry_run)
    if not dry_run and check_path.exists():
        check_path.chmod(0o755)
    if "docs/generated/harness-manifest.md" not in created:
        updated.append("docs/generated/harness-manifest.md")
    if "scripts/check_harness.py" not in created:
        updated.append("scripts/check_harness.py")

    return {
        "repo": str(repo),
        "language": language,
        "audit": audit,
        "created": sorted(set(created)),
        "updated": sorted(set(updated)),
        "high_risk_plan": remediation_plan,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair low-risk Harness drift and plan high-risk corrections")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--mode", choices=("safe-fix", "report-only"), default="safe-fix")
    parser.add_argument("--date", default=date.today().isoformat(), help="Plan creation date")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--format", choices=("json", "md"), default="md")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    result = repair_repository(repo, args.mode, args.dry_run, args.date)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("# Harness Repair")
        print()
        print(f"- Repo: `{result['repo']}`")
        print(f"- Created: {len(result['created'])}")
        print(f"- Updated: {len(result['updated'])}")
        print(f"- High-risk plan: `{result['high_risk_plan']}`")
        if result["created"]:
            print()
            print("## Created")
            print()
            for item in result["created"]:
                print(f"- `{item}`")
        if result["updated"]:
            print()
            print("## Updated")
            print()
            for item in result["updated"]:
                print(f"- `{item}`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
