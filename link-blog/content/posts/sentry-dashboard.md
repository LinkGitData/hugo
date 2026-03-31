---
title: "雲地混合架構：Sentry 全鏈路監控"
date: 2026-03-31T12:20:00+08:00
draft: false
tags: ["Sentry", "Observability", "Cloud Native", "Architecture"]
categories: ["Architecture"]
mermaid: true
cover:
  image: "images/sentry-cover.png?v=1"
  alt: "Sentry 全鏈路監控"
  caption: "前端部署於雲端，後端部署於在地機房的監控整合方案"
  relative: false
---

這篇筆記探討了如何利用 **Sentry** 來實現**前端部署於雲端 (Cloud)**、**後端部署於在地機房 (On-Premise)** 的全鏈路監控整合方案。

## 📋 目錄

1. [系統架構](#系統架構)
2. [前端能做什麼？(雲端)](#前端能做什麼雲端)
3. [後端能做什麼？(在地)](#後端能做什麼在地)
4. [雲地串聯：分散式追蹤 (Distributed Tracing)](#雲地串聯分散式追蹤-distributed-tracing)

---

## 系統架構

以下是結合雲端前端與在地後端的監控系統資料流與架構：

{{< mermaid >}}
graph TD
    %% 定義樣式
    classDef cloud fill:#e0f2fe,stroke:#38bdf8,stroke-width:2px;
    classDef onprem fill:#dcfce7,stroke:#4ade80,stroke-width:2px;
    classDef sentry fill:#f3e8ff,stroke:#c084fc,stroke-width:2px;
    classDef team fill:#fef3c7,stroke:#fbbf24,stroke-width:2px;

    subgraph Cloud ["☁️ 雲端環境 (Cloud Frontend)"]
        User("👤 使用者 (Browser/App)")
        FE("🖥️ 前端應用 (React/Vue)<br /><span style='font-size:12px;color:#666'>捕捉 UI 崩潰、效能指標</span>")
        User -- "點擊 / 頁面載入" --> FE
    end
    class Cloud cloud;

    subgraph OnPrem ["🏢 在地機房 (On-Premise Backend)"]
        BE("⚙️ 後端 API 伺服器<br /><span style='font-size:12px;color:#666'>捕捉 API 報錯、CPU 瓶頸</span>")
        DB("🗄️ 在地資料庫<br /><span style='font-size:12px;color:#666'>監控 SQL 查詢耗時</span>")
        BE -- "資料讀寫" --> DB
    end
    class OnPrem onprem;

    subgraph SentryHub ["👁️ Sentry 監控平台 (SaaS 或在地部署)"]
        S_Trace("🔗 分散式追蹤<br />(Distributed Tracing)")
        S_Error("🐛 錯誤聚合<br />(Error Tracking & Source Maps)")
        S_Replay("🎬 操作回放<br />(Session Replay)")
    end
    class SentryHub sentry;

    subgraph Team ["👥 開發與運維團隊"]
        Alerts("🚨 警報系統<br />(Slack/Teams/Email)")
        Jira("📋 工單系統<br />(Jira/GitHub)")
        Alerts -.-> Jira
    end
    class Team team;

    %% 跨環境連線
    FE <-->|"1. API 請求 (Header 夾帶 sentry-trace ID)"| BE

    %% 數據上報連線
    FE -.->|"2. 前端報錯、錄影、Web Vitals"| SentryHub
    BE -.->|"3. 後端 Exception、SQL 耗時、過濾敏感數據"| SentryHub

    %% Sentry 內部關聯
    S_Error --- S_Trace
    S_Replay --- S_Error

    %% 告警連線
    SentryHub -.->|"4. 觸發規則 (如：在地 API 500 錯誤激增)"| Alerts
{{< /mermaid >}}

---

## 前端能做什麼？(雲端)

* **✅ 錯誤還原：** 搭配 Source Maps，將雲端壓縮過的程式碼還原，精準定位報錯的行數。
* **✅ 操作回放 (Session Replay)：** 錄製用戶報錯前的滑鼠軌跡與點擊，重現「雲端特定裝置/瀏覽器」才發生的玄學 Bug。
* **✅ Web Vitals 監控：** 監測雲端分發到全球用戶的 LCP, FID 等載入效能體驗。

---

## 後端能做什麼？(在地)

* **✅ 效能剖析 (Profiling)：** 找出在地伺服器中，哪一段函數寫法導致 CPU 飆高或資源卡頓。
* **✅ 資料庫查詢監控：** 記錄慢查詢 (Slow SQL)，辨識是網路延遲還是在地資料庫缺少 Index。
* **✅ 隱私數據脫敏 (Scrubbing)：** 在數據傳出機房前，利用 `beforeSend` 攔截並清除 PII (如身份證、真實 IP)。

---

## 雲地串聯：分散式追蹤 (Distributed Tracing)

> 這是解決「雲端前端」與「在地後端」分離痛點的核心技術。

**運作原理：**
前端在雲端發起請求時，Sentry 會在 HTTP Header 自動加入 `sentry-trace` 與 `baggage`。

**價值：**
當使用者抱怨「系統好慢」，你可以在 Sentry 介面上看到一條完整的時間軸：

1. 用戶點擊按鈕 (前端) ➡️ 網路傳輸耗時 (雲地連線) ➡️ API 驗證 (後端) ➡️ SQL 查詢 (在地 DB)。
2. **秒懂瓶頸：** 一眼看出卡頓是發生在「跨網段傳輸」，還是「在地資料庫死鎖」。
