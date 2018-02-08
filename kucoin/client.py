# coding=utf-8

import base64
import hashlib
import hmac
import time
import requests

from .exceptions import KucoinAPIException, KucoinRequestException, KucoinResolutionException
from .helpers import date_to_seconds


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
    TRANSFER_STATUS_PENDING = 'PENDING'
    TRANSFER_STATUS_FINISHED = 'FINISHED'

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

            client = Client(api_key, api_secret)

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

            if 'success' in json and not json['success']:
                raise KucoinAPIException(response)

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

    # User API Endpoints

    def create_api_key(self):
        """Create a new API Key

        https://kucoinapidocs.docs.apiary.io/#reference/0/user-api-management/create-api-key

        .. code:: python

            result = client.create_api_key()

        :returns: API Response

        .. code-block:: python

            {
                "remark": null,
                "secret": "54e1a7f3-f5c0-47f2-bdce-f1d5124602e1",
                "enabled": true,
                "userOid": "59663b126732d50be3ac8bcb",
                "accessKey": "59c5ecfe18497f5394ded813",
                "createdAt": 1506143486528,
                "updatedAt": 1506143486528,
                "permissions": null
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        return self._post('api/create', True)

    def update_api_key(self, key, enabled=None, remark=None, permissions=None):
        """Update an API Key

        https://kucoinapidocs.docs.apiary.io/#reference/0/user-api-management/update-api-key

        :param key: API Key string
        :type key: string
        :param enabled: optional - Enable or disable key
        :type enabled: boolean
        :param remark: optional - Remark for API Key
        :type remark: string
        :param permissions: optional - Permissions for API Key
        :type permissions: string

        .. code:: python

            result = client.update_api_key("59c5ecfe18497f5394ded813", enabled=False)

        :returns: True on success

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {
            'key': key
        }
        if enabled is not None:
            data['enabled'] = enabled
        if remark:
            data['remark'] = remark
        if permissions:
            data['permissions'] = permissions

        return self._post('api/update', True, data=data)

    def get_api_keys(self):
        """Get list of API Keys

        https://kucoinapidocs.docs.apiary.io/#reference/0/user-api-management/list-api-key

        .. code:: python

            result = client.get_api_keys()

        :returns: API Response

        .. code-block:: python
            [
                {
                    "remark": null,
                    "secret": "*",  # display within 30 minutes after created
                    "enabled": true,
                    "userOid": "59663b126732d50be3ac8bcb",
                    "accessKey": "59c5ecfe18497f5394ded813",
                    "createdAt": 1506143487000,
                    "updatedAt": 1506143487000,
                    "permissions": null
                }
            ]

        :raises:  KucoinResponseException, KucoinAPIException

        """

        return self._get('api/list', True)

    def delete_api_key(self, key):
        """Update an API Key

        https://kucoinapidocs.docs.apiary.io/#reference/0/user-api-management/delete-api-key

        :param key: API Key string
        :type key: string

        .. code:: python

            result = client.delete_api_key("59c5ecfe18497f5394ded813")

        :returns: True on success

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {
            'key': key
        }

        return self._post('api/delete', True, data=data)

    # Currency Endpoints

    def get_currencies(self, coins=None):
        """List the exchange rate of coins

        https://kucoinapidocs.docs.apiary.io/#reference/0/currencies-plugin/list-exchange-rate-of-coins(open)

        :param coins: optional - Comma separated list of coins to get exchange rate for
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

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {}
        if coins:
            if type(coins) != list:
                coins = [coins]
            data['coins'] = ','.join(coins)

        return self._get('open/currencies', False, data=data)

    def set_default_currency(self, currency):
        """Set your default currency

        Get a list of available currency from the get_currencies call

        https://kucoinapidocs.docs.apiary.io/#reference/0/currencies-plugin/set-default-currency

        :param currency: Currency string e.g USD,CNY,JPY
        :type currency: string

        .. code:: python

            # call with no coins
            products = client.set_default_currency('USD')

        :returns: None

        """
        data = {
            'currency': currency
        }

        return self._post('user/change-currency', False, data=data)

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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

        """

        return self._get('referrer/descendant/count', True)

    def get_reward_info(self, coin=None):
        """Get promotion reward info all coins or an individual coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/inviting-promotion/get-promotion-reward-info

        :param coin: optional - Name of coin to get reward info
        :type coin: string

        .. code:: python

            # all coins
            user = client.get_reward_info('NEO')

            # specific coin
            user = client.get_reward_info('NEO')

        :returns: ApiResponse

        .. code:: python

            {
                "assignedCount": 0,
                "drawingCount": 0,
                "grantCountDownSeconds": 604800
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if coin:
            data['coin'] = coin

        return self._get('account/promotion/info', True, data=data)

    def get_reward_summary(self, coin=None):
        """Get promotion reward summary for all coins or a specific coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/inviting-promotion/get-promotion-reward-summary

        :param coin: optional - Name of coin to get reward summary
        :type coin: string

        .. code:: python

            # all coins
            user = client.get_reward_summary()

            # specific coin
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

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if coin:
            data['coin'] = coin

        return self._get('account/promotion/sum', True, data=data)

    def extract_invite_bonus(self, coin=None):
        """Extract the invitation bonus for all coins or a specific coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/invitation-bonus/extract-invitation-bonus

        :param coin: optional - Name of coin to extract the invitation bonus
        :type coin: string

        .. code:: python

            # all coins
            user = client.extract_invite_bonus()

            # specific coin
            user = client.extract_invite_bonus('KCS')

        :returns: ApiResponse

        .. code:: python

            {
                "count": 0  # The number of successful extracted
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if coin:
            data['coin'] = coin

        return self._post('account/promotion/draw', True, data=data)

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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

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
        :param status: optional - Status of deposit (FINISHED, CANCEL, PENDING)
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

        :raises: KucoinResponseException, KucoinAPIException

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
        :param status: optional - Status of withdrawal (FINISHED, CANCEL, PENDING)
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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

        """

        return self._get('account/{}/balance'.format(coin), True)

    def get_all_balances(self, limit=None, page=None):
        """Get all coin balances

        https://kucoinapidocs.docs.apiary.io/#reference/0/assets-operation/get-all-balance

        :param limit: optional - Number of balances default 12, max 20
        :type limit: int
        :param page: optional - Page to fetch
        :type page: int

        .. code:: python

            # get the default response
            balances = client.get_all_balances()

            # get a paged response
            balances = client.get_all_balances(limit=20, page=2)

        :returns: ApiResponse

        .. code:: python

            [
                {
                    coinType: "BTC",
                    balance: 1233214,
                    freezeBalance: 321321,
                    balanceStr: "1233214"
                    freezeBalanceStr: "321321"
                }
            ]

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('account/balances', True, data=data)

    def get_total_balance(self, currency='USD'):
        """Get total balance in your currency, USD by default

        :param currency: Currency string
        :type currency: str

        .. code:: python

            # get balance in USD
            balances = client.get_total_balance()

            # get balance in EUR
            balances = client.get_total_balance('EUR')

        :returns: float balance value

        :raises: Exception, KucoinResponseException, KucoinAPIException

        """

        # get balances
        balances = self.get_all_balances()
        # find unique coin names
        coins_csl = ','.join([b['coinType'] for b in balances])
        # get rates for these coins
        currency_res = self.get_currencies(coins_csl)
        rates = currency_res['rates']

        total = 0
        for b in balances:
            # ignore any coins of 0 value
            if b['balanceStr'] == '0.0' and b['freezeBalanceStr'] == '0.0':
                continue
            # ignore the coin if we don't have a rate for it
            if b['coinType'] not in rates:
                continue
            # add the value for this coin to the total
            try:
                total += (b['balance'] + b['freezeBalance']) * rates[b['coinType']][currency]
            except KeyError:
                raise Exception("Unknown currency:{}".format(currency))

        return total

    # Trading Endpoints

    def create_order(self, symbol, order_type, price, amount):
        """Create an order

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/create-an-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_type: BUY or SELL
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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

        """

        return self.create_order(symbol, self.SIDE_SELL, price, amount)

    def get_active_orders(self, symbol, kv_format=False):
        """Get list of active orders

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/list-active-orders

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param kv_format: optional - whether to return as kv format or not
        :type kv_format: bool

        .. code:: python

            orders = client.get_active_orders('KCS-BTC')

            # return orders in KV format
            orders_kv = client.get_active_orders('KCS-BTC', True)

        :returns: ApiResponse

        Non KV Format

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

        KV Format

            {
                "success": true,
                "code": "OK",
                "msg": "Operation succeeded.",
                "timestamp": 1508306965706,
                "data": {
                    "SELL": [
                        {
                            "oid": "59e59b279bd8d31d093d956e",
                            "type": "SELL",
                            "userOid": null,
                            "coinType": "KCS",
                            "coinTypePair": "BTC",
                            "direction": "SELL",
                            "price": 0.1,
                            "dealAmount": 0,
                            "pendingAmount": 100,
                            "createdAt": 1508219688000,
                            "updatedAt": 1508219688000
                        }
                    ],
                    "BUY": [
                        {
                            "oid": "59e42bf09bd8d374c9956caa",
                            "type": "BUY",
                            "userOid": null,
                            "coinType": "KCS",
                            "coinTypePair": "BTC",
                            "direction": "BUY",
                            "price": 0.00009727,
                            "dealAmount": 31.14503,
                            "pendingAmount": 16.94827,
                            "createdAt": 1508125681000,
                            "updatedAt": 1508125681000
                        }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {
            'symbol': symbol
        }

        path = 'order/active'
        if kv_format:
            path += '-map'

        return self._get(path, True, data=data)

    def cancel_order(self, order_id, order_type, symbol=None):
        """Cancel an order

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/cancel-orders

        Note: The Kucoin documentation is incorrect, the symbol parameter goes in the body not the query string

        :param order_id: Order id
        :type order_id: string
        :param order_type: Order type
        :type order_type: string
        :param symbol: optional - Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            client.cancel_order(1)

            client.cancel_order(1, 'KCS-BTC', 'BUY')

        :returns: None on success

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {
            'orderOid': order_id
        }

        if order_type:
            data['type'] = order_type
        if symbol:
            data['symbol'] = symbol

        return self._post('cancel-order', True, data=data)

    def cancel_all_orders(self, symbol=None, order_type=None):
        """Cancel all orders

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/cancel-all-orders

        Note: The Kucoin documentation is incorrect, the symbol parameter goes in the body not the query string

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_type: Order type
        :type order_type: string

        .. code:: python

            # cancel all active orders
            client.cancel_all_orders()

            # cancel all KCS-BTC Buy orders
            client.cancel_all_orders('KCS-BTC', 'BUY')

        :returns: None on success

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if order_type:
            data['type'] = order_type
        if symbol:
            data['symbol'] = symbol

        return self._post('order/cancel-all', True, data=data)

    def get_dealt_orders(self, symbol=None, order_type=None, limit=None, page=None, since=None, before=None):
        """Get a list of dealt orders with pagination

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/list-dealt-orders(merged)

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_type: Order type
        :type order_type: string
        :param limit: optional - Number of deals
        :type limit: int
        :param page: optional - Page to fetch
        :type page: int
        :param since: optional - Since timestamp filter
        :type since: int
        :param before: optional - Before timestamp filter
        :type before: int

        .. code:: python

            orders = client.get_dealt_orders(limit=10, page=2)

        :returns: ApiResponse

        .. code:: python

            {
                "total": 1416,
                "datas": [
                    {
                        "createdAt": 1508219588000,
                        "amount": 92.79323381,
                        "dealValue": 0.00927932,
                        "dealPrice": 0.0001,
                        "fee": 1e-8,
                        "feeRate": 0,
                        "oid": "59e59ac49bd8d31d09f85fa8",
                        "orderOid": "59e59ac39bd8d31d093d956a",
                        "coinType": "KCS",
                        "coinTypePair": "BTC",
                        "direction": "BUY",
                        "dealDirection": "BUY"
                    },
                    {
                        "createdAt": 1508219588000,
                        "amount": 92.79323381,
                        "dealValue": 0.00927932,
                        "dealPrice": 0.0001,
                        "fee": 1e-8,
                        "feeRate": 0,
                        "oid": "59e59ac49bd8d31d09f85fa7",
                        "orderOid": "59e41c949bd8d374c9956c74",
                        "coinType": "KCS",
                        "coinTypePair": "BTC",
                        "direction": "SELL",
                        "dealDirection": "BUY"
                    }
                ],
                "limit": 2,
                "page": 1
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if symbol:
            data['symbol'] = symbol
        if order_type:
            data['type'] = order_type
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page
        if since:
            data['since'] = since
        if before:
            data['before'] = before

        return self._get('order/dealt', True, data=data)

    def get_symbol_dealt_orders(self, symbol, order_type=None, limit=None, page=None):
        """Get a list of dealt orders for a specific symbol with pagination

        Does not return symbol info in response, unlike get_dealt_orders

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/list-dealt-orders(specific-symbol)

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_type: Order type
        :type order_type: string
        :param limit: optional - Number of deals
        :type limit: int
        :param page: optional - Page to fetch
        :type page: int

        .. code:: python

            orders = client.get_symbol_dealt_orders('KCS-BTC', Client.SIDE_SELL, limit=10, page=2)

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

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {
            'symbol': symbol
        }
        if order_type:
            data['type'] = order_type
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page

        return self._get('deal-orders', True, data=data)

    def get_order_details(self, symbol, order_type, limit=None, page=None, order_id=None):
        """Get order details

        https://kucoinapidocs.docs.apiary.io/#reference/0/trading/order-details

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_type: Order type
        :type order_type: string
        :param limit: optional - Number of deals
        :type limit: int
        :param page: optional - Page to fetch
        :type page: int
        :param order_id: optional - orderOid value
        :type order_id: int

        .. code:: python

            orders = client.get_order_details('KCS-BTC', Client.SIDE_SELL)

        :returns: ApiResponse

        .. code:: python

            {
                "coinType": "KCS",
                "dealValueTotal": 0.00938022,
                "dealPriceAverage": 0.0001009,
                "feeTotal": 2e-8,
                "userOid": "5969ddc96732d54312eb960e",
                "dealAmount": 0,
                "dealOrders": {
                    "total": 709,
                    "firstPage": true,
                    "lastPage": false,
                    "datas": [
                        {
                            "amount": 1,
                            "dealValue": 0.0001009,
                            "fee": 1e-8,
                            "dealPrice": 0.0001009,
                            "feeRate": 0
                        },
                        {
                            "amount": 92.79323381,
                            "dealValue": 0.00927932,
                            "fee": 1e-8,
                            "dealPrice": 0.0001,
                            "feeRate": 0
                        }
                    ],
                    "currPageNo": 1,
                    "limit": 2,
                    "pageNos": 355
                },
                "coinTypePair": "BTC",
                "orderPrice": 0.0001067,
                "type": "SELL",
                "orderOid": "59e41cd69bd8d374c9956c75",
                "pendingAmount": 187.34
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {
            'symbol': symbol,
            'type': order_type
        }
        if limit:
            data['limit'] = limit
        if page:
            data['page'] = page
        if order_id:
            data['orderOid'] = order_id

        return self._get('/order/detail', True, data=data)

    # Market Endpoints

    def get_tick(self, symbol=None):
        """Get all ticks or a symbol tick

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/tick(open)

        :param symbol: optional - Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            # get all ticks
            ticks = client.get_tick()

            tick = client.get_tick('KCS-BTC')

        :returns: ApiResponse

        Without a symbol param

        .. code:: python

            [
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
            ]

        With a symbol param

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

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if symbol:
            data['symbol'] = symbol

        return self._get('open/tick', False, data=data)

    def get_order_book(self, symbol, group=None, limit=None):
        """Get the order book for a symbol

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/order-books(open)

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param group: optional - sets the price display precision - valid values (1-8)
        :type group: int
        :param limit: optional - depth to return
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

        :raises: KucoinResponseException, KucoinAPIException

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
        :param group: optional - sets the price display precision - valid values (1-8)
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

        :raises: KucoinResponseException, KucoinAPIException

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
        :param group: optional - sets the price display precision - valid values (1-8)
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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {
            'symbol': symbol
        }
        if limit:
            data['limit'] = limit
        if since:
            data['since'] = since

        return self._get('open/deal-orders', False, data=data)

    def get_trading_markets(self):
        """Get list of trading markets

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/list-trading-markets(open)

        .. code:: python

            coins = client.get_trading_markets()

        :returns: ApiResponse

        .. code:: python

            [
                "BTC",
                "ETH",
                "NEO",
                "USDT"
            ]

        :raises: KucoinResponseException, KucoinAPIException

        """

        return self._get('open/markets')

    def get_trading_symbols(self, market=None):
        """Get list of trading symbols for an optional market

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/list-trading-symbols(open)

        :param market: Name of market e.g. BTC
        :type market: string

        .. code:: python

            # get all trading symbols
            coins = client.get_trading_symbols()

            # get KCS trading symbols
            coins = client.get_trading_symbols('KCS)

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

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if market:
            data['market'] = market

        return self._get('market/open/symbols', False, data=data)

    def get_trending_coins(self, market=None):
        """Get list of trending coins for an optional market

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/list-trendings(open)

        :param market: Name of market e.g. BTC
        :type market: string

        .. code:: python

            # get all trending coins
            coins = client.get_trending_coins()

            # get trending coins for BTC
            coins = client.get_trending_coins('BTC')

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

        :raises: KucoinResponseException, KucoinAPIException

        """
        data = {}
        if market:
            data['market'] = market

        return self._get('market/open/coins-trending', False, data=data)

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

        :raises: KucoinResponseException, KucoinAPIException, KucoinResolutionException

        """

        try:
            resolution = self._resolution_map[resolution]
        except KeyError:
            raise KucoinResolutionException('Invalid resolution passed')

        data = {
            'symbol': symbol,
            'type': resolution,
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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

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

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {
            'symbol': symbol,
            'resolution': resolution,
            'from': from_time,
            'to': to_time
        }

        return self._get('open/chart/history', False, data=data)

    def get_historical_klines_tv(self, symbol, interval, start_str, end_str=None):
        """Get Historical Klines in OHLCV format (Trading View)

        See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Trading View Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format
        :type start_str: str
        :param end_str: optional - end date string in UTC format
        :type end_str: str

        .. code:: python

            klines = client.get_historical_klines_tv('KCS-BTC', Client.RESOLUTION_1MINUTE, '1 hour ago UTC')

            # fetch 30 minute klines for the last month of 2017
            klines = client.get_historical_klines_tv("NEO-BTC", Client.RESOLUTION_30MINUTES, "1 Dec, 2017", "1 Jan, 2018"))

            # fetch weekly klines since it listed
            klines = client.get_historical_klines_tv("XRP-BTC", Client.RESOLUTION_1WEEK, "1 Jan, 2017"))

        :return: list of OHLCV values

        """

        # init our array for klines
        klines = []

        # convert our date strings to seconds
        start_ts = date_to_seconds(start_str)

        # if an end time was not passed we need to use now
        if end_str is None:
            end_str = 'now UTC'
        end_ts = date_to_seconds(end_str)

        kline_res = self.get_kline_data_tv(symbol, interval, start_ts, end_ts)

        # check if we got a result
        if 't' in kline_res and len(kline_res['t']):
            # now convert this array to OHLCV format and add to the array
            for i in range(1, len(kline_res['t'])):
                klines.append((
                    kline_res['t'][i],
                    kline_res['o'][i],
                    kline_res['h'][i],
                    kline_res['l'][i],
                    kline_res['c'][i],
                    kline_res['v'][i]
                ))

        # finally return our converted klines
        return klines

    def get_coin_info(self, coin=None):
        """Get info about all coins or a coin

        https://kucoinapidocs.docs.apiary.io/#reference/0/market/get-coin-info(open)

        .. code:: python

            # all coin info
            info = client.get_coin_info()

            # EOS coin info
            info = client.get_coin_info('EOS')

        :returns: ApiResponse

        .. code:: python

            {
                "withdrawMinFee": 100000,
                "withdrawMinAmount": 200000,
                "withdrawFeeRate": 0.001,
                "confirmationCount": 12,
                "name": "Bitcoin",
                "tradePrecision": 7,
                "coin": "BTC",
                "infoUrl": null,
                "enableWithdraw": true,
                "enableDeposit": true,
                "depositRemark": "",
                "withdrawRemark": ""
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if coin:
            data['coin'] = coin

        return self._get('market/open/coin-info', False, data=data)

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

        :raises: KucoinResponseException, KucoinAPIException

        """

        return self._get('market/open/coins')
