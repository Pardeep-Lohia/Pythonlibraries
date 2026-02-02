#!/usr/bin/env python3
"""
Implementation examples for TemporaryFile usage in the tempfile module.

This script demonstrates various ways to use TemporaryFile for anonymous
temporary files that are automatically cleaned up.
"""

import tempfile
import os
import sys
import io


def basic_temporary_file():
    """
    Basic usage of TemporaryFile - creates an anonymous temporary file.
    """
    print("=== Basic TemporaryFile Usage ===")

    # Create an anonymous temporary file
    with tempfile.TemporaryFile() as temp_file:
        print(f"Temporary file created (no accessible filename)")

        # Write some data
        data = b"Hello, this is anonymous temporary data!"
        temp_file.write(data)
        print(f"Wrote {len(data)} bytes to anonymous temporary file")

        # Read the data back
        temp_file.seek(0)  # Go back to beginning
        read_data = temp_file.read()
        print(f"Read back: {read_data.decode()}")

        # File has no accessible name
        try:
            print(f"File name: {temp_file.name}")
        except AttributeError:
            print("TemporaryFile has no 'name' attribute (anonymous)")

    # File is automatically deleted when exiting the context
    print("Anonymous temporary file automatically cleaned up")


def temporary_file_modes():
    """
    Demonstrate different file modes with TemporaryFile.
    """
    print("\n=== TemporaryFile with Different Modes ===")

    # Binary mode (default)
    print("Binary mode:")
    with tempfile.TemporaryFile() as f:
        f.write(b"Binary data for anonymous file")
        f.seek(0)
        print(f"  Read: {f.read()}")

    # Text mode
    print("Text mode:")
    with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as f:
        f.write("Text data: Hello 世界 (Unicode)")
        f.seek(0)
        print(f"  Read: {f.read()}")


def temporary_file_buffering():
    """
    Demonstrate buffering behavior with TemporaryFile.
    """
    print("\n=== TemporaryFile Buffering ===")

    # Default buffering
    print("Default buffering:")
    with tempfile.TemporaryFile() as f:
        print(f"  Buffering: {f.buffering}")
        f.write(b"Data with default buffering")
        print(f"  Raw: {f.raw}")
        print(f"  Buffered: {hasattr(f, 'buffer')}")

    # Line buffering
    print("Line buffering:")
    with tempfile.TemporaryFile(buffering=1) as f:
        print(f"  Buffering: {f.buffering}")
        f.write(b"Line buffered data\n")
        f.write(b"Another line\n")
        f.seek(0)
        print(f"  Read: {f.read().decode()}")


def temporary_file_vs_named_temporary_file():
    """
    Compare TemporaryFile with NamedTemporaryFile.
    """
    print("\n=== TemporaryFile vs NamedTemporaryFile ===")

    print("TemporaryFile (anonymous):")
    with tempfile.TemporaryFile() as f:
        f.write(b"Anonymous data")
        print(f"  Has name attribute: {hasattr(f, 'name')}")
        print(f"  File descriptor: {f.fileno()}")

    print("NamedTemporaryFile (named):")
    with tempfile.NamedTemporaryFile() as f:
        f.write(b"Named data")
        print(f"  Has name attribute: {hasattr(f, 'name')}")
        print(f"  Filename: {f.name}")
        print(f"  File exists: {os.path.exists(f.name)}")


def temporary_file_external_access():
    """
    Show limitations of TemporaryFile for external program access.
    """
    print("\n=== External Program Access Limitations ===")

    # TemporaryFile cannot be accessed by external programs
    # because it has no filename
    with tempfile.TemporaryFile() as temp_file:
        temp_file.write(b"Data for external processing")

        # Cannot pass to external programs
        try:
            # This would fail because there's no filename
            # external_program(temp_file.name)  # AttributeError!
            print("Cannot access TemporaryFile from external programs")
            print("Use NamedTemporaryFile for external access")
        except AttributeError as e:
            print(f"Expected error: {e}")

    # Correct approach for external access
    print("\nCorrect approach with NamedTemporaryFile:")
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Data for external processing")
        temp_file.close()  # Close before external access

        print(f"File accessible at: {temp_file.name}")
        print(f"File exists: {os.path.exists(temp_file.name)}")

        # Now external programs can access it
        # external_program(temp_file.name)

        # Manual cleanup
        os.unlink(temp_file.name)
        print("File manually cleaned up")


def temporary_file_with_io_operations():
    """
    Demonstrate I/O operations with TemporaryFile.
    """
    print("\n=== I/O Operations with TemporaryFile ===")

    with tempfile.TemporaryFile(mode='w+b') as f:
        # Write various data types
        f.write(b"Binary data\n")
        f.write("String data".encode('utf-8'))
        f.write(b"\n")
        f.write(bytearray(b"Bytearray data"))

        # Seek operations
        print(f"File size: {f.tell()} bytes")
        f.seek(0)

        # Read operations
        print("Reading all data:")
        all_data = f.read()
        print(f"  {all_data}")

        # Read line by line
        f.seek(0)
        print("Reading line by line:")
        for line in f:
            print(f"  Line: {line.decode().strip()}")

        # Read specific amount
        f.seek(0)
        chunk = f.read(10)
        print(f"First 10 bytes: {chunk}")


