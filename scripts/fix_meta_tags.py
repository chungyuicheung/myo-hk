#!/usr/bin/env python3
"""
Fix missing critical meta tags across key pages.

Adds:
- <meta name="robots" content="index, follow"> to v2.html and blog/index.html
- <meta property="og:image" content="..."> to poster.html

Usage: python3 scripts/fix_meta_tags.py [--test]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
BASE_URL = "https://myo-makeyourown.pages.dev"
LOGO_URL = f"{BASE_URL}/image/01_company_logo.webp"

PAGES_TO_FIX = [
    ("v2.html", "robots"),
    ("blog/index.html", "robots"),
    ("poster.html", "og_image"),
]


def ensure_robots_meta(content: str, page_name: str, test_mode: bool, root: Path = ROOT) -> tuple[str, bool]:
    """Add robots meta if missing. Returns (new_content, changed)."""
    if 'name="robots"' in content:
        return content, False

    robots_tag = '<meta name="robots" content="index, follow">'
    head_end = content.find("</head>")
    if head_end == -1:
        return content, False

    meta_pattern = re.compile(r'\s*<meta[^>]*>\s*\n?', re.MULTILINE)
    last_meta = None
    for m in meta_pattern.finditer(content[:head_end]):
        last_meta = m

    if last_meta:
        insert_pos = last_meta.end()
        new_content = content[:insert_pos] + robots_tag + "\n" + content[insert_pos:]
    else:
        new_content = content[:head_end] + robots_tag + "\n" + content[head_end:]

    print(f"  ✓ {page_name}: added robots meta")
    if not test_mode:
        path = root / page_name
        path.write_text(new_content, encoding="utf-8")
    return new_content, True


def ensure_og_image(content: str, page_name: str, test_mode: bool, root: Path = ROOT) -> tuple[str, bool]:
    """Add og:image meta if missing. Returns (new_content, changed)."""
    if 'property="og:image"' in content:
        return content, False

    og_tag = f'<meta property="og:image" content="{LOGO_URL}">'
    head_end = content.find("</head>")
    if head_end == -1:
        return content, False

    new_content = content[:head_end] + og_tag + "\n" + content[head_end:]

    print(f"  ✓ {page_name}: added og:image meta")
    if not test_mode:
        path = root / page_name
        path.write_text(new_content, encoding="utf-8")
    return new_content, True


def fix_pages(test_mode: bool = False, root: Path = ROOT) -> list[tuple[str, str]]:
    """Fix meta tags across all configured pages. Returns list of (page, tag) changed."""
    changes = []

    for page_name, fix_type in PAGES_TO_FIX:
        page_path = root / page_name
        if not page_path.exists():
            continue

        content = page_path.read_text(encoding="utf-8")

        if fix_type == "robots":
            new_content, changed = ensure_robots_meta(content, page_name, test_mode, root)
        elif fix_type == "og_image":
            new_content, changed = ensure_og_image(content, page_name, test_mode, root)
        else:
            continue

        if changed:
            changes.append((page_name, fix_type))

    return changes


def main() -> None:
    test_mode = "--test" in sys.argv
    changes = fix_pages(test_mode=test_mode)
    status = "[DRY-RUN] " if test_mode else ""
    print(f"\n{status}Fixed {len(changes)} meta tag issue(s).")
    for page, tag in changes:
        print(f"  - {page}: added <meta {tag}>")


if __name__ == "__main__":
    main()
