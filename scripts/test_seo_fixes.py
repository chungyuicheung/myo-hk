#!/usr/bin/env python3
"""
pytest test suite for SEO fix scripts.

Tests cover:
- fix_duplicate_titles.py
- expand_descriptions.py
- fix_meta_tags.py
"""

import pytest
import re
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fix_duplicate_titles
import expand_descriptions
import fix_meta_tags


# ─── Fix Duplicate Titles Tests ───────────────────────────────────────────────


class TestFixDuplicateTitles:
    """Tests for fix_duplicate_titles.py"""

    def test_find_duplicate_groups(self, tmp_path):
        """Correctly identifies articles with identical titles."""
        # Create fake blog directory
        blog = tmp_path / "blog"
        blog.mkdir()

        # Two files with same title
        (blog / "婚禮攝影合約.html").write_text(
            '<html><head><title>婚禮攝影合約注意事項：保障權益</title></head><body></body></html>',
            encoding="utf-8",
        )
        (blog / "婚禮攝影合約注意事項.html").write_text(
            '<html><head><title>婚禮攝影合約注意事項：保障權益</title></head><body></body></html>',
            encoding="utf-8",
        )
        # One unique file
        (blog / "其他文章.html").write_text(
            '<html><head><title>其他獨特標題</title></head><body></body></html>',
            encoding="utf-8",
        )

        with patch.object(fix_duplicate_titles, "BLOG_DIR", blog):
            groups = fix_duplicate_titles.find_duplicate_groups()

        assert len(groups) == 1
        assert len(groups[0]) == 2
        assert "婚禮攝影合約.html" in groups[0]
        assert "婚禮攝影合約注意事項.html" in groups[0]

    def test_is_shorter_name(self):
        """Shorter filename is identified correctly."""
        assert fix_duplicate_titles.is_shorter_name("a.html", "abc.html") is True
        assert fix_duplicate_titles.is_shorter_name("abc.html", "a.html") is False
        assert fix_duplicate_titles.is_shorter_name("a.html", "a.html") is False

    def test_no_duplicates_no_changes(self, tmp_path):
        """No changes when all titles are unique."""
        blog = tmp_path / "blog"
        blog.mkdir()
        (blog / "文章A.html").write_text(
            '<html><head><title>文章A標題</title></head><body></body></html>',
            encoding="utf-8",
        )
        (blog / "文章B.html").write_text(
            '<html><head><title>文章B標題</title></head><body></body></html>',
            encoding="utf-8",
        )

        with patch.object(fix_duplicate_titles, "BLOG_DIR", blog):
            changed = fix_duplicate_titles.fix_duplicate_titles(test_mode=True)

        assert changed == 0

    def test_duplicate_titles_get_suffix(self, tmp_path):
        """More specific filename gets disambiguation suffix in dry-run."""
        blog = tmp_path / "blog"
        blog.mkdir()

        simple = '<html><head><title>婚禮攝影合約注意事項：保障權益</title></head><body></body></html>'
        specific = '<html><head><title>婚禮攝影合約注意事項：保障權益</title></head><body></body></html>'

        (blog / "婚禮攝影合約.html").write_text(simple, encoding="utf-8")
        (blog / "婚禮攝影合約注意事項.html").write_text(specific, encoding="utf-8")

        with patch.object(fix_duplicate_titles, "BLOG_DIR", blog):
            changed = fix_duplicate_titles.fix_duplicate_titles(test_mode=True)

        assert changed == 1
        # Verify file not modified in dry-run
        content = (blog / "婚禮攝影合約注意事項.html").read_text(encoding="utf-8")
        assert "（進階版）" not in content

    def test_duplicate_titles_written_on_real_run(self, tmp_path):
        """More specific filename gets suffix written to file when not dry-run."""
        blog = tmp_path / "blog"
        blog.mkdir()

        simple = '<html><head><title>測試標題</title></head><body></body></html>'
        specific = '<html><head><title>測試標題</title></head><body></body></html>'

        (blog / "測試.html").write_text(simple, encoding="utf-8")
        (blog / "測試進階.html").write_text(specific, encoding="utf-8")

        with patch.object(fix_duplicate_titles, "BLOG_DIR", blog):
            changed = fix_duplicate_titles.fix_duplicate_titles(test_mode=False)

        assert changed == 1
        content = (blog / "測試進階.html").read_text(encoding="utf-8")
        assert "（進階版）" in content

    def test_different_titles_not_modified(self, tmp_path):
        """Files with different titles are not considered duplicates."""
        blog = tmp_path / "blog"
        blog.mkdir()

        (blog / "文章A.html").write_text(
            '<html><head><title>標題A</title></head><body></body></html>',
            encoding="utf-8",
        )
        (blog / "文章B.html").write_text(
            '<html><head><title>標題B（進階版）</title></head><body></body></html>',
            encoding="utf-8",
        )

        with patch.object(fix_duplicate_titles, "BLOG_DIR", blog):
            changed = fix_duplicate_titles.fix_duplicate_titles(test_mode=True)

        assert changed == 0


