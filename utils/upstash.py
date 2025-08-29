import json
import os

from datetime import datetime
from typing import Any, Final
from upstash_redis import Redis

from utils.logger import logger


REDIS_EXPIRATION_DURATION: Final = 30 * 24 * 3600  # 30 days in seconds
KEEP_LAST_N_ENTRIES: Final = 200
MAX_REQUEST_ITEMS: Final = 100
REQUEST_PREFIX: Final = "requests_"
USERS_PREFIX: Final = "users_"


class Upstash:
    """Handles all data storage operations."""
    def __init__(self):
        self.redis: Redis = None
        self.requests_memory: list[dict[str, Any]] = []
        self.users_memory: dict[str, dict[str, str]] = {}
        self._init_redis()
        if self.redis is None:
            self.users_memory = {"test": "test"}
    
    def _init_redis(self) -> None:
        """Initializes Redis client if environment variables are available."""
        redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
        redis_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
        
        if redis_url and redis_token:
            try:
                self.redis = Redis(url=redis_url, token=redis_token)
                logger.info("Connected to Upstash Redis")
            
            except Exception as e:
                logger.error(f"Failed to connect to Upstash Redis: {e}")
                self.redis = None
        else:
            logger.info("No Redis credentials found, using in-memory storage")
    
    def _save_request_data(self, data: dict[str, Any]) -> None:
        """Saves data to Redis or memory fallback."""
        if self.redis:
            self._save_request_data_to_redis(data)
        else:
            self._save_request_data_to_memory(data)
    
    def _get_request_data(self, limit: int = MAX_REQUEST_ITEMS) -> list[dict[str, Any]] | None:
        """Gets data from Redis or memory fallback."""
        if self.redis:
            return self._get_requests_from_redis(REQUEST_PREFIX, limit)
        else:
            return self._get_requests_from_memory(limit)
    
    def add_user(self, username: str, password: str) -> None:
        """Adds user to Redis or memory fallback"""
        if self.redis:
            self._add_user_to_redis(username, password)
        else:
            self._add_user_to_memory(username, password)
    
    def get_user(self, username: str) -> str | None:
        """Gets user from Redis or memory fallback"""
        if self.redis:
            return self._get_user_from_redis(username)
        else:
            return self._get_user_from_memory(username)
    
    def _save_request_data_to_redis(self, data: dict[str, Any]) -> None:
        """Saves data to Redis."""
        try:
            key = f"{REQUEST_PREFIX}:{datetime.now().isoformat()}"
            self.redis.set(key, json.dumps(data))
            # self.redis.expire(key, REDIS_EXPIRATION_DURATION)
            self._cleanup_old_redis_entries(REQUEST_PREFIX)

        except Exception as e:
            logger.error(f"Error saving to Redis: {e}")
            self.requests_memory.append(data)
    
    def _save_request_data_to_memory(self, data: dict[str, Any]) -> None:
        """Saves data to memory storage."""
        self.requests_memory.append(data)
        if len(self.requests_memory) > KEEP_LAST_N_ENTRIES:
            self.requests_memory = self.requests_memory[KEEP_LAST_N_ENTRIES//2:]
    
    def _get_requests_from_redis(self, key_prefix: str, limit: int = None) -> list[dict[str, Any]] | None:
        """Gets data from Redis, sorted by timestamp."""
        try:
            # Get all keys
            keys = self.redis.keys(f"{key_prefix}:*")
            if not keys:
                return None
            
            # Sort keys
            sorted_keys = sorted(keys)
            if limit:
                sorted_keys = sorted_keys[:limit]
            
            # Get all values
            values = self.redis.mget(*sorted_keys)
            # Process results
            data_list = []
            for value in values:
                if value:
                    data_list.append(json.loads(value))
            
            return data_list
        
        except Exception as e:
            logger.error(f"Error fetching from Redis: {e}")
            return self._get_requests_from_memory(limit)
    
    def _get_requests_from_memory(self, limit: int) -> list[dict[str, Any]] | None:
        """Gets data from memory storage"""
        if not self.requests_memory:
            return None
        # Reverse the slice to get newest first
        memory_data = list(reversed(self.requests_memory))
        return memory_data[:limit] if limit else memory_data
    
    def _get_user_from_redis(self, username: str) -> str | None:
        """Gets user from Redis"""
        try:
            result = self.redis.get(f"{USERS_PREFIX}{username}")
            return result
        
        except Exception as e:
            logger.error(f"Error fetching user from Redis: {e}")
            return self._get_user_from_memory(username)
    
    def _get_user_from_memory(self, username: str) -> str | None:
        """Gets users from memory storage"""
        try:
            return self.users_memory[username]
        
        except Exception as e:
            logger.error(f"Error fetching user from memory: {e}")
            return None
    
    def _add_user_to_redis(self, username: str, password: str) -> None:
        """Adds user to Redis"""
        try:
            self.redis.set(f"{USERS_PREFIX}{username}", password)
        
        except Exception as e:
            logger.error(f"Error adding user to Redis: {e}")
            self._add_user_to_memory(username, password)
    
    def _add_user_to_memory(self, username: str, password: str) -> None:
        """Adds user to memory storage"""
        self.users_memory[username] = password
    
    def _cleanup_old_redis_entries(self, key_prefix: str) -> None:
        """Cleans up old Redis entries"""
        try:
            keys = self.redis.keys(f"{key_prefix}:*")
            if len(keys) > KEEP_LAST_N_ENTRIES:
                sorted_keys = sorted(keys)
                keys_to_delete = sorted_keys[:-KEEP_LAST_N_ENTRIES//2]
                removed_keys = self.redis.delete(*keys_to_delete)
                logger.info(f"Cleaned up {removed_keys} old Redis entries")
        
        except Exception as e:
            logger.error(f"Error during Redis cleanup: {e}")
    
    def get_connection_status(self) -> dict[str, Any]:
        """Gets current storage connection status"""
        return {
            "redis_connected": self.redis is not None,
            "memory_entries": len(self.requests_memory),
            "storage_type": "redis" if self.redis else "memory"
        }


upstash = Upstash()
