from dataclasses import dataclass
from typing import List

from bytewax.outputs import DynamicSink, StatelessSinkPartition

from nortech_internal.derivers.gateways.producer import SocketClient
from nortech_internal.derivers.values.metrics import DataMessage, IdentifyMessage


@dataclass
class ProcessorPartition(StatelessSinkPartition):
    socket_client: SocketClient

    def write_batch(self, items: List[DataMessage]):
        data_message = DataMessage(timestamp=items[0].timestamp, data=[])

        for message in items:
            for metric in message.data:
                data_message.data.append(metric)

        self.socket_client.send(data_message)

    def close(self):
        self.socket_client.disconnect()


@dataclass
class ProcessorSink(DynamicSink):
    host: str
    port: int
    identify_message: IdentifyMessage
    backoff_max_delay: int = 60
    backoff_factor: float = 2.0

    def build(self, worker_index, worker_count):
        socket_client = SocketClient(
            host=self.host,
            port=self.port,
            identify_message=self.identify_message,
            backoff_max_delay=self.backoff_max_delay,
            backoff_factor=self.backoff_factor,
        )

        return ProcessorPartition(socket_client=socket_client)
