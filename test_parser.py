import unittest

from envaudit.parser import parse_env_text


class ParserTests(unittest.TestCase):
    def test_basic_pairs(self):
        self.assertEqual(parse_env_text("A=1\nB=two"), {"A": "1", "B": "two"})

    def test_comments_and_blank_lines(self):
        self.assertEqual(parse_env_text("# hi\n\nA=1\n  # x\n"), {"A": "1"})

    def test_export_prefix(self):
        self.assertEqual(parse_env_text("export TOKEN=abc"), {"TOKEN": "abc"})

    def test_quotes(self):
        text = "A=\"hello world\"\nB='x # y'\nC=\"\""
        self.assertEqual(parse_env_text(text), {"A": "hello world", "B": "x # y", "C": ""})

    def test_inline_comment(self):
        self.assertEqual(parse_env_text("A=value # note"), {"A": "value"})

    def test_empty_value_and_equals_in_value(self):
        self.assertEqual(parse_env_text("A=\nB=x=y"), {"A": "", "B": "x=y"})

    def test_invalid_lines_ignored(self):
        self.assertEqual(parse_env_text("not a pair\n1BAD=x\nGOOD=1"), {"GOOD": "1"})


if __name__ == "__main__":
    unittest.main()
