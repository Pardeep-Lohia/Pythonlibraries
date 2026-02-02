# Input/Output Pipes with Subprocess

## Overview

Input/Output (I/O) pipes are fundamental to `subprocess` functionality, enabling communication between parent and child processes. This document covers stdin, stdout, stderr handling, piping between processes, and advanced I/O patterns.

## Standard Streams

### stdin (Standard Input)

#### Purpose
Provides input data to the subprocess.

#### Configuration Options
- **`subprocess.PIPE`**: Create a pipe for writing input
- **`subprocess.DEVNULL`**: Discard input (Unix) or NUL (Windows)
- **File object**: Redirect from a file
- **`None`**: Inherit from parent (default)

#### Examples

**Piping Input**
```python
import subprocess

# Send string input to command
process = subprocess.run(['grep', 'python'],
                        input='Python is great\nJava is good\n',
                        capture_output=True, text=True)
print(process.stdout)  # "Python is great"
```

**Input from File**
```python
with open('input.txt', 'r') as f:
    result = subprocess.run(['cat'], stdin=f, capture_output=True, text=True)
print(result.stdout)
```

**Interactive Input with Popen**
```python
process = subprocess.Popen(['python3', '-c', 'print(input("Enter: "))'],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          text=True)

stdout, stderr = process.communicate(input='Hello World\n')
print(stdout.strip())  # "Enter: Hello World"
```

### stdout (Standard Output)

#### Purpose
Captures output produced by the subprocess.

#### Configuration Options
- **`subprocess.PIPE`**: Capture output in pipe
- **`subprocess.DEVNULL`**: Discard output
- **File object**: Redirect to a file
- **`None`**: Inherit from parent (default)

#### Examples

**Capture Output**
```python
result = subprocess.run(['echo', 'Hello'], capture_output=True, text=True)
print(result.stdout.strip())  # "Hello"
```

**Redirect to File**
```python
with open('output.txt', 'w') as f:
    subprocess.run(['ls', '-la'], stdout=f)
```

**Live Output Streaming**
```python
process = subprocess.Popen(['ping', '-c', '3', 'google.com'],
                          stdout=subprocess.PIPE, text=True)

while True:
    line = process.stdout.readline()
    if not line and process.poll() is not None:
        break
    if line:
        print(line.strip())
```

### stderr (Standard Error)

#### Purpose
Captures error messages from the subprocess.

#### Configuration Options
- **`subprocess.PIPE`**: Capture error output
- **`subprocess.DEVNULL`**: Discard errors
- **`subprocess.STDOUT`**: Merge stderr with stdout
- **File object**: Redirect to a file
- **`None`**: Inherit from parent (default)

#### Examples

**Separate Error Handling**
```python
result = subprocess.run(['ls', 'nonexistent'],
                       capture_output=True, text=True)
print(f"Output: {result.stdout}")
print(f"Errors: {result.stderr}")
print(f"Return code: {result.returncode}")
```

**Merge stdout and stderr**
```python
result = subprocess.run(['command'],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT,
                       text=True)
# Both stdout and stderr in result.stdout
```

**Redirect Errors to File**
```python
with open('errors.log', 'w') as f:
    subprocess.run(['command'], stderr=f)
```

## Pipe Communication Patterns

### Basic Piping

#### Command to Command Piping
```python
# Manual piping: command1 | command2
p1 = subprocess.Popen(['echo', 'hello world'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', 'hello'], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()  # Allow p1 to receive SIGPIPE
output = p2.communicate()[0]
```

#### Using shell for piping (not recommended)
```python
# Avoid this for security reasons
result = subprocess.run('echo "hello" | grep "hello"',
                       shell=True, capture_output=True, text=True)
```

### Advanced Pipe Patterns

