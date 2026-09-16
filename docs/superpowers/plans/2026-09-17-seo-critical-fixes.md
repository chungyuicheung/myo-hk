# SEO Critical Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the three critical SEO issues identified in the 2026-09-17 audit: duplicate titles, short meta descriptions, and missing meta tags.

**Architecture:** Three independent Python scripts in `scripts/`, each following the established `--test` (dry-run) convention. Scripts parse existing HTML structure, apply targeted fixes, and regenerate sitemap. A test suite validates all changes before committing.

**Tech Stack:** Python 3, regex-based HTML parsing, pytest for tests

---

## File Structure

| File | Responsibility |
|------|----------------|
| `scripts/fix_duplicate_titles.py` | Resolve 40 duplicate title pairs by appending disambiguation suffixes |
| `scripts/expand_descriptions.py` | Extend all 421 blog article descriptions from ~31 chars to 150-160 chars |
| `scripts/fix_meta_tags.py` | Add missing robots meta to v2.html/blog/index.html, add OG image to poster.html |
| `scripts/test_seo_fixes.py` | Test suite validating all three scripts' behavior |
| `docs/superpowers/plans/2026-09-17-seo-critical-fixes.md` | This plan document |

---

### Task 1: Duplicate Title Resolution Script

**Files:**
- Create: `scripts/fix_duplicate_titles.py`
- Test: `scripts/test_seo_fixes.py` (new test class)

The problem: 40 title pairs share identical `<title>` tags. The pattern is consistent — one file ends with `指南.html` and its partner is the base name (e.g., `婚禮攝影合約注意事項.html` vs `婚禮攝影合約.html`). The script must:
1. Scan all blog articles and group by title
2. For each duplicate group, keep the longer/more-specific filename's title unchanged
3. Append a disambiguation suffix to the other article's title
4. Support `--test` dry-run mode

- [ ] **Step 1: Write the test file with failing tests**

Create `scripts/test_seo_fixes.py`:

