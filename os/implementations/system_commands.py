"""
System Commands Implementation

This module demonstrates how to execute system commands and interact with
the operating system shell using the os module.
"""

import os
import subprocess
import shlex
import time
from typing import List, Tuple, Optional


class CommandExecutor:
    """
    A class for executing system commands with proper error handling.
    """

    def __init__(self, shell=None):
        """
        Initialize the command executor.

        Args:
            shell (str): Shell to use for command execution
        """
        self.shell = shell or self._get_default_shell()

    def _get_default_shell(self):
        """Get the default shell for the system."""
        if os.name == 'nt':
            return os.environ.get('COMSPEC', 'cmd.exe')
        else:
            return os.environ.get('SHELL', '/bin/bash')

    def execute(self, command: str, timeout: Optional[int] = None) -> Tuple[int, str, str]:
        """
        Execute a command and return the results.

        Args:
            command (str): Command to execute
            timeout (int): Timeout in seconds

        Returns:
            tuple: (return_code, stdout, stderr)
        """
        try:
            # Use subprocess for safer execution
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=dict(os.environ)  # Copy environment
            )

            return result.returncode, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return -1, "", f"Command timed out after {timeout} seconds"
        except Exception as e:
            return -1, "", str(e)

    def execute_piped(self, commands: List[str]) -> Tuple[int, str, str]:
        """
        Execute a pipeline of commands.

        Args:
            commands (list): List of commands to pipe

        Returns:
            tuple: (return_code, stdout, stderr)
        """
        if not commands:
            return 0, "", ""

        try:
            # Start with the first command
            processes = []
            previous_output = None

            for i, cmd in enumerate(commands):
                if i == 0:
                    # First command
                    proc = subprocess.Popen(
                        cmd if isinstance(cmd, list) else shlex.split(cmd),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=previous_output
                    )
                elif i == len(commands) - 1:
                    # Last command
                    proc = subprocess.Popen(
                        cmd if isinstance(cmd, list) else shlex.split(cmd),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=previous_output
                    )
                else:
                    # Middle command
                    proc = subprocess.Popen(
                        cmd if isinstance(cmd, list) else shlex.split(cmd),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=previous_output
                    )

                processes.append(proc)
                previous_output = proc.stdout

            # Wait for all processes and collect output
            stdout, stderr = processes[-1].communicate()

            # Get the return code from the last process
            return_code = processes[-1].returncode

            return return_code, stdout.decode(), stderr.decode()

        except Exception as e:
            return -1, "", str(e)

    def is_command_available(self, command: str) -> bool:
        """
        Check if a command is available in the system PATH.

        Args:
            command (str): Command to check

        Returns:
            bool: True if command is available
        """
        try:
            result = subprocess.run(
                [command, '--version'] if os.name != 'nt' else [command],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False


def run_command_background(command: str) -> subprocess.Popen:
    """
    Run a command in the background.

    Args:
        command (str): Command to run

    Returns:
        Popen: Process object
    """
    return subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )


