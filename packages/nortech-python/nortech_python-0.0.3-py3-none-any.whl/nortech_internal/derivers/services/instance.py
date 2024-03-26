from typing import Any, Callable, Dict

from nortech_internal.derivers.services.schema import (
    get_deriver_schema_DAG,
)
from nortech_internal.derivers.values.instance import CWADUS
from nortech_internal.derivers.values.schema import DeriverSchema, DeriverSchemaDAG


def get_CWADUS_from_inputs(inputs: Dict[Any, str]) -> Dict[str, CWADUS]:
    CWADUS_dict = {}

    for key, value in inputs.items():
        CWADUS_values = value.split("/")

        if len(CWADUS_values) != 6:
            raise ValueError(
                f"CWADUS values must be in the format: <customer>/<workspace>/<asset>/<division>/<unit>/<signal> but only got {CWADUS_values}"
            )

        CWADUS_dict[key[0]] = CWADUS(
            customer=CWADUS_values[0],
            workspace=CWADUS_values[1],
            asset=CWADUS_values[2],
            division=CWADUS_values[3],
            unit=CWADUS_values[4],
            signal=CWADUS_values[5],
        )

    return CWADUS_dict


def get_stored_deriver_to_deploy(
    create_deriver_schema: Callable[[], DeriverSchema],
) -> DeriverSchemaDAG:
    stored_deriver_schema = get_deriver_schema_DAG(create_deriver_schema)

    return stored_deriver_schema
