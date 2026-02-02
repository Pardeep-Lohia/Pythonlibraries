# SpooledTemporaryFile Class

The `SpooledTemporaryFile` class provides a file-like object that behaves like a temporary file but optimizes memory usage by keeping data in memory until a specified size threshold is reached.

## Overview

`SpooledTemporaryFile` starts as an in-memory `StringIO` or `BytesIO` object and automatically switches to a temporary file on disk when the data size exceeds the `max_size` parameter. This provides the best of both worlds: fast in-memory operations for small data and disk-based storage for larger data.

## Basic Usage

```python
import tempfile

# Create a spooled temporary file with 1MB threshold
with tempfile.SpooledTemporaryFile(max_size=1024*1024) as f:
    f.write(b'Small data')  # Stored in memory
    f.write(b'Large data that might exceed threshold')  # May spill to disk
    f.seek(0)
    data = f.read()
# File automatically cleaned up
```

## Constructor Parameters

### `max_size`
- **Type**: `int`
- **Default**: `0` (no threshold, always uses disk)
- **Description**: Maximum size in bytes before switching to disk

```python
# Always use memory (if max_size=0, it uses disk)
with tempfile.SpooledTemporaryFile(max_size=0) as f:
    pass

# Use memory up to 1MB, then disk
with tempfile.SpooledTemporaryFile(max_size=1024*1024) as f:
    pass
```

### `mode`
- **Type**: `str`
- **Default**: `'w+b'`
- **Description**: File mode (must be binary for BytesIO compatibility)

```python
# Text mode (less common)
with tempfile.SpooledTemporaryFile(mode='w+', max_size=1024) as f:
    f.write('Text data')
```

### `buffering`
- **Type**: `int` or `None`
- **Default**: `-1`
- **Description**: Buffering policy

### `encoding`
- **Type**: `str` or `None`
- **Default**: `None`
- **Description**: Text encoding (for text modes)

### `newline`
- **Type**: `str` or `None`
- **Default**: `None`
- **Description**: Newline handling (for text modes)

### `suffix`, `prefix`, `dir`
Same as other `tempfile` classes for customizing the temporary file when it spills to disk.

## Behavior and Lifecycle

### Memory Phase
- Data is stored in a `BytesIO` or `StringIO` object
- All operations are fast in-memory operations
- No disk I/O occurs

### Disk Phase (After Threshold)
- Automatically creates a `NamedTemporaryFile`
- Data is copied from memory to disk
- Subsequent operations use the disk file
- File is subject to normal temporary file cleanup

### Transition Process
```python
f = tempfile.SpooledTemporaryFile(max_size=100)
f.write(b'X' * 50)  # Still in memory
print(f._file)  # <BytesIO object>

f.write(b'X' * 60)  # Exceeds threshold, spills to disk
print(f._file)  # <TemporaryFile object>
```

## Methods

`SpooledTemporaryFile` supports all standard file methods:

- `read()`, `readline()`, `readlines()`
- `write()`, `writelines()`
- `seek()`, `tell()`
- `flush()`, `close()`
- `fileno()` (only available after spilling to disk)
- `truncate()`, `isatty()`

### Additional Methods
- `rollover()`: Force transition to disk storage
- `isatty()`: Returns `False`

## Advanced Usage Patterns

### Controlled Spilling
```python
# Force disk usage for large data
with tempfile.SpooledTemporaryFile(max_size=1024) as f:
    f.write(b'Small data')
    f.rollover()  # Force to disk even if under threshold
    large_data = b'X' * 10000
    f.write(large_data)
```

### Integration with Libraries
```python
import csv
import tempfile

# Use with CSV module
with tempfile.SpooledTemporaryFile(mode='w+', max_size=8192) as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Age', 'City'])
    writer.writerow(['Alice', 30, 'New York'])
    f.seek(0)
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

### Custom Spooled File
```python
class CustomSpooledFile(tempfile.SpooledTemporaryFile):
    def __init__(self, max_size=1024*1024, callback=None, *args, **kwargs):
        super().__init__(max_size=max_size, *args, **kwargs)
        self.callback = callback
    
    def rollover(self):
        if self.callback:
            self.callback()
        super().rollover()

