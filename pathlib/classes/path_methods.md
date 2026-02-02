# Path Methods in pathlib

## Overview of Path Methods

The `pathlib` library provides a rich set of methods for manipulating and inspecting Path objects. These methods are divided into categories based on their functionality: path construction, inspection, manipulation, and filesystem operations.

## Path Construction Methods

### Creating Path Objects
```python
from pathlib import Path

# From string
path1 = Path('/home/user/file.txt')

# From multiple components
path2 = Path('home', 'user', 'file.txt')

# From another Path
path3 = Path(path1)

# Special constructors
home = Path.home()        # User's home directory
cwd = Path.cwd()          # Current working directory
```

### Path Joining and Building
```python
base = Path('/home/user')

# Using / operator (recommended)
documents = base / 'Documents'
file_path = documents / 'report.pdf'

# Using joinpath() method
file_path2 = base.joinpath('Documents', 'report.pdf')

# Both approaches produce the same result
assert file_path == file_path2
```

## Path Inspection Methods

### Basic Properties
```python
path = Path('/home/user/documents/report.pdf')

# Component access
print(path.name)      # 'report.pdf'
print(path.stem)      # 'report'
print(path.suffix)    # '.pdf'
print(path.suffixes)  # ['.pdf']
print(path.parent)    # PosixPath('/home/user/documents')
print(path.parts)     # ('/', 'home', 'user', 'documents', 'report.pdf')

# Path type checks
print(path.is_absolute())  # True
print(path.is_relative_to(Path('/home/user')))  # True
```

### Existence and Type Checking
```python
path = Path('/home/user/file.txt')

print(path.exists())   # True if file exists
print(path.is_file())  # True if it's a file
print(path.is_dir())   # True if it's a directory
print(path.is_symlink())  # True if it's a symbolic link
```

### File Metadata
```python
if path.exists():
    stat = path.stat()
    print(f"Size: {stat.st_size} bytes")
    print(f"Modified: {stat.st_mtime}")
    print(f"Permissions: {oct(stat.st_mode)}")

    # Human-readable size
    size_mb = stat.st_size / (1024 * 1024)
    print(f"Size: {size_mb:.2f} MB")
```

## Path Manipulation Methods

### Changing Path Components
```python
original = Path('/home/user/old_name.txt')

# Change name
renamed = original.with_name('new_name.txt')
print(renamed)  # PosixPath('/home/user/new_name.txt')

# Change suffix
backup = original.with_suffix('.bak')
print(backup)  # PosixPath('/home/user/old_name.bak')

# Change to different suffix
pdf_version = original.with_suffix('.pdf')
print(pdf_version)  # PosixPath('/home/user/old_name.pdf')
```

### Path Resolution
```python
# Resolve relative paths and symlinks
relative = Path('../config/settings.ini')
absolute = relative.resolve()
print(absolute)  # Absolute path

# Resolve symlinks
symlink = Path('/home/user/docs_link')
real_path = symlink.resolve()
print(real_path)  # Actual target path
```

### Relative Path Operations
```python
base = Path('/home/user/projects')
full = Path('/home/user/projects/myapp/src/main.py')

# Get relative path
relative = full.relative_to(base)
print(relative)  # PosixPath('myapp/src/main.py')

# Check if path is relative to another
print(full.is_relative_to(base))  # True
print(full.is_relative_to(Path('/tmp')))  # False
```

## Filesystem Operation Methods

### File Content Operations
```python
file_path = Path('data.txt')

# Read text
content = file_path.read_text(encoding='utf-8')
print(content)

# Write text
file_path.write_text('Hello, World!', encoding='utf-8')

# Read bytes
binary_data = file_path.read_bytes()

# Write bytes
file_path.write_bytes(b'Binary data')
```

### Directory Operations
```python
dir_path = Path('/tmp/new_directory')

# Create directory
dir_path.mkdir(parents=True, exist_ok=True)

# List contents
for item in dir_path.iterdir():
    print(f"{'File' if item.is_file() else 'Dir'}: {item.name}")

# Recursive listing
for py_file in Path('.').rglob('*.py'):
    print(f"Python file: {py_file}")
```

### File System Modification
```python
file_path = Path('old_name.txt')

# Rename/move file
new_path = file_path.with_name('new_name.txt')
file_path.rename(new_path)

# Create empty file
empty_file = Path('touch_me.txt')
empty_file.touch()

# Delete file
temp_file = Path('temp.txt')
temp_file.unlink(missing_ok=True)  # Won't error if file doesn't exist

# Delete directory (must be empty)
empty_dir = Path('empty_dir')
empty_dir.rmdir()
```

## Pattern Matching Methods

### Glob Operations
```python
project = Path('/myproject')

# Find all Python files in current directory
py_files = list(project.glob('*.py'))

# Find all Python files recursively
all_py_files = list(project.rglob('*.py'))

# Find all text files
text_files = list(project.rglob('*.txt'))

# Find all files in src directory
src_files = list(project.glob('src/**/*'))
```

