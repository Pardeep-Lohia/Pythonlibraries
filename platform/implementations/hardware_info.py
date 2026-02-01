#!/usr/bin/env python3
"""
Hardware Information Implementation

This script demonstrates various ways to gather and display hardware information
using the platform module. All examples are cross-platform safe.
"""

import platform
import sys
import json
from datetime import datetime


def basic_hardware_info():
    """Display basic hardware information."""
    print("=== Basic Hardware Information ===")

    # Get hardware details
    machine = platform.machine()
    processor = platform.processor()
    bits, linkage = platform.architecture()

    print(f"Machine Type: {machine}")
    print(f"Processor: {processor or 'Not available'}")
    print(f"Architecture: {bits}-bit")
    print(f"Linkage: {linkage}")
    print()


def detailed_hardware_info():
    """Display detailed hardware information from uname()."""
    print("=== Detailed Hardware Information ===")

    # Get comprehensive system information
    info = platform.uname()

    print(f"Machine: {info.machine}")
    print(f"Processor: {info.processor or 'Not available'}")

    # Additional architecture info
    bits, linkage = platform.architecture()
    print(f"Architecture: {bits}")
    print(f"Executable Linkage: {linkage}")
    print()


def architecture_analysis():
    """Analyze system architecture."""
    print("=== Architecture Analysis ===")

    machine = platform.machine().lower()
    bits, linkage = platform.architecture()

    # Determine architecture family
    if machine in ['x86_64', 'amd64']:
        arch_family = 'x86-64 (Intel/AMD 64-bit)'
    elif machine in ['i386', 'i686']:
        arch_family = 'x86 (Intel/AMD 32-bit)'
    elif machine in ['arm64', 'aarch64']:
        arch_family = 'ARM 64-bit'
    elif machine.startswith('arm'):
        arch_family = 'ARM 32-bit'
    elif machine.startswith('ppc'):
        arch_family = 'PowerPC'
    else:
        arch_family = f'Other ({machine})'

    print(f"Machine String: {platform.machine()}")
    print(f"Architecture Family: {arch_family}")
    print(f"Bit Architecture: {bits}")
    print(f"Linkage Type: {linkage}")

    # Check for common architectures
    common_archs = ['x86_64', 'AMD64', 'arm64', 'aarch64']
    is_common = machine in [arch.lower() for arch in common_archs]
    print(f"Common Architecture: {is_common}")
    print()


def processor_detection():
    """Detect and analyze processor information."""
    print("=== Processor Detection ===")

    processor = platform.processor()
    machine = platform.machine()

    if processor:
        print(f"Processor String: {processor}")

        # Simple processor type detection
        proc_lower = processor.lower()

        if 'intel' in proc_lower:
            vendor = 'Intel'
        elif 'amd' in proc_lower:
            vendor = 'AMD'
        elif 'arm' in proc_lower:
            vendor = 'ARM'
        elif 'apple' in proc_lower:
            vendor = 'Apple'
        else:
            vendor = 'Other'

        print(f"Detected Vendor: {vendor}")

        # Check for virtualization indicators
        virt_indicators = ['virtual', 'vmware', 'xen', 'kvm', 'qemu', 'hypervisor']
        likely_virtual = any(indicator in proc_lower for indicator in virt_indicators)

        print(f"Likely Virtualized: {likely_virtual}")

    else:
        print("Processor information not available")
        print(f"Machine type: {machine}")

        # Fallback detection based on machine type
        if machine.lower() in ['x86_64', 'amd64']:
            print("Likely x86-64 compatible processor")
        elif machine.lower() in ['arm64', 'aarch64']:
            print("Likely ARM 64-bit processor")
    print()


def bit_architecture_check():
    """Check and analyze bit architecture."""
    print("=== Bit Architecture Check ===")

    bits, linkage = platform.architecture()
    machine = platform.machine()

    print(f"Reported Architecture: {bits}")
    print(f"Machine Type: {machine}")

    # Verify architecture consistency
    is_64bit_reported = bits == '64bit'
    is_64bit_machine = machine.lower() in ['x86_64', 'amd64', 'arm64', 'aarch64', 'ppc64']

    print(f"64-bit Reported: {is_64bit_reported}")
    print(f"64-bit Machine: {is_64bit_machine}")

    if is_64bit_reported == is_64bit_machine:
        print("✓ Architecture reporting is consistent")
    else:
        print("⚠ Architecture reporting may be inconsistent")

    # Check Python's internal bit detection
    python_bits = 64 if sys.maxsize > 2**32 else 32
    print(f"Python Internal Bits: {python_bits}-bit")

    if python_bits == int(bits.replace('bit', '')):
        print("✓ Python and platform architecture match")
    else:
        print("⚠ Python and platform architecture differ")
    print()


