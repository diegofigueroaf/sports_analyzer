"""
Data Collection Pipeline
Run this script to collect and save all data
"""
import sys
import os
from datetime import datetime

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.data_manager import DataManager
from backend.models.database import SportsDatabase
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_data_collection():
    """Run complete data collection pipeline"""
    print("Sports Betting Data Collection Pipeline")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize components
    manager = DataManager()
    db = SportsDatabase()
    
    total_saved = 0
    errors = []
    
    try:
        # Step 1: Collect team data
        print("\nStep 1: Collecting team data...")
        team_data = manager.collect_team_data()
        
        if team_data['teams']:
            teams_saved = db.save_teams(team_data['teams'])
            total_saved += teams_saved
            print(f"  ✅ Saved {teams_saved} teams")
        else:
            errors.append("No team data collected")
            print("  ❌ No team data collected")
        
        # Step 2: Collect game data
        print("\nStep 2: Collecting game data...")
        game_data = manager.collect_game_data(include_weather=True)
        
        if game_data['games']:
            games_saved = db.save_games(game_data['games'])
            total_saved += games_saved
            print(f"  ✅ Saved {games_saved} games")
            
            # Show weather data status
            weather_count = sum(1 for game in game_data['games'] 
                              if game.get('weather', {}).get('status') != 'not_needed')
            print(f"  📊 Weather data collected for {weather_count} games")
        else:
            errors.append("No game data collected")
            print("  ❌ No game data collected")
        
        if game_data['errors']:
            errors.extend(game_data['errors'])
        
        # Step 3: Database stats
        print("\nStep 3: Database summary...")
        stats = db.get_database_stats()
        print(f"  📊 Total games: {stats['games']}")
        print(f"  📊 Total teams: {stats['teams']}")
        print(f"  📊 Database size: {stats['database_size']} bytes")
        
    except Exception as e:
        errors.append(f"Critical error: {str(e)}")
        logger.error(f"Critical error in data collection: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Data Collection Complete")
    print(f"Total records saved: {total_saved}")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  ❌ {error}")
    
    if total_saved > 0:
        print("\n✅ Data collection successful - ready for predictions!")
    else:
        print("\n❌ No data collected - check your setup")
    
    return {
        'total_saved': total_saved,
        'errors': errors,
        'success': total_saved > 0
    }

if __name__ == "__main__":
    result = run_data_collection()
    
    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)