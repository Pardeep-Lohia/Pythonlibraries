# Common Mistakes When Using `shutil`

This guide covers the most frequent errors and misconceptions when working with the `shutil` module, along with how to avoid them.

## 1. Using `copy()` Instead of `copy2()`

### The Mistake
```python
import shutil

# Wrong: Loses metadata
shutil.copy('important.txt', 'backup.txt')
```

### Why It's Wrong
`shutil.copy()` only preserves the file's permission mode but not timestamps, extended attributes, or other metadata. This can cause issues in backup systems, deployment scripts, or any scenario where metadata preservation matters.

### The Fix
```python
# Correct: Preserves all metadata
shutil.copy2('important.txt', 'backup.txt')
```

### When `copy()` Is Acceptable
Only use `copy()` when you explicitly don't want to preserve metadata, such as when creating cache files or temporary copies.

## 2. Not Handling Errors Properly

### The Mistake
```python
import shutil

# Wrong: No error handling
shutil.copytree('source', 'destination')
shutil.rmtree('temp_dir')
```

### Why It's Wrong
File operations can fail for many reasons: permissions, disk space, file locks, network issues, etc. Without error handling, your program will crash unexpectedly.

### The Fix
```python
import shutil

try:
    shutil.copytree('source', 'destination')
    print("Copy successful")
except FileExistsError:
    print("Destination already exists")
except PermissionError:
    print("Permission denied")
except OSError as e:
    print(f"Copy failed: {e}")

# For rmtree, be extra careful
try:
    shutil.rmtree('temp_dir')
except OSError as e:
    print(f"Failed to remove directory: {e}")
```

## 3. Using `rmtree()` Without Confirmation

### The Mistake
```python
import shutil

# Dangerous: No confirmation
shutil.rmtree('/user/data')
```

### Why It's Wrong
`rmtree()` recursively deletes everything in the specified directory. This operation is irreversible and can cause catastrophic data loss.

### The Fix
```python
import shutil
import os

def safe_rmtree(path, force=False):
    """Safely remove directory tree with confirmation."""
    if not os.path.exists(path):
        print(f"Path {path} does not exist")
        return

    if not force:
        response = input(f"Really delete {path} and all contents? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled")
            return

    try:
        shutil.rmtree(path)
        print(f"Removed {path}")
    except OSError as e:
        print(f"Error removing {path}: {e}")

# Usage
safe_rmtree('/user/data')
```

## 4. Mixing Path Types Inconsistently

### The Mistake
```python
import shutil
from pathlib import Path

src = Path('file.txt')
dst = 'copy.txt'

# Wrong: Inconsistent types
shutil.copy(src, dst)  # May work but inconsistent
```

### Why It's Wrong
While `shutil` functions accept both strings and Path objects, mixing them can lead to confusion and platform-specific issues. Some functions may not handle Path objects correctly in all Python versions.

### The Fix
```python
import shutil
from pathlib import Path

# Consistent: Convert to strings
src = Path('file.txt')
dst = Path('copy.txt')

shutil.copy(str(src), str(dst))

# Or use Path operations
dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copy(str(src), str(dst))
```

## 5. Not Checking Disk Space Before Operations

### The Mistake
```python
import shutil

# Wrong: No space checking
shutil.copytree('/large/source', '/small/destination')
```

### Why It's Wrong
Copy operations can fail with "No space left on device" errors, leaving partial copies and corrupted data.

### The Fix
```python
import shutil
import os

def calculate_directory_size(path):
    """Calculate total size of directory recursively."""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total += os.path.getsize(filepath)
            except OSError:
                pass
    return total

def safe_copytree(src, dst):
    """Copy directory tree with space checking."""
    if not os.path.exists(src):
        raise ValueError(f"Source {src} does not exist")

    # Calculate required space
    src_size = calculate_directory_size(src)
    dst_usage = shutil.disk_usage(dst)

    # Add some buffer (10% overhead)
    required_space = int(src_size * 1.1)

    if required_space > dst_usage.free:
        raise OSError(f"Insufficient space: need {required_space:,} bytes, "
                     f"have {dst_usage.free:,} bytes free")

    shutil.copytree(src, dst)
    print(f"Successfully copied {src_size:,} bytes")

# Usage
try:
    safe_copytree('/large/source', '/small/destination')
except OSError as e:
    print(f"Copy failed: {e}")
```

## 6. Using `move()` Incorrectly for Cross-Filesystem Operations

