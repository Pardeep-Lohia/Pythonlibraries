# OS Distribution Information Functions

This section covers the `platform` library functions that provide detailed information about specific operating system distributions and versions.

## platform.linux_distribution()

### Purpose
Returns information about the Linux distribution (deprecated in Python 3.8+).

### Syntax
```python
platform.linux_distribution(full_distribution_name=True)
```

### Parameters
- `full_distribution_name` (bool): If True, returns full distribution name

### Example
```python
import platform

distro_name, version, codename = platform.linux_distribution()
print(f"Distribution: {distro_name} {version} ({codename})")
# Output: Distribution: Ubuntu 20.04.3 LTS (focal)
```

### Edge Cases
- Deprecated in Python 3.8+, use `distro` module instead
- May not work on all Linux distributions
- Returns ('', '', '') if unable to determine

## platform.mac_ver()

### Purpose
Returns Mac OS X version information.

### Syntax
```python
platform.mac_ver(release='', versioninfo=('', '', ''), machine='')
```

### Parameters
- `release` (str): Override release detection
- `versioninfo` (tuple): Override version info detection
- `machine` (str): Override machine detection

### Example
```python
import platform

release, versioninfo, machine = platform.mac_ver()
print(f"macOS: {release}")
print(f"Version info: {versioninfo}")
print(f"Machine: {machine}")

# Output:
# macOS: 11.6
# Version info: ('', ('', '', ''), '')
# Machine: x86_64
```

### Edge Cases
- Only works on macOS systems
- Returns default values on other platforms
- Version info tuple may be empty

## platform.win32_ver()

### Purpose
Returns Windows version information.

### Syntax
```python
platform.win32_ver(release='', version='', csd='', ptype='')
```

### Parameters
- `release` (str): Override release detection
- `version` (str): Override version detection
- `csd` (str): Override CSD (service pack) detection
- `ptype` (str): Override product type detection

### Example
```python
import platform

release, version, csd, ptype = platform.win32_ver()
print(f"Windows release: {release}")
print(f"Version: {version}")
print(f"Service Pack: {csd}")
print(f"Product Type: {ptype}")

# Output:
# Windows release: 10
# Version: 10.0.19043
# Service Pack: 
# Product Type: Multiprocessor Free
```

### Edge Cases
- Only works on Windows systems
- CSD (service pack) is often empty on modern Windows
- Product type indicates workstation vs server

## platform.win32_edition()

### Purpose
Returns the Windows edition (available on Windows only).

### Syntax
```python
platform.win32_edition()
```

### Example
```python
import platform

edition = platform.win32_edition()
print(f"Windows edition: {edition}")
# Output: Windows edition: Professional
#         Windows edition: Home
#         Windows edition: Enterprise
```

### Edge Cases
- Only available on Windows
- Returns None on other platforms
- May require administrative privileges for some editions

## platform.win32_is_iot()

### Purpose
Returns True if running on Windows IoT (available on Windows only).

### Syntax
```python
platform.win32_is_iot()
```

### Example
```python
import platform

is_iot = platform.win32_is_iot()
print(f"Windows IoT: {is_iot}")
# Output: Windows IoT: False
```

### Edge Cases
- Only available on Windows
- Returns False on non-IoT Windows versions

## platform.freedesktop_os_release()

### Purpose
Returns OS release information using freedesktop.org standards (Linux/Unix).

### Syntax
```python
platform.freedesktop_os_release()
```

### Example
```python
import platform

try:
    release_info = platform.freedesktop_os_release()
    print("OS Release Info:")
    for key, value in release_info.items():
        print(f"  {key}: {value}")
    # Output:
    # OS Release Info:
    #   NAME: Ubuntu
    #   VERSION: 20.04.3 LTS (Focal Fossa)
    #   ID: ubuntu
    #   VERSION_ID: 20.04
except Exception as e:
    print(f"Could not get OS release info: {e}")
```

### Edge Cases
- Only works on systems with /etc/os-release or similar files
- Raises exception if file not found or unreadable
- More reliable than linux_distribution() on modern Linux

## Common Usage Patterns

### Cross-Platform Distribution Detection
```python
import platform

def get_distribution_info():
    """Get distribution information across platforms."""
    system = platform.system()

    if system == 'Linux':
        try:
            # Try modern method first
            info = platform.freedesktop_os_release()
            return {
                'name': info.get('NAME', 'Unknown'),
                'version': info.get('VERSION', 'Unknown'),
                'id': info.get('ID', 'Unknown')
            }
        except:
            # Fallback to deprecated method
            name, version, codename = platform.linux_distribution()
            return {
                'name': name or 'Unknown',
                'version': version or 'Unknown',
                'codename': codename or 'Unknown'
            }
    elif system == 'Darwin':
        release, _, _ = platform.mac_ver()
        return {
            'name': 'macOS',
            'version': release,
            'id': 'macos'
        }
    elif system == 'Windows':
        release, version, csd, ptype = platform.win32_ver()
        edition = platform.win32_edition()
        return {
            'name': 'Windows',
            'version': version,
            'release': release,
            'service_pack': csd,
            'product_type': ptype,
            'edition': edition
        }
    else:
        return {
            'name': system,
            'version': 'Unknown',
            'id': 'unknown'
        }

dist_info = get_distribution_info()
print(f"Distribution: {dist_info}")
```

