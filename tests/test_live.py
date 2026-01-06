import pytest
import os
from py_gamma_sdk.models import Market, Event, Tag, Team, SportMetadata, Series, Comment, Profile
from py_gamma_sdk.exceptions import GammaAPIError

# These tests hit the live Gamma API.
# Use: pytest tests/test_live.py

@pytest.mark.asyncio
async def test_live_status(client):
    status = await client.get_status()
    assert status == "OK"

@pytest.mark.asyncio
async def test_live_list_markets(client):
    markets = await client.markets.list(limit=5, active=True)
    assert len(markets) > 0
    assert isinstance(markets[0], Market)

@pytest.mark.asyncio
async def test_live_list_events(client):
    events = await client.events.list(limit=5, active=True)
    assert len(events) > 0
    assert isinstance(events[0], Event)

@pytest.mark.asyncio
async def test_live_list_tags(client):
    tags = await client.tags.list(limit=5)
    assert len(tags) > 0
    assert isinstance(tags[0], Tag)

@pytest.mark.asyncio
async def test_live_list_teams(client):
    teams = await client.sports.list_teams(limit=5)
    assert len(teams) > 0
    assert isinstance(teams[0], Team)

@pytest.mark.asyncio
async def test_live_sports_metadata(client):
    metadata = await client.sports.get_metadata()
    assert len(metadata) > 0
    assert isinstance(metadata[0], SportMetadata)

@pytest.mark.asyncio
async def test_live_sports_market_types(client):
    types = await client.sports.get_market_types()
    assert isinstance(types, list)

@pytest.mark.asyncio
async def test_live_list_series(client):
    series = await client.series.list(limit=5)
    assert len(series) > 0
    assert isinstance(series[0], Series)

@pytest.mark.asyncio
async def test_live_list_comments(client):
    # Comments requires parent_entity_id and entity_entity_type
    # We fetch an active market to get an ID
    markets = await client.markets.list(limit=1, active=True)
    if not markets:
        pytest.skip("No active markets found to test comments")
        
    market_id = markets[0].id
    try:
        # Gamma API typically uses camelCase
        comments = await client.comments.list(parentEntityId=market_id, entityEntityType="market")
        assert isinstance(comments, list)
        if comments:
            assert isinstance(comments[0], Comment)
    except GammaAPIError as e:
        if e.status_code in [401, 422]:
            pytest.skip(f"Comments endpoint returned {e.status_code}")
        raise

@pytest.mark.asyncio
async def test_live_search(client):
    try:
        results = await client.search("Politics", limit=1)
        assert "data" in results
        assert len(results["data"]) > 0
    except GammaAPIError as e:
        if e.status_code == 401:
            pytest.skip("Search endpoint returns 401 Unauthorized")
        raise

@pytest.mark.asyncio
async def test_live_resolve_url_market(client):
    # Dynamic lookup to ensure slug is active
    markets = await client.markets.list(limit=1, active=True)
    if not markets:
        pytest.skip("No active markets found to test resolve_url")
    
    slug = markets[0].slug
    url = f"https://polymarket.com/market/{slug}"
    result = await client.resolve_url(url)
    assert result is not None
    assert result.slug == slug

@pytest.mark.asyncio
async def test_live_get_tag_by_slug(client):
    # 'politics' is a common tag
    tag = await client.tags.get_by_slug("politics")
    assert isinstance(tag, Tag)
    assert tag.slug == "politics"
