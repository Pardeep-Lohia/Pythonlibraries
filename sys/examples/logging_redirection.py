#!/usr/bin/env python3
"""
Logging and Output Redirection Example

Demonstrates how to redirect stdout, stderr, and implement custom logging
using sys module capabilities.
"""

import sys
import os
import time
import logging
from datetime import datetime
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
import threading


class OutputRedirector:
    """Advanced output redirection manager"""

    def __init__(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.log_file = None
        self.buffer = StringIO()

    @contextmanager
    def redirect_to_file(self, filename: str, mode: str = 'a'):
        """Context manager to redirect output to file"""
        self.log_file = open(filename, mode)

        # Create custom streams that write to both buffer and file
        class TeeStream:
            def __init__(self, stream, file):
                self.stream = stream
                self.file = file

            def write(self, text):
                self.stream.write(text)
                self.file.write(text)
                self.stream.flush()
                self.file.flush()

            def flush(self):
                self.stream.flush()
                self.file.flush()

        old_stdout = sys.stdout
        old_stderr = sys.stderr

        sys.stdout = TeeStream(old_stdout, self.log_file)
        sys.stderr = TeeStream(old_stderr, self.log_file)

        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            self.log_file.close()
            self.log_file = None

    @contextmanager
    def redirect_to_buffer(self):
        """Context manager to redirect output to internal buffer"""
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        sys.stdout = self.buffer
        sys.stderr = self.buffer

        try:
            yield self.buffer
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def get_buffer_content(self) -> str:
        """Get content from internal buffer"""
        return self.buffer.getvalue()

    def clear_buffer(self):
        """Clear internal buffer"""
        self.buffer = StringIO()


class Logger:
    """Custom logger using sys streams"""

    def __init__(self, name: str = "app", level: str = "INFO"):
        self.name = name
        self.level = self._parse_level(level)
        self.level_names = {0: 'DEBUG', 1: 'INFO', 2: 'WARNING', 3: 'ERROR'}

    def _parse_level(self, level: str) -> int:
        levels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}
        return levels.get(level.upper(), 1)

    def _should_log(self, level: int) -> bool:
        return level >= self.level

    def _format_message(self, level: int, message: str) -> str:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        level_name = self.level_names.get(level, 'UNKNOWN')
        return f"[{timestamp}] {self.name} {level_name}: {message}"

    def debug(self, message: str):
        if self._should_log(0):
            print(self._format_message(0, message), file=sys.stdout)

    def info(self, message: str):
        if self._should_log(1):
            print(self._format_message(1, message), file=sys.stdout)

    def warning(self, message: str):
        if self._should_log(2):
            print(self._format_message(2, message), file=sys.stderr)

    def error(self, message: str):
        if self._should_log(3):
            print(self._format_message(3, message), file=sys.stderr)


class ProgressLogger:
    """Logger for progress tracking with visual indicators"""

    def __init__(self):
        self.start_time = None
        self.last_update = 0

    def start(self, message: str = "Starting operation..."):
        """Start progress tracking"""
        self.start_time = time.time()
        print(message, file=sys.stderr)
        sys.stderr.flush()

    def update(self, current: int, total: int, message: str = ""):
        """Update progress"""
        now = time.time()
        if now - self.last_update < 0.1:  # Throttle updates
            return

        self.last_update = now

        percentage = (current / total) * 100
        elapsed = now - self.start_time
        eta = (elapsed / current) * (total - current) if current > 0 else 0

        # Create progress bar
        width = 40
        filled = int(width * current / total)
        bar = '█' * filled + '░' * (width - filled)

        # Clear line and print progress
        sys.stderr.write('\r')
        sys.stderr.write(f'[{bar}] {current}/{total} ({percentage:.1f}%) ETA: {eta:.1f}s')
        if message:
            sys.stderr.write(f' - {message}')
        sys.stderr.flush()

    def complete(self, message: str = "Complete"):
        """Mark progress as complete"""
        elapsed = time.time() - self.start_time
        sys.stderr.write('\n')
        sys.stderr.write(f"{message} (took {elapsed:.2f}s)\n")
        sys.stderr.flush()


def basic_redirection_demo():
    """Demonstrate basic output redirection"""
    print("=== Basic Output Redirection ===")

    redirector = OutputRedirector()

    print("1. Normal output:")
    print("This goes to console")
    print("So does this", file=sys.stderr)

    print("\n2. Redirected to buffer:")
    with redirector.redirect_to_buffer() as buffer:
        print("This goes to buffer")
        print("And this too", file=sys.stderr)

    print("Buffer content:")
    print(repr(redirector.get_buffer_content()))

    print("\n3. Redirected to file:")
    with redirector.redirect_to_file('demo_output.log', 'w'):
        print("This goes to file and console")
        print("Errors too", file=sys.stderr)

    print("Check demo_output.log for the redirected output")


def logging_demo():
    """Demonstrate custom logging"""
    print("=== Custom Logging Demo ===")

    # Create logger
    logger = Logger("demo", "DEBUG")

    print("Logging at different levels:")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    print("\nChanging log level to WARNING:")
    logger.level = 2
    logger.debug("This debug message won't show")
    logger.info("This info message won't show")
    logger.warning("This warning will show")
    logger.error("This error will show")


