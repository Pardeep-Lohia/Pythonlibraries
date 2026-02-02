# What All Can Be Done with pathlib?

The `pathlib` library provides a comprehensive set of capabilities for handling filesystem paths and operations in Python. This document outlines all the major things developers can accomplish using `pathlib`, organized by functional categories.

## Path Creation and Manipulation

### Creating Path Objects
**What it enables**: Instantiate Path objects from strings, other paths, or system-specific locations.

**Why it's useful**: Provides a consistent, object-oriented way to represent filesystem paths across platforms.

**Real-world scenario**: Building configuration file paths that work on any operating system.
```python
from pathlib import Path

# From string
config_path = Path('/etc/myapp/config.ini')

# From home directory
user_config = Path.home() / '.myapp' / 'config.ini'

# From current working directory
project_root = Path.cwd() / 'src'
```

### Path Joining and Composition
**What it enables**: Combine path components using the `/` operator or `joinpath()` method.

**Why it's useful**: Eliminates platform-specific path separator concerns and prevents common concatenation errors.

**Real-world scenario**: Constructing file paths for a document management system.
```python
base_path = Path('/documents')
user_folder = base_path / 'users' / 'john_doe' / 'reports'
final_path = user_folder / 'monthly_report.pdf'
```

### Path Modification
**What it enables**: Change path components like name, suffix, or parent directory.

**Why it's useful**: Easily create related paths (backups, versions, etc.) without string manipulation.

**Real-world scenario**: Creating backup files with timestamps.
```python
original = Path('/data/file.txt')
backup = original.with_suffix('.bak')
timestamped = original.with_name(f"{original.stem}_backup_{timestamp}{original.suffix}")
```

## File and Directory Inspection

### Existence and Type Checking
**What it enables**: Check if paths exist, and determine if they point to files or directories.

**Why it's useful**: Validate paths before performing operations, preventing errors.

**Real-world scenario**: Verifying configuration files exist before loading application settings.
```python
config_file = Path('/etc/myapp/config.json')
if config_file.exists():
    if config_file.is_file():
        # Load configuration
        pass
    elif config_file.is_dir():
        # Handle directory case
        pass
```

### Path Properties and Components
**What it enables**: Access path components like name, parent, suffix, stem, etc.

**Why it's useful**: Extract meaningful information from paths for processing or display.

**Real-world scenario**: Organizing files by type in a file manager application.
```python
file_path = Path('/documents/important_report.pdf')
print(f"Name: {file_path.name}")        # 'important_report.pdf'
print(f"Stem: {file_path.stem}")        # 'important_report'
print(f"Suffix: {file_path.suffix}")    # '.pdf'
print(f"Parent: {file_path.parent}")    # PosixPath('/documents')
```

### File Metadata Access
**What it enables**: Get file statistics like size, modification time, permissions.

**Why it's useful**: Make decisions based on file characteristics without additional system calls.

**Real-world scenario**: Implementing a file cleanup utility that removes old temporary files.
```python
temp_file = Path('/tmp/cache.dat')
if temp_file.exists():
    stat = temp_file.stat()
    size_mb = stat.st_size / (1024 * 1024)
    age_days = (time.time() - stat.st_mtime) / (24 * 3600)
    if size_mb > 100 or age_days > 7:
        temp_file.unlink()
```

## Reading and Writing Files

### Text File Operations
**What it enables**: Read and write text files with automatic encoding handling.

**Why it's useful**: Simplifies common file I/O operations with sensible defaults.

**Real-world scenario**: Reading configuration files and writing log entries.
```python
config_path = Path('config.ini')
if config_path.exists():
    content = config_path.read_text(encoding='utf-8')
    # Process configuration

log_path = Path('app.log')
log_entry = f"{datetime.now()}: Application started\n"
log_path.write_text(log_entry, encoding='utf-8', mode='a')
```

### Binary File Operations
**What it enables**: Read and write binary data to files.

**Why it's useful**: Handle non-text files like images, executables, or serialized data.

**Real-world scenario**: Downloading and caching binary assets.
```python
image_path = Path('cache') / 'logo.png'
if not image_path.exists():
    image_data = requests.get('https://example.com/logo.png').content
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(image_data)
```

## Directory Traversal and Globbing

### Directory Listing
**What it enables**: Iterate over files and subdirectories in a directory.

**Why it's useful**: Process all files in a directory tree systematically.

**Real-world scenario**: Building a file index for a search application.
```python
def index_files(directory: Path):
    for item in directory.iterdir():
        if item.is_file():
            print(f"File: {item}")
        elif item.is_dir():
            print(f"Directory: {item}")
            index_files(item)  # Recursive

index_files(Path('/documents'))
```

### Pattern-Based File Search
**What it enables**: Find files matching glob patterns using `glob()` and `rglob()`.

**Why it's useful**: Locate files by name patterns without manual filtering.

**Real-world scenario**: Finding all Python files in a project for linting.
```python
project_root = Path('/myproject')

# Find all Python files in current directory
python_files = list(project_root.glob('*.py'))

# Find all Python files recursively
all_python_files = list(project_root.rglob('*.py'))

# Find all log files
log_files = list(project_root.rglob('*.log'))
```

## Directory Operations

### Directory Creation
**What it enables**: Create directories, including parent directories if needed.

**Why it's useful**: Ensure directory structures exist before creating files.

**Real-world scenario**: Setting up application data directories on first run.
```python
app_data_dir = Path.home() / '.myapp' / 'data'
app_data_dir.mkdir(parents=True, exist_ok=True)
```

### Directory Removal
**What it enables**: Remove empty directories or entire directory trees.

