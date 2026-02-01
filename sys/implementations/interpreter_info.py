#!/usr/bin/env python3
"""
Interpreter Information Implementation

This module demonstrates how to access and utilize various interpreter
information provided by the sys module, including version details,
platform information, and runtime characteristics.
"""

import sys
import platform
import os


def basic_interpreter_info():
    """Display basic interpreter information"""
    print("Basic Interpreter Information")
    print("=" * 30)

    print(f"Python Version: {sys.version}")
    print(f"Version Info: {sys.version_info}")
    print(f"Platform: {sys.platform}")
    print(f"Implementation: {sys.implementation}")
    print(f"Executable: {sys.executable}")
    print(f"Prefix: {sys.prefix}")
    print(f"Base Prefix: {sys.base_prefix}")
    print(f"Exec Prefix: {sys.exec_prefix}")
    print(f"Base Exec Prefix: {sys.base_exec_prefix}")


def version_checking():
    """Demonstrate version checking and compatibility"""
    print("\nVersion Checking and Compatibility")
    print("=" * 35)

    # Check Python version
    if sys.version_info >= (3, 8):
        print("✓ Python 3.8+ detected")
    else:
        print("✗ Python 3.8+ required")

    # Version comparison
    version = sys.version_info
    print(f"Major: {version.major}")
    print(f"Minor: {version.minor}")
    print(f"Micro: {version.micro}")
    print(f"Release Level: {version.releaselevel}")
    print(f"Serial: {version.serial}")

    # Check for specific features
    features = {
        "3.6+": version >= (3, 6),
        "3.7+": version >= (3, 7),
        "3.8+": version >= (3, 8),
        "3.9+": version >= (3, 9),
        "3.10+": version >= (3, 10),
    }

    print("\nFeature Support:")
    for feature, supported in features.items():
        status = "✓" if supported else "✗"
        print(f"  {status} {feature}")


def platform_detection():
    """Detect and handle different platforms"""
    print("\nPlatform Detection")
    print("=" * 19)

    platform_name = sys.platform
    print(f"sys.platform: {platform_name}")

    # Platform-specific handling
    if platform_name.startswith('win'):
        print("Running on Windows")
        # Windows-specific code
        print(f"Windows version: {platform.version()}")

    elif platform_name.startswith('linux'):
        print("Running on Linux")
        # Linux-specific code
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME'):
                        print(f"Distribution: {line.split('=')[1].strip().strip('\"')}")
                        break
        except FileNotFoundError:
            print("Could not determine Linux distribution")

    elif platform_name.startswith('darwin'):
        print("Running on macOS")
        # macOS-specific code
        print(f"macOS version: {platform.mac_ver()[0]}")

    else:
        print(f"Running on unknown platform: {platform_name}")

    # Cross-platform information
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"System: {platform.system()}")


def implementation_details():
    """Explore Python implementation details"""
    print("\nImplementation Details")
    print("=" * 23)

    impl = sys.implementation

    print(f"Name: {impl.name}")
    print(f"Version: {impl.version}")
    print(f"Hex Version: {impl.hexversion}")
    print(f"Cache Tag: {impl.cache_tag}")

    # Check implementation type
    if impl.name == 'cpython':
        print("✓ Running CPython (standard implementation)")
    elif impl.name == 'pypy':
        print("✓ Running PyPy (JIT compiler)")
    elif impl.name == 'jython':
        print("✓ Running Jython (JVM implementation)")
    elif impl.name == 'ironpython':
        print("✓ Running IronPython (.NET implementation)")
    else:
        print(f"? Unknown implementation: {impl.name}")

    # Hex version breakdown
    hex_ver = impl.hexversion
    major = (hex_ver >> 24) & 0xFF
    minor = (hex_ver >> 16) & 0xFF
    micro = (hex_ver >> 8) & 0xFF
    release = hex_ver & 0xFF

    print(f"Hex version breakdown: {major}.{minor}.{micro}.{release}")


def path_and_modules():
    """Explore Python path and module information"""
    print("\nPath and Module Information")
    print("=" * 28)

    print(f"Python Path: {sys.path[:3]}...")  # Show first 3 entries
    print(f"Path length: {len(sys.path)}")

    # Module information
    print(f"Built-in modules: {len(sys.builtin_module_names)}")
    print(f"First 10 built-in modules: {list(sys.builtin_module_names)[:10]}")

    # Meta path
    print(f"Meta path entries: {len(sys.meta_path)}")
    for i, finder in enumerate(sys.meta_path):
        print(f"  {i}: {type(finder).__name__}")

    # Path hooks
    print(f"Path hooks: {len(sys.path_hooks)}")
    for i, hook in enumerate(sys.path_hooks):
        print(f"  {i}: {type(hook).__name__}")


def threading_and_async():
    """Check threading and async capabilities"""
    print("\nThreading and Async Information")
    print("=" * 32)

    # Threading info
    try:
        import threading
        print(f"Threading available: ✓")
        print(f"Active threads: {threading.active_count()}")
        print(f"Current thread: {threading.current_thread().name}")
    except ImportError:
        print("Threading not available: ✗")

    # AsyncIO info
    try:
        import asyncio
        print(f"AsyncIO available: ✓")
        print(f"AsyncIO version: {asyncio.__version__ if hasattr(asyncio, '__version__') else 'built-in'}")
    except ImportError:
        print("AsyncIO not available: ✗")

    # Check if running in thread
    print(f"Main thread: {threading.current_thread() is threading.main_thread()}")


