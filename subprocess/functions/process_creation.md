# Process Creation with Subprocess

## Overview

Process creation is at the heart of the `subprocess` module. This document covers how to spawn new processes, manage their execution context, and handle the parent-child relationship between Python scripts and external commands.

## Synchronous Process Creation

### subprocess.run() - High-Level Process Creation

`subprocess.run()` is the recommended function for most process creation needs. It creates a child process, waits for completion, and returns a `CompletedProcess` instance.

#### Basic Syntax
```python
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None,
               capture_output=False, shell=False, cwd=None, timeout=None,
               check=False, encoding=None, errors=None, text=None,
               env=None, universal_newlines=None)
```

#### Parameters
- **args**: Command and arguments (list or string)
- **stdin/stdout/stderr**: Standard stream handling
- **capture_output**: Capture both stdout and stderr
- **shell**: Execute through shell
- **cwd**: Working directory for child process
- **timeout**: Maximum execution time
- **check**: Raise exception on non-zero exit
- **encoding/text**: Text mode handling
- **env**: Environment variables

#### Examples

**Simple Process Creation**
```python
import subprocess

# Create and run a process
result = subprocess.run(['echo', 'Hello World'])
print(f"Process completed with return code: {result.returncode}")
```

**Process with Custom Environment**
```python
import os

# Create process with modified environment
env = os.environ.copy()
env['CUSTOM_VAR'] = 'Hello from subprocess'

result = subprocess.run(['env'], env=env, capture_output=True, text=True)
print(result.stdout)
```

**Process in Different Working Directory**
```python
# Run process in specific directory
result = subprocess.run(['pwd'], cwd='/tmp', capture_output=True, text=True)
print(f"Working directory: {result.stdout.strip()}")
```

## Asynchronous Process Creation

### subprocess.Popen() - Low-Level Process Creation

`subprocess.Popen()` provides fine-grained control over process creation and management. It returns immediately, allowing the parent to continue execution while the child runs.

#### Basic Syntax
```python
subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None,
                 stderr=None, preexec_fn=None, close_fds=True, shell=False,
                 cwd=None, env=None, universal_newlines=None,
                 startupinfo=None, creationflags=0, restore_signals=True,
                 start_new_session=False, pass_fds=(), encoding=None,
                 errors=None, text=None)
```

#### Key Methods
- **communicate()**: Interact with process I/O
- **poll()**: Check if process has terminated
- **wait()**: Wait for process completion
- **terminate()**: Send SIGTERM signal
- **kill()**: Send SIGKILL signal

#### Examples

**Basic Asynchronous Execution**
```python
# Create process without waiting
process = subprocess.Popen(['sleep', '5'])
print(f"Process started with PID: {process.pid}")

# Do other work while process runs
import time
time.sleep(2)

# Check if still running
if process.poll() is None:
    print("Process is still running")
else:
    print(f"Process finished with code: {process.returncode}")
```

**Process with I/O Communication**
```python
# Create process with pipes for communication
process = subprocess.Popen(['python3', '-c', 'print(input("Enter: "))'],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          text=True)

# Send input and get output
stdout, stderr = process.communicate(input='Hello World\n')
print(f"Output: {stdout.strip()}")

# Wait for completion
process.wait()
```

## Process Context Management

### Environment Variables

Child processes inherit the parent's environment but can be modified:

```python
import os

# Inherit and modify environment
env = os.environ.copy()
env['PATH'] = '/custom/path:' + env.get('PATH', '')
env['MY_VAR'] = 'custom_value'

process = subprocess.run(['env'], env=env, capture_output=True, text=True)
```

### Working Directory

Control where the child process executes:

```python
import os

# Run in different directory
original_cwd = os.getcwd()
try:
    process = subprocess.run(['pwd'], cwd='/tmp', capture_output=True, text=True)
    print(f"Process ran in: {process.stdout.strip()}")
finally:
    os.chdir(original_cwd)  # Restore original directory
```

### User and Group Context (Unix)

Change the user/group context for security:

