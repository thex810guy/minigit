import json
from pathlib import Path

from .blob import Blob
from .repository import Repository
from .types import AddRemoveOperation
from .utils import user_input_to_path


class StagingArea:
    def __init__(self) -> None:
        self.repo = Repository()
        self._files = set()
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

    # User command

    def update_command(self, path_str: str, add_remove_operation: AddRemoveOperation):
        self.repo.ensure_valid()

        self.sync_with_index()
        self._update(
            user_input_to_path(path_str),
            add_remove_operation
        )
        self.save_to_index()

    # Internal methods to update the staging area

    def _update(self, path: Path, add_remove_operation: AddRemoveOperation) -> None:
        if path.is_dir():
            self._update_dir(path, add_remove_operation)
        else:
            self._update_file(path, add_remove_operation)

    def _update_file(self, file: Path, add_remove_operation: AddRemoveOperation) -> None:
        name = str(file)

        if not (name in self.repo.tracked_files):
            print("Following file is not tracked, ignoring: " + name)
            return

        if add_remove_operation == AddRemoveOperation.ADD:
            if name in self._files:
                print("Following file is already in staging area: " + name)
                return

            self._files.add(name)
            print("Added file: " + name)

            blob = Blob(file)
            blob.serialize()
        elif add_remove_operation == AddRemoveOperation.REMOVE:
            if not (name in self._files):
                return

            self._files.remove(name)
            print("Removed file: " + name)

    def _update_dir(self, dir: Path, add_remove_operation: AddRemoveOperation) -> None:
        for path in dir.iterdir():
            self._update(path, add_remove_operation)
