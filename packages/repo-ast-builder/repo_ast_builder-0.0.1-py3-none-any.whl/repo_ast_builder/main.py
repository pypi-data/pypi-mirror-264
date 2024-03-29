import json
import sys
from pathlib import Path

from .file_walking import walk


def main():
    if len(sys.argv) < 2:
        print("Please provide the project path as a command-line argument.")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    if not project_path.exists() or not project_path.is_dir():
        print("Invalid project path. Please provide a valid directory path.")
        sys.exit(1)

    print(f"Created {project_path.name}.json")
    with open(f"{project_path.name}.json", "w") as file:
        file.write(json.dumps(walk(project_path)))


if __name__ == "__main__":
    main()
