import typer

from .repository import Repository

app = typer.Typer()

@app.command()
def init() -> None:
    repository = Repository()
    repository.initialize()

# Temporary function so there's atleast two command for typer
# to function normally
@app.command()
def do_nothing() -> None:
    pass

def main() -> None:
    app()