#### Pipeline Builder
```python
class Pipeline:
    def __init__(self, *commands):
        self.commands = commands
        self.processes = []

    def run(self):
        prev_stdout = None
        for i, cmd in enumerate(self.commands):
            stdin = prev_stdout
            stdout = subprocess.PIPE if i < len(self.commands) - 1 else None

            process = subprocess.Popen(cmd,
                                     stdin=stdin,
                                     stdout=stdout,
                                     stderr=subprocess.PIPE)
            self.processes.append(process)
            prev_stdout = process.stdout

        # Close the first process's stdout to allow SIGPIPE
        if self.processes:
            self.processes[0].stdout.close()

        # Wait for all processes
        results = []
        for process in self.processes:
            stdout, stderr = process.communicate()
            results.append({
                'returncode': process.returncode,
                'stdout': stdout,
                'stderr': stderr
            })

        return results

# Usage
pipeline = Pipeline(['echo', 'hello world'],
                   ['grep', 'hello'],
                   ['wc', '-l'])
results = pipeline.run()
```

#### Bidirectional Communication
```python
process = subprocess.Popen(['python3', '-c', '''
import sys
while True:
    line = sys.stdin.readline()
    if not line:
        break
    sys.stdout.write(f"Processed: {line.upper()}")
    sys.stdout.flush()
'''],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          text=True)

# Send multiple inputs
inputs = ['hello', 'world', 'test']
for inp in inputs:
    process.stdin.write(inp + '\n')
    process.stdin.flush()
    response = process.stdout.readline()
    print(f"Sent: {inp}, Received: {response.strip()}")

process.stdin.close()
process.wait()
```

## File Redirection

### Redirecting to/from Files

#### Input from File
```python
with open('input.txt', 'r') as infile:
    result = subprocess.run(['cat'], stdin=infile, capture_output=True)
```

#### Output to File
```python
with open('output.txt', 'w') as outfile:
    subprocess.run(['ls', '-la'], stdout=outfile)
```

#### Append to File
```python
with open('log.txt', 'a') as logfile:
    subprocess.run(['echo', 'log message'], stdout=logfile)
```

#### Simultaneous File and Pipe
```python
with open('output.txt', 'w') as outfile:
    result = subprocess.run(['command'],
                           stdout=outfile,
                           stderr=subprocess.PIPE,
                           text=True)
    # stdout goes to file, stderr captured in result.stderr
```

### Temporary Files for Large Data
```python
import tempfile

def process_large_data(data):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(data)
        tmp.flush()

        # Process the temporary file
        result = subprocess.run(['cat', tmp.name], capture_output=True, text=True)

    # Clean up
    os.unlink(tmp.name)
    return result.stdout
```

## DEVNULL Usage

### Discarding Output
```python
# Discard both stdout and stderr
result = subprocess.run(['command'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

# Silent execution
subprocess.run(['command'], capture_output=False)  # Output goes to console
```

### Conditional Output
```python
def run_quietly(cmd, quiet=False):
    stdout = subprocess.DEVNULL if quiet else None
    stderr = subprocess.DEVNULL if quiet else None
    return subprocess.run(cmd, stdout=stdout, stderr=stderr)
```

## Text vs Binary Mode

### Text Mode Handling
```python
# Text mode (Python 3.7+)
result = subprocess.run(['echo', 'hello'],
                       capture_output=True, text=True)
print(result.stdout)  # String

# Binary mode
result = subprocess.run(['echo', 'hello'],
                       capture_output=True)
print(result.stdout)  # Bytes
```

### Encoding Considerations
```python
# Specify encoding
result = subprocess.run(['command'],
                       capture_output=True,
                       encoding='utf-8')

# Handle encoding errors
result = subprocess.run(['command'],
                       capture_output=True,
                       encoding='utf-8',
                       errors='replace')
```

## Advanced I/O Patterns

### Non-blocking I/O
```python
import select
import fcntl
import os

def make_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

process = subprocess.Popen(['long_running_command'],
                          stdout=subprocess.PIPE)

make_nonblocking(process.stdout.fileno())

while True:
    ready, _, _ = select.select([process.stdout], [], [], 0.1)
    if ready:
        data = process.stdout.read(1024)
        if not data:
            break
        print(data.decode(), end='')
    if process.poll() is not None:
        break
```

### Buffered I/O
```python
# Line-buffered reading
process = subprocess.Popen(['command'],
                          stdout=subprocess.PIPE,
                          bufsize=1,  # Line buffered
                          text=True)

for line in process.stdout:
    print(f"Received: {line.strip()}")
```

