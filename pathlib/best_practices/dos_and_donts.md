# Do's and Don'ts of pathlib

## Introduction

`pathlib` provides a powerful, object-oriented interface for filesystem operations, but like any tool, it has best practices that should be followed. This guide outlines the essential do's and don'ts for effective `pathlib` usage.

## Do's

### ✅ Do Use Path Objects Consistently

**Do this:**
```python
from pathlib import Path

def process_file(file_path: Path) -> None:
    """Process a file using Path objects throughout."""
    if file_path.exists():
        content = file_path.read_text()
        backup = file_path.with_suffix('.bak')
        backup.write_text(content)

# Usage
file_path = Path('data.txt')
process_file(file_path)
```

**Why:** Path objects provide type safety, cross-platform compatibility, and a rich API.

### ✅ Do Use the `/` Operator for Path Joining

**Do this:**
```python
# Use the / operator
config_path = Path.home() / '.config' / 'myapp' / 'settings.ini'
```

**Don't do this:**
```python
# Avoid string concatenation
config_path = str(Path.home()) + '/.config/myapp/settings.ini'
```

**Why:** The `/` operator is overloaded for intuitive path joining and handles platform differences automatically.

### ✅ Do Handle Exceptions Appropriately

**Do this:**
```python
def safe_read_file(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return "File not found"
    except PermissionError:
        return "Permission denied"
    except UnicodeDecodeError:
        return "Invalid encoding"
```

**Why:** Filesystem operations can fail for various reasons; handle them gracefully.

### ✅ Do Use Path Methods for Path Manipulation

**Do this:**
```python
original = Path('/home/user/file.txt')

# Use Path methods
backup = original.with_suffix('.bak')
parent_dir = original.parent
filename = original.name
```

**Don't do this:**
```python
# Avoid string operations
import os
backup = os.path.splitext('/home/user/file.txt')[0] + '.bak'
parent_dir = os.path.dirname('/home/user/file.txt')
filename = os.path.basename('/home/user/file.txt')
```

**Why:** Path methods are more readable and less error-prone.

### ✅ Do Prefer Absolute Paths When Possible

**Do this:**
```python
# Resolve to absolute path
config_file = Path('config.ini').resolve()
data_dir = Path('../data').resolve()
```

**Why:** Absolute paths eliminate ambiguity and make operations more predictable.

### ✅ Do Use `iterdir()` for Directory Iteration

**Do this:**
```python
def list_files(directory: Path) -> None:
    for item in directory.iterdir():
        if item.is_file():
            print(f"File: {item.name}")
        elif item.is_dir():
            print(f"Directory: {item.name}")
```

**Why:** `iterdir()` is efficient and provides Path objects directly.

### ✅ Do Use `glob()` and `rglob()` for Pattern Matching

**Do this:**
```python
# Find all Python files
py_files = list(Path('.').rglob('*.py'))

# Find all config files
config_files = list(Path('.').glob('*.ini'))
```

**Why:** Built-in globbing is more efficient than manual filtering.

### ✅ Do Check File Existence Before Operations

**Do this:**
```python
file_path = Path('important.txt')
if file_path.exists():
    content = file_path.read_text()
    # Process content
```

**Why:** Prevents exceptions and makes code more robust.

### ✅ Do Use `parents=True` with `mkdir()`

**Do this:**
```python
# Create nested directories
output_dir = Path('results') / '2023' / 'reports'
output_dir.mkdir(parents=True, exist_ok=True)
```

**Why:** Ensures parent directories are created automatically.

### ✅ Do Use Type Hints with Path Objects

**Do this:**
```python
from pathlib import Path
from typing import List

def find_files(directory: Path, pattern: str) -> List[Path]:
    return list(directory.rglob(pattern))
```

**Why:** Improves code readability and enables static type checking.

## Don'ts

### ❌ Don't Mix Path Objects and Strings

**Don't do this:**
```python
# Mixing Path and string
path = Path('/home/user')
full_path = str(path) + '/file.txt'  # Bad!

# Inconsistent usage
def bad_function(file_path):
    if isinstance(file_path, str):
        # Handle string
        pass
    else:
        # Handle Path
        pass
```

**Do this instead:**
```python
# Use Path objects consistently
path = Path('/home/user') / 'file.txt'
```

**Why:** Mixing types leads to confusion and bugs.

### ❌ Don't Use `os.path` Functions with Path Objects

**Don't do this:**
```python
import os
from pathlib import Path

path = Path('file.txt')
# Don't do this
dirname = os.path.dirname(str(path))  # Unnecessary conversion
```

**Do this instead:**
```python
path = Path('file.txt')
dirname = path.parent
```

**Why:** Path objects have equivalent methods that are more convenient.

### ❌ Don't Hardcode Path Separators

**Don't do this:**
```python
# Platform-specific code
import os

if os.name == 'nt':
    path = 'C:\\Users\\user\\file.txt'
else:
    path = '/home/user/file.txt'
```

**Do this instead:**
```python
# Cross-platform code
from pathlib import Path

path = Path.home() / 'file.txt'
```

**Why:** `pathlib` handles platform differences automatically.

