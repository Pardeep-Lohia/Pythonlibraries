# Subprocess Cheatsheet

## Quick Reference Guide

### Basic Usage

#### Run a command and wait for completion
```python
import subprocess

# Simple execution
result = subprocess.run(['ls', '-la'])

# Capture output
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)

# Check for success
if result.returncode == 0:
    print("Success!")
```

#### Run command with error handling
```python
try:
    result = subprocess.run(['command'], check=True, timeout=30)
except subprocess.CalledProcessError as e:
    print(f"Failed with code {e.returncode}")
except subprocess.TimeoutExpired:
    print("Timed out")
```

### Input/Output Handling

#### Capture stdout and stderr separately
```python
result = subprocess.run(['command'],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       text=True)
```

#### Redirect stderr to stdout
```python
result = subprocess.run(['command'],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT,
                       text=True)
```

#### Provide input to command
```python
result = subprocess.run(['grep', 'pattern'],
                       input='line1\nline2\nline3',
                       capture_output=True,
                       text=True)
```

#### Pipe between commands
```python
# Method 1: Manual piping
p1 = subprocess.Popen(['echo', 'hello'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', 'ell'], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()
output = p2.communicate()[0]

# Method 2: Shell piping (use with caution)
result = subprocess.run('echo hello | grep ell', shell=True, capture_output=True, text=True)
```

### Process Management

#### Asynchronous execution with Popen
```python
process = subprocess.Popen(['long_command'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

# Check if running
if process.poll() is None:
    print("Still running")

# Wait for completion
process.wait()

# Get result
output, errors = process.communicate()
```

#### Terminate a process
```python
process = subprocess.Popen(['command'])

# Graceful termination
process.terminate()
time.sleep(1)

# Force kill if still running
if process.poll() is None:
    process.kill()
```

#### Run with timeout
```python
try:
    result = subprocess.run(['command'], timeout=10)
except subprocess.TimeoutExpired:
    print("Command timed out")
```

### Environment and Context

#### Custom environment variables
```python
import os

env = os.environ.copy()
env['CUSTOM_VAR'] = 'value'

result = subprocess.run(['command'], env=env)
```

#### Change working directory
```python
result = subprocess.run(['command'], cwd='/path/to/directory')
```

#### Run as different user (Unix only)
```python
import os

def run_as_user(uid, gid):
    def preexec():
        os.setgid(gid)
        os.setuid(uid)
    return preexec

process = subprocess.Popen(['command'], preexec_fn=run_as_user(1000, 1000))
```

### Security Best Practices

#### ✅ Safe: Use argument lists
```python
# Good
subprocess.run(['ls', directory])
```

#### ❌ Unsafe: Shell injection risk
```python
# Bad - vulnerable to injection
subprocess.run(f'ls {directory}', shell=True)
```

#### Input validation
```python
def safe_command(user_input):
    # Validate input
    if not user_input or '..' in user_input:
        raise ValueError("Invalid input")

    return subprocess.run(['cat', user_input])
```

### Cross-Platform Code

#### Platform detection
```python
import platform

if platform.system() == 'Windows':
    result = subprocess.run(['cmd', '/c', 'dir'])
else:
    result = subprocess.run(['ls', '-la'])
```

#### Path handling
```python
import os

# Cross-platform paths
script_path = os.path.join('scripts', 'myscript.py')
subprocess.run(['python', script_path])
```

### Common Patterns

#### Command builder
```python
class Cmd:
    def __init__(self, cmd):
        self.cmd = [cmd]

    def arg(self, *args):
        self.cmd.extend(args)
        return self

    def flag(self, flag):
        self.cmd.append(flag)
        return self

    def run(self, **kwargs):
        return subprocess.run(self.cmd, **kwargs)

# Usage
(Cmd('git').arg('log').flag('--oneline').run(capture_output=True))
```

#### Safe runner
```python
def run_safe(cmd, **kwargs):
    defaults = {
        'capture_output': True,
        'text': True,
        'timeout': 30,
        'check': False
    }
    defaults.update(kwargs)
    return subprocess.run(cmd, **defaults)

result = run_safe(['ls', '-la'])
```

#### Process pool
```python
from concurrent.futures import ThreadPoolExecutor

def run_parallel(commands):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(subprocess.run, cmd, capture_output=True, text=True)
                  for cmd in commands]
        return [f.result() for f in futures]

results = run_parallel([['cmd1'], ['cmd2'], ['cmd3']])
```

