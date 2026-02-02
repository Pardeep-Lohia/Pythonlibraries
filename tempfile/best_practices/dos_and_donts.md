# Do's and Don'ts for Using the `tempfile` Module

This guide outlines the essential best practices for using Python's `tempfile` module safely and effectively. Following these guidelines will help you avoid common pitfalls and security vulnerabilities.

## Do's

### ✅ Use Context Managers
Always use temporary files and directories within context managers to ensure automatic cleanup:

```python
# Good: Automatic cleanup
with tempfile.NamedTemporaryFile() as f:
    f.write(b'data')
    process_file(f.name)

# Also good: Explicit cleanup control
with tempfile.NamedTemporaryFile(delete=False) as f:
    f.write(b'data')
    process_file(f.name)
# File automatically deleted here
```

### ✅ Use Appropriate File Classes
Choose the right temporary file class for your use case:

```python
# For files that need accessible filenames
with tempfile.NamedTemporaryFile() as f:
    external_program(f.name)

# For anonymous temporary files
with tempfile.TemporaryFile() as f:
    f.write(data)
    f.seek(0)
    process_data(f)

# For memory-efficient operations
with tempfile.SpooledTemporaryFile(max_size=1024*1024) as f:
    f.write(large_data)
```

### ✅ Set Proper Permissions
Use restrictive permissions when creating temporary files:

```python
# Good: Restrictive permissions (default behavior)
with tempfile.NamedTemporaryFile() as f:
    f.write(sensitive_data)

# Avoid: Overly permissive permissions
# The tempfile module handles this automatically
```

### ✅ Handle Exceptions Properly
Always handle exceptions that might occur during file operations:

```python
try:
    with tempfile.NamedTemporaryFile() as f:
        f.write(data)
        risky_operation(f.name)
except OSError as e:
    logger.error(f"Failed to process temporary file: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Ensure cleanup even on unexpected errors
```

### ✅ Use Secure Temporary Directories
Let the system choose secure temporary directories:

```python
# Good: System chooses secure location
with tempfile.TemporaryDirectory() as temp_dir:
    # Work in secure temp directory
    pass

# Avoid: Hardcoded temp paths
# temp_dir = "/tmp/my_app"  # Insecure!
```

### ✅ Clean Up Manually When Needed
Use `delete=False` only when necessary and ensure manual cleanup:

```python
# Acceptable when external programs need access
temp_file = tempfile.NamedTemporaryFile(delete=False)
try:
    temp_file.write(data)
    temp_file.close()
    external_process(temp_file.name)
finally:
    os.unlink(temp_file.name)  # Manual cleanup
```

### ✅ Use Descriptive Prefixes and Suffixes
Make temporary files identifiable for debugging:

```python
with tempfile.NamedTemporaryFile(
    prefix='myapp_cache_',
    suffix='.json'
) as f:
    json.dump(cache_data, f)
```

### ✅ Consider Memory vs Disk Trade-offs
Choose appropriate storage based on data size:

```python
# Small data: Use SpooledTemporaryFile for efficiency
with tempfile.SpooledTemporaryFile(max_size=1024*1024) as f:
    f.write(small_data)

# Large data: Use NamedTemporaryFile directly
with tempfile.NamedTemporaryFile() as f:
    f.write(large_data)
```

### ✅ Log Temporary File Operations
Add logging for debugging and monitoring:

```python
import logging

with tempfile.NamedTemporaryFile(prefix='debug_') as f:
    logging.debug(f"Created temporary file: {f.name}")
    f.write(data)
    logging.debug(f"Wrote {len(data)} bytes to temporary file")
```

### ✅ Test with Realistic Data Sizes
Test your code with various data sizes to understand memory behavior:

```python
# Test with different data sizes
test_sizes = [1024, 1024*1024, 100*1024*1024]

for size in test_sizes:
    with tempfile.SpooledTemporaryFile(max_size=1024*1024) as f:
        data = b'X' * size
        f.write(data)
        # Test if behavior changes with size
```

## Don'ts

### ❌ Don't Use `mktemp()` (Deprecated)
The `mktemp()` function is deprecated and insecure:

```python
# Bad: Race condition vulnerability
temp_path = tempfile.mktemp()  # Don't use!
with open(temp_path, 'w') as f:
    f.write(data)

# Good: Use secure alternatives
with tempfile.NamedTemporaryFile() as f:
    f.write(data)
```

### ❌ Don't Hardcode Temporary Paths
Avoid hardcoding temporary file paths:

```python
# Bad: Hardcoded path
temp_file = "/tmp/my_temp_file.txt"
with open(temp_file, 'w') as f:
    f.write(data)

# Good: Let system choose
with tempfile.NamedTemporaryFile() as f:
    f.write(data)
```

