"""
Data Manager
Coordinates data collection from multiple sources
"""
from datetime import datetime
from typing import Dict, List, Optional
import logging
from .espn_collector import ESPNCollector
from .weather_collector import WeatherCollector
from config.api_keys import api_keys

logger = logging.getLogger(__name__)

class DataManager:
    """Manages data collection from all sources"""
    
    def __init__(self):
        # Initialize collectors
        self.espn = ESPNCollector()
        self.weather = WeatherCollector()
        
        # Track available sources
        self.available_sources = api_keys.get_available_sources()
        logger.info(f"Available data sources: {self.available_sources}")
    
    def collect_game_data(self, include_weather: bool = True) -> Dict:
        """Collect comprehensive game data"""
        logger.info("Starting comprehensive game data collection")
        
        result = {
            'collection_time': datetime.now().isoformat(),
            'games': [],
            'errors': []
        }
        
        # Get games from ESPN
        games_data = self.espn.collect_data('games')
        
        if not games_data or not games_data.get('games'):
            result['errors'].append("Failed to collect games data from ESPN")
            return result
        
        # Enrich games with weather data
        for game in games_data['games']:
            enriched_game = game.copy()
            
            # Add weather data if available and needed
            if (include_weather and 
                'weather' in self.available_sources and 
                game.get('weather_needed', False)):
                
                weather_data = self.weather.collect_data(
                    'game_weather',
                    team_id=game['home_team']['id']
                )
                
                if weather_data and 'weather' in weather_data:
                    enriched_game['weather'] = weather_data['weather']
                    logger.info(f"Added weather data for {game['home_team']['name']} game")
                else:
                    enriched_game['weather'] = {'status': 'unavailable'}
            else:
                enriched_game['weather'] = {'status': 'not_needed'}
            
            result['games'].append(enriched_game)
        
        logger.info(f"Collected data for {len(result['games'])} games")
        return result
    
    def collect_team_data(self) -> Dict:
        """Collect team information"""
        logger.info("Collecting team data")
        
        teams_data = self.espn.collect_data('teams')
        
        return {
            'collection_time': datetime.now().isoformat(),
            'teams': teams_data.get('teams', []),
            'source': 'espn'
        }
    
    def get_prediction_data(self, team_id: str = None) -> Dict:
        """Get all data needed for predictions"""
        logger.info(f"Collecting prediction data for team {team_id or 'all teams'}")
        
        # Collect games
        games_result = self.collect_game_data(include_weather=True)
        
        # Collect team data
        teams_result = self.collect_team_data()
        
        # Filter for specific team if requested
        if team_id:
            filtered_games = [
                game for game in games_result['games']
                if (game['home_team']['id'] == team_id or 
                    game['away_team']['id'] == team_id)
            ]
            games_result['games'] = filtered_games
        
        return {
            'collection_time': datetime.now().isoformat(),
            'games': games_result['games'],
            'teams': teams_result['teams'],
            'available_sources': self.available_sources,
            'errors': games_result.get('errors', [])
        }
    
    def get_collector_status(self) -> Dict:
        """Get status of all collectors"""
        return {
            'espn': self.espn.get_status(),
            'weather': self.weather.get_status(),
            'available_sources': self.available_sources,
            'api_keys_configured': api_keys.validate_keys()
        }
    
    def test_all_collectors(self) -> Dict:
        """Test all collectors"""
        logger.info("Testing all data collectors")
        
        results = {
            'espn': {'status': 'unknown', 'error': None},
            'weather': {'status': 'unknown', 'error': None}
        }
        
        # Test ESPN
        try:
            espn_data = self.espn.collect_data('teams')
            if self.espn.validate_data(espn_data):
                results['espn']['status'] = 'working'
            else:
                results['espn']['status'] = 'failed'
                results['espn']['error'] = 'Data validation failed'
        except Exception as e:
            results['espn']['status'] = 'error'
            results['espn']['error'] = str(e)
        
        # Test Weather (only if API key is configured)
        if 'weather' in self.available_sources:
            try:
                weather_data = self.weather.collect_data('current', city='Miami')
                if self.weather.validate_data(weather_data):
                    results['weather']['status'] = 'working'
                else:
                    results['weather']['status'] = 'failed'
                    results['weather']['error'] = 'Data validation failed'
            except Exception as e:
                results['weather']['status'] = 'error'
                results['weather']['error'] = str(e)
        else:
            results['weather']['status'] = 'not_configured'
            results['weather']['error'] = 'API key not provided'
        
        return results