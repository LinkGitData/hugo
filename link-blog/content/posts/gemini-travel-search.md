---
title: "「快與準」的完美交織：基於 Gemini Enterprise Agent Platform 的雙路徑旅遊搜尋系統實戰"
date: 2026-05-29T17:08:00+08:00
draft: false
tags: ["Gemini Enterprise", "Agent Platform", "ADK", "Context Caching", "RAG Engine", "Memory Bank"]
categories: ["Tech", "AI Projects"]
mermaid: true
cover:
  image: "images/gemini-travel-search-cover.png?v=1"
  alt: "Gemini Travel Search Cover"
  caption: "基於 Gemini 企業級代理人平台構建的雙路徑智慧旅遊搜尋系統"
  relative: false
---

在構建企業級生成式 AI 應用時，開發團隊往往會面臨一個難以調和的兩難局勢： **「速度」** 與 **「精度」** 彷彿是天平的兩端。如果為了追求極速而採用簡單的快取機制，系統容易回傳過時的內容；反之，若為了追求資料的準確性而每一次都進行完整的多源檢索與長文本推理，則會帶來數秒甚至數十秒的延遲，大幅降低使用者體驗。

為了徹底解決這一 Tension，本文將基於 Google 專為企業級應用打造的 **Gemini Enterprise Agent Platform** （ 搭載全新 **ADK** 代理人開發套件與 **Gemini 2.0 / 2.5 系列模型** ），實作一套雙路徑旅遊搜尋系統（ Travel Search System ）。本系統不需任何自行託管的基礎設施（ Zero Self-Managed Infrastructure ），完全運行於 Google Cloud 託管生態中，在 50 ms 內判斷使用者意圖並自動分流：
1. **Path A — CAG (Cache-Augmented Generation)** ：靜態知識查詢（ 如門票價格、開放時間等 ），利用 Context Caching 將延遲壓低至 **300 – 500 ms** 以內。
2. **Path B — Agentic RAG** ：複雜與個人化行程規劃，利用 ADK Graph Workflow、長期 Memory Bank 與 MCP (Model Context Protocol) 外部服務，在 **2 – 4 秒** 內生成結合歷史記憶與即時運算的高品質解答。

