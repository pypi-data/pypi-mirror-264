from datetime import datetime
from typing import Dict, List

from nortech_internal.derivers.values.instance import DeployedOutput
from nortech_internal.derivers.values.metrics import Metric
from nortech_internal.derivers.values.schema import DeriverSchemaOutput


def create_metrics(
    timestamp: datetime,
    message: DeriverSchemaOutput,
    outputs: Dict[str, DeployedOutput],
) -> List[Metric]:
    return [
        Metric(
            index=output_signal.index,
            value=message.__getattribute__(name),
            time_of_real_sample=timestamp,
        )
        for name, output_signal in outputs.items()
        if message.__getattribute__(name) is not None
    ]
