
import os
import sys
import asyncio

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from kucoin import AsyncClient

api_key = os.environ.get('KUCOIN_APIKEY')
api_secret = os.environ.get('KUCOIN_SECRET')
api_passphrase = os.environ.get('KUCOIN_PASSWORD')

async def main():
    client = AsyncClient(api_key, api_secret, api_passphrase)

    order = await client.create_market_order('LTC-USDT', AsyncClient.SIDE_SELL, size=0.1)

    print(order)

asyncio.run(main())