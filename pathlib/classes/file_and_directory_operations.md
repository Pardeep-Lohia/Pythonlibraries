# File and Directory Operations in pathlib

## Overview

The `pathlib` library provides comprehensive methods for file and directory operations through its Path classes. These operations combine the object-oriented path handling with practical filesystem interactions, making common file management tasks more intuitive and less error-prone.

## File Operations

### Creating and Writing Files

#### Creating Empty Files
```python
from pathlib import Path

# Create an empty file or update timestamp if it exists
empty_file = Path('empty.txt')
empty_file.touch()

# Create with specific permissions (Unix-like systems)
empty_file.touch(mode=0o644)
```

#### Writing Text Content
```python
file_path = Path('document.txt')

# Write text to file
file_path.write_text('Hello, World!', encoding='utf-8')

# Append to existing file
with open(file_path, 'a', encoding='utf-8') as f:
    f.write('\nAppended text')

# Overwrite file with new content
file_path.write_text('New content', encoding='utf-8')
```

#### Writing Binary Content
```python
binary_file = Path('data.bin')

# Write binary data
binary_data = b'\x00\x01\x02\x03'
binary_file.write_bytes(binary_data)

# Copy binary file
source = Path('image.png')
destination = Path('image_copy.png')
destination.write_bytes(source.read_bytes())
```

### Reading Files

#### Reading Text Files
```python
text_file = Path('document.txt')

# Read entire file as string
content = text_file.read_text(encoding='utf-8')
print(content)

# Read with specific encoding
content_utf16 = text_file.read_text(encoding='utf-16')

# Read lines as list
lines = text_file.read_text().splitlines()
for line in lines:
    print(line)
```

#### Reading Binary Files
```python
binary_file = Path('data.bin')

# Read entire file as bytes
data = binary_file.read_bytes()
print(f"Read {len(data)} bytes")
```

### File Modification Operations

#### Renaming Files
```python
original = Path('old_name.txt')
renamed = original.with_name('new_name.txt')

# Rename the file
original.rename(renamed)
```

#### Moving Files
```python
source = Path('file.txt')
destination = Path('/tmp/file.txt')

# Move file to new location
source.rename(destination)
```

#### Copying Files
```python
import shutil

source = Path('source.txt')
destination = Path('destination.txt')

# Copy file
shutil.copy(source, destination)

# Copy with metadata preservation
shutil.copy2(source, destination)
```

### File Deletion
```python
file_to_delete = Path('temp.txt')

# Delete file
file_to_delete.unlink()

# Delete only if exists (no error if missing)
file_to_delete.unlink(missing_ok=True)
```

## Directory Operations

### Creating Directories

#### Creating Single Directory
```python
new_dir = Path('/tmp/new_directory')
new_dir.mkdir()
```

#### Creating Nested Directories
```python
nested_dir = Path('/tmp/parent/child/grandchild')
nested_dir.mkdir(parents=True)
```

#### Safe Directory Creation
```python
safe_dir = Path('/tmp/safe_dir')
safe_dir.mkdir(parents=True, exist_ok=True)  # No error if exists
```

### Listing Directory Contents

#### Basic Directory Listing
```python
directory = Path('/home/user/documents')

# List all items
for item in directory.iterdir():
    print(f"{'File' if item.is_file() else 'Directory'}: {item.name}")
```

#### Filtering Directory Contents
```python
# List only files
files = [item for item in directory.iterdir() if item.is_file()]

# List only directories
dirs = [item for item in directory.iterdir() if item.is_dir()]

# List by pattern
txt_files = list(directory.glob('*.txt'))
```

### Recursive Directory Traversal

#### Walking Directory Tree
```python
def walk_directory(directory: Path, prefix: str = ""):
    """Recursively walk directory and print structure."""
    try:
        items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "

            print(f"{prefix}{connector}{item.name}")

            if item.is_dir():
                extension = "    " if is_last else "│   "
                walk_directory(item, prefix + extension)
    except PermissionError:
        print(f"{prefix}└── [Permission Denied]")

# Usage
walk_directory(Path('.'))
```

#### Finding Files Recursively
```python
project_root = Path('/myproject')

# Find all Python files
python_files = list(project_root.rglob('*.py'))

# Find all files in src directory
src_files = list(project_root.glob('src/**/*'))

# Find files by multiple patterns
code_files = []
for pattern in ['*.py', '*.js', '*.java']:
    code_files.extend(project_root.rglob(pattern))
```

### Directory Deletion

#### Removing Empty Directories
```python
empty_dir = Path('empty_directory')
empty_dir.rmdir()  # Only works if directory is empty
```

