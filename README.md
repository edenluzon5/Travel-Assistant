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

###  Run
**🌐 Web interface (recommended):**
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

**💻 Command line:**
```bash
python main.py
```

**Ready to start planning your trip?** 🚀



