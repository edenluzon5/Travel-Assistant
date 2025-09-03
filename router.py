# router.py - Decision/classification/extraction logic using LLMService
import json
import logging
from apis import LLMService
from prompts import UNIFIED_ANALYSIS_PROMPT

# Set up logging
logger = logging.getLogger(__name__)

class Router:
    def __init__(self):
        """Initialize the router with LLM service"""
        self.llm_service = LLMService()
    
    def analyze_question(self, user_message: str, conversation_history: list = None) -> dict:
        """
        Unified analysis: classification, weather decision, and location extraction in one call
        
        Args:
            user_message: User's input message
            conversation_history: Optional conversation history for context
            
        Returns:
            Dictionary with all analysis results
        """
        try:
            # Prepare unified analysis prompt with conversation context
            if conversation_history:
                # Include recent conversation context for better analysis
                context_messages = conversation_history[-4:]  # Last 4 messages (2 exchanges)
                context_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context_messages])
                logger.info(f"Using conversation context: {context_text}")
                analysis_prompt = UNIFIED_ANALYSIS_PROMPT.format(user_message=user_message, context=context_text)
            else:
                logger.info("No conversation history available")
                analysis_prompt = UNIFIED_ANALYSIS_PROMPT.format(user_message=user_message, context="")
            
            # Get analysis from LLM
            result = self.llm_service.run_json(
                system="You are a travel assistant analyzing questions for classification, weather needs, and location extraction. Consider conversation context when available.",
                user=analysis_prompt
            )
            
            logger.info(f"Unified Analysis JSON Response: {result}")
            
            # Check for rate limit error
            if "error" in result and result["error"] == "rate_limit":
                logger.error(f"Rate limit error in analysis: {result.get('message', 'Unknown error')}")
                # Temporarily return a default analysis instead of rate limit error
                return {
                    "category": "GENERAL",
                    "needs_weather": False,
                    "mode": "none",
                    "city": "",
                    "country": "",
                    "when": "",
                    "needs_clarification": True,  # Default to clarification for safety
                    "confidence": 0.0,
                    "reason": "Rate limit error - using fallback analysis"
                }
            
            # Normalize the result with defaults
            normalized_result = {
                "category": result.get("category", "GENERAL"),
                "needs_weather": result.get("needs_weather", False),
                "mode": result.get("mode", "none"),
                "city": result.get("city", ""),
                "country": result.get("country", ""),
                "when": result.get("when", ""),
                "needs_clarification": result.get("needs_clarification", False),
                "confidence": float(result.get("confidence", 0.0)),
                "reason": result.get("reason", "No reason provided")
            }
            
            # Validate category
            valid_categories = ["DESTINATION", "COMPLEX_REASONING", "PACKING", "ATTRACTIONS", "WEATHER", "GENERAL"]
            if normalized_result["category"] not in valid_categories:
                logger.warning(f"Invalid category: {normalized_result['category']}, defaulting to GENERAL")
                normalized_result["category"] = "GENERAL"
            
            # Validate weather mode
            valid_modes = ["current", "forecast", "climate", "none"]
            if normalized_result["mode"] not in valid_modes:
                logger.warning(f"Invalid weather mode: {normalized_result['mode']}, defaulting to none")
                normalized_result["mode"] = "none"
            
            logger.info(f"Analysis: {normalized_result['category']}, weather: {normalized_result['needs_weather']} ({normalized_result['mode']}), location: {normalized_result.get('city', normalized_result.get('country', 'unknown'))}, clarification: {normalized_result['needs_clarification']}")
            
            return normalized_result
            
        except Exception as e:
            logger.error(f"Unified Analysis Error: {e}")
            return {
                "category": "GENERAL",
                "needs_weather": False,
                "mode": "none",
                "city": "",
                "country": "",
                "when": "",
                "needs_clarification": False,
                "confidence": 0.0,
                "reason": "Analysis error"
            }