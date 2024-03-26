from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from json import dumps
from logging import getLogger
from socket import AF_INET, SOCK_STREAM
from socket import error as SocketError
from socket import socket as Socket
from struct import pack
from time import sleep
from typing import Callable, Optional

from nortech_internal.derivers.values.metrics import DataMessage, IdentifyMessage

logger = getLogger()


def try_with_backoff(
    backoff_factor: float,
    backoff_max_delay: int,
    try_function: Callable,
    destroy_function: Callable,
):
    delay = 1  # start with a delay of 1 second
    while True:
        try:
            try_function()
            return
        except SocketError:
            destroy_function()

            delay = delay * backoff_factor
            if delay > backoff_max_delay:
                raise SocketClientError(
                    f"Maximum backoff delay of {backoff_max_delay} seconds reached communicating with Processor."
                )

            sleep(delay)


class SocketClientError(Exception):
    pass


@dataclass
class SocketClient:
    host: str
    port: int
    identify_message: IdentifyMessage
    socket: Optional[Socket] = None
    backoff_max_delay: int = 60  # maximum delay in seconds
    backoff_factor: float = 2.0  # factor by which to increase delay

    def __post_init__(self):
        self.connect()

    def connect(self):
        if not self.socket:

            def try_function():
                self.socket = Socket(AF_INET, SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.socket.sendall(json_to_packet(value=self.identify_message))

            try_with_backoff(
                backoff_factor=self.backoff_factor,
                backoff_max_delay=self.backoff_max_delay,
                try_function=try_function,
                destroy_function=self.disconnect,
            )

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def send(self, value: DataMessage):
        packet = json_to_packet(value=value)

        def try_function():
            self.connect()
            self.socket.sendall(packet)  # type: ignore

        try_with_backoff(
            backoff_factor=self.backoff_factor,
            backoff_max_delay=self.backoff_max_delay,
            try_function=try_function,
            destroy_function=self.disconnect,
        )


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        obj = obj.replace(tzinfo=timezone.utc)

        return int(obj.timestamp() * 1000)

    raise TypeError("Type %s not serializable" % type(obj))


def json_to_packet(value):
    packet_json = dumps(asdict(value), default=json_serial).encode("utf-8")
    json_length = len(packet_json)

    len_array = pack(">I", json_length)
    full_packet = len_array + packet_json

    return full_packet
