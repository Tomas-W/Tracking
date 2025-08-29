from flask import Flask
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils.logger import logger

from utils.config import CFG


limiter_: Limiter | None = None
def get_limiter(app: Flask) -> Limiter:
    global limiter_
    try:
        if limiter_ is None:
            limiter_ = Limiter(
                get_remote_address,
                app=app,
                default_limits=CFG.server.LIMITER_DEFAULT_LIMITS,
                storage_uri=CFG.server.LIMITER_STORAGE_URI,
            )
        return limiter_
    
    except Exception as e:
        logger.error(f"Failed to initialize limiter: {e}")
        raise


cache_: Cache | None = None
def get_cache() -> Cache:
    global cache_
    if cache_ is None:
        cache_ = Cache()
    return cache_
