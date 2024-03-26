from typing import Dict, Generic

from pydantic import BaseModel, Field
from requests import post

from nortech_internal.derivers.values.instance import (
    Deriver,
    DeriverInputType,
    DeriverOutputType,
)
from nortech_internal.derivers.values.schema import ConfigurationType, DeriverSchemaDAG


class SQLQueryResponse(BaseModel):
    sqlQueries: Dict[str, str]
    dataDBURL: str


def get_SQL_queries_from_deriver_inputs(
    muninn_URL: str, deriver_inputs: Dict[str, DeriverInputType]
) -> SQLQueryResponse:
    SQL_queries_from_CWADUS_endpoint = (
        muninn_URL + "/api/deriver/getSQLQueryFromDeriverInputs"
    )

    request = {
        "deriverInputs": {
            name: {
                "customer": CWADUS_value.customer,
                "workspace": CWADUS_value.workspace,
                "asset": CWADUS_value.asset,
                "division": CWADUS_value.division,
                "unit": CWADUS_value.unit,
                "signal": CWADUS_value.signal,
            }
            for name, CWADUS_value in deriver_inputs.items()
        }
    }

    response = post(
        url=SQL_queries_from_CWADUS_endpoint,
        json=request,
    )

    try:
        assert response.status_code == 200
    except AssertionError:
        if response.status_code == 500:
            raise AssertionError(
                f"Failed to get SQL queries from CWADUS list. "
                f"Status code: {response.status_code}. "
                f"Response: {response.json()}"
            )
        else:
            raise AssertionError(
                f"Failed to get SQL queries from CWADUS list. "
                f"Status code: {response.status_code}. "
            )

    return SQLQueryResponse(**response.json())


class CreateDeriver(
    BaseModel, Generic[DeriverInputType, DeriverOutputType, ConfigurationType]
):
    name: str = Field()
    description: str = Field()

    inputs: Dict[str, DeriverInputType] = Field()
    outputs: Dict[str, DeriverOutputType] = Field()
    configurations: ConfigurationType = Field()

    startAt: str = Field()


class CreateDeriverRequest(
    BaseModel, Generic[DeriverInputType, DeriverOutputType, ConfigurationType]
):
    deriver: CreateDeriver[DeriverInputType, DeriverOutputType, ConfigurationType]
    deriverSchemaDAG: DeriverSchemaDAG = Field()

    dryRun: bool = Field()


def create_deriver(
    muninn_URL: str,
    deriver: Deriver,
    deriver_schema_DAG: DeriverSchemaDAG,
    dry_run: bool,
):
    deriver_DAG_endpoint = muninn_URL + "/api/deriver/createDeriver"

    create_deriver_request = CreateDeriverRequest(
        deriver=CreateDeriver(
            name=deriver.name,
            description=deriver.description,
            inputs=deriver.inputs,
            outputs=deriver.outputs,
            configurations=deriver.configurations,
            startAt=str(deriver.start_at),
        ),
        deriverSchemaDAG=deriver_schema_DAG,
        dryRun=dry_run,
    )

    response = post(
        url=deriver_DAG_endpoint,
        json=create_deriver_request.model_dump(),
    )

    try:
        assert response.status_code == 200
    except AssertionError:
        raise AssertionError(
            f"Failed to create DeriverDAG. "
            f"Status code: {response.status_code}. "
            f"Response: {response.json()}"
        )

    return response.json()