### ❌ Don't Ignore `exist_ok` Parameter

**Don't do this:**
```python
# May raise FileExistsError
Path('existing_dir').mkdir()
```

**Do this instead:**
```python
# Safe directory creation
Path('existing_dir').mkdir(exist_ok=True)
```

**Why:** `exist_ok=True` prevents exceptions when directories already exist.

### ❌ Don't Use Path Objects for Non-Path Operations

**Don't do this:**
```python
# Using Path for string operations
path = Path('file.txt')
name = str(path).replace('file', 'document')  # Bad!
```

**Do this instead:**
```python
# Use Path methods
path = Path('file.txt')
name = path.with_stem('document')
```

**Why:** Path objects have methods for common manipulations.

### ❌ Don't Forget to Handle Symlinks

**Don't do this:**
```python
# May not work as expected with symlinks
if Path('link.txt').exists():
    content = Path('link.txt').read_text()
```

**Do this instead:**
```python
# Handle symlinks explicitly
link_path = Path('link.txt')
if link_path.exists():
    if link_path.is_symlink():
        target = link_path.resolve()
        print(f"Symlink points to: {target}")
    content = link_path.read_text()
```

**Why:** Symlinks can behave differently than regular files.

### ❌ Don't Use `read_text()`/`write_text()` for Large Files

**Don't do this:**
```python
# Loads entire file into memory
large_file = Path('huge_file.dat')
content = large_file.read_text()  # Bad for large files!
```

**Do this instead:**
```python
# Process large files line by line
large_file = Path('huge_file.dat')
with open(large_file, 'r', encoding='utf-8') as f:
    for line in f:
        # Process line
        pass
```

**Why:** Large files can cause memory issues.

### ❌ Don't Modify Paths In-Place

**Don't do this:**
```python
# Path objects are immutable
path = Path('/home/user/file.txt')
path = path + '_backup'  # This doesn't work as expected
```

**Do this instead:**
```python
# Create new Path objects
path = Path('/home/user/file.txt')
backup_path = path.with_stem(path.stem + '_backup')
```

**Why:** Path objects are immutable; operations return new objects.

### ❌ Don't Use Relative Paths for Critical Operations

**Don't do this:**
```python
# May not work as expected
config_path = Path('../config/settings.ini')
if config_path.exists():
    # This might check the wrong file
    pass
```

**Do this instead:**
```python
# Resolve to absolute path
config_path = Path('../config/settings.ini').resolve()
if config_path.exists():
    # Now we're sure about the path
    pass
```

**Why:** Relative paths depend on the current working directory.

### ❌ Don't Ignore Encoding Parameters

**Don't do this:**
```python
# May fail with Unicode files
content = Path('file.txt').read_text()  # Uses default encoding
```

**Do this instead:**
```python
# Specify encoding explicitly
content = Path('file.txt').read_text(encoding='utf-8')
```

**Why:** Different systems may have different default encodings.

## Advanced Do's and Don'ts

### ✅ Do Use Context Managers for Complex Operations

**Do this:**
```python
from contextlib import contextmanager

@contextmanager
def temp_file_operation(file_path: Path):
    """Context manager for safe file operations."""
    backup = file_path.with_suffix('.bak')
    if file_path.exists():
        # Create backup
        backup.write_bytes(file_path.read_bytes())

    try:
        yield file_path
    finally:
        # Restore backup if something went wrong
        if backup.exists():
            file_path.write_bytes(backup.read_bytes())
            backup.unlink()
```

### ✅ Do Implement Path Validation

**Do this:**
```python
def validate_path(path: Path, must_exist: bool = True) -> bool:
    """Validate a path for common issues."""
    if must_exist and not path.exists():
        return False

    # Check for invalid characters (basic validation)
    invalid_chars = '<>:"|?*'
    if any(char in str(path) for char in invalid_chars):
        return False

    # Check path length (Windows has limits)
    if len(str(path)) > 260:  # Windows MAX_PATH
        return False

    return True
```

### ❌ Don't Create Deeply Nested Directory Structures Without Care

**Don't do this:**
```python
# May create very deep directory structures
user_input = input("Enter path: ")
Path(user_input).mkdir(parents=True)  # Potentially dangerous
```

**Do this instead:**
```python
# Validate input
user_input = input("Enter path: ")
path = Path(user_input)

# Basic validation
if len(path.parts) > 10:  # Arbitrary limit
    raise ValueError("Path too deep")

path.mkdir(parents=True, exist_ok=True)
```

**Why:** Deep directory structures can cause issues and may indicate malformed input.

## Summary

Following these do's and don'ts will help you write more reliable, maintainable, and cross-platform code with `pathlib`:

**Key Principles:**
- Use Path objects consistently throughout your code
- Leverage the rich Path API instead of string operations
- Handle exceptions appropriately
- Prefer absolute paths for critical operations
- Always specify encodings for text operations
- Use `exist_ok=True` when creating directories

**Remember:** `pathlib` is designed to make filesystem operations more intuitive and less error-prone. When in doubt, prefer Path methods over string manipulation or `os.path` functions.
