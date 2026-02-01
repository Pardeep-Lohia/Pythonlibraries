# Exception Handling Functions

## Purpose
`sys` provides functions to access and manipulate exception information during error handling, allowing for advanced exception inspection and custom error processing.

## Key Functions

### `sys.exc_info()`
- **Purpose**: Get information about the current exception
- **Returns**: Tuple of `(type, value, traceback)` or `(None, None, None)` if no exception
- **Usage**: Access exception details from within exception handlers

### `sys.exception()`
- **Purpose**: Get the current exception instance (Python 3.11+)
- **Returns**: Current exception object or `None`
- **Usage**: Direct access to exception object

### `sys.unraisablehook(hook)`
- **Purpose**: Set a hook for unraisable exceptions
- **Parameters**: `hook` - callable that takes `(exception, err_msg)` arguments
- **Usage**: Handle exceptions that cannot be raised normally

### `sys.excepthook(type, value, traceback)`
- **Purpose**: Handle uncaught exceptions
- **Parameters**:
  - `type`: Exception class
  - `value`: Exception instance
  - `traceback`: Traceback object
- **Usage**: Custom handling of uncaught exceptions

## Syntax and Examples

### Basic Exception Information
```python
import sys

def exception_info_demo():
    try:
        1 / 0
    except:
        # Get current exception info
        exc_type, exc_value, exc_traceback = sys.exc_info()

        print(f"Exception type: {exc_type}")
        print(f"Exception value: {exc_value}")
        print(f"Has traceback: {exc_traceback is not None}")

        # Exception info is cleared after handler
        print("After handler:")
        print(f"exc_info: {sys.exc_info()}")

exception_info_demo()
```

### Custom Exception Hook
```python
import sys

def custom_excepthook(exc_type, exc_value, exc_traceback):
    """Custom handler for uncaught exceptions"""
    print("=== Uncaught Exception ===")
    print(f"Type: {exc_type.__name__}")
    print(f"Message: {exc_value}")

    # Log to file
    with open('error.log', 'a') as f:
        import traceback
        f.write(f"{exc_type.__name__}: {exc_value}\n")
        traceback.print_exc(file=f)
        f.write("\n" + "="*50 + "\n")

    # Call original hook (optional)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

# Install custom hook
sys.excepthook = custom_excepthook

# Test with uncaught exception
# raise ValueError("This will be caught by custom hook")
```

### Exception Context Preservation
```python
import sys

def exception_context_demo():
    def inner_function():
        raise ValueError("Inner error")

    def outer_function():
        try:
            inner_function()
        except Exception as e:
            # At this point, sys.exc_info() contains the exception
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(f"Caught: {exc_type.__name__}: {exc_value}")

            # Re-raise with context
            raise RuntimeError("Outer error") from e

    try:
        outer_function()
    except Exception as e:
        print(f"Final exception: {e}")
        print(f"Cause: {e.__cause__}")

exception_context_demo()
```

### Unraisable Exception Hook
```python
import sys
import weakref

def custom_unraisable_hook(unraisable):
    """Handle unraisable exceptions"""
    exception = unraisable.exception
    err_msg = unraisable.err_msg

    print("=== Unraisable Exception ===")
    print(f"Exception: {exception}")
    print(f"Error message: {err_msg}")

    # Log the issue
    with open('unraisable.log', 'a') as f:
        f.write(f"Unraisable: {exception} - {err_msg}\n")

# Install hook
sys.unraisablehook = custom_unraisable_hook

# Example of unraisable exception (weakref callback error)
def callback(ref):
    raise ValueError("Error in callback")

obj = [1, 2, 3]
ref = weakref.ref(obj, callback)

# Delete object and trigger callback
del obj
# The callback error becomes unraisable
```

## Advanced Usage

### Exception Tracing and Logging
```python
import sys
import logging
import traceback

# Set up logging
logging.basicConfig(filename='exceptions.log', level=logging.ERROR)

def advanced_exception_handler():
    """Advanced exception handling with full context"""

    def log_exception(exc_info):
        """Log exception with full traceback"""
        exc_type, exc_value, exc_traceback = exc_info

        # Format traceback
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = ''.join(tb_lines)

        # Log to file
        logging.error("Exception occurred:\n%s", tb_text)

        # Also print to stderr
        sys.stderr.write("Exception logged. See exceptions.log for details.\n")

    def custom_hook(exc_type, exc_value, exc_traceback):
        """Custom excepthook that logs exceptions"""
        log_exception((exc_type, exc_value, exc_traceback))
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    # Install custom hook
    sys.excepthook = custom_hook

    return log_exception

# Usage
log_exception = advanced_exception_handler()

# Test
try:
    raise ValueError("Test exception")
except:
    log_exception(sys.exc_info())
```