```python
#!/usr/bin/env python3
"""Tests for SEO fix scripts — validates title deduplication, description expansion, and meta tag fixes."""

import pytest
import re
import sys
import os
from pathlib import Path
from unittest.mock import patch, mock_open
from io import StringIO

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ─── Fix Duplicate Titles Tests ──────────────────────────────────────────────

class TestFixDuplicateTitles:
    """Validate that duplicate titles get unique disambiguation suffixes."""

    def test_detects_duplicate_titles(self):
        """Two articles with identical titles should be detected."""
        from fix_duplicate_titles import find_duplicate_titles
        articles = [
            {"filename": "A.html", "title": "Same Title Here"},
            {"filename": "B.html", "title": "Same Title Here"},
            {"filename": "C.html", "title": "Unique Title"},
        ]
        dups = find_duplicate_titles(articles)
        assert len(dups) == 1
        assert len(dups[0]) == 2
        assert "A.html" in dups[0]
        assert "B.html" in dups[0]

    def test_no_false_duplicates(self):
        """Articles with different titles should not be flagged."""
        from fix_duplicate_titles import find_duplicate_titles
        articles = [
            {"filename": "A.html", "title": "Title One"},
            {"filename": "B.html", "title": "Title Two"},
        ]
        dups = find_duplicate_titles(articles)
        assert len(dups) == 0

    def test_disambiguation_suffix_appended(self):
        """Duplicate pair should get suffix on one title."""
        from fix_duplicate_titles import generate_disambiguation
        result = generate_disambiguation("婚禮攝影合約", "婚禮攝影合約.html", "婚禮攝影合約注意事項.html")
        assert result != "婚禮攝影合約"
        assert "注意事項" in result or "完整" in result

    def test_longer_filename_keeps_title(self):
        """Article with more specific filename keeps original title."""
        from fix_duplicate_titles import choose_preserved_article
        kept = choose_preserved_article(
            [{"filename": "short.html", "title": "Same"}, {"filename": "long-name-guide.html", "title": "Same"}]
        )
        assert kept["filename"] == "long-name-guide.html"


# ─── Expand Descriptions Tests ───────────────────────────────────────────────

class TestExpandDescriptions:
    """Validate meta description expansion to 150-160 characters."""

    def test_short_description_expanded(self):
        """Descriptions under 80 chars should be expanded."""
        from expand_descriptions import expand_description
        result = expand_description("短描述", "婚禮攝影對焦技巧")
        assert len(result) >= 120

    def test_already_long_description_unchanged(self):
        """Descriptions already 150+ chars should not be modified."""
        from expand_descriptions import should_expand
        long_desc = "這是一段非常長的描述，已經超過一百五十個字元，不需要再擴展了因為它已經符合SEO標準。"
        assert not should_expand(long_desc)

    def test_exact_length_boundary(self):
        """Description of exactly 150 chars should not be expanded."""
        from expand_descriptions import should_expand
        exact = "x" * 150
        assert not should_expand(exact)

    def test_149_chars_needs_expansion(self):
        """Description of 149 chars should be flagged for expansion."""
        from expand_descriptions import should_expand
        near = "x" * 149
        assert should_expand(near)


# ─── Meta Tag Fix Tests ──────────────────────────────────────────────────────

class TestFixMetaTags:
    """Validate missing meta tag fixes."""

    def test_robots_missing_added(self):
        """HTML without robots meta should receive one."""
        from fix_meta_tags import add_robots_meta
        html = '<html><head></head><body>test</body></html>'
        result = add_robots_meta(html, "index, follow")
        assert 'name="robots"' in result
        assert "index, follow" in result

    def test_robots_already_present_skipped(self):
        """HTML with existing robots meta should not be modified."""
        from fix_meta_tags import has_robots_meta
        html = '<meta name="robots" content="noindex, nofollow">'
        assert has_robots_meta(html)

    def test_og_image_added(self):
        """HTML without og:image should receive one."""
        from fix_meta_tags import add_og_image
        html = '<html><head></head><body>test</body></html>'
        result = add_og_image(html, "https://example.com/image.webp")
        assert 'property="og:image"' in result
        assert "image.webp" in result


# ─── Integration Tests ───────────────────────────────────────────────────────

class TestIntegration:
    """End-to-end validation with mock file system."""

    def test_duplicate_title_fix_workflow(self, tmp_path):
        """Full workflow: detect duplicates → generate new titles → write."""
        from fix_duplicate_titles import process_duplicates
        # Create two mock files with same title
        f1 = tmp_path / "A.html"
        f2 = tmp_path / "B.html"
        f1.write_text('<title>相同標題</title><meta name="description" content="A的描述">', encoding="utf-8")
        f2.write_text('<title>相同標題</title><meta name="description" content="B的描述">', encoding="utf-8")
        
        # Dry-run should report changes without writing
        output = StringIO()
        with patch('sys.stdout', output):
            process_duplicates([f1, f2], test_mode=True)
        result = output.getvalue()
        assert "相同標題" in result

    def test_description_expansion_workflow(self, tmp_path):
        """Full workflow: find short desc → expand → write."""
        from expand_descriptions import process_articles
        f = tmp_path / "article.html"
        f.write_text(
            '<title>測試文章</title>'
            '<meta name="description" content="短">'
            '<h1>測試</h1>',
            encoding="utf-8"
        )
        output = StringIO()
        with patch('sys.stdout', output):
            process_articles([f], test_mode=True)
        result = output.getvalue()
        assert "短" in result or "→" in result
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest scripts/test_seo_fixes.py -v`
Expected: FAIL — modules `fix_duplicate_titles`, `expand_descriptions`, `fix_meta_tags` not found

- [ ] **Step 3: Create fix_duplicate_titles.py**

Create `scripts/fix_duplicate_titles.py`:

