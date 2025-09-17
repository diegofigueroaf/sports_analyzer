"""
Advanced Prediction Engine
Multi-factor NFL game prediction system
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import json
from dataclasses import dataclass
from .data_manager import DataManager
from ..models.database import SportsDatabase
from config.data_sources import NFL_STADIUMS

logger = logging.getLogger(__name__)

@dataclass
class PredictionFactor:
    name: str
    value: float  # -100 to +100 (negative favors away, positive favors home)
    weight: float  # 0.0 to 1.0 (importance)
    confidence: float  # 0.0 to 1.0 (data quality)
    explanation: str

@dataclass
class GamePrediction:
    game_id: str
    home_team: str
    away_team: str
    predicted_winner: str
    confidence: float
    spread_prediction: float
    total_prediction: Optional[float]
    factors: List[PredictionFactor]
    algorithm_version: str
    created_at: str

class AdvancedPredictionEngine:
    """Advanced multi-factor prediction engine"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.database = SportsDatabase()
        self.version = "1.0"
        
        # Factor weights (tunable parameters)
        self.factor_weights = {
            'team_strength': 0.35,      # Win/loss records, recent form
            'head_to_head': 0.20,       # Historical matchups
            'home_advantage': 0.15,     # Home field advantage
            'rest_advantage': 0.10,     # Days of rest difference
            'weather_impact': 0.10,     # Weather conditions
            'motivation': 0.05,         # Playoff implications, division games
            'injuries': 0.05           # Key player availability (placeholder)
        }
        
        logger.info(f"Initialized Prediction Engine v{self.version}")
    
    def predict_games(self, games_data: List[Dict] = None) -> List[GamePrediction]:
        """Generate predictions for multiple games"""
        if not games_data:
            # Get current games from data manager
            prediction_data = self.data_manager.get_prediction_data()
            games_data = prediction_data.get('games', [])
        
        predictions = []
        
        for game in games_data:
            try:
                prediction = self._predict_single_game(game)
                if prediction:
                    predictions.append(prediction)
            except Exception as e:
                logger.error(f"Failed to predict game {game.get('espn_id')}: {e}")
        
        logger.info(f"Generated {len(predictions)} game predictions")
        return predictions
    
    def _predict_single_game(self, game: Dict) -> Optional[GamePrediction]:
        """Predict outcome for a single game"""
        if game.get('status') != 'STATUS_SCHEDULED':
            return None  # Only predict upcoming games
        
        home_team = game['home_team']
        away_team = game['away_team']
        
        # Collect all prediction factors
        factors = [
            self._calculate_team_strength_factor(home_team, away_team),
            self._calculate_head_to_head_factor(home_team['id'], away_team['id']),
            self._calculate_home_advantage_factor(home_team['id']),
            self._calculate_rest_factor(game),
            self._calculate_weather_factor(game),
            self._calculate_motivation_factor(game),
            self._calculate_injury_factor(home_team['id'], away_team['id'])
        ]
        
        # Calculate weighted prediction
        prediction_result = self._calculate_final_prediction(factors, home_team, away_team)
        
        return GamePrediction(
            game_id=game['espn_id'],
            home_team=home_team['name'],
            away_team=away_team['name'],
            predicted_winner=prediction_result['winner'],
            confidence=prediction_result['confidence'],
            spread_prediction=prediction_result['spread'],
            total_prediction=prediction_result.get('total'),
            factors=factors,
            algorithm_version=self.version,
            created_at=datetime.now().isoformat()
        )
    
    def _calculate_team_strength_factor(self, home_team: Dict, away_team: Dict) -> PredictionFactor:
        """Calculate team strength differential"""
        try:
            # Get win percentages
            home_record = home_team.get('record', {'wins': 0, 'losses': 0, 'ties': 0})
            away_record = away_team.get('record', {'wins': 0, 'losses': 0, 'ties': 0})
            
            home_games = home_record['wins'] + home_record['losses'] + home_record['ties']
            away_games = away_record['wins'] + away_record['losses'] + away_record['ties']
            
            if home_games == 0 or away_games == 0:
                return PredictionFactor(
                    name="Team Strength",
                    value=0,
                    weight=self.factor_weights['team_strength'],
                    confidence=0.1,
                    explanation="Insufficient season data"
                )
            
            home_win_pct = (home_record['wins'] + 0.5 * home_record['ties']) / home_games
            away_win_pct = (away_record['wins'] + 0.5 * away_record['ties']) / away_games
            
            # Convert to point differential (roughly 14 points per 100% win rate difference)
            strength_diff = (home_win_pct - away_win_pct) * 14
            
            return PredictionFactor(
                name="Team Strength",
                value=strength_diff,
                weight=self.factor_weights['team_strength'],
                confidence=min(0.9, (home_games + away_games) / 20),  # Higher confidence with more games
                explanation=f"Home: {home_win_pct:.1%} ({home_record['wins']}-{home_record['losses']}) vs Away: {away_win_pct:.1%} ({away_record['wins']}-{away_record['losses']})"
            )
            
        except Exception as e:
            logger.warning(f"Error calculating team strength: {e}")
            return PredictionFactor("Team Strength", 0, 0, 0, "Calculation error")
    
    def _calculate_head_to_head_factor(self, home_team_id: str, away_team_id: str) -> PredictionFactor:
        """Calculate head-to-head historical performance"""
        try:
            # Get historical games between these teams from database
            historical_games = self._get_historical_matchups(home_team_id, away_team_id)
            
            if len(historical_games) < 3:
                return PredictionFactor(
                    name="Head-to-Head",
                    value=0,
                    weight=self.factor_weights['head_to_head'],
                    confidence=0.2,
                    explanation="Limited historical data"
                )
            
            # Analyze recent matchups (last 5 games)
            recent_games = historical_games[-5:]
            home_wins = 0
            total_point_diff = 0
            
            for game in recent_games:
                if game['home_team_id'] == home_team_id:
                    # Current home team was home
                    if game['home_score'] > game['away_score']:
                        home_wins += 1
                    total_point_diff += (game['home_score'] - game['away_score'])
                else:
                    # Current home team was away
                    if game['away_score'] > game['home_score']:
                        home_wins += 1
                    total_point_diff += (game['away_score'] - game['home_score'])
            
            avg_point_diff = total_point_diff / len(recent_games)
            
            return PredictionFactor(
                name="Head-to-Head",
                value=avg_point_diff,
                weight=self.factor_weights['head_to_head'],
                confidence=min(0.8, len(recent_games) / 5),
                explanation=f"Last {len(recent_games)} games: avg margin {avg_point_diff:+.1f} points"
            )
            
        except Exception as e:
            logger.warning(f"Error calculating head-to-head: {e}")
            return PredictionFactor("Head-to-Head", 0, 0, 0, "Historical data unavailable")
    
    def _calculate_home_advantage_factor(self, home_team_id: str) -> PredictionFactor:
        """Calculate home field advantage"""
        try:
            stadium_info = NFL_STADIUMS.get(home_team_id, {})
            
            # Base home advantage
            base_advantage = 2.5  # NFL average
            
            # Adjust for specific factors
            if stadium_info.get('dome', False):
                base_advantage += 0.5  # Dome advantage (controlled conditions)
            
            # Could add more factors: altitude, crowd noise, etc.
            
            return PredictionFactor(
                name="Home Advantage",
                value=base_advantage,
                weight=self.factor_weights['home_advantage'],
                confidence=0.9,
                explanation=f"Standard home advantage: {base_advantage:.1f} points"
            )
            
        except Exception as e:
            logger.warning(f"Error calculating home advantage: {e}")
            return PredictionFactor("Home Advantage", 2.5, self.factor_weights['home_advantage'], 0.8, "Standard advantage")
    
    def _calculate_rest_factor(self, game: Dict) -> PredictionFactor:
        """Calculate rest advantage"""
        try:
            # This would require tracking when teams last played
            # For now, return neutral
            return PredictionFactor(
                name="Rest Advantage",
                value=0,
                weight=self.factor_weights['rest_advantage'],
                confidence=0.1,
                explanation="Rest data not implemented"
            )
            
        except Exception as e:
            return PredictionFactor("Rest Advantage", 0, 0, 0, "Data unavailable")
    
    def _calculate_weather_factor(self, game: Dict) -> PredictionFactor:
        """Calculate weather impact on game"""
        try:
            weather = game.get('weather', {})
            
            if not weather or weather.get('status') == 'not_needed':
                return PredictionFactor(
                    name="Weather",
                    value=0,
                    weight=self.factor_weights['weather_impact'],
                    confidence=0.9,
                    explanation="Indoor game - no weather impact"
                )
            
            if weather.get('status') == 'unavailable':
                return PredictionFactor(
                    name="Weather",
                    value=0,
                    weight=self.factor_weights['weather_impact'],
                    confidence=0.1,
                    explanation="Weather data unavailable"
                )
            
            # Use weather impact calculation if available
            game_impact = weather.get('game_impact', {})
            total_impact = game_impact.get('total_score_impact', 0)
            
            return PredictionFactor(
                name="Weather",
                value=total_impact,
                weight=self.factor_weights['weather_impact'],
                confidence=0.7,
                explanation=f"Weather impact: {total_impact:+.1f} points ({weather.get('conditions', 'unknown')})"
            )
            
        except Exception as e:
            logger.warning(f"Error calculating weather factor: {e}")
            return PredictionFactor("Weather", 0, 0, 0, "Weather calculation error")
    
    def _calculate_motivation_factor(self, game: Dict) -> PredictionFactor:
        """Calculate motivation factors (division games, playoff implications)"""
        try:
            # Placeholder for motivation analysis
            # Could analyze: division games, playoff race, rivalry games, etc.
            
            return PredictionFactor(
                name="Motivation",
                value=0,
                weight=self.factor_weights['motivation'],
                confidence=0.2,
                explanation="Motivation factors not implemented"
            )
            
        except Exception as e:
            return PredictionFactor("Motivation", 0, 0, 0, "Motivation data unavailable")
    
    def _calculate_injury_factor(self, home_team_id: str, away_team_id: str) -> PredictionFactor:
        """Calculate impact of key injuries"""
        try:
            # Placeholder for injury analysis
            # Would analyze injury reports, key player status, etc.
            
            return PredictionFactor(
                name="Injuries",
                value=0,
                weight=self.factor_weights['injuries'],
                confidence=0.1,
                explanation="Injury analysis not implemented"
            )
            
        except Exception as e:
            return PredictionFactor("Injuries", 0, 0, 0, "Injury data unavailable")
    
    def _calculate_final_prediction(self, factors: List[PredictionFactor], 
                                  home_team: Dict, away_team: Dict) -> Dict:
        """Calculate final prediction from all factors"""
        total_weighted_value = 0
        total_weight = 0
        
        # Calculate weighted average of all factors
        for factor in factors:
            if factor.confidence > 0:
                weighted_value = factor.value * factor.weight * factor.confidence
                total_weighted_value += weighted_value
                total_weight += factor.weight * factor.confidence
        
        # Normalize to get final point spread
        if total_weight > 0:
            predicted_spread = total_weighted_value / total_weight
        else:
            predicted_spread = 0
        
        # Determine winner and confidence
        if predicted_spread > 0:
            winner = home_team['name']
            confidence = min(85, abs(predicted_spread) * 8 + 50)  # 50-85% range
        else:
            winner = away_team['name']
            confidence = min(85, abs(predicted_spread) * 8 + 50)
        
        return {
            'winner': winner,
            'confidence': round(confidence, 1),
            'spread': round(predicted_spread, 1),
            'total': None  # Not implemented yet
        }
    
    def _get_historical_matchups(self, team1_id: str, team2_id: str) -> List[Dict]:
        """Get historical games between two teams"""
        try:
            games = self.database.get_games(limit=100)  # Get recent games
            
            # Filter for matchups between these teams
            matchups = []
            for game in games:
                if ((game['home_team_id'] == team1_id and game['away_team_id'] == team2_id) or
                    (game['home_team_id'] == team2_id and game['away_team_id'] == team1_id)):
                    matchups.append(game)
            
            return matchups
            
        except Exception as e:
            logger.error(f"Error getting historical matchups: {e}")
            return []
    
    def save_predictions(self, predictions: List[GamePrediction]) -> int:
        """Save predictions to database"""
        saved_count = 0
        
        for prediction in predictions:
            try:
                prediction_data = {
                    'game_id': prediction.game_id,
                    'predicted_winner': prediction.predicted_winner,
                    'confidence': prediction.confidence,
                    'prediction_type': 'spread',
                    'factors': [
                        {
                            'name': f.name,
                            'value': f.value,
                            'weight': f.weight,
                            'confidence': f.confidence,
                            'explanation': f.explanation
                        }
                        for f in prediction.factors
                    ]
                }
                
                self.database.save_prediction(prediction_data)
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving prediction for game {prediction.game_id}: {e}")
        
        logger.info(f"Saved {saved_count} predictions to database")
        return saved_count
    
    def get_model_performance(self) -> Dict:
        """Get performance metrics for the prediction model"""
        try:
            # This would analyze historical predictions vs actual results
            # For now, return placeholder metrics
            
            return {
                'total_predictions': 0,
                'correct_predictions': 0,
                'accuracy_percentage': 0.0,
                'average_confidence': 0.0,
                'model_version': self.version
            }
            
        except Exception as e:
            logger.error(f"Error calculating model performance: {e}")
            return {'error': str(e)}