#!/usr/bin/env python
# coding=utf-8

from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException, KucoinRequestException, MarketOrderException, LimitOrderException
import pytest
import requests_mock


client = Client('api_key', 'api_secret', 'api_phrase')


def test_invalid_json():
    """Test Invalid response Exception"""

    with pytest.raises(KucoinRequestException):
        with requests_mock.mock() as m:
            m.get('https://openapi-v2.kucoin.com/api/v1/currencies', text='<head></html>')
            client.get_currencies()


def test_api_exception():
    """Test API response Exception"""

    with pytest.raises(KucoinAPIException):
        with requests_mock.mock() as m:
            json_obj = {
                "code": "900003",
                "msg": "currency {0} not exists"
            }
            m.get('https://openapi-v2.kucoin.com/api/v1/currencies/BTD', json=json_obj, status_code=400)
            client.get_currency('BTD')
