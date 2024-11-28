import os
import pytest
from kucoin import Client, AsyncClient
import asyncio

proxies = {}
proxy = os.getenv("PROXY")

api_key = "apiKey"
api_secret = "secret"

@pytest.fixture(scope="function")
def client():
    return Client(api_key, api_secret)


@pytest.fixture(autouse=True, scope="function")
def event_loop():
    """Create new event loop for each test"""
    loop = asyncio.new_event_loop()
    yield loop
    # Clean up pending tasks
    pending = asyncio.all_tasks(loop)
    for task in pending:
        task.cancel()
    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    loop.close()


@pytest.fixture(scope="function")
def asyncClient():
    return AsyncClient(api_key, api_secret)