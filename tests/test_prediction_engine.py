"""
Test the prediction engine
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.prediction_engine import AdvancedPredictionEngine
import json

def test_prediction_engine():
    """Test the prediction engine functionality"""
    print("Testing Advanced Prediction Engine")
    print("=" * 60)
    
    # Initialize prediction engine
    engine = AdvancedPredictionEngine()
    
    # Test 1: Generate predictions for current games
    print("\nTest 1: Generating Game Predictions")
    print("-" * 40)
    
    try:
        predictions = engine.predict_games()
        
        if predictions:
            print(f"✅ Generated {len(predictions)} predictions")
            
            # Show details for first few predictions
            for i, pred in enumerate(predictions[:3]):
                print(f"\n📊 Game {i+1}: {pred.away_team} @ {pred.home_team}")
                print(f"   Predicted Winner: {pred.predicted_winner}")
                print(f"   Confidence: {pred.confidence}%")
                print(f"   Spread: {pred.spread_prediction:+.1f}")
                print(f"   Factors analyzed: {len(pred.factors)}")
                
                # Show top factors
                print("   Key factors:")
                for factor in pred.factors:
                    if factor.confidence > 0.5:  # Only show reliable factors
                        print(f"     • {factor.name}: {factor.value:+.1f} ({factor.explanation})")
        else:
            print("⚠️  No predictions generated (might be off-season)")
    
    except Exception as e:
        print(f"❌ Prediction generation failed: {e}")
    
    # Test 2: Save predictions to database
    print("\nTest 2: Saving Predictions")
    print("-" * 40)
    
    try:
        if predictions:
            saved_count = engine.save_predictions(predictions)
            print(f"✅ Saved {saved_count} predictions to database")
        else:
            print("⚠️  No predictions to save")
    
    except Exception as e:
        print(f"❌ Prediction saving failed: {e}")
    
    # Test 3: Model performance metrics
    print("\nTest 3: Model Performance")
    print("-" * 40)
    
    try:
        performance = engine.get_model_performance()
        
        for metric, value in performance.items():
            print(f"   {metric}: {value}")
    
    except Exception as e:
        print(f"❌ Performance calculation failed: {e}")
    
    # Test 4: Factor analysis
    print("\nTest 4: Factor Analysis")
    print("-" * 40)
    
    if predictions:
        # Analyze factor importance across all predictions
        factor_summary = {}
        
        for pred in predictions:
            for factor in pred.factors:
                if factor.name not in factor_summary:
                    factor_summary[factor.name] = {
                        'total_impact': 0,
                        'count': 0,
                        'avg_confidence': 0
                    }
                
                factor_summary[factor.name]['total_impact'] += abs(factor.value)
                factor_summary[factor.name]['count'] += 1
                factor_summary[factor.name]['avg_confidence'] += factor.confidence
        
        # Calculate averages
        print("   Factor importance across all predictions:")
        for name, data in factor_summary.items():
            avg_impact = data['total_impact'] / data['count'] if data['count'] > 0 else 0
            avg_confidence = data['avg_confidence'] / data['count'] if data['count'] > 0 else 0
            
            print(f"     {name}: {avg_impact:.1f} avg impact, {avg_confidence:.1%} confidence")
    
    print("\n" + "=" * 60)
    print("Prediction Engine Test Complete")
    
    if predictions and len(predictions) > 0:
        print("✅ Ready for Step 4: Web Interface Development")
    else:
        print("⚠️  Limited predictions (check if games are available)")
    
    return predictions

if __name__ == "__main__":
    predictions = test_prediction_engine()