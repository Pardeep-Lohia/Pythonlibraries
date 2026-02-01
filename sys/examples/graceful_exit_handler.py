#!/usr/bin/env python3
"""
Graceful Exit Handler Example

Demonstrates how to implement graceful shutdown and cleanup using sys module,
including signal handling, resource cleanup, and proper exit codes.
"""

import sys
import os
import time
import signal
import atexit
import threading
from typing import Callable, List, Any


class GracefulExitHandler:
    """Handles graceful application shutdown with cleanup"""

    def __init__(self):
        self.exit_functions: List[Callable] = []
        self.shutdown_event = threading.Event()
        self.exit_code = 0
        self.setup_signal_handlers()
        self.setup_atexit_handler()

    def setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            """Handle termination signals"""
            signal_names = {
                signal.SIGINT: "SIGINT",
                signal.SIGTERM: "SIGTERM",
                signal.SIGHUP: "SIGHUP" if hasattr(signal, 'SIGHUP') else "SIGHUP(unavailable)",
            }
            signal_name = signal_names.get(signum, f"Signal {signum}")

            print(f"\nReceived {signal_name}, initiating graceful shutdown...")
            self.graceful_shutdown(128 + signum)  # Standard Unix exit codes

        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, signal_handler)

    def setup_atexit_handler(self):
        """Set up atexit handler for final cleanup"""
        atexit.register(self.final_cleanup)

    def add_exit_function(self, func: Callable, *args, **kwargs):
        """Add a function to be called during shutdown"""
        def wrapper():
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Error in exit function {func.__name__}: {e}", file=sys.stderr)

        self.exit_functions.append(wrapper)

    def graceful_shutdown(self, exit_code: int = 0):
        """Initiate graceful shutdown"""
        if self.shutdown_event.is_set():
            return  # Already shutting down

        self.shutdown_event.set()
        self.exit_code = exit_code

        print("Starting graceful shutdown sequence...")

        # Execute cleanup functions in reverse order
        for func in reversed(self.exit_functions):
            try:
                func()
            except Exception as e:
                print(f"Cleanup function failed: {e}", file=sys.stderr)

        print("Cleanup complete, exiting...")
        sys.exit(exit_code)

    def final_cleanup(self):
        """Final cleanup function called by atexit"""
        if not self.shutdown_event.is_set():
            print("Application terminated unexpectedly, performing final cleanup...")
            # Perform minimal cleanup
            for func in reversed(self.exit_functions):
                try:
                    func()
                except Exception as e:
                    print(f"Final cleanup error: {e}", file=sys.stderr)

    def wait_for_shutdown(self, timeout: float = None):
        """Wait for shutdown signal"""
        return self.shutdown_event.wait(timeout)

    def is_shutting_down(self) -> bool:
        """Check if shutdown has been initiated"""
        return self.shutdown_event.is_set()


class ResourceManager:
    """Manages resources that need cleanup"""

    def __init__(self, exit_handler: GracefulExitHandler):
        self.resources: List[Any] = []
        self.exit_handler = exit_handler
        self.exit_handler.add_exit_function(self.cleanup_all)

    def add_resource(self, resource: Any, cleanup_func: Callable = None):
        """Add a resource to be managed"""
        if cleanup_func is None:
            # Default cleanup based on resource type
            if hasattr(resource, 'close'):
                cleanup_func = lambda: resource.close()
            elif hasattr(resource, 'cleanup'):
                cleanup_func = lambda: resource.cleanup()
            else:
                cleanup_func = lambda: None

        self.resources.append((resource, cleanup_func))

    def cleanup_all(self):
        """Clean up all managed resources"""
        print(f"Cleaning up {len(self.resources)} resources...")
        for resource, cleanup_func in reversed(self.resources):
            try:
                cleanup_func()
                print(f"Cleaned up: {type(resource).__name__}")
            except Exception as e:
                print(f"Error cleaning up {type(resource).__name__}: {e}", file=sys.stderr)


def simulate_long_running_task(name: str, duration: float, exit_handler: GracefulExitHandler):
    """Simulate a long-running task that can be interrupted"""
    print(f"Starting task: {name}")

    start_time = time.time()
    while time.time() - start_time < duration:
        if exit_handler.is_shutting_down():
            print(f"Task {name} interrupted during shutdown")
            break

        time.sleep(0.1)  # Small sleep to prevent busy waiting

    if not exit_handler.is_shutting_down():
        print(f"Task {name} completed")


