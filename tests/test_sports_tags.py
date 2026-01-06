import pytest
import respx
from httpx import Response

@pytest.mark.asyncio
async def test_list_teams(client):
    mock_teams = [{"id": 1, "name": "Team A", "league": "NBA"}]
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/teams").mock(
            return_value=Response(200, json=mock_teams)
        )
        teams = await client.sports.list_teams()
        assert len(teams) == 1
        assert teams[0].name == "Team A"

@pytest.mark.asyncio
async def test_list_tags(client):
    mock_tags = [{"id": "t1", "label": "Tag 1"}]
    with respx.mock:
        respx.get("https://gamma-api.polymarket.com/tags").mock(
            return_value=Response(200, json=mock_tags)
        )
        tags = await client.tags.list()
        assert len(tags) == 1
        assert tags[0].label == "Tag 1"
