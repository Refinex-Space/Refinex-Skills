#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from string import Template
from typing import Dict, Iterable, List, Sequence

MANAGED_MARKER = "<!-- HARNESS:MANAGED FILE -->"
WORKSPACE_PARENT_DIRS = {"apps", "packages", "services", "crates", "libs", "modules"}
FRONTEND_DIR_HINTS = {"app", "apps", "components", "frontend", "pages", "public", "src", "ui", "web"}
BACKEND_DIR_HINTS = {"api", "backend", "cmd", "crates", "db", "internal", "server", "services", "src-tauri"}
CORE_DOCS = [
    "AGENTS.md",
    "ARCHITECTURE.md",
    "docs/README.md",
    "docs/PLANS.md",
    "docs/SECURITY.md",
    "docs/RELIABILITY.md",
    "docs/OBSERVABILITY.md",
    "docs/QUALITY_SCORE.md",
    "docs/exec-plans/tech-debt-tracker.md",
    "docs/exec-plans/completed/README.md",
    "docs/generated/README.md",
    "docs/references/index.md",
]
FRONTEND_DOCS = [
    "docs/FRONTEND.md",
    "docs/PRODUCT_SENSE.md",
    "docs/product-specs/index.md",
]
COMPLEX_ARCH_DOCS = [
    "docs/DESIGN.md",
    "docs/design-docs/index.md",
    "docs/design-docs/core-beliefs.md",
]


def load_text_template(skill_root: Path, rel_path: str) -> Template:
    path = skill_root / "assets" / "templates" / rel_path
    return Template(path.read_text(encoding="utf-8"))


def parse_library(skill_root: Path, rel_path: str) -> Dict[str, str]:
    content = (skill_root / "assets" / "templates" / rel_path).read_text(encoding="utf-8")
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


