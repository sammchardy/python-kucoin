Websockets
==========

Note: The websocket client is only available for python3.6+

This feature is still in development so check the documentation around message topics here
https://docs.kucoin.com/#websocket-feed


TODO:
-----

- Helper functions for topics
- Multiplexing
- Local Order book level 2 & 3


Sample Code
-----------

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


Unsubscribe from channel
------------------------

Send the same topic name to the unsubscribe function

.. code:: python

        await ksm.unsubscribe('/market/ticker:ETH-USDT')
