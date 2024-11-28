import time
from kucoin.exceptions import KucoinAPIException, KucoinRequestException
from kucoin.utils import compact_json_dict, get_loop
import aiohttp
from .base_client import BaseClient


class AsyncClientBase(BaseClient):
    def __init__(
        self,
        api_key: str = None,
        api_secret: str = None,
        api_passphrase: str = None,
        is_sandbox: bool = False,
        loop = None,
        request_params = None,
    ):
        self.loop = loop or get_loop()
        super().__init__(
            api_key, api_secret, api_passphrase, is_sandbox, request_params
        )

    def _init_session(self) -> aiohttp.ClientSession:
        session = aiohttp.ClientSession(loop =self.loop, headers=self._get_headers())
        return session

    async def close(self):
        await self._session.close()

    async def _handle_response(self, response: aiohttp.ClientResponse):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status).startswith("2"):
            raise KucoinAPIException(response, response.status, await response.text())
        try:
            return await response.json()
        except ValueError:
            txt = await response.text()
            raise KucoinRequestException(f"Invalid Response: {txt}")

    async def _request(
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
        uri = self._create_uri(full_path, is_futures)

        if signed:
            # generate signature
            nonce = int(time.time() * 1000)
            kwargs["headers"]["KC-API-TIMESTAMP"] = str(nonce)
            kwargs["headers"]["KC-API-SIGN"] = self._generate_signature(
                nonce, method, full_path, kwargs["data"]
            )
            kwargs["headers"]["KC-API-PARTNER"] = self.SPOT_KC_PARTNER
            kwargs["headers"]["KC-API-PARTNER-VERIFY"] = "true"
            kwargs["headers"]["KC-API-PARTNER-SIGN"] = self._sign_partner()

        if kwargs["data"]:
            if method == "post":
                kwargs["data"] = compact_json_dict(kwargs["data"])
            else:
                kwargs["params"] = kwargs["data"]
                del kwargs["data"]

        async with getattr(self.session, method)(
            uri,
            **kwargs,
        ) as response:
            self.response = response
            return await self._handle_response(response)

    async def _get(
        self, path, signed=False, api_version=None, is_futures=False, **kwargs
    ):
        return await self._request(
            "get", path, signed, api_version, is_futures, **kwargs
        )

    async def _post(
        self, path, signed=False, api_version=None, is_futures=False, **kwargs
    ):
        return await self._request(
            "post", path, signed, api_version, is_futures, **kwargs
        )

    async def _put(
        self, path, signed=False, api_version=None, is_futures=False, **kwargs
    ):
        return await self._request(
            "put", path, signed, api_version, is_futures, **kwargs
        )

    async def _delete(
        self, path, signed=False, api_version=None, is_futures=False, **kwargs
    ):
        return await self._request(
            "delete", path, signed, api_version, is_futures, **kwargs
        )
