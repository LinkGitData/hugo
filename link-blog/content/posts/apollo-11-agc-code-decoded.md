---
title: "🌑 破解 1969 年的神話：Apollo 11 原始碼「再次公開」的真實意涵"
date: 2026-04-17T11:42:37+08:00
draft: false
tags: ["Apollo 11", "AGC", "Software Engineering", "Real-Time Systems", "Public Domain"]
categories: ["Tech History"]
mermaid: true
cover:
  image: "images/apollo-agc-cover.png?v=1"
  alt: "Futuristic Apollo AGC Computer Code Flowing"
  caption: "Apollo AGC: The origin of modern real-time fault-tolerant systems."
  relative: false
---

近期網路上再次掀起一波關於 Apollo 11 導航電腦 (AGC) 原始碼的熱烈討論，但讓我們先講最重要的結論：**Apollo 11 的 AGC 原始碼並不是 2026 年才第一次出現在 GitHub 上的。**

目前 GitHub 上著名的 `chrislgarry/Apollo-11` 倉庫明確說明，這些 Apollo 11 指令艙 Comanche055 與登月艙 Luminary099 的 AGC 原始碼，來源是 Virtual AGC 專案與 MIT Museum 數位化的紙本資料，且授權標示為 Public domain。也就是說，這套飛行軟體與其模擬器早已長期公開，其初衷便是為了讓大眾能在現代電腦上重現與研究這些歷史級的系統。因此，近期的熱度比較像是「再次爆紅」或「重新被當作教材討論」，而非 NASA 在 2026 年突然首次解密。

## 📋 目錄

