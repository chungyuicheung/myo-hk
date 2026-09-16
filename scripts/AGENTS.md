# SCRIPTS — 自動化腳本庫

## OVERVIEW
30+ 個 Python 自動化腳本，分為 5 大類別：SEO/Schema、效能優化、Presentation 內容管線、分析追蹤、工具。

## STRUCTURE
```
scripts/
├── SEO / JSON-LD / Schema（13 個）
│   ├── add_org_schema_to_articles.py
│   ├── add_breadcrumb_schema.py
│   ├── add_howto_schema.py
│   ├── enhance_org_schema.py
│   ├── cleanup_json_ld.py
│   ├── consolidate_jsonld.py
│   ├── upgrade_to_blogposting.py
│   ├── fix_canonical_urls.py
│   ├── fix_blog_titles.py
│   ├── fix_duplicate_titles.py
│   ├── expand_descriptions.py
│   ├── fix_meta_tags.py
│   ├── test_seo_fixes.py
│   ├── fix_llms_txt.py
│   ├── generate_sitemap.py
│   ├── rank_articles.py
│   └── optimize_openings.py
│
├── 效能 / Lighthouse（6 個）
│   ├── optimize_blog_head.py
│   ├── remove_unused_fa.py
│   ├── fix_transition_all.py
│   ├── optimize_images.py
│   ├── replace-tailwind-cdn.py
│   └── add_pwa_tags.py
│
├── Presentation 內容管線（8 個）
│   ├── parse_blog.py              # 解析部落格 HTML → blog_index.json
│   ├── match_blog_to_chapter.py   # 部落格章節配對到簡報章節
│   ├── expand_narrations.py       # 生成 narrations.ts（含噪音過濾、廣東話改寫）
│   ├── generate_fallback_narrations.py  # 無比對時生成通用旁白
│   ├── expand_tsx_bullets.py      # 增強 TSX 投影片 bullet 文字
│   ├── search_supplement.py       # DuckDuckGo 搜尋補充薄內容
│   ├── expand_presentation_content.py  # 主控編排器
│   └── test_expand_narrations.py  # pytest 測試套件
│
├── 分析追蹤（2 個）
│   ├── add_social_tracking.py
│   └── add_blog_social_tracking.py
│
├── 其他（1 個）
│   └── migrate_blog_urls.py
│
├── generate-presentations/       # Node.js 批次生成器
│   ├── generate.js
│   ├── data.js                   # 4111 行內容資料
│   └── svgLibrary.js             # SVG 圖示字串庫
│
└── blog_index.json               # parse_blog.py 產物（58K 行）
```

## WHERE TO LOOK
| 任務 | 位置 |
|------|------|
| 批量添加 JSON-LD | `scripts/add_*.py` |
| 修復 SEO 問題 | `scripts/fix_*.py` |
| 生成 sitemap | `scripts/generate_sitemap.py` |
| Presentation 內容生成 | `scripts/expand_presentation_content.py` |
| 效能優化 | `scripts/optimize_*.py`、`scripts/remove_unused_fa.py` |
| 測試腳本品質 | `scripts/test_expand_narrations.py` |

## CONVENTIONS
- **Dry-run 優先**：多數腳本支援 `--test`（不寫入，僅報告）
- **寫入需明確**：`replace-tailwind-cdn.py` 需 `--write`，`optimize_images.py` 需 Pillow
- **pytest 測試**：`python3 -m pytest scripts/test_expand_narrations.py -v [-k filter]`
- **輸入資料**：`docs/top20_articles.json`（rank_articles.py 產物）
- **輸出資料**：`scripts/blog_index.json`（parse_blog.py 產物）

## ANTI-PATTERNS
- 勿直接手動編輯 421 篇文章 — 用腳本批次處理
- 勿跳過 `--test` 直接執行 — 先確認 dry-run 結果
- 勿 commit `blog_index.json` 的臨時版本（58K 行，僅作工具內部使用）

## COMMANDS
```bash
# SEO / Schema
python3 scripts/generate_sitemap.py
python3 scripts/add_org_schema_to_articles.py
python3 scripts/add_breadcrumb_schema.py
python3 scripts/cleanup_json_ld.py
python3 scripts/fix_canonical_urls.py
python3 scripts/fix_blog_titles.py
python3 scripts/fix_duplicate_titles.py
python3 scripts/expand_descriptions.py [--test]
python3 scripts/fix_meta_tags.py [--test]
python3 -m pytest scripts/test_seo_fixes.py -v
python3 scripts/fix_llms_txt.py
python3 scripts/rank_articles.py
python3 scripts/optimize_openings.py

# 效能
python3 scripts/optimize_blog_head.py [--dry-run]
python3 scripts/remove_unused_fa.py [--test]
python3 scripts/fix_transition_all.py
python3 scripts/optimize_images.py
python3 scripts/replace-tailwind-cdn.py --write
python3 scripts/add_pwa_tags.py

# Presentation 內容管線
python3 scripts/parse_blog.py
python3 scripts/expand_presentation_content.py [04|all]
python3 -m pytest scripts/test_expand_narrations.py -v

# 根目錄腳本（未遷入 scripts/）
python3 add_sticky_bar.py
python3 fix_json_ld_and_table.py
python3 fix_medium_issues.py
```

## NOTES
- 根目錄 3 個 Python 腳本（add_sticky_bar.py、fix_json_ld_and_table.py、fix_medium_issues.py）尚未遷入 scripts/
- `optimize_images.py` 需要 Pillow 依賴
- `search_supplement.py` 使用 DuckDuckGo 網頁搜尋（無 API key）
- `expand_presentation_content.py` 編排完整管線：parse → match → expand → fallback → search
- Node.js 生成器（`generate-presentations/`）與 Python 管線互補

## SELF-UPDATE

每次新增或修改腳本，更新此檔結構與 COMMANDS 後 commit：

```bash
git add AGENTS.md
git commit -m "docs: update scripts/AGENTS.md — {script-name}"
```

如腳本涉及新踩坑（如 Puppeteer mock 失效、DuckDuckGo rate limit），寫入 `../docs/lessons/scripts-{topic}.md`。
