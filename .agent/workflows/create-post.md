---
description: 根據提供的內容或草稿，產生統一規格的 Hugo 部落格文章
---
當使用者呼叫此 Workflow (例如輸入 `/create-post` 並附帶一段草稿、筆記或想法) 時，請嚴格執行以下任務：

1. **分析主題**：仔細閱讀使用者提供的內容，提取出核心重點，並為其定出一個專業且具吸引力的「文章主題」。
2. **套用版型生成文章**：遵守下方的【系統寫作規範】來撰寫完整的部落格文章。

### 🤖 系統寫作規範

請以「專業技術部落格作者」的身分，套用以下格式、風格與結構。

**【風格與語氣】**
*   **語氣：** 專業、條理清晰、具備吸引力，帶有「科技實驗室/探險者」的調性。
*   **排版：** 善用標題、條列式清單、**粗體**標示關鍵字，提升文章的可掃視度。請以「繁體中文」輸出所有內容。
*   **視覺引導（非常重要）：** 在 H2 標題 (`##`) 前面必須加上適合的 Emoji（例如：🌟、📋、🏗️、💻、🚀、🤖 等）。善用引言區塊 (`>`) 來標示重點提示 (`> 💡 **經驗分享**：`) 、程式碼提示 (`> 🤖 **Agent Prompt**:`) 或 Live Demo 連結。

**【Frontmatter 結構】**
最開頭必須嚴格包含以下 YAML Frontmatter：
```yaml
---
title: "[為文章產生的專業性標題]"
date: [請填寫當前時間，格式必須為 ISO 8601，如：2026-04-08T12:00:00+08:00]
draft: false
tags: ["[根據內容萃取的標籤1]", "[標籤2]"]
categories: ["[適當的分類，例如：Tech, AI Projects, Web Development 之一]"]
mermaid: true # 若內容會產生架構流程圖請設為 true，否則省略此欄位
cover:
  image: "images/[與主題相關英文短名稱]-cover.png?v=1"
  alt: "[簡短的英文圖片替代文字]"
  caption: "[簡短的圖片說明]"
  relative: false
---
```

**【必須包含的預期文章結構】**
1.  **前言/導言**：簡要介紹技術核心或該篇筆記解決了什麼痛點。
2.  **## 📋 目錄**：利用 Markdown 與錨點連結建立目錄清單。
3.  **本文段落 (H2)**：根據使用者的內容展開具體的技術章節，請為標題配上對應的 Emoji。
    * 若可將概念圖解，請優先使用 Hugo 的 `{{< mermaid >}}` 短代碼繪製架構圖/資料流圖。
    * 若有程式碼，必須使用有語言標籤 (如 `python` 或 `bash`) 的 Code Block。
4.  **## 🚀 結論與未來進階**：統整全篇觀念並給予下一步的行動建議。

**【封面圖片生成 (Cover Image Prompt)】**
在文章的最末端（以 `---` 水平線與正文隔開），請提供一段給 AI 繪圖工具（如 Midjourney / DALL-E）的「封面圖片生成 Prompt」。
*   **使用英文撰寫。**
*   **風格需求：** High quality, tech vibe, subtle anime or modern flat illustration style, clean UI aesthetic, vibrant colors.
*   **畫面內容：** 根據文章核心技術自由發揮，例如："A futuristic data center flowing with glowing nodes..."。

### 3. 主動協助保存
文章生成並展示給使用者確認後，主動詢問使用者：「是否需要我將這篇文章直接寫入專案的 `link-blog/content/posts/[檔案名稱].md` 中？」。
如果使用者同意，請呼叫 `write_to_file` 工具建立該檔案 (檔名須為英文小寫連字號格式)。
