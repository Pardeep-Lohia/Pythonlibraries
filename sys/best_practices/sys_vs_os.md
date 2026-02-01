# `sys` vs `os` - When to Use Which Module

Understanding the distinction between the `sys` and `os` modules is crucial for effective Python programming. While both provide system-level functionality, they serve different purposes and operate at different levels of abstraction.

## Core Differences

### `sys` Module
- **Focus:** Python interpreter and runtime environment
- **Abstraction Level:** High-level interpreter interface
- **Primary Use:** Interpreter control, I/O streams, runtime inspection
- **Cross-platform:** Consistent across all Python implementations

### `os` Module
- **Focus:** Operating system interface
- **Abstraction Level:** System calls and OS-specific operations
- **Primary Use:** File system operations, process management, environment variables
- **Cross-platform:** Provides platform-specific implementations

## When to Use `sys`

### ✅ Command-Line Interface Development
```python
import sys

# Access command-line arguments
script_name = sys.argv[0]
input_file = sys.argv[1] if len(sys.argv) > 1 else None

# Exit with status codes
if not input_file:
    sys.stderr.write("Usage: script.py <input_file>\n")
    sys.exit(1)
```

### ✅ Interpreter Information and Control
```python
import sys

# Check Python version
if sys.version_info < (3, 6):
    sys.exit("Python 3.6+ required")

# Get platform information
print(f"Platform: {sys.platform}")
print(f"Version: {sys.version}")
```

### ✅ Standard I/O Stream Management
```python
import sys

# Redirect output
original_stdout = sys.stdout
with open('output.log', 'w') as f:
    sys.stdout = f
    print("This goes to log file")
sys.stdout = original_stdout
```

### ✅ Runtime Environment Inspection
```python
import sys

# Memory usage monitoring
size = sys.getsizeof(large_object)

# Recursion limit management
sys.setrecursionlimit(2000)

# Module path inspection
print(sys.path)
```

## When to Use `os`

### ✅ File System Operations
```python
import os

# File and directory operations
os.mkdir('new_directory')
os.rename('old_name.txt', 'new_name.txt')
os.remove('file_to_delete.txt')

# Path manipulations
full_path = os.path.join('folder', 'subfolder', 'file.txt')
exists = os.path.exists(full_path)
```

### ✅ Process and System Information
```python
import os

# Process management
pid = os.getpid()
ppid = os.getppid()

# Environment variables
home_dir = os.environ.get('HOME')
path_var = os.environ.get('PATH')
```

### ✅ Directory Navigation
```python
import os

# Current working directory
cwd = os.getcwd()
os.chdir('/new/directory')

# Directory listing
files = os.listdir('.')
```

### ✅ System Commands Execution
```python
import os

# Execute system commands
os.system('ls -la')  # Simple execution
result = os.popen('ls -la').read()  # Capture output

# Using subprocess is preferred for complex operations
import subprocess
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
```

## Complementary Usage Patterns

### 🔄 Environment Variables
```python
import sys
import os

# os: Access system environment variables
user_home = os.environ.get('HOME')  # OS environment
temp_dir = os.environ.get('TMPDIR', '/tmp')

# sys: Python-specific environment inspection
python_path = sys.path  # Python module search path
executable = sys.executable  # Python executable location
```

### 🔄 Path Handling
```python
import sys
import os
from pathlib import Path

# os: OS-specific path operations
full_path = os.path.join('folder', 'file.txt')
normalized = os.path.normpath('./folder/../file.txt')
exists = os.path.exists(full_path)

# sys: Python path management
sys.path.insert(0, '/custom/module/path')  # Add to Python path
sys.path.remove('/custom/module/path')     # Remove from Python path
```

### 🔄 Platform Detection
```python
import sys
import os

# Both can detect platform, but serve different purposes
if sys.platform == 'win32':
    # Python-specific behavior
    line_ending = '\r\n'
elif sys.platform.startswith('linux'):
    # Python-specific behavior
    line_ending = '\n'

if os.name == 'nt':  # Windows
    # OS-specific operations
    dir_sep = '\\'
else:  # Unix-like
    # OS-specific operations
    dir_sep = '/'
```

