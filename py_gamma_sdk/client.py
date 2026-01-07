import httpx
import logging
from typing import List, Optional, Any, Dict, Union
from urllib.parse import urlparse

from .constants import BASE_URL, DEFAULT_TIMEOUT
from .exceptions import GammaError, GammaAPIError, NotFoundError, ValidationError
from .models import Market, Event, Tag, Team, SportMetadata, Series, Comment, Profile

logger = logging.getLogger(__name__)

# ==========================================
# Synchronous Client Implementation
# ==========================================

class BaseSyncSubClient:
    def __init__(self, client: 'GammaClient'):
        self._client = client

class SportsClient(BaseSyncSubClient):
    """Client for fetching sports-related metadata and team information."""
    
    def list_teams(self, **params) -> List[Team]:
        """
        List sports teams.
        
        :param params: Optional query parameters (e.g., league, name, limit).
        :return: A list of Team objects.
        """
        data = self._client._request("GET", "/teams", params=params)
        return [Team(**item) for item in data]

    def get_metadata(self) -> List[SportMetadata]:
        """
        Get metadata for all available sports.
        
        :return: A list of SportMetadata objects.
        """
        data = self._client._request("GET", "/sports")
        return [SportMetadata(**item) for item in data]

    def get_market_types(self) -> List[str]:
        """
        Get valid sports market types.
        
        :return: A list of strings representing market types.
        """
        data = self._client._request("GET", "/sports/market-types")
        return data.get("marketTypes", [])

class TagsClient(BaseSyncSubClient):
    """Client for managing and discovering tags."""
    
    def list(self, **params) -> List[Tag]:
        """List all available tags."""
        data = self._client._request("GET", "/tags", params=params)
        return [Tag(**item) for item in data]

    def get_by_id(self, tag_id: str) -> Tag:
        """Get a specific tag by its unique ID."""
        data = self._client._request("GET", f"/tags/{tag_id}")
        return Tag(**data)

    def get_by_slug(self, slug: str) -> Tag:
        """Get a specific tag by its URL slug."""
        data = self._client._request("GET", f"/tags/slug/{slug}")
        return Tag(**data)

    def get_related_by_id(self, tag_id: str) -> List[Dict]:
        return self._client._request("GET", f"/tags-related-tag-id/{tag_id}")

    def get_related_by_slug(self, slug: str) -> List[Dict]:
        return self._client._request("GET", f"/tags-related-tag-slug/{slug}")

    def get_tags_related_to_id(self, tag_id: str) -> List[Tag]:
        data = self._client._request("GET", f"/tags/{tag_id}/related")
        return [Tag(**item) for item in data]

    def get_tags_related_to_slug(self, slug: str) -> List[Tag]:
        data = self._client._request("GET", f"/tags/slug/{slug}/related")
        return [Tag(**item) for item in data]

class EventsClient(BaseSyncSubClient):
    """Client for discovering events (groups of markets)."""
    
    def list(self, **params) -> List[Event]:
        """List events based on provided filters."""
        data = self._client._request("GET", "/events", params=params)
        return [Event(**item) for item in data]

    def get_by_id(self, event_id: str) -> Event:
        """Get a specific event by ID."""
        data = self._client._request("GET", f"/events/{event_id}")
        return Event(**data)

    def get_tags(self, event_id: str) -> List[Tag]:
        """Get tags associated with an event."""
        data = self._client._request("GET", f"/events/{event_id}/tags")
        return [Tag(**item) for item in data]

    def get_by_slug(self, slug: str) -> Event:
        """Get an event by its unique slug."""
        data = self._client._request("GET", f"/events/slug/{slug}")
        return Event(**data)

class MarketsClient(BaseSyncSubClient):
    """Client for accessing Polymarket market data."""
    
    def list(self, **params) -> List[Market]:
        """
        List markets with extensive filtering options.
        
        :param params: Filters like active, tag_id, slug, limit, offset, etc.
        """
        data = self._client._request("GET", "/markets", params=params)
        return [Market(**item) for item in data]

    def get_by_id(self, market_id: str) -> Market:
        """Get a specific market by its ID."""
        data = self._client._request("GET", f"/markets/{market_id}")
        return Market(**data)

    def get_tags(self, market_id: str) -> List[Tag]:
        """Get tags associated with a specific market."""
        data = self._client._request("GET", f"/markets/{market_id}/tags")
        return [Tag(**item) for item in data]

    def get_by_slug(self, slug: str) -> Market:
        """Get a market by its unique slug."""
        data = self._client._request("GET", f"/markets/slug/{slug}")
        if isinstance(data, list):
            return Market(**data[0]) if data else None
        return Market(**data)

class SeriesClient(BaseSyncSubClient):
    def list(self, **params) -> List[Series]:
        data = self._client._request("GET", "/series", params=params)
        return [Series(**item) for item in data]

    def get_by_id(self, series_id: str) -> Series:
        data = self._client._request("GET", f"/series/{series_id}")
        return Series(**data)

