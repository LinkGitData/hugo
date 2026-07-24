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

人工智慧的演進已經不僅僅停留在生成文字或圖像，我們正全面邁入 **「代理人時代」** 。要讓 AI 代理人 (AI Agents) 能夠自主地協助我們查詢資料、管理專案、甚至部署完整的堆疊應用程式，關鍵的技術橋樑便是 **模型上下文通訊協定 (Model Context Protocol, 簡稱 MCP)** 。Cloudflare 近期不僅聯手 10 家業界領先的 AI 公司展示了遠端 MCP 伺服器的強大威力，更公開了其內部的企業級 MCP 部署參考架構，展示如何以更安全、更簡單且成本更低的方式來管理 AI 代理人的存取與運作。

本文將帶您深入探討這場由 Cloudflare 引領的 MCP 革命，從業界巨頭的實際應用案例，到企業級資安防護與成本優化的創新架構，為您的開發團隊與企業 IT 規劃提供一份詳盡的參考指南。

## 📋 目錄
1. 🌟 前言：邁入 AI 代理人的新紀元
2. 🚀 MCP 是什麼？為何它能推動下一代應用程式？
3. 💻 Cloudflare 上的 MCP 生態系：十家領先企業的實踐
4. 🏗️ 企業級 MCP 部署：架構、安全與治理
5. 🛡️ 應對安全風險：存取控制與影子 MCP (Shadow MCP)
6. 💰 降低成本的秘密武器：Code Mode 與 MCP Portal
7. 🤖 結論與未來進階

---

## 🌟 前言：邁入 AI 代理人的新紀元

曾幾何時，我們認為每項服務（無論是實體商店還是線上平台）都必須擁有一個網站才能觸及使用者。然而，隨著 Web 使用者逐漸習慣讓 AI 助手（如 Claude）代為完成任務，未來的互動模式可能將徹底改變。當開發者在編寫程式碼時，自然會想到利用 Claude 這樣的 AI 助手來協助；既然它能幫忙寫扣，那麼讓它協助部署程式碼也是理所當然的進展。

這種讓 AI 直接跨平台操作服務的願景，如今已透過 **遠端 MCP (Remote MCP)** 成為現實。在早期，使用者必須在本地端 (Local) 安裝 MCP 伺服器才能使用這項協定；現在，隨著整合技術的突破，使用 MCP 伺服器就如同瀏覽網站一般簡單——只需輸入網址即可連接。

Cloudflare 致力於簡化遠端 MCP 伺服器的開發，並推出了一鍵部署的解決方案。讓工程團隊不必費心於底層協定的管理，而是能將所有心力專注在為應用程式打造具備商業價值的 MCP 工具。

## 🚀 MCP 是什麼？為何它能推動下一代應用程式？

**模型上下文通訊協定 (MCP)** 是一種開放式標準，旨在為 AI 應用程式與其所需存取的資料來源之間，建立一條安全的雙向通道。在這種架構下， **MCP Client (客戶端)** 負責與大語言模型 (LLM) 或 AI 代理人整合，而 **MCP Server (伺服器端)** 則扮演著資料與企業資源的守門員。

這種用戶端與伺服器端分離的設計極具巧思。它允許 AI 代理人自主追求目標並採取行動，同時確保 AI 模型與企業的機密 API、登入憑證之間保持清晰的安全界線。企業如果選擇採用 MCP，將能迅速獲得以下優勢：

- **降低使用門檻** ：使用者不再需要研讀繁雜的使用者手冊或儀表板教學。他們只需以自然語言描述需求，MCP 便會串接 AI 代理人代勞。
- **打造高度個人化體驗** ：MCP 能夠追蹤使用者的請求與互動模式，未來的工具呼叫將自動適應使用者的偏好，提供精準的客製化服務。
- **零阻力的功能升級與整合** ：開發者無須在內部自行打造所有的第三方整合。只要透過 MCP 公開工具，AI 代理人就能自動組合不同供應商的服務，實現無縫協作。

