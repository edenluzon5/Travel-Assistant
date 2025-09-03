# apis.py - External API integrations (Groq, Weather, Country info)
import json
import requests
import time
import logging

from langchain_groq import ChatGroq
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import GROQ_API_KEY, MODEL_NAME, MAX_CONVERSATION_HISTORY, TEMPERATURE, MAX_TOKENS_TOOL, MAX_TOKENS_GENERATION, WEATHER_API_KEY, API_DELAY_SECONDS

# Set up logging
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        """Initialize the Groq LLM service"""
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS_TOOL  # Default to tool tokens
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException, Exception))
    )
    def run(self, system: str, user: str, history: list = None, max_tokens: int = None) -> str:
        """
        Generic method to run LLM with system and user messages
        
        Args:
            system: System prompt
            user: User message
            history: Optional conversation history
            max_tokens: Override max tokens for this call
            
        Returns:
            LLM response as string
        """
        try:
            # Use provided max_tokens or default
            tokens_to_use = max_tokens if max_tokens else MAX_TOKENS_TOOL
            
            # Update the existing LLM instance with new token limit
            self.llm.max_tokens = tokens_to_use
            
            # Prepare messages for the LLM
            messages = []
            
            # Add system prompt
            messages.append({"role": "system", "content": system})
            
            # Add conversation history if available
            if history:
                for msg in history[-MAX_CONVERSATION_HISTORY:]:  # Keep last N messages
                    messages.append(msg)
            
            # Add current user message
            messages.append({"role": "user", "content": user})
            
            # Get response from LLM
            response = self.llm.invoke(messages)
            
            # Add delay to prevent rate limiting
            time.sleep(API_DELAY_SECONDS)
            
            return response.content.strip()
            
        except Exception as e:
            error_msg = str(e)
            # Handle rate limit errors specifically
            if "429" in error_msg or "rate limit" in error_msg.lower():
                return "Sorry, I've reached the API rate limit. Please try again in a few minutes."
            return f"Sorry, I encountered an error: {error_msg}"
    

    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException, Exception))
    )
    def run_json(self, system: str, user: str) -> dict:
        """
        Generic method to run LLM and return parsed JSON response
        
        Args:
            system: System prompt
            user: User message
            
        Returns:
            Parsed JSON response as dictionary
        """
        try:
            # Get response from LLM
            response = self.run(system, user)
            logger.debug(f"Raw LLM Response: '{response}'")
            
            # Check if response is an error message (not JSON)
            if response.startswith("Sorry, I've reached the API rate limit") or response.startswith("Sorry, I encountered an error"):
                logger.error(f"API Error: {response}")
                return {"error": "rate_limit", "message": response}
            
            # Clean the response - remove any extra text before/after JSON
            response = response.strip()
            
            # Try to find JSON in the response
            if response.startswith('{') and response.endswith('}'):
                json_str = response
            else:
                # Look for JSON pattern in the response
                start_idx = response.find('{')
                end_idx = response.rfind('}')
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx+1]
                else:
                    raise json.JSONDecodeError("No valid JSON found", response, 0)
            
            logger.debug(f"Extracted JSON: '{json_str}'")
            
            # Parse JSON response
            result = json.loads(json_str)
            logger.debug(f"Successfully parsed JSON: {result}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON Parse Error: {e}")
            logger.error(f"Raw response: '{response}'")
            # Check if it's a rate limit error
            if "429" in response or "rate limit" in response.lower():
                return {"error": "rate_limit", "message": "API rate limit reached. Please try again in a few minutes."}
            return {"error": "JSON parse error", "raw_response": response}
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            error_msg = str(e)
            if "429" in error_msg or "rate limit" in error_msg.lower():
                return {"error": "rate_limit", "message": "API rate limit reached. Please try again in a few minutes."}
            return {"error": "LLM error", "message": error_msg}