def hardware_capabilities():
    """Assess hardware capabilities based on detected information."""
    print("=== Hardware Capabilities Assessment ===")

    machine = platform.machine().lower()
    bits, _ = platform.architecture()

    capabilities = {
        '64bit_support': bits == '64bit',
        'x86_64': machine in ['x86_64', 'amd64'],
        'arm64': machine in ['arm64', 'aarch64'],
        'arm32': machine.startswith('arm') and not machine in ['arm64', 'aarch64'],
        'intel_amd': machine in ['x86_64', 'amd64', 'i386', 'i686'],
        'powerpc': machine.startswith('ppc'),
        'embedded': machine.startswith('arm') or machine.startswith('aarch64')
    }

    print("Detected Capabilities:")
    for capability, supported in capabilities.items():
        status = "✓" if supported else "✗"
        print(f"  {status} {capability.replace('_', ' ').title()}: {supported}")

    # Suggest use cases
    print("\nSuggested Use Cases:")
    if capabilities['x86_64']:
        print("  • General-purpose computing")
        print("  • Scientific computing")
        print("  • Server applications")
    if capabilities['arm64']:
        print("  • Mobile/embedded systems")
        print("  • Energy-efficient computing")
        print("  • IoT devices")
    if capabilities['embedded']:
        print("  • Embedded systems")
        print("  • Single-board computers")
    print()


def hardware_info_dict():
    """Return hardware information as a dictionary."""
    bits, linkage = platform.architecture()

    info = {
        'timestamp': datetime.now().isoformat(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'architecture_bits': bits,
        'architecture_linkage': linkage,
        'uname_machine': platform.uname().machine,
        'uname_processor': platform.uname().processor,
        'python_bits': 64 if sys.maxsize > 2**32 else 32
    }

    # Add analysis
    machine_lower = info['machine'].lower()
    info['analysis'] = {
        'is_64bit': bits == '64bit',
        'architecture_family': get_architecture_family(machine_lower),
        'likely_virtualized': is_likely_virtualized(info['processor']),
        'common_architecture': machine_lower in ['x86_64', 'amd64', 'arm64', 'aarch64']
    }

    return info


def get_architecture_family(machine):
    """Determine architecture family from machine string."""
    if machine in ['x86_64', 'amd64']:
        return 'x86-64'
    elif machine in ['i386', 'i686']:
        return 'x86'
    elif machine in ['arm64', 'aarch64']:
        return 'ARM64'
    elif machine.startswith('arm'):
        return 'ARM'
    elif machine.startswith('ppc'):
        return 'PowerPC'
    else:
        return 'Other'


def is_likely_virtualized(processor):
    """Check if processor string indicates virtualization."""
    if not processor:
        return False

    virt_indicators = ['virtual', 'vmware', 'xen', 'kvm', 'qemu', 'hypervisor', 'virtualbox']
    return any(indicator.lower() in processor.lower() for indicator in virt_indicators)


def save_hardware_info_to_file(filename=None):
    """Save hardware information to a JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hardware_info_{timestamp}.json"

    info = hardware_info_dict()

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print(f"Hardware information saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving hardware info: {e}")
        return False


def hardware_compatibility_check():
    """Check hardware compatibility for common software."""
    print("=== Hardware Compatibility Check ===")

    machine = platform.machine().lower()
    bits, _ = platform.architecture()

    # Define compatibility requirements
    requirements = {
        'modern_software': {
            'min_bits': 64,
            'supported_arch': ['x86_64', 'amd64', 'arm64', 'aarch64']
        },
        'legacy_software': {
            'min_bits': 32,
            'supported_arch': ['x86_64', 'amd64', 'i386', 'i686', 'arm64', 'aarch64', 'arm']
        },
        'embedded_systems': {
            'min_bits': 32,
            'supported_arch': ['arm64', 'aarch64', 'arm']
        }
    }

    current_bits = int(bits.replace('bit', ''))
    current_arch = machine

    print(f"Current Hardware: {current_bits}-bit {current_arch.upper()}")

    for software_type, reqs in requirements.items():
        compatible = (current_bits >= reqs['min_bits'] and
                     current_arch in reqs['supported_arch'])

        status = "✓ Compatible" if compatible else "✗ Not Compatible"
        print(f"  {software_type.replace('_', ' ').title()}: {status}")

    print()


def main():
    """Main function to run all hardware examples."""
    print("Platform Module - Hardware Information Examples")
    print("=" * 50)
    print()

    # Run all examples
    basic_hardware_info()
    detailed_hardware_info()
    architecture_analysis()
    processor_detection()
    bit_architecture_check()
    hardware_capabilities()
    hardware_compatibility_check()

    # Save hardware info to file
    print("=== Saving Hardware Information ===")
    save_hardware_info_to_file()

    # Display hardware info as JSON
    print("\n=== Hardware Information (JSON) ===")
    info = hardware_info_dict()
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
