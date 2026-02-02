#!/usr/bin/env python3
"""
Error Handling Implementation Examples

This module demonstrates comprehensive error handling patterns for subprocess operations,
including exception handling, timeout management, logging, and recovery strategies.
"""

import subprocess
import sys
import time
import logging
import os
import signal
from pathlib import Path


def basic_exception_handling():
    """Demonstrate basic exception handling with subprocess"""
    print("=== Basic Exception Handling ===")

    commands = [
        ['echo', 'This will succeed'],
        ['false'],  # Always fails
        ['nonexistent_command'],  # Doesn't exist
    ]

    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            print(f"✓ {' '.join(cmd)} -> return code: {result.returncode}")
        except subprocess.CalledProcessError as e:
            print(f"✗ {' '.join(cmd)} -> CalledProcessError: {e.returncode}")
        except subprocess.TimeoutExpired as e:
            print(f"⏰ {' '.join(cmd)} -> TimeoutExpired: {e.timeout}s")
        except FileNotFoundError as e:
            print(f"❌ {' '.join(cmd)} -> FileNotFoundError: {e.filename}")
        except Exception as e:
            print(f"💥 {' '.join(cmd)} -> Unexpected error: {e}")


def comprehensive_error_handler():
    """Demonstrate a comprehensive error handling class"""
    print("\n=== Comprehensive Error Handler ===")

    class SubprocessErrorHandler:
        def __init__(self, logger=None):
            self.logger = logger or print

        def run_with_handling(self, cmd, **kwargs):
            """Run command with comprehensive error handling"""
            defaults = {
                'capture_output': True,
                'text': True,
                'timeout': 30,
                'check': False
            }
            defaults.update(kwargs)

            start_time = time.time()

            try:
                self.logger(f"Running: {' '.join(cmd)}")
                result = subprocess.run(cmd, **defaults)
                duration = time.time() - start_time

                if result.returncode == 0:
                    self.logger(f"Command succeeded in {duration:.2f}s")
                else:
                    self.logger(f"Command failed with code {result.returncode} in {duration:.2f}s")

                return {
                    'success': result.returncode == 0,
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'duration': duration
                }

            except subprocess.CalledProcessError as e:
                duration = time.time() - start_time
                self.logger(f"CalledProcessError after {duration:.2f}s: {e.returncode}")
                return {
                    'success': False,
                    'error': 'called_process_error',
                    'returncode': e.returncode,
                    'stdout': e.stdout,
                    'stderr': e.stderr,
                    'duration': duration
                }

            except subprocess.TimeoutExpired as e:
                duration = time.time() - start_time
                self.logger(f"TimeoutExpired after {duration:.2f}s: {e.timeout}s limit")
                return {
                    'success': False,
                    'error': 'timeout',
                    'timeout': e.timeout,
                    'duration': duration
                }

            except FileNotFoundError as e:
                duration = time.time() - start_time
                self.logger(f"FileNotFoundError after {duration:.2f}s: {e.filename}")
                return {
                    'success': False,
                    'error': 'file_not_found',
                    'filename': e.filename,
                    'duration': duration
                }

            except PermissionError as e:
                duration = time.time() - start_time
                self.logger(f"PermissionError after {duration:.2f}s: {e.filename}")
                return {
                    'success': False,
                    'error': 'permission_denied',
                    'filename': e.filename,
                    'duration': duration
                }

            except OSError as e:
                duration = time.time() - start_time
                self.logger(f"OSError after {duration:.2f}s: {e}")
                return {
                    'success': False,
                    'error': 'os_error',
                    'os_error': str(e),
                    'duration': duration
                }

            except Exception as e:
                duration = time.time() - start_time
                self.logger(f"Unexpected error after {duration:.2f}s: {e}")
                return {
                    'success': False,
                    'error': 'unexpected',
                    'exception': str(e),
                    'duration': duration
                }

    # Use the error handler
    handler = SubprocessErrorHandler()

    test_commands = [
        ['echo', 'Success'],
        ['false'],
        ['nonexistent'],
        ['sleep', '5'],  # Will timeout
    ]

    for cmd in test_commands:
        result = handler.run_with_handling(cmd, timeout=2)
        print(f"Result: {result['success']} ({result.get('error', 'none')})")


