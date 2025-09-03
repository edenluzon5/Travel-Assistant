# assistant.py - Main Travel Assistant class and conversation management
import logging
from apis import LLMService, WeatherService  # TripAdvisorService disabled
from router import Router
from config import MAX_CONVERSATION_HISTORY, MAX_TOKENS_GENERATION, MAX_TOKENS_DEBUG, SHOW_CHAIN_OF_THOUGHT
from prompts import (
    DESTINATION_SYSTEM_PROMPT, COMPLEX_REASONING_PROMPT, NORMAL_MODE_INSTRUCTIONS, DEBUG_MODE_INSTRUCTIONS, 
    PACKING_SYSTEM_PROMPT, ATTRACTIONS_SYSTEM_PROMPT, WEATHER_SYSTEM_PROMPT, FALLBACK_SYSTEM_PROMPT
)

# Set up logging
logger = logging.getLogger(__name__)

class TravelAssistant:
    def __init__(self):
        """Initialize the travel assistant"""
        self.llm_service = LLMService()
        self.weather_service = WeatherService()
        self.router = Router()
        self.conversation_history = []
        
        # Category to system prompt mapping
        self.prompt_map = {
            "DESTINATION": DESTINATION_SYSTEM_PROMPT,
            "COMPLEX_REASONING": None,  # Will be set dynamically using unified prompt
            "PACKING": PACKING_SYSTEM_PROMPT,
            "ATTRACTIONS": ATTRACTIONS_SYSTEM_PROMPT,
            "WEATHER": WEATHER_SYSTEM_PROMPT,
            "GENERAL": FALLBACK_SYSTEM_PROMPT
        }
    
    def _get_complex_reasoning_prompt(self, user_message: str):
        """Get the unified complex reasoning prompt with appropriate formatting based on debug mode"""
        import os
        is_debug_mode = os.getenv("SHOW_CHAIN_OF_THOUGHT", "false").lower() == "true"
        
        # Select the appropriate formatting instructions
        output_instructions = DEBUG_MODE_INSTRUCTIONS if is_debug_mode else NORMAL_MODE_INSTRUCTIONS
        
        # Format the unified prompt with the selected instructions
        final_prompt = COMPLEX_REASONING_PROMPT.format(
            user_message=user_message,
            output_format_instructions=output_instructions
        )
        
        return final_prompt
    
    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})
        
        # Keep only the last N messages to manage context length
        if len(self.conversation_history) > MAX_CONVERSATION_HISTORY * 2:  # *2 for user+assistant pairs
            self.conversation_history = self.conversation_history[-MAX_CONVERSATION_HISTORY * 2:]
    
    def get_response(self, user_message: str) -> str:
        """
        Get a response from the assistant with question classification and weather integration
        
        Args:
            user_message: The user's input message
            
        Returns:
            Assistant's response
        """
        logger.info(f"User Input: '{user_message}'")
        
        # Step 1: Unified analysis (classification, weather decision, location extraction)
        logger.info("Step 1: Analyzing question...")
        analysis = self.router.analyze_question(user_message, self.conversation_history)
        logger.info(f"Category: {analysis['category']}, Weather: {analysis['needs_weather']} ({analysis['mode']}), Location: {analysis.get('city', analysis.get('country', 'unknown'))}, Clarification: {analysis['needs_clarification']}")
        
        # Check for rate limit error in analysis
        if analysis.get('reason') == 'Rate limit error - using fallback analysis':
            logger.error("Rate limit error detected, using fallback analysis")
            # Continue with the fallback analysis instead of returning error
        
        # Step 2: Handle clarification requests for open-ended questions (except COMPLEX_REASONING)
        if analysis['needs_clarification'] and analysis['category'] != 'COMPLEX_REASONING':
            logger.info(f"Step 2: Handling clarification request for open-ended {analysis['category']} question")
            if analysis['category'] == 'COMPLEX_REASONING':
                system_prompt = self._get_complex_reasoning_prompt(user_message)
            else:
                system_prompt = self.prompt_map.get(analysis['category'], FALLBACK_SYSTEM_PROMPT)
            self.add_to_history("user", user_message)
            response = self.llm_service.run(system_prompt, user_message, self.conversation_history, MAX_TOKENS_GENERATION)
            self.add_to_history("assistant", response)
            logger.info("Clarification response generated successfully!")
            return response
        
        # Step 3: Get weather data if needed
        enhanced_message = user_message
        weather_context = ""
        tripadvisor_context = ""  # TripAdvisor disabled - weather API provides external data
        
        if analysis['needs_weather'] and analysis['mode'] in ['current', 'forecast', 'climate']:
            # Determine location for weather API
            location = analysis.get('city') or analysis.get('country')
            
            if location:
                logger.info(f"Step 3: Fetching {analysis['mode']} weather for {location}")
                weather_data = self.weather_service.get_weather(location, analysis['mode'], analysis.get('when'))
                
                if 'error' not in weather_data:
                    if analysis['mode'] == 'current':
                        logger.info(f"Current Weather: {weather_data['temperature']}°C, {weather_data['description']}")
                        weather_context = f"Current weather in {location}: {weather_data['temperature']}°C, {weather_data['description']}, humidity {weather_data['humidity']}%"
                    elif analysis['mode'] == 'forecast':
                        if 'min_temp' in weather_data and 'max_temp' in weather_data:
                            logger.info(f"Forecast Weather: {weather_data['temperature']}°C, {weather_data['description']}")
                            weather_context = f"Tomorrow's forecast for {location}: {weather_data['min_temp']}°C to {weather_data['max_temp']}°C, {weather_data['description']}, humidity {weather_data['humidity']}%"
                        else:
                            logger.info(f"Forecast Weather: {weather_data['temperature']}°C, {weather_data['description']}")
                            weather_context = f"Forecast for {location}: {weather_data['temperature']}°C, {weather_data['description']}"
                    else:  # climate
                        logger.info(f"Climate Info: {weather_data.get('message', 'Seasonal information available')}")
                        weather_context = f"Climate in {location}: {weather_data.get('message', 'Check local weather services for seasonal conditions')}"
                else:
                    logger.warning(f"Weather Error: {weather_data.get('message', 'Unknown error')}")
                    weather_context = f"Weather information unavailable: {weather_data.get('message', 'Service temporarily unavailable')}"
            else:
                logger.warning("No location found for weather data")
        
        
        # Step 4: Get appropriate system prompt
        if analysis['category'] == 'COMPLEX_REASONING':
            system_prompt = self._get_complex_reasoning_prompt(user_message)
            import os
            debug_mode = os.getenv("SHOW_CHAIN_OF_THOUGHT", "false").lower() == "true"
            logger.info(f"Using {analysis['category']} system prompt (debug mode: {debug_mode})")
        else:
            system_prompt = self.prompt_map.get(analysis['category'], FALLBACK_SYSTEM_PROMPT)
            logger.info(f"Using {analysis['category']} system prompt")
        
        # Step 5: Add user message to history
        self.add_to_history("user", user_message)
        
        # Step 6: Prepare enhanced message with facts
        facts = []
        if weather_context:
            facts.append(f"Weather: {weather_context}")
        
        if facts:
            enhanced_message = f"Task: {user_message}\n\nFacts:\n- " + "\n- ".join(facts)
        else:
            enhanced_message = f"Task: {user_message}"
        
        # Step 7: Get response from LLM with specialized prompt
        logger.info("Generating response...")
        
        # Use debug token limit if debug mode is enabled and this is a COMPLEX_REASONING question
        max_tokens = MAX_TOKENS_DEBUG if (SHOW_CHAIN_OF_THOUGHT and analysis['category'] == 'COMPLEX_REASONING') else MAX_TOKENS_GENERATION
        
        if SHOW_CHAIN_OF_THOUGHT and analysis['category'] == 'COMPLEX_REASONING':
            logger.info(f"Using debug token limit: {max_tokens} tokens for chain of thought display")
        
        # For COMPLEX_REASONING, the user_message is already embedded in the system prompt
        if analysis['category'] == 'COMPLEX_REASONING':
            response = self.llm_service.run(system_prompt, "", self.conversation_history, max_tokens)
        else:
            response = self.llm_service.run(system_prompt, enhanced_message, self.conversation_history, max_tokens)
        
        # Check for rate limit error in final response
        if response.startswith("Sorry, I've reached the API rate limit") or response.startswith("Sorry, I encountered an error"):
            logger.error(f"Rate limit error in final response: {response}")
            response = "I'm experiencing high demand right now. Please try again in a few minutes, or feel free to ask a more specific question about your travel plans."
        
        # Step 9: Add assistant response to history
        self.add_to_history("assistant", response)
        
        logger.info("Response generated successfully!")
        
        return response
    
    def get_conversation_history(self) -> list:
        """Get the current conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    

