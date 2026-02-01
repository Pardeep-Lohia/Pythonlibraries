# OS Information Functions

## Overview
The `os` module provides functions to retrieve information about the operating system, hardware, and current process. These functions are essential for writing portable code that adapts to different environments.

## System Identification

### `os.name` - Operating System Name
**Purpose**: Returns a string identifying the operating system.

**Return Values**:
- `'posix'`: Unix-like systems (Linux, macOS, BSD, etc.)
- `'nt'`: Windows NT family (Windows NT, 2000, XP, Vista, 7, 8, 10)
- `'java'`: Jython (Java implementation of Python)

**Examples**:
```python
import os

print(f"OS family: {os.name}")

# Platform-specific code
if os.name == 'nt':
    print("Running on Windows")
    path_sep = '\\'
elif os.name == 'posix':
    print("Running on Unix-like system")
    path_sep = '/'
else:
    print("Running on Java platform")
```

### `sys.platform` - Detailed Platform Information
**Purpose**: More specific platform identification (requires `sys` module).

**Common Values**:
- `'linux'`: Linux
- `'darwin'`: macOS
- `'win32'`: 32-bit Windows
- `'win64'`: 64-bit Windows (Python 3.8+)
- `'cygwin'`: Cygwin on Windows
- `'freebsd'`: FreeBSD
- `'openbsd'`: OpenBSD

**Examples**:
```python
import sys

print(f"Detailed platform: {sys.platform}")

# More specific detection
if sys.platform.startswith('win'):
    print("Windows system")
elif sys.platform == 'darwin':
    print("macOS system")
elif sys.platform.startswith('linux'):
    print("Linux system")
```

### `platform` Module Integration
**Purpose**: Comprehensive platform information (requires `platform` module).

**Examples**:
```python
import platform

print(f"System: {platform.system()}")
print(f"Release: {platform.release()}")
print(f"Version: {platform.version()}")
print(f"Machine: {platform.machine()}")
print(f"Processor: {platform.processor()}")
print(f"Python version: {platform.python_version()}")
```

## System Information

### `os.uname()` - System Information (Unix-like)
**Purpose**: Returns system information as a named tuple.

**Return Value**: `posix.uname_result` with attributes:
- `sysname`: Operating system name
- `nodename`: Network name (hostname)
- `release`: OS release
- `version`: OS version
- `machine`: Hardware identifier

**Examples**:
```python
import os

try:
    uname_info = os.uname()
    print(f"System: {uname_info.sysname}")
    print(f"Node: {uname_info.nodename}")
    print(f"Release: {uname_info.release}")
    print(f"Version: {uname_info.version}")
    print(f"Machine: {uname_info.machine}")
except AttributeError:
    print("os.uname() not available on this platform")
```

### `os.ctermid()` - Controlling Terminal
**Purpose**: Returns the filename of the controlling terminal.

**Examples**:
```python
import os

try:
    terminal = os.ctermid()
    print(f"Controlling terminal: {terminal}")
except AttributeError:
    print("os.ctermid() not available on this platform")
```

### `os.getloadavg()` - System Load Average (Unix)
**Purpose**: Returns the system load average as a tuple.

**Return Value**: 3-tuple of (1min, 5min, 15min) load averages

**Examples**:
```python
import os

try:
    load_avg = os.getloadavg()
    print(f"Load average: {load_avg[0]:.2f} (1min), {load_avg[1]:.2f} (5min), {load_avg[2]:.2f} (15min)")
except AttributeError:
    print("os.getloadavg() not available on this platform")
```

## Process Information

### `os.getpid()` - Current Process ID
**Purpose**: Returns the current process ID.

**Examples**:
```python
import os

pid = os.getpid()
print(f"Current process ID: {pid}")
```

### `os.getppid()` - Parent Process ID
**Purpose**: Returns the parent process ID.

**Examples**:
```python
import os

ppid = os.getppid()
print(f"Parent process ID: {ppid}")
```

### `os.getuid()` / `os.getgid()` - User/Group IDs (Unix)
**Purpose**: Returns the current process's user/group ID.

**Examples**:
```python
import os

try:
    uid = os.getuid()
    gid = os.getgid()
    print(f"User ID: {uid}, Group ID: {gid}")
except AttributeError:
    print("User/Group ID functions not available on this platform")
```

### `os.geteuid()` / `os.getegid()` - Effective User/Group IDs (Unix)
**Purpose**: Returns the current process's effective user/group ID.

**Examples**:
```python
import os

try:
    euid = os.geteuid()
    egid = os.getegid()
    print(f"Effective User ID: {euid}, Effective Group ID: {egid}")
except AttributeError:
    print("Effective User/Group ID functions not available on this platform")
```

### `os.getgroups()` - Supplementary Group IDs (Unix)
**Purpose**: Returns list of supplementary group IDs.