> 🔗 **參考手冊來源** ：[GenAI_TravelSearch_Lab_2026_1.docx](file:///Users/yuting/Documents/GitHub/raw/GenAI_TravelSearch_Lab_2026_1.docx)

---

## 📋 目錄

1. [雙路徑架構設計與運作流程](#雙路徑架構設計與運作流程)
2. [核心服務四大層級深度解析](#核心服務四大層級深度解析)
3. [Hands-On Lab 實戰指引](#hands-on-lab-實戰指引)
   * [Lab 1：環境設置與知識庫準備](#lab-1環境設置與知識庫準備)
   * [Lab 2：建立 Intent Router](#lab-2建立-intent-router)
   * [Lab 3：Path A — CAG 靜態快取查詢](#lab-3path-a--cag-靜態快取查詢)
   * [Lab 4：Path B — Agentic RAG 個人規劃](#lab-4path-b--agentic-rag-個人規劃)
   * [Lab 5：部署至 Agent Engine 與安全治理](#lab-5部署至-agent-engine-與安全治理)
4. [端到端查詢流式追蹤](#端到端查詢流式追蹤)
5. [總結與未來進階](#總結與未來進階)

---

## 🏗️ 雙路徑架構設計與運作流程

整個旅遊搜尋系統的架構由 **BUILD** （ 構建 ）、 **SCALE** （ 規模化與記憶 ）、 **GOVERN** （ 安全治理 ）與 **OPTIMIZE** （ 觀測與優化 ）四大支柱構成。

以下是完整的系統資料流與請求分流架構圖：

{{< mermaid >}}
flowchart TD
    client[使用者與網頁應用程式] --> gateway[Cloud API Gateway 與 Agent Gateway]
    gateway --> router[ADK Intent Router 判斷複雜度]
    router -->|複雜度低| pathA[Path A CAG 靜態快取路徑]
    router -->|複雜度高| pathB[Path B Agentic RAG 推理路徑]
    
    subgraph PathA[Path A CAG 靜態查詢]
        cag_cache[Context Caching KV 快取] --> rag_eng_a[RAG Engine 知識庫檢索]
        rag_eng_a --> gemini_flash[Gemini Flash 快速回應]
    end
    
    subgraph PathB[Path B Agentic RAG 個人規劃]
        memory_bank[Memory Bank 載入長期記憶] --> graph_wf[ADK Graph Workflow 狀態機]
        graph_wf --> rag_eng_b[RAG Engine 與 Vector Search 混合檢索]
        graph_wf --> mcp_servers[MCP 外部服務如 Maps 和 BigQuery]
        rag_eng_b --> gemini_pro[Gemini Pro 推理與 Reflection 檢算]
        mcp_servers --> gemini_pro
        gemini_pro -->|預算超出| graph_wf
        gemini_pro -->|回覆生成| output_b[高品質個人化回應]
    end
    
    PathA --> optimize[Agent Observability 與 Trace 追蹤]
    PathB --> optimize
{{< /mermaid >}}

---

## 🛠️ 核心服務四大層級深度解析

### 1. BUILD 層：智慧代理與多模態檢索

* **ADK + Intent Router + Graph Workflow** ：
  ADK (Agent Development Kit) 是 Google 推出模型無關的代理人開發框架。其 Graph Workflow 能支援有向循環圖（ Cycle ），允許開發者設定「思考-反射-重寫」的循環推理邏輯。而 **Intent Router** 則是一個極輕量化的 `LlmAgent`，能在 50 ms 內對使用者的 Input 進行評分（ 0.0 代表純靜態查詢，1.0 代表極為複雜的多步規劃 ），以極低的 Token 成本精準分流。
* **Context Caching (CAG)** ：
  這是大幅縮減延遲與開銷的關鍵技術。對於包含大量靜態資料的旅遊知識庫（ 如飯店指南、景點票價表、車次時刻表，約 80k-2M Tokens ），我們將其作為 prefix 預載入模型的 KV cache 中。快取 Token 的計費僅為標準輸入 Token 的 **25%** ，並支援配置 TTL 與自動重新整理間隔。
* **RAG Engine** ：
  全託管的 RAG Pipeline。從 Document AI 的智慧文件解析、自動 Chunking、以最新 `text-embedding-005` 模型生成 Embedding，到 Reranking 的混合檢索，一氣呵成。底層採用 **Managed Spanner** 向量資料庫，具備 VPC-SC 網路隔離與 CMEK 自訂金鑰加密。
* **Vector Search** ：
  底層基於 Google 自研的 ScaNN 演算法，在千萬級（ 10M+ ）向量的規模下，依然能將檢索延遲控制在 **10 ms** 左右，並原生支援 RRF (Reciprocal Rank Fusion) 混合檢索。
* **MCP (Model Context Protocol) Servers** ：
  這是 2025 年確立的統一工具連接協定。系統不需要為 Maps、BigQuery、Search 等外部資料源編寫繁瑣的客製化 SDK 連接器，全部透過 **Agent Registry** 進行統一集中管理與工具授權。

### 2. SCALE 層：會話持久化與長期記憶體

* **Agent Engine (Deployments)** ：
  全託管的無伺服器 Agent 執行環境，支援秒級冷啟動（ Sub-second Cold Start ），且在閒置時完全不計費（ 內含免費額度 ）。其支援 **A2A (Agent-to-Agent)** 協作協定，能讓主規劃 Agent 將「尋找飯店」與「比對機票」等子任務平行委派給多個 Sub-agents 執行。
* **Sessions** ：
  自動以 `SessionEvent` 格式記錄每一次的對話細節（ 包含 Tool call 內容與 LLM 中間思考過程 ），提供狀態持久化，確保多輪問答的脈絡（ Context ）不丟失。
* **Memory Bank + Memory Profiles** ：
  在 Session 結束後，系統會透過非同步的背景任務自動從對話事件中萃取關鍵事實（ 如：`「使用者偏好避開京都，且有 7 歲同行小孩」` ），並將其寫入隔離的 **Memory Profile** 。在下一次新會話開始時，透過語意搜尋自動預載入（ Preload ）記憶，避免重複詢問。在此層，系統還設有防範 **Memory Poisoning** （ 惡意記憶投毒 ）的安全檢查機制。

### 3. GOVERN 層：企業級安全邊界

* **Agent Gateway** ：所有 Agent 發出或接收的外部流量都必須通過的中央閘道，強制執行 mTLS 雙向加密、DPoP Token 綁定與基於 OAuth 2.0 的細粒度 IAM 授權。
* **Agent Identity** ：部署的每一個 Agent 都被賦予唯一的 SPIFFE 標識與 X.509 憑證。
* **Model Armor** ：部署於閘道最前端的安全盾牌，防止 Prompt Injection（ 提示詞注入 ）攻擊，並自動偵測及遮蔽 MCP 回傳結果或生成內容中的個人識別資訊（ PII ）。

### 4. OPTIMIZE 層：全鏈路觀測與自動優化

* **Unified Trace Viewer** ：基於 OpenTelemetry 標準的自動化 Trace 追蹤，開發者能直觀地在圖表上看到每一個 Tool call 耗時、檢索權重與 Token 用量，精準定位延遲瓶頸。
* **Agent Evaluation & Simulation** ：利用 Gemini-as-judge 機制對多輪對話質量（ groundedness, trajectory ）進行量化評分，並能透過模擬器自動投放邊界異常輸入（ 如：`「 Maps API 連線逾時」` ）進行上線前壓力測試。

---

## 💻 Hands-On Lab 實戰指引

本實戰指南共包含五個實驗，請確保您已安裝 Python 3.11+ 以及 `google-adk` 與 `google-cloud-aiplatform` 庫。

### Lab 1：環境設置與知識庫準備

在此步驟中，我們將啟用 GCP 相關 API，上傳旅遊手冊至 Google Cloud Storage (GCS)，並初始化全託管的 **RAG Engine Corpus** 。

```bash
# 1. 啟用 Google Cloud 必要 API
gcloud services enable \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  documentai.googleapis.com

# 2. 建立儲存貯體並上傳旅遊文件
export PROJECT_ID="your-project-id"
export REGION="asia-northeast1"

gsutil mb -l $REGION gs://$PROJECT_ID-travel-docs
gsutil cp ./japan_travel_guide.pdf  gs://$PROJECT_ID-travel-docs/
gsutil cp ./ticket_prices_2026.pdf  gs://$PROJECT_ID-travel-docs/
```

接著，使用 Python SDK 建立索引庫：

```python
import vertexai
from vertexai.preview import rag

# 初始化 Vertex AI 環境
vertexai.init(project="your-project-id", location="asia-northeast1")

# 設定 Embedding 模型 (使用 Google 最新 text-embedding-005)
embedding_model_config = rag.RagEmbeddingModelConfig(
    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
        publisher_model="publishers/google/models/text-embedding-005"
    )
)

# 建立全託管 Corpus
corpus = rag.create_corpus(
    display_name="japan-travel-knowledge-base",
    backend_config=rag.RagVectorDbConfig(
        rag_embedding_model_config=embedding_model_config
    ),
)
print(f"✓ 成功建立 Corpus: {corpus.name}")

# 從 GCS 匯入所有旅遊指南 (設定 chunk 大小與 overlap 確保上下文不中斷)
operation = rag.import_files(
    corpus.name,
    paths=[f"gs://your-project-id-travel-docs/"],
    chunk_size=512,
    chunk_overlap=100,
)
print(f"✓ 檔案匯入並索引完成。狀態: {operation.metadata}")
```

#### 📌 驗證檢索效果
我們可以直接查詢 Corpus 以驗證檢索器是否能精準抽取出票價資料：

```python
# 測試 Corpus 檢索效果
test_query = "東京迪士尼門票價格"
response = rag.retrieval_query(
    rag_resources=[rag.RagResource(rag_corpus=corpus.name)],
    text=test_query,
    similarity_top_k=3,
)

for i, chunk in enumerate(response.contexts.contexts):
    print(f"\n--- Chunk {i+1} (檢索分數: {chunk.score:.3f}) ---")
    print(chunk.text[:200] + "...")
```

---

### Lab 2：建立 Intent Router

Intent Router 透過分析使用者的輸入，判斷應走 **Path A (CAG)** 還是 **Path B (Agentic RAG)** 。我們使用輕量且快速的 `gemini-2.0-flash-latest` 來做分流決策。

```python
import json
import asyncio
from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.runners import InMemoryRunner
from google.genai import types

# 制定 Intent Router 的 Prompt 規範，要求其輸出 JSON 格式
ROUTER_INSTRUCTION = """
你是旅遊查詢的分流器。分析使用者的問題，回傳 JSON（只回傳 JSON，不要加任何 markdown 標記或說明）：

{"route": "cag", "score": 0.0-0.3, "reason": "說明原因"} 
→ 適用於靜態知識查詢：單一票價、時刻表、地理距離、開放時間等固定資訊。

{"route": "agentic", "score": 0.7-1.0, "reason": "說明原因"} 
→ 適用於需要規劃、個人化、多步驟推理：行程規劃、綜合預算分配、排雷推薦等。
"""

intent_router = LlmAgent(
    model="gemini-2.0-flash-latest", # 使用 Flash 降低路由延遲至 50ms 內
    name="travel_intent_router",
    instruction=ROUTER_INSTRUCTION.strip(),
)

app = App(name="travel-router-app", root_agent=intent_router)
runner = InMemoryRunner(agent=intent_router, app_name="travel-router-app")

async def test_routing():
    queries = [
        "東京迪士尼一日門票多少錢？",
        "幫我規劃 5 天日本行程，預算 8 萬，我帶了 7 歲小孩，已去過京都"
    ]
    for q in queries:
        session = await runner.session_service.create_session(
            app_name="travel-router-app", user_id="test_user"
        )
        content = types.Content(role="user", parts=[types.Part(text=q)])
        
        # 串流讀取分流結果
        text_res = ""
        async for event in runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=content,
        ):
            if event.is_final_response():
                text_res = event.content.parts[0].text
                break
        
        result_data = json.loads(text_res.strip())
        print(f"\n問題: {q}")
        print(f"路由決策: {result_data['route']} (分數: {result_data['score']})")
        print(f"分流原因: {result_data['reason']}")

asyncio.run(test_routing())
```

---

### Lab 3：Path A — CAG 靜態快取查詢

對於靜態問題，我們啟用 **Context Caching** 預先載入知識庫。快取能大幅減少冷啟動延遲並壓低輸入 Token 成本。

```python
from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.agents.context_cache_config import ContextCacheConfig
import time
import asyncio
from google.adk.runners import InMemoryRunner

# 建立 Path A 專屬的 Flash Agent
cag_agent = LlmAgent(
    model="gemini-2.0-flash-latest",
    name="travel_cag_agent",
    instruction="你是旅遊資訊查詢助手，專門回答靜態旅遊資訊。請利用內建 Corpus 回答。限制 100 字內，簡明扼要。",
)

# 載入 Context Caching 配置
cag_app = App(
    name="travel-cag-app",
    root_agent=cag_agent,
    context_cache_config=ContextCacheConfig(
        min_tokens=1024,      # 超過此門檻自動啟用快取
        ttl_seconds=3600,     # 快取生命週期 (1小時)
        cache_intervals=5,    # 每 5 次請求自動重新整理
    )
)

runner = InMemoryRunner(agent=cag_agent, app_name="travel-cag-app")

async def benchmark_latency():
    session = await runner.session_service.create_session(
        app_name="travel-cag-app", user_id="bench_user"
    )
    
    # 進行連續 3 次相同靜態查詢，觀察延遲變化
    for idx in range(3):
        t0 = time.time()
        result = await runner.run_async(
            user_id="bench_user",
            session_id=session.id,
            new_message="東京迪士尼樂園門票一日票多少錢？"
        )
        elapsed = (time.time() - t0) * 1000
        print(f"第 {idx+1} 次查詢耗時: {elapsed:.0f} ms")
        if idx == 0:
            print(f"回覆內容: {result.content.parts[0].text.strip()}\n")

asyncio.run(benchmark_latency())
```
> 💡 **快取成效分析** ：
> 第一次查詢（ 冷啟動 ）通常需要 **800 - 1200 ms** 進行文本讀取與嵌入；第二與第三次查詢在命中 **Context Cache** 後，延遲會顯著降至 **300 - 450 ms** ，且輸入計費降為原先的 25%。

---

### Lab 4：Path B — Agentic RAG 個人規劃

針對個人化行程規劃，我們將使用具備推理能力的 `gemini-2.0-pro-latest`。在執行前，我們透過自訂 Python 函數註冊工具（ Tool ），並載入 `PreloadMemory` 來讀取該使用者的歷史偏好。

```python
from google.adk.agents import LlmAgent
from google.adk.memory import PreloadMemory
from google.adk.runners import Runner
from google.adk.memory import VertexAiMemoryBankService
from google.adk.sessions import VertexAiSessionService
from vertexai.preview import rag
import asyncio

# 1. 宣告 Agent 的 Tool 函數 (ADK 會自動進行 Schema 包裝)
def search_travel_knowledge(query: str, top_k: int = 6) -> str:
    """搜尋旅遊知識庫，取得相關景點與費用片段。"""
    response = rag.retrieval_query(
        rag_resources=[rag.RagResource(rag_corpus="japan-travel-knowledge-base")],
        text=query,
        similarity_top_k=top_k,
    )
    chunks = [ctx.text for ctx in response.contexts.contexts]
    return "\n---\n".join(chunks) if chunks else "未找到相關資料"

def calculate_budget(items: list[dict]) -> str:
    """計算行程總費用，並以 JSON 結構回傳明細與總額。
    items 結構範例: [{'name': '迪士尼門票', 'cost_twd': 2500}]
    """
    total = sum(item['cost_twd'] for item in items)
    breakdown = "\n".join([f"- {i['name']}: NT$ {i['cost_twd']}" for i in items])
    return f"預算驗證結果:\n{breakdown}\n\n總計費用: NT$ {total}"

# 2. 建立具備推理、驗證、記憶感知的 Agentic RAG Agent
agentic_agent = LlmAgent(
    model="gemini-2.0-pro-latest",
    name="travel_agentic_planner",
    instruction="""
你是專業的旅遊規劃師。規劃行程時必須嚴格執行以下流程：
1. 查看系統預載的使用者旅遊記憶 (PreloadMemory)，主動排除已造訪的目的地。
2. 呼叫 search_travel_knowledge 檢索景點與房價。
3. 呼叫 calculate_budget 驗證所有消費是否在使用者預算限制內。若超支，必須重新調整。
4. 最終回覆需包含：每日行程路線、預算花費明細、貼心提示。
    """.strip(),
    tools=[
        search_travel_knowledge,
        calculate_budget,
        PreloadMemory() # 自動載入長期記憶 Profile
    ]
)

# 3. 初始化長期記憶體服務 (Memory Bank)
# 注意：AGENT_ENGINE_ID 將於 Lab 5 部署後取得，此處使用 mock_id
ENGINE_ID = "mock-agent-engine-id"
memory_service = VertexAiMemoryBankService(
    project="your-project-id", location="asia-northeast1", agent_engine_id=ENGINE_ID
)
session_service = VertexAiSessionService(
    project="your-project-id", location="asia-northeast1", agent_engine_id=ENGINE_ID
)

# 建立連接長期記憶體與狀態機的 Runner
runner = Runner(
    agent=agentic_agent,
    app_name="travel-agentic-app",
    session_service=session_service,
    memory_service=memory_service,
)
```

我們可以在本地手動模擬注入使用者的長期記憶（ 實際應用中，系統會在 Session 結束時非同步自動寫入 ）：

```python
async def seed_memory_and_run():
    user_id = "user_vip_99"
    
    # 模擬注入「過去對話所沉澱的長期記憶」
    await memory_service.add_fact_to_profile(
        user_id=user_id,
        fact="使用者在 2025/11 去過京都，且偏好自然與文化景點，討厭擁擠，孩子目前 7 歲。"
    )
    
    # 開啟新 Session 進行複雜查詢
    session = await session_service.create_session(
        app_name="travel-agentic-app", user_id=user_id
    )
    
    query = "幫我規劃 5 天日本行程，預算 8 萬台幣，我帶小孩去玩。請避開我之前去過的地方。"
    from google.genai import types
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    print("AI 開始進行多步思考、檢索與計算...")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.is_final_response():
            print("\n=== 最終行程推薦 ===")
            print(event.content.parts[0].text)
            
    # 對話結束後，觸發非同步 Memory Bank 萃取
    await memory_service.add_session_to_memory(
        app_name="travel-agentic-app", user_id=user_id, session_id=session.id
    )
    print("\n✓ 對話結束，新事實已非同步沉澱至長期記憶體。")

asyncio.run(seed_memory_and_run())
```

---

### Lab 5：部署至 Agent Engine 與安全治理

完成本地調試後，我們將整個應用包裝成 `AdkApp` 並部署到 Google Cloud 的 **Agent Engine** 上，並開啟安全防護閘道。

```python
import vertexai
from vertexai.Client import Client
from vertexai.agent_engines import AdkApp
from google.adk.apps import App

# 封裝 App
travel_app = App(
    name="travel-prod-app",
    root_agent=intent_router, # 以 Router 作為系統根節點
)
adk_app = AdkApp(agent=intent_router)

# 初始化託管平台客戶端並部署
client = Client(project="your-project-id", location="asia-northeast1")
remote_app = client.agent_engines.create(
    agent=adk_app,
    config={
        "requirements": [
            "google-cloud-aiplatform[agent_engines,adk]",
            "google-cloud-storage",
        ],
        "staging_bucket": "gs://your-project-id-staging",
        "display_name": "travel-search-prod",
    }
)
print(f"✓ 成功部署！資源名稱: {remote_app.resource_name}")
```

#### 🛡️ 設定安全治理 (Govern Layer)
部署完成後，使用 `gcloud` 啟用 **Agent Gateway** 並掛載 **Model Armor** 的安全防護範本，以阻擋惡意的 Prompt Injection（ 提示詞注入 ）攻擊與 PII（ 個人隱私資訊 ）外洩：

```bash
# 啟用 Gateway 與安全模組
gcloud vertex-ai agent-runtimes update travel-search-prod \
  --region=asia-northeast1 \
  --enable-agent-gateway \
  --model-armor-template=travel-safety-template
```

---

## 端到端查詢流式追蹤

當系統上線運行後，我們可以使用平台內建的 **Unified Trace Viewer** 追蹤請求的完整生命週期：

### 1. 查詢 A（ 靜態門票查詢 ）
* 使用者輸入：`「東京迪士尼樂園門票一日票多少錢？」`
* **Intent Router** 分析意圖，判定複雜度分數為 `0.12`，分流至 **Path A (CAG)** 。
* **Context Caching** 機制命中，直接調用預先快取的知識庫數據，跳過 RAG 重新嵌入的步驟。
* **Gemini Flash** 生成簡短回答。
* **總延遲：310 ms** （ 系統流圖中顯示無額外 Tool 呼叫 span ）。

### 2. 查詢 B（ 複雜個人規劃 ）
* 使用者輸入：`「規劃 5 天日本行程，預算 8 萬，帶小孩去，避開去過的地方。」`
* **Intent Router** 判定複雜度為 `0.94`，分流至 **Path B (Agentic RAG)** 。
* **Memory Bank** 自動加載該使用者的 Profile，讀出事實：`「曾去過京都、小孩 7 歲」`。
* **ADK Graph Workflow** 重寫 Query 為：`「適合 7 歲幼童、預算 8 萬台幣、排除京都的日本 5 天親子行程」`。
* 連續觸發 `search_travel_knowledge` 取回大阪與奈良的遊樂場與飯店資訊。
* 呼叫 `calculate_budget`，經計算後費用合計為 NT$ 77,500，符合預算限制。
* **Gemini Pro** 彙整生成詳盡的每日行程與費用拆解表。
* 會話結束後， **Memory Bank** 異步存入新偏好：`「對奈良餵鹿與大阪環球影城表現出高度興趣」`。
* **總延遲：2,840 ms** （ 平台 Trace Viewer 中可點開詳細的混合檢索與工具呼叫 span ）。

---

## 🚀 結論與未來進階

透過 **Gemini Enterprise Agent Platform** 的託管生態系統，我們在不需要自行維護資料庫伺服器與平行運算排程的情況下，成功構建出了一套「既快且準」的智慧旅遊搜尋系統。
* **Path A** 利用快取成功解決了傳統 RAG 系統的「首字延遲（ TTFT ）痛點」，實現了亞秒級極速響應。
* **Path B** 則通過 ADK 靈活的架構與長期記憶體（ Memory Bank ），解決了 AI 無法保持上下文記憶與無法精準控制預算的難題。

這套架構也為未來更廣泛的 **A2A (Agent-to-Agent)** 自主協作（ 如自動對接第三方訂房系統 API ）奠定了無縫擴展的基礎。
