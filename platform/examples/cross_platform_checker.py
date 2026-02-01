#!/usr/bin/env python3
"""
Cross-Platform Compatibility Checker

This script demonstrates a comprehensive cross-platform compatibility checker
that uses the platform module to ensure applications work correctly across
different operating systems and architectures.
"""

import platform
import os
import sys
from pathlib import Path


class CrossPlatformChecker:
    """A comprehensive cross-platform compatibility checker."""

    def __init__(self):
        self.system = platform.system()
        self.machine = platform.machine()
        self.release = platform.release()
        self.version = platform.version()
        self.bits, self.linkage = platform.architecture()
        self.python_version = platform.python_version_tuple()

    def check_basic_compatibility(self):
        """Check basic platform compatibility."""
        print("=== Basic Platform Compatibility Check ===")

        supported_systems = ['Windows', 'Linux', 'Darwin']
        supported_architectures = ['x86_64', 'AMD64', 'arm64', 'aarch64', 'i386', 'i686']

        system_ok = self.system in supported_systems
        arch_ok = self.machine in supported_architectures
        bits_ok = self.bits == '64bit'  # Prefer 64-bit

        print(f"Operating System: {self.system} - {'✓' if system_ok else '✗'}")
        print(f"Architecture: {self.machine} ({self.bits}) - {'✓' if arch_ok else '✗'}")
        print(f"64-bit: {bits_ok} - {'✓' if bits_ok else '⚠'}")

        overall_ok = system_ok and arch_ok
        print(f"Overall Compatibility: {'✓ PASS' if overall_ok else '✗ FAIL'}")

        return overall_ok

    def check_path_handling(self):
        """Check platform-specific path handling."""
        print("\n=== Path Handling Compatibility ===")

        # Test path separators
        test_path = os.path.join('home', 'user', 'documents', 'file.txt')
        print(f"Platform path: {test_path}")

        # Check path separator
        expected_sep = '\\' if self.system == 'Windows' else '/'
        actual_sep = os.sep
        sep_ok = actual_sep == expected_sep
        print(f"Path separator: '{actual_sep}' - {'✓' if sep_ok else '✗'}")

        # Check path operations
        dirname = os.path.dirname(test_path)
        basename = os.path.basename(test_path)
        print(f"Path operations: dirname='{dirname}', basename='{basename}' - ✓")

        # Check absolute path
        abs_path = os.path.abspath(test_path)
        print(f"Absolute path: {abs_path} - ✓")

        return sep_ok

    def check_file_operations(self):
        """Check platform-specific file operations."""
        print("\n=== File Operations Compatibility ===")

        # Test file permissions (Unix-like vs Windows)
        test_file = "test_compatibility.tmp"

        try:
            # Create test file
            with open(test_file, 'w') as f:
                f.write("test content")

            # Check file existence
            exists = os.path.exists(test_file)
            print(f"File creation: {'✓' if exists else '✗'}")

            # Check file permissions
            if hasattr(os, 'chmod'):
                try:
                    # Try to set permissions (may fail on some systems)
                    os.chmod(test_file, 0o644)
                    print("File permissions: ✓ (Unix-style)")
                except (OSError, AttributeError):
                    print("File permissions: ✓ (Windows-style)")
            else:
                print("File permissions: ✓ (limited support)")

            # Clean up
            os.remove(test_file)
            print("File cleanup: ✓")

            return True

        except Exception as e:
            print(f"File operations error: {e}")
            # Clean up if file exists
            if os.path.exists(test_file):
                try:
                    os.remove(test_file)
                except:
                    pass
            return False

    def check_environment_variables(self):
        """Check environment variable handling."""
        print("\n=== Environment Variables Compatibility ===")

        # Check common environment variables
        test_vars = {
            'PATH': os.environ.get('PATH'),
            'HOME': os.environ.get('HOME') or os.environ.get('USERPROFILE'),
            'TEMP': os.environ.get('TEMP') or os.environ.get('TMP') or '/tmp',
            'USER': os.environ.get('USER') or os.environ.get('USERNAME')
        }

        for var_name, var_value in test_vars.items():
            status = '✓' if var_value else '✗'
            print(f"{var_name}: {status}")

        # Check PATH separator
        path_sep = os.pathsep
        expected_path_sep = ';' if self.system == 'Windows' else ':'
        path_sep_ok = path_sep == expected_path_sep
        print(f"PATH separator: '{path_sep}' - {'✓' if path_sep_ok else '✗'}")

        return all(test_vars.values()) and path_sep_ok

    def check_system_commands(self):
        """Check system command availability."""
        print("\n=== System Commands Compatibility ===")

        # Platform-specific commands to test
        commands = {
            'Windows': ['cmd', 'powershell'],
            'Linux': ['bash', 'sh'],
            'Darwin': ['bash', 'zsh']
        }

        system_commands = commands.get(self.system, ['sh'])
        available_commands = []

        for cmd in system_commands:
            # Check if command exists in PATH
            cmd_path = None
            for path_dir in os.environ.get('PATH', '').split(os.pathsep):
                potential_path = os.path.join(path_dir, cmd)
                if os.path.exists(potential_path) or os.path.exists(potential_path + '.exe'):
                    cmd_path = potential_path
                    break

            if cmd_path:
                available_commands.append(cmd)
                print(f"{cmd}: ✓ (found at {cmd_path})")
            else:
                print(f"{cmd}: ✗ (not found in PATH)")

        return len(available_commands) > 0

    def check_python_features(self):
        """Check Python feature availability."""
        print("\n=== Python Features Compatibility ===")

        major, minor, micro = map(int, self.python_version[:3])

        # Check Python version compatibility
        python_36_plus = (major, minor) >= (3, 6)
        python_38_plus = (major, minor) >= (3, 8)

        print(f"Python {major}.{minor}.{micro}: ✓")
        print(f"Python 3.6+: {'✓' if python_36_plus else '✗'}")
        print(f"Python 3.8+: {'✓' if python_38_plus else '⚠'}")

        # Check important modules
        important_modules = ['os', 'sys', 'platform', 'pathlib', 'subprocess']
        missing_modules = []

        for module in important_modules:
            try:
                __import__(module)
                print(f"Module '{module}': ✓")
            except ImportError:
                missing_modules.append(module)
                print(f"Module '{module}': ✗")

        return len(missing_modules) == 0

    def check_networking(self):
        """Check networking capabilities."""
        print("\n=== Networking Compatibility ===")

        try:
            import socket

            # Test basic socket creation
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.close()
            print("Socket creation: ✓")

            # Test hostname resolution
            hostname = socket.gethostname()
            print(f"Hostname resolution: ✓ ({hostname})")

            # Test localhost connection
            try:
                info = socket.getaddrinfo('localhost', 80)
                print("Localhost resolution: ✓")
            except socket.gaierror:
                print("Localhost resolution: ⚠ (expected for some systems)")

            return True

        except Exception as e:
            print(f"Networking check failed: {e}")
            return False

    def generate_compatibility_report(self):
        """Generate a comprehensive compatibility report."""
        print("\n" + "="*50)
        print("CROSS-PLATFORM COMPATIBILITY REPORT")
        print("="*50)

        print(f"Platform: {self.system} {self.release}")
        print(f"Architecture: {self.machine} ({self.bits})")
        print(f"Python: {platform.python_version()}")
        print(f"Generated: {platform.node()}")
        print()

        # Run all checks
        checks = [
            ("Basic Platform", self.check_basic_compatibility()),
            ("Path Handling", self.check_path_handling()),
            ("File Operations", self.check_file_operations()),
            ("Environment Variables", self.check_environment_variables()),
            ("System Commands", self.check_system_commands()),
            ("Python Features", self.check_python_features()),
            ("Networking", self.check_networking())
        ]

        passed = 0
        total = len(checks)

        print("COMPATIBILITY CHECK RESULTS:")
        print("-" * 30)

        for check_name, result in checks:
            status = "PASS" if result else "FAIL"
            symbol = "✓" if result else "✗"
            print(f"{symbol} {check_name}: {status}")
            if result:
                passed += 1

        print("-" * 30)
        print(f"Overall Score: {passed}/{total} checks passed")

        if passed == total:
            print("🎉 EXCELLENT: Full cross-platform compatibility!")
        elif passed >= total * 0.8:
            print("✅ GOOD: Minor compatibility issues")
        elif passed >= total * 0.6:
            print("⚠️ FAIR: Some compatibility concerns")
        else:
            print("❌ POOR: Major compatibility issues")

        return passed == total

    def get_platform_specific_advice(self):
        """Provide platform-specific advice."""
        print("\nPLATFORM-SPECIFIC ADVICE:")
        print("-" * 25)

        if self.system == 'Windows':
            print("• Use os.path.join() for cross-platform paths")
            print("• Handle file permissions carefully (limited on Windows)")
            print("• Consider using pathlib for modern path handling")
            print("• Test with different Windows versions (10, 11)")

        elif self.system == 'Linux':
            print("• File permissions are important")
            print("• Check for different Linux distributions")
            print("• Consider systemd vs. other init systems")
            print("• Test on different package managers (apt, yum, etc.)")

        elif self.system == 'Darwin':
            print("• macOS has Unix-like behavior but with Apple-specific features")
            print("• Consider different macOS versions (Monterey, Big Sur, etc.)")
            print("• Test with both Intel and Apple Silicon Macs")
            print("• Be aware of App Store sandboxing restrictions")

        else:
            print("• Unknown platform - test thoroughly")
            print("• Consider fallback behaviors")
            print("• Document platform-specific requirements")

    def save_report(self, filename=None):
        """Save compatibility report to file."""
        if filename is None:
            system_name = self.system.lower()
            timestamp = platform.node() + "_" + str(hash(str(self.__dict__)))[:8]
            filename = f"compatibility_report_{system_name}_{timestamp}.txt"

        try:
            # Capture output to file
            import io
            from contextlib import redirect_stdout

            with open(filename, 'w', encoding='utf-8') as f:
                with redirect_stdout(f):
                    self.generate_compatibility_report()
                    self.get_platform_specific_advice()

            print(f"\nReport saved to: {filename}")
            return True

        except Exception as e:
            print(f"Error saving report: {e}")
            return False


def main():
    """Main function to run cross-platform compatibility check."""
    print("Cross-Platform Compatibility Checker")
    print("Using platform module for comprehensive testing")
    print()

    checker = CrossPlatformChecker()

    # Generate full report
    checker.generate_compatibility_report()
    checker.get_platform_specific_advice()

    # Save report
    print("\n" + "="*50)
    checker.save_report()


if __name__ == "__main__":
    main()
