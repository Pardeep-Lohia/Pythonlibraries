# Do's and Don'ts of Subprocess Usage

## Security Do's and Don'ts

### ✅ DO: Use List Arguments Instead of Shell Strings

**Good:**
```python
# Safe: Arguments as list
subprocess.run(['ls', '-la', directory])
```

**Bad:**
```python
# Dangerous: Shell injection vulnerability
subprocess.run(f'ls -la {directory}', shell=True)
```

**Why:** List arguments prevent shell injection attacks where malicious input could execute arbitrary commands.

### ❌ DON'T: Use `shell=True` Unless Absolutely Necessary

**Good:**
```python
# Preferred: No shell needed
subprocess.run(['echo', 'hello'])
```

**Bad:**
```python
# Avoid when possible
subprocess.run('echo hello', shell=True)
```

**Why:** Shell mode introduces security risks and performance overhead. Only use when shell features (pipes, redirection, wildcards) are required.

### ✅ DO: Validate and Sanitize All Inputs

**Good:**
```python
def safe_run_command(user_input):
    # Validate input
    if not isinstance(user_input, str) or '..' in user_input:
        raise ValueError("Invalid input")

    # Use absolute paths when possible
    safe_path = os.path.abspath(user_input)

    return subprocess.run(['cat', safe_path], capture_output=True)
```

**Bad:**
```python
def unsafe_run_command(user_input):
    # No validation - vulnerable to path traversal
    return subprocess.run(['cat', user_input], capture_output=True)
```

**Why:** Input validation prevents command injection and path traversal attacks.

### ✅ DO: Set Appropriate Timeouts

**Good:**
```python
# Prevent hanging processes
result = subprocess.run(['command'], timeout=30)
```

**Bad:**
```python
# Process could hang indefinitely
result = subprocess.run(['command'])  # No timeout
```

**Why:** Timeouts prevent resource exhaustion and unresponsive processes.

## Error Handling Do's and Don'ts

### ✅ DO: Handle All Exceptions Properly

**Good:**
```python
def robust_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        return None
    except subprocess.TimeoutExpired:
        logger.error("Command timed out")
        return None
    except FileNotFoundError:
        logger.error(f"Command not found: {cmd[0]}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

**Bad:**
```python
def fragile_command(cmd):
    # No error handling - crashes on any error
    return subprocess.run(cmd).stdout
```

**Why:** Proper error handling makes code reliable and debuggable.

### ❌ DON'T: Ignore Return Codes

**Good:**
```python
result = subprocess.run(['command'])
if result.returncode != 0:
    handle_error(result.stderr)
```

**Bad:**
```python
# Ignoring return code - silent failures
subprocess.run(['command'])
```

**Why:** Return codes indicate success/failure - ignoring them leads to undetected errors.

### ✅ DO: Use `check=True` When Failure Should Raise Exception

**Good:**
```python
# Explicit error handling
try:
    subprocess.run(['required_command'], check=True)
except subprocess.CalledProcessError:
    handle_critical_failure()
```

**Bad:**
```python
# Silent failure
subprocess.run(['required_command'])  # Ignores failures
```

**Why:** `check=True` ensures failures are not silently ignored in critical operations.

## Resource Management Do's and Don'ts

### ✅ DO: Close File Descriptors Properly

**Good:**
```python
# Explicit cleanup
process = subprocess.Popen(['command'], stdout=subprocess.PIPE)
try:
    output = process.communicate(timeout=30)[0]
finally:
    process.stdout.close()
    process.stderr.close()
```

**Bad:**
```python
# Resource leak
process = subprocess.Popen(['command'], stdout=subprocess.PIPE)
output = process.communicate()[0]
# File descriptors not closed
```

**Why:** Proper cleanup prevents resource leaks and zombie processes.

### ❌ DON'T: Create Zombie Processes

**Good:**
```python
# Always wait for child processes
process = subprocess.Popen(['command'])
process.wait()  # Prevents zombies
```

**Bad:**
```python
# Creates zombie processes
process = subprocess.Popen(['command'])
# No wait() - child becomes zombie when it exits
```

**Why:** Zombie processes consume system resources and should be avoided.

### ✅ DO: Limit Resource Usage

**Good:**
```python
import resource

# Set resource limits for child processes
def run_with_limits(cmd):
    # Limit CPU time to 60 seconds
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
    # Limit memory to 100MB
    resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))

    return subprocess.run(cmd)
```

**Bad:**
```python
# No resource limits - potential DoS
subprocess.run(['untrusted_command'])
```

**Why:** Resource limits prevent abuse and protect system stability.

## Performance Do's and Don'ts

### ✅ DO: Use Appropriate Execution Method

**Good:**
```python
# For simple synchronous execution
result = subprocess.run(['command'], capture_output=True)

