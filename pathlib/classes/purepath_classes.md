# PurePath Classes in pathlib

## Overview of PurePath Classes

PurePath classes provide abstract path operations without requiring filesystem access. They are the foundation of `pathlib`'s object-oriented path handling, offering pure computational path manipulations that work across platforms.

## PurePath Class Hierarchy

### Base PurePath Class
`PurePath` is the abstract base class for all path objects. It provides the core path manipulation functionality without any filesystem I/O operations.

```python
from pathlib import PurePath

# Create a PurePath object
path = PurePath('/home/user/file.txt')
print(type(path))  # <class 'pathlib.PurePosixPath'> or <class 'pathlib.PureWindowsPath'>
```

### Platform-Specific Subclasses

#### PurePosixPath
Handles POSIX-style paths (Unix, Linux, macOS):
- Uses forward slashes `/` as separators
- Case-sensitive path components
- No drive letters

```python
from pathlib import PurePosixPath

posix_path = PurePosixPath('/home/user/documents/file.txt')
print(posix_path)  # PurePosixPath('/home/user/documents/file.txt')
```

#### PureWindowsPath
Handles Windows-style paths:
- Uses backslashes `\` as separators
- Supports drive letters (C:, D:, etc.)
- Case-insensitive path components (on case-insensitive filesystems)

```python
from pathlib import PureWindowsPath

windows_path = PureWindowsPath('C:\\Users\\user\\Documents\\file.txt')
print(windows_path)  # PureWindowsPath('C:/Users/user/Documents/file.txt')
```

## Creating PurePath Objects

### From Strings
```python
# Automatic platform detection
path1 = PurePath('/home/user/file.txt')  # Creates PurePosixPath on Unix-like systems

# Explicit platform specification
posix_path = PurePosixPath('/home/user/file.txt')
windows_path = PureWindowsPath('C:\\Users\\user\\file.txt')
```

### From Multiple Components
```python
# Join path components
path = PurePath('home', 'user', 'documents', 'file.txt')
print(path)  # PurePosixPath('home/user/documents/file.txt')
```

### From Other Path Objects
```python
existing_path = PurePath('/home/user')
new_path = PurePath(existing_path, 'file.txt')
print(new_path)  # PurePosixPath('/home/user/file.txt')
```

## PurePath Properties

### Path Components
```python
path = PurePath('/home/user/documents/report.pdf')

print(f"Full path: {path}")
print(f"Name: {path.name}")           # 'report.pdf'
print(f"Stem: {path.stem}")           # 'report'
print(f"Suffix: {path.suffix}")       # '.pdf'
print(f"Suffixes: {path.suffixes}")   # ['.pdf']
print(f"Parent: {path.parent}")       # PurePosixPath('/home/user/documents')
print(f"Parts: {path.parts}")         # ('/', 'home', 'user', 'documents', 'report.pdf')
```

### Path Type Information
```python
print(f"Is absolute: {path.is_absolute()}")  # True
print(f"Is relative: {not path.is_absolute()}")  # False

# Check if path is relative to another
base = PurePath('/home/user')
full = PurePath('/home/user/documents/file.txt')
print(full.is_relative_to(base))  # True
```

## Path Manipulation Methods

### Path Joining with `/` Operator
```python
base = PurePath('/home/user')
documents = base / 'Documents'
file_path = documents / 'report.pdf'

print(file_path)  # PurePosixPath('/home/user/Documents/report.pdf')
```

### Changing Path Components
```python
original = PurePath('/home/user/file.txt')

# Change name
renamed = original.with_name('new_file.txt')
print(renamed)  # PurePosixPath('/home/user/new_file.txt')

# Change suffix
backup = original.with_suffix('.bak')
print(backup)  # PurePosixPath('/home/user/file.bak')