```python
import os
import pwd
import grp

def run_as_user(username, command):
    """Run command as different user (requires root privileges)"""
    try:
        user_info = pwd.getpwnam(username)
        group_info = grp.getgrgid(user_info.pw_gid)

        def preexec():
            os.setgid(user_info.pw_gid)
            os.setuid(user_info.pw_uid)

        return subprocess.run(command, preexec_fn=preexec)

    except PermissionError:
        print("Insufficient privileges to change user context")
    except KeyError:
        print(f"User {username} not found")
```

## Process Groups and Sessions

### Process Group Management

Organize related processes into groups for collective management:

```python
# Create process in new group (Unix)
process = subprocess.Popen(['command'],
                          start_new_session=True)  # Creates new process group

print(f"Process group: {os.getpgid(process.pid)}")
```

### Session Management

Create new sessions to isolate process groups:

```python
# Start process as session leader
process = subprocess.Popen(['command'],
                          start_new_session=True)

# Process is now session leader
print(f"Session ID: {os.getsid(process.pid)}")
```

## File Descriptor Management

### File Descriptor Inheritance

Control which file descriptors are inherited by child processes:

```python
# Close all file descriptors except stdin/stdout/stderr
process = subprocess.Popen(['command'], close_fds=True)

# Inherit specific file descriptors
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    process = subprocess.Popen(['command'],
                              stdin=infile,
                              stdout=outfile,
                              pass_fds=[infile.fileno(), outfile.fileno()])
```

### Standard Stream Redirection

Redirect standard streams to files or other processes:

```python
# Redirect stdout to file
with open('output.log', 'w') as logfile:
    process = subprocess.run(['command'], stdout=logfile)

# Redirect stderr to stdout
process = subprocess.run(['command'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
```

## Cross-Platform Process Creation

### Platform-Specific Considerations

Handle differences between operating systems:

```python
import platform

def run_ls_command():
    """Cross-platform directory listing"""
    system = platform.system()

    if system == 'Windows':
        return subprocess.run(['cmd', '/c', 'dir'],
                             capture_output=True, text=True)
    elif system == 'Darwin':  # macOS
        return subprocess.run(['ls', '-la'],
                             capture_output=True, text=True)
    else:  # Linux and other Unix-like
        return subprocess.run(['ls', '--color=auto', '-la'],
                             capture_output=True, text=True)
```

### Windows-Specific Options

Use Windows-specific creation flags:

```python
import subprocess

if platform.system() == 'Windows':
    # Create process in new console window
    creationflags = subprocess.CREATE_NEW_CONSOLE
    process = subprocess.Popen(['notepad.exe'],
                              creationflags=creationflags)
```

### Unix-Specific Options

Leverage Unix process management features:

```python
# Set process priority (Unix)
def run_with_nice_priority(command, priority=10):
    def preexec():
        os.nice(priority)

    return subprocess.Popen(command, preexec_fn=preexec)
```

## Resource Management

### CPU and Memory Limits

Set resource constraints for child processes:

```python
import resource

def run_with_limits(command, cpu_limit=10, mem_limit=50*1024*1024):
    """Run command with resource limits"""

    def preexec():
        # CPU time limit (seconds)
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))

        # Memory limit (bytes)
        resource.setrlimit(resource.RLIMIT_AS, (mem_limit, mem_limit))

    return subprocess.Popen(command, preexec_fn=preexec)
```

### Process Monitoring

Track process resource usage:

```python
import psutil
import time

def monitor_process(process, duration=10):
    """Monitor process resource usage"""
    pid = process.pid

    for _ in range(duration):
        try:
            proc = psutil.Process(pid)
            cpu_percent = proc.cpu_percent()
            memory_info = proc.memory_info()

            print(f"CPU: {cpu_percent}%, Memory: {memory_info.rss} bytes")
            time.sleep(1)

        except psutil.NoSuchProcess:
            print("Process has terminated")
            break
```

## Error Handling in Process Creation

### Common Creation Errors

Handle various failure scenarios:

