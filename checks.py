"""The actual audit logic."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Report:
    missing_in_example: list[str] = field(default_factory=list)
    missing_in_env: list[str] = field(default_factory=list)
    env_not_ignored: bool = False

    @property
    def ok(self) -> bool:
        return not (
            self.missing_in_example or self.missing_in_env or self.env_not_ignored
        )


def compare_keys(env_keys, example_keys) -> tuple[list[str], list[str]]:
    """Return (keys only in env, keys only in example), each sorted."""
    env_set, example_set = set(env_keys), set(example_keys)
    return sorted(env_set - example_set), sorted(example_set - env_set)


def audit(env_keys, example_keys, env_is_ignored: bool) -> Report:
    only_env, only_example = compare_keys(env_keys, example_keys)
    return Report(
        missing_in_example=only_env,
        missing_in_env=only_example,
        env_not_ignored=not env_is_ignored,
    )
