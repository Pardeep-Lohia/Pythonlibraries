# Common Mistakes with Subprocess

## Overview

Despite its power and flexibility, `subprocess` is prone to common mistakes that can lead to security vulnerabilities, unexpected behavior, and hard-to-debug issues. This document outlines the most frequent pitfalls and how to avoid them.

## Security Mistakes

### 1. Using shell=True with Untrusted Input

**❌ Wrong:**
```python
# DANGEROUS: Shell injection vulnerability
filename = input("Enter filename: ")
subprocess.run(f'cat {filename}', shell=True)  # Attacker can execute "; rm -rf /"
```

**✅ Correct:**
```python
# SAFE: Arguments passed directly to exec
filename = input("Enter filename: ")
subprocess.run(['cat', filename])
```

**Why it's dangerous:** Shell interprets special characters, allowing command injection attacks.

### 2. Not Sanitizing Environment Variables

**❌ Wrong:**
```python
# Dangerous: Inherits all environment variables
subprocess.run(['command'], env=os.environ.copy())
```

**✅ Correct:**
```python
# Safe: Only include necessary variables
safe_env = {
    'PATH': '/usr/local/bin:/usr/bin:/bin',
    'HOME': os.environ.get('HOME', ''),
    'USER': os.environ.get('USER', ''),
}
subprocess.run(['command'], env=safe_env)
```

**Why it's dangerous:** Malicious environment variables can alter command behavior.

### 3. Using Shell for Simple Commands

**❌ Wrong:**
```python
# Unnecessary shell overhead
subprocess.run('echo hello', shell=True)
```

**✅ Correct:**
```python
# Direct execution
subprocess.run(['echo', 'hello'])
```

**Why it's dangerous:** Shell adds performance overhead and parsing complexity.

## Error Handling Mistakes

### 4. Ignoring Return Codes

**❌ Wrong:**
```python
# Silent failure
subprocess.run(['command'])
print("Command completed successfully")  # May not be true
```

**✅ Correct:**
```python
result = subprocess.run(['command'])
if result.returncode != 0:
    print(f"Command failed with code {result.returncode}")
    handle_error()
```

**Why it's dangerous:** Programs appear to succeed when they actually fail.

### 5. Not Handling Exceptions Properly

**❌ Wrong:**
```python
# Bare except catches everything
try:
    subprocess.run(['command'])
except:
    pass  # Silently ignore all errors
```

**✅ Correct:**
```python
try:
    result = subprocess.run(['command'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed: {e}")
except FileNotFoundError:
    print("Command not found")
except Exception as e:
    print(f"Unexpected error: {e}")
```

**Why it's dangerous:** Important errors get hidden, making debugging impossible.

### 6. Not Setting Timeouts

**❌ Wrong:**
```python
# Can hang indefinitely
subprocess.run(['long_running_command'])
```

**✅ Correct:**
```python
# Timeout prevents hanging
subprocess.run(['long_running_command'], timeout=30)
```

**Why it's dangerous:** Processes can hang forever, consuming resources.

## Resource Management Mistakes

### 7. Creating Zombie Processes

**❌ Wrong:**
```python
# Creates zombie processes
process = subprocess.Popen(['command'])
# No wait() - process becomes zombie when it exits
```

**✅ Correct:**
```python
process = subprocess.Popen(['command'])
process.wait()  # Prevents zombies
```

**Why it's dangerous:** Zombie processes consume system resources.

### 8. Not Closing File Descriptors

**❌ Wrong:**
```python
# Resource leak
process = subprocess.Popen(['command'], stdout=subprocess.PIPE)
output = process.communicate()[0]
# File descriptors not explicitly closed
```

**✅ Correct:**
```python
with subprocess.Popen(['command'], stdout=subprocess.PIPE) as process:
    output = process.communicate()[0]
# Automatically cleaned up
```

**Why it's dangerous:** File descriptor leaks can exhaust system limits.

### 9. Improper Signal Handling

**❌ Wrong:**
```python
# Race condition in signal handling
import signal

def terminate_process(process):
    process.terminate()
    time.sleep(1)  # Unreliable
    if process.poll() is None:
        process.kill()
```

**✅ Correct:**
```python
def terminate_process(process):
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
```

**Why it's dangerous:** Improper cleanup can leave processes running.

## I/O and Data Handling Mistakes

### 10. Mixing Text and Binary Modes

**❌ Wrong:**
```python
# Inconsistent encoding
result = subprocess.run(['command'], capture_output=True)
text_output = result.stdout.decode('utf-8')  # May fail
```

**✅ Correct:**
```python
# Explicit text mode
result = subprocess.run(['command'], capture_output=True, text=True)
text_output = result.stdout  # Already decoded
```

**Why it's dangerous:** Encoding errors can crash programs or corrupt data.

### 11. Not Handling Large Output

**❌ Wrong:**
```python
# Loads entire output into memory
result = subprocess.run(['command_with_huge_output'], capture_output=True)
process_output(result.stdout)  # May cause memory exhaustion
```

**✅ Correct:**
```python
# Stream output to avoid memory issues
process = subprocess.Popen(['command'], stdout=subprocess.PIPE, text=True)
for line in process.stdout:
    process_line(line)  # Process line by line
process.wait()
```

**Why it's dangerous:** Large outputs can exhaust memory.

### 12. Incorrect Pipe Usage

**❌ Wrong:**
```python
# Broken pipe - reading after writing closes pipe
p1 = subprocess.Popen(['echo', 'hello'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', 'hello'], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()  # Too early - p2 may not have read yet
```

**✅ Correct:**
```python
p1 = subprocess.Popen(['echo', 'hello'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', 'hello'], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()  # Close after p2 starts
output = p2.communicate()[0]  # Let p2 finish first
```

