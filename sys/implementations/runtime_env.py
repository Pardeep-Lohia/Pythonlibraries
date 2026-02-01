#!/usr/bin/env python3
"""
Runtime Environment Implementation

This module demonstrates runtime environment control using sys module,
including module management, path manipulation, recursion control,
memory monitoring, and controlled program termination.
"""

import sys
import os
import time
import tracemalloc
from typing import Dict, List, Any, Optional


class RuntimeEnvironment:
    """Manager for Python runtime environment"""

    def __init__(self):
        self.original_recursion_limit = sys.getrecursionlimit()
        self.original_path = sys.path[:]
        self.memory_monitoring = False

    def set_recursion_limit(self, limit: int):
        """Set recursion limit with validation"""
        if limit < 100:
            raise ValueError("Recursion limit too low")
        if limit > 10000:
            raise ValueError("Recursion limit too high")

        sys.setrecursionlimit(limit)
        print(f"Recursion limit set to {limit}")

    def reset_recursion_limit(self):
        """Reset recursion limit to original value"""
        sys.setrecursionlimit(self.original_recursion_limit)
        print(f"Recursion limit reset to {self.original_recursion_limit}")

    def add_path(self, path: str, priority: bool = False):
        """Add path to sys.path"""
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")

        if priority:
            sys.path.insert(0, path)
        else:
            sys.path.append(path)

        print(f"Added path: {path} (priority: {priority})")

    def remove_path(self, path: str):
        """Remove path from sys.path"""
        if path in sys.path:
            sys.path.remove(path)
            print(f"Removed path: {path}")
        else:
            print(f"Path not found: {path}")

    def reset_path(self):
        """Reset sys.path to original state"""
        sys.path[:] = self.original_path
        print("sys.path reset to original state")

    def get_module_info(self) -> Dict[str, Any]:
        """Get information about loaded modules"""
        return {
            'total_modules': len(sys.modules),
            'module_names': list(sys.modules.keys())[:10],  # First 10
            'builtin_modules': [name for name in sys.modules.keys()
                              if name.startswith('_') and not name.startswith('__')],
        }

    def start_memory_monitoring(self):
        """Start memory monitoring"""
        if not self.memory_monitoring:
            tracemalloc.start()
            self.memory_monitoring = True
            print("Memory monitoring started")

    def stop_memory_monitoring(self):
        """Stop memory monitoring"""
        if self.memory_monitoring:
            tracemalloc.stop()
            self.memory_monitoring = False
            print("Memory monitoring stopped")

    def get_memory_usage(self) -> Optional[Dict[str, int]]:
        """Get current memory usage"""
        if not self.memory_monitoring:
            return None

        current, peak = tracemalloc.get_traced_memory()
        return {
            'current': current,
            'peak': peak,
            'current_mb': current / 1024 / 1024,
            'peak_mb': peak / 1024 / 1024,
        }

    def get_object_size(self, obj: Any) -> int:
        """Get size of an object in bytes"""
        return sys.getsizeof(obj)

    def get_refcount(self, obj: Any) -> int:
        """Get reference count of an object"""
        return sys.getrefcount(obj)

    def controlled_exit(self, code: int = 0, message: str = None):
        """Exit program with cleanup"""
        if message:
            if code == 0:
                print(message)
            else:
                sys.stderr.write(message + '\n')

        print("Performing cleanup...")
        self.reset_recursion_limit()
        self.reset_path()
        self.stop_memory_monitoring()

        sys.exit(code)


