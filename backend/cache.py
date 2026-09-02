from datetime import datetime, timedelta
import json
from typing import Dict, Optional, List

class Cache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self, duration: int = 600):
        """
        Initialize cache
        
        Args:
            duration: Cache duration in seconds (default 10 minutes)
        """
        self.cache = {}
        self.duration = duration
    
    def set(self, key: str, value: Dict) -> None:
        """Set a cache entry"""
        self.cache[key] = {
            'data': value,
            'timestamp': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=self.duration)
        }
    
    def get(self, key: str) -> Optional[Dict]:
        """Get a cache entry if it exists and hasn't expired"""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        if datetime.now() > entry['expires_at']:
            del self.cache[key]
            return None
        
        return entry['data']
    
    def delete(self, key: str) -> None:
        """Delete a cache entry"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_entries = len(self.cache)
        expired_entries = 0
        
        for key, entry in list(self.cache.items()):
            if datetime.now() > entry['expires_at']:
                expired_entries += 1
                del self.cache[key]
        
        return {
            'total_entries': total_entries - expired_entries,
            'expired_entries': expired_entries,
            'cache_duration': self.duration,
            'timestamp': datetime.now().isoformat()
        }
