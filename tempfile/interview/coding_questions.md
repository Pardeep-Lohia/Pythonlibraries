# Coding Questions for `tempfile` Module Interviews

This document contains coding problems and exercises related to Python's `tempfile` module that are commonly asked in technical interviews.

## Basic Coding Problems

### 1. Safe Temporary File Creation

**Problem:** Write a function that safely creates a temporary file, writes data to it, and ensures it's properly cleaned up.

**Solution:**
```python
import tempfile
import os

def safe_write_temp_data(data):
    """
    Safely write data to a temporary file with automatic cleanup.
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(data)
        temp_path = temp_file.name

    try:
        # Use the temporary file
        print(f"Data written to: {temp_path}")
        with open(temp_path, 'r') as f:
            content = f.read()
        return content
    finally:
        # Manual cleanup since delete=False
        os.unlink(temp_path)

# Usage
result = safe_write_temp_data("Hello, temporary world!")
print(result)
```

**Follow-up Questions:**
- Why use `delete=False`?
- What happens if an exception occurs?
- How would you modify this for binary data?

### 2. Temporary Directory Context Manager

**Problem:** Implement a context manager that creates a temporary directory and automatically cleans it up, including any files created within it.

**Solution:**
```python
import tempfile
import os
from contextlib import contextmanager

@contextmanager
def temp_workspace():
    """
    Context manager for temporary workspace directory.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        # Clean up all files and subdirectories
        import shutil
        shutil.rmtree(temp_dir)

# Usage
with temp_workspace() as workspace:
    # Create files in the workspace
    file1 = os.path.join(workspace, "data.txt")
    file2 = os.path.join(workspace, "config.json")

    with open(file1, 'w') as f:
        f.write("Temporary data")

    with open(file2, 'w') as f:
        f.write('{"setting": "value"}')

    print(f"Workspace: {workspace}")
    print(f"Files: {os.listdir(workspace)}")

# Directory automatically cleaned up
print(f"Workspace exists: {os.path.exists(workspace)}")
```

**Alternative Solution using built-in:**
```python
# Using the built-in TemporaryDirectory
with tempfile.TemporaryDirectory() as workspace:
    # Same usage as above
    pass
```

### 3. Memory-Efficient File Processing

**Problem:** Write a function that processes large files efficiently using `SpooledTemporaryFile`, switching between memory and disk storage based on size.

**Solution:**
```python
import tempfile

def process_large_data(data, max_memory=1024*1024):
    """
    Process data using SpooledTemporaryFile for memory efficiency.
    """
    with tempfile.SpooledTemporaryFile(max_size=max_memory, mode='w+') as temp_file:
        # Write data (may stay in memory or spill to disk)
        temp_file.write(data)
        temp_file.flush()

        # Get file size and storage location
        temp_file.seek(0, 2)  # Seek to end
        size = temp_file.tell()
        temp_file.seek(0)  # Seek back to beginning

        # Determine storage type
        if hasattr(temp_file, '_file') and hasattr(temp_file._file, 'read'):
            storage = "memory" if isinstance(temp_file._file, io.BytesIO) else "disk"
        else:
            storage = "disk"

        # Process the data
        content = temp_file.read()
        processed = content.upper()  # Example processing

        return {
            'original_size': len(data),
            'temp_size': size,
            'storage_type': storage,
            'processed_data': processed
        }

# Test with different sizes
small_data = b"Hello, World!"
large_data = b"X" * (2 * 1024 * 1024)  # 2MB

print("Small data:", process_large_data(small_data))
print("Large data:", process_large_data(large_data))
```

## Intermediate Coding Problems

### 4. Temporary File with Custom Cleanup

**Problem:** Create a temporary file that can be accessed by external programs but ensures cleanup even if the program crashes.

**Solution:**
```python
import tempfile
import os
import atexit
import signal

class ManagedTempFile:
    """
    Temporary file with guaranteed cleanup.
    """
    def __init__(self, data=None, suffix='', prefix='tmp_'):
        self.temp_file = tempfile.NamedTemporaryFile(
            suffix=suffix,
            prefix=prefix,
            delete=False
        )

        if data:
            self.temp_file.write(data)
        self.temp_file.close()  # Close but don't delete

        self.path = self.temp_file.name
        self._register_cleanup()

    def _register_cleanup(self):
        """Register cleanup handlers."""
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle termination signals."""
        self.cleanup()
        raise SystemExit()

    def cleanup(self):
        """Clean up the temporary file."""
        try:
            if os.path.exists(self.path):
                os.unlink(self.path)
        except OSError:
            pass  # Already deleted or permission issue

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

# Usage
with ManagedTempFile(data=b"Sensitive data") as temp:
    print(f"File created: {temp.path}")
    # File can be accessed by external programs
    # Will be cleaned up even on crash

print(f"File cleaned up: {not os.path.exists(temp.path)}")
```