### The Mistake
```python
import shutil

# Wrong assumption: move is always efficient
shutil.move('/local/file.txt', '/network/drive/file.txt')
```

### Why It's Wrong
`shutil.move()` automatically chooses between efficient rename (same filesystem) and copy+delete (different filesystems). However, for large files across slow networks, this can take unexpectedly long without progress feedback.

### The Fix
```python
import shutil
import os

def smart_move(src, dst, show_progress=False):
    """Move file with awareness of filesystem boundaries."""
    src_stat = os.stat(src)
    dst_stat = os.stat(os.path.dirname(dst))

    # Check if same filesystem
    same_fs = src_stat.st_dev == dst_stat.st_dev

    if same_fs:
        # Efficient rename
        shutil.move(src, dst)
    else:
        # Cross-filesystem: copy + delete with progress
        if show_progress:
            print(f"Cross-filesystem move: copying {src} to {dst}")

        shutil.copy2(src, dst)

        if show_progress:
            print("Removing source file")

        os.remove(src)

# Usage
smart_move('/local/file.txt', '/network/drive/file.txt', show_progress=True)
```

## 7. Ignoring the `ignore` Parameter in `copytree()`

### The Mistake
```python
import shutil

# Wrong: Copies everything including unwanted files
shutil.copytree('project', 'backup')
```

### Why It's Wrong
This copies all files including temporary files, cache directories, version control files, etc., which can waste space and copy sensitive information.

### The Fix
```python
import shutil
import fnmatch

def ignore_patterns(*patterns):
    """Create ignore function for multiple patterns."""
    def _ignore_patterns(path, names):
        ignored = []
        for pattern in patterns:
            ignored.extend(fnmatch.filter(names, pattern))
        return set(ignored)
    return _ignore_patterns

# Correct: Exclude unwanted files
shutil.copytree(
    'project',
    'backup',
    ignore=ignore_patterns(
        '*.pyc', '__pycache__', '.git', '.svn', '.DS_Store',
        '*.tmp', '*.bak', '*.swp', '~*', 'node_modules'
    )
)
```

## 8. Not Understanding Archive Formats

### The Mistake
```python
import shutil

# Wrong: Assuming all archives work the same
shutil.make_archive('backup', 'zip', 'source')  # Creates backup.zip
shutil.unpack_archive('backup.zip', 'destination')  # Wrong extension assumption
```

### Why It's Wrong
`make_archive()` automatically adds appropriate extensions (.zip, .tar.gz, etc.), but `unpack_archive()` doesn't auto-detect format from extension. Also, different formats have different capabilities and compression levels.

### The Fix
```python
import shutil

# Correct: Handle extensions properly
archive_name = shutil.make_archive('backup', 'zip', 'source')
# archive_name is now 'backup.zip'

# Extract with explicit format or let it auto-detect
shutil.unpack_archive(archive_name, 'destination')

# Or specify format explicitly
shutil.unpack_archive('backup.tar.gz', 'destination', format='gztar')

# Check supported formats
print("Supported archive formats:")
for name, desc in shutil.get_archive_formats():
    print(f"  {name}: {desc}")
```

## 9. Using `shutil` for Path Operations

### The Mistake
```python
import shutil

# Wrong: Using shutil for path operations
dirname = shutil.os.path.dirname('/path/to/file.txt')
basename = shutil.os.path.basename('/path/to/file.txt')
```

### Why It's Wrong
While `shutil` does import `os.path`, it's not the intended interface. This creates confusion and makes code less readable. `shutil` is for file operations, not path manipulations.

### The Fix
```python
import os
from pathlib import Path

# Correct: Use os.path for path operations
dirname = os.path.dirname('/path/to/file.txt')
basename = os.path.basename('/path/to/file.txt')

# Better: Use pathlib
path = Path('/path/to/file.txt')
dirname = str(path.parent)
basename = path.name
```

## 10. Not Handling Symlinks Correctly

### The Mistake
```python
import shutil

# Wrong: Unaware of symlink behavior
shutil.copytree('source', 'dest')  # Default: symlinks=True
```

### Why It's Wrong
By default, `copytree()` copies symlinks as symlinks. If the symlink points to a file outside the source tree, the destination symlink will be broken (dangling).

