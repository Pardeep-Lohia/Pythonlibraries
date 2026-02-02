# Path Objects Overview

## Introduction to Path Objects in pathlib

Path objects are the fundamental building blocks of the `pathlib` library. They represent filesystem paths as immutable objects, providing a more intuitive and powerful way to handle file and directory paths compared to traditional string-based approaches.

## Core Characteristics of Path Objects

### Immutability
Path objects cannot be modified after creation. All operations that appear to modify a path actually return a new Path object.

```python
from pathlib import Path

original = Path('/home/user/file.txt')
modified = original.with_suffix('.bak')  # Creates new Path object

print(original)   # PosixPath('/home/user/file.txt')
print(modified)   # PosixPath('/home/user/file.bak')
```

### Cross-Platform Compatibility
Path objects automatically handle platform-specific path conventions:

- **Unix-like systems** (Linux, macOS): Use forward slashes `/`
- **Windows**: Use backslashes `\` and support drive letters

```python
# Same code works on all platforms
from pathlib import Path

path = Path('folder') / 'subfolder' / 'file.txt'
print(path)  # Automatically uses correct separator
```

### Object-Oriented Design
Paths are objects with methods and properties, not just strings:

```python
path = Path('/home/user/documents/report.pdf')

# Properties
print(path.name)      # 'report.pdf'
print(path.parent)    # PosixPath('/home/user/documents')
print(path.suffix)    # '.pdf'

# Methods
print(path.exists())  # Check if path exists
print(path.is_file()) # Check if it's a file
```

## Path Object Hierarchy

### PurePath Classes
Abstract base classes for path operations without filesystem access:

- **PurePath**: Base class for all path objects
- **PurePosixPath**: POSIX-style paths (Unix-like systems)
- **PureWindowsPath**: Windows-style paths

### Concrete Path Classes
Classes that interact with the filesystem:

- **Path**: Base class for concrete paths
- **PosixPath**: POSIX filesystem paths
- **WindowsPath**: Windows filesystem paths

```python
from pathlib import PurePath, Path

# Pure paths (no filesystem access)
pure_path = PurePath('/home/user/file.txt')

# Concrete paths (filesystem operations available)
concrete_path = Path('/home/user/file.txt')

print(type(pure_path))     # <class 'pathlib.PurePosixPath'>
print(type(concrete_path)) # <class 'pathlib.PosixPath'>
```

## Creating Path Objects

### From Strings
```python
from pathlib import Path

# Direct string conversion
path1 = Path('/home/user/file.txt')
path2 = Path('relative/path/file.txt')
path3 = Path('C:\\Windows\\System32')  # Windows path
```

### From Multiple Components
```python
# Join multiple path components
path = Path('home', 'user', 'documents', 'file.txt')
print(path)  # PosixPath('home/user/documents/file.txt')
```

### Special Constructors
```python
# Current working directory
cwd = Path.cwd()

# User's home directory
home = Path.home()

# Current script directory
script_dir = Path(__file__).parent
```

### Path Joining with `/` Operator
```python
base = Path('/home/user')
documents = base / 'Documents'
file_path = documents / 'report.pdf'

print(file_path)  # PosixPath('/home/user/Documents/report.pdf')
```

## Path Properties and Components

### Basic Path Components
```python
path = Path('/home/user/documents/report.pdf')

print(f"Full path: {path}")
print(f"Name: {path.name}")           # 'report.pdf'
print(f"Stem: {path.stem}")           # 'report'
print(f"Suffix: {path.suffix}")       # '.pdf'
print(f"Suffixes: {path.suffixes}")   # ['.pdf']
print(f"Parent: {path.parent}")       # PosixPath('/home/user/documents')
print(f"Parts: {path.parts}")         # ('/', 'home', 'user', 'documents', 'report.pdf')
```

### Path Type Information
```python
print(f"Is absolute: {path.is_absolute()}")  # True
print(f"Is relative: {path.is_relative_to(Path('/home/user'))}")  # True
```

## Path Manipulation Methods

### Changing Path Components
```python
original = Path('/home/user/file.txt')

# Change name
renamed = original.with_name('new_file.txt')
print(renamed)  # PosixPath('/home/user/new_file.txt')

# Change suffix
backup = original.with_suffix('.bak')
print(backup)  # PosixPath('/home/user/file.bak')

# Change to different suffix
pdf_version = original.with_suffix('.pdf')
print(pdf_version)  # PosixPath('/home/user/file.pdf')
```

### Path Resolution
```python
# Resolve relative paths and symlinks
relative = Path('../config/settings.ini')
absolute = relative.resolve()

# Get relative path between paths
base = Path('/home/user/projects')
full = Path('/home/user/projects/myapp/src/main.py')
relative_path = full.relative_to(base)
print(relative_path)  # PosixPath('myapp/src/main.py')
```

## Filesystem Operations

### Existence and Type Checking
```python
path = Path('/home/user/file.txt')

