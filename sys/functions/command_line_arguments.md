# Command Line Arguments (`sys.argv`)

## Purpose
`sys.argv` provides access to command-line arguments passed to a Python script when executed from the terminal or command prompt.

## Syntax
```python
import sys

# Access command line arguments
arguments = sys.argv  # Returns a list of strings
script_name = sys.argv[0]  # First element is script name
first_arg = sys.argv[1]  # Subsequent elements are arguments
```

## Description
- `sys.argv` is a list containing the command-line arguments
- The first element (`sys.argv[0]`) is always the script name or path
- Subsequent elements are the arguments passed to the script
- Arguments are always strings, even if they look like numbers

## Examples

### Basic Usage
```python
#!/usr/bin/env python3
import sys

def main():
    print(f"Script name: {sys.argv[0]}")
    print(f"Number of arguments: {len(sys.argv) - 1}")

    if len(sys.argv) > 1:
        print("Arguments:")
        for i, arg in enumerate(sys.argv[1:], 1):
            print(f"  {i}: {arg}")

if __name__ == "__main__":
    main()
```

**Execution:**
```bash
python script.py hello world 123
```

**Output:**
```
Script name: script.py
Number of arguments: 3
Arguments:
  1: hello
  2: world
  3: 123
```

### Argument Validation
```python
import sys

def validate_args():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Input: {input_file}")
    print(f"Output: {output_file}")

validate_args()
```

### Type Conversion
```python
import sys

def process_numbers():
    if len(sys.argv) < 2:
        print("Usage: python script.py <number1> <number2> ...")
        return

    numbers = []
    for arg in sys.argv[1:]:
        try:
            num = float(arg)
            numbers.append(num)
        except ValueError:
            print(f"Error: '{arg}' is not a valid number")
            return

    total = sum(numbers)
    average = total / len(numbers)
    print(f"Numbers: {numbers}")
    print(f"Sum: {total}")
    print(f"Average: {average}")

process_numbers()
```

## Edge Cases

### No Arguments
```python
import sys

# Always safe to access
script_name = sys.argv[0]  # Always exists
arg_count = len(sys.argv) - 1  # May be 0

if arg_count == 0:
    print("No arguments provided")
```

### Arguments with Spaces
Arguments containing spaces must be quoted when passed:
```bash
python script.py "hello world" "foo bar"
```

### Special Characters
```python
import sys

# Arguments with special characters
for arg in sys.argv[1:]:
    print(f"Raw argument: {repr(arg)}")
```

**Execution:**
```bash
python script.py "hello\nworld" "path\to\file"
```

**Output:**
```
Raw argument: 'hello\nworld'
Raw argument: 'path\\to\\file'
```

## Common Patterns

### Optional Arguments
```python
import sys

def flexible_script():
    verbose = False
    input_file = None

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-v' or sys.argv[i] == '--verbose':
            verbose = True
        elif sys.argv[i] == '-i' or sys.argv[i] == '--input':
            i += 1
            if i < len(sys.argv):
                input_file = sys.argv[i]
        else:
            print(f"Unknown argument: {sys.argv[i]}")
            sys.exit(1)
        i += 1

    if verbose:
        print("Verbose mode enabled")

    if input_file:
        print(f"Input file: {input_file}")
```

### Argument Parsing Helper
```python
import sys

def get_arg_value(flag, default=None):
    """Get value for a flag argument like -f value or --flag value"""
    try:
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    except ValueError:
        pass
    return default

# Usage
filename = get_arg_value('-f', 'default.txt')
count = int(get_arg_value('-c', '1'))
```

## Best Practices

1. **Always validate argument count** before accessing `sys.argv[1]`
2. **Provide usage messages** when arguments are invalid
3. **Use meaningful variable names** instead of `sys.argv[1]`
4. **Consider using `argparse`** for complex argument parsing
5. **Handle type conversion errors** gracefully
6. **Document expected arguments** in docstrings or help messages

## Comparison with `argparse`

| Feature | `sys.argv` | `argparse` |
|---------|------------|------------|
| Complexity | Simple | Advanced |
| Type conversion | Manual | Automatic |
| Help generation | Manual | Automatic |
| Validation | Manual | Automatic |
| Default values | Manual | Automatic |
| Short options | Manual | Built-in |

Use `sys.argv` for simple scripts, `argparse` for complex command-line interfaces.
