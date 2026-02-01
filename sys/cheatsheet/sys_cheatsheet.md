# Python `sys` Module Cheatsheet

## Command Line Arguments
```python
import sys

# Access command line arguments
script_name = sys.argv[0]        # Script name/path
first_arg = sys.argv[1]          # First argument
all_args = sys.argv[1:]          # All arguments except script name
num_args = len(sys.argv) - 1     # Number of arguments

# Safe argument access
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    sys.exit("Usage: script.py <filename>")
```

## Version Information
```python
import sys

# Version as string
version_str = sys.version                    # "3.9.7 (default, Sep 16 2021, 13:09:58) [GCC 7.5.0]"

# Version as tuple (recommended)
vi = sys.version_info                         # sys.version_info(major=3, minor=9, micro=7, releaselevel='final', serial=0)
major = vi.major                              # 3
minor = vi.minor                              # 9

# Version checking
if sys.version_info >= (3, 8):                # Python 3.8+
    # Use new features
    pass

# Other version info
api_version = sys.api_version                 # C API version
hex_version = sys.hexversion                  # Version as hex number
```

## Platform Information
```python
import sys

platform = sys.platform                        # 'win32', 'linux', 'darwin', 'cygwin'
byteorder = sys.byteorder                      # 'little' or 'big'
maxsize = sys.maxsize                          # Max integer size (determines 32/64-bit)

# Architecture check
is_64bit = sys.maxsize > 2**32
```

## Paths and Locations
```python
import sys

executable = sys.executable                    # Python executable path
prefix = sys.prefix                            # Installation prefix
base_prefix = sys.base_prefix                  # Base prefix (system Python in venv)
exec_prefix = sys.exec_prefix                  # Execution prefix

# Virtual environment detection
in_venv = sys.prefix != sys.base_prefix

# Module search paths
paths = sys.path                               # List of module search directories
sys.path.insert(0, '/custom/path')             # Add custom path
sys.path.remove('/custom/path')                # Remove path
```

## Standard I/O Streams
```python
import sys

# Standard streams
stdin = sys.stdin                              # Standard input
stdout = sys.stdout                            # Standard output
stderr = sys.stderr                            # Standard error

# Basic I/O
line = sys.stdin.readline()                    # Read line from stdin
sys.stdout.write("Hello\n")                    # Write to stdout
sys.stderr.write("Error\n")                    # Write to stderr

# Flushing (important for prompts)
sys.stdout.write("Enter name: ")
sys.stdout.flush()
name = sys.stdin.readline().strip()
```

## Stream Redirection
```python
import sys
from contextlib import redirect_stdout, redirect_stderr

# Temporary redirection
with open('output.log', 'w') as f:
    sys.stdout = f
    print("This goes to file")
sys.stdout = sys.__stdout__                    # Restore

# Using contextlib
with redirect_stdout(open('out.log', 'w')):
    print("Redirected output")

with redirect_stderr(open('err.log', 'w')):
    print("Redirected error", file=sys.stderr)
```

## Module System
```python
import sys

# Loaded modules
modules = sys.modules                          # Dict of loaded modules
num_modules = len(sys.modules)                 # Number of loaded modules

# Check if module is loaded
if 'json' in sys.modules:
    json_module = sys.modules['json']

# Module search customization
sys.path_hooks                                # List of path hook callables
sys.meta_path                                 # List of meta path finder objects
```

## Runtime Control
```python
import sys

# Program exit
sys.exit(0)                                   # Success exit
sys.exit(1)                                   # Error exit
sys.exit("Error message")                     # Exit with message

# Recursion control
current_limit = sys.getrecursionlimit()       # Get current limit (usually 1000)
sys.setrecursionlimit(2000)                   # Set new limit

# Restore original limit
original_limit = sys.getrecursionlimit()
sys.setrecursionlimit(5000)
try:
    # Deep recursion code
    pass
finally:
    sys.setrecursionlimit(original_limit)
```

## Memory Analysis
```python
import sys

# Object size
size = sys.getsizeof(obj)                     # Size in bytes (shallow)
ref_count = sys.getrefcount(obj) - 1          # Reference count (subtract 1)

# Deep size calculation
def get_deep_size(obj, seen=None):
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    size = sys.getsizeof(obj)
    if isinstance(obj, (list, tuple)):
        size += sum(get_deep_size(item, seen) for item in obj)
    elif isinstance(obj, dict):
        size += sum(get_deep_size(k, seen) + get_deep_size(v, seen) for k, v in obj.items())
    return size
```

