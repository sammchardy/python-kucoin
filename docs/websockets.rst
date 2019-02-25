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
            print(f"msg sequence:{msg['data']['sequence']}")
            if msg['topic'] == '/market/ticker:ETH-USDT':
                # do something about the ticker
                print(f'got ETH-USDT tick:{msg["data"]}')
            elif msg['topic'] == '/market/snapshot:KCS-BTC':
                # do something about the ticker
                print(f'got KCS-BTC snapshot:{msg["data"]}')

        client = Client(api_key, api_secret, api_passphrase)

        ksm = await KucoinSocketManager.create(loop, client, handle_evt)

        await ksm.subscribe('/market/ticker:ETH-USDT')
        await ksm.subscribe('/market/snapshot:KCS-BTC')

        while True:
            print("sleeping to keep loop open")
            await asyncio.sleep(20, loop=loop)


    if __name__ == "__main__":

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