### 5. Batch File Processor with Temporary Storage

**Problem:** Implement a batch file processor that uses temporary directories to organize intermediate results.

**Solution:**
```python
import tempfile
import os
import glob
import shutil

class BatchFileProcessor:
    """
    Process multiple files using temporary storage.
    """
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='batch_processor_')

    def process_files(self, file_paths, processor_func):
        """
        Process multiple files with temporary intermediate storage.
        """
        results = {}

        try:
            # Stage 1: Copy files to temp directory
            staged_files = self._stage_files(file_paths)

            # Stage 2: Process each file
            processed_files = []
            for staged_file in staged_files:
                processed_file = self._process_single_file(
                    staged_file, processor_func
                )
                processed_files.append(processed_file)

            # Stage 3: Collect results
            results = self._collect_results(processed_files)

        finally:
            # Clean up
            shutil.rmtree(self.temp_dir)

        return results

    def _stage_files(self, file_paths):
        """Stage input files to temp directory."""
        staged = []
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            staged_path = os.path.join(self.temp_dir, f"input_{filename}")
            shutil.copy2(file_path, staged_path)
            staged.append(staged_path)
        return staged

    def _process_single_file(self, input_file, processor_func):
        """Process a single file."""
        # Create output filename
        basename = os.path.basename(input_file)
        output_file = os.path.join(
            self.temp_dir,
            f"processed_{basename}"
        )

        # Apply processing function
        with open(input_file, 'r') as f:
            data = f.read()

        processed_data = processor_func(data)

        with open(output_file, 'w') as f:
            f.write(processed_data)

        return output_file

    def _collect_results(self, processed_files):
        """Collect processing results."""
        results = {}
        for processed_file in processed_files:
            filename = os.path.basename(processed_file)
            with open(processed_file, 'r') as f:
                results[filename] = f.read()
        return results

# Example usage
def uppercase_processor(data):
    """Example processor that uppercases text."""
    return data.upper()

processor = BatchFileProcessor()

# Create test files
test_files = []
for i in range(3):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(f"Content of file {i}\n")
        test_files.append(f.name)

try:
    results = processor.process_files(test_files, uppercase_processor)
    for filename, content in results.items():
        print(f"{filename}: {content.strip()}")
finally:
    # Clean up test files
    for f in test_files:
        os.unlink(f)
```

### 6. Secure File Upload Handler

**Problem:** Implement a secure file upload handler that uses temporary files to validate uploads before moving them to permanent storage.

