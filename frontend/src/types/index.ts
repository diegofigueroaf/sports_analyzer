// Types for your prediction data
export interface Team {
  id: string;
  name: string;
  abbreviation: string;
  record?: {
    wins: number;
    losses: number;
    ties: number;
  };
}

export interface PredictionFactor {
  name: string;
  value: number;
  weight: number;
  confidence: number;
  explanation: string;
}

export interface GamePrediction {
  game_id: string;
  home_team: string;
  away_team: string;
  predicted_winner: string;
  confidence: number;
  spread_prediction: number;
  total_prediction?: number;
  factors: PredictionFactor[];
  algorithm_version: string;
  created_at: string;
}

export interface Game {
  espn_id: string;
  date: string;
  status: string;
  home_team: Team;
  away_team: Team;
  weather_needed?: boolean;
  weather?: any;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}