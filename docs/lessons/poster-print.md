# 教訓：poster.html PDF 列印縮放公式

> **日期**：2026-07-20  
> **關聯 PR**：Lighthouse CLS 深度修復  
> **狀態**：已解決

---

### 問題

`poster.html` 提供「下載 PDF」功能，透過 `window.print()` 輸出 A5 海報到 A4 紙張。  
多次嘗試後仍無法正確縮放：

| # | 嘗試 | 問題 |
|---|------|------|
| 1 | `html2canvas` + `jsPDF` | 圖片被 CSS 壓扁（`object-fit: cover`、`flex`、`padding` 無法被正確捕捉）|
| 2 | `window.open()` + `document.write()` | POPUP 視窗中所有圖片變空白（重建 DOM 丟失圖片資源參照）|
| 3 | `@media print` + `transform: scale(calc(...))` | 海報被推到右下，左邊大片空白、右邊內容飛出 A4 |

### 教訓

**核心洞察**：print 時必須先「釘死」容器在 `(0, 0)`，再從左上角縮放。  
`margin: 0 auto` / flex 居中會在 print 時將容器推到畫面中央，`transform-origin: top left` 在此基礎上縮放 → 位移放大。

### 解法

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
| 海報設計寬度 | 420px | `.a5-flyer` |
| A4 寬度（96 DPI） | 793.7px | `210mm × 3.7795 px/mm` |
| A4 高度 | 1123px | 海報高度 530px × 1.8898 = 1002px（< A4 高度，正常留白） |
| 縮放倍數 | 1.8898 | `793.7 / 420`，硬編碼避免 `calc()` 單位混算 |

### 預防

- 任何涉及 `window.print()` 的列印功能，優先測試 `position: absolute` + 硬編碼 `scale()`
- 勿用 `html2canvas` 處理現代 CSS 佈局（flexbox、gap、object-fit）
- 勿用 `window.open()` 重建 DOM 做列印 —— 圖片資源會斷