## Common Scenarios and Best Choices

### Scenario 1: Command-Line Script
```python
#!/usr/bin/env python3
import sys
import os

# Use sys for argument parsing and exit handling
if len(sys.argv) < 2:
    sys.stderr.write(f"Usage: {sys.argv[0]} <file>\n")
    sys.exit(1)

filename = sys.argv[1]

# Use os for file operations
if not os.path.exists(filename):
    sys.stderr.write(f"File not found: {filename}\n")
    sys.exit(1)

# Use sys for output
with open(filename, 'r') as f:
    content = f.read()
    sys.stdout.write(content)
```

### Scenario 2: Cross-Platform Application
```python
import sys
import os

def setup_application():
    # Use sys for Python version check
    if sys.version_info < (3, 6):
        sys.stderr.write("Python 3.6+ required\n")
        sys.exit(1)

    # Use os for platform-specific setup
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(os.environ['APPDATA'], 'myapp')
    else:  # Unix-like
        config_dir = os.path.join(os.environ.get('HOME', '/'), '.config', 'myapp')

    os.makedirs(config_dir, exist_ok=True)
    return config_dir
```

### Scenario 3: Memory and Performance Monitoring
```python
import sys
import os
import psutil

def system_diagnostics():
    # Use sys for Python interpreter info
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Recursion limit: {sys.getrecursionlimit()}")

    # Use os for system resource info
    print(f"Process ID: {os.getpid()}")
    print(f"Current directory: {os.getcwd()}")

    # Use psutil for detailed system info (external library)
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    print(f"Memory usage: {memory_usage} bytes")
```

## Decision Tree: sys vs os

```
Need to work with...?
├── Python interpreter/runtime
│   ├── Command-line arguments → sys.argv
│   ├── Standard I/O streams → sys.stdin/stdout/stderr
│   ├── Version/platform info → sys.version_info, sys.platform
│   ├── Module paths → sys.path
│   └── Exit handling → sys.exit()
│
├── Operating system
│   ├── Files and directories → os.path, os.mkdir, os.listdir
│   ├── Environment variables → os.environ
│   ├── Process management → os.getpid, os.system
│   ├── Current directory → os.getcwd, os.chdir
│   └── System commands → os.system, subprocess
│
└── Both (complementary)
    ├── Platform detection → sys.platform + os.name
    ├── Path operations → os.path + sys.path
    └── Environment → os.environ + sys.path/executable
```

## Anti-Patterns to Avoid

### ❌ Using `os` for Interpreter Control
```python
# DON'T DO THIS
import os
# Trying to exit using os
os._exit(1)  # Unclean exit, doesn't run cleanup

# DO THIS INSTEAD
import sys
sys.exit(1)  # Clean exit with cleanup
```

### ❌ Using `sys` for File System Operations
```python
# DON'T DO THIS
import sys
# Trying to check file existence with sys
if len(sys.path) > 0:  # Wrong approach
    pass

# DO THIS INSTEAD
import os
if os.path.exists('file.txt'):
    pass
```

### ❌ Confusing Platform Detection
```python
# DON'T DO THIS - inconsistent platform checks
import sys
if sys.platform == 'win32':
    separator = '\\'
else:
    separator = '/'

# DO THIS INSTEAD - use os for OS-specific operations
import os
separator = os.sep  # Automatically correct for platform
```

## Summary

**Choose `sys` when you need to:**
- Interact with the Python interpreter
- Handle command-line arguments and program flow
- Manage standard I/O streams
- Inspect runtime environment and version info

**Choose `os` when you need to:**
- Perform file system operations
- Access system environment variables
- Execute system commands
- Manage processes and directories

**Use both when you need:**
- Cross-platform compatibility
- Comprehensive system introspection
- Complex applications requiring both interpreter and OS interaction

Remember: `sys` is about Python's world, `os` is about the system's world. Understanding this distinction leads to cleaner, more maintainable code.
