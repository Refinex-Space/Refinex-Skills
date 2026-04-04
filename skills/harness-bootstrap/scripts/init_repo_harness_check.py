#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
from string import Template
from typing import Dict, List, Optional

from profile_repo import build_profile


def _load_template(name: str) -> Template:
    template_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / name
    return Template(template_path.read_text(encoding="utf-8"))


def _bullet_list(items: List[str], empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- `{item}`" for item in items)


def _detect_language(repo: Path, override: Optional[str]) -> str:
    if override and override != "auto":
        return override
    return str(build_profile(repo)["doc_language"])


def render_manifest(repo: Path, language: str, managed_files: List[str], local_agents: List[str]) -> str:
    profile = build_profile(repo)
    template_name = f"harness-manifest.{language}.md.tpl"
    template = _load_template(template_name)
    return template.substitute(
        PROJECT_NAME=profile["repo_name"],
        PROJECT_TYPE=profile["project_type"],
        LANGUAGES=", ".join(profile["languages"]),
        FRAMEWORKS=", ".join(profile["frameworks"]),
        LANGUAGE=language,
        FINGERPRINT=profile["profile_fingerprint"],
        MANAGED_FILES=_bullet_list(sorted(managed_files), "No managed Harness files yet"),
        LOCAL_AGENTS=_bullet_list(local_agents, "No local AGENTS generated"),
        INDEX_FILES=_bullet_list(
            [
                "docs/PLANS.md",
                "docs/OBSERVABILITY.md",
                "docs/exec-plans/tech-debt-tracker.md",
                "docs/generated/harness-manifest.md",
                "docs/references/index.md",
            ],
            "No index files",
        ),
    )


def render_check_script(profile: Dict[str, object]) -> str:
    template = _load_template("check-harness.py.tpl")
    required_files = sorted(
        set(profile["required_harness_files"] + ["docs/generated/harness-manifest.md", "scripts/check_harness.py"])
    )
    return template.substitute(
        REQUIRED_FILES_JSON=json.dumps(required_files, ensure_ascii=False),
        ROUTE_DOCS_JSON=json.dumps(profile["route_docs"], ensure_ascii=False),
        LOCAL_AGENT_DIRS_JSON=json.dumps(profile["local_agent_dirs"], ensure_ascii=False),
        PROFILE_FINGERPRINT=profile["profile_fingerprint"],
    )


def install_repo_harness_check(
    repo: Path,
    language: str,
    managed_files: List[str],
    local_agent_dirs: List[str],
) -> Dict[str, str]:
    repo.mkdir(parents=True, exist_ok=True)
    manifest_path = repo / "docs" / "generated" / "harness-manifest.md"
    check_path = repo / "scripts" / "check_harness.py"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    check_path.parent.mkdir(parents=True, exist_ok=True)

    profile = build_profile(repo)
    manifest_path.write_text(
        render_manifest(repo, language, managed_files, local_agent_dirs),
        encoding="utf-8",
    )
    check_path.write_text(render_check_script(profile), encoding="utf-8")
    check_path.chmod(0o755)

    return {
        "manifest_path": str(manifest_path),
        "check_path": str(check_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Install repo-local Harness check files")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--language", choices=("auto", "zh", "en"), default="auto")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    language = _detect_language(repo, args.language)
    profile = build_profile(repo)
    managed_files = sorted(set(profile["required_harness_files"]))
    result = install_repo_harness_check(repo, language, managed_files, profile["local_agent_dirs"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
