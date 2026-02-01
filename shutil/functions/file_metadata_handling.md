# File Metadata Handling Functions in `shutil`

The `shutil` module provides functions for manipulating file metadata such as permissions, timestamps, and ownership. These functions allow fine-grained control over file attributes beyond basic copying operations.

## `shutil.copymode(src, dst, *, follow_symlinks=True)`

### Purpose
Copy the permission mode (file permissions) from source to destination without copying file content or other metadata.

### Syntax
```python
shutil.copymode(src, dst, *, follow_symlinks=True)
```

### Parameters
- `src`: Source file path
- `dst`: Destination file path
- `follow_symlinks`: If `True` (default), follow symbolic links; if `False`, operate on the link itself

### Return Value
None

### Example
```python
import shutil
import os

# Create a file with specific permissions
with open('source.txt', 'w') as f:
    f.write('test content')

# Set restrictive permissions on source
os.chmod('source.txt', 0o600)  # Owner read/write only

# Create destination file
with open('destination.txt', 'w') as f:
    f.write('different content')

# Copy permissions from source to destination
shutil.copymode('source.txt', 'destination.txt')

# Verify permissions are copied
print(f"Source permissions: {oct(os.stat('source.txt').st_mode)}")
print(f"Dest permissions: {oct(os.stat('destination.txt').st_mode)}")
```

### Edge Cases
- Only copies permission bits, not ownership or timestamps
- Works on both files and directories
- May fail if destination doesn't exist or lacks write permissions

## `shutil.copystat(src, dst, *, follow_symlinks=True)`

### Purpose
Copy all file metadata (permissions, timestamps, and other attributes) from source to destination.

### Syntax
```python
shutil.copystat(src, dst, *, follow_symlinks=True)
```

### Parameters
- `src`: Source file path
- `dst`: Destination file path
- `follow_symlinks`: If `True` (default), follow symbolic links; if `False`, operate on the link itself

### Return Value
None

### Example
```python
import shutil
import os
import time

# Create source file and set its metadata
with open('source.txt', 'w') as f:
    f.write('source content')

# Set specific permissions and timestamps
os.chmod('source.txt', 0o755)
os.utime('source.txt', (time.time() - 3600, time.time() - 1800))  # 1 hour ago

# Create destination file
with open('dest.txt', 'w') as f:
    f.write('dest content')

print("Before copystat:")
print(f"Source: mode={oct(os.stat('source.txt').st_mode)}, mtime={os.stat('source.txt').st_mtime}")
print(f"Dest: mode={oct(os.stat('dest.txt').st_mode)}, mtime={os.stat('dest.txt').st_mtime}")

# Copy all metadata
shutil.copystat('source.txt', 'dest.txt')

print("\nAfter copystat:")
print(f"Source: mode={oct(os.stat('source.txt').st_mode)}, mtime={os.stat('source.txt').st_mtime}")
print(f"Dest: mode={oct(os.stat('dest.txt').st_mode)}, mtime={os.stat('dest.txt').st_mtime}")
```

### Edge Cases
- Copies permissions, access time, modification time, and change time
- May not copy all attributes on all platforms (e.g., extended attributes)
- Requires appropriate permissions to modify destination metadata

## `shutil.chown(path, user=None, group=None, *, follow_symlinks=True)`

### Purpose
Change the owner and/or group of a file or directory (Unix-like systems only).

### Syntax
```python
shutil.chown(path, user=None, group=None, *, follow_symlinks=True)
```

### Parameters
- `path`: Path to the file or directory
- `user`: New owner (username string or UID integer)
- `group`: New group (group name string or GID integer)
- `follow_symlinks`: If `True` (default), follow symbolic links; if `False`, operate on the link itself

### Return Value
None

### Example
```python
import shutil
import os

# Create a test file
with open('test_file.txt', 'w') as f:
    f.write('test')

# Change owner to 'www-data' user
try:
    shutil.chown('test_file.txt', user='www-data')
    print("Owner changed to www-data")
except OSError as e:
    print(f"Failed to change owner: {e}")

# Change group to 'developers'
try:
    shutil.chown('test_file.txt', group='developers')
    print("Group changed to developers")
except OSError as e:
    print(f"Failed to change group: {e}")

# Change both user and group using numeric IDs
try:
    shutil.chown('test_file.txt', user=1000, group=1000)
    print("Owner and group changed to UID/GID 1000")
except OSError as e:
    print(f"Failed to change ownership: {e}")

# Get current ownership
stat = os.stat('test_file.txt')
print(f"Current UID: {stat.st_uid}, GID: {stat.st_gid}")
```

