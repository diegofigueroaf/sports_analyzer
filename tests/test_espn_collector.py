"""
Test script for ESPN Data Collector
"""
import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.espn_collector import ESPNCollector
import json
from datetime import datetime

def test_espn_collector():
    """Test ESPN data collection"""
    print("🏈 Testing ESPN Data Collector")
    print("=" * 50)
    
    # Initialize collector
    collector = ESPNCollector()
    
    # Test 1: Collect current games
    print("\n📊 Test 1: Collecting current games...")
    games_data = collector.collect_data('games')
    
    if games_data and games_data.get('games'):
        print(f"✅ Found {len(games_data['games'])} games")
        
        # Show first game details
        if games_data['games']:
            game = games_data['games'][0]
            print(f"   Example: {game['away_team']['name']} @ {game['home_team']['name']}")
            print(f"   Status: {game['status']}")
            print(f"   Weather needed: {game['weather_needed']}")
    else:
        print("⚠️  No current games found (might be off-season)")
    
    # Test 2: Collect teams data
    print("\n📊 Test 2: Collecting teams data...")
    teams_data = collector.collect_data('teams')
    
    if teams_data and teams_data.get('teams'):
        print(f"✅ Found {len(teams_data['teams'])} teams")
        
        # Show a few teams
        for team in teams_data['teams'][:3]:
            print(f"   - {team['name']} ({team['abbreviation']})")
    else:
        print("❌ Failed to collect teams data")
    
    # Test 3: Validate data
    print("\n📊 Test 3: Validating data...")
    games_valid = collector.validate_data(games_data)
    teams_valid = collector.validate_data(teams_data)
    
    print(f"   Games data valid: {'✅' if games_valid else '❌'}")
    print(f"   Teams data valid: {'✅' if teams_valid else '❌'}")
    
    # Test 4: Check collector status
    print("\n📊 Test 4: Collector status...")
    status = collector.get_status()
    print(f"   Collector: {status['name']}")
    print(f"   Status: {status['status']}")
    print(f"   Recent requests: {status['last_request_count']}")
    
    print("\n" + "=" * 50)
    print("🎉 ESPN Collector test complete!")
    
    return {
        'games_data': games_data,
        'teams_data': teams_data,
        'games_valid': games_valid,
        'teams_valid': teams_valid
    }

if __name__ == "__main__":
    test_results = test_espn_collector()