## Exception Handling
```python
import sys

# Current exception info (only in except blocks)
try:
    1 / 0
except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(f"Exception: {exc_type.__name__}: {exc_value}")

# Custom exception hook
def custom_hook(exc_type, exc_value, exc_traceback):
    print(f"Uncaught: {exc_type.__name__}: {exc_value}")
    # Log to file, send to monitoring, etc.
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = custom_hook

# Unraisable exception hook (Python 3.8+)
def unraisable_hook(unraisable):
    print(f"Unraisable: {unraisable.exception}")
    print(f"Error: {unraisable.err_msg}")

sys.unraisablehook = unraisable_hook
```

## Debugging and Introspection
```python
import sys

# Current frame
frame = sys._getframe()                        # Current stack frame
print(f"Current function: {frame.f_code.co_name}")
print(f"Current file: {frame.f_code.co_filename}")

# All thread frames
frames = sys._current_frames()                 # Dict of thread_id -> frame

# Call tracing
def trace_calls(frame, event, arg):
    if event == 'call':
        print(f"Calling: {frame.f_code.co_name}")
    return trace_calls

sys.settrace(trace_calls)                      # Enable tracing
```

## Common Patterns

### Version-Aware Code
```python
import sys

if sys.version_info >= (3, 8):
    # Use walrus operator :=
    if (n := len(data)) > 0:
        process(data)
elif sys.version_info >= (3, 6):
    # Use f-strings
    print(f"Processed {len(data)} items")
else:
    # Fallback for older versions
    print("Processed {} items".format(len(data)))
```

### Cross-Platform Code
```python
import sys
import os

# Platform-specific operations
if sys.platform == 'win32':
    path_sep = '\\'
    home = os.environ.get('USERPROFILE')
elif sys.platform == 'darwin':
    path_sep = '/'
    home = os.environ.get('HOME')
else:  # Linux and others
    path_sep = '/'
    home = os.environ.get('HOME')
```

### Safe Argument Parsing
```python
import sys

def get_arg(index, default=None, convert=str):
    """Safely get command line argument with conversion"""
    try:
        return convert(sys.argv[index])
    except (IndexError, ValueError):
        return default

# Usage
input_file = get_arg(1, 'default.txt', str)
count = get_arg(2, 10, int)
verbose = get_arg(3, False, lambda x: x.lower() in ('true', '1', 'yes'))
```

### Memory Monitoring
```python
import sys
import tracemalloc

# Start memory tracing
tracemalloc.start()

# Your code here
data = [i for i in range(100000)]

# Get memory usage
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024:.1f} KB")
print(f"Peak: {peak / 1024:.1f} KB")

# Get top memory users
stats = tracemalloc.get_traced_memory()
top_stats = tracemalloc.take_snapshot().statistics('lineno')
for stat in top_stats[:5]:
    print(f"{stat.size / 1024:.1f} KB: {stat.traceback.format()[-1]}")

tracemalloc.stop()
```

### Graceful Shutdown
```python
import sys
import atexit
import signal

class GracefulShutdown:
    def __init__(self):
        self.shutdown = False
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        print(f"\nReceived signal {signum}, shutting down...")
        self.shutdown = True
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        print("Performing cleanup...")
        # Close files, save state, etc.

# Usage
shutdown = GracefulShutdown()

while not shutdown.shutdown:
    # Main application loop
    pass
```

## Quick Reference

### Most Used Functions
- `sys.argv` - Command line arguments
- `sys.version_info` - Python version (tuple)
- `sys.platform` - Platform identifier
- `sys.path` - Module search paths
- `sys.exit()` - Exit program
- `sys.getsizeof()` - Object size in bytes

### Most Used Attributes
- `sys.stdin` - Standard input
- `sys.stdout` - Standard output
- `sys.stderr` - Standard error
- `sys.modules` - Loaded modules dict
- `sys.executable` - Python executable path
- `sys.prefix` - Installation prefix

### Common Checks
```python
# Python version checks
sys.version_info >= (3, 8)                     # 3.8 or higher
sys.version_info < (3, 7)                      # Older than 3.7

# Platform checks
sys.platform == 'win32'                        # Windows
sys.platform == 'darwin'                       # macOS
sys.platform.startswith('linux')               # Linux

# Architecture checks
sys.maxsize > 2**32                            # 64-bit Python

# Virtual environment
sys.prefix != sys.base_prefix                   # In virtual env
```

### Error Exit Codes
```python
sys.exit(0)                                    # Success
sys.exit(1)                                    # General error
sys.exit(2)                                    # Command line syntax error
sys.exit(130)                                  # Script terminated by Ctrl+C
```

This cheatsheet covers the most commonly used `sys` module features. For complete documentation, refer to the official Python documentation.
