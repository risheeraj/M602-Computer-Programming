import requests
from typing import Dict, Any, List
from config import Config

class WeatherAPI:
    def __init__(self):
        self.config = Config()
    
    def get_current_weather(self, city: str) -> Dict[str, Any]:
        try:
            url = f"{self.config.BASE_URL}/weather"
            params = {
                'q': city,
                'appid': self.config.API_KEY,
                'units': self.config.UNITS
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch weather data: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing weather data: {str(e)}")
    
    def get_forecast(self, city: str, days: int = 5) -> Dict[str, Any]:
        try:
            url = f"{self.config.BASE_URL}/forecast"
            params = {
                'q': city,
                'appid': self.config.API_KEY,
                'units': self.config.UNITS,
                'cnt': days * 8  
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch forecast data: {str(e)}")