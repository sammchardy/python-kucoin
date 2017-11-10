#!/usr/bin/env python
# coding=utf-8

from kucoin.client import Client
from kucoin.exceptions import KucoinResolutionException
import pytest

client = Client('api_key', 'api_secret')


def test_resolution_exception():
    """Test Resolution Exception"""

    with pytest.raises(KucoinResolutionException):

        client.get_kline_data('KCS-BTC', 'invalid-res', 1510156800, 1510278278)
