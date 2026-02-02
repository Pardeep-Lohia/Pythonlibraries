# Error Handling with Subprocess

## Overview

Error handling is crucial when working with `subprocess` due to the complexity of external process execution. This document covers exception handling, return code interpretation, timeout management, and robust error recovery patterns.

## Exception Types

### subprocess.CalledProcessError

Raised when a process returns a non-zero exit code and `check=True` is used.

```python
import subprocess

try:
    subprocess.run(['false'], check=True)  # Command that always fails
except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}")
    print(f"Command: {e.cmd}")
    print(f"Output: {e.output}")
    print(f"Error: {e.stderr}")
```

### subprocess.TimeoutExpired

Raised when a process exceeds the specified timeout.

```python
try:
    result = subprocess.run(['sleep', '10'], timeout=5)
except subprocess.TimeoutExpired as e:
    print(f"Command timed out after {e.timeout} seconds")
    print(f"Command: {e.cmd}")
```

### FileNotFoundError

Raised when the specified command is not found.

```python
try:
    subprocess.run(['nonexistent_command'])
except FileNotFoundError as e:
    print(f"Command not found: {e.filename}")
```

### PermissionError

Raised when there are insufficient permissions to execute a command.

```python
try:
    subprocess.run(['./script.sh'])
except PermissionError as e:
    print(f"Permission denied: {e.filename}")
```

### OSError and Subclasses

Base class for various system-related errors.

```python
try:
    subprocess.run(['command'])
except OSError as e:
    print(f"OS error: {e}")
except BrokenPipeError as e:
    print(f"Broken pipe: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}")
```

## Return Code Interpretation

### Standard Return Codes

- **0**: Success
- **1**: General error
- **2**: Shell syntax error (when using shell=True)
- **126**: Command found but not executable
- **127**: Command not found
- **128+n**: Terminated by signal n

```python
def interpret_return_code(returncode):
    """Interpret common return codes"""
    if returncode == 0:
        return "Success"
    elif returncode == 1:
        return "General error"
    elif returncode == 2:
        return "Shell syntax error"
    elif returncode == 126:
        return "Command not executable"
    elif returncode == 127:
        return "Command not found"
    elif returncode > 128:
        signal = returncode - 128
        return f"Terminated by signal {signal}"
    else:
        return f"Unknown error code: {returncode}"

result = subprocess.run(['false'])
print(f"Result: {interpret_return_code(result.returncode)}")
```

### Application-Specific Return Codes

Many commands use specific return codes:

```python
def handle_grep_return_code(returncode):
    """Handle grep-specific return codes"""
    if returncode == 0:
        return "Pattern found"
    elif returncode == 1:
        return "Pattern not found"
    elif returncode == 2:
        return "Error occurred"
    else:
        return f"Unknown return code: {returncode}"

result = subprocess.run(['grep', 'pattern', 'file.txt'])
print(handle_grep_return_code(result.returncode))
```

## Comprehensive Error Handling Patterns

### Basic Error Handling

```python
def run_command_basic(cmd):
    """Basic error handling for subprocess commands"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return {
            'success': True,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': 'non_zero_exit',
            'returncode': e.returncode,
            'stdout': e.stdout,
            'stderr': e.stderr
        }
    except subprocess.TimeoutExpired as e:
        return {
            'success': False,
            'error': 'timeout',
            'timeout': e.timeout
        }
    except FileNotFoundError as e:
        return {
            'success': False,
            'error': 'command_not_found',
            'command': e.filename
        }
    except PermissionError as e:
        return {
            'success': False,
            'error': 'permission_denied',
            'command': e.filename
        }
    except Exception as e:
        return {
            'success': False,
            'error': 'unexpected',
            'message': str(e)
        }
```

### Advanced Error Handling with Context

```python
class SubprocessError(Exception):
    """Custom exception for subprocess errors"""
    pass

class CommandRunner:
    """Command runner with comprehensive error handling"""

    def __init__(self, logger=None):
        self.logger = logger or print

    def run(self, cmd, **kwargs):
        """Run command with full error context"""
        self.logger(f"Running command: {' '.join(cmd)}")

        # Set sensible defaults
        defaults = {
            'capture_output': True,
            'text': True,
            'timeout': 60,
            'check': False
        }
        defaults.update(kwargs)

        try:
            result = subprocess.run(cmd, **defaults)

            if result.returncode == 0:
                self.logger("Command succeeded")
                return result
            else:
                error_msg = f"Command failed with return code {result.returncode}"
                if result.stderr:
                    error_msg += f": {result.stderr.strip()}"
                raise SubprocessError(error_msg)

        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timed out after {e.timeout} seconds"
            self.logger(error_msg)
            raise SubprocessError(error_msg) from e

        except FileNotFoundError as e:
            error_msg = f"Command not found: {e.filename}"
            self.logger(error_msg)
            raise SubprocessError(error_msg) from e

        except PermissionError as e:
            error_msg = f"Permission denied: {e.filename}"
            self.logger(error_msg)
            raise SubprocessError(error_msg) from e

        except OSError as e:
            error_msg = f"OS error: {e}"
            self.logger(error_msg)
            raise SubprocessError(error_msg) from e

        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            self.logger(error_msg)
            raise SubprocessError(error_msg) from e
```

