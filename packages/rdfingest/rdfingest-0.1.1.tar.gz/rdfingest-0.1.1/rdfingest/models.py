"""Pydantic Models for RDFIngest."""

import re

from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    ConfigDict,
    FilePath,
    ValidationError,
    field_validator,
    model_validator,
)


class InvalidRegistryEntry(Exception):
    """Exception indicating an invalid RegistryEntry."""


class RegistryEntry(BaseModel):
    source: AnyHttpUrl | FilePath | list[AnyHttpUrl | FilePath]
    graph_id: AnyUrl | None = None

    model_config = ConfigDict(extra="forbid")  # type: ignore

    @field_validator("source")
    @classmethod
    def _make_source_list(cls, value):
        """Ensure that the source field holds a list + string cast from pydantic_core.Url."""
        source = (
            [str(value)]
            if not isinstance(value, list)
            else [str(v) for v in value])

        return source

    @model_validator(mode="after")
    @classmethod
    def _check_trigs(cls, data):
        """Check if a graph_id is defined for non-Trig input."""
        trig_check = not any(
            re.match(r".+\.trig\/?", str(source))
            for source in data.source
        )

        if trig_check and (data.graph_id is None):
            raise InvalidRegistryEntry(
                """Model field 'graph_id' is required for non-Trig input"""
            )

        return data


class RegistryModel(BaseModel):
    graphs: list[RegistryEntry]


class ServiceModel(BaseModel):
    endpoint: AnyHttpUrl
    user: str
    password: str


class ConfigModel(BaseModel):
    service: ServiceModel
