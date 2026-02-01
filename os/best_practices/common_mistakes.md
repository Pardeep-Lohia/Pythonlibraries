# Common Mistakes and Pitfalls

## Overview
This document outlines the most common mistakes developers make when working with the `os` module, along with solutions and best practices to avoid them.

## 1. Path Separator Issues

### ❌ Common Mistake: Hardcoding Path Separators
```python
# Wrong - platform dependent
path = 'folder/file.txt'  # Works on Unix, fails on Windows
path = 'folder\\file.txt'  # Works on Windows, fails on Unix

# Wrong - string concatenation
base_path = '/home/user'
full_path = base_path + '/documents/file.txt'  # Missing separator handling
```

### ✅ Solution: Use `os.path.join()`
```python
import os

# Correct - platform independent
path = os.path.join('folder', 'file.txt')

# Correct - handles separators automatically
base_path = '/home/user'
full_path = os.path.join(base_path, 'documents', 'file.txt')
```

## 2. Current Working Directory Assumptions

### ❌ Common Mistake: Assuming CWD
```python
# Wrong - assumes current working directory
with open('config.json', 'r') as f:
    config = json.load(f)

# Wrong - relative paths without context
log_path = '../logs/app.log'
```

### ✅ Solution: Use Absolute Paths
```python
import os

# Correct - use __file__ for module-relative paths
module_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(module_dir, 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)

# Correct - or use absolute paths
log_dir = os.path.abspath('../logs')
log_path = os.path.join(log_dir, 'app.log')
```

## 3. File Existence Checks

### ❌ Common Mistake: Not Checking File Existence
```python
# Wrong - may raise FileNotFoundError
with open('data.txt', 'r') as f:
    data = f.read()

# Wrong - incomplete checks
if os.path.exists(filepath):
    # File exists, but is it readable?
    with open(filepath, 'r') as f:
        data = f.read()
```

### ✅ Solution: Proper Existence and Permission Checks
```python
import os

def safe_read_file(filepath):
    """Safely read a file with proper checks."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if not os.path.isfile(filepath):
        raise ValueError(f"Path is not a file: {filepath}")

    if not os.access(filepath, os.R_OK):
        raise PermissionError(f"Cannot read file: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()
```

## 4. Environment Variable Handling

### ❌ Common Mistake: Unsafe Environment Variable Access
```python
# Wrong - KeyError if variable doesn't exist
database_url = os.environ['DATABASE_URL']

# Wrong - no validation
port = int(os.environ['PORT'])
```

### ✅ Solution: Safe Environment Variable Access
```python
import os

# Correct - use get() with defaults
database_url = os.environ.get('DATABASE_URL', 'sqlite:///default.db')

# Correct - validate and convert
port_str = os.environ.get('PORT', '8000')
try:
    port = int(port_str)
    if not (1024 <= port <= 65535):
        raise ValueError("Port out of range")
except ValueError:
    port = 8000
```

## 5. Directory Traversal Vulnerabilities

### ❌ Common Mistake: Path Traversal Attacks
```python
# Wrong - vulnerable to directory traversal
def read_file(user_input):
    filepath = os.path.join(BASE_DIR, user_input)
    with open(filepath, 'r') as f:
        return f.read()

# User could pass '../../../etc/passwd'
```

### ✅ Solution: Path Validation
```python
import os

def secure_path_join(base_dir, user_path):
    """Safely join paths without directory traversal."""
    # Normalize the path
    full_path = os.path.normpath(os.path.join(base_dir, user_path))

    # Ensure it stays within base directory
    base_abs = os.path.abspath(base_dir)
    full_abs = os.path.abspath(full_path)

    if not full_abs.startswith(base_abs):
        raise ValueError("Path traversal detected")

    return full_path
```

## 6. File Permission Issues

### ❌ Common Mistake: Ignoring Permissions
```python
# Wrong - assumes permissions
os.remove('/important/file.txt')

# Wrong - no permission checks
with open('/etc/passwd', 'w') as f:
    f.write('hacked')
```

