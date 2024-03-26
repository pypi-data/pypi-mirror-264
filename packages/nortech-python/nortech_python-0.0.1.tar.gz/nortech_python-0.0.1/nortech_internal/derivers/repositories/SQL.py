"""Connectors for [SQL](https://en.wikipedia.org/wiki/SQL).

Importing this module requires the
[`SQLAlchemy`](https://github.com/sqlalchemy/sqlalchemy)
package to be installed.

It also requires any database-specific packages to be installed, such as
[`psycopg2`](https://github.com/psycopg/psycopg2) for PostgreSQL.

"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from logging import CRITICAL, getLogger
from typing import Dict, Generic, List, Optional, Type, TypeVar

from bytewax.inputs import StatefulSourcePartition
from sqlalchemy import Connection, text
from sqlalchemy.exc import DBAPIError

from nortech_internal.derivers.services.logger import logger
from nortech_internal.derivers.values.schema import PartialInputType

sqlalchemy_logger = getLogger("sqlalchemy")
sqlalchemy_logger.propagate = False
sqlalchemy_logger.setLevel(CRITICAL)
sqlalchemy_logger.handlers = []

StatefulSourcePartitionState = TypeVar("StatefulSourcePartitionState")


@dataclass
class SQLPartition(
    Generic[PartialInputType, StatefulSourcePartitionState],
    StatefulSourcePartition[PartialInputType, Dict[str, StatefulSourcePartitionState]],
):
    input_type: Type[PartialInputType]

    connection: Connection
    query: str

    cursor_dict: Dict[str, StatefulSourcePartitionState]

    batch_size: int
    backoff_start_delay: float = 1.0
    backoff_factor: float = 2.0
    backoff_max_delay: float = 60.0

    def __post_init__(self):
        self._delay = self.backoff_start_delay
        self._result = None

    def next_batch(self, sched: Optional[datetime]) -> List[PartialInputType]:
        if (
            self._result is None
            or self._result.closed
            or self.connection.get_transaction() is None
        ):
            try:
                self._result = self.connection.execution_options(
                    stream_results=True, yield_per=self.batch_size
                ).execute(text(self.query), self.cursor_dict)
            except DBAPIError as e:
                logger.error(f"DBAPIError occurred: {e}")
                logger.error(f"Statement: {e.statement}")
                logger.error(f"Params: {e.params}")
                logger.error(f"Orig: {e.orig}")
                raise e
        try:
            rows = self._result.fetchmany(self.batch_size)
        except Exception:
            rows = []

        items = []
        for row in rows:
            item = row._asdict()
            items.append(item)

        if items:
            self._delay = self.backoff_start_delay

            last_item = items[-1]
            for key in self.cursor_dict.keys():
                self.cursor_dict[key] = last_item[key]
        else:
            transaction = self.connection.get_transaction()
            if transaction is not None:
                try:
                    transaction.commit()
                except Exception as e:
                    transaction.rollback()
                    logger.error(f"Exception occurred while committing: {e}")

            self._result = None

            self._delay = min(self._delay * self.backoff_factor, self.backoff_max_delay)

        return [self.input_type(**item) for item in items]

    def next_awake(self) -> Optional[datetime]:
        return datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(
            seconds=self._delay
        )

    def snapshot(self) -> Dict[str, StatefulSourcePartitionState]:
        return self.cursor_dict

    def close(self):
        if self._result is not None and not self._result.closed:
            self._result.close()

        self.connection.close()
