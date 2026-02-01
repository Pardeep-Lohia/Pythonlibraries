# `shutil` vs `os` vs `pathlib`: When to Use What

Understanding the differences between Python's file system modules is crucial for writing efficient and maintainable code. This guide helps you choose the right tool for the right job.

## Module Overview

| Module | Purpose | Level | Best For |
|--------|---------|-------|----------|
| `os` | Low-level OS interface | Low-level | System calls, process management |
| `shutil` | High-level file operations | High-level | File copying, moving, archiving |
| `pathlib` | Object-oriented path handling | Medium-level | Path manipulation, file system navigation |

## `shutil` vs `os`: High-level vs Low-level

### When to Use `shutil` Over `os`

#### ✅ File Copying Operations
```python
import shutil
import os

# shutil: Simple and robust
shutil.copy2('source.txt', 'destination.txt')

# os: Manual and error-prone
with open('source.txt', 'rb') as src, open('destination.txt', 'wb') as dst:
    dst.write(src.read())
os.chmod('destination.txt', os.stat('source.txt').st_mode)
os.utime('destination.txt', (os.stat('source.txt').st_atime, os.stat('source.txt').st_mtime))
```

**Why `shutil`?** Handles metadata preservation, error checking, and platform differences automatically.

#### ✅ Directory Operations
```python
# shutil: One-liner recursive operations
shutil.copytree('project', 'project_backup')

# os: Manual recursion required
def copytree_manual(src, dst):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isdir(src_path):
            copytree_manual(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)  # Still need shutil for copying!
```

**Why `shutil`?** Provides recursive operations with proper error handling.

#### ✅ Archiving
```python
# shutil: Built-in archiving
shutil.make_archive('project_v1', 'zip', 'project')

# os: No built-in support
# Would need to manually create ZIP/TAR files using zipfile/tarfile modules
```

**Why `shutil`?** Unified interface for multiple archive formats.

### When to Use `os` Over `shutil`

#### ✅ Low-level File System Operations
```python
import os

# os: Direct system calls
os.chmod('file.txt', 0o755)  # Change permissions
os.chown('file.txt', 1000, 1000)  # Change ownership (Unix only)
os.stat('file.txt')  # Get detailed file info
```

**Why `os`?** Direct access to system-specific features and detailed file metadata.

#### ✅ Process and System Management
```python
# os: Process and environment management
os.fork()  # Create child process
os.execv('/bin/ls', ['ls', '-l'])  # Execute program
os.environ['PATH']  # Access environment variables
```

**Why `os`?** `shutil` doesn't handle processes or environment variables.

#### ✅ File Descriptors and Low-level I/O
```python
# os: Direct file descriptor operations
fd = os.open('file.txt', os.O_RDONLY)
data = os.read(fd, 1024)
os.close(fd)
```

**Why `os`?** `shutil` works with file paths, not file descriptors.

## `shutil` vs `pathlib`: Operations vs Paths

### When to Use `shutil` Over `pathlib`

#### ✅ File Content Operations
```python
import shutil
from pathlib import Path

# shutil: Copy file contents and metadata
shutil.copy2('source.txt', 'dest.txt')

# pathlib: Only path operations
src = Path('source.txt')
dst = Path('dest.txt')
# pathlib can't copy file contents - need to combine with shutil
import shutil
shutil.copy2(str(src), str(dst))
```

**Why `shutil`?** `pathlib` handles paths, `shutil` handles file operations.

#### ✅ Directory Tree Operations
```python
# shutil: Recursive directory operations
shutil.copytree('src_dir', 'dst_dir')

# pathlib: Path manipulation only
src_dir = Path('src_dir')
dst_dir = Path('dst_dir')
# Still need shutil for actual copying
```

**Why `shutil`?** `pathlib` doesn't perform file system operations.

### When to Use `pathlib` Over `shutil`

#### ✅ Path Construction and Manipulation
```python
from pathlib import Path

# pathlib: Elegant path handling
config_dir = Path.home() / 'config' / 'app'
config_file = config_dir / 'settings.ini'

# os: String manipulation
config_dir = os.path.join(os.path.expanduser('~'), 'config', 'app')
config_file = os.path.join(config_dir, 'settings.ini')
```

**Why `pathlib`?** More readable and less error-prone than string operations.

#### ✅ File System Navigation
```python
# pathlib: Object-oriented navigation
documents = Path.home() / 'Documents'
python_files = documents.glob('**/*.py')

# os: Manual path construction
documents = os.path.join(os.path.expanduser('~'), 'Documents')
python_files = []
for root, dirs, files in os.walk(documents):
    for file in files:
        if file.endswith('.py'):
            python_files.append(os.path.join(root, file))
```

**Why `pathlib`?** More Pythonic and intuitive path handling.

#### ✅ Cross-platform Path Operations
```python
# pathlib: Automatic path separator handling
path = Path('folder') / 'subfolder' / 'file.txt'
str(path)  # 'folder/subfolder/file.txt' on Unix, 'folder\\subfolder\\file.txt' on Windows

# os: Manual separator handling
path = os.path.join('folder', 'subfolder', 'file.txt')
```

