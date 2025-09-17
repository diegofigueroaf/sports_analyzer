"""
Algorithm Optimizer
Optimize prediction algorithm parameters for best performance
"""
from datetime import datetime
from typing import Dict, List, Tuple
import logging
from .backtester import Backtester
from .prediction_engine import AdvancedPredictionEngine
import itertools

logger = logging.getLogger(__name__)

class AlgorithmOptimizer:
    """Optimize prediction algorithm parameters"""
    
    def __init__(self):
        self.backtester = Backtester()
        self.base_engine = AdvancedPredictionEngine()
        logger.info("Initialized algorithm optimizer")
    
    def optimize_factor_weights(self) -> Dict:
        """Optimize the weights of prediction factors"""
        logger.info("Starting factor weight optimization")
        
        # Define weight ranges to test (sum must equal 1.0)
        weight_options = {
            'team_strength': [0.25, 0.30, 0.35, 0.40],
            'head_to_head': [0.15, 0.20, 0.25],
            'home_advantage': [0.10, 0.15, 0.20],
            'rest_advantage': [0.05, 0.10, 0.15],
            'weather_impact': [0.05, 0.10, 0.15],
            'motivation': [0.02, 0.05, 0.08],
            'injuries': [0.02, 0.05, 0.08]
        }
        
        best_accuracy = 0
        best_weights = None
        best_results = None
        
        # Test different weight combinations
        # Note: This is simplified - full optimization would test many more combinations
        test_combinations = self._generate_weight_combinations(weight_options)
        
        results_log = []
        
        for i, weights in enumerate(test_combinations[:10]):  # Limit to 10 tests for speed
            logger.info(f"Testing weight combination {i+1}/10")
            
            # Update engine with test weights
            test_engine = self._create_test_engine(weights)
            
            # Run backtest with these weights
            backtest_results = self._run_test_backtest(test_engine)
            
            if backtest_results and backtest_results.get('accuracy', 0) > best_accuracy:
                best_accuracy = backtest_results['accuracy']
                best_weights = weights
                best_results = backtest_results
            
            results_log.append({
                'weights': weights,
                'accuracy': backtest_results.get('accuracy', 0),
                'total_games': backtest_results.get('completed_games', 0)
            })
        
        return {
            'best_weights': best_weights,
            'best_accuracy': best_accuracy,
            'best_results': best_results,
            'all_tests': results_log,
            'optimization_date': datetime.now().isoformat()
        }
    
    def _generate_weight_combinations(self, weight_options: Dict) -> List[Dict]:
        """Generate valid weight combinations that sum to 1.0"""
        combinations = []
        
        # Simple approach: test a few reasonable combinations
        # Full optimization would use more sophisticated methods
        
        combinations.extend([
            # Balanced approach
            {
                'team_strength': 0.35,
                'head_to_head': 0.20,
                'home_advantage': 0.15,
                'rest_advantage': 0.10,
                'weather_impact': 0.10,
                'motivation': 0.05,
                'injuries': 0.05
            },
            # Heavy team strength focus
            {
                'team_strength': 0.45,
                'head_to_head': 0.15,
                'home_advantage': 0.15,
                'rest_advantage': 0.10,
                'weather_impact': 0.08,
                'motivation': 0.04,
                'injuries': 0.03
            },
            # Historical focus
            {
                'team_strength': 0.30,
                'head_to_head': 0.30,
                'home_advantage': 0.15,
                'rest_advantage': 0.10,
                'weather_impact': 0.08,
                'motivation': 0.04,
                'injuries': 0.03
            }
        ])
        
        return combinations
    
    def _create_test_engine(self, weights: Dict) -> AdvancedPredictionEngine:
        """Create prediction engine with test weights"""
        engine = AdvancedPredictionEngine()
        engine.factor_weights = weights
        return engine
    
    def _run_test_backtest(self, engine: AdvancedPredictionEngine) -> Dict:
        """Run simplified backtest for optimization"""
        try:
            # Get a sample of historical games for quick testing
            historical_games = self.backtester._get_historical_games()[:50]  # Test on 50 games
            
            if not historical_games:
                return {'accuracy': 0, 'completed_games': 0}
            
            correct = 0
            total = 0
            
            for game in historical_games:
                if not self.backtester._is_game_completed(game):
                    continue
                
                prediction = self.backtester._predict_historical_game(game)
                if not prediction:
                    continue
                
                actual_winner = self.backtester._get_actual_winner(game)
                
                if prediction.predicted_winner == actual_winner:
                    correct += 1
                total += 1
            
            accuracy = correct / total if total > 0 else 0
            
            return {
                'accuracy': accuracy,
                'completed_games': total,
                'correct_predictions': correct
            }
            
        except Exception as e:
            logger.error(f"Error in test backtest: {e}")
            return {'accuracy': 0, 'completed_games': 0}
    
    def analyze_factor_importance(self) -> Dict:
        """Analyze which factors are most important for predictions"""
        logger.info("Analyzing factor importance")
        
        # Run backtest with current settings
        baseline_results = self.backtester.run_backtest()
        
        if not baseline_results or baseline_results.get('completed_games', 0) == 0:
            return {'error': 'No historical data available for analysis'}
        
        # Test removing each factor individually
        factor_analysis = {}
        
        for factor_name in self.base_engine.factor_weights.keys():
            logger.info(f"Testing impact of removing {factor_name}")
            
            # Create engine without this factor
            test_weights = self.base_engine.factor_weights.copy()
            removed_weight = test_weights.pop(factor_name)
            
            # Redistribute the weight proportionally
            total_remaining = sum(test_weights.values())
            if total_remaining > 0:
                for key in test_weights:
                    test_weights[key] += (removed_weight * test_weights[key] / total_remaining)
            
            # Test performance without this factor
            test_engine = self._create_test_engine(test_weights)
            test_results = self._run_test_backtest(test_engine)
            
            accuracy_drop = baseline_results['accuracy'] - test_results.get('accuracy', 0)
            
            factor_analysis[factor_name] = {
                'baseline_accuracy': baseline_results['accuracy'],
                'without_factor_accuracy': test_results.get('accuracy', 0),
                'accuracy_drop': accuracy_drop,
                'importance_score': accuracy_drop * 100  # Convert to percentage points
            }
        
        return {
            'baseline_accuracy': baseline_results['accuracy'],
            'factor_importance': factor_analysis,
            'analysis_date': datetime.now().isoformat()
        }
    
    def recommend_improvements(self) -> Dict:
        """Generate recommendations for algorithm improvements"""
        logger.info("Generating improvement recommendations")
        
        # Run various analyses
        optimization_results = self.optimize_factor_weights()
        importance_analysis = self.analyze_factor_importance()
        
        recommendations = []
        
        # Weight optimization recommendations
        if optimization_results.get('best_accuracy', 0) > self.base_engine.get_model_performance().get('accuracy_percentage', 0):
            recommendations.append({
                'type': 'weight_optimization',
                'priority': 'high',
                'description': f"Optimize factor weights to improve accuracy by {(optimization_results['best_accuracy'] * 100):.1f}%",
                'suggested_weights': optimization_results['best_weights']
            })
        
        # Factor importance recommendations
        if importance_analysis.get('factor_importance'):
            low_impact_factors = [
                name for name, data in importance_analysis['factor_importance'].items()
                if data['importance_score'] < 1.0  # Less than 1% accuracy impact
            ]
            
            if low_impact_factors:
                recommendations.append({
                    'type': 'factor_removal',
                    'priority': 'medium',
                    'description': f"Consider removing low-impact factors: {', '.join(low_impact_factors)}",
                    'factors': low_impact_factors
                })
        
        # Data quality recommendations
        recommendations.append({
            'type': 'data_enhancement',
            'priority': 'medium',
            'description': "Implement weather API integration for better outdoor game predictions",
            'action': 'weather_integration'
        })
        
        recommendations.append({
            'type': 'data_enhancement',
            'priority': 'low',
            'description': "Add injury report analysis for more accurate predictions",
            'action': 'injury_integration'
        })
        
        return {
            'recommendations': recommendations,
            'current_performance': {
                'accuracy': optimization_results.get('best_accuracy', 0),
                'total_games_analyzed': optimization_results.get('best_results', {}).get('completed_games', 0)
            },
            'generated_at': datetime.now().isoformat()
        }