# Coding Interview Questions

## File System Operations

### 1. Safe Path Join Function
**Problem:** Implement a function that safely joins paths without allowing directory traversal attacks.

**Requirements:**
- Prevent `../../../etc/passwd` style attacks
- Handle absolute paths correctly
- Normalize the result

**Solution:**
```python
import os

def safe_path_join(base_dir, user_path):
    """
    Safely join a base directory with a user-provided path.

    Args:
        base_dir (str): The base directory
        user_path (str): User-provided path component

    Returns:
        str: Safe absolute path within base_dir

    Raises:
        ValueError: If path traversal is detected
    """
    # Normalize both paths
    base_dir = os.path.abspath(base_dir)
    full_path = os.path.normpath(os.path.join(base_dir, user_path))

    # Ensure the result is within the base directory
    if not full_path.startswith(base_dir):
        raise ValueError("Path traversal attempt detected")

    return full_path

# Test cases
try:
    # Valid paths
    result = safe_path_join('/home/user', 'documents/file.txt')
    print(f"Valid: {result}")

    # Path traversal attempt
    result = safe_path_join('/home/user', '../../../etc/passwd')
    print(f"Traversal: {result}")
except ValueError as e:
    print(f"Blocked: {e}")
```

### 2. File Organizer by Extension
**Problem:** Write a function that organizes files in a directory by their file extensions.

**Requirements:**
- Create subdirectories for each extension
- Move files into appropriate directories
- Handle files without extensions
- Skip directories

**Solution:**
```python
import os
import shutil

def organize_files_by_extension(directory):
    """
    Organize files in a directory by their extensions.

    Args:
        directory (str): Directory to organize

    Returns:
        dict: Summary of organization results
    """
    results = {}

    # Get all files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(filepath):
            continue

        # Get file extension
        _, ext = os.path.splitext(filename)
        ext = ext.lower() if ext else 'no_extension'

        # Create extension directory
        ext_dir = os.path.join(directory, ext[1:] if ext.startswith('.') else ext)
        os.makedirs(ext_dir, exist_ok=True)

        # Move file
        dest_path = os.path.join(ext_dir, filename)
        shutil.move(filepath, dest_path)

        # Track results
        if ext not in results:
            results[ext] = []
        results[ext].append(filename)

    return results

# Usage
results = organize_files_by_extension('/path/to/organize')
for ext, files in results.items():
    print(f"{ext}: {len(files)} files")
```

### 3. Directory Size Calculator
**Problem:** Calculate the total size of a directory including all subdirectories.

**Requirements:**
- Recursively traverse directories
- Handle permission errors gracefully
- Return size in bytes and human-readable format

**Solution:**
```python
import os

def calculate_directory_size(directory):
    """
    Calculate the total size of a directory.

    Args:
        directory (str): Directory path

    Returns:
        dict: Size information
    """
    total_size = 0
    file_count = 0
    dir_count = 0

    for root, dirs, files in os.walk(directory):
        dir_count += 1

        for file in files:
            try:
                filepath = os.path.join(root, file)
                total_size += os.path.getsize(filepath)
                file_count += 1
            except (OSError, PermissionError):
                # Skip files we can't access
                continue

    return {
        'total_size_bytes': total_size,
        'file_count': file_count,
        'dir_count': dir_count,
        'size_mb': total_size / (1024 * 1024),
        'size_gb': total_size / (1024 * 1024 * 1024)
    }

def format_size(size_bytes):
    """Format size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return ".1f"
        size_bytes /= 1024.0
    return ".1f"

# Usage
size_info = calculate_directory_size('/home/user')
print(f"Size: {format_size(size_info['total_size_bytes'])}")
print(f"Files: {size_info['file_count']}")
```

## Environment Variables

### 4. Configuration Loader from Environment
**Problem:** Load application configuration from environment variables with validation and type conversion.

**Requirements:**
- Support different data types (string, int, float, bool)
- Provide defaults for missing variables
- Validate required variables

