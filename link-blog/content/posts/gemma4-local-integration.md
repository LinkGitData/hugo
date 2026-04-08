---
title: "🚀 輕量多模態 AI 實驗室：macOS 本地端建置 Gemma 4 與 Ollama 實戰"
date: 2026-04-08T11:35:00+08:00
draft: false
tags: ["Gemma 4", "Ollama", "Local LLM", "Multimodal", "Python"]
categories: ["AI Projects"]
mermaid: true
cover:
  image: "images/gemma4-local-integration-cover.png?v=1"
  alt: "Gemma 4 and Ollama Local Setup"
  caption: "Powered by Gemma 4:e4b on macOS"
  relative: false
---

在生成式 AI 的發展下，除了雲端大模型，將大型語言模型（LLM）部署在「本地端」並具備多模態（Multimodal）能力，已成為開發者與系統建構者（System Builder）的新趨勢。這不僅能大幅降低依賴外部 API 的成本，更能確保敏感資料（如私人圖片與文件）的絕對安全。

本文詳細紀錄了在 macOS 環境中，如何不需透過繁雜設定，透過 **Ollama** 整合 Python 腳本，完整體驗 Google 最新具備多模態能力的 **Gemma 4** 邊緣模型落地實戰。

---

## 📋 目錄

1. [環境確認與 Gemma 4 規格選擇](#-環境確認與-gemma-4-規格選擇)
2. [Ollama 隔離式安裝與模型下載](#-ollama-隔離式安裝與模型下載)
3. [核心系統：Bash 與 Python 對話腳本](#-核心系統bash-與-python-對話腳本)
4. [多模態結構與 CLI 命令模式](#-多模態結構與-cli-命令模式)
5. [實測示範：玉山主峰影像解析](#-實測示範玉山主峰影像解析)
6. [效能指標（Benchmark）詳解](#-效能指標benchmark詳解)
7. [Gemma 4 官方部署限制與開發須知](#-gemma-4-官方部署限制與開發須知)
8. [專案架構與完整使用手冊](#-專案架構與完整使用手冊)
9. [結論與未來進階](#-結論與未來進階)

---

## 🏗️ 環境確認與 Gemma 4 規格選擇

### 1. 本地實測環境

| 項目 | 說明 |
| :--- | :--- |
| **作業系統** | macOS |
| **開發工具** | Python 3.9.6, pip 23.2.1 |
| **硬體資源** | 16 GB RAM |
| **依賴套件** | 未安裝 Homebrew，未預先安裝 Ollama |

為了不干擾系統底層，我們採用 **方案 A：Ollama Binary + Python 腳本**，不強制依賴系統套件管理器。

### 2. Gemma 4 模型挑選

根據 Google 釋出的資訊，Gemma 4 提供多樣的參數量，我們評估了以下官方規格：

| 模型 Tag | 檔案大小 | 特性與說明 |
| :--- | :--- | :--- |
| `gemma4:e2b` | 7.2 GB | 邊緣裝置適用，支援文字/圖片/音訊。 |
| **`gemma4:e4b`** | **9.6 GB** | **邊緣裝置適用，支援文字/圖片/音訊 (✅ 本次選用)** |
| `gemma4:26b` | 18 GB | MoE (混合專家) 架構，需高硬體規格。 |
| `gemma4:31b` | 20 GB | Dense 模型架構。 |

> 💡 **經驗分享**：在 16 GB RAM 的基準下，`gemma4:e4b` 可以在不耗盡系統資源的前提下提供最高畫質的語義與圖片解析能力。

---

## 💻 Ollama 隔離式安裝與模型下載

### 1. 安裝與自訂路徑

若您不希望透過 `curl | sh` 的方式污染系統 PATH，可以像我們一樣利用 macOS App bundle 提取二進位執行檔：

```bash
# 從 App bundle 抽出二進位檔案放入專案的 bin 目錄
mkdir -p /Users/yuting/Claude/bin
cp /Applications/Ollama.app/Contents/Resources/ollama ./bin/ollama
chmod +x ./bin/ollama

# 確認是否可執行，應顯示 0.20.3 等版本號
./bin/ollama --version
```

### 2. 下載 Gemma 4 模型

我們使用 `OLLAMA_MODELS` 參數，強迫模型權重儲存於專案內：

```bash
# 背景啟動 Ollama 伺服器
OLLAMA_MODELS=/Users/yuting/Claude/models ./bin/ollama serve > ollama.log 2>&1 &

# 拉取 gemma4:e4b 模型
OLLAMA_MODELS=/Users/yuting/Claude/models ./bin/ollama pull gemma4:e4b
```

由於模型達 9.6GB，Ollama 會切分為約 16 個 600MB 的分片進行下載，在良好的網速下約需 **12 分鐘** 即可完成。最後可透過 `list` 指令確認模型就緒。

---

## 🛠️ 核心系統：Bash 與 Python 對話腳本

為了讓系統好用，我們製作了一套封裝腳本（包含 Bash 進入點與 Python 核心程式）。以下是資料流設計：

{{< mermaid >}}
graph LR
    User[使用者 CLI 輸入] --> Bash[start.sh]
    Bash -->|檢查 Ollama API| Check{伺服器狀態}
    Check -->|未啟動| Start[Ollama Serve]
    Check -->|已啟動| Py[chat.py]
    Start --> Py
    Py -->|多模態 Payload| Ollama[Gemma 4 API]
    Ollama -->|JSON 流| Py
    Py -->|渲染| User
{{< /mermaid >}}

### 啟動入口：`start.sh`
這支腳本負責自動依賴檢查，省去使用者手動開啟 Server 的麻煩。
```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export OLLAMA_MODELS="$SCRIPT_DIR/models"
OLLAMA="$SCRIPT_DIR/bin/ollama"

# 健康檢查 (Health Check)
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "啟動 Ollama 伺服器..."
    "$OLLAMA" serve > "$SCRIPT_DIR/ollama.log" 2>&1 &
    sleep 2
fi

# 判斷是否為單次查詢參數或進入互動模式
if [ $# -gt 0 ]; then
    python3 "$SCRIPT_DIR/chat.py" -- "$@"
else
    python3 "$SCRIPT_DIR/chat.py"
fi
```

而在 `chat.py` 核心中，它支援了 API 串流 (Streaming)、Benchmark 指標解析，以及**多模態輸入擷取**。

---

## 📂 多模態結構與 CLI 命令模式

### 多模態 Payload 格式
要讓 Gemma 4 成功「看見」圖片或「聽見」聲音，我們只需在 JSON 中加入 `images` 參數使用 Base64 編碼即可。支援了 `JPG`, `PNG`, `MP3`, `WAV` 等常見格式。

```python
# API 傳遞格式範例
{
    "role": "user",
    "content": "請描述這張圖片",
    "images": ["<base64_encoded_str>"] 
}
```

### CLI 參數快速運用
系統設計為可互動也能單次執行（適合寫成排程任務）：
```bash
# 純文字詢問
./start.sh "台灣最高峰是哪一座山？"

# 影像分析實測
./start.sh /image /path/to/photo.png "描述這張圖片的雲海"

# 多重圖片比較
./start.sh /image a.png /image b.png "比較兩張圖的色彩差異"
```

---

## 🏞️ 實測示範：玉山主峰影像解析

身為台灣的開發者，當然要測試最具代表性的地標。我們準備了一張高達 8.5 MB 的玉山紀念原圖。

**指令：**
```bash
./start.sh /image /Users/yuting/Claude/pic/Yushan.png "請詳細分析這張圖片，包括：景色內容、地點特徵、天氣、光線、拍攝角度，以及任何值得注意的細節。請用繁體中文回答。"
```

![玉山主峰分析測試圖片](/images/Yushan.png)

### Gemma 4 分析結果摘要
*   **⛰️ 地點特徵：** 正確讀出「Mt. Jade Main Peak, 3952m」，確認是玉山主峰人工砌石平台。
*   **☁️ 氣候與場景：** 觀測到「山下低垂雲海」、「晴朗高能見度」，並聰明地從「登山者多層次穿著搭配防風帽」推理出山峰具有**強風**環境。
*   **📸 視覺構圖：** 識別出使用了「略微仰角 (Low Angle)」的拍攝視角，形塑了大自然與人的壯闊對比美學。

> 💡 **經驗分享**：Gemma 4 對於中文石碑可能還略顯吃力，但其英文辨識 (OCR) 能力與自然環境推理的準確度十分驚人。

---

## 📊 效能指標（Benchmark）詳解

Ollama 的設計非常工程師友善，在回傳的最後一個資料 Chunk 當中，會附帶極度詳盡的效能消耗數據。我們將原始的 `.ns` (奈秒) 轉換為好讀的秒數。

**本次處理 8.5MB 高畫質圖片的數據：**

| 系統指標 | 實測表現 | 說明 |
| :--- | :--- | :--- |
| **總耗時** (`total_duration`) | 131.424 秒 | 從發送請求到收到最後一個字的總體驗時間。 |
| **模型載入** (`load_duration`)| 6.427 秒 | (冷啟動) 將 9.6GB 全推入記憶體的時間。 |
| **首字延遲** (**TTFT**) | 7.581 秒 | 載入模型加 Prompt 解析，到**第一個字印出**的延遲。非常快！ |
| **Prompt 速度** | **277.4 t/s** (1.15 秒) | Gemma 取用 Base64 轉換圖片與文字的速度，此階段吞吐極快。 |
| **生成速度** | **20.4 t/s** (長達 106.6 秒) | 生成了驚人的 `2180 tokens`，20 字/秒足以跟上人類閱讀節奏。 |

---

## ⚠️ Gemma 4 官方部署限制與開發須知

作為一套「開放權重 (Open-weights)」模型，Gemma 4 在本地端部署時有以下幾點官方限制與開發上的考量：

1. **硬體依賴**：算力完全吃本機資源。`e2b/e4b` 適合一般電腦，但高階的 `26B/31B` 需工作站級別 VRAM 才能順暢運行。
2. **上下文長度**：邊緣模型 (`e2b/e4b`) 最高支援 128K Tokens，大模型則支援至 256K Tokens。
3. **多模態差異**：全系列皆支援圖文，且小模型針對「音訊」有原生最佳化。但「影片」無法直接連貫讀取，需先拆分為連續單張影格 (Frames) 才能處理。
4. **開源與安全**：官方未公開原始訓練資料。此外，雖無 API 用量上限，但開發者須自行建構內容安全防護網。

---

## 📂 專案架構與完整使用手冊

最終，我們用如此單純的結構擁有了強大的本地 AI 解析庫。

### 專案目錄樹
```text
/Users/yuting/Claude/
├── bin/
│   └── ollama              # 隔離版的 Ollama 執行檔
├── models/
│   ├── blobs/              # 存放 9.6 GB 權重
│   └── manifests/          
├── pic/
│   └── Yushan.png          # 相關測試圖片存放
├── chat.py                 # Gemma 核心 Python 控制器
├── start.sh                # 使用者操作進入點
└── ollama.log              # 伺服器背景服務日誌
```

### 控制指令速查表
若您進入互動模式 (`./start.sh` 不帶變數)，可以隨時使用以下指令與系統交互：

| 指令 | 說明 | 注意事項 |
| :--- | :--- | :--- |
| `/image <路徑>` | 載入圖片進行下標 | 圖片越大，Prompt 轉換成 Base64 所花費的時間就越長。 |
| `/audio <路徑>` | 解析語音輸入 | 依賴 Ollama 底層支援，實驗性功能失敗時可換 `gemma4:e2b`。 |
| `/bench` | 再次印出效能表 | 無需重新耗電，直接重繪前一次的對話消耗指標。 |
| `/clear` | 清除記憶 | 將 context history 放空，防止胡言亂語。 |

> ⚠️ **手動重啟**：若要關閉背景伺服器釋放記憶體，請執行 `kill $(lsof -ti:11434)`。

---

## 🚀 結論與未來進階

採用 Ollama 二進位隔離安裝與簡單的 Python SDK 封裝，我們已經能流暢地在 MacBook 上「無雲端」安全解析大容量圖像。不僅保障圖片隱私，更掌握了效能精準的衡量指標。

隨著這套機制成熟，未來的**進階路徑**可以考慮：
1. **多輪對話持久化：** 在 `chat.py` 內建 SQLite，將圖文混合的上下文記憶下來。
2. **完全自動化 (Automation)：** 將分析後的資料串接 `Make` 或 `n8n`，實現諸如「丟張發票進資料夾，後台就自動用 Gemma 4 解析並輸出報表到 Google Sheets」。這也是個人 AI OS 系統構建的核心最終目標！
