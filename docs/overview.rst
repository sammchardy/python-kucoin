Getting Started
===============

This API has been updated to work with the v2 Sandbox

Installation
------------

``python-kucoin`` is available on `PYPI <https://pypi.python.org/pypi/python-kucoin/>`_.
Install with ``pip``:

.. code:: bash

    pip install python-kucoin

For previous v1 API install with

.. code:: bash

    pip install python-kucoin==0.1.12

Register on Kucoin
-------------------

Firstly register an account with `Kucoin <https://www.kucoin.com/ucenter/signup?rcode=E42cWB>`_.

To test on the Sandbox register with `Kucoin Sandbox <https://sandbox.kucoin.com/ucenter/signup?rcode=ewcefH>`_.

Generate an API Key
-------------------

To use signed account methods you are required to `create an API Key <https://kucoin.com/account/api>`_ and enable it.

Initialise the client
---------------------

Pass your API Key, Secret and API Passphrase

.. code:: python

    from kucoin.client import Client
    client = Client(api_key, api_secret, api_passphrase)


Requests Settings
-----------------

`python-kucoin` uses the `requests <http://docs.python-requests.org/en/master/>`_ library.

You can set custom requests parameters for all API calls when creating the client.

.. code:: python

    client = Client("api-key", "api-secret", "api-passphrase", {"verify": False, "timeout": 20})

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

Public Endpoints - 30 requests per ten seconds.

Private Endpoints - 50 requests per ten seconds.

* Websocket *

Connect - 30 times per minutes

Subscribe - 120 times per minute

Unsubscribe - 120 times per minute
