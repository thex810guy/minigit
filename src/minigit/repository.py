import json
import shutil
from pathlib import Path

from .exceptions import (
    RepositoryAlreadyExistsError,
    RepositoryCorrupted,
    RepositoryInitilizationError,
    RepositoryNotFound,
)


class Repository:
    def __init__(self) -> None:
        self.root = Path.cwd() / ".minigit"

        self.files = {
            "name": self.root / "NAME",
            "head": self.root / "HEAD",
            "index": self.root / "index.json", # TODO: switch from json to binary
        }

        self.directories = {
            "refs": self.root / "refs",
            "blobs": self.root / "objects" / "blobs",
            "trees": self.root / "objects" / "trees",
            "commits": self.root / "objects" / "commits",
        }

        self.ignore_file = Path.cwd() / ".minigitignore.json"
        self.ignore = [
            ".minigitignore.json",
            ".minigit",
            ".git",
            ".venv"
        ]
        self.tracked_files = self._get_tracked_files()

    def initialize(self) -> None:
        try:
            self.root.mkdir(exist_ok=False)

            for file in self.files.values():
                file.touch(exist_ok=False)

            for directory in self.directories.values():
                directory.mkdir(parents=True, exist_ok=False)

            self.ignore_file.touch(exist_ok=False)

            # Defaults

            self.files["name"].write_text(Path.cwd().name)
            self.files["head"].write_text("master")
            (self.directories["refs"] / "master.json").touch() # TODO: swtich from json to binary

            self.files["index"].write_text(
                json.dumps(list())
            )
            self.ignore_file.write_text(
                json.dumps(self.ignore)
            )
        except FileExistsError as e:
            raise RepositoryAlreadyExistsError(".minigit or ignore file already exists within the current working directory!") from e
        except OSError as e:
            shutil.rmtree(self.root, ignore_errors=True)

            raise RepositoryInitilizationError("Something went wrong!") from e

    def status(self):
        pass

    def ensure_valid(self) -> None:
        if not self.root.is_dir():
            raise RepositoryNotFound(".minigit directory appears to be missing!")

        if not self.ignore_file.is_file():
            raise RepositoryCorrupted(".minigitignore.json is missing.")

        for file in self.files.values():
            if not file.is_file():
                raise RepositoryCorrupted(f".minigit is missing crucial file {file!s}!")

        for directory in self.directories.values():
            if not directory.is_dir():
                raise RepositoryCorrupted(f".minigit is missing crucial directory {directory!s}!")

    def _get_tracked_files(self) -> set[str]:
        tracked_files = set()

        def _scan_file(path: Path):
            # TODO: Perhaps there is a better way to do this
            if path.name in self.ignore:
                return

            if path.is_file():
                tracked_files.add(str(path.relative_to(Path.cwd())))
            else:
                for file in path.iterdir():
                    _scan_file(file)

        _scan_file(Path.cwd())

        return tracked_files
