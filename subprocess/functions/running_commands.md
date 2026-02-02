# Running Commands with Subprocess

## Overview

The `subprocess` module provides several functions for running external commands. The primary functions are `run()`, `Popen()`, `call()`, and `check_output()`. This document focuses on the recommended approaches for running commands.

## subprocess.run()

### Purpose
`subprocess.run()` is the recommended high-level function for running external commands. It waits for the command to complete and returns a `CompletedProcess` instance.

### Syntax
```python
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None,
               capture_output=False, shell=False, cwd=None, timeout=None,
               check=False, encoding=None, errors=None, text=None,
               env=None, universal_newlines=None)
```

### Parameters
- **args**: Command and arguments as a list or string
- **stdin/stdout/stderr**: How to handle standard streams
- **capture_output**: Capture both stdout and stderr
- **shell**: Run command through shell
- **cwd**: Working directory for the command
- **timeout**: Maximum time to wait for command completion
- **check**: Raise exception if command returns non-zero exit code
- **encoding/text**: Handle output as text instead of bytes
- **env**: Environment variables for the subprocess

### Examples

#### Basic Command Execution
```python
import subprocess

# Run a simple command
result = subprocess.run(['echo', 'Hello World'])
print(f"Return code: {result.returncode}")
```

#### Capturing Output
```python
# Capture stdout
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)
```

#### Providing Input
```python
# Send input to command
result = subprocess.run(['grep', 'python'],
                       input='Python is great\nJavaScript is also good\n',
                       capture_output=True, text=True)
print(result.stdout)  # "Python is great"
```

#### Error Handling
```python
# Raise exception on non-zero exit code
try:
    subprocess.run(['false'], check=True)  # Command that always fails
except subprocess.CalledProcessError as e:
    print(f"Command failed with code {e.returncode}")
```

#### With Timeout
```python
# Timeout after 5 seconds
try:
    result = subprocess.run(['sleep', '10'], timeout=5)
except subprocess.TimeoutExpired:
    print("Command timed out")
```

### Edge Cases

#### Command Not Found
```python
try:
    subprocess.run(['nonexistent_command'])
except FileNotFoundError:
    print("Command not found")
```

#### Permission Denied
```python
# On Unix systems
subprocess.run(['chmod', '000', 'file.txt'])  # Remove permissions
result = subprocess.run(['cat', 'file.txt'])  # Will fail with permission error
```

## subprocess.Popen()

### Purpose
`subprocess.Popen()` provides low-level control over subprocess creation and management. It's useful for advanced scenarios requiring fine-grained control.

### Syntax
```python
subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None,
                 stderr=None, preexec_fn=None, close_fds=True, shell=False,
                 cwd=None, env=None, universal_newlines=None,
                 startupinfo=None, creationflags=0, restore_signals=True,
                 start_new_session=False, pass_fds=(), encoding=None,
                 errors=None, text=None)
```

### Key Methods
- **communicate()**: Interact with process I/O
- **poll()**: Check if process has terminated
- **wait()**: Wait for process to complete
- **terminate()**: Send SIGTERM signal
- **kill()**: Send SIGKILL signal

### Examples

#### Basic Usage
```python
process = subprocess.Popen(['ping', '-c', '4', 'google.com'],
                          stdout=subprocess.PIPE, text=True)

output, error = process.communicate()
print(f"Return code: {process.returncode}")
print(f"Output: {output}")
```

#### Asynchronous Execution
```python
import time

process = subprocess.Popen(['sleep', '5'])
print("Process started")

while process.poll() is None:
    print("Process still running...")
    time.sleep(1)

print("Process finished")
```

#### Real-time Output Reading
```python
process = subprocess.Popen(['ping', 'google.com'],
                          stdout=subprocess.PIPE, text=True)

while True:
    output = process.stdout.readline()
    if output == '' and process.poll() is not None:
        break
    if output:
        print(output.strip())
```

#### Process Termination
```python
process = subprocess.Popen(['sleep', '100'])

# Give it some time
time.sleep(2)

# Terminate gracefully
process.terminate()
time.sleep(1)

# Force kill if still running
if process.poll() is None:
    process.kill()

process.wait()
print(f"Final return code: {process.returncode}")
```

### Edge Cases

#### Handling Large Output
```python
# For commands with large output, read in chunks
process = subprocess.Popen(['cat', 'large_file.txt'],
                          stdout=subprocess.PIPE)

chunk_size = 8192
while True:
    chunk = process.stdout.read(chunk_size)
    if not chunk:
        break
    process_chunk(chunk)
```