# Usage
def on_rollover():
    print("File rolled over to disk")

with CustomSpooledFile(max_size=100, callback=on_rollover) as f:
    f.write(b'X' * 150)  # Triggers callback and rollover
```

## Performance Characteristics

### Memory Usage
- **Small files**: Minimal memory overhead (just the data)
- **Large files**: Memory usage spikes during transition, then stable
- **Threshold consideration**: Set `max_size` based on available RAM

### I/O Performance
- **Memory phase**: Extremely fast (no disk I/O)
- **Disk phase**: Standard temporary file performance
- **Transition cost**: One-time copy operation from memory to disk

### Benchmarks
```python
import time
import tempfile

# Memory-only performance
start = time.time()
with tempfile.SpooledTemporaryFile(max_size=1024*1024) as f:
    for i in range(1000):
        f.write(b'X' * 100)
end = time.time()
print(f"Memory operations: {end - start:.4f}s")

# Disk-spilling performance
start = time.time()
with tempfile.SpooledTemporaryFile(max_size=1024) as f:
    for i in range(1000):
        f.write(b'X' * 100)
end = time.time()
print(f"Disk operations: {end - start:.4f}s")
```

## Use Cases

### Web File Uploads
```python
def process_upload(file_data):
    with tempfile.SpooledTemporaryFile(max_size=1024*1024) as temp_file:
        temp_file.write(file_data)
        
        # Process small files in memory
        if temp_file.tell() <= 1024*1024:
            temp_file.seek(0)
            process_in_memory(temp_file)
        else:
            # Large files already on disk
            process_large_file(temp_file)
```

### Data Streaming
```python
def stream_processor(data_stream):
    with tempfile.SpooledTemporaryFile(max_size=10*1024*1024) as buffer:
        for chunk in data_stream:
            buffer.write(chunk)
            
            # Periodic processing
            if buffer.tell() > 1024*1024:
                buffer.seek(0)
                process_chunk(buffer)
                buffer.seek(0)
                buffer.truncate(0)
```

### Caching Systems
```python
class SmartCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        return None
    
    def set(self, key, data):
        # Use spooled file for potentially large data
        temp_file = tempfile.SpooledTemporaryFile(max_size=1024*1024)
        temp_file.write(data)
        temp_file.seek(0)
        self.cache[key] = temp_file
```

## Error Handling

### Transition Errors
```python
try:
    with tempfile.SpooledTemporaryFile(max_size=100) as f:
        f.write(b'X' * 200)  # May fail during rollover
except OSError as e:
    print(f"Error during file rollover: {e}")
```

### Disk Space Issues
```python
try:
    with tempfile.SpooledTemporaryFile(max_size=1) as f:  # Forces disk usage
        f.write(b'X' * 1024*1024*1024)  # 1GB
except OSError:
    print("Insufficient disk space")
```

## Security Considerations

- **Memory exposure**: Data in memory phase may be visible in core dumps
- **Disk security**: Follows standard temporary file security practices
- **Cleanup**: Automatic cleanup prevents data leakage

## Best Practices

1. **Choose appropriate thresholds** based on your memory constraints
2. **Consider data sensitivity** when deciding memory vs disk storage
3. **Use context managers** for automatic cleanup
4. **Test with various data sizes** to understand behavior
5. **Monitor memory usage** in production environments

## Limitations

- **Binary mode restriction**: Primarily designed for binary data
- **Transition overhead**: One-time cost when spilling to disk
- **Memory pressure**: Large thresholds can cause memory issues
- **Not thread-safe**: Concurrent access requires external synchronization

## Comparison with Alternatives

| Feature | SpooledTemporaryFile | NamedTemporaryFile | BytesIO |
|---------|---------------------|-------------------|---------|
| Memory efficient | Yes | No | No |
| Disk fallback | Yes | Yes | No |
| Automatic cleanup | Yes | Yes | No |
| File-like interface | Yes | Yes | Yes |
| Performance | Adaptive | Consistent | Fast |
| Use case | Variable size data | Known large data | Small data only |
