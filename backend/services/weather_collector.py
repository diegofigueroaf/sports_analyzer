"""
Weather Data Collector
Collects weather data for outdoor NFL games
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from .base_collector import BaseDataCollector
from config.data_sources import WEATHER_CONFIG, NFL_STADIUMS
from config.api_keys import api_keys

logger = logging.getLogger(__name__)

class WeatherCollector(BaseDataCollector):
    """Weather API data collector"""
    
    def __init__(self):
        super().__init__(
            name="Weather",
            base_url=WEATHER_CONFIG['base_url'],
            rate_limit=WEATHER_CONFIG['rate_limit']['requests_per_minute']
        )
        self.api_key = api_keys.WEATHER_API_KEY
        self.stadiums = NFL_STADIUMS
    
    def collect_data(self, data_type: str = 'current', **kwargs) -> Dict:
        """Collect weather data"""
        if self.api_key == 'YOUR_API_KEY_HERE':
            logger.warning("Weather API key not configured")
            return {'error': 'API key not configured'}
        
        logger.info(f"Collecting {data_type} weather data")
        
        if data_type == 'current':
            city = kwargs.get('city')
            return self._collect_current_weather(city)
        elif data_type == 'game_weather':
            team_id = kwargs.get('team_id')
            game_date = kwargs.get('game_date')
            return self._collect_game_weather(team_id, game_date)
        elif data_type == 'forecast':
            city = kwargs.get('city')
            return self._collect_forecast(city)
        else:
            logger.error(f"Unknown data type: {data_type}")
            return {}
    
    def _collect_current_weather(self, city: str) -> Dict:
        """Collect current weather for a city"""
        if not city:
            return {}
        
        endpoint = WEATHER_CONFIG['endpoints']['current']
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'imperial'
        }
        
        raw_data = self.make_request(endpoint, params)
        if not raw_data:
            return {}
        
        # Save raw data
        self.save_raw_data(raw_data, f"weather_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # Process weather data
        weather_data = self._process_weather_data(raw_data)
        
        return {
            'source': 'weather',
            'data_type': 'current',
            'city': city,
            'collected_at': datetime.now().isoformat(),
            'weather': weather_data
        }
    
    def _collect_game_weather(self, team_id: str, game_date: str = None) -> Dict:
        """Collect weather for a specific team's game"""
        if not team_id or team_id not in self.stadiums:
            return {}
        
        stadium_info = self.stadiums[team_id]
        
        # Skip if it's a dome
        if stadium_info.get('dome', True):
            return {
                'source': 'weather',
                'data_type': 'game_weather',
                'team_id': team_id,
                'weather': {'conditions': 'dome', 'impact': 'none'}
            }
        
        city = f"{stadium_info['city']},{stadium_info['state']}"
        return self._collect_current_weather(city)
    
    def _collect_forecast(self, city: str) -> Dict:
        """Collect weather forecast for a city"""
        if not city:
            return {}
        
        endpoint = WEATHER_CONFIG['endpoints']['forecast']
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'imperial'
        }
        
        raw_data = self.make_request(endpoint, params)
        if not raw_data:
            return {}
        
        # Save raw data
        self.save_raw_data(raw_data, f"forecast_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        forecast_data = self._process_forecast_data(raw_data)
        
        return {
            'source': 'weather',
            'data_type': 'forecast',
            'city': city,
            'collected_at': datetime.now().isoformat(),
            'forecast': forecast_data
        }
    
    def _process_weather_data(self, raw_data: Dict) -> Dict:
        """Process raw weather data into standardized format"""
        try:
            main = raw_data['main']
            weather = raw_data['weather'][0]
            wind = raw_data.get('wind', {})
            
            processed = {
                'temperature': round(main['temp'], 1),
                'feels_like': round(main['feels_like'], 1),
                'humidity': main['humidity'],
                'pressure': main['pressure'],
                'conditions': weather['main'],
                'description': weather['description'],
                'wind_speed': wind.get('speed', 0),
                'wind_direction': wind.get('deg', 0),
                'visibility': raw_data.get('visibility', 10000) / 1000,  # Convert to km
                'game_impact': self._calculate_game_impact(main['temp'], wind.get('speed', 0), weather['main'])
            }
            
            return processed
            
        except KeyError as e:
            logger.error(f"Error processing weather data: {e}")
            return {}
    
    def _process_forecast_data(self, raw_data: Dict) -> List[Dict]:
        """Process forecast data"""
        forecasts = []
        
        try:
            for item in raw_data['list'][:8]:  # Next 24 hours (3-hour intervals)
                forecast = {
                    'datetime': item['dt_txt'],
                    'temperature': round(item['main']['temp'], 1),
                    'conditions': item['weather'][0]['main'],
                    'wind_speed': item.get('wind', {}).get('speed', 0),
                    'precipitation_probability': item.get('pop', 0) * 100
                }
                forecasts.append(forecast)
        
        except KeyError as e:
            logger.error(f"Error processing forecast data: {e}")
        
        return forecasts
    
    def _calculate_game_impact(self, temp: float, wind_speed: float, conditions: str) -> Dict:
        """Calculate weather impact on game scoring"""
        impact = {
            'total_score_impact': 0,  # Points adjustment for over/under
            'passing_impact': 0,     # Impact on passing game
            'kicking_impact': 0,     # Impact on field goals
            'overall_rating': 'neutral'
        }
        
        # Temperature impact
        if temp < 32:  # Freezing
            impact['total_score_impact'] -= 3
            impact['passing_impact'] -= 2
            impact['kicking_impact'] -= 2
        elif temp > 90:  # Very hot
            impact['total_score_impact'] -= 1
            impact['passing_impact'] -= 1
        
        # Wind impact
        if wind_speed > 20:  # Strong wind
            impact['total_score_impact'] -= 4
            impact['passing_impact'] -= 3
            impact['kicking_impact'] -= 4
        elif wind_speed > 15:  # Moderate wind
            impact['total_score_impact'] -= 2
            impact['passing_impact'] -= 1
            impact['kicking_impact'] -= 2
        
        # Precipitation impact
        if conditions in ['Rain', 'Snow', 'Thunderstorm']:
            impact['total_score_impact'] -= 3
            impact['passing_impact'] -= 2
            impact['kicking_impact'] -= 1
        
        # Overall rating
        total_impact = abs(impact['total_score_impact'])
        if total_impact >= 5:
            impact['overall_rating'] = 'severe'
        elif total_impact >= 3:
            impact['overall_rating'] = 'moderate'
        elif total_impact >= 1:
            impact['overall_rating'] = 'mild'
        
        return impact
    
    def validate_data(self, data: Dict) -> bool:
        """Validate collected weather data"""
        if not data or 'error' in data:
            return False
        
        required_fields = ['source', 'data_type', 'collected_at']
        
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False
        
        if data['source'] != 'weather':
            logger.error(f"Invalid source: {data['source']}")
            return False
        
        return True