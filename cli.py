"""Command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .checks import audit
from .gitignore import is_ignored
from .parser import parse_env_file

EXIT_OK = 0
EXIT_PROBLEMS = 1
EXIT_USAGE = 2


def run_check(env_path: str, example_path: str, gitignore_path: str, out=None) -> int:
    out = out or sys.stdout
    env_file, example_file, ignore_file = (
        Path(env_path),
        Path(example_path),
        Path(gitignore_path),
    )

    for label, p in ((".env file", env_file), ("example file", example_file)):
        if not p.is_file():
            print(f"error: {label} not found: {p}", file=sys.stderr)
            return EXIT_USAGE

    env_keys = parse_env_file(env_file)
    example_keys = parse_env_file(example_file)
    ignore_text = (
        ignore_file.read_text(encoding="utf-8-sig") if ignore_file.is_file() else ""
    )
    report = audit(env_keys, example_keys, is_ignored(ignore_text, env_file.name))

    for key in report.missing_in_example:
        print(f"[ERROR] {key} is in {env_file.name} but missing from {example_file.name}", file=out)
    for key in report.missing_in_env:
        print(f"[ERROR] {key} is in {example_file.name} but missing from {env_file.name}", file=out)
    if report.env_not_ignored:
        print(
            f"[ERROR] {env_file.name} is not ignored by {ignore_file.name} "
            "(your secrets could be committed!)",
            file=out,
        )

    if report.ok:
        print(f"[OK] {env_file.name} and {example_file.name} are in sync.", file=out)
        return EXIT_OK
    return EXIT_PROBLEMS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="envaudit",
        description="Keep your .env and .env.example files in sync.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="compare .env with .env.example")
    check.add_argument("--env", default=".env", help="path to your .env (default: .env)")
    check.add_argument(
        "--example", default=".env.example", help="path to the template (default: .env.example)"
    )
    check.add_argument(
        "--gitignore", default=".gitignore", help="path to .gitignore (default: .gitignore)"
    )
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "check":
        return run_check(args.env, args.example, args.gitignore)
    return EXIT_USAGE  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
