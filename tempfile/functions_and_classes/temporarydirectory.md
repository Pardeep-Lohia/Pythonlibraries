# TemporaryDirectory Class

The `TemporaryDirectory` class provides a secure and convenient way to create temporary directories that are automatically cleaned up when no longer needed. It ensures that temporary directory structures are properly managed and removed, preventing disk space leaks and security issues.

## Overview

`TemporaryDirectory` creates a temporary directory and all its contents are automatically deleted when the object is destroyed or when explicitly exiting a context manager. This class is essential for applications that need isolated directory spaces for processing, caching, or staging data.

## Basic Usage

```python
import tempfile

# Using context manager (recommended)
with tempfile.TemporaryDirectory() as temp_dir:
    print(f"Temporary directory: {temp_dir}")
    # Use temp_dir for file operations
    # Directory automatically cleaned up on exit

# Manual cleanup
temp_dir = tempfile.TemporaryDirectory()
try:
    print(f"Temporary directory: {temp_dir.name}")
    # Use temp_dir.name for operations
finally:
    temp_dir.cleanup()  # Explicit cleanup
```

## Constructor Parameters

### `suffix`
- **Type**: `str` or `None`
- **Default**: `''`
- **Description**: Suffix for the directory name

```python
with tempfile.TemporaryDirectory(suffix='_cache') as temp_dir:
    print(temp_dir)  # e.g., /tmp/tmpXXXXXX_cache
```

### `prefix`
- **Type**: `str` or `None`
- **Default**: `'tmp'`
- **Description**: Prefix for the directory name

```python
with tempfile.TemporaryDirectory(prefix='myapp_') as temp_dir:
    print(temp_dir)  # e.g., /tmp/myapp_XXXXXX
```

### `dir`
- **Type**: `str` or `None`
- **Default**: `None` (system default temp directory)
- **Description**: Directory where the temporary directory will be created

```python
import os
custom_temp = os.path.join(os.getcwd(), 'temp')
os.makedirs(custom_temp, exist_ok=True)

with tempfile.TemporaryDirectory(dir=custom_temp) as temp_dir:
    print(temp_dir)  # Created in custom_temp directory
```

### `ignore_cleanup_errors`
- **Type**: `bool`
- **Default**: `False`
- **Description**: If `True`, errors during cleanup are ignored

```python
# Ignore cleanup errors (useful in some edge cases)
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
    # Even if some files can't be deleted, no exception is raised
    pass
```

## Properties and Methods

### `name` Property
Returns the absolute path to the temporary directory.

```python
temp_dir = tempfile.TemporaryDirectory()
print(temp_dir.name)  # /tmp/tmpXXXXXX
temp_dir.cleanup()
```

### `cleanup()` Method
Manually cleans up the temporary directory and its contents.

```python
temp_dir = tempfile.TemporaryDirectory()
# ... use temp_dir.name ...
temp_dir.cleanup()  # Explicit cleanup
```

## Advanced Usage Patterns

### Creating Directory Structures

```python
with tempfile.TemporaryDirectory() as temp_dir:
    # Create nested directory structure
    import os
    dirs = ['data', 'logs', 'cache', 'output']
    for dir_name in dirs:
        os.makedirs(os.path.join(temp_dir, dir_name))

    # Create files in different directories
    with open(os.path.join(temp_dir, 'data', 'input.txt'), 'w') as f:
        f.write('Input data')

    with open(os.path.join(temp_dir, 'logs', 'app.log'), 'w') as f:
        f.write('Log entry')
```

### Using with pathlib

```python
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # Create files and directories using pathlib
    (temp_path / 'config' / 'settings.json').parent.mkdir(parents=True, exist_ok=True)
    (temp_path / 'config' / 'settings.json').write_text('{"debug": true}')

    # Iterate through files
    for file_path in temp_path.rglob('*.json'):
        print(f"Found config file: {file_path}")
```

### Batch Processing

```python
def process_files_in_temp_dir(file_list, processor_func):
    with tempfile.TemporaryDirectory(prefix='batch_') as temp_dir:
        results = {}

        # Stage input files
        for filename, content in file_list.items():
            input_path = os.path.join(temp_dir, f"input_{filename}")
            with open(input_path, 'w') as f:
                f.write(content)

        # Process files
        for filename in file_list.keys():
            input_path = os.path.join(temp_dir, f"input_{filename}")
            output_path = os.path.join(temp_dir, f"output_{filename}")

            with open(input_path, 'r') as f:
                data = f.read()

            processed_data = processor_func(data)

            with open(output_path, 'w') as f:
                f.write(processed_data)

            results[filename] = processed_data

        return results
```

### Exception Safety

```python
def safe_processing():
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Processing that might fail
            risky_operation(temp_dir)
        except Exception as e:
            print(f"Processing failed: {e}")
            # Directory automatically cleaned up even on failure
            raise
```

## Integration with Other tempfile Classes

### Combining with NamedTemporaryFile

