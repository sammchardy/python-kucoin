from .exceptions import (
    KucoinAPIException,
    KucoinRequestException,
    MarketOrderException,
    LimitOrderException,
)
from .utils import flat_uuid

from .async_client_base import AsyncClientBase


class AsyncClient(AsyncClientBase):
    def __init__(
        self,
        api_key=None,
        api_secret=None,
        passphrase=None,
        sandbox=False,
        requests_params=None,
    ):
        """Kucoin API Client constructor

        https://docs.kucoin.com/

        :param api_key: Api Token Id
        :type api_key: string
        :param api_secret: Api Secret
        :type api_secret: string
        :param passphrase: Api Passphrase used to create API
        :type passphrase: string
        :param sandbox: (optional) Use the sandbox endpoint or not (default False)
        :type sandbox: bool
        :param requests_params: (optional) Dictionary of requests params to use for all calls
        :type requests_params: dict.

        .. code:: python

            client = Client(api_key, api_secret, api_passphrase)

        """
        super().__init__(api_key, api_secret, passphrase, sandbox, requests_params)

    async def get_timestamp(self, **params):
        """Get the server timestamp

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-server-time

        :return: response timestamp in ms

        """
        return await self._get("timestamp", data=params)

    async def futures_get_timestamp(self, **params):
        """Get the futures server timestamp

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-server-time

        :return: response timestamp in ms

        """
        return await self._get("timestamp", is_futures=True, data=params)

    async def get_status(self, **params):
        """Get the service status

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-service-status

        .. code:: python

            currencies = client.get_status()

        :returns: API Response

        .. code-block:: python
            {
                "status": "open",                //open, close, cancelonly
                "msg":  "upgrade match engine"   //remark for operation
            }

        """
        return await self._get("status", data=params)

    async def futures_get_status(self, **params):
        """Get the futures service status

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-service-status

        .. code:: python

            currencies = client.futures_get_status()

        :returns: API Response

        .. code-block:: python
            {
                "status": "open",                //open, close, cancelonly
                "msg":  "upgrade match engine"   //remark for operation
            }

        """
        return await self._get("status", is_futures=True, data=params)

    async def get_announcements(
        self,
        page=None,
        limit=None,
        ann_type=None,
        lang=None,
        start=None,
        end=None,
        **params,
    ):
        """Get a list of the latest news announcements

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-announcements

        :param page: (optional) Current page
        :type page: int
        :param limit: (optional) Number of results to return
        :type limit: int
        :param ann_type: (optional) Announcement type: latest-announcements, activities, new-listings, product-updates, vip, maintenance-updates, product-updates, delistings, others, api-campaigns (default latest-announcements)
        :type ann_type: string
        :param lang: (optional) Language (default is en_US): zh_HK - Chinese (Hong Kong), ja_JP - Japanese (Japan), ko_KR - Korean (Korea), en_US - English, pl_PL - Polish (Poland), es_ES - Spanish (Spain), fr_FR - French (France), ar_AE - Arabic (Egypt), it_IT - Italian (Italy), id_ID - Indonesian (Indonesia), nl_NL - Dutch (Netherlands), pt_PT - Portuguese (Brazil), vi_VN - Vietnamese (Vietnam), de_DE - German (Germany), tr_TR - Turkish (Turkey), ms_MY - Malay (Malaysia), ru_RU - Russian (Russia), th_TH - Thai (Thailand), hi_IN - Hindi (India), bn_BD - Bengali (Bangladesh), fil_PH - Filipino (Philippines), ur_PK - Urdu (Pakistan).
        :type lang: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string

        .. code:: python

            accounts = client.get_announcements()
            accounts = client.get_announcements(page=2, lang='ja_JP')

        :returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": {
                    "totalNum": 198,
                    "items": [
                        {
                            "annId": 131185,
                            "annTitle": "Announcement of KuCoin Futures System Upgrade",
                            "annType": [
                                "latest-announcements",
                                "futures-announcements"
                            ],
                            "annDesc": "Announcement of KuCoin Futures System Upgrade",
                            "cTime": 1730798882000,
                            "language": "en_US",
                            "annUrl": "https://www.kucoin.com/announcement/announcement-of-kucoin-futures-system-upgrade-2024-11-11?lang=en_US"
                        }
                    ],
                    "currentPage": 2,
                    "pageSize": 1,
                    "totalPage": 198
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {}
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit
        if ann_type:
            data["annType"] = ann_type
        if lang:
            data["lang"] = lang
        if start:
            data["startTime"] = start
        if end:
            data["endTime"] = end

        return await self._get(
            "announcements",
            False,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    # Currency Endpoints

    async def get_currencies(self):
        """List known currencies

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-currency-list

        .. code:: python

            currencies = client.get_currencies()

        :returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": [
                    {
                        "currency": "BTC",
                        "name": "BTC",
                        "fullName": "Bitcoin",
                        "precision": 8,
                        "confirms": null,
                        "contractAddress": null,
                        "isMarginEnabled": true,
                        "isDebitEnabled": true,
                        "chains": [
                            {
                                "chainName" : "BTC",
                                "withdrawalMinFee" : "0.001",
                                "withdrawalMinSize" : "0.0012",
                                "withdrawFeeRate" : "0",
                                "depositMinSize" : "0.0002",
                                "isWithdrawEnabled" : true,
                                "isDepositEnabled" : true,
                                "preConfirms" : 1,
                                "contractAddress" : "",
                                "chainId" : "btc",
                                "confirms" : 3
                            },
                            {
                                "chainName" : "KCC",
                                "withdrawalMinFee" : "0.00002",
                                "withdrawalMinSize" : "0.0008",
                                "withdrawFeeRate" : "0",
                                "depositMinSize" : null,
                                "isWithdrawEnabled" : true,
                                "isDepositEnabled" : true,
                                "preConfirms" : 20,
                                "contractAddress" : "0xfa93c12cd345c658bc4644d1d4e1b9615952258c",
                                "chainId" : "kcc",
                                "confirms" : 20
                            },
                            {
                                "chainName" : "BTC-Segwit",
                                "withdrawalMinFee" : "0.0005",
                                "withdrawalMinSize" : "0.0008",
                                "withdrawFeeRate" : "0",
                                "depositMinSize" : "0.0002",
                                "isWithdrawEnabled" : false,
                                "isDepositEnabled" : true,
                                "preConfirms" : 2,
                                "contractAddress" : "",
                                "chainId" : "bech32",
                                "confirms" : 2
                            }
                        ]
                    }
                ]
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        return await self._get("currencies", False, api_version=self.API_VERSION3)

    async def get_currency(self, currency, chain=None, **params):
        """Get single currency detail

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-currency-detail

        :param currency: Currency code
        :type currency: string
        :param chain: (optional) Chain name. The available value for USDT are OMNI, ERC20, TRC20.
        :type chain: string

        .. code:: python

            # call with no coins
            currency = client.get_currency('BTC')
            currency = client.get_currency('BTC', 'ERC20')

        :returns: API Response

        .. code-block:: python

            {
                "data" : {
                    "isMarginEnabled" : true,
                    "chains" : [
                        {
                            "chainName" : "BTC",
                            "withdrawalMinFee" : "0.001",
                            "withdrawalMinSize" : "0.0012",
                            "withdrawFeeRate" : "0",
                            "depositMinSize" : "0.0002",
                            "isWithdrawEnabled" : true,
                            "isDepositEnabled" : true,
                            "preConfirms" : 1,
                            "contractAddress" : "",
                            "chainId" : "btc",
                            "confirms" : 3
                        },
                        {
                            "chainName" : "KCC",
                            "withdrawalMinFee" : "0.00002",
                            "withdrawalMinSize" : "0.0008",
                            "withdrawFeeRate" : "0",
                            "depositMinSize" : null,
                            "isWithdrawEnabled" : true,
                            "isDepositEnabled" : true,
                            "preConfirms" : 20,
                            "contractAddress" : "0xfa93c12cd345c658bc4644d1d4e1b9615952258c",
                            "chainId" : "kcc",
                            "confirms" : 20
                        },
                        {
                            "chainName" : "BTC-Segwit",
                            "withdrawalMinFee" : "0.0005",
                            "withdrawalMinSize" : "0.0008",
                            "withdrawFeeRate" : "0",
                            "depositMinSize" : "0.0002",
                            "isWithdrawEnabled" : false,
                            "isDepositEnabled" : true,
                            "preConfirms" : 2,
                            "contractAddress" : "",
                            "chainId" : "bech32",
                            "confirms" : 2
                        }
                    ],
                    "contractAddress" : null,
                    "isDebitEnabled" : true,
                    "fullName" : "Bitcoin",
                    "precision" : 8,
                    "currency" : "BTC",
                    "name" : "BTC",
                    "confirms" : null
                },
                "code" : "200000"
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency}

        if chain:
            data["chain"] = chain

        return await self._get(
            "currencies/{}".format(currency),
            False,
            api_version=self.API_VERSION3,
            data=dict({"chain": chain}, **params),
        )

    # Market Endpoints

    async def get_symbols(self, market=None, **params):
        """Get a list of available currency pairs for trading.

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-symbols-list

        :param market: (optional) Name of market e.g. BTC
        :type market: string

        .. code:: python

            symbols = client.get_symbols()
            symbols = client.get_symbols('USDS')

        :returns: ApiResponse

        .. code:: python

            [
                {
                    "symbol": "XLM-USDT",
                    "name": "XLM-USDT",
                    "baseCurrency": "XLM",
                    "quoteCurrency": "USDT",
                    "feeCurrency": "USDT",
                    "market": "USDS",
                    "baseMinSize": "0.1",
                    "quoteMinSize": "0.01",
                    "baseMaxSize": "10000000000",
                    "quoteMaxSize": "99999999",
                    "baseIncrement": "0.0001",
                    "quoteIncrement": "0.000001",
                    "priceIncrement": "0.000001",
                    "priceLimitRate": "0.1",
                    "minFunds": "0.1",
                    "isMarginEnabled": true,
                    "enableTrading": true
                },
                {
                    "symbol": "VET-USDT",
                    "name": "VET-USDT",
                    "baseCurrency": "VET",
                    "quoteCurrency": "USDT",
                    "feeCurrency": "USDT",
                    "market": "USDS",
                    "baseMinSize": "10",
                    "quoteMinSize": "0.01",
                    "baseMaxSize": "10000000000",
                    "quoteMaxSize": "99999999",
                    "baseIncrement": "0.0001",
                    "quoteIncrement": "0.000001",
                    "priceIncrement": "0.0000001",
                    "priceLimitRate": "0.1",
                    "minFunds": "0.1",
                    "isMarginEnabled": true,
                    "enableTrading": true
                }
            ]

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if market:
            data["market"] = market

        return await self._get(
            "symbols", False, api_version=self.API_VERSION2, data=dict(data, **params)
        )

    async def get_symbol(self, symbol=None, **params):
        """Get a symbol details for trading.

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-symbol-detail

        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            symbol = client.get_symbol('XLM-USDT')

        :returns: ApiResponse

        .. code:: python

            {
                "data" : {
                    "quoteMinSize" : "0.1",
                    "quoteCurrency" : "USDT",
                    "feeCurrency" : "USDT",
                    "symbol" : "BTC-USDT",
                    "market" : "USDS",
                    "baseMaxSize" : "10000000000",
                    "baseIncrement" : "0.00000001",
                    "quoteIncrement" : "0.000001",
                    "priceIncrement" : "0.1",
                    "priceLimitRate" : "0.1",
                    "minFunds" : "0.1",
                    "isMarginEnabled" : true,
                    "enableTrading" : true,
                    "baseCurrency" : "BTC",
                    "baseMinSize" : "0.00001",
                    "name" : "BTC-USDT",
                    "quoteMaxSize" : "99999999"
                },
                "code" : "200000"
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if symbol:
            data["symbol"] = symbol

        return await self._get(
            "symbol", False, api_version=self.API_VERSION2, data=dict(data, **params)
        )

    async def get_ticker(self, symbol, **params):
        """Get symbol ticker

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-ticker

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            ticker = client.get_ticker('ETH-BTC')

        :returns: ApiResponse

        .. code:: python

            {
                "sequence": "1550467636704",
                "price": "0.03715005",
                "size": "0.17",
                "bestAsk": "0.03715004",
                "bestAskSize": "1.788",
                "bestBid": "0.03710768",
                "bestBidSize": "3.803",
                "time": 1550653727731
            }

        :raises: KucoinResponseException, KucoinAPIException

        """
        data = {"symbol": symbol}
        return await self._get("market/orderbook/level1", False, data=dict(data, **params))

    async def get_tickers(self):
        """Get symbol tickers

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-all-tickers

        .. code:: python

            tickers = client.get_tickers()

        :returns: ApiResponse

        .. code:: python

            {
                "time": 1602832092060,
                "ticker": [
                    {
                    "symbol": "BTC-USDT", // symbol
                    "symbolName": "BTC-USDT", // Name of trading pairs, it would change after renaming
                    "buy": "11328.9", // bestAsk
                    "sell": "11329", // bestBid
                    "bestBidSize": "0.1",
                    "bestAskSize": "1",
                    "changeRate": "-0.0055", // 24h change rate
                    "changePrice": "-63.6", // 24h change price
                    "high": "11610", // 24h highest price
                    "low": "11200", // 24h lowest price
                    "vol": "2282.70993217", // 24h volume，the aggregated trading volume in BTC
                    "volValue": "25984946.157790431", // 24h total, the trading volume in quote currency of last 24 hours
                    "last": "11328.9", // last price
                    "averagePrice": "11360.66065903", // 24h average transaction price yesterday
                    "takerFeeRate": "0.001", // Basic Taker Fee
                    "makerFeeRate": "0.001", // Basic Maker Fee
                    "takerCoefficient": "1", // Taker Fee Coefficient
                    "makerCoefficient": "1" // Maker Fee Coefficient
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """
        return await self._get("market/allTickers", False)

    async def get_24hr_stats(self, symbol, **params):
        """Get 24hr stats for a symbol. Volume is in base currency units. open, high, low are in quote currency units.

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-24hr-stats

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            stats = client.get_24hr_stats('ETH-BTC')

        :returns: ApiResponse

        .. code:: python

            {
                "time": 1602832092060, // time
                "symbol": "BTC-USDT", // symbol
                "buy": "11328.9", // bestAsk
                "sell": "11329", // bestBid
                "changeRate": "-0.0055", // 24h change rate
                "changePrice": "-63.6", // 24h change price
                "high": "11610", // 24h highest price
                "low": "11200", // 24h lowest price
                "vol": "2282.70993217", // 24h volume the aggregated trading volume in BTC
                "volValue": "25984946.157790431", // 24h total, the trading volume in quote currency of last 24 hours
                "last": "11328.9", // last price
                "averagePrice": "11360.66065903", // 24h average transaction price yesterday
                "takerFeeRate": "0.001", // Basic Taker Fee
                "makerFeeRate": "0.001", // Basic Maker Fee
                "takerCoefficient": "1", // Taker Fee Coefficient
                "makerCoefficient": "1" // Maker Fee Coefficient
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get("market/stats", False, data=dict(data, **params))

    async def get_markets(self):
        """Get supported market list

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-market-list

        .. code:: python

            markets = client.get_markets()

        :returns: ApiResponse

        .. code:: python

            {
                "data": [
                    "USDS", //SC has been changed to USDS
                    "BTC",
                    "KCS",
                    "ALTS", //ALTS market includes ETH, NEO, TRX
                    "NFT-ETF",
                    "FIAT",
                    "DeFi",
                    "NFT",
                    "Metaverse",
                    "Polkadot",
                    "ETF"
                ],
                "code": "200000"
            }

        :raises: KucoinResponseException, KucoinAPIException

        """
        return await self._get("markets", False)

    async def get_order_book(self, symbol, depth_20=False, **params):
        """Get a list of bids and asks aggregated by price for a symbol.

        Returns up to 20 or 100 depth each side. Fastest Order book API

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-part-order-book-aggregated-

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param depth_20: If to return only 20 depth
        :type depth_20: bool

        .. code:: python

            orders = client.get_order_book('KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            {
                "sequence": "3262786978",
                "time": 1550653727731,
                "bids": [
                    ["6500.12", "0.45054140"],
                    ["6500.11", "0.45054140"]
                ],
                "asks": [
                    ["6500.16", "0.57753524"],
                    ["6500.15", "0.57753524"]
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}
        path = "market/orderbook/level2_"
        if depth_20:
            path += "20"
        else:
            path += "100"

        return await self._get(path, False, data=dict(data, **params))

    async def get_full_order_book(self, symbol, **params):
        """Get a list of all bids and asks aggregated by price for a symbol.

        This call is generally used by professional traders because it uses more server resources and traffic,
        and Kucoin has strict access frequency control.

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-full-order-book-aggregated-

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            orders = client.get_order_book('KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            {
                "sequence": "3262786978",
                "bids": [
                    ["6500.12", "0.45054140"],  # [price size]
                    ["6500.11", "0.45054140"]
                ],
                "asks": [
                    ["6500.16", "0.57753524"],
                    ["6500.15", "0.57753524"]
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "market/orderbook/level2",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def get_trade_histories(self, symbol, **params):
        """List the latest trades for a symbol

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-trade-histories

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            orders = client.get_trade_histories('KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            [
                {
                    "sequence": "1545896668571",
                    "price": "0.07",                # Filled price
                    "size": "0.004",                # Filled amount
                    "side": "buy",                  # Filled side. The filled side is set to the taker by default.
                    "time": 1545904567062140823     # Transaction time
                },
                {
                    "sequence": "1545896668578",
                    "price": "0.054",
                    "size": "0.066",
                    "side": "buy",
                    "time": 1545904581619888405
                }
            ]

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get("market/histories", False, data=dict(data, **params))

    async def get_kline_data(self, symbol, kline_type="5min", start=None, end=None, **params):
        """Get kline data

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-klines

        For each query, the system would return at most 1500 pieces of data.
        To obtain more data, please page the data by time.

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param kline_type: type of symbol, type of candlestick patterns: 1min, 3min, 5min, 15min, 30min, 1hour, 2hour,
                           4hour, 6hour, 8hour, 12hour, 1day, 1week
        :type kline_type: string
        :param start: Start time as unix timestamp (optional) default start of day in UTC
        :type start: int
        :param end: End time as unix timestamp (optional) default now in UTC
        :type end: int

        .. code:: python

            klines = client.get_kline_data('KCS-BTC', '5min', 1507479171, 1510278278)

        :returns: ApiResponse

        .. code:: python

            [
                [
                    "1545904980",             //Start time of the candle cycle
                    "0.058",                  //opening price
                    "0.049",                  //closing price
                    "0.058",                  //highest price
                    "0.049",                  //lowest price
                    "0.018",                  //Transaction amount
                    "0.000945"                //Transaction volume
                ],
                [
                    "1545904920",
                    "0.058",
                    "0.072",
                    "0.072",
                    "0.058",
                    "0.103",
                    "0.006986"
                ]
            ]

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        if kline_type is not None:
            data["type"] = kline_type
        if start is not None:
            data["startAt"] = start
        if end is not None:
            data["endAt"] = end

        return await self._get("market/candles", False, data=dict(data, **params))

    async def get_fiat_prices(self, base=None, currencies=None, **params):
        """Get fiat price for currency

        https://www.kucoin.com/docs/rest/spot-trading/market-data/get-fiat-price

        :param base: (optional) Fiat,eg.USD,EUR, default is USD.
        :type base: string
        :param currencies: (optional) Cryptocurrencies.For multiple cyrptocurrencies, please separate them with
                       comma one by one. default is all
        :type currencies: string

        .. code:: python

            prices = client.get_fiat_prices()

        :returns: ApiResponse

        .. code:: python

            {
                "BTC": "3911.28000000",
                "ETH": "144.55492453",
                "LTC": "48.45888179",
                "KCS": "0.45546856"
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if base is not None:
            data["base"] = base
        if currencies is not None:
            data["currencies"] = currencies

        return await self._get("prices", False, data=dict(data, **params))

    # Futures Market Endpoints

    async def futures_get_symbols(self, **params):
        """Get a list of available currency pairs for trading.

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-symbols-list

        .. code:: python

            symbols = client.futures_get_symbols()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "symbol": "XBTUSDTM",
                    "rootSymbol": "USDT",
                    "type": "FFWCSX",
                    "firstOpenDate": 1585555200000,
                    "expireDate": null,
                    "settleDate": null,
                    "baseCurrency": "XBT",
                    "quoteCurrency": "USDT",
                    "settleCurrency": "USDT",
                    "maxOrderQty": 1000000,
                    "maxPrice": 1000000.0,
                    "lotSize": 1,
                    "tickSize": 0.1,
                    "indexPriceTickSize": 0.01,
                    "multiplier": 0.001,
                    "initialMargin": 0.008,
                    "maintainMargin": 0.004,
                    "maxRiskLimit": 100000,
                    "minRiskLimit": 100000,
                    "riskStep": 50000,
                    "makerFeeRate": 2.0E-4,
                    "takerFeeRate": 6.0E-4,
                    "takerFixFee": 0.0,
                    "makerFixFee": 0.0,
                    "settlementFee": null,
                    "isDeleverage": true,
                    "isQuanto": true,
                    "isInverse": false,
                    "markMethod": "FairPrice",
                    "fairMethod": "FundingRate",
                    "fundingBaseSymbol": ".XBTINT8H",
                    "fundingQuoteSymbol": ".USDTINT8H",
                    "fundingRateSymbol": ".XBTUSDTMFPI8H",
                    "indexSymbol": ".KXBTUSDT",
                    "settlementSymbol": "",
                    "status": "Open",
                    "fundingFeeRate": 6.41E-4,
                    "predictedFundingFeeRate": 5.5E-5,
                    "fundingRateGranularity": 28800000,
                    "openInterest": "6273644",
                    "turnoverOf24h": 1.9110000807101517E9,
                    "volumeOf24h": 21807.101,
                    "markPrice": 87351.75,
                    "indexPrice": 87357.57,
                    "lastTradePrice": 87319.4,
                    "nextFundingRateTime": 1816952,
                    "maxLeverage": 125,
                    "sourceExchanges": [
                        "okex",
                        "binance",
                        "kucoin",
                        "bybit",
                        "bitmart",
                        "gateio"
                    ],
                    "premiumsSymbol1M": ".XBTUSDTMPI",
                    "premiumsSymbol8H": ".XBTUSDTMPI8H",
                    "fundingBaseSymbol1M": ".XBTINT",
                    "fundingQuoteSymbol1M": ".USDTINT",
                    "lowPrice": 85201.8,
                    "highPrice": 90000.0,
                    "priceChgPct": -0.0033,
                    "priceChg": -291.0,
                    "k": 490.0,
                    "m": 300.0,
                    "f": 1.3,
                    "mmrLimit": 0.3,
                    "mmrLevConstant": 125.0,
                    "supportCross": true,
                    "buyLimit": 91717.92,
                    "sellLimit": 82982.88
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("contracts/active", False, is_futures=True, data=params)

    async def futures_get_symbol(self, symbol, **params):
        """Get a symbol details for trading.

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-symbol-detail

        :param symbol: Name of symbol e.g. XBTUSDTM
        :type symbol: string

        .. code:: python

            symbol = client.futures_get_symbol('XBTUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "symbol": "XBTUSDTM",
                    "rootSymbol": "USDT",
                    "type": "FFWCSX",
                    "firstOpenDate": 1585555200000,
                    "expireDate": null,
                    "settleDate": null,
                    "baseCurrency": "XBT",
                    "quoteCurrency": "USDT",
                    "settleCurrency": "USDT",
                    "maxOrderQty": 1000000,
                    "maxPrice": 1000000.0,
                    "lotSize": 1,
                    "tickSize": 0.1,
                    "indexPriceTickSize": 0.01,
                    "multiplier": 0.001,
                    "initialMargin": 0.008,
                    "maintainMargin": 0.004,
                    "maxRiskLimit": 100000,
                    "minRiskLimit": 100000,
                    "riskStep": 50000,
                    "makerFeeRate": 2.0E-4,
                    "takerFeeRate": 6.0E-4,
                    "takerFixFee": 0.0,
                    "makerFixFee": 0.0,
                    "settlementFee": null,
                    "isDeleverage": true,
                    "isQuanto": true,
                    "isInverse": false,
                    "markMethod": "FairPrice",
                    "fairMethod": "FundingRate",
                    "fundingBaseSymbol": ".XBTINT8H",
                    "fundingQuoteSymbol": ".USDTINT8H",
                    "fundingRateSymbol": ".XBTUSDTMFPI8H",
                    "indexSymbol": ".KXBTUSDT",
                    "settlementSymbol": "",
                    "status": "Open",
                    "fundingFeeRate": 6.41E-4,
                    "predictedFundingFeeRate": 5.5E-5,
                    "fundingRateGranularity": 28800000,
                    "openInterest": "6273644",
                    "turnoverOf24h": 1.9110000807101517E9,
                    "volumeOf24h": 21807.101,
                    "markPrice": 87351.75,
                    "indexPrice": 87357.57,
                    "lastTradePrice": 87319.4,
                    "nextFundingRateTime": 1816952,
                    "maxLeverage": 125,
                    "sourceExchanges": [
                        "okex",
                        "binance",
                        "kucoin",
                        "bybit",
                        "bitmart",
                        "gateio"
                    ],
                    "premiumsSymbol1M": ".XBTUSDTMPI",
                    "premiumsSymbol8H": ".XBTUSDTMPI8H",
                    "fundingBaseSymbol1M": ".XBTINT",
                    "fundingQuoteSymbol1M": ".USDTINT",
                    "lowPrice": 85201.8,
                    "highPrice": 90000.0,
                    "priceChgPct": -0.0033,
                    "priceChg": -291.0,
                    "k": 490.0,
                    "m": 300.0,
                    "f": 1.3,
                    "mmrLimit": 0.3,
                    "mmrLevConstant": 125.0,
                    "supportCross": true,
                    "buyLimit": 91717.92,
                    "sellLimit": 82982.88
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get(
            "contracts/{}".format(symbol), False, is_futures=True, data=params
        )

    async def futures_get_ticker(self, symbol, **params):
        """Get symbol ticker

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-ticker

        :param symbol: Name of symbol e.g. XBTUSDTM

        .. code:: python

            ticker = client.futures_get_ticker('XBTUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "sequence": 1001,
                    "symbol":
                    "side": "buy",
                    "size": 10,
                    "price": "7000.0",
                    "bestBidSize": 20,
                    "bestBidPrice": "7000.0",
                    "bestAskSize": 30,
                    "bestAskPrice": "7001.0",
                    "tradeId": "5cbd7377a6ffab0c7ba98b26",
                    "ts": 1550653727731
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get("ticker", False, is_futures=True, data=dict(data, **params))

    async def futures_get_tickers(self, **params):
        """Get symbol tickers

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-latest-ticker-for-all-contracts

        .. code:: python

            tickers = client.futures_get_tickers()

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": [
                    {
                        "sequence": 1721456489271,
                        "symbol": "THETAUSDTM",
                        "side": "buy",
                        "size": 728,
                        "tradeId": "1721456489263",
                        "price": "1.479",
                        "bestBidPrice": "1.536",
                        "bestBidSize": 272,
                        "bestAskPrice": "1.54",
                        "bestAskSize": 1000,
                        "ts": 1722237164196000000
                    }
                    ...
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("allTickers", False, is_futures=True, data=params)

    async def futures_get_order_book(self, symbol, depth_20=False, **params):
        """Get a list of bids and asks aggregated by price for a symbol.

        Returns up to 20 or 100 depth each side. Fastest Order book API

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-part-order-book-level-2

        :param symbol: Name of symbol e.g. XBTUSDTM

        .. code:: python

            orders = client.futures_get_order_book('XBTUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "symbol": "XBTUSDM",
                    "sequence": 100,
                    "asks": [
                        ["5000.0", 1000],
                        ["6000.0", 1983]
                    ],
                    "bids": [
                        ["3200.0", 800],
                        ["3100.0", 100]
                    ],
                    "ts": 1604643655040584408
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        path = "level2/depth"
        if depth_20:
            path += "20"
        else:
            path += "100"

        return await self._get(path, False, is_futures=True, data=dict(data, **params))

    async def futures_get_full_order_book(self, symbol, **params):
        """Get a list of all bids and asks aggregated by price for a symbol.

        This call is generally used by professional traders because it uses more server resources and traffic,

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-full-order-book-level-2

        :param symbol: Name of symbol e.g. XBTUSDTM

        .. code:: python

            orders = client.futures_get_full_order_book('XBTUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "symbol": "XBTUSDM",
                    "sequence": 100,
                    "asks": [
                        ["5000.0", 1000],
                        ["6000.0", 1983]
                    ],
                    "bids": [
                        ["3200.0", 800],
                        ["3100.0", 100]
                    ],
                    "ts": 1604643655040584408
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "level2/snapshot", False, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_trade_histories(self, symbol, **params):
        """List the latest trades for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-transaction-history

        :param symbol: Name of symbol e.g. XBTUSDTM

        .. code:: python

            orders = client.futures_get_trade_histories('XBTUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "sequence": 102,
                    "tradeId": "5cbd7377a6ffab0c7ba98b26",
                    "takerOrderId": "5cbd7377a6ffab0c7ba98b27",
                    "makerOrderId": "5cbd7377a6ffab0c7ba98b28",
                    "price": "7000.0",
                    "size": 1,
                    "side": "buy",
                    "ts": 1545904567062140823
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "trade/history", False, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_klines(
        self, symbol, kline_type="5min", start=None, end=None, **params
    ):
        """Get kline data

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-klines

        For each query, the system would return at most 1500 pieces of data.

        :param symbol: Name of symbol e.g. XBTUSDTM
        :type symbol: string
        :param kline_type: type of symbol, type of candlestick patterns: 1min, 3min, 5min, 15min, 30min, 1hour, 2hour,
                            4hour, 6hour, 8hour, 12hour, 1day, 1week
        :type kline_type: string
        :param start: Start time as unix timestamp (optional) default start of day in UTC
        :type start: int
        :param end: End time as unix timestamp (optional) default now in UTC
        :type end: int

        .. code:: python

            klines = client.futures_get_klines('XBTUSDTM', '5min', 1507479171, 1510278278)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": [
                    [
                        1575331200000,
                        7495.01,
                        8309.67,
                        7250,
                        7463.55,
                        0
                    ],
                    [
                        1575374400000,
                        7464.37,
                        8297.85,
                        7273.02,
                        7491.44,
                        0
                    ]
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "granularity": kline_type}

        if start is not None:
            data["from"] = start
        if end is not None:
            data["to"] = end

        return await self._get(
            "kline/query", False, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_interest_rate(
        self,
        symbol,
        start=None,
        end=None,
        reverse=True,
        offset=None,
        forward=False,
        max_count=None,
        **params,
    ):
        """Get interest rate

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-interest-rate-list

        :param symbol: Name of symbol e.g. XBTUSDTM
        :type symbol: string
        :param start: Start time as unix timestamp (optional) default start of day in UTC
        :type start: int
        :param end: End time as unix timestamp (optional) default now in UTC
        :type end: int
        :param reverse: (optional) True means “yes”. False means no. This parameter is set as True by default.
        :type reverse: bool
        :param offset: (optional) Start offset. The unique attribute of the last returned result of the last request.
                                The data of the first page will be returned by default.
        :type offset: int
        :param forward: (optional) True means “yes”. False means no. This parameter is set as False by default.
        :type forward: bool
        :param max_count: (optional) Maximum number of data to return. The default value is 100.
        :type max_count: int

        .. code:: python

            interest_rate = client.futures_get_interest_rate('XBTUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "dataList": [
                    {
                        "symbol": ".XBTINT",
                        "granularity": 60000,
                        "timePoint": 1557996300000,
                        "value": 0.0003
                    },
                    {
                        "symbol": ".XBTINT",
                        "granularity": 60000,
                        "timePoint": 1557996240000,
                        "value": 0.0003
                    },
                    {
                        "symbol": ".XBTINT",
                        "granularity": 60000,
                        "timePoint": 1557996180000,
                        "value": 0.0003
                    }
                ],
                "hasMore": true
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        if start is not None:
            data["startAt"] = start
        if end is not None:
            data["endAt"] = end
        if reverse is not None:
            data["reverse"] = reverse
        if offset is not None:
            data["offset"] = offset
        if forward is not None:
            data["forward"] = forward
        if max_count is not None:
            data["maxCount"] = max_count

        return await self._get(
            "interest/query", False, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_index(
        self,
        symbol,
        start=None,
        end=None,
        reverse=True,
        offset=None,
        forward=False,
        max_count=None,
        **params,
    ):
        """Get index

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-index-list

        :param symbol: Name of symbol e.g. XBTUSDTM
        :type symbol: string
        :param start: Start time as unix timestamp (optional) default start of day in UTC
        :type start: int
        :param end: End time as unix timestamp (optional) default now in UTC
        :type end: int
        :param reverse: (optional) True means “yes”. False means no. This parameter is set as True by default.
        :type reverse: bool
        :param offset: (optional) Start offset. The unique attribute of the last returned result of the last request.
                                The data of the first page will be returned by default.
        :type offset: int
        :param forward: (optional) True means “yes”. False means no. This parameter is set as False by default.
        :type forward: bool
        :param max_count: (optional) Maximum number of data to return. The default value is 100.
        :type max_count: int

        :param symbol: Name of symbol e.g. XBTUSDTM

        .. code:: python

            index = client.futures_get_index('XBTUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "dataList": [
                    {
                        "symbol": ".KXBT",
                        "granularity": 1000,
                        "timePoint": 1557998570000,
                        "value": 8016.24,
                        "decomposionList": [
                            {
                                "exchange": "gemini",
                                "price": 8016.24,
                                "weight": 0.08042611
                            },
                            {
                                "exchange": "kraken",
                                "price": 8016.24,
                                "weight": 0.02666502
                            },
                            {
                                "exchange": "coinbase",
                                "price": 8016.24,
                                "weight": 0.03847059
                            },
                            {
                                "exchange": "liquid",
                                "price": 8016.24,
                                "weight": 0.20419723
                            },
                            {
                                "exchange": "bittrex",
                                "price": 8016.24,
                                "weight": 0.29848962
                            },
                            {
                                "exchange": "bitstamp",
                                "price": 8016.24,
                                "weight": 0.35175143
                            }
                        ]
                    }
                ],
                "hasMore": true
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        if start is not None:
            data["startAt"] = start
        if end is not None:
            data["endAt"] = end
        if reverse is not None:
            data["reverse"] = reverse
        if offset is not None:
            data["offset"] = offset
        if forward is not None:
            data["forward"] = forward
        if max_count is not None:
            data["maxCount"] = max_count

        return await self._get(
            "index/query", False, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_mark_price(self, symbol, **params):
        """Get mark price

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-current-mark-price

        :param symbol: Name of symbol e.g. XBTUSDTM
        :type symbol: string

        .. code:: python

            mark_price = client.futures_get_mark_price('XBTUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "symbol": "XBTUSDM",
                "granularity": 1000,
                "timePoint": 1557999585000,
                "value": 8052.51,
                "indexPrice": 8041.95
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "mark-price/{}/current".format(symbol),
            False,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_get_premium_index(
        self,
        symbol,
        start=None,
        end=None,
        reverse=True,
        offset=None,
        forward=False,
        max_count=None,
        **params,
    ):
        """Get premium index

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-premium-index

        :param symbol: Name of symbol e.g. XBTUSDTM
        :type symbol: string
        :param start: Start time as unix timestamp (optional) default start of day in UTC
        :type start: int
        :param end: End time as unix timestamp (optional) default now in UTC
        :type end: int
        :param reverse: (optional) True means “yes”. False means no. This parameter is set as True by default.
        :type reverse: bool
        :param offset: (optional) Start offset. The unique attribute of the last returned result of the last request.
                                The data of the first page will be returned by default.
        :type offset: int
        :param forward: (optional) True means “yes”. False means no. This parameter is set as False by default.
        :type forward: bool
        :param max_count: (optional) Maximum number of data to return. The default value is 100.
        :type max_count: int

        .. code:: python

            premium_index = client.futures_get_premium_index('XBTUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "dataList": [
                    {
                        "symbol": ".XBTUSDMPI",
                        "granularity": 60000,
                        "timePoint": 1558000320000,
                        "value": 0.022585
                    },
                    {
                        "symbol": ".XBTUSDMPI",
                        "granularity": 60000,
                        "timePoint": 1558000260000,
                        "value": 0.022611
                    },
                    {
                        "symbol": ".XBTUSDMPI",
                        "granularity": 60000,
                        "timePoint": 1558000200000,
                        "value": 0.021421
                    }
                ],
                "hasMore": true
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        if start is not None:
            data["startAt"] = start
        if end is not None:
            data["endAt"] = end
        if reverse is not None:
            data["reverse"] = reverse
        if offset is not None:
            data["offset"] = offset
        if forward is not None:
            data["forward"] = forward
        if max_count is not None:
            data["maxCount"] = max_count

        return await self._get(
            "premium/query", False, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_24hr_transaction_volume(self, **params):
        """Get 24hr stats

        https://www.kucoin.com/docs/rest/futures-trading/market-data/get-24hour-futures-transaction-volume

        .. code:: python

            stats = client.futures_get_24hr_transaction_volume()

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": {
                    "turnoverOf24h": 619
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("trade-statistics", False, is_futures=True, data=params)

    # User Account Endpoints

    async def get_accounts(self, currency=None, account_type=None, **params):
        """Get a list of accounts

        https://www.kucoin.com/docs/rest/account/basic-info/get-account-list-spot-margin-trade_hf

        :param currency: optional Currency code
        :type currency: string
        :param account_type: optional Account type - main, trade, margin or pool
        :type account_type: string

        .. code:: python

            accounts = client.get_accounts()
            accounts = client.get_accounts('BTC')
            accounts = client.get_accounts('BTC', 'trade)

        :returns: API Response

        .. code-block:: python

            [
                {
                    "id": "5bd6e9286d99522a52e458de",
                    "currency": "BTC",
                    "type": "main",
                    "balance": "237582.04299",
                    "available": "237582.032",
                    "holds": "0.01099"
                },
                {
                    "id": "5bd6e9216d99522a52e458d6",
                    "currency": "BTC",
                    "type": "trade",
                    "balance": "1234356",
                    "available": "1234356",
                    "holds": "0"
                }
            ]

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {}
        if currency:
            data["currency"] = currency
        if account_type:
            data["type"] = account_type

        return await self._get("accounts", True, data=dict(data, **params))

    async def get_subaccounts(self, **params):
        """Get a list of subaccounts

        https://www.kucoin.com/docs/rest/account/sub-account/get-all-sub-accounts-info-v1-

        .. code:: python

            accounts = client.get_subaccounts()

        :returns: API Response

        .. code-block:: python

            [
                {
                    "userId": "5cbd31ab9c93e9280cd36a0a", //subUserId
                    "uid": "1789234",
                    "subName": "kucoin1",
                    "type": 0, //type:0-nomal
                    "remarks": "kucoin1",
                    "access": "All"
                },
                {
                    "userId": "5cbd31b89c93e9280cd36a0d",
                    "uid": "1789431",
                    "subName": "kucoin2",
                    "type": 1, //type:1-rebot
                    "remarks": "kucoin2",
                    "access": "All"
                }
            ]

        :raises:  KucoinResponseException, KucoinAPIException

        """
        # todo check and add the response

        return await self._get("sub/user", True, data=params)

    async def get_subaccounts_v2(self, page=None, limit=None, **params):
        """Get a list of subaccounts

        https://www.kucoin.com/docs/rest/account/sub-account/get-all-sub-accounts-info-v2-

        :param page: (optional) Current page - default 1
        :type page: int
        :param limit: (optional) Number of results to return - default 10
        :type limit: int

        .. code:: python

            accounts = client.get_subaccounts()
            accounts = client.get_subaccounts(page=2, limit=5)

        :returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": {
                    "currentPage": 1,
                    "pageSize": 100,
                    "totalNum": 1,
                    "totalPage": 1,
                    "items": [
                        {
                            "userId": "635002438793b80001dcc8b3",
                            "uid": 62356,
                            "subName": "margin01",
                            "status": 2,
                            "type": 4,
                            "access": "Margin",
                            "createdAt": 1666187844000,
                            "remarks": null
                        }
                    ]
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """
        # todo check and add the response

        data = {}
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get(
            "sub/user", True, api_version=self.API_VERSION2, data=dict(data, **params)
        )

    async def margin_get_account_detail(self, **params):
        """Get account detail

        https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-margin

        .. code:: python

            account = client.margin_get_account_detail()

        :returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": {
                    "debtRatio": "0",
                    "accounts": [
                        {
                            "currency": "KCS",
                            "totalBalance": "0.01",
                            "availableBalance": "0.01",
                            "holdBalance": "0",
                            "liability": "0",
                            "maxBorrowSize": "0"
                        },
                        {
                            "currency": "USDT",
                            "totalBalance": "0",
                            "availableBalance": "0",
                            "holdBalance": "0",
                            "liability": "0",
                            "maxBorrowSize": "0"
                        },
                        ...
                    ]
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        return await self._get("margin/account", True, data=params)

    async def margin_get_cross_account_detail(
        self, quote_currency=None, query_type=None, **params
    ):
        """Get cross account detail

        https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-cross-margin

        :param quote_currency: (optional) quote currency
        :type quote_currency: string
        :param query_type: (optional) query type
        :type query_type: string

        .. code:: python

            account = client.margin_get_cross_account_detail()

        :returns: API Response

        .. code-block:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": {
                    "timestamp": 1669708513820,
                    "currentPage": 1,
                    "pageSize": 100,
                    "totalNum": 1,
                    "totalPage": 1,
                    "items": [
                        {
                            "totalLiabilityOfQuoteCurrency": "0.976",
                            "totalAssetOfQuoteCurrency": "1.00",
                            "debtRatio": "0.976",
                            "status": "LIQUIDATION",
                            "assets": [
                                {
                                    "currency": "BTC",
                                    "borrowEnabled": true,
                                    "repayEnabled": true,
                                    "transferEnabled": false,
                                    "borrowed": "0.976",
                                    "totalAsset": "1.00",
                                    "available": "0.024",
                                    "hold": "0",
                                    "maxBorrowSize": "0"
                                }
                            ]
                        }
                    ]
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {}
        if quote_currency:
            data["quoteCurrency"] = quote_currency
        if query_type:
            data["type"] = query_type

        return await self._get(
            "margin/accounts",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_get_isolated_account_detail(
        self, symbol=None, quote_currency=None, query_type=None, **params
    ):
        """Get isolated account detail

        https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-isolated-margin

        :param symbol: (optional) symbol
        :type symbol: string
        :param quote_currency: (optional) quote currency
        :type quote_currency: string
        :param query_type: (optional) query type
        :type query_type: string

        .. code:: python

            account = client.margin_get_isolated_account_detail()

        :returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": [
                    {
                        "totalAssetOfQuoteCurrency": "3.4939947",
                        "totalLiabilityOfQuoteCurrency": "0.00239066",
                        "timestamp": 1668062174000,
                        "assets": [
                            {
                                "symbol": "MANA-USDT",
                                "debtRatio": "0",
                                "status": "BORROW",
                                "baseAsset": {
                                    "currency": "MANA",
                                    "borrowEnabled": true,
                                    "repayEnabled": true,
                                    "transferEnabled": true,
                                    "borrowed": "0",
                                    "totalAsset": "0",
                                    "available": "0",
                                    "hold": "0",
                                    "maxBorrowSize": "1000"
                                },
                                "quoteAsset": {
                                    "currency": "USDT",
                                    "borrowEnabled": true,
                                    "repayEnabled": true,
                                    "transferEnabled": true,
                                    "borrowed": "0",
                                    "totalAsset": "0",
                                    "available": "0",
                                    "hold": "0",
                                    "maxBorrowSize": "50000"
                                }
                            }
                        ]
                    }
                ]
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {}
        if symbol:
            data["symbol"] = symbol
        if quote_currency:
            data["quoteCurrency"] = quote_currency
        if query_type:
            data["type"] = query_type

        return await self._get(
            "isolated/accounts",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def futures_get_account_detail(self, currency=None, **params):
        """Get futures account detail

        https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-futures

        :param currency: (optional) currency
        :type currency: string

        .. code:: python

            account = client.futures_get_account_detail()

        :returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": {
                    "accountEquity": 99.8999305281,
                    "unrealisedPNL": 0,
                    "marginBalance": 99.8999305281,
                    "positionMargin": 0,
                    "orderMargin": 0,
                    "frozenFunds": 0,
                    "availableBalance":
                    "currency": "XBT" ,
                    "riskRatio": 0
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {}
        if currency:
            data["currency"] = currency

        return await self._get(
            "account-overview", True, is_futures=True, data=dict(data, **params)
        )

    async def get_subaccount_balance(self, sub_user_id, include_base_ammount, **params):
        """Get the account info of a sub-user specified by the subUserId

        https://www.kucoin.com/docs/rest/account/sub-account/get-a-sub-account-balance

        :param sub_user_id: Sub account user id
        :type sub_user_id: string
        :param include_base_ammount: Include base amount or not
        :type include_base_ammount: bool

        .. code:: python

            accounts = client.get_subaccount_balance('5cbd31ab9c93e9280cd36a0a', True)

        :returns: API Response

        .. code-block:: python

            {
                "subUserId": "5caefba7d9575a0688f83c45",
                "subName": "sdfgsdfgsfd",
                "mainAccounts": [
                    {
                        "currency": "BTC",
                        "balance": "8",
                        "available": "8",
                        "holds": "0",
                        "baseCurrency": "BTC",
                        "baseCurrencyPrice": "1",
                        "baseAmount": "1.1"
                    }
                ],
                "tradeAccounts": [
                    {
                        "currency": "BTC",
                        "balance": "1000",
                        "available": "1000",
                        "holds": "0",
                        "baseCurrency": "BTC",
                        "baseCurrencyPrice": "1",
                        "baseAmount": "1.1"
                    }
                ],
                "marginAccounts": [
                    {
                        "currency": "BTC",
                        "balance": "1.1",
                        "available": "1.1",
                        "holds": "0",
                        "baseCurrency": "BTC",
                        "baseCurrencyPrice": "1",
                        "baseAmount": "1.1"
                    }
                ]
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """
        # todo check and add the response

        data = {"subUserId": sub_user_id, "includeBaseAmount": include_base_ammount}

        return await self._get(
            "sub-accounts/{}".format(sub_user_id), True, data=dict(data, **params)
        )

    async def get_all_subaccounts_balance(self):
        """Get the account info of all sub-users

        https://www.kucoin.com/docs/rest/account/sub-account/get-all-sub-accounts-balance-v1-

        .. code:: python

            accounts = client.get_all_subaccounts_balance()

        :returns: API Response

        .. code-block:: python

            [
                {
                    "subUserId": "5caefba7d9575a0688f83c45",
                    "subName": "kucoin1",
                    "mainAccounts": [
                        {
                            "currency": "BTC",
                            "balance": "6",
                            "available": "6",
                            "holds": "0",
                            "baseCurrency": "BTC",
                            "baseCurrencyPrice": "1",
                            "baseAmount": "1.1"
                        }
                    ],
                    "tradeAccounts": [
                        {
                            "currency": "BTC",
                            "balance": "1000",
                            "available": "1000",
                            "holds": "0",
                            "baseCurrency": "BTC",
                            "baseCurrencyPrice": "1",
                            "baseAmount": "1.1"
                        }
                    ],
                    "marginAccounts": [
                        {
                            "currency": "BTC",
                            "balance": "1.1",
                            "available": "1.1",
                            "holds": "0",
                            "baseCurrency": "BTC",
                            "baseCurrencyPrice": "1",
                            "baseAmount": "1.1"
                        }
                    ]
                }
            ]

        :raises:  KucoinResponseException, KucoinAPIException

        """
        # todo check and add the response

        return await self._get("sub-accounts", True)

    async def get_all_subaccounts_balance_v2(self, page=None, limit=None, **params):
        """Get the account info of all sub-users

        https://www.kucoin.com/docs/rest/account/sub-account/get-all-sub-accounts-balance-v2-

        :param page: (optional) Current page - default 1
        :type page: int
        :param limit: (optional) Number of results to return - default 10
        :type limit: int

        .. code:: python

            accounts = client.get_all_subaccounts_balance_v2()
            accounts = client.get_all_subaccounts_balance_v2(page=2, limit=5)

        :returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": {
                    "currentPage": 1,
                    "pageSize": 10,
                    "totalNum": 14,
                    "totalPage": 2,
                    "items": [
                        {
                            "subUserId": "635002438793b80001dcc8b3",
                            "subName": "margin03",
                            "mainAccounts": [
                                {
                                    "currency": "00",
                                    "balance": "0",
                                    "available": "0",
                                    "holds": "0",
                                    "baseCurrency": "BTC",
                                    "baseCurrencyPrice": "125.63",
                                    "baseAmount": "0"
                                }
                            ]
                        }
                    ]
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """
        # todo check and add the response

        data = {}
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get(
            "sub-accounts",
            True,
            api_version=self.API_VERSION2,
            data=dict(data, **params),
        )

    async def futures_get_all_subaccounts_balance(self, currency=None, **params):
        """Get the account info of all sub-users

        https://www.kucoin.com/docs/rest/funding/funding-overview/get-all-sub-accounts-balance-futures

        :param currency: (optional) currency
        :type currency: string

        .. code:: python

            accounts = client.futures_get_all_subaccounts_balance()

        :returns: API Response

        .. code-block:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": {
                    "summary": {
                        "accountEquityTotal": 9.99,
                        "unrealisedPNLTotal": 0,
                        "marginBalanceTotal": 9.99,
                        "positionMarginTotal": 0,
                        "orderMarginTotal": 0,
                        "frozenFundsTotal": 0,
                        "availableBalanceTotal": 9.99,
                        "currency": "USDT"
                    },
                    "accounts": [
                        {
                            "accountName": "main",
                            "accountEquity": 9.99,
                            "unrealisedPNL": 0,
                            "marginBalance": 9.99,
                            "positionMargin": 0,
                            "orderMargin": 0,
                            "frozenFunds": 0,
                            "availableBalance": 9.99,
                            "currency": "USDT"
                        },
                        {
                            "accountName": "subacct",
                            "accountEquity": 0,
                            "unrealisedPNL": 0,
                            "marginBalance": 0,
                            "positionMargin": 0,
                            "orderMargin": 0,
                            "frozenFunds": 0,
                            "availableBalance": 0,
                            "currency": "USDT"
                        }
                    ]
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """
        # todo check and add the response

        data = {}
        if currency:
            data["currency"] = currency

        return await self._get(
            "account-overview-all", True, is_futures=True, data=dict(data, **params)
        )

    async def get_subaccount_api_list(self, sub_name, api_key=None, **params):
        """Get the API key list of a sub-user

        https://www.kucoin.com/docs/rest/account/sub-account-api/get-sub-account-api-list

        :param api_key: (optional) API key
        :type api_key: string
        :param sub_name: Sub account name
        :type sub_name: string

        .. code:: python

            accounts = client.get_subaccount_api_list('kucoin1')
            accounts = client.get_subaccount_api_list('kucoin1', '5cbd31ab9c93e9280cd36a0a')

        :returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": [
                    {
                        "subName": "AAAAAAAAAAAAA0022",
                        "remark": "hytest01-01",
                        "apiKey": "63032453e75087000182982b",
                        "permission": "General",
                        "ipWhitelist": "",
                        "createdAt": 1661150291000,
                        "apiVersion" : 3
                    }
                ]
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        # todo check and add the response

        data = {"subName": sub_name}

        if api_key:
            data["apiKey"] = api_key

        return await self._get("sub/api-key", True, data=dict(data, **params))

    async def create_subaccount_api(
        self,
        sub_name,
        passphrase,
        remark,
        permission=None,
        ip_whitelist=None,
        expire=None,
        **params,
    ):
        """Create Spot APIs for sub-accounts

        https://www.kucoin.com/docs/rest/account/sub-account-api/create-sub-account-api

        :param sub_name: Sub account name
        :type sub_name: string
        :param passphrase: Sub account passphrase
        :type passphrase: string
        :param remark: API key remark
        :type remark: string
        :param permission: (optional) API key permission - General, Tradable, Withdraw
        :type permission: string
        :param ip_whitelist: (optional) IP whitelist
        :type ip_whitelist: string
        :param expire: (optional) API key expiration time in seconds
        :type expire: string

        .. code:: python

            accounts = client.create_subaccount_api('kucoin1', 'mypassword', 'myApiKey')

        returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": {
                    "subName": "AAAAAAAAAA0007",
                    "remark": "remark",
                    "apiKey": "630325e0e750870001829864",
                    "apiSecret": "110f31fc-61c5-4baf-a29f-3f19a62bbf5d",
                    "passphrase": "passphrase",
                    "permission": "General",
                    "ipWhitelist": "",
                    "createdAt": 1661150688000
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        # todo check and add the response

        data = {"subName": sub_name, "passphrase": passphrase, "remark": remark}

        if permission:
            data["permission"] = permission
        if ip_whitelist:
            data["ipWhitelist"] = ip_whitelist
        if expire:
            data["expire"] = expire

        return await self._post("sub/api-key", True, data=dict(data, **params))

    async def modify_subaccount_api(
        self,
        sub_name,
        api_key,
        passphrase,
        permission=None,
        ip_whitelist=None,
        expire=None,
        **params,
    ):
        """Modify Spot APIs for sub-accounts

        https://www.kucoin.com/docs/rest/account/sub-account-api/modify-sub-account-api

        :param sub_name: Sub account name
        :type sub_name: string
        :param api_key: API key
        :type api_key: string
        :param passphrase: Sub account passphrase
        :type passphrase: string
        :param permission: (optional) API key permission - General, Tradable, Withdraw
        :type permission: string
        :param ip_whitelist: (optional) IP whitelist
        :type ip_whitelist: string
        :param expire: (optional) API key expiration time in seconds
        :type expire: string

        .. code:: python

            accounts = client.modify_subaccount_api('kucoin1', 'myApiKey', 'mypassword')

        returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": {
                    "subName": "AAAAAAAAAA0007",
                    "apiKey": "630329b4e7508700018298c5",
                    "permission": "General",
                    "ipWhitelist": "127.0.0.1"
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        # todo check and add the response

        data = {"subName": sub_name, "apiKey": api_key, "passphrase": passphrase}

        if permission:
            data["permission"] = permission
        if ip_whitelist:
            data["ipWhitelist"] = ip_whitelist
        if expire:
            data["expire"] = expire

        return await self._post("sub/api-key/update", True, data=dict(data, **params))

    async def delete_subaccount_api(self, api_key, passphrase, sub_name, **params):
        """Delete Spot APIs for sub-accounts

        https://www.kucoin.com/docs/rest/account/sub-account-api/delete-sub-account-api

        :param api_key: API key
        :type api_key: string
        :param passphrase: Sub account passphrase
        :type passphrase: string
        :param sub_name: Sub account name
        :type sub_name: string

        .. code:: python

            accounts = client.delete_subaccount_api('myApiKey', 'mypassword', 'kucoin1')

        returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": {
                    "subName": "AAAAAAAAAA0007",
                    "apiKey": "630325e0e750870001829864"
                }
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        # todo check and add the response

        data = {"apiKey": api_key, "passphrase": passphrase, "subName": sub_name}

        return await self._delete("sub/api-key", True, data=dict(data, **params))

    async def get_account(self, account_id):
        """Get an individual account

        https://www.kucoin.com/docs/rest/account/basic-info/get-account-detail-spot-margin-trade_hf

        :param account_id: ID for account - from list_accounts()
        :type account_id: string

        .. code:: python

            account = client.get_account('5bd6e9216d99522a52e458d6')

        :returns: API Response

        .. code-block:: python

            {
                "currency": "KCS",
                "balance": "1000000060.6299",
                "available": "1000000060.6299",
                "holds": "0"
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        return await self._get("accounts/{}".format(account_id), True)

    async def create_account(self, account_type, currency):
        """Create an account

        https://docs.kucoin.com/#create-an-account

        :param account_type: Account type - main, trade, margin
        :type account_type: string
        :param currency: Currency code
        :type currency: string

        .. code:: python

            account = client.create_account('trade', 'BTC')

        :returns: API Response

        .. code-block:: python

            {
                "id": "5bd6e9286d99522a52e458de"
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {"type": account_type, "currency": currency}
        # todo check this endpoint

        return await self._post("accounts", True, data=data)

    async def create_subaccount(self, password, sub_name, access, remarks=None, **params):
        """Create a subaccount

        https://www.kucoin.com/docs/rest/account/sub-account/create-sub-account

        :param password: Password(7-24 characters, must contain letters and numbers, cannot only contain numbers or include special characters).
        :type password: string
        :param sub_name: Sub-account name(must contain 7-32 characters, at least one number and one letter. Cannot contain any spaces.)
        :type sub_name: string
        :param access: Permission (Spot, Futures, Margin permissions, which can be used alone or in combination).
        :type access: string
        :param remarks: optional Remarks(1~24 characters).
        :type remarks: string

        .. code:: python

            account = client.create_subaccount('mypassword', 'mySubAccount', 'Spot')
            account = client.create_subaccount('mypassword', 'mySubAccount', 'Spot, Margin', 'My Sub Account')

        :returns: API Response

        .. code-block:: python

            {
                "id": "5bd6e9286d99522a52e458de"
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        # todo check and add the response (last time it was 100010: Network error. Please try again later)
        data = {"password": password, "subName": sub_name, "access": access}
        if remarks:
            data["remarks"] = remarks

        return await self._post(
            "sub/user/created",
            True,
            api_version=self.API_VERSION2,
            data=dict(data, **params),
        )

    async def get_account_activity(
        self,
        currency=None,
        direction=None,
        biz_type=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get list of account activity

        https://www.kucoin.com/docs/rest/account/basic-info/get-account-ledgers-spot-margin

        :param currency: (optional) currency name
        :type currency: string
        :param direction: (optional) Side: in - Receive, out - Send
        :type direction: string
        :param biz_type: (optional) Business type: DEPOSIT, WITHDRAW, TRANSFER, SUB_TRANSFER,TRADE_EXCHANGE, MARGIN_EXCHANGE, KUCOIN_BONUS.
        :type biz_type: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param page: (optional) Current page - default 1
        :type page: int
        :param limit: (optional) Number of results to return - default 50
        :type limit: int

        .. code:: python

            history = client.get_account_activity()

            history = client.get_account_activity('ETH', start='1540296039000')

            history = client.get_account_activity('ETH', page=2, page_size=10)

        :returns: API Response

        .. code-block:: python

            {
                "currentPage": 1,
                "pageSize": 10,
                "totalNum": 2,
                "totalPage": 1,
                "items": [
                    {
                        "currency": "KCS",
                        "amount": "0.0998",
                        "fee": "0",
                        "balance": "1994.040596",
                        "bizType": "withdraw",
                        "direction": "in",
                        "createdAt": 1540296039000,
                        "context": {
                             "orderId": "5bc7f080b39c5c03286eef8a",
                             "currency": "BTC"
                         }
                    },
                    {
                        "currency": "KCS",
                        "amount": "0.0998",
                        "fee": "0",
                        "balance": "1994.140396",
                        "bizType": "trade exchange",
                        "direction": "in",
                        "createdAt": 1540296039000,
                        "context": {
                             "orderId": "5bc7f080b39c5c03286eef8e",
                             "tradeId": "5bc7f080b3949c03286eef8a",
                             "symbol": "BTC-USD"
                        }
                    }
                ]
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {}
        if currency:
            data["currency"] = currency
        if direction:
            data["direction"] = direction
        if biz_type:
            data["bizType"] = biz_type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get("accounts/ledgers", True, dict(data, **params))

    async def hf_get_account_activity(
        self,
        currency=None,
        direction=None,
        biz_type=None,
        start=None,
        end=None,
        limit=None,
        last_id=None,
        margin=False,
        **params,
    ):
        """Get list of hf account activity

        https://www.kucoin.com/docs/rest/account/basic-info/get-account-ledgers-trade_hf
        https://www.kucoin.com/docs/rest/account/basic-info/get-account-ledgers-margin_hf

        :param currency: (optional) currency name
        :type currency: string
        :param direction: (optional) Side: in - Receive, out - Send
        :type direction: string
        :param biz_type: (optional) Business type: DEPOSIT, WITHDRAW, TRANSFER, SUB_TRANSFER,TRADE_EXCHANGE, MARGIN_EXCHANGE, KUCOIN_BONUS.
        :type biz_type: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param limit: (optional) Number of results to return - default 100
        :type limit: int
        :param last_id: (optional) The id of the last set of data from the previous batch of data. By default, the latest information is given.
        :type last_id: int
        :param margin: (optional) If True, get margin account activity - default False
        :type margin: bool

        .. code:: python

            history = client.hf_get_account_activity()

            history = client.hf_get_account_activity('ETH', start='1540296039000')

            history = client.hf_get_account_activity('ETH', margin=True, limit=10)

        :returns: API Response

        .. code-block:: python

            {
                "code": "200000",
                "data": [
                    {
                        "id": "981449530900577",
                        "currency": "ETH",
                        "amount": "0.00617410",
                        "fee": "0.00000000",
                        "tax": "0",
                        "balance": "0.00617410",
                        "accountType": "TRADE_HF",
                        "bizType": "TRADE_EXCHANGE",
                        "direction": "in",
                        "createdAt": "1730545211517",
                        "context": "{\"symbol\": \"ETH-USDT\",\"orderId\": \"6726063b4d742800076e0273\",\"tradeId\": \"10330457609226241\"}"
                    }
                ]
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {}
        if currency:
            data["currency"] = currency
        if direction:
            data["direction"] = direction
        if biz_type:
            data["bizType"] = biz_type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if limit:
            data["limit"] = limit
        if last_id:
            data["lastId"] = last_id

        path = "hf/accounts/ledgers"
        if margin:
            path = "hf/margin/account/ledgers"
        return await self._get(path, True, data=dict(data, **params))

    async def futures_get_account_activity(
        self,
        currency=None,
        type=None,
        start=None,
        end=None,
        limit=None,
        offset=None,
        forward=True,
        **params,
    ):
        """Get list of futures account activity

        https://www.kucoin.com/docs/rest/account/basic-info/get-account-ledgers-futures

        :param currency: (optional) currency name
        :type currency: string
        :param type: (optional) Type: RealisedPNL, Deposit, Withdrawal, Transferin, TransferOut.
        :type type: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param limit: (optional) Number of results to return - default 50
        :type limit: int
        :param offset: (optional) Start offset. Generally, the only attribute of the last returned result of the previous request is used, and the first page is returned by default
        :type offset: int
        :param forward: (optional) This parameter functions to judge whether the lookup is forward or not. True means “yes” and False means “no” - default True
        :type forward: bool

        .. code:: python

            history = client.get_futures_account_activity()

            history = client.get_account_activity('ETH', start='1540296039000')

            history = client.get_account_activity('ETH', forward=TRUE, page_size=10)

        :returns: API Response

        :raises:  KucoinResponseException, KucoinAPIException

        """
        # todo check and add the response
        data = {}
        if currency:
            data["currency"] = currency
        if type:
            data["type"] = type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if limit:
            data["maxCount"] = limit
        if offset:
            data["offset"] = offset
        if not forward:
            data["forward"] = False

        return await self._get(
            "transaction-history", True, is_futures=True, data=dict(data, **params)
        )

    # Transfer Endpoints

    async def get_transferable_balance(self, currency, type, tag=None, **params):
        """Get transferable balance

        https://www.kucoin.com/docs/rest/funding/transfer/get-the-transferable

        :param currency: currency name
        :type currency: string
        :param type: Account type: MAIN、TRADE、MARGIN、ISOLATED
        :type type: string
        :param tag: (optional) Trading pair, required when the account type is ISOLATED; other types are not passed, e.g.: BTC-USDT
        :type tag: string

        .. code:: python

            transfer = client.get_transferable_balance('BTC', 'MAIN')

        :returns: API Response

        .. code-block:: python

            {
                "currency": "KCS",
                "balance": "0",
                "available": "0",
                "holds": "0",
                "transferable": "0"
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency, "type": type}
        if tag:
            data["tag"] = tag

        return await self._get("accounts/transferable", True, data=dict(data, **params))

    async def create_universal_transfer(
        self,
        client_oid,
        amount,
        from_account_type,
        type,
        to_account_type,
        currency=None,
        from_user_id=None,
        from_account_tag=None,
        to_user_id=None,
        to_account_tag=None,
        **params,
    ):
        """Transfer fund among accounts on the platform

        https://www.kucoin.com/docs/rest/funding/transfer/flextransfer

        :param client_oid: Unique order id created by users to identify their orders, e.g. UUID, with a maximum length of 128 bits
        :type client_oid: string
        :param amount: Transfer amount, the amount is a positive integer multiple of the currency precision.
        :type amount: string
        :param from_account_type: Account type：MAIN、TRADE、CONTRACT、MARGIN、ISOLATED、MARGIN_V2、ISOLATED_V2
        :type from_account_type: string
        :param type: Transfer type: Transfer type：INTERNAL(Transfer within account)、PARENT_TO_SUB(Transfer from master-account to sub-account)，SUB_TO_PARENT(Transfer from sub-account to master-account)
        :type type: string
        :param to_account_type: Account type：MAIN、TRADE、CONTRACT、MARGIN、ISOLATED、MARGIN_V2、ISOLATED_V2
        :type to_account_type: string
        :param currency: (optional) currency name
        :type currency: string
        :param from_user_id: (optional) Transfer out UserId， This is required when transferring sub-account to master-account. It is optional for internal transfers.
        :type from_user_id: string
        :param from_account_tag: (optional) Symbol, required when the account type is ISOLATED or ISOLATED_V2, for example: BTC-USDT
        :type from_account_tag: string
        :param to_user_id: (optional) Transfer in UserId， This is required when transferring master-account to sub-account. It is optional for internal transfers.
        :type to_user_id: string
        :param to_account_tag: (optional) Symbol, required when the account type is ISOLATED or ISOLATED_V2, for example: BTC-USDT
        :type to_account_tag: string

        .. code:: python

            transfer = client.create_universal_transfer('6d539dc614db3', 1, 'MAIN', 'INTERNAL', 'TRADE')

        :returns: API Response

        .. code-block:: python

            {
                "clientOid": "64ccc0f164781800010d8c09",
                "type": "INTERNAL",
                "currency": "BTC",
                "amount": 1,
                "fromAccountType": "TRADE",
                "toAccountType": "CONTRACT"
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {
            "clientOid": client_oid,
            "amount": amount,
            "fromAccountType": from_account_type,
            "type": type,
            "toAccountType": to_account_type,
        }
        if currency:
            data["currency"] = currency
        if from_user_id:
            data["fromUserId"] = from_user_id
        if from_account_tag:
            data["fromAccountTag"] = from_account_tag
        if to_user_id:
            data["toUserId"] = to_user_id
        if to_account_tag:
            data["toAccountTag"] = to_account_tag

        return await self._post(
            "accounts/universal-transfer", True, data=dict(data, **params)
        )

    async def create_subaccount_transfer(
        self,
        client_oid,
        currency,
        amount,
        direction,
        sub_user_id,
        account_type=None,
        sub_account_type=None,
        **params,
    ):
        """Transfer fund from master account to sub-account or from sub-account to master account

        https://www.kucoin.com/docs/rest/funding/transfer/transfer-between-master-account-and-sub-account

        :param client_oid: Unique order id created by users to identify their orders, e.g. UUID, with a maximum length of 128 bits
        :type client_oid: string
        :param currency: currency name
        :type currency: string
        :param amount: Transfer amount, the amount is a positive integer multiple of the currency precision.
        :type amount: string
        :param direction: Transfer direction. OUT — the master user to sub user. IN — the sub user to the master user.
        :type direction: string
        :param sub_user_id: Sub account user id
        :type sub_user_id: string
        :param account_type: (optional) The account type of the master user: MAIN, TRADE, MARGIN or CONTRACT, default is MAIN.
        :type account_type: string
        :param sub_account_type: (optional) The account type of the sub user: MAIN, TRADE, MARGIN or CONTRACT, default is MAIN.
        :type sub_account_type: string

        .. code:: python

            transfer = client.create_subaccount_transfer('6d539dc614db3', 'BTC', 1, 'OUT', '5cbd31ab9c93e9280cd36a0a')

        :returns: API Response

        .. code-block:: python

            {
                "orderId": "5cbd870fd9575a18e4438b9a"
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {
            "clientOid": client_oid,
            "currency": currency,
            "amount": amount,
            "direction": direction,
            "subUserId": sub_user_id,
        }
        if account_type:
            data["accountType"] = account_type
        if sub_account_type:
            data["subAccountType"] = sub_account_type

        return await self._post(
            "accounts/sub-transfer",
            True,
            api_version=self.API_VERSION2,
            data=dict(data, **params),
        )

    async def create_inner_transfer(
        self,
        client_oid,
        currency,
        from_type,
        to_type,
        amount,
        from_tag=None,
        to_tag=None,
        **params,
    ):
        """Transfer fund among accounts on the platform

        https://www.kucoin.com/docs/rest/funding/transfer/inner-transfer

        :param client_oid: Unique order id created by users to identify their orders, e.g. UUID, with a maximum length of 128 bits
        :type client_oid: string
        :param currency: currency name
        :type currency: str
        :param from_type: Payment Account Type: main, trade, margin, isolated, margin_v2, isolated_v2
        :type from_type: str
        :param to_type: Receiving Account Type: main, trade, margin, isolated, margin_v2, isolated_v2, contract
        :type to_type: str
        :param amount: Amount to transfer
        :type amount: int
        :param from_tag: (optional) Symbol, required when the account type is ISOLATED or ISOLATED_V2, for example: BTC-USDT
        :type from_tag: str
        :param to_tag: (optional) Symbol, required when the account type is ISOLATED or ISOLATED_V2, for example: BTC-USDT
        :type to_tag: str

        .. code:: python

            transfer = client.create_inner_transfer('6d539dc614db3', 'BTC', 'main', 'trade', 1)

        :returns: API Response

        .. code-block:: python

            {
                "orderId": "5bd6e9286d99522a52e458de"
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {
            "clientOid": client_oid,
            "currency": currency,
            "from": from_type,
            "to": to_type,
            "amount": amount,
        }
        if from_tag:
            data["fromTag"] = from_tag
        if to_tag:
            data["toTag"] = to_tag

        return await self._post(
            "accounts/inner-transfer",
            True,
            api_version=self.API_VERSION2,
            data=dict(data, **params),
        )

    async def create_transfer_out(self, amount, currency, rec_account_type, **params):
        """Transfer to Main or TRADE Account

        https://www.kucoin.com/docs/rest/funding/transfer/transfer-to-main-or-trade-account

        :param amount: Transfer amount
        :type amount: string
        :param currency: Currency
        :type currency: string
        :param rec_account_type: Receive account type, including MAIN,TRADE
        :type rec_account_type: string

        .. code:: python

            transfer = client.create_transfer_out('1', 'BTC', 'TRADE')

        :returns: API Response

        .. code-block:: python

            {
                "applyId": "620a0bbefeaa6a000110e833",
                "bizNo": "620a0bbefeaa6a000110e832",
                "payAccountType": "CONTRACT",
                "payTag": "DEFAULT",
                "remark": "",
                "recAccountType": "MAIN",
                "recTag": "DEFAULT",
                "recRemark": "",
                "recSystem": "KUCOIN",
                "status": "PROCESSING",
                "currency": "USDT",
                "amount": "0.001",
                "fee": "0",
                "sn": 889048787670001,
                "reason": "",
                "createdAt": 1644825534000,
                "updatedAt": 1644825534000
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {
            "amount": amount,
            "currency": currency,
            "recAccountType": rec_account_type,
        }

        return await self._post(
            "accounts/transfer-out",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def create_transfer_in(self, amount, currency, pay_account_type, **params):
        """Transfer to Futures Account

        https://www.kucoin.com/docs/rest/funding/transfer/transfer-to-futures-account

        :param amount: Transfer amount
        :type amount: string
        :param currency: Currency
        :type currency: string
        :param pay_account_type: Pay account type, including MAIN,TRADE
        :type pay_account_type: string

        .. code:: python

            transfer = client.create_transfer_in('1', 'BTC', 'TRADE')

        :returns: API Response

        .. code-block:: python

            {
                "code": "200",
                "msg": "",
                "retry": true,
                "success": true
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {
            "amount": amount,
            "currency": currency,
            "payAccountType": pay_account_type,
        }

        return await self._post("accounts/transfer-in", True, data=dict(data, **params))

    async def get_transfer_list(
        self,
        start=None,
        end=None,
        status=None,
        query_status=None,
        currency=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get Futures Transfer-Out Request Records

        https://www.kucoin.com/docs/rest/funding/transfer/get-futures-transfer-out-request-records

        :param start: (optional) Start time (milisecond)
        :type start: int
        :param end: (optional) End time (milisecond)
        :type end: int
        :param status: (optional) Transfer status: PROCESSING, SUCCESS, FAILURE
        :type status: string
        :param query_status: (optional) Transfer status: PROCESSING, SUCCESS, FAILURE
        :type query_status: string
        :param currency: (optional) currency name
        :type currency: string
        :param page: (optional) Current page - default 1
        :type page: int
        :param limit: (optional) Number of results to return - default 50
        :type limit: int

        .. code:: python

            transfer = client.get_transfer_list()
            transfer = client.get_transfer_list('1540296039000')
            transfer = client.get_transfer_list('1540296039000', '1540296039000')
            transfer = client.get_transfer_list('1540296039000', '1540296039000', 'PROCESSING')
            transfer = client.get_transfer_list('1540296039000', '1540296039000', 'PROCESSING', 'PROCESSING')
            transfer = client.get_transfer_list('1540296039000', '1540296039000', 'PROCESSING', 'PROCESSING', 'BTC')
            transfer = client.get_transfer_list('1540296039000', '1540296039000', 'PROCESSING', 'PROCESSING', 'BTC', 1, 10)

        :returns: API Response

        .. code-block:: python

            {
                "currentPage": 1,
                "pageSize": 50,
                "totalNum": 1,
                "totalPage": 1,
                "items": [
                    {
                    "applyId": "620a0bbefeaa6a000110e833", //Transfer-out request ID
                    "currency": "USDT", //Currency
                    "recRemark": "", //Receive account tx remark
                    "recSystem": "KUCOIN", //Receive system
                    "status": "SUCCESS", //Status  PROCESSING, SUCCESS, FAILURE
                    "amount": "0.001", //Transaction amount
                    "reason": "", //Reason caused the failure
                    "offset": 889048787670001, //Offset
                    "createdAt": 1644825534000, //Request application time
                    "remark": "" //User remark
                    }
                ]
            }

        :raises:  KucoinResponseException, KucoinAPIException

        """

        data = {}
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if status:
            data["status"] = status
        if query_status:
            data["queryStatus"] = query_status
        if currency:
            data["currency"] = currency
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get("transfer-list", True, data=dict(data, **params))

    # Deposit Endpoints

    async def create_deposit_address(
        self, currency, chain=None, to=None, amount=None, **params
    ):
        """Create deposit address for a currency you intend to deposit

        https://www.kucoin.com/docs/rest/funding/deposit/create-deposit-address-v3-

        :param currency: Name of currency
        :type currency: string
        :param chain: (optional) The chain name of currency
        :type chain: string
        :param to: (optional) The address that the currency will be sent to
        :type to: string
        :param amount: (optional) The amount of currency to be deposited
        :type amount: string

        .. code:: python

            address = client.create_deposit_address_v3('USDT')
            address = client.create_deposit_address_v3('USDT', 'ERC20')
            address = client.create_deposit_address_v3('USDT', 'ERC20', '0x0a2586d5a901c8e7e68f6b0dc83bfd8bd8600ff5')
            address = client.create_deposit_address_v3('USDT', 'ERC20', '0x0a2586d5a901c8e7e68f6b0dc83bfd8bd8600ff5', 100)

        :returns: ApiResponse

        .. code:: python

            {
                "data" : {
                    "memo" : null,
                    "chain" : "ERC20",
                    "chainId" : "eth",
                    "to" : "MAIN",
                    "currency" : "USDT",
                    "address" : "0x0a2586d5a901c8e7e68f6b0dc83bfd8bd8600ff5"
                },
                "code" : "200000"
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency}

        if chain is not None:
            data["chain"] = chain

        if to is not None:
            data["to"] = to

        if amount is not None:
            data["amount"] = amount

        return await self._post(
            "deposit-address/create",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def get_deposit_addresses(self, currency, amount=None, chain=None, **params):
        """Get all deposit addresses for the currency you intend to deposit.

        https://www.kucoin.com/docs/rest/funding/deposit/get-deposit-addresses-v3-

        :param currency: Name of currency
        :type currency: string
        :param amount: (optional) The amount of currency to be deposited
        :type amount: string
        :param chain: (optional) The chain name of currency
        :type chain: string

        .. code:: python

            address = client.get_deposit_addresses('USDT')
            address = client.get_deposit_addresses('USDT', '100')
            address = client.get_deposit_addresses('USDT', '100', 'ERC20')

        :returns: ApiResponse

        .. code:: python

            {
                "data" : [
                    {
                        "address" : "bc1qwyuvmx53d*****gdg47kqxfwqy",
                        "chain" : "BTC-Segwit",
                        "memo" : "",
                        "contractAddress" : "",
                        "to" : "MAIN",
                        "chainId" : "bech32",
                        "currency" : "BTC"
                    },
                    {
                        "address" : "3K7X9Vjnd*****TGaTAWoJ7H",
                        "chain" : "BTC",
                        "memo" : "",
                        "contractAddress" : "",
                        "to" : "MAIN",
                        "chainId" : "btc",
                        "currency" : "BTC"
                    },
                    {
                        "address" : "0x637da22b860*****ac0c2433",
                        "chain" : "KCC",
                        "memo" : "",
                        "contractAddress" : "0xfa93c12cd345c658bc4644d1d4e1b9615952258c",
                        "to" : "MAIN",
                        "chainId" : "kcc",
                        "currency" : "BTC"
                    }
                ],
                "code" : "200000"
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency}

        if amount is not None:
            data["amount"] = amount

        if chain is not None:
            data["chain"] = chain

        return await self._get(
            "deposit-addresses",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def get_deposits(
        self,
        currency=None,
        status=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get deposit records for a currency

        https://www.kucoin.com/docs/rest/funding/deposit/get-deposit-list

        :param currency: Name of currency (optional)
        :type currency: string
        :param status: optional - Status of deposit (PROCESSING, SUCCESS, FAILURE)
        :type status: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of transactions
        :type limit: int

        .. code:: python

            deposits = client.get_deposits('NEO')
            deposits = client.get_deposits('NEO', 'SUCCESS')
            deposits = client.get_deposits('NEO', 'SUCCESS', 1540296039000, 1540296039000)
            deposits = client.get_deposits('NEO', 'SUCCESS', 1540296039000, 1540296039000, 1, 5)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "currentPage": 1,
                    "pageSize": 50,
                    "totalNum": 1,
                    "totalPage": 1,
                    "items": [
                        {
                            "currency": "XRP",
                            "chain": "xrp",
                            "status": "SUCCESS",
                            "address": "rNFugeoj3ZN8Wv6xhuLegUBBPXKCyWLRkB",
                            "memo": "1919537769",
                            "isInner": false,
                            "amount": "20.50000000",
                            "fee": "0.00000000",
                            "walletTxId": "2C24A6D5B3E7D5B6AA6534025B9B107AC910309A98825BF5581E25BEC94AD83B",
                            "createdAt": 1666600519000,
                            "updatedAt": 1666600549000,
                            "remark": "Deposit"
                        }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if currency:
            data["currency"] = currency
        if status:
            data["status"] = status
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if limit:
            data["pageSize"] = limit
        if page:
            data["currentPage"] = page

        return await self._get("deposits", True, data=dict(data, **params))

    async def get_deposit_history(
        self,
        currency=None,
        status=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get deposit history

        https://www.kucoin.com/docs/rest/funding/deposit/get-v1-historical-deposits-list

        :param currency: Name of currency (optional)
        :type currency: string
        :param status: optional - Status of deposit (PROCESSING, SUCCESS, FAILURE)
        :type status: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of transactions
        :type limit: int

        .. code:: python

            deposits = client.get_deposit_history('NEO')
            deposits = client.get_deposit_history('NEO', 'SUCCESS')
            deposits = client.get_deposit_history('NEO', 'SUCCESS', 1540296039000, 1540296039000)
            deposits = client.get_deposit_history('NEO', 'SUCCESS', 1540296039000, 1540296039000, 1, 5)

        :returns: ApiResponse

        .. code:: python

            {
                "currentPage": 1,
                "pageSize": 1,
                "totalNum": 9,
                "totalPage": 9,
                "items": [
                    {
                        "currency": "BTC",
                        "createAt": 1528536998,
                        "amount": "0.03266638",
                        "walletTxId": "55c643bc2c68d6f17266383ac1be9e454038864b929ae7cee0bc408cc5c869e8",
                        "isInner": false,
                        "status": "SUCCESS"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if currency:
            data["currency"] = currency
        if status:
            data["status"] = status
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if limit:
            data["pageSize"] = limit
        if page:
            data["currentPage"] = page

        return await self._get("hist-deposits", True, data=dict(data, **params))

    async def get_user_type(self, **params):
        """Get user type (the current user is a spot high-frequency user or a spot low-frequency user)

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-user-type

        .. code:: python

            deposits = client.get_user_type()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": true // true: high-frequency user, false: low-frequency user
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("hf/accounts/opened", True, data=params)

    # Withdraw Endpoints

    async def get_withdrawals(
        self,
        currency=None,
        status=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get deposit records for a currency

        https://www.kucoin.com/docs/rest/funding/withdrawals/get-withdrawals-list

        :param currency: Name of currency (optional)
        :type currency: string
        :param status: optional - Status of deposit (PROCESSING, SUCCESS, FAILURE)
        :type status: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of transactions
        :type limit: int

        .. code:: python

            withdrawals = client.get_withdrawals('NEO')
            withdrawals = client.get_withdrawals('NEO', 'SUCCESS')
            withdrawals = client.get_withdrawals('NEO', 'SUCCESS', 1540296039000, 1540296039000)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "currentPage": 1,
                    "pageSize": 50,
                    "totalNum": 1,
                    "totalPage": 1,
                    "items": [
                        {
                            "id": "63564dbbd17bef00019371fb",
                            "currency": "XRP",
                            "chain": "xrp",
                            "status": "SUCCESS",
                            "address": "rNFugeoj3ZN8Wv6xhuLegUBBPXKCyWLRkB",
                            "memo": "1919537769",
                            "isInner": false,
                            "amount": "20.50000000",
                            "fee": "0.50000000",
                            "walletTxId": "2C24A6D5B3E7D5B6AA6534025B9B107AC910309A98825BF5581E25BEC94AD83B",
                            "createdAt": 1666600379000,
                            "updatedAt": 1666600511000,
                            "remark": "test"
                        }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if currency:
            data["currency"] = currency
        if status:
            data["status"] = status
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if limit:
            data["pageSize"] = limit
        if page:
            data["currentPage"] = page

        return await self._get("withdrawals", True, data=dict(data, **params))

    async def get_historical_withdrawals(
        self,
        currency=None,
        status=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get historical withdrawals

        https://www.kucoin.com/docs/rest/funding/withdrawals/get-v1-historical-withdrawals-list

        :param currency: Name of currency (optional)
        :type currency: string
        :param status: optional - Status of deposit (PROCESSING, SUCCESS, FAILURE)
        :type status: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of transactions
        :type limit: int

        .. code:: python

            withdrawals = client.get_historical_withdrawals('NEO')
            withdrawals = client.get_historical_withdrawals('NEO', 'SUCCESS')
            withdrawals = client.get_historical_withdrawals('NEO', 'SUCCESS', 1540296039000, 1540296039000)

        :returns: ApiResponse

        .. code:: python

            {
                "currentPage": 1,
                "pageSize": 1,
                "totalNum": 2,
                "totalPage": 2,
                "items": [
                    {
                        "currency": "BTC",
                        "createAt": 1526723468,
                        "amount": "0.534",
                        "address": "33xW37ZSW4tQvg443Pc7NLCAs167Yc2XUV",
                        "walletTxId": "aeacea864c020acf58e51606169240e96774838dcd4f7ce48acf38e3651323f4",
                        "isInner": false,
                        "status": "SUCCESS"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if currency:
            data["currency"] = currency
        if status:
            data["status"] = status
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if limit:
            data["pageSize"] = limit
        if page:
            data["currentPage"] = page

        return await self._get("hist-withdrawals", True, data=dict(data, **params))

    async def get_withdrawal_quotas(self, currency, chain=None, **params):
        """Get withdrawal quotas for a currency

        https://www.kucoin.com/docs/rest/funding/withdrawals/get-withdrawal-quotas

        :param currency: Name of currency
        :type currency: string
        :param chain: (optional) The chain name of currency
        :type chain: string

        .. code:: python

            quotas = client.get_withdrawal_quotas('ETH')

        :returns: ApiResponse

        .. code:: python

            {
                "data": {
                    "limitBTCAmount": "37.83993375",
                    "quotaCurrency": "USDT",
                    "chain": "BTC",
                    "remainAmount": "37.83993375",
                    "innerWithdrawMinFee": "0",
                    "usedBTCAmount": "0.00000000",
                    "limitQuotaCurrencyAmount": "1000000.00000000",
                    "withdrawMinSize": "0.0008",
                    "withdrawMinFee": "0.0005",
                    "precision": 8,
                    "reason": null,
                    "usedQuotaCurrencyAmount": "0",
                    "currency": "BTC",
                    "availableAmount": "0",
                    "isWithdrawEnabled": true
                },
                "code": "200000"
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency}

        if chain is not None:
            data["chain"] = chain

        return await self._get("withdrawals/quotas", True, data=dict(data, **params))

    async def create_withdrawal(
        self,
        currency,
        amount,
        address,
        withdraw_type,
        memo=None,
        is_inner=False,
        remark=None,
        chain=None,
        fee_deduct_type=None,
        **params,
    ):
        """Process a withdrawal

        https://www.kucoin.com/docs/rest/funding/withdrawals/apply-withdraw-v3-

        :param currency: Name of currency
        :type currency: string
        :param amount: Amount to withdraw
        :type amount: number
        :param address: Address to withdraw to
        :type address: string
        :param withdraw_type: Withdrawal type (ADDRESS (withdrawal address), UID, MAIL (email), PHONE (mobile phone number))
        :type withdraw_type: string
        :param memo: (optional) Remark to the withdrawal address
        :type memo: string
        :param is_inner: (optional) Remark to the withdrawal address
        :type is_inner: bool
        :param remark: (optional) Remark
        :type remark: string
        :param chain: (optional) The chain name of currency
        :type chain: string
        :param fee_deduct_type: (optional) Fee deduct type (INTERNAL or EXTERNAL)
        :type fee_deduct_type: string

        .. code:: python

            withdrawal = client.create_withdrawal('NEO', 20, '598aeb627da3355fa3e851', 'ADDRESS')

        :returns: ApiResponse

        .. code:: python

            # todo add response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {
            "currency": currency,
            "amount": amount,
            "address": address,
            "withdraw_type": withdraw_type,
        }

        if memo:
            data["memo"] = memo
        if is_inner:
            data["isInner"] = is_inner
        if remark:
            data["remark"] = remark
        if chain:
            data["chain"] = chain
        if fee_deduct_type:
            data["feeDeductType"] = fee_deduct_type

        return await self._post(
            "withdrawals",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def cancel_withdrawal(self, withdrawal_id, **params):
        """Cancel a withdrawal

        https://www.kucoin.com/docs/rest/funding/withdrawals/cancel-withdrawal

        :param withdrawal_id: ID of withdrawal
        :type withdrawal_id: string

        .. code:: python

            client.cancel_withdrawal('5bffb63303aa675e8bbe18f9')

        :returns: ApiResponse

        .. code:: python

            {
                "withdrawalId": "5bffb63303aa675e8bbe18f9"
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"withdrawalId": withdrawal_id}

        return await self._delete(
            "withdrawals/{}".format(withdrawal_id), True, data=dict(data, **params)
        )

    # Trade Fee Endpoints

    async def get_base_fee(self, currency_type=None, **params):
        """Get base fee

        https://www.kucoin.com/docs/rest/funding/trade-fee/basic-user-fee-spot-margin-trade_hf

        :param currency_type: (optional) Currency type: 0-crypto currency, 1-fiat currency. default is 0-crypto currency
        :type currency_type: string

        .. code:: python

            fee = client.get_base_fee()
            fee = client.get_base_fee(1)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "takerFeeRate": "0.001",
                    "makerFeeRate": "0.001"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if currency_type:
            data["currencyType"] = currency_type

        return await self._get("base-fee", True, data=dict(data, **params))

    async def get_trading_pair_fee(self, symbols, **params):
        """Trading pair actual fee - Spot/Margin/trade_hf

        https://www.kucoin.com/docs/rest/funding/trade-fee/trading-pair-actual-fee-spot-margin-trade_hf

        :param symbols: Trading pair (optional, you can inquire fee rates of 10 trading pairs each time at most)
        :type symbols: string

        .. code:: python

            fee = client.get_trading_pair_fee()
            fee = client.get_trading_pair_fee('BTC-USDT')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": [
                    {
                        "symbol": "BTC-USDT",
                        "takerFeeRate": "0.001",
                        "makerFeeRate": "0.001"
                    },
                    {
                        "symbol": "KCS-USDT",
                        "takerFeeRate": "0.002",
                        "makerFeeRate": "0.0005"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if symbols:
            data["symbols"] = symbols

        return await self._get("trade-fees", True, data=dict(data, **params))

    async def futures_get_trading_pair_fee(self, symbol, **params):
        """Trading pair actual fee - Futures

        https://www.kucoin.com/docs/rest/funding/trade-fee/trading-pair-actual-fee-futures

        :param symbol: Trading pair
        :type symbol: string

        .. code:: python

            fee = client.futures_get_trading_pair_fee('ETHUSDTM')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "symbol": "XBTUSDTM",
                    "takerFeeRate": "0.0006",
                    "makerFeeRate": "0.0002"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get("trade-fees", True, is_futures=True, data=dict(data, **params))

    # Order Endpoints

    async def _get_common_order_data(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
    ):
        """Internal helper for creating a common data for order"""

        data = {"symbol": symbol, "type": type, "side": side}

        if type == self.ORDER_MARKET:
            if not size and not funds:
                raise MarketOrderException("Need size or fund parameter")
            if size and funds:
                raise MarketOrderException("Need size or fund parameter not both")
            if size:
                data["size"] = size
            if funds:
                data["funds"] = funds
            if price:
                raise MarketOrderException(
                    "Cannot use price parameter with market order"
                )
            if time_in_force:
                raise MarketOrderException(
                    "Cannot use time_in_force parameter with market order"
                )
            if cancel_after:
                raise MarketOrderException(
                    "Cannot use cancel_after parameter with market order"
                )
            if post_only:
                raise MarketOrderException(
                    "Cannot use post_only parameter with market order"
                )
            if hidden:
                raise MarketOrderException(
                    "Cannot use hidden parameter with market order"
                )
            if iceberg:
                raise MarketOrderException(
                    "Cannot use iceberg parameter with market order"
                )
            if visible_size:
                raise MarketOrderException(
                    "Cannot use visible_size parameter with market order"
                )

        elif type == self.ORDER_LIMIT:
            if not price:
                raise LimitOrderException("Need price parameter for limit order")
            if funds:
                raise LimitOrderException("Cannot use funds parameter with limit order")
            if not size:
                raise LimitOrderException("Need size parameter for limit order")
            if cancel_after and time_in_force != self.TIMEINFORCE_GOOD_TILL_TIME:
                raise LimitOrderException(
                    'Cancel after only works with time_in_force = "GTT"'
                )
            if hidden and iceberg:
                raise LimitOrderException('Order can be either "hidden" or "iceberg"')
            if iceberg and not visible_size:
                raise LimitOrderException("Iceberg order requires visible_size")
            data["size"] = size
            data["price"] = price
            if time_in_force:
                data["timeInForce"] = time_in_force
            if cancel_after:
                data["cancelAfter"] = cancel_after
            if post_only:
                data["postOnly"] = post_only
            if hidden:
                data["hidden"] = hidden
            if iceberg:
                data["iceberg"] = iceberg
            if visible_size:
                data["visibleSize"] = visible_size

        elif type == self.ORDER_LIMIT_STOP or type == self.ORDER_MARKET_STOP:
            raise KucoinRequestException(
                "Invalid order type {}. Possible types are {} and {}. To create a stop order please use create_stop_order()".format(
                    type, self.ORDER_LIMIT, self.ORDER_MARKET
                )
            )
        else:
            raise KucoinRequestException(
                "Invalid order type {}. Possible types are {} and {}".format(
                    type, self.ORDER_LIMIT, self.ORDER_MARKET
                )
            )

        if client_oid:
            data["clientOid"] = client_oid
        if stp:
            data["stp"] = stp
        if remark:
            data["remark"] = remark
        return data

    async def create_order(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        **params,
    ):
        """Create a spot order

        https://www.kucoin.com/docs/rest/spot-trading/orders/place-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string

        .. code:: python

            order = client.create_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, size=20, price=2000)
            order = client.create_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "orderId": "672a249054d62a0007ae04b8",
                    "clientOid": "988a99edda5e496e95eb6e050c444994"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        trade_type = params.get("trade_type") or params.get("tradeType")
        if trade_type and trade_type != "TRADE":
            raise KucoinRequestException(
                "trade_type is deprecated. Only TRADE (spot) is supported. For margin orders use create_margin_order()"
            )

        if not client_oid:
            client_oid = flat_uuid()

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )
        return await self._post("orders", True, data=dict(data, **params))

    async def create_market_order(
        self,
        symbol,
        side,
        size=None,
        funds=None,
        client_oid=None,
        remark=None,
        stp=None,
        **params,
    ):
        """Create a spot market order

        One of size or funds must be set

        https://www.kucoin.com/docs/rest/spot-trading/orders/place-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency
        :type size: string
        :param funds: (optional) Desired amount of quote currency to use
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string

        .. code:: python

            order = client.create_market_order('ETH-USDT', Client.SIDE_BUY, size=20)

        :returns: ApiResponse

        .. code:: python

            {
                "orderOid": "596186ad07015679730ffa02"
            }

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException

        """

        return await self.create_order(
            symbol,
            self.ORDER_MARKET,
            side,
            size=size,
            funds=funds,
            client_oid=client_oid,
            remark=remark,
            stp=stp,
            **params,
        )

    async def create_limit_order(
        self,
        symbol,
        side,
        price,
        size,
        client_oid=None,
        remark=None,
        time_in_force=None,
        stop=None,
        stop_price=None,
        stp=None,
        trade_type=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        **params,
    ):
        """Create a spot limit order

        https://docs.kucoin.com/#place-a-new-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param side: buy or sell
        :type side: string
        :param price: Name of coin
        :type price: string
        :param size: Amount of base currency to buy or sell
        :type size: string
        :param client_oid: (optional) Unique order_id  default flat_uuid()
        :type client_oid: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param trade_type: (optional) - deprecated - TRADE (spot) is supported only (default is TRADE)
        :type trade_type: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK (default is GTC)
        :type time_in_force: string
        :param stop: (deprecated) not supported
        :param stop_price: (deprecated) not supported
        :param cancel_after: (optional) number of seconds to cancel the order if not filled
            required time_in_force to be GTT
        :type cancel_after: string
        :param post_only: (optional) indicates that the order should only make liquidity. If any part of
            the order results in taking liquidity, the order will be rejected and no part of it will execute.
        :type post_only: bool
        :param hidden: (optional) Orders not displayed in order book
        :type hidden: bool
        :param iceberg:  (optional) Only visible portion of the order is displayed in the order book
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order
        :type visible_size: string

        .. code:: python

            order = client.create_limit_order('KCS-BTC', Client.SIDE_BUY, '0.01', '1000')

        :returns: ApiResponse

        .. code:: python

            {
                "orderOid": "596186ad07015679730ffa02"
            }

        :raises: KucoinResponseException, KucoinAPIException, LimitOrderException

        """

        if stop or stop_price:
            raise KucoinRequestException(
                "stop and stop_price in create_limit_order are deprecated. To create a stop order please use create_stop_order()"
            )

        return await self.create_order(
            symbol,
            self.ORDER_LIMIT,
            side,
            size=size,
            price=price,
            client_oid=client_oid,
            remark=remark,
            stp=stp,
            time_in_force=time_in_force,
            cancel_after=cancel_after,
            post_only=post_only,
            hidden=hidden,
            iceberg=iceberg,
            visible_size=visible_size,
            trade_type=trade_type,
            **params,
        )

    async def create_test_order(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        **params,
    ):
        """Create a test spot order

        https://www.kucoin.com/docs/rest/spot-trading/orders/place-order-test

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string

        .. code:: python

            order = client.create_test_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, size=20, price=2000)
            order = client.create_test_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "orderId": "672cf15bb2cdb8000708765c"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        if not client_oid:
            client_oid = flat_uuid()

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )
        return await self._post("orders/test", True, data=dict(data, **params))

    async def create_orders(self, symbol, order_list, **params):
        """Create multiple spot limit orders

        Maximum of 5 orders can be created at once
        Only limit orders are supported

        https://www.kucoin.com/docs/rest/spot-trading/orders/place-multiple-orders

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_list: List of orders to create
        :type order_list: list of dicts
            every order should have the following keys:
                - side: buy or sell
                - price: Price
                - size: Amount in base currency
                - client_oid: (optional) Unique order id
                - remark: (optional) remark for the order, max 100 utf8 characters
                - stp: (optional) self trade protection CN, CO, CB or DC (default is None)
                - time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC
                - cancel_after: (optional) time in ms to cancel after
                - post_only: (optional) Post only flag
                - hidden: (optional) Hidden order flag
                - iceberg: (optional) Iceberg order flag
                - visible_size: (optional) The maximum visible size of an iceberg order
                - stop: (optional) loss or entry
                - stop_price: (optional) stop price - required for stop orders

        .. code:: python

            order_list = [
                {
                    "side": "buy",
                    "price": "3000",
                    "size": "0.1",
                    "client_oid": "my_order_id_1"
                },
                {
                    "side": "sell",
                    "type": "limit",
                    "price": "3500",
                    "size": "0.1",
                }
            ]
            orders = client.create_orders('ETH-USDT', order_list)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "data": [
                        {
                            "symbol": "ETH-USDT",
                            "type": "limit",
                            "side": "buy",
                            "price": "100",
                            "size": "0.01",
                            "funds": null,
                            "stp": "",
                            "stop": "loss",
                            "stopPrice": "90",
                            "timeInForce": "GTC",
                            "cancelAfter": 0,
                            "postOnly": false,
                            "hidden": false,
                            "iceberge": false,
                            "iceberg": false,
                            "visibleSize": null,
                            "channel": "API",
                            "id": "672e023a54d62a0007a60f73",
                            "status": "success",
                            "failMsg": null,
                            "clientOid": "test_create_orders"
                        }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException, KucoinRequestException, LimitOrderException

        """

        orders = []

        for order in order_list:
            if "type" in order and order["type"] != self.ORDER_LIMIT:
                raise KucoinRequestException(
                    "Only limit orders are supported by create_orders"
                )
            order_data = await self._get_common_order_data(
                symbol,
                self.ORDER_LIMIT,
                order["side"],
                order["size"],
                order["price"],
                client_oid=order.get("client_oid"),
                remark=order.get("remark"),
                stp=order.get("stp"),
                time_in_force=order.get("time_in_force"),
                cancel_after=order.get("cancel_after"),
                post_only=order.get("post_only"),
                hidden=order.get("hidden"),
                iceberg=order.get("iceberg"),
                visible_size=order.get("visible_size"),
            )
            del order_data["symbol"]
            if "clientOid" not in order_data:
                order_data["clientOid"] = flat_uuid()
            if "stop" in order:
                if not "stop_price" in order:
                    raise LimitOrderException("Stop order needs stop_price")
                if order["stop"] not in ["loss", "entry"]:
                    raise LimitOrderException("Stop order type must be loss or entry")
                order_data["stop"] = order["stop"]
                order_data["stopPrice"] = order["stop_price"]
            elif "stop_price" in order:
                raise LimitOrderException(
                    "Stop price is only valid with stop order. Provide stop parameter (loss or entry)"
                )
            orders.append(order_data)

        data = {"symbol": symbol, "orderList": orders}

        return await self._post("orders/multi", True, data=dict(data, **params))

    async def cancel_order(self, order_id, **params):
        """Cancel a spot order

        https://www.kucoin.com/docs/rest/spot-trading/orders/cancel-order-by-orderid

        :param order_id: Order id
        :type order_id: string

        .. code:: python

            res = client.cancel_order('5bd6e9286d99522a52e458de')

        :returns: ApiResponse

        .. code:: python

            {
                "cancelledOrderIds": [
                    "5bd6e9286d99522a52e458de"
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        return await self._delete("orders/{}".format(order_id), True, data=params)

    async def cancel_order_by_client_oid(self, client_oid, **params):
        """Cancel a spot order by the clientOid

        https://www.kucoin.com/docs/rest/spot-trading/orders/cancel-order-by-clientoid

        :param client_oid: ClientOid
        :type client_oid: string

        .. code:: python

            res = client.cancel_order_by_client_oid('6d539dc614db3')

        :returns: ApiResponse

        .. code:: python

            {
                "cancelledOrderId": "5f311183c9b6d539dc614db3",
                "clientOid": "6d539dc614db3"
            }

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        return await self._delete(
            "order/client-order/{}".format(client_oid), True, data=params
        )

    async def cancel_all_orders(self, symbol=None, trade_type=None, **params):
        """Cancel all orders

        https://www.kucoin.com/docs/rest/spot-trading/orders/cancel-all-orders

        :param symbol: (optional) Name of symbol e.g. ETH-USDT
        :type symbol: string
        :param trade_type: (optional) The type of trading:
            TRADE - spot trading, MARGIN_TRADE - cross margin trading, MARGIN_ISOLATED_TRADE - isolated margin trading
            default is TRADE
        :type trade_type: string

        .. code:: python

            res = client.cancel_all_orders()

        :returns: ApiResponse

        .. code:: python

            {
                "cancelledOrderIds": [
                    "5bd6e9286d99522a52e458de"
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """
        data = {}
        if symbol:
            data["symbol"] = symbol
        if trade_type:
            data["tradeType"] = trade_type

        return await self._delete("orders", True, data=dict(data, **params))

    async def get_orders(
        self,
        symbol=None,
        status=None,
        side=None,
        order_type=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        trade_type=None,
        **params,
    ):
        """Get list of orders

        https://www.kucoin.com/docs/rest/spot-trading/orders/get-order-list

        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param status: (optional) Specify status active or done (default done)
        :type status: string
        :param side: (optional) buy or sell
        :type side: string
        :param order_type: (optional) limit, market, limit_stop or market_stop
        :type order_type: string
        :param trade_type: (optional) The type of trading :
            TRADE - spot trading, MARGIN_TRADE - cross margin trading, MARGIN_ISOLATED_TRADE - isolated margin trading
            default is TRADE
        :type trade_type: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            orders = client.get_orders(symbol='KCS-BTC', status='active')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "currentPage": 1,
                    "pageSize": 50,
                    "totalNum": 1,
                    "totalPage": 1,
                    "items": [
                        {
                            "id": "67320d92429d8b0007a962d0",
                            "symbol": "ETH-USDT",
                            "opType": "DEAL",
                            "type": "limit",
                            "side": "buy",
                            "price": "100",
                            "size": "0.01",
                            "funds": "0",
                            "dealFunds": "0",
                            "dealSize": "0",
                            "fee": "0",
                            "feeCurrency": "USDT",
                            "stp": null,
                            "stop": null,
                            "stopTriggered": false,
                            "stopPrice": "0",
                            "timeInForce": "GTC",
                            "postOnly": false,
                            "hidden": false,
                            "iceberg": false,
                            "visibleSize": "0",
                            "cancelAfter": 0,
                            "channel": "API",
                            "clientOid": null,
                            "remark": null,
                            "tags": "partner:ccxt",
                            "isActive": true,
                            "cancelExist": false,
                            "createdAt": 1731333522333,
                            "tradeType": "TRADE"
                        }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if symbol:
            data["symbol"] = symbol
        if status:
            data["status"] = status
        if side:
            data["side"] = side
        if order_type:
            data["type"] = order_type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit
        if trade_type:
            data["tradeType"] = trade_type

        return await self._get("orders", True, data=dict(data, **params))

    async def get_historical_orders(
        self, symbol=None, side=None, start=None, end=None, page=None, limit=None
    ):
        """Deprecated"""

        raise KucoinAPIException(
            "The interface has been deprecated. Please use get_orders"
        )

    async def get_recent_orders(self, page=None, limit=None, **params):
        """Get up to 1000 last orders in the last 24 hours.

        https://www.kucoin.com/docs/rest/spot-trading/orders/get-recent-orders-list

        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            orders = client.get_recent_orders()

        :returns: ApiResponse

        todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if page:
            data["page"] = page
        if limit:
            data["limit"] = limit

        return await self._get("limit/orders", True, data=dict(data, **params))

    async def get_order(self, order_id, **params):
        """Get order details

        https://www.kucoin.com/docs/rest/spot-trading/orders/get-order-details-by-orderid

        :param order_id: orderOid value
        :type order_id: str

        .. code:: python

            order = client.get_order('5c35c02703aa673ceec2a168')

        :returns: ApiResponse

        .. code:: python

            {
                "id": "5c35c02703aa673ceec2a168",
                "symbol": "BTC-USDT",
                "opType": "DEAL",
                "type": "limit",
                "side": "buy",
                "price": "10",
                "size": "2",
                "funds": "0",
                "dealFunds": "0.166",
                "dealSize": "2",
                "fee": "0",
                "feeCurrency": "USDT",
                "stp": "",
                "stop": "",
                "stopTriggered": false,
                "stopPrice": "0",
                "timeInForce": "GTC",
                "postOnly": false,
                "hidden": false,
                "iceberge": false,
                "visibleSize": "0",
                "cancelAfter": 0,
                "channel": "IOS",
                "clientOid": null,
                "remark": null,
                "tags": null,
                "isActive": false,
                "cancelExist": false,
                "createdAt": 1547026471000
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("orders/{}".format(order_id), True, data=params)

    async def get_order_by_client_oid(self, client_oid, **params):
        """Get order details by clientOid

        https://www.kucoin.com/docs/rest/spot-trading/orders/get-order-details-by-clientoid

        :param client_oid: clientOid value
        :type client_oid: str

        .. code:: python

            order = client.get_order_by_client_oid('6d539dc614db312')

        :returns: ApiResponse

        .. code:: python

            {
                "id": "5f3113a1c9b6d539dc614dc6",
                "symbol": "KCS-BTC",
                "opType": "DEAL",
                "type": "limit",
                "side": "buy",
                "price": "0.00001",
                "size": "1",
                "funds": "0",
                "dealFunds": "0",
                "dealSize": "0",
                "fee": "0",
                "feeCurrency": "BTC",
                "stp": "",
                "stop": "",
                "stopTriggered": false,
                "stopPrice": "0",
                "timeInForce": "GTC",
                "postOnly": false,
                "hidden": false,
                "iceberg": false,
                "visibleSize": "0",
                "cancelAfter": 0,
                "channel": "API",
                "clientOid": "6d539dc614db312",
                "remark": "",
                "tags": "",
                "isActive": true,
                "cancelExist": false,
                "createdAt": 1597051810000,
                "tradeType": "TRADE"
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("order/client-order/{}".format(client_oid), True, data=params)

    # HF Order Endpoints

    async def hf_create_order(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        tags=None,
        **params,
    ):
        """Create a hf spot order

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/place-hf-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string
        :param tags: (optional) order tag, length cannot exceed 20 characters (ASCII)
        :type tags: string

        .. code:: python

            order = client.hf_create_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, size=20, price=2000)
            order = client.hf_create_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "orderId": "672a249054d62a0007ae04b8",
                    "clientOid": "988a99edda5e496e95eb6e050c444994"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )

        if tags:
            data["tags"] = tags

        return await self._post("hf/orders", True, data=dict(data, **params))

    async def hf_create_market_order(
        self,
        symbol,
        side,
        size=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        tags=None,
        **params,
    ):
        """Create a hf spot market order

        One of size or funds must be set

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/place-hf-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency
        :type size: string
        :param funds: (optional) Desired amount of quote currency to use
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param tags: (optional) order tag, length cannot exceed 20 characters (ASCII)
        :type tags: string

        .. code:: python

            order = client.hf_create_market_order('ETH-USDT', Client.SIDE_BUY, size=20)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "orderId": "5bd6e9286d99522a52e458de",
                    "clientOid": "11223344"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException

        """

        return await self.hf_create_order(
            symbol,
            self.ORDER_MARKET,
            side,
            size,
            funds=funds,
            client_oid=client_oid,
            stp=stp,
            remark=remark,
            tags=tags,
            **params,
        )

    async def hf_create_limit_order(
        self,
        symbol,
        side,
        price,
        size,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        tags=None,
        **params,
    ):
        """Create a hf spot limit order

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/place-hf-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param side: buy or sell
        :type side: string
        :param price: Name of coin
        :type price: string
        :param size: Amount of base currency to buy or sell
        :type size: string
        :param client_oid: (optional) Unique order_id  default flat_uuid()
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK (default is GTC)
        :type time_in_force: string
        :param cancel_after: (optional) number of seconds to cancel the order if not filled
            required time_in_force to be GTT
        :type cancel_after: string
        :param post_only: (optional) indicates that the order should only make liquidity. If any part of
            the order results in taking liquidity, the order will be rejected and no part of it will execute.
        :type post_only: bool
        :param hidden: (optional) Orders not displayed in order book
        :type hidden: bool
        :param iceberg:  (optional) Only visible portion of the order is displayed in the order book
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order
        :type visible_size: bool
        :param tags: (optional) order tag, length cannot exceed 20 characters (ASCII)
        :type tags: string

        .. code:: python

            order = client.hf_create_limit_order('KCS-BTC', Client.SIDE_BUY, '0.01', '1000')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "orderId": "5bd6e9286d99522a52e458de",
                    "clientOid": "11223344"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException, LimitOrderException

        """

        return await self.hf_create_order(
            symbol,
            self.ORDER_LIMIT,
            side,
            size,
            price=price,
            client_oid=client_oid,
            stp=stp,
            remark=remark,
            time_in_force=time_in_force,
            cancel_after=cancel_after,
            post_only=post_only,
            hidden=hidden,
            iceberg=iceberg,
            visible_size=visible_size,
            tags=tags,
            **params,
        )

    async def hf_create_test_order(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        tags=None,
        **params,
    ):
        """Create a hf test spot order

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/place-hf-order-test

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string
        :param tags: (optional) order tag, length cannot exceed 20 characters (ASCII)
        :type tags: string

        .. code:: python

            order = client.hf_create_test_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, size=20, price=2000)
            order = client.hf_create_test_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "orderId": "672a249054d62a0007ae04b8",
                    "clientOid": "988a99edda5e496e95eb6e050c444994"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )

        if tags:
            data["tags"] = tags

        return await self._post("hf/orders/test", True, data=dict(data, **params))

    async def sync_hf_create_order(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        tags=None,
        **params,
    ):
        """Create a hf spot order
        The difference between this interface and hf_create_order is that this interface will
        synchronously return the order information after the order matching is completed

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/sync-place-hf-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string
        :param tags: (optional) order tag, length cannot exceed 20 characters (ASCII)
        :type tags: string

        .. code:: python

            order = client.sync_hf_create_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, size=20, price=2000)
            order = client.sync_hf_create_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "orderId": "673219d13cda6500071f613d",
                    "orderTime": 1731336657616,
                    "originSize": "0",
                    "dealSize": "0.0003158",
                    "remainSize": "0",
                    "canceledSize": "0",
                    "originFunds": "1",
                    "dealFunds": "0.999709112",
                    "remainFunds": "0",
                    "canceledFunds": "0.000290888",
                    "status": "done",
                    "matchTime": 1731336657641
                }
            }

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )

        if tags:
            data["tags"] = tags

        return await self._post("hf/orders/sync", True, data=dict(data, **params))

    async def hf_create_orders(self, order_list, **params):
        """Create multiple hf spot orders

        Maximum of 5 orders can be created at once

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/place-multiple-orders

        :param order_list: List of orders to create
        :type order_list: list of dicts
            every order should have the following keys:
                - symbol: Name of symbol e.g. ETH-USDT
                - type: order type (limit or market)
                - side: buy or sell
                - size: amount in base currency
                - price: (optional) price (mandatory for limit order)
                - client_oid: (optional) unique order id
                - remark: (optional) remark for the order, max 100 utf8 characters
                - stp: (optional) self trade protection CN, CO, CB or DC (default is None)
                - time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC
                - cancel_after: (optional) time in ms to cancel after
                - post_only: (optional) Post only flag
                - hidden: (optional) Hidden order flag
                - iceberg: (optional) Iceberg order flag
                - visible_size: (optional) The maximum visible size of an iceberg order
                - tags: (optional) order tag, length cannot exceed 20 characters (ASCII)

        .. code:: python

            order_list = [
                {
                    "symbol": "ETH-USDT",
                    "side": "buy",
                    'type': 'market',
                    "size": "0.1",
                    "client_oid": "my_order_id_1"
                },
                {
                    "symbol": "ETH-USDT",
                    "side": "sell",
                    "type": "limit",
                    "price": "3500",
                    "size": "0.1",
                }
            ]
            orders = client.hf_create_orders(order_list)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, KucoinRequestException, LimitOrderException

        """

        orders = []

        for order in order_list:
            order_data = await self._get_common_order_data(
                order.get("symbol"),
                order.get("type"),
                order.get("side"),
                order.get("size"),
                order.get("price"),
                order.get("funds"),
                order.get("client_oid"),
                order.get("stp"),
                order.get("remark"),
                order.get("time_in_force"),
                order.get("cancel_after"),
                order.get("post_only"),
                order.get("hidden"),
                order.get("iceberg"),
                order.get("visible_size"),
            )
            if "tags" in order:
                order_data["tags"] = order["tags"]
            orders.append(order_data)

        data = {"orderList": orders}

        return await self._post("hf/orders/multi", True, data=dict(data, **params))

    async def sync_hf_create_orders(self, order_list, **params):
        """Create multiple hf spot orders

        The difference between this interface and hf_create_orders is that this interface will
        synchronously return the order information after the order matching is completed
        Maximum of 20 orders can be created at once

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/sync-place-multiple-hf-orders

        :param order_list: List of orders to create
        :type order_list: list of dicts
            every order should have the following keys:
                - symbol: Name of symbol e.g. ETH-USDT
                - type: order type (limit or market)
                - side: buy or sell
                - size: amount in base currency
                - price: (optional) price (mandatory for limit order)
                - client_oid: (optional) unique order id
                - remark: (optional) remark for the order, max 100 utf8 characters
                - stp: (optional) self trade protection CN, CO, CB or DC (default is None)
                - time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC
                - cancel_after: (optional) time in ms to cancel after
                - post_only: (optional) Post only flag
                - hidden: (optional) Hidden order flag
                - iceberg: (optional) Iceberg order flag
                - visible_size: (optional) The maximum visible size of an iceberg order
                - tags: (optional) order tag, length cannot exceed 20 characters (ASCII)

        .. code:: python

            order_list = [
                {
                    {
                    "symbol": "ETH-USDT",
                    "side": "buy",
                    'type': 'market',
                    "size": "0.1",
                    "client_oid": "my_order_id_1"
                },
                {
                    "symbol": "ETH-USDT",
                    "side": "sell",
                    "type": "limit",
                    "price": "3500",
                    "size": "0.1",
                }
            ]
            orders = client.sync_hf_create_orders(order_list)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, KucoinRequestException, LimitOrderException

        """

        orders = []

        for order in order_list:
            order_data = await self._get_common_order_data(
                order.get("symbol"),
                order.get("type"),
                order.get("side"),
                order.get("size"),
                order.get("price"),
                order.get("funds"),
                order.get("client_oid"),
                order.get("stp"),
                order.get("remark"),
                order.get("time_in_force"),
                order.get("cancel_after"),
                order.get("post_only"),
                order.get("hidden"),
                order.get("iceberg"),
                order.get("visible_size"),
            )
            if "tags" in order:
                order_data["tags"] = order["tags"]
            orders.append(order_data)

        data = {"orderList": orders}

        return await self._post("hf/orders/multi/sync", True, data=dict(data, **params))

    async def hf_modify_order(
        self,
        symbol,
        order_id=None,
        client_oid=None,
        new_size=None,
        new_price=None,
        **params,
    ):
        """Modify an existing hf order

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/modify-hf-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_id: OrderId
        :type order_id: string
        :param client_oid: ClientOid
        :type client_oid: string
        :param new_size: (optional) Desired amount in base currency
        :type new_size: string
        :param new_price: (optional) Price
        :type new_price: string

        .. code:: python

            order = client.hf_modify_order('ETH-USDT', order_id='5c35c02703aa673ceec2a168', new_size='0.2')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        if not order_id and not client_oid:
            raise KucoinAPIException("Either order_id or client_oid is required")
        if order_id and client_oid:
            raise KucoinAPIException(
                "Either order_id or client_oid is required, not both"
            )

        if order_id:
            data["orderId"] = order_id
        if client_oid:
            data["clientOid"] = client_oid
        if new_size:
            data["newSize"] = new_size
        if new_price:
            data["newPrice"] = new_price

        return await self._post("hf/orders/alter", True, data=dict(data, **params))

    async def hf_cancel_order(self, order_id, symbol, **params):
        """Cancel an hf order by the orderId

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/cancel-hf-order-by-orderid

        :param order_id: OrderId
        :type order_id: string
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            res = client.hf_cancel_order('5bd6e9286d99522a52e458de', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {"symbol": symbol}

        return await self._delete(
            "hf/orders/{}".format(order_id), True, data=dict(data, **params)
        )

    async def sync_hf_cancel_order(self, order_id, symbol, **params):
        """Cancel an hf order by the orderId
        The difference between this interface and hf_cancel_order is that this interface will
        synchronously return the order information after the order canceling is completed.

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/sync-cancel-hf-order-by-orderid


        :param order_id: OrderId
        :type order_id: string
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            res = client.sync_hf_cancel_order('5bd6e9286d99522a52e458de', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {"symbol": symbol}

        return await self._delete(
            "hf/orders/sync/{}".format(order_id), True, data=dict(data, **params)
        )

    async def hf_cancel_order_by_client_oid(self, client_oid, symbol, **params):
        """Cancel a hf order by the clientOid

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/cancel-hf-order-by-clientoid

        :param client_oid: ClientOid
        :type client_oid: string
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            res = client.hf_cancel_order_by_client_oid('6d539dc614db3', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {"symbol": symbol}

        return await self._delete(
            "hf/orders/client-order{}".format(client_oid),
            True,
            data=dict(data, **params),
        )

    async def sync_hf_cancel_order_by_client_oid(self, client_oid, symbol, **params):
        """Cancel a hf order by the clientOid
        The difference between this interface and hf_cancel_order is that this interface will
        synchronously return the order information after the order canceling is completed.

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/sync-cancel-hf-order-by-orderid

        :param client_oid: ClientOid
        :type client_oid: string
        :param symbol: Name of symbol e.g. ETH-USDT
        :type symbol: string

        .. code:: python

            res = client.sync_hf_cancel_order_by_client_oid('6d539dc614db3', 'ETH-USDT')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {"symbol": symbol}

        return await self._delete(
            "hf/orders/sync/client-order/{}".format(client_oid),
            True,
            data=dict(data, **params),
        )

    async def hf_cancel_specified_quantity_of_order(
        self, order_id, symbol, cancel_size, **params
    ):
        """Cancel a specified quantity of an hf order by the orderId

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/cancel-specified-number-hf-orders-by-orderid

        :param order_id: OrderId
        :type order_id: string
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param cancel_size: The quantity to cancel
        :type cancel_size: string

        .. code:: python

            res = client.hf_cancel_specified_quantity_of_order('5bd6e9286d99522a52e458de', 'ETH-USDT, '0.1')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException

        """

        data = {"symbol": symbol, "cancelSize": cancel_size}

        return await self._delete(
            "hf/orders/cancel/{}".format(order_id), True, data=dict(data, **params)
        )

    async def hf_cancel_orders_by_symbol(self, symbol, **params):
        """Cancel all hf orders by symbol

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/cancel-all-hf-orders-by-symbol

        :param symbol: Name of symbol e.g. ETH-USDT
        :type symbol: string

        .. code:: python

            res = client.hf_cancel_orders_by_symbol('ETH-USDT')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._delete("hf/orders", True, data=dict(data, **params))

    async def hf_cancel_all_orders(self, **params):
        """Cancel all hf orders

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/cancel-all-hf-orders

        .. code:: python

            res = client.hf_cancel_all_orders()

        :returns: ApiResponse

        .. code:: python

            {
                "succeedSymbols": [
                    "ETH-USDT"
                ],
                "failedSymbols": [
                    {
                        "symbol": "BTC-USDT",
                        "error": "can't cancel, system timeout"
                    }
                ],
            }

        :raises: KucoinResponseException, KucoinAPIException

        """
        return await self._delete("hf/orders/cancelAll", True, data=params)

    async def hf_get_active_orders(self, symbol, **params):
        """Get a list of active hf orders

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-active-hf-orders-list

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            orders = client.hf_get_active_orders('ETH-USDT')

        :returns: ApiResponse

        .. code:: python

            {
                "code" : "200000",
                "data" : [
                    "id": "5c35c02703aa673ceec2a168",
                    "symbol": "BTC-USDT",
                    "opType": "DEAL",
                    "type": "limit",
                    "side": "buy",
                    "price": "10",
                    "size": "2",
                    "funds": "0",
                    "dealFunds": "0.166",
                    "dealSize": "2",
                    "fee": "0",
                    "feeCurrency": "USDT",
                    "stp": "",
                    "timeInForce": "GTC",
                    "postOnly": false,
                    "hidden": false,
                    "iceberg": false,
                    "visibleSize": "0",
                    "cancelAfter": 0,
                    "channel": "IOS",
                    "clientOid": "",
                    "remark": "",
                    "tags": "",
                    "active": true,
                    "inOrderBook": true,
                    "cancelExist": false,
                    "createdAt": 1547026471000,
                    "lastUpdatedAt": 1547026471001,
                    "tradeType": "TRADE",
                    "cancelledSize": "0",
                    "cancelledFunds": "0",
                    "remainSize": "0",
                    "remainFunds": "0"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get("hf/orders/active", True, data=dict(data, **params))

    async def hf_get_symbol_with_active_orders(self, **params):
        """Get a list of symbols with active hf orders

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-symbol-with-active-hf-orders-list

        .. code:: python

            orders = client.hf_get_symbol_with_active_orders()

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": {
                    "symbols": ["BTC-USDT"]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("hf/orders/active/symbols", True, data=params)

    async def hf_get_completed_orders(
        self,
        symbol,
        side=None,
        type=None,
        start=None,
        end=None,
        last_id=None,
        limit=None,
        **params,
    ):
        """Get a list of completed hf orders

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-hf-completed-order-list

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param side: (optional) buy or sell
        :type side: string
        :param type: (optional) limit, market, limit_stop or market_stop
        :type type: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param last_id: (optional) The last orderId of the last page
        :type last_id: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            orders = client.hf_get_completed_orders('ETH-USDT')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "lastId": 2682265600,
                    "items": [
                    {
                        "id": "63074a5a27ecbe0001e1f3ba",
                        "symbol": "CSP-USDT",
                        "opType": "DEAL",
                        "type": "limit",
                        "side": "sell",
                        "price": "0.1",
                        "size": "0.1",
                        "funds": "0.01",
                        "dealSize": "0",
                        "dealFunds": "0",
                        "fee": "0",
                        "feeCurrency": "USDT",
                        "stp": "",
                        "timeInForce": "GTC",
                        "postOnly": false,
                        "hidden": false,
                        "iceberg": false,
                        "visibleSize": "0",
                        "cancelAfter": 0,
                        "channel": "API",
                        "clientOid": "",
                        "remark": "",
                        "tags": "",
                        "cancelExist": true,
                        "createdAt": 1661422170924,
                        "lastUpdatedAt": 1661422196926,
                        "tradeType": "TRADE",
                        "inOrderBook": false,
                        "active": false,
                        "cancelledSize": "0",
                        "cancelledFunds": "0",
                        "remainSize": "0",
                        "remainFunds": "0"
                    }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        if side:
            data["side"] = side
        if type:
            data["type"] = type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if last_id:
            data["lastId"] = last_id
        if limit:
            data["limit"] = limit

        return await self._get("hf/orders/done", True, data=dict(data, **params))

    async def hf_get_order(self, order_id, symbol, **params):
        """Get an hf order details by the orderId

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-hf-order-details-by-orderid

        :param order_id: OrderId
        :type order_id: string
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            order = client.hf_get_order('5bd6e9286d99522a52e458de', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "id": "5f3113a1c9b6d539dc614dc6",
                    "symbol": "KCS-BTC",
                    "opType": "DEAL",
                    "type": "limit",
                    "side": "buy",
                    "price": "0.00001",
                    "size": "1",
                    "funds": "0",
                    "dealFunds": "0",
                    "dealSize": "0",
                    "fee": "0",
                    "feeCurrency": "BTC",
                    "stp": "",
                    "timeInForce": "GTC",
                    "postOnly": false,
                    "hidden": false,
                    "iceberg": false,
                    "visibleSize": "0",
                    "cancelAfter": 0,
                    "channel": "API",
                    "clientOid": "6d539dc614db312",
                    "remark": "",
                    "tags": "",
                    "active": true,
                    "inOrderBook": false,
                    "cancelExist": false,
                    "createdAt": 1547026471000,
                    "lastUpdatedAt": 1547026471001,
                    "tradeType": "TRADE",
                    "cancelledSize": "0",
                    "cancelledFunds": "0",
                    "remainSize": "0",
                    "remainFunds": "0"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "hf/orders/{}".format(order_id), True, data=dict(data, **params)
        )

    async def hf_get_order_by_client_oid(self, client_oid, symbol, **params):
        """Get hf order details by clientOid

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-hf-order-details-by-clientoid

        :param client_oid: clientOid value
        :type client_oid: str
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            order = client.hf_get_order_by_client_oid('6d539dc614db312', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "hf/orders/client-order/{}".format(client_oid),
            True,
            data=dict(data, **params),
        )

    async def hf_auto_cancel_order(self, timeout, symbol=None, **params):
        """Auto cancel a hf order

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/auto-cancel-hf-order-setting

        :param timeout: The timeout period in ms
        :type timeout: int
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            res = client.hf_auto_cancel_order(60000)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "currentTime": 1682010526,
                    "triggerTime": 1682010531
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"timeout": timeout}

        if symbol:
            data["symbol"] = symbol

        return await self._post("hf/orders/dead-cancel-all", True, data=dict(data, **params))

    async def hf_get_auto_cancel_order(self, **params):
        """Get auto cancel setting

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/auto-cancel-hf-order-setting-query

        .. code:: python

            res = client.hf_get_auto_cancel_order()

        :returns: ApiResponse

        .. code:: python

            {
                "timeout": 5,
                "symbols": "BTC-USDT",
                "currentTime": 1682010526,
                "triggerTime": 1682010531
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("hf/orders/dead-cancel-all", True, data=params)

    # Stop Orders

    async def create_stop_order(
        self,
        symbol,
        type,
        side,
        stop_price,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        stop=None,
        trade_type=None,
        **params,
    ):
        """Create a stop order

        https://www.kucoin.com/docs/rest/spot-trading/stop-order/place-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param stop_price: Stop price
        :type stop_price: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string
        :param stop: (optional) stop type - loss or entry (default is loss)
        :type stop: string
        :param trade_type: (optional) TRADE (Spot Trading), MARGIN_TRADE (Margin Trading), MARGIN_ISOLATED_TRADE (Isolated Margin Trading), default is TRADE.
        :type trade_type: string

        .. code:: python

            order = client.create_stop_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, stop_price=2100, size=20, price=2000)
            order = client.create_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, stop_price=2100, funds=20)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "orderId": "672a249054d62a0007ae04b8",
                    "clientOid": "988a99edda5e496e95eb6e050c444994"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        if not client_oid:
            client_oid = flat_uuid()

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )

        data["stopPrice"] = stop_price
        if stop:
            data["stop"] = stop
        if trade_type:
            data["tradeType"] = trade_type

        return await self._post("stop-order", True, data=dict(data, **params))

    async def cancel_stop_order(self, order_id, **params):
        """Cancel a stop order

        https://www.kucoin.com/docs/rest/spot-trading/stop-order/cancel-order-by-orderid

        :param order_id: Order id
        :type order_id: string

        .. code:: python

            res = client.cancel_stop_order('5bd6e9286d99522a52e458de')

        :returns: ApiResponse

        .. code:: python

            {
                "cancelledOrderIds": [
                    "5bd6e9286d99522a52e458de"
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        return await self._delete("stop-order/{}".format(order_id), True, data=params)

    async def cancel_stop_order_by_client_oid(self, client_oid, symbol=None, **params):
        """Cancel a spot order by the clientOid

        https://www.kucoin.com/docs/rest/spot-trading/orders/cancel-order-by-clientoid

        :param client_oid: ClientOid
        :type client_oid: string
        :param symbol: (optional) Name of symbol e.g. ETH-USDT
        :type symbol: string

        .. code:: python

            res = client.cancel_order_by_client_oid('6d539dc614db3')

        :returns: ApiResponse

        .. code:: python

            {
                "cancelledOrderId": "5f311183c9b6d539dc614db3",
                "clientOid": "6d539dc614db3"
            }

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {"clientOid": client_oid}

        if symbol:
            data["symbol"] = symbol

        return await self._delete(
            "stop-order/cancelOrderByClientOid", True, data=dict(data, **params)
        )

    async def cancel_all_stop_orders(
        self, symbol=None, trade_type=None, order_ids=None, **params
    ):
        """Cancel all stop orders

        https://www.kucoin.com/docs/rest/spot-trading/stop-order/cancel-stop-orders

        :param symbol: (optional) Name of symbol e.g. ETH-USDT
        :type symbol: string
        :param trade_type: (optional) The type of trading:
            TRADE - spot trading, MARGIN_TRADE - cross margin trading, MARGIN_ISOLATED_TRADE - isolated margin trading
            default is TRADE
        :type trade_type: string
        :param order_ids: (optional) Comma seperated order IDs (e.g. '5bd6e9286d99522a52e458de,5bd6e9286d99522a52e458df')
        :type order_ids: string

        .. code:: python

            res = client.cancel_all_stop_orders()

        :returns: ApiResponse

        .. code:: python

            {
                "cancelledOrderIds": [
                    "5bd6e9286d99522a52e458de"
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """
        data = {}
        if symbol:
            data["symbol"] = symbol
        if trade_type:
            data["tradeType"] = trade_type
        if order_ids:
            data["orderIds"] = order_ids

        return await self._delete("stop-order/cancel", True, data=dict(data, **params))

    async def get_stop_orders(
        self,
        symbol=None,
        side=None,
        order_type=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        trade_type=None,
        order_ids=None,
        stop=None,
        **params,
    ):
        """Get list of stop orders

        https://www.kucoin.com/docs/rest/spot-trading/stop-order/get-stop-orders-list

        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param side: (optional) buy or sell
        :type side: string
        :param order_type: (optional) limit, market, limit_stop or market_stop
        :type order_type: string
        :param trade_type: (optional) The type of trading :
            TRADE - spot trading, MARGIN_TRADE - cross margin trading, MARGIN_ISOLATED_TRADE - isolated margin trading
            default is TRADE
        :type trade_type: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int
        :param order_ids: (optional) Comma seperated order IDs (e.g. '5bd6e9286d99522a52e458de,5bd6e9286d99522a52e458df')
        :type order_ids: string
        :param stop: (optional) stop (stop loss order) or oco (oco order) todo check this parameter
        :type stop: string

        .. code:: python

            orders = client.get_stop_orders(symbol='KCS-BTC', side='sell')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if symbol:
            data["symbol"] = symbol
        if side:
            data["side"] = side
        if order_type:
            data["type"] = order_type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit
        if trade_type:
            data["tradeType"] = trade_type
        if order_ids:
            data["orderIds"] = order_ids
        if stop:
            data["stop"] = stop

        return await self._get("stop-order", True, data=dict(data, **params))

    async def get_stop_order(self, order_id, **params):
        """Get stop order details

        https://www.kucoin.com/docs/rest/spot-trading/stop-order/get-order-details-by-orderid

        :param order_id: orderOid value
        :type order_id: str

        .. code:: python

            order = client.get_stop_order('5c35c02703aa673ceec2a168')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("stop-order/{}".format(order_id), True, data=params)

    async def get_stop_order_by_client_oid(self, client_oid, symbol=None, **params):
        """Get stop order details by clientOid

        https://www.kucoin.com/docs/rest/spot-trading/stop-order/get-order-details-by-clientoid

        :param client_oid: clientOid value
        :type client_oid: str
        :param symbol: (optional) Name of symbol e.g. ETH-USDT
        :type symbol: string

        .. code:: python

            order = client.get_stop_order_by_client_oid('6d539dc614db312')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"clientOid": client_oid}

        if symbol:
            data["symbol"] = symbol

        return await self._get(
            "stop-order/queryOrderByClientOid", True, data=dict(data, **params)
        )

    # OCO Orders

    async def oco_create_order(
        self,
        symbol,
        side,
        size,
        price,
        stop_price,
        limit_price,
        client_oid=None,
        remark=None,
        **params,
    ):
        """Create an OCO order

        https://www.kucoin.com/docs/rest/spot-trading/oco-order/place-order

        :param symbol: Name of symbol e.g. ETH-USDT
        :type symbol: string
        :param side: buy or sell
        :type side: string
        :param size: Desired amount in base currency
        :type size: string
        :param price: price
        :type price: string
        :param stop_price: trigger price
        :type stop_price: string
        :param limit_price: limit order price after take-profit and stop-loss are triggered
        :type limit_price: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string

        .. code:: python

            order = client.oco_create_order('ETH-USDT', Client.SIDE_BUY, size=20, price=2000, stop_price=2100, limit_price=2200)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {
            "symbol": symbol,
            "side": side,
            "size": size,
            "price": price,
            "stopPrice": stop_price,
            "limitPrice": limit_price,
        }

        if not client_oid:
            client_oid = flat_uuid()
        else:
            data["clientOid"] = client_oid

        if remark:
            data["remark"] = remark

        return await self._post(
            "oco/order", True, api_version=self.API_VERSION3, data=dict(data, **params)
        )

    async def oco_cancel_order(self, order_id, **params):
        """Cancel an oco order

        https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-order-by-orderid

        :param order_id: Order id
        :type order_id: string

        .. code:: python

            res = client.oco_cancel_order('5bd6e9286d99522a52e458de')

        :returns: ApiResponse

        todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        return await self._delete(
            "oco/order/{}".format(order_id),
            True,
            api_version=self.API_VERSION3,
            data=params,
        )

    async def oco_cancel_order_by_client_oid(self, client_oid, **params):
        """Cancel a spot order by the clientOid

        https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-order-by-clientoid

        :param client_oid: ClientOid
        :type client_oid: string

        .. code:: python

            res = client.oco_cancel_order_by_client_oid('6d539dc614db3')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        return await self._delete(
            "oco/client-order/{}".format(client_oid),
            True,
            api_version=self.API_VERSION3,
            data=params,
        )

    async def oco_cancel_all_orders(self, symbol=None, order_ids=None, **params):
        """Cancel all oco orders

        https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-multiple-orders

        :param symbol: (optional) Name of symbol e.g. ETH-USDT
        :type symbol: string
        :param order_ids: (optional) Comma seperated order IDs (e.g. '5bd6e9286d99522a52e458de,5bd6e9286d99522a52e458df')
        :type order_ids: string

        .. code:: python

            res = client.oco_cancel_all_orders()

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """
        data = {}
        if symbol:
            data["symbol"] = symbol
        if order_ids:
            data["orderIds"] = order_ids

        return await self._delete(
            "oco/orders", True, api_version=self.API_VERSION3, data=dict(data, **params)
        )

    async def oco_get_order_info(self, order_id, **params):
        """Get oco order information
        for the order details use oco_get_order()

        https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-info-by-orderid

        :param order_id: orderOid value
        :type order_id: str

        .. code:: python

            order = client.oco_get_order_info('5c35c02703aa673ceec2a168')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get(
            "oco/order/{}".format(order_id),
            True,
            api_version=self.API_VERSION3,
            data=params,
        )

    async def oco_get_order(self, order_id, **params):
        """Get oco order information

        https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-details-by-orderid

        :param order_id: orderOid value
        :type order_id: str

        .. code:: python

            order = client.oco_get_order('5c35c02703aa673ceec2a168')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get(
            "oco/order/details/{}".format(order_id),
            True,
            api_version=self.API_VERSION3,
            data=params,
        )

    async def oco_get_order_by_client_oid(self, client_oid, **params):
        """Get oco order details by clientOid

        https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-info-by-clientoid

        :param client_oid: clientOid value
        :type client_oid: string

        .. code:: python

            order = client.oco_get_order_by_client_oid('6d539dc614db312')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get(
            "oco/client-order/{}".format(client_oid),
            True,
            api_version=self.API_VERSION3,
            data=params,
        )

    async def oco_get_orders(
        self,
        symbol=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        order_ids=None,
        **params,
    ):
        """Get list of oco orders

        https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-list

        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int
        :param order_ids: (optional) Comma seperated order IDs (e.g. '5bd6e9286d99522a52e458de,5bd6e9286d99522a52e458df')
        :type order_ids: string

        .. code:: python

            orders = client.oco_get_orders(symbol='KCS-BTC')

        :returns: ApiResponse
        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if symbol:
            data["symbol"] = symbol
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit
        if order_ids:
            data["orderIds"] = order_ids

        return await self._get(
            "oco/orders", True, api_version=self.API_VERSION3, data=dict(data, **params)
        )

    # Margin Orders

    async def margin_create_order(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        margin_model=None,
        auto_borrow=None,
        auto_repay=None,
        **params,
    ):
        """Create a margin order

        https://www.kucoin.com/docs/rest/margin-trading/orders/place-margin-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string
        :param margin_model: (optional) cross or isolated (default is cross)
        :type margin_model: string
        :param auto_borrow: (optional) auto borrow flag (default is False). If true the system will first borrow you funds
            at the optimal interest rate and then place an order for you. Currently autoBorrow parameter
            only supports cross mode, not isolated mode. When add this param, stop profit and stop loss are not supported,
            if it is a sell order, the size must be passed
        :type auto_borrow: bool
        :param auto_repay: (optional) auto repay flag (default is False). Automatically repay when placing an order,
            that is, the system automatically triggers repayment after the order is completed.
            The maximum currency repayment amount is the trade amount.
            The same order does not support the simultaneous use of autoBorrow and autoRepay.

        .. code:: python

            order = client.margin_create_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, size=20, price=2000)
            order = client.margin_create_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        if not client_oid:
            client_oid = flat_uuid()

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )

        if margin_model:
            data["marginModel"] = margin_model
        if auto_borrow and auto_repay:
            raise KucoinRequestException(
                "auto_borrow and auto_repay cannot be used together"
            )
        if auto_borrow:
            data["autoBorrow"] = auto_borrow
        if auto_repay:
            data["autoRepay"] = auto_repay

        return await self._post("margin/order", True, data=dict(data, **params))

    async def margin_create_test_order(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        margin_model=None,
        auto_borrow=None,
        auto_repay=None,
        **params,
    ):
        """Create a margin test order

        https://www.kucoin.com/docs/rest/margin-trading/orders/place-margin-order-test

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string
        :param margin_model: (optional) cross or isolated (default is cross)
        :type margin_model: string
        :param auto_borrow: (optional) auto borrow flag (default is False). If true the system will first borrow you funds
            at the optimal interest rate and then place an order for you. Currently autoBorrow parameter
            only supports cross mode, not isolated mode. When add this param, stop profit and stop loss are not supported,
            if it is a sell order, the size must be passed
        :type auto_borrow: bool
        :param auto_repay: (optional) auto repay flag (default is False). Automatically repay when placing an order,
            that is, the system automatically triggers repayment after the order is completed.
            The maximum currency repayment amount is the trade amount.
            The same order does not support the simultaneous use of autoBorrow and autoRepay.

        .. code:: python

            order = client.margin_create_test_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, size=20, price=2000)
            order = client.margin_create_test_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        if not client_oid:
            client_oid = flat_uuid()

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )

        if margin_model:
            data["marginModel"] = margin_model
        if auto_borrow and auto_repay:
            raise KucoinRequestException(
                "auto_borrow and auto_repay cannot be used together"
            )
        if auto_borrow:
            data["autoBorrow"] = auto_borrow
        if auto_repay:
            data["autoRepay"] = auto_repay

        return await self._post("margin/order/test", True, data=dict(data, **params))

    # HF Margin Orders

    async def hf_margin_create_order(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        is_isolated=None,
        auto_borrow=None,
        auto_repay=None,
        **params,
    ):
        """Create an hf margin order

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/place-hf-order

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string
        :param is_isolated: (optional) True for isolated margin, False for cross margin (default is False)
        :type margin_model: bool
        :param auto_borrow: (optional) auto borrow flag (default is False).
            When Margin HFTrading Account has inefficient balance,
            System autoborrows inefficient assets and opens positions
            according to the lowest market interest rate.
        :type auto_borrow: bool
        :param auto_repay: (optional) auto repay flag (default is False).
            AutoPay allows returning borrowed assets when you close a position.
            System automatically triggers the repayment and the maximum repayment
            amount equals to the filled-order amount.

        .. code:: python

            order = client.hf_margin_create_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, size=20, price=2000)
            order = client.hf_margin_create_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        if not client_oid:
            client_oid = flat_uuid()

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )

        if is_isolated:
            data[
                "isIsolated"
            ] = is_isolated  # todo check this parameter for margin_create_order
        if auto_borrow:
            data["autoBorrow"] = auto_borrow
        if auto_repay:
            data["autoRepay"] = auto_repay

        return await self._post(
            "hf/margin/order",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def hf_margin_create_test_order(
        self,
        symbol,
        type,
        side,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        cancel_after=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        is_isolated=None,
        auto_borrow=None,
        auto_repay=None,
        **params,
    ):
        """Create an hf margin test order

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/place-hf-order-test

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param type: order type (limit or market)
        :type type: string
        :param side: buy or sell
        :type side: string
        :param size: (optional) Desired amount in base currency (required for limit order)
        :type size: string
        :param price: (optional) Price (required for limit order)
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use (for market order only)
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO, CB or DC (default is None)
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC, GTT, IOC, or FOK - default is GTC (for limit order only)
        :type time_in_force: string
        :param cancel_after: (optional) time in ms to cancel after (for limit order only)
        :type cancel_after: string
        :param post_only: (optional) Post only flag (for limit order only)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (for limit order only)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (for limit order only)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order (for limit orders only)
        :type visible_size: string
        :param is_isolated: (optional) True for isolated margin, False for cross margin (default is False)
        :type margin_model: bool
        :param auto_borrow: (optional) auto borrow flag (default is False).
            When Margin HFTrading Account has inefficient balance,
            System autoborrows inefficient assets and opens positions
            according to the lowest market interest rate.
        :type auto_borrow: bool
        :param auto_repay: (optional) auto repay flag (default is False).
            AutoPay allows returning borrowed assets when you close a position.
            System automatically triggers the repayment and the maximum repayment
            amount equals to the filled-order amount.

        .. code:: python

            order = client.hf_margin_create_test_order('ETH-USDT', Client.ORDER_LIMIT, Client.SIDE_BUY, size=20, price=2000)
            order = client.hf_margin_create_test_order('ETH-USDT', Client.ORDER_MARKET, Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        if not client_oid:
            client_oid = flat_uuid()

        data = await self._get_common_order_data(
            symbol,
            type,
            side,
            size,
            price,
            funds,
            client_oid,
            stp,
            remark,
            time_in_force,
            cancel_after,
            post_only,
            hidden,
            iceberg,
            visible_size,
        )

        if is_isolated:
            data[
                "isIsolated"
            ] = is_isolated  # todo check this parameter for margin_create_order
        if auto_borrow:
            data["autoBorrow"] = auto_borrow
        if auto_repay:
            data["autoRepay"] = auto_repay

        return await self._post(
            "hf/margin/order/test",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def hf_margin_cancel_order(self, order_id, symbol, **params):
        """Cancel an hf margin order by the orderId

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/cancel-hf-order-by-orderid

        :param order_id: OrderId
        :type order_id: string
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            res = client.hf_margin_cancel_order('5bd6e9286d99522a52e458de', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {"symbol": symbol}

        return await self._delete(
            "hf/margin/orders/{}".format(order_id),
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def hf_margin_cancel_order_by_client_oid(self, client_oid, symbol, **params):
        """Cancel a hf margin order by the clientOid

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/cancel-hf-order-by-clientoid

        :param client_oid: ClientOid
        :type client_oid: string
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            res = client.hf_margin_cancel_order_by_client_oid('6d539dc614db3', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {"symbol": symbol}

        return await self._delete(
            "hf/margin/orders/client-order/{}".format(client_oid),
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def hf_margin_cancel_orders_by_symbol(self, symbol, trade_type, **params):
        """Cancel all hf margin orders by symbol

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/cancel-all-hf-orders-by-symbol

        :param symbol: Name of symbol e.g. ETH-USDT
        :type symbol: string
        :param trade_type: MARGIN_TRADE (Margin Trading) or MARGIN_ISOLATED_TRADE (Isolated Margin Trading)
        :type trade_type: string

        .. code:: python

            res = client.hf_margin_cancel_orders_by_symbol('ETH-USDT')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "tradeType": trade_type}

        return await self._delete(
            "hf/margin/orders",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def hf_margin_get_active_orders(self, symbol, trade_type, **params):
        """Get a list of active hf margin orders

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/get-active-hf-orders-list

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param trade_type: MARGIN_TRADE (Margin Trading) or MARGIN_ISOLATED_TRADE (Isolated Margin Trading)
        :type trade_type: string

        .. code:: python

            orders = client.hf_margin_get_active_orders('ETH-USDT')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "tradeType": trade_type}

        return await self._get(
            "hf/margin/orders/active",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def hf_margin_get_completed_orders(
        self,
        symbol,
        trade_type,
        side=None,
        type=None,
        start=None,
        end=None,
        last_id=None,
        limit=None,
        **params,
    ):
        """Get a list of completed hf margin orders

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/get-hf-filled-list

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param trade_type: MARGIN_TRADE (Margin Trading) or MARGIN_ISOLATED_TRADE (Isolated Margin Trading)
        :type trade_type: string
        :param side: (optional) buy or sell
        :type side: string
        :param type: (optional) limit, market, limit_stop or market_stop
        :type type: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param last_id: (optional) The last orderId of the last page
        :type last_id: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            orders = client.hf_margin_get_completed_orders('ETH-USDT', 'MARGIN_ISOLATED_TRADE')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "tradeType": trade_type}

        if side:
            data["side"] = side
        if type:
            data["type"] = type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if last_id:
            data["lastId"] = last_id
        if limit:
            data["limit"] = limit

        return await self._get(
            "hf/margin/orders/done",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def hf_margin_get_order(self, order_id, symbol, **params):
        """Get an hf margin order details by the orderId

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/get-hf-order-details-by-orderid

        :param order_id: OrderId
        :type order_id: string
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            order = client.hf_get_order('5bd6e9286d99522a52e458de', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "hf/margin/orders/{}".format(order_id),
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def hf_get_margin_order_by_client_oid(self, client_oid, symbol, **params):
        """Get hf margin order details by clientOid

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/get-hf-order-details-by-clientoid

        :param client_oid: clientOid value
        :type client_oid: str
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            order = client.hf_get_order_by_client_oid('6d539dc614db312', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "hf/margin/orders/client-order/{}".format(client_oid),
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def hf_margin_get_symbol_with_active_orders(self, trade_type, **params):
        """Get a list of symbols with active hf margin orders

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/get-active-hf-order-symbols

        :param trade_type: MARGIN_TRADE (Margin Trading) or MARGIN_ISOLATED_TRADE (Isolated Margin Trading)
        :type trade_type: string

        .. code:: python

            orders = client.hf_margin_get_symbol_with_active_orders('MARGIN_TRADE')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "symbolSize": 1,
                    "symbols": ["ADA-USDT"]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"tradeType": trade_type}

        return await self._get(
            "hf/margin/order/active/symbols",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    # Futures Orders

    async def _get_common_futures_order_data(
        self,
        symbol,
        type=None,
        side=None,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        value_qty=None,
        leverage=None,
        stop=None,
        stop_price_type=None,
        trigger_stop_up_price=None,
        stop_price=None,
        trigger_stop_down_price=None,
        reduce_only=None,
        force_hold=None,
        margin_mode=None,
        is_tpsl_order=None,
        **params,
    ):
        data = {"symbol": symbol}

        client_oid = client_oid or params.get("clientOid")
        if client_oid:
            data["clientOid"] = client_oid
        else:
            data["clientOid"] = flat_uuid()

        if type:
            data["type"] = type
        else:
            raise KucoinRequestException("type is required for futures orders")

        if side:
            data["side"] = side
        else:
            raise KucoinRequestException("side is required for futures orders")

        if leverage:
            data["leverage"] = leverage
        else:
            raise KucoinRequestException("leverage is required for futures orders")

        funds = funds or params.get("qty")
        value_qty = value_qty or params.get("valueQty")
        if size:
            if funds or value_qty:
                raise KucoinRequestException(
                    "size cannot be used with funds or value_qty"
                )
            data["size"] = size
        elif funds:
            if size or value_qty:
                raise KucoinRequestException(
                    "funds cannot be used with size or value_qty"
                )
            data["qty"] = funds
        elif value_qty:
            if size or funds:
                raise KucoinRequestException(
                    "value_qty cannot be used with size or funds"
                )
            data["valueQty"] = value_qty
        else:
            raise KucoinRequestException(
                "size, funds or value_qty is required for futures orders"
            )

        if type == self.ORDER_MARKET:
            if price:
                raise MarketOrderException(
                    "Cannot use price parameter with market order"
                )
            if time_in_force:
                raise MarketOrderException(
                    "Cannot use time_in_force parameter with market order"
                )
            if post_only:
                raise MarketOrderException(
                    "Cannot use post_only parameter with market order"
                )
            if hidden:
                raise MarketOrderException(
                    "Cannot use hidden parameter with market order"
                )
            if iceberg:
                raise MarketOrderException(
                    "Cannot use iceberg parameter with market order"
                )
            if visible_size:
                raise MarketOrderException(
                    "Cannot use visible_size parameter with market order"
                )
        elif type == self.ORDER_LIMIT:
            if not price:
                raise LimitOrderException("Price is required for limit order")
            if hidden and iceberg:
                raise LimitOrderException('Order can be either "hidden" or "iceberg"')
            if iceberg and not visible_size:
                raise LimitOrderException("Iceberg order requires visible_size")
            data["price"] = price
            if time_in_force:
                data["timeInForce"] = time_in_force
            if post_only:
                data["postOnly"] = post_only
            if hidden:
                data["hidden"] = hidden
            if iceberg:
                data["iceberg"] = iceberg
            if visible_size:
                data["visibleSize"] = visible_size

        if stp:
            data["stp"] = stp
        if remark:
            data["remark"] = remark
        if reduce_only:
            data["reduceOnly"] = reduce_only
        if force_hold:
            data["forceHold"] = force_hold
        if margin_mode:
            data["marginMode"] = margin_mode

        if is_tpsl_order:
            if trigger_stop_up_price:
                data["triggerStopUpPrice"] = trigger_stop_up_price
            if stop_price_type:
                data["stopPriceType"] = stop_price_type
            if trigger_stop_down_price:
                data["triggerStopDownPrice"] = trigger_stop_down_price
        else:
            if stop:
                if (not stop_price_type) or (not stop_price):
                    raise KucoinRequestException(
                        "stop_price_type and stop_price are required for stop orders"
                    )
                data["stop"] = stop
                data["stopPriceType"] = stop_price_type
                data["stopPrice"] = stop_price

        return dict(data, **params)

    async def futures_create_order(
        self,
        symbol,
        type=None,
        side=None,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        value_qty=None,
        leverage=None,
        stop=None,
        stop_price_type=None,
        stop_price=None,
        reduce_only=None,
        close_order=None,
        force_hold=None,
        margin_mode=None,
        **params,
    ):
        """Create a futures order

        https://www.kucoin.com/docs/rest/futures-trading/orders/place-order

        :param symbol: Name of symbol e.g. ETHUSDTM
        :type symbol: string
        :param type: (optional)order type - limit or market (default is limit)
            Is mandatory if close_order!=True
        :type type: string
        :param side: (optional) buy or sell
            Is mandatory if close_order!=True
        :type side: string
        :param size: (optional) Desired amount in base currency
            Is mandatory if funds and value_qty are not passed and close_order!=True
        :type size: string
        :param price: (optional) Price per base currency
            Is mandatory for limit order
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use
            Is mandatory if size and value_qty are not passed and close_order!=True
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO or CB (default is None). DC is not supported
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC or IOC - default is GTC
        :type time_in_force: string
        :param post_only: (optional) Post only flag (default is False)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (default is False)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (default is False)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order
        :type visible_size: string
        :param value_qty: (optional) Order size (Value), USDS-Swap correspond to USDT or USDC.
            The unit of the quantity of coin-swap is size(lot), which is not supported
            Is mandatory if size and funds are not passed and close_order!=True
        :type value_qty: string
        :param leverage: (optional) Leverage of the order
            is mandatory if close_order!=True
        :type leverage: string
        :param stop: (optional) down (triggers when the price reaches or goes below the stopPrice) or up (triggers when the price reaches or goes above the stopPrice).
            Requires stopPrice and stopPriceType to be defined
        :type stop: string
        :param stop_price_type: (optional) Either TP (trade price), IP (index price) or MP (mark price)
            Is mandatory if stop is defined
        :type stop_price_type: string
        :param stop_price: (optional) The trigger price of the order
            Is mandatory if stop is defined
        :type stop_price: string
        :param reduce_only: (optional) Reduce only flag (default is False)
        :type reduce_only: bool
        :param close_order: (optional) A flag to close the position. Set to false by default.
            If closeOrder is set to True, the system will close the position and the position size will become 0.
            Side, Size and Leverage fields can be left empty and the system will determine the side and size automatically.
        :type close_order: bool
        :param force_hold: (optional) A flag to forcely hold the funds for an order, even though it's an order to reduce the position size.
            This helps the order stay on the order book and not get canceled when the position size changes.
            Set to false by default. The system will forcely freeze certain amount of funds for this order, including orders whose direction is opposite to the current positions.
            This feature is to ensure that the order would not be canceled by the matching engine in such a circumstance that not enough funds are frozen for the order.
        :type force_hold: bool
        :param margin_mode: (optional) ISOLATED or CROSS (default is ISOLATED)
        :type margin_mode: string

        .. code:: python

            order = client.futures_create_order('ETHUSDTM', type=Client.ORDER_LIMIT, side=Client.SIDE_BUY, size=20, price=2000)
            order = client.futures_create_order('ETHUSDTM', type=Client.ORDER_MARKET, side=Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        if close_order:
            data = {
                "symbol": symbol,
            }
        else:
            data = await self._get_common_futures_order_data(
                symbol,
                type=type,
                side=side,
                size=size,
                price=price,
                funds=funds,
                client_oid=client_oid,
                stp=stp,
                remark=remark,
                time_in_force=time_in_force,
                post_only=post_only,
                hidden=hidden,
                iceberg=iceberg,
                visible_size=visible_size,
                value_qty=value_qty,
                leverage=leverage,
                stop=stop,
                stop_price_type=stop_price_type,
                stop_price=stop_price,
                reduce_only=reduce_only,
                force_hold=force_hold,
                margin_mode=margin_mode,
                is_tpsl_order=False,
                **params,
            )

        return await self._post("orders", True, is_futures=True, data=data)

    async def futures_create_test_order(
        self,
        symbol,
        type=None,
        side=None,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        value_qty=None,
        leverage=None,
        stop=None,
        stop_price_type=None,
        stop_price=None,
        reduce_only=None,
        close_order=None,
        force_hold=None,
        margin_mode=None,
        **params,
    ):
        """Create a futures test order

        https://www.kucoin.com/docs/rest/futures-trading/orders/place-order-test

        :param symbol: Name of symbol e.g. ETHUSDTM
        :type symbol: string
        :param type: (optional)order type - limit or market (default is limit)
            Is mandatory if close_order!=True
        :type type: string
        :param side: (optional) buy or sell
            Is mandatory if close_order!=True
        :type side: string
        :param size: (optional) Desired amount in base currency
            Is mandatory if funds and value_qty are not passed and close_order!=True
        :type size: string
        :param price: (optional) Price per base currency
            Is mandatory for limit order
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use
            Is mandatory if size and value_qty are not passed and close_order!=True
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO or CB (default is None). DC is not supported
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC or IOC - default is GTC
        :type time_in_force: string
        :param post_only: (optional) Post only flag (default is False)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (default is False)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (default is False)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order
        :type visible_size: string
        :param value_qty: (optional) Order size (Value), USDS-Swap correspond to USDT or USDC.
            The unit of the quantity of coin-swap is size(lot), which is not supported
            Is mandatory if size and funds are not passed and close_order!=True
        :type value_qty: string
        :param leverage: (optional) Leverage of the order
            is mandatory if close_order!=True
        :type leverage: string
        :param stop: (optional) down (triggers when the price reaches or goes below the stopPrice) or up (triggers when the price reaches or goes above the stopPrice).
            Requires stopPrice and stopPriceType to be defined
        :type stop: string
        :param stop_price_type: (optional) Either TP (trade price), IP (index price) or MP (mark price)
            Is mandatory if stop is defined
        :type stop_price_type: string
        :param stop_price: (optional) The trigger price of the order
            Is mandatory if stop is defined
        :type stop_price: string
        :param reduce_only: (optional) Reduce only flag (default is False)
        :type reduce_only: bool
        :param close_order: (optional) A flag to close the position. Set to false by default.
            If closeOrder is set to True, the system will close the position and the position size will become 0.
            Side, Size and Leverage fields can be left empty and the system will determine the side and size automatically.
        :type close_order: bool
        :param force_hold: (optional) A flag to forcely hold the funds for an order, even though it's an order to reduce the position size.
            This helps the order stay on the order book and not get canceled when the position size changes.
            Set to false by default. The system will forcely freeze certain amount of funds for this order, including orders whose direction is opposite to the current positions.
            This feature is to ensure that the order would not be canceled by the matching engine in such a circumstance that not enough funds are frozen for the order.
        :type force_hold: bool
        :param margin_mode: (optional) ISOLATED or CROSS (default is ISOLATED)
        :type margin_mode: string

        .. code:: python

            order = client.futures_create_test_order('ETHUSDTM', type=Client.ORDER_LIMIT, side=Client.SIDE_BUY, size=20, price=2000)
            order = client.futures_create_test_order('ETHUSDTM', type=Client.ORDER_MARKET, side=Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        if close_order:
            data = {
                "symbol": symbol,
            }
        else:
            data = await self._get_common_futures_order_data(
                symbol,
                type=type,
                side=side,
                size=size,
                price=price,
                funds=funds,
                client_oid=client_oid,
                stp=stp,
                remark=remark,
                time_in_force=time_in_force,
                post_only=post_only,
                hidden=hidden,
                iceberg=iceberg,
                visible_size=visible_size,
                value_qty=value_qty,
                leverage=leverage,
                stop=stop,
                stop_price_type=stop_price_type,
                stop_price=stop_price,
                reduce_only=reduce_only,
                force_hold=force_hold,
                margin_mode=margin_mode,
                is_tpsl_order=False,
                **params,
            )

        return await self._post("orders/test", True, is_futures=True, data=data)

    async def futures_create_stop_order(
        self,
        symbol,
        type=None,
        side=None,
        size=None,
        price=None,
        funds=None,
        client_oid=None,
        stp=None,
        remark=None,
        time_in_force=None,
        post_only=None,
        hidden=None,
        iceberg=None,
        visible_size=None,
        value_qty=None,
        leverage=None,
        trigger_stop_up_price=None,
        stop_price_type=None,
        trigger_stop_down_price=None,
        reduce_only=None,
        close_order=None,
        force_hold=None,
        margin_mode=None,
        **params,
    ):
        """Create a futures take profit and/or stop loss order

        https://www.kucoin.com/docs/rest/futures-trading/orders/place-take-profit-and-stop-loss-order

        :param symbol: Name of symbol e.g. ETHUSDTM
        :type symbol: string
        :param type: (optional)order type - limit or market (default is limit)
            Is mandatory if close_order!=True
        :type type: string
        :param side: (optional) buy or sell
            Is mandatory if close_order!=True
        :type side: string
        :param size: (optional) Desired amount in base currency
            Is mandatory if funds and value_qty are not passed and close_order!=True
        :type size: string
        :param price: (optional) Price per base currency
            Is mandatory for limit order
        :type price: string
        :param funds: (optional) Desired amount of quote currency to use
            Is mandatory if size and value_qty are not passed and close_order!=True
        :type funds: string
        :param client_oid: (optional) Unique order id (default flat_uuid())
        :type client_oid: string
        :param stp: (optional) self trade protection CN, CO or CB (default is None). DC is not supported
        :type stp: string
        :param remark: (optional) remark for the order, max 100 utf8 characters
        :type remark: string
        :param time_in_force: (optional) GTC or IOC - default is GTC
        :type time_in_force: string
        :param post_only: (optional) Post only flag (default is False)
        :type post_only: bool
        :param hidden: (optional) Hidden order flag (default is False)
        :type hidden: bool
        :param iceberg: (optional) Iceberg order flag (default is False)
        :type iceberg: bool
        :param visible_size: (optional) The maximum visible size of an iceberg order
        :type visible_size: string
        :param value_qty: (optional) Order size (Value), USDS-Swap correspond to USDT or USDC.
            The unit of the quantity of coin-swap is size(lot), which is not supported
            Is mandatory if size and funds are not passed and close_order!=True
        :type value_qty: string
        :param leverage: (optional) Leverage of the order
            is mandatory if close_order!=True
        :type leverage: string
        :param trigger_stop_up_price: (optional) The trigger price of the take profit order
        :type trigger_stop_up_price: string
        :param stop_price_type: (optional) Either TP (trade price), IP (index price) or MP (mark price)
        :type stop_price_type: string
        :param trigger_stop_down_price: (optional) The trigger price of the stop loss order
        :type trigger_stop_down_price: string
        :param reduce_only: (optional) Reduce only flag (default is False)
        :type reduce_only: bool
        :param close_order: (optional) A flag to close the position. Set to false by default.
            If closeOrder is set to True, the system will close the position and the position size will become 0.
            Side, Size and Leverage fields can be left empty and the system will determine the side and size automatically.
        :type close_order: bool
        :param force_hold: (optional) A flag to forcely hold the funds for an order, even though it's an order to reduce the position size.
            This helps the order stay on the order book and not get canceled when the position size changes.
            Set to false by default. The system will forcely freeze certain amount of funds for this order, including orders whose direction is opposite to the current positions.
            This feature is to ensure that the order would not be canceled by the matching engine in such a circumstance that not enough funds are frozen for the order.
        :type force_hold: bool
        :param margin_mode: (optional) ISOLATED or CROSS (default is ISOLATED)
        :type margin_mode: string

        .. code:: python

            order = client.futures_create_stop_order('ETHUSDTM', type=Client.ORDER_LIMIT, side=Client.SIDE_BUY, size=20, price=2000)
            order = client.futures_create_stop_order('ETHUSDTM', type=Client.ORDER_MARKET, side=Client.SIDE_BUY, funds=20)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        if close_order:
            data = {
                "symbol": symbol,
            }
        else:
            data = await self._get_common_futures_order_data(
                symbol,
                type=type,
                side=side,
                size=size,
                price=price,
                funds=funds,
                client_oid=client_oid,
                stp=stp,
                remark=remark,
                time_in_force=time_in_force,
                post_only=post_only,
                hidden=hidden,
                iceberg=iceberg,
                visible_size=visible_size,
                value_qty=value_qty,
                leverage=leverage,
                trigger_stop_up_price=trigger_stop_up_price,
                stop_price_type=stop_price_type,
                trigger_stop_down_price=trigger_stop_down_price,
                reduce_only=reduce_only,
                force_hold=force_hold,
                margin_mode=margin_mode,
                is_tpsl_order=True,
                **params,
            )

        return await self._post("st-orders", True, is_futures=True, data=data)

    async def futures_create_orders(self, orders_data):
        """Create multiple futures orders
        You can place up to 20 orders at one time, including limit orders, market orders, and stop orders

        https://www.kucoin.com/docs/rest/futures-trading/orders/place-multiple-orders

        :param orders_data: List of orders data
        :type orders_data: list
            Every order data is a dict with the same parameters as futures_create_order

        .. code:: python

            orders = [
                {
                    'symbol': 'ETHUSDTM',
                    'type': Client.ORDER_LIMIT,
                    'side': Client.SIDE_BUY,
                    'size': 20,
                    'price': 2000
                },
                {
                    'symbol': 'ETHUSDTM',
                    'type': Client.ORDER_MARKET,
                    'side': Client.SIDE_BUY,
                    'funds': 20
                }
            ]
            order = client.futures_create_orders(orders)

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException, MarketOrderException, LimitOrderException, KucoinRequestException

        """

        data = []
        for order in orders_data:
            if "close_order" in order and order["close_order"]:
                data.append({"symbol": order["symbol"], "closeOrder": True})
            else:
                order_data = await self._get_common_futures_order_data(**order)
                del order_data["clientOid"]
                data.append(order_data)

        return await self._post("orders/multi", True, is_futures=True, data=data)

    async def futures_cancel_order(self, order_id, **params):
        """Cancel a futures order by order id

        https://www.kucoin.com/docs/rest/futures-trading/orders/cancel-order-by-orderid

        :param order_id: Order id
        :type order_id: string

        .. code:: python

            res = client.futures_cancel_order('5bd6e9286d99522a52e458de')

        :returns: ApiResponse

        .. code:: python

            {
                "cancelledOrderIds": [
                    "5bd6e9286d99522a52e458de"
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        return await self._delete(
            "orders/{}".format(order_id), True, is_futures=True, data=params
        )

    async def futures_cancel_order_by_client_oid(self, client_oid, symbol, **params):
        """Cancel a futures order by the clientOid

        https://www.kucoin.com/docs/rest/futures-trading/orders/cancel-order-by-clientoid

        :param client_oid: ClientOid
        :type client_oid: string
        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            res = client.futures_cancel_order_by_client_oid('6d539dc614db3', 'KCS-BTC')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {"symbol": symbol}

        return await self._delete(
            "orders/client-order/{}".format(client_oid),
            True,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_cancel_orders(
        self, symbol=None, order_ids=None, client_oids=None, **params
    ):
        """Cancel multiple futures orders by order ids or clientOids
        Either order_ids or client_oids and symbol are mandatory

        https://www.kucoin.com/docs/rest/futures-trading/orders/batch-cancel-orders

        :param symbol: (optional) Name of symbol e.g. ETHUSDTM
            Is mandatory if order_ids are not passed
        :type symbol: string
        :param order_ids: (optional) List of order ids
            Is mandatory if client_oids is not passed
        :type order_ids: list
        :param client_oids: (optional) List of clientOids
            Is mandatory if order_ids are not passed
        :type client_oids: list

        .. code:: python

            res = client.futures_cancel_orders(['5bd6e9286d99522a52e458de', '5bd6e9286d99522a52e458df'])

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        KucoinAPIException If order_id is not found

        """

        data = {}
        if order_ids and client_oids:
            raise KucoinRequestException(
                "Either order_ids or client_oids should be passed, not both"
            )
        if not order_ids and not client_oids:
            raise KucoinRequestException(
                "Either order_ids or client_oids should be passed"
            )
        if order_ids:
            data["orderIdsList"] = order_ids
        elif not symbol:
            raise KucoinRequestException("symbol is required if client_oids are passed")
        else:
            data["clientOidsList"] = client_oids
            data["symbol"] = symbol

        return await self._delete(
            "orders/multi-cancel", True, is_futures=True, data=dict(data, **params)
        )

    async def futures_cancel_all_orders(self, symbol=None, **params):
        """Cancel all futures orders

        https://www.kucoin.com/docs/rest/futures-trading/orders/cancel-multiple-futures-limit-orders

        :param symbol: (optional) Name of symbol e.g. ETHUSDTM
        :type symbol: string

        .. code:: python

            res = client.futures_cancel_all_orders()

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """
        data = {}
        if symbol:
            data["symbol"] = symbol

        return await self._delete("orders", True, is_futures=True, data=dict(data, **params))

    async def futures_cancel_all_stop_orders(self, symbol=None, **params):
        """Cancel all futures stop orders

        https://www.kucoin.com/docs/rest/futures-trading/orders/cancel-multiple-futures-stop-orders

        :param symbol: (optional) Name of symbol e.g. ETHUSDTM
        :type symbol: string

        .. code:: python

            res = client.futures_cancel_all_stop_orders()

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """
        data = {}
        if symbol:
            data["symbol"] = symbol

        return await self._delete(
            "stopOrders", True, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_orders(
        self,
        symbol=None,
        status=None,
        side=None,
        order_type=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get list of futures orders

        https://www.kucoin.com/docs/rest/futures-trading/orders/get-order-list

        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param status: (optional) Specify status active or done (default done)
        :type status: string
        :param side: (optional) buy or sell
        :type side: string
        :param order_type: (optional) limit, market, limit_stop or market_stop
        :type order_type: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of orders (default 50, max 1000)
        :type limit: int

        .. code:: python

            orders = client.futures_get_orders(symbol='ETHUSDTM', status='active')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if symbol:
            data["symbol"] = symbol
        if status:
            data["status"] = status
        if side:
            data["side"] = side
        if order_type:
            data["type"] = order_type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get("orders", True, is_futures=True, data=dict(data, **params))

    async def futures_get_stop_orders(
        self,
        symbol=None,
        side=None,
        order_type=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get list of untriggered futures stop orders

        https://www.kucoin.com/docs/rest/futures-trading/orders/get-untriggered-stop-order-list

        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param side: (optional) buy or sell
        :type side: string
        :param order_type: (optional) limit, market, limit_stop or market_stop
        :type order_type: string
        :param start: (optional) Start time as unix timestamp
        :type start: string
        :param end: (optional) End time as unix timestamp
        :type end: string
        :param page: (optional) Page to fetch
        :type page: int
        :param limit: (optional) Number of orders (default 50, max 1000)
        :type limit: int

        .. code:: python

            orders = client.futures_get_stop_orders(symbol='ETHUSDTM')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if symbol:
            data["symbol"] = symbol
        if side:
            data["side"] = side
        if order_type:
            data["type"] = order_type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get("stopOrders", True, is_futures=True, data=dict(data, **params))

    async def futures_get_recent_orders(self, symbol=None, **params):
        """Get up to 1000 last futures done orders in the last 24 hours.

        https://www.kucoin.com/docs/rest/futures-trading/orders/get-list-of-orders-completed-in-24h

        :param symbol: (optional) Name of symbol e.g. ETHUSDTM
        :type symbol: string

        .. code:: python

            orders = client.futures_get_recent_orders()

        :returns: ApiResponse

        todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}
        if symbol:
            data["symbol"] = symbol

        return await self._get(
            "recentDoneOrders", True, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_order(self, order_id, **params):
        """Get futures order details by order id

        https://www.kucoin.com/docs/rest/futures-trading/orders/get-order-details-by-orderid-clientoid

        :param order_id: orderOid value
        :type order_id: str

        .. code:: python

            order = client.futures_get_order('5c35c02703aa673ceec2a168')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get(
            "orders/{}".format(order_id), True, is_futures=True, data=params
        )

    async def futures_get_order_by_client_oid(self, client_oid, **params):
        """Get futures order details by clientOid

        https://www.kucoin.com/docs/rest/futures-trading/orders/get-order-details-by-orderid-clientoid

        :param client_oid: clientOid value
        :type client_oid: string

        .. code:: python

            order = client.futures_get_order_by_client_oid('6d539dc614db312')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"clientOid": client_oid}

        return await self._get("orders/byClientOid", True, is_futures=True, data=params)

    # Fill Endpoints

    async def get_fills(
        self,
        trade_type,
        order_id=None,
        symbol=None,
        side=None,
        type=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get a list of recent fills.

        https://www.kucoin.com/docs/rest/spot-trading/fills/get-filled-list

        :param trade_type: TRADE (Spot Trading), MARGIN_TRADE (Margin Trading), MARGIN_ISOLATED_TRADE (Isolated Margin Trading), TRADE as default.
        :type trade_type: string
        :param order_id: (optional) OrderId
        :type order_id: string
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param side: (optional) buy or sell
        :type side: string
        :param type: (optional) limit, market, limit_stop or market_stop
        :type type: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param page: (optional) Page number
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            fills = client.get_fills('TRADE')

        :returns: ApiResponse

        .. code:: python

            {
                "currentPage": 1,
                "pageSize": 1,
                "totalNum": 251915,
                "totalPage": 251915,
                "items": [
                    {
                    "symbol": "BTC-USDT",
                    "tradeId": "5c35c02709e4f67d5266954e",
                    "orderId": "5c35c02703aa673ceec2a168",
                    "counterOrderId": "5c1ab46003aa676e487fa8e3",
                    "side": "buy",
                    "liquidity": "taker",
                    "forceTaker": true,
                    "price": "0.083",
                    "size": "0.8424304",
                    "funds": "0.0699217232",
                    "fee": "0",
                    "feeRate": "0",
                    "feeCurrency": "USDT",
                    "stop": "",
                    "type": "limit",
                    "createdAt": 1547026472000,
                    "tradeType": "TRADE"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"tradeType": trade_type}

        if order_id:
            data["orderId"] = order_id
        if symbol:
            data["symbol"] = symbol
        if side:
            data["side"] = side
        if type:
            data["type"] = type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get("fills", False, data=dict(data, **params))

    async def get_recent_fills(self, **params):
        """Get a list of recent fills.

        https://www.kucoin.com/docs/rest/spot-trading/fills/get-recent-filled-list

        .. code:: python

            fills = client.get_recent_fills()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": [
                    {
                        "counterOrderId": "5db7ee769797cf0008e3beea",
                        "createdAt": 1572335233000,
                        "fee": "0.946357371456",
                        "feeCurrency": "USDT",
                        "feeRate": "0.001",
                        "forceTaker": true,
                        "funds": "946.357371456",
                        "liquidity": "taker",
                        "orderId": "5db7ee805d53620008dce1ba",
                        "price": "9466.8",
                        "side": "buy",
                        "size": "0.09996592",
                        "stop": "",
                        "symbol": "BTC-USDT",
                        "tradeId": "5db7ee8054c05c0008069e21",
                        "tradeType": "MARGIN_TRADE",
                        "type": "market"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("limit/fills", True, data=params)

    async def hf_get_fills(
        self,
        symbol,
        order_id=None,
        side=None,
        type=None,
        start=None,
        end=None,
        last_id=None,
        limit=None,
        **params,
    ):
        """Get a list of hf fills

        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-hf-filled-list

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_id: (optional) OrderId
        :type order_id: string
        :param side: (optional) buy or sell
        :type side: string
        :param type: (optional) limit, market, limit_stop or market_stop
        :type type: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param last_id: (optional) The last orderId of the last page
        :type last_id: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            fills = client.hf_get_fills('ETH-USDT')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "items": [
                    {
                        "id": 2678765568,
                        "symbol": "BTC-ETC",
                        "tradeId": 616179312641,
                        "orderId": "6306cf6e27ecbe0001e1e03a",
                        "counterOrderId": "6306cf4027ecbe0001e1df4d",
                        "side": "buy",
                        "liquidity": "taker",
                        "forceTaker": false,
                        "price": "1",
                        "size": "1",
                        "funds": "1",
                        "fee": "0.00021",
                        "feeRate": "0.00021",
                        "feeCurrency": "USDT",
                        "stop": "",
                        "tradeType": "TRADE",
                        "type": "limit",
                        "createdAt": 1661390702919
                    }
                    ],
                    "lastId": 2678765568
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        if order_id:
            data["orderId"] = order_id
        if side:
            data["side"] = side
        if type:
            data["type"] = type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if last_id:
            data["lastId"] = last_id
        if limit:
            data["limit"] = limit

        return await self._get("hf/fills", True, data=dict(data, **params))

    async def hf_margin_get_fills(
        self,
        symbol,
        trade_type,
        order_id=None,
        side=None,
        type=None,
        start=None,
        end=None,
        last_id=None,
        limit=None,
        **params,
    ):
        """Get a list of hf fills

        https://www.kucoin.com/docs/rest/margin-trading/margin-hf-trade/get-hf-transaction-records

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param trade_type: MARGIN_TRADE (Margin Trading) or MARGIN_ISOLATED_TRADE (Isolated Margin Trading)
        :type trade_type: string
        :param order_id: (optional) OrderId
        :type order_id: string
        :param side: (optional) buy or sell
        :type side: string
        :param type: (optional) limit, market, limit_stop or market_stop
        :type type: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param last_id: (optional) The last orderId of the last page
        :type last_id: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            fills = client.hf_get_fills('ETH-USDT')

        :returns: ApiResponse

        .. code:: python

            todo add the response example

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "tradeType": trade_type}

        if order_id:
            data["orderId"] = order_id
        if side:
            data["side"] = side
        if type:
            data["type"] = type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if last_id:
            data["lastId"] = last_id
        if limit:
            data["limit"] = limit

        return await self._get(
            "hf/margin/fills",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def futures_get_fills(
        self,
        order_id=None,
        symbol=None,
        side=None,
        type=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get a list of recent futures fills.

        https://www.kucoin.com/docs/rest/futures-trading/fills/get-filled-list

        :param order_id: (optional) OrderId
        :type order_id: string
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param side: (optional) buy or sell
        :type side: string
        :param type: (optional) limit, market, limit_stop or market_stop
        :type type: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param page: (optional) Page number
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            fills = client.futures_get_fills()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "currentPage": 1,
                    "pageSize": 1,
                    "totalNum": 251915,
                    "totalPage": 251915,
                    "items": [
                        {
                            "symbol": "XBTUSDM",
                            "tradeId": "5ce24c1f0c19fc3c58edc47c",
                            "orderId": "5ce24c16b210233c36ee321d",
                            "side": "sell",
                            "liquidity": "taker",
                            "forceTaker": true,
                            "price": "8302",
                            "size": 10,
                            "value": "0.001204529",
                            "feeRate": "0.0005",
                            "fixFee": "0.00000006",
                            "feeCurrency": "XBT",
                            "stop": "",
                            "fee": "0.0000012022",
                            "orderType": "limit",
                            "tradeType": "trade",
                            "createdAt": 1558334496000,
                            "settleCurrency": "XBT",
                            "openFeePay": "0.002",
                            "closeFeePay": "0.002",
                            "tradeTime": 1558334496000000000,
                            "marginMode": "ISOLATED"
                        }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if order_id:
            data["orderId"] = order_id
        if symbol:
            data["symbol"] = symbol
        if side:
            data["side"] = side
        if type:
            data["type"] = type
        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get("fills", False, is_futures=True, data=dict(data, **params))

    async def futures_get_recent_fills(self, symbol=None, **params):
        """Get a list of recent futures fills.

        https://www.kucoin.com/docs/rest/futures-trading/fills/get-recent-filled-list

        .. code:: python

            fills = client.futures_get_recent_fills()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": [
                    {
                        "symbol": "XBTUSDM",
                        "tradeId": "5ce24c1f0c19fc3c58edc47c",
                        "orderId": "5ce24c16b210233c36ee321d",
                        "side": "sell",
                        "liquidity": "taker",
                        "forceTaker": true,
                        "price": "8302",
                        "size": 10,
                        "value": "0.001204529",
                        "feeRate": "0.0005",
                        "fixFee": "0.00000006",
                        "feeCurrency": "XBT",
                        "stop": "",
                        "fee": "0.0000012022",
                        "orderType": "limit",
                        "tradeType": "trade",
                        "createdAt": 1558334496000,
                        "settleCurrency": "XBT",
                        "openFeePay": "0.002",
                        "closeFeePay": "0.002",
                        "tradeTime": 1558334496000000000,
                        "marginMode": "ISOLATED"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if symbol:
            data["symbol"] = symbol

        return await self._get(
            "recentFills", False, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_active_order_value(self, symbol, **params):
        """Get the active order value of a symbol

        https://www.kucoin.com/docs/rest/futures-trading/fills/get-active-order-value-calculation

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string

        .. code:: python

            active_order_value = client.futures_get_active_order_value('XBTUSDM')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "openOrderBuySize": 20,
                    "openOrderSellSize": 0,
                    "openOrderBuyCost": "0.0025252525",
                    "openOrderSellCost": "0",
                    "settleCurrency": "XBT"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "openOrderStatistics", False, is_futures=True, data=dict(data, **params)
        )

    # Margin Info Endpoints

    async def margin_get_leverage_token_info(self, currency=None, **params):
        """Get a list of leverage token info

        https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-leveraged-token-info

        :param currency: (optional) Currency, if empty query all currencies
        :type currency: string

        .. code:: python

            leverage_token_info = client.get_leverage_token_info()

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": [
                    {
                        "currency": "BTCUP",
                        "netAsset": 0.001,
                        "targetLeverage": "2-4",
                        "actualLeverage": "2.33",
                        "assetsUnderManagement": "766834.764756714775 USDT"
                        "basket": "-78.671762 XBTUSDTM"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if currency:
            data["currency"] = currency

        return await self._get(
            "etf/info", True, api_version=self.API_VERSION3, data=dict(data, **params)
        )

    async def margin_get_all_trading_pairs_mark_prices(self, **params):
        """Get a list of trading pairs and their mark prices

        https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-all-trading-pairs-mark-price

        .. code:: python

            trading_pairs_mark_prices = client.get_all_trading_pairs_mark_prices()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": [
                    {
                        "symbol": "POND-BTC",
                        "timePoint": 1721027167000,
                        "value": 2.96603125E-7
                    },
                    {
                        "symbol": "REN-BTC",
                        "timePoint": 1721027217000,
                        "value": 7.36068750E-7
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get(
            "mark-price/all-symbols", False, api_version=self.API_VERSION3, data=params
        )

    async def margin_get_mark_price(self, symbol, **params):
        """Get the mark price of a symbol

        https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-mark-price

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            mark_price = client.get_mark_price('ETH-USDT')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "symbol": "USDT-BTC",
                    "timePoint": 1659930234000,
                    "value": 0.0000429
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "mark-price/{}/current".format(symbol), False, data=dict(data, **params)
        )

    async def margin_get_config(self, **params):
        """Get the margin configuration

        https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-margin-configuration-info

        .. code:: python

            margin_config = client.get_config()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "currencyList": [
                        "XEM",
                        "MATIC",
                        "VRA",
                        ...
                    ],
                    "maxLeverage": 5,
                    "warningDebtRatio": "0.95",
                    "liqDebtRatio": "0.97"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("margin/config", True, data=params)

    async def margin_get_cross_isolated_risk_limit_config(
        self, isolated, symbol=None, currency=None, **params
    ):
        """Get the cross or isolated margin risk limit configuration

        https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-cross-isolated-margin-risk-limit-currency-config

        :param isolated: True for isolated margin, False for cross margin
        :type isolated: bool
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param currency: (optional) Currency
        :type currency: string

        .. code:: python

            risk_limit_config = client.get_cross_isolated_risk_limit_config(False)

        :returns: ApiResponse

        .. code:: python

            CROSS MARGIN RESPONSES
            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": [
                    {
                        "timestamp": 1697783812257,
                        "currency": "XMR",
                        "borrowMaxAmount": "999999999999999999",
                        "buyMaxAmount": "999999999999999999",
                        "holdMaxAmount": "999999999999999999",
                        "borrowCoefficient": "0.5",
                        "marginCoefficient": "1",
                        "precision": 8,
                        "borrowMinAmount": "0.001",
                        "borrowMinUnit": "0.001",
                        "borrowEnabled": true
                    }
                ]
            }
            ISOLATED MARGIN RESPONSES

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": [
                    {
                        "timestamp": 1697782543851,
                        "symbol": "LUNC-USDT",
                        "baseMaxBorrowAmount": "999999999999999999",
                        "quoteMaxBorrowAmount": "999999999999999999",
                        "baseMaxBuyAmount": "999999999999999999",
                        "quoteMaxBuyAmount": "999999999999999999",
                        "baseMaxHoldAmount": "999999999999999999",
                        "quoteMaxHoldAmount": "999999999999999999",
                        "basePrecision": 8,
                        "quotePrecision": 8,
                        "baseBorrowCoefficient": "1",
                        "quoteBorrowCoefficient": "1",
                        "baseMarginCoefficient": "1",
                        "quoteMarginCoefficient": "1",
                        "baseBorrowMinAmount": null,
                        "baseBorrowMinUnit": null,
                        "quoteBorrowMinAmount": "0.001",
                        "quoteBorrowMinUnit": "0.001",
                        "baseBorrowEnabled": false,
                        "quoteBorrowEnabled": true
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"isolated": isolated}

        if symbol:
            data["symbol"] = symbol
        if currency:
            data["currency"] = currency

        return await self._get(
            "margin/currencies",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_get_isolated_synbols_config(self, **params):
        """Get the isolated margin symbol configuration

        https://www.kucoin.com/docs/rest/margin-trading/isolated-margin/get-isolated-margin-symbols-configuration

        .. code:: python

            isolated_symbols_config = client.get_isolated_synbols_config()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": [
                    {
                        "symbol": "EOS-USDC",
                        "symbolName": "EOS-USDC",
                        "baseCurrency": "EOS",
                        "quoteCurrency": "USDC",
                        "maxLeverage": 10,
                        "flDebtRatio": "0.97",
                        "tradeEnable": true,
                        "autoRenewMaxDebtRatio": "0.96",
                        "baseBorrowEnable": true,
                        "quoteBorrowEnable": true,
                        "baseTransferInEnable": true,
                        "quoteTransferInEnable": true
                    },
                    {
                        "symbol": "MANA-USDT",
                        "symbolName": "MANA-USDT",
                        "baseCurrency": "MANA",
                        "quoteCurrency": "USDT",
                        "maxLeverage": 10,
                        "flDebtRatio": "0.9",
                        "tradeEnable": true,
                        "autoRenewMaxDebtRatio": "0.96",
                        "baseBorrowEnable": true,
                        "quoteBorrowEnable": true,
                        "baseTransferInEnable": true,
                        "quoteTransferInEnable": true
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("isolated/symbols", True, data=params)

    async def margin_get_isolated_account_info(self, balance_currency=None, **params):
        """Get the isolated margin account info

        https://www.kucoin.com/docs/rest/margin-trading/isolated-margin/get-isolated-margin-account-info

        :param balance_currency: (optional) The pricing coin, currently only supports USDT, KCS, and BTC. Defaults to BTC if no value is passed.
        :type balance_currency: string

        .. code:: python

            isolated_account_info = client.get_isolated_account_info()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "totalConversionBalance": "3.4939947",
                    "liabilityConversionBalance": "0.00239066",
                    "assets": [
                        {
                            "symbol": "MANA-USDT",
                            "status": "CLEAR",
                            "debtRatio": "0",
                            "baseAsset": {
                            "currency": "MANA",
                            "totalBalance": "0",
                            "holdBalance": "0",
                            "availableBalance": "0",
                            "liability": "0",
                            "interest": "0",
                            "borrowableAmount": "0"
                        },
                            "quoteAsset": {
                                "currency": "USDT",
                                "totalBalance": "0",
                                "holdBalance": "0",
                                "availableBalance": "0",
                                "liability": "0",
                                "interest": "0",
                                "borrowableAmount": "0"
                            }
                        },
                        {
                            "symbol": "EOS-USDC",
                            "status": "CLEAR",
                            "debtRatio": "0",
                            "baseAsset": {
                                "currency": "EOS",
                                "totalBalance": "0",
                                "holdBalance": "0",
                                "availableBalance": "0",
                                "liability": "0",
                                "interest": "0",
                                "borrowableAmount": "0"
                            },
                            "quoteAsset": {
                                "currency": "USDC",
                                "totalBalance": "0",
                                "holdBalance": "0",
                                "availableBalance": "0",
                                "liability": "0",
                                "interest": "0",
                                "borrowableAmount": "0"
                            }
                        }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if balance_currency:
            data["balanceCurrency"] = balance_currency

        return await self._get("isolated/accounts", True, data=dict(data, **params))

    async def margin_get_single_isolated_account_info(self, symbol, **params):
        """Get the isolated margin account info for a single symbol

        https://www.kucoin.com/docs/rest/margin-trading/isolated-margin/get-single-isolated-margin-account-info

        :param symbol: Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            isolated_account_info = client.get_single_isolated_account_info('EOS-USDC')

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "symbol": "MANA-USDT",
                    "status": "CLEAR",
                    "debtRatio": "0",
                    "baseAsset": {
                        "currency": "MANA",
                        "totalBalance": "0",
                        "holdBalance": "0",
                        "availableBalance": "0",
                        "liability": "0",
                        "interest": "0",
                        "borrowableAmount": "0"
                    },
                    "quoteAsset": {
                        "currency": "USDT",
                        "totalBalance": "0",
                        "holdBalance": "0",
                        "availableBalance": "0",
                        "liability": "0",
                        "interest": "0",
                        "borrowableAmount": "0"
                    }
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "isolated/account/{}".format(symbol), True, data=dict(data, **params)
        )

    async def margin_borrow(
        self,
        currency,
        size,
        time_in_force,
        isolated=False,
        symbol=None,
        is_hf=False,
        **params,
    ):
        """Borrow funds for margin trading

        https://www.kucoin.com/docs/rest/margin-trading/margin-trading-v3-/margin-borrowing

        :param currency: Currency
        :type currency: string
        :param size: Amount to borrow
        :type size: string
        :param time_in_force: GTC (Good till cancelled) or GTT (Good till time)
        :type time_in_force: string
        :param isolated: (optional) True for isolated margin, False for cross margin
        :type isolated: bool
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param is_hf: (optional) true: high frequency borrowing, false: low frequency borrowing; default false
        :type is_hf: bool

        .. code:: python

            borrow = client.margin_borrow('USDT', '100', 'GTC')

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": {
                    "orderNo": "5da6dba0f943c0c81f5d5db5",
                    "actualSize": 10
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency, "size": size, "timeInForce": time_in_force}

        if isolated:
            data["isolated"] = isolated
        if symbol:
            data["symbol"] = symbol
        if is_hf:
            data["isHf"] = is_hf

        return await self._post(
            "margin/borrow",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_repay(
        self, currency, size, isolated=False, symbol=None, is_hf=False, **params
    ):
        """Repay borrowed funds for margin trading

        https://www.kucoin.com/docs/rest/margin-trading/margin-trading-v3-/repayment

        :param currency: Currency
        :type currency: string
        :param size: Amount to repay
        :type size: string
        :param isolated: (optional) True for isolated margin, False for cross margin
        :type isolated: bool
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param is_hf: (optional) true: high frequency borrowing, false: low frequency borrowing; default false
        :type is_hf: bool

        .. code:: python

            repay = client.margin_repay('USDT', '100')

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": {
                    "orderNo": "5da6dba0f943c0c81f5d5db5",
                    "actualSize": 10
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency, "size": size}

        if isolated:
            data["isolated"] = isolated
        if symbol:
            data["symbol"] = symbol
        if is_hf:
            data["isHf"] = is_hf

        return await self._post(
            "margin/repay",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_get_borrow_history(
        self,
        currency,
        isolated=False,
        symbol=None,
        order_no=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get the borrow history for margin trading

        https://www.kucoin.com/docs/rest/margin-trading/margin-trading-v3-/get-margin-borrowing-history

        :param currency: Currency
        :type currency: string
        :param isolated: (optional) True for isolated margin, False for cross margin
        :type isolated: bool
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_no: (optional) OrderNo
        :type order_no: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param page: (optional) Page number
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

                borrow_history = client.margin_get_borrow_history('USDT')

        :returns: ApiResponse

        .. code:: python

            {
                "currentPage": 1,
                "pageSize": 50,
                "totalNum": 1,
                "totalPage": 1,
                "items": [
                    {
                        "orderNo": "5da6dba0f943c0c81f5d5db5",
                        "symbol": "BTC-USDT",
                        "currency": "USDT",
                        "size": 10,
                        "actualSize": 10,
                        "status": "DONE",
                        "createdTime": 1555056425000
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency}

        if isolated:
            data["isolated"] = isolated
        if symbol:
            data["symbol"] = symbol
        if order_no:
            data["orderNo"] = order_no
        if start:
            data["startTime"] = start
        if end:
            data["endTime"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get(
            "margin/borrow",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_get_repay_history(
        self,
        currency,
        isolated=False,
        symbol=None,
        order_no=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get the repay history for margin trading

        https://www.kucoin.com/docs/rest/margin-trading/margin-trading-v3-/get-repayment-history

        :param currency: Currency
        :type currency: string
        :param isolated: (optional) True for isolated margin, False for cross margin
        :type isolated: bool
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param order_no: (optional) OrderNo
        :type order_no: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param page: (optional) Page number
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

                repay_history = client.margin_get_repay_history('USDT')

        :returns: ApiResponse

        .. code:: python

            {
                "currentPage": 1,
                "pageSize": 50,
                "totalNum": 1,
                "totalPage": 1,
                "items": {
                    "orderNo": "5da6dba0f943c0c81f5d5db5",
                    "symbol": "BTC-USDT",
                    "currency": "USDT",
                    "size": 10,
                    "actualSize": 10,
                    "status": "DONE",
                    "createdTime": 1555056425000
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency}

        if isolated:
            data["isolated"] = isolated
        if symbol:
            data["symbol"] = symbol
        if order_no:
            data["orderNo"] = order_no
        if start:
            data["startTime"] = start
        if end:
            data["endTime"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get(
            "margin/repay",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_get_cross_isolated_interest_records(
        self,
        isolated=False,
        symbol=None,
        currency=None,
        start=None,
        end=None,
        page=None,
        limit=None,
        **params,
    ):
        """Get the cross or isolated margin interest records

        https://www.kucoin.com/docs/rest/margin-trading/margin-trading-v3-/get-cross-isolated-margin-interest-records

        :param isolated: (optional) True for isolated margin, False for cross margin
        :type isolated: bool
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param currency: (optional) Currency
        :type currency: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param page: (optional) Page number
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            interest_records = client.margin_get_cross_isolated_interest_records()

        :returns: ApiResponse

        .. code:: python

            {
                "currentPage": 1,
                "pageSize": 50,
                "totalNum": 1,
                "totalPage": 1,
                "items": [
                    {
                        "createdAt": 1697783812257,
                        "currency": "XMR",
                        "interestAmount": "0.1",
                        "dayRatio": "0.001"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if isolated:
            data["isolated"] = isolated
        if symbol:
            data["symbol"] = symbol
        if currency:
            data["currency"] = currency
        if start:
            data["startTime"] = start
        if end:
            data["endTime"] = end
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get(
            "margin/interest",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_get_cross_trading_pairs_config(self, symbol=None, **params):
        """Get the cross margin trading pairs configuration

        https://www.kucoin.com/docs/rest/margin-trading/margin-trading-v3-/get-cross-margin-trading-pairs-configuration

        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string

        .. code:: python

            trading_pairs_config = client.margin_get_cross_trading_pairs_config()

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "timestamp": 1718779915377,
                    "items": [{
                        "symbol": "ATOM-USDT",
                        "name": "ATOM-USDT",
                        "enableTrading": true,
                        "market": "USDS",
                        "baseCurrency": "ATOM",
                        "quoteCurrency": "USDT",
                        "baseIncrement": 0.0001,
                        "baseMinSize": 0.1,
                        "quoteIncrement": 0.0001,
                        "quoteMinSize": 0.1,
                        "baseMaxSize": 10000000000,
                        "quoteMaxSize": 99999999,
                        "priceIncrement": 0.0001,
                        "feeCurrency": "USDT",
                        "priceLimitRate": 0.1,
                        "minFunds": 0.1
                    }]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if symbol:
            data["symbol"] = symbol

        return await self._get(
            "margin/symbols",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_modify_leverage_multiplier(
        self, leverage, symbol=None, isolated=False, **params
    ):
        """Modify the leverage multiplier

        https://www.kucoin.com/docs/rest/margin-trading/margin-trading-v3-/modify-leverage-multiplier

        :param leverage: Must be greater than 1 and up to two decimal places,
                        and cannot be less than the user's current debt leverage or greater than the system's maximum leverage
        :type leverage: int
        :param symbol: (optional) Name of symbol e.g. KCS-BTC
        :type symbol: string
        :param isolated: (optional) True for isolated margin, False for cross margin
        :type isolated: bool

        .. code:: python

            leverage_multiplier = client.margin_modify_leverage_multiplier(5)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": None
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"leverage": leverage}

        if symbol:
            data["symbol"] = symbol
        if isolated:
            data["isolated"] = isolated

        return await self._post(
            "position/update-user-leverage",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    # Lending Market Endpoints

    async def margin_lending_get_currency_info(self, currency=None, **params):
        """Get the lending currency info

        https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-currency-information

        :param currency: (optional) Currency
        :type currency: string

        .. code:: python

            currency_info = client.lending_get_currency_info()

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": [
                    {
                        "currency": "BTC",
                        "purchaseEnable": true,
                        "redeemEnable": true,
                        "increment": "1",
                        "minPurchaseSize": "10",
                        "minInterestRate": "0.004",
                        "maxInterestRate": "0.02",
                        "interestIncrement": "0.0001",
                        "maxPurchaseSize": "20000",
                        "marketInterestRate": "0.009",
                        "autoPurchaseEnable": true
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if currency:
            data["currency"] = currency

        return await self._get(
            "project/list",
            False,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_lending_get_interest_rate(self, currency, **params):
        """Get the interest rate for a currency

        https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-interest-rates

        :param currency: Currency
        :type currency: string

        .. code:: python

            interest_rate = client.lending_get_interest_rate('BTC')

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": [
                    {
                        "time": "202303261200",
                        "marketInterestRate": "0.003"
                    },
                    {
                        "time": "202303261300",
                        "marketInterestRate": "0.004"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency}

        return await self._get(
            "project/marketInterestRatet",
            False,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_lending_subscribtion(self, currency, size, interest_rate, **params):
        """Subscribe to a lending product

        https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/subscription

        :param currency: Currency
        :type currency: string
        :param size: Amount to subscribe
        :type size: string
        :param interest_rate: Interest rate
        :type interest_rate: string

        .. code:: python

            subscription = client.lending_subscribtion('BTC', '10', '0.004')

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": {
                    "orderNo": "5da6dba0f943c0c81f5d5db5"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency, "size": size, "interestRate": interest_rate}

        return await self._post(
            "purchase", True, api_version=self.API_VERSION3, data=dict(data, **params)
        )

    async def margin_lending_redemption(self, currency, size, purchase_order_no, **params):
        """Redeem a lending product

        https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/redemption

        :param currency: Currency
        :type currency: string
        :param size: Amount to redeem
        :type size: string
        :param purchase_order_no: OrderNo
        :type purchase_order_no: string

        .. code:: python

            redemption = client.lending_redemption('BTC', '10', '5da6dba0f943c0c81f5d5db5')

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": {
                    "orderNo": "5da6dba0f943c0c81f5d5db5"
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {
            "currency": currency,
            "size": size,
            "purchaseOrderNo": purchase_order_no,
        }

        return await self._post(
            "redeem", True, api_version=self.API_VERSION3, data=dict(data, **params)
        )

    async def margin_lending_modify_subscription_orders(
        self, currency, purchase_order_no, interest_rate, **params
    ):
        """Modify subscription orders

        https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/modify-subscription-orders

        :param currency: Currency
        :type currency: string
        :param purchase_order_no: OrderNo
        :type purchase_order_no: string
        :param interest_rate: Interest rate
        :type interest_rate: string

        .. code:: python

            modify_subscription = client.lending_modify_subscription_orders('BTC', '5da6dba0f943c0c81f5d5db5', '0.004')

        :returns: ApiResponse

        .. code:: python

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {
            "currency": currency,
            "purchaseOrderNo": purchase_order_no,
            "interestRate": interest_rate,
        }

        return await self._post(
            "lend/purchase/update",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_lending_get_redemtion_orders(
        self, currency, status, redeem_order_no=None, page=None, limit=None, **params
    ):
        """Get redemption orders

        https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-redemption-orders

        :param currency: Currency
        :type currency: string
        :param status: Status
        :type status: string
        :param redeem_order_no: (optional) OrderNo
        :type redeem_order_no: string
        :param page: (optional) Page number
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            redemption_orders = client.lending_get_redemtion_orders('BTC', 'DONE')

        :returns: ApiResponse

        .. code:: python

            {
                "currentPage": 1,
                "pageSize": 100,
                "totalNum": 1,
                "totalPage": 1,
                "items": [
                    {
                        "currency": "BTC",
                        "purchaseOrderNo": "5da6dba0f943c0c81f5d5db5",
                        "redeemOrderNo": "5da6dbasdffga1f5d5dfsb5",
                        "redeemAmount": "300000",
                        "receiptAmount": "250000",
                        "applyTime": 1669508513820,
                        "status": "PENDING"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency, "status": status}

        if redeem_order_no:
            data["orderNo"] = redeem_order_no
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get(
            "redeem/orders",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    async def margin_lending_get_subscription_orders(
        self, currency, status, purchase_order_no=None, page=None, limit=None, **params
    ):
        """Get subscription orders

        https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-subscription-orders

        :param currency: Currency
        :type currency: string
        :param status: Status
        :type status: string
        :param purchase_order_no: (optional) OrderNo
        :type purchase_order_no: string
        :param page: (optional) Page number
        :type page: int
        :param limit: (optional) Number of orders
        :type limit: int

        .. code:: python

            subscription_orders = client.lending_get_subscription_orders('BTC', 'DONE')

        :returns: ApiResponse

        .. code:: python

            {
                "currentPage": 1,
                "pageSize": 100,
                "totalNum": 1,
                "totalPage": 1,
                "items": [
                    {
                        "currency": "BTC",
                        "purchaseOrderNo": "5da6dba0f943c0c81f5d5db5",
                        "purchaseAmount": "300000",
                        "lendAmount": "0",
                        "redeemAmount": "300000",
                        "interestRate": "0.0003",
                        "incomeAmount": "200",
                        "applyTime": 1669508513820,
                        "status": "DONE"
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"currency": currency, "status": status}

        if purchase_order_no:
            data["orderNo"] = purchase_order_no
        if page:
            data["currentPage"] = page
        if limit:
            data["pageSize"] = limit

        return await self._get(
            "purchase/orders",
            True,
            api_version=self.API_VERSION3,
            data=dict(data, **params),
        )

    # Futures Position Endpoints

    async def futures_get_max_open_position_size(self, symbol, price, leverage, **params):
        """Get the maximum open position size for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/get-maximum-open-position-size

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param price: Price
        :type price: int
        :param leverage: Leverage
        :type leverage: int

        .. code:: python

            max_open_position_size = client.futures_get_max_open_position_size('XBTUSDM', 10000, 10)

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "price": price, "leverage": leverage}

        return await self._get(
            "getMaxOpenSize",
            True,
            api_version=self.API_VERSION2,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_get_position(self, symbol, **params):
        """Get the position for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/get-position-details

        :param symbol: Name of symbol e.g. XBTUSDM

        .. code:: python

            position = client.get_position('XBTUSDM')

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get("position", True, is_futures=True, data=dict(data, **params))

    async def futures_get_positions(self, currency=None, **params):
        """Get the positions

        https://www.kucoin.com/docs/rest/futures-trading/positions/get-position-list

        :param currency: (optional) Currency
        :type currency: string

        .. code:: python

            positions = client.get_positions()

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if currency:
            data["currency"] = currency

        return await self._get("positions", True, is_futures=True, data=dict(data, **params))

    async def futures_get_positions_history(
        self, symbol=None, start=None, end=None, page=None, limit=None, **params
    ):
        """Get the positions history

        https://www.kucoin.com/docs/rest/futures-trading/positions/get-positions-history

        :param symbol: (optional) Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param page: (optional) Page number
        :type page: int
        :param limit: (optional) Number of requests per page, max 200, default 10
        :type limit: int

        .. code:: python

            positions_history = client.get_positions_history()

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {}

        if symbol:
            data["symbol"] = symbol
        if start:
            data["from"] = start
        if end:
            data["to"] = end
        if page:
            data["pageId"] = page
        if limit:
            data["limit"] = limit

        return await self._get(
            "history-positions", True, is_futures=True, data=dict(data, **params)
        )

    async def futures_modify_auto_deposit_margin(self, symbol, status=True, **params):
        """Modify the auto deposit margin status for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/modify-auto-deposit-margin-status

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param status: Status
        :type status: bool

        .. code:: python

            auto_deposit_margin = client.modify_auto_deposit_margin('XBTUSDM', True)

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "status": status}

        return await self._post(
            "position/margin/auto-deposit-status",
            True,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_get_max_withdraw_margin(self, symbol, **params):
        """Get the maximum withdraw margin for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/get-max-withdraw-margin

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string

        .. code:: python

            max_withdraw_margin = client.get_max_withdraw_margin('XBTUSDM')

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "margin/maxWithdrawMargin", True, is_futures=True, data=dict(data, **params)
        )

    async def futures_withdraw_margin(self, symbol, amount, **params):
        """Withdraw margin for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/remove-margin-manually

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param amount: Amount to withdraw
        :type amount: string

        .. code:: python

            withdraw_margin = client.withdraw_margin('XBTUSDM', '100')

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "amount": amount}

        return await self._post(
            "margin/withdrawMargin", True, is_futures=True, data=dict(data, **params)
        )

    async def futures_deposit_margin(self, symbol, margin, biz_no, **params):
        """Deposit margin for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/add-margin-manually

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param margin: Margin
        :type margin: int
        :param biz_no: Business number
        :type biz_no: string

        .. code:: python

            deposit_margin = client.deposit_margin('XBTUSDM', 100, '123456')

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "margin": margin, "bizNo": biz_no}

        return await self._post(
            "position/margin/deposit-margin",
            True,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_get_margin_mode(self, symbol, **params):
        """Get the margin mode for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/get-margin-mode

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string

        .. code:: python

            margin_mode = client.get_margin_mode('XBTUSDM')

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "position/getMarginMode",
            True,
            api_version=self.API_VERSION2,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_modify_margin_mode(self, symbol, mode, **params):
        """Modify the margin mode for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/modify-margin-mode

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param mode: Margin mode (CROSS or ISOLATED)
        :type mode: string

        .. code:: python

            margin_mode = client.modify_margin_mode('XBTUSDM', 'CROSS')

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "marginMode": mode}

        return await self._post(
            "position/changeMarginMode",
            True,
            api_version=self.API_VERSION2,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_get_cross_margin_leverage(self, symbol, **params):
        """Get the cross margin leverage for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/get-cross-margin-leverage

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string

        .. code:: python

            cross_margin_leverage = client.get_cross_margin_leverage('XBTUSDM')

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "getCrossUserLeverage",
            True,
            api_version=self.API_VERSION2,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_modify_cross_margin_leverage(self, symbol, leverage, **params):
        """Modify the cross margin leverage for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/positions/modify-cross-margin-leverage

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param leverage: Leverage
        :type leverage: string

        .. code:: python

            cross_margin_leverage = client.modify_cross_margin_leverage('XBTUSDM', '10')

        :returns: ApiResponse

        .. code:: python

            # todo: example response

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "leverage": leverage}

        return await self._post(
            "changeCrossUserLeverage",
            True,
            api_version=self.API_VERSION2,
            is_futures=True,
            data=dict(data, **params),
        )

    # Futures Risk Limit Endpoints

    async def futures_get_risk_limit_level(self, symbol, **params):
        """Get the risk limit level for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/risk-limit/get-futures-risk-limit-level

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string

        .. code:: python

            risk_limit_level = client.futures_get_risk_limit_level('XBTUSDM')

        :returns: ApiResponse

            {
                "code": "200000",
                "data": [
                    {
                        "symbol": "ADAUSDTM",
                        "level": 1,
                        "maxRiskLimit": 500,
                        "minRiskLimit": 0,
                        "maxLeverage": 20,
                        "initialMargin": 0.05,
                        "maintainMargin": 0.025
                    },
                    {
                        "symbol": "ADAUSDTM",
                        "level": 2,
                        "maxRiskLimit": 1000,
                        "minRiskLimit": 500,
                        "maxLeverage": 2,
                        "initialMargin": 0.5,
                        "maintainMargin": 0.25
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "contracts/risk-limit{}".format(symbol),
            True,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_modify_risk_limit_level(self, symbol, level, **params):
        """Modify the risk limit level for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/risk-limit/modify-risk-limit-level

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param level: Risk limit level
        :type level: int

        .. code:: python

            risk_limit_level = client.futures_modify_risk_limit_level('XBTUSDM', 2)

        :returns: ApiResponse

            {
                "code": "200000",
                "data": true
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "level": level}

        return await self._post(
            "position/risk-limit-level/change",
            True,
            is_futures=True,
            data=dict(data, **params),
        )

    # Futures Funding Fees Endpoints

    async def futures_get_funding_rate(self, symbol, **params):
        """Get the funding rate for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/funding-fees/get-current-funding-rate

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string

        .. code:: python

            funding_rate = client.futures_get_funding_rate('XBTUSDM')

        :returns: ApiResponse

            {
                "code": "200000",
                "data": {
                    "symbol": ".XBTUSDTMFPI8H",
                    "granularity": 28800000,
                    "timePoint": 1731441600000,
                    "value": 0.000641,
                    "predictedValue": 0.000052,
                    "fundingRateCap": 0.003,
                    "fundingRateFloor": -0.003
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        return await self._get(
            "funding-rate/{}/current".format(symbol),
            True,
            is_futures=True,
            data=dict(data, **params),
        )

    async def futures_get_public_funding_history(self, symbol, start, end, **params):
        """Get the public funding history for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/funding-fees/get-public-funding-history

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param start: Start time as unix timestamp
        :type start: int
        :param end: End time as unix timestamp
        :type end: int

        .. code:: python

            funding_history = client.futures_get_public_funding_history('XBTUSDM', 1669508513820, 1669508513820)

        :returns: ApiResponse

            {
                "success": true,
                "code": "200",
                "msg": "success",
                "retry": false,
                "data": [
                    {
                        "symbol": "IDUSDTM",
                        "fundingRate": 0.018750,
                        "timepoint": 1702310700000
                    }
                ]
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol, "from": start, "to": end}

        return await self._get(
            "contract/funding-rates", False, is_futures=True, data=dict(data, **params)
        )

    async def futures_get_private_funding_history(
        self,
        symbol,
        start=None,
        end=None,
        reverse=True,
        offset=None,
        forward=False,
        max_count=None,
        **params,
    ):
        """Get the private funding history for a symbol

        https://www.kucoin.com/docs/rest/futures-trading/funding-fees/get-private-funding-history

        :param symbol: Name of symbol e.g. XBTUSDM
        :type symbol: string
        :param start: (optional) Start time as unix timestamp
        :type start: int
        :param end: (optional) End time as unix timestamp
        :type end: int
        :param reverse: (optional) Reverse the results
        :type reverse: bool
        :param offset: (optional) Offset
        :type offset: int
        :param forward: (optional) Forward the results
        :type forward: bool
        :param max_count: (optional) Maximum number of results
        :type max_count: int

        .. code:: python

            funding_history = client.futures_get_private_funding_history('XBTUSDM')

        :returns: ApiResponse

            {
                "dataList": [
                    {
                        "id": 36275152660006,
                        "symbol": "XBTUSDM",
                        "timePoint": 1557918000000,
                        "fundingRate": 0.000013,
                        "markPrice": 8058.27,
                        "positionQty": 10,
                        "positionCost": -0.001241,
                        "funding": -0.00000464,
                        "settleCurrency": "XBT"
                    },
                    {
                        "id": 36275152660004,
                        "symbol": "XBTUSDM",
                        "timePoint": 1557914400000,
                        "fundingRate": 0.00375,
                        "markPrice": 8079.65,
                        "positionQty": 10,
                        "positionCost": -0.0012377,
                        "funding": -0.00000465,
                        "settleCurrency": "XBT"
                    },
                    {
                        "id": 36275152660002,
                        "symbol": "XBTUSDM",
                        "timePoint": 1557910800000,
                        "fundingRate": 0.00375,
                        "markPrice": 7889.03,
                        "positionQty": 10,
                        "positionCost": -0.0012676,
                        "funding": -0.00000476,
                        "settleCurrency": "XBT"
                    }
                ],
                "hasMore": true
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        data = {"symbol": symbol}

        if start:
            data["startAt"] = start
        if end:
            data["endAt"] = end
        if reverse:
            data["reverse"] = reverse
        if offset:
            data["offset"] = offset
        if forward:
            data["forward"] = forward
        if max_count:
            data["maxCount"] = max_count

        return await self._get(
            "funding-history", True, is_futures=True, data=dict(data, **params)
        )

    # Websocket Endpoints

    async def get_ws_endpoint(self, private=False):
        """Get websocket channel details

        :param private: (optional) True for private channel
        :type private: bool

        https://www.kucoin.com/docs/websocket/basic-info/apply-connect-token/public-token-no-authentication-required-
        https://www.kucoin.com/docs/websocket/basic-info/apply-connect-token/private-channels-authentication-request-required-

        .. code:: python

            ws_details = client.get_ws_endpoint(private=True)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "token": "2neAiuYvAU737TOajb2U3uT8AEZqSWYe0fBD4LoHuXJDSC7gIzJiH4kNTWhCPISWo6nDpAe7aUYs6Y1N4x9p7wSsRU5m3-PcVsqeGGI9bNupipWRcVoGHnwZIngtMdMrjqPnP-biofFWbNaP1cl0X1pZc2SQ-33hDH1LgNP-yg89NEzuQg4KjtLDa9zSoVaC.rc5an2wAXOiNB42guxeKhQ==",
                    "instanceServers": [
                        {
                            "endpoint": "wss://ws-api-spot.kucoin.com/",
                            "encrypt": true,
                            "protocol": "websocket",
                            "pingInterval": 18000,
                            "pingTimeout": 10000
                        }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        path = "bullet-public"
        signed = private
        if private:
            path = "bullet-private"

        return await self._post(path, signed)

    async def futures_get_ws_endpoint(self, private=False):
        """Get websocket futures channel details

        :param private: (optional) True for private channel
        :type private: bool

        https://www.kucoin.com/docs/websocket/basic-info/apply-connect-token/public-token-no-authentication-required-
        https://www.kucoin.com/docs/websocket/basic-info/apply-connect-token/private-channels-authentication-request-required-

        .. code:: python

            ws_details = client.futures_get_ws_endpoint(private=True)

        :returns: ApiResponse

        .. code:: python

            {
                "code": "200000",
                "data": {
                    "token": "2neAiuYvAU737TOajb2U3uT8AEZqSWYe0fBD4LoHuXJDSC7gIzJiH4kNTWhCPISWo6nDpAe7aUYs6Y1N4x9p7wSsRU5m3-PcVsqeGGI9bNupipWRcVoGHnwZIngtMdMrjqPnP-biofFWbNaP1cl0X1pZc2SQ-33hDH1LgNP-yg9a0FbYvs_Bct6QYKlTjDiL.uo5fqwmeBei2enyEh62Qvg==",
                    "instanceServers": [
                        {
                            "endpoint": "wss://ws-api-futures.kucoin.com/",
                            "encrypt": true,
                            "protocol": "websocket",
                            "pingInterval": 18000,
                            "pingTimeout": 10000
                        }
                    ]
                }
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        path = "bullet-public"
        signed = private
        if private:
            path = "bullet-private"

        return await self._post(path, signed, is_futures=True)

    async def get_user_info(self):
        """Get account summary info

        https://www.kucoin.com/docs/rest/account/basic-info/get-account-summary-info

        .. code:: python

            user_info = client.get_user_info()

        :returns: ApiResponse

        .. code:: python

            {
                "level": 0,
                "subQuantity": 5,
                "maxDefaultSubQuantity": 5,
                "maxSubQuantity": 5,
                "spotSubQuantity": 5,
                "marginSubQuantity": 5,
                "futuresSubQuantity": 5,
                "maxSpotSubQuantity": 0,
                "maxMarginSubQuantity": 0,
                "maxFuturesSubQuantity": 0
            }

        :raises: KucoinResponseException, KucoinAPIException

        """

        return await self._get("user-info", True, api_version=self.API_VERSION2)