**Solution:**
```python
import tempfile
import os
import hashlib
import magic  # python-magic library for file type detection

class SecureFileUploadHandler:
    """
    Secure file upload handler using temporary files.
    """

    def __init__(self, max_size=10*1024*1024, allowed_types=None):
        self.max_size = max_size
        self.allowed_types = allowed_types or ['text/plain', 'image/jpeg', 'application/pdf']

    def handle_upload(self, file_data, filename):
        """
        Handle file upload with security checks.
        """
        # Create temporary file for validation
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_data)
            temp_path = temp_file.name

        try:
            # Perform security checks
            self._validate_file(temp_path, file_data, filename)

            # If validation passes, move to permanent location
            final_path = self._move_to_permanent(temp_path, filename)

            return {
                'success': True,
                'path': final_path,
                'size': len(file_data),
                'hash': self._calculate_hash(file_data)
            }

        except (ValueError, OSError) as e:
            # Clean up on failure
            os.unlink(temp_path)
            return {
                'success': False,
                'error': str(e)
            }

    def _validate_file(self, temp_path, file_data, filename):
        """Validate uploaded file."""
        # Check file size
        if len(file_data) > self.max_size:
            raise ValueError(f"File too large: {len(file_data)} > {self.max_size}")

        # Check file type using magic
        file_type = magic.from_file(temp_path, mime=True)
        if file_type not in self.allowed_types:
            raise ValueError(f"Invalid file type: {file_type}")

        # Additional security checks
        if self._contains_suspicious_content(file_data):
            raise ValueError("File contains suspicious content")

    def _contains_suspicious_content(self, data):
        """Check for suspicious content patterns."""
        # Simple check for common attack patterns
        suspicious_patterns = [
            b'<script',
            b'javascript:',
            b'onload=',
            b'<?php'
        ]

        data_lower = data.lower()
        for pattern in suspicious_patterns:
            if pattern in data_lower:
                return True
        return False

    def _calculate_hash(self, data):
        """Calculate SHA256 hash of file data."""
        return hashlib.sha256(data).hexdigest()

    def _move_to_permanent(self, temp_path, filename):
        """Move validated file to permanent storage."""
        # Create uploads directory if needed
        upload_dir = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        # Generate safe filename
        safe_filename = self._generate_safe_filename(filename)
        final_path = os.path.join(upload_dir, safe_filename)

        # Move file
        os.rename(temp_path, final_path)
        return final_path

    def _generate_safe_filename(self, filename):
        """Generate a safe filename."""
        # Remove path separators and dangerous characters
        safe_name = os.path.basename(filename)
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '._-')

        # Add timestamp to prevent conflicts
        import time
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(safe_name)
        return f"{name}_{timestamp}{ext}"

# Usage example
handler = SecureFileUploadHandler()

# Simulate file upload
test_data = b"This is a test file content."
result = handler.handle_upload(test_data, "test.txt")

if result['success']:
    print(f"File uploaded successfully: {result['path']}")
else:
    print(f"Upload failed: {result['error']}")
```

## Advanced Coding Problems

### 7. Concurrent Temporary File Manager

**Problem:** Implement a thread-safe temporary file manager that can handle concurrent file creation and cleanup in a multi-threaded application.

**Solution:**
```python
import tempfile
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class ConcurrentTempFileManager:
    """
    Thread-safe temporary file manager for concurrent applications.
    """

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='concurrent_temp_')
        self.files = set()
        self.lock = threading.RLock()  # Reentrant lock
        self.executor = ThreadPoolExecutor(max_workers=4)

    def create_temp_file(self, data=None, suffix='', prefix='tmp_'):
        """
        Create a temporary file in a thread-safe manner.
        """
        with self.lock:
            temp_file = tempfile.NamedTemporaryFile(
                dir=self.temp_dir,
                suffix=suffix,
                prefix=prefix,
                delete=False
            )

            if data:
                temp_file.write(data)
            temp_file.close()

            self.files.add(temp_file.name)
            return temp_file.name

    def create_temp_file_async(self, data, callback=None):
        """
        Create temporary file asynchronously.
        """
        future = self.executor.submit(self.create_temp_file, data)
        if callback:
            future.add_done_callback(lambda f: callback(f.result()))
        return future

    def cleanup_file(self, file_path):
        """
        Safely remove a temporary file.
        """
        with self.lock:
            if file_path in self.files:
                try:
                    os.unlink(file_path)
                    self.files.remove(file_path)
                except OSError:
                    pass  # Already deleted

    def cleanup_all(self):
        """
        Clean up all temporary files and directory.
        """
        with self.lock:
            for file_path in list(self.files):
                try:
                    os.unlink(file_path)
                except OSError:
                    pass

            try:
                os.rmdir(self.temp_dir)
            except OSError:
                pass  # Directory not empty or already deleted

            self.files.clear()

    def get_stats(self):
        """
        Get statistics about temporary file usage.
        """
        with self.lock:
            return {
                'temp_dir': self.temp_dir,
                'active_files': len(self.files),
                'total_size': sum(
                    os.path.getsize(f) for f in self.files
                    if os.path.exists(f)
                )
            }

# Thread-safe usage example
def worker_thread(manager, thread_id):
    """Worker function for testing concurrent access."""
    # Create some temporary files
    files = []
    for i in range(3):
        data = f"Thread {thread_id}, file {i}".encode()
        file_path = manager.create_temp_file(data)
        files.append(file_path)
        time.sleep(0.01)  # Simulate work

    # Clean up some files
    for file_path in files[:2]:  # Leave one file
        manager.cleanup_file(file_path)

    return files[2]  # Return remaining file

# Test concurrent usage
manager = ConcurrentTempFileManager()

try:
    # Run multiple threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(worker_thread, manager, i)
            for i in range(4)
        ]

        remaining_files = [f.result() for f in futures]

    print(f"Stats: {manager.get_stats()}")

    # Clean up remaining files
    for file_path in remaining_files:
        manager.cleanup_file(file_path)

finally:
    manager.cleanup_all()

print(f"Final cleanup complete. Dir exists: {os.path.exists(manager.temp_dir)}")
```

