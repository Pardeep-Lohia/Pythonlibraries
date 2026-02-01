# File Metadata and Permissions

## Overview
The `os` module provides functions to access and modify file metadata (timestamps, size, permissions) and manage file permissions. These operations are essential for file system management and security.

## File Statistics (`os.stat`)

### `os.stat(path)` - Get File Status
**Purpose**: Returns file status information as a `stat_result` object.

**Syntax**:
```python
os.stat(path)
```

**Return Value**: `stat_result` object with file attributes

**Common Attributes**:
- `st_mode`: File mode (permissions)
- `st_ino`: Inode number
- `st_dev`: Device
- `st_nlink`: Number of hard links
- `st_uid`: User ID of owner
- `st_gid`: Group ID of owner
- `st_size`: Size in bytes
- `st_atime`: Last access time
- `st_mtime`: Last modification time
- `st_ctime`: Creation time (or last metadata change)

**Example**:
```python
import os
from datetime import datetime

stat_info = os.stat('file.txt')
print(f"Size: {stat_info.st_size} bytes")
print(f"Modified: {datetime.fromtimestamp(stat_info.st_mtime)}")
print(f"Permissions: {oct(stat_info.st_mode)}")
```

### `os.lstat(path)` - Get Symbolic Link Status
**Purpose**: Like `stat()`, but doesn't follow symbolic links.

**Syntax**:
```python
os.lstat(path)
```

**Use Case**: Check if a path is a symbolic link itself.

## Timestamp Operations

### `os.utime(path, times=None)` - Set File Timestamps
**Purpose**: Sets access and modification times of a file.

**Syntax**:
```python
os.utime(path, times=None)
```

**Parameters**:
- `path`: File path
- `times`: Tuple of (atime, mtime) or None for current time

**Examples**:
```python
import os
import time

# Set to current time
os.utime('file.txt')

# Set specific times
one_hour_ago = time.time() - 3600
os.utime('file.txt', (one_hour_ago, one_hour_ago))

# Copy timestamps from another file
source_stat = os.stat('source.txt')
os.utime('dest.txt', (source_stat.st_atime, source_stat.st_mtime))
```

## Permission Management

### `os.chmod(path, mode)` - Change File Mode
**Purpose**: Changes the mode (permissions) of a file.

**Syntax**:
```python
os.chmod(path, mode)
```

**Parameters**:
- `path`: File or directory path
- `mode`: Permission mode (integer)

**Permission Constants**:
```python
import os
import stat

# Owner permissions
stat.S_IRUSR  # Read
stat.S_IWUSR  # Write
stat.S_IXUSR  # Execute

# Group permissions
stat.S_IRGRP  # Read
stat.S_IWGRP  # Write
stat.S_IXGRP  # Execute

# Others permissions
stat.S_IROTH  # Read
stat.S_IWOTH  # Write
stat.S_IXOTH  # Execute

# Special bits
stat.S_ISUID  # Set user ID
stat.S_ISGID  # Set group ID
stat.S_ISVTX  # Sticky bit
```

**Examples**:
```python
import os
import stat

# Make file readable/writable by owner only
os.chmod('secret.txt', stat.S_IRUSR | stat.S_IWUSR)

# Make script executable
os.chmod('script.py', 0o755)  # rwxr-xr-x

# Add execute permission for owner
current_mode = os.stat('file.txt').st_mode
os.chmod('file.txt', current_mode | stat.S_IXUSR)
```

### `os.chown(path, uid, gid)` - Change File Owner
**Purpose**: Changes the owner and group of a file.

**Syntax**:
```python
os.chown(path, uid, gid)
```

**Parameters**:
- `path`: File path
- `uid`: User ID (-1 to leave unchanged)
- `gid`: Group ID (-1 to leave unchanged)

**Example**:
```python
import os

# Change owner to user ID 1000, keep group
os.chown('file.txt', 1000, -1)

# Change both owner and group
os.chown('file.txt', 1000, 1000)
```

**Note**: Requires appropriate privileges (usually root).

## File Ownership

### `os.getuid()` - Get User ID
**Purpose**: Returns the current process's user ID.

**Syntax**:
```python
os.getuid()
```

### `os.getgid()` - Get Group ID
**Purpose**: Returns the current process's group ID.

**Syntax**:
```python
os.getgid()
```

### `os.geteuid()` - Get Effective User ID
**Purpose**: Returns the current process's effective user ID.

**Syntax**:
```python
os.geteuid()
```

### `os.getegid()` - Get Effective Group ID
**Purpose**: Returns the current process's effective group ID.