def timeout_strategies():
    """Demonstrate different timeout handling strategies"""
    print("\n=== Timeout Strategies ===")

    def run_with_timeout(cmd, timeout=10):
        """Basic timeout handling"""
        try:
            return subprocess.run(cmd, timeout=timeout, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            print(f"Command timed out after {timeout} seconds")
            return None

    def run_with_progressive_timeout(cmd, initial_timeout=5, max_attempts=3):
        """Progressive timeout - increase timeout on each retry"""
        timeout = initial_timeout

        for attempt in range(max_attempts):
            try:
                result = subprocess.run(cmd, timeout=timeout, capture_output=True, text=True)
                return result
            except subprocess.TimeoutExpired:
                if attempt < max_attempts - 1:
                    timeout *= 2
                    print(f"Attempt {attempt + 1} timed out, retrying with {timeout}s timeout")
                else:
                    print(f"All {max_attempts} attempts timed out")
                    return None

    def run_with_cleanup(cmd, timeout=10):
        """Timeout with proper cleanup"""
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return {
                'returncode': process.returncode,
                'stdout': stdout,
                'stderr': stderr
            }
        except subprocess.TimeoutExpired:
            print("Process timed out, terminating...")
            process.terminate()

            try:
                process.wait(timeout=5)
                print("Process terminated gracefully")
            except subprocess.TimeoutExpired:
                print("Process didn't terminate gracefully, killing...")
                process.kill()
                process.wait()

            return {'error': 'timeout'}

    # Test timeout strategies
    print("1. Basic timeout:")
    result = run_with_timeout(['sleep', '3'], timeout=2)

    print("\n2. Progressive timeout:")
    result = run_with_progressive_timeout(['sleep', '10'], initial_timeout=2)

    print("\n3. Timeout with cleanup:")
    result = run_with_cleanup(['sleep', '10'], timeout=2)


def return_code_interpretation():
    """Demonstrate return code interpretation"""
    print("\n=== Return Code Interpretation ===")

    def interpret_return_code(returncode):
        """Interpret common return codes"""
        if returncode == 0:
            return "Success"
        elif returncode == 1:
            return "General error"
        elif returncode == 2:
            return "Shell syntax error"
        elif returncode == 126:
            return "Command found but not executable"
        elif returncode == 127:
            return "Command not found"
        elif returncode == 128:
            return "Invalid argument to exit"
        elif returncode > 128:
            signal_num = returncode - 128
            signals = {
                1: "SIGHUP", 2: "SIGINT", 3: "SIGQUIT", 4: "SIGILL",
                6: "SIGABRT", 8: "SIGFPE", 9: "SIGKILL", 11: "SIGSEGV",
                15: "SIGTERM"
            }
            signal_name = signals.get(signal_num, f"Signal {signal_num}")
            return f"Terminated by {signal_name}"
        else:
            return f"Unknown error code: {returncode}"

    # Test various return codes
    test_commands = [
        ['true'],  # 0
        ['false'],  # 1
        ['sh', '-c', 'exit 42'],  # 42
    ]

    for cmd in test_commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            interpretation = interpret_return_code(result.returncode)
            print(f"{' '.join(cmd)} -> {result.returncode}: {interpretation}")
        except Exception as e:
            print(f"{' '.join(cmd)} -> Error: {e}")


def logging_and_auditing():
    """Demonstrate logging and auditing of subprocess operations"""
    print("\n=== Logging and Auditing ===")

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('subprocess_audit.log')
        ]
    )

    logger = logging.getLogger('subprocess_audit')

    def audited_run(cmd, user="unknown", **kwargs):
        """Run command with audit logging"""
        cmd_str = ' '.join(cmd)
        logger.info(f"User '{user}' executing: {cmd_str}")

        start_time = time.time()

        try:
            result = subprocess.run(cmd, **kwargs)
            duration = time.time() - start_time

            if result.returncode == 0:
                logger.info(f"Command succeeded in {duration:.2f}s")
            else:
                logger.warning(f"Command failed with code {result.returncode} in {duration:.2f}s")
            return result

        except subprocess.TimeoutExpired as e:
            duration = time.time() - start_time
            logger.error(f"Command timed out after {duration:.2f}s")
            raise
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Command failed after {duration:.2f}s: {e}")
            raise

    # Test audited execution
    try:
        audited_run(['echo', 'Test command'], capture_output=True, text=True)
        audited_run(['false'], capture_output=True, text=True)  # Will fail
        audited_run(['sleep', '5'], timeout=2, capture_output=True, text=True)  # Will timeout
    except subprocess.TimeoutExpired:
        pass  # Expected

    print("Audit log written to subprocess_audit.log")


