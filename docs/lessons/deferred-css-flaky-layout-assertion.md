# 教訓：deferred preload+onload CSS 讓 layout 斷言讀到未套用樣式的盒子

> **日期**：2026-09-26
> **關聯 PR**：commit `cd751c0b`
> **狀態**：已解決

---

### 問題

`tests/lighthouse-audits.spec.ts` 的 `design style images should maintain natural aspect ratio` 間歇性失敗，且**失敗的 project 每次不同**：

```
[Desktop Chrome] › design style images should maintain natural aspect ratio
  Expected: < 0.05    Received: 0.3840579710144928

[Tablet (iPad)] › 同一個測試
  Expected: < 0.05    Received: 1.827477757086696

[Mobile (iPhone 12 viewport)] › 同一個測試
  Expected: < 0.05    Received: 1.6605504587155961
```

關鍵時序證據：

| 條件 | 結果 |
|---|---|
| 隔離執行 `-g "design style images..."` 連跑 3 次 | **3/3 全過** |
| 完整套件並行（`fullyParallel: true` + 3 workers） | 偶發失敗 |
| 換成更快的 bundled headless shell（17s vs 60s） | **失敗更頻繁** |

### 教訓

**兩層**根因，只解一層不夠。

**第一層**：圖片未解碼。`waitForSelector` 只等元素掛載到 DOM，**不等圖片 `load`**。解掉後偏差從 `1.66` 降到 `0.10`——改善很大，但仍 2/3 的執行失敗。

**第二層（真正的關鍵）**：**本專案為消除 CLS，刻意把 CSS 改成 `preload + onload` 延遲載入**（見 README「421 個部落格頁面消除渲染阻塞 CSS」）。所以樣式表在 HTML 解析後才套用，而 `waitForSelector` 與 `img.complete` 兩者**都可能在樣式表套用前就為真**。此時讀到的 `clientWidth/clientHeight` 是**未套用樣式的盒子尺寸**，算出來的長寬比自然對不上。

殘差偏差落在 10–21% 這個量級，是判斷關鍵：解碼問題會造成極大偏差（>100%），10–20% 則更像「盒子根本還沒被 CSS 排版」。

**「瀏覽器越快越容易失敗」**是這個診斷的強訊號：競態窗口是「等待」造成的，跑得越快越容易在樣式套用前就量到。

### 解法

```ts
test('design style images should maintain natural aspect ratio', async ({ page }) => {
  // 'load' rather than the default, so the deferred preload+onload stylesheets
  // have been applied; measuring earlier reports unstyled box dimensions.
  await page.goto('/', { waitUntil: 'load' });

  await page.waitForSelector('.design-style-card img', { timeout: 10000 });
  // waitForSelector resolves on DOM attachment, not on image load.
  await page.waitForFunction(
    () =>
      Array.from(document.querySelectorAll<HTMLImageElement>('.design-style-card img')).every(
        (img) => img.complete
      ),
    undefined,
    { timeout: 10000 }
  );
  // Let a layout pass run so the measured box reflects the final styles.
  await page.evaluate(
    () => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)))
  );

  // ...原本的量測迴圈不變
});
```

三層依序是：樣式表套用（`load`）→ 圖片解碼（`complete`）→ 版面重算（雙 `requestAnimationFrame`）。

驗證：完整套件**連續 4 次全綠**（94 passed / 0 failed，每次約 17 秒）。只跑一次證明不了 flaky 修好。

### 預防

1. **本專案任何讀 `clientWidth` / `clientHeight` / `getBoundingClientRect` / 元素位置做斷言的測試，都必須先等 `load`**，不能只靠 `waitForSelector`。延遲 CSS 是全站性的，不是單頁問題。
2. **新寫版面相關 E2E 斷言時，驗證標準是「完整套件連跑 3–4 次」**，不是單次通過。
3. **失敗落在不同 project = 競態**，不是該 project 的問題。別去改該 project 的設定。
4. **數值量級是線索**：偏差 >100% 通常是資源未載入；10–20% 通常是樣式未套用。
5. 修好測試後**務必確認效能測試仍然跑得動**——本案例中換更快的瀏覽器反而讓潛藏的競態浮現，若只看單次執行會誤判為「環境不穩」。
