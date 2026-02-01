# Memory Management Functions

The `sys` module provides several functions and attributes for memory management and monitoring in Python. These tools help developers understand memory usage, track object sizes, and manage memory-related aspects of the interpreter.

## `sys.getsizeof(object[, default])`

Returns the size of an object in bytes.

### Purpose
- Measure memory consumption of Python objects
- Debug memory usage issues
- Optimize data structures

### Syntax
```python
import sys

size = sys.getsizeof(object)
size_with_default = sys.getsizeof(object, default_value)
```

### Parameters
- `object`: The object to measure
- `default`: Optional default value if size cannot be determined

### Examples
```python
import sys

# Basic usage
x = 42
print(sys.getsizeof(x))  # Output: 28 (size of int object)

# String sizes
s = "hello"
print(sys.getsizeof(s))  # Output: 54 (string object + content)

# List sizes
lst = [1, 2, 3, 4, 5]
print(sys.getsizeof(lst))  # Output: 104 (list object overhead + references)

# Dictionary sizes
d = {'a': 1, 'b': 2}
print(sys.getsizeof(d))  # Output: 232 (dict object + hash table)

# Custom object
class MyClass:
    def __init__(self):
        self.value = 42

obj = MyClass()
print(sys.getsizeof(obj))  # Size of instance
print(sys.getsizeof(obj.__dict__))  # Size of instance dict
```

### Edge Cases
- For containers, `getsizeof` returns the size of the container object itself, not the contents
- Use recursion to calculate total memory usage of complex objects
- Some built-in types may have platform-dependent sizes

## `sys.getrefcount(object)`

Returns the reference count of an object.

### Purpose
- Understand object lifetime and garbage collection
- Debug reference cycles and memory leaks
- Analyze object sharing

### Syntax
```python
import sys

ref_count = sys.getrefcount(object)
```

### Parameters
- `object`: The object to check reference count for

### Examples
```python
import sys

# Basic reference counting
x = [1, 2, 3]
print(sys.getrefcount(x))  # Output: 2 (one for x, one for getrefcount argument)

# Function scope
def check_refcount():
    y = "hello"
    print(sys.getrefcount(y))  # Reference count during function execution
    return y

result = check_refcount()
print(sys.getrefcount(result))  # Reference count after function returns

# Multiple references
z = [1, 2, 3]
a = z  # Additional reference
b = z  # Another reference
print(sys.getrefcount(z))  # Output: 4 (z, a, b, getrefcount argument)
```

### Edge Cases
- The function call itself creates a temporary reference
- Reference counts can change during garbage collection
- Not all objects support reference counting (e.g., small integers may be cached)

## `sys.getallocatedblocks()`

Returns the number of memory blocks currently allocated by the interpreter.

### Purpose
- Monitor overall memory allocation
- Track memory usage trends
- Debug memory leaks

### Syntax
```python
import sys

blocks = sys.getallocatedblocks()
```

### Examples
```python
import sys

# Check current allocation
print(f"Currently allocated blocks: {sys.getallocatedblocks()}")

# Create some objects
lst = []
for i in range(1000):
    lst.append([i] * 100)

print(f"After creating objects: {sys.getallocatedblocks()}")

# Delete objects
del lst
print(f"After deletion: {sys.getallocatedblocks()}")
```

### Edge Cases
- This is a debugging function, not for production use
- May not be available in all Python implementations
- Values can fluctuate due to internal interpreter operations

## `sys.gettotalrefcount()` (Debug builds only)

Returns the total number of references in the system.

### Purpose
- Advanced memory debugging
- Understanding interpreter's internal reference management

### Syntax
```python
import sys

total_refs = sys.gettotalrefcount()
```

### Notes
- Only available in debug builds of Python
- Primarily used by core developers and memory specialists

## Memory Management Attributes

### `sys.maxsize`

The maximum value a variable of type `Py_ssize_t` can take.

### Purpose
- Platform-specific size limits
- Memory allocation bounds checking

### Examples
```python
import sys

print(f"Maximum size: {sys.maxsize}")
print(f"In bytes: {sys.maxsize.bit_length() // 8} bytes")

# Check if a size is within limits
size = 2**63 - 1
if size <= sys.maxsize:
    print("Size is within platform limits")
```

### `sys.int_info`

Information about the internal representation of integers.

### Purpose
- Understanding integer implementation details
- Platform-specific integer behavior

### Examples
```python
import sys

print(f"Integer info: {sys.int_info}")
# Output: sys.int_info(bits_per_digit=30, sizeof_digit=4)

# Check integer limits
max_int = 2**(sys.int_info.bits_per_digit * sys.int_info.sizeof_digit * 8) - 1
print(f"Maximum integer value: {max_int}")
```

## Practical Memory Analysis Functions

### Recursive Size Calculation
```python
import sys
from collections import deque

def get_total_size(obj, seen=None):
    """Recursively calculate total memory usage of an object and its contents"""
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    seen.add(obj_id)
    size = sys.getsizeof(obj)

    if isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(get_total_size(item, seen) for item in obj)
    elif isinstance(obj, dict):
        size += sum(get_total_size(k, seen) + get_total_size(v, seen) for k, v in obj.items())
    elif hasattr(obj, '__dict__'):
        size += get_total_size(obj.__dict__, seen)

    return size

# Usage
data = {'numbers': [1, 2, 3], 'text': 'hello', 'nested': {'a': 1, 'b': [4, 5]}}
total_size = get_total_size(data)
print(f"Total memory usage: {total_size} bytes")
```

### Memory Usage Monitoring
```python
import sys
import psutil
import os

def get_memory_usage():
    """Get current memory usage of the process"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss  # Resident Set Size in bytes

def memory_profile(func):
    """Decorator to profile memory usage of a function"""
    def wrapper(*args, **kwargs):
        start_mem = get_memory_usage()
        start_blocks = sys.getallocatedblocks()

        result = func(*args, **kwargs)

        end_mem = get_memory_usage()
        end_blocks = sys.getallocatedblocks()

        print(f"Memory usage: {end_mem - start_mem} bytes")
        print(f"Allocated blocks: {end_blocks - start_blocks}")

        return result
    return wrapper

@memory_profile
def create_large_list(n):
    return [i**2 for i in range(n)]

result = create_large_list(10000)
```

## Best Practices

1. **Use `getsizeof` for shallow size**: Remember it doesn't include referenced objects
2. **Combine with garbage collection**: Use `gc.get_objects()` for comprehensive analysis
3. **Platform awareness**: Memory sizes can vary between platforms
4. **Debug builds**: Some functions only work in debug Python builds
5. **Performance considerations**: Memory analysis can be expensive for large objects

## Common Patterns

### Memory Leak Detection
```python
import sys
import gc

def detect_potential_leaks():
    """Simple memory leak detection"""
    initial_objects = len(gc.get_objects())

    # Perform operations
    for i in range(1000):
        temp = [i] * 100

    gc.collect()
    final_objects = len(gc.get_objects())

    if final_objects > initial_objects + 100:  # Allow some tolerance
        print(f"Potential memory leak: {final_objects - initial_objects} extra objects")
```

### Object Size Comparison
```python
import sys

def compare_structures():
    """Compare memory usage of different data structures"""
    structures = {
        'list': [i for i in range(1000)],
        'tuple': tuple(i for i in range(1000)),
        'set': set(range(1000)),
        'dict': {i: i for i in range(1000)},
    }

    for name, structure in structures.items():
        size = sys.getsizeof(structure)
        print(f"{name}: {size} bytes")
```

This comprehensive coverage of memory management functions in `sys` enables developers to monitor, analyze, and optimize memory usage in Python applications.
