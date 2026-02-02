# pathlib Cheatsheet

## Import and Basic Usage

```python
from pathlib import Path, PurePath

# Create Path objects
path = Path('/home/user/file.txt')
path = Path('home', 'user', 'file.txt')  # Multiple components
path = Path()  # Current directory

# Special paths
home = Path.home()
cwd = Path.cwd()
```

## Path Construction and Joining

```python
base = Path('/home/user')

# Join paths (recommended)
config = base / 'config.ini'
docs = base / 'Documents' / 'report.pdf'

# Alternative joining
config = base.joinpath('config.ini')
config = Path(base, 'config.ini')

# From string
path = Path('/home/user/file.txt')
```

## Path Components

```python
path = Path('/home/user/documents/report.pdf')

# Access components
print(path.name)      # 'report.pdf'
print(path.stem)      # 'report'
print(path.suffix)    # '.pdf'
print(path.suffixes)  # ['.pdf']
print(path.parent)    # PosixPath('/home/user/documents')
print(path.parents[0]) # PosixPath('/home/user/documents')
print(path.parents[1]) # PosixPath('/home/user')
print(path.parts)     # ('/', 'home', 'user', 'documents', 'report.pdf')
```

## Path Modification

```python
original = Path('/home/user/file.txt')

# Change components
renamed = original.with_name('new.txt')      # '/home/user/new.txt'
backup = original.with_suffix('.bak')        # '/home/user/file.bak'
pdf = original.with_suffix('.pdf')           # '/home/user/file.pdf'

# Path is immutable - these return new Path objects
print(original)  # Still '/home/user/file.txt'
```

## Filesystem Checks

```python
path = Path('/home/user/file.txt')

# Existence and type
path.exists()        # True if exists
path.is_file()       # True if file
path.is_dir()        # True if directory
path.is_symlink()    # True if symlink
path.is_absolute()   # True if absolute path
path.is_relative_to(Path('/home/user'))  # True if relative to given path
```

## File Operations

```python
# Read/Write text
content = path.read_text(encoding='utf-8')
path.write_text('content', encoding='utf-8')

# Read/Write bytes
data = path.read_bytes()
path.write_bytes(b'data')

# Context manager
with path.open('r', encoding='utf-8') as f:
    content = f.read()

# Create empty file
path.touch()

# Delete file
path.unlink(missing_ok=True)  # Won't error if file doesn't exist
```

## Directory Operations

```python
dir_path = Path('/home/user/docs')

# Create directory
dir_path.mkdir(parents=True, exist_ok=True)

# List contents
items = list(dir_path.iterdir())
for item in dir_path.iterdir():
    print(item.name)

# Delete empty directory
dir_path.rmdir()
```

## Pattern Matching (Glob)

```python
# Current directory
txt_files = list(Path('.').glob('*.txt'))
py_files = list(Path('.').glob('*.py'))

# Recursive (all subdirectories)
all_txt = list(Path('.').rglob('*.txt'))
all_py = list(Path('.').rglob('*.py'))

# Multiple patterns
code_files = []
for pattern in ['*.py', '*.js', '*.html']:
    code_files.extend(Path('.').rglob(pattern))

# Complex patterns
images = list(Path('.').rglob('*.{jpg,jpeg,png,gif}'))
```

## Path Resolution

```python
# Resolve relative paths and symlinks
relative = Path('../config/settings.ini')
absolute = relative.resolve()

# Expand user home
config = Path('~/.config/app/settings.ini').expanduser()

# Get absolute path
abs_path = path.absolute()  # May not resolve symlinks
```

## File Metadata

```python
if path.exists():
    stat = path.stat()

    # Size
    size_bytes = stat.st_size
    size_mb = stat.st_size / (1024 * 1024)

    # Timestamps
    import time
    modified_time = stat.st_mtime
    modified_str = time.ctime(stat.st_mtime)

    # Permissions (Unix)
    import stat
    mode = stat.filemode(stat.st_mode)
    readable = bool(stat.st_mode & stat.S_IRUSR)
    writable = bool(stat.st_mode & stat.S_IWUSR)
    executable = bool(stat.st_mode & stat.S_IXUSR)
```

## Path Comparison and Sorting

```python
path1 = Path('/home/user/file1.txt')
path2 = Path('/home/user/file2.txt')
path3 = Path('/home/user/file1.txt')

# Equality
path1 == path3  # True
path1 == path2  # False

# Filesystem comparison
path1.samefile(path3)  # True if same file on disk

# Sorting (lexicographic)
paths = [Path('c.txt'), Path('a.txt'), Path('b.txt')]
paths.sort()  # ['a.txt', 'b.txt', 'c.txt']
```

## Cross-Platform Operations

```python
# pathlib handles platform differences automatically
path = Path('home/user/file.txt')
# On Windows: WindowsPath('home\\user\\file.txt')
# On Unix: PosixPath('home/user/file.txt')

# String representation
str(path)  # Uses platform-specific separators

# Platform-specific classes
from pathlib import PosixPath, WindowsPath

# Force platform-specific behavior
posix_path = PosixPath('/home/user/file.txt')
```

## Working with Relative Paths

```python
base = Path('/home/user/projects/myapp')
file_path = Path('/home/user/projects/myapp/src/main.py')

# Get relative path
relative = file_path.relative_to(base)  # PosixPath('src/main.py')

# Check if relative
file_path.is_relative_to(base)  # True

# Combine absolute and relative
full_path = base / relative  # Back to absolute
```

## Common Patterns