### Timeout-based I/O
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("I/O timeout")

process = subprocess.Popen(['slow_command'],
                          stdout=subprocess.PIPE)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)  # 5 second timeout

try:
    output, _ = process.communicate()
    signal.alarm(0)  # Cancel alarm
except TimeoutError:
    process.kill()
    print("Command timed out")
```

## Error Handling in I/O Operations

### Pipe Errors
```python
try:
    process = subprocess.Popen(['command'],
                              stdout=subprocess.PIPE)
    output, error = process.communicate(timeout=10)
except subprocess.TimeoutExpired:
    process.kill()
    print("Process timed out")
except BrokenPipeError:
    print("Broken pipe - process may have exited")
except OSError as e:
    print(f"I/O error: {e}")
```

### Buffer Overflow Prevention
```python
def safe_communicate(process, input_data=None, timeout=None):
    try:
        if input_data:
            # Write input in chunks to avoid buffer issues
            chunk_size = 8192
            for i in range(0, len(input_data), chunk_size):
                chunk = input_data[i:i + chunk_size]
                process.stdin.write(chunk)
                process.stdin.flush()

            process.stdin.close()

        # Read output in chunks
        output_chunks = []
        while True:
            chunk = process.stdout.read(8192)
            if not chunk:
                break
            output_chunks.append(chunk)

        return b''.join(output_chunks)

    except (BrokenPipeError, OSError) as e:
        print(f"I/O error: {e}")
        return None
```

## Cross-Platform I/O Considerations

### Line Ending Handling
```python
# Handle different line endings
result = subprocess.run(['command'],
                       capture_output=True, text=True)

# Normalize line endings
normalized = result.stdout.replace('\r\n', '\n').replace('\r', '\n')
```

### Path Encoding
```python
import locale

# Use system encoding for file paths
encoding = locale.getpreferredencoding(False)

result = subprocess.run(['ls', '/path/with/unicode/characters'],
                       capture_output=True,
                       encoding=encoding)
```

## Performance Optimization

### I/O Buffering
```python
# Use appropriate buffer sizes
process = subprocess.Popen(['cat', 'large_file'],
                          stdout=subprocess.PIPE,
                          bufsize=8192)  # 8KB buffer

# For line-based processing
for line in iter(process.stdout.readline, b''):
    process_line(line)
```

### Memory-efficient Streaming
```python
def stream_process_output(cmd, chunk_size=8192):
    """Stream process output to avoid loading large data in memory"""
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    while True:
        chunk = process.stdout.read(chunk_size)
        if not chunk:
            break
        yield chunk

    process.wait()

# Usage
for chunk in stream_process_output(['cat', 'large_file.txt']):
    process_chunk(chunk)
```

### Concurrent I/O
```python
import threading

def read_output(process, output_list):
    for line in iter(process.stdout.readline, b''):
        output_list.append(line.decode().strip())

process = subprocess.Popen(['long_command'],
                          stdout=subprocess.PIPE)

output = []
thread = threading.Thread(target=read_output, args=(process, output))
thread.start()

# Do other work while reading output
do_other_work()

thread.join()
print("All output:", output)
```

## Security Considerations

### Input Validation
```python
def safe_pipe_input(cmd, input_data):
    # Validate input data
    if not isinstance(input_data, str):
        raise ValueError("Input must be string")

    # Limit input size
    max_size = 1024 * 1024  # 1MB limit
    if len(input_data) > max_size:
        raise ValueError("Input too large")

    return subprocess.run(cmd,
                         input=input_data,
                         capture_output=True,
                         text=True)
```

### Output Sanitization
```python
import html

def sanitize_output(output):
    # Escape HTML characters if output will be displayed in web interface
    return html.escape(output)

result = subprocess.run(['command'], capture_output=True, text=True)
safe_output = sanitize_output(result.stdout)
```

This comprehensive guide covers all aspects of input/output pipe management in `subprocess`, from basic usage to advanced patterns and performance optimization.
