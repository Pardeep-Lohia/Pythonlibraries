# Coding Questions

This section contains practical coding challenges and solutions related to the `sys` module, designed to test understanding of Python's runtime environment and system interactions.

## Beginner Level

### Challenge 1: CLI Argument Parser

**Problem:** Create a command-line script that accepts a name and age as arguments, validates them, and displays a personalized greeting. Use only the `sys` module for argument parsing.

**Requirements:**
- Accept exactly 2 arguments: name and age
- Validate that age is a positive integer
- Display appropriate error messages and exit codes
- Show usage information when arguments are missing

**Solution:**
```python
#!/usr/bin/env python3
import sys

def main():
    # Check argument count
    if len(sys.argv) != 3:
        sys.stderr.write(f"Usage: {sys.argv[0]} <name> <age>\n")
        sys.exit(1)

    name = sys.argv[1]
    age_str = sys.argv[2]

    # Validate age
    try:
        age = int(age_str)
        if age <= 0:
            raise ValueError("Age must be positive")
    except ValueError:
        sys.stderr.write("Error: Age must be a positive integer\n")
        sys.exit(1)

    # Display greeting
    sys.stdout.write(f"Hello, {name}! You are {age} years old.\n")

if __name__ == "__main__":
    main()
```

**Key Concepts Tested:**
- `sys.argv` for argument access
- `sys.stderr` and `sys.stdout` for proper output streams
- `sys.exit()` for controlled termination
- Argument validation and error handling

### Challenge 2: Version Checker

**Problem:** Write a script that checks if the current Python version meets minimum requirements and exits with appropriate status codes.

**Requirements:**
- Accept minimum version as command-line argument (e.g., "3.8")
- Compare against current Python version
- Exit with code 0 if compatible, 1 if not
- Display informative messages

**Solution:**
```python
#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <min_version>\n")
        sys.stderr.write("Example: python version_check.py 3.8\n")
        sys.exit(1)

    min_version_str = sys.argv[1]

    # Parse minimum version
    try:
        major, minor = map(int, min_version_str.split('.'))
        min_version = (major, minor)
    except ValueError:
        sys.stderr.write("Error: Version must be in format 'major.minor'\n")
        sys.exit(1)

    current_version = sys.version_info[:2]

    print(f"Current Python version: {sys.version_info.major}.{sys.version_info.minor}")
    print(f"Required minimum version: {major}.{minor}")

    if current_version >= min_version:
        print("✓ Version check passed")
        sys.exit(0)
    else:
        print("✗ Version check failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Key Concepts Tested:**
- `sys.version_info` for version checking
- Version comparison logic
- Exit codes for different outcomes

## Intermediate Level

### Challenge 3: Memory Usage Monitor

**Problem:** Create a script that monitors memory usage of a file processing operation and reports the results.

**Requirements:**
- Load and process a text file
- Track memory usage before and after operations
- Display memory statistics
- Handle file errors gracefully

**Solution:**
```python
#!/usr/bin/env python3
import sys
import gc

def get_memory_usage():
    """Get current memory allocation in blocks"""
    return sys.getallocatedblocks()

