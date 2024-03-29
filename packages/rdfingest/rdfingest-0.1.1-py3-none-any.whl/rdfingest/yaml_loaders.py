"""Loader callables for reading YAML files."""

from functools import partial
from pathlib import Path

from typing import TypeAlias, TypeVar
from collections.abc import Callable

import yaml
from pydantic import BaseModel, ValidationError

from rdfingest.models import ConfigModel, RegistryModel, InvalidRegistryEntry


ModelType = TypeVar("ModelType", bound=BaseModel)
Loader: TypeAlias = Callable[[str | Path], ModelType]


class YAMLValidationError(Exception):
    """Exception for indicating a Pydanitc ValidationError from a YAML loader."""


def yaml_loader(path: str | Path, model: type[ModelType]) -> ModelType:
    """Load a YAML file from disc and validate it against a model."""
    _data: dict = yaml.safe_load(Path(path).read_text())

    try:
        data = model(**_data)
    except (ValidationError, InvalidRegistryEntry) as e:
        raise YAMLValidationError(e)

    return data


config_loader: Loader = partial(yaml_loader, model=ConfigModel)
registry_loader: Loader = partial(yaml_loader, model=RegistryModel)
