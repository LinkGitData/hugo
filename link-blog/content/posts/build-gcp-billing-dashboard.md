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

本專案採用高度標準化的 **前後分離 (Separation of Concerns)** 設計，並透過基礎設施即代碼（IaC）達成全自動化部署。

*   **前端展示**：利用 Flutter Web 與原生 Android App 雙棲架構撰寫，介面狀態以 `provider` 進行管理，並利用 `fl_chart` 提供各月成本的精確報表圖。
*   **後端服務**：奠基於 Python FastAPI 與 Google BigQuery 之間，負責進行複雜的 SQL 分析，將 BigQuery Export 中扁平的成本及折讓明細，清洗為巢狀 JSON 結構。
*   **基礎設施與部署**：透過 Terraform 管理 VPC、Cloud Run 以及 IAM 權限分配。

以下為核心的資料請求流向：

{{< mermaid >}}
graph TD
    User([系統使用者]) -->|1. OAuth 帳號驗證| Auth[Google 驗證]
    User -->|2. 送出查詢請求| Nginx[前端 Flutter 容器 Nginx]
    Nginx -->|3. 通過 IP 白名單| Nginx
    Nginx -->|4. 注入密鑰後轉發 API| Backend[Cloud Run Backend]
    Backend -->|5. Middleware 解析密鑰| FastAPI[FastAPI 核心處理]
    FastAPI -->|6. Gcp_Billing_Export_v1 查詢| BQ[(BigQuery Billing 資料集)]
    BQ -->|7. 回傳成本/折讓資料| FastAPI
    FastAPI -->|8. 回傳階層式 JSON 資料| Nginx
    Nginx -->|9. 產生 Treemap 視覺化| User
{{< /mermaid >}}

## 🖼️ 視覺化成果展示

經過系統轉換後，原先複雜且難以閱讀的 BigQuery 表格，已被轉化為能互動點擊的成本趨勢圖與專案攤提列表，讓我們得以快速追查成本劇增的潛在危機。

*(系統截圖已預先濾除非公然的公司業務資訊)*

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

