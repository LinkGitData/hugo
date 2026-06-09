---
title: "SafeBite: A Three-Tiered AI Diet Assistant Tailored for Diabetics and High-Risk Groups"
date: 2026-06-09T10:05:00+08:00
draft: false
slug: "safebite-ai-diet-assistant-en"
tags: ["Gemini", "Flutter", "iOS Development", "Healthcare AI", "Vertex AI", "APAC GenAI Academy", "App Store Submission", "SaMD"]
categories: ["AI Projects"]
mermaid: true
cover:
  image: "images/safebite-cover.png?v=1"
  alt: "SafeBite AI Diet Assistant Cover"
  caption: "SafeBite: A smart dining assistant for blood sugar management"
  relative: false
---

> 🔗 **Event-Exclusive Project** : This project is developed exclusively for the [APAC GenAI Academy — Meet the Builders](https://hack2skill.com/event/apac-genaiacademy?tab=meetBuilders&utm_source=hack2skill&utm_medium=homepage) program. We aim to leverage Generative AI to bridge clinical education with real-time dining scenarios, providing a reliable, portable, and instant decision-support tool for blood sugar management.

---

## 🌟 A Dining Pain Point Impossible to Ignore: 'Can I Eat This?'

Every time I took my mother out for a meal, she would pause in front of the menu, a hint of hesitation and anxiety in her eyes, asking the same question: **"Can I eat this?"**

My mother had Type 2 diabetes. She was highly proactive about her health, taking her medication on time and attending regular check-ups. But when it came to dining out—which in Taiwan is almost a daily necessity—she was truly lost on what food was safe for her. It wasn't for a lack of effort; the information simply wasn't there. Restaurant menus don't label carbohydrates or Glycemic Index (GI). The dishes served looked completely different from the perfect illustrations in clinical education pamphlets. The doctor's advice to **"eat fewer high-sugar foods and watch your carb exchanges"** felt completely useless when standing in front of a bustling buffet or a complex menu.

Sadly, she passed away before I could finish this app. But that question lingered, weighing heavily on my heart.

As a developer, I often think: if technology cannot alleviate the suffering of those closest to us, what is its purpose? Perhaps Generative AI holds the answer. I do not want other families to experience that same helplessness at the dining table. This is where **SafeBite** began: not as a tech toy, but as a trustworthy voice right at the dining table for anyone navigating blood sugar management.

---

## 📋 Table of Contents

- [1. A Problem Bigger Than My Family: The Societal Challenge of Diabetes](#1-a-problem-bigger-than-my-family-the-societal-challenge-of-diabetes)
- [2. Introducing SafeBite: Your Portable AI Dining Companion](#2-introducing-safebite-your-portable-ai-dining-companion)
- [3. Hardware-Software Integration: Flutter iOS Native LiDAR and TrueDepth Depth Estimation](#3-hardware-software-integration-flutter-ios-native-lidar-and-truedepth-depth-estimation)
- [4. Three-Tiered AI Architecture: Balancing Speed, Cost, and Clinical Safety](#4-three-tiered-ai-architecture-balancing-speed-cost-and-clinical-safety)
- [5. Infrastructure and Full Tech Stack](#5-infrastructure-and-full-tech-stack)
- [6. Project Milestones and Acceptance Criteria](#6-project-milestones-and-acceptance-criteria)
- [7. App Store Submission and Regulatory Compliance Checklist](#7-app-store-submission-and-regulatory-compliance-checklist)
- [8. Project Risk Registry and Mitigation Strategies](#8-project-risk-registry-and-mitigation-strategies)
- [9. Fast-Track Demo Development Path for Gen AI Academy](#9-fast-track-demo-development-path-for-gen-ai-academy)
- [10. Honestly Addressing Estimation Errors: From Calculator to Decision Guardrail](#10-honestly-addressing-estimation-errors-from-calculator-to-decision-guardrail)
- [11. Conclusion and Future Outlook](#11-conclusion-and-future-outlook)

---

## 1. A Problem Bigger Than My Family: The Societal Challenge of Diabetes

In Taiwan, blood sugar management is not an isolated issue, but a major societal challenge:

1. **Massive Diabetic Population** : Taiwan has over **2.3 million** diagnosed diabetic patients—roughly 1 in 10 adults.
2. **Expanding Pre-diabetic Population** : According to the National Nutrition and Health Survey, approximately **6 million** people in Taiwan are pre-diabetic. Their blood sugar is already elevated, and insulin sensitivity has begun to decline. Although not yet clinically diagnosed, dietary intervention at this stage has a high chance of delaying or preventing the onset of Type 2 diabetes.

What this group needs most is guidance at the exact moment they make a choice. Existing solutions on the market fall into two main categories, both with significant pain points:

* **Traditional Nutrition Tracking Apps** : These require users to manually search for and log ingredients, weights, and cooking methods. This is highly tedious. Furthermore, restaurant food is complex; users cannot easily know how much oil, salt, or sugar went into a dish. Most users give up within a few weeks due to the friction.
* **Paper-based Clinical Education Booklets** : While medically accurate, they are static guidelines (e.g., "one exchange of starch equals a quarter-bowl of rice"). When facing a complex restaurant menu, it is difficult for users to translate this theory into immediate ordering decisions.

Neither approach works at the moment of decision-making. SafeBite's mission is to bridge this gap between clinical knowledge and table-side decisions.

---

## 2. Introducing SafeBite: Your Portable AI Dining Companion

SafeBite is an AI dining assistant designed specifically for blood sugar management. Built as a **Flutter application integrated with iOS native capabilities** , this setup directly addresses the most difficult bottleneck in food tracking: portion size estimation. By leveraging iOS hardware features (LiDAR scanners and TrueDepth cameras), we capture depth data to assist the AI in estimating volume, dramatically improving carbohydrate estimation accuracy.

### 🌟 Core SafeBite Workflow

```
Personalized Profile ➔ Food Logging via Photo ➔ Real-Time Menu Analysis ➔ Daily & Weekly Summary
```

### 1. Personalized Profile Setup
Upon first launching SafeBite, the system does not ask users to input complex calorie goals or macronutrient ratios. Instead, it builds a user profile through five simple questions:
* Age and gender
* Weight and height
* Current health status (diagnosed Type 2 diabetes, pre-diabetes, or high-risk group)
* Current medications or insulin usage
* Daily physical activity level

The backend automatically calculates a personalized **daily carbohydrate quota (in grams)** according to established medical guidelines. Different safety thresholds and alert parameters are applied for diagnosed patients versus pre-diabetic users, ensuring safety while offering flexibility to those who need it.

### 2. Food Logging via Photo
Before eating, users do not need to break down ingredients. They simply take a photo of their plate. SafeBite automatically identifies the food, estimates carbohydrate content, and deducts it in real-time from the daily quota. On LiDAR-equipped devices, the app retrieves depth data via platform channels to estimate the physical volume of the dish, preventing the AI from miscalculating due to visual perspective issues.

### 3. Real-Time Menu Analysis (Core Feature)
When ordering at a restaurant, users point the camera at a menu and snap a photo. SafeBite's AI engine instantly goes to work:
1. **Structure the Menu** : Automatically recognizes and extracts all options and prices from the menu.
2. **Compare with Quota** : Retrieves the user's consumed carbs for the day and the remaining balance.
3. **Generate Actionable Guidance** : Generates clear, personalized ordering recommendations.

For example, when a diabetic user with a remaining quota of 48g orders at a local diner, SafeBite's advice is not "choose low GI options," but rather:
> 💡 **SafeBite Suggestion** : "We suggest ordering the 'Steamed Fish Set'. Eat only half of the white rice (approx. 30g carbs). You can eat all the blanched vegetables, but ask the kitchen to skip the minced pork gravy. Avoid the 'Corn Chowder' as the starch thickening contains hidden carbs that will push you over today's limit."

This specific, actionable advice is what users truly need when deciding what to eat.

### 4. Daily and Weekly Summaries
SafeBite avoids creating constant tracking anxiety. Every evening after dinner or at 10 PM, the app pushes a minimal daily summary of the user's progress and a simple tip for the next day. Every Sunday, a weekly report is compiled to show the 7-day glycemic load trend, making it easy to share with physicians or dieticians during check-ups.

---

## 3. Hardware-Software Integration: Flutter iOS Native LiDAR and TrueDepth Depth Estimation

In dietary logging, the biggest bottleneck is that **"a single 2D image contains no scale information."** A plate of pasta looks identical on screen whether it is served on an 8-inch plate or a 12-inch platter. If an AI relies solely on visual pixel data, carb estimation errors can easily exceed 50%.

To solve this physical limitation, SafeBite uses a **Flutter hardware-software bridge** . On the iOS platform, we retrieve point cloud data and depth maps via ARKit and SceneKit:

```
[Flutter Frontend] ➔ Platform Channel ➔ [Swift / ARKit iOS Native] ➔ Retrieve LiDAR 3D Point Cloud ➔ Calculate Physical Volume
```

### 🛠️ Implementation and Platform Channel Bridge
We use Flutter's `MethodChannel` and `EventChannel` to connect Dart code with native Swift. When the camera is active, Swift initiates an `ARSession` and listens to depth data per frame:

1. **LiDAR Point Cloud Capture** : On LiDAR-equipped iPhones (iPhone 12 Pro and later), we capture 3D spatial coordinates via `ARFrame.rawFeaturePoints`.
2. **Depth Map Alignment** : For non-LiDAR devices with a TrueDepth camera (FaceID module), we retrieve depth maps during food selfie capture; alternatively, we calculate depth from dual-camera disparity (`AVDepthData`).
3. **Mesh Boundary Calculation** : When a user taps a food item on the screen, Swift performs a 3D raycast from the tap coordinate, identifies the bounding box of the food item, and calculates its physical volume (in cubic centimeters).
4. **Data Return to Flutter** : The calculated volume and image asset are packaged together and sent back to Dart, where they are attached as metadata when calling Google Cloud Vertex AI.

This hardware-software loop removes the blind spots of 2D image analysis, giving the AI crucial physical scale context.

---

## 4. Three-Tiered AI Architecture: Balancing Speed, Cost, and Clinical Safety

In healthcare and wellness applications, developers face a dual challenge: **response speed** (users standing in front of a menu cannot wait 30 seconds for feedback) and **clinical safety** (an incorrect AI decision, such as recommending a high-GI dish as safe, could cause acute hyperglycemia).

To solve this, we designed a **Three-Tiered AI Architecture** to balance speed, cost, and safety.

{{< mermaid >}}
graph TD
    UserTakePic[User takes photo of meal or menu] --> SendToTier1[Send to Tier 1 AI Recognition Layer]
    SendToTier1 --> Tier1Model[Gemini 3.1 Flash Lite detects food items]
    Tier1Model --> InstantResponse[Instant response in UI within 1-2s]
    InstantResponse --> CheckQuota[Compare with user remaining carb quota]
    CheckQuota --> SendToTier2[Send to Tier 2 AI Estimation and Suggestion Layer]
    SendToTier2 --> Tier2Model[Gemini 3.5 Flash estimates carbs and glycemic load]
    Tier2Model --> LiDARAssist[Incorporate iOS LiDAR depth data to calibrate portions]
    LiDARAssist --> Evaluator[Trigger high risk validation]
    Evaluator -- Yes: Low confidence or high glycemic mix sauce --> SendToTier3[Send to Tier 3 AI Clinical Validation Layer]
    Evaluator -- No --> OutputSuggestion[Output personalized ordering and adjustment suggestions]
    SendToTier3 --> Tier3Model[Gemini 3.1 Pro conducts clinical logic validation]
    Tier3Model --> CorrectSuggestion[Correct suggestions if necessary]
    CorrectSuggestion --> OutputSuggestion
    OutputSuggestion --> UserDecide[User gets actionable advice and decides]
{{< /mermaid >}}

### 🔍 Deep Dive into the Three Tiers

#### 1. Tier 1: Real-Time Detection —— Gemini 3.1 Flash Lite
* **Task** : Instantly recognize food items (e.g., braised pork rice, stir-fried cabbage, meatball soup) or convert menu images into structured text.
* **Latency** : **1 to 2 seconds** .
* **Design Rationale** : Users need immediate feedback after snapping a photo. Gemini 3.1 Flash Lite's fast inference detects objects in real-time, displaying bounding boxes and labels on screen. This establishes early trust—showing the user that the app "saw" the food.

#### 2. Tier 2: Carb Estimation and Suggestions —— Gemini 3.5 Flash
* **Task** : Process identified items, evaluate cooking preparation (e.g., stir-frying vs. steaming glycemic impacts), incorporate LiDAR volume data, cross-reference the user's profile and remaining quota, and generate structured dining advice.
* **Latency** : **3 to 5 seconds** .
* **Design Rationale** : This is the main workhorse layer. Gemini 3.5 Flash's strong multimodal capabilities handle our structured prompts, outputting clean JSON payloads for the Flutter frontend to render.

#### 3. Tier 3: High-Risk Validation —— Gemini 3.1 Pro
* **Task** : Perform clinical safety verification to protect user health.
* **Trigger Conditions** :
  * Tier 2 confidence score falls below 85%.
  * Food items belong to "high-risk mixed dishes" or "hidden glycemic categories" (e.g., starch-thickened soups, sweet teriyaki glaze, mixed hotpot ingredients).
  * User is diagnosed with diabetes, and their remaining quota is under 15g.
* **Design Rationale** : This layer is conditionally triggered to control Vertex AI API costs. When active, Gemini 3.1 Pro acts as a senior dietician, checking Tier 2 outputs: *“This dish contains vegetables, but the sauce is high in refined sugar. Since the user is on insulin, does this suggestion risk postprandial blood sugar spikes?”* If a risk is found, Gemini 3.1 Pro corrects the recommendation on the fly before it is displayed on screen.

---

## 5. Infrastructure and Full Tech Stack

SafeBite's operations rely on the integration of Google Cloud and Firebase. Below is the system architecture:

| System Component | Google Technology / Service | Specific Role and Configuration Details |
| :--- | :--- | :--- |
| **Frontend Application** | **Flutter (iOS)** | Cross-platform UI optimized for accessibility and smooth user flows. |
| **Hardware Sensors** | **ARKit via Platform Channel** | Interfaces with native iOS ARKit point cloud APIs to fetch volume metadata. |
| **Object Detection** | **Gemini 3.1 Flash Lite** | Low-latency food bounding box detection and initial tagging. |
| **Recommendation Engine** | **Gemini 3.5 Flash** | Multimodal reasoning combining volume metadata and user profile into JSON. |
| **Clinical Safety Gate** | **Gemini 3.1 Pro** | Conditionally triggered reasoning engine for clinical logic verification. |
| **AI Agent Orchestration** | **Vertex AI / Firebase AI Logic** | Securely encapsulates prompts and model configurations, preventing prompt injection. |
| **Backend Core API** | **Cloud Run** | Dockerized Node.js service managing business logic and routing between AI tiers. |
| **Async & Cron Jobs** | **Cloud Functions** | Handles weekly report compilation and schedules evening summaries via FCM at 10 PM. |
| **NoSQL Database** | **Firebase Firestore** | Stores onboarding profiles, daily consumption logs, and real-time quota balances. |
| **Blob Storage** | **Cloud Storage** | Securely hosts uploaded meal photos, with a 30-day auto-deletion lifecycle. |
| **Identity Authentication** | **Firebase Auth** | Handles secure sign-in, integrating Sign in with Apple to meet App Store requirements. |
| **Push Notifications** | **Firebase Cloud Messaging (FCM)** | Connects to Apple Push Notification service (APNs) for daily reminders and alerts. |

---

## 6. Project Milestones and Acceptance Criteria

For our internal engineering tracking, SafeBite's development is divided into five milestones, each with clear acceptance criteria:

### 🏁 M0: Infrastructure and Skeleton Setup
* **Timeline** : 2–3 Days (Full-Time) / 1 Week (Part-Time)
* **Tasks** :
  * Initialize Flutter project and set up basic iOS configurations.
  * Create Firebase project and link `GoogleService-Info.plist`.
  * Set up Firebase Auth, prioritizing Sign in with Apple to satisfy App Store guidelines.
  * Build Firestore collections for user profiles and daily logging structures.
  * Connect Vertex AI SDK and configure Firebase AI Logic routes.
  * Set up GitHub Actions CI/CD to automate TestFlight builds.
* **Acceptance Criteria** : Successful sign-in on a physical device, reading/writing test records to Firestore, and receiving a basic text response from Gemini.

### 🏁 M1: MVP / Core Demo (Key Presentation Milestone)
* **Timeline** : 3–4 Weeks (Full-Time) / 6–8 Weeks (Part-Time)
* **Tasks** :
  * Implement the 5-question onboarding questionnaire, saving metrics to Firestore.
  * Implement auto-calculation of daily carb limits based on health category.
  * Build the camera interface and connect the two-tier AI pipeline (Gemini 3.1 Flash Lite + Gemini 3.5 Flash).
  * Build the daily log accumulator (supporting flexible meal counts instead of a rigid three-meal structure).
  * Build the evening daily wrap-up screen.
* **Acceptance Criteria** :
  * User profile details write correctly to Firestore upon onboarding completion.
  * Snapping a photo of a typical Taiwanese meal (e.g., pork chop bento) returns carb estimates and dining advice **within 10 seconds** on a physical device.
  * Daily quota adjusts correctly across multiple meal logs.
  * **"Safe/Danger" direction classification achieves ≥ 80% accuracy** on a 20-image test set of local dishes (evaluating direction safety, not exact gram accuracy).

### 🏁 M2: Three-Tiered AI and Advanced Features
* **Timeline** : 1–1.5 Weeks (Full-Time) / 2–3 Weeks (Part-Time)
* **Tasks** :
  * Implement the Tier 3 Gemini 3.1 Pro conditional trigger pipeline.
  * Ensure validation and advice corrections happen before the UI renders.
  * Implement OCR menu parsing for structured dish selection.
  * Create Cloud Functions for weekly trend summaries.
  * Hook up FCM for scheduled push notifications at 10 PM.
* **Acceptance Criteria** :
  * Normal meals bypass Tier 3; starch-thickened soups or sweet sauces trigger Tier 3 validation and show corrected advice on screen.
  * **Tier 3 trigger rate is maintained under 30%** to keep API costs sustainable.
  * Daily summaries deliver on schedule via FCM.

### 🏁 M3: LiDAR / Depth Sensor Integration
* **Timeline** : 2–3 Weeks (Full-Time) / 4–6 Weeks (Part-Time)
* **Note** : **Highly recommended to defer to v1.5** .
* **Tasks** :
  * Establish platform channel communication with iOS ARKit.
  * Retrieve raw point cloud data and disparity visual maps.
  * Calculate physical bounding volume using native Swift helpers.
  * Feed calculated volume parameters into Gemini 3.5 Flash's prompts.
* **Acceptance Criteria** : Significant reduction in gram estimation errors on LiDAR-supported devices compared to the image-only baseline.

### 🏁 M4: Productization and App Store Submission
* **Timeline** : 3–5 Weeks (Full-Time) / 6–10 Weeks (Part-Time)
* **Tasks** :
  * Implement offline caching and sync queues for poor network connectivity.
  * Author a detailed Privacy Policy addressing health metrics and photo storage.
  * Implement the required "Delete Account and Data" workflow.
  * Add clear, permanent medical disclaimers in onboarding and suggestion footers.
  * Complete Privacy Nutrition Labels in App Store Connect.
  * Conduct extensive boundary testing using hundreds of local dishes.
* **Acceptance Criteria** : Passing all App Store review criteria, obtaining TestFlight Beta approval, and passing the final store review.

### 🏁 M5: Personalized Long-Term Memory & Agentic Analysis (v2 Target)
* **Timeline** : 3–5 Weeks (Full-Time) / 6–10 Weeks (Part-Time)
* **Tasks** :
  * **Long-Term Memory** : Integrate Vertex AI Agent Engine Memory Bank (GA) and Sessions. Retrieve historical preferences, meal-glucose patterns, and recent meds before generating Tier 2 advice.
  * **Data Analytics** : Stream daily log tables to Google Cloud BigQuery. Run BigQuery ML (`AUTO_ARIMA`) to predict high-risk glycemic periods for the upcoming week.
  * **Similarity Retrieval** : Use Vector Search 2.0 (GA) to retrieve similar historical meal images and glycemic responses in milliseconds.
  * **CGM Integration** : Interface with Continuous Glucose Monitor (CGM) APIs to inject glucose feedback loops into the Memory Bank.
* **Acceptance Criteria** :
  * AI suggestions reflect user preferences across multiple sessions.
  * Account deletion triggers immediate, verifiable erasure of both Firestore logs and Memory Bank entries.

---

## 7. App Store Submission and Regulatory Compliance Checklist

Submitting a wellness AI application to the App Store requires planning to avoid rejections or classification as a regulated medical device:

### 1. Store Distribution Strategy
* **Launch via TestFlight First** : During demo or pilot phases, distribute the app through TestFlight (supporting up to 10,000 testers). TestFlight reviews are less intensive, avoiding strict clinical verification bottlenecks during early demonstrations.

### 2. Copywriting and "De-medicalization" (Critical)
* **Avoid Medical Claims** : The store listing, screenshots, and in-app text **must not** contain terms like "diagnose," "treat," "cure," or "prevent diabetes."
* **Accurate Positioning** : Position the app as a "dietary awareness tracker" or "lifestyle carbohydrate helper."
* **Permanent Disclaimers** : Display clear disclaimers stating: *“This app is for educational and nutritional awareness only. It does not provide medical diagnosis or treatment. Consult a physician before making dietary changes.”*

### 3. Review Technical Requirements
* **In-App Account Deletion** : Users must be able to delete their account and all associated data from within the app. This must purge Firestore and Memory Bank data immediately.
* **Sign in with Apple** : If the app supports any third-party auth (e.g., Google Sign-In), it **must** offer "Sign in with Apple" with equal prominence (Apple Guideline 4.8).
* **Privacy Disclosures** : Publicly host a Privacy Policy, and declare "Health & Fitness" data collection in the App Store Privacy Nutrition Labels.

### 4. Software as a Medical Device (SaMD) Boundaries
* Under regulatory guidelines (such as TFDA in Taiwan or FDA in the US), software that "interprets clinical data to prescribe treatments or adjust drug dosages (e.g., calculating insulin units based on glucose readings)" is classified as a regulated medical device (SaMD).
* SafeBite remains in the **non-medical wellness assistant** zone by focusing only on lifestyle food substitutions (e.g., "eat half your rice") and refusing to manage medications or diagnostic assessments.

---

## 8. Project Risk Registry and Mitigation Strategies

We mapped out the primary technical and regulatory risks along with mitigation plans:

| Identified Risk | Potential Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Portion Volume Estimation Errors** | Miscalculating complex mixed dishes leads to incorrect remaining carb balance. | Frame UI around "Safety Zones (Safe/Moderate/Warning)" instead of precise grams. Build in a 10% safety margin in backend prompts. |
| **LiDAR Integration Delay** | ARKit point cloud processing stalls the development timeline. | Remove LiDAR from M1 path. Use visual reference objects (e.g., standard utensils) for v1, deferring LiDAR to v1.5. |
| **API Operational Cost Spikes** | Heavy usage of Tier 3 (Gemini 3.1 Pro) drives up Google Cloud Vertex AI fees. | Apply gatekeeper rules in Tier 2 to keep Tier 3 trigger rates **under 30%** of total calls. Set billing alerts and API caps. |
| **App Store Review Rejection** | App flagged for medical claims or missing compliance features. | Prioritize TestFlight distribution; remove medical claims from listing metadata; implement account deletion and Apple Login. |
| **Memory Bank Cost Overrun** | In v2, frequent Session logs to Agent Engine drive up RAG storage and compute costs. | Implement background filters to write only impactful dietary events to the Memory Bank. |
| **Health Data Privacy Violations** | Storing glucose and meal logs exposes the app to regulatory penalties. | Keep logs de-identified (do not store real ID numbers), and link account deletion directly to deep database deletion pipelines. |

---

## 9. Fast-Track Demo Development Path for Gen AI Academy

If your goal is to present a high-impact, functional demo for the Gen AI Academy Showcase or a hackathon, we recommend this **Fast-Track Path** :

```
[M0 Infrastructure] ➔ [M1 MVP (No LiDAR)] ➔ [M2 Orchestration (Tier 3 + Push)] ➔ [TestFlight Distribution]
```

1. **Defer M3 LiDAR Integration** : List LiDAR volume estimation as a "v1.5 Future Roadmap" feature. Use a simple visual cue instructing users to place a standard fork or coin next to their plate. This saves 2 to 3 weeks of native Swift/ARKit bridge testing.
2. **Avoid the Store Submission Bottleneck** : **Do not submit to the App Store.** Rely entirely on TestFlight. This allows judges to download the app onto physical devices via a public link, bypassing Apple's SaMD guidelines.
3. **Focus on Tiered Orchestration** : Focus your demo on showing how ordering a starch-heavy soup triggers Tier 3 (Gemini 3.1 Pro) to override Tier 2's suggestion on the fly. This showcases the orchestration capabilities of Gemini.

This fast-track plan delivers a working demo in **4–6 weeks (Full-Time) or 8–10 weeks (Part-Time)** .

---

## 10. Honestly Addressing Estimation Errors: From Calculator to Decision Guardrail

As developers applying AI to healthcare, we must remain honest and humble. We must accept that **"estimating exact macronutrients from images and depth sensors is physically impossible at a 100% accuracy level."**

In real-world testing, we face physical constraints:
* **Hidden Ingredients** : An AI detects stir-fried cabbage, but cannot know if the chef used lard, vegetable oil, or refined sugar.
* **Internal Density** : Facing a bowl of beef noodles, the scanner calculates superficial volume, but cannot know the ratio of broth, noodles, and beef hidden underneath.
* **Visual Occlusions** : Food items blocked behind other foods on the plate remain hidden from the camera.

If we position SafeBite as a "precision carb calculator," we risk creating a false sense of security, which is dangerous for insulin-dependent users.

### 🛡️ Pivoting to a "Guardrail"

Thus, we pivoted SafeBite's product design: **we position it as a dietary decision guardrail, not a scale.**

1. **Use Qualitative Ranges** : We avoid showing "52.4g carbs." Instead, the UI uses color-coded glycemic load ranges (Safe, Moderate, Alert).
2. **Focus on Substitutions** : Prompts focus on optimization. The AI tells the user: *“Eat only half the rice and remove the fried skin from the chicken, and this meal is safe.”* This guidance is easier to follow and absorbs estimation errors.
3. **Safety Margin Buffer** : We subtract a 10% safety margin from the remaining daily quota during prompt evaluation to account for physical measurement variance.

This is a responsible design choice for wellness AI. AI is not perfect, but with protective guardrails, it can still provide real, daily value.

---

## 11. Conclusion and Future Outlook

SafeBite was built to address a personal yet universal challenge. By combining Flutter's cross-platform UI with iOS hardware features and Google Cloud's Gemini models, we show that **Generative AI is not just for drafting emails—it can walk right into our lives and support chronic disease management.**

Debuting this project at the [APAC GenAI Academy — Meet the Builders](https://hack2skill.com/event/apac-genaiacademy?tab=meetBuilders&utm_source=hack2skill&utm_medium=homepage) program is just the beginning. Our roadmap includes:

* **Expanding to Other Chronic Conditions** : Adding models for chronic kidney disease (monitoring potassium, phosphorus, sodium) and gout (limiting purines).
* **Localized Database Enrichment** : Training RAG pipelines on regional cuisines and street food to improve classification accuracy.
* **CGM Sensor Integration** : Hooking into continuous glucose monitor APIs to create a closed-loop system that adjusts AI prompts based on the user's postprandial glucose curves.
* **Android Porting** : Migrating depth estimation algorithms to Android devices using ARCore's Depth API.

We believe the future of health management is decentralized, personalized, and immediate. SafeBite will continue to work so that every diabetic user can open a menu, look at their choices, and say: **"I can enjoy this meal with peace of mind."**