**Why it's useful**: Clean up temporary or unused directory structures.

**Real-world scenario**: Removing old backup directories after successful operations.
```python
backup_dir = Path('/backups/old_version')
if backup_dir.exists() and backup_dir.is_dir():
    # Remove directory and all contents
    import shutil
    shutil.rmtree(backup_dir)
    # Or for empty directories only:
    # backup_dir.rmdir()
```

## File Operations

### File Creation and Modification
**What it enables**: Create empty files, rename files, change permissions.

**Why it's useful**: Basic file management operations for application workflows.

**Real-world scenario**: Creating lock files for process synchronization.
```python
lock_file = Path('/tmp/myapp.lock')
lock_file.touch()  # Create empty file

# Rename file
new_name = lock_file.with_name('myapp.lock.backup')
lock_file.rename(new_name)
```

### File Deletion
**What it enables**: Remove files from the filesystem.

**Why it's useful**: Clean up temporary files or remove obsolete data.

**Real-world scenario**: Cleaning up temporary upload files after processing.
```python
temp_upload = Path('/tmp/upload_12345.dat')
if temp_upload.exists():
    temp_upload.unlink()
```

## Cross-Platform Compatibility

### Platform-Aware Path Handling
**What it enables**: Automatic handling of OS-specific path conventions.

**Why it's useful**: Write code that works identically on Windows, macOS, and Linux.

**Real-world scenario**: Developing a cross-platform file synchronization tool.
```python
# Works on all platforms
config_dir = Path.home() / '.config' / 'myapp'
data_file = config_dir / 'data.json'

# pathlib handles:
# - Path separators (/ vs \)
# - Drive letters (Windows)
# - Case sensitivity differences
```

### System Path Access
**What it enables**: Access system-specific directories like home, temp, etc.

**Why it's useful**: Locate standard directories without hardcoding paths.

**Real-world scenario**: Finding appropriate locations for user data and cache files.
```python
from pathlib import Path

# User-specific directories
home = Path.home()
desktop = home / 'Desktop'
documents = home / 'Documents'

# System directories
temp_dir = Path('/tmp')  # Unix
# Or use platform-independent approach:
import tempfile
temp_dir = Path(tempfile.gettempdir())
```

## Advanced Path Operations

### Path Resolution and Normalization
**What it enables**: Resolve relative paths, eliminate `.` and `..` components.

**Why it's useful**: Convert relative paths to absolute and canonical forms.

**Real-world scenario**: Resolving symlinks and relative paths in configuration files.
```python
# Resolve relative paths
relative_path = Path('../config/settings.json')
absolute_path = relative_path.resolve()

# Handle symlinks
symlink_path = Path('/home/user/docs_link')
real_path = symlink_path.resolve()
```

### Path Comparison and Sorting
**What it enables**: Compare paths for equality, ordering, and containment.

**Why it's useful**: Sort file lists or check path relationships.

**Real-world scenario**: Sorting files by name for consistent processing order.
```python
files = [Path('c.txt'), Path('a.txt'), Path('b.txt')]
files.sort()  # Alphabetical sorting
print(files)  # [PosixPath('a.txt'), PosixPath('b.txt'), PosixPath('c.txt')]

# Check if path is within another
base_dir = Path('/documents')
file_path = Path('/documents/reports/annual.pdf')
print(file_path.is_relative_to(base_dir))  # True
```

## Integration with Other Libraries

### Compatibility with Standard Library
**What it enables**: Use Path objects with functions expecting strings.

**Why it's useful**: Seamless integration with existing code and libraries.

**Real-world scenario**: Using pathlib with JSON configuration files and standard I/O.
```python
import json
from pathlib import Path

config_path = Path('config.json')

# Read JSON
with open(config_path, 'r') as f:  # open() accepts Path
    config = json.load(f)

# Write JSON
output_path = Path('output.json')
with open(output_path, 'w') as f:
    json.dump(data, f)
```

### Working with shutil and Other Modules
**What it enables**: Use Path objects with shutil, os, and other filesystem modules.

**Why it's useful**: Combine high-level pathlib operations with specialized utilities.

**Real-world scenario**: Copying directory trees while preserving metadata.
```python
import shutil
from pathlib import Path

src_dir = Path('/source/project')
dst_dir = Path('/backup/project')

# Copy entire directory tree
shutil.copytree(src_dir, dst_dir)

# pathlib + shutil combination
for file_path in src_dir.rglob('*.py'):
    relative_path = file_path.relative_to(src_dir)
    dst_file = dst_dir / relative_path
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, dst_file)  # Preserve metadata
```

## Error Handling and Validation

### Robust Path Operations
**What it enables**: Handle filesystem errors gracefully with Path objects.

**Why it's useful**: Write more reliable code that handles edge cases.

**Real-world scenario**: Safely attempting file operations with proper error handling.
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

content = safe_read_file(Path('config.txt'))
```

## Summary

`pathlib` enables developers to perform virtually all filesystem operations in a clean, object-oriented, and cross-platform manner. From basic path manipulation to complex file system traversals, `pathlib` provides a comprehensive toolkit that eliminates the need for string-based path handling. Its integration with Python's ecosystem and focus on usability make it the preferred choice for modern Python filesystem operations.

Key capabilities include:
- Path creation, joining, and modification
- File and directory inspection and manipulation
- Reading/writing files (text and binary)
- Directory traversal and pattern matching
- Cross-platform compatibility
- Integration with other Python libraries
- Robust error handling

By using `pathlib`, developers can write more maintainable, readable, and reliable filesystem code that works consistently across different operating systems.
