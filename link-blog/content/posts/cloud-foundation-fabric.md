---
title: "打造企業級雲端地基：Google Cloud Foundation Fabric (CFF) 實戰解析"
date: 2026-05-13T15:49:23+08:00
draft: false
tags: ["Google Cloud", "Terraform", "Infrastructure as Code", "Landing Zone", "Cloud Architecture"]
categories: ["Tech", "Web Development"]
mermaid: true
cover:
  image: "images/cloud-foundation-fabric-cover.png?v=1"
  alt: "Google Cloud Foundation Fabric Architecture Concept"
  caption: "利用 Cloud Foundation Fabric 打造安全且可擴充的雲端 Landing Zone"
  relative: false
---

> 🔗 **官方資料來源**：[Google Cloud Foundation Fabric GitHub](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric)

當企業將龐大業務遷移至雲端時，平台工程師最常面臨的夢魘便是：「如何為不同的團隊建立一致、安全且具備完善權限隔離的雲端環境？」如果每次開設新專案都必須手刻 Terraform 腳本，不僅耗時，更容易因為人為疏失導致資安破口。

為了解決這個痛點，Google 官方推出了開源的 **Cloud Foundation Fabric (CFF)**。它被譽為建構 GCP 基礎建設的「瑞士刀」，能幫助開發團隊以前所未有的速度與標準，部署具備企業級安全護欄的 Landing Zone。

## 📋 目錄
1. [什麼是 Cloud Foundation Fabric？](#-什麼是-cloud-foundation-fabric)
2. [核心架構解析：FAST 與模組化工廠](#-核心架構解析fast-與模組化工廠)
3. [架構生命週期圖解](#-架構生命週期圖解)
4. [實戰範例：告別落落長的 Terraform 腳本](#-實戰範例告別落落長的-terraform-腳本)
5. [適合哪些團隊與情境？](#-適合哪些團隊與情境)
6. [結論與未來進階](#-結論與未來進階)

## 🌟 什麼是 Cloud Foundation Fabric？

**Cloud Foundation Fabric** 是一個由 Google 維護的開源基礎設施即程式碼 (IaC) 工具包。它的核心理念在於「不要重複造輪子」。透過提供一系列經過實戰測試的 Terraform 模組 (Modules) 與端到端藍圖 (Blueprints)，它讓基礎架構的部署變得像樂高積木一樣靈活。

CFF 不僅僅是一堆程式碼，它更直接將 Google 的最佳實踐（包含 IAM 群組管理、資源階層設計、集中式 Logging）內建於架構中，天然支援 GitOps 的開發工作流。

## 🏗️ 核心架構解析：FAST 與模組化工廠

整個 CFF 框架可以拆解為三個最具威力的核心元件：

1.  **Module (基礎模組)**：CFF 提供了超過 87 個涵蓋所有核心雲端服務的 Terraform 模組。這些模組設計簡潔、具備高可讀性，開發者可以直接呼叫，省去從零開始撰寫底層邏輯的時間。
2.  **Factory (專案工廠)**：面對大規模的資源管理，CFF 引入了 YAML 驅動的設計。您只需要修改 YAML 設定檔，系統就會自動批量生成對應的專案、資料夾與網路設定，大幅降低 Terraform 語法的維護門檻。
3.  **Fabric FAST (快速落地藍圖)**：這是 CFF 最受矚目的旗艦藍圖。它提供了一個「工廠化」的方法來引導企業完成 GCP 組織的初始設定。FAST 將建置過程劃分為多個明確的階段（包含 Bootstrap、資源層級、安全性、網路拓樸），確保安全優先。

## 💻 架構生命週期圖解

我們可以透過 Fabric FAST 的運作流程，了解一個企業級 Landing Zone 是如何被分階段建立出來的：

{{< mermaid >}}
graph TD
  Start[啟動 Fabric FAST] --> Bootstrap[階段一 Bootstrap 核心基座]
  Bootstrap --> CICD[建立 CI 與 CD 自動化管線]
  CICD --> ResMan[階段二 資源層級與 IAM 管理]
  ResMan --> Network[階段三 企業級網路架構與安全]
  Network --> ProjectFactory[階段四 專案工廠 Project Factory]
  ProjectFactory -->|YAML設定| AppEnvA[應用程式環境 A]
  ProjectFactory -->|YAML設定| AppEnvB[應用程式環境 B]
{{< /mermaid >}}

> 💡 **經驗分享**：在 FAST 架構中，原生就支援了 **Workload Identity Federation**，這意味著您的 CI/CD 管線（如 GitHub Actions）無需依賴長效型金鑰即可安全地部署資源。

## 📝 實戰範例：告別落落長的 Terraform 腳本

為了讓您更有感，我們來比較一下「傳統寫法」與「使用 CFF 模組」建立一個 GCP 專案的差異。

假設我們要建立一個專案、啟用幾個 API，並指派一個 Viewer 權限群組：

> 🤖 **Agent Prompt**: 傳統上，您必須寫三種不同的 Terraform Resource：`google_project`, `google_project_service` 以及 `google_project_iam_member`。若有十幾個 API 和權限，程式碼會變得非常冗長。

但有了 **CFF 的 Project Module**，一切變得如此優雅：

```terraform
module "project" {
  source          = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/project?ref=v31.0.0"
  billing_account = "123456-123456-123456"
  name            = "my-new-app-prod"
  parent          = "folders/1234567890"
  
  # 統一在這裡開啟所需服務
  services = [
    "compute.googleapis.com",
    "container.googleapis.com"
  ]
  
  # IAM 權限指派也整合在同一個模組內
  iam = {
    "roles/viewer" = ["group:app-viewers@example.com"]
  }
}
```

如您所見，CFF 將底層的複雜度完美封裝。您只需專注於宣告「您想要什麼」，而不必去管底層元件如何拼湊，這就是它能大幅提升維護性的秘密。

## 🚀 適合哪些團隊與情境？

Cloud Foundation Fabric 的高彈性讓它能適應各種規模的組織：

*   **大型企業 (Enterprise)**：需要快速落地企業級 Landing Zone，規劃複雜的跨部門 IAM 權限與嚴格的資源隔離設計。
*   **新創團隊 (Startup)**：專案需要快速啟動。透過 Project Factory 搭配 YAML，能瞬間開出新專案並自動套用標準的網路與安全護欄，減少重複性的苦工。
*   **平台開發者 (Developer)**：無需再煩惱 Terraform 的目錄結構設計。直接借用 CFF 內成熟的模組，並 Fork 一份客製化版本以符合公司內部政策，能大幅提升程式碼品質。

## 🤖 結論與未來進階

總結來說， **Cloud Foundation Fabric** 能讓雲端組織建設變得更快、更安全、也更易於維護。它採用的 Apache 2.0 授權讓企業能放心將其應用於商業環境中。

如果您是雲端架構師或平台工程師，強烈建議您前往官方 GitHub Repository 進行 Clone。您可以先從最基礎的 Module 開始試用，等熟悉後再導入 Fabric FAST 來重構整體的 Landing Zone，讓基礎設施管理邁入現代化的自動化境界！