#### Cross-Platform Considerations
```python
import platform

if platform.system() == 'Windows':
    process = subprocess.Popen(['cmd', '/c', 'dir'],
                              stdout=subprocess.PIPE)
else:
    process = subprocess.Popen(['ls', '-la'],
                              stdout=subprocess.PIPE)
```

## subprocess.call() (Legacy)

### Purpose
`subprocess.call()` is a legacy function that runs a command and returns the return code. It's simpler than `run()` but less flexible.

### Syntax
```python
subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False,
                cwd=None, timeout=None, **other_popen_kwargs)
```

### Example
```python
# Simple execution
return_code = subprocess.call(['ls', '-la'])
print(f"Command exited with code: {return_code}")
```

**Note**: Prefer `subprocess.run()` over `subprocess.call()` for new code.

## subprocess.check_output() (Legacy)

### Purpose
`subprocess.check_output()` runs a command and returns the output. It raises an exception if the command fails.

### Syntax
```python
subprocess.check_output(args, *, stdin=None, stderr=None, shell=False,
                        cwd=None, encoding=None, errors=None, text=None,
                        timeout=None, **other_popen_kwargs)
```

### Example
```python
# Get command output
output = subprocess.check_output(['ls', '-la'], text=True)
print(output)
```

**Note**: Use `subprocess.run(capture_output=True)` instead for new code.

## Best Practices for Running Commands

### Security
```python
# GOOD: Use list format to prevent shell injection
user_input = "file.txt"
subprocess.run(['cat', user_input])

# BAD: Shell injection vulnerability
subprocess.run(f'cat {user_input}', shell=True)
```

### Error Handling
```python
def run_command_safely(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=30, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except subprocess.TimeoutExpired:
        print("Command timed out")
        return None
    except FileNotFoundError:
        print("Command not found")
        return None
```

### Cross-Platform Compatibility
```python
import platform

def run_ls_command():
    if platform.system() == 'Windows':
        return subprocess.run(['dir'], capture_output=True, text=True)
    else:
        return subprocess.run(['ls', '-la'], capture_output=True, text=True)
```

### Resource Management
```python
# Always close file handles
with subprocess.Popen(['command'], stdout=subprocess.PIPE) as process:
    output = process.communicate()[0]

# Or explicitly close
process = subprocess.Popen(['command'], stdout=subprocess.PIPE)
try:
    output = process.communicate()
finally:
    process.stdout.close()
    process.stderr.close()
```

## Common Patterns

### Command Builder
```python
class CommandBuilder:
    def __init__(self, base_cmd):
        self.cmd = [base_cmd]

    def add_arg(self, arg):
        self.cmd.append(arg)
        return self

    def add_flag(self, flag):
        self.cmd.append(flag)
        return self

    def run(self, **kwargs):
        return subprocess.run(self.cmd, **kwargs)

# Usage
cmd = CommandBuilder('git').add_arg('log').add_flag('--oneline')
result = cmd.run(capture_output=True, text=True)
```

### Command Runner with Logging
```python
import logging

class CommandRunner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run(self, cmd, **kwargs):
        self.logger.info(f"Running command: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, **kwargs)
            self.logger.info(f"Command completed with code: {result.returncode}")
            return result
        except Exception as e:
            self.logger.error(f"Command failed: {e}")
            raise
```

### Parallel Command Execution
```python
from concurrent.futures import ThreadPoolExecutor

def run_commands_parallel(commands):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(subprocess.run, cmd, capture_output=True, text=True)
                  for cmd in commands]
        return [future.result() for future in futures]

# Usage
commands = [['echo', 'cmd1'], ['echo', 'cmd2'], ['echo', 'cmd3']]
results = run_commands_parallel(commands)
```

## Performance Considerations

### When to Use Each Function
- **`run()`**: Most common use cases, simple synchronous execution
- **`Popen()`**: Advanced control, asynchronous execution, real-time I/O
- **`call()`**: Legacy, simple cases where you only need return code
- **`check_output()`**: Legacy, when you only need output and want exceptions on failure

### Overhead Comparison
- `run()`: Minimal overhead, recommended for most cases
- `Popen()`: Slightly more overhead but maximum flexibility
- Shell execution: Significant overhead, avoid when possible

### Memory Usage
```python
# For large output, stream to avoid memory issues
def stream_output(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        yield line.strip()
    process.wait()

for line in stream_output(['cat', 'large_file.txt']):
    process_line(line)
```

This comprehensive guide covers the essential functions and patterns for running commands with `subprocess`, ensuring safe, efficient, and maintainable code.
