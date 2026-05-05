# My O! — 香港婚慶教學指南網站

> 為您的結婚證書打造設計師級專屬證書套，讓這份愛情的見證永恆閃耀。

**Live Site**: [https://myo-hk.github.io](https://myo-hk.github.io)
**教學指南**: [https://myo-hk.github.io/blog/](https://myo-hk.github.io/blog/)
 
---

## 📋 目錄

- [項目概述](#項目概述)
- [核心數據](#核心數據)
- [網站架構](#網站架構)
- [內容分類](#內容分類)
- [SEO 優化](#seo-優化)
- [內容生成 SOP](#內容生成-sop)
- [技術棧](#技術棧)
- [自動化腳本](#自動化腳本)
- [部署指南](#部署指南)
- [專案結構](#專案結構)
- [開發規範](#開發規範)

---

## 項目概述

My O! 是一家專注於客製化結婚證書套的香港品牌。本項目是品牌的官方靜態網站，提供：

- **品牌展示** — 產品介紹、材質選擇、客製化選項
- **婚慶教學指南** — 420+ 篇涵蓋婚禮籌備全流程的中文文章
- **SEO 內容矩陣** — 通過 Topical Authority 策略建立行業權威
- **社交分享** — 每篇文章內建 WhatsApp、Facebook、Twitter 分享按鈕

網站採用純靜態 HTML 架構，部署於 GitHub Pages，無需後端服務器。

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
myo-hk.github.io/
├── index.html              # 首頁 — 品牌展示、產品介紹、聯絡我們
├── blog/
│   ├── index.html          # 教學指南索引 — 搜尋、分類篩選、動態計數
│   └── [420+ articles]     # 教學指南文章
├── privacy.html            # 私隱政策
├── terms.html              # 服務條款
├── sitemap.xml             # XML 網站地圖
├── robots.txt              # 爬蟲指引
└── image/                  # 圖片資源
    └── 01_company_logo.png # 品牌 Logo
```

### 頁面連結策略

- **零孤立頁面** — 每篇文章包含 4 個「延伸閱讀」連結，指向隨機相關文章
- **雙向導航** — 所有頁面均可透過導航列返回首頁和教學指南索引
- **麵包屑導航** — 每篇文章包含「首頁 > 教學指南 > 文章標題」麵包屑
- **底部 CTA** — 每篇文章底部包含 WhatsApp 和 Instagram 聯絡我們按鈕

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
```

### Schema.org 結構化數據

- **Article Schema** — 標題、描述、作者、發佈日期
- **FAQPage Schema** — 常見問題與答案（部分文章）
- **BreadcrumbList Schema** — 麵包屑導航結構

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
| Google Fonts | 字體 | Inter (300/400/600/700) |
| JavaScript | 互動功能 | Vanilla JS |
| JSON-LD | 結構化數據 | Schema.org |

### 無需編譯

- 無 Node.js 依賴
- 無構建步驟
- 無框架依賴
- 直接部署靜態文件

---

## 自動化腳本

項目包含 4 個 Python 腳本用於內容管理：

### 1. `generate_articles.py`

批量生成教學指南文章的 HTML 文件。

**用途**：從文章定義列表快速生成符合模板的 HTML 文件，包含完整的 SEO meta 標籤、OG 標籤、Twitter Card、結構化數據、導航、麵包屑、延伸閱讀和 CTA。

**使用方法**：
```bash
python3 generate_articles.py
```

### 2. `audit_and_fix_articles.py`

審計並修正文章以符合 SOP 標準。

**功能**：
- 計算每篇文章的字數
- 檢測最長純文字區塊
- 自動插入表格、清單、提示框和 H3 標題
- 按分類匹配對應的豐富內容

**使用方法**：
```bash
python3 audit_and_fix_articles.py
```

### 3. `enrich_articles.py`

為字數不足的文章補充內容。

**功能**：
- 識別低於 1,500 字的文章
- 插入詳細指南、比較分析、檢查清單、專業貼士、常見問題和婚後事項等模塊
- 確保每篇文章達到目標字數

**使用方法**：
```bash
python3 enrich_articles.py
```

### 4. `fix_links_and_share.py`

修復 URL、添加分享按鈕、確保無孤立頁面。

**功能**：
- 將 og:url、canonical、og:image 改為動態 `window.location.href`
- 為每篇文章添加 WhatsApp、Facebook、Twitter、複製連結分享按鈕
- 隨機分配 4 篇相關文章作為延伸閱讀
- 確保所有頁面都有內部連結

**使用方法**：
```bash
python3 fix_links_and_share.py
```

---

## 部署指南

### GitHub Pages 部署

網站已配置為 GitHub Pages 靜態站點：

1. 推送代碼到 `main` 分支
2. GitHub Pages 自動從根目錄提供服務
3. 網站網址：`https://myo-hk.github.io`

### 自定義域名

如需使用自定義域名：

1. 在倉庫 Settings → Pages 中添加自定義域名
2. 在 DNS 提供商處添加 CNAME 記錄指向 `myo-hk.github.io`
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
├── index.html                  # 首頁
├── privacy.html                # 私隱政策
├── terms.html                  # 服務條款
├── robots.txt                  # 爬蟲指引
├── sitemap.xml                 # XML 網站地圖
├── opencode.jsonc              # OpenCode 配置
│
├── blog/
│   ├── index.html              # 教學指南索引（搜尋 + 分類篩選）
│   └── [420+ .html files]      # 教學指南文章
│
├── image/
│   └── 01_company_logo.png     # 品牌 Logo
│
├── js library/                 # JavaScript 庫
│
├── generate_articles.py        # 批量生成文章
├── audit_and_fix_articles.py   # SOP 審計與修正
├── enrich_articles.py          # 文章內容補充
├── fix_links_and_share.py      # 連結與分享修復
├── generate_articles_batch1.sh # 批量生成腳本（Shell）
└── heic-converter.html         # HEIC 圖片轉換工具
```

---

## 開發規範

### 新增文章

1. 在 `generate_articles.py` 的 `ARTICLES` 列表中添加文章定義：
   ```python
   ("文件名", "分類", "標題", "描述", "關鍵字"),
   ```
2. 運行 `python3 generate_articles.py`
3. 運行 `python3 fix_links_and_share.py` 添加分享按鈕和相關連結
4. 在 `blog/index.html` 中添加文章卡片

### 修改現有文章

1. 直接編輯 HTML 文件
2. 確保字數 ≥ 1,500 中文字符
3. 確保每 300 字內有視覺中斷（表格、清單、提示框、H3）
4. 運行 `python3 audit_and_fix_articles.py` 檢查合規性

### 提交代碼

```bash
git add .
git commit -m "feat: 描述更改"
git push
```

---

## 品牌資訊

| 項目 | 詳情 |
|------|------|
| **品牌名稱** | My O! 專屬結婚證書套 |
| **WhatsApp** | +852 6379 6410 |
| **Instagram** | [@myo.makeyourown](https://www.instagram.com/myo.makeyourown/) |
| **網站** | [myo-hk.github.io](https://myo-hk.github.io) |
| **產品** | 客製化結婚證書套（亞麻布 / 磨砂珠光） |
| **特色** | 熱轉印（燙印）工藝、新人名字 + 日期、書法家設計字體 |

---

## 授權

© 2026 My O! 版權所有。
