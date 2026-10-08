"""A small .gitignore matcher, just enough to answer: is this file ignored?"""

from __future__ import annotations

from fnmatch import fnmatchcase


def is_ignored(gitignore_text: str, filename: str = ".env") -> bool:
    """Return True if `filename` (in the repo root) is ignored by the rules.

    Later rules override earlier ones, and `!pattern` re-includes a file,
    just like Git does.
    """
    ignored = False
    for raw in gitignore_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        negate = line.startswith("!")
        if negate:
            line = line[1:]
        if line.endswith("/"):  # directory-only rule, never matches a file
            continue
        line = line.lstrip("/")
        while line.startswith("**/"):
            line = line[3:]
        if fnmatchcase(filename, line):
            ignored = not negate
    return ignored
