"""
ESPN Data Collector
Collects NFL data from ESPN's public API
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from .base_collector import BaseDataCollector
from config.data_sources import ESPN_CONFIG, NFL_TEAMS, NFL_STADIUMS

logger = logging.getLogger(__name__)

class ESPNCollector(BaseDataCollector):
    """ESPN API data collector"""
    
    def __init__(self):
        super().__init__(
            name="ESPN",
            base_url=ESPN_CONFIG['base_url'],
            rate_limit=ESPN_CONFIG['rate_limit']['requests_per_minute']
        )
        self.teams = NFL_TEAMS
        self.stadiums = NFL_STADIUMS
    
    def collect_data(self, data_type: str = 'games', **kwargs) -> Dict:
        """Collect different types of ESPN data"""
        logger.info(f"Collecting {data_type} data from ESPN")
        
        if data_type == 'games':
            return self._collect_games()
        elif data_type == 'teams':
            return self._collect_teams()
        elif data_type == 'team_stats':
            team_id = kwargs.get('team_id')
            return self._collect_team_stats(team_id)
        elif data_type == 'standings':
            return self._collect_standings()
        else:
            logger.error(f"Unknown data type: {data_type}")
            return {}
    
    def _collect_games(self, date: str = None) -> Dict:
        """Collect current week's games"""
        endpoint = ESPN_CONFIG['endpoints']['scoreboard']
        
        if date:
            endpoint = ESPN_CONFIG['endpoints']['games'].format(date=date)
        
        raw_data = self.make_request(endpoint)
        if not raw_data:
            return {}
        
        # Save raw data for debugging
        self.save_raw_data(raw_data, f"espn_games_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # Process and clean the data
        games_data = self._process_games_data(raw_data)
        
        return {
            'source': 'espn',
            'data_type': 'games',
            'collected_at': datetime.now().isoformat(),
            'games': games_data
        }
    
    def _process_games_data(self, raw_data: Dict) -> List[Dict]:
        """Process raw ESPN games data into standardized format"""
        games = []
        
        for event in raw_data.get('events', []):
            try:
                competition = event['competitions'][0]
                competitors = competition['competitors']
                
                # Ensure we have exactly 2 teams
                if len(competitors) != 2:
                    continue
                
                # Identify home and away teams
                home_team = None
                away_team = None
                
                for competitor in competitors:
                    if competitor['homeAway'] == 'home':
                        home_team = competitor
                    else:
                        away_team = competitor
                
                if not home_team or not away_team:
                    continue
                
                # Extract game information
                game = {
                    'espn_id': event['id'],
                    'date': event['date'],
                    'status': event['status']['type']['name'],
                    'week': competition.get('week', {}).get('number'),
                    'season_type': competition.get('season', {}).get('type'),
                    'home_team': {
                        'id': home_team['team']['id'],
                        'name': home_team['team']['displayName'],
                        'abbreviation': home_team['team']['abbreviation'],
                        'score': home_team.get('score', 0),
                        'record': self._extract_record(home_team)
                    },
                    'away_team': {
                        'id': away_team['team']['id'],
                        'name': away_team['team']['displayName'],
                        'abbreviation': away_team['team']['abbreviation'],
                        'score': away_team.get('score', 0),
                        'record': self._extract_record(away_team)
                    },
                    'venue': self._extract_venue_info(competition),
                    'odds': self._extract_odds(competition),
                    'weather_needed': self._needs_weather_data(home_team['team']['id'])
                }
                
                games.append(game)
                
            except KeyError as e:
                logger.warning(f"Missing data in game event: {e}")
                continue
        
        logger.info(f"Processed {len(games)} games")
        return games
    
    def _extract_record(self, team_data: Dict) -> Dict:
        """Extract team record information"""
        try:
            records = team_data.get('records', [])
            for record in records:
                if record.get('type') == 'total':
                    return {
                        'wins': int(record.get('wins', 0)),
                        'losses': int(record.get('losses', 0)),
                        'ties': int(record.get('ties', 0))
                    }
        except (KeyError, ValueError, TypeError):
            pass
        
        return {'wins': 0, 'losses': 0, 'ties': 0}
    
    def _extract_venue_info(self, competition: Dict) -> Dict:
        """Extract venue information"""
        try:
            venue = competition.get('venue', {})
            return {
                'name': venue.get('fullName', 'Unknown'),
                'city': venue.get('address', {}).get('city', 'Unknown'),
                'state': venue.get('address', {}).get('state', 'Unknown'),
                'indoor': venue.get('indoor', False)
            }
        except (KeyError, TypeError):
            return {'name': 'Unknown', 'city': 'Unknown', 'state': 'Unknown', 'indoor': False}
    
    def _extract_odds(self, competition: Dict) -> Optional[Dict]:
        """Extract betting odds if available"""
        try:
            odds = competition.get('odds', [])
            if odds:
                return {
                    'spread': odds[0].get('spread'),
                    'over_under': odds[0].get('overUnder'),
                    'home_team_odds': odds[0].get('homeTeamOdds'),
                    'away_team_odds': odds[0].get('awayTeamOdds')
                }
        except (KeyError, IndexError):
            pass
        
        return None
    
    def _needs_weather_data(self, team_id: str) -> bool:
        """Check if game needs weather data (outdoor stadium)"""
        return not self.stadiums.get(team_id, {}).get('dome', True)
    
    def _collect_teams(self) -> Dict:
        """Collect all NFL teams data"""
        endpoint = ESPN_CONFIG['endpoints']['teams']
        raw_data = self.make_request(endpoint)
        
        if not raw_data:
            return {}
        
        # Save raw data
        self.save_raw_data(raw_data, f"espn_teams_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        teams_data = self._process_teams_data(raw_data)
        
        return {
            'source': 'espn',
            'data_type': 'teams',
            'collected_at': datetime.now().isoformat(),
            'teams': teams_data
        }
    
    def _process_teams_data(self, raw_data: Dict) -> List[Dict]:
        """Process raw teams data"""
        teams = []
        
        try:
            for team in raw_data['sports'][0]['leagues'][0]['teams']:
                team_info = team['team']
                teams.append({
                    'id': team_info['id'],
                    'name': team_info['displayName'],
                    'abbreviation': team_info['abbreviation'],
                    'color': team_info.get('color', '#000000'),
                    'logo': team_info.get('logos', [{}])[0].get('href', ''),
                    'location': team_info.get('location', 'Unknown')
                })
        except KeyError as e:
            logger.error(f"Error processing teams data: {e}")
        
        return teams
    
    def _collect_team_stats(self, team_id: str) -> Dict:
        """Collect detailed stats for a specific team"""
        if not team_id:
            return {}
        
        endpoint = ESPN_CONFIG['endpoints']['team_detail'].format(team_id=team_id)
        raw_data = self.make_request(endpoint)
        
        if not raw_data:
            return {}
        
        # Save raw data
        self.save_raw_data(raw_data, f"espn_team_{team_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        return {
            'source': 'espn',
            'data_type': 'team_stats',
            'team_id': team_id,
            'collected_at': datetime.now().isoformat(),
            'data': raw_data
        }
    
    def validate_data(self, data: Dict) -> bool:
        """Validate collected ESPN data"""
        if not data:
            return False
        
        required_fields = ['source', 'data_type', 'collected_at']
        
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False
        
        if data['source'] != 'espn':
            logger.error(f"Invalid source: {data['source']}")
            return False
        
        return True