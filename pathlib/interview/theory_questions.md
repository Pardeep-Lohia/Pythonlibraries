# Theory Questions for pathlib Interviews

## Basic Concepts

### 1. What is pathlib and why was it introduced?

**Answer:**
pathlib is a module introduced in Python 3.4 that provides an object-oriented interface for filesystem paths. It was introduced to replace the old `os.path` and `glob` modules with a more intuitive and cross-platform way of handling filesystem operations.

Key benefits:
- Object-oriented approach instead of string manipulation
- Cross-platform compatibility (Windows, Unix, macOS)
- More readable and maintainable code
- Less error-prone than string-based path operations

### 2. What are the main classes in pathlib?

**Answer:**
- `Path`: The main concrete class for filesystem paths
- `PurePath`: Abstract base class for path manipulation without filesystem access
- `PosixPath`: Unix/Linux specific path class
- `WindowsPath`: Windows-specific path class

`Path` is actually an alias for the platform-specific class (`PosixPath` on Unix, `WindowsPath` on Windows).

### 3. What's the difference between PurePath and Path?

**Answer:**
- `PurePath`: Handles path manipulation only, no filesystem interaction
- `Path`: Inherits from PurePath and adds filesystem operations

PurePath is useful for:
- Path manipulation without filesystem access
- Cross-platform path handling in environments without filesystem
- String parsing and path construction

Path adds methods like:
- `exists()`, `is_file()`, `is_dir()`
- `read_text()`, `write_text()`
- `stat()`, `chmod()`, `unlink()`

## Path Construction

### 4. How do you create Path objects?

**Answer:**
```python
from pathlib import Path

# From string
path1 = Path('/home/user/file.txt')

# From multiple components
path2 = Path('home', 'user', 'file.txt')

# From another Path
path3 = Path(path1)

# Special constructors
home = Path.home()
cwd = Path.cwd()
```

### 5. How do you join paths in pathlib?

**Answer:**
```python
base = Path('/home/user')

# Using / operator (recommended)
config = base / 'config.ini'

# Using joinpath()
config = base.joinpath('config.ini')

# Multiple levels
deep = base / 'docs' / 'reports' / 'annual.pdf'
```

## Path Operations

### 6. How do you get different parts of a path?

**Answer:**
```python
path = Path('/home/user/documents/report.pdf')

print(path.name)      # 'report.pdf'
print(path.stem)      # 'report'
print(path.suffix)    # '.pdf'
print(path.parent)    # PosixPath('/home/user/documents')
print(path.parts)     # ('/', 'home', 'user', 'documents', 'report.pdf')
```

### 7. How do you modify path components?

**Answer:**
```python
original = Path('/home/user/file.txt')

# Change name
renamed = original.with_name('new.txt')

# Change suffix
backup = original.with_suffix('.bak')

# Change to different suffix
pdf = original.with_suffix('.pdf')
```

## Filesystem Operations

### 8. How do you check if a path exists and what type it is?

**Answer:**
```python
path = Path('/some/file.txt')

print(path.exists())     # True if exists
print(path.is_file())    # True if file
print(path.is_dir())     # True if directory
print(path.is_symlink()) # True if symbolic link
```

### 9. How do you read and write files?

**Answer:**
```python
path = Path('file.txt')

# Read text
content = path.read_text(encoding='utf-8')

# Write text
path.write_text('content', encoding='utf-8')

# Read bytes
data = path.read_bytes()

# Write bytes
path.write_bytes(b'data')
```

### 10. How do you list directory contents?

**Answer:**
```python
dir_path = Path('/home/user')

# List all items
items = list(dir_path.iterdir())

# Iterate with filtering
for item in dir_path.iterdir():
    if item.is_file():
        print(f"File: {item.name}")
    elif item.is_dir():
        print(f"Dir: {item.name}")
```

## Pattern Matching

### 11. How do you find files using patterns?

**Answer:**
```python
# Current directory
txt_files = list(Path('.').glob('*.txt'))

# Recursive search
all_py = list(Path('.').rglob('*.py'))

# Multiple patterns
code_files = []
for pattern in ['*.py', '*.js', '*.html']:
    code_files.extend(Path('.').rglob(pattern))
```

### 12. What's the difference between glob() and rglob()?

**Answer:**
- `glob(pattern)`: Searches only in the current directory
- `rglob(pattern)`: Searches recursively in all subdirectories

Both use the same pattern syntax (Unix shell-style wildcards).

## Path Resolution

### 13. How do you resolve relative paths?

**Answer:**
```python
# Resolve relative to current directory
relative = Path('../config/settings.ini')
absolute = relative.resolve()

# Resolve symlinks
symlink = Path('/home/user/docs_link')
real_path = symlink.resolve()
```

### 14. How do you expand user home directory?

**Answer:**
```python
# Expand ~ to home directory
config_path = Path('~/.config/app/settings.ini').expanduser()
```

## Cross-Platform Compatibility

### 15. How does pathlib handle different operating systems?

**Answer:**
pathlib automatically handles platform differences:

