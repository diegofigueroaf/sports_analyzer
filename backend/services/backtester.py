"""
Backtesting System
Test prediction algorithm against historical data
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from ..models.database import SportsDatabase
from .prediction_engine import AdvancedPredictionEngine
import json

logger = logging.getLogger(__name__)

class Backtester:
    """Backtest prediction algorithms against historical data"""
    
    def __init__(self):
        self.database = SportsDatabase()
        self.prediction_engine = AdvancedPredictionEngine()
        logger.info("Initialized backtesting system")
    
    def run_backtest(self, start_date: str = None, end_date: str = None) -> Dict:
        """Run backtest on historical games"""
        logger.info(f"Running backtest from {start_date} to {end_date}")
        
        # Get historical games
        historical_games = self._get_historical_games(start_date, end_date)
        
        if not historical_games:
            return {
                'error': 'No historical games found for backtesting',
                'games_analyzed': 0
            }
        
        results = {
            'total_games': len(historical_games),
            'completed_games': 0,
            'correct_predictions': 0,
            'accuracy': 0.0,
            'avg_confidence': 0.0,
            'predictions': [],
            'performance_by_confidence': {},
            'factor_analysis': {}
        }
        
        total_confidence = 0
        confidence_buckets = {
            '50-60%': {'correct': 0, 'total': 0},
            '60-70%': {'correct': 0, 'total': 0},
            '70-80%': {'correct': 0, 'total': 0},
            '80%+': {'correct': 0, 'total': 0}
        }
        
        for game in historical_games:
            # Only analyze completed games
            if not self._is_game_completed(game):
                continue
            
            # Generate prediction for this historical game
            prediction = self._predict_historical_game(game)
            
            if not prediction:
                continue
            
            results['completed_games'] += 1
            
            # Check if prediction was correct
            actual_winner = self._get_actual_winner(game)
            predicted_winner = prediction.predicted_winner
            
            is_correct = actual_winner == predicted_winner
            
            if is_correct:
                results['correct_predictions'] += 1
            
            # Track confidence buckets
            confidence = prediction.confidence
            total_confidence += confidence
            
            bucket = self._get_confidence_bucket(confidence)
            confidence_buckets[bucket]['total'] += 1
            if is_correct:
                confidence_buckets[bucket]['correct'] += 1
            
            # Store prediction result
            results['predictions'].append({
                'game_id': game['espn_id'],
                'matchup': f"{game['away_team_name']} @ {game['home_team_name']}",
                'predicted_winner': predicted_winner,
                'actual_winner': actual_winner,
                'confidence': confidence,
                'correct': is_correct,
                'factors': [
                    {
                        'name': f.name,
                        'value': f.value,
                        'weight': f.weight
                    }
                    for f in prediction.factors
                ]
            })
        
        # Calculate final metrics
        if results['completed_games'] > 0:
            results['accuracy'] = results['correct_predictions'] / results['completed_games']
            results['avg_confidence'] = total_confidence / results['completed_games']
        
        results['performance_by_confidence'] = confidence_buckets
        results['factor_analysis'] = self._analyze_factors(results['predictions'])
        
        logger.info(f"Backtest complete: {results['accuracy']:.1%} accuracy on {results['completed_games']} games")
        return results
    
    def _get_historical_games(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get historical games from database"""
        try:
            # For now, get all completed games
            all_games = self.database.get_games(limit=500)
            
            # Filter for completed games only
            completed_games = [
                game for game in all_games 
                if self._is_game_completed(game)
            ]
            
            # Apply date filters if provided
            if start_date or end_date:
                # Date filtering logic would go here
                pass
            
            return completed_games
            
        except Exception as e:
            logger.error(f"Error getting historical games: {e}")
            return []
    
    def _is_game_completed(self, game: Dict) -> bool:
        """Check if game is completed with a final score"""
        return (game.get('status') == 'STATUS_FINAL' or 
                (game.get('home_score', 0) > 0 or game.get('away_score', 0) > 0))
    
    def _predict_historical_game(self, game: Dict) -> Optional:
        """Generate prediction for historical game using current algorithm"""
        try:
            # Convert database game format to prediction engine format
            game_data = {
                'espn_id': game['espn_id'],
                'status': 'STATUS_SCHEDULED',  # Pretend it's upcoming
                'home_team': {
                    'id': game['home_team_id'],
                    'name': game['home_team_name'],
                    'record': {'wins': 0, 'losses': 0, 'ties': 0}  # Would need historical records
                },
                'away_team': {
                    'id': game['away_team_id'],
                    'name': game['away_team_name'],
                    'record': {'wins': 0, 'losses': 0, 'ties': 0}  # Would need historical records
                },
                'weather': json.loads(game.get('weather_data', '{}')) if game.get('weather_data') else {}
            }
            
            return self.prediction_engine._predict_single_game(game_data)
            
        except Exception as e:
            logger.warning(f"Error predicting historical game {game.get('espn_id')}: {e}")
            return None
    
    def _get_actual_winner(self, game: Dict) -> str:
        """Determine actual winner from game result"""
        home_score = game.get('home_score', 0)
        away_score = game.get('away_score', 0)
        
        if home_score > away_score:
            return game['home_team_name']
        elif away_score > home_score:
            return game['away_team_name']
        else:
            return 'TIE'
    
    def _get_confidence_bucket(self, confidence: float) -> str:
        """Categorize prediction confidence"""
        if confidence >= 80:
            return '80%+'
        elif confidence >= 70:
            return '70-80%'
        elif confidence >= 60:
            return '60-70%'
        else:
            return '50-60%'
    
    def _analyze_factors(self, predictions: List[Dict]) -> Dict:
        """Analyze which factors contribute most to accuracy"""
        factor_performance = {}
        
        for pred in predictions:
            is_correct = pred['correct']
            
            for factor in pred['factors']:
                name = factor['name']
                
                if name not in factor_performance:
                    factor_performance[name] = {
                        'total_predictions': 0,
                        'correct_predictions': 0,
                        'avg_impact': 0,
                        'accuracy': 0
                    }
                
                factor_performance[name]['total_predictions'] += 1
                factor_performance[name]['avg_impact'] += abs(factor['value'])
                
                if is_correct:
                    factor_performance[name]['correct_predictions'] += 1
        
        # Calculate averages
        for name, stats in factor_performance.items():
            if stats['total_predictions'] > 0:
                stats['accuracy'] = stats['correct_predictions'] / stats['total_predictions']
                stats['avg_impact'] = stats['avg_impact'] / stats['total_predictions']
        
        return factor_performance
    
    def simulate_betting_performance(self, backtest_results: Dict, 
                                   bet_amount: float = 100) -> Dict:
        """Simulate betting performance based on predictions"""
        total_bets = 0
        total_winnings = 0
        total_wagered = 0
        
        for prediction in backtest_results.get('predictions', []):
            # Only bet on high-confidence predictions
            if prediction['confidence'] < 60:
                continue
            
            total_bets += 1
            total_wagered += bet_amount
            
            if prediction['correct']:
                # Assume -110 odds (win $90.91 on $100 bet)
                total_winnings += bet_amount * 0.9091
            
        profit_loss = total_winnings - total_wagered
        roi = (profit_loss / total_wagered * 100) if total_wagered > 0 else 0
        
        return {
            'total_bets': total_bets,
            'total_wagered': total_wagered,
            'total_winnings': total_winnings,
            'profit_loss': profit_loss,
            'roi_percentage': roi,
            'break_even_accuracy': 52.38  # Need 52.38% to break even at -110 odds
        }