# Do's and Don'ts for Using the `sys` Module

This guide outlines best practices for using the `sys` module effectively and safely in Python applications.

## Do's

### ✅ Do Use `sys.exit()` for Clean Program Termination

**Why:** Provides a standardized way to exit with status codes that other programs can interpret.

**Good Example:**
```python
import sys

def main():
    try:
        # Your application logic
        process_data()
        return 0  # Success
    except FileNotFoundError:
        sys.stderr.write("Error: Input file not found\n")
        return 1  # Error
    except Exception as e:
        sys.stderr.write(f"Unexpected error: {e}\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())
```

### ✅ Do Check Python Version Compatibility

**Why:** Ensures your code runs on supported Python versions and handles version-specific features gracefully.

**Good Example:**
```python
import sys

# Check minimum version
if sys.version_info < (3, 6):
    sys.stderr.write("Python 3.6+ required\n")
    sys.exit(1)

# Use version-specific features safely
if sys.version_info >= (3, 8):
    # Use walrus operator :=
    if (n := len(sys.argv)) > 1:
        process_args(sys.argv[1:])
else:
    # Fallback for older versions
    n = len(sys.argv)
    if n > 1:
        process_args(sys.argv[1:])
```

### ✅ Do Use `sys.argv` for Command-Line Arguments

**Why:** Direct access to command-line arguments without external dependencies.

**Good Example:**
```python
import sys

def main():
    if len(sys.argv) < 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <input_file>\n")
        return 1

    input_file = sys.argv[1]
    # Process file...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### ✅ Do Handle Standard Streams Properly

**Why:** Ensures proper input/output redirection and error handling.

**Good Example:**
```python
import sys

# Read from stdin
for line in sys.stdin:
    # Process line
    processed = line.upper()
    sys.stdout.write(processed)

# Write errors to stderr
try:
    risky_operation()
except Exception as e:
    sys.stderr.write(f"Error: {e}\n")
    sys.exit(1)
```

### ✅ Do Use `sys.path` for Module Path Management

**Why:** Allows dynamic modification of Python's module search path.

**Good Example:**
```python
import sys
from pathlib import Path

# Add custom directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now you can import from the custom location
import my_custom_module
```

### ✅ Do Check Platform-Specific Behavior

**Why:** Ensures cross-platform compatibility.

**Good Example:**
```python
import sys
import os

if sys.platform == 'win32':
    # Windows-specific code
    path_sep = '\\'
    null_device = 'nul'
else:
    # Unix-like systems
    path_sep = '/'
    null_device = '/dev/null'
```

### ✅ Do Use `sys.getsizeof()` for Memory Analysis

**Why:** Helps understand memory usage of objects.

**Good Example:**
```python
import sys

def analyze_memory_usage(obj):
    """Analyze memory usage of an object and its contents"""
    size = sys.getsizeof(obj)
    print(f"Object size: {size} bytes")

    if hasattr(obj, '__dict__'):
        dict_size = sys.getsizeof(obj.__dict__)
        print(f"Instance dict size: {dict_size} bytes")

    return size
```

## Don'ts

### ❌ Don't Modify `sys.path` Unnecessarily

**Why:** Can break imports and create unpredictable behavior.

**Bad Example:**
```python
import sys

# DON'T DO THIS - modifies path globally
sys.path.append('/some/random/directory')

# This can interfere with other imports
import some_module  # Might import from the wrong location
```

**Better Approach:**
```python
import sys
from pathlib import Path

# DO THIS - use context managers or local scope
def import_from_custom_path():
    custom_path = Path('/custom/modules')
    sys.path.insert(0, str(custom_path))
    try:
        import custom_module
        return custom_module
    finally:
        sys.path.remove(str(custom_path))
```

### ❌ Don't Use `sys.exit()` in Libraries

**Why:** Libraries should raise exceptions instead of terminating the program.

**Bad Example:**
```python
# In a library module - DON'T DO THIS
def validate_config(config):
    if not config.get('required_param'):
        sys.stderr.write("Configuration error\n")
        sys.exit(1)  # Terminates the calling program!
