Changelog
=========

v2.1.1 - 2010-04-17
^^^^^^^^^^^^^^^^^^^^

**Added**

- websocket support for private messages
- `get_historical_orders` function to get V1 historical orders

**Fixed**

- fixed `get_ticker` to work for all tickers
- websocket reconnect ability


v2.1.0 - 2010-02-25
^^^^^^^^^^^^^^^^^^^^

**Added**

- websocket support
- `get_fiat_prices` function to get fiat price for currency
- `get_markets` function to get supported market list
- iceberg order support
- util functions to generate uuid and convert dict to compact json string

**Updated**

- `get_ticker` to have optional symbol param

**Fixed**

- market and limit order create functions
- `get_kline_data` function
- `get_account_holds` function endpoint
- LimitOrderException message


v2.0.2 - 2010-02-23
^^^^^^^^^^^^^^^^^^^^

**Fixed**

- signature generation for get requests


v2.0.1 - 2010-01-23
^^^^^^^^^^^^^^^^^^^^

**Fixed**

- added auth for get_fills()

v2.0.0 - 2019-01-22
^^^^^^^^^^^^^^^^^^^^

**Added**

- support for REST endpoint of v2 API

v0.1.12 - 2018-04-27
^^^^^^^^^^^^^^^^^^^^

**Added**

- timestamp in milliseconds to `get_historical_klines_tv` function

**Fixed**

- make `coin` parameter required in `get_coin_info` function

v0.1.11 - 2018-03-01
^^^^^^^^^^^^^^^^^^^^

**Added**

- option for passing requests module parameters on Client initialisation

**Restored**

- old `get_all_balances` non-paged functionality

v0.1.10 - 2018-02-10
^^^^^^^^^^^^^^^^^^^^

**Fixed**

- remove slash in path in `get_order_details` function

v0.1.9 - 2018-02-09
^^^^^^^^^^^^^^^^^^^

**Updated**

- path for `get_all_balances` to match update in Kucoin docs, now supports pagination

v0.1.8 - 2018-01-20
^^^^^^^^^^^^^^^^^^^

**Added**

- better exception error messages

**Fixed**

- `cancel_order` format to make `order_type` required

v0.1.7 - 2018-01-17
^^^^^^^^^^^^^^^^^^^

**Fixed**

- `cancel_order` format to send symbol in payload, remove URL params
- `cancel_all_orders` format to send symbol in payload, remove URL params


v0.1.6 - 2018-01-15
^^^^^^^^^^^^^^^^^^^

**Added**

- constants for transfer types, pending, finished and cancelled
- documentation for `group` param on `get_order_book`, `get_buy_orders` and `get_sell_orders`
- add `get_trading_markets` endpoint
- add `market` param to `get_trading_symbols` and `get_trending_coins`
- add `get_coin_info` function with optional `coin` param

**Fixed**

- set coin param to optional for `get_reward_info`, `get_reward_summary` and `extract_invite_bonus`
- actually use the `kv_format` param on `get_active_orders`
- `cancel_order` format to send symbol in URL
- `cancel_all_orders` format to send symbol in URL
- `order_details` removed symbol from URL
- `get_tick` symbol is now optional
- fix `get_coin_list` URL


v0.1.5 - 2018-01-14
^^^^^^^^^^^^^^^^^^^

**Fixed**

- remove debug output

v0.1.4 - 2018-01-14
^^^^^^^^^^^^^^^^^^^

**Added**

- add function `get_historical_klines_tv` to get klines in OHLCV format

**Fixed**

- handle success: false type errors properly to raise exception
- fix passed param name on `get_kline_data`

v0.1.3 - 2018-01-12
^^^^^^^^^^^^^^^^^^^

**Added**

- add function `get_total_balance` to get balance in Fiat
- added pagination params to `get_all_balances`

v0.1.2 - 2018-01-07
^^^^^^^^^^^^^^^^^^^

**Added**

- api key endpoints
- set default currency function
- extract invite bonus function

v0.1.1 - 2018-01-02
^^^^^^^^^^^^^^^^^^^

**Added**

- cancel all orders function
- get order details function
- get dealt orders function

**Updated**

- old get_deal_orders function to get_symbol_dealt_orders

v0.1.0 - 2017-11-12
^^^^^^^^^^^^^^^^^^^

**Added**

- Kucoin client interface
- Coverage for all main endpoints
- Constants for transfer type and status, order side and kline resolution
- Full documentation
