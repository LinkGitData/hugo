---
title: "專案聚焦：Gemini 情感分析與實體識別"
date: 2025-12-08T12:05:00+08:00
draft: false
tags: ["Generative AI", "Gemini", "Flask", "Python", "Sentiment Analysis"]
categories: ["AI Projects"]
mermaid: true
cover:
  image: "images/ai-cover.png?v=7"
  alt: "Gemini 情感分析"
  caption: "Powered by Gemini 1.5 Flash"
  relative: false
---

在這篇文章中，我們將深入探討一個令人興奮的開源專案，該專案利用 Google 的 **Gemini 1.5 Flash** 模型對文字進行進階的情感分析和實體識別。這個名為 `gemini-sentiment-web` 的專案展示了如何將現代生成式 AI (Generative AI) 整合到簡單的 Flask Web 應用程式中。

> 🎮 **線上試玩**：您可以直接訪問 [Live Demo](https://sentiment.yuting.cc/) 來體驗情感分析功能。

## 🌟 專案概觀

此應用程式的核心目標是接收一段文字（例如客戶評論或社群媒體留言），並自動執行以下操作：

1.  **情感分析**：判斷語氣是正面、中性還是負面（細分為 7 個等級）。
2.  **實體提取**：識別文中提到的人名、地點或產品。
3.  **自動標註**：分配特定標籤，例如「產品品質（正面）」或「服務（負面）」。
4.  **解釋原因**：提供分析背後的理由，讓 AI 的判斷透明化。

## 🏗️ 系統架構

以下是該應用程式的運作流程：

{{< mermaid >}}
graph LR
    User[使用者] -->|輸入文字| Web[Flask Web 介面]
    Web -->|POST 請求 /analyze| App[App.py 後端邏輯]
    
    subgraph AI Processing
        App -->|API 呼叫| Vertex[Google Vertex AI]
        Vertex -->|Prompt 提示詞| Gemini[Gemini 1.5 Flash 模型]
        Gemini -->|JSON 回應| App
    end
    
    App -->|渲染結果| Result[分析報告頁面]
{{< /mermaid >}}

## 🛠️ 技術堆疊

*   **後端**：Python, Flask
*   **AI 模型**：Google Vertex AI (Gemini 1.5 Flash)
*   **監控**：Sentry (用於錯誤追蹤)
*   **部署**：支援 Docker / Cloud Run (內含 Procfile)

## 💻 程式碼深度解析

讓我們來看看 `app.py` 中發生了什麼魔法。

### 1. 模型初始化

首先，我們使用 `vertexai.preview.generative_models` 函式庫來載入 **Gemini 1.5 Flash** 模型。請注意我們給予 AI 一個「評論家」的角色設定。

```python
model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""你是很棒的評論家，你的服務很有幫助"""]
)
```

### 2. Prompt Engineering (提示詞工程)

任何 GenAI 應用程式最關鍵的部分就是 Prompt。這個專案使用結構化的 Prompt 來引導 Gemini 輸出程式碼容易解析的格式。

```python
def analyze_text(text):
    response = model.generate_content(
        f"""分析以下文字的情緒，並標註其中的實體且自動貼標：
        "{text}"
        情緒應為以下其中之一：非常正面、正面、稍微正面、中性、稍微負面、負面、非常負面。
        實體可以是人名、地名、組織名、產品名等。
        自動貼標可以是牛肉麵品質(正面)、炒飯品質(負面)、服務(正面)、環境(中性)、等候或處理時間(負面)、價格（正面）等。
        請用以下格式回答：
        情緒: <情緒>
        解釋: <情緒解釋>
        Gemini的解釋: <Gemini自己的情緒解釋>
        實體: <實體1>, <實體2>, ...
        自動貼標: <標籤1>, <標籤2>, ...
        """,
        # ... config
    )
    return response
```

### 3. 安全設定與參數配置

為了確保 AI 產出的內容安全簡潔，我們設定了 `max_output_tokens` 和安全性閾值。

```python
generation_config = {
    "max_output_tokens": 256,
    "temperature": 1.0,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    # ... 其他類別
}

```

## 🚀 為什麼這很重要

這個專案展示了軟體開發中的「Agent-First」方法。我們不需要從頭開始訓練情感分析模型（這通常需要大量數據和算力），而是簡單地**編排 (Orchestrate)** 一個強大的預訓練 LLM (Gemini) 來完成繁重的工作。

這種方法大幅縮短了開發時間，讓開發者能夠專注於**應用邏輯**和**使用者體驗**，而不是底層的機器學習基礎設施。

---

*在 GitHub 上查看完整原始碼：[LinkGitData/gemini-sentiment-web](https://github.com/LinkGitData/gemini-sentiment-web)*
