# Hardware Architecture Functions

This section covers the `platform` library functions that provide information about the underlying hardware architecture and processor details.

## platform.machine()

### Purpose
Returns the machine hardware name (architecture identifier).

### Syntax
```python
platform.machine()
```

### Example
```python
import platform

machine = platform.machine()
print(f"Machine architecture: {machine}")
# Output: Machine architecture: x86_64
#         Machine architecture: AMD64
#         Machine architecture: arm64
#         Machine architecture: aarch64
```

### Edge Cases
- Returns empty string if hardware cannot be determined
- Naming conventions vary between platforms (x86_64 vs AMD64)
- In virtualized environments, may reflect virtual hardware

## platform.processor()

### Purpose
Returns the processor name or description.

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
#         Processor: AMD Ryzen 7 3700X 8-Core Processor
```

### Edge Cases
- May return empty string on some Unix systems
- Very detailed on Windows, often empty or minimal on Linux/macOS
- Does not necessarily reflect the actual CPU model in all cases

## platform.architecture()

### Purpose
Returns a tuple containing the bit architecture and linkage format of the Python interpreter.

### Syntax
```python
platform.architecture(executable=None, bits=None, linkage=None)
```

### Parameters
- `executable` (str): Path to executable to check (default: sys.executable)
- `bits` (str): Override automatic bit detection
- `linkage` (str): Override automatic linkage detection

### Example
```python
import platform

bits, linkage = platform.architecture()
print(f"Architecture: {bits}")
print(f"Linkage: {linkage}")

# Output:
# Architecture: 64bit
# Linkage: WindowsPE

# Check a specific executable
bits, linkage = platform.architecture('/usr/bin/python3')
print(f"Python3: {bits}, {linkage}")
```

### Edge Cases
- Returns ('', '') if architecture cannot be determined
- Linkage types: WindowsPE, ELF, Mach-O, etc.
- Can analyze any executable, not just Python

## platform.uname() - Hardware Fields

### Purpose
The `uname()` function includes hardware-related fields.

### Hardware-Specific Fields
```python
import platform

info = platform.uname()
print(f"Machine: {info.machine}")      # Hardware platform
print(f"Processor: {info.processor}")  # Processor name
```

### Example
```python
import platform

info = platform.uname()
print("Hardware Information:")
print(f"  Machine: {info.machine}")
print(f"  Processor: {info.processor}")

# Output:
# Hardware Information:
#   Machine: x86_64
#   Processor: Intel64 Family 6 Model 158 Stepping 10, GenuineIntel
```

### Edge Cases
- Processor field may be empty on some systems
- Machine field is more reliable than processor

## Advanced Hardware Detection

### Combining Functions for Complete Hardware Profile
```python
import platform

def get_hardware_info():
    """Get comprehensive hardware information."""
    return {
        'machine': platform.machine(),
        'processor': platform.processor(),
        'architecture': platform.architecture(),
        'uname_machine': platform.uname().machine,
        'uname_processor': platform.uname().processor
    }

hardware = get_hardware_info()
for key, value in hardware.items():
    print(f"{key}: {value}")
```

### Architecture-Based Decision Making
```python
import platform

def get_optimized_library_path():
    """Return platform-specific library path."""
    machine = platform.machine().lower()

    if 'x86_64' in machine or 'amd64' in machine:
        return '/lib/x86_64-linux-gnu/'
    elif 'arm64' in machine or 'aarch64' in machine:
        return '/lib/aarch64-linux-gnu/'
    elif 'arm' in machine:
        return '/lib/arm-linux-gnueabihf/'
    else:
        return '/lib/'

path = get_optimized_library_path()
print(f"Library path: {path}")
```

### Virtualization Detection
```python
import platform

def detect_virtualization():
    """Attempt to detect if running in a virtualized environment."""
    processor = platform.processor().lower()
    machine = platform.machine()

    # Simple heuristics (not foolproof)
    virtual_indicators = ['virtual', 'vmware', 'xen', 'kvm', 'qemu']

    is_virtual = any(indicator in processor for indicator in virtual_indicators)

    return {
        'likely_virtual': is_virtual,
        'processor_info': processor,
        'machine': machine
    }

virt_info = detect_virtualization()
print(f"Likely virtualized: {virt_info['likely_virtual']}")
```

## Common Hardware Architecture Patterns

### 64-bit vs 32-bit Detection
```python
import platform

def is_64bit():
    """Check if running on 64-bit architecture."""
    bits, _ = platform.architecture()
    return '64' in bits

def get_bit_architecture():
    """Get detailed bit architecture info."""
    bits, linkage = platform.architecture()
    machine = platform.machine()

    return {
        'bits': bits,
        'linkage': linkage,
        'machine': machine,
        'is_64bit': '64' in bits
    }

arch_info = get_bit_architecture()
print(f"Running on {arch_info['bits']} architecture")
```

### CPU Architecture Families
```python
import platform

def get_cpu_family():
    """Determine CPU architecture family."""
    machine = platform.machine().lower()

    if machine in ['x86_64', 'amd64', 'i386', 'i686']:
        return 'x86'
    elif machine in ['arm64', 'aarch64']:
        return 'ARM64'
    elif machine.startswith('arm'):
        return 'ARM'
    elif machine.startswith('ppc'):
        return 'PowerPC'
    else:
        return 'Unknown'

cpu_family = get_cpu_family()
print(f"CPU Family: {cpu_family}")
```

### Hardware-Specific Optimizations
```python
import platform

def get_hardware_optimized_settings():
    """Return hardware-specific configuration settings."""
    machine = platform.machine().lower()

    if 'x86_64' in machine or 'amd64' in machine:
        return {
            'vectorization': 'AVX2',
            'threads': 8,
            'memory_alignment': 64
        }
    elif 'arm64' in machine or 'aarch64' in machine:
        return {
            'vectorization': 'NEON',
            'threads': 4,
            'memory_alignment': 16
        }
    else:
        return {
            'vectorization': 'none',
            'threads': 2,
            'memory_alignment': 8
        }

settings = get_hardware_optimized_settings()
print("Hardware-optimized settings:")
for key, value in settings.items():
    print(f"  {key}: {value}")
```

## Best Practices for Hardware Detection

### Don't Rely Solely on Hardware Info
```python
import platform

def safe_hardware_check():
    """Safely check hardware with fallbacks."""
    try:
        machine = platform.machine()
        if not machine:
            machine = "unknown"
    except Exception:
        machine = "unknown"

    return machine

safe_machine = safe_hardware_check()
print(f"Safe machine detection: {safe_machine}")
```

### Combine Multiple Sources
```python
import platform
import sys

def comprehensive_architecture_info():
    """Get architecture info from multiple sources."""
    return {
        'platform_machine': platform.machine(),
        'platform_architecture': platform.architecture(),
        'sys_maxsize': sys.maxsize,  # Indirect bit detection
        'sys_platform': sys.platform
    }

info = comprehensive_architecture_info()
print("Comprehensive architecture info:")
for key, value in info.items():
    print(f"  {key}: {value}")
```

These functions enable developers to write hardware-aware applications that can adapt to different processor architectures and system capabilities.
