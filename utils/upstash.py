import json
import os

from datetime import datetime
from typing import Dict, Any, List
from upstash_redis import Redis


REDIS_EXPIRATION_DURATION = 30 * 24 * 3600  # 30 days in seconds
KEEP_LAST_N_ENTRIES = 200
REQUEST_PREFIX = "requests_"
WEIGHT_PREFIX = "weight_"


class Upstash:
    """Handles all data storage operations."""
    def __init__(self):
        self.redis = None
        self.requests_memory = []
        self._init_redis()
    
    def _init_redis(self) -> None:
        """Initializes Redis client if environment variables are available."""
        redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
        redis_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
        
        if redis_url and redis_token:
            try:
                self.redis = Redis(url=redis_url, token=redis_token)
                print("Connected to Upstash Redis")
            
            except Exception as e:
                print(f"Failed to connect to Upstash Redis: {e}")
                self.redis = None
        else:
            print("No Redis credentials found, using in-memory storage")
    
    def save_request_data(self, data: Dict[str, Any], duration: bool = False) -> bool:
        """Saves data to Redis or memory fallback."""
        if self.redis:
            try:
                # Timestamp as key
                key = f"{REQUEST_PREFIX}:{datetime.now().isoformat()}"
                
                self.redis.set(key, json.dumps(data))
                if duration:
                    self.redis.expire(key, REDIS_EXPIRATION_DURATION)
                    self._cleanup_old_redis_entries(REQUEST_PREFIX)
                
                print(f"Saved data to Redis: {key}")
                return True
                
            except Exception as e:
                print(f"Error saving to Redis: {e}")
                return self._save_to_memory(data)
        else:
            self.requests_memory.append(data)
        
            if len(self.requests_memory) > KEEP_LAST_N_ENTRIES:
                self.requests_memory = self.requests_memory[KEEP_LAST_N_ENTRIES//2:]
            
            print("Saved data to memory storage")
            return True
    
    def get_request_data(self, limit: int) -> List[Dict[str, Any]]:
        """Gets data from Redis or memory fallback."""
        if self.redis:
            return self._get_from_redis(REQUEST_PREFIX, limit)
        else:
            return self._get_requests_from_memory(limit)
    
    def _get_requests_from_memory(self, limit: int) -> List[Dict[str, Any]]:
        """Get data from memory storage"""
        return self.requests_memory[-limit:] if self.requests_memory else []
    
    def save_weight_data(self, date: str, weight: float) -> bool:
        """Saves weight data to Redis."""
        if self.redis:
            try:
                key = f"{WEIGHT_PREFIX}{date}"
                self.redis.set(key, weight)
                return True
            except Exception as e:
                print(f"Error saving weight data to Redis: {e}")
                return False
        
        else:
            print("No Redis credentials found, using in-memory storage")
            return False
    
    def get_weight_data(self, date: str) -> float:
        """Gets weight data from Redis."""
        if self.redis:
            return self._get_from_redis(WEIGHT_PREFIX, None)
        else:
            return None
    
    def check_weight_data(self, date: str) -> bool:
        """Checks if weight data exists in Redis."""
        if self.redis:
            return self.redis.exists(f"{WEIGHT_PREFIX}{date}")
        else:
            return False
    
    def _get_from_redis(self, key_prefix: str, limit: int = None) -> List[Dict[str, Any]]:
        """Gets data from Redis."""
        try:
            keys = self.redis.keys(f"{key_prefix}:*")
            if keys:
                sorted_keys = sorted(keys)
                if limit:
                    sorted_keys = sorted_keys[-limit:]
                
                data_list = []
                for key in sorted_keys:
                    data = self.redis.get(key)
                    if data:
                        data_list.append(json.loads(data))
                
                return data_list
            return []
        
        except Exception as e:
            print(f"Error fetching from Redis: {e}")
            return self._get_requests_from_memory(limit)
    
    def _cleanup_old_redis_entries(self, key_prefix: str) -> None:
        """Clean up old Redis entries to prevent unlimited growth"""
        try:
            keys = self.redis.keys(f"{key_prefix}:*")
            if len(keys) > KEEP_LAST_N_ENTRIES:
                sorted_keys = sorted(keys)
                keys_to_delete = sorted_keys[:-KEEP_LAST_N_ENTRIES//2]
                for old_key in keys_to_delete:
                    self.redis.delete(old_key)
                print(f"Cleaned up {len(keys_to_delete)} old Redis entries")
        except Exception as e:
            print(f"Error during Redis cleanup: {e}")
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current storage connection status"""
        return {
            "redis_connected": self.redis is not None,
            "memory_entries": len(self.requests_memory),
            "storage_type": "redis" if self.redis else "memory"
        }


upstash = Upstash()
