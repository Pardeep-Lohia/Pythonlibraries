# tempfile Module Cheatsheet

A quick reference guide for Python's `tempfile` module functions and classes.

## Quick Reference

### TemporaryFile
```python
import tempfile

# Anonymous temporary file (no filename)
with tempfile.TemporaryFile() as f:
    f.write(b"data")
    f.seek(0)
    data = f.read()
# Automatically deleted
```

### NamedTemporaryFile
```python
# Named temporary file (accessible filename)
with tempfile.NamedTemporaryFile() as f:
    print(f.name)  # e.g., /tmp/tmpXXXXXX
    f.write(b"data")

# Keep file after context
with tempfile.NamedTemporaryFile(delete=False) as f:
    f.write(b"data")
    # File persists after context
os.unlink(f.name)  # Manual cleanup
```

### TemporaryDirectory
```python
# Temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    # Use temp_dir for file operations
    pass
# Automatically deleted with all contents
```

### SpooledTemporaryFile
```python
# Memory-efficient for variable sizes
with tempfile.SpooledTemporaryFile(max_size=1024*1024) as f:
    f.write(b"data")  # In memory if < 1MB, on disk if > 1MB
```

## Function Parameters

### Common Parameters
- `mode`: File mode ('w+b', 'w+', etc.)
- `buffering`: Buffering policy (-1=default, 0=unbuffered, 1=line-buffered)
- `encoding`: Text encoding (for text modes)
- `newline`: Newline handling
- `suffix`: Filename suffix
- `prefix`: Filename prefix
- `dir`: Directory to create in

### TemporaryFile Parameters
```python
tempfile.TemporaryFile(
    mode='w+b',      # Binary mode default
    buffering=-1,    # Default buffering
    encoding=None,   # Not used in binary mode
    newline=None,    # Not used in binary mode
    suffix='',       # No suffix
    prefix='tmp',    # Default prefix
    dir=None         # System temp dir
)
```

### NamedTemporaryFile Parameters
```python
tempfile.NamedTemporaryFile(
    mode='w+b',      # Binary mode default
    buffering=-1,
    encoding=None,
    newline=None,
    suffix='',
    prefix='tmp',
    dir=None,
    delete=True      # Auto-delete on close
)
```

### TemporaryDirectory Parameters
```python
tempfile.TemporaryDirectory(
    suffix='',           # Directory suffix
    prefix='tmp',        # Directory prefix
    dir=None,            # Parent directory
    ignore_cleanup_errors=False  # Raise on cleanup errors
)
```

### SpooledTemporaryFile Parameters
```python
tempfile.SpooledTemporaryFile(
    max_size=0,      # 0 = no limit, always in memory
    mode='w+b',
    buffering=-1,
    encoding=None,
    newline=None,
    suffix='',
    prefix='tmp',
    dir=None
)
```

## Low-Level Functions

### mkstemp()
```python
# Create temp file, return descriptor and path
fd, path = tempfile.mkstemp()
try:
    with os.fdopen(fd, 'w+b') as f:
        f.write(b"data")
finally:
    os.unlink(path)  # Manual cleanup
```

### mkdtemp()
```python
# Create temp directory, return path
temp_dir = tempfile.mkdtemp()
try:
    # Use temp_dir
    pass
finally:
    shutil.rmtree(temp_dir)  # Manual cleanup
```

### gettempdir()
```python
# Get system temp directory
temp_dir = tempfile.gettempdir()
# Returns: '/tmp' on Unix, system temp on Windows
```

### gettempprefix()
```python
# Get temp file prefix
prefix = tempfile.gettempprefix()
# Returns: 'tmp' on Unix, system prefix on Windows
```

## Usage Patterns

### File Processing
```python
# Process data in temp file
with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
    # Write processed data
    f.write(processed_data)
    f.flush()

    # Pass to external command
    subprocess.run(['command', f.name])

os.unlink(f.name)
```

