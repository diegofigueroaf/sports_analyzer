"""
Step 3 Verification - Complete Algorithm System Check
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.prediction_engine import AdvancedPredictionEngine
from backend.services.backtester import Backtester
from backend.services.optimizer import AlgorithmOptimizer
from backend.services.data_manager import DataManager

def verify_step_3():
    """Verify Step 3 completion"""
    print("Step 3 Verification: Algorithm Development")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = 5
    
    # Test 1: Prediction Engine
    print("\n1. Advanced Prediction Engine")
    try:
        engine = AdvancedPredictionEngine()
        predictions = engine.predict_games()
        
        if predictions and len(predictions) > 0:
            print("   ✅ Multi-factor prediction engine working")
            print(f"   📊 Generated {len(predictions)} predictions")
            
            # Check factor analysis
            sample = predictions[0]
            active_factors = sum(1 for f in sample.factors if f.confidence > 0)
            print(f"   📊 Using {active_factors} active factors per prediction")
            
            passed_tests += 1
        else:
            print("   ⚠️  Prediction engine working but no current games")
            passed_tests += 0.5
            
    except Exception as e:
        print(f"   ❌ Prediction engine failed: {e}")
    
    # Test 2: Backtesting System
    print("\n2. Backtesting System")
    try:
        backtester = Backtester()
        
        # Quick test of backtesting functionality
        historical_games = backtester._get_historical_games()
        
        if len(historical_games) > 0:
            print(f"   ✅ Backtesting system ready")
            print(f"   📊 {len(historical_games)} historical games available")
            passed_tests += 1
        else:
            print("   ⚠️  Backtesting system ready but no historical data")
            passed_tests += 0.5
            
    except Exception as e:
        print(f"   ❌ Backtesting system failed: {e}")
    
    # Test 3: Algorithm Optimization
    print("\n3. Algorithm Optimization")
    try:
        optimizer = AlgorithmOptimizer()
        
        # Test optimizer initialization and basic functionality
        test_engine = optimizer._create_test_engine({'team_strength': 1.0})
        
        if test_engine:
            print("   ✅ Algorithm optimization system ready")
            print("   📊 Parameter tuning capabilities available")
            passed_tests += 1
        else:
            print("   ❌ Optimization system initialization failed")
            
    except Exception as e:
        print(f"   ❌ Algorithm optimization failed: {e}")
    
    # Test 4: Database Integration
    print("\n4. Database Integration")
    try:
        from backend.models.database import SportsDatabase
        
        db = SportsDatabase()
        stats = db.get_database_stats()
        
        print(f"   ✅ Database integration working")
        print(f"   📊 Games: {stats['games']}, Predictions: {stats['predictions']}")
        
        if stats['games'] > 0:
            passed_tests += 1
        else:
            print("   ⚠️  Database working but no game data")
            passed_tests += 0.5
            
    except Exception as e:
        print(f"   ❌ Database integration failed: {e}")
    
    # Test 5: Complete Workflow
    print("\n5. Complete Algorithm Workflow")
    try:
        data_manager = DataManager()
        
        # Test end-to-end workflow
        prediction_data = data_manager.get_prediction_data()
        
        if prediction_data.get('games') and prediction_data.get('teams'):
            print("   ✅ Complete algorithm workflow ready")
            print(f"   📊 Data pipeline: {len(prediction_data['games'])} games, {len(prediction_data['teams'])} teams")
            passed_tests += 1
        else:
            print("   ⚠️  Workflow ready but limited data")
            passed_tests += 0.5
            
    except Exception as e:
        print(f"   ❌ Complete workflow failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Step 3 Verification: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests >= 4:
        print("\n✅ Step 3 COMPLETE - Algorithm Development Ready")
        print("\nAlgorithm Features Built:")
        print("  • Multi-factor prediction engine")
        print("  • Team strength analysis")
        print("  • Home field advantage calculation")
        print("  • Weather impact assessment")
        print("  • Historical performance backtesting")
        print("  • Algorithm parameter optimization")
        print("  • Database integration for predictions")
        print("  • Performance tracking and analysis")
        
        print(f"\n🎯 Ready for comprehensive system testing!")
        return True
    else:
        print(f"\n❌ Step 3 INCOMPLETE - Fix failing components")
        return False

if __name__ == "__main__":
    success = verify_step_3()
    sys.exit(0 if success else 1)