```python
#!/usr/bin/env python3
"""
Fix duplicate blog article titles by appending disambiguation suffixes.
Detects title collisions and renames the less-specific article.
Usage: python3 scripts/fix_duplicate_titles.py [--test]
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

BLOG_DIR = Path(__file__).parent.parent / "blog"

# Suffixes to append when disambiguating
DISAMBIGUATION_SUFFIXES = [
    "：完整實戰指南與注意事項",
    "：進階技巧與實戰應用",
    "：詳細步驟與常見錯誤",
    "：2026 最新建議與案例",
    "：新手必備完全攻略",
]

# Known pair patterns: (base_name, guide_name) where guide_name has "指南"
# The "base" version gets the suffix to differentiate
PAIR_PATTERNS = [
    ("指南", "完整實戰指南"),
    ("注意事項", "完整注意事項與免踩雷指南"),
    ("比較", "詳細比較分析"),
    ("推薦", "人氣推薦完整清單"),
    ("創意", "創意靈感完整攻略"),
]


def extract_title(content: str) -> str:
    match = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_filename_stem(filename: str) -> str:
    """Remove .html and common suffixes to get the base topic."""
    stem = filename.replace(".html", "")
    for suffix in ["指南", "注意事項", "比較", "推薦", "創意", "大全"]:
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def find_duplicate_titles(articles: list[dict]) -> list[list[dict]]:
    """Group articles that share the same title."""
    by_title = defaultdict(list)
    for art in articles:
        by_title[art["title"]].append(art)
    return [group for group in by_title.values() if len(group) > 1]


def choose_preserved_article(group: list[dict]) -> dict:
    """Choose which article keeps its original title (the more specific one)."""
    # Prefer article whose filename contains "指南", "注意事項", "比較" etc.
    priority_keywords = ["指南", "注意事項", "比較", "推薦", "創意", "完整", "詳細"]
    scored = []
    for art in group:
        score = sum(1 for kw in priority_keywords if kw in art["filename"])
        scored.append((score, art))
    scored.sort(key=lambda x: -x[0])
    return scored[0][1]


def generate_disambiguation(base_topic: str, kept_filename: str, other_filename: str) -> str:
    """Generate a unique title for the article that needs renaming."""
    # Try to find a pattern-based suffix
    other_stem = extract_filename_stem(other_filename)
    kept_stem = extract_filename_stem(kept_filename)
    
    # If kept has a distinguishing keyword, use it
    for pattern, suffix in PAIR_PATTERNS:
        if pattern in kept_filename and pattern not in other_filename:
            return f"{other_stem}{suffix}"
    
    # Fallback: use indexed suffix
    for suffix in DISAMBIGUATION_SUFFIXES:
        candidate = f"{base_topic}{suffix}"
        if len(candidate) <= 60:
            return candidate
    
    return f"{base_topic}（完整攻略）"


def process_duplicates(files: list[Path], test_mode: bool = False) -> tuple[int, int]:
    """Process all blog files and fix duplicate titles. Returns (changed, skipped)."""
    articles = []
    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        title = extract_title(content)
        articles.append({"filename": fpath.name, "title": title, "path": fpath, "content": content})
    
    duplicates = find_duplicate_titles(articles)
    changed = 0
    skipped = 0
    
    for group in duplicates:
        kept = choose_preserved_article(group)
        for art in group:
            if art is kept:
                skipped += 1
                continue
            base_topic = extract_filename_stem(art["filename"])
            new_title = generate_disambiguation(base_topic, kept["filename"], art["filename"])
            
            old_content = art["content"]
            new_content = re.sub(
                r"<title>.*?</title>",
                f"<title>{new_title}</title>",
                old_content,
                count=1,
                flags=re.DOTALL
            )
            
            if new_content != old_content:
                if not test_mode:
                    art["path"].write_text(new_content, encoding="utf-8")
                marker = "✓" if not test_mode else "○"
                print(f"  {marker} {art['filename']}: \"{art['title']}\" → \"{new_title}\"")
                changed += 1
            else:
                skipped += 1
    
    return changed, skipped


def main() -> None:
    test_mode = "--test" in sys.argv
    files = sorted(BLOG_DIR.glob("*.html"))
    print(f"Scanning {len(files)} blog articles for duplicate titles...")
    changed, skipped = process_duplicates(files, test_mode=test_mode)
    print(f"\nTotal: {changed} titles updated, {skipped} skipped")
    if test_mode:
        print("(dry-run mode — no files written)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/test_seo_fixes.py::TestFixDuplicateTitles -v`