def process_file(filename):
    """Process a text file and return statistics"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.splitlines()
        words = content.split()
        chars = len(content)

        # Create word frequency dictionary
        word_freq = {}
        for word in words:
            word = word.lower().strip('.,!?')
            word_freq[word] = word_freq.get(word, 0) + 1

        return {
            'lines': len(lines),
            'words': len(words),
            'characters': chars,
            'unique_words': len(word_freq),
            'most_common': max(word_freq.items(), key=lambda x: x[1]) if word_freq else None
        }

    except FileNotFoundError:
        sys.stderr.write(f"Error: File '{filename}' not found\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error processing file: {e}\n")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <filename>\n")
        sys.exit(1)

    filename = sys.argv[1]

    # Memory monitoring
    gc.collect()  # Clean up before measurement
    initial_memory = get_memory_usage()

    print(f"Initial memory usage: {initial_memory} blocks")

    # Process file
    stats = process_file(filename)

    final_memory = get_memory_usage()
    memory_used = final_memory - initial_memory

    # Display results
    print(f"\nFile: {filename}")
    print(f"Lines: {stats['lines']}")
    print(f"Words: {stats['words']}")
    print(f"Characters: {stats['characters']}")
    print(f"Unique words: {stats['unique_words']}")

    if stats['most_common']:
        word, count = stats['most_common']
        print(f"Most common word: '{word}' ({count} times)")

    print(f"\nMemory used: {memory_used} blocks")

if __name__ == "__main__":
    main()
```

**Key Concepts Tested:**
- `sys.getallocatedblocks()` for memory monitoring
- Memory profiling techniques
- File I/O with error handling

### Challenge 4: Stream Redirector

**Problem:** Implement a context manager that temporarily redirects stdout and stderr to files, with options for append mode and error logging.

**Requirements:**
- Create a context manager class
- Support separate files for stdout and stderr
- Option to append or overwrite files
- Restore original streams automatically
- Handle exceptions properly

**Solution:**
```python
#!/usr/bin/env python3
import sys
import os
from contextlib import contextmanager

class StreamRedirector:
    """Context manager for redirecting stdout and stderr"""

    def __init__(self, stdout_file=None, stderr_file=None, append=False):
        self.stdout_file = stdout_file
        self.stderr_file = stderr_file
        self.append = append
        self.original_stdout = None
        self.original_stderr = None
        self.stdout_handle = None
        self.stderr_handle = None

    def __enter__(self):
        # Save original streams
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        # Open files if specified
        mode = 'a' if self.append else 'w'

        if self.stdout_file:
            self.stdout_handle = open(self.stdout_file, mode, encoding='utf-8')
            sys.stdout = self.stdout_handle

        if self.stderr_file:
            self.stderr_handle = open(self.stderr_file, mode, encoding='utf-8')
            sys.stderr = self.stderr_handle

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original streams
        if self.stdout_handle:
            self.stdout_handle.close()
        if self.stderr_handle:
            self.stderr_handle.close()

        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

        # Don't suppress exceptions
        return False

@contextmanager
def redirect_streams(stdout_file=None, stderr_file=None, append=False):
    """Context manager function for stream redirection"""
    with StreamRedirector(stdout_file, stderr_file, append) as redirector:
        yield redirector

def demo_stream_redirection():
    """Demonstrate stream redirection functionality"""
    print("1. Normal output (to console)")
    print("This should appear on console")

    with redirect_streams(stdout_file='output.log'):
        print("2. Redirected output (to file)")
        print("This should go to output.log")

    print("3. Back to console")
    print("This should appear on console again")

    # Separate stdout and stderr
    with StreamRedirector(stdout_file='stdout.log', stderr_file='stderr.log'):
        print("4. Separate streams")
        print("This goes to stdout.log")
        sys.stderr.write("This error goes to stderr.log\n")

    print("5. Append mode")
    with redirect_streams(stdout_file='output.log', append=True):
        print("This should be appended to output.log")

    # Error handling
    try:
        with redirect_streams(stdout_file='/invalid/path/output.log'):
            print("This will fail")
    except Exception as e:
        print(f"Handled error: {e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo_stream_redirection()
    else:
        print("Stream Redirection Demo")
        print("Usage: python stream_redirector.py demo")
        print("This will create log files in the current directory")

if __name__ == "__main__":
    main()
```

**Key Concepts Tested:**
- `sys.stdout` and `sys.stderr` manipulation
- Context manager implementation
- File handling with proper cleanup
- Exception handling in context managers

### Challenge 5: Recursive Memory Calculator

**Problem:** Implement a function that calculates the total memory usage of nested Python objects, handling circular references.

**Requirements:**
- Recursively traverse object structures
- Avoid infinite loops with circular references
- Handle different object types (lists, dicts, custom objects)
- Provide both shallow and deep memory analysis

**Solution:**
```python
#!/usr/bin/env python3
import sys

def get_deep_size(obj, seen=None):
    """Calculate total memory usage of an object and its contents"""
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0  # Avoid circular references

    seen.add(obj_id)
    size = sys.getsizeof(obj)

    # Handle different object types
    if isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(get_deep_size(item, seen) for item in obj)
    elif isinstance(obj, dict):
        size += sum(get_deep_size(k, seen) + get_deep_size(v, seen)
                   for k, v in obj.items())
    elif hasattr(obj, '__dict__'):
        size += get_deep_size(obj.__dict__, seen)

    return size

def analyze_object_memory(obj, name="object"):
    """Analyze memory usage of an object"""
    shallow_size = sys.getsizeof(obj)
    deep_size = get_deep_size(obj)

    print(f"\nMemory analysis for {name}:")
    print(f"  Shallow size: {shallow_size} bytes")
    print(f"  Deep size: {deep_size} bytes")
    print(f"  Content overhead: {deep_size - shallow_size} bytes")

    return deep_size

def main():
    # Test with various data structures
    test_cases = [
        ("empty list", []),
        ("small list", [1, 2, 3, 4, 5]),
        ("nested list", [[1, 2], [3, 4], [5, 6]]),
        ("dictionary", {'a': 1, 'b': [1, 2, 3], 'c': {'nested': True}}),
        ("mixed structure", {
            'numbers': list(range(10)),
            'text': ['hello'] * 5,
            'nested': {'deep': {'deeper': [1, 2, 3] * 3}}
        }),
    ]

    for name, obj in test_cases:
        analyze_object_memory(obj, name)

    # Test circular reference handling
    print("\nTesting circular reference handling:")

    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    node1 = Node(1)
    node2 = Node(2)
    node1.next = node2
    node2.next = node1  # Circular reference

    try:
        circular_size = get_deep_size(node1)
        print(f"Circular reference handled successfully: {circular_size} bytes")
    except RecursionError:
        print("Error: Circular reference caused recursion error")

if __name__ == "__main__":
    main()
```

**Key Concepts Tested:**
- `sys.getsizeof()` for memory measurement
- Recursive algorithms with cycle detection
- Object introspection techniques
- Memory analysis patterns

### Challenge 6: Reference Counting Explorer

**Problem:** Create a script that demonstrates reference counting behavior and helps understand object lifetime.

**Requirements:**
- Show how reference counts change with different operations
- Demonstrate the effect of containers and function calls
- Explain when objects get garbage collected

**Solution:**
```python
#!/usr/bin/env python3
import sys
import gc

def show_refcount(obj, operation="current"):
    """Display reference count for an object"""
    count = sys.getrefcount(obj)
    print(f"Reference count after '{operation}': {count}")
    return count

def demonstrate_references():
    """Demonstrate reference counting behavior"""
    print("Reference Counting Demonstration")
    print("=" * 40)

    # Create an object
    print("\n1. Object Creation")
    test_obj = [1, 2, 3, "hello"]
    show_refcount(test_obj, "creation")

    # Create additional references
    print("\n2. Creating Additional References")
    ref1 = test_obj
    show_refcount(test_obj, "creating ref1")

    ref2 = test_obj
    show_refcount(test_obj, "creating ref2")

    # Add to container
    print("\n3. Adding to Container")
    container = [test_obj]
    show_refcount(test_obj, "adding to list")

    # Dictionary
    dict_container = {'key': test_obj}
    show_refcount(test_obj, "adding to dict")

    # Function call (temporary reference)
    print("\n4. Function Call Effects")
    show_refcount(test_obj, "before function call")
    result = show_refcount(test_obj, "inside function call")
    show_refcount(test_obj, "after function call")

    # Delete references
    print("\n5. Deleting References")
    del ref1
    show_refcount(test_obj, "deleting ref1")

    del ref2
    show_refcount(test_obj, "deleting ref2")

    del container[0]
    show_refcount(test_obj, "removing from list")

    del dict_container['key']
    show_refcount(test_obj, "removing from dict")

    # Test garbage collection
    print("\n6. Garbage Collection")
    obj_id = id(test_obj)
    print(f"Object ID before deletion: {obj_id}")

    del test_obj
    print("Object deleted, running garbage collection...")

    collected = gc.collect()
    print(f"Objects collected by GC: {collected}")

def reference_counting_quiz():
    """Interactive quiz about reference counting"""
    questions = [
        {
            'question': "What happens to an object's reference count when you add it to a list?",
            'options': [
                "It stays the same",
                "It increases by 1",
                "It decreases by 1",
                "It becomes zero"
            ],
            'correct': 1,
            'explanation': "Adding an object to a container increases its reference count by 1."
        },
        {
            'question': "When does Python garbage collect an object?",
            'options': [
                "Immediately when del is called",
                "When its reference count reaches zero",
                "Only at program exit",
                "When memory is low"
            ],
            'correct': 1,
            'explanation': "Python uses reference counting, so objects are collected when their reference count reaches zero."
        },
        {
            'question': "What does sys.getrefcount() include in its count?",
            'options': [
                "Only explicit references in your code",
                "All references including temporary ones",
                "Only references to the object itself",
                "References in other threads only"
            ],
            'correct': 1,
            'explanation': "sys.getrefcount() counts all references, including the temporary reference created by the function call itself."
        }
    ]

    print("\nReference Counting Quiz")
    print("=" * 25)

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"  {j+1}. {option}")

        while True:
            try:
                answer = int(input("Your answer (1-4): ")) - 1
                if 0 <= answer < len(q['options']):
                    break
                else:
                    print("Please enter 1-4")
            except ValueError:
                print("Please enter a number")

        if answer == q['correct']:
            print("✓ Correct!")
            score += 1
        else:
            print("✗ Incorrect")

        print(f"Explanation: {q['explanation']}")

    print(f"\nFinal score: {score}/{len(questions)}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'quiz':
        reference_counting_quiz()
    else:
        demonstrate_references()
        print("\n" + "="*50)
        print("Run with 'quiz' argument for interactive quiz:")
        print("python reference_explorer.py quiz")

if __name__ == "__main__":
    main()
```

**Key Concepts Tested:**
- `sys.getrefcount()` usage and interpretation
- Reference counting mechanics
- Object lifetime management
- Garbage collection interaction

## Advanced Level

### Challenge 7: Module Path Inspector

**Problem:** Create a comprehensive tool for inspecting and managing Python's module search path.

**Requirements:**
- Display all paths in `sys.path`
- Check which paths exist and are readable
- Allow adding/removing paths
- Show module loading statistics

**Solution:**
```python
#!/usr/bin/env python3
import sys
import os
from pathlib import Path

class ModulePathInspector:
    """Tool for inspecting and managing sys.path"""

    def __init__(self):
        self.original_path = sys.path.copy()

    def display_path_info(self):
        """Display detailed information about sys.path"""
        print("Python Module Search Path Analysis")
        print("=" * 40)

        for i, path in enumerate(sys.path):
            path_obj = Path(path)
            exists = path_obj.exists()
            is_dir = path_obj.is_dir() if exists else False
            readable = os.access(path, os.R_OK) if exists else False

            status = "✓" if exists and readable else "✗"

            print(f"{i:2d}. {status} {path}")
            if exists:
                if is_dir:
                    try:
                        items = len(list(path_obj.iterdir()))
                        print(f"      Directory with {items} items")
                    except PermissionError:
                        print("      Directory (permission denied)")
                else:
                    print("      File (not a directory)"
            else:
                print("      Path does not exist"
        print(f"\nTotal paths: {len(sys.path)}")

    def analyze_path_effectiveness(self):
        """Analyze how effective the current path configuration is"""
        print("\nPath Effectiveness Analysis")
        print("=" * 30)

        total_paths = len(sys.path)
        existing_paths = 0
        readable_paths = 0
        python_packages = 0

        for path in sys.path:
            path_obj = Path(path)
            if path_obj.exists():
                existing_paths += 1
                if os.access(path, os.R_OK):
                    readable_paths += 1

                    # Check for Python packages
                    if path_obj.is_dir():
                        try:
                            items = list(path_obj.iterdir())
                            py_files = [f for f in items if f.suffix == '.py']
                            init_files = [f for f in items if f.name == '__init__.py']
                            if py_files or init_files:
                                python_packages += 1
                        except:
                            pass

        print(f"Existing paths: {existing_paths}/{total_paths} ({existing_paths/total_paths*100:.1f}%)")
        print(f"Readable paths: {readable_paths}/{total_paths} ({readable_paths/total_paths*100:.1f}%)")
        print(f"Paths with Python code: {python_packages}/{readable_paths} ({python_packages/readable_paths*100 if readable_paths else 0:.1f}%)")

    def add_path(self, new_path):
        """Add a path to sys.path if it exists and is readable"""
        path_obj = Path(new_path).resolve()

        if not path_obj.exists():
            print(f"Error: Path does not exist: {path_obj}")
            return False

        if not path_obj.is_dir():
            print(f"Error: Not a directory: {path_obj}")
            return False

        if not os.access(path_obj, os.R_OK):
            print(f"Error: Path not readable: {path_obj}")
            return False

        if str(path_obj) in sys.path:
            print(f"Warning: Path already in sys.path: {path_obj}")
            return False

        sys.path.insert(0, str(path_obj))
        print(f"Added to sys.path: {path_obj}")
        return True

    def remove_path(self, path_to_remove):
        """Remove a path from sys.path"""
        if path_to_remove in sys.path:
            sys.path.remove(path_to_remove)
            print(f"Removed from sys.path: {path_to_remove}")
            return True
        else:
            print(f"Path not found in sys.path: {path_to_remove}")
            return False

    def show_module_stats(self):
        """Show statistics about loaded modules"""
        print("\nLoaded Module Statistics")
        print("=" * 25)

        total_modules = len(sys.modules)
        print(f"Total loaded modules: {total_modules}")

        # Categorize modules by origin
        builtin_modules = [m for m in sys.modules.keys() if m in sys.builtin_module_names]
        print(f"Built-in modules: {len(builtin_modules)}")

        # Try to identify standard library modules
        stdlib_modules = []
        site_packages_modules = []

        for name, module in sys.modules.items():
            if hasattr(module, '__file__') and module.__file__:
                file_path = Path(module.__file__)
                if 'site-packages' in str(file_path):
                    site_packages_modules.append(name)
                elif 'python' in str(file_path).lower():
                    if not 'site-packages' in str(file_path):
                        stdlib_modules.append(name)

        print(f"Standard library modules: {len(stdlib_modules)}")
        print(f"Third-party modules: {len(site_packages_modules)}")

    def reset_path(self):
        """Reset sys.path to original state"""
        sys.path[:] = self.original_path
        print("sys.path reset to original state")

def main():
    inspector = ModulePathInspector()

    commands = {
        'info': inspector.display_path_info,
        'analyze': inspector.analyze_path_effectiveness,
        'modules': inspector.show_module_stats,
        'reset': inspector.reset_path,
    }

    if len(sys.argv) < 2:
        print("Module Path Inspector")
        print("Usage: python path_inspector.py <command> [args...]")
        print()
        print("Commands:")
        print("  info          Show detailed path information")
        print("  analyze       Analyze path effectiveness")
        print("  modules       Show module loading statistics")
        print("  add <path>    Add path to sys.path")
        print("  remove <path> Remove path from sys.path")
        print("  reset         Reset sys.path to original state")
        return

    command = sys.argv[1].lower()

    if command in commands:
        commands[command]()
    elif command == 'add' and len(sys.argv) >= 3:
        inspector.add_path(sys.argv[2])
    elif command == 'remove' and len(sys.argv) >= 3:
        inspector.remove_path(sys.argv[2])
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
```

**Key Concepts Tested:**
- `sys.path` manipulation and inspection
- Module loading mechanics
- Path validation and management
- System integration

## Summary

These coding challenges cover the full spectrum of `sys` module usage:

- **Beginner:** Basic argument parsing, version checking, and stream usage
- **Intermediate:** Memory monitoring, stream redirection, recursive analysis, reference counting
- **Advanced:** Module path management, comprehensive system inspection

Each challenge includes:
- Clear problem statements
- Specific requirements
- Complete working solutions
- Key concepts being tested
- Best practices demonstrations

The solutions emphasize proper error handling, resource management, and cross-platform compatibility - essential skills when working with system-level Python code.
