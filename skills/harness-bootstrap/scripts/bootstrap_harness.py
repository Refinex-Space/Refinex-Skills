#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path
from string import Template
from typing import Dict, List

from init_repo_harness_check import install_repo_harness_check
from profile_repo import build_profile, selected_doc_paths

MANAGED_MARKER = "<!-- HARNESS:MANAGED FILE -->"


def _parse_template_library(name: str) -> Dict[str, str]:
    path = Path(__file__).resolve().parent.parent / "assets" / "templates" / name
    content = path.read_text(encoding="utf-8")
    sections: Dict[str, List[str]] = {}
    current_key = ""
    for line in content.splitlines():
        if line.startswith("@@ "):
            current_key = line[3:].strip()
            sections[current_key] = []
            continue
        if current_key:
            sections[current_key].append(line)
    return {key: "\n".join(lines).strip() + "\n" for key, lines in sections.items()}


def _load_template(name: str) -> Template:
    path = Path(__file__).resolve().parent.parent / "assets" / "templates" / name
    return Template(path.read_text(encoding="utf-8"))


def _detect_language(profile: Dict[str, object], override: str) -> str:
    if override != "auto":
        return override
    return str(profile["doc_language"])


def _doc_context(profile: Dict[str, object], language: str) -> Dict[str, str]:
    has_frontend = bool(profile["has_frontend"])
    complex_arch = bool(profile["complex_architecture"])
    template_library = _parse_template_library(f"bootstrap-docs.{language}.tpl")
    summary = (
        "该仓库已启用面向智能体的工程控制面，要求路由简洁、计划可继续、运行态可观察。"
        if language == "zh"
        else "This repository uses an agent-first control plane with concise routing, resumable plans, and observable runtime surfaces."
    )
    local_hints = profile["local_agent_dirs"] or []
    local_agent_hint_lines = [f"- `{item}/AGENTS.md`" for item in local_hints]
    if not local_agent_hint_lines:
        local_agent_hint_lines = ["- 暂无额外局部 AGENTS" if language == "zh" else "- No additional local AGENTS yet"]
    docs_extra = []
    routes_extra = []
    if has_frontend:
        docs_extra.append(template_library["docs/README.md.extra.frontend"].strip())
        routes_extra.append(template_library["AGENTS.md.extra.frontend"].strip())
    if complex_arch:
        docs_extra.append(template_library["docs/README.md.extra.design"].strip())
        routes_extra.append(template_library["AGENTS.md.extra.design"].strip())
    structure_summary = (
        f"- 顶层结构：{profile['structure_summary']}"
        if language == "zh"
        else f"- Top-level structure: {profile['structure_summary']}"
    )
    return {
        "PROJECT_NAME": str(profile["repo_name"]),
        "PROJECT_SUMMARY": summary,
        "ACTIVE_PLAN_PATH": "docs/exec-plans/active/harness-bootstrap.md",
        "EXTRA_ROUTES": "\n".join(routes_extra) if routes_extra else "",
        "LOCAL_AGENT_HINTS": "\n".join(local_agent_hint_lines),
        "STRUCTURE_SUMMARY": structure_summary,
        "DOCS_EXTRA_INDEX": "\n".join(docs_extra) if docs_extra else "",
    }


def _local_agent_context(target_path: str, language: str) -> Dict[str, str]:
    name = Path(target_path).name
    if language == "zh":
        summary = f"`{target_path}` 是一个需要独立约束、验证和接手说明的真实工作边界。"
        focus = "- 本目录的边界\n- 本目录的主要命令\n- 与相邻目录的协作方式"
    else:
        summary = f"`{target_path}` is a real work boundary that needs local rules, validation, and handoff guidance."
        focus = "- local boundaries\n- main commands for this area\n- coordination with adjacent directories"
    return {
        "TARGET_NAME": name,
        "TARGET_PATH": target_path,
        "AREA_SUMMARY": summary,
        "FOCUS_POINTS": focus,
    }


