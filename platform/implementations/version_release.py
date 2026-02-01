#!/usr/bin/env python3
"""
Version and Release Information Implementation

This script demonstrates various ways to gather and display version and release information
using the platform module. All examples are cross-platform safe.
"""

import platform
import sys
import json
from datetime import datetime


def basic_version_info():
    """Display basic version and release information."""
    print("=== Basic Version and Release Information ===")

    system = platform.system()
    release = platform.release()
    version = platform.version()
    platform_str = platform.platform()

    print(f"System: {system}")
    print(f"Release: {release}")
    print(f"Version: {version}")
    print(f"Platform: {platform_str}")
    print()


def detailed_uname_info():
    """Display detailed information from uname()."""
    print("=== Detailed uname() Information ===")

    info = platform.uname()

    print(f"System: {info.system}")
    print(f"Node: {info.node}")
    print(f"Release: {info.release}")
    print(f"Version: {info.version}")
    print(f"Machine: {info.machine}")
    print(f"Processor: {info.processor or 'Not available'}")
    print()


def version_parsing():
    """Parse and analyze version strings."""
    print("=== Version Parsing and Analysis ===")

    system = platform.system()
    release = platform.release()
    version = platform.version()

    print(f"Raw Release: {release}")
    print(f"Raw Version: {version}")

    # Parse based on system
    if system == 'Linux':
        # Linux kernel version parsing
        kernel_parts = release.split('-')[0].split('.')
        if len(kernel_parts) >= 3:
            try:
                major, minor, patch = map(int, kernel_parts[:3])
                print(f"Kernel Version: {major}.{minor}.{patch}")
                print(f"Kernel Major: {major}")
                print(f"Kernel Minor: {minor}")
                print(f"Kernel Patch: {patch}")
            except ValueError:
                print("Could not parse kernel version numbers")

    elif system == 'Windows':
        # Windows version parsing
        win_release, win_version, csd, ptype = platform.win32_ver()
        try:
            version_parts = win_version.split('.')
            if len(version_parts) >= 3:
                major, minor, build = map(int, version_parts[:3])
                print(f"Windows Version: {major}.{minor}.{build}")
                print(f"Windows Major: {major}")
                print(f"Windows Minor: {minor}")
                print(f"Windows Build: {build}")
                print(f"Service Pack: {csd or 'None'}")
        except ValueError:
            print("Could not parse Windows version numbers")

    elif system == 'Darwin':
        # macOS version parsing
        mac_release, _, _ = platform.mac_ver()
        try:
            version_parts = mac_release.split('.')
            if len(version_parts) >= 2:
                major, minor = map(int, version_parts[:2])
                patch = int(version_parts[2]) if len(version_parts) > 2 else 0
                print(f"macOS Version: {major}.{minor}.{patch}")
                print(f"macOS Major: {major}")
                print(f"macOS Minor: {minor}")
                print(f"macOS Patch: {patch}")
        except ValueError:
            print("Could not parse macOS version numbers")

    print()


def version_comparison():
    """Demonstrate version comparison logic."""
    print("=== Version Comparison Examples ===")

    system = platform.system()

    if system == 'Linux':
        current_kernel = platform.release().split('-')[0]
        print(f"Current Kernel: {current_kernel}")

        # Test versions
        test_versions = ['4.0.0', '5.0.0', '5.4.0', '5.10.0', '6.0.0']
        for test_ver in test_versions:
            result = version_compare(current_kernel, test_ver)
            status = "≥" if result else "<"
            print(f"  {current_kernel} {status} {test_ver}")

    elif system == 'Windows':
        _, win_version, _, _ = platform.win32_ver()
        print(f"Current Windows: {win_version}")

        # Test versions
        test_versions = ['6.1', '10.0', '10.0.19041', '11.0']
        for test_ver in test_versions:
            result = version_compare(win_version, test_ver)
            status = "≥" if result else "<"
            print(f"  {win_version} {status} {test_ver}")

    elif system == 'Darwin':
        mac_release, _, _ = platform.mac_ver()
        print(f"Current macOS: {mac_release}")

        # Test versions
        test_versions = ['10.12', '10.15', '11.0', '12.0']
        for test_ver in mac_release.split('.'):
            for test_ver in test_versions:
                result = version_compare(mac_release, test_ver)
                status = "≥" if result else "<"
                print(f"  {mac_release} {status} {test_ver}")

    print()


