"""Bump the version literal in src/flappy_raqui/__version__.py.

    python .github/scripts/bump_version.py [major|minor|patch]

That file is the project's single source of truth: hatchling reads
`__version__` from it at build time (see `[tool.hatch.version]` in
pyproject.toml), so a release only has to edit the literal. Everything around
the literal is rewritten verbatim, so the module stays valid Python.

The new version is echoed to stdout and, when running under Actions, written to
$GITHUB_OUTPUT as `new_version` so later steps and jobs can consume it.
"""

import os
import re
import sys
from pathlib import Path

VERSION_FILE = Path("src/flappy_raqui/__version__.py")

# Captures the quoted literal so the surrounding text (comments, docstring,
# quote style) survives the rewrite untouched.
VERSION_RE = re.compile(
    r"""(?P<prefix>^__version__\s*=\s*(?P<quote>["']))"""
    r"""(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"""
    r"""(?P=quote)""",
    re.MULTILINE,
)

BUMP_TYPES = ("major", "minor", "patch")


def main() -> int:
    bump_type = sys.argv[1] if len(sys.argv) > 1 else "patch"
    if bump_type not in BUMP_TYPES:
        print(
            f"Unknown bump type {bump_type!r}, expected one of {', '.join(BUMP_TYPES)}",
            file=sys.stderr,
        )
        return 2

    source = VERSION_FILE.read_text()
    match = VERSION_RE.search(source)
    if match is None:
        print(
            f'No `__version__ = "X.Y.Z"` assignment found in {VERSION_FILE}',
            file=sys.stderr,
        )
        return 1

    major, minor, patch = (int(match[part]) for part in ("major", "minor", "patch"))

    if bump_type == "major":
        major, minor, patch = major + 1, 0, 0
    elif bump_type == "minor":
        minor, patch = minor + 1, 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    quote = match["quote"]
    VERSION_FILE.write_text(
        f"{source[: match.start()]}{match['prefix']}{new_version}{quote}"
        f"{source[match.end() :]}"
    )

    print(f"Bumped version to {new_version}")
    if github_output := os.environ.get("GITHUB_OUTPUT"):
        with open(github_output, "a") as f:
            f.write(f"new_version={new_version}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
