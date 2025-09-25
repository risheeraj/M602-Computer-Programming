# config.py
import os

class Config:
    API_KEY = os.getenv('OPENWEATHER_API_KEY', 'df70ff280acd3243b2df48b00a2c178a')
    BASE_URL = 'https://api.openweathermap.org/data/2.5'
    FAVORITES_FILE = 'data/favorites.json'
    UNITS = 'metric'  # metric, imperial, or kelvin