import pytest
import respx
from httpx import Response
from py_gamma_sdk.models import Market

@pytest.mark.asyncio
async def test_get_market_by_slug(client):
    mock_market = {
        "id": "123",
        "question": "Will it rain?",
        "conditionId": "0xc1",
        "slug": "will-it-rain",
        "outcomes": ["Yes", "No"],
        "clobTokenIds": ["1", "2"]
    }
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/markets/slug/will-it-rain").mock(
            return_value=Response(200, json=mock_market, headers={"Content-Type": "application/json"})
        )
        market = await client.markets.get_by_slug("will-it-rain")
        assert isinstance(market, Market)
        assert market.id == "123"
        assert market.question == "Will it rain?"

@pytest.mark.asyncio
async def test_list_markets(client):
    mock_markets = [
        {
            "id": "123",
            "question": "Will it rain?",
            "conditionId": "0xc1",
            "slug": "will-it-rain",
            "outcomes": ["Yes", "No"],
            "clobTokenIds": ["1", "2"]
        }
    ]
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/markets").mock(
            return_value=Response(200, json=mock_markets, headers={"Content-Type": "application/json"})
        )
        markets = await client.markets.list(active=True)
        assert len(markets) == 1
        assert markets[0].slug == "will-it-rain"
