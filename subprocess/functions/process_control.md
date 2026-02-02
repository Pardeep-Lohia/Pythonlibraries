# Process Control with Subprocess

## Overview

Process control involves monitoring, managing, and terminating subprocesses. The `subprocess` module provides comprehensive tools for controlling process lifecycle, handling signals, and managing long-running processes.

## Process Monitoring

### Checking Process Status

#### poll() Method
Check if a process has terminated without blocking:

```python
import subprocess
import time

process = subprocess.Popen(['sleep', '5'])

# Check status periodically
while True:
    status = process.poll()
    if status is None:
        print("Process is still running...")
        time.sleep(1)
    else:
        print(f"Process finished with return code: {status}")
        break
```

#### Process Information
Access process attributes:

```python
process = subprocess.Popen(['python', 'script.py'])

print(f"Process ID: {process.pid}")
print(f"Return code: {process.returncode}")  # None if running
print(f"Process args: {process.args}")
```

### Waiting for Process Completion

#### wait() Method
Wait for process to complete and get return code:

```python
process = subprocess.Popen(['long_command'])

# Wait indefinitely
return_code = process.wait()
print(f"Process completed with code: {return_code}")

# Wait with timeout
try:
    return_code = process.wait(timeout=30)
    print(f"Process completed with code: {return_code}")
except subprocess.TimeoutExpired:
    print("Process did not complete within timeout")
    process.kill()
```

#### Synchronous vs Asynchronous Waiting
```python
# Synchronous (blocking)
result = subprocess.run(['command'])  # Automatically waits

# Asynchronous (non-blocking)
process = subprocess.Popen(['command'])
# Do other work...
return_code = process.wait()  # Explicit wait
```

## Process Termination

### Graceful Termination

#### terminate() Method
Send SIGTERM signal for graceful shutdown:

```python
import signal
import time

process = subprocess.Popen(['long_running_process'])

# Give process time to clean up
process.terminate()

try:
    process.wait(timeout=10)  # Wait up to 10 seconds
    print("Process terminated gracefully")
except subprocess.TimeoutExpired:
    print("Process didn't terminate gracefully, forcing kill")
    process.kill()
    process.wait()
```

#### Platform-Specific Termination
```python
import platform

def terminate_process(process):
    """Cross-platform process termination"""
    if platform.system() == 'Windows':
        # Windows uses different signal handling
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
    else:
        # Unix-like systems
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
```

### Forceful Termination

#### kill() Method
Send SIGKILL signal for immediate termination:

```python
def force_kill_process(process):
    """Forcefully terminate a process"""
    try:
        process.kill()  # Send SIGKILL
        process.wait(timeout=5)  # Wait for cleanup
        print("Process forcefully terminated")
    except subprocess.TimeoutExpired:
        print("Process didn't respond to kill signal")
    except ProcessLookupError:
        print("Process already terminated")
```

### Termination Best Practices

```python
def safe_terminate(process, timeout=10):
    """Safely terminate a process with escalation"""
    if process.poll() is not None:
        return  # Already terminated

    # Step 1: Try graceful termination
    process.terminate()

    try:
        process.wait(timeout=timeout)
        return
    except subprocess.TimeoutExpired:
        pass

    # Step 2: Force kill if graceful termination failed
    try:
        process.kill()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("Warning: Process may still be running")
```

## Signal Handling

### Signal Concepts

Signals are software interrupts sent to processes:

**Common Signals:**
- **SIGTERM (15)**: Termination request (graceful)
- **SIGKILL (9)**: Force termination (cannot be caught)
- **SIGINT (2)**: Interrupt (Ctrl+C)
- **SIGSTOP (19)**: Stop process execution
- **SIGCONT (18)**: Continue stopped process

### Sending Signals

```python
import os
import signal

def send_signal_to_process(pid, sig):
    """Send signal to process by PID"""
    try:
        os.kill(pid, sig)
        print(f"Signal {sig} sent to process {pid}")
    except ProcessLookupError:
        print(f"Process {pid} not found")
    except PermissionError:
        print(f"No permission to signal process {pid}")
```

