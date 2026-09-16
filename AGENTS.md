# PROJECT KNOWLEDGE BASE — My O! Hong Kong Wedding Site

> **語言偏好**：所有輸出與說明請使用繁體中文（Traditional Chinese）。用戶可用英文回覆，Agent 以繁體中文回應。
>
> **溝通規範**：精準直接，不說客套話；複雜任務拆為 bullet points。

> 倉庫：GitHub Pages 靜態網站 · 純 HTML + Tailwind CSS · 420+ 部落格文章 · 40 個 Vite+React 簡報
> **子目錄 AGENTS.md**（各層級獨立指引，優先讀取）：
> - `presentations/AGENTS.md` — 40 個 Vite+React 簡報項目結構、腳手架、音訊管線
> - `scripts/AGENTS.md` — 34 個自動化腳本（SEO/Schema、效能、Presentation 管線）

---

<!-- anchor: core-commands -->
## 核心指令

```bash
npm run build:css            # Tailwind CSS 生產構建
python3 -m http.server 8000  # 本地預覽

npm test                     # Playwright E2E（Mobile/Desktop/Tablet）
npm run test:mobile          # 僅手機測試
npm run test:headed          # 有頭模式（可視化）

python3 scripts/generate_sitemap.py
python3 scripts/add_org_schema_to_articles.py
python3 scripts/add_breadcrumb_schema.py
python3 scripts/cleanup_json_ld.py
python3 scripts/fix_canonical_urls.py
python3 scripts/fix_blog_titles.py
python3 scripts/optimize_openings.py
python3 scripts/optimize_blog_head.py
python3 scripts/remove_unused_fa.py
python3 scripts/add_pwa_tags.py

bash presentations/_scaffold.sh <NN> <slug> "<標題>" <theme>
# 單個簡報：cd presentations/XX-slug/presentation && npx vite --base "" && npm run build
```

**禁止跳過 dry-run**：多數 Python 腳本支援 `--test`，先跑 dry-run 確認結果再寫入。

---

<!-- anchor: content-structure -->
## 內容結構

| 集合 | 路徑 | 數量 |
|---|---|---|
| 部落格文章 | `blog/*.html` | 421 |
| 首頁版本 | `index.html` / `v2.html` | 2 |
| 政策頁 | `privacy.html` / `terms.html` | 2 |
| 工具頁 | `poster.html` / `heic-converter.html` / `faq.html` | 3 |
| 婚禮簡報 | `presentations/01-*/presentation/` | 40 個 Vite+React 專案 |
| 自動化腳本 | `scripts/*.py` + `generate-presentations/` | ~34 |
| 品牌圖片 | `image/` | 38 |
| 第三方 JS | `js library/` | heic2any / JSZip / FileSaver |

**部落格文章**：421 篇扁平 HTML，無子目錄分類，中文檔名（如 `婚禮攝影對焦技巧.html`）。

**簡報結構**：每項目含 `article.md` + `outline.md` + `script.md` + `presentation/`（Vite+React 專案）。

---

<!-- anchor: file-map -->
## 檔案地圖

| 路徑 | 用途 |
|---|---|
| `blog/*.html` | 421 篇教學文章（JSON-LD + SEO meta 已內嵌） |
| `blog/index.html` | 文章索引頁（搜尋 + 分類篩選） |
| `index.html` / `v2.html` | 兩個首頁版本（原始 / CSS 變量重設計） |
| `sw.js` + `manifest.json` | PWA 服務 worker |
| `css/tailwind.min.css` | 生產 Tailwind CSS（`npm run build:css` 生成） |
| `scripts/blog_index.json` | parse_blog.py 產物（58K 行結構化索引） |
| `docs/top20_articles.json` | rank_articles.py 產物（高流量文章評分） |
| `docs/superpowers/{plans,specs}/` | dated plan/spec 歸檔 |
| `docs/lessons/*.md` | 踩坑教訓歸檔（按需讀取，見下方表格） |

---

<!-- anchor: context-loading -->
## 按需讀取

這些檔案不在會話自動載入範圍內，遇到對應工作類型才讀取：

| 工作類型 | 讀取檔案 | 關鍵 section |
|---|---|---|
| 新增部落格文章 | `blog/婚禮攝影對焦技巧.html` | 現有文章模板對照 |
| 批量 SEO 修復 | `scripts/fix_*.py` | --test 旗標用法 |
| 效能優化 | `scripts/optimize_blog_head.py` | preconnect / preload 格式 |
| Presentation 開發 | `presentations/AGENTS.md` | 完整結構 + 音訊管線 |
| 新增簡報 | `presentations/_scaffold.sh` | 8 種主題配色 |
| TTS 音訊生成 | `presentations/*/presentation/scripts/synthesize-audio.sh` | provider 選擇 |
| 部落格→簡報管線 | `scripts/expand_presentation_content.py` | parse → match → expand → fallback |
| poster.html PDF 列印 | `docs/lessons/poster-print.md` | scale(1.8898) 公式 |
| CLAUDE.md 注意事項 | `CLAUDE.md` | Presentation base path 陷阱 |
| 內容 SOP 標準 | `common/coding-style.md` | KISS / DRY / YAGNI 原則 |