```python
def safe_process_creation(command):
    """Safely create a process with comprehensive error handling"""
    try:
        # Validate command
        if not command or not isinstance(command, list):
            raise ValueError("Invalid command format")

        # Check if executable exists
        if not shutil.which(command[0]):
            raise FileNotFoundError(f"Command not found: {command[0]}")

        # Create process
        process = subprocess.Popen(command,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

        return process

    except FileNotFoundError as e:
        print(f"Command not found: {e}")
    except PermissionError:
        print("Permission denied")
    except OSError as e:
        print(f"OS error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None
```

### Timeout Handling

Prevent processes from running indefinitely:

```python
def run_with_timeout(command, timeout=30):
    """Run command with timeout protection"""
    try:
        result = subprocess.run(command,
                               timeout=timeout,
                               capture_output=True,
                               text=True)
        return result

    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds")
        return None
```

## Advanced Process Creation Patterns

### Process Pools

Create multiple processes concurrently:

```python
from concurrent.futures import ThreadPoolExecutor
import subprocess

def run_commands_parallel(commands, max_workers=4):
    """Run multiple commands in parallel"""

    def run_single_command(cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {
                'command': cmd,
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'output': result.stdout,
                'error': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {'command': cmd, 'success': False, 'error': 'Timeout'}
        except Exception as e:
            return {'command': cmd, 'success': False, 'error': str(e)}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(run_single_command, commands))

    return results
```

### Process Factories

Create reusable process configurations:

```python
class ProcessFactory:
    """Factory for creating configured processes"""

    def __init__(self, base_env=None, base_cwd=None):
        self.base_env = base_env or os.environ.copy()
        self.base_cwd = base_cwd

    def create_process(self, command, **kwargs):
        """Create a process with base configuration"""
        config = {
            'env': self.base_env.copy(),
            'cwd': self.base_cwd,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'text': True
        }
        config.update(kwargs)

        return subprocess.Popen(command, **config)

# Usage
factory = ProcessFactory(base_cwd='/tmp')
process = factory.create_process(['ls', '-la'])
```

### Context Managers for Processes

Ensure proper cleanup with context managers:

```python
class ManagedProcess:
    """Context manager for subprocess management"""

    def __init__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        self.process = None

    def __enter__(self):
        self.process = subprocess.Popen(self.command, **self.kwargs)
        return self.process

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

# Usage
with ManagedProcess(['long_running_command']) as proc:
    # Process runs here
    output = proc.communicate(timeout=60)
# Process automatically cleaned up
```

## Security Considerations

### Input Validation

Always validate inputs to prevent security issues:

```python
import shlex

def safe_command_execution(user_input):
    """Safely execute user-provided commands"""

    # Validate input format
    if not isinstance(user_input, str) or len(user_input) > 1000:
        raise ValueError("Invalid input")

    # Parse safely (if allowing shell-like syntax)
    try:
        parsed = shlex.split(user_input)
    except ValueError:
        raise ValueError("Invalid command syntax")

    # Whitelist allowed commands
    allowed_commands = {'ls', 'pwd', 'echo', 'cat', 'head', 'tail'}
    if parsed[0] not in allowed_commands:
        raise ValueError("Command not allowed")

    return subprocess.run(parsed, capture_output=True, text=True)
```

### Environment Sanitization

Clean environment variables for security:

```python
def sanitize_environment():
    """Create a safe environment for subprocess execution"""
    safe_env = {}

    # Copy only safe variables
    safe_vars = {'PATH', 'HOME', 'USER', 'SHELL', 'LANG', 'LC_ALL'}

    for var in safe_vars:
        value = os.environ.get(var)
        if value:
            safe_env[var] = value

    # Set secure PATH
    safe_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'

    return safe_env

# Use sanitized environment
safe_env = sanitize_environment()
process = subprocess.run(['command'], env=safe_env)
```

This comprehensive guide covers all aspects of process creation with `subprocess`, from basic synchronous execution to advanced asynchronous patterns, resource management, and security considerations.
