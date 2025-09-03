# test_run.py - Batch test suite for Travel Assistant
import logging
import time
from assistant import TravelAssistant

# Set up logging for test suite (separate from CLI)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('travel_assistant_test.log'),
        logging.FileHandler('travel_assistant_test.log', encoding='utf-8'),
        logging.StreamHandler()
    ],
    force=True  # Override any existing logging configuration
)

logger = logging.getLogger(__name__)

def run_test_suite():
    """Run comprehensive test suite for Travel Assistant"""
    
    # Initialize the assistant
    logger.info("=" * 80)
    logger.info("STARTING TRAVEL ASSISTANT TEST SUITE")
    logger.info("=" * 80)
    
    assistant = TravelAssistant()
    
    # Test questions organized by category
    test_questions = {
        "DESTINATION": [
            "Is it a good time to visit Rome in May?",
            "Should I go to Thailand in August?",
            "What are the best cities to visit in Japan?",
            "Is December a good month to go to New York?",
            "Which European country is best to visit in winter?",
            "What are the safest destinations in South America?",
            "Where should I go for a beach vacation in September?",
            "Should I visit Iceland in November?"
        ],
        
        "COMPLEX_REASONING": [
            # Chain of thought questions
            "Where should I go for vacation?",
            "What do you recommend for a trip?",
            "Best places to visit?",
            "Where should I go for a romantic getaway?",
            "Best places to travel with kids?",
            "Where should I go for an adventure trip?",
            "What's the best destination for a solo traveler?",
            "Where should I go for a cultural experience?"
        ],
        
        "PACKING": [
            "What should I pack for Tokyo in December?",
            "I'm going to Iceland next week, what clothes should I bring?",
            "What should I pack for a 5-day hiking trip in the Alps?",
            "Do I need warm clothes for Lisbon in April?",
            "Should I bring a raincoat for London in October?",
            "What should I pack for a beach holiday in Greece?",
            "What essentials do I need for a road trip across the US?",
            "Do I need adapters for my electronics in the UK?",
            # Open-ended questions that should trigger clarification
            "What should I pack?",
            "What do I need for my trip?",
            "Packing list?",
            "What should I bring?"
        ],
        
        "ATTRACTIONS": [
            "What are the top attractions in Paris?",
            "Tell me about the Louvre.",
            "What are the best restaurants in London?",
            "What can I do in Barcelona at night?",
            "What museums should I see in Berlin?",
            "What are the hidden gems in Lisbon?",
            "Is the Colosseum in Rome worth a visit?",
            "What are the best things to do in Bali?",
            # Open-ended questions that should trigger clarification
            "What should I see in Rome?",
            "What to do in Tokyo?",
            "Best attractions in Paris?",
            "What can I do in London?"
        ],
        
        # "WEATHER": [
        #     "What is the weather like in Paris tomorrow?",
        #     "Is it raining in London right now?",
        #     "Should I expect snow in New York in January?",
        #     "What is the average temperature in Madrid in July?",
        #     "Will it be hot in Dubai in August?",
        #     "How cold will it be in Moscow in winter?",
        #     "Do I need an umbrella in Singapore this week?",
        #     "Is there hurricane season in Miami in September?"
        # ],
        
        # "GENERAL": [
        #     "Can I travel from New York to London?",
        #     "How do I get to Tokyo airport?",
        #     "What is the history of Athens?",
        #     "How many hours does it take to fly from Los Angeles to Sydney?",
        #     "What currency is used in Morocco?",
        #     "Do I need a visa to visit Canada?",
        #     "How expensive is Switzerland compared to France?",
        #     "What language is spoken in Brazil?"
        # ]
    }
    
    total_questions = sum(len(questions) for questions in test_questions.values())
    current_question = 0
    
    # Run tests for each category
    for category, questions in test_questions.items():
        logger.info(f"\n{'='*20} TESTING {category} CATEGORY {'='*20}")
        
        for i, question in enumerate(questions, 1):
            current_question += 1
            logger.info(f"\n--- Question {current_question}/{total_questions} ({category} #{i}) ---")
            logger.info(f"Question: {question}")
            
            try:
                start_time = time.time()
                response = assistant.get_response(question)
                end_time = time.time()
                
                logger.info(f"Response: {response}")
                logger.info(f"Response time: {end_time - start_time:.2f} seconds")
                
                # Clear history between questions to avoid context bleeding
                assistant.clear_history()
                
            except Exception as e:
                logger.error(f"Error processing question: {e}")
                logger.error(f"Question: {question}")
            
            # Small delay between questions to be respectful to APIs (only for batch testing)
            time.sleep(2.0)  # 2 second delay for batch testing to avoid rate limits
    
    logger.info("\n" + "=" * 80)
    logger.info("TEST SUITE COMPLETED")
    logger.info("=" * 80)
    logger.info(f"Total questions tested: {total_questions}")
    logger.info("Check 'travel_assistant_test.log' for detailed logs")

if __name__ == "__main__":
    run_test_suite()