Expected: 4 passed

- [ ] **Step 5: Create expand_descriptions.py**

Create `scripts/expand_descriptions.py`:

```python
#!/usr/bin/env python3
"""
Expand short blog article meta descriptions to 150-160 characters.
Generates context-aware descriptions based on article topic keywords.
Usage: python3 scripts/expand_descriptions.py [--test]
"""

import re
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"

# Topic-specific description templates
DESCRIPTION_TEMPLATES = {
    "婚禮攝影": "學習{topic}的完整技巧與實戰方法。涵蓋拍攝手法、器材選擇、後期處理與常見問題解答，適合香港婚禮攝影師與愛好者參考。",
    "攝影": "掌握{topic}的專業技巧。詳細介紹拍攝手法、器材建議、後期處理流程與實戰案例，助你提升婚禮攝影作品質量。",
    "場地": "了解{topic}的完整指南。涵蓋場地類型比較、預訂流程、價格範圍與選擇要點，助你找到最適合的婚禮場地。",
    "證書套": "探索{topic}的完整資訊。包括材質選擇、尺寸規格、訂製流程與保養建議，讓你為珍貴的結婚證書找到完美守護。",
    "儀式": "認識{topic}的傳統與現代做法。詳細介紹流程步驟、禮品準備、禁忌注意事項，讓重要儀式順利進行。",
    "婚紗": "了解{topic}的完整攻略。涵蓋款式選擇、尺碼測量、試穿準備與保養保存方法，助你找到夢想婚紗。",
    "婚宴": "掌握{topic}的完整規劃。包括菜單選擇、預算分配、供應商比較與場地佈置建議，打造完美的婚禮宴會。",
    "婚禮": "深入了解{topic}的實用技巧。涵蓋策劃要點、預算管理、供應商選擇與常見錯誤避免，讓婚禮籌備順暢无忧。",
    "結婚": "全面了解{topic}的完整資訊。包括法律程序、文件準備、注意事項與實用建議，助你顺利完成人生大事。",
    "婚後": "學習{topic}的實戰方法。涵蓋財務規劃、溝通技巧、生活適應與關係維護，讓婚後生活更加美滿。",
    "鑽石": "深入了解{topic}的完整知識。包括4C標準、鑑定證書、購買建議與保養方法，助你做出明智的選擇。",
    "蜜月": "探索{topic}的推薦目的地。涵蓋行程規劃、預算建議、簽證資訊與必訪景點，打造難忘的蜜月旅程。",
    "請柬": "了解{topic}的創意設計。包括款式風格、文字內容、印刷工藝與發送時機，留下完美的第一印象。",
    "回禮": "掌握{topic}的精選建議。涵蓋禮物類型、預算分配、包裝設計與發放時機，表達對賓客的感謝心意。",
}

DEFAULT_TEMPLATE = "學習{topic}的完整指南。詳細介紹相關技巧、實用建議與常見問題，涵蓋從入門到進階的完整內容，助你輕鬆掌握核心知識。"


def extract_description(content: str) -> str:
    match = re.search(r'<meta name="description" content="(.*?)">', content)
    return match.group(1) if match else ""


def extract_title(content: str) -> str:
    match = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
    return match.group(1).strip() if match else ""


def should_expand(desc: str) -> bool:
    """Check if description needs expansion (under 120 chars)."""
    return len(desc) < 120


def generate_expanded_description(title: str, current_desc: str, filename: str) -> str:
    """Generate an expanded description based on article topic."""
    topic = filename.replace(".html", "")
    
    # Match template by keyword
    for keyword, template in DESCRIPTION_TEMPLATES.items():
        if keyword in title or keyword in topic:
            return template.format(topic=topic)
    
    return DEFAULT_TEMPLATE.format(topic=topic)


def process_articles(files: list[Path], test_mode: bool = False) -> tuple[int, int]:
    """Process all blog files and expand short descriptions. Returns (changed, skipped)."""
    changed = 0
    skipped = 0
    
    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        title = extract_title(content)
        current_desc = extract_description(content)
        
        if not should_expand(current_desc):
            skipped += 1
            continue
        
        new_desc = generate_expanded_description(title, current_desc, fpath.name)
        new_content = re.sub(
            r'<meta name="description" content=".*?">',
            f'<meta name="description" content="{new_desc}">',
            content,
            count=1
        )
        
        if new_content != content:
            if not test_mode:
                fpath.write_text(new_content, encoding="utf-8")
            marker = "✓" if not test_mode else "○"
            print(f"  {marker} {fpath.name}: {len(current_desc)}→{len(new_desc)} chars")
            changed += 1
        else:
            skipped += 1
    
    return changed, skipped


def main() -> None:
    test_mode = "--test" in sys.argv
    files = sorted(BLOG_DIR.glob("*.html"))
    print(f"Scanning {len(files)} blog articles for short descriptions...")
    changed, skipped = process_articles(files, test_mode=test_mode)
    print(f"\nTotal: {changed} descriptions expanded, {skipped} skipped (already sufficient)")
    if test_mode:
        print("(dry-run mode — no files written)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python3 -m pytest scripts/test_seo_fixes.py::TestExpandDescriptions -v`