**Examples**:
```python
import os

try:
    groups = os.getgroups()
    print(f"Supplementary groups: {groups}")
except AttributeError:
    print("os.getgroups() not available on this platform")
```

### `os.getlogin()` - User Login Name
**Purpose**: Returns the name of the user logged in on the controlling terminal.

**Examples**:
```python
import os

try:
    login = os.getlogin()
    print(f"Logged in user: {login}")
except OSError:
    print("Could not determine logged in user")
```

## Environment Information

### `os.getcwd()` - Current Working Directory
**Purpose**: Returns the current working directory.

**Examples**:
```python
import os

cwd = os.getcwd()
print(f"Current working directory: {cwd}")
```

### `os.getcwdb()` - Current Working Directory (Bytes)
**Purpose**: Returns the current working directory as bytes.

**Examples**:
```python
import os

cwdb = os.getcwdb()
print(f"Current working directory (bytes): {cwdb}")
```

### `os.environ` - Environment Variables
**Purpose**: Dictionary-like object containing environment variables.

**Examples**:
```python
import os

# Get specific environment variable
home = os.environ.get('HOME', os.environ.get('USERPROFILE', '/tmp'))
print(f"Home directory: {home}")

# Check if variable exists
if 'PATH' in os.environ:
    path_dirs = os.environ['PATH'].split(os.pathsep)
    print(f"PATH contains {len(path_dirs)} directories")

# Get all environment variables
print(f"Total environment variables: {len(os.environ)}")
```

## System Limits and Configuration

### `os.sysconf(name)` - System Configuration (Unix)
**Purpose**: Returns system configuration information.

**Common Names**:
- `'SC_PAGE_SIZE'`: System page size
- `'SC_OPEN_MAX'`: Maximum number of open files
- `'SC_NPROCESSORS_ONLN'`: Number of online processors

**Examples**:
```python
import os

try:
    page_size = os.sysconf('SC_PAGE_SIZE')
    max_files = os.sysconf('SC_OPEN_MAX')
    cpu_count = os.sysconf('SC_NPROCESSORS_ONLN')

    print(f"Page size: {page_size} bytes")
    print(f"Max open files: {max_files}")
    print(f"CPU count: {cpu_count}")
except (AttributeError, ValueError):
    print("System configuration not available")
```

### `os.confstr(name)` - Configuration Strings (Unix)
**Purpose**: Returns system configuration strings.

**Examples**:
```python
import os

try:
    path_max = os.confstr('CS_PATH')
    print(f"Maximum path length: {path_max}")
except (AttributeError, ValueError):
    print("Configuration strings not available")
```

### `os.pathconf(path, name)` - Path Configuration
**Purpose**: Returns system configuration information for a path.

**Examples**:
```python
import os

try:
    # Maximum filename length
    name_max = os.pathconf('/', 'PC_NAME_MAX')
    print(f"Maximum filename length: {name_max}")

    # Maximum path length
    path_max = os.pathconf('/', 'PC_PATH_MAX')
    print(f"Maximum path length: {path_max}")
except (AttributeError, OSError):
    print("Path configuration not available")
```

## File System Information

### `os.statvfs(path)` - File System Statistics
**Purpose**: Returns file system statistics.

**Return Value**: `statvfs_result` with attributes:
- `f_bsize`: Fundamental file system block size
- `f_frsize`: Fragment size
- `f_blocks`: Total number of blocks
- `f_bfree`: Number of free blocks
- `f_bavail`: Number of available blocks
- `f_files`: Total number of file nodes
- `f_ffree`: Number of free file nodes
- `f_favail`: Number of available file nodes

**Examples**:
```python
import os

try:
    statvfs = os.statvfs('/')

    # Calculate sizes
    total_bytes = statvfs.f_blocks * statvfs.f_frsize
    free_bytes = statvfs.f_bavail * statvfs.f_frsize
    used_bytes = total_bytes - free_bytes

    print(f"Total space: {total_bytes / (1024**3):.2f} GB")
    print(f"Free space: {free_bytes / (1024**3):.2f} GB")
    print(f"Used space: {used_bytes / (1024**3):.2f} GB")
    print(f"Usage: {(used_bytes / total_bytes * 100):.1f}%")

except AttributeError:
    print("os.statvfs() not available on this platform")
```

## Cross-Platform System Detection

