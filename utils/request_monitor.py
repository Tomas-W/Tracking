import pytz
import requests

from dataclasses import dataclass
from datetime import datetime
from flask import request
from typing import Any, Final
from user_agents import parse

from utils.upstash import upstash
from utils.logger import logger


GEOLOCATION_API_URL: Final = "http://ip-api.com/json"
GEOLOCATION_CACHE_DURATION: Final = 3600
REQUEST_TIMEOUT: Final = 5


@dataclass
class GeolocationData:
    country: str
    country_code: str
    city: str
    region: str
    isp: str
    timezone: str

    @classmethod
    def create_local(cls) -> 'GeolocationData':
        return cls(
            country="Local Network",
            country_code="LN",
            city="Local",
            region="Local",
            isp="N/A",
            timezone="N/A"
        )

    @classmethod
    def create_unknown(cls) -> 'GeolocationData':
        return cls(
            country="Unknown",
            country_code="Unknown",
            city="Unknown",
            region="Unknown",
            isp="Unknown",
            timezone="Unknown"
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "country": self.country,
            "country_code": self.country_code,
            "city": self.city,
            "region": self.region,
            "isp": self.isp,
            "timezone": self.timezone
        }

@dataclass
class DeviceInfo:
    browser: str
    os: str
    device: str
    is_mobile: bool
    is_tablet: bool
    is_pc: bool
    is_bot: bool
    raw_user_agent: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "browser": self.browser,
            "os": self.os,
            "device": self.device,
            "is_mobile": self.is_mobile,
            "is_tablet": self.is_tablet,
            "is_pc": self.is_pc,
            "is_bot": self.is_bot,
            "raw_user_agent": self.raw_user_agent
        }

class RequestContext:
    """Manages request data collection."""
    
    def get_ip_address(self) -> str:
        """Get client IP address, handling proxy forwarding."""
        forwarded_for = request.headers.get("X-Forwarded-For")
        return forwarded_for.split(",")[0].strip() if forwarded_for else request.remote_addr
    
    def _is_local_dev(self, ip_address: str) -> bool:
        """Check if IP address is from local development environment."""
        return (ip_address == "127.0.0.1" or 
                ip_address == "localhost" or 
                ip_address.startswith(("192.168.", "10.")))
    
    def _request_geolocation(self, ip_address: str) -> dict[str, str] | None:
        """Request geolocation data from API with caching."""
        try:
            response = requests.get(
                f"{GEOLOCATION_API_URL}/{ip_address}",
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            return data if data.get("status") == "success" else None
            
        except Exception as e:
            logger.error(f"Geolocation request failed for IP {ip_address}: {e}")
            return None

    def get_geolocation(self, ip_address: str) -> GeolocationData:
        """Get geolocation data for an IP address."""
        if self._is_local_dev(ip_address):
            return GeolocationData.create_local()
        
        geolocation_data = self._request_geolocation(ip_address)
        if geolocation_data:
            return GeolocationData(
                country=geolocation_data.get("country", "Unknown"),
                country_code=geolocation_data.get("countryCode", "Unknown"),
                city=geolocation_data.get("city", "Unknown"),
                region=geolocation_data.get("regionName", "Unknown"),
                isp=geolocation_data.get("isp", "Unknown"),
                timezone=geolocation_data.get("timezone", "Unknown")
            )
        return GeolocationData.create_unknown()

    def get_device_info(self) -> DeviceInfo:
        """Get device and browser information from user agent."""
        user_agent_string = request.headers.get("User-Agent", "")
        user_agent = parse(user_agent_string)
        return DeviceInfo(
            browser=f"{user_agent.browser.family} {user_agent.browser.version_string}",
            os=f"{user_agent.os.family} {user_agent.os.version_string}",
            device=user_agent.device.family,
            is_mobile=user_agent.is_mobile,
            is_tablet=user_agent.is_tablet,
            is_pc=user_agent.is_pc,
            is_bot=user_agent.is_bot,
            raw_user_agent=user_agent_string
        )


class RequestMonitor:
    """Manages collecting and retrieving request data."""
    
    def __init__(self):
        self.context = RequestContext()
        self.storage = upstash
    
    def monitor(self) -> None:
        """Collects and saves request data."""
        try:
            request_data = self.get_request_details()
            self.storage._save_request_data(request_data)
        
        except Exception as e:
            logger.error(f"Failed to monitor request: {e}")
    
    def get_request_details(self) -> dict[str, Any]:
        """Collects request data from context."""
        ip_address = self.context.get_ip_address()
        geo_data = self.context.get_geolocation(ip_address)
        device_info = self.context.get_device_info()
        
        cet = pytz.timezone('Europe/Amsterdam')
        cet_time = datetime.now(cet)
        cet_strftime = cet_time.strftime("%Y-%m-%d @ %H:%M")
        
        return {
            "timestamp": cet_strftime,
            "ip_address": ip_address,
            "geo_data": geo_data.to_dict(),
            "device_info": device_info.to_dict(),
            "os": device_info.os,
            "route": request.endpoint.split(".")[-1],
            "method": request.method,
            "referrer": request.referrer or "Direct"
        }
    
    def get_request_data(self, limit: int | None = None) -> list[dict[str, Any]] | None:
        """Gets stored request data with optional limit."""
        try:
            data = self.storage._get_request_data()
            return data[:limit] if limit and data else data

        except Exception as e:
            logger.error(f"Failed to retrieve request data: {e}")
            return None
    
    def get_storage_status(self) -> dict[str, Any]:
        """Gets current storage connection status."""
        try:
            return self.storage.get_connection_status()
        
        except Exception as e:
            logger.error(f"Failed to get storage status: {e}")
            return {"status": "error", "message": str(e)}


request_monitor = RequestMonitor()
