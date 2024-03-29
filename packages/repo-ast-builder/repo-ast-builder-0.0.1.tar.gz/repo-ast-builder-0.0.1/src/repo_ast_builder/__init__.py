from pathlib import Path

from .file_walking import walk
import json


def read_ast(path: str) -> str:
    return json.dumps(walk(Path(path)))
