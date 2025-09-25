# data_manager.py
import json
import os
from typing import List, Dict, Any
from datetime import datetime

class DataManager:
    def __init__(self, favorites_file: str):
        self.favorites_file = favorites_file
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        os.makedirs(os.path.dirname(self.favorites_file), exist_ok=True)
    
    def load_favorites(self) -> List[str]:
        """Load favorite cities from file."""
        try:
            if os.path.exists(self.favorites_file):
                with open(self.favorites_file, 'r') as file:
                    data = json.load(file)
                    return data.get('favorites', [])
            return []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading favorites: {e}")
            return []
    
    def save_favorites(self, favorites: List[str]):
        """Save favorite cities to file."""
        try:
            data = {
                'favorites': favorites,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.favorites_file, 'w') as file:
                json.dump(data, file, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save favorites: {str(e)}")
    
    def add_favorite(self, city: str) -> bool:
        """Add a city to favorites."""
        favorites = self.load_favorites()
        if city not in favorites:
            favorites.append(city)
            self.save_favorites(favorites)
            return True
        return False
    
    def remove_favorite(self, city: str) -> bool:
        """Remove a city from favorites."""
        favorites = self.load_favorites()
        if city in favorites:
            favorites.remove(city)
            self.save_favorites(favorites)
            return True
        return False