---
title: "Project Spotlight: Gemini Sentiment Analysis & Entity Recognition"
date: 2025-12-08T11:57:00+08:00
draft: false
tags: ["Generative AI", "Gemini", "Flask", "Python", "Sentiment Analysis"]
categories: ["AI Projects"]
cover:
  image: "images/ai-cover.png" # Temporary: reusing the manga style cover
  alt: "Gemini Sentiment Analysis"
  caption: "Powered by Gemini 1.5 Flash"
  relative: false
---

In this post, we'll dive into an exciting open-source project that leverages Google's **Gemini 1.5 Flash** model to perform advanced sentiment analysis and entity recognition on text. This project, `gemini-sentiment-web`, demonstrates how to integrate modern Generative AI into a simple Flask web application.

## 🌟 Project Overview

The core goal of this application is to take a piece of text (like a customer review or social media comment) and automatically:

1.  **Analyze Sentiment**: Determine if the tone is Positive, Neutral, or Negative (with 7 levels of granularity).
2.  **Extract Entities**: Identify key people, places, or products mentioned.
3.  **Auto-Labeling**: Assign specific tags like "Product Quality (Positive)" or "Service (Negative)".
4.  **Explain**: Provide a reason for the analysis, making the AI transparent.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask
*   **AI Model**: Google Vertex AI (Gemini 1.5 Flash)
*   **Monitoring**: Sentry (for error tracking)
*   **Deployment**: Docker / Cloud Run ready (Procfile included)

## 💻 Code Deep Dive

Let's look at how the magic happens in `app.py`.

### 1. Model Initialization

First, we utilize the `vertexai.preview.generative_models` library to load the **Gemini 1.5 Flash** model. Note the system instruction giving the AI a persona.

```python
model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""你是很棒的評論家，你的服務很有幫助"""]
)
```

### 2. Prompt Engineering

The most critical part of any GenAI application is the prompt. This project uses a structured prompt to guide Gemini's output into a specific format that the code can parse easily.

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

### 3. Safety Settings & Configuration

To ensure the AI produces safe and concise content, we configure `max_output_tokens` and safety thresholds.

```python
generation_config = {
    "max_output_tokens": 256,
    "temperature": 1.0,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    # ... other categories
}
```

## 🚀 Why This Matters

This project illustrates the "Agent-First" approach to software development. Instead of training a custom sentiment model from scratch (which requires massive datasets and compute), we simply **orchestrate** a powerful pre-trained LLM (Gemini) to do the heavy lifting.

This approach drastically reduces development time and allows developers to focus on the **application logic** and **user experience** rather than the underlying ML infrastructure.

---

*Check out the full source code on GitHub: [LinkGitData/gemini-sentiment-web](https://github.com/LinkGitData/gemini-sentiment-web)*
