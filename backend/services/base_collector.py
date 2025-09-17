"""
Base Data Collector
Abstract base class for all data collectors
"""
import requests
import time
import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_calls_per_minute: int = 60):
        self.max_calls = max_calls_per_minute
        self.calls = []
    
    def wait_if_needed(self):
        """Wait if we've hit the rate limit"""
        now = datetime.now()
        
        # Remove calls older than 1 minute
        self.calls = [call_time for call_time in self.calls 
                     if now - call_time < timedelta(minutes=1)]
        
        # If we're at the limit, wait
        if len(self.calls) >= self.max_calls:
            sleep_time = 60 - (now - self.calls[0]).total_seconds()
            if sleep_time > 0:
                logger.info(f"Rate limit reached, sleeping for {sleep_time:.1f} seconds")
                time.sleep(sleep_time)
        
        # Record this call
        self.calls.append(now)

class BaseDataCollector(ABC):
    """Abstract base class for all data collectors"""
    
    def __init__(self, name: str, base_url: str, rate_limit: int = 60):
        self.name = name
        self.base_url = base_url
        self.rate_limiter = RateLimiter(rate_limit)
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'GreenGuruSports/1.0 (Sports Analytics Tool)',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        })
        
        logger.info(f"Initialized {self.name} collector")
    
    def make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make rate-limited HTTP request"""
        try:
            # Apply rate limiting
            self.rate_limiter.wait_if_needed()
            
            # Make request
            url = f"{self.base_url}{endpoint}"
            logger.debug(f"Making request to: {url}")
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None
    
    def save_raw_data(self, data: Dict, filename: str):
        """Save raw data to file for debugging/backup"""
        try:
            filepath = f"data/raw/{filename}"
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.debug(f"Saved raw data to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save raw data: {e}")
    
    @abstractmethod
    def collect_data(self, **kwargs) -> Dict:
        """Abstract method - implement in subclasses"""
        pass
    
    @abstractmethod
    def validate_data(self, data: Dict) -> bool:
        """Abstract method - validate collected data"""
        pass
    
    def get_status(self) -> Dict:
        """Get collector status information"""
        return {
            'name': self.name,
            'base_url': self.base_url,
            'last_request_count': len(self.rate_limiter.calls),
            'rate_limit': self.rate_limiter.max_calls,
            'status': 'active'
        }