## 💻 Cloudflare 上的 MCP 生態系：十家領先企業的實踐

在近期的 MCP 示範日中，Cloudflare 宣布與十家業界頂尖企業合作，推出了全新系列的遠端 MCP 伺服器。這些企業皆選擇將基礎架構架設於 Cloudflare 之上，以確保低延遲、高安全性與無縫擴展的能力。以下是幾個亮眼的實踐案例：

- **Asana** ：透過 MCP，Asana 讓 AI 工具（如 Claude）能直接與其 Work Graph 互動。使用者能以自然語言查詢專案進度、指派任務，甚至將會議記錄瞬間轉化為結構化的待辦清單，大幅消除了應用程式間切換的摩擦力。
- **Atlassian** ：Jira 與 Confluence 的用戶現在可以透過遠端 MCP 伺服器，直接在 AI 對話中總結工作項目、批量建立工單。這不僅豐富了開發背景資訊，還確保了資料始終遵守嚴格的權限邊界。
- **Intercom** ：其 AI 代理人 Fin 已能自動解決超過一半的客服對話。藉助 MCP，工程師可以在 Cursor 等開發工具中，直接調閱使用者的對話歷程紀錄，這讓除錯與分析的過程變得精準且高效。
- **PayPal** ：作為支付巨頭，PayPal 透過 MCP 賦予了開發者利用自然語言呼叫商務功能的能力。從庫存管理、付款處理到退款追蹤，AI 代理人都能自主優化並執行商業工作流程。
- **Sentry 與 Webflow** ：Sentry 允許開發者透過 MCP 查詢環境錯誤與根本原因分析；而 Webflow 則開放了 CMS 管理、內容在地化與網站發佈的動作。他們都深刻體會到，將 MCP 託管於 Cloudflare 邊緣網路，能有效避開本地端執行的驗證與擴展難題。

## 🏗️ 企業級 MCP 部署：架構、安全與治理

儘管 MCP 帶來了極大的便利性，但在企業內部廣泛部署時，不可避免地會面臨諸多資安挑戰。例如授權擴張 (Authorization Sprawl)、提示詞注入 (Prompt Injection) 以及供應鏈攻擊 (Supply Chain Attacks) 等風險。

為了保障全公司的 MCP 應用安全，Cloudflare 設計了一套整合式的內部架構。他們發現， **本地端託管 (Local Hosting)** 的 MCP 伺服器往往缺乏有效的審核機制，這會讓企業 IT 管理員難以管控版本與更新，形同門戶洞開。因此，Cloudflare 採用了 **「集中管理、邊緣部署」** 的策略。

透過使用 Cloudflare Developer Platform，他們建立了一個共享的 MCP 平台。當員工需要將內部資源透過 MCP 開放給 AI 使用時，必須先取得 AI 治理團隊的核准，接著使用標準化的範本進行部署。這套機制自動內建了預設拒絕 (Default-Deny) 的寫入控制、稽核日誌 (Audit Logging)、CI/CD 管道與機密管理 (Secrets Management)。部署完成後，這些遠端 MCP 伺服器會分發到全球的資料中心，確保所有員工皆能享有低延遲的存取體驗。

以下為 Cloudflare 企業級 MCP 部署的參考架構圖解：

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

## 🛡️ 應對安全風險：存取控制與影子 MCP (Shadow MCP)

在此架構中，資安防護被分為幾個核心層次。首先，所有需要存取企業內部資源的 MCP 伺服器，都會與 **Cloudflare Access** 進行身分驗證整合。Cloudflare Access 扮演了單一登入 (SSO) 與多因素驗證 (MFA) 的聚合器，同時分析 IP 位址與裝置憑證，確保只有經過授權的員工才能喚醒對應的 MCP 伺服器。

