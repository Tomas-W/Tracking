from dataclasses import dataclass


@dataclass
class Server:
    # Limiter
    LIMITER_STORAGE_URI: str = "memory://"
    LIMITER_DEFAULT_LIMITS: list[str] = None
    # Cache
    CACHE_TYPE: str = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT: int = 300
    STATIC_CACHE_DURATION = 3600 * 24 * 7
    API_CACHE_DURATION = 3600
    # Security headers
    SECURITY_HEADERS: dict[str, str] = None

    def __post_init__(self):
        if self.LIMITER_DEFAULT_LIMITS is None:
            self.LIMITER_DEFAULT_LIMITS = ["300 per day", "100 per hour", "20 per minute"]
        
        if self.SECURITY_HEADERS is None:
            self.SECURITY_HEADERS = {
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


@dataclass
class Routes:
    landing: str = "/"
    home: str = "/home"
    weight: str = "/weight"
    calories: str = "/calories"
    requests: str = "/admin/requests"
    add_user: str = "/admin/add-user"


@dataclass
class Templates:
    landing: str = "landing/landing.html"
    home: str = "home/home.html"
    graph: str = "home/graph.html"
    weight: str = "home/weight.html"
    calories: str = "home/calories.html"
    requests: str = "admin/requests.html"
    add_user: str = "admin/add_user.html"


@dataclass
class Redirects:
    landing: str = "landing.landing"
    home: str = "home.home"
    weight: str = "home.weight"
    calories: str = "home.calories"
    requests: str = "admin.requests"
    add_user: str = "admin.add_user"


@dataclass
class Config:
    server: Server = None
    route: Routes = None
    template: Templates = None
    redirect: Redirects = None

    def __post_init__(self):
        if self.server is None:
            self.server = Server()
        if self.route is None:
            self.route = Routes()
        if self.template is None:
            self.template = Templates()
        if self.redirect is None:
            self.redirect = Redirects()


CFG = Config()
