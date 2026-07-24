---
title: "Cloudflare 企業級 MCP 佈署指南：推動 AI 代理走向標準化與安全管理"
date: 2026-07-24T11:41:36+08:00
draft: false
tags: ["MCP", "Cloudflare", "AI Agents", "Security"]
categories: ["Tech"]
mermaid: true
cover:
  image: "images/cloudflare-mcp-cover.png?v=1"
  alt: "Cloudflare MCP Concept"
  caption: "Cloudflare 企業級 MCP 與代理人工作流程圖解"
  relative: false
---

> 🔗 **官方資料來源**：
> - [MCP 示範日：10 家領先的 AI 公司如何在 Cloudflare 上建置 MCP 伺服器](https://blog.cloudflare.com/zh-tw/mcp-demo-day/)
> - [Scaling MCP adoption: Our reference architecture for simpler, safer and cheaper enterprise deployments of MCP](https://blog.cloudflare.com/enterprise-mcp/)

隨著人工智慧從單純的「問答對話」快速轉向「自主執行」，我們正全面邁入 **「代理人時代 (Agentic Era)」** 。要讓 AI 代理人 (AI Agents) 能夠跨越應用程式的藩籬，自主查詢資料庫、調閱監控日誌、操作專案看板、甚至部署程式碼，關鍵的基礎設施通訊協定便是 Anthropic 所提出的 **模型上下文通訊協定 (Model Context Protocol, 簡稱 MCP)** 。

Cloudflare 近期透過一連串重磅發布，展現了其在 AI 代理人基礎設施領域的強大野心。不僅聯手 10 家業界頂尖的科技巨頭展示了遠端 MCP 伺服器 (Remote MCP) 的創新應用，更正式公開了內部研發的 **企業級 MCP 參考架構 (Enterprise Reference Architecture)** 。本文將深度解析這項變革，帶您了解 Cloudflare 如何解決遠端 MCP 在企業落地時面臨的安全、治理與 Token 成本痛點。

## 📋 目錄
1. 🌟 前言：從 GUI 邁向 LUI 與代理人基礎設施
2. 🚀 MCP 核心概念：為何解耦 Client 與 Server 是關鍵？
3. 💻 Cloudflare 上的 MCP 生態系：十家領先企業的實踐案例
4. 🏗️ 企業級 MCP 參考架構：集中治理與邊緣部署
5. 🛡️ 資安防衛戰：身分驗證、DLP 與影子 MCP (Shadow MCP) 攔截
6. 💰 突破性的成本優化： Code Mode 如何節省 94% 的 Token
7. 🤖 結論與企業未來佈署建議

---

## 🌟 前言：從 GUI 邁向 LUI 與代理人基礎設施

過往二十年間，軟體產業圍繞著「圖形使用者介面 (GUI)」進行優化。企業開發出無數優美的儀表板與 Web 應用程式，吸引使用者點擊與操作。然而，當使用者逐漸習慣利用 AI 助手（如 Claude、Cursor 等）協助處理日常工作時，軟體互動的範式正在發生劇烈轉移——從 GUI 邁向 **自然語言介面 (Language User Interface, LUI)** 。

對於工程師或企業員工而言，「登入網站 -> 尋找按鈕 -> 手動填寫表單」的流程正逐漸被「以自然語言交代任務 -> AI 自動呼叫 API 完成操作」所取代。如果 AI 能幫忙撰寫程式碼，那麼讓 AI 自動執行部署、查詢客戶工單、甚至處理退款，也是順理成章的演進。

然而，傳統的 RESTful API 或 GraphQL 原本是為人類開發者或固定程式碼所設計，缺乏讓 AI 動態探索與理解的情境資訊 (Context)。這正是 **模型上下文通訊協定 (MCP)** 誕生並迅速成為產業標準的原因。

## 🚀 MCP 核心概念：為何解耦 Client 與 Server 是關鍵？

**模型上下文通訊協定 (MCP)** 是一種開放式的標準雙向通訊協定。它的架構本質上實現了 **用戶端 (Client)** 與 **伺服器端 (Server)** 的完美解耦：

- **MCP Client (客戶端)** ：通常整合在 AI 應用程式中（例如 Anthropic Claude Desktop、Cursor IDE、Replit 等），負責將使用者的意圖傳送給 LLM，並接收 LLM 發出的工具呼叫請求。
- **MCP Server (伺服器端)** ：負責包裝企業內部的資料庫、第三方 SaaS API 或內部服務工具，向 Client 揭露可用的工具定義 (Tool Schemas) 與資源 (Resources)。

這種分離架構帶來了三大優勢：
- **降低開發與整合門檻** ：企業無須為每一款 AI Client 單獨編寫整合套件，只需公開標準化的 MCP 伺服器，任何支援 MCP 的 AI 助手都能立即存取。
- **邊界清晰的權限控管** ：敏感的 API 金鑰與資料庫憑證均保留在 MCP 伺服器端，LLM 僅能透過抽象化的工具定義提出申請，無法直接接觸底層憑證。
- **靈活的遠端託管 (Remote MCP)** ：早期的 MCP 伺服器需要使用者在本地端電腦自行安裝與執行；而 Cloudflare 則推動了「遠端 MCP」模式，讓 MCP 伺服器能像網址一樣，透過標準 HTTP/SSE 進行跨網路連線與彈性擴展。

## 💻 Cloudflare 上的 MCP 生態系：十家領先企業的實踐案例

在 Cloudflare MCP 示範日中，共有十家業界領先企業展示了部署於 Cloudflare 全球邊緣網路 (Edge Network) 上的遠端 MCP 伺服器。這些企業充分利用了 Cloudflare Workers 的極速啟動速度與無伺服器 (Serverless) 特性：

- **Asana** ：透過 MCP，Asana 將其 Work Graph 與 AI 代理人串聯。使用者可以在 AI 對話中輸入「幫我確認本週逾期的專案任務」，AI 代理人便能直接查詢 Asana，並自動生成結構化的追蹤清單與指派任務。
- **Atlassian** ：Jira 與 Confluence 開放了遠端 MCP 伺服器。開發者無須離開 AI 開發環境，即可直接查詢產品規格書、總結 Jira Bug 報告，甚至一鍵批量建立工單。
- **Intercom** ：Intercom 將客服 AI 代理人 Fin 與開發端工具對接。工程師在 Cursor 中除錯時，能直接喚醒 MCP 工具調閱特定客戶的真實對話紀錄與報錯背景，讓排錯過程事半功倍。
- **PayPal** ：商家與開發者現在能透過自然語言呼叫 PayPal 的商務 MCP 工具，實現訂單檢索、庫存自動調度與退款審核，將複雜的支付邏輯抽象化為自然語言互動。
- **Sentry** ：開發者能透過 MCP 伺服器讓 AI 直接讀取實時的 Error Logs 與 Stack Trace，AI 不僅能解釋崩潰原因，還能結合程式碼倉庫提出具體的修復 Pull Request。
- **Webflow** ：開放了 CMS 數據管理與網站發布的 MCP 接口，讓行銷人員能透過 AI 自動更新部落格文章、進行多國語言翻譯並一鍵發布上線。

此外，包括 **Stripe** 、 **Linear** 、 **Block** 與 **Anthropic** 等企業，也皆選用 Cloudflare 作為其 MCP 伺服器的最佳託管平台，印證了 Edge Computing 與 MCP 結合的強大潛力。

## 🏗️ 企業級 MCP 參考架構：集中治理與邊緣部署

雖然遠端 MCP 帶來了強大的生產力，但對企業資安與 IT 團隊而言，未受控管的 MCP 部署無疑是重大隱患。典型的安全風險包括：
- **授權擴張 (Authorization Sprawl)** ：員工私自連線外部 MCP 伺服器，導致企業資料未經許可流出。
- **提示詞注入 (Prompt Injection)** ：惡意的第三方 MCP 伺服器可能傳回隱含攻擊指令的工具回覆，劫持 AI 代理人的控制權。
- **版本與稽核失控** ：本地端託管的 MCP 伺服器缺乏中央日誌與更新機制。

為了解決這些問題，Cloudflare 提出了 **企業級 MCP 參考架構** ，採用 **「集中管理、邊緣部署」** 的戰略方針：

{{< mermaid >}}
graph TD
    User[End User] --> Client[MCP Client]
    Client --> AIGateway[Cloudflare AI Gateway]
    AIGateway --> Portal[MCP Server Portal]
    Portal --> Access[Cloudflare Access]
    
    Access --> InternalMCP1[Internal MCP Server 1]
    Access --> InternalMCP2[Internal MCP Server 2]
    Access --> ExternalMCP[Third Party MCP Server]
    
    InternalMCP1 --> DB[Enterprise Database]
    InternalMCP2 --> Jira[Project Management]
    ExternalMCP --> SaaS[Third Party SaaS API]
    
    subgraph Security Governance Layer
        AIGateway
        Portal
        Access
    end
{{< /mermaid >}}

在該架構中，所有內部 MCP 伺服器的開發皆基於標準化範本，託管於 Cloudflare 邊緣平台上，內建預設拒絕 (Default-Deny) 權限控管與CI/CD自動化防護。

## 🛡️ 資安防衛戰：身分驗證、DLP 與影子 MCP (Shadow MCP) 攔截

為了達成零信任 (Zero Trust) 級別的安全維護，Cloudflare 在這套架構中整合了多重安全防禦機制：

### 1. 嚴格的身分驗證與存取控制 (Cloudflare Access)
所有存取內部 MCP 伺服器的連線，必須通過 **Cloudflare Access** 的關卡。系統會強制檢查使用者的 SSO 身分驗證、多因素驗證 (MFA)、IP 地理位置以及設備安全狀態 (Device Posture)。只有通過核准的請求，才能建立 SSE (Server-Sent Events) 連線並呼叫 MCP 工具。

### 2. 流量稽核與機密防護 (MCP Server Portals & DLP)
企業透過 **MCP Server Portals** 為員工提供統一的「MCP 應用商店」。系統會自動檢查所有傳入與傳出的封包，並掛載資料外洩防護 (DLP) 引擎，自動遮蔽傳送給外部 AI 模型的敏感個資 (PII) 或企業機密。

### 3. 影子 MCP (Shadow MCP) 自動偵測與攔截
針對員工可能私自連線未授權遠端 MCP 伺服器的狀況，Cloudflare 利用 Secure Web Gateway (SWG) 在邊緣進行流量深度檢查 (DPI)：
- **主機名標籤過濾 (`httpHost`)** ：鎖定常見的 `mcp.*` 或第三方 MCP 服務網域。
- **路徑過濾 (`httpRequestURI`)** ：比對 `/mcp`、`/mcp/sse` 等標準通訊協定端點。
- **JSON-RPC 封包特徵掃描** ：辨識封包內是否含有 MCP 獨有的 JSON-RPC 語法（如 `tools/call`、`prompts/get` 或 `initialize`），一旦發現未核准的外部連線，即刻進行隔離與告警。

## 💰 突破性的成本優化： Code Mode 如何節省 94% 的 Token

除了安全性之外，規模化部署 MCP 所帶來的 **Token 費用暴漲** ，是企業面臨的另一個現實挑戰。

在傳統的 MCP 模式下，當 AI Client 連接至 MCP 伺服器時，伺服器必須將所有工具的文字說明 (Schemas) 完整放入 LLM 的 Prompt 中。如果企業掛載了數十個 MCP 伺服器、上百個 API 工具，每一次對話光是載入工具定義就會消耗高達數萬個 Tokens，不僅費用昂貴，還會導致模型反應遲鈍。

為了破解這個難題，Cloudflare 研發了全新的 **Code Mode (程式碼模式)** 選擇：

### Code Mode 的運作機制：
1. **工具高度收斂** ：MCP Server Portal 對外只向 AI 模型暴露 **兩個** 核心工具：
   - `portal_codemode_search`：讓 AI 模型以關鍵字動態搜尋並過濾需要用到的工具定義。
   - `portal_codemode_execute`：允許 AI 模型寫出一小段沙盒 JavaScript 程式碼，一次性鏈式呼叫多個 API。
2. **動態載入與沙盒執行** ：AI 模型不再需要一口氣讀取所有 API 說明書，而是透過編寫程式碼，動態探索並在安全的隔離環境中執行運算，最後僅將最終產出結果回傳給模型。

根據 Cloudflare 的實測數據：
- **傳統 MCP 模式** ：暴露 52 個工具需要消耗約 **9,400 個 Tokens** 。
- **Code Mode 模式** ：僅暴露 2 個動態工具， Token 消耗量 **大幅暴跌至大約 600 個** ，成功實現了驚人的 **94% Token 成本節省** ！

更重要的是，這個 Token 消耗量是 **常數等級 ($O(1)$)** 的，無論後端未來擴充到數千個工具，上下文消耗都將維持在極低的水平。

## 🤖 結論與企業未來佈署建議

模型上下文通訊協定 (MCP) 正迅速從一項技術實驗，演變為企業 AI 基礎設施不可或缺的標準配備。它打破了過去數據孤島與 API 整合的困境，真正讓 AI 代理人具備了強大的執行力。

Cloudflare 透過將遠端 MCP 部署在邊緣網路上，結合 Zero Trust、AI Gateway 與 Code Mode，為全球企業提供了一套兼具 **高度安全** 、 **極致效能** 與 **極低成本** 的示範解答。

### 給企業 IT 與架構師的實務建議：
1. **優先選用遠端 MCP (Remote MCP)** ：避免在本地端部署無稽核機制的 MCP 伺服器，改採基於 Serverless 邊緣架構的集中化部署。
2. **建立 Zero Trust 資安邊界** ：結合 SSO/MFA 身分驗證與 SWG 流量掃描，防範影子 MCP 與資料洩漏。
3. **導入 Code Mode 技術** ：在工具數量眾多的複雜情境下，優先採用 Code Mode 進行整合，最大化控制 Token 營運成本。

邁向 AI 代理人的時代已經到來，唯有建立標準化與安全治理兼備的基礎設施，企業才能在保障資安的前提下，全面釋放 AI 的極致生產力！
