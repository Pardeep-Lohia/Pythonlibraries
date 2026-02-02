# `mkstemp()` and `mkdtemp()` Functions

## Overview

`mkstemp()` and `mkdtemp()` are low-level functions in the `tempfile` module that provide direct access to secure temporary file and directory creation. These functions offer maximum control but require manual resource management.

## `mkstemp()` Function

### Function Signature
```python
def mkstemp(suffix=None, prefix=None, dir=None, text=False)
```

### Parameters
- **suffix**: Filename suffix (e.g., '.tmp')
- **prefix**: Filename prefix (e.g., 'tmp')
- **dir**: Directory for temp file (None for system default)
- **text**: Return text mode file object (False for binary)

### Return Value
Returns a tuple: `(file_descriptor, absolute_path)`

### Key Features
- **Secure Creation**: Uses system `mkstemp()` for race-free file creation
- **Low-Level Access**: Returns file descriptor, not file object
- **Manual Cleanup**: No automatic deletion
- **Cross-Platform**: Works consistently across operating systems

### Usage Examples

#### Basic Usage
```python
import tempfile
import os

# Create temporary file
fd, path = tempfile.mkstemp(suffix='.txt', prefix='myapp_')
print(f"File descriptor: {fd}")
print(f"Path: {path}")

# Use the file
with os.fdopen(fd, 'w') as f:
    f.write('Hello, world!')

# Read back
with open(path, 'r') as f:
    content = f.read()
    print(content)

# Manual cleanup
os.unlink(path)
```

#### With Context Manager Pattern
```python
import os
import contextlib

@contextlib.contextmanager
def temp_file(**kwargs):
    fd, path = tempfile.mkstemp(**kwargs)
    try:
        with os.fdopen(fd, 'w+') as f:
            yield f, path
    finally:
        os.unlink(path)

# Usage
with temp_file(suffix='.log') as (f, path):
    f.write('Log entry')
    # File automatically cleaned up
```

## `mkdtemp()` Function

### Function Signature
```python
def mkdtemp(suffix=None, prefix=None, dir=None)
```

### Parameters
- **suffix**: Directory name suffix
- **prefix**: Directory name prefix
- **dir**: Parent directory for temp directory

### Return Value
Returns the absolute path to the created directory (string)

### Key Features
- **Secure Creation**: Uses system `mkdtemp()` for race-free directory creation
- **Directory Path**: Returns path string, not file descriptor
- **Manual Cleanup**: No automatic deletion
- **Full Control**: Complete filesystem permissions

### Usage Examples

#### Basic Usage
```python
import tempfile
import shutil

# Create temporary directory
tmpdir = tempfile.mkdtemp(prefix='build_', suffix='_tmp')
print(f"Temporary directory: {tmpdir}")

# Use the directory
with open(f"{tmpdir}/data.txt", 'w') as f:
    f.write('temporary data')

# List contents
import os
files = os.listdir(tmpdir)
print(f"Files: {files}")

# Manual cleanup
shutil.rmtree(tmpdir)
```

#### Build Directory Example
```python
def compile_sources(source_files):
    tmpdir = tempfile.mkdtemp(prefix='compile_')

    try:
        # Copy sources
        for src in source_files:
            shutil.copy(src, tmpdir)

        # Compile
        result = run_compiler(tmpdir)

        # Move results
        shutil.move(os.path.join(tmpdir, 'output'), 'final_output')

        return result
    finally:
        # Ensure cleanup
        shutil.rmtree(tmpdir)
```

## Comparison: `mkstemp()` vs `mkdtemp()`

| Aspect | `mkstemp()` | `mkdtemp()` |
|--------|-------------|-------------|
| Returns | (fd, path) tuple | path string |
| Resource Type | File | Directory |
| Access Method | File descriptor | Directory path |
| Use Case | Single file operations | Multi-file workspaces |
| Cleanup | `os.unlink(path)` | `shutil.rmtree(path)` |

## Security Considerations

### Race-Free Creation
Both functions use system-level secure creation that prevents race conditions:

