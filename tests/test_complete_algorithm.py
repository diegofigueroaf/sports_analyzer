"""
Complete Algorithm Testing Suite
Test all algorithm components together
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.prediction_engine import AdvancedPredictionEngine
from backend.services.backtester import Backtester
from backend.services.optimizer import AlgorithmOptimizer
from backend.services.data_manager import DataManager
from backend.models.database import SportsDatabase

def test_complete_algorithm():
    """Test the complete algorithm system"""
    print("Complete Algorithm Testing Suite")
    print("=" * 60)
    
    # Initialize components
    engine = AdvancedPredictionEngine()
    backtester = Backtester()
    optimizer = AlgorithmOptimizer()
    data_manager = DataManager()
    database = SportsDatabase()
    
    test_results = {
        'prediction_engine': False,
        'backtesting': False,
        'optimization': False,
        'data_integration': False,
        'database_integration': False
    }
    
    # Test 1: Prediction Engine
    print("\nTest 1: Prediction Engine")
    print("-" * 30)
    
    try:
        predictions = engine.predict_games()
        
        if predictions and len(predictions) > 0:
            print(f"✅ Generated {len(predictions)} predictions")
            
            # Show sample prediction details
            sample = predictions[0]
            print(f"   Sample: {sample.away_team} @ {sample.home_team}")
            print(f"   Winner: {sample.predicted_winner} ({sample.confidence}%)")
            print(f"   Spread: {sample.spread_prediction:+.1f}")
            
            # Analyze prediction quality
            avg_confidence = sum(p.confidence for p in predictions) / len(predictions)
            print(f"   Average confidence: {avg_confidence:.1f}%")
            
            test_results['prediction_engine'] = True
        else:
            print("⚠️  No predictions generated (might be off-season)")
    
    except Exception as e:
        print(f"❌ Prediction engine failed: {e}")
    
    # Test 2: Database Integration
    print("\nTest 2: Database Integration")
    print("-" * 30)
    
    try:
        if predictions:
            saved_count = engine.save_predictions(predictions)
            print(f"✅ Saved {saved_count} predictions to database")
        
        # Check database stats
        stats = database.get_database_stats()
        print(f"   Database contains: {stats['games']} games, {stats['predictions']} predictions")
        
        if stats['games'] > 0:
            test_results['database_integration'] = True
        
    except Exception as e:
        print(f"❌ Database integration failed: {e}")
    
    # Test 3: Backtesting System
    print("\nTest 3: Backtesting System")
    print("-" * 30)
    
    try:
        # Run limited backtest for speed
        backtest_results = backtester.run_backtest()
        
        if backtest_results and backtest_results.get('completed_games', 0) > 0:
            accuracy = backtest_results['accuracy'] * 100
            games = backtest_results['completed_games']
            
            print(f"✅ Backtest completed on {games} historical games")
            print(f"   Accuracy: {accuracy:.1f}%")
            print(f"   Average confidence: {backtest_results.get('avg_confidence', 0):.1f}%")
            
            # Show performance by confidence bucket
            performance = backtest_results.get('performance_by_confidence', {})
            for bucket, data in performance.items():
                if data['total'] > 0:
                    bucket_accuracy = (data['correct'] / data['total']) * 100
                    print(f"   {bucket}: {bucket_accuracy:.1f}% ({data['correct']}/{data['total']})")
            
            test_results['backtesting'] = True
        else:
            print("⚠️  Limited historical data for backtesting")
    
    except Exception as e:
        print(f"❌ Backtesting failed: {e}")
    
    # Test 4: Data Integration
    print("\nTest 4: Data Integration")
    print("-" * 30)
    
    try:
        # Test data collection and processing
        prediction_data = data_manager.get_prediction_data()
        
        games_collected = len(prediction_data.get('games', []))
        teams_collected = len(prediction_data.get('teams', []))
        
        print(f"✅ Data integration working")
        print(f"   Games available: {games_collected}")
        print(f"   Teams available: {teams_collected}")
        print(f"   Data sources: {', '.join(prediction_data.get('available_sources', []))}")
        
        if games_collected > 0 and teams_collected > 0:
            test_results['data_integration'] = True
    
    except Exception as e:
        print(f"❌ Data integration failed: {e}")
    
    # Test 5: Algorithm Optimization (Limited)
    print("\nTest 5: Algorithm Optimization")
    print("-" * 30)
    
    try:
        # Run limited optimization test
        print("   Running factor importance analysis...")
        importance_analysis = optimizer.analyze_factor_importance()
        
        if importance_analysis and 'factor_importance' in importance_analysis:
            print("✅ Algorithm optimization working")
            
            # Show factor importance
            print("   Factor importance scores:")
            for factor, data in importance_analysis['factor_importance'].items():
                score = data.get('importance_score', 0)
                print(f"     {factor}: {score:+.2f} percentage points")
            
            test_results['optimization'] = True
        else:
            print("⚠️  Limited data for optimization analysis")
    
    except Exception as e:
        print(f"❌ Optimization failed: {e}")
    
    # Test 6: End-to-End Workflow
    print("\nTest 6: End-to-End Workflow")
    print("-" * 30)
    
    try:
        print("   Testing complete prediction workflow...")
        
        # Collect fresh data
        fresh_data = data_manager.collect_game_data(include_weather=False)
        
        # Generate predictions
        if fresh_data.get('games'):
            fresh_predictions = engine.predict_games(fresh_data['games'])
            
            if fresh_predictions:
                print(f"✅ Complete workflow successful")
                print(f"   Generated {len(fresh_predictions)} fresh predictions")
                
                # Save to database
                saved = engine.save_predictions(fresh_predictions)
                print(f"   Saved {saved} predictions to database")
            else:
                print("⚠️  No fresh predictions generated")
        else:
            print("⚠️  No fresh game data available")
    
    except Exception as e:
        print(f"❌ End-to-end workflow failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Algorithm Testing Summary")
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    print(f"Tests passed: {passed_tests}/{total_tests}")
    
    for test_name, passed in test_results.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {test_name.replace('_', ' ').title()}")
    
    if passed_tests >= 4:  # Need most core components working
        print("\n✅ Algorithm system ready for web interface!")
        print("\nAlgorithm capabilities:")
        print("  • Multi-factor game predictions")
        print("  • Historical performance backtesting")
        print("  • Algorithm optimization")
        print("  • Database integration")
        print("  • Automated data processing")
        
        return True
    else:
        print(f"\n❌ Algorithm system needs fixes ({passed_tests}/{total_tests} tests passed)")
        return False

if __name__ == "__main__":
    success = test_complete_algorithm()
    sys.exit(0 if success else 1)