### Signal Handling in Subprocesses

```python
def run_with_signal_handling(command, signal_handler=None):
    """Run command with custom signal handling"""

    def preexec():
        if signal_handler:
            signal.signal(signal.SIGTERM, signal_handler)
            signal.signal(signal.SIGINT, signal_handler)

    return subprocess.Popen(command, preexec_fn=preexec)
```

## Process Groups and Sessions

### Process Group Management

Organize related processes for collective control:

```python
# Create process in new group
process = subprocess.Popen(['command'], start_new_session=True)

# Get process group ID
pgid = os.getpgid(process.pid)

# Send signal to entire process group
os.killpg(pgid, signal.SIGTERM)
```

### Session Management

Create new sessions to isolate process groups:

```python
# Start process as session leader
process = subprocess.Popen(['command'], start_new_session=True)

# Process becomes session leader
sid = os.getsid(process.pid)
print(f"Session ID: {sid}")
```

## Timeout Management

### Execution Timeouts

Prevent processes from running indefinitely:

```python
# With subprocess.run()
try:
    result = subprocess.run(['command'], timeout=30)
    print("Command completed within timeout")
except subprocess.TimeoutExpired:
    print("Command timed out")

# With Popen
process = subprocess.Popen(['command'])

try:
    process.wait(timeout=30)
    print("Process completed within timeout")
except subprocess.TimeoutExpired:
    print("Process timed out")
    process.kill()
```

### Communication Timeouts

Set timeouts for I/O operations:

```python
process = subprocess.Popen(['command'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

try:
    stdout, stderr = process.communicate(timeout=10)
    print("Communication completed")
except subprocess.TimeoutExpired:
    print("Communication timed out")
    process.kill()
```

## Resource Management

### CPU Time Limits

```python
import resource

def run_with_cpu_limit(command, cpu_seconds=60):
    """Run command with CPU time limit"""

    def preexec():
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))

    return subprocess.Popen(command, preexec_fn=preexec)
```

### Memory Limits

```python
def run_with_memory_limit(command, memory_bytes=100*1024*1024):  # 100MB
    """Run command with memory limit"""

    def preexec():
        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))

    return subprocess.Popen(command, preexec_fn=preexec)
```

### Process Priority

```python
def run_with_priority(command, nice_level=10):
    """Run command with adjusted priority"""

    def preexec():
        os.nice(nice_level)

    return subprocess.Popen(command, preexec_fn=preexec)
```

## Advanced Process Control Patterns

### Process Supervisor

Monitor and restart processes automatically:

```python
class ProcessSupervisor:
    """Supervisor for managing process lifecycle"""

    def __init__(self, command, restart_on_failure=True):
        self.command = command
        self.restart_on_failure = restart_on_failure
        self.process = None
        self.restart_count = 0

    def start(self):
        """Start the supervised process"""
        if self.process and self.process.poll() is None:
            return  # Already running

        self.process = subprocess.Popen(self.command)
        print(f"Started process with PID: {self.process.pid}")

    def stop(self):
        """Stop the supervised process"""
        if self.process:
            self.safe_terminate(self.process)
            self.process = None

    def monitor(self):
        """Monitor process and restart if necessary"""
        if not self.process:
            self.start()
            return

        if self.process.poll() is not None:
            print(f"Process exited with code: {self.process.returncode}")

            if self.restart_on_failure and self.restart_count < 5:
                print("Restarting process...")
                self.restart_count += 1
                self.start()
            else:
                print("Process failed permanently")

    def safe_terminate(self, process, timeout=10):
        """Safely terminate a process"""
        process.terminate()
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
```

### Process Pool Manager

Manage multiple related processes:

