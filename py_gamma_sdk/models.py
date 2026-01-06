from typing import List, Optional, Any, Union, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class GammaBaseModel(BaseModel):
    class Config:
        populate_by_name = True

class Tag(GammaBaseModel):
    id: str
    label: Optional[str] = None
    slug: Optional[str] = None
    force_show: Optional[bool] = Field(None, alias="forceShow")
    force_hide: Optional[bool] = Field(None, alias="forceHide")
    is_carousel: Optional[bool] = Field(None, alias="isCarousel")
    published_at: Optional[str] = Field(None, alias="publishedAt")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

class Market(GammaBaseModel):
    """Represents a single Polymarket market."""
    id: str
    question: str
    condition_id: str = Field(..., alias="conditionId")
    slug: str
    twitter_card_image: Optional[str] = Field(None, alias="twitterCardImage")
    resolution_source: Optional[str] = Field(None, alias="resolutionSource")
    end_date_iso: Optional[str] = Field(None, alias="endDateIso")
    category: Optional[str] = None
    amm_type: Optional[str] = Field(None, alias="ammType")
    liquidity: Optional[float] = None
    volume: Optional[float] = None
    outcomes: Union[List[str], str]
    clob_token_ids: Union[List[str], str] = Field(..., alias="clobTokenIds")
    group_item_title: Optional[str] = Field(None, alias="groupItemTitle")
    group_item_threshold: Optional[str] = Field(None, alias="groupItemThreshold")
    question_id: Optional[str] = Field(None, alias="questionId")
    rewards_min_size: Optional[float] = Field(None, alias="rewardsMinSize")
    rewards_max_spread: Optional[float] = Field(None, alias="rewardsMaxSpread")
    spread: Optional[float] = None
    last_trade_price: Optional[float] = Field(None, alias="lastTradePrice")
    best_bid: Optional[float] = Field(None, alias="bestBid")
    best_ask: Optional[float] = Field(None, alias="bestAsk")
    active: bool = True
    closed: bool = False
    archived: bool = False
    restricted: bool = False
    event_id: Optional[str] = Field(None, alias="eventId")

class Event(GammaBaseModel):
    """Represents an event that can contain multiple markets."""
    id: str
    ticker: Optional[str] = None
    slug: str
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    icon: Optional[str] = None
    active: bool = True
    closed: bool = False
    archived: bool = False
    new: bool = False
    featured: bool = False
    restricted: bool = False
    start_date: Optional[datetime] = Field(None, alias="startDate")
    end_date: Optional[datetime] = Field(None, alias="endDate")
    creation_date: Optional[datetime] = Field(None, alias="creationDate")
    last_updated_at: Optional[datetime] = Field(None, alias="lastUpdatedAt")
    markets: List[Market] = []
    tags: List[Tag] = []

class Team(GammaBaseModel):
    """Represents a sports team."""
    id: int
    name: str
    league: str
    record: Optional[str] = None
    logo: Optional[str] = None
    abbreviation: Optional[str] = None
    alias: Optional[str] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

class SportMetadata(GammaBaseModel):
    """Provides metadata for sports events."""
    sport: str
    image: Optional[str] = None
    resolution: Optional[str] = None
    ordering: Optional[str] = None
    tags: Optional[str] = None
    series: Optional[str] = None

class Series(GammaBaseModel):
    """Represents a series or collection of events/markets."""
    id: str
    title: str
    slug: str
    active: bool
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

class Comment(GammaBaseModel):
    """Represents a user comment on a market or event."""
    id: str
    comment: str
    user_address: str = Field(..., alias="userAddress")
    user_name: Optional[str] = Field(None, alias="userName")
    proxy_wallet: Optional[str] = Field(None, alias="proxyWallet")
    market_id: Optional[str] = Field(None, alias="marketId")
    event_id: Optional[str] = Field(None, alias="eventId")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

class Profile(GammaBaseModel):
    proxy_wallet: str = Field(..., alias="proxyWallet")
    display_name: Optional[str] = Field(None, alias="displayName")
    bio: Optional[str] = None
    image: Optional[str] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