### Safe File Reading
```python
def safe_read(path: Path, default='') -> str:
    try:
        if path.exists() and path.is_file():
            return path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        pass
    return default

content = safe_read(Path('file.txt'))
```

### Find Files by Extension
```python
def find_by_extension(directory: Path, extension: str) -> list[Path]:
    return list(directory.rglob(f'*.{extension}'))

py_files = find_by_extension(Path('.'), 'py')
```

### Create Backup
```python
def create_backup(file_path: Path) -> Path:
    backup = file_path.with_suffix(f'{file_path.suffix}.bak')
    backup.write_text(file_path.read_text())
    return backup

backup_path = create_backup(Path('config.txt'))
```

### Directory Size
```python
def get_dir_size(directory: Path) -> int:
    if not directory.exists():
        return 0
    return sum(f.stat().st_size for f in directory.rglob('*') if f.is_file())

size = get_dir_size(Path('/home/user'))
```

### Organize Files by Type
```python
def organize_by_type(source: Path, dest: Path):
    for file_path in source.iterdir():
        if file_path.is_file():
            ext = file_path.suffix[1:] or 'no_extension'
            type_dir = dest / ext
            type_dir.mkdir(exist_ok=True)
            file_path.rename(type_dir / file_path.name)

organize_by_type(Path('downloads'), Path('organized'))
```

## Integration with Other Modules

### With os
```python
import os
from pathlib import Path

# Convert between Path and str
path_str = str(Path('file.txt'))
path = Path(os.path.join('home', 'user', 'file.txt'))

# Use with os functions
os.chdir(Path('mydir'))
os.remove(Path('file.txt'))
```

### With shutil
```python
import shutil
from pathlib import Path

# Copy operations
shutil.copy(Path('source.txt'), Path('dest.txt'))
shutil.copy2(Path('source.txt'), Path('dest.txt'))  # Preserve metadata
shutil.move(Path('old.txt'), Path('new.txt'))
```

### With glob (old module)
```python
import glob
from pathlib import Path

# Old way
files = glob.glob('*.txt')

# New way (better)
files = [str(p) for p in Path('.').glob('*.txt')]
# Or keep as Path objects
files = list(Path('.').glob('*.txt'))
```

## Error Handling

```python
path = Path('file.txt')

# Check before operations
if not path.exists():
    print("File not found")

# Handle specific exceptions
try:
    content = path.read_text()
except FileNotFoundError:
    content = "File not found"
except PermissionError:
    content = "Permission denied"
except UnicodeDecodeError:
    content = "Encoding error"
```

## Performance Tips

```python
# Inefficient: multiple stat calls
files = [f for f in Path('.').iterdir()
         if f.is_file() and f.stat().st_size > 1024]

# Better: single stat call
files = []
for f in Path('.').iterdir():
    if f.is_file():
        stat = f.stat()
        if stat.st_size > 1024:
            files.append(f)

# Use glob when possible
large_files = [f for f in Path('.').glob('*')
               if f.is_file() and f.stat().st_size > 1024]
```

## PurePath vs Path

```python
# Pure paths (no filesystem access)
pure = PurePath('/home/user/file.txt')
pure.parts  # Works
# pure.exists()  # AttributeError

# Concrete paths (filesystem access)
concrete = Path('/home/user/file.txt')
concrete.exists()  # Works
concrete.parts     # Also works
```

## Common Conversions

```python
# Path to string
path_str = str(path)

# Path to bytes
path_bytes = bytes(path)

# String to Path
path = Path(path_str)

# Path to URI
uri = path.as_uri()  # 'file:///home/user/file.txt'

# URI to Path
from urllib.parse import unquote
from pathlib import Path
path = Path(unquote(uri.replace('file://', '')))
```

## Advanced Usage

### Custom Path Subclass
```python
class ProjectPath(Path):
    def is_python_file(self):
        return self.is_file() and self.suffix == '.py'

    def get_module_name(self):
        return self.stem if self.is_python_file() else None

file_path = ProjectPath('main.py')
file_path.is_python_file()  # True
file_path.get_module_name()  # 'main'
```

### Atomic Writes
```python
def atomic_write(path: Path, content: str):
    temp = path.with_suffix('.tmp')
    temp.write_text(content)
    temp.replace(path)  # Atomic on POSIX

atomic_write(Path('config.txt'), 'new content')
```

### Temporary Files
```python
import tempfile

# Temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir) / 'temp.txt'
    temp_path.write_text('temporary')

# Temporary file
with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    temp_path = Path(temp_file.name)
    # Use temp_path
```

## Quick Reference

### Creating Paths
- `Path('file.txt')` - From string
- `Path('dir', 'file.txt')` - From components
- `Path.home()` - Home directory
- `Path.cwd()` - Current directory

### Path Operations
- `path / 'sub'` - Join paths
- `path.exists()` - Check existence
- `path.is_file()` - Check if file
- `path.is_dir()` - Check if directory

### File Operations
- `path.read_text()` - Read text
- `path.write_text('content')` - Write text
- `path.read_bytes()` - Read bytes
- `path.write_bytes(b'data')` - Write bytes

### Directory Operations
- `path.mkdir()` - Create directory
- `list(path.iterdir())` - List contents
- `path.rmdir()` - Remove empty directory

### Pattern Matching
- `path.glob('*.txt')` - Current directory
- `path.rglob('*.txt')` - Recursive

### Path Info
- `path.name` - Filename
- `path.stem` - Name without suffix
- `path.suffix` - File extension
- `path.parent` - Parent directory
- `path.parts` - Path components
