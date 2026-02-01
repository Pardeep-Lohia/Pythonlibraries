#!/usr/bin/env python3
"""
Python Runtime Information Implementation

This script demonstrates various ways to gather and display Python runtime information
using the platform module. All examples are cross-platform safe.
"""

import platform
import sys
import json
from datetime import datetime


def basic_python_info():
    """Display basic Python version and implementation information."""
    print("=== Basic Python Information ===")

    version = platform.python_version()
    implementation = platform.python_implementation()
    compiler = platform.python_compiler()

    print(f"Python Version: {version}")
    print(f"Implementation: {implementation}")
    print(f"Compiler: {compiler}")
    print()


def detailed_version_info():
    """Display detailed Python version information."""
    print("=== Detailed Python Version Information ===")

    version = platform.python_version()
    version_tuple = platform.python_version_tuple()
    version_string = platform.python_version_string()

    print(f"Version: {version}")
    print(f"Version Tuple: {version_tuple}")
    print(f"Version String: {version_string}")

    # Parse version components
    major, minor, micro = map(int, version_tuple[:3])
    print(f"Major Version: {major}")
    print(f"Minor Version: {minor}")
    print(f"Micro Version: {micro}")
    print()


def build_info():
    """Display Python build information."""
    print("=== Python Build Information ===")

    build_no, build_date = platform.python_build()
    branch = platform.python_branch()
    revision = platform.python_revision()

    print(f"Build Number: {build_no}")
    print(f"Build Date: {build_date}")

    if branch:
        print(f"Branch: {branch}")
    if revision:
        print(f"Revision: {revision}")
    print()


def implementation_details():
    """Display Python implementation details."""
    print("=== Python Implementation Details ===")

    implementation = platform.python_implementation()

    print(f"Implementation: {implementation}")

    # Implementation-specific information
    if implementation == 'CPython':
        print("• Standard Python implementation")
        print("• Written in C")
        print("• Supports C extensions")
        print("• Global Interpreter Lock (GIL)")
    elif implementation == 'PyPy':
        print("• Alternative Python implementation")
        print("• Just-In-Time (JIT) compiler")
        print("• Better performance for some workloads")
        print("• No Global Interpreter Lock (GIL)")
    elif implementation == 'Jython':
        print("• Python implementation for JVM")
        print("• Seamless Java integration")
        print("• Access to Java libraries")
    elif implementation == 'IronPython':
        print("• Python implementation for .NET CLR")
        print("• Seamless .NET integration")
        print("• Access to .NET libraries")
    else:
        print("• Other Python implementation")

    print()


def version_compatibility_check():
    """Check Python version compatibility."""
    print("=== Python Version Compatibility Check ===")

    version_tuple = platform.python_version_tuple()
    major, minor, micro = map(int, version_tuple[:3])

    print(f"Current Version: {major}.{minor}.{micro}")

    # Check compatibility with common requirements
    requirements = [
        ('Python 3.6+', (3, 6, 0)),
        ('Python 3.7+', (3, 7, 0)),
        ('Python 3.8+', (3, 8, 0)),
        ('Python 3.9+', (3, 9, 0)),
        ('Python 3.10+', (3, 10, 0)),
        ('Python 3.11+', (3, 11, 0))
    ]

    for req_name, req_version in requirements:
        compatible = (major, minor, micro) >= req_version
        status = "✓ Compatible" if compatible else "✗ Not Compatible"
        print(f"  {req_name}: {status}")

    print()


def implementation_comparison():
    """Compare different Python implementations."""
    print("=== Python Implementation Comparison ===")

    implementation = platform.python_implementation()
    version = platform.python_version()

    print(f"Current Implementation: {implementation} {version}")

    # Implementation characteristics
    impl_info = {
        'CPython': {
            'language': 'C',
            'gil': True,
            'jit': False,
            'performance': 'Standard',
            'extensions': 'C extensions'
        },
        'PyPy': {
            'language': 'RPython',
            'gil': False,
            'jit': True,
            'performance': 'Often faster',
            'extensions': 'Limited C extension support'
        },
        'Jython': {
            'language': 'Java',
            'gil': False,
            'jit': True,
            'performance': 'Varies',
            'extensions': 'Java integration'
        },
        'IronPython': {
            'language': 'C#',
            'gil': False,
            'jit': True,
            'performance': 'Varies',
            'extensions': '.NET integration'
        }
    }

    if implementation in impl_info:
        info = impl_info[implementation]
        print(f"Language: {info['language']}")
        print(f"GIL: {'Yes' if info['gil'] else 'No'}")
        print(f"JIT Compiler: {'Yes' if info['jit'] else 'No'}")
        print(f"Performance: {info['performance']}")
        print(f"Extensions: {info['extensions']}")
    else:
        print("Implementation details not available")

    print()


