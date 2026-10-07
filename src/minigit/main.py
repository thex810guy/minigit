import typer

from .repository import Repository
from .staging import StagingArea
from .types import AddRemoveOperation
from .utils import user_input_to_path

app = typer.Typer()
repo = Repository()
staging_area = StagingArea()

@app.command()
def init() -> None:
    repo.initialize()

@app.command() # TODO: Migrate removing to its own command
def add(path_str: str, operation_add: bool = True) -> None:
    operation = AddRemoveOperation.ADD if operation_add else AddRemoveOperation.REMOVE
    repo.ensure_valid()

    staging_area.sync_with_index() # TODO: Migrate into main()
    staging_area.update(
        user_input_to_path(path_str),
        operation
    )
    staging_area.save_to_index()

def main() -> None:
    app()
