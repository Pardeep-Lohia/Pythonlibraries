# Common Mistakes with the `sys` Module

## Command Line Arguments

### Mistake 1: Accessing `sys.argv[1]` without checking length
```python
import sys

# WRONG: IndexError if no arguments provided
filename = sys.argv[1]  # Crashes with "IndexError: list index out of range"

# CORRECT
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Usage: python script.py <filename>")
    sys.exit(1)
```

### Mistake 2: Assuming arguments are the correct type
```python
import sys

# WRONG: TypeError if argument is not a number
count = int(sys.argv[1])  # Crashes if argv[1] is "abc"

# CORRECT
try:
    count = int(sys.argv[1])
except (IndexError, ValueError):
    print("Please provide a valid number")
    sys.exit(1)
```

### Mistake 3: Not handling spaces in arguments
```python
# Command line: python script.py hello world
# WRONG: Forgets to strip whitespace
name = sys.stdin.readline()  # Gets "hello world\n"

# CORRECT
name = sys.stdin.readline().strip()  # Gets "hello world"
```

## Version Checking

### Mistake 4: Using string operations for version comparison
```python
import sys

# WRONG: Brittle string parsing
if sys.version[0] == '3' and int(sys.version[2]) >= 8:
    pass  # May fail with different version formats

# CORRECT
if sys.version_info >= (3, 8):
    pass
```

### Mistake 5: Checking version in the wrong place
```python
import sys

# WRONG: Version check at module level (affects import time)
if sys.version_info < (3, 6):
    raise ImportError("Python 3.6+ required")

# BETTER: Check at application startup
def main():
    if sys.version_info < (3, 6):
        print("Python 3.6+ required", file=sys.stderr)
        sys.exit(1)
```

## Stream Handling

### Mistake 6: Forgetting to flush stdout before reading stdin
```python
import sys

# WRONG: Prompt may not appear
sys.stdout.write("Enter your name: ")
name = sys.stdin.readline()  # User might not see prompt

# CORRECT
sys.stdout.write("Enter your name: ")
sys.stdout.flush()
name = sys.stdin.readline()
```

### Mistake 7: Using print() without considering stderr
```python
# WRONG: Error messages going to stdout
print("Error: file not found")  # Should go to stderr

# CORRECT
print("Error: file not found", file=sys.stderr)
```

### Mistake 8: Not handling encoding issues
```python
import sys

# WRONG: May fail with UnicodeEncodeError
sys.stdout.write("café")  # Fails if terminal doesn't support UTF-8

# CORRECT
try:
    sys.stdout.write("café")
except UnicodeEncodeError:
    # Fallback to ASCII-safe output
    sys.stdout.write("cafe")
```

## Path Management

### Mistake 9: Adding invalid paths to `sys.path`
```python
import sys

# WRONG: No validation
sys.path.append(user_input_path)  # Could be malicious

# CORRECT
import os
safe_path = os.path.abspath(user_input_path)
if os.path.exists(safe_path):
    sys.path.append(safe_path)
```

### Mistake 10: Modifying `sys.path` permanently
```python
import sys

# WRONG: Permanent modification
sys.path.insert(0, '/tmp/my_modules')

# CORRECT: Temporary modification with restoration
original_path = sys.path[:]
sys.path.insert(0, '/tmp/my_modules')
try:
    import my_module
finally:
    sys.path[:] = original_path
```

## Recursion and Limits

### Mistake 11: Setting recursion limit too high
```python
import sys

# WRONG: May cause stack overflow or system instability
sys.setrecursionlimit(1000000)

# CORRECT: Reasonable limits
sys.setrecursionlimit(5000)  # Still high but safer
```

### Mistake 12: Not restoring recursion limit
```python
import sys

# WRONG: Permanent change
original_limit = sys.getrecursionlimit()
sys.setrecursionlimit(2000)
# Forgot to restore...

# CORRECT
original_limit = sys.getrecursionlimit()
sys.setrecursionlimit(2000)
try:
    deep_function()
finally:
    sys.setrecursionlimit(original_limit)
```

## Memory Management

### Mistake 13: Misunderstanding `sys.getsizeof()`
```python
import sys

# WRONG: Thinking it includes all referenced objects
data = [[1, 2, 3]] * 1000
total_size = sys.getsizeof(data)
print(f"Total size: {total_size}")  # Only container size

# CORRECT: Calculate recursively
def get_deep_size(obj):
    size = sys.getsizeof(obj)
    if isinstance(obj, (list, tuple, dict, set)):
        if isinstance(obj, (list, tuple)):
            size += sum(get_deep_size(item) for item in obj)
        elif isinstance(obj, dict):
            size += sum(get_deep_size(k) + get_deep_size(v) for k, v in obj.items())
        elif isinstance(obj, set):
            size += sum(get_deep_size(item) for item in obj)
    return size

total_size = get_deep_size(data)
```

### Mistake 14: Ignoring reference count offset
```python
import sys

# WRONG: Incorrect reference counting
obj = [1, 2, 3]
count = sys.getrefcount(obj)
print(f"References: {count}")  # Actually count + 1

# CORRECT
obj = [1, 2, 3]
count = sys.getrefcount(obj) - 1  # Subtract 1 for getrefcount argument
print(f"References: {count}")
```

## Exit Handling

### Mistake 15: Using `sys.exit()` in libraries
```python
# WRONG: In a library module
def process_data(data):
    if not data:
        sys.exit(1)  # Terminates the calling program

# CORRECT
def process_data(data):
    if not data:
        raise ValueError("No data provided")
```

