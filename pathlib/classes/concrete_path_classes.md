# Concrete Path Classes in pathlib

## Overview

Concrete path classes in `pathlib` are the classes that interact with the actual filesystem. Unlike pure path classes that only handle path manipulation without filesystem access, concrete classes provide methods for reading, writing, and querying the filesystem.

## Main Concrete Classes

### Path Class

The `Path` class is the main entry point for concrete path operations. It's actually an alias for the appropriate platform-specific class:

```python
from pathlib import Path

# On Unix-like systems (Linux, macOS)
# Path is an alias for PosixPath

# On Windows
# Path is an alias for WindowsPath

# Usage is the same regardless of platform
path = Path('/home/user/file.txt')  # Works on both Unix and Windows
```

### Platform-Specific Classes

#### PosixPath

Used on Unix-like systems (Linux, macOS, BSD):

```python
from pathlib import PosixPath

# Explicitly create a POSIX path
path = PosixPath('/home/user/file.txt')

# All methods work the same as Path
print(path.exists())
print(path.is_file())
```

#### WindowsPath

Used on Windows systems:

```python
from pathlib import WindowsPath

# Explicitly create a Windows path
path = WindowsPath('C:\\Users\\user\\file.txt')

# Or using forward slashes (pathlib handles conversion)
path = WindowsPath('C:/Users/user/file.txt')

# Methods work identically
print(path.exists())
print(path.is_file())
```

## Key Differences from Pure Paths

### Filesystem Interaction

Concrete paths can interact with the filesystem:

```python
from pathlib import Path

# Pure paths can't do this
pure_path = PurePath('/home/user/file.txt')
# pure_path.exists()  # AttributeError

# Concrete paths can
concrete_path = Path('/home/user/file.txt')
print(concrete_path.exists())  # True or False
print(concrete_path.is_file())  # True or False
```

### Path Resolution

Concrete paths resolve relative paths and symlinks:

```python
# Relative path resolution
relative = Path('../config/settings.ini')
absolute = relative.resolve()
print(absolute)  # /full/absolute/path/to/config/settings.ini

# Symlink resolution
symlink = Path('/home/user/docs_link')
real_path = symlink.resolve()
print(real_path)  # Actual target of the symlink
```

### User Directory Expansion

Concrete paths can expand user home directory:

```python
# Expand ~ to home directory
config_path = Path('~/.config/app/settings.ini').expanduser()
print(config_path)  # /home/user/.config/app/settings.ini
```

## Common Methods

### File Operations

```python
file_path = Path('data.txt')

# Read and write text
content = file_path.read_text(encoding='utf-8')
file_path.write_text('New content', encoding='utf-8')

# Read and write bytes
data = file_path.read_bytes()
file_path.write_bytes(b'Binary data')

# Check file properties
print(f"Size: {file_path.stat().st_size} bytes")
print(f"Is readable: {file_path.stat().st_mode & 0o400 != 0}")
```

### Directory Operations

```python
dir_path = Path('/tmp/new_dir')

# Create directory
dir_path.mkdir(parents=True, exist_ok=True)

# List contents
for item in dir_path.iterdir():
    print(f"{'File' if item.is_file() else 'Directory'}: {item.name}")

# Recursive operations
for py_file in Path('.').rglob('*.py'):
    print(f"Python file: {py_file}")
```

### File System Modifications

```python
# Rename/move
old_path = Path('old_name.txt')
new_path = old_path.with_name('new_name.txt')
old_path.rename(new_path)

# Create empty file
Path('empty.txt').touch()

# Delete files
Path('temp.txt').unlink(missing_ok=True)

# Delete empty directory
Path('empty_dir').rmdir()
```

## Pattern Matching (Glob)

```python
project = Path('/myproject')

# Find Python files
py_files = list(project.glob('*.py'))
all_py_files = list(project.rglob('*.py'))

# Find by multiple patterns
code_files = []
for pattern in ['*.py', '*.js', '*.html']:
    code_files.extend(project.rglob(pattern))
```

## Path Manipulation

### Building Paths

```python
# Using / operator
home = Path.home()
config = home / '.config' / 'app' / 'settings.ini'

# Using joinpath
config2 = home.joinpath('.config', 'app', 'settings.ini')

assert config == config2
```

### Path Components

```python
path = Path('/home/user/documents/report.pdf')

print(path.name)       # 'report.pdf'
print(path.stem)       # 'report'
print(path.suffix)     # '.pdf'
print(path.parent)     # PosixPath('/home/user/documents')
print(path.parts)      # ('/', 'home', 'user', 'documents', 'report.pdf')
```

### Path Transformations

```python
original = Path('/home/user/file.txt')

# Change name
renamed = original.with_name('new_file.txt')

# Change suffix
backup = original.with_suffix('.bak')

# Get relative path
base = Path('/home/user')
relative = original.relative_to(base)  # PosixPath('file.txt')
```

## Cross-Platform Compatibility