```python
class ProcessPool:
    """Manager for a pool of processes"""

    def __init__(self, max_processes=4):
        self.max_processes = max_processes
        self.processes = []

    def add_process(self, command):
        """Add a process to the pool"""
        if len(self.processes) >= self.max_processes:
            self.wait_for_any()

        process = subprocess.Popen(command)
        self.processes.append(process)
        return process

    def wait_for_any(self):
        """Wait for any process to complete"""
        if not self.processes:
            return

        # Wait for first process to complete
        while self.processes:
            for i, process in enumerate(self.processes):
                if process.poll() is not None:
                    completed = self.processes.pop(i)
                    return completed

            time.sleep(0.1)

    def wait_all(self):
        """Wait for all processes to complete"""
        for process in self.processes:
            process.wait()
        self.processes.clear()

    def terminate_all(self):
        """Terminate all processes in pool"""
        for process in self.processes:
            try:
                process.terminate()
            except:
                pass

        # Wait for termination
        time.sleep(1)

        for process in self.processes:
            if process.poll() is None:
                process.kill()

        self.processes.clear()
```

### Context Manager for Process Control

```python
class ManagedProcess:
    """Context manager for automatic process cleanup"""

    def __init__(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        self.process = None

    def __enter__(self):
        self.process = subprocess.Popen(self.command, **self.kwargs)
        return self.process

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.process:
            self._cleanup_process()

    def _cleanup_process(self):
        """Clean up the process"""
        if self.process.poll() is None:
            # Try graceful termination first
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
                return
            except subprocess.TimeoutExpired:
                pass

            # Force kill if graceful termination failed
            try:
                self.process.kill()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Warning: Process may still be running")

# Usage
with ManagedProcess(['long_running_command']) as proc:
    # Process runs here, automatically cleaned up on exit
    output = proc.communicate(timeout=60)
```

## Cross-Platform Process Control

### Platform-Specific Signal Handling

```python
def cross_platform_terminate(process):
    """Terminate process in a cross-platform way"""
    try:
        if platform.system() == 'Windows':
            # Windows handles termination differently
            process.terminate()
            # Give it time to terminate
            process.wait(timeout=5)
        else:
            # Unix-like systems
            process.terminate()
            process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        # Force kill if termination didn't work
        process.kill()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Warning: Process may still be running")
```

### Windows-Specific Control

```python
import subprocess

if platform.system() == 'Windows':
    # Windows process creation flags
    creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
    process = subprocess.Popen(['command'], creationflags=creation_flags)

    # Windows uses different signal handling
    # SIGTERM equivalent
    process.terminate()
```

### Unix-Specific Control

```python
if platform.system() != 'Windows':
    # Send signal to process group
    def terminate_process_group(pgid):
        os.killpg(pgid, signal.SIGTERM)

    # Create process in new group
    process = subprocess.Popen(['command'], start_new_session=True)
    pgid = os.getpgid(process.pid)

    # Terminate entire group
    terminate_process_group(pgid)
```

## Error Handling in Process Control

### Robust Process Management

```python
def robust_process_control(command, timeout=30):
    """Robust process control with comprehensive error handling"""
    process = None

    try:
        # Start process
        process = subprocess.Popen(command,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

        # Wait with timeout
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return {
                'success': True,
                'returncode': process.returncode,
                'stdout': stdout,
                'stderr': stderr
            }
        except subprocess.TimeoutExpired:
            # Timeout occurred
            safe_terminate(process)
            return {
                'success': False,
                'error': 'timeout',
                'timeout': timeout
            }

    except FileNotFoundError:
        return {'success': False, 'error': 'command_not_found'}
    except PermissionError:
        return {'success': False, 'error': 'permission_denied'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        # Ensure process is cleaned up
        if process and process.poll() is None:
            safe_terminate(process)
```

### Logging Process Events

```python
import logging

class ProcessController:
    """Process controller with logging"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run_command(self, command, **kwargs):
        """Run command with logging"""
        self.logger.info(f"Starting command: {' '.join(command)}")

        try:
            process = subprocess.Popen(command, **kwargs)

            self.logger.info(f"Process started with PID: {process.pid}")

            # Monitor process
            while process.poll() is None:
                time.sleep(1)

            returncode = process.returncode
            self.logger.info(f"Process completed with code: {returncode}")

            return returncode

        except Exception as e:
            self.logger.error(f"Process failed: {e}")
            raise
```

This comprehensive guide covers all aspects of process control with `subprocess`, from basic monitoring to advanced lifecycle management, signal handling, and cross-platform considerations.