**Solution:**
```python
import os

class ConfigLoader:
    """Load configuration from environment variables."""

    def __init__(self, prefix='', required_vars=None):
        self.prefix = prefix
        self.required_vars = required_vars or []

    def load_config(self):
        """
        Load configuration from environment variables.

        Returns:
            dict: Configuration dictionary

        Raises:
            ValueError: If required variables are missing
        """
        config = {}

        # Check required variables
        for var in self.required_vars:
            full_var = f"{self.prefix}{var}"
            if full_var not in os.environ:
                raise ValueError(f"Required environment variable missing: {full_var}")

        # Load all prefixed variables
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                config_key = key[len(self.prefix):].lower()
                config[config_key] = self._convert_value(value)

        return config

    def _convert_value(self, value):
        """Convert string value to appropriate type."""
        # Boolean conversion
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'

        # Integer conversion
        try:
            return int(value)
        except ValueError:
            pass

        # Float conversion
        try:
            return float(value)
        except ValueError:
            pass

        # String (default)
        return value

# Usage
loader = ConfigLoader(prefix='MYAPP_', required_vars=['DATABASE_URL'])
config = loader.load_config()
print(f"Database URL: {config.get('database_url')}")
print(f"Debug mode: {config.get('debug', False)}")
```

### 5. Temporary Environment Context Manager
**Problem:** Create a context manager that temporarily sets environment variables and restores them afterward.

**Requirements:**
- Set multiple variables temporarily
- Restore original values when exiting
- Handle variables that didn't exist originally

**Solution:**
```python
import os
from contextlib import contextmanager

@contextmanager
def temp_env_vars(**kwargs):
    """
    Temporarily set environment variables.

    Usage:
        with temp_env_vars(DEBUG='true', LOG_LEVEL='INFO'):
            # Code here runs with modified environment
            pass
        # Environment automatically restored
    """
    # Save original values
    originals = {}
    for key, value in kwargs.items():
        originals[key] = os.environ.get(key)

    # Set new values
    for key, value in kwargs.items():
        os.environ[key] = str(value)

    try:
        yield
    finally:
        # Restore original values
        for key, original_value in originals.items():
            if original_value is None:
                # Variable didn't exist originally
                os.environ.pop(key, None)
            else:
                # Restore original value
                os.environ[key] = original_value

# Usage
print(f"Original DEBUG: {os.environ.get('DEBUG', 'not set')}")
print(f"Original LOG_LEVEL: {os.environ.get('LOG_LEVEL', 'not set')}")

with temp_env_vars(DEBUG='true', LOG_LEVEL='DEBUG'):
    print(f"Inside context - DEBUG: {os.environ.get('DEBUG')}")
    print(f"Inside context - LOG_LEVEL: {os.environ.get('LOG_LEVEL')}")
    # Run code with modified environment

print(f"After context - DEBUG: {os.environ.get('DEBUG', 'not set')}")
print(f"After context - LOG_LEVEL: {os.environ.get('LOG_LEVEL', 'not set')}")
```

## System Commands

### 6. Safe Command Executor
**Problem:** Implement a safe command executor that prevents injection attacks and provides proper error handling.

**Requirements:**
- Prevent shell injection
- Handle timeouts
- Capture output and errors
- Return structured results