def temporary_file_context_manager_details():
    """
    Show details of TemporaryFile context manager behavior.
    """
    print("\n=== Context Manager Behavior ===")

    temp_file = tempfile.TemporaryFile()
    print("TemporaryFile created")

    try:
        temp_file.write(b"Test data")
        print("Data written")

        # File is still open here
        print(f"File open: {not temp_file.closed}")
        print(f"File descriptor: {temp_file.fileno()}")

    finally:
        temp_file.close()
        print("TemporaryFile closed and cleaned up")

    # File is deleted after close
    print("Context manager exited - file cleaned up")


def temporary_file_error_handling():
    """
    Demonstrate error handling with TemporaryFile.
    """
    print("\n=== Error Handling ===")

    try:
        with tempfile.TemporaryFile() as f:
            # Try to perform invalid operation
            f.write("String data to binary file")
    except TypeError as e:
        print(f"Caught expected type error: {e}")

    # Proper usage
    with tempfile.TemporaryFile(mode='w+b') as f:
        f.write(b"Proper binary data")
        f.seek(0)
        print(f"Successfully wrote: {f.read()}")

    # Handle disk space issues
    try:
        with tempfile.TemporaryFile() as f:
            # Try to write more data than available disk space
            large_data = b"X" * (1024 * 1024 * 1024)  # 1GB
            f.write(large_data)
    except OSError as e:
        print(f"Disk space error (expected): {e}")


def temporary_file_performance_comparison():
    """
    Compare performance of TemporaryFile vs other approaches.
    """
    print("\n=== Performance Comparison ===")

    import time
    test_data = b"X" * (1024 * 1024)  # 1MB

    # TemporaryFile
    start_time = time.time()
    with tempfile.TemporaryFile() as f:
        f.write(test_data)
        f.seek(0)
        _ = f.read()
    temp_time = time.time() - start_time

    # NamedTemporaryFile
    start_time = time.time()
    with tempfile.NamedTemporaryFile() as f:
        f.write(test_data)
        f.seek(0)
        _ = f.read()
    named_time = time.time() - start_time

    # BytesIO (memory only)
    start_time = time.time()
    buffer = io.BytesIO()
    buffer.write(test_data)
    buffer.seek(0)
    _ = buffer.read()
    memory_time = time.time() - start_time

    print(".4f")
    print(".4f")
    print(".4f")

    print("\nPerformance notes:")
    print("- TemporaryFile: Anonymous, auto-cleanup, disk-based")
    print("- NamedTemporaryFile: Named, auto-cleanup, disk-based")
    print("- BytesIO: Anonymous, manual cleanup, memory-based")


def temporary_file_use_cases():
    """
    Demonstrate practical use cases for TemporaryFile.
    """
    print("\n=== Practical Use Cases ===")

    # Use case 1: Data processing pipeline
    print("Data processing pipeline:")
    with tempfile.TemporaryFile(mode='w+b') as temp_buffer:
        # Simulate processing chunks
        for i in range(5):
            chunk = f"Chunk {i} data\n".encode()
            temp_buffer.write(chunk)

        # Process all data at once
        temp_buffer.seek(0)
        processed_data = temp_buffer.read().decode().upper()
        print(f"Processed: {len(processed_data)} characters")

    # Use case 2: Temporary storage for calculations
    print("\nTemporary calculation storage:")
    with tempfile.TemporaryFile() as calc_file:
        results = []
        for i in range(10):
            result = i * i
            results.append(result)
            calc_file.write(f"{result}\n".encode())

        calc_file.seek(0)
        stored_results = [int(line.decode().strip())
                         for line in calc_file if line.strip()]
        print(f"Stored {len(stored_results)} calculation results")

    # Use case 3: Buffer for network data
    print("\nNetwork data buffering:")
    with tempfile.TemporaryFile() as network_buffer:
        # Simulate receiving network packets
        packets = [b"Packet 1", b"Packet 2", b"Packet 3"]
        for packet in packets:
            network_buffer.write(packet)
            network_buffer.write(b"\n")

        # Read all packets
        network_buffer.seek(0)
        all_packets = network_buffer.read()
        packet_count = all_packets.count(b"\n")
        print(f"Buffered {packet_count} network packets")


def main():
    """
    Run all TemporaryFile implementation examples.
    """
    print("TemporaryFile Implementation Examples")
    print("=" * 50)

    basic_temporary_file()
    temporary_file_modes()
    temporary_file_buffering()
    temporary_file_vs_named_temporary_file()
    temporary_file_external_access()
    temporary_file_with_io_operations()
    temporary_file_context_manager_details()
    temporary_file_error_handling()
    temporary_file_performance_comparison()
    temporary_file_use_cases()

    print("\n" + "=" * 50)
    print("All examples completed successfully!")


if __name__ == "__main__":
    main()
