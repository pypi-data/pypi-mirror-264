from datetime import datetime
from typing import Any, Callable, Dict, Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from nortech_internal.derivers.values.physical_units_schema import PhysicalUnit
from nortech_internal.derivers.values.schema import (
    ConfigurationType,
    DeriverSchema,
    InputType,
    OutputType,
)


class CWADUS(BaseModel):
    customer: str = Field()
    workspace: str = Field()
    asset: str = Field()
    division: str = Field()
    unit: str = Field()
    signal: str = Field()


class DeriverInput(CWADUS):
    physicalUnit: PhysicalUnit


class DeriverOutput(CWADUS):
    physicalUnit: PhysicalUnit


DeriverInputType = TypeVar("DeriverInputType", bound=DeriverInput)
DeriverOutputType = TypeVar("DeriverOutputType", bound=DeriverOutput)


class Deriver(
    BaseModel,
    Generic[
        InputType, OutputType, ConfigurationType, DeriverInputType, DeriverOutputType
    ],
):
    name: str = Field()
    description: str = Field()

    inputs: Dict[Any, DeriverInputType] = Field()
    outputs: Dict[Any, DeriverOutputType] = Field()
    configurations: ConfigurationType = Field()

    start_at: datetime = Field()

    create_deriver_schema: Callable[
        [], DeriverSchema[InputType, OutputType, ConfigurationType]
    ] = Field()

    def __init__(self, **data):
        super().__init__(**data)
        # Parse inputs
        self.inputs = {
            str(key[0]): value
            for key, value in self.inputs.items()
            if isinstance(key, tuple) and len(key) > 0
        }
        # Parse outputs
        self.outputs = {
            str(key[0]): value
            for key, value in self.outputs.items()
            if isinstance(key, tuple) and len(key) > 0
        }


class DeployedInput(BaseModel):
    physicalUnit: str = Field()
    SIUnit: str = Field()

    query: str = Field()


class DeployedOutput(BaseModel):
    physicalUnit: str = Field()
    SIUnit: str = Field()

    index: int = Field()


class Secrets(BaseSettings):
    DATABASE_URL: str = Field(default=...)
    PROCESSOR_HOSTNAME: str = Field(default=...)
    PROCESSOR_PORT: int = Field(default=...)
    BATCH_SIZE: int = Field(default=...)
    DEPLOYED_DERIVER_PATH: str = Field(default=...)


class DeployedDeriver(BaseModel):
    name: str = Field()
    description: str = Field()

    inputs: Dict[str, DeployedInput] = Field()
    outputs: Dict[str, DeployedOutput] = Field()
    configurations: Dict[str, Any] = Field()
    script: str

    start_at: datetime = Field()

    secrets: Secrets = Field()
