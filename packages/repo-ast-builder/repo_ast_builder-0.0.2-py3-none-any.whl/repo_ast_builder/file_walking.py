import ast
from pathlib import Path

from .nodes import process_node


def walk(directory: Path) -> dict:
    repository_info: dict = {}

    for file_path in directory.rglob("*.py"):
        relative_path = file_path.relative_to(directory)
        if ".venv" in str(relative_path):
            continue
        package_path = relative_path.parent

        root_node = repository_info
        for part in package_path.parts:
            root_node = root_node.setdefault(part, {"type": "package"})

        try:
            with file_path.open("r") as f:
                tree = ast.parse(f.read())

            for node in tree.body:
                process_node(node, root_node, file_path, directory)
        except SyntaxError as e:
            print(f"Skipping file {file_path} due to syntax error: {str(e)}")
            continue

    return repository_info