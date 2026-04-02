# AI Keyword Content Expansion Plan

> **Created**: 2026-04-02  
> **Objective**: Expand content matrix using AI-driven keyword research and programmatic SEO  
> **Target**: 50+ articles within 3 months

---

## 1. Keyword Research Strategy

### 1.1 Core Keyword Clusters

| Cluster | Primary Keywords | Search Intent | Article Count |
|---------|-----------------|---------------|---------------|
| **註冊流程** | 結婚註冊流程, 擬結婚通知書, 婚姻登記處 | 資訊型 | 5 |
| **證書套** | 結婚證書套, 證書套推薦, 客製化證書套 | 商業型 | 8 |
| **婚禮籌備** | 婚禮籌備清單, 結婚預算, 婚前準備 | 資訊型 | 10 |
| **場地推薦** | 婚宴場地, 註冊場地, 戶外婚禮 | 商業型 | 15 |
| **供應商** | 婚攝推薦, 化妝師, 司儀, 婚紗 | 商業型 | 12 |
| **法律知識** | 結婚法律, 海外結婚, 離婚再婚 | 資訊型 | 6 |
| **文化習俗** | 過大禮, 安床, 回門, 敬茶 | 資訊型 | 8 |
| **蜜月旅行** | 蜜月推薦, 蜜月預算, 簽證 | 商業型 | 6 |

### 1.2 AI-Generated Long-Tail Keywords

Using programmatic SEO approach:

**地區 × 場地類型**:
- `{地區} + 婚宴場地推薦` (18 區 × 3 類型 = 54 頁面)
- `{地區} + 註冊場地` (18 區 × 2 類型 = 36 頁面)
- `{地區} + 婚攝推薦` (18 區 = 18 頁面)

**材質 × 產品**:
- `{材質} + 結婚證書套` (5 材質 = 5 頁面)
- `{風格} + 證書套設計` (6 風格 = 6 頁面)

**預算 × 服務**:
- `{預算範圍} + 婚禮攝影` (4 範圍 = 4 頁面)
- `{預算範圍} + 婚宴` (4 範圍 = 4 頁面)

---

## 2. Content Generation Workflow

### 2.1 AI Content Pipeline

```
Keyword Research → Content Brief → AI Draft → AI Review → Web Search Review → Auto-Fix → Publish
     (AI)            (AI)           (AI)        (AI)         (AI + Web)        (Auto)      (Auto)
```

### 2.2 Automated Workflow Steps

1. **Keyword Discovery** (AI)
   - Use Exa Search to find trending wedding keywords
   - Analyze competitor content gaps
   - Generate keyword clusters with search volume estimates

2. **Content Brief Generation** (AI)
   - Auto-generate content outlines based on top-ranking pages
   - Include target keywords, H2/H3 structure, FAQ suggestions
   - Add internal linking recommendations

3. **AI Draft Creation** (AI)
   - Generate first draft using approved templates
   - Maintain brand voice and tone guidelines
   - Include placeholder for product mentions

4. **🆕 AI Review** (AI)
   - **Grammar & Readability Check**: AI 檢查語法、錯字、句子流暢度、用詞一致性
   - **SEO Compliance**: 驗證 title/meta 長度（30-60/120-160 字元）、關鍵字密度（1-2%）、H 標籤結構（單一 H1）
   - **Schema Validation**: 自動檢查 FAQPage/HowTo/Article JSON-LD 格式正確性
   - **Internal Link Audit**: 確認所有內部連結指向有效頁面，無 404
   - **AI Slop Detection**: 檢測過度模板化、重複短語、空洞內容、AI 痕跡
   - **Content Structure Check**: 驗證 80% 資訊 + 20% 產品比例
   - **輸出**: 自動修復輕微問題（格式、標點），標記需人工處理的嚴重問題，生成「AI 審查報告」

5. **🆕 Web Search Review** (AI + Web Tools)
   - **Fact-Checking via Exa Search**: 交叉驗證所有事實聲明（法律條文、費用、程序、日期）
   - **Tier 0-1 Source Verification**: 自動比對 elegislation.gov.hk、immd.gov.hk、clic.org.hk 官方資料
   - **Competitor Content Comparison**: 搜尋同關鍵字 Google top 3 結果，確保內容深度、字數、結構不遜色
   - **Price/Date Accuracy Check**: 驗證所有價錢和日期是否為最新，標註過時資訊
   - **Broken External Link Detection**: 檢查所有外部連結是否有效（返回 200）
   - **Multi-Source Cross-Validation**: 對每個事實聲明至少找 2 個獨立來源交叉驗證
   - **輸出**: 生成「事實核查報告」，包含：✅ 已驗證聲明、⚠️ 需人工確認、❌ 發現矛盾/過時

