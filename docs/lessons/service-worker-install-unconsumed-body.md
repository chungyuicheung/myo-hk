# 教訓：service worker install 因未消費 response body 而永久掛起

> **日期**：2026-09-26
> **關聯 PR**：commit `dda46481`（此坑在修正過程中引入，修正後一併移除）
> **狀態**：已解決

---

### 問題

修正 `sw.js` 的快取污染時，第一版改動把 install 事件搞到**永遠停在 `installing`**：

```js
// ❌ 第一版：手寫 fetch + 條件式 put
STATIC_ASSETS.map((url) =>
  fetch(url)
    .then((response) => (isCacheable(response) ? cache.put(url, response) : null))
    .catch(() => console.warn('Failed to cache: ' + url))
)
```

瀏覽器端症狀：SW 永遠 `installing`，20 秒、40 秒、60 秒…，`navigator.serviceWorker.ready` 永不 resolve。

伺服器端症狀（本機重現伺服器日誌）：大量

```
BrokenPipeError: [Errno 32] Broken pipe
  File "http/server.py", line 867, in copyfile
    shutil.copyfileobj(source, outputfile)
```

而 v1 原本用 `cache.add()` 時不會有這個問題。

### 教訓

`fetch()` 回傳的 `Response` 若**沒有把 body 讀完就把它丟掉**，瀏覽器會中止那條 stream，導致伺服器收到 broken pipe。對 `isCacheable(response)` 為 false 的回應回傳 `null`，等於**完全不消費 body**就棄置。

連帶效果：`event.waitUntil()` 等待的 Promise 從未 settle → `install` 事件永遠不完成 → SW 永遠不會 `activate`。

這是 service worker 裡很容易踩的坑，因為「不打算用這個回應」時，直覺就是回傳 `null` 或不碰它，但 `Response` 物件**佔有底層資源**。

**教訓**：在 service worker 裡，「不用某個 Response」不等於「可以安全丟棄」——必須讓它的 body 被讀完或被明確取消。

### 解法

不要手寫 `fetch()`，改回 `cache.add()`（它會正確處理 body），再另加一道清除步驟處理轉導項：

```js
async function purgeRedirectEntries() {
  const cache = await caches.open(CACHE_NAME);
  const keys = await cache.keys();
  await Promise.all(
    keys.map(async (request) => {
      const cached = await cache.match(request);
      if (cached && cached.redirected) await cache.delete(request);
    })
  );
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) =>
        Promise.allSettled(
          STATIC_ASSETS.map((url) => cache.add(url).catch(() => console.warn('Failed to cache: ' + url)))
        )
      )
      .then(purgeRedirectEntries)   // ← 附加的清除步驟
  );
  self.skipWaiting();
});
```

效果：`install` 從「永久掛起」變成 **9 毫秒完成**，v2 快取 7 筆（5 個轉導項被清除）。

### 預防

1. **不要為了自訂快取條件就手寫 `fetch()` + 條件式 `cache.put()`**。`cache.add()` 已經處理好 body 生命週期，需要額外過濾時，改成「先 `cache.add()`，再 purge」兩階段。
2. **診斷 `install` 掛起時，看伺服器端日誌**。瀏覽器只會顯示「卡在 installing」，沒有原因；`BrokenPipeError` 才是真正的線索。
3. **驗證 `install` 是否真的完成，不要只看 `caches.keys()`**。安裝進行中時讀快取會拿到部分結果（本次一度誤以為 images 沒被快取）。要輪詢 `reg.installing ? 'installing' : reg.waiting ? 'waiting' : reg.active.state`。
4. `Promise.allSettled` 能避免單一 URL 失敗讓整個 install 失敗，但不能避免「body 未被消費」造成的掛起——兩者是不同問題。
5. 若真的需要手寫 `fetch()`，至少要 `.catch(() => null)` 之外再確保 body 被處理，例如 `response.body?.cancel()`（主動取消，正確）或 `await response.arrayBuffer()`（讀完，浪費記憶體）。
