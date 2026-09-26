# 教訓：npx playwright install 下載完成但解壓永久卡死

> **環境層**：此坑不限於本專案，其他專案也可能踩到
> **日期**：2026-09-26
> **關聯 PR**：無（環境問題）
> **狀態**：已解決

---

### 問題

`npx playwright install chromium` 永遠卡住。下載本身正常（進度條到 `100% of 165.5 MiB`），但解壓階段停止推進：

```
~/Library/Caches/ms-playwright/chromium-1217/   448K / 39 檔   ← 凍結
```

連續觀察 10 分鐘（每 30 秒取樣），檔案數與大小**完全零變化**。

下游症狀：

```
Error: browserType.launch: Executable doesn't exist at
/Users/bubu/Library/Caches/ms-playwright/chromium_headless_shell-1217/
chrome-headless-shell-mac-arm64/chrome-headless-shell
```

### 教訓

卡住的是 **Playwright 自己的進程外解壓輔助程序** `oopDownloadBrowserMain.js`，不是 zip 損壞、不是 macOS、不是 Gatekeeper、不是檔案系統。

診斷路徑：

```bash
ps -o pid,stat,time,%cpu,command -p <install pid>
# STAT=SN  TIME=0.58s  %CPU=0.0     ← 睡眠中，幾乎沒燒 CPU

pgrep -P <install pid>
# <child> ... /lib/server/registry/oopDownloadBrowserMain.js

lsof -p <child> | grep zip
# /Users/.../playwright-download-chromium-mac15-arm64-1217.zip   ← zip 已完整下載
```

**決定性驗證**：把同一個 zip 改用 macOS 原生 `ditto` 解壓。

```bash
time ditto -x -k chromium-1217.zip ~/Library/Caches/ms-playwright/chromium-1217
# 0.45s user  0.30s system  95% cpu  0.783 total   →  336M / 335 檔
```

0.783 秒完成。同一份資料、同一個檔案系統，Playwright 內部解壓卻卡 10 分鐘零成長 → 瓶頸確定在 Playwright。

**誤診紀錄**：過程中曾判定「只是慢，耐心等」，那是錯的。判斷依據應是「10 分鐘零成長」這種絕對停滯，不是單次取樣沒變化。

### 解法

下載讓它跑完，保全 zip，殺掉卡死程序，改用 `ditto` 解壓，再手動寫入 Playwright 認的完成標記。

```bash
# 1. 讓下載跑完，等 log 出現 "100% of"
npx playwright install chromium

# 2. 保全 zip（必須在殺程序之前，temp 目錄可能被清）
HS=$(pgrep -f 'oopDownloadBrowserMain' | head -1)
ZIP=$(lsof -p $HS | grep -oE '/Users/.*playwright-download-[^ ]*\.zip' | head -1)
cp "$ZIP" /tmp/chromium-1217.zip

# 3. 終止卡死程序
pkill -f 'playwright install'; pkill -f 'oopDownloadBrowserMain'

# 4. 驗證 zip 完整
unzip -t /tmp/chromium-1217.zip

# 5. 用 ditto 解壓到 Playwright 預期路徑
DEST=~/Library/Caches/ms-playwright/chromium-1217
mkdir -p "$DEST" && ditto -x -k /tmp/chromium-1217.zip "$DEST"

# 6. 寫入完成標記（Playwright 靠這個判定安裝成功）
touch "$DEST/INSTALLATION_COMPLETE"
```

**headless shell 必須另外裝**。只裝 `chromium` 不夠，Playwright 預設 headless 模式要的是 `chromium_headless_shell-1217`：

```bash
npx playwright install chromium-headless-shell   # 重複上述步驟
```

最終結果：

```
chromium-1217/                 336M  ✅ INSTALLATION_COMPLETE
chromium_headless_shell-1217/  189M  ✅ INSTALLATION_COMPLETE
```

裝在**共用 cache**，所以這台機器上所有 Playwright 專案都零設定可用，不需要 `channel`、不需要 alias、不需要動任何專案設定檔。

### 預防

1. **`npx playwright install` 卡住時，先量 CPU 再判斷**。`%CPU=0.0` + `TIME` 停在極小值 = 死鎖，不是慢。
2. **不要重試同一件事超過兩次**。第一次卡住就該改走 `ditto` 手動路徑，本次浪費了兩輪 15 分鐘的工具逾時。
3. **絕對不要在解壓中途殺程序後重跑安裝**——會留下半損的 `chromium-1217`（本次親自清掉過一次），而且舊的 partial 目錄會讓狀況更難判讀。
4. **先找 `INSTALLATION_COMPLETE` 這個標記的名字**（`grep -rhoE "INSTALLATION_COMPLETE[A-Z_]*" node_modules/playwright-core/lib/`），才能手動補齊。
5. 若 `npx playwright install` 在此機器持續失敗，別退而求其次去改專案設定檔（`channel: 'chrome'` 會讓測試依賴本機安裝的 Chrome）。修環境優先於繞過。
6. 下載檔案位置：`lsof -p <child pid> | grep -oE '/Users/.*playwright-download-[^ ]*\.zip'`。
