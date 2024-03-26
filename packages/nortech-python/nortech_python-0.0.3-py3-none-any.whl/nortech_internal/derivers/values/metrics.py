from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional


class MessageType(str, Enum):
    IDENTIFY = "identify"
    DATA = "data"


@dataclass
class IdentifyMessage:
    name: str
    type: Literal[MessageType.IDENTIFY] = MessageType.IDENTIFY


@dataclass
class Metric:
    index: int
    value: Optional[float]
    time_of_real_sample: Optional[datetime]


@dataclass
class DataMessage:
    timestamp: datetime
    data: List[Metric]
    type: Literal[MessageType.DATA] = MessageType.DATA
