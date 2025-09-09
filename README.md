# 🌍 Travel Assistant

<img width="1890" height="892" alt="image" src="https://github.com/user-attachments/assets/bc012f51-3ae9-4e01-96e8-2152505d5a96" />

A smart AI travel assistant that understands natural conversations and provides weather info, destination recommendations, packing lists, and local attractions.

##  What it does

- 🗣️ **Natural conversation** 
- 🌤️ **Weather data**
- 🎯 **Destination recommendations** 
- 🎒 **Packing lists** 
- 🏛️ **Local attractions**
- 🌐 **Web interface**
- 💻 **Command line**

##  Quick Start

### 1. Installation
```bash
# Clone the project
git clone <repository-url>
cd travel_assistant

# Install dependencies
pip install -r requirements.txt
```

### 2. API Keys
Create a `.env` file with your keys:
```env
GROQ_API_KEY=your_groq_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

**How to get keys:**
- **Groq:** [console.groq.com](https://console.groq.com/) - Free signup
- **Weather:** [openweathermap.org/api](https://openweathermap.org/api) - Free signup

## 📁 Project Files

| File | Description |
|------|-------------|
| `app.py` | Streamlit web interface |
| `main.py` | Main entry point with mode selection |
| `cli.py` | Command-line interface |
| `assistant.py` | Core AI assistant logic |
| `apis.py` | External API integrations (Groq, Weather) |
| `router.py` | Question classification and routing |
| `prompts.py` | AI prompt templates |
| `config.py` | Configuration settings |
| `test_run.py` |  Batch test suite |
| `test_debug.py` | Debug tools to show COT (Chain of Thought) behind the model's reasoning |
| `requirements.txt` | Python dependencies |
| `PROMPT_ENGINEERING.md` | Technical documentation |

## 🧠 Advanced Prompt Engineering

This project implements a modular, multi-pattern prompt engineering framework that enables the Travel Assistant to respond with both flexibility and reliability across diverse query types. Our prompts follow a Path-Based Prompting structure, where each system prompt is built around dual execution paths: 
(1) Clarification Path for vague user inputs, and (2) Direct Response Path for specific, well-formed questions. This approach ensures robustness and minimizes hallucinations by adapting response behavior to the input quality.


### Chain of Thought (CoT) Reasoning:
Used in the COMPLEX_REASONING_PROMPT, the model performs multi-step, internal logic to analyze constraints (e.g. budget, season, interests) and generate grounded destination recommendations.

### Constraint-Based Reasoning: 
Especially in CoT prompts, the model breaks down the user query, evaluates tradeoffs, and arrives at a final, justified recommendation.

### Few-Shot Learning: 
Several prompts include instructional demonstrations or examples, helping guide the LLM's behavior for classification, clarification, or structured responses.

### CogNitive Verifier Pattern: 
When queries lack critical context (destination, dates, interests), the assistant uses targeted, domain-specific questions to fill gaps before responding.

### Context-Aware Classification:
The UNIFIED_ANALYSIS_PROMPT classifies user intent (e.g. DESTINATION, PACKING) based on both current and previous turns, ensuring accurate multi-turn understanding.

### Anti-Hallucination Measures: 
Each prompt includes strict behavioral constraints, fallback strategies, and guardrails — especially for weather data or when information is uncertain.


##  Run
**🌐 Web interface:**
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

**💻 Command line:**
```bash
python main.py
```

**Ready to start planning your trip?** 🚀





