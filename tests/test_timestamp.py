import pytest

def test_spot_timestamp(client):
    ping_response = client.get_timestamp()
    assert ping_response is not None

def test_futures_timestamp(client):
    ping_response = client.futures_get_timestamp()
    assert ping_response is not None

@pytest.mark.asyncio()
async def test_timestamp_async(asyncClient):
    ping_response = await asyncClient.get_timestamp()
    assert ping_response is not None

@pytest.mark.asyncio()
async def test_futures_ping_async(asyncClient):
    ping_response = await asyncClient.futures_get_timestamp()
    assert ping_response is not None