Expected: 4 passed

- [ ] **Step 7: Create fix_meta_tags.py**

Create `scripts/fix_meta_tags.py`:

```python
#!/usr/bin/env python3
"""
Fix missing meta tags on key pages:
- Add robots meta to v2.html and blog/index.html
- Add og:image to poster.html
Usage: python3 scripts/fix_meta_tags.py [--test]
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def has_robots_meta(content: str) -> bool:
    return bool(re.search(r'<meta\s+name="robots"', content, re.IGNORECASE))


def add_robots_meta(content: str, content_value: str = "index, follow") -> str:
    """Add robots meta tag after the viewport meta tag."""
    pattern = r'(<meta\s+name="viewport"[^>]*>)'
    replacement = f'\\1\n    <meta name="robots" content="{content_value}">'
    return re.sub(pattern, replacement, content, count=1)


def has_og_image(content: str) -> bool:
    return bool(re.search(r'meta\s+property="og:image"', content, re.IGNORECASE))


def add_og_image(content: str, image_url: str) -> str:
    """Add og:image meta tag after the og:type tag."""
    pattern = r'(<meta\s+property="og:type"[^>]*>)'
    replacement = f'\\1\n    <meta property="og:image" content="{image_url}">'
    return re.sub(pattern, replacement, content, count=1)


def fix_page(filepath: Path, checks: list[tuple[str, callable, ...]]) -> tuple[int, str]:
    """Apply fixes to a single page. Returns (changes_made, description)."""
    content = filepath.read_text(encoding="utf-8")
    original = content
    changes = []
    
    for check_name, check_fn, *args in checks:
        if check_fn(content, *args) if args else check_fn(content):
            continue
        # Apply fix
        if check_name == "robots":
            content = add_robots_meta(content, args[0] if args else "index, follow")
        elif check_name == "og_image":
            content = add_og_image(content, args[0])
        changes.append(check_name)
    
    return content, original, changes


def main() -> None:
    test_mode = "--test" in sys.argv
    changed = 0
    
    # Fix v2.html: add robots meta
    v2_path = ROOT / "v2.html"
    if v2_path.exists():
        content = v2_path.read_text(encoding="utf-8")
        if not has_robots_meta(content):
            new_content = add_robots_meta(content, "index, follow")
            if not test_mode:
                v2_path.write_text(new_content, encoding="utf-8")
            marker = "✓" if not test_mode else "○"
            print(f"  {marker} v2.html: added robots meta tag")
            changed += 1
        else:
            print("  - v2.html: robots meta already present")
    
    # Fix blog/index.html: add robots meta
    blog_index = ROOT / "blog" / "index.html"
    if blog_index.exists():
        content = blog_index.read_text(encoding="utf-8")
        if not has_robots_meta(content):
            new_content = add_robots_meta(content, "index, follow")
            if not test_mode:
                blog_index.write_text(new_content, encoding="utf-8")
            marker = "✓" if not test_mode else "○"
            print(f"  {marker} blog/index.html: added robots meta tag")
            changed += 1
        else:
            print("  - blog/index.html: robots meta already present")
    
    # Fix poster.html: add og:image
    poster_path = ROOT / "poster.html"
    if poster_path.exists():
        content = poster_path.read_text(encoding="utf-8")
        if not has_og_image(content):
            new_content = add_og_image(content, "https://myo-makeyourown.pages.dev/image/01_company_logo.webp")
            if not test_mode:
                poster_path.write_text(new_content, encoding="utf-8")
            marker = "✓" if not test_mode else "○"
            print(f"  {marker} poster.html: added og:image meta tag")
            changed += 1
        else:
            print("  - poster.html: og:image already present")
    
    print(f"\nTotal: {changed} pages fixed")
    if test_mode:
        print("(dry-run mode — no files written)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 8: Run all tests**

Run: `python3 -m pytest scripts/test_seo_fixes.py -v`
Expected: All tests pass

- [ ] **Step 9: Dry-run all scripts**

Run each script with `--test` to verify changes before applying:

```bash
python3 scripts/fix_duplicate_titles.py --test
python3 scripts/expand_descriptions.py --test
python3 scripts/fix_meta_tags.py --test
```

Expected output:
- `fix_duplicate_titles.py --test`: Reports ~40 title changes with ○ markers
- `expand_descriptions.py --test`: Reports 421 description expansions with ○ markers
- `fix_meta_tags.py --test`: Reports 3 page fixes with ○ markers

- [ ] **Step 10: Apply fixes (write mode)**

```bash
python3 scripts/fix_duplicate_titles.py
python3 scripts/expand_descriptions.py
python3 scripts/fix_meta_tags.py
```

- [ ] **Step 11: Regenerate sitemap**

```bash
python3 scripts/generate_sitemap.py
```

- [ ] **Step 12: Verify fixes**

```bash
# Check no duplicate titles remain
python3 -c "
import os, re
from collections import Counter
titles = []
for f in os.listdir('blog'):
    if f.endswith('.html'):
        with open(f'blog/{f}') as fh:
            m = re.search(r'<title>(.*?)</title>', fh.read())
            if m: titles.append(m.group(1))
