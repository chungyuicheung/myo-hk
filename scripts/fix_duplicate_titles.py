#!/usr/bin/env python3
"""
Fix duplicate <title> tags among blog articles.

When two articles share the same <title>, the simpler filename keeps its title
unchanged while the more descriptive filename gets a disambiguation suffix.

Pattern: base_name.html + base_name_suffix.html both have identical titles.
Strategy: keep base_name.html's title, append "（進階版）" to base_name_suffix.html's title.

Usage: python3 scripts/fix_duplicate_titles.py [--test]
"""

import re
import sys
from pathlib import Path

from typing import Optional

BLOG_DIR = Path(__file__).parent.parent / "blog"


def extract_title(content: str) -> Optional[str]:
    """Extract <title> content from HTML."""
    m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
    return m.group(1).strip() if m else None


def find_duplicate_groups() -> list[list[str]]:
    """Find groups of articles sharing the same <title>."""
    title_map: dict[str, list[str]] = {}
    for fpath in sorted(BLOG_DIR.glob("*.html")):
        content = fpath.read_text(encoding="utf-8")
        title = extract_title(content)
        if title:
            title_map.setdefault(title, []).append(fpath.name)
    return [files for files in title_map.values() if len(files) > 1]


def is_shorter_name(a: str, b: str) -> bool:
    """Return True if a has fewer characters than b (simpler filename)."""
    return len(a) < len(b)


def fix_duplicate_titles(test_mode: bool = False) -> int:
    """Fix duplicate titles. Returns count of changes made."""
    groups = find_duplicate_groups()
    changed = 0

    for files in groups:
        # Sort: simpler (shorter) name first
        files_sorted = sorted(files, key=len)
        simple_name = files_sorted[0]
        specific_name = files_sorted[1]

        simple_path = BLOG_DIR / simple_name
        specific_path = BLOG_DIR / specific_name

        simple_content = simple_path.read_text(encoding="utf-8")
        specific_content = specific_path.read_text(encoding="utf-8")

        simple_title = extract_title(simple_content)
        specific_title = extract_title(specific_content)

        if not simple_title or not specific_title:
            continue

        # Only fix when titles are identical (true duplicates)
        if simple_title != specific_title:
            continue

        # Append disambiguation suffix to the more specific filename's title
        suffix = "（進階版）"
        new_specific_title = specific_title + suffix

        new_content = re.sub(
            r"<title>(.*?)</title>",
            f"<title>{new_specific_title}</title>",
            specific_content,
            count=1,
            flags=re.IGNORECASE,
        )

        if new_content != specific_content:
            if not test_mode:
                specific_path.write_text(new_content, encoding="utf-8")
            marker = "✓" if not test_mode else "○"
            print(f"  {marker} {specific_name}: \"{specific_title}\" → \"{new_specific_title}\"")
            changed += 1

    return changed


def main() -> None:
    test_mode = "--test" in sys.argv
    print(f"Scanning {BLOG_DIR} for duplicate titles...")
    changed = fix_duplicate_titles(test_mode=test_mode)
    status = "[DRY-RUN] " if test_mode else ""
    print(f"\n{status}Fixed {changed} duplicate title pair(s).")


if __name__ == "__main__":
    main()
