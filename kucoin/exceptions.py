# coding=utf-8

import json

# System error codes
# Code	Meaning
# 403000	No Auth -- The requested is forbidden for current API key.
# 404000	Url Not Found -- The request resource could not be found
# 400100	Parameter Error -- You tried to access the resource with invalid parameters
# 411100	User are frozen -- User are frozen, please contact us via support center.
# 500000	Internal Server Error -- We had a problem with our server. Try again later.


class KucoinAPIException(Exception):
    """Exception class to handle general API Exceptions

        `code` values

        `message` format

    """
    def __init__(self, response):
        self.code = ''
        self.message = 'Unknown Error'
        try:
            json_res = response.json()
        except ValueError:
            self.message = response.content
        else:
            if 'error' in json_res:
                self.message = json_res['error']
            if 'msg' in json_res:
                self.message = json_res['msg']
            if 'message' in json_res and json_res['message'] != 'No message available':
                self.message += ' - {}'.format(json_res['message'])
            if 'code' in json_res:
                self.code = json_res['code']
            if 'data' in json_res:
                try:
                    self.message += " " + json.dumps(json_res['data'])
                except ValueError:
                    pass

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'KucoinAPIException {}: {}'.format(self.code, self.message)


class KucoinRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'KucoinRequestException: {}'.format(self.message)


class MarketOrderException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'MarketOrderException: {}'.format(self.message)


class LimitOrderException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'MarketOrderException: {}'.format(self.message)