### 8. Temporary File Cache with LRU Eviction

**Problem:** Implement a temporary file-based cache with LRU (Least Recently Used) eviction policy.

**Solution:**
```python
import tempfile
import os
import time
import threading
from collections import OrderedDict

class TempFileCache:
    """
    LRU cache using temporary files for storage.
    """

    def __init__(self, max_size=100, max_memory=50*1024*1024):
        self.max_size = max_size  # Max number of cached items
        self.max_memory = max_memory  # Max memory usage
        self.cache = OrderedDict()  # {key: (file_path, size, access_time)}
        self.temp_dir = tempfile.mkdtemp(prefix='cache_')
        self.lock = threading.RLock()
        self._memory_usage = 0

    def get(self, key):
        """
        Retrieve item from cache.
        """
        with self.lock:
            if key in self.cache:
                file_path, size, _ = self.cache[key]
                # Update access time (move to end)
                self.cache.move_to_end(key)
                # Read and return data
                with open(file_path, 'rb') as f:
                    return f.read()
            return None

    def put(self, key, data):
        """
        Store item in cache.
        """
        with self.lock:
            # Remove existing entry if present
            if key in self.cache:
                self._remove_entry(key)

            # Create temporary file
            with tempfile.NamedTemporaryFile(
                dir=self.temp_dir,
                delete=False
            ) as f:
                f.write(data)
                file_path = f.name

            # Add to cache
            size = len(data)
            self.cache[key] = (file_path, size, time.time())
            self._memory_usage += size

            # Evict if necessary
            self._evict_if_needed()

    def _evict_if_needed(self):
        """
        Evict items using LRU policy if cache limits exceeded.
        """
        # Evict by count
        while len(self.cache) > self.max_size:
            self._evict_lru()

        # Evict by memory
        while self._memory_usage > self.max_memory and self.cache:
            self._evict_lru()

    def _evict_lru(self):
        """
        Evict the least recently used item.
        """
        key, (file_path, size, _) = self.cache.popitem(last=False)
        try:
            os.unlink(file_path)
        except OSError:
            pass
        self._memory_usage -= size

    def _remove_entry(self, key):
        """
        Remove a cache entry.
        """
        if key in self.cache:
            file_path, size, _ = self.cache[key]
            try:
                os.unlink(file_path)
            except OSError:
                pass
            self._memory_usage -= size
            del self.cache[key]

    def clear(self):
        """
        Clear all cached items.
        """
        with self.lock:
            for file_path, _, _ in self.cache.values():
                try:
                    os.unlink(file_path)
                except OSError:
                    pass
            self.cache.clear()
            self._memory_usage = 0

    def cleanup(self):
        """
        Clean up cache and temporary directory.
        """
        self.clear()
        try:
            os.rmdir(self.temp_dir)
        except OSError:
            pass

    def get_stats(self):
        """
        Get cache statistics.
        """
        with self.lock:
            return {
                'size': len(self.cache),
                'memory_usage': self._memory_usage,
                'max_size': self.max_size,
                'max_memory': self.max_memory,
                'temp_dir': self.temp_dir
            }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

# Usage example
with TempFileCache(max_size=5, max_memory=1024*1024) as cache:
    # Add items to cache
    for i in range(7):  # More than max_size
        data = f"Data for item {i}".encode() * 100  # Make it larger
        cache.put(f"key_{i}", data)

    print(f"Cache stats after adding: {cache.get_stats()}")

    # Access some items (updates LRU order)
    cache.get("key_3")
    cache.get("key_4")

    # Add one more (should evict key_0)
    cache.put("key_new", b"New data")

    print(f"Cache stats after access and add: {cache.get_stats()}")

    # Verify eviction
    evicted_data = cache.get("key_0")
    print(f"Evicted item accessible: {evicted_data is not None}")

# Automatic cleanup on exit
```

### 9. Distributed Temporary File Coordinator

**Problem:** Implement a coordinator that manages temporary files across multiple worker processes in a distributed system.