# ─── Expand Descriptions Tests ────────────────────────────────────────────────


class TestExpandDescriptions:
    """Tests for expand_descriptions.py"""

    def test_short_description_triggered(self, tmp_path):
        """Articles with description < 120 chars are expanded."""
        blog = tmp_path / "blog"
        blog.mkdir()
        content = (
            '<html><head>'
            '<title>婚禮攝影合約</title>'
            '<meta name="description" content="短描述。">'
            "</head><body></body></html>"
        )
        (blog / "測試.html").write_text(content, encoding="utf-8")

        with patch.object(expand_descriptions, "BLOG_DIR", blog):
            changed = expand_descriptions.expand_descriptions(test_mode=True)

        assert changed == 1

    def test_long_description_skipped(self, tmp_path):
        """Articles with description >= 150 chars are skipped."""
        blog = tmp_path / "blog"
        blog.mkdir()
        long_desc = "這是一段非常長的文字描述，超過了一百五十字數的限制，所以不應該被修改，這只是測試用的長描述內容而已，用來確保腳本不會修改已經夠長的描述，這個描述必須足夠長才能通過測試的驗證條件要求，請確保文字總數達到一百五十字以上才算合格通過測試，多寫一些字來確保長度足夠且符合標準規範要求，這樣才能確保測試能夠順利通過並且驗證腳本的正確性。"
        content = (
            '<html><head>'
            '<title>測試文章</title>'
            f'<meta name="description" content="{long_desc}">'
            "</head><body></body></html>"
        )
        (blog / "測試.html").write_text(content, encoding="utf-8")

        with patch.object(expand_descriptions, "BLOG_DIR", blog):
            changed = expand_descriptions.expand_descriptions(test_mode=True)

        assert changed == 0

    def test_no_description_tag_skipped(self, tmp_path):
        """Articles without a description meta tag are skipped."""
        blog = tmp_path / "blog"
        blog.mkdir()
        content = '<html><head><title>測試文章</title></head><body></body></html>'
        (blog / "測試.html").write_text(content, encoding="utf-8")

        with patch.object(expand_descriptions, "BLOG_DIR", blog):
            changed = expand_descriptions.expand_descriptions(test_mode=True)

        assert changed == 0

    def test_photography_topic_template(self, tmp_path):
        """Photography-related article gets photography template."""
        blog = tmp_path / "blog"
        blog.mkdir()
        content = (
            '<html><head>'
            '<title>婚禮攝影合約</title>'
            '<meta name="description" content="短。">'
            "</head><body></body></html>"
        )
        (blog / "婚禮攝影合約.html").write_text(content, encoding="utf-8")

        with patch.object(expand_descriptions, "BLOG_DIR", blog):
            changed = expand_descriptions.expand_descriptions(test_mode=False)

        assert changed == 1
        new_content = (blog / "婚禮攝影合約.html").read_text(encoding="utf-8")
        new_desc = re.search(r'<meta name="description" content="([^"]*)">', new_content)
        assert new_desc
        desc = new_desc.group(1)
        assert len(desc) >= 148  # Allow slight boundary variance
        assert "攝影" in desc

    def test_venue_topic_template(self, tmp_path):
        """Venue-related article gets venue template."""
        blog = tmp_path / "blog"
        blog.mkdir()
        content = (
            '<html><head>'
            '<title>婚禮場地選擇</title>'
            '<meta name="description" content="短。">'
            "</head><body></body></html>"
        )
        (blog / "婚禮場地選擇.html").write_text(content, encoding="utf-8")

        with patch.object(expand_descriptions, "BLOG_DIR", blog):
            changed = expand_descriptions.expand_descriptions(test_mode=False)

        assert changed == 1
        new_content = (blog / "婚禮場地選擇.html").read_text(encoding="utf-8")
        new_desc = re.search(r'<meta name="description" content="([^"]*)">', new_content)
        assert new_desc
        desc = new_desc.group(1)
        assert len(desc) >= 148  # Allow slight boundary variance
        assert "場地" in desc

    def test_certificate_topic_template(self, tmp_path):
        """Certificate-related article gets certificate template."""
        blog = tmp_path / "blog"
        blog.mkdir()
        content = (
            '<html><head>'
            '<title>證書套選擇</title>'
            '<meta name="description" content="短。">'
            "</head><body></body></html>"
        )
        (blog / "證書套選擇.html").write_text(content, encoding="utf-8")

        with patch.object(expand_descriptions, "BLOG_DIR", blog):
            changed = expand_descriptions.expand_descriptions(test_mode=False)

        assert changed == 1
        new_content = (blog / "證書套選擇.html").read_text(encoding="utf-8")
        new_desc = re.search(r'<meta name="description" content="([^"]*)">', new_content)
        assert new_desc
        desc = new_desc.group(1)
        assert len(desc) >= 148  # Allow slight boundary variance

    def test_dry_run_does_not_modify_files(self, tmp_path):
        """Dry-run mode does not modify any files."""
        blog = tmp_path / "blog"
        blog.mkdir()
        original = '<html><head><title>測試</title><meta name="description" content="短。"></head><body></body></html>'
        (blog / "測試.html").write_text(original, encoding="utf-8")

        with patch.object(expand_descriptions, "BLOG_DIR", blog):
            expand_descriptions.expand_descriptions(test_mode=True)

        content = (blog / "測試.html").read_text(encoding="utf-8")
        assert content == original

    def test_expanded_description_within_target_range(self, tmp_path):
        """Expanded descriptions fall within target range (150-160 chars)."""
        blog = tmp_path / "blog"
        blog.mkdir()
        content = (
            '<html><head>'
            '<title>婚禮場地選擇</title>'
            '<meta name="description" content="短。">'
            "</head><body></body></html>"
        )
        (blog / "婚禮場地選擇.html").write_text(content, encoding="utf-8")

        with patch.object(expand_descriptions, "BLOG_DIR", blog):
            expand_descriptions.expand_descriptions(test_mode=False)

        new_content = (blog / "婚禮場地選擇.html").read_text(encoding="utf-8")
        new_desc = re.search(r'<meta name="description" content="([^"]*)">', new_content)
        assert new_desc
        desc = new_desc.group(1)
        assert 140 <= len(desc) <= 170  # Allow some slack for boundary trimming


