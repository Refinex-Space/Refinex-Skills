import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = ROOT / "plugins" / "harness-powers"
SKILLS_ROOT = PLUGIN_ROOT / "skills"

EXPECTED_SKILLS = {
    "harness-using",
    "harness-brainstorm",
    "harness-plan",
    "harness-execute",
    "harness-bootstrap",
    "harness-garden",
    "harness-feat",
    "harness-fix",
    "harness-verify",
    "harness-review",
    "harness-dispatch",
    "harness-worktree",
    "harness-finish",
    "harness-frontend",
}

LEGACY_SKILLS = {
    "using-superpowers",
    "brainstorming",
    "writing-plans",
    "executing-plans",
    "test-driven-development",
    "systematic-debugging",
    "verification-before-completion",
    "requesting-code-review",
    "receiving-code-review",
    "subagent-driven-development",
    "dispatching-parallel-agents",
    "using-git-worktrees",
    "finishing-a-development-branch",
}

FORBIDDEN_DEFAULT_PATHS = {
    "docs/superpowers/specs",
    "docs/superpowers/plans",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class HarnessPowersPluginTests(unittest.TestCase):
    def test_plugin_metadata_exists_and_points_to_skills(self) -> None:
        plugin_json = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
        self.assertTrue(plugin_json.is_file())

        metadata = json.loads(read_text(plugin_json))
        self.assertEqual(metadata["name"], "harness-powers")
        self.assertEqual(metadata["skills"], "./skills/")
        self.assertEqual(metadata["interface"]["displayName"], "Harness Powers")

    def test_expected_public_skill_directories_exist(self) -> None:
        for skill in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=skill):
                self.assertTrue((SKILLS_ROOT / skill).is_dir())
                self.assertTrue((SKILLS_ROOT / skill / "SKILL.md").is_file())

    def test_legacy_superpowers_skill_directories_are_not_published(self) -> None:
        for skill in sorted(LEGACY_SKILLS):
            with self.subTest(skill=skill):
                self.assertFalse((SKILLS_ROOT / skill).exists())

    def test_skill_frontmatter_names_match_directories(self) -> None:
        for skill in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=skill):
                content = read_text(SKILLS_ROOT / skill / "SKILL.md")
                self.assertTrue(content.startswith("---\n"))
                self.assertIn(f"name: {skill}", content)
                self.assertIn("description:", content)

    def test_plugin_skills_do_not_use_superpowers_default_paths(self) -> None:
        for skill_file in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
            content = read_text(skill_file)
            for forbidden in FORBIDDEN_DEFAULT_PATHS:
                with self.subTest(skill=skill_file.parent.name, forbidden=forbidden):
                    self.assertNotIn(forbidden, content)

    def test_readme_lists_public_skill_inventory(self) -> None:
        content = read_text(PLUGIN_ROOT / "README.md")
        for skill in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=skill):
                self.assertIn(f"`{skill}`", content)

    def test_harness_using_routes_core_harness_powers_paths(self) -> None:
        content = read_text(SKILLS_ROOT / "harness-using" / "SKILL.md")
        for keyword in [
            "harness-brainstorm",
            "harness-plan",
            "harness-execute",
            "harness-review",
            "harness-verify",
        ]:
            with self.subTest(keyword=keyword):
                self.assertIn(keyword, content)

    def test_harness_verify_contains_reporting_contract(self) -> None:
        content = read_text(SKILLS_ROOT / "harness-verify" / "SKILL.md")
        for keyword in ["Claim:", "Command:", "Result:", "Conclusion:"]:
            with self.subTest(keyword=keyword):
                self.assertIn(keyword, content)

    def test_harness_review_priority_order_is_explicit(self) -> None:
        content = read_text(SKILLS_ROOT / "harness-review" / "SKILL.md")
        self.assertIn("security > correctness > performance > readability", content)

    def test_harness_dispatch_worker_output_contract_is_explicit(self) -> None:
        content = read_text(SKILLS_ROOT / "harness-dispatch" / "SKILL.md")
        for keyword in ["changed files", "verification", "residual risks"]:
            with self.subTest(keyword=keyword):
                self.assertIn(keyword, content.lower())

    def test_tdd_and_debugging_are_internalized_as_references(self) -> None:
        feat = read_text(SKILLS_ROOT / "harness-feat" / "SKILL.md")
        fix = read_text(SKILLS_ROOT / "harness-fix" / "SKILL.md")

        self.assertIn("references/tdd-discipline.md", feat)
        self.assertIn("references/testing-anti-patterns.md", feat)
        self.assertTrue((SKILLS_ROOT / "harness-feat" / "references" / "tdd-discipline.md").is_file())
        self.assertTrue((SKILLS_ROOT / "harness-feat" / "references" / "testing-anti-patterns.md").is_file())

        self.assertIn("references/systematic-debugging.md", fix)
        self.assertTrue((SKILLS_ROOT / "harness-fix" / "references" / "systematic-debugging.md").is_file())


if __name__ == "__main__":
    unittest.main()
