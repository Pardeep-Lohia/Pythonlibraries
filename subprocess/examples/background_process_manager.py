#!/usr/bin/env python3
"""
Background Process Manager

This module demonstrates managing long-running background processes using subprocess,
including monitoring, logging, resource management, and graceful shutdown.
"""

import subprocess
import threading
import time
import signal
import os
import logging
import psutil
from typing import Dict, List, Optional
import sys


class BackgroundProcess:
    """Represents a background process with monitoring capabilities"""

    def __init__(self, command: List[str], name: str = None, env: Dict = None,
                 cwd: str = None, timeout: int = None):
        self.command = command
        self.name = name or f"Process-{id(self)}"
        self.env = env or os.environ.copy()
        self.cwd = cwd
        self.timeout = timeout

        self.process: Optional[subprocess.Popen] = None
        self.start_time: Optional[float] = None
        self.thread: Optional[threading.Thread] = None
        self.monitoring = False
        self.logger = logging.getLogger(f"BackgroundProcess.{self.name}")

    def start(self) -> bool:
        """Start the background process"""
        try:
            self.logger.info(f"Starting process: {' '.join(self.command)}")

            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=self.env,
                cwd=self.cwd,
                start_new_session=True  # Create new process group
            )

            self.start_time = time.time()
            self.logger.info(f"Process started with PID: {self.process.pid}")

            # Start monitoring thread
            self.monitoring = True
            self.thread = threading.Thread(target=self._monitor_process, daemon=True)
            self.thread.start()

            return True

        except Exception as e:
            self.logger.error(f"Failed to start process: {e}")
            return False

    def stop(self, timeout: int = 10) -> bool:
        """Stop the background process gracefully"""
        if not self.process or self.process.poll() is not None:
            self.logger.info("Process already stopped")
            return True

        self.logger.info(f"Stopping process {self.process.pid}")

        try:
            # Try graceful termination first
            self.process.terminate()

            # Wait for process to terminate
            try:
                self.process.wait(timeout=timeout)
                self.logger.info("Process terminated gracefully")
                return True

            except subprocess.TimeoutExpired:
                self.logger.warning("Process didn't terminate gracefully, killing...")

                # Force kill if graceful termination failed
                self.process.kill()
                try:
                    self.process.wait(timeout=5)
                    self.logger.info("Process killed")
                    return True
                except subprocess.TimeoutExpired:
                    self.logger.error("Process couldn't be killed")
                    return False

        except Exception as e:
            self.logger.error(f"Error stopping process: {e}")
            return False
        finally:
            self.monitoring = False

    def is_running(self) -> bool:
        """Check if process is still running"""
        return self.process is not None and self.process.poll() is None

    def get_status(self) -> Dict:
        """Get process status information"""
        if not self.process:
            return {'status': 'not_started'}

        returncode = self.process.poll()

        if returncode is None:
            status = 'running'
        elif returncode == 0:
            status = 'completed'
        else:
            status = 'failed'

        info = {
            'name': self.name,
            'pid': self.process.pid,
            'status': status,
            'returncode': returncode,
            'runtime': time.time() - self.start_time if self.start_time else 0
        }

        # Try to get resource usage
        try:
            if self.is_running():
                proc = psutil.Process(self.process.pid)
                memory_info = proc.memory_info()
                cpu_percent = proc.cpu_percent()

                info.update({
                    'memory_mb': memory_info.rss / 1024 / 1024,
                    'cpu_percent': cpu_percent
                })
        except (psutil.NoSuchProcess, ImportError):
            pass

        return info

    def _monitor_process(self):
        """Monitor process in background thread"""
        while self.monitoring and self.process:
            if self.process.poll() is not None:
                # Process has finished
                returncode = self.process.returncode
                runtime = time.time() - self.start_time

                if returncode == 0:
                    self.logger.info(f"Process completed successfully in {runtime:.2f} seconds")
                else:
                    self.logger.error(f"Process failed with return code {returncode} after {runtime:.2f} seconds")
                break

            time.sleep(1)  # Check every second


