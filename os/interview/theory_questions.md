# OS Module Theory Interview Questions

## Overview
This document contains theoretical interview questions about Python's `os` module, covering core concepts, functionality, and best practices.

## Core Concepts

### 1. What is the `os` module in Python?
**Answer:** The `os` module is a standard library module in Python that provides a way to interact with the operating system. It allows Python programs to perform operating system-dependent functionality like reading or writing to the file system, managing processes, and accessing environment variables. The module provides a portable way of using operating system dependent functionality.

### 2. How does `os` differ from `os.path`?
**Answer:** The `os` module provides general operating system functionality, while `os.path` is specifically for path manipulations. `os.path` contains functions for pathname manipulations that are cross-platform, such as joining paths, splitting paths, and checking if paths exist. The `os` module handles broader OS operations like file I/O, process management, and environment variables.

### 3. What are the main categories of functions in the `os` module?
**Answer:** The main categories are:
- **File and Directory Operations**: `os.listdir()`, `os.mkdir()`, `os.remove()`, `os.rename()`
- **Path Operations**: `os.path.join()`, `os.path.exists()`, `os.path.isfile()`
- **Process Management**: `os.system()`, `os.execv()`, `os.fork()` (Unix only)
- **Environment Variables**: `os.environ`, `os.getenv()`, `os.putenv()`
- **System Information**: `os.name`, `os.uname()`, `os.getpid()`
- **Permissions**: `os.access()`, `os.chmod()`, `os.chown()`

### 4. Explain the difference between `os.listdir()` and `os.scandir()`.
**Answer:** `os.listdir(path)` returns a list of filenames in the specified directory, loading all entries into memory at once. `os.scandir(path)` returns an iterator of `DirEntry` objects, which is more memory-efficient for large directories. `os.scandir()` also provides additional information about each entry (like file type and stat info) without requiring separate `os.stat()` calls.