**Why it's dangerous:** Broken pipes cause unexpected termination.

## Cross-Platform Mistakes

### 13. Assuming Unix Behavior on Windows

**❌ Wrong:**
```python
# Unix-only
subprocess.run(['ls', '-la'])  # Fails on Windows
```

**✅ Correct:**
```python
import platform

if platform.system() == 'Windows':
    subprocess.run(['dir'])
else:
    subprocess.run(['ls', '-la'])
```

**Why it's dangerous:** Code works on one platform but fails on others.

### 14. Hardcoding Paths

**❌ Wrong:**
```python
# Platform-specific paths
subprocess.run(['/bin/ls'])  # Doesn't work on Windows
```

**✅ Correct:**
```python
import shutil

ls_command = shutil.which('ls')
if ls_command:
    subprocess.run([ls_command])
```

**Why it's dangerous:** Paths differ between operating systems.

### 15. Ignoring Platform-Specific Return Codes

**❌ Wrong:**
```python
# Assumes Unix return codes
result = subprocess.run(['command'])
if result.returncode == 2:  # May mean different things
    handle_error()
```

**✅ Correct:**
```python
# Check platform-specific meanings
result = subprocess.run(['command'])
if result.returncode != 0:
    # Handle error generically, then check platform specifics
    handle_error(result.returncode, platform.system())
```

**Why it's dangerous:** Same return code can mean different things on different platforms.

## Performance Mistakes

### 16. Unnecessary Shell Usage

**❌ Wrong:**
```python
# Shell overhead for simple commands
for i in range(100):
    subprocess.run(f'echo {i}', shell=True)  # Shell created 100 times
```

**✅ Correct:**
```python
# Direct execution
for i in range(100):
    subprocess.run(['echo', str(i)])  # No shell overhead
```

**Why it's dangerous:** Shell startup time adds up with many calls.

### 17. Inefficient Output Handling

**❌ Wrong:**
```python
# Inefficient for large data
result = subprocess.run(['command'], capture_output=True)
lines = result.stdout.decode().split('\n')  # Decode entire output
```

**✅ Correct:**
```python
# Process line by line
process = subprocess.Popen(['command'], stdout=subprocess.PIPE, text=True)
for line in process.stdout:
    process_line(line.strip())
```

**Why it's dangerous:** Large outputs consume excessive memory.

### 18. Not Reusing Process Objects

**❌ Wrong:**
```python
# Creates new process for each call
for file in files:
    result = subprocess.run(['process_file', file], capture_output=True)
```

**✅ Correct:**
```python
# Consider if process can be reused or batched
# If not, at least use threading for concurrent execution
import concurrent.futures

def process_file(file):
    return subprocess.run(['process_file', file], capture_output=True)

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(process_file, files))
```

**Why it's dangerous:** Process creation overhead can be significant.

## Best Practices to Avoid Mistakes

### Defense in Depth

```python
def safe_subprocess_run(cmd, **kwargs):
    """Safe subprocess execution with multiple layers of protection"""

    # 1. Input validation
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Command must be non-empty list")

    # 2. Sanitize command
    safe_cmd = [str(arg) for arg in cmd]  # Ensure strings

    # 3. Safe defaults
    defaults = {
        'capture_output': True,
        'text': True,
        'timeout': 30,
        'check': False,
    }
    defaults.update(kwargs)

    # 4. Execute with error handling
    try:
        result = subprocess.run(safe_cmd, **defaults)
        return result
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Command timed out: {' '.join(safe_cmd)}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Command not found: {safe_cmd[0]}")
    except Exception as e:
        raise RuntimeError(f"Subprocess error: {e}") from e
```

### Comprehensive Testing

```python
def test_subprocess_safety():
    """Test subprocess operations for common mistakes"""

    # Test injection attempts
    dangerous_inputs = [
        "; rm -rf /",
        "| cat /etc/passwd",
        "`whoami`",
        "$(evil_command)",
    ]

    for dangerous_input in dangerous_inputs:
        try:
            # This should fail safely
            result = subprocess.run(['echo', dangerous_input],
                                  capture_output=True, text=True, timeout=5)
            assert dangerous_input in result.stdout  # Should only echo the input
            print(f"✓ Safe handling of: {dangerous_input}")
        except Exception as e:
            print(f"✗ Unexpected error with: {dangerous_input} - {e}")

    # Test timeout handling
    try:
        subprocess.run(['sleep', '10'], timeout=1)
        assert False, "Should have timed out"
    except subprocess.TimeoutExpired:
        print("✓ Timeout handling works")

    # Test error handling
    try:
        subprocess.run(['false'], check=True)
        assert False, "Should have raised exception"
    except subprocess.CalledProcessError:
        print("✓ Error handling works")
```

### Code Review Checklist

- [ ] Are all commands using list format, not shell strings?
- [ ] Is `shell=True` only used when absolutely necessary?
- [ ] Are timeouts set for all potentially long-running commands?
- [ ] Is error output captured and handled appropriately?
- [ ] Are return codes checked and handled?
- [ ] Is input validated and sanitized?
- [ ] Are file descriptors properly closed?
- [ ] Is the code cross-platform compatible?
- [ ] Are resources properly cleaned up?
- [ ] Is logging adequate for debugging?

## Summary

The most common subprocess mistakes involve:
1. **Security**: Using shell with untrusted input
2. **Error handling**: Ignoring return codes and exceptions
3. **Resources**: Not cleaning up processes and file descriptors
4. **Performance**: Unnecessary shell usage and inefficient I/O
5. **Cross-platform**: Assuming Unix behavior everywhere

Following these guidelines and using the provided safe patterns will help avoid these pitfalls and create robust, secure subprocess code.
