Getting Started
===============

Installation
------------

``python-kucoin`` is available on `PYPI <https://pypi.python.org/pypi/python-kucoin/>`_.
Install with ``pip``:

.. code:: bash

    pip install python-kucoin


Register on Kucoin
-------------------

Firstly register an account with `Kucoin <https://www.kucoin.com/#/?r=E42cWB>`_.

Generate an API Key
-------------------

To use signed account methods you are required to `create an API Key <https://www.kucoin.com/#/user/setting/api>`_ and enable it.

Initialise the client
---------------------

Pass your API Key and Secret

.. code:: python

    from kucoin.client import Client
    client = Client(api_key, api_secret)

    # optionally pass the language you would like to use
    # see client.get_languages() for options
    client = Client(api_key, api_secret, language='zh_CN)


API Rate Limit
--------------

Unknown