### 5. What is the purpose of `os.path.join()` and why is it important?
**Answer:** `os.path.join()` intelligently joins path components using the appropriate path separator for the operating system (`/` on Unix/Linux, `\` on Windows). It's important because it ensures cross-platform compatibility and handles edge cases like multiple consecutive separators or absolute paths correctly, preventing bugs when code runs on different operating systems.

## Path Handling

### 6. Explain absolute vs relative paths and how `os` handles them.
**Answer:** An absolute path starts from the root directory (e.g., `/home/user/file.txt` on Unix, `C:\Users\user\file.txt` on Windows). A relative path is relative to the current working directory (e.g., `file.txt`, `../parent/file.txt`).

The `os` module provides:
- `os.path.isabs(path)` - checks if a path is absolute
- `os.path.abspath(path)` - converts relative paths to absolute
- `os.getcwd()` - gets current working directory
- `os.chdir(path)` - changes current working directory

### 7. How do you safely construct file paths to prevent directory traversal attacks?
**Answer:** Use `os.path.normpath()` to normalize the path, then check that the resulting absolute path starts with the intended base directory:

```python
import os

def safe_path_join(base_dir, user_path):
    full_path = os.path.normpath(os.path.join(base_dir, user_path))
    base_abs = os.path.abspath(base_dir)
    full_abs = os.path.abspath(full_path)

    if not full_abs.startswith(base_abs):
        raise ValueError("Path traversal detected")

    return full_path
```

### 8. What are the differences between `os.walk()` and `os.scandir()`?
**Answer:** `os.walk()` recursively traverses a directory tree, yielding a 3-tuple `(dirpath, dirnames, filenames)` for each directory. It's designed for recursive traversal.

`os.scandir()` only looks at a single directory level, returning `DirEntry` objects. For recursive traversal with `os.scandir()`, you need to implement the recursion yourself, but it gives you more control and can be more efficient.

## File Operations

### 9. How do you check if a file exists and is readable before opening it?
**Answer:** Use a combination of `os.path.exists()`, `os.path.isfile()`, and `os.access()`:

```python
import os

def safe_file_read(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if not os.path.isfile(filepath):
        raise ValueError(f"Path is not a file: {filepath}")

    if not os.access(filepath, os.R_OK):
        raise PermissionError(f"Cannot read file: {filepath}")

    with open(filepath, 'r') as f:
        return f.read()
```

### 10. Explain the difference between `os.remove()` and `os.unlink()`.
**Answer:** They are the same function - `os.unlink()` is the Unix system call name, and `os.remove()` is the more generic name. On Windows, `os.remove()` can delete read-only files, while `os.unlink()` cannot. In practice, `os.remove()` is preferred for cross-platform code.

### 11. How do you get file metadata like size, modification time, and permissions?
**Answer:** Use `os.stat()` or `os.lstat()` (for symlinks):

```python
import os
from datetime import datetime

stat_info = os.stat(filepath)
file_size = stat_info.st_size
mod_time = datetime.fromtimestamp(stat_info.st_mtime)
permissions = oct(stat_info.st_mode)[-3:]
```

## Environment Variables

### 12. How do you safely access environment variables?
**Answer:** Use `os.environ.get(key, default)` instead of `os.environ[key]` to avoid KeyError:

```python
import os

# Safe access with default
database_url = os.environ.get('DATABASE_URL', 'sqlite:///default.db')

# Safe conversion
port_str = os.environ.get('PORT', '8000')
try:
    port = int(port_str)
except ValueError:
    port = 8000
```

### 13. How do you modify environment variables for the current process?
**Answer:** Use `os.environ[key] = value` to set, and `del os.environ[key]` to delete. Changes only affect the current process and its children:

```python
import os

# Set environment variable
os.environ['MY_VAR'] = 'my_value'

# Delete environment variable
if 'MY_VAR' in os.environ:
    del os.environ['MY_VAR']
```

## Process Management

### 14. What are the security implications of using `os.system()`?
**Answer:** `os.system()` can be vulnerable to command injection attacks if user input is not properly sanitized. It passes the command string to the shell, which can interpret shell metacharacters. For example:

```python
# Vulnerable
filename = input("Enter filename: ")
os.system(f"rm {filename}")  # Dangerous if filename contains "; rm -rf /"
```

Use `subprocess` module instead for safer command execution.

### 15. How do you get information about the current process?
**Answer:** Use various `os` functions:
- `os.getpid()` - current process ID
- `os.getppid()` - parent process ID
- `os.getcwd()` - current working directory
- `os.getuid()` / `os.getgid()` - user/group ID (Unix only)
- `os.environ` - environment variables

## Cross-Platform Considerations

### 16. How does the `os` module handle cross-platform compatibility?
**Answer:** The `os` module abstracts platform differences:
- `os.name` returns `'posix'`, `'nt'`, or `'java'` to identify the platform
- `os.sep` gives the path separator (`'/'` or `'\\'`)
- `os.linesep` gives the line separator (`'\n'` or `'\r\n'`)
- Functions like `os.path.join()` automatically use correct separators
- Some functions are platform-specific (e.g., `os.fork()` only on Unix)

### 17. What are the differences in file permissions between Unix and Windows?
**Answer:** Unix has complex permission systems with read/write/execute for user/group/others. Windows has simpler permissions (read-only vs full access) but also supports ACLs. The `os` module provides:
- `os.access()` - checks permissions in a cross-platform way
- `os.chmod()` - sets permissions (mode parameter differs by platform)
- `os.chown()` - changes ownership (Unix only)

## Best Practices

### 18. Why should you use `os.path.join()` instead of string concatenation?
**Answer:** `os.path.join()`:
- Automatically uses correct path separators
- Handles absolute paths correctly
- Prevents double separators
- Is more readable and maintainable

### 19. How do you handle temporary files safely?
**Answer:** Use the `tempfile` module instead of manual temporary file creation:

```python
import tempfile

# Safe temporary file
with tempfile.NamedTemporaryFile(mode='w', delete=True) as f:
    temp_path = f.name
    f.write('temporary data')
    # File automatically deleted when context exits
```

### 20. What are some common pitfalls when using the `os` module?
**Answer:** Common pitfalls include:
- Assuming current working directory
- Hardcoding path separators
- Not checking file existence before operations
- Using `os.system()` with user input
- Ignoring permissions
- Not handling symlinks properly
- Race conditions (TOCTOU vulnerabilities)

## Advanced Topics

### 21. Explain the concept of file descriptors and how `os` handles them.
**Answer:** File descriptors are integer handles that the OS uses to identify open files. The `os` module provides low-level file operations:
- `os.open()` - opens a file, returns file descriptor
- `os.read(fd, n)` / `os.write(fd, data)` - read/write using descriptors
- `os.close(fd)` - closes file descriptor
- `os.dup()` / `os.dup2()` - duplicates descriptors

These are lower-level than Python's built-in `open()` function.

### 22. How does `os.walk()` work internally and what are its performance considerations?
**Answer:** `os.walk()` uses `os.listdir()` and `os.stat()` internally. For each directory, it:
1. Lists all entries with `os.listdir()`
2. Calls `os.stat()` on each entry to determine if it's a file or directory
3. Yields the 3-tuple for the current directory
4. Recursively processes subdirectories

Performance considerations:
- Loads all directory entries into memory at once
- Makes many `os.stat()` calls
- Can be slow for deep directory trees
- Consider `os.scandir()` for better performance

### 23. What are the differences between `os.stat()`, `os.lstat()`, and `os.fstat()`?
**Answer:** All return file statistics, but:
- `os.stat(path)` - follows symlinks, returns info about the target
- `os.lstat(path)` - doesn't follow symlinks, returns info about the link itself
- `os.fstat(fd)` - takes a file descriptor instead of path, returns info about the open file

### 24. How do you handle Unicode filenames with the `os` module?
**Answer:** Python 3 handles Unicode filenames automatically. The `os` module works with Unicode strings:
- Paths are Unicode strings by default
- `os.listdir()` returns Unicode filenames
- Use proper encoding when reading/writing files
- Be aware of filesystem encoding limitations

### 25. Explain the concept of umask and how it affects file creation.
**Answer:** umask (user mask) is a Unix concept that determines default permissions for newly created files. The `os` module provides:
- `os.umask(mask)` - sets the umask and returns the old one
- Default file permissions = 0666 & ~umask
- Default directory permissions = 0777 & ~umask

For example, with umask 022, files get permissions 644, directories get 755.
