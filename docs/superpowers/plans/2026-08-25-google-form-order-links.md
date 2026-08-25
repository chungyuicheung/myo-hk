# Google Form 訂購連結（Approach A）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `index.html` 加入三個指向 Google Form（證書套訂購表單）的新視窗連結，含 gtag 追蹤與 Playwright 測試。

**Architecture:** 純靜態 HTML 修改 —— 三個 `<a target="_blank" rel="noopener">` 入口（Hero 次要連結、#contact 第三張卡片、FAQ 行內連結），無新增 JS 邏輯、無 CSP 變更、無 iframe。測試擴充現有 `tests/homepage.spec.ts`。

**Tech Stack:** HTML + Tailwind（既有 CDN）、inline gtag onclick（既有模式）、Playwright。

**Spec:** `docs/superpowers/specs/2026-08-25-google-form-order-integration-design.md`

---

### Task 1: 失敗測試先行（TDD）

**Files:**
- Modify: `tests/homepage.spec.ts`（檔案末尾 `});` 之前插入）

- [ ] **Step 1: 寫入失敗測試**

在 `test.describe` 區塊內、`RWD - 平板尺寸` 測試之前加入：

```typescript
  test('訂購表單連結應該存在且正確', async ({ page }) => {
    await page.goto('/');

    const formLinks = page.locator('a[href*="docs.google.com/forms/d/e/1FAIpQLScqX5Fq6dA50bSGzbFa14pFJ5RH3FX3PENF-kUPhuBJluCNVA"]');

    // 三個入口：Hero、#contact 卡片、FAQ 行內
    await expect(formLinks).toHaveCount(3);

    // 全部新視窗開啟且帶 noopener
    const count = await formLinks.count();
    for (let i = 0; i < count; i++) {
      await expect(formLinks.nth(i)).toHaveAttribute('target', '_blank');
      await expect(formLinks.nth(i)).toHaveAttribute('rel', /noopener/);
    }

    // Hero：.hero-section 內可見
    await expect(page.locator('.hero-section a[href*="docs.google.com/forms"]')).toBeVisible();

    // #contact：第三張卡片，含文案
    const contactCard = page.locator('#contact .contact-cta-item[href*="docs.google.com/forms"]');
    await expect(contactCard).toBeVisible();
    await expect(contactCard).toContainText('填寫網上訂購表單');

    // #faq：行內連結可見
    await expect(page.locator('#faq a[href*="docs.google.com/forms"]')).toBeVisible();
  });
```

- [ ] **Step 2: 執行並確認失敗**

Run: `npx playwright test tests/homepage.spec.ts -g "訂購表單"`
Expected: FAIL（`toHaveCount(3)` 得到 0）

### Task 2: Hero 次要連結

**Files:**
- Modify: `index.html:284-285`（btn-primary 之後）

- [ ] **Step 1: 插入連結**

```html
            <a href="#contact" class="btn-primary text-md font-semibold inline-block mb-6 md:mb-8"> 立即聯絡我們
            </a>
            <a href="https://docs.google.com/forms/d/e/1FAIpQLScqX5Fq6dA50bSGzbFa14pFJ5RH3FX3PENF-kUPhuBJluCNVA/viewform" target="_blank" rel="noopener" class="inline-block text-sm md:text-base text-rose-700 hover:text-rose-800 font-medium" onclick="gtag('event', 'click_order_form', {'event_category': 'engagement', 'event_label': 'hero', 'value': 1})">或填寫網上訂購表單 →</a>
```

（沿用站內次要連結樣式 `text-rose-700 hover:text-rose-800 font-medium`，不加 transition 以符合效能規範。）

### Task 3: #contact 第三張卡片

**Files:**
- Modify: `index.html:544`（grid 改三欄）與 `index.html:549-550`（WhatsApp 卡片後插入）

- [ ] **Step 1:** `index.html:544` 的

```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
```
改為
```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-3 md:gap-4">
```

- [ ] **Step 2:** WhatsApp 卡片 `</a>` 之後、`</div>` 之前插入：

```html
                    <a href="https://docs.google.com/forms/d/e/1FAIpQLScqX5Fq6dA50bSGzbFa14pFJ5RH3FX3PENF-kUPhuBJluCNVA/viewform" target="_blank" rel="noopener" class="contact-cta-item" onclick="gtag('event', 'click_order_form', {'event_category': 'engagement', 'event_label': 'contact', 'value': 1})">
                        <span class="icon-large" aria-hidden="true">📋</span> <span class="cta-text text-base md:text-base">填寫網上訂購表單</span>
                    </a>
```

### Task 4: FAQ 行內連結

**Files:**
- Modify: `index.html:520`

- [ ] **Step 1:** 該句改為：

```html
<p class="text-gray-700 mt-3 leading-relaxed">選擇款式與顏色 → 提供新人名字與結婚日期 → 我們確認設計稿 → 製作 → 送貨。全程可透過 Instagram 或 WhatsApp 溝通，亦可直接<a href="https://docs.google.com/forms/d/e/1FAIpQLScqX5Fq6dA50bSGzbFa14pFJ5RH3FX3PENF-kUPhuBJluCNVA/viewform" target="_blank" rel="noopener" class="text-rose-700 hover:text-rose-800 font-medium" onclick="gtag('event', 'click_order_form', {'event_category': 'engagement', 'event_label': 'faq', 'value': 1})">填寫網上訂購表單</a>。<a href="faq.html" class="text-rose-700 hover:text-rose-800 ml-1 font-medium">了解更多 →</a></p>
```

### Task 5: 驗證

- [ ] **Step 1:** Run: `npx playwright test tests/homepage.spec.ts`
Expected: ALL PASS（含新測試與既有測試）
- [ ] **Step 2:** Run: `npx playwright test`（全套）
Expected: PASS；若 CLS/TBT 迴歸測試存在於其他 spec，一併確認不受影響

### Task 6: Commit（僅在用戶明確批准後執行）

```bash
git add index.html tests/homepage.spec.ts
git commit -m "feat: add Google Form order links to homepage"
```

---

## Self-Review

1. **Spec 對應**：§3 三入口 → Task 2/3/4；§4 連結行為（target/rel/樣式/gtag）→ 各任務程式碼；§5 無 CSP → 無相關任務 ✓；§7 追蹤 → onclick 已含三種 event_label ✓；§8 測試 → Task 1/5 ✓
2. **佔位符掃描**：所有步驟含完整程式碼，無 TBD ✓
3. **一致性**：URL 三處一致；locator 選擇器與 index.html 結構對應（.hero-section、#contact .contact-cta-item、#faq）✓
