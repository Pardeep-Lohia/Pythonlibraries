#!/usr/bin/env python3
"""
Environment Diagnostics Tool

This script demonstrates a comprehensive environment diagnostics tool that uses
the platform module to gather and analyze system information for troubleshooting
and system analysis purposes.
"""

import platform
import sys
import os
import psutil
from datetime import datetime
from pathlib import Path


class EnvironmentDiagnostics:
    """A comprehensive environment diagnostics tool."""

    def __init__(self):
        self.system_info = self._gather_system_info()
        self.python_info = self._gather_python_info()
        self.hardware_info = self._gather_hardware_info()
        self.environment_info = self._gather_environment_info()

    def _gather_system_info(self):
        """Gather comprehensive system information."""
        uname_info = platform.uname()

        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'platform': platform.platform(),
            'hostname': uname_info.node,
            'architecture': platform.architecture(),
            'uname': uname_info._asdict()
        }

    def _gather_python_info(self):
        """Gather Python runtime information."""
        return {
            'version': platform.python_version(),
            'version_tuple': platform.python_version_tuple(),
            'implementation': platform.python_implementation(),
            'compiler': platform.python_compiler(),
            'build': platform.python_build(),
            'branch': platform.python_branch(),
            'revision': platform.python_revision(),
            'version_string': platform.python_version_string(),
            'executable': sys.executable,
            'path': sys.path,
            'prefix': sys.prefix,
            'base_prefix': getattr(sys, 'base_prefix', sys.prefix),
            'maxsize': sys.maxsize,
            'version_info': sys.version_info._asdict()
        }

    def _gather_hardware_info(self):
        """Gather hardware-related information."""
        try:
            import psutil
            has_psutil = True
        except ImportError:
            has_psutil = False

        info = {
            'cpu_count': os.cpu_count(),
            'has_psutil': has_psutil
        }

        if has_psutil:
            info.update({
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': psutil.virtual_memory()._asdict(),
                'disk_usage': psutil.disk_usage('/')._asdict(),
                'network_interfaces': list(psutil.net_if_addrs().keys())
            })

        return info

    def _gather_environment_info(self):
        """Gather environment and configuration information."""
        return {
            'environment_variables': dict(os.environ),
            'current_working_directory': os.getcwd(),
            'user_home': Path.home(),
            'temp_directory': Path(os.environ.get('TEMP', '/tmp')),
            'path_directories': os.environ.get('PATH', '').split(os.pathsep),
            'umask': oct(os.umask(os.umask(0))),  # Get and restore umask
            'process_id': os.getpid(),
            'parent_process_id': os.getppid()
        }

    def run_full_diagnostics(self):
        """Run complete environment diagnostics."""
        print("=== Environment Diagnostics Report ===")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Hostname: {self.system_info['hostname']}")
        print("=" * 50)
        print()

        self._print_system_diagnostics()
        self._print_python_diagnostics()
        self._print_hardware_diagnostics()
        self._print_environment_diagnostics()
        self._print_compatibility_analysis()
        self._print_recommendations()

    def _print_system_diagnostics(self):
        """Print system diagnostics."""
        print("SYSTEM DIAGNOSTICS")
        print("-" * 20)

        sys_info = self.system_info
        print(f"Operating System: {sys_info['system']}")
        print(f"Release: {sys_info['release']}")
        print(f"Version: {sys_info['version']}")
        print(f"Machine: {sys_info['machine']}")
        print(f"Processor: {sys_info['processor'] or 'Not available'}")
        print(f"Platform: {sys_info['platform']}")

        bits, linkage = sys_info['architecture']
        print(f"Architecture: {bits}-bit ({linkage})")
        print()

    def _print_python_diagnostics(self):
        """Print Python diagnostics."""
        print("PYTHON DIAGNOSTICS")
        print("-" * 19)

        py_info = self.python_info
        print(f"Python Version: {py_info['version']}")
        print(f"Implementation: {py_info['implementation']}")
        print(f"Compiler: {py_info['compiler']}")

        build_no, build_date = py_info['build']
        print(f"Build: {build_no} ({build_date})")

        if py_info['branch']:
            print(f"Branch: {py_info['branch']}")
        if py_info['revision']:
            print(f"Revision: {py_info['revision']}")

        print(f"Executable: {py_info['executable']}")
        print(f"Prefix: {py_info['prefix']}")

        is_64bit = py_info['maxsize'] > 2**32
        print(f"64-bit Python: {'Yes' if is_64bit else 'No'}")
        print()

    def _print_hardware_diagnostics(self):
        """Print hardware diagnostics."""
        print("HARDWARE DIAGNOSTICS")
        print("-" * 21)

        hw_info = self.hardware_info
        print(f"CPU Cores: {hw_info['cpu_count']}")

        if hw_info['has_psutil']:
            print(f"CPU Usage: {hw_info['cpu_percent']}%")

            mem = hw_info['memory']
            print(f"Memory Total: {self._format_bytes(mem['total'])}")
            print(f"Memory Available: {self._format_bytes(mem['available'])}")
            print(f"Memory Used: {self._format_bytes(mem['used'])} ({mem['percent']}%)")

            disk = hw_info['disk_usage']
            print(f"Disk Total: {self._format_bytes(disk['total'])}")
            print(f"Disk Free: {self._format_bytes(disk['free'])}")
            print(f"Disk Used: {self._format_bytes(disk['used'])} ({disk['percent']}%)")

            print(f"Network Interfaces: {len(hw_info['network_interfaces'])} detected")
        else:
            print("psutil not available - limited hardware diagnostics")
        print()

    def _print_environment_diagnostics(self):
        """Print environment diagnostics."""
        print("ENVIRONMENT DIAGNOSTICS")
        print("-" * 24)

        env_info = self.environment_info
        print(f"Current Directory: {env_info['current_working_directory']}")
        print(f"Home Directory: {env_info['user_home']}")
        print(f"Temp Directory: {env_info['temp_directory']}")
        print(f"Process ID: {env_info['process_id']}")
        print(f"Parent Process ID: {env_info['parent_process_id']}")

        # Environment variables summary
        env_vars = env_info['environment_variables']
        print(f"Environment Variables: {len(env_vars)} defined")

        important_vars = ['PATH', 'PYTHONPATH', 'HOME', 'USER', 'SHELL', 'TERM']
        print("Key Environment Variables:")
        for var in important_vars:
            value = env_vars.get(var, 'Not set')
            if var == 'PATH':
                path_count = len(env_info['path_directories'])
                print(f"  {var}: {path_count} directories")
            else:
                print(f"  {var}: {value}")
        print()

    def _print_compatibility_analysis(self):
        """Print compatibility analysis."""
        print("COMPATIBILITY ANALYSIS")
        print("-" * 22)

        sys_info = self.system_info
        py_info = self.python_info

        # Python version compatibility
        py_version = tuple(map(int, py_info['version_tuple'][:2]))
        if py_version >= (3, 8):
            py_compat = "✓ Modern Python (3.8+)"
        elif py_version >= (3, 6):
            py_compat = "~ Compatible Python (3.6-3.7)"
        else:
            py_compat = "⚠ Legacy Python (< 3.6)"

        print(f"Python Compatibility: {py_compat}")

        # System compatibility
        system = sys_info['system']
        if system in ['Windows', 'Linux', 'Darwin']:
            sys_compat = "✓ Well-supported platform"
        else:
            sys_compat = "~ Less common platform"

        print(f"System Compatibility: {sys_compat}")

        # Architecture compatibility
        bits = sys_info['architecture'][0]
        if bits == '64bit':
            arch_compat = "✓ 64-bit architecture"
        else:
            arch_compat = "⚠ 32-bit architecture (limited support)"

        print(f"Architecture Compatibility: {arch_compat}")

        # Hardware compatibility
        cpu_count = self.hardware_info['cpu_count'] or 1
        if cpu_count >= 2:
            hw_compat = "✓ Multi-core system"
        else:
            hw_compat = "~ Single-core system"

        print(f"Hardware Compatibility: {hw_compat}")
        print()

    def _print_recommendations(self):
        """Print recommendations based on diagnostics."""
        print("RECOMMENDATIONS")
        print("-" * 15)

        recommendations = []

        # Python version recommendations
        py_version = tuple(map(int, self.python_info['version_tuple'][:2]))
        if py_version < (3, 8):
            recommendations.append("Consider upgrading to Python 3.8+ for better performance and features")

        # System-specific recommendations
        system = self.system_info['system']
        if system == 'Windows':
            win_ver = platform.win32_ver()[1]
            if not win_ver.startswith('10.'):
                recommendations.append("Consider upgrading to Windows 10 or 11 for better compatibility")
        elif system == 'Linux':
            kernel_ver = self.system_info['release'].split('-')[0]
            if tuple(map(int, kernel_ver.split('.')[:2])) < (5, 4):
                recommendations.append("Consider upgrading kernel to 5.4+ for modern features")

        # Hardware recommendations
        if self.hardware_info['cpu_count'] and self.hardware_info['cpu_count'] < 2:
            recommendations.append("Multi-core CPU recommended for better performance")

        # Memory recommendations
        if self.hardware_info['has_psutil']:
            mem_gb = self.hardware_info['memory']['total'] / (1024**3)
            if mem_gb < 4:
                recommendations.append("Consider upgrading to 4GB+ RAM for better performance")

        if recommendations:
            for rec in recommendations:
                print(f"• {rec}")
        else:
            print("✓ No major recommendations - system looks good!")

        print()

    def _format_bytes(self, bytes_value):
        """Format bytes into human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return ".1f"
            bytes_value /= 1024.0
        return ".1f"

    def export_report(self, filename=None):
        """Export diagnostics report to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"env_diagnostics_{timestamp}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Capture stdout to file
                import io
                from contextlib import redirect_stdout

                with redirect_stdout(f):
                    self.run_full_diagnostics()

            print(f"Diagnostics report exported to: {filename}")
            return True
        except Exception as e:
            print(f"Error exporting report: {e}")
            return False

    def get_summary(self):
        """Get a quick summary of the environment."""
        return {
            'system': f"{self.system_info['system']} {self.system_info['release']}",
            'python': self.python_info['version'],
            'architecture': f"{self.system_info['architecture'][0]} ({self.system_info['machine']})",
            'cpu_cores': self.hardware_info['cpu_count'],
            'hostname': self.system_info['hostname']
        }


def main():
    """Main function to run environment diagnostics."""
    print("Environment Diagnostics Tool")
    print("Using platform module for system analysis")
    print()

    # Create diagnostics instance
    diagnostics = EnvironmentDiagnostics()

    # Print quick summary
    summary = diagnostics.get_summary()
    print("QUICK SUMMARY")
    print("-" * 13)
    for key, value in summary.items():
        print(f"{key.capitalize()}: {value}")
    print()

    # Run full diagnostics
    diagnostics.run_full_diagnostics()

    # Export report
    print("EXPORTING REPORT")
    print("-" * 16)
    diagnostics.export_report()


if __name__ == "__main__":
    main()
