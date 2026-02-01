# Path Handling with `os.path`

## Overview
The `os.path` submodule provides functions for manipulating filesystem paths in a cross-platform manner. It handles platform-specific differences automatically, making code portable across Windows, macOS, and Linux.

## Core Path Functions

### `os.path.join(*paths)` - Join Path Components
**Purpose**: Joins path components intelligently with the correct separator for the platform.

**Syntax**:
```python
os.path.join(path, *paths)
```

**Parameters**:
- `path`: First path component
- `*paths`: Additional path components

**Examples**:
```python
import os

# Basic joining
path = os.path.join('home', 'user', 'documents')
# Unix: 'home/user/documents'
# Windows: 'home\\user\\documents'

# Multiple components
full_path = os.path.join('C:', 'Users', 'John', 'Desktop', 'file.txt')
# Windows: 'C:\\Users\\John\\Desktop\\file.txt'

# Absolute path handling
path = os.path.join('/home/user', 'documents', 'file.txt')
# Result: '/home/user/documents/file.txt' (absolute path preserved)
```

**Key Behaviors**:
- Ignores empty strings and None values
- Preserves absolute paths (starting component overrides previous)
- Uses platform-appropriate separators

### `os.path.abspath(path)` - Get Absolute Path
**Purpose**: Converts a relative path to an absolute path.

**Syntax**:
```python
os.path.abspath(path)
```

**Examples**:
```python
import os

# Relative to absolute
abs_path = os.path.abspath('file.txt')
# Result: '/current/working/directory/file.txt'

# Already absolute (no change)
abs_path = os.path.abspath('/home/user/file.txt')
# Result: '/home/user/file.txt'

# Complex relative path
abs_path = os.path.abspath('../parent/file.txt')
# Result: '/parent/directory/file.txt'
```

### `os.path.normpath(path)` - Normalize Path
**Purpose**: Normalizes a path by resolving redundant separators and relative components.

**Syntax**:
```python
os.path.normpath(path)
```

**Examples**:
```python
import os

# Remove redundant separators
path = os.path.normpath('home//user///file.txt')
# Result: 'home/user/file.txt'

# Resolve current directory
path = os.path.normpath('home/./user/file.txt')
# Result: 'home/user/file.txt'

# Resolve parent directory
path = os.path.normpath('home/user/../documents/file.txt')
# Result: 'home/documents/file.txt'

# Mixed separators (platform-dependent result)
path = os.path.normpath('home\\user/file.txt')
# Unix: 'home\\user/file.txt'
# Windows: 'home\\user\\file.txt'
```

### `os.path.dirname(path)` - Get Directory Name
**Purpose**: Returns the directory portion of a path.

**Syntax**:
```python
os.path.dirname(path)
```

**Examples**:
```python
import os

# File path
dir_name = os.path.dirname('/home/user/file.txt')
# Result: '/home/user'

# Nested path
dir_name = os.path.dirname('/home/user/documents/readme.txt')
# Result: '/home/user/documents'

# Root level
dir_name = os.path.dirname('/file.txt')
# Result: '/'

# No directory
dir_name = os.path.dirname('file.txt')
# Result: '' (empty string)
```

### `os.path.basename(path)` - Get Base Name
**Purpose**: Returns the final component of a path (filename or directory name).

**Syntax**:
```python
os.path.basename(path)
```

**Examples**:
```python
import os

# File path
base_name = os.path.basename('/home/user/file.txt')
# Result: 'file.txt'

# Directory path
base_name = os.path.basename('/home/user/documents/')
# Result: 'documents'

# Root path
base_name = os.path.basename('/')
# Result: '' (empty string)

# Just filename
base_name = os.path.basename('file.txt')
# Result: 'file.txt'
```

### `os.path.splitext(path)` - Split Extension
**Purpose**: Splits a path into root and extension.

**Syntax**:
```python
os.path.splitext(path)
```

**Return Value**: Tuple of (root, extension)

