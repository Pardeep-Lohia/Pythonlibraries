#!/usr/bin/env python3
"""
OS Distribution Information Implementation

This script demonstrates various ways to gather and display OS distribution information
using the platform module. All examples are cross-platform safe.
"""

import platform
import sys
import json
from datetime import datetime


def basic_distribution_info():
    """Display basic OS distribution information."""
    print("=== Basic Distribution Information ===")

    system = platform.system()
    print(f"System: {system}")

    if system == 'Linux':
        try:
            # Try modern freedesktop method first
            info = platform.freedesktop_os_release()
            print(f"Name: {info.get('NAME', 'Unknown')}")
            print(f"Version: {info.get('VERSION', 'Unknown')}")
            print(f"ID: {info.get('ID', 'Unknown')}")
        except Exception:
            # Fallback to deprecated method
            name, version, codename = platform.linux_distribution()
            print(f"Name: {name or 'Unknown'}")
            print(f"Version: {version or 'Unknown'}")
            print(f"Codename: {codename or 'Unknown'}")

    elif system == 'Windows':
        release, version, csd, ptype = platform.win32_ver()
        edition = platform.win32_edition()
        print(f"Release: {release}")
        print(f"Version: {version}")
        print(f"Service Pack: {csd or 'None'}")
        print(f"Product Type: {ptype}")
        print(f"Edition: {edition}")

    elif system == 'Darwin':
        release, versioninfo, machine = platform.mac_ver()
        print(f"Release: {release}")
        print(f"Machine: {machine}")

    else:
        print("Distribution detection not supported for this system")

    print()


