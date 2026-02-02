#!/usr/bin/env python3
"""
Subprocess Command Execution Examples

This module demonstrates various ways to run external commands using the subprocess module.
All examples are safe, cross-platform, and include proper error handling.
"""

import subprocess
import sys
import time
import platform
import os


def run_basic_command():
    """Demonstrate basic command execution with subprocess.run()"""
    print("=== Basic Command Execution ===")

    try:
        # Run a simple command
        result = subprocess.run(['echo', 'Hello, subprocess!'],
                               capture_output=True, text=True)

        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout.strip()}")

    except FileNotFoundError:
        print("Error: 'echo' command not found")
    except Exception as e:
        print(f"Unexpected error: {e}")


def run_command_with_error_handling():
    """Demonstrate command execution with comprehensive error handling"""
    print("\n=== Command Execution with Error Handling ===")

    commands = [
        ['echo', 'This will succeed'],
        ['false'],  # Command that always fails
        ['nonexistent_command'],
    ]

    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                print(f"✓ Command {' '.join(cmd)} succeeded")
                if result.stdout.strip():
                    print(f"  Output: {result.stdout.strip()}")
            else:
                print(f"✗ Command {' '.join(cmd)} failed with code {result.returncode}")
                if result.stderr.strip():
                    print(f"  Error: {result.stderr.strip()}")

        except subprocess.TimeoutExpired:
            print(f"⏰ Command {' '.join(cmd)} timed out")
        except FileNotFoundError:
            print(f"❌ Command {' '.join(cmd)} not found")
        except Exception as e:
            print(f"💥 Unexpected error running {' '.join(cmd)}: {e}")


def run_command_with_input():
    """Demonstrate providing input to commands"""
    print("\n=== Command Input Examples ===")

    # Example 1: Send text input to grep
    try:
        result = subprocess.run(['grep', 'python'],
                               input='Python is great\nJava is also good\nGo is fast\n',
                               capture_output=True, text=True)

        print("Grep for 'python':")
        print(result.stdout.strip())

    except FileNotFoundError:
        print("grep command not found")

    # Example 2: Interactive command (simulated)
    try:
        # Use printf to simulate user input
        result = subprocess.run(['cat'],
                               input='Line 1\nLine 2\nLine 3\n',
                               capture_output=True, text=True)

        print("\nCat command with input:")
        print(result.stdout.strip())

    except FileNotFoundError:
        print("cat command not found")


def run_long_running_command():
    """Demonstrate handling long-running commands"""
    print("\n=== Long-Running Command Handling ===")

    try:
        print("Starting a 3-second sleep command...")

        # Run with timeout
        start_time = time.time()
        result = subprocess.run(['sleep', '3'], timeout=5)
        end_time = time.time()

        print(".2f")
        print(f"Return code: {result.returncode}")

    except subprocess.TimeoutExpired:
        print("Command timed out (this shouldn't happen in this example)")
    except FileNotFoundError:
        print("sleep command not found")


def run_commands_in_parallel():
    """Demonstrate running multiple commands concurrently"""
    print("\n=== Parallel Command Execution ===")

    import concurrent.futures

    def run_single_command(cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return {
                'command': cmd,
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'output': result.stdout.strip() if result.stdout else '',
                'error': result.stderr.strip() if result.stderr else ''
            }
        except Exception as e:
            return {
                'command': cmd,
                'success': False,
                'error': str(e)
            }

    commands = [
        ['echo', 'Command 1'],
        ['echo', 'Command 2'],
        ['sleep', '1'],  # Short sleep to simulate work
        ['echo', 'Command 3'],
    ]

    print(f"Running {len(commands)} commands in parallel...")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(run_single_command, commands))

    for result in results:
        status = "✓" if result['success'] else "✗"
        print(f"{status} {' '.join(result['command'])}")
        if result['success'] and result['output']:
            print(f"  Output: {result['output']}")
        elif not result['success']:
            print(f"  Error: {result.get('error', 'Unknown error')}")