### Conditional Error Checking

```python
def run_with_conditional_check(cmd, allowed_codes=None):
    """Run command with conditional error checking"""
    if allowed_codes is None:
        allowed_codes = [0]  # Only success by default

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode in allowed_codes:
        return result
    else:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, result.stdout, result.stderr
        )

# Usage
try:
    # Allow both success (0) and "not found" (1) for grep
    result = run_with_conditional_check(['grep', 'pattern', 'file.txt'], [0, 1])
except subprocess.CalledProcessError as e:
    print(f"Grep failed: {e}")
```

## Timeout Management

### Command-Level Timeouts

```python
def run_with_timeout(cmd, timeout=30, **kwargs):
    """Run command with timeout and proper cleanup"""
    try:
        result = subprocess.run(cmd, timeout=timeout, **kwargs)
        return result
    except subprocess.TimeoutExpired:
        # Log timeout but don't raise - let caller decide
        print(f"Command timed out after {timeout} seconds: {' '.join(cmd)}")
        return None

# Usage
result = run_with_timeout(['sleep', '10'], timeout=5)
if result is None:
    print("Command timed out")
```

### Communication Timeouts

```python
def communicate_with_timeout(process, input_data=None, timeout=10):
    """Communicate with process with timeout"""
    try:
        stdout, stderr = process.communicate(input=input_data, timeout=timeout)
        return stdout, stderr
    except subprocess.TimeoutExpired:
        # Kill the process if communication times out
        process.kill()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass  # Process didn't respond to kill
        raise
```

### Progressive Timeout Strategy

```python
def run_with_progressive_timeout(cmd, initial_timeout=10, max_attempts=3):
    """Run command with increasing timeouts"""
    timeout = initial_timeout

    for attempt in range(max_attempts):
        try:
            result = subprocess.run(cmd, timeout=timeout, capture_output=True, text=True)
            return result
        except subprocess.TimeoutExpired:
            if attempt < max_attempts - 1:
                timeout *= 2  # Double the timeout
                print(f"Attempt {attempt + 1} timed out, retrying with {timeout}s timeout")
            else:
                raise

# Usage
try:
    result = run_with_progressive_timeout(['slow_command'], initial_timeout=5)
except subprocess.TimeoutExpired:
    print("Command failed even with maximum timeout")
```

## Resource Error Handling

### Memory and CPU Limits

```python
import resource

def run_with_resource_limits(cmd, cpu_limit=60, mem_limit=100*1024*1024):
    """Run command with resource limits and error handling"""

    def preexec():
        # Set CPU time limit
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
        # Set memory limit
        resource.setrlimit(resource.RLIMIT_AS, (mem_limit, mem_limit))

    try:
        process = subprocess.Popen(cmd, preexec_fn=preexec)
        stdout, stderr = process.communicate(timeout=cpu_limit + 10)
        return {
            'success': True,
            'returncode': process.returncode,
            'stdout': stdout,
            'stderr': stderr
        }
    except subprocess.TimeoutExpired:
        process.kill()
        return {'success': False, 'error': 'timeout'}
    except resource.error as e:
        return {'success': False, 'error': f'resource_limit: {e}'}
```

### Disk Space Handling

```python
def run_with_disk_check(cmd, min_space_mb=100):
    """Run command only if sufficient disk space is available"""
    try:
        # Check available disk space
        stat = os.statvfs('.')
        available_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)

        if available_mb < min_space_mb:
            raise OSError(f"Insufficient disk space: {available_mb:.1f}MB available")

        return subprocess.run(cmd, capture_output=True, text=True)

    except OSError as e:
        print(f"Disk space error: {e}")
        return None
```

## Cross-Platform Error Handling

### Platform-Specific Errors

```python
import platform

def handle_platform_specific_errors(cmd):
    """Handle errors differently based on platform"""
    system = platform.system()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    except FileNotFoundError as e:
        if system == 'Windows':
            # Windows might need .exe extension
            alt_cmd = [cmd[0] + '.exe'] + cmd[1:]
            try:
                return subprocess.run(alt_cmd, capture_output=True, text=True)
            except FileNotFoundError:
                raise e
        else:
            raise

    except PermissionError as e:
        if system == 'Windows':
            print("Try running as Administrator")
        else:
            print("Check file permissions with 'ls -la'")
        raise
```

