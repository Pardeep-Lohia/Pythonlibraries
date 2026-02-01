# Directory Operations Functions in `shutil`

The `shutil` module provides powerful functions for directory operations, including recursive copying, moving, and removal of directory trees. This document covers all directory-related functions with their syntax, examples, and edge cases.

## `shutil.copytree(src, dst, symlinks=False, ignore=None, copy_function=<function copy2>, ignore_dangling_symlinks=False, dirs_exist_ok=False)`

### Purpose
Recursively copies an entire directory tree from source to destination, preserving all file metadata and directory structure.

### Syntax
```python
shutil.copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False, dirs_exist_ok=False)
```

### Parameters
- `src`: Source directory path
- `dst`: Destination directory path (must not exist unless `dirs_exist_ok=True`)
- `symlinks`: If `True`, copy symlinks as symlinks; if `False`, follow and copy their targets
- `ignore`: Function that returns a set of names to ignore, or callable that takes directory path and list of contents
- `copy_function`: Function to use for copying files (default: `copy2`)
- `ignore_dangling_symlinks`: If `True`, ignore dangling symlinks; if `False`, raise error
- `dirs_exist_ok`: If `True`, allow destination directory to exist (Python 3.8+)

### Return Value
Returns the destination directory path.

### Example
```python
import shutil

# Basic directory copy
shutil.copytree('source_dir', 'destination_dir')

# Copy with custom ignore patterns
def ignore_patterns(*patterns):
    import fnmatch
    def _ignore_patterns(path, names):
        ignored = []
        for pattern in patterns:
            ignored.extend(fnmatch.filter(names, pattern))
        return set(ignored)
    return _ignore_patterns

shutil.copytree('project', 'backup',
                ignore=ignore_patterns('*.pyc', '__pycache__', '.git'))

# Copy allowing existing destination (Python 3.8+)
shutil.copytree('source', 'existing_dest', dirs_exist_ok=True)
```

### Edge Cases
- Destination directory must not exist (unless `dirs_exist_ok=True`)
- Symlinks are followed by default; set `symlinks=True` to copy as links
- Permissions and metadata are preserved
- Large directory trees can take significant time and disk space

## `shutil.rmtree(path, ignore_errors=False, onerror=None)`

### Purpose
Recursively removes a directory tree, deleting all files and subdirectories.

### Syntax
```python
shutil.rmtree(path, ignore_errors=False, onerror=None)
```

### Parameters
- `path`: Directory path to remove
- `ignore_errors`: If `True`, ignore errors during removal
- `onerror`: Function called when errors occur (receives function, path, and exception info)

### Return Value
None

### Example
```python
import shutil

# Remove directory tree
shutil.rmtree('temp_directory')

# Remove with error handling
def handle_error(func, path, exc_info):
    print(f'Error removing {path}: {exc_info[1]}')

shutil.rmtree('problematic_dir', onerror=handle_error)

# Ignore all errors
shutil.rmtree('may_not_exist', ignore_errors=True)
```

### Edge Cases
- Operation is irreversible - use with caution
- May fail if files are in use by other processes
- Permission errors common on read-only filesystems
- Symbolic links are removed, not followed

## `shutil.move(src, dst)`

### Purpose
Moves a file or directory from source to destination. If moving across filesystems, this performs a copy followed by delete.

### Syntax
```python
shutil.move(src, dst)
```

### Parameters
- `src`: Source path (file or directory)
- `dst`: Destination path

### Return Value
Returns the destination path.

### Example
```python
import shutil

# Move file
shutil.move('old_location.txt', 'new_location.txt')

# Move directory
shutil.move('old_folder', 'new_folder')

# Move into directory
shutil.move('file.txt', 'destination_directory/')
```

### Edge Cases
- If `dst` is a directory, `src` is moved into it
- Cross-filesystem moves are copy + delete operations
- Same-filesystem moves are efficient renames
- Overwrites destination if it exists

## `shutil.disk_usage(path)`

### Purpose
Returns disk usage statistics for the filesystem containing the given path.

### Syntax
```python
shutil.disk_usage(path)
```

### Parameters
- `path`: Path on the filesystem to check

### Return Value
Named tuple with fields: `total`, `used`, `free` (all in bytes)

### Example
```python
import shutil

# Get disk usage
usage = shutil.disk_usage('/')
print(f"Total: {usage.total / (1024**3):.2f} GB")
print(f"Used: {usage.used / (1024**3):.2f} GB")
print(f"Free: {usage.free / (1024**3):.2f} GB")

# Calculate usage percentage
percent_used = (usage.used / usage.total) * 100
print(f"Usage: {percent_used:.1f}%")
```

### Edge Cases
- Returns usage for the filesystem containing `path`
- Values are in bytes
- May not work on all filesystems (e.g., some network drives)

## `shutil.chown(path, user=None, group=None)`

### Purpose
Changes the owner and/or group of a file or directory (Unix-like systems only).

### Syntax
```python
shutil.chown(path, user=None, group=None)
```

### Parameters
- `path`: Path to change ownership
- `user`: New owner (username or UID)
- `group`: New group (group name or GID)

### Return Value
None

### Example
```python
import shutil

# Change owner
shutil.chown('file.txt', user='newuser')

# Change group
shutil.chown('file.txt', group='newgroup')

# Change both
shutil.chown('file.txt', user='user', group='group')

# Use numeric IDs
shutil.chown('file.txt', user=1000, group=1000)
```

### Edge Cases
- Only available on Unix-like systems
- Requires appropriate permissions to change ownership
- Can change ownership of directories recursively with `os.walk()`

