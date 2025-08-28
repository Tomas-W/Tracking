import os

from flask import (
    Flask, 
    request,
)
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils.config import CFG


cache = Cache()

def get_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))
    configure_app(app)
    return app


def configure_app(app):
    limiter_ = Limiter(
        get_remote_address,
        app=app,
        default_limits=CFG.LIMITER_DEFAULT_LIMITS,
        storage_uri=CFG.LIMITER_STORAGE_URI,
    )
    
    # Configure cache
    cache_config = {
        "CACHE_TYPE": CFG.CACHE_TYPE,
        "CACHE_DEFAULT_TIMEOUT": CFG.CACHE_DEFAULT_TIMEOUT
    }
    cache.init_app(app, config=cache_config)
    
    # Configure security headers
    app.config["SECURITY_HEADERS"] = CFG.SECURITY_HEADERS
    
    # Add after request handlers for headers
    @app.after_request
    def add_security_headers(response):
        for header, value in app.config["SECURITY_HEADERS"].items():
            response.headers[header] = value
        return response
    
    @app.after_request
    def add_cache_control_headers(response):
        content_type = response.headers.get("Content-Type", "")
        path = request.path

        # Static assets that can be cached aggressively
        if "application/javascript" in content_type or "image/" in content_type or "font/" in content_type:
            response.cache_control.public = True
            response.cache_control.max_age = CFG.STATIC_CACHE_DURATION
            response.expires = CFG.STATIC_CACHE_DURATION
            
            # Add debugging headers for images
            if "image/" in content_type:
                response.headers["X-Cache-Debug"] = f"max-age={CFG.STATIC_CACHE_DURATION}"
        
        # HTML and CSS - disable caching
        elif "text/html" in content_type or "text/css" in content_type:
            response.cache_control.no_store = True
            response.cache_control.no_cache = True
            response.cache_control.max_age = 0
            response.expires = 0
        
        # HTML and CSS - enable caching
        # elif "text/html" in content_type or "text/css" in content_type:
        #     if os.environ.get("FLASK_ENV") != "deploy":
        #         response.cache_control.public = True
        #         response.cache_control.max_age = CFG.STATIC_CACHE_DURATION
        #         response.expires = CFG.STATIC_CACHE_DURATION
        #     else:
        #         response.cache_control.no_store = True
        #         response.cache_control.no_cache = True
        #         response.cache_control.max_age = 0
        #         response.expires = 0
        
        # API responses (JSON, XML) - moderate caching
        elif "application/json" in content_type or "application/xml" in content_type:
            response.cache_control.public = True
            response.cache_control.max_age = CFG.API_CACHE_DURATION
            response.expires = CFG.API_CACHE_DURATION
        
        # Default for all other content types - minimal caching
        else:
            response.cache_control.public = True
            response.cache_control.max_age = 60  # 1 minute
            response.expires = 60
        
        return response
