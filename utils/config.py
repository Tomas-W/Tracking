class Config:
    # Limiter
    LIMITER_STORAGE_URI = "memory://"
    LIMITER_DEFAULT_LIMITS = ["1800 per day", "600 per hour", "200 per minute"]
    # Cache
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    # Caching
    STATIC_CACHE_DURATION = 3600 * 24 * 7  # 7 days
    API_CACHE_DURATION = 3600  # 1 hour
    VIEW_CACHE_DURATION = 60  # 60 seconds
    # Security headers
    SECURITY_HEADERS = {
        # Prevents MIME type sniffing
        "X-Content-Type-Options": "nosniff",
        # Controls how the site can be framed - protects against clickjacking
        "X-Frame-Options": "SAMEORIGIN",
        # Enforces HTTPS - 1 year duration with subdomains
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        # Content Security Policy
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob: *; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "object-src 'none'; "
            "frame-src 'self'; "
            "worker-src 'self'; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "frame-ancestors 'self'; "
            "upgrade-insecure-requests; "
        ),
        # Controls how much referrer information is included with requests
        "Referrer-Policy": "strict-origin-when-cross-origin",
        
        # Prevents browsers from performing DNS prefetching
        "X-DNS-Prefetch-Control": "off",
        # Controls browser features - restricts potentially risky features
        "Permissions-Policy": (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        ),
        # Enables cross-origin isolation capabilities
        "Cross-Origin-Opener-Policy": "same-origin",
        "Cross-Origin-Embedder-Policy": "require-corp",
        "Cross-Origin-Resource-Policy": "same-origin"
    }


CFG = Config()
