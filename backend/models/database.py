"""
Simple SQLite Database for storing collected data
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging
import os

logger = logging.getLogger(__name__)

class SportsDatabase:
    """Simple SQLite database for sports data"""
    
    def __init__(self, db_path: str = "data/sports_betting.db"):
        self.db_path = db_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.init_database()
        logger.info(f"Database initialized: {db_path}")
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            # Games table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    espn_id TEXT UNIQUE,
                    game_date TEXT,
                    home_team_id TEXT,
                    home_team_name TEXT,
                    away_team_id TEXT,
                    away_team_name TEXT,
                    status TEXT,
                    home_score INTEGER DEFAULT 0,
                    away_score INTEGER DEFAULT 0,
                    weather_data TEXT,
                    raw_data TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            
            # Teams table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY,
                    espn_id TEXT UNIQUE,
                    name TEXT,
                    abbreviation TEXT,
                    city TEXT,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    ties INTEGER DEFAULT 0,
                    last_updated TEXT
                )
            ''')
            
            # Predictions table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id TEXT,
                    predicted_winner TEXT,
                    confidence REAL,
                    prediction_type TEXT,
                    factors TEXT,
                    created_at TEXT,
                    result TEXT,
                    correct INTEGER
                )
            ''')
            
            conn.commit()
    
    def save_games(self, games_data: List[Dict]) -> int:
        """Save games data to database"""
        saved_count = 0
        
        with sqlite3.connect(self.db_path) as conn:
            for game in games_data:
                try:
                    # Insert or update game
                    conn.execute('''
                        INSERT OR REPLACE INTO games (
                            espn_id, game_date, home_team_id, home_team_name,
                            away_team_id, away_team_name, status, home_score,
                            away_score, weather_data, raw_data, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        game.get('espn_id'),
                        game.get('date'),
                        game.get('home_team', {}).get('id'),
                        game.get('home_team', {}).get('name'),
                        game.get('away_team', {}).get('id'),
                        game.get('away_team', {}).get('name'),
                        game.get('status'),
                        game.get('home_team', {}).get('score', 0),
                        game.get('away_team', {}).get('score', 0),
                        json.dumps(game.get('weather', {})),
                        json.dumps(game),
                        datetime.now().isoformat(),
                        datetime.now().isoformat()
                    ))
                    saved_count += 1
                    
                except Exception as e:
                    logger.error(f"Error saving game {game.get('espn_id')}: {e}")
            
            conn.commit()
        
        logger.info(f"Saved {saved_count} games to database")
        return saved_count
    
    def save_teams(self, teams_data: List[Dict]) -> int:
        """Save teams data to database"""
        saved_count = 0
        
        with sqlite3.connect(self.db_path) as conn:
            for team in teams_data:
                try:
                    conn.execute('''
                        INSERT OR REPLACE INTO teams (
                            espn_id, name, abbreviation, city, last_updated
                        ) VALUES (?, ?, ?, ?, ?)
                    ''', (
                        team.get('id'),
                        team.get('name'),
                        team.get('abbreviation'),
                        team.get('location'),
                        datetime.now().isoformat()
                    ))
                    saved_count += 1
                    
                except Exception as e:
                    logger.error(f"Error saving team {team.get('name')}: {e}")
            
            conn.commit()
        
        logger.info(f"Saved {saved_count} teams to database")
        return saved_count
    
    def get_games(self, limit: int = 50) -> List[Dict]:
        """Get games from database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM games 
                ORDER BY game_date DESC 
                LIMIT ?
            ''', (limit,))
            
            games = []
            for row in cursor.fetchall():
                game = dict(row)
                # Parse JSON fields
                if game['weather_data']:
                    game['weather'] = json.loads(game['weather_data'])
                if game['raw_data']:
                    game['raw'] = json.loads(game['raw_data'])
                games.append(game)
            
            return games
    
    def get_teams(self) -> List[Dict]:
        """Get all teams from database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM teams ORDER BY name')
            
            return [dict(row) for row in cursor.fetchall()]
    
    def save_prediction(self, prediction: Dict) -> int:
        """Save a prediction to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO predictions (
                    game_id, predicted_winner, confidence, prediction_type,
                    factors, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                prediction.get('game_id'),
                prediction.get('predicted_winner'),
                prediction.get('confidence'),
                prediction.get('prediction_type', 'general'),
                json.dumps(prediction.get('factors', [])),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            games_count = conn.execute('SELECT COUNT(*) FROM games').fetchone()[0]
            teams_count = conn.execute('SELECT COUNT(*) FROM teams').fetchone()[0]
            predictions_count = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
            
            return {
                'games': games_count,
                'teams': teams_count,
                'predictions': predictions_count,
                'database_size': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            }