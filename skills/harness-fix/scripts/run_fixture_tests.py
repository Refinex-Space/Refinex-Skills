#!/usr/bin/env python3

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from subprocess import run


def _skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _fixture_root() -> Path:
    return _skill_root() / "assets" / "test-fixtures"


def _bootstrap_script() -> Path:
    return _skill_root().parent / "harness-bootstrap" / "scripts" / "bootstrap_harness.py"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _materialize(repo: Path, files: dict[str, str]) -> None:
    for rel_path, content in files.items():
        path = repo / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _run_json(cmd: list[str]) -> dict:
    result = run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def _assert_repo_lifecycle_scripts_absent(repo: Path) -> None:
    for rel_path in [
        "scripts/init_exec_plan.py",
        "scripts/sync_plan_state.py",
        "scripts/archive_exec_plan.py",
    ]:
        if (repo / rel_path).exists():
            raise AssertionError(f"Target repository unexpectedly contains {rel_path}")


def _normalize_paths(value: object, repo: Path) -> object:
    repo_resolved = str(repo.resolve())
    private_resolved = repo_resolved.replace("/var/", "/private/var/")
    if isinstance(value, dict):
        return {key: _normalize_paths(item, repo) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize_paths(item, repo) for item in value]
    if isinstance(value, str):
        return value.replace(private_resolved, "<REPO>").replace(repo_resolved, "<REPO>")
    return value


def _bootstrap_repo(repo: Path, files: dict[str, str], language: str) -> None:
    _materialize(repo, files)
    _run_json(
        [
            "python3",
            str(_bootstrap_script()),
            "--repo",
            str(repo),
            "--language",
            language,
            "--date",
            "2026-04-05",
            "--format",
            "json",
        ]
    )


def _run_case_managed_e2e(repo: Path, fixture: dict) -> dict:
    _bootstrap_repo(repo, fixture["files"], fixture["language"])
    _assert_repo_lifecycle_scripts_absent(repo)
    init_result = _run_json(
        [
            "python3",
            str(_skill_root() / "scripts" / "init_exec_plan.py"),
            "--repo",
            str(repo),
            "--title",
            "Provider Timeout Regression",
            "--severity",
            "P1",
            "--goal",
            "Restore explicit timeout failures",
            "--impact",
            "Provider requests can hang without surfacing an error",
            "--expected",
            "Timeouts should fail fast with a visible error",
            "--observed",
            "Requests stay loading until manually interrupted",
            "--evidence",
            "Manual provider switch leaves session hanging",
            "--reproduction",
            "Open settings, switch provider, send a message",
            "--surface",
            "apps/web",
            "--surface",
            "services/api",
            "--hypothesis",
            "Timeout path no longer emits completion or error event",
            "--validation",
            "Manual repro ends with success or explicit timeout error",
            "--date",
            "2026-04-05",
        ]
    )
    (repo / "docs" / "generated" / "harness-manifest.md").write_text(
        "<!-- HARNESS:MANAGED FILE -->\n# stale manifest\n",
        encoding="utf-8",
    )
    (repo / "scripts" / "check_harness.py").write_text(
        "# HARNESS:MANAGED FILE\n#!/usr/bin/env python3\nprint('stale')\n",
        encoding="utf-8",
    )
    archive_result = _run_json(
        [
            "python3",
            str(_skill_root() / "scripts" / "archive_exec_plan.py"),
            "--repo",
            str(repo),
            "--plan",
            init_result["relative_path"],
            "--summary",
            "Bound and archived timeout regression fix plan",
            "--duration",
            "1 day",
            "--learning",
            "Keep reproduction evidence near the active plan",
            "--completed-date",
            "2026-04-06",
        ]
    )
    return {
        "init_result": _normalize_paths(init_result, repo),
        "archive_result": _normalize_paths(archive_result, repo),
        "plans_md": (repo / "docs" / "PLANS.md").read_text(encoding="utf-8"),
        "manifest_md": (repo / "docs" / "generated" / "harness-manifest.md").read_text(encoding="utf-8"),
        "completed_plan": (repo / archive_result["archived_to"]).read_text(encoding="utf-8"),
    }


def _run_case_unmanaged_plans_safe(repo: Path, fixture: dict) -> dict:
    _materialize(repo, fixture["files"])
    _assert_repo_lifecycle_scripts_absent(repo)
    init_result = _run_json(
        [
            "python3",
            str(_skill_root() / "scripts" / "init_exec_plan.py"),
            "--repo",
            str(repo),
            "--title",
            "API Crash Investigation",
            "--severity",
            "P2",
            "--goal",
            "Bound the crash and add a repair plan",
            "--impact",
            "Some requests fail immediately",
            "--observed",
            "Server exits with a traceback",
            "--validation",
            "Crash path is reproduced and then eliminated",
            "--date",
            "2026-04-05",
        ]
    )
    return {
        "init_result": _normalize_paths(init_result, repo),
        "plans_md": (repo / "docs" / "PLANS.md").read_text(encoding="utf-8"),
    }


def _run_case(case_name: str, update_golden: bool) -> None:
    case_root = _fixture_root() / case_name
    fixture = _read_json(case_root / "input.json")
    with tempfile.TemporaryDirectory(prefix=f"harness-fix-{case_name}-") as temp_dir:
        repo = Path(temp_dir) / "repo"
        repo.mkdir(parents=True, exist_ok=True)
        if case_name == "managed-e2e":
            observed = _run_case_managed_e2e(repo, fixture)
        elif case_name == "unmanaged-plans-safe":
            observed = _run_case_unmanaged_plans_safe(repo, fixture)
        else:
            raise ValueError(f"Unknown case: {case_name}")

        golden_path = case_root / "golden.json"
        if update_golden:
            _write_json(golden_path, observed)
            return

        expected = _read_json(golden_path)
        if observed != expected:
            raise AssertionError(
                f"{case_name} mismatch\nACTUAL:\n{json.dumps(observed, ensure_ascii=False, indent=2)}\nEXPECTED:\n{json.dumps(expected, ensure_ascii=False, indent=2)}"
            )


def main() -> int:
    cases = ["managed-e2e", "unmanaged-plans-safe"]
    update = "--update-golden" in __import__("sys").argv
    for case_name in cases:
        _run_case(case_name, update)
        print(f"[ok] {case_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
