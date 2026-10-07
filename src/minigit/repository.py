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

    def ensure_valid(self) -> None:
        if not self.root.is_dir():
            raise RepositoryNotFound(".minigit directory appears to be missing!")

        for file in self.files.values():
            if not file.is_file():
                raise RepositoryCorrupted(f".minigit is missing crucial file {file!s}!")

        for directory in self.directories.values():
            if not directory.is_dir():
                raise RepositoryCorrupted(f".minigit is missing crucial directory {directory!s}!")

    def initialize(self) -> None:
        try:
            self.root.mkdir(exist_ok=False)

            for file in self.files.values():
                file.touch(exist_ok=False)

            for directory in self.directories.values():
                directory.mkdir(parents=True, exist_ok=False)

            # Defaults

            self.files["name"].write_text(Path.cwd().name)
            self.files["head"].write_text("master")
            (self.directories["refs"] / "master.json").touch() # TODO: swtich from json to binary

        except FileExistsError as e:
            raise RepositoryAlreadyExistsError(".minigit already exists within the current working directory!") from e
        except OSError as e:
            shutil.rmtree(self.root, ignore_errors=True)

            raise RepositoryInitilizationError("Something went wrong!") from e