def module_explorer():
    """Explore loaded modules and their properties"""
    print("Module Explorer")
    print("=" * 15)

    env = RuntimeEnvironment()
    info = env.get_module_info()

    print(f"Total modules loaded: {info['total_modules']}")
    print()

    print("First 10 loaded modules:")
    for i, name in enumerate(info['module_names'], 1):
        module = sys.modules[name]
        module_type = type(module).__name__
        print(f"  {i:2d}. {name} ({module_type})")

    print()
    print("Builtin modules:")
    for name in sorted(info['builtin_modules'])[:10]:
        print(f"  {name}")

    if len(info['builtin_modules']) > 10:
        print(f"  ... and {len(info['builtin_modules']) - 10} more")

    # Import a module and see the change
    print()
    print("Importing 'collections' module...")
    import collections

    new_info = env.get_module_info()
    print(f"Modules after import: {new_info['total_modules']} (+{new_info['total_modules'] - info['total_modules']})")


def path_manager_demo():
    """Demonstrate path management capabilities"""
    print("Path Management Demo")
    print("=" * 20)

    env = RuntimeEnvironment()

    print("Original sys.path entries:")
    for i, path in enumerate(sys.path[:5]):
        print(f"  {i+1}: {path}")
    if len(sys.path) > 5:
        print(f"  ... and {len(sys.path) - 5} more")

    # Create a temporary directory for demo
    import tempfile
    temp_dir = tempfile.mkdtemp()
    print(f"\nCreated temporary directory: {temp_dir}")

    try:
        # Add with high priority
        env.add_path(temp_dir, priority=True)
        print("After adding temp directory with priority:")
        print(f"  First path: {sys.path[0]}")

        # Add another path with low priority
        another_temp = tempfile.mkdtemp()
        env.add_path(another_temp, priority=False)
        print(f"  Last path: {sys.path[-1]}")

        # Remove paths
        env.remove_path(temp_dir)
        env.remove_path(another_temp)

    finally:
        # Cleanup
        os.rmdir(temp_dir)
        if 'another_temp' in locals():
            os.rmdir(another_temp)

    env.reset_path()
    print("Paths reset to original state")