# For complex process management
process = subprocess.Popen(['command'], stdout=subprocess.PIPE)
```

**Bad:**
```python
# Using Popen for simple cases
process = subprocess.Popen(['command'], stdout=subprocess.PIPE)
output, _ = process.communicate()
process.wait()
# Equivalent to subprocess.run() but more verbose
```

**Why:** Choose the right tool for the job to keep code simple and efficient.

### ❌ DON'T: Run Commands in Loops Inefficiently

**Good:**
```python
# Batch commands when possible
commands = [['cmd1'], ['cmd2'], ['cmd3']]
results = [subprocess.run(cmd, capture_output=True) for cmd in commands]
```

**Bad:**
```python
# Inefficient: Creates new shell for each command
for cmd in ['cmd1', 'cmd2', 'cmd3']:
    subprocess.run(cmd, shell=True)  # Shell overhead each time
```

**Why:** Minimize shell/process creation overhead by batching operations.

### ✅ DO: Use Text Mode When Working with Strings

**Good:**
```python
# Text mode for string processing
result = subprocess.run(['command'], capture_output=True, text=True)
lines = result.stdout.splitlines()
```

**Bad:**
```python
# Manual decoding required
result = subprocess.run(['command'], capture_output=True)
lines = result.stdout.decode('utf-8').splitlines()
```

**Why:** Text mode simplifies string handling and handles encoding automatically.

## Cross-Platform Do's and Don'ts

### ✅ DO: Handle Platform Differences

**Good:**
```python
import platform

def run_ls():
    if platform.system() == 'Windows':
        return subprocess.run(['dir'], capture_output=True, text=True)
    else:
        return subprocess.run(['ls', '-la'], capture_output=True, text=True)
```

**Bad:**
```python
# Unix-only
subprocess.run(['ls', '-la'])  # Fails on Windows
```

**Why:** Cross-platform code ensures portability and reliability.

### ❌ DON'T: Assume Unix Path Separators

**Good:**
```python
import os

# Cross-platform path handling
script_path = os.path.join('scripts', 'myscript.py')
subprocess.run(['python', script_path])
```

**Bad:**
```python
# Unix-only paths
subprocess.run(['python', 'scripts/myscript.py'])  # Fails on Windows
```

**Why:** Use `os.path` for platform-independent path operations.

### ✅ DO: Handle Line Endings Appropriately

**Good:**
```python
# Normalize line endings
result = subprocess.run(['command'], capture_output=True, text=True)
normalized = result.stdout.replace('\r\n', '\n').replace('\r', '\n')
```

**Bad:**
```python
# Line ending issues on Windows
result = subprocess.run(['command'], capture_output=True, text=True)
lines = result.stdout.split('\n')  # May not work correctly
```

**Why:** Different platforms use different line ending conventions.

## Code Organization Do's and Don'ts

### ✅ DO: Create Helper Functions for Common Patterns

**Good:**
```python
def run_command_safely(cmd, **kwargs):
    """Safe command execution with sensible defaults"""
    defaults = {
        'capture_output': True,
        'text': True,
        'timeout': 30,
        'check': False
    }
    defaults.update(kwargs)
    return subprocess.run(cmd, **defaults)

# Usage
result = run_command_safely(['git', 'status'])
```

**Bad:**
```python
# Repeated subprocess.run calls with same parameters
result1 = subprocess.run(['cmd1'], capture_output=True, text=True, timeout=30)
result2 = subprocess.run(['cmd2'], capture_output=True, text=True, timeout=30)
result3 = subprocess.run(['cmd3'], capture_output=True, text=True, timeout=30)
```

**Why:** Helper functions reduce code duplication and ensure consistency.

### ❌ DON'T: Mix Synchronous and Asynchronous Patterns Unnecessarily

**Good:**
```python
# Clear synchronous pattern
def process_files():
    for file in files:
        result = subprocess.run(['process_file', file], capture_output=True)
        handle_result(result)
```

**Bad:**
```python
# Confusing mix of sync/async
def process_files():
    processes = []
    for file in files:
        process = subprocess.Popen(['process_file', file], stdout=subprocess.PIPE)
        processes.append(process)

    # Later...
    for process in processes:
        output = process.communicate()[0]  # Synchronous wait
```

**Why:** Mixing patterns makes code harder to understand and maintain.

### ✅ DO: Log Subprocess Operations

**Good:**
```python
import logging

def logged_run(cmd, **kwargs):
    logging.info(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, **kwargs)
        logging.info(f"Command completed with code: {result.returncode}")
        return result
    except Exception as e:
        logging.error(f"Command failed: {e}")
        raise
```

**Bad:**
```python
# Silent operations
subprocess.run(['important_command'])  # No logging
```

**Why:** Logging helps with debugging, monitoring, and auditing subprocess operations.

## Summary

**Key Principles:**
- **Security First:** Always prefer list arguments over shell strings
- **Handle Errors:** Never ignore return codes or exceptions
- **Resource Aware:** Set timeouts and clean up properly
- **Cross-Platform:** Write portable code that works everywhere
- **Performance Conscious:** Choose appropriate execution methods
- **Maintainable:** Use helper functions and proper logging

**Remember:** Subprocess operations can have significant security, performance, and reliability implications. When in doubt, err on the side of caution and use the most restrictive, safe options available.
