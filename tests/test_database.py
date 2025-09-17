"""
Test database integration
"""
import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.models.database import SportsDatabase
from backend.services.data_manager import DataManager

def test_database():
    """Test database functionality"""
    print("Testing Database Integration")
    print("=" * 50)
    
    # Initialize database
    db = SportsDatabase()
    manager = DataManager()
    
    # Test 1: Database initialization
    print("\nTest 1: Database Status")
    print("-" * 25)
    stats = db.get_database_stats()
    print(f"  Games: {stats['games']}")
    print(f"  Teams: {stats['teams']}")
    print(f"  Predictions: {stats['predictions']}")
    print(f"  Database size: {stats['database_size']} bytes")
    
    # Test 2: Collect and save data
    print("\nTest 2: Collecting and Saving Data")
    print("-" * 25)
    
    try:
        # Collect team data
        print("  Collecting teams...")
        team_data = manager.collect_team_data()
        
        if team_data['teams']:
            teams_saved = db.save_teams(team_data['teams'])
            print(f"  ✅ Saved {teams_saved} teams")
        
        # Collect game data
        print("  Collecting games...")
        game_data = manager.collect_game_data(include_weather=False)
        
        if game_data['games']:
            games_saved = db.save_games(game_data['games'])
            print(f"  ✅ Saved {games_saved} games")
        else:
            print("  ⚠️  No games to save")
        
    except Exception as e:
        print(f"  ❌ Error collecting/saving data: {e}")
    
    # Test 3: Retrieve data
    print("\nTest 3: Retrieving Data")
    print("-" * 25)
    
    try:
        # Get teams
        teams = db.get_teams()
        print(f"  Teams in database: {len(teams)}")
        
        if teams:
            for team in teams[:3]:
                print(f"    - {team['name']} ({team['abbreviation']})")
        
        # Get games
        games = db.get_games(limit=5)
        print(f"  Games in database: {len(games)}")
        
        if games:
            for game in games[:3]:
                print(f"    - {game['away_team_name']} @ {game['home_team_name']} ({game['status']})")
    
    except Exception as e:
        print(f"  ❌ Error retrieving data: {e}")
    
    # Test 4: Updated stats
    print("\nTest 4: Final Database Stats")
    print("-" * 25)
    final_stats = db.get_database_stats()
    print(f"  Games: {final_stats['games']}")
    print(f"  Teams: {final_stats['teams']}")
    print(f"  Predictions: {final_stats['predictions']}")
    print(f"  Database size: {final_stats['database_size']} bytes")
    
    print("\n" + "=" * 50)
    print("Database Test Complete")
    
    if final_stats['teams'] > 0:
        print("✅ Database ready for Step 3: Algorithm Development")
    else:
        print("❌ No data in database - check data collection")

if __name__ == "__main__":
    test_database()