**Solution:**
```python
import os
import subprocess
import shlex
from typing import Optional, Tuple

class SafeCommandExecutor:
    """Execute system commands safely."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def execute(self, command: str, **kwargs) -> Tuple[int, str, str]:
        """
        Execute a command safely.

        Args:
            command (str): Command to execute
            **kwargs: Additional arguments for subprocess.run

        Returns:
            tuple: (return_code, stdout, stderr)
        """
        try:
            # Parse command safely
            if isinstance(command, str):
                args = shlex.split(command)
            else:
                args = command

            # Execute command
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                **kwargs
            )

            return result.returncode, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return -1, "", f"Command timed out after {self.timeout} seconds"
        except FileNotFoundError:
            return -1, "", f"Command not found: {command}"
        except Exception as e:
            return -1, "", str(e)

    def is_command_available(self, command: str) -> bool:
        """
        Check if a command is available.

        Args:
            command (str): Command to check

        Returns:
            bool: True if available
        """
        try:
            result = subprocess.run(
                [command, '--version'] if os.name != 'nt' else [command],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

# Usage
executor = SafeCommandExecutor(timeout=10)

# Safe command execution
return_code, stdout, stderr = executor.execute('ls -la')
if return_code == 0:
    print("Command succeeded:")
    print(stdout)
else:
    print(f"Command failed: {stderr}")

# Check command availability
if executor.is_command_available('python'):
    print("Python is available")
else:
    print("Python is not available")
```

### 7. Cross-Platform Path Handler
**Problem:** Create a class that handles file paths in a cross-platform manner.

**Requirements:**
- Abstract platform differences
- Provide common operations
- Handle edge cases

**Solution:**
```python
import os
from typing import List

class CrossPlatformPath:
    """Handle file paths in a cross-platform manner."""

    def __init__(self, *path_components):
        """Initialize with path components."""
        self.path = os.path.join(*path_components) if path_components else ''

    @property
    def separator(self) -> str:
        """Get platform-specific path separator."""
        return os.sep

    @property
    def path_separator(self) -> str:
        """Get platform-specific path list separator."""
        return os.pathsep

    def join(self, *components) -> 'CrossPlatformPath':
        """Join path components."""
        new_path = os.path.join(self.path, *components)
        return CrossPlatformPath._from_path(new_path)

    def normalize(self) -> 'CrossPlatformPath':
        """Normalize the path."""
        return CrossPlatformPath._from_path(os.path.normpath(self.path))

    def absolute(self) -> 'CrossPlatformPath':
        """Get absolute path."""
        return CrossPlatformPath._from_path(os.path.abspath(self.path))

    def exists(self) -> bool:
        """Check if path exists."""
        return os.path.exists(self.path)

    def is_file(self) -> bool:
        """Check if path is a file."""
        return os.path.isfile(self.path)

    def is_dir(self) -> bool:
        """Check if path is a directory."""
        return os.path.isdir(self.path)

    def get_size(self) -> int:
        """Get file size in bytes."""
        return os.path.getsize(self.path)

    def get_parent(self) -> 'CrossPlatformPath':
        """Get parent directory."""
        return CrossPlatformPath._from_path(os.path.dirname(self.path))

    def get_name(self) -> str:
        """Get filename or directory name."""
        return os.path.basename(self.path)

    def split_extension(self) -> tuple:
        """Split path into root and extension."""
        return os.path.splitext(self.path)

    @classmethod
    def _from_path(cls, path: str) -> 'CrossPlatformPath':
        """Create instance from path string."""
        instance = cls()
        instance.path = path
        return instance

    @classmethod
    def home(cls) -> 'CrossPlatformPath':
        """Get user's home directory."""
        return cls._from_path(os.path.expanduser('~'))

    @classmethod
    def current_dir(cls) -> 'CrossPlatformPath':
        """Get current working directory."""
        return cls._from_path(os.getcwd())

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return f"CrossPlatformPath('{self.path}')"

# Usage
# Create paths
config_path = CrossPlatformPath('app', 'config', 'settings.json')
home_config = CrossPlatformPath.home().join('.myapp', 'config')

print(f"Config path: {config_path}")
print(f"Home config: {home_config}")
print(f"Separator: {CrossPlatformPath().separator}")
print(f"Path separator: {CrossPlatformPath().path_separator}")

# Path operations
abs_path = config_path.absolute()
print(f"Absolute: {abs_path}")

normalized = config_path.join('..', 'data').normalize()
print(f"Normalized: {normalized}")
```

### 8. Directory Tree Analyzer
**Problem:** Analyze a directory tree and provide statistics about files and subdirectories.