### ❌ Don't Forget to Close Files
Always close temporary files before external access:

```python
# Bad: File not closed before external access
with tempfile.NamedTemporaryFile() as f:
    f.write(data)
    external_program(f.name)  # May fail - file still open

# Good: Close file first
with tempfile.NamedTemporaryFile() as f:
    f.write(data)
    f.close()  # Close before external access
    external_program(f.name)
```

### ❌ Don't Use Temporary Files for Sensitive Data Without Care
Be cautious with sensitive data in temporary files:

```python
# Problematic: Sensitive data in world-readable temp file
with tempfile.NamedTemporaryFile() as f:
    f.write(credit_card_data)

# Better: Use memory buffers for sensitive data
import io
buffer = io.BytesIO()
buffer.write(credit_card_data)
# Process from memory
```

### ❌ Don't Mix Manual and Automatic Cleanup
Avoid mixing cleanup strategies inconsistently:

```python
# Bad: Inconsistent cleanup
temp_files = []
for i in range(3):
    if i % 2 == 0:
        f = tempfile.NamedTemporaryFile()  # Auto cleanup
    else:
        f = tempfile.NamedTemporaryFile(delete=False)  # Manual cleanup
    temp_files.append(f)

# Good: Consistent strategy
temp_files = []
try:
    for i in range(3):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(data)
        f.close()
        temp_files.append(f.name)
finally:
    for name in temp_files:
        os.unlink(name)
```

### ❌ Don't Ignore Disk Space Constraints
Consider disk space limitations:

```python
# Bad: No consideration for disk space
with tempfile.NamedTemporaryFile() as f:
    f.write(huge_data)  # May fill up disk

# Good: Check available space
import shutil
disk_stats = shutil.disk_usage(tempfile.gettempdir())
if len(data) > disk_stats.free * 0.1:  # Leave 10% free
    raise OSError("Insufficient disk space")
with tempfile.NamedTemporaryFile() as f:
    f.write(data)
```

### ❌ Don't Use Temporary Files for Inter-Process Communication
Avoid using temporary files for IPC when other methods are available:

```python
# Bad: Using temp file for IPC
with tempfile.NamedTemporaryFile() as f:
    f.write(message)
    f.close()
    # Other process reads f.name

# Better: Use pipes, queues, or sockets
import multiprocessing
queue = multiprocessing.Queue()
queue.put(message)
```

### ❌ Don't Leave Temporary Files Open Longer Than Necessary
Close temporary files as soon as possible:

```python
# Bad: File kept open too long
with tempfile.NamedTemporaryFile() as f:
    f.write(data)
    # ... lots of processing ...
    result = process_data(f)  # File still open

# Good: Close when no longer needed
with tempfile.NamedTemporaryFile() as f:
    f.write(data)
    f.close()  # Close immediately
    result = process_data(f.name)
```

### ❌ Don't Use Temporary Files for Configuration
Avoid storing configuration in temporary files:

```python
# Bad: Config in temp file
with tempfile.NamedTemporaryFile(mode='w') as f:
    json.dump(config, f)
    f.close()
    load_config(f.name)

# Good: Use proper config storage
config_file = os.path.expanduser('~/.myapp/config.json')
os.makedirs(os.path.dirname(config_file), exist_ok=True)
with open(config_file, 'w') as f:
    json.dump(config, f)
```

### ❌ Don't Assume Temporary Directory Permissions
Don't assume specific permissions on temp directories:

```python
# Bad: Assuming permissions
temp_dir = tempfile.mkdtemp()
subprocess.run(['chmod', '755', temp_dir])  # May not be necessary

# Good: Let tempfile handle permissions
with tempfile.TemporaryDirectory() as temp_dir:
    # Use as-is
    pass
```

## Security Checklist

- [ ] Use context managers for automatic cleanup
- [ ] Never use `mktemp()` or hardcoded temp paths
- [ ] Close files before external program access
- [ ] Consider data sensitivity and permissions
- [ ] Test with various data sizes and disk space scenarios
- [ ] Handle exceptions properly
- [ ] Use descriptive prefixes for debugging
- [ ] Avoid race conditions in multi-threaded code

## Performance Checklist

- [ ] Choose appropriate file classes for data size
- [ ] Use `SpooledTemporaryFile` for variable-sized data
- [ ] Close files when no longer needed
- [ ] Consider memory vs disk trade-offs
- [ ] Test with realistic data volumes
- [ ] Monitor disk space usage
- [ ] Use appropriate buffering

Following these do's and don'ts will help you use the `tempfile` module safely, efficiently, and maintainably in your Python applications.
