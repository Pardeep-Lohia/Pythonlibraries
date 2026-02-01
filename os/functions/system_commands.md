# System Commands

## Overview
The `os` module provides functions to execute system commands and interact with the operating system shell. These functions allow Python programs to run external commands, capture output, and handle process execution.

## Core System Command Functions

### `os.system(command)` - Execute System Command
**Purpose**: Executes a command in a subshell.

**Syntax**:
```python
os.system(command)
```

**Parameters**:
- `command`: Command string to execute

**Return Value**: Exit code of the command (0 for success, non-zero for failure)

**Examples**:
```python
import os

# Simple command execution
exit_code = os.system('echo "Hello, World!"')

# Check result
if exit_code == 0:
    print("Command executed successfully")
else:
    print(f"Command failed with exit code: {exit_code}")

# Platform-specific commands
if os.name == 'nt':  # Windows
    os.system('dir')
else:  # Unix-like
    os.system('ls -la')
```

**Limitations**:
- No access to command output
- No input to command
- Synchronous execution only
- Security risks (shell injection)

### `os.popen(command, mode='r')` - Open Pipe to Command
**Purpose**: Opens a pipe to or from a command.

**Syntax**:
```python
os.popen(command, mode='r')
```

**Parameters**:
- `command`: Command to execute
- `mode`: File mode ('r' for reading, 'w' for writing)

**Return Value**: File-like object connected to command's stdin/stdout

**Examples**:
```python
import os

# Read command output
with os.popen('ls -la', 'r') as pipe:
    output = pipe.read()
    print(output)

# Write to command input
with os.popen('sort', 'w') as pipe:
    pipe.write('banana\napple\ncherry\n')

# Get command exit code
pipe = os.popen('echo "test"', 'r')
output = pipe.read()
exit_code = pipe.close()  # Returns exit code or None
```

**Note**: Deprecated in favor of `subprocess` module.

### `os.spawn*` Functions - Process Spawning
**Purpose**: Create child processes with various execution modes.

**Functions**:
- `os.spawnl(mode, path, arg0, arg1, ...)`: Argument list
- `os.spawnle(mode, path, arg0, arg1, ..., env)`: With environment
- `os.spawnlp(mode, file, arg0, arg1, ...)`: Search in PATH
- `os.spawnlpe(mode, file, arg0, arg1, ..., env)`: Search in PATH with environment
- `os.spawnv(mode, path, args)`: Argument vector
- `os.spawnve(mode, path, args, env)`: With environment
- `os.spawnvp(mode, file, args)`: Search in PATH
- `os.spawnvp(mode, file, args, env)`: Search in PATH with environment

**Mode Parameters**:
- `os.P_WAIT`: Wait for child to terminate
- `os.P_NOWAIT` / `os.P_NOWAITO`: Don't wait
- `os.P_DETACH`: Detached child
- `os.P_OVERLAY`: Replace current process

**Example**:
```python
import os

# Spawn process and wait
pid = os.spawnlp(os.P_WAIT, 'ls', 'ls', '-la')
print(f"Command completed, PID was: {pid}")

# Spawn detached process
pid = os.spawnlp(os.P_DETACH, 'python', 'python', 'script.py')
print(f"Detached process started with PID: {pid}")
```

## Process Management

### `os.fork()` - Create Child Process
**Purpose**: Creates a child process by duplicating the current process.

**Syntax**:
```python
os.fork()
```

**Return Value**:
- In parent: Child process ID
- In child: 0

**Example**:
```python
import os
import time

pid = os.fork()

if pid == 0:
    # Child process
    print("Child process executing")
    time.sleep(1)
    print("Child process done")
    os._exit(0)
else:
    # Parent process
    print(f"Parent process, child PID: {pid}")
    os.waitpid(pid, 0)
    print("Parent process done")
```

**Note**: Unix only, not available on Windows.

### `os.exec*` Functions - Replace Process Image
**Purpose**: Replace current process with a new program.

**Functions**:
- `os.execl(path, arg0, arg1, ...)`: Argument list
- `os.execle(path, arg0, arg1, ..., env)`: With environment
- `os.execlp(file, arg0, arg1, ...)`: Search in PATH
- `os.execlpe(file, arg0, arg1, ..., env)`: Search in PATH with environment
- `os.execv(path, args)`: Argument vector
- `os.execve(path, args, env)`: With environment
- `os.execvp(file, args)`: Search in PATH
- `os.execvpe(file, args, env)`: Search in PATH with environment

**Example**:
```python
import os

# Replace current process with new program
os.execlp('python', 'python', 'script.py', 'arg1', 'arg2')

# This line never executes
print("This won't print")
```

### `os.waitpid(pid, options)` - Wait for Process
**Purpose**: Wait for a child process to change state.

**Syntax**:
```python
os.waitpid(pid, options)
```

**Parameters**:
- `pid`: Process ID to wait for (-1 for any child)
- `options`: Wait options (0 for blocking, os.WNOHANG for non-blocking)

**Return Value**: Tuple of (pid, status)

**Example**:
```python
import os

pid = os.fork()
if pid == 0:
    # Child
    os.execlp('sleep', 'sleep', '2')
else:
    # Parent
    child_pid, status = os.waitpid(pid, 0)
    print(f"Child {child_pid} exited with status {status}")
```

## System Information

### `os.name` - Operating System Name
**Purpose**: String identifying the operating system.

**Values**:
- `'posix'`: Unix-like systems (Linux, macOS, BSD)
- `'nt'`: Windows
- `'java'`: Jython