6. **🆕 Auto-Fix & Optimization** (AI)
   - **自動修復 AI Review 標記問題**: 修正語法、SEO 不合規、AI Slop
   - **自動處理 Web Search Review ⚠️ 項目**: 加入「資料可能變動」免責聲明、更新過時資訊
   - **自動處理 ❌ 矛盾項目**: 以 Tier 0-1 來源為準自動修正內容
   - **自動本地化**: 加入香港地道用語、常見表達方式
   - **自動產品植入調整**: 確保 My O! 證書套提及自然（不超過 20% 篇幅）
   - **自動品牌語氣優化**: 調整語氣符合 My O! 品牌定位
   - **自動生成 HTML**: 從 markdown 模板生成完整 HTML
   - **自動更新 sitemap.xml**: 加入新文章 URL

7. **Publish & Monitor** (Auto)
   - Auto-generate HTML from markdown template
   - Update sitemap.xml automatically
   - Deploy to GitHub Pages
   - Monitor performance in Search Console

---

## 3. Programmatic SEO Implementation

### 3.1 Template-Based Page Generation

**場地推薦頁面模板**:
```markdown
# {地區}{場地類型}推薦 2026

## 為什麼選擇{地區}？
{地區特色介紹}

## Top {數量} {場地類型}推薦
1. {場地名稱} - {特色} - {價錢範圍}
2. {場地名稱} - {特色} - {價錢範圍}
3. {場地名稱} - {特色} - {價錢範圍}

## {地區}婚禮場地比較
| 場地 | 容納人數 | 價錢 | 特色 |
|------|----------|------|------|
| {場地1} | {人數} | {價錢} | {特色} |
| {場地2} | {人數} | {價錢} | {特色} |

## 常見問題
- {地區}婚禮場地要提前多久預訂？
- {地區}婚宴價錢範圍？
- {地區}有什麼特色婚禮場地？
```

### 3.2 Data Sources for Automation

| Data Type | Source | Update Frequency |
|-----------|--------|------------------|
| 場地資料 | 政府公開資料、場地官網 | 每月 |
| 價錢資訊 | 場地官網、婚慶平台 | 每季 |
| 評價評分 | Google Reviews、OpenRice | 每月 |
| 交通資訊 | 運輸署、地鐵官網 | 每季 |

---

## 4. Content Calendar (Next 3 Months)

### Month 1: Core Expansion (Weeks 1-4)
- [ ] 過大禮清單 2026（完整指南）
- [ ] 敬茶儀式流程（傳統vs現代）
- [ ] 安床習俗與禁忌
- [ ] 回門習俗介紹
- [ ] 結婚法律知識（財產、姓名）
- [ ] 離婚人士再婚指南
- [ ] 絲絨證書套 vs 亞麻布證書套
- [ ] 燙印證書套價錢比較
- [ ] 證書套保養貼士
- [ ] 客製化證書套設計靈感

### Month 2: Programmatic Launch (Weeks 5-8)
- [ ] 18 區婚宴場地推薦（系列文章）
- [ ] 18 區註冊場地推薦（系列文章）
- [ ] 預算 $10K 以下婚禮攝影
- [ ] 預算 $10K-20K 婚禮攝影
- [ ] 預算 $20K-50K 婚禮攝影
- [ ] 預算 $50K+ 婚禮攝影
- [ ] 戶外婚禮場地推薦
- [ ] 小型婚宴場地推薦
- [ ] 教堂婚禮場地推薦
- [ ] 酒店婚宴場地推薦

### Month 3: Authority Building (Weeks 9-12)
- [ ] 香港結婚文化變遷
- [ ] 中西婚禮習俗比較
- [ ] 結婚證書歷史
- [ ] 婚戒材質比較（黃金 vs 白金 vs 玫瑰金）
- [ ] 鑽石 4C 選購指南
- [ ] 婚紗租賃 vs 購買比較
- [ ] 婚禮保險有必要嗎？
- [ ] 結婚稅務優惠指南
- [ ] 婚後理財規劃
- [ ] 蜜月簽證完整指南

---

## 5. AI Prompt Templates

### 5.1 Keyword Research Prompt
```
你是 SEO 專家和香港婚慶市場分析師。請為「{主題}」生成：
1. 10 個高搜尋量長尾關鍵字（附預估搜尋量）
2. 5 個競爭對手未覆蓋的內容缺口
3. 3 個 Programmatic SEO 頁面組合建議
4. 搜尋意圖分析（資訊型/商業型/交易型）

輸出格式：表格，包含關鍵字、搜尋量、競爭度、搜尋意圖
```

### 5.2 Content Brief Prompt
```
你是內容策略專家。請為關鍵字「{關鍵字」生成內容大綱：
1. H1 標題（符合 SEO 最佳實踐）
2. H2/H3 結構（8-12 個小節）
3. 目標字數（1500-2500 字）
4. 內部連結建議（3-5 個現有文章）
5. FAQ 區塊（5 個問題）
6. 產品植入點（My O! 證書套自然植入）

輸出格式：結構化大綱，標註每個小節的目標關鍵字
```