class BackgroundProcessManager:
    """Manager for multiple background processes"""

    def __init__(self, max_processes: int = 10):
        self.max_processes = max_processes
        self.processes: Dict[str, BackgroundProcess] = {}
        self.logger = logging.getLogger("BackgroundProcessManager")

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def add_process(self, name: str, command: List[str], **kwargs) -> bool:
        """Add a new background process"""
        if name in self.processes:
            self.logger.warning(f"Process '{name}' already exists")
            return False

        if len(self.processes) >= self.max_processes:
            self.logger.error(f"Maximum processes ({self.max_processes}) reached")
            return False

        process = BackgroundProcess(command, name, **kwargs)
        self.processes[name] = process

        self.logger.info(f"Added process '{name}': {' '.join(command)}")
        return True

    def start_process(self, name: str) -> bool:
        """Start a specific process"""
        if name not in self.processes:
            self.logger.error(f"Process '{name}' not found")
            return False

        return self.processes[name].start()

    def stop_process(self, name: str, timeout: int = 10) -> bool:
        """Stop a specific process"""
        if name not in self.processes:
            self.logger.error(f"Process '{name}' not found")
            return False

        return self.processes[name].stop(timeout)

    def start_all(self) -> int:
        """Start all processes"""
        started = 0
        for name, process in self.processes.items():
            if not process.is_running():
                if process.start():
                    started += 1

        self.logger.info(f"Started {started} processes")
        return started

    def stop_all(self, timeout: int = 10) -> int:
        """Stop all processes"""
        stopped = 0
        for name, process in self.processes.items():
            if process.is_running():
                if process.stop(timeout):
                    stopped += 1

        self.logger.info(f"Stopped {stopped} processes")
        return stopped

    def get_status(self) -> Dict[str, Dict]:
        """Get status of all processes"""
        return {name: process.get_status() for name, process in self.processes.items()}

    def list_processes(self) -> List[Dict]:
        """List all processes with their status"""
        processes = []
        for name, process in self.processes.items():
            status = process.get_status()
            status['name'] = name
            processes.append(status)

        return processes

    def wait_for_completion(self, timeout: int = None) -> bool:
        """Wait for all processes to complete"""
        start_time = time.time()

        while True:
            all_completed = all(not process.is_running() for process in self.processes.values())

            if all_completed:
                self.logger.info("All processes completed")
                return True

            if timeout and (time.time() - start_time) > timeout:
                self.logger.warning(f"Timeout waiting for processes to complete")
                return False

            time.sleep(1)

    def cleanup_zombies(self) -> int:
        """Clean up any zombie processes"""
        cleaned = 0
        for name, process in list(self.processes.items()):
            if process.process and process.process.poll() is not None:
                # Process has finished, remove from active list
                del self.processes[name]
                cleaned += 1

        if cleaned > 0:
            self.logger.info(f"Cleaned up {cleaned} completed processes")

        return cleaned

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop_all(timeout=30)
        sys.exit(0)


def demonstrate_basic_usage():
    """Demonstrate basic background process management"""
    print("=== Basic Background Process Management ===")

    # Create process manager
    manager = BackgroundProcessManager()

    # Add a simple background process
    manager.add_process(
        'echo_server',
        ['python3', '-c', '''
import time
import sys

print("Echo server started")
sys.stdout.flush()

for i in range(10):
    print(f"Server running... {i+1}")
    sys.stdout.flush()
    time.sleep(1)

print("Echo server finished")
'''],
        name='Echo Server'
    )

    # Start the process
    if manager.start_process('echo_server'):
        print("Process started successfully")

        # Monitor for a few seconds
        for i in range(5):
            status = manager.get_status()
            echo_status = status.get('echo_server', {})
            print(f"Status: {echo_status.get('status', 'unknown')}")
            time.sleep(1)

        # Stop the process
        manager.stop_process('echo_server')
        print("Process stopped")

    # Show final status
    status = manager.get_status()
    print(f"Final status: {status}")


def demonstrate_multiple_processes():
    """Demonstrate managing multiple background processes"""
    print("\n=== Multiple Process Management ===")

    manager = BackgroundProcessManager(max_processes=5)

    # Add multiple processes
    processes = [
        ('web_server', ['python3', '-c', '''
import time
print("Web server started on port 8000")
for i in range(20):
    print(f"Handling request {i+1}")
    time.sleep(0.5)
print("Web server stopped")
''']),
        ('database', ['python3', '-c', '''
import time
print("Database started")
for i in range(15):
    print(f"Processing query {i+1}")
    time.sleep(0.7)
print("Database stopped")
''']),
        ('cache', ['python3', '-c', '''
import time
print("Cache server started")
for i in range(25):
    print(f"Cache hit/miss {i+1}")
    time.sleep(0.4)
print("Cache server stopped")
'''])
    ]

    # Add all processes
    for name, command in processes:
        manager.add_process(name, command)

    # Start all processes
    started = manager.start_all()
    print(f"Started {started} processes")

    # Monitor all processes
    for i in range(10):
        all_status = manager.get_status()
        running = sum(1 for s in all_status.values() if s.get('status') == 'running')
        print(f"Iteration {i+1}: {running} processes running")
        time.sleep(1)

    # Stop all processes
    stopped = manager.stop_all(timeout=15)
    print(f"Stopped {stopped} processes")

    # Show final status
    final_status = manager.list_processes()
    for proc in final_status:
        print(f"{proc['name']}: {proc['status']} (runtime: {proc.get('runtime', 0):.1f}s)")


