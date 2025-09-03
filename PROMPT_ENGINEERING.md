# Prompt Engineering Decisions

This document outlines the key prompt engineering decisions used in building the Travel Assistant system. The design focuses on conversation quality, reasoning structure, and safe interaction with external tools (e.g., weather APIs).

---

## 1. Dual-Path Prompt Logic (Clarification vs. Direct Answer)

Each expert prompt (destination, packing, attractions) is structured with **two exclusive paths**:

* **Path 1 – Ask for Clarification:**
  Triggered for vague queries (e.g., *"What should I pack?", "Where should I go?"*).
  The assistant asks 2–3 focused clarification questions before proceeding.

* **Path 2 – Answer Directly:**
  Used when the user provides specific details (e.g., *"What should I pack for Tokyo in December?"*).
  The assistant responds immediately with relevant, weather-aware information.

> ### Only one path may be followed — never both.

---

## 2. Unified JSON Classification Prompt

The assistant uses a **unified classification prompt** to analyze each user query and return structured JSON.
This enables downstream routing and minimizes hallucinations.

**Fields include:**

* `category`: e.g., `"DESTINATION"`, `"PACKING"`, `"COMPLEX_REASONING"`
* `needs_clarification`: Boolean to control flow
* `needs_weather`: Whether to fetch weather
* `mode`: `"climate"` / `"forecast"`
* `city`, `country`, `when`: Extracted location/time info

**Example output:**

```json
{
  "category": "PACKING",
  "needs_weather": true,
  "mode": "climate",
  "city": "Tokyo",
  "country": "Japan",
  "when": "December",
  "needs_clarification": false
}
```

---

## 3. Chain of Thought (COT) Prompting for Complex Recommendations

The `COMPLEX_REASONING_PROMPT` enables the assistant to provide high-quality, multi-constraint destination suggestions.  
I chose to implement **internal chain-of-thought reasoning** in 4 structured steps:

1. Deconstruct user constraints (e.g., "budget", "family", "nature", "May").
2. Analyze the tradeoffs (e.g., weather vs. cost).
3. Evaluate multiple options.
4. Synthesize one optimal recommendation and one runner-up.

>  I chose this pattern to **simulate a human decision-making process** and avoid shallow suggestions often produced by default LLM responses.

---

## 4. Weather-Aware Packing Prompts with Hard Constraints

The `PACKING_SYSTEM_PROMPT` uses a strict format to ensure consistency:

- Starts with a **required weather summary**
- Follows with a **concise 5–7 item list** (excluding generic items like toiletries)

>  I enforced these constraints to ensure that the output is **compact, weather-relevant**, and easy to parse or copy.

> This helped **prevent hallucinations** (e.g., suggesting swimsuits for snowy locations) and made the output feel reliable and expert-like.

---

## 5. Clarification System for Ambiguous Queries

All main prompts include a built-in **clarification path**, which asks the user key missing details (like location or timeframe).  
This was designed to avoid hallucinating answers for vague prompts and improve conversational realism.

>  Instead of guessing, the model behaves like a smart assistant — it **asks the right questions**, then waits.

This is handled both at the prompt level (via `PATH 1`) and in the JSON classification (`needs_clarification = true`).

---

## 6. Anti-Hallucination Measures

Several steps were taken to **reduce hallucinations**:

- In the `WEATHER_SYSTEM_PROMPT`, the model is told to:
  - Avoid fake forecasts  
  - Warn about missing data  
  - Recommend official sources

- In the packing prompt, the assistant is **forbidden from suggesting obvious or irrelevant items** (e.g., "passport").

> ⚠These defenses improved **trustworthiness** and avoided factual errors — especially when API data was missing or partial.

---

## 7. CogNitive Verifier Pattern

I designed our classification and reasoning prompts to include **self-verification** mechanisms:

- In the JSON classification, the LLM must **justify** whether clarification is needed
- In complex reasoning, it must **reason internally** before giving an answer

>  These design patterns reduce randomness and **force the LLM to think before speaking**.

---

## 8. Prompt Chaining with Context Memory

To maintain context across turns, I used a **prompt chaining architecture**:

- Each message is processed through:
  1. Classification
  2. Context analysis
  3. System prompt selection

- Previous messages (`conversation_history`) are passed into classification to resolve references like “that trip”.

>  This allows the assistant to **understand follow-ups** and maintain logical continuity — a key for natural conversations.


