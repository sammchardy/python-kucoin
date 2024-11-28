import os
import pytest
from kucoin import Client


proxies = {}
proxy = os.getenv("PROXY")

api_key = "apiKey"
api_secret = "secret"

@pytest.fixture(scope="function")
def client():
    return Client(api_key, api_secret)