### ✅ Solution: Check Permissions First
```python
import os

def safe_file_operation(filepath, operation='read'):
    """Perform file operation with permission checks."""
    if operation == 'read':
        if not os.access(filepath, os.R_OK):
            raise PermissionError(f"Cannot read: {filepath}")
    elif operation == 'write':
        if not os.access(filepath, os.W_OK):
            raise PermissionError(f"Cannot write: {filepath}")

    # Perform operation...
```

## 7. Resource Leaks

### ❌ Common Mistake: Not Closing File Handles
```python
# Wrong - resource leak
entries = os.scandir(directory)
for entry in entries:
    process_entry(entry)
# entries never closed
```

### ✅ Solution: Use Context Managers
```python
import os

# Correct - automatic cleanup
with os.scandir(directory) as entries:
    for entry in entries:
        process_entry(entry)

# Or manual cleanup
entries = os.scandir(directory)
try:
    for entry in entries:
        process_entry(entry)
finally:
    entries.close()
```

## 8. Cross-Platform Incompatibilities

### ❌ Common Mistake: Platform-Specific Code
```python
# Wrong - Windows only
if os.name == 'nt':
    command = 'dir'
else:
    command = 'ls'
# But what about other operations?
```

### ✅ Solution: Abstract Platform Differences
```python
import os

def list_directory_contents(directory):
    """Cross-platform directory listing."""
    try:
        return os.listdir(directory)
    except OSError:
        return []

def get_path_separator():
    """Get platform-specific path separator."""
    return os.sep

def is_windows():
    """Check if running on Windows."""
    return os.name == 'nt'

def is_unix():
    """Check if running on Unix-like system."""
    return os.name == 'posix'
```

## 9. Temporary File Mishandling

### ❌ Common Mistake: Insecure Temporary Files
```python
# Wrong - predictable names
temp_file = '/tmp/temp_' + str(os.getpid()) + '.txt'
with open(temp_file, 'w') as f:
    f.write('sensitive data')

# Wrong - no cleanup
import tempfile
temp = tempfile.NamedTemporaryFile(delete=False)
# File persists after program ends
```

### ✅ Solution: Secure Temporary Files
```python
import os
import tempfile

# Correct - secure temporary files
with tempfile.NamedTemporaryFile(mode='w', delete=True, suffix='.txt') as f:
    f.write('sensitive data')
    temp_path = f.name
    # File automatically deleted when context exits

# Correct - manual cleanup
with tempfile.NamedTemporaryFile(delete=False) as f:
    temp_path = f.name
    f.write('data')

try:
    # Use temp file
    process_file(temp_path)
finally:
    # Ensure cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)
```

## 10. Command Injection Vulnerabilities

### ❌ Common Mistake: Unsafe Command Execution
```python
# Wrong - command injection
filename = input("Enter filename: ")
os.system(f"rm {filename}")

# Wrong - shell injection
user_input = input("Enter command: ")
os.popen(user_input)
```

### ✅ Solution: Safe Command Execution
```python
import subprocess
import shlex

def safe_execute_command(command, *args):
    """Safely execute a command with arguments."""
    # Use subprocess with list arguments
    result = subprocess.run(
        [command] + list(args),
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

# Correct usage
filename = input("Enter filename: ")
# Validate filename first
if not any(char in filename for char in [';', '&', '|', '`', '$']):
    safe_execute_command('rm', filename)
else:
    print("Invalid filename")
```

## 11. Symlink Handling

### ❌ Common Mistake: Ignoring Symlinks
```python
# Wrong - may follow symlinks unexpectedly
if os.path.isfile(filepath):
    # This could be a symlink to a directory
    process_file(filepath)

# Wrong - recursive operations may follow symlinks
for root, dirs, files in os.walk(directory):
    for file in files:
        process_file(os.path.join(root, file))
```

### ✅ Solution: Explicit Symlink Handling
```python
import os

def process_path_safely(filepath):
    """Process a path with proper symlink handling."""
    if os.path.islink(filepath):
        # Handle symlink
        target = os.readlink(filepath)
        print(f"Symlink: {filepath} -> {target}")
        return

    if os.path.isfile(filepath):
        process_file(filepath)
    elif os.path.isdir(filepath):
        process_directory(filepath)

