"""Very simple Typer CLI for RDFIngest."""

from pathlib import Path
from typing import Annotated, Union

import typer

from loguru import logger

from rdfingest.cli_help import (
    config_help,
    registry_help,
    drop_help,
    debug_help
)
from rdfingest.ingest import RDFIngest


app = typer.Typer()


@app.command()
def main(
        config: Annotated[
            Path,
            typer.Option(
                "--config", "-c",
                help=config_help,
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                resolve_path = True
            )
        ] = Path("./config.yaml"),
        registry: Annotated[
            Path,
            typer.Option(
                "--registry", "-r",
                help=registry_help,
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                resolve_path = True
            )
        ] = Path("./registry.yaml"),
        drop: Annotated[bool, typer.Option(help=drop_help)] = True,
        debug: Annotated[bool, typer.Option(help=debug_help)] = False,
):
    """RDFIngest CLI.

    Ingest local and remote RDF data sources into a triplestore.
    """
    logger.info("Initializing RDFIngest.")
    rdfingest = RDFIngest(
        config=config,
        registry=registry,
        drop=drop,
        debug=debug
    )

    logger.info(f"Running update requests against '{rdfingest.config.service.endpoint}'.")
    rdfingest.run_ingest()


if __name__ == "__main__":
    app()
