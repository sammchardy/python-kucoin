Changelog
=========

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
