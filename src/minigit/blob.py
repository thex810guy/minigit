from hashlib import sha256
from pathlib import Path

from .repository import Repository


class Blob:
    def __init__(self, file: Path) -> None:
        self.repo = Repository()
        self.content = file.read_bytes()
        self.name = sha256(self.content).hexdigest()
        self.path = self.repo.directories["blobs"] / self.name

    def serialize(self):
        self.path.touch()
        self.path.write_bytes(self.content)
