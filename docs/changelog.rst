Changelog
=========

v0.1.4 - 2010-01-14
^^^^^^^^^^^^^^^^^^^

**Added**

- add function `get_historical_klines_tv` to get klines in OHLCV format

**Fixed**

- handle success: false type errors properly to raise exception
- fix passed param name on `get_kline_data`

v0.1.3 - 2010-01-12
^^^^^^^^^^^^^^^^^^^

**Added**

- add function `get_total_balance` to get balance in Fiat
- added pagination params to `get_all_balances`

v0.1.2 - 2010-01-07
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
