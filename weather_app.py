from weather_api import WeatherAPI
from data_manager import DataManager
from config import Config

class WeatherApp:
    def __init__(self):
        self.weather_api = WeatherAPI()
        self.data_manager = DataManager(Config.FAVORITES_FILE)
        self.current_city = None
        self.current_weather = None
        self.forecast_data = None
    
    def search_city(self, city: str):
        try:
            self.current_weather = self.weather_api.get_current_weather(city)
            self.forecast_data = self.weather_api.get_forecast(city)
            self.current_city = city
            return True
        except Exception as e:
            raise Exception(f"Failed to get weather for {city}: {str(e)}")
    
    def add_to_favorites(self, city: str = None):
        city = city or self.current_city
        if city:
            return self.data_manager.add_favorite(city)
        return False
    
    def get_favorites(self):
        return self.data_manager.load_favorites()
    
    def format_current_weather(self) -> str:
        if not self.current_weather:
            return "No weather data available"
        
        data = self.current_weather
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].title()
        
        return f"""
Current Weather in {data['name']}:
Temperature: {temp}°C (feels like {feels_like}°C)
Conditions: {description}
Humidity: {humidity}%
"""

if __name__ == "__main__":
    app = WeatherApp()
    try:
        app.search_city("London")
        print(app.format_current_weather())
    except Exception as e:
        print(f"Error: {e}")