def contains_chinese(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def _walk_files(repo: Path, max_depth: int = 4) -> Iterable[Path]:
    for root, dirs, files in os.walk(repo):
        root_path = Path(root)
        depth = len(root_path.relative_to(repo).parts)
        dirs[:] = [name for name in dirs if not name.startswith(".") and depth < max_depth]
        for filename in files:
            if filename.startswith("."):
                continue
            path = root_path / filename
            if len(path.relative_to(repo).parts) <= max_depth:
                yield path


def _walk_dirs(repo: Path, max_depth: int = 4) -> Iterable[Path]:
    for root, dirs, _ in os.walk(repo):
        root_path = Path(root)
        depth = len(root_path.relative_to(repo).parts)
        visible_dirs = [name for name in dirs if not name.startswith(".")]
        dirs[:] = [name for name in visible_dirs if depth < max_depth]
        for dirname in visible_dirs:
            path = root_path / dirname
            if len(path.relative_to(repo).parts) <= max_depth:
                yield path


def _has_file_named(repo: Path, names: Iterable[str], max_depth: int = 4) -> bool:
    wanted = set(names)
    return any(path.name in wanted for path in _walk_files(repo, max_depth=max_depth))


def _has_extension(repo: Path, extensions: Iterable[str], max_depth: int = 4) -> bool:
    wanted = set(extensions)
    return any(path.suffix in wanted for path in _walk_files(repo, max_depth=max_depth))


def _has_dir_named(repo: Path, names: Iterable[str], max_depth: int = 4) -> bool:
    wanted = set(names)
    return any(path.name in wanted for path in _walk_dirs(repo, max_depth=max_depth))


def detect_doc_language(repo: Path) -> str:
    for rel_path in ["AGENTS.md", "README.md", "docs/README.md", "docs/PLANS.md"]:
        path = repo / rel_path
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if contains_chinese(text):
            return "zh"
        if text.strip():
            return "en"
    return "zh"


def detect_languages(repo: Path) -> List[str]:
    languages: List[str] = []
    has_typescript = _has_file_named(
        repo,
        {"tsconfig.json", "tsconfig.base.json", "tsconfig.app.json", "pnpm-workspace.yaml"},
    ) or _has_extension(repo, {".ts", ".tsx"})
    has_javascript = _has_file_named(repo, {"package.json"}) or _has_extension(
        repo,
        {".js", ".jsx", ".mjs", ".cjs"},
    )
    if has_typescript:
        languages.append("TypeScript")
    if has_javascript and (not has_typescript or _has_extension(repo, {".js", ".jsx", ".mjs", ".cjs"})):
        languages.append("JavaScript")
    checks = {
        "Rust": {"Cargo.toml"},
        "Go": {"go.mod"},
        "Python": {"pyproject.toml", "requirements.txt", "requirements-dev.txt"},
    }
    for language, markers in checks.items():
        if _has_file_named(repo, markers):
            languages.append(language)
    return languages or ["Unknown"]


def detect_frameworks(repo: Path) -> List[str]:
    frameworks: List[str] = []
    if _has_file_named(repo, {"next.config.js", "next.config.mjs", "next.config.ts"}):
        frameworks.extend(["Next.js", "React"])
    elif _has_file_named(repo, {"vite.config.ts", "vite.config.js", "vite.config.mjs"}):
        frameworks.append("Vite")
    if _has_file_named(repo, {"vitest.config.ts", "vitest.config.js", "vitest.config.mjs"}):
        frameworks.append("Vitest")
    if _has_file_named(repo, {"tauri.conf.json", "tauri.conf.json5"}) or _has_dir_named(repo, {"src-tauri"}):
        frameworks.append("Tauri")
    if (repo / "pnpm-workspace.yaml").exists():
        frameworks.append("pnpm Workspace")
    if (repo / "Cargo.toml").exists() and any(
        path.name in {"crates", "apps", "services"} for path in top_level_dirs(repo, as_paths=True)
    ):
        frameworks.append("Cargo Workspace")
    if "React" not in frameworks and _has_dir_named(repo, {"app", "components", "pages"}, max_depth=4):
        frameworks.append("React")
    return frameworks or ["Unknown"]


def top_level_dirs(repo: Path, as_paths: bool = False) -> List[Path] | List[str]:
    entries = sorted(
        entry for entry in repo.iterdir() if entry.is_dir() and not entry.name.startswith(".")
    )
    if as_paths:
        return entries
    return [entry.name for entry in entries]


def _dir_looks_like_workspace(path: Path) -> bool:
    workspace_markers = {
        "package.json",
        "Cargo.toml",
        "go.mod",
        "pyproject.toml",
        "requirements.txt",
        "tsconfig.json",
    }
    if any((path / marker).exists() for marker in workspace_markers):
        return True
    child_dirs = {item.name for item in path.iterdir() if item.is_dir() and not item.name.startswith(".")}
    return bool(child_dirs & (FRONTEND_DIR_HINTS | BACKEND_DIR_HINTS))


def suggest_local_agents(repo: Path) -> List[str]:
    suggestions: List[str] = []
    for dirname in top_level_dirs(repo):
        if dirname not in WORKSPACE_PARENT_DIRS:
            continue
        parent = repo / dirname
        children = [
            child for child in sorted(parent.iterdir()) if child.is_dir() and not child.name.startswith(".")
        ]
        workspace_children = [child for child in children if _dir_looks_like_workspace(child)]
        if not workspace_children:
            if children:
                suggestions.append(dirname)
            continue
        if len(workspace_children) == 1:
            suggestions.append(f"{dirname}/{workspace_children[0].name}")
            continue
        suggestions.append(dirname)
        suggestions.extend(f"{dirname}/{child.name}" for child in workspace_children)
    seen = set()
    ordered: List[str] = []
    for item in suggestions:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def _has_frontend_signals(repo: Path, frameworks: Sequence[str]) -> bool:
    return any(
        [
            "React" in frameworks,
            "Next.js" in frameworks,
            _has_dir_named(repo, {"app", "components", "pages", "public", "ui", "web"}, max_depth=4),
            _has_file_named(repo, {"index.html"}, max_depth=3),
        ]
    )


def _has_backend_signals(repo: Path, languages: Sequence[str], frameworks: Sequence[str]) -> bool:
    return any(
        [
            "Tauri" in frameworks,
            any(language in {"Rust", "Go", "Python"} for language in languages),
            _has_dir_named(repo, {"api", "backend", "cmd", "internal", "server", "services"}, max_depth=4),
        ]
    )


def determine_project_type(repo: Path, languages: Sequence[str], frameworks: Sequence[str]) -> str:
    top_dirs = set(top_level_dirs(repo))
    workspace_roots = top_dirs & WORKSPACE_PARENT_DIRS
    if (repo / "pnpm-workspace.yaml").exists() or len(workspace_roots) >= 2 or (
        workspace_roots and len(suggest_local_agents(repo)) >= 2
    ):
        return "monorepo"
    has_frontend = _has_frontend_signals(repo, frameworks)
    has_backend = _has_backend_signals(repo, languages, frameworks)
    if has_frontend and has_backend:
        return "full-stack"
    if has_frontend:
        return "frontend"
    if has_backend:
        return "backend"
    if {"Python"} == set(languages) or {"Go"} == set(languages):
        return "service"
    return "library"


def selected_doc_paths(profile: Dict[str, object]) -> List[str]:
    paths = list(CORE_DOCS)
    if profile["has_frontend"]:
        paths.extend(FRONTEND_DOCS)
    if profile["complex_architecture"]:
        paths.extend(COMPLEX_ARCH_DOCS)
    return paths


def selected_route_docs(profile: Dict[str, object]) -> List[str]:
    docs = [
        "docs/PLANS.md",
        "docs/SECURITY.md",
        "docs/RELIABILITY.md",
        "docs/OBSERVABILITY.md",
        "docs/QUALITY_SCORE.md",
    ]
    if profile["has_frontend"]:
        docs.extend(["docs/FRONTEND.md", "docs/PRODUCT_SENSE.md"])
    if profile["complex_architecture"]:
        docs.extend(["docs/DESIGN.md", "docs/design-docs/index.md"])
    return docs


def profile_fingerprint(profile: Dict[str, object]) -> str:
    stable_payload = {
        "project_type": profile["project_type"],
        "languages": profile["languages"],
        "frameworks": profile["frameworks"],
        "doc_language": profile["doc_language"],
        "has_frontend": profile["has_frontend"],
        "complex_architecture": profile["complex_architecture"],
        "local_agent_dirs": profile["local_agent_dirs"],
        "required_harness_files": profile["required_harness_files"],
        "route_docs": profile["route_docs"],
        "structure_summary": profile["structure_summary"],
    }
    return hashlib.sha256(
        json.dumps(stable_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]


def build_profile(repo: Path) -> Dict[str, object]:
    languages = detect_languages(repo)
    frameworks = detect_frameworks(repo)
    project_type = determine_project_type(repo, languages, frameworks)
    local_agents = suggest_local_agents(repo)
    has_frontend = _has_frontend_signals(repo, frameworks)
    complex_arch = project_type in {"monorepo", "full-stack"} or len(local_agents) >= 2
    top_dirs = top_level_dirs(repo)
    profile: Dict[str, object] = {
        "repo_name": repo.name,
        "project_type": project_type,
        "languages": languages,
        "frameworks": frameworks,
        "doc_language": detect_doc_language(repo),
        "has_frontend": has_frontend,
        "complex_architecture": complex_arch,
        "local_agent_dirs": local_agents,
        "top_level_dirs": top_dirs,
        "structure_summary": ", ".join(top_dirs[:12]) or "(empty repo)",
    }
    profile["required_harness_files"] = selected_doc_paths(profile)
    profile["route_docs"] = selected_route_docs(profile)
    profile["profile_fingerprint"] = profile_fingerprint(profile)
    return profile


def is_managed(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return MANAGED_MARKER in content or "# HARNESS:MANAGED FILE" in content


def collect_managed_files(repo: Path) -> List[str]:
    managed: List[str] = []
    for path in _walk_files(repo, max_depth=6):
        rel_path = str(path.relative_to(repo))
        if is_managed(path):
            managed.append(rel_path)
    return sorted(set(managed))


def render_manifest(skill_root: Path, repo: Path, language: str, managed_files: List[str]) -> str:
    profile = build_profile(repo)
    template = load_text_template(skill_root, f"harness-manifest.{language}.md.tpl")
    return template.substitute(
        PROJECT_NAME=profile["repo_name"],
        PROJECT_TYPE=profile["project_type"],
        LANGUAGES=", ".join(profile["languages"]),
        FRAMEWORKS=", ".join(profile["frameworks"]),
        LANGUAGE=language,
        FINGERPRINT=profile["profile_fingerprint"],
        MANAGED_FILES=bullet_list(managed_files, "No managed Harness files yet"),
        LOCAL_AGENTS=bullet_list(profile["local_agent_dirs"], "No local AGENTS suggested"),
        INDEX_FILES=bullet_list(
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


def render_check_script(skill_root: Path, profile: Dict[str, object]) -> str:
    template = load_text_template(skill_root, "check-harness.py.tpl")
    required_files = sorted(
        set(profile["required_harness_files"] + ["docs/generated/harness-manifest.md", "scripts/check_harness.py"])
    )
    return template.substitute(
        REQUIRED_FILES_JSON=json.dumps(required_files, ensure_ascii=False),
        ROUTE_DOCS_JSON=json.dumps(profile["route_docs"], ensure_ascii=False),
        LOCAL_AGENT_DIRS_JSON=json.dumps(profile["local_agent_dirs"], ensure_ascii=False),
        PROFILE_FINGERPRINT=profile["profile_fingerprint"],
    )


def bullet_list(items: Iterable[str], empty_message: str) -> str:
    normalized = [item for item in items if item]
    if not normalized:
        return f"- {empty_message}"
    return "\n".join(f"- `{item}`" for item in normalized)


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def required_paths_for_garden(repo: Path) -> List[str]:
    return build_profile(repo)["required_harness_files"]


def missing_archive_header(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return not text.lstrip().startswith("> ✅ Completed:")
