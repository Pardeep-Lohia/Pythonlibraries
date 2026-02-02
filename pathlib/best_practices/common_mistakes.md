# Common Mistakes and Pitfalls in pathlib

## Overview

While pathlib provides an elegant and powerful way to handle filesystem paths, there are several common mistakes that developers make when using it. This guide covers the most frequent pitfalls and how to avoid them.

## 1. Mixing Path Objects with Strings

### The Problem
```python
from pathlib import Path

# Common mistake: mixing Path and string
base_path = Path('/home/user')
config_file = base_path + '/config.ini'  # TypeError!

# This doesn't work because Path + str is not supported
```

### The Solution
```python
# Correct ways to combine paths
base_path = Path('/home/user')

# Using / operator (recommended)
config_file = base_path / 'config.ini'

# Using joinpath()
config_file = base_path.joinpath('config.ini')

# Converting to string if needed
config_str = str(base_path / 'config.ini')
```

## 2. Forgetting Path Objects are Not Strings

### The Problem
```python
path = Path('/home/user/file.txt')

# These will fail or behave unexpectedly
if path == '/home/user/file.txt':  # False!
    print("Paths are equal")

with open(path, 'r') as f:  # This actually works, but...
    content = f.read()

# Path objects work in most string contexts, but comparison fails
```

### The Solution
```python
path = Path('/home/user/file.txt')
string_path = '/home/user/file.txt'

# Correct comparison
if str(path) == string_path:
    print("Paths are equal")

if path == Path(string_path):
    print("Paths are equal")

# Or use Path.samefile() for filesystem comparison
if path.samefile(string_path):
    print("Files are the same")
```

## 3. Not Handling Non-Existent Paths

### The Problem
```python
path = Path('/nonexistent/file.txt')

# This will raise FileNotFoundError
content = path.read_text()

# This will raise OSError
stat_info = path.stat()
```

### The Solution
```python
path = Path('/nonexistent/file.txt')

# Check existence first
if path.exists():
    content = path.read_text()
    stat_info = path.stat()
else:
    print(f"Path does not exist: {path}")

# Or use safe methods
try:
    content = path.read_text()
except FileNotFoundError:
    content = None

# For reading with default
content = path.read_text() if path.exists() else "default content"
```

## 4. Incorrect Path Resolution

### The Problem
```python
# In a script located at /home/user/project/script.py
script_dir = Path(__file__).parent

# Wrong: assumes current working directory
config_path = Path('config/settings.ini')

# This resolves relative to cwd, not script location
absolute_config = config_path.resolve()
```

### The Solution
```python
script_dir = Path(__file__).parent

# Correct: resolve relative to script directory
config_path = script_dir / 'config' / 'settings.ini'

# Or resolve explicitly
relative_config = Path('config/settings.ini')
absolute_config = (script_dir / relative_config).resolve()
```

## 5. Platform-Specific Path Issues

### The Problem
```python
# Hardcoded separators (bad)
path_str = '/home/user/file.txt'  # Unix only
path_str = 'C:\\Users\\user\\file.txt'  # Windows only

# Manual path construction
full_path = os.path.join('home', 'user', 'file.txt')  # Old way
```

### The Solution
```python
# Let pathlib handle platform differences
path = Path('home', 'user', 'file.txt')  # Cross-platform

# Or from string (pathlib handles conversion)
unix_path = Path('/home/user/file.txt')
windows_path = Path('C:/Users/user/file.txt')  # Forward slashes work on Windows

# pathlib automatically uses correct separators
print(path)  # PosixPath('home/user/file.txt') on Unix
            # WindowsPath('home\\user\\file.txt') on Windows
```

## 6. Inefficient Multiple Filesystem Calls

### The Problem
```python
# Inefficient: multiple stat calls
files = []
for item in Path('.').iterdir():
    if item.is_file() and item.stat().st_size > 1024:
        files.append(item)
```

### The Solution
```python
# More efficient: single stat call per file
files = []
for item in Path('.').iterdir():
    if item.is_file():
        stat_info = item.stat()
        if stat_info.st_size > 1024:
            files.append(item)

# Or use list comprehension
large_files = [f for f in Path('.').iterdir()
               if f.is_file() and f.stat().st_size > 1024]
```

## 7. Not Using Context Managers for File Operations

### The Problem
```python
# Risky: file might not be closed properly
path = Path('file.txt')
file_obj = path.open('w')
file_obj.write('content')
file_obj.close()  # Might not execute if exception occurs
```

### The Solution
```python
# Safe: automatic cleanup
path = Path('file.txt')
with path.open('w') as file_obj:
    file_obj.write('content')
# File automatically closed here

# Or use convenience methods
path.write_text('content')  # Even simpler
```

## 8. Incorrect Use of Glob Patterns

### The Problem
```python
# Wrong: expects exact match
files = list(Path('.').glob('*.txt'))  # Only in current directory

# Wrong: doesn't recurse
all_txt = list(Path('.').glob('**/*.txt'))  # Correct recursive

# Wrong: case sensitivity issues
readme_files = list(Path('.').glob('readme*'))  # Case sensitive
```

