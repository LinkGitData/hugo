---
title: "Next.js 伺服器 Memory Leak 事故分析：動態載入的致命陷阱與修復指南"
date: 2026-05-18T15:14:51+08:00
draft: false
tags: ["Next.js", "Memory Leak", "Node.js", "Performance", "RCA"]
categories: ["Tech"]
mermaid: true
cover:
  image: "images/memory-leak-cover.png?v=1"
  alt: "伺服器 Memory Leak 視覺化插圖"
  caption: "當記憶體溢出，猶如資料狂流淹沒伺服器機房。"
  relative: false
---

> 🔗 **官方資料來源**：本篇報告改編自團隊內部的 RCA (Root Cause Analysis) 紀錄，旨在紀錄除錯歷程並作為未來開發的防雷指南。

這是一份以 **5W2H** 結構整理的系統事故分析報告。我們將透過生活化的比喻與深度的技術解析，完整還原本次 Next.js 伺服器在 Cloud Run 環境下，因為不當使用模組載入而引發的 **Memory Leak** （記憶體洩漏）問題，以及最終的科學驗證與解決方案。

## 📋 目錄
- [🔍 5W：發生了什麼事？](#-5w發生了什麼事)
- [🛠️ 2H：證明與解決方案](#️-2h證明與解決方案)
- [🚀 結論與未來進階](#-結論與未來進階)

---

## 🔍 5W：發生了什麼事？

### 👤 1. Who (誰受影響 / 誰發現的？)
*   **受影響範圍** ：所有存取網站的使用者，在尖峰期可能會面臨連線緩慢或中斷。
*   **相關人員** ：負責維護系統與前端架構的工程師團隊，負責排查與修復。

### ❓ 2. What (發生了什麼事？)
伺服器發生了俗稱的 **Memory Leak** （記憶體洩漏）。

> 💡 **生活化比喻** ：想像伺服器的「記憶體」是一個大水槽。正常情況下，處理完網頁請求後，用過的水就會排掉（也就是 Garbage Collection 垃圾回收機制）。但現在排水管塞住了，水一直流進來卻排不出去，最後水槽滿出來引發 **Out Of Memory** ，導致伺服器當機或被迫重啟。

### 🕒 3. When (什麼時候發生的？)
*   **潛在問題引入** ：今年 2 月底，工程師為了實作特定功能，寫下了引發問題的程式碼。
*   **問題引爆點** ：在 **3 月 17 日下午 13:01** ，該段程式碼被正式發布到雲端伺服器後，隨著網站流量逐漸增加，系統監控面板顯示記憶體開始呈現線性且「無法回復」的上升趨勢。

### 📍 4. Where (在哪裡發生的？)
*   **雲端主機** ：GCP Cloud Run（位於亞洲東區 `asia-east1` 的 `example-service` 服務）。
*   **程式碼位置** ：位於專案 `app/_lib/core/fetcher.js` 檔案內部，這裡是負責處理全站 API 資料請求的核心通道。

### 🤔 5. Why (為什麼會這樣？)
這是由於為了規避 Next.js 框架的限制，而採取了不適當的「動態載入」方式：
*   **原本面臨的限制** ：在 Next.js 的快取機制 (`unstable_cache`) 中，系統嚴格規定不能直接讀取使用者的 Request Headers，否則會觸發編譯或執行期的錯誤。
*   **導致問題的解法** ：為了規避這個報錯，工程師使用了 `await import('next/headers')` 這個寫法，也就是 **「動態載入模組」** ，試圖在執行當下才去拿取標頭資料。

> 💡 **生活化比喻** ：這就像是為了解決「圖書館不能大聲說話」的規定，發明了一招：「那我每次都花錢請一個『外送員』把紙條偷偷送進來！」。
> 
> 結果，只要有人點擊網頁，系統就叫一個外送員。悲劇的是，因為 Node.js 與 Webpack 底層機制的缺陷， **這些外送員送完紙條後，產生的紀錄竟然留在圖書館不走了** （系統無法自動回收他們）！最後幾千個外送員把圖書館擠爆，伺服器資源耗盡而崩潰。

以下我們用流程圖來解析這場記憶體災難的發生路徑：

{{< mermaid >}}
graph TD
  A1[使用者發送 Request] --> B1[呼叫核心通道 fetcher]
  B1 --> C1[動態載入 next模組]
  C1 --> D1[Node底層模組快取]
  D1 -- 無法被垃圾回收 --> E1[Memory Leak]
  E1 --> F1[伺服器 OOM 崩潰]
{{< /mermaid >}}

---

### 🕵️‍♂️ 深度盤查：為什麼排除其他可能？

在實務上， **Memory Leak** 有時候是多個因素疊加造成的。為了解除疑慮，我們深度盤查了這段期間的 Git Commits 以及幾個常見的 Next.js/Node.js 地雷區，為您做了一次「排除法」的全面診斷。這也進一步反證了為什麼 `await import` 是最高風險的嫌疑犯：

✅ **1. 排除 Next.js 官方 Fetch Cache 洩漏（已被妥善防護）**
*   **情境** ：Next.js (特別是使用 App Router 時) 有一個眾所皆知的雷點，如果在 SSR 大量使用 `fetch` 搭配 `cache: 'force-cache'` 或 `revalidate`，內建的 In-Memory Data Cache 會無上限增長，吃光記憶體。
*   **排除原因** ：檢查 `next.config.mjs` 後，發現團隊已經非常有先見之明地加入了以下設定：
```javascript
// next.config.mjs
cacheMaxMemorySize: 5 * 1024 * 1024, // 限制在 5MB
```
註解也明確寫著這是為了防止高基數 (high-cardinality) API 造成無限記憶體增長。因此這個最大的潛在兇手被排除了。

✅ **2. 排除自訂 Logger 的記憶體堆積**
*   **情境** ：開發者自己寫的 Logger 如果把 Log 存成 Array 或 Map，且沒有定期清除，就會造成洩漏。
*   **排除原因** ：我們審查了 `app/_lib/core/logger.js`。裡面的 `errorBuffer` 只在開發環境啟用；而負責頻率限制的 `logRateLimit` (Map 物件)，團隊有實作 `maybeCleanupRateLimit` 機制，每 5 分鐘會自動清理舊資料。這個模組是 Memory-Safe 的。

✅ **3. 排除 Promise 等待鎖 (Deduplication Lock)**
*   **情境** ：在先前的更新 (`0bed4e54`) 中，團隊加入了一個 `registerDevicePromise` 來防止重複註冊設備。如果這個 Promise 掛在全域變數上且永遠不 Resolve，就會造成洩漏。
*   **排除原因** ：這段程式碼受到 `if (isBrowser)` 的嚴格保護，完全不會在 Server-Side (Cloud Run) 上執行，因此不會造成雲端伺服器的記憶體洩漏。

✅ **4. 排除未清除的計時器 (Timers / Event Listeners)**
*   **情境** ：`setInterval` 未被 `clearInterval`，或 `process.on` 事件監聽器未被移除。
*   **排除原因** ：掃描了近期的所有變更，並沒有引入任何伺服器端的持續性 Timer 或全域 Event Listener。

**🎯 結論：為什麼矛頭還是指向 await import？**
在排除了上述所有常見的 Node.js/Next.js 記憶體洩漏源之後，`app/_lib/core/fetcher.js` 裡的 `await import('next/headers')` 成為了唯一在 Hot Path（高頻執行路徑）上不斷產生動態記憶體配置的程式碼。

在 Webpack 打包環境中，`await import` 不像標準的 Node.js `require` 那樣簡單。Webpack 為了處理動態加載，會把它轉譯成一段負責解析模組、分配 Promise 與 Context 的 Runtime Code。當一秒鐘幾十個 Request 都在呼叫它時，Webpack 的 Module Registry 會產生大量微小的閉包 (Closures) 與 Promise，這些東西被底層牽扯，導致 Garbage Collector (GC) 無法順利回收。

---

## 🛠️ 2H：證明與解決方案

### 🔬 6. How (如何證明是它惹的禍？怎麼修復？)

儘管透過代碼審查（Code Review）排除了其他可能，但我們身為工程師，最保險的做法是不要猜測，讓證據說話！我們可透過科學的壓力測試（Load Testing）直接驗證：

**🕵️‍♂️ 證明方式一：A/B 壓力測試對比 (推薦)**
1. **壓測當前版本（異常版）** ：使用測試軟體在一秒內對伺服器發送大量請求。監控圖表顯示伺服器記憶體瞬間飆高，且測試結束後， **記憶體使用量無法回落** （外送員不走），這證實了洩漏確實存在。
2. **壓測修復版本（正常版）** ：只要把那行 `await import` 改回「靜態載入」，用 autocannon 壓測 30 秒。如果記憶體水位線立刻恢復正常，且測試結束後 **會迅速掉回原本的安全基準線** ，那兇手就 100% 確鑿了！

**🕵️‍♂️ 證明方式二：Heap Snapshot 記憶體快照**
如果改了之後還是漏水，那我們就能利用 Heap Snapshot 直接抓出真正的深層 Leak 來源。

**✅ 修復建議**
絕對要避免在每次請求（Request）生命週期內頻繁地動態載入核心模組。應將代碼修改如下：

```javascript
// ❌ 錯誤示範：於 Request 生命週期內頻繁動態載入
const fetcher = async () => {
  const { headers } = await import('next/headers');
  // ... 執行 API 請求
}
```

改為在檔案頂端進行靜態宣告：

```javascript
// ✅ 正確示範：於檔案頂部靜態載入
import { headers } from 'next/headers'; 

const fetcher = async () => {
  // ... 執行 API 請求
}
```

> 💡 **最佳實踐** ： **不要在最底層的 fetcher 讀取 Request Context** 。應由最外層的頁面（Page 或 Layout）準備好需要的資料（如 Correlation ID 或 Token），再以參數形式「傳遞」給 fetcher，從根本上解耦並消除潛在的快取衝突與記憶體問題。

### 💰 7. How much (影響程度與代價？)
*   **系統可用性受損** ：記憶體被耗盡後，Cloud Run 容器會觸發保護機制被迫重啟。這會導致瞬間的 API 請求中斷，使用者會遇到介面卡頓或看到 502/503 錯誤畫面。
*   **運算資源浪費** ：高頻繁的動態載入 (`await import`) 會增加不必要的 CPU 開銷與解析時間，拖慢整體網站的 API 回應速度，並無謂地增加了雲端資源的帳單成本。

---

## 🚀 結論與未來進階

遇到框架限制（如 Next.js 的 `unstable_cache` 規則）時，使用 Hack 技巧（如動態載入 `await import`）往往會帶來預期之外的沈重代價。在 Node.js 的伺服器端環境下，模組的載入與底層快取機制非常容易成為 **Memory Leak** 的溫床。

**未來行動建議** ：
1. **遵循資料流向** ：嚴格遵守 Next.js 伺服器元件（Server Components）的資料傳遞流，由上往下透過 Props 傳遞 Context，而非在底層共用函式庫中強行讀取。
2. **導入壓測機制** ：將壓測（Load Testing）與記憶體快照（Memory Profiling）納入部署前的常規查核流程中，提早攔截此類效能異常，確保每次上線都安穩可靠。