### 5.3 Content Generation Prompt
```
你是專業婚慶內容作家。根據以下大綱撰寫文章：
- 關鍵字：{關鍵字}
- 目標讀者：{讀者描述}
- 字數：{字數}
- 語氣：專業但親切，使用繁體中文
- 要求：
  * 加入真實數據和來源引用
  * 包含 5 個 FAQ
  * 自然植入 My O! 證書套產品（不超過 20% 篇幅）
  * 加入免責聲明
  * 使用 H2/H3 結構

輸出格式：完整文章，包含 HTML 標籤
```

### 5.4 🆕 AI Review Prompt
```
你是 SEO 內容審查專家。請審查以下文章並輸出審查報告：

文章：{文章內容}
目標關鍵字：{關鍵字}

審查項目：
1. 語法與錯字檢查 — 列出所有錯誤
2. SEO 合規檢查 — title 8-21 字元、meta 36-50 字元、單一 H1、關鍵字密度 1-2%
3. AI Slop 檢測 — 標記過度模板化、重複短語、空洞內容
4. 內部連結檢查 — 確認所有 href 指向有效頁面
5. Schema 格式檢查 — FAQPage/Article JSON-LD 是否有效
6. 產品比例檢查 — My O! 提及是否超過 20%

輸出格式：
- ✅ 通過項目
- ⚠️ 需人工處理項目（具體說明）
- ❌ 阻擋發布項目（必須修復）
- 自動修復建議
```

### 5.5 🆕 Web Search Review Prompt
```
你是事實核查專家。請對以下文章進行多源驗證：

文章：{文章內容}
包含的事實聲明：{提取的事實列表}

核查流程：
1. 對每個事實聲明，使用 Exa Search 找至少 2 個獨立來源
2. 優先比對 Tier 0（elegislation.gov.hk）和 Tier 1（immd.gov.hk）來源
3. 檢查所有價錢和日期是否為最新
4. 搜尋同關鍵字 Google top 3 結果，比較內容深度

輸出格式：
事實核查報告：
- ✅ {聲明} — 已驗證（來源 1, 來源 2）
- ⚠️ {聲明} — 需人工確認（原因）
- ❌ {聲明} — 發現矛盾（官方說法 vs 文章說法）

競爭對手比較：
- 字數比較：本文 {字數} vs top 3 平均 {字數}
- 結構比較：本文 {H2 數量} 個 H2 vs top 3 平均 {數量} 個
- 內容缺口：top 3 有但本文沒有的主題
```

---

## 6. Quality Control Framework

### 6.1 AI Content Validation Checklist

#### Phase 1: AI Review（自動）
| 檢查項 | 標準 | 驗證方式 |
|--------|------|----------|
| **語法與錯字** | 零錯字、語法正確 | AI 自動檢查 |
| **可讀性** | Flesch Reading Ease > 60 | AI 工具檢查 |
| **AI Slop Detection** | 無過度模板化、無重複短語 | AI 自動檢測 |
| **關鍵字密度** | 1-2% 自然出現 | AI 工具檢查 |
| **Title 長度** | 8-21 中文字元 | 自動檢查 |
| **Meta Description** | 36-50 中文字元 | 自動檢查 |
| **H 標籤結構** | 單一 H1、正確層級 | 自動檢查 |
| **內部連結** | 3-5 個相關連結，無 404 | 自動檢查 |
| **Schema Markup** | FAQPage + Article 格式正確 | 自動驗證 |
| **產品比例** | 不超過 20% 篇幅 | AI 自動計算 |

#### Phase 2: Web Search Review（AI + Web Tools）
| 檢查項 | 標準 | 驗證方式 |
|--------|------|----------|
| **事實準確性** | Tier 0-1 來源支持 | Exa Search + Web Fetch 交叉驗證 |
| **法律條文** | 與 elegislation.gov.hk 一致 | 自動比對法例原文 |
| **費用/程序** | 與 immd.gov.hk 一致 | 自動比對官方網頁 |
| **價錢時效性** | 標註「可能變動」或最新數據 | 搜尋最新公開資料 |
| **競爭對手比較** | 內容深度 ≥ top 3 結果 | Exa Search 比較字數、結構 |
| **外部連結** | 全部返回 200 | 自動 HTTP 檢查 |
| **多源驗證** | 每事實聲明 ≥ 2 獨立來源 | Exa + Web Fetch 交叉驗證 |