def recursion_control_demo():
    """Demonstrate recursion limit control"""
    print("Recursion Control Demo")
    print("=" * 22)

    env = RuntimeEnvironment()

    print(f"Original recursion limit: {sys.getrecursionlimit()}")

    # Test with different limits
    limits = [200, 500, 1000, 2000]

    for limit in limits:
        try:
            env.set_recursion_limit(limit)

            # Test recursion
            def countdown(n):
                if n <= 0:
                    return 0
                return n + countdown(n - 1)

            try:
                result = countdown(limit // 2)  # Use half the limit
                print(f"  Successfully computed with limit {limit}")
            except RecursionError:
                print(f"  RecursionError with limit {limit}")

        except ValueError as e:
            print(f"  Invalid limit {limit}: {e}")

    env.reset_recursion_limit()
    print(f"Reset to original limit: {sys.getrecursionlimit()}")


def memory_monitor_demo():
    """Demonstrate memory monitoring capabilities"""
    print("Memory Monitor Demo")
    print("=" * 19)

    env = RuntimeEnvironment()
    env.start_memory_monitoring()

    print("Creating data structures...")

    # Create various objects
    small_list = [i for i in range(100)]
    large_list = [i for i in range(10000)]
    nested_dict = {f"key_{i}": {"data": list(range(100))} for i in range(100)}

    # Check memory usage
    memory = env.get_memory_usage()
    if memory:
        print("Memory usage:")
        print(f"Current: {memory['current_mb']:.2f} MB")
        print(f"Peak: {memory['peak_mb']:.2f} MB")

    # Check object sizes
    print("\nObject sizes:")
    objects = [
        ("Small list", small_list),
        ("Large list", large_list),
        ("Nested dict", nested_dict),
        ("String", "Hello, World!"),
        ("Integer", 42),
    ]

    for name, obj in objects:
        size = env.get_object_size(obj)
        refcount = env.get_refcount(obj)
        print("8")

    env.stop_memory_monitoring()


def performance_profiler():
    """Simple performance profiler using sys capabilities"""
    print("Performance Profiler")
    print("=" * 20)

    env = RuntimeEnvironment()
    env.start_memory_monitoring()

    def profile_function(func, *args, **kwargs):
        """Profile a function's execution"""
        start_time = time.time()
        start_memory = env.get_memory_usage()

        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = None
            success = False
            error = str(e)

        end_time = time.time()
        end_memory = env.get_memory_usage()

        execution_time = end_time - start_time
        memory_delta = (end_memory['current'] - start_memory['current']) if start_memory and end_memory else 0

        print(f"Function: {func.__name__}")
        print(".4f")
        print("+.2f")
        print(f"  Success: {success}")

        if not success:
            print(f"  Error: {error}")

        return result

    # Test functions
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    def list_operations():
        data = []
        for i in range(1000):
            data.append(i ** 2)
        return sum(data)

    print("Profiling functions:")
    print()

    profile_function(fibonacci, 25)
    print()
    profile_function(list_operations)

    env.stop_memory_monitoring()


def environment_inspector():
    """Inspect and report on runtime environment"""
    print("Environment Inspector")
    print("=" * 21)

    env = RuntimeEnvironment()

    print("Runtime Information:")
    print(f"  Python executable: {sys.executable}")
    print(f"  Platform: {sys.platform}")
    print(f"  Version: {sys.version.split()[0]}")
    print(f"  Recursion limit: {sys.getrecursionlimit()}")
    print(f"  Modules loaded: {len(sys.modules)}")

    # Path information
    print(f"\nPath Information:")
    print(f"  Total paths: {len(sys.path)}")
    print(f"  Current directory in path: {'' in sys.path or '.' in sys.path}")

    # Memory information
    env.start_memory_monitoring()
    memory = env.get_memory_usage()
    if memory:
        print("Memory Information:")
        print(".2f")
        print(".2f")
    env.stop_memory_monitoring()

    # Test object creation
    test_objects = [42, "hello", [1, 2, 3], {"key": "value"}]
    print("Object Information:")
    for obj in test_objects:
        size = env.get_object_size(obj)
        refcount = env.get_refcount(obj)
        print("8")


def controlled_shutdown_demo():
    """Demonstrate controlled program shutdown"""
    print("Controlled Shutdown Demo")
    print("=" * 25)

    env = RuntimeEnvironment()

    # Modify environment
    env.set_recursion_limit(1500)
    temp_dir = "/tmp/demo_path"
    os.makedirs(temp_dir, exist_ok=True)
    env.add_path(temp_dir)

    print("Environment modified:")
    print(f"  Recursion limit: {sys.getrecursionlimit()}")
    print(f"  Paths: {len(sys.path)}")

    # Simulate some work
    time.sleep(0.5)

    # Controlled shutdown
    print("\nInitiating controlled shutdown...")
    env.controlled_exit(0, "Program completed successfully")

    # This line won't execute
    print("This won't print")


def main():
    """Main function with different runtime environment demonstrations"""

    demos = {
        'modules': module_explorer,
        'path': path_manager_demo,
        'recursion': recursion_control_demo,
        'memory': memory_monitor_demo,
        'profile': performance_profiler,
        'inspect': environment_inspector,
        'shutdown': controlled_shutdown_demo,
    }

    if len(sys.argv) < 2:
        print("Runtime Environment Control Tool")
        print("=================================")
        print()
        print("Available demonstrations:")
        for name in demos.keys():
            print(f"  {name}")
        print()
        print("Usage: python runtime_env.py <demo_name>")
        print("Example: python runtime_env.py modules")
        return

    demo_name = sys.argv[1].lower()

    if demo_name in demos:
        try:
            demos[demo_name]()
        except KeyboardInterrupt:
            print("\nDemo interrupted by user")
        except Exception as e:
            print(f"\nDemo failed: {e}")
    else:
        sys.stderr.write(f"Unknown demonstration: {demo_name}\n")
        sys.stderr.write(f"Available demos: {', '.join(demos.keys())}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()