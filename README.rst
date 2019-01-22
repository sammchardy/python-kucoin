================================
Welcome to python-kucoin v2.0.0
================================

.. image:: https://img.shields.io/pypi/v/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/pypi/l/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/travis/sammchardy/python-kucoin.svg
    :target: https://travis-ci.org/sammchardy/python-kucoin

.. image:: https://img.shields.io/coveralls/sammchardy/python-kucoin.svg
    :target: https://coveralls.io/github/sammchardy/python-kucoin

.. image:: https://img.shields.io/pypi/wheel/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

.. image:: https://img.shields.io/pypi/pyversions/python-kucoin.svg
    :target: https://pypi.python.org/pypi/python-kucoin

This is an unofficial Python wrapper for the `Kucoin exchanges REST API v2 <https://docs.kucoin.com/>`_. I am in no way affiliated with Kucoin, use at your own risk.


PyPi
  https://pypi.python.org/pypi/python-kucoin

Source code
  https://github.com/sammchardy/python-kucoin

Documentation
  https://python-kucoin.readthedocs.io/en/latest/

Blog with examples
  https://sammchardy.github.io


Features
--------

- Implementation of REST endpoints
- Simple handling of authentication
- Response exception handling

TODO
----

- Implement websockets

Quick Start
-----------

Register an account with `Kucoin <https://www.kucoin.com/#/?r=E42cWB>`_.

To test on the Sandbox register with `Kucoin Sandbox <https://sandbox.kucoin.com/ucenter/signup?rcode=ewcefH>`_.

`Generate an API Key <https://kucoin.com/account/api>`_ and enable it.

.. code:: bash

    pip install python-kucoin

If you are looking for the older v1 API install python-kucoin==0.1.12

.. code:: bash

    pip install python-kucoin==0.1.12

.. code:: python

    from kucoin.client import Client
    client = Client(api_key, api_secret, api_passphrase, sandbox=True)

    # get currencies
    currencies = client.get_currencies()

    # get market depth
    depth = client.get_order_book('KCS-BTC')

    # get symbol klines
    klines = client.get_kline_dat('KCS-BTC')

    # place a market buy order
    order = client.create_market_order('NEO', Client.SIDE_BUY, size=20)

    # get list of active orders
    orders = client.get_active_orders('KCS-BTC')


For more `check out the documentation <https://python-kucoin.readthedocs.io/en/latest/>`_.

Donate
------

If this library helped you out feel free to donate.

- ETH: 0xD7a7fDdCfA687073d7cC93E9E51829a727f9fE70
- NEO: AVJB4ZgN7VgSUtArCt94y7ZYT6d5NDfpBo
- LTC: LPC5vw9ajR1YndE1hYVeo3kJ9LdHjcRCUZ
- BTC: 1Dknp6L6oRZrHDECRedihPzx2sSfmvEBys

Other Exchanges
---------------

If you use `Binance <https://www.binance.com/?ref=10099792>`_ check out my `python-binance <https://github.com/sammchardy/python-binance>`_ library.

If you use `Allcoin <https://www.allcoin.com/Account/RegisterByPhoneNumber/?InviteCode=MTQ2OTk4MDgwMDEzNDczMQ==>`_ check out my `python-allucoin <https://github.com/sammchardy/python-allcoin>`_ library.

If you use `IDEX <https://idex.market>`_ check out my `python-idex <https://github.com/sammchardy/python-idex>`_ library.

If you use `BigONE <https://big.one>`_ check out my `python-bigone <https://github.com/sammchardy/python-bigone>`_ library.

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-kucoin?pixel
