#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import subprocess
import hashlib
from pathlib import Path
from string import Template
from typing import Dict, Iterable, List

MANAGED_MARKER = "<!-- HARNESS:MANAGED FILE -->"


def detect_doc_language(repo: Path) -> str:
    for rel_path in ["AGENTS.md", "README.md", "docs/README.md", "docs/PLANS.md"]:
        path = repo / rel_path
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if re.search(r"[\u4e00-\u9fff]", text):
            return "zh"
        if text.strip():
            return "en"
    return "zh"


def is_managed(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return MANAGED_MARKER in content or "# HARNESS:MANAGED FILE" in content


def placeholder(language: str) -> str:
    return "待补充" if language == "zh" else "TBD"


def normalize_text(value: str | None, language: str) -> str:
    text = (value or "").strip()
    return text if text else placeholder(language)


def dedupe(items: Iterable[str]) -> List[str]:
    result: List[str] = []
    seen: set[str] = set()
    for item in items:
        value = item.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def format_block(items: Iterable[str], language: str) -> str:
    values = dedupe(items)
    if not values:
        values = [placeholder(language)]
    return "\n".join(f"  - {value}" for value in values)


def normalize_slug(raw: str, fallback_prefix: str, today: str) -> str:
    ascii_only = raw.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only).strip("-").lower()
    slug = re.sub(r"-{2,}", "-", slug)
    if slug:
        return slug[:64].strip("-")
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]
    return f"{fallback_prefix}-{today}-{digest}"


def next_markdown_path(directory: Path, slug: str) -> Path:
    candidate = directory / f"{slug}.md"
    if not candidate.exists():
        return candidate
    index = 2
    while True:
        candidate = directory / f"{slug}-{index}.md"
        if not candidate.exists():
            return candidate
        index += 1


def load_template(skill_root: Path, rel_path: str) -> Template:
    return Template((skill_root / "assets" / rel_path).read_text(encoding="utf-8"))


def active_plans(repo: Path) -> List[str]:
    active_dir = repo / "docs" / "exec-plans" / "active"
    if not active_dir.exists():
        return []
    return sorted(
        str(path.relative_to(repo))
        for path in active_dir.glob("*.md")
        if path.is_file() and path.name != "README.md"
    )


def repo_harness_signals(repo: Path) -> Dict[str, bool]:
    return {
        "has_repo_check": (repo / "scripts" / "check_harness.py").exists(),
        "has_manifest": (repo / "docs" / "generated" / "harness-manifest.md").exists(),
        "has_observability_doc": (repo / "docs" / "OBSERVABILITY.md").exists(),
        "has_tech_debt_tracker": (repo / "docs" / "exec-plans" / "tech-debt-tracker.md").exists(),
    }


def run_repo_check(repo: Path) -> Dict[str, object]:
    check_path = repo / "scripts" / "check_harness.py"
    if not check_path.exists():
        return {"available": False, "ok": None, "findings": []}
    result = subprocess.run(
        ["python3", str(check_path), "--repo", str(repo), "--format", "json"],
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    payload = json.loads(result.stdout or "{}")
    return {
        "available": True,
        "ok": payload.get("ok"),
        "findings": payload.get("findings", []),
    }


def render_plans_index(skill_root: Path, repo: Path, language: str) -> str:
    template = load_template(skill_root, f"plans-index.{language}.md.tpl")
    active = active_plans(repo)
    if active:
        active_lines = "\n".join(
            f"- [{Path(rel_path).stem.replace('-', ' ').title()}]({rel_path})"
            for rel_path in active
        )
    else:
        active_lines = "- 暂无活跃计划" if language == "zh" else "- No active plans"
    return template.substitute(ACTIVE_PLANS=active_lines)
