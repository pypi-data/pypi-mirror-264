from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from functools import reduce
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, Type, TypeVar

import pandas as pd
from bytewax.inputs import FixedPartitionedSource, StatefulSourcePartition

from nortech_internal.derivers.services.logger import logger
from nortech_internal.derivers.values.schema import InputType, PartialInputType

StatefulSourcePartitionState = TypeVar("StatefulSourcePartitionState")


@dataclass
class TimeBucketState(Generic[PartialInputType, StatefulSourcePartitionState]):
    source_states: Dict[str, StatefulSourcePartitionState]
    source_buffers: Dict[str, List[PartialInputType]]


def join_source_buffers(source_buffers: Dict[str, List[PartialInputType]]):
    # Create DataFrames from source_buffers
    dataframes = {
        name: pd.DataFrame([message.model_dump() for message in buffer])
        for name, buffer in source_buffers.items()
    }

    # Perform the outer join using Pandas and reduce
    merged_df = reduce(
        lambda left, right: pd.merge(left, right, on="timestamp", how="outer"),
        dataframes.values(),
    )

    # Sort merged_df by timestamp
    merged_df = merged_df.sort_values(by="timestamp")

    return merged_df


def flatten_df_to_records(
    input_type: Type[InputType], df: pd.DataFrame
) -> List[InputType]:
    # Convert the DataFrame to list of dictionaries
    records = map(input_type.model_validate, df.to_dict("records"))

    return list(records)


def is_within_window(
    timestamp: datetime, window_start: datetime, window_end: datetime
) -> bool:
    return window_start <= timestamp < window_end


@dataclass
class _TimeBucketJoinPartition(
    Generic[InputType, PartialInputType, StatefulSourcePartitionState],
    StatefulSourcePartition[InputType, StatefulSourcePartitionState],
):
    input_type: Type[InputType]

    sources: Dict[str, StatefulSourcePartition[Any, StatefulSourcePartitionState]]

    length: timedelta
    align_to: datetime

    max_awake: Optional[datetime] = None

    output_buffer: List[InputType] = field(default_factory=list)
    source_buffers: Dict[str, List[PartialInputType]] = field(default_factory=dict)

    stop_at: Optional[datetime] = None

    def __post_init__(self):
        self.update_current_window(self.align_to)

    def update_current_window(self, timestamp: datetime):
        time_since_alignment = timestamp - self.align_to
        self.current_window_start = (
            self.align_to + (time_since_alignment // self.length) * self.length
        )
        self.current_window_end = self.current_window_start + self.length

    def pull_sources(self) -> Tuple[bool, bool]:
        all_outside_window = True
        all_done = True

        for name, source in self.sources.items():
            buffer = self.source_buffers[name]
            last_timestamp = buffer[-1].timestamp if len(buffer) else self.align_to

            if is_within_window(
                last_timestamp, self.current_window_start, self.current_window_end
            ):
                all_outside_window = False

                try:
                    next_messages = source.next_batch(None)
                    all_done = False
                except StopIteration:
                    next_messages = []

                if not next_messages:
                    next_wake = source.next_awake()

                    if next_wake is not None:
                        self.max_awake = (
                            max(self.max_awake, next_wake)
                            if self.max_awake
                            else next_wake
                        )

                    continue

                for next_message in next_messages:
                    next_message.timestamp = next_message.timestamp.replace(
                        tzinfo=timezone.utc
                    )
                    self.source_buffers[name].append(next_message)

        return all_outside_window, all_done

    def split_buffers(self) -> Dict[str, List[PartialInputType]]:
        buffers_within_window: Dict[str, List[PartialInputType]] = {}

        for name, buffer in self.source_buffers.items():
            # Given that buffers are in order by timestamp
            split_index = next(
                (
                    index
                    for index, msg in enumerate(buffer)
                    if msg.timestamp >= self.current_window_end
                    or (msg.timestamp >= self.stop_at if self.stop_at else False)
                ),
                len(buffer),
            )

            if len(buffer[:split_index]) > 0:
                buffers_within_window[name] = buffer[:split_index]

            self.source_buffers[name] = buffer[split_index:]

        return buffers_within_window

    def next_batch(self, sched: Optional[datetime]) -> List[InputType]:
        if self.current_window_start >= self.stop_at if self.stop_at else False:
            raise StopIteration()

        all_outside_window, all_done = self.pull_sources()

        if all_outside_window or all_done:
            buffers_within_window = self.split_buffers()

            if len(buffers_within_window):
                merged_df = join_source_buffers(buffers_within_window)

                for name in self.input_type.model_fields.keys():
                    if name not in merged_df.columns:
                        merged_df[name] = None

                self.output_buffer = flatten_df_to_records(
                    input_type=self.input_type, df=merged_df
                )

            next_window_start = min(
                [
                    buffer[0].timestamp
                    for buffer in self.source_buffers.values()
                    if buffer
                ]
                or [self.current_window_end]
            )
            self.update_current_window(next_window_start)

        output = self.output_buffer
        self.output_buffer = []

        if (
            all_done
            and all(len(buffer) == 0 for buffer in self.source_buffers.values())
            and len(output) == 0
        ):
            raise StopIteration()

        return output

    def next_awake(self) -> Optional[datetime]:
        max_awake = self.max_awake
        self.max_awake = None

        return max_awake

    def snapshot(
        self,
    ) -> TimeBucketState[PartialInputType, StatefulSourcePartitionState]:
        source_states = {
            source_name: source.snapshot()
            for source_name, source in self.sources.items()
        }

        self.state = TimeBucketState(
            source_states=source_states, source_buffers=self.source_buffers
        )

        logger.info(f"Snapshot state: {self.state.source_states}")
        return self.state

    def close(self):
        for source in self.sources.values():
            source.close()


@dataclass
class TimeBucketJoinSource(
    Generic[InputType, PartialInputType, StatefulSourcePartitionState],
    FixedPartitionedSource[
        InputType,
        Optional[TimeBucketState[PartialInputType, StatefulSourcePartitionState]],
    ],
):
    input_type: Type[InputType]
    source_inits: Dict[
        str,
        Callable[
            [Optional[StatefulSourcePartitionState]],
            StatefulSourcePartition[PartialInputType, StatefulSourcePartitionState],
        ],
    ]
    length: timedelta
    align_to: datetime

    stop_at: Optional[datetime] = None

    def list_parts(self) -> List[str]:
        return ["single"]

    def build_part(
        self,
        now: datetime,
        for_part,
        resume_state: Optional[
            TimeBucketState[PartialInputType, StatefulSourcePartitionState]
        ],
    ):
        if resume_state is not None:
            sources = {
                name: self.source_inits[name](state)
                for name, state in resume_state.source_states.items()
            }
        else:
            sources = {
                name: self.source_inits[name](None) for name in self.source_inits
            }

        source_buffers = (
            resume_state.source_buffers
            if resume_state
            else {name: [] for name in sources.keys()}
        )

        return _TimeBucketJoinPartition(
            input_type=self.input_type,
            sources=sources,
            stop_at=self.stop_at,
            length=self.length,
            align_to=self.align_to,
            source_buffers=source_buffers,
        )