### Edge Cases
- Only available on Unix-like systems (Linux, macOS)
- Not available on Windows
- Requires appropriate permissions (usually root)
- Can operate on directories recursively with `os.walk()`

## Advanced Metadata Operations

### Preserving Metadata During Copy
```python
import shutil
import os

def copy_with_metadata_preservation(src, dst):
    """Copy file while preserving all possible metadata"""
    # First copy the file content
    shutil.copy2(src, dst)  # copy2 already preserves most metadata

    # For additional metadata preservation (platform-dependent)
    try:
        # Try to preserve extended attributes (Linux)
        import xattr
        attrs = xattr.getxattr(src, 'user.mime_type')
        xattr.setxattr(dst, 'user.mime_type', attrs)
    except (ImportError, OSError):
        pass  # Extended attributes not supported or available

    return dst

# Usage
copy_with_metadata_preservation('important.doc', 'backup.doc')
```

### Batch Permission Changes
```python
import shutil
import os
from pathlib import Path

def set_directory_permissions_recursive(path, mode):
    """Set permissions recursively for all files in directory"""
    path = Path(path)

    for item in path.rglob('*'):
        if item.is_file():
            try:
                os.chmod(item, mode)
            except OSError:
                print(f"Could not change permissions for {item}")

def normalize_permissions(base_path):
    """Normalize permissions for a project directory"""
    base_path = Path(base_path)

    # Set directory permissions
    for dir_path in base_path.rglob('*'):
        if dir_path.is_dir():
            try:
                os.chmod(dir_path, 0o755)  # rwxr-xr-x
            except OSError:
                pass

    # Set file permissions
    for file_path in base_path.rglob('*'):
        if file_path.is_file():
            try:
                os.chmod(file_path, 0o644)  # rw-r--r--
            except OSError:
                pass

# Usage
normalize_permissions('/path/to/project')
```

### Timestamp Management
```python
import shutil
import os
import time
from pathlib import Path

def preserve_timestamps(src_dir, dst_dir):
    """Copy directory while preserving all timestamps"""
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)

    # Copy directory structure
    shutil.copytree(src_path, dst_path)

    # Preserve timestamps for all items
    for src_item in src_path.rglob('*'):
        relative_path = src_item.relative_to(src_path)
        dst_item = dst_path / relative_path

        if dst_item.exists():
            # Copy timestamps
            stat = src_item.stat()
            os.utime(dst_item, (stat.st_atime, stat.st_mtime))

def touch_files_recursively(path, timestamp=None):
    """Update timestamps recursively"""
    if timestamp is None:
        timestamp = time.time()

    path = Path(path)
    for item in path.rglob('*'):
        try:
            os.utime(item, (timestamp, timestamp))
        except OSError:
            pass

# Usage
preserve_timestamps('source_project', 'timestamped_backup')
touch_files_recursively('cache_directory')  # Update all to current time
```

### Ownership Management
```python
import shutil
import os
import pwd
import grp
from pathlib import Path

def change_ownership_recursive(path, user=None, group=None):
    """Change ownership recursively (Unix only)"""
    if os.name == 'nt':
        print("Ownership changes not supported on Windows")
        return

    path = Path(path)

    # Convert names to IDs if needed
    uid = None
    gid = None

    if user:
        if isinstance(user, str):
            uid = pwd.getpwnam(user).pw_uid
        else:
            uid = user

    if group:
        if isinstance(group, str):
            gid = grp.getgrnam(group).gr_gid
        else:
            gid = group

    for item in path.rglob('*'):
        try:
            shutil.chown(item, user=uid, group=gid)
        except OSError as e:
            print(f"Could not change ownership of {item}: {e}")

def get_ownership_info(path):
    """Get detailed ownership information"""
    stat = os.stat(path)

    try:
        user_name = pwd.getpwuid(stat.st_uid).pw_name
    except KeyError:
        user_name = f"UID {stat.st_uid}"

    try:
        group_name = grp.getgrgid(stat.st_gid).gr_name
    except KeyError:
        group_name = f"GID {stat.st_gid}"

    return {
        'uid': stat.st_uid,
        'gid': stat.st_gid,
        'user': user_name,
        'group': group_name
    }

# Usage (Unix only)
ownership = get_ownership_info('/etc/passwd')
print(f"Owner: {ownership['user']} ({ownership['uid']})")
print(f"Group: {ownership['group']} ({ownership['gid']})")

# Change ownership recursively
change_ownership_recursive('/var/www/html', user='www-data', group='www-data')
```