#### Phase 3: Auto-Fix（AI 自動修復）
| 檢查項 | 標準 | 驗證方式 |
|--------|------|----------|
| **自動修復 AI 問題** | 修正語法、SEO 不合規、AI Slop | AI 自動執行 |
| **自動處理 ⚠️ 項目** | 加入免責聲明、更新過時資訊 | AI 自動執行 |
| **自動處理 ❌ 矛盾** | 以 Tier 0-1 來源為準修正 | AI 自動執行 |
| **自動本地化** | 加入香港地道用語 | AI 自動執行 |
| **產品比例調整** | My O! 提及不超過 20% | AI 自動調整 |
| **品牌語氣優化** | 符合 My O! 品牌定位 | AI 自動調整 |
| **HTML 生成** | 完整 HTML 文件 | AI 自動生成 |

### 6.2 Performance Monitoring

| 指標 | 目標 | 監控頻率 |
|------|------|----------|
| 自然流量增長 | +20% 每月 | 每週 |
| 關鍵字排名 | Top 20 關鍵字 +10 每月 | 每週 |
| 頁面停留時間 | > 2 分鐘 | 每月 |
| 跳出率 | < 60% | 每月 |
| 轉換率（CTA 點擊） | > 3% | 每月 |

---

## 7. Technical Implementation

### 7.1 Static Site Generator Migration

**Phase 1**: Continue with HTML (Current)
- Manual content creation
- Direct HTML editing
- Basic sitemap updates

**Phase 2**: Migrate to Astro (Month 2)
- Markdown-based content creation
- Component-based layouts
- Auto-generated sitemap/RSS
- Internal link automation
- Schema markup automation

**Phase 3**: Programmatic SEO (Month 3)
- Database-driven page generation
- Template-based content creation
- Automated internal linking
- Dynamic sitemap updates

### 7.2 Content Management Workflow

```
AI Research → Content Brief → AI Draft → AI Review → Web Search Review → Auto-Fix → Publish
      ↓             ↓             ↓            ↓              ↓              ↓             ↓
  Keyword DB   Template DB   Draft DB    AI Review Log   Fact Check    Auto-Fix Log   GitHub Pages
                                                    Report
```

**Auto-Fix Actions**:
- ✅ AI Review issues: auto-fix grammar, SEO, structure
- ⚠️ Web Search warnings: add disclaimers, update stale data
- ❌ Contradictions: auto-correct to match Tier 0-1 sources
- 🔄 Localization: add HK colloquial terms, brand voice
- 📦 HTML generation: markdown → complete HTML file

**AI Review Output**:
- ✅ Auto-fixed: formatting, punctuation, minor grammar
- ⚠️ Flagged: AI slop detection, structure issues, product ratio
- ❌ Blocked: missing schema, broken links, title/meta violations

**Web Search Review Output**:
- ✅ Verified: facts matched with Tier 0-1 sources
- ⚠️ Needs Confirmation: prices/dates that may have changed
- ❌ Contradiction Found: facts that conflict with official sources

---

## 8. Budget & Resources

| 項目 | 成本 | 備註 |
|------|------|------|
| AI 工具 | HK$0-200/月 | ChatGPT/Claude 免費版足夠 |
| SEO 工具 | HK$0-500/月 | Ahrefs/Semrush（可選） |
| 內容審核 | HK$0 | 自行審核 |
| 技術基建 | HK$0 | GitHub Pages 免費 |
| **總計** | **HK$0-700/月** | |

---

## 9. Success Metrics

### 3-Month Targets

| 指標 | 當前 | 目標 | 增長 |
|------|------|------|------|
| 文章數量 | 16 | 50+ | +212% |
| 月自然流量 | 0 | 5,000+ | 新增 |
| 關鍵字排名 | 0 | Top 50: 20+ | 新增 |
| 內部連結 | 2.8/篇 | 4.0/篇 | +43% |
| 孤島頁面 | 0 | 0 | 保持 |

### 6-Month Targets

| 指標 | 目標 |
|------|------|
| 文章數量 | 100+ |
| 月自然流量 | 15,000+ |
| 關鍵字排名 | Top 20: 30+ |
| 月收入 | HK$10,000-25,000 |

---

## 10. Next Steps

### Immediate (This Week)
1. [ ] 設定 AI 關鍵字研究工作流程
2. [ ] 生成第一批 10 篇内容大綱
3. [ ] 建立 Programmatic SEO 模板
4. [ ] 設定內容審核清單

### Short-term (Month 1)
1. [ ] 發布 10 篇新文章
2. [ ] 建立 18 區場地頁面模板
3. [ ] 優化現有 16 篇文章內容深度
4. [ ] 設定 GA4 和 Search Console 監控

### Medium-term (Months 2-3)
1. [ ] 遷移至 Astro SSG
2. [ ] 自動化 sitemap 生成
3. [ ] 發布 30+ Programmatic SEO 頁面
4. [ ] 申請聯盟計畫和 AdSense

---

**Plan Version**: 1.0  
**Last Updated**: 2026-04-02  
**Status**: Ready for Implementation
