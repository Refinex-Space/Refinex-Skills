#!/usr/bin/env python3

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict


def _skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _fixture_root() -> Path:
    return _skill_root() / "assets" / "test-fixtures"


def _bootstrap_script() -> Path:
    return _skill_root().parent / "harness-bootstrap" / "scripts" / "bootstrap_harness.py"


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


def _normalize_payload(payload: Dict[str, object]) -> Dict[str, object]:
    normalized = copy.deepcopy(payload)

    def _walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "repo_name" and isinstance(value, str):
                    node[key] = "fixture-repo"
                elif key == "repo" and isinstance(value, str):
                    node[key] = "<REPO>"
                else:
                    _walk(value)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(normalized)
    return normalized


def _assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(
            f"{label} mismatch\nACTUAL:\n{json.dumps(actual, ensure_ascii=False, indent=2)}\nEXPECTED:\n{json.dumps(expected, ensure_ascii=False, indent=2)}"
        )


def _run_bootstrap(repo: Path, language: str) -> Dict[str, object]:
    result = subprocess.run(
        ["python3", str(_bootstrap_script()), "--repo", str(repo), "--language", language, "--date", "2026-04-05", "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _run_repair(repo: Path) -> Dict[str, object]:
    script = _skill_root() / "scripts" / "repair_harness.py"
    result = subprocess.run(
        ["python3", str(script), "--repo", str(repo), "--mode", "safe-fix", "--date", "2026-04-05", "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _run_audit(repo: Path) -> Dict[str, object]:
    script = _skill_root() / "scripts" / "audit_harness.py"
    result = subprocess.run(
        ["python3", str(script), "--repo", str(repo), "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _read_expected_files(repo: Path, rel_paths: Dict[str, str]) -> Dict[str, str]:
    return {rel_path: (repo / rel_path).read_text(encoding="utf-8") for rel_path in rel_paths}


def _prepare_managed_drift(repo: Path, fixture: Dict[str, object]) -> None:
    _materialize_files(repo, fixture["files"])
    _run_bootstrap(repo, fixture.get("language", "zh"))
    (repo / "docs" / "OBSERVABILITY.md").unlink()
    (repo / "docs" / "generated" / "harness-manifest.md").write_text(
        "<!-- HARNESS:MANAGED FILE -->\n# stale manifest\n",
        encoding="utf-8",
    )
    (repo / "scripts" / "check_harness.py").write_text(
        "# HARNESS:MANAGED FILE\n#!/usr/bin/env python3\nprint('stale')\n",
        encoding="utf-8",
    )


def _prepare_unmanaged_strategy(repo: Path, fixture: Dict[str, object]) -> None:
    _materialize_files(repo, fixture["files"])


def run_case(case_name: str, update_golden: bool) -> None:
    case_root = _fixture_root() / case_name
    fixture = _read_json(case_root / "input.json")
    with tempfile.TemporaryDirectory(prefix=f"harness-garden-{case_name}-") as temp_dir:
        repo = Path(temp_dir) / "repo"
        repo.mkdir(parents=True, exist_ok=True)

        kind = fixture["kind"]
        if kind == "managed-drift":
            _prepare_managed_drift(repo, fixture)
        elif kind == "unmanaged-strategy":
            _prepare_unmanaged_strategy(repo, fixture)
        else:
            raise ValueError(f"Unsupported fixture kind: {kind}")

        repair_result = _normalize_payload(_run_repair(repo))
        post_audit = _normalize_payload(_run_audit(repo))
        observed = {
            "repair_result": repair_result,
            "post_audit": post_audit,
            "files": _read_expected_files(repo, fixture.get("golden_files", {})),
        }

        golden_path = case_root / "golden.json"
        if update_golden:
            _write_json(golden_path, observed)
            return

        golden = _read_json(golden_path)
        _assert_equal(observed["repair_result"], golden["repair_result"], f"{case_name} repair_result")
        _assert_equal(observed["post_audit"], golden["post_audit"], f"{case_name} post_audit")
        _assert_equal(observed["files"], golden["files"], f"{case_name} files")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run fixed fixture regression tests for harness-garden")
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