def run_command_with_custom_environment():
    """Demonstrate running commands with custom environment variables"""
    print("\n=== Custom Environment Variables ===")

    # Get current environment and modify it
    env = os.environ.copy()
    env['CUSTOM_VAR'] = 'Hello from subprocess'
    env['PATH'] = env.get('PATH', '')  # Ensure PATH exists

    try:
        # Run a command that uses environment variables
        if platform.system() == 'Windows':
            # Windows echo doesn't expand variables by default
            result = subprocess.run(['cmd', '/c', 'echo %CUSTOM_VAR%'],
                                   env=env, capture_output=True, text=True)
        else:
            # Unix shells expand variables
            result = subprocess.run(['sh', '-c', 'echo $CUSTOM_VAR'],
                                   env=env, capture_output=True, text=True)

        print(f"Environment variable output: {result.stdout.strip()}")

        # Show that the variable is isolated
        result2 = subprocess.run(['sh', '-c', 'echo $CUSTOM_VAR'],
                                capture_output=True, text=True)
        print(f"Variable in normal environment: '{result2.stdout.strip()}'")

    except FileNotFoundError:
        print("Shell command not found")


def run_command_with_different_cwd():
    """Demonstrate running commands in different working directories"""
    print("\n=== Different Working Directory ===")

    try:
        # Get current directory
        original_cwd = os.getcwd()
        print(f"Original working directory: {original_cwd}")

        # Run command in parent directory (if it exists)
        parent_dir = os.path.dirname(original_cwd)
        if os.path.exists(parent_dir):
            result = subprocess.run(['pwd'], cwd=parent_dir,
                                   capture_output=True, text=True)
            print(f"Command run in: {result.stdout.strip()}")
        else:
            print("No parent directory available")

        # Confirm we're back in original directory
        print(f"Current working directory: {os.getcwd()}")

    except FileNotFoundError:
        print("pwd command not found")
    except Exception as e:
        print(f"Error: {e}")


def run_cross_platform_commands():
    """Demonstrate cross-platform command execution"""
    print("\n=== Cross-Platform Command Execution ===")

    system = platform.system()

    if system == 'Windows':
        # Windows commands
        commands = [
            ['cmd', '/c', 'echo Windows command'],
            ['cmd', '/c', 'ver'],  # Version info
        ]
    else:
        # Unix-like commands
        commands = [
            ['echo', 'Unix-like command'],
            ['uname', '-a'],  # System info
        ]

    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                print(f"✓ {' '.join(cmd)}")
                if result.stdout.strip():
                    # Truncate long output
                    output = result.stdout.strip()
                    if len(output) > 100:
                        output = output[:100] + "..."
                    print(f"  Output: {output}")
            else:
                print(f"✗ {' '.join(cmd)} (code: {result.returncode})")

        except subprocess.TimeoutExpired:
            print(f"⏰ {' '.join(cmd)} timed out")
        except FileNotFoundError:
            print(f"❌ {' '.join(cmd)} not found")
        except Exception as e:
            print(f"💥 {' '.join(cmd)} error: {e}")


def demonstrate_command_builder():
    """Demonstrate a command builder pattern for complex commands"""
    print("\n=== Command Builder Pattern ===")

    class CommandBuilder:
        def __init__(self, base_command):
            self.command = [base_command]
            self.options = {}

        def add_argument(self, arg):
            self.command.append(arg)
            return self

        def add_option(self, flag, value=None):
            if value is not None:
                self.command.extend([flag, str(value)])
            else:
                self.command.append(flag)
            return self

        def set_option(self, key, value):
            self.options[key] = value
            return self

        def run(self, **run_options):
            # Merge command options with run options
            final_options = {**self.options, **run_options}
            return subprocess.run(self.command, **final_options)

    # Example: Build a complex find command (Unix-like systems)
    if platform.system() != 'Windows':
        try:
            cmd = (CommandBuilder('find')
                   .add_argument('.')
                   .add_option('-name', '*.py')
                   .add_option('-type', 'f')
                   .add_option('-exec', 'wc')
                   .add_option('-l', '{}')
                   .add_argument(';')
                   .set_option('capture_output', True)
                   .set_option('text', True)
                   .set_option('timeout', 10))

            print(f"Built command: {' '.join(cmd.command)}")
            result = cmd.run()

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                print(f"Found {len(lines)} Python files")
            else:
                print(f"Command failed with code {result.returncode}")

        except FileNotFoundError:
            print("find command not found")
        except subprocess.TimeoutExpired:
            print("find command timed out")
    else:
        print("Command builder example skipped on Windows")


def main():
    """Run all examples"""
    print("Subprocess Command Execution Examples")
    print("=" * 50)

    examples = [
        run_basic_command,
        run_command_with_error_handling,
        run_command_with_input,
        run_long_running_command,
        run_commands_in_parallel,
        run_command_with_custom_environment,
        run_command_with_different_cwd,
        run_cross_platform_commands,
        demonstrate_command_builder,
    ]

    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")

    print("\n" + "=" * 50)
    print("All examples completed!")


if __name__ == '__main__':
    main()