def demonstrate_process_monitoring():
    """Demonstrate advanced process monitoring"""
    print("\n=== Advanced Process Monitoring ===")

    manager = BackgroundProcessManager()

    # Add a CPU and memory intensive process
    manager.add_process(
        'intensive_task',
        ['python3', '-c', '''
import time
import math

print("Starting intensive computation")
data = []
for i in range(100000):
    data.append(math.sin(i) * math.cos(i))
    if i % 10000 == 0:
        print(f"Progress: {i}/100000")
print("Computation completed")
''']
    )

    # Start the process
    manager.start_process('intensive_task')

    # Monitor resources
    print("Monitoring process resources...")
    for i in range(8):
        status = manager.get_status()
        task_status = status.get('intensive_task', {})

        if 'memory_mb' in task_status:
            print(f"Memory: {task_status['memory_mb']:.1f} MB, "
                  f"CPU: {task_status.get('cpu_percent', 0):.1f}%")
        else:
            print(f"Status: {task_status.get('status', 'unknown')}")

        time.sleep(1)

    # Wait for completion
    manager.wait_for_completion(timeout=30)
    print("Process completed")


def demonstrate_graceful_shutdown():
    """Demonstrate graceful shutdown handling"""
    print("\n=== Graceful Shutdown Handling ===")

    manager = BackgroundProcessManager()

    # Add processes that handle signals
    manager.add_process(
        'signal_handler',
        ['python3', '-c', '''
import signal
import time
import sys

def signal_handler(signum, frame):
    print(f"Received signal {signum}, cleaning up...")
    print("Cleanup completed")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

print("Process started, waiting for signals...")
for i in range(50):
    time.sleep(0.2)
    if i % 10 == 0:
        print(f"Still running... {i}")
''']
    )

    # Start the process
    manager.start_process('signal_handler')

    # Let it run for a few seconds
    time.sleep(3)

    # Trigger graceful shutdown
    print("Initiating graceful shutdown...")
    manager.stop_all(timeout=10)

    print("Shutdown completed")


def demonstrate_error_handling():
    """Demonstrate error handling in background processes"""
    print("\n=== Error Handling ===")

    manager = BackgroundProcessManager()

    # Add processes that will fail
    manager.add_process('failing_process',
                       ['python3', '-c', 'import sys; sys.exit(42)'])

    manager.add_process('nonexistent_command',
                       ['this_command_does_not_exist'])

    # Start processes
    manager.start_all()

    # Monitor for completion
    start_time = time.time()
    while time.time() - start_time < 10:
        status = manager.get_status()

        for name, proc_status in status.items():
            if proc_status.get('status') in ['completed', 'failed']:
                returncode = proc_status.get('returncode')
                if returncode == 0:
                    print(f"✓ {name} completed successfully")
                else:
                    print(f"✗ {name} failed with code {returncode}")

        time.sleep(0.5)

        # Break if all processes are done
        if all(s.get('status') in ['completed', 'failed'] for s in status.values()):
            break

    # Clean up
    manager.stop_all()


def create_service_manager():
    """Create a service-like process manager"""
    print("\n=== Service Manager Example ===")

    class ServiceManager(BackgroundProcessManager):
        """Service manager with restart capabilities"""

        def __init__(self):
            super().__init__()
            self.services = {}  # name -> service config

        def add_service(self, name: str, command: List[str], restart_on_failure: bool = True,
                       max_restarts: int = 3, **kwargs):
            """Add a service with restart policy"""
            self.services[name] = {
                'command': command,
                'restart_on_failure': restart_on_failure,
                'max_restarts': max_restarts,
                'restart_count': 0,
                'kwargs': kwargs
            }

            self.add_process(name, command, **kwargs)

        def monitor_services(self):
            """Monitor services and restart failed ones"""
            while True:
                status = self.get_status()

                for name, proc_status in status.items():
                    if name in self.services:
                        service = self.services[name]

                        if (proc_status.get('status') == 'failed' and
                            service['restart_on_failure'] and
                            service['restart_count'] < service['max_restarts']):

                            service['restart_count'] += 1
                            print(f"Restarting service {name} (attempt {service['restart_count']})")

                            # Stop the failed process
                            self.stop_process(name)

                            # Start a new instance
                            self.start_process(name)

                time.sleep(2)

    # Create service manager
    service_manager = ServiceManager()

    # Add services
    service_manager.add_service(
        'ping_service',
        ['python3', '-c', '''
import time
import random

print("Ping service started")
for i in range(10):
    print(f"Ping {i+1}")
    time.sleep(1)

    # Simulate occasional failure
    if random.random() < 0.3:
        print("Simulated failure")
        import sys
        sys.exit(1)

print("Ping service completed")
'''],
        restart_on_failure=True
    )

    # Start services
    service_manager.start_all()

    # Monitor for a short time
    print("Monitoring services (10 seconds)...")
    monitor_thread = threading.Thread(target=service_manager.monitor_services, daemon=True)
    monitor_thread.start()

    time.sleep(10)

    # Stop all services
    service_manager.stop_all()
    print("All services stopped")


def main():
    """Run all background process management examples"""
    print("Background Process Manager Examples")
    print("=" * 40)

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    examples = [
        demonstrate_basic_usage,
        demonstrate_multiple_processes,
        demonstrate_process_monitoring,
        demonstrate_graceful_shutdown,
        demonstrate_error_handling,
        create_service_manager,
    ]

    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")

    print("\n" + "=" * 40)
    print("All background process examples completed!")


if __name__ == '__main__':
    main()
