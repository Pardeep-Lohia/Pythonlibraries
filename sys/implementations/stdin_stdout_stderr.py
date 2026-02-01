#!/usr/bin/env python3
"""
Standard Input/Output/Error Streams Implementation

This module demonstrates various ways to work with stdin, stdout, and stderr
using the sys module for stream manipulation and redirection.
"""

import sys
import time
import json
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO


class StreamManager:
    """Manager for standard streams with redirection capabilities"""

    def __init__(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.original_stdin = sys.stdin

    def redirect_stdout_to_file(self, filename: str):
        """Redirect stdout to a file"""
        self.stdout_file = open(filename, 'w')
        sys.stdout = self.stdout_file

    def redirect_stderr_to_file(self, filename: str):
        """Redirect stderr to a file"""
        self.stderr_file = open(filename, 'w')
        sys.stderr = self.stderr_file

    def restore_streams(self):
        """Restore original streams"""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        sys.stdin = self.original_stdin

        # Close any opened files
        if hasattr(self, 'stdout_file'):
            self.stdout_file.close()
        if hasattr(self, 'stderr_file'):
            self.stderr_file.close()


def basic_stream_operations():
    """Demonstrate basic stream operations"""
    print("=== Basic Stream Operations ===")

    # Write to stdout
    sys.stdout.write("This is written to stdout\n")
    sys.stdout.flush()  # Ensure immediate output

    # Write to stderr
    sys.stderr.write("This is written to stderr\n")
    sys.stderr.flush()

    # Read from stdin
    sys.stdout.write("Enter your name: ")
    sys.stdout.flush()
    name = sys.stdin.readline().strip()

    print(f"Hello, {name}!")


def stream_redirection_example():
    """Demonstrate stream redirection"""
    print("=== Stream Redirection Example ===")

    manager = StreamManager()

    # Redirect stdout to file
    manager.redirect_stdout_to_file('output.log')
    print("This goes to the log file")
    print("So does this")

    # Redirect stderr to different file
    manager.redirect_stderr_to_file('errors.log')
    print("This is normal output", file=sys.stdout)
    print("This is an error message", file=sys.stderr)

    # Restore streams
    manager.restore_streams()

    print("Back to normal output")

    # Show contents of log files
    try:
        with open('output.log', 'r') as f:
            print("Output log contents:")
            print(f.read())

        with open('errors.log', 'r') as f:
            print("Error log contents:")
            print(f.read())
    except FileNotFoundError:
        print("Log files not found")


def progress_bar_example():
    """Demonstrate progress bar using stdout"""
    print("=== Progress Bar Example ===")

    def progress_bar(current, total, width=50):
        """Display a progress bar"""
        percentage = current / total
        filled = int(width * percentage)
        bar = '█' * filled + '░' * (width - filled)

        # Use carriage return to overwrite line
        sys.stdout.write(f'\r[{bar}] {current}/{total} ({percentage:.1%})')
        sys.stdout.flush()

        if current == total:
            sys.stdout.write('\n')  # New line when complete

    # Simulate progress
    total_items = 100
    for i in range(total_items + 1):
        progress_bar(i, total_items)
        time.sleep(0.02)  # Simulate work

    print("Progress complete!")


def json_stream_processor():
    """Process JSON data from stdin to stdout"""
    print("=== JSON Stream Processor ===")
    print("Enter JSON objects (one per line), Ctrl+D to end:")

    processed_count = 0
    error_count = 0

    try:
        for line_num, line in enumerate(sys.stdin, 1):
            line = line.strip()
            if not line:
                continue

            try:
                # Parse JSON
                data = json.loads(line)

                # Process data (add metadata)
                data['processed'] = True
                data['line_number'] = line_num
                data['timestamp'] = time.time()

                # Output processed JSON
                json.dump(data, sys.stdout)
                sys.stdout.write('\n')
                sys.stdout.flush()

                processed_count += 1

            except json.JSONDecodeError as e:
                error_msg = f"Line {line_num}: Invalid JSON - {e}"
                sys.stderr.write(error_msg + '\n')
                error_count += 1

    except KeyboardInterrupt:
        sys.stderr.write("\nProcessing interrupted by user\n")

    # Summary
    sys.stderr.write(f"\nProcessing complete: {processed_count} processed, {error_count} errors\n")


def stream_buffering_demo():
    """Demonstrate stream buffering behavior"""
    print("=== Stream Buffering Demo ===")

    print("Normal print (line buffered):", end=' ')
    time.sleep(1)
    print("appears immediately")

    # Force flush
    print("Manual flush:", end=' ')
    sys.stdout.flush()
    time.sleep(1)
    print("after flush")

    # Unbuffered output
    print("Unbuffered output:", end='', flush=True)
    time.sleep(1)
    print(" appears immediately")


def custom_stream_writer():
    """Demonstrate custom stream writer"""
    print("=== Custom Stream Writer ===")

    class UppercaseWriter:
        """A stream writer that converts output to uppercase"""

        def __init__(self, stream):
            self.stream = stream

        def write(self, text):
            """Write text in uppercase"""
            self.stream.write(text.upper())

        def flush(self):
            """Flush the underlying stream"""
            self.stream.flush()

    # Create custom writer
    upper_writer = UppercaseWriter(sys.stdout)

    # Temporarily redirect
    original_stdout = sys.stdout
    sys.stdout = upper_writer

    print("this text will be uppercase")
    print("so will this text")

    # Restore
    sys.stdout = original_stdout

    print("back to normal case")


def error_handling_with_streams():
    """Demonstrate error handling with streams"""
    print("=== Error Handling with Streams ===")

    def safe_write(stream, text):
        """Safely write to a stream with error handling"""
        try:
            stream.write(text)
            stream.flush()
        except (OSError, IOError) as e:
            # Fallback to stderr
            sys.stderr.write(f"Write error: {e}\n")
            return False
        return True

    def safe_read(stream):
        """Safely read from a stream"""
        try:
            return stream.readline()
        except (OSError, IOError) as e:
            sys.stderr.write(f"Read error: {e}\n")
            return None

    # Test safe operations
    safe_write(sys.stdout, "Safe write to stdout\n")

    # Simulate writing to closed stream
    closed_buffer = StringIO()
    closed_buffer.close()
    safe_write(closed_buffer, "This will fail safely\n")

    print("Error handling demonstration complete")


def context_manager_redirection():
    """Demonstrate stream redirection using context managers"""
    print("=== Context Manager Redirection ===")

    # Using contextlib.redirect_stdout
    output_buffer = StringIO()
    with redirect_stdout(output_buffer):
        print("This goes to the buffer")
        print("So does this")

    print("Captured output:")
    print(repr(output_buffer.getvalue()))

    # Using contextlib.redirect_stderr
    error_buffer = StringIO()
    with redirect_stderr(error_buffer):
        import warnings
        warnings.warn("This warning goes to the buffer")

    print("Captured errors:")
    print(repr(error_buffer.getvalue()))


def interactive_cli_builder():
    """Build an interactive CLI using stdin/stdout"""
    print("=== Interactive CLI Builder ===")

    def get_input(prompt, validator=None, error_msg="Invalid input"):
        """Get validated input from user"""
        while True:
            sys.stdout.write(prompt)
            sys.stdout.flush()

            response = sys.stdin.readline().strip()

            if validator is None or validator(response):
                return response

            sys.stderr.write(error_msg + '\n')

    def is_number(text):
        """Check if text is a valid number"""
        try:
            float(text)
            return True
        except ValueError:
            return False

    def is_yes_no(text):
        """Check if text is y/n"""
        return text.lower() in ['y', 'yes', 'n', 'no']

    # Interactive session
    name = get_input("What is your name? ")
    age = float(get_input("What is your age? ", is_number, "Please enter a valid number"))

    continue_prompt = get_input("Continue? (y/n): ", is_yes_no, "Please enter y/yes or n/no")

    if continue_prompt.lower() in ['y', 'yes']:
        print(f"Hello {name}, you are {age} years old!")
    else:
        print("Goodbye!")


def main():
    """Main function to run different stream examples"""

    examples = {
        'basic': basic_stream_operations,
        'redirect': stream_redirection_example,
        'progress': progress_bar_example,
        'json': json_stream_processor,
        'buffer': stream_buffering_demo,
        'custom': custom_stream_writer,
        'error': error_handling_with_streams,
        'context': context_manager_redirection,
        'interactive': interactive_cli_builder,
    }

    if len(sys.argv) < 2:
        print("Standard I/O Streams Examples")
        print("==============================")
        print()
        print("Available examples:")
        for name in examples.keys():
            print(f"  {name}")
        print()
        print("Usage: python stdin_stdout_stderr.py <example_name>")
        print("Example: python stdin_stdout_stderr.py basic")
        return

    example_name = sys.argv[1].lower()

    if example_name in examples:
        examples[example_name]()
    else:
        sys.stderr.write(f"Unknown example: {example_name}\n")
        sys.stderr.write(f"Available examples: {', '.join(examples.keys())}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
