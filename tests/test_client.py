import pytest
import respx
from httpx import Response
from py_gamma_sdk import GammaClient
from py_gamma_sdk.exceptions import GammaAPIError, NotFoundError

@pytest.mark.asyncio
async def test_get_status_ok(client):
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/status").mock(return_value=Response(200, text="OK", headers={"Content-Type": "text/plain"}))
        status = await client.get_status()
        assert status == "OK"

@pytest.mark.asyncio
async def test_get_status_json_ok(client):
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/status").mock(return_value=Response(200, json="OK", headers={"Content-Type": "application/json"}))
        status = await client.get_status()
        assert status == "OK"

@pytest.mark.asyncio
async def test_not_found_error(client):
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/markets/999").mock(return_value=Response(404))
        with pytest.raises(NotFoundError):
            await client.markets.get_by_id("999")

@pytest.mark.asyncio
async def test_search(client):
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/search").mock(return_value=Response(200, json={"data": [{"id": "1"}]}))
        results = await client.search("test")
        assert len(results["data"]) == 1
        assert results["data"][0]["id"] == "1"
