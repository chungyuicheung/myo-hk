# 教訓：Cloudflare Pages 308 轉導讓 service worker 快取污染，全部 .html 連結 ERR_FAILED

> **日期**：2026-09-26
> **關聯 PR**：commit `dda46481`
> **狀態**：已解決

---

### 問題

線上首頁「宣傳單張」等連結點擊後跳到 `chrome-error://chromewebdata/`（`net::ERR_FAILED`），但連結本身的 `href` 完全正確。

釐清範圍後發現是**系統性**故障，不只單一連結：

| 請求 | 線上回應 |
|---|---|
| `/poster.html` | 308 → `/poster` |
| `/privacy.html` | 308 → `/privacy` |
| `/terms.html` | 308 → `/terms` |
| `/v2.html` | 308 → `/v2` |
| `/blog/index.html` | 308 → `/blog/` |
| `/`、`/llms.txt`、`/sw.js` | 200 |

五條路徑全部失效，且恰好等於 `sw.js` 內 `STATIC_ASSETS`  precache 的五個 `.html`。

**誤導方向**：一度以為是 `dist/` 缺少 `poster.html`、或舊的 `myo-hk.github.io` 部署問題。實際現行站是 Cloudflare Pages，兩者皆非根因。

### 教訓

Cloudflare Pages 對每個 `*.html` 回傳 **308 到無副檔名形式**。而 `sw.js` 的安裝流程用：

```js
cache.add('/poster.html')
```

`cache.add()` **會跟隨轉導**，因此把 `redirected: true` 的回應存進了名為 `/poster.html` 的快取鍵。fetch handler 又是 cache-first：

```js
return cached || fetchPromise;   // 導覽時優先回傳快取
```

導覽請求因此拿到一個「從轉導衍生」的回應，Chrome 判定為非法導覽來源，直接中止。

診斷關鍵是 `response.redirected` 這個欄位：

```js
const hit = await cache.match('/poster.html');
// { status: 200, type: 'basic', redirected: true, url: '.../poster' }
```

`redirected: true` 就是污染指紋。

**兩層教訓**：
1. `cache.add()` 對轉導 URL 會靜默產生「redirect-derived」快取項，這在 Cache API 層面完全看不出問題。
2. 修好 cache 版本號不夠——只要 install 仍用 `cache.add()` 預快取轉導 URL，新一代快取還是會被污染。

### 解法

`sw.js` 三處改動：

```js
const CACHE_NAME = 'myo-cache-v2';   // 1. 升版，清除受污染的 v1

function isCacheable(response) {     // 2. 永不寫入轉導來源的回應
  return Boolean(response) && response.status === 200
    && response.type === 'basic' && !response.redirected;
}

async function purgeRedirectEntries() {   // 3. 安裝後精確清除
  const cache = await caches.open(CACHE_NAME);
  const keys = await cache.keys();
  await Promise.all(keys.map(async (request) => {
    const cached = await cache.match(request);
    if (cached && cached.redirected) await cache.delete(request);
  }));
}

self.addEventListener('fetch', (event) => {
  // navigation 改 network-first，快取僅作離線備援
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((response) => { cacheResponse(event.request, response); return response; })
        .catch(() => caches.match(event.request).then((c) => c || caches.match('/')))
    );
    return;
  }
  // ...
});
```

修復後 v2 快取為 7 筆（原 12 筆減去 5 個轉導項），`posterHtmlCached: false`。

### 預防

1. **不要把轉導 URL 當快取鍵**。若部署平台會做 `.html` → 無副檔名轉導，`STATIC_ASSETS` 應改列無副檔名形式，或明確知道它們不會被預快取。
2. **navigation 一律 network-first**。cache-first 對頁面導覽風險最高，因為它會重播任何不適合導覽的回應。
3. **加入 `!response.redirected` 檢查**，並在 install 後 purge 一次。這是不顯眼的防禦性條件，但刪掉就會還原此故障——所以程式碼裡留了註解說明。
4. **重現方式**：本機起一個會對 `.html` 回 308 的伺服器，就能用真實瀏覽器穩定重現，見 `docs/lessons/` 內同類診斷慣例。
5. 部署平台換成會做轉導的（Cloudflare Pages、Netlify）時，這條必須重測。
