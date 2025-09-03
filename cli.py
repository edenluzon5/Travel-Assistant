# cli.py - Simple command-line interface for testing
import logging
from assistant import TravelAssistant

# Configure CLI-specific logging (action steps go to log file only)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('travel_assistant_cli.log'),
        logging.FileHandler('travel_assistant_cli.log', encoding='utf-8'),
        logging.StreamHandler()
    ],
    force=True
)

# Set console logging to WARNING only (hide action steps from user)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

# Remove default console handler and add our custom one
root_logger = logging.getLogger()
for handler in root_logger.handlers[:]:
    if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
        root_logger.removeHandler(handler)
root_logger.addHandler(console_handler)

def main():
    """Main CLI interface for testing the travel assistant"""
    print("Travel Assistant - Your AI Travel Companion")
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("Type 'help' for more commands")
    print("-" * 50)
    
    # Initialize the assistant
    try:
        assistant = TravelAssistant()
        print("Assistant initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize assistant: {e}")
        print("Please check your .env file and API keys.")
        return
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye! Safe travels!")
                break
            elif user_input.lower() == 'clear':
                assistant.clear_history()
                print("Conversation history cleared!")
                continue
            elif user_input.lower() == 'help':
                print("\n Available commands:")
                print("  - quit/exit: End the conversation")
                print("  - clear: Clear conversation history")
                print("  - help: Show this help message")
                print("  - Any other text: Ask a travel question")
                continue
            elif not user_input:
                continue
            
            # Get response from assistant (action steps logged to file)
            response = assistant.get_response(user_input)
            print(f"\nAssistant: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Safe travels!")
            break
        except Exception as e:
            error_msg = str(e)
            if "rate limit" in error_msg.lower() or "429" in error_msg:
                print(f"\n  Rate limit reached. Please try again in a few minutes.")
            else:
                print(f"\n Error: {error_msg}")

if __name__ == "__main__":
    main()