## `shutil.make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0, dry_run=0, owner=None, group=None, logger=None)`

### Purpose
Creates an archive file (ZIP, TAR, etc.) from a directory.

### Syntax
```python
shutil.make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0, dry_run=0, owner=None, group=None, logger=None)
```

### Parameters
- `base_name`: Base name of the archive (without extension)
- `format`: Archive format ('zip', 'tar', 'gztar', 'bztar', 'xztar')
- `root_dir`: Root directory for archive (default: current directory)
- `base_dir`: Directory to archive within root_dir
- `verbose`: Verbosity level
- `dry_run`: If true, don't create archive
- `owner/group`: Set ownership in tar archives
- `logger`: Logger object for output

### Return Value
Returns the archive file name.

### Example
```python
import shutil

# Create ZIP archive
shutil.make_archive('backup', 'zip', 'source_directory')

# Create compressed tar archive
shutil.make_archive('project_backup', 'gztar', '.', 'my_project')

# Create tar archive with custom root
archive_name = shutil.make_archive('website', 'tar', '/var/www', 'html')
print(f"Created: {archive_name}")
```

### Edge Cases
- Archive format determines compression and capabilities
- `base_dir` is archived within `root_dir`
- Extensions are added automatically (.zip, .tar.gz, etc.)

## `shutil.unpack_archive(filename, extract_dir=None, format=None)`

### Purpose
Extracts an archive file to a directory.

### Syntax
```python
shutil.unpack_archive(filename, extract_dir=None, format=None)
```

### Parameters
- `filename`: Archive file to extract
- `extract_dir`: Directory to extract to (default: current directory)
- `format`: Archive format (auto-detected if None)

### Return Value
None

### Example
```python
import shutil

# Extract archive
shutil.unpack_archive('backup.zip')

# Extract to specific directory
shutil.unpack_archive('project.tar.gz', 'extracted_project')

# Extract with format specification
shutil.unpack_archive('archive.xz', extract_dir='output', format='xztar')
```

### Edge Cases
- Format is auto-detected from file extension
- Creates extraction directory if it doesn't exist
- Overwrites files without warning

## `shutil.get_archive_formats()`

### Purpose
Returns a list of supported archive formats.

### Syntax
```python
shutil.get_archive_formats()
```

### Return Value
List of tuples: (format_name, description)

### Example
```python
import shutil

# List supported formats
formats = shutil.get_archive_formats()
for name, desc in formats:
    print(f"{name}: {desc}")
```

## `shutil.get_unpack_formats()`

### Purpose
Returns a list of supported unpack formats.

### Syntax
```python
shutil.get_unpack_formats()
```

### Return Value
List of tuples: (format_name, extensions, description)

### Example
```python
import shutil

# List supported unpack formats
formats = shutil.get_unpack_formats()
for name, exts, desc in formats:
    print(f"{name} ({', '.join(exts)}): {desc}")
```

## Common Patterns

### Safe Directory Removal with Confirmation
```python
import shutil
import os

def safe_rmtree(path, confirm=True):
    """Safely remove directory tree with confirmation."""
    if not os.path.exists(path):
        print(f"Path {path} does not exist")
        return

    if confirm:
        response = input(f"Remove directory {path}? (y/N): ")
        if response.lower() != 'y':
            return

    try:
        shutil.rmtree(path)
        print(f"Removed {path}")
    except Exception as e:
        print(f"Error removing {path}: {e}")
```

### Directory Synchronization
```python
import shutil
import os
from pathlib import Path

def sync_dirs(src, dst):
    """Synchronize destination directory with source."""
    src_path = Path(src)
    dst_path = Path(dst)

    # Remove destination if it exists
    if dst_path.exists():
        shutil.rmtree(dst_path)

    # Copy source to destination
    shutil.copytree(src_path, dst_path)
```

### Archive Management
```python
import shutil
from datetime import datetime

def create_timestamped_backup(src_dir, backup_dir):
    """Create timestamped backup archive."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_name = f"backup_{timestamp}"

    archive_path = shutil.make_archive(
        os.path.join(backup_dir, archive_name),
        'gztar',
        src_dir
    )

    return archive_path
```

## Error Handling

Directory operations can raise various exceptions:

```python
import shutil
from shutil import Error as ShutilError

try:
    shutil.copytree('source', 'destination')
except FileExistsError:
    print("Destination already exists")
except PermissionError:
    print("Permission denied")
except OSError as e:
    print(f"OS error: {e}")
except ShutilError as e:
    print(f"Multiple errors: {e}")
```

## Performance Considerations

- `copytree()` can be slow for large directory trees
- `rmtree()` is generally fast but irreversible
- `move()` is efficient within the same filesystem
- Archive operations are I/O intensive
- Consider using `os.scandir()` for very large directories

## Platform Differences

- **Windows**: Some operations may behave differently (e.g., permissions)
- **Unix/Linux**: Full POSIX semantics supported
- **macOS**: Resource forks and extended attributes handling
- Archive formats may have platform-specific limitations

## Best Practices

1. Always check if paths exist before operations
2. Use `try/except` blocks for error handling
3. Consider using `pathlib.Path` for path operations
4. Test operations on small directories first
5. Use `ignore` parameter to exclude unwanted files
6. Be cautious with `rmtree()` - operations are irreversible
7. Use `dirs_exist_ok=True` when appropriate (Python 3.8+)
8. Consider disk space requirements for copy operations

These functions provide comprehensive directory manipulation capabilities essential for file system automation, backup systems, and deployment tools.
