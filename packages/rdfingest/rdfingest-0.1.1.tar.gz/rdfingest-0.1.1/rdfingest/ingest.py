"""RDFIngest.

Automatically ingest local and/or remote RDF data sources indicated in a YAML registry into a triplestore.
"""

import gzip

from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from http import HTTPStatus

import requests

from SPARQLWrapper import SPARQLWrapper, DIGEST, POST
from loguru import logger
from rdflib import BNode, Dataset, Graph, URIRef
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID

from rdfingest.parse_graph import ParseGraph

from rdfingest.yaml_loaders import config_loader, registry_loader
from rdfingest.models import RegistryModel, ConfigModel
from rdfingest.ingest_strategies import (
    gzip_strategy,
    serialize_strategy,
    semantic_chunk_strategy,
    UpdateStrategy
)


class BNodeIDException(Exception):
    """Exception for indicating that a Graph has a Bnode ID."""


class RDFIngest:
    """RDFIngest class.

    This class provides functionality for automatically ingesting local/remote RDF data sources
    indicated in a YAML registry into a triplestore.

    :param registry: Indicites a local YAML file which registers local/remote RDF data sources.
    This YAML file gets validated against rdfingest.models.RegistryModel.

    :param config: Indicates a local YAML file which holds credentials for a triplestore.
    This YAML file gets validated against rdfingest.models.ConfigModel.
    """
    def __init__(
            self,
            registry: str | Path = "./registry.yaml",
            config: str | Path = "./config.yaml",
            drop: bool = True,
            debug: bool = False,
            strategies: tuple[UpdateStrategy, ...] = (
                serialize_strategy,
                gzip_strategy
            )
    ) -> None:
        """RDFIngester initializer."""
        self.registry: RegistryModel = registry_loader(registry)
        self.config: ConfigModel = config_loader(config)
        self._drop = drop
        self._debug = debug
        self._strategies = strategies


    @staticmethod
    def _parse_entry_sources(
            source: list[str],
            graph_id: str | None = None
    ) -> Iterator[Graph]:
        """Parse entry sources and generate contextualized Graphs.

        For contextless RDF sources, graph_id specified in registry.yaml is assigned,
        for contextualized RDF sources, the Dataset is split into separate graphs.

        Note that (at least for now) the default graph of Datasets is ignored.
        Named graphs are a good thing, performing automated POST/DROP operations
        on a remote default graph seems inadvisable.
        """
        _get_extension = lambda x: str(x).rpartition(".")[-1]
        _default_graph_id = DATASET_DEFAULT_GRAPH_ID
        _graph_id = (
            URIRef(str(graph_id))
            if graph_id is not None
            else graph_id
        )

        for _source in source:
            if (extension := _get_extension(_source)) in ("trig", "trix"):
                dataset = Dataset()
                dataset.parse(source=_source, format=extension)
                yield from filter(
                    lambda g: g.identifier != _default_graph_id,
                    dataset.contexts()
                )
            else:
                graph = ParseGraph(identifier=_graph_id)
                graph.parse(source=_source)
                yield graph

    @staticmethod
    def _get_dataset_from_graph(graph: Graph) -> Dataset:
        """Get a single context dataset from a Graph.

        Graph should have an identifier explicitly defined,
        BNode identifiers are not allowed.
        """
        if isinstance(graph.identifier, BNode):
            raise BNodeIDException(f"Graph object '{graph}' has BNode identifier.")

        dataset = Dataset()
        dataset.graph(graph)
        return dataset

    def _log_status_code(self, response: requests.Response) -> None:
        """Log the response.status_code either with loglevel 'info' or 'warning'."""
        log_level: str = "info" if (200 <= response.status_code <= 299) else "warning"
        log_method: Callable = getattr(logger, log_level)
        log_message: str = (
            f"HTTP status code {response.status_code} "
            f"('{HTTPStatus(response.status_code).phrase}')."
        )

        log_method(log_message)

        if self._debug:
            logger.debug(response.content)

    def _run_sparql_drop(self, graph_id: str) -> None:
        """Run a SPARQL CLEAR request for a named graph against the configured triplestore."""
        sparql = SPARQLWrapper(self.config.service.endpoint)
        sparql.setCredentials(
            self.config.service.user,
            self.config.service.password
        )
        sparql.setMethod(POST)

        sparql.setQuery(f"CLEAR GRAPH <{graph_id}>")
        results = sparql.query()
        logger.info(f"SPARQL response: {results.response.code}")

    def _run_named_graph_update_request(self, named_graph: Dataset) -> requests.Response:
        """Execute a POST request for a named graph against the config store.

        Note: This is used as a side-effects only callable.
        """
        endpoint = str(self.config.service.endpoint)
        auth: tuple[str, str] = self.config.service.user, self.config.service.password

        for strategy in self._strategies:
            response = strategy(named_graph, endpoint, auth)
            self._log_status_code(response)

            if response.status_code > 199 and response.status_code < 300:
                return response

        return response

    def run_ingest(self) -> None:
        """Run ingest operations for RDF sources.

        Parse graphs from a registry, optionally run DROP operations
        and POST graph data to the specified triplestore.
        """
        for entry in self.registry.graphs:
            logger.info(f"Parsing graphs for {entry.source}.")

            graphs = list(
                self._parse_entry_sources(
                    source=entry.source,     # type: ignore ; see source field validator
                    graph_id=entry.graph_id  # type: ignore ; see source field validator
                )
            )

            if self._drop:
                for graph_id in set(g.identifier for g in graphs):
                    logger.info(
                        "Running SPARQL DROP operation for named graph " +
                        str(graph_id)
                    )
                    self._run_sparql_drop(graph_id)

            for graph in graphs:
                dataset = self._get_dataset_from_graph(graph)
                self._run_named_graph_update_request(dataset)
