# Theory Questions: Python `sys` Module

## Basic Concepts

### 1. What is the `sys` module in Python?
**Answer:** The `sys` module is a built-in Python module that provides access to system-specific parameters and functions. It allows interaction with the Python interpreter and provides information about the runtime environment, command-line arguments, standard I/O streams, and interpreter internals.

### 2. How does `sys` differ from the `os` module?
**Answer:** While both modules interact with the system, `sys` focuses on the Python interpreter and runtime environment, whereas `os` provides interfaces to operating system services. `sys` deals with Python-specific concerns like interpreter version and module loading, while `os` handles OS-level operations like file management and process control.

### 3. What are the main components of the `sys` module?
**Answer:** The main components include:
- Command-line argument access (`sys.argv`)
- Standard I/O streams (`sys.stdin`, `sys.stdout`, `sys.stderr`)
- Interpreter information (`sys.version`, `sys.platform`)
- Module system (`sys.modules`, `sys.path`)
- Runtime control (`sys.exit()`, recursion limits)
- Exception handling (`sys.exc_info()`)
- Memory analysis (`sys.getsizeof()`)

## Command Line Arguments

### 4. Explain `sys.argv` and its usage.
**Answer:** `sys.argv` is a list containing command-line arguments passed to a Python script. `sys.argv[0]` is the script name/path, and subsequent elements are the arguments. It's essential for creating command-line interfaces and should always be validated before access to prevent IndexError.

### 5. How do you handle command-line arguments safely?
**Answer:** Always check `len(sys.argv)` before accessing elements. Use try-except blocks for type conversion, and consider using `argparse` for complex argument parsing. Example:
```python
if len(sys.argv) < 2:
    print("Usage: script.py <filename>")
    sys.exit(1)
filename = sys.argv[1]
```

## Interpreter Information

### 6. What is the difference between `sys.version` and `sys.version_info`?
**Answer:** `sys.version` returns a string representation of the Python version (e.g., "3.9.7 (default, Sep 16 2021, 13:09:58) [GCC 7.5.0]"), while `sys.version_info` returns a named tuple with structured version information (major, minor, micro, releaselevel, serial) that's easier for programmatic version checking.

### 7. How would you check if the current Python version meets minimum requirements?
**Answer:** Use `sys.version_info` for comparison:
```python
if sys.version_info < (3, 6):
    raise RuntimeError("Python 3.6+ required")
```

### 8. What does `sys.platform` tell you?
**Answer:** `sys.platform` returns a string identifying the platform Python is running on. Common values include 'win32' (Windows), 'linux' (Linux), 'darwin' (macOS), and 'cygwin' (Cygwin on Windows).

## Standard I/O Streams

### 9. Explain the standard I/O streams in `sys`.
**Answer:** `sys.stdin` is the standard input stream for reading data, `sys.stdout` is the standard output stream for normal program output, and `sys.stderr` is the standard error stream for error messages and diagnostics. They can be redirected or manipulated for various purposes.

### 10. When should you flush `sys.stdout`?
**Answer:** You should flush `sys.stdout` when you need immediate output, especially before reading from `sys.stdin` (to ensure prompts appear) or when writing progress indicators. In interactive applications or when output needs to appear immediately rather than being buffered.

## Module System

### 11. What is `sys.path` and how is it used?
**Answer:** `sys.path` is a list of strings specifying the search paths for modules. Python uses this list to find modules when importing. You can modify it to add custom module locations, but should restore original values to avoid permanent changes.

### 12. Explain `sys.modules` and its purpose.
**Answer:** `sys.modules` is a dictionary mapping module names to module objects for all loaded modules. It serves as a cache to avoid re-importing modules and can be inspected to see what's currently loaded. Direct manipulation should be done carefully.

## Runtime Control

### 13. What does `sys.exit()` do and when should it be used?
**Answer:** `sys.exit()` terminates the Python interpreter and exits the program. It takes an optional exit code (0 for success, non-zero for errors). It should be used in scripts and command-line tools, but avoided in libraries (raise exceptions instead).

### 14. Explain recursion limits in Python.
**Answer:** Python has a recursion limit to prevent stack overflow. `sys.getrecursionlimit()` returns the current limit, and `sys.setrecursionlimit()` can change it. The default is usually 1000. Increasing it allows deeper recursion but risks stack overflow.

## Memory Management

### 15. What does `sys.getsizeof()` return?
**Answer:** `sys.getsizeof()` returns the size of an object in bytes, including the overhead of the object structure. It doesn't include the size of referenced objects for containers. For complete memory analysis, you need recursive calculation.