**Why `pathlib`?** Handles platform differences automatically.

## Best Practices: Combining the Modules

### The Power Trio: `os` + `pathlib` + `shutil`

```python
import os
import shutil
from pathlib import Path

def backup_project(project_name: str):
    """Backup a project using the best of all modules."""

    # pathlib: Path construction
    project_dir = Path.home() / 'projects' / project_name
    backup_dir = Path('/backups') / f"{project_name}_backup"

    # os: Check if source exists
    if not os.path.exists(project_dir):
        raise FileNotFoundError(f"Project not found: {project_dir}")

    # os: Check available space
    project_size = sum(
        os.path.getsize(f) for f in project_dir.rglob('*') if f.is_file()
    )
    usage = shutil.disk_usage(backup_dir.parent)
    if project_size > usage.free:
        raise OSError("Insufficient backup space")

    # shutil: Perform the backup
    shutil.copytree(str(project_dir), str(backup_dir))

    # pathlib: Verify backup
    original_files = list(project_dir.rglob('*'))
    backup_files = list(backup_dir.rglob('*'))

    if len(original_files) != len(backup_files):
        raise RuntimeError("Backup verification failed")

    return backup_dir
```

### Recommended Usage Patterns

#### For File Operations
```python
from pathlib import Path
import shutil

def process_files():
    """Process files in a directory."""

    # pathlib for path operations
    source_dir = Path('/data/input')
    output_dir = Path('/data/output')

    # shutil for file operations
    for file_path in source_dir.glob('*.txt'):
        # pathlib: path manipulation
        output_file = output_dir / file_path.name

        # shutil: file operation
        shutil.copy2(str(file_path), str(output_file))
```

#### For Directory Management
```python
import os
import shutil
from pathlib import Path

def organize_files():
    """Organize files by type."""

    # pathlib for path operations
    source = Path('/downloads')
    organized = Path('/organized')

    # Create subdirectories
    for ext in ['pdf', 'jpg', 'txt']:
        (organized / ext).mkdir(parents=True, exist_ok=True)

    # shutil for moving files
    for file_path in source.iterdir():
        if file_path.is_file():
            ext = file_path.suffix.lower().lstrip('.')
            if ext in ['pdf', 'jpg', 'txt']:
                dest_dir = organized / ext
                shutil.move(str(file_path), str(dest_dir / file_path.name))
```

## Performance Considerations

### `shutil` Performance Characteristics
- **Copy operations**: Efficient for large files (uses buffering)
- **Directory operations**: Can be slow for deep directory trees
- **Archive operations**: Memory-efficient for most use cases

### `os` Performance Characteristics
- **Direct calls**: Fastest for simple operations
- **No overhead**: Minimal Python-level processing
- **System-dependent**: Performance varies by platform

### `pathlib` Performance Characteristics
- **Path operations**: Fast string manipulation
- **Object creation**: Slight overhead vs string operations
- **Iteration**: Efficient for large directory traversals

### Optimization Tips

```python
import os
import shutil
from pathlib import Path

# ✅ Efficient: Use pathlib for filtering, shutil for operations
def find_and_copy_python_files(src_dir, dst_dir):
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)

    # pathlib: efficient filtering
    python_files = list(src_path.rglob('*.py'))

    # shutil: efficient copying
    for py_file in python_files:
        rel_path = py_file.relative_to(src_path)
        dst_file = dst_path / rel_path
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(py_file), str(dst_file))

# ❌ Inefficient: String operations in loop
def find_and_copy_python_files_slow(src_dir, dst_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, src_dir)
                dst_file = os.path.join(dst_dir, rel_path)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
```

## Migration Guide

### Migrating from `os` to `shutil`

```python
# Old: os-based copying
def old_copy(src, dst):
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            fdst.write(fsrc.read())

# New: shutil-based copying
def new_copy(src, dst):
    shutil.copy2(src, dst)  # Simpler, more robust
```

### Migrating from `os.path` to `pathlib`

```python
# Old: os.path operations
def old_path_ops():
    path = os.path.join('folder', 'subfolder', 'file.txt')
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)

# New: pathlib operations
def new_path_ops():
    path = Path('folder') / 'subfolder' / 'file.txt'
    dirname = path.parent
    basename = path.name
```

## Summary

Choose the right tool for the job:

- **`shutil`**: High-level file operations (copying, moving, archiving)
- **`os`**: Low-level system interface and detailed file metadata
- **`pathlib`**: Modern path handling and file system navigation

**Best practice**: Use them together - `pathlib` for paths, `shutil` for operations, `os` when you need low-level control.

```python
# Ideal combination
from pathlib import Path
import shutil
import os

def robust_file_operation():
    # pathlib: path handling
    src = Path('data') / 'input.txt'
    dst = Path('backup') / src.name

    # os: system checks
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source not found: {src}")

    # shutil: file operation
    shutil.copy2(str(src), str(dst))
