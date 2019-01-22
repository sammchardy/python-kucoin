Constants
=========

Kucoin defines constants for Redord Types, Order Side, Order Status and Resolution. These are accessible from the Client class.

.. code:: python

    SIDE_BUY = 'buy'
    SIDE_SELL = 'sell'

    ACCOUNT_MAIN = 'main'
    ACCOUNT_TRADE = 'trade'


    ORDER_LIMIT = 'limit'
    ORDER_MARKET = 'market'
    ORDER_LIMIT_STOP = 'limit_stop'
    ORDER_MARKET_STOP = 'market_stop'

    STOP_LOSS = 'loss'
    STOP_ENTRY = 'entry'

    STP_CANCEL_NEWEST = 'CN'
    STP_CANCEL_OLDEST = 'CO'
    STP_DECREASE_AND_CANCEL = 'DC'
    STP_CANCEL_BOTH = 'CB'

    TIMEINFORCE_GOOD_TILL_CANCELLED = 'GTC'
    TIMEINFORCE_GOOD_TILL_TIME = 'GTT'
    TIMEINFORCE_IMMEDIATE_OR_CANCEL = 'IOC'
    TIMEINFORCE_FILL_OR_KILL = 'FOK'

Use in your code like below.

.. code:: python

    from kucoin.client import Client

    order_side = Client.SIDE_BUY
