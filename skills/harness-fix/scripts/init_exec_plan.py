#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path

from _plan_common import (
    detect_doc_language,
    format_block,
    load_template,
    next_markdown_path,
    normalize_slug,
    normalize_text,
    repo_harness_signals,
    run_repo_check,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a fix execution plan")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--title", required=True, help="Plan title")
    parser.add_argument("--severity", help="Issue severity")
    parser.add_argument("--goal", help="Repair goal")
    parser.add_argument("--impact", help="Impact scope")
    parser.add_argument("--expected", help="Expected behavior")
    parser.add_argument("--observed", help="Observed behavior")
    parser.add_argument("--rollback", help="Rollback or mitigation path")
    parser.add_argument("--owner", default="Codex / Claude Agent", help="Plan owner")
    parser.add_argument("--slug", help="Custom filename slug")
    parser.add_argument("--language", choices=("auto", "zh", "en"), default="auto", help="Plan language")
    parser.add_argument("--date", default=date.today().isoformat(), help="Creation date")
    parser.add_argument("--evidence", action="append", default=[], help="Existing evidence, repeatable")
    parser.add_argument("--reproduction", action="append", default=[], help="Reproduction step, repeatable")
    parser.add_argument("--surface", action="append", default=[], help="Likely surface, repeatable")
    parser.add_argument("--hypothesis", action="append", default=[], help="Root-cause hypothesis, repeatable")
    parser.add_argument("--validation", action="append", default=[], help="Validation item, repeatable")
    parser.add_argument("--doc", action="append", default=[], help="Document to sync, repeatable")
    parser.add_argument("--risk", action="append", default=[], help="Residual risk, repeatable")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--skip-sync", action="store_true", help="Do not sync docs/PLANS.md after creation")
    return parser.parse_args()


def default_rollback(language: str) -> str:
    return "Git revert 或恢复本次修改文件" if language == "zh" else "Git revert or restore the modified files"


def default_validation_note(language: str) -> str:
    return "初始化计划，待补充实际复现、修复与验证结果" if language == "zh" else "Plan initialized; add actual reproduction, repair, and validation results"


def render_content(args: argparse.Namespace, plan_path: Path, repo_root: Path, language: str) -> str:
    relative_path = plan_path.relative_to(repo_root).as_posix()
    harness = repo_harness_signals(repo_root)
    docs_sync_items = [relative_path, "docs/PLANS.md", *args.doc]
    if harness["has_manifest"]:
        docs_sync_items.append("docs/generated/harness-manifest.md")
    repo_check = run_repo_check(repo_root)
    template = load_template(Path(__file__).resolve().parent.parent, f"fix-plan.{language}.md.tpl")
    return template.substitute(
        title=args.title.strip(),
        owner=args.owner.strip(),
        date=args.date,
        severity=normalize_text(args.severity, language),
        goal=normalize_text(args.goal, language),
        impact=normalize_text(args.impact, language),
        expected=normalize_text(args.expected, language),
        observed=normalize_text(args.observed, language),
        rollback=normalize_text(args.rollback, language) if args.rollback else default_rollback(language),
        plan_path=relative_path,
        evidence=format_block(args.evidence, language),
        reproduction=format_block(args.reproduction, language),
        likely_surfaces=format_block(args.surface, language),
        hypotheses=format_block(args.hypothesis, language),
        validation=format_block(args.validation, language),
        docs_sync=format_block(docs_sync_items, language),
        risk_summary=format_block(args.risk, language),
        initial_validation_note=default_validation_note(language),
        HARNESS_CHECK_STATUS=(
            "可用且通过" if language == "zh" and repo_check["available"] and repo_check["ok"]
            else "可用但存在发现" if language == "zh" and repo_check["available"]
            else "不可用" if language == "zh"
            else "available and passing" if repo_check["available"] and repo_check["ok"]
            else "available with findings" if repo_check["available"]
            else "not available"
        ),
        HARNESS_SURFACES=format_block(
            [
                "scripts/check_harness.py" if harness["has_repo_check"] else ("scripts/check_harness.py (missing)"),
                "docs/generated/harness-manifest.md" if harness["has_manifest"] else ("docs/generated/harness-manifest.md (missing)"),
                "docs/OBSERVABILITY.md" if harness["has_observability_doc"] else ("docs/OBSERVABILITY.md (missing)"),
                "docs/exec-plans/tech-debt-tracker.md" if harness["has_tech_debt_tracker"] else ("docs/exec-plans/tech-debt-tracker.md (missing)"),
            ],
            language,
        ),
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).expanduser().resolve()
    repo_root.mkdir(parents=True, exist_ok=True)
    language = detect_doc_language(repo_root) if args.language == "auto" else args.language
    active_dir = repo_root / "docs" / "exec-plans" / "active"
    active_dir.mkdir(parents=True, exist_ok=True)

    raw_slug = args.slug.strip() if args.slug else args.title.strip()
    slug = normalize_slug(raw_slug, "fix", args.date)
    plan_path = next_markdown_path(active_dir, slug)
    content = render_content(args, plan_path, repo_root, language)

    sync_result = None
    if not args.dry_run:
        plan_path.write_text(content, encoding="utf-8")
        if not args.skip_sync:
            sync_script = Path(__file__).resolve().parent / "sync_plan_state.py"
            result = subprocess.run(
                ["python3", str(sync_script), "--repo", str(repo_root), "--language", language, "--format", "json"],
                check=True,
                capture_output=True,
                text=True,
            )
            sync_result = json.loads(result.stdout)

    payload = {
        "mode": "fix",
        "language": language,
        "plan_path": str(plan_path),
        "relative_path": plan_path.relative_to(repo_root).as_posix(),
        "slug": plan_path.stem,
        "written": not args.dry_run,
        "sync_result": sync_result,
    }
    if args.dry_run:
        payload["content"] = content

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