# For os.walk, use followlinks parameter
for root, dirs, files in os.walk(directory, followlinks=False):
    for file in files:
        filepath = os.path.join(root, file)
        process_path_safely(filepath)
```

## 12. Encoding Issues

### ❌ Common Mistake: Ignoring File Encoding
```python
# Wrong - assumes default encoding
with open('file.txt', 'r') as f:
    content = f.read()

# Wrong - no encoding specified for writing
with open('file.txt', 'w') as f:
    f.write(content)
```

### ✅ Solution: Explicit Encoding Handling
```python
import os

def read_file_with_encoding(filepath, encoding='utf-8'):
    """Read file with proper encoding handling."""
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # Try alternative encodings
        for alt_encoding in ['latin-1', 'cp1252']:
            try:
                with open(filepath, 'r', encoding=alt_encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise

def write_file_with_encoding(filepath, content, encoding='utf-8'):
    """Write file with proper encoding."""
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(content)
```

## 13. Race Conditions

### ❌ Common Mistake: TOCTOU Vulnerabilities
```python
# Wrong - Time of Check, Time of Use vulnerability
if os.path.exists(filepath):
    time.sleep(0.1)  # File could be deleted here
    with open(filepath, 'r') as f:
        data = f.read()
```

### ✅ Solution: Atomic Operations
```python
import os

def safe_file_read(filepath):
    """Safely read a file avoiding race conditions."""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except PermissionError:
        return None

# Or use os.open with flags
import os
def atomic_file_operation(filepath):
    """Perform atomic file operations."""
    try:
        fd = os.open(filepath, os.O_RDONLY)
        try:
            data = os.read(fd, 1024 * 1024)  # Read up to 1MB
            return data.decode('utf-8')
        finally:
            os.close(fd)
    except OSError:
        return None
```

## 14. Memory Issues with Large Directories

### ❌ Common Mistake: Loading All Files into Memory
```python
# Wrong - loads all filenames into memory
all_files = os.listdir('/large/directory')
for filename in all_files:
    process_file(filename)
```

### ✅ Solution: Iterator-Based Processing
```python
import os

def process_large_directory(directory):
    """Process large directories efficiently."""
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                process_file(entry.path)
                # Process one at a time to save memory
```

## 15. Ignoring Error Handling

### ❌ Common Mistake: No Error Handling
```python
# Wrong - crashes on any error
os.makedirs('/readonly/directory/new/folder')
os.remove('/nonexistent/file.txt')
```

### ✅ Solution: Comprehensive Error Handling
```python
import os
from errno import EEXIST, ENOENT, EACCES

def safe_makedirs(path, mode=0o755):
    """Safely create directories with error handling."""
    try:
        os.makedirs(path, mode=mode, exist_ok=True)
        return True
    except OSError as e:
        if e.errno == EACCES:
            print(f"Permission denied: {path}")
        elif e.errno == EEXIST:
            print(f"Directory already exists: {path}")
        else:
            print(f"Error creating directory {path}: {e}")
        return False

def safe_remove(filepath):
    """Safely remove a file with error handling."""
    try:
        os.remove(filepath)
        return True
    except OSError as e:
        if e.errno == ENOENT:
            print(f"File not found: {filepath}")
        elif e.errno == EACCES:
            print(f"Permission denied: {filepath}")
        else:
            print(f"Error removing file {filepath}: {e}")
        return False
```

## Summary

The most common mistakes when using the `os` module involve:
1. Path separator assumptions
2. Current working directory dependencies
3. Missing file existence and permission checks
4. Unsafe environment variable handling
5. Directory traversal vulnerabilities
6. Resource leaks
7. Cross-platform incompatibilities
8. Temporary file mishandling
9. Command injection vulnerabilities
10. Improper symlink handling
11. Encoding issues
12. Race conditions
13. Memory issues with large datasets
14. Poor error handling

Always use the appropriate `os.path` functions, check permissions, handle errors gracefully, and be aware of platform differences to avoid these pitfalls.