class WeatherService:
    def __init__(self):
        """Initialize the weather service"""
        self.api_key = WEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.cache = {}  # Simple cache for weather data
        self.cache_duration = 300  # 5 minutes
    
    def _is_cache_valid(self, cache_time):
        """Check if cache entry is still valid"""
        return time.time() - cache_time < self.cache_duration
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type((requests.exceptions.RequestException, Exception))
    )
    def get_weather(self, city: str, weather_type: str = "current", when: str = None) -> dict:
        """
        Get weather data for a specific city
        
        Args:
            city: City name
            weather_type: "current" for current weather, "climate" for seasonal info
            
        Returns:
            Weather data dictionary
        """
        # Check cache first
        cache_key = f"{city}_{weather_type}"
        if cache_key in self.cache:
            cache_time, cached_data = self.cache[cache_key]
            if self._is_cache_valid(cache_time):
                logger.info(f"Using cached weather data for {city}")
                return cached_data
        
        # Always use weather API - it can handle current, forecast, and historical data
        return self._get_weather_data(city, weather_type, when)
    
    def _get_weather_data(self, city: str, weather_type: str, when: str = None) -> dict:
        """
        Unified weather data method that handles current, forecast, and climate data
        """
        try:
            # First, get coordinates for the city
            geocode_url = "https://api.openweathermap.org/geo/1.0/direct"
            geocode_params = {
                'q': city,
                'limit': 1,
                'appid': self.api_key
            }
            
            geocode_response = requests.get(geocode_url, params=geocode_params, timeout=10)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()
            
            if not geocode_data:
                return {
                    'city': city,
                    'type': weather_type,
                    'message': f"Could not find location data for {city}. Please check local weather services."
                }
            
            lat = geocode_data[0]['lat']
            lon = geocode_data[0]['lon']
            country = geocode_data[0].get('country', 'Unknown')
            
            # Determine what type of weather data to fetch
            if weather_type == "current":
                return self._get_current_weather_data(lat, lon, city, country)
            elif weather_type == "forecast":
                return self._get_forecast_weather_data(lat, lon, city, country, when)
            elif weather_type == "climate":
                return self._get_climate_weather_data(lat, lon, city, country, when)
            else:
                # Default to current weather
                return self._get_current_weather_data(lat, lon, city, country)
                
        except requests.exceptions.Timeout:
            logger.warning(f"Weather API timeout for {city}")
            return {
                'city': city,
                'type': weather_type,
                'message': f"Weather data temporarily unavailable for {city}. Please check local weather services."
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API Error: {e}")
            return {
                'city': city,
                'type': weather_type,
                'message': f"Weather data unavailable for {city}. Please check local weather services."
            }
        except Exception as e:
            logger.error(f"Weather Error: {e}")
            return {
                'city': city,
                'type': weather_type,
                'message': f"Weather data unavailable for {city}. Please check local weather services."
            }
    
    def _get_current_weather_data(self, lat: float, lon: float, city: str, country: str) -> dict:
        """Get current weather data"""
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant weather information
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'type': 'current'
            }
            
            # Cache the result
            self.cache[f"{city}_current"] = (time.time(), weather_info)
            
            return weather_info
            
        except requests.exceptions.Timeout:
            logger.warning(f"Weather API timeout for {city}")
            return {"error": "timeout", "message": "The forecast service seems to be overloaded—we'll try again in a moment or continue without weather data."}
        except requests.exceptions.RequestException as e:
            if "404" in str(e):
                logger.warning(f"City not found: {city}")
                return {"error": "not_found", "message": f"I couldn't find the city '{city}'. Would you like to try an English name or a more precise name?"}
            else:
                logger.error(f"Weather API Error: {e}")
                return {"error": "api_error", "message": "Weather service temporarily unavailable."}
        except Exception as e:
            logger.error(f"Weather Error: {e}")
            return {"error": "unknown", "message": "Weather data unavailable."}
    
    def _get_forecast_weather_data(self, lat: float, lon: float, city: str, country: str, when: str = None) -> dict:
        """Get forecast weather data for specific future days like 'tomorrow'"""
        try:
            # Use OpenWeatherMap forecast API for specific future days
            forecast_params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            forecast_response = requests.get(self.forecast_url, params=forecast_params, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            if 'list' in forecast_data and forecast_data['list']:
                forecasts = forecast_data['list']
                
                # Handle specific time requests like "tomorrow"
                if when:
                    when_lower = when.lower().strip()
                    
                    if when_lower in ['tomorrow', 'next day']:
                        # Get tomorrow's forecast (next 24-48 hours)
                        tomorrow_forecasts = forecasts[8:16]  # Next day (8 * 3-hour intervals = 24 hours)
                        
                        if tomorrow_forecasts:
                            # Calculate average temperature and find most common weather
                            temps = [f['main']['temp'] for f in tomorrow_forecasts]
                            descriptions = [f['weather'][0]['description'] for f in tomorrow_forecasts]
                            humidities = [f['main']['humidity'] for f in tomorrow_forecasts]
                            
                            avg_temp = sum(temps) / len(temps)
                            most_common_desc = max(set(descriptions), key=descriptions.count)
                            avg_humidity = sum(humidities) / len(humidities)
                            
                            # Get min/max temps
                            min_temp = min(temps)
                            max_temp = max(temps)
                            
                            weather_info = {
                                'city': city,
                                'country': country,
                                'type': 'forecast',
                                'temperature': round(avg_temp, 1),
                                'min_temp': round(min_temp, 1),
                                'max_temp': round(max_temp, 1),
                                'description': most_common_desc,
                                'humidity': round(avg_humidity),
                                'when': when,
                                'message': f"Tomorrow's forecast for {city}"
                            }
                            
                            # Cache the result
                            cache_key = f"{city}_forecast_{when}"
                            self.cache[cache_key] = (time.time(), weather_info)
                            
                            return weather_info
                    else:
                        # For other specific days, provide general forecast info
                        avg_temp = sum(f['main']['temp'] for f in forecasts[:8]) / 8
                        descriptions = [f['weather'][0]['description'] for f in forecasts[:8]]
                        most_common_desc = max(set(descriptions), key=descriptions.count)
                        
                        return {
                            'city': city,
                            'country': country,
                            'type': 'forecast',
                            'temperature': round(avg_temp, 1),
                            'description': most_common_desc,
                            'when': when,
                            'message': f"Forecast for {when} in {city}"
                        }
                else:
                    # No specific time mentioned, provide next 24 hours
                    next_24h = forecasts[:8]  # Next 24 hours
                    avg_temp = sum(f['main']['temp'] for f in next_24h) / len(next_24h)
                    descriptions = [f['weather'][0]['description'] for f in next_24h]
                    most_common_desc = max(set(descriptions), key=descriptions.count)
                    
                    return {
                        'city': city,
                        'country': country,
                        'type': 'forecast',
                        'temperature': round(avg_temp, 1),
                        'description': most_common_desc,
                        'message': f"Next 24 hours forecast for {city}"
                    }
            else:
                return {
                    'city': city,
                    'type': 'forecast',
                    'message': f"Forecast data unavailable for {city}. Please check local weather services."
                }
                
        except requests.exceptions.Timeout:
            logger.warning(f"Forecast API timeout for {city}")
            return {"error": "timeout", "message": "The forecast service seems to be overloaded—we'll try again in a moment or continue without weather data."}
        except requests.exceptions.RequestException as e:
            if "404" in str(e):
                logger.warning(f"City not found: {city}")
                return {"error": "not_found", "message": f"I couldn't find the city '{city}'. Would you like to try an English name or a more precise name?"}
            else:
                logger.error(f"Forecast API Error: {e}")
                return {"error": "api_error", "message": "Forecast service temporarily unavailable."}
        except Exception as e:
            logger.error(f"Forecast Error: {e}")
            return {"error": "unknown", "message": "Forecast data unavailable."}
    
    def _get_climate_weather_data(self, lat: float, lon: float, city: str, country: str, when: str = None) -> dict:
        """Get seasonal snapshot information using OpenWeatherMap forecast API"""
        try:
            # Use the provided lat, lon directly (no duplicate geocoding)
            # Use OpenWeatherMap forecast API for seasonal snapshot data
            forecast_params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            forecast_response = requests.get(self.forecast_url, params=forecast_params, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            if 'list' in forecast_data and forecast_data['list']:
                # Analyze forecast data
                forecasts = forecast_data['list']
                
                # If a specific time period is mentioned, provide relevant information
                if when:
                    when_lower = when.lower().strip()
                    
                    # Check for specific months/seasons
                    month_seasons = {
                        'january': 'winter', 'jan': 'winter',
                        'february': 'winter', 'feb': 'winter', 
                        'march': 'spring', 'mar': 'spring',
                        'april': 'spring', 'apr': 'spring',
                        'may': 'spring',
                        'june': 'summer', 'jun': 'summer',
                        'july': 'summer', 'jul': 'summer',
                        'august': 'summer', 'aug': 'summer',
                        'september': 'autumn', 'sep': 'autumn', 'sept': 'autumn',
                        'october': 'autumn', 'oct': 'autumn',
                        'november': 'autumn', 'nov': 'autumn',
                        'december': 'winter', 'dec': 'winter',
                        'winter': 'winter', 'spring': 'spring', 'summer': 'summer', 'autumn': 'autumn', 'fall': 'autumn'
                    }
                    
                    for month_key, season in month_seasons.items():
                        if month_key in when_lower:
                            # Provide general seasonal information
                            season_info = {
                                'winter': 'cold weather, possible snow',
                                'spring': 'mild temperatures, occasional rain',
                                'summer': 'warm to hot weather, generally dry',
                                'autumn': 'cooling temperatures, variable weather'
                            }
                            
                            message = f"{when.title()} in {city} typically has {season_info.get(season, 'variable weather')}; this is a seasonal snapshot based on forecast data."
                            break
                    else:
                        # Default message if no season/month found
                        message = f"Weather information for {when} in {city} is available; this is a seasonal snapshot based on forecast data."
                else:
                    # Default: provide general forecast information
                    avg_temp = sum(f['main']['temp'] for f in forecasts[:8]) / 8  # Average of next 24 hours
                    descriptions = [f['weather'][0]['description'] for f in forecasts[:8]]
                    most_common_desc = max(set(descriptions), key=descriptions.count)
                    message = f"Next few days in {city}: {avg_temp:.1f}°C average, {most_common_desc}; this is a seasonal snapshot based on forecast data."
            else:
                message = f"Weather data for {city} is available; check local sources for specific conditions."
            
            result = {
                'city': city,
                'country': country,
                'type': 'climate',
                'message': message
            }
            
            # Cache the result
            self.cache[f"{city}_climate"] = (time.time(), result)
            
            return result
            
        except requests.exceptions.Timeout:
            logger.warning(f"Forecast API timeout for {city}")
            return {
                'city': city,
                'type': 'climate',
                'message': f"Forecast data temporarily unavailable for {city}. Please check local weather services."
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Forecast API Error: {e}")
            return {
                'city': city,
                'type': 'climate',
                'message': f"Forecast data unavailable for {city}. Please check local weather services."
            }
        except Exception as e:
            logger.error(f"Forecast Error: {e}")
            return {
                'city': city,
                'type': 'climate',
                'message': f"Forecast data unavailable for {city}. Please check local weather services."
            }



