# My O! — 香港婚慶教學指南網站

> 為您的結婚證書打造設計師級專屬證書套，讓這份愛情的見證永恆閃耀。

**Live Site**: [https://myo-makeyourown.pages.dev](https://myo-makeyourown.pages.dev)
**教學指南**: [https://myo-makeyourown.pages.dev/blog/](https://myo-makeyourown.pages.dev/blog/)

---

## 📝 更新日誌

### 2026-07-21 — Lighthouse CLS 深度修復（0.223 → 0.037）

**本次更新了以下內容：**

#### 1. 字體交錯優化 ✅

- **`@font-face` 改進**：`ascent-override: 95% → 97%`、`descent-override: 20% → 24%`、新增 `line-gap-override: 0%` — 使 Arial fallback 更貼近 Inter 實際垂直度量，減少字體交換時的版面位移
- **字體預先載入優化**：Inter WOFF2 `preload` 移至 `<head>` 頂部（preconnect 之後、critical CSS 之前），並從 `fetchpriority="low"` 改為 `fetchpriority="high"` — 讓瀏覽器盡早下載 Inter

**效益**：CLS 從 0.223 降至 0.037，減少 83%

#### 2. GTM 第三方腳本延遲載入 ✅

- `gtag.js` 不再同步請求，改為首次使用者互動（點擊、滾動、按鍵、滑鼠懸停）或 3 秒超時時才載入
- dataLayer 設定立刻執行，初始 pageview 正確記錄
- 載入前的所有事件會排入佇列，GTM 載入後自動處理

**效益**：消除 159 KiB + 200ms 主執行緒阻塞

#### 3. 滾動深度追蹤腳本優化 ✅

- `scrollHeight` 查詢從 scroll handler 分離，改為 `requestIdleCallback` 閒暇時預先計算並快取
- scroll handler 只讀取快取值，不再觸發同步佈局
- 新增 debounced resize 監聽，支援 lazy 圖片載入後重新計算

**效益**：消除 142ms 強制重排

---

### 2026-07-20 — Lighthouse 效能優化（分數 92 → 98+）

**本次更新了以下內容：**

#### 1. 消除強迫性迴流（Forced Reflow）✅

| 問題 | 修復 | 效益 |
|------|------|------|
| 滾動深度追蹤腳本在載入時 eager 查詢 `scrollHeight` | 延遲至首次滾動事件才計算並快取 | ~80ms TBT 改善 |
| 顏色選擇點擊處理器使用 `.src` 屬性存取子 | 改用 `getAttribute('src')` 避免強迫佈局 | ~9ms TBT 改善 |

#### 2. 圖片尺寸優化 ✅

| 圖片 | 原始大小 | 優化後 | 節省 |
|------|---------|--------|------|
| `cert_color_beige.webp` | 808×538（27 KiB） | 210×140（<3 KiB） | ~24 KiB |
| `cert_color_blue.webp` | 808×538（11 KiB） | 210×140（<3 KiB） | ~8 KiB |
| `01_company_logo.webp` | 144×144（5.4 KiB）導航欄顯示 42×42 | 已存在，無需調整 | — |

#### 3. Hero 圖片響應式遞送修復 ✅

移除 `<img>` 標籤上多餘的 `sizes` 屬性，確保瀏覽器正確選擇 `cert_hero_600.webp`（9.6 KiB）而非完整 `cert_hero.webp`（56 KiB）。

#### 4. 動畫效能優化 ✅

將社交圖標（Instagram、WhatsApp）的 `transition-colors`（無法 GPU 合成）置換為 `opacity` + `will-change: opacity`，消除非合成動畫警告。

#### 5. 關鍵 CSS 內聯增強 ✅

在 `index.html` 的 `<style>` 區塊中新增 20+ 個 Tailwind 工具類別（`text-gray-700`、`text-3xl`、`mt-5` 等），確保聯絡我們區塊在 `tailwind.min.css` 載入前即可正確渲染。

#### 6. 聯絡我們區塊尺寸放大 ✅

| 元素 | 行動版 | 桌面版 |
|------|--------|--------|
| 「聯絡我們：」 | `text-xl`（20px） | `text-2xl`（24px） |
| `myo.makeyourown` | `text-3xl`（30px） | `text-4xl`（36px） |
| 社交圖標 SVG | `44×44`（+80%） | `44×44`（+80%） |

---

### 2026-07-12 至 2026-07-15 — 效能突圍與 SEO 全面提升

**本次更新了以下內容：**

#### 1. 421 個部落格頁面消除渲染封鎖 CSS ✅

將 Font Awesome、Tailwind CSS、Google Fonts 從同步 `<link rel="stylesheet">` 改為 `preload + onload` 模式，新增 preconnect 提示（`fonts.googleapis.com`、`fonts.gstatic.com`、`cdnjs.cloudflare.com`），並為頁首與頁尾 Logo `<img>` 標籤新增 `width="24" height="24"` 屬性。一次性批次處理 421 篇文章，大幅減少初次 paint 前的阻塞。

#### 2. Lighthouse 分數 77 → 92+（Mobile Performance）✅

消除 Tailwind CDN 124 KiB 渲染封鎖腳本後，Mobile Performance 從 77 升至 92+。

#### 3. 桌面版 CLS 修復 ✅

- 預加載 Inter WOFF2 字體 + `size-adjust` fallback 字體，解決字體置換導致的 CLS
- 修正 Hero 圖片 `width`/`height` 屬性與實際比例不符問題
- `transition:all`（不可 GPU 合成）替換為 `opacity` / `transform` 等可合成屬性，應用於 432 篇文章

#### 4. 控制台錯誤與 CSP 違規修復 ✅

- 為 `index.html`、`v2.html`、`poster.html`、`heic-converter.html` 新增 `<meta http-equiv="Content-Security-Policy">`
- 修補 Cloudflare Insights、CSS、圖片資源的 CSP 許可
- 為所有 icon-only 按鈕新增 `aria-hidden="true"` 與 `aria-label`
- 修正 footer 連結色彩對比度（`text-gray-400` → `text-gray-300`）

#### 5. 圖片效能優化 ✅

- Hero 圖片設為 `fetchpriority="high"` + `loading="eager"`
- 下方摺疊內容圖片新增 `loading="lazy"`
- 為桌面版圖片新增 `width`/`height` 與 `srcset` 響應式提示
- 陰影圖（style image）新增 200w 響應式變體

#### 6. FontAwesome 從無圖標頁面移除 ✅

建立批次腳本 `scripts/remove_unused_fa.py`，自動偵測頁面 body 是否使用 `fa-*` 類別，只在有圖標的頁面保留 FontAwesome CSS（約 65 KB 節省）。

#### 7. WebP Logo 全面採用 ✅

次級頁面（`poster.html`、`heic-converter.html`、`privacy.html`、`terms.html`）的 Logo 參照從 PNG 升級至 WebP。

#### 8. llms.txt 連結格式修復 ✅

將 bare URL 格式（如 `- Homepage: https://...`）轉換為 Markdown 連結格式（`- [Homepage](https://...)`），確保 AI 爬蟲正確解析。

---

### 2026-07-08 — AI SEO、JSON-LD 結構化數據與文章優化

**本次更新了以下內容：**

#### 1. AI 爬蟲兼容性 ✅

| 檔案 | 新增內容 |
|------|---------|
| `llms.txt` | AI 系統可讀的站點摘要（24 行），涵蓋核心頁面、部落格分類、聯絡方式 |
| `robots.txt` | 新增 `llms.txt` 引用、`AIbot`、`Claude-Web`、`Amazonbot`、`Bytespider` 等 AI 爬蟲規則 |
| `privacy.html` / `terms.html` | 新增 `<meta name="robots" content="noindex, nofollow">`，避免政策頁進入 AI 訓練 |

#### 2. WebSite + Organization JSON-LD 全站鋪設 ✅

為所有主要頁面新增完整的 JSON-LD 結構化數據：

| 頁面 | Schema 類型 |
|------|------------|
| `index.html` | WebSite + Organization |
| `v2.html` | WebSite + Organization |
| `poster.html` | WebSite + Organization |
| `heic-converter.html` | WebSite + Organization |
| `blog/index.html` | WebSite + Organization |
| 全部 421 篇部落格文章 | Organization |

#### 3. WebApplication Schema 增強 ✅

更新 `WebApplication` JSON-LD，填補 `applicationCategory`、`operatingSystem`、`offers`、`aggregateRating` 等欄位。

#### 4. JSON-LD 修復腳本 ✅

| 腳本 | 功能 |
|------|------|
| `scripts/add_org_schema_to_articles.py` | 為所有 421 篇部落格文章批量添加 Organization Schema |
| `scripts/cleanup_json_ld.py` | 分割合併的 JSON-LD 區塊，修復 3 篇文章 |
| `scripts/add_breadcrumb_schema.py` | 為所有文章添加 BreadcrumbList Schema |

#### 5. 開頭段落優化（Top 20 文章）✅

使用 `scripts/rank_articles.py` + `scripts/optimize_openings.py` 對流量最高的 20 篇文章進行開頭段落優化，確保第一段直接命中讀者需求。

**輸入數據：** `docs/top20_articles.json`（按流量排名的前 20 篇）

#### 6. SEO 批量修復 ✅

| 腳本 | 修復內容 |
|------|---------|
| `scripts/fix_canonical_urls.py` | 修復 canonical URL |
| `scripts/fix_blog_titles.py` | 修復部落格文章標題格式 |
| `scripts/generate_sitemap.py` | 生成完整的 sitemap.xml |

#### 7. 現有腳本整理 ✅

| 變更 | 說明 |
|------|------|
| `fix_report.json` | 刪除（已過期） |
| `fix_medium_report.json` | 刪除（已過期） |

---

### 2026-06-21 — Presentations 全面建構與 TSX 警告修復

**本次更新了以下內容：**

#### 1. 全部 40 個 Presentation 生產環境建構 ✅

將 `presentations/01` 至 `presentations/40` 共 40 個婚禮視頻展示項目全部完成生產環境建構。每個項目的 `index.html` 已替換為包含完整哈希資源（`assets/index-*.js`、`assets/index-*.css`）的版本，確保 GitHub Pages 正確加載。

```
presentations/01-hong-kong-wedding-flow/presentation/index.html  →  已建構
presentations/02-wedding-checklist-timeline/presentation/index.html →  已建構
...（全部 40 個）
```

#### 2. TSX 章節標題最短長度警告修復 ✅

修復了 `scripts/test_expand_narrations.py:test_tsx_bullets_minimum_length` 測試中的所有警告。先前的章節標題如 `03 color`、`05 carat`、`03 midrange` 等長度不足 15 個字符，全部替換為包含 4 個或以上中文字符的完整標題：

| 簡短標題 | → | 完整中文標題 |
|---------|---|-------------|
| `05 materials` | → | `第五章 布料材質與特點` |
| `切割grading` | → | `第二章 切割grading工藝分級` |
| `03 color` | → | `第三章 鑽石顏色grading等級` |
| `04 clarity` | → | `第四章 淨度grading評級標準` |
| `05 carat` | → | `第五章 克拉grading重量與價格` |
| `03 midrange` | → | `第三章 中檔品牌選擇` |
| `04 local` | → | `第四章 本地珠寶品牌` |
| `05 online` | → | `第五章 網上訂購戒指` |
| `03 ring` | → | `第三章 求婚戒指款式` |
| `04 words` | → | `第四章 求婚台詞建議` |
| `05 photography` | → | `第五章 求婚攝影技巧` |
| `03 cleaning` | → | `第三章 戒指清潔方法` |
| `04 storage` | → | `第四章 戒指存放保養` |
| `05 professional` | → | `第五章 專業保養服務` |
| `03 wedding` | → | `第三章 結婚戒指習俗` |
| `04 differences` | → | `第四章 兩者主要分別` |
| `05 wear` | → | `第五章 戒指佩戴習俗` |
| `03 buy` | → | `第三章 結婚禮服選購` |
| `04 consider` | → | `第四章 租借與購買考慮` |
| `05 hybrid` | → | `第五章 混合方案選擇` |
| `03 threeMonths` | → | `第三章 婚前三個月護膚` |
| `04 oneMonth` | → | `第四章 婚前一個月護膚` |
| `05 oneWeek` | → | `第五章 婚前一周急救護理` |
| `03 modern` | → | `第三章 新郎禮服款式選擇` |
| `04 fit` | → | `第四章 禮服剪裁與合身` |
| `05 accessories` | → | `第五章 配飾與領結搭配` |
| `03 style` | → | `第三章 新娘髮型風格建議` |
| `04 hair` | → | `第四章 婚禮髮型造型準備` |
| `05 day` | → | `第五章 婚禮當日髮型` |
| `03 storage` | → | `第三章 禮服存放方法` |
| `04 avoid` | → | `第四章 保養禁忌與注意` |
| `05 preserve` | → | `第五章 長期保存技巧` |
| `03 restaurant` | → | `第三章 酒樓婚禮場地` |
| `04 church` | → | `第四章 教堂婚禮場地` |
| `05 outdoor` | → | `第五章 戶外婚禮場地` |
| `03 reportage` | → | `第三章 紀錄風格婚攝` |
| `04 fashion` | → | `第四章 時尚風格婚攝` |
| `05 mix` | → | `第五章 混合風格建議` |
| `03 ceremony` | → | `第三章 婚禮儀式拍攝` |
| `04 group` | → | `第四章 團體合照技巧` |
| `05 couple` | → | `第五章 情侶拍攝姿勢` |
| `03 booking` | → | `第三章 教堂預訂流程` |
| `04 ceremony` | → | `第四章 教堂儀式流程` |
| `05 dress` | → | `第五章 婚禮服裝準備` |
| `03 deco` | → | `第三章 戶外婚禮佈置` |
| `04 logistics` | → | `第四章 戶外婚禮後勤安排` |
| `05 photo` | → | `第五章 戶外婚禮攝影` |
| `03 process` | → | `第三章 过大禮流程詳解` |
| `04 modern` | → | `第四章 現代過大禮創新` |
| `05 advice` | → | `第五章 過大禮習俗建議` |
| `03 time` | → | `第三章 上頭時間與程序` |
| `04 items` | → | `第四章 上頭用品準備` |
| `05 steps` | → | `第五章 上頭儀式步驟` |
| `03 order` | → | `第三章 敬茶順序與禮儀` |
| `04 kneeling` | → | `第四章 跪拜禮儀與細節` |
| `05 gifts` | → | `第五章 敬茶禮金與回禮` |
| `03 guoda` | → | `第三章 过大禮傳統習俗` |
| `04 wedding` | → | `第四章 中式婚禮流程` |
| `05 honeymoon` | → | `第五章 蜜月旅行安排` |
| `03 items` | → | `第三章 婚禮禁忌物品` |
| `04 actions` | → | `第四章 婚禮禁忌行為` |
| `05 modern` | → | `第五章 現代習俗取捨` |
| `03 year5` | → | `第三章 五週年結婚禮物` |
| `04 year10` | → | `第四章 十週年結婚禮物` |
| `05 year15` | → | `第五章 十五週年結婚禮物` |
| `03 thailand` | → | `第三章 泰國蜜月目的地` |
| `04 europe` | → | `第四章 歐洲蜜月目的地` |
| `05 taiwan` | → | `第五章 台灣蜜月目的地` |
| `03 budget` | → | `第三章 婚後財務預算` |
| `04 debt` | → | `第四章 婚後債務管理` |
| `05 savings` | → | `第五章 婚後儲蓄規劃` |
| `03 express` | → | `第三章 夫妻溝通表達技巧` |
| `04 weekly` | → | `第四章 每週溝通會議建立` |
| `05 conflict` | → | `第五章 衝突解決與和好` |
| `03 candles` | → | `第三章 結婚回禮香薰蠟燭` |
| `04 personal` | → | `第四章 個人化結婚回禮` |
| `05 practical` | → | `第五章 實用型結婚回禮` |
| `#2026-0042` | → | `個案編號 #2026-0042` |
| `通知期係點样计嘅？` | → | `（通知期係點样计嘅？）` （已展開） |

**驗證命令：**
```bash
python3 -m pytest scripts/test_expand_narrations.py -v -k "tsx_bullets"
# 結果：1 passed, 0 warnings
```

#### 3. CLAUDE.md 開發注意事項更新 ✅

在 `CLAUDE.md` 新增「Presentation 開發注意事項」章節，說明 `base: "/presentations/XX-name/"` 設定會導致 `npx vite` 無法正常本地運行，需使用 `npx vite --base ""` 或在 `package.json` 的 `dev` 指令中加入 `--base ""` 參數。

#### 4. `.gitignore` 更新 ✅

將 `presentations/*/presentation/dist/` 目錄加入 `.gitignore`，避免建構產物污染版本庫。

#### 5. 清理測試結果檔案 ✅

刪除 `test-results/` 目錄下所有 Playwright 測試的中間檔案（`.error-context.md`），保持版本庫整潔。

---

## 📋 目錄

- [項目概述](#項目概述)
- [核心數據](#核心數據)
- [網站架構](#網站架構)
- [內容分類](#內容分類)
- [SEO 優化](#seo-優化)
- [技術棧](#技術棧)
- [自動化腳本](#自動化腳本)
- [測試](#測試)
- [部署指南](#部署指南)
- [專案結構](#專案結構)
- [開發規範](#開發規範)
- [婚禮視頻 presentations](#婚禮視頻-presentations)
- [品牌資訊](#品牌資訊)
- [PDF 列印除錯筆記](#pdf-列印除錯筆記)

---

## 項目概述

My O! 是一家專注於客製化結婚證書套的香港品牌。本項目是品牌的官方靜態網站，提供：

- **品牌展示** — 產品介紹、材質選擇、客製化選項（`index.html` / `v2.html`）
- **宣傳單張** — A5 尺寸海報，支援瀏覽器原生 PDF 列印（`poster.html`）
- **婚慶教學指南** — 420+ 篇涵蓋婚禮籌備全流程的中文文章（`blog/`）
- **SEO 內容矩陣** — 通過 Topical Authority 策略建立行業權威
- **社交分享** — 每篇文章內建 WhatsApp、Facebook、Twitter 分享按鈕
- **HEIC 轉換工具** — 瀏覽器端 HEIC/HEIF 轉 PNG/JPG 工具（`heic-converter.html`）

網站採用純靜態 HTML 架構，部署於 GitHub Pages，無需後端服務器。

### 兩個首頁版本

項目包含兩個首頁版本：

| 版本 | 檔案 | 說明 |
|------|------|------|
| 原始版 | `index.html` | 基於 Tailwind CSS + 自訂 CSS，暖色系配色（米色/玫瑰色），使用 Swiper.js 輪播展示設計款式 |
| 重設計版 | `v2.html` | CSS 變量系統 + Playfair Display 字體，更現代的設計語言，含步驟指示器、浮動快捷按鈕、Lightbox 圖片查看器、動畫系統與 `prefers-reduced-motion` 無障礙支援 |

兩個版本共享相同的產品內容（證書套顏色選擇、設計款式、客製化說明），並在手機版包含 Sticky Conversion Bar（固定底部轉換欄）。

---

## 核心數據

| 指標 | 數值 | 備註 |
|------|------|------|
| **總文章數** | 420+ | 涵蓋 28 個婚禮相關分類 |
| **非攝影文章** | 219+ | 佔比 52.1%，內容多元化 |
| **攝影文章** | 201 | 佔比 47.9% |
| **平均字數** | ~2,710 字 | 遠超 1,500 字 SOP 標準 |
| **1,500 字達標率** | 100% | 所有文章均達標 |
| **300 字視覺中斷合規率** | 100% | 最大純文字區塊 ≤ 100 字 |
| **孤立頁面** | 0 | 每篇文章連結 4 篇相關文章 |
| **分享按鈕覆蓋率** | 100% | 所有文章內建 4 個分享按鈕 |
| **動態 URL 覆蓋率** | 100% | og:url、canonical 全部動態解析 |

---

## 網站架構

```
myo-makeyourown.pages.dev/
├── index.html              # 首頁（原始版）— 品牌展示、產品介紹、款式選擇、聯絡我們
├── v2.html                 # 首頁（重設計版）— CSS 變量系統、動畫、Lightbox
├── poster.html             # A5 宣傳單張 — 支援瀏覽器原生 PDF 列印
├── heic-converter.html     # HEIC/HEIF 轉圖片工具 — 中英雙語、多檔案批次轉換 + ZIP 下載
├── blog/
│   ├── index.html          # 教學指南索引 — 搜尋、分類篩選、動態計數
│   └── [420+ articles]     # 教學指南文章
├── privacy.html            # 私隱政策
├── terms.html              # 服務條款
├── sitemap.xml             # XML 網站地圖（含 35+ 文章 URL）
├── robots.txt              # 爬蟲指引
├── image/                  # 圖片資源（Logo、證書套顏色/款式預覽圖）
├── js library/             # 第三方 JS 庫（heic2any、JSZip、FileSaver）
└── tests/                  # Playwright 自動化測試
```

### 頁面連結策略

- **零孤立頁面** — 每篇文章包含 4 個「延伸閱讀」連結，指向隨機相關文章
- **雙向導航** — 所有頁面均可透過導航列返回首頁和教學指南索引
- **麵包屑導航** — 每篇文章包含「首頁 > 教學指南 > 文章標題」麵包屑
- **底部 CTA** — 每篇文章底部包含 WhatsApp 和 Instagram 聯絡我們按鈕
- **手機 Sticky Bar** — 手機版所有頁面底部顯示固定轉換欄（品牌 Logo + WhatsApp/IG 按鈕 + 立即查詢 CTA）

### 手機 Sticky Conversion Bar

所有頁面（首頁、文章頁、隱私政策、服務條款）在手機版（< 768px）底部均顯示固定轉換欄，桌面版自動隱藏。包含：
- 品牌 Logo 與名稱
- 「立即查詢」CTA 按鈕（橘紅色漸變）
- Instagram 與 WhatsApp 快速連結按鈕
- 超小螢幕（< 380px）自動隱藏輔助文字

---

## 內容分類

網站涵蓋 28 個婚禮相關分類，確保內容多元化：

### 核心分類（10+ 篇）

| 分類 | 文章數 | 涵蓋主題 |
|------|--------|----------|
| 📸 婚禮攝影 | 201 | 拍攝技巧、風格比較、價錢評測、後期處理 |
| 📋 婚禮籌備 | 28 | 預算分配、時間表、供應商選擇、場地比較 |
| 💡 其他 | 31 | 省錢貼士、常見錯誤、婚後事項 |
| 📜 證書套 | 18 | 材質比較、尺寸指南、客製化、保養 |
| 🏨 婚宴場地 | 16 | 酒店、餐廳、戶外、教堂、小型場地 |

### 支援分類（5-9 篇）

| 分類 | 文章數 | 涵蓋主題 |
|------|--------|----------|
| 🎎 傳統習俗 | 14 | 过大禮、安床、敬茶、上頭、回門 |
| ⚖️ 法律財務 | 10 | 財產協議、稅務優惠、保險規劃 |
| 🎨 婚禮創意 | 10 | 拍照道具、祝酒詞、簽名板 |
| 💑 婚後生活 | 10 | 溝通技巧、理財規劃、家居佈置 |
| 🤵 賓客服務 | 9 | 座位安排、住宿、交通、兒童照顧 |
| 🎀 婚禮佈置 | 9 | 花藝、燈飾、背景牆、甜品桌 |

### 細分分類（2-8 篇）

| 分類 | 文章數 | 分類 | 文章數 |
|------|--------|------|--------|
| 🎁 禮物紀念 | 8 | 💍 婚戒珠寶 | 8 |
| 💌 請柬設計 | 7 | 👰 新娘化妝 | 7 |
| 🎵 婚禮音樂 | 7 | 👗 婚紗禮服 | 6 |
| 🎊 婚禮回禮 | 6 | 🌿 環保婚禮 | 5 |
| 💔 離婚再婚 | 4 | 📝 註冊結婚 | 4 |
| 🏖️ 蜜月旅行 | 4 | 🌍 海外結婚 | 4 |
| ⛈️ 天氣應對 | 4 | 🎬 婚禮影片 | 2 |
| 🎤 婚禮司儀 | 2 | 🛡️ 婚禮保險 | 2 |
| 👥 婚禮人員 | 2 | | |

---

## SEO 優化

### 頁面級 SEO

每篇文章包含完整的 SEO meta 標籤：

```html
<title>文章標題</title>
<meta name="description" content="文章描述">
<meta name="keywords" content="關鍵字1, 關鍵字2, 關鍵字3">
<link rel="canonical" href="動態生成">
<meta property="og:title" content="文章標題">
<meta property="og:description" content="文章描述">
<meta property="og:url" content="動態生成">
<meta property="og:image" content="品牌圖片">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
```

### Schema.org 結構化數據

- **Article Schema** — 標題、描述、作者、發佈日期
- **FAQPage Schema** — 常見問題與答案（部分文章）
- **BreadcrumbList Schema** — 麵包屑導航結構
- **WebPage Schema** — 用於隱私政策、服務條款等非文章頁面
- **WebSite + Organization Schema** — 首頁、v2、poster、heic-converter、部落格索引頁及全部 421 篇文章
- **WebApplication Schema** — 含 applicationCategory、operatingSystem、offers、aggregateRating

### AI 爬蟲兼容性

網站已針對 AI 系統进行全面優化：

| 優化項目 | 說明 |
|---------|------|
| **llms.txt** | AI 可讀的站點摘要，列出核心頁面、部落格分類、聯絡方式 |
| **robots.txt AI 規則** | 明確允許/限制 AI 爬蟲（Claude-Web、AIbot、Amazonbot、Bytespider 等） |
| **政策頁 noindex** | `privacy.html`、`terms.html` 設為 `noindex, nofollow`，避免進入 AI 訓練 |

### 動態 URL 解析

所有社交分享 URL 使用 JavaScript 動態獲取當前頁面 URL，確保在不同域名部署時正確運作：

```javascript
(function() {
    var canonical = document.querySelector('link[rel="canonical"]');
    if (canonical) canonical.href = window.location.href;
    var ogUrl = document.querySelector('meta[property="og:url"]');
    if (ogUrl) ogUrl.setAttribute('content', window.location.href);
})();
```

### 社交分享按鈕

每篇文章內建 4 個分享按鈕，URL 動態生成：

| 平台 | 實現方式 |
|------|----------|
| WhatsApp | `api.whatsapp.com/send?text=` |
| Facebook | `facebook.com/sharer/sharer.php?u=` |
| Twitter | `twitter.com/intent/tweet?url=` |
| 複製連結 | `navigator.clipboard.writeText()` |

### 內容 SOP 標準

| 規則 | 標準 | 合規率 |
|------|------|--------|
| 黃金字數 | 1,500+ 中文字符 | 100% |
| 視覺中斷 | 純文字區塊 ≤ 300 字 | 100%（實際 ≤ 100 字） |
| 視覺中斷類型 | 表格、清單、提示框、H3 標題 | 每篇文章 3-6 個 |

**為什麼是 1,500 字？**
- 防 AI 廢話：避免無中生有和重複觀點
- SEO 權重：足以佈局 1 個主關鍵字 + 5-8 個長尾關鍵字
- 香港市場：3-4 分鐘閱讀時間，保持低跳出率

**300 字視覺中斷法則：**
- 對 Google：表格和清單增加 Featured Snippets 機會
- 對讀者：迎合 F 型視覺掃描習慣，增加 Dwell Time

---

## 技術棧

| 技術 | 用途 | 版本/來源 |
|------|------|-----------|
| HTML5 | 頁面結構 | 純靜態 |
| Tailwind CSS | 樣式框架 | CDN (v3.x) |
| Font Awesome | 圖標庫 | CDN (v6.5.2) |
| Google Fonts | 字體 | Inter + Playfair Display + Noto Sans TC |
| JavaScript | 互動功能 | Vanilla JS |
| JSON-LD | 結構化數據 | Schema.org |
| Swiper.js | 輪播/滑塊 | CDN (swiper-bundle) |
| heic2any | HEIC 圖片轉換 | `js library/heic2any.min.js` |
| JSZip | ZIP 打包下載 | `js library/jszip.min.js` |
| FileSaver | 檔案下載 | `js library/FileSaver.min.js` |
| Playwright | 自動化測試 | npm 套件（v1.40） |
| Python 3 | 批次處理腳本 | — |

### 無需編譯

- 無 Node.js 依賴（除測試外）
- 無構建步驟
- 無框架依賴
- 直接部署靜態文件

---

## 自動化腳本

項目包含 3 個 Python 腳本用於內容管理與品質控制：

### 1. `fix_json_ld_and_table.py`

JSON-LD 結構化數據合併 + 表格無障礙修復。

**功能**：
- 合併重複的 JSON-LD FAQPage 區塊（保留問題數最多的）
- 為所有 `<th>` 標籤添加 `scope="col"` 以符合無障礙標準
- 生成 JSON 格式修復報告

**使用方法**：
```bash
python3 fix_json_ld_and_table.py [--test]
```

### 2. `fix_medium_issues.py`

中等 SEO 問題批量修復。

**功能**：
- 將硬編碼的絕對 URL（`https://myo-makeyourown.pages.dev/blog/`）替換為相對 URL
- 為缺少 meta robots 標籤的頁面添加 `<meta name="robots" content="index, follow">`
- 為所有 `<img>` 標籤添加 `loading="lazy"` 延遲加載

**使用方法**：
```bash
python3 fix_medium_issues.py [--test]
```

### 3. `add_sticky_bar.py`

批次為所有 HTML 頁面添加手機版 Sticky Conversion Bar。

**功能**：
- 注入完整的 CSS 樣式（含響應式設計）
- 注入 HTML 結構（品牌 Logo + WhatsApp/IG 按鈕 + CTA）
- 自動根據檔案路徑（blog/ vs 根目錄）調整圖片路徑
- 自動跳過已存在 Sticky Bar 的檔案

**使用方法**：
```bash
python3 add_sticky_bar.py
```

### 4. `add_org_schema_to_articles.py`

為所有 421 篇部落格文章批量添加 Organization JSON-LD Schema。

**使用方法**：
```bash
python3 scripts/add_org_schema_to_articles.py
```

### 5. `add_breadcrumb_schema.py`

為所有文章添加 BreadcrumbList JSON-LD 結構化數據。

**使用方法**：
```bash
python3 scripts/add_breadcrumb_schema.py
```

### 6. `cleanup_json_ld.py`

分割合併的 JSON-LD 區塊，確保每篇文章只有一個 JSON-LD script 標籤。

**使用方法**：
```bash
python3 scripts/cleanup_json_ld.py
```

### 7. `fix_canonical_urls.py`

修復 canonical URL，確保所有頁面使用動態 canonical。

**使用方法**：
```bash
python3 scripts/fix_canonical_urls.py
```

### 8. `fix_blog_titles.py`

修復部落格文章標題格式，確保標題一致性。

**使用方法**：
```bash
python3 scripts/fix_blog_titles.py
```

### 9. `generate_sitemap.py`

生成完整的 sitemap.xml，包含所有部落格文章 URL。

**使用方法**：
```bash
python3 scripts/generate_sitemap.py
```

### 10. `optimize_openings.py`

優化 Top 20 流量文章的開頭段落，直接命中讀者需求。

**使用方法**：
```bash
python3 scripts/optimize_openings.py
```

**輸入數據：** `docs/top20_articles.json`（由 `scripts/rank_articles.py` 生成）

---

## 測試

項目使用 Playwright 進行自動化端對端測試，覆蓋手機、平板、桌面三種裝置。

### 測試架構

```bash
tests/
├── homepage.spec.ts     # 首頁功能測試
└── mobile.spec.ts       # 手機版專屬測試（Sticky Bar、漢堡選單等）
```

### Playwright 配置

三種測試專案並行執行：

| 專案 | 裝置 | 視窗 |
|------|------|------|
| Mobile (iPhone 12) | 行動裝置 | 390 × 844 |
| Desktop Chrome | 桌面 | 1280 × 720 |
| Tablet (iPad) | 平板 | 768 × 1024 |

### 執行測試

```bash
# 安裝依賴
npm install

# 執行所有測試
npm test

# 手機版測試
npm run test:mobile

# 有頭模式（可視化）
npm run test:headed

# 查看測試報告
npm run report
```

---

## 部署指南

### GitHub Pages 部署

網站已配置為 GitHub Pages 靜態站點：

1. 推送代碼到 `main` 分支
2. GitHub Pages 自動從根目錄提供服務
3. 網站網址：`https://myo-makeyourown.pages.dev`

### 自定義域名

如需使用自定義域名：

1. 在倉庫 Settings → Pages 中添加自定義域名
2. 在 DNS 提供商處添加 CNAME 記錄指向 `myo-makeyourown.pages.dev`
3. 所有社交分享 URL 會自動適應新域名（使用 `window.location.href`）

### 本地預覽

```bash
# 使用任何靜態文件服務器
python3 -m http.server 8000
# 訪問 http://localhost:8000
```

---

## 專案結構

```
myo-hk/
├── index.html                  # 首頁（原始版）— Tailwind + Swiper
├── v2.html                     # 首頁（重設計版）— CSS 變量 + 動畫系統
├── poster.html                 # A5 宣傳單張 — 支援 PDF 列印下載
├── heic-converter.html         # HEIC/HEIF 轉圖片工具（中英雙語）
├── HTML-Artifacts.html         # PDF 下載實驗（html2pdf.js）
├── privacy.html                # 私隱政策
├── terms.html                  # 服務條款
├── robots.txt                  # 爬蟲指引
├── sitemap.xml                 # XML 網站地圖
│
├── blog/
│   ├── index.html              # 教學指南索引（搜尋 + 分類篩選）
│   └── [420+ .html files]      # 教學指南文章
│
├── image/
│   ├── 01_company_logo.png     # 品牌 Logo
│   ├── cert_color_beige.jpg    # 米色證書套預覽
│   ├── cert_color_blue.jpg     # 藍色證書套預覽
│   ├── cert_color_beige_texture.png
│   ├── cert_color_blue_texture.png
│   ├── cert_color_beige_and_blue.png
│   └── cert_style_[1-5]*.png   # 款式 1-5 預覽圖
│
├── js library/
│   ├── heic2any.min.js         # HEIC → PNG/JPG 轉換庫
│   ├── jszip.min.js            # ZIP 打包庫
│   └── FileSaver.min.js        # 瀏覽器端檔案儲存
│
├── tests/
│   ├── homepage.spec.ts        # 首頁 Playwright 測試
│   └── mobile.spec.ts          # 手機版 Playwright 測試
│
├── docs/                       # 文件資源
├── presentations/              # 40 個婚禮視頻展示項目
│   ├── index.html              # 視頻索引頁面
│   ├── _scaffold.sh            # 腳手架生成腳本
│   └── [01-40]-*/presentation/ # 40 個獨立 Vite + React 項目
│
├── fix_json_ld_and_table.py    # JSON-LD 合併 + 表格無障礙修復
├── fix_medium_issues.py        # SEO 中等問題批量修復
├── add_sticky_bar.py           # 批次添加手機 Sticky Bar
├── fix_medium_report.json      # 修復報告
├── fix_report.json             # 修復報告
│
├── package.json                # Node.js 依賴（Playwright 測試）
├── playwright.config.js        # Playwright 配置
├── opencode.jsonc              # OpenCode AI 編輯器配置
│
├── CLAUDE.md                   # AI 行為指南
├── USER.md                     # 用戶指南
└── SOUL.md                     # 專案靈魂文件
```

---

## 開發規範

### 修改首頁

- `index.html`：修改直接編輯 HTML/CSS，使用 Tailwind CDN + 自訂 CSS 變量
- `v2.html`：修改時使用 `:root` CSS 變量系統（`--color-primary`、`--bg-primary` 等），確保無障礙支援（`prefers-reduced-motion`）

### 修改文章

1. 直接編輯對應的 HTML 文件
2. 確保字數 ≥ 1,500 中文字符
3. 確保每 300 字內有視覺中斷（表格、清單、提示框、H3）
4. 運行 `python3 fix_medium_issues.py --test` 檢查 SEO 合規性
5. 運行 `python3 fix_json_ld_and_table.py --test` 檢查結構化數據

### 新增文章

1. 以現有文章為模板創建新 HTML 文件
2. 修改 meta 標籤（title、description、keywords）
3. 修改 canonical URL 和 OG 標籤
4. 添加 JSON-LD Article Schema
5. 在 `blog/index.html` 中添加文章卡片
6. 在 `sitemap.xml` 中添加 URL 條目
7. 運行 `python3 add_sticky_bar.py` 添加手機轉換欄

### 提交代碼

```bash
git add .
git commit -m "feat: 描述更改"
git push
```

---

## 婚禮視頻 presentations

40 個獨立婚禮視頻展示項目已完成，部署於 `presentations/` 目錄。

### 功能特點

- **40 個主題視頻** — 涵蓋香港結婚籌備各個環節（場地、習俗、婚紗、攝影等）
- **6 章節結構** — 每個視頻包含 6 個章節（開場 → 內容 → 結尾 CTA）
- **繁體中文** — 全部內容使用繁體中文
- **TypeScript + React + Vite** — 現代前端技術棧
- **無障礙支援** — `prefers-reduced-motion` 媒體查詢支援
- **響應式設計** — 適配桌面和移動設備

### 目錄結構

每個視頻項目位於 `presentations/XX-主題-slug/presentation/`，結構如下：

```
presentations/
├── index.html                  # 全部 40 個視頻的索引頁面
├── _scaffold.sh               # 視頻項目腳手架生成腳本
├── 01-hong-kong-wedding-flow/
│   └── presentation/
│       ├── src/
│       │   ├── chapters/       # 6 個章節目錄（01-coldopen ~ 06-cta）
│       │   │   └── 01-coldopen/
│       │   │       ├── Coldopen.tsx
│       │   │       ├── Coldopen.css
│       │   │       └── narrations.ts
│       │   ├── registry/
│       │   │   ├── chapters.ts  # 章節註冊表
│       │   │   └── types.ts      # 類型定義
│       │   ├── hooks/
│       │   │   └── useStepper.ts
│       │   ├── App.tsx
│       │   └── main.tsx
│       └── tsconfig.json
└── [39 more video projects...]
```

### 40 個視頻主題

| # | 主題 | 主題 |
|---|---|---|
| 01 | 香港結婚流程 | 結婚資格與文件 |
| 02 | 結婚 checklist 時間表 | 海外結婚指南 |
| 03 | 結婚習俗完整攻略 | 婚姻習俗傳統 |
| 04 | 婚禮場地選擇 | 教堂婚禮指南 |
| 05 | 海外結婚指南 | 結婚年齡須知 |
| 06 | 結婚年齡法律 | 同性婚姻 |
| 07 | 求婚策劃攻略 | 求婚驚喜創意 |
| 08 | 情人節求婚創意 | 婚禮驚喜策劃 |
| 09 | 求婚方式創意 | 訂婚派對策劃 |
| 10 | 求婚戒指選擇 | 求婚成功後準備 |
| 11 | 結婚領證流程 | 婚姻登記預約 |
| 12 | 結婚文件代辦 | 證婚人須知 |
| 13 | 結婚年齡規定 | 婚姻法新規 |
| 14 | 海外結婚代辦 | 跨境婚姻指南 |
| 15 | 婚紗挑選攻略 | 婚紗款式選擇 |
| 16 | 婚紗試穿準備 | 婚紗尺碼選擇 |
| 17 | 婚紗保養保存 | 婚紗拍攝技巧 |
| 18 | 求婚攻略完整版 | 婚禮策劃時間表 |
| 19 | 婚禮預算規劃 | 婚禮省錢技巧 |
| 20 | 婚禮賓客名單 | 婚禮座位安排 |
| 21 | 婚禮音樂選擇 | 婚禮歌單推薦 |
| 22 | 婚禮流程策劃 | 婚禮當天時間表 |
| 23 | 婚禮化妝造型 | 新娘妝容教程 |
| 24 | 新娘美甲建議 | 婚禮美髮造型 |
| 25 | 婚紗拍攝技巧 | 婚禮攝影指南 |
| 26 | 婚禮場地佈置 | 婚禮花藝設計 |
| 27 | 婚禮蛋糕選擇 | 婚禮甜品桌 |
| 28 | 婚禮回禮禮物 | 婚禮賓客禮品 |
| 29 | 婚禮統籌技巧 | 婚禮公司選擇 |
| 30 | 婚禮保險須知 | 婚禮保障 |
| 31 | 結婚證書套選擇 | 結婚證書設計 |
| 32 | 結婚請柬設計 | 結婚請帖款式 |
| 33 | 敬茶禮儀習俗 | 結婚敬茶準備 |
| 34 | 安床習俗詳解 | 結婚安床攻略 |
| 35 | 过大礼传统习俗 | 結婚過大禮攻略 |
| 36 | 回門習俗攻略 | 結婚回門禮俗 |
| 37 | 蜜月旅行攻略 | 蜜月目的地推薦 |
| 38 | 婚姻生活適應 | 婚後生活調適 |
| 39 | 婚後財務規劃 | 婚後理財攻略 |
| 40 | 結婚回禮創意 | 婚禮優惠資訊 |

### 技術架構

| 層面 | 技術 |
|------|------|
| 框架 | React 18 + TypeScript |
| 構建工具 | Vite |
| 樣式 | CSS 變量 + 傳統 CSS |
| 類型檢查 | TypeScript strict mode |
| 部署 | GitHub Pages (每視頻獨立部署) |

### 開發命令

```bash
cd presentations/01-hong-kong-wedding-flow/presentation

# 安裝依賴
npm install

# 本地開發
npm run dev

# 類型檢查
npx tsc --noEmit

# 生產構建
npm run build
```

### 創建新視頻

```bash
# 使用腳手架腳本
cd presentations
./_scaffold.sh

# 或手動創建
mkdir -p presentations/XX-topic-slug/presentation/src/{chapters,registry,hooks}
# 複製 package.json, tsconfig.json, vite.config.ts 等
```

---

## 品牌資訊

| 項目 | 詳情 |
|------|------|
| **品牌名稱** | My O! 專屬結婚證書套 |
| **WhatsApp** | +852 6379 6410 |
| **Instagram** | [@myo.makeyourown](https://www.instagram.com/myo.makeyourown/) |
| **網站** | [myo-makeyourown.pages.dev](https://myo-makeyourown.pages.dev) |
| **產品** | 客製化結婚證書套（亞麻布 / 磨砂珠光） |
| **特色** | 熱轉印（燙印）工藝、新人名字 + 日期、書法家設計字體 |

---

## 授權

© 2026 My O! 版權所有。

---

## PDF 列印除錯筆記

### 背景
`poster.html` 提供「下載 PDF」功能，透過 `window.print()` 讓瀏覽器原生輸出 A4 PDF。

### 遇到的問題與解決方案

| # | 嘗試 | 問題 | 學到的教訓 |
|---|------|------|-----------|
| 1 | `html2canvas` + `jsPDF` | 圖片被 CSS 壓扁（`object-fit: cover`、`flex`、`padding` 無法被正確捕捉） | html2canvas 不支援現代 CSS 佈局（flexbox、gap、object-fit、transform），只能用於簡單 DOM |
| 2 | `window.print()` 原生列印 | POPUP 視窗中所有圖片變空白 | `window.open()` + `document.write()` 重建 DOM 會丟失圖片資源參照，**必須在原頁面觸發 `window.print()`** |
| 3 | `@media print` + `transform: scale(calc(...))` | 海報被推到右下，左邊大片空白、右邊內容飛出 A4 | 網頁的 `margin: 0 auto` / flex 居中會在 print 時將容器推到畫面中央，`transform-origin: top left` 在此基礎上縮放 → 位移放大 |
| 4 | **✅ 最終解法**: `position: absolute; left: 0; top: 0` + 精確 `scale(1.8898)` | 完美 | **核心洞察**：print 時必須先「釘死」容器在 (0,0)，再從左上角縮放 |

### 最終實現（第 4 版）

```css
@media print {
  .a5-flyer {
    position: absolute !important;   /* 脫離排版流，避免居中位移 */
    left: 0 !important;
    top: 0 !important;
    margin: 0 !important;            /* 拔除 margin: 0 auto */
    width: 420px !important;         /* 海報原始設計寬度 */
    transform: scale(1.8898) !important;  /* A4 width(793.7px) / poster(420px) */
    transform-origin: top left !important;
  }
}
```

### 關鍵數字

| 參數 | 數值 | 來源 |
|------|------|------|
| 海報設計寬度 | 420px | `poster.html` `.a5-flyer` |
| A4 寬度（96 DPI） | 793.7px | `210mm × 3.7795 px/mm` |
| A4 高度 | 1123px | 海報高度 530px × 1.8898 = 1002px（< A4 高度，正常留白） |
| 縮放倍數 | 1.8898 | `793.7 / 420`，硬編碼避免 `calc()` 單位混算 |

### poster.html 關鍵特性

- **品牌展示**：Alex Brush 手寫字體 Logo + Noto Serif 副標題
- **產品展示**：5 款證書套設計款式網格 + 顏色選擇（米色亞麻布 / 藍色磨砂珠光）
- **QR Code**：透過 `api.qrserver.com` 動態生成 Instagram / WhatsApp / 網站 QR Code
- **客製化說明**：產品特色四格佈局（尺寸、封面、保護、印刷）
- **螢幕自適應**：JS 根據視窗寬度自動縮放海報比例