#### Removing Directory Trees
```python
import shutil

dir_tree = Path('directory_to_remove')
if dir_tree.exists():
    shutil.rmtree(dir_tree)  # Removes entire directory tree
```

## Advanced File Operations

### Working with File Permissions

#### Checking Permissions
```python
import stat

file_path = Path('script.py')
mode = file_path.stat().st_mode

print(f"Owner read: {bool(mode & stat.S_IRUSR)}")
print(f"Owner write: {bool(mode & stat.S_IWUSR)}")
print(f"Owner execute: {bool(mode & stat.S_IXUSR)}")
print(f"Group read: {bool(mode & stat.S_IRGRP)}")
print(f"Others read: {bool(mode & stat.S_IROTH)}")
```

#### Changing Permissions
```python
# Make file executable
current_mode = file_path.stat().st_mode
executable_mode = current_mode | 0o111  # Add execute for all
file_path.chmod(executable_mode)

# Set specific permissions
file_path.chmod(0o755)  # rwxr-xr-x
```

### File Metadata Operations

#### Getting File Information
```python
file_path = Path('document.txt')
stat_info = file_path.stat()

print(f"Size: {stat_info.st_size} bytes")
print(f"Created: {stat_info.st_ctime}")
print(f"Modified: {stat_info.st_mtime}")
print(f"Accessed: {stat_info.st_atime}")

# Human-readable size
def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

print(f"Size: {format_size(stat_info.st_size)}")
```

#### File Timestamps
```python
from datetime import datetime

mod_time = datetime.fromtimestamp(stat_info.st_mtime)
print(f"Last modified: {mod_time}")

# Update file timestamp
file_path.touch()  # Updates modification time to now
```

### Working with Symlinks

#### Creating Symlinks
```python
target = Path('original.txt')
link = Path('link.txt')

# Create symbolic link
link.symlink_to(target)

# Create hard link
link.hardlink_to(target)
```

#### Resolving Symlinks
```python
link_path = Path('link.txt')

# Get target of symlink
real_path = link_path.resolve()
print(f"Points to: {real_path}")

# Check if path is a symlink
print(f"Is symlink: {link_path.is_symlink()}")
```

## Batch Operations

### Processing Multiple Files
```python
def process_text_files(directory: Path):
    """Process all text files in a directory."""
    for txt_file in directory.glob('*.txt'):
        try:
            content = txt_file.read_text(encoding='utf-8')
            # Process content
            processed = content.upper()

            # Write back
            txt_file.write_text(processed, encoding='utf-8')
            print(f"Processed: {txt_file.name}")
        except UnicodeDecodeError:
            print(f"Skipped (not UTF-8): {txt_file.name}")
        except PermissionError:
            print(f"Skipped (permission denied): {txt_file.name}")

process_text_files(Path('/documents'))
```

### File Organization
```python
def organize_by_extension(source_dir: Path, dest_dir: Path):
    """Organize files into subdirectories by extension."""
    for file_path in source_dir.rglob('*'):
        if file_path.is_file():
            ext = file_path.suffix[1:]  # Remove the dot
            if not ext:
                ext = 'no_extension'

            # Create extension directory
            ext_dir = dest_dir / ext
            ext_dir.mkdir(exist_ok=True)

            # Move file
            new_path = ext_dir / file_path.name
            file_path.rename(new_path)
            print(f"Moved {file_path.name} to {ext}/")

# Usage
organize_by_extension(Path('/downloads'), Path('/organized'))
```

### Backup System
```python
def create_backups(source_dir: Path, backup_dir: Path):
    """Create backups of all files in source directory."""
    from datetime import datetime
    import shutil

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_subdir = backup_dir / f"backup_{timestamp}"
    backup_subdir.mkdir(parents=True)

    for file_path in source_dir.rglob('*'):
        if file_path.is_file():
            # Calculate relative path
            relative_path = file_path.relative_to(source_dir)
            backup_path = backup_subdir / relative_path

            # Create parent directories
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            shutil.copy2(file_path, backup_path)
            print(f"Backed up: {relative_path}")

create_backups(Path('/important'), Path('/backups'))
```

## Error Handling

### Safe File Operations
```python
def safe_read_file(file_path: Path) -> str:
    """Safely read a file with comprehensive error handling."""
    try:
        if not file_path.exists():
            return "File does not exist"

        if not file_path.is_file():
            return "Path is not a file"

        return file_path.read_text(encoding='utf-8')
    except PermissionError:
        return "Permission denied"
    except UnicodeDecodeError:
        return "File is not valid UTF-8 text"
    except OSError as e:
        return f"OS error: {e}"

def safe_write_file(file_path: Path, content: str) -> bool:
    """Safely write content to a file."""
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        file_path.write_text(content, encoding='utf-8')
        return True
    except PermissionError:
        print(f"Permission denied: {file_path}")
        return False
    except OSError as e:
        print(f"Write failed: {e}")
        return False
```

