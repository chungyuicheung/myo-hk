# Google Form 訂購整合設計（Google Form Order Integration）

**日期**：2026-08-25
**狀態**：REVISED（整合方式已由用戶選定 A；角色/範圍採預設值）— 待最終批准。如與你的意向不符，回覆修正即可，規格會相應更新。

| 決策點 | 採用結果 | 理由 |
|---|---|---|
| 整合方式 | **A — 直接連結開新視窗**（用戶已選定 2026-08-25） | 改動最小、零首屏成本、無需修改 CSP |
| 表單角色 | **附加訂購渠道**（WhatsApp / IG 保持不變） | 「add this to my homepage」語意為新增；不動現有轉換路徑，改動最小 |
| 頁面範圍 | **僅 `index.html`** | index.html 為線上首頁；v2.html 未確認為正式版 |

---

## 1. 目標與背景

將 Google Form（證書套訂購表單）加入首頁，讓訪客可直接在站內填寫訂購資料。

**站點約束（探索結果）：**

- 純靜態 HTML + Tailwind，部署於 Cloudflare Pages，無構建步驟
- `index.html` 第 35 行 CSP：`frame-src 'none'` → 內嵌 iframe 必須修改 CSP
- 網站深度效能優化：CLS 0.037、Lighthouse 98+，且有 CLS ≤0.05 迴歸測試 —— **不可**直接內嵌重型第三方 iframe
- 已有可複用的模式：圖片 Lightbox `.modal` CSS、gtag 點擊事件（`click_whatsapp` / `click_instagram`）、Playwright 測試（`tests/homepage.spec.ts`）

## 2. 表單資訊

- 短連結：`forms.gle/urG3Q6xTjTKV6m6t9`（已解析）
- 表單 URL（本方案直接使用，新視窗開啟）：
  `https://docs.google.com/forms/d/e/1FAIpQLScqX5Fq6dA50bSGzbFa14pFJ5RH3FX3PENF-kUPhuBJluCNVA/viewform`
- 表單內容：中英雙語、2 頁；欄位含電郵、新郎/新娘姓名、結婚日期、封面顏色、款式 1–6、電話、備註、取貨方式

## 3. 入口點（共 3 處，全部指向同一訂購表單連結）

1. **Hero 區**：現有「立即聯絡我們」按鈕下方加次要文字連結「或填寫網上訂購表單 →」
2. **聯絡我們區塊（#contact）**：在 WhatsApp、Instagram 卡片旁新增第三張卡片「網上訂購表單」（複用 `.contact-cta-item` 樣式）
3. **FAQ 訂購流程答案文案**：補一句「亦可填寫網上訂購表單」，並附行內連結

行動版 Sticky Bar 本期**不動**（維持 WhatsApp CTA）。

## 4. 連結行為（Approach A）

- 三個入口皆為 `<a>` 標籤：`href` = §2 的「新視窗開啟 URL」，`target="_blank"` + `rel="noopener"`
- Hero：現有「立即聯絡我們」按鈕下方加次要文字連結「或填寫網上訂購表單 →」
- 聯絡我們區塊：新增第三張 `.contact-cta-item` 卡片「網上訂購表單」（附圖標，樣式複用現有卡片）
- FAQ：訂購流程答案補一句文案並附行內連結（沿用現有 `faq.html` 行內連結樣式）
- 純 HTML + inline gtag onclick，**不新增任何 JS 邏輯**

## 5. CSP

**不修改。** `frame-src 'none'` 維持原狀 —— 本方案不引入任何第三方 frame，零安全與效能面變化。

## 6. 錯誤處理

不適用 —— 外部連結新視窗開啟，不存在嵌入載入失敗情境；Google 端問題時既有 WhatsApp/IG 渠道照常可用。

## 7. 追蹤

比照現有模式：`gtag('event', 'click_order_form', { event_category: 'engagement', event_label: '<hero|contact|faq>', value: 1 })`

## 8. 測試（擴充 tests/homepage.spec.ts）

1. 三個入口存在且可見
2. `href` 正確、`target="_blank"`、`rel="noopener"`
3. 純連結/卡片佈局，無 iframe，既有 CLS/TBT 迴歸測試不受影響

## 9. 範圍外（Out of Scope)

- v2.html、Sticky Bar 改動、替換 WhatsApp 流程、任何後端/自建表單

---

## 規格自查記錄（Spec Self-Review）

- **佔位符掃描**：無 TBD/TODO；URL 為已解析實際值
- **內部一致性**：全文已無 Modal/CSP 變更殘留；入口點 ↔ 連結行為 ↔ 測試項目互相對應
- **範圍檢查**：單一頁面、三處連結、零 JS 新邏輯，適合一份小型實作計劃
- **歧義檢查**：整合方式已由用戶選定（A）；角色與範圍採用預設且已標注

## 決策記錄

| 決策點 | 結果 |
|---|---|
| 整合方式 | ✅ 用戶選定 **A** |
| 表單角色 | 附加選項（預設，未獲異議） |
| 頁面範圍 | 僅 index.html（預設，未獲異議） |

## 待確認

修訂後規格是否批准？批准後即進入 writing-plans 實作計劃。