```python
with tempfile.TemporaryDirectory() as temp_dir:
    # Create temporary files within the temporary directory
    temp_files = []
    for i in range(3):
        with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as f:
            f.write(f"Data for file {i}".encode())
            temp_files.append(f.name)

    print(f"Created {len(temp_files)} files in temp directory")
    # All files automatically cleaned up with directory
```

### Using SpooledTemporaryFile in TemporaryDirectory

```python
with tempfile.TemporaryDirectory() as temp_dir:
    # Use spooled files for processing
    with tempfile.SpooledTemporaryFile(dir=temp_dir, max_size=1024*1024) as f:
        f.write(large_data)
        f.seek(0)
        process_data(f)
```

## Performance Considerations

### Directory Creation Overhead
- `TemporaryDirectory` uses system calls to create secure directories
- Minimal overhead compared to manual directory management
- Automatic cleanup prevents accumulation of temp directories

### Cleanup Performance
- Cleanup uses `shutil.rmtree()` for efficient recursive deletion
- Large directory trees may take time to clean up
- Consider using `ignore_cleanup_errors=True` for fault tolerance

### Memory Usage
- Only directory paths are stored in memory
- File contents are on disk
- Suitable for large temporary file collections

## Security Features

### Secure Directory Creation
- Uses system secure temporary directory creation functions
- Prevents race conditions in directory creation
- Automatic permission restrictions

### Automatic Cleanup
- Prevents temporary file accumulation
- Reduces risk of sensitive data exposure
- Exception-safe resource management

### Permission Handling
- Created directories have restrictive permissions
- Prevents unauthorized access to temporary data

## Error Handling

### Cleanup Errors
```python
try:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create files that might be locked
        create_locked_files(temp_dir)
except OSError as e:
    print(f"Cleanup error: {e}")
```

### Disk Space Issues
```python
try:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Operations that might exhaust disk space
        create_many_files(temp_dir)
except OSError as e:
    if "No space left on device" in str(e):
        print("Insufficient disk space")
    else:
        print(f"Other error: {e}")
```

### Permission Issues
```python
try:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Operations requiring specific permissions
        create_protected_files(temp_dir)
except PermissionError as e:
    print(f"Permission error: {e}")
```

## Use Cases

### Data Processing Pipelines
```python
def process_dataset(input_files):
    with tempfile.TemporaryDirectory() as workspace:
        # Extract and stage data
        for input_file in input_files:
            extract_to_workspace(input_file, workspace)

        # Process data
        intermediate_results = process_in_workspace(workspace)

        # Generate final output
        final_result = generate_output(intermediate_results, workspace)

        return final_result
```

### Testing Environments
```python
import unittest

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_processing(self):
        # Use self.temp_dir.name for test isolation
        test_file = os.path.join(self.temp_dir.name, 'test.dat')
        # ... test code ...
```

### Build Systems
```python
def build_project(source_dir, build_config):
    with tempfile.TemporaryDirectory(prefix='build_') as build_dir:
        # Copy source files
        copy_source_to_build_dir(source_dir, build_dir)

        # Compile
        compile_sources(build_dir, build_config)

        # Package
        package_build(build_dir)

        # Return package path
        return find_package(build_dir)
```

### Cache Management
```python
class TempFileCache:
    def __init__(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix='cache_')

    def get(self, key):
        cache_file = os.path.join(self.temp_dir.name, key)
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return f.read()
        return None

    def put(self, key, data):
        cache_file = os.path.join(self.temp_dir.name, key)
        with open(cache_file, 'wb') as f:
            f.write(data)

    def clear(self):
        # Recreate temp directory to clear cache
        self.temp_dir.cleanup()
        self.temp_dir = tempfile.TemporaryDirectory(prefix='cache_')
```

## Best Practices

1. **Always use context managers** for automatic cleanup
2. **Handle exceptions properly** to ensure cleanup occurs
3. **Use descriptive prefixes** for debugging
4. **Consider disk space** for large temporary structures
5. **Test cleanup behavior** in your applications
6. **Use pathlib** for modern path handling
7. **Combine with other tempfile classes** for complex scenarios

## Limitations

- **Cleanup timing**: Directory persists until object destruction
- **Nested cleanup**: Complex nested structures may have cleanup order issues
- **Platform differences**: Behavior may vary slightly across platforms
- **Permission inheritance**: File permissions in temp dir follow normal rules

## Comparison with Alternatives

| Feature | TemporaryDirectory | mkdtemp() | Manual mkdir |
|---------|-------------------|-----------|--------------|
| Auto cleanup | Yes | No | No |
| Exception safe | Yes | No | No |
| Secure creation | Yes | Yes | No |
| Context manager | Yes | No | No |
| Cross-platform | Yes | Yes | Partial |

## Conclusion

`TemporaryDirectory` is the recommended approach for temporary directory management in Python. It provides security, convenience, and reliability that manual approaches cannot match. Use it whenever you need isolated directory spaces for processing, testing, or data staging.
