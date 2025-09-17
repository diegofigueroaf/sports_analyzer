"""
Test Data Manager and all collectors
"""
import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.data_manager import DataManager
import json
from datetime import datetime

def test_data_manager():
    """Test the complete data collection system"""
    print("Testing Data Collection System")
    print("=" * 60)
    
    # Initialize data manager
    manager = DataManager()
    
    # Test 1: Check collector status
    print("\nTest 1: Collector Status")
    print("-" * 30)
    status = manager.get_collector_status()
    
    for collector_name, collector_status in status.items():
        if isinstance(collector_status, dict) and 'status' in collector_status:
            print(f"  {collector_name}: {collector_status['status']}")
        else:
            print(f"  {collector_name}: {collector_status}")
    
    # Test 2: Test all collectors
    print("\nTest 2: Testing All Collectors")
    print("-" * 30)
    test_results = manager.test_all_collectors()
    
    for collector, result in test_results.items():
        status_icon = "✅" if result['status'] == 'working' else "⚠️" if result['status'] == 'not_configured' else "❌"
        print(f"  {status_icon} {collector}: {result['status']}")
        if result['error']:
            print(f"      Error: {result['error']}")
    
    # Test 3: Collect game data
    print("\nTest 3: Collecting Game Data")
    print("-" * 30)
    try:
        game_data = manager.collect_game_data(include_weather=False)  # Start without weather
        
        if game_data['games']:
            print(f"  ✅ Collected {len(game_data['games'])} games")
            
            # Show first game
            game = game_data['games'][0]
            print(f"  📊 Sample: {game['away_team']['name']} @ {game['home_team']['name']}")
            print(f"      Status: {game['status']}")
            print(f"      Weather needed: {game.get('weather_needed', 'unknown')}")
        else:
            print("  ⚠️  No games found (might be off-season)")
        
        if game_data['errors']:
            print(f"  ❌ Errors: {len(game_data['errors'])}")
            for error in game_data['errors']:
                print(f"      - {error}")
    
    except Exception as e:
        print(f"  ❌ Game data collection failed: {e}")
    
    # Test 4: Collect team data
    print("\nTest 4: Collecting Team Data")
    print("-" * 30)
    try:
        team_data = manager.collect_team_data()
        
        if team_data['teams']:
            print(f"  ✅ Collected {len(team_data['teams'])} teams")
            
            # Show a few teams
            for team in team_data['teams'][:3]:
                print(f"      - {team['name']} ({team['abbreviation']})")
        else:
            print("  ❌ No teams found")
    
    except Exception as e:
        print(f"  ❌ Team data collection failed: {e}")
    
    # Test 5: Get prediction data
    print("\nTest 5: Getting Prediction Data")
    print("-" * 30)
    try:
        prediction_data = manager.get_prediction_data()
        
        print(f"  📊 Games for prediction: {len(prediction_data['games'])}")
        print(f"  📊 Teams available: {len(prediction_data['teams'])}")
        print(f"  📊 Data sources: {', '.join(prediction_data['available_sources'])}")
        
        if prediction_data['errors']:
            print(f"  ⚠️  Errors: {len(prediction_data['errors'])}")
    
    except Exception as e:
        print(f"  ❌ Prediction data collection failed: {e}")
    
    print("\n" + "=" * 60)
    print("Data Collection System Test Complete")
    
    # Summary
    working_collectors = sum(1 for result in test_results.values() if result['status'] == 'working')
    total_collectors = len(test_results)
    
    print(f"Working collectors: {working_collectors}/{total_collectors}")
    
    if working_collectors > 0:
        print("✅ Ready for Step 3: Algorithm Development")
    else:
        print("❌ Fix data collection issues before proceeding")

if __name__ == "__main__":
    test_data_manager()