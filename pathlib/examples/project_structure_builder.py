#!/usr/bin/env python3
"""
Project Structure Builder Example

This script demonstrates how to create complex project directory structures
using pathlib, with proper error handling and cross-platform compatibility.
"""

from pathlib import Path
import json
from typing import Dict, List, Any


class ProjectStructureBuilder:
    """A class for building project directory structures from configuration."""

    def __init__(self, base_directory: Path):
        self.base_directory = base_directory.resolve()
        self.created_files: List[Path] = []
        self.created_directories: List[Path] = []

    def create_directory_structure(self, structure: Dict[str, Any]) -> None:
        """Create a directory structure from a nested dictionary."""
        self._create_structure_recursive(self.base_directory, structure)

    def _create_structure_recursive(
        self, current_path: Path, structure: Dict[str, Any]
    ) -> None:
        """Recursively create directory structure."""
        for name, content in structure.items():
            item_path = current_path / name

            if isinstance(content, dict):
                item_path.mkdir(parents=True, exist_ok=True)
                self.created_directories.append(item_path)
                self._create_structure_recursive(item_path, content)

            elif isinstance(content, str):
                item_path.parent.mkdir(parents=True, exist_ok=True)
                item_path.write_text(content, encoding="utf-8")
                self.created_files.append(item_path)

            elif content is None:
                item_path.parent.mkdir(parents=True, exist_ok=True)
                item_path.touch()
                self.created_files.append(item_path)

    def create_from_json_config(self, config_file: Path) -> None:
        """Create project structure from a JSON configuration file."""
        with config_file.open(encoding="utf-8") as f:
            config = json.load(f)

        if "structure" in config:
            self.create_directory_structure(config["structure"])

    def get_summary(self) -> Dict[str, int]:
        """Get a summary of created items."""
        return {
            "directories": len(self.created_directories),
            "files": len(self.created_files),
            "total": len(self.created_directories) + len(self.created_files),
        }

    def list_created_items(self) -> None:
        """Print a list of all created directories and files."""
        print("Created directories:")
        for directory in sorted(self.created_directories):
            print(f"  {directory.relative_to(self.base_directory)}/")

        print("\nCreated files:")
        for file in sorted(self.created_files):
            print(f"  {file.relative_to(self.base_directory)}")


def create_python_project_structure() -> Dict[str, Any]:
    """Create a standard Python project structure."""
    return {
        "src": {
            "myproject": {
                "__init__.py": "",
                "main.py": '''#!/usr/bin/env python3
"""Main module for myproject."""

def main():
    print("Hello from myproject!")

if __name__ == "__main__":
    main()
''',
            }
        },
        "setup.cfg": """[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,build,dist

[tool:pytest]
testpaths = tests

[tool:black]
line-length = 88
target-version = ['py38']
""",
        "README.md": "# My Python Project\n",
    }


def create_web_project_structure() -> Dict[str, Any]:
    """Create a standard web project structure."""
    return {
        "public": {
            "index.html": "<!DOCTYPE html><html><body>Hello</body></html>",
            "images": {
                "logo.png": None,
            },
        },
        "src": {
            "server.py": "print('Web server')",
        },
        "requirements.txt": "Flask\npytest\n",
    }


def main() -> None:
    print("Project Structure Builder Demonstration")
    print("=" * 45)

    python_project_dir = Path("demo_python_project")
    python_builder = ProjectStructureBuilder(python_project_dir)
    python_builder.create_directory_structure(create_python_project_structure())

    print(f"Created Python project in: {python_project_dir}")
    print(python_builder.get_summary())

    web_project_dir = Path("demo_web_project")
    web_builder = ProjectStructureBuilder(web_project_dir)
    web_builder.create_directory_structure(create_web_project_structure())

    print(f"Created Web project in: {web_project_dir}")
    print(web_builder.get_summary())

    print("\nPython Project Contents:")
    python_builder.list_created_items()

    print("\nWeb Project Contents:")
    web_builder.list_created_items()


if __name__ == "__main__":
    main()
