3+# Directory Traversal

## Overview
Directory traversal functions allow you to walk through directory trees, visit files and subdirectories, and perform operations on them. The `os` module provides `os.walk()` and `os.scandir()` for efficient directory traversal.

## Core Traversal Functions

### `os.walk(top, topdown=True, onerror=None, followlinks=False)` - Directory Tree Walk
**Purpose**: Generates the file names in a directory tree by walking the tree either top-down or bottom-up.

**Parameters**:
- `top`: Directory to start walking from
- `topdown`: If True, walk directories top-down; if False, bottom-up
- `onerror`: Function called when walk encounters an error
- `followlinks`: If True, follow symbolic links

**Return Value**: Generator yielding (dirpath, dirnames, filenames) tuples

**Examples**:
```python
import os

# Basic directory walk
for dirpath, dirnames, filenames in os.walk('/home/user/documents'):
    print(f"Directory: {dirpath}")
    print(f"Subdirectories: {dirnames}")
    print(f"Files: {filenames}")
    print()

# Count all files in a directory tree
def count_files(directory):
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        total_files += len(filenames)
    return total_files

file_count = count_files('/home/user')
print(f"Total files: {file_count}")
```

### `os.scandir(path='.')` - Directory Iterator
**Purpose**: Returns an iterator of `DirEntry` objects for the directory.

**Return Value**: Iterator of `DirEntry` objects with methods like `name`, `path`, `is_file()`, `is_dir()`, `stat()`

**Examples**:
```python
import os

# Efficient directory listing
with os.scandir('/home/user') as entries:
    for entry in entries:
        if entry.is_file():
            print(f"File: {entry.name}, Size: {entry.stat().st_size}")
        elif entry.is_dir():
            print(f"Directory: {entry.name}")
```

## Advanced Traversal Patterns

### Filtering During Traversal
```python
import os

def find_files_by_extension(directory, extension):
    """Find all files with a specific extension."""
    matches = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                matches.append(os.path.join(dirpath, filename))
    return matches

# Find all Python files
python_files = find_files_by_extension('/home/user/project', '.py')
print(f"Found {len(python_files)} Python files")
```

### Size-Based File Discovery
```python
import os

def find_large_files(directory, min_size_mb=100):
    """Find files larger than specified size."""
    large_files = []
    min_size_bytes = min_size_mb * 1024 * 1024

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if os.path.getsize(filepath) > min_size_bytes:
                    large_files.append((filepath, os.path.getsize(filepath)))
            except OSError:
                continue

    return sorted(large_files, key=lambda x: x[1], reverse=True)

# Find files over 50MB
large_files = find_large_files('/home/user', 50)
for filepath, size in large_files[:10]:  # Top 10
    print(f"{filepath}: {size / (1024*1024):.1f} MB")
```

### Recent File Discovery
```python
import os
import time

def find_recent_files(directory, hours=24):
    """Find files modified within the last N hours."""
    cutoff_time = time.time() - (hours * 60 * 60)
    recent_files = []

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if os.path.getmtime(filepath) > cutoff_time:
                    recent_files.append((filepath, os.path.getmtime(filepath)))
            except OSError:
                continue

    return sorted(recent_files, key=lambda x: x[1], reverse=True)

# Find files modified in last 2 hours
recent = find_recent_files('/home/user/documents', 2)
for filepath, mtime in recent:
    print(f"{filepath}: {time.ctime(mtime)}")
```

