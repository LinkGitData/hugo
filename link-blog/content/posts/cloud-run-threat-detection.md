---
title: "Google Cloud Run Threat Detection (CRTD) 實戰指南：無伺服器架構的零信任防護"
date: 2026-04-16T17:16:19+08:00
draft: false
tags: ["Google Cloud", "Cloud Run", "Security", "CRTD", "Serverless"]
categories: ["Tech"]
mermaid: true
cover:
  image: "images/cloud-run-crtd-cover.png?v=1"
  alt: "Cloud Run Threat Detection Cover"
  caption: "Cloud Run Threat Detection 全網域防護與遙測架構"
  relative: false
---

無伺服器運算 (Serverless Computing) 雖然解放了維運團隊的雙手，但也帶來了全新的資安盲點。傳統的防火牆與身分驗證僅能守住「邊界 (The Perimeter)」，但在 Cloud Run 這樣的容器化無伺服器應用中，執行階段 (Runtime) 的內部行為卻宛如黑盒子。

這篇指南將帶你深入了解 Google Cloud 推出的 **Cloud Run Threat Detection (CRTD)** 工具，一次搞懂它如何透過原生整合與 gVisor 技術，實現容器內部的全方位防護。

## 📋 目錄

1. [🌟 無伺服器運算的資安盲點：邊界防禦還不夠](#-無伺服器運算的資安盲點邊界防禦還不夠)
2. [🏗️ 什麼是 Cloud Run Threat Detection (CRTD)？](#-什麼是-cloud-run-threat-detection-crtd)
3. [💻 技術架構解密：Watcher 與遙測機制](#-技術架構解密watcher-與遙測機制)
4. [🤖 偵測模組詳解](#-偵測模組詳解)
5. [🚀 結論與未來進階](#-結論與未來進階)

---

## 🌟 無伺服器運算的資安盲點：邊界防禦還不夠

在典型的防禦機制中，我們通常依賴 Cloud Armor 阻擋外部惡意流量，或透過 IAM 與 VPC Service Controls 進行存取控制。這些「邊界防禦」確實有效，卻無法看見容器內部的行為。

當應用程式存在漏洞，攻擊者可能成功繞過外部防線並在 Container 內部執行惡意代碼，此時，防禦就必須轉向 **「執行階段 (The Runtime)」** 的可視性挑戰。

> 💡 **經驗分享**：傳統在虛擬機 (VM) 或 Kubernetes 內安裝 DaemonSet 或代理程式 (Agent) 的做法，大多不適用於 Cloud Run 等 Serverless 服務。這正是原生防護機制不可或缺的主因。

---

## 🏗️ 什麼是 Cloud Run Threat Detection (CRTD)？

CRTD 是 Google Cloud Security Command Center (SCC) Premium / Enterprise 版本提供的強大內建服務。它專門監控 Cloud Run 容器的執行狀態，能在接近即時 (Near Real-time) 的狀況下偵測執行階段的攻擊行為。

它具備了三個重大的技術優勢：
- **無需修改程式碼**：原生整合，開發團隊不需要在容器內安裝任何代理程式 (Agent) 或 Sidecar。
- **託管式服務**：由 Google Cloud 自動維護最新的偵測規則與威脅情資。
- **深度整合**：直接與 Google 的輕量級安全沙盒 `gVisor` 隔離技術結合，提供 Linux 核心層級的可視性。

---

## 💻 技術架構解密：Watcher 與遙測機制

CRTD 到底如何攔截惡意行為？以下帶你拆解它的運作流程：

{{< mermaid >}}
graph LR
    subgraph Cloud Run Instance
        A["Container (User Code)"]
        B["Watcher Process"]
        A -- "Syscalls, File Access, Network" --> B
    end
    C["Detector Service & SCC"]
    B -- "Telemetry (遙測數據)" --> C
    
    style A fill:#f9f9f9,stroke:#333,stroke-width:2px
    style B fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px
    style C fill:#fff3e0,stroke:#ff9800,stroke-width:2px
{{< /mermaid >}}

1. 使用者代碼所在的容器，其所有的**系統呼叫 (Syscalls)**、**檔案存取 (File Access)** 與**網路連線 (Network)**，皆會被側錄攔截。
2. 這些行為交由內部的 `Watcher Process` 進行捕獲。
3. Watcher 將即時遙測資料傳送給後端的 Detector Service 與 SCC 進行分析與威脅判定。

> ⚠️ **關鍵要求**：CRTD 強烈依賴 **第二代執行環境 (Gen 2 Execution Environment)**。因為 Gen 2 才能提供更完整的 Linux 核心相容性層級。若 Watcher 程序發生異常終止，該實例將進入「遙測中斷」狀態且無法自動重啟。

---

## 🤖 偵測模組詳解

CRTD 內建了豐富的威脅偵測模組，負責揪出常見的駭客入侵軌跡，主要可以分為兩大類：

### 1. 入侵與惡意執行
*   📡 **反向 Shell (Reverse Shell)**：偵測到容器嘗試與外部攻擊者建立連線，這通常是遠端命令執行 (RCE) 的前兆 (`CLOUD_RUN_REVERSE_SHELL`)。
*   📜 **惡意腳本執行 (Malicious Script Executed)**：利用自然語言處理 (NLP) 技術，智慧分析 Bash 或 Python 腳本的意圖，精準區分合法維運腳本與惡意代碼 (`CLOUD_RUN_MALICIOUS_SCRIPT_EXECUTED`)。
*   🏃‍♂️ **容器逃逸 (Container Escape)**：即時偵測試圖突破隔離層並存取底層基礎設施 (Host) 的危險行為 (`CLOUD_RUN_CONTAINER_ESCAPE`)。

### 2. 持久化與規避偵測
*   📦 **新增的二進位檔案 (Added Binary Executed)**：若執行了原始容器映像檔 (Image) 中未曾定義的二進位檔案，通常意味著攻擊者已成功植入後門 (`CLOUD_RUN_ADDED_BINARY_EXECUTED`)。
*   🔐 **混淆/加密檔案 (Obfuscated Files)**：抓出使用 AES 或 XOR 高度加密或混淆的檔案，這常是惡意軟體規避內部靜態掃描的手法 (`CLOUD_RUN_AES_XOR_ENCODED_FILE`)。
*   ⚠️ **CLI 參數監控 (CLI Arguments)**：擷取並監控指令執行細節 (`CLOUD_RUN_REPORT_CLI_ARGS`)。
    *   *Privacy Warning：請特別注意，若應用程式設計不良，將機密資訊 (Secrets) 以指令參數明文傳入，可能會導致機密在稽核日誌或 SCC 平台內意外洩漏。*

---

## 🚀 結論與未來進階

採用 Serverless 架構並不等於零風險。Cloud Run 搭配 CRTD 填補了執行階段可視性的空白，能夠幫助維運與資安團隊第一時間掌握容器內部的不尋常信號。

針對下一步的實踐，建議您可以：
1. 確保 Cloud Run 服務全面開啟 **第二代執行環境 (Gen 2)**。
2. 盡量使用 Google Cloud Secret Manager 來管理敏感機密，杜絕由環境變數或 CLI 參數明文洩漏的風險。
3. 進入 Security Command Center，啟用設定並測試 CRTD 告警與自動化通報的整合機制。

---

> **封面圖片生成 Prompt (給 Midjourney / DALL-E 使用)**:
> High quality, tech vibe, subtle anime or modern flat illustration style, clean UI aesthetic, vibrant colors. A futuristic data center flowing with glowing nodes representing Google Cloud serverless containers, protected by a sophisticated, energetic blue security force field or cyber-shield symbolizing Cloud Run Threat Detection, dark theme background with high contrast glowing elements, ultra-detailed --ar 16:9
