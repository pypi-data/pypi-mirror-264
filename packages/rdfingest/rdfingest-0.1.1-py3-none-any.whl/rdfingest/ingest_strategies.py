"""Strategies for updating a triplestore."""

import gzip
import requests

from tempfile import NamedTemporaryFile
from collections.abc import Callable
from typing import TypeAlias

from loguru import logger
from rdflib import Dataset


UpdateStrategy: TypeAlias = Callable[
    [Dataset, str, tuple[str, str]],
    requests.Response
]


def serialize_strategy(
        named_graph: Dataset,
        endpoint: str,
        auth: tuple[str, str]
) -> requests.Response:
    """Gzip update strategy."""

    logger.info(f"Running 'Serialize POST' strategy")

    response = requests.post(
        url=endpoint,
        headers={"Content-Type": "application/x-trig"},
        data=named_graph.serialize(format="trig"),
        auth=auth,
        stream=True
    )

    return response

def gzip_strategy(
        named_graph: Dataset,
        endpoint: str,
        auth: tuple[str, str]
) -> requests.Response:
    """Gzip update strategy."""
    compressed = gzip.compress(named_graph.serialize(format="trig").encode("utf-8"))

    logger.info(f"Running 'Gzip POST' strategy")

    response = requests.post(
        url=endpoint,
        headers={"Content-Type": "application/x-trig", "Content-Encoding": "gzip"},
        data=compressed,
        auth=auth,
        stream=True
    )

    return response


def semantic_chunk_strategy(
        named_graph: Dataset,
        endpoint: str,
        auth: tuple[str, str]
) -> requests.Response:
    """Chunk post strategy."""
    #### note: This needs to do "semantic chunking".
    #### i.e. for every graph in a Dataset POST a set of triple chunks
    #### this can utilize serialize_post_strategy!
    pass
