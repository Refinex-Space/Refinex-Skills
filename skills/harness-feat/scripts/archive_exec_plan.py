#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path

from _plan_common import detect_doc_language, next_markdown_path, placeholder


def _resolve_plan_path(repo: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return repo / value


def _archive_header(summary: str, duration: str, learnings: list[str], completed_date: str, language: str) -> str:
    learning_text = "; ".join(learnings) if learnings else placeholder(language)
    return (
        f"> ✅ Completed: {completed_date}\n"
        f"> Summary: {summary}\n"
        f"> Duration: {duration}\n"
        f"> Key learnings: {learning_text}\n\n"
    )


def archive_exec_plan(repo: Path, plan_path: Path, summary: str, duration: str, learnings: list[str], completed_date: str, language: str) -> dict:
    if not plan_path.exists():
        raise FileNotFoundError(f"Plan does not exist: {plan_path}")

    active_dir = repo / "docs" / "exec-plans" / "active"
    completed_dir = repo / "docs" / "exec-plans" / "completed"
    completed_dir.mkdir(parents=True, exist_ok=True)

    try:
        relative = plan_path.relative_to(active_dir)
    except ValueError as exc:
        raise ValueError(f"Plan must be under {active_dir}") from exc

    destination = next_markdown_path(completed_dir, relative.stem)
    body = plan_path.read_text(encoding="utf-8")
    if not body.lstrip().startswith("> ✅ Completed:"):
        body = _archive_header(summary, duration, learnings, completed_date, language) + body
    destination.write_text(body, encoding="utf-8")
    plan_path.unlink()

    sync_script = Path(__file__).resolve().parent / "sync_plan_state.py"
    sync_result = subprocess.run(
        ["python3", str(sync_script), "--repo", str(repo), "--language", language, "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
    )

    return {
        "repo": str(repo),
        "archived_from": str(plan_path.relative_to(repo)),
        "archived_to": str(destination.relative_to(repo)),
        "sync_result": json.loads(sync_result.stdout),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive a completed feature execution plan")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--plan", required=True, help="Active plan path")
    parser.add_argument("--summary", required=True, help="Completion summary")
    parser.add_argument("--duration", default="TBD", help="Actual duration")
    parser.add_argument("--learning", action="append", default=[], help="Key learning, repeatable")
    parser.add_argument("--completed-date", default=date.today().isoformat(), help="Completion date")
    parser.add_argument("--language", choices=("auto", "zh", "en"), default="auto")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    language = detect_doc_language(repo) if args.language == "auto" else args.language
    result = archive_exec_plan(
        repo=repo,
        plan_path=_resolve_plan_path(repo, args.plan).resolve(),
        summary=args.summary.strip(),
        duration=args.duration.strip(),
        learnings=[item.strip() for item in args.learning if item.strip()],
        completed_date=args.completed_date,
        language=language,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