def recovery_and_retry_patterns():
    """Demonstrate recovery and retry patterns"""
    print("\n=== Recovery and Retry Patterns ===")

    def run_with_retry(cmd, max_retries=3, delay=1, backoff=2, **kwargs):
        """Run command with exponential backoff retry"""
        retry_count = 0

        while retry_count <= max_retries:
            try:
                result = subprocess.run(cmd, **kwargs)

                if result.returncode == 0:
                    return result

                if retry_count < max_retries:
                    print(f"Command failed (attempt {retry_count + 1}), retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= backoff
                    retry_count += 1
                else:
                    print(f"Command failed after {max_retries + 1} attempts")
                    return result

            except subprocess.TimeoutExpired:
                if retry_count < max_retries:
                    print(f"Timeout (attempt {retry_count + 1}), retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= backoff
                    retry_count += 1
                else:
                    print(f"Command timed out after {max_retries + 1} attempts")
                    raise
            except Exception as e:
                print(f"Unexpected error on attempt {retry_count + 1}: {e}")
                if retry_count < max_retries:
                    time.sleep(delay)
                    delay *= backoff
                    retry_count += 1
                else:
                    raise

    def run_with_fallback(primary_cmd, fallback_cmd, **kwargs):
        """Run primary command, fall back to alternative on failure"""
        try:
            print(f"Trying primary command: {' '.join(primary_cmd)}")
            result = subprocess.run(primary_cmd, **kwargs)
            if result.returncode == 0:
                print("Primary command succeeded")
                return result
            else:
                print("Primary command failed, trying fallback...")
        except Exception as e:
            print(f"Primary command error: {e}, trying fallback...")

        try:
            print(f"Trying fallback command: {' '.join(fallback_cmd)}")
            result = subprocess.run(fallback_cmd, **kwargs)
            print("Fallback command succeeded")
            return result
        except Exception as e:
            print(f"Fallback command also failed: {e}")
            raise

    # Test retry pattern
    print("Testing retry pattern:")
    result = run_with_retry(['sh', '-c', 'exit 1'], max_retries=2,
                           capture_output=True, text=True)

    # Test fallback pattern
    print("\nTesting fallback pattern:")
    result = run_with_fallback(['false'], ['true'],
                              capture_output=True, text=True)


def cross_platform_error_handling():
    """Demonstrate cross-platform error handling"""
    print("\n=== Cross-Platform Error Handling ===")

    import platform

    def run_cross_platform(cmd, **kwargs):
        """Run command with platform-specific error handling"""
        system = platform.system()

        try:
            result = subprocess.run(cmd, **kwargs)
            return result

        except FileNotFoundError as e:
            if system == 'Windows':
                # Try with .exe extension
                alt_cmd = [cmd[0] + '.exe'] + cmd[1:]
                try:
                    return subprocess.run(alt_cmd, **kwargs)
                except FileNotFoundError:
                    raise e
            else:
                raise

        except PermissionError as e:
            if system == 'Windows':
                print("Try running as Administrator")
            else:
                print("Check file permissions with 'ls -la'")
            raise

        except subprocess.TimeoutExpired as e:
            if system == 'Windows':
                print("Windows may have slower process startup")
            raise

    # Test cross-platform handling
    try:
        result = run_cross_platform(['nonexistent'], capture_output=True, text=True)
    except FileNotFoundError:
        print("Handled FileNotFoundError appropriately")


def context_managers_for_error_handling():
    """Demonstrate context managers for error handling"""
    print("\n=== Context Managers for Error Handling ===")

    class SafeSubprocess:
        """Context manager for safe subprocess execution"""

        def __init__(self, cmd, **kwargs):
            self.cmd = cmd
            self.kwargs = kwargs
            self.process = None
            self.result = None

        def __enter__(self):
            self.kwargs.setdefault('stdout', subprocess.PIPE)
            self.kwargs.setdefault('stderr', subprocess.PIPE)
            self.kwargs.setdefault('text', True)

            self.process = subprocess.Popen(self.cmd, **self.kwargs)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.process:
                if self.process.poll() is None:
                    # Process still running, terminate it
                    self.process.terminate()
                    try:
                        self.process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self.process.kill()
                        self.process.wait()

                # Get final result
                if self.process.returncode is not None:
                    self.result = {
                        'returncode': self.process.returncode,
                        'stdout': '',
                        'stderr': ''
                    }

                    # Try to get output if pipes were used
                    if hasattr(self.process, 'stdout') and self.process.stdout:
                        try:
                            remaining, errors = self.process.communicate(timeout=1)
                            self.result['stdout'] = remaining or ''
                            self.result['stderr'] = errors or ''
                        except subprocess.TimeoutExpired:
                            pass

    # Use the context manager
    print("Testing context manager:")
    with SafeSubprocess(['python3', '-c', '''
import time
print("Starting long process...")
time.sleep(2)
print("Process completed")
''']) as sp:
        print(f"Process {sp.process.pid} started")
        time.sleep(1)  # Let it run briefly

    print("Context exited, process cleaned up")
    if sp.result:
        print(f"Final result: {sp.result}")


def main():
    """Run all error handling examples"""
    print("Subprocess Error Handling Examples")
    print("=" * 35)

    examples = [
        basic_exception_handling,
        comprehensive_error_handler,
        timeout_strategies,
        return_code_interpretation,
        logging_and_auditing,
        recovery_and_retry_patterns,
        cross_platform_error_handling,
        context_managers_for_error_handling,
    ]

    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")

    print("\n" + "=" * 35)
    print("All error handling examples completed!")

    # Clean up log file
    if os.path.exists('subprocess_audit.log'):
        print("Cleaning up audit log...")
        os.remove('subprocess_audit.log')


if __name__ == '__main__':
    main()
