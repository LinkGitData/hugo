---
title: "從暗數據到結構化黃金：利用 BigQuery Knowledge Catalog 實現批量媒體文件推理"
date: 2026-06-01T09:10:31+08:00
draft: false
tags: ["BigQuery", "Dataplex", "Vertex AI", "Dark Data", "Agentic Data Cloud"]
categories: ["Tech"]
mermaid: true
cover:
  image: "images/dark-data-gold-cover.png?v=1"
  alt: "Dark data transformed to structured gold"
  caption: "透過 BigQuery 與 Dataplex 將暗數據轉化為結構化黃金"
  relative: false
---

> 🔗 **官方資料來源** ：[How I turned dark data into structured gold!](https://medium.com/google-cloud/how-i-turned-dark-data-into-structured-gold-456b2c8c4f4f)

在當今企業的數位轉型浪潮中，數據被譽為新的石油。然而，絕大多數企業所擁有的數據石油，依然處於未經開採的原始狀態。這些被遺忘在雲端儲存空間（Cloud Storage Buckets）中的大量非結構化文件，如 PDF 合約、產品規格書、收據、掃描影像與語音記錄，在業界被稱為 **「暗數據」** （Dark Data） 。

根據各大市調機構的估計，企業內部有超過 **80% 到 90%** 的數據屬於此類非結構化數據。這些數據由於缺乏結構，傳統的 SQL 查詢工具與商業智慧（BI）儀表板完全無法感知它們的存在。

過去，要將這些暗數據轉化為可分析的結構化資訊，企業必須建構極其複雜、脆弱且維護成本高昂的資料管線（ETL Pipelines）。然而，隨著大語言模型（LLM）的爆發以及雲端數據倉庫的演進，我們迎來了全新的解決方案。

Google Cloud 開發倡議者 Abirami Sukumaran 發表了一篇精闢的文章，詳細介紹了如何利用 **BigQuery Knowledge Catalog** 與 **Dataplex** ，在幾分鐘內完成大規模媒體文件的批量推理（Bulk Inference），將暗數據「點石成金」，轉化為結構化的黃金資產。

本篇文章將針對此主題進行深度的技術心得剖析與應用分析，探討這項技術如何作為 **「代理人數據雲」** （Agentic Data Cloud） 的堅實起步，並為企業帶來革命性的商業價值。

---

## 📋 目錄

- [企業遺忘的寶藏：解密什麼是「暗數據」（Dark Data）](#企業遺忘的寶藏解密什麼是暗數據dark-data)
- [代理人數據雲的基石：BigQuery & Dataplex 的強強聯手](#代理人數據雲的基石bigquery--dataplex-的強強聯手)
- [實戰演練：從 Cloud Storage 到 BigQuery 的批量推理工作流](#實戰演練從-cloud-storage-到-bigquery-的批量推理工作流)
  - [步驟一：建立 Cloud Resource Connection](#步驟一建立-cloud-resource-connection)
  - [步驟二：在 BigQuery 中建立 Object Table（對象表）](#步驟二在-bigquery-中建立-object-table對象表)
  - [步驟三：配置 Dataplex 數據掃描與語義推理](#步驟三配置-dataplex-數據掃描與語義推理)
  - [步驟四：註冊與配置 Vertex AI 遠端模型](#步驟四註冊與配置-vertex-ai-遠端模型)
  - [步驟五：使用 SQL 進行大規模批量推理與欄位提取](#步驟五使用-sql-進行大規模批量推理與欄位提取)
- [邁向 Agentic Data Cloud：多代理人系統的關鍵起點](#邁向-agentic-data-cloud多代理人系統的關鍵起點)
- [應用場景與商業價值剖析](#應用場景與商業價值剖析)
  - [場景一：零售與供應鏈管理（供應商規格書自動化）](#場景一零售與供應鏈管理供應商規格書自動化)
  - [場景二：金融與保險業（歷史合約與理賠單據審查）](#場景二金融與保險業歷史合約與理賠單據審查)
  - [場景三：醫療健康領域（非結構化臨床病歷結構化）](#場景三醫療健康領域非結構化臨床病歷結構化)
- [結論與未來進階](#結論與未來進階)

---

## 🌌 企業遺忘的寶藏：解密什麼是「暗數據」（Dark Data）

在深入探討技術架構之前，我們必須先釐清：為什麼非結構化數據會被稱為 **「暗數據」** ？

**「暗數據」** 指的是企業在日常營運活動中收集、處理並儲存，但通常無法用於任何其他目的（例如分析、商業預測或決策支援）的資訊資產。這些數據就像是宇宙中的暗物質——我們知道它佔據了絕大部分的質量，但傳統的儀器卻完全觀測不到它。

### 傳統提取技術的局限與痛點

在生成式 AI 與現代大語言模型成熟之前，企業若想從 PDF、收據或影像中提取關鍵欄位，通常會採用以下幾種方案，但各自都面臨嚴重的瓶頸：

1.  **光學字元識別（OCR）結合正規表達式（Regex）** ：
    這是最傳統的做法。先用 OCR 工具將圖片或 PDF 轉化為純文字，再利用複雜的 Regex 規則去搜尋特定的字眼（例如「總金額」、「發票日期」）。
    *   **痛點** ：容錯率極低。一旦供應商的發票排版稍微調整一個像素，或者文字順序發生變動，Regex 規則就會完全失效，需要工程師重新編寫與維護。
2.  **基於機器學習的專用文檔理解模型（如 Document AI）** ：
    這比 Regex 更進步，能夠理解文件的視覺結構（例如表格與鍵值對）。
    *   **痛點** ：雖然精準，但對於「非標準化、多樣化」的文件類型（例如寫滿各類非結構化文字敘述的商業合同、技術規格書、或研究報告），自訂模型的開發週期與訓練成本依舊高昂。
3.  **外包人工登打（Data Entry）** ：
    直接僱用人力閱讀文件並手動輸入資料庫。
    *   **痛點** ：速度極慢，無法應對海量數據的即時處理需求，且存在人為疏失與資安隱私外洩的風險。

由於上述技術的限制，許多企業選擇將這些非結構化文件默默堆積在 **Cloud Storage** 中，成為名副其實的「暗數據」，任由其折舊與流失價值。然而，這些文件往往蘊含著企業的核心機密、歷史客戶行為、供應商合約細節、甚至是多年積累的研發配方。如何用最簡單、最符合經濟效益的方式開採這座金礦，是現代 CIO 面臨的重大課題。

---

## 🏗️ 代理人數據雲的基石：BigQuery & Dataplex 的強強聯手

為了解決暗數據的開採難題，Google Cloud 推出了以 **BigQuery Object Tables（物件表）** 為核心，並無縫整合 **Dataplex Knowledge Catalog（知識型錄）** 與 **Vertex AI 遠端模型** 的全新架構。這套架構的核心思想是： **「讓計算走向數據，而非將數據搬向計算」** 。

我們不需要把大量的 PDF 檔案解構並匯入 BigQuery 內部，而是讓 BigQuery 直接去「閱讀」存放在 Cloud Storage 上的文件，並利用大語言模型（如 Gemini）在資料庫端直接進行理解與分析。

下面是這套非結構化數據轉化為結構化黃金的系統架構流程圖：

{{< mermaid >}}
graph TD
    A[Cloud Storage 儲存桶 - 非結構化 PDFs] --> B[Dataplex Knowledge Catalog 掃描]
    B --> C[語義推理與自動分類]
    A --> D[BigQuery Object Tables 建立連結]
    D --> E[BigQuery Remote Model 呼叫 Gemini]
    C --> D
    E --> F[執行 SQL 批量推理 ML.GENERATE_TEXT]
    F --> G[JSON 提取與解析 JSON_EXTRACT]
    G --> H[結構化黃金資料表]
{{< /mermaid >}}

### 核心組件的角色分配

*   **BigQuery Object Tables（物件表）** ：
    這是 BigQuery 的一種特殊外部表類型。它不會儲存實際的檔案內容，而是唯讀地映射 Cloud Storage 中的檔案列表。每一行代表一個檔案，欄位則包含檔案的 `file_uri`（檔案路徑）、`metadata`（建立時間、檔案大小、MIME 類型）以及指向該檔案的安全權限。這意味著我們可以像查詢普通 SQL 表格一樣，篩選、排序這些非結構化檔案。
*   **Dataplex Knowledge Catalog** ：
    這扮演著「元數據治理與感知引擎」的角色。它可以自動掃描（Data Scan）指定的 Cloud Storage 儲存桶，自動識別檔案的類型與結構，並生成資料目錄。
*   **語義推理（Semantic Inference）** ：
    這是 Dataplex 的一項關鍵特性。在掃描過程中，語義推理能夠理解文件之間的語義關聯、提取實體（Entities）與標籤，並為資料資產標註元數據。這使得原本毫無關聯的檔案，在元數據層面建立起了網絡結構，為後續的 AI Agent 提供更豐富的脈絡資訊（Context）。

---

## 💻 實戰演練：從 Cloud Storage 到 BigQuery 的批量推理工作流

接下來，我們將根據 Abirami Sukumaran 在文章中揭示的步驟，進行具體的技術實作演練。我們將展示如何透過 SQL 在 BigQuery 中建立物件表，並呼叫 Gemini 模型進行大規模的批量推理，將 PDF 中的複雜資訊提煉成乾淨的結構化資料表。

### 步驟一：建立 Cloud Resource Connection

在 BigQuery 中，要存取外部資源（如 Cloud Storage 中的檔案或呼叫 Vertex AI 的遠端模型），必須使用 **Cloud Resource Connection** 。這是 GCP 提供的一種安全授權機制，避免在 SQL 程式碼中硬編碼任何敏感的 API 密鑰。

請在 BigQuery console 或透過 CLI 執行以下 SQL 來建立連線：

```sql
-- 建立與外部 Google Cloud 資源的安全連線
CREATE OR REPLACE CONNECTION `project-id.us.my-cloud-connection`
  CONNOPTS(
    description = '用於存取 Cloud Storage 與 Vertex AI Gemini 模型的安全連線'
  );
```

> 💡 **經驗分享** ：建立連線後，系統會自動生成一個服務帳戶（Service Account，格式通常為 `bqcx-xxxxxx@gcp-sa-bigquery-condel.iam.gserviceaccount.com`）。您必須前往 IAM 頁面，為此服務帳戶授予 **「Storage Object Viewer」** （讀取 Cloud Storage 檔案）以及 **「Vertex AI User」** （呼叫 Gemini 模型）的權限。

---

### 步驟二：在 BigQuery 中建立 Object Table（對象表）

有了連線並授予適當權限後，我們就可以建立物件表。這個表將直接映射 Cloud Storage 儲存桶中的 PDF 檔案。

假設我們將所有的產品規格說明書（PDF 格式）儲存在 `gs://enterprise-dark-data-bucket/specs/` 目錄下：

```sql
-- 建立指向 Cloud Storage PDF 檔案的物件表
CREATE OR REPLACE EXTERNAL TABLE `project-id.my_dataset.product_specs_object_table`
WITH CONNECTION `project-id.us.my-cloud-connection`
OPTIONS (
  object_metadata = 'SIMPLE',
  uris = ['gs://enterprise-dark-data-bucket/specs/*.pdf']
);
```

現在，如果您對這個表執行 `SELECT * FROM product_specs_object_table LIMIT 5`，您將會看到類似下表的結構化中介資料：

| uri | size | content_type | updated | metadata |
| :--- | :--- | :--- | :--- | :--- |
| `gs://.../spec_a.pdf` | 1542000 | `application/pdf` | 2026-05-20... | ... |
| `gs://.../spec_b.pdf` | 2405100 | `application/pdf` | 2026-05-21... | ... |

---

### 步驟三：配置 Dataplex 數據掃描與語義推理

要在 Dataplex 中對該儲存桶配置掃描並啟用語義推理，您需要前往 Google Cloud Console 中的 **Dataplex** 頁面，並執行以下設定：

1.  進入 **Knowledge Catalog** 或是 **Datascan** 功能。
2.  建立一個新的「元數據掃描任務」（Metadata Scan Job）。
3.  將掃描目標設定為您的儲存桶 `gs://enterprise-dark-data-bucket/specs/`。
4.  在高級選項中，勾選 **「啟用語義推理」** （Enable Semantic Inference） 。這將允許 Dataplex 自動分析文件內容，產生關聯標籤，並將這些中介資料直接同步至 BigQuery 物件表的延伸欄位或中介資料屬性中。

---

### 步驟四：註冊與配置 Vertex AI 遠端模型

我們需要在大語言模型與 BigQuery 之間搭起橋樑。透過在 BigQuery 中註冊 Vertex AI 遠端模型，我們可以直接在 SQL 查詢中呼叫大語言模型。

此處我們選擇效能強大、推理能力極佳且支援長上下文的 **Gemini 1.5 Pro** 模型：

```sql
-- 在 BigQuery 中註冊遠端 Gemini 1.5 Pro 模型
CREATE OR REPLACE MODEL `project-id.my_dataset.gemini_pro_model`
  REMOTE WITH CONNECTION `project-id.us.my-cloud-connection`
  OPTIONS (
    endpoint = 'gemini-1.5-pro'
  );
```

---

### 步驟五：使用 SQL 進行大規模批量推理與欄位提取

這是最關鍵的一步。我們將使用 BigQuery ML 的 `ML.GENERATE_TEXT` 函數。我們把物件表中的每一行（即每一個 PDF 檔案）作為輸入傳給 Gemini，並透過 **System Prompt** 要求 Gemini 將分析結果以標準的 JSON 格式輸出。

最後，我們利用 SQL 中的 `JSON_EXTRACT` 函數將 JSON 欄位解構，存入最終的結構化黃金資料表中。

以下是完整的 SQL 大規模推理與提取腳本：

```sql
-- 執行批量推理並將非結構化 PDF 轉換為結構化關聯表
CREATE OR REPLACE TABLE `project-id.my_dataset.structured_product_specs` AS
WITH raw_inference AS (
  SELECT
    uri,
    -- 呼叫遠端模型進行文本生成與信息提取
    ml_generate_text_result
  FROM
    ML.GENERATE_TEXT(
      MODEL `project-id.my_dataset.gemini_pro_model`,
      -- 將物件表傳入作為查詢目標
      TABLE `project-id.my_dataset.product_specs_object_table`,
      STRUCT(
        -- 設定 Prompt，引導模型進行高度結構化的 JSON 輸出
        '''
        你是一個專業的資料提取助手。請閱讀傳入的 PDF 文件（產品規格說明書），並精確提取出以下資訊：
        1. 產品名稱 (product_name)
        2. 製造商名稱 (manufacturer)
        3. 核心規格參數 (core_specs，請以文字摘要)
        4. 建議零售價 (msrp_usd，若無則填寫 null)
        5. 安全合規認證 (certifications，請以陣列形式列出)

        注意：你必須且只能輸出一個合法的 JSON 物件，格式如下，不要包含任何 markdown 標記（如 ```json 等）：
        {
          "product_name": "字串",
          "manufacturer": "字串",
          "core_specs": "字串",
          "msrp_usd": 數字或 null,
          "certifications": ["認證1", "認證2"]
        }
        ''' AS prompt,
        -- 強制模型輸出 JSON 格式
        TRUE AS flatten_json_output,
        0.1 AS temperature
      )
    )
),
parsed_json AS (
  SELECT
    uri,
    -- 將生成的文字解析為 BigQuery JSON 數據類型
    SAFE.PARSE_JSON(ml_generate_text_result) AS parsed_data
  FROM
    raw_inference
)
-- 最終提取乾淨的欄位，轉化為實體關聯表
SELECT
  uri,
  -- 提取產品名稱
  SAFE_CAST(JSON_VALUE(parsed_data.product_name) AS STRING) AS product_name,
  -- 提取製造商
  SAFE_CAST(JSON_VALUE(parsed_data.manufacturer) AS STRING) AS manufacturer,
  -- 提取規格摘要
  SAFE_CAST(JSON_VALUE(parsed_data.core_specs) AS STRING) AS core_specs,
  -- 提取價格並轉為 FLOAT64
  SAFE_CAST(JSON_VALUE(parsed_data.msrp_usd) AS FLOAT64) AS msrp_usd,
  -- 提取合規認證陣列
  JSON_VALUE_ARRAY(parsed_data.certifications) AS certifications
FROM
  parsed_json;
```

> 💡 **經驗分享** ：在處理成千上萬個檔案時，直接呼叫遠端模型可能會觸發 API 的配額限制（Quota limits）。在實際生產環境中，建議在 SQL 查詢中結合分批處理（Batching），或者向 Google Cloud 申請調高 Vertex AI 的每分鐘請求數（RPM）配額。

透過上述短短的幾段 SQL，原本被深埋在 Cloud Storage 中的成百上千份 PDF 規格書，在幾分鐘內就變成了一張乾淨、可被普通 BI 工具查詢、可用於 SQL 分析的 **「結構化黃金資料表」** 。這就是大數據、雲端計算與生成式 AI 融合帶來的巨大威力。

---

## 🤖 邁向 Agentic Data Cloud：多代理人系統的關鍵起點

為什麼 Abirami Sukumaran 會把這項技術做為她 **「Agentic Data Cloud」** 五部曲的第 1 部？這背後有著深刻的架構設計考量。

在當前 AI 應用的開發中， **AI Agents（智慧代理人）** 正在逐漸取代簡單的聊天機器人。一個真正的 AI Agent 不僅僅是回答問題，還需要具備主動規劃、呼叫工具（Tool Use）、查詢資料庫、並根據查詢結果執行特定商業逻辑的能力。

然而，AI Agent 的決策品質，完全取決於它所能獲取的「資料品質與格式」。

### 為什麼 Agent 需要結構化數據？

1.  **降低 Token 消耗與延遲（Latency）** ：
    如果我們讓一個 AI Agent 去回答「哪幾款產品的價格低於 100 美元且具備 CE 認證？」，而資料源是 1,000 份 PDF 文件。如果 Agent 每次都需要把 1,000 份 PDF 全部丟給 LLM 進行即時檢索與分析，這將消耗數百萬的 Token，且回覆時間可能長達數分鐘，這在商業應用中是完全不可接受的。
    相反，如果我們事先使用 BigQuery 將這 1,000 份 PDF 推理並轉化為結構化的資料表，Agent 只需要產生並執行一條簡單的 SQL 語法：
    `SELECT product_name FROM dataset.specs WHERE msrp_usd < 100 AND 'CE' IN UNNEST(certifications)`
    這條查詢只需要不到一秒鐘的時間，消耗極低的計算資源，且結果精確無誤。
2.  **提升推理的精準度，避免幻覺（Hallucination）** ：
    大語言模型在面對極長且混亂的非結構化文字時，容易忽略細節或產生幻覺。而關聯式資料庫的欄位限制與類型約束（如 FLOAT64, DATE），本質上就是一種強大的資料品質過濾器。交給 Agent 一個結構良好的資料庫，能大幅提高 Agent 的決策可靠度。
3.  **支持多模態與多代理人的協同作業** :
    在 Abirami Sukumaran 的後續規劃中，結構化後的數據將流入 AlloyDB 作為 transactional 資料來源，並與資料聯邦技術（Data Federation）結合。在此之上，我們可以建構不同的專屬 Agent（例如負責採購的 Procurement Agent、負責法務的 Compliance Agent）。這些 Agent 之間可以透過共享的、由暗數據提煉出來的「數據黃金」進行高效的協作與資訊傳遞。

因此，將暗數據結構化，並非單純的資料處理任務，而是為建構下一代 **「代理人數據雲」** 鋪設不可或缺的高速公路。

---

## 🌟 應用場景與商業價值剖析

BigQuery Knowledge Catalog 與物件表批量推理的技術，在各行各業都有著極其廣泛的應用場景。以下我們列舉三個最具代表性的商業落地案例：

### 場景一：零售與供應鏈管理（供應商規格書自動化）

*   **痛點** ：大型零售商（如跨國超市）每天會收到成百上千家供應商寄送的產品規格書（PDF）、成份表、包裝尺寸說明等。這些資料需要被手動登錄到內部的 ERP 系統中，以便採購部門進行比對。
*   **應用方案** ：將這些規格書上傳至 Cloud Storage，透過 Dataplex 自動發現，並使用 BigQuery + Gemini 批量提取「產品條碼、成份、過敏原、包裝規格、保存期限」等。
*   **商業價值** ：將原本需要數週的人工審查與登錄流程縮短至幾分鐘，加快新品上架速度，並能即時監控成分合規性。

### 場景二：金融與保險業（歷史合約與理賠單據審查）

*   **痛點** ：保險公司積累了數十年的紙本理賠申請書掃描檔、診斷證明書、以及合約文本。當法務或精算部門想要分析「某類特定疾病的理賠趨勢與條款漏洞」時，由於資料都在圖片或 PDF 中，根本無法進行大規模 SQL 分析。
*   **應用方案** ：建構 BigQuery 物件表，呼叫遠端模型對理賠掃描件進行文字提取與關鍵欄位（理賠金額、疾病代碼、醫生診斷摘要）結構化。
*   **商業價值** ：使歷史理賠數據重新獲得分析價值，幫助精算師精準設計保單保費，並能自動識別疑似詐保的異常模式。

### 場景三：醫療健康領域（非結構化臨床病歷結構化）

*   **痛點** ：醫院中的電子病歷（EHR）包含大量的醫生自由文本手記、出院小結、病理報告等。這些資料是非結構化的，科研人員很難透過 SQL 篩選出特定病徵的患者群體來進行臨床研究。
*   **應用方案** ：使用 Dataplex Knowledge Catalog 對醫療報告進行語義分類，並利用大語言模型提取「病患症狀、用藥史、副作用、檢驗數值」等實體。
*   **商業價值** ：極大地促進了臨床真實世界研究（Real-World Evidence）的開展，縮短科研數據清洗時間，為精準醫療與新藥研發提供強大的數據支撐。

---

## 🚀 結論與未來進階

大數據與人工智慧的深度融合，正在重新定義資料工程的邊界。以前， **「非結構化數據」** 與 **「SQL 查詢」** 是兩個平行世界，中間隔著巨大的技術鴻溝。而 **BigQuery Knowledge Catalog** 、 **BigQuery Object Tables** 與 **Vertex AI** 的無縫結合，徹底打破了這道藩籬。

這項技術的商業啟示在於： **企業不再需要為了利用 AI 而放棄現有的資料庫基礎設施** 。我們可以直接在 BigQuery 這個全球最先進的資料倉庫中，用最熟悉的 SQL 語言，去驅動最前沿的生成式 AI 模型。

這僅僅是第一步。隨著我們成功將「暗數據」提煉為「結構化黃金」，我們已經擁有了建構自主資料代理人的黃金密鑰。未來，結合 **AlloyDB** 的交易性能、資料庫層的向量檢索、以及多代理人編排框架，企業將能夠打造出真正懂業務、懂歷史數據、且能自主執行的 **「代理人數據雲」** （Agentic Data Cloud） 。

對於所有資料工程師與 CIO 來說，現在正是時候去重新盤點那些躺在 Cloud Storage 裡沉睡的非結構化檔案。因為在 AI 時代，每一粒被遺忘的暗數據沙子，都有可能在幾分鐘之內，被提煉成照亮業務決策的耀眼黃金。
