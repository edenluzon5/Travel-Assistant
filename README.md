# 🌍 Travel Assistant

A sophisticated conversational AI travel assistant built with LangChain and Groq API, featuring natural conversation flow, weather integration, and smart question classification.

![Travel Assistant Demo](https://via.placeholder.com/800x400/1E88E5/FFFFFF?text=Travel+Assistant+Demo)

## ✨ Features

- 🗣️ **Natural Conversation** - Context-aware chat with conversation history
- 🌤️ **Weather Integration** - Real-time weather data and forecasts
- 🧠 **Smart Classification** - Automatically categorizes travel questions
- 🎯 **Destination Recommendations** - Personalized travel suggestions
- 🎒 **Packing Suggestions** - Weather-aware packing advice
- 🏛️ **Local Attractions** - Information about places and activities
- 🔄 **Clarification System** - Asks for details when questions are too vague
- 🌐 **Web Interface** - Modern Streamlit chat interface
- 💻 **CLI Interface** - Clean command-line interface
- 🧪 **Batch Testing** - Comprehensive test suite

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd travel_assistant

# Install dependencies
pip install -r requirements.txt
```

### 2. API Keys Setup

Create a `.env` file in the project root with your API keys:

```env
# Required API Keys
GROQ_API_KEY=your_groq_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

#### 🔑 Getting API Keys

**Groq API Key:**
1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up/Login
3. Go to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

**Weather API Key:**
1. Visit [openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a free account
3. Go to API Keys section
4. Copy your API key to your `.env` file

### 3. Run the Application

**🌐 Web Interface (Recommended):**
```bash
streamlit run app.py
```
The web interface will open at `http://localhost:8501`

**💻 Command Line Interface:**
```bash
python main.py
```

**🧪 Test Suite:**
```bash
python test_run.py
```

## 🖥️ Interface Options

### Web Interface (Streamlit)
- **URL:** `http://localhost:8501`
- **Features:** 
  - Modern chat interface
  - Conversation history
  - Quick action buttons
  - Debug mode toggle
  - Responsive design

![Web Interface](https://via.placeholder.com/600x400/4CAF50/FFFFFF?text=Web+Interface+Chat)

### Command Line Interface
- **Command:** `python main.py`
- **Features:**
  - Clean conversation interface
  - Real-time responses
  - Command history
  - Logging to file

![CLI Interface](https://via.placeholder.com/600x300/FF9800/FFFFFF?text=Command+Line+Interface)

### Test Suite
- **Command:** `python test_run.py`
- **Features:**
  - 40+ test questions
  - All categories covered
  - Performance metrics
  - Detailed logging

![Test Suite](https://via.placeholder.com/600x300/9C27B0/FFFFFF?text=Test+Suite+Results)

## 🎯 Usage Examples

### Weather Questions
```
User: What's the weather like in Tokyo tomorrow?
Assistant: Tomorrow's forecast for Tokyo: 18°C to 22°C, partly cloudy, humidity 65%
```

### Destination Recommendations
```
User: Where should I go for a cultural trip in June?
Assistant: I'd love to help you find the perfect destination! To give you the best recommendations, could you tell me: 1) What's your budget range? 2) What type of experience interests you most - relaxation, adventure, culture, or something else? 3) Are you traveling solo, as a couple, or with family?
```

### Packing Suggestions
```
User: What should I pack for Tokyo in December?
Assistant: Based on the forecast for Tokyo in December, expect cold weather with average temperatures around 8°C (46°F) and occasional rain.

Here's a concise packing list for your trip:
* A warm, waterproof coat is essential
* Layering items like sweaters or fleece jackets
* Comfortable, waterproof boots for walking
* A warm hat, gloves, and a scarf
* A compact umbrella for the rain
```

### Follow-up Questions
```
User: So what should I pack for that kind of trip?
Assistant: [Uses conversation context to understand "that kind of trip" refers to the previous Spain recommendation]
```

## 🏗️ Project Structure

```
travel_assistant/
├── 🌐 app.py                 # Streamlit web interface
├── 🚀 main.py               # Single entry point with mode selection
├── 💻 cli.py                # Command-line interface
├── 🧠 assistant.py          # Main assistant logic and orchestration
├── 🔌 apis.py               # External API integrations (Groq, Weather)
├── 🎯 router.py             # Question classification and routing
├── 📝 prompts.py            # Prompt templates and system messages
├── ⚙️ config.py             # Configuration and settings
├── 🧪 test_run.py           # Batch test suite
├── 📋 requirements.txt      # Python dependencies
├── 🔐 .env                  # API keys (create this file)
└── 📊 *.log                 # Log files
```

## 🔧 Configuration

### Performance Settings
- **API Delay:** `1.0` seconds (adjustable in `config.py`)
- **Max Tokens:** `1024` for responses, `128` for classification
- **Conversation History:** Last 10 messages kept for context
- **Cache Duration:** 5 minutes for weather data

### Debug Mode
Set `SHOW_CHAIN_OF_THOUGHT=true` in your `.env` file to see internal reasoning:
```env
SHOW_CHAIN_OF_THOUGHT=true
```

## 🧪 Testing

### Batch Test Suite
```bash
python test_run.py
```
Tests 40+ questions across all categories:
- Weather questions
- Destination recommendations  
- Packing suggestions
- Local attractions
- General travel advice

### Manual Testing
```bash
python main.py
# Choose option 1 for interactive CLI
# Choose option 2 for test suite
# Choose option 3 for web interface
```

## 📊 Supported Question Types

| Category | Examples | Features |
|----------|----------|----------|
| **Weather** | "What's the weather in Paris tomorrow?" | Current weather, forecasts, climate data |
| **Destination** | "Is Rome good in May?" | Specific destination advice |
| **Packing** | "What should I pack for Tokyo in December?" | Weather-aware packing lists |
| **Attractions** | "What are the top attractions in Paris?" | Local places and activities |
| **Complex Reasoning** | "Best places for families on a budget?" | Multi-step recommendations |
| **General** | "Travel tips for Europe" | General travel advice |

## 🔄 Conversation Flow

1. **Question Analysis** - Classifies the question type
2. **Context Check** - Uses conversation history for follow-ups
3. **Weather Integration** - Fetches weather data if needed
4. **Response Generation** - Uses appropriate system prompt
5. **History Update** - Stores conversation for context

## 🛠️ Troubleshooting

### Common Issues

**Rate Limit Errors:**
- Increase `API_DELAY_SECONDS` in `config.py`
- Check your Groq API usage limits

**Weather API Errors:**
- Verify your OpenWeatherMap API key
- Check API key permissions

**Import Errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### Logs
- **CLI Logs:** `travel_assistant_cli.log`
- **Test Logs:** `travel_assistant_test.log`
- **Debug Info:** Check console output for detailed logs

## 📈 Performance

- **Response Time:** 2-5 seconds per question
- **Accuracy:** High classification accuracy with context awareness
- **Rate Limits:** Built-in retry logic and exponential backoff
- **Caching:** Weather data cached for 5 minutes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📚 Documentation

### Technical Documentation
- **[Prompt Engineering Guide](PROMPT_ENGINEERING.md)** - Detailed explanation of key prompt engineering decisions, architecture choices, and design rationale

### Key Prompt Engineering Decisions
The Travel Assistant uses a sophisticated prompt engineering approach:

- **Two-Stage Architecture**: Unified analysis + specialized generation
- **Context-Aware Classification**: Uses conversation history for follow-up questions
- **Anti-Hallucination Measures**: Built-in safety rules and validation
- **Clarification System**: Asks for details when questions are too vague
- **Chain of Thought**: Multi-step reasoning for complex recommendations
- **Performance Optimization**: Single LLM call for analysis, efficient token usage

See [PROMPT_ENGINEERING.md](PROMPT_ENGINEERING.md) for complete technical details.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq** for the fast LLM API
- **OpenWeatherMap** for weather data
- **LangChain** for the LLM framework
- **Streamlit** for the web interface

---

**Ready to start your travel planning journey?** 🚀

Run `streamlit run app.py` and start chatting with your AI travel assistant!