## Cross-Platform Metadata Handling

### Platform-Aware Metadata Operations
```python
import shutil
import os
import platform

def copy_metadata_cross_platform(src, dst):
    """Copy metadata with platform awareness"""
    system = platform.system()

    # Basic metadata copy (works everywhere)
    try:
        shutil.copystat(src, dst)
    except OSError:
        pass  # Some platforms may not support all metadata

    # Platform-specific operations
    if system == 'Linux':
        # Copy extended attributes
        try:
            import xattr
            for key in xattr.listxattr(src):
                if key.startswith('user.'):
                    value = xattr.getxattr(src, key)
                    xattr.setxattr(dst, key, value)
        except ImportError:
            pass

    elif system == 'Darwin':  # macOS
        # Copy resource fork or extended attributes
        try:
            import xattr
            for key in xattr.listxattr(src):
                value = xattr.getxattr(src, key)
                xattr.setxattr(dst, key, value)
        except ImportError:
            pass

    elif system == 'Windows':
        # Windows-specific attributes (limited support)
        # Note: Windows permissions are handled by copystat
        pass

def get_file_attributes(path):
    """Get comprehensive file attributes"""
    stat = os.stat(path)
    attrs = {
        'size': stat.st_size,
        'mode': oct(stat.st_mode),
        'uid': stat.st_uid,
        'gid': stat.st_gid,
        'atime': stat.st_atime,
        'mtime': stat.st_mtime,
        'ctime': stat.st_ctime
    }

    # Platform-specific attributes
    system = platform.system()
    if system != 'Windows':
        try:
            attrs['user'] = pwd.getpwuid(stat.st_uid).pw_name
            attrs['group'] = grp.getgrgid(stat.st_gid).gr_name
        except (ImportError, KeyError):
            pass

    return attrs

# Usage
attrs = get_file_attributes('important_file.txt')
for key, value in attrs.items():
    print(f"{key}: {value}")
```

## Error Handling

Metadata operations can fail for various reasons:

```python
import shutil

def safe_metadata_copy(src, dst):
    """Copy metadata with comprehensive error handling"""
    errors = []

    try:
        shutil.copymode(src, dst)
    except OSError as e:
        errors.append(f"Failed to copy mode: {e}")

    try:
        shutil.copystat(src, dst)
    except OSError as e:
        errors.append(f"Failed to copy stat: {e}")

    # Ownership change (Unix only)
    if hasattr(os, 'chown') and os.name != 'nt':
        try:
            src_stat = os.stat(src)
            shutil.chown(dst, user=src_stat.st_uid, group=src_stat.st_gid)
        except OSError as e:
            errors.append(f"Failed to copy ownership: {e}")

    return errors

# Usage
errors = safe_metadata_copy('source.txt', 'dest.txt')
if errors:
    print("Metadata copy completed with warnings:")
    for error in errors:
        print(f"  {error}")
else:
    print("All metadata copied successfully")
```

## Performance Considerations

- Metadata operations are generally fast (system calls)
- Recursive ownership changes can be slow on large directory trees
- Extended attribute operations may have platform-specific performance
- Consider caching metadata for bulk operations

## Security Considerations

1. **Permission Validation**: Always check permissions before metadata changes
2. **Ownership Risks**: Changing ownership can have security implications
3. **Path Safety**: Validate paths to prevent directory traversal
4. **Platform Differences**: Be aware of platform-specific security models

## Best Practices

1. **Preserve Metadata**: Use `copy2()` for most copying operations to maintain metadata
2. **Handle Errors Gracefully**: Metadata operations can fail due to permissions
3. **Platform Awareness**: Test on all target platforms
4. **Minimal Changes**: Only modify necessary metadata attributes
5. **Backup Before Changes**: Critical files should be backed up before metadata changes
6. **Use Appropriate Functions**: Choose the right function for the specific metadata needs
7. **Document Changes**: Keep track of intentional metadata modifications

These functions provide essential tools for managing file metadata across different platforms and use cases, from simple permission copying to complex ownership management in multi-user environments.