### Linux Distribution-Specific Code
```python
import platform

def handle_linux_specific_tasks():
    """Perform tasks based on Linux distribution."""
    try:
        info = platform.freedesktop_os_release()
        dist_id = info.get('ID', '').lower()

        if dist_id == 'ubuntu':
            print("Running Ubuntu-specific commands")
            # apt update, etc.
        elif dist_id == 'centos':
            print("Running CentOS-specific commands")
            # yum update, etc.
        elif dist_id == 'fedora':
            print("Running Fedora-specific commands")
            # dnf update, etc.
        else:
            print(f"Running generic Linux commands for {dist_id}")

    except Exception as e:
        print(f"Could not determine Linux distribution: {e}")
        # Fallback to generic Linux handling

handle_linux_specific_tasks()
```

### Windows Version-Specific Features
```python
import platform

def check_windows_features():
    """Check Windows-specific features availability."""
    if platform.system() != 'Windows':
        return {}

    release, version, csd, ptype = platform.win32_ver()
    edition = platform.win32_edition()

    features = {
        'version': version,
        'edition': edition,
        'is_server': 'server' in ptype.lower(),
        'is_iot': platform.win32_is_iot()
    }

    # Check for Windows 10/11 specific features
    try:
        major_version = int(version.split('.')[0])
        if major_version >= 10:
            features['has_modern_features'] = True
        else:
            features['has_modern_features'] = False
    except (ValueError, IndexError):
        features['has_modern_features'] = False

    return features

win_features = check_windows_features()
print(f"Windows features: {win_features}")
```

### macOS Version Checking
```python
import platform

def check_macos_version():
    """Check macOS version and available features."""
    if platform.system() != 'Darwin':
        return None

    release, versioninfo, machine = platform.mac_ver()

    try:
        major_version = int(release.split('.')[0])
        features = {
            'version': release,
            'major_version': major_version,
            'machine': machine
        }

        # macOS version-specific features
        if major_version >= 12:
            features['has_universal_control'] = True
        if major_version >= 11:
            features['has_m1_support'] = True
        if major_version >= 10:
            features['has_metal'] = True

        return features
    except (ValueError, IndexError):
        return {'version': release, 'error': 'Could not parse version'}

mac_features = check_macos_version()
if mac_features:
    print(f"macOS features: {mac_features}")
```

## Best Practices

### Modern Linux Distribution Detection
```python
import platform

def safe_linux_detection():
    """Safely detect Linux distribution using modern methods."""
    if platform.system() != 'Linux':
        return None

    try:
        # Use freedesktop.org standard
        info = platform.freedesktop_os_release()
        return {
            'method': 'freedesktop',
            'name': info.get('NAME', 'Unknown'),
            'version': info.get('VERSION', 'Unknown'),
            'id': info.get('ID', 'Unknown'),
            'version_id': info.get('VERSION_ID', 'Unknown')
        }
    except Exception:
        # Fallback to deprecated method
        try:
            name, version, codename = platform.linux_distribution()
            return {
                'method': 'deprecated',
                'name': name,
                'version': version,
                'codename': codename
            }
        except Exception:
            return {
                'method': 'failed',
                'name': 'Unknown Linux',
                'version': 'Unknown'
            }

linux_info = safe_linux_detection()
print(f"Linux detection: {linux_info}")
```

### Platform-Aware Feature Detection
```python
import platform

def get_platform_features():
    """Get platform-specific features and capabilities."""
    system = platform.system()
    features = {}

    if system == 'Linux':
        try:
            info = platform.freedesktop_os_release()
            features['package_manager'] = get_package_manager(info.get('ID'))
            features['init_system'] = detect_init_system()
        except:
            features['package_manager'] = 'unknown'
            features['init_system'] = 'unknown'

    elif system == 'Darwin':
        release, _, _ = platform.mac_ver()
        features['macos_version'] = release
        features['has_homebrew'] = check_homebrew()

    elif system == 'Windows':
        edition = platform.win32_edition()
        features['windows_edition'] = edition
        features['is_iot'] = platform.win32_is_iot()

    return features

def get_package_manager(dist_id):
    """Determine package manager based on distribution."""
    managers = {
        'ubuntu': 'apt',
        'debian': 'apt',
        'centos': 'yum',
        'fedora': 'dnf',
        'opensuse': 'zypper',
        'arch': 'pacman'
    }
    return managers.get(dist_id, 'unknown')

def detect_init_system():
    """Detect Linux init system (simplified)."""
    # This would need actual system checks
    return 'systemd'  # Most modern Linux uses systemd

def check_homebrew():
    """Check if Homebrew is installed (simplified)."""
    # This would need actual system checks
    return True  # Assume for macOS

platform_features = get_platform_features()
print(f"Platform features: {platform_features}")
```

These functions enable developers to write distribution-aware code that can adapt to different Linux distributions, Windows editions, and macOS versions.
