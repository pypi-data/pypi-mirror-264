from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional

import bytewax.operators as op
from bytewax.dataflow import Dataflow
from bytewax.testing import TestingSink, run_main
from IPython.display import Markdown, display
from pandas import DataFrame
from pint import Quantity
from sqlalchemy import Connection

from nortech_internal.derivers.gateways.muninn import (
    create_deriver,
    get_SQL_queries_from_deriver_inputs,
)
from nortech_internal.derivers.repositories.data_db import get_data_db_connection
from nortech_internal.derivers.repositories.SQL import SQLPartition
from nortech_internal.derivers.repositories.TimeBucketJoin import TimeBucketJoinSource
from nortech_internal.derivers.services.schema import (
    get_deriver_schema_DAG,
)
from nortech_internal.derivers.services.visualize import (
    create_deriver_schema_DAG_mermaid,
    create_deriver_schema_subgraph,
)
from nortech_internal.derivers.values.instance import (
    Deriver,
    DeriverInputType,
    DeriverOutputType,
)
from nortech_internal.derivers.values.schema import (
    ConfigurationType,
    DeriverSchema,
    InputType,
    OutputType,
    PartialInput,
)


@dataclass
class TimeWindow:
    start: datetime
    end: datetime

    def __post_init__(self):
        assert self.start <= self.end


def run_deriver_locally(
    muninn_URL: str,
    deriver: Deriver[
        InputType, OutputType, ConfigurationType, DeriverInputType, DeriverOutputType
    ],
    time_window: TimeWindow,
    data_db_connection: Optional[Connection] = None,
):
    SQL_query_response = get_SQL_queries_from_deriver_inputs(
        muninn_URL=muninn_URL, deriver_inputs=deriver.inputs
    )

    db_connection = (
        data_db_connection
        if data_db_connection
        else get_data_db_connection(SQL_query_response.dataDBURL)
    )

    deriver_schema = deriver.create_deriver_schema()

    source = TimeBucketJoinSource(
        input_type=deriver_schema.inputs,
        stop_at=time_window.end,
        source_inits={
            name: lambda resume_state, query=query: SQLPartition(
                input_type=PartialInput,
                connection=db_connection,
                query=query,
                cursor_dict=resume_state or {"timestamp": time_window.start},
                batch_size=10000,
            )
            for name, query in SQL_query_response.sqlQueries.items()
        },
        length=timedelta(seconds=1),
        align_to=datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )

    flow = Dataflow(deriver.name)

    stream = op.input("input", flow, source)

    input_model_fields = dict(deriver_schema.inputs.model_fields.items())

    def convert_input(inp):
        for input_name, input in deriver.inputs.items():
            if input_name != "timestamp":
                SIUnit: str = input_model_fields[input_name].json_schema_extra[  # type: ignore
                    "physicalQuantity"
                ]["SIUnitSymbol"]

                value = inp.__getattr__(input_name)
                if value is not None:
                    inp.__setattr__(
                        input_name,
                        Quantity(value, input.physicalUnit.symbol).to(SIUnit).magnitude,
                    )

        return inp

    converted_input_stream = op.map("convert_input", stream, convert_input)

    transformed_stream = deriver_schema.transform_stream(
        converted_input_stream, deriver.configurations
    )

    output_model_fields = dict(deriver_schema.outputs.model_fields.items())

    def convert_output(out):
        for output_name, output in deriver.outputs.items():
            if output_name != "timestamp":
                SIUnit: str = output_model_fields[output_name].json_schema_extra[  # type: ignore
                    "physicalQuantity"
                ]["SIUnitSymbol"]

                value = out.__getattr__(output_name)
                if value is not None:
                    out.__setattr__(
                        output_name,
                        Quantity(value, SIUnit)
                        .to(output.physicalUnit.symbol)
                        .magnitude,
                    )

        return out

    converted_output_stream = op.map(
        "convert_output", transformed_stream, convert_output
    )

    output_list = []
    output_sink = TestingSink(output_list)

    op.output("out", converted_output_stream, output_sink)

    run_main(flow)

    return DataFrame([output.model_dump() for output in output_list]).set_index(
        "timestamp"
    )


def deploy_deriver(
    muninn_URL: str,
    deriver: Deriver,
    dry_run: bool,
):
    deriver_schema_DAG = get_deriver_schema_DAG(deriver.create_deriver_schema)

    deriver_diffs = create_deriver(
        muninn_URL=muninn_URL,
        deriver=deriver,
        deriver_schema_DAG=deriver_schema_DAG,
        dry_run=dry_run,
    )

    return deriver_diffs


def visualize_deriver_schema(create_deriver_schema: Callable[[], DeriverSchema]):
    deriver_schema_DAG = get_deriver_schema_DAG(create_deriver_schema)

    mermaid = """
```mermaid
flowchart LR
"""

    mermaid = create_deriver_schema_DAG_mermaid(
        mermaid=mermaid, deriver_schema_DAG=deriver_schema_DAG
    )

    mermaid += """
```
"""

    display(Markdown(mermaid))


def visualize_deriver(deriver: Deriver):
    deriver_schema_DAG = get_deriver_schema_DAG(deriver.create_deriver_schema)

    mermaid = f"""
```mermaid
flowchart LR
    subgraph "Deriver ({deriver.name})"
"""

    mermaid += create_deriver_schema_subgraph(deriver_schema_DAG=deriver_schema_DAG)

    for input_name, input in deriver.inputs.items():
        mermaid += f"""
            {deriver.name.__hash__()}_{input.signal}["{input.signal}<br/>[{input.physicalUnit.symbol.replace(' ', '')}]"] --> {deriver_schema_DAG.name.__hash__()}_{input_name}
        """

    for output_name, output in deriver.outputs.items():
        mermaid += f"""
            {deriver_schema_DAG.name.__hash__()}_{output_name} --> {deriver.name.__hash__()}_{output_name}["{output_name}<br/>[{output.physicalUnit.symbol.replace(' ', '')}]"]
        """

    mermaid += """
end
```
"""

    display(Markdown(mermaid))
