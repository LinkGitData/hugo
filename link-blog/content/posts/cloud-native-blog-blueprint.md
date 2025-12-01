---
title: "🚀 Google Antigravity 實作實驗室：Agent-First 雲原生部落格部署指南"
date: 2025-11-28T17:42:24+08:00
draft: false
tags: ["Antigravity", "Hugo", "GCP", "Terraform", "Cloud Run"]
mermaid: true
---

本手冊紀錄了如何利用 Google Antigravity 的 Agent 能力，在不手寫大量設定檔的情況下，快速重現「雲端原生部落格終極藍圖」架構。我們從零打造了一個基於 Hugo、Docker (Chainguard)、Terraform 與 Cloud Run 的高可用性部落格系統。

## 📋 目錄

1. [專案簡介與架構](#1-專案簡介與架構)
2. [先決條件](#2-先決條件)
3. [階段 1：環境初始化與專案建置](#3-階段-1環境初始化與專案建置)
4. [階段 2：容器化與本地預覽](#4-階段-2容器化與本地預覽)
5. [階段 3：基礎設施即代碼 (Terraform)](#5-階段-3基礎設施即代碼-terraform)
6. [階段 4：CI/CD 自動化管線](#6-階段-4cicd-自動化管線)
7. [階段 5：驗證與體驗](#7-階段-5驗證與體驗)
8. [清理資源](#8-清理資源)

---

## 1. 專案簡介與架構

本實驗室透過 Antigravity Agent 協調以下技術堆疊，實現 100% 代碼管理與自動化部署：

*   🎨 **應用層**：Hugo (靜態網站生成器) + Congo Theme (Tailwind CSS)
*   🔒 **容器層**：Multi-stage Build + Chainguard Nginx Images (最小權限安全性)
*   🏗️ **基礎設施層**：Terraform (IaC) 管理 Cloud Run, Artifact Registry, Load Balancer, CDN
*   ⚡ **開發流程**：Agent 驅動的本地熱重載 (Hot-reload) 與 GitOps 自動化

### 架構流程圖

{{< mermaid >}}
graph TD
    User[Developer / Antigravity] -->|Git Push| GitHub[GitHub Repository]
    GitHub -->|Trigger| CB[Cloud Build]
    
    subgraph CI/CD Pipeline
        CB -->|Build| Docker[Docker Image]
        Docker -->|Push| AR[Artifact Registry]
        CB -->|Deploy| CR[Cloud Run Service]
    end
    
    subgraph Infrastructure
        LB[Global Load Balancer] -->|Traffic| CR
        CR -->|Pull Image| AR
    end
    
    PublicUser[Public User] -->|HTTPS| LB
{{< /mermaid >}}

## 2. 先決條件

在開始之前，請確保您已具備以下條件：

- [x] **Google Antigravity IDE**：已安裝並更新至最新版本。
- [x] **Google Cloud Platform (GCP) 帳號**：擁有一個已啟用帳單 (Billing) 的專案 (`linklin-lab`)。
- [x] **Antigravity 設定**：已切換至 Enterprise Mode。已連結目標 GCP 專案。

## 3. 階段 1：環境初始化與專案建置

🎯 **目標**：讓 Agent 準備開發環境並生成 Hugo 網站骨架。

### 實作細節

1.  **API 啟用**：啟用了 Cloud Run, Artifact Registry, Cloud Build, Compute Engine。
2.  **Hugo 站點**：建立了 `link-blog` 專案，並設定 `Congo` 主題。
3.  **Git 初始化**：初始化了 Git Repository 並推送到 GitHub (`LinkGitData/hugo`)。

## 4. 階段 2：容器化與本地預覽

🎯 **目標**：生成符合安全最佳實踐的 Dockerfile 並進行本地測試。

### 實作細節

我們使用了 **Multi-stage build** 來優化映像檔大小與安全性：

1.  **Build Stage**: 使用 `klakegg/hugo:ext-alpine` 生成靜態檔案。
2.  **Run Stage**: 使用 `cgr.dev/chainguard/nginx:latest` 提供服務。
3.  **配置**: Nginx 設定為監聽 `$PORT` 環境變數，符合 Cloud Run 要求。

## 5. 階段 3：基礎設施即代碼 (Terraform 生成)

🎯 **目標**：由 Agent 生成定義 Cloud Run、Load Balancer 與 CDN 的 Terraform 代碼。

### 實作細節

我們在 `infra/` 目錄下建立了 Terraform 設定，並成功部署了以下資源：

*   **Artifact Registry**: `link-blog-repo`
*   **Cloud Run Service**: `link-blog-service`
*   **Load Balancer**: Global External HTTPS Load Balancer (含 Cloud CDN)
*   **Backend State**: 使用 GCS Bucket `linklin-lab-tfstate` 儲存 Terraform 狀態。

> 💡 **經驗分享**：在初始化 Terraform 時，我們遇到了 GCS 權限問題，通過 `gcloud auth application-default login` 重新驗證解決。

## 6. 階段 4：CI/CD 自動化管線

🎯 **目標**：設定 GitOps 流程，讓 Git Push 自動觸發 Cloud Build 進行部署。

### 實作細節

1.  **Cloud Build 設定**: 建立了 `cloudbuild.yaml`，定義了 Build -> Push -> Deploy 流程。
2.  **GitHub 連結**: 這是關鍵的一步。我們需要在 GCP Console 中手動將 GitHub Repository (`LinkGitData/hugo`) 連結到 Cloud Build。
3.  **觸發器 (Trigger)**: 設定了 `link-blog-trigger`，當 `main` 分支有 Push 時自動觸發。

> ⚠️ **重要提示**：Cloud Build 的 GitHub Repository 連結必須在 GCP Console 中手動完成，無法完全透過 CLI 自動化。

## 7. 階段 5：驗證與體驗

🎯 **目標**：確認全域部署成功，並體驗「熱重載」開發流程。

### 驗證結果

*   **本地預覽**: `localhost:1313` 成功運行。
*   **雲端部署**: Cloud Run 服務已上線，並透過 Load Balancer 提供服務。
*   **CI/CD**: 推送代碼到 GitHub 後，Cloud Build 自動觸發並更新了服務。

## 8. 清理資源

🛑 **警告**：為避免產生不必要的 GCP 費用，實驗結束後請務必清理資源。

```bash
cd infra
terraform destroy
```

---

*文件版本: 1.1 | 更新日期: 2025-11-28*
