# Version and Release Information Functions

This section covers the `platform` library functions that provide detailed version and release information about the operating system and platform.

## platform.release()

### Purpose
Returns the system's release version.

### Syntax
```python
platform.release()
```

### Example
```python
import platform

release = platform.release()
print(f"System release: {release}")
# Output: System release: 5.4.0-74-generic (Linux)
#         System release: 10 (Windows)
#         System release: 20.6.0 (macOS)
```

### Edge Cases
- Format varies significantly between operating systems
- On Linux, includes kernel version details
- On Windows, returns major version number
- On macOS, returns Darwin kernel version

## platform.version()

### Purpose
Returns the system's version information.

### Syntax
```python
platform.version()
```

### Example
```python
import platform

version = platform.version()
print(f"System version: {version}")
# Output: System version: #74-Ubuntu SMP Wed Sep 29 16:43:40 UTC 2021 (Linux)
#         System version: 10.0.19043 (Windows)
```

### Edge Cases
- Very detailed and platform-specific
- On Linux, includes build information and date
- On Windows, includes build number
- Can be quite long and technical

## platform.uname() - Version Fields

### Purpose
The `uname()` function includes version-related fields.

### Version-Specific Fields
```python
import platform

info = platform.uname()
print(f"Release: {info.release}")    # System release
print(f"Version: {info.version}")    # System version
```

### Example
```python
import platform

info = platform.uname()
print("Version Information:")
print(f"  Release: {info.release}")
print(f"  Version: {info.version}")

# Output:
# Version Information:
#   Release: 5.4.0-74-generic
#   Version: #74-Ubuntu SMP Wed Sep 29 16:43:40 UTC 2021
```

### Edge Cases
- Release is more standardized than version
- Version field contains very detailed information

## platform.platform()

### Purpose
Returns a single string summarizing platform information including version.

### Syntax
```python
platform.platform(aliased=True, terse=False)
```

### Parameters
- `aliased` (bool): Use human-readable aliases
- `terse` (bool): Return shortened version

### Example
```python
import platform

# Full platform string
full_platform = platform.platform()
print(f"Full platform: {full_platform}")
# Output: Full platform: Linux-5.4.0-74-generic-x86_64-with-Ubuntu-20.04.3-LTS

# Terse version
terse_platform = platform.platform(terse=True)
print(f"Terse platform: {terse_platform}")
# Output: Terse platform: Linux-5.4.0-74-generic
```

### Edge Cases
- Includes Python version and distribution info
- Very long string with full information
- Aliased version is more readable

## Advanced Version Parsing

### Linux Kernel Version Parsing
```python
import platform

def parse_linux_kernel_version():
    """Parse Linux kernel version into components."""
    release = platform.release()

    try:
        # Linux kernel version format: major.minor.patch-extra
        parts = release.split('-')[0].split('.')
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2]) if len(parts) > 2 else 0

        return {
            'major': major,
            'minor': minor,
            'patch': patch,
            'full': release
        }
    except (ValueError, IndexError):
        return {'error': 'Could not parse kernel version'}

kernel_info = parse_linux_kernel_version()
print(f"Kernel version: {kernel_info}")
```

### Windows Version Parsing
```python
import platform

def parse_windows_version():
    """Parse Windows version information."""
    release, version, csd, ptype = platform.win32_ver()

    try:
        # Windows version format: major.minor.build
        version_parts = version.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1])
        build = int(version_parts[2]) if len(version_parts) > 2 else 0

        return {
            'release': release,
            'major': major,
            'minor': minor,
            'build': build,
            'service_pack': csd,
            'product_type': ptype
        }
    except (ValueError, IndexError, AttributeError):
        return {'error': 'Could not parse Windows version'}

win_info = parse_windows_version()
print(f"Windows version: {win_info}")
```

### macOS Version Parsing
```python
import platform

def parse_macos_version():
    """Parse macOS version information."""
    release, versioninfo, machine = platform.mac_ver()

    try:
        # macOS release format: major.minor.patch
        version_parts = release.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else 0
        patch = int(version_parts[2]) if len(version_parts) > 2 else 0

        return {
            'release': release,
            'major': major,
            'minor': minor,
            'patch': patch,
            'machine': machine
        }
    except (ValueError, IndexError):
        return {'error': 'Could not parse macOS version'}

mac_info = parse_macos_version()
print(f"macOS version: {mac_info}")
```

