# Directory Handling Functions

## Overview
Directory handling functions in the `os` module allow you to create, remove, and navigate directories. These operations are fundamental for file system management.

## Core Functions

### `os.getcwd()` - Get Current Working Directory
**Purpose**: Returns the current working directory as a string.

**Syntax**:
```python
os.getcwd()
```

**Return Value**: String representing the absolute path of the current directory.

**Example**:
```python
import os
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")
# Output: Current directory: /home/user/projects
```

**Edge Cases**:
- Always returns an absolute path
- May raise `OSError` if the current directory is deleted while the process is running

### `os.chdir(path)` - Change Current Working Directory
**Purpose**: Changes the current working directory to the specified path.

**Syntax**:
```python
os.chdir(path)
```

**Parameters**:
- `path`: String or path-like object to change to

**Example**:
```python
import os
print(f"Before: {os.getcwd()}")
os.chdir('/tmp')
print(f"After: {os.getcwd()}")
```

**Edge Cases**:
- Raises `FileNotFoundError` if path doesn't exist
- Raises `PermissionError` if no access permission
- Relative paths are resolved from current directory

### `os.listdir(path='.')` - List Directory Contents
**Purpose**: Returns a list of entries in the specified directory.

**Syntax**:
```python
os.listdir(path='.')
```

**Parameters**:
- `path`: Directory to list (default: current directory)

**Return Value**: List of strings (filenames and directory names)

**Example**:
```python
import os
entries = os.listdir('.')
print("Directory contents:")
for entry in entries:
    print(f"  {entry}")
```

**Edge Cases**:
- Returns only names, not full paths
- Includes hidden files (starting with `.`)
- Order is not guaranteed (depends on filesystem)
- Raises `FileNotFoundError` for non-existent directories

### `os.mkdir(path, mode=0o777)` - Create Directory
**Purpose**: Creates a new directory at the specified path.

**Syntax**:
```python
os.mkdir(path, mode=0o777)
```

**Parameters**:
- `path`: Path for the new directory
- `mode`: Permission mode (Unix-like systems only)

**Example**:
```python
import os
os.mkdir('new_folder')
print("Directory created")
```

**Edge Cases**:
- Raises `FileExistsError` if directory already exists
- Parent directories must exist (use `os.makedirs()` for recursive creation)
- Mode parameter ignored on Windows

### `os.makedirs(path, mode=0o777, exist_ok=False)` - Create Directories Recursively
**Purpose**: Creates directories recursively, creating intermediate directories as needed.

**Syntax**:
```python
os.makedirs(path, mode=0o777, exist_ok=False)
```

**Parameters**:
- `path`: Path to create (intermediate directories created automatically)
- `mode`: Permission mode for new directories
- `exist_ok`: If True, don't raise error if directory exists

**Example**:
```python
import os
os.makedirs('parent/child/grandchild', exist_ok=True)
print("Directory tree created")
```

**Edge Cases**:
- `exist_ok=True` prevents errors when directory already exists
- More efficient than checking existence manually
- Still raises `PermissionError` if no write access

### `os.rmdir(path)` - Remove Directory
**Purpose**: Removes an empty directory.

**Syntax**:
```python
os.rmdir(path)
```

**Parameters**:
- `path`: Path to the directory to remove

**Example**:
```python
import os
os.rmdir('empty_folder')
print("Directory removed")
```

**Edge Cases**:
- Directory must be empty
- Raises `OSError` if directory not empty
- Raises `FileNotFoundError` if directory doesn't exist

### `os.removedirs(path)` - Remove Directories Recursively
**Purpose**: Removes directories recursively, removing empty parent directories.

**Syntax**:
```python
os.removedirs(path)
```

**Parameters**:
- `path`: Path to start removing from

**Example**:
```python
import os
os.removedirs('parent/child/grandchild')
print("Directory tree removed")
```

**Edge Cases**:
- Stops when it encounters a non-empty directory
- Useful for cleaning up temporary directory structures
- May leave partial directory trees

## Advanced Directory Operations

### `os.scandir(path='.')` - Efficient Directory Iteration
**Purpose**: Returns an iterator of directory entries with more information than `listdir()`.

**Syntax**:
```python
os.scandir(path='.')
```

**Return Value**: Iterator of `DirEntry` objects

**Example**:
```python
import os
with os.scandir('.') as entries:
    for entry in entries:
        print(f"{entry.name}: {'directory' if entry.is_dir() else 'file'}")
```

**Benefits**:
- More efficient than `listdir()` + `stat()`
- Provides `DirEntry` objects with methods like `is_file()`, `is_dir()`
- Automatically closes directory handle

### `os.rename(src, dst)` - Rename/Move Files and Directories
**Purpose**: Renames or moves a file or directory.

**Syntax**:
```python
os.rename(src, dst)
```

**Parameters**:
- `src`: Source path
- `dst`: Destination path

**Example**:
```python
import os
os.rename('old_name.txt', 'new_name.txt')
os.rename('file.txt', 'backup/file.txt')  # Move
```

**Edge Cases**:
- Cannot move across filesystems on Unix
- Destination directory must exist for moves
- Overwrites destination if it exists

### `os.replace(src, dst)` - Replace Files and Directories
**Purpose**: Renames or moves, overwriting the destination if it exists.

**Syntax**:
```python
os.replace(src, dst)
```

**Parameters**:
- `src`: Source path
- `dst`: Destination path

**Example**:
```python
import os
os.replace('file.txt', 'existing_file.txt')  # Overwrites
```

**Cross-platform**: Works across filesystems unlike `os.rename()` on some systems.

## Best Practices

1. **Use `os.path.join()`** for path construction
2. **Check existence** before operations when necessary
3. **Use `exist_ok=True`** with `makedirs()` to avoid race conditions
4. **Prefer `os.scandir()`** for directory iteration when you need file type information
5. **Handle permissions** appropriately for your use case
6. **Use context managers** when working with directory iterators

## Common Patterns

### Safe Directory Creation
```python
import os

def ensure_dir(path):
    """Ensure directory exists, create if necessary."""
    os.makedirs(path, exist_ok=True)
```

### Temporary Directory Management
```python
import os
import tempfile

def with_temp_dir(func):
    """Execute function in a temporary directory."""
    original_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        try:
            return func()
        finally:
            os.chdir(original_dir)
```

### Recursive Directory Removal
```python
import os
import shutil

def remove_dir_tree(path):
    """Remove directory tree recursively."""
    if os.path.exists(path):
        shutil.rmtree(path)  # More robust than os.removedirs
```

These functions provide the foundation for file system navigation and management in Python applications.
