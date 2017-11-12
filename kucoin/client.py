#!/usr/bin/env python
# coding=utf-8

import base64
import hashlib
import hmac
import time
import requests

from .exceptions import KucoinAPIException, KucoinRequestException, KucoinResolutionException


class Client(object):

    API_URL = 'https://api.kucoin.com'
    API_VERSION = 'v1'
    _language = 'en-US'

    _last_timestamp = None

    TRANSFER_WITHDRAWAL = 'WITHDRAW'
    TRANSFER_DEPOSIT = 'DEPOSIT'

    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'

    TRANSFER_STATUS_CANCELLED = 'CANCEL'
    TRANSFER_STATUS_SUCCESS = 'SUCCESS'

    RESOLUTION_1MINUTE = '1'
    RESOLUTION_5MINUTES = '5'
    RESOLUTION_15MINUTES = '15'
    RESOLUTION_30MINUTES = '30'
    RESOLUTION_1HOUR = '60'
    RESOLUTION_8HOURS = '480'
    RESOLUTION_1DAY = 'D'
    RESOLUTION_1WEEK = 'W'

    _resolution_map = {
        RESOLUTION_1MINUTE: '1min',
        RESOLUTION_5MINUTES: '5min',
        RESOLUTION_15MINUTES: '15min',
        RESOLUTION_30MINUTES: '30min',
        RESOLUTION_1HOUR: '1hour',
        RESOLUTION_8HOURS: '8hour',
        RESOLUTION_1DAY: '1day',
        RESOLUTION_1WEEK: '1week',
    }

    def __init__(self, api_key, api_secret, language=None):
        """Kucoin API Client constructor

        https://kucoinapidocs.docs.apiary.io/

        :param api_key: Api Token Id
        :type api_key: string
        :param api_secret: Api Secret
        :type api_secret: string

        .. code:: python

            products = Client(api_key, api_secret)

        """

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        if language:
            self._language = language
        self.session = self._init_session()

    def _init_session(self):

        session = requests.session()
        headers = {'Accept': 'application/json',
                   'User-Agent': 'python-kucoin',
                   'KC-API-KEY': self.API_KEY,
                   'HTTP_ACCEPT_LANGUAGE': self._language,
                   'Accept-Language': self._language}
        session.headers.update(headers)
        return session

    def _order_params_for_sig(self, data):
        """Convert params to ordered string for signature

        :param data:
        :return: ordered parameters like amount=10&price=1.1&type=BUY

        """
        strs = []
        for key in sorted(data):
            strs.append("{}={}".format(key, data[key]))
        return '&'.join(strs)

    def _generate_signature(self, path, data, nonce):
        """Generate the call signature

        :param path:
        :param data:
        :param nonce:

        :return: signature string

        """

        query_string = self._order_params_for_sig(data)
        sig_str = ("{}/{}/{}".format(path, nonce, query_string)).encode('utf-8')
        m = hmac.new(self.API_SECRET.encode('utf-8'), base64.b64encode(sig_str), hashlib.sha256)
        return m.hexdigest()

    def _create_path(self, method, path):
        return '/{}/{}'.format(self.API_VERSION, path)

    def _create_uri(self, path):
        return '{}{}'.format(self.API_URL, path)

    def _request(self, method, path, signed, **kwargs):

        kwargs['data'] = kwargs.get('data', {})
        kwargs['headers'] = kwargs.get('headers', {})

        full_path = self._create_path(method, path)
        uri = self._create_uri(full_path)

        if signed:
            # generate signature
            nonce = int(time.time() * 1000)
            kwargs['headers']['KC-API-NONCE'] = str(nonce)
            kwargs['headers']['KC-API-SIGNATURE'] = self._generate_signature(full_path, kwargs['data'], nonce)

        if kwargs['data'] and method == 'get':
            kwargs['params'] = kwargs['data']
            del(kwargs['data'])

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Internal helper for handling API responses from the Quoine server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """

        if not str(response.status_code).startswith('2'):
            raise KucoinAPIException(response)
        try:
            json = response.json()
            self._last_timestamp = None
            if 'timestamp' in json:
                self._last_timestamp = json['timestamp']

            # by default return full response
            res = json
            # if it's a normal response we have a data attribute, return that
            if 'data' in json:
                res = json['data']
            return res
        except ValueError:
            raise KucoinRequestException('Invalid Response: %s' % response.text)

    def _get(self, path, signed=False, **kwargs):
        return self._request('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs):
        return self._request('post', path, signed, **kwargs)

    def _put(self, path, signed=False, **kwargs):
        return self._request('put', path, signed, **kwargs)

    def _delete(self, path, signed=False, **kwargs):
        return self._request('delete', path, signed, **kwargs)

    def get_last_timestamp(self):
        """Get the server timestamp for the last request

        :return: response timestamp in ms

        """
        return self._last_timestamp

    # Currency Endpoints

    def get_currencies(self, coins=None):
        """List the exchange rate of coins

        https://kucoinapidocs.docs.apiary.io/#reference/0/currencies-plugin/list-exchange-rate-of-coins(open)

        :param coins: optional - List of coins to get exchange rate for
        :type coins: string or list

        .. code:: python

            # call with no coins
            products = client.get_currencies()

            # call with just one coin
            products = client.get_currencies('NEO')

            # call with a list of coin strings
            products = client.get_currencies(['NEO', 'BTC'])

        :returns: API Response

        .. code-block:: python

            {
                "currencies": [
                    [
                        "USD",
                        "$"
                    ],
                    [
                        "EUR",
                        "€"
                    ],
                    [
                        "CNY",
                        "¥"
                    ],
                    [
                        "JPY",
                        "¥"
                    ],
                    [
                        "CHF",
                        "CHF"
                    ],
                    [
                        "HKD",
                        "$"
                    ],
                    [
                        "GBP",
                        "£"
                    ],
                    [
                        "RUB",
                        "₽"
                    ],
                    [
                        "AUD",
                        "$"
                    ]
                ],
                "rates": {
                    "BTC": {
                        "AUD": 7377.67,
                        "CHF": 5642.31,
                        "HKD": 45111.9,
                        "JPY": 648153.6,
                        "EUR": 4892.29,
                        "GBP": 4353.16,
                        "USD": 5777.8,
                        "RUB": 333263.5,
                        "CNY": 38077.43
                    }
                }
            }

        :raises:  KucoinResponseException,  KucoinAPIException

        """

        data = {}
        if coins:
            if type(coins) != list:
                coins = [coins]
            data['coins'] = ','.join(coins)

        return self._get('open/currencies', False, data=data)

    # Language Endpoints

    def get_languages(self):
        """List of supported languages

        https://kucoinapidocs.docs.apiary.io/#reference/0/language/list-languages(open)

        .. code:: python

            languages = client.get_languages()

        :returns: API Response

        .. code-block:: python

            [
                [
                    "zh_CN",
                    "中文",
                    true        # if language is available
                ],
                [
                    "en_US",
                    "English",
                    false
                ]
            ]

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('open/lang-list')

    # User Endpoints

    def update_language(self, language):
        """Change the language for your account.

        https://kucoinapidocs.docs.apiary.io/#reference/0/language/change-language

        :param language: Language string - see get_languages() for values
        :type language: string

        .. code:: python

            client.update_language(language='zh_CN')

        :returns: None

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'lang': language
        }
        return self._post('user/change-lang', True, data=data)

    def get_user(self):
        """Get user info

        https://kucoinapidocs.docs.apiary.io/#reference/0/user/get-user-info

        .. code:: python

            user = client.get_user()

        :returns: ApiResponse

        .. code:: python

            {
                "referrer_code": "jkLmne",
                "photoCredentialValidated": true,
                "videoValidated": false,
                "language": "en_US",
                "currency": "USD",
                "oid": "59663b126732d50be3ac8bcb",
                "baseFeeRate": 1,
                "hasCredential": true,
                "credentialNumber": "5103**********0013",
                "phoneValidated": true,
                "phone": "18******139",
                "credentialValidated": true,
                "googleTwoFaBinding": true,
                "nickname": null,
                "name": "*醇",
                "hasTradePassword": true,
                "emailValidated": true,
                "email": "robert2041@163.com"
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('user/info', True)

    # Invitation Endpoints

    def get_invite_count(self):
        """Get invite count

        https://kucoinapidocs.docs.apiary.io/#reference/0/inviting-promotion/get-inviting-count

        .. code:: python

            user = client.get_invite_count()

        :returns: ApiResponse

        .. code:: python

            {
                "count": 20,
                "countTwo": 40,
                "countThree": 60
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('referrer/descendant/count', True)

    def get_reward_info(self, coin):
        """Get promotion reward info for a coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/inviting-promotion/get-promotion-reward-info

        :param coin: Name of coin to get reward info
        :type coin: string

        .. code:: python

            user = client.get_reward_info('NEO')

        :returns: ApiResponse

        .. code:: python

            {
                "assignedCount": 0,
                "drawingCount": 0,
                "grantCountDownSeconds": 604800
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'coin': coin
        }

        return self._get('account/promotion/info', True, data=data)

    def get_reward_summary(self, coin):
        """Get promotion reward summary for a coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/inviting-promotion/get-promotion-reward-summary

        :param coin: Name of coin to get reward summary
        :type coin: string

        .. code:: python

            user = client.get_reward_summary('NEO')

        :returns: ApiResponse

        .. code:: python

            [
                {
                    "oid": "59cf3449bc2ec0820158ea4d",
                    "coin": "BTC",
                    "amount": 0.05978693,
                    "count": 128,
                    "userOid": "59c3aa5cbc2ec035341689d8",
                    "lastGrantAt": 1507532458000,
                    "createdAt": 1506704761000,
                    "updatedAt": 1507532458000,
                    "undrawnAmount": 0.05978693,
                    "drawnAmount": 0
                }
            ]

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'coin': coin
        }

        return self._get('account/promotion/sum', True, data=data)

    # Asset Endpoints

    def get_deposit_address(self, coin):
        """Get deposit address for a coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/assets-operation/get-coin-deposit-address

        :param coin: Name of coin
        :type coin: string

        .. code:: python

            address = client.get_deposit_address('NEO')

        :returns: ApiResponse

        .. code:: python

            {
                "oid": "598aeb627da3355fa3e851ca",
                "address": "598aeb627da3355fa3e851ca",
                "context": null,
                "userOid": "5969ddc96732d54312eb960e",
                "coinType": "CNY",
                "createdAt": 1502276446000,
                "deletedAt": null,
                "updatedAt": 1502276446000,
                "lastReceivedAt": 1502276446000
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('account/{}/wallet/address'.format(coin), True)

    def create_withdrawal(self, coin, amount, address):
        """Get deposit address for a coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/assets-operation/create-withdrawal

        :param coin: Name of coin
        :type coin: string
        :param amount: Amount to withdraw
        :type amount: number
        :param address: Address to withdraw to
        :type address: string

        .. code:: python

            client.create_withdrawal('NEO', 20, '598aeb627da3355fa3e851')

        :returns: None

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'amount': amount,
            'address': address
        }

        return self._post('account/{}/withdraw/apply'.format(coin), True, data=data)

    def cancel_withdrawal(self, coin, txid):
        """Cancel a withdrawal

        https://kucoinapidocs.docs.apiary.io/#reference/0/assets-operation/cancel-withdrawal

        :param coin: Name of coin
        :type coin: string
        :param txid: Transaction id
        :type txid: string

        .. code:: python

            client.cancel_withdrawal('NEO', '598aeb627da3355fa3e851')

        :returns: None

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'txOid': txid
        }

        return self._get('account/{}/withdraw/cancel'.format(coin), True, data=data)

    def get_deposits(self, coin, status=None, limit=None, page=None):
        """Get deposit records for a coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/assets-operation/list-deposit-&-withdrawal-records

        :param coin: Name of coin
        :type coin: string
        :param status: optional - Status of deposit
        :type status: string
        :param limit: optional - Number of transactions
        :type limit: int
        :param page: optional - Page to fetch
        :type page: int

        .. code:: python

            deposits = client.get_deposits('NEO')

        :returns: ApiResponse

        .. code:: python

            {
                "datas": [
                    {
                        "fee": 1,
                        "oid": "5960957d07015669deca1254",
                        "type": "DEPOSIT",
                        "amount": 209,
                        "remark": "",
                        "status": "CANCEL",
                        "address": "aag",
                        "context": "",
                        "userOid": "TEST",
                        "coinType": "BTC",
                        "createdAt": 1499501950000,
                        "deletedAt": null,
                        "updatedAt": 1499502103000,
                        "outerWalletTxid": null
                    }
                ],
                "total": 7,
                "limit": 2,
                "pageNos": 4,
                "currPageNo": 1,
                "navigatePageNos": [
                    1,
                    2,
                    3,
                    4
                ],
                "coinType": "BTC",
                "type": null,
                "userOid": "TEST",
                "status": null,
                "firstPage": true,
                "lastPage": false,
                "startRow": 0
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'type': self.TRANSFER_DEPOSIT
        }
        if status:
            data['status'] = status
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('account/{}/wallet/records'.format(coin), True, data=data)

    def get_withdrawals(self, coin, status=None, limit=None, page=None):
        """Get withdrawal records for a coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/assets-operation/list-deposit-&-withdrawal-records

        :param coin: Name of coin
        :type coin: string
        :param status: optional - Status of withdrawal
        :type status: string
        :param limit: optional - Number of transactions
        :type limit: int
        :param page: optional - Page to fetch
        :type page: int

        .. code:: python

            withdrawals = client.get_withdrawals('NEO')

        :returns: ApiResponse

        .. code:: python

            {
                "datas": [
                    {
                        "fee": 1,
                        "oid": "5960957d07015669deca1254",
                        "type": "WITHDRAWAL",
                        "amount": 209,
                        "remark": "",
                        "status": "CANCEL",
                        "address": "aag",
                        "context": "",
                        "userOid": "TEST",
                        "coinType": "BTC",
                        "createdAt": 1499501950000,
                        "deletedAt": null,
                        "updatedAt": 1499502103000,
                        "outerWalletTxid": null
                    }
                ],
                "total": 7,
                "limit": 2,
                "pageNos": 4,
                "currPageNo": 1,
                "navigatePageNos": [
                    1,
                    2,
                    3,
                    4
                ],
                "coinType": "BTC",
                "type": null,
                "userOid": "TEST",
                "status": null,
                "firstPage": true,
                "lastPage": false,
                "startRow": 0
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'type': self.TRANSFER_WITHDRAWAL
        }
        if status:
            data['status'] = status
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('account/{}/wallet/records'.format(coin), True, data=data)

    def get_coin_balance(self, coin):
        """Get balance of a coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/assets-operation/get-balance-of-coin

        :param coin: Name of coin
        :type coin: string

        .. code:: python

            balance = client.get_coin_balance('KCS')

        :returns: ApiResponse

        .. code:: python

            {
                coinType: "BTC",
                balance: 1233214,
                freezeBalance: 321321
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('account/{}/balance'.format(coin), True)

    def get_all_balances(self):
        """Get all coin balances

        https://kucoinapidocs.docs.apiary.io/#reference/0/assets-operation/get-all-balance

        .. code:: python

            balances = client.get_all_balances()

        :returns: ApiResponse

        .. code:: python

            [
                {
                    coinType: "BTC",
                    balance: 1233214,
                    freezeBalance: 321321
                }
            ]

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('account/balance', True)

    # Trading Endpoints

    def create_order(self, symbol, order_type, price, amount):
        """Create an order

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/create-an-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_type: Buy or Sell
        :type order_type: string
        :param price: Name of coin
        :type price: string
        :param amount: Amount
        :type amount: string

        .. code:: python

            transaction = client.create_order('KCS-BTC', Client.SIDE_BUY, '0.01', '1000')

        :returns: ApiResponse

        .. code:: python

            {
                "orderOid": "596186ad07015679730ffa02"
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol,
            'type': order_type,
            'price': price,
            'amount': amount
        }

        return self._post('order', True, data=data)

    def create_buy_order(self, symbol, price, amount):
        """Create a buy order

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/create-an-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param price: Name of coin
        :type price: string
        :param amount: Amount
        :type amount: string

        .. code:: python

            transaction = client.create_buy_order('KCS-BTC', '0.01', '1000')

        :returns: ApiResponse

        .. code:: python

            {
                "orderOid": "596186ad07015679730ffa02"
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self.create_order(symbol, self.SIDE_BUY, price, amount)

    def create_sell_order(self, symbol, price, amount):
        """Create a sell order

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/create-an-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param price: Name of coin
        :type price: string
        :param amount: Amount
        :type amount: string

        .. code:: python

            transaction = client.create_sell_order('KCS-BTC', '0.01', '1000')

        :returns: ApiResponse

        .. code:: python

            {
                "orderOid": "596186ad07015679730ffa02"
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self.create_order(symbol, self.SIDE_SELL, price, amount)

    def get_active_orders(self, symbol):
        """Get list of active orders

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/list-active-orders

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            orders = client.get_active_orders('KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            {
                "SELL": [],
                "BUY": [
                    [
                        1499563694000,                  # time
                        "BUY",                          # type
                        38,                             # price
                        5,                              # amount
                        0,                              # deal amount
                        "596186ad07015679730ffa02"      # order oid
                    ],
                    [
                        1499563686000,
                        "BUY",
                        35,
                        5,
                        0,
                        "596186a007015679730ffa01"
                    ],
                    [
                        1499563699000,
                        "BUY",
                        22,
                        5,
                        0,
                        "596186b207015679730ffa03"
                    ]
                ]
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol
        }

        return self._get('order/active', True, data=data)

    def cancel_order(self, symbol, order_id, order_type):
        """Cancel an order

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/cancel-orders

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_id: Order id
        :type order_id: string
        :param order_type: Order type
        :type order_type: string

        .. code:: python

            orders = client.cancel_order('KCS-BTC', ')

        :returns: None

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol,
            'orderOid': order_id,
            'type': order_type
        }

        return self._post('cancel-order', True, data=data)

    def get_deal_orders(self, symbol, order_type, limit=None, page=None):
        """Get a list of deal orders with pagination

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/list-deal-orders

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_type: Order type
        :type order_type: string
        :param limit: optional - Number of deals
        :type limit: int
        :param page: optional - Page to fetch
        :type page: int

        .. code:: python

            orders = client.get_deal_orders('KCS-BTC', Client.SIDE_SELL, limit=10, page=2)

        :returns: ApiResponse

        .. code:: python

            {
                "datas": [
                    {
                        "oid": "59c47e7904dd275c7696ed15",
                        "dealPrice": 5040,
                        "orderOid": "59c47e7804dd275cd15773fc",
                        "direction": "BUY",
                        "amount": 100000000,
                        "dealValue": 5040,
                        "createdAt": 1506049657000
                    },
                    {
                        "oid": "59c3979104dd275c7696ec4d",
                        "dealPrice": 6510,
                        "orderOid": "59c3913d04dd275c76f2a10c",
                        "direction": "SELL",
                        "amount": 100000000,
                        "dealValue": 6510,
                        "createdAt": 1505990545000
                    }
                ],
                "total": 51,
                "limit": 12,
                "pageNos": 5,
                "currPageNo": 1,
                "navigatePageNos": [
                    1,
                    2,
                    3,
                    4,
                    5
                ],
                "userOid": "59bc96b89346432ce9cb7a8e",
                "direction": null,
                "startRow": 0,
                "firstPage": true,
                "lastPage": false
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol,
            'type': order_type
        }
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('deal-orders', True, data=data)

    # Market Endpoints

    def get_tick(self, symbol):
        """Get a symbol tick

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/tick(open)

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            orders = client.get_tick('KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            {
                "coinType": "KCS",
                "trading": true,
                "lastDealPrice": 5040,
                "buy": 5000,
                "sell": 5040,
                "coinTypePair": "BTC",
                "sort": 0,
                "feeRate": 0.001,
                "volValue": 308140577,
                "high": 6890,
                "datetime": 1506050394000,
                "vol": 5028739175025,
                "low": 5040,
                "changeRate": -0.2642
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol
        }

        return self._get('open/tick', False, data=data)

    def get_order_book(self, symbol, group=None, limit=None):
        """Get the order book for a symbol

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/order-books(open)

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param group:
        :type group: int
        :param limit: Depth to return
        :type limit: int

        .. code:: python

            orders = client.get_order_book('KCS-BTC', limit=50)

        :returns: ApiResponse

        .. code:: python

            {
                "SELL": [
                    [
                        20,     # price
                        5,      # amount
                        100     # volume
                    ],
                    [
                        19,
                        5,
                        95
                    ]
                ],
                "BUY": [
                    [
                        18,
                        5,
                        90
                    ],
                    [
                        17,
                        5,
                        85
                    ]
                ]
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol
        }
        if group:
            data['group'] = group
        if limit:
            data['limit'] = limit

        return self._get('open/orders', False, data=data)

    def get_buy_orders(self, symbol, group=None, limit=None):
        """Get the buy orders for a symbol

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/buy-order-books(open)

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param group: optional - not sure what this means
        :type group: int
        :param limit: optional - Depth to return
        :type limit: int

        .. code:: python

            orders = client.get_buy_orders('KCS-BTC', limit=50)

        :returns: ApiResponse

        .. code:: python

             [
                [
                    18,
                    5,
                    90
                ],
                [
                    17,
                    5,
                    85
                ]
            ]

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol
        }
        if group:
            data['group'] = group
        if limit:
            data['limit'] = limit

        return self._get('open/orders-buy', False, data=data)

    def get_sell_orders(self, symbol, group=None, limit=None):
        """Get the sell orders for a symbol

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/sell-order-books(open)

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param group: optional - not sure what this means
        :type group: int
        :param limit: optional - Depth to return
        :type limit: int

        .. code:: python

            orders = client.get_sell_orders('KCS-BTC', limit=50)

        :returns: ApiResponse

        .. code:: python

             [
                [
                    18,
                    5,
                    90
                ],
                [
                    17,
                    5,
                    85
                ]
            ]

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol
        }
        if group:
            data['group'] = group
        if limit:
            data['limit'] = limit

        return self._get('open/orders-sell', False, data=data)

    def get_recent_orders(self, symbol, limit=None, since=None):
        """Get recent orders

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/recently-deal-orders(open)

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param limit: optional - Number of orders to return. Limit overrides since parameter
        :type limit: int
        :param since: optional - timestamp unsure how this works, tried s and ms values with no effect
        :type since: int

        .. code:: python

            orders = client.get_recent_trades('KCS-BTC')

            # optional limit parameter
            orders = client.get_recent_trades('KCS-BTC', limit=20)

        :returns: ApiResponse

        .. code:: python

            [
                [
                    1506037604000,      # timestamp
                    "SELL",             # order type
                    5210,               # price
                    48600633397,        # amount
                    2532093             # volume
                ],
                [
                    1506037604000,
                    "SELL",
                    5800,
                    10227827586,
                    593214
                ]

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol
        }
        if limit:
            data['limit'] = limit
        if since:
            data['since'] = since

        return self._get('open/deal-orders', False, data=data)

    def get_trading_symbols(self):
        """Get list of trading symbols

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/list-trading-symbols(open)

        .. code:: python

            coins = client.get_trading_symbols()

        :returns: ApiResponse

        .. code:: python

            [
                {
                    "coinType": "KCS",
                    "trading": true,
                    "lastDealPrice": 4500,
                    "buy": 4120,
                    "sell": 4500,
                    "coinTypePair": "BTC",
                    "sort": 0,
                    "feeRate": 0.001,
                    "volValue": 324866889,
                    "high": 6890,
                    "datetime": 1506051488000,
                    "vol": 5363831663913,
                    "low": 4500,
                    "changeRate": -0.3431
                },
                {
                    "coinType": "KNC",
                    "trading": true,
                    "lastDealPrice": null,
                    "buy": 1000000,
                    "sell": null,
                    "coinTypePair": "BTC",
                    "sort": 1,
                    "feeRate": 0.001,
                    "volValue": 0,
                    "high": null,
                    "datetime": 1506051488000,
                    "vol": 0,
                    "low": null,
                    "changeRate": null
                }
            ]

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('market/open/symbols')

    def get_trending_coins(self):
        """Get list of trending coins

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/list-trendings(open)

        .. code:: python

            coins = client.get_trending_coins()

        :returns: ApiResponse

        .. code:: python

            [
                {
                    "coinPair": "BTM-BTC",
                    "deals": [
                        [
                            1506049200000,
                            null
                        ],
                        [
                            1506045600000,
                            null
                        ],
                        [
                            1506042000000,
                            null
                        ],
                        [
                            1506038400000,
                            1260
                        ]
                    ]
                }
            ]

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('market/open/coins-trending')

    def get_kline_data(self, symbol, resolution, from_time, to_time, limit=None):
        """Get kline data

        Validates resolution value is correct

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param resolution: Data resolution from RESOLUTION_* types
        :type resolution: string
        :param from_time: From timestamp in seconds
        :type from_time: int
        :param to_time: To timestamp in seconds
        :type to_time: int
        :param limit: optional - Number of results
        :type limit: int

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/get-kline-data(open)

        .. code:: python

            klines = client.get_kline_data('KCS-BTC', Client.RESOLUTION_1MINUTE, 1507479171, 1510278278)

        :returns: ApiResponse

        .. code:: python

            [
                {
                    "coinPair": "BTM-BTC",
                    "deals": [
                        [
                            1506049200000,
                            null
                        ],
                        [
                            1506045600000,
                            null
                        ],
                        [
                            1506042000000,
                            null
                        ],
                        [
                            1506038400000,
                            1260
                        ]
                    ]
                }
            ]

        :raises: KucoinResponseException,  KucoinAPIException, KucoinResolutionException

        """

        try:
            resolution = self._resolution_map[resolution]
        except KeyError:
            raise KucoinResolutionException('Invalid resolution passed')

        data = {
            'symbol': symbol,
            'resolution': resolution,
            'from': from_time,
            'to': to_time
        }
        if limit:
            data['limit'] = limit

        return self._get('open/kline', False, data=data)

    def get_kline_config_tv(self):
        """Get kline config (TradingView version)

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/get-kline-config(open,-tradingview-version)

        .. code:: python

            config = client.get_kline_config_tv()

        :returns: ApiResponse

        .. code:: python

            {
                "supports_marks": false,
                "supports_time": true,
                "supports_search": true,
                "supports_group_request": false,
                "supported_resolutions": [
                    "1",
                    "5",
                    "15",
                    "30",
                    "60",
                    "480",
                    "D",
                    "W"
                ]
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('open/chart/config')

    def get_symbol_tv(self, symbol):
        """Get symbol data (TradingView version)

        Note this function doesn't seem to be implemented by Kucoin yet.

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/get-symbol(open,-tradingview-version)

        .. code:: python

            symbol = client.get_symbol_tv('KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            {
                "ticker": "KCS-BTC",
                "minmov": 1,
                "minmov2": 0,
                "session": "24x7",
                "timezone": "Asia/Shanghai",
                "has_intraday": true,
                "description": "KCS-BTC",
                "supported_resolutions": [
                    "1",
                    "5",
                    "15",
                    "30",
                    "60",
                    "480",
                    "D",
                    "W"
                ],
                "type": "stock",
                "currency_code": "BTC",
                "exchange-listed": "",
                "volume_precision": 8,
                "pointvalue": 1,
                "name": "KCS-BTC",
                "exchange-traded": "",
                "pricescale": 100000000,
                "has_no_volume": true
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol
        }

        return self._get('open/chart/symbol', False, data=data)

    def get_kline_data_tv(self, symbol, resolution, from_time, to_time):
        """Get kline data (TradingView version)

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param resolution: Data resolution from RESOLUTION_* types
        :type resolution: string
        :param from_time: From timestamp in seconds
        :type from_time: int
        :param to_time: To timestamp in seconds
        :type to_time: int

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/get-kline-data(open,-tradingview-version)

        .. code:: python

            klines = client.get_kline_data_tv('KCS-BTC', Client.RESOLUTION_1MINUTE, 1507479171, 1510278278)

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "OK",
                "s": "ok",
                "c": [
                    0.00008999,
                    0.0001195,
                    0.00012488,
                    0.00009231,
                    0.00008483,
                    0.00009245,
                    0.00008964,
                    0.00006934,
                    0.0000836,
                    0.00009188
                ],
                "t": [
                    1507201200,
                    1507287600,
                    1507374000,
                    1507460400,
                    1507546800,
                    1507633200,
                    1507719600,
                    1507806000,
                    1507892400,
                    1507978800
                ],
                "v": [
                    677184.95840835,
                    1383918.84700098,
                    756304.77228774,
                    633909.71537665,
                    436374.60456221,
                    425808.74766085,
                    469397.21371071,
                    537288.87941776,
                    573752.12538949,
                    590450.62919965
                ],
                "h": [
                    0.000092,
                    0.0001214,
                    0.000125,
                    0.00012468,
                    0.000103,
                    0.0000932,
                    0.0001175,
                    0.00009056,
                    0.0000858,
                    0.00009368
                ],
                "l": [
                    0.0000671,
                    0.0000886,
                    0.00010998,
                    0.00008312,
                    0.00008315,
                    0.00008,
                    0.00008101,
                    0.000063,
                    0.000068,
                    0.0000792
                ],
                "o": [
                    0.0000671,
                    0.00009,
                    0.00011912,
                    0.00012462,
                    0.00009544,
                    0.00008381,
                    0.00009245,
                    0.00008846,
                    0.00006875,
                    0.00008349
                ]
            }

        :raises: KucoinResponseException,  KucoinAPIException

        """

        data = {
            'symbol': symbol,
            'resolution': resolution,
            'from': from_time,
            'to': to_time
        }

        return self._get('open/chart/history', False, data=data)

    def get_coin_list(self):
        """Get a list of coins with trade and withdrawal information

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/list-coins(open)

        .. code:: python

            coins = client.get_coin_list()

        :returns: ApiResponse

        .. code:: python

            [
                {
                    "withdrawMinFee": 100000,
                    "withdrawMinAmount": 200000,
                    "withdrawFeeRate": 0.001,
                    "name": "Bitcoin",
                    "tradePrecision": 7,
                    "pairs": "",
                    "coin": "BTC"
                },
                {
                    "withdrawMinFee": 3000000000,
                    "withdrawMinAmount": 5000000000,
                    "withdrawFeeRate": 0.001,
                    "name": "Bytom",
                    "tradePrecision": 4,
                    "pairs": "BTM-BTC",
                    "coin": "BTM"
                }
            ]

        :raises: KucoinResponseException,  KucoinAPIException

        """

        return self._get('market/open/coins-list')