## Version Comparison Functions

### Cross-Platform Version Comparison
```python
import platform

def compare_system_versions(min_version_req):
    """Compare current system version against requirements."""
    system = platform.system()

    if system == 'Linux':
        current = platform.release().split('-')[0]  # Get base kernel version
        return version_compare(current, min_version_req)
    elif system == 'Windows':
        release, version, _, _ = platform.win32_ver()
        current = f"{release}.{version}"
        return version_compare(current, min_version_req)
    elif system == 'Darwin':
        current = platform.mac_ver()[0]
        return version_compare(current, min_version_req)
    else:
        return False

def version_compare(current, required):
    """Simple version comparison (simplified implementation)."""
    try:
        current_parts = list(map(int, current.split('.')))
        required_parts = list(map(int, required.split('.')))

        # Pad shorter version with zeros
        max_len = max(len(current_parts), len(required_parts))
        current_parts.extend([0] * (max_len - len(current_parts)))
        required_parts.extend([0] * (max_len - len(required_parts)))

        return current_parts >= required_parts
    except (ValueError, AttributeError):
        return False

# Example usage
is_supported = compare_system_versions('5.0.0')  # Linux kernel 5.0+
print(f"System version supported: {is_supported}")
```

### Feature Detection Based on Version
```python
import platform

def check_version_features():
    """Check available features based on system version."""
    system = platform.system()
    features = {}

    if system == 'Linux':
        kernel_ver = platform.release().split('-')[0]
        try:
            major, minor = map(int, kernel_ver.split('.')[:2])
            features['kernel_major'] = major
            features['kernel_minor'] = minor

            # Feature availability based on kernel version
            features['has_epoll'] = (major, minor) >= (2, 6)
            features['has_inotify'] = (major, minor) >= (2, 6)
            features['has_namespaces'] = (major, minor) >= (2, 6)
            features['has_cgroups'] = (major, minor) >= (2, 6)

        except (ValueError, IndexError):
            features['error'] = 'Could not parse kernel version'

    elif system == 'Windows':
        release, version, _, _ = platform.win32_ver()
        try:
            major = int(version.split('.')[0])
            features['windows_major'] = major

            # Windows version features
            features['has_wsl'] = major >= 10
            features['has_windows_store'] = major >= 8
            features['has_uwp'] = major >= 10

        except (ValueError, IndexError):
            features['error'] = 'Could not parse Windows version'

    elif system == 'Darwin':
        release, _, _ = platform.mac_ver()
        try:
            major = int(release.split('.')[0])
            features['macos_major'] = major

            # macOS version features
            features['has_metal'] = major >= 10
            features['has_catalyst'] = major >= 10
            features['has_m1_support'] = major >= 11

        except (ValueError, IndexError):
            features['error'] = 'Could not parse macOS version'

    return features

version_features = check_version_features()
print(f"Version-based features: {version_features}")
```

## Version Logging and Diagnostics

### Comprehensive Version Report
```python
import platform

def generate_version_report():
    """Generate a comprehensive version report."""
    report = {
        'system': platform.system(),
        'platform': platform.platform(),
        'uname': platform.uname()._asdict()
    }

    system = platform.system()
    if system == 'Linux':
        try:
            dist_info = platform.freedesktop_os_release()
            report['distribution'] = dist_info
        except:
            report['distribution'] = platform.linux_distribution()
    elif system == 'Windows':
        report['windows_info'] = platform.win32_ver()
        report['windows_edition'] = platform.win32_edition()
    elif system == 'Darwin':
        report['mac_info'] = platform.mac_ver()

    return report

version_report = generate_version_report()
print("Version Report:")
for key, value in version_report.items():
    print(f"  {key}: {value}")
```

