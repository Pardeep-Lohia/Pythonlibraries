#!/usr/bin/env python3
"""
Advanced Popen Usage Examples

This module demonstrates advanced usage of subprocess.Popen() for complex
process management scenarios including asynchronous execution, real-time I/O,
process monitoring, and cross-platform compatibility.
"""

import subprocess
import sys
import threading
import time
import platform
import os
import signal


def basic_popen_usage():
    """Demonstrate basic Popen usage"""
    print("=== Basic Popen Usage ===")

    # Start a simple process
    process = subprocess.Popen(['echo', 'Hello from Popen'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

    # Wait for completion and get output
    stdout, stderr = process.communicate()

    print(f"Return code: {process.returncode}")
    print(f"Output: {stdout.strip()}")
    if stderr:
        print(f"Errors: {stderr.strip()}")


def asynchronous_execution():
    """Demonstrate asynchronous process execution"""
    print("\n=== Asynchronous Execution ===")

    # Start multiple processes concurrently
    processes = []

    commands = [
        ['python3', '-c', 'import time; time.sleep(1); print("Process 1 done")'],
        ['python3', '-c', 'import time; time.sleep(2); print("Process 2 done")'],
        ['python3', '-c', 'import time; time.sleep(1); print("Process 3 done")'],
    ]

    print("Starting processes asynchronously...")
    for cmd in commands:
        process = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
        processes.append(process)
        print(f"Started process {process.pid}")

    # Monitor completion
    completed = 0
    while completed < len(processes):
        for i, process in enumerate(processes):
            if process.poll() is not None and process.returncode is not None:
                stdout, stderr = process.communicate()
                print(f"Process {process.pid} completed with code {process.returncode}")
                if stdout.strip():
                    print(f"  Output: {stdout.strip()}")
                completed += 1
                processes[i] = None  # Mark as processed

        time.sleep(0.1)

    print("All processes completed")


def real_time_output_reading():
    """Demonstrate reading output in real-time"""
    print("\n=== Real-Time Output Reading ===")

    # Start a process that produces output over time
    if platform.system() == 'Windows':
        cmd = ['ping', '-n', '4', '127.0.0.1']
    else:
        cmd = ['ping', '-c', '4', '127.0.0.1']

    process = subprocess.Popen(cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              text=True,
                              bufsize=1)

    print("Reading output in real-time:")
    while True:
        line = process.stdout.readline()
        if line == '' and process.poll() is not None:
            break
        if line:
            print(f"  {line.strip()}")

    print(f"Process completed with return code: {process.returncode}")


def bidirectional_communication():
    """Demonstrate bidirectional communication with a subprocess"""
    print("\n=== Bidirectional Communication ===")

    # Start an interactive Python process
    process = subprocess.Popen([sys.executable, '-c', '''
import sys
print("Interactive subprocess started")
sys.stdout.flush()

while True:
    try:
        line = input(">>> ")
        if line.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
        try:
            result = eval(line)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
        sys.stdout.flush()
    except (EOFError, KeyboardInterrupt):
        break
'''],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

    # Interact with the process
    interactions = [
        ('2 + 3', '5'),
        ('len("hello")', '5'),
        ('print("Hello")', None),  # This will print directly
        ('quit', 'Goodbye!')
    ]

    for input_line, expected in interactions:
        print(f"Sending: {input_line}")

        # Send input
        process.stdin.write(input_line + '\n')
        process.stdin.flush()

        # Read response(s)
        time.sleep(0.1)  # Allow subprocess to process

        # Read all available output
        while True:
            line = process.stdout.readline()
            if line == '' and process.poll() is not None:
                break
            if line:
                print(f"  Received: {line.strip()}")
            else:
                break

    # Close stdin and get remaining output
    process.stdin.close()
    remaining, errors = process.communicate()

    if remaining:
        print(f"Remaining output: {remaining.strip()}")

    print(f"Subprocess return code: {process.returncode}")


def process_monitoring_and_control():
    """Demonstrate process monitoring and control"""
    print("\n=== Process Monitoring and Control ===")

    # Start a long-running process
    process = subprocess.Popen(['python3', '-c', '''
import time
import signal
import sys

def signal_handler(signum, frame):
    print(f"Received signal {signum}, cleaning up...")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

print("Process started, working...")
for i in range(20):
    print(f"Iteration {i+1}/20")
    time.sleep(0.5)
print("Process completed normally")
'''],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

    print(f"Started process {process.pid}")

    # Monitor for a few seconds
    start_time = time.time()
    while time.time() - start_time < 3:
        if process.poll() is not None:
            break
        time.sleep(0.1)

    # Check if still running
    if process.poll() is None:
        print("Process is still running, terminating...")

        # Try graceful termination
        if platform.system() != 'Windows':
            process.terminate()
            try:
                process.wait(timeout=3)
                print("Process terminated gracefully")
            except subprocess.TimeoutExpired:
                print("Process didn't terminate gracefully, killing...")
                process.kill()
                process.wait()
        else:
            process.terminate()
            process.wait()

    # Get final output
    stdout, stderr = process.communicate()
    print(f"Final return code: {process.returncode}")
    if stdout:
        lines = stdout.strip().split('\n')
        print(f"Output lines: {len(lines)}")


def resource_limits():
    """Demonstrate setting resource limits on subprocesses"""
    print("\n=== Resource Limits ===")

    try:
        import resource

        # Set resource limits for child process
        def run_with_limits():
            # CPU time limit (10 seconds)
            resource.setrlimit(resource.RLIMIT_CPU, (10, 10))

            # Memory limit (50MB)
            resource.setrlimit(resource.RLIMIT_AS, (50 * 1024 * 1024, 50 * 1024 * 1024))

            # Run a potentially resource-intensive process
            subprocess.run(['python3', '-c', '''
import time
data = []
try:
    while True:
        data.extend([0] * 100000)  # Try to use lots of memory
        time.sleep(0.1)
except MemoryError:
    print("Memory limit reached")
'''])

        print("Running process with resource limits...")
        process = subprocess.Popen(run_with_limits,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

        stdout, stderr = process.communicate(timeout=15)
        print(f"Process completed with code: {process.returncode}")
        if stdout:
            print(f"Output: {stdout.strip()}")
        if stderr:
            print(f"Errors: {stderr.strip()}")

    except ImportError:
        print("Resource limits not available on this platform")


def custom_environment():
    """Demonstrate running processes with custom environments"""
    print("\n=== Custom Environment ===")

    # Create custom environment
    env = os.environ.copy()
    env['CUSTOM_VAR'] = 'Hello from Popen'
    env['PATH'] = '/usr/local/bin:/usr/bin:/bin'  # Secure PATH

    # Remove potentially dangerous variables
    for var in ['LD_LIBRARY_PATH', 'LD_PRELOAD']:
        env.pop(var, None)

    process = subprocess.Popen(['python3', '-c', '''
import os
print(f"CUSTOM_VAR: {os.environ.get('CUSTOM_VAR', 'Not set')}")
print(f"PATH: {os.environ.get('PATH', 'Not set')[:50]}...")
'''],
                              env=env,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)

    stdout, stderr = process.communicate()
    print("Process output:")
    print(stdout.strip())


def process_groups_and_sessions():
    """Demonstrate process groups and sessions"""
    print("\n=== Process Groups and Sessions ===")

    if platform.system() == 'Windows':
        print("Process groups not fully supported on Windows")
        return

    # Start process in new session (becomes group leader)
    process = subprocess.Popen(['python3', '-c', '''
import os
import time

print(f"PID: {os.getpid()}")
print(f"PGID: {os.getpgid(0)}")
print(f"SID: {os.getsid(0)}")

for i in range(10):
    time.sleep(0.2)
    if i % 3 == 0:
        print(f"Working... {i}")
'''],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True,
                              start_new_session=True)

    print(f"Parent PID: {os.getpid()}")
    print(f"Child PID: {process.pid}")
    print(f"Child PGID: {os.getpgid(process.pid)}")
    print(f"Child SID: {os.getsid(process.pid)}")

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


def non_blocking_io():
    """Demonstrate non-blocking I/O operations"""
    print("\n=== Non-Blocking I/O ===")

    try:
        import fcntl
        import select

        # Start a process
        process = subprocess.Popen(['python3', '-c', '''
import time
for i in range(10):
    print(f"Line {i+1}")
    time.sleep(0.2)
'''],
                                  stdout=subprocess.PIPE,
                                  text=True)

        # Make stdout non-blocking
        fd = process.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        print("Reading non-blocking output:")
        output_lines = []

        while process.poll() is None or output_lines:
            # Check if data is available
            ready, _, _ = select.select([process.stdout], [], [], 0.1)

            if ready:
                try:
                    line = process.stdout.readline()
                    if line:
                        output_lines.append(line.strip())
                        print(f"  Read: {line.strip()}")
                except OSError:
                    # No data available
                    pass

            # Process completed
            if process.poll() is not None and not ready:
                break

        print(f"Total lines read: {len(output_lines)}")

    except ImportError:
        print("Non-blocking I/O not available on this platform")


def cross_platform_popen():
    """Demonstrate cross-platform Popen usage"""
    print("\n=== Cross-Platform Popen ===")

    system = platform.system()

    if system == 'Windows':
        # Windows-specific process
        print("Windows process:")
        process = subprocess.Popen(['cmd', '/c', 'echo Windows process'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

    elif system == 'Darwin':  # macOS
        # macOS-specific process
        print("macOS process:")
        process = subprocess.Popen(['echo', 'macOS process'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

    else:  # Linux and other Unix
        # Unix-specific process
        print("Unix process:")
        process = subprocess.Popen(['echo', 'Unix process'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)

    stdout, stderr = process.communicate()
    print(f"Output: {stdout.strip()}")
    print(f"Return code: {process.returncode}")


def error_handling_with_popen():
    """Demonstrate error handling with Popen"""
    print("\n=== Error Handling with Popen ===")

    # Test various error conditions
    test_cases = [
        (['echo', 'Success'], "Normal success"),
        (['false'], "Command failure"),
        (['nonexistent_command'], "Command not found"),
        (['sleep', '10'], "Timeout case"),
    ]

    for cmd, description in test_cases:
        print(f"\nTesting: {description}")
        print(f"Command: {' '.join(cmd)}")

        try:
            process = subprocess.Popen(cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True)

            if 'sleep' in cmd:
                # Timeout test
                try:
                    stdout, stderr = process.communicate(timeout=2)
                    print("  Result: Completed within timeout")
                except subprocess.TimeoutExpired:
                    print("  Result: TimeoutExpired")
                    process.kill()
                    process.wait()
            else:
                stdout, stderr = process.communicate(timeout=10)
                print(f"  Result: returncode={process.returncode}")

            if stdout:
                print(f"  Output: {stdout.strip()}")
            if stderr:
                print(f"  Errors: {stderr.strip()}")

        except FileNotFoundError:
            print("  Result: FileNotFoundError")
        except Exception as e:
            print(f"  Result: {type(e).__name__}: {e}")


def advanced_popen_patterns():
    """Demonstrate advanced Popen patterns"""
    print("\n=== Advanced Popen Patterns ===")

    # Context manager for Popen
    class ManagedPopen:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self.process = None

        def __enter__(self):
            self.kwargs.setdefault('stdout', subprocess.PIPE)
            self.kwargs.setdefault('stderr', subprocess.PIPE)
            self.kwargs.setdefault('text', True)
            self.process = subprocess.Popen(*self.args, **self.kwargs)
            return self.process

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.process and self.process.poll() is None:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait()

    # Use context manager
    print("Using context manager for automatic cleanup:")
    with ManagedPopen(['python3', '-c', '''
import time
print("Process started")
time.sleep(2)
print("Process finished")
''']) as proc:
        print(f"Process {proc.pid} started")
        time.sleep(1)  # Let it run briefly

    print("Context exited, process cleaned up automatically")

    # Process pool with Popen
    print("\nProcess pool pattern:")
    processes = []
    commands = [
        ['python3', '-c', 'print("Task 1")'],
        ['python3', '-c', 'print("Task 2")'],
        ['python3', '-c', 'print("Task 3")'],
    ]

    # Start all processes
    for cmd in commands:
        process = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True)
        processes.append(process)

    # Collect results
    results = []
    for process in processes:
        stdout, stderr = process.communicate()
        results.append({
            'pid': process.pid,
            'returncode': process.returncode,
            'stdout': stdout.strip(),
            'stderr': stderr.strip()
        })

    for result in results:
        print(f"Process {result['pid']}: {result['stdout']}")


def main():
    """Run all Popen examples"""
    print("Advanced Popen Usage Examples")
    print("=" * 35)

    examples = [
        basic_popen_usage,
        asynchronous_execution,
        real_time_output_reading,
        bidirectional_communication,
        process_monitoring_and_control,
        resource_limits,
        custom_environment,
        process_groups_and_sessions,
        non_blocking_io,
        cross_platform_popen,
        error_handling_with_popen,
        advanced_popen_patterns,
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
    print("All Popen examples completed!")


if __name__ == '__main__':
    main()