### Directory Tree Analysis
```python
import os
from collections import defaultdict

def analyze_directory_tree(directory):
    """Analyze directory structure and file types."""
    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'file_types': defaultdict(int),
        'depth_distribution': defaultdict(int),
        'largest_files': []
    }

    for dirpath, dirnames, filenames in os.walk(directory):
        stats['total_dirs'] += len(dirnames)

        # Calculate depth
        rel_path = os.path.relpath(dirpath, directory)
        depth = 0 if rel_path == '.' else len(rel_path.split(os.sep))
        stats['depth_distribution'][depth] += 1

        for filename in filenames:
            stats['total_files'] += 1

            # File type analysis
            _, ext = os.path.splitext(filename)
            stats['file_types'][ext.lower()] += 1

            # Track largest files
            filepath = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(filepath)
                stats['largest_files'].append((filepath, size))
                stats['largest_files'].sort(key=lambda x: x[1], reverse=True)
                stats['largest_files'] = stats['largest_files'][:10]  # Keep top 10
            except OSError:
                continue

    return stats

# Analyze project directory
stats = analyze_directory_tree('/home/user/project')
print(f"Total files: {stats['total_files']}")
print(f"Total directories: {stats['total_dirs']}")
print(f"File types: {dict(stats['file_types'])}")
print("Largest files:")
for filepath, size in stats['largest_files']:
    print(f"  {filepath}: {size / 1024:.1f} KB")
```

## Error Handling in Traversal

### Robust Traversal with Error Handling
```python
import os

def walk_with_error_handling(directory):
    """Walk directory tree with proper error handling."""
    def onerror(error):
        print(f"Error accessing {error.filename}: {error.strerror}")
        # Could log to file, send notification, etc.

    try:
        for dirpath, dirnames, filenames in os.walk(directory, onerror=onerror):
            # Skip directories that cause permission errors
            dirnames[:] = [d for d in dirnames if os.access(os.path.join(dirpath, d), os.R_OK)]

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    # Process file
                    stat_info = os.stat(filepath)
                    yield filepath, stat_info
                except OSError as e:
                    print(f"Error processing {filepath}: {e}")
                    continue

    except OSError as e:
        print(f"Error walking directory {directory}: {e}")

# Usage
for filepath, stat_info in walk_with_error_handling('/var/log'):
    print(f"Processing: {filepath}")
```

### Memory-Efficient Large Directory Processing
```python
import os

def process_large_directory(directory, batch_size=1000):
    """Process large directories in batches to manage memory."""
    file_batch = []

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_batch.append(filepath)

            # Process in batches
            if len(file_batch) >= batch_size:
                process_file_batch(file_batch)
                file_batch = []  # Clear batch

    # Process remaining files
    if file_batch:
        process_file_batch(file_batch)

def process_file_batch(filepaths):
    """Process a batch of files."""
    for filepath in filepaths:
        try:
            # Perform file processing
            size = os.path.getsize(filepath)
            print(f"Processed: {filepath} ({size} bytes)")
        except OSError as e:
            print(f"Error processing {filepath}: {e}")

# Usage
process_large_directory('/large/dataset', batch_size=500)
```

## Performance Optimization

### Efficient File Type Checking
```python
import os

def efficient_file_type_check(directory):
    """Use os.scandir for efficient file type checking."""
    file_count = 0
    dir_count = 0
    total_size = 0

    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    file_count += 1
                    try:
                        total_size += entry.stat().st_size
                    except OSError:
                        pass
                elif entry.is_dir():
                    dir_count += 1
    except OSError as e:
        print(f"Error scanning directory: {e}")
        return None

    return {
        'files': file_count,
        'directories': dir_count,
        'total_size': total_size
    }

# Usage
stats = efficient_file_type_check('/home/user')
if stats:
    print(f"Files: {stats['files']}, Directories: {stats['directories']}")
```

### Selective Directory Traversal
```python
import os

def selective_walk(directory, include_patterns=None, exclude_patterns=None):
    """Walk directory with selective inclusion/exclusion."""
    import fnmatch

    for dirpath, dirnames, filenames in os.walk(directory):
        # Filter directories
        if exclude_patterns:
            dirnames[:] = [d for d in dirnames
                          if not any(fnmatch.fnmatch(d, pattern)
                                   for pattern in exclude_patterns)]

        # Filter files
        filtered_files = []
        for filename in filenames:
            if include_patterns:
                if any(fnmatch.fnmatch(filename, pattern)
                      for pattern in include_patterns):
                    filtered_files.append(filename)
            else:
                filtered_files.append(filename)

        if filtered_files:
            yield dirpath, filtered_files

# Usage
# Include only Python files, exclude __pycache__ directories
for dirpath, files in selective_walk(
    '/home/user/project',
    include_patterns=['*.py'],
    exclude_patterns=['__pycache__']
):
    print(f"{dirpath}: {len(files)} Python files")
```

