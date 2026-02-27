from typer import Typer

from ._commands.serve import serve_app


app: Typer = Typer()
app.add_typer(serve_app)
