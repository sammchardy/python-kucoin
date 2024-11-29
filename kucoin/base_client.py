import base64
import hashlib
import hmac
import time

import requests

from .exceptions import KucoinAPIException, KucoinRequestException
from .utils import compact_json_dict


class BaseClient:
    REST_API_URL = "https://api.kucoin.com"
    REST_FUTURES_API_URL = "https://api-futures.kucoin.com"
    # SANDBOX_API_URL = 'https://openapi-sandbox.kucoin.com' # does not supported anymore
    API_VERSION = "v1"
    API_VERSION2 = "v2"
    API_VERSION3 = "v3"

    SIDE_BUY = "buy"
    SIDE_SELL = "sell"

    ACCOUNT_MAIN = "main"
    ACCOUNT_TRADE = "trade"

    ORDER_LIMIT = "limit"
    ORDER_MARKET = "market"
    ORDER_LIMIT_STOP = "limit_stop"  # deprecated
    ORDER_MARKET_STOP = "market_stop"  # deprecated

    STOP_LOSS = "loss"
    STOP_ENTRY = "entry"

    STP_CANCEL_NEWEST = "CN"
    STP_CANCEL_OLDEST = "CO"
    STP_DECREASE_AND_CANCEL = "DC"
    STP_CANCEL_BOTH = "CB"

    TIMEINFORCE_GOOD_TILL_CANCELLED = "GTC"
    TIMEINFORCE_GOOD_TILL_TIME = "GTT"
    TIMEINFORCE_IMMEDIATE_OR_CANCEL = "IOC"
    TIMEINFORCE_FILL_OR_KILL = "FOK"

    SPOT_KC_PARTNER = "python-kucoinspot"
    SPOT_KC_KEY = "922783d1-067e-4a31-bb42-4d1589624e30"

    FUTURES_KC_PARTNER = "python-kucoinfutures"
    FUTURES_KC_KEY = "5c0f0e56-a866-44d9-a50b-8c7c179dc915"

    def __init__(
        self, api_key, api_secret, passphrase, sandbox=False, requests_params=None
    ):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.API_PASSPHRASE = passphrase
        if sandbox:
            raise KucoinAPIException(
                "Sandbox mode is not supported anymore. See https://www.kucoin.com/docs/beginners/sandbox. To test orders, use test methods (e.g. create_test_order)"
            )
        else:
            self.API_URL = self.REST_API_URL
            self.FUTURES_API_URL = self.REST_FUTURES_API_URL

        self._requests_params = requests_params
        self.session = self._init_session()

    def _get_headers(self):
        headers = {
            "Accept": "application/json",
            "User-Agent": "python-kucoin",
            "Content-Type": "application/json",
            "KC-API-KEY": self.API_KEY,
            "KC-API-PASSPHRASE": self.API_PASSPHRASE,
        }
        return headers

    def _init_session(self):
        session = requests.session()
        session.headers.update(self._get_headers())
        return session

    def _sign_partner(self, is_futures=False):
        nonce = int(time.time() * 1000)
        partner = self.FUTURES_KC_PARTNER if is_futures else self.SPOT_KC_PARTNER
        sig_str = "{}{}{}".format(nonce, partner, self.API_KEY).encode(
            "utf-8"
        )
        key = self.FUTURES_KC_KEY if is_futures else self.SPOT_KC_KEY
        m = hmac.new(key.encode("utf-8"), sig_str, hashlib.sha256)
        return base64.b64encode(m.digest()).decode('latin-1')

    @staticmethod
    def _get_params_for_sig(data):
        """Convert params to ordered string for signature

        :param data:
        :return: ordered parameters like amount=10&price=1.1&type=BUY

        """
        return "&".join(["{}={}".format(key, data[key]) for key in data])

    def _generate_signature(self, nonce, method, path, data):
        """Generate the call signature

        :param path:
        :param data:
        :param nonce:

        :return: signature string

        """

        data_json = ""
        endpoint = path
        if method == "get" or method == "delete":
            if data:
                query_string = self._get_params_for_sig(data)
                endpoint = "{}?{}".format(path, query_string)
        elif data:
            data_json = compact_json_dict(data)
        sig_str = (
            "{}{}{}{}".format(nonce, method.upper(), endpoint, data_json)
        ).encode("utf-8")
        m = hmac.new(self.API_SECRET.encode("utf-8"), sig_str, hashlib.sha256)
        return base64.b64encode(m.digest()).decode('latin-1')

    def _create_path(self, path, api_version=None):
        api_version = api_version or self.API_VERSION
        return "/api/{}/{}".format(api_version, path)

    def _create_url(self, path, is_futures=False):
        base_url = self.FUTURES_API_URL if is_futures else self.API_URL
        return "{}{}".format(base_url, path)

    def _request(
        self, method, path, signed, api_version=None, is_futures=False, **kwargs
    ):
        # set default requests timeout
        kwargs["timeout"] = 10

        # add our global requests params
        if self._requests_params:
            kwargs.update(self._requests_params)

        kwargs["data"] = kwargs.get("data", {})
        kwargs["headers"] = kwargs.get("headers", {})

        full_path = self._create_path(path, api_version)
        url = self._create_url(full_path, is_futures)

        if signed:
            # generate signature
            nonce = int(time.time() * 1000)
            kwargs["headers"]["KC-API-TIMESTAMP"] = str(nonce)
            kwargs["headers"]["KC-API-SIGN"] = self._generate_signature(
                nonce, method, full_path, kwargs["data"]
            )
            kwargs["headers"]["KC-API-PARTNER"] = (
                self.FUTURES_KC_PARTNER if is_futures else self.SPOT_KC_PARTNER
            )
            kwargs["headers"]["KC-API-PARTNER-VERIFY"] = "true"
            kwargs["headers"]["KC-API-PARTNER-SIGN"] = self._sign_partner(is_futures)

        if kwargs["data"]:
            if method == "post":
                kwargs["data"] = compact_json_dict(kwargs["data"])
            else:
                kwargs["params"] = kwargs["data"]
                del kwargs["data"]

        response = getattr(self.session, method)(url, **kwargs)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        """Internal helper for handling API responses from the Kucoin server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """

        if not str(response.status_code).startswith("2"):
            raise KucoinAPIException(response, response.status_code, response.text)
        try:
            res = response.json()

            if "code" in res and res["code"] != "200000":
                raise KucoinAPIException(response, response.status_code, response.text)

            if "success" in res and not res["success"]:
                raise KucoinAPIException(response, response.status_code, response.text)

            # by default return full response
            # if it's a normal response we have a data attribute, return that
            if "data" in res:
                res = res["data"]
            return res
        except ValueError:
            raise KucoinRequestException("Invalid Response: %s" % response.text)

    def _get(self, path, signed=False, api_version=None, is_futures=False, **kwargs):
        return self._request("get", path, signed, api_version, is_futures, **kwargs)

    def _post(self, path, signed=False, api_version=None, is_futures=False, **kwargs):
        return self._request("post", path, signed, api_version, is_futures, **kwargs)

    def _put(self, path, signed=False, api_version=None, is_futures=False, **kwargs):
        return self._request("put", path, signed, api_version, is_futures, **kwargs)

    def _delete(self, path, signed=False, api_version=None, is_futures=False, **kwargs):
        return self._request("delete", path, signed, api_version, is_futures, **kwargs)

    def close_connection(self):
        if self.session:
            assert self.session
            self.session.close()