**Requirements:**
- Count files by type
- Calculate total sizes
- Find largest and oldest files
- Handle permission errors

**Solution:**
```python
import os
from collections import defaultdict
from datetime import datetime

class DirectoryAnalyzer:
    """Analyze directory trees and provide statistics."""

    def __init__(self, root_path: str):
        self.root_path = os.path.abspath(root_path)
        if not os.path.exists(self.root_path):
            raise FileNotFoundError(f"Path does not exist: {self.root_path}")

    def analyze(self) -> dict:
        """
        Analyze the directory tree.

        Returns:
            dict: Analysis results
        """
        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'file_types': defaultdict(int),
            'size_by_type': defaultdict(int),
            'largest_files': [],
            'oldest_files': [],
            'newest_files': [],
            'errors': []
        }

        for root, dirs, files in os.walk(self.root_path):
            stats['total_dirs'] += 1

            for file in files:
                try:
                    filepath = os.path.join(root, file)
                    stat_info = os.stat(filepath)

                    stats['total_files'] += 1
                    stats['total_size'] += stat_info.st_size

                    # File type analysis
                    _, ext = os.path.splitext(file)
                    ext = ext.lower() if ext else 'no_extension'
                    stats['file_types'][ext] += 1
                    stats['size_by_type'][ext] += stat_info.st_size

                    # Track largest files
                    file_info = {
                        'path': filepath,
                        'size': stat_info.st_size,
                        'modified': datetime.fromtimestamp(stat_info.st_mtime)
                    }

                    stats['largest_files'].append(file_info)
                    stats['oldest_files'].append(file_info)
                    stats['newest_files'].append(file_info)

                except (OSError, PermissionError) as e:
                    stats['errors'].append(f"Error processing {filepath}: {e}")
                    continue

        # Sort and limit results
        stats['largest_files'].sort(key=lambda x: x['size'], reverse=True)
        stats['largest_files'] = stats['largest_files'][:10]

        stats['oldest_files'].sort(key=lambda x: x['modified'])
        stats['oldest_files'] = stats['oldest_files'][:10]

        stats['newest_files'].sort(key=lambda x: x['modified'], reverse=True)
        stats['newest_files'] = stats['newest_files'][:10]

        # Convert defaultdicts to regular dicts
        stats['file_types'] = dict(stats['file_types'])
        stats['size_by_type'] = dict(stats['size_by_type'])

        return stats

    def print_report(self, stats: dict):
        """Print a formatted analysis report."""
        print("=== Directory Analysis Report ===")
        print(f"Root Path: {self.root_path}")
        print(f"Total Files: {stats['total_files']:,}")
        print(f"Total Directories: {stats['total_dirs']:,}")
        print(f"Total Size: {stats['total_size'] / (1024*1024):.2f} MB")
        print()

        print("File Types:")
        for ext, count in sorted(stats['file_types'].items(),
                                key=lambda x: x[1], reverse=True):
            size_mb = stats['size_by_type'][ext] / (1024*1024)
            print(f"  {ext}: {count:,} files ({size_mb:.2f} MB)")
        print()

        if stats['largest_files']:
            print("Largest Files:")
            for file_info in stats['largest_files'][:5]:
                size_mb = file_info['size'] / (1024*1024)
                print(f"  {file_info['path']} ({size_mb:.2f} MB)")
        print()

        if stats['errors']:
            print(f"Errors Encountered: {len(stats['errors'])}")
            for error in stats['errors'][:3]:
                print(f"  {error}")
            if len(stats['errors']) > 3:
                print(f"  ... and {len(stats['errors']) - 3} more")

# Usage
analyzer = DirectoryAnalyzer('/path/to/analyze')
stats = analyzer.analyze()
analyzer.print_report(stats)
```

These coding problems demonstrate practical usage of the `os` module in real-world scenarios, covering file system operations, environment management, system commands, and cross-platform compatibility.