### The Fix
```python
import shutil

# Option 1: Follow symlinks (copy targets)
shutil.copytree('source', 'dest', symlinks=False)

# Option 2: Copy symlinks but handle dangling ones
try:
    shutil.copytree('source', 'dest', symlinks=True, ignore_dangling_symlinks=True)
except shutil.Error as e:
    print(f"Copy completed with warnings: {e}")

# Option 3: Custom symlink handling
def copytree_with_symlink_check(src, dst, **kwargs):
    """Copy tree with symlink validation."""
    def ignore_dangling(path, names):
        ignored = []
        for name in names:
            full_path = os.path.join(path, name)
            if os.path.islink(full_path):
                try:
                    os.stat(full_path)  # Check if target exists
                except OSError:
                    ignored.append(name)
                    print(f"Ignoring dangling symlink: {full_path}")
        return ignored

    ignore_func = kwargs.get('ignore', lambda p, n: [])
    def combined_ignore(path, names):
        return ignore_func(path, names) | set(ignore_dangling(path, names))

    kwargs['ignore'] = combined_ignore
    shutil.copytree(src, dst, **kwargs)
```

## 11. Memory Issues with Large Directories

### The Mistake
```python
import shutil

# Wrong: May consume too much memory for large trees
shutil.copytree('/very/large/directory', '/destination')
```

### Why It's Wrong
`copytree()` loads directory structures into memory. For very large directory trees, this can cause memory exhaustion.

### The Fix
```python
import shutil
import os
from pathlib import Path

def copytree_streaming(src, dst, chunk_size=1024*1024):
    """Copy directory tree with controlled memory usage."""
    src_path = Path(src)
    dst_path = Path(dst)

    for src_file in src_path.rglob('*'):
        if src_file.is_file():
            dst_file = dst_path / src_file.relative_to(src_path)
            dst_file.parent.mkdir(parents=True, exist_ok=True)

            # Copy in chunks to control memory usage
            with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
                while True:
                    chunk = fsrc.read(chunk_size)
                    if not chunk:
                        break
                    fdst.write(chunk)

            # Copy metadata
            shutil.copymode(src_file, dst_file)
            shutil.copystat(src_file, dst_file)

# For extremely large trees, consider batching
def copytree_batched(src, dst, batch_size=1000):
    """Copy large directory trees in batches."""
    files = list(Path(src).rglob('*'))
    files = [f for f in files if f.is_file()]

    for i in range(0, len(files), batch_size):
        batch = files[i:i + batch_size]
        for src_file in batch:
            dst_file = Path(dst) / src_file.relative_to(src)
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
        print(f"Processed {min(i + batch_size, len(files))}/{len(files)} files")
```

## 12. Race Conditions in Multi-Process Environments

### The Mistake
```python
import shutil
import os

# Wrong: Race condition prone
if not os.path.exists('lockfile'):
    with open('lockfile', 'w') as f:
        f.write('locked')
    shutil.rmtree('temp_data')
    os.remove('lockfile')
```

### Why It's Wrong
Between checking file existence and performing operations, another process might modify the filesystem, leading to race conditions.

### The Fix
```python
import shutil
import tempfile
import os

# Correct: Use atomic operations and proper locking
def safe_cleanup(directory):
    """Safely clean up directory with proper locking."""
    lockfile = directory + '.lock'

    # Use exclusive file creation
    try:
        with open(lockfile, 'x') as f:  # 'x' mode fails if file exists
            f.write(str(os.getpid()))

        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
        finally:
            os.remove(lockfile)

    except FileExistsError:
        print(f"Directory {directory} is locked by another process")
    except OSError as e:
        print(f"Cleanup failed: {e}")
        # Don't remove lockfile if operation failed
```

## Summary

### Most Common Mistakes

1. **Using `copy()` instead of `copy2()`** - Lose metadata
2. **No error handling** - Unexpected crashes
3. **Using `rmtree()` without confirmation** - Data loss
4. **Inconsistent path types** - Platform issues
5. **No disk space checking** - Operation failures
6. **Wrong assumptions about `move()`** - Performance issues
7. **Not using `ignore` in `copytree()`** - Unwanted file copying
8. **Archive format confusion** - Extraction failures
9. **Using `shutil` for path operations** - Code confusion
10. **Symlink handling issues** - Broken links

### Prevention Strategies

- **Read the documentation** carefully for each function
- **Test operations** on small datasets first
- **Use type hints** and consistent parameter types
- **Implement comprehensive error handling**
- **Add logging** for debugging and monitoring
- **Write unit tests** for file operations
- **Use context managers** for resource management
- **Validate inputs** before operations

By avoiding these common mistakes, you'll write more robust and reliable code using the `shutil` module.
