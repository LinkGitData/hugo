---
title: "企業級 GCP 帳單分析平台：從零打造高安全性的視覺化內部系統"
date: 2026-04-08T14:54:25+08:00
draft: false
tags: ["GCP", "Flutter", "FastAPI", "Terraform", "Cloud Run"]
categories: ["Web Development"]
mermaid: true
cover:
  image: "images/gcp-billing-dashboard-cover.png?v=2"
  alt: "A clean, modern enterprise dashboard"
  caption: "Building an Enterprise Billing Dashboard on Google Cloud"
  relative: false
---

企業在雲端資源的規模逐漸擴展後，原生的 GCP 帳單後台往往無法滿足精細的「專案、服務、月份」攤提與成本分析需求。本篇文章將完整解析我們如何透過微服務架構，利用 Terraform、FastAPI 與 Flutter Web 開發出一套專供內部網域使用的高安全性 GCP 帳單視覺化平台。

## 📋 目錄
1. [🏗️ 核心技術與微服務架構](#-核心技術與微服務架構)
2. [🖼️ 視覺化成果展示](#-視覺化成果展示)
3. [💡 實踐中的關鍵挑戰與解法](#-實踐中的關鍵挑戰與解法)
4. [🔒 企業級的多層次資安架構](#-企業級的多層次資安架構)
5. [🚀 結論與未來進階](#-結論與未來進階)

## 🏗️ 核心技術與微服務架構

本專案採用高度標準化的 **前後分離 (Separation of Concerns)** 與 **微服務 (Microservices)** 架構。所有的基礎設施皆透過 **Terraform (IaC)** 進行定義，確保環境的可移植性與安全性。

### 📁 模組化職責拆解

1.  **前端展示層 (`frontend/`)**：
    *   **技術選型**：採用 **Flutter Web** 驅動，利用同一套 Dart 邏輯兼顧 Android App 版本的開發，實現「一份程式碼，多端部署」。
    *   **狀態與圖表**：使用 `provider` 進行全局狀態管理，並整合 `fl_chart` 與 `syncfusion_flutter_treemap` 繪製高互動性的 Treemap 樹狀圖與折線圖。
    *   **容器化設計**：以前端 Nginx 容器作為入口，除了提供靜態資源，亦扮演 **Reverse Proxy** 的角色，負擔 IP 白名單檢查並在轉發 API 請求時自動注入中繼憑證。

2.  **後端邏輯層 (`backend/`)**：
    *   **高效能開發**：基於 Python **FastAPI** 框架，利用 Pydantic 進行嚴格的參數驗證與資料模型定義，提供標準的 RESTful API。
    *   **大數據分析**：作為 Google **BigQuery Client**，後端負責執行複雜的 SQL 彙整語句。它能將 GCP 原始匯出的扁平化（Flat）帳單列 (Raw Rows)，清洗與轉換為以 `Project -> Service -> MonthlyCost` 為階層的巢狀 JSON 結構。
    *   **安全性 Middleware**：實作自定義中繼軟體，強制校驗請求標頭中的 `X-Service-Secret`，確保所有 API 呼叫皆來自受信任的前端代理。

3.  **基礎設施層 (`terraform/`)**：
    *   **資源管理**：透過 Terraform 自動化配置 **Artifact Registry** (映像檔倉庫)、**VPC 專用網路**與子網。
    *   **Serverless 部署**：將服務部署於 **Google Cloud Run**。後端設定為 `INTERNAL_ONLY` 模式，而前端則配置 **VPC Access Connector**，建立起一條專屬的內部加密通道與後端通訊。

### 📊 系統資料流向圖

以下是從用戶登入到呈現視覺化報表的完整請求生命週期：

{{< mermaid >}}
graph TD
    User([系統使用者]) -->|1. OAuth 登入驗證| Auth[Google OAuth colatour.com.tw]
    User -->|2. 送出查詢請求| Nginx[前端 Flutter 容器 Nginx]
    subgraph Frontend Container
        Nginx -->|3. 檢查 allowed_ips.conf| Nginx
        Nginx -->|4. 注入 X-Service-Secret| Proxy[Reverse Proxy]
    end
    Proxy -->|5. 透過 VPC Connector 轉發| Backend[Cloud Run Backend]
    subgraph Backend Service
        Backend -->|6. Middleware 秘鑰檢查| FastAPI[FastAPI 核心處理]
        FastAPI -->|7. BigQuery SQL 彙整查詢| BQ[(GCP Billing Export v1)]
    end
    BQ -->|8. 回傳成本/折讓資料| FastAPI
    FastAPI -->|9. 封裝 JSON 結構| Proxy
    Proxy -->|10. fl_chart / Treemap 渲染| User
{{< /mermaid >}}

## 🖼️ 視覺化成果展示

經過系統轉換後，原先複雜且難以閱讀的 BigQuery 表格，已被轉化為能互動點擊的成本趨勢圖與專案攤提列表，讓我們得以快速追查成本劇增的潛在危機。


![GCP Billing Dashboard](/images/gcp-billing-dashboard-anonymized.png?v=2)

## 💡 實踐中的關鍵挑戰與解法

在為期數個月的專案開發與維護過程中，我們遇到了許多針對雲端架構的技術門檻與挑戰：

### 1. Cloud Run 部署 403 Forbidden 問題
當時嘗試將 Cloud Run IAM 的存取從測試的 `allUsers` 縮限至嚴密的帳戶存取時，遭遇了惱人的 API 阻斷問題。
> 💡 **經驗分享**：部署 Cloud Run 時，必須確認服務憑證 (Service Account) 是否經過適當串接。我們透過將 `backend_invoker` 角色限定發給前端 `billing-frontend-sa`，同時配合自定義 HTTP 標頭 (`X-Service-Secret`) 來雙重保證調用的合法性。

### 2. Terraform 銷毀保護 (Deletion Protection) 卡關
專案更新時，Terraform 因為 Cloud Run 發生異動，提示了 `Error: cannot destroy service without setting deletion_protection=false and running terraform apply`。此時必須先更新 `main.tf` 狀態檔，才能釋放資源鎖。

```bash
# 修正 main.tf 後重新 Apply 解除 State 保護
terraform apply -target=google_cloud_run_v2_service.default
```

### 3. Flutter Web 退化或編譯版本衝突
在升級 `fl_chart` 後因為 `MaterialColor.withValues` 對新舊 Dart 編譯版本的不相容產生報錯。透過獨立的 `android_app/` 目錄隔離設定，順利區分跨平台前端的打包邏輯。

## 🔒 企業級的多層次資安架構

這類掌管企業「成本命脈」的內部系統絕對必須極度嚴謹。我們實踐了以下幾道防線：

1.  **VPC 網路層隔離**：透過 Terraform 將後端 Cloud Run 的 `ingress` 設定為 `INGRESS_TRAFFIC_INTERNAL_ONLY`，完全拒絕外部網路直連。
2.  **前端網域嚴格管控**：前臺的 Google OAuth 網域鎖定 `colatour.com.tw`。
3.  **前端容器白名單防護**：Nginx 層實作了 `allowed_ips.conf`。透過 Terraform 在啟動階段將靜態環境變數載入，封鎖來自外部的非預期流量。
4.  **Middleware 中繼檢查**：公司內網即使與 VPC 互通，未持有正確的 `X-Service-Secret` 的第三方微服務也將不被允許調用內部成本系統的 API 節點。

> 🤖 **Agent Prompt**: 撰寫 Nginx 反向代理並自動注入 Header 配置時，可以直接請 AI 將 `proxy_set_header X-Service-Secret $BACKEND_SECRET;` 結合 Docker `envsubst` 做一次性的打包宣告，這是管理這類無狀態連線中最好運用的技巧。

## 🚀 結論與未來進階

從 Terraform IAM 控制到 FastAPI 中繼驗證，整套方案利用了 GCP 雲端原生生態系的最佳資安實踐。未來如果業務繼續擴大，可以將此流程對接至 Pub/Sub，進階發展出即時成本突增 (Cost Anomaly) 預警機器人。

