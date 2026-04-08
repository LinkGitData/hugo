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

本文紀錄了在 macOS 環境中，不需繁雜設定，透過 **Ollama** 整合 Python 腳本，快速將 Google 最新支援多模態的 **Gemma 4 (e4b 版本)** 大模型落地運行的實戰筆記。

---

## 📋 目錄

1. [系統環境與 Gemma 4 模型選擇](#-系統環境與-gemma-4-模型選擇)
2. [系統架構：Ollama 與 Python 串接](#-系統架構ollama-與-python-串接)
3. [Ollama 安裝與自訂路徑實作](#-ollama-安裝與自訂路徑實作)
4. [實測：多模態影像解析 (玉山主峰)](#-實測多模態影像解析-玉山主峰)
5. [Benchmark 效能指標剖析](#-benchmark-效能指標剖析)
6. [結論與未來進階](#-結論與未來進階)

---

## 🏗️ 系統環境與 Gemma 4 模型選擇

在開始部署前，我們盤點了目前的硬體資源，這決定了我們可以乘載多大的模型：
*   **作業系統**：macOS
*   **開發環境**：Python 3.9.6
*   **記憶體**：16 GB RAM

在此前提下，我們選用了 **`gemma4:e4b`**。這款模型容量約 9.6 GB，專門為邊緣裝置設計，最大的優勢是在 16 GB 的規格下能穩定運行，且完美支援了「文字、圖片與音訊」的**多模態處理**能力。

> 💡 **經驗分享**：如果您的設備 RAM 小於 16GB，建議可以降級採用 `gemma4:e2b` (約 7.2 GB) 來確保推論時系統不會過載發燙。

---

## ⚙️ 系統架構：Ollama 與 Python 串接

我們設定這套系統為一個可以直接透過終端機 (CLI) 互動的腳本工具，以下是整體的資料流架構：

{{< mermaid >}}
graph LR
    User[使用者] -->|輸入參數或圖片| Bash[start.sh 腳本]
    Bash -->|參數傳遞| Py[chat.py Python 核心]
    
    subgraph Local LLM Engine
        Py -->|API 請求 + Base64 圖片| Ollama[Ollama 伺服器]
        Ollama -->|Load| Model[(Gemma 4:e4b)]
    end
    
    Ollama -->|串流生成 JSON Chunk| Py
    Py -->|渲染 Markdown 與 Benchmark| User
{{< /mermaid >}}

---

## 💻 Ollama 安裝與自訂路徑實作

為了保持開發環境乾淨，我們選擇不去動用到 Homebrew 及全域設定 (`sudo`)，而是結合 App Bundle 將執行檔提取出來，並使用環境變數綁定模型下載路徑。

### 1. 隔離式安裝

這是一個很靈活的本地測試技巧：

```bash
# 從 App bundle 複製分離 binary
mkdir -p /Users/yuting/Claude/bin
cp /Applications/Ollama.app/Contents/Resources/ollama ./bin/ollama
chmod +x ./bin/ollama

# 確認版本
./bin/ollama --version
```

### 2. 啟動與模型載入

利用 `OLLAMA_MODELS` 環境變數，強迫將高達近 10GB 的模型權重，指定下載至專案內的 `./models`，讓系統管理更為優雅。

```bash
# 啟動伺服器，將日誌背景輸出
OLLAMA_MODELS=/Users/yuting/Claude/models ./bin/ollama serve > ollama.log 2>&1 &

# 拉取 gemma4:e4b 模型 (花費約 12 分鐘)
OLLAMA_MODELS=/Users/yuting/Claude/models ./bin/ollama pull gemma4:e4b
```

> 🤖 **Agent Prompt**: 如果您設計自動化腳本，建議在執行對話 Python 前加入 health check：`curl -s http://localhost:11434/api/tags`，若沒有啟動再自行觸發。

---

## 🏞️ 實測：多模態影像解析 (玉山主峰)

最令人期待的多模態測試！我們傳送了一張大小高達 8.5 MB 的玉山紀念照片作為測試，並要求 Gemma 作出分析。

**CLI 執行腳本範例：**
```bash
./start.sh /image /Users/yuting/Claude/pic/Yushan.png "請詳細分析這張圖片，包括：景色內容、地點特徵、天氣、光線、拍攝角度，以及任何值得注意的細節。請用繁體中文回答。"
```

![玉山主峰分析測試圖片](/images/Yushan.png)

### Gemma 4 解析結果精華：
*   **⛰️ 地點判斷正確：** 精準認出石碑上的英文字「Mt. Jade Main Peak, 3952m」，認定為玉山主峰。
*   **📸 構圖理解：** 判斷為「略微仰角 (Low Angle) 拍攝」，強調了人物與大自然的壯闊對比。
*   **☁️ 氣候分析推理：** 從山下低垂雲海與高能見度判斷為晴朗，且透過「人物著防雪多層裝備」推理出高山具備強風特徵。

> 💡 **經驗分享**：Ollama API 處理多模態的邏輯，是將影像經過 Base64 編碼塞進 Payload 中的 `images` 陣列傳送，這意味著解析高畫質照片時會瞬間產生龐大的 Token 與處理時間。

---

## 📊 Benchmark 效能指標剖析

要成為一位 System Builder，必須嚴謹評估大模型的資源耗損。Ollama 的串流 API 提供了精確的數據讓我們調校系統：

| 指標項目 | 我們的實測數值 (8.5 MB 圖片) | 意義與說明 |
| :--- | :--- | :--- |
| **總耗時** | 131.4 秒 | 從發出請求到全文明轉錄的總花費時間。 |
| **首字延遲 (TTFT)** | 7.58 秒 | 使用者感覺到「AI 開始思考輸出」的時間，非常優異！|
| **Prompt 處理速度** | **277.4 t/s** (1.15 秒) | Gemma 分析大圖與大量 Prompt 飛快的讀取速度。 |
| **生成速度** | **20.4 t/s** (長達 2180 tokens) | 本地端運行能擁有 20 字/秒，閱讀不卡頓。 |

*註解：首次冷啟動 (Cold start) 載入模型需 6~20 秒，之後的熱啟動耗時將趨近於 0。*

---

## 🚀 結論與未來進階

透過 Ollama 與 Python 的輕量結合，我們不僅在 macOS 上成功建立了一座無需聯網即可使用的多模態 AI 工具庫，更為未來的自動化資料爬取、本地視覺辨識，奠定下強而有力的基礎。

**下一步的挑戰方向：**
1. **Chat 記憶體機制封裝**：利用 SQLite 將對話與圖片歷史保存，實現連續對話追問記憶。
2. **音訊轉換接合**：利用腳本自動裁切較長的錄音檔，分段匯入 Gemma 4，打造純本地的高精度語音會議紀錄機器人。

期待未來能夠在個人 AI OS (Personal AI OS) 內，將這些獨立模組整合成完全自動化的流程！

---

**[Cover Image Prompt]**
A futuristic data center or tech lab flowing with glowing nodes and code interfaces. In the center, a stylized robotic eye or lens representing "Multimodal Vision". High quality, tech vibe, subtle anime or modern flat illustration style, clean UI aesthetic, vibrant gradients, isometric perspective.