def database_simulation():
    """Simulate database operations"""
    print("Connecting to database...")

    # Simulate database connection
    class MockDatabase:
        def __init__(self):
            self.connected = True
            print("Database connected")

        def query(self, sql: str):
            if not self.connected:
                raise Exception("Database not connected")
            print(f"Executing: {sql}")
            time.sleep(0.1)  # Simulate query time
            return f"Results for: {sql}"

        def close(self):
            if self.connected:
                print("Closing database connection...")
                self.connected = False
                time.sleep(0.1)  # Simulate close time

    return MockDatabase()


def network_simulation():
    """Simulate network operations"""
    print("Opening network connections...")

    class MockNetwork:
        def __init__(self):
            self.connections = 3
            print(f"Opened {self.connections} network connections")

        def send_data(self, data: str):
            if self.connections == 0:
                raise Exception("No network connections available")
            print(f"Sending: {data}")
            time.sleep(0.05)

        def close(self):
            if self.connections > 0:
                print(f"Closing {self.connections} network connections...")
                self.connections = 0
                time.sleep(0.1)

    return MockNetwork()


def file_operations_simulation():
    """Simulate file operations"""
    print("Opening files...")

    import tempfile
    import json

    # Create temporary files
    temp_files = []
    for i in range(2):
        fd, path = tempfile.mkstemp(suffix=f'_demo_{i}.json')
        os.close(fd)  # Close the file descriptor

        # Write some data
        with open(path, 'w') as f:
            json.dump({"file": i, "data": f"content_{i}"}, f)

        temp_files.append(path)
        print(f"Created file: {os.path.basename(path)}")

    class MockFileManager:
        def __init__(self, files: List[str]):
            self.files = files

        def process_files(self):
            for path in self.files:
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                        print(f"Processed {os.path.basename(path)}: {data}")
                except Exception as e:
                    print(f"Error processing {os.path.basename(path)}: {e}")

        def cleanup(self):
            print(f"Cleaning up {len(self.files)} temporary files...")
            for path in self.files:
                try:
                    os.unlink(path)
                    print(f"Deleted: {os.path.basename(path)}")
                except Exception as e:
                    print(f"Error deleting {os.path.basename(path)}: {e}")

    return MockFileManager(temp_files)


def basic_graceful_exit_demo():
    """Demonstrate basic graceful exit handling"""
    print("=== Basic Graceful Exit Demo ===")
    print("Press Ctrl+C to trigger graceful shutdown")
    print("Or wait for automatic completion")
    print()

    exit_handler = GracefulExitHandler()

    # Add some cleanup functions
    def cleanup_temp_files():
        print("Cleaning up temporary files...")

    def save_state():
        print("Saving application state...")

    def close_connections():
        print("Closing network connections...")

    exit_handler.add_exit_function(cleanup_temp_files)
    exit_handler.add_exit_function(save_state)
    exit_handler.add_exit_function(close_connections)

    # Simulate main application loop
    print("Application running... (Ctrl+C to exit)")

    try:
        for i in range(50):  # About 5 seconds
            if exit_handler.is_shutting_down():
                break
            time.sleep(0.1)
            if i % 10 == 0:
                print(f"Heartbeat: {i//10 + 1}/5")

        if not exit_handler.is_shutting_down():
            print("Application completed normally")
            exit_handler.graceful_shutdown(0)

    except KeyboardInterrupt:
        print("Received keyboard interrupt")
        exit_handler.graceful_shutdown(130)  # Standard SIGINT exit code


def resource_management_demo():
    """Demonstrate resource management with graceful shutdown"""
    print("=== Resource Management Demo ===")

    exit_handler = GracefulExitHandler()
    resource_manager = ResourceManager(exit_handler)

    # Initialize resources
    db = database_simulation()
    network = network_simulation()
    file_manager = file_operations_simulation()

    # Register resources
    resource_manager.add_resource(db)
    resource_manager.add_resource(network)
    resource_manager.add_resource(file_manager)

    print("\nResources initialized. Press Ctrl+C to shutdown gracefully")
    print("Or wait for operations to complete")
    print()

    try:
        # Simulate operations
        for i in range(20):
            if exit_handler.is_shutting_down():
                break

            # Perform some operations
            if i % 5 == 0:
                db.query(f"SELECT * FROM table_{i//5}")
                network.send_data(f"Data packet {i}")
                file_manager.process_files()

            time.sleep(0.2)

        if not exit_handler.is_shutting_down():
            print("All operations completed successfully")
            exit_handler.graceful_shutdown(0)

    except KeyboardInterrupt:
        print("Operations interrupted by user")
        exit_handler.graceful_shutdown(130)


