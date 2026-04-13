import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class HarnessContentTests(unittest.TestCase):
    def test_new_skills_exist(self) -> None:
        self.assertTrue((ROOT / "skills/harness-using/SKILL.md").is_file())
        self.assertTrue((ROOT / "skills/harness-verify/SKILL.md").is_file())

    def test_harness_using_routes_all_core_paths(self) -> None:
        content = read_text("skills/harness-using/SKILL.md")
        for keyword in [
            "harness-bootstrap",
            "harness-garden",
            "harness-feat",
            "harness-fix",
            "harness-verify",
        ]:
            with self.subTest(keyword=keyword):
                self.assertIn(keyword, content)

    def test_harness_verify_contains_fresh_evidence_rule(self) -> None:
        content = read_text("skills/harness-verify/SKILL.md")
        self.assertIn("NO COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE", content)
        self.assertIn("the command that proves the claim", content)

    def test_harness_feat_forbids_placeholder_plans(self) -> None:
        content = read_text("skills/harness-feat/SKILL.md")
        self.assertIn("Plan quality bar: no placeholders", content)
        self.assertIn("docs/exec-plans/active/", content)
        self.assertIn("alternate planning directories such as `docs/superpowers/plans/`", content)

    def test_harness_feat_review_order_is_spec_then_quality(self) -> None:
        content = read_text("skills/harness-feat/SKILL.md")
        spec_pos = content.index("spec compliance review first")
        quality_pos = content.index("code quality review second")
        self.assertLess(spec_pos, quality_pos)

    def test_harness_fix_contains_attempt_stop_rule(self) -> None:
        content = read_text("skills/harness-fix/SKILL.md")
        self.assertIn("NO FIX WITHOUT REPRODUCTION EVIDENCE", content)
        self.assertIn("THREE FAILED FIX ATTEMPTS MEAN STOP AND REPLAN", content)
        self.assertIn("three failed fix attempts", content.lower())

    def test_suite_docs_and_readme_mention_new_skills(self) -> None:
        targets = [
            "README.md",
            "README.zh.md",
            "docs/harness-suite.en.md",
            "docs/harness-suite.zh.md",
        ]
        for target in targets:
            content = read_text(target)
            with self.subTest(target=target):
                self.assertIn("harness-using", content)
                self.assertIn("harness-verify", content)

    def test_codex_install_doc_exists(self) -> None:
        content = read_text(".codex/INSTALL.md")
        self.assertIn("native skill discovery", content)
        self.assertIn("harness-using", content)


if __name__ == "__main__":
    unittest.main()
