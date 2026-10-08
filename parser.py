"""Minimal, dependency-free parser for .env files."""

from __future__ import annotations

import re
from pathlib import Path

_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _clean_value(value: str) -> str:
    """Remove quotes and trailing inline comments from a raw value."""
    if value[:1] in ("'", '"'):
        quote = value[0]
        end = value.find(quote, 1)
        return value[1:end] if end != -1 else value[1:]
    comment = value.find(" #")
    if comment != -1:
        value = value[:comment]
    return value.strip()


def parse_env_text(text: str) -> dict[str, str]:
    """Parse the contents of a .env file into a {KEY: value} dict."""
    result: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not _KEY_RE.match(key):
            continue
        result[key] = _clean_value(value.strip())
    return result


def parse_env_file(path: str | Path) -> dict[str, str]:
    """Read and parse a .env file from disk."""
    text = Path(path).read_text(encoding="utf-8-sig")
    return parse_env_text(text)
