===============================
Welcome to python-kucoin v2.1.1
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

This is an unofficial Python wrapper for the `Kucoin exchanges REST and Websocket API v2 <https://docs.kucoin.com/>`_.
I am in no way affiliated with Kucoin, use at your own risk.


PyPi
  https://pypi.python.org/pypi/python-kucoin

Source code
  https://github.com/sammchardy/python-kucoin

Documentation
  https://python-kucoin.readthedocs.io/en/latest/

Blog with examples
  https://sammchardy.github.io


Features
--------

- Implementation of REST endpoints
- Simple handling of authentication
- Response exception handling
- Implement websockets (note only python3.5+)

TODO
----

- L2 and L3 Local Order Books

Quick Start
-----------

Register an account with `Kucoin <https://www.kucoin.com/ucenter/signup?rcode=E42cWB>`_.

To test on the Sandbox register with `Kucoin Sandbox <https://sandbox.kucoin.com/ucenter/signup?rcode=ewcefH>`_.

`Generate an API Key <https://kucoin.com/account/api>`_
or `Generate an API Key in Sandbox <https://sandbox.kucoin.com/account/api>`_ and enable it.

.. code:: bash

    pip install python-kucoin

.. code:: python

    from kucoin.client import Client

    api_key = '<api_key>'
    api_secret = '<api_secret>'
    api_passphrase = '<api_passphrase>'

    client = Client(api_key, api_secret, api_passphrase)

    # or connect to Sandbox
    # client = Client(api_key, api_secret, api_passphrase, sandbox=True)

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
        await ksm.subscribe('/account/balance')

        while True:
            print("sleeping to keep loop open")
            await asyncio.sleep(20, loop=loop)


    if __name__ == "__main__":

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())


For more `check out the documentation <https://python-kucoin.readthedocs.io/en/latest/>`_.

Donate
------

If this library helped you out feel free to donate.

- ETH: 0xD7a7fDdCfA687073d7cC93E9E51829a727f9fE70
- NEO: AVJB4ZgN7VgSUtArCt94y7ZYT6d5NDfpBo
- LTC: LPC5vw9ajR1YndE1hYVeo3kJ9LdHjcRCUZ
- BTC: 1Dknp6L6oRZrHDECRedihPzx2sSfmvEBys

Other Exchanges
---------------

If you use `Binance <https://www.binance.com/?ref=10099792>`_ check out my `python-binance <https://github.com/sammchardy/python-binance>`_ library.

If you use `Binance Chain <https://testnet.binance.org/>`_ check out my `python-binance-chain <https://github.com/sammchardy/python-binance-chain>`_ library.

If you use `Allcoin <https://www.allcoin.com/GXHKu1>`_ check out my `python-allcoin <https://github.com/sammchardy/python-allcoin>`_ library.

If you use `IDEX <https://idex.market>`_ check out my `python-idex <https://github.com/sammchardy/python-idex>`_ library.

If you use `BigONE <https://big.one>`_ check out my `python-bigone <https://github.com/sammchardy/python-bigone>`_ library.

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-kucoin?pixel
