import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTION_ROOT = ROOT / "notion"
NOTION_SKILLS = NOTION_ROOT / "skills"
NOTION_INSTRUCTIONS = NOTION_ROOT / "instructions"
REFERENCE_DOC = ROOT / "docs" / "reference" / "notion" / "README.md"

EXPECTED_SKILLS = {
    "tech-planner.md": [
        "Research Dossier",
        "Concept Dependency Map",
        "Series Outline",
        "Coherence Notes",
        "Do not mirror the official documentation table of contents.",
    ],
    "tech-writing.md": [
        "Anchor Sheet",
        "Central argument",
        "Narrative Voices",
        "60-second rule",
        "Do not fill missing measurements or source facts with invented precision.",
    ],
    "tech-rewrite.md": [
        "Fact Register",
        "KEPT",
        "DISCARDED",
        "MISSING",
        "AMBIGUOUS",
        "Contamination Risk Assessment",
        "Do not inherit the source structure unless it is justified by the target argument.",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class NotionWritingSkillTests(unittest.TestCase):
    def test_expected_notion_skill_pages_exist(self) -> None:
        actual = {path.name for path in NOTION_SKILLS.glob("*.md")}
        self.assertEqual(actual, set(EXPECTED_SKILLS))

    def test_notion_skill_pages_are_not_codex_skill_files(self) -> None:
        for path in sorted(NOTION_SKILLS.glob("*.md")):
            with self.subTest(path=path.name):
                content = read_text(path)
                self.assertFalse(content.startswith("---\n"))
                self.assertIn("Notion Skill", content)
                self.assertIn("When To Use", content)
                self.assertIn("Stop Rules", content)

    def test_notion_skill_pages_preserve_write_suite_gates(self) -> None:
        for filename, required_terms in EXPECTED_SKILLS.items():
            content = read_text(NOTION_SKILLS / filename)
            for term in required_terms:
                with self.subTest(filename=filename, term=term):
                    self.assertIn(term, content)

    def test_instructions_keep_persistent_rules_separate(self) -> None:
        content = read_text(NOTION_INSTRUCTIONS / "writing-agent.md")
        for term in [
            "always-on layer",
            "Do not put task-specific workflows here",
            "Skill Routing",
            "Tech Planner - Notion Skill",
            "Tech Writing - Notion Skill",
            "Tech Rewrite - Notion Skill",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, content)

    def test_reference_doc_uses_official_notion_model(self) -> None:
        content = read_text(REFERENCE_DOC)
        for term in [
            "Skills for Notion Agent",
            "Instructions for Notion Agent",
            "Skill",
            "Instructions",
            "Custom Agent",
            "Settings",
            "Notion AI",
            "Use as AI Skill",
            "Use as AI Instruction",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, content)

    def test_reference_doc_contains_first_use_smoke_tests(self) -> None:
        content = read_text(REFERENCE_DOC)
        for term in [
            "First-Use Smoke Tests",
            "@Tech Planner - Notion Skill",
            "@Tech Writing - Notion Skill",
            "@Tech Rewrite - Notion Skill",
            "Research Dossier",
            "Anchor Sheet",
            "Fact Register",
        ]:
            with self.subTest(term=term):
                self.assertIn(term, content)


if __name__ == "__main__":
    unittest.main()