### Advanced Pattern Matching
```python
# Match multiple patterns
patterns = ['*.py', '*.js', '*.html']
code_files = []
for pattern in patterns:
    code_files.extend(project.rglob(pattern))

# Case-insensitive matching (platform dependent)
# On case-insensitive filesystems (Windows, macOS)
readme_files = list(project.rglob('readme*'))

# Find files by name regardless of case
def find_files_insensitive(directory: Path, filename: str):
    return [f for f in directory.rglob('*') if f.name.lower() == filename.lower()]

readme_files = find_files_insensitive(project, 'readme.md')
```

## Path Comparison and Sorting

### Comparison Operations
```python
path1 = Path('/home/user/file1.txt')
path2 = Path('/home/user/file2.txt')
path3 = Path('/home/user/file1.txt')

print(path1 == path3)  # True
print(path1 == path2)  # False

# Paths are compared lexicographically
paths = [Path('c.txt'), Path('a.txt'), Path('b.txt')]
paths.sort()
print(paths)  # [PosixPath('a.txt'), PosixPath('b.txt'), PosixPath('c.txt')]
```

### Path Relationship Checks
```python
parent = Path('/home/user')
child = Path('/home/user/documents/file.txt')

print(child.is_relative_to(parent))  # True
print(parent.is_relative_to(child))  # False

# Check if path is within another directory
print(child.parent == parent)  # False
print(child.parent.is_relative_to(parent))  # True
```

## Advanced Methods

### Path Expansion
```python
# Expand user home directory
config_path = Path('~/.config/app/settings.ini').expanduser()
print(config_path)  # PosixPath('/home/user/.config/app/settings.ini')

# Note: expanduser() is available on concrete Path objects
```

### Working with File Permissions
```python
file_path = Path('script.py')

# Make executable
current_mode = file_path.stat().st_mode
executable_mode = current_mode | 0o111  # Add execute permissions
file_path.chmod(executable_mode)

# Check permissions
import stat
if file_path.stat().st_mode & stat.S_IRUSR:
    print("Readable by owner")
```

## Method Chaining

### Fluent Interface Pattern
```python
# Method chaining for complex operations
backup_path = (Path.home() / 'documents' / 'important.txt'
               .with_suffix('.bak')
               .with_name(lambda x: f"backup_{x}"))

# Equivalent without chaining
original = Path.home() / 'documents' / 'important.txt'
backup = original.with_suffix('.bak')
final_backup = backup.with_name(f"backup_{backup.name}")
```

### Practical Examples
```python
def create_backup(original_path: Path) -> Path:
    """Create a timestamped backup of a file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{original_path.stem}_{timestamp}{original_path.suffix}"
    backup_path = original_path.parent / backup_name
    return backup_path

def find_recent_files(directory: Path, days: int = 7) -> list[Path]:
    """Find files modified within the last N days."""
    cutoff = time.time() - (days * 24 * 3600)
    recent_files = []
    for file_path in directory.rglob('*'):
        if file_path.is_file() and file_path.stat().st_mtime > cutoff:
            recent_files.append(file_path)
    return recent_files

def organize_by_type(source_dir: Path, dest_dir: Path):
    """Organize files by extension into subdirectories."""
    for file_path in source_dir.rglob('*'):
        if file_path.is_file():
            ext = file_path.suffix[1:] or 'no_extension'
            type_dir = dest_dir / ext
            type_dir.mkdir(parents=True, exist_ok=True)
            # Move file to type directory
            new_path = type_dir / file_path.name
            file_path.rename(new_path)
```

## Error Handling with Methods

### Handling Common Errors
```python
def safe_file_operations(file_path: Path):
    """Demonstrate safe file operations with error handling."""
    try:
        # Check existence before operations
        if not file_path.exists():
            print(f"File {file_path} does not exist")
            return

        # Read with error handling
        try:
            content = file_path.read_text(encoding='utf-8')
            print(f"Read {len(content)} characters")
        except UnicodeDecodeError:
            print("File is not valid UTF-8 text")
        except PermissionError:
            print("Permission denied reading file")

        # Write operations
        backup_path = file_path.with_suffix('.bak')
        try:
            backup_path.write_text(content, encoding='utf-8')
            print(f"Created backup: {backup_path}")
        except PermissionError:
            print("Permission denied creating backup")

    except OSError as e:
        print(f"OS error: {e}")

# Usage
safe_file_operations(Path('example.txt'))
```

## Performance Considerations

### Efficient Operations
```python
# Inefficient: Multiple filesystem calls
files = []
for item in Path('.').iterdir():
    if item.is_file():
        files.append(item)

# More efficient: Single glob operation
files = list(Path('.').glob('*'))  # Files only
dirs = list(Path('.').glob('*/'))  # Directories only

# Use exists() sparingly
# Instead of:
if Path('file.txt').exists():
    content = Path('file.txt').read_text()

# Do:
file_path = Path('file.txt')
if file_path.exists():
    content = file_path.read_text()
```

## Summary

Path methods in `pathlib` provide a comprehensive toolkit for filesystem operations:

- **Construction**: Creating and joining paths
- **Inspection**: Checking existence, type, and properties
- **Manipulation**: Changing components and resolving paths
- **Operations**: Reading, writing, and modifying files/directories
- **Pattern Matching**: Finding files with glob patterns
- **Comparison**: Sorting and comparing paths

These methods enable clean, readable, and cross-platform filesystem code. The object-oriented design allows for method chaining and intuitive operations that closely mirror natural language descriptions of file system tasks.
