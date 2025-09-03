# 🌍 Travel Assistant

A smart AI travel assistant that understands natural conversations and provides weather info, destination recommendations, packing lists, and local attractions.

## ✨ What it does

- 🗣️ **Natural conversation** - Remembers context from previous messages
- 🌤️ **Weather data** - Real-time weather and forecasts
- 🎯 **Destination recommendations** - Personalized travel suggestions
- 🎒 **Packing lists** - Smart advice based on weather
- 🏛️ **Local attractions** - Info about places and activities
- 🌐 **Web interface** - Modern and friendly chat
- 💻 **Command line** - Simple and fast

## 🚀 Quick Start

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

### 3. Run
**🌐 Web interface (recommended):**
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

**💻 Command line:**
```bash
python main.py
```

**🧪 Testing:**
```bash
python test_run.py
```

## 🎯 Usage Examples

**Weather:**
```
"What's the weather like in Tokyo tomorrow?"
```

**Destinations:**
```
"Where should I go for a cultural trip in June?"
```

**Packing:**
```
"What should I pack for Tokyo in December?"
```

**Attractions:**
```
"What are the best attractions in Paris?"
```

## 📊 Supported Question Types

| Category | Examples |
|----------|----------|
| **Weather** | "What's the weather in Paris tomorrow?" |
| **Destinations** | "Is Rome good in May?" |
| **Packing** | "What should I pack for Tokyo in December?" |
| **Attractions** | "What are the best attractions in Paris?" |
| **General** | "Travel tips for Europe" |

## 🛠️ Troubleshooting

**API errors:**
- Check your keys are correct in `.env`
- Wait a bit if there's rate limiting

**Installation errors:**
- `pip install -r requirements.txt`
- Python 3.8+ required

## 📈 Performance

- **Response time:** 2-5 seconds per question
- **Accuracy:** High with context awareness
- **Memory:** Remembers last 10 messages

---

**Ready to start planning your trip?** 🚀

Run `streamlit run app.py` and start chatting with your smart assistant!