## Cross-Platform Considerations

### Handling Different Path Separators
```python
import os

def cross_platform_walk(directory):
    """Walk directory with cross-platform path handling."""
    for dirpath, dirnames, filenames in os.walk(directory):
        # Normalize paths
        dirpath = os.path.normpath(dirpath)

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Use normalized path for consistency
            yield os.path.normpath(filepath)

# Usage
for filepath in cross_platform_walk('/home/user'):
    print(filepath)  # Will use correct separators for platform
```

### Permission-Aware Traversal
```python
import os

def permission_aware_walk(directory):
    """Walk directory tree respecting permissions."""
    for dirpath, dirnames, filenames in os.walk(directory):
        # Remove directories we can't access
        dirnames[:] = [d for d in dirnames
                      if os.access(os.path.join(dirpath, d), os.R_OK)]

        # Process accessible files
        accessible_files = []
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.access(filepath, os.R_OK):
                accessible_files.append(filename)

        if accessible_files:
            yield dirpath, accessible_files

# Usage
for dirpath, files in permission_aware_walk('/var'):
    print(f"Accessible in {dirpath}: {len(files)} files")
```

## Best Practices

### 1. Use `os.scandir()` for Better Performance
```python
# Preferred for performance
with os.scandir(directory) as entries:
    for entry in entries:
        if entry.is_file():
            process_file(entry.path)

# Less efficient
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
        process_file(filepath)
```

### 2. Handle Permissions and Errors Gracefully
```python
def safe_walk(directory):
    """Walk directory safely handling permissions."""
    def onerror(error):
        print(f"Access denied: {error.filename}")

    try:
        for dirpath, dirnames, filenames in os.walk(directory, onerror=onerror):
            # Process what we can access
            yield dirpath, dirnames, filenames
    except PermissionError:
        print(f"Cannot access directory: {directory}")

for dirpath, dirnames, filenames in safe_walk('/restricted/area'):
    print(f"Processing: {dirpath}")
```

### 3. Use Top-Down vs Bottom-Up Appropriately
```python
# Top-down: Process parents before children
for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
    # Can modify dirnames to control traversal
    dirnames[:] = [d for d in dirnames if not d.startswith('.')]

# Bottom-up: Process children before parents
for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
    # Useful for cleanup operations
    pass
```

### 4. Implement Progress Tracking for Long Operations
```python
import os

def walk_with_progress(directory, progress_callback=None):
    """Walk directory with progress reporting."""
    total_processed = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Process file
            process_file(filepath)
            total_processed += 1

            if progress_callback and total_processed % 100 == 0:
                progress_callback(total_processed, filepath)

    return total_processed

def progress_callback(count, current_file):
    print(f"Processed {count} files, currently: {current_file}")

total = walk_with_progress('/large/dataset', progress_callback)
print(f"Total files processed: {total}")
```

### 5. Avoid Infinite Loops with Symbolic Links
```python
# Safe traversal that doesn't follow symlinks
for dirpath, dirnames, filenames in os.walk(directory, followlinks=False):
    # Process without following symlinks
    pass

# Or detect symlink cycles
visited = set()
for dirpath, dirnames, filenames in os.walk(directory):
    real_path = os.path.realpath(dirpath)
    if real_path in visited:
        # Cycle detected, skip
        dirnames[:] = []
        continue
    visited.add(real_path)
```

These functions provide powerful capabilities for traversing and analyzing directory structures while handling edge cases and performance considerations.