def detailed_linux_info():
    """Display detailed Linux distribution information."""
    print("=== Detailed Linux Distribution Information ===")

    if platform.system() != 'Linux':
        print("This function is only for Linux systems")
        return

    # Try freedesktop.org standard
    try:
        info = platform.freedesktop_os_release()
        print("Using freedesktop.org standard:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"freedesktop method failed: {e}")

        # Fallback to deprecated method
        try:
            name, version, codename = platform.linux_distribution()
            print("Using deprecated linux_distribution:")
            print(f"  Name: {name}")
            print(f"  Version: {version}")
            print(f"  Codename: {codename}")
        except Exception as e2:
            print(f"Both methods failed: {e2}")

    print()


def windows_detailed_info():
    """Display detailed Windows version information."""
    print("=== Detailed Windows Information ===")

    if platform.system() != 'Windows':
        print("This function is only for Windows systems")
        return

    release, version, csd, ptype = platform.win32_ver()
    edition = platform.win32_edition()
    is_iot = platform.win32_is_iot()

    print(f"Release: {release}")
    print(f"Version: {version}")
    print(f"Service Pack: {csd or 'None'}")
    print(f"Product Type: {ptype}")
    print(f"Edition: {edition}")
    print(f"Windows IoT: {is_iot}")

    # Parse version for more details
    try:
        major, minor, build = map(int, version.split('.'))
        print(f"Major Version: {major}")
        print(f"Minor Version: {minor}")
        print(f"Build Number: {build}")

        # Windows version names
        version_names = {
            (10, 0): "Windows 10",
            (6, 3): "Windows 8.1",
            (6, 2): "Windows 8",
            (6, 1): "Windows 7",
            (6, 0): "Windows Vista",
            (5, 2): "Windows XP 64-bit/Windows Server 2003",
            (5, 1): "Windows XP",
            (5, 0): "Windows 2000"
        }

        version_key = (major, minor)
        if version_key in version_names:
            print(f"Version Name: {version_names[version_key]}")

    except (ValueError, IndexError):
        print("Could not parse version details")

    print()


def macos_detailed_info():
    """Display detailed macOS version information."""
    print("=== Detailed macOS Information ===")

    if platform.system() != 'Darwin':
        print("This function is only for macOS systems")
        return

    release, versioninfo, machine = platform.mac_ver()

    print(f"Release: {release}")
    print(f"Machine: {machine}")
    print(f"Version Info: {versioninfo}")

    # Parse macOS version
    try:
        major, minor, patch = map(int, release.split('.'))
        print(f"Major Version: {major}")
        print(f"Minor Version: {minor}")
        print(f"Patch Version: {patch}")

        # macOS version names
        version_names = {
            (12,): "macOS Monterey",
            (11,): "macOS Big Sur",
            (10, 15): "macOS Catalina",
            (10, 14): "macOS Mojave",
            (10, 13): "macOS High Sierra",
            (10, 12): "macOS Sierra",
            (10, 11): "macOS El Capitan",
            (10, 10): "macOS Yosemite"
        }

        # Try major.minor match first, then major only
        version_key = (major, minor)
        if version_key in version_names:
            print(f"Version Name: {version_names[version_key]}")
        elif (major,) in version_names:
            print(f"Version Name: {version_names[(major,)]}")

    except (ValueError, IndexError):
        print("Could not parse version details")

    print()


def distribution_family_detection():
    """Detect distribution family and characteristics."""
    print("=== Distribution Family Detection ===")

    system = platform.system()
    print(f"System: {system}")

    if system == 'Linux':
        try:
            info = platform.freedesktop_os_release()
            dist_id = info.get('ID', '').lower()

            # Categorize distribution family
            families = {
                'ubuntu': 'Debian-based',
                'debian': 'Debian-based',
                'linuxmint': 'Debian-based',
                'pop': 'Debian-based',
                'elementary': 'Debian-based',
                'zorin': 'Debian-based',
                'centos': 'Red Hat-based',
                'rhel': 'Red Hat-based',
                'fedora': 'Red Hat-based',
                'opensuse': 'SUSE-based',
                'sles': 'SUSE-based',
                'arch': 'Arch-based',
                'manjaro': 'Arch-based',
                'gentoo': 'Gentoo-based',
                'slackware': 'Slackware-based'
            }

            family = families.get(dist_id, 'Other')
            print(f"Distribution ID: {dist_id}")
            print(f"Family: {family}")

            # Package manager detection
            package_managers = {
                'Debian-based': 'apt/dpkg',
                'Red Hat-based': 'yum/dnf',
                'SUSE-based': 'zypper',
                'Arch-based': 'pacman',
                'Gentoo-based': 'emerge',
                'Slackware-based': 'slackpkg'
            }

            pkg_mgr = package_managers.get(family, 'Unknown')
            print(f"Package Manager: {pkg_mgr}")

        except Exception as e:
            print(f"Could not detect distribution family: {e}")

    elif system == 'Windows':
        edition = platform.win32_edition()
        print(f"Edition: {edition}")
        print("Family: Windows NT")

    elif system == 'Darwin':
        print("Family: Unix-like (BSD-based)")

    print()


def compatibility_check():
    """Check distribution compatibility for software requirements."""
    print("=== Distribution Compatibility Check ===")

    system = platform.system()
    print(f"Current System: {system}")

    # Define compatibility requirements
    requirements = {
        'Web Server Software': {
            'Linux': ['ubuntu', 'centos', 'debian', 'fedora'],
            'Windows': ['10', '11', 'Server'],
            'Darwin': ['10.12+']
        },
        'Database Software': {
            'Linux': ['ubuntu', 'centos', 'debian', 'rhel'],
            'Windows': ['10', '11', 'Server'],
            'Darwin': ['10.10+']
        },
        'Development Tools': {
            'Linux': ['all'],
            'Windows': ['10', '11'],
            'Darwin': ['10.12+']
        }
    }

    for software, reqs in requirements.items():
        if system in reqs:
            compatible = check_specific_compatibility(system, reqs[system])
            status = "✓ Compatible" if compatible else "✗ Not Compatible"
            print(f"  {software}: {status}")
        else:
            print(f"  {software}: ✗ Not supported on {system}")

    print()


def check_specific_compatibility(system, requirements):
    """Check compatibility for specific system requirements."""
    if system == 'Linux':
        try:
            info = platform.freedesktop_os_release()
            dist_id = info.get('ID', '').lower()
            return dist_id in requirements or 'all' in requirements
        except:
            return False

    elif system == 'Windows':
        edition = platform.win32_edition()
        release, _, _, _ = platform.win32_ver()
        return edition in requirements or release in requirements

    elif system == 'Darwin':
        release, _, _ = platform.mac_ver()
        return any(release.startswith(req.replace('+', '')) for req in requirements)

    return False


def distribution_info_dict():
    """Return distribution information as a dictionary."""
    system = platform.system()

    info = {
        'timestamp': datetime.now().isoformat(),
        'system': system,
        'platform': platform.platform()
    }

    if system == 'Linux':
        # Try modern method
        try:
            dist_info = platform.freedesktop_os_release()
            info['distribution'] = dist_info
            info['method'] = 'freedesktop'
        except Exception:
            # Fallback to deprecated method
            try:
                name, version, codename = platform.linux_distribution()
                info['distribution'] = {
                    'name': name,
                    'version': version,
                    'codename': codename
                }
                info['method'] = 'deprecated'
            except Exception:
                info['distribution'] = {'error': 'Could not detect Linux distribution'}
                info['method'] = 'failed'

    elif system == 'Windows':
        release, version, csd, ptype = platform.win32_ver()
        edition = platform.win32_edition()
        info['distribution'] = {
            'release': release,
            'version': version,
            'service_pack': csd,
            'product_type': ptype,
            'edition': edition,
            'is_iot': platform.win32_is_iot()
        }

    elif system == 'Darwin':
        release, versioninfo, machine = platform.mac_ver()
        info['distribution'] = {
            'release': release,
            'versioninfo': versioninfo,
            'machine': machine
        }

    else:
        info['distribution'] = {'error': f'Distribution detection not supported for {system}'}

    # Add analysis
    info['analysis'] = analyze_distribution(info)

    return info


def analyze_distribution(info):
    """Analyze distribution information."""
    system = info['system']
    analysis = {}

    if system == 'Linux' and 'distribution' in info:
        dist = info['distribution']
        if 'ID' in dist:
            dist_id = dist['ID'].lower()
            analysis['family'] = get_linux_family(dist_id)
            analysis['package_manager'] = get_package_manager(analysis['family'])
        elif 'name' in dist:
            analysis['family'] = 'Unknown'
            analysis['package_manager'] = 'Unknown'

    elif system == 'Windows' and 'distribution' in info:
        dist = info['distribution']
        analysis['is_server'] = 'server' in dist.get('product_type', '').lower()
        analysis['is_iot'] = dist.get('is_iot', False)

    elif system == 'Darwin':
        analysis['is_macos'] = True

    return analysis


def get_linux_family(dist_id):
    """Get Linux distribution family."""
    families = {
        'ubuntu': 'Debian',
        'debian': 'Debian',
        'centos': 'Red Hat',
        'rhel': 'Red Hat',
        'fedora': 'Red Hat',
        'opensuse': 'SUSE',
        'arch': 'Arch',
        'gentoo': 'Gentoo'
    }
    return families.get(dist_id, 'Other')


def get_package_manager(family):
    """Get package manager for distribution family."""
    managers = {
        'Debian': 'apt',
        'Red Hat': 'dnf/yum',
        'SUSE': 'zypper',
        'Arch': 'pacman',
        'Gentoo': 'emerge'
    }
    return managers.get(family, 'Unknown')


def save_distribution_info_to_file(filename=None):
    """Save distribution information to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"distribution_info_{timestamp}.json"

    info = distribution_info_dict()

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print(f"Distribution information saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving distribution info: {e}")
        return False


def main():
    """Main function to run all distribution examples."""
    print("Platform Module - OS Distribution Information Examples")
    print("=" * 55)
    print()

    # Run all examples
    basic_distribution_info()

    # System-specific detailed info
    if platform.system() == 'Linux':
        detailed_linux_info()
    elif platform.system() == 'Windows':
        windows_detailed_info()
    elif platform.system() == 'Darwin':
        macos_detailed_info()

    distribution_family_detection()
    compatibility_check()

    # Save distribution info to file
    print("=== Saving Distribution Information ===")
    save_distribution_info_to_file()

    # Display distribution info as JSON
    print("\n=== Distribution Information (JSON) ===")
    info = distribution_info_dict()
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
