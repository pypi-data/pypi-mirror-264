import json
from datetime import datetime, timedelta, timezone

import bytewax.operators as op
from bytewax.dataflow import Dataflow
from pint import Quantity

from nortech_internal.derivers.repositories.data_db import get_data_db_connection
from nortech_internal.derivers.repositories.Processor import ProcessorSink
from nortech_internal.derivers.repositories.SQL import SQLPartition
from nortech_internal.derivers.repositories.TimeBucketJoin import TimeBucketJoinSource
from nortech_internal.derivers.services.logger import logger
from nortech_internal.derivers.services.metrics import create_metrics
from nortech_internal.derivers.services.schema import get_create_deriver_schema
from nortech_internal.derivers.values.instance import (
    DeployedDeriver,
    Secrets,
)
from nortech_internal.derivers.values.metrics import DataMessage, IdentifyMessage
from nortech_internal.derivers.values.schema import (
    PartialInput,
)

secrets = Secrets()

logger.info(f"Loading Deployed Deriver from {secrets.DEPLOYED_DERIVER_PATH}")
with open(secrets.DEPLOYED_DERIVER_PATH, "r") as f:
    data = json.load(f)

deployed_deriver = DeployedDeriver(**data, secrets=secrets)
logger.info(f"Deployed Deriver: {deployed_deriver}")

create_deriver_schema = get_create_deriver_schema(deployed_deriver.script)
deriver_schema = create_deriver_schema()
logger.info(f"Deriver schema: {deriver_schema}")

db_connection = get_data_db_connection(data_db_URL=secrets.DATABASE_URL)
logger.info("Connected to database")

source = TimeBucketJoinSource(
    input_type=deriver_schema.inputs,
    source_inits={
        name: lambda resume_state, query=deployed_input.query: SQLPartition(
            input_type=PartialInput,
            connection=db_connection,
            query=query,
            cursor_dict=resume_state or {"timestamp": deployed_deriver.start_at},
            batch_size=10000,
        )
        for name, deployed_input in deployed_deriver.inputs.items()
    },
    length=timedelta(seconds=1),
    align_to=datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
)
logger.info(f"Source created {source}")

flow = Dataflow(deployed_deriver.name)

stream = op.input("input", flow, source)


def convert_input(inp):
    for input_name, input in deployed_deriver.inputs.items():
        value = inp.__getattr__(input_name)
        if value is not None:
            inp.__setattr__(
                input_name,
                Quantity(value, input.physicalUnit).to(input.SIUnit).magnitude,
            )

    return inp


converted_input_stream = op.map("convert_input", stream, convert_input)

transformed_stream = deriver_schema.transform_stream(
    converted_input_stream,
    deriver_schema.configurations(**deployed_deriver.configurations),
)


def convert_output(out):
    for output_name, output in deployed_deriver.outputs.items():
        value = out.__getattr__(output_name)
        if value is not None:
            out.__setattr__(
                output_name,
                Quantity(value, output.SIUnit).to(output.physicalUnit).magnitude,
            )

    return out


converted_output_stream = op.map("convert_output", transformed_stream, convert_output)


def convert_to_data_message(message):
    return DataMessage(
        timestamp=message.__getattribute__("timestamp"),
        data=create_metrics(
            timestamp=message.__getattribute__("timestamp"),
            message=message,
            outputs=deployed_deriver.outputs,
        ),
    )


data_message_stream = op.map(
    "convert_to_data_message", converted_output_stream, convert_to_data_message
)

output_sink = ProcessorSink(
    host=secrets.PROCESSOR_HOSTNAME,
    port=secrets.PROCESSOR_PORT,
    identify_message=IdentifyMessage(name=deployed_deriver.name),
)
logger.info(f"Sink created {output_sink}")

op.output("out", data_message_stream, output_sink)
