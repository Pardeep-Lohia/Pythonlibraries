# Python Runtime Information Functions

This section covers the `platform` library functions that provide information about the Python interpreter and runtime environment.

## platform.python_version()

### Purpose
Returns the Python version as a string in 'major.minor.micro' format.

### Syntax
```python
platform.python_version()
```

### Example
```python
import platform

version = platform.python_version()
print(f"Python version: {version}")
# Output: Python version: 3.9.7
```

### Edge Cases
- Always returns a valid version string
- Format is consistent across platforms

## platform.python_version_tuple()

### Purpose
Returns the Python version as a tuple of strings (major, minor, micro).

### Syntax
```python
platform.python_version_tuple()
```

### Example
```python
import platform

major, minor, micro = platform.python_version_tuple()
print(f"Python {major}.{minor}.{micro}")
# Output: Python 3.9.7
```

### Edge Cases
- Useful for version comparisons
- All elements are strings, not integers

## platform.python_implementation()

### Purpose
Returns the Python implementation name.

### Syntax
```python
platform.python_implementation()
```

### Example
```python
import platform

implementation = platform.python_implementation()
print(f"Python implementation: {implementation}")
# Output: Python implementation: CPython
#         Python implementation: PyPy
#         Python implementation: Jython
```

### Edge Cases
- Common values: 'CPython', 'PyPy', 'Jython', 'IronPython'
- Helps identify different Python interpreters

## platform.python_compiler()

### Purpose
Returns the compiler used to build Python.

### Syntax
```python
platform.python_compiler()
```

### Example
```python
import platform

compiler = platform.python_compiler()
print(f"Python compiler: {compiler}")
# Output: Python compiler: MSC v.1928 64 bit (AMD64)
#         Python compiler: GCC 9.3.0
```

### Edge Cases
- Very platform and build-specific
- May be empty or generic on some distributions

## platform.python_build()

### Purpose
Returns a tuple containing the build number and build date.

### Syntax
```python
platform.python_build()
```

### Example
```python
import platform

build_no, build_date = platform.python_build()
print(f"Python build: {build_no} ({build_date})")
# Output: Python build: ('v3.9.7', 'Aug 31 2021 13:45:56')
```

### Edge Cases
- Build date format may vary
- Useful for identifying specific Python builds

## platform.python_branch()

### Purpose
Returns the version control branch from which Python was built.

### Syntax
```python
platform.python_branch()
```

### Example
```python
import platform

branch = platform.python_branch()
print(f"Python branch: {branch}")
# Output: Python branch: tags/v3.9.7
#         Python branch: main
```

### Edge Cases
- May be empty for release builds
- Useful for development or CI environments

## platform.python_revision()

### Purpose
Returns the version control revision from which Python was built.

### Syntax
```python
platform.python_revision()
```

### Example
```python
import platform

revision = platform.python_revision()
print(f"Python revision: {revision}")
# Output: Python revision: 8e6e92c3b7
```

### Edge Cases
- May be empty for release builds
- Contains git commit hash or SVN revision

## platform.python_version_string()

### Purpose
Returns a string containing the Python version, build, and compiler information.

### Syntax
```python
platform.python_version_string()
```

### Example
```python
import platform

version_string = platform.python_version_string()
print(f"Python version string: {version_string}")
# Output: Python version string: 3.9.7 (v3.9.7:6cc6b133, Aug 31 2021, 13:45:56) [MSC v.1928 64 bit (AMD64)]
```

### Edge Cases
- Very detailed and long string
- Combines multiple pieces of information

## Common Usage Patterns

### Version Checking
```python
import platform

def check_python_version(min_version='3.6.0'):
    """Check if Python version meets minimum requirements."""
    current = platform.python_version()
    return current >= min_version

if check_python_version():
    print("Python version is sufficient")
else:
    print("Python version is too old")
```

### Implementation-Specific Code
```python
import platform

def get_implementation_features():
    """Return features based on Python implementation."""
    impl = platform.python_implementation()

    if impl == 'CPython':
        return ['GIL', 'C extensions', 'Standard library']
    elif impl == 'PyPy':
        return ['No GIL', 'JIT compiler', 'Memory efficient']
    elif impl == 'Jython':
        return ['JVM integration', 'Java libraries', 'Threading']
    else:
        return ['Unknown implementation']

features = get_implementation_features()
print(f"Implementation features: {features}")
```

### Build Information Logging
```python
import platform
import logging

def log_python_info():
    """Log comprehensive Python runtime information."""
    logging.info(f"Python version: {platform.python_version()}")
    logging.info(f"Implementation: {platform.python_implementation()}")
    logging.info(f"Compiler: {platform.python_compiler()}")

    build_no, build_date = platform.python_build()
    logging.info(f"Build: {build_no} ({build_date})")

    if platform.python_branch():
        logging.info(f"Branch: {platform.python_branch()}")
    if platform.python_revision():
        logging.info(f"Revision: {platform.python_revision()}")

log_python_info()
```

### Version Comparison
```python
import platform

def compare_versions():
    """Compare Python versions using different methods."""
    version_str = platform.python_version()
    version_tuple = platform.python_version_tuple()

    print(f"String version: {version_str}")
    print(f"Tuple version: {version_tuple}")

    # Compare with required version
    required = (3, 8, 0)
    current_tuple = tuple(map(int, version_tuple))

    if current_tuple >= required:
        print("Version requirement met")
    else:
        print("Version requirement not met")

compare_versions()
```

### Environment Detection
```python
import platform

def detect_environment():
    """Detect if running in different Python environments."""
    impl = platform.python_implementation()
    version = platform.python_version()

    if impl == 'PyPy':
        return 'PyPy runtime'
    elif 'Anaconda' in platform.python_version_string():
        return 'Anaconda distribution'
    elif impl == 'CPython' and version.startswith('3.'):
        return 'Standard CPython 3.x'
    else:
        return 'Other Python environment'

env = detect_environment()
print(f"Detected environment: {env}")
```

## Best Practices

### Version Checking
```python
import platform

def safe_version_check():
    """Safely check Python version with proper comparison."""
    try:
        version = platform.python_version_tuple()
        major, minor, micro = map(int, version[:3])

        # Check for Python 3.8+
        if (major, minor) >= (3, 8):
            return True
        else:
            return False
    except (ValueError, IndexError):
        # Fallback for unexpected version formats
        return False

is_supported = safe_version_check()
print(f"Python version supported: {is_supported}")
```

### Implementation-Aware Code
```python
import platform

def implementation_aware_function():
    """Function that behaves differently based on implementation."""
    impl = platform.python_implementation()

    if impl == 'CPython':
        # Use CPython-specific features
        return "CPython optimized path"
    elif impl == 'PyPy':
        # Use PyPy-specific optimizations
        return "PyPy optimized path"
    else:
        # Generic implementation
        return "Generic implementation"

result = implementation_aware_function()
print(f"Result: {result}")
```

These functions provide essential information about the Python runtime environment, enabling developers to write implementation-aware and version-compatible code.
