# Runtime Environment Functions

## Purpose
`sys` provides functions to inspect and control various aspects of Python's runtime environment, including module loading, path management, recursion limits, and memory usage tracking.

## Key Functions and Attributes

### Module System

#### `sys.modules`
- **Purpose**: Dictionary of loaded modules
- **Type**: Dictionary
- **Keys**: Module names (strings)
- **Values**: Module objects

#### `sys.path`
- **Purpose**: List of directories to search for modules
- **Type**: List of strings
- **Modification**: Can be modified to add custom search paths

#### `sys.path_hooks`
- **Purpose**: List of path hook callables for custom import behavior
- **Type**: List of callables

#### `sys.meta_path`
- **Purpose**: List of meta path finder objects
- **Type**: List of finder objects

### Execution Control

#### `sys.getrecursionlimit()`
- **Purpose**: Get the current recursion limit
- **Returns**: Integer (default: 1000)

#### `sys.setrecursionlimit(limit)`
- **Purpose**: Set the maximum recursion depth
- **Parameters**: `limit` (integer)

#### `sys.exit([code])`
- **Purpose**: Exit the program with optional status code
- **Parameters**: `code` (integer, optional, default: 0)

### Memory and Size Information

#### `sys.getsizeof(object[, default])`
- **Purpose**: Get the size of an object in bytes
- **Parameters**: `object` (any), `default` (optional)
- **Returns**: Size in bytes

#### `sys.getrefcount(object)`
- **Purpose**: Get the reference count of an object
- **Parameters**: `object` (any)
- **Returns**: Integer reference count

## Syntax and Examples

### Module System Management
```python
import sys

def explore_modules():
    # Show loaded modules count
    print(f"Loaded modules: {len(sys.modules)}")

    # Check if a module is loaded
    if 'os' in sys.modules:
        print("os module is loaded")
    else:
        print("os module not loaded")

    # Show first 5 loaded modules
    for i, (name, module) in enumerate(sys.modules.items()):
        if i >= 5:
            break
        print(f"{name}: {module}")

explore_modules()
```

### Path Management
```python
import sys
import os

def manage_paths():
    print("Current Python path:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")

    # Add a custom path
    custom_path = "/my/custom/modules"
    if custom_path not in sys.path:
        sys.path.insert(0, custom_path)
        print(f"Added custom path: {custom_path}")

    # Show updated path
    print(f"Total paths: {len(sys.path)}")

manage_paths()
```

### Recursion Control
```python
import sys

def recursion_demo():
    print(f"Current recursion limit: {sys.getrecursionlimit()}")

    # Increase recursion limit for deep recursion
    sys.setrecursionlimit(2000)
    print(f"New recursion limit: {sys.getrecursionlimit()}")

    # Recursive function
    def factorial(n, acc=1):
        if n <= 1:
            return acc
        return factorial(n - 1, n * acc)

    try:
        result = factorial(1000)
        print(f"Factorial 1000 calculated successfully")
    except RecursionError as e:
        print(f"Recursion error: {e}")

recursion_demo()
```

### Memory Analysis
```python
import sys

def analyze_memory():
    # Simple objects
    num = 42
    text = "Hello, World!"
    my_list = [1, 2, 3, 4, 5]

    print("Object sizes:")
    print(f"Integer: {sys.getsizeof(num)} bytes")
    print(f"String: {sys.getsizeof(text)} bytes")
    print(f"List: {sys.getsizeof(my_list)} bytes")

    # List overhead vs content
    empty_list = []
    print(f"Empty list: {sys.getsizeof(empty_list)} bytes")
    print(f"List with 5 elements: {sys.getsizeof(my_list)} bytes")

    # Reference counts
    print(f"Reference count of 42: {sys.getrefcount(42)}")
    print(f"Reference count of text: {sys.getrefcount(text)}")

analyze_memory()
```

## Advanced Usage

### Custom Module Loading
```python
import sys
import importlib.util

def custom_import():
    # Add a custom path
    sys.path.insert(0, '/tmp/my_modules')

    # Create a module dynamically
    spec = importlib.util.spec_from_file_location("mymodule", "/tmp/my_modules/mymodule.py")
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules["mymodule"] = module  # Register in sys.modules
        spec.loader.exec_module(module)
        print("Custom module loaded")

custom_import()
```

### Path Hook Implementation
```python
import sys
import importlib.abc
import importlib.util

class CustomFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "magic_module":
            # Create a spec for our magic module
            spec = importlib.util.spec_from_loader(fullname, CustomLoader())
            return spec
        return None

class CustomLoader(importlib.abc.Loader):
    def create_module(self, spec):
        return None  # Use default module creation

    def exec_module(self, module):
        module.value = 42
        module.get_value = lambda: module.value

# Register custom finder
sys.meta_path.insert(0, CustomFinder())

# Now we can import magic_module
import magic_module
print(f"Magic value: {magic_module.get_value()}")
```