def _is_managed(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return MANAGED_MARKER in content or "# HARNESS:MANAGED FILE" in content


def _write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _selected_templates(profile: Dict[str, object]) -> List[str]:
    return selected_doc_paths(profile)


def _render_doc(template_library: Dict[str, str], rel_path: str, context: Dict[str, str]) -> str:
    template = Template(template_library[rel_path])
    return template.substitute(context)


def _run_repo_check(repo: Path) -> Dict[str, object]:
    check_script = repo / "scripts" / "check_harness.py"
    if not check_script.exists():
        return {
            "ok": False,
            "findings": [
                {
                    "severity": "P0",
                    "code": "missing-check-script",
                    "path": "scripts/check_harness.py",
                    "message": "Bootstrap did not install the repo-local check script",
                }
            ],
        }
    result = subprocess.run(
        ["python3", str(check_script), "--repo", str(repo), "--format", "json"],
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    payload = json.loads(result.stdout or "{}")
    if not isinstance(payload, dict):
        return {"ok": False, "findings": [{"severity": "P0", "code": "invalid-check-output", "path": "scripts/check_harness.py", "message": "Repo-local check returned invalid JSON"}]}
    return payload


def bootstrap_repo(repo: Path, language: str, dry_run: bool) -> Dict[str, object]:
    profile = build_profile(repo)
    template_library = _parse_template_library(f"bootstrap-docs.{language}.tpl")
    context = _doc_context(profile, language)

    created: List[str] = []
    updated: List[str] = []
    skipped: List[str] = []
    managed_files: List[str] = []

    for rel_path in _selected_templates(profile):
        content = _render_doc(template_library, rel_path, context)
        path = repo / rel_path
        if not path.exists():
            _write_file(path, content, dry_run)
            created.append(rel_path)
            managed_files.append(rel_path)
        elif _is_managed(path):
            _write_file(path, content, dry_run)
            updated.append(rel_path)
            managed_files.append(rel_path)
        else:
            skipped.append(f"{rel_path} (existing unmanaged file preserved)")

    local_template = _load_template(f"local-agent.{language}.md.tpl")
    for target_dir in profile["local_agent_dirs"]:
        rel_path = f"{target_dir}/AGENTS.md"
        path = repo / rel_path
        content = local_template.substitute(_local_agent_context(target_dir, language))
        if not path.exists():
            _write_file(path, content, dry_run)
            created.append(rel_path)
            managed_files.append(rel_path)
        elif _is_managed(path):
            _write_file(path, content, dry_run)
            updated.append(rel_path)
            managed_files.append(rel_path)
        else:
            skipped.append(f"{rel_path} (existing unmanaged file preserved)")

    plan_template = _load_template(f"bootstrap-plan.{language}.md.tpl")
    plan_path = "docs/exec-plans/active/harness-bootstrap.md"
    touched_items = created + updated
    created_items = touched_items if touched_items else ["(no files created yet)"]
    skipped_items = skipped or (["- 无" if language == "zh" else "- none"])
    follow_up_items = skipped or (["- 无额外风险" if language == "zh" else "- no additional follow-ups"])
    plan_content = plan_template.substitute(
        DATE=date.today().isoformat(),
        PROJECT_NAME=profile["repo_name"],
        PLAN_PATH=plan_path,
        PROFILE_SUMMARY=(
            f"- 项目类型：{profile['project_type']}\n- 语言：{', '.join(profile['languages'])}\n- 框架信号：{', '.join(profile['frameworks'])}\n- 局部 AGENTS 候选：{', '.join(profile['local_agent_dirs']) or '无'}\n- Profile 指纹：{profile['profile_fingerprint']}"
            if language == "zh"
            else f"- Project type: {profile['project_type']}\n- Languages: {', '.join(profile['languages'])}\n- Frameworks: {', '.join(profile['frameworks'])}\n- Local AGENTS candidates: {', '.join(profile['local_agent_dirs']) or 'none'}\n- Profile fingerprint: {profile['profile_fingerprint']}"
        ),
        CREATED_ITEMS="\n".join(f"- `{item}`" for item in created_items),
        SKIPPED_ITEMS="\n".join(f"- {item}" for item in skipped_items),
        FOLLOW_UP_ITEMS="\n".join(f"- {item}" for item in follow_up_items),
    )
    _write_file(repo / plan_path, plan_content, dry_run)
    managed_files.append(plan_path)

    if not dry_run:
        mechanical_files = sorted(set(managed_files + ["scripts/check_harness.py", "docs/generated/harness-manifest.md"]))
        check_result = install_repo_harness_check(
            repo,
            language,
            mechanical_files,
            list(profile["local_agent_dirs"]),
        )
        managed_files.extend(["scripts/check_harness.py", "docs/generated/harness-manifest.md"])
        validation = _run_repo_check(repo)
    else:
        check_result = {
            "manifest_path": str(repo / "docs/generated/harness-manifest.md"),
            "check_path": str(repo / "scripts/check_harness.py"),
        }
        validation = {"ok": True, "findings": []}

    return {
        "repo": str(repo),
        "language": language,
        "profile": profile,
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "managed_files": sorted(set(managed_files)),
        "check_result": check_result,
        "validation": validation,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap Harness Engineering into a repository")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument("--mode", default="adaptive", choices=("adaptive",), help="Scaffold mode")
    parser.add_argument("--language", default="auto", choices=("auto", "zh", "en"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--format", default="md", choices=("md", "json"))
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    repo.mkdir(parents=True, exist_ok=True)
    profile = build_profile(repo)
    language = _detect_language(profile, args.language)
    result = bootstrap_repo(repo, language, args.dry_run)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("# Harness Bootstrap")
        print()
        print(f"- Repo: `{result['repo']}`")
        print(f"- Language: `{result['language']}`")
        print(f"- Project type: `{result['profile']['project_type']}`")
        print(f"- Profile fingerprint: `{result['profile']['profile_fingerprint']}`")
        print(f"- Created: {len(result['created'])}")
        print(f"- Updated: {len(result['updated'])}")
        print(f"- Skipped: {len(result['skipped'])}")
        print(f"- Dry run: {args.dry_run}")
        print(f"- Validation OK: {result['validation']['ok']}")
        if result["skipped"]:
            print()
            print("## Skipped unmanaged files")
            print()
            for item in result["skipped"]:
                print(f"- {item}")
        if result["validation"]["findings"]:
            print()
            print("## Validation findings")
            print()
            for item in result["validation"]["findings"]:
                print(f"- [{item['severity']}] `{item['code']}` {item['path']}: {item['message']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
