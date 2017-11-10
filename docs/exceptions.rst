Exceptions
==========

KucoinResponseException
-----------------------

Raised if a non JSON response is returned

KucoinAPIException
------------------

On an API call error a quoine.exceptions.QuoineAPIException will be raised.

The exception provides access to the

- `status_code` - response status code
- `response` - response object
- `message` - Quoine error message dictionary
- `request` - request object if available

.. code:: python

    try:
        client.get_coin_list()
    except KucoinAPIException as e:
        print(e.status_code)
        print(e.message)

KucoinResolutionException
-------------------------

Raised if resolution entered for kline data is invalid
