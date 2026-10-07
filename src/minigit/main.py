import typer

from .repository import Repository
from .staging import StagingArea
from .types import AddRemoveOperation

app = typer.Typer()
repo = Repository()
staging_area = StagingArea()

@app.command()
def init() -> None:
    repo.initialize()

@app.command() # TODO: Migrate removing to its own command
def add(path_str: str) -> None:
    staging_area.update_command(path_str, AddRemoveOperation.ADD)

@app.command()
def restore(path_str: str, staged: bool = False):
    if not staged:
        print("Restore without --staged flag is work in progress!")
        return

    staging_area.update_command(path_str, AddRemoveOperation.REMOVE)

def main() -> None:
    app()
