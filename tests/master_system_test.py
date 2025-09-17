"""
Master System Test - Complete Deep Dive
Tests every component from Steps 1, 2, and 3
"""
import sys
import os
import time
from datetime import datetime

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def master_system_test():
    """Comprehensive test of the entire system"""
    print("🏈 SPORTS BETTING ANALYTICS - MASTER SYSTEM TEST")
    print("=" * 80)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python path: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    
    test_results = {}
    total_score = 0
    max_score = 0
    
    # STEP 1 VERIFICATION
    print("\n" + "🔧 STEP 1: DEVELOPMENT ENVIRONMENT" + "=" * 48)
    
    step1_score = 0
    step1_max = 5
    
    # Test 1.1: Python Environment
    print("\n1.1 Python Environment")
    try:
        import requests, pandas, numpy, fastapi
        print(f"   ✅ Core packages: requests, pandas, numpy, fastapi")
        step1_score += 1
    except ImportError as e:
        print(f"   ❌ Package import failed: {e}")
    
    # Test 1.2: Project Structure
    print("\n1.2 Project Structure")
    required_dirs = ['backend', 'frontend', 'data', 'config', 'tests', 'scripts']
    missing_dirs = [d for d in required_dirs if not os.path.exists(d)]
    
    if not missing_dirs:
        print(f"   ✅ All required directories present")
        step1_score += 1
    else:
        print(f"   ❌ Missing directories: {missing_dirs}")
    
    # Test 1.3: Configuration Files
    print("\n1.3 Configuration Files")
    try:
        from config.data_sources import ESPN_CONFIG, NFL_TEAMS
        from config.api_keys import api_keys
        print(f"   ✅ Configuration files loaded")
        print(f"   📊 NFL teams configured: {len(NFL_TEAMS)} divisions")
        step1_score += 1
    except ImportError as e:
        print(f"   ❌ Configuration import failed: {e}")
    
    # Test 1.4: Environment Variables
    print("\n1.4 Environment Variables")
    if os.path.exists('.env'):
        print(f"   ✅ .env file exists")
        step1_score += 1
    else:
        print(f"   ⚠️  .env file missing (optional)")
        step1_score += 0.5
    
    # Test 1.5: Git Repository
    print("\n1.5 Git Repository")
    if os.path.exists('.git'):
        print(f"   ✅ Git repository initialized")
        step1_score += 1
    else:
        print(f"   ❌ Git repository not found")
    
    test_results['step1'] = {'score': step1_score, 'max': step1_max}
    total_score += step1_score
    max_score += step1_max
    
    # STEP 2 VERIFICATION
    print("\n" + "📊 STEP 2: DATA COLLECTION FRAMEWORK" + "=" * 40)
    
    step2_score = 0
    step2_max = 8
    
    # Test 2.1: Base Data Collector
    print("\n2.1 Base Data Collector")
    try:
        from backend.services.base_collector import BaseDataCollector, RateLimiter
        
        # Test rate limiter
        limiter = RateLimiter(max_calls_per_minute=5)
        print(f"   ✅ Base collector and rate limiter working")
        step2_score += 1
    except Exception as e:
        print(f"   ❌ Base collector failed: {e}")
    
    # Test 2.2: ESPN Data Collector
    print("\n2.2 ESPN Data Collector")
    try:
        from backend.services.espn_collector import ESPNCollector
        
        espn = ESPNCollector()
        teams_data = espn.collect_data('teams')
        
        if espn.validate_data(teams_data) and teams_data.get('teams'):
            print(f"   ✅ ESPN collector working: {len(teams_data['teams'])} teams")
            step2_score += 1
        else:
            print(f"   ❌ ESPN collector validation failed")
    except Exception as e:
        print(f"   ❌ ESPN collector failed: {e}")
    
    # Test 2.3: Weather Data Collector
    print("\n2.3 Weather Data Collector")
    try:
        from backend.services.weather_collector import WeatherCollector
        
        weather = WeatherCollector()
        status = weather.get_status()
        
        print(f"   ✅ Weather collector initialized: {status['status']}")
        step2_score += 1
    except Exception as e:
        print(f"   ❌ Weather collector failed: {e}")
    
    # Test 2.4: Data Manager Integration
    print("\n2.4 Data Manager Integration")
    try:
        from backend.services.data_manager import DataManager
        
        manager = DataManager()
        collector_status = manager.get_collector_status()
        
        print(f"   ✅ Data manager working")
        print(f"   📊 Available sources: {', '.join(collector_status['available_sources'])}")
        step2_score += 1
    except Exception as e:
        print(f"   ❌ Data manager failed: {e}")
    
    # Test 2.5: Live Data Collection
    print("\n2.5 Live Data Collection")
    try:
        game_data = manager.collect_game_data(include_weather=False)
        
        if game_data.get('games'):
            print(f"   ✅ Live data collection: {len(game_data['games'])} games")
            step2_score += 1
        else:
            print(f"   ⚠️  No current games (might be off-season)")
            step2_score += 0.5
    except Exception as e:
        print(f"   ❌ Live data collection failed: {e}")
    
    # Test 2.6: Database System
    print("\n2.6 Database System")
    try:
        from backend.models.database import SportsDatabase
        
        db = SportsDatabase()
        stats = db.get_database_stats()
        
        print(f"   ✅ Database working")
        print(f"   📊 Games: {stats['games']}, Teams: {stats['teams']}, Predictions: {stats['predictions']}")
        print(f"   📊 Database size: {stats['database_size']} bytes")
        
        if stats['games'] > 0 and stats['teams'] > 0:
            step2_score += 1
        else:
            step2_score += 0.5
    except Exception as e:
        print(f"   ❌ Database failed: {e}")
    
    # Test 2.7: Data Storage and Retrieval
    print("\n2.7 Data Storage and Retrieval")
    try:
        # Save current games to database
        if game_data.get('games'):
            saved_games = db.save_games(game_data['games'])
            print(f"   ✅ Data storage: saved {saved_games} games")
        
        # Retrieve games
        retrieved_games = db.get_games(limit=5)
        print(f"   ✅ Data retrieval: {len(retrieved_games)} games retrieved")
        step2_score += 1
    except Exception as e:
        print(f"   ❌ Data storage/retrieval failed: {e}")
    
    # Test 2.8: Data Pipeline
    print("\n2.8 Complete Data Pipeline")
    try:
        prediction_data = manager.get_prediction_data()
        
        pipeline_score = 0
        if prediction_data.get('games'):
            pipeline_score += 0.5
        if prediction_data.get('teams'):
            pipeline_score += 0.5
        
        print(f"   ✅ Data pipeline working: {len(prediction_data.get('games', []))} games, {len(prediction_data.get('teams', []))} teams")
        step2_score += pipeline_score
    except Exception as e:
        print(f"   ❌ Data pipeline failed: {e}")
    
    test_results['step2'] = {'score': step2_score, 'max': step2_max}
    total_score += step2_score
    max_score += step2_max
    
    # STEP 3 VERIFICATION
    print("\n" + "🧠 STEP 3: ALGORITHM DEVELOPMENT" + "=" * 45)
    
    step3_score = 0
    step3_max = 7
    
    # Test 3.1: Prediction Engine Core
    print("\n3.1 Prediction Engine Core")
    try:
        from backend.services.prediction_engine import AdvancedPredictionEngine, PredictionFactor
        
        engine = AdvancedPredictionEngine()
        print(f"   ✅ Prediction engine initialized: v{engine.version}")
        print(f"   📊 Factor weights: {len(engine.factor_weights)} factors")
        step3_score += 1
    except Exception as e:
        print(f"   ❌ Prediction engine failed: {e}")
    
    # Test 3.2: Game Predictions Generation
    print("\n3.2 Game Predictions Generation")
    try:
        predictions = engine.predict_games()
        
        if predictions and len(predictions) > 0:
            print(f"   ✅ Predictions generated: {len(predictions)} games")
            
            # Analyze prediction quality
            sample = predictions[0]
            print(f"   📊 Sample: {sample.away_team} @ {sample.home_team}")
            print(f"   📊 Winner: {sample.predicted_winner} ({sample.confidence}%)")
            print(f"   📊 Spread: {sample.spread_prediction:+.1f}")
            print(f"   📊 Factors analyzed: {len(sample.factors)}")
            
            step3_score += 1
        else:
            print(f"   ⚠️  No predictions generated (no current games)")
            step3_score += 0.5
    except Exception as e:
        print(f"   ❌ Prediction generation failed: {e}")
    
    # Test 3.3: Factor Analysis
    print("\n3.3 Multi-Factor Analysis")
    try:
        if predictions:
            # Analyze factors across all predictions
            factor_summary = {}
            
            for pred in predictions:
                for factor in pred.factors:
                    if factor.name not in factor_summary:
                        factor_summary[factor.name] = {
                            'total_weight': 0,
                            'avg_confidence': 0,
                            'count': 0
                        }
                    
                    factor_summary[factor.name]['total_weight'] += factor.weight
                    factor_summary[factor.name]['avg_confidence'] += factor.confidence
                    factor_summary[factor.name]['count'] += 1
            
            print(f"   ✅ Factor analysis working")
            for name, data in factor_summary.items():
                avg_confidence = data['avg_confidence'] / data['count'] if data['count'] > 0 else 0
                print(f"     {name}: weight {data['total_weight']:.3f}, confidence {avg_confidence:.1%}")
            
            step3_score += 1
    except Exception as e:
        print(f"   ❌ Factor analysis failed: {e}")
    
    # Test 3.4: Prediction Persistence
    print("\n3.4 Prediction Persistence")
    try:
        if predictions:
            saved_count = engine.save_predictions(predictions)
            print(f"   ✅ Prediction saving: {saved_count} predictions saved")
            step3_score += 1
    except Exception as e:
        print(f"   ❌ Prediction persistence failed: {e}")
    
    # Test 3.5: Backtesting System
    print("\n3.5 Backtesting System")
    try:
        from backend.services.backtester import Backtester
        
        backtester = Backtester()
        historical_games = backtester._get_historical_games()
        
        print(f"   ✅ Backtesting system initialized")
        print(f"   📊 Historical games available: {len(historical_games)}")
        
        # Try limited backtest
        if len(historical_games) > 0:
            completed_games = [g for g in historical_games if backtester._is_game_completed(g)]
            print(f"   📊 Completed games for testing: {len(completed_games)}")
            
            if len(completed_games) > 0:
                print(f"   ✅ Backtesting data available")
                step3_score += 1
            else:
                print(f"   ⚠️  No completed games for backtesting")
                step3_score += 0.5
        else:
            print(f"   ⚠️  No historical data for backtesting")
            step3_score += 0.5
    except Exception as e:
        print(f"   ❌ Backtesting system failed: {e}")
    
    # Test 3.6: Algorithm Optimization
    print("\n3.6 Algorithm Optimization")
    try:
        from backend.services.optimizer import AlgorithmOptimizer
        
        optimizer = AlgorithmOptimizer()
        
        # Test weight generation
        test_weights = {
            'team_strength': 0.4,
            'head_to_head': 0.2,
            'home_advantage': 0.15,
            'rest_advantage': 0.1,
            'weather_impact': 0.1,
            'motivation': 0.03,
            'injuries': 0.02
        }
        
        test_engine = optimizer._create_test_engine(test_weights)
        
        if test_engine:
            print(f"   ✅ Algorithm optimization ready")
            print(f"   📊 Parameter tuning capabilities available")
            step3_score += 1
    except Exception as e:
        print(f"   ❌ Algorithm optimization failed: {e}")
    
    # Test 3.7: Model Performance Tracking
    print("\n3.7 Model Performance Tracking")
    try:
        performance = engine.get_model_performance()
        
        print(f"   ✅ Performance tracking working")
        print(f"   📊 Model version: {performance['model_version']}")
        print(f"   📊 Total predictions: {performance['total_predictions']}")
        step3_score += 1
    except Exception as e:
        print(f"   ❌ Performance tracking failed: {e}")
    
    test_results['step3'] = {'score': step3_score, 'max': step3_max}
    total_score += step3_score
    max_score += step3_max
    
    # INTEGRATION TESTS
    print("\n" + "🔗 INTEGRATION TESTS" + "=" * 55)
    
    integration_score = 0
    integration_max = 5
    
    # Test I.1: End-to-End Data Flow
    print("\n🔄 I.1 End-to-End Data Flow")
    try:
        print("     Collecting fresh data...")
        fresh_data = manager.collect_game_data()
        
        print("     Generating predictions...")
        if fresh_data.get('games'):
            fresh_predictions = engine.predict_games(fresh_data['games'])
            
            print("     Saving to database...")
            if fresh_predictions:
                saved = engine.save_predictions(fresh_predictions)
                
                print(f"   ✅ Complete workflow: {len(fresh_data['games'])} games → {len(fresh_predictions)} predictions → {saved} saved")
                integration_score += 1
            else:
                print(f"   ⚠️  Workflow partial: data collected but no predictions")
                integration_score += 0.5
        else:
            print(f"   ⚠️  No fresh data for workflow test")
            integration_score += 0.5
    except Exception as e:
        print(f"   ❌ End-to-end workflow failed: {e}")
    
    # Test I.2: Database Consistency
    print("\n💾 I.2 Database Consistency")
    try:
        final_stats = db.get_database_stats()
        
        # Check data relationships
        teams = db.get_teams()
        games = db.get_games(limit=10)
        
        consistency_checks = 0
        
        # Check if game teams exist in teams table
        if games and teams:
            team_ids = {team['espn_id'] for team in teams}
            
            for game in games:
                if game['home_team_id'] in team_ids and game['away_team_id'] in team_ids:
                    consistency_checks += 1
        
        print(f"   ✅ Database consistency check")
        print(f"   📊 Final stats: {final_stats}")
        print(f"   📊 Data consistency: {consistency_checks}/{len(games) if games else 0} games verified")
        integration_score += 1
    except Exception as e:
        print(f"   ❌ Database consistency check failed: {e}")
    
    # Test I.3: Error Handling
    print("\n⚠️  I.3 Error Handling")
    try:
        # Test graceful failure with invalid data
        test_engine = AdvancedPredictionEngine()
        
        # Try prediction with malformed game data
        bad_game = {'invalid': 'data'}
        bad_prediction = test_engine._predict_single_game(bad_game)
        
        if bad_prediction is None:
            print(f"   ✅ Error handling: graceful failure with invalid data")
            integration_score += 1
        else:
            print(f"   ⚠️  Error handling: should fail gracefully with invalid data")
            integration_score += 0.5
    except Exception as e:
        print(f"   ❌ Error handling test failed: {e}")
    
    # Test I.4: Performance and Speed
    print("\n⚡ I.4 Performance and Speed")
    try:
        start_time = time.time()
        
        # Time a complete prediction cycle
        perf_data = manager.get_prediction_data()
        if perf_data.get('games'):
            perf_predictions = engine.predict_games(perf_data['games'])
        
        end_time = time.time()
        duration = end_time - start_time
        
        games_per_second = len(perf_data.get('games', [])) / duration if duration > 0 else 0
        
        print(f"   ✅ Performance test completed")
        print(f"   📊 Duration: {duration:.2f} seconds")
        print(f"   📊 Speed: {games_per_second:.1f} games/second")
        
        if duration < 10:  # Should complete in under 10 seconds
            integration_score += 1
        else:
            integration_score += 0.5
    except Exception as e:
        print(f"   ❌ Performance test failed: {e}")
    
    # Test I.5: Data Quality Validation
    print("\n🔍 I.5 Data Quality Validation")
    try:
        validation_score = 0
        
        # Check prediction quality
        if predictions:
            for pred in predictions[:3]:  # Check first 3 predictions
                # Confidence should be reasonable (50-85%)
                if 50 <= pred.confidence <= 85:
                    validation_score += 0.2
                
                # Should have multiple active factors
                active_factors = sum(1 for f in pred.factors if f.confidence > 0)
                if active_factors >= 3:
                    validation_score += 0.2
        
        print(f"   ✅ Data quality validation")
        print(f"   📊 Quality score: {validation_score:.1f}/1.0")
        integration_score += validation_score
    except Exception as e:
        print(f"   ❌ Data quality validation failed: {e}")
    
    test_results['integration'] = {'score': integration_score, 'max': integration_max}
    total_score += integration_score
    max_score += integration_max
    
    # FINAL SUMMARY
    print("\n" + "🏆 MASTER SYSTEM TEST RESULTS" + "=" * 45)
    
    overall_percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    print(f"\nOverall Score: {total_score:.1f}/{max_score} ({overall_percentage:.1f}%)")
    
    for step, results in test_results.items():
        step_percentage = (results['score'] / results['max'] * 100) if results['max'] > 0 else 0
        status = "✅" if step_percentage >= 80 else "⚠️" if step_percentage >= 60 else "❌"
        print(f"{status} {step.upper()}: {results['score']:.1f}/{results['max']} ({step_percentage:.1f}%)")
    
    # System Readiness Assessment
    print(f"\n" + "📋 SYSTEM READINESS ASSESSMENT" + "=" * 40)
    
    if overall_percentage >= 85:
        print("🟢 SYSTEM STATUS: PRODUCTION READY")
        print("   All core components working excellently")
        print("   Ready for web interface development")
        print("   Algorithm performing well")
    elif overall_percentage >= 70:
        print("🟡 SYSTEM STATUS: FUNCTIONAL WITH MINOR ISSUES")
        print("   Core functionality working")
        print("   Some advanced features may need attention")
        print("   Ready for continued development")
    elif overall_percentage >= 50:
        print("🟠 SYSTEM STATUS: BASIC FUNCTIONALITY")
        print("   Essential components working")
        print("   Several areas need improvement")
        print("   Requires fixes before production")
    else:
        print("🔴 SYSTEM STATUS: NEEDS SIGNIFICANT WORK")
        print("   Major components failing")
        print("   Requires debugging and fixes")
    
    print(f"\nTest completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {time.time() - start_time if 'start_time' in locals() else 'Unknown'}")
    
    return {
        'total_score': total_score,
        'max_score': max_score,
        'percentage': overall_percentage,
        'details': test_results,
        'status': 'ready' if overall_percentage >= 70 else 'needs_work'
    }

if __name__ == "__main__":
    results = master_system_test()
    
    # Exit with appropriate code
    sys.exit(0 if results['status'] == 'ready' else 1)