class CommentsClient(BaseSyncSubClient):
    def list(self, **params) -> List[Comment]:
        data = self._client._request("GET", "/comments", params=params)
        return [Comment(**item) for item in data]

    def get_by_id(self, comment_id: str) -> Comment:
        data = self._client._request("GET", f"/comments/{comment_id}")
        return Comment(**data)

    def get_by_user(self, address: str) -> List[Comment]:
        data = self._client._request("GET", f"/comments/user/{address}")
        return [Comment(**item) for item in data]

class ProfilesClient(BaseSyncSubClient):
    def get_by_address(self, address: str) -> Profile:
        data = self._client._request("GET", f"/profiles/{address}")
        return Profile(**data)

class GammaClient:
    """
    Main entry point for the Polymarket Gamma API SDK (Synchronous).
    
    Usage:
        client = GammaClient()
        try:
            status = client.get_status()
            markets = client.markets.list(active=True)
        finally:
            client.close()
            
    Context Manager:
        with GammaClient() as client:
            ...
    """
    def __init__(self, base_url: str = BASE_URL, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._http_client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

        self.sports = SportsClient(self)
        self.tags = TagsClient(self)
        self.events = EventsClient(self)
        self.markets = MarketsClient(self)
        self.series = SeriesClient(self)
        self.comments = CommentsClient(self)
        self.profiles = ProfilesClient(self)

    def close(self):
        """Close the underlying HTTPX client."""
        self._http_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        try:
            response = self._http_client.request(method, endpoint, **kwargs)
            if response.status_code == 404:
                raise NotFoundError(f"Resource not found: {endpoint}", status_code=404)
            response.raise_for_status()
            
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                return response.text.strip('"')
        except httpx.HTTPStatusError as e:
            raise GammaAPIError(f"API Error: {e}", status_code=e.response.status_code, response_text=e.response.text)
        except GammaError:
            raise
        except Exception as e:
            raise GammaAPIError(f"Unexpected Error: {e}")

    def get_status(self) -> str:
        return self._request("GET", "/status")

    def search(self, query: str, **params) -> Dict[str, Any]:
        params["q"] = query
        return self._request("GET", "/search", params=params)

    def resolve_url(self, url: str) -> Union[Market, Event, None]:
        """
        Resolve a Polymarket URL to a Market or Event object.
        """
        slug = self._extract_slug_from_url(url)
        if not slug:
            raise ValidationError(f"Invalid Polymarket URL: {url}")

        # Try market first
        try:
            return self.markets.get_by_slug(slug)
        except Exception:
            pass

        # Try event next
        try:
            return self.events.get_by_slug(slug)
        except Exception:
            pass

        return None

    def _extract_slug_from_url(self, url: str) -> Optional[str]:
        try:
            parsed = urlparse(url)
            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) >= 2 and path_parts[0] in ["market", "event"]:
                return path_parts[-1]
            return None
        except Exception:
            return None

# ==========================================
# Asynchronous Client Implementation
# ==========================================

class BaseAsyncSubClient:
    def __init__(self, client: 'AsyncGammaClient'):
        self._client = client

class AsyncSportsClient(BaseAsyncSubClient):
    """Client for fetching sports-related metadata and team information."""
    
    async def list_teams(self, **params) -> List[Team]:
        data = await self._client._request("GET", "/teams", params=params)
        return [Team(**item) for item in data]

    async def get_metadata(self) -> List[SportMetadata]:
        data = await self._client._request("GET", "/sports")
        return [SportMetadata(**item) for item in data]

    async def get_market_types(self) -> List[str]:
        data = await self._client._request("GET", "/sports/market-types")
        return data.get("marketTypes", [])

class AsyncTagsClient(BaseAsyncSubClient):
    """Client for managing and discovering tags."""
    
    async def list(self, **params) -> List[Tag]:
        data = await self._client._request("GET", "/tags", params=params)
        return [Tag(**item) for item in data]

    async def get_by_id(self, tag_id: str) -> Tag:
        data = await self._client._request("GET", f"/tags/{tag_id}")
        return Tag(**data)

    async def get_by_slug(self, slug: str) -> Tag:
        data = await self._client._request("GET", f"/tags/slug/{slug}")
        return Tag(**data)

    async def get_related_by_id(self, tag_id: str) -> List[Dict]:
        return await self._client._request("GET", f"/tags-related-tag-id/{tag_id}")

    async def get_related_by_slug(self, slug: str) -> List[Dict]:
        return await self._client._request("GET", f"/tags-related-tag-slug/{slug}")

    async def get_tags_related_to_id(self, tag_id: str) -> List[Tag]:
        data = await self._client._request("GET", f"/tags/{tag_id}/related")
        return [Tag(**item) for item in data]

    async def get_tags_related_to_slug(self, slug: str) -> List[Tag]:
        data = await self._client._request("GET", f"/tags/slug/{slug}/related")
        return [Tag(**item) for item in data]