### Directory Operation Safety
```python
def safe_create_directory(dir_path: Path) -> bool:
    """Safely create a directory."""
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        print(f"Permission denied: {dir_path}")
        return False
    except FileExistsError:
        # This shouldn't happen with exist_ok=True, but just in case
        print(f"Directory already exists: {dir_path}")
        return True
    except OSError as e:
        print(f"Failed to create directory: {e}")
        return False
```

## Performance Considerations

### Efficient File Processing
```python
# Inefficient: Reading entire file into memory
def bad_process_large_file(file_path: Path):
    content = file_path.read_text()  # Loads entire file
    lines = content.splitlines()
    for line in lines:
        # Process line
        pass

# Efficient: Process line by line
def good_process_large_file(file_path: Path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Process line
            pass
```

### Minimizing Filesystem Calls
```python
# Inefficient: Multiple stat calls
def bad_get_file_sizes(directory: Path):
    sizes = {}
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            sizes[file_path] = file_path.stat().st_size
    return sizes

# Efficient: Single stat call per file
def good_get_file_sizes(directory: Path):
    sizes = {}
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            try:
                stat_info = file_path.stat()
                sizes[file_path] = stat_info.st_size
            except OSError:
                # Skip inaccessible files
                continue
    return sizes
```

## Cross-Platform Considerations

### Path Separator Handling
```python
# pathlib handles separators automatically
path = Path('folder') / 'subfolder' / 'file.txt'
print(path)  # Correct separator for current platform

# Manual separator handling (avoid)
import os
bad_path = 'folder' + os.sep + 'subfolder' + os.sep + 'file.txt'
```

### Permission Handling
```python
# Cross-platform permission checking
def is_readable(file_path: Path) -> bool:
    try:
        with open(file_path, 'r'):
            return True
    except (PermissionError, OSError):
        return False

def is_writable(file_path: Path) -> bool:
    try:
        # Try to open for writing (will create if doesn't exist)
        if file_path.exists():
            with open(file_path, 'r+'):
                return True
        else:
            with open(file_path, 'w'):
                file_path.unlink()  # Clean up
                return True
    except (PermissionError, OSError):
        return False
```

## Best Practices

### Use Context Managers for File Operations
```python
# Good: Automatic cleanup
with open(Path('file.txt'), 'r', encoding='utf-8') as f:
    content = f.read()

# Avoid: Manual file closing
f = open(Path('file.txt'), 'r', encoding='utf-8')
try:
    content = f.read()
finally:
    f.close()
```

### Validate Operations Before Execution
```python
def safe_move_file(src: Path, dst: Path) -> bool:
    """Safely move a file with validation."""
    if not src.exists():
        print(f"Source does not exist: {src}")
        return False

    if not src.is_file():
        print(f"Source is not a file: {src}")
        return False

    if dst.exists():
        print(f"Destination already exists: {dst}")
        return False

    try:
        # Ensure destination directory exists
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        return True
    except OSError as e:
        print(f"Move failed: {e}")
        return False
```

### Handle Large Files Appropriately
```python
def process_large_file(file_path: Path, chunk_size: int = 8192):
    """Process a large file in chunks."""
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                # Process chunk
                process_chunk(chunk)
    except MemoryError:
        print("File too large to process")
    except OSError as e:
        print(f"Error reading file: {e}")

def process_chunk(chunk: bytes):
    """Process a chunk of data."""
    # Implement your chunk processing logic
    pass
```

## Summary

`pathlib` provides a comprehensive set of file and directory operations that combine object-oriented path handling with practical filesystem interactions:

**File Operations:**
- Creating, reading, writing files (text and binary)
- Renaming, moving, copying files
- File permission management
- Symlink handling

**Directory Operations:**
- Creating directories (single and nested)
- Listing and traversing directories
- Recursive file searching
- Directory removal

**Advanced Features:**
- Batch file processing
- File organization
- Backup systems
- Cross-platform compatibility
- Comprehensive error handling

The key advantages of using `pathlib` for file operations include:
- **Consistency**: Same API across all platforms
- **Safety**: Built-in validation and error handling
- **Readability**: Code reads like natural language
- **Integration**: Works seamlessly with other Python libraries

By using Path objects consistently, developers can write more reliable, maintainable, and cross-platform file handling code.