### The Solution
```python
# Current directory only
txt_files = list(Path('.').glob('*.txt'))

# Recursive search
all_txt_files = list(Path('.').rglob('*.txt'))

# Case-insensitive search (platform dependent)
import os
if os.name == 'nt':  # Windows is case-insensitive
    readme_files = list(Path('.').glob('readme*'))
else:  # Unix-like systems
    readme_files = []
    for pattern in ['readme*', 'README*', 'Readme*']:
        readme_files.extend(Path('.').glob(pattern))
```

## 9. Path Object Mutability Confusion

### The Problem
```python
path = Path('/home/user/file.txt')

# Path objects are immutable!
new_path = path.with_name('new.txt')  # Creates new Path object
print(path)  # Still '/home/user/file.txt'
print(new_path)  # '/home/user/new.txt'
```

### The Solution
```python
path = Path('/home/user/file.txt')

# Correct: assign the result
renamed_path = path.with_name('new.txt')

# Or chain operations
final_path = (path.parent / 'backup' / path.name).with_suffix('.bak')
```

## 10. Ignoring Encoding Issues

### The Problem
```python
# Wrong: assumes UTF-8
content = path.read_text()  # Might fail with UnicodeDecodeError

# Wrong: no encoding specified for write
path.write_text('content')  # Uses default, might not be UTF-8
```

### The Solution
```python
# Explicit encoding
content = path.read_text(encoding='utf-8')

# Handle encoding errors
try:
    content = path.read_text(encoding='utf-8')
except UnicodeDecodeError:
    print("File is not valid UTF-8")

# Write with explicit encoding
path.write_text('content', encoding='utf-8')
```

## 11. Not Handling Permissions Correctly

### The Problem
```python
# Wrong: assumes permissions allow operation
path.write_text('content')  # Might raise PermissionError

# Wrong: ignores permission errors
try:
    path.unlink()
except:
    pass  # Too broad exception handling
```

### The Solution
```python
# Check permissions before operation
if path.exists() and os.access(path, os.W_OK):
    path.write_text('content')
else:
    print("Cannot write to file")

# Specific exception handling
try:
    path.unlink()
except PermissionError:
    print("Permission denied")
except FileNotFoundError:
    print("File already deleted")
except OSError as e:
    print(f"OS error: {e}")
```

## 12. Directory Operations Without Existence Checks

### The Problem
```python
# Wrong: assumes directory exists
for item in Path('/nonexistent').iterdir():
    print(item)
# Raises FileNotFoundError
```

### The Solution
```python
def safe_iterdir(directory: Path):
    """Safely iterate directory contents."""
    if not directory.exists():
        print(f"Directory does not exist: {directory}")
        return []
    if not directory.is_dir():
        print(f"Not a directory: {directory}")
        return []

    try:
        return list(directory.iterdir())
    except PermissionError:
        print(f"Permission denied: {directory}")
        return []
    except OSError as e:
        print(f"OS error: {e}")
        return []

# Usage
items = safe_iterdir(Path('/some/dir'))
```

## 13. Race Conditions in File Operations

### The Problem
```python
# Race condition: file might be deleted between check and use
if path.exists():
    content = path.read_text()  # File might be gone now
```

### The Solution
```python
# Handle exceptions instead of checking first
try:
    content = path.read_text()
except FileNotFoundError:
    content = None

# Or use context managers for atomic operations
def atomic_write(path: Path, content: str):
    """Atomically write content to file."""
    temp_path = path.with_suffix('.tmp')
    try:
        temp_path.write_text(content)
        temp_path.replace(path)  # Atomic on POSIX
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
```

## 14. Memory Issues with Large Files

### The Problem
```python
# Wrong: loads entire file into memory
content = path.read_text()
# Process content...
```

### The Solution
```python
# Process large files line by line
with path.open('r', encoding='utf-8') as file:
    for line in file:
        # Process line
        pass

# Or use binary mode for large binary files
with path.open('rb') as file:
    while chunk := file.read(8192):  # Read in chunks
        # Process chunk
        pass
```

## 15. Not Using Path Methods Effectively

### The Problem
```python
# Verbose string manipulation
path_str = str(path)
name = os.path.basename(path_str)
stem = os.path.splitext(name)[0]
extension = os.path.splitext(name)[1]
```

### The Solution
```python
# Clean pathlib approach
name = path.name
stem = path.stem
suffix = path.suffix

# Even better for complex operations
if path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
    print("Image file")
```

## Summary

To avoid common pathlib mistakes:

1. **Use `/` operator** instead of string concatenation
2. **Check path existence** before operations
3. **Handle exceptions** appropriately
4. **Be aware of platform differences**
5. **Use efficient patterns** for multiple files
6. **Employ context managers** for file operations
7. **Specify encodings** explicitly
8. **Check permissions** when necessary
9. **Handle race conditions** properly
10. **Process large files** in chunks
11. **Leverage Path methods** instead of string operations

Following these guidelines will help you write robust, cross-platform filesystem code with pathlib.
