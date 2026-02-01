#!/usr/bin/env python3
"""
Exception Hooks Implementation

This module demonstrates advanced exception handling using sys module,
including custom exception hooks, unraisable exception handling,
and comprehensive error logging and recovery systems.
"""

import sys
import logging
import traceback
import threading
import time
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
import json
import weakref


class ExceptionHandler:
    """Advanced exception handling system"""

    def __init__(self, log_file: str = 'exceptions.log'):
        self.log_file = log_file
        self.original_excepthook = sys.excepthook
        self.original_unraisablehook = sys.unraisablehook
        self.exception_counts: Dict[str, int] = {}
        self.recovery_actions: Dict[str, Callable] = {}
        self.setup_logging()

    def setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def custom_excepthook(self, exc_type, exc_value, exc_traceback):
        """Custom exception hook for uncaught exceptions"""
        # Count exception types
        exc_name = exc_type.__name__
        self.exception_counts[exc_name] = self.exception_counts.get(exc_name, 0) + 1

        # Log the exception
        self.log_exception(exc_type, exc_value, exc_traceback, "Uncaught exception")

        # Print to stderr
        print(f"Uncaught exception logged to {self.log_file}", file=sys.stderr)

        # Call original hook
        self.original_excepthook(exc_type, exc_value, exc_traceback)

    def custom_unraisablehook(self, unraisable):
        """Custom hook for unraisable exceptions"""
        exception = unraisable.exception
        err_msg = unraisable.err_msg

        exc_name = type(exception).__name__
        self.exception_counts[exc_name] = self.exception_counts.get(exc_name, 0) + 1

        # Log unraisable exception
        logging.error(f"Unraisable exception: {exc_name}: {exception} - {err_msg}")

        print(f"Unraisable exception logged to {self.log_file}", file=sys.stderr)

    def log_exception(self, exc_type, exc_value, exc_traceback, context: str = ""):
        """Log an exception with full details"""
        # Format traceback
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_text = ''.join(tb_lines)

        # Create log message
        log_message = f"Exception: {exc_type.__name__}: {exc_value}"
        if context:
            log_message += f" (Context: {context})"

        # Log to file
        logging.error(log_message)
        logging.error("Traceback:\n%s", tb_text)

    def register_recovery(self, exc_type: str, action: Callable):
        """Register recovery action for specific exception type"""
        self.recovery_actions[exc_type] = action

    def attempt_recovery(self, func: Callable, *args, **kwargs):
        """Execute function with recovery"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exc_name = type(e).__name__

            if exc_name in self.recovery_actions:
                print(f"Attempting recovery for {exc_name}...")
                try:
                    recovery_result = self.recovery_actions[exc_name](e)
                    if recovery_result:
                        print("Recovery successful")
                        return recovery_result
                except Exception as recovery_error:
                    print(f"Recovery failed: {recovery_error}")

            # Re-raise if no recovery or recovery failed
            raise

    def install_hooks(self):
        """Install custom exception hooks"""
        sys.excepthook = self.custom_excepthook
        sys.unraisablehook = self.custom_unraisablehook
        print("Custom exception hooks installed")

    def uninstall_hooks(self):
        """Restore original exception hooks"""
        sys.excepthook = self.original_excepthook
        sys.unraisablehook = self.original_unraisablehook
        print("Original exception hooks restored")

    def get_statistics(self) -> Dict[str, Any]:
        """Get exception handling statistics"""
        return {
            'total_exceptions': sum(self.exception_counts.values()),
            'exception_types': self.exception_counts.copy(),
            'recovery_actions': list(self.recovery_actions.keys()),
        }


class ThreadExceptionHandler:
    """Handle exceptions in multi-threaded applications"""

    def __init__(self):
        self.thread_exceptions: Dict[int, Dict[str, Any]] = {}
        self.lock = threading.Lock()

    def thread_excepthook(self, args):
        """Handle thread exceptions"""
        thread_id = args.thread.ident
        exc_type = args.exc_type
        exc_value = args.exc_value
        exc_traceback = args.exc_traceback

        exception_info = {
            'type': exc_type,
            'value': exc_value,
            'traceback': exc_traceback,
            'timestamp': datetime.now(),
            'thread_name': args.thread.name,
        }

        with self.lock:
            self.thread_exceptions[thread_id] = exception_info

        print(f"Exception in thread {args.thread.name} (ID: {thread_id}): {exc_type.__name__}: {exc_value}")

    def get_thread_exceptions(self) -> Dict[int, Dict[str, Any]]:
        """Get all thread exceptions"""
        with self.lock:
            return self.thread_exceptions.copy()

    def clear_exceptions(self):
        """Clear stored thread exceptions"""
        with self.lock:
            self.thread_exceptions.clear()

    def install(self):
        """Install thread exception hook"""
        threading.excepthook = self.thread_excepthook
        print("Thread exception handler installed")

    def uninstall(self):
        """Uninstall thread exception hook"""
        threading.excepthook = threading.__excepthook__
        print("Thread exception handler uninstalled")


def exception_logging_demo():
    """Demonstrate comprehensive exception logging"""
    print("Exception Logging Demo")
    print("=" * 23)

    handler = ExceptionHandler('demo_exceptions.log')

    def risky_function():
        """Function that raises different exceptions"""
        operations = [
            lambda: 1 / 0,  # ZeroDivisionError
            lambda: int("not_a_number"),  # ValueError
            lambda: open("/nonexistent/file.txt"),  # FileNotFoundError
        ]

        for i, op in enumerate(operations, 1):
            try:
                result = op()
                print(f"Operation {i} succeeded: {result}")
            except Exception as e:
                print(f"Operation {i} failed: {type(e).__name__}")
                # Log the exception
                handler.log_exception(type(e), e, e.__traceback__, f"Operation {i}")

    # Test exception logging
    risky_function()

    # Show statistics
    stats = handler.get_statistics()
    print(f"\nException statistics: {stats}")


def recovery_system_demo():
    """Demonstrate exception recovery system"""
    print("Exception Recovery System")
    print("=" * 27)

    handler = ExceptionHandler()

    # Register recovery actions
    def handle_connection_error(e):
        print("Attempting to reconnect...")
        time.sleep(0.5)  # Simulate reconnection
        return "Reconnected successfully"

    def handle_file_error(e):
        print("Attempting to create missing file...")
        try:
            with open("recovery_file.txt", "w") as f:
                f.write("Created by recovery system\n")
            return "File created successfully"
        except:
            return None

    handler.register_recovery("ZeroDivisionError", lambda e: "Division by zero handled")
    handler.register_recovery("ConnectionError", handle_connection_error)
    handler.register_recovery("FileNotFoundError", handle_file_error)

    def test_operations():
        """Test operations that may fail"""

        operations = [
            ("Safe division", lambda: 10 / 2),
            ("Risky division", lambda: 10 / 0),
            ("Safe file open", lambda: open("existing_file.txt", "r")),
            ("Risky file open", lambda: open("nonexistent.txt", "r")),
        ]

        for name, op in operations:
            try:
                result = handler.attempt_recovery(op)
                print(f"{name}: Success - {result}")
            except Exception as e:
                print(f"{name}: Failed - {type(e).__name__}: {e}")

    test_operations()


def custom_hooks_demo():
    """Demonstrate custom exception hooks"""
    print("Custom Exception Hooks Demo")
    print("=" * 28)

    handler = ExceptionHandler('custom_hooks.log')
    handler.install_hooks()

    def cause_uncaught_exception():
        """Cause an uncaught exception"""
        raise RuntimeError("This is an uncaught exception")

    def cause_unraisable_exception():
        """Cause an unraisable exception"""
        # Create a weakref callback that raises an exception
        def bad_callback(ref):
            raise ValueError("Exception in weakref callback")

        obj = [1, 2, 3]
        weak_ref = weakref.ref(obj, bad_callback)

        # Delete object, triggering callback
        del obj

    print("Testing uncaught exception handling...")
    try:
        cause_uncaught_exception()
    except:
        print("Exception was caught and logged")

    print("\nTesting unraisable exception handling...")
    cause_unraisable_exception()

    # Show statistics
    stats = handler.get_statistics()
    print(f"\nFinal statistics: {stats}")

    handler.uninstall_hooks()


def thread_exception_demo():
    """Demonstrate thread exception handling"""
    print("Thread Exception Handling")
    print("=" * 27)

    thread_handler = ThreadExceptionHandler()
    thread_handler.install()

    def thread_with_exception(thread_id):
        """Thread function that raises an exception"""
        time.sleep(0.1 * thread_id)  # Stagger execution

        if thread_id == 1:
            raise ValueError(f"Exception from thread {thread_id}")
        elif thread_id == 2:
            raise RuntimeError(f"RuntimeError from thread {thread_id}")
        else:
            print(f"Thread {thread_id} completed successfully")

    # Start threads
    threads = []
    for i in range(4):
        thread = threading.Thread(target=thread_with_exception, args=(i,))
        thread.name = f"Worker-{i}"
        threads.append(thread)
        thread.start()

    # Wait for threads
    for thread in threads:
        thread.join()

    # Check for exceptions
    thread_exceptions = thread_handler.get_thread_exceptions()
    print(f"\nThread exceptions caught: {len(thread_exceptions)}")

    for thread_id, exc_info in thread_exceptions.items():
        print(f"Thread {thread_id} ({exc_info['thread_name']}): {exc_info['type'].__name__}: {exc_info['value']}")

    thread_handler.uninstall()


def exception_filter_demo():
    """Demonstrate exception filtering and handling"""
    print("Exception Filtering Demo")
    print("=" * 24)

    class ExceptionFilter:
        """Filter and handle exceptions based on criteria"""

        def __init__(self):
            self.filters = []

        def add_filter(self, condition: Callable, handler: Callable):
            """Add a filter with handler"""
            self.filters.append((condition, handler))

        def handle_exception(self, exc_info):
            """Handle exception using filters"""
            exc_type, exc_value, exc_traceback = exc_info

            for condition, handler in self.filters:
                if condition(exc_type, exc_value):
                    return handler(exc_type, exc_value, exc_traceback)

            return False  # No filter matched

    # Create filter
    exc_filter = ExceptionFilter()

    # Add filters
    def is_network_error(exc_type, exc_value):
        return exc_type.__name__ in ('ConnectionError', 'TimeoutError')

    def is_file_error(exc_type, exc_value):
        return exc_type.__name__ in ('FileNotFoundError', 'PermissionError')

    def handle_network_error(exc_type, exc_value, exc_traceback):
        print(f"Network error handled: {exc_value}")
        return "Network recovered"

    def handle_file_error(exc_type, exc_value, exc_traceback):
        print(f"File error handled: {exc_value}")
        return "File error recovered"

    exc_filter.add_filter(is_network_error, handle_network_error)
    exc_filter.add_filter(is_file_error, handle_file_error)

    # Test filtering
    test_exceptions = [
        ("Network error", ConnectionError("Connection failed")),
        ("File error", FileNotFoundError("File not found")),
        ("Other error", ValueError("Some other error")),
    ]

    for desc, exc in test_exceptions:
        try:
            raise exc
        except:
            result = exc_filter.handle_exception(sys.exc_info())
            if result:
                print(f"{desc}: {result}")
            else:
                print(f"{desc}: Not handled by filter")


def comprehensive_error_handler():
    """Comprehensive error handling system"""
    print("Comprehensive Error Handler")
    print("=" * 29)

    class ComprehensiveHandler:
        """Full-featured error handling system"""

        def __init__(self):
            self.error_log = []
            self.error_counts = {}
            self.recovery_attempts = 0
            self.successful_recoveries = 0

        def log_error(self, exc_info, context=""):
            """Log error with context"""
            exc_type, exc_value, exc_traceback = exc_info

            error_entry = {
                'timestamp': datetime.now(),
                'type': exc_type.__name__,
                'value': str(exc_value),
                'context': context,
                'traceback': traceback.format_exc()
            }

            self.error_log.append(error_entry)
            self.error_counts[exc_type.__name__] = self.error_counts.get(exc_type.__name__, 0) + 1

        def attempt_recovery(self, exc_info):
            """Attempt to recover from exception"""
            exc_type, exc_value, exc_traceback = exc_info
            exc_name = exc_type.__name__

            self.recovery_attempts += 1

            # Recovery strategies
            if exc_name == 'FileNotFoundError':
                # Try to create the file
                try:
                    with open('recovered_file.txt', 'w') as f:
                        f.write('Created by recovery system\n')
                    self.successful_recoveries += 1
                    return "File created"
                except:
                    pass

            elif exc_name == 'ZeroDivisionError':
                self.successful_recoveries += 1
                return "Division by zero handled"

            return None

        def handle_exception(self, exc_info, context=""):
            """Handle an exception comprehensively"""
            self.log_error(exc_info, context)

            # Attempt recovery
            recovery_result = self.attempt_recovery(exc_info)
            if recovery_result:
                return recovery_result

            return False

        def get_report(self):
            """Generate error report"""
            return {
                'total_errors': len(self.error_log),
                'error_types': self.error_counts,
                'recovery_rate': self.successful_recoveries / max(self.recovery_attempts, 1),
                'recent_errors': self.error_log[-5:]  # Last 5 errors
            }

    # Test comprehensive handler
    handler = ComprehensiveHandler()

    def test_error_scenarios():
        """Test various error scenarios"""

        scenarios = [
            ("File operation", lambda: open("nonexistent.txt")),
            ("Math operation", lambda: 1 / 0),
            ("Type operation", lambda: int("abc")),
            ("Safe operation", lambda: "safe"),
        ]

        for desc, operation in scenarios:
            try:
                result = operation()
                print(f"{desc}: Success - {result}")
            except Exception as e:
                recovery = handler.handle_exception(sys.exc_info(), desc)
                if recovery:
                    print(f"{desc}: Recovered - {recovery}")
                else:
                    print(f"{desc}: Failed - {type(e).__name__}")

    test_error_scenarios()

    # Show report
    report = handler.get_report()
    print(f"\nError Report:")
    print(f"  Total errors: {report['total_errors']}")
    print(f"  Error types: {report['error_types']}")
    print(".1%")


def main():
    """Main function with different exception handling demonstrations"""

    demos = {
        'logging': exception_logging_demo,
        'recovery': recovery_system_demo,
        'hooks': custom_hooks_demo,
        'threads': thread_exception_demo,
        'filter': exception_filter_demo,
        'comprehensive': comprehensive_error_handler,
    }

    if len(sys.argv) < 2:
        print("Exception Handling Demonstrations")
        print("===================================")
        print()
        print("Available demonstrations:")
        for name in demos.keys():
            print(f"  {name}")
        print()
        print("Usage: python exception_hooks.py <demo_name>")
        print("Example: python exception_hooks.py logging")
        return

    demo_name = sys.argv[1].lower()

    if demo_name in demos:
        try:
            demos[demo_name]()
        except KeyboardInterrupt:
            print("\nDemo interrupted by user")
        except Exception as e:
            print(f"\nDemo failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        sys.stderr.write(f"Unknown demonstration: {demo_name}\n")
        sys.stderr.write(f"Available demos: {', '.join(demos.keys())}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