- [🔍 不只是懷舊：近期的熱議動態](#-不只是懷舊近期的熱議動態)
- [⚙️ 極限硬體下的奇蹟：系統工程的雛形](#️-極限硬體下的奇蹟系統工程的雛形)
- [🧠 技術力巔峰：真正強大的 4 大關鍵](#-技術力巔峰真正強大的-4-大關鍵)
- [🌍 改寫歷史：對現代工程的三大影響](#-改寫歷史對現代工程的三大影響)
- [🚀 結論與未來進階](#-結論與未來進階)

---

## 🔍 不只是懷舊：近期的熱議動態

回顧近三個月內，有幾個值得注意的相關動向。透過以下的時間軸，我們可以看出這份古老程式碼如何轉變為現代工程的熱門教材：

{{< mermaid >}}
timeline
    title 2026年 Apollo 11 原始碼熱議時間軸
    2026年3月底 : AI 逆向工程 : 現代工程師使用 AI 工具 : 重新解析 AGC 組合語言
    2026年4月上旬 : 歷史 Bug 澄清 : 網傳程式碼存在歷史問題 : 官方社群澄清當年已修復
    2026年4月中旬 : 科技媒體轉載 : 科技大廠與媒體大量報導 : 聚焦極限資源與效能對比
{{< /mermaid >}}

1. **科技媒體重新聚焦**：多家科技媒體重新報導了這份在 GitHub 上的 Public Domain 資源。媒體的焦點大多放在「用極少硬體資源完成登月」的強烈反差上。
2. **社群考古與 Debug**：出現了新一波的技術討論，有人聲稱在原始碼中找到了歷史 Bug；但 Virtual AGC 社群隨後澄清，該問題其實在當年測試階段就已被發現，只是這段歷史不為大眾所熟知。
3. **AI 逆向工程**：有現代工程師開始使用最新的 AI 工具去逆向解析這些組合語言。這象徵著這份舊時代的程式碼正式從「歷史文物」轉變為「現代軟體工程教材」。

---

## ⚙️ 極限硬體下的奇蹟：系統工程的雛形

就當時的技術來看，Apollo AGC 最驚人的，絕非單純「4KB 記憶體、74KB ROM、1MHz」這些近似數字。**真正令人敬畏之處在於，它在極端受限的資源下，做到了即時 (Real-time)、可靠且可恢復。**

> 💡 **精確的硬體規格釐清**
> 新聞媒體常簡寫為 4KB RAM / 74KB ROM / 1MHz 以方便傳播。更精確的寫法應為：
> - **Erasable Memory**: 約 3,840 bytes
> - **Fixed Memory (Rope Memory)**: 約 36K words
> - **時脈 (Clock Speed)**: 約 1.024 MHz

在今天，即便是最簡單的嵌入式裝置都會覺得這樣的資源捉襟見肘。但在 1969 年，這台 AGC 要負責導航、姿態控制、任務流程，還要與 DSKY 人機介面協作，並承受登月飛行過程中的種種不確定性。以下是 AGC 的核心互動架構：

{{< mermaid >}}
graph TD
    A[Apollo Guidance Computer AGC] -->|Fixed: 36K words| B(Rope Memory / 程式儲存)
    A -->|Erasable: 3,840 bytes| C(RAM / 變數與狀態)
    D[太空人 Astronauts] <-->|操作與顯示| E[DSKY 介面]
    E <-->|指令輸入 / 告警顯示| A
    A --> F[導航 Navigation]
    A --> G[姿態控制 Attitude Control]
    A --> H[下降引擎 Descent Engine]
    
    style A fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#fff
    style B fill:#334155,stroke:#64748b,color:#fff
    style C fill:#334155,stroke:#64748b,color:#fff
    style D fill:#475569,stroke:#f59e0b,color:#fff
    style E fill:#0f172a,stroke:#10b981,color:#fff
    style F fill:#1e293b,stroke:#0ea5e9,color:#fff
    style G fill:#1e293b,stroke:#0ea5e9,color:#fff
    style H fill:#1e293b,stroke:#ef4444,color:#fff
{{< /mermaid >}}

---

## 🧠 技術力巔峰：真正強大的 4 大關鍵

Apollo 11 的真正偉大，不是「小電腦居然能登月」，而是它把系統工程做到了近乎現代 **Safety-critical software (安全關鍵軟體)** 的雛形。

最經典的例子就是 **1201/1202 警報 (Alarm)**。根據 NASA 記載，當時電腦在下降過程中出現此警報時，系統會自動重啟，並優先恢復真正重要的工作。我們可以用以下的狀態圖來拆解這個在 1969 年就存在的「即時容錯」機制：

{{< mermaid >}}
stateDiagram-v2
    [*] --> Normal_Execution: 系統正常運行
    Normal_Execution --> Overload: 感測器資料過載 (如雷達異常)
    Overload --> Alarm_1201_1202: 觸發 1201/1202 資源耗盡警報
    Alarm_1201_1202 --> System_Reset: 發起軟體重啟 (Soft Reset)
    
    state System_Reset {
        [*] --> Task_Evaluator
        Task_Evaluator --> Drop_Low_Priority: 丟棄低優先級任務 (如螢幕更新)
        Task_Evaluator --> Keep_High_Priority: 保留高優先級任務 (優先姿態控制與下降)
    }
    
    System_Reset --> Normal_Execution: 穩定核心功能，完成登月
{{< /mermaid >}}

這段機制反映了 AGC 最強大的四大特質：

1. **硬體層面強在取捨，不盲目堆規格**：
   沒有多餘資源，每一個位元、中斷、記憶體配置都必須為任務服務。這是任務導向的極限設計，而非消費性電子邏輯。
2. **軟體層面強在高度可預測性**：
   現今很多系統算力龐大但行為難以預測；AGC 則是資源極少，但工程師完全知道系統在壓力與錯誤下會作何反應。1201/1202 能不致命，就是可預測設計的功勞。
3. **早熟的人機協作 (Human-Machine Interaction)**：
   AGC 並不是全自動的「完美神機」。它將「人」納入容錯閉環系統的一部分，這遠比假設機器永遠不可能出錯來得務實許多。
4. **極高的程式工程紀律**：
   觀察 GitHub 上的原始碼，其檔名、註解、模組邊界都極具工程結構化。它能跨越半世紀仍被現代 AI 分析與理解，這本身就是極高品質的證明。

> 🤖 **Agent Prompt: 現代工程視角**
> 從現代眼光來看，AGC 其實是一個超早期、極度精簡版的 **Real-time fault-tolerant system (即時容錯系統)**。任務優先級 (Priority)、容錯、降級運行 (Graceful Degradation)、關鍵任務保活，這些現代微服務都在用的概念，在 1969 年就已被付諸實踐。

---

## 🌍 改寫歷史：對現代工程的三大影響

針對這次的討論熱度，我認為 AGC 的歷史意義至少有三個層次：

1. **改寫「軟體只是配角」的歷史**
   Apollo 11 讓世界看到，關鍵任務不只靠火箭與機械，還要靠可驗證、可維持、可容錯的**軟體**。這對後來的航太、軍工、核能甚至醫療設備等產業的軟體工程觀念，產生了深遠的影響。
2. **推動嵌入式與即時系統的設計哲學**
   AGC 展示了一個核心原理：真正厲害的系統不是擁有最多資源，而是在最少資源下，仍能對最重要的事情做出正確反應。今天的飛控、汽車 ECU (電子控制單元) 及工控系統，都能看見其影子。
3. **轉化為跨世代的工程教育資產**
   這波熱度不單純是懷舊。當我們看到有人拿它做模擬器、用 AI 逆向工程找 Bug、討論錯誤恢復機制時，Apollo 11 的影響早已從「太空歷史」延伸到了「現代軟體工程方法論」。

---

## 🚀 結論與未來進階

Apollo 11 最震撼的地方，**不是用今天看來很弱的電腦登月，而是用今天依然先進的工程思維登月**。

硬體規格也許早就過時了，但它背後的設計哲學卻歷久彌新：**資源節制、優先級清楚、故障可恢復、人機分工明確、系統行為可驗證**。這也是為什麼當我們在 2026 年重新審視這份程式碼時，驚訝的不是它有多古老，而是它居然還這麼現代。

如果你對此感興趣，建議可以直接前往 GitHub 的 [chrislgarry/Apollo-11](https://github.com/chrislgarry/Apollo-11) 探索，或者使用 Virtual AGC 模擬器親自體驗這套跨時代的傳奇系統！
