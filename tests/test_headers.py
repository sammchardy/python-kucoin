import requests_mock
import pytest
from aioresponses import aioresponses


SPOT_KC_PARTNER = "python-kucoinspot"
SPOT_KC_KEY = "922783d1-067e-4a31-bb42-4d1589624e30"
FUTURES_KC_PARTNER = "python-kucoinfutures"
FUTURES_KC_KEY = "5c0f0e56-a866-44d9-a50b-8c7c179dc915"


def test_post_headers(client):
    with requests_mock.mock() as m:
        m.post("https://api.kucoin.com/api/v1/orders", json={}, status_code=200)
        client.create_order(symbol="LTCUSDT", side="buy", type="market", quantity=0.1, size=0.1)
        headers = m.last_request._request.headers
        assert client.SPOT_KC_KEY == SPOT_KC_KEY
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"
        assert "KC-API-KEY" in headers
        assert "KC-API-PASSPHRASE" in headers
        assert headers["KC-API-PARTNER"] == SPOT_KC_PARTNER

    with requests_mock.mock() as m:
        m.post("https://api.kucoin.com/api/v1/hf/orders/alter", json={}, status_code=200)
        client.hf_modify_order(symbol="LTCUSDT", order_id="123", new_size=0.1)
        headers = m.last_request._request.headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"
        assert "KC-API-KEY" in headers
        assert "KC-API-PASSPHRASE" in headers
        assert headers["KC-API-PARTNER"] == SPOT_KC_PARTNER


def test_post_headers_futures(client):
    with requests_mock.mock() as m:
        m.post("https://api-futures.kucoin.com/api/v1/orders", json={}, status_code=200)
        client.futures_create_order(symbol="LTCUSDT", side="buy", type="market", quantity=0.1, size=0.1, leverage=2)
        headers = m.last_request._request.headers
        assert client.FUTURES_KC_KEY == FUTURES_KC_KEY
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"
        assert "KC-API-KEY" in headers
        assert headers["KC-API-PARTNER"] == FUTURES_KC_PARTNER



@pytest.mark.asyncio()
async def test_post_headers_async(asyncClient):
    with aioresponses() as m:

        def handler(url, **kwargs):
            headers = kwargs["headers"]
            assert headers["KC-API-PARTNER"] == SPOT_KC_PARTNER

        m.post(
            "https://api.kucoin.com/api/v1/orders",
            payload={"id": 123},
            status=200,
            callback=handler,
        )
        await asyncClient.create_order(
            symbol="LTCUSDT", side="buy", type="market", quantity=0.1, size=0.1
        )
        await asyncClient.close_connection()


async def test_post_headers_async_futures(asyncClient):
    with aioresponses() as m:

        def handler(url, **kwargs):
            headers = kwargs["headers"]
            assert headers["KC-API-PARTNER"] == FUTURES_KC_PARTNER

        m.post(
            "https://api.kucoin.com/api/v1/orders",
            payload={"id": 123},
            status=200,
            callback=handler,
        )
        await asyncClient.futures_create_order(
            symbol="LTCUSDT", side="buy", type="market", quantity=0.1, size=0.1, leverage=2
        )
        await asyncClient.close_connection()