def version_compare(current, required):
    """Simple version comparison function."""
    try:
        # Split versions into parts
        current_parts = current.split('.')
        required_parts = required.split('.')

        # Convert to integers where possible
        current_nums = []
        required_nums = []

        for part in current_parts:
            try:
                current_nums.append(int(part))
            except ValueError:
                current_nums.append(part)

        for part in required_parts:
            try:
                required_nums.append(int(part))
            except ValueError:
                required_nums.append(part)

        # Pad shorter version with zeros
        max_len = max(len(current_nums), len(required_nums))
        current_nums.extend([0] * (max_len - len(current_nums)))
        required_nums.extend([0] * (max_len - len(required_nums)))

        # Compare
        return current_nums >= required_nums

    except Exception:
        return False


def compatibility_check():
    """Check version compatibility for common software."""
    print("=== Version Compatibility Check ===")

    system = platform.system()
    print(f"System: {system}")

    # Define minimum version requirements
    requirements = {
        'Python 3.8+ Applications': '3.8.0',
        'Modern Web Frameworks': '3.6.0',
        'Scientific Computing': '3.7.0',
        'Legacy Applications': '2.7.0'
    }

    python_version = platform.python_version()
    print(f"Python Version: {python_version}")

    for software, min_version in requirements.items():
        compatible = version_compare(python_version, min_version)
        status = "✓ Compatible" if compatible else "✗ Not Compatible"
        print(f"  {software}: {status} (requires {min_version})")

    # System-specific requirements
    if system == 'Linux':
        kernel_ver = platform.release().split('-')[0]
        print(f"\nLinux Kernel: {kernel_ver}")

        kernel_requirements = {
            'Modern Linux Software': '3.10.0',
            'Container Runtimes': '4.0.0',
            'Latest Features': '5.4.0'
        }

        for feature, min_kernel in kernel_requirements.items():
            compatible = version_compare(kernel_ver, min_kernel)
            status = "✓ Supported" if compatible else "✗ Not Supported"
            print(f"  {feature}: {status} (requires kernel {min_kernel})")

    elif system == 'Windows':
        win_release, win_version, _, _ = platform.win32_ver()
        print(f"\nWindows Version: {win_version}")

        windows_requirements = {
            'Windows 10 Apps': '10.0',
            'Modern Windows Software': '6.1',  # Windows 7
            'Latest Windows Features': '10.0.19041'
        }

        for feature, min_win in windows_requirements.items():
            compatible = version_compare(win_version, min_win)
            status = "✓ Supported" if compatible else "✗ Not Supported"
            print(f"  {feature}: {status} (requires Windows {min_win})")

    elif system == 'Darwin':
        mac_release, _, _ = platform.mac_ver()
        print(f"\nmacOS Version: {mac_release}")

        macos_requirements = {
            'Modern macOS Apps': '10.12',
            'Latest macOS Features': '10.15',
            'Apple Silicon Apps': '11.0'
        }

        for feature, min_mac in macos_requirements.items():
            compatible = version_compare(mac_release, min_mac)
            status = "✓ Supported" if compatible else "✗ Not Supported"
            print(f"  {feature}: {status} (requires macOS {min_mac})")

    print()


def version_info_dict():
    """Return version and release information as a dictionary."""
    system = platform.system()

    info = {
        'timestamp': datetime.now().isoformat(),
        'system': system,
        'release': platform.release(),
        'version': platform.version(),
        'platform': platform.platform(),
        'uname': platform.uname()._asdict(),
        'python_version': platform.python_version(),
        'python_version_tuple': platform.python_version_tuple()
    }

    # Add system-specific information
    if system == 'Linux':
        try:
            dist_info = platform.freedesktop_os_release()
            info['distribution'] = dist_info
        except:
            info['distribution'] = platform.linux_distribution()

    elif system == 'Windows':
        info['windows_info'] = platform.win32_ver()
        info['windows_edition'] = platform.win32_edition()

    elif system == 'Darwin':
        info['mac_info'] = platform.mac_ver()

    # Add analysis
    info['analysis'] = analyze_versions(info)

    return info


