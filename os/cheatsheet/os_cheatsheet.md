# Python `os` Module Cheatsheet

## Quick Reference Guide

### Path Operations (`os.path`)

#### Basic Path Functions
```python
import os

# Join paths (cross-platform)
path = os.path.join('home', 'user', 'file.txt')
# 'home/user/file.txt' (Unix) or 'home\\user\\file.txt' (Windows)

# Get absolute path
abs_path = os.path.abspath('file.txt')

# Normalize path (resolve . and ..)
norm_path = os.path.normpath('home/./user/../file.txt')
# 'home/file.txt'

# Get directory and filename
dirname = os.path.dirname('/home/user/file.txt')    # '/home/user'
basename = os.path.basename('/home/user/file.txt')  # 'file.txt'

# Split extension
root, ext = os.path.splitext('file.txt')  # ('file', '.txt')
```

#### Path Checking
```python
# Check existence and type
os.path.exists(path)      # True if path exists
os.path.isfile(path)      # True if regular file
os.path.isdir(path)       # True if directory
os.path.islink(path)      # True if symbolic link
os.path.ismount(path)     # True if mount point
```

#### Path Comparison
```python
os.path.samefile(path1, path2)    # Same file/directory
os.path.samestat(stat1, stat2)    # Same file status
```

### Directory Operations

#### Basic Directory Functions
```python
# Get current working directory
cwd = os.getcwd()

# Change directory
os.chdir('/home/user')

# Create directory
os.mkdir('new_dir')                    # Single level
os.makedirs('a/b/c', exist_ok=True)    # Recursive

# Remove directory
os.rmdir('empty_dir')                  # Must be empty
os.removedirs('a/b/c')                 # Remove recursively
```

#### Directory Listing
```python
# List directory contents
entries = os.listdir('.')              # List of strings
with os.scandir('.') as it:            # Iterator of DirEntry
    for entry in it:
        print(entry.name, entry.is_file())
```

#### Directory Traversal
```python
# Walk directory tree
for root, dirs, files in os.walk('start_dir'):
    print(f"Directory: {root}")
    print(f"Subdirs: {dirs}")
    print(f"Files: {files}")

    # Modify dirs to control traversal
    dirs[:] = [d for d in dirs if not d.startswith('.')]
```

### File Operations

#### File Information
```python
# Get file statistics
stat_info = os.stat('file.txt')
size = stat_info.st_size
modified = stat_info.st_mtime
mode = stat_info.st_mode

# File size
size = os.path.getsize('file.txt')

# Modification time
mtime = os.path.getmtime('file.txt')
atime = os.path.getatime('file.txt')

# Format time
import time
time.ctime(mtime)  # Human readable
```

#### File Permissions
```python
# Check permissions
os.access('file.txt', os.R_OK)    # Read permission
os.access('file.txt', os.W_OK)    # Write permission
os.access('file.txt', os.X_OK)    # Execute permission
os.access('file.txt', os.F_OK)    # File exists

# Change permissions
os.chmod('file.txt', 0o755)      # Octal notation
os.chmod('file.txt', stat.S_IRUSR | stat.S_IWUSR)  # Symbolic

# Change ownership (Unix)
os.chown('file.txt', uid, gid)
```

### Environment Variables

#### Basic Operations
```python
# Get environment variable
value = os.environ.get('HOME', '/tmp')
value = os.environ['HOME']              # Raises KeyError if missing

# Set environment variable
os.environ['MY_VAR'] = 'value'
os.environ.setdefault('MY_VAR', 'default')  # Only if not exists

# Remove environment variable
del os.environ['MY_VAR']
os.environ.pop('MY_VAR', None)
```

#### Common Environment Variables
```python
os.environ['HOME']        # User's home directory
os.environ['PATH']        # Executable search paths
os.environ['TMP']         # Temporary directory
os.environ['USER']        # Current user name
os.environ['PWD']         # Current working directory
```

### System Information

#### OS Information
```python
os.name                    # 'posix' or 'nt'
sys.platform              # 'linux', 'darwin', 'win32', etc.

# Detailed system info (Unix)
uname = os.uname()
print(uname.sysname)      # 'Linux'
print(uname.nodename)     # hostname
print(uname.release)      # kernel version
```

#### Process Information
```python
os.getpid()               # Current process ID
os.getppid()              # Parent process ID
os.getuid()               # User ID (Unix)
os.getgid()               # Group ID (Unix)
os.getlogin()             # Logged in user name
```

### System Commands

#### Command Execution
```python
# Execute command (deprecated, security issues)
exit_code = os.system('ls -la')

# Better: use subprocess
import subprocess
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
output = result.stdout
```

