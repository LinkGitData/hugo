---
title: "使用 MCP Toolbox 串接 GCP BigQuery：讓 AI 自動生成雲端費用報告"
date: 2026-06-30T16:44:31+08:00
draft: false
tags: ["GCP", "BigQuery", "MCP", "AI", "Claude"]
categories: ["Tech"]
mermaid: true
cover:
  image: "images/gcp-billing-mcp-cover.png?v=1"
  alt: "GCP Billing MCP Toolbox"
  caption: "透過 MCP Toolbox 讓 AI 自動分析 GCP 帳單"
  relative: false
---

> 🔗 **官方資料來源**：這是一篇關於使用 MCP Toolbox 串接 BigQuery 以產生報告的實戰筆記。

這篇文章記錄了如何透過 MCP Toolbox 將 Claude 直接接上 GCP Billing BigQuery 匯出，並讓 AI 自動查詢數據、產生一份帶有動態圖表的互動式 HTML 費用分析報告。過去需要工程師手動撈資料、貼 Excel 的工作，現在能大幅自動化。

以下是整個流程的完整步驟，任何有 GCP 帳單 BigQuery 匯出的團隊都可以照著實作。

## 📋 目錄

- [整體架構概覽](#-整體架構概覽)
- [Step 1：開啟 GCP Billing Export 到 BigQuery](#-step-1開啟-gcp-billing-export-到-bigquery)
- [Step 2：安裝 MCP Toolbox](#-step-2安裝-mcp-toolbox)
- [Step 3：建立 tools.yaml](#-step-3建立-toolsyaml)
- [Step 4：設定 .mcp.json](#-step-4設定-mcpjson)
- [Step 5：用 Claude 查詢 BigQuery 並驗證資料](#-step-5用-claude-查詢-bigquery-並驗證資料)
- [Step 6：請 Claude 產生 HTML 費用報告](#-step-6請-claude-產生-html-費用報告)
- [Step 7：常見踩坑與解法](#-step-7常見踩坑與解法)
- [🚀 結論與未來進階](#-結論與未來進階)

## 🏗️ 整體架構概覽

整個系統的組成與資料流如下：

{{< mermaid >}}
graph LR
  GCP[GCP Billing Export] --> BQ[BigQuery]
  BQ --> MCP[MCP Toolbox]
  MCP --> Claude[Claude Cowork]
  Claude --> Report[HTML 報告]
{{< /mermaid >}}

1. **GCP Billing Export → BigQuery**：GCP 原生功能，自動將帳單明細寫入 BigQuery dataset。
2. **MCP Toolbox (Google)**：一個本地執行的 binary，將 BigQuery SQL 查詢包裝成 MCP tools。
3. **.mcp.json**：Cowork / Claude Code 的 MCP server 設定檔，告訴 Claude 要啟動哪些工具。
4. **tools.yaml**：定義所有 SQL 查詢工具的設定檔，Toolbox 會讀取此檔案。
5. **Claude (Cowork)**：透過 MCP tools 對話式查詢 BigQuery，並用 Python 產生 HTML 報告。

> 💡 **經驗分享**：為什麼用 MCP Toolbox 而不是直接查 BigQuery？  
> MCP Toolbox 讓 Claude 能以 **「工具呼叫」** 方式執行預定義 SQL，不需要每次寫原始 SQL。不僅查詢有參數化保護（防 injection），且可以限制 Claude 能查哪些 table 或欄位，安全可控。

## 🌟 Step 1：開啟 GCP Billing Export 到 BigQuery

### 1-1 在 GCP Console 啟用 Billing Export

進入 GCP Console → 帳單 → 帳單匯出，選擇 **「BigQuery 匯出」** 標籤並編輯設定。填入目標 BigQuery Project 及 Dataset 名稱，例如：

- **Project**: `example-billing-admin`
- **Dataset**: `gcp_billing_export`

儲存後，GCP 每天會自動將帳單寫入自動建立的 Table：  
`example-billing-admin.gcp_billing_export.gcp_billing_export_v1_XXXXXX_XXXXXX_XXXXXX`

### 1-2 確認 Table 架構

Table 中的關鍵欄位包含：

- `project.id` / `project.name`：GCP 專案 ID 與名稱
- `service.description`：GCP 服務名稱
- `sku.description`：SKU 細項名稱
- `usage_start_time`：使用時間
- `cost`：毛成本（未折扣）
- `credits`：包含所有折扣（CUD、SUD 等）的 ARRAY，每筆有 `type`、`name`、`amount`

**費用計算公式：**
`net_cost = gross_cost + total_credits` (因 `credits.amount` 為負數)

> 🤖 **Agent Prompt**:
>
> ```sql
> SUM(cost) AS gross_cost,
> SUM((SELECT SUM(amount) FROM UNNEST(credits))) AS total_credits,
> SUM(cost) + SUM((SELECT SUM(amount) FROM UNNEST(credits))) AS net_cost
> ```

## 💻 Step 2：安裝 MCP Toolbox

### 2-1 下載 Toolbox Binary

MCP Toolbox 由 Google 開源，可直接下載對應平台的 binary：

```bash
# macOS ARM64 (M1/M2/M3)
curl -L https://github.com/googleapis/genai-toolbox/releases/latest/download/toolbox_darwin_arm64 \
     -o ./toolbox
chmod +x ./toolbox
```

將 `toolbox` binary 放在專案根目錄。

### 2-2 設定 GCP 認證

執行以下指令，透過 Application Default Credentials (ADC) 連接 BigQuery：

```bash
gcloud auth application-default login
gcloud config set project example-billing-admin
```

> ⚠️ **注意事項**：執行指令後，credentials 會存在 `~/.config/gcloud/`。正式環境建議改用 Service Account JSON，並設定 `GOOGLE_APPLICATION_CREDENTIALS` 環境變數。

## 📋 Step 3：建立 tools.yaml

這是整個流程的核心，定義了 Toolbox 的資料來源與所有可供呼叫的 SQL 工具。

### 3-1 核心檔案結構

```yaml
sources:
  billing-source:
    kind: bigquery
    project: example-billing-admin
tools:
  monthly_cost_by_project:
    source: billing-source
    kind: bigquery-sql
    description: >
      查詢指定月份區間內，各專案的每月總費用。
    parameters:
      - name: start_month
        type: string
      - name: end_month
        type: string
    statement: |
      SELECT
          project.name AS project_name,
          project.id AS project_id,
          FORMAT_DATE('%Y-%m', usage_start_time) AS month,
          SUM(cost) + SUM((SELECT SUM(amount) FROM UNNEST(credits))) AS net_cost
      FROM `example-billing-admin.gcp_billing_export.gcp_billing_export_v1_XXXX`
      WHERE FORMAT_DATE('%Y-%m', usage_start_time) BETWEEN @start_month AND @end_month
      GROUP BY 1, 2, 3
      ORDER BY month, net_cost DESC
```

### 3-2 關鍵防呆機制

在撰寫 `top_services_by_cost` 查詢時，若使用 `ORDER BY net_cost DESC` 會讓有 `NULL` 的服務排序錯亂。因為某些服務只有 `cost` 沒有 `credits`，這時 `net_cost` 為 `NULL`，導致重要服務被排除在外。

**解法**：改用 `ORDER BY COALESCE(net_cost, gross_cost) DESC`。

## ⚙️ Step 4：設定 .mcp.json

在專案根目錄建立 `.mcp.json`，告訴 Claude 如何啟動 Toolbox：

```json
{
  "mcpServers": {
    "gcp-billing": {
      "command": "./toolbox",
      "args": ["--tools-file", "tools.yaml", "--stdio"],
      "env": {
        "BIGQUERY_PROJECT": "example-billing-admin"
      }
    }
  }
}
```

設定完成後，重新開啟工作階段，可以請 Claude 「查詢 2026-05 到 2026-06 的各專案費用」驗證是否連線成功。

## 🤖 Step 5：用 Claude 查詢 BigQuery 並驗證資料

取得數據後建議進行以下驗證：

- **對帳 GCP Console**：到 GCP Console → 帳單 → 費用摘要，對照 Claude 查到的數字。
- **CUD 注意事項**：BigQuery 中的 `FEE_UTILIZATION_OFFSET` 金額與 GCP Console 顯示的 **「CUD 節省」** 不相等。兩者計算基準不同，不能直接比較。

## 📊 Step 6：請 Claude 產生 HTML 費用報告

你可以下達類似以下的 Prompt，請 Claude 自動產出圖文並茂的 HTML 報告：

> 幫我用以上數據產生一份 HTML 費用分析報告，需包含：  
>
> - KPI cards：本月總費用、上月總費用、最大漲幅/降幅專案  
> - 分組長條圖：各專案 3 個月費用比較 (Chart.js)  
> - 洞察摘要：條列式重點說明  
> - Chart.js 請內嵌 (不要用 CDN)

**Chart.js 內嵌的重要性**：在預覽環境中，外部 CDN 連線可能被阻擋。確保使用 `<script>` 標籤直接將 Chart.js 原始碼內嵌。

## 🛠️ Step 7：常見踩坑與解法

1. **JS 語法錯誤導致報告空白**：若 KPI 卡片全部空白，通常是 JS 語法出錯。使用瀏覽器 F12 檢查 Console 即可。
2. **Python f-string 大括號衝突**：用 Python `f-string` 生成含 JS 程式碼的 HTML 時，JS 的 `{}` 會被視為變數，必須改成 `{{}}`。
3. **Regex 替換 HTML 失敗**：非貪婪匹配會在第一個 `</div>` 停下。解法是改用 `str.replace` 或是 BeautifulSoup。
4. **服務排序錯亂**：必須使用 `COALESCE(net_cost, gross_cost)`。
5. **CUD 折扣數字不一致**：若要在報告中標示 CUD 節省，建議直接引用 GCP Console 的數字避免誤導。

## 🚀 結論與未來進階

整個流程熟悉後大約 1-2 小時即可完成初版設定。之後每個月只需簡單的一句話，Claude 就能透過 MCP 自動撈取 BigQuery 的資料，產出一份包含 KPI 與動態圖表的美觀報告。我們正式邁入 **「代理人時代」** 領域，將大量例行性工時解放，轉化為更多的創新動能。