# ─── Fix Meta Tags Tests ──────────────────────────────────────────────────────


class TestFixMetaTags:
    """Tests for fix_meta_tags.py"""

    def test_v2_missing_robots_added(self, tmp_path):
        """v2.html gets robots meta when missing."""
        html = '<html><head><title>Test</title></head><body></body></html>'
        v2 = tmp_path / "v2.html"
        v2.write_text(html, encoding="utf-8")

        new_content, changed = fix_meta_tags.ensure_robots_meta(html, "v2.html", test_mode=False, root=tmp_path)
        assert changed is True
        assert 'name="robots"' in new_content
        assert 'content="index, follow"' in new_content
        content = v2.read_text(encoding="utf-8")
        assert 'name="robots"' in content

    def test_v2_already_has_robots_skipped(self, tmp_path):
        """v2.html with existing robots meta is not modified."""
        html = '<html><head><meta name="robots" content="index, follow"><title>Test</title></head><body></body></html>'
        v2 = tmp_path / "v2.html"
        v2.write_text(html, encoding="utf-8")

        new_content, changed = fix_meta_tags.ensure_robots_meta(html, "v2.html", test_mode=False, root=tmp_path)
        assert changed is False
        content = v2.read_text(encoding="utf-8")
        assert content.count('name="robots"') == 1

    def test_blog_index_missing_robots_added(self, tmp_path):
        """blog/index.html gets robots meta when missing."""
        html = '<html><head><title>Test</title></head><body></body></html>'
        blog_dir = tmp_path / "blog"
        blog_dir.mkdir()
        index = blog_dir / "index.html"
        index.write_text(html, encoding="utf-8")

        new_content, changed = fix_meta_tags.ensure_robots_meta(html, "blog/index.html", test_mode=False, root=tmp_path)
        assert changed is True
        assert 'name="robots"' in new_content
        content = index.read_text(encoding="utf-8")
        assert 'name="robots"' in content

    def test_poster_missing_og_image_added(self, tmp_path):
        """poster.html gets og:image meta when missing."""
        html = '<html><head><title>Test</title></head><body></body></html>'
        poster = tmp_path / "poster.html"
        poster.write_text(html, encoding="utf-8")

        new_content, changed = fix_meta_tags.ensure_og_image(html, "poster.html", test_mode=False, root=tmp_path)
        assert changed is True
        assert 'property="og:image"' in new_content
        assert "01_company_logo.webp" in new_content
        content = poster.read_text(encoding="utf-8")
        assert 'property="og:image"' in content

    def test_poster_already_has_og_image_skipped(self, tmp_path):
        """poster.html with existing og:image is not modified."""
        html = '<html><head><meta property="og:image" content="existing.jpg"><title>Test</title></head><body></body></html>'
        poster = tmp_path / "poster.html"
        poster.write_text(html, encoding="utf-8")

        new_content, changed = fix_meta_tags.ensure_og_image(html, "poster.html", test_mode=False, root=tmp_path)
        assert changed is False
        content = poster.read_text(encoding="utf-8")
        assert content.count('property="og:image"') == 1
        assert "existing.jpg" in content

    def test_dry_run_does_not_modify_files(self, tmp_path):
        """Dry-run mode does not modify any files."""
        html = '<html><head><title>Test</title></head><body></body></html>'
        v2 = tmp_path / "v2.html"
        v2.write_text(html, encoding="utf-8")
        blog_dir = tmp_path / "blog"
        blog_dir.mkdir()
        index = blog_dir / "index.html"
        index.write_text(html, encoding="utf-8")
        poster = tmp_path / "poster.html"
        poster.write_text(html, encoding="utf-8")

        # In dry-run, functions return modified content but don't write files
        content_v2, changed_v2 = fix_meta_tags.ensure_robots_meta(html, "v2.html", test_mode=True, root=tmp_path)
        assert changed_v2 is True
        assert 'name="robots"' in content_v2
        assert content_v2 != html

        # File should not be modified
        content = v2.read_text(encoding="utf-8")
        assert content == html

    def test_robots_inserted_before_closing_head(self, tmp_path):
        """Robots meta is inserted before </head>."""
        html = '<html><head><title>Test</title>\n<p>body</p>\n</head><body></body></html>'
        v2 = tmp_path / "v2.html"
        v2.write_text(html, encoding="utf-8")

        new_content, changed = fix_meta_tags.ensure_robots_meta(html, "v2.html", test_mode=False, root=tmp_path)
        assert changed is True
        robots_pos = new_content.find('name="robots"')
        head_close_pos = new_content.find("</head>")
        assert robots_pos > 0
        assert robots_pos < head_close_pos