#### Process Management
```python
# Fork process (Unix only)
pid = os.fork()
if pid == 0:
    # Child process
    os.execvp('ls', ['ls', '-la'])
else:
    # Parent process
    os.waitpid(pid, 0)

# Spawn process
os.spawnlp(os.P_WAIT, 'ls', 'ls', '-la')
```

### File Descriptors (Advanced)

#### Low-level File Operations
```python
# Open file descriptor
fd = os.open('file.txt', os.O_RDONLY)

# Read from file descriptor
data = os.read(fd, 1024)

# Write to file descriptor
os.write(fd, b'data')

# Close file descriptor
os.close(fd)

# Duplicate file descriptor
new_fd = os.dup(fd)
```

### Cross-Platform Constants

#### Path Separators
```python
os.sep                    # '/' on Unix, '\\' on Windows
os.pathsep               # ':' on Unix, ';' on Windows
os.linesep               # '\\n' on Unix, '\\r\\n' on Windows
os.extsep                # '.' (extension separator)
```

#### Platform Detection
```python
if os.name == 'nt':
    # Windows-specific code
    pass
elif os.name == 'posix':
    # Unix-like systems
    pass
```

### Common Patterns

#### Safe Path Construction
```python
def safe_join(base, *paths):
    """Join paths safely."""
    path = os.path.normpath(os.path.join(base, *paths))
    if not path.startswith(os.path.abspath(base)):
        raise ValueError("Path traversal detected")
    return path
```

#### Temporary File Management
```python
import tempfile

# Create temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    temp_file = os.path.join(temp_dir, 'temp.txt')
    with open(temp_file, 'w') as f:
        f.write('temporary data')
    # Automatically cleaned up
```

#### Cross-Platform Home Directory
```python
home = os.environ.get('HOME') or os.environ.get('USERPROFILE')
```

#### File Size Formatting
```python
def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return ".1f"
        size /= 1024
    return ".1f"
```

#### Directory Size Calculation
```python
def dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        total += sum(os.path.getsize(os.path.join(root, f))
                    for f in files)
    return total
```

### Error Handling

#### Common Exceptions
```python
try:
    os.chdir('/nonexistent')
except FileNotFoundError:
    print("Directory not found")

try:
    os.remove('readonly_file.txt')
except PermissionError:
    print("Permission denied")

try:
    os.mkdir('/root/newdir')
except PermissionError:
    print("Permission denied")
```

### Performance Tips

#### Cache File Stats
```python
# Instead of multiple os.path.getsize() calls
stats = {}
for root, dirs, files in os.walk('.'):
    for file in files:
        path = os.path.join(root, file)
        stats[path] = os.stat(path)

# Use cached stats
large_files = [p for p, s in stats.items() if s.st_size > 1024*1024]
```

#### Use `os.scandir()` for Large Directories
```python
# More efficient than os.listdir() + os.stat()
with os.scandir('.') as entries:
    files = [e.name for e in entries if e.is_file()]
```

### Security Considerations

#### Avoid Command Injection
```python
# Dangerous
os.system(f"rm {user_input}")

# Safe
import subprocess
subprocess.run(['rm', user_input], check=True)
```

#### Validate Paths
```python
# Check for path traversal
if '..' in user_path or user_path.startswith('/'):
    raise ValueError("Invalid path")
```

### Integration with Other Modules

#### With `pathlib`
```python
from pathlib import Path

# Convert between os and pathlib
path_obj = Path(os.getcwd())
path_str = str(Path.home())
```

#### With `shutil`
```python
import shutil

# High-level file operations
shutil.copy('source.txt', 'dest.txt')      # Copy file
shutil.move('file.txt', 'new_location/')   # Move file
shutil.rmtree('directory/')                # Remove directory tree
```

#### With `glob`
```python
import glob

# Pattern matching
txt_files = glob.glob('*.txt')
recursive_py = glob.glob('**/*.py', recursive=True)
```

### Quick Command Reference

| Function | Purpose | Example |
|----------|---------|---------|
| `os.getcwd()` | Get current directory | `os.getcwd()` |
| `os.chdir(path)` | Change directory | `os.chdir('/tmp')` |
| `os.listdir(path)` | List directory | `os.listdir('.')` |
| `os.mkdir(path)` | Create directory | `os.mkdir('new')` |
| `os.path.join()` | Join paths | `os.path.join('a', 'b')` |
| `os.path.exists()` | Check existence | `os.path.exists('file')` |
| `os.path.isfile()` | Check if file | `os.path.isfile('file')` |
| `os.path.isdir()` | Check if directory | `os.path.isdir('dir')` |
| `os.stat(path)` | Get file stats | `os.stat('file')` |
| `os.environ.get()` | Get env var | `os.environ.get('HOME')` |
| `os.system(cmd)` | Run command | `os.system('ls')` |
| `os.walk(path)` | Walk directory tree | `os.walk('.')` |

This cheatsheet provides quick access to the most commonly used `os` module functions and patterns.
