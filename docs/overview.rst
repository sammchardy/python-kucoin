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

Response Timestamps
-------------------

Most responses return a server timestamp, to fetch this use the `get_last_timestamp` function.

.. code:: python

    products = client.get_currencies()
    timestamp = client.get_last_timestamp()


Requests Settings
-----------------

`python-binance` uses the `requests <http://docs.python-requests.org/en/master/>`_ library.

You can set custom requests parameters for all API calls when creating the client.

.. code:: python

    client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})

Check out the `requests documentation <http://docs.python-requests.org/en/master/>`_ for all options.

**Proxy Settings**

You can use the Requests Settings method above

.. code:: python

    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080'
    }

    # in the Client instantiation
    client = Client("api-key", "api-secret", {'proxies': proxies})

Or set an environment variable for your proxy if required to work across all requests.

An example for Linux environments from the `requests Proxies documentation <http://docs.python-requests.org/en/master/user/advanced/#proxies>`_ is as follows.

.. code-block:: bash

    $ export HTTP_PROXY="http://10.10.1.10:3128"
    $ export HTTPS_PROXY="http://10.10.1.10:1080"

For Windows environments

.. code-block:: bash

    C:\>set HTTP_PROXY=http://10.10.1.10:3128
    C:\>set HTTPS_PROXY=http://10.10.1.10:1080

API Rate Limit
--------------

Currently no rate limits
