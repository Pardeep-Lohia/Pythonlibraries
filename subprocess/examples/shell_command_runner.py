#!/usr/bin/env python3
"""
Shell Command Runner

A practical example of a command-line tool that safely executes shell commands
with proper error handling, logging, and user interaction.
"""

import subprocess
import sys
import argparse
import logging
import time
import platform
import os
from pathlib import Path


class ShellCommandRunner:
    """A safe and user-friendly shell command runner"""

    def __init__(self, verbose=False, log_file=None):
        self.verbose = verbose
        self.setup_logging(log_file)

    def setup_logging(self, log_file):
        """Set up logging configuration"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        level = logging.DEBUG if self.verbose else logging.INFO

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(log_format))

        # File handler if specified
        handlers = [console_handler]
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(log_format))
            handlers.append(file_handler)

        logging.basicConfig(level=level, handlers=handlers)
        self.logger = logging.getLogger(__name__)

    def run_command(self, command, timeout=30, cwd=None, env=None):
        """Run a single command safely"""
        self.logger.info(f"Executing: {' '.join(command)}")

        start_time = time.time()

        try:
            # Prepare environment
            run_env = os.environ.copy()
            if env:
                run_env.update(env)

            # Run the command
            result = subprocess.run(
                command,
                cwd=cwd,
                env=run_env,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            duration = time.time() - start_time

            if result.returncode == 0:
                self.logger.info(f"✓ Command succeeded in {duration:.2f}s")
                if result.stdout and self.verbose:
                    self.logger.debug(f"Output: {result.stdout.strip()}")
            else:
                self.logger.warning(f"✗ Command failed (code {result.returncode}) in {duration:.2f}s")
                if result.stderr:
                    self.logger.warning(f"Error: {result.stderr.strip()}")

            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'duration': duration
            }

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            self.logger.error(f"⏰ Command timed out after {duration:.2f}s")
            return {
                'success': False,
                'error': 'timeout',
                'duration': duration
            }

        except FileNotFoundError as e:
            self.logger.error(f"❌ Command not found: {e.filename}")
            return {
                'success': False,
                'error': 'command_not_found',
                'filename': e.filename
            }

        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"💥 Unexpected error after {duration:.2f}s: {e}")
            return {
                'success': False,
                'error': 'unexpected',
                'exception': str(e),
                'duration': duration
            }

    def run_commands_batch(self, commands, continue_on_error=True):
        """Run multiple commands in batch"""
        self.logger.info(f"Running batch of {len(commands)} commands")

        results = []
        success_count = 0

        for i, cmd in enumerate(commands, 1):
            self.logger.info(f"Command {i}/{len(commands)}")
            result = self.run_command(cmd)

            results.append(result)
            if result['success']:
                success_count += 1
            elif not continue_on_error:
                self.logger.error("Stopping batch due to command failure")
                break

        self.logger.info(f"Batch completed: {success_count}/{len(commands)} commands succeeded")
        return results

    def interactive_mode(self):
        """Run in interactive mode"""
        self.logger.info("Starting interactive mode")
        print("Shell Command Runner - Interactive Mode")
        print("Type 'exit' or 'quit' to exit")
        print("Type 'help' for available commands")
        print("-" * 40)

        while True:
            try:
                # Get user input
                user_input = input("cmd> ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break

                if user_input.lower() == 'help':
                    self.show_help()
                    continue

                # Parse and execute command
                command = self.parse_command(user_input)
                if command:
                    result = self.run_command(command, timeout=60)

                    # Display result
                    if result['success']:
                        print("✓ Command executed successfully")
                        if result.get('stdout'):
                            print(result['stdout'])
                    else:
                        print("✗ Command failed")
                        if result.get('stderr'):
                            print(f"Error: {result['stderr']}")

            except KeyboardInterrupt:
                print("\nInterrupted by user")
                break
            except EOFError:
                print("\nEOF received, exiting")
                break
            except Exception as e:
                print(f"Error: {e}")

    def parse_command(self, user_input):
        """Parse user input into command list"""
        # Simple parsing - can be enhanced for complex commands
        import shlex

        try:
            # Use shlex for proper parsing
            command = shlex.split(user_input)
            return command
        except ValueError as e:
            print(f"Parse error: {e}")
            return None

    def show_help(self):
        """Show help information"""
        help_text = """
Available commands:
  <command>          Execute a shell command
  help               Show this help
  exit/quit          Exit interactive mode

Examples:
  cmd> ls -la
  cmd> echo "Hello World"
  cmd> python --version
  cmd> git status

Note: Commands are executed with a 60-second timeout.
Use Ctrl+C to interrupt long-running commands.
        """
        print(help_text)

    def get_system_info(self):
        """Get system information for diagnostics"""
        info = {
            'platform': platform.system(),
            'python_version': sys.version,
            'working_directory': os.getcwd(),
            'user': os.environ.get('USER') or os.environ.get('USERNAME'),
        }

        # Try to get additional system info
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(['ver'], capture_output=True, text=True, timeout=5)
                info['system_version'] = result.stdout.strip()
            else:
                result = subprocess.run(['uname', '-a'], capture_output=True, text=True, timeout=5)
                info['system_info'] = result.stdout.strip()
        except:
            pass

        return info


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Safe Shell Command Runner")
    parser.add_argument('command', nargs='*', help='Command to execute')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-l', '--log-file', help='Log file path')
    parser.add_argument('-t', '--timeout', type=int, default=30, help='Command timeout in seconds')
    parser.add_argument('-c', '--cwd', help='Working directory')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--batch', help='Batch file with commands (one per line)')
    parser.add_argument('--continue-on-error', action='store_true', help='Continue batch on error')

    args = parser.parse_args()

    # Create runner
    runner = ShellCommandRunner(verbose=args.verbose, log_file=args.log_file)

    # Show system info
    if args.verbose:
        info = runner.get_system_info()
        runner.logger.info("System Information:")
        for key, value in info.items():
            runner.logger.info(f"  {key}: {value}")

    try:
        if args.interactive:
            # Interactive mode
            runner.interactive_mode()

        elif args.batch:
            # Batch mode
            batch_file = Path(args.batch)
            if not batch_file.exists():
                runner.logger.error(f"Batch file not found: {args.batch}")
                return 1

            commands = []
            with open(batch_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        command = runner.parse_command(line)
                        if command:
                            commands.append(command)

            if not commands:
                runner.logger.warning("No valid commands found in batch file")
                return 0

            results = runner.run_commands_batch(commands, args.continue_on_error)

            # Summary
            success_count = sum(1 for r in results if r['success'])
            runner.logger.info(f"Batch summary: {success_count}/{len(results)} commands succeeded")

            return 0 if success_count == len(results) else 1

        elif args.command:
            # Single command mode
            result = runner.run_command(args.command, timeout=args.timeout, cwd=args.cwd)

            if result['success']:
                # Print output to stdout for piping
                if result.get('stdout'):
                    print(result['stdout'], end='')
                return 0
            else:
                # Print error to stderr
                if result.get('stderr'):
                    print(result['stderr'], end='', file=sys.stderr)
                return result.get('returncode', 1)

        else:
            # No command provided, show help
            parser.print_help()
            return 0

    except KeyboardInterrupt:
        runner.logger.info("Interrupted by user")
        return 130
    except Exception as e:
        runner.logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
