import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = ROOT / "tests/fixtures"
VALIDATOR_SOURCE = ROOT / "skills/harness-bootstrap/scripts/check_harness.py"


def prepare_fixture(name: str) -> Path:
    temp_root = Path(tempfile.mkdtemp(prefix=f"harness-fixture-{name}-"))
    fixture_src = FIXTURE_ROOT / name
    fixture_dst = temp_root / name
    shutil.copytree(fixture_src, fixture_dst)
    scripts_dir = fixture_dst / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(VALIDATOR_SOURCE, scripts_dir / "check_harness.py")
    return fixture_dst


class CheckHarnessIntegrationTests(unittest.TestCase):
    def run_fixture(self, name: str) -> subprocess.CompletedProcess[str]:
        fixture_dir = prepare_fixture(name)
        self.addCleanup(shutil.rmtree, fixture_dir.parent, True)
        return subprocess.run(
            [sys.executable, "scripts/check_harness.py"],
            cwd=fixture_dir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_good_fixture_passes(self) -> None:
        result = self.run_fixture("control-plane-good")
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("All checks passed", result.stdout)

    def test_missing_file_fixture_fails(self) -> None:
        result = self.run_fixture("control-plane-bad-missing")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MISSING file: docs/OBSERVABILITY.md", result.stdout)

    def test_broken_link_fixture_fails(self) -> None:
        result = self.run_fixture("control-plane-bad-link")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BROKEN LINK in AGENTS.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