> **原則**：只讀當下任務相關的 section，不要把整個文件塞進 context。

---

<!-- anchor: where-to-look -->
## WHERE TO LOOK

| 任務 | 位置 | 備註 |
|------|------|------|
| 新增部落格文章 | `blog/` | 中文檔名，參考現有文章模板 |
| 修改首頁 | `index.html` / `v2.html` | v2 用 CSS 變量系統 |
| 新增簡報 | `presentations/_scaffold.sh` | 見 presentations/AGENTS.md |
| 運行測試 | `npm test` | 3 裝置（Mobile/Desktop/Tablet） |
| 批量 SEO 修復 | `scripts/` | add_*.py / fix_*.py / optimize_*.py |
| 品牌圖片 | `image/` | Logo、證書套預覽 |
| 第三方 JS | `js library/` | heic2any、JSZip、FileSaver |
| PWA | `sw.js` + `manifest.json` | 根目錄服務 worker |

---

<!-- anchor: conventions -->
## CONVENTIONS

- **文章 SOP**：≥1,500 中文字 + 每 ≤300 字需視覺中斷（表格/清單/H3/提示框）
- **JSON-LD**：每篇文章含 Article/BlogPosting + BreadcrumbList + Organization + FAQPage
- **動態 URL**：canonical、og:url、og:image 全用 JS 動態解析（`window.location.href`）
- **手機版 Sticky Bar**：所有頁面底部固定轉換欄（`add_sticky_bar.py` 批量注入）
- **語言**：`lang="zh-Hant"`，繁體中文內容
- **字型**：Inter（Google Fonts preload+onload）+ Noto Sans TC
- **CSS 框架**：Tailwind CDN → 已改為本地 `css/tailwind.min.css`
- **分享按鈕**：WhatsApp / Facebook / Twitter / 複製連結，URL 動態生成
- **Python 腳本**：多用 `--test`（dry-run）旗標，`replace-tailwind-cdn.py` 需 `--write`

---

<!-- anchor: anti-patterns -->
## ANTI-PATTERNS

- 勿直接修改 `blog/` 文章 — 先用腳本確認，避免批次操作遺漏
- 勿在 `presentations/*/presentation/src/` 硬編碼 base URL — 用 `import.meta.env.BASE_URL`
- 勿將 `node_modules/` 提交 git（`.gitignore` 已設定）
- 勿在 `transition: all` 上使用（不可 GPU 合成）— 改用 `opacity` / `transform`
- 勿在 `.html` 中使用 CDN 載入 Tailwind（已改為本地 CSS）
- 勿在文章模板外硬編碼絕對 URL — 全部動態解析
- 勿跳過 `--test` 直接執行 Python 腳本 — 先確認 dry-run 結果

**非標準注意：**
- `Users/baba/Documents/Github/myo-hk/` — 意外巢狀 repo 副本，應排除
- `.omo/run-continuation/*.json` — session state 已提交 git
- `.gstack/qa-reports/` — 已提交（雖在 .gitignore）
- `dist/`、`test-results/.last-run.json` — build 產物已提交
- `test_file.txt` / `test2.txt` — 根目錄垃圾檔
- `common/agents.md` 小寫 — 與 AGENTS.md 慣例撞名

---

<!-- anchor: self-update -->
## 自我更新協議

AGENTS.md 是活文件——每次會話遇到以下任一情況，更新對應 section 後 commit：

| 觸發條件 | 動作 |
|---|---|
| 新增部落格文章（非批量腳本） | 確認模板一致；如有新 section 結構，更新 CONVENTIONS |
| 新增或修改 Python 腳本 | 更新 scripts/AGENTS.md 分類與 COMMANDS |
| 新增 Presentation 簡報 | 更新 presentations/AGENTS.md STRUCTURE（如有新 hook/component） |
| 發現新的踩坑教訓 | 寫入 `docs/lessons/<topic>.md`，更新按需讀取表 |
| 網站部署行為變更 | 更新核心指令或 NOTES |

**格式**：
```markdown
### {簡短標題}
- **現象**：{錯誤訊息}
- **教訓**：{根本原因}
- **預防**：{下次如何避免}
```

**Commit 規範**：
```bash
git add AGENTS.md
git commit -m "docs: update AGENTS.md — {topic}"
```

---

<!-- anchor: review-commit -->
## 定期 Review Commit

每當完成以下任一事項，執行 Review：

| 觸發條件 | 動作 |
|---|---|
| 新增 10+ 篇部落格文章 | 檢查 JSON-LD 合規 + 分類計數 |
| 新增 Presentation 簡報 | 檢查 `_scaffold.sh` 模板是否完整 |
| 批量腳本修改變更 | 更新 scripts/AGENTS.md 命令參數 |
| 每月定期維護 | 檢查 `docs/lessons/` 是否需要歸檔舊教訓 |

```bash
# 靜態稽核
python3 -m pytest scripts/test_expand_narrations.py -v
npm test

# 審視 diff 後 commit
git diff AGENTS.md presentations/AGENTS.md scripts/AGENTS.md
git commit -m "docs: review AGENTS.md — auto-sync $(date +%Y-%m-%d)"
```
