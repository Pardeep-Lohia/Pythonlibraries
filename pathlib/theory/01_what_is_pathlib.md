# What is pathlib?

## Introduction
`pathlib` is a Python standard library module introduced in Python 3.4 that provides an object-oriented approach to handling filesystem paths. Unlike traditional string-based path manipulation using modules like `os.path`, `pathlib` treats paths as objects, making code more readable, maintainable, and less error-prone.

## Path Objects: The Core Concept
At the heart of `pathlib` are **Path objects**. These are immutable objects that represent filesystem paths. Instead of working with strings like `/home/user/documents/file.txt`, you work with Path instances that encapsulate the path logic.

### Basic Example
```python
from pathlib import Path

# Create a Path object
path = Path('/home/user/documents/file.txt')
print(path)  # Output: /home/user/documents/file.txt
```

## Key Characteristics
- **Object-Oriented**: Paths are objects with methods and properties
- **Immutable**: Path objects cannot be modified in-place
- **Cross-Platform**: Automatically handles OS-specific path separators
- **Intuitive**: Method names are descriptive and easy to understand

## Path vs String: A Simple Analogy
Think of a string path as a raw address written on paper:
```
"/home/user/documents/file.txt"
```

A Path object is like a structured address card:
```
Address Card:
- Root: /
- Parts: ['home', 'user', 'documents', 'file.txt']
- Name: file.txt
- Suffix: .txt
- Parent: /home/user/documents
```

## Why Objects Matter
With objects, you can:
- Access path components easily: `path.name`, `path.parent`
- Perform operations naturally: `path / 'subdir' / 'file.txt'`
- Chain methods: `path.with_suffix('.bak').rename('new_name.txt')`

## Getting Started
To use `pathlib`, simply import the `Path` class:
```python
from pathlib import Path
```

Then create Path objects and start exploring the filesystem in a more Pythonic way!