### Automatic Path Separation

pathlib handles path separators automatically:

```python
# On Windows
path = Path('C:/Users/user/file.txt')
print(path)  # WindowsPath('C:/Users/user/file.txt')

# On Unix
path = Path('/home/user/file.txt')
print(path)  # PosixPath('/home/user/file.txt')

# Internal representation uses forward slashes
print(str(path))  # '/home/user/file.txt' on both systems
```

### Platform-Specific Operations

```python
import os
from pathlib import Path

def get_desktop_path():
    """Get desktop path in a cross-platform way."""
    if os.name == 'nt':  # Windows
        return Path.home() / 'Desktop'
    else:  # Unix-like
        return Path.home() / 'Desktop'

desktop = get_desktop_path()
print(f"Desktop: {desktop}")
```

## Error Handling

### Safe Operations

```python
def safe_file_read(file_path: Path):
    """Safely read a file with proper error handling."""
    try:
        if not file_path.exists():
            print(f"File {file_path} does not exist")
            return None

        content = file_path.read_text(encoding='utf-8')
        return content

    except PermissionError:
        print(f"Permission denied: {file_path}")
        return None
    except UnicodeDecodeError:
        print(f"File is not valid text: {file_path}")
        return None
    except OSError as e:
        print(f"OS error reading {file_path}: {e}")
        return None

# Usage
content = safe_file_read(Path('example.txt'))
```

### Checking Before Operations

```python
def safe_delete(file_path: Path):
    """Safely delete a file."""
    if not file_path.exists():
        print(f"File {file_path} does not exist")
        return False

    if not file_path.is_file():
        print(f"{file_path} is not a file")
        return False

    try:
        file_path.unlink()
        print(f"Deleted: {file_path}")
        return True
    except PermissionError:
        print(f"Permission denied deleting: {file_path}")
        return False
    except OSError as e:
        print(f"Error deleting {file_path}: {e}")
        return False
```

## Performance Considerations

### Efficient Operations

```python
# Inefficient: Multiple stat calls
files = []
for item in Path('.').iterdir():
    if item.is_file() and item.stat().st_size > 1024:
        files.append(item)

# More efficient: Single iteration
files = [item for item in Path('.').iterdir()
         if item.is_file() and item.stat().st_size > 1024]

# Use glob for filtering
large_files = [f for f in Path('.').glob('*')
               if f.is_file() and f.stat().st_size > 1024]
```

### Caching Stat Results

```python
def get_large_files(directory: Path, min_size: int = 1024*1024):
    """Find files larger than min_size efficiently."""
    large_files = []
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            stat_info = file_path.stat()
            if stat_info.st_size > min_size:
                large_files.append((file_path, stat_info.st_size))
    return large_files

# Usage
large_files = get_large_files(Path('/home/user'), 10*1024*1024)  # 10MB
```

## Advanced Usage

### Custom Path Classes

You can subclass concrete path classes:

```python
class ProjectPath(Path):
    """Custom path class for project-specific operations."""

    def is_python_file(self):
        """Check if path points to a Python file."""
        return self.is_file() and self.suffix == '.py'

    def get_relative_to_project(self, project_root: Path):
        """Get path relative to project root."""
        try:
            return self.relative_to(project_root)
        except ValueError:
            return None

    @property
    def module_name(self):
        """Get module name for Python files."""
        if not self.is_python_file():
            return None
        return self.stem

# Usage
project_root = Path('/myproject')
file_path = ProjectPath('/myproject/src/main.py')

print(file_path.is_python_file())  # True
print(file_path.get_relative_to_project(project_root))  # src/main.py
print(file_path.module_name)  # main
```

### Context Managers for Temporary Operations

```python
from contextlib import contextmanager

@contextmanager
def temp_file_operation(file_path: Path, mode='w', **kwargs):
    """Context manager for temporary file operations."""
    temp_path = file_path.with_suffix('.tmp')

    try:
        # Create temporary file
        with temp_path.open(mode, **kwargs) as f:
            yield f

        # Atomic move to final location
        temp_path.replace(file_path)

    except Exception:
        # Clean up on error
        if temp_path.exists():
            temp_path.unlink()
        raise

# Usage
with temp_file_operation(Path('config.ini'), 'w', encoding='utf-8') as f:
    f.write('[settings]\nkey=value\n')
```

## Summary

Concrete path classes provide the filesystem interaction layer of pathlib:

- **Path**: Main concrete class (platform-specific alias)
- **PosixPath/WindowsPath**: Platform-specific implementations
- **Filesystem Operations**: Read, write, create, delete files/directories
- **Path Resolution**: Handle relative paths and symlinks
- **Cross-Platform**: Automatic handling of path separators
- **Pattern Matching**: Glob operations for finding files
- **Error Handling**: Robust operations with proper exception handling

These classes make filesystem operations in Python more intuitive, readable, and cross-platform compatible compared to traditional string-based approaches.
