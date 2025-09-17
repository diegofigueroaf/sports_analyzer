"""
API Keys Configuration
Store all API keys and sensitive configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIKeys:
    """Centralized API key management"""
    
    def __init__(self):
        # Weather API (OpenWeatherMap)
        self.WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'YOUR_API_KEY_HERE')
        
        # The Odds API (Future)
        self.ODDS_API_KEY = os.getenv('ODDS_API_KEY', 'YOUR_API_KEY_HERE')
        
        # News API (Future)
        self.NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'YOUR_API_KEY_HERE')
        
        # SportRadar API (Future - Professional)
        self.SPORTRADAR_API_KEY = os.getenv('SPORTRADAR_API_KEY', 'YOUR_API_KEY_HERE')
    
    def validate_keys(self):
        """Check which API keys are configured"""
        keys_status = {
            'weather': self.WEATHER_API_KEY != 'YOUR_API_KEY_HERE',
            'odds': self.ODDS_API_KEY != 'YOUR_API_KEY_HERE',
            'news': self.NEWS_API_KEY != 'YOUR_API_KEY_HERE',
            'sportradar': self.SPORTRADAR_API_KEY != 'YOUR_API_KEY_HERE'
        }
        return keys_status
    
    def get_available_sources(self):
        """Return list of available data sources based on configured keys"""
        available = []
        status = self.validate_keys()
        
        if status['weather']:
            available.append('weather')
        if status['odds']:
            available.append('odds')
        if status['news']:
            available.append('news')
        if status['sportradar']:
            available.append('sportradar')
            
        # Always available (free APIs)
        available.extend(['espn', 'scraping'])
        
        return available

# Global instance
api_keys = APIKeys()