**Solution:**
```python
import tempfile
import os
import json
import uuid
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

class DistributedTempCoordinator:
    """
    Coordinator for temporary files across distributed workers.
    """

    def __init__(self, base_temp_dir=None):
        self.base_temp_dir = base_temp_dir or tempfile.gettempdir()
        self.session_id = str(uuid.uuid4())[:8]
        self.session_dir = os.path.join(
            self.base_temp_dir,
            f"dist_temp_{self.session_id}"
        )
        os.makedirs(self.session_dir, exist_ok=True)

        # Track worker sessions
        self.worker_sessions = {}
        self.lock = mp.Lock()

    def create_worker_session(self, worker_id):
        """
        Create a session directory for a worker.
        """
        with self.lock:
            worker_dir = os.path.join(self.session_dir, f"worker_{worker_id}")
            os.makedirs(worker_dir, exist_ok=True)
            self.worker_sessions[worker_id] = worker_dir
            return worker_dir

    def allocate_temp_file(self, worker_id, suffix='', prefix='tmp_'):
        """
        Allocate a temporary file for a specific worker.
        """
        worker_dir = self.worker_sessions.get(worker_id)
        if not worker_dir:
            raise ValueError(f"Worker {worker_id} not registered")

        with tempfile.NamedTemporaryFile(
            dir=worker_dir,
            suffix=suffix,
            prefix=prefix,
            delete=False
        ) as f:
            return f.name

    def list_worker_files(self, worker_id):
        """
        List all temporary files for a worker.
        """
        worker_dir = self.worker_sessions.get(worker_id)
        if not worker_dir:
            return []

        try:
            return [
                os.path.join(worker_dir, f)
                for f in os.listdir(worker_dir)
                if os.path.isfile(os.path.join(worker_dir, f))
            ]
        except OSError:
            return []

    def cleanup_worker(self, worker_id):
        """
        Clean up all files for a specific worker.
        """
        worker_dir = self.worker_sessions.get(worker_id)
        if worker_dir and os.path.exists(worker_dir):
            import shutil
            shutil.rmtree(worker_dir)
            del self.worker_sessions[worker_id]

    def cleanup_all(self):
        """
        Clean up the entire session.
        """
        import shutil
        if os.path.exists(self.session_dir):
            shutil.rmtree(self.session_dir)
        self.worker_sessions.clear()

    def get_session_stats(self):
        """
        Get statistics for the entire session.
        """
        total_files = 0
        total_size = 0

        for worker_dir in self.worker_sessions.values():
            if os.path.exists(worker_dir):
                for filename in os.listdir(worker_dir):
                    filepath = os.path.join(worker_dir, filename)
                    if os.path.isfile(filepath):
                        total_files += 1
                        total_size += os.path.getsize(filepath)

        return {
            'session_id': self.session_id,
            'session_dir': self.session_dir,
            'workers': len(self.worker_sessions),
            'total_files': total_files,
            'total_size': total_size
        }

# Worker function for distributed processing
def worker_process(worker_id, coordinator, data_chunk):
    """
    Simulate a worker process that uses temporary files.
    """
    try:
        # Register with coordinator
        worker_dir = coordinator.create_worker_session(worker_id)

        # Process data using temporary files
        temp_file = coordinator.allocate_temp_file(worker_id, suffix='.json')

        # Simulate processing
        result = {
            'worker_id': worker_id,
            'data_size': len(data_chunk),
            'processed_at': str(uuid.uuid4()),
            'temp_file': temp_file
        }

        with open(temp_file, 'w') as f:
            json.dump(result, f)

        return result

    except Exception as e:
        return {'error': str(e), 'worker_id': worker_id}

# Usage example
coordinator = DistributedTempCoordinator()

try:
    # Simulate distributed processing
    data_chunks = [f"chunk_{i}" * 100 for i in range(4)]

    with ProcessPoolExecutor(max_workers=4) as executor:
        # Submit worker tasks
        futures = [
            executor.submit(worker_process, i, coordinator, chunk)
            for i, chunk in enumerate(data_chunks)
        ]

        results = [f.result() for f in futures]

    # Check results
    print("Processing results:")
    for result in results:
        if 'error' not in result:
            print(f"Worker {result['worker_id']}: {result['data_size']} bytes")
        else:
            print(f"Worker {result['worker_id']} error: {result['error']}")

    # Session statistics
    stats = coordinator.get_session_stats()
    print(f"\nSession stats: {stats}")

finally:
    coordinator.cleanup_all()

print(f"Session directory cleaned up: {not os.path.exists(coordinator.session_dir)}")
```