**Example**:
```python
import os

if os.name == 'nt':
    print("Running on Windows")
elif os.name == 'posix':
    print("Running on Unix-like system")
```

### `os.uname()` - System Information
**Purpose**: Returns system information.

**Return Value**: Named tuple with:
- `sysname`: OS name
- `nodename`: Network name
- `release`: OS release
- `version`: OS version
- `machine`: Hardware identifier

**Example**:
```python
import os

info = os.uname()
print(f"System: {info.sysname}")
print(f"Node: {info.nodename}")
print(f"Release: {info.release}")
print(f"Version: {info.version}")
print(f"Machine: {info.machine}")
```

**Note**: Not available on Windows.

### `os.getpid()` - Get Process ID
**Purpose**: Returns the current process ID.

**Syntax**:
```python
os.getpid()
```

### `os.getppid()` - Get Parent Process ID
**Purpose**: Returns the parent process ID.

**Syntax**:
```python
os.getppid()
```

## Security Considerations

### Command Injection Prevention
```python
import os
import subprocess

# Vulnerable to command injection
filename = input("Enter filename: ")
os.system(f"rm {filename}")  # Dangerous!

# Safe alternatives
filename = input("Enter filename: ")

# Option 1: Validate input
if '/' not in filename and '\\' not in filename:
    os.system(f"rm {filename}")
else:
    print("Invalid filename")

# Option 2: Use subprocess with argument lists
subprocess.run(['rm', filename], check=True)

# Option 3: Use shell=False (most secure)
subprocess.run(['rm', filename], shell=False, check=True)
```

### Safe Command Execution
```python
import os
import shlex
import subprocess

def safe_system(command, **kwargs):
    """Execute system command safely."""
    if isinstance(command, str):
        # Parse command string safely
        args = shlex.split(command)
    else:
        args = command

    # Use subprocess instead of os.system
    result = subprocess.run(args, **kwargs)
    return result.returncode

# Usage
exit_code = safe_system('ls -la /tmp')
exit_code = safe_system(['ls', '-la', '/tmp'])
```

## Best Practices

### 1. Prefer `subprocess` Over `os.system`
```python
import subprocess

# Instead of:
os.system('ls -la')

# Use:
subprocess.run(['ls', '-la'], check=True)
```

### 2. Handle Command Output Properly
```python
import subprocess

# Capture output
result = subprocess.run(['ls', '-la'],
                       capture_output=True,
                       text=True,
                       check=True)
print(result.stdout)
```

### 3. Validate and Sanitize Input
```python
import os
import subprocess

def safe_execute_command(command, allowed_commands=None):
    """Execute command safely with validation."""
    if allowed_commands and command not in allowed_commands:
        raise ValueError(f"Command not allowed: {command}")

    # Use subprocess with shell=False
    result = subprocess.run(command.split(),
                          capture_output=True,
                          text=True,
                          timeout=30)

    return result.returncode, result.stdout, result.stderr
```

### 4. Use Timeouts for Long-Running Commands
```python
import subprocess

try:
    result = subprocess.run(['long_running_command'],
                          timeout=300,  # 5 minutes
                          check=True)
except subprocess.TimeoutExpired:
    print("Command timed out")
```

### 5. Handle Process Groups for Complex Commands
```python
import os
import subprocess

# Run command in new process group
result = subprocess.run(['command'],
                       preexec_fn=os.setsid,
                       check=True)
```

## Common Patterns

### Cross-Platform Command Execution
```python
import os
import subprocess
import platform

def run_command_cross_platform(command_dict):
    """Run command based on platform."""
    system = platform.system().lower()

    if system in command_dict:
        command = command_dict[system]
        return subprocess.run(command, check=True)
    else:
        raise OSError(f"No command defined for {system}")

# Usage
commands = {
    'windows': ['cmd', '/c', 'dir'],
    'linux': ['ls', '-la'],
    'darwin': ['ls', '-la']
}

result = run_command_cross_platform(commands)
```

### Command Pipeline
```python
import subprocess

def run_pipeline(commands):
    """Run a pipeline of commands."""
    previous_output = None

    for i, command in enumerate(commands):
        if i == 0:
            # First command
            proc = subprocess.Popen(command,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        elif i == len(commands) - 1:
            # Last command
            proc = subprocess.Popen(command,
                                  stdin=previous_output,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        else:
            # Middle command
            proc = subprocess.Popen(command,
                                  stdin=previous_output,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

        previous_output = proc.stdout

    # Wait for all processes
    output, errors = proc.communicate()
    return output.decode(), errors.decode()

# Usage
commands = [
    ['echo', 'Hello World'],
    ['grep', 'Hello'],
    ['wc', '-l']
]

output, errors = run_pipeline(commands)
```

### Background Process Management
```python
import os
import subprocess
import signal
import time

class BackgroundProcess:
    """Manage background processes."""

    def __init__(self, command):
        self.command = command
        self.process = None

    def start(self):
        """Start the background process."""
        self.process = subprocess.Popen(self.command,
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)

    def stop(self):
        """Stop the background process."""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

    def is_running(self):
        """Check if process is running."""
        return self.process and self.process.poll() is None

# Usage
bg_proc = BackgroundProcess(['python', 'server.py'])
bg_proc.start()

# Do other work
time.sleep(10)

bg_proc.stop()
```

These functions provide powerful capabilities for system interaction, but require careful attention to security and cross-platform compatibility.
