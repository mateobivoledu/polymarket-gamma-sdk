import pytest
import pytest_asyncio
from py_gamma_sdk import GammaClient

@pytest_asyncio.fixture
async def client():
    async with GammaClient() as client:
        yield client
