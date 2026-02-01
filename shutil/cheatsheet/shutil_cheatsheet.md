# `shutil` Module Quick Reference

## File Operations

### Copy Files
```python
import shutil

# Basic copy (preserves mode, not timestamps)
shutil.copy(src, dst)

# Copy with metadata preservation
shutil.copy2(src, dst)

# Copy file object
with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
    shutil.copyfileobj(fsrc, fdst)

# Copy only file contents
shutil.copyfile(src, dst)
```

### Move/Rename Files
```python
# Move file (efficient rename if same filesystem)
shutil.move(src, dst)
```

### Metadata Operations
```python
# Copy permissions only
shutil.copymode(src, dst)

# Copy all metadata (permissions, timestamps)
shutil.copystat(src, dst)

# Change ownership (Unix only)
shutil.chown(path, user='username', group='groupname')
```

## Directory Operations

### Copy Directories
```python
# Recursive directory copy
shutil.copytree(src, dst)

# Copy with ignore patterns
shutil.copytree(src, dst, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))

# Copy allowing existing destination (Python 3.8+)
shutil.copytree(src, dst, dirs_exist_ok=True)
```

### Remove Directories
```python
# Remove directory tree
shutil.rmtree(path)

# Remove with error handling
shutil.rmtree(path, onerror=error_handler)

# Ignore all errors
shutil.rmtree(path, ignore_errors=True)
```

### Move Directories
```python
# Move directory (same as file move)
shutil.move(src_dir, dst_dir)
```

## Archiving Operations

### Create Archives
```python
# ZIP archive
shutil.make_archive('backup', 'zip', 'source_dir')

# Compressed tar
shutil.make_archive('backup', 'gztar', 'source_dir')

# BZIP2 tar
shutil.make_archive('backup', 'bztar', 'source_dir')

# XZ tar
shutil.make_archive('backup', 'xztar', 'source_dir')
```

### Extract Archives
```python
# Auto-detect format
shutil.unpack_archive('archive.zip', 'extract_dir')

# Specify format
shutil.unpack_archive('archive.tar.gz', 'extract_dir', format='gztar')
```

### Archive Information
```python
# Get supported formats
formats = shutil.get_archive_formats()  # [('zip', 'zip'), ('tar', 'tar'), ...]
unpack_formats = shutil.get_unpack_formats()
```

## Utility Functions

### Disk Usage
```python
# Get filesystem usage
usage = shutil.disk_usage(path)
print(f"Total: {usage.total}, Used: {usage.used}, Free: {usage.free}")
```

### Path Operations
```python
# Get disk usage as percentages
total_gb = usage.total / (1024**3)
used_percent = (usage.used / usage.total) * 100
```

## Common Patterns

### Safe File Operations
```python
import os

# Check if destination exists
if os.path.exists(dst):
    overwrite = input(f"Overwrite {dst}? (y/N): ").lower() == 'y'
    if not overwrite:
        exit()

# Check disk space before copy
src_size = os.path.getsize(src)
dst_usage = shutil.disk_usage(os.path.dirname(dst))
if src_size > dst_usage.free:
    print("Insufficient disk space")
    exit()

shutil.copy2(src, dst)
```

### Directory Synchronization
```python
def sync_dirs(src, dst):
    """Basic directory sync"""
    for root, dirs, files in os.walk(src):
        # Create relative path
        rel_path = os.path.relpath(root, src)
        dst_root = os.path.join(dst, rel_path) if rel_path != '.' else dst

        # Create directories
        os.makedirs(dst_root, exist_ok=True)

        # Copy files
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_root, file)
            if not os.path.exists(dst_file) or \
               os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                shutil.copy2(src_file, dst_file)
```

### Error Handling
```python
try:
    shutil.copytree('source', 'destination')
except FileExistsError:
    print("Destination exists")
except PermissionError:
    print("Permission denied")
except OSError as e:
    print(f"OS error: {e}")
except shutil.Error as e:
    print(f"Multiple errors: {e}")
```

### Progress Reporting
```python
import os

def copy_with_progress(src, dst):
    """Copy with simple progress"""
    size = os.path.getsize(src)
    copied = 0

    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        while True:
            chunk = fsrc.read(8192)
            if not chunk:
                break
            fdst.write(chunk)
            copied += len(chunk)
            progress = (copied / size) * 100
            print(f"\rProgress: {progress:.1f}%", end='')
    print()  # New line
```

### Temporary Files
```python
import tempfile

# Safe atomic operations
with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as tmp:
    # Write to temporary file
    shutil.copy2('source', tmp.name)

    # Atomic move to final location
    shutil.move(tmp.name, 'destination')
```

## Platform Considerations

### Windows
- Use raw strings for paths: `r'C:\path\to\file'`
- Drive letters: `shutil.disk_usage('C:\\')`
- Permissions work differently

### Unix/Linux/macOS
- Full POSIX permissions support
- Symbolic links preserved by default
- `chown()` available for ownership changes

### Cross-Platform
```python
import os

# Platform-safe path joining
path = os.path.join('folder', 'subfolder', 'file.txt')

# Check platform
if os.name == 'nt':  # Windows
    # Windows-specific code
else:  # Unix-like
    # POSIX code
```

## Performance Tips

- Use `copy()` instead of `copy2()` if timestamps aren't needed
- `move()` is efficient within the same filesystem
- For large files, `copyfileobj()` with custom buffer size
- Use `ignore` parameter in `copytree()` to skip unwanted files
- Consider memory usage with deep directory trees

## Import Statement
```python
import shutil
```

## Error Classes
- `shutil.Error`: Collection of multiple errors (e.g., from `copytree()`)
- `shutil.SameFileError`: Source and destination are the same
- `shutil.SpecialFileError`: Special file types not supported

## Function Categories

| Category | Functions |
|----------|-----------|
| File Copy | `copy()`, `copy2()`, `copyfile()`, `copyfileobj()` |
| Directory | `copytree()`, `rmtree()`, `move()` |
| Metadata | `copymode()`, `copystat()`, `chown()` |
| Archive | `make_archive()`, `unpack_archive()` |
| Utility | `disk_usage()`, `get_archive_formats()` |

## Quick Examples

```python
# Backup with timestamp
import time
backup_name = f"backup_{time.strftime('%Y%m%d_%H%M%S')}"
shutil.make_archive(backup_name, 'zip', 'important_files')

# Clean old files
import os
for file in os.listdir('temp'):
    if file.endswith('.tmp'):
        os.remove(os.path.join('temp', file))

# Get directory size
def dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        total += sum(os.path.getsize(os.path.join(root, file)) for file in files)
    return total
```

This cheatsheet covers the most commonly used `shutil` functions and patterns. For complete documentation, see the official Python documentation.