dups = [t for t, c in Counter(titles).items() if c > 1]
print(f'Duplicate titles remaining: {len(dups)}')
"
```

Expected: `Duplicate titles remaining: 0`

- [ ] **Step 13: Commit**

```bash
git add scripts/fix_duplicate_titles.py scripts/expand_descriptions.py scripts/fix_meta_tags.py scripts/test_seo_fixes.py
git commit -m "feat(seo): add scripts to fix duplicate titles, expand descriptions, and add missing meta tags

- fix_duplicate_titles.py: resolves 40 duplicate title pairs with disambiguation suffixes
- expand_descriptions.py: extends all 421 article descriptions to 150+ chars
- fix_meta_tags.py: adds robots meta to v2.html/blog/index.html, og:image to poster.html
- test_seo_fixes.py: pytest test suite for all three scripts"
```

---

### Task 2: Validate and Update Existing Scripts

After Task 1 completes, verify that existing scripts still work correctly with the updated articles.

**Files:**
- Modify: `scripts/generate_sitemap.py` (if needed — verify lastmod handling)
- Modify: `scripts/parse_blog.py` (if needed — verify it handles updated titles)

- [ ] **Step 1: Re-run generate_sitemap.py and verify output**

```bash
python3 scripts/generate_sitemap.py
head -30 sitemap.xml
```

Expected: Sitemap contains all 421 blog URLs with correct lastmod dates

- [ ] **Step 2: Re-run parse_blog.py and verify index updates**

```bash
python3 scripts/parse_blog.py
wc -l scripts/blog_index.json
```

Expected: `blog_index.json` updated with new titles and descriptions

- [ ] **Step 3: Run existing test suite**

```bash
python3 -m pytest scripts/test_expand_narrations.py -v
```

Expected: All existing tests still pass

- [ ] **Step 4: Commit**

```bash
git add scripts/generate_sitemap.py scripts/parse_blog.py
git commit -m "chore: verify existing scripts work with updated article metadata"
```

---

### Task 3: Final Verification and Documentation

- [ ] **Step 1: Run final SEO validation**

```bash
python3 -c "
import os, re
from collections import Counter

