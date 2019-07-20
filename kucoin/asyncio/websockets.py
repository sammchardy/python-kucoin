import asyncio
import json
import logging
import time
from random import random

import websockets as ws


class KucoinSocketManagerPrivateException(Exception):
    pass


class ReconnectingWebsocket:

    MAX_RECONNECTS = 5
    MAX_RECONNECT_SECONDS = 60
    MIN_RECONNECT_WAIT = 0.1
    TIMEOUT = 10
    PROTOCOL_VERSION = '1.0.0'

    def __init__(self, loop, client, coro, private=False):
        self._loop = loop
        self._log = logging.getLogger(__name__)
        self._coro = coro
        self._reconnect_attempts = 0
        self._conn = None
        self._ws_details = None
        self._connect_id = None
        self._client = client
        self._private = private
        self._last_ping = None
        self._socket = None

        self._connect()

    def _connect(self):
        self._conn = asyncio.ensure_future(self._run(), loop=self._loop)

    async def _run(self):

        keep_waiting = True
        self._last_ping = time.time()  # record last ping
        # get the websocket details
        self._ws_details = None
        self._ws_details = self._client.get_ws_endpoint(self._private)

        async with ws.connect(self._get_ws_endpoint(), ssl=self._get_ws_encryption()) as socket:
            self._socket = socket
            self._reconnect_attempts = 0

            try:
                while keep_waiting:
                    if time.time() - self._last_ping > self._get_ws_pingtimeout():
                        await self.send_ping()
                    try:
                        evt = await asyncio.wait_for(self._socket.recv(), timeout=self._get_ws_pingtimeout())
                    except asyncio.TimeoutError:
                        self._log.debug("no message in {} seconds".format(self._get_ws_pingtimeout()))
                        await self.send_ping()
                    except asyncio.CancelledError:
                        self._log.debug("cancelled error")
                        await self._socket.ping()
                    else:
                        try:
                            evt_obj = json.loads(evt)
                        except ValueError:
                            pass
                        else:
                            await self._coro(evt_obj)
            except ws.ConnectionClosed:
                keep_waiting = False
                await self._reconnect()
            except Exception as e:
                self._log.debug('ws exception:{}'.format(e))
                keep_waiting = False
                await self._reconnect()

    def _get_ws_endpoint(self):
        if not self._ws_details:
            raise Exception("Unknown Websocket details")

        self._ws_connect_id = str(int(time.time() * 1000))
        token = self._ws_details['token']
        endpoint = self._ws_details['instanceServers'][0]['endpoint']

        ws_endpoint = f"{endpoint}?token={token}&connectId={self._ws_connect_id}"
        if self._private:
            ws_endpoint += '&acceptUserMessage=true'
        return ws_endpoint

    def _get_ws_encryption(self):
        if not self._ws_details:
            raise Exception("Unknown Websocket details")

        return self._ws_details['instanceServers'][0]['encrypt']

    def _get_ws_pingtimeout(self):

        if not self._ws_details:
            raise Exception("Unknown Websocket details")

        ping_timeout = int(self._ws_details['instanceServers'][0]['pingTimeout'] / 1000 / 2) - 1
        return ping_timeout

    async def _reconnect(self):
        await self.cancel()
        self._reconnect_attempts += 1
        if self._reconnect_attempts < self.MAX_RECONNECTS:

            self._log.debug(f"websocket reconnecting {self.MAX_RECONNECTS - self._reconnect_attempts} attempts left")
            reconnect_wait = self._get_reconnect_wait(self._reconnect_attempts)
            await asyncio.sleep(reconnect_wait)
            self._connect()
        else:
            # maybe raise an exception
            self._log.error(f"websocket could not reconnect after {self._reconnect_attempts} attempts")
            pass

    def _get_reconnect_wait(self, attempts):
        expo = 2 ** attempts
        return round(random() * min(self.MAX_RECONNECT_SECONDS, expo - 1) + 1)

    async def send_ping(self):
        msg = {
            'id': str(int(time.time() * 1000)),
            'type': 'ping'
        }
        await self._socket.send(json.dumps(msg))
        self._last_ping = time.time()

    async def send_message(self, msg, retry_count=0):
        if not self._socket:
            if retry_count < 5:
                await asyncio.sleep(1)
                await self.send_message(msg, retry_count + 1)
        else:
            msg['id'] = str(int(time.time() * 1000))
            msg['privateChannel'] = self._private
            await self._socket.send(json.dumps(msg))

    async def cancel(self):
        try:
            self._conn.cancel()
        except asyncio.CancelledError:
            pass


class KucoinSocketManager:

    PRIVATE_TOPICS = [
        '/account/balance'
    ]

    def __init__(self):
        """Initialise the IdexSocketManager

        """
        self._callback = None
        self._conn = None
        self._loop = None
        self._client = None
        self._private = False
        self._log = logging.getLogger(__name__)

    @classmethod
    async def create(cls, loop, client, callback, private=False):
        self = KucoinSocketManager()
        self._loop = loop
        self._client = client
        self._private = private
        self._callback = callback
        self._conn = ReconnectingWebsocket(loop, client, self._recv, private)
        return self

    async def _recv(self, msg):
        if 'data' in msg:
            await self._callback(msg)

    async def subscribe(self, topic):
        """Subscribe to a channel

        :param topic: required
        :type topic: str
        :returns: None

        Sample ws response

        .. code-block:: python

            {
                "type":"message",
                "topic":"/market/ticker:BTC-USDT",
                "subject":"trade.ticker",
                "data":{
                    "sequence":"1545896668986",
                    "bestAsk":"0.08",
                    "size":"0.011",
                    "bestBidSize":"0.036",
                    "price":"0.08",
                    "bestAskSize":"0.18",
                    "bestBid":"0.049"
                }
            }

        Error response

        .. code-block:: python

            {
                'code': 404,
                'data': 'topic /market/ticker:BTC-USDT is not found',
                'id': '1550868034537',
                'type': 'error'
            }

        """

        req_msg = {
            'type': 'subscribe',
            'topic': topic,
            'response': True
        }

        if topic in self.PRIVATE_TOPICS and not self._private:
            raise KucoinSocketManagerPrivateException(
                "Initialise KucoinSocketManager with private=true for {} topic".format(topic)
            )

        await self._conn.send_message(req_msg)

    async def unsubscribe(self, topic):
        """Unsubscribe from a topic

        :param topic: required
        :type topic: str

        :returns: None

        Sample ws response

        .. code-block:: python

            {
                "id": "1545910840805",
                "type": "ack"
            }

        """

        req_msg = {
            'type': 'unsubscribe',
            'topic': topic,
            'response': True
        }

        await self._conn.send_message(req_msg)
