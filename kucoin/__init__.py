"""An unofficial Python wrapper for the Kucoin exchange API with Websocket support

.. moduleauthor:: Sam McHardy

"""

__version__ = "2.1.3"

from kucoin.client import Client
from kucoin.async_client import AsyncClient

from kucoin.exceptions import KucoinAPIException, KucoinRequestException, MarketOrderException, LimitOrderException