# Change to different suffix
pdf_version = original.with_suffix('.pdf')
print(pdf_version)  # PurePosixPath('/home/user/file.pdf')
```

### Path Arithmetic
```python
# Join multiple paths
path1 = PurePath('home') / 'user' / 'file.txt'
path2 = PurePath('home', 'user', 'file.txt')
path3 = PurePath('home/user') / 'file.txt'

print(path1 == path2 == path3)  # True
```

## Path Comparison and Operations

### Equality and Comparison
```python
path1 = PurePath('/home/user/file.txt')
path2 = PurePath('/home/user/file.txt')
path3 = PurePath('/home/user/other.txt')

print(path1 == path2)  # True
print(path1 == path3)  # False

# Lexicographical comparison
print(path1 < path3)   # True ('f' comes before 'o')
```

### Path Relationships
```python
parent = PurePath('/home/user')
child = PurePath('/home/user/documents/file.txt')

print(child.is_relative_to(parent))  # True
print(parent.is_relative_to(child))  # False

# Get relative path
relative = child.relative_to(parent)
print(relative)  # PurePosixPath('documents/file.txt')
```

## Platform-Specific Behavior

### POSIX Path Characteristics
```python
posix_path = PurePosixPath('/Home/User/File.txt')

# Case-sensitive
print(posix_path == PurePosixPath('/home/user/file.txt'))  # False

# No drive concept
print(posix_path.drive)  # ''
print(posix_path.root)   # '/'
```

### Windows Path Characteristics
```python
windows_path = PureWindowsPath('C:\\Home\\User\\File.txt')

# Case-insensitive on Windows filesystems
print(windows_path == PureWindowsPath('c:\\home\\user\\file.txt'))  # True

# Drive and root
print(windows_path.drive)  # 'C:'
print(windows_path.root)   # '\\' (note: displayed as single backslash)

# UNC paths
unc_path = PureWindowsPath('\\\\server\\share\\file.txt')
print(unc_path.drive)  # '\\\\server\\share'
```

## Advanced Path Operations

### Path Normalization
PurePath performs basic normalization but doesn't resolve `..` or `.` components:

```python
# Basic normalization
path1 = PurePath('home//user/./file.txt')
path2 = PurePath('home/user/file.txt')
print(path1 == path2)  # True (normalized)

# But doesn't resolve .. 
path3 = PurePath('home/user/../user/file.txt')
print(path3.parts)  # ('home', 'user', '..', 'user', 'file.txt')
# The .. is kept as-is, not resolved
```

### Working with Multiple Suffixes
```python
# Files with multiple extensions
tar_gz_file = PurePath('archive.tar.gz')

print(tar_gz_file.suffix)       # '.gz'
print(tar_gz_file.suffixes)     # ['.tar', '.gz']
print(tar_gz_file.stem)         # 'archive.tar'

# Change suffix affects only the last one
without_gz = tar_gz_file.with_suffix('')
print(without_gz)  # PurePosixPath('archive.tar')
```

## PurePath Use Cases

### Path Template Creation
```python
def create_config_path(app_name: str, filename: str) -> PurePath:
    """Create a cross-platform config file path."""
    return PurePath.home() / '.config' / app_name / filename

config_path = create_config_path('myapp', 'settings.ini')
print(config_path)  # PurePosixPath('/home/user/.config/myapp/settings.ini')
```

### Path Validation and Parsing
```python
def parse_backup_path(backup_path: PurePath) -> dict:
    """Parse a backup file path to extract metadata."""
    if not backup_path.suffix == '.bak':
        raise ValueError("Not a backup file")

    original_stem = backup_path.stem  # Remove .bak
    if '_' in original_stem:
        name, timestamp = original_stem.rsplit('_', 1)
        return {
            'original_name': name,
            'timestamp': timestamp,
            'extension': backup_path.suffix
        }
    else:
        return {
            'original_name': original_stem,
            'timestamp': None,
            'extension': backup_path.suffix
        }

