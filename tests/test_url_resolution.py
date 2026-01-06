import pytest
import respx
from httpx import Response

@pytest.mark.asyncio
async def test_resolve_url_market(client):
    url = "https://polymarket.com/market/market-slug"
    mock_market = {
        "id": "1", "question": "Q", "conditionId": "0x1", "slug": "market-slug", "outcomes": [], "clobTokenIds": []
    }
    with respx.mock:
        # Resolve calls markets.get_by_slug(slug)
        respx.get("https://gamma-api.polymarket.com/markets/slug/market-slug").mock(
            return_value=Response(200, json=mock_market)
        )
        result = await client.resolve_url(url)
        assert result.slug == "market-slug"
        assert result.id == "1"

@pytest.mark.asyncio
async def test_resolve_url_event(client):
    url = "https://polymarket.com/event/event-slug"
    mock_event = {
        "id": "e1", "slug": "event-slug", "title": "Event", "markets": []
    }
    with respx.mock:
        # Resolve calls markets.get_by_slug first (fail it) then events.get_by_slug
        respx.get("https://gamma-api.polymarket.com/markets/slug/event-slug").mock(
            return_value=Response(404)
        )
        respx.get("https://gamma-api.polymarket.com/events/slug/event-slug").mock(
            return_value=Response(200, json=mock_event)
        )
        result = await client.resolve_url(url)
        assert result.slug == "event-slug"
        assert result.id == "e1"
