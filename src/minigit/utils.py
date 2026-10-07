from pathlib import Path

from .exceptions import PathNotFound


def user_input_to_path(input_str: str):
    path: Path = Path(input_str)

    if not path.exists():
        raise PathNotFound("Couldn't find file/directory: " + str(path))

    return path
