# Polymarket Gamma SDK

An asynchronous Python SDK for Polymarket's Gamma API, built with `httpx` and `pydantic`.

This SDK provides a clean, type-safe interface to interact with Polymarket's market discovery and metadata API.

## Features

- **Asynchronous**: Built on `httpx` for high-performance non-blocking I/O.
- **Type-Safe**: All responses are parsed into Pydantic v2 models.
- **Hierarchical Client**: Logically grouped endpoints (e.g., `client.markets`, `client.sports`).
- **Robust Exception Handling**: Custom exceptions for `404 Not Found`, validation errors, and general API issues.
- **URL Resolution**: Convert Polymarket web URLs (markets or events) directly into SDK objects.
- **Fully Documented**: Docstrings for all classes and methods.

## Installation

### Prerequisites
- Python 3.8+

### Setup
We recommend using a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Or install the package in editable mode:
```bash
pip install -e .
```

## Quick Start

```python
import asyncio
from py_gamma_sdk import GammaClient

async def main():
    async with GammaClient() as client:
        # 1. Check API Health
        status = await client.get_status()
        print(f"API Health: {status}")

        # 2. Fetch a specific Market
        market = await client.markets.get_by_slug("will-barron-attend-georgetown")
        print(f"Question: {market.question}")
        print(f"Current Odds: {market.outcomes}")

        # 3. Resolve a Polymarket URL
        url = "https://polymarket.com/market/will-china-blockade-taiwan-by-june-30"
        obj = await client.resolve_url(url)
        if obj:
            print(f"Resolved {type(obj).__name__}: {getattr(obj, 'question', getattr(obj, 'title', ''))}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Detailed Usage

### Markets
```python
# List active markets
markets = await client.markets.list(active=True, limit=10)

# Get market by ID
market = await client.markets.get_by_id("12345")

# Get tags for a market
tags = await client.markets.get_tags("12345")
```

### Events
Events group multiple markets together.
```python
# List events with a specific slug
events = await client.events.list(slug="fed-decision")

# Get event by slug
event = await client.events.get_by_slug("fed-decision-in-january")
```

### Sports & Teams
```python
# Get all sports metadata (leagues, images, etc.)
sports = await client.sports.get_metadata()

# List teams in a specific league
teams = await client.sports.list_teams(league="NBA")
```

### Error Handling
The SDK uses a custom exception hierarchy:
```python
from py_gamma_sdk.exceptions import GammaAPIError, NotFoundError

try:
    market = await client.markets.get_by_id("invalid-id")
except NotFoundError:
    print("Market doesn't exist.")
except GammaAPIError as e:
    print(f"API Error ({e.status_code}): {e}")
```

## Development & Testing

Run unit tests:
```bash
python -m pytest tests
```

Run live integration tests (requires internet):
```bash
python -m pytest tests/test_live.py
```

## License
MIT