### Version Compatibility Checking
```python
import platform

def check_compatibility(requirements):
    """
    Check system compatibility against requirements.

    Args:
        requirements: dict with system requirements
        Example: {
            'min_kernel': '5.0.0',  # Linux
            'min_windows': '10.0',  # Windows
            'min_macos': '10.15'    # macOS
        }
    """
    system = platform.system()
    compatible = True
    issues = []

    if system == 'Linux':
        current_kernel = platform.release().split('-')[0]
        min_kernel = requirements.get('min_kernel')
        if min_kernel and not version_compare(current_kernel, min_kernel):
            compatible = False
            issues.append(f"Kernel version {current_kernel} < required {min_kernel}")

    elif system == 'Windows':
        _, version, _, _ = platform.win32_ver()
        min_windows = requirements.get('min_windows')
        if min_windows and not version_compare(version, min_windows):
            compatible = False
            issues.append(f"Windows version {version} < required {min_windows}")

    elif system == 'Darwin':
        release, _, _ = platform.mac_ver()
        min_macos = requirements.get('min_macos')
        if min_macos and not version_compare(release, min_macos):
            compatible = False
            issues.append(f"macOS version {release} < required {min_macos}")

    return {
        'compatible': compatible,
        'issues': issues,
        'current_system': system,
        'current_version': get_current_version_string()
    }

def get_current_version_string():
    """Get current system version as string."""
    system = platform.system()
    if system == 'Linux':
        return platform.release()
    elif system == 'Windows':
        _, version, _, _ = platform.win32_ver()
        return version
    elif system == 'Darwin':
        return platform.mac_ver()[0]
    else:
        return platform.version()

requirements = {
    'min_kernel': '4.0.0',
    'min_windows': '10.0',
    'min_macos': '10.12'
}

compatibility = check_compatibility(requirements)
print(f"Compatibility check: {compatibility}")
```

## Best Practices

### Safe Version Parsing
```python
import platform

def safe_version_parsing():
    """Safely parse version information with error handling."""
    try:
        system = platform.system()
        release = platform.release()
        version = platform.version()

        # Attempt to parse version numbers
        parsed_version = {'raw': version}

        if system == 'Linux':
            # Parse kernel version
            kernel_parts = release.split('-')[0].split('.')
            if len(kernel_parts) >= 2:
                parsed_version['kernel_major'] = int(kernel_parts[0])
                parsed_version['kernel_minor'] = int(kernel_parts[1])

        elif system == 'Windows':
            win_release, win_version, _, _ = platform.win32_ver()
            parsed_version['windows_release'] = win_release
            parsed_version['windows_version'] = win_version

        elif system == 'Darwin':
            mac_release, _, _ = platform.mac_ver()
            parsed_version['macos_release'] = mac_release

        return parsed_version

    except Exception as e:
        return {'error': str(e), 'raw': platform.version()}

safe_versions = safe_version_parsing()
print(f"Safe version parsing: {safe_versions}")
```

### Version Caching for Performance
```python
import platform

class VersionCache:
    """Cache version information for performance."""

    def __init__(self):
        self._cache = {}

    def get_system_info(self):
        """Get cached system information."""
        if 'system_info' not in self._cache:
            self._cache['system_info'] = {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'platform': platform.platform(),
                'uname': platform.uname()
            }
        return self._cache['system_info']

    def get_distribution_info(self):
        """Get cached distribution information."""
        if 'dist_info' not in self._cache:
            system = self.get_system_info()['system']
            if system == 'Linux':
                try:
                    self._cache['dist_info'] = platform.freedesktop_os_release()
                except:
                    self._cache['dist_info'] = platform.linux_distribution()
            elif system == 'Windows':
                self._cache['dist_info'] = platform.win32_ver()
            elif system == 'Darwin':
                self._cache['dist_info'] = platform.mac_ver()
            else:
                self._cache['dist_info'] = {}

        return self._cache['dist_info']

# Usage
cache = VersionCache()
system_info = cache.get_system_info()
dist_info = cache.get_distribution_info()

print(f"Cached system info: {system_info}")
print(f"Cached distribution info: {dist_info}")
```

These functions provide comprehensive access to system version and release information, enabling developers to write version-aware and compatibility-checking code.
