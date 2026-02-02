#!/usr/bin/env python3
"""
SpooledTemporaryFile Usage Examples

This script demonstrates the use of SpooledTemporaryFile for
memory-efficient handling of temporary data that may grow large.
"""

import tempfile
import io
import json
import time


def basic_spooled_file():
    """Basic usage of SpooledTemporaryFile."""
    print("=== Basic SpooledTemporaryFile Usage ===")

    with tempfile.SpooledTemporaryFile(max_size=1024) as f:  # 1KB threshold
        print(f"Initial file type: {type(f)}")

        # Write small amount of data (stays in memory)
        f.write(b"Hello, Spooled File!")
        print(f"After small write: {type(f)}")
        print(f"Current position: {f.tell()}")

        # Read back
        f.seek(0)
        content = f.read()
        print(f"Content: {content}")

    print()


def rollover_behavior():
    """Demonstrate memory to disk rollover."""
    print("=== Memory to Disk Rollover ===")

    # Small threshold to trigger rollover quickly
    max_size = 100  # 100 bytes

    with tempfile.SpooledTemporaryFile(max_size=max_size) as f:
        print(f"Max size: {max_size} bytes")
        print(f"Initial type: {type(f)}")

        # Write data that fits in memory
        small_data = b"Small data " * 3  # ~30 bytes
        f.write(small_data)
        print(f"After small write ({len(small_data)} bytes): {type(f)}")

        # Write more data to trigger rollover
        large_data = b"Large data chunk " * 10  # ~160 bytes
        f.write(large_data)
        print(f"After large write ({len(large_data)} bytes): {type(f)}")
        print(f"Total size: {f.tell()} bytes")

        # Read everything back
        f.seek(0)
        all_content = f.read()
        print(f"Total content length: {len(all_content)}")

    print()


def text_mode_spooled_file():
    """Using SpooledTemporaryFile in text mode."""
    print("=== Text Mode SpooledTemporaryFile ===")

    with tempfile.SpooledTemporaryFile(mode='w+', max_size=512, encoding='utf-8') as f:
        print(f"Mode: {f.mode}")
        print(f"Encoding: {f.encoding}")

        # Write text data
        text_data = "Hello, 世界! " * 20  # Mix of ASCII and Unicode
        f.write(text_data)
        print(f"Written {len(text_data)} characters")

        # Check if rolled over
        print(f"File type: {type(f)}")

        # Read back
        f.seek(0)
        read_text = f.read()
        print(f"Read back: {read_text[:50]}...")  # First 50 chars
        print(f"Content matches: {read_text == text_data}")

    print()


def json_processing():
    """Processing JSON data with SpooledTemporaryFile."""
    print("=== JSON Processing with Spooled File ===")

    # Large JSON data that might exceed memory threshold
    data = {
        "users": [
            {"id": i, "name": f"User {i}", "data": "x" * 100}
            for i in range(50)  # 50 users with 100 chars each
        ],
        "metadata": {
            "version": "1.0",
            "timestamp": "2023-12-07T10:00:00Z",
            "description": "Sample large JSON data"
        }
    }

    with tempfile.SpooledTemporaryFile(mode='w+', max_size=2048) as f:  # 2KB threshold
        # Write JSON
        json.dump(data, f, indent=2)
        f.flush()

        print(f"JSON written, file type: {type(f)}")
        print(f"File size: {f.tell()} bytes")

        # Read back and parse
        f.seek(0)
        loaded_data = json.load(f)

        print(f"Users count: {len(loaded_data['users'])}")
        print(f"First user: {loaded_data['users'][0]}")
        print(f"Data integrity check: {len(loaded_data['users']) == 50}")

    print()


def streaming_data_processing():
    """Simulating streaming data processing."""
    print("=== Streaming Data Processing ===")

    def generate_data_stream():
        """Generator that yields data chunks."""
        for i in range(10):
            yield f"Chunk {i}: {'data' * 50}\n".encode()  # ~250 bytes per chunk
            time.sleep(0.01)  # Simulate I/O delay

    with tempfile.SpooledTemporaryFile(max_size=1024) as f:  # 1KB threshold
        print("Writing streaming data...")

        total_bytes = 0
        for chunk in generate_data_stream():
            f.write(chunk)
            total_bytes += len(chunk)
            print(f"Written {total_bytes} bytes, type: {type(f)}")

        print(f"Total data written: {total_bytes} bytes")
        print(f"Final file type: {type(f)}")

        # Process the accumulated data
        f.seek(0)
        lines = f.readlines()
        print(f"Total lines: {len(lines)}")
        print(f"First line: {lines[0].decode().strip()}")
        print(f"Last line: {lines[-1].decode().strip()}")

    print()


def memory_efficiency_comparison():
    """Compare memory usage with regular file."""
    print("=== Memory Efficiency Comparison ===")

    import sys

    # Test data
    test_data = b"Test data " * 1000  # ~10KB

    print(f"Test data size: {len(test_data)} bytes")

    # Spooled file
    print("\nSpooledTemporaryFile:")
    with tempfile.SpooledTemporaryFile(max_size=2048) as f:  # 2KB threshold
        f.write(test_data)
        print(f"File type: {type(f)}")
        print(f"File size: {f.tell()}")

        # Force rollover by writing more
        f.write(b"Additional data " * 500)  # ~8KB more
        print(f"After additional write: {type(f)}")
        print(f"Total size: {f.tell()}")

    # Regular NamedTemporaryFile for comparison
    print("\nNamedTemporaryFile (comparison):")
    with tempfile.NamedTemporaryFile() as f:
        f.write(test_data)
        print(f"File type: {type(f)}")
        print(f"File size: {f.tell()}")

    print()


def error_handling():
    """Demonstrate error handling with SpooledTemporaryFile."""
    print("=== Error Handling ===")

    try:
        with tempfile.SpooledTemporaryFile(max_size=-1) as f:  # Invalid max_size
            f.write(b"test")
    except (ValueError, TypeError) as e:
        print(f"Caught expected error: {e}")

    # Normal usage with error recovery
    try:
        with tempfile.SpooledTemporaryFile(max_size=1024) as f:
            f.write(b"Some data")

            # Simulate processing error
            if f.tell() > 500:
                raise ValueError("Processing failed")

            f.write(b"More data")

    except ValueError as e:
        print(f"Processing error handled: {e}")
        # File is still properly cleaned up by context manager

    print()


def performance_benchmark():
    """Simple performance comparison."""
    print("=== Performance Benchmark ===")

    import time

    # Test data sizes
    sizes = [1000, 10000, 100000]  # 1KB, 10KB, 100KB

    for size in sizes:
        data = b"x" * size

        # Spooled file
        start = time.time()
        with tempfile.SpooledTemporaryFile(max_size=2048) as f:
            f.write(data)
            f.seek(0)
            _ = f.read()
        spooled_time = time.time() - start

        # Regular temp file
        start = time.time()
        with tempfile.NamedTemporaryFile() as f:
            f.write(data)
            f.seek(0)
            _ = f.read()
        regular_time = time.time() - start

        print(f"Size {size} bytes:")
        print(".4f")
        print(".4f")
        print(".2f")
        print()

    print()


def main():
    """Run all examples."""
    print("SpooledTemporaryFile Usage Examples")
    print("=" * 40)
    print()

    basic_spooled_file()
    rollover_behavior()
    text_mode_spooled_file()
    json_processing()
    streaming_data_processing()
    memory_efficiency_comparison()
    error_handling()
    performance_benchmark()

    print("All examples completed!")


if __name__ == "__main__":
    main()
