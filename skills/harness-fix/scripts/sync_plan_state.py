#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _plan_common import detect_doc_language, is_managed, render_plans_index


def sync_plan_state(repo: Path, language: str) -> dict:
    plans_path = repo / "docs" / "PLANS.md"
    skill_root = Path(__file__).resolve().parent.parent
    desired_content = render_plans_index(skill_root, repo, language)

    if not plans_path.exists():
        return {
            "repo": str(repo),
            "plans_path": "docs/PLANS.md",
            "language": language,
            "written": False,
            "manual_update_required": True,
            "reason": "docs/PLANS.md is missing; use harness-bootstrap or harness-garden first",
            "desired_content": desired_content,
        }

    if not is_managed(plans_path):
        return {
            "repo": str(repo),
            "plans_path": "docs/PLANS.md",
            "language": language,
            "written": False,
            "manual_update_required": True,
            "reason": "docs/PLANS.md is unmanaged and was preserved",
            "desired_content": desired_content,
        }

    plans_path.write_text(desired_content, encoding="utf-8")
    return {
        "repo": str(repo),
        "plans_path": "docs/PLANS.md",
        "language": language,
        "written": True,
        "manual_update_required": False,
        "reason": "",
        "desired_content": desired_content,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync docs/PLANS.md with active execution plans")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--language", choices=("auto", "zh", "en"), default="auto")
    parser.add_argument("--format", choices=("json", "md"), default="json")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    language = detect_doc_language(repo) if args.language == "auto" else args.language
    result = sync_plan_state(repo, language)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("# Plan State Sync")
        print()
        print(f"- Repo: `{result['repo']}`")
        print(f"- Plans path: `{result['plans_path']}`")
        print(f"- Language: `{result['language']}`")
        print(f"- Written: {result['written']}")
        print(f"- Manual update required: {result['manual_update_required']}")
        if result["reason"]:
            print(f"- Reason: {result['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
