import tempfile
import unittest
from pathlib import Path
from unittest import mock

from commit_scope import allowed_scopes, check_message, first_message_line

SETTINGS = 'include(":shared")\ninclude(":androidApp")\ninclude(":core:network", ":core:common")'


class AllowedScopesTest(unittest.TestCase):
    def test_module_paths_and_areas_are_allowed(self):
        scopes = allowed_scopes(SETTINGS)
        for s in [
            "shared",
            "androidApp",
            "core:network",
            "core:common",
            "build",
            "build-logic",
            "ci",
            "deps",
            "tooling",
            "docs",
            "release",
        ]:
            self.assertIn(s, scopes)

    def test_parent_directory_of_nested_modules_is_allowed(self):
        self.assertIn("core", allowed_scopes(SETTINGS))

    def test_unknown_module_is_not_allowed(self):
        self.assertNotIn("iosApp", allowed_scopes(SETTINGS))

    def test_modules_are_read_from_the_real_settings_file(self):
        settings = Path(__file__).resolve().parents[2] / "settings.gradle.kts"
        scopes = allowed_scopes(settings.read_text())
        self.assertIn("shared", scopes)
        self.assertIn("androidApp", scopes)


class CheckMessageTest(unittest.TestCase):
    def test_valid_scope_passes(self):
        self.assertIsNone(check_message("feat(shared): add greeting", allowed_scopes(SETTINGS)))

    def test_nested_module_scope_passes(self):
        self.assertIsNone(check_message("feat(core:network): add problem decoding", allowed_scopes(SETTINGS)))

    def test_parent_directory_scope_passes(self):
        self.assertIsNone(check_message("feat(core): add the core modules", allowed_scopes(SETTINGS)))

    def test_breaking_marker_passes(self):
        self.assertIsNone(check_message("feat(shared)!: drop the old greeting", allowed_scopes(SETTINGS)))

    def test_unknown_scope_fails_naming_it(self):
        self.assertIn("shard", check_message("fix(shard): typo", allowed_scopes(SETTINGS)))

    def test_missing_scope_fails(self):
        self.assertIsNotNone(check_message("fix: something", allowed_scopes(SETTINGS)))

    def test_ci_and_docs_may_omit_scope(self):
        for m in ["ci: add workflows", "docs: add contributing guide"]:
            self.assertIsNone(check_message(m, allowed_scopes(SETTINGS)))

    def test_build_tooling_scope_passes(self):
        self.assertIsNone(
            check_message("build(tooling): add app skeleton and repository configuration", allowed_scopes(SETTINGS))
        )

    def test_git_generated_messages_pass(self):
        for m in [
            "Merge branch 'develop' into feature/x",
            'Revert "feat(shared): x"',
            "fixup! feat(shared): x",
            "squash! feat(shared): x",
            "amend! feat(shared): x",
        ]:
            self.assertIsNone(check_message(m, allowed_scopes(SETTINGS)))

    def test_unknown_type_fails_naming_it(self):
        self.assertIn("feature", check_message("feature(shared): x", allowed_scopes(SETTINGS)))

    def test_uppercase_summary_fails(self):
        self.assertIsNotNone(check_message("feat(shared): Add greeting", allowed_scopes(SETTINGS)))

    def test_trailing_period_fails(self):
        self.assertIsNotNone(check_message("feat(shared): add greeting.", allowed_scopes(SETTINGS)))

    def test_missing_space_after_colon_fails(self):
        self.assertIsNotNone(check_message("feat(shared):add greeting", allowed_scopes(SETTINGS)))

    def test_empty_summary_fails(self):
        self.assertIsNotNone(check_message("feat(shared): ", allowed_scopes(SETTINGS)))

    def test_header_length_limit_is_72(self):
        prefix = "feat(shared): "
        at_limit = prefix + "a" * (72 - len(prefix))
        self.assertEqual(72, len(at_limit))
        self.assertIsNone(check_message(at_limit, allowed_scopes(SETTINGS)))
        self.assertIsNotNone(check_message(at_limit + "a", allowed_scopes(SETTINGS)))


class FirstMessageLineTest(unittest.TestCase):
    def test_file_is_read_as_utf_8(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "COMMIT_EDITMSG"
            path.write_text("# café comment\nfeat(shared): add greeting\n", encoding="utf-8")
            with mock.patch("io.text_encoding", side_effect=lambda encoding, stacklevel=2: encoding or "ascii"):
                self.assertEqual("feat(shared): add greeting", first_message_line(str(path)))


if __name__ == "__main__":
    unittest.main()
