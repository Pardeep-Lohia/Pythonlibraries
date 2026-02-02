#!/usr/bin/env python3
"""
Implementation examples for TemporaryDirectory usage in the tempfile module.

This script demonstrates various ways to use TemporaryDirectory for creating
temporary directories that are automatically cleaned up.
"""

import tempfile
import os
import sys
import shutil
from pathlib import Path


def basic_temporary_directory():
    """
    Basic usage of TemporaryDirectory - creates a temporary directory.
    """
    print("=== Basic TemporaryDirectory Usage ===")

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Temporary directory created: {temp_dir}")

        # Create some files in it
        test_file = os.path.join(temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write("Hello from temporary directory!")

        print(f"Created file: {test_file}")
        print(f"File exists: {os.path.exists(test_file)}")

    # Directory is automatically deleted when exiting the context
    print("Temporary directory automatically cleaned up")


def temporary_directory_custom_prefix_suffix():
    """
    Demonstrate custom prefix and suffix with TemporaryDirectory.
    """
    print("\n=== Custom Prefix and Suffix ===")

    with tempfile.TemporaryDirectory(prefix='myapp_', suffix='_temp') as temp_dir:
        print(f"Custom temp directory: {temp_dir}")

        # Create nested structure
        subdir = os.path.join(temp_dir, 'data')
        os.makedirs(subdir)
        with open(os.path.join(subdir, 'file.dat'), 'w') as f:
            f.write("Data file")

    print("Custom temp directory cleaned up")


def temporary_directory_persistence():
    """
    Show how to control persistence of TemporaryDirectory.
    """
    print("\n=== Directory Persistence Control ===")

    # Automatic cleanup with context manager
    with tempfile.TemporaryDirectory() as auto_cleanup:
        print(f"Auto-cleanup directory: {auto_cleanup}")
        with open(os.path.join(auto_cleanup, 'auto.txt'), 'w') as f:
            f.write("Auto cleanup")
    print(f"Auto-cleanup directory exists: {os.path.exists(auto_cleanup)}")

    # Manual cleanup control
    manual_dir = tempfile.TemporaryDirectory()
    try:
        print(f"Manual directory: {manual_dir.name}")
        with open(os.path.join(manual_dir.name, 'manual.txt'), 'w') as f:
            f.write("Manual cleanup")
        print(f"Directory exists before cleanup: {os.path.exists(manual_dir.name)}")
    finally:
        manual_dir.cleanup()
        print(f"Directory exists after cleanup: {os.path.exists(manual_dir.name)}")


def temporary_directory_with_custom_dir():
    """
    Use TemporaryDirectory with custom parent directory.
    """
    print("\n=== Custom Parent Directory ===")

    # Create a custom temp directory
    custom_temp = tempfile.mkdtemp(prefix='parent_')
    print(f"Custom parent directory: {custom_temp}")

    try:
        with tempfile.TemporaryDirectory(dir=custom_temp, prefix='child_') as temp_dir:
            print(f"Child temp directory: {temp_dir}")
            print(f"Is child of parent: {os.path.dirname(temp_dir) == custom_temp}")

            # Create content
            with open(os.path.join(temp_dir, 'content.txt'), 'w') as f:
                f.write("Content in custom location")
    finally:
        # Clean up parent directory
        shutil.rmtree(custom_temp)
        print("Parent directory cleaned up")


def temporary_directory_with_pathlib():
    """
    Demonstrate TemporaryDirectory usage with pathlib.
    """
    print("\n=== TemporaryDirectory with pathlib ===")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create directory structure
        (temp_path / 'config').mkdir()
        (temp_path / 'data' / 'input').mkdir(parents=True)
        (temp_path / 'logs').mkdir()

        # Create files
        (temp_path / 'config' / 'settings.json').write_text('{"debug": true}')
        (temp_path / 'data' / 'input' / 'data.csv').write_text('col1,col2\n1,2\n3,4')

        # List contents
        print("Directory structure:")
        for item in sorted(temp_path.rglob('*')):
            if item.is_file():
                print(f"  File: {item.relative_to(temp_path)}")


def temporary_directory_integration():
    """
    Show integration with other tempfile classes.
    """
    print("\n=== Integration with Other Tempfile Classes ===")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create temporary files within the directory
        temp_files = []
        for i in range(3):
            with tempfile.NamedTemporaryFile(dir=temp_dir, delete=False) as f:
                f.write(f"Content for file {i}".encode())
                temp_files.append(f.name)

        print(f"Created {len(temp_files)} named temp files in temp directory:")
        for name in temp_files:
            print(f"  {name}")

        # Create anonymous temp file
        with tempfile.TemporaryFile(dir=temp_dir) as anon_f:
            anon_f.write(b"Anonymous content")
            print(f"Anonymous file descriptor: {anon_f.fileno()}")

        # Create spooled file
        with tempfile.SpooledTemporaryFile(dir=temp_dir, max_size=1024) as spool_f:
            spool_f.write(b"Spooled content")
            print(f"Spooled file size: {spool_f.tell()}")

    print("All integrated temp files cleaned up with directory")


def temporary_directory_error_handling():
    """
    Demonstrate error handling with TemporaryDirectory.
    """
    print("\n=== Error Handling ===")

    # Handle cleanup errors
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
            # Create a file and make it read-only (simulating cleanup issues)
            test_file = os.path.join(temp_dir, 'readonly.txt')
            with open(test_file, 'w') as f:
                f.write("Read-only file")

            # Make file read-only (on Unix-like systems)
            try:
                os.chmod(test_file, 0o444)
            except OSError:
                pass  # Skip on Windows

            print("Created potentially problematic file")
    except Exception as e:
        print(f"Error occurred: {e}")

    # Normal operation
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Normal operation in: {temp_dir}")


def temporary_directory_use_cases():
    """
    Demonstrate practical use cases for TemporaryDirectory.
    """
    print("\n=== Practical Use Cases ===")

    # Use case 1: Build workspace
    print("Build workspace:")
    with tempfile.TemporaryDirectory(prefix='build_') as build_dir:
        # Simulate build process
        source_dir = os.path.join(build_dir, 'src')
        build_output = os.path.join(build_dir, 'bin')

        os.makedirs(source_dir)
        os.makedirs(build_output)

        # Create source files
        with open(os.path.join(source_dir, 'main.py'), 'w') as f:
            f.write("print('Hello from build')")

        # Simulate compilation
        shutil.copy(os.path.join(source_dir, 'main.py'), build_output)

        print(f"Build completed in: {build_dir}")
        print(f"Output files: {os.listdir(build_output)}")

    # Use case 2: Data processing pipeline
    print("\nData processing pipeline:")
    with tempfile.TemporaryDirectory(prefix='pipeline_') as pipeline_dir:
        # Stage input data
        input_dir = os.path.join(pipeline_dir, 'input')
        temp_dir = os.path.join(pipeline_dir, 'temp')
        output_dir = os.path.join(pipeline_dir, 'output')

        os.makedirs(input_dir)
        os.makedirs(temp_dir)
        os.makedirs(output_dir)

        # Create input data
        with open(os.path.join(input_dir, 'data.txt'), 'w') as f:
            f.write("Raw data\nLine 2\nLine 3")

        # Process data (simulate)
        with open(os.path.join(input_dir, 'data.txt'), 'r') as f:
            data = f.read()

        processed_data = data.upper()

        with open(os.path.join(temp_dir, 'processed.tmp'), 'w') as f:
            f.write(processed_data)

        # Generate output
        with open(os.path.join(output_dir, 'result.txt'), 'w') as f:
            f.write(f"Processed: {len(processed_data)} characters")

        print(f"Pipeline completed in: {pipeline_dir}")
        print(f"Stages: {os.listdir(pipeline_dir)}")


def temporary_directory_performance():
    """
    Compare TemporaryDirectory performance characteristics.
    """
    print("\n=== Performance Characteristics ===")

    import time

    # Measure creation time
    start_time = time.time()
    with tempfile.TemporaryDirectory() as temp_dir:
        creation_time = time.time() - start_time

        # Create some content
        for i in range(10):
            with open(os.path.join(temp_dir, f'file_{i}.txt'), 'w') as f:
                f.write(f'Content {i}\n' * 100)

        # Measure cleanup time
        cleanup_start = time.time()
    cleanup_time = time.time() - cleanup_start

    print(".4f")
    print(".4f")
    print(".4f")


def main():
    """
    Run all TemporaryDirectory implementation examples.
    """
    print("TemporaryDirectory Implementation Examples")
    print("=" * 50)

    basic_temporary_directory()
    temporary_directory_custom_prefix_suffix()
    temporary_directory_persistence()
    temporary_directory_with_custom_dir()
    temporary_directory_with_pathlib()
    temporary_directory_integration()
    temporary_directory_error_handling()
    temporary_directory_use_cases()
    temporary_directory_performance()

    print("\n" + "=" * 50)
    print("All examples completed successfully!")


if __name__ == "__main__":
    main()