print(f"Exists: {path.exists()}")
print(f"Is file: {path.is_file()}")
print(f"Is directory: {path.is_dir()}")
print(f"Is symlink: {path.is_symlink()}")
```

### File Content Operations
```python
# Read and write text
path.write_text('Hello, World!', encoding='utf-8')
content = path.read_text(encoding='utf-8')

# Read and write bytes
binary_data = path.read_bytes()
path.write_bytes(b'Binary data')
```

### Directory Operations
```python
# Create directory
new_dir = Path('/tmp/new_directory')
new_dir.mkdir(parents=True, exist_ok=True)

# List directory contents
for item in new_dir.iterdir():
    print(f"{'File' if item.is_file() else 'Dir'}: {item.name}")

# Recursive iteration
for py_file in Path('.').rglob('*.py'):
    print(f"Python file: {py_file}")
```

### File System Modification
```python
# Rename/move
old_path = Path('old_name.txt')
new_path = old_path.with_name('new_name.txt')
old_path.rename(new_path)

# Create empty file
Path('empty.txt').touch()

# Delete
Path('temp.txt').unlink()  # Delete file
Path('temp_dir').rmdir()   # Delete empty directory
```

## Pattern Matching (Globbing)

### Finding Files with Patterns
```python
project = Path('/myproject')

# Find all Python files in current directory
py_files = list(project.glob('*.py'))

# Find all Python files recursively
all_py_files = list(project.rglob('*.py'))

# Find all text files
text_files = list(project.rglob('*.txt'))
```

## Path Comparison and Sorting

### Comparison Operations
```python
path1 = Path('/home/user/file1.txt')
path2 = Path('/home/user/file2.txt')
path3 = Path('/home/user/file1.txt')

print(path1 == path3)  # True
print(path1 < path2)   # True (lexicographical comparison)

# Sorting paths
paths = [Path('c.txt'), Path('a.txt'), Path('b.txt')]
paths.sort()
print(paths)  # [PosixPath('a.txt'), PosixPath('b.txt'), PosixPath('c.txt')]
```

## Advanced Path Operations

### Path Arithmetic
```python
# Path joining with /
path = Path('/home') / 'user' / 'file.txt'

# Path subtraction (relative_to)
base = Path('/home/user')
full = Path('/home/user/documents/file.txt')
relative = full.relative_to(base)  # PosixPath('documents/file.txt')
```

### Path Normalization
```python
# PurePath automatically normalizes paths
path = PurePath('/home/user/../user/file.txt')
print(path)  # PurePosixPath('/home/user/../user/file.txt')
# Note: PurePath doesn't resolve .., only concrete Path does

# Concrete Path resolution
concrete_path = Path('/home/user/../user/file.txt')
resolved = concrete_path.resolve()
print(resolved)  # PosixPath('/home/user/file.txt')
```

## Error Handling

### Safe Path Operations
```python
def safe_read_file(file_path: Path) -> str:
    try:
        if not file_path.exists():
            return "File does not exist"
        return file_path.read_text(encoding='utf-8')
    except PermissionError:
        return "Permission denied"
    except UnicodeDecodeError:
        return "Invalid encoding"

result = safe_read_file(Path('config.txt'))
```

## Integration with Other Libraries

### Compatibility with Standard Library
Path objects implement the `__fspath__` protocol, making them compatible with functions expecting strings:

```python
import os
from pathlib import Path

path = Path('file.txt')

# Works with os functions
os.path.exists(path)  # Path automatically converts to string

# Works with open()
with open(path, 'r') as f:
    content = f.read()
```

### Working with shutil
```python
import shutil
from pathlib import Path

src = Path('source.txt')
dst = Path('destination.txt')

shutil.copy(src, dst)  # shutil accepts Path objects
```

## Best Practices

### When to Use Path Objects
- **Always prefer Path objects** over string paths in new code
- Use Path objects for file system operations
- Convert to strings only when interfacing with legacy code

### Path Object Patterns
```python
# Good: Use Path objects throughout
def process_file(file_path: Path) -> None:
    if file_path.exists() and file_path.is_file():
        content = file_path.read_text()
        # Process content...

# Avoid: Mixing strings and Paths
def bad_example(file_path_str: str) -> None:
    path = Path(file_path_str)  # Convert to Path immediately
    # Then use Path methods
```

## Summary

Path objects provide a powerful, object-oriented interface for filesystem path handling. Key benefits include:

- **Immutability**: Safe sharing and modification without side effects
- **Cross-platform**: Automatic handling of OS differences
- **Rich API**: Comprehensive methods for all path operations
- **Type safety**: Better error prevention and validation
- **Integration**: Seamless compatibility with existing Python code

By using Path objects consistently, developers can write more reliable, readable, and maintainable filesystem code that works across all platforms where Python runs.