backup = PurePath('/data/file_20231201_143022.bak')
info = parse_backup_path(backup)
print(info)
# {'original_name': 'file', 'timestamp': '20231201_143022', 'extension': '.bak'}
```

### Cross-Platform Path Building
```python
def build_project_path(*components) -> PurePath:
    """Build a project path from components."""
    return PurePath('projects', *components)

# Works on any platform
src_path = build_project_path('myproject', 'src', 'main.py')
test_path = build_project_path('myproject', 'tests', 'test_main.py')

print(src_path)   # PurePosixPath('projects/myproject/src/main.py')
print(test_path)  # PurePosixPath('projects/myproject/tests/test_main.py')
```

## Integration with Concrete Paths

### Converting Between Pure and Concrete
```python
from pathlib import Path

# PurePath to concrete Path
pure_path = PurePath('/home/user/file.txt')
concrete_path = Path(pure_path)

# Concrete Path to PurePath
concrete = Path('/home/user/file.txt')
pure = PurePath(concrete)
```

### When to Use PurePath vs Path
```python
# Use PurePath when:
# - You need path manipulation without filesystem access
# - Building paths for different platforms
# - Path calculations and transformations
# - Working with path templates

# Use Path when:
# - You need to interact with the filesystem
# - Checking file existence, reading/writing files
# - Directory operations
# - File metadata access
```

## Error Handling

### Path Validation
```python
def validate_config_path(config_path: PurePath) -> bool:
    """Validate that a path looks like a valid config file path."""
    try:
        # Check if it's an absolute path
        if not config_path.is_absolute():
            return False

        # Check if it has the right structure
        parts = config_path.parts
        if len(parts) < 4:  # /, home, user, .config, app, config.ini
            return False

        # Check if it's a config file
        if config_path.suffix not in ['.ini', '.json', '.yaml', '.yml']:
            return False

        return True
    except Exception:
        return False

valid_path = PurePath('/home/user/.config/myapp/settings.ini')
invalid_path = PurePath('relative/config.txt')

print(validate_config_path(valid_path))    # True
print(validate_config_path(invalid_path))  # False
```

## Best Practices

### Prefer PurePath for Path Logic
```python
# Good: Use PurePath for path construction and manipulation
def create_backup_path(original: PurePath, timestamp: str) -> PurePath:
    backup_name = f"{original.stem}_{timestamp}{original.suffix}"
    return original.parent / backup_name

# Avoid: Mixing string operations
def bad_create_backup_path(original_str: str, timestamp: str) -> str:
    # String manipulation prone to errors
    pass
```

### Cross-Platform Compatibility
```python
# Good: Use PurePath for platform-independent path building
def get_cache_dir(app_name: str) -> PurePath:
    """Get platform-appropriate cache directory."""
    if PurePath.home():  # This works on all platforms
        return PurePath.home() / '.cache' / app_name

# The actual platform-specific behavior is handled automatically
cache_dir = get_cache_dir('myapp')
print(cache_dir)  # Correct path for current platform
```

## Summary

PurePath classes provide the foundation for `pathlib`'s path handling:

- **Abstract Operations**: Path manipulation without filesystem access
- **Cross-Platform**: Automatic platform-specific behavior
- **Immutable Objects**: Safe path transformations
- **Rich API**: Comprehensive methods for path operations

Key characteristics:
- **PurePosixPath**: Unix-like path handling
- **PureWindowsPath**: Windows path handling
- **Automatic Platform Selection**: `PurePath` chooses appropriate subclass
- **Path Arithmetic**: Intuitive joining with `/` operator
- **Component Access**: Properties for name, parent, suffix, etc.

PurePath classes are ideal for:
- Path template creation
- Cross-platform path building
- Path validation and parsing
- Complex path manipulations
- Applications where filesystem access isn't needed

When filesystem operations are required, use the concrete `Path` classes, which inherit all PurePath functionality plus I/O capabilities.