**Examples**:
```python
import os

# Regular file
root, ext = os.path.splitext('/home/user/file.txt')
# root: '/home/user/file', ext: '.txt'

# Multiple extensions
root, ext = os.path.splitext('/home/user/archive.tar.gz')
# root: '/home/user/archive.tar', ext: '.gz'

# No extension
root, ext = os.path.splitext('/home/user/README')
# root: '/home/user/README', ext: ''

# Hidden file
root, ext = os.path.splitext('/home/user/.bashrc')
# root: '/home/user/.bashrc', ext: ''
```

## Path Checking Functions

### `os.path.exists(path)` - Check Path Existence
**Purpose**: Tests whether a path exists in the filesystem.

**Syntax**:
```python
os.path.exists(path)
```

**Return Value**: `True` if path exists, `False` otherwise

**Examples**:
```python
import os

# Check file
exists = os.path.exists('/home/user/file.txt')

# Check directory
exists = os.path.exists('/home/user/documents')

# Check non-existent path
exists = os.path.exists('/non/existent/path')
# Result: False
```

### `os.path.isfile(path)` - Check if File
**Purpose**: Tests whether a path is an existing regular file.

**Syntax**:
```python
os.path.isfile(path)
```

**Examples**:
```python
import os

# Regular file
is_file = os.path.isfile('/home/user/file.txt')
# Result: True

# Directory
is_file = os.path.isfile('/home/user/documents')
# Result: False

# Non-existent
is_file = os.path.isfile('/non/existent/file.txt')
# Result: False
```

### `os.path.isdir(path)` - Check if Directory
**Purpose**: Tests whether a path is an existing directory.

**Syntax**:
```python
os.path.isdir(path)
```

**Examples**:
```python
import os

# Directory
is_dir = os.path.isdir('/home/user/documents')
# Result: True

# File
is_dir = os.path.isdir('/home/user/file.txt')
# Result: False

# Non-existent
is_dir = os.path.isdir('/non/existent/dir')
# Result: False
```

### `os.path.islink(path)` - Check if Symbolic Link
**Purpose**: Tests whether a path is an existing symbolic link.

**Syntax**:
```python
os.path.islink(path)
```

**Examples**:
```python
import os

# Symbolic link
is_link = os.path.islink('/home/user/symlink')

# Regular file/directory
is_link = os.path.islink('/home/user/file.txt')
# Result: False
```

### `os.path.ismount(path)` - Check if Mount Point
**Purpose**: Tests whether a path is a mount point.

**Syntax**:
```python
os.path.ismount(path)
```

**Examples**:
```python
import os

# Mount point
is_mount = os.path.ismount('/mnt/external')

# Regular directory
is_mount = os.path.isdir('/home/user')
# Result: False
```

## Path Comparison and Operations

### `os.path.samefile(path1, path2)` - Check Same File
**Purpose**: Tests whether two pathnames refer to the same file or directory.

**Syntax**:
```python
os.path.samefile(path1, path2)
```

**Examples**:
```python
import os

# Same file, different paths
same = os.path.samefile('/home/user/file.txt', './file.txt')

# Different files
same = os.path.samefile('/home/user/file1.txt', '/home/user/file2.txt')
# Result: False
```

### `os.path.samestat(stat1, stat2)` - Compare File Stats
**Purpose**: Tests whether two stat tuples refer to the same file.

**Syntax**:
```python
os.path.samestat(stat1, stat2)
```

**Examples**:
```python
import os

stat1 = os.stat('/home/user/file.txt')
stat2 = os.stat('./file.txt')

same = os.path.samestat(stat1, stat2)
```

### `os.path.relpath(path, start)` - Get Relative Path
**Purpose**: Returns a relative filepath to path from the start directory.

**Syntax**:
```python
os.path.relpath(path, start=os.curdir)
```

