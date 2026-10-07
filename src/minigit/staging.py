import json
from pathlib import Path

from .repository import Repository
from .types import AddRemoveOperation


class StagingArea:
    def __init__(self) -> None:
        self.repo = Repository()
        self._files = set() # Avoids duplicates
        self._staging_file = self.repo.files["index"]

    # Read/Write with the internal staging area and index

    def sync_with_index(self) -> None:
        try:
            self._files = set(
                json.loads(self._staging_file.read_text())
            )
        except json.JSONDecodeError:
            # TODO: This always occurs when the repository is first initliazed, change this behavior
            print("Unable to load index file, might be empty")
            self._files = set()

    def save_to_index(self):
        self._staging_file.write_text(
            # Sets can't be serialized
            json.dumps(list(self._files))
        )

    # Add/Remove to staging area

    def update(self, path: Path, add_remove_operation: AddRemoveOperation) -> None:
        if path.is_dir():
            self._update_dir(path, add_remove_operation)
        else:
            self._update_file(path, add_remove_operation)

    def _update_file(self, file: Path, add_remove_operation: AddRemoveOperation) -> None:
        name = str(file)

        if add_remove_operation == AddRemoveOperation.ADD:
            # Duplicates are handled but the user isn't informed
            # Report if file is already staged
            self._files.add(name)
            print("Added file: " + name)
        elif add_remove_operation == AddRemoveOperation.REMOVE:
            try:
                self._files.remove(name)
                print("Removed file: " + name)
            except KeyError:
                print("Unable to remove following file as it was not staged: " + name)

    def _update_dir(self, dir: Path, add_remove_operation: AddRemoveOperation) -> None:
        for path in dir.iterdir():
            self.update(path, add_remove_operation)
