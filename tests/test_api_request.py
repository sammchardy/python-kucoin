#!/usr/bin/env python
# coding=utf-8

from kucoin.exceptions import (
    KucoinAPIException,
    KucoinRequestException,
)
import pytest
import requests_mock


def test_invalid_json(client):
    """Test Invalid response Exception"""

    with pytest.raises(KucoinRequestException):
        with requests_mock.mock() as m:
            m.get(
                "https://api.kucoin.com/api/v3/currencies", text="<head></html>"
            )
            client.get_currencies()


def test_api_exception(client):
    """Test API response Exception"""

    with pytest.raises(KucoinAPIException):
        with requests_mock.mock() as m:
            json_obj = {"code": "900003", "msg": "currency {0} not exists"}
            m.get(
                "https://api.kucoin.com/api/v3/currencies/BTD",
                json=json_obj,
                status_code=400,
            )
            client.get_currency("BTD")
