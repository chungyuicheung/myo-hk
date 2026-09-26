# 教訓：agent-browser 診斷 service worker 時的四個工具陷阱

> **環境層**：此坑不限於本專案，其他專案也可能踩到
> **日期**：2026-09-26
> **關聯 PR**：無（工具用法）
> **狀態**：已解決

---

### 問題

用 agent-browser 診斷 service worker / Cache API 時，連續踩到四個非顯而易見的陷阱，每個都造成一次錯誤結論或逾時。

### 教訓

#### 1. `eval` 不會 await 你回傳的 Promise

```js
// ❌ 回傳 {}（Promise 物件被序列化成空物件）
return { cacheNames: names };

// ✅ 必須包成字串
return JSON.stringify({ cacheNames: names });
```

#### 2. `navigator.serviceWorker.ready` 會永久掛起

若 SW 卡在 `installing`，`ready` 永不 resolve，直接撞上 MCP 30 秒 timeout：

```
MCP error -32001: Request timed out
```

改用自己輪詢 state，並加有界迴圈：

```js
const reg = await navigator.serviceWorker.getRegistration('/');
st = reg.installing ? 'installing' : reg.waiting ? 'waiting' : reg.active.state;
```

**推論**：`ready` 只適合「SW 確定會成功」的情況；診斷時它反而是最大的 timeout 來源。

#### 3. `unregister()` 會掛死

```js
const regs = await navigator.serviceWorker.getRegistrations();
await Promise.all(regs.map((r) => r.unregister()));   // ❌ 兩個瀏覽器工具都會 timeout
```

`unregister()` 觸發 SW 生命週期與頁面 context 的競態，導致 eval 所在執行環境被拆掉，Promise 永不 resolve。

**替代方案（更好）**：完全放棄手動 unregister，走瀏覽器內建的 SW 更新路徑——重新載入頁面，瀏覽器偵測到 `sw.js` 位元組不同就自動安裝新版，`skipWaiting()` + `clients.claim()` 接管，而新版 `install` 會重新預快取。

這反而**測到的是真實使用者的升級流程**，比人為重置狀態更有驗證價值。

#### 4. 沒有 `navigate_page` 這個工具

憑空猜工具名會直接回傳可用工具清單（這反而是最快的糾錯方式）。實際是：

- `agent-browser_agent_browser_open`（可帶 URL，等同導航）
- `agent-browser_agent_browser_reload`

### 解法

診斷 service worker 的可靠寫法：

```js
(async () => {
  const reg = await navigator.serviceWorker.getRegistration('/');
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const t0 = Date.now();
  while (Date.now() - t0 < 25000) {
    const st = reg.installing ? 'installing' : reg.waiting ? 'waiting'
              : reg.active ? reg.active.state : 'none';
    if (st === 'activated') break;
    await sleep(400);
  }
  const names = await caches.keys();
  const c = await caches.open('myo-cache-v2');
  const keys = await c.keys();
  const hit = await c.match('/poster.html');
  return JSON.stringify({
    swState: st,
    allCaches: names,
    entries: keys.map((k) => new URL(k.url).pathname).sort(),
    posterHtmlCached: Boolean(hit),
    redirected: hit ? hit.redirected : null,
  });
})()
```

**診斷期間只用唯讀操作**（`caches.keys()` / `cache.match()`），全程不碰 `cache.delete()`。若診斷過程本身清掉了污染快取，RED 測試就是假的——故障必須真實存在才能確定修正有效。

### 預防

1. **agent-browser 的 `eval` 一律回傳字串**（`JSON.stringify`），不要回傳物件或 Promise。
2. **不要用 `serviceWorker.ready`**，改 `getRegistration()` + 輪詢，並務必設逾時上限。
3. **不要用 `unregister()`**。要重置 SW 狀態就重載頁面，讓 `skipWaiting` 自然生效。
4. **猜工具名是安全的**——猜錯會列出所有可用工具，成本低；亂猜參數或語意才危險。
5. **本機重現伺服器要開 `Cache-Control: no-store`**，否則瀏覽器 HTTP 快取會干擾，導致無法確定請求有沒有真的經過 service worker。
6. 想知道 SW 到底做了什麼，開一個本機會做 308 轉導的靜態伺服器 + 真實瀏覽器，比讀原始碼可靠得多。
