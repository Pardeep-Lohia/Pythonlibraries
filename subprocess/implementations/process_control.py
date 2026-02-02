#!/usr/bin/env python3
"""
Process Control Examples

This module demonstrates advanced process control techniques with subprocess,
including monitoring, termination, signal handling, and resource management.
"""

import subprocess
import signal
import time
import threading
import platform
import os
import psutil


def basic_process_monitoring():
    """Demonstrate basic process monitoring"""
    print("=== Basic Process Monitoring ===")

    # Start a background process
    process = subprocess.Popen(['python3', '-c', '''
import time
for i in range(10):
    print(f"Working {i+1}/10")
    time.sleep(0.5)
print("Done!")
'''],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

    print(f"Started process with PID: {process.pid}")

    # Monitor the process
    while process.poll() is None:
        print(f"Process {process.pid} is still running...")
        time.sleep(1)

    # Get final result
    stdout, stderr = process.communicate()
    print(f"Process completed with return code: {process.returncode}")
    print(f"Output: {stdout.strip()}")


def process_termination_examples():
    """Demonstrate different process termination methods"""
    print("\n=== Process Termination Examples ===")

    # Start a long-running process
    process = subprocess.Popen(['python3', '-c', '''
import time
import signal
import sys

def signal_handler(sig, frame):
    print(f"Received signal {sig}, cleaning up...")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

for i in range(100):
    print(f"Iteration {i+1}")
    time.sleep(0.2)
'''],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

    print(f"Started process {process.pid}")

    # Let it run for a few seconds
    time.sleep(2)

    # Terminate gracefully
    print("Sending SIGTERM...")
    process.terminate()

    try:
        stdout, stderr = process.communicate(timeout=5)
        print("Process terminated gracefully")
        print(f"Output: {stdout.strip()}")
    except subprocess.TimeoutExpired:
        print("Process didn't terminate gracefully, killing...")
        process.kill()
        stdout, stderr = process.communicate()
        print("Process forcefully killed")

    print(f"Final return code: {process.returncode}")


def signal_handling_examples():
    """Demonstrate signal handling with subprocess"""
    print("\n=== Signal Handling Examples ===")

    # Start a process that handles signals
    process = subprocess.Popen(['python3', '-c', '''
import signal
import time
import sys

def sigterm_handler(signum, frame):
    print("Received SIGTERM, shutting down gracefully...")
    sys.exit(0)

def sigint_handler(signum, frame):
    print("Received SIGINT, ignoring...")

signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigint_handler)

print("Process started, waiting for signals...")
for i in range(50):
    time.sleep(0.1)
    if i % 10 == 0:
        print(f"Still running... {i}")
'''],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

    print(f"Process {process.pid} started")

    # Wait a bit then send signals
    time.sleep(1)

    print("Sending SIGINT (should be ignored)...")
    if platform.system() != 'Windows':
        os.kill(process.pid, signal.SIGINT)
    else:
        # Windows signal handling is different
        process.terminate()

    time.sleep(1)

    print("Sending SIGTERM (should terminate gracefully)...")
    if platform.system() != 'Windows':
        os.kill(process.pid, signal.SIGTERM)
    else:
        process.terminate()

    # Wait for completion
    stdout, stderr = process.communicate(timeout=10)
    print(f"Process output: {stdout.strip()}")
    print(f"Return code: {process.returncode}")


def process_group_management():
    """Demonstrate process group management"""
    print("\n=== Process Group Management ===")

    if platform.system() == 'Windows':
        print("Process groups not fully supported on Windows")
        return

    # Start a process in a new session (becomes group leader)
    process = subprocess.Popen(['python3', '-c', '''
import time
import os

print(f"PID: {os.getpid()}")
print(f"PGID: {os.getpgid(0)}")
print(f"SID: {os.getsid(0)}")

for i in range(20):
    time.sleep(0.2)
    if i % 5 == 0:
        print(f"Child working... {i}")
'''],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True,
                              start_new_session=True)

    print(f"Parent process group: {os.getpgid(0)}")
    print(f"Child PID: {process.pid}")
    print(f"Child PGID: {os.getpgid(process.pid)}")

    # Let it run for a bit
    time.sleep(2)

    # Terminate the entire process group
    print("Terminating process group...")
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        stdout, stderr = process.communicate(timeout=5)
        print("Process group terminated")
        print(f"Output: {stdout.strip()}")
    except subprocess.TimeoutExpired:
        print("Process group didn't terminate, killing...")
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        process.wait()

    print(f"Final return code: {process.returncode}")


def resource_monitoring():
    """Demonstrate process resource monitoring"""
    print("\n=== Resource Monitoring ===")

    try:
        # Start a memory-intensive process
        process = subprocess.Popen(['python3', '-c', '''
import time
data = []
for i in range(100000):
    data.append('x' * 100)  # Allocate memory
    if i % 10000 == 0:
        print(f"Allocated {i} items")
        time.sleep(0.1)
print("Memory allocation complete")
'''],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

        # Monitor resources
        try:
            proc = psutil.Process(process.pid)
            print(f"Monitoring process {process.pid}")

            for _ in range(10):
                if process.poll() is not None:
                    break

                try:
                    memory_info = proc.memory_info()
                    cpu_percent = proc.cpu_percent()

                    print(f"  Memory: {memory_info.rss / 1024 / 1024:.1f} MB, "
                          f"CPU: {cpu_percent:.1f}%")
                except psutil.NoSuchProcess:
                    break

                time.sleep(0.5)

        except ImportError:
            print("psutil not available, skipping detailed monitoring")

        # Wait for completion
        stdout, stderr = process.communicate(timeout=30)
        print(f"Process completed: {stdout.strip()}")

    except subprocess.TimeoutExpired:
        print("Process timed out")
        process.kill()


def timeout_management():
    """Demonstrate timeout management techniques"""
    print("\n=== Timeout Management ===")

    # Example 1: Simple timeout
    print("Example 1: Simple timeout")
    try:
        result = subprocess.run(['sleep', '5'], timeout=2)
    except subprocess.TimeoutExpired:
        print("Command timed out after 2 seconds")

    # Example 2: Progressive timeouts
    print("\nExample 2: Progressive timeouts")
    timeouts = [1, 2, 5]
    for timeout in timeouts:
        try:
            result = subprocess.run(['sleep', '10'], timeout=timeout)
            print(f"Command completed within {timeout} seconds")
            break
        except subprocess.TimeoutExpired:
            print(f"Command timed out after {timeout} seconds, trying longer...")

    # Example 3: Timeout with cleanup
    print("\nExample 3: Timeout with cleanup")
    process = subprocess.Popen(['sleep', '10'])

    try:
        process.wait(timeout=3)
        print("Process completed normally")
    except subprocess.TimeoutExpired:
        print("Process timed out, cleaning up...")
        process.kill()
        try:
            process.wait(timeout=5)
            print("Process cleaned up successfully")
        except subprocess.TimeoutExpired:
            print("Process didn't respond to kill signal")


def process_pool_management():
    """Demonstrate managing multiple processes"""
    print("\n=== Process Pool Management ===")

    class SimpleProcessPool:
        """Simple process pool implementation"""

        def __init__(self, max_processes=3):
            self.max_processes = max_processes
            self.processes = []

        def add_process(self, command):
            """Add a process to the pool"""
            if len(self.processes) >= self.max_processes:
                self.wait_for_any()

            process = subprocess.Popen(command,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True)
            self.processes.append(process)
            return process

        def wait_for_any(self):
            """Wait for any process to complete"""
            while self.processes:
                for i, process in enumerate(self.processes):
                    if process.poll() is not None:
                        completed = self.processes.pop(i)
                        return completed
                time.sleep(0.1)

        def wait_all(self):
            """Wait for all processes to complete"""
            results = []
            for process in self.processes:
                stdout, stderr = process.communicate()
                results.append({
                    'pid': process.pid,
                    'returncode': process.returncode,
                    'stdout': stdout,
                    'stderr': stderr
                })
            self.processes.clear()
            return results

        def terminate_all(self):
            """Terminate all processes in the pool"""
            for process in self.processes:
                try:
                    process.terminate()
                except:
                    pass

            time.sleep(1)  # Give them time to terminate

            for process in self.processes:
                if process.poll() is None:
                    process.kill()

            self.processes.clear()

    # Use the process pool
    pool = SimpleProcessPool(max_processes=2)

    commands = [
        ['python3', '-c', 'import time; time.sleep(1); print("Task 1 done")'],
        ['python3', '-c', 'import time; time.sleep(2); print("Task 2 done")'],
        ['python3', '-c', 'import time; time.sleep(1); print("Task 3 done")'],
        ['python3', '-c', 'import time; time.sleep(3); print("Task 4 done")'],
    ]

    print("Starting processes...")
    for cmd in commands:
        pool.add_process(cmd)
        print(f"Added process, pool size: {len(pool.processes)}")

    print("Waiting for completion...")
    results = pool.wait_all()

    print("All processes completed:")
    for result in results:
        print(f"  PID {result['pid']}: return code {result['returncode']}")
        if result['stdout']:
            print(f"    Output: {result['stdout'].strip()}")


def context_manager_for_processes():
    """Demonstrate context manager for automatic cleanup"""
    print("\n=== Context Manager for Processes ===")

    class ManagedProcess:
        """Context manager for subprocess with automatic cleanup"""

        def __init__(self, command, **kwargs):
            self.command = command
            self.kwargs = kwargs
            self.process = None

        def __enter__(self):
            self.kwargs.setdefault('stdout', subprocess.PIPE)
            self.kwargs.setdefault('stderr', subprocess.PIPE)
            self.kwargs.setdefault('text', True)

            self.process = subprocess.Popen(self.command, **self.kwargs)
            return self.process

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.process and self.process.poll() is None:
                print(f"Cleaning up process {self.process.pid}...")

                # Try graceful termination first
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                    print("Process terminated gracefully")
                except subprocess.TimeoutExpired:
                    print("Process didn't terminate gracefully, killing...")
                    self.process.kill()
                    try:
                        self.process.wait(timeout=5)
                        print("Process killed")
                    except subprocess.TimeoutExpired:
                        print("Warning: Process may still be running")

    # Use the context manager
    with ManagedProcess(['python3', '-c', '''
import time
print("Process started")
for i in range(5):
    print(f"Working... {i+1}")
    time.sleep(0.5)
print("Process finished")
''']) as proc:
        print(f"Managed process started with PID: {proc.pid}")

        # Let it run for a bit
        time.sleep(2)

        # Process will be automatically cleaned up when exiting the context

    print("Context exited, process cleaned up")


def cross_platform_process_control():
    """Demonstrate cross-platform process control"""
    print("\n=== Cross-Platform Process Control ===")

    system = platform.system()

    if system == 'Windows':
        # Windows-specific process control
        print("Windows process control:")

        process = subprocess.Popen(['timeout', '10'],  # Windows timeout command
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

        print(f"Started Windows process {process.pid}")

        # Windows uses different termination
        time.sleep(2)
        process.terminate()

        try:
            stdout, stderr = process.communicate(timeout=5)
            print("Process terminated")
        except subprocess.TimeoutExpired:
            process.kill()
            print("Process killed")

    else:
        # Unix-like systems
        print("Unix process control:")

        process = subprocess.Popen(['sleep', '10'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

        print(f"Started Unix process {process.pid}")

        # Send SIGTERM
        time.sleep(2)
        os.kill(process.pid, signal.SIGTERM)

        try:
            stdout, stderr = process.communicate(timeout=5)
            print("Process terminated with SIGTERM")
        except subprocess.TimeoutExpired:
            os.kill(process.pid, signal.SIGKILL)
            process.wait()
            print("Process killed with SIGKILL")

    print(f"Final return code: {process.returncode}")


def advanced_monitoring_and_logging():
    """Demonstrate advanced monitoring and logging"""
    print("\n=== Advanced Monitoring and Logging ===")

    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO,
                       format='%(asctime)s - %(levelname)s - %(message)s')

    class ProcessMonitor:
        """Advanced process monitor with logging"""

        def __init__(self):
            self.logger = logging.getLogger('ProcessMonitor')

        def monitor_process(self, process, name="Process"):
            """Monitor a process with detailed logging"""
            self.logger.info(f"Starting monitoring of {name} (PID: {process.pid})")

            start_time = time.time()
            last_output_time = start_time

            while process.poll() is None:
                current_time = time.time()

                # Log periodic status
                if current_time - last_output_time >= 2:
                    elapsed = current_time - start_time
                    self.logger.info(f"{name} still running after {elapsed:.1f}s")
                    last_output_time = current_time

                time.sleep(0.5)

            elapsed = time.time() - start_time
            returncode = process.returncode

            if returncode == 0:
                self.logger.info(f"{name} completed successfully in {elapsed:.1f}s")
            else:
                self.logger.error(f"{name} failed with code {returncode} after {elapsed:.1f}s")

            return returncode

    # Use the monitor
    monitor = ProcessMonitor()

    process = subprocess.Popen(['python3', '-c', '''
import time
import random

for i in range(10):
    print(f"Step {i+1}/10")
    time.sleep(random.uniform(0.5, 1.5))

print("All steps completed")
'''],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

    return_code = monitor.monitor_process(process, "Sample Process")

    # Get final output
    stdout, stderr = process.communicate()
    if stdout:
        print(f"Final output: {stdout.strip()}")


def main():
    """Run all process control examples"""
    print("Process Control Examples")
    print("=" * 30)

    examples = [
        basic_process_monitoring,
        process_termination_examples,
        signal_handling_examples,
        process_group_management,
        resource_monitoring,
        timeout_management,
        process_pool_management,
        context_manager_for_processes,
        cross_platform_process_control,
        advanced_monitoring_and_logging,
    ]

    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")

    print("\n" + "=" * 30)
    print("All process control examples completed!")


if __name__ == '__main__':
    main()
