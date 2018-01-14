#!/usr/bin/env python
# coding=utf-8

from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException, KucoinRequestException, KucoinResolutionException
import pytest
import requests_mock


client = Client('api_key', 'api_secret')


def test_invalid_json():
    """Test Invalid response Exception"""

    with pytest.raises(KucoinRequestException):
        with requests_mock.mock() as m:
            m.get('https://api.kucoin.com/v1/open/currencies', text='<head></html>')
            client.get_currencies()


def test_api_exception():
    """Test API response Exception"""

    with pytest.raises(KucoinAPIException):
        with requests_mock.mock() as m:
            json_obj = {
                "code": "UNAUTH",
                "msg": "Signature verification failed",
                "success": False,
                "timestamp": 1510287654892
            }
            m.get('https://api.kucoin.com/v1/user/info', json=json_obj, status_code=400)
            client.get_user()


def test_api_error_exception():
    """Test API response Exception"""

    with pytest.raises(KucoinAPIException):
        with requests_mock.mock() as m:
            json_obj = {
                "timestamp": 1510287193757,
                "status": 404,
                "error": "Not Found",
                "message": "No message available",
                "path": "/open/chart/symbol"
            }
            m.get('https://api.kucoin.com/v1/open/chart/symbol?symbol=KCS-BTC', json=json_obj, status_code=400)
            client.get_symbol_tv('KCS-BTC')


def test_api_200_exception():
    """Test API response Exception"""

    with pytest.raises(KucoinAPIException):
        with requests_mock.mock() as m:
            json_obj = {
                "success": False,
                "code": "NO_BALANCE",
                "msg": "Insufficient balance: BTC",
                "timestamp": 1515925287831,
                "data": {
                    "coinType": "BTC",
                    "expect": 0.00465456,
                    "actual": 2.6447E-4
                }
            }

            m.get('https://api.kucoin.com/v1/user/info', json=json_obj, status_code=200)
            client.get_user()