### Mistake 16: Using wrong exit codes
```python
import sys

# WRONG: Non-standard exit codes
sys.exit(42)  # What does 42 mean?

# CORRECT: Standard exit codes
sys.exit(0)  # Success
sys.exit(1)  # General error
sys.exit(2)  # Command line syntax error
```

## Module Management

### Mistake 17: Direct manipulation of `sys.modules`
```python
import sys

# WRONG: Dangerous module registry manipulation
sys.modules['fake_json'] = fake_object

# CORRECT: Let Python handle module loading
try:
    import json
except ImportError:
    # Handle missing module
    pass
```

### Mistake 18: Checking module existence incorrectly
```python
import sys

# WRONG: Unnecessary check
if 'os' not in sys.modules:
    import os

# CORRECT: Just import (Python handles it)
import os
```

## Exception Handling

### Mistake 19: Using `sys.exc_info()` outside exception handlers
```python
import sys

# WRONG: exc_info only valid during exception handling
def normal_function():
    info = sys.exc_info()  # Returns (None, None, None)
    print(info)

# CORRECT: Only use within except blocks
try:
    risky_operation()
except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    # Handle exception info here
```

### Mistake 20: Not calling original exception hooks
```python
import sys

# WRONG: Replacing without calling original
def my_hook(exc_type, exc_value, exc_traceback):
    print("My custom handling")
    # Forgot to call original hook

sys.excepthook = my_hook

# CORRECT
original_hook = sys.excepthook
def my_hook(exc_type, exc_value, exc_traceback):
    print("My custom handling")
    original_hook(exc_type, exc_value, exc_traceback)

sys.excepthook = my_hook
```

## Thread Safety

### Mistake 21: Calling `sys.exit()` from threads
```python
import sys
import threading

# WRONG: Terminates entire process
def worker():
    if error_condition:
        sys.exit(1)  # Kills main thread too

# CORRECT: Signal to main thread
def worker():
    if error_condition:
        error_flag.set()
        return
```

### Mistake 22: Modifying `sys.path` from multiple threads
```python
import sys
import threading

# WRONG: Race conditions
def add_path_thread(path):
    sys.path.append(path)  # Not thread-safe

# CORRECT: Use locks
path_lock = threading.Lock()

def add_path_thread(path):
    with path_lock:
        if path not in sys.path:
            sys.path.append(path)
```

## Platform-Specific Issues

### Mistake 23: Assuming Unix path separators
```python
import sys

# WRONG: Hardcoded separators
if sys.platform == 'win32':
    path = 'C:\\Program Files\\App'
else:
    path = '/usr/local/bin'

# CORRECT: Use os.path
import os
path = os.path.join('C:' if sys.platform == 'win32' else '', 'Program Files' if sys.platform == 'win32' else 'usr', 'local', 'bin')
```

### Mistake 24: Ignoring platform differences in stream handling
```python
import sys

# WRONG: May not work on Windows
sys.stdout.write("Hello\n")  # \n may not flush on Windows

# CORRECT: Use print() or flush explicitly
print("Hello")
# or
sys.stdout.write("Hello\n")
sys.stdout.flush()
```

## Performance Issues

### Mistake 25: Frequent `sys.getsizeof()` calls
```python
import sys

# WRONG: Performance overhead
for item in large_list:
    size = sys.getsizeof(item)  # Called for each item
    process_item(item, size)

# CORRECT: Batch processing
sizes = [sys.getsizeof(item) for item in large_list]
for item, size in zip(large_list, sizes):
    process_item(item, size)
```

### Mistake 26: Unnecessary version checks in loops
```python
import sys

# WRONG: Version check in loop
for item in data:
    if sys.version_info >= (3, 8):  # Checked every iteration
        process_new_way(item)
    else:
        process_old_way(item)

# CORRECT: Check version once
use_new_way = sys.version_info >= (3, 8)
for item in data:
    if use_new_way:
        process_new_way(item)
    else:
        process_old_way(item)
```

## Security Issues

### Mistake 27: Path injection via `sys.path`
```python
import sys

# WRONG: Direct user input to sys.path
user_path = input("Enter module path: ")
sys.path.append(user_path)  # Path traversal possible

# CORRECT: Validate and sanitize
import os
user_path = input("Enter module path: ")
safe_path = os.path.abspath(user_path)
if os.path.exists(safe_path) and safe_path.startswith('/safe/base/path'):
    sys.path.append(safe_path)
```

### Mistake 28: Information disclosure via `sys` attributes
```python
import sys

# WRONG: Exposing sensitive information
print(f"Python path: {sys.executable}")  # May reveal installation details

# CORRECT: Be mindful of what you expose
# Only show necessary information
if debug_mode:
    print(f"Python path: {sys.executable}")
```

## Summary

The most common mistakes with `sys` involve:

1. **Argument handling**: Not checking `len(sys.argv)` before access
2. **Version checking**: Using string operations instead of `sys.version_info`
3. **Stream management**: Forgetting to flush stdout or using wrong streams
4. **Path manipulation**: Adding unvalidated paths or not restoring changes
5. **Exit handling**: Using `sys.exit()` inappropriately
6. **Memory analysis**: Misunderstanding what `sys.getsizeof()` measures
7. **Thread safety**: Modifying shared state from multiple threads
8. **Platform differences**: Assuming Unix behavior on all platforms

Always validate inputs, restore modified state, and use appropriate error handling patterns.