**Syntax**:
```python
os.getegid()
```

## Advanced Permission Operations

### `os.access(path, mode)` - Check Access Permissions
**Purpose**: Checks if the current user has access to a file.

**Syntax**:
```python
os.access(path, mode)
```

**Parameters**:
- `path`: File path
- `mode`: Access mode flags

**Mode Flags**:
- `os.R_OK`: Read permission
- `os.W_OK`: Write permission
- `os.X_OK`: Execute permission
- `os.F_OK`: File exists

**Examples**:
```python
import os

# Check if file exists
if os.access('file.txt', os.F_OK):
    print("File exists")

# Check read permission
if os.access('file.txt', os.R_OK):
    print("Can read file")

# Check read and write
if os.access('file.txt', os.R_OK | os.W_OK):
    print("Can read and write file")
```

**Note**: This checks effective permissions, not just file permissions.

### `os.umask(mask)` - Set File Creation Mask
**Purpose**: Sets the umask for new file creation.

**Syntax**:
```python
os.umask(mask)
```

**Parameters**:
- `mask`: Permission mask

**Example**:
```python
import os

# Set umask so new files have 0o644 permissions
old_umask = os.umask(0o022)
print(f"Old umask: {oct(old_umask)}")
```

## File System Information

### `os.statvfs(path)` - Get File System Statistics
**Purpose**: Returns file system statistics.

**Syntax**:
```python
os.statvfs(path)
```

**Return Value**: `statvfs_result` object with attributes like:
- `f_bsize`: Block size
- `f_frsize`: Fragment size
- `f_blocks`: Total blocks
- `f_bfree`: Free blocks
- `f_bavail`: Available blocks

**Example**:
```python
import os

statvfs = os.statvfs('/')
total_bytes = statvfs.f_blocks * statvfs.f_frsize
free_bytes = statvfs.f_bavail * statvfs.f_frsize
print(f"Total: {total_bytes / (1024**3):.2f} GB")
print(f"Free: {free_bytes / (1024**3):.2f} GB")
```

## Best Practices

### Permission Management
1. **Use symbolic constants** instead of octal literals
2. **Check permissions** before operations when necessary
3. **Preserve existing permissions** when modifying
4. **Handle permission errors** gracefully

### Timestamp Handling
1. **Use `os.path.getmtime()`** for simple modification time
2. **Convert timestamps** using `datetime.fromtimestamp()`
3. **Preserve timestamps** when copying files

### Cross-Platform Considerations
1. **File permissions** work differently on Windows vs Unix
2. **Owner information** may not be available on all systems
3. **Timestamps** have different resolutions on different systems

## Common Patterns

### Safe File Operations with Permission Checks
```python
import os
import stat

def safe_write_file(filepath, content):
    """Write content to file with proper permissions."""
    # Check if we can write
    if not os.access(os.path.dirname(filepath), os.W_OK):
        raise PermissionError(f"No write permission for {filepath}")

    # Write file
    with open(filepath, 'w') as f:
        f.write(content)

    # Set restrictive permissions
    os.chmod(filepath, stat.S_IRUSR | stat.S_IWUSR)

    return True
```

### File Age Checker
```python
import os
import time
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Get file age in days."""
    stat_info = os.stat(filepath)
    file_time = datetime.fromtimestamp(stat_info.st_mtime)
    age = datetime.now() - file_time
    return age.days

def find_old_files(directory, days_old=30):
    """Find files older than specified days."""
    old_files = []
    cutoff_time = time.time() - (days_old * 24 * 60 * 60)

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if os.stat(filepath).st_mtime < cutoff_time:
                old_files.append(filepath)

    return old_files
```

### Permission Analyzer
```python
import os
import stat

def analyze_permissions(filepath):
    """Analyze file permissions in detail."""
    stat_info = os.stat(filepath)
    mode = stat_info.st_mode

    permissions = {
        'owner': {
            'read': bool(mode & stat.S_IRUSR),
            'write': bool(mode & stat.S_IWUSR),
            'execute': bool(mode & stat.S_IXUSR)
        },
        'group': {
            'read': bool(mode & stat.S_IRGRP),
            'write': bool(mode & stat.S_IWGRP),
            'execute': bool(mode & stat.S_IXGRP)
        },
        'others': {
            'read': bool(mode & stat.S_IROTH),
            'write': bool(mode & stat.S_IWOTH),
            'execute': bool(mode & stat.S_IXOTH)
        }
    }

    return permissions
```

These functions provide comprehensive control over file metadata and permissions in a cross-platform manner.
