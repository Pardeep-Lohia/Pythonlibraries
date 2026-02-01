# System Information Functions

This section covers the `platform` library functions that provide system-level information about the operating system and platform.

## platform.system()

### Purpose
Returns the system/OS name as a string.

### Syntax
```python
platform.system()
```

### Example
```python
import platform

system = platform.system()
print(f"Operating System: {system}")
# Output: Operating System: Windows
#         Operating System: Linux
#         Operating System: Darwin
```

### Edge Cases
- Returns an empty string if the system cannot be determined
- On some platforms, may return generic names like 'Linux' for various Unix-like systems

## platform.node()

### Purpose
Returns the computer's network name (hostname).

### Syntax
```python
platform.node()
```

### Example
```python
import platform

hostname = platform.node()
print(f"Hostname: {hostname}")
# Output: Hostname: my-computer
```

### Edge Cases
- May return an empty string if hostname cannot be determined
- In some environments (like containers), might return generic names

## platform.release()

### Purpose
Returns the system release version.

### Syntax
```python
platform.release()
```

### Example
```python
import platform

release = platform.release()
print(f"Release: {release}")
# Output: Release: 10 (Windows)
#         Release: 5.4.0-42-generic (Linux)
```

### Edge Cases
- Format varies significantly between operating systems
- May not correspond to marketing version numbers

## platform.version()

### Purpose
Returns the system version information.

### Syntax
```python
platform.version()
```

### Example
```python
import platform

version = platform.version()
print(f"Version: {version}")
# Output: Version: 10.0.19041 (Windows)
#         Version: #42-Ubuntu SMP Fri Oct 2 12:34:56 UTC 2020 (Linux)
```

### Edge Cases
- Very detailed and platform-specific
- Can be quite long and contain technical details
- May include build numbers, timestamps, etc.

## platform.uname()

### Purpose
Returns a named tuple containing comprehensive system information.

### Syntax
```python
platform.uname()
```

### Example
```python
import platform

info = platform.uname()
print(f"System: {info.system}")
print(f"Node: {info.node}")
print(f"Release: {info.release}")
print(f"Version: {info.version}")
print(f"Machine: {info.machine}")
print(f"Processor: {info.processor}")

# Output:
# System: Windows
# Node: my-computer
# Release: 10
# Version: 10.0.19041
# Machine: AMD64
# Processor: Intel64 Family 6 Model 158 Stepping 10, GenuineIntel
```

### Edge Cases
- All fields are strings, some may be empty
- Processor field might be empty on some systems
- Provides the most complete system information in one call

## platform.platform()

### Purpose
Returns a single string summarizing the platform information.

### Syntax
```python
platform.platform(aliased=False, terse=False)
```

### Parameters
- `aliased` (bool): If True, uses aliases for better readability
- `terse` (bool): If True, returns a shorter version

### Example
```python
import platform

# Default (aliased=True, terse=False)
full_info = platform.platform()
print(f"Platform: {full_info}")
# Output: Platform: Windows-10-10.0.19041-SP0

# Terse version
terse_info = platform.platform(terse=True)
print(f"Terse: {terse_info}")
# Output: Terse: Windows-10

# Non-aliased
non_aliased = platform.platform(aliased=False)
print(f"Non-aliased: {non_aliased}")
# Output: Non-aliased: Windows-10.0.19041
```

### Edge Cases
- The exact format varies by platform
- Aliased versions are more human-readable
- Terse versions omit some details

## platform.architecture()

### Purpose
Returns a tuple containing the bit architecture and linkage format.

### Syntax
```python
platform.architecture(executable=None, bits=None, linkage=None)
```

### Parameters
- `executable` (str): Path to executable to check (default: Python interpreter)
- `bits` (str): Override bit detection
- `linkage` (str): Override linkage detection

### Example
```python
import platform

bits, linkage = platform.architecture()
print(f"Architecture: {bits}-bit")
print(f"Linkage: {linkage}")

# Output:
# Architecture: 64-bit
# Linkage: WindowsPE
```

### Edge Cases
- Returns ('', '') if architecture cannot be determined
- Linkage format varies (ELF, WindowsPE, Mach-O, etc.)
- Can check specific executables by passing the path

## platform.machine()

### Purpose
Returns the machine type (hardware platform).

### Syntax
```python
platform.machine()
```

### Example
```python
import platform

machine = platform.machine()
print(f"Machine: {machine}")
# Output: Machine: x86_64
#         Machine: AMD64
#         Machine: arm64
```

### Edge Cases
- Returns empty string if cannot be determined
- Different platforms may use different naming conventions
- May indicate virtualization (e.g., 'x86_64' on ARM via emulation)

## platform.processor()

### Purpose
Returns the processor name.

### Syntax
```python
platform.processor()
```

### Example
```python
import platform

processor = platform.processor()
print(f"Processor: {processor}")
# Output: Processor: Intel64 Family 6 Model 158 Stepping 10, GenuineIntel
```

### Edge Cases
- May return empty string on some systems
- Very detailed on Windows, less detailed on Unix
- Might not reflect actual CPU model in virtualized environments

## Common Usage Patterns

### Basic System Detection
```python
import platform

def get_system_info():
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }

info = get_system_info()
print(info)
```

### Cross-Platform Compatibility Check
```python
import platform

def is_supported_platform():
    system = platform.system()
    machine = platform.machine()

    supported_systems = ['Windows', 'Linux', 'Darwin']
    supported_architectures = ['x86_64', 'AMD64', 'arm64']

    return system in supported_systems and machine in supported_architectures

if is_supported_platform():
    print("Platform is supported")
else:
    print("Platform is not supported")
```

### Logging System Information
```python
import platform
import logging

def log_system_info():
    info = platform.uname()
    logging.info(f"System: {info.system} {info.release}")
    logging.info(f"Machine: {info.machine}")
    logging.info(f"Python: {platform.python_version()}")

log_system_info()
```

These functions provide the foundation for system-aware Python applications and are essential for cross-platform development.