### Comprehensive Platform Detection
```python
import os
import sys
import platform

def get_system_info():
    """Get comprehensive system information."""
    info = {
        'os_family': os.name,
        'platform': sys.platform,
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version()
    }

    # OS-specific information
    if os.name == 'posix':
        try:
            uname_info = os.uname()
            info.update({
                'sysname': uname_info.sysname,
                'nodename': uname_info.nodename,
                'os_release': uname_info.release,
                'os_version': uname_info.version,
                'architecture': uname_info.machine
            })
        except AttributeError:
            pass

        # Process information
        try:
            info['pid'] = os.getpid()
            info['ppid'] = os.getppid()
            info['uid'] = os.getuid()
            info['gid'] = os.getgid()
            info['login'] = os.getlogin()
        except AttributeError:
            pass

    elif os.name == 'nt':
        info['pid'] = os.getpid()
        info['ppid'] = os.getppid()

    # Environment information
    info['cwd'] = os.getcwd()
    info['env_vars'] = len(os.environ)

    # File system information
    try:
        statvfs = os.statvfs('/')
        info['fs_block_size'] = statvfs.f_bsize
        info['fs_total_blocks'] = statvfs.f_blocks
        info['fs_free_blocks'] = statvfs.f_bfree
    except AttributeError:
        pass

    return info

# Usage
system_info = get_system_info()
for key, value in system_info.items():
    print(f"{key}: {value}")
```

### Platform-Specific Code Organization
```python
import os
import sys

class PlatformDetector:
    """Cross-platform system detection and adaptation."""

    def __init__(self):
        self.os_family = os.name
        self.platform = sys.platform
        self.is_windows = os.name == 'nt'
        self.is_posix = os.name == 'posix'
        self.is_linux = sys.platform.startswith('linux')
        self.is_macos = sys.platform == 'darwin'
        self.is_freebsd = sys.platform.startswith('freebsd')

    def get_path_separator(self):
        """Get platform-appropriate path separator."""
        return '\\' if self.is_windows else '/'

    def get_path_list_separator(self):
        """Get platform-appropriate path list separator."""
        return ';' if self.is_windows else ':'

    def get_default_shell(self):
        """Get default shell for the platform."""
        if self.is_windows:
            return os.environ.get('COMSPEC', 'cmd.exe')
        else:
            return os.environ.get('SHELL', '/bin/sh')

    def get_temp_directory(self):
        """Get platform-appropriate temporary directory."""
        return os.environ.get('TMP', os.environ.get('TEMP', '/tmp'))

    def get_home_directory(self):
        """Get user's home directory."""
        return os.environ.get('HOME', os.environ.get('USERPROFILE', '/tmp'))

# Usage
detector = PlatformDetector()
print(f"OS Family: {detector.os_family}")
print(f"Platform: {detector.platform}")
print(f"Path separator: {detector.get_path_separator()}")
print(f"Home directory: {detector.get_home_directory()}")
```

## Best Practices

### 1. Use Multiple Detection Methods
```python
# Good: Check both os.name and sys.platform
if os.name == 'posix' and sys.platform == 'darwin':
    print("Running on macOS")
elif os.name == 'nt':
    print("Running on Windows")
else:
    print("Running on other POSIX system")
```

### 2. Handle Platform Differences Gracefully
```python
def get_username():
    """Get current username in a cross-platform way."""
    # Try multiple methods
    username = os.environ.get('USER') or os.environ.get('USERNAME')

    if username:
        return username

    # Fallback to login
    try:
        return os.getlogin()
    except OSError:
        return 'unknown'

username = get_username()
print(f"Current user: {username}")
```

### 3. Test for Feature Availability
```python
def safe_uname():
    """Get uname info safely."""
    try:
        return os.uname()
    except AttributeError:
        # Windows doesn't have os.uname()
        return None

uname_info = safe_uname()
if uname_info:
    print(f"System: {uname_info.sysname}")
else:
    print("uname not available on this platform")
```

### 4. Use Appropriate Modules for Specific Information
```python
import os
import platform
import sys

def get_comprehensive_system_info():
    """Get system information using appropriate modules."""

    info = {
        'basic': {
            'os_family': os.name,
            'platform': sys.platform,
            'system': platform.system(),
            'release': platform.release()
        },
        'process': {
            'pid': os.getpid(),
            'ppid': os.getppid(),
            'cwd': os.getcwd()
        },
        'environment': {
            'variables': len(os.environ),
            'path_dirs': len(os.environ.get('PATH', '').split(os.pathsep))
        }
    }

    # Add POSIX-specific info
    if os.name == 'posix':
        try:
            uname = os.uname()
            info['posix'] = {
                'sysname': uname.sysname,
                'machine': uname.machine,
                'version': uname.version
            }
        except AttributeError:
            pass

    return info

system_info = get_comprehensive_system_info()
print(system_info)
```

### 5. Cache Expensive Operations
```python
import os
import functools

@functools.lru_cache(maxsize=1)
def get_system_config():
    """Cache system configuration (expensive operation)."""
    config = {}

    try:
        config['page_size'] = os.sysconf('SC_PAGE_SIZE')
        config['cpu_count'] = os.sysconf('SC_NPROCESSORS_ONLN')
        config['max_files'] = os.sysconf('SC_OPEN_MAX')
    except (AttributeError, ValueError):
        pass

    return config

# Usage
config = get_system_config()  # Computed once, cached thereafter
print(f"CPU count: {config.get('cpu_count', 'unknown')}")
```

These functions provide essential information about the operating system and execution environment, enabling cross-platform compatibility and system-aware programming.
