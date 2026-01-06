import pytest
import respx
from httpx import Response
from py_gamma_sdk.models import Event

@pytest.mark.asyncio
async def test_get_event_by_slug(client):
    mock_event = {
        "id": "e1",
        "slug": "event-slug",
        "title": "Main Event",
        "markets": []
    }
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/events/slug/event-slug").mock(
            return_value=Response(200, json=mock_event)
        )
        event = await client.events.get_by_slug("event-slug")
        assert event.id == "e1"
        assert event.title == "Main Event"

@pytest.mark.asyncio
async def test_get_event_tags(client):
    mock_tags = [{"id": "t1", "label": "Politics"}]
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/events/e1/tags").mock(
            return_value=Response(200, json=mock_tags)
        )
        tags = await client.events.get_tags("e1")
        assert len(tags) == 1
        assert tags[0].label == "Politics"