- Uses correct path separators (`/` on Unix, `\` on Windows)
- Handles case sensitivity appropriately
- Provides platform-specific classes when needed
- Accepts both `/` and `\` in path strings on Windows

```python
# Works on both Windows and Unix
path = Path('home/user/file.txt')
# Displays as: PosixPath('home/user/file.txt') on Unix
# Displays as: WindowsPath('home\\user\\file.txt') on Windows
```

## Comparison and Sorting

### 16. How do you compare Path objects?

**Answer:**
```python
path1 = Path('/home/user/file.txt')
path2 = Path('/home/user/file.txt')
other = Path('/home/user/other.txt')

print(path1 == path2)  # True
print(path1 == other)  # False

# For filesystem comparison
print(path1.samefile(path2))  # True if same file on disk
```

### 17. How are Path objects sorted?

**Answer:**
Path objects are sorted lexicographically based on their string representation:

```python
paths = [Path('c.txt'), Path('a.txt'), Path('b.txt')]
paths.sort()
# Result: [PosixPath('a.txt'), PosixPath('b.txt'), PosixPath('c.txt')]
```

## Error Handling

### 18. How do you handle pathlib operations safely?

**Answer:**
```python
path = Path('file.txt')

# Check before operations
if path.exists():
    content = path.read_text()
else:
    content = 'default'

# Use try-except for operations
try:
    content = path.read_text()
except FileNotFoundError:
    content = None
except UnicodeDecodeError:
    print("File encoding issue")
```

## Advanced Topics

### 19. What are PurePath classes used for?

**Answer:**
PurePath classes are used when you need path manipulation without filesystem access:

- Parsing paths from strings
- Building paths for different platforms
- Path arithmetic without disk I/O
- Working in environments without filesystem access

### 20. How do you work with file permissions?

**Answer:**
```python
import stat

path = Path('script.py')

# Get permissions
mode = path.stat().st_mode

# Check permissions
readable = bool(mode & stat.S_IRUSR)
writable = bool(mode & stat.S_IWUSR)

# Make executable
executable_mode = mode | stat.S_IXUSR
path.chmod(executable_mode)
```

### 21. How do you handle large files efficiently?

**Answer:**
```python
# Don't read entire file at once
# Instead, process in chunks
with path.open('rb') as file:
    while chunk := file.read(8192):
        process_chunk(chunk)

# Or line by line for text
with path.open('r', encoding='utf-8') as file:
    for line in file:
        process_line(line)
```

### 22. What's the difference between Path.unlink() and Path.rmdir()?

**Answer:**
- `unlink()`: Deletes a file (like `os.remove()`)
- `rmdir()`: Deletes an empty directory (like `os.rmdir()`)

Both raise `OSError` if the operation fails.

### 23. How do you create temporary paths?

**Answer:**
```python
import tempfile

# Temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir) / 'temp_file.txt'
    temp_path.write_text('temporary content')

# Temporary file
with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
    temp_path = Path(temp_file.name)
    temp_path.write_text('temp content')
```

### 24. How do you copy files with pathlib?

**Answer:**
pathlib doesn't have built-in copy methods. Use shutil:

```python
import shutil
from pathlib import Path

src = Path('source.txt')
dst = Path('destination.txt')

# Copy file
shutil.copy(src, dst)

# Copy with metadata
shutil.copy2(src, dst)
```

### 25. What are some common pathlib mistakes to avoid?

**Answer:**
1. Mixing Path objects with strings using `+`
2. Not checking path existence before operations
3. Forgetting that Path objects are immutable
4. Not handling encoding properly
5. Using inefficient patterns for multiple filesystem calls
6. Not using context managers for file operations

## Performance Considerations

### 26. How can you optimize pathlib operations?

**Answer:**
```python
# Inefficient: multiple stat calls
files = [f for f in Path('.').iterdir() if f.is_file() and f.stat().st_size > 1024]

# Better: single stat call per file
files = []
for f in Path('.').iterdir():
    if f.is_file():
        size = f.stat().st_size
        if size > 1024:
            files.append(f)

# Use glob for filtering when possible
large_files = [f for f in Path('.').glob('*') if f.stat().st_size > 1024]
```

## Integration with Other Modules

### 27. How does pathlib work with os and shutil?

**Answer:**
```python
import os
import shutil
from pathlib import Path

# os operations with Path
path = Path('file.txt')
os.chdir(path.parent)
os.remove(path)  # Accepts Path objects

# shutil operations
shutil.copy(path, Path('backup.txt'))
shutil.move(path, Path('new_location.txt'))
```

### 28. How do you convert between pathlib and other path representations?

**Answer:**
```python
path = Path('/home/user/file.txt')

# To string
path_str = str(path)

# To bytes
path_bytes = bytes(path)

# From os.path operations
import os.path
posix_path = Path(os.path.join('home', 'user', 'file.txt'))
```

## Best Practices

### 29. What are some pathlib best practices?

**Answer:**
1. Use the `/` operator for path joining
2. Prefer Path methods over os.path functions
3. Always specify encoding for text operations
4. Check path existence before operations
5. Use context managers for file operations
6. Handle exceptions appropriately
7. Use relative paths when appropriate
8. Leverage pathlib's cross-platform features

### 30. When should you not use pathlib?

**Answer:**
- When working with very old Python versions (< 3.4)
- When you need very low-level filesystem operations
- When interfacing with libraries that expect string paths
- In performance-critical code where string operations are faster
- When you need platform-specific behavior beyond what pathlib provides