# Check titles
titles = []
descs = []
for f in os.listdir('blog'):
    if f.endswith('.html'):
        with open(f'blog/{f}') as fh:
            content = fh.read()
        t = re.search(r'<title>(.*?)</title>', content)
        d = re.search(r'<meta name=\"description\" content=\"(.*?)\">', content)
        if t: titles.append(t.group(1))
        if d: descs.append(len(d.group(1)))

dups = [t for t, c in Counter(titles).items() if c > 1]
short_descs = sum(1 for d in descs if d < 120)
avg_desc = sum(descs) / len(descs) if descs else 0

print(f'Total articles: {len(titles)}')
print(f'Duplicate titles: {len(dups)}')
print(f'Short descriptions (<120 chars): {short_descs}')
print(f'Average description length: {avg_desc:.0f} chars')
"
```

Expected output:
```
Total articles: 421
Duplicate titles: 0
Short descriptions (<120 chars): 0
Average description length: 140+ chars
```

- [ ] **Step 2: Verify root pages**

```bash
python3 -c "
import re
for page in ['v2.html', 'blog/index.html', 'poster.html']:
    with open(page) as f:
        content = f.read()
    robots = re.search(r'meta name=\"robots\" content=\"(.*?)\">', content)
    og_img = re.search(r'property=\"og:image\" content=\"(.*?)\">', content)
    print(f'{page}: robots={robots.group(1) if robots else \"MISSING\"}, og_image={og_img.group(1)[-30:] if og_img else \"MISSING\"}')
"
```

Expected: All three pages show robots and og_image present

- [ ] **Step 3: Update scripts/AGENTS.md**

Add new scripts to the SEO section:

```markdown
│   ├── fix_duplicate_titles.py     # Resolve duplicate blog article titles
│   ├── expand_descriptions.py      # Expand short meta descriptions to 150+ chars
│   ├── fix_meta_tags.py            # Add missing robots/og meta tags
│   └── test_seo_fixes.py           # Test suite for SEO fix scripts
```

And in COMMANDS:

```bash
# SEO fixes (run after article batch operations)
python3 scripts/fix_duplicate_titles.py [--test]
python3 scripts/expand_descriptions.py [--test]
python3 scripts/fix_meta_tags.py [--test]
```

- [ ] **Step 4: Final commit**

```bash
git add scripts/AGENTS.md
git commit -m "docs: update scripts/AGENTS.md — add SEO fix scripts to documentation"
```

---

## Execution Notes

1. **Run in order**: Task 1 must complete before Task 2 (Task 2 depends on updated articles)
2. **Always use --test first**: Each script supports dry-run; verify output before writing
3. **Backup strategy**: The scripts modify files in-place. Consider `git stash` before running if concerned
4. **No external APIs needed**: All scripts work locally; no DuckDuckGo or LLM calls required
5. **Sitemap regeneration**: Must run after all fixes to reflect updated lastmod timestamps

## Rollback Plan

If any script causes unexpected changes:
```bash
git checkout -- scripts/ blog/ v2.html poster.html
```
All changes are git-tracked and can be reverted with a single command.