```python
# Secure: Atomic creation
fd, path = tempfile.mkstemp()

# Insecure: Separate name generation and creation (DON'T DO THIS)
name = tempfile.mktemp()  # Deprecated and unsafe
open(name, 'w')  # Race condition possible
```

### Permission Handling
- Files created with restrictive permissions (0o600 on Unix)
- Directories created with restrictive permissions (0o700 on Unix)
- Prevents unauthorized access to temporary resources

## Platform-Specific Behavior

### Unix/Linux
- Uses system `mkstemp()`/`mkdtemp()` calls
- Files in `/tmp` by default
- Proper permission masking

### Windows
- Uses `GetTempFileName()` and `CreateDirectory()` APIs
- Files in system temp directory
- Appropriate security descriptors

### macOS
- Inherits Unix behavior
- Additional security through sandboxing

## Error Handling

### Common Exceptions
- `OSError`: File system errors
- `PermissionError`: Insufficient permissions
- `FileNotFoundError`: Invalid directory specified

```python
try:
    fd, path = tempfile.mkstemp()
except OSError as e:
    if e.errno == errno.ENOSPC:
        raise DiskFullError("No space for temporary files")
    elif e.errno == errno.EACCES:
        raise PermissionError("Cannot create temp files in specified directory")
    else:
        raise
```

## Performance Characteristics

### Efficiency
- Direct system call integration
- Minimal Python overhead
- Optimized for temporary resource creation

### Resource Usage
- Low memory footprint
- No additional background processes
- Efficient for high-frequency temporary resource needs

## Best Practices

### Always Clean Up
```python
# Good: Always cleanup
fd, path = tempfile.mkstemp()
try:
    # use file
    pass
finally:
    os.close(fd)  # Close descriptor first
    os.unlink(path)  # Then remove file
```

### Use High-Level Alternatives When Possible
```python
# Prefer high-level classes for most cases
with tempfile.NamedTemporaryFile() as f:
    # Automatic cleanup
    pass

# Use mkstemp() only when you need the file descriptor
fd, path = tempfile.mkstemp()
# Manual management required
```

### Handle Interrupts
```python
import signal

def cleanup_handler(signum, frame):
    # Cleanup code
    shutil.rmtree(tmpdir)
    sys.exit(1)

signal.signal(signal.SIGINT, cleanup_handler)
signal.signal(signal.SIGTERM, cleanup_handler)

tmpdir = tempfile.mkdtemp()
# ... operations ...
```

## Integration Examples

### With `os` Module
```python
import os

# Create temp file and get its size
fd, path = tempfile.mkstemp()
with os.fdopen(fd, 'w') as f:
    f.write('data')

size = os.path.getsize(path)
os.unlink(path)
```

### With `subprocess`
```python
import subprocess

# Create temp script
fd, script_path = tempfile.mkstemp(suffix='.py')
with os.fdopen(fd, 'w') as f:
    f.write('#!/usr/bin/env python\nprint("Hello")')

os.chmod(script_path, 0o755)
result = subprocess.run([script_path], capture_output=True)
os.unlink(script_path)
```

### With `pathlib`
```python
from pathlib import Path

tmpdir = tempfile.mkdtemp()
tmp_path = Path(tmpdir)

# Use pathlib operations
(tmp_path / 'file.txt').write_text('content')
files = list(tmp_path.glob('*.txt'))

shutil.rmtree(tmpdir)
```

## When to Use Low-Level Functions

### When You Need File Descriptors
```python
# For low-level I/O operations
fd, path = tempfile.mkstemp()
# Use fd with os.read(), os.write(), etc.
```

### For System Integration
```python
# When passing to C extensions or system calls
fd, path = tempfile.mkstemp()
# Pass fd to C function
```

### For Maximum Control
```python
# When you need to manage lifecycle manually
fd, path = tempfile.mkstemp()
# Complex cleanup logic
```

`mkstemp()` and `mkdtemp()` provide the foundation for secure temporary resource creation in Python, offering maximum control for advanced use cases while requiring careful resource management.
