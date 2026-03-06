#!/usr/bin/env python3
"""Promote CHANGELOG Unreleased section to a concrete version and date."""

import os
import re
from datetime import date
from pathlib import Path

CHANGELOG_PATH = Path("CHANGELOG.md")


def main() -> None:
    version = os.environ.get("VERSION", "").strip()
    if not version:
        raise RuntimeError("VERSION env var is required")

    if not CHANGELOG_PATH.exists():
        raise RuntimeError("CHANGELOG.md not found")

    content = CHANGELOG_PATH.read_text(encoding="utf-8")
    unreleased_pattern = re.compile(r"^## \[Unreleased\]\s*$", re.MULTILINE)

    if unreleased_pattern.search(content):
        dated_header = f"## [{version}] - {date.today().isoformat()}"
        updated = unreleased_pattern.sub(dated_header, content, count=1)
        CHANGELOG_PATH.write_text(updated, encoding="utf-8")
        print(f"Changelog promoted: [Unreleased] -> [{version}]")
        return

    # If no Unreleased section exists, do not fail release: append a minimal section.
    minimal = (
        f"\n\n## [{version}] - {date.today().isoformat()}\n"
        "### Changed\n"
        "- Maintenance release.\n"
    )
    CHANGELOG_PATH.write_text(content.rstrip() + minimal + "\n", encoding="utf-8")
    print("No [Unreleased] section found; appended a minimal release section.")


if __name__ == "__main__":
    main()