### Exception Filtering and Handling
```python
import sys

class ExceptionFilter:
    """Filter and handle exceptions based on criteria"""

    def __init__(self):
        self.handlers = {}

    def register_handler(self, exc_type, handler):
        """Register a handler for specific exception type"""
        self.handlers[exc_type] = handler

    def handle_exception(self, exc_info):
        """Handle exception using registered handlers"""
        exc_type, exc_value, exc_traceback = exc_info

        # Find handler for this exception type
        for base_type, handler in self.handlers.items():
            if isinstance(exc_value, base_type):
                return handler(exc_type, exc_value, exc_traceback)

        # No specific handler found
        return False

# Create filter
exception_filter = ExceptionFilter()

# Register handlers
def handle_value_error(exc_type, exc_value, exc_traceback):
    print(f"ValueError handled: {exc_value}")
    return True

def handle_key_error(exc_type, exc_value, exc_traceback):
    print(f"KeyError handled: {exc_value}")
    return True

exception_filter.register_handler(ValueError, handle_value_error)
exception_filter.register_handler(KeyError, handle_key_error)

# Custom excepthook using filter
def filtered_excepthook(exc_type, exc_value, exc_traceback):
    exc_info = (exc_type, exc_value, exc_traceback)

    if not exception_filter.handle_exception(exc_info):
        # Fall back to default handling
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = filtered_excepthook
```

### Exception Chain Analysis
```python
import sys

def analyze_exception_chain():
    """Analyze chained exceptions"""

    def create_exception_chain():
        try:
            raise ValueError("Original error")
        except ValueError as e:
            raise RuntimeError("Wrapper error") from e

    try:
        create_exception_chain()
    except Exception as e:
        print("Exception chain analysis:")
        print(f"Final exception: {e}")

        # Walk the exception chain
        current = e
        depth = 0
        while current:
            print(f"  Level {depth}: {type(current).__name__}: {current}")
            current = current.__cause__ or current.__context__
            depth += 1

        # Also check sys.exc_info
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"sys.exc_info type: {exc_type}")
        print(f"sys.exc_info value: {exc_value}")

analyze_exception_chain()
```

### Thread-Safe Exception Handling
```python
import sys
import threading
import traceback

class ThreadExceptionHandler:
    """Handle exceptions in threads safely"""

    def __init__(self):
        self.thread_exceptions = {}
        self.lock = threading.Lock()

    def thread_excepthook(self, args):
        """Handle thread exceptions"""
        thread_id = args.thread.ident
        exc_type = args.exc_type
        exc_value = args.exc_value
        exc_traceback = args.exc_traceback

        with self.lock:
            self.thread_exceptions[thread_id] = {
                'type': exc_type,
                'value': exc_value,
                'traceback': exc_traceback
            }

        print(f"Exception in thread {thread_id}: {exc_type.__name__}: {exc_value}")

    def get_thread_exceptions(self):
        """Get all thread exceptions"""
        with self.lock:
            return self.thread_exceptions.copy()

# Install thread exception hook
handler = ThreadExceptionHandler()
threading.excepthook = handler.thread_excepthook

def problematic_thread():
    """Thread that raises an exception"""
    raise ValueError("Thread exception")

# Start thread
thread = threading.Thread(target=problematic_thread)
thread.start()
thread.join()

# Check for exceptions
exceptions = handler.get_thread_exceptions()
print(f"Thread exceptions: {len(exceptions)}")
```

## Edge Cases and Considerations

### Exception Info Lifetime
```python
import sys

def exception_info_lifetime():
    """Demonstrate when exc_info is available"""

    def check_exc_info():
        info = sys.exc_info()
        print(f"exc_info in handler: {info[0] is not None}")

    try:
        raise ValueError("Test")
    except:
        check_exc_info()

    # Outside handler
    info = sys.exc_info()
    print(f"exc_info outside handler: {info[0] is not None}")

exception_info_lifetime()
```

### Nested Exception Handlers
```python
import sys

def nested_handlers():
    """Nested exception handlers and exc_info"""

    try:
        try:
            raise ValueError("Inner")
        except ValueError:
            print(f"Inner handler exc_info: {sys.exc_info()[0].__name__}")
            raise RuntimeError("Outer")
    except RuntimeError:
        print(f"Outer handler exc_info: {sys.exc_info()[0].__name__}")

nested_handlers()
```

