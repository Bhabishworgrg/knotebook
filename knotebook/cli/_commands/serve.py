from typer import Typer

from knotebook.logging import logger


serve_app: Typer = Typer()


@serve_app.command()
def serve():
    logger.info('Serving')