def multi_threaded_graceful_exit():
    """Demonstrate graceful exit with multiple threads"""
    print("=== Multi-threaded Graceful Exit Demo ===")

    exit_handler = GracefulExitHandler()

    def worker_thread(thread_id: int):
        """Worker thread function"""
        print(f"Thread {thread_id} starting")

        # Simulate work
        for i in range(30):
            if exit_handler.is_shutting_down():
                print(f"Thread {thread_id} shutting down gracefully")
                break

            time.sleep(0.1)

            if i % 10 == 0:
                print(f"Thread {thread_id}: checkpoint {i//10 + 1}")

        print(f"Thread {thread_id} finished")

    # Start worker threads
    threads = []
    for i in range(3):
        thread = threading.Thread(target=worker_thread, args=(i+1,))
        threads.append(thread)
        thread.start()

    print("All threads started. Press Ctrl+C to shutdown gracefully")
    print()

    try:
        # Wait for threads or shutdown signal
        while True:
            if exit_handler.is_shutting_down():
                break

            # Check if all threads are done
            if all(not t.is_alive() for t in threads):
                print("All threads completed")
                break

            time.sleep(0.1)

        if not exit_handler.is_shutting_down():
            exit_handler.graceful_shutdown(0)

    except KeyboardInterrupt:
        print("Shutdown requested by user")
        exit_handler.graceful_shutdown(130)

    # Wait for threads to finish
    for thread in threads:
        thread.join(timeout=2.0)
        if thread.is_alive():
            print(f"Thread {thread.name} did not finish cleanly")


def error_handling_with_graceful_exit():
    """Demonstrate error handling combined with graceful exit"""
    print("=== Error Handling with Graceful Exit ===")

    exit_handler = GracefulExitHandler()

    def risky_operation(name: str, should_fail: bool = False):
        """Simulate an operation that might fail"""
        print(f"Starting operation: {name}")

        if should_fail:
            raise Exception(f"Operation {name} failed intentionally")

        time.sleep(0.5)
        print(f"Operation {name} completed successfully")
        return f"Result of {name}"

    def error_recovery():
        """Error recovery function"""
        print("Performing error recovery...")
        time.sleep(0.2)
        print("Error recovery completed")

    exit_handler.add_exit_function(error_recovery)

    try:
        # Perform operations, some will fail
        operations = [
            ("safe_operation", False),
            ("failing_operation", True),
            ("another_safe", False),
        ]

        results = []
        for name, should_fail in operations:
            try:
                result = risky_operation(name, should_fail)
                results.append(result)
            except Exception as e:
                print(f"Operation {name} failed: {e}")
                print("Initiating graceful shutdown due to error...")
                exit_handler.graceful_shutdown(1)  # Error exit code

        print(f"All operations completed. Results: {results}")
        exit_handler.graceful_shutdown(0)

    except KeyboardInterrupt:
        print("Interrupted by user during error handling")
        exit_handler.graceful_shutdown(130)


def main():
    """Main function with different graceful exit demonstrations"""

    demos = {
        'basic': basic_graceful_exit_demo,
        'resources': resource_management_demo,
        'threads': multi_threaded_graceful_exit,
        'errors': error_handling_with_graceful_exit,
    }

    if len(sys.argv) < 2:
        print("Graceful Exit Handler Demonstrations")
        print("====================================")
        print()
        print("Available demonstrations:")
        for name in demos.keys():
            print(f"  {name}")
        print()
        print("Usage: python graceful_exit_handler.py <demo_name>")
        print("Example: python graceful_exit_handler.py basic")
        print()
        print("Note: Most demos respond to Ctrl+C for graceful shutdown")
        return

    demo_name = sys.argv[1].lower()

    if demo_name in demos:
        try:
            demos[demo_name]()
        except KeyboardInterrupt:
            print("\nDemo interrupted by user")
            sys.exit(130)
        except Exception as e:
            print(f"\nDemo failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        sys.stderr.write(f"Unknown demonstration: {demo_name}\n")
        sys.stderr.write(f"Available demos: {', '.join(demos.keys())}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