def performance_flags():
    """Check Python performance and optimization flags"""
    print("\nPerformance and Optimization Flags")
    print("=" * 36)

    # Check optimization level
    if hasattr(sys, 'flags'):
        flags = sys.flags
        print(f"Debug: {flags.debug}")
        print(f"Inspect: {flags.inspect}")
        print(f"Interactive: {flags.interactive}")
        print(f"Optimize: {flags.optimize}")
        print(f"Dont write bytecode: {flags.dont_write_bytecode}")
        print(f"No user site: {flags.no_user_site}")
        print(f"No site: {flags.no_site}")
        print(f"Ignore environment: {flags.ignore_environment}")
        print(f"Verbose: {flags.verbose}")
        print(f"Bytes warning: {flags.bytes_warning}")
        print(f"Quiet: {flags.quiet}")

    # Check if running optimized
    if sys.flags.optimize:
        print("Running in optimized mode")
    else:
        print("Running in normal mode")

    # Check for debug build
    if hasattr(sys, 'gettotalrefcount'):
        print("Debug build detected")
    else:
        print("Release build")


def environment_variables():
    """Check Python-related environment variables"""
    print("\nPython Environment Variables")
    print("=" * 30)

    python_env_vars = [
        'PYTHONPATH',
        'PYTHONHOME',
        'PYTHONSTARTUP',
        'PYTHONOPTIMIZE',
        'PYTHONDEBUG',
        'PYTHONINSPECT',
        'PYTHONUNBUFFERED',
        'PYTHONDONTWRITEBYTECODE',
        'PYTHONNOUSERSITE',
        'PYTHONVERBOSE',
    ]

    for var in python_env_vars:
        value = os.environ.get(var, 'Not set')
        if value != 'Not set':
            print(f"{var}: {value}")
        else:
            print(f"{var}: Not set")


def system_limits():
    """Display system limits and constraints"""
    print("\nSystem Limits and Constraints")
    print("=" * 31)

    print(f"Max size (sys.maxsize): {sys.maxsize}")
    print(f"Max size in bits: {sys.maxsize.bit_length()}")

    # Recursion limit
    print(f"Recursion limit: {sys.getrecursionlimit()}")

    # Integer info
    if hasattr(sys, 'int_info'):
        int_info = sys.int_info
        print(f"Integer bits per digit: {int_info.bits_per_digit}")
        print(f"Integer sizeof digit: {int_info.sizeof_digit}")

    # Float info
    if hasattr(sys, 'float_info'):
        float_info = sys.float_info
        print(f"Float mantissa bits: {float_info.mant_dig}")
        print(f"Float max exponent: {float_info.max_exp}")
        print(f"Float min exponent: {float_info.min_exp}")

    # Hash randomization
    if hasattr(sys, 'flags') and hasattr(sys.flags, 'hash_randomization'):
        print(f"Hash randomization: {sys.flags.hash_randomization}")


def compatibility_checker():
    """Demonstrate a compatibility checker utility"""
    print("\nCompatibility Checker")
    print("=" * 21)

    def check_compatibility(requirements):
        """Check if current Python meets requirements"""
        current = sys.version_info
        results = {}

        for req_name, req_version in requirements.items():
            if isinstance(req_version, tuple):
                results[req_name] = current >= req_version
            else:
                # Assume string like "3.8"
                major, minor = map(int, req_version.split('.'))
                results[req_name] = current >= (major, minor)

        return results

    # Example requirements
    requirements = {
        "Web framework": "3.8",
        "Data science": "3.7",
        "Async support": "3.5",
        "Type hints": "3.5",
        "F-strings": "3.6",
    }

    results = check_compatibility(requirements)

    print("Compatibility Check Results:")
    for feature, compatible in results.items():
        status = "✓" if compatible else "✗"
        print(f"  {status} {feature}")


def runtime_inspection():
    """Inspect current runtime state"""
    print("\nRuntime Inspection")
    print("=" * 19)

    # Current working directory
    print(f"CWD: {os.getcwd()}")

    # Process ID
    print(f"PID: {os.getpid()}")

    # Command line arguments
    print(f"Command line: {sys.argv}")

    # Module search path (first few)
    print("Module search path:")
    for i, path in enumerate(sys.path[:5]):
        print(f"  {i}: {path}")
    if len(sys.path) > 5:
        print(f"  ... and {len(sys.path) - 5} more")

    # Loaded modules count
    print(f"Loaded modules: {len(sys.modules)}")

    # Check if running from script or interactive
    if hasattr(sys, 'ps1'):
        print("Running in interactive mode")
    else:
        print("Running from script")


def main():
    """Main function to run all interpreter info examples"""

    examples = {
        'basic': basic_interpreter_info,
        'version': version_checking,
        'platform': platform_detection,
        'implementation': implementation_details,
        'path': path_and_modules,
        'threading': threading_and_async,
        'performance': performance_flags,
        'environment': environment_variables,
        'limits': system_limits,
        'compatibility': compatibility_checker,
        'runtime': runtime_inspection,
    }

    if len(sys.argv) < 2:
        print("Interpreter Information Examples")
        print("===============================")
        print()
        print("Available examples:")
        for name in examples.keys():
            print(f"  {name}")
        print()
        print("Usage: python interpreter_info.py <example_name>")
        print("Example: python interpreter_info.py basic")
        return

    example_name = sys.argv[1].lower()

    if example_name in examples:
        try:
            examples[example_name]()
        except Exception as e:
            print(f"Error running example '{example_name}': {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Unknown example: {example_name}")
        print(f"Available examples: {', '.join(examples.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