### Directory Operations
```python
# Batch processing in temp directory
with tempfile.TemporaryDirectory() as temp_dir:
    # Create input files
    for i, data in enumerate(datasets):
        with open(f"{temp_dir}/input_{i}.dat", 'w') as f:
            f.write(data)

    # Process files
    results = process_files_in_dir(temp_dir)

    # Save results
    with open(f"{temp_dir}/results.json", 'w') as f:
        json.dump(results, f)
```

### Memory-Efficient Processing
```python
# Handle large or variable-sized data
with tempfile.SpooledTemporaryFile(max_size=10*1024*1024) as f:
    # Write data (in memory if < 10MB, disk if > 10MB)
    f.write(data)

    # Process
    f.seek(0)
    process_data(f)
```

### Context Manager Combinations
```python
# Multiple temp files in temp directory
with tempfile.TemporaryDirectory() as temp_dir:
    with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as f1, \
         tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as f2:

        # Work with f1 and f2
        pass
    # All files cleaned up with directory
```

## Error Handling

### Disk Space Errors
```python
try:
    with tempfile.NamedTemporaryFile() as f:
        f.write(large_data)
except OSError as e:
    if "No space left" in str(e):
        raise MemoryError("Insufficient temp space")
```

### Permission Errors
```python
try:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Operations that might fail
        pass
except PermissionError:
    # Handle permission issues
    pass
```

### Cleanup Errors
```python
# Ignore cleanup errors
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
    # Some files might not be deletable
    pass
```

## Platform Notes

### Unix/Linux
- Temp dir: `/tmp`
- Secure creation: Uses `open()` with `O_EXCL | O_CREAT`
- Permissions: `0o600` (owner read/write)

### Windows
- Temp dir: System temp directory
- Secure creation: Uses secure APIs
- Permissions: Appropriate Windows permissions

### macOS
- Same as Unix/Linux
- Additional security features via SIP

## Security Best Practices

1. **Always use context managers** for automatic cleanup
2. **Use default temp directories** unless you have specific needs
3. **Avoid predictable names** - let tempfile generate them
4. **Handle exceptions** to ensure cleanup
5. **Use appropriate file modes** (binary for data, text for text)
6. **Consider SpooledTemporaryFile** for memory efficiency

## Common Conversions

### From manual temp files
```python
# Old way (insecure)
temp_path = f"/tmp/myapp_{os.getpid()}.tmp"
with open(temp_path, 'w') as f:
    f.write(data)
os.unlink(temp_path)

# New way (secure)
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write(data)
os.unlink(f.name)
```

### From in-memory processing
```python
# Old way (memory intensive)
data = io.BytesIO()
data.write(content)
process(data.getvalue())

# New way (memory efficient)
with tempfile.SpooledTemporaryFile() as f:
    f.write(content)
    f.seek(0)
    process(f)
```

## Performance Tips

- Use `TemporaryFile` for anonymous temp storage
- Use `SpooledTemporaryFile` for variable-sized data
- Use `TemporaryDirectory` for complex file hierarchies
- Avoid `delete=False` unless necessary
- Use appropriate buffering for your use case

## Quick Examples

### CSV Processing
```python
with tempfile.NamedTemporaryFile(mode='w+', newline='', suffix='.csv') as f:
    writer = csv.writer(f)
    writer.writerows(data)
    f.seek(0)
    # Process CSV
```

### JSON Cache
```python
with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
    json.dump(cache_data, f)
    f.flush()
    # Use f.name for external access
os.unlink(f.name)
```

### Log Rotation
```python
with tempfile.TemporaryDirectory() as temp_dir:
    # Rotate logs
    for log_file in log_files:
        temp_log = os.path.join(temp_dir, os.path.basename(log_file))
        shutil.move(log_file, temp_log)
        compress_log(temp_log)
```

This cheatsheet covers the essential usage patterns and options for Python's tempfile module.
