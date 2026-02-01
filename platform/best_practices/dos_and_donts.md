# Do's and Don'ts for Using the `platform` Module

## Do's

### ✅ Cache Platform Information
**Do** cache platform information that doesn't change during program execution.

```python
# Good: Cache platform info
import platform

class SystemInfo:
    def __init__(self):
        self._system = platform.system()
        self._machine = platform.machine()
        self._python_version = platform.python_version()

    @property
    def system(self):
        return self._system

# Usage
sys_info = SystemInfo()
if sys_info.system == 'Windows':
    # Windows-specific code
```

### ✅ Use Platform for Feature Detection
**Do** use platform information to detect available features.

```python
import platform

def get_path_separator():
    """Get appropriate path separator for the platform."""
    if platform.system() == 'Windows':
        return '\\'
    else:
        return '/'

# Better: use os.path.sep
import os
separator = os.path.sep
```

### ✅ Handle Errors Gracefully
**Do** handle cases where platform information might not be available.

```python
import platform

def safe_get_machine():
    """Safely get machine information."""
    try:
        machine = platform.machine()
        return machine if machine else 'unknown'
    except Exception:
        return 'unknown'
```

### ✅ Combine with Other Modules
**Do** use platform information alongside other system modules.

```python
import platform
import os
import sys

def get_system_info():
    return {
        'platform_system': platform.system(),
        'os_name': os.name,
        'sys_platform': sys.platform,
        'python_version': platform.python_version()
    }
```

### ✅ Test on Multiple Platforms
**Do** test your code on all supported platforms.

```python
# Use conditional logic that works across platforms
import platform

def get_config_path():
    system = platform.system()
    if system == 'Windows':
        return os.path.expanduser('~\\AppData\\Local\\MyApp')
    elif system == 'Darwin':
        return os.path.expanduser('~/Library/Application Support/MyApp')
    else:  # Linux and other Unix-like
        return os.path.expanduser('~/.config/myapp')
```

### ✅ Document Platform Dependencies
**Do** document platform-specific behavior in your code.

```python
def create_temp_file():
    """
    Create a temporary file.

    Note: On Windows, this uses the system temp directory.
    On Unix-like systems, it uses /tmp or equivalent.
    """
    import tempfile
    return tempfile.NamedTemporaryFile(delete=False)
```

### ✅ Use Semantic Version Comparison
**Do** use proper version comparison for feature detection.

```python
import platform

def supports_feature():
    """Check if platform supports a specific feature."""
    system = platform.system()
    release = platform.release()

    if system == 'Linux':
        # Parse kernel version properly
        kernel_ver = release.split('-')[0]
        major, minor = map(int, kernel_ver.split('.')[:2])
        return (major, minor) >= (4, 9)  # Example requirement

    return False
```

## Don'ts

### ❌ Don't Use Platform for Security
**Don't** use platform information for security decisions.

```python
# Bad: Using platform for security
import platform

def is_admin():
    # This is not reliable for security!
    if platform.system() == 'Windows':
        # Windows-specific check
        pass
    return False

# Good: Use proper security libraries
import os
if os.name == 'nt':  # Windows
    import ctypes
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
else:
    is_admin = os.geteuid() == 0
```

### ❌ Don't Hardcode Platform Strings
**Don't** hardcode platform strings without validation.

```python
# Bad: Hardcoded strings
if platform.system() == 'win32':  # May not work on all systems
    pass

# Good: Use documented values
if platform.system() == 'Windows':
    pass
```

### ❌ Don't Assume Platform Capabilities
**Don't** assume capabilities based on platform alone.

```python
# Bad: Assuming all Linux systems have systemd
import platform

if platform.system() == 'Linux':
    # Not all Linux distros use systemd!
    use_systemd = True

# Good: Detect capabilities
def detect_init_system():
    # Actual detection logic here
    pass
```

### ❌ Don't Use Deprecated Functions
**Don't** use deprecated platform functions.

```python
# Bad: Using deprecated linux_distribution()
import platform

distro = platform.linux_distribution()  # Deprecated in Python 3.8+

# Good: Use modern alternatives
try:
    info = platform.freedesktop_os_release()
except AttributeError:
    # Fallback for older Python versions
    pass
```

### ❌ Don't Rely Solely on Platform for Compatibility
**Don't** use only platform information for compatibility checks.

```python
# Bad: Only checking platform
import platform

if platform.system() == 'Windows':
    # Assume Windows 10+ features available
    use_modern_features = True

# Good: Check actual capabilities
import sys
if sys.getwindowsversion().major >= 10:
    use_modern_features = True
```

### ❌ Don't Make Performance-Critical Decisions
**Don't** use platform checks in performance-critical loops.

```python
# Bad: Platform check in loop
import platform

for item in large_list:
    if platform.system() == 'Windows':
        process_windows(item)
    else:
        process_unix(item)

# Good: Check once outside loop
import platform

is_windows = platform.system() == 'Windows'
for item in large_list:
    if is_windows:
        process_windows(item)
    else:
        process_unix(item)
```

### ❌ Don't Ignore Virtualization
**Don't** ignore that systems might be virtualized.

```python
# Bad: Assuming physical hardware
cpu_count = os.cpu_count()  # Might be virtual CPUs

# Good: Be aware of virtualization
cpu_count = os.cpu_count()
if cpu_count > 64:  # Unusually high count
    print("Warning: This might be a virtualized environment")
```

### ❌ Don't Use Platform for User Interface Decisions
**Don't** use platform alone for UI decisions.

```python
# Bad: Platform-based UI decisions
if platform.system() == 'Darwin':
    use_cocoa_ui = True

# Good: Use actual UI framework detection
try:
    import Cocoa
    use_cocoa_ui = True
except ImportError:
    use_cocoa_ui = False
```

### ❌ Don't Forget About Edge Cases
**Don't** forget about unusual platform configurations.

```python
# Bad: Not handling WSL
if platform.system() == 'Linux':
    use_linux_paths = True

# Good: Handle WSL and other edge cases
system = platform.system()
release = platform.release()

if system == 'Linux':
    if 'Microsoft' in release:  # WSL
        # Special handling for WSL
        pass
    else:
        use_linux_paths = True
```

## Summary

- **Cache** platform information to avoid repeated calls
- **Combine** platform with other modules for robust detection
- **Test** on multiple platforms
- **Handle errors** gracefully
- **Don't use** platform for security decisions
- **Don't assume** capabilities based on platform alone
- **Don't ignore** virtualization and edge cases
- **Document** platform-specific behavior

Following these guidelines will help you write more robust, maintainable, and cross-platform compatible Python code.
