#!/usr/bin/env python3
"""
Project Structure Generator Example

This script demonstrates how to create complex project structures
using the `os` module, including templates for different project types.
"""

import os
import os.path
import json
from typing import Dict, List, Any
import argparse


class ProjectGenerator:
    """Generate project structures with templates."""

    def __init__(self, base_dir: str = "."):
        self.base_dir = os.path.abspath(base_dir)

    def create_project(self, project_type: str, project_name: str,
                      structure: Dict[str, Any] = None) -> str:
        """
        Create a project with the specified structure.

        Args:
            project_type (str): Type of project (python, web, data_science, etc.)
            project_name (str): Name of the project
            structure (dict): Custom structure (optional)

        Returns:
            str: Path to created project
        """
        if structure is None:
            structure = self._get_template(project_type)

        project_path = os.path.join(self.base_dir, project_name)

        # Create the structure
        self._create_structure(project_path, structure)

        print(f"Created {project_type} project: {project_name}")
        return project_path

    def _get_template(self, project_type: str) -> Dict[str, Any]:
        """Get template structure for project type."""
        templates = {
            'python': {
                'src': {
                    '__init__.py': '',
                    'main.py': 'def main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()',
                    'utils.py': 'def helper():\n    pass'
                },
                'tests': {
                    '__init__.py': '',
                    'test_main.py': 'import unittest\n\nclass TestMain(unittest.TestCase):\n    def test_example(self):\n        self.assertTrue(True)'
                },
                'docs': {
                    'README.md': '# Project Name\n\nDescription of the project.',
                    'CHANGELOG.md': '# Changelog\n\n## [Unreleased]'
                },
                'requirements.txt': 'requests==2.25.1\npytest==6.2.4',
                'setup.py': 'from setuptools import setup\n\nsetup(\n    name="project_name",\n    version="0.1.0",\n    packages=["src"],\n)',
                '.gitignore': '__pycache__/\n*.pyc\n*.pyo\n*.pyd\n.Python\nenv/\nvenv/',
                'README.md': '# Project Name\n\nA Python project.\n\n## Installation\n\n```bash\npip install -r requirements.txt\n```\n\n## Usage\n\n```python\nfrom src.main import main\nmain()\n```'
            },

            'web': {
                'public': {
                    'index.html': '<!DOCTYPE html>\n<html>\n<head>\n    <title>Web App</title>\n</head>\n<body>\n    <h1>Hello, World!</h1>\n</body>\n</html>',
                    'css': {
                        'style.css': 'body {\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 20px;\n}'
                    },
                    'js': {
                        'app.js': 'console.log("Hello, World!");'
                    }
                },
                'src': {
                    'server.py': 'from flask import Flask\n\napp = Flask(__name__)\n\n@app.route("/")\ndef home():\n    return "Hello, World!"\n\nif __name__ == "__main__":\n    app.run(debug=True)',
                    'static': {},
                    'templates': {
                        'base.html': '<!DOCTYPE html>\n<html>\n<body>\n    {% block content %}{% endblock %}\n</body>\n</html>'
                    }
                },
                'requirements.txt': 'Flask==2.0.1\nJinja2==3.0.1',
                '.gitignore': '__pycache__/\n*.pyc\nenv/\n.DS_Store',
                'README.md': '# Web Application\n\nA web application built with Flask.\n\n## Setup\n\n```bash\npip install -r requirements.txt\npython src/server.py\n```'
            },

            'data_science': {
                'notebooks': {
                    'exploratory_analysis.ipynb': '',
                    'model_training.ipynb': ''
                },
                'src': {
                    '__init__.py': '',
                    'data_loader.py': 'import pandas as pd\n\ndef load_data(filepath):\n    return pd.read_csv(filepath)',
                    'model.py': 'from sklearn.linear_model import LinearRegression\n\nclass Model:\n    def __init__(self):\n        self.model = LinearRegression()\n\n    def train(self, X, y):\n        self.model.fit(X, y)\n        return self.model',
                    'utils.py': 'import numpy as np\n\ndef preprocess_data(data):\n    # Preprocessing logic here\n    return data'
                },
                'data': {
                    'raw': {},
                    'processed': {},
                    'models': {}
                },
                'tests': {
                    '__init__.py': '',
                    'test_model.py': 'import unittest\n\nclass TestModel(unittest.TestCase):\n    def test_model_creation(self):\n        from src.model import Model\n        model = Model()\n        self.assertIsNotNone(model)'
                },
                'requirements.txt': 'pandas==1.3.3\nnumpy==1.21.2\nscikit-learn==0.24.2\njupyter==1.0.0\nmatplotlib==3.4.3',
                '.gitignore': '__pycache__/\n*.pyc\ndata/raw/*\ndata/processed/*\nmodels/*\n.ipynb_checkpoints/',
                'README.md': '# Data Science Project\n\nA data science project template.\n\n## Setup\n\n```bash\npip install -r requirements.txt\njupyter notebook\n```',
                'config.json': '{\n    "data_path": "data/",\n    "model_path": "data/models/",\n    "random_seed": 42\n}'
            },

            'api': {
                'app': {
                    '__init__.py': '',
                    'main.py': 'from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/")\ndef read_root():\n    return {"Hello": "World"}\n\n@app.get("/items/{item_id}")\ndef read_item(item_id: int, q: str = None):\n    return {"item_id": item_id, "q": q}',
                    'models.py': 'from pydantic import BaseModel\n\nclass Item(BaseModel):\n    name: str\n    price: float\n    is_offer: bool = None',
                    'routes': {
                        '__init__.py': '',
                        'items.py': 'from fastapi import APIRouter, HTTPException\nfrom app.models import Item\n\nrouter = APIRouter()\n\n@router.get("/")\ndef get_items():\n    return {"items": []}\n\n@router.post("/")\ndef create_item(item: Item):\n    return item'
                    }
                },
                'tests': {
                    '__init__.py': '',
                    'test_main.py': 'from fastapi.testclient import TestClient\nfrom app.main import app\n\nclient = TestClient(app)\n\ndef test_read_main():\n    response = client.get("/")\n    assert response.status_code == 200\n    assert response.json() == {"Hello": "World"}'
                },
                'requirements.txt': 'fastapi==0.68.1\nuvicorn==0.15.0\npydantic==1.8.2',
                '.gitignore': '__pycache__/\n*.pyc\n__pycache__/',
                'README.md': '# API Project\n\nA FastAPI-based REST API.\n\n## Setup\n\n```bash\npip install -r requirements.txt\nuvicorn app.main:app --reload\n```',
                'Dockerfile': 'FROM python:3.9-slim\n\nWORKDIR /app\n\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\n\nCOPY . .\n\nCMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]'
            }
        }

        return templates.get(project_type, {})

    def _create_structure(self, base_path: str, structure: Dict[str, Any]) -> None:
        """Recursively create directory structure."""
        for name, content in structure.items():
            path = os.path.join(base_path, name)

            if isinstance(content, dict):
                # It's a directory
                os.makedirs(path, exist_ok=True)
                self._create_structure(path, content)
            else:
                # It's a file
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)

    def list_templates(self) -> List[str]:
        """List available project templates."""
        return ['python', 'web', 'data_science', 'api']

    def save_template(self, name: str, structure: Dict[str, Any]) -> None:
        """Save a custom template."""
        template_path = os.path.join(self.base_dir, 'templates', f'{name}.json')
        os.makedirs(os.path.dirname(template_path), exist_ok=True)

        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2)

    def load_template(self, name: str) -> Dict[str, Any]:
        """Load a custom template."""
        template_path = os.path.join(self.base_dir, 'templates', f'{name}.json')

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template {name} not found")

        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def main():
    """Command line interface for project generation."""
    parser = argparse.ArgumentParser(description='Generate project structures')
    parser.add_argument('project_name', help='Name of the project')
    parser.add_argument('--type', '-t', default='python',
                       choices=['python', 'web', 'data_science', 'api'],
                       help='Type of project to create')
    parser.add_argument('--output', '-o', default='.',
                       help='Output directory')

    args = parser.parse_args()

    generator = ProjectGenerator(args.output)
    project_path = generator.create_project(args.type, args.project_name)

    print(f"\nProject created successfully at: {project_path}")
    print("Available templates:", ', '.join(generator.list_templates()))


if __name__ == "__main__":
    main()