### Memory Profiling
```python
import sys
import tracemalloc

def memory_profile():
    # Start tracing
    tracemalloc.start()

    # Create some objects
    data = []
    for i in range(1000):
        data.append([i] * 100)  # Lists of lists

    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory: {current / 1024:.1f} KB")
    print(f"Peak memory: {peak / 1024:.1f} KB")

    # Analyze object sizes
    total_size = sum(sys.getsizeof(item) for item in data)
    print(f"Data size: {total_size / 1024:.1f} KB")

    tracemalloc.stop()

memory_profile()
```

### Controlled Exit
```python
import sys
import atexit

def cleanup():
    print("Performing cleanup...")

atexit.register(cleanup)

def controlled_exit():
    try:
        # Some operation that might fail
        risky_operation()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit with error code

    print("Operation completed successfully")
    sys.exit(0)  # Exit with success code

controlled_exit()
```

## Edge Cases and Considerations

### Path Modification Risks
```python
import sys

def path_modification_risks():
    # Dangerous: Adding relative paths
    sys.path.append('.')  # Could lead to module confusion

    # Dangerous: Adding untrusted paths
    sys.path.insert(0, '/untrusted/path')  # Security risk

    # Better: Use absolute paths
    import os
    safe_path = os.path.abspath('/trusted/modules')
    sys.path.insert(0, safe_path)

    print("Paths modified safely")

path_modification_risks()
```

### Recursion Limit Considerations
```python
import sys

def recursion_limit_considerations():
    original_limit = sys.getrecursionlimit()

    # Temporary increase for specific operation
    sys.setrecursionlimit(5000)

    try:
        # Perform deep recursion operation
        deep_operation()
    finally:
        # Always restore original limit
        sys.setrecursionlimit(original_limit)

    print("Recursion limit restored")

recursion_limit_considerations()
```

### Module Registry Management
```python
import sys

def module_registry():
    # Check if module exists
    if 'json' in sys.modules:
        json_module = sys.modules['json']
        print(f"JSON module: {json_module}")
    else:
        import json
        print("JSON module loaded on demand")

    # Remove module from registry (dangerous!)
    # This can cause issues if module is still referenced
    # sys.modules.pop('json', None)

    print(f"Modules in registry: {len(sys.modules)}")

module_registry()
```

## Common Patterns

### Environment Setup
```python
import sys
import os

def setup_environment():
    """Set up the Python environment for the application"""

    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Set recursion limit based on use case
    if os.environ.get('DEEP_RECURSION') == '1':
        sys.setrecursionlimit(10000)
    else:
        sys.setrecursionlimit(2000)

    # Configure exit behavior
    def custom_exit(code=0):
        print(f"Exiting with code: {code}")
        sys.exit(code)

    # Replace sys.exit with custom version
    sys.exit = custom_exit

setup_environment()
```

### Memory Monitoring
```python
import sys
import psutil
import os

def monitor_memory():
    """Monitor memory usage of the Python process"""

    def get_memory_usage():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # MB

    initial_memory = get_memory_usage()
    print(f"Initial memory: {initial_memory:.1f} MB")

    # Create some data structures
    big_list = [i for i in range(100000)]
    big_dict = {i: i**2 for i in range(10000)}

    final_memory = get_memory_usage()
    print(f"Final memory: {final_memory:.1f} MB")
    print(f"Memory increase: {final_memory - initial_memory:.1f} MB")

    # Analyze object sizes
    print(f"List size: {sys.getsizeof(big_list)} bytes")
    print(f"Dict size: {sys.getsizeof(big_dict)} bytes")

monitor_memory()
```

### Import Path Management
```python
import sys
import os
from contextlib import contextmanager

@contextmanager
def temporary_path(*paths):
    """Temporarily add paths to sys.path"""
    original_path = sys.path[:]
    for path in paths:
        if path not in sys.path:
            sys.path.insert(0, path)

    try:
        yield
    finally:
        sys.path[:] = original_path

def import_with_temp_path():
    with temporary_path('/tmp/modules', '/opt/custom'):
        # Imports here will use the temporary paths
        try:
            import custom_module
            print("Custom module imported successfully")
        except ImportError:
            print("Custom module not found")

import_with_temp_path()
```

## Best Practices

1. **Be careful modifying `sys.path`** - Use absolute paths and avoid untrusted locations
2. **Restore recursion limits** after temporary changes
3. **Use `sys.exit()` with appropriate codes** - 0 for success, non-zero for errors
4. **Monitor memory usage** in long-running applications
5. **Avoid manipulating `sys.modules`** directly unless necessary
6. **Use context managers** for temporary environment changes

## Performance Considerations

- **Path lookups are cached** - `sys.path` changes affect future imports
- **Module registry access is fast** - `sys.modules` is a dictionary lookup
- **Recursion limit checks** occur on function calls, affecting performance
- **Memory size calculations** have some overhead for complex objects

## Comparison with Other Modules

| Feature | `sys` | `os` | `importlib` |
|---------|-------|------|-------------|
| Path management | `sys.path` | `os.path` | `importlib.util` |
| Module loading | `sys.modules` | N/A | Full control |
| Process control | `sys.exit` | `os._exit` | N/A |
| Memory info | `sys.getsizeof` | N/A | N/A |

`sys` provides the core runtime environment control, while other modules offer specialized functionality.