def analyze_versions(info):
    """Analyze version information."""
    system = info['system']
    analysis = {}

    # Python version analysis
    python_ver = info['python_version']
    try:
        major, minor, micro = map(int, python_ver.split('.')[:3])
        analysis['python_major'] = major
        analysis['python_minor'] = minor
        analysis['python_micro'] = micro
        analysis['python_3_plus'] = major >= 3
        analysis['python_modern'] = (major, minor) >= (3, 8)
    except (ValueError, IndexError):
        analysis['python_version_error'] = 'Could not parse Python version'

    # System-specific analysis
    if system == 'Linux':
        kernel_ver = info['release'].split('-')[0]
        try:
            k_major, k_minor = map(int, kernel_ver.split('.')[:2])
            analysis['kernel_major'] = k_major
            analysis['kernel_minor'] = k_minor
            analysis['kernel_modern'] = (k_major, k_minor) >= (5, 4)
        except (ValueError, IndexError):
            analysis['kernel_version_error'] = 'Could not parse kernel version'

    elif system == 'Windows':
        win_ver = info['windows_info'][1]  # version string
        try:
            major = int(win_ver.split('.')[0])
            analysis['windows_major'] = major
            analysis['windows_modern'] = major >= 10
        except (ValueError, IndexError):
            analysis['windows_version_error'] = 'Could not parse Windows version'

    elif system == 'Darwin':
        mac_ver = info['mac_info'][0]
        try:
            major = int(mac_ver.split('.')[0])
            analysis['macos_major'] = major
            analysis['macos_modern'] = major >= 10
        except (ValueError, IndexError):
            analysis['macos_version_error'] = 'Could not parse macOS version'

    return analysis


def save_version_info_to_file(filename=None):
    """Save version and release information to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"version_info_{timestamp}.json"

    info = version_info_dict()

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print(f"Version information saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving version info: {e}")
        return False


def version_history_demo():
    """Demonstrate version history and evolution."""
    print("=== Version History and Evolution ===")

    system = platform.system()
    print(f"Current System: {system}")

    if system == 'Linux':
        kernel = platform.release().split('-')[0]
        print(f"Current Kernel: {kernel}")

        # Linux kernel milestones
        milestones = [
            ('1.0', '1994', 'First stable Linux kernel'),
            ('2.0', '1996', 'SMP support'),
            ('2.4', '2001', 'Improved scalability'),
            ('2.6', '2003', 'Current stable branch'),
            ('3.0', '2011', 'Namespace support'),
            ('4.0', '2015', 'Live patching'),
            ('5.0', '2019', 'Modern features'),
            ('6.0', '2022', 'Latest major release')
        ]

        print("\nLinux Kernel Milestones:")
        for ver, year, desc in milestones:
            reached = version_compare(kernel, ver)
            status = "✓ Reached" if reached else "Future"
            print(f"  {ver} ({year}): {desc} - {status}")

    elif system == 'Windows':
        _, win_ver, _, _ = platform.win32_ver()
        print(f"Current Windows: {win_ver}")

        # Windows version history
        milestones = [
            ('5.1', '2001', 'Windows XP'),
            ('6.0', '2006', 'Windows Vista'),
            ('6.1', '2009', 'Windows 7'),
            ('6.2', '2012', 'Windows 8'),
            ('6.3', '2013', 'Windows 8.1'),
            ('10.0', '2015', 'Windows 10'),
            ('11.0', '2021', 'Windows 11')
        ]

        print("\nWindows Version History:")
        for ver, year, desc in milestones:
            reached = version_compare(win_ver, ver)
            status = "✓ Current or earlier" if reached else "Future"
            print(f"  {ver} ({year}): {desc} - {status}")

    elif system == 'Darwin':
        mac_ver, _, _ = platform.mac_ver()
        print(f"Current macOS: {mac_ver}")

        # macOS version history
        milestones = [
            ('10.0', '2000', 'Mac OS X Cheetah'),
            ('10.4', '2005', 'Mac OS X Tiger'),
            ('10.6', '2009', 'Mac OS X Snow Leopard'),
            ('10.8', '2012', 'OS X Mountain Lion'),
            ('10.10', '2014', 'OS X Yosemite'),
            ('10.12', '2016', 'macOS Sierra'),
            ('10.14', '2018', 'macOS Mojave'),
            ('10.15', '2019', 'macOS Catalina'),
            ('11.0', '2020', 'macOS Big Sur'),
            ('12.0', '2021', 'macOS Monterey')
        ]

        print("\nmacOS Version History:")
        for ver, year, desc in milestones:
            reached = version_compare(mac_ver, ver)
            status = "✓ Current or earlier" if reached else "Future"
            print(f"  {ver} ({year}): {desc} - {status}")

    print()


def main():
    """Main function to run all version and release examples."""
    print("Platform Module - Version and Release Information Examples")
    print("=" * 58)
    print()

    # Run all examples
    basic_version_info()
    detailed_uname_info()
    version_parsing()
    version_comparison()
    compatibility_check()
    version_history_demo()

    # Save version info to file
    print("=== Saving Version Information ===")
    save_version_info_to_file()

    # Display version info as JSON
    print("\n=== Version Information (JSON) ===")
    info = version_info_dict()
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
