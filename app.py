import os

from enum import Enum
from flask import (
    Flask, 
)
from typing import Final

from routes.landing.landing_route import landing_bp
from routes.home.home_routes import home_bp
from routes.admin.admin_routes import admin_bp

from utils.config import CFG


DEFAULT_CACHE_DURATION: Final = 60
STATIC_CACHE_DURATION: Final = CFG.server.STATIC_CACHE_DURATION
API_CACHE_DURATION: Final = CFG.server.API_CACHE_DURATION


def get_app() -> Flask:
    """Initializes the Flask app."""
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

    # _init_limiter(app)
    _init_security_headers(app)
    # _init_cache(app)
    _init_session(app)
    _init_blueprints(app)
    return app


# def _init_limiter(app: Flask) -> None:
#     limiter = get_limiter(app)
#     # Use Redis storage for rate limiting
#     storage_uri = os.environ.get("UPSTASH_REDIS_REST_URL", "memory://")
#     app.config["RATELIMIT_STORAGE_URI"] = storage_uri
#     limiter.init_app(app)


def _init_security_headers(app: Flask) -> None:
    app.config["SECURITY_HEADERS"] = CFG.server.SECURITY_HEADERS
    @app.after_request
    def add_security_headers(response):
        for header, value in app.config["SECURITY_HEADERS"].items():
            response.headers[header] = value
        return response


# def _init_cache(app) -> None:
#     cache = get_cache()
#     cache_config = {
#         "CACHE_TYPE": "RedisCache" if os.environ.get("UPSTASH_REDIS_REST_URL") else "NullCache",
#         "CACHE_REDIS_URL": os.environ.get("UPSTASH_REDIS_REST_URL"),
#         "CACHE_DEFAULT_TIMEOUT": CFG.server.CACHE_DEFAULT_TIMEOUT
#     }
#     cache.init_app(app, config=cache_config)

#     @app.after_request
#     def add_cache_control_headers(response: Response) -> Response:
#         content_type = response.headers.get("Content-Type", "")

#         def set_cache_headers(max_age: int, public: bool = True) -> None:
#             response.cache_control.public = public
#             response.cache_control.max_age = max_age
#             response.expires = max_age

#         # Static assets (js, images, fonts)
#         if any(typ in content_type for typ in ContentType.STATIC.value):
#             set_cache_headers(STATIC_CACHE_DURATION)
            
#             # Debug headers for images
#             if "image/" in content_type:
#                 response.headers["X-Cache-Debug"] = f"max-age={STATIC_CACHE_DURATION}"
        
#         # HTML and CSS
#         elif any(typ in content_type for typ in ContentType.DOCUMENT.value):
#             if os.environ.get("FLASK_ENV") != "deploy":
#                 set_cache_headers(STATIC_CACHE_DURATION)
#             else:
#                 response.cache_control.no_store = True
#                 response.cache_control.no_cache = True
#                 set_cache_headers(0, public=False)
        
#         # API responses
#         elif any(typ in content_type for typ in ContentType.API.value):
#             set_cache_headers(API_CACHE_DURATION)
        
#         # Other content types
#         else:
#             set_cache_headers(DEFAULT_CACHE_DURATION)
        
#         return response


def _init_session(app: Flask) -> None:
    app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))
    
    is_production = os.environ.get("DEBUG") == "False"
    
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=is_production,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=2592000,
        SESSION_COOKIE_NAME='tracker_session',
        SESSION_COOKIE_PATH='/',
        SESSION_PROTECTION='strong',
        SESSION_REFRESH_EACH_REQUEST=False
    )

def _init_blueprints(app):
    app.register_blueprint(landing_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)


class ContentType(Enum):
    """Content types with their cache settings"""
    STATIC = ["application/javascript", "image/", "font/"]
    DOCUMENT = ["text/html", "text/css"]
    API = ["application/json", "application/xml"]
