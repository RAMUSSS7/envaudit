import unittest

from envaudit.gitignore import is_ignored


class GitignoreTests(unittest.TestCase):
    def test_exact(self):
        self.assertTrue(is_ignored(".env\n"))

    def test_leading_slash(self):
        self.assertTrue(is_ignored("/.env"))

    def test_wildcards(self):
        self.assertTrue(is_ignored(".env*"))
        self.assertTrue(is_ignored("*.env"))

    def test_not_ignored(self):
        self.assertFalse(is_ignored("node_modules/\n*.log\n"))
        self.assertFalse(is_ignored(""))

    def test_comment_is_not_a_rule(self):
        self.assertFalse(is_ignored("# .env"))

    def test_negation_overrides(self):
        self.assertFalse(is_ignored(".env*\n!.env"))
        self.assertTrue(is_ignored("!.env\n.env"))

    def test_directory_rule_does_not_match_file(self):
        self.assertFalse(is_ignored(".env/"))


if __name__ == "__main__":
    unittest.main()
