"""
Add sample historical game data for testing
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.models.database import SportsDatabase
import random
from datetime import datetime, timedelta

def add_sample_historical_games():
    """Add some sample completed games for testing"""
    db = SportsDatabase()
    
    # Sample completed games with realistic scores
    sample_games = [
        {
            'espn_id': 'hist_001',
            'game_date': (datetime.now() - timedelta(days=7)).isoformat(),
            'home_team_id': '2',
            'home_team_name': 'Buffalo Bills',
            'away_team_id': '15',
            'away_team_name': 'Miami Dolphins',
            'status': 'STATUS_FINAL',
            'home_score': 24,
            'away_score': 17,
            'weather_data': '{"conditions": "clear"}',
            'raw_data': '{}'
        },
        {
            'espn_id': 'hist_002',
            'game_date': (datetime.now() - timedelta(days=6)).isoformat(),
            'home_team_id': '12',
            'home_team_name': 'Kansas City Chiefs',
            'away_team_id': '7',
            'away_team_name': 'Denver Broncos',
            'status': 'STATUS_FINAL',
            'home_score': 31,
            'away_score': 14,
            'weather_data': '{"conditions": "clear"}',
            'raw_data': '{}'
        },
        {
            'espn_id': 'hist_003',
            'game_date': (datetime.now() - timedelta(days=5)).isoformat(),
            'home_team_id': '25',
            'home_team_name': 'San Francisco 49ers',
            'away_team_id': '26',
            'away_team_name': 'Seattle Seahawks',
            'status': 'STATUS_FINAL',
            'home_score': 21,
            'away_score': 28,
            'weather_data': '{"conditions": "rain"}',
            'raw_data': '{}'
        }
    ]
    
    # Fix: Use sqlite3 directly instead of db.database
    import sqlite3
    
    with sqlite3.connect(db.db_path) as conn:
        for game in sample_games:
            conn.execute('''
                INSERT OR REPLACE INTO games (
                    espn_id, game_date, home_team_id, home_team_name,
                    away_team_id, away_team_name, status, home_score,
                    away_score, weather_data, raw_data, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game['espn_id'], game['game_date'], game['home_team_id'], 
                game['home_team_name'], game['away_team_id'], game['away_team_name'],
                game['status'], game['home_score'], game['away_score'],
                game['weather_data'], game['raw_data'],
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
        conn.commit()
    
    print(f"Added {len(sample_games)} historical games for testing")