class AsyncEventsClient(BaseAsyncSubClient):
    """Client for discovering events (groups of markets)."""
    
    async def list(self, **params) -> List[Event]:
        data = await self._client._request("GET", "/events", params=params)
        return [Event(**item) for item in data]

    async def get_by_id(self, event_id: str) -> Event:
        data = await self._client._request("GET", f"/events/{event_id}")
        return Event(**data)

    async def get_tags(self, event_id: str) -> List[Tag]:
        data = await self._client._request("GET", f"/events/{event_id}/tags")
        return [Tag(**item) for item in data]

    async def get_by_slug(self, slug: str) -> Event:
        data = await self._client._request("GET", f"/events/slug/{slug}")
        return Event(**data)

class AsyncMarketsClient(BaseAsyncSubClient):
    """Client for accessing Polymarket market data."""
    
    async def list(self, **params) -> List[Market]:
        data = await self._client._request("GET", "/markets", params=params)
        return [Market(**item) for item in data]

    async def get_by_id(self, market_id: str) -> Market:
        data = await self._client._request("GET", f"/markets/{market_id}")
        return Market(**data)

    async def get_tags(self, market_id: str) -> List[Tag]:
        data = await self._client._request("GET", f"/markets/{market_id}/tags")
        return [Tag(**item) for item in data]

    async def get_by_slug(self, slug: str) -> Market:
        data = await self._client._request("GET", f"/markets/slug/{slug}")
        if isinstance(data, list):
            return Market(**data[0]) if data else None
        return Market(**data)

class AsyncSeriesClient(BaseAsyncSubClient):
    async def list(self, **params) -> List[Series]:
        data = await self._client._request("GET", "/series", params=params)
        return [Series(**item) for item in data]

    async def get_by_id(self, series_id: str) -> Series:
        data = await self._client._request("GET", f"/series/{series_id}")
        return Series(**data)

class AsyncCommentsClient(BaseAsyncSubClient):
    async def list(self, **params) -> List[Comment]:
        data = await self._client._request("GET", "/comments", params=params)
        return [Comment(**item) for item in data]

    async def get_by_id(self, comment_id: str) -> Comment:
        data = await self._client._request("GET", f"/comments/{comment_id}")
        return Comment(**data)

    async def get_by_user(self, address: str) -> List[Comment]:
        data = await self._client._request("GET", f"/comments/user/{address}")
        return [Comment(**item) for item in data]

class AsyncProfilesClient(BaseAsyncSubClient):
    async def get_by_address(self, address: str) -> Profile:
        data = await self._client._request("GET", f"/profiles/{address}")
        return Profile(**data)

class AsyncGammaClient:
    """
    Main entry point for the Polymarket Gamma API SDK (Asynchronous).
    
    Usage:
        async with AsyncGammaClient() as client:
            status = await client.get_status()
            markets = await client.markets.list(active=True)
    """
    def __init__(self, base_url: str = BASE_URL, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._http_client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

        self.sports = AsyncSportsClient(self)
        self.tags = AsyncTagsClient(self)
        self.events = AsyncEventsClient(self)
        self.markets = AsyncMarketsClient(self)
        self.series = AsyncSeriesClient(self)
        self.comments = AsyncCommentsClient(self)
        self.profiles = AsyncProfilesClient(self)

    async def close(self):
        """Close the underlying HTTPX client."""
        await self._http_client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        try:
            response = await self._http_client.request(method, endpoint, **kwargs)
            if response.status_code == 404:
                raise NotFoundError(f"Resource not found: {endpoint}", status_code=404)
            response.raise_for_status()
            
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            else:
                return response.text.strip('"')
        except httpx.HTTPStatusError as e:
            raise GammaAPIError(f"API Error: {e}", status_code=e.response.status_code, response_text=e.response.text)
        except GammaError:
            raise
        except Exception as e:
            raise GammaAPIError(f"Unexpected Error: {e}")

    async def get_status(self) -> str:
        return await self._request("GET", "/status")

    async def search(self, query: str, **params) -> Dict[str, Any]:
        params["q"] = query
        return await self._request("GET", "/search", params=params)

    async def resolve_url(self, url: str) -> Union[Market, Event, None]:
        """
        Resolve a Polymarket URL to a Market or Event object.
        """
        slug = self._extract_slug_from_url(url)
        if not slug:
            raise ValidationError(f"Invalid Polymarket URL: {url}")

        # Try market first
        try:
            return await self.markets.get_by_slug(slug)
        except Exception:
            pass

        # Try event next
        try:
            return await self.events.get_by_slug(slug)
        except Exception:
            pass

        return None

    def _extract_slug_from_url(self, url: str) -> Optional[str]:
        try:
            parsed = urlparse(url)
            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) >= 2 and path_parts[0] in ["market", "event"]:
                return path_parts[-1]
            return None
        except Exception:
            return None
