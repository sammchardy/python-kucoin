import requests_mock
import pytest
from aioresponses import aioresponses

from kucoin import Client, AsyncClient


def test_post_headers(client):
    with requests_mock.mock() as m:
        m.post("https://api.kucoin.com/api/v1/orders", json={}, status_code=200)
        client.create_order(symbol="LTCUSDT", side="buy", type="market", quantity=0.1, size=0.1)
        headers = m.last_request._request.headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"

    with requests_mock.mock() as m:
        m.post("https://api.kucoin.com/api/v1/hf/orders/alter", json={}, status_code=200)
        client.hf_modify_order(symbol="LTCUSDT", order_id="123", new_size=0.1)
        headers = m.last_request._request.headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"

@pytest.mark.asyncio()
async def test_post_headers_async():
    clientAsync = AsyncClient(
        api_key="api_key", api_secret="api_secret", passphrase="passphrase"
    )  # reuse client later
    with aioresponses() as m:

        def handler(url, **kwargs):
            headers = kwargs["headers"]
            assert "Content-Type" in headers
            assert headers["Content-Type"] == "application/json"

        m.post(
            "https://api.kucoin.com/api/v1/orders",
            payload={"id": 123},
            status=200,
            callback=handler,
        )
        await clientAsync.create_order(
            symbol="LTCUSDT", side="buy", type="market", quantity=0.1, size=0.1
        )
        await clientAsync.close_connection()