```

**Good Example:**
```python
# In a library module - DO THIS
class ConfigurationError(Exception):
    pass

def validate_config(config):
    if not config.get('required_param'):
        raise ConfigurationError("Missing required parameter")
```

### ❌ Don't Hardcode `sys.argv` Indices

**Why:** Makes code brittle and error-prone.

**Bad Example:**
```python
import sys

# DON'T DO THIS - assumes specific argument positions
input_file = sys.argv[1]  # What if no arguments?
output_file = sys.argv[2]  # What if only one argument?
```

**Good Example:**
```python
import sys

def parse_args():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: script.py <input> <output>\n")
        sys.exit(1)

    return {
        'input_file': sys.argv[1],
        'output_file': sys.argv[2]
    }

args = parse_args()
```

### ❌ Don't Ignore Encoding Issues

**Why:** Can cause data corruption and platform-specific problems.

**Bad Example:**
```python
import sys

# DON'T DO THIS - assumes default encoding
content = sys.stdin.read()  # May fail with Unicode
```

**Good Example:**
```python
import sys
import locale

# DO THIS - handle encoding explicitly
encoding = locale.getpreferredencoding(False)
try:
    content = sys.stdin.read()
except UnicodeDecodeError:
    sys.stderr.write("Error: Invalid input encoding\n")
    sys.exit(1)
```

### ❌ Don't Modify `sys.stdout`/`sys.stderr` Without Restoration

**Why:** Can break logging and error reporting for other parts of the program.

**Bad Example:**
```python
import sys

# DON'T DO THIS - permanent redirection
sys.stdout = open('log.txt', 'w')

# Now all print statements go to log.txt forever
print("This goes to log.txt")
# Even error messages from other modules!
```

**Good Example:**
```python
import sys
from contextlib import redirect_stdout, redirect_stderr

# DO THIS - temporary redirection with context manager
with open('log.txt', 'w') as log_file:
    with redirect_stdout(log_file):
        print("This goes to log.txt")

# stdout is restored automatically
print("This goes to console again")
```

### ❌ Don't Use `sys.getrefcount()` for Production Logic

**Why:** It's a debugging tool that can give misleading results and may not be available in all Python implementations.

**Bad Example:**
```python
import sys

# DON'T DO THIS - using refcount for logic
def process_item(item):
    if sys.getrefcount(item) > 2:  # Unreliable!
        # Some logic based on reference count
        pass
```

**Good Example:**
```python
# DO THIS - use proper object ownership tracking
class ResourceManager:
    def __init__(self):
        self._active_resources = set()

    def acquire(self, resource):
        if resource in self._active_resources:
            raise ValueError("Resource already in use")
        self._active_resources.add(resource)
        return resource

    def release(self, resource):
        self._active_resources.discard(resource)
```

### ❌ Don't Assume `sys.maxsize` is the Same Across Platforms

**Why:** The maximum integer value varies between 32-bit and 64-bit systems.

**Bad Example:**
```python
import sys

# DON'T DO THIS - assumes 64-bit
if some_value > 2**63 - 1:
    # Handle large numbers
    pass
```

**Good Example:**
```python
import sys

# DO THIS - use sys.maxsize
if some_value > sys.maxsize:
    # Handle large numbers
    pass
```

### ❌ Don't Modify `sys.modules` Directly

**Why:** Can break the import system and create circular dependencies.

**Bad Example:**
```python
import sys

# DON'T DO THIS - direct module manipulation
sys.modules['my_module'] = some_object

# This can confuse the import system
import my_module  # Might not work as expected
```

**Good Example:**
```python
# DO THIS - let Python handle module management
# Create proper .py files and use import statements
import my_module
```

## Summary

**Key Principles:**
- Use `sys` for its intended purposes (runtime inspection, I/O, exit handling)
- Always restore modified global state
- Handle errors gracefully instead of terminating abruptly
- Check compatibility and platform differences
- Prefer raising exceptions over calling `sys.exit()` in libraries
- Use context managers for temporary stream redirection

**Remember:** The `sys` module gives you powerful access to Python's internals. Use this power responsibly to create robust, maintainable, and cross-platform compatible applications.