def progress_demo():
    """Demonstrate progress logging"""
    print("=== Progress Logging Demo ===")

    progress = ProgressLogger()
    progress.start("Processing items...")

    total_items = 100
    for i in range(total_items + 1):
        # Simulate work
        time.sleep(0.02)

        # Update progress
        if i % 10 == 0:
            progress.update(i, total_items, f"Processed {i} items")

    progress.complete("All items processed")


def multi_threaded_logging():
    """Demonstrate logging in multi-threaded environment"""
    print("=== Multi-threaded Logging ===")

    def worker_thread(thread_id: int, logger: Logger):
        """Worker thread function"""
        for i in range(5):
            logger.info(f"Thread {thread_id}: Message {i+1}")
            time.sleep(0.1)

    # Create logger
    logger = Logger("multithread", "INFO")

    # Start threads
    threads = []
    for i in range(3):
        thread = threading.Thread(target=worker_thread, args=(i+1, logger))
        threads.append(thread)
        thread.start()

    # Wait for threads
    for thread in threads:
        thread.join()

    print("All threads completed")


def error_handling_with_logging():
    """Demonstrate error handling with logging"""
    print("=== Error Handling with Logging ===")

    logger = Logger("error_demo", "INFO")

    def risky_operation(name: str):
        """Simulate a risky operation"""
        logger.info(f"Starting operation: {name}")

        try:
            if name == "division":
                result = 1 / 0
            elif name == "file":
                with open("/nonexistent/file", "r") as f:
                    content = f.read()
            elif name == "type":
                result = int("not_a_number")
            else:
                result = f"Success: {name}"

            logger.info(f"Operation {name} completed: {result}")
            return result

        except Exception as e:
            logger.error(f"Operation {name} failed: {type(e).__name__}: {e}")
            return None

    # Test different operations
    operations = ["division", "file", "type", "safe_operation"]

    for op in operations:
        result = risky_operation(op)
        if result:
            print(f"✓ {op}: {result}")
        else:
            print(f"✗ {op}: Failed")


def context_manager_demo():
    """Demonstrate using context managers for redirection"""
    print("=== Context Manager Redirection ===")

    # Using built-in contextlib
    print("1. Using redirect_stdout:")
    buffer = StringIO()
    with redirect_stdout(buffer):
        print("This goes to buffer")
        print("So does this")

    print("Buffer content:")
    print(repr(buffer.getvalue()))

    print("\n2. Using redirect_stderr:")
    error_buffer = StringIO()
    with redirect_stderr(error_buffer):
        import warnings
        warnings.warn("This warning goes to buffer")

    print("Error buffer content:")
    print(repr(error_buffer.getvalue()))

    print("\n3. Combined redirection:")
    out_buffer = StringIO()
    err_buffer = StringIO()

    with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
        print("Normal output to buffer")
        print("Error output to buffer", file=sys.stderr)

    print("Combined output:")
    print("STDOUT:", repr(out_buffer.getvalue()))
    print("STDERR:", repr(err_buffer.getvalue()))


def file_logging_system():
    """Demonstrate a complete file logging system"""
    print("=== File Logging System ===")

    class FileLogger:
        """Complete file logging system"""

        def __init__(self, base_filename: str = "app"):
            self.base_filename = base_filename
            self.log_file = None
            self.open_log_file()

        def open_log_file(self):
            """Open log file with timestamp"""
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.base_filename}_{timestamp}.log"
            self.log_file = open(filename, 'w')
            print(f"Logging to: {filename}")

        def log(self, level: str, message: str):
            """Log a message"""
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"[{timestamp}] {level}: {message}\n"

            # Write to file
            self.log_file.write(log_entry)
            self.log_file.flush()

            # Also write to appropriate stream
            if level in ['ERROR', 'WARNING']:
                sys.stderr.write(log_entry)
            else:
                sys.stdout.write(log_entry)

        def close(self):
            """Close log file"""
            if self.log_file:
                self.log_file.close()

    # Test file logging
    logger = FileLogger("demo")

    try:
        logger.log("INFO", "Application started")
        logger.log("DEBUG", "Initializing components")

        # Simulate some operations
        for i in range(3):
            logger.log("INFO", f"Processing item {i+1}")
            time.sleep(0.1)

            if i == 1:
                logger.log("WARNING", "Slow operation detected")

        logger.log("ERROR", "Simulated error occurred")
        logger.log("INFO", "Application finished")

    finally:
        logger.close()

    print("Check the log file for complete output")


def main():
    """Main function with different logging demonstrations"""

    demos = {
        'basic': basic_redirection_demo,
        'logging': logging_demo,
        'progress': progress_demo,
        'threaded': multi_threaded_logging,
        'errors': error_handling_with_logging,
        'context': context_manager_demo,
        'filelog': file_logging_system,
    }

    if len(sys.argv) < 2:
        print("Logging and Output Redirection Examples")
        print("========================================")
        print()
        print("Available demonstrations:")
        for name in demos.keys():
            print(f"  {name}")
        print()
        print("Usage: python logging_redirection.py <demo_name>")
        print("Example: python logging_redirection.py basic")
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
