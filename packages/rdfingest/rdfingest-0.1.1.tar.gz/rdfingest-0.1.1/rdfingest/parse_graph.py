"""ParseGraph: A simple rdflib.Graph subclass with an additional format resolution strategy for parsing."""

from loguru import logger
from rdflib import Graph
from rdflib.plugin import PluginException
from rdflib.util import guess_format


class ParseGraph(Graph):
    """Simple rdflib.Graph subclass for parsing "text/plain" remote sources.

    rdflib.Graph.parse exclusively uses the response header content type for parsing remote sources.
    If the content type is "text/plain" this fails because there is no parser registered for "text/plain"
    and no further resolution strategy to obtain an applicable parser is pursued.

    ParseGraph.parse mostly is an rdflib.Graph.parse proxy which calls guess_format explicitly on a PluginException.
    See https://github.com/RDFLib/rdflib/issues/2734.
    """
    def parse(self, *args, **kwargs):
        try:
            graph = super().parse(*args, **kwargs)
        except PluginException:
            guessed_format = guess_format(kwargs["source"])

            logger.info("Encountered PluginException")
            logger.info(f"Retrying to parse with guessed format '{guessed_format}'.")

            kwargs.update({"format": guessed_format})
            graph = super().parse(*args, **kwargs)

        return graph