**Examples**:
```python
import os

# Get relative path
rel_path = os.path.relpath('/home/user/documents/file.txt', '/home/user')
# Result: 'documents/file.txt'

# From current directory
rel_path = os.path.relpath('/etc/passwd')
# Result: '../../../etc/passwd' (relative to current dir)
```

## Platform-Specific Attributes

### `os.path.sep` - Path Separator
**Purpose**: The character used to separate path components.

**Value**:
- Unix/Linux/macOS: `'/'`
- Windows: `'\\'`

### `os.path.altsep` - Alternative Separator
**Purpose**: An alternative path separator (None on Unix, `'/'` on Windows).

### `os.path.extsep` - Extension Separator
**Purpose**: The character that separates the base filename from the extension.

**Value**: `'.'`

### `os.path.pathsep` - Path Environment Separator
**Purpose**: The character used to separate paths in environment variables like PATH.

**Value**:
- Unix/Linux/macOS: `':'`
- Windows: `';'`

## Advanced Path Operations

### `os.path.commonprefix(list)` - Common Prefix
**Purpose**: Returns the longest common subpath of each pathname in the list.

**Syntax**:
```python
os.path.commonprefix(list)
```

**Examples**:
```python
import os

# Common prefix
prefix = os.path.commonprefix([
    '/home/user/documents/file1.txt',
    '/home/user/documents/file2.txt',
    '/home/user/downloads/file3.txt'
])
# Result: '/home/user/'
```

### `os.path.commonpath(paths)` - Common Path
**Purpose**: Returns the longest common subpath of each pathname.

**Syntax**:
```python
os.path.commonpath(paths)
```

**Note**: Available in Python 3.5+

## Best Practices

### 1. Always Use `os.path.join()` for Path Construction
```python
# Good
path = os.path.join('home', 'user', 'file.txt')

# Bad
path = 'home' + '/' + 'user' + '/' + 'file.txt'  # Platform-specific
```

### 2. Normalize Paths After User Input
```python
user_path = input("Enter path: ")
safe_path = os.path.normpath(user_path)
```

### 3. Check Path Existence Before Operations
```python
if os.path.exists(file_path):
    if os.path.isfile(file_path):
        # Handle file
    elif os.path.isdir(file_path):
        # Handle directory
```

### 4. Use Absolute Paths for Critical Operations
```python
config_path = os.path.abspath('config.json')
```

### 5. Handle Extensions Properly
```python
filename = 'document.pdf'
name, ext = os.path.splitext(filename)
if ext.lower() == '.pdf':
    # Handle PDF file
```

## Common Patterns

### Safe File Path Construction
```python
def build_safe_path(base_dir, *components):
    """Build a safe path within a base directory."""
    # Ensure base_dir is absolute and normalized
    base_dir = os.path.abspath(base_dir)

    # Join components
    full_path = os.path.join(base_dir, *components)

    # Normalize and ensure it's still within base_dir
    full_path = os.path.normpath(full_path)

    if not full_path.startswith(base_dir):
        raise ValueError("Path traversal attempt detected")

    return full_path
```

### File Type Detection
```python
def get_file_type(filepath):
    """Determine file type from path."""
    if not os.path.exists(filepath):
        return 'nonexistent'

    if os.path.islink(filepath):
        return 'symlink'
    elif os.path.isdir(filepath):
        return 'directory'
    elif os.path.isfile(filepath):
        return 'file'
    else:
        return 'unknown'
```

### Path Validation
```python
def validate_path(filepath, base_dir=None):
    """Validate a file path."""
    checks = {
        'exists': os.path.exists(filepath),
        'is_file': os.path.isfile(filepath),
        'is_dir': os.path.isdir(filepath),
        'is_absolute': os.path.isabs(filepath),
        'is_link': os.path.islink(filepath)
    }

    if base_dir:
        base_dir = os.path.abspath(base_dir)
        abs_path = os.path.abspath(filepath)
        checks['within_base'] = abs_path.startswith(base_dir)

    return checks
```

These functions provide robust, cross-platform path handling that works reliably across different operating systems and filesystem configurations.
