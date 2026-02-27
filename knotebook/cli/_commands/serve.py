from typer import Typer

from knotebook.logging import logger
from knotebook.server import DevServer


serve_app: Typer = Typer()

@serve_app.command()
def serve(host: str = '127.0.0.1', port: int = 3000):
    logger.info(f'Starting the server at http://{host}:{port}... (Press Ctrl+C to quit)')

    httpd: DevServer = DevServer(host, port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('Shutting down the server gracefully... (Press Ctrl+C again to force)')
        httpd.shutdown()
        httpd.server_close()
