# config.py - Configuration and settings for Travel Assistant
import os
from dotenv import load_dotenv

# Fix encoding issues
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    if os.name == "nt":
        os.system("chcp 65001 >NUL")
except Exception:
    pass

# Load environment variables
load_dotenv()

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please create a .env file with your API key.")
MODEL_NAME = "llama-3.3-70b-versatile"

# Weather API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY not found in environment variables. Please add it to your .env file.")

# External APIs Configuration

# Model Parameters (can be overridden by environment variables)
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS_TOOL = int(os.getenv("MAX_TOKENS_TOOL", "128"))  # For classification/decision calls
MAX_TOKENS_GENERATION = int(os.getenv("MAX_TOKENS_GENERATION", "1024"))  # For final responses
MAX_TOKENS_DEBUG = int(os.getenv("MAX_TOKENS_DEBUG", "1024"))  # For debug mode with chain of thought

# Conversation settings (can be overridden by environment variables)
MAX_CONVERSATION_HISTORY = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))  # Keep last 10 messages for context

# Rate limiting settings
# Set to 1.0 for normal CLI use (balanced speed/reliability)
# Set to 2.0 for batch testing to avoid rate limits
API_DELAY_SECONDS = 1.0

# Debug settings
# Set to True to show chain of thought reasoning in responses (for evaluation/demonstration)
SHOW_CHAIN_OF_THOUGHT = os.getenv("SHOW_CHAIN_OF_THOUGHT", "false").lower() == "true"
