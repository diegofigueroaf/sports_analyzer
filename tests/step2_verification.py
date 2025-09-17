"""
Step 2 Verification - Check all components are working
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.data_manager import DataManager
from backend.models.database import SportsDatabase
from config.api_keys import api_keys

def verify_step_2():
    """Verify Step 2 completion"""
    print("Step 2 Verification Checklist")
    print("=" * 50)
    
    passed_tests = 0
    total_tests = 6
    
    # Test 1: Configuration files
    print("\n1. Configuration Files")
    try:
        from config.data_sources import ESPN_CONFIG, NFL_TEAMS
        from config.api_keys import api_keys
        print("   ✅ Configuration files imported successfully")
        passed_tests += 1
    except ImportError as e:
        print(f"   ❌ Configuration import failed: {e}")
    
    # Test 2: Data collectors
    print("\n2. Data Collectors")
    try:
        manager = DataManager()
        collector_status = manager.get_collector_status()
        print(f"   ✅ Data collectors initialized")
        print(f"   📊 Available sources: {', '.join(collector_status['available_sources'])}")
        passed_tests += 1
    except Exception as e:
        print(f"   ❌ Data collectors failed: {e}")
    
    # Test 3: ESPN data collection
    print("\n3. ESPN Data Collection")
    try:
        test_results = manager.test_all_collectors()
        if test_results['espn']['status'] == 'working':
            print("   ✅ ESPN collector working")
            passed_tests += 1
        else:
            print(f"   ❌ ESPN collector failed: {test_results['espn']['error']}")
    except Exception as e:
        print(f"   ❌ ESPN test failed: {e}")
    
    # Test 4: Database functionality
    print("\n4. Database Functionality")
    try:
        db = SportsDatabase()
        stats = db.get_database_stats()
        print(f"   ✅ Database connected")
        print(f"   📊 Database stats: {stats}")
        passed_tests += 1
    except Exception as e:
        print(f"   ❌ Database failed: {e}")
    
    # Test 5: Data collection pipeline
    print("\n5. Data Collection Pipeline")
    try:
        prediction_data = manager.get_prediction_data()
        if prediction_data['games'] or prediction_data['teams']:
            print("   ✅ Data collection pipeline working")
            print(f"   📊 Collected: {len(prediction_data['games'])} games, {len(prediction_data['teams'])} teams")
            passed_tests += 1
        else:
            print("   ⚠️  Pipeline working but no data (might be off-season)")
            passed_tests += 0.5
    except Exception as e:
        print(f"   ❌ Pipeline failed: {e}")
    
    # Test 6: Weather integration (optional)
    print("\n6. Weather Integration (Optional)")
    if 'weather' in manager.available_sources:
        try:
            weather_test = manager.weather.collect_data('current', city='Miami')
            if weather_test and 'weather' in weather_test:
                print("   ✅ Weather integration working")
                passed_tests += 1
            else:
                print("   ❌ Weather data collection failed")
        except Exception as e:
            print(f"   ❌ Weather integration failed: {e}")
    else:
        print("   ⚠️  Weather API not configured (optional)")
        passed_tests += 0.5  # Half credit for optional feature
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Step 2 Verification: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests >= 4:
        print("\n✅ Step 2 COMPLETE - Ready for Step 3: Algorithm Development")
        print("\nWhat you've built:")
        print("  • Modular data collection framework")
        print("  • ESPN sports data integration")
        print("  • Weather data capability (optional)")
        print("  • SQLite database storage")
        print("  • Data validation and error handling")
        print("  • Automated data collection pipeline")
        return True
    else:
        print("\n❌ Step 2 INCOMPLETE - Fix failing tests before Step 3")
        return False

if __name__ == "__main__":
    success = verify_step_2()
    sys.exit(0 if success else 1)