## Performance Benchmarking Problems

### 10. Temporary File Performance Benchmark

**Problem:** Create a comprehensive benchmark comparing the performance of different temporary file approaches.

**Solution:**
```python
import tempfile
import time
import os
import io
from contextlib import contextmanager

class TempFileBenchmark:
    """
    Comprehensive benchmark for temporary file operations.
    """

    def __init__(self):
        self.results = {}

    @contextmanager
    def timer(self, operation_name):
        """Context manager for timing operations."""
        start = time.perf_counter()
        yield
        end = time.perf_counter()
        self.results[operation_name] = end - start

    def benchmark_named_temporary_file(self, data_sizes):
        """Benchmark NamedTemporaryFile operations."""
        print("Benchmarking NamedTemporaryFile...")

        for size in data_sizes:
            data = b'X' * size

            with self.timer(f'NamedTempFile_{size}'):
                with tempfile.NamedTemporaryFile() as f:
                    f.write(data)
                    f.flush()
                    f.seek(0)
                    _ = f.read()

    def benchmark_spooled_temporary_file(self, data_sizes, max_memory=1024*1024):
        """Benchmark SpooledTemporaryFile operations."""
        print("Benchmarking SpooledTemporaryFile...")

        for size in data_sizes:
            data = b'X' * size

            with self.timer(f'SpooledTempFile_{size}'):
                with tempfile.SpooledTemporaryFile(max_size=max_memory) as f:
                    f.write(data)
                    f.flush()
                    f.seek(0)
                    _ = f.read()

    def benchmark_manual_temp_file(self, data_sizes):
        """Benchmark manual temporary file operations."""
        print("Benchmarking manual temp file...")

        for size in data_sizes:
            data = b'X' * size

            with self.timer(f'ManualTempFile_{size}'):
                import tempfile as tf
                fd, path = tf.mkstemp()
                try:
                    with os.fdopen(fd, 'w+b') as f:
                        f.write(data)
                        f.flush()
                        f.seek(0)
                        _ = f.read()
                finally:
                    os.unlink(path)

    def benchmark_memory_buffer(self, data_sizes):
        """Benchmark in-memory operations for comparison."""
        print("Benchmarking memory buffer...")

        for size in data_sizes:
            data = b'X' * size

            with self.timer(f'MemoryBuffer_{size}'):
                buffer = io.BytesIO()
                buffer.write(data)
                buffer.flush()
                buffer.seek(0)
                _ = buffer.read()

    def run_comprehensive_benchmark(self):
        """Run comprehensive benchmark suite."""
        data_sizes = [1024, 1024*100, 1024*1000, 10*1024*1000]  # 1KB, 100KB, 1MB, 10MB

        print("Running comprehensive temporary file benchmark...")
        print("=" * 60)

        # Run all benchmarks
        self.benchmark_memory_buffer(data_sizes)
        self.benchmark_named_temporary_file(data_sizes)
        self.benchmark_spooled_temporary_file(data_sizes)
        self.benchmark_manual_temp_file(data_sizes)

        # Print results
        print("\nBenchmark Results:")
        print("-" * 40)

        for operation, time_taken in sorted(self.results.items()):
            size = operation.split('_')[-1]
            method = '_'.join(operation.split('_')[:-1])
            print("15")

        # Analysis
        print("\nAnalysis:")
        print("-" * 40)

        # Compare small file performance
        small_file_ops = {k: v for k, v in self.results.items() if '1024' in k}
        fastest_small = min(small_file_ops, key=small_file_ops.get)
        print(f"Fastest for small files (1KB): {fastest_small}")

        # Compare large file performance
        large_file_ops = {k: v for k, v in self.results.items() if '10485760' in k}
        fastest_large = min(large_file_ops, key=large_file_ops.get)
        print(f"Fastest for large files (10MB): {fastest_large}")

        # Memory efficiency
        print("\nMemory efficiency notes:")
        print("- SpooledTemporaryFile adapts between memory and disk")
        print("- NamedTemporaryFile always uses disk")
        print("- MemoryBuffer never uses disk")
        print("- Manual approach always uses disk")

# Run benchmark
if __name__ == "__main__":
    benchmark = TempFileBenchmark()
    benchmark.run_comprehensive_benchmark()
```

These coding problems cover a wide range of `tempfile` usage scenarios, from basic file operations to advanced concurrent and distributed systems. They test understanding of security, performance, and proper resource management principles.