此外，隨著遠端 MCP 伺服器數量的增加，員工可能會面臨 **「發現困難 (Discovery)」** 的問題。為此，Cloudflare 推出了 **MCP Server Portals** 功能。入口網站不僅能統一揭露員工有權限使用的伺服器清單，還能強制執行資料外洩防護 (DLP) 規則。管理員可以設定規則，防止敏感個資 (PII) 透過某些特定工具傳送給外部大模型。

但防堵了合法的管道，還必須抓出未經核准的 **影子 MCP (Shadow MCP)** 行為。員工可能會私自連線至未經授權的遠端 MCP 伺服器。對此，Cloudflare 利用其 Secure Web Gateway 功能，針對企業網路流量進行深度掃描：
- 利用 `httpHost` 篩選器監控常見的 MCP 伺服器主機名稱（例如 `mcp.*` 子網域）。
- 利用 `httpRequestURI` 篩選器尋找帶有 `/mcp` 或 `/mcp/sse` 的 URL 路徑。
- 利用 DLP 內容檢查，掃描 HTTP 封包內容。由於 MCP 使用 JSON-RPC 協定，因此系統會尋找包含 `tools/call`、`prompts/get` 或 `initialize` 等特徵欄位的請求，精準攔截違規連線。

## 💰 降低成本的秘密武器：Code Mode 與 MCP Portal

當您大規模部署 MCP 時，還有一個無法忽視的問題： **Token 消耗成本** 。

傳統的 MCP 運作方式，會要求伺服器將所有可用的工具定義 (Schemas) 一次性傳送給 AI 代理人。如果一個 MCP 伺服器背後連接著數千個 API 端點，光是傳輸這些「說明書」，就會瞬間耗盡大語言模型的上下文視窗 (Context Window) 與高昂的 Token 額度。

為了解決這個痛點，Cloudflare 創造了顛覆性的 **Code Mode (程式碼模式)** 。

在 Code Mode 之下，無論後端有多少台 MCP 伺服器與數百個工具，MCP Server Portal 對 AI 模型都只會暴露兩個工具：
1. `portal_codemode_search`：AI 模型可以透過編寫 JavaScript，動態搜尋並過濾後端所有可用的工具定義。
2. `portal_codemode_execute`：AI 模型撰寫 JavaScript 腳本，透過代理物件直接呼叫目標工具。它能在沙盒環境中串接多個操作、處理錯誤，最後只回傳必要的結果給模型。

這項創新讓驚人的 Token 消耗大幅縮水。在 Cloudflare 的內部測試中，原本暴露 52 個工具需要消耗約 9,400 個 Tokens；啟動 Code Mode 後，僅需提供上述兩個工具，Token 消耗量 **斷崖式下降至大約 600 個 (節省高達 94%)** 。更棒的是，這個成本是固定的，未來就算連接更多 MCP 伺服器，Token 消耗也不會隨之暴增。

## 🤖 結論與未來進階

MCP 正在快速成為一種嶄新的 AI 使用者介面。在不久的將來，它極有可能成為人類、企業與程式碼探索服務的預設途徑。

透過將 AI 代理人的客戶端與資料存取的伺服器端完美解耦，企業能夠兼顧 AI 驅動的自動化效率與極致的資訊安全。Cloudflare 透過其 AI Gateway、Cloudflare Access 與 MCP Server Portals，為業界示範了一套可行、安全且具備高度成本效益的企業級部署藍圖。

如果您或您的團隊也正準備擁抱 AI 代理人的未來，現在正是利用這套架構建立專屬遠端 MCP 伺服器的最佳時機。無論是自動化 DevOps 流程、解放客服資料庫的價值，還是讓 AI 幫忙審閱架構設計，標準化與安全治理將是您脫穎而出的關鍵。

> 💡 **經驗分享**：在著手建置 MCP 伺服器時，請務必先將安全與驗證機制納入考量。您可以嘗試使用 Cloudflare 提供的遠端 MCP 快速入門範本，親身體驗零伺服器 (Serverless) 與休眠模式帶來的靈活度與成本優勢。
