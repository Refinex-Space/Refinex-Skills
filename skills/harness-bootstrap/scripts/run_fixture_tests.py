#!/usr/bin/env python3

from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict


def _skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _fixture_root() -> Path:
    return _skill_root() / "assets" / "test-fixtures"


def _read_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _materialize_files(repo: Path, files: Dict[str, str]) -> None:
    for rel_path, content in files.items():
        path = repo / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _normalize_bootstrap_result(result: Dict[str, object], repo: Path) -> Dict[str, object]:
    normalized = copy.deepcopy(result)
    repo_resolved = repo.resolve()
    normalized["repo"] = "<REPO>"
    profile = normalized.get("profile", {})
    if isinstance(profile, dict):
        profile["repo_name"] = "fixture-repo"
    check_result = normalized.get("check_result", {})
    if isinstance(check_result, dict):
        for key in ("manifest_path", "check_path"):
            if key in check_result:
                check_result[key] = str(Path(check_result[key]).resolve().relative_to(repo_resolved))
    return normalized


def _read_expected_files(repo: Path, rel_paths: Dict[str, str]) -> Dict[str, str]:
    return {rel_path: (repo / rel_path).read_text(encoding="utf-8") for rel_path in rel_paths}


def _assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(
            f"{label} mismatch\nACTUAL:\n{json.dumps(actual, ensure_ascii=False, indent=2)}\nEXPECTED:\n{json.dumps(expected, ensure_ascii=False, indent=2)}"
        )


def _run_bootstrap(repo: Path, language: str) -> Dict[str, object]:
    script = _skill_root() / "scripts" / "bootstrap_harness.py"
    result = subprocess.run(
        ["python3", str(script), "--repo", str(repo), "--language", language, "--date", "2026-04-05", "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _run_repo_check(repo: Path) -> Dict[str, object]:
    result = subprocess.run(
        ["python3", str(repo / "scripts" / "check_harness.py"), "--repo", str(repo), "--format", "json"],
        check=False,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _case_paths(case_name: str) -> Dict[str, Path]:
    case_root = _fixture_root() / case_name
    return {
        "case_root": case_root,
        "input": case_root / "input.json",
        "golden": case_root / "golden.json",
    }


def run_case(case_name: str, update_golden: bool) -> None:
    paths = _case_paths(case_name)
    fixture = _read_json(paths["input"])
    with tempfile.TemporaryDirectory(prefix=f"harness-bootstrap-{case_name}-") as temp_dir:
        repo = Path(temp_dir) / "repo"
        repo.mkdir(parents=True, exist_ok=True)
        _materialize_files(repo, fixture["files"])

        result = _run_bootstrap(repo, fixture.get("language", "zh"))
        normalized_result = _normalize_bootstrap_result(result, repo)
        observed = {
            "result": normalized_result,
            "repo_check": _run_repo_check(repo),
            "files": _read_expected_files(repo, fixture.get("golden_files", {})),
        }

        if update_golden:
            _write_json(paths["golden"], observed)
            return

        golden = _read_json(paths["golden"])
        _assert_equal(observed["result"], golden["result"], f"{case_name} result")
        _assert_equal(observed["repo_check"], golden["repo_check"], f"{case_name} repo_check")
        _assert_equal(observed["files"], golden["files"], f"{case_name} files")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run fixed fixture regression tests for harness-bootstrap")
    parser.add_argument("--case", action="append", dest="cases", help="Specific case name to run")
    parser.add_argument("--update-golden", action="store_true", help="Rewrite golden.json files from current output")
    args = parser.parse_args()

    case_root = _fixture_root()
    cases = args.cases or sorted(path.name for path in case_root.iterdir() if path.is_dir())
    for case_name in cases:
        run_case(case_name, args.update_golden)
        print(f"[ok] {case_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
