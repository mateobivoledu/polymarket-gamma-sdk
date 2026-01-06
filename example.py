import asyncio
import json
from py_gamma_sdk import GammaClient

async def main():
    async with GammaClient() as client:
        print("--- Checking Health ---")
        status = await client.get_status()
        print(f"Status: {status}")

        print("\n--- Fetching Market by Slug ---")
        # Example slug from documentation
        slug = "will-barron-attend-georgetown"
        try:
            market = await client.markets.get_by_slug(slug)
            print(f"Market Question: {market.question}")
            print(f"Condition ID: {market.condition_id}")
        except Exception as e:
            print(f"Fetch market status: {e}")

        print("\n--- Listing Sports Metadata ---")
        sports = await client.sports.get_metadata()
        for sport in sports[:3]:
            print(f"Sport: {sport.sport}, Image: {sport.image}")

        print("\n--- Searching for 'Politics' ---")
        results = await client.search("Politics")
        print(f"Search results count: {len(results.get('data', []))}")

if __name__ == "__main__":
    asyncio.run(main())
