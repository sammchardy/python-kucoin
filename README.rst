===============================
Welcome to python-kucoin v2.1.3
===============================

.. image:: https://img.shields.io/pypi/v/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/pypi/l/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/travis/sammchardy/python-kucoin.svg
    :target: https://travis-ci.org/sammchardy/python-kucoin

.. image:: https://img.shields.io/coveralls/sammchardy/python-kucoin.svg
    :target: https://coveralls.io/github/sammchardy/python-kucoin

.. image:: https://img.shields.io/pypi/wheel/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/pypi/pyversions/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

This is an unofficial Python wrapper for the `Kucoin exchanges REST and Websocket API v3 <https://docs.kucoin.com/>`_.
I am in no way affiliated with `Kucoin <https://www.kucoin.com/ucenter/signup?rcode=E5wkqe>`_, use at your own risk.


PyPi
  https://pypi.python.org/pypi/python-kucoin

Source code
  https://github.com/sammchardy/python-kucoin

Documentation
  https://python-kucoin.readthedocs.io/en/latest/

Examples
  https://github.com/sammchardy/python-kucoin/tree/master/examples


Features
--------

- Implementation of REST endpoints
- Spot and Futures
- Sync and Async suport
- Simple handling of authentication
- Response exception handling
- Implement websockets (note only python3.5+)
- Proxy support

TODO
----

- L2 and L3 Local Order Books

Quick Start
-----------

Register an account with `Kucoin <https://www.kucoin.com/ucenter/signup?rcode=E42cWB>`_.

`Generate an API Key <https://kucoin.com/account/api>`_.

.. code:: bash

    pip install python-kucoin

.. code:: python

    from kucoin import Client

    api_key = '<api_key>'
    api_secret = '<api_secret>'
    api_passphrase = '<api_passphrase>'

    client = Client(api_key, api_secret, api_passphrase)

    # get currencies
    currencies = client.get_currencies()

    # get market depth
    depth = client.get_order_book('KCS-BTC')

    # get symbol klines
    klines = client.get_kline_data('KCS-BTC')

    # get list of markets
    markets = client.get_markets()

    # place a market buy order
    order = client.create_market_order('NEO', Client.SIDE_BUY, size=20)

    # get list of active orders
    orders = client.get_active_orders('KCS-BTC')


Async
-----

.. code:: python

    from kucoin import AsyncClient

    api_key = '<api_key>'
    api_secret = '<api_secret>'
    api_passphrase = '<api_passphrase>'

    client = AsyncClient(api_key, api_secret, api_passphrase)

    # get currencies
    currencies = await client.get_currencies()

Websockets
----------

Note only for python3.5+

.. code:: python

    import asyncio

    from kucoin.client import Client
    from kucoin.asyncio import KucoinSocketManager

    api_key = '<api_key>'
    api_secret = '<api_secret>'
    api_passphrase = '<api_passphrase>'


    async def main():
        global loop

        # callback function that receives messages from the socket
        async def handle_evt(msg):
            if msg['topic'] == '/market/ticker:ETH-USDT':
                print(f'got ETH-USDT tick:{msg["data"]}')

            elif msg['topic'] == '/market/snapshot:BTC':
                print(f'got BTC market snapshot:{msg["data"]}')

            elif msg['topic'] == '/market/snapshot:KCS-BTC':
                print(f'got KCS-BTC symbol snapshot:{msg["data"]}')

            elif msg['topic'] == '/market/ticker:all':
                print(f'got all market snapshot:{msg["data"]}')

            elif msg['topic'] == '/account/balance':
                print(f'got account balance:{msg["data"]}')

            elif msg['topic'] == '/market/level2:KCS-BTC':
                print(f'got L2 msg:{msg["data"]}')

            elif msg['topic'] == '/market/match:BTC-USDT':
                print(f'got market match msg:{msg["data"]}')

            elif msg['topic'] == '/market/level3:BTC-USDT':
                if msg['subject'] == 'trade.l3received':
                    if msg['data']['type'] == 'activated':
                        # must be logged into see these messages
                        print(f"L3 your order activated: {msg['data']}")
                    else:
                        print(f"L3 order received:{msg['data']}")
                elif msg['subject'] == 'trade.l3open':
                    print(f"L3 order open: {msg['data']}")
                elif msg['subject'] == 'trade.l3done':
                    print(f"L3 order done: {msg['data']}")
                elif msg['subject'] == 'trade.l3match':
                    print(f"L3 order matched: {msg['data']}")
                elif msg['subject'] == 'trade.l3change':
                    print(f"L3 order changed: {msg['data']}")

        client = Client(api_key, api_secret, api_passphrase)

        ksm = await KucoinSocketManager.create(loop, client, handle_evt)

        # for private topics such as '/account/balance' pass private=True
        ksm_private = await KucoinSocketManager.create(loop, client, handle_evt, private=True)

        # Note: try these one at a time, if all are on you will see a lot of output

        # ETH-USDT Market Ticker
        await ksm.subscribe('/market/ticker:ETH-USDT')
        # BTC Symbol Snapshots
        await ksm.subscribe('/market/snapshot:BTC')
        # KCS-BTC Market Snapshots
        await ksm.subscribe('/market/snapshot:KCS-BTC')
        # All tickers
        await ksm.subscribe('/market/ticker:all')
        # Level 2 Market Data
        await ksm.subscribe('/market/level2:KCS-BTC')
        # Market Execution Data
        await ksm.subscribe('/market/match:BTC-USDT')
        # Level 3 market data
        await ksm.subscribe('/market/level3:BTC-USDT')
        # Account balance - must be authenticated
        await ksm_private.subscribe('/account/balance')

        while True:
            print("sleeping to keep loop open")
            await asyncio.sleep(20, loop=loop)


    if __name__ == "__main__":

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())


For more `check out the documentation <https://python-kucoin.readthedocs.io/en/latest/>`_.


Other Exchanges
---------------

- If you use `Binance <https://accounts.binance.com/register?ref=PGDFCE46>`_ check out my `python-binance <https://github.com/sammchardy/python-binance>`_ library.
- Check out `CCXT <https://github.com/ccxt/ccxt>`_ for more than 100 crypto exchanges with a unified trading API.

