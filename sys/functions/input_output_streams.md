# Input/Output Streams (`sys.stdin`, `sys.stdout`, `sys.stderr`)

## Purpose
`sys` provides access to the standard input, output, and error streams, allowing programs to read from and write to these streams, which are fundamental for console-based applications and data pipelines.

## Key Streams

### `sys.stdin`
- **Purpose**: Standard input stream for reading data
- **Type**: TextIOWrapper (file-like object)
- **Default**: Connected to keyboard input or piped input

### `sys.stdout`
- **Purpose**: Standard output stream for normal program output
- **Type**: TextIOWrapper (file-like object)
- **Default**: Connected to console/terminal output

### `sys.stderr`
- **Purpose**: Standard error stream for error messages and diagnostics
- **Type**: TextIOWrapper (file-like object)
- **Default**: Connected to console/terminal error output

## Syntax
```python
import sys

# Reading from stdin
input_data = sys.stdin.read()
line = sys.stdin.readline()

# Writing to stdout
sys.stdout.write("Hello, World!\n")
print("Hello, World!", file=sys.stdout)

# Writing to stderr
sys.stderr.write("Error message\n")
print("Error message", file=sys.stderr)
```

## Examples

### Basic Stream Operations
```python
import sys

def demonstrate_streams():
    # Write to stdout
    sys.stdout.write("This is standard output\n")

    # Write to stderr
    sys.stderr.write("This is standard error\n")

    # Read from stdin
    sys.stdout.write("Enter your name: ")
    sys.stdout.flush()  # Ensure prompt appears
    name = sys.stdin.readline().strip()

    sys.stdout.write(f"Hello, {name}!\n")

demonstrate_streams()
```

### Line-by-Line Processing
```python
import sys

def process_lines():
    """Process input line by line"""
    line_number = 1
    for line in sys.stdin:
        # Remove trailing newline
        line = line.rstrip('\n')
        # Process the line
        processed = f"{line_number}: {line.upper()}"
        sys.stdout.write(processed + '\n')
        line_number += 1

if __name__ == "__main__":
    process_lines()
```

**Usage:**
```bash
echo -e "hello\nworld" | python script.py
```

### Stream Redirection
```python
import sys

def redirect_example():
    # Save original streams
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Redirect stdout to file
    with open('output.log', 'w') as f:
        sys.stdout = f
        print("This goes to the log file")

    # Redirect stderr to different file
    with open('errors.log', 'w') as f:
        sys.stderr = f
        print("This error goes to errors.log", file=sys.stderr)

    # Restore original streams
    sys.stdout = original_stdout
    sys.stderr = original_stderr

    print("Back to normal output")

redirect_example()
```

### Custom Stream Classes
```python
import sys
from io import StringIO

class UppercaseWriter:
    """A custom writer that converts text to uppercase"""
    def __init__(self, stream):
        self.stream = stream

    def write(self, text):
        self.stream.write(text.upper())

    def flush(self):
        self.stream.flush()

def custom_stream_example():
    # Create a string buffer
    buffer = StringIO()

    # Wrap it with uppercase writer
    upper_writer = UppercaseWriter(buffer)

    # Temporarily redirect stdout
    original_stdout = sys.stdout
    sys.stdout = upper_writer

    print("hello world")
    print("this will be uppercase")

    # Restore
    sys.stdout = original_stdout

    # Show result
    print("Buffered output:", repr(buffer.getvalue()))

custom_stream_example()
```

## Edge Cases

### Binary Data Handling
```python
import sys
import os

def binary_streams():
    # For binary data, use buffered readers/writers
    if hasattr(sys.stdout, 'buffer'):
        # Python 3: access binary buffer
        binary_stdout = sys.stdout.buffer
        binary_stdout.write(b"Binary data\n")

    # Check if streams support binary mode
    print(f"stdin binary: {hasattr(sys.stdin, 'buffer')}")
    print(f"stdout binary: {hasattr(sys.stdout, 'buffer')}")

binary_streams()
```

### Closed Streams
```python
import sys

def handle_closed_streams():
    try:
        # This might fail if stdin is closed
        data = sys.stdin.read(1)
    except OSError as e:
        sys.stderr.write(f"Error reading stdin: {e}\n")
        return

    if not data:
        sys.stderr.write("EOF reached on stdin\n")
        return

    sys.stdout.write(f"Read: {repr(data)}\n")

handle_closed_streams()
```

### Encoding Issues
```python
import sys

def encoding_example():
    # Check stream encoding
    print(f"stdin encoding: {getattr(sys.stdin, 'encoding', 'unknown')}")
    print(f"stdout encoding: {getattr(sys.stdout, 'encoding', 'unknown')}")

    # Handle encoding errors
    try:
        text = "café"
        sys.stdout.write(text + '\n')
    except UnicodeEncodeError as e:
        sys.stderr.write(f"Encoding error: {e}\n")
        # Fallback to ASCII-safe output
        sys.stdout.write(text.encode('ascii', 'replace').decode('ascii') + '\n')

encoding_example()
```

## Common Patterns

### Progress Indicators
```python
import sys
import time

def progress_example():
    for i in range(10):
        sys.stdout.write(f"\rProgress: {i+1}/10")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\nDone!\n")

progress_example()
```

### Error Logging
```python
import sys

def log_error(message, error_code=1):
    """Log error message to stderr and exit"""
    sys.stderr.write(f"ERROR: {message}\n")
    sys.exit(error_code)

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        log_error("Division by zero")
    except TypeError:
        log_error("Invalid types for division")

result = safe_divide(10, 0)  # Will log error and exit
```

### Pipeline Processing
```python
import sys
import json

def json_processor():
    """Process JSON lines from stdin to stdout"""
    for line_num, line in enumerate(sys.stdin, 1):
        line = line.strip()
        if not line:
            continue

        try:
            data = json.loads(line)
            # Process the data
            data['processed'] = True
            data['line_number'] = line_num

            # Output processed JSON
            json.dump(data, sys.stdout)
            sys.stdout.write('\n')

        except json.JSONDecodeError as e:
            sys.stderr.write(f"Line {line_num}: Invalid JSON - {e}\n")
            continue

if __name__ == "__main__":
    json_processor()
```

## Best Practices

1. **Always flush after writing prompts** to ensure they appear before reading input
2. **Use stderr for errors**, stdout for normal output to allow proper redirection
3. **Handle encoding issues** gracefully, especially in cross-platform code
4. **Restore original streams** after temporary redirection
5. **Check for stream availability** before operations (especially in restricted environments)
6. **Use context managers** for temporary stream redirection

## Performance Considerations

- **Buffering**: Streams are buffered by default; use `flush()` for immediate output
- **Binary vs Text**: Use binary buffers for large data transfers
- **Line buffering**: Consider using `sys.stdout.reconfigure(line_buffering=True)` for line-buffered output

## Comparison with Built-in Functions

| Operation | `sys.stdout` | `print()` |
|-----------|--------------|-----------|
| Basic output | `sys.stdout.write("text")` | `print("text")` |
| No newline | `sys.stdout.write("text")` | `print("text", end="")` |
| File output | `print("text", file=f)` | `sys.stdout = f; print("text")` |
| Formatting | Manual | Built-in sep/end parameters |

`print()` is more convenient for simple output, while `sys` streams offer more control for advanced use cases.
