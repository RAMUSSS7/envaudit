import io
import tempfile
import unittest
from pathlib import Path

from envaudit.cli import EXIT_OK, EXIT_PROBLEMS, EXIT_USAGE, run_check


def make_project(env, example, gitignore):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    if env is not None:
        (root / ".env").write_text(env)
    if example is not None:
        (root / ".env.example").write_text(example)
    if gitignore is not None:
        (root / ".gitignore").write_text(gitignore)
    return tmp, root


def check(root):
    out = io.StringIO()
    code = run_check(
        str(root / ".env"), str(root / ".env.example"), str(root / ".gitignore"), out
    )
    return code, out.getvalue()


class CliTests(unittest.TestCase):
    def test_all_good(self):
        tmp, root = make_project("A=1\nB=2", "A=\nB=", ".env\n")
        with tmp:
            code, output = check(root)
        self.assertEqual(code, EXIT_OK)
        self.assertIn("[OK]", output)

    def test_key_missing_from_example(self):
        tmp, root = make_project("A=1\nSECRET=x", "A=", ".env\n")
        with tmp:
            code, output = check(root)
        self.assertEqual(code, EXIT_PROBLEMS)
        self.assertIn("SECRET is in .env but missing from .env.example", output)

    def test_key_missing_from_env(self):
        tmp, root = make_project("A=1", "A=\nNEW_KEY=", ".env\n")
        with tmp:
            code, output = check(root)
        self.assertEqual(code, EXIT_PROBLEMS)
        self.assertIn("NEW_KEY is in .env.example but missing from .env", output)

    def test_env_not_ignored(self):
        tmp, root = make_project("A=1", "A=", "*.log\n")
        with tmp:
            code, output = check(root)
        self.assertEqual(code, EXIT_PROBLEMS)
        self.assertIn("not ignored", output)

    def test_missing_gitignore_counts_as_not_ignored(self):
        tmp, root = make_project("A=1", "A=", None)
        with tmp:
            code, _ = check(root)
        self.assertEqual(code, EXIT_PROBLEMS)

    def test_missing_files_is_usage_error(self):
        tmp, root = make_project(None, "A=", ".env\n")
        with tmp:
            code, _ = check(root)
        self.assertEqual(code, EXIT_USAGE)


if __name__ == "__main__":
    unittest.main()