def get_command_output(command: str, timeout: int = 30) -> Optional[str]:
    """
    Get the output of a command as a string.

    Args:
        command (str): Command to execute
        timeout (int): Timeout in seconds

    Returns:
        str or None: Command output or None if failed
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None

    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None


def find_executable(command: str) -> Optional[str]:
    """
    Find the full path to an executable.

    Args:
        command (str): Command name

    Returns:
        str or None: Full path to executable
    """
    # Check if it's already a full path
    if os.path.isfile(command) and os.access(command, os.X_OK):
        return command

    # Search in PATH
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)

    for directory in path_dirs:
        if not directory:
            continue

        full_path = os.path.join(directory, command)

        # Add .exe extension on Windows if not present
        if os.name == 'nt' and not full_path.endswith('.exe'):
            full_path += '.exe'

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path

    return None


def get_system_info() -> dict:
    """
    Get basic system information using system commands.

    Returns:
        dict: System information
    """
    info = {}

    # Try different commands based on platform
    if os.name == 'nt':
        # Windows commands
        commands = {
            'os': 'ver',
            'cpu': 'wmic cpu get name',
            'memory': 'wmic OS get TotalVisibleMemorySize'
        }
    else:
        # Unix-like commands
        commands = {
            'os': 'uname -a',
            'cpu': 'lscpu | head -1' if find_executable('lscpu') else 'cat /proc/cpuinfo | grep "model name" | head -1',
            'memory': 'free -h | head -2'
        }

    for key, cmd in commands.items():
        output = get_command_output(cmd)
        info[key] = output if output else 'Not available'

    return info


def list_processes(pattern: Optional[str] = None) -> List[dict]:
    """
    List running processes, optionally filtered by pattern.

    Args:
        pattern (str): Pattern to filter process names

    Returns:
        list: List of process information dictionaries
    """
    processes = []

    try:
        if os.name == 'nt':
            # Windows: use tasklist
            result = subprocess.run(['tasklist', '/FO', 'CSV', '/NH'],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    parts = line.split('","')
                    if len(parts) >= 2:
                        name = parts[0].strip('"')
                        pid = parts[1].strip('"')

                        if not pattern or pattern.lower() in name.lower():
                            processes.append({
                                'name': name,
                                'pid': pid,
                                'platform': 'windows'
                            })
        else:
            # Unix-like: use ps
            result = subprocess.run(['ps', 'aux'],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 11:
                        user = parts[0]
                        pid = parts[1]
                        cpu = parts[2]
                        memory = parts[3]
                        name = ' '.join(parts[10:])

                        if not pattern or pattern.lower() in name.lower():
                            processes.append({
                                'name': name,
                                'pid': pid,
                                'user': user,
                                'cpu': cpu,
                                'memory': memory,
                                'platform': 'unix'
                            })

    except Exception as e:
        print(f"Error listing processes: {e}")

    return processes


def demonstrate_system_commands():
    """Demonstrate various system command operations."""

    print("=== System Commands Demo ===\n")

    # Initialize command executor
    executor = CommandExecutor()

    print("1. Basic Command Execution:")
    # Test basic commands
    test_commands = ['echo "Hello, World!"']

    if os.name != 'nt':
        test_commands.append('ls -la | head -5')
        test_commands.append('pwd')
    else:
        test_commands.append('dir /b')
        test_commands.append('cd')

    for cmd in test_commands:
        print(f"   Executing: {cmd}")
        return_code, stdout, stderr = executor.execute(cmd)

        if return_code == 0:
            print(f"   Success (exit code: {return_code})")
            if stdout.strip():
                print(f"   Output: {stdout.strip()[:100]}...")
        else:
            print(f"   Failed (exit code: {return_code})")
            if stderr.strip():
                print(f"   Error: {stderr.strip()[:100]}...")
        print()

    print("2. Command Availability Check:")
    commands_to_check = ['python', 'git', 'ls', 'dir']
    for cmd in commands_to_check:
        available = executor.is_command_available(cmd)
        status = "Available" if available else "Not found"
        print(f"   {cmd}: {status}")
    print()

    print("3. Finding Executables:")
    executables = ['python', 'git', 'bash', 'cmd']
    for exe in executables:
        path = find_executable(exe)
        if path:
            print(f"   {exe}: {path}")
        else:
            print(f"   {exe}: Not found")
    print()

    print("4. System Information:")
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print(f"   {key.upper()}: {value[:80]}...")
    print()

    print("5. Process Listing:")
    # List a few processes
    processes = list_processes()
    print(f"   Found {len(processes)} processes")

    # Show first few processes
    for proc in processes[:5]:
        if 'user' in proc:
            print(f"   {proc['name'][:30]:30} (PID: {proc['pid']}, User: {proc['user']})")
        else:
            print(f"   {proc['name'][:30]:30} (PID: {proc['pid']})")
    print()

    print("6. Background Command Execution:")
    # Run a background command (ping or sleep)
    if os.name == 'nt':
        bg_cmd = 'timeout /t 5 /nobreak > nul'
    else:
        bg_cmd = 'sleep 2'

    print(f"   Starting background command: {bg_cmd}")
    proc = run_command_background(bg_cmd)

    # Wait a bit
    time.sleep(1)

    # Check if still running
    if proc.poll() is None:
        print("   Background command is still running")
        proc.wait()  # Wait for completion
        print("   Background command completed")
    else:
        print(f"   Background command finished with exit code: {proc.returncode}")
    print()

    print("Demo completed!")


if __name__ == "__main__":
    demonstrate_system_commands()