### Encoding Error Handling

```python
def run_with_encoding_fallback(cmd, encodings=None):
    """Run command with encoding fallback"""
    if encodings is None:
        encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            result = subprocess.run(cmd, capture_output=True,
                                   text=True, encoding=encoding)
            return result
        except UnicodeDecodeError:
            continue

    # If all encodings fail, try with errors='replace'
    result = subprocess.run(cmd, capture_output=True,
                           text=True, encoding='utf-8', errors='replace')
    return result
```

## Logging and Monitoring

### Error Logging

```python
import logging

class SubprocessLogger:
    """Logger for subprocess operations"""

    def __init__(self):
        self.logger = logging.getLogger('subprocess')
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_command_start(self, cmd):
        self.logger.info(f"Starting command: {' '.join(cmd)}")

    def log_command_success(self, cmd, result):
        self.logger.info(f"Command succeeded: {' '.join(cmd)} (code: {result.returncode})")

    def log_command_error(self, cmd, error):
        self.logger.error(f"Command failed: {' '.join(cmd)} - {error}")

    def run_with_logging(self, cmd, **kwargs):
        """Run command with automatic logging"""
        self.log_command_start(cmd)

        try:
            result = subprocess.run(cmd, **kwargs)

            if result.returncode == 0:
                self.log_command_success(cmd, result)
            else:
                error_msg = f"Non-zero exit code: {result.returncode}"
                if hasattr(result, 'stderr') and result.stderr:
                    error_msg += f" - {result.stderr.strip()}"
                self.log_command_error(cmd, error_msg)

            return result

        except Exception as e:
            self.log_command_error(cmd, str(e))
            raise
```

### Performance Monitoring

```python
import time

def run_with_performance_monitoring(cmd, **kwargs):
    """Run command with performance monitoring"""
    start_time = time.time()

    try:
        result = subprocess.run(cmd, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time

        print(f"Command completed in {execution_time:.2f} seconds")
        print(f"Return code: {result.returncode}")

        if execution_time > 10:  # Log slow commands
            print(f"WARNING: Command took longer than 10 seconds")

        return result

    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Command failed after {execution_time:.2f} seconds: {e}")
        raise
```

## Recovery and Retry Patterns

### Automatic Retry

```python
def run_with_retry(cmd, max_retries=3, delay=1, **kwargs):
    """Run command with automatic retry on failure"""
    import time

    for attempt in range(max_retries + 1):
        try:
            result = subprocess.run(cmd, **kwargs)

            if result.returncode == 0:
                return result
            else:
                if attempt < max_retries:
                    print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    raise subprocess.CalledProcessError(
                        result.returncode, cmd, result.stdout, result.stderr
                    )

        except (subprocess.TimeoutExpired, OSError) as e:
            if attempt < max_retries:
                print(f"Attempt {attempt + 1} failed with {type(e).__name__}, retrying...")
                time.sleep(delay)
                delay *= 2
            else:
                raise
```

### Graceful Degradation

```python
def run_with_fallback(primary_cmd, fallback_cmd, **kwargs):
    """Run primary command, fall back to alternative on failure"""
    try:
        result = subprocess.run(primary_cmd, **kwargs)
        if result.returncode == 0:
            return result
        else:
            print("Primary command failed, trying fallback...")
            return subprocess.run(fallback_cmd, **kwargs)
    except Exception as e:
        print(f"Primary command error: {e}, trying fallback...")
        return subprocess.run(fallback_cmd, **kwargs)
```

## Testing Error Conditions

### Error Simulation for Testing

```python
def simulate_command_errors():
    """Demonstrate various error conditions for testing"""

    test_cases = [
        (['true'], "Success case"),
        (['false'], "Non-zero exit code"),
        (['sleep', '10'], "Timeout case"),
        (['nonexistent_command'], "Command not found"),
        (['sh', '-c', 'exit 42'], "Custom exit code"),
    ]

    for cmd, description in test_cases:
        print(f"\nTesting: {description}")
        print(f"Command: {' '.join(cmd)}")

        try:
            if 'sleep' in cmd:
                result = subprocess.run(cmd, timeout=2, capture_output=True, text=True)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            print(f"Result: returncode={result.returncode}")

        except subprocess.TimeoutExpired:
            print("Result: TimeoutExpired")
        except FileNotFoundError:
            print("Result: FileNotFoundError")
        except Exception as e:
            print(f"Result: {type(e).__name__}: {e}")

# Run error simulation
simulate_command_errors()
```

This comprehensive guide covers all aspects of error handling in `subprocess`, from basic exception catching to advanced recovery patterns, cross-platform considerations, and testing strategies.