### Error Handling Reference

#### Exception types
```python
try:
    result = subprocess.run(['command'], check=True)
except subprocess.CalledProcessError as e:
    # Non-zero exit code
    print(f"Failed: {e.returncode}")
except subprocess.TimeoutExpired as e:
    # Timeout exceeded
    print(f"Timed out after {e.timeout}s")
except FileNotFoundError:
    # Command not found
    print("Command not found")
except PermissionError:
    # Permission denied
    print("Permission denied")
```

#### Return code meanings
- `0`: Success
- `1`: General error
- `2`: Shell syntax error
- `126`: Command found but not executable
- `127`: Command not found
- `128+n`: Terminated by signal n

### Performance Tips

#### Avoid shell when possible
```python
# Faster
subprocess.run(['echo', 'hello'])

# Slower (shell overhead)
subprocess.run('echo hello', shell=True)
```

#### Use text mode for string processing
```python
# Efficient for text
result = subprocess.run(['command'], capture_output=True, text=True)
lines = result.stdout.splitlines()
```

#### Stream large output
```python
# Memory efficient
process = subprocess.Popen(['large_output_cmd'], stdout=subprocess.PIPE, text=True)
for line in process.stdout:
    process_line(line.strip())
process.wait()
```

### Function Comparison

| Function | Use Case | Blocking | Returns | Complexity |
|----------|----------|----------|---------|------------|
| `run()` | Simple commands | Yes | `CompletedProcess` | Low |
| `Popen()` | Advanced control | No | `Popen` object | High |
| `call()` | Legacy simple | Yes | Return code | Low |
| `check_output()` | Legacy output | Yes | Output bytes | Low |

### Parameter Quick Reference

#### subprocess.run() parameters
- `args`: Command and arguments (list)
- `capture_output`: Capture stdout/stderr
- `text`: Return strings instead of bytes
- `input`: String to send to stdin
- `timeout`: Maximum execution time
- `check`: Raise exception on non-zero exit
- `cwd`: Working directory
- `env`: Environment variables
- `shell`: Run through shell

#### subprocess.Popen() parameters
- `args`: Command and arguments
- `stdin/stdout/stderr`: I/O handling
- `shell`: Use shell
- `cwd`: Working directory
- `env`: Environment variables
- `preexec_fn`: Function to run before exec (Unix)
- `start_new_session`: New process session

### Common Command Examples

#### File operations
```python
# List files
subprocess.run(['ls', '-la'])

# Copy files
subprocess.run(['cp', 'source', 'dest'])

# Find files
subprocess.run(['find', '.', '-name', '*.py'])
```

#### System information
```python
# Disk usage
subprocess.run(['df', '-h'])

# Process list
subprocess.run(['ps', 'aux'])

# Network info
subprocess.run(['ifconfig'])
```

#### Development tools
```python
# Git commands
subprocess.run(['git', 'status'])
subprocess.run(['git', 'log', '--oneline'])

# Python execution
subprocess.run(['python', 'script.py'])

# Package management
subprocess.run(['pip', 'install', 'package'])
```

### Debugging Tips

#### Enable logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
# Subprocess operations will be logged
```

#### Inspect process state
```python
process = subprocess.Popen(['command'])
print(f"PID: {process.pid}")
print(f"Return code: {process.returncode}")  # None if running
```

#### Test commands manually
```python
# Test command in terminal first
# Then translate to subprocess
# echo hello -> ['echo', 'hello']
# ls -la | grep py -> Use Popen with pipes
```

### Security Checklist

- [ ] Use list arguments, not shell strings
- [ ] Validate all user input
- [ ] Set timeouts to prevent hangs
- [ ] Handle errors and exceptions
- [ ] Use absolute paths when possible
- [ ] Limit resource usage
- [ ] Log subprocess operations
- [ ] Test with malicious input

### Cross-Platform Checklist

- [ ] Test on Windows, Linux, macOS
- [ ] Use `os.path` for paths
- [ ] Handle different line endings
- [ ] Account for different commands
- [ ] Use `shutil.which()` for executables
- [ ] Handle encoding differences

This cheatsheet covers the most common subprocess operations and patterns. Keep it handy for quick reference during development!
