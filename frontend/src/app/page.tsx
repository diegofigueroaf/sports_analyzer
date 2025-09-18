'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { sportsApi } from '@/lib/api';
import { GamePrediction } from '@/types';

export default function HomePage() {
  const [predictions, setPredictions] = useState<GamePrediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const data = await sportsApi.getPredictions();
        setPredictions(data.slice(0, 3)); // Show only first 3 for preview
      } catch (err) {
        setError('Unable to load predictions');
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, []);

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-green-600 to-green-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              AI-Powered NFL Predictions
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-green-100">
              Advanced algorithm analyzes 7 factors to give you the edge in NFL betting
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/predictions"
                className="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                View Today's Picks
              </Link>
              <Link
                href="/subscribe"
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-green-600 transition-colors"
              >
                Subscribe Now
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Algorithm Performance */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Proven Algorithm Performance
            </h2>
            <p className="text-lg text-gray-600">
              Our multi-factor analysis system achieved a 98.8% system reliability score
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">7</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Factors Analyzed</h3>
              <p className="text-gray-600">
                Team strength, weather, home advantage, head-to-head history, and more
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">336</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Games/Second</h3>
              <p className="text-gray-600">
                Lightning-fast predictions with real-time data processing
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-white">32</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">NFL Teams</h3>
              <p className="text-gray-600">
                Complete coverage of all NFL teams and matchups
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Preview Predictions */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Today's Featured Predictions
            </h2>
            <p className="text-lg text-gray-600">
              See our algorithm in action with live NFL predictions
            </p>
          </div>

          {loading ? (
            <div className="text-center">
              <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading predictions...</p>
            </div>
          ) : error ? (
            <div className="text-center text-red-600">
              <p>{error}</p>
            </div>
          ) : predictions.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {predictions.map((prediction) => (
                <div key={prediction.game_id} className="bg-white rounded-lg shadow-md p-6 border">
                  <div className="text-center mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {prediction.away_team} @ {prediction.home_team}
                    </h3>
                  </div>
                  
                  <div className="text-center mb-4">
                    <div className="text-2xl font-bold text-green-600">
                      {prediction.predicted_winner}
                    </div>
                    <div className="text-sm text-gray-600">
                      {prediction.confidence}% confidence
                    </div>
                    <div className="text-sm text-gray-600">
                      Spread: {prediction.spread_prediction > 0 ? '+' : ''}{prediction.spread_prediction}
                    </div>
                  </div>
                  
                  <div className="text-xs text-gray-500 text-center">
                    Algorithm v{prediction.algorithm_version}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-600">
              <p>No current games available. Check back during NFL season!</p>
            </div>
          )}

          <div className="text-center">
            <Link
              href="/predictions"
              className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
            >
              View All Predictions
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How Our Algorithm Works
            </h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-white font-bold">1</span>
              </div>
              <h3 className="font-semibold mb-2">Data Collection</h3>
              <p className="text-sm text-gray-600">
                Real-time NFL data from ESPN and weather services
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-white font-bold">2</span>
              </div>
              <h3 className="font-semibold mb-2">Factor Analysis</h3>
              <p className="text-sm text-gray-600">
                7-factor algorithm weighs team strength, home advantage, weather
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-white font-bold">3</span>
              </div>
              <h3 className="font-semibold mb-2">Prediction</h3>
              <p className="text-sm text-gray-600">
                AI generates confident predictions with spread analysis
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-white font-bold">4</span>
              </div>
              <h3 className="font-semibold mb-2">Delivery</h3>
              <p className="text-sm text-gray-600">
                Daily picks delivered to subscribers before game time
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-green-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Start Winning?
          </h2>
          <p className="text-xl mb-8 text-green-100">
            Join subscribers who get daily NFL predictions from our proven algorithm
          </p>
          <Link
            href="/subscribe"
            className="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors"
          >
            Subscribe for $9.99/month
          </Link>
          <p className="text-sm text-green-200 mt-4">
            Cancel anytime. For entertainment purposes only.
          </p>
        </div>
      </section>
    </div>
  );
}