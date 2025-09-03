# 🧠 Prompt Engineering Decisions

This document outlines the key prompt engineering decisions made in the Travel Assistant project, explaining the rationale behind each design choice and how they contribute to the system's effectiveness.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Unified Analysis System](#unified-analysis-system)
3. [Specialized System Prompts](#specialized-system-prompts)
4. [Clarification System](#clarification-system)
5. [Chain of Thought Implementation](#chain-of-thought-implementation)
6. [Anti-Hallucination Measures](#anti-hallucination-measures)
7. [Context Management](#context-management)
8. [Performance Optimizations](#performance-optimizations)

## 🏗️ Architecture Overview

### Design Philosophy
The prompt engineering follows a **two-stage architecture**:
1. **Analysis Stage**: Unified classification and routing
2. **Generation Stage**: Specialized expert responses

This separation allows for:
- **Efficient routing** with minimal LLM calls
- **Specialized expertise** for each domain
- **Consistent classification** across all question types
- **Context-aware** decision making

## 🎯 Unified Analysis System

### Core Prompt: `UNIFIED_ANALYSIS_PROMPT`

**Purpose**: Single LLM call to classify questions, decide weather needs, extract locations, and determine clarification requirements.

**Key Design Decisions**:

#### 1. **JSON-Only Output**
```json
{
  "category": "DESTINATION|COMPLEX_REASONING|PACKING|ATTRACTIONS|WEATHER|GENERAL",
  "needs_weather": true|false,
  "mode": "current|forecast|climate|none",
  "city": "city_name|null",
  "country": "country_name|null", 
  "when": "time_reference|null",
  "needs_clarification": true|false
}
```

**Rationale**: 
- **Reliable parsing** - No ambiguity in response format
- **Structured data** - Easy to process programmatically
- **Error reduction** - Eliminates parsing inconsistencies

#### 2. **Explicit Clarification Rules**
```
VAGUE QUESTIONS that need clarification include: 
"Where should I travel?", "Where should I go for vacation?", 
"Where should I travel this year?", "What should I pack?", 
"What should I see?", "Best places to visit?"
```

**Rationale**:
- **Prevents generic responses** - Forces personalized recommendations
- **Improves user experience** - Gets specific details needed
- **Reduces hallucination** - Avoids making assumptions

#### 3. **Context-Aware Analysis**
```
IMPORTANT: Consider conversation context when available. 
If the user's question refers to previous conversation 
(like "that kind of trip", "for that destination"), 
use the context to understand what they're referring to.
```

**Rationale**:
- **Maintains conversation flow** - Understands follow-up questions
- **Reduces repetition** - Uses previous context intelligently
- **Natural interaction** - Mimics human conversation patterns

## 🎨 Specialized System Prompts

### Design Pattern: **Path-Based Prompts**

Each specialized prompt follows a **two-path structure**:

#### Path 1: Clarification
- **Trigger**: Vague or open-ended questions
- **Action**: Ask 2-3 targeted questions
- **Goal**: Gather specific details

#### Path 2: Direct Response
- **Trigger**: Specific questions with sufficient detail
- **Action**: Provide expert advice
- **Goal**: Deliver actionable information

### Example: `DESTINATION_SYSTEM_PROMPT`

```
CRITICAL RULE: You must choose ONLY ONE of the following two paths. Never do both.

---
PATH 1: ASK FOR CLARIFICATION
Use this path for VAGUE queries like "Where should I go?" or "What do you recommend?".
- YOUR TASK: Ask 2-3 targeted clarifying questions (Timing, Budget, Interests) to understand the user's needs. Do NOT provide any recommendations yet.

---
PATH 2: ANSWER DIRECTLY  
Use this path for SPECIFIC queries like "Is Rome good in May?" or "Should I visit Thailand?".
- YOUR TASK: Provide direct, detailed answers with practical information.
```

**Benefits**:
- **Clear decision logic** - Eliminates ambiguity
- **Consistent behavior** - Same pattern across all prompts
- **User guidance** - Explicit instructions for each scenario

## 🔍 Clarification System

### Design Principles

#### 1. **Targeted Question Framework**
Each category has specific clarifying questions:

**Destination Questions**:
- **Timing**: When do you want to travel?
- **Budget**: What's your budget range?
- **Interests**: What type of experience interests you most?
- **Travel Style**: Who are you traveling with?

**Packing Questions**:
- **Destination & Timing**: Where and when?
- **Trip Style**: Business, leisure, adventure?
- **Activities**: What activities do you plan?

**Attraction Questions**:
- **Time Frame**: How long are you staying?
- **Interests**: What interests you most?
- **Travel Style**: What's your pace?

#### 2. **Example-Driven Learning**
```
Examples of good clarifying responses:
- "I'd love to help you find the perfect destination! To give you the best recommendations, could you tell me: 1) When are you planning to travel? 2) What's your budget range? 3) What type of experience interests you most - relaxation, adventure, culture, or something else?"
```

**Rationale**:
- **Consistent tone** - Maintains friendly, helpful voice
- **Clear structure** - Numbered questions for easy response
- **Specific options** - Provides examples to guide user responses

## 🧩 Chain of Thought Implementation

### Design: `COMPLEX_REASONING_PROMPT`

**Purpose**: Multi-step reasoning for complex destination recommendations.

#### 1. **Structured Reasoning Process**
```
CORE PRINCIPLES (NON-NEGOTIABLE):
1. **Strict Constraint Adherence:** You MUST meticulously analyze and adhere to all explicit constraints in the user's query.
2. **Decisiveness:** Since the user has provided a detailed query, your goal is to provide a confident, final recommendation, NOT to ask for more information.
3. **Faithfulness:** Your final recommendation MUST be the direct and logical result of your internal reasoning process.
```

#### 2. **Dynamic Output Formatting**
```
{output_format_instructions}
```

**Normal Mode Instructions**:
- Keep responses to maximum 2-3 sentences total
- Focus on the primary recommendation
- Be concise and actionable

**Debug Mode Instructions**:
- Show the complete reasoning process
- Include all analysis steps
- Display decision rationale

#### 3. **Anti-Hallucination Measures**
```
CRITICAL ANTI-HALLUCINATION RULES:
- If you're not certain about specific details (hours, prices, exact names), generalize or say "check the official website"
- Never make up specific details you're not sure about
- If unsure about current information, suggest checking official sources
```

## 🛡️ Anti-Hallucination Measures

### Multi-Layer Protection

#### 1. **Prompt-Level Rules**
Every system prompt includes:
```
Rules:
- For hours/prices: only mention if you're certain, otherwise say "check the official website"
- If unsure about exact names/details, generalize or say "not sure"
- Avoid making up specific details you're not sure about
- If unsure about current information, suggest checking official sources
```

#### 2. **Structured Output Requirements**
```
You must respond with ONLY valid JSON. No other text.
Do not include any text before or after the JSON. No markdown.
Use lowercase booleans (true/false), no quotes around booleans.
```

#### 3. **Context Validation**
- **Weather data integration** - Uses real API data instead of assumptions
- **Location verification** - Geocoding validation for weather requests
- **Time reference handling** - Proper parsing of temporal expressions

## 🔄 Context Management

### Conversation History Integration

#### 1. **Smart Context Selection**
```python
context_messages = conversation_history[-4:]  # Last 4 messages (2 exchanges)
context_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context_messages])
```

**Rationale**:
- **Relevant context** - Only recent conversation matters
- **Token efficiency** - Limits context to essential information
- **Performance** - Reduces processing time

#### 2. **Context-Aware Classification**
```
- "So what should I pack for that kind of trip?" (with context about Spain in June) 
-> PACKING, needs_weather: true, mode: climate, city: null, country: Spain, when: June, needs_clarification: false
```

**Benefits**:
- **Natural follow-ups** - Understands pronoun references
- **Reduced clarification** - Uses previous context to fill gaps
- **Better user experience** - Maintains conversation flow

## ⚡ Performance Optimizations

### 1. **Unified Analysis**
**Before**: 3 separate LLM calls (classification + weather decision + location extraction)
**After**: 1 LLM call for all analysis

**Impact**: 
- **3x faster** analysis phase
- **Reduced API costs** - Fewer token usage
- **Better consistency** - Single reasoning process

### 2. **Token Management**
```python
MAX_TOKENS_TOOL = 128        # For classification/decision calls
MAX_TOKENS_GENERATION = 1024 # For final responses
MAX_TOKENS_DEBUG = 1024      # For debug mode with chain of thought
```

**Rationale**:
- **Efficient classification** - Short, focused prompts for analysis
- **Rich responses** - Adequate tokens for detailed answers
- **Cost optimization** - Right-sized tokens for each use case

### 3. **Caching Strategy**
```python
self.cache_duration = 300  # 5 minutes for weather data
```

**Benefits**:
- **Reduced API calls** - Weather data cached for 5 minutes
- **Faster responses** - Instant retrieval for recent requests
- **Cost savings** - Fewer external API calls

## 🎯 Key Success Factors

### 1. **Explicit Instructions**
Every prompt includes:
- **Clear role definition** - "You are a travel destination expert"
- **Specific task description** - "Your task is to respond to the user's query"
- **Concrete examples** - Real question-answer pairs
- **Anti-hallucination rules** - Explicit safety measures

### 2. **Consistent Patterns**
- **Two-path structure** - Clarification vs. Direct response
- **JSON output format** - Structured, parseable responses
- **Example-driven learning** - Consistent tone and format
- **Error handling** - Graceful degradation strategies

### 3. **Context Awareness**
- **Conversation history** - Maintains context across exchanges
- **Weather integration** - Real-time data for relevant responses
- **Location extraction** - Smart parsing of geographic references
- **Temporal understanding** - Handles time references correctly

#

