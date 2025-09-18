import axios from 'axios';
import { GamePrediction, Game, ApiResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions to connect to your Python backend
export const sportsApi = {
  // Get current predictions
  async getPredictions(): Promise<GamePrediction[]> {
    try {
      const response = await api.get('/predictions');
      return response.data;
    } catch (error) {
      console.error('Error fetching predictions:', error);
      throw error;
    }
  },

  // Get current games
  async getGames(): Promise<Game[]> {
    try {
      const response = await api.get('/games');
      return response.data;
    } catch (error) {
      console.error('Error fetching games:', error);
      throw error;
    }
  },

  // Get algorithm performance
  async getPerformance() {
    try {
      const response = await api.get('/performance');
      return response.data;
    } catch (error) {
      console.error('Error fetching performance:', error);
      throw error;
    }
  },

  // Subscribe endpoint (will implement with Stripe later)
  async subscribe(email: string, plan: string) {
    try {
      const response = await api.post('/subscribe', { email, plan });
      return response.data;
    } catch (error) {
      console.error('Error subscribing:', error);
      throw error;
    }
  }
};