### Exception in Exception Handler
```python
import sys

def exception_in_handler():
    """Handle exceptions that occur during exception handling"""

    def risky_handler(exc_type, exc_value, exc_traceback):
        try:
            # This might fail
            with open('/nonexistent/file', 'w') as f:
                f.write(f"Exception: {exc_value}")
        except:
            # Fallback handling
            sys.stderr.write(f"Failed to log exception: {exc_value}\n")
        finally:
            # Always call original hook
            sys.__excepthook__(exc_type, exc_value, exc_traceback)

    # Install risky handler
    sys.excepthook = risky_handler

    # Test
    raise ValueError("Test exception")

exception_in_handler()
```

## Common Patterns

### Global Exception Logger
```python
import sys
import logging
from datetime import datetime

class GlobalExceptionLogger:
    """Global exception logging system"""

    def __init__(self, log_file='exceptions.log'):
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def log_exception(self, exc_info, context=None):
        """Log an exception with context"""
        exc_type, exc_value, exc_traceback = exc_info

        # Create detailed log message
        import traceback
        tb_str = ''.join(traceback.format_exception(*exc_info))

        log_message = f"Exception: {exc_type.__name__}: {exc_value}"
        if context:
            log_message += f"\nContext: {context}"

        logging.error(log_message)
        logging.error("Traceback:\n%s", tb_str)

    def install_hook(self):
        """Install as global exception hook"""
        def hook(exc_type, exc_value, exc_traceback):
            exc_info = (exc_type, exc_value, exc_traceback)
            self.log_exception(exc_info, "Uncaught exception")
            sys.__excepthook__(exc_type, exc_value, exc_traceback)

        sys.excepthook = hook

# Usage
logger = GlobalExceptionLogger()
logger.install_hook()

# Test
# raise RuntimeError("This will be logged")
```

### Exception Recovery System
```python
import sys
import time

class ExceptionRecovery:
    """System for recovering from exceptions"""

    def __init__(self):
        self.recovery_actions = {}
        self.max_retries = 3

    def register_recovery(self, exc_type, action):
        """Register recovery action for exception type"""
        self.recovery_actions[exc_type] = action

    def attempt_recovery(self, func, *args, **kwargs):
        """Execute function with recovery"""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                exc_type = type(e)

                if exc_type in self.recovery_actions and attempt < self.max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    recovery_action = self.recovery_actions[exc_type]
                    recovery_action()
                    time.sleep(1)  # Wait before retry
                else:
                    raise

# Example recovery actions
def network_recovery():
    print("Attempting network recovery...")
    # Reset network connection, etc.

def file_recovery():
    print("Attempting file recovery...")
    # Close and reopen files, etc.

# Set up recovery system
recovery = ExceptionRecovery()
recovery.register_recovery(ConnectionError, network_recovery)
recovery.register_recovery(IOError, file_recovery)

def risky_operation():
    # Simulate failure
    raise ConnectionError("Network down")

# Test recovery
try:
    result = recovery.attempt_recovery(risky_operation)
except Exception as e:
    print(f"Final failure: {e}")
```

## Best Practices

1. **Use `sys.exc_info()` within exception handlers** - It's only valid during handling
2. **Install custom hooks carefully** - They affect global exception handling
3. **Preserve original exception hooks** - Call `sys.__excepthook__` for fallback
4. **Handle exceptions in hooks safely** - Avoid raising exceptions in exception handlers
5. **Log exceptions comprehensively** - Include full tracebacks and context
6. **Consider thread safety** - Exception handling in multi-threaded applications

## Performance Considerations

- **`sys.exc_info()` is fast** when called within exception handlers
- **Custom hooks have minimal overhead** until exceptions occur
- **Exception logging** can impact performance if done synchronously
- **Thread exception hooks** are called synchronously, affecting thread performance

## Comparison with Other Exception Handling

| Method | `sys.exc_info()` | `traceback` module | `logging` module |
|--------|------------------|-------------------|------------------|
| Scope | Current exception | Full traceback | General logging |
| Usage | Within handlers | Any context | Any context |
| Details | Type, value, tb | Formatted traceback | Custom messages |
| Performance | Fast | Medium | Configurable |

`sys` provides the foundation for exception access, while other modules offer formatting and logging capabilities.