def python_environment_info():
    """Display Python environment information."""
    print("=== Python Environment Information ===")

    print(f"Executable: {sys.executable}")
    print(f"Prefix: {sys.prefix}")
    print(f"Base Prefix: {getattr(sys, 'base_prefix', sys.prefix)}")
    print(f"Version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Max Size: {sys.maxsize}")

    # 64-bit check
    is_64bit = sys.maxsize > 2**32
    print(f"64-bit Python: {is_64bit}")

    # Path information
    print(f"Python Path entries: {len(sys.path)}")
    print(f"Current working directory: {sys.path[0] if sys.path else 'N/A'}")

    print()


def python_info_dict():
    """Return Python runtime information as a dictionary."""
    info = {
        'timestamp': datetime.now().isoformat(),
        'version': platform.python_version(),
        'version_tuple': platform.python_version_tuple(),
        'version_string': platform.python_version_string(),
        'implementation': platform.python_implementation(),
        'compiler': platform.python_compiler(),
        'build': platform.python_build(),
        'branch': platform.python_branch(),
        'revision': platform.python_revision(),
        'executable': sys.executable,
        'prefix': sys.prefix,
        'base_prefix': getattr(sys, 'base_prefix', sys.prefix),
        'platform': sys.platform,
        'maxsize': sys.maxsize,
        'path_count': len(sys.path)
    }

    # Add analysis
    major, minor, micro = map(int, info['version_tuple'][:3])
    info['analysis'] = {
        'is_64bit': info['maxsize'] > 2**32,
        'python_3': major >= 3,
        'modern_python': (major, minor) >= (3, 8),
        'implementation_type': 'cpython' if info['implementation'] == 'CPython' else 'alternative',
        'has_branch_info': bool(info['branch']),
        'has_revision_info': bool(info['revision'])
    }

    return info


def save_python_info_to_file(filename=None):
    """Save Python runtime information to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"python_runtime_info_{timestamp}.json"

    info = python_info_dict()

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print(f"Python runtime information saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving Python info: {e}")
        return False


def python_diagnostics():
    """Perform Python runtime diagnostics."""
    print("=== Python Runtime Diagnostics ===")

    issues = []
    warnings = []

    # Check version
    version_tuple = platform.python_version_tuple()
    major, minor = map(int, version_tuple[:2])

    if major < 3:
        issues.append("Python 2 is end-of-life, consider upgrading to Python 3")
    elif (major, minor) < (3, 6):
        warnings.append("Python version is quite old, consider upgrading")

    # Check implementation
    implementation = platform.python_implementation()
    if implementation not in ['CPython', 'PyPy']:
        warnings.append(f"Using less common Python implementation: {implementation}")

    # Check for virtual environment
    in_venv = getattr(sys, 'base_prefix', sys.prefix) != sys.prefix
    if in_venv:
        print("✓ Running in virtual environment")
    else:
        warnings.append("Not running in virtual environment")

    # Report findings
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  ✗ {issue}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ⚠ {warning}")

    if not issues and not warnings:
        print("✓ Python environment looks good")

    print()


def main():
    """Main function to run all Python runtime examples."""
    print("Platform Module - Python Runtime Information Examples")
    print("=" * 56)
    print()

    # Run all examples
    basic_python_info()
    detailed_version_info()
    build_info()
    implementation_details()
    version_compatibility_check()
    implementation_comparison()
    python_environment_info()
    python_diagnostics()

    # Save Python info to file
    print("=== Saving Python Runtime Information ===")
    save_python_info_to_file()

    # Display Python info as JSON
    print("\n=== Python Runtime Information (JSON) ===")
    info = python_info_dict()
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
