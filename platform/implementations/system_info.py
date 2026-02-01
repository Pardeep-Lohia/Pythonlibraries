#!/usr/bin/env python3
"""
System Information Implementation

This script demonstrates various ways to gather and display system information
using the platform module. All examples are cross-platform safe.
"""

import platform
import sys
import json
from datetime import datetime


def basic_system_info():
    """Display basic system information."""
    print("=== Basic System Information ===")

    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()

    print(f"Operating System: {system}")
    print(f"Release: {release}")
    print(f"Version: {version}")
    print(f"Machine: {machine}")
    print(f"Processor: {processor or 'Not available'}")
    print()


def uname_system_info():
    """Display system information using uname()."""
    print("=== uname() System Information ===")

    uname_info = platform.uname()

    print(f"System: {uname_info.system}")
    print(f"Node (hostname): {uname_info.node}")
    print(f"Release: {uname_info.release}")
    print(f"Version: {uname_info.version}")
    print(f"Machine: {uname_info.machine}")
    print(f"Processor: {uname_info.processor or 'Not available'}")
    print()


def platform_string_info():
    """Display platform string information."""
    print("=== Platform String Information ===")

    # Different platform string variations
    platform_default = platform.platform()
    platform_aliased = platform.platform(aliased=True)
    platform_terse = platform.platform(terse=True)

    print(f"Full Platform: {platform_default}")
    print(f"Aliased Platform: {platform_aliased}")
    print(f"Terse Platform: {platform_terse}")
    print()


def architecture_info():
    """Display system architecture information."""
    print("=== Architecture Information ===")

    bits, linkage = platform.architecture()
    machine = platform.machine()

    print(f"Architecture: {bits}-bit")
    print(f"Linkage: {linkage}")
    print(f"Machine Type: {machine}")

    # Determine if 64-bit
    is_64bit = bits == '64bit'
    print(f"64-bit System: {is_64bit}")
    print()


def system_comparison():
    """Compare different system information sources."""
    print("=== System Information Comparison ===")

    system = platform.system()
    uname_system = platform.uname().system

    print(f"platform.system(): {system}")
    print(f"platform.uname().system: {uname_system}")
    print(f"Match: {system == uname_system}")

    # Compare with sys.platform
    import sys
    print(f"sys.platform: {sys.platform}")

    # Check consistency
    if system == uname_system:
        print("✓ platform.system() and uname().system are consistent")
    else:
        print("⚠ platform.system() and uname().system differ")
    print()


def system_info_summary():
    """Display a summary of system information."""
    print("=== System Information Summary ===")

    uname_info = platform.uname()
    bits, _ = platform.architecture()

    summary = {
        'os': uname_info.system,
        'hostname': uname_info.node,
        'kernel_release': uname_info.release,
        'architecture': f"{bits} ({uname_info.machine})",
        'processor': uname_info.processor or 'Unknown'
    }

    for key, value in summary.items():
        print(f"{key.capitalize()}: {value}")

    print()


def system_compatibility_check():
    """Check system compatibility for common software."""
    print("=== System Compatibility Check ===")

    system = platform.system()
    machine = platform.machine()
    bits, _ = platform.architecture()

    print(f"Current System: {system} {machine} ({bits})")

    # Define compatibility requirements
    compat_checks = {
        'Modern Applications': {
            'systems': ['Windows', 'Linux', 'Darwin'],
            'architectures': ['x86_64', 'AMD64', 'arm64', 'aarch64'],
            'min_bits': '64bit'
        },
        'Legacy Software': {
            'systems': ['Windows', 'Linux', 'Darwin'],
            'architectures': ['x86_64', 'AMD64', 'i386', 'i686'],
            'min_bits': '32bit'
        },
        'Embedded Systems': {
            'systems': ['Linux'],
            'architectures': ['arm64', 'aarch64', 'arm'],
            'min_bits': '32bit'
        }
    }

    for software_type, reqs in compat_checks.items():
        compatible = (
            system in reqs['systems'] and
            machine in reqs['architectures'] and
            (bits == reqs['min_bits'] or (reqs['min_bits'] == '32bit' and bits == '64bit'))
        )

        status = "✓ Compatible" if compatible else "✗ Not Compatible"
        print(f"  {software_type}: {status}")

    print()


def system_info_dict():
    """Return system information as a dictionary."""
    uname_info = platform.uname()
    bits, linkage = platform.architecture()

    info = {
        'timestamp': datetime.now().isoformat(),
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'platform': platform.platform(),
        'architecture_bits': bits,
        'architecture_linkage': linkage,
        'hostname': uname_info.node,
        'uname': uname_info._asdict()
    }

    # Add analysis
    info['analysis'] = {
        'is_64bit': bits == '64bit',
        'is_windows': info['system'] == 'Windows',
        'is_linux': info['system'] == 'Linux',
        'is_macos': info['system'] == 'Darwin',
        'common_architecture': info['machine'].lower() in ['x86_64', 'amd64', 'arm64', 'aarch64']
    }

    return info


def save_system_info_to_file(filename=None):
    """Save system information to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_info_{timestamp}.json"

    info = system_info_dict()

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print(f"System information saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving system info: {e}")
        return False


def system_diagnostics():
    """Perform basic system diagnostics."""
    print("=== System Diagnostics ===")

    issues = []
    warnings = []

    # Check for basic information availability
    system = platform.system()
    if not system:
        issues.append("Unable to determine operating system")

    machine = platform.machine()
    if not machine:
        warnings.append("Unable to determine machine architecture")

    processor = platform.processor()
    if not processor:
        warnings.append("Processor information not available")

    # Check architecture consistency
    bits, _ = platform.architecture()
    uname_machine = platform.uname().machine

    if machine and uname_machine and machine != uname_machine:
        warnings.append(f"Machine type mismatch: {machine} vs {uname_machine}")

    # Report findings
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  ✗ {issue}")
    else:
        print("✓ No critical issues found")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ⚠ {warning}")

    if not issues and not warnings:
        print("✓ System information looks good")

    print()


def main():
    """Main function to run all system information examples."""
    print("Platform Module - System Information Examples")
    print("=" * 48)
    print()

    # Run all examples
    basic_system_info()
    uname_system_info()
    platform_string_info()
    architecture_info()
    system_comparison()
    system_info_summary()
    system_compatibility_check()
    system_diagnostics()

    # Save system info to file
    print("=== Saving System Information ===")
    save_system_info_to_file()

    # Display system info as JSON
    print("\n=== System Information (JSON) ===")
    info = system_info_dict()
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