### 16. Explain reference counting in relation to `sys.getrefcount()`.
**Answer:** `sys.getrefcount()` returns the reference count of an object (number of references to it). The count is increased by 1 during the call itself, so the actual reference count is `sys.getrefcount(obj) - 1`. Python uses reference counting for garbage collection.

## Exception Handling

### 17. When is `sys.exc_info()` useful?
**Answer:** `sys.exc_info()` returns a tuple (type, value, traceback) containing information about the current exception. It's only valid within exception handlers and returns (None, None, None) outside them. Useful for advanced exception handling and logging.

### 18. What are exception hooks in `sys`?
**Answer:** `sys.excepthook` is a function called when an uncaught exception occurs. You can replace it with a custom function for custom exception handling, logging, or cleanup. `sys.unraisablehook` handles exceptions that cannot be raised normally.

## Advanced Topics

### 19. How does `sys` interact with the import system?
**Answer:** `sys` provides `sys.path` for module search paths, `sys.modules` for the module cache, and `sys.path_hooks`/`sys.meta_path` for customizing import behavior. These allow advanced control over how Python finds and loads modules.

### 20. What is the significance of `sys.executable`?
**Answer:** `sys.executable` returns the path to the Python interpreter executable. It's useful for spawning new Python processes, finding the Python installation directory, and ensuring scripts run with the correct interpreter.

### 21. Explain `sys.byteorder` and `sys.maxsize`.
**Answer:** `sys.byteorder` indicates the byte order of the system ('little' or 'big' endian). `sys.maxsize` is the maximum value for integers on the platform, which helps determine if Python is running in 32-bit or 64-bit mode.

### 22. How can `sys` be used for debugging?
**Answer:** `sys` provides debugging capabilities through:
- `sys._getframe()` for stack frame inspection
- `sys._current_frames()` for thread frame information
- Exception information via `sys.exc_info()`
- Module loading inspection via `sys.modules`

### 23. What are the security implications of using `sys`?
**Answer:** `sys` can expose sensitive information like file paths, environment details, and system capabilities. Modifying `sys.path` can lead to module injection attacks. Always validate inputs and be cautious when using `sys` in security-sensitive applications.

### 24. How does `sys` handle thread safety?
**Answer:** Most `sys` operations are thread-safe for reading, but modifications (like changing `sys.path` or `sys.stdout`) can cause race conditions. Use locks when modifying shared `sys` state from multiple threads. Thread-specific information is available through `sys._current_frames()`.

### 25. What is the relationship between `sys` and virtual environments?
**Answer:** `sys.prefix` and `sys.base_prefix` help detect virtual environments. In a virtual environment, `sys.prefix` points to the virtual environment directory, while `sys.base_prefix` points to the system Python installation. This distinction is useful for environment-specific behavior.

## Common Interview Follow-ups

### 26. Why might you modify `sys.path` at runtime?
**Answer:** You might modify `sys.path` to:
- Add custom module directories
- Support plugin architectures
- Enable dynamic module discovery
- Test modules before installation

Always document such modifications and consider using environment variables or configuration files instead.

### 27. How would you implement a custom import hook using `sys`?
**Answer:** You can implement custom import behavior by:
1. Creating a finder class implementing `importlib.abc.MetaPathFinder`
2. Adding it to `sys.meta_path`
3. Implementing `find_spec()` method
4. Optionally adding path hooks to `sys.path_hooks`

### 28. What happens if you call `sys.exit()` in a thread?
**Answer:** `sys.exit()` terminates the entire process, not just the thread. This can be problematic in multi-threaded applications. Instead, use thread communication mechanisms like events or queues to signal the main thread to exit gracefully.

### 29. How can `sys` help with memory leak detection?
**Answer:** `sys` can help with memory leak detection by:
- Using `sys.getsizeof()` to track object sizes
- Monitoring `sys.getrefcount()` for unexpected reference counts
- Inspecting `sys.modules` for module accumulation
- Using `tracemalloc` (which integrates with `sys`) for detailed memory tracing

### 30. Explain the difference between `sys.path` and `PYTHONPATH`.
**Answer:** `PYTHONPATH` is an environment variable that Python reads at startup to initialize `sys.path`. While you can modify `sys.path` at runtime, changes to `PYTHONPATH` require restarting Python. `sys.path` provides more dynamic control but `PYTHONPATH` is better for system-wide configuration.
