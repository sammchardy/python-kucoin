
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from kucoin.client import Client

api_key = os.environ.get('KUCOIN_APIKEY')
api_secret = os.environ.get('KUCOIN_SECRET')
api_passphrase = os.environ.get('KUCOIN_PASSWORD')

client = Client(api_key, api_secret, api_passphrase)

order = client.create_market_order('LTC-USDT', Client.SIDE